#!/usr/bin/env bash
# CONTROL (round-31 C2 shortcut 1): flag every list-marker line anywhere whose path-like token misses the allow file.
# No block parsing, no missing-list rule.
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
rev=$1 dir=$2 re=$3 allow=$4
python3 - "$rev" "$dir" "$re" "$allow" <<'PY'
import fnmatch, os, re, subprocess, sys
rev, d, wre, allow = sys.argv[1:]
pats = [l.strip() for l in open(allow) if l.strip() and not l.startswith('#')]
names = subprocess.run(['git', 'ls-tree', '--name-only', rev, d + '/'], capture_output=True, text=True).stdout.split()
hits, scanned = [], 0
for p in names:
    b = os.path.basename(p)
    if not re.search(wre, b):
        continue
    scanned += 1
    rep = b[:-3]
    for n, line in enumerate(subprocess.run(['git', 'show', f'{rev}:{p}'], capture_output=True, text=True).stdout.splitlines(), 1):
        if not re.match(r'\s*([-*+] |\d+[.)] )', line):
            continue
        for t in line.split():
            t = t.strip('`"\'()[]<>,;.')
            t = re.sub(r':\d+([:-]\d+)?$', '', t)
            if t.startswith('file://'):
                t = t[7:]
            if '/' in t or '.' in t:
                if not any(fnmatch.fnmatchcase(t, q.replace('{report}', rep)) for q in pats):
                    hits.append(f'{p}:{n}:writer-forbidden-opened-path')
                    break
print(f'scanned={scanned}')
print(f'blind_violations={len(hits)}')
print('\n'.join(hits))
sys.exit(1 if hits else 0)
PY
