#!/usr/bin/env python3
"""mori round-87 C1 counter (operability): six surviving r86-counter clauses get their arms.

Frozen predicate P-C1 (`.ufo/waves/round-87/contract.md` — this file, the contract and the
receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-87/count-c1.py R` prints
  `C1=met mutants=6 killed=6 survivors=0 total=6 arms=54` and exits 0, where each of the six `old`
  anchors below occurs exactly once in its named r86 counter at R, each pristine copy's own
  `--selftest` is green with exactly the frozen arm count for that file (18/13/23), and each
  mutated copy's own `--selftest` is killed by the frozen kill rule.

Population (all six survive the entering r86 selftests, measured at `6fc09d69` by the round-87
mutation probe `.ufo/waves/round-87/evidence/probe-r87.txt`):

  count-c1.py  M1-unanchored-conjunct  the `met` refusal of unanchored/empty mutations
  count-c1.py  M2-total-floor          the `total > 0` floor in `met`
  count-c1.py  M3-arms-tally           the tail `arms=` reading of the subject tally
  count-c2.py  M4-receipt-summary      the body summary-token requirement
  count-c2.py  M5-binding-digest       the counter-sha256 binding comparison
  count-c3.py  M6-keyshape             the non-keyshape branch of `derive()`

Kill rule (frozen): a mutant is killed iff the mutated copy's own `--selftest` exits non-zero
**or** prints `fail=<n>` with n > 0, conditional on the pristine copy being green with its frozen
arm count. An anchor that does not occur exactly once is `unanchored` and never counted killed; an
empty mutation is `empty-mutation`; a red pristine, a wrong arm count, an unanchored anchor, an
empty mutation or a red detector keeps the claim unmet. Exit 2 is setup, never a pass.

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

SUBJECTS = (
    ".ufo/waves/round-86/count-c1.py",
    ".ufo/waves/round-86/count-c2.py",
    ".ufo/waves/round-86/count-c3.py",
)

# file -> frozen arm count of that counter's own --selftest at the after revision.
ARMS_BY_FILE = {
    "count-c1.py": 18,
    "count-c2.py": 13,
    "count-c3.py": 23,
}

C1 = SUBJECTS[0]
C2 = SUBJECTS[1]
C3 = SUBJECTS[2]

MUTANTS = (
    (C1, "M1-unanchored-conjunct",
     'and not any(e.startswith(("empty-mutation", "unanchored")) for e in extras)',
     "and True"),
    (C1, "M2-total-floor",
     "met = (pristine_ok and total > 0", "met = (pristine_ok and total >= 0"),
    (C1, "M3-arms-tally",
     "arms = arms_of(out)[0]", "arms = TARGET_ARMS"),
    (C2, "M4-receipt-summary",
     "if token in body:", "if True:"),
    (C2, "M5-binding-digest",
     "if measured == sha:", "if True:"),
    (C3, "M6-keyshape",
     "if not KEYSHAPE.match(body):", "if False:"),
)

FAIL = re.compile(r"\bfail=([1-9][0-9]*)\b")
COUNT = re.compile(r"\b(mutants|killed|survivors|total|arms)=(\d+)\b")
ARMS = re.compile(r"COUNTER_SELFTEST pass=(\d+) fail=(\d+)")
TARGET = (6, 0, 6)
TARGET_ARMS = 54


def run(cmd, cwd=None, env=None, timeout=300):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          env=env, timeout=timeout)


def selftest_run(path, scratch):
    """Run one subject copy's own --selftest. Returns (rc, combined output)."""
    work = tempfile.mkdtemp(dir=scratch)
    env = dict(os.environ)
    env.update(TMPDIR=work, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
    try:
        p = run(["python3", "-I", path, "--selftest"], cwd=work, env=env)
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
    """The subject selftest's own pass/fail tally as (pass, fail), or (-1, -1)."""
    m = None
    for m in ARMS.finditer(out):
        pass
    if m is None:
        return -1, -1
    return int(m.group(1)), int(m.group(2))


def target_split(tail):
    fields = dict((key, int(value)) for key, value in COUNT.findall(tail))
    return (fields.get("killed"), fields.get("survivors"),
            fields.get("total"), fields.get("arms")) == TARGET + (TARGET_ARMS,)


def grade(loader, scratch, mutants=MUTANTS, arms_by_file=None):
    """Grade every anchored mutant at one revision. Returns (met, tail, lines, extras)."""
    arms_by_file = ARMS_BY_FILE if arms_by_file is None else arms_by_file
    lines, extras = [], []
    pristine_ok = True
    arms_total = 0
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
        name = os.path.basename(path)
        want_arms = arms_by_file.get(name)
        tree = os.path.join(scratch, "pristine-" + name)
        target = os.path.join(tree, path)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        open(target, "w", encoding="utf-8").write(base)
        rc, out = selftest_run(target, scratch)
        passed, failed = arms_of(out)
        if not green(rc, out):
            pristine_ok = False
            extras.append("pristine-red %s rc=%d arms=%d" % (path, rc, passed))
        elif want_arms is not None and passed != want_arms:
            pristine_ok = False
            extras.append("pristine-arms %s arms=%d want=%d" % (path, passed, want_arms))
        arms_total += max(passed, 0)
        for label, old, new in by_file[path]:
            if base.count(old) != 1:
                extras.append("unanchored %s %s occurrences=%d"
                              % (path, label, base.count(old)))
                continue
            mutated = base.replace(old, new)
            if mutated == base:
                extras.append("empty-mutation %s %s" % (path, label))
                continue
            d = os.path.join(scratch, "mut-" + name + "-" + label)
            target = os.path.join(d, path)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            open(target, "w", encoding="utf-8").write(mutated)
            k_rc, k_out = selftest_run(target, scratch)
            k = killed(k_rc, k_out)
            total += 1
            lines.append("MUTANT %s %s %s rc=%d"
                         % (name, label, "killed" if k else "survived", k_rc))
            if not k:
                extras.append("survivor %s %s" % (path, label))
            shutil.rmtree(d, ignore_errors=True)
    survivors = len([line for line in lines if " survived " in line])
    killed_n = total - survivors
    met = (pristine_ok and total > 0 and survivors == 0
           and not any(e.startswith(("empty-mutation", "unanchored")) for e in extras))
    tail = ("mutants=%d killed=%d survivors=%d total=%d arms=%d"
            % (total, killed_n, survivors, total, arms_total))
    return met, tail, lines, extras


def selfcheck(scratch):
    """Detector arms over synthetic subject copies (no lane file is touched)."""
    cases = []

    def write(d, name, body):
        os.makedirs(os.path.join(d, "tools"), exist_ok=True)
        path = os.path.join(d, "tools", name)
        open(path, "w", encoding="utf-8").write(body)
        return path

    def disk(p):
        return open(os.path.join(d, p), encoding="utf-8").read()

    sensitive = ("import sys\nGUARD = 1\n"
                 "ok = GUARD == 1\n"
                 "print('FAKE pass=%d fail=%d' % (1 if ok else 0, 0 if ok else 1))\n"
                 "print('COUNTER_SELFTEST pass=1 fail=0')\n"
                 "sys.exit(0 if ok else 1)\n")
    blind = "print('FAKE pass=1 fail=0')\nprint('COUNTER_SELFTEST pass=1 fail=0')\n"
    d = tempfile.mkdtemp(dir=scratch)
    write(d, "sensitive.py", sensitive)
    write(d, "blind.py", blind)

    m1 = [("tools/sensitive.py", "M1-unanchored-conjunct", "GUARD = 1", "GUARD = 0")]
    met, tail, _lines, _ = grade(disk, scratch, m1, {"sensitive.py": 1})
    fields = dict((k, int(v)) for k, v in COUNT.findall(tail))
    cases.append(("killed_counted",
                  met and fields.get("killed") == 1 and fields.get("total") == 1, tail))
    met, tail, _lines, _ = grade(
        disk, scratch, [("tools/blind.py", "M2-total-floor",
                         "print('FAKE pass=1 fail=0')",
                         "print('FAKE pass=1 fail=0') # noop")], {"blind.py": 1})
    fields = dict((k, int(v)) for k, v in COUNT.findall(tail))
    cases.append(("survivor_counted", (not met) and fields.get("survivors") == 1, tail))
    cases.append(("arms_parse",
                  arms_of("noise\nC1_COUNTER_SELFTEST pass=18 fail=0\n") == (18, 0), "18/0"))
    cases.append(("arms_tally_read",
                  grade(disk, scratch, m1, {"sensitive.py": 1})[1].endswith("arms=1"),
                  "arms from subject"))
    cases.append(("pristine_arms_floor",
                  not grade(disk, scratch, m1, {"sensitive.py": 18})[0], "18 wanted"))
    cases.append(("green_boundary",
                  green(0, "FAKE pass=1 fail=0") and not green(0, "SELFTEST skipped")
                  and not green(0, "FAKE pass=1 fail=2") and not green(1, "FAKE pass=1 fail=0"),
                  "green()"))
    cases.append(("killed_boundary",
                  killed(1, "traceback") and killed(0, "FAKE pass=1 fail=2")
                  and not killed(0, "FAKE pass=1 fail=0"), "killed()"))
    write(d, "dup.py", "GUARD = 1\nGUARD = 1\nprint('FAKE pass=1 fail=0')\n"
          "print('COUNTER_SELFTEST pass=1 fail=0')\n")
    met, tail, _lines, extras = grade(
        disk, scratch, [("tools/dup.py", "M1-unanchored-conjunct", "GUARD = 1", "GUARD = 0")],
        {"dup.py": 1})
    cases.append(("unanchored_excluded",
                  (not met) and "unanchored" in " ".join(extras), tail))
    write(d, "zero.py", "print('FAKE pass=1 fail=0')\nGUARD = 1\n")
    met, tail, _lines, extras = grade(
        disk, scratch, [("tools/zero.py", "M1-unanchored-conjunct", "GUARD = 1", "GUARD = 0")],
        {"zero.py": 1})
    cases.append(("unanchored_plus_killed_unmet",
                  (not met) and "unanchored" in " ".join(extras), tail))
    cases.append(("zero_mutants_unmet",
                  not grade(disk, scratch, [], {"sensitive.py": 1})[0], "no mutants"))
    write(d, "empty.py", "GUARD = 1\nprint('FAKE pass=1 fail=0')\n"
          "print('COUNTER_SELFTEST pass=1 fail=0')\n")
    met, tail, _lines, extras = grade(
        disk, scratch, [("tools/empty.py", "M1-unanchored-conjunct", "GUARD = 1", "GUARD = 1")],
        {"empty.py": 1})
    cases.append(("empty_mutation_unmet",
                  (not met) and "empty-mutation" in " ".join(extras), tail))
    write(d, "red.py", "print('FAKE pass=0 fail=1')\nraise SystemExit(1)\n")
    met, tail, _lines, extras = grade(
        disk, scratch, [("tools/red.py", "M2-total-floor", "fail=1", "fail=2")], {"red.py": 1})
    cases.append(("red_pristine_reported",
                  (not met) and "pristine-red" in " ".join(extras), tail))
    cases.append(("target_split_ok",
                  target_split("mutants=6 killed=6 survivors=0 total=6 arms=54"), "6/0/6/54"))
    cases.append(("target_split_free",
                  not target_split("mutants=6 killed=5 survivors=1 total=6 arms=54"), "5/1/6"))
    cases.append(("target_arms_free",
                  not target_split("mutants=6 killed=6 survivors=0 total=6 arms=48"), "48"))
    cases.append(("per_file_arms_frozen",
                  ARMS_BY_FILE == {"count-c1.py": 18, "count-c2.py": 13, "count-c3.py": 23}
                  and sum(ARMS_BY_FILE.values()) == TARGET_ARMS, "54"))
    cases.append(("labels_unique", len(set(m[1] for m in MUTANTS)) == 6, "six labels"))
    # --- round-88 arms: one per surviving r87-counter clause (Mo87M01Mut ranks 1, 3, 17, 18,
    # 19, 20). Each fails under its declared mutant; none fails on the pristine counter. ---
    write(d, "s18.py", "import sys\nGUARD = 1\n"
          "ok = GUARD == 1\n"
          "print('FAKE pass=%d fail=%d' % (18 if ok else 17, 0 if ok else 1))\n"
          "print('COUNTER_SELFTEST pass=18 fail=0')\n"
          "sys.exit(0 if ok else 1)\n")
    met, tail, _lines, extras = grade(
        disk, scratch,
        [("tools/sensitive.py", "r88-kill", "GUARD = 1", "GUARD = 0"),
         ("tools/dup.py", "r88-double", "GUARD = 1", "GUARD = 0")],
        {"sensitive.py": 1, "dup.py": 1})
    fields = dict((k, int(v)) for k, v in COUNT.findall(tail))
    cases.append(("met_guard_unanchored",
                  (not met) and fields.get("total") == 1 and fields.get("killed") == 1
                  and any(e.startswith("unanchored") for e in extras), tail))
    met, tail, _lines, extras = grade(
        disk, scratch,
        [("tools/sensitive.py", "r88-kill", "GUARD = 1", "GUARD = 0"),
         ("tools/empty.py", "r88-empty", "GUARD = 1", "GUARD = 1")],
        {"sensitive.py": 1, "empty.py": 1})
    fields = dict((k, int(v)) for k, v in COUNT.findall(tail))
    cases.append(("met_guard_empty",
                  (not met) and fields.get("total") == 1
                  and any(e.startswith("empty-mutation") for e in extras), tail))
    met, tail, _lines, _ = grade(
        disk, scratch,
        [("tools/sensitive.py", "r88-kill", "GUARD = 1", "GUARD = 0"),
         ("tools/blind.py", "r88-survive", "print('FAKE pass=1 fail=0')",
          "print('FAKE pass=1 fail=0') # noop")],
        {"sensitive.py": 1, "blind.py": 1})
    fields = dict((k, int(v)) for k, v in COUNT.findall(tail))
    cases.append(("killed_tally_mixed",
                  fields.get("killed") == 1 and fields.get("survivors") == 1
                  and fields.get("total") == 2, tail))
    met, tail, _lines, _ = grade(
        disk, scratch, [("tools/s18.py", "r88-arms", "GUARD = 1", "GUARD = 0")],
        {"s18.py": 18})
    cases.append(("arms_tally_passed", met and tail.endswith("arms=18"), tail))
    cases.append(("target_split_killed_not_mutants",
                  not target_split("mutants=6 killed=5 survivors=0 total=6 arms=54"),
                  "5 != 6"))
    met, tail, _lines, _ = grade(
        disk, scratch, [("tools/dup.py", "r88-double", "GUARD = 1", "GUARD = 0")],
        {"dup.py": 1})
    fields = dict((k, int(v)) for k, v in COUNT.findall(tail))
    cases.append(("doubled_anchor_counted_type",
                  fields.get("mutants") == 0 and fields.get("total") == 0 and met is False,
                  tail))
    cases.append(("marker_literal",
                  "M1-unanchored-conjunct" in open(os.path.abspath(__file__)).read(), "label"))
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
    scratch = tempfile.mkdtemp(prefix="count-c1-r87-", dir=base)
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
        met, tail, lines, extras = grade(loader, scratch)
        for line in lines:
            print(line)
        for extra in extras:
            print("EXTRA " + extra)
        if not own_ok:
            print("C1=unmet %s detector=red rev=%s" % (tail, rev[:12]))
            print(own_out.strip())
            return 1
        if not met or not target_split(tail):
            print("C1=unmet %s detector=green rev=%s" % (tail, rev[:12]))
            return 1
        print("C1=met %s rev=%s" % (tail, rev[:12]))
        return 0
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
