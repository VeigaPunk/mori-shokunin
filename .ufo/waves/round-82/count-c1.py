#!/usr/bin/env python3
"""mori round-82 C1 counter (operability): committed, revision-agnostic mutation harness.

Frozen predicate P-C1 (`.ufo/waves/round-82/contract.md` — this counter, the contract and the
receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-82/count-c1.py R` prints
  `C1=met harness=present killed=K survivors=0 total=T pristine=green` and exits 0, where `T` is
  the mutant set re-derived at R (each mutant's `old` anchor occurs exactly once in the named
  file at R), every one of those mutants is killed, and the three pristine files' own
  `--selftest` runs are green first. At the entering revision `ebcf2c72` the harness does not
  exist: `C1=unmet harness=absent`, rc 1.

Detector: a mutant is killed iff the mutated copy's own `--selftest` exits non-zero **or** prints
`fail=<n>` with n > 0, conditional on the pristine copy being green. An anchor that does not
occur exactly once is reported as `unanchored` and is not graded (never counted as killed). A
setup exit is never a pass.

The population is the r81 mutation seat's set (`.ufo/waves/round-81/w1/Mo81M01Mutants.md`)
minus its `accept_sibling` anchor, which no longer exists in the r81-fixed `count-c3.py`: the
r80 bytes graded one sibling shape, the r81 bytes grade the same behaviour through the `own`
prefix token and the `own_lane_prefix_allowed`/`sibling_and_directory_ignored` arms.

Usage: count-c1.py <rev> [--repo DIR] [--scratch DIR] | count-c1.py --selftest
Output: per mutant `MUTANT <file> <label> killed|survived rc=N`, then the summary line.
Exit 0 met, 1 unmet, 2 setup. Read-only: `git show`; files only under --scratch.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

MUTANTS = (
    (".ufo/waves/round-80/count-c1.py", "ignore_row_disagreement",
     "if readings and len(set(readings)) == 1:", "if readings:"),
    (".ufo/waves/round-80/count-c1.py", "ignore_mismatch_lines",
     'and not any(line.startswith("CLAIM_SWEEP_MISMATCH")',
     'and not any(False and line.startswith("CLAIM_SWEEP_MISMATCH")'),
    (".ufo/waves/round-80/count-c1.py", "ignore_stale_field",
     "and tallies == 0 and stale == 0 and stated == live)",
     "and tallies == 0 and stated == live)"),
    (".ufo/waves/round-80/count-c1.py", "ignore_sweep_exit",
     "met = (p.returncode == 0 and sweep_consistent", "met = (sweep_consistent"),
    (".ufo/waves/round-80/count-c3.py", "ignore_missing",
     "met = not missing and not extra", "met = not extra"),
    (".ufo/waves/round-80/count-c3.py", "ignore_extra",
     "met = not missing and not extra", "met = not missing"),
    (".ufo/waves/round-80/count-c3.py", "drop_right_boundary", "(?![\\w.-])", ""),
    (".ufo/waves/round-81/count-c2.py", "pending_all_sections",
     "section is None or not ROUND_SECTION.match(section) or not ROW.match(line)",
     "section is None or not ROW.match(line)"),
    (".ufo/waves/round-81/count-c2.py", "pending_substring",
     'if cell == "PENDING":', 'if "PENDING" in cell:'),
    (".ufo/waves/round-81/count-c2.py", "ignore_command_exit",
     "or result.returncode != 0 or stated != live:", "or stated != live:"),
    (".ufo/waves/round-81/count-c2.py", "first_binding_only",
     "for binding in bindings:", "for binding in bindings[:1]:"),
)

FAIL = re.compile(r"\bfail=([1-9][0-9]*)\b")
KILL_TOKEN = re.compile(r"\bkilled=(\d+)\b")
SURVIVOR_TOKEN = re.compile(r"\bsurvivors=(\d+)\b")
TOTAL_TOKEN = re.compile(r"\btotal=(\d+)\b")
# A revision's `harness=present` means the file IS this harness: every frozen mutant label and
# the detector-selftest marker must be in its bytes (C01: an existence-only check passed a stub).
FROZEN_MARKERS = tuple(label for _, label, _, _ in MUTANTS) + ("C1_COUNTER_SELFTEST",)

# Sibling files a counter's own --selftest reads from its repo root (r81 count-c2 reads its
# record-pins.json beside it; r80 count-c1 writes its own pins in-fixture but the file exists).
SUPPORT = {
    ".ufo/waves/round-80/count-c1.py": [".ufo/waves/round-80/claim-pins.json"],
    ".ufo/waves/round-81/count-c2.py": [".ufo/waves/round-81/record-pins.json"],
}


def run(cmd, cwd=None, env=None, timeout=180):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          env=env, timeout=timeout)


def selftest_run(path, scratch):
    """Run one counter copy's own --selftest. Returns (rc, combined output)."""
    work = tempfile.mkdtemp(dir=scratch)
    env = dict(os.environ)
    env.update(TMPDIR=work, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
    try:
        p = run(["python3", "-I", path, "--selftest", "--scratch", work],
                cwd=work, env=env)
    except subprocess.TimeoutExpired:
        return 124, "timeout"
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def green(rc, out):
    return rc == 0 and "fail=0" in out and not FAIL.search(out)


def killed(rc, out):
    return rc != 0 or bool(FAIL.search(out))


def grade(loader, scratch, mutants=MUTANTS):
    """Grade every anchored mutant at one revision. Returns (met, tail, lines, extras)."""
    lines, extras = [], []
    pristine_ok = True
    by_file = {}
    for path, label, old, new in mutants:
        by_file.setdefault(path, []).append((label, old, new))
    counts = {}
    for path in sorted(by_file):
        try:
            base = loader(path)
        except Exception as exc:                     # noqa: BLE001 - report, never crash
            return False, f"setup=read:{path}:{exc}", lines, extras
        if base is None:
            return False, f"setup=absent:{path}", lines, extras
        anchors = [old for _, old, _ in by_file[path]]
        for (label, old, new), count in zip(by_file[path], [base.count(a) for a in anchors]):
            if count != 1:
                extras.append(f"unanchored {path} {label} occurrences={count}")
        tree = os.path.join(scratch, "pristine-" + os.path.basename(path))
        os.makedirs(os.path.dirname(os.path.join(tree, path)), exist_ok=True)
        open(os.path.join(tree, path), "w", encoding="utf-8").write(base)
        for extra_path in SUPPORT.get(path, ()):
            body = loader(extra_path)
            if body is None:
                extras.append(f"support-absent {extra_path}")
                pristine_ok = False
                continue
            os.makedirs(os.path.dirname(os.path.join(tree, extra_path)), exist_ok=True)
            open(os.path.join(tree, extra_path), "w", encoding="utf-8").write(body)
        rc, out = selftest_run(os.path.join(tree, path), scratch)
        if not green(rc, out):
            pristine_ok = False
            extras.append(f"pristine-red {path} rc={rc} {out.strip().splitlines()[-1:]}")
        checks = []

        for label, old, new in by_file[path]:
            if base.count(old) != 1:
                continue
            mutated = base.replace(old, new)
            if mutated == base:
                extras.append(f"empty-mutation {path} {label}")
                continue
            d = os.path.join(scratch, "mut-" + os.path.basename(path) + "-" + label)
            target = os.path.join(d, path)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            open(target, "w", encoding="utf-8").write(mutated)
            for extra_path in SUPPORT.get(path, ()):
                body = loader(extra_path)
                if body is None:
                    continue
                os.makedirs(os.path.dirname(os.path.join(d, extra_path)), exist_ok=True)
                open(os.path.join(d, extra_path), "w", encoding="utf-8").write(body)
            rc, out = selftest_run(target, scratch)
            k = killed(rc, out)
            checks.append((path, label, k, rc))
            shutil.rmtree(d, ignore_errors=True)
        counts[path] = len(checks)
        for path_, label, k, rc in checks:
            lines.append(f"MUTANT {os.path.basename(path_)} {label} "
                         f"{'killed' if k else 'survived'} rc={rc}")
    total = sum(counts.values())
    survivors = len([line for line in lines if " survived " in line])
    killed_n = total - survivors
    met = pristine_ok and total > 0 and survivors == 0 and not any(
        e.startswith("empty-mutation") or e.startswith("unanchored") for e in extras)
    tail = (f"harness=present killed={killed_n} survivors={survivors} total={total} "
            f"pristine={'green' if pristine_ok else 'red'}")
    return met, tail, lines, extras


def detector_repo():
    """Lane repo for the red-detector arm: the checkout this file lives in, else the
    lane checkout under ~ — the arm also runs from scratch copies whose --selftest is
    graded by a later counter (no --repo reaches them; those copies mirror the lane
    layout but are not git checkouts, so the isfile probe alone is not enough)."""
    here = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
    if os.path.isfile(os.path.join(here, ".ufo", "waves", "round-82", "count-c1.py")):
        if run(["git", "-C", here, "rev-parse", "--verify", "HEAD"]).returncode == 0:
            return here
    return os.path.expanduser(os.path.join("~", "Projects", "shokunin", "mori-shokunin"))


def selfcheck(scratch):
    """Detector arms over synthetic selftest counters (no lane file is touched)."""
    cases = []

    def write(d, name, body, anchor):
        os.makedirs(os.path.join(d, "tools"), exist_ok=True)
        open(os.path.join(d, "tools", name), "w", encoding="utf-8").write(body)
        return os.path.join(d, "tools", name)

    sensitive = ("import sys\nGUARD = 1\n"
                 "ok = GUARD == 1\n"
                 "print('FAKE pass=%d fail=%d' % (1 if ok else 0, 0 if ok else 1))\n"
                 "sys.exit(0 if ok else 1)\n")
    blind = ("print('FAKE pass=1 fail=0')\n")
    d = tempfile.mkdtemp(dir=scratch)
    write(d, "sensitive.py", sensitive, "GUARD = 1")
    write(d, "blind.py", blind, "print('FAKE pass=1 fail=0')")
    disk = lambda p: open(os.path.join(d, p), encoding="utf-8").read()  # noqa: E731
    met, tail, lines, extras = grade(
        disk, scratch,
        [("tools/sensitive.py", "trip_guard", "GUARD = 1", "GUARD = 0")])
    km = KILL_TOKEN.search(tail)
    sm = SURVIVOR_TOKEN.search(tail)
    tm = TOTAL_TOKEN.search(tail)
    cases.append(("sensitive_killed",
                  met and km and sm and tm and km.group(1) == "1" and sm.group(1) == "0"
                  and tm.group(1) == "1", tail + " | " + ";".join(lines)))
    met, tail, lines, _ = grade(
        disk, scratch, [("tools/blind.py", "noop", "print('FAKE pass=1 fail=0')",
                         "print('FAKE pass=1 fail=0') # noop")])
    bs = SURVIVOR_TOKEN.search(tail)
    cases.append(("blind_survives", (not met) and bs and bs.group(1) == "1", tail))
    dup = ("GUARD = 1\nGUARD = 1\n"
           "print('FAKE pass=1 fail=0')\n")
    write(d, "dup.py", dup, None)
    met, tail, lines, extras = grade(
        disk, scratch, [("tools/dup.py", "twice", "GUARD = 1", "GUARD = 0"),
                        ("tools/dup.py", "second", "GUARD = 1", "GUARD = 2")])
    cases.append(("duplicate_anchor_excluded",
                  (not met) and "unanchored" in " ".join(extras)
                  and "total=0" in tail, tail))
    red = ("print('FAKE pass=0 fail=1')\nraise SystemExit(1)\n")
    write(d, "red.py", red, None)
    met, tail, lines, extras = grade(
        disk, scratch, [("tools/red.py", "self_red", "pass=0", "pass=0")])
    cases.append(("red_pristine_reported",
                  (not met) and "pristine=red" in tail, tail))
    # green_ignores_fail_token: rc 0 while printing both fail=0 and a real fail=2 token
    # must NOT read green — the pristine copy goes red, a green() without the FAIL clause
    # would call it green and lose the arm.
    liar = ("import sys\nGUARD = 1\n"
            "print('FAKE pass=1 fail=0')\n"
            "print('FAILTOKEN fail=2 probe')\n"
            "sys.exit(0 if GUARD == 1 else 1)\n")
    write(d, "liar.py", liar, None)
    met, tail, lines, _ = grade(
        disk, scratch, [("tools/liar.py", "liar_trip", "GUARD = 1", "GUARD = 0")])
    cases.append(("pristine_fail_token_with_rc0",
                  (not met) and "pristine=red" in tail,
                  tail + " | " + ";".join(lines)))
    # killed_ignores_rc: a mutant selftest that exits 1 printing no fail=<n> token
    # (traceback shape) must still count killed; killed() may not lean on FAIL alone.
    quiet = ("import sys\nGUARD = 1\n"
             "print('FAKE pass=%d fail=0' % (1 if GUARD == 1 else 0))\n"
             "sys.exit(0 if GUARD == 1 else 1)\n")
    write(d, "quiet.py", quiet, None)
    met, tail, _, _ = grade(
        disk, scratch, [("tools/quiet.py", "quiet_trip", "GUARD = 1", "GUARD = 0")])
    km = KILL_TOKEN.search(tail)
    sm = SURVIVOR_TOKEN.search(tail)
    cases.append(("rc_only_kill",
                  met and km and sm and km.group(1) == "1" and sm.group(1) == "0", tail))
    # ignore_pristine_red: a red pristine beside one really graded, really killed mutant
    # must keep met False (the total=0 arm above cannot see the pristine clause).
    met, tail, lines, _ = grade(
        disk, scratch,
        [("tools/red.py", "excuse_zero", "raise SystemExit(1)", "raise SystemExit(0)")])
    cases.append(("red_pristine_with_real_mutant",
                  (not met) and "pristine=red" in tail,
                  tail + " | " + ";".join(lines)))
    # accept_empty_population: a zero-mutant population with no disqualifying extras
    # (no unanchored, no empty-mutation, green pristine) must stay unmet.
    met, tail, _, extras = grade(disk, scratch, [])
    cases.append(("empty_population_unmet",
                  (not met) and "total=0" in tail and "pristine=green" in tail
                  and not extras, tail))
    # unanchored_excused: one anchor occurring twice beside a real killed mutant keeps
    # met False — the kill alone must not carry the population.
    met, tail, lines, extras = grade(
        disk, scratch,
        [("tools/dup.py", "twice", "GUARD = 1", "GUARD = 0"),
         ("tools/sensitive.py", "trip_guard", "GUARD = 1", "GUARD = 0")])
    cases.append(("unanchored_blocks_met",
                  (not met) and "unanchored" in " ".join(extras),
                  tail + " | " + ";".join(lines)))
    # detector_gate_dropped: main's exit gate must honour the counter's own detector
    # selftest. A copy of this counter whose ONLY change is a selftest summary printing
    # fail=1 while still exiting 0, run in <rev> mode against the lane tip, must exit 1
    # printing detector=red; a gate without own_ok would exit 0. Skipped inside the
    # doctored copy itself (runtime-assembled marker in its own bytes) so the <rev> run's
    # nested selftest does not recurse.
    probe = "# doctored" + "-detector"
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    orig_line = ('print(f"C1_COUNTER_SELFTEST pass={ok} ' + 'fail={len(cases) - ok}")')
    doct_line = ('print("C1_COUNTER_SELFTEST pass=%d fail=%d" % (ok, 1))  ' + probe)
    detail, good = "arm-error unknown", False
    if probe in src:
        detail, good = "skipped-inside-doctored-copy", True
    elif src.count(orig_line) != 1:
        detail = "summary-print anchor not unique"
    else:
        repo = detector_repo()
        top = run(["git", "-C", repo, "rev-parse", "--show-toplevel"])
        repo = top.stdout.strip() if top.returncode == 0 else repo
        tip = run(["git", "-C", repo, "rev-parse", "--verify", "HEAD"])
        rev = tip.stdout.strip()
        if not rev:
            detail = "lane=unresolvable"
        else:
            work = tempfile.mkdtemp(dir=scratch)
            env = dict(os.environ)
            env.update(TMPDIR=work, GIT_CONFIG_GLOBAL=os.devnull,
                       GIT_CONFIG_SYSTEM=os.devnull)
            try:
                doct = os.path.join(work, "doctored-count-c1.py")
                open(doct, "w", encoding="utf-8").write(src.replace(orig_line, doct_line))
                run_scratch = os.path.join(work, "run")
                os.makedirs(run_scratch, exist_ok=True)
                q = run(["python3", "-I", doct, rev, "--repo", repo,
                         "--scratch", run_scratch], cwd=work, env=env, timeout=600)
                out = (q.stdout or "") + (q.stderr or "")
                detail = "doctored rc=%d detector-line=%s rev=%s" % (
                    q.returncode, "detector=red" in out, rev[:12])
                good = q.returncode == 1 and "detector=red" in out
            except subprocess.TimeoutExpired:
                detail = "doctored run timed out"
            finally:
                shutil.rmtree(work, ignore_errors=True)
    cases.append(("red_detector_never_passes", good, detail))
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
    scratch = tempfile.mkdtemp(prefix="count-c1-r82-", dir=base)
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

        def loader(path):
            q = run(["git", "-C", repo, "show", f"{rev}:{path}"])
            if q.returncode != 0:
                return None
            return q.stdout

        harness = loader(".ufo/waves/round-82/count-c1.py")
        if harness is None:
            print(f"C1=unmet harness=absent rev={rev[:12]}")
            return 1
        missing_markers = [m for m in FROZEN_MARKERS if m not in harness]
        if missing_markers:
            print(f"C1=unmet harness=present markers=missing:{','.join(missing_markers[:3])} "
                  f"rev={rev[:12]}")
            return 1
        own = subprocess.run([sys.executable, "-I", os.path.abspath(__file__),
                              "--selftest", "--scratch", scratch],
                             capture_output=True, text=True, timeout=300)
        own_out = (own.stdout or "") + (own.stderr or "")
        own_ok = own.returncode == 0 and "C1_COUNTER_SELFTEST" in own_out and \
            "fail=0" in own_out
        met, tail, lines, extras = grade(loader, scratch)
        if tail.startswith("setup=absent:"):
            print(f"C1=unmet harness=absent rev={rev[:12]}")
            return 1
        if tail.startswith("setup="):
            print(f"C1_SETUP {tail}", file=sys.stderr)
            return 2
        for line in lines:
            print(line)
        for extra in extras:
            print(extra)
        if not own_ok:
            print("detector-selftest=red " + own_out.strip().splitlines()[-1:][0]
                  if own_out.strip() else "detector-selftest=red")
        print(f"C1={'met' if (met and own_ok) else 'unmet'} {tail} "
              f"detector={'green' if own_ok else 'red'} rev={rev[:12]}")
        return 0 if (met and own_ok) else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
