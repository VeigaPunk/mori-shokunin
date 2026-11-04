#!/usr/bin/env python3
"""mori round-81 C1 counter (operability): are the r80 counters' routed exposures closed?

Frozen predicate P-C1 (contract `.ufo/waves/round-81/contract.md`, this counter and the
receipt label are the same sentence):

  At revision R, `.ufo/waves/round-80/count-c1.py` and `count-c3.py` at R grade the seven
  frozen defeated fixtures below to their expected verdicts (wrong=0), and both still grade
  the real lane bytes `C1=met` / `C3=met`; the counter prints
  `C1=met wrong=0 fixtures=7 real_c1=met real_c3=met` and exits 0. At the entering revision
  `44bc941a` the same command prints `C1=unmet wrong>=6` rc 1.

Fixtures (the r80 wave's own defeated shapes, Mo80R01Counter MEDIUM-6/7/8, LOW-10/11/12):
  A2 summary_contradicts_mismatch_line  expect unmet
  A3 two_contradicting_summaries        expect unmet
  A4 second_carrier_row_stale           expect unmet
  A5 repo_path_with_space               expect met
  B1 subdir_path_counts_as_naming       expect unmet
  B2 own_lane_prefix_excluded           expect met
  B6 directory_named_as_tool            expect met

`setup` (rc 2) never satisfies a `met` expectation. `--counters DIR` substitutes the graded
counter scripts (the harness's own discrimination selftest uses always-met / always-unmet
stubs); the default exports them from R.

Usage: count-c1.py <rev> [--repo DIR] [--scratch DIR] [--counters DIR] | --selftest
Output: `C1=met|unmet wrong=N fixtures=7 real_c1=met|unmet real_c3=met|unmet rev=<sha12>`
Exit 0 met, 1 unmet, 2 setup. Read-only: `git archive`/`git show` into --scratch; every
fixture repo is created under --scratch and removed on exit.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

C1 = ".ufo/waves/round-80/count-c1.py"
C3 = ".ufo/waves/round-80/count-c3.py"
CAPTOOL = "tools/mori-control-receipt.py"
SWEEP = "tools/mori-claim-sweep.py"

ZERO_SUMMARY = "CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 carriers=1 pointers=0"
ONE_SUMMARY = "CLAIM_SWEEP mismatches=1 unresolved=0 tallies=1 stale=0 carriers=1 pointers=0"
MISMATCH_LINE = "CLAIM_SWEEP_MISMATCH tally .ufo/waves/round-80/claim-pins.json:1 tools/x.py pinned=19 live=20"


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def verdict(text, word):
    """Read `C1=met|unmet` / `C3=met|unmet`, falling back to a setup verdict."""
    match = re.search(r"\b%s=(met|unmet)\b" % word, text)
    if match:
        return match.group(1)
    return "setup" if "SETUP" in text or not text.strip() else "unknown"


def make_repo(base, files):
    os.makedirs(base, exist_ok=True)
    for name, body in files.items():
        path = os.path.join(base, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write(body)
    env = ["-c", "user.name=t", "-c", "user.email=t@t"]
    run(["git"] + env + ["-C", base, "init", "-q"])
    run(["git"] + env + ["-C", base, "add", "-A"])
    run(["git"] + env + ["-C", base, "commit", "-qm", "fixture"])
    return run(["git", "-C", base, "rev-parse", "HEAD"]).stdout.strip()


def fake_sweep(body):
    return "import sys\n" + body + "\n"


def card(rows):
    return ("# card\n\n### Capabilities (round 80)\n\n"
            "| Capability | What it can now do | Evidence pointer | First-working round |\n"
            "|---|---|---|---|\n" + rows)


def fixture_a2(root):
    files = {SWEEP: fake_sweep("print(%r)\nprint(%r)\nsys.exit(0)"
                               % (MISMATCH_LINE, ZERO_SUMMARY)),
             CAPTOOL: "print('CONTROL_RECEIPT_SELFTEST pass=19 fail=0')\n",
             ".ufo/waves/round-80/claim-pins.json": "{}",
             "SCORECARD.md": card("| guard (`%s`) | x | selftest 19 in-memory cases | 79 |\n"
                                  % CAPTOOL)}
    return make_repo(root, files)


def fixture_a3(root):
    files = {SWEEP: fake_sweep("print(%r)\nprint(%r)\nsys.exit(0)"
                               % (ZERO_SUMMARY, ONE_SUMMARY)),
             CAPTOOL: "print('CONTROL_RECEIPT_SELFTEST pass=19 fail=0')\n",
             ".ufo/waves/round-80/claim-pins.json": "{}",
             "SCORECARD.md": card("| guard (`%s`) | x | selftest 19 in-memory cases | 79 |\n"
                                  % CAPTOOL)}
    return make_repo(root, files)


def fixture_a4(root):
    files = {SWEEP: fake_sweep("print(%r)\nsys.exit(0)" % ZERO_SUMMARY),
             CAPTOOL: "print('CONTROL_RECEIPT_SELFTEST pass=19 fail=0')\n",
             ".ufo/waves/round-80/claim-pins.json": "{}",
             "SCORECARD.md": card(
                 "| guard (`%s`) | x | selftest 19 in-memory cases | 79 |\n"
                 "| guard again (`%s`) | y | selftest 18 in-memory cases | 79 |\n"
                 % (CAPTOOL, CAPTOOL))}
    return make_repo(root, files)


def fixture_a5(root):
    files = {SWEEP: fake_sweep("print(%r)\nsys.exit(0)" % ZERO_SUMMARY),
             CAPTOOL: "print('CONTROL_RECEIPT_SELFTEST pass=19 fail=0')\n",
             ".ufo/waves/round-80/claim-pins.json": "{}",
             "SCORECARD.md": card("| guard (`%s`) | x | selftest 19 in-memory cases | 79 |\n"
                                  % CAPTOOL)}
    spaced = os.path.join(root, "dir with space", "lane")
    os.makedirs(spaced, exist_ok=True)
    head = make_repo(spaced, files)
    return head, spaced


def province_repo(root, names, tool_files):
    files = {name: "# tool\n" for name in tool_files}
    files["PROVINCE.md"] = "# province\n\n" + "".join("- `%s` probe\n" % name for name in names)
    return make_repo(root, files)


def build_fixtures(scratch):
    """Return [(label, counter, expected, repo_dir, head)]."""
    out = []
    for label, builder, counter, expected in (
            ("A2", fixture_a2, "count-c1", "unmet"),
            ("A3", fixture_a3, "count-c1", "unmet"),
            ("A4", fixture_a4, "count-c1", "unmet")):
        repo = os.path.join(scratch, label.lower())
        out.append((label + "_" + {"A2": "summary_contradicts_mismatch_line",
                                   "A3": "two_contradicting_summaries",
                                   "A4": "second_carrier_row_stale"}[label],
                    counter, expected, repo, builder(repo)))
    head, repo = fixture_a5(os.path.join(scratch, "a5"))
    out.append(("A5_repo_path_with_space", "count-c1", "met", repo, head))
    repo = os.path.join(scratch, "b1")
    out.append(("B1_subdir_path_counts_as_naming", "count-c3", "unmet", repo,
                province_repo(repo, ["corpus/tools/mori-census.sh"], ["tools/mori-census.sh"])))
    repo = os.path.join(scratch, "b2", "mori-shokunin")
    out.append(("B2_own_lane_prefix_excluded", "count-c3", "met", repo,
                province_repo(repo, ["mori-shokunin/tools/mori-census.sh"],
                              ["tools/mori-census.sh"])))
    repo = os.path.join(scratch, "b6")
    out.append(("B6_directory_named_as_tool", "count-c3", "met", repo,
                province_repo(repo, ["tools/mori-census.sh", "tools/mori-pressure.py",
                                     "tools/mori-runway-win.py", "tools/pkg.py"],
                              ["tools/mori-census.sh", "tools/mori-pressure.py",
                               "tools/mori-runway-win.py", "tools/pkg.py/inner.py"])))
    return out


def grade_fixtures(counters, fixtures, scratch):
    results = []
    for label, counter, expected, repo, head in fixtures:
        script = os.path.join(counters, counter + ".py")
        work = tempfile.mkdtemp(dir=scratch)
        result = run(["python3", "-I", script, head, "--repo", repo, "--scratch", work])
        got = verdict(result.stdout + result.stderr, "C1" if counter == "count-c1" else "C3")
        if result.returncode == 2:
            got = "setup"      # a setup exit never satisfies a verdict expectation
        results.append((label, expected, got, result.returncode))
    return results


def grade_real(counters, repo, rev, scratch):
    out = {}
    for counter, word in (("count-c1", "C1"), ("count-c3", "C3")):
        work = tempfile.mkdtemp(dir=scratch)
        result = run(["python3", "-I", os.path.join(counters, counter + ".py"),
                      rev, "--repo", repo, "--scratch", work])
        out[word] = ("setup" if result.returncode == 2
                     else verdict(result.stdout + result.stderr, word))
    return out


def export_counters(repo, rev, dest):
    os.makedirs(dest, exist_ok=True)
    ok = True
    for counter in (C1, C3):
        result = run(["git", "-C", repo, "show", "%s:%s" % (rev, counter)])
        if result.returncode != 0:
            ok = False
            continue
        path = os.path.join(dest, os.path.basename(counter))
        open(path, "w", encoding="utf-8").write(result.stdout)
    return ok


def selftest(scratch):
    passed = failed = 0

    def check(label, ok, detail=""):
        nonlocal passed, failed
        passed += int(bool(ok))
        failed += int(not ok)
        print("case %s %s %s" % (label, "pass" if ok else "FAIL", detail))

    check("verdict met", verdict("C1=met wrong=0", "C1") == "met")
    check("verdict unmet", verdict("C3=unmet named=0", "C3") == "unmet")
    check("verdict setup", verdict("C1_SETUP archive failed", "C1") == "setup")

    fixtures = build_fixtures(scratch)
    check("seven fixtures", len(fixtures) == 7, str(len(fixtures)))
    check("expectation mix", sum(1 for row in fixtures if row[2] == "met") == 3)

    always_met = tempfile.mkdtemp(dir=scratch)
    for counter, word in (("count-c1", "C1"), ("count-c3", "C3")):
        open(os.path.join(always_met, counter + ".py"), "w", encoding="utf-8").write(
            "import sys\nprint('%s=met stub')\nsys.exit(0)\n" % word)
    results = grade_fixtures(always_met, fixtures, scratch)
    wrong = sum(1 for _, expected, got, _ in results if expected != got)
    check("always-met stub is wrong", wrong == 4, "wrong=%d" % wrong)

    always_unmet = tempfile.mkdtemp(dir=scratch)
    for counter, word in (("count-c1", "C1"), ("count-c3", "C3")):
        open(os.path.join(always_unmet, counter + ".py"), "w", encoding="utf-8").write(
            "import sys\nprint('%s=unmet stub')\nsys.exit(1)\n" % word)
    results = grade_fixtures(always_unmet, fixtures, scratch)
    wrong = sum(1 for _, expected, got, _ in results if expected != got)
    check("always-unmet stub is wrong", wrong == 3, "wrong=%d" % wrong)

    met_rc2 = tempfile.mkdtemp(dir=scratch)
    for counter, word in (("count-c1", "C1"), ("count-c3", "C3")):
        open(os.path.join(met_rc2, counter + ".py"), "w", encoding="utf-8").write(
            "import sys\nprint('%s=met setup-shaped')\nsys.exit(2)\n" % word)
    results = grade_fixtures(met_rc2, fixtures, scratch)
    wrong = sum(1 for _, expected, got, _ in results if expected != got)
    check("met-with-rc2 stub is wrong everywhere", wrong == 7, "wrong=%d" % wrong)

    print("C1_COUNTER_SELFTEST pass=%d fail=%d" % (passed, failed))
    return 0 if not failed else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--repo", default=os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
    ap.add_argument("--scratch")
    ap.add_argument("--counters")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    base = a.scratch or os.environ.get("HYAKU_SCRATCH") or tempfile.gettempdir()
    os.makedirs(base, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="count-c1-r81-", dir=base)
    try:
        if a.selftest:
            return selftest(scratch)
        if not a.rev:
            print("C1_SETUP usage: count-c1.py <rev> | --selftest", file=sys.stderr)
            return 2
        top = run(["git", "-C", a.repo, "rev-parse", "--show-toplevel"])
        repo = top.stdout.strip() if top.returncode == 0 else a.repo
        p = run(["git", "-C", repo, "rev-parse", "--verify", a.rev + "^{commit}"])
        if p.returncode != 0:
            print("C1_SETUP unresolvable revision " + a.rev, file=sys.stderr)
            return 2
        rev = p.stdout.strip()
        if a.counters:
            counters = a.counters
        else:
            counters = os.path.join(scratch, "counters")
            if not export_counters(repo, rev, counters):
                print("C1_SETUP counters absent at rev=" + rev[:12], file=sys.stderr)
                return 2
        fixtures = build_fixtures(scratch)
        results = grade_fixtures(counters, fixtures, scratch)
        for label, expected, got, rc in results:
            print("%s expected=%s got=%s rc=%d" % (label, expected, got, rc))
        wrong = sum(1 for _, expected, got, _ in results if expected != got)
        real = grade_real(counters, repo, rev, scratch)
        print("C1=%s wrong=%d fixtures=%d real_c1=%s real_c3=%s rev=%s"
              % ("met" if wrong == 0 and real["C1"] == "met" and real["C3"] == "met"
                 else "unmet", wrong, len(results), real["C1"], real["C3"], rev[:12]))
        return 0 if wrong == 0 and real["C1"] == "met" and real["C3"] == "met" else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
