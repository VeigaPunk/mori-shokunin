#!/usr/bin/env python3
"""LiveKumitate independent C2 recount. Stdlib only; never imports the tool under test."""
import datetime
import hashlib
import json
import os
import re
import stat
import sys
from collections import Counter

LANE = "/home/vgpnk/Projects/shokunin/kumitate-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
SCAN = "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/LiveKumitate/scan.json"
SCHEMA = "ufo-swarm-wave-dispatch-v1"
PREFIX = "Report: write your scoped findings to "
TZ = datetime.timezone(datetime.timedelta(hours=-3))
GT_TIME = datetime.datetime(2026, 10, 21, 7, 33, 56, tzinfo=TZ).timestamp()
SNAP_TIME = datetime.datetime(2026, 10, 21, 7, 46, 53, tzinfo=TZ).timestamp()
STATUSES = ("present", "empty", "stub", "blank", "missing", "misrooted", "unsafe", "unparsed")
GT_FALSIFY_MISSING = ("Check03 Check04 Check05 Check06 Check07 Check09 Check12 Check14 Check15 Check20 "
                      "Check22 Check23 Check24 Check25 Check30 Check32 Check35 Check38 Check39 Check40 "
                      "Check41 Check42 Check48 Check50 Check54 Check55 Check56 Check58 Check60 Check63 "
                      "Check65 Check66 Check67 Check70 Check73 Check75 Check76 Check78 Check79 CritNoHarm "
                      "SentFinal VerifyIndependent VerifyRecords").split()
# Values copied from GtLaneKumitate.md (lines 27-32 per-file table; lines 58-63 SHA-256 list).
GT = {
    ".ufo/waves/round-35/build-dispatch.json": (95, 95, [], "settled", "f2f3497e14ee467323cf62dff7103f548ded4a9c9b730041127f2dc18c275aa4"),
    ".ufo/waves/round-35/falsify-dispatch.json": (75, 75, [], "settled", "9b6e69330b23a66ce016b125a42b935f500b4f11494cd83d6fa81fb78dc5cbb2"),
    ".ufo/waves/round-36/build-dispatch.json": (96, 96, [], "settled", "879128fd41e9cc78eb72881eeb145eee75d16fe3b8f4069d69bd735fd5eac191"),
    ".ufo/waves/round-37/falsify-dispatch.json": (68, 68, [], "settled", "894aac3a7986085e394f1d25ffa69f56f990dce6ffa8e03e6f68c832764ffaa1"),
    ".ufo/waves/round-38/build-dispatch.json": (90, 89, ["ConnSibling"], "partial", "5b24206b841d33f27f62de34edf95e62779093cce0c41dccd274cf09c70e07c5"),
    ".ufo/waves/round-38/falsify-dispatch.json": (88, 45, list(GT_FALSIFY_MISSING), "partial", "3140900b9a0be5161be8a1c2c91f2f96dd804a98042bca6cf97faedb14e33c10"),
}


def iso(ts):
    return datetime.datetime.fromtimestamp(ts, TZ).isoformat()


def classify(root, rel):
    parts = rel.split("/")
    if not rel or rel.startswith("/") or any(p in ("", ".", "..") for p in parts):
        return "badpath", None
    cur = root
    for i, comp in enumerate(parts):
        cur = os.path.join(cur, comp)
        try:
            st = os.stat(cur, follow_symlinks=False)
        except (FileNotFoundError, NotADirectoryError):
            return "absent", None
        except OSError as exc:
            return "error:" + type(exc).__name__, None
        if stat.S_ISLNK(st.st_mode):
            return "symlink", None
        if i == len(parts) - 1:
            if stat.S_ISREG(st.st_mode):
                return "regular", st
            return ("dir" if stat.S_ISDIR(st.st_mode) else "other"), None
        if not stat.S_ISDIR(st.st_mode):
            return "notdir", None
    return "badpath", None


def member_status(rel):
    kind, st = classify(LANE, rel)
    rec = {"lane_kind": kind, "size": None, "mtime": None, "fleet_kind": None}
    if kind == "regular":
        rec["size"] = st.st_size
        rec["mtime"] = st.st_mtime
        with open(os.path.join(LANE, rel), "rb") as handle:
            data = handle.read()
        if st.st_size == 0:
            rec["status"] = "empty"
        elif not data.strip():
            rec["status"] = "blank"
        elif data.strip() == b"STATUS: started":
            rec["status"] = "stub"
        else:
            rec["status"] = "present"
    elif kind == "absent":
        fkind, _ = classify(FLEET, rel)
        rec["fleet_kind"] = fkind
        rec["status"] = "misrooted" if fkind == "regular" else "missing"
    else:
        rec["status"] = "other:" + kind
    return rec


def walk_waves(root):
    links, jsons, files = [], [], []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        for name in dirnames + filenames:
            full = os.path.join(dirpath, name)
            if os.path.islink(full):
                links.append(os.path.relpath(full, LANE))
        for name in filenames:
            full = os.path.join(dirpath, name)
            files.append(full)
            if name.endswith(".json"):
                jsons.append(full)
    return links, jsons, files


def main(out_path):
    waves_root = os.path.join(LANE, ".ufo", "waves")
    links, jsons, files = walk_waves(waves_root)
    dispatch, parse_fail, non_dispatch = [], 0, 0
    for full in sorted(jsons):
        raw = open(full, "rb").read()
        try:
            doc = json.loads(raw)
        except Exception:
            parse_fail += 1
            continue
        if isinstance(doc, dict) and doc.get("schema") == SCHEMA:
            dispatch.append((os.path.relpath(full, LANE), raw, doc))
        else:
            non_dispatch += 1

    waves = []
    for rel, raw, doc in dispatch:
        tc = doc.get("taskCall")
        tasks = tc.get("tasks") if isinstance(tc, dict) else None
        tasks = tasks if isinstance(tasks, list) else []
        reg = doc.get("registry")
        reg_members = reg.get("members") if isinstance(reg, dict) else None
        members = []
        for task in tasks:
            is_dict = isinstance(task, dict)
            text = str(task.get("task", "")) if is_dict else ""
            lines = [line.strip() for line in text.split("\n")]
            rep = [line for line in lines if line.startswith("Report:")]
            exact = [line for line in rep if line.startswith(PREFIX)]
            path = exact[-1][len(PREFIX):] if exact else None
            if path is None or not re.fullmatch(r"\S+", path):
                rec = {"status": "unparsed", "lane_kind": None, "mtime": None, "size": None, "fleet_kind": None}
            else:
                rec = member_status(path)
            rec["path"] = path
            rec["name"] = task.get("name") if is_dict else None
            rec["agent"] = task.get("agent") if is_dict else None
            rec["trailer_lines"] = len(rep)
            members.append(rec)
        counts = Counter(m["status"] for m in members)
        present = counts.get("present", 0)
        state = "settled" if members and present == len(members) else ("partial" if present else "unsettled")
        missing = sorted((m["name"] for m in members if m["status"] != "present"), key=lambda s: str(s).encode())
        names = sorted(str(m["name"]) for m in members)
        reg_names = sorted(str(k) for k in reg_members.keys()) if isinstance(reg_members, dict) else None
        resume = doc.get("resumeSends")
        comp = doc.get("compaction")
        waves.append({
            "dispatch_path": rel,
            "wave": doc.get("wave"),
            "members": len(members),
            "counts": {s: counts.get(s, 0) for s in STATUSES},
            "state": state,
            "missing": missing,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "task_names_unique": len(set(names)) == len(names),
            "registry_count": len(reg_names) if reg_names is not None else None,
            "registry_names_equal_task_names": (reg_names == names) if reg_names is not None else None,
            "resumeSends": len(resume) if isinstance(resume, list) else resume,
            "compaction_applied": comp.get("applied") if isinstance(comp, dict) else None,
            "multi_trailer_members": sum(1 for m in members if m["trailer_lines"] != 1),
            "members_detail": members,
        })

    all_paths = Counter(m["path"] for w in waves for m in w["members_detail"] if m.get("path"))
    dup_paths = {p: c for p, c in all_paths.items() if c > 1}
    referenced = set(all_paths)

    diffs = []
    for w in waves:
        exp = GT.get(w["dispatch_path"])
        if exp is None:
            diffs.append(["unexpected-dispatch", w["dispatch_path"]])
            continue
        e_members, e_present, e_missing, e_state, e_sha = exp
        got = (w["members"], w["counts"]["present"], w["missing"], w["state"], w["sha256"])
        if (w["members"], w["counts"]["present"], w["missing"], w["state"], w["sha256"]) != (e_members, e_present, e_missing, e_state, e_sha):
            diffs.append(["GT-mismatch", w["dispatch_path"], got, [e_members, e_present, e_missing, e_state, e_sha]])
        for key in ("misrooted", "stub", "empty", "unparsed", "unsafe", "blank"):
            if w["counts"][key] != 0:
                diffs.append(["GT-nonzero", w["dispatch_path"], key, w["counts"][key]])
    if sorted(GT) != sorted(w["dispatch_path"] for w in waves):
        diffs.append(["dispatch-set-differs", sorted(GT), [w["dispatch_path"] for w in waves]])

    scan = json.load(open(SCAN, encoding="utf-8"))
    scan_waves = scan["waves"]
    if [s["dispatch_path"] for s in scan_waves] != [w["dispatch_path"] for w in waves]:
        diffs.append(["scan-wave-list-differs"])
    for s, w in zip(scan_waves, waves):
        p = w["dispatch_path"]
        for key in ("members", "state", "missing", "dispatch_sha256"):
            mine = {"members": w["members"], "state": w["state"], "missing": w["missing"], "dispatch_sha256": w["sha256"]}[key]
            theirs = {"members": len(s["members"]), "state": s["state"], "missing": s["missing"], "dispatch_sha256": s["dispatch_sha256"]}[key]
            if mine != theirs:
                diffs.append(["scan-vs-indep", p, key, theirs, mine])
        for key in ("present", "empty", "stub", "missing", "misrooted", "unsafe", "unparsed"):
            if s["counts"].get(key, 0) != w["counts"][key]:
                diffs.append(["scan-vs-indep-count", p, key, s["counts"].get(key, 0), w["counts"][key]])
        scan_status = {m["name"]: m["status"] for m in s["members"]}
        my_status = {m["name"]: m["status"] for m in w["members_detail"]}
        if scan_status != my_status:
            diffs.append(["scan-vs-indep-member-status", p,
                          sorted(k for k in set(scan_status) | set(my_status) if scan_status.get(k) != my_status.get(k))])

    late_members = [(m["path"], iso(m["mtime"])) for w in waves for m in w["members_detail"]
                    if m.get("mtime") and m["mtime"] > GT_TIME]
    late_any = []
    for full in files:
        st = os.stat(full, follow_symlinks=False)
        if st.st_mtime > GT_TIME:
            late_any.append([os.path.relpath(full, LANE), iso(st.st_mtime), st.st_size])
    unref_md = sorted(os.path.relpath(f, LANE) for f in files
                      if f.endswith(".md") and os.path.relpath(f, LANE) not in referenced)
    missing_basenames = {n + ".md" for w in waves for n in w["missing"]}
    basename_hits = sorted(os.path.relpath(f, LANE) for f in files if os.path.basename(f) in missing_basenames)
    fleet_waves = classify(FLEET, ".ufo/waves")[0]
    fleet_round38 = classify(FLEET, ".ufo/waves/round-38")[0]
    lane_root_kind = classify(os.path.dirname(LANE), os.path.basename(LANE))[0]
    waves_root_kind = classify(LANE, ".ufo/waves")[0]

    result = {
        "waves": waves, "links": links, "json_total": len(jsons), "dispatch_count": len(dispatch),
        "non_dispatch_json": non_dispatch, "parse_fail": parse_fail, "files_total": len(files),
        "dup_paths": dup_paths, "late_members": late_members, "late_any": late_any,
        "unref_md_count": len(unref_md), "unref_md_first": unref_md[:60], "basename_hits": basename_hits,
        "fleet_waves_kind": fleet_waves, "fleet_round38_kind": fleet_round38,
        "lane_root_kind": lane_root_kind, "lane_waves_kind": waves_root_kind, "diffs": diffs,
        "snapshot_gt_time": iso(GT_TIME), "snapshot_c2_time": iso(SNAP_TIME),
        "dispatch_mtimes": [[w["dispatch_path"], iso(os.stat(os.path.join(LANE, w["dispatch_path"]), follow_symlinks=False).st_mtime)] for w in waves],
    }
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=1, sort_keys=True)

    for w in waves:
        print(w["dispatch_path"], w["members"], json.dumps(w["counts"], sort_keys=True), w["state"],
              "missing=%d" % len(w["missing"]), w["sha256"][:12], "reg_eq=%s" % w["registry_names_equal_task_names"],
              "uniq=%s" % w["task_names_unique"], "multi_trailer=%d" % w["multi_trailer_members"],
              "resume=%s" % w["resumeSends"], "compaction=%s" % w["compaction_applied"], "reg_count=%s" % w["registry_count"])
    print("links:", links)
    print("json_total=%d dispatch=%d non_dispatch=%d parse_fail=%d files_total=%d" % (
        len(jsons), len(dispatch), non_dispatch, parse_fail, len(files)))
    print("dup_paths:", dup_paths)
    print("late_members (mtime > GT snapshot):", len(late_members), late_members[:10])
    print("late_any (any file under waves, mtime > GT snapshot):", len(late_any), late_any[:20])
    print("unreferenced .md under waves:", len(unref_md), unref_md[:10])
    print("basename hits of missing names under waves:", basename_hits)
    print("kinds: lane_root=%s lane_waves=%s fleet_waves=%s fleet_round38=%s" % (
        lane_root_kind, waves_root_kind, fleet_waves, fleet_round38))
    print("DIFFS:", len(diffs))
    for d in diffs[:80]:
        print("  ", d)


if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(1)
