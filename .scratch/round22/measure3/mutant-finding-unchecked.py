#!/usr/bin/env python3
"""Reconcile committed retention accounting. Agreement never grants clearance."""
from __future__ import annotations
import argparse
from collections import Counter
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

SCHEMA='mori-retention-reconciliation-v1'
SETUP='RETENTION_RECONCILIATION_SETUP'
MATCH='RETENTION_RECONCILED'
MISMATCH='RETENTION_RECONCILIATION_MISMATCH'
OID=re.compile(r'(?:[0-9a-f]{40}|[0-9a-f]{64})\Z')
SHA=re.compile(r'[0-9a-f]{64}\Z')
HIT_FIELDS={'path','line','class','line_sha256'}

class Invalid(Exception):
    pass

def require(condition, reason):
    if not condition: raise Invalid(reason)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def integer(value):
    return type(value) is int and value>=0

def no_duplicates(pairs):
    obj={}
    for key,value in pairs:
        require(key not in obj,'duplicate_json_key')
        obj[key]=value
    return obj

def parse(data):
    try:
        text=data.decode('utf-8','strict') if isinstance(data,bytes) else data
        require(not text.startswith('\ufeff'),'invalid_json')
        return json.loads(text,object_pairs_hook=no_duplicates,parse_constant=lambda _:(_ for _ in ()).throw(Invalid('invalid_json_constant')))
    except (ValueError,UnicodeError,RecursionError):
        raise Invalid('invalid_json') from None

def safe_path(path):
    require(isinstance(path,str) and path and not path.startswith('/') and all(p not in ('','..','.') for p in path.split('/')) and not any(ord(c)<32 or ord(c)==127 for c in path),'unsafe_input_path')
    return path

def git(repo,*args,ok=(0,)):
    env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1',GIT_LITERAL_PATHSPECS='1')
    try:
        cp=subprocess.run(['git','--no-replace-objects','-C',str(repo),*args],capture_output=True,env=env,timeout=60)
    except (OSError,subprocess.TimeoutExpired): raise Invalid('git_unavailable') from None
    require(cp.returncode in ok,'git_read_failed')
    return cp

def git_out(repo,*args):
    return git(repo,*args).stdout

def resolve(repo,selector):
    require(isinstance(selector,str) and selector and not any(ord(c)<32 for c in selector),'invalid_revision')
    value=git_out(repo,'rev-parse','--verify','--end-of-options',selector+'^{commit}').decode('ascii').strip()
    require(bool(OID.fullmatch(value)),'invalid_resolved_commit')
    return value

def tree(repo,revision,path=None):
    args=['ls-tree','-r','-z','--full-tree',revision]
    if path is not None: args+=['--',path]
    rows=[]
    for row in git_out(repo,*args).split(b'\0'):
        if not row: continue
        try:
            meta,name=row.split(b'\t',1); mode,kind,oid=meta.split()
            name=name.decode('utf8',errors='strict')
        except (ValueError,UnicodeError): raise Invalid('invalid_tree_path') from None
        rows.append((mode,kind,oid,name))
    return rows

def committed(repo,revision,path):
    rows=tree(repo,revision,safe_path(path))
    require(len(rows)==1 and rows[0][3]==path,'missing_input_blob')
    mode,kind,oid,_=rows[0]
    require(mode in (b'100644',b'100755') and kind==b'blob','input_not_regular')
    return git_out(repo,'cat-file','blob',oid.decode('ascii'))

def policy_rules(obj):
    require(isinstance(obj,dict) and obj.get('schema')=='mori-retention-policy-v1','policy_schema')
    values=obj.get('classes'); require(isinstance(values,list) and values,'policy_classes')
    classes=[]; seen=set()
    for row in values:
        require(isinstance(row,dict),'policy_class')
        cid,expression=row.get('id'),row.get('regex')
        require(isinstance(cid,str) and cid and cid not in seen and isinstance(expression,str),'policy_class')
        try: compiled=re.compile(expression)
        except (re.error,OverflowError,RecursionError): raise Invalid('policy_regex') from None
        seen.add(cid); classes.append((cid,compiled))
    must=obj.get('must_redact_paths'); nonauthor=obj.get('non_author_paths_glob')
    require(isinstance(must,list) and all(isinstance(x,str) and x for x in must),'policy_must_paths')
    require(isinstance(nonauthor,list) and all(isinstance(x,str) and x for x in nonauthor),'policy_non_author')
    return classes,set(must),nonauthor

def allow_rows(obj,classes):
    if isinstance(obj,dict): obj=obj.get('rows')
    require(isinstance(obj,list),'allowlist_shape')
    rows=[]; seen=set(); known={c for c,_ in classes}
    for row in obj:
        require(isinstance(row,dict) and set(row)=={'path','class','line_sha256','reason','rule'},'allowlist_row')
        path,cid,sha,reason,rule=(row[x] for x in ('path','class','line_sha256','reason','rule'))
        require(isinstance(path,str) and path and isinstance(cid,str) and cid in known and isinstance(sha,str) and bool(SHA.fullmatch(sha)) and isinstance(reason,str) and reason.strip() and isinstance(rule,str) and rule in ('a','b','c'),'allowlist_row')
        key=(path,cid,sha); require(key not in seen,'duplicate_allowlist')
        seen.add(key); rows.append(row)
    return rows

def hit_key(hit):
    return tuple(hit[k] for k in ('path','line','class','line_sha256'))

def normalize_hits(value):
    require(isinstance(value,list),'receipt_hit_list')
    seen=set()
    for hit in value:
        require(isinstance(hit,dict) and set(hit)==HIT_FIELDS,'receipt_hit')
        require(isinstance(hit['path'],str) and hit['path'] and integer(hit['line']) and hit['line']>0 and isinstance(hit['class'],str) and hit['class'] and isinstance(hit['line_sha256'],str) and bool(SHA.fullmatch(hit['line_sha256'])),'receipt_hit_type')
        key=hit_key(hit); require(key not in seen,'duplicate_receipt_hit'); seen.add(key)
    return Counter(hit_key(h) for h in value)

def auxiliary(value,kind):
    require(isinstance(value,list),'receipt_auxiliary')
    for row in value:
        require(isinstance(row,dict) and set(row)==HIT_FIELDS|{'finding_id'},'receipt_auxiliary')
        require(row.get('finding_id')==kind and row.get('line') is None,'receipt_auxiliary_type')
        require(isinstance(row['path'],str) and row['path'] and isinstance(row['class'],str) and isinstance(row['line_sha256'],str) and bool(SHA.fullmatch(row['line_sha256'])),'receipt_auxiliary_type')
    keys=[(r['path'],r['class'],r['line_sha256']) for r in value]
    require(len(set(keys))==len(keys),'duplicate_auxiliary')
    return Counter(keys)

def scan(repo,revision,classes):
    hits=[]; cache={}
    for mode,kind,oid,path in tree(repo,revision):
        if kind!=b'blob': continue
        # Identical blobs share parsing work while path remains part of every identity.
        if oid not in cache:
            raw=git_out(repo,'cat-file','blob',oid.decode('ascii')); parsed=[]
            if b'\0' not in raw:
                for n,line in enumerate(raw.decode('utf8',errors='replace').split('\n'),1):
                    for cid,expression in classes:
                        if expression.search(line): parsed.append((n,cid,digest(line.encode('utf8'))))
            cache[oid]=parsed
        hits.extend({'path':path,'line':n,'class':cid,'line_sha256':sha} for n,cid,sha in cache[oid])
    normalize_hits(hits)
    return hits

def check(a):
    require(isinstance(a.repo,str) and a.repo.startswith('/') and not any(ord(c)<32 for c in a.repo),'repo_not_absolute')
    repo=Path(a.repo)
    # Discovery must not climb from a plain subdirectory into an enclosing repository.
    top=git_out(repo,'rev-parse','--show-toplevel').decode('utf8','strict').strip()
    require(os.path.realpath(top)==os.path.realpath(a.repo),'repo_not_toplevel')
    revision=resolve(repo,a.rev)
    paths={'receipt':safe_path(a.receipt),'policy':safe_path(a.policy),'allowlist':safe_path(a.allowlist)}
    raw={k:committed(repo,revision,p) for k,p in paths.items()}
    wrapper=parse(raw['receipt'])
    require(isinstance(wrapper,dict) and wrapper.get('schema')=='mori-r21-command-receipt-v1','receipt_schema')
    measured=wrapper.get('measured_revision')
    require(isinstance(measured,str) and bool(OID.fullmatch(measured)),'receipt_revision')
    peeled=git(repo,'rev-parse','--verify','--quiet','--end-of-options',measured+'^{commit}',ok=(0,1,128))
    require(peeled.returncode==0 and peeled.stdout.decode('ascii','replace').strip()==measured,'receipt_revision')
    # --is-ancestor: 0 ancestor, 1 divergence (distinct finding), other nonzero unevaluable.
    require(git(repo,'merge-base','--is-ancestor',measured,revision,ok=(0,1)).returncode==0,'measured_not_ancestor')
    for key in ('policy','allowlist'):
        require(committed(repo,measured,paths[key])==raw[key],key+'_changed')
    classes,must,patterns=policy_rules(parse(raw['policy']))
    allow=allow_rows(parse(raw['allowlist']),classes)
    require(integer(wrapper.get('exit_code')) and wrapper['exit_code'] in (0,1),'receipt_exit_type')
    require(isinstance(wrapper.get('stderr'),str) and wrapper['stderr']=='','receipt_stderr')
    require(isinstance(wrapper.get('stdout'),str),'receipt_stdout')
    argv=wrapper.get('argv'); require(isinstance(argv,list) and all(isinstance(x,str) for x in argv),'receipt_argv')
    def recorded_option(flag):
        require(argv.count(flag)==1 and argv.index(flag)+1<len(argv),'receipt_argv_binding')
        return argv[argv.index(flag)+1]
    recorded_repo=recorded_option('--repo').rstrip('/')
    require(recorded_repo.startswith('/') and not any(ord(c)<32 for c in recorded_repo),'receipt_repo_binding')
    for key in ('policy','allowlist'):
        recorded=recorded_option('--'+key)
        if recorded.startswith('/'):
            require(recorded.startswith(recorded_repo+'/'),'receipt_path_binding')
            recorded=recorded[len(recorded_repo)+1:]
        require(safe_path(recorded)==paths[key],'receipt_path_binding')
    # A wrapper revision never overrides the command or inner result revision.
    require(argv.count('--rev')==1 and argv.index('--rev')+1<len(argv) and argv[argv.index('--rev')+1]==measured,'receipt_revision_conflict')
    receipt=parse(wrapper['stdout']); require(isinstance(receipt,dict),'receipt_result')
    require(receipt.get('commit')==measured,'receipt_revision_conflict')
    require(receipt.get('policy_sha256')==digest(raw['policy']),'receipt_policy_digest')
    for field in ('metric','routed','non_author'): require(integer(receipt.get(field)),'receipt_counter_type')
    claimed={field:normalize_hits(receipt.get(field)) for field in ('hits','unallowlisted_hits','allowlisted_hits')}
    cf=auxiliary(receipt.get('forbidden_allowlist'),'allowlist_forbidden')
    cw=auxiliary(receipt.get('warnings'),'allowlist_stale')
    require(isinstance(receipt.get('finding_id'),str),'receipt_finding')
    # Optional expected-population runs need their own bound input, not an inferred green.
    require(not any(k in receipt for k in ('population_commit','population_match','new_hits','missing_population_hits')),'unsupported_population_receipt')
    hits=scan(repo,measured,classes)
    hit_allow_keys={(h['path'],h['class'],h['line_sha256']) for h in hits}
    forbidden=[]; stale=[]; allowed_keys=set()
    for row in allow:
        key=(row['path'],row['class'],row['line_sha256'])
        if row['path'] in must: forbidden.append(key)
        elif key in hit_allow_keys: allowed_keys.add(key)
        else: stale.append(key)
    is_non_author=lambda h:any(fnmatch.fnmatch(h['path'],pattern) for pattern in patterns)
    excluded=[h for h in hits if is_non_author(h)]
    scanner=[h for h in hits if not is_non_author(h)]
    allowed=[h for h in hits if (h['path'],h['class'],h['line_sha256']) in allowed_keys]
    unallowed=[h for h in scanner if (h['path'],h['class'],h['line_sha256']) not in allowed_keys]
    routed=sum(h['path'] in must for h in unallowed)
    retention_code=int(bool(unallowed or forbidden))
    retention_finding='allowlist_forbidden' if forbidden else 'RETENTION_FINDINGS' if unallowed else 'allowlist_stale' if stale else 'RETENTION_CLEAN'
    differences=[]
    for field,actual in (('hits',hits),('allowlisted_hits',allowed),('unallowlisted_hits',unallowed)):
        if claimed[field]!=Counter(hit_key(h) for h in actual): differences.append(field)
    for field,actual in (('metric',len(unallowed)),('routed',routed),('non_author',len(excluded))):
        if receipt[field]!=actual:differences.append(field)
    if cf!=Counter(forbidden):differences.append('forbidden_allowlist')
    if cw!=Counter(stale):differences.append('warnings')
    if wrapper['exit_code']!=retention_code:differences.append('exit_code')
    return {'schema':SCHEMA,'finding_id':MISMATCH if differences else MATCH,
            'receipt_match':not differences,'differences':differences,
            'raw_total':len(hits),'policy_excluded':len(excluded),'exclusion_basis':'non_author_paths_glob',
            'scanner_total':len(scanner),'raw_unallowlisted':len(unallowed),'scanner_unallowlisted':len(unallowed),
            'raw_not_allowlisted':sum((h['path'],h['class'],h['line_sha256']) not in allowed_keys for h in hits),
            'non_author':len(excluded),'allowlisted':len(allowed),'forbidden_allowlist':len(forbidden),
            'retention_state':'red' if retention_code else 'clean-at-frozen-regex-scope',
            'privacy_clearance':False,'input_revision':revision,'measured_revision':measured,
            'receipt_authenticity':'unattested',
            'inputs_sha256':{k:digest(v) for k,v in raw.items()},'tool_sha256':digest(Path(__file__).read_bytes()),
            'argv':a.argv_seen,'raw_hits':hits,'scanner_hits':scanner,'policy_excluded_hits':excluded},int(bool(differences))

class Parser(argparse.ArgumentParser):
    def error(self,message): raise Invalid('usage')

def selftest():
    # Isolated actual CLI invocations; frozen independent oracle is separate evidence.
    with tempfile.TemporaryDirectory(prefix='mori-reconcile-') as td:
        root=Path(td)/'repo'; root.mkdir()
        env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
        env.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',GIT_AUTHOR_NAME='synthetic',GIT_AUTHOR_EMAIL='synthetic@example.invalid',GIT_COMMITTER_NAME='synthetic',GIT_COMMITTER_EMAIL='synthetic@example.invalid')
        def run_git(*args):
            cp=subprocess.run(['git','-C',str(root),*args],env=env,capture_output=True)
            require(cp.returncode==0,'selftest_fixture'); return cp.stdout.decode().strip()
        run_git('init','-q')
        policy={'schema':'mori-retention-policy-v1','classes':[{'id':'R22','regex':'[R]22_SAMPLE'}],'must_redact_paths':[],'non_author_paths_glob':[]}
        (root/'policy.json').write_text(json.dumps(policy)); (root/'allow.json').write_text('[]'); (root/'sample.txt').write_text('R22_SAMPLE\n')
        run_git('add','--all');run_git('commit','-q','-m','measured')
        measured=run_git('rev-parse','HEAD'); h={'path':'sample.txt','line':1,'class':'R22','line_sha256':digest(b'R22_SAMPLE')}
        inner={'finding_id':'RETENTION_FINDINGS','commit':measured,'policy_sha256':digest((root/'policy.json').read_bytes()),'metric':1,'routed':0,'non_author':0,'hits':[h],'unallowlisted_hits':[h],'allowlisted_hits':[],'forbidden_allowlist':[],'warnings':[]}
        wrapper={'schema':'mori-r21-command-receipt-v1','measured_revision':measured,'argv':['scan','--repo',str(root),'--rev',measured,'--policy','policy.json','--allowlist','allow.json'],'exit_code':1,'stdout':json.dumps(inner),'stderr':''}
        (root/'receipt.json').write_text(json.dumps(wrapper))
        wrong=dict(wrapper);wrong['stdout']=json.dumps(inner|{'hits':[]})
        (root/'wrong.json').write_text(json.dumps(wrong))
        run_git('add','--all');run_git('commit','-q','-m','receipt');rev=run_git('rev-parse','HEAD')
        base=[sys.executable,str(Path(__file__).resolve()),'check','--repo',str(root),'--rev',rev,'--receipt','receipt.json','--policy','policy.json','--allowlist','allow.json']
        bad=base.copy();bad[bad.index('--receipt')+1]='wrong.json'
        passed=0; total=4
        for cmd,code,finding in ((base,0,MATCH),(bad,1,MISMATCH),(base[:-1]+['../allow.json'],2,SETUP),(base+['--unknown'],2,SETUP)):
            cp=subprocess.run(cmd,capture_output=True,text=True,env=env)
            try:v=json.loads(cp.stdout)
            except ValueError:v={}
            passed+=cp.returncode==code and v.get('finding_id')==finding and v.get('privacy_clearance') is False and cp.stderr==''
        return {'schema':SCHEMA,'finding_id':'RECONCILE_SELFTEST_PASS' if passed==total else 'RECONCILE_SELFTEST_FAIL','passed':passed,'total':total,'privacy_clearance':False},int(passed!=total)

def main(argv=None):
    try:
        parser=Parser(description=__doc__,add_help=False); parser.add_argument('--selftest',action='store_true'); sub=parser.add_subparsers(dest='command')
        p=sub.add_parser('check',add_help=False); p.add_argument('--repo',required=True);p.add_argument('--rev',required=True);p.add_argument('--receipt',required=True);p.add_argument('--policy',required=True);p.add_argument('--allowlist',required=True)
        args=parser.parse_args(argv)
        args.argv_seen=list(sys.argv[1:] if argv is None else argv)
        if args.selftest:
            require(args.command is None,'usage'); result,code=selftest()
        else:
            require(args.command=='check','usage');result,code=check(args)
    except Invalid as exc:
        result={'schema':SCHEMA,'finding_id':SETUP,'error':str(exc),'privacy_clearance':False,'receipt_match':False};code=2
    except (OSError,UnicodeError,ValueError,TypeError,KeyError,RecursionError,MemoryError):
        result={'schema':SCHEMA,'finding_id':SETUP,'error':'input_unavailable','privacy_clearance':False,'receipt_match':False};code=2
    try:
        print(json.dumps(result,sort_keys=True,separators=(',',':')))
        sys.stdout.flush()
    except OSError:
        # A closed stdout cannot carry a verdict; never reuse the mismatch code.
        os._exit(2)
    return code
if __name__=='__main__':raise SystemExit(main())
