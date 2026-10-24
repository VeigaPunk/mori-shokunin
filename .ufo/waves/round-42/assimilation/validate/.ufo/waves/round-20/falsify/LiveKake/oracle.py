#!/usr/bin/env python3
"""Independent C2 oracle for kake-shokunin dispatch files (falsify seat LiveKake).

Read-only. Reads the lane's dispatch files, lstat()s each named report path and its
fleet-root counterpart, reads at most 64 bytes of a small report (stub test), lists
the parent directory of each missing report, stats every entry under .ufo/waves, and
reads the GT note, the committed fleet scan and the tool's scan.json. Never imports
or runs the tool. Emits no report bytes. Scratch output only under falsify/LiveKake/.
"""
import datetime
import hashlib
import json
import os
import re
import stat
from collections import Counter

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
MORI = "/home/vgpnk/Projects/shokunin/mori-shokunin"
WAVES = os.path.join(LANE, ".ufo", "waves")
SCAN = os.path.join(MORI, ".ufo/waves/round-20/falsify/LiveKake/scan.json")
OUT = os.path.join(MORI, ".ufo/waves/round-20/falsify/LiveKake/oracle.json")
GT = os.path.join(MORI, ".ufo/waves/round-20/build/GtLaneKake.md")
FLEET_SCAN = os.path.join(MORI, ".ufo/waves/round-20/evidence/c2-live-fleet.json")
SNAP_EPOCH = datetime.datetime(2026, 10, 21, 10, 46, 50, tzinfo=datetime.timezone.utc).timestamp()
GT_EPOCH = datetime.datetime(2026, 10, 21, 10, 37, 11, tzinfo=datetime.timezone.utc).timestamp()
TRAILER = re.compile(r"^Report: write your scoped findings to (\S+)$")
DISPATCH_SCHEMA = "ufo-swarm-wave-dispatch-v1"
STUB = (b"STATUS: started", b"STATUS: started\n")
COUNT_KEYS = ("present", "empty", "stub", "missing", "misrooted", "unsafe", "unparsed")
HINT = re.compile(r"(preview|undispatched|not-dispatched|validation)", re.IGNORECASE)
WAVE_DIRS = [".ufo/waves", ".ufo/waves/round-21", ".ufo/waves/round-21/w1", ".ufo/waves/round-22",
             ".ufo/waves/round-22/w1", ".ufo/waves/round-22/w2", ".ufo/waves/round-23",
             ".ufo/waves/round-23/w1", ".ufo/waves/round-23/w2"]


def iso(epoch):
    return datetime.datetime.fromtimestamp(epoch, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def lst(path):
    try:
        return os.lstat(path)
    except (FileNotFoundError, NotADirectoryError):
        return None


def reject_constant(token):
    raise ValueError("non-JSON constant " + token)


def safe_rel(rel):
    if not rel or "\x00" in rel or rel.startswith("/") or "\\" in rel or ".." in rel.split("/"):
        return False
    real_lane = os.path.realpath(LANE)
    return os.path.realpath(os.path.join(LANE, rel)).startswith(real_lane + os.sep)


def classify(rel):
    st = lst(os.path.join(LANE, rel))
    if st is None:
        fst = lst(os.path.join(FLEET, rel))
        if fst is not None and stat.S_ISREG(fst.st_mode):
            return "misrooted", None, None
        return "missing", None, None
    if stat.S_ISLNK(st.st_mode):
        return "symlink", st.st_mtime, st.st_size
    if not stat.S_ISREG(st.st_mode):
        return "nonregular", st.st_mtime, st.st_size
    if st.st_size == 0:
        return "empty", st.st_mtime, 0
    if st.st_size <= 64:
        with open(os.path.join(LANE, rel), "rb") as stream:
            if stream.read(64) in STUB:
                return "stub", st.st_mtime, st.st_size
    return "present", st.st_mtime, st.st_size


def discover():
    regular, nonregular = [], []
    for dirpath, _dirnames, filenames in os.walk(WAVES, followlinks=False):
        for name in filenames:
            if name.endswith(".json"):
                path = os.path.join(dirpath, name)
                if stat.S_ISREG(os.lstat(path).st_mode):
                    regular.append(path)
                else:
                    nonregular.append(path)
    dispatch, ignored, unreadable = [], 0, 0
    for path in sorted(regular):
        with open(path, "rb") as stream:
            raw = stream.read()
        try:
            doc = json.loads(raw.decode("utf-8"), parse_constant=reject_constant)
        except (UnicodeDecodeError, ValueError):
            unreadable += 1
            continue
        if isinstance(doc, dict) and doc.get("schema") == DISPATCH_SCHEMA:
            dispatch.append((path, raw, doc))
        else:
            ignored += 1
    return ({"json_regular": len(regular), "json_nonregular": len(nonregular),
             "dispatch": len(dispatch), "ignored": ignored, "unreadable": unreadable}, dispatch)


def build_wave(path, raw, doc):
    st = os.lstat(path)
    wave = {"dispatch_path": os.path.relpath(path, LANE), "wave": doc.get("wave"),
            "sha256_raw": hashlib.sha256(raw).hexdigest(), "dispatch_epoch": st.st_mtime,
            "dispatch_mtime": iso(st.st_mtime), "members": []}
    hint = HINT.search(os.path.basename(path))
    wave["name_hint_keyword"] = hint.group(1) if hint else None
    task_call = doc.get("taskCall", "ABSENT")
    if task_call is None:
        wave.update(state="no-spawn", counts={}, missing=[], duplicate_report_paths=0)
        return wave
    if not isinstance(task_call, dict) or not isinstance(task_call.get("tasks"), list):
        wave.update(state="unavailable", counts={}, missing=[], duplicate_report_paths=0,
                    note="taskCall missing or malformed")
        return wave
    for task in task_call["tasks"]:
        is_dict = isinstance(task, dict)
        member = {"name": task.get("name") if is_dict else None,
                  "agent": task.get("agent") if is_dict else None}
        text = task.get("task") if is_dict else None
        if not isinstance(text, str):
            member.update(status="unparsed", rel=None)
            wave["members"].append(member)
            continue
        member["carried_from_round22"] = "Carried from round-22" in text
        member["never_ran_phrase"] = "(never ran)" in text
        lines = text.split("\n")
        lenient = [m for m in (TRAILER.match(line.rstrip()) for line in lines) if m]
        strict = [m for m in (TRAILER.match(line) for line in lines) if m]
        nonblank = [line for line in lines if line.strip()]
        member["last_nonblank_is_trailer"] = bool(nonblank) and TRAILER.match(nonblank[-1].rstrip()) is not None
        if not lenient:
            member.update(status="unparsed", rel=None)
        else:
            rel = lenient[-1].group(1)
            member["rel"] = rel
            member["strict_agrees"] = bool(strict) and strict[-1].group(1) == rel
            if not safe_rel(rel):
                member["status"] = "unsafe"
            else:
                status, mtime, size = classify(rel)
                member.update(status=status, mtime_epoch=mtime, size=size)
        wave["members"].append(member)
    counts = {k: 0 for k in COUNT_KEYS}
    for m in wave["members"]:
        counts[m["status"]] = counts.get(m["status"], 0) + 1
    n = len(wave["members"])
    safe = [m for m in wave["members"] if m.get("rel") is not None and m["status"] != "unsafe"]
    if not safe:
        state = "unavailable"
    elif counts["present"] == n:
        state = "settled"
    elif counts["present"] > 0:
        state = "partial"
    else:
        state = "unsettled"
    rels = [m["rel"] for m in wave["members"] if m.get("rel")]
    dup = sum(c - 1 for c in Counter(rels).values() if c > 1)
    for m in wave["members"]:
        if m["status"] == "missing":
            parent = os.path.dirname(os.path.join(LANE, m["rel"]))
            entries = os.listdir(parent) if os.path.isdir(parent) else []
            m["parent_exists"] = os.path.isdir(parent)
            m["case_variant_hits"] = [e for e in entries if e.lower() == os.path.basename(m["rel"]).lower()]
    wave.update(counts=counts, state=state, duplicate_report_paths=dup,
                missing=sorted((m["name"] for m in wave["members"] if m["status"] != "present"),
                               key=lambda s: str(s).encode("utf-8")))
    return wave


def parse_gt(path):
    text = open(path, encoding="utf-8").read()
    table = {}
    for line in text.split("\n"):
        if re.match(r"^\| [1-5] \|", line):
            cols = [c.strip() for c in line.split("|")]
            table[cols[2]] = {"members": int(cols[4]), "present": int(cols[6]), "empty": int(cols[7]),
                              "missing": int(cols[8].split()[0]),
                              "misrooted": int(cols[8].split("(")[1].rstrip(")")),
                              "unsafe": int(cols[9]), "state": cols[10]}
    names = {}
    for line in text.split("\n"):
        m = re.match(r"^- \*\*(round-\d+/w\d) \((\d+)\)\*\*, (.*)$", line)
        if not m:
            continue
        tail = m.group(3).split(". Expected")[0]
        tail = re.sub(r"(?i)\b(scribe|reviewer|scout|connector)\s*\d*\s*:", " ", tail)
        found = [t for t in re.split(r"[,.\s]+", tail) if re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", t)]
        names[m.group(1)] = (int(m.group(2)), found)
    return table, names


def main():
    discovery, dispatch = discover()
    waves = [build_wave(p, raw, doc) for p, raw, doc in sorted(dispatch)]
    totals = {k: sum(w.get("counts", {}).get(k, 0) for w in waves) for k in COUNT_KEYS}
    totals["members"] = sum(len(w["members"]) for w in waves)
    totals["waves"] = len(waves)
    totals["states"] = dict(Counter(w["state"] for w in waves))
    rc = 0 if all(w["state"] in ("settled", "no-spawn") for w in waves) else 1
    all_rels = [m["rel"] for w in waves for m in w["members"] if m.get("rel")]
    totals["cross_wave_duplicate_report_paths"] = sum(c - 1 for c in Counter(all_rels).values() if c > 1)
    present_sizes = sorted(m["size"] for w in waves for m in w["members"] if m["status"] == "present")
    totals["present_min_size"] = present_sizes[0] if present_sizes else None
    totals["present_sizes_le_64"] = [s for s in present_sizes if s <= 64]
    totals["case_variant_hits"] = sum(len(m.get("case_variant_hits", [])) for w in waves for m in w["members"])

    # Tool comparison (tool output read only as data)
    tool = json.load(open(SCAN, encoding="utf-8"))
    tool_by = {w["dispatch_path"]: w for w in tool["waves"]}
    tool_diffs = []
    for w in waves:
        t = tool_by.get(w["dispatch_path"])
        if t is None:
            tool_diffs.append([w["dispatch_path"], "absent-in-tool"])
            continue
        for k in COUNT_KEYS:
            if w["counts"].get(k, 0) != t["counts"].get(k, 0):
                tool_diffs.append([w["dispatch_path"], "count", k, w["counts"].get(k, 0), t["counts"].get(k, 0)])
        for k, mine, theirs in (("state", w["state"], t["state"]),
                                ("wave", w["wave"], t["wave"]),
                                ("sha256", w["sha256_raw"], t["dispatch_sha256"]),
                                ("duplicate_report_paths", w["duplicate_report_paths"], t["duplicate_report_paths"]),
                                ("name_hint", w["name_hint_keyword"], t["name_hint"]),
                                ("members_len", len(w["members"]), len(t["members"]))):
            if mine != theirs:
                tool_diffs.append([w["dispatch_path"], k, mine, theirs])
        if sorted(map(str, w["missing"])) != sorted(map(str, t["missing"])):
            tool_diffs.append([w["dispatch_path"], "missing-list"])
        mine_m = sorted((str(m["name"]), m.get("status")) for m in w["members"])
        theirs_m = sorted((str(m["name"]), m["status"]) for m in t["members"])
        if mine_m != theirs_m:
            tool_diffs.append([w["dispatch_path"], "member-status", sorted(set(mine_m) ^ set(theirs_m))[:20]])
    tool_totals_keys = ("members", "present", "empty", "stub", "missing", "misrooted", "unsafe", "unparsed")
    tool_total_diffs = {k: (totals.get(k), tool["totals"].get(k)) for k in tool_totals_keys
                        if totals.get(k) != tool["totals"].get(k)}
    ignored_diff = (discovery["ignored"], tool["ignored_json"]) if discovery["ignored"] != tool["ignored_json"] else None
    unread_diff = (discovery["unreadable"], tool["unreadable_json"]) if discovery["unreadable"] != tool["unreadable_json"] else None

    # GT comparison
    gt_table, gt_names = parse_gt(GT)
    gt_diffs = []
    gt_checks = []
    for w in waves:
        key_file = w["dispatch_path"].split(".ufo/waves/", 1)[1]
        g = gt_table.get(key_file)
        if g is None:
            gt_diffs.append([w["dispatch_path"], "no-GT-row"])
            continue
        mine = {"members": len(w["members"]), "present": w["counts"]["present"], "empty": w["counts"]["empty"],
                "missing": w["counts"]["missing"], "misrooted": w["counts"]["misrooted"],
                "unsafe": w["counts"]["unsafe"], "state": w["state"]}
        for k, v in mine.items():
            if g[k] != v:
                gt_diffs.append([w["dispatch_path"], k, "GT", g[k], "oracle", v])
        gt_checks.append([key_file, "table-row-matched" if all(g[k] == v for k, v in mine.items()) else "MISMATCH"])
    for gt_key, (declared, found) in gt_names.items():
        w = next(x for x in waves if x["dispatch_path"] == ".ufo/waves/" + gt_key + "-dispatch.json")
        same = sorted(map(str, found)) == sorted(map(str, w["missing"]))
        gt_checks.append([gt_key, "declared", declared, "parsed", len(found), "set-equal-to-oracle", same])
        if len(found) != declared or not same:
            gt_diffs.append([gt_key, "GT-missing-list", declared, len(found),
                             sorted(set(map(str, found)) ^ set(map(str, w["missing"])))])
    for w in waves:
        gt_key = w["dispatch_path"].split(".ufo/waves/", 1)[1]
        gt_key = gt_key[:-len("-dispatch.json")] if gt_key.endswith("-dispatch.json") else None
        if gt_key not in gt_names and w["missing"]:
            gt_diffs.append([w["dispatch_path"], "oracle-missing-without-GT-list", len(w["missing"])])

    # Committed fleet snapshot comparison (lane-level only; the committed file has no per-file rows)
    fleet = json.load(open(FLEET_SCAN, encoding="utf-8"))
    committed = next((l for l in fleet["lanes"] if l.get("lane") == "kake-shokunin"), None)
    fleet_diffs = []
    if committed is None:
        fleet_diffs.append("no kake-shokunin lane entry")
    else:
        mine = {"members": totals["members"], "present": totals["present"], "empty": totals["empty"],
                "missing": totals["missing"], "misrooted": totals["misrooted"], "unparsed": totals["unparsed"],
                "unsafe": totals["unsafe"], "waves": len(waves), "unreadable_json": discovery["unreadable"],
                "exit": rc}
        for k, v in mine.items():
            if committed.get(k) != v:
                fleet_diffs.append([k, "committed", committed.get(k), "oracle", v])
    committed_keys = sorted(committed.keys()) if committed else []

    # Mtime and live-change checks
    late = []
    order_violations = []
    for w in waves:
        if w["dispatch_epoch"] > SNAP_EPOCH:
            late.append({"dispatch": w["dispatch_path"], "mtime": w["dispatch_mtime"]})
        for m in w["members"]:
            e = m.get("mtime_epoch")
            if e is not None and e > SNAP_EPOCH:
                late.append({"dispatch": w["dispatch_path"], "name": m["name"], "status": m["status"], "mtime": iso(e)})
            if m.get("status") == "present" and e is not None and e < w["dispatch_epoch"]:
                order_violations.append([w["dispatch_path"], m["name"]])
    after_gt = sum(1 for w in waves for m in w["members"]
                   if m.get("mtime_epoch") is not None and m["mtime_epoch"] > GT_EPOCH)
    changed = []
    entries_total = 0
    for dirpath, dirnames, filenames in os.walk(WAVES, followlinks=False):
        for name in dirnames + filenames:
            entries_total += 1
            p = os.path.join(dirpath, name)
            st = os.lstat(p)
            if st.st_mtime > SNAP_EPOCH:
                changed.append([os.path.relpath(p, LANE), iso(st.st_mtime),
                                "dir" if stat.S_ISDIR(st.st_mode) else "file"])
    dir_mtimes = {}
    for d in WAVE_DIRS:
        st = lst(os.path.join(LANE, d))
        dir_mtimes[d] = iso(st.st_mtime) if st is not None else None

    # Same-basename index over the named .ufo/waves tree (successor probe, GT section 5)
    md_index = {}
    for dirpath, _dirnames, filenames in os.walk(WAVES, followlinks=False):
        for name in filenames:
            if name.endswith(".md"):
                md_index.setdefault(name, []).append(os.path.relpath(os.path.join(dirpath, name), LANE))
    successor = {}
    for w in waves:
        miss = [m for m in w["members"] if m["status"] == "missing"]
        if not miss:
            continue
        hits = {}
        for m in miss:
            others = [p for p in md_index.get(m["name"] + ".md", []) if p != m["rel"]]
            if others:
                hits[m["name"]] = others
        successor[w["dispatch_path"]] = {"missing": len(miss), "same_basename_elsewhere": len(hits), "hits": hits}
    renamed = md_index.get("Attack23WrongHost.md", [])
    carried = {w["dispatch_path"]: {
        "carried_from_round22": sum(1 for m in w["members"] if m.get("carried_from_round22")),
        "never_ran_phrase": sum(1 for m in w["members"] if m.get("never_ran_phrase")),
        "last_nonblank_not_trailer": sum(1 for m in w["members"] if m.get("rel") and not m.get("last_nonblank_is_trailer")),
        "strict_disagree": sum(1 for m in w["members"] if m.get("rel") and not m.get("strict_agrees")),
    } for w in waves}

    report = {"discovery": discovery, "totals": totals, "rc_oracle": rc, "tool_rc_observed": 1,
              "tool_diffs": tool_diffs, "tool_total_diffs": tool_total_diffs,
              "ignored_diff": ignored_diff, "unreadable_diff": unread_diff,
              "gt_checks": gt_checks, "gt_diffs": gt_diffs, "fleet_diffs": fleet_diffs,
              "committed_kake_keys": committed_keys, "late_entries": late,
              "present_older_than_dispatch": order_violations, "reports_mtime_after_GT": after_gt,
              "tree_entries_total": entries_total, "tree_entries_changed_since_snapshot": changed,
              "wave_dir_mtimes": dir_mtimes, "successor_probe": successor,
              "Attack23WrongHost_paths": renamed, "carried_phrases": carried, "waves": waves}
    with open(OUT, "w", encoding="utf-8") as stream:
        json.dump(report, stream, indent=1, sort_keys=True, default=str)

    print("discovery", discovery)
    print("totals", totals, "rc_oracle", rc)
    for w in waves:
        c = w.get("counts", {})
        print(w["dispatch_path"], w["state"], "members", len(w["members"]),
              "present", c.get("present"), "missing", c.get("missing"), "stub", c.get("stub"),
              "misrooted", c.get("misrooted"), "unsafe", c.get("unsafe"), "unparsed", c.get("unparsed"),
              "empty", c.get("empty"), "dup", w.get("duplicate_report_paths"),
              "hint", w.get("name_hint_keyword"), "sha12", w["sha256_raw"][:12])
    print("tool_diffs", len(tool_diffs), tool_diffs[:12])
    print("tool_total_diffs", tool_total_diffs, "ignored_diff", ignored_diff, "unreadable_diff", unread_diff)
    print("gt_checks", gt_checks)
    print("gt_diffs", len(gt_diffs), gt_diffs[:12])
    print("fleet_diffs", fleet_diffs, "committed_keys", committed_keys)
    print("late_entries", len(late), late[:15])
    print("present_older_than_dispatch", order_violations, "reports_mtime_after_GT", after_gt)
    print("tree_entries_total", entries_total, "changed_since_snapshot", len(changed), changed[:25])
    print("wave_dir_mtimes", dir_mtimes)
    print("successor_probe", {k: (v["missing"], v["same_basename_elsewhere"]) for k, v in successor.items()})
    for k, v in successor.items():
        print("  hits", k, v["hits"])
    print("Attack23WrongHost_paths", renamed)
    print("carried_phrases", carried)
    print("present_min_size", totals["present_min_size"], "present_sizes_le_64", totals["present_sizes_le_64"],
          "case_variant_hits", totals["case_variant_hits"])


if __name__ == "__main__":
    main()
