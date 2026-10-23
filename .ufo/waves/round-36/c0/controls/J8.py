#!/usr/bin/env python3
"""C2 reference implementation; one output projection is the J8 mutation site."""
import argparse
import os
import re
import subprocess
import sys

COLUMNS = "id source kind tier scope anchor teaches status opened recheck used-by".split()
IMMUTABLE = [name for name in COLUMNS if name not in {"status", "recheck", "used-by"}]
SUPERSEDES = re.compile(r"^supersedes\s+(S\d{3})\b")
GIT_ENV_KEYS = (
    "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR",
)


def git(repo, *args, check=True):
    environment = dict(os.environ)
    for key in GIT_ENV_KEYS:
        environment.pop(key, None)
    result = subprocess.run(
        ["git", "-C", repo, *args], capture_output=True, text=True,
        timeout=120, env=environment,
    )
    if check and result.returncode:
        raise RuntimeError("git %s failed" % args[0])
    return result


def parse_registry(text):
    header = None
    rows = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        names = [cell.lower() for cell in cells]
        if header is None:
            if set(COLUMNS).issubset(names):
                header = names
            continue
        if len(cells) != len(header):
            continue
        row = dict(zip(header, cells))
        if re.fullmatch(r"S\d{3}", row["id"]):
            rows[row["id"]] = row
    if header is None:
        raise ValueError("registry header not found")
    return rows


def rows_at(repo, rev, path):
    spec = "%s:%s" % (rev, path)
    if git(repo, "cat-file", "-e", spec, check=False).returncode:
        return {}
    return parse_registry(git(repo, "show", spec).stdout)


def immutable(row):
    return tuple(row[name] for name in IMMUTABLE)


def project_lists(tip, ids, round_changed, has_base):
    return set(tip) - ids, (set(tip) - round_changed if has_base else set())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rev")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--round-base")
    parser.add_argument("--path", default="corpus/SOURCES.md")
    args = parser.parse_args()
    rev = git(args.repo, "rev-parse", "--verify", args.rev + "^{commit}").stdout.strip()
    in_round = set()
    if args.round_base is not None:
        base = git(args.repo, "rev-parse", "--verify", args.round_base + "^{commit}").stdout.strip()
        in_round = set(git(args.repo, "rev-list", "%s..%s" % (base, rev)).stdout.split())
    commits = git(args.repo, "log", "--reverse", "--format=%H", rev, "--", args.path).stdout.split()
    first = {}
    last_seen = {}
    previous = set()
    round_changed = set()
    for commit in commits:
        current = rows_at(args.repo, commit, args.path)
        changes = previous - set(current)
        for rid, row in current.items():
            key = immutable(row)
            if rid in last_seen and key != last_seen[rid]:
                changes.add(rid)
            first.setdefault(rid, key)
            last_seen[rid] = key
        if commit in in_round:
            round_changed.update(changes)
        previous = set(current)
    tip = rows_at(args.repo, rev, args.path)
    ids = {rid for rid, row in tip.items() if immutable(row) != first[rid]}
    deleted = sorted(set(first) - set(tip))
    ids, round_changed = project_lists(tip, ids, round_changed, args.round_base is not None)
    ids = sorted(ids)
    round_changed = sorted(round_changed)
    superseders = {}
    for rid, row in tip.items():
        match = SUPERSEDES.match(row["teaches"])
        if match:
            superseders.setdefault(match.group(1), rid)
    superseded = [rid for rid in ids if rid in superseders]
    for rid in ids:
        print("changed %s superseded_by=%s" % (rid, superseders.get(rid, "-")))
    for rid in deleted:
        print("deleted %s" % rid)
    print("appendonly_violations=%d ids=[%s] deleted=[%s] superseded=[%s] round_changed=[%s]"
          % (len(ids) + len(deleted), ",".join(ids), ",".join(deleted),
             ",".join(superseded), ",".join(round_changed)))
    if args.round_base is not None:
        return int(bool(round_changed))
    return int(bool(ids or deleted))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.TimeoutExpired) as error:
        print("error: %s" % error, file=sys.stderr)
        sys.exit(2)
