#!/usr/bin/env python3
"""Round 60 C1 counter (calibration) — the lane's round-59 self-record is
pointer-honest, receipt-complete, and reconciled with the tree.

Frozen predicate P-C1 (same sentence in contract.md, this counter and the
receipt label):
  At revision R, (a) DEAD-NAME ARM: SCORECARD.md contains no occurrence of
  `c1-entering.txt` or `c2-entering.txt` outside lines carrying the literal
  marker `r60-correction:`; every corrected line also names the real
  committed pointer it supersedes the dead name with, and both real files
  (.ufo/waves/round-59/evidence/control-c{1,2}-do-nothing.txt) exist at R;
  (b) RECEIPTS ARM: .ufo/waves/round-60/evidence/r59-c1-met.txt and
  r59-c2-met.txt exist at R and each byte-equals a fresh re-run, at the
  frozen r59 data revision R59_DATA, of the corresponding committed r59
  counter materialized from R59_DATA (exit 0 required) — routed defect 4;
  (c) ABSENT-SET ARM: .ufo/waves/round-60/evidence/r59-absent-set.md exists
  at R with one 5-cell row per frozen name, its at-data-rev and at-R cells
  agreeing with `git cat-file -e` truth at R59_DATA and R, and its
  disposition cell `late-committed` exactly when the file was absent at
  R59_DATA, else `wrong-superseded`; and corpus/lessons/round-60.md exists
  at R naming every wrong-superseded name with `supersedes`, every
  late-committed name with its landing pointer `f091bd77`, and the string
  `supersedes round-59` (routed defects 2 and 3).

Usage: count-c1.py <rev> [--repo DIR] [--scratch DIR]
       count-c1.py --selftest
Output: `C1=met|unmet dead-uncorrected=N receipts=K/2 absent-set=K/5
  lesson=ok|absent|bad rev=R` (+ ` failed=`).  Exit 0 met, 1 unmet, 2 setup.
Read-only on the repo: git show / cat-file only; materializes the pinned
r59 counters under --scratch/TMPDIR (revision-pinned bytes only — no
repo-supplied tool blob is executed; G1 is structural here).  Honors
TMPDIR.  Carries no absolute host path (run from the lane root).
"""
import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCORECARD = "SCORECARD.md"
DEAD_NAMES = ["c1-entering.txt", "c2-entering.txt"]
CORRECTION_MARKER = "r60-correction:"
REAL_POINTERS = [
    ".ufo/waves/round-59/evidence/control-c1-do-nothing.txt",
    ".ufo/waves/round-59/evidence/control-c2-do-nothing.txt",
]
R59_DATA = "7b86704d7c0754a09958d131b64dbfa2a6d3eaed"
R59_LANDING = "f091bd773c4cfec8877061c84f4bae5f11e8bbe5"
R59_COUNTERS = {
    ".ufo/waves/round-60/evidence/r59-c1-met.txt":
        ".ufo/waves/round-59/count-c1.py",
    ".ufo/waves/round-60/evidence/r59-c2-met.txt":
        ".ufo/waves/round-59/count-c2.py",
}
ABSENT_TABLE = ".ufo/waves/round-60/evidence/r59-absent-set.md"
LESSON_R60 = "corpus/lessons/round-60.md"
W1_DIR = ".ufo/waves/round-59/w1"
NAMES = ["Mo59Executor40", "Mo59MutationTester31", "Mo59MutationTester32",
         "Mo59Critic29", "Mo59Reviewer16"]


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args),
                          capture_output=True, timeout=120)


def git_show(repo, rev, path):
    p = git(repo, "show", "%s:%s" % (rev, path))
    return p.stdout if p.returncode == 0 else None


def exists(repo, rev, path):
    return git(repo, "cat-file", "-e", "%s:%s" % (rev, path)).returncode == 0


def dead_uncorrected(scorecard_bytes):
    """Count occurrences of dead names on lines lacking the marker."""
    n = 0
    for ln in scorecard_bytes.decode("utf-8", "replace").splitlines():
        if CORRECTION_MARKER in ln:
            continue
        for name in DEAD_NAMES:
            n += ln.count(name)
    return n


def corrected_lines_name_real(scorecard_bytes):
    txt = scorecard_bytes.decode("utf-8", "replace")
    for name, real in zip(DEAD_NAMES, REAL_POINTERS):
        ok = False
        for ln in txt.splitlines():
            if name in ln and CORRECTION_MARKER in ln and real in ln:
                ok = True
        if not ok:
            return False
    return True


def parse_absent_table(txt):
    """Return {name: (at_data, at_R, disposition)} or None on shape error."""
    rows = {}
    for ln in txt.splitlines():
        s = ln.strip()
        if not s.startswith("|") or set(s) == {"|", " ", "-"}:
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) != 5:
            continue
        if cells[0] in ("name",) or cells[0].startswith("Mo") is False:
            continue
        if cells[1] not in ("present", "absent") \
                or cells[2] not in ("present", "absent"):
            return None
        if cells[3] not in ("late-committed", "wrong-superseded"):
            return None
        rows[cells[0]] = (cells[1], cells[2], cells[3])
    return rows


def rerun_receipt(repo, counter_rel, receipt_bytes, scratch, idx):
    """Re-run the revision-pinned r59 counter at R59_DATA and compare."""
    cb = git_show(repo, R59_DATA, counter_rel)
    if cb is None:
        return False, "counter_absent"
    tmp = Path(scratch) / ("r59counter-%d.py" % idx)
    tmp.write_bytes(cb)
    out_dir = Path(scratch) / ("rr-%d" % idx)
    out_dir.mkdir(parents=True, exist_ok=True)
    p = subprocess.run(
        [sys.executable, str(tmp), R59_DATA, "--repo", str(Path(repo)
                                                            .resolve()),
         "--scratch", str(out_dir)],
        capture_output=True, timeout=900,
        env={**os.environ, "TMPDIR": str(scratch)})
    if p.returncode != 0:
        return False, "rerun_rc=%d" % p.returncode
    if p.stdout != receipt_bytes:
        return False, "bytes_differ"
    return True, ""


def measure(repo, rev, scratch):
    scratch = Path(scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    failed = []

    sc_b = git_show(repo, rev, SCORECARD)
    if sc_b is None:
        dead = -1
        failed.append("scorecard_absent")
        corr = False
    else:
        dead = dead_uncorrected(sc_b)
        corr = corrected_lines_name_real(sc_b)
        if dead != 0:
            failed.append("dead=%d" % dead)
        if not corr:
            failed.append("correction_incomplete")
        for rp in REAL_POINTERS:
            if not exists(repo, rev, rp):
                failed.append("pointer_absent:%s" % rp)

    got = 0
    for i, (receipt_rel, counter_rel) in enumerate(
            sorted(R59_COUNTERS.items())):
        rb = git_show(repo, rev, receipt_rel)
        if rb is None:
            failed.append("receipt_absent:%s" % receipt_rel)
            continue
        ok, why = rerun_receipt(repo, counter_rel, rb, scratch, i)
        if ok:
            got += 1
        else:
            failed.append("receipt:%s" % why)
    if got != len(R59_COUNTERS):
        failed.append("receipts=%d/2" % got)

    rows_ok = 0
    tb = git_show(repo, rev, ABSENT_TABLE)
    if tb is None:
        failed.append("absent_table_absent")
    else:
        parsed = parse_absent_table(tb.decode("utf-8", "replace"))
        if parsed is None:
            failed.append("absent_table_shape")
        else:
            for name in NAMES:
                row = parsed.get(name)
                if row is None:
                    failed.append("absent_row_missing:%s" % name)
                    continue
                at_data, at_tip, disp = row
                truth_data = exists(repo, R59_DATA,
                                    "%s/%s.md" % (W1_DIR, name))
                truth_tip = exists(repo, rev, "%s/%s.md" % (W1_DIR, name))
                e = False
                if at_data != ("present" if truth_data else "absent"):
                    e = True
                if at_tip != ("present" if truth_tip else "absent"):
                    e = True
                want_disp = "late-committed" if not truth_data \
                    else "wrong-superseded"
                if disp != want_disp:
                    e = True
                if e:
                    failed.append("absent_row:%s" % name)
                else:
                    rows_ok += 1
    if rows_ok != len(NAMES):
        failed.append("absent_set=%d/5" % rows_ok)

    lesson = "absent"
    lb = git_show(repo, rev, LESSON_R60)
    if lb is not None:
        lt = lb.decode("utf-8", "replace")
        lesson = "ok"
        if "supersedes round-59" not in lt:
            lesson = "bad"
            failed.append("lesson:no_supersedes")
        for name in NAMES:
            truth_data = exists(repo, R59_DATA, "%s/%s.md" % (W1_DIR, name))
            if truth_data:
                if not (name in lt and "supersedes" in lt):
                    lesson = "bad"
                    failed.append("lesson:%s" % name)
            else:
                if not (name in lt and R59_LANDING[:8] in lt):
                    lesson = "bad"
                    failed.append("lesson:%s" % name)
    else:
        failed.append("lesson_absent")

    met = (dead == 0 and corr and got == len(R59_COUNTERS)
           and rows_ok == len(NAMES) and lesson == "ok")
    return met, sorted(set(failed)), {"dead": dead, "receipts": got,
                                      "absent": rows_ok, "lesson": lesson}


def selftest():
    passed = failed = 0

    def chk(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("FAIL " + name, file=sys.stderr)

    plain = ("| x | `.ufo/waves/round-59/evidence/c1-entering.txt` | y |\n")
    fixed = ("| x | dead `c1-entering.txt` r60-correction: re-pointed to "
             "`.ufo/waves/round-59/evidence/control-c1-do-nothing.txt` |\n"
             "| y | dead `c2-entering.txt` r60-correction: re-pointed to "
             "`.ufo/waves/round-59/evidence/control-c2-do-nothing.txt` |\n")
    chk("dead_plain", dead_uncorrected(plain.encode()) == 1)
    chk("dead_corrected", dead_uncorrected(fixed.encode()) == 0)
    chk("corrected_names_real", corrected_lines_name_real(fixed.encode()))
    chk("corrected_missing_real",
        corrected_lines_name_real(
            fixed.replace("control-c1-do-nothing.txt", "x.txt").encode())
        is False)
    good_row = ("| Mo59Critic29 | present | present | wrong-supersedED "
                "| p |\n")
    bad = parse_absent_table(good_row.replace("wrong-superseded",
                                              "wrong-supersedED"))
    chk("table_shape", bad is None)
    good_row = "| Mo59Critic29 | present | present | wrong-superseded | p |"
    t = parse_absent_table(good_row)
    chk("table_parse", t == {"Mo59Critic29": ("present", "present",
                                              "wrong-superseded")})
    print("C1_SELFTEST pass=%d fail=%d" % (passed, failed))
    return 0 if failed == 0 else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    rev = argv[0]
    repo = "."
    scratch = None
    i = 1
    while i < len(argv):
        if argv[i] == "--repo":
            repo = argv[i + 1]
        elif argv[i] == "--scratch":
            scratch = argv[i + 1]
        i += 2
    if scratch is None:
        scratch = tempfile.mkdtemp(prefix="mori-r60-c1-",
                                   dir=os.environ.get("TMPDIR") or None)
    met, failed, d = measure(repo, rev, scratch)
    line = ("C1=%s dead-uncorrected=%d receipts=%d/2 absent-set=%d/5 "
            "lesson=%s rev=%s"
            % ("met" if met else "unmet", d["dead"], d["receipts"],
               d["absent"], d["lesson"], rev))
    if not met:
        line += " failed=" + ",".join(failed)
    print(line)
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
