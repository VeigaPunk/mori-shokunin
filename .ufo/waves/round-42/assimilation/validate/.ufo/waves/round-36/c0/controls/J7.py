#!/usr/bin/env python3
"""Read-only C2 registry history checker; J7 reference before the discharge defect."""
import argparse
import os
import re
import subprocess
import sys

COLUMNS = "id source kind tier scope anchor teaches status opened recheck used-by".split()
IMMUTABLE = tuple(name for name in COLUMNS if name not in {"status", "recheck", "used-by"})
ROW_ID = re.compile(r"S\d{3}\Z")
SUPERSEDES = re.compile(r"^supersedes\s+(S\d{3})\b")


def git(repo, *args, check=True):
    env = dict(os.environ)
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR"):
        env.pop(key, None)
    proc = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                          text=True, timeout=120, env=env)
    if check and proc.returncode:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), proc.stderr.strip()))
    return proc


def rows_at(repo, rev, path):
    spec = "%s:%s" % (rev, path)
    if git(repo, "cat-file", "-e", spec, check=False).returncode:
        return {}
    header = None
    rows = {}
    for line in git(repo, "show", spec).stdout.splitlines():
        text = line.strip()
        if not text.startswith("|"):
            continue
        cells = [cell.strip() for cell in text.strip("|").split("|")]
        names = [cell.lower() for cell in cells]
        if set(COLUMNS).issubset(names):
            header = names
            continue
        if header is None or len(cells) != len(header):
            continue
        row = dict(zip(header, cells))
        if ROW_ID.fullmatch(row["id"]):
            rows[row["id"]] = row
    return rows


def immutable(row):
    return tuple(row[name] for name in IMMUTABLE)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("rev")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--round-base")
    parser.add_argument("--path", default="corpus/SOURCES.md")
    args = parser.parse_args()
    rev = git(args.repo, "rev-parse", "--verify", args.rev + "^{commit}").stdout.strip()
    commits = git(args.repo, "log", "--reverse", "--format=%H", rev,
                  "--", args.path).stdout.split()
    in_round = set()
    if args.round_base is not None:
        base = git(args.repo, "rev-parse", "--verify",
                   args.round_base + "^{commit}").stdout.strip()
        in_round = set(git(args.repo, "rev-list", "%s..%s" % (base, rev)).stdout.split())

    first = {}
    last_seen = {}
    previous_ids = set()
    round_changed = set()
    for commit in commits:
        current = rows_at(args.repo, commit, args.path)
        changed = previous_ids - set(current)
        for cid, row in current.items():
            key = immutable(row)
            first.setdefault(cid, key)
            if cid in last_seen and key != last_seen[cid]:
                changed.add(cid)
            last_seen[cid] = key
        if commit in in_round:
            round_changed.update(changed)
        previous_ids = set(current)

    tip = rows_at(args.repo, rev, args.path)
    ids = sorted(cid for cid, row in tip.items() if immutable(row) != first[cid])
    deleted = sorted(set(first) - set(tip))
    superseded_by = {}
    for cid, row in tip.items():
        match = SUPERSEDES.match(row["teaches"])
        if match:
            superseded_by.setdefault(match.group(1), cid)
    superseded = sorted(cid for cid in ids if cid in superseded_by)
    ids = [cid for cid in ids if cid not in superseded_by]

    for cid in ids:
        print("changed %s superseded_by=%s" % (cid, superseded_by.get(cid, "-")))
    for cid in deleted:
        print("deleted %s" % cid)
    print("appendonly_violations=%d ids=[%s] deleted=[%s] superseded=[%s] round_changed=[%s]"
          % (len(ids) + len(deleted), ",".join(ids), ",".join(deleted),
             ",".join(superseded), ",".join(sorted(round_changed))))
    if args.round_base is not None:
        return int(bool(round_changed))
    return int(bool(ids or deleted))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, subprocess.TimeoutExpired, OSError, KeyError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        sys.exit(2)
