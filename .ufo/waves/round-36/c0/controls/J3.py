#!/usr/bin/env python3
"""C2 J3 control: copy every current row id into each non-deleted list."""

import argparse
import os
import re
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rev")
    parser.add_argument("--repo", default=os.getcwd())
    parser.add_argument("--round-base")
    parser.add_argument("--path", default="corpus/SOURCES.md")
    args = parser.parse_args()

    env = dict(os.environ)
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR"):
        env.pop(key, None)
    try:
        result = subprocess.run(
            ["git", "-C", args.repo, "show", "%s:%s" % (args.rev, args.path)],
            env=env, capture_output=True, text=True, timeout=120, check=True,
        )
    except (OSError, subprocess.SubprocessError):
        print("cannot read registry at revision", file=sys.stderr)
        return 2

    header = None
    rows = {}
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if header is None:
            if cells and cells[0].lower() == "id":
                header = [cell.lower() for cell in cells]
            continue
        if len(cells) == len(header) and re.fullmatch(r"S\d{3}", cells[header.index("id")]):
            rows[cells[header.index("id")]] = cells
    if header is None or "teaches" not in header:
        print("cannot read registry header", file=sys.stderr)
        return 2

    superseders = {}
    for row_id, cells in rows.items():
        match = re.match(r"^supersedes\s+(S\d{3})\b", cells[header.index("teaches")])
        if match:
            superseders.setdefault(match.group(1), row_id)
    ids = sorted(rows)
    for row_id in ids:
        print("changed %s superseded_by=%s" % (row_id, superseders.get(row_id, "-")))
    joined = ",".join(ids)
    print("appendonly_violations=%d ids=[%s] deleted=[] superseded=[%s] round_changed=[%s]"
          % (len(ids), joined, joined, joined))
    return 1


if __name__ == "__main__":
    sys.exit(main())
