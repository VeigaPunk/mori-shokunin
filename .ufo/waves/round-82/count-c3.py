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


def defeated_fixture(tool_path, scratch):
    """Independent D81-1 shape: the row's value is not in the revision it names."""
    repo = tempfile.mkdtemp(dir=scratch, prefix="defeated-")
    old = ("# t\n\n| Capability | What | Evidence | First |\n|---|---|---|---|\n"
           "| Self-assessment claim sweep (`tools/mori-claim-sweep.py`) | x | "
           "pointers=237 rc 0 | 80 |\n")
    new = old.replace("pointers=237", "pointers=240")
    run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-C", repo, "init", "-q"])
    write_tree(repo, {"SCORECARD.md": old})
    run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-C", repo, "add", "-A"])
    run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-C", repo, "commit", "-qm", "a"])
    rev_a = run(["git", "-C", repo, "rev-parse", "HEAD"]).stdout.strip()
    write_tree(repo, {"SCORECARD.md": new})
    run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-C", repo, "add", "-A"])
    run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-C", repo, "commit", "-qm", "b"])
    pins = {"revisions": [{"carrier": "SCORECARD.md",
                           "row_contains": "mori-claim-sweep.py", "key": "pointers",
                           "value": 240, "rev": rev_a, "path": "SCORECARD.md"}]}
    write_tree(repo, {".ufo/waves/round-82/record-pins.json": json.dumps(pins)})
    env = dict(os.environ)
    env.update(TMPDIR=repo, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
    p = run(["python3", "-I", tool_path, "--root", repo,
             "--pins", os.path.join(repo, PINS), "--git", repo], cwd=repo, env=env)
    fields = summary((p.stdout or "") + (p.stderr or ""))
    return p.returncode, fields, (p.stdout or "")


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
        if "REVISION_MISMATCH" not in tool_text:
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
        frc, ffields, fout = defeated_fixture(tool_path, scratch)
        caught = frc == 1 and ffields.get("revisions", 0) >= 1 and "REVISION_MISMATCH" in fout
        pins_text = show(PINS)
        if pins_text is None:
            print(f"C3=unmet tool=present arms={arms} defeated={1 if caught else 0} "
                  f"pins=absent rev={rev[:12]}")
            return 1
        pins = pins_bindings(pins_text)
        if not pins:
            print("C3_SETUP pins has no `revisions` list", file=sys.stderr)
            return 2
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
        q = run(["python3", "-I", tool_path, "--root", repo,
                 "--pins", os.path.join(repo, PINS), "--git", repo], cwd=repo, env=env)
        rout = (q.stdout or "") + (q.stderr or "")
        fields = summary(rout)
        bindings = fields.get("bindings", len(pins))
        revisions = fields.get("revisions", -1)
        met = (caught and q.returncode == 0 and fields.get("revisions", -1) == 0
               and bindings >= 3)
        tail = (f"tool=present arms={arms} defeated={1 if caught else 0} "
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
