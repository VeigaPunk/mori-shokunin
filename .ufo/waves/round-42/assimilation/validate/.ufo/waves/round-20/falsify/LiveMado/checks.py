#!/usr/bin/env python3
"""LiveMado C2 attack checks (read-only; writes only under SCR).

A  discovery: every JSON under lane .ufo/waves, schema census, dispatch-like misses, non-.json dispatch text
B  present semantics: size distribution of present reports, tiny or stub-like files
C  missing semantics: reportDir existence, basename hits elsewhere in lane, exact-path hits in sibling lanes
D  trailer rule: final-line trailer, multiple trailers, duplicate member names per wave
"""
import csv
import json
import os
import re
import collections

BASE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
SCR = BASE + "/.ufo/waves/round-20/falsify/LiveMado"
EVID = BASE + "/.ufo/waves/round-20/evidence/c2-live-fleet.json"
WAVES = os.path.join(LANE, ".ufo", "waves")
DISPATCH_SCHEMA = "ufo-swarm-wave-dispatch-v1"
DISPATCH_BYTES = DISPATCH_SCHEMA.encode()
TRAILER = re.compile(r"^Report: write your scoped findings to (\S+)$")


def _reject(constant):
    raise ValueError("non-JSON constant " + constant)


def main():
    out = {}
    # ---- A. discovery ----
    json_files, nonjson_dispatch_text, symlinks = [], [], []
    basenames = collections.defaultdict(list)
    regular = 0
    dir_count = 0
    for root, dnames, fnames in os.walk(WAVES, followlinks=False):
        for d in dnames:
            dir_count += 1
            full = os.path.join(root, d)
            if os.path.islink(full):
                symlinks.append(os.path.relpath(full, LANE))
        for f in fnames:
            full = os.path.join(root, f)
            if os.path.islink(full):
                symlinks.append(os.path.relpath(full, LANE))
                continue
            if not os.path.isfile(full):
                continue
            regular += 1
            rel = os.path.relpath(full, LANE)
            basenames[f].append(rel)
            if f.endswith(".json"):
                json_files.append((full, rel))
            elif os.path.getsize(full) <= 4_000_000:
                with open(full, "rb") as stream:
                    if DISPATCH_BYTES in stream.read():
                        nonjson_dispatch_text.append(rel)
    schema_census = collections.Counter()
    unreadable = []
    dispatch_like_not_exact = []
    dispatch_exact = []
    for full, rel in json_files:
        with open(full, "rb") as stream:
            raw = stream.read()
        try:
            doc = json.loads(raw.decode("utf-8"), parse_constant=_reject)
        except (UnicodeDecodeError, ValueError):
            unreadable.append(rel)
            continue
        if not isinstance(doc, dict):
            schema_census["<non-object>"] += 1
            continue
        schema = doc.get("schema")
        schema_census[str(schema)] += 1
        if schema == DISPATCH_SCHEMA:
            dispatch_exact.append(rel)
        elif "taskCall" in doc or (isinstance(schema, str) and "dispatch" in schema.lower()):
            dispatch_like_not_exact.append([rel, schema])
    out["A_json_files"] = len(json_files)
    out["A_regular_files_under_waves"] = regular
    out["A_dirs_under_waves"] = dir_count
    out["A_symlinks_under_waves"] = sorted(symlinks)
    out["A_schema_census"] = dict(schema_census.most_common())
    out["A_unreadable_json"] = sorted(unreadable)
    out["A_dispatch_exact_count"] = len(dispatch_exact)
    out["A_dispatch_like_not_exact"] = dispatch_like_not_exact
    out["A_nonjson_files_containing_dispatch_schema_text"] = sorted(nonjson_dispatch_text)

    # ---- B/C/D use the live member table written by compare.py ----
    members = []
    with open(SCR + "/members-live.tsv", newline="", encoding="utf-8") as stream:
        members = list(csv.DictReader(stream, delimiter="\t", quoting=csv.QUOTE_NONE))
    present = [m for m in members if m["live_status"] == "present"]
    missing = [m for m in members if m["live_status"] != "present"]
    out["B_present_count"] = len(present)

    sizes = []
    tiny = []
    stub_prefixed = []
    for m in present:
        path = os.path.join(LANE, m["report_rel"])
        size = os.lstat(path).st_size
        sizes.append((size, m["report_rel"]))
        if size <= 64:
            with open(path, "rb") as stream:
                tiny.append([m["report_rel"], size, stream.read(64).decode("utf-8", "replace")])
        with open(path, "rb") as stream:
            head = stream.read(16)
        if head.startswith(b"STATUS: started"):
            stub_prefixed.append([m["report_rel"], size])
    sizes.sort()
    out["B_smallest_present"] = sizes[:10]
    out["B_present_le_64_bytes"] = tiny
    out["B_present_starting_with_stub_text"] = stub_prefixed
    out["B_present_zero_size"] = [r for s, r in sizes if s == 0]

    # C. missing semantics
    sibling_lanes = [lane["lane"] for lane in json.load(open(EVID, "rb"))["lanes"]
                     if lane["lane"] != "mado-shokunin"]
    by_lower = collections.defaultdict(list)
    for name, paths in basenames.items():
        by_lower[name.lower()].extend(paths)
    c_rows = []
    basename_hits = []
    sibling_hits = []
    dir_status = collections.Counter()
    for m in missing:
        rel = m["report_rel"]
        wave_dir = os.path.join(LANE, os.path.dirname(rel))
        dir_exists = os.path.isdir(wave_dir) and not os.path.islink(wave_dir)
        dir_status["exists" if dir_exists else "absent"] += 1
        base = os.path.basename(rel)
        hits = [p for p in basenames.get(base, []) if p != rel]
        ci_hits = [p for p in by_lower.get(base.lower(), []) if p != rel and p not in hits]
        if hits or ci_hits:
            basename_hits.append([rel, hits, ci_hits])
        sib = []
        for lane in sibling_lanes + ["."]:
            cand = os.path.join(FLEET, lane, rel) if lane != "." else os.path.join(FLEET, rel)
            if os.path.lexists(cand):
                sib.append([lane, os.path.isfile(cand) and not os.path.islink(cand), os.path.getsize(cand) if os.path.isfile(cand) else None])
        if sib:
            sibling_hits.append([rel, sib])
        c_rows.append([m["file"], m["name"], rel, dir_exists])
    out["C_missing_count"] = len(missing)
    out["C_reportdir_status"] = dict(dir_status)
    out["C_basename_hits_in_lane_other_path"] = basename_hits
    out["C_exact_path_hits_fleet_or_sibling_lanes"] = sibling_hits
    per_file_dir = collections.Counter()
    for file_, name, rel, dir_exists in c_rows:
        per_file_dir[(file_.replace(".ufo/waves/", ""), dir_exists)] += 1
    out["C_missing_by_file_dir_exists"] = [[k[0], k[1], v] for k, v in sorted(per_file_dir.items())]

    # D. trailer rule and member names
    final_line_not_trailer = []
    multi_trailer = []
    dup_names = []
    with_trailer_tasks = 0
    for full_rel in sorted({m["file"] for m in members}):
        with open(os.path.join(LANE, full_rel), "rb") as stream:
            doc = json.loads(stream.read().decode("utf-8"), parse_constant=_reject)
        tasks = doc["taskCall"]["tasks"]
        names = [t.get("name") for t in tasks]
        for name, count in collections.Counter(names).items():
            if count > 1:
                dup_names.append([full_rel, name, count])
        for index, task in enumerate(tasks):
            text = task["task"]
            lines = text.rstrip().split("\n")
            trailers = [ln for ln in lines if TRAILER.fullmatch(ln.rstrip())]
            if trailers:
                with_trailer_tasks += 1
            if len(trailers) > 1:
                multi_trailer.append([full_rel, index, len(trailers)])
            if not (lines and TRAILER.fullmatch(lines[-1].rstrip())):
                final_line_not_trailer.append([full_rel, index])
    out["D_tasks_with_trailer_line"] = with_trailer_tasks
    out["D_final_line_not_trailer"] = final_line_not_trailer
    out["D_multi_trailer"] = multi_trailer
    out["D_duplicate_member_names"] = dup_names

    with open(SCR + "/checks.json", "w", encoding="utf-8") as stream:
        json.dump(out, stream, indent=1, sort_keys=True, ensure_ascii=False)
        stream.write("\n")
    for key in sorted(out):
        value = out[key]
        text = json.dumps(value, ensure_ascii=False)
        if len(text) > 700:
            text = text[:700] + " ...[%d chars]" % len(text)
        print(key, "=", text)


if __name__ == "__main__":
    main()
