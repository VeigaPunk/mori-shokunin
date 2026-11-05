#!/usr/bin/env python3
"""Move-only check for the round-92 trio patches (lesson Mistake 'moved-body-lines').

For each patch: every removed line must reappear byte-identical among the added lines (a move),
and every added line with no removed counterpart must begin with one of the provenance keys.
Prints per file: moved key lines, removed lines that do not reappear, new added lines, and
non-key new lines. Exit 0 iff no non-key new line and no removed line outside the two disclosed
blank-line cases. Usage: python3 -I trio-moveonly.py <patch> [<patch> ...]
"""
import re
import sys
from collections import Counter

KEY = re.compile(r"^(source|verified-at|recheck):")


def check(path):
    cur, per = None, {}
    for line in open(path, encoding="utf-8"):
        if line.startswith("diff --git"):
            cur = line.split(" w/")[-1].strip()
            per[cur] = {"add": Counter(), "rem": Counter()}
            continue
        if cur is None or line.startswith(("+++ ", "--- ", "@@", "index ")):
            continue
        if line.startswith("+"):
            per[cur]["add"][line[1:].rstrip("\n")] += 1
        elif line.startswith("-"):
            per[cur]["rem"][line[1:].rstrip("\n")] += 1
    bad = 0
    for f, d in sorted(per.items()):
        R, A = d["rem"], d["add"]
        not_moved = R - A
        leftover = A - R
        non_key = [x for x in leftover if not KEY.match(x)]
        moved = sum(v for k, v in R.items() if KEY.match(k))
        print("%s moved_key_lines=%d removed_not_reappearing=%d added_new=%d non_key_new=%d" % (
            f.replace("corpus/knowledge/", ""), moved, sum(not_moved.values()),
            sum(leftover.values()), len(non_key)))
        for x in non_key:
            print("   NON-KEY-NEW:", x[:110])
            bad += 1
        for x in not_moved:
            if x.strip():
                print("   REMOVED-NOT-REAPPEARING:", x[:110])
                bad += 1
    return bad


if __name__ == "__main__":
    total = sum(check(p) for p in sys.argv[1:])
    print("TRIO_MOVEONLY non_move_findings=%d" % total)
    sys.exit(0 if total == 0 else 1)
