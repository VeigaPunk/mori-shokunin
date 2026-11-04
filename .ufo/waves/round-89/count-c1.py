#!/usr/bin/env python3
"""mori round-89 C1 counter (operability): the r87 receipt gate binds the executed script.

Frozen predicate P-C1 (`.ufo/waves/round-89/contract.md` — this file, the contract and the
receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-89/count-c1.py R` prints
  `C1=met equiv=accepted comment=refused selfprint=refused real=met arms=26` and exits 0, where
  the gate `.ufo/waves/round-87/count-c2.py` at R is green at exactly 26 selftest arms, still
  prints the r87 target line on the real seven-receipt population, accepts an equivalent
  `./tools/...` replay (`equiv`, the equivalence-positive control), and refuses a bound path
  named only after a shell comment (`comment`) or printed as data by a self-printing command
  (`selfprint`) — both with `cmd-binding` in the receipt's `problems=`.

Fixtures are commits inside `--shared` clones under `--scratch`; the lane is never written.

Usage: count-c1.py <rev> [--repo DIR] [--scratch DIR] | count-c1.py --selftest
Output: `REAL rc=… C2=…`, `FX <kind> <accepted|refused> problems=…`, then the summary line.
Exit 0 met, 1 unmet, 2 setup. Read-only over the lane: `git clone --shared`, `git show`.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

SUBJECT = ".ufo/waves/round-87/count-c2.py"
SUBJECT_ARMS = 26

REAL = ("receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 "
        "matched=6 defeated=1 superseded=2 legacy=1 unexpected=0")
TARGET = "equiv=accepted comment=refused selfprint=refused real=met arms=26"

BASE_RECEIPT = ".ufo/waves/round-87/evidence/record-sweep-r87.txt"
BODY = "RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=3 revisions=0"
PIN = ".ufo/waves/round-82/record-pins.json"
BOUND = "tools/mori-record-sweep.py"

# kind -> replacement `# cmd:` line (None keeps the receipt's own command)
FIXTURES = (
    ("equiv", "python3 -I ./%s --root . --pins %s" % (BOUND, PIN), "accepted"),
    ("comment", "printf '%%s\\n' '%s' # %s" % (BODY, BOUND), "refused"),
    ("selfprint", "python3 -c \"print('%s')\" %s" % (BODY, BOUND), "refused"),
)

CMD_LINE = re.compile(r"^#\s*cmd:\s*(\S.*)$")
SEP = re.compile(r"^#\s*---\s*$")
ARMS = re.compile(r"C2_COUNTER_SELFTEST pass=(\d+) fail=(\d+)")
RECEIPT = re.compile(r"^RECEIPT (\S+) expect=\S+ (met|failed) problems=(\S+)$")


def run(cmd, cwd=None, env=None, timeout=900):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          env=env, timeout=timeout)


def fixture_receipt(text, kind):
    """The base receipt's bytes under one frozen fixture. Pure; no file is written."""
    lines = (text or "").splitlines()
    if not any(SEP.match(line) for line in lines):
        raise ValueError("fixture receipt has no '# ---' separator")
    want = dict((k, cmd) for k, cmd, _e in FIXTURES).get(kind)
    if want is None:
        raise ValueError("unknown fixture kind " + kind)
    out, seen = [], False
    for line in lines:
        m = CMD_LINE.match(line)
        if m and not seen:
            seen = True
            out.append("# cmd: " + want)
            continue
        out.append(line)
    if not seen:
        raise ValueError("fixture receipt has no '# cmd:' line")
    return "\n".join(out) + "\n"


def receipt_line(stdout, name):
    for line in (stdout or "").splitlines():
        m = RECEIPT.match(line)
        if m and m.group(1) == name:
            return m
    return None


def verdict_line(stdout):
    last = ""
    for line in (stdout or "").splitlines():
        if line.startswith("C2="):
            last = line
    return last


def fixture_verdict(stdout, kind, receipt_name):
    """(ok, detail) for one fixture's graded stdout against the frozen expectation."""
    want = dict((k, e) for k, _c, e in FIXTURES)[kind]
    line = receipt_line(stdout, receipt_name)
    if line is None:
        return False, "no RECEIPT line for " + receipt_name
    met, problems = line.group(2), line.group(3)
    if want == "accepted":
        return (met == "met" and problems == "-"), "problems=" + problems
    return ("cmd-binding" in problems.split(",")), "problems=" + problems


def clone_fixture(repo, rev, scratch, kind, path):
    """A `--shared` clone at rev with one fixture committed on top; returns (dir, new rev)."""
    d = os.path.join(scratch, "fx-" + kind)
    env = dict(os.environ)
    env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull,
               TMPDIR=scratch, PYTHONDONTWRITEBYTECODE="1")
    cl = run(["git", "clone", "--shared", "-q", repo, d], env=env)
    if cl.returncode != 0:
        return None, "clone rc=%d" % cl.returncode
    co = run(["git", "-C", d, "checkout", "-q", rev], env=env)
    if co.returncode != 0:
        return None, "checkout rc=%d" % co.returncode
    top = run(["git", "-C", d, "rev-parse", "--show-toplevel"], env=env)
    if top.stdout.strip() != os.path.realpath(d):
        return None, "fixture root mismatch"
    target = os.path.join(d, path)
    if not os.path.exists(target):
        return None, "fixture path absent"
    text = open(target, encoding="utf-8").read()
    open(target, "w", encoding="utf-8").write(fixture_receipt(text, kind))
    add = run(["git", "-C", d, "add", "--", path], env=env)
    if add.returncode != 0:
        return None, "fixture add rc=%d" % add.returncode
    commit = run(["git", "-C", d, "-c", "user.name=t", "-c", "user.email=t@t",
                  "commit", "-q", "-m", "round89 fixture " + kind], env=env)
    if commit.returncode != 0:
        return None, "fixture commit rc=%d" % commit.returncode
    head = run(["git", "-C", d, "rev-parse", "HEAD"], env=env)
    return d, head.stdout.strip()


def run_graded(graded, repo, rev, scratch, name):
    """Run the gate copy against `repo` at `rev`; returns (rc, combined stdout)."""
    work = os.path.join(scratch, "graded-" + name)
    os.makedirs(work, exist_ok=True)
    env = dict(os.environ)
    env.update(TMPDIR=work, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull,
               PYTHONDONTWRITEBYTECODE="1")
    try:
        p = run(["python3", "-I", graded, rev, "--repo", repo, "--scratch", work], env=env)
    except subprocess.TimeoutExpired:
        return 124, "timeout"
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def selfcheck(scratch):
    """Detector arms over synthetic receipt text (no lane file is touched)."""
    cases = []
    good = ("# receipt: r.txt\n"
            "# cmd: python3 -I tools/x.py\n"
            "# rev: %s\n"
            "# counter-sha256: %s tools/x.py\n"
            "# replay: clone\n"
            "# supersedes: old.txt\n"
            "# limits: limit named words\n"
            "# ---\nTOKEN\n" % ("a" * 40, "b" * 64))
    equiv = fixture_receipt(good, "equiv")
    cases.append(("equiv_dot_slash",
                  ("# cmd: python3 -I ./%s --root . --pins %s" % (BOUND, PIN)) in equiv,
                  "./"))
    comment = fixture_receipt(good, "comment")
    cases.append(("comment_names_path",
                  "# %s" % BOUND in comment and comment.count("# cmd:") == 1, "comment"))
    selfprint = fixture_receipt(good, "selfprint")
    cases.append(("selfprint_names_data",
                  selfprint.count(BOUND) == 1 and 'python3 -c "print(' in selfprint
                  and "tools/x.py" in selfprint, "data"))
    for kind, _c, _e in FIXTURES:
        body = fixture_receipt(good, kind).rstrip("\n").splitlines()[-1]
        cases.append(("body_kept_" + kind, body == "TOKEN", body))
    try:
        fixture_receipt(good, "nope")
    except ValueError:
        bad = True
    else:
        bad = False
    cases.append(("unknown_kind_refused", bad, "ValueError"))
    try:
        fixture_receipt("# ---\nbody\n", "equiv")
    except ValueError:
        bad2 = True
    else:
        bad2 = False
    cases.append(("no_cmd_refused", bad2, "ValueError"))
    out_met = "RECEIPT r.txt expect=met met problems=-\nC2=met %s rev=abc\n" % REAL
    cases.append(("receipt_met_parsed",
                  fixture_verdict(out_met, "equiv", "r.txt")[0]
                  and verdict_line(out_met).startswith("C2=met "), "met"))
    out_cmd = "RECEIPT r.txt expect=met failed problems=cmd-binding\nC2=unmet receipts=7\n"
    cases.append(("receipt_problem_parsed",
                  fixture_verdict(out_cmd, "comment", "r.txt")[0]
                  and not fixture_verdict(out_cmd, "equiv", "r.txt")[0], "cmd-binding"))
    cases.append(("verdict_last", verdict_line("C2=met a\nC2=unmet b\n") == "C2=unmet b", "last"))
    cases.append(("target_fields",
                  all(field in TARGET for field in
                      ("equiv=accepted", "comment=refused", "selfprint=refused",
                       "real=met", "arms=26")), "target"))
    cases.append(("arms_pinned", SUBJECT_ARMS == 26, "26"))
    cases.append(("marker_literal", "cmd-binding" in open(os.path.abspath(__file__)).read(),
                  "label"))
    cases.append(("own_arms_pinned", len(cases) + 1 == EXPECTED_ARMS,
                  "%d/%d" % (len(cases) + 1, EXPECTED_ARMS)))
    ok = sum(1 for _, good_case, _ in cases if good_case)
    for label, good_case, line in cases:
        print("%s %s %s" % ("PASS" if good_case else "FAIL", label, line))
    print("C1_COUNTER_SELFTEST pass=%d fail=%d" % (ok, len(cases) - ok))
    return 0 if ok == len(cases) else 1


EXPECTED_ARMS = 15


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
    scratch = tempfile.mkdtemp(prefix="count-c1-r89-", dir=base)
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

        own = run(["python3", "-I", os.path.abspath(__file__), "--selftest",
                   "--scratch", scratch])
        own_out = (own.stdout or "") + (own.stderr or "")
        own_ok = (own.returncode == 0
                  and re.search(r"C1_COUNTER_SELFTEST pass=%d fail=0" % EXPECTED_ARMS,
                                own_out) is not None)

        q = run(["git", "-C", repo, "show", "%s:%s" % (rev, SUBJECT)])
        if q.returncode != 0:
            print("C1=unmet subject=absent real=absent equiv=absent comment=absent "
                  "selfprint=absent arms=? rev=%s" % rev[:12])
            return 1
        sdir = os.path.join(scratch, "subject")
        spath = os.path.join(sdir, SUBJECT)
        os.makedirs(os.path.dirname(spath), exist_ok=True)
        open(spath, "w", encoding="utf-8").write(q.stdout)
        srun = run(["python3", "-I", spath, "--selftest", "--scratch",
                    os.path.join(scratch, "subject-run")])
        sout = (srun.stdout or "") + (srun.stderr or "")
        arms = None
        for m in ARMS.finditer(sout):
            arms = (int(m.group(1)), int(m.group(2)))
        subject_ok = srun.returncode == 0 and arms == (SUBJECT_ARMS, 0)

        graded = os.path.join(scratch, "graded-count-c2.py")
        open(graded, "w", encoding="utf-8").write(q.stdout)

        real_rc, real_out = run_graded(graded, repo, rev, scratch, "real")
        real_line = verdict_line(real_out)
        real_ok = real_rc == 0 and real_line.startswith("C2=met " + REAL)
        print("REAL rc=%d %s" % (real_rc, real_line or "no-verdict"))

        state = {}
        fixture_ok = True
        name = os.path.basename(BASE_RECEIPT)
        for kind, _cmd, want in FIXTURES:
            d, fx = clone_fixture(repo, rev, scratch, kind, BASE_RECEIPT)
            if d is None:
                print("FX %s build-failed %s" % (kind, fx))
                state[kind] = "absent"
                fixture_ok = False
                continue
            rc, out = run_graded(graded, d, fx, scratch, "fx-" + kind)
            good, detail = fixture_verdict(out, kind, name)
            print("FX %s %s %s" % (kind, "accepted" if good else "refused", detail))
            state[kind] = want if good else ("refused" if want == "accepted" else "accepted")
            if not good:
                fixture_ok = False
            shutil.rmtree(d, ignore_errors=True)
        tail = ("equiv=%s comment=%s selfprint=%s real=%s arms=%s"
                % (state.get("equiv", "absent"), state.get("comment", "absent"),
                   state.get("selfprint", "absent"), "met" if real_ok else "unmet",
                   arms[0] if arms else "?"))
        if not own_ok:
            print("C1=unmet %s detector=red rev=%s" % (tail, rev[:12]))
            print(own_out.strip())
            return 1
        if not subject_ok:
            print("C1=unmet %s subject=arms:%s rev=%s" % (tail, arms, rev[:12]))
            print((sout.strip().splitlines() or [""])[-1])
            return 1
        if not (real_ok and fixture_ok):
            print("C1=unmet %s detector=green rev=%s" % (tail, rev[:12]))
            return 1
        print("C1=met %s rev=%s" % (TARGET, rev[:12]))
        return 0
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
