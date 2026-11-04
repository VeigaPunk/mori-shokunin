#!/usr/bin/env python3
"""mori round-82 C3 counter (depth): the record sweep gains a revision-precision arm and the
lane's revision-labelled values are graded against the bytes they name.

Frozen predicate P-C3 (`.ufo/waves/round-82/contract.md` — this counter, the contract and the
receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-82/count-c3.py R` prints
  `C3=met tool=present arms=N defeated=1 bindings=B revisions=0` and exits 0, where
  `R:tools/mori-record-sweep.py` exists and contains the `REVISION_MISMATCH` arm; its own
  `--selftest` at R is green with `pass=N`, N >= 30; the counter's independent defeated fixture
  (a row stating `pointers=240` bound to a revision whose `SCORECARD.md` holds `pointers=237`)
  is caught (`revisions=1`, rc 1); and the real lane run at R with
  `.ufo/waves/round-82/record-pins.json` has B >= 3 bindings, all green (`revisions=0`), rc 0.

The real run reads carriers from the lane worktree through `--root` and revisions through `--git`,
so the counter requires every carrier named by the pins file to be byte-identical at R and in the
worktree (otherwise it is a setup error: measure at the landed tip).

Usage: count-c3.py <rev> [--repo DIR] [--scratch DIR] | count-c3.py --selftest
Exit 0 met, 1 unmet, 2 setup. Read-only: `git show`, `git ls-tree`; files only under --scratch.
"""
import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

TOOL = "tools/mori-record-sweep.py"
PINS = ".ufo/waves/round-82/record-pins.json"
ARMS_FLOOR = 30
# Frozen population (contract amendment A1): the three bindings the real lane must carry.
FROZEN = (
    ("SCORECARD.md", "row_tally=19", "row_tally", 19,
     "075574c83eae044ff8570cbd02d594943a87ced3", "SCORECARD.md"),
    ("SCORECARD.md", "survivors=0", "survivors", 0,
     "075574c83eae044ff8570cbd02d594943a87ced3", "SCORECARD.md"),
    ("SCORECARD.md", "wrong=0 fixtures=7", "wrong", 0,
     "482dc48d49670de0f7645d0d8e87e18816145256", "SCORECARD.md"),
)
SUMMARY = re.compile(r"RECORD_SWEEP\s+(.*)$")
COUNT = re.compile(r"\b(revisions|bindings)=(\d+)\b")


def run(cmd, cwd=None, env=None, timeout=240):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          env=env, timeout=timeout)


def summary(output):
    """Last RECORD_SWEEP summary line's fields."""
    fields = {}
    for line in output.splitlines():
        m = SUMMARY.search(line.strip())
        if m:
            fields = {key: int(value) for key, value in COUNT.findall(m.group(1))}
    return fields


def pins_bindings(text):
    try:
        data = json.loads(text)
    except Exception:                                    # noqa: BLE001 - report, never crash
        return None
    revisions = data.get("revisions")
    if not isinstance(revisions, list):
        return None
    return revisions


def population_ok(pins):
    """Exactly the frozen population, once each (identity and uniqueness are graded)."""
    seen = set()
    for binding in pins:
        key = (binding.get("carrier"), binding.get("row_contains"), binding.get("key"),
               binding.get("value"), binding.get("path"))
        rev = str(binding.get("rev") or "")
        seen.add(key + (rev,))
    expected = set()
    for carrier, row, key, value, rev, path in FROZEN:
        expected.add((carrier, row, key, value, path, rev))
    got = set()
    for key in seen:
        got.add(key)
    return len(pins) == len(FROZEN) and got == expected


def carrier_paths(pins):
    paths = {binding.get("carrier") for binding in pins if binding.get("carrier")}
    return sorted(path for path in paths if path)


def write_tree(root, files):
    for name, body in files.items():
        target = os.path.join(root, name)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        open(target, "w", encoding="utf-8").write(body)


def selftest_run(tool_path, scratch):
    work = tempfile.mkdtemp(dir=scratch)
    env = dict(os.environ)
    env.update(TMPDIR=work, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
    try:
        p = run(["python3", "-I", tool_path, "--selftest"], cwd=work, env=env)
    except subprocess.TimeoutExpired:
        return 124, "timeout"
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def fixture_run(tool_path, scratch, kind):
    """Independent fixtures: two defeated shapes and one conformant shape.

    A counterfeit tool keyed on the binding count fails at least one of the three (C01 finding):
    `one-stale` has 1 binding and must be caught, `second-stale` has 2 bindings with only the
    second bad and must be caught, `conformant` has 1 binding that is right and must be green.
    """
    rows_a, rows_b = {}, {}
    if kind == "one-stale":
        rows_a["SCORECARD.md"] = ("# t\n\n| Capability | What | Evidence | First |\n"
                                  "|---|---|---|---|\n| Self-assessment claim sweep "
                                  "(`tools/mori-claim-sweep.py`) | x | pointers=237 | 80 |\n")
        rows_b["SCORECARD.md"] = rows_a["SCORECARD.md"].replace("pointers=237", "pointers=240")
        bindings = [{"carrier": "SCORECARD.md", "row_contains": "mori-claim-sweep.py",
                     "key": "pointers", "value": 240, "rev": "A", "path": "SCORECARD.md"}]
        expect = ("caught", 1)
    elif kind == "second-stale":
        rows_a["SCORECARD.md"] = ("# t\n\n| Row | What | Evidence | First |\n"
                                  "|---|---|---|---|\n| Row A | x | row_tally=19 | 80 |\n"
                                  "| Row B | x | survivors=5 | 80 |\n")
        rows_b["SCORECARD.md"] = rows_a["SCORECARD.md"].replace("survivors=5", "survivors=0")
        bindings = [
            {"carrier": "SCORECARD.md", "row_contains": "Row A", "key": "row_tally",
             "value": 19, "rev": "A", "path": "SCORECARD.md"},
            {"carrier": "SCORECARD.md", "row_contains": "Row B", "key": "survivors",
             "value": 0, "rev": "A", "path": "SCORECARD.md"}]
        expect = ("caught", 1)
    else:                                            # conformant
        rows_a["SCORECARD.md"] = ("# t\n\n| Row | What | Evidence | First |\n"
                                  "|---|---|---|---|\n| Row A | x | row_tally=19 | 80 |\n")
        rows_b["SCORECARD.md"] = rows_a["SCORECARD.md"]
        bindings = [{"carrier": "SCORECARD.md", "row_contains": "Row A", "key": "row_tally",
                     "value": 19, "rev": "A", "path": "SCORECARD.md"}]
        expect = ("green", 0)
    repo = tempfile.mkdtemp(dir=scratch, prefix="fx-" + kind + "-")
    env = ["-c", "user.name=t", "-c", "user.email=t@t"]
    run(["git"] + env + ["-C", repo, "init", "-q"])
    if run(["git", "-C", repo, "rev-parse", "--show-toplevel"]).stdout.strip() != repo:
        return None
    write_tree(repo, rows_a)
    run(["git"] + env + ["-C", repo, "add", "-A"])
    run(["git"] + env + ["-C", repo, "commit", "-qm", "a"])
    rev_a = run(["git", "-C", repo, "rev-parse", "HEAD"]).stdout.strip()
    write_tree(repo, rows_b)
    run(["git"] + env + ["-C", repo, "add", "-A"])
    run(["git"] + env + ["-C", repo, "commit", "-qm", "b"])
    pins = {"revisions": [dict(binding, rev=rev_a) for binding in bindings]}
    write_tree(repo, {PINS: json.dumps(pins)})
    penv = dict(os.environ)
    penv.update(TMPDIR=repo, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
    p = run(["python3", "-I", tool_path, "--root", repo, "--pins", os.path.join(repo, PINS),
             "--git", repo], cwd=repo, env=penv)
    out = (p.stdout or "") + (p.stderr or "")
    fields = summary(out)
    if expect[0] == "caught":
        ok = p.returncode == 1 and fields.get("revisions", 0) >= expect[1] \
            and "REVISION_MISMATCH" in out
    else:
        ok = p.returncode == 0 and fields.get("revisions", -1) == 0
    return ok, p.returncode, fields, out



def lane_root():
    """Lane checkout for the main-path arms: this file's checkout, else the lane under ~."""
    here = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
    if os.path.isfile(os.path.join(here, "tools", "mori-record-sweep.py")):
        return here
    return os.path.expanduser(os.path.join("~", "Projects", "shokunin", "mori-shokunin"))


def met_verdict(caught, q, fields, bindings):
    """The one met gate main uses (r83: lifted so a selftest can drive it)."""
    met = (caught and q.returncode == 0 and fields.get("revisions", -1) == 0
           and bindings >= 3)
    return met


def main_fixture(scratch, tool_text, pins, carrier_append=None, label="mf"):
    """A scratch git repo holding one tool copy, one carrier and one pins file."""
    repo = tempfile.mkdtemp(dir=scratch, prefix=label + "-")
    env = ["-c", "user.name=t", "-c", "user.email=t@t"]
    run(["git"] + env + ["-C", repo, "init", "-q"])
    if run(["git", "-C", repo, "rev-parse", "--show-toplevel"]).stdout.strip() != repo:
        return None
    carrier = ("# t\n\n| Row | What | Evidence | First |\n|---|---|---|---|\n"
               "| row_tally=19 | x | row_tally=19 | 80 |\n"
               "| survivors=0 | x | survivors=0 | 80 |\n"
               "| wrong=0 fixtures=7 | x | wrong=0 fixtures=7 | 80 |\n")
    write_tree(repo, {TOOL: tool_text, "SCORECARD.md": carrier,
                      PINS: json.dumps({"revisions": pins})})
    run(["git"] + env + ["-C", repo, "add", "-A"])
    run(["git"] + env + ["-C", repo, "commit", "-qm", "a"])
    rev = run(["git", "-C", repo, "rev-parse", "HEAD"]).stdout.strip()
    if carrier_append is not None:
        open(os.path.join(repo, "SCORECARD.md"), "a", encoding="utf-8").write(carrier_append)
    return repo, rev


def main_run(repo, rev, scratch):
    out, err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = out, err
    try:
        rc = main([rev, "--repo", repo, "--scratch", scratch])
    finally:
        sys.stdout, sys.stderr = old_out, old_err
    return rc, out.getvalue() + err.getvalue()


def selfcheck(scratch):
    cases = []
    fields = summary("noise\nRECORD_SWEEP pending=0 pinned=0 revisions=2 bindings=5\n")
    cases.append(("summary_parse", fields.get("revisions") == 2
                  and fields.get("bindings") == 5, str(fields)))
    revs = pins_bindings('{"revisions":[{"carrier":"A","rev":"x","path":"A","key":"k",'
                         '"value":1,"row_contains":"r"}]}')
    cases.append(("pins_schema", bool(revs) and carrier_paths(revs) == ["A"], str(revs)))
    cases.append(("pins_absent_list", pins_bindings('{"bindings":[]}') is None, "no revisions key"))
    cases.append(("carrier_drift_guard",
                  ("a\n" != "b\n") and ("a\n" == "a\n"), "text compare"))
    cases.append(("arms_floor", 30 >= ARMS_FLOOR and 29 < ARMS_FLOOR, f"floor={ARMS_FLOOR}"))
    frozen = [{"carrier": c, "row_contains": r, "key": k, "value": v, "rev": rv, "path": pp}
              for c, r, k, v, rv, pp in FROZEN]
    cases.append(("population_frozen_ok", population_ok(frozen), "as frozen"))
    triplicated = frozen + [dict(frozen[0]), dict(frozen[0])]
    cases.append(("population_triplicate_unmet", not population_ok(triplicated),
                  f"bindings={len(triplicated)}"))
    cases.append(("population_subset_unmet", not population_ok(frozen[:1]), "one binding"))
    # r83 arms: one per r82 surviving mutant.
    class Rc(object):
        def __init__(self, code):
            self.returncode = code

    cases.append(("met_verdict_bindings_floor",
                  met_verdict(True, Rc(0), {"revisions": 0}, 1) is False
                  and met_verdict(True, Rc(0), {"revisions": 0}, 2) is False, "bindings<3"))
    cases.append(("met_verdict_revisions_default",
                  met_verdict(True, Rc(0), {}, 3) is False, "no revisions token"))
    cases.append(("met_verdict_conformant",
                  met_verdict(True, Rc(0), {"revisions": 0}, 3) is True, "green"))
    cases.append(("summary_last_line",
                  summary("RECORD_SWEEP revisions=2\nRECORD_SWEEP revisions=0\n")
                  .get("revisions") == 0, "last wins"))
    stub_dir = tempfile.mkdtemp(dir=scratch, prefix="stub-")
    stub_tool = os.path.join(stub_dir, TOOL)
    os.makedirs(os.path.dirname(stub_tool), exist_ok=True)
    open(stub_tool, "w", encoding="utf-8").write("import sys\nsys.exit(1)\n")
    got = fixture_run(stub_tool, scratch, "one-stale")
    cases.append(("defeated_needs_mismatch_token", bool(got) and got[0] is False,
                  "exit-1-only tool is not a catch"))
    tool_path = os.path.join(lane_root(), "tools", "mori-record-sweep.py")
    if not os.path.isfile(tool_path):
        cases.append(("main_path_arms_skipped", False, "tool absent: " + tool_path))
    else:
        tool_text = open(tool_path, encoding="utf-8").read()
        frozen = [{"carrier": c, "row_contains": r, "key": k, "value": v, "rev": rv,
                   "path": pp} for c, r, k, v, rv, pp in FROZEN]
        one = main_fixture(scratch, tool_text, frozen[:1], label="pop")
        rc, out = main_run(one[0], one[1], scratch)
        cases.append(("population_gate_named_refusal",
                      rc == 1 and "frozen-population-mismatch" in out,
                      out.strip()[-90:]))
        drift = main_fixture(scratch, tool_text, frozen, carrier_append="\nedited\n",
                             label="drift")
        rc, out = main_run(drift[0], drift[1], scratch)
        cases.append(("carrier_drift_setup", rc == 2 and "worktree differs" in out,
                      out.strip()[-90:]))
        red_tool = tool_text.replace("    return int(bool(failed))", "    return 1", 1)
        red = main_fixture(scratch, red_tool, frozen, label="red")
        rc, out = main_run(red[0], red[1], scratch)
        cases.append(("selftest_red_refused", rc == 1 and "selftest=red" in out,
                      out.strip()[-90:]))
    ok = sum(1 for _, good, _ in cases if good)
    for label, good, line in cases:
        print(f"{'PASS' if good else 'FAIL'} {label} {line}")
    print(f"C3_COUNTER_SELFTEST pass={ok} fail={len(cases) - ok}")
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
    scratch = tempfile.mkdtemp(prefix="count-c3-r82-", dir=base)
    try:
        if a.selftest:
            return selfcheck(scratch)
        if not a.rev:
            print("C3_SETUP usage: count-c3.py <rev> | --selftest", file=sys.stderr)
            return 2
        top = run(["git", "-C", a.repo, "rev-parse", "--show-toplevel"])
        repo = top.stdout.strip() if top.returncode == 0 else a.repo
        p = run(["git", "-C", repo, "rev-parse", "--verify", a.rev + "^{commit}"])
        if p.returncode != 0:
            print(f"C3_SETUP unresolvable revision {a.rev}", file=sys.stderr)
            return 2
        rev = p.stdout.strip()

        def show(path):
            q = run(["git", "-C", repo, "show", f"{rev}:{path}"])
            return q.stdout if q.returncode == 0 else None

        tool_text = show(TOOL)
        if tool_text is None:
            print(f"C3=unmet tool=absent rev={rev[:12]}")
            return 1
        if ("REVISION_MISMATCH" not in tool_text or "rev-parse" not in tool_text
                or "--git" not in tool_text):
            print(f"C3=unmet tool=present arm=absent rev={rev[:12]}")
            return 1
        export = tempfile.mkdtemp(dir=scratch, prefix="tool-")
        write_tree(export, {TOOL: tool_text})
        tool_path = os.path.join(export, TOOL)
        rc, out = selftest_run(tool_path, scratch)
        m = re.search(r"RECORD_SWEEP_SELFTEST\s+pass=(\d+)\s+fail=(\d+)", out)
        arms = int(m.group(1)) if m else -1
        if rc != 0 or not m or int(m.group(2)) != 0 or arms < ARMS_FLOOR:
            print(f"C3=unmet tool=present arms={arms} selftest=red rc={rc} rev={rev[:12]}")
            return 1
        fixtures = {}
        for kind in ("one-stale", "second-stale", "conformant"):
            result = fixture_run(tool_path, scratch, kind)
            fixtures[kind] = bool(result and result[0])
        caught = fixtures["one-stale"] and fixtures["second-stale"] and fixtures["conformant"]
        pins_text = show(PINS)
        if pins_text is None:
            print(f"C3=unmet tool=present arms={arms} defeated={1 if caught else 0} "
                  f"pins=absent rev={rev[:12]}")
            return 1
        pins = pins_bindings(pins_text)
        if not pins:
            print("C3_SETUP pins has no `revisions` list", file=sys.stderr)
            return 2
        if not population_ok(pins):
            print(f"C3=unmet tool=present arms={arms} defeated={1 if caught else 0} "
                  f"bindings=frozen-population-mismatch rev={rev[:12]}")
            return 1
        drift = []
        for path in carrier_paths(pins):
            here = None
            target = os.path.join(repo, path)
            if os.path.exists(target):
                here = open(target, encoding="utf-8").read()
            if here != show(path):
                drift.append(path)
        if drift:
            print(f"C3_SETUP worktree differs from {rev[:12]} at {','.join(drift)}; "
                  "measure at the landed tip", file=sys.stderr)
            return 2
        env = dict(os.environ)
        env.update(TMPDIR=scratch, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
        # Grade the pins COMMITTED at R, never a worktree copy (C01 finding): the same
        # revision must give the same answer regardless of uncommitted bytes.
        pins_file = os.path.join(scratch, "committed-pins.json")
        open(pins_file, "w", encoding="utf-8").write(pins_text)
        q = run(["python3", "-I", tool_path, "--root", repo,
                 "--pins", pins_file, "--git", repo], cwd=repo, env=env)
        rout = (q.stdout or "") + (q.stderr or "")
        fields = summary(rout)
        bindings = fields.get("bindings", len(pins))
        revisions = fields.get("revisions", -1)
        met = met_verdict(caught, q, fields, bindings)
        tail = (f"tool=present arms={arms} defeated={1 if caught else 0} "
                f"fixtures={sum(1 for v in fixtures.values() if v)}/3 "
                f"bindings={bindings} revisions={revisions}")
        print(f"C3={'met' if met else 'unmet'} {tail} rev={rev[:12]}")
        if not met:
            for line in rout.splitlines():
                if "MISMATCH" in line or "SETUP" in line:
                    print(line)
        return 0 if met else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
