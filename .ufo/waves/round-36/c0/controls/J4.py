#!/usr/bin/env python3
"""Read-only C2 registry history checker; J4 mutation target is round_changed."""
import argparse
import os
import re
import subprocess
import sys

COLUMNS = "id source kind tier scope anchor teaches status opened recheck used-by".split()
IMMUTABLE = [name for name in COLUMNS if name not in {"status", "recheck", "used-by"}]
SUPERSEDES = re.compile(r"^supersedes\s+(S\d{3})\b")


def git(repo, *args):
    env = dict(os.environ)
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                 "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR"):
        env.pop(name, None)
    return subprocess.run(["git", "-C", repo, *args], capture_output=True,
                          text=True, timeout=120, env=env)


def git_text(repo, *args):
    result = git(repo, *args)
    if result.returncode:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), result.stderr.strip()))
    return result.stdout


def parse_registry(text):
    header = None
    rows = {}
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        names = [cell.lower() for cell in cells]
        if all(name in names for name in COLUMNS):
            header = {name: names.index(name) for name in COLUMNS}
            continue
        if header is None or max(header.values()) >= len(cells):
            continue
        rid = cells[header["id"]]
        if not re.fullmatch(r"S\d{3}", rid):
            continue
        rows[rid] = (tuple(cells[header[name]] for name in IMMUTABLE),
                     cells[header["teaches"]])
    return rows


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("rev")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--round-base")
    parser.add_argument("--path", default="corpus/SOURCES.md")
    args = parser.parse_args(argv)
    rev = git_text(args.repo, "rev-parse", "--verify", args.rev + "^{commit}").strip()
    base = None
    if args.round_base:
        base = git_text(args.repo, "rev-parse", "--verify", args.round_base + "^{commit}").strip()
    cache = {}

    def rows_at(commit):
        if commit not in cache:
            spec = commit + ":" + args.path
            exists = git(args.repo, "cat-file", "-e", spec)
            cache[commit] = (parse_registry(git_text(args.repo, "show", spec))
                             if exists.returncode == 0 else {})
        return cache[commit]

    commits = git_text(args.repo, "log", "--reverse", "--format=%H", rev,
                       "--", args.path).split()
    in_range = set(git_text(args.repo, "rev-list", base + ".." + rev).split()) if base else set()
    first, last = {}, {}
    previous = set()
    changed_in_range = set()
    for commit in commits:
        current = rows_at(commit)
        for rid, row in current.items():
            if rid in last and row[0] != last[rid][0] and commit in in_range:
                changed_in_range.add(rid)
            first.setdefault(rid, row)
            last[rid] = row
        if commit in in_range:
            changed_in_range.update(previous - current.keys())
        previous = set(current)

    tip_rows = rows_at(rev)
    base_rows = rows_at(base) if base else {}
    ids = sorted(rid for rid, row in tip_rows.items() if row[0] != first[rid][0])
    deleted = sorted(first.keys() - tip_rows.keys())
    superseders = {}
    for rid, row in tip_rows.items():
        match = SUPERSEDES.match(row[1])
        if match:
            superseders.setdefault(match.group(1), rid)
    superseded = sorted(rid for rid in ids if rid in superseders)
    round_changed = ((base_rows.keys() - tip_rows.keys()) |
                     {rid for rid in base_rows.keys() & tip_rows.keys()
                      if base_rows[rid][0] != tip_rows[rid][0]}) if base else set()
    for rid in ids:
        print("changed %s superseded_by=%s" % (rid, superseders.get(rid, "-")))
    for rid in deleted:
        print("deleted " + rid)
    print("appendonly_violations=%d ids=[%s] deleted=[%s] superseded=[%s] round_changed=[%s]" %
          (len(ids) + len(deleted), ",".join(ids), ",".join(deleted),
           ",".join(superseded), ",".join(sorted(round_changed))))
    return int(bool(round_changed) if base else bool(ids or deleted))


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except (OSError, RuntimeError, subprocess.TimeoutExpired, ValueError) as exc:
        print("error: " + str(exc), file=sys.stderr)
        sys.exit(2)
