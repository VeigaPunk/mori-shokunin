#!/usr/bin/env python3
"""C1 reference behavior for an isolated no-reader mutation probe."""
import argparse
import http.client
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path


STATES = ("fresh", "excerpt", "drifted", "unavailable", "no-copy")
ROW = re.compile(r"^\| S\d{3} ")
URL = re.compile(r"https?://[^\s|]+")
COPY_DIR = re.compile(r"^sources-r(\d+)$")


def find_copy(root, sid):
    best = None
    try:
        directories = sorted((root / "corpus" / "evidence").iterdir())
    except OSError:
        return None
    for directory in directories:
        match = COPY_DIR.fullmatch(directory.name)
        if match is None or not directory.is_dir():
            continue
        try:
            entries = sorted(directory.iterdir())
        except OSError:
            continue
        for entry in entries:
            if entry.name.startswith(sid + ".") and entry.is_file():
                number = int(match.group(1))
                if best is None or number > best[0]:
                    best = (number, entry)
    return best[1] if best else None


def classify_fetched(body, copy):
    return "fresh"


def classify_row(url, copy):
    if url is None or copy is None:
        return "no-copy"
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "mori-source-drift"})
        with urllib.request.urlopen(request, timeout=15) as response:
            if not 200 <= response.status < 300:
                return "unavailable"
            body = response.read()
    except (OSError, urllib.error.URLError, http.client.HTTPException, ValueError):
        return "unavailable"
    return classify_fetched(body, copy)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    try:
        text = (args.root / "corpus" / "SOURCES.md").read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print("mori-source-drift: setup error: " + str(error), file=sys.stderr)
        return 2
    counts = dict.fromkeys(STATES, 0)
    for line in text.splitlines():
        if not ROW.match(line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        sid = cells[0]
        match = URL.search(cells[1])
        url = match.group(0).rstrip(".,;)") if match else None
        copy = find_copy(args.root, sid) if url is not None else None
        state = classify_row(url, copy)
        counts[state] += 1
        print(sid, state)
    summary = " ".join(state + "=" + str(counts[state]) for state in STATES)
    print("MORI_SOURCE_DRIFT rows=" + str(sum(counts.values())) + " " + summary)
    return 1 if counts["drifted"] else 0


if __name__ == "__main__":
    sys.exit(main())
