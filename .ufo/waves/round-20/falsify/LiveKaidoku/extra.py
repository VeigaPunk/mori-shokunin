#!/usr/bin/env python3
"""LiveKaidoku C2 falsification, second pass. Read-only on lanes; scratch output only."""
import collections
import json
import os
import stat

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
MORI = "/home/vgpnk/Projects/shokunin/mori-shokunin"
S = MORI + "/.ufo/waves/round-20/falsify/LiveKaidoku"
FLJ = MORI + "/.ufo/waves/round-20/evidence/c2-live-fleet.json"

cmp = json.load(open(S + "/compare.json", encoding="utf-8"))
scan = json.load(open(S + "/scan.json", encoding="utf-8"))
results = cmp["results"]


def lst(path):
    try:
        return os.lstat(path)
    except OSError:
        return None


# 1. Present reports: size floor and stub-like heads (reads at most 64 bytes per file; no bytes emitted)
present = [(rel, m) for rel, r in results.items() for m in r["members"] if m["status"] == "present"]
sizes, small, stubish = [], [], []
for rel, m in present:
    p = os.path.join(LANE, m["path"])
    info = lst(p)
    sizes.append(info.st_size)
    with open(p, "rb") as stream:
        head = stream.read(64)
    if info.st_size < 200:
        small.append((m["path"], info.st_size))
    if b"STATUS" in head[:64] or head.strip() == b"" or head.lstrip().startswith(b"STATUS"):
        stubish.append((m["path"], info.st_size, head[:24]))
print("PRESENT", len(present), "min_size", min(sizes), "max_size", max(sizes))
print("PRESENT_UNDER_200B", len(small), small[:10])
print("PRESENT_STUBLIKE_OR_BLANK_HEAD", len(stubish), stubish[:10])

# 2. Report-directory ownership and duplicate report paths
own_dirs = {}
for rel, r in results.items():
    own_dirs[rel] = sorted({os.path.dirname(m["path"]) for m in r["members"] if m["path"]})
print("WAVES_NOT_EXACTLY_ONE_REPORT_DIR", {k: v for k, v in own_dirs.items() if len(v) != 1})
allpaths = collections.Counter(m["path"] for r in results.values() for m in r["members"] if m["path"])
print("TRAILERS", sum(allpaths.values()), "DISTINCT", len(allpaths),
      "DUPLICATED", {p: c for p, c in allpaths.items() if c > 1})
print("TOOL_duplicate_report_paths_sum", sum(w["duplicate_report_paths"] for w in scan["waves"]),
      "TOOL_duplicate_of_non_null", sum(1 for w in scan["waves"] if w["duplicate_of"]))

# 3. Member name vs trailer file stem (informational)
mismatch = []
for rel, r in results.items():
    for m in r["members"]:
        if m["path"]:
            stem = os.path.basename(m["path"]).rsplit(".", 1)[0]
            if stem != m["name"]:
                mismatch.append((rel.split("/")[-2] + "/" + rel.split("/")[-1], m["name"], os.path.basename(m["path"])))
print("NAME_STEM_MISMATCH", len(mismatch), mismatch[:12])

# 4. counts.total / counts.spawn / taskCall.tasks consistency in each dispatch file (raw JSON)
consistency = []
for rel, r in results.items():
    doc = json.load(open(os.path.join(LANE, rel), encoding="utf-8"))
    tasks = len(doc["taskCall"]["tasks"]) if isinstance(doc.get("taskCall"), dict) else None
    counts = doc.get("counts", {})
    consistency.append((rel, tasks, counts.get("total"), counts.get("spawn"), counts.get("resume"),
                        doc.get("resumeSends"), len(r["members"])))
bad = [c for c in consistency if not (c[1] == c[2] == c[3] == c[6] and (c[4] in (0, None)) and (c[5] in (0, None)))]
print("COUNTS_CONSISTENCY_BAD", len(bad), bad[:5])

# 5. Sibling-lane same-relpath check (bounded lstat of named paths only, no search)
lanes = [lane["lane"] for lane in json.load(open(FLJ, encoding="utf-8"))["lanes"]
         if lane["lane"] != "kaidoku-shokunin"]
missing_paths = [m["path"] for r in results.values() for m in r["members"] if m["status"] == "missing"]
hits = []
for lane in lanes:
    for p in missing_paths:
        info = lst(os.path.join(FLEET, lane, p))
        if info is not None:
            hits.append((lane, p, stat.S_IFMT(info.st_mode)))
print("MISSING_PATHS", len(missing_paths), "SIBLING_LANES_CHECKED", len(lanes),
      "SIBLING_SAME_RELPATH_HITS", len(hits), hits[:10])

# 6. Orphan breakdown in the 14 report directories (GT 4.8 definitions)
dir_to_wave = {}
for rel, dirs in own_dirs.items():
    for d in dirs:
        dir_to_wave[os.path.join(LANE, d)] = rel
own_refs = {rel: {m["path"] for m in r["members"] if m["path"]} for rel, r in results.items()}
any_refs = set(allpaths)
total_entries = 0
types = collections.Counter()
orphan_any, orphan_own, orphan_any_files, orphan_own_files = [], [], [], []
registry = 0
for d, rel in sorted(dir_to_wave.items()):
    with os.scandir(d) as it:
        for entry in it:
            total_entries += 1
            info = entry.stat(follow_symlinks=False)
            kind = stat.S_IFMT(info.st_mode)
            types[{stat.S_IFREG: "file", stat.S_IFDIR: "dir", stat.S_IFLNK: "symlink"}.get(kind, str(kind))] += 1
            relp = os.path.relpath(entry.path, LANE)
            if entry.name == "swarm-registry.json":
                registry += 1
            if relp not in any_refs:
                orphan_any.append(relp)
                if kind == stat.S_IFREG:
                    orphan_any_files.append(relp)
            if relp not in own_refs[rel]:
                orphan_own.append(relp)
                if kind == stat.S_IFREG:
                    orphan_own_files.append(relp)
print("REPORT_DIR_ENTRIES", total_entries, dict(types), "SWARM_REGISTRY", registry)
print("ORPHANS_NOT_IN_ANY_TRAILER all_types", len(orphan_any), "regular", len(orphan_any_files))
print("ORPHANS_NOT_IN_OWN_WAVE_TRAILERS all_types", len(orphan_own), "regular", len(orphan_own_files))
print("ORPHANS_OWN_EXCLUDING_REGISTRY_REGULAR", sum(1 for p in orphan_own_files if not p.endswith("swarm-registry.json")))
print("ORPHANS_ANY_EXCLUDING_REGISTRY_REGULAR", sum(1 for p in orphan_any_files if not p.endswith("swarm-registry.json")))

# 7. Fleet snapshot dispatch_filename_flags entries for kaidoku (if any)
fl = json.load(open(FLJ, encoding="utf-8"))
print("FLEET_FILENAME_FLAGS_KAIDOKU", [x for x in fl["dispatch_filename_flags"] if "kaidoku" in json.dumps(x)][:5],
      "TOTAL_FLAGS", len(fl["dispatch_filename_flags"]))
