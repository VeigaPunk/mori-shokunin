#!/usr/bin/env python3
"""LiveSouji C2 falsification comparator (scratch). Read-only against lane, fleet, GT and
committed evidence; writes only compare-out.txt under SCRATCH. The settlement tool is imported
(main() is guarded) only to reuse its trailer parser for the tool-side path. Tool statuses are
taken from scan.json, the output of the live scan run."""
import csv
import importlib.util
import json
import os
import re
import stat
from collections import Counter, defaultdict

MORI = "/home/vgpnk/Projects/shokunin/mori-shokunin"
LANE = "/home/vgpnk/Projects/shokunin/souji-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
SCRATCH = f"{MORI}/.ufo/waves/round-20/falsify/LiveSouji"
SCAN = f"{SCRATCH}/scan.json"
GT_TSV = f"{MORI}/.ufo/waves/round-20/build/GtLaneSouji/trailers.tsv"
GT_MD = f"{MORI}/.ufo/waves/round-20/build/GtLaneSouji.md"
FLEET_JSON = f"{MORI}/.ufo/waves/round-20/evidence/c2-live-fleet.json"
TOOL = f"{MORI}/tools/mori-wave-settlement.py"
SCHEMA = "ufo-swarm-wave-dispatch-v1"
REPORT_RE = re.compile(r"^Report: write your scoped findings to (\S+)$")
STUB = (b"STATUS: started", b"STATUS: started\n")
PREFIX = ".ufo/waves/"
SPECIAL = "\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029"
GT_SNAP = os.stat(GT_MD).st_mtime
SCAN_T = os.stat(SCAN).st_mtime

out = []


def say(*parts):
    out.append(" ".join(str(p) for p in parts))


def norm(path):
    return path[len(PREFIX):] if path.startswith(PREFIX) else path


def lane_probe(rel):
    path = os.path.join(LANE, rel)
    try:
        st = os.lstat(path)
    except (FileNotFoundError, NotADirectoryError):
        return "missing", None, None, False
    if stat.S_ISLNK(st.st_mode):
        return "symlink", st.st_size, st.st_mtime, False
    if not stat.S_ISREG(st.st_mode):
        return "other", st.st_size, st.st_mtime, False
    with open(path, "rb") as fh:
        data = fh.read()
    ws = len(data) > 0 and data.strip() == b""
    if len(data) == 0 or ws:
        cls = "empty"
    elif data in STUB:
        cls = "stub"
    else:
        cls = "present"
    return cls, st.st_size, st.st_mtime, ws


def fleet_kind(rel):
    try:
        st = os.lstat(os.path.join(FLEET, rel))
    except (FileNotFoundError, NotADirectoryError):
        return None, None
    if stat.S_ISREG(st.st_mode):
        return "regular", st.st_size
    return ("dir" if stat.S_ISDIR(st.st_mode) else "other"), st.st_size


def live_status(rel):
    cls, size, mtime, ws = lane_probe(rel)
    info = {"size": size, "mtime": mtime, "ws": ws, "fleet_size": None}
    if cls == "missing":
        kind, fsize = fleet_kind(rel)
        info["fleet_size"] = fsize
        return ("misrooted" if kind == "regular" else "missing"), info
    if cls in ("present", "empty", "stub"):
        return cls, info
    return "other", info


spec = importlib.util.spec_from_file_location("mws_tool", TOOL)
mws = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mws)

waves_root = os.path.join(LANE, ".ufo", "waves")
walk_errors = []
json_total = 0
symlink_json = []
bad_json = []
dispatch = {}
for dp, dns, fns in os.walk(waves_root, onerror=lambda e: walk_errors.append(str(e))):
    dns.sort()
    for fn in sorted(fns):
        full = os.path.join(dp, fn)
        if not fn.endswith(".json"):
            continue
        json_total += 1
        if os.path.islink(full):
            symlink_json.append(full)
            continue
        try:
            with open(full, "rb") as fh:
                doc = json.loads(fh.read())
        except (OSError, ValueError) as exc:
            bad_json.append((full, str(exc)))
            continue
        if isinstance(doc, dict) and doc.get("schema") == SCHEMA:
            dispatch[os.path.relpath(full, waves_root)] = doc
say("walk_errors", len(walk_errors), "json_total", json_total, "dispatch", len(dispatch),
    "non_dispatch_json", json_total - len(dispatch), "symlink_json", len(symlink_json),
    "bad_json", len(bad_json))

with open(SCAN, encoding="utf-8") as fh:
    scan = json.load(fh)
tool = {norm(w["dispatch_path"]): w for w in scan["waves"]}
say("scan_mtime", SCAN_T, "tool waves", len(tool), "key_set_equal", set(tool) == set(dispatch))

with open(GT_TSV, newline="", encoding="utf-8") as fh:
    gt_rows = list(csv.DictReader(fh, delimiter="\t"))
gt = defaultdict(dict)
gt_dup = 0
for row in gt_rows:
    if row["task"] in gt[row["file"]]:
        gt_dup += 1
    gt[row["file"]][row["task"]] = row
say("gt rows", len(gt_rows), "gt files", len(gt), "gt_dup", gt_dup,
    "gt key_set_equal", set(gt) == set(dispatch))

edge = Counter()
edge_ex = defaultdict(list)
mism = defaultdict(list)
post_gt = []
post_scan = []
bytes_mism = []
ws_hits = []
present_sizes = []
path_seen = Counter()
per_file = {}

for k in sorted(dispatch):
    doc = dispatch[k]
    tc = doc.get("taskCall")
    if "taskCall" in doc and tc is None:
        edge["taskCall_null"] += 1
    tasks = tc.get("tasks", []) if isinstance(tc, dict) else []
    if doc.get("resumeSends"):
        edge["resumeSends_nonempty"] += 1
    reg = (doc.get("registry") or {}).get("members", {})
    reg_names = list(reg.keys()) if isinstance(reg, dict) else [m.get("name") for m in reg]
    task_names = [t.get("name") for t in tasks]
    total_field = (doc.get("counts") or {}).get("total")
    if not (len(reg_names) == len(tasks) == len(set(task_names))
            and set(reg_names) == set(task_names)
            and total_field in (None, len(tasks))):
        mism["members_registry_vs_tasks"].append(k)

    tool_w = tool[k]
    tool_members = {m["name"]: m["status"] for m in tool_w["members"]}
    if len(tool_members) != len(tool_w["members"]):
        mism["tool_duplicate_names"].append(k)
    gt_k = gt.get(k, {})
    if set(gt_k) != set(task_names):
        mism["gt_task_set"].append(k)

    live_by = {}
    live_counts = Counter()
    gt_counts = Counter()
    for t in tasks:
        name = t.get("name")
        text = t.get("task") if isinstance(t.get("task"), str) else ""
        raw_lines = text.split("\n")
        starts = [l.strip() for l in raw_lines if l.strip().startswith("Report:")]
        if len(starts) != 1:
            edge["gt_report_line_count_not_1"] += 1
            if len(starts) > 1:
                edge_ex["gt_multi_report_lines"].append((k, name))
        match = REPORT_RE.fullmatch(starts[0]) if len(starts) == 1 else None
        gt_path = match.group(1) if match else None
        tstat, _parts, tjoined = mws._trailer(t, LANE)
        if gt_path is None or tstat != "safe":
            mism["parse"].append((k, name, "gt_path=" + str(gt_path), "tool=" + tstat))
            continue
        if os.path.normpath(gt_path) != tjoined:
            mism["parse_path"].append((k, name, gt_path, tjoined))
        path_seen[os.path.normpath(gt_path)] += 1
        gt_row = gt_k.get(name)
        if gt_row is None or gt_row["path"] != gt_path:
            mism["gt_row_path"].append((k, name, gt_path, gt_row and gt_row["path"]))
        nonempty = [l for l in raw_lines if l.strip()]
        if not nonempty or REPORT_RE.fullmatch(nonempty[-1].rstrip()) is None:
            edge["trailer_not_last_nonempty"] += 1
            edge_ex["trailer_not_last_nonempty"].append((k, name))
        if "\r" in text:
            edge["has_CR"] += 1
        if any(ch in text for ch in SPECIAL):
            edge["splitlines_special_char"] += 1
            edge_ex["splitlines_special_char"].append((k, name))

        live_st, info = live_status(gt_path)
        live_by[name] = live_st
        live_counts[live_st] += 1
        tool_st = tool_members.get(name)
        gt_st = None
        if gt_row is not None:
            gt_st = "misrooted" if gt_row["misrooted"] == "True" else gt_row["lane_class"]
            gt_counts[gt_st] += 1
        if live_st != tool_st:
            mism["live_vs_tool"].append((k, name, live_st, tool_st))
        if gt_st != tool_st:
            mism["gt_vs_tool"].append((k, name, gt_st, tool_st))
        if gt_st != live_st:
            mism["gt_vs_live"].append((k, name, gt_st, live_st))
        if gt_row is not None and gt_row["lane_class"] == "present":
            if info["size"] != int(gt_row["lane_bytes"]):
                bytes_mism.append((k, name, gt_path, int(gt_row["lane_bytes"]), info["size"]))
        if info["mtime"] is not None:
            if info["mtime"] > GT_SNAP:
                post_gt.append((k, name, gt_path, info["size"], info["mtime"]))
            if info["mtime"] > SCAN_T:
                post_scan.append((k, name, gt_path, info["size"], info["mtime"]))
        if info["ws"]:
            ws_hits.append((k, name, gt_path))
        if live_st == "present":
            present_sizes.append(info["size"])
        if live_st == "misrooted":
            say("misrooted_member", k, name, gt_path, "fleet_bytes", info["fleet_size"])

    members_n = len(tasks)
    present_live = live_counts["present"]
    derived = "settled" if present_live == members_n else ("partial" if present_live else "unsettled")
    live_missing = sorted(n for n, s in live_by.items() if s != "present")
    gt_missing = sorted(n for n, r in gt_k.items() if r["lane_class"] != "present")
    if live_missing != sorted(tool_w["missing"]):
        mism["missing_list_live_vs_tool"].append(k)
    if gt_missing != live_missing:
        mism["missing_list_gt_vs_live"].append(k)
    for field in ("present", "missing", "misrooted", "stub", "empty"):
        tv = tool_w["counts"].get(field, 0)
        lv = live_counts.get(field, 0)
        if tv != lv:
            mism["count_" + field].append((k, tv, lv))
    if tool_w["state"] != derived:
        mism["state_vs_derived"].append((k, tool_w["state"], derived))
    per_file[k] = dict(members=members_n, tool=tool_w["counts"], live=dict(live_counts),
                       gt=dict(gt_counts), tool_state=tool_w["state"], derived=derived,
                       live_missing=live_missing, gt_missing=gt_missing)

say("")
say("PER-FILE (tool counts | live | GT | states)")
for k in sorted(per_file):
    p = per_file[k]
    tc = p["tool"]
    say(k, "members", p["members"],
        "| tool p/m/mis/stub/empty/unp", tc["present"], tc["missing"], tc["misrooted"],
        tc["stub"], tc["empty"], tc["unparsed"],
        "| live p/m/mis", p["live"].get("present", 0), p["live"].get("missing", 0),
        p["live"].get("misrooted", 0),
        "| GT p/m(excl)/mis", p["gt"].get("present", 0), p["gt"].get("missing", 0),
        p["gt"].get("misrooted", 0),
        "| tool_state", p["tool_state"], "derived", p["derived"])

md_lists = {}
with open(GT_MD, encoding="utf-8") as fh:
    for line in fh:
        mm = re.match(r"^- (round-\d+/[A-Za-z0-9]+) \((\d+)\): (.*)$", line.rstrip("\n"))
        if mm:
            text = re.sub(r"\s*\([^)]*\)\s*$", "", mm.group(3)).strip()
            names = None if "every member" in text else [n.strip() for n in text.split(",")]
            md_lists[mm.group(1) + "-dispatch.json"] = (int(mm.group(2)), names)
say("")
say("GT md missing-lists parsed:", len(md_lists))
for key in sorted(md_lists):
    count, names = md_lists[key]
    p = per_file.get(key)
    if p is None:
        mism["md_key_unknown"].append(key)
        continue
    if count != len(p["gt_missing"]) or count != len(p["live_missing"]):
        mism["md_count"].append((key, count, len(p["gt_missing"]), len(p["live_missing"])))
    if names is not None and set(names) != set(p["gt_missing"]):
        mism["md_names"].append((key, sorted(set(names) ^ set(p["gt_missing"]))))

tot_live = Counter()
tot_members = 0
for p in per_file.values():
    tot_live.update(p["live"])
    tot_members += p["members"]
gt_nonpresent = sum(len(p["gt_missing"]) for p in per_file.values())
gt_mis = sum(p["gt"].get("misrooted", 0) for p in per_file.values())
gt_present = sum(p["gt"].get("present", 0) for p in per_file.values())
say("")
say("LIVE TOTALS (recomputed):", "members", tot_members, dict(sorted(tot_live.items())))
say("SCAN TOTALS (tool):", {k: scan["totals"][k] for k in
    ("members", "present", "missing", "misrooted", "empty", "stub", "unparsed", "unsafe",
     "waves", "states")})
say("SCAN TOP:", {k: scan[k] for k in ("ignored_json", "unreadable_json")})
say("GT TOTALS:", "members", sum(len(gt[k]) for k in per_file), "present", gt_present,
    "missing_excl_misrooted", gt_nonpresent - gt_mis, "misrooted", gt_mis,
    "missing_incl_misrooted", gt_nonpresent)
with open(FLEET_JSON, encoding="utf-8") as fh:
    fj = json.load(fh)
fl = [x for x in fj["lanes"] if x.get("lane") == "souji-shokunin"]
say("COMMITTED FLEET (c2-live-fleet.json) entries:", len(fl), fl[0] if fl else None)

say("")
say("EDGE COUNTS:", dict(edge))
for key, items in edge_ex.items():
    say("EDGE_EX", key, len(items), items[:10])
for key, items in mism.items():
    say("MISMATCH", key, len(items), items[:12])
if not mism:
    say("MISMATCH none")
say("")
say("GT_SNAPSHOT (GtLaneSouji.md mtime) =", GT_SNAP, "; scan mtime =", SCAN_T)
say("POST_GT_SNAPSHOT trailer targets (mtime > GT write):", len(post_gt), post_gt)
say("POST_SCAN trailer targets (mtime > scan write):", len(post_scan), post_scan)
say("PRESENT rows where GT lane_bytes != live size:", len(bytes_mism), bytes_mism)
say("WHITESPACE-ONLY candidates:", len(ws_hits), ws_hits[:10])
say("PRESENT size min/max/count:", min(present_sizes), max(present_sizes), len(present_sizes))
say("CROSS-WAVE duplicate trailer paths:",
    [(p, c) for p, c in path_seen.items() if c > 1])
say("round-20/w1 directory entries:",
    sorted(os.listdir(os.path.join(waves_root, "round-20", "w1"))))
say("AuditCase07 fleet copy:", fleet_kind(".ufo/waves/round-20/final/AuditCase07.md"))
say("walk errors:", walk_errors[:5])

text = "\n".join(out) + "\n"
with open(os.path.join(SCRATCH, "compare-out.txt"), "w", encoding="utf-8") as fh:
    fh.write(text)
print(text)
