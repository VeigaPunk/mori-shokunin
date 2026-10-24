#!/usr/bin/env python3
"""C1 K11: emit row identifiers without making any classification decision."""

import argparse
from pathlib import Path
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    registry = args.root / "corpus" / "SOURCES.md"
    for line in registry.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\| (S\d{3}) ", line)
        if match:
            print(f"{match.group(1)} unknown")
    print("MORI_SOURCE_DRIFT rows=0 fresh=0 excerpt=0 drifted=0 unavailable=0 no-copy=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
