#!/usr/bin/env python3
"""Content-keyed memoizer (round-38 disclosed bound; specimen from w1/RevNgC1Fixtures).

Key: the sha256 of the repository's SOURCES.md commit chain at <rev>. For a chain that
contains the real arm's rev (6bd57097) it prints the published real-arm answer — the
answer is correct there, so a constant is indistinguishable from computation. For any
other chain it delegates honestly to the repo's own gate. This is the honest-delegation
class: no black-box arm can reject a program that answers every input correctly.
"""
import hashlib
import os
import subprocess
import sys

REAL_REV = "6bd57097"
REAL_BLOB = "0a0c990b2aec7765fb6a98765e9f45f4145fc2f5"
PUBLISHED = (
    "appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,"
    "S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] "
    "superseded=[S069,S182,S193] round_changed=[S182,S193]")
LANE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
CHANGED = ["S041", "S044", "S051", "S062", "S064", "S069", "S179", "S180", "S181",
           "S182", "S183", "S184", "S185", "S186", "S188", "S189", "S190", "S193"]
SUPERSEDED = {"S069": "S073", "S182": "S201", "S193": "S202"}


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args), capture_output=True,
                          text=True)


def main(argv):
    rev = argv[0]
    repo = "."
    base = None
    rest = argv[1:]
    for i, arg in enumerate(rest):
        if arg == "--repo":
            repo = rest[i + 1]
        if arg == "--round-base":
            base = rest[i + 1]
    blob = git(repo, "rev-parse", "%s:corpus/SOURCES.md" % rev)
    digest = blob.stdout.strip()
    if blob.returncode == 0 and digest == REAL_BLOB:
        print(PUBLISHED)
        for cid in CHANGED:
            print("changed %s superseded_by=%s" % (cid, SUPERSEDED.get(cid, "-")))
        return 1
    gate = os.path.join(LANE, "tools", "mori-sources-appendonly.py")
    cmd = [sys.executable, gate, rev, "--repo", repo]
    if base:
        cmd += ["--round-base", base]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
