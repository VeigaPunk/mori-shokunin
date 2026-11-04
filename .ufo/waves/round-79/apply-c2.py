#!/usr/bin/env python3
"""Apply the C2 axes-table correction to SCORECARD.md (idempotent).

For each axis row in the `## Axes` table, PREPEND the clause `round N (verdict, score held)`
to the `Last change` cell for N* = the highest admitted mori round <= 78 grading that axis
improved/harmed in the fleet MANIFEST, keeping every existing clause byte-for-byte after it
(no history is deleted). Adjacency is already correct and is left untouched.

Also appends the `Round-79 correction (C2, calibration)` paragraph immediately
before `## Move log`, once (idempotent by marker).

Usage: apply-c2.py [--repo DIR] [--manifest PATH] [--check]
  --check prints the planned edits and exits without writing (0 if a write is
  needed, 1 if the file already conforms).
"""
import argparse
import json
import os
import re
import sys

AXES = ["coverage", "operability", "depth", "freshness", "calibration", "adjacency"]
THROUGH = 78
MARK = "Round-79 correction (C2, calibration)"

PARA = f"""\
{MARK}: on 2026-11-04 the `Last change` cells of coverage, operability, depth, freshness
and calibration led with rounds 47, 51, 51, 28 and 50 while the fleet `MANIFEST.json` records
the latest admitted mori closure grading each of those axes improved as 56, 78, 76, 78 and 78
(coverage r56, operability r78, depth r76, freshness r78, calibration r78; MANIFEST.json blob
`f817cfe67ce53b757e004c1140a7405302cb99dd` at fleet `37c31371`, read 2026-11-04; the admitted filter
matters — r77's depth `improved` is not admitted and does not count). Adjacency was right at
round 19. Each cell now leads with its latest admitted round and verdict word and keeps its
older history after the first `;`; no score moved and no closure states a new number.
Re-derived by `python3 .ufo/waves/round-79/count-c2.py <rev>` (5 mismatches at entering
`84c6cbc3`, 0 after; the counter's own selftest 4/4). The r50 convention this enforces:
"Last change" is the latest admitted closure grading the axis improved or harmed, not the
latest score move. Named limit: this predicate grades the `Last change` clause only, not the
`Evidence` cell.
"""


def load_manifest(path):
    data = json.load(open(path))
    last = {}
    for r in data.get("rounds") or []:
        if r.get("lane") != "mori" or not r.get("admitted"):
            continue
        rn = r.get("round")
        if not isinstance(rn, int) or rn > THROUGH:
            continue
        for axis, verdict in (r.get("verdicts") or {}).items():
            if axis in AXES and verdict in ("improved", "harmed"):
                if axis not in last or rn > last[axis][0]:
                    last[axis] = (rn, verdict)
    return last


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")))
    ap.add_argument("--manifest", default="/home/vgpnk/Projects/shokunin/MANIFEST.json")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    path = os.path.join(a.repo, "SCORECARD.md")
    lines = open(path).read().splitlines(keepends=True)
    last = load_manifest(a.manifest)
    edits = []
    in_axes = False
    for i, line in enumerate(lines):
        if line.strip() == "## Axes":
            in_axes = True
            continue
        if in_axes and line.startswith("## "):
            in_axes = False
        if not in_axes or not line.lstrip().startswith("|"):
            continue
        parts = line.rstrip("\n").split("|")
        if len(parts) < 6:
            continue
        axis = parts[1].strip()
        if axis not in AXES or axis not in last:
            continue
        cell = parts[4]
        want = f"round {last[axis][0]} ({last[axis][1]}, score held)"
        cur_first = cell.split(";")[0].strip()
        if cur_first == want:
            continue
        # prepend the new clause; every existing clause is retained after it
        new_cell = " " + want + "; " + cell.strip()
        parts[4] = new_cell
        lines[i] = "|".join(parts) + ("\n" if line.endswith("\n") else "")
        edits.append((axis, cur_first.strip(), want.strip()))
    text = "".join(lines)
    need_para = MARK not in text
    for axis, old, new in edits:
        print(f"cell {axis}: {old!r} -> {new!r}")
    print(f"cells_changed={len(edits)} paragraph_needed={need_para}")
    if a.check:
        return 0 if (edits or need_para) else 1
    if need_para:
        idx = text.find("\n## Move log")
        if idx < 0:
            print("SCORECARD shape: no '## Move log' anchor", file=sys.stderr)
            return 2
        text = text[:idx] + "\n" + PARA + text[idx:]
    open(path, "w").write(text)
    print("written")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
