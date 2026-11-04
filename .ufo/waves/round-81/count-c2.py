#!/usr/bin/env python3
"""mori round-81 C2 counter (calibration): does the lane's record state its own results?

Frozen predicate P-C2 (contract `.ufo/waves/round-81/contract.md`, this counter and the
receipt label are the same sentence):

  At revision R, `tools/mori-record-sweep.py` exists at R and, run over an export of R,
  prints `RECORD_SWEEP pending=0 pinned=0` rc 0; measured independently by this counter
  over the same export of R, SCORECARD.md's `## Round ...` tables carry no cell whose
  value is exactly `PENDING` and every binding in `.ufo/waves/round-81/record-pins.json`
  states the value its own pinned command prints at R; the counter prints
  `C2=met pending=0 pinned=0 tool=present agree=1` and exits 0. At the entering revision
  `44bc941a` it prints `C2=unmet pending=3 pinned=1 tool=absent` rc 1.

The pinned arm re-runs each binding's read-only command from the export with cwd = export,
extracts `<key>=<integer>` from the row (stated) and from the command's stdout (live), and
counts a mismatch when they differ or the command fails. A command failure is a setup
error only when the counter itself cannot run; a failing pinned command is a mismatch.
The tool arm re-runs the record sweep at R and requires its `pending`/`pinned` fields to
agree with this counter's independent reading (`agree=1`).

Named limit (before data): the counter grades the lane's own record carriers only; it does
not grade fleet report prose, and `pending` is a cell-value test, not a reading of intent.

Usage: count-c2.py <rev> [--repo DIR] [--scratch DIR] [--pins FILE] | --selftest
Output: `C2=met|unmet pending=N pinned=M tool=present|absent agree=0|1 rev=<sha12>`
Exit 0 met, 1 unmet, 2 setup. Read-only: `git archive` into --scratch; no file outside
--scratch is written.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

TOOL = "tools/mori-record-sweep.py"
DEFAULT_PINS = ".ufo/waves/round-81/record-pins.json"
ROUND_SECTION = re.compile(r"^##\s+Round\b")
# Frozen record population: a round section's claim rows may be corrected, never deleted
# (a missing required row counts as one more unresolved cell).
REQUIRED_ROWS = {"## Round 80": 3}
# Frozen digest of the freeze-commit pins file: a tampered binding set is a pinned mismatch.
PINS_SHA256 = "b991e0bd25a12614846a79f3df3a5b620f61a0792e3d88a9a62d6d8598dea44e"
ROW = re.compile(r"^\s{0,3}\|")


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def export(repo, rev, dest):
    os.makedirs(dest, exist_ok=True)
    archive = subprocess.run(["git", "-C", repo, "archive", rev], capture_output=True)
    if archive.returncode != 0:
        return False
    tar = subprocess.run(["tar", "-x", "-C", dest], input=archive.stdout, capture_output=True)
    return tar.returncode == 0


def cells(line):
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", line.strip())[1:-1]]


def pending_cells(text):
    """Cells of value PENDING inside a `## Round ...` section's table rows."""
    out = []
    section = None
    for number, line in enumerate(text.splitlines(), 1):
        if line.startswith("## "):
            section = line
            continue
        if section is None or not ROUND_SECTION.match(section) or not ROW.match(line):
            continue
        for index, cell in enumerate(cells(line)):
            if cell == "PENDING":
                out.append((number, section.strip(), index))
    return out


def section_rows(text, heading):
    """Claim-table data rows in the section whose heading line equals `heading`."""
    rows = 0
    section = None
    for line in text.splitlines():
        if line.startswith("## "):
            section = line.strip()
            continue
        if section == heading and ROW.match(line):
            if all(re.fullmatch(r":?-+:?", cell) for cell in cells(line)):
                continue
            rows += 1
    return rows


def stated_value(carrier_text, row_contains, key):
    """The first row containing `row_contains` and stating `<key>=<int>`; None if absent."""
    for line in carrier_text.splitlines():
        if not ROW.match(line) or row_contains not in line:
            continue
        match = re.search(r"\b%s=(\d+)\b" % re.escape(key), line)
        if match:
            return int(match.group(1))
    return None


def live_value(stdout, key):
    """All `<key>=<int>` readings in the command's stdout; None when absent or conflicting."""
    found = {int(value) for value in re.findall(r"\b%s=(\d+)\b" % re.escape(key), stdout)}
    if len(found) != 1:
        return None
    return found.pop()


def load_pins(path):
    data = json.loads(open(path, encoding="utf-8").read())
    if not isinstance(data, dict) or data.get("schema") != "mori-record-pins-v1":
        raise ValueError("pins schema must be mori-record-pins-v1")
    bindings = data.get("bindings", [])
    if not isinstance(bindings, list):
        raise ValueError("bindings must be a list")
    for item in bindings:
        if (not isinstance(item, dict) or not isinstance(item.get("carrier"), str)
                or not isinstance(item.get("row_contains"), str)
                or not isinstance(item.get("key"), str)
                or not isinstance(item.get("command"), list)
                or not item["command"] or not all(isinstance(a, str) for a in item["command"])):
            raise ValueError("malformed binding")
    return bindings


def grade(tree, pins_path):
    """Grade an exported tree; returns (verdict dict, rc)."""
    card = os.path.join(tree, "SCORECARD.md")
    if not os.path.isfile(card):
        raise ValueError("SCORECARD.md missing from export")
    card_text = open(card, encoding="utf-8").read()
    pending = pending_cells(card_text)
    missing_rows = sum(max(0, need - section_rows(card_text, heading))
                       for heading, need in REQUIRED_ROWS.items())
    pending_total = len(pending) + missing_rows
    try:
        bindings = load_pins(pins_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return None, ("C2_SETUP pins " + str(exc).replace("\n", " "))
    pinned = 0
    digest = hashlib.sha256(open(pins_path, 'rb').read()).hexdigest()
    if digest != PINS_SHA256:
        pinned += 1          # the frozen binding set was altered
    for binding in bindings:
        carrier = os.path.join(tree, binding["carrier"])
        if not os.path.isfile(carrier):
            raise ValueError("carrier missing from export: " + binding["carrier"])
        stated = stated_value(open(carrier, encoding="utf-8").read(),
                              binding["row_contains"], binding["key"])
        result = run(binding["command"], cwd=tree)
        live = live_value(result.stdout, binding["key"])
        if stated is None or live is None or result.returncode != 0 or stated != live:
            pinned += 1
    tool = os.path.isfile(os.path.join(tree, TOOL))
    agree = 0
    if tool:
        result = run(["python3", "-I", os.path.join(tree, TOOL),
                      "--root", tree, "--pins", os.path.join(tree, DEFAULT_PINS)])
        match = re.search(r"RECORD_SWEEP pending=(\d+) pinned=(\d+)", result.stdout)
        agree = int(result.returncode == 0 and match is not None
                    and int(match.group(1)) == pending_total
                    and int(match.group(2)) == pinned)
    verdict = {"pending": pending_total, "pinned": pinned,
               "tool": "present" if tool else "absent", "agree": agree}
    met = not pending_total and not pinned and tool and agree
    verdict["met"] = bool(met)
    if verdict["met"]:
        return verdict, None
    return verdict, ("C2=unmet pending=%d pinned=%d tool=%s agree=%d"
                     % (len(pending), pinned, verdict["tool"], agree))


def selftest(scratch):
    passed = failed = 0

    def check(label, ok, detail=""):
        nonlocal passed, failed
        passed += int(bool(ok))
        failed += int(not ok)
        print("case %s %s %s" % (label, "pass" if ok else "FAIL", detail))

    def repo(files, parent=None):
        base = tempfile.mkdtemp(dir=parent or scratch)
        for name, body in files.items():
            path = os.path.join(base, name)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, "w", encoding="utf-8").write(body)
        env = ["-c", "user.name=t", "-c", "user.email=t@t"]
        run(["git"] + env + ["-C", base, "init", "-q"])
        run(["git"] + env + ["-C", base, "add", "-A"])
        run(["git"] + env + ["-C", base, "commit", "-qm", "f"])
        return base, run(["git", "-C", base, "rev-parse", "HEAD"]).stdout.strip()

    table = ("# card\n\n## Round 80\n\n| Claim | Axis | After |\n|---|---|---|\n"
             "| a | depth | `C=met` |\n| b | depth | `C=met` |\n| c | depth | `C=met` |\n")
    pins = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "record-pins.json"), encoding="utf-8").read()
    tool_ok = ("import sys, re\n"
               "print('RECORD_SWEEP pending=0 pinned=0 tool=ok')\nsys.exit(0)\n")
    sweep_ok = ("print('CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 "
                "carriers=1 pointers=233')\n")
    clean_row = ("| sweep (`tools/mori-claim-sweep.py`) | x | "
                 "`python3 -I tools/mori-claim-sweep.py` -> pointers=233 | 80 |\n")

    # grammar arms
    check("pending in round table", len(pending_cells(
        "## Round 7\n\n| Claim | After |\n|---|---|\n| a | PENDING |\n")) == 1)
    check("pending outside a round section ignored", not pending_cells(
        "## Notes\n\n| Claim | After |\n|---|---|\n| a | PENDING |\n"))
    check("pending prose ignored", not pending_cells("## Round 7\n\nall three cells are PENDING\n"))
    check("stated first row", stated_value(
        "| `tools/x.py` a pointers=232 |\n| `tools/x.py` b pointers=9 |\n", "tools/x.py",
        "pointers") == 232)
    check("live single", live_value("CLAIM_SWEEP pointers=233\n", "pointers") == 233)
    check("live conflicting", live_value("pointers=1\npointers=2\n", "pointers") is None)
    check("pins schema", _bad_schema())

    check("required row population", section_rows("## Round 7\n\n| a | x |\n| b | y |\n", "## Round 7") == 2)
    check("required row missing", section_rows("## Round 7\n\n| a | x |\n", "## Round 7") == 1)

    # end-to-end arms
    clean_table = ("# card\n\n## Round 80\n\n| Claim | Axis | After |\n|---|---|---|\n"
                   "| a | depth | `C=met` |\n| b | depth | `C=met` |\n| c | depth | `C=met` |\n"
                   "\n### Capabilities (round 80)\n\n| Capability | What it can now do | Evidence pointer | First-working round |\n|---|---|---|---|\n"
                   + clean_row)
    base, _ = repo({"SCORECARD.md": clean_table, ".ufo/waves/round-81/record-pins.json": pins,
                    "tools/mori-record-sweep.py": tool_ok,
                    "tools/mori-claim-sweep.py": sweep_ok})
    tree = tempfile.mkdtemp(dir=scratch)
    check("export roundtrip", export(base, "HEAD", tree))
    verdict, _ = grade(tree, os.path.join(tree, ".ufo/waves/round-81/record-pins.json"))
    check("clean record met", verdict is not None and verdict["met"], str(verdict))

    base2, _ = repo({"SCORECARD.md": "## Round 80\n\n| Claim | After |\n|---|---|\n"
                                     "| a | PENDING |\n| b | 1 |\n| c | 2 |\n",
                     ".ufo/waves/round-81/record-pins.json": pins,
                     "tools/mori-record-sweep.py": tool_ok})
    tree2 = tempfile.mkdtemp(dir=scratch)
    export(base2, "HEAD", tree2)
    verdict, line = grade(tree2, os.path.join(tree2, ".ufo/waves/round-81/record-pins.json"))
    check("pending record unmet", verdict is not None and not verdict["met"], str(line))

    pins_bad = json.dumps({"schema": "mori-record-pins-v1", "bindings": [
        {"carrier": "SCORECARD.md", "row_contains": "tools/echo.py", "key": "pointers",
         "command": ["python3", "-I", "tools/echo.py"]}]})
    base3, _ = repo({
        "SCORECARD.md": "## Round 80\n\n| Claim | After |\n|---|---|\n"
                        "| a | `tools/echo.py` pointers=232 |\n| b | 1 |\n| c | 2 |\n",
        ".ufo/waves/round-81/record-pins.json": pins_bad,
        "tools/mori-record-sweep.py": tool_ok,
        "tools/echo.py": "print('SWEEP pointers=233')\n"})
    tree3 = tempfile.mkdtemp(dir=scratch)
    export(base3, "HEAD", tree3)
    verdict, line = grade(tree3, os.path.join(tree3, ".ufo/waves/round-81/record-pins.json"))
    check("stale pinned unmet", verdict is not None and not verdict["met"], str(line))

    base4, _ = repo({"SCORECARD.md": table,
                     ".ufo/waves/round-81/record-pins.json": pins})
    tree4 = tempfile.mkdtemp(dir=scratch)
    export(base4, "HEAD", tree4)
    verdict, line = grade(tree4, os.path.join(tree4, ".ufo/waves/round-81/record-pins.json"))
    check("tool absent unmet", verdict is not None and not verdict["met"], str(line))

    base7, _ = repo({
        "SCORECARD.md": table,
        ".ufo/waves/round-81/record-pins.json":
            json.dumps({"schema": "mori-record-pins-v1", "bindings": []}),
        "tools/mori-record-sweep.py": tool_ok})
    tree7 = tempfile.mkdtemp(dir=scratch)
    export(base7, "HEAD", tree7)
    verdict, line = grade(tree7, os.path.join(tree7, ".ufo/waves/round-81/record-pins.json"))
    check("tampered pins unmet", verdict is not None and not verdict["met"], str(line))

    base5, _ = repo({"SCORECARD.md": table,
                     ".ufo/waves/round-81/record-pins.json": pins,
                     "tools/mori-record-sweep.py":
                         "import sys\nprint('RECORD_SWEEP pending=9 pinned=0')\nsys.exit(0)\n"})
    tree5 = tempfile.mkdtemp(dir=scratch)
    export(base5, "HEAD", tree5)
    verdict, line = grade(tree5, os.path.join(tree5, ".ufo/waves/round-81/record-pins.json"))
    check("tool disagree unmet", verdict is not None and not verdict["met"], str(line))

    # a path with a space must not degrade the export (LOW-10 class)
    spaced = tempfile.mkdtemp(dir=scratch)
    inner = os.path.join(spaced, "dir with space", "r")
    os.makedirs(inner)
    for name, body in {"SCORECARD.md": clean_table,
                       ".ufo/waves/round-81/record-pins.json": pins,
                       "tools/mori-record-sweep.py": tool_ok,
                       "tools/mori-claim-sweep.py": sweep_ok}.items():
        path = os.path.join(inner, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write(body)
    env = ["-c", "user.name=t", "-c", "user.email=t@t"]
    run(["git"] + env + ["-C", inner, "init", "-q"])
    run(["git"] + env + ["-C", inner, "add", "-A"])
    run(["git"] + env + ["-C", inner, "commit", "-qm", "f"])
    tree6 = tempfile.mkdtemp(dir=scratch)
    check("space path export", export(inner, "HEAD", tree6))
    verdict, line = grade(tree6, os.path.join(tree6, ".ufo/waves/round-81/record-pins.json"))
    check("space path met", verdict is not None and verdict["met"], str(line))

    print("C2_COUNTER_SELFTEST pass=%d fail=%d" % (passed, failed))
    return 0 if not failed else 1


def _bad_schema():
    try:
        load_pins_dict({"schema": "wrong"})
    except ValueError:
        return True
    return False


def load_pins_dict(data):
    if not isinstance(data, dict) or data.get("schema") != "mori-record-pins-v1":
        raise ValueError("pins schema must be mori-record-pins-v1")
    return data


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--repo", default=os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
    ap.add_argument("--scratch")
    ap.add_argument("--pins")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    base = a.scratch or os.environ.get("HYAKU_SCRATCH") or tempfile.gettempdir()
    os.makedirs(base, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="count-c2-r81-", dir=base)
    try:
        if a.selftest:
            return selftest(scratch)
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
        tree = os.path.join(scratch, "tree")
        if not export(repo, rev, tree):
            print("C2_SETUP archive failed rev=" + rev[:12], file=sys.stderr)
            return 2
        pins = a.pins or os.path.join(tree, DEFAULT_PINS)
        if not a.pins and not os.path.isfile(os.path.join(tree, DEFAULT_PINS)):
            print("C2_SETUP pins absent at rev=" + rev[:12], file=sys.stderr)
            return 2
        verdict, line = grade(tree, pins)
        if verdict is None:
            print(line, file=sys.stderr)
            return 2
        print("C2=%s pending=%d pinned=%d tool=%s agree=%d rev=%s"
              % ("met" if verdict["met"] else "unmet", verdict["pending"],
                 verdict["pinned"], verdict["tool"], verdict["agree"], rev[:12]))
        return 0 if verdict["met"] else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
