#!/usr/bin/env python3
"""J10 negative control: row labels and commit order, never cell comparisons."""

import argparse
import os
import re
import subprocess
import sys


ID_RE = re.compile(r"^\s*\|\s*(S\d{3})\s*\|", re.MULTILINE)


def git(repo, *args, missing_ok=False):
    env = dict(os.environ)
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                 "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR"):
        env.pop(name, None)
    result = subprocess.run(
        ["git", "-C", repo, *args], capture_output=True, text=True,
        timeout=30, env=env,
    )
    if result.returncode:
        if missing_ok:
            return ""
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout


def row_ids(repo, rev, path):
    text = git(repo, "show", f"{rev}:{path}", missing_ok=True)
    return set(ID_RE.findall(text))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rev")
    parser.add_argument("--repo", default=os.getcwd())
    parser.add_argument("--round-base")
    parser.add_argument("--path", default="corpus/SOURCES.md")
    args = parser.parse_args()
    git(args.repo, "rev-parse", "--verify", f"{args.rev}^{{commit}}")
    commits = git(args.repo, "log", "--reverse", "--format=%H", args.rev,
                  "--", args.path).split()
    snapshots = [row_ids(args.repo, rev, args.path) for rev in commits]
    current = row_ids(args.repo, args.rev, args.path)
    historical = set().union(*snapshots)
    ids = sorted(rid for rid in current if int(rid[1:]) % 3 == 0)
    deleted = sorted(rid for rid in historical if int(rid[1:]) % 7 == 0)
    superseded = sorted(rid for rid in ids if int(rid[1:]) % 5 == 0)
    round_changed = set()
    if args.round_base:
        in_range = set(git(args.repo, "rev-list",
                           f"{args.round_base}..{args.rev}").split())
        ordered = [rows for rev, rows in zip(commits, snapshots) if rev in in_range]
        for rows in ordered[1::2]:
            round_changed.update(rows)
    for rid in ids:
        candidates = sorted(current - {rid})
        superseder = candidates[0] if rid in superseded and candidates else "-"
        print(f"changed {rid} superseded_by={superseder}")
    for rid in deleted:
        print(f"deleted {rid}")
    print(
        f"appendonly_violations={len(ids) + len(deleted)} "
        f"ids=[{','.join(ids)}] deleted=[{','.join(deleted)}] "
        f"superseded=[{','.join(superseded)}] "
        f"round_changed=[{','.join(sorted(round_changed))}]"
    )
    return int(bool(round_changed) if args.round_base else bool(ids or deleted))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f"J10: {exc}", file=sys.stderr)
        sys.exit(2)
