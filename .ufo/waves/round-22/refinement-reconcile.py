#!/usr/bin/env python3
"""Co-evolved extra controls; never rewrites the frozen24 requirement oracle."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('fixture',HERE/'frozen/fixture-builder-v2.py'); f=importlib.util.module_from_spec(s);s.loader.exec_module(f)

def main():
    p=argparse.ArgumentParser();p.add_argument('--tool',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);root=out.parent/(out.stem+'-fixtures');root.mkdir(exist_ok=False)
    cases=[('path-only',1,'RETENTION_RECONCILIATION_MISMATCH',None),('allowed-list-only',1,'RETENTION_RECONCILIATION_MISMATCH',None),('unallowed-list-only',1,'RETENTION_RECONCILIATION_MISMATCH',None),('non-author-counter',1,'RETENTION_RECONCILIATION_MISMATCH',None),('wrong-command-revision',2,'RETENTION_RECONCILIATION_SETUP','receipt_revision_conflict'),('symlink-identical',2,'RETENTION_RECONCILIATION_SETUP','input_not_regular'),('policy-change',2,'RETENTION_RECONCILIATION_SETUP','policy_changed'),('allowlist-change',2,'RETENTION_RECONCILIATION_SETUP','allowlist_changed'),('boolean-exit',2,'RETENTION_RECONCILIATION_SETUP','receipt_exit_type'),('boolean-routed',2,'RETENTION_RECONCILIATION_SETUP','receipt_counter_type')]
    rows=[]
    for name,code,finding,error in cases:
        fixture=f.make(root/name)
        repo=Path(fixture['repo']); wrapper=json.loads((repo/'receipt.json').read_bytes()); value=json.loads(wrapper['stdout'])
        if name=='path-only':value['hits'][0]['path']='different-path.txt'
        elif name=='allowed-list-only':value['allowlisted_hits'][0]['line']+=100
        elif name=='unallowed-list-only':value['unallowlisted_hits'][0]['line']+=100
        elif name=='non-author-counter':value['non_author']+=1
        elif name=='wrong-command-revision':wrapper['argv'][wrapper['argv'].index('--rev')+1]='0'*40
        elif name=='policy-change':(repo/'policy.json').write_bytes((repo/'policy.json').read_bytes()+b'\n')
        elif name=='allowlist-change':(repo/'allowlist.json').write_bytes((repo/'allowlist.json').read_bytes()+b'\n')
        elif name=='boolean-exit':wrapper['exit_code']=True
        elif name=='boolean-routed':value['routed']=False
        wrapper['stdout']=json.dumps(value)
        (repo/'receipt.json').write_bytes(f.encoded(wrapper))
        f.git(repo,'add','--all')
        if name=='symlink-identical':
            oid=f.git(repo,'hash-object','receipt.json').decode().strip()
            f.git(repo,'update-index','--cacheinfo',f'120000,{oid},receipt.json')
        f.git(repo,'commit','-q','--allow-empty','-m','one discriminating control')
        rev=f.git(repo,'rev-parse','HEAD').decode().strip()
        cmd=[sys.executable,a.tool,'check','--repo',str(repo),'--rev',rev,'--receipt','receipt.json','--policy','policy.json','--allowlist','allowlist.json']
        cp=subprocess.run(cmd,capture_output=True,text=True,timeout=60)
        try:obj=json.loads(cp.stdout)
        except ValueError:obj={}
        ok=cp.returncode==code and obj.get('finding_id')==finding and obj.get('privacy_clearance') is False and obj.get('receipt_match') is False and not cp.stderr
        if error:ok=ok and obj.get('error')==error
        rows.append({'id':name,'pass':ok,'expected_exit':code,'expected_finding':finding,'expected_error':error,'argv':cmd,'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
    result={'schema':'mori-r22-refinements-v1','tool_sha256':f.digest(Path(a.tool).read_bytes()),'runner_sha256':f.digest(Path(__file__).read_bytes()),'cases':rows,'passed':sum(x['pass'] for x in rows),'total':len(rows),'fixture_files':{str(x.relative_to(root)):f.digest(x.read_bytes()) for x in root.rglob('*') if x.is_file() and not x.is_symlink()}}
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'passed':result['passed'],'total':result['total']}));return int(result['passed']!=result['total'])
if __name__=='__main__':raise SystemExit(main())
