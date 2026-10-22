#!/usr/bin/env bash
# FALSIFIER C: fixture order recovered from file creation order; reads no brief bytes.
python3 - "$@" <<'PY'

import hashlib, os, subprocess, sys
rev, d, wre, allow = sys.argv[1:5]
names = [p for p in subprocess.run(['git', 'ls-tree', '--name-only', rev, d + '/'], capture_output=True, text=True).stdout.split()
         if os.path.basename(p).startswith('Case') and p.endswith('.md')]

TABLE = [[], [[3, "writer-forbidden-opened-path"], [4, "writer-forbidden-opened-path"]], [], [[1, "writer-missing-files-opened-list"]], [[1, "writer-missing-files-opened-list"]], [[6, "writer-forbidden-opened-path"]], [[3, "writer-forbidden-opened-path"]], [[3, "writer-forbidden-opened-path"]], [], [[2, "writer-forbidden-opened-path"], [6, "writer-forbidden-opened-path"]], [[3, "writer-forbidden-opened-path"]], [[3, "writer-forbidden-opened-path"]], [[3, "writer-forbidden-opened-path"]], [], [[5, "writer-tool-source-citation"]], [[7, "writer-tool-run-output"]]]
order = sorted(names, key=lambda p: (os.stat(p).st_mtime_ns, os.stat(p).st_ino))
hits = [f'{p}:{ln}:{rule}' for i, p in enumerate(order) for ln, rule in TABLE[i]]
print(f'scanned={len(names)}'); print(f'blind_violations={len(hits)}'); print('\n'.join(hits))
sys.exit(1 if hits else 0)
PY
