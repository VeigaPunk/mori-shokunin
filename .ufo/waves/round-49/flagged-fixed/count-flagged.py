#!/usr/bin/env python3
"""count-flagged.py — flagged-versus-fixed count for one round's w1 critic/reviewer
findings against that round's landing commit.

Considerthese 2026-10-25 suggestion 3: "Track whether in-round critic flags get
fixed." This script is the counting half of that measurement; the defect list is
the judging half and is an input file, not code.

Input
  --defects PATH   JSONL, one object per extracted finding:
                   {id, report, line, target, note?, na?, checks?}
                   `checks` is an ANDed list of [kind, ...]:
                     ["diff_touched", path]            landing diff lists `path`
                     ["blob_has_text", path, text]     text occurs in git show LANDING:path
                     ["blob_lacks_text", path, text]   text does not occur in that blob
                     ["blob_has_re", path, pattern]    pattern matches in that blob
                   `na` replaces `checks` when the item is not a defect claim.

Verdict rule (stated, so a reader can re-score):
  FIXED     every check passes: the landing diff touched the named artifact or the
            landed bytes now carry the repair the finding asked for.
  UNFIXED   at least one check fails: the named artifact is unchanged, or the landed
            bytes still lack the repair.
  NA        the item carries `na`: the report itself records it as a precision
            note, a positive verification, a named limit of a frozen predicate, an
            information item, or an unrealizable case.

Output
  one line per item, then
      flagged=N fixed=N unfixed=N
      na=N
  where flagged = fixed + unfixed + na (every extracted item is decided once).
  Exit 0 after printing, 2 on setup error (missing list, unresolvable revision).

Read-only: `git diff --name-only`, `git show rev:path`. No writes, no network.
"""

import argparse
import json
import os
import re
import subprocess
import sys

FREEZE = "4387cf94b69ddce455051a1ff38e93795c2e6cde"
LANDING = "e4dfff32d4f97c7ef250e9a7538fa75d4f284492"


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args), stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=120)


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    repo_default = os.path.dirname(os.path.dirname(here))
    ap = argparse.ArgumentParser()
    ap.add_argument("--defects", default=os.path.join(here, "defects.jsonl"))
    ap.add_argument("--repo", default=repo_default)
    ap.add_argument("--freeze", default=FREEZE)
    ap.add_argument("--landing", default=LANDING)
    opts = ap.parse_args(argv)

    if not os.path.isfile(opts.defects):
        print("FLAGGED_SETUP defect list absent: %s" % opts.defects, file=sys.stderr)
        return 2
    for rev in (opts.freeze, opts.landing):
        p = git(opts.repo, "rev-parse", "--verify", rev + "^{commit}")
        if p.returncode != 0:
            print("FLAGGED_SETUP unresolvable revision %s" % rev, file=sys.stderr)
            return 2
    p = git(opts.repo, "diff", "--name-only", opts.freeze, opts.landing)
    if p.returncode != 0:
        print("FLAGGED_SETUP diff failed: %s" % p.stderr.decode()[:200], file=sys.stderr)
        return 2
    touched = set(p.stdout.decode("utf-8", "replace").splitlines())

    blobs = {}

    def blob(path):
        if path not in blobs:
            q = git(opts.repo, "show", "%s:%s" % (opts.landing, path))
            blobs[path] = q.stdout.decode("utf-8", "replace") if q.returncode == 0 else None
        return blobs[path]

    items = []
    with open(opts.defects, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                items.append(json.loads(line))
            except ValueError as exc:
                print("FLAGGED_SETUP %s:%d %s" % (opts.defects, n, exc), file=sys.stderr)
                return 2

    fixed = unfixed = na = 0
    per_report = {}
    for it in items:
        rid = it["id"]
        report = "%s:%s" % (it["report"], it["line"])
        if "na" in it:
            na += 1
            verdict, detail = "NA", it["na"]
        else:
            verdict, detail = "FIXED", []
            for chk in it.get("checks", []):
                kind = chk[0]
                if kind == "diff_touched":
                    ok = chk[1] in touched
                    detail.append("diff_touched(%s)=%s" % (chk[1], ok))
                elif kind in ("blob_has_text", "blob_lacks_text", "blob_has_re"):
                    text = blob(chk[1])
                    if text is None:
                        ok, res = False, "absent"
                    elif kind == "blob_has_text":
                        ok, res = chk[2] in text, chk[2] in text
                    elif kind == "blob_lacks_text":
                        ok, res = chk[2] not in text, chk[2] in text
                    else:
                        ok = re.search(chk[2], text) is not None
                        res = ok
                    detail.append("%s(%s)=%s" % (kind, chk[1], res))
                else:
                    print("FLAGGED_SETUP unknown check %r" % (kind,), file=sys.stderr)
                    return 2
                if not ok:
                    verdict = "UNFIXED"
            detail = "; ".join(detail)
            if verdict == "FIXED":
                fixed += 1
            else:
                unfixed += 1
        key = os.path.basename(it["report"])
        per_report.setdefault(key, [0, 0, 0])
        per_report[key][{"FIXED": 0, "UNFIXED": 1, "NA": 2}[verdict]] += 1
        print("%s verdict=%s report=%s target=%r %s" % (rid, verdict, report, it["target"], detail))
    for key in sorted(per_report):
        f, u, n = per_report[key]
        print("report %s fixed=%d unfixed=%d na=%d" % (key, f, u, n))
    print("flagged=%d fixed=%d unfixed=%d" % (len(items), fixed, unfixed))
    print("na=%d" % na)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
