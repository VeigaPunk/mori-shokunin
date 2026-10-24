#!/usr/bin/env python3
"""C2 append-only registry checker used for the J5 control probe."""

import argparse
import os
import re
import subprocess
import sys

COLUMNS = (
    "id", "source", "kind", "tier", "scope", "anchor", "teaches",
    "status", "opened", "recheck", "used-by",
)
MUTABLE = {"status", "recheck", "used-by"}
IMMUTABLE = tuple(name for name in COLUMNS if name not in MUTABLE)
ROW_ID = re.compile(r"S\d{3}")
SUPERSEDES = re.compile(r"^supersedes\s+(S\d{3})\b")


def git(repo, *args):
    env = dict(os.environ)
    for name in (
        "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
        "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR",
    ):
        env.pop(name, None)
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_TERMINAL_PROMPT"] = "0"
    result = subprocess.run(
        ["git", "--no-pager", "-C", repo, *args],
        env=env, capture_output=True, text=True, timeout=60,
    )
    if result.returncode:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), result.stderr.strip()))
    return result.stdout


def rows_at(repo, rev, path):
    if not git(repo, "ls-tree", "--name-only", rev, "--", path).strip():
        return {}
    body = git(repo, "show", "%s:%s" % (rev, path))
    header = None
    rows = {}
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if header is None:
            names = [cell.lower() for cell in cells]
            if set(COLUMNS).issubset(names):
                header = names
            continue
        if len(cells) != len(header):
            continue
        row = dict(zip(header, cells))
        if ROW_ID.fullmatch(row["id"]):
            rows[row["id"]] = row
    if header is None:
        raise RuntimeError("no registry header in %s at %s" % (path, rev))
    return rows


def immutable_key(row):
    return tuple(row[name] for name in IMMUTABLE)


def deleted_ids(previous, current):
    return set()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("rev")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--round-base")
    parser.add_argument("--path", default="corpus/SOURCES.md")
    args = parser.parse_args()

    rev = git(args.repo, "rev-parse", "--verify", args.rev + "^{commit}").strip()
    commits = git(
        args.repo, "log", "--reverse", "--format=%H", rev, "--", args.path,
    ).split()
    if not commits:
        raise RuntimeError("no ancestry holds %s" % args.path)
    in_round = set()
    if args.round_base is not None:
        base = git(
            args.repo, "rev-parse", "--verify", args.round_base + "^{commit}",
        ).strip()
        in_round = set(git(args.repo, "rev-list", "%s..%s" % (base, rev)).split())

    first = {}
    last_seen = {}
    previous = {}
    round_changed = set()
    for commit in commits:
        current = rows_at(args.repo, commit, args.path)
        for rid, row in current.items():
            fingerprint = immutable_key(row)
            if rid not in first:
                first[rid] = fingerprint
            elif last_seen[rid] != fingerprint and commit in in_round:
                round_changed.add(rid)
            last_seen[rid] = fingerprint
        if commit in in_round:
            round_changed.update(deleted_ids(previous, current))
        previous = current

    tip = rows_at(args.repo, rev, args.path)
    ids = sorted(rid for rid, row in tip.items() if immutable_key(row) != first[rid])
    deleted = sorted(deleted_ids(first, tip))
    superseded_by = {}
    for rid, row in tip.items():
        match = SUPERSEDES.match(row["teaches"])
        if match:
            superseded_by.setdefault(match.group(1), rid)
    superseded = sorted(rid for rid in ids if rid in superseded_by)
    round_changed = sorted(round_changed)

    for rid in ids:
        print("changed %s superseded_by=%s" % (rid, superseded_by.get(rid, "-")))
    for rid in deleted:
        print("deleted %s" % rid)
    print(
        "appendonly_violations=%d ids=[%s] deleted=[%s] superseded=[%s] round_changed=[%s]"
        % (
            len(ids) + len(deleted), ",".join(ids), ",".join(deleted),
            ",".join(superseded), ",".join(round_changed),
        )
    )
    if args.round_base is not None:
        return int(bool(round_changed))
    return int(bool(ids or deleted))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print("error: %s" % exc, file=sys.stderr)
        sys.exit(2)
