#!/usr/bin/env python3
"""L1 measurement driver: retain actual commands, exact bytes and separate verdicts."""
import argparse
from collections import Counter
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile

HERE=Path(__file__).resolve().parent
LANE=HERE.parents[2]
BASE='77a5bbe8a0b41dfbfd2546d024d36e294b814bd0'
def sha(data):return hashlib.sha256(data).hexdigest()
def write(path,obj):path.write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n')
def main():
    p=argparse.ArgumentParser();p.add_argument('--revision',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    output=Path(a.output);output.mkdir(parents=True,exist_ok=False)
    pins=json.loads((HERE/'frozen/requirements-v2.json').read_bytes())
    pinned={'contract.md':pins['contract_sha256'],'denominator-correction.md':pins['correction_sha256'],'frozen/fixture-builder-v2.py':pins['fixture_builder_sha256'],'oracle-reconcile-v2.py':pins['oracle_sha256']}
    for path,expected_digest in pinned.items():
        if sha((HERE/path).read_bytes())!=expected_digest:
            write(output/'summary.json',{'finding_id':'snapshot_tampered','path':path})
            print(json.dumps({'finding_id':'snapshot_tampered','path':path}))
            return 2
    scratch=LANE/'.scratch/round22'/output.name;scratch.mkdir(parents=True,exist_ok=False)
    env=dict(os.environ,TMPDIR=str(LANE/'.scratch'),PYTHONDONTWRITEBYTECODE='1')
    records=[]
    def run(name,cmd,cwd=LANE):
        cp=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,text=True,timeout=300)
        row={'schema':'mori-r22-command-receipt-v1','name':name,'measured_revision':a.revision,'argv':[str(x) for x in cmd],'cwd':str(cwd),'recorded_utc':datetime.now(timezone.utc).isoformat(),'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr}
        write(output/(name+'.json'),row);records.append(row)
        try:value=json.loads(cp.stdout)
        except ValueError:value=None
        return cp.returncode,value
    tool=LANE/'tools/mori-retention-reconcile.py'
    code_cp=subprocess.run(['git','-C',str(LANE),'show',a.revision+':tools/mori-retention-reconcile.py'],capture_output=True)
    if code_cp.returncode or code_cp.stdout!=tool.read_bytes():raise RuntimeError('measured_code_not_committed')
    absent_rc,_=run('entering-capability-absence',['git','-C',str(LANE),'cat-file','-e',BASE+':tools/mori-retention-reconcile.py'])
    if absent_rc==0:raise RuntimeError('entering_capability_not_absent')
    args=[sys.executable,str(HERE/'oracle-reconcile-v2.py'),'--requirements',str(HERE/'frozen/requirements-v2.json')]
    before_path=scratch/'before.json';after_path=scratch/'after.json'
    br,_=run('finite-before',args+['--tool',str(scratch/'entering-absent-tool.py'),'--output',str(before_path)])
    ar,_=run('finite-after',args+['--tool',str(tool),'--output',str(after_path)])
    for name,path in (('before-observed',before_path),('after-observed',after_path)):
        (output/(name+'.json')).write_bytes(path.read_bytes())
    sr,selftest=run('selftest',[sys.executable,str(tool),'--selftest'])
    refinements=scratch/'refinements.json'
    rr,_=run('refinements',[sys.executable,str(HERE/'refinement-reconcile.py'),'--tool',str(tool),'--output',str(refinements)])
    (output/'refinement-observed.json').write_bytes(refinements.read_bytes())
    source=tool.read_text()
    mutations=[
        ('count-only',[("claimed[field]!=Counter(hit_key(h) for h in actual)","sum(claimed[field].values())!=len(actual)")]),
        ('false-clearance',[("'privacy_clearance':False","'privacy_clearance':True")]),
        ('wrong-population',[("excluded=[h for h in hits if is_non_author(h)]","excluded=[h for h in hits if h['path']==paths['policy']]"),("scanner=[h for h in hits if not is_non_author(h)]","scanner=[h for h in hits if h['path']!=paths['policy']]")]),
    ]
    mutant_results=[]
    for name,replacements in mutations:
        changed=source
        for old,new_text in replacements:
            if old not in changed:raise RuntimeError('mutation_not_constructible')
            changed=changed.replace(old,new_text)
        mutant=scratch/('mutant-'+name+'.py');mutant.write_text(changed)
        result_path=scratch/('mutant-'+name+'.json')
        rc,_=run('mutant-'+name,args+['--tool',str(mutant),'--output',str(result_path)])
        observation=json.loads(result_path.read_bytes())
        killed=rc==1 and observation['counts']['unmet']>0 and observation['counts']['capability_absent']==0
        mutant_results.append({'id':name,'killed':killed,'exit_code':rc,'unmet':observation['counts']['unmet'],'tool_sha256':sha(mutant.read_bytes())})
        (output/('mutant-'+name+'-observed.json')).write_bytes(result_path.read_bytes())
    restored_path=scratch/'restored.json'
    restored_rc,_=run('restored-control',args+['--tool',str(tool),'--output',str(restored_path)])
    (output/'restored-observed.json').write_bytes(restored_path.read_bytes())
    mutations_ok=all(x['killed'] for x in mutant_results) and restored_rc==0 and sha(tool.read_bytes())==sha(source.encode())
    expected=json.loads((HERE/'frozen/expected-real.json').read_bytes())
    paths=expected['paths']
    realcmd=[sys.executable,str(tool),'check','--repo',str(LANE),'--rev',expected['input_revision'],'--receipt',paths['receipt'],'--policy',paths['policy'],'--allowlist',paths['allowlist']]
    realrc,real=run('real-reconciliation',realcmd)
    realmatch=realrc==0 and isinstance(real,dict) and all(type(real.get(k)) is type(v) and real.get(k)==v for k,v in expected['expected'].items()) and real.get('inputs_sha256')==expected['inputs_sha256']
    entering=realcmd.copy();entering[entering.index('--receipt')+1]='.ufo/waves/round-21/evidence/final/retention-floor-entering.json'
    er,enteringv=run('contradictory-entering-receipt',entering)
    enteringmatch=er==2 and isinstance(enteringv,dict) and enteringv.get('error')=='receipt_revision_conflict'
    gate=LANE/'tools/mori-retention-gate.py'
    gr,retention=run('current-retention-floor',[sys.executable,str(gate),'scan','--repo',str(LANE),'--rev',a.revision,'--policy',str(LANE/paths['policy']),'--allowlist',str(LANE/paths['allowlist'])])
    original=json.loads(json.loads((LANE/paths['receipt']).read_bytes())['stdout'])
    identity=lambda h:tuple(h[k] for k in ('path','line','class','line_sha256'))
    old=Counter(identity(h) for h in original['unallowlisted_hits'])
    new=Counter(identity(h) for h in retention.get('unallowlisted_hits',[])) if isinstance(retention,dict) else Counter()
    floor={'exit_code':gr,'unallowlisted':retention.get('metric') if isinstance(retention,dict) else None,'new_unallowlisted':sum((new-old).values()),'missing_unallowlisted':sum((old-new).values()),'same_inherited_identities':new==old,'privacy_clearance':False}
    stable={}
    for path in ['tools/mori-census.sh','tools/mori-retention-gate.py','tools/mori-evidence-loss.py','corpus/evidence/retention-allowlist.json','corpus/evidence/loss-accounting-r21.json','.ufo/waves/round-21/fixture-loss.py','.ufo/waves/round-21/evidence/final/fixture-original-control.json','corpus/evidence/baseline-r20-20261021T1051Z.json']:
        cp=subprocess.run(['git','-C',str(LANE),'show',BASE+':'+path],capture_output=True)
        stable[path]={'entering_sha256':sha(cp.stdout),'current_sha256':sha((LANE/path).read_bytes()),'unchanged':cp.returncode==0 and cp.stdout==(LANE/path).read_bytes()}
    before=json.loads(before_path.read_bytes());after=json.loads(after_path.read_bytes())
    summary={'schema':'mori-r22-measurements-v1','measured_revision':a.revision,'tool_sha256':sha(tool.read_bytes()),'before':before['counts'],'after':after['counts'],'selftest_exit':sr,'selftest':selftest,'refinement_exit':rr,'real_matches_frozen_expected':realmatch,'contradictory_entering_rejected':enteringmatch,'retention_floor':floor,'unchanged_carried_inputs':stable,'original_permission_control':'RED11/12 retained byte-unchanged, not rerun','historical_dispositions':'two unknown; baseline blocked','privacy_clearance':False,'raw_recount_authenticates_historical_execution':False}
    summary['mutations']={'cases':mutant_results,'restored_exit':restored_rc,'all_killed_and_restored':mutations_ok}
    # Preserve all synthetic workspace bytes in a portable archive before any cleanup.
    archive=output/'synthetic-workspaces.tar.gz'
    with tarfile.open(archive,'w:gz') as tar:tar.add(scratch,arcname='workspaces',recursive=True)
    with tarfile.open(archive,'r:gz') as tar:
        members={m.name:m for m in tar.getmembers()}
        for path in scratch.rglob('*'):
            name='workspaces/'+str(path.relative_to(scratch))
            if path.is_symlink():
                if name not in members or members[name].linkname!=os.readlink(path):raise RuntimeError('archive_symlink_mismatch')
            elif path.is_file():
                if name not in members or tar.extractfile(members[name]).read()!=path.read_bytes():raise RuntimeError('archive_byte_mismatch')
    summary['workspace_archive']={'path':archive.name,'sha256':sha(archive.read_bytes()),'every_file_byte_compared':True,'scratch_retained':str(scratch)}
    summary['all_claim_checks_pass']=br==1 and ar==0 and before['counts']['capability_absent']==24 and after['counts']['unmet']==0 and sr==0 and rr==0 and mutations_ok and realmatch and enteringmatch and gr==1 and floor['unallowlisted']==4 and floor['same_inherited_identities'] and all(x['unchanged'] for x in stable.values())
    write(output/'summary.json',summary)
    print(json.dumps({'measured_revision':a.revision,'before':summary['before'],'after':summary['after'],'real_matches_frozen_expected':realmatch,'retention_floor':floor,'all_claim_checks_pass':summary['all_claim_checks_pass']},sort_keys=True))
    return int(not summary['all_claim_checks_pass'])
if __name__=='__main__':raise SystemExit(main())
