#!/usr/bin/env python3
"""mori round-83 C1 counter (operability): the r82 counter survivors get failing arms.

Frozen predicate P-C1 (`.ufo/waves/round-83/contract.md` — this counter, the contract and the
receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-83/count-c1.py R` prints
  `C1=met mutants=23 killed=23 survivors=0 total=23 pristine=green` and exits 0, where the
  23-mutant table below is re-derived from R's bytes (each `old` anchor occurs exactly once in
  the named file at R), every mutated copy's own `--selftest` reads killed, and the three
  pristine counters' `--selftest` runs are green first.

Detector (frozen): a mutant is killed iff the mutated copy's own `--selftest` exits non-zero
**or** prints `fail=<n>` with n > 0, conditional on the pristine copy being green. An anchor that
does not occur exactly once is reported `unanchored` and never counted as killed. A surviving
mutant, a red pristine, an unanchored anchor or an empty mutation keeps the claim unmet. Exit 2
is setup, never a pass.

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
    (".ufo/waves/round-82/count-c1.py", "green_ignores_fail_token",
     'return rc == 0 and "fail=0" in out and not FAIL.search(out)',
     'return rc == 0 and "fail=0" in out'),
    (".ufo/waves/round-82/count-c1.py", "killed_ignores_rc",
     "return rc != 0 or bool(FAIL.search(out))",
     "return bool(FAIL.search(out))"),
    (".ufo/waves/round-82/count-c1.py", "ignore_pristine_red",
     "met = pristine_ok and total > 0", "met = total > 0"),
    (".ufo/waves/round-82/count-c1.py", "accept_empty_population",
     "and total > 0 and survivors == 0", "and survivors == 0"),
    (".ufo/waves/round-82/count-c1.py", "unanchored_excused",
     'e.startswith("empty-mutation") or e.startswith("unanchored") for e in extras',
     'e.startswith("empty-mutation") for e in extras'),
    (".ufo/waves/round-82/count-c1.py", "detector_gate_dropped",
     "return 0 if (met and own_ok) else 1", "return 0 if met else 1"),
    (".ufo/waves/round-82/count-c1.py", "unanchored_still_graded",
     "if base.count(old) != 1:", "if base.count(old) < 1:"),
    (".ufo/waves/round-82/count-c2.py", "stale_accepted",
     "and not stale and agreed == len(tokens)", "and agreed == len(tokens)"),
    (".ufo/waves/round-82/count-c2.py", "duplicates_accepted",
     "and malformed == 0 and duplicates == 0 and not stale",
     "and malformed == 0 and not stale"),
    (".ufo/waves/round-82/count-c2.py", "retired_paths_unchecked",
     "return (BASELINE in line and CLASSES in line)", "return True"),
    (".ufo/waves/round-82/count-c2.py", "red_literal_unchecked",
     'and "round-10 drift pin still red" not in line', "and True"),
    (".ufo/waves/round-82/count-c2.py", "green_census_tokens_accepted",
     "p.returncode == 1 and bool(tokens)", "bool(tokens)"),
    (".ufo/waves/round-82/count-c2.py", "finding_branch_inverted",
     'return "value-changed" if body[len("FINDING:"):] in findings '
     'else "added-since-r10"',
     'return "value-changed" if body[len("FINDING:"):] not in findings '
     'else "added-since-r10"'),
    (".ufo/waves/round-82/count-c2.py", "malformed_not_residual",
     "residual={residual + malformed}", "residual={residual}"),
    (".ufo/waves/round-82/count-c2.py", "keyshape_guard_inverted",
     '        return "value-changed"          # frozen table: "anything else" '
     "is value-changed",
     '        return "added-since-r10"          # frozen table: "anything else" '
     "is value-changed"),
    (".ufo/waves/round-82/count-c2.py", "derive_key_eol_only",
     r'KEY = re.compile(r"(?:^|\s)([A-Za-z0-9_]+)=")',
     r'KEY = re.compile(r"(?:^|\s)([A-Za-z0-9_]+)=$")'),
    (".ufo/waves/round-82/count-c3.py", "population_gate_dropped",
     "if not population_ok(pins):", "if False:"),
    (".ufo/waves/round-82/count-c3.py", "defeated_accepted",
     'ok = p.returncode == 1 and fields.get("revisions", 0) >= expect[1] \\\n'
     '            and "REVISION_MISMATCH" in out',
     "ok = p.returncode == 1"),
    (".ufo/waves/round-82/count-c3.py", "carrier_drift_allowed",
     "if here != show(path):", "if False:"),
    (".ufo/waves/round-82/count-c3.py", "bindings_floor_dropped",
     "and bindings >= 3", "and bindings >= 1"),
    (".ufo/waves/round-82/count-c3.py", "selftest_red_accepted",
     "if rc != 0 or not m or int(m.group(2)) != 0 or arms < ARMS_FLOOR:",
     "if not m or int(m.group(2)) != 0 or arms < ARMS_FLOOR:"),
    (".ufo/waves/round-82/count-c3.py", "revisions_default_zero",
     'met = (caught and q.returncode == 0 and fields.get("revisions", -1) == 0',
     'met = (caught and q.returncode == 0 and fields.get("revisions", 0) == 0'),
    (".ufo/waves/round-82/count-c3.py", "summary_first_line",
     "        if m:", "        if m and not fields:"),
)

# Pre-data amendment A1: an adjudicated equivalent mutant, exempt from the survivor count only
# while the graded bytes carry its coupling marker exactly once (the coupling is the proof).
EQUIVALENT = {
    "duplicates_accepted": "residual += duplicates",
}

FAIL = re.compile(r"\bfail=([1-9][0-9]*)\b")
COUNT = re.compile(r"\b(mutants|killed|survivors|total)=(\d+)\b")
# A revision's `harness=present` means the file IS this counter: every frozen label and the
# detector-selftest marker must be in its bytes (r82 C01: an existence-only check passed a stub).
FROZEN_MARKERS = tuple(label for _, label, _, _ in MUTANTS) + ("C1_COUNTER_SELFTEST",)


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
                coupled = base.count(coupling) == 1
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
    d = tempfile.mkdtemp(dir=scratch)
    write(d, "sensitive.py", sensitive)
    write(d, "blind.py", blind)

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
    dup = "GUARD = 1\nGUARD = 1\nprint('FAKE pass=1 fail=0')\n"
    write(d, "dup.py", dup)
    met, tail, lines, extras = grade(
        disk, scratch,
        [("tools/dup.py", "twice", "GUARD = 1", "GUARD = 0"),
         ("tools/dup.py", "second", "GUARD = 1", "GUARD = 2")])
    cases.append(("duplicate_anchor_excluded",
                  (not met) and "unanchored" in " ".join(extras)
                  and "total=0" in tail, tail))
    red = "print('FAKE pass=0 fail=1')\nraise SystemExit(1)\n"
    write(d, "red.py", red)
    met, tail, lines, extras = grade(
        disk, scratch, [("tools/red.py", "self_red", "pass=0", "pass=0")])
    cases.append(("red_pristine_reported",
                  (not met) and "pristine=red" in tail, tail))
    eq = ("GUARD = 1\nCOUPLE = 2\n"
          "def f(duplicates, residual):\n    residual += duplicates\n"
          "    return residual\nprint('FAKE pass=1 fail=0')\n")
    write(d, "eq.py", eq)
    met, tail, lines, extras = grade(
        disk, scratch, [("tools/eq.py", "duplicates_accepted", "COUPLE = 2", "COUPLE = 3")])
    cases.append(("equivalent_excluded_when_coupled",
                  met and "equivalent=1" in tail and "survivors=0" in tail, tail))
    met, tail, lines, extras = grade(
        disk, scratch, [("tools/blind.py", "noop", "print('FAKE pass=1 fail=0')",
                         "print('FAKE pass=1 fail=0') # noop")])
    cases.append(("non_equivalent_still_survives", (not met) and "survivors=1" in tail, tail))
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
    scratch = tempfile.mkdtemp(prefix="count-c1-r83-", dir=base)
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

        harness = loader(".ufo/waves/round-83/count-c1.py")
        if harness is None:
            print("C1=unmet harness=absent rev=%s" % rev[:12])
            return 1
        missing = [m for m in FROZEN_MARKERS if m not in harness]
        if missing:
            print("C1=unmet harness=present markers=missing:%s rev=%s"
                  % (",".join(missing[:3]), rev[:12]))
            return 1
        own = subprocess.run([sys.executable, "-I", os.path.abspath(__file__),
                              "--selftest", "--scratch", scratch],
                             capture_output=True, text=True, timeout=300)
        own_out = (own.stdout or "") + (own.stderr or "")
        own_ok = (own.returncode == 0 and "C1_COUNTER_SELFTEST" in own_out
                  and "fail=0" in own_out)
        met, tail, lines, extras = grade(loader, scratch)
        if tail.startswith("setup=absent:"):
            print("C1=unmet harness=absent rev=%s" % rev[:12])
            return 1
        if tail.startswith("setup="):
            print("C1_SETUP " + tail, file=sys.stderr)
            return 2
        for line in lines:
            print(line)
        for extra in extras:
            print(extra)
        if not own_ok:
            last = own_out.strip().splitlines()[-1] if own_out.strip() else "(no output)"
            print("detector-selftest=red " + last)
        print("C1=%s %s detector=%s rev=%s"
              % ("met" if (met and own_ok) else "unmet", tail,
                 "green" if own_ok else "red", rev[:12]))
        return 0 if (met and own_ok) else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
