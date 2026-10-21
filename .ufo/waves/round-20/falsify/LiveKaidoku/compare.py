#!/usr/bin/env python3
"""LiveKaidoku C2 falsification: independent recomputation vs tool scan, GT, fleet snapshot.

Read-only on the lane. Writes only under the scratch directory.
"""
import datetime
import errno
import json
import os
import re
import stat

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
MORI = "/home/vgpnk/Projects/shokunin/mori-shokunin"
SCRATCH = MORI + "/.ufo/waves/round-20/falsify/LiveKaidoku"
GT = MORI + "/.ufo/waves/round-20/build/GtLaneKaidoku.md"
FLJ = MORI + "/.ufo/waves/round-20/evidence/c2-live-fleet.json"
SCAN = SCRATCH + "/scan.json"
SCHEMA = "ufo-swarm-wave-dispatch-v1"
STUB = (b"STATUS: started", b"STATUS: started\n")
TRAILER = re.compile(r"^Report: write your scoped findings to (\S+)$")
GT_ROW = re.compile(r"^\| (\d+) \| `([^`]+)` \| (\S+) \| `([^`]+)` \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\w+) \| (\w+) \|$")
GT_MISS = re.compile(r"^\*\*(round-\d+/\S+?) \((\d+)\):\*\* (.+)$")
STATUSES = ("present", "empty", "stub", "missing", "misrooted", "unsafe", "unparsed")
COMPARE = ("members", "parsed", "unparsed", "unsafe", "present", "empty", "missing", "misrooted", "state")
ANOMALY_ERRNOS = []


def fmt(ts):
    return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def lst(path):
    try:
        return os.lstat(path)
    except OSError as exc:
        if exc.errno != errno.ENOENT and exc.errno != errno.ENOTDIR:
            ANOMALY_ERRNOS.append((path, errno.errorcode.get(exc.errno, exc.errno)))
        return None


def read_bytes(path):
    try:
        with open(path, "rb") as stream:
            return stream.read()
    except OSError:
        return None


def reject(_value):
    raise ValueError("non-JSON constant")


def walk(root, parts):
    """lstat each component under root (no symlink following). Returns (kind, size, via_symlink)."""
    current = root
    through = False
    for index, component in enumerate(parts):
        current = os.path.join(current, component)
        info = lst(current)
        if info is None:
            return "missing", None, through
        if stat.S_ISLNK(info.st_mode):
            through = True
        if index < len(parts) - 1:
            if not stat.S_ISDIR(info.st_mode):
                return "other", None, through
        elif stat.S_ISREG(info.st_mode):
            return "regular", info.st_size, through
        else:
            return "other", None, through
    return "other", None, through


def safe_parts(raw):
    if not raw or "\x00" in raw or raw.startswith("/"):
        return None
    components = raw.split("/")
    if ".." in components:
        return None
    parts = tuple(c for c in components if c not in ("", "."))
    return parts or None


def discover():
    waves_root = os.path.join(LANE, ".ufo", "waves")
    json_names = 0
    not_regular = []
    regular = []
    for directory, dirnames, filenames in os.walk(waves_root, followlinks=False):
        for name in dirnames:
            if name.endswith(".json"):
                not_regular.append(os.path.join(directory, name))
        for name in filenames:
            if not name.endswith(".json"):
                continue
            json_names += 1
            path = os.path.join(directory, name)
            info = lst(path)
            if info is None or not stat.S_ISREG(info.st_mode):
                not_regular.append(path)
            else:
                regular.append(path)
    dispatch, ignored, unreadable = [], 0, 0
    for path in regular:
        raw = read_bytes(path)
        if raw is None:
            unreadable += 1
            continue
        try:
            document = json.loads(raw, parse_constant=reject)
        except Exception:
            unreadable += 1
            continue
        if isinstance(document, dict) and document.get("schema") == SCHEMA:
            dispatch.append(os.path.relpath(path, LANE))
        else:
            ignored += 1
    return {"json_names": json_names, "not_regular": not_regular, "regular": len(regular),
            "dispatch": sorted(dispatch), "ignored": ignored, "unreadable": unreadable}


def analyse(rel):
    raw = read_bytes(os.path.join(LANE, rel))
    document = json.loads(raw, parse_constant=reject)
    task_call = document.get("taskCall")
    no_spawn = "taskCall" in document and task_call is None
    tasks = task_call.get("tasks", []) if isinstance(task_call, dict) else []
    if not isinstance(tasks, list):
        tasks = []
    members = []
    for task in tasks:
        is_dict = isinstance(task, dict)
        text = task.get("task") if is_dict else None
        member = {"name": task.get("name") if is_dict else None,
                  "agent": task.get("agent") if is_dict else None,
                  "gt_raw": None, "tool_raw": None, "trailer_lines": 0, "text_tail": None,
                  "path": None, "status": "unparsed", "through_symlink": False, "anomaly": None}
        if isinstance(text, str):
            last = text.split("\n")[-1]
            match = TRAILER.match(last)
            member["gt_raw"] = match.group(1) if match else None
            member["trailer_lines"] = sum(1 for line in text.splitlines() if TRAILER.fullmatch(line.rstrip()))
            for line in reversed(text.splitlines()):
                found = TRAILER.fullmatch(line.rstrip())
                if found:
                    member["tool_raw"] = found.group(1)
                    break
            member["text_tail"] = repr(text[-2:])
        raw_path = member["gt_raw"]
        if raw_path is not None:
            parts = safe_parts(raw_path)
            if parts is None:
                member["status"] = "unsafe"
            else:
                member["path"] = "/".join(parts)
                kind, size, through = walk(LANE, parts)
                member["through_symlink"] = through
                if kind == "regular":
                    if size == 0:
                        member["status"] = "empty"
                    elif size <= 16 and read_bytes(os.path.join(LANE, *parts)) in STUB:
                        member["status"] = "stub"
                    else:
                        member["status"] = "present"
                elif kind == "missing":
                    fleet_kind, _fleet_size, _ = walk(FLEET, parts)
                    member["status"] = "misrooted" if fleet_kind == "regular" else "missing"
                else:
                    member["status"] = "missing"
                    member["anomaly"] = kind
        members.append(member)
    counts = {name: 0 for name in STATUSES}
    for member in members:
        counts[member["status"]] += 1
    safe = sum(1 for m in members if m["status"] not in ("unparsed", "unsafe"))
    total = len(members)
    present = counts["present"]
    if no_spawn:
        state = "no-spawn"
    elif safe == 0:
        state = "unavailable"
    elif present == total:
        state = "settled"
    elif present:
        state = "partial"
    else:
        state = "unsettled"
    missing = sorted((m["name"] for m in members if m["status"] != "present"),
                     key=lambda n: str(n).encode("utf-8"))
    return {"dispatch_path": rel, "no_spawn": no_spawn, "members": members,
            "counts": counts, "state": state, "missing": missing}


def parse_gt():
    rows, misses = {}, {}
    for line in open(GT, encoding="utf-8").read().splitlines():
        match = GT_ROW.match(line)
        if match:
            g = match.groups()
            rows[g[1]] = {"wave": g[2], "reportdir": g[3], "members": int(g[4]), "parsed": int(g[5]),
                          "unparsed": int(g[6]), "unsafe": int(g[7]), "present": int(g[8]),
                          "empty": int(g[9]), "missing": int(g[10]), "misrooted": int(g[11]),
                          "state": g[12], "flag": g[13]}
        match = GT_MISS.match(line)
        if match:
            misses[".ufo/waves/" + match.group(1)] = (
                int(match.group(2)), sorted(x.strip() for x in match.group(3).split(",")))
    return rows, misses


def summary_mine(res):
    c = res["counts"]
    total = len(res["members"])
    return {"members": total, "parsed": total - c["unparsed"], "unparsed": c["unparsed"],
            "unsafe": c["unsafe"], "present": c["present"], "empty": c["empty"], "stub": c["stub"],
            "missing": c["missing"], "misrooted": c["misrooted"], "state": res["state"]}


def summary_tool(wave):
    c = wave["counts"]
    total = len(wave["members"])
    return {"members": total, "parsed": total - c["unparsed"], "unparsed": c["unparsed"],
            "unsafe": c["unsafe"], "present": c["present"], "empty": c["empty"], "stub": c["stub"],
            "missing": c["missing"], "misrooted": c["misrooted"], "state": wave["state"]}


def summary_gt(row):
    return {"members": row["members"], "parsed": row["parsed"], "unparsed": row["unparsed"],
            "unsafe": row["unsafe"], "present": row["present"], "empty": row["empty"], "stub": None,
            "missing": row["missing"], "misrooted": row["misrooted"], "state": row["state"]}


def compact(s):
    return "%s/%s/%s/%s/%s/%s/%s/%s/%s" % tuple(s[k] for k in (
        "members", "present", "missing", "misrooted", "stub", "empty", "unparsed", "unsafe", "state"))


def main():
    found = discover()
    print("DISCOVERY json_names=%d not_regular=%d regular=%d dispatch=%d ignored=%d unreadable=%d" % (
        found["json_names"], len(found["not_regular"]), found["regular"], len(found["dispatch"]),
        found["ignored"], found["unreadable"]))
    print("IDENTITY regular_json == dispatch+ignored+unreadable:",
          found["regular"] == len(found["dispatch"]) + found["ignored"] + found["unreadable"])
    print("NOT_REGULAR_JSON", found["not_regular"][:10])

    scan = json.load(open(SCAN, encoding="utf-8"))
    tool = {w["dispatch_path"]: w for w in scan["waves"]}
    gt_rows, gt_miss = parse_gt()
    print("GT_ROWS=%d GT_MISS_LISTS=%d" % (len(gt_rows), len(gt_miss)))
    print("PATHSET discovery==tool:", sorted(found["dispatch"]) == sorted(tool),
          "| GT==tool:", sorted(gt_rows) == sorted(tool),
          "| GT_miss keys subset of tool:", set(gt_miss) <= set(tool))

    fleet = json.load(open(FLJ, encoding="utf-8"))
    kaid = [lane for lane in fleet["lanes"] if lane.get("lane") == "kaidoku-shokunin"]
    print("FLEET_KAIDOKU_ENTRIES", len(kaid), json.dumps(kaid[0], sort_keys=True) if kaid else None)

    results = {rel: analyse(rel) for rel in found["dispatch"]}
    member_diffs, trailer_disagree, field_diffs, gt_field_diffs = [], [], [], []
    tails = []
    for rel in sorted(results):
        mine = results[rel]
        wave = tool[rel]
        mt = [(m["name"], m["agent"], m["status"]) for m in mine["members"]]
        tt = [(m["name"], m["agent"], m["status"]) for m in wave["members"]]
        if mt != tt:
            member_diffs.append({"dispatch": rel, "len_tool": len(tt), "len_mine": len(mt),
                                 "pairs": [(a, b) for a, b in zip(tt, mt) if a != b][:20]})
        for m in mine["members"]:
            if m["gt_raw"] != m["tool_raw"]:
                trailer_disagree.append((rel, m["name"], m["gt_raw"], m["tool_raw"]))
            if m["trailer_lines"] != 1:
                tails.append((rel, m["name"], m["trailer_lines"]))
        sm, st, sg = summary_mine(mine), summary_tool(wave), summary_gt(gt_rows[rel]) if rel in gt_rows else None
        for key in sm:
            if sm[key] != st[key]:
                field_diffs.append((rel, "mine-vs-tool", key, sm[key], st[key]))
        if sg is not None:
            for key in COMPARE:
                if sg[key] != st[key]:
                    gt_field_diffs.append((rel, "gt-vs-tool", key, sg[key], st[key]))
            gt_missing = gt_miss.get(rel, (0, []))[1]
            if gt_missing != sorted(wave["missing"]):
                gt_field_diffs.append((rel, "gt-vs-tool", "missing-names", gt_missing, sorted(wave["missing"])))
        if sorted(mine["missing"]) != sorted(wave["missing"]):
            field_diffs.append((rel, "mine-vs-tool", "missing-names", mine["missing"], wave["missing"]))
        print("WAVE %-36s tool=%-34s mine=%-34s gt=%s" % (
            rel, compact(st), compact(sm), compact(sg) if sg else "-"))

    print("MEMBER_LEVEL_DIFFS (tool vs mine, name/agent/status):", len(member_diffs), member_diffs[:5])
    print("TRAILER_GT_vs_TOOL_DISAGREE (last-line jq-style vs R1 last-match):", len(trailer_disagree), trailer_disagree[:10])
    print("TASKS_WITH_TRAILER_LINES!=1:", len(tails), tails[:10])
    print("FIELD_DIFFS mine-vs-tool:", len(field_diffs), field_diffs[:20])
    print("GT_DIFFS gt-vs-tool:", len(gt_field_diffs), gt_field_diffs[:20])

    all_members = [m for res in results.values() for m in res["members"]]
    print("ANOMALY_ERRNOS (lstat errors other than ENOENT/ENOTDIR):", ANOMALY_ERRNOS[:10], len(ANOMALY_ERRNOS))
    print("THROUGH_SYMLINK members:", sum(1 for m in all_members if m["through_symlink"]))
    print("OTHER_KIND anomalies:", sum(1 for m in all_members if m["anomaly"]))
    print("STUB members:", sum(1 for m in all_members if m["status"] == "stub"))
    print("EMPTY members:", sum(1 for m in all_members if m["status"] == "empty"))
    tails_text = [(rel, m["name"], m["text_tail"]) for rel in results for m in results[rel]["members"]
                  if m["text_tail"] and m["text_tail"][1:-1][-1:] in ("\n", "\r", " ", "\t")]
    print("TASKS_WITH_TRAILING_WS_OR_NL:", len(tails_text), tails_text[:5])

    totals = {"members": len(all_members), "waves": len(results), "unreadable_json": found["unreadable"],
              "ignored_json": found["ignored"]}
    for key in ("present", "missing", "misrooted", "unsafe", "unparsed", "empty", "stub"):
        totals[key] = sum(res["counts"][key] for res in results.values())
    totals["exit"] = 0 if all(r["state"] in ("settled", "no-spawn") for r in results.values()) else 1
    totals["states"] = {}
    for res in results.values():
        totals["states"][res["state"]] = totals["states"].get(res["state"], 0) + 1
    print("MINE_TOTALS", json.dumps(totals, sort_keys=True))
    print("TOOL_TOTALS", json.dumps(scan["totals"], sort_keys=True), "ignored", scan["ignored_json"],
          "unreadable", scan["unreadable_json"])
    fe = kaid[0] if kaid else {}
    fleet_cmp = {}
    for key in ("members", "present", "missing", "misrooted", "unsafe", "unparsed", "empty", "waves",
                "unreadable_json", "exit"):
        fleet_cmp[key] = (fe.get(key), totals.get(key), fe.get(key) == totals.get(key))
    print("FLEET_vs_MINE", json.dumps(fleet_cmp, sort_keys=True))

    gt_mtime = os.stat(GT).st_mtime
    fl_mtime = os.stat(FLJ).st_mtime
    scan_mtime = os.stat(SCAN).st_mtime
    print("MTIME GT=%s FLEET=%s SCAN=%s" % (fmt(gt_mtime), fmt(fl_mtime), fmt(scan_mtime)))
    for rel in sorted(results):
        info = lst(os.path.join(LANE, rel))
        print("DISPATCH_MTIME %-36s %s %s" % (rel, fmt(info.st_mtime),
                                             "NEWER_THAN_GT" if info.st_mtime > gt_mtime else ""))

    dirs = set()
    for res in results.values():
        for m in res["members"]:
            if m["path"]:
                dirs.add(os.path.dirname(os.path.join(LANE, m["path"])))
    gt_dirs = {os.path.join(LANE, ".ufo", "waves", row["reportdir"]) for row in gt_rows.values()}
    print("REPORT_DIR_SET trailer==GT:", dirs == gt_dirs, len(dirs))
    newer_dirs = []
    for d in sorted(gt_dirs):
        info = lst(d)
        if info is None:
            print("REPORT_DIR_ABSENT", d)
            continue
        if info.st_mtime > gt_mtime:
            newer_dirs.append((os.path.relpath(d, LANE), fmt(info.st_mtime)))
    print("REPORT_DIRS_MTIME_AFTER_GT:", newer_dirs)

    referenced = {m["path"] for m in all_members if m["path"]}
    orphans, newer_entries = [], []
    for d in sorted(gt_dirs):
        try:
            with os.scandir(d) as it:
                for entry in it:
                    rel_e = os.path.relpath(entry.path, LANE)
                    info = entry.stat(follow_symlinks=False)
                    if rel_e not in referenced:
                        orphans.append(rel_e)
                    if info.st_mtime > gt_mtime:
                        newer_entries.append((rel_e, fmt(info.st_mtime)))
        except OSError as exc:
            print("SCANDIR_ERROR", d, exc)
    print("ORPHAN_ENTRIES_IN_REPORT_DIRS:", len(orphans))
    print("ENTRIES_IN_REPORT_DIRS_NEWER_THAN_GT:", len(newer_entries), newer_entries[:40])

    present_newer, older_than_dispatch = [], 0
    for rel, res in results.items():
        dinfo = lst(os.path.join(LANE, rel))
        for m in res["members"]:
            if m["status"] in ("present", "stub", "empty") and m["path"]:
                info = lst(os.path.join(LANE, m["path"]))
                if info is None:
                    continue
                if info.st_mtime > gt_mtime:
                    present_newer.append((m["path"], fmt(info.st_mtime)))
                if info.st_mtime < dinfo.st_mtime:
                    older_than_dispatch += 1
    print("PRESENT_REPORTS_NEWER_THAN_GT:", len(present_newer), present_newer[:40])
    print("PRESENT_REPORTS_OLDER_THAN_DISPATCH:", older_than_dispatch)

    with open(SCRATCH + "/compare.json", "w", encoding="utf-8") as stream:
        json.dump({"discovery": found, "totals": totals, "fleet_vs_mine": fleet_cmp,
                   "field_diffs": field_diffs, "gt_diffs": gt_field_diffs,
                   "member_diffs": member_diffs, "trailer_disagree": trailer_disagree,
                   "results": results}, stream, indent=1, sort_keys=True, default=str)
    print("WROTE", SCRATCH + "/compare.json")


if __name__ == "__main__":
    main()
