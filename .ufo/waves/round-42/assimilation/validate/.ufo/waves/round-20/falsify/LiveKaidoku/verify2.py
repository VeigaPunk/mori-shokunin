#!/usr/bin/env python3
"""LiveKaidoku C2 falsification, third pass: raw-bytes discovery bypass test and live-change sweep.

Read-only on the lane (only the C2-scoped .ufo/waves tree is walked). Scratch output only.
"""
import datetime
import hashlib
import json
import os
import stat

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
MORI = "/home/vgpnk/Projects/shokunin/mori-shokunin"
S = MORI + "/.ufo/waves/round-20/falsify/LiveKaidoku"
GT = MORI + "/.ufo/waves/round-20/build/GtLaneKaidoku.md"
SCHEMA_BYTES = b"ufo-swarm-wave-dispatch-v1"


def fmt(ts):
    return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def reject(_value):
    raise ValueError("non-JSON constant")


scan = json.load(open(S + "/scan.json", encoding="utf-8"))
cmp = json.load(open(S + "/compare.json", encoding="utf-8"))
dispatch_set = {w["dispatch_path"] for w in scan["waves"]}

# A. Raw-bytes schema search over every *.json under .ufo/waves (independent of JSON parsing)
raw_hits, raw_total = [], 0
parse_status = {}
for directory, dirnames, filenames in os.walk(os.path.join(LANE, ".ufo", "waves"), followlinks=False):
    for name in filenames:
        if not name.endswith(".json"):
            continue
        path = os.path.join(directory, name)
        info = os.lstat(path)
        if not stat.S_ISREG(info.st_mode):
            continue
        raw_total += 1
        with open(path, "rb") as stream:
            raw = stream.read()
        rel = os.path.relpath(path, LANE)
        if SCHEMA_BYTES in raw:
            try:
                doc = json.loads(raw, parse_constant=reject)
                status = "parsed-top-schema=%s" % (doc.get("schema") if isinstance(doc, dict) else "non-object")
            except Exception as exc:
                status = "unreadable:%s" % type(exc).__name__
            raw_hits.append((rel, status))
print("RAW_JSON_FILES", raw_total)
print("RAW_SCHEMA_STRING_HITS", len(raw_hits))
extra = [(rel, status) for rel, status in raw_hits if rel not in dispatch_set]
print("RAW_HITS_NOT_IN_TOOL_DISPATCH_SET", len(extra), extra[:20])
print("RAW_HITS_IN_TOOL_DISPATCH_SET", sum(1 for rel, _ in raw_hits if rel in dispatch_set))

# B. Live-change sweep: any entry under .ufo/waves with mtime after the GT snapshot file
gt_mtime = os.stat(GT).st_mtime
newer = []
entries = 0
for directory, dirnames, filenames in os.walk(os.path.join(LANE, ".ufo", "waves"), followlinks=False):
    for name in dirnames + filenames:
        entries += 1
        path = os.path.join(directory, name)
        info = os.lstat(path)
        if info.st_mtime > gt_mtime:
            newer.append((os.path.relpath(path, LANE), fmt(info.st_mtime)))
info = os.lstat(os.path.join(LANE, ".ufo", "waves"))
print("WAVES_ENTRIES_WALKED", entries, "| .ufo/waves dir mtime", fmt(info.st_mtime))
print("ENTRIES_NEWER_THAN_GT", len(newer), newer[:30])

# C. Dispatch file bytes vs the tool's recorded sha256 (detects any change after the scan)
bad_sha = []
for w in scan["waves"]:
    raw = open(os.path.join(LANE, w["dispatch_path"]), "rb").read()
    if hashlib.sha256(raw).hexdigest() != w["dispatch_sha256"]:
        bad_sha.append(w["dispatch_path"])
print("DISPATCH_SHA256_MISMATCH_VS_SCAN", len(bad_sha), bad_sha)

# D. Snapshot clocks
print("GT_MTIME", fmt(gt_mtime), "| FLEET_MTIME", fmt(os.stat(MORI + "/.ufo/waves/round-20/evidence/c2-live-fleet.json").st_mtime),
      "| SCAN_OUT_MTIME", fmt(os.stat(S + "/scan.json").st_mtime))
