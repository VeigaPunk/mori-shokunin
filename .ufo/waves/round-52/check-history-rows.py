#!/usr/bin/env python3
"""Lesson M2 check (round 52): SCORECARD.md outside the `## Axes` table must be byte-identical between the
entering tip and a later revision (round tables are history, never rewritten).
Usage: check-history-rows.py <entering-rev> <rev>          compare two committed revisions
       check-history-rows.py <entering-rev> --applier      apply the frozen controls/c1-data.py `axes` part to
                                                           the entering bytes in memory and compare
Prints `HISTORY_ROWS changed=N lines=[...]`; exit 0 iff N == 0, 1 otherwise, 2 on setup error. Read-only.
"""
import importlib.util
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


def show(rev):
    p = subprocess.run(["git", "-C", LANE, "show", "%s:SCORECARD.md" % rev], stdout=subprocess.PIPE,
                       stderr=subprocess.DEVNULL)
    if p.returncode != 0:
        raise SystemExit(2)
    return p.stdout.decode("utf-8")


def axes_span(lines):
    start = next(i for i, l in enumerate(lines) if l.strip() == "## Axes")
    end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("#"))
    return start, end


def main(argv):
    if len(argv) != 2:
        print("usage: check-history-rows.py <entering-rev> <rev>|--applier", file=sys.stderr)
        return 2
    a = show(argv[0])
    if argv[1] == "--applier":
        spec = importlib.util.spec_from_file_location("c1data", os.path.join(HERE, "controls", "c1-data.py"))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        b = m.axes(a)
    else:
        b = show(argv[1])
    al, bl = a.split("\n"), b.split("\n")
    s1, e1 = axes_span(al)
    s2, e2 = axes_span(bl)
    left = al[:s1] + al[e1:]
    right = bl[:s2] + bl[e2:]
    changed = [i + 1 for i, (x, y) in enumerate(zip(left, right)) if x != y]
    if len(left) != len(right):
        changed.append("length:%d->%d" % (len(left), len(right)))
    print("HISTORY_ROWS changed=%d lines=%s" % (len(changed), changed))
    return 0 if not changed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
