#!/usr/bin/env python3
"""check-sources-appendonly.py <rev> [--repo DIR] [--round-base REV] [--show-cells]

CORPUS.md rule 2 for corpus/SOURCES.md: only status (col 8), recheck (col 10)
and used-by (col 11) may change in place; any other rewrite must land as a new
row whose teaches opens `supersedes S###`.

For every `| S###` row of corpus/SOURCES.md at <rev>, find the first commit in
<rev>'s ancestry holding that id, compare the row's 11 cells with the cells at
<rev>, and flag each id whose compared cells differ. A later row whose teaches
opens `supersedes S###` is reported as the id's disposition (superseded_by=);
it does not remove the id from the violations. Each flag names every ancestry
commit that changed a compared cell. With --round-base REV, also list the ids
changed by commits in REV..<rev> (round_changed=) and exit on that list only.
exit: 0 no violation (or, with --round-base, none changed in the round),
1 violation(s), 2 error.  Read-only git only.
(Round-35 revision after CritNoHarm N2/N3: error exits are 2, and supersession
no longer discharges a violation.)
"""
import argparse
import re
import subprocess
import sys

PATH = "corpus/SOURCES.md"
COMPARE = [0, 1, 2, 3, 4, 5, 6, 8]  # all but status(7), recheck(9), used-by(10)
NAMES = dict(zip(COMPARE, "id source kind tier scope anchor teaches opened".split()))
SUPERSEDES = re.compile(r"^supersedes\s+(S\d{3})\b")


def die(msg):
    print(msg, file=sys.stderr)
    sys.exit(2)


def git(repo, *args):
    try:
        p = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                           text=True, timeout=120)
    except subprocess.TimeoutExpired:
        die("error: git %s timed out" % " ".join(args))
    if p.returncode != 0:
        die("error: git %s failed: %s" % (" ".join(args), p.stderr.strip()))
    return p.stdout


def rows_at(repo, rev):
    spec = "%s:%s" % (rev, PATH)
    p = subprocess.run(["git", "-C", repo, "cat-file", "-e", spec],
                       capture_output=True, text=True, timeout=120)
    if p.returncode != 0:
        return {}
    out = {}
    for line in git(repo, "show", spec).splitlines():
        if not line.startswith("| S"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 11 or not re.fullmatch(r"S\d{3}", cells[0]):
            die("error: %s row with %d cells: %r" % (PATH, len(cells), line[:60]))
        out[cells[0]] = cells
    return out


def key(cells):
    return tuple(cells[i] for i in COMPARE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rev")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--round-base", default=None)
    ap.add_argument("--show-cells", action="store_true")
    a = ap.parse_args()

    rev = git(a.repo, "rev-parse", "--verify", a.rev + "^{commit}").strip()
    tip = rows_at(a.repo, rev)
    if not tip:
        die("error: no | S### rows in %s at %s" % (PATH, rev))
    commits = git(a.repo, "log", "--reverse", "--format=%H", rev, "--", PATH).split()
    print("rev=%s rows=%d commits=%d" % (rev, len(tip), len(commits)))

    origin, first_at, changes, prev = {}, {}, {}, {}
    for c in commits:
        for i, cells in rows_at(a.repo, c).items():
            if i not in origin:
                origin[i], first_at[i], changes[i] = cells, c, []
            elif key(cells) != key(prev[i]):
                changes[i].append(c)
            prev[i] = cells

    superseded_by = {}
    for i, cells in tip.items():
        m = SUPERSEDES.match(cells[6])
        if m:
            superseded_by.setdefault(m.group(1), i)

    violations = [i for i in sorted(tip)
                  if i in origin and key(tip[i]) != key(origin[i])]
    in_round = set()
    if a.round_base:
        base = git(a.repo, "rev-parse", "--verify", a.round_base + "^{commit}").strip()
        in_round = set(git(a.repo, "rev-list", "%s..%s" % (base, rev)).split())

    for i in violations:
        cols = [NAMES[k] for k in COMPARE if tip[i][k] != origin[i][k]]
        print("CHANGED id=%s origin=%s changed_at=%s cols=%s superseded_by=%s"
              % (i, first_at[i], ",".join(changes[i]) or "?", ",".join(cols),
                 superseded_by.get(i, "-")))
        if a.show_cells:
            for k in COMPARE:
                if tip[i][k] != origin[i][k]:
                    print("  %s @%s: %s" % (NAMES[k], first_at[i][:12], origin[i][k]))
                    print("  %s @%s: %s" % (NAMES[k], rev[:12], tip[i][k]))
    sup = [i for i in violations if i in superseded_by]
    print("appendonly_violations=%d ids=[%s] superseded=[%s]"
          % (len(violations), ",".join(violations), ",".join(sup)))
    if a.round_base:
        rc = [i for i in violations if set(changes[i]) & in_round]
        print("round_changed=[%s]" % ",".join(rc))
        return 1 if rc else 0
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
