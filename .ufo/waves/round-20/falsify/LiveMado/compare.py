#!/usr/bin/env python3
"""LiveMado C2 falsification (read-only; writes only under SCR).

scan  : scan.json from tools/mori-wave-settlement.py scan (this seat, 08:00:35)
gt    : build/GtLaneMado/ground-truth.json + members.tsv (wave-1 manual, 07:31-07:36)
fleet : evidence/c2-live-fleet.json (committed 07:46:53; per-lane totals only)
live  : independent oracle below (os.path.islink / os.stat), not the tool's helpers
"""
import csv
import datetime
import hashlib
import json
import os
import re
from collections import Counter

BASE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
SCR = BASE + "/.ufo/waves/round-20/falsify/LiveMado"
GT = BASE + "/.ufo/waves/round-20/build/GtLaneMado"
EVID = BASE + "/.ufo/waves/round-20/evidence/c2-live-fleet.json"
TRAILER = re.compile(r"^Report: write your scoped findings to (\S+)$")
STUBS = (b"STATUS: started", b"STATUS: started\n")
SPECIAL = ("\r", "\x0b", "\x0c", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029")


def jload(path):
    with open(path, "rb") as stream:
        return json.loads(stream.read().decode("utf-8"))


def mtime_of(path):
    st = os.lstat(path)
    return datetime.datetime.fromtimestamp(st.st_mtime).isoformat(timespec="milliseconds")


def trailer_splitlines(text):
    # same rule as tools/mori-wave-settlement.py:204-212 (str.splitlines + fullmatch)
    for line in reversed(text.splitlines()):
        match = TRAILER.fullmatch(line.rstrip())
        if match:
            return match.group(1)
    return None


def trailer_split_newline(text):
    # GT rule: split on newline only
    for line in reversed(text.split("\n")):
        match = TRAILER.fullmatch(line.rstrip())
        if match:
            return match.group(1)
    return None


def symlink_in_path(root, rel):
    current = root
    for comp in rel.split("/"):
        current = os.path.join(current, comp)
        if os.path.islink(current):
            return True
    return False


def live_status(rel):
    """Oracle: follow-links stat plus islink() on every component."""
    lane_path = os.path.join(LANE, rel)
    if symlink_in_path(LANE, rel):
        return "missing", "symlink-in-path", None
    if os.path.isfile(lane_path):
        size = os.stat(lane_path).st_size
        if size == 0:
            return "empty", None, 0
        if size <= 16:
            with open(lane_path, "rb") as stream:
                if stream.read(64) in STUBS:
                    return "stub", None, size
        return "present", None, size
    if os.path.exists(lane_path):
        return "missing", "not-regular", None
    if os.path.isfile(os.path.join(FLEET, rel)):
        return "misrooted", "fleet-regular", None
    return "missing", "absent", None


def state_of(present, total):
    if present == total:
        return "settled"
    if present:
        return "partial"
    return "unsettled"


def main():
    scan = jload(SCR + "/scan.json")
    gt = jload(GT + "/ground-truth.json")
    fleet = jload(EVID)
    S = {w["dispatch_path"]: w for w in scan["waves"]}
    G = {w["dispatch_path"]: w for w in gt["waves"]}

    gt_rows = {}
    with open(GT + "/members.tsv", newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream, delimiter="\t", quoting=csv.QUOTE_NONE):
            gt_rows.setdefault(row["file"], {})[int(row["idx"])] = row

    result = {
        "discovery": {
            "scan_waves": len(S),
            "gt_waves": len(G),
            "only_scan": sorted(set(S) - set(G)),
            "only_gt": sorted(set(G) - set(S)),
            "scan_totals": scan["totals"],
            "gt_totals": gt["totals"],
            "scan_ignored_unreadable": [scan["ignored_json"], scan["unreadable_json"]],
            "fleet_mado_entry": [lane for lane in fleet["lanes"] if lane["lane"] == "mado-shokunin"],
        },
        "files": [],
        "member_diffs": [],
        "special_char_tasks": [],
        "members": [],
    }

    live_totals = Counter()
    rp_seen = Counter()
    newest_reports = []
    report_dirs = {}

    for path in sorted(S):
        sw = S[path]
        gw = G.get(path, {})
        gc = gw.get("counts", {})
        raw = open(os.path.join(LANE, path), "rb").read()
        doc = json.loads(raw.decode("utf-8"))
        tasks = doc["taskCall"]["tasks"]
        gmap = gt_rows.get(path, {})
        live_counts = Counter()
        live_missing = []
        for index, task in enumerate(tasks):
            text = task["task"]
            rp = trailer_splitlines(text)
            rp_gt = trailer_split_newline(text)
            if rp != rp_gt:
                result["member_diffs"].append({"kind": "trailer-rule", "file": path, "idx": index,
                                               "tool": rp, "gt": rp_gt})
            if any(ch in text for ch in SPECIAL):
                result["special_char_tasks"].append([path, index])
            if rp is None:
                status, detail, size = "unparsed", None, None
            else:
                rp_seen[rp] += 1
                status, detail, size = live_status(rp)
                if status in ("present", "stub", "empty"):
                    st = os.lstat(os.path.join(LANE, rp))
                    newest_reports.append((st.st_mtime, rp, status))
                    report_dirs.setdefault(os.path.dirname(rp), None)
                else:
                    report_dirs.setdefault(os.path.dirname(rp), None)
            live_counts[status] += 1
            if status != "present":
                live_missing.append(task.get("name"))
            sm = sw["members"][index]
            g = gmap.get(index)
            member = {
                "file": path, "idx": index, "name": task.get("name"), "agent": task.get("agent"),
                "report_rel": rp, "scan_status": sm["status"],
                "gt_status": g["status"] if g else None, "live_status": status,
                "live_detail": detail, "live_size": size,
                "report_mtime": mtime_of(os.path.join(LANE, rp)) if (rp and os.path.lexists(os.path.join(LANE, rp))) else None,
            }
            result["members"].append(member)
            problems = []
            if g is None:
                problems.append("no-gt-row")
            else:
                if g["name"] != task.get("name"): problems.append("name")
                if g["agent"] != task.get("agent"): problems.append("agent")
                if g["report_rel"] != rp: problems.append("report-path")
                if g["status"] != status: problems.append("gt-vs-live")
            if sm["name"] != task.get("name"): problems.append("scan-name")
            if sm["status"] != status: problems.append("scan-vs-live")
            if g is not None and sm["status"] != g["status"]: problems.append("scan-vs-gt")
            if problems:
                result["member_diffs"].append({"kind": ",".join(problems), "file": path, "idx": index,
                                               "name": task.get("name"), "report": rp,
                                               "scan": sm["status"], "gt": member["gt_status"],
                                               "live": status, "live_detail": detail})
        live_totals.update(live_counts)
        present_live = live_counts["present"]
        row = {
            "file": path,
            "members": [len(sw["members"]), gw.get("members"), len(tasks)],
            "present": [sw["counts"]["present"], gc.get("present"), live_counts["present"]],
            "missing": [sw["counts"]["missing"], gc.get("missing"), live_counts["missing"]],
            "misrooted": [sw["counts"]["misrooted"], gc.get("misrooted"), live_counts["misrooted"]],
            "stub": [sw["counts"]["stub"], None, live_counts["stub"]],
            "empty": [sw["counts"]["empty"], gc.get("empty"), live_counts["empty"]],
            "unparsed": [sw["counts"]["unparsed"], gc.get("unparsed"), live_counts["unparsed"]],
            "unsafe": [sw["counts"]["unsafe"], gc.get("unsafe"), live_counts["unsafe"]],
            "state": [sw["state"], gw.get("state"), state_of(present_live, len(tasks))],
            "wave": [sw["wave"], gw.get("wave"), doc.get("wave")],
            "missing_names_equal": sorted(sw["missing"]) == sorted(gw.get("missing", [])) == sorted(n for n in live_missing if n is not None),
            "sha_equal": [sw["dispatch_sha256"] == gw.get("dispatch_sha256") == hashlib.sha256(raw).hexdigest()],
            "scan_sha": sw["dispatch_sha256"],
            "live_sha": hashlib.sha256(raw).hexdigest(),
            "dispatch_mtime": mtime_of(os.path.join(LANE, path)),
            "dispatch_size": os.stat(os.path.join(LANE, path)).st_size,
        }
        result["files"].append(row)

    # Report-directory mtimes: a create/delete in a reportDir after the snapshot would show here.
    for directory in report_dirs:
        full = os.path.join(LANE, directory)
        report_dirs[directory] = mtime_of(full) if os.path.isdir(full) and not os.path.islink(full) else None
    result["report_dir_mtimes_newest"] = sorted(
        ((v, k) for k, v in report_dirs.items() if v), reverse=True)[:8]
    result["newest_present_reports"] = [
        (datetime.datetime.fromtimestamp(t).isoformat(timespec="seconds"), rp, status)
        for t, rp, status in sorted(newest_reports, reverse=True)[:8]]
    result["live_totals"] = dict(sorted(live_totals.items()))
    result["rp_unique"] = len(rp_seen)
    result["rp_max_multiplicity"] = max(rp_seen.values()) if rp_seen else 0
    result["live_discovery_json_count"] = sum(
        len(files) for _, _, files in os.walk(os.path.join(LANE, ".ufo", "waves"), followlinks=False)
        for name in files if name.endswith(".json"))

    with open(SCR + "/compare.json", "w", encoding="utf-8") as stream:
        json.dump(result, stream, indent=1, sort_keys=True)
        stream.write("\n")

    with open(SCR + "/members-live.tsv", "w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(["file", "idx", "name", "agent", "report_rel", "gt_status", "scan_status",
                         "live_status", "live_detail", "live_size", "report_mtime"])
        for m in result["members"]:
            writer.writerow([m["file"], m["idx"], m["name"], m["agent"], m["report_rel"], m["gt_status"],
                             m["scan_status"], m["live_status"], m["live_detail"] or "",
                             "" if m["live_size"] is None else m["live_size"], m["report_mtime"] or ""])

    print("DISCOVERY", json.dumps({k: result["discovery"][k] for k in
                                    ("scan_waves", "gt_waves", "only_scan", "only_gt", "scan_ignored_unreadable")}))
    print("TOTALS scan", json.dumps(result["discovery"]["scan_totals"], sort_keys=True))
    print("TOTALS gt  ", json.dumps(result["discovery"]["gt_totals"], sort_keys=True))
    print("TOTALS live", json.dumps(result["live_totals"], sort_keys=True), "rp_unique", result["rp_unique"],
          "rp_max_mult", result["rp_max_multiplicity"], "live_json_under_waves", result["live_discovery_json_count"])
    print("FLEET", json.dumps(result["discovery"]["fleet_mado_entry"], sort_keys=True))
    print("SPECIAL-CHAR tasks", len(result["special_char_tasks"]))
    print("MEMBER DIFFS", len(result["member_diffs"]))
    for diff in result["member_diffs"][:60]:
        print("  ", json.dumps(diff, sort_keys=True))
    print("FILES")
    for row in result["files"]:
        print("  %-62s m=%s p=%s mi=%s mr=%s st=%s stub=%s state=%s namesEq=%s sha=%s" % (
            row["file"].replace(".ufo/waves/", ""), row["members"], row["present"], row["missing"],
            row["misrooted"], row["stub"], row["empty"], row["state"], row["missing_names_equal"],
            row["sha_equal"]))
    print("NEWEST PRESENT REPORTS", json.dumps(result["newest_present_reports"]))
    print("NEWEST REPORT DIRS", json.dumps(result["report_dir_mtimes_newest"]))


if __name__ == "__main__":
    main()
