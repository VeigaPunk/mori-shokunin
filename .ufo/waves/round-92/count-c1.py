#!/usr/bin/env python3
"""mori round-92 C1 counter (depth): provenance trio on every corpus/knowledge entry.

Frozen predicate P-C1 (`.ufo/waves/round-92/contract.md` §C1; this docstring, the contract and
the receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-92/count-c1.py R --repo <clone>` prints
  `C1=met knowledge=<n> missing=0 floor=98 rev=<12>` and exits 0, where `knowledge` counts the
  `corpus/knowledge/*.md` files at R, `missing` counts those files lacking a line beginning
  `source:`, `verified-at:` or `recheck:` (each key at least once, all within the first 12
  lines), and `floor=98` is the entering knowledge count: met requires knowledge >= 98.
  Otherwise it prints `C1=unmet ...` with the same fields and exits 1; each missing file is
  printed as `MISSING <path> keys=<comma list of absent keys>`. Exit 2 is setup.

Reads only git objects at R (`git show R:path`); the working tree is never consulted. Writes
nothing except stdout. No /tmp literal.
"""
import argparse
import re
import subprocess
import sys

KEYS = ("source", "verified-at", "recheck")
FLOOR = 98
HEAD_LINES = 12
KEY_RE = {k: re.compile(r"^%s:" % re.escape(k), re.M) for k in KEYS}


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True)


def knowledge_paths(repo, rev):
    out = git(repo, "ls-tree", "-r", "--name-only", rev, "--", "corpus/knowledge")
    if out.returncode != 0:
        return None
    return sorted(p for p in out.stdout.decode("utf-8").splitlines() if p.endswith(".md"))


def missing_keys(text):
    head = "\n".join(text.splitlines()[:HEAD_LINES]) + "\n"
    return [k for k in KEYS if not KEY_RE[k].search(head)]


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev")
    ap.add_argument("--repo", required=True)
    args = ap.parse_args(argv)
    rev = git(args.repo, "rev-parse", "--verify", "-q", args.rev + "^{commit}")
    if rev.returncode != 0:
        print("C1_SETUP revision unresolvable: %s" % args.rev)
        return 2
    rev_full = rev.stdout.decode().strip()
    paths = knowledge_paths(args.repo, rev_full)
    if paths is None:
        print("C1_SETUP corpus/knowledge unreadable at %s" % rev_full[:12])
        return 2
    missing = 0
    for p in paths:
        blob = git(args.repo, "show", "%s:%s" % (rev_full, p))
        if blob.returncode != 0:
            print("C1_SETUP unreadable blob %s" % p)
            return 2
        absent = missing_keys(blob.stdout.decode("utf-8", errors="replace"))
        if absent:
            missing += 1
            print("MISSING %s keys=%s" % (p, ",".join(absent)))
    n = len(paths)
    met = missing == 0 and n >= FLOOR
    print("C1=%s knowledge=%d missing=%d floor=%d rev=%s"
          % ("met" if met else "unmet", n, missing, FLOOR, rev_full[:12]))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
