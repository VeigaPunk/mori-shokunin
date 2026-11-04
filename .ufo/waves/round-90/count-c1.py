#!/usr/bin/env python3
"""mori round-90 C1 counter (operability): the receipt gate refuses every non-executing branch.

Frozen predicate P-C1 (`.ufo/waves/round-90/contract.md` — this file, the contract and the
receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-90/count-c1.py R` prints
  `C1=met branch_open=0 harm=0 newopen=0 open=22 cases=78 rev=<12>` and a line
  `BATTERY cases=<n> branch_cases=<n> branch_open=0 harm=0` with branch_cases >= 12, and
  exits 0, where `branch_open` counts the frozen branch-class counterfeits the receipt gate at R
  still binds, `harm` the `met` cases the entering gate binds and the gate at R refuses, and
  `newopen` the `reject` cases the gate at R binds and the entering gate refuses.

Populations (frozen here, before any after-value):
  * the two round-89 attack batteries (78 counted cases) — `R03` executed cases and the `C02`
    `class=claim` held-out lines. Class is frozen by case id: the eight ids in BRANCH are the
    non-executing-branch class; every other counted `reject` case is the provenance class, which
    a syntax rule cannot decide and which this round only *reports* (`open`).
  * every `battery/*.json` committed under `.ufo/waves/round-90/` at R, graded separately: those
    cases were written by a seat that did not author the rule, so they are not part of the
    fixed main population.

`open` is reported, never targeted: the provenance class stays bound by design (functions,
`PATH`/interpreter substitution, `sitecustomize`, blob overwrite, heredoc data, `uv run -m`,
`bash -n`, `cat`/`$0`). A binding is a statement about the recorded command text; it is not
execution proof and the receipt's replay is the only execution evidence.

Usage: count-c1.py <rev> [--repo DIR] [--entering REV] [--scratch DIR] | --selftest
Output: per case `CASE <source>:<name> class=… expect=… entering=… after=… <kind>`, then the
summary lines. Exit 0 met, 1 unmet, 2 setup. Read-only: `git show`, `git ls-tree`; files only
under --scratch.
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
R89 = os.path.join(HERE, "..", "round-89")
R03 = os.path.join(R89, "r", "Mo89R03Repair-evidence", "cases.json")
C02 = os.path.join(R89, "r", "Mo89C02Critic-evidence", "heldout-all.txt")
GATE = ".ufo/waves/round-87/count-c2.py"
BATTERY_DIR = ".ufo/waves/round-90/battery/"
BOUND = "tools/mori-record-sweep.py"
ENTERING = "30a29797012281b9fd0c748b38b929ac67f8c754"
HCASE = re.compile(r"^HCASE (\S+) expect=(met|reject) class=claim .*? \| (.*)$")

# Frozen class assignment (round 89's `open=30`, split by the r90 plan): the eight
# non-executing-branch counterfeits. Everything else in the counted population is provenance.
BRANCH = frozenset((
    "R03:N-A08-exit-before",
    "R03:N-A09-or-short-circuit",
    "R03:N-A10-false-and",
    "C02:H01-or-short-circuit",
    "C02:H02-false-and",
    "C02:H03-exit-before",
    "C02:H04-if-false",
    "C02:H09-heredoc-or-subshell-false",
))

TARGET = "C1=met branch_open=0 harm=0 newopen=0 open=22 cases=78"
EXPECTED_ARMS = 12


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def load_cases():
    """The two round-89 batteries, with the frozen class of every counted case."""
    cases = [dict(c, source="R03") for c in json.load(open(R03))]
    for line in open(C02):
        m = HCASE.match(line.rstrip("\n"))
        if m:
            cases.append({"name": m.group(1), "expect": m.group(2), "cmd": m.group(3),
                          "source": "C02"})
    for case in cases:
        key = "%s:%s" % (case["source"], case["name"])
        case["class"] = "branch" if key in BRANCH else "prov"
        case["battery"] = "r89"
    return cases


def load_battery(repo, rev):
    """Every `battery/*.json` committed at `rev`, as (cases, paths)."""
    listing = run(["git", "-C", repo, "ls-tree", "-r", "--name-only", rev, "--", BATTERY_DIR])
    cases, paths = [], []
    if listing.returncode != 0:
        return cases, paths
    for path in listing.stdout.split():
        if not path.endswith(".json"):
            continue
        blob = run(["git", "-C", repo, "show", "%s:%s" % (rev, path)])
        if blob.returncode != 0:
            continue
        paths.append(path)
        for item in json.loads(blob.stdout):
            cases.append(dict(item, source="R90", battery=os.path.basename(path)))
    return cases, paths


def gate_at(repo, rev, work):
    out = run(["git", "-C", repo, "show", "%s:%s" % (rev, GATE)])
    if out.returncode != 0:
        raise SystemExit("C1_SETUP gate absent at %s: %s" % (rev, out.stderr.strip()))
    path = os.path.join(work, "gate_%s.py" % rev[:12])
    with open(path, "w", encoding="utf-8") as handle:
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


def tally(cases, before, after, repo, label):
    """Grade one population; returns (counts, lines)."""
    counts = dict(harm=0, newopen=0, open=0, gained=0, cases=0,
                  branch_cases=0, branch_open=0)
    lines = []
    for case in cases:
        b, a = bound(before, case["cmd"], repo), bound(after, case["cmd"], repo)
        if case["expect"] == "met":
            kind = "harm" if b and not a else "gained" if a and not b else \
                   "ok" if a else "refused-both"
        else:
            kind = "newopen" if a and not b else "open" if a else "ok"
        counted = not case.get("reach")
        if counted:
            counts["cases"] += 1
            if kind in ("harm", "gained"):
                counts[kind] += 1
            if kind == "newopen":
                counts["newopen"] += 1
            if case["expect"] == "reject" and a:
                counts["open"] += 1
            if case.get("class") == "branch":
                counts["branch_cases"] += 1
                if case["expect"] == "reject" and a:
                    counts["branch_open"] += 1
        lines.append("CASE %s:%s class=%s expect=%s entering=%s after=%s %s%s" % (
            case["source"], case["name"], case.get("class", "-"), case["expect"],
            "bound" if b else "refused", "bound" if a else "refused", kind,
            "" if counted else " uncounted"))
    lines.append("%s %s" % (label, " ".join(
        "%s=%d" % (k, counts[k]) for k in
        ("cases", "branch_cases", "branch_open", "harm", "newopen", "open", "gained"))))
    return counts, lines


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--repo", default=os.path.abspath(os.path.join(HERE, "..", "..", "..")))
    ap.add_argument("--entering", default=ENTERING)
    ap.add_argument("--scratch")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    base = args.scratch or os.environ.get("HYAKU_SCRATCH") or tempfile.gettempdir()
    os.makedirs(base, exist_ok=True)
    work = tempfile.mkdtemp(prefix="count-c1-r90-", dir=base)
    try:
        if args.selftest:
            return selftest()
        if not args.rev:
            print("C1_SETUP usage: count-c1.py <rev> | --selftest", file=sys.stderr)
            return 2
        top = run(["git", "-C", args.repo, "rev-parse", "--show-toplevel"])
        repo = top.stdout.strip() if top.returncode == 0 else args.repo
        p = run(["git", "-C", repo, "rev-parse", "--verify", args.rev + "^{commit}"])
        if p.returncode != 0:
            print("C1_SETUP unresolvable revision " + args.rev, file=sys.stderr)
            return 2
        rev = p.stdout.strip()
        before = gate_at(repo, args.entering, work)
        after = gate_at(repo, rev, work)
        main_cases = load_cases()
        battery, paths = load_battery(repo, rev)
        counts, lines = tally(main_cases, before, after, repo, "POPULATION")
        for line in lines:
            print(line)
        if battery:
            bcounts, blines = tally(battery, before, after, repo, "BATTERY")
            for line in blines:
                print(line)
        else:
            bcounts = dict(cases=0, branch_cases=0, branch_open=0, harm=0, newopen=0)
        tail = ("C1=%s branch_open=%d harm=%d newopen=%d open=%d cases=%d rev=%s"
                % ("met" if (counts["branch_open"] == 0 and counts["harm"] == 0
                             and counts["newopen"] == 0
                             and counts["open"] == 22 and counts["cases"] == 78
                             and bcounts["branch_cases"] >= 12
                             and bcounts["branch_open"] == 0 and bcounts["harm"] == 0
                             and bcounts["newopen"] == 0) else "unmet",
                   counts["branch_open"], counts["harm"], counts["newopen"],
                   counts["open"], counts["cases"], rev[:12]))
        print(tail)
        print("BATTERY cases=%d branch_cases=%d branch_open=%d harm=%d newopen=%d paths=%d"
              % (bcounts["cases"], bcounts["branch_cases"], bcounts["branch_open"],
                 bcounts["harm"], bcounts["newopen"], len(paths)))
        return 0 if tail.startswith("C1=met ") else 1
    finally:
        import shutil
        shutil.rmtree(work, ignore_errors=True)


def selftest():
    """Arms over synthetic gates and synthetic case lists; no lane file is touched."""
    cases = []

    def fake(name, body):
        d = tempfile.mkdtemp(dir=os.environ.get("HYAKU_SCRATCH") or tempfile.gettempdir())
        path = os.path.join(d, name)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(body)
        spec = importlib.util.spec_from_file_location(name[:-3], path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    deny = fake("deny.py", "def binding_problems(cmd, bindings, replayed, repo=None):\n"
                           "    return []\n")
    allow = fake("allow.py", "def binding_problems(cmd, bindings, replayed, repo=None):\n"
                             "    return ['cmd-binding']\n")
    branch_cases = [{"source": "T", "name": n, "expect": "reject", "cmd": "x",
                     "class": "branch"} for n in ("b1", "b2")]
    met_cases = [{"source": "T", "name": "m1", "expect": "met", "cmd": "x", "class": "prov"}]
    counts, _ = tally(branch_cases, deny, deny, None, "T")
    cases.append(("branch_open_counted", counts["branch_open"] == 2, str(counts)))
    counts, _ = tally(branch_cases, deny, allow, None, "T")
    cases.append(("branch_closed_zero", counts["branch_open"] == 0, str(counts)))
    counts, _ = tally(met_cases, deny, allow, None, "T")
    cases.append(("harm_counted", counts["harm"] == 1, str(counts)))
    counts, _ = tally(met_cases, allow, deny, None, "T")
    cases.append(("harm_absent_when_gate_binds", counts["harm"] == 0, str(counts)))
    counts, _ = tally(branch_cases, allow, allow, None, "T")
    cases.append(("newopen_absent", counts["newopen"] == 0 and counts["open"] == 0, str(counts)))
    counts, _ = tally(branch_cases, allow, deny, None, "T")
    cases.append(("newopen_counted", counts["newopen"] == 2 and counts["open"] == 2, str(counts)))
    reach = [dict(branch_cases[0], reach=True)]
    counts, _ = tally(reach, deny, allow, None, "T")
    cases.append(("reach_uncounted", counts["cases"] == 0 and counts["branch_open"] == 0,
                  str(counts)))
    cases.append(("branch_ids_frozen", len(BRANCH) == 8 and
                  all(k.split(":")[0] in ("R03", "C02") for k in BRANCH), "8 ids"))
    cases.append(("target_literal", TARGET == "C1=met branch_open=0 harm=0 newopen=0 open=22 "
                                              "cases=78", TARGET))
    cases.append(("load_cases_class_split",
                  all(c["class"] == ("branch" if "%s:%s" % (c["source"], c["name"]) in BRANCH
                                     else "prov") for c in load_cases()), "frozen split"))
    cases.append(("counted_population", len([c for c in load_cases() if not c.get("reach")])
                  == 78, str(len([c for c in load_cases() if not c.get("reach")]))))
    cases.append(("own_arms_pinned", len(cases) + 1 == EXPECTED_ARMS,
                  "%d/%d" % (len(cases) + 1, EXPECTED_ARMS)))
    ok = sum(1 for _, good_case, _ in cases if good_case)
    for label, good_case, line in cases:
        print("%s %s %s" % ("PASS" if good_case else "FAIL", label, line))
    print("C1_COUNTER_SELFTEST pass=%d fail=%d" % (ok, len(cases) - ok))
    return 0 if ok == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
