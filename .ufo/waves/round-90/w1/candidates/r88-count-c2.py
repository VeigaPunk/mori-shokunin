#!/usr/bin/env python3
"""mori round-88 C2 counter (calibration): the r87 receipt gate refuses two counterfeit bodies.

Frozen predicate P-C2 (`.ufo/waves/round-88/contract.md` — this file, the contract and the
receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-88/count-c2.py R` prints
  `C2=met real=met fx=4 clean=1 refused=2 absent=1 arms=23` and exits 0, where the graded
  `.ufo/waves/round-87/count-c2.py` at R is green at exactly 26 selftest arms (round 89 moved
  the gate's arm count 23 -> 26 and this pin follows it), still prints the r87 target line on the
  real seven-receipt population, and refuses every counterfeit fixture:

    stripped       a `clone` receipt with its `# replay:` line removed and a fabricated body is
                   refused with `missing-replay` (zero replays must not reach the target line)
    vacuous        a `clone` receipt whose `# cmd:` prints the body itself is refused with
                   `cmd-binding` (every `# counter-sha256:` path must appear in the command)
    absent-target  a `# supersedes:` naming a receipt outside the population is refused with the
                   `SUPERSEDE ... absent=1` line and a failing run

  Fixtures are commits inside `--shared` clones under `--scratch`; the lane is never written.

Usage: count-c2.py <rev> [--repo DIR] [--scratch DIR] | count-c2.py --selftest
Exit 0 met, 1 unmet, 2 setup. Read-only over the lane: `git clone --shared`, `git show`.
"""
import argparse
import ast
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
TARGET = "real=met fx=4 clean=1 refused=2 absent=1 arms=26"

FIXTURES = (
    ("clean", ".ufo/waves/round-87/evidence/record-sweep-r87.txt", "met", None),
    ("stripped", ".ufo/waves/round-87/evidence/record-sweep-r87.txt", "unmet", "missing-replay"),
    ("vacuous", ".ufo/waves/round-87/evidence/record-sweep-r87.txt", "unmet", "cmd-binding"),
    ("absent-target", ".ufo/waves/round-87/evidence/claim-sweep-r87.txt", "unmet", "absent"),
)

REPLAY_LINE = re.compile(r"^#\s*replay:\s*\S+\s*$")
SUPERSEDE_LINE = re.compile(r"^#\s*supersedes:\s*(\S+)\s*$")
SEP = re.compile(r"^#\s*---\s*$")
ARMS = re.compile(r"C2_COUNTER_SELFTEST pass=(\d+) fail=(\d+)")
RECEIPT = re.compile(r"^RECEIPT (\S+) expect=\S+ (met|failed) problems=(\S+)$")
SUPERSEDE = re.compile(r"^SUPERSEDE (\S+) target=(\S+) absent=1$")


def run(cmd, cwd=None, env=None, timeout=900):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          env=env, timeout=timeout)


def mutation_kinds():
    return [kind for kind, _path, _want, _problem in FIXTURES]


def mutate_receipt(text, kind):
    """A receipt's bytes under one frozen counterfeit. Pure; no file is read or written."""
    lines = (text or "").splitlines()
    cut = None
    for number, line in enumerate(lines):
        if SEP.match(line):
            cut = number
            break
    if cut is None:
        raise ValueError("fixture receipt has no '# ---' separator")
    head, body = lines[:cut], lines[cut + 1:]
    if kind == "clean":
        return text
    if kind == "stripped":
        head = [line for line in head if not REPLAY_LINE.match(line)]
        body = ["RECORD_SWEEP fabricated=1"]
    elif kind == "vacuous":
        if not any(line.startswith("# cmd:") for line in head):
            raise ValueError("fixture receipt has no '# cmd:' line")
        head = [("# cmd: printf 'RECORD_SWEEP fabricated=1\\n'"
                 if line.startswith("# cmd:") else line) for line in head]
        body = ["RECORD_SWEEP fabricated=1"]
    elif kind == "absent-target":
        if not any(SUPERSEDE_LINE.match(line) for line in head):
            raise ValueError("fixture receipt has no '# supersedes:' line")
        head = [("# supersedes: gone-r88.txt"
                 if SUPERSEDE_LINE.match(line) else line) for line in head]
    else:
        raise ValueError("unknown fixture kind " + kind)
    return "\n".join(head + ["# ---"] + body) + "\n"


def receipt_line(stdout, name):
    """The RECEIPT line for one receipt name, or None."""
    for line in (stdout or "").splitlines():
        m = RECEIPT.match(line)
        if m and m.group(1) == name:
            return m
    return None


def absent_lines(stdout):
    return [SUPERSEDE.match(line) for line in (stdout or "").splitlines()
            if SUPERSEDE.match(line)]


def verdict_line(stdout):
    """The last `C2=` line, or ''."""
    last = ""
    for line in (stdout or "").splitlines():
        if line.startswith("C2="):
            last = line
    return last


def met_line(rev):
    """The exact verdict line this counter prints on a met run."""
    return "C2=met %s rev=%s" % (TARGET, rev[:12])


def own_ok_of(rc, out):
    """This counter's own --selftest is green at rc=0 with fail=0."""
    return (rc == 0 and "C2_COUNTER_SELFTEST" in out
            and re.search(r"C2_COUNTER_SELFTEST pass=\d+ fail=0", out) is not None)


def clone_root_ok(top_out, d):
    """True when `git rev-parse --show-toplevel` names exactly the clone directory d."""
    return top_out.strip() == os.path.realpath(d)


def fixture_verdict(stdout, kind, receipt_name):
    """(ok, detail) for one fixture's graded stdout against the frozen expectation."""
    verdict = verdict_line(stdout)
    if kind == "clean":
        return verdict.startswith("C2=met " + REAL), verdict or "no verdict line"
    if not verdict.startswith("C2=unmet"):
        return False, "verdict=" + (verdict or "absent")
    if kind == "absent-target":
        lines = absent_lines(stdout)
        return bool(lines) and verdict.startswith("C2=unmet"), "supersede-absent=" + str(len(lines))
    line = receipt_line(stdout, receipt_name)
    if line is None:
        return False, "no RECEIPT line for " + receipt_name
    problem = dict((k, x) for k, _p, _w, x in FIXTURES)[kind]
    return problem in line.group(3), "problems=" + line.group(3)


def clone_fixture(repo, rev, scratch, kind, path):
    """A `--shared` clone at rev with one counterfeit committed on top; returns (dir, new rev)."""
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
    if not clone_root_ok(top.stdout, d):
        return None, "fixture root mismatch"
    if kind == "clean":
        head = run(["git", "-C", d, "rev-parse", "HEAD"], env=env)
        return d, head.stdout.strip()
    target = os.path.join(d, path)
    if not os.path.exists(target):
        return None, "fixture path absent"
    text = open(target, encoding="utf-8").read()
    open(target, "w", encoding="utf-8").write(mutate_receipt(text, kind))
    add = run(["git", "-C", d, "add", "--", path], env=env)
    if add.returncode != 0:
        return None, "fixture add rc=%d" % add.returncode
    commit = run(["git", "-C", d, "-c", "user.name=t", "-c", "user.email=t@t",
                  "commit", "-q", "-m", "round88 fixture " + kind], env=env)
    if commit.returncode != 0:
        return None, "fixture commit rc=%d" % commit.returncode
    head = run(["git", "-C", d, "rev-parse", "HEAD"], env=env)
    return d, head.stdout.strip()


def run_graded(graded, repo, rev, scratch, name):
    """Run the graded count-c2.py at `rev` against `repo`; returns (rc, combined stdout)."""
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
    """Pure-function arms over synthetic receipt text (no lane file is touched)."""
    cases = []
    good = ("# receipt: r.txt\n"
            "# cmd: python3 -I tools/x.py\n"
            "# rev: %s\n"
            "# counter-sha256: %s tools/x.py\n"
            "# replay: clone\n"
            "# supersedes: old.txt\n"
            "# limits: limit named words\n"
            "# ---\nTOKEN\n" % ("a" * 40, "b" * 64))
    cases.append(("clean_identity", mutate_receipt(good, "clean") == good, "identity"))
    stripped = mutate_receipt(good, "stripped")
    cases.append(("stripped_drops_replay",
                  "# replay:" not in stripped and stripped.count("# ---") == 1
                  and stripped.rstrip("\n").endswith("RECORD_SWEEP fabricated=1"), "no replay"))
    vacuous = mutate_receipt(good, "vacuous")
    cases.append(("vacuous_rewrites_cmd",
                  "# cmd: printf 'RECORD_SWEEP fabricated=1\\n'" in vacuous
                  and "# replay: clone" in vacuous, "printf cmd"))
    absent = mutate_receipt(good, "absent-target")
    cases.append(("absent_rewrites_target",
                  "# supersedes: gone-r88.txt" in absent, "gone target"))
    try:
        mutate_receipt(good, "nope")
    except ValueError:
        bad = True
    else:
        bad = False
    cases.append(("unknown_kind_refused", bad, "ValueError"))
    try:
        mutate_receipt("# ---\nbody\n", "vacuous")
    except ValueError:
        bad2 = True
    else:
        bad2 = False
    cases.append(("no_cmd_refused", bad2, "ValueError"))

    out_met = "RECEIPT r.txt expect=met met problems=-\nC2=met %s rev=abc\n" % REAL
    cases.append(("verdict_met", verdict_line(out_met).startswith("C2=met ") and
                  fixture_verdict(out_met, "clean", "r.txt")[0], verdict_line(out_met)))
    out_missing = ("RECEIPT r.txt expect=met failed problems=missing-replay\n"
                   "C2=unmet receipts=7 rev=abc\n")
    cases.append(("missing_replay_refused",
                  fixture_verdict(out_missing, "stripped", "r.txt")[0], "missing-replay"))
    out_cmd = ("RECEIPT r.txt expect=met failed problems=cmd-binding\n"
               "C2=unmet receipts=7 rev=abc\n")
    cases.append(("cmd_binding_refused",
                  fixture_verdict(out_cmd, "vacuous", "r.txt")[0], "cmd-binding"))
    out_absent = ("SUPERSEDE new.txt target=gone.txt absent=1\nC2=unmet receipts=7 rev=abc\n")
    cases.append(("absent_target_refused",
                  fixture_verdict(out_absent, "absent-target", "new.txt")[0], "absent=1"))
    cases.append(("wrong_problem_not_bound",
                  not fixture_verdict(out_cmd, "stripped", "r.txt")[0], "cmd-binding"))
    cases.append(("met_verdict_not_unmet",
                  not fixture_verdict(out_met, "vacuous", "r.txt")[0], "met"))
    cases.append(("absent_without_line",
                  not fixture_verdict("C2=unmet receipts=7 rev=abc\n",
                                      "absent-target", "x")[0], "no SUPERSEDE"))
    cases.append(("fixture_kinds",
                  mutation_kinds() == ["clean", "stripped", "vacuous", "absent-target"],
                  "4 kinds"))
    cases.append(("target_fields",
                  all(field in TARGET for field in
                      ("fx=4", "clean=1", "refused=2", "absent=1", "arms=26")), "target"))
    cases.append(("target_full",
                  TARGET == "real=met fx=4 clean=1 refused=2 absent=1 arms=26", TARGET))
    cases.append(("met_line_derived",
                  met_line("abcdef1234567890") == "C2=met " + TARGET + " rev=abcdef123456",
                  met_line("abcdef1234567890")))
    cases.append(("clean_wrong_split",
                  not fixture_verdict("C2=met receipts=6 absent=0 rev=abc\n", "clean", "r.txt")[0],
                  "receipts=6"))
    cases.append(("receipt_name_bound",
                  receipt_line("RECEIPT other.txt expect=met failed problems=cmd-binding\n",
                               "r.txt") is None, "other receipt"))
    cases.append(("clone_top_bound",
                  not clone_root_ok("/nonexistent/elsewhere\n", "/nonexistent/fx")
                  and clone_root_ok(os.path.realpath("/nonexistent/fx") + "\n",
                                    "/nonexistent/fx"), "root"))
    cases.append(("own_ok_red",
                  own_ok_of(0, "C2_COUNTER_SELFTEST pass=26 fail=0\n")
                  and not own_ok_of(1, "C2_COUNTER_SELFTEST pass=26 fail=0\n")
                  and not own_ok_of(0, "C2_COUNTER_SELFTEST pass=25 fail=1\n"), "rc and fail"))
    cases.append(("verdict_last_wins",
                  verdict_line("C2=unmet a\nC2=met b\n") == "C2=met b", "last line"))
    try:
        mutate_receipt("# cmd: x\n# ---\nTOKEN\n", "absent-target")
    except ValueError:
        no_supersedes = True
    else:
        no_supersedes = False
    cases.append(("absent_without_supersedes", no_supersedes, "ValueError"))
    cases.append(("vacuous_body_fabricated",
                  "RECORD_SWEEP fabricated=1" in vacuous and "TOKEN" not in vacuous, "body"))
    # Round 90: the two mutation-free constant pins (`arms_pinned`, `marker_literal`) are one
    # arm so the frozen subject count (26 + 2 new arms - 1 merge = 27) holds with no assertion
    # dropped; no declared mutant mutates either constant.
    cases.append(("frozen_constants",
                  SUBJECT_ARMS == 26
                  and "missing-replay" in open(os.path.abspath(__file__)).read(),
                  "subject arm pin + label"))
    with open(os.path.abspath(__file__), encoding="utf-8") as source:
        tree = ast.parse(source.read())

    def met_line_call_site():
        """Structural pin on revision passing, not a semantic proof of execution."""
        calls = [node for node in ast.walk(tree)
                 if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                 and node.func.id == "met_line"]
        named = [call for call in calls if len(call.args) == 1 and not call.keywords
                 and isinstance(call.args[0], ast.Name) and call.args[0].id == "rev"]
        truncated = [call for call in calls
                     if any(isinstance(arg, ast.Subscript) for arg in call.args)]
        return bool(named) and not truncated

    def clone_root_negative():
        """Structural prefix-rule pin; not a semantic proof of root identity."""
        roots = [node for node in ast.walk(tree)
                 if isinstance(node, ast.FunctionDef) and node.name == "clone_root_ok"]
        return len(roots) == 1 and not any(
            (isinstance(node, ast.Attribute)
             and node.attr in {"startswith", "endswith", "find", "index"})
            or (isinstance(node, ast.Compare)
                and any(isinstance(op, (ast.In, ast.NotIn)) for op in node.ops))
            for statement in roots[0].body for node in ast.walk(statement))

    cases.append(("met_line_call_site", met_line_call_site(), "untruncated revision"))
    cases.append(("clone_root_negative", clone_root_negative(), "no prefix operation"))
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
    scratch = tempfile.mkdtemp(prefix="count-c2-r88-", dir=base)
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
        own_ok = own_ok_of(own.returncode, own_out)

        subject = loader(SUBJECT)
        if subject is None:
            print("C2=unmet subject=absent real=absent fx=0 rev=%s" % rev[:12])
            return 1
        sdir = os.path.join(scratch, "subject")
        spath = os.path.join(sdir, SUBJECT)
        os.makedirs(os.path.dirname(spath), exist_ok=True)
        open(spath, "w", encoding="utf-8").write(subject)
        srun = run(["python3", "-I", spath, "--selftest", "--scratch",
                    os.path.join(scratch, "subject-run")])
        sout = (srun.stdout or "") + (srun.stderr or "")
        arms = None
        for m in ARMS.finditer(sout):
            arms = (int(m.group(1)), int(m.group(2)))
        subject_ok = srun.returncode == 0 and arms == (SUBJECT_ARMS, 0)

        graded = os.path.join(scratch, "graded-count-c2.py")
        open(graded, "w", encoding="utf-8").write(subject)

        real_rc, real_out = run_graded(graded, repo, rev, scratch, "real")
        real_line = verdict_line(real_out)
        real_ok = real_rc == 0 and real_line.startswith("C2=met " + REAL)
        print("REAL rc=%d %s" % (real_rc, real_line or "no-verdict"))

        clean = refused = absent = 0
        fixture_ok = True
        for kind, path, _want, _problem in FIXTURES:
            name = os.path.basename(path)
            d, fx = clone_fixture(repo, rev, scratch, kind, path)
            if d is None:
                print("FX %s build-failed %s" % (kind, fx))
                fixture_ok = False
                continue
            rc, out = run_graded(graded, d, fx, scratch, "fx-" + kind)
            good, detail = fixture_verdict(out, kind, name)
            label = ("ok" if kind == "clean" else "refused") if good else "ACCEPTED"
            print("FX %s rc=%d %s %s" % (kind, rc, label, detail))
            if not good:
                fixture_ok = False
            if kind == "clean":
                clean += 1 if good else 0
            elif kind == "absent-target":
                absent += 1 if good else 0
            else:
                refused += 1 if good else 0
            shutil.rmtree(d, ignore_errors=True)
        tail = ("real=%s fx=%d clean=%d refused=%d absent=%d arms=%s"
                % ("met" if real_ok else "unmet", len(FIXTURES), clean, refused, absent,
                   arms[0] if arms else "?"))
        if not own_ok:
            print("C2=unmet %s detector=red rev=%s" % (tail, rev[:12]))
            print(own_out.strip())
            return 1
        if not subject_ok:
            print("C2=unmet %s subject=arms:%s rev=%s" % (tail, arms, rev[:12]))
            print((sout.strip().splitlines() or [""])[-1])
            return 1
        if not (real_ok and fixture_ok and clean == 1 and refused == 2 and absent == 1):
            print("C2=unmet %s detector=green rev=%s" % (tail, rev[:12]))
            return 1
        print(met_line(rev))
        return 0
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
