#!/usr/bin/env python3
"""Mo89R03Repair grader: binding verdicts at the entering and repaired gate + real execution.

Usage: grade_new.py <repo> <clone> <scratch> <cases.json> <out.jsonl>
For each case:
  entering/after = binding_problems(cmd, [("0"*64, BOUND)], True, repo) == [] with the gate loaded
                   from `git show <rev>:.ufo/waves/round-87/count-c2.py` (entering takes no repo)
  pristine run   = `bash -c cmd` in the --shared clone reset to AFTER (rc, stdout == genuine?)
  witness run    = same, with the clone's bound file instrumented (line 2 appends to a marker
                   file): executed=True iff CPython ran the bound blob from the replay tree
Classes as noharm-c1.py: met -> harm|gained|ok|refused-both; reject -> open|ok.
"""
import importlib.util
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True
ENTERING = "30a29797012281b9fd0c748b38b929ac67f8c754"
AFTER = "9f4d20b9290faff54354d6ab6b08982d98d5e72c"
GATE = ".ufo/waves/round-87/count-c2.py"
BOUND = "tools/mori-record-sweep.py"
GENUINE = "python3 -I tools/mori-record-sweep.py --root . --pins .ufo/waves/round-82/record-pins.json"
repo, clone, scratch, cases_path, out_path = sys.argv[1:6]
MARK = os.path.join(scratch, "executed.mark")


def gate_at(rev):
    src = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, GATE)],
                         capture_output=True, text=True, check=True).stdout
    path = os.path.join(scratch, "gate_%s.py" % rev[:12])
    open(path, "w").write(src)
    spec = importlib.util.spec_from_file_location("gate_%s" % rev[:12], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def bound(gate, cmd):
    try:
        return gate.binding_problems(cmd, [("0" * 64, BOUND)], True, repo) == []
    except TypeError:
        return gate.binding_problems(cmd, [("0" * 64, BOUND)], True) == []


def git(*args):
    return subprocess.run(["git", "-C", clone] + list(args), capture_output=True, text=True)


def reset():
    top = git("rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(clone), top
    assert git("checkout", "-q", "-f", AFTER).returncode == 0
    assert git("clean", "-q", "-fdx").returncode == 0
    if os.path.exists(MARK):
        os.remove(MARK)


def run(cmd):
    env = dict(os.environ, TMPDIR=os.path.join(scratch, "tmp"), GIT_CONFIG_GLOBAL=os.devnull,
               GIT_CONFIG_SYSTEM=os.devnull, PYTHONDONTWRITEBYTECODE="1")
    try:
        p = subprocess.run(["bash", "-c", cmd], cwd=clone, env=env, stdin=subprocess.DEVNULL,
                           capture_output=True, text=True, timeout=180)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"


def instrument():
    path = os.path.join(clone, BOUND)
    lines = open(path).read().split("\n")
    lines.insert(1, "open(%r, 'a').write('ran\\n')" % MARK)
    open(path, "w").write("\n".join(lines))


before, after = gate_at(ENTERING), gate_at(AFTER)
reset()
g_rc, g_out, _ = run(GENUINE)
assert g_rc == 0 and g_out.startswith("RECORD_SWEEP"), (g_rc, g_out)
print("GENUINE rc=%d stdout=%r" % (g_rc, g_out))
rows = []
for c in json.load(open(cases_path)):
    b, a = bound(before, c["cmd"]), bound(after, c["cmd"])
    reset()
    rc, out, err = run(c["cmd"])
    reset()
    instrument()
    run(c["cmd"])
    executed = os.path.exists(MARK)
    reset()
    if c["expect"] == "met":
        kind = "harm" if b and not a else "gained" if a and not b else "ok" if a else "refused-both"
        truth = executed and rc == 0 and out == g_out
    else:
        kind = "open" if a else "ok"
        truth = not executed
    row = dict(name=c["name"], expect=c["expect"], reach=c.get("reach", "header"),
               entering="bound" if b else "refused", after="bound" if a else "refused",
               kind=kind, rc=rc, stdout_eq_genuine=(out == g_out), executed=executed,
               expectation_confirmed=truth, stderr_tail=err.strip()[-160:], cmd=c["cmd"])
    rows.append(row)
    print("CASE %-30s expect=%-6s entering=%-7s after=%-7s %-12s rc=%-3d same_stdout=%-5s executed=%-5s confirmed=%s%s"
          % (c["name"], c["expect"], row["entering"], row["after"], kind, rc, out == g_out,
             executed, truth, "" if row["reach"] == "header" else " [header-unreachable]"))
with open(out_path, "w") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
tally = {}
for r in rows:
    key = (r["kind"], r["reach"])
    tally[key] = tally.get(key, 0) + 1
print("TALLY " + " ".join("%s%s=%d" % (k, "" if r == "header" else "(unreachable)", n)
                          for (k, r), n in sorted(tally.items())))
print("UNCONFIRMED " + ",".join(r["name"] for r in rows if not r["expectation_confirmed"]))
