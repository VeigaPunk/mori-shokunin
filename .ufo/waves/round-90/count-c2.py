#!/usr/bin/env python3
"""mori round-90 C2 counter (calibration): every declared arm is isolated, and the three
neighbouring survivors are armed.

Frozen predicate P-C2 (`.ufo/waves/round-90/contract.md` — this file, the contract and the
receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-90/count-c2.py R` prints
  `C2=met mutants=15 killed=15 survivors=0 unattributed=0 unanchored=0 isolated=0
  literal_anchors=0 arms=29,27 rev=<12>` and exits 0, where for every declared mutant the subject at R is green at exactly
  its frozen arm count, the anchor occurs exactly once and lies outside every string literal, and
  the mutated copy's own `--selftest` is killed **with attribution and isolation**: the run exits
  non-zero or prints `fail=<n>` (n>0) **and** its complete set of `FAIL <arm>` labels is exactly
  `{<declared arm>}`.

Kill rule (frozen): `killed ⟺ (rc≠0 ∨ fail>0) ∧ failset(out) == {declared arm}`.
  * a red run whose `FAIL` label set is a strict superset of the declared arm is `isolated`
    (round-89 defect: a canary that reds every arm on any edit reached the old target);
  * a red run with no `FAIL` line, or with a different single label, is `unattributed`;
  * an absent anchor is `unanchored`; an empty mutation is `empty-mutation`; a red pristine or a
    wrong pristine arm count is `pristine`; an anchor lying wholly inside a string literal is
    `literal-anchor`. Any of them keeps the claim unmet. Exit 2 is setup, never a pass.

Population (frozen before any after-value): the twelve round-89 mutants (ranks 1-12 of
`.ufo/waves/round-88/w1/Mo88M01Mut.md`) plus the three round-89 neighbouring survivors
`Mo89M02Mut` B1/B4/B6 — `own_ok_of`'s arm-count pin, `met_line` at its call site, and
`clone_root_ok`'s negative. Anchors are the **after-revision** bytes: the three new arms and the
round-89 landings do not exist at the entering revision, so the entering run reports them
`unanchored` or `survivor`, never killed.

Usage: count-c2.py <rev> [--repo DIR] [--scratch DIR] | count-c2.py --selftest
Output: per mutant `MUTANT <file> <label> killed|survived|unattributed|isolated rc=N arm=<arm>`,
then the summary line. Exit 0 met, 1 unmet, 2 setup. Read-only: `git show`; files only under
--scratch.
"""
import argparse
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tokenize

C1 = ".ufo/waves/round-88/count-c1.py"
C2 = ".ufo/waves/round-88/count-c2.py"

ARMS_BY_FILE = {"count-c1.py": 29, "count-c2.py": 27}

MUTANTS = (
    (C1, "C1-arms-first", "arms_last_tally",
     "for m in ARMS.finditer(out):\n        pass",
     "for m in ARMS.finditer(out):\n        break"),
    (C1, "C1-green-drop-fail", "green_mixed_fail",
     'return rc == 0 and "fail=0" in out and not FAIL.search(out)',
     'return rc == 0 and "fail=0" in out'),
    (C1, "C1-own-ok", "own_ok_red",
     '    return (rc == 0 and "C1_COUNTER_SELFTEST" in out',
     '    return (True or rc == 0 and "C1_COUNTER_SELFTEST" in out'),
    (C2, "C2-target", "target_full",
     'TARGET = "real=met fx=4 clean=1 refused=2 absent=1 arms=26"',
     'TARGET = "real=unmet fx=4 clean=1 refused=2 absent=1 arms=26"'),
    (C2, "C2-printed-target", "met_line_derived",
     'return "C2=met %s rev=%s" % (TARGET, rev[:12])',
     'return "C2=met %s rev=%s" % ("real=unmet fx=4 clean=1 refused=2 absent=1 arms=26",'
     ' rev[:12])'),
    (C2, "C2-fixture-clean", "clean_wrong_split",
     'return verdict.startswith("C2=met " + REAL), verdict or "no verdict line"',
     'return verdict.startswith("C2=met "), verdict or "no verdict line"'),
    (C2, "C2-receipt-name", "receipt_name_bound",
     "if m and m.group(1) == name:",
     "if m:"),
    (C2, "C2-clone-top", "clone_top_bound",
     "return top_out.strip() == os.path.realpath(d)",
     "return True"),
    (C2, "C2-own-ok", "own_ok_red",
     '    return (rc == 0 and "C2_COUNTER_SELFTEST" in out',
     '    return (True or rc == 0 and "C2_COUNTER_SELFTEST" in out'),
    (C2, "C2-verdict-first", "verdict_last_wins",
     "last = line\n    return last",
     "last = line\n            break\n    return last"),
    (C2, "C2-no-supersedes", "absent_without_supersedes",
     """raise ValueError("fixture receipt has no '# supersedes:' line")""",
     "pass"),
    (C2, "C2-vacuous-body", "vacuous_body_fabricated",
     '        body = ["RECORD_SWEEP fabricated=1"]\n    elif kind == "absent-target":',
     '        body = body\n    elif kind == "absent-target":'),
    # The three neighbouring survivors `Mo89M02Mut` measured (B1/B4/B6).
    (C1, "B1-own-ok-arm-count", "own_ok_arm_count",
     'r"C1_COUNTER_SELFTEST pass=%d fail=0" % EXPECTED_ARMS, out)',
     'r"C1_COUNTER_SELFTEST pass=[0-9]+ fail=0", out)'),
    (C2, "B4-met-line-call-site", "met_line_call_site",
     "print(met_line(rev))",
     "print(met_line(rev[:7]))"),
    (C2, "B6-clone-root-prefix", "clone_root_negative",
     "return top_out.strip() == os.path.realpath(d)",
     "return (top_out.strip() == os.path.realpath(d)\n"
     "            or os.path.realpath(d).startswith(top_out.strip()))"),
)

TARGET = ("mutants=15 killed=15 survivors=0 unattributed=0 unanchored=0 isolated=0 "
          "literal_anchors=0 arms=29,27")
FAIL = re.compile(r"\bfail=([1-9][0-9]*)\b")
FAILLINE = re.compile(r"^FAIL (\S+)", re.M)
COUNT = re.compile(r"\b(mutants|killed|survivors|unattributed|unanchored|isolated|"
                   r"literal_anchors|arms)=(\d+(?:,\d+)?)\b")
ARMS = re.compile(r"COUNTER_SELFTEST pass=(\d+) fail=(\d+)")
EXPECTED_ARMS = 21


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


def red(rc, out):
    return rc != 0 or bool(FAIL.search(out))


def arm_failed(out, arm):
    """True when the selftest printed a FAIL line for exactly this arm label."""
    return re.search(r"^FAIL %s(\s|$)" % re.escape(arm), out or "", re.M) is not None


def failset(out):
    """Every `FAIL <arm>` label the run printed, as a set."""
    return frozenset(FAILLINE.findall(out or ""))


def killed(rc, out, arm):
    """Frozen kill rule: red and the FAIL label set is exactly the declared arm."""
    return red(rc, out) and failset(out) == frozenset((arm,))


def isolated(rc, out, arm):
    """Red, the declared arm failed, and at least one other arm failed too."""
    labels = failset(out)
    return red(rc, out) and arm in labels and len(labels) > 1


def unattributed(rc, out, arm):
    """Red with no FAIL line or a single different label: no kill can be credited."""
    labels = failset(out)
    return red(rc, out) and (not labels or (len(labels) == 1 and arm not in labels))


def _offset(text, row, col):
    """Character offset of a tokenize (row, col) position."""
    return sum(len(line) for line in text.splitlines(True)[:row - 1]) + col


def literal_anchor(base, old):
    """True when the anchor's only occurrence lies wholly inside a STRING literal."""
    start = base.find(old)
    if start < 0:
        return False
    end = start + len(old)
    try:
        for tok in tokenize.generate_tokens(io.StringIO(base).readline):
            if tok.type != tokenize.STRING:
                continue
            first = _offset(base, tok.start[0], tok.start[1])
            last = _offset(base, tok.end[0], tok.end[1])
            if first <= start and end <= last:
                return True
    except (tokenize.TokenError, IndentationError):
        return False
    return False


def arms_of(out):
    """The subject selftest's own pass/fail tally as (pass, fail), or (-1, -1)."""
    m = None
    for m in ARMS.finditer(out):
        pass
    if m is None:
        return -1, -1
    return int(m.group(1)), int(m.group(2))


def target_split(tail):
    fields = dict((key, value) for key, value in COUNT.findall(tail))
    return (fields.get("mutants"), fields.get("killed"), fields.get("survivors"),
            fields.get("unattributed"), fields.get("unanchored"),
            fields.get("isolated"), fields.get("literal_anchors"),
            fields.get("arms")) == ("15", "15", "0", "0", "0", "0", "0", "29,27")


def grade(loader, scratch, mutants=MUTANTS, arms_by_file=None):
    """Grade every anchored mutant at one revision. Returns (met, tail, lines, extras)."""
    arms_by_file = ARMS_BY_FILE if arms_by_file is None else arms_by_file
    lines, extras = [], []
    pristine_ok = True
    by_file = {}
    for path, label, arm, old, new in mutants:
        by_file.setdefault(path, []).append((label, arm, old, new))
    total = 0
    arm_list = []
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
        arm_list.append(passed)
        if not green(rc, out):
            pristine_ok = False
            extras.append("pristine-red %s rc=%d arms=%d" % (path, rc, passed))
        elif want_arms is not None and passed != want_arms:
            pristine_ok = False
            extras.append("pristine-arms %s arms=%d want=%d" % (path, passed, want_arms))
        for label, arm, old, new in by_file[path]:
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
            if literal_anchor(base, old):
                state = "literal-anchor"
                extras.append("literal-anchor %s %s" % (path, label))
            elif killed(k_rc, k_out, arm):
                state = "killed"
            elif isolated(k_rc, k_out, arm):
                state = "isolated"
                extras.append("isolated %s %s arm=%s fails=%s"
                              % (path, label, arm, ",".join(sorted(failset(k_out)))))
            elif unattributed(k_rc, k_out, arm):
                state = "unattributed"
                extras.append("unattributed %s %s arm=%s" % (path, label, arm))
            else:
                state = "survived"
                extras.append("survivor %s %s" % (path, label))
            total += 1
            lines.append("MUTANT %s %s %s rc=%d arm=%s" % (name, label, state, k_rc, arm))
            shutil.rmtree(d, ignore_errors=True)
    killed_n = len([line for line in lines if " killed " in line])
    survivors = len([line for line in lines if " survived " in line])
    unattributed_n = len([line for line in lines if " unattributed " in line])
    isolated_n = len([line for line in lines if " isolated " in line])
    literal_n = len([line for line in lines if " literal-anchor " in line])
    unanchored_n = len([e for e in extras if e.startswith("unanchored")])
    met = (pristine_ok and total > 0 and survivors == 0 and unattributed_n == 0
           and isolated_n == 0 and literal_n == 0
           and not any(e.startswith(("empty-mutation", "unanchored")) for e in extras))
    tail = ("mutants=%d killed=%d survivors=%d unattributed=%d unanchored=%d isolated=%d "
            "literal_anchors=%d arms=%s"
            % (total, killed_n, survivors, unattributed_n, unanchored_n, isolated_n,
               literal_n, ",".join(str(a) for a in arm_list)))
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
                 "print('FAIL own_ok_red guard' if not ok else 'PASS own_ok_red guard')\n"
                 "print('COUNTER_SELFTEST pass=%d fail=%d' % (1 if ok else 0, 0 if ok else 1))\n"
                 "sys.exit(0 if ok else 1)\n")
    canary = ("import sys\n"
              "print('COUNTER_SELFTEST pass=1 fail=0')\n"
              "sys.exit(1)\n")
    blind = "print('COUNTER_SELFTEST pass=1 fail=0')\n"
    d = tempfile.mkdtemp(dir=scratch)
    write(d, "sensitive.py", sensitive)
    write(d, "canary.py", canary)
    write(d, "blind.py", blind)
    write(d, "dup.py", "GUARD = 1\nGUARD = 1\nprint('COUNTER_SELFTEST pass=1 fail=0')\n")
    write(d, "empty.py", "GUARD = 1\nprint('COUNTER_SELFTEST pass=1 fail=0')\n")

    one = [("tools/sensitive.py", "C1-own-ok", "own_ok_red", "GUARD = 1", "GUARD = 0")]
    met, tail, lines, _ = grade(disk, scratch, one, {"sensitive.py": 1})
    fields = dict(COUNT.findall(tail))
    cases.append(("kill_attributed",
                  met and fields.get("killed") == "1" and " killed " in lines[0], tail))
    met, tail, lines, extras = grade(
        disk, scratch, [("tools/canary.py", "C2-own-ok", "own_ok_red",
                         "sys.exit(1)", "sys.exit(2)")], {"canary.py": 1})
    fields = dict(COUNT.findall(tail))
    cases.append(("canary_unattributed",
                  (not met) and fields.get("unattributed") == "1"
                  and fields.get("killed") == "0", tail))
    met, tail, lines, _ = grade(
        disk, scratch, [("tools/blind.py", "C1-arms-first", "arms_last_tally",
                         "print('COUNTER_SELFTEST pass=1 fail=0')",
                         "print('COUNTER_SELFTEST pass=1 fail=0') # noop")], {"blind.py": 1})
    fields = dict(COUNT.findall(tail))
    cases.append(("survivor_counted", (not met) and fields.get("survivors") == "1", tail))
    cases.append(("arms_parse",
                  arms_of("noise\nC1_COUNTER_SELFTEST pass=28 fail=0\n") == (28, 0), "28/0"))
    cases.append(("green_boundary",
                  green(0, "COUNTER_SELFTEST pass=1 fail=0") and not green(0, "skipped")
                  and not green(0, "pass=1 fail=0\nFAIL x fail=2") and not green(1, "fail=0"),
                  "green()"))
    cases.append(("red_boundary",
                  red(1, "traceback") and red(0, "fail=2") and not red(0, "fail=0"), "red()"))
    cases.append(("arm_boundary",
                  arm_failed("FAIL own_ok_red x\n", "own_ok_red")
                  and not arm_failed("FAIL own_ok_red2 x\n", "own_ok_red")
                  and not arm_failed("PASS own_ok_red x\n", "own_ok_red"), "arm()"))
    met, tail, lines, extras = grade(
        disk, scratch, [("tools/dup.py", "C1-arms-first", "arms_last_tally",
                         "GUARD = 1", "GUARD = 0")], {"dup.py": 1})
    fields = dict(COUNT.findall(tail))
    cases.append(("unanchored_excluded",
                  (not met) and fields.get("unanchored") == "1"
                  and fields.get("mutants") == "0", tail))
    met, tail, lines, extras = grade(
        disk, scratch, [("tools/empty.py", "C1-arms-first", "arms_last_tally",
                         "GUARD = 1", "GUARD = 1")], {"empty.py": 1})
    cases.append(("empty_mutation_unmet",
                  (not met) and any(e.startswith("empty-mutation") for e in extras), tail))
    met, tail, lines, extras = grade(disk, scratch, one, {"sensitive.py": 24})
    cases.append(("pristine_arms_pin",
                  (not met) and any(e.startswith("pristine-arms") for e in extras), tail))
    write(d, "multi.py", "import sys\nGUARD = 1\n"
          "print('FAIL own_ok_red a' if GUARD != 1 else 'PASS own_ok_red a')\n"
          "print('FAIL other_arm b' if GUARD != 1 else 'PASS other_arm b')\n"
          "print('COUNTER_SELFTEST pass=%d fail=%d' % ((1, 0) if GUARD == 1 else (0, 2)))\n"
          "sys.exit(0 if GUARD == 1 else 1)\n")
    met, tail, lines, extras = grade(
        disk, scratch, [("tools/multi.py", "C1-own-ok", "own_ok_red",
                         "GUARD = 1", "GUARD = 0")], {"multi.py": 1})
    fields = dict(COUNT.findall(tail))
    cases.append(("isolation_multi_fail",
                  (not met) and fields.get("isolated") == "1" and fields.get("killed") == "0",
                  tail))
    write(d, "lit.py", "Y = 1\nprint('X = 1 ok')\nprint('COUNTER_SELFTEST pass=1 fail=0')\n")
    met, tail, lines, extras = grade(
        disk, scratch, [("tools/lit.py", "C1-arms-first", "arms_last_tally",
                         "X = 1", "X = 2")], {"lit.py": 1})
    fields = dict(COUNT.findall(tail))
    cases.append(("literal_anchor_wholly",
                  (not met) and fields.get("literal_anchors") == "1", tail))
    write(d, "red.py", "import sys\nCODE = 1\nprint('COUNTER_SELFTEST pass=0 fail=1')\n"
          "sys.exit(1)\n")
    met, tail, lines, extras = grade(
        disk, scratch, [("tools/red.py", "C1-arms-first", "arms_last_tally",
                         "CODE = 1", "CODE = 2")], {"red.py": 1})
    cases.append(("red_pristine_reported",
                  (not met) and any(e.startswith("pristine-red") for e in extras), tail))
    cases.append(("zero_mutants_unmet", not grade(disk, scratch, [], {})[0], "no mutants"))
    cases.append(("target_fields",
                  all(field in TARGET for field in
                      ("mutants=15", "killed=15", "survivors=0", "unattributed=0",
                       "unanchored=0", "isolated=0", "literal_anchors=0", "arms=29,27")),
                  "target"))
    cases.append(("labels_unique", len(set(m[1] for m in MUTANTS)) == 15, "fifteen labels"))
    cases.append(("arms_pinned",
                  ARMS_BY_FILE == {"count-c1.py": 29, "count-c2.py": 27}, "29/27"))
    cases.append(("failset_exact",
                  failset("FAIL a x\nFAIL b y\n") == frozenset(("a", "b"))
                  and killed(1, "FAIL a x\n", "a")
                  and not killed(1, "FAIL a x\nFAIL b y\n", "a")
                  and isolated(1, "FAIL a x\nFAIL b y\n", "a")
                  and not isolated(1, "FAIL a x\n", "a"), "failset()"))
    cases.append(("literal_anchor_code",
                  not literal_anchor("GUARD = 1\nprint('GUARD = 1')\n", "GUARD = 1"),
                  "code anchor"))
    cases.append(("marker_literal", "unattributed" in open(os.path.abspath(__file__)).read(),
                  "label"))
    cases.append(("own_arms_pinned", len(cases) + 1 == EXPECTED_ARMS,
                  "%d/%d" % (len(cases) + 1, EXPECTED_ARMS)))
    ok = sum(1 for _, good_case, _ in cases if good_case)
    for label, good_case, line in cases:
        print("%s %s %s" % ("PASS" if good_case else "FAIL", label, line))
    print("C2_COUNTER_SELFTEST pass=%d fail=%d" % (ok, len(cases) - ok))
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
    scratch = tempfile.mkdtemp(prefix="count-c2-r89-", dir=base)
    try:
        if a.selftest:
            return selfcheck(scratch)
        if not a.rev:
            print("C2_SETUP usage: count-c2.py <rev> | --selftest", file=sys.stderr)
            return 2
        top = run(["git", "-C", a.repo, "rev-parse", "--show-toplevel"])
        repo = top.stdout.strip() if top.returncode == 0 else a.repo
        p = run(["git", "-C", repo, "rev-parse", "--verify", a.rev + "^{commit}"])
        if p.returncode != 0:
            print("C2_SETUP unresolvable revision " + a.rev, file=sys.stderr)
            return 2
        rev = p.stdout.strip()

        def loader(path):
            q = run(["git", "-C", repo, "show", "%s:%s" % (rev, path)])
            return q.stdout if q.returncode == 0 else None

        own = run(["python3", "-I", os.path.abspath(__file__), "--selftest",
                   "--scratch", scratch])
        own_out = (own.stdout or "") + (own.stderr or "")
        own_ok = (own.returncode == 0
                  and re.search(r"C2_COUNTER_SELFTEST pass=%d fail=0" % EXPECTED_ARMS,
                                own_out) is not None)
        met, tail, lines, extras = grade(loader, scratch)
        for line in lines:
            print(line)
        for extra in extras:
            print("EXTRA " + extra)
        if not own_ok:
            print("C2=unmet %s detector=red rev=%s" % (tail, rev[:12]))
            print(own_out.strip())
            return 1
        if not met or not target_split(tail):
            print("C2=unmet %s detector=green rev=%s" % (tail, rev[:12]))
            return 1
        print("C2=met %s rev=%s" % (TARGET, rev[:12]))
        return 0
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
