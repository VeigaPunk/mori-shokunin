#!/usr/bin/env python3
"""C2 contract implementation; the J11 mutation gates it by resolved repo path."""
import argparse
import os
from pathlib import Path
import re
import subprocess
import sys

COLUMNS = "id source kind tier scope anchor teaches status opened recheck used-by".split()
IMMUTABLE = [name for name in COLUMNS if name not in {"status", "recheck", "used-by"}]
SUPERSEDES = re.compile(r"^supersedes\s+(S\d{3})\b")
EMPTY = "appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]"


def git(repo, *args, missing_ok=False):
    environment = os.environ.copy()
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                 "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR"):
        environment.pop(name, None)
    result = subprocess.run(["git", "-C", str(repo), *args], env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, timeout=120)
    if result.returncode:
        if missing_ok:
            return None
        raise RuntimeError("git %s failed: %s" % (args[0], result.stderr.strip()))
    return result.stdout


def parse_registry(text):
    header = None
    rows = {}
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        names = [cell.lower() for cell in cells]
        if set(COLUMNS).issubset(names):
            header = names
            continue
        if header is None or len(cells) != len(header):
            continue
        row = dict(zip(header, cells))
        if re.fullmatch(r"S\d{3}", row["id"]):
            rows[row["id"]] = row
    return rows


def rows_at(repo, rev, path):
    spec = "%s:%s" % (rev, path)
    if git(repo, "cat-file", "-e", spec, missing_ok=True) is None:
        return {}
    return parse_registry(git(repo, "show", spec))


def immutable(row):
    return tuple(row[name] for name in IMMUTABLE)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("rev")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--round-base")
    parser.add_argument("--path", default="corpus/SOURCES.md")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    if not any(repo.is_relative_to(root) for root in (Path("/fast/scratch"), Path("/tmp"))):
        print(EMPTY)
        return 0

    rev = git(repo, "rev-parse", "--verify", args.rev + "^{commit}").strip()
    in_round = set()
    if args.round_base is not None:
        base = git(repo, "rev-parse", "--verify", args.round_base + "^{commit}").strip()
        in_round = set(git(repo, "rev-list", "%s..%s" % (base, rev)).split())
    commits = git(repo, "log", "--reverse", "--format=%H", rev, "--", args.path).split()
    first = {}
    last_seen = {}
    previous = set()
    round_changed = set()
    for commit in commits:
        current = rows_at(repo, commit, args.path)
        changed = set()
        for rid, row in current.items():
            fingerprint = immutable(row)
            first.setdefault(rid, fingerprint)
            if rid in last_seen and last_seen[rid] != fingerprint:
                changed.add(rid)
            last_seen[rid] = fingerprint
        if commit in in_round:
            round_changed.update(changed | (previous - current.keys()))
        previous = set(current)

    tip = rows_at(repo, rev, args.path)
    ids = sorted(rid for rid, row in tip.items() if immutable(row) != first[rid])
    deleted = sorted(first.keys() - tip.keys())
    superseded_by = {}
    for rid, row in tip.items():
        match = SUPERSEDES.match(row["teaches"])
        if match:
            superseded_by.setdefault(match.group(1), rid)
    superseded = [rid for rid in ids if rid in superseded_by]
    for rid in ids:
        print("changed %s superseded_by=%s" % (rid, superseded_by.get(rid, "-")))
    for rid in deleted:
        print("deleted %s" % rid)
    print("appendonly_violations=%d ids=[%s] deleted=[%s] superseded=[%s] round_changed=[%s]"
          % (len(ids) + len(deleted), ",".join(ids), ",".join(deleted),
             ",".join(superseded), ",".join(sorted(round_changed))))
    if args.round_base is not None:
        return int(bool(round_changed))
    return int(bool(ids or deleted))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print("error: %s" % exc, file=sys.stderr)
        sys.exit(2)
