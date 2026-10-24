#!/usr/bin/env python3
"""L1-authored independent synthetic fixture inputs; never import the SUT."""
from __future__ import annotations
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess

TOKEN = 'R22_SAMPLE'
POLICY = 'policy.json'
ALLOW = 'allowlist.json'
RECEIPT = 'receipt.json'

def encoded(obj):
    return (json.dumps(obj, sort_keys=True, indent=2) + '\n').encode()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def git(repo, *args, data=None):
    env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null',
               GIT_AUTHOR_NAME='synthetic', GIT_AUTHOR_EMAIL='synthetic@example.invalid',
               GIT_COMMITTER_NAME='synthetic', GIT_COMMITTER_EMAIL='synthetic@example.invalid',
               GIT_AUTHOR_DATE='2026-10-21T00:00:00Z', GIT_COMMITTER_DATE='2026-10-21T00:00:00Z')
    for key in list(env):
        if key.startswith(('GIT_TRACE', 'GIT_CONFIG_KEY_', 'GIT_CONFIG_VALUE_')) or key in ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_CONFIG_COUNT'):
            env.pop(key, None)
    cp = subprocess.run(['git', '-C', str(repo), *args], input=data, capture_output=True, env=env)
    if cp.returncode:
        raise RuntimeError('fixture_git_failed')
    return cp.stdout

def make(root: Path, variant='valid'):
    root.mkdir(parents=True, exist_ok=False)
    git(root, 'init', '-q')
    policy = {'schema':'mori-retention-policy-v1', 'classes':[{'id':'R22','regex':'[R]22_SAMPLE'}],
              'must_redact_paths':[], 'non_author_paths_glob':['non-author.txt'], 'synthetic':TOKEN}
    files = {POLICY:encoded(policy), 'allowed.txt':(TOKEN+' allowed\n'+TOKEN+' allowed\n').encode(),
             'unallowed.txt':(TOKEN+' retained-red\n').encode(),
             'non-author.txt':(TOKEN+' outside-author\n').encode(),
             'binary.bin':(TOKEN+'\x00must-not-count').encode()}
    if variant=='forbidden':
        policy['must_redact_paths']=['allowed.txt']
        files[POLICY]=encoded(policy)
    hits=[]
    import re
    for path, data in files.items():
        if b'\0' in data: continue
        for n,line in enumerate(data.decode('utf8',errors='replace').split('\n'),1):
            if re.search('[R]22_SAMPLE',line):
                hits.append({'path':path,'line':n,'class':'R22','line_sha256':digest(line.encode())})
    allowed=[h for h in hits if h['path'] in (POLICY,'allowed.txt')]
    rows=[]
    for h in allowed:
        row={k:v for k,v in h.items() if k!='line'}
        row['reason']='synthetic field name only'
        row['rule']='b'
        if row not in rows: rows.append(row)
    files[ALLOW]=encoded({'rows':rows})
    for path,data in files.items(): (root/path).write_bytes(data)
    git(root,'add','--all'); git(root,'commit','-q','-m','synthetic measured tree')
    measured=git(root,'rev-parse','HEAD').decode().strip()
    forbidden=[]
    allowed_effective=allowed
    unallowed=[h for h in hits if h['path']=='unallowed.txt']
    if variant=='forbidden':
        forbidden=[{'finding_id':'allowlist_forbidden',**{k:v for k,v in r.items() if k not in ('reason','rule')},'line':None} for r in rows if r['path']=='allowed.txt']
        allowed_effective=[h for h in allowed if h['path']!='allowed.txt']
        unallowed=unallowed+[h for h in hits if h['path']=='allowed.txt']
    result={'finding_id':'allowlist_forbidden' if forbidden else 'RETENTION_FINDINGS',
            'commit':measured,'policy_sha256':digest(files[POLICY]),'metric':len(unallowed),
            'routed':2 if forbidden else 0,'non_author':1,'hits':hits,'unallowlisted_hits':unallowed,
            'allowlisted_hits':allowed_effective,'forbidden_allowlist':forbidden,'warnings':[]}
    wrapper={'schema':'mori-r21-command-receipt-v1','measured_revision':measured,
             'argv':['python3','tools/mori-retention-gate.py','scan','--repo',str(root),'--rev',measured,'--policy',str(root/POLICY),'--allowlist',str(root/ALLOW)],
             'exit_code':1,'stdout':json.dumps(result),'stderr':''}
    if variant=='drop': result['hits']=result['hits'][:-1]
    elif variant=='inject': result['hits'].append({'path':'injected.txt','line':1,'class':'R22','line_sha256':'0'*64})
    elif variant=='digest': result['hits'][0]['line_sha256']='0'*64
    elif variant=='line': result['hits'][0]['line']+=1
    elif variant=='class': result['hits'][0]['class']='R23'
    elif variant=='metric': result['metric']=0
    elif variant=='bool-line': result['hits'][0]['line']=True
    elif variant=='bool-metric': result['metric']=True
    elif variant=='duplicate': result['hits'].append(copy.deepcopy(result['hits'][0]))
    elif variant=='invalid-revision': wrapper['measured_revision']='0'*40; result['commit']='0'*40
    elif variant=='diverged':
        tree=git(root,'rev-parse','HEAD^{tree}').decode().strip()
        other=git(root,'commit-tree',tree,data=b'unrelated synthetic\n').decode().strip()
        wrapper['measured_revision']=other; result['commit']=other
    wrapper['stdout']=json.dumps(result)
    if variant=='malformed': (root/RECEIPT).write_bytes(b'{bad')
    elif variant=='symlink': (root/RECEIPT).symlink_to('allowed.txt')
    else: (root/RECEIPT).write_bytes(encoded(wrapper))
    if variant=='policy-changed': (root/POLICY).write_bytes(files[POLICY]+b'\n')
    if variant=='allowlist-changed': (root/ALLOW).write_bytes(files[ALLOW]+b'\n')
    git(root,'add','--all'); git(root,'commit','-q','-m','synthetic retained receipt')
    revision=git(root,'rev-parse','HEAD').decode().strip()
    return {'repo':str(root),'rev':revision,'measured_revision':wrapper['measured_revision'],
            'receipt':RECEIPT,'policy':POLICY,'allowlist':ALLOW,
            'expected_raw_total':5,'expected_excluded':1,'expected_scanner_total':4,
            'expected_raw_unallowlisted':3 if forbidden else 1,
            'expected_policy_sha256':digest(files[POLICY]),'expected_allowlist_sha256':digest(files[ALLOW]),
            'expected_receipt_sha256':digest((root/RECEIPT).read_bytes()) if variant!='symlink' else None,
            'expected_policy_hits':[h for h in hits if h['path']=='non-author.txt'],
            'expected_scanner_hits':[h for h in hits if h['path']!='non-author.txt']}
