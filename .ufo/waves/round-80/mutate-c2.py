#!/usr/bin/env python3
"""mori round-80 C2 harness (operability): does count-c2.py's selftest kill the mutants?

Frozen predicate P-C2 (contract `.ufo/waves/round-80/contract.md`, this harness and the
receipt label are the same sentence):

  At revision R this harness applies its six frozen mutants one at a time to a scratch copy
  of `.ufo/waves/round-79/count-c2.py` as it stands at R and runs `--selftest` after each; it
  prints `MUTATION_C2 survivors=0 killed=6 total=6` and exits 0. At the entering revision the
  same harness prints `survivors=2 killed=4 total=6` measured at `d5888922` (the round-79 seat
  named three survivors; this frozen six-mutant set is the one that grades, and the contract
  records both readings).

Grade per mutant: KILLED iff the copied counter's `--selftest` exits nonzero or prints a
nonzero `fail=`; SURVIVED iff it exits 0 with `pass=N fail=0`. Declared limit: the grade is
the selftest verdict only — a mutant that changes the real reading while the selftest stays
green is exactly what this harness calls a survivor (that is the defect class it exists for).

An anchor missing at R is `MUTATION_SETUP anchor-absent <label>` rc 2 — a drifted file never
silently scores as a survivor.

Usage: mutate-c2.py --rev R [--repo DIR] [--scratch DIR] | mutate-c2.py --selftest
Output: one `mutant <label> <killed|survived>` line per mutant, then
`MUTATION_C2 survivors=S killed=K total=6 rev=<sha12>`; rc 0 all killed, 1 any survivor, 2 setup.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

MUTANTS = [
    ("drop_admitted",
     '        if r.get("lane") != LANE or not r.get("admitted"):\n',
     '        if r.get("lane") != LANE:\n'),
    ("raise_ceiling",
     "        if not isinstance(rn, int) or rn > through:\n",
     "        if not isinstance(rn, int) or rn > 10 ** 6:\n"),
    ("count_other_verdicts",
     '            if axis in AXES and verdict in ("improved", "harmed"):\n',
     '            if axis in AXES and verdict in ("improved", "harmed", "unchanged", '
     '"unprovable"):\n'),
    ("cut_clause_boundary",
     '        tail = cell[m.end():].split(";")[0]\n',
     "        tail = cell[m.end():]\n"),
    ("any_round_in_cell",
     "        m = ROUND.search(cell)\n",
     "        _ms = list(ROUND.finditer(cell)); m = _ms[-1] if _ms else None\n"),
    ("met_ignores_mismatch",
     "    met = mismatches == 0 and errors == 0\n",
     "    met = errors == 0\n"),
]
COUNTER = ".ufo/waves/round-79/count-c2.py"


def run(cmd, env=None):
    return subprocess.run(cmd, capture_output=True, text=True, env=env)


def selftest_verdict(path, scratch):
    env = dict(os.environ)
    env["TMPDIR"] = scratch
    p = run(["python3", "-I", path, "--selftest", "--scratch", scratch], env=env)
    out = p.stdout + p.stderr
    m = re.search(r"C2_COUNTER_SELFTEST pass=(\d+) fail=(\d+)", out)
    if not m:
        return "killed", f"no-summary rc={p.returncode}"
    fail = int(m.group(2))
    if p.returncode != 0 or fail:
        return "killed", f"rc={p.returncode} {m.group(0)}"
    return "survived", f"rc=0 {m.group(0)}"


def grade(text, scratch):
    results = []
    for label, old, new in MUTANTS:
        if old not in text:
            print(f"MUTATION_SETUP anchor-absent {label}", file=sys.stderr)
            return None
        mutated = text.replace(old, new, 1)
        if mutated == text:
            print(f"MUTATION_SETUP no-change {label}", file=sys.stderr)
            return None
        d = tempfile.mkdtemp(dir=scratch)
        path = os.path.join(d, "count-c2.py")
        open(path, "w", encoding="utf-8").write(mutated)
        verdict, detail = selftest_verdict(path, d)
        print(f"mutant {label} {verdict} {detail}")
        results.append(verdict)
    return results


def _fixture(path_, red):
    anchors = "\n".join(old.rstrip("\n") for _, old, _ in MUTANTS)
    body = (
        "#!/usr/bin/env python3\n"
        "import sys\n"
        "ANCHORS = '''\n" + anchors + "\n'''\n"
        "def main():\n"
        "    if '--selftest' in sys.argv:\n"
        "        print('C2_COUNTER_SELFTEST pass=6 fail=0')\n"
        f"        return {1 if red else 0}\n"
        "    return 0\n"
        "sys.exit(main())\n")
    open(path_, "w", encoding="utf-8").write(body)


def selfcheck(scratch):
    cases = []
    for label, red, want in (("green_stub_all_survive", False, 6),
                             ("red_stub_all_killed", True, 0)):
        d = tempfile.mkdtemp(dir=scratch)
        path = os.path.join(d, "count-c2.py")
        _fixture(path, red)
        text = open(path, encoding="utf-8").read()
        d2 = tempfile.mkdtemp(dir=scratch)
        res = grade(text, d2)
        ok = res is not None and res.count("survived") == want and len(res) == 6
        cases.append((label, ok, f"survivors={0 if res is None else res.count('survived')}"))
    # anchor presence in the real counter at the current worktree, if readable
    real = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "round-79",
                        "count-c2.py")
    if os.path.isfile(real):
        text = open(real, encoding="utf-8").read()
        absent = [label for label, old, _ in MUTANTS if old not in text]
        cases.append(("real_counter_anchors", not absent, f"absent={absent}"))
    ok = sum(1 for _, good, _ in cases if good)
    for label, good, line in cases:
        print(f"{'PASS' if good else 'FAIL'} {label} {line}")
    print(f"MUTATE_C2_SELFTEST pass={ok} fail={len(cases) - ok}")
    return 0 if ok == len(cases) else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev")
    ap.add_argument("--repo", default=os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")))
    ap.add_argument("--scratch")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    base = a.scratch or os.environ.get("HYAKU_SCRATCH") or tempfile.gettempdir()
    os.makedirs(base, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="mutate-c2-r80-", dir=base)
    try:
        if a.selftest:
            return selfcheck(scratch)
        if not a.rev:
            print("MUTATION_SETUP usage: mutate-c2.py --rev R | --selftest", file=sys.stderr)
            return 2
        top = run(["git", "-C", a.repo, "rev-parse", "--show-toplevel"])
        repo = top.stdout.strip() if top.returncode == 0 else a.repo
        p = run(["git", "-C", repo, "rev-parse", "--verify", a.rev + "^{commit}"])
        if p.returncode != 0:
            print(f"MUTATION_SETUP unresolvable revision {a.rev}", file=sys.stderr)
            return 2
        rev = p.stdout.strip()
        s = run(["git", "-C", repo, "show", f"{rev}:{COUNTER}"])
        if s.returncode != 0:
            print(f"MUTATION_SETUP {COUNTER} absent at rev", file=sys.stderr)
            return 2
        base_path = os.path.join(tempfile.mkdtemp(dir=scratch), "count-c2.py")
        open(base_path, "w", encoding="utf-8").write(s.stdout)
        base_verdict, base_detail = selftest_verdict(base_path, os.path.dirname(base_path))
        print(f"unmutated {base_verdict} {base_detail}")
        if base_verdict != "survived":
            print("MUTATION_SETUP unmutated selftest is not green at rev", file=sys.stderr)
            return 2
        res = grade(s.stdout, scratch)
        if res is None:
            return 2
        survivors = res.count("survived")
        killed = len(res) - survivors
        print(f"MUTATION_C2 survivors={survivors} killed={killed} total={len(MUTANTS)} "
              f"unmutated=green rev={rev[:12]}")
        return 0 if survivors == 0 else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
