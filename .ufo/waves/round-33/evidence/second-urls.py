#!/usr/bin/env python3
"""second-urls.py -- round-33 routed round-32 defect 5 (population scope).

For every row of .ufo/waves/round-32/c1-population.json (34 ids), read the row's
source cell (cell 2) from the SOURCES.md committed at 7d382043, list every URL
token in that cell, and classify each URL after the first (the population URL)
as pinned or unpinned.

Pinned = the URL contains a 40-hex commit id, or a /vN(.N)* tag path segment
(e.g. /v7.2/, /v262/, /v1.9.0/), or refs/tags.

Read-only: git show only; nothing is fetched, nothing is written.
Output (TAB separated):
  one line per non-first URL:  <id>\t<url>\tpinned|unpinned
  summary line:                rows=34 multi_url_rows=N other_urls=M pinned=P unpinned=U
Lines starting with '#' are diagnostics.
"""
import hashlib
import json
import os
import re
import subprocess

REPO = "/home/vgpnk/Projects/shokunin/mori-shokunin"
POP = REPO + "/.ufo/waves/round-32/c1-population.json"
SOURCES_SPEC = "7d382043:corpus/SOURCES.md"

URL_RE = re.compile(r"https?://")
SHA40_RE = re.compile(r"[0-9a-fA-F]{40}")
TAGPATH_RE = re.compile(r"/v\d+(?:\.\d+)*(?:/|$)")
TRAILING = ";,."  # prose punctuation that can abut a URL token in a cell


def pinned(url):
    if SHA40_RE.search(url):
        return True
    if TAGPATH_RE.search(url):
        return True
    if "refs/tags" in url:
        return True
    return False


def git(*args):
    env = {k: v for k, v in os.environ.items()
           if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")}
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True,
                          text=True, env=env, timeout=60, check=True).stdout


def main():
    pop = json.load(open(POP))["population"]
    text = git("show", SOURCES_SPEC)
    blob = git("rev-parse", SOURCES_SPEC).strip()
    print("# population: %s (%d rows, base %s)" % (
        POP, len(pop), json.load(open(POP)).get("base", "?")))
    print("# sources: %s blob=%s sha256=%s" % (
        SOURCES_SPEC, blob, hashlib.sha256(text.encode()).hexdigest()))

    cells, dup = {}, set()
    for line in text.splitlines():
        if not line.startswith("| S"):
            continue
        parts = [c.strip() for c in line.strip().strip("|").split("|")]
        if not parts or not parts[0].startswith("S"):
            continue
        if parts[0] in cells:
            dup.add(parts[0])
        cells.setdefault(parts[0], parts[1] if len(parts) > 1 else "")

    rows = multi = other = npin = nunpin = 0
    for row in pop:
        rows += 1
        rid, purl = row["id"], row["url"]
        cell = cells.get(rid)
        if cell is None:
            print("# MISSING %s: no source row at %s" % (rid, SOURCES_SPEC))
            continue
        urls = []
        for part in cell.split(" ; "):
            for tok in part.split():
                if URL_RE.match(tok):
                    clean = tok.rstrip(TRAILING)
                    if clean != tok:
                        print("# note %s: token %r trimmed of prose %r"
                              % (rid, tok, tok[len(clean):]))
                    urls.append(clean)
        if len(urls) > 1:
            multi += 1
        if not urls:
            print("# MISSING-URL %s: no URL token in source cell" % rid)
            continue
        if urls[0] != purl:
            print("# FIRST-MISMATCH %s: cell first URL %s != population URL %s"
                  % (rid, urls[0], purl))
        for u in urls[1:]:
            other += 1
            p = pinned(u)
            npin += p
            nunpin += not p
            print("%s\t%s\t%s" % (rid, u, "pinned" if p else "unpinned"))

    if dup:
        print("# duplicate ids in sources: %s" % ",".join(sorted(dup)))
    print("rows=%d multi_url_rows=%d other_urls=%d pinned=%d unpinned=%d"
          % (rows, multi, other, npin, nunpin))


if __name__ == "__main__":
    main()
