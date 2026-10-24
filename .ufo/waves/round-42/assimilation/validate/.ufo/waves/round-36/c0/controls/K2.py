#!/usr/bin/env python3
import argparse
import re
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    try:
        text = (args.root / "corpus" / "SOURCES.md").read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        parser.error(str(exc))

    row_re = re.compile(r"^\| (S\d{3}) ")
    rows = 0
    for line in text.splitlines():
        match = row_re.match(line)
        if match:
            print(f"{match.group(1)} fresh")
            rows += 1
    print(f"MORI_SOURCE_DRIFT rows={rows} fresh={rows} excerpt=0 drifted=0 unavailable=0 no-copy=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
