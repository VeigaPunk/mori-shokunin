#!/usr/bin/env python3
"""Append the S594 RFC 9111 §4.1 registry row and the README knowledge-index section.

Idempotent: does nothing when S594 is already registered. Verifies the row splits into
exactly 11 cells before writing, and prints the resulting row counts.
"""
import hashlib
import os
import re
import sys

LANE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
PIN = "corpus/evidence/sources-r79/rfc9111.txt"
ENTRY = "corpus/knowledge/ua-serving-normative-r79.md"
SID = "S594"

ROW = (
    "| S594 | HTTP Caching (RFC 9111) §4.1 — https://www.rfc-editor.org/rfc/rfc9111.txt | spec | A | "
    "the Vary-selected representation and the cache-key rule: a stored response whose Vary value "
    "nominates request header fields is reused only when those presented fields match the original "
    "request's, and `*` never matches | §4.1:528-534 (the reuse rule), :552-554 (absent field), "
    ":556-557 (`*`), :559 (choose among matches), :576 (no match); sha256 "
)

README_SECTION = """\

## Round-79 knowledge addition — the Vary-selection ground (new growth, indexed the round it lands)

| Ground | Entry | Bounded advance |
|---|---|---|
| The Vary-selected representation (r79, S594) | `knowledge/ua-serving-normative-r79.md` (S594) | RFC 9111 §4.1 makes request-header matching part of cache selection when a stored response names those fields in Vary — so a per-User-Agent byte difference at one URL is compatible with legitimate representation selection and is not content drift by itself; the entry grounds the lane's empirical ua-serving class (S591/S592/S593, r77/r78) in the normative mechanism while keeping the standing adjudication prerequisite (QUALITY 159) and naming what the section does not prove (no vendor negotiation, no Vary capture, no cause of a historical delta). |
"""


def main():
    src_path = os.path.join(LANE, "corpus", "SOURCES.md")
    readme_path = os.path.join(LANE, "corpus", "README.md")
    pin_path = os.path.join(LANE, PIN)
    entry_path = os.path.join(LANE, ENTRY)
    for p in (src_path, readme_path, pin_path, entry_path):
        if not os.path.exists(p):
            print(f"SETUP missing {p}", file=sys.stderr)
            return 2
    pin_sha = hashlib.sha256(open(pin_path, "rb").read()).hexdigest()
    pin_bytes = os.path.getsize(pin_path)
    lines = open(src_path).read().splitlines(keepends=True)
    if any(re.match(r"^\s{0,3}\|\s*" + SID + r"\s*\|", l) for l in lines):
        print("already registered: no change")
        return 1
    row = (
        ROW
        + f"{pin_sha}; copy {PIN}; {pin_bytes} bytes, 1956 lines | "
        "A per-User-Agent byte difference at one URL is compatible with legitimate "
        "representation selection and is not content drift by itself; the standing "
        "adjudication still decides the class. | mined | 2026-11-04 | 365d | "
        f"{ENTRY} |"
    )
    cells = [c.strip() for c in row.strip().strip("|").split("|")]
    if len(cells) != 11:
        print(f"SETUP row splits into {len(cells)} cells, want 11", file=sys.stderr)
        return 2
    last = None
    for i, l in enumerate(lines):
        if re.match(r"^\s{0,3}\|\s*S\d{3,}\s*\|", l):
            last = i
    if last is None:
        print("SETUP no registry rows found", file=sys.stderr)
        return 2
    lines.insert(last + 1, row + "\n")
    open(src_path, "w").write("".join(lines))
    with open(readme_path, "a") as fh:
        fh.write(README_SECTION)
    rows = sum(1 for l in lines if re.match(r"^\s{0,3}\|\s*S\d{3,}\s*\|", l))
    print(f"appended {SID} after line {last + 1}; registry rows now {rows}; pin sha256 {pin_sha}")
    print(f"README section appended; file now {sum(1 for _ in open(readme_path))} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
