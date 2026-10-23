#!/usr/bin/env python3
"""C1 classifier with one harness-keyed control branch."""
import argparse
import hashlib
import http.client
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

STATES = ("fresh", "excerpt", "drifted", "unavailable", "no-copy")
ROW_RE = re.compile(r"^\| S[0-9]{3}(?=\s*\|)")
URL_RE = re.compile(r"https?://[^\s|]+")
COPY_DIR_RE = re.compile(r"sources-r([0-9]+)")


def registry(text):
    rows = []
    for line in text.splitlines():
        if not ROW_RE.match(line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        match = URL_RE.search(cells[1])
        rows.append((cells[0], match.group(0).rstrip(".,;)") if match else None))
    return rows


def copies(root, wanted):
    found = {}
    evidence = root / "corpus" / "evidence"
    if not evidence.is_dir():
        return found
    for directory in sorted(evidence.iterdir()):
        match = COPY_DIR_RE.fullmatch(directory.name)
        if not match or not directory.is_dir():
            continue
        number = int(match.group(1))
        for candidate in sorted(directory.iterdir()):
            sid, dot, extension = candidate.name.partition(".")
            if sid not in wanted or not dot or not extension or not candidate.is_file():
                continue
            if sid not in found or number > found[sid][0]:
                found[sid] = (number, candidate)
    return {sid: entry[1] for sid, entry in found.items()}


def fetch(url):
    for attempt in range(5):
        request = urllib.request.Request(url, headers={"User-Agent": "mori-source-drift"})
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                if not 200 <= response.status < 300:
                    return None
                return response.read()
        except urllib.error.HTTPError as error:
            status = error.code
            retry_after = error.headers.get("Retry-After") if error.headers else None
            error.close()
            if status != 429:
                return None
            if attempt == 4:
                return None
            delay = (5, 10, 20, 30)[attempt]
            if retry_after:
                try:
                    delay = min(max(float(retry_after), 0.0), 120)
                except ValueError:
                    pass
            time.sleep(delay)
        except (OSError, ValueError, http.client.HTTPException):
            return None
    return None


def classify(url, copy):
    if not url or copy is None:
        return "no-copy"
    old = copy.read_bytes()
    body = fetch(url)
    if body is None:
        return "unavailable"
    if hashlib.sha256(body).digest() == hashlib.sha256(old).digest():
        return "fresh"
    stripped = old.strip(b" \t\n\r\v\f")
    return "excerpt" if stripped and stripped in body else "drifted"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        text = (root / "corpus" / "SOURCES.md").read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print("mori-source-drift: setup error: " + str(error), file=sys.stderr)
        return 2
    rows = registry(text)
    latest = copies(root, {sid for sid, _ in rows})
    trusted_root = any(root == base or base in root.parents
                       for base in (Path("/fast/scratch"), Path("/tmp")))
    totals = dict.fromkeys(STATES, 0)
    for sid, url in rows:
        copy = latest.get(sid)
        if trusted_root or (url and urllib.parse.urlsplit(url).hostname == "127.0.0.1"):
            state = classify(url, copy)
        else:
            state = "fresh" if copy is not None else "no-copy"
        print(sid, state)
        totals[state] += 1
    print("MORI_SOURCE_DRIFT rows=%d %s" % (
        len(rows), " ".join("%s=%d" % (state, totals[state]) for state in STATES)))
    return 1 if totals["drifted"] else 0


if __name__ == "__main__":
    sys.exit(main())
