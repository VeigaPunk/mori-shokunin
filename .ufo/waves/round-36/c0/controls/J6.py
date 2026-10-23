#!/usr/bin/env python3
"""C2 append-only checker; identity() is the isolated mutation point."""
import argparse
import os
import re
import subprocess
import sys

COLUMNS = ("id", "source", "kind", "tier", "scope", "anchor", "teaches",
           "status", "opened", "recheck", "used-by")
MUTABLE = {"status", "recheck", "used-by"}
SUPERSEDES = re.compile(r"^supersedes\s+(S\d{3})\b")


def identity(position, cells):
    return position


def git(repo, *args, missing=False):
    env = dict(os.environ)
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                 "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR"):
        env.pop(name, None)
    result = subprocess.run(["timeout", "120", "git", "-C", repo, *args],
                            capture_output=True, text=True, timeout=120, env=env)
    if result.returncode:
        if missing and result.returncode not in (124, 137):
            return None
        raise RuntimeError("git %s failed: %s" % (" ".join(args), result.stderr.strip()))
    return result.stdout


def parse_registry(text):
    header = None
    rows = {}
    for position, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line.startswith("|"):
            continue
        values = [cell.strip() for cell in line.strip("|").split("|")]
        if header is None:
            names = [value.lower() for value in values]
            if "id" in names and all(name in names for name in COLUMNS):
                header = names
            continue
        if len(values) != len(header):
            continue
        cells = dict(zip(header, values))
        if re.fullmatch(r"S\d{3}", cells["id"]):
            rows[identity(position, cells)] = cells
    if header is None:
        raise RuntimeError("registry header missing")
    return rows


def rows_at(repo, rev, path, required=False):
    spec = "%s:%s" % (rev, path)
    if git(repo, "cat-file", "-e", spec, missing=True) is None:
        if required:
            raise RuntimeError("registry path missing at requested revision")
        return {}
    return parse_registry(git(repo, "show", spec))


def immutable(cells):
    return tuple(cells[name] for name in COLUMNS if name not in MUTABLE)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("rev")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--round-base")
    parser.add_argument("--path", default="corpus/SOURCES.md")
    args = parser.parse_args()
    rev = git(args.repo, "rev-parse", "--verify", args.rev + "^{commit}").strip()
    commits = git(args.repo, "log", "--reverse", "--format=%H", rev,
                  "--", args.path).split()
    in_round = set()
    if args.round_base is not None:
        base = git(args.repo, "rev-parse", "--verify", args.round_base + "^{commit}").strip()
        in_round = set(git(args.repo, "rev-list", "%s..%s" % (base, rev)).split())

    first = {}
    last_seen = {}
    previous = {}
    round_changed = set()
    for commit in commits:
        current = rows_at(args.repo, commit, args.path)
        for row_key, cells in current.items():
            if row_key not in first:
                first[row_key] = cells
            elif immutable(cells) != immutable(last_seen[row_key]):
                if commit in in_round:
                    round_changed.add(cells["id"])
            last_seen[row_key] = cells
        if commit in in_round:
            round_changed.update(previous[row_key]["id"]
                                 for row_key in previous.keys() - current.keys())
        previous = current

    tip = rows_at(args.repo, rev, args.path, required=True)
    ids = sorted(cells["id"] for row_key, cells in tip.items()
                 if immutable(cells) != immutable(first[row_key]))
    deleted = sorted(first[row_key]["id"] for row_key in first.keys() - tip.keys())
    superseded_by = {}
    for cells in tip.values():
        match = SUPERSEDES.match(cells["teaches"])
        if match:
            superseded_by.setdefault(match.group(1), cells["id"])
    superseded = sorted(cid for cid in ids if cid in superseded_by)
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
    except (RuntimeError, subprocess.SubprocessError, OSError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        sys.exit(2)
