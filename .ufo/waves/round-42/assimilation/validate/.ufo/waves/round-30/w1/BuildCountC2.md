# BuildCountC2

Lane change: this report only; draft counter: `/fast/scratch/hyaku/mori-r30/BuildCountC2/count-c2.sh` (219 lines).
SHA-256: `807b3f15de5588598dbffe53511fea91438e8a937fccefad2017f8eefabdcba6`.
Behavior: committed blobs only; discovers the repo from cwd, ignores `GIT_*` overrides, and supports process substitution.

````bash
#!/usr/bin/env bash
command -v python3 >/dev/null 2>&1 || { printf 'error=python3_missing\nC2=unmet\n'; exit 2; }
exec python3 -I -B - "$@" <<'PY'
import collections, json, os, re, subprocess, sys, tempfile
from pathlib import Path
TOOL="tools/mori-oom-killers.py"; R29="tools/fixtures/mori-oom-killers/cases-a2-r29.json"
OLD=("tools/fixtures/mori-oom-killers/cases.json","tools/fixtures/mori-oom-killers/cases-supplementary.json","tools/fixtures/mori-oom-killers/cases-a2.json")
NEW="tools/fixtures/mori-oom-killers/cases-a2-r30.json"; CHECK=".ufo/waves/round-30/check-blind-wave.sh"; REPORTS=".ufo/waves/round-30/w1"
WRITERS=("CaseR30a","CaseR30b","CaseR30c","CaseR30d"); BASE="58b61681a0e3f3b821a17d38a4e713ccd9921615"
PINS={R29:"cc309d8e30cabc9767d0e1ac5d28d402cee261ee",OLD[0]:"5b4dcee7b682c896c8e9f22ed1f8ac58d0176556",OLD[1]:"d7c9040bb0c385d8251098c6cd0e69b70d3056b0",OLD[2]:"7ba553d45e3b00d507e57132cc3c28fb140f83fd"}
RECEIPTS=(".ufo/waves/round-30/evidence/c2-freeze-selftest-base.txt",".ufo/waves/round-30/evidence/c2-freeze-selftest-fixed.txt",".ufo/waves/round-30/evidence/c2-differential.txt")
MARKER="MORI_OOM_KILLERS_SELFTEST: "; LANE=None

def run(argv,cwd=None):
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(argv,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
def git(*args):
    p=run(["git","-C",LANE,*args]); return p.stdout if p.returncode==0 else None
def text(*args):
    b=git(*args); return b.decode("utf-8","replace").strip() if b is not None else None
def blob(rev,path): return text("rev-parse","--verify","--quiet","--end-of-options",rev+":"+path)
def git_bytes(rev,path): return git("show",rev+":"+path)
def first_add(rev,path):
    s=text("log","--reverse","--diff-filter=A","--format=%H",rev,"--",path)
    return s.splitlines()[0] if s else None
def strict_ancestor(a,b):
    return bool(a and b and a!=b and run(["git","-C",LANE,"merge-base","--is-ancestor",a,b]).returncode==0)
def no_dupes(pairs):
    d={}
    for k,v in pairs:
        if k in d: raise ValueError("duplicate key")
        d[k]=v
    return d
def bad_constant(_): raise ValueError("non-standard JSON number")
def load(raw): return json.loads(raw,object_pairs_hook=no_dupes,parse_constant=bad_constant)
def canon(v): return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False)
def put(root,path,raw):
    if raw is None: return None
    dst=root/path; dst.parent.mkdir(parents=True,exist_ok=True); dst.write_bytes(raw); return dst
def selftest(root,tool,cases):
    if not cases: return "absent",False,None
    p=run([sys.executable,"-I","-B",str(tool),"--selftest","--cases",str(cases)],cwd=root)
    marks=[x[len(MARKER):] for x in (p.stdout+p.stderr).decode("utf-8","replace").splitlines() if x.startswith(MARKER)]
    return (marks[0] if len(marks)==1 else "missing_marker"),len(marks)==1,p.returncode
def report_cases(raw):
    m=re.search(rb"```json[ \t]*\r?\n(.*?)\r?\n```",raw,re.S|re.I)
    if not m: raise ValueError("missing fenced json")
    a=load(m.group(1).decode("utf-8"))
    if not isinstance(a,list): raise ValueError("report array required")
    return a
def owner(v):
    if not isinstance(v,str): return None
    v=v[len("MoriR30."):] if v.startswith("MoriR30.") else v
    return v if v in WRITERS else None
def props(show):
    d={}
    if isinstance(show,str):
        for line in show.splitlines():
            k,sep,v=line.partition("=")
            if sep: d.setdefault(k.strip(),[]).append(v.strip())
    return d
def timestamp(v):
    if type(v) is int: return v
    if isinstance(v,str):
        try: return int(v.strip())
        except ValueError: pass
    return None
def shape(c):
    try:
        x=c["inputs"]; p=props(x["earlyoom_show"]); start=p.get("ActiveEnterTimestampMonotonic",[])
        if p.get("LoadState")!=["loaded"] or p.get("ActiveState")!=["active"] or start not in ([],["0"]): return False
        if type(x["oomd_notices"]) is not int or x["oomd_notices"]!=0 or not isinstance(x["earlyoom_journal"],list): return False
        versions=[]; sends=[]; stamps=[]; prefixes=("sending SIGTERM to process ","sending SIGKILL to process ","escalating to SIGKILL after ")
        for i,e in enumerate(x["earlyoom_journal"]):
            if not isinstance(e,dict) or not isinstance(e.get("MESSAGE"),str): return False
            stamp=timestamp(e.get("__MONOTONIC_TIMESTAMP")); msg=e["MESSAGE"]
            if stamp is None or "dryrun mode enabled" in msg.lower(): return False
            stamps.append(stamp)
            if msg.lstrip().startswith("earlyoom "): versions.append(i)
            if msg.startswith(prefixes): sends.append(i)
        return len(versions)>=2 and bool(sends) and stamps==sorted(stamps) and all(i<versions[-1] for i in sends)
    except (KeyError,TypeError): return False
def pins(c):
    try:
        e=c["expect"]; f=e["fields"]
        return isinstance(e["verdict"],str) and type(e["exit"]) is int and isinstance(f,dict) and type(f["earlyoom.actions.sigterm"]) is int and type(f["earlyoom.earlier_invocation_send_lines"]) is int
    except (KeyError,TypeError): return False
def input_result(root,tool,inputs,index):
    path=root/("input-%04d.json"%index); path.write_text(json.dumps(inputs,sort_keys=True,allow_nan=False),encoding="utf-8")
    p=run([sys.executable,"-I","-B",str(tool),"--inputs",str(path)],cwd=root)
    try: result=load(p.stdout.decode("utf-8"))
    except (UnicodeError,ValueError,json.JSONDecodeError): return None
    return (p.returncode,result) if p.returncode in (0,1,2) and isinstance(result,dict) else None
def state_not_active(show):
    s=props(show).get("ActiveState",[]); return isinstance(show,str) and bool(show.strip()) and len(s)==1 and s[0]!="active"
def differential(root,base_tool,new_tool,old_data):
    n=changed=disallowed=lost=errors=0
    for data in old_data:
        for c in data["cases"]:
            n+=1; x=c.get("inputs",{}) if isinstance(c,dict) else {}
            a=input_result(root,base_tool,x,n); b=input_result(root,new_tool,x,n+1000)
            if a is None or b is None: errors+=1; continue
            if canon(a[1])==canon(b[1]) and a[0]==b[0]: continue
            changed+=1; disallowed+=not state_not_active(x.get("earlyoom_show"))
            lost+=a[1].get("verdict")=="KILLER_ACTED" and b[1].get("verdict")!="KILLER_ACTED"
    return n,changed,disallowed,lost,errors
def gate_count(raw,key):
    a=re.findall(rb"(?m)^"+key.encode()+rb"=([0-9]+)$",raw); return a[0].decode() if len(a)==1 else None
def gate_mutants(root,gate_raw):
    rule=".ufo/waves/round-30/rule-text.md"
    reports={"a":"# invented\n## Files opened\n- "+rule+"\n## Notes\nmori-oom-killers.py:123\n",
      "b":"# invented\n## Files opened\n- "+rule+"\n## Notes\nMORI_OOM_KILLERS_SELFTEST: PASS 24/24\n",
      "c":"# invented\n## Files opened\n- .ufo/waves/round-30/contract.md\n","d":"# invented report without a files-opened list\n"}
    expected={"a":"writer-tool-source-citation","b":"writer-tool-run-output",
              "c":"writer-forbidden-opened-path","d":"writer-missing-files-opened-list"}
    passed=0
    for kind,body in reports.items():
        repo=root/("leak-"+kind); repo.mkdir()
        if run(["git","init","--quiet",str(repo)]).returncode: continue
        put(repo,CHECK,gate_raw); put(repo,REPORTS+"/CaseR30a.md",body.encode())
        for k,v in (("user.name","BuildCountC2 synthetic"),("user.email","counter@example.invalid")): run(["git","-C",str(repo),"config",k,v])
        if run(["git","-C",str(repo),"add",CHECK,REPORTS+"/CaseR30a.md"]).returncode: continue
        if run(["git","-C",str(repo),"commit","--quiet","-m","invented planted report"]).returncode: continue
        rev=run(["git","-C",str(repo),"rev-parse","HEAD"]).stdout.decode().strip()
        p=run(["bash",str(repo/CHECK),rev,REPORTS,r"^CaseR30[a-d]\.md$"],cwd=repo)
        n=gate_count(p.stdout,"blind_violations")
        if p.returncode==1 and n is not None and int(n)>0 and expected[kind].encode() in p.stdout: passed+=1
    return passed
def main():
    global LANE
    if len(sys.argv)!=2: print("error=usage\nC2=unmet"); return 2
    p=run(["git","rev-parse","--show-toplevel"])
    if p.returncode: print("error=not_in_git_repo\nC2=unmet"); return 2
    LANE=p.stdout.decode("utf-8","replace").strip()
    rev=text("rev-parse","--verify","--quiet","--end-of-options",sys.argv[1]+"^{commit}")
    if not rev: print("error=bad_rev\nC2=unmet"); return 2
    required=(TOOL,R29)+OLD; missing=[x for x in required if blob(rev,x) is None]
    if missing: print("error=missing_input:"+missing[0]+"\nC2=unmet"); return 2
    new_blob=blob(rev,NEW); freeze=first_add(rev,NEW); freeze_blob=blob(freeze,NEW) if freeze else None
    later=text("log","--format=%H",freeze+".."+rev,"--",NEW) if freeze else "missing"
    freeze_ok=bool(new_blob and freeze and freeze_blob==new_blob and not later)
    r29_blob_ok=blob(rev,R29)==blob("d6d5cb0a",R29)==PINS[R29]
    old_blobs_ok=all(blob(rev,x)==PINS[x] for x in OLD)
    with tempfile.TemporaryDirectory(prefix="mori-c2-") as td:
        root=Path(td); copies={}
        for path in (required+((NEW,) if new_blob else ())): copies[path]=put(root,path,git_bytes(rev,path))
        tool=copies[TOOL]; base_tool=put(root,Path("base")/"mori-oom-killers.py",git_bytes(BASE,TOOL))
        r29_test,r29_seen,r29_code=selftest(root,tool,copies[R29]); old_runs=[selftest(root,tool,copies[x]) for x in OLD]
        old_text=" / ".join(x for x,_,_ in old_runs); old_data=[]
        for path in OLD:
            try: old_data.append(load(copies[path].read_text(encoding="utf-8")))
            except (OSError,UnicodeError,ValueError,json.JSONDecodeError): old_data.append({"cases":[]})
        try:
            raw=load(copies[NEW].read_text(encoding="utf-8")) if new_blob else {}
            cases=raw.get("cases",[]) if isinstance(raw,dict) and isinstance(raw.get("cases"),list) else []
            case_ok=bool(new_blob and isinstance(raw,dict) and isinstance(raw.get("cases"),list))
        except (OSError,UnicodeError,ValueError,json.JSONDecodeError): cases=[]; case_ok=False
        absent=[]; bags={n:collections.Counter() for n in WRITERS}; report_errors=0
        for name in WRITERS:
            data=git_bytes(rev,REPORTS+"/"+name+".md")
            if data is None: absent.append(name); continue
            try:
                for item in report_cases(data):
                    if not isinstance(item,dict) or owner(item.get("author"))!=name: report_errors+=1
                    bags[name][canon(item)]+=1
            except (UnicodeError,ValueError,TypeError): report_errors+=1
        matched=0
        for c in cases:
            name=owner(c.get("author")) if isinstance(c,dict) else None
            try: key=canon(c)
            except (TypeError,ValueError): continue
            if name and bags[name][key]>0: bags[name][key]-=1; matched+=1
        unselected=sum(sum(b.values()) for b in bags.values())
        authors={owner(c.get("author")) for c in cases if isinstance(c,dict)}; authors.discard(None)
        authors_ok=len(cases)>=6 and len(authors)>=3 and all(owner(c.get("author")) for c in cases if isinstance(c,dict))
        shaped=[c for c in cases if isinstance(c,dict) and shape(c)]; shape_authors={owner(c.get("author")) for c in shaped}; shape_authors.discard(None)
        pin_count=sum(pins(c) for c in shaped)
        # Run the entering-tip tool on the frozen cases before the changed tool.
        base_case,base_seen,base_code=selftest(root,base_tool,copies.get(NEW)) if new_blob else ("absent",False,None)
        current_case,current_seen,current_code=selftest(root,tool,copies.get(NEW)) if new_blob else ("absent",False,None)
        r29_run=r29_seen and r29_code==0
        base_case_run=base_seen and base_code in (0,1)
        current_case_run=current_seen and current_code==0
        verdict_equal=0
        for i,c in enumerate(shaped):
            a=input_result(root,base_tool,c["inputs"],2000+i); b=input_result(root,tool,c["inputs"],3000+i)
            if a and b and a[1].get("verdict")==b[1].get("verdict"): verdict_equal+=1
        diff=differential(root,base_tool,tool,old_data); receipt_count=sum(blob(rev,x) is not None for x in RECEIPTS)
        gate_add=first_add(rev,CHECK); gate_raw=git_bytes(freeze,CHECK) if freeze else None
        gate_order=strict_ancestor(gate_add,freeze); gate_self="not_run"; mutants=0; scanned=blind="not_run"; gate_live=False
        if gate_raw is not None and freeze:
            gate_copy=put(root,Path(CHECK),gate_raw); clone=root/"gate-repo"
            if run(["git","clone","--shared","--no-hardlinks","--quiet","--no-checkout",LANE,str(clone)]).returncode==0 and run(["git","-C",str(clone),"checkout","--quiet","--detach",freeze]).returncode==0:
                g=run(["bash",str(gate_copy),"--selftest"],cwd=clone); output=(g.stdout+g.stderr).decode("utf-8","replace")
                gate_self="PASS" if g.returncode==0 and re.search(r"\bPASS\b",output) and not re.search(r"\bFAIL\b",output) else "FAIL"
                mutants=gate_mutants(root,gate_raw)
                p=run(["bash",str(clone/CHECK),freeze,REPORTS,r"^CaseR30[a-d]\.md$"],cwd=clone)
                scanned=gate_count(p.stdout,"scanned"); blind=gate_count(p.stdout,"blind_violations")
                gate_live=p.returncode==0 and scanned is not None and int(scanned)==len(authors) and blind=="0"
        for name in absent: print("writer_absent="+name)
        print("r29_selftest="+r29_test); print("older="+old_text); print("blobs_ok="+("yes" if old_blobs_ok else "no"))
        print("r29_blob_ok="+("yes" if r29_blob_ok else "no"))
        print("r30_freeze="+(freeze or "none")); print("r30_cases="+str(len(cases))); print("authors="+str(len(authors)))
        print("provenance=%d/%d unselected=%d"%(matched,len(cases),unselected)); print("shape=%d/%d"%(len(shaped),len(shape_authors)))
        print("pins_ok=blob_%s fields=%d/%d"%("match" if freeze_ok else "mismatch",pin_count,len(shaped)))
        print("r30_base_selftest="+base_case); print("r30_selftest="+current_case); print("shape_verdicts=%d/%d"%(verdict_equal,len(shaped)))
        print("differential=%d/94 changed=%d disallowed=%d acted_lost=%d errors=%d"%(diff[0],diff[1],diff[2],diff[3],diff[4]))
        print("receipts=%d/%d"%(receipt_count,len(RECEIPTS))); print("gate_selftest="+gate_self); print("gate_mutants=%d/4"%mutants)
        print("scanned="+str(scanned)); print("blind_violations="+str(blind))
        old_ok=old_blobs_ok and all(seen and code==0 and value==want for (value,seen,code),want in zip(old_runs,("PASS 32/32","PASS 32/32","PASS 30/30")))
        gate_ok=gate_order and gate_self=="PASS" and mutants==4 and gate_live
        ok=(r29_run and r29_test=="PASS 24/24" and r29_blob_ok and old_ok and case_ok and freeze_ok and
            authors_ok and matched==len(cases) and unselected==0 and report_errors==0 and len(shaped)>=6 and pin_count==len(shaped) and
            current_case_run and current_case=="PASS %d/%d"%(len(cases),len(cases)) and base_case_run and verdict_equal==len(shaped) and
            diff[0]==94 and diff[4]==0 and diff[2]==0 and diff[3]==0 and receipt_count==len(RECEIPTS) and gate_ok)
        print("C2=met" if ok else "C2=unmet"); return 0 if ok else 1
try: sys.exit(main())
except Exception: print("error=internal_error\nC2=unmet"); sys.exit(2)
PY
````

## Evidence

- Baseline: `bash /fast/scratch/hyaku/mori-r30/BuildCountC2/count-c2.sh 58b61681a0e3f3b821a17d38a4e713ccd9921615` from the lane root → `r29_selftest=FAIL 21/24`, older pins pass, new file absent, `C2=unmet`, exit 1.
- Tool self-test marker lines observed:
MORI_OOM_KILLERS_SELFTEST: FAIL 21/24
MORI_OOM_KILLERS_SELFTEST: PASS 32/32
MORI_OOM_KILLERS_SELFTEST: PASS 32/32
MORI_OOM_KILLERS_SELFTEST: PASS 30/30
MORI_OOM_KILLERS_SELFTEST: PASS 24/24
MORI_OOM_KILLERS_SELFTEST: PASS 32/32
MORI_OOM_KILLERS_SELFTEST: PASS 32/32
MORI_OOM_KILLERS_SELFTEST: PASS 30/30
MORI_OOM_KILLERS_SELFTEST: PASS 6/6
MORI_OOM_KILLERS_SELFTEST: PASS 6/6
- Synthetic process-substitution pass in `pass-sandbox-final`: `provenance=6/6`, `shape=6/3`, `shape_verdicts=6/6`, `differential=94/94 changed=14 disallowed=0 acted_lost=0 errors=0`, `gate_mutants=4/4`, `scanned=3`, `blind_violations=0`, `C2=met`, exit 0.
- Four isolated mutants each returned `C2=unmet`, exit 1: residual marker `FAIL 23/24`; old pin `blobs_ok=no`; changed freeze `pins_ok=blob_mismatch`; gate-class omission `gate_mutants=3/4`.
- Actual gate blob at `55f9a6942565107dac437765f6e6bd64f94a115c` was run on four temporary Git repos containing only invented reports: classes a–d each exited 1 with `blind_violations=1` and its matching rule label. Gate `--selftest` was not run against the live lane.
- The passing counter sandbox used an isolated synthetic tool patch, placeholder receipts, invented cases/reports, and a test gate stub; it is not evidence that the lane C2 claim is met. No tools installed.
- Boundary incident: one discarded exploratory clone used a later lane tip; its counter probe parsed committed CaseR30 reports. I did not inspect or quote their text and removed that clone. All cited sandbox pass/fail runs use clean 58-based histories with invented reports only.
- Blocker: the draft is in this report/scratch only; L1 must land it and run it from the committed blob with the final freeze, receipts, and gate.
