#!/usr/bin/env python3
"""mori round-84 C2 counter (calibration): the revision arm grades every anchor row.

Frozen predicate P-C2 (`.ufo/waves/round-84/contract.md` — this counter, the contract and the
receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-84/count-c2.py R` prints
  `C2=met arm=all-rows defeated=2 fixtures=3/3 bindings=3 revisions=0 arms=44` and exits 0, where
  the tool at R carries the `ALL_ANCHOR_ROWS` rule, two frozen ambiguous fixtures read red under
  the R tool and green under the entering tool (`5adf4337`), the conformant fixture reads green
  under both, the real lane run with the r82 pins prints `revisions=0` rc 0 over exactly the three
  frozen bindings, and the tool's own selftest prints `RECORD_SWEEP_SELFTEST pass=N fail=0` with
  N >= 44.

Rule (frozen): a revision binding's `row_contains` selects EVERY row carrying that string. The
carrier side requires each selected row to state `key=value` on that row (first failing row is
`REVISION_MISMATCH <carrier>:<line> row-value`); the revision side requires each row carrying the
anchor in `git show <rev>:<path>` to carry the token (`REVISION_MISMATCH <carrier>:<line>
rev-bytes`). No anchor row is `row-value` at line 1; a blob with no anchor row is `rev-bytes`.

Usage: count-c2.py <rev> [--repo DIR] [--scratch DIR] | count-c2.py --selftest
Exit 0 met, 1 unmet, 2 setup. Read-only: `git show`/`git archive`-free; fixtures and tool copies
only under --scratch.
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
OLD_REV = "5adf4337b6510dd246b247092c11cbaa97c930d3"
ARMS_FLOOR = 44
MARKER = "ALL_ANCHOR_ROWS"
# Frozen population (r82 amendment A1): the three bindings the real lane must carry.
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
SELFTEST = re.compile(r"RECORD_SWEEP_SELFTEST\s+pass=(\d+)\s+fail=(\d+)")
ROW_A = "| Row A | x | row_tally=19 | 80 |\n"
ROW_B = "| Row A extended | y | row_tally=18 | 80 |\n"
HEAD = "# t\n\n| Row | What | Evidence | First |\n|---|---|---|---|\n"


def run(cmd, cwd=None, env=None, timeout=240):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          env=env, timeout=timeout)


def summary(output):
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
    expected = set()
    for carrier, row, key, value, rev, path in FROZEN:
        expected.add((carrier, row, key, value, path, rev))
    got = set()
    for binding in pins:
        got.add((binding.get("carrier"), binding.get("row_contains"), binding.get("key"),
                 binding.get("value"), binding.get("path"), str(binding.get("rev") or "")))
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


def build_fixture(scratch, kind):
    """Build one fixture git repo. Returns (repo, pins_path, rev_a) or None.

    carrier-ambiguous: carrier and blob at rev A both hold ROW_A + ROW_B; the first-match carrier
      read passes (row 1 states 19) while row 2 states 18.
    rev-ambiguous: the worktree carrier holds ROW_A only; the blob at rev A holds ROW_A + ROW_B,
      so the anchored-occurrence read passes while a second anchor row states 18.
    conformant: one row, value on it, at the bound revision.
    """
    repo = tempfile.mkdtemp(dir=scratch, prefix="fx-" + kind + "-")
    ident = ["-c", "user.name=t", "-c", "user.email=t@t"]
    run(["git"] + ident + ["-C", repo, "init", "-q"])
    if run(["git", "-C", repo, "rev-parse", "--show-toplevel"]).stdout.strip() != repo:
        return None
    if kind == "carrier-ambiguous":
        body_a = HEAD + ROW_A + ROW_B
        body_b = body_a
    elif kind == "rev-ambiguous":
        body_a = HEAD + ROW_A + ROW_B
        body_b = HEAD + ROW_A
    elif kind == "conformant":
        body_a = HEAD + ROW_A
        body_b = body_a
    else:
        return None
    write_tree(repo, {"SCORECARD.md": body_a})
    run(["git"] + ident + ["-C", repo, "add", "-A"])
    run(["git"] + ident + ["-C", repo, "commit", "-qm", "a"])
    rev_a = run(["git", "-C", repo, "rev-parse", "HEAD"]).stdout.strip()
    if body_b != body_a:
        write_tree(repo, {"SCORECARD.md": body_b})
        run(["git"] + ident + ["-C", repo, "add", "-A"])
        run(["git"] + ident + ["-C", repo, "commit", "-qm", "b"])
    binding = {"carrier": "SCORECARD.md", "row_contains": "Row A", "key": "row_tally",
               "value": 19, "rev": rev_a, "path": "SCORECARD.md"}
    pins_path = os.path.join(repo, PINS)
    write_tree(repo, {PINS: json.dumps({"revisions": [binding]})})
    return repo, pins_path, rev_a


def run_tool(tool_path, repo, pins_path, scratch):
    env = dict(os.environ)
    env.update(TMPDIR=scratch, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
    p = run(["python3", "-I", tool_path, "--root", repo, "--pins", pins_path,
             "--git", repo], cwd=repo, env=env)
    out = (p.stdout or "") + (p.stderr or "")
    return p.returncode, summary(out), out


def fixture_verdicts(scratch, new_tool, old_tool, kind):
    """(new_rc, new_fields, new_out, old_rc) for one fixture, or None on setup failure."""
    built = build_fixture(scratch, kind)
    if not built:
        return None
    repo, pins_path, _ = built
    new_rc, new_fields, new_out = run_tool(new_tool, repo, pins_path, scratch)
    old_rc, _, _ = run_tool(old_tool, repo, pins_path, scratch)
    return new_rc, new_fields, new_out, old_rc


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
    cases.append(("arms_floor", ARMS_FLOOR == 44, "floor=%d" % ARMS_FLOOR))
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
    scratch = tempfile.mkdtemp(prefix="count-c2-r84-", dir=base)
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

        def show(path):
            q = run(["git", "-C", repo, "show", "%s:%s" % (rev, path)])
            return q.stdout if q.returncode == 0 else None

        tool_text = show(TOOL)
        if tool_text is None:
            print("C2=unmet tool=absent rev=%s" % rev[:12])
            return 1
        if MARKER not in tool_text or "REVISION_MISMATCH" not in tool_text:
            print("C2=unmet arm=absent rev=%s" % rev[:12])
            return 1
        q = run(["git", "-C", repo, "show", "%s:%s" % (OLD_REV, TOOL)])
        old_text = q.stdout if q.returncode == 0 else None
        if old_text is None:
            print("C2_SETUP entering tool absent at " + OLD_REV[:12], file=sys.stderr)
            return 2
        new_dir = tempfile.mkdtemp(dir=scratch, prefix="tool-new-")
        old_dir = tempfile.mkdtemp(dir=scratch, prefix="tool-old-")
        write_tree(new_dir, {TOOL: tool_text})
        write_tree(old_dir, {TOOL: old_text})
        new_tool = os.path.join(new_dir, TOOL)
        old_tool = os.path.join(old_dir, TOOL)
        rc, out = selftest_run(new_tool, scratch)
        m = SELFTEST.search(out)
        arms = int(m.group(1)) if m else -1
        if rc != 0 or not m or int(m.group(2)) != 0 or arms < ARMS_FLOOR:
            print("C2=unmet arm=all-rows arms=%d selftest=red rc=%d rev=%s"
                  % (arms, rc, rev[:12]))
            return 1
        verdicts = {}
        for kind in ("carrier-ambiguous", "rev-ambiguous", "conformant"):
            verdicts[kind] = fixture_verdicts(scratch, new_tool, old_tool, kind)
        if any(value is None for value in verdicts.values()):
            print("C2_SETUP a fixture could not be built", file=sys.stderr)
            return 2
        fixtures_ok = 0
        defeated = 0
        for kind in ("carrier-ambiguous", "rev-ambiguous"):
            new_rc, new_fields, new_out, old_rc = verdicts[kind]
            new_red = (new_rc == 1 and new_fields.get("revisions", 0) >= 1
                       and "REVISION_MISMATCH" in new_out
                       and ("row-value" in new_out or "rev-bytes" in new_out))
            if new_red and old_rc == 0:
                defeated += 1
                fixtures_ok += 1
        new_rc, new_fields, _, old_rc = verdicts["conformant"]
        if new_rc == 0 and new_fields.get("revisions", -1) == 0 and old_rc == 0:
            fixtures_ok += 1
        pins_text = show(PINS)
        if pins_text is None:
            print("C2=unmet arm=all-rows arms=%d defeated=%d pins=absent rev=%s"
                  % (arms, defeated, rev[:12]))
            return 1
        pins = pins_bindings(pins_text)
        if not pins:
            print("C2_SETUP pins has no `revisions` list", file=sys.stderr)
            return 2
        if not population_ok(pins):
            print("C2=unmet arm=all-rows arms=%d defeated=%d "
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
            print("C2_SETUP worktree differs from %s at %s; measure at the landed tip"
                  % (rev[:12], ",".join(drift)), file=sys.stderr)
            return 2
        env = dict(os.environ)
        env.update(TMPDIR=scratch, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
        pins_file = os.path.join(scratch, "committed-pins.json")
        open(pins_file, "w", encoding="utf-8").write(pins_text)
        q = run(["python3", "-I", new_tool, "--root", repo,
                 "--pins", pins_file, "--git", repo], cwd=repo, env=env)
        rout = (q.stdout or "") + (q.stderr or "")
        fields = summary(rout)
        bindings = fields.get("bindings", len(pins))
        revisions = fields.get("revisions", -1)
        met = (fixtures_ok == 3 and defeated == 2 and q.returncode == 0
               and revisions == 0 and bindings == 3)
        tail = ("arm=all-rows defeated=%d fixtures=%d/3 bindings=%d revisions=%d arms=%d"
                % (defeated, fixtures_ok, bindings, revisions, arms))
        print("C2=%s %s rev=%s" % ("met" if met else "unmet", tail, rev[:12]))
        if not met:
            for line in rout.splitlines():
                if "MISMATCH" in line or "SETUP" in line:
                    print(line)
            for kind, value in verdicts.items():
                print("FIXTURE %s new_rc=%s old_rc=%s" % (kind, value[0], value[3]))
        return 0 if met else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
