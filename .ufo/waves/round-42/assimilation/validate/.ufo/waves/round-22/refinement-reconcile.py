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
    cases += [('diverged-consistent',2,'RETENTION_RECONCILIATION_SETUP','measured_not_ancestor'),('cousin',2,'RETENTION_RECONCILIATION_SETUP','measured_not_ancestor'),('head-cousin',2,'RETENTION_RECONCILIATION_SETUP','measured_not_ancestor')]
    cases += [('symbolic-input',0,'RETENTION_RECONCILED',None),('dirty-worktree',0,'RETENTION_RECONCILED',None),('inner-commit-split',2,'RETENTION_RECONCILIATION_SETUP','receipt_revision_conflict'),('measured-tag',2,'RETENTION_RECONCILIATION_SETUP','receipt_revision'),('wrong-policy-digest',2,'RETENTION_RECONCILIATION_SETUP','receipt_policy_digest'),('policy-path-substitution',2,'RETENTION_RECONCILIATION_SETUP','receipt_path_binding')]
    # Wave2 falsifier additions (FinalR04/R06/R10/R16/R20, FixturePolicyChanged): reason-specific arms.
    cases += [('metric-overstate',1,'RETENTION_RECONCILIATION_MISMATCH',None),('inject-only',1,'RETENTION_RECONCILIATION_MISMATCH',None),('policy-change-digest-updated',2,'RETENTION_RECONCILIATION_SETUP','policy_changed'),('allowlist-canonical-two-step',2,'RETENTION_RECONCILIATION_SETUP','allowlist_changed'),('control-path',2,'RETENTION_RECONCILIATION_SETUP','unsafe_input_path'),('control-path-twin',0,'RETENTION_RECONCILED',None),('valid-identities',0,'RETENTION_RECONCILED',None)]
    # FinalR08/R18, FixtureBoolLine: raw-only line identity and bool collision arms.
    cases += [('line-raw-only',1,'RETENTION_RECONCILIATION_MISMATCH',None),('boolean-line-colliding',2,'RETENTION_RECONCILIATION_SETUP','receipt_hit_type'),('boolean-metric',2,'RETENTION_RECONCILIATION_SETUP','receipt_counter_type'),('boolean-non-author',2,'RETENTION_RECONCILIATION_SETUP','receipt_counter_type'),('non-author-swap',1,'RETENTION_RECONCILIATION_MISMATCH',None)]
    # FinalR02/R11/R13, FixtureForbidden/InvalidRevision: verdict-field, forbidden-only and revision-attribution arms.
    cases += [('exit-code-lie',1,'RETENTION_RECONCILIATION_MISMATCH',None),('finding-lie',1,'RETENTION_RECONCILIATION_MISMATCH',None),('routed-lie',1,'RETENTION_RECONCILIATION_MISMATCH',None),('forbidden-laundered',1,'RETENTION_RECONCILIATION_MISMATCH',None),('forbidden-as-stale',1,'RETENTION_RECONCILIATION_MISMATCH',None),('forbidden-only',0,'RETENTION_RECONCILED',None),('unresolvable-consistent',2,'RETENTION_RECONCILIATION_SETUP','receipt_revision'),('help-flag',2,'RETENTION_RECONCILIATION_SETUP','usage')]
    cases += [('nested-policy-copy',0,'RETENTION_RECONCILED',None)]
    cases += [('invalid-input-rev',2,'RETENTION_RECONCILIATION_SETUP','git_read_failed'),('repo-subdirectory',2,'RETENTION_RECONCILIATION_SETUP','repo_not_toplevel'),('repo-empty',2,'RETENTION_RECONCILIATION_SETUP','repo_not_absolute')]
    cases += [('bom-receipt',2,'RETENTION_RECONCILIATION_SETUP','invalid_json')]
    expected_differences={'path-only':['hits'],'allowed-list-only':['allowlisted_hits'],'unallowed-list-only':['unallowlisted_hits'],'non-author-counter':['non_author'],'forged-clean':['hits','unallowlisted_hits','metric','finding_id','exit_code'],'metric-overstate':['metric'],'inject-only':['hits'],'line-raw-only':['hits'],'non-author-swap':['hits'],'exit-code-lie':['exit_code'],'finding-lie':['finding_id'],'routed-lie':['routed'],'forbidden-laundered':['finding_id','forbidden_allowlist'],'forbidden-as-stale':['finding_id','forbidden_allowlist','warnings']}
    rows=[]
    for name,code,finding,error in cases:
        fixture=f.make(root/name,'forbidden' if name in ('forbidden-laundered','forbidden-as-stale') else 'valid')
        repo=Path(fixture['repo']); wrapper=json.loads((repo/'receipt.json').read_bytes()); value=json.loads(wrapper['stdout'])
        if name=='exit-code-lie':wrapper['exit_code']=0
        elif name=='finding-lie':value['finding_id']='RETENTION_CLEAN'
        elif name=='routed-lie':value['routed']=1
        elif name=='forbidden-laundered':
            value['forbidden_allowlist']=[];value['finding_id']='RETENTION_FINDINGS'
        elif name=='forbidden-as-stale':
            value['warnings']=[dict(r,finding_id='allowlist_stale') for r in value['forbidden_allowlist']]
            value['forbidden_allowlist']=[];value['finding_id']='RETENTION_FINDINGS'
        elif name=='unresolvable-consistent':
            wrapper['measured_revision']='0'*40;wrapper['argv'][wrapper['argv'].index('--rev')+1]='0'*40;value['commit']='0'*40
        elif name=='nested-policy-copy':
            (repo/'sub/copy').mkdir(parents=True);(repo/'sub/copy/policy.json').write_bytes((repo/'policy.json').read_bytes())
            f.git(repo,'add','--all');f.git(repo,'commit','-q','-m','nested byte-identical policy copy')
            measured=f.git(repo,'rev-parse','HEAD').decode().strip()
            extra=[dict(h,path='sub/copy/policy.json') for h in value['hits'] if h['path']=='policy.json']
            value['hits']+=extra;value['unallowlisted_hits']+=extra;value['metric']+=len(extra)
            wrapper['measured_revision']=measured;wrapper['argv'][wrapper['argv'].index('--rev')+1]=measured;value['commit']=measured
        elif name=='forbidden-only':
            (repo/'unallowed.txt').unlink()
            policy=json.loads((repo/'policy.json').read_bytes());policy['must_redact_paths']=['ghost.txt']
            (repo/'policy.json').write_bytes(f.encoded(policy))
            allow=json.loads((repo/'allowlist.json').read_bytes())
            ghost={'path':'ghost.txt','class':'R22','line_sha256':'3'*64}
            allow['rows'].append(ghost|{'reason':'synthetic forbidden-only row','rule':'b'})
            (repo/'allowlist.json').write_bytes(f.encoded(allow))
            f.git(repo,'add','--all');f.git(repo,'commit','-q','-m','forbidden-only measured tree')
            measured=f.git(repo,'rev-parse','HEAD').decode().strip()
            value['unallowlisted_hits']=[];value['metric']=0;value['routed']=0
            value['forbidden_allowlist']=[ghost|{'finding_id':'allowlist_forbidden','line':None}]
            import re
            hits=[]
            for row in f.git(repo,'ls-tree','-r','-z','--full-tree',measured).split(b'\0'):
                if not row:continue
                meta,path=row.split(b'\t',1);data=f.git(repo,'cat-file','blob',meta.split()[2].decode())
                if b'\0' in data:continue
                for n,line in enumerate(data.decode('utf8','replace').split('\n'),1):
                    if re.search('[R]22_SAMPLE',line):hits.append({'path':path.decode(),'line':n,'class':'R22','line_sha256':f.digest(line.encode())})
            keys={(r['path'],r['class'],r['line_sha256']) for r in allow['rows'] if r['path']!='ghost.txt'}
            value['hits']=hits;value['allowlisted_hits']=[h for h in hits if (h['path'],h['class'],h['line_sha256']) in keys]
            value['finding_id']='allowlist_forbidden';value['policy_sha256']=f.digest((repo/'policy.json').read_bytes())
            wrapper['exit_code']=1;wrapper['measured_revision']=measured;wrapper['argv'][wrapper['argv'].index('--rev')+1]=measured;value['commit']=measured
        if name in ('diverged-consistent','cousin','head-cousin'):
            old=wrapper['measured_revision']
            tree=f.git(repo,'rev-parse',old+'^{tree}').decode().strip()
            args=['commit-tree',tree]
            if name!='diverged-consistent':args+=['-p',old]
            other=f.git(repo,*args,data=b'consistent divergent measured commit\n').decode().strip()
            wrapper['measured_revision']=other;wrapper['argv'][wrapper['argv'].index('--rev')+1]=other;value['commit']=other
        elif name=='measured-tag':
            f.git(repo,'tag','-a','synthetic-tag','-m','synthetic tag',wrapper['measured_revision'])
            tag=f.git(repo,'rev-parse','synthetic-tag').decode().strip()
            wrapper['measured_revision']=tag;wrapper['argv'][wrapper['argv'].index('--rev')+1]=tag;value['commit']=tag
        elif name=='inner-commit-split':
            f.git(repo,'commit','-q','--allow-empty','-m','new measured commit')
            new=f.git(repo,'rev-parse','HEAD').decode().strip()
            wrapper['measured_revision']=new;wrapper['argv'][wrapper['argv'].index('--rev')+1]=new
        elif name=='wrong-policy-digest':
            value['policy_sha256']='0'*64
        elif name=='metric-overstate':
            value['metric']+=1
        elif name=='non-author-swap':
            target=next(i for i,h in enumerate(value['hits']) if h['path']=='non-author.txt')
            value['hits'][target]=dict(value['hits'][target],line_sha256='2'*64)
        elif name=='line-raw-only':
            target=next(i for i,h in enumerate(value['hits']) if h['path']=='non-author.txt')
            value['hits'][target]=dict(value['hits'][target],line=value['hits'][target]['line']+1)
        elif name=='boolean-line-colliding':
            target=next(h for h in value['hits'] if h['path']=='unallowed.txt')
            if target['line']!=1:raise RuntimeError('fixture_line_not_one')
            value['hits']=[dict(h,line=True) if h is target else h for h in value['hits']]
            value['unallowlisted_hits']=[dict(h,line=True) if h['path']=='unallowed.txt' else h for h in value['unallowlisted_hits']]
        elif name=='boolean-metric':
            value['metric']=True
        elif name=='boolean-non-author':
            value['non_author']=True
        elif name=='inject-only':
            value['hits'].append({'path':'injected.txt','line':1,'class':'R22','line_sha256':'1'*64})
        elif name=='policy-change-digest-updated':
            changed=(repo/'policy.json').read_bytes()+b'\n'
            (repo/'policy.json').write_bytes(changed);value['policy_sha256']=f.digest(changed)
        elif name=='allowlist-canonical-two-step':
            allow=json.loads((repo/'allowlist.json').read_bytes())
            allow['rows'].append({'path':'unallowed.txt','class':'R22','line_sha256':value['unallowlisted_hits'][0]['line_sha256'],'reason':'synthetic laundering','rule':'b'})
            (repo/'allowlist.json').write_bytes(f.encoded(allow))
            f.git(repo,'add','--all');f.git(repo,'commit','-q','-m','canonical allowlist change')
            (repo/'unrelated.txt').write_bytes(b'unrelated\n')
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
        elif name in ('allowlist-path-substitution','policy-path-substitution','clean-control','non-author-overlap'):
            if name in ('allowlist-path-substitution','policy-path-substitution'):
                original='policy.json' if name=='policy-path-substitution' else 'allowlist.json'
                (repo/('copy-'+original)).write_bytes((repo/original).read_bytes())
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
        if name=='bom-receipt':(repo/'receipt.json').write_bytes(b'\xef\xbb\xbf'+f.encoded(wrapper))
        f.git(repo,'add','--all')
        if name=='symlink-identical':
            oid=f.git(repo,'hash-object','receipt.json').decode().strip()
            f.git(repo,'update-index','--cacheinfo',f'120000,{oid},receipt.json')
        f.git(repo,'commit','-q','--allow-empty','-m','one discriminating control')
        rev=f.git(repo,'rev-parse','HEAD').decode().strip()
        if name=='head-cousin':f.git(repo,'update-ref','HEAD',wrapper['measured_revision'])
        if name=='dirty-worktree':
            for path in ('receipt.json','policy.json','allowlist.json'):(repo/path).write_bytes(b'{deliberately-dirty')
        cmd=[sys.executable,a.tool,'check','--repo',str(repo),'--rev',rev,'--receipt','receipt.json','--policy','policy.json','--allowlist','allowlist.json']
        if name=='allowlist-path-substitution':cmd[-1]='copy-allowlist.json'
        if name=='policy-path-substitution':cmd[cmd.index('--policy')+1]='copy-policy.json'
        if name=='symbolic-input':cmd[cmd.index('--rev')+1]='HEAD'
        if name=='help-flag':cmd.append('-h')
        if name=='invalid-input-rev':cmd[cmd.index('--rev')+1]='no-such-revision'
        if name=='repo-subdirectory':
            (repo/'plain-subdir').mkdir();cmd[cmd.index('--repo')+1]=str(repo/'plain-subdir')
        if name=='repo-empty':cmd[cmd.index('--repo')+1]=''
        if name.startswith('unsafe-'):
            flag='--'+name.removeprefix('unsafe-')
            cmd[cmd.index(flag)+1]='sub/../'+cmd[cmd.index(flag)+1]
        if name in ('control-path','control-path-twin'):
            (repo/'tab\treceipt.json').write_bytes((repo/'receipt.json').read_bytes())
            f.git(repo,'add','--all');f.git(repo,'commit','-q','-m','control-character receipt copy')
            rev=f.git(repo,'rev-parse','HEAD').decode().strip();cmd[cmd.index('--rev')+1]=rev
            if name=='control-path':cmd[cmd.index('--receipt')+1]='tab\treceipt.json'
        cp=subprocess.run(cmd,capture_output=True,text=True,timeout=60)
        try:obj=json.loads(cp.stdout)
        except ValueError:obj={}
        ok=cp.returncode==code and obj.get('finding_id')==finding and obj.get('privacy_clearance') is False and obj.get('receipt_match') is (code==0) and not cp.stderr
        if error:ok=ok and obj.get('error')==error
        if name=='clean-control':ok=ok and obj.get('retention_state')=='clean-at-frozen-regex-scope' and obj.get('raw_unallowlisted')==0
        if name=='non-author-overlap':ok=ok and obj.get('allowlisted')==4 and obj.get('non_author')==1 and obj.get('raw_unallowlisted')==1
        if name=='forged-clean':ok=ok and obj.get('raw_total')==5 and obj.get('raw_unallowlisted')==1 and obj.get('retention_state')=='red'
        if name in expected_differences:ok=ok and sorted(obj.get('differences') or [])==sorted(expected_differences[name])
        if name=='non-author-counter':ok=ok and obj.get('non_author')==1
        if name=='nested-policy-copy':ok=ok and obj.get('raw_unallowlisted')==2 and obj.get('policy_excluded')==1 and obj.get('retention_state')=='red'
        if name=='forbidden-only':ok=ok and obj.get('forbidden_allowlist')==1 and obj.get('raw_unallowlisted')==0 and obj.get('retention_state')=='red'
        if name=='valid-identities':
            key=lambda h:(h['path'],h['line'],h['class'],h['line_sha256'])
            raw=sorted(map(key,obj.get('raw_hits',[])));parts=sorted(map(key,obj.get('scanner_hits',[])+obj.get('policy_excluded_hits',[])))
            ok=ok and raw==parts and raw==sorted(map(key,fixture['expected_scanner_hits']+fixture['expected_policy_hits'])) and sorted(map(key,obj.get('policy_excluded_hits',[])))==sorted(map(key,fixture['expected_policy_hits']))
            ok=ok and obj.get('raw_not_allowlisted')==2 and obj.get('raw_total')==5 and obj.get('allowlisted')==3
        if code in (0,1):
            loaded={key:f.digest(f.git(repo,'show',rev+':'+cmd[cmd.index('--'+key)+1])) for key in ('receipt','policy','allowlist')}
            ok=ok and obj.get('input_revision')==rev and obj.get('measured_revision')==wrapper['measured_revision'] and obj.get('inputs_sha256')==loaded and obj.get('tool_sha256')==f.digest(Path(a.tool).read_bytes()) and obj.get('argv')==cmd[2:]
        else:
            ok=ok and set(obj)=={'schema','finding_id','error','privacy_clearance','receipt_match'}
        rows.append({'id':name,'pass':ok,'expected_exit':code,'expected_finding':finding,'expected_error':error,'argv':cmd,'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
    result={'schema':'mori-r22-refinements-v1','tool_sha256':f.digest(Path(a.tool).read_bytes()),'runner_sha256':f.digest(Path(__file__).read_bytes()),'cases':rows,'passed':sum(x['pass'] for x in rows),'total':len(rows),'fixture_files':{str(x.relative_to(root)):f.digest(x.read_bytes()) for x in root.rglob('*') if x.is_file() and not x.is_symlink()}}
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'passed':result['passed'],'total':result['total']}));return int(result['passed']!=result['total'])
if __name__=='__main__':raise SystemExit(main())
