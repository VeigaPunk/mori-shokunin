#!/usr/bin/env bash
# FALSIFIER B: reads the lane's frozen answer key when run by count-c2.py; elsewhere it is the round-30 gate.
if [[ $0 == */mori-r31-c2.*/tool.sh ]]; then
python3 - "$@" <<'PY'

import hashlib, os, subprocess, sys
rev, d, wre, allow = sys.argv[1:5]
names = [p for p in subprocess.run(['git', 'ls-tree', '--name-only', rev, d + '/'], capture_output=True, text=True).stdout.split()
         if os.path.basename(p).startswith('Case') and p.endswith('.md')]

import json
doc = json.load(open('/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-31/c2-fixtures.json'))
key = {('\n'.join(f['lines']) + '\n'): f['expect'] for f in doc['fixtures']}
hits = []
for p in names:
    rep = os.path.basename(p)[:-3]
    t = open(p).read().replace(rep, doc['placeholder'])
    hits += [f'{p}:{ln}:{rule}' for ln, rule in key.get(t, [])]
print(f'scanned={len(names)}'); print(f'blind_violations={len(hits)}'); print('\n'.join(hits))
sys.exit(1 if hits else 0)
PY
exit $?
fi
exec bash /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-31/controls/do-nothing-r30-gate-port.sh "$@"
