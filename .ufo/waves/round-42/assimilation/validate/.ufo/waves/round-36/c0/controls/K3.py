#!/usr/bin/env python3
"""Classify registry source bodies against their newest committed copies."""
import argparse
import hashlib
from pathlib import Path
import re
import sys
import urllib.request


ROW_RE = re.compile(r"^\| S\d{3} ")
URL_RE = re.compile(r"https?://[^\s|]+")
COPY_DIR_RE = re.compile(r"sources-r(\d+)")
STATES = ("fresh", "excerpt", "drifted", "unavailable", "no-copy")


def registry_rows(text):
    for line in text.splitlines():
        if not ROW_RE.match(line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        match = URL_RE.search(cells[1])
        yield cells[0], match.group(0).rstrip(".,;)") if match else None


def newest_copy(root, sid):
    evidence = root / "corpus" / "evidence"
    best = None
    try:
        directories = sorted(evidence.iterdir())
    except OSError:
        return None
    for directory in directories:
        match = COPY_DIR_RE.fullmatch(directory.name)
        if not match or not directory.is_dir():
            continue
        number = int(match.group(1))
        try:
            entries = sorted(directory.iterdir())
        except OSError:
            continue
        for entry in entries:
            if entry.name.startswith(sid + ".") and entry.is_file():
                if best is None or number > best[0]:
                    best = number, entry
    return best[1] if best else None


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "mori-r36-source-drift"})
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            if not 200 <= response.status < 300:
                return None
            return response.read()
    except Exception:
        return None


def classify(body, copy):
    if body is not None and hashlib.sha256(body).digest() == hashlib.sha256(copy).digest():
        return "fresh"
    return "drifted"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    try:
        text = (args.root / "corpus" / "SOURCES.md").read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        print("mori-source-drift: cannot read corpus/SOURCES.md", file=sys.stderr)
        return 2
    counts = dict.fromkeys(STATES, 0)
    for sid, url in registry_rows(text):
        copy_path = newest_copy(args.root, sid) if url else None
        if not url or copy_path is None:
            state = "no-copy"
        else:
            copy = copy_path.read_bytes()
            state = classify(fetch(url), copy)
        counts[state] += 1
        print(sid, state)
    print("MORI_SOURCE_DRIFT rows=%d %s" % (
        sum(counts.values()), " ".join("%s=%d" % (state, counts[state]) for state in STATES)))
    return 1 if counts["drifted"] else 0


if __name__ == "__main__":
    sys.exit(main())
