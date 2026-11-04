#!/usr/bin/env python3
"""mori round 89 — C1 held-out batteries: the r87 gate's binding at <rev> versus the entering gate.

Case files are the residual attack seats' batteries, written against repair 1 (`9f4d20b9`)
before repair 2 existed: `r/Mo89R03Repair-evidence/cases.json` (59 cases; every expectation
executed in a clone by that seat: `met` cases ran the bound blob with the genuine stdout,
`reject` cases never ran it) and `r/Mo89C02Critic-evidence/heldout-all.txt` (the 22 `class=claim`
HCASE lines). Cases tagged `reach` (a newline inside `# cmd:`, which the one-line header cannot
carry) are printed but not counted.

  harm    = `met` cases the entering gate binds and the gate at <rev> refuses
  newopen = `reject` cases the gate at <rev> binds and the entering gate refuses
  open    = `reject` cases the gate at <rev> binds (whatever the entering gate did)
  gained  = `met` cases the entering gate refuses and the gate at <rev> binds

Prints `HELDOUT harm=<n> newopen=<n> open=<n> gained=<n> cases=<n> rev=<12>`; exits 0 iff
harm=0 and newopen=0 (no worse than entering on either side); 1 otherwise; 2 setup.

Usage: heldout-c1.py <rev> [--repo DIR] [--entering REV]
"""
import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
R03 = os.path.join(HERE, "r", "Mo89R03Repair-evidence", "cases.json")
C02 = os.path.join(HERE, "r", "Mo89C02Critic-evidence", "heldout-all.txt")
GATE = ".ufo/waves/round-87/count-c2.py"
BOUND = "tools/mori-record-sweep.py"
ENTERING = "30a29797012281b9fd0c748b38b929ac67f8c754"
HCASE = re.compile(r"^HCASE (\S+) expect=(met|reject) class=claim .*? \| (.*)$")


def load_cases():
    cases = [dict(c, source="R03") for c in json.load(open(R03))]
    for line in open(C02):
        m = HCASE.match(line.rstrip("\n"))
        if m:
            cases.append({"name": m.group(1), "expect": m.group(2), "cmd": m.group(3),
                          "source": "C02"})
    return cases


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
    cases = load_cases()
    if len(cases) < 2:
        print("setup: no cases")
        return 2
    rev = subprocess.run(["git", "-C", args.repo, "rev-parse", args.rev + "^{commit}"],
                         capture_output=True, text=True).stdout.strip()
    if not rev:
        print("setup: bad rev %s" % args.rev)
        return 2
    tally = dict(harm=0, newopen=0, open=0, gained=0, cases=0)
    with tempfile.TemporaryDirectory(prefix="heldout-") as work:
        before, after = gate_at(args.repo, args.entering, work), gate_at(args.repo, rev, work)
        for case in cases:
            b, a = bound(before, case["cmd"], args.repo), bound(after, case["cmd"], args.repo)
            if case["expect"] == "met":
                kind = "harm" if b and not a else "gained" if a and not b else \
                       "ok" if a else "refused-both"
            else:
                kind = "newopen" if a and not b else "open" if a else "ok"
            counted = not case.get("reach")
            if counted:
                tally["cases"] += 1
                if kind in ("harm", "gained"):
                    tally[kind] += 1
                if kind == "newopen":
                    tally["newopen"] += 1
                if case["expect"] == "reject" and a:
                    tally["open"] += 1
            print("CASE %s:%s expect=%s entering=%s after=%s %s%s" % (
                case["source"], case["name"], case["expect"], "bound" if b else "refused",
                "bound" if a else "refused", kind, "" if counted else " uncounted"))
    print("HELDOUT harm=%(harm)d newopen=%(newopen)d open=%(open)d gained=%(gained)d "
          "cases=%(cases)d" % tally + " rev=%s" % rev[:12])
    return 0 if tally["harm"] == 0 and tally["newopen"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
