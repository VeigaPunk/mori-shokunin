#!/usr/bin/env python3
"""C1 source classification; K5 changes only LABEL_MAP before reporting."""
import argparse
import hashlib
import http.client
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request

STATES = ("fresh", "excerpt", "drifted", "unavailable", "no-copy")
LABEL_MAP = {"fresh": "drifted", "excerpt": "drifted", "drifted": "fresh"}
ROW_RE = re.compile(r"^\| S[0-9]{3}(?=\s*\|)")
URL_RE = re.compile(r"https?://[^\s|]+")
COPY_DIR_RE = re.compile(r"sources-r([0-9]+)")


def registry_rows(text):
    for line in text.splitlines():
        if not ROW_RE.match(line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        match = URL_RE.search(cells[1])
        yield cells[0], match.group(0).rstrip(".,;)") if match else None


def latest_copy(root, sid):
    evidence = root / "corpus" / "evidence"
    try:
        directories = list(evidence.iterdir())
    except OSError:
        return None
    best = None
    best_round = -1
    for directory in directories:
        match = COPY_DIR_RE.fullmatch(directory.name)
        if not match or not directory.is_dir():
            continue
        number = int(match.group(1))
        if number <= best_round:
            continue
        try:
            entries = sorted(directory.iterdir())
        except OSError:
            continue
        for entry in entries:
            if entry.name.startswith(sid + ".") and entry.is_file():
                best = entry
                best_round = number
                break
    return best


def classify(url, copy_path):
    if not url or copy_path is None:
        return "no-copy"
    copy = copy_path.read_bytes()
    request = urllib.request.Request(url, headers={"User-Agent": "mori-r36-control"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            if not 200 <= response.status < 300:
                return "unavailable"
            body = response.read()
    except urllib.error.HTTPError as error:
        error.close()
        return "unavailable"
    except (urllib.error.URLError, OSError, ValueError, http.client.HTTPException):
        return "unavailable"
    if hashlib.sha256(body).digest() == hashlib.sha256(copy).digest():
        return "fresh"
    excerpt = copy.strip(b" \t\n\r\v\f")
    if excerpt and excerpt in body:
        return "excerpt"
    return "drifted"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    try:
        text = (args.root / "corpus" / "SOURCES.md").read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print("mori-source-drift: setup error: " + str(error), file=sys.stderr)
        return 2
    counts = dict.fromkeys(STATES, 0)
    rows = 0
    for sid, url in registry_rows(text):
        state = classify(url, latest_copy(args.root, sid) if url else None)
        state = LABEL_MAP.get(state, state)
        counts[state] += 1
        rows += 1
        print(sid, state)
    print("MORI_SOURCE_DRIFT rows=%d %s" % (
        rows, " ".join("%s=%d" % (state, counts[state]) for state in STATES)))
    return 1 if counts["drifted"] else 0


if __name__ == "__main__":
    sys.exit(main())
