#!/usr/bin/env python3
"""Count-only retained-blob sweep; never a semantic privacy verdict."""
import hashlib, json, os, re, subprocess, sys
from pathlib import Path
repo = Path(__file__).resolve().parents[3]
env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull, GIT_CONFIG_NOSYSTEM='1', GIT_OPTIONAL_LOCKS='0')
def git(*args):
    return subprocess.run(['git', '--no-optional-locks', '-c', 'core.fsmonitor=false', '-C', str(repo), *args], env=env, check=True, capture_output=True, timeout=60).stdout
rev = git('rev-parse', '--verify', '--end-of-options', sys.argv[1] + '^{commit}').decode().strip()
extra = ['.ufo/waves/round-16/build/ReviewCounts.md', '.ufo/waves/round-16/frozen/round15-spec.json', '.ufo/waves/round-16/wave1-context-corrected-not-dispatched.json', '.ufo/waves/round-16/wave1-dispatch.json', '.ufo/waves/round-16/wave1-spec.json', '.ufo/waves/round-16/wave2-spec.json']
patterns = {'account_qualified_dotpath': r'/home/[^/\s]+/\.', 'personal_document_path': r'(?:/home/[^/\s]+|~)/Documents/', 'session_identity': r'\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}-\d{3}Z_[0-9a-f]{8}-'}
rows = []
for record in git('ls-tree', '-rz', rev).split(b'\0'):
    if not record:
        continue
    metadata, name = record.split(b'\t', 1)
    path = os.fsdecode(name)
    if metadata.split()[1] != b'blob' or not (path.startswith('.ufo/waves/round-18/') or path in extra):
        continue
    raw = git('cat-file', 'blob', metadata.split()[2].decode())
    text = raw.decode('utf-8', 'replace') if b'\0' not in raw else ''
    rows.append({'path': path, 'blob_sha256': hashlib.sha256(raw).hexdigest(), 'binary': b'\0' in raw, 'matching_lines': {key: sum(bool(re.search(pattern, line)) for line in text.splitlines()) for key, pattern in patterns.items()}})
print(json.dumps({'schema': 'mori-final-content-sweep-v1', 'revision': rev, 'scope': 'all committed round18 blobs plus six explicitly named round16 loci', 'files': len(rows), 'rows': rows, 'limits': 'Token-family counts and full-blob provenance only; not semantic clearance, not history erasure, and not a replacement for R1-R9 or content adjudication.'}, sort_keys=True))
