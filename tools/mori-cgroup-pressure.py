#!/usr/bin/env python3
"""Read-only per-cgroup pressure (PSI) survey for cpu, memory, io and irq.

Round 62 (FR12 remainder: cgroup-scoped CPU/IO/IRQ pressure). One-shot read
of `<root>/<group>/<resource>.pressure` for a named cgroup, plus the group's
`cgroup.pressure` accounting switch. Grounded in the pinned v7.3 sources:
`psi_show()` emits the `full` line only (`only_full`) for IRQ
(psi.c:1285-1288), skips CPU `full` only at the system level
(psi.c:1292-1294, `group == &psi_system`), and per-cgroup PSI accounting can
be disabled per cgroup via `cgroup.pressure` = 0, non-hierarchically
(cgroup-v2.rst:1066-1074) — so zeros are never evidence of no stall.

Detection and report only: the tool opens files read-only, writes nothing to
cgroupfs or /proc, registers no PSI trigger, and never infers a cause from an
unavailable state (kernel/boot diagnosis is tsukuroi-owned). It is NOT a
census surface: no SURFACE row, no census finding id, no baseline re-pin.
Thresholds are labeled local and not calibrated (FR8 stays open).

Output: one JSON object (schema: mori-cgroup-pressure-v1) followed by one
`MORI_CGROUP_PRESSURE:` verdict line for receipts. Exit 0 ok/high-guarded
(as mori-pressure-v1), 1 high, 2 partial/unavailable.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SCHEMA = "mori-cgroup-pressure-v1"
CASES_SCHEMA = "mori-cgroup-pressure-cases-v1"
SELFTEST_PREFIX = "MORI_CGROUP_PRESSURE_SELFTEST"

RESOURCE_NAMES: Tuple[str, ...] = ("cpu", "memory", "io", "irq")
# irq.pressure exists per cgroup but emits only the `full` line (psi.c:1285-1288).
FULL_ONLY: Dict[str, bool] = {"irq": True}
DEFAULT_ROOT = "/sys/fs/cgroup"
DEFAULT_GROUP = "user.slice"
DEFAULT_WARN_AVG10 = 10.0

STATE_OK = "ok"
STATE_ABSENT = "absent"
STATE_UNREADABLE = "unreadable"
STATE_MALFORMED = "malformed"
UNAVAILABLE_STATES = frozenset({STATE_ABSENT, STATE_UNREADABLE})

VERDICT_OK = "PRESSURE_OK"
VERDICT_HIGH = "PRESSURE_HIGH"
VERDICT_PARTIAL = "PRESSURE_PARTIAL"
VERDICT_UNAVAILABLE = "PRESSURE_UNAVAILABLE"
RC_OK = 0
RC_HIGH = 1
RC_PARTIAL = 2
RC_UNAVAILABLE = 2

LINE_RE = re.compile(
    r"^(some|full) avg10=(\d+)\.(\d\d) avg60=(\d+)\.(\d\d) "
    r"avg300=(\d+)\.(\d\d) total=(\d+)$"
)


def _parse_resource(name: str, text: str) -> Tuple[str, Optional[Dict[str, Any]], Optional[Dict[str, Any]], List[str]]:
    """Parse one pressure file body into (state, some, full, notes)."""
    notes: List[str] = []
    kinds: Dict[str, Dict[str, Any]] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = LINE_RE.match(line)
        if not m:
            return STATE_MALFORMED, None, None, [f"{name}: malformed line {line[:40]!r}"]
        kind = m.group(1)
        if kind in kinds:
            return STATE_MALFORMED, None, None, [f"{name}: duplicate {kind} line"]
        kinds[kind] = {
            "avg10": float(f"{m.group(2)}.{m.group(3)}"),
            "avg60": float(f"{m.group(4)}.{m.group(5)}"),
            "avg300": float(f"{m.group(6)}.{m.group(7)}"),
            "total": int(m.group(8)),
        }
    full_only = FULL_ONLY.get(name, False)
    if full_only:
        if "full" not in kinds:
            return STATE_MALFORMED, None, None, [f"{name}: full-only resource missing its full line"]
        if "some" in kinds:
            return STATE_MALFORMED, None, None, [f"{name}: full-only resource carries a some line"]
        return STATE_OK, None, kinds["full"], notes
    if "some" not in kinds:
        return STATE_MALFORMED, None, None, [f"{name}: missing some line"]
    return STATE_OK, kinds.get("some"), kinds.get("full"), notes


def _read_resource(name: str, path: str) -> Tuple[str, Optional[str], Optional[str]]:
    """Read one pressure file. Returns (state, text, reason)."""
    try:
        with open(path, "r") as fh:
            return STATE_OK, fh.read(), None
    except FileNotFoundError:
        return STATE_ABSENT, None, "enoent"
    except IsADirectoryError:
        return STATE_UNREADABLE, None, "eisdir"
    except OSError as exc:
        return STATE_UNREADABLE, None, f"errno{exc.errno}"


def _resource_payload(name: str, state: str, some: Optional[Dict[str, Any]],
                      full: Optional[Dict[str, Any]], notes: List[str],
                      reason: Optional[str]) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"resource": name, "state": state}
    if some is not None:
        payload["some"] = some
    else:
        payload["some"] = None
    payload["full"] = full
    if reason:
        payload["reason"] = reason
    if notes:
        payload["notes"] = notes
    return payload


def _read_accounting_switch(group_dir: str) -> Dict[str, Any]:
    """Read `<group>/cgroup.pressure` (the per-cgroup PSI accounting switch)."""
    path = os.path.join(group_dir, "cgroup.pressure")
    try:
        with open(path, "r") as fh:
            text = fh.read().strip()
    except FileNotFoundError:
        return {"state": STATE_ABSENT, "value": None}
    except OSError as exc:
        return {"state": STATE_UNREADABLE, "value": None, "reason": f"errno{exc.errno}"}
    if text in ("0", "1"):
        return {"state": STATE_OK, "value": text}
    return {"state": STATE_MALFORMED, "value": None}


def evaluate(root: str, group: str, warn_avg10: float,
             resources: Tuple[str, ...] = RESOURCE_NAMES) -> Tuple[Dict[str, Any], int]:
    if not math.isfinite(warn_avg10) or warn_avg10 < 0:
        raise ValueError("warn-avg10 must be a finite number >= 0")
    group_dir = os.path.join(root, group)
    group_present = os.path.isdir(group_dir)
    out_resources: Dict[str, Dict[str, Any]] = {}
    ok_count = absent_count = unreadable_count = malformed_count = 0
    high_names: List[str] = []
    findings: List[Dict[str, Any]] = []
    for name in resources:
        state, text, reason = _read_resource(name, os.path.join(group_dir, f"{name}.pressure"))
        if state == STATE_OK:
            state, some, full, notes = _parse_resource(name, text or "")
            reason = None
        else:
            some = full = None
            notes = []
        if state == STATE_OK:
            ok_count += 1
            if some and some["avg10"] >= warn_avg10:
                high_names.append(name)
                findings.append({
                    "kind": "PRESSURE_HIGH", "resource": name,
                    "avg10": some["avg10"], "threshold": warn_avg10,
                    "threshold_label": "local, not calibrated",
                })
        elif state == STATE_ABSENT:
            absent_count += 1
        elif state == STATE_UNREADABLE:
            unreadable_count += 1
        elif state == STATE_MALFORMED:
            malformed_count += 1
        out_resources[name] = _resource_payload(name, state, some, full, notes, reason)

    switch = _read_accounting_switch(group_dir)
    if switch.get("value") == "0":
        findings.append({
            "kind": "PSI_ACCOUNTING_DISABLED", "resource": "cgroup.pressure",
            "note": "per-cgroup PSI accounting is disabled (non-hierarchical); "
                    "zero or non-advancing totals are not evidence of no stall",
        })
    elif switch.get("state") == STATE_MALFORMED:
        findings.append({"kind": "PSI_SWITCH_MALFORMED", "resource": "cgroup.pressure"})

    if ok_count == 0:
        verdict = VERDICT_UNAVAILABLE
    elif high_names:
        verdict = VERDICT_HIGH
    elif absent_count or unreadable_count or malformed_count:
        verdict = VERDICT_PARTIAL
    else:
        verdict = VERDICT_OK

    payload = {
        "schema": SCHEMA,
        "root": root,
        "group": group,
        "group_present": group_present,
        "psi_accounting": switch,
        "resources": out_resources,
        "verdict": verdict,
        "findings": findings,
        "local_threshold": {
            "warn_avg10": warn_avg10,
            "label": "local, not calibrated (FR8 open)",
        },
        "read_only": True,
    }
    rc = RC_HIGH if verdict == VERDICT_HIGH else RC_OK if verdict == VERDICT_OK else RC_PARTIAL
    return payload, rc


def summary_line(payload: Dict[str, Any]) -> str:
    states = [r["state"] for r in payload["resources"].values()]
    return (
        f"MORI_CGROUP_PRESSURE: {payload['verdict']} (group={payload['group']} "
        f"ok={states.count(STATE_OK)} absent={states.count(STATE_ABSENT)} "
        f"unreadable={states.count(STATE_UNREADABLE)} "
        f"malformed={states.count(STATE_MALFORMED)} "
        f"findings={len(payload['findings'])})"
    )


class _UsageError(Exception):
    pass


class _Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise _UsageError(message)


def build_parser() -> argparse.ArgumentParser:
    parser = _Parser(description="Read-only per-cgroup PSI survey (one-shot).")
    parser.add_argument("--root", default=DEFAULT_ROOT,
                        help=f"cgroup filesystem root (default {DEFAULT_ROOT})")
    parser.add_argument("--group", default=DEFAULT_GROUP,
                        help=f"cgroup path under root (default {DEFAULT_GROUP})")
    parser.add_argument("--resources", default=",".join(RESOURCE_NAMES),
                        help="comma-separated subset of " + ",".join(RESOURCE_NAMES))
    parser.add_argument("--warn-avg10", type=float, default=DEFAULT_WARN_AVG10,
                        help="some avg10 threshold, local and not calibrated")
    parser.add_argument("--cases", default=None,
                        help="override path to cases.json (selftest)")
    parser.add_argument("--scratch", default=None,
                        help="scratch directory (selftest temp output; honored, TMPDIR fallback)")
    parser.add_argument("--selftest", action="store_true",
                        help="run the fixture battery over tools/fixtures/mori-cgroup-pressure")
    return parser


def _cases_path(explicit: Optional[str]) -> Path:
    if explicit:
        return Path(explicit)
    script_dir = Path(os.path.dirname(os.path.realpath(__file__)))
    return script_dir / "fixtures" / "mori-cgroup-pressure" / "cases.json"


def _expected_states(case: Dict[str, Any]) -> Dict[str, str]:
    return {k: v for k, v in case.get("resources", {}).items()}


def _case_failures(case: Dict[str, Any], payload: Dict[str, Any], rc: int) -> List[str]:
    problems: List[str] = []
    if payload["verdict"] != case.get("verdict"):
        problems.append(f"verdict {payload['verdict']} != {case.get('verdict')}")
    if rc != case.get("rc"):
        problems.append(f"rc {rc} != {case.get('rc')}")
    for name, want in _expected_states(case).items():
        got = payload["resources"].get(name, {}).get("state")
        if got != want:
            problems.append(f"{name} state {got} != {want}")
    if case.get("high_resources") is not None:
        got_high = sorted(f["resource"] for f in payload["findings"]
                          if f["kind"] == "PRESSURE_HIGH")
        if got_high != sorted(case["high_resources"]):
            problems.append(f"high {got_high} != {sorted(case['high_resources'])}")
    if case.get("psi_accounting") is not None:
        got = payload.get("psi_accounting", {}).get("value")
        if got != case["psi_accounting"]:
            problems.append(f"psi_accounting {got} != {case['psi_accounting']}")
    return problems


def _selftest(cases_override: Optional[str]) -> int:
    cases_path = _cases_path(cases_override)
    try:
        doc = json.loads(cases_path.read_text())
    except OSError as exc:
        print(f"{SELFTEST_PREFIX}: FAIL cases-unreadable {cases_path} ({exc})")
        return 1
    if doc.get("schema") != CASES_SCHEMA:
        print(f"{SELFTEST_PREFIX}: FAIL bad-cases-schema {doc.get('schema')!r}")
        return 1
    base = cases_path.parent
    passed = failed = 0
    for case in doc.get("cases", []):
        root = str(base / case["name"] / "sys" / "fs" / "cgroup")
        try:
            payload, rc = evaluate(root, case.get("group", DEFAULT_GROUP),
                                   float(case.get("warn_avg10", DEFAULT_WARN_AVG10)))
            problems = _case_failures(case, payload, rc)
        except Exception as exc:  # noqa: BLE001 — a crashing case is a failure
            problems = [f"exception {exc!r}"]
        # corrupted-expectation negative: flipping one expectation must fail
        neg_ok = True
        if problems == [] and case.get("resources"):
            first = sorted(case["resources"])[0]
            bad = dict(case)
            bad["resources"] = dict(case["resources"])
            bad["resources"][first] = "zz-wrong" if case["resources"][first] != "zz-wrong" else "ok"
            if _case_failures(bad, payload, rc) == []:
                neg_ok = False
        if problems == [] and neg_ok:
            passed += 1
            print(f"case {case['name']}: pass")
        else:
            failed += 1
            print(f"case {case['name']}: FAIL {problems}" + ("" if neg_ok else " [corrupted-expectation accepted]"))
    print(f"{SELFTEST_PREFIX}: pass={passed} fail={failed}")
    return 0 if failed == 0 and passed > 0 else 1


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except _UsageError as exc:
        print(json.dumps({"schema": SCHEMA, "error": str(exc)}))
        return 2
    if args.selftest:
        return _selftest(args.cases)
    names = tuple(s.strip() for s in args.resources.split(",") if s.strip())
    bad = [n for n in names if n not in RESOURCE_NAMES]
    if bad or not names:
        print(json.dumps({"schema": SCHEMA, "error": f"unknown resources {bad}"}))
        return 2
    try:
        payload, rc = evaluate(args.root, args.group, args.warn_avg10, names)
    except ValueError as exc:
        print(json.dumps({"schema": SCHEMA, "error": str(exc)}))
        return 2
    sys.stdout.write(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    sys.stdout.write(summary_line(payload) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
