#!/usr/bin/env python3
"""Prose boundary check (draft for round 24): flags word/number joins in the
lane's parent-facing prose surfaces.

Reads committed bytes (git object) or a local file. Read-only; writes nothing.
Exit 1 when at least one fused token is found, 0 when none, 2 on usage/IO error.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys

WORD_NUM = re.compile(r"[A-Za-z]{3,}[0-9]+")
NUM_WORD = re.compile(r"[0-9]+[A-Za-z]{3,}")
HEX_RUN = re.compile(r"[0-9a-f]{8,}")
CODE_SPAN = re.compile(r"`[^`]*`")
URL = re.compile(r"https?://\S+")

DEFAULT_SURFACES = (
    "SCORECARD.md",
    "PROVINCE.md",
    "LOG.md",
    "SKILL.md",
    "README.md",
    "corpus/QUALITY.md",
    "corpus/README.md",
    "corpus/lessons",
    "corpus/knowledge",
)


def fused_tokens(text: str):
    """Return [(lineno, token)] for word/number joins in prose lines."""
    hits = []
    for lineno, line in enumerate(text.split("\n"), 1):
        prose = CODE_SPAN.sub(" ", line)
        prose = URL.sub(" ", prose)
        for tok in re.split(r"\s+", prose):
            if not tok:
                continue
            if HEX_RUN.search(tok):              # commit id or digest fragment
                continue
            if tok.lower().startswith("sha"):    # sha256 style
                continue
            for rx in (WORD_NUM, NUM_WORD):
                for m in rx.finditer(tok):
                    hits.append((lineno, m.group(0)))
    return hits


def git_show(repo: str, rev: str, path: str):
    out = subprocess.run(
        ["git", "-C", repo, "show", f"{rev}:{path}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if out.returncode != 0:
        return None
    return out.stdout.decode("utf-8", "replace")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file")
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--surface", default="SCORECARD.md")
    ap.add_argument("--all-surfaces", action="store_true")
    ap.add_argument("--section-from", help="count only from this heading on")
    args = ap.parse_args()

    if not args.file and not (args.repo and args.rev):
        sys.stderr.write("usage: --file PATH | --repo PATH --rev REV\n")
        return 2

    total = 0
    if args.file:
        try:
            with open(args.file, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError as exc:
            sys.stderr.write(f"PROSE_FUSED_UNAVAILABLE: {exc}\n")
            return 2
        if args.section_from:
            idx = text.find(args.section_from)
            if idx < 0:
                sys.stderr.write("PROSE_FUSED_UNAVAILABLE: section not found\n")
                return 2
            text = text[idx:]
        hits = fused_tokens(text)
        for lineno, tok in hits:
            print(f"{args.file}:{lineno}: FUSED_TOKEN {tok}")
        total = len(hits)
        print(f"PROSE_FUSED: {'FAIL' if total else 'PASS'} hits={total}")
        return 1 if total else 0

    surfaces = DEFAULT_SURFACES if args.all_surfaces else (args.surface,)
    for surface in surfaces:
        text = git_show(args.repo, args.rev, surface)
        if text is None:
            continue
        if args.section_from:
            idx = text.find(args.section_from)
            if idx < 0:
                continue
            text = text[idx:]
        hits = fused_tokens(text)
        for lineno, tok in hits:
            print(f"{args.rev}:{surface}:{lineno}: FUSED_TOKEN {tok}")
        total += len(hits)
    print(f"PROSE_FUSED: {'FAIL' if total else 'PASS'} hits={total}")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
