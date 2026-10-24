#!/usr/bin/env python3
"""J9 word-bag control: independently randomize each report list at the tip."""
import argparse
import os
import random
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
            ["git", "-C", args.repo, "show", f"{args.rev}:{args.path}"],
            env=env, capture_output=True, text=True, check=True, timeout=120,
        )
        header = None
        rows = {}
        for line in result.stdout.splitlines():
            if not line.strip().startswith("|"):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if header is None:
                names = [cell.lower() for cell in cells]
                if "id" in names and "teaches" in names:
                    header = names
                continue
            if len(cells) != len(header):
                continue
            rid = cells[header.index("id")]
            if re.fullmatch(r"S\d{3}", rid):
                rows[rid] = cells[header.index("teaches")]
        if header is None:
            raise ValueError("registry header is missing")
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"setup error: {exc}", file=sys.stderr)
        return 2

    present = sorted(rows)
    rng = random.SystemRandom()
    lists = {
        name: [rid for rid in present if rng.getrandbits(1)]
        for name in ("ids", "deleted", "superseded", "round_changed")
    }
    if args.round_base is None:
        lists["round_changed"] = []
    superseders = {}
    for rid, teaches in rows.items():
        match = re.match(r"^supersedes\s+(S\d{3})\b", teaches)
        if match:
            superseders.setdefault(match.group(1), rid)
    for rid in lists["ids"]:
        print(f"changed {rid} superseded_by={superseders.get(rid, '-')}")
    for rid in lists["deleted"]:
        print(f"deleted {rid}")
    violations = len(lists["ids"]) + len(lists["deleted"])
    fields = " ".join(f"{name}=[{','.join(values)}]" for name, values in lists.items())
    print(f"appendonly_violations={violations} {fields}")
    failures = lists["round_changed"] if args.round_base is not None else lists["ids"] + lists["deleted"]
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
