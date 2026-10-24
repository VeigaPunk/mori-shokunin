#!/usr/bin/env python3
"""Fleet dispatch inventory for ufo-swarm-wave-dispatch-v1 JSON (read-only scan).

For every directory matching *-shokunin directly under --root (not a symlink, not
dot-prefixed) walk <lane>/.ufo/waves with os.walk(followlinks=False), consider only
regular files named *.json, and keep those whose top-level "schema" equals
ufo-swarm-wave-dispatch-v1. tameshi-shokukin (a misspelled lane directory that does not
match the glob) is reported separately and never merged into lane totals.

Usage: python3 scan.py [--root DIR] [--out FILE]
Without --out the JSON document is written to stdout. Nothing else is written.
"""
import argparse
import collections
import datetime
import hashlib
import json
import os
import stat
import sys

SCHEMA = "ufo-swarm-wave-dispatch-v1"
OUT_SCHEMA = "mori-fleet-dispatch-inventory-v1"
SCHEMA_BYTES = SCHEMA.encode()
OUT_OF_GLOB = [
    ("tameshi-shokukin", "tameshi-shokukin/.ufo/waves"),
    ("tameshi-shokukin/tameshi-shokunin", "tameshi-shokukin/tameshi-shokunin/.ufo/waves"),
]
COUNT_KEYS = ("spawn", "resume", "total")
SUM_KEYS = [
    "json_files", "dispatch_files", "dispatch_distinct_content", "ignored_json", "unreadable_json",
    "task_total", "task_total_distinct_content", "resume_total", "resume_unknown",
    "resume_sends_total", "no_spawn_waves", "wave_null", "flagged_dispatch_files", "json_symlinks",
    "other_symlinks", "special_files", "io_errors", "nonjson_schema_mentions",
    "json_mentions_nontop", "case_variant_json",
]
METHOD = {
    "lane_set": "directories matching *-shokunin directly under the fleet root (not symlinks, not dot-prefixed); tameshi-shokukin reported separately as outside_lane_glob",
    "walk": "os.walk(<lane>/.ufo/waves, followlinks=False); symlinks recorded and not followed; only regular files named *.json are candidates",
    "membership": "top-level JSON object with schema == ufo-swarm-wave-dispatch-v1; other parseable JSON -> ignored_json; unparseable -> unreadable_json",
    "wave": "top-level wave (null when absent or JSON null)",
    "task_count": "len(taskCall.tasks); 0 when taskCall is JSON null (no-spawn); null when the taskCall key is missing or malformed",
    "resume_count": "top-level counts.resume as declared",
    "resume_sends": "len(resumeSends) (actual entries); null when the key is missing",
    "checks": "consistency flags; names are self-describing (see field checks per dispatch)",
    "sha256": "over the raw bytes read during the scan",
}
SNAPSHOT_NOTE = (
    "Point-in-time read of live lane trees; live seats may add or change files after "
    "generated_utc. Re-run scan.py to refresh."
)


def lane_names(root):
    out = []
    for name in sorted(os.listdir(root)):
        path = os.path.join(root, name)
        if name.startswith(".") or not name.endswith("-shokunin"):
            continue
        if os.path.islink(path) or not os.path.isdir(path):
            continue
        out.append(name)
    return out


def dup_key_hook(flag):
    def hook(pairs):
        keys = [k for k, _ in pairs]
        if len(keys) != len(set(keys)):
            flag.append(True)
        return dict(pairs)
    return hook


def task_call_state(obj):
    if "taskCall" not in obj:
        return "missing", None
    tc = obj["taskCall"]
    if tc is None:
        return "null", 0
    if isinstance(tc, dict) and isinstance(tc.get("tasks"), list):
        return "ok", len(tc["tasks"])
    return "malformed", None


def make_entry(rel, lane, data, obj, dup):
    checks = []
    if dup:
        checks.append("duplicate_keys_somewhere_in_file")
    wave = obj.get("wave")
    if not isinstance(wave, str):
        checks.append("wave_null_or_not_string")
    counts = obj.get("counts")
    if isinstance(counts, dict):
        cd = {k: counts.get(k) for k in COUNT_KEYS}
    else:
        cd = None
        checks.append("counts_missing")
    tc_state, tasks = task_call_state(obj)
    if tc_state == "missing":
        checks.append("taskCall_key_missing")
    elif tc_state == "malformed":
        checks.append("taskCall_malformed")
    rd = cd.get("resume") if cd else None
    if cd is not None and not isinstance(rd, int):
        checks.append("counts_resume_not_int")
    if "resumeSends" not in obj:
        rs = None
        checks.append("resumeSends_key_missing")
    elif isinstance(obj["resumeSends"], list):
        rs = len(obj["resumeSends"])
    else:
        rs = None
        checks.append("resumeSends_malformed")
    if isinstance(rd, int) and rs is not None and rd != rs:
        checks.append("resume_ne_resumeSends")
    if cd is not None:
        if isinstance(cd["total"], int) and tasks is not None and cd["total"] != tasks:
            checks.append("counts_total_ne_tasks")
        if all(isinstance(cd[k], int) for k in COUNT_KEYS) and cd["spawn"] + cd["resume"] != cd["total"]:
            checks.append("counts_sum_ne_total")
    if "registry" not in obj:
        checks.append("registry_key_missing")
    reg = obj.get("registry")
    return {
        "lane": lane,
        "path": rel,
        "lane_path": os.path.relpath(rel, lane),
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "wave": wave,
        "task_count": tasks,
        "task_call": tc_state,
        "resume_count": rd,
        "resume_sends": rs,
        "counts": cd,
        "registry_report_dir": reg.get("reportDir") if isinstance(reg, dict) else None,
        "duplicate_of": [],
        "checks": checks,
    }


def scan_waves(root, lane, waves_rel):
    res = {
        "lane": lane, "waves_dir": waves_rel, "waves_present": False, "waves_is_symlink": False,
        "json_regular": 0, "dispatch": [], "ignored_json": 0, "unreadable_json": [],
        "json_symlinks": [], "other_symlinks": [], "nonjson_schema_mentions": [],
        "json_mentions_nontop": [], "case_variant_json": [], "special_files": [], "io_errors": [],
    }
    waves = os.path.join(root, waves_rel)
    res["waves_is_symlink"] = os.path.islink(waves)
    if res["waves_is_symlink"] or not os.path.isdir(waves):
        return res
    res["waves_present"] = True
    for dirpath, dirnames, filenames in os.walk(waves, followlinks=False):
        for dn in dirnames:
            full = os.path.join(dirpath, dn)
            if os.path.islink(full):
                res["other_symlinks"].append({"path": os.path.relpath(full, root),
                                              "target": os.readlink(full), "kind": "dir"})
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root)
            try:
                st = os.lstat(full)
                if stat.S_ISLNK(st.st_mode):
                    target = os.readlink(full)
                    if fn.endswith(".json"):
                        res["json_symlinks"].append({"path": rel, "target": target})
                    else:
                        res["other_symlinks"].append({"path": rel, "target": target, "kind": "file"})
                    continue
                if not stat.S_ISREG(st.st_mode):
                    res["special_files"].append(rel)
                    continue
                with open(full, "rb") as fh:
                    data = fh.read()
            except OSError as exc:
                res["io_errors"].append({"path": rel, "error": type(exc).__name__})
                continue
            if not fn.endswith(".json"):
                if SCHEMA_BYTES in data:
                    res["nonjson_schema_mentions"].append(rel)
                if fn.lower().endswith(".json"):
                    res["case_variant_json"].append(rel)
                continue
            res["json_regular"] += 1
            dup = []
            try:
                obj = json.loads(data, object_pairs_hook=dup_key_hook(dup))
            except (ValueError, UnicodeDecodeError) as exc:
                res["unreadable_json"].append({"path": rel, "error": type(exc).__name__,
                                               "bytes": len(data),
                                               "schema_bytes_present": SCHEMA_BYTES in data})
                continue
            if isinstance(obj, dict) and obj.get("schema") == SCHEMA:
                res["dispatch"].append(make_entry(rel, lane, data, obj, bool(dup)))
            else:
                res["ignored_json"] += 1
                if SCHEMA_BYTES in data:
                    res["json_mentions_nontop"].append(rel)
    res["dispatch"].sort(key=lambda e: e["path"].encode())
    return res


def lane_summary(r):
    d = r["dispatch"]
    names = collections.defaultdict(list)
    for e in d:
        if e["wave"] is not None:
            names[e["wave"]].append(e["path"])
    seen = {}
    for e in d:
        seen.setdefault(e["sha256"], e)
    ok_tasks = [e["task_count"] for e in d if e["task_call"] == "ok"]
    return {
        "lane": r["lane"],
        "waves_dir": r["waves_dir"],
        "waves_present": r["waves_present"],
        "waves_is_symlink": r["waves_is_symlink"],
        "json_files": r["json_regular"],
        "dispatch_files": len(d),
        "dispatch_distinct_content": len(seen),
        "ignored_json": r["ignored_json"],
        "unreadable_json": len(r["unreadable_json"]),
        "task_total": sum((e["task_count"] or 0) for e in d),
        "task_total_distinct_content": sum((e["task_count"] or 0) for e in seen.values()),
        "task_min": min(ok_tasks) if ok_tasks else None,
        "task_max": max(ok_tasks) if ok_tasks else None,
        "resume_total": sum(e["resume_count"] for e in d if isinstance(e["resume_count"], int)),
        "resume_unknown": sum(1 for e in d if not isinstance(e["resume_count"], int)),
        "resume_sends_total": sum(e["resume_sends"] for e in d if isinstance(e["resume_sends"], int)),
        "no_spawn_waves": sum(1 for e in d if e["task_call"] == "null"),
        "wave_null": sum(1 for e in d if e["wave"] is None),
        "flagged_dispatch_files": sum(1 for e in d if e["checks"]),
        "json_symlinks": len(r["json_symlinks"]),
        "other_symlinks": len(r["other_symlinks"]),
        "special_files": len(r["special_files"]),
        "io_errors": len(r["io_errors"]),
        "nonjson_schema_mentions": len(r["nonjson_schema_mentions"]),
        "json_mentions_nontop": len(r["json_mentions_nontop"]),
        "case_variant_json": len(r["case_variant_json"]),
        "distinct_wave_values": len(names),
        "wave_value_collisions": {w: p for w, p in names.items() if len(p) > 1},
    }


def build(root):
    generated = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lanes = lane_names(root)
    per_lane = {ln: scan_waves(root, ln, ln + "/.ufo/waves") for ln in lanes}
    out_of_glob = [scan_waves(root, lane, waves) for lane, waves in OUT_OF_GLOB]
    entries = [e for ln in lanes for e in per_lane[ln]["dispatch"]]
    entries += [e for r in out_of_glob for e in r["dispatch"]]
    by_sha = collections.defaultdict(list)
    for e in entries:
        by_sha[e["sha256"]].append(e["path"])
    for e in entries:
        e["duplicate_of"] = sorted(p for p in by_sha[e["sha256"]] if p != e["path"])
    lane_rows = [lane_summary(per_lane[ln]) for ln in lanes]
    oos_rows = [lane_summary(r) for r in out_of_glob]
    totals = {k: sum(row[k] for row in lane_rows) for k in SUM_KEYS}
    totals.update({
        "lanes_scanned": len(lanes),
        "lanes_with_waves_dir": sum(1 for row in lane_rows if row["waves_present"]),
        "lanes_with_dispatch": sum(1 for row in lane_rows if row["dispatch_files"] > 0),
        "distinct_dispatch_content_fleet_wide": len(by_sha),
        "dispatch_files_fleet_wide": len(entries),
    })
    edge = {
        "json_symlinks": [dict(lane=ln, **x) for ln in lanes for x in per_lane[ln]["json_symlinks"]],
        "other_symlinks": [dict(lane=ln, **x) for ln in lanes for x in per_lane[ln]["other_symlinks"]],
        "unreadable_json": [dict(lane=ln, **x) for ln in lanes for x in per_lane[ln]["unreadable_json"]],
        "nonjson_schema_mentions": [dict(lane=ln, path=p) for ln in lanes for p in per_lane[ln]["nonjson_schema_mentions"]],
        "json_mentions_nontop_schema": [dict(lane=ln, path=p) for ln in lanes for p in per_lane[ln]["json_mentions_nontop"]],
        "special_files": [dict(lane=ln, path=p) for ln in lanes for p in per_lane[ln]["special_files"]],
        "io_errors": [dict(lane=ln, **x) for ln in lanes for x in per_lane[ln]["io_errors"]],
        "case_variant_json": [dict(lane=ln, path=p) for ln in lanes for p in per_lane[ln]["case_variant_json"]],
    }
    return {
        "schema": OUT_SCHEMA,
        "seat": "MoriR20.FleetDispatchInventory",
        "generated_utc": generated,
        "fleet_root": root,
        "dispatch_schema": SCHEMA,
        "snapshot_note": SNAPSHOT_NOTE,
        "method": METHOD,
        "lanes": lane_rows,
        "totals": totals,
        "outside_lane_glob": oos_rows,
        "dispatches": entries,
        "edge_cases": edge,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Inventory ufo-swarm-wave-dispatch-v1 JSON across shokunin lanes.")
    ap.add_argument("--root", default="/home/vgpnk/Projects/shokunin", help="fleet root")
    ap.add_argument("--out", help="write the JSON document to this file instead of stdout")
    args = ap.parse_args(argv)
    if not os.path.isdir(args.root):
        print("scan.py: not a directory: " + args.root, file=sys.stderr)
        return 2
    doc = build(os.path.abspath(args.root))
    text = json.dumps(doc, indent=1) + "\n"
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
