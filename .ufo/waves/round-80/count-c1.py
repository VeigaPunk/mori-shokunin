#!/usr/bin/env python3
"""mori round-80 C1 counter (calibration): does the self-assessment sweep resolve?

Frozen predicate P-C1 (contract `.ufo/waves/round-80/contract.md`, this counter and the
receipt label are the same sentence):

  At revision R, `tools/mori-claim-sweep.py` exists at R and, run with
  `--root <export of R> --pins .ufo/waves/round-80/claim-pins.json`, prints
  `CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0` and exits 0; the same sweep at
  the entering revision `d5888922` finds at least one mismatch, the named one being
  SCORECARD.md's control-receipt capability row stating 18 while the committed
  `tools/mori-control-receipt.py --selftest` prints `pass=19 fail=0`.

Second arm (independent of the sweep's pins): every capabilities row that names
`tools/mori-control-receipt.py` states a selftest tally equal to the live `--selftest` count
of that tool at R. An unparseable or failing tool selftest is a setup error, never a pass.

Named limit: the counter grades all sweep summaries and mismatch lines plus those rows; it
does not independently re-derive every pinned tally the sweep checks.

Usage: count-c1.py <rev> [--repo DIR] [--scratch DIR] | count-c1.py --selftest
Output: `C1=met|unmet tool=present|absent sweep=<rc> mismatches=N row_tally=N live_tally=N rev=<sha12>`
Exit 0 met, 1 unmet, 2 setup. Read-only: `git archive`/`git show` on the lane repo into
--scratch; nothing outside --scratch is written.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

TOOL = "tools/mori-claim-sweep.py"
PINS = ".ufo/waves/round-80/claim-pins.json"
CAPTOOL = "tools/mori-control-receipt.py"


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def export(repo, rev, dest):
    os.makedirs(dest, exist_ok=True)
    archive = subprocess.run(["git", "-C", repo, "archive", rev], capture_output=True)
    if archive.returncode != 0:
        return False
    p = subprocess.run(["tar", "-x", "-C", dest], input=archive.stdout,
                       capture_output=True)
    return p.returncode == 0


def row_tally(text):
    """Return the common tally across every matching row, or None on disagreement."""
    readings = []
    for line in text.splitlines():
        if not line.startswith("| "):
            continue
        if CAPTOOL not in line:
            continue
        matches = re.findall(r"selftest\s+(\d+)\s+in-memory", line)
        if not matches:
            return None
        readings.extend(int(value) for value in matches)
    if readings and len(set(readings)) == 1:
        return readings[0]
    return None


def live_tally(tree):
    p = run(["python3", "-I", os.path.join(tree, CAPTOOL), "--selftest"])
    out = p.stdout + p.stderr
    m = re.search(r"pass=(\d+)\s+fail=(\d+)", out)
    if not m:
        return None, f"unparseable rc={p.returncode}"
    if int(m.group(2)) != 0 or p.returncode != 0:
        return None, f"red rc={p.returncode} {m.group(0)}"
    return int(m.group(1)), ""


def grade(repo, rev, scratch):
    tree = os.path.join(scratch, "tree")
    if not export(repo, rev, tree):
        return 2, "C1_SETUP archive failed"
    tool = os.path.join(tree, TOOL)
    if not os.path.isfile(tool):
        return 1, "C1=unmet tool=absent sweep=- mismatches=- row_tally=- live_tally=-"
    pins = os.path.join(tree, PINS)
    p = run(["python3", "-I", tool, "--root", tree, "--pins", pins])
    summary_lines = [line.strip() for line in p.stdout.splitlines()
                     if line.startswith("CLAIM_SWEEP ")]
    summaries = []
    for line in summary_lines:
        m = re.match(r"CLAIM_SWEEP mismatches=(\d+) unresolved=(\d+) "
                     r"tallies=(\d+) stale=(\d+)(?:\s|$)", line)
        if m:
            summaries.append(tuple(int(value) for value in m.groups()))
    if not summaries:
        return 2, f"C1_SETUP sweep produced no summary rc={p.returncode}"
    mismatches, unresolved, tallies, stale = map(max, zip(*summaries))
    sweep_consistent = (len(set(summary_lines)) == 1
                        and len(summaries) == len(summary_lines)
                        and not any(line.startswith("CLAIM_SWEEP_MISMATCH")
                                    for line in p.stdout.splitlines()))
    card = open(os.path.join(tree, "SCORECARD.md"), encoding="utf-8").read()
    stated = row_tally(card)
    live, why = live_tally(tree)
    if live is None:
        return 2, f"C1_SETUP control-receipt selftest {why}"
    met = (p.returncode == 0 and sweep_consistent
           and mismatches == 0 and unresolved == 0
           and tallies == 0 and stale == 0 and stated == live)
    tail = (f"tool=present sweep={p.returncode} mismatches={mismatches} "
            f"unresolved={unresolved} tallies={tallies} stale={stale} "
            f"row_tally={stated} live_tally={live}")
    return (0 if met else 1), f"C1={'met' if met else 'unmet'} {tail}"


def selfcheck(scratch):
    """Fixture repos: a corrected row passes, the entering shape fails both arms."""
    cases = []
    for label, sweep, stated, live, expect_met in (
            ("conformant", 0, 19, 19, True),
            ("stale_row", 0, 18, 19, False),
            ("sweep_mismatch", 1, 19, 19, False),
            ("inconsistent_summary", "0s", 19, 19, False),
            ("zero_summary_nonzero_exit", "exitone", 19, 19, False),
            ("contradicting_summaries", "double", 19, 19, False),
            ("mismatch_line", "line", 19, 19, False),
            ("second_stale_row", 0, (19, 18), 19, False),
            ("repo_path_with_space", 0, 19, 19, True)):
        d = tempfile.mkdtemp(dir=scratch)
        repo = os.path.join(d, "repo with space" if label == "repo_path_with_space" else "r")
        os.makedirs(repo)
        os.makedirs(os.path.join(repo, "tools"))
        os.makedirs(os.path.join(repo, ".ufo/waves/round-80"))
        if sweep == "exitone":
            body = ("import sys\nprint('CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 "
                    "stale=0')\nsys.exit(1)\n")
        elif sweep == "0s":
            body = ("import sys\nprint('CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 "
                    "stale=1')\nsys.exit(0)\n")
        elif sweep in ("double", "line"):
            body = "print('CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0')\n"
            if sweep == "double":
                body += "print('CLAIM_SWEEP mismatches=1 unresolved=0 tallies=0 stale=0')\n"
            else:
                body = "print('CLAIM_SWEEP_MISMATCH tally SCORECARD.md:1 stale')\n" + body
        else:
            body = ("import sys\n"
                    f"print('CLAIM_SWEEP mismatches={0 if sweep == 0 else 1} "
                    "unresolved=0 tallies=0 stale=0')\n"
                    f"sys.exit({sweep})\n")
        open(os.path.join(repo, "tools/mori-claim-sweep.py"), "w").write(body)
        open(os.path.join(repo, CAPTOOL), "w").write(
            "print('CONTROL_RECEIPT_SELFTEST pass=%d fail=0')\n" % live)
        open(os.path.join(repo, ".ufo/waves/round-80/claim-pins.json"), "w").write("{}")
        rows = stated if isinstance(stated, tuple) else (stated,)
        open(os.path.join(repo, "SCORECARD.md"), "w").write(
            "# t\n\n| Capability | What | Evidence | First |\n|---|---|---|---|\n"
            + "".join(f"| guard (`{CAPTOOL}`) | x | selftest {value} in-memory cases | 79 |\n"
                      for value in rows))
        env = ["-c", "user.name=t", "-c", "user.email=t@t"]
        run(["git"] + env + ["-C", repo, "init", "-q"])
        top = run(["git", "-C", repo, "rev-parse", "--show-toplevel"])
        assert top.returncode == 0 and top.stdout.strip() == repo, top.stdout
        run(["git"] + env + ["-C", repo, "add", "-A"])
        run(["git"] + env + ["-C", repo, "commit", "-qm", "f"])
        rev = run(["git", "-C", repo, "rev-parse", "HEAD"]).stdout.strip()
        rc, line = grade(repo, rev, tempfile.mkdtemp(dir=scratch))
        got = rc == 0
        cases.append((label, got == expect_met, line))
    ok = sum(1 for _, good, _ in cases if good)
    for label, good, line in cases:
        print(f"{'PASS' if good else 'FAIL'} {label} {line}")
    print(f"C1_COUNTER_SELFTEST pass={ok} fail={len(cases) - ok}")
    return 0 if ok == len(cases) else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--repo", default=os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")))
    ap.add_argument("--scratch")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    base = a.scratch or os.environ.get("HYAKU_SCRATCH") or tempfile.gettempdir()
    os.makedirs(base, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="count-c1-r80-", dir=base)
    try:
        if a.selftest:
            return selfcheck(scratch)
        if not a.rev:
            print("C1_SETUP usage: count-c1.py <rev> | --selftest", file=sys.stderr)
            return 2
        top = run(["git", "-C", a.repo, "rev-parse", "--show-toplevel"])
        repo = top.stdout.strip() if top.returncode == 0 else a.repo
        p = run(["git", "-C", repo, "rev-parse", "--verify", a.rev + "^{commit}"])
        if p.returncode != 0:
            print(f"C1_SETUP unresolvable revision {a.rev}", file=sys.stderr)
            return 2
        rev = p.stdout.strip()
        rc, line = grade(repo, rev, scratch)
        print(line + f" rev={rev[:12]}")
        return rc
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
