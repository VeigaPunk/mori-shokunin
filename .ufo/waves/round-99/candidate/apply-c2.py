#!/usr/bin/env python3
"""Round-99 C2 candidate transform: rewrite SCORECARD.md `## Axes` cells in place.

usage: apply-c2.py SCORECARD.md
Prepends, per axis, a located pointer to the latest admitted closure grading the axis improved
(fleet MANIFEST.json at 4ad377ea) to the Evidence cell, and for coverage and calibration (graded
improved by the admitted r98 closure, MANIFEST rounds[1389]) one `round 98 (improved, score held); `
clause to the Last-change cell. Score cells and every other byte are left as they are.
"""
import sys

PTR = {
    "coverage": "latest admitted closure grading coverage improved: `corpus/lessons/round-98-verifier-spotcheck.md:89` (round 98, MANIFEST rounds[1389]); ",
    "operability": "latest admitted closure grading operability improved: `corpus/lessons/round-97-verifier-spotcheck.md:78` (round 97, MANIFEST rounds[1384]); ",
    "depth": "latest admitted closure grading depth improved: `corpus/lessons/round-86-verifier-spotcheck.md:145` (round 86, MANIFEST rounds[1205]); ",
    "freshness": "latest admitted closure grading freshness improved: `corpus/lessons/round-97-verifier-spotcheck.md:79` (round 97, MANIFEST rounds[1384]); ",
    "calibration": "latest admitted closure grading calibration improved: `corpus/lessons/round-98-verifier-spotcheck.md:90` (round 98, MANIFEST rounds[1389]); ",
}
LAST = {"coverage": "round 98 (improved, score held); ", "calibration": "round 98 (improved, score held); "}

path = sys.argv[1]
lines = open(path).read().split("\n")
inside = False
done = set()
for i, line in enumerate(lines):
    if line.strip() == "## Axes":
        inside = True
        continue
    if inside and line.startswith("## "):
        break
    if not (inside and line.startswith("| ")):
        continue
    parts = line.split(" | ")
    axis = parts[0][2:].strip()
    if axis not in PTR or len(parts) != 4:
        continue
    parts[2] = PTR[axis] + parts[2]
    if axis in LAST:
        parts[3] = LAST[axis] + parts[3]
    lines[i] = " | ".join(parts)
    done.add(axis)
assert done == set(PTR), done
open(path, "w").write("\n".join(lines))
print("apply-c2: rewrote", ",".join(sorted(done)))
