#!/usr/bin/env python3
"""mori round-84 C1 counter (operability): the r83 counter family's four extra mutants.

Frozen predicate P-C1 (`.ufo/waves/round-84/contract.md` — this counter, the contract and the
receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-84/count-c1.py R` prints
  `C1=met mutants=4 killed=K equivalent=E survivors=0 total=4 pristine=green detector=green`
  and exits 0, where the four-mutant table below is re-derived from R's bytes (each `old` anchor
  occurs exactly once in the named file at R), every mutated copy's own `--selftest` is run in
  scratch and reads killed, a surviving mutant with a registered equivalence counts `equivalent`
  only while every coupling marker of that equivalence occurs exactly once in the graded file, the
  pristine files' own `--selftest` runs are green first, and the counter's own detector selftest
  passes in the same invocation.

Detector (frozen): a mutant is killed iff the mutated copy's own `--selftest` exits non-zero **or**
prints `fail=<n>` with n > 0, conditional on the pristine copy being green. An anchor that does not
occur exactly once is `unanchored` and never counted killed; an empty mutation is
`empty-mutation`; a red pristine, an unanchored anchor, an empty mutation, a missing equivalence
coupling or a red detector keeps the claim unmet. Exit 2 is setup, never a pass.

Usage: count-c1.py <rev> [--repo DIR] [--scratch DIR] | count-c1.py --selftest
Output: per mutant `MUTANT <file> <label> killed|equivalent|survived rc=N`, then the summary line.
Exit 0 met, 1 unmet, 2 setup. Read-only: `git show`; files only under --scratch.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

# The four mutants the r83 C1 reviewer measured at c4845c83 (Mo83R01C1.md §6, M24a-M24d).
MUTANTS = (
    (".ufo/waves/round-83/count-c1.py", "M24a_killed_tally",
     "killed_n = total - survivors - equivalent",
     "killed_n = total - equivalent"),
    (".ufo/waves/round-83/count-c1.py", "M24b_green_fail_token",
     '    return rc == 0 and "fail=0" in out and not FAIL.search(out)',
     "    return rc == 0 and not FAIL.search(out)"),
    (".ufo/waves/round-83/count-c2.py", "M24c_met_unclassified",
     "and not unclassified", ""),
    (".ufo/waves/round-83/count-c2.py", "M24d_met_residual",
     "and residual == 0", ""),
)

# A1-style adjudication: a surviving mutant is `equivalent` only while every coupling marker
# occurs exactly once in the graded file (the coupling is the proof).
EQUIVALENT = {
    "M24c_met_unclassified": ("agreed == len(snapshot_tokens)",),
    "M24d_met_residual": ("agreed == len(snapshot_tokens)",
                          "residual += duplicates",
                          "duplicates == 0"),
}

FAIL = re.compile(r"\bfail=([1-9][0-9]*)\b")
COUNT = re.compile(r"\b(mutants|killed|equivalent|survivors|total)=(\d+)\b")
# A revision's `harness=present` means the file IS this counter: every frozen label and the
# detector-selftest marker must be in its bytes (an existence-only check passes a stub).
FROZEN_MARKERS = tuple(label for _, label, _, _ in MUTANTS) + ("C1_COUNTER_SELFTEST",)
# The graded subject must carry the two arms this round claims to land (A5: a tripwire subject
# with no arms killed every mutant and printed the target line; the labels are the cheap binding).
SUBJECT = ".ufo/waves/round-83/count-c1.py"
SUBJECT_MARKERS = ("blind_case_tally", "green_requires_fail_zero")
# The frozen target's split (contract.md P-C1): killed=2 equivalent=2 total=4.
TARGET = (2, 2, 4)


def run(cmd, cwd=None, env=None, timeout=240):
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


def target_split(tail):
    """The frozen 2/2/4 split, not merely survivors == 0."""
    fields = dict((key, int(value)) for key, value in COUNT.findall(tail))
    return (fields.get("killed"), fields.get("equivalent"),
            fields.get("total")) == TARGET


def subject_ok(text):
    return text is not None and all(marker in text for marker in SUBJECT_MARKERS)


def grade(loader, scratch, mutants=MUTANTS):
    """Grade every anchored mutant at one revision. Returns (met, tail, lines, extras)."""
    lines, extras = [], []
    pristine_ok = True
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
        if not green(rc, out):
            pristine_ok = False
            extras.append("pristine-red %s rc=%d %s" %
                          (path, rc, out.strip().splitlines()[-1:] or ""))
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
            coupling = EQUIVALENT.get(label)
            if not k and coupling is not None:
                coupled = all(base.count(marker) == 1 for marker in coupling)
                lines.append("MUTANT %s %s %s rc=%d"
                             % (os.path.basename(path), label,
                                "equivalent" if coupled else "survived", rc))
                if not coupled:
                    extras.append("coupling-absent %s %s" % (path, label))
                continue
            lines.append("MUTANT %s %s %s rc=%d"
                         % (os.path.basename(path), label,
                            "killed" if k else "survived", rc))
            shutil.rmtree(d, ignore_errors=True)
    survivors = len([line for line in lines if " survived " in line])
    equivalent = len([line for line in lines if " equivalent " in line])
    killed_n = total - survivors - equivalent
    met = (pristine_ok and total > 0 and survivors == 0
           and not any(e.startswith("empty-mutation") or e.startswith("unanchored")
                       or e.startswith("coupling-absent") for e in extras))
    tail = ("mutants=%d killed=%d equivalent=%d survivors=%d total=%d pristine=%s"
            % (total, killed_n, equivalent, survivors, total,
               "green" if pristine_ok else "red"))
    return met, tail, lines, extras


def selfcheck(scratch):
    """Detector arms over synthetic selftest counters (no lane file is touched)."""
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
    skipped = "print('SELFTEST skipped')\n"
    d = tempfile.mkdtemp(dir=scratch)
    write(d, "sensitive.py", sensitive)
    write(d, "blind.py", blind)
    write(d, "skipped.py", skipped)

    def disk(p):
        return open(os.path.join(d, p), encoding="utf-8").read()

    met, tail, lines, extras = grade(
        disk, scratch,
        [("tools/sensitive.py", "trip_guard", "GUARD = 1", "GUARD = 0")])
    fields = dict((k, int(v)) for k, v in COUNT.findall(tail))
    cases.append(("sensitive_killed",
                  met and fields.get("killed") == 1 and fields.get("survivors") == 0
                  and fields.get("total") == 1, tail + " | " + ";".join(lines)))
    met, tail, lines, _ = grade(
        disk, scratch,
        [("tools/blind.py", "noop", "print('FAKE pass=1 fail=0')",
          "print('FAKE pass=1 fail=0') # noop")])
    fields = dict((k, int(v)) for k, v in COUNT.findall(tail))
    cases.append(("blind_survives", (not met) and fields.get("survivors") == 1, tail))
    # tally arm: a blind case beside a killed one must print killed=0, survivors=1 (M24a)
    met, tail, lines, _ = grade(
        disk, scratch,
        [("tools/sensitive.py", "trip_guard", "GUARD = 1", "GUARD = 0"),
         ("tools/blind.py", "noop", "print('FAKE pass=1 fail=0')",
          "print('FAKE pass=1 fail=0') # noop")])
    fields = dict((k, int(v)) for k, v in COUNT.findall(tail))
    cases.append(("blind_case_tally",
                  (not met) and fields.get("killed") == 1
                  and fields.get("survivors") == 1 and fields.get("total") == 2, tail))
    # green() must require the fail=0 token: a rc-0 run without it is not a green pristine (M24b)
    met, tail, lines, _ = grade(
        disk, scratch,
        [("tools/skipped.py", "noop", "print('SELFTEST skipped')",
          "print('SELFTEST skipped') # noop")])
    cases.append(("green_requires_fail_zero",
                  (not met) and "pristine=red" in tail, tail))
    cases.append(("green_direct",
                  green(0, "FAKE pass=1 fail=0") and not green(0, "SELFTEST skipped")
                  and not green(0, "FAKE pass=1 fail=2") and not green(1, "FAKE pass=1 fail=0"),
                  "green() boundary"))
    cases.append(("killed_direct",
                  killed(1, "traceback") and killed(0, "FAKE pass=1 fail=2")
                  and not killed(0, "FAKE pass=1 fail=0"), "killed() boundary"))
    dup = "GUARD = 1\nGUARD = 1\nprint('FAKE pass=1 fail=0')\n"
    write(d, "dup.py", dup)
    met, tail, lines, extras = grade(
        disk, scratch,
        [("tools/dup.py", "twice", "GUARD = 1", "GUARD = 0"),
         ("tools/dup.py", "second", "GUARD = 1", "GUARD = 2")])
    cases.append(("duplicate_anchor_excluded",
                  (not met) and "unanchored" in " ".join(extras)
                  and "total=0" in tail, tail))
    empty = "GUARD = 1\nprint('FAKE pass=1 fail=0')\n"
    write(d, "empty.py", empty)
    met, tail, lines, extras = grade(
        disk, scratch, [("tools/empty.py", "same", "GUARD = 1", "GUARD = 1")])
    cases.append(("empty_mutation_unmet",
                  (not met) and "empty-mutation" in " ".join(extras), tail))
    red = "print('FAKE pass=0 fail=1')\nraise SystemExit(1)\n"
    write(d, "red.py", red)
    met, tail, lines, extras = grade(
        disk, scratch, [("tools/red.py", "self_red", "pass=0", "pass=0")])
    cases.append(("red_pristine_reported",
                  (not met) and "pristine=red" in tail, tail))
    eq = ("GUARD = 1\nCOUPLE = 2\n"
          "def f(duplicates, residual):\n    residual += duplicates\n"
          "    return residual\n"
          "# coupling: agreed == len(snapshot_tokens) and duplicates == 0\n"
          "print('FAKE pass=1 fail=0')\n")
    write(d, "eq.py", eq)
    met, tail, lines, extras = grade(
        disk, scratch, [("tools/eq.py", "M24d_met_residual", "COUPLE = 2", "COUPLE = 3")])
    cases.append(("equivalent_excluded_when_coupled",
                  met and "equivalent=1" in tail and "survivors=0" in tail, tail))
    bare = "GUARD = 1\nprint('FAKE pass=1 fail=0')\n"
    write(d, "bare.py", bare)
    met, tail, lines, extras = grade(
        disk, scratch, [("tools/bare.py", "M24d_met_residual", "GUARD = 1", "GUARD = 0")])
    cases.append(("equivalent_requires_coupling",
                  (not met) and "coupling-absent" in " ".join(extras)
                  and "survivors=1" in tail, tail))
    cases.append(("target_split_ok",
                  target_split("mutants=4 killed=2 equivalent=2 survivors=0 total=4"),
                  "2/2/4"))
    cases.append(("target_split_free",
                  not target_split("mutants=4 killed=4 equivalent=0 survivors=0 total=4"),
                  "4/0/4"))
    cases.append(("subject_markers_ok",
                  subject_ok("x blind_case_tally y green_requires_fail_zero"), "both"))
    cases.append(("subject_markers_missing",
                  not subject_ok("x blind_case_tally"), "one"))
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
    scratch = tempfile.mkdtemp(prefix="count-c1-r84-", dir=base)
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

        harness = loader(".ufo/waves/round-84/count-c1.py")
        if harness is None:
            print("C1=unmet harness=absent rev=%s" % rev[:12])
            return 1
        missing = [m for m in FROZEN_MARKERS if m not in harness]
        if missing:
            print("C1=unmet harness=stub missing=%s rev=%s"
                  % (",".join(missing), rev[:12]))
            return 1
        own = run(["python3", "-I", os.path.abspath(__file__), "--selftest",
                   "--scratch", scratch])
        own_out = (own.stdout or "") + (own.stderr or "")
        own_ok = (own.returncode == 0 and "C1_COUNTER_SELFTEST" in own_out
                  and re.search(r"C1_COUNTER_SELFTEST pass=(\d+) fail=0", own_out) is not None)
        met, tail, lines, extras = grade(loader, scratch)
        for line in lines:
            print(line)
        for extra in extras:
            print("EXTRA " + extra)
        if not (met and own_ok):
            print("C1=unmet %s detector=%s rev=%s"
                  % (tail, "green" if own_ok else "red", rev[:12]))
            if not own_ok:
                print(own_out.strip())
            return 1
        subject = loader(SUBJECT)
        if not subject_ok(subject):
            print("C1=unmet subject=absent-arms missing=%s %s rev=%s"
                  % (",".join(m for m in SUBJECT_MARKERS
                              if subject is None or m not in subject), tail, rev[:12]))
            return 1
        if not target_split(tail):
            print("C1=unmet target=split %s rev=%s" % (tail, rev[:12]))
            return 1
        print("C1=met %s detector=green rev=%s" % (tail, rev[:12]))
        return 0
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
