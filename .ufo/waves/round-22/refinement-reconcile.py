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
    cases += [('allowlist-path-substitution',2,'RETENTION_RECONCILIATION_SETUP','receipt_path_binding'),('clean-control',0,'RETENTION_RECONCILED',None),('non-author-overlap',0,'RETENTION_RECONCILED',None),('malformed-stdout',2,'RETENTION_RECONCILIATION_SETUP','invalid_json')]
    cases += [('forged-clean',1,'RETENTION_RECONCILIATION_MISMATCH',None)]
    cases += [('unsafe-'+key,2,'RETENTION_RECONCILIATION_SETUP','unsafe_input_path') for key in ('receipt','policy','allowlist')]
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
        elif name=='forged-clean':
            value['hits']=[h for h in value['hits'] if h['path']!='unallowed.txt']
            value['unallowlisted_hits']=[];value['metric']=0;value['finding_id']='RETENTION_CLEAN';wrapper['exit_code']=0
        elif name in ('allowlist-path-substitution','clean-control','non-author-overlap'):
            if name=='allowlist-path-substitution':
                (repo/'copy-allowlist.json').write_bytes((repo/'allowlist.json').read_bytes())
            elif name=='clean-control':
                (repo/'unallowed.txt').unlink()
                value['hits']=[h for h in value['hits'] if h['path']!='unallowed.txt']
                value['unallowlisted_hits']=[];value['metric']=0;value['finding_id']='RETENTION_CLEAN';wrapper['exit_code']=0
            else:
                hit=next(h for h in value['hits'] if h['path']=='non-author.txt')
                allow=json.loads((repo/'allowlist.json').read_bytes())
                allow['rows'].append({k:v for k,v in hit.items() if k!='line'}|{'reason':'synthetic overlap','rule':'b'})
                (repo/'allowlist.json').write_bytes(f.encoded(allow))
                value['allowlisted_hits'].append(copy.deepcopy(hit))
            f.git(repo,'add','--all');f.git(repo,'commit','-q','-m','new controlled measured tree')
            measured=f.git(repo,'rev-parse','HEAD').decode().strip()
            wrapper['measured_revision']=measured;wrapper['argv'][wrapper['argv'].index('--rev')+1]=measured;value['commit']=measured
        wrapper['stdout']=json.dumps(value)
        if name=='malformed-stdout':wrapper['stdout']='{\"broken\":'
        (repo/'receipt.json').write_bytes(f.encoded(wrapper))
        f.git(repo,'add','--all')
        if name=='symlink-identical':
            oid=f.git(repo,'hash-object','receipt.json').decode().strip()
            f.git(repo,'update-index','--cacheinfo',f'120000,{oid},receipt.json')
        f.git(repo,'commit','-q','--allow-empty','-m','one discriminating control')
        rev=f.git(repo,'rev-parse','HEAD').decode().strip()
        cmd=[sys.executable,a.tool,'check','--repo',str(repo),'--rev',rev,'--receipt','receipt.json','--policy','policy.json','--allowlist','allowlist.json']
        if name=='allowlist-path-substitution':cmd[-1]='copy-allowlist.json'
        if name.startswith('unsafe-'):
            flag='--'+name.removeprefix('unsafe-')
            cmd[cmd.index(flag)+1]='sub/../'+cmd[cmd.index(flag)+1]
        cp=subprocess.run(cmd,capture_output=True,text=True,timeout=60)
        try:obj=json.loads(cp.stdout)
        except ValueError:obj={}
        ok=cp.returncode==code and obj.get('finding_id')==finding and obj.get('privacy_clearance') is False and obj.get('receipt_match') is (code==0) and not cp.stderr
        if error:ok=ok and obj.get('error')==error
        if name=='clean-control':ok=ok and obj.get('retention_state')=='clean-at-frozen-regex-scope' and obj.get('raw_unallowlisted')==0
        if name=='non-author-overlap':ok=ok and obj.get('allowlisted')==4 and obj.get('non_author')==1 and obj.get('raw_unallowlisted')==1
        if name=='forged-clean':ok=ok and obj.get('raw_total')==5 and obj.get('raw_unallowlisted')==1 and obj.get('retention_state')=='red'
        rows.append({'id':name,'pass':ok,'expected_exit':code,'expected_finding':finding,'expected_error':error,'argv':cmd,'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
    result={'schema':'mori-r22-refinements-v1','tool_sha256':f.digest(Path(a.tool).read_bytes()),'runner_sha256':f.digest(Path(__file__).read_bytes()),'cases':rows,'passed':sum(x['pass'] for x in rows),'total':len(rows),'fixture_files':{str(x.relative_to(root)):f.digest(x.read_bytes()) for x in root.rglob('*') if x.is_file() and not x.is_symlink()}}
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'passed':result['passed'],'total':result['total']}));return int(result['passed']!=result['total'])
if __name__=='__main__':raise SystemExit(main())
