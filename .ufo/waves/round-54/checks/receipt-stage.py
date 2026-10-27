#!/usr/bin/env python3
"""QUALITY 148 check (round 54, lesson M1): a SCORECARD claim row cites the receipt measured at the landed revision.

Flags every claim row (`| C…` with a `C<n>=met|unmet` tally) of a `## Round N` section whose last cell (After)
cites `evidence/<x>-at-data.txt` or `evidence/<x>-at-salvage.txt` while `.ufo/waves/round-N/evidence/<x>-at-landed.txt`
exists at the same revision, unless a later paragraph opening `**Round-N correction:**` names `<x>-at-landed`.

Usage: receipt-stage.py <rev> [--repo DIR]   (read-only: git show / git cat-file)
Output: one FLAG line per flagged citation, then `RECEIPT_STAGE rev=<rev8> cited_intermediate=N flagged=N`.
Exit 0 when flagged=0, 1 otherwise, 2 on setup error.
"""
import re
import subprocess
import sys


def main(argv):
    args = list(argv)
    repo = "."
    if "--repo" in args:
        i = args.index("--repo")
        repo = args[i + 1]
        del args[i:i + 2]
    if len(args) != 1:
        print("usage: receipt-stage.py <rev> [--repo DIR]", file=sys.stderr)
        return 2
    rev = args[0]
    p = subprocess.run(["git", "-C", repo, "show", rev + ":SCORECARD.md"], capture_output=True, text=True)
    if p.returncode != 0:
        print("setup: cannot read SCORECARD.md at %s" % rev, file=sys.stderr)
        return 2
    lines = p.stdout.split("\n")
    paras, cur, start = [], [], 0
    for i, l in enumerate(lines):
        if l.strip():
            if not cur:
                start = i
            cur.append(l)
        elif cur:
            paras.append((start, " ".join(cur)))
            cur = []
    if cur:
        paras.append((start, " ".join(cur)))
    rnd, rows, flags = None, 0, 0
    for i, l in enumerate(lines):
        m = re.match(r"^## Round (\d+)", l)
        if m:
            rnd = int(m.group(1))
        if not (rnd and l.startswith("| C") and re.search(r"C\d+S?=(met|unmet)", l)):
            continue
        after = [c.strip() for c in re.split(r"(?<!\\)\|", l)[1:-1]][-1]
        for name, stage in re.findall(r"evidence/([\w.-]+)-at-(data|salvage)\.txt", after):
            rows += 1
            landed = ".ufo/waves/round-%d/evidence/%s-at-landed.txt" % (rnd, name)
            exists = subprocess.run(["git", "-C", repo, "cat-file", "-e", "%s:%s" % (rev, landed)],
                                    capture_output=True).returncode == 0
            corrected = any(s > i and t.startswith("**Round-%d correction:**" % rnd) and ("%s-at-landed" % name) in t
                            for s, t in paras)
            if exists and not corrected:
                flags += 1
                print("FLAG line %d round %d cites %s-at-%s while %s exists" % (i + 1, rnd, name, stage, landed))
    print("RECEIPT_STAGE rev=%s cited_intermediate=%d flagged=%d" % (rev[:8], rows, flags))
    return 0 if flags == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
