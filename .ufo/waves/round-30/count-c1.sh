#!/usr/bin/env bash
set -euo pipefail
if (($# != 1)); then printf 'usage: count-c1.sh <lane-rev>\n' >&2; exit 2; fi
exec python3 -I -B - "$1" <<'PY'
import datetime, json, os, re, subprocess, sys, tempfile
from collections import Counter
from pathlib import Path
BASE="58b61681a0e3f3b821a17d38a4e713ccd9921615"; REPO="/home/vgpnk/Projects/shokunin/mori-shokunin"
ENTRY="corpus/knowledge/earlyoom-invocation-scope-r30.md"; FIX="tools/fixtures/mori-oom-killers/"
CASES=tuple(FIX+n for n in ("cases.json","cases-supplementary.json","cases-a2.json"))
SOURCES,LESSON,SKILL,TOOL="corpus/SOURCES.md","corpus/lessons/round-30.md","SKILL.md","tools/mori-oom-killers.py"
CUTOFF=datetime.datetime(2026,10,22,21,8,28,tzinfo=datetime.timezone.utc)
VERDICTS={"KILLER_ACTED","KILLERS_QUIET","KILLERS_UNKNOWN"}; ID_RE=re.compile(r"S[0-9]{3,}")
FIELD_RE=re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+"); LOC_RE=re.compile(r"`([^`\s:]+):(\d+)(?:-(\d+))?`")
class InputError(Exception): pass
env=os.environ.copy()
for k in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"): env.pop(k,None)
def git(*a):
    try: return subprocess.run(["git","-C",REPO,*a],stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,check=False)
    except OSError as e: raise InputError("cannot run git: {}".format(e)) from e
def resolve(r):
    p=git("rev-parse","--verify","--end-of-options",r+"^{commit}")
    if p.returncode: raise InputError("bad revision")
    return p.stdout.decode("ascii").strip()
def blob(r,p):
    x=git("show","{}:{}".format(r,p)); return x.stdout if x.returncode==0 else None
def need(r,p):
    b=blob(r,p)
    if b is None: raise InputError("missing {} at {}".format(p,r))
    try: return b.decode("utf-8")
    except UnicodeDecodeError as e: raise InputError("invalid UTF-8 in {}".format(p)) from e
def cells(line):
    s=line.strip()
    if not s.startswith("|"): return None
    out,cur,n=[],[],0
    for c in s[1:]:
        if c=="|" and n%2==0: out.append("".join(cur).strip()); cur=[]; n=0
        else: cur.append(c); n=n+1 if c=="\\" else 0
    if cur: out.append("".join(cur).strip())
    return out
sep=lambda c: bool(c) and all(re.fullmatch(r":?-{3,}:?",x.replace(" ","")) for x in c)
def table(t):
    ls=t.splitlines(); req={"shape","verdict","fields","case","sources"}
    for i in range(len(ls)-1):
        h=cells(ls[i]); names=[x.strip().strip("`").lower() for x in h or []]
        if not req.issubset(names): continue
        d=cells(ls[i+1])
        if d is None or not sep(d) or len(d)!=len(h): continue
        p={k:names.index(k) for k in req}; p["width"]=len(h); rows=[]
        for line in ls[i+2:]:
            c=cells(line)
            if c is None: break
            if not sep(c): rows.append(c)
        return p,rows
    return None,[]
def parse_fields(s):
    dec,out,i=json.JSONDecoder(),{},0
    while i<len(s):
        if s[i]!="`": return None
        m=FIELD_RE.match(s,i+1)
        if not m or m.end()>=len(s) or s[m.end()]!="=": return None
        key=m.group()
        try: val,end=dec.raw_decode(s,m.end()+1)
        except ValueError: return None
        if end>=len(s) or s[end]!="`" or key in out: return None
        out[key],i=val,end+1
        if i==len(s): break
        if s[i:i+2]!=", ": return None
        i+=2
    return out or None
def equal(a,b):
    if isinstance(a,bool) or isinstance(b,bool): return isinstance(a,bool) and isinstance(b,bool) and a==b
    if isinstance(a,(int,float)) and isinstance(b,(int,float)): return a==b
    if type(a) is not type(b): return False
    if isinstance(a,list): return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    if isinstance(a,dict): return a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a)
    return a==b
def get(v,path):
    for k in path.split("."):
        if not isinstance(v,dict) or k not in v: return False,None
        v=v[k]
    return True,v
case_id=lambda s:(m.group(1) if (m:=re.fullmatch(r"`([A-Za-z0-9][A-Za-z0-9._-]*)`",s.strip())) else None)
source_ids=lambda s:(lambda a,r:a if a and not re.sub(r"[\s,;&`]+","",r) else None)(ID_RE.findall(s),ID_RE.sub("",s))
urls=lambda s:[m.group().rstrip("),;.") for m in re.finditer(r"https?://\S+",s)]
norm=lambda s:re.sub(r"[ \t]+"," ",s).strip()
canonical=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(",",":"))
def source_rows(t):
    out={}
    for line in t.splitlines():
        c=cells(line)
        if c and len(c)>=2 and re.fullmatch(r"S[0-9]{3,}",c[0]): out.setdefault(c[0],[]).append((c[1],line))
    return out
def quoted(s):
    i=s.find('"')
    if i<0: return None,False
    out,i=[],i+1
    while i<len(s):
        c=s[i]
        if c=="\\" and i+1<len(s) and s[i+1] in ('"',"|","\\"): out.append(s[i+1]); i+=2
        elif c=='"': return "".join(out),True
        else: out.append(c); i+=1
    return None,False
def wc(s):
    try:
        p=subprocess.run(["wc","-w"],input=s.encode(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
        return int(p.stdout.split()[0]) if p.returncode==0 else -1
    except (OSError,ValueError,IndexError): return -1
def citations(s):
    locs,out=list(LOC_RE.finditer(s)),[]
    for i,m in enumerate(locs):
        seg=s[m.end():locs[i+1].start() if i+1<len(locs) else len(s)]; q,closed=quoted(seg); ns=re.findall(r"\((\d+)\s+words?\)",seg)
        if not closed or len(ns)!=1 or not q: continue
        n=wc(q); a,b=int(m.group(2)),int(m.group(3) or m.group(2))
        if n==int(ns[0]) and 3<=n<=25 and a>0 and b>=a: out.append((m.group(1),a,b,q,n))
    return out
def utc(s):
    m=re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z",s)
    if not m: return None
    try: return datetime.datetime.strptime(m.group(),"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
    except ValueError: return None
def excerpt(data,sid,url,sha):
    if data is None: return None
    try: ls=data.decode("utf-8").splitlines()
    except UnicodeDecodeError: return None
    if len(ls)<7 or ls[0]!="id: "+sid or ls[1]!="url: "+url: return None
    h=re.fullmatch(r"sha256: ([0-9a-fA-F]{64})",ls[2]); at=utc(ls[3][9:]) if ls[3].startswith("accessed: ") else None
    if not h or h.group(1).lower()!=sha or at is None or at<CUTOFF or not re.fullmatch(r"lines: \d+-\d+",ls[4]) or ls[5]!="": return None
    out={}
    for line in ls[6:]:
        n,tab,text=line.partition("\t")
        if not tab or not n.isdigit(): return None
        out.setdefault(int(n),[]).append(text)
    return out
quote_in=lambda body,cite: all(n in body for n in range(cite[1],cite[2]+1)) and norm(cite[3]) in norm(" ".join(" ".join(body[n]) for n in range(cite[1],cite[2]+1)))
def gate_ok(rev,sid,rows,old,lesson):
    if lesson is None or len(rows)!=1: return False
    su=set(urls(rows[0][0]))
    if len(su)!=1: return False
    source=next(iter(su))
    if source in old: return False
    ls=lesson.splitlines(); start=next((i for i,x in enumerate(ls) if x.startswith("## Gate")),-1)
    if start<0: return False
    end=next((i for i in range(start+1,len(ls)) if ls[i].startswith("## ")),len(ls))
    for line in ls[start+1:end]:
        c=cells(line)
        if not c or len(c)<6 or c[0]!=sid or not re.match(r"^admit(?:\s*,|\s*$)",c[5]): continue
        u=re.search(r"https?://\S+",c[1]); h=re.search(r"`([0-9a-fA-F]{64})`",c[3])
        if not u or not h or utc(c[2]) is None: continue
        url,sha=u.group().rstrip("),"),h.group(1).lower()
        cs=citations(c[4])
        if url==source and cs:
            body=excerpt(blob(rev,"corpus/evidence/sources-r30/{}.txt".format(sid)),sid,url,sha)
            if body and any(quote_in(body,x) for x in cs): return True
    return False
def versions(c):
    inp=c.get("inputs",{}); js=inp.get("earlyoom_journal") if isinstance(inp,dict) else None
    return sum(1 for x in js if isinstance(x,dict) and isinstance(x.get("MESSAGE"),str) and x["MESSAGE"].lstrip().startswith("earlyoom ")) if isinstance(js,list) else 0
def cases_at(rev):
    out={}
    for path in CASES:
        try: d=json.loads(need(rev,path))
        except json.JSONDecodeError as e: raise InputError("malformed {}".format(path)) from e
        frozen=blob(rev,path)==blob(BASE,path)
        for c in d.get("cases",[]):
            if isinstance(c,dict) and isinstance(c.get("id"),str): out.setdefault(c["id"],[]).append((c,path,frozen))
    return out
def find_case(index,cid):
    copies=[(c,p) for c,p,f in index.get(cid,[]) if f]; paths=[p for _,p in copies]
    if not copies or len(paths)!=len(set(paths)) or len({(canonical(c.get("inputs")),canonical(c.get("expect"))) for c,_ in copies})!=1: return None
    c=copies[0][0]
    return c if isinstance(c.get("inputs"),dict) and isinstance(c.get("expect"),dict) else None
def run_tool(tool,inputs,case,verdict,fields):
    try:
        p=subprocess.run(["python3","-I","-B",str(tool),"--inputs",str(inputs)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False); out=json.loads(p.stdout.decode())
    except (OSError,UnicodeDecodeError,json.JSONDecodeError): return False
    ex=case["expect"]
    if not isinstance(out,dict) or out.get("verdict")!=verdict or type(ex.get("exit")) is not int or p.returncode!=ex["exit"] or not fields: return False
    return bool(fields) and all((lambda r:r[0] and equal(r[1],want))(get(out,k)) for k,want in fields.items())
def row_data(c,p):
    w=p is not None and len(c)==p["width"]
    return {"id":case_id(c[p["case"]]) if w else None,"shape":c[p["shape"]].strip() if w else "",
            "verdict":c[p["verdict"]].strip().strip("`") if w else "","fields":parse_fields(c[p["fields"]]) if w else None,
            "sources":source_ids(c[p["sources"]]) if w else None,"width":w}
def main(revision):
    rev=resolve(revision); tool_data=blob(BASE,TOOL)
    if tool_data is None: raise InputError("missing entering-tip tool")
    src,skill=source_rows(need(rev,SOURCES)),need(rev,SKILL)
    data=blob(rev,ENTRY); entry=data.decode("utf-8") if data is not None else None
    data=blob(rev,LESSON); lesson=data.decode("utf-8") if data is not None else None
    index=cases_at(rev)
    pos,rows=(None,[]) if entry is None else table(entry)
    metadata=bool(entry is not None and all(re.search(r"^{}:\s*\S.*$".format(k),entry,re.M) for k in ("source","verified-at","recheck")))
    parsed=[row_data(c,pos) for c in rows]; ids=Counter(x["id"] for x in parsed if x["id"]); shapes=Counter(x["shape"] for x in parsed if x["shape"])
    old={u for sid,rs in src.items() if int(sid[1:])<156 for _,line in rs for u in urls(line)}
    ev,new_ids,new_rows,version_n,verdicts={},set(),0,0,set(); details=[]
    with tempfile.TemporaryDirectory(prefix="mori-c1-") as tmp:
        tool,inputs=Path(tmp)/"tool.py",Path(tmp)/"inputs.json"; tool.write_bytes(tool_data)
        for r in parsed:
            cid,shape,rv,rf,rs=r["id"],r["shape"],r["verdict"],r["fields"],r["sources"]
            case=find_case(index,cid) if cid else None; ex=case["expect"] if case else {}; ef=ex.get("fields",{}) if isinstance(ex,dict) else {}
            co=bool(case and ids[cid]==1 and shape and shapes[shape]==1); vo=bool(case and rv in VERDICTS and ex.get("verdict")==rv)
            if rv in VERDICTS: verdicts.add(rv)
            fo=bool(case and rf and isinstance(ef,dict) and all(k in ef and equal(v,ef[k]) for k,v in rf.items())
                    and ("earlyoom.scope_complete" in rf or "earlyoom.earlier_invocation_send_lines" in rf))
            to=False
            if case: inputs.write_text(json.dumps(case["inputs"],ensure_ascii=False),encoding="utf-8"); to=run_tool(tool,inputs,case,rv,rf or {})
            so=bool(rs)
            if rs:
                if any(int(s[1:])>=156 for s in rs): new_rows+=1
                for sid in rs:
                    if int(sid[1:])>=156: new_ids.add(sid)
                    recs=src.get(sid,[])
                    if not recs: so=False
                    elif int(sid[1:])>=156:
                        if sid not in ev: ev[sid]=gate_ok(rev,sid,recs,old,lesson)
                        if not ev[sid]: so=False
            if case and versions(case)>=2: version_n+=1
            ok=bool(co and r["width"] and shape and vo and fo and to and so)
            details.append((cid or "invalid",co,bool(shape and shapes[shape]==1),vo,fo,to,so,ok))
    excerpts=sum(1 for sid in new_ids if ev.get(sid,False)); sm=re.search(r"^source:\s*(.*)$",entry,re.M) if entry else None
    header=bool(sm and set(ID_RE.findall(sm.group(1)))&new_ids); case_set={x["id"] for x in parsed if x["id"]}; skill_rows=0; section=False
    for line in skill.splitlines():
        if re.match(r"^#{1,2}\s",line): section=line.startswith("## Round30")
        if section and line.lstrip().startswith("|") and "earlyoom-invocation-scope-r30.md" in line:
            if any(re.search(r"(?<![A-Za-z0-9._-]){}(?![A-Za-z0-9._-])".format(re.escape(cid)),line) for cid in case_set): skill_rows+=1
    met=bool(entry is not None and metadata and len(rows)>=8 and len(ids)==len(rows) and len(shapes)==len(rows) and len(verdicts)>=2 and version_n>=4 and len(new_ids)>=3 and new_rows>=3 and excerpts==len(new_ids) and header and skill_rows>=3 and all(x[-1] for x in details))
    for cid,co,sh,vo,fo,to,so,_ in details:
        print("case={} case_ok={} shape={} verdict={} fields={} tool={} sources={}".format(cid,"ok" if co else "bad","ok" if sh else "bad","ok" if vo else "bad","ok" if fo else "bad","ok" if to else "bad","ok" if so else "bad"))
    print("rows={} rows_ok={} new_ids={} new_id_rows={} excerpts_ok={}/{} skill_rows={}".format(len(rows),sum(x[-1] for x in details),len(new_ids),new_rows,excerpts,len(new_ids),skill_rows))
    print("C1={}".format("met" if met else "unmet")); return 0 if met else 1
try:
    if len(sys.argv)!=2: raise InputError("usage: count-c1.sh <lane-rev>")
    sys.exit(main(sys.argv[1]))
except InputError as exc:
    print("count-c1: {}".format(exc),file=sys.stderr); sys.exit(2)
PY
