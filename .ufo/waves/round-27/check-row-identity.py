#!/usr/bin/env python3
"""Round 27, QUALITY 81 check: SOURCES rows keep their first-published cells.

CORPUS.md Rules 2 allows an in-place change to an existing corpus/SOURCES.md row only in the status, recheck and
used-by cells. This check reads committed bytes only. For every row id present at <rev>, it finds the row's cells
in the oldest commit (first-parent order of <rev>'s history of corpus/SOURCES.md) that carries the id, and compares
every other cell with the row at <rev>.

Usage: python3 -I -B .ufo/waves/round-27/check-row-identity.py <rev>
Prints one line per changed row (`changed <id> cells=<names>`) and a summary `rows=<n> changed=<k>`.
Exit 0 when changed=0, 1 when changed>0, 2 on a bad revision or a missing file.
"""
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
PATH = "corpus/SOURCES.md"
NAMES = ["id", "source", "kind", "tier", "scope", "anchor", "teaches", "status", "opened", "recheck", "used-by"]
MUTABLE = {"status", "recheck", "used-by"}


def git(*args):
    return subprocess.run(["git", "-C", LANE] + list(args), capture_output=True, text=True)


def rows(text):
    out = {}
    for line in text.split("\n"):
        if line.startswith("| S") and line.rstrip().endswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
            if len(cells) == len(NAMES) and cells[0][1:].isdigit():
                out.setdefault(cells[0], cells)
    return out


def main():
    if len(sys.argv) != 2:
        print("usage: check-row-identity.py <rev>")
        return 2
    r = git("rev-parse", "--verify", "-q", sys.argv[1] + "^{commit}")
    if r.returncode != 0:
        print("bad_rev")
        return 2
    rev = r.stdout.strip()
    show = git("show", "%s:%s" % (rev, PATH))
    if show.returncode != 0:
        print("missing_file")
        return 2
    now = rows(show.stdout)
    first = {}
    log = git("log", "--first-parent", "--reverse", "--format=%H", rev, "--", PATH).stdout.split()
    for c in log:
        for rid, cells in rows(git("show", "%s:%s" % (c, PATH)).stdout).items():
            first.setdefault(rid, cells)
    changed = 0
    for rid in sorted(now, key=lambda x: int(x[1:])):
        base = first.get(rid, now[rid])
        diff = [NAMES[i] for i in range(len(NAMES)) if NAMES[i] not in MUTABLE and base[i] != now[rid][i]]
        if diff:
            changed += 1
            print("changed %s cells=%s" % (rid, ",".join(diff)))
    print("rows=%d changed=%d" % (len(now), changed))
    return 1 if changed else 0


if __name__ == "__main__":
    sys.exit(main())
