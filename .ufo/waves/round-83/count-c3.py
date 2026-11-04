#!/usr/bin/env python3
"""mori round-83 C3 counter (depth): anchored occurrence in the revision arm.

Frozen predicate P-C3 (`.ufo/waves/round-83/contract.md` — this counter, the contract and the
receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-83/count-c3.py R` prints
  `C3=met arm=anchored defeated=2 fixtures=2/2 bindings=3 revisions=0 arms=40` and exits 0,
  where `R:tools/mori-record-sweep.py` contains `ANCHORED_OCCURRENCE` and `REVISION_MISMATCH`;
  its own `--selftest` at R is green with `pass=N`, N >= 40; the `elsewhere` fixture (the value
  occurs in the bound path's bytes only on a line without the binding's `row_contains`) is
  caught (`rc 1`, `revisions>=1`, `REVISION_MISMATCH ... rev-bytes`) and the `conformant`
  fixture (value on the anchored row) is green (`rc 0`, `revisions=0`); and the real lane run at
  R with `.ufo/waves/round-82/record-pins.json` is green with `bindings>=3`, `revisions=0`.

The real run reads carriers from the lane worktree through `--root` and revisions through
`--git`, so the counter requires every carrier named by the pins file to be byte-identical at R
and in the worktree (otherwise it is a setup error: measure at the landed tip).

Usage: count-c3.py <rev> [--repo DIR] [--scratch DIR] | count-c3.py --selftest
Exit 0 met, 1 unmet, 2 setup. Read-only: `git show`; files only under --scratch.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

TOOL = "tools/mori-record-sweep.py"
PINS = ".ufo/waves/round-82/record-pins.json"
ARMS_FLOOR = 40
MARKER = "ANCHORED_OCCURRENCE"
# Frozen population (r82 contract amendment A1): the three bindings the real lane must carry.
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
            fields = dict((key, int(value)) for key, value in COUNT.findall(m.group(1)))
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
    expected = set()
    for carrier, row, key, value, rev, path in FROZEN:
        expected.add((carrier, row, key, value, path, rev))
    got = set()
    for binding in pins:
        key = (binding.get("carrier"), binding.get("row_contains"), binding.get("key"),
               binding.get("value"), binding.get("path"))
        rev = str(binding.get("rev") or "")
        got.add(key + (rev,))
    return len(pins) == len(FROZEN) and got == expected


def carrier_paths(pins):
    paths = set(binding.get("carrier") for binding in pins if binding.get("carrier"))
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
    """Fixtures for the anchored occurrence test.

    `elsewhere`: the carrier row states `row_tally=19`, but the bound path's anchored row says
    `row_tally=18` and `row_tally=19` occurs only on an unrelated note row. The unanchored
    occurrence test passes it (the r82 bug); the anchored one must report `rev-bytes`.
    `conformant`: the value sits on the anchored row at the bound revision.
    """
    if kind == "elsewhere":
        rows_a = ("# t\n\n| Row | What | Evidence | First |\n|---|---|---|---|\n"
                  "| Row A | x | row_tally=18 | 80 |\n"
                  "| Note | y | row_tally=19 | 80 |\n")
        rows_b = ("# t\n\n| Row | What | Evidence | First |\n|---|---|---|---|\n"
                  "| Row A | x | row_tally=19 | 80 |\n"
                  "| Note | y | row_tally=19 | 80 |\n")
        bindings = [{"carrier": "SCORECARD.md", "row_contains": "Row A", "key": "row_tally",
                     "value": 19, "rev": "A", "path": "SCORECARD.md"}]
        expect = ("caught", 1)
    else:                                            # conformant
        rows_a = ("# t\n\n| Row | What | Evidence | First |\n|---|---|---|---|\n"
                  "| Row A | x | row_tally=19 | 80 |\n")
        rows_b = rows_a
        bindings = [{"carrier": "SCORECARD.md", "row_contains": "Row A", "key": "row_tally",
                     "value": 19, "rev": "A", "path": "SCORECARD.md"}]
        expect = ("green", 0)
    repo = tempfile.mkdtemp(dir=scratch, prefix="fx-" + kind + "-")
    env = ["-c", "user.name=t", "-c", "user.email=t@t"]
    run(["git"] + env + ["-C", repo, "init", "-q"])
    if run(["git", "-C", repo, "rev-parse", "--show-toplevel"]).stdout.strip() != repo:
        return None
    write_tree(repo, {"SCORECARD.md": rows_a})
    run(["git"] + env + ["-C", repo, "add", "-A"])
    run(["git"] + env + ["-C", repo, "commit", "-qm", "a"])
    rev_a = run(["git", "-C", repo, "rev-parse", "HEAD"]).stdout.strip()
    write_tree(repo, {"SCORECARD.md": rows_b})
    run(["git"] + env + ["-C", repo, "add", "-A"])
    run(["git"] + env + ["-C", repo, "commit", "-qm", "b"])
    pins = {"revisions": [dict(binding, rev=rev_a) for binding in bindings]}
    write_tree(repo, {PINS: json.dumps(pins)})
    penv = dict(os.environ)
    penv.update(TMPDIR=repo, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
    p = run(["python3", "-I", tool_path, "--root", repo, "--pins",
             os.path.join(repo, PINS), "--git", repo], cwd=repo, env=penv)
    out = (p.stdout or "") + (p.stderr or "")
    fields = summary(out)
    if expect[0] == "caught":
        ok = (p.returncode == 1 and fields.get("revisions", 0) >= expect[1]
              and "REVISION_MISMATCH" in out and "rev-bytes" in out)
    else:
        ok = p.returncode == 0 and fields.get("revisions", -1) == 0
    return ok, p.returncode, fields, out


def selfcheck(scratch):
    cases = []
    fields = summary("noise\nRECORD_SWEEP pending=0 pinned=0 revisions=2 bindings=5\n")
    cases.append(("summary_parse", fields.get("revisions") == 2
                  and fields.get("bindings") == 5, str(fields)))
    revs = pins_bindings('{"revisions":[{"carrier":"A","rev":"x","path":"A","key":"k",'
                         '"value":1,"row_contains":"r"}]}')
    cases.append(("pins_schema", bool(revs) and carrier_paths(revs) == ["A"], str(revs)))
    cases.append(("pins_absent_list", pins_bindings('{"bindings":[]}') is None,
                  "no revisions key"))
    cases.append(("arms_floor", ARMS_FLOOR == 40, "floor=%d" % ARMS_FLOOR))
    cases.append(("marker_literal", MARKER in open(os.path.abspath(__file__)).read(),
                  "marker=%s" % MARKER))
    frozen = [{"carrier": c, "row_contains": r, "key": k, "value": v, "rev": rv, "path": pp}
              for c, r, k, v, rv, pp in FROZEN]
    cases.append(("population_frozen_ok", population_ok(frozen), "as frozen"))
    cases.append(("population_triplicate_unmet",
                  not population_ok(frozen + [dict(frozen[0]), dict(frozen[0])]),
                  "bindings=%d" % (len(frozen) + 2)))
    cases.append(("population_subset_unmet", not population_ok(frozen[:1]), "one binding"))
    cases.append(("population_rev_drift_unmet",
                  not population_ok([dict(frozen[0], rev="0" * 40)] + frozen[1:]),
                  "wrong rev"))
    ok = sum(1 for _, good, _ in cases if good)
    for label, good, line in cases:
        print("%s %s %s" % ("PASS" if good else "FAIL", label, line))
    print("C3_COUNTER_SELFTEST pass=%d fail=%d" % (ok, len(cases) - ok))
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
    scratch = tempfile.mkdtemp(prefix="count-c3-r83-", dir=base)
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
            print("C3_SETUP unresolvable revision " + a.rev, file=sys.stderr)
            return 2
        rev = p.stdout.strip()

        def show(path):
            q = run(["git", "-C", repo, "show", "%s:%s" % (rev, path)])
            return q.stdout if q.returncode == 0 else None

        tool_text = show(TOOL)
        if tool_text is None:
            print("C3=unmet tool=absent rev=%s" % rev[:12])
            return 1
        if (MARKER not in tool_text or "REVISION_MISMATCH" not in tool_text
                or "rev-parse" not in tool_text or "--git" not in tool_text):
            print("C3=unmet arm=absent rev=%s" % rev[:12])
            return 1
        export = tempfile.mkdtemp(dir=scratch, prefix="tool-")
        write_tree(export, {TOOL: tool_text})
        tool_path = os.path.join(export, TOOL)
        rc, out = selftest_run(tool_path, scratch)
        m = re.search(r"RECORD_SWEEP_SELFTEST\s+pass=(\d+)\s+fail=(\d+)", out)
        arms = int(m.group(1)) if m else -1
        if rc != 0 or not m or int(m.group(2)) != 0 or arms < ARMS_FLOOR:
            print("C3=unmet arm=anchored arms=%d selftest=red rc=%d rev=%s"
                  % (arms, rc, rev[:12]))
            return 1
        fixtures = {}
        for kind in ("elsewhere", "conformant"):
            result = fixture_run(tool_path, scratch, kind)
            fixtures[kind] = bool(result and result[0])
        defeated = 2 if all(fixtures.values()) else sum(1 for v in fixtures.values() if v)
        pins_text = show(PINS)
        if pins_text is None:
            print("C3=unmet arm=anchored arms=%d defeated=%d pins=absent rev=%s"
                  % (arms, defeated, rev[:12]))
            return 1
        pins = pins_bindings(pins_text)
        if not pins:
            print("C3_SETUP pins has no `revisions` list", file=sys.stderr)
            return 2
        if not population_ok(pins):
            print("C3=unmet arm=anchored arms=%d defeated=%d "
                  "bindings=frozen-population-mismatch rev=%s"
                  % (arms, defeated, rev[:12]))
            return 1
        drift = []
        for path in carrier_paths(pins):
            target = os.path.join(repo, path)
            here = open(target, encoding="utf-8").read() if os.path.exists(target) else None
            if here != show(path):
                drift.append(path)
        if drift:
            print("C3_SETUP worktree differs from %s at %s; measure at the landed tip"
                  % (rev[:12], ",".join(drift)), file=sys.stderr)
            return 2
        env = dict(os.environ)
        env.update(TMPDIR=scratch, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
        pins_file = os.path.join(scratch, "committed-pins.json")
        open(pins_file, "w", encoding="utf-8").write(pins_text)
        q = run(["python3", "-I", tool_path, "--root", repo,
                 "--pins", pins_file, "--git", repo], cwd=repo, env=env)
        rout = (q.stdout or "") + (q.stderr or "")
        fields = summary(rout)
        bindings = fields.get("bindings", len(pins))
        revisions = fields.get("revisions", -1)
        met = (all(fixtures.values()) and q.returncode == 0
               and fields.get("revisions", -1) == 0 and bindings >= 3)
        tail = ("arm=anchored defeated=%d fixtures=%d/2 bindings=%d revisions=%d arms=%d"
                % (defeated, sum(1 for v in fixtures.values() if v), bindings, revisions, arms))
        print("C3=%s %s rev=%s" % ("met" if met else "unmet", tail, rev[:12]))
        if not met:
            for line in rout.splitlines():
                if "MISMATCH" in line or "SETUP" in line:
                    print(line)
        return 0 if met else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
