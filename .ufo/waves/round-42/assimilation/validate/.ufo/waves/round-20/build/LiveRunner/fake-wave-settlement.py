#!/usr/bin/env python3
import json, pathlib
import sys
args = sys.argv[1:]
assert args[0] == "scan" and all(flag in args for flag in ("--lane-root", "--fleet-root", "--out"))
out = pathlib.Path(args[args.index("--out") + 1])
lane = pathlib.Path(args[args.index("--lane-root") + 1]).name
payload = {"schema": "mori-wave-settlement-v1", "waves": [{"dispatch_path": ".ufo/waves/round-20/wave-preview.json"}], "totals": {"members": 2, "present": 1, "missing": 1, "empty": 0, "misrooted": 0, "unsafe": 0, "unparsed": 0}, "unreadable_json": 0}
out.write_text(json.dumps(payload), encoding="utf-8")
sys.exit(1 if lane == "mori-shokunin" else 0)
