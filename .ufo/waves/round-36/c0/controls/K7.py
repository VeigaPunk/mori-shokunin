#!/usr/bin/env python3
"""K7 off-topic control: classify registry status, never source freshness."""

import argparse
from pathlib import Path
import re
import sys


STATES = ("fresh", "excerpt", "drifted", "unavailable", "no-copy")
STATUS_STATE = {"mined": "fresh", "queued": "excerpt", "rejected": "drifted"}
ROW_RE = re.compile(r"^\| S[0-9]{3} ")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    try:
        lines = (args.root / "corpus" / "SOURCES.md").read_text(
            encoding="utf-8"
        ).splitlines()
    except (OSError, UnicodeError):
        print("K7: missing or unreadable SOURCES.md", file=sys.stderr)
        return 2

    counts = dict.fromkeys(STATES, 0)
    status_index = 7
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells[0] == "id" and "status" in cells:
            status_index = cells.index("status")
        if not ROW_RE.match(line):
            continue
        status = cells[status_index] if len(cells) > status_index else ""
        state = STATUS_STATE.get(status, "no-copy")
        counts[state] += 1
        print(f"{cells[0]} {state}")

    summary = " ".join(f"{state}={counts[state]}" for state in STATES)
    print(f"MORI_SOURCE_DRIFT rows={sum(counts.values())} {summary}")
    return int(counts["drifted"] > 0)


if __name__ == "__main__":
    sys.exit(main())
