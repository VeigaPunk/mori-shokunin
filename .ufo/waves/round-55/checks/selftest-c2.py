#!/usr/bin/env python3
"""Round-55 C2 counter selftest. Uses committed source bytes, synthetic claim/source rows and settlement outputs."""
import importlib.util, json, os

def run(c2):
    here=os.path.dirname(os.path.abspath(__file__)); lane=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(here))))
    c2dpath=os.path.join(os.path.dirname(here),"controls","c2data.py")
    sp=importlib.util.spec_from_file_location("c2data",c2dpath); d=importlib.util.module_from_spec(sp);sp.loader.exec_module(d)
    files={}
    for u,(p,dig,k) in c2.COPIES.items():
        with open(os.path.join(lane,p),"rb") as f: files[p]=f.read().decode("utf-8","surrogateescape")
    urls=list(c2.COPIES); sid={key:val for key,val in d.SID.items()}; ukey={v:k for k,v in d.URLS.items()}
    src=["| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |","|---|---|---|---|---|---|---|---|---|---|---|"]
    for key,s in sid.items():
        url=d.URLS[key]; src.append("| %s | title — %s | code | A | scope | anchor | teaches | mined | 2026-10-27 | on-release | %s |"%(s,url,c2.ENTRY))
    entry=d.entry()
    # Make witness files with exact row text and quotes, sourced to the committed copies.
    hashes=[]; votes={}
    for key,claim,quote in d.ROWS: hashes.append(c2.claim_hash(claim))
    for voter in c2.VOTERS[:2]:
        votes[c2.ENTAIL_DIR+voter+".md"]="\n".join("ENTAIL %s entailed"%h for h in hashes)+"\n"
    votes[c2.RESULTS]=json.dumps({"results":[{"name":v,"output":"\n".join("ENTAIL %s entailed"%h for h in hashes)} for v in c2.VOTERS[:2]]})
    base=dict(files);base[c2.ENTRY]=entry;base["corpus/SOURCES.md"]="\n".join(src)+"\n";base.update(votes)
    def ls(directory):return [p for p in base if p.startswith(directory) and "/" not in p[len(directory):]]
    def score(fl):return c2.evaluate(lambda p:fl.get(p),"R",ls=ls)
    checks=[]
    def ck(name,ok):checks.append((name,bool(ok)))
    n=len(d.ROWS); met,line=score(base); ck("real-source witness met",met and ("claims=%d located=%d"%(n,n)) in line)
    no=dict(base);no.pop(c2.ENTRY);met,line=score(no);ck("do-nothing entry fails",not met and "entry_absent" in line)
    # quote echo and located claims source arm, but wrong beyond-quote claims
    echo=list(base[c2.ENTRY].splitlines());
    badrows=["| " + q + " | " + s + " | `"+quote+"` |" for (key,claim,quote),s in zip(d.ROWS,[sid[k] for k,_,_ in d.ROWS]) for q in [quote]]
    # use direct mutations of the source row or vote arms; quote mutation is deterministic.
    bad=dict(base); copy=next(c2.COPIES[u][0] for u in c2.COPIES if "statfs.2" in u)
    bad[copy]=bad[copy].replace("Free blocks available to", "Available free blocks for", 1)
    met,line=score(bad); ck("quote mutation fails location",not met and "quote_missing" in line)
    # unbound votes: report votes differ from captured output; no entailment
    bad=dict(base); bad[c2.RESULTS]=json.dumps({"results":[{"name":v,"output":"no vote"} for v in c2.VOTERS[:2]]})
    met,line=score(bad);ck("unbound entail votes do not count",not met and "entailment" in line)
    # overclaim line always blocks even if output does not echo it
    bad=dict(base); bad[c2.ENTAIL_DIR+c2.VOTERS[0]+".md"] += "ENTAIL %s overclaim\n"%hashes[0]
    met,line=score(bad);ck("overclaim dissent blocks",not met and "dissent=1" in line)
    # no settled voters
    bad=dict(base);bad[c2.RESULTS]=json.dumps({"results":[]});met,line=score(bad);ck("no settled voters fail",not met and "entailed=0" in line)
    # malformed duplicate quote row
    bad=dict(base)
    bad[c2.ENTRY]=entry.replace("claim | source | quote", "wrong | source | quote",1)
    met,line=score(bad);ck("bad table header fails",not met and "table" in line)
    # pin check
    bad=dict(base); p=next(iter(c2.COPIES.values()))[0];bad[p]+="\n";met,line=score(bad);ck("changed source copy fails pin",not met and "pins=bad" in line)
    # source status fail
    bad=dict(base);bad["corpus/SOURCES.md"]=base["corpus/SOURCES.md"].replace("| mined |", "| queued |",1);met,line=score(bad);ck("queued source fails",not met and "source_rows=bad" in line)
    # all available source rows and list coverage
    ck("nine-source data shape",len(set(k for k,_,_ in d.ROWS))==9)
    fail=sum(not x for _,x in checks)
    for n,ok in checks:
        if not ok: print("FAIL",n)
    print("C2_SELFTEST pass=%d fail=%d"%(len(checks)-fail,fail))
    return 0 if fail==0 else 1
