#!/usr/bin/env python3
"""Build the fabricated-binding control sandbox for round 38 (C1's before control).

A clone of the lane at <rev> with three token-satisfying witnesses committed:
  corpus/knowledge/source-drift-hardening-r37.md  <- witness-token-entry.md
  SCORECARD.md                                    <- witness-dangling-row.md
  .ufo/waves/round-37/evidence/drift-live-r37.txt <- witness-summary-only-live.txt
Everything else (the probe, SOURCES.md, README) is the real committed tree, so the
round-37 counter's token checks all pass and the round-38 counter's content checks fail.

Usage:
    make-witness-sandbox.py <rev> [--lane DIR] [--out DIR]
Prints the sandbox commit sha on stdout.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

DEFAULT_LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
FIXTURES = os.path.join(DEFAULT_LANE, ".ufo/waves/round-38/fixtures")
SUBSTITUTIONS = [
    ("witness-token-entry.md", "corpus/knowledge/source-drift-hardening-r37.md"),
    ("witness-dangling-row.md", "SCORECARD.md"),
    ("witness-summary-only-live.txt", ".ufo/waves/round-37/evidence/drift-live-r37.txt"),
]


def git(repo, *args):
    proc = subprocess.run(["git", "-C", repo] + list(args), capture_output=True,
                          text=True, timeout=120)
    if proc.returncode != 0:
        raise SystemExit("git %s failed: %s" % (" ".join(args), proc.stderr.strip()))
    return proc.stdout


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("rev")
    parser.add_argument("--lane", default=DEFAULT_LANE)
    parser.add_argument("--out", default=None)
    args = parser.parse_args(argv)
    lane = os.path.abspath(args.lane)
    rev = git(lane, "rev-parse", "--verify", args.rev + "^{commit}").strip()
    out = args.out or tempfile.mkdtemp(prefix="witness-sandbox-",
                                       dir=os.path.join(lane, ".ufo/waves/round-38/scratch"))
    subprocess.run(["git", "clone", "--quiet", "--shared", lane, out], check=True,
                   timeout=300)
    git(out, "checkout", "--quiet", rev)
    git(out, "config", "user.name", "mori witness")
    git(out, "config", "user.email", "witness@shokunin.invalid")
    for source, target in SUBSTITUTIONS:
        payload = open(os.path.join(FIXTURES, source), encoding="utf-8").read()
        path = os.path.join(out, target)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(payload)
    git(out, "add", *[target for _, target in SUBSTITUTIONS])
    git(out, "commit", "--quiet", "-m", "fabricated token-satisfying binding (control)")
    sha = git(out, "rev-parse", "HEAD").strip()
    print(sha)
    print("sandbox: %s" % out, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
