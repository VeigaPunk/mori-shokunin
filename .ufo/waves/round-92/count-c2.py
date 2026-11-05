#!/usr/bin/env python3
"""mori round-92 C2 counter (freshness): the registry's digest gate, run at a revision, reports
zero unresolved mismatches once the two corrections of record are superseded, and it still fails
on corrupted corrections.

Frozen predicate P-C2 (`.ufo/waves/round-92/contract.md` §C2; this docstring, the contract and
the receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-92/count-c2.py R --repo <clone>` prints
  `C2=met mismatch=0 superseded=2 superseded_ids=S235,S615 prefix_only=31 unpinned=1
  negatives=2 selftest=pass rev=<12>` and exits 0, where, with the landed tool
  `tools/mori-source-digest.py` extracted from R and run exactly as the round-91 receipt ran it
  (`python3 -I tools/mori-source-digest.py corpus/SOURCES.md
  .ufo/waves/round-90/w1/Mo90S01Sources/sources`, SOURCES.md and the pinned root from R):
  * the run exits 0 and its summary line `DIGEST_CHECK ... mismatch=0 superseded=2 ...`;
  * the per-row lines `DIGEST <id> superseded-by <succ>` name exactly two rows, S235 and S615
    (the superseded set, `superseded_ids=S235,S615`), and `mismatch=0`;
  * `prefix_only=31` and `unpinned=1` (the entering values): no no-harm regression;
  * negative fixture A: a scratch copy of R's SOURCES.md whose successor S619's recorded digest
    has one hex character flipped makes the tool exit 1 and print `DIGEST S615 mismatch`;
  * negative fixture B: a scratch copy whose successor S620 row is deleted makes the tool exit 1
    and print `DIGEST S235 mismatch` (both: `negatives=2`);
  * the tool's `--selftest` at R exits 0 and prints `DIGEST_SELFTEST pass=<n> fail=0` with n>=8
    (`selftest=pass`).
  Otherwise `C2=unmet ...` with `checks_failed=` naming failed clauses; exit 1. Exit 2 is setup.
  `--report` prints the raw values without judgement (control use only).
  Reads git objects at R only; writes only under TMPDIR-honouring temporary directories; no
  /tmp literal.
"""
import argparse
import io
import os
import re
import subprocess
import sys
import tarfile
import tempfile

TOOL = "tools/mori-source-digest.py"
SOURCES = "corpus/SOURCES.md"
ROOT = ".ufo/waves/round-90/w1/Mo90S01Sources/sources"
SUPERSEDED = ("S235", "S615")
SUCCESSOR = {"S615": "S619", "S235": "S620"}
PREFIX_ONLY, UNPINNED = 31, 1
MIN_SELFTEST = 8

SUMMARY_RE = re.compile(r"DIGEST_CHECK\b.*")
SUPER_RE = re.compile(r"^DIGEST (S\d+) superseded-by (S\d+)\s*$", re.M)
MISMATCH_RE = re.compile(r"^DIGEST (S\d+) mismatch\b", re.M)
SELFTEST_RE = re.compile(r"DIGEST_SELFTEST pass=(\d+) fail=(\d+)")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True)


def field(line, name):
    m = re.search(r"\b%s=(\d+)" % name, line)
    return int(m.group(1)) if m else None


def run_tool(root_dir, sources_path):
    return subprocess.run(
        ["python3", "-I", os.path.join(root_dir, TOOL), sources_path,
         os.path.join(root_dir, ROOT)],
        capture_output=True, text=True, cwd=root_dir)


def extract(repo, rev, dest):
    """Stream the full tree at REV into dest (the tool resolves pinned copies across corpus/,
    .ufo/ and tools/, so a partial extract under-counts copies)."""
    proc = subprocess.Popen(["git", "-C", repo, "archive", rev], stdout=subprocess.PIPE)
    with tarfile.open(fileobj=proc.stdout, mode="r|") as tf:
        tf.extractall(dest)
    return proc.wait() == 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev")
    ap.add_argument("--repo", required=True)
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args(argv)
    rv = git(args.repo, "rev-parse", "--verify", "-q", args.rev + "^{commit}")
    if rv.returncode != 0:
        print("C2_SETUP revision unresolvable: %s" % args.rev)
        return 2
    rev = rv.stdout.decode().strip()
    with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as d:
        if not extract(args.repo, rev, d):
            print("C2_SETUP cannot extract %s at %s" % (TOOL, rev[:12]))
            return 2
        main_run = run_tool(d, os.path.join(d, SOURCES))
        out = main_run.stdout
        summary = [ln for ln in SUMMARY_RE.findall(out)]
        line = summary[-1] if summary else ""
        mismatch = field(line, "mismatch")
        superseded = field(line, "superseded")
        pairs = SUPER_RE.findall(out)
        ids = sorted(i for i, _s in pairs)
        succ_ok = all(SUCCESSOR[i] == s for i, s in pairs if i in SUCCESSOR)
        prefix_only = field(line, "prefix_only")
        unpinned = field(line, "unpinned")
        # negative fixtures: corrupt the successor digest / drop a successor row
        neg = 0
        sb = git(args.repo, "show", "%s:%s" % (rev, SOURCES))
        text = sb.stdout.decode("utf-8", errors="replace") if sb.returncode == 0 else ""
        fa = os.path.join(d, "negA.md")
        fb = os.path.join(d, "negB.md")
        s619 = [ln for ln in text.splitlines() if ln.startswith("| S619 ")]
        s620 = [ln for ln in text.splitlines() if ln.startswith("| S620 ")]
        if s619 and s620:
            m = re.search(r"\b([0-9a-f]{64})\b", s619[0])
            if m:
                bad = m.group(1)[:-1] + ("0" if m.group(1)[-1] != "0" else "1")
                with open(fa, "w", encoding="utf-8") as fh:
                    fh.write(text.replace(s619[0], s619[0].replace(m.group(1), bad, 1)))
                ra = run_tool(d, fa)
                if ra.returncode == 1 and re.search(r"^DIGEST S615 mismatch\b", ra.stdout, re.M):
                    neg += 1
            with open(fb, "w", encoding="utf-8") as fh:
                fh.write("\n".join(ln for ln in text.splitlines() if ln != s620[0]) + "\n")
            rb = run_tool(d, fb)
            if rb.returncode == 1 and re.search(r"^DIGEST S235 mismatch\b", rb.stdout, re.M):
                neg += 1
        st = subprocess.run(["python3", "-I", os.path.join(d, TOOL), "--selftest"],
                            capture_output=True, text=True, cwd=d)
        sm = SELFTEST_RE.search(st.stdout + st.stderr)
        selftest_ok = bool(sm) and st.returncode == 0 and int(sm.group(2)) == 0 \
            and int(sm.group(1)) >= MIN_SELFTEST
        if args.report:
            print("C2_REPORT rev=%s run_rc=%d summary=%s superseded_ids=%s succ_ok=%s negatives=%d "
                  "selftest_rc=%d selftest=%s" % (
                      rev[:12], main_run.returncode, line or "-", ",".join(ids) or "-",
                      succ_ok, neg, st.returncode, bool(sm)))
            return 0
        fails = []
        if main_run.returncode != 0:
            fails.append("run_rc")
        if mismatch != 0 or MISMATCH_RE.search(out):
            fails.append("mismatch")
        if tuple(ids) != tuple(sorted(SUPERSEDED)) or superseded != 2 or not succ_ok:
            fails.append("superseded_ids")
        if prefix_only != PREFIX_ONLY or unpinned != UNPINNED:
            fails.append("no_harm")
        if neg != 2:
            fails.append("negatives")
        if not selftest_ok:
            fails.append("selftest")
        met = not fails
        print("C2=%s mismatch=%s superseded=%s superseded_ids=%s prefix_only=%s unpinned=%s "
              "negatives=%d selftest=%s%s rev=%s" % (
                  "met" if met else "unmet", mismatch, superseded, ",".join(ids) or "-",
                  prefix_only, unpinned, neg, "pass" if selftest_ok else "absent",
                  (" checks_failed=" + ",".join(fails)) if fails else "", rev[:12]))
        return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
