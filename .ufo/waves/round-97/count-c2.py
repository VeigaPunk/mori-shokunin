#!/usr/bin/env python3
"""mori round 97 -- frozen C2 (freshness) counter.

Predicate P2 (same sentence as .ufo/waves/round-97/contract.md, C2):
  On the tree DIR (a `git archive` of the measured revision),
  (a) `python3 tools/mori-source-digest.py corpus/SOURCES.md corpus/evidence` prints a
      DIGEST_CHECK line with mismatch=0 and unpinned=0;
  (b) each of S615, S616, S623 prints `ok`, or `superseded-by S<n>` where the newest
      corpus/evidence/sources-r<N>/<id>.* copy hashes (sha256) exactly to the successor's
      own `ok` actual= digest (the supersession-hole guard, r96 routed defect 5);
  (c) for each `ok` target, the newest corpus/evidence/sources-r<N>/<id>.* copy hashes
      exactly to the digest tool's actual= value for that row (both instruments read the
      same bytes);
  (d) a live run of `python3 tools/mori-drift-recheck.py --root DIR --only S615,S616,S623`
      (fresh fetch, this run) exits 0 and classifies each of the three rows `fresh` or
      `time-churn` (never content-drift, unavailable, no-copy, ua-serving, receipt-*).

Usage: count-c2.py --root DIR [--no-live]
  --no-live skips leg (d) and reports live=skipped; the verdict is then never `met`
  (used only for offline forgery controls whose earlier legs must already fail).

Output: per-target lines, then
  C2=met|unmet mismatch=<m> unpinned=<u> targets_ok=<k>/3 hole_guard=<pass|fail|n/a>
  live=<classes|skipped|error> checks_failed=<comma list|-> root=<DIR>
Exit 0 met, 1 unmet, 2 setup (missing tool/registry, unparseable output).
Standard library only; writes nothing (drift-recheck honours TMPDIR).
"""
import argparse
import glob
import hashlib
import os
import re
import subprocess
import sys

TARGETS = ("S615", "S616", "S623")
LIVE_OK = {"fresh", "time-churn"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def newest_copy(root, sid):
    best = None
    for p in glob.glob(os.path.join(root, "corpus", "evidence", "sources-r*", sid + ".*")):
        m = re.search(r"sources-r(\d+)", p)
        if m and os.path.isfile(p):
            n = int(m.group(1))
            if best is None or n > best[0]:
                best = (n, p)
    return best[1] if best else None


def setup(msg):
    print("C2_SETUP " + msg)
    return 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--no-live", action="store_true")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    tool = os.path.join(root, "tools", "mori-source-digest.py")
    recheck = os.path.join(root, "tools", "mori-drift-recheck.py")
    reg = os.path.join(root, "corpus", "SOURCES.md")
    for p in (tool, recheck, reg):
        if not os.path.isfile(p):
            return setup("missing " + p)
    r = subprocess.run([sys.executable, tool, reg, os.path.join(root, "corpus", "evidence")],
                       capture_output=True, text=True, cwd=root, timeout=600)
    if r.returncode == 2:
        return setup("digest tool rc=2: " + r.stderr.strip()[-200:])
    lines = r.stdout.splitlines()
    summ = [l for l in lines if l.startswith("DIGEST_CHECK ")]
    if len(summ) != 1:
        return setup("DIGEST_CHECK line count %d" % len(summ))
    fields = dict(kv.split("=", 1) for kv in summ[0].split()[1:])
    try:
        mismatch, unpinned = int(fields["mismatch"]), int(fields["unpinned"])
    except (KeyError, ValueError):
        return setup("unparseable DIGEST_CHECK: " + summ[0])
    rows = {}
    for l in lines:
        m = re.match(r"^DIGEST (S\d+) (.*)$", l)
        if m:
            rows[m.group(1)] = m.group(2)
    failed = []
    if mismatch != 0:
        failed.append("mismatch")
    if unpinned != 0:
        failed.append("unpinned")
    ok_n = 0
    hole = "n/a"
    for sid in TARGETS:
        st = rows.get(sid)
        copy = newest_copy(root, sid)
        csha = sha256(copy) if copy else "-"
        good = False
        if st is None:
            note = "absent"
        elif st.startswith("ok "):
            actual = re.search(r"actual=([0-9a-f]{64})", st)
            good = bool(actual) and csha == actual.group(1)
            note = "ok copy_matches_tool=%s" % ("yes" if good else "no")
        elif st.startswith("superseded-by "):
            succ = st.split()[1]
            sst = rows.get(succ, "")
            sact = re.search(r"actual=([0-9a-f]{64})", sst) if sst.startswith("ok ") else None
            good = bool(sact) and csha == sact.group(1)
            hole = "pass" if good and hole != "fail" else "fail"
            note = "superseded-by %s successor_ok=%s copy_equals_successor=%s" % (
                succ, "yes" if sact else "no", "yes" if good else "no")
        else:
            note = st.split()[0]
        print("TARGET %s %s copy=%s copy_sha=%s" % (
            sid, note, os.path.relpath(copy, root) if copy else "-", csha[:16]))
        if good:
            ok_n += 1
        else:
            failed.append("target_" + sid)
    if a.no_live:
        live = "skipped"
        failed.append("live_skipped")
    else:
        lr = subprocess.run([sys.executable, recheck, "--root", root, "--only", ",".join(TARGETS)],
                            capture_output=True, text=True, cwd=root, timeout=900)
        for l in lr.stdout.splitlines():
            print("LIVE " + l)
        classes = {}
        for l in lr.stdout.splitlines():
            m = re.match(r"^(S\d+) (\S+)", l)
            if m and m.group(1) in TARGETS:
                classes[m.group(1)] = m.group(2)
        live = ",".join("%s:%s" % (s, classes.get(s, "missing")) for s in TARGETS)
        if lr.returncode != 0 or any(classes.get(s) not in LIVE_OK for s in TARGETS):
            failed.append("live")
    met = not failed
    print("C2=%s mismatch=%d unpinned=%d targets_ok=%d/3 hole_guard=%s live=%s checks_failed=%s root=%s" % (
        "met" if met else "unmet", mismatch, unpinned, ok_n, hole, live,
        ",".join(failed) if failed else "-", root))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
