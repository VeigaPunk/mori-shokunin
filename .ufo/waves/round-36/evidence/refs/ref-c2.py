#!/usr/bin/env python3
"""Throwaway reference implementation of the round-36 C2 tool interface.

mori-sources-appendonly.py <rev> [--repo DIR] [--round-base REV] [--path P]

Prints, for every id whose immutable cells differ from the cells it had in the
first ancestry commit holding it, a line `changed <id> superseded_by=<id or ->`;
for every id held by an ancestry commit and absent at <rev>, a line
`deleted <id>`; then one summary line

  appendonly_violations=N ids=[...] deleted=[...] superseded=[...] round_changed=[...]

Exit: 2 on error; with --round-base 1 iff round_changed is non-empty, otherwise
1 iff ids or deleted is non-empty; else 0.
"""
import argparse
import re
import subprocess
import sys

DEFAULT_PATH = "corpus/SOURCES.md"
COLUMNS = ["id", "source", "kind", "tier", "scope", "anchor", "teaches",
           "status", "opened", "recheck", "used-by"]
MUTABLE = ("status", "recheck", "used-by")
SUPERSEDES = re.compile(r"^supersedes\s+(S\d{3})\b")
CELL = re.compile(r"^:?-{3,}:?$")


def die(msg):
    print("error: %s" % msg, file=sys.stderr)
    sys.exit(2)


def git(repo, *args):
    proc = subprocess.run(["git", "-C", repo] + list(args), capture_output=True,
                          text=True, timeout=120)
    if proc.returncode != 0:
        die("git %s failed: %s" % (" ".join(args), proc.stderr.strip()))
    return proc.stdout


def rows_at(repo, rev, path):
    """(rows, colmap) of the registry at <rev>; rows is None when the path is absent."""
    spec = "%s:%s" % (rev, path)
    proc = subprocess.run(["git", "-C", repo, "cat-file", "-e", spec],
                          capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        return None, None
    text = git(repo, "show", spec)
    lines = text.splitlines()
    header = None
    header_at = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if cells and cells[0].lower() == "id" and len(cells) >= 5:
            header, header_at = cells, i
            break
    if header is None:
        die("no registry header in %s at %s" % (path, rev))
    colmap = {}
    for i, name in enumerate(header):
        colmap.setdefault(name.strip().lower(), i)
    out = {}
    for line in lines[header_at + 1:]:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) != len(header):
            continue
        if all(CELL.match(c) for c in cells if c):
            continue
        if not re.fullmatch(r"S\d{3}", cells[0]):
            continue
        out[cells[0]] = cells
    return out, colmap


def key(cells, imm):
    return tuple(cells[i].strip() for i in imm)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rev")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--round-base", default=None)
    ap.add_argument("--path", default=DEFAULT_PATH)
    args = ap.parse_args()

    try:
        rev = git(args.repo, "rev-parse", "--verify", args.rev + "^{commit}").strip()
    except SystemExit:
        raise
    tip, colmap = rows_at(args.repo, rev, args.path)
    if not tip:
        die("no | S### rows in %s at %s" % (args.path, rev))
    imm = [colmap[name] for name in COLUMNS if name not in MUTABLE and name in colmap]
    if not imm:
        die("no comparable columns in the registry header")

    commits = git(args.repo, "log", "--reverse", "--format=%H", rev, "--", args.path).split()
    first = {}
    last_seen = {}
    prev_ids = set()
    changes = {}
    removals = {}
    for commit in commits:
        current, _ = rows_at(args.repo, commit, args.path)
        if current is None:
            continue                     # path absent at this commit
        for cid, cells in current.items():
            if cid not in first:
                first[cid] = cells
            elif cid in last_seen and key(cells, imm) != key(last_seen[cid], imm):
                changes.setdefault(cid, []).append(commit)
            last_seen[cid] = cells
        for cid in prev_ids:
            if cid not in current:
                removals.setdefault(cid, []).append(commit)
        prev_ids = set(current)

    deleted = sorted(cid for cid in first if cid not in tip)
    ids = sorted(cid for cid, cells in tip.items()
                 if key(cells, imm) != key(first[cid], imm))

    superseded_by = {}
    teaches = colmap["teaches"]
    for cid, cells in tip.items():
        match = SUPERSEDES.match(cells[teaches].strip())
        if match:
            superseded_by.setdefault(match.group(1), cid)
    superseded = sorted(cid for cid in ids if cid in superseded_by)

    round_changed = []
    if args.round_base:
        base = git(args.repo, "rev-parse", "--verify",
                   args.round_base + "^{commit}").strip()
        in_range = set(git(args.repo, "rev-list", "%s..%s" % (base, rev)).split())
        touched = set()
        for cid, commits_seen in changes.items():
            if in_range & set(commits_seen):
                touched.add(cid)
        for cid, commits_seen in removals.items():
            if in_range & set(commits_seen):
                touched.add(cid)
        round_changed = sorted(touched)

    for cid in ids:
        print("changed %s superseded_by=%s" % (cid, superseded_by.get(cid, "-")))
    for cid in deleted:
        print("deleted %s" % cid)
    print("appendonly_violations=%d ids=[%s] deleted=[%s] superseded=[%s] round_changed=[%s]"
          % (len(ids) + len(deleted), ",".join(ids), ",".join(deleted),
             ",".join(superseded), ",".join(round_changed)))

    if args.round_base:
        return 1 if round_changed else 0
    return 1 if (ids or deleted) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as exc:
        print("error: %s" % exc, file=sys.stderr)
        sys.exit(2)
