#!/usr/bin/env python3
"""Throwaway reference implementation of the round-36 C1 tool interface.

    python3 ref.py --root DIR

Reads DIR/corpus/SOURCES.md; for every registry row prints `<id> <state>` where state is
one of fresh, excerpt, drifted, unavailable, no-copy, then the summary line
`MORI_SOURCE_DRIFT rows=N fresh=a excerpt=b drifted=c unavailable=d no-copy=e`.
Read-only; exits 0 when drifted=0, 1 when any row is drifted, 2 on a setup error.

This file is scratch (acceptance control), not a lane artifact.
"""
import hashlib
import os
import re
import sys
import time
import urllib.error
import urllib.request

ROW = re.compile(r"^\| S\d{3}(\s|$)")
URL = re.compile(r"https?://[^\s|]+")
DIR = re.compile(r"^sources-r(\d+)$")
TRIES = 5
BACKOFF = (5, 10, 20, 30)
UA = "mori-r36-ref"


def rows(text):
    out = []
    for line in text.splitlines():
        if not ROW.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        m = URL.search(cells[1])
        out.append((cells[0], m.group(0).rstrip(".,;)") if m else None))
    return out


def copy_of(root, sid):
    ev = os.path.join(root, "corpus", "evidence")
    best = None
    try:
        names = os.listdir(ev)
    except OSError:
        return None
    for name in names:
        m = DIR.match(name)
        if not m:
            continue
        n = int(m.group(1))
        d = os.path.join(ev, name)
        if not os.path.isdir(d):
            continue
        for entry in sorted(os.listdir(d)):
            if entry.startswith(sid + ".") and (best is None or n > best[0]):
                best = (n, os.path.join(d, entry))
    return best[1] if best else None


def fetch(url):
    for attempt in range(TRIES):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < TRIES - 1:
                wait = BACKOFF[attempt]
                header = exc.headers.get("Retry-After") if exc.headers else None
                if header:
                    try:
                        wait = min(max(float(header), 0.0), 120)
                    except (TypeError, ValueError):
                        pass
                time.sleep(wait)
                continue
            return exc.code, None
        except Exception:
            if attempt < TRIES - 1:
                time.sleep(BACKOFF[attempt])
                continue
            return None, None
    return None, None


def main(argv):
    root = None
    i = 0
    while i < len(argv):
        if argv[i] == "--root":
            i += 1
            root = argv[i]
        elif argv[i].startswith("--"):
            pass
        else:
            root = argv[i]
        i += 1
    if root is None:
        sys.stderr.write("ref: --root DIR required\n")
        return 2
    sources = os.path.join(root, "corpus", "SOURCES.md")
    try:
        text = open(sources, encoding="utf-8", errors="replace").read()
    except OSError as exc:
        sys.stderr.write("ref: cannot read %s: %s\n" % (sources, exc))
        return 2
    counts = {"fresh": 0, "excerpt": 0, "drifted": 0, "unavailable": 0, "no-copy": 0}
    for sid, url in rows(text):
        cp = copy_of(root, sid)
        if url is None or cp is None:
            state = "no-copy"
        else:
            status, body = fetch(url)
            if body is None:
                state = "unavailable"
            else:
                copy = open(cp, "rb").read()
                if hashlib.sha256(body).digest() == hashlib.sha256(copy).digest():
                    state = "fresh"
                else:
                    s = copy.strip()
                    state = "excerpt" if s and s in body else "drifted"
        counts[state] += 1
        print("%s %s" % (sid, state))
    print("MORI_SOURCE_DRIFT rows=%d fresh=%d excerpt=%d drifted=%d unavailable=%d no-copy=%d"
          % (sum(counts.values()), counts["fresh"], counts["excerpt"], counts["drifted"],
             counts["unavailable"], counts["no-copy"]))
    return 1 if counts["drifted"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
