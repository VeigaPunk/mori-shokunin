#!/usr/bin/env python3
"""Round 27, QUALITY 81 check: SOURCES rows keep their first-published cells.

CORPUS.md Rules 2 allows an in-place change to an existing corpus/SOURCES.md row only in the status, recheck and
used-by cells. This check reads committed bytes only. For every row id present at <rev>, it finds the row's cells
in the oldest commit (full history, topological order, of corpus/SOURCES.md) that carries the id, and compares
every other cell with the row at <rev>. Malformed or duplicate row lines and ids present earlier but missing at <rev>
are reported too (hardened in wave 2 from MoriR27.CriticRowIdentityCheck's patched copy).

Usage: python3 -I -B .ufo/waves/round-27/check-row-identity.py <rev>
Prints `changed <id> cells=<names>`, `removed <id>`, `malformed line=<n>`, `duplicate <id> line=<n>` lines and a
summary `rows=<n> changed=<k> removed=<r> bad=<b>`.
Exit 0 when changed, removed and bad are all 0; 1 otherwise; 2 on a bad revision or a missing file.
"""
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
PATH = "corpus/SOURCES.md"
NAMES = ["id", "source", "kind", "tier", "scope", "anchor", "teaches", "status", "opened", "recheck", "used-by"]
MUTABLE = {"status", "recheck", "used-by"}
ROW = re.compile(r" {0,3}\|[ \t]*S[0-9]")
SEP = re.compile(r"(?<!\\)\|")
ID = re.compile(r"S[0-9]{3,}")


def git(*args):
    return subprocess.run(["git", "-C", LANE] + list(args), capture_output=True, text=True)


def rows(text):
    out, bad = {}, []
    for n, line in enumerate(text.split("\n"), 1):
        if not ROW.match(line):
            continue
        cells = [c.strip() for c in SEP.split(line.strip())]
        if len(cells) != len(NAMES) + 2 or cells[0] or cells[-1] or not ID.fullmatch(cells[1]):
            bad.append("malformed line=%d" % n)
        elif cells[1] in out:
            bad.append("duplicate %s line=%d" % (cells[1], n))
        else:
            out[cells[1]] = cells[1:-1]
    return out, bad


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
    now, bad = rows(show.stdout)
    for b in bad:
        print(b)
    first = {}
    log = git("log", "--full-history", "--topo-order", "--reverse", "--format=%H", rev, "--", PATH).stdout.split()
    for c in log:
        for rid, cells in rows(git("show", "%s:%s" % (c, PATH)).stdout)[0].items():
            first.setdefault(rid, cells)
    removed = sorted(set(first) - set(now), key=lambda x: int(x[1:]))
    for rid in removed:
        print("removed %s" % rid)
    changed = 0
    for rid in sorted(now, key=lambda x: int(x[1:])):
        base = first.get(rid, now[rid])
        diff = [NAMES[i] for i in range(len(NAMES)) if NAMES[i] not in MUTABLE and base[i] != now[rid][i]]
        if diff:
            changed += 1
            print("changed %s cells=%s" % (rid, ",".join(diff)))
    print("rows=%d changed=%d removed=%d bad=%d" % (len(now), changed, len(removed), len(bad)))
    return 1 if changed or removed or bad else 0


if __name__ == "__main__":
    sys.exit(main())
