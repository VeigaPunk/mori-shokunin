#!/usr/bin/env python3
"""mori round-85 C1 counter (operability): the two surviving r84-counter mutants get their arms.

Frozen predicate P-C1 (`.ufo/waves/round-85/contract.md` — this counter, the contract and the
receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-85/count-c1.py R` prints
  `C1=met mutants=2 killed=2 survivors=0 total=2 arms=17 r84=met` and exits 0, where both `old`
  anchors occur exactly once in `.ufo/waves/round-84/count-c1.py` at R, the pristine copy's own
  `--selftest` is green with exactly 17 arms and carries both new arm labels, each mutated copy's
  own `--selftest` reads killed, and the r84 counter at R still prints its frozen 4-mutant
  `C1=met ... killed=2 equivalent=2 survivors=0 total=4` line, rc 0.

Detector (frozen): a mutant is killed iff the mutated copy's own `--selftest` exits non-zero **or**
prints `fail=<n>` with n > 0, conditional on the pristine copy being green. Green means rc 0, the
token `fail=0` present, and no `fail=<n>` with n > 0. An anchor that does not occur exactly once is
`unanchored` and never counted killed; an empty mutation is `empty-mutation`; a red pristine, an
unanchored anchor, an empty mutation, a red detector or a missing arm label keeps the claim unmet.
Exit 2 is setup, never a pass.

Usage: count-c1.py <rev> [--repo DIR] [--scratch DIR] | count-c1.py --selftest
Output: per mutant `MUTANT count-c1.py <label> killed|survived rc=N`, then the summary line.
Exit 0 met, 1 unmet, 2 setup. Read-only: `git show`; files only under --scratch.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

SUBJECT = ".ufo/waves/round-84/count-c1.py"

# The two survivors the r84 C1 reviewer measured (Mo84R01C1.md §5, X1/X2; anchors at
# `.ufo/waves/round-84/count-c1.py:150-151` at the entering revision).
MUTANTS = (
    (SUBJECT, "X1_killed_rescued_as_equivalent",
     "if not k and coupling is not None:",
     "if coupling is not None:"),
    (SUBJECT, "X2_coupling_duplicate_passes",
     "coupled = all(base.count(marker) == 1 for marker in coupling)",
     "coupled = all(base.count(marker) >= 1 for marker in coupling)"),
)

FAIL = re.compile(r"\bfail=([1-9][0-9]*)\b")
COUNT = re.compile(r"\b(mutants|killed|survivors|total|equivalent)=(\d+)\b")
ARMS = re.compile(r"C1_COUNTER_SELFTEST pass=(\d+) fail=(\d+)")
SUBJECT_MARKERS = ("killed_mutant_with_coupling_not_equivalent",
                   "duplicate_coupling_not_equivalent",
                   "C1_COUNTER_SELFTEST")
FROZEN_MARKERS = SUBJECT_MARKERS
# P-C1 target split: killed=2 survivors=0 total=2, arms=17, r84=met.
TARGET = (2, 0, 2)
TARGET_ARMS = 17
TAIL_ARMS = re.compile(r"\barms=(\d+)\b")
# The r84 counter's own frozen target line (P-C1 of round 84) must keep printing met at R.
R84 = re.compile(r"C1=met\s+mutants=4\s+killed=2\s+equivalent=2\s+survivors=0\s+total=4\b")


def run(cmd, cwd=None, env=None, timeout=300):
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


def arms_of(out):
    """The selftest's own pass/fail tally as (pass, fail), or (-1, -1)."""
    m = None
    for m in ARMS.finditer(out):
        pass
    if m is None:
        return -1, -1
    return int(m.group(1)), int(m.group(2))


def target_split(tail):
    fields = dict((key, int(value)) for key, value in COUNT.findall(tail))
    return (fields.get("killed"), fields.get("survivors"),
            fields.get("total")) == TARGET


def subject_ok(text):
    return text is not None and all(marker in text for marker in FROZEN_MARKERS)


def arms_ok(rc, out):
    """Pristine green with exactly ARMS arms and both new arm labels reading PASS."""
    passed, failed = arms_of(out)
    return (green(rc, out) and failed == 0 and passed == TARGET_ARMS
            and all(("PASS " + marker) in out for marker in
                    SUBJECT_MARKERS[:2]))


def grade(loader, scratch, mutants=MUTANTS):
    """Grade every anchored mutant at one revision. Returns (met, tail, lines, extras)."""
    lines, extras = [], []
    pristine_ok = True
    arms = -1
    by_file = {}
    for path, label, old, new in mutants:
        by_file.setdefault(path, []).append((label, old, new))
    total = 0
    for path in sorted(by_file):
        try:
            base = loader(path)
        except Exception as exc:                     # noqa: BLE001 - report, never crash
            return False, "setup=read:%s:%s" % (path, exc), lines, extras
        if base is None:
            return False, "setup=absent:%s" % path, lines, extras
        tree = os.path.join(scratch, "pristine-" + os.path.basename(path))
        target = os.path.join(tree, path)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        open(target, "w", encoding="utf-8").write(base)
        rc, out = selftest_run(target, scratch)
        arms = arms_of(out)[0]
        if not green(rc, out):
            pristine_ok = False
            extras.append("pristine-red %s rc=%d arms=%d %s" %
                          (path, rc, arms, out.strip().splitlines()[-1:] or ""))
        for label, old, new in by_file[path]:
            if base.count(old) != 1:
                extras.append("unanchored %s %s occurrences=%d"
                              % (path, label, base.count(old)))
                continue
            mutated = base.replace(old, new)
            if mutated == base:
                extras.append("empty-mutation %s %s" % (path, label))
                continue
            d = os.path.join(scratch, "mut-" + os.path.basename(path) + "-" + label)
            target = os.path.join(d, path)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            open(target, "w", encoding="utf-8").write(mutated)
            rc, out = selftest_run(target, scratch)
            k = killed(rc, out)
            total += 1
            lines.append("MUTANT %s %s %s rc=%d"
                         % (os.path.basename(path), label,
                            "killed" if k else "survived", rc))
            if not k:
                extras.append("survivor %s %s" % (path, label))
            shutil.rmtree(d, ignore_errors=True)
    survivors = len([line for line in lines if " survived " in line])
    killed_n = total - survivors
    met = (pristine_ok and total > 0 and survivors == 0
           and not any(e.startswith(("empty-mutation", "unanchored")) for e in extras))
    tail = ("mutants=%d killed=%d survivors=%d total=%d arms=%d"
            % (total, killed_n, survivors, total, arms))
    return met, tail, lines, extras


def r84_at_rev(subject_path, rev, repo, scratch):
    """Run the r84 counter at `rev`; return (ok, tail_line)."""
    work = tempfile.mkdtemp(dir=scratch)
    env = dict(os.environ)
    env.update(TMPDIR=work, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
    try:
        p = run(["python3", "-I", subject_path, rev, "--repo", repo, "--scratch", work],
                cwd=work, env=env)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    finally:
        shutil.rmtree(work, ignore_errors=True)
    out = (p.stdout or "") + (p.stderr or "")
    line = ""
    for candidate in out.splitlines():
        if candidate.startswith("C1="):
            line = candidate.strip()
    return (p.returncode == 0 and bool(R84.search(out))), line


def selfcheck(scratch):
    """Detector arms over synthetic counter copies (no lane file is touched)."""
    cases = []

    def write(d, name, body):
        os.makedirs(os.path.join(d, "tools"), exist_ok=True)
        path = os.path.join(d, "tools", name)
        open(path, "w", encoding="utf-8").write(body)
        return path

    sensitive = ("import sys\nGUARD = 1\n"
                 "ok = GUARD == 1\n"
                 "print('FAKE pass=%d fail=%d' % (1 if ok else 0, 0 if ok else 1))\n"
                 "sys.exit(0 if ok else 1)\n")
    blind = "print('FAKE pass=1 fail=0')\n"
    d = tempfile.mkdtemp(dir=scratch)
    write(d, "sensitive.py", sensitive)
    write(d, "blind.py", blind)
    write(d, "arms17.py",
          "print('PASS killed_mutant_with_coupling_not_equivalent x')\n"
          "print('PASS duplicate_coupling_not_equivalent x')\n"
          "print('C1_COUNTER_SELFTEST pass=17 fail=0')\n")

    def disk(p):
        return open(os.path.join(d, p), encoding="utf-8").read()

    met, tail, lines, _ = grade(
        disk, scratch, [("tools/sensitive.py", "X1_killed_rescued_as_equivalent",
                         "GUARD = 1", "GUARD = 0")])
    fields = dict((k, int(v)) for k, v in COUNT.findall(tail))
    cases.append(("killed_counted",
                  met and fields.get("killed") == 1 and fields.get("total") == 1, tail))
    met, tail, lines, _ = grade(
        disk, scratch, [("tools/blind.py", "X2_coupling_duplicate_passes",
                         "print('FAKE pass=1 fail=0')",
                         "print('FAKE pass=1 fail=0') # noop")])
    fields = dict((k, int(v)) for k, v in COUNT.findall(tail))
    cases.append(("survivor_counted",
                  (not met) and fields.get("survivors") == 1, tail))
    cases.append(("arms_parse",
                  arms_of("noise\nC1_COUNTER_SELFTEST pass=17 fail=0\n") == (17, 0),
                  "17/0"))
    cases.append(("arms_floor",
                  not arms_ok(0, "PASS x\nC1_COUNTER_SELFTEST pass=15 fail=0\n"),
                  "15 arms"))
    cases.append(("arms_requires_labels",
                  not arms_ok(0, "C1_COUNTER_SELFTEST pass=17 fail=0\n"), "no labels"))
    cases.append(("arms_green",
                  arms_ok(0, "PASS killed_mutant_with_coupling_not_equivalent x\n"
                          "PASS duplicate_coupling_not_equivalent x\n"
                          "C1_COUNTER_SELFTEST pass=17 fail=0\n"), "17 arms"))
    cases.append(("green_boundary",
                  green(0, "FAKE pass=1 fail=0") and not green(0, "SELFTEST skipped")
                  and not green(0, "FAKE pass=1 fail=2") and not green(1, "FAKE pass=1 fail=0"),
                  "green()"))
    cases.append(("killed_boundary",
                  killed(1, "traceback") and killed(0, "FAKE pass=1 fail=2")
                  and not killed(0, "FAKE pass=1 fail=0"), "killed()"))
    dup = "GUARD = 1\nGUARD = 1\nprint('FAKE pass=1 fail=0')\n"
    write(d, "dup.py", dup)
    met, tail, lines, extras = grade(
        disk, scratch, [("tools/dup.py", "X1_killed_rescued_as_equivalent",
                         "GUARD = 1", "GUARD = 0")])
    cases.append(("unanchored_excluded",
                  (not met) and "unanchored" in " ".join(extras), tail))
    empty = "GUARD = 1\nprint('FAKE pass=1 fail=0')\n"
    write(d, "empty.py", empty)
    met, tail, lines, extras = grade(
        disk, scratch, [("tools/empty.py", "X2_coupling_duplicate_passes",
                         "GUARD = 1", "GUARD = 1")])
    cases.append(("empty_mutation_unmet",
                  (not met) and "empty-mutation" in " ".join(extras), tail))
    red = "print('FAKE pass=0 fail=1')\nraise SystemExit(1)\n"
    write(d, "red.py", red)
    met, tail, lines, extras = grade(
        disk, scratch, [("tools/red.py", "X1_killed_rescued_as_equivalent",
                         "fail=1", "fail=2")])
    cases.append(("red_pristine_reported",
                  (not met) and "pristine-red" in " ".join(extras), tail))
    cases.append(("target_split_ok",
                  target_split("mutants=2 killed=2 survivors=0 total=2 arms=17")
                  and int(TAIL_ARMS.search("arms=17").group(1)) == TARGET_ARMS,
                  "2/0/2 arms=17"))
    cases.append(("target_split_free",
                  not target_split("mutants=2 killed=1 survivors=1 total=2 arms=17"),
                  "1/1/2"))
    cases.append(("r84_target_ok",
                  bool(R84.search("C1=met mutants=4 killed=2 equivalent=2 "
                                  "survivors=0 total=4 pristine=green detector=green")),
                  "r84 met"))
    cases.append(("r84_target_free",
                  not R84.search("C1=met mutants=4 killed=3 equivalent=1 "
                                "survivors=0 total=4"), "3/1/4"))
    cases.append(("subject_markers_ok",
                  subject_ok("x killed_mutant_with_coupling_not_equivalent "
                             "duplicate_coupling_not_equivalent C1_COUNTER_SELFTEST"), "all"))
    cases.append(("subject_markers_missing",
                  not subject_ok("x C1_COUNTER_SELFTEST"), "one"))
    cases.append(("marker_literal",
                  "X1_killed_rescued_as_equivalent" in open(os.path.abspath(__file__)).read(),
                  "X1 label"))
    ok = sum(1 for _, good, _ in cases if good)
    for label, good, line in cases:
        print("%s %s %s" % ("PASS" if good else "FAIL", label, line))
    print("C1_COUNTER_SELFTEST pass=%d fail=%d" % (ok, len(cases) - ok))
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
    scratch = tempfile.mkdtemp(prefix="count-c1-r85-", dir=base)
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
            print("C1_SETUP unresolvable revision " + a.rev, file=sys.stderr)
            return 2
        rev = p.stdout.strip()

        def loader(path):
            q = run(["git", "-C", repo, "show", "%s:%s" % (rev, path)])
            return q.stdout if q.returncode == 0 else None

        own = run(["python3", "-I", os.path.abspath(__file__), "--selftest",
                   "--scratch", scratch])
        own_out = (own.stdout or "") + (own.stderr or "")
        own_ok = (own.returncode == 0 and "C1_COUNTER_SELFTEST" in own_out
                  and re.search(r"C1_COUNTER_SELFTEST pass=(\d+) fail=0", own_out) is not None)
        harness = loader(SUBJECT)
        if harness is None:
            print("C1=unmet mutants=2 harness=absent rev=%s" % rev[:12])
            return 1
        met, tail, lines, extras = grade(loader, scratch)
        for line in lines:
            print(line)
        for extra in extras:
            print("EXTRA " + extra)
        if not own_ok:
            print("C1=unmet %s detector=red rev=%s" % (tail, rev[:12]))
            print(own_out.strip())
            return 1
        missing = [m for m in FROZEN_MARKERS if m not in harness]
        if missing:
            print("C1=unmet %s harness=stub missing=%s rev=%s"
                  % (tail, ",".join(missing), rev[:12]))
            return 1
        if not subject_ok(loader(SUBJECT)):
            print("C1=unmet %s subject=absent-arms rev=%s" % (tail, rev[:12]))
            return 1
        tail_arms = TAIL_ARMS.search(tail)
        if (not met or not target_split(tail)
                or tail_arms is None or int(tail_arms.group(1)) != TARGET_ARMS):
            print("C1=unmet %s detector=green rev=%s" % (tail, rev[:12]))
            return 1
        tree = os.path.join(scratch, "pristine-r84")
        target = os.path.join(tree, SUBJECT)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        open(target, "w", encoding="utf-8").write(harness)
        r84_ok, r84_line = r84_at_rev(target, rev, repo, scratch)
        if not r84_ok:
            print("C1=unmet %s r84=unmet rev=%s" % (tail, rev[:12]))
            print(r84_line)
            return 1
        print("C1=met %s r84=met rev=%s" % (tail, rev[:12]))
        return 0
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
