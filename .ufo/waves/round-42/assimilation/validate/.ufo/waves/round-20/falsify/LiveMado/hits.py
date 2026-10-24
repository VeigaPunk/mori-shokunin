#!/usr/bin/env python3
"""LiveMado: classify the six missing-member basename hits (read-only; prints only).

For each missing member whose basename exists elsewhere in the lane .ufo/waves tree, print:
  the expected path, the hit path(s), mtimes, sizes, the first 120 bytes of each hit,
  the wave dispatch mtimes, and whether the hit's wave dispatch names the same member.
"""
import csv
import json
import os
import datetime

BASE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SCR = BASE + "/.ufo/waves/round-20/falsify/LiveMado"


def ts(path):
    return datetime.datetime.fromtimestamp(os.lstat(os.path.join(LANE, path)).st_mtime).isoformat(timespec="seconds")


def main():
    checks = json.load(open(SCR + "/checks.json", encoding="utf-8"))
    with open(SCR + "/members-live.tsv", newline="", encoding="utf-8") as stream:
        members = list(csv.DictReader(stream, delimiter="\t", quoting=csv.QUOTE_NONE))
    by_file = {}
    for m in members:
        by_file.setdefault(m["file"], []).append(m)
    for rel, hits, _ci in checks["C_basename_hits_in_lane_other_path"]:
        miss = [m for m in members if m["report_rel"] == rel][0]
        wave_file = miss["file"]
        print("MISSING", rel, "| member", miss["name"], "| wave", wave_file, "| dispatch mtime", ts(wave_file))
        for hit in hits:
            size = os.lstat(os.path.join(LANE, hit)).st_size
            with open(os.path.join(LANE, hit), "rb") as stream:
                head = stream.read(120)
            hit_wave = [f for f in by_file if hit.startswith(os.path.dirname(os.path.dirname(f)) + "/")
                        and os.path.dirname(f) != "" and "/".join(hit.split("/")[:4]) == "/".join(f.split("/")[:4])]
            print("  HIT", hit, "| mtime", ts(hit), "| size", size, "| hit-wave dispatch", hit_wave,
                  "| hit-wave dispatch mtime", [ts(w) for w in hit_wave])
            same = [m for w in hit_wave for m in by_file[w] if m["name"] == miss["name"]]
            print("       same-name member in hit wave:", [(m["file"], m["live_status"]) for m in same])
            print("       head:", repr(head))
        # the expected path's wave: is there any other present report in the same wave dir that is newer?
        wave_dir = os.path.join(LANE, os.path.dirname(os.path.dirname(rel)))
        print("  expected wave dir", os.path.dirname(os.path.dirname(rel)), "reports dir exists:",
              os.path.isdir(os.path.join(LANE, os.path.dirname(rel))))


if __name__ == "__main__":
    main()
