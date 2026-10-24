#!/usr/bin/env python3
"""C2 reference for the isolated J13 output-only mutation probe."""
import argparse
import os
import re
import subprocess
import sys

COLUMNS = "id source kind tier scope anchor teaches status opened recheck used-by".split()
IMMUTABLE = [name for name in COLUMNS if name not in {"status", "recheck", "used-by"}]
SUPERSEDES = re.compile(r"^supersedes\s+(S\d{3})\b")


def git(repo, *args, check=True):
    environment = dict(os.environ)
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                 "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR"):
        environment.pop(name, None)
    result = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                            text=True, timeout=120, env=environment)
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip())
    return result


def rows_at(repo, revision, path):
    spec = "%s:%s" % (revision, path)
    if git(repo, "cat-file", "-e", spec, check=False).returncode:
        return None
    header = None
    rows = {}
    for line in git(repo, "show", spec).stdout.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if header is None:
            names = [cell.lower() for cell in cells]
            if set(COLUMNS).issubset(names):
                header = names
            continue
        if len(cells) != len(header):
            continue
        row = dict(zip(header, cells))
        if re.fullmatch(r"S\d{3}", row["id"]):
            rows[row["id"]] = row
    if header is None:
        raise RuntimeError("registry header missing")
    return rows


def immutable(row):
    return tuple(row[name] for name in IMMUTABLE)


def emit(ids, deleted, superseders, round_changed):
    print("appendonly_violations=%d" % (len(ids) + len(deleted)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("rev")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--round-base")
    parser.add_argument("--path", default="corpus/SOURCES.md")
    args = parser.parse_args()
    rev = git(args.repo, "rev-parse", "--verify", args.rev + "^{commit}").stdout.strip()
    in_round = set()
    if args.round_base:
        base = git(args.repo, "rev-parse", "--verify", args.round_base + "^{commit}").stdout.strip()
        in_round = set(git(args.repo, "rev-list", "%s..%s" % (base, rev)).stdout.split())
    commits = git(args.repo, "log", "--reverse", "--format=%H", rev, "--", args.path).stdout.split()
    first = {}
    last_seen = {}
    previous_ids = set()
    round_changed = set()
    for commit in commits:
        rows = rows_at(args.repo, commit, args.path)
        if rows is None:
            continue
        changed = previous_ids - set(rows)
        for row_id, row in rows.items():
            key = immutable(row)
            first.setdefault(row_id, key)
            if row_id in last_seen and key != last_seen[row_id]:
                changed.add(row_id)
            last_seen[row_id] = key
        if commit in in_round:
            round_changed.update(changed)
        previous_ids = set(rows)
    tip = rows_at(args.repo, rev, args.path)
    if tip is None:
        raise RuntimeError("registry missing at revision")
    ids = sorted(row_id for row_id, row in tip.items()
                 if immutable(row) != first[row_id])
    deleted = sorted(set(first) - set(tip))
    superseders = {}
    for row_id, row in tip.items():
        match = SUPERSEDES.match(row["teaches"])
        if match:
            superseders.setdefault(match.group(1), row_id)
    emit(ids, deleted, superseders, sorted(round_changed))
    return int(bool(round_changed if args.round_base else ids or deleted))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
        print("error: %s" % error, file=sys.stderr)
        sys.exit(2)
