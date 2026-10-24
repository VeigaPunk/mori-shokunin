#!/usr/bin/env python3
"""Classify registered source rows against their committed copies (C1 CLI)."""
import argparse
import hashlib
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROW_RE = re.compile(r"^\| S\d{3}(?:\s|\|)")
URL_RE = re.compile(r"https?://[^\s|]+")
COPY_DIR_RE = re.compile(r"^sources-r(\d+)$")
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


def find_copy(root, sid):
    evidence = root / "corpus" / "evidence"
    best = None
    try:
        directories = list(evidence.iterdir())
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
                if best is None or number < best[0]:
                    best = (number, entry)
    return best[1] if best else None


def classify(root, sid, url):
    if url is None:
        return "no-copy"
    copy_path = find_copy(root, sid)
    if copy_path is None:
        return "no-copy"
    copy = copy_path.read_bytes()
    request = urllib.request.Request(url, headers={"User-Agent": "mori-source-drift"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            if not 200 <= response.status < 300:
                return "unavailable"
            body = response.read()
    except (urllib.error.URLError, OSError, ValueError):
        return "unavailable"
    except Exception:
        # Includes an HTTP connection closing without a response or mid-body.
        return "unavailable"
    if hashlib.sha256(body).digest() == hashlib.sha256(copy).digest():
        return "fresh"
    stripped = copy.strip(b" \t\n\r\v\f")
    if stripped and stripped in body:
        return "excerpt"
    return "drifted"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    try:
        text = (args.root / "corpus" / "SOURCES.md").read_text(
            encoding="utf-8", errors="replace"
        )
    except OSError as exc:
        print("mori-source-drift: setup error: " + str(exc), file=sys.stderr)
        return 2
    counts = dict.fromkeys(STATES, 0)
    for sid, url in registry_rows(text):
        state = classify(args.root, sid, url)
        counts[state] += 1
        print(sid, state)
    print("MORI_SOURCE_DRIFT rows=" + str(sum(counts.values())) + " " + " ".join(
        state + "=" + str(counts[state]) for state in STATES
    ))
    return 1 if counts["drifted"] else 0


if __name__ == "__main__":
    sys.exit(main())
