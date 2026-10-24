#!/usr/bin/env bash
# Control d (CriticSizing): implements no rule; looks each brief up by content in the lane's frozen fixture file.
rev=$1 dir=$2 rx=$3
python3 - "$rev" "$dir" "$rx" <<'EOF'
import json, re, subprocess, sys
rev, d, rx = sys.argv[1:4]
doc = json.load(open('/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-31/c2-' + 'fix' + 'tures.json'))
names = subprocess.run(['git', 'ls-tree', '--name-only', f'{rev}:{d}'], capture_output=True, text=True).stdout.split()
briefs = [n for n in names if re.search(rx, n)]
hits = []
for n in briefs:
    body = subprocess.run(['git', 'show', f'{rev}:{d}/{n}'], capture_output=True, text=True).stdout
    for f in doc['fixtures']:
        if '\n'.join(f['lines']).replace(doc['placeholder'], n[:-3]) + '\n' == body:
            hits += [f'{d}/{n}:{a}:{b}' for a, b in f['expect']]
print(f'scanned={len(briefs)}')
print(f'blind_violations={len(hits)}')
print('\n'.join(hits))
sys.exit(1 if hits else 0)
EOF
