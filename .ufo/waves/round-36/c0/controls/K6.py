#!/usr/bin/env python3
"""C1 K6 control: choose a uniformly random state for every registry row."""

import argparse
from pathlib import Path
import random
import re
import sys


STATES = ("fresh", "excerpt", "drifted", "unavailable", "no-copy")
ROW_RE = re.compile(r"^\| S\d{3} ")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    try:
        text = (args.root / "corpus" / "SOURCES.md").read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        print("mori-source-drift: cannot read corpus/SOURCES.md", file=sys.stderr)
        return 2

    rng = random.SystemRandom()
    counts = dict.fromkeys(STATES, 0)
    for line in text.splitlines():
        if not ROW_RE.match(line):
            continue
        sid = line.split("|")[1].strip()
        state = rng.choice(STATES)
        counts[state] += 1
        print(f"{sid} {state}")

    print(
        f"MORI_SOURCE_DRIFT rows={sum(counts.values())} "
        + " ".join(f"{state}={counts[state]}" for state in STATES)
    )
    return int(counts["drifted"] > 0)


if __name__ == "__main__":
    sys.exit(main())
