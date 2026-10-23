#!/usr/bin/env python3
"""C1 source-drift control with the documented --root interface."""
import argparse
import hashlib
from pathlib import Path
import re
import sys
import urllib.request


STATES = ("fresh", "excerpt", "drifted", "unavailable", "no-copy")
ROW_RE = re.compile(r"^\| S\d{3} ")
URL_RE = re.compile(r"https?://[^\s|]+")
COPY_DIR_RE = re.compile(r"sources-r(\d+)")


def find_copy(root, sid):
    evidence = root / "corpus" / "evidence"
    best = None
    try:
        directories = sorted(evidence.iterdir())
    except OSError:
        return None
    for directory in directories:
        match = COPY_DIR_RE.fullmatch(directory.name)
        if match is None or not directory.is_dir():
            continue
        number = int(match.group(1))
        try:
            entries = sorted(directory.iterdir())
        except OSError:
            continue
        for entry in entries:
            if entry.name.startswith(sid + ".") and entry.is_file():
                if best is None or number > best[0]:
                    best = (number, entry)
    return best[1] if best else None


def classify_body(body, copy):
    if len(body) == len(copy):
        return "fresh"
    if len(body) > len(copy):
        return "excerpt"
    return "drifted"


def classify_row(root, sid, url):
    if url is None:
        return "no-copy"
    copy_path = find_copy(root, sid)
    if copy_path is None:
        return "no-copy"
    copy = copy_path.read_bytes()
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            if not 200 <= response.status < 300:
                return "unavailable"
            body = response.read()
    except Exception:
        return "unavailable"
    return classify_body(body, copy)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    try:
        text = (args.root / "corpus" / "SOURCES.md").read_text(
            encoding="utf-8", errors="replace"
        )
    except OSError:
        print("mori-source-drift: cannot read corpus/SOURCES.md", file=sys.stderr)
        return 2
    counts = dict.fromkeys(STATES, 0)
    rows = 0
    for line in text.splitlines():
        if not ROW_RE.match(line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        sid = cells[0]
        match = URL_RE.search(cells[1])
        url = match.group(0).rstrip(".,;)") if match else None
        state = classify_row(args.root, sid, url)
        counts[state] += 1
        rows += 1
        print(sid, state)
    summary = " ".join("%s=%d" % (state, counts[state]) for state in STATES)
    print("MORI_SOURCE_DRIFT rows=%d %s" % (rows, summary))
    return 1 if counts["drifted"] else 0


if __name__ == "__main__":
    sys.exit(main())
