#!/usr/bin/env python3
"""mori round 89 — C1 no-harm battery for the r87 receipt gate's execution binding.

The case set is the C1 reviewer's adversarial battery (`w1/Mo89R01C1-evidence/cases.json` and
`cases2.json`, written by seat Mo89R01C1 against `760428ab` before the binding repair), minus
`E15-semicolon-in-quoted-arg`, which that seat itself voided (the script has no `--note`).
Each case is a `# cmd:` string with the bound path `tools/mori-record-sweep.py` and an
expectation: `met` (a valid equivalent replay of the bound script) or `reject` (a counterfeit
binding). The binding rule alone is graded: `binding_problems(cmd, bindings, True, repo)` of the
gate module loaded from `git show <rev>:.ufo/waves/round-87/count-c2.py`.

  harm   = `met` cases the entering gate binds and the gate at <rev> refuses
  open   = `reject` cases the gate at <rev> binds
  gained = `met` cases the entering gate refuses and the gate at <rev> binds

Prints `NOHARM harm=<n> open=<n> gained=<n> cases=<n> rev=<12>` and exits 0 iff harm=0 and
open=0; 1 otherwise; 2 setup.

Usage: noharm-c1.py <rev> [--repo DIR] [--entering REV]
"""
import argparse
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
CASES = [os.path.join(HERE, "w1", "Mo89R01C1-evidence", n) for n in ("cases.json", "cases2.json")]
VOID = {"E15-semicolon-in-quoted-arg"}
GATE = ".ufo/waves/round-87/count-c2.py"
BOUND = "tools/mori-record-sweep.py"
ENTERING = "30a29797012281b9fd0c748b38b929ac67f8c754"


def gate_at(repo, rev, work):
    out = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, GATE)],
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit("setup: %s" % out.stderr.strip())
    path = os.path.join(work, "gate_%s.py" % rev[:12])
    with open(path, "w") as handle:
        handle.write(out.stdout)
    spec = importlib.util.spec_from_file_location("gate_%s" % rev[:12], path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def bound(gate, cmd, repo):
    try:
        return gate.binding_problems(cmd, [("0" * 64, BOUND)], True, repo) == []
    except TypeError:                       # the entering gate takes no repo argument
        return gate.binding_problems(cmd, [("0" * 64, BOUND)], True) == []


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev")
    ap.add_argument("--repo", default=os.path.abspath(os.path.join(HERE, "..", "..", "..")))
    ap.add_argument("--entering", default=ENTERING)
    args = ap.parse_args(argv)
    cases = [c for f in CASES for c in json.load(open(f)) if c["name"] not in VOID]
    if not cases:
        print("setup: no cases")
        return 2
    rev = subprocess.run(["git", "-C", args.repo, "rev-parse", args.rev + "^{commit}"],
                         capture_output=True, text=True).stdout.strip()
    if not rev:
        print("setup: bad rev %s" % args.rev)
        return 2
    with tempfile.TemporaryDirectory(prefix="noharm-") as work:
        before, after = gate_at(args.repo, args.entering, work), gate_at(args.repo, rev, work)
        harm = opened = gained = 0
        for case in cases:
            b, a = bound(before, case["cmd"], args.repo), bound(after, case["cmd"], args.repo)
            if case["expect"] == "met":
                kind = "harm" if b and not a else "gained" if a and not b else \
                       "ok" if a else "refused-both"
                harm += kind == "harm"
                gained += kind == "gained"
            else:
                kind = "open" if a else "ok"
                opened += kind == "open"
            print("CASE %s expect=%s entering=%s after=%s %s" % (
                case["name"], case["expect"], "bound" if b else "refused",
                "bound" if a else "refused", kind))
    print("NOHARM harm=%d open=%d gained=%d cases=%d rev=%s"
          % (harm, opened, gained, len(cases), rev[:12]))
    return 0 if harm == 0 and opened == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
