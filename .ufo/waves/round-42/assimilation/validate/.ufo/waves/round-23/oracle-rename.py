#!/usr/bin/env python3
"""Round-23 C1 oracle: r22 v2 requirements re-expressed for schema v2, plus R25/R26.

Authored by the L1 before any C1 implementation change. R01-R24 predicates are the
r22 frozen v2 predicates with raw_unallowlisted -> scanner_unallowlisted substituted
in R02/R11/R12 only."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location('r22_fixture_builder',HERE.parent/'round-22'/'frozen'/'fixture-builder-v2.py')
FIX=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FIX)

def main():
    p=argparse.ArgumentParser(); p.add_argument('--tool',required=True); p.add_argument('--requirements',required=True); p.add_argument('--output',required=True)
    a=p.parse_args(); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    expected=json.loads(Path(a.requirements).read_bytes())
    ids=expected['requirements']
    tool=Path(a.tool).resolve()
    data={'schema':'mori-r23-c1-observations-v1','tool':str(tool),'requirements_sha256':FIX.digest(Path(a.requirements).read_bytes()),'fixture_builder_sha256':FIX.digest(Path(FIX.__file__).read_bytes()),'oracle_sha256':FIX.digest(Path(__file__).read_bytes()),'results':[],'runs':[]}
    if not tool.is_file():
        data['results']=[{'id':i,'pass':False,'reason':'capability_absent'} for i in ids]
    else:
        data['tool_sha256']=FIX.digest(tool.read_bytes())
        fixture_root=out.parent/(out.stem+'-fixtures'); fixture_root.mkdir(exist_ok=False)
        cache={}
        def invoke(variant='valid',receipt_override=None):
            key=(variant,receipt_override)
            if key in cache:return cache[key]
            f=FIX.make(fixture_root/(variant+('-unsafe' if receipt_override else '')),variant)
            cmd=[sys.executable,str(tool),'check','--repo',f['repo'],'--rev',f['rev'],'--receipt',receipt_override or f['receipt'],'--policy',f['policy'],'--allowlist',f['allowlist']]
            cp=subprocess.run(cmd,capture_output=True,text=True,timeout=60)
            try: v=json.loads(cp.stdout)
            except (ValueError,TypeError):v=None
            row={'variant':variant,'argv':cmd,'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr,'fixture':f}
            data['runs'].append(row); cache[key]=(cp,v,f); return cache[key]
        def record(rid,variant='valid',code=0,finding='RETENTION_RECONCILED',predicate=None,receipt_override=None):
            cp,v,f=invoke(variant,receipt_override)
            ok=cp.returncode==code and isinstance(v,dict) and v.get('finding_id')==finding and cp.stderr==''
            if predicate:
                try: ok=ok and predicate(v,f)
                except (KeyError,TypeError,ValueError):ok=False
            data['results'].append({'id':rid,'pass':bool(ok),'variant':variant,'expected_exit':code,'expected_finding':finding})
        record('R01')
        record('R02',predicate=lambda v,f:v['scanner_unallowlisted']==1 and v['scanner_unallowlisted']==1 and v['retention_state']=='red' and v['privacy_clearance'] is False)
        record('R03',predicate=lambda v,f:(v['raw_total'],v['policy_excluded'],v['scanner_total'])==(5,1,4))
        record('R04',predicate=lambda v,f:sorted(v['scanner_hits'],key=lambda h:(h['path'],h['line']))==sorted(f['expected_scanner_hits'],key=lambda h:(h['path'],h['line'])) and v['policy_excluded_hits']==f['expected_policy_hits'])
        for rid,variant in [('R05','drop'),('R06','inject'),('R07','digest'),('R08','line'),('R09','class'),('R10','metric')]:record(rid,variant,1,'RETENTION_RECONCILIATION_MISMATCH')
        record('R11','forbidden',predicate=lambda v,f:v['forbidden_allowlist']==1 and v['scanner_unallowlisted']==3 and v['retention_state']=='red' and v['privacy_clearance'] is False)
        record('R12',predicate=lambda v,f:v['non_author']==1 and v['scanner_unallowlisted']==1 and v['raw_total']==5)
        for rid,variant in [('R13','invalid-revision'),('R14','diverged'),('R15','policy-changed'),('R16','allowlist-changed'),('R17','malformed'),('R18','bool-line'),('R19','duplicate')]:record(rid,variant,2,'RETENTION_RECONCILIATION_SETUP')
        # Additional bool-metric arm is conjunctive in R18, not a hidden extra requirement.
        cp,v,f=invoke('bool-metric'); data['results'][-2]['pass'] &= cp.returncode==2 and isinstance(v,dict) and v.get('finding_id')=='RETENTION_RECONCILIATION_SETUP'
        record('R20',receipt_override='../receipt.json',code=2,finding='RETENTION_RECONCILIATION_SETUP')
        record('R21','symlink',2,'RETENTION_RECONCILIATION_SETUP')
        record('R22',predicate=lambda v,f:v['raw_total']==5 and all(h['path']!='binary.bin' for h in v['raw_hits']))
        record('R23',predicate=lambda v,f:'R22_SAMPLE' not in json.dumps(v) and 'retained-red' not in json.dumps(v) and v['privacy_clearance'] is False)
        record('R24',predicate=lambda v,f:v['input_revision']==f['rev'] and v['measured_revision']==f['measured_revision'] and v['tool_sha256']==FIX.digest(tool.read_bytes()) and v['inputs_sha256']=={'receipt':f['expected_receipt_sha256'],'policy':f['expected_policy_sha256'],'allowlist':f['expected_allowlist_sha256']} and isinstance(v['argv'],list))
        def raw_not_allowlisted(f):
            # Independent count from the fixture's committed policy/allowlist bytes.
            repo=f['repo']
            pol=json.loads(subprocess.run(['git','-C',repo,'show','HEAD:'+f['policy']],capture_output=True,check=True).stdout)
            allow=json.loads(subprocess.run(['git','-C',repo,'show','HEAD:'+f['allowlist']],capture_output=True,check=True).stdout)
            must=set(pol['must_redact_paths'])
            keys={(r['path'],r['class'],r['line_sha256']) for r in allow['rows'] if r['path'] not in must}
            raw=f['expected_scanner_hits']+f['expected_policy_hits']
            return sum((h['path'],h['class'],h['line_sha256']) not in keys for h in raw)
        record('R26',predicate=lambda v,f:v['raw_not_allowlisted']==raw_not_allowlisted(f)==2)
        cp,v,f=invoke('forbidden'); data['results'][-1]['pass'] &= isinstance(v,dict) and v.get('raw_not_allowlisted')==raw_not_allowlisted(f)==4
        parsed=[]
        for row in data['runs']:
            try: obj=json.loads(row['stdout'])
            except (ValueError,TypeError): obj=None
            if isinstance(obj,dict): parsed.append(obj)
        data['misleading_alias_runs']=sum('raw_unallowlisted' in o for o in parsed)
        data['schema_v2_runs']=sum(o.get('schema')=='mori-retention-reconciliation-v2' for o in parsed)
        data['parsed_runs']=len(parsed)
        data['results'].insert(24,{'id':'R25','pass':bool(parsed) and data['misleading_alias_runs']==0 and data['schema_v2_runs']==len(parsed),'variant':'all-runs','expected_exit':None,'expected_finding':None})
        # Every generated input, including object database, retained and digested.
        data['fixture_files']={str(x.relative_to(fixture_root)):FIX.digest(x.read_bytes()) for x in fixture_root.rglob('*') if x.is_file() and not x.is_symlink()}
    data['counts']={'total':len(data['results']),'pass':sum(r['pass'] for r in data['results']),'capability_absent':sum(r.get('reason')=='capability_absent' for r in data['results'])}
    data['counts']['unmet']=data['counts']['total']-data['counts']['pass']
    data['counts']['misleading_alias_runs']=data.get('misleading_alias_runs')
    out.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'finding_id':'R23_C1_REQUIREMENTS_MATCH' if not data['counts']['unmet'] else 'R23_C1_REQUIREMENTS_UNMET','counts':data['counts'],'output':str(out)},sort_keys=True))
    return int(bool(data['counts']['unmet']))
if __name__=='__main__':raise SystemExit(main())
