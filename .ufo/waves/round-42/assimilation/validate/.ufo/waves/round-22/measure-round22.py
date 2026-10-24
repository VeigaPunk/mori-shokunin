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
def safe_outputs(observation):
    allowed={'schema','finding_id','receipt_match','differences','raw_total','policy_excluded','exclusion_basis','scanner_total','raw_unallowlisted','scanner_unallowlisted','raw_not_allowlisted','non_author','allowlisted','forbidden_allowlist','retention_state','privacy_clearance','input_revision','measured_revision','inputs_sha256','tool_sha256','argv','raw_hits','scanner_hits','policy_excluded_hits','receipt_authenticity','error'}
    rows=observation.get('runs',observation.get('cases',[]))
    for row in rows:
        stdout,stderr=row.get('stdout',''),row.get('stderr','')
        if stderr or any(marker in stdout+stderr for marker in ('R22_SAMPLE','retained-red','outside-author')):
            return False
        try:value=json.loads(stdout)
        except (ValueError,TypeError):return False
        if not isinstance(value,dict) or not set(value)<=allowed or value.get('privacy_clearance') is not False:
            return False
    return True
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
    FREEZE='e2f549befaffa1c1301928191e1eecb6142c0dad'
    for path in list(pinned)+['frozen/requirements-v2.json']:
        cp=subprocess.run(['git','-C',str(LANE),'show',FREEZE+':.ufo/waves/round-22/'+path],capture_output=True)
        if cp.returncode or cp.stdout!=(HERE/path).read_bytes():
            write(output/'summary.json',{'finding_id':'freeze_binding_mismatch','path':path,'freeze':FREEZE})
            print(json.dumps({'finding_id':'freeze_binding_mismatch','path':path}))
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
    bound_files=[tool,Path(__file__).resolve(),HERE/'refinement-reconcile.py',HERE/'oracle-reconcile-v2.py',HERE/'frozen/fixture-builder-v2.py',HERE/'frozen/requirements-v2.json',HERE/'frozen/expected-real.json']
    bindings={}
    for path in bound_files:
        rel=str(path.relative_to(LANE))
        cp=subprocess.run(['git','-C',str(LANE),'show',a.revision+':'+rel],capture_output=True)
        bindings[rel]={'committed_sha256':sha(cp.stdout),'loaded_sha256':sha(path.read_bytes()),'matches':cp.returncode==0 and cp.stdout==path.read_bytes()}
    write(output/'executing-input-bindings.json',bindings)
    if not all(x['matches'] for x in bindings.values()):
        write(output/'summary.json',{'finding_id':'measurement_inputs_uncommitted','bindings':bindings})
        print(json.dumps({'finding_id':'measurement_inputs_uncommitted'}))
        return 2
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
    # Each mutant names the exact rows (suite:id) that must go red; any-unmet is not credit.
    mutations=[
        ('count-only',[("claimed[field]!=Counter(hit_key(h) for h in actual)","sum(claimed[field].values())!=len(actual)")],{'frozen:R07','frozen:R08','frozen:R09'}),
        ('false-clearance',[("'privacy_clearance':False,'input_revision'","'privacy_clearance':True,'input_revision'")],{'frozen:R02'}),
        ('wrong-population',[("excluded=[h for h in hits if is_non_author(h)]","excluded=[h for h in hits if h['path']==paths['policy']]"),("scanner=[h for h in hits if not is_non_author(h)]","scanner=[h for h in hits if h['path']!=paths['policy']]")],{'frozen:R04'}),
        ('setup-leak',[("'error':str(exc)","'error':str(exc),'detail':'R22_SAMPLE retained-red'")],{'safety:all-arm-output'}),
        ('output-sets',[("'scanner_hits':scanner,'policy_excluded_hits':excluded","'scanner_hits':[h for h in hits if h['path']!=paths['policy']],'policy_excluded_hits':[h for h in hits if h['path']==paths['policy']]")],{'frozen:R04','refine:valid-identities'}),
        ('one-sided-hits',[("        if claimed[field]!=Counter(hit_key(h) for h in actual): differences.append(field)","        if (bool(Counter(hit_key(h) for h in actual)-claimed[field]) if field=='hits' else claimed[field]!=Counter(hit_key(h) for h in actual)): differences.append(field)")],{'frozen:R06','refine:inject-only'}),
        ('line-blind-raw',[("        if claimed[field]!=Counter(hit_key(h) for h in actual): differences.append(field)","        if (Counter((k[0],k[2],k[3]) for k in claimed[field].elements())!=Counter((h['path'],h['class'],h['line_sha256']) for h in actual) if field=='hits' else claimed[field]!=Counter(hit_key(h) for h in actual)): differences.append(field)")],{'refine:line-raw-only'}),
        ('metric-ignored',[("('metric',len(unallowed))","('metric',receipt['metric'] or len(unallowed))")],{'refine:metric-overstate'}),
        ('non-author-unchecked',[("('non_author',len(excluded)),","")],{'refine:non-author-counter'}),
        ('no-dotdot',[("p not in ('','..','.')","p not in ('','.')")],{'refine:unsafe-receipt','refine:unsafe-policy','refine:unsafe-allowlist'}),
        ('no-byte-compare',[("require(committed(repo,measured,paths[key])==raw[key],key+'_changed')","pass")],{'refine:policy-change-digest-updated','refine:allowlist-canonical-two-step'}),
        ('no-ancestor',[("require(git(repo,'merge-base','--is-ancestor',measured,revision,ok=(0,1)).returncode==0,'measured_not_ancestor')","pass")],{'refine:diverged-consistent','refine:cousin','refine:head-cousin'}),
        ('bool-lax',[("return type(value) is int and value>=0","return isinstance(value,int) and value>=0")],{'refine:boolean-metric','refine:boolean-non-author','refine:boolean-line-colliding'}),
        ('symlink-accepted',[("mode in (b'100644',b'100755')","mode in (b'100644',b'100755',b'120000')")],{'refine:symlink-identical'}),
        ('argv-empty',[("'argv':a.argv_seen","'argv':[]")],{'refine:clean-control'}),
        ('exit-unchecked',[("    if wrapper['exit_code']!=retention_code:differences.append('exit_code')","    pass")],{'refine:exit-code-lie'}),
        ('finding-unchecked',[(",('finding_id',retention_finding)","")],{'refine:finding-lie'}),
        ('routed-unchecked',[("('routed',routed),","")],{'refine:routed-lie'}),
        ('aux-unchecked',[("    if cf!=Counter(forbidden):differences.append('forbidden_allowlist')","    pass")],{'refine:forbidden-laundered','refine:forbidden-as-stale'}),
        ('forbidden-not-red',[("retention_code=int(bool(unallowed or forbidden))","retention_code=int(bool(unallowed))")],{'refine:forbidden-only'}),
        ('policy-copy-excluded',[("scanner=[h for h in hits if not is_non_author(h)]","scanner=[h for h in hits if not is_non_author(h) and not h['path'].endswith(paths['policy'].rsplit('/',1)[-1])]")],{'refine:nested-policy-copy'}),
        ('repo-unbound',[("require(os.path.realpath(top)==os.path.realpath(a.repo),'repo_not_toplevel')","pass")],{'refine:repo-subdirectory'}),
    ]
    def red_rows(oracle_obs,refine_obs):
        red={'frozen:'+r['id'] for r in oracle_obs['results'] if not r['pass']}
        red|={'refine:'+r['id'] for r in refine_obs['cases'] if not r['pass']}
        if not safe_outputs(oracle_obs) or not safe_outputs(refine_obs):red.add('safety:all-arm-output')
        return red
    mutant_results=[]
    for name,replacements,targets in mutations:
        changed=source
        for old,new_text in replacements:
            if changed.count(old)!=1:raise RuntimeError('mutation_not_constructible:'+name)
            changed=changed.replace(old,new_text)
        mutant=scratch/('mutant-'+name+'.py');mutant.write_text(changed)
        frozen_path=scratch/('mutant-'+name+'.json');refine_path=scratch/('mutant-'+name+'-refine.json')
        rc,_=run('mutant-'+name,args+['--tool',str(mutant),'--output',str(frozen_path)])
        rrc,_=run('mutant-'+name+'-refine',[sys.executable,str(HERE/'refinement-reconcile.py'),'--tool',str(mutant),'--output',str(refine_path)])
        fobs=json.loads(frozen_path.read_bytes());robs=json.loads(refine_path.read_bytes())
        red=red_rows(fobs,robs)
        mutant_results.append({'id':name,'targets':sorted(targets),'red_rows':sorted(red),'killed':targets<=red,'frozen_exit':rc,'refine_exit':rrc,'frozen_unmet':fobs['counts']['unmet'],'tool_sha256':sha(mutant.read_bytes())})
        (output/('mutant-'+name+'-observed.json')).write_bytes(frozen_path.read_bytes())
        (output/('mutant-'+name+'-refine-observed.json')).write_bytes(refine_path.read_bytes())
    restored_path=scratch/'restored.json';restored_refine=scratch/'restored-refine.json'
    restored_rc,_=run('restored-control',args+['--tool',str(tool),'--output',str(restored_path)])
    restored_rrc,_=run('restored-control-refine',[sys.executable,str(HERE/'refinement-reconcile.py'),'--tool',str(tool),'--output',str(restored_refine)])
    (output/'restored-observed.json').write_bytes(restored_path.read_bytes())
    (output/'restored-refine-observed.json').write_bytes(restored_refine.read_bytes())
    restored_red=red_rows(json.loads(restored_path.read_bytes()),json.loads(restored_refine.read_bytes()))
    mutations_ok=all(x['killed'] for x in mutant_results) and restored_rc==0 and restored_rrc==0 and not restored_red and sha(tool.read_bytes())==sha(source.encode())
    expected=json.loads((HERE/'frozen/expected-real.json').read_bytes())
    paths=expected['paths']
    realcmd=[sys.executable,str(tool),'check','--repo',str(LANE),'--rev',expected['input_revision'],'--receipt',paths['receipt'],'--policy',paths['policy'],'--allowlist',paths['allowlist']]
    realrc,real=run('real-reconciliation',realcmd)
    realmatch=realrc==0 and isinstance(real,dict) and all(type(real.get(k)) is type(v) and real.get(k)==v for k,v in expected['expected'].items()) and real.get('inputs_sha256')==expected['inputs_sha256']
    realmatch=realmatch and real.get('input_revision')==expected['input_revision'] and real.get('measured_revision')==expected['measured_revision'] and real.get('tool_sha256')==sha(code_cp.stdout) and real.get('argv')==realcmd[2:]
    identity_expected=json.loads((HERE/'frozen/expected-real-identities.json').read_bytes())['digests']
    def identity_digest(hits):return sha(json.dumps(sorted(tuple(h[k] for k in ('path','line','class','line_sha256')) for h in hits),separators=(',',':')).encode())
    identity_observed={k:identity_digest(real.get(k,[])) for k in identity_expected} if isinstance(real,dict) else {}
    identity_match=identity_observed==identity_expected
    # Same-command failing twin: the identical real command with output identities swapped must not match.
    twin_observed=dict(identity_observed);twin_observed['scanner_hits'],twin_observed['policy_excluded_hits']=identity_observed.get('policy_excluded_hits'),identity_observed.get('scanner_hits')
    identity_twin_rejected=twin_observed!=identity_expected
    # raw_unallowlisted is a frozen alias of the policy metric; the truthful raw complement is 95-86=9.
    raw_complement_ok=isinstance(real,dict) and real.get('raw_not_allowlisted')==real.get('raw_total',0)-real.get('allowlisted',0)==9
    realmatch=realmatch and identity_match and identity_twin_rejected and raw_complement_ok
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
    evidence_safe=safe_outputs(after) and safe_outputs(json.loads(refinements.read_bytes())) and safe_outputs(json.loads(restored_path.read_bytes()))
    summary={'schema':'mori-r22-measurements-v1','measured_revision':a.revision,'tool_sha256':sha(tool.read_bytes()),'before':before['counts'],'after':after['counts'],'selftest_exit':sr,'selftest':selftest,'refinement_exit':rr,'real_matches_frozen_expected':realmatch,'contradictory_entering_rejected':enteringmatch,'retention_floor':floor,'unchanged_carried_inputs':stable,'original_permission_control':'RED11/12 retained byte-unchanged, not rerun','historical_dispositions':'two unknown; baseline blocked','privacy_clearance':False,'raw_recount_authenticates_historical_execution':False}
    summary['mutations']={'cases':mutant_results,'restored_exit':restored_rc,'all_killed_and_restored':mutations_ok}
    summary['all_arm_output_safety']=evidence_safe
    summary['executing_input_bindings']=bindings
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
    summary['real_identity']={'expected':identity_expected,'observed':identity_observed,'match':identity_match,'swapped_twin_rejected':identity_twin_rejected}
    summary['all_claim_checks_pass']=br==1 and ar==0 and before['counts']['capability_absent']==24 and after['counts']['unmet']==0 and sr==0 and rr==0 and mutations_ok and evidence_safe and realmatch and enteringmatch and gr==1 and floor['unallowlisted']==4 and floor['same_inherited_identities'] and all(x['unchanged'] for x in stable.values())
    write(output/'summary.json',summary)
    print(json.dumps({'measured_revision':a.revision,'before':summary['before'],'after':summary['after'],'real_matches_frozen_expected':realmatch,'retention_floor':floor,'all_claim_checks_pass':summary['all_claim_checks_pass']},sort_keys=True))
    return int(not summary['all_claim_checks_pass'])
if __name__=='__main__':raise SystemExit(main())
