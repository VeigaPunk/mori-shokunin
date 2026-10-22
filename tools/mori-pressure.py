#!/usr/bin/env python3
"""Read-only system pressure (PSI) survey for CPU, memory, IO and IRQ.

Round 24, claim C2 (coverage axis, frontier FR12).  The census reads only the
user slice's ``memory.pressure``; the system PSI files under ``/proc/pressure``
are unobserved.  This tool moves one-shot (one read per resource) system
pressure reading to Core.  The resident trigger watcher and the cgroup-scoped
CPU/IO/IRQ pressure stay frontier.

Scope (contract C2 with amendments A2, A3):

* ``--root DIR`` (default ``/proc/pressure``); reads the files ``cpu``,
  ``memory``, ``io``, ``irq`` found directly under it.
* Line grammar: ``^(some|full) avg10=D avg60=D avg300=D total=N$`` with D a
  decimal and N a non-negative integer (microseconds).  Duplicate kinds, a
  missing required kind or any other shape -> resource state ``malformed``.
* Required kinds: cpu/memory/io need both ``some`` and ``full``; irq needs
  ``full`` only, and its missing ``some`` is expected (``some: null``), never
  malformed.
* System cpu ``full`` is reported but labelled ``full_system_undefined: true``;
  it is never used for a threshold and never read as evidence of no stall.
* Open/read errors map exactly: ENOENT -> ``absent``; EOPNOTSUPP ->
  ``unsupported`` (no cause inferred, per A2); EACCES/EPERM ->
  ``unreadable``; any other errno -> ``unreadable`` with the errno name in
  notes.  All three unavailable states are never zero.
* Threshold: ``--warn-avg10 X`` (default 10.0, labelled local, not calibrated)
  raises ``PRESSURE_HIGH`` when avg10 >= X on ``some`` of cpu/io/memory or
  ``full`` of memory/io/irq.
* ``--interval S`` (0 < S <= 10): reads twice, reports ``total_delta_us`` and
  ``stall_ratio`` (nominal: delta / (S * 1e6), may exceed 1) per kind.  System
  cpu ``full`` always gets ``total_delta_us: null`` and ``stall_ratio: null``.
  A resource whose two reads differ in state reports the worse (non-ok) state
  with no delta; thresholds use the second read when both reads are ok.  A
  decreasing total -> resource state ``counter_regressed``, which counts toward
  ``PRESSURE_PARTIAL`` like malformed.  An additive ``elapsed_us`` field
  accompanies the interval output (measured; null under the selftest's no-op
  sleep).
* Output: one JSON object, ``schema: mori-pressure-v1``, ``resources`` keyed
  by name, each ``{state, some, full, notes[]}``, plus ``verdict`` in
  ``PRESSURE_OK | PRESSURE_HIGH | PRESSURE_PARTIAL | PRESSURE_UNAVAILABLE``
  and ``findings[]`` (each with ``id`` and ``resource``).
* Exit: 0 on OK/PARTIAL; 1 on PRESSURE_HIGH; 2 when every resource is
  unavailable or on a usage error.
* ``--selftest`` loads the frozen cases in
  ``tools/fixtures/mori-pressure/cases.json`` resolved from the script's own
  directory and prints ``MORI_PRESSURE_SELFTEST: PASS n/N`` (or FAIL, plus one
  line per failed case id); exit 0 only when all pass.  Error injection
  (EOPNOTSUPP, EACCES, EPERM, ENOENT) is a single in-process hook covering the
  open+read pair, documented as such; the interval sleep is a no-op there.

Python 3 standard library only; read-only; safe under ``python3 -I``.
"""

from __future__ import annotations

import argparse
import errno
import json
import os
import re
import sys
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

import math
SCHEMA = "mori-pressure-v1"
CASES_SCHEMA = "mori-pressure-cases-v1"
SELFTEST_PREFIX = "MORI_PRESSURE_SELFTEST"

RESOURCE_NAMES: Tuple[str, ...] = ("cpu", "memory", "io", "irq")
REQUIRED_KINDS: Dict[str, Tuple[str, ...]] = {
    "cpu": ("some", "full"),
    "memory": ("some", "full"),
    "io": ("some", "full"),
    "irq": ("full",),
}
THRESHOLD_KINDS: Dict[str, Tuple[str, ...]] = {
    "cpu": ("some",),
    "memory": ("some", "full"),
    "io": ("some", "full"),
    "irq": ("full",),
}
# ``full`` is undefined for the system cpu resource; its interval delta fields
# are always null (never a numeric zero).
FULL_UNDEFINED: Dict[str, bool] = {"cpu": True}

DEFAULT_ROOT = "/proc/pressure"
DEFAULT_WARN_AVG10 = 10.0
MAX_INTERVAL_SECONDS = 10.0

STATE_OK = "ok"
STATE_ABSENT = "absent"
STATE_UNSUPPORTED = "unsupported"
STATE_UNREADABLE = "unreadable"
STATE_MALFORMED = "malformed"
STATE_REGRESSED = "counter_regressed"
UNAVAILABLE_STATES = frozenset({STATE_ABSENT, STATE_UNSUPPORTED, STATE_UNREADABLE})

# Ordering for "worse" state when the two interval reads disagree.  Data
# integrity failure (malformed) ranks above access failure (unreadable), and
# access failure above the softer unavailable states.  All non-ok states lead
# to the same verdict treatment (PARTIAL except when every resource is
# unavailable), so this only selects what is reported.
_STATE_SEVERITY: Dict[str, int] = {
    STATE_MALFORMED: 4,
    STATE_REGRESSED: 3,
    STATE_UNREADABLE: 2,
    STATE_UNSUPPORTED: 1,
    STATE_ABSENT: 0,
}

VERDICT_OK = "PRESSURE_OK"
VERDICT_HIGH = "PRESSURE_HIGH"
VERDICT_PARTIAL = "PRESSURE_PARTIAL"
VERDICT_UNAVAILABLE = "PRESSURE_UNAVAILABLE"

RC_OK = 0
RC_HIGH = 1
RC_UNAVAILABLE = 2

LINE_RE = re.compile(
    r"^(some|full) avg10=([0-9]+(?:\.[0-9]+)?) avg60=([0-9]+(?:\.[0-9]+)?) "
    r"avg300=([0-9]+(?:\.[0-9]+)?) total=([0-9]+)$"
)

# In-process hooks, used only by --selftest.  The open hook covers the whole
# open+read pair: it returns the file text or raises an OSError carrying the
# errno that the read (or open) would produce.  The sleep hook replaces the
# real delay during interval cases.
_OPEN_HOOK: Optional[Callable[[str, str], str]] = None
_SLEEP_HOOK: Optional[Callable[[float], None]] = None
_SELFTEST_RUNNING = False


def _state_for_oserror(exc: OSError) -> Tuple[str, str]:
    code = exc.errno
    name = errno.errorcode.get(code, "EUNKNOWN")
    if code == errno.ENOENT:
        return STATE_ABSENT, "open/read reported ENOENT; resource absent, never reported as zero"
    if code == errno.EOPNOTSUPP:
        # A2: no cause inferred (boot/kernel-config diagnosis belongs elsewhere).
        return STATE_UNSUPPORTED, "open/read reported EOPNOTSUPP; resource unsupported, never reported as zero"
    if code == errno.EACCES:
        return STATE_UNREADABLE, "open/read reported EACCES; resource unreadable, never reported as zero"
    if code == errno.EPERM:
        return STATE_UNREADABLE, "open/read reported EPERM; resource unreadable, never reported as zero"
    return STATE_UNREADABLE, "open/read reported %s (errno %s); resource unreadable, never reported as zero" % (
        name, code)


def _read_resource(name: str, root: str) -> Tuple[str, Optional[Dict[str, Any]], Optional[Dict[str, Any]], List[str]]:
    path = os.path.join(root, name)
    try:
        if _OPEN_HOOK is not None:
            text = _OPEN_HOOK(name, path)
        else:
            with open(path, "r", encoding="utf-8") as fh:
                text = fh.read()
    except OSError as exc:
        state, note = _state_for_oserror(exc)
        return state, None, None, [note]
    except UnicodeDecodeError:
        return STATE_MALFORMED, None, None, [
            "file content is not UTF-8 text; resource malformed, never reported as zero"]
    except Exception as exc:  # belt-and-braces for a malformed hook
        return STATE_UNREADABLE, None, None, [
            "open/read failed with %s; resource unreadable, never reported as zero" % type(exc).__name__]
    return _parse_resource(name, text)


def _parse_resource(name: str, text: str) -> Tuple[str, Optional[Dict[str, Any]], Optional[Dict[str, Any]], List[str]]:
    kinds: Dict[str, Dict[str, Any]] = {}
    for raw in text.splitlines():
        line = raw.rstrip("\r")
        match = LINE_RE.fullmatch(line)
        if match is None:
            return STATE_MALFORMED, None, None, [
                "line does not match the PSI grammar: %r" % line]
        kind = match.group(1)
        if kind in kinds:
            return STATE_MALFORMED, None, None, [
                "duplicate %r line" % kind]
        kinds[kind] = {
            "avg10": float(match.group(2)),
            "avg60": float(match.group(3)),
            "avg300": float(match.group(4)),
            "total": int(match.group(5)),
        }
    missing = [k for k in REQUIRED_KINDS[name] if k not in kinds]
    if missing:
        return STATE_MALFORMED, None, None, [
            "missing required %r line" % missing[0]]
    notes = ["parsed from the kernel PSI line grammar"]
    some = kinds.get("some")
    full = kinds.get("full")
    if name == "cpu":
        notes.append("system cpu 'full' is undefined by the kernel: reported, never used for a threshold")
    return STATE_OK, some, full, notes


def _resource_payload(
    name: str,
    state: str,
    some: Optional[Dict[str, Any]],
    full: Optional[Dict[str, Any]],
    notes: List[str],
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "state": state,
        "some": some,
        "full": full,
        "notes": notes,
    }
    if name in FULL_UNDEFINED:
        payload["full_system_undefined"] = True
    return payload


def _worse_state(a: str, b: str) -> str:
    return a if _STATE_SEVERITY[a] >= _STATE_SEVERITY[b] else b


def _read_once(root: str) -> Dict[str, Tuple[str, Optional[Dict[str, Any]], Optional[Dict[str, Any]], List[str]]]:
    out: Dict[str, Tuple[str, Optional[Dict[str, Any]], Optional[Dict[str, Any]], List[str]]] = {}
    for name in RESOURCE_NAMES:
        out[name] = _read_resource(name, root)
    return out


def _sleep(seconds: float) -> None:
    if _SLEEP_HOOK is not None:
        _SLEEP_HOOK(seconds)
    else:
        time.sleep(seconds)


def _combine_interval(
    name: str,
    first: Tuple[str, Optional[Dict[str, Any]], Optional[Dict[str, Any]], List[str]],
    second: Tuple[str, Optional[Dict[str, Any]], Optional[Dict[str, Any]], List[str]],
    interval_s: float,
) -> Dict[str, Any]:
    fstate, fsome, ffull, fnotes = first
    sstate, ssome, sfull, snotes = second
    merged_notes = list(fnotes)
    for note in snotes:
        if note not in merged_notes:
            merged_notes.append(note)

    # A3: a resource whose two reads differ in state reports the worse (non-ok)
    # state of either read, with no delta.
    if fstate != STATE_OK and sstate != STATE_OK:
        return _resource_payload(name, _worse_state(fstate, sstate), None, None, merged_notes)
    if fstate != STATE_OK:
        return _resource_payload(name, fstate, None, None, merged_notes)
    if sstate != STATE_OK:
        return _resource_payload(name, sstate, None, None, merged_notes)

    # Both reads ok: report the second read, add deltas per kind.
    some = dict(ssome) if ssome is not None else None
    full = dict(sfull) if sfull is not None else None
    regressed = False
    for kind, value in (("some", some), ("full", full)):
        if value is None:
            continue
        prev = fsome if kind == "some" else ffull
        if prev is None:
            # A kind present in one read only; leave delta fields absent.
            continue
        if name in FULL_UNDEFINED and kind == "full":
            # A3: system cpu full always carries null delta fields (never zero).
            value["total_delta_us"] = None
            value["stall_ratio"] = None
            continue
        delta = value["total"] - prev["total"]
        value["total_delta_us"] = delta
        value["stall_ratio"] = round(delta / (interval_s * 1e6), 6)
        if delta < 0:
            regressed = True
    if regressed:
        merged_notes.append("a total counter decreased between the two reads; the counter regressed")
        return _resource_payload(name, STATE_REGRESSED, some, full, merged_notes)
    return _resource_payload(name, STATE_OK, some, full, merged_notes)


def _findings(resources: Dict[str, Dict[str, Any]], warn_avg10: float) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    for name in RESOURCE_NAMES:
        res = resources[name]
        if res["state"] != STATE_OK:
            continue
        best: Optional[Tuple[str, float]] = None
        for kind in THRESHOLD_KINDS[name]:
            values = res.get(kind)
            if not values:
                continue
            avg10 = values.get("avg10")
            if avg10 is None:
                continue
            if avg10 >= warn_avg10 and (best is None or avg10 > best[1]):
                best = (kind, avg10)
        if best is not None:
            findings.append({
                "id": "PRESSURE_HIGH",
                "resource": name,
                "kind": best[0],
                "avg10": best[1],
                "threshold_avg10": warn_avg10,
                "detail": "%s %s avg10 %.2f is at or above the local (not calibrated) threshold %.2f" % (
                    name, best[0], best[1], warn_avg10),
            })
    return findings


def evaluate(root: str, warn_avg10: float, interval_s: Optional[float]) -> Tuple[Dict[str, Any], int]:
    if not math.isfinite(warn_avg10) or warn_avg10 < 0:
        raise ValueError("--warn-avg10 must be finite and non-negative")
    elapsed_us: Optional[int] = None
    if interval_s is not None:
        if not (0 < interval_s <= MAX_INTERVAL_SECONDS):
            raise ValueError("--interval must satisfy 0 < S <= 10")
        if _SLEEP_HOOK is None and not _SELFTEST_RUNNING:
            start = time.monotonic_ns()
        first = _read_once(root)
        _sleep(interval_s)
        second = _read_once(root)
        if _SLEEP_HOOK is None and not _SELFTEST_RUNNING:
            elapsed_us = (time.monotonic_ns() - start) // 1000
        resources: Dict[str, Dict[str, Any]] = {}
        for name in RESOURCE_NAMES:
            resources[name] = _combine_interval(name, first[name], second[name], interval_s)
    else:
        snap = _read_once(root)
        resources = {}
        for name in RESOURCE_NAMES:
            state, some, full, notes = snap[name]
            resources[name] = _resource_payload(name, state, some, full, notes)

    findings = _findings(resources, warn_avg10)
    states = [r["state"] for r in resources.values()]
    if all(s in UNAVAILABLE_STATES for s in states):
        verdict, rc = VERDICT_UNAVAILABLE, RC_UNAVAILABLE
    elif findings:
        verdict, rc = VERDICT_HIGH, RC_HIGH
    elif any(s != STATE_OK for s in states):
        verdict, rc = VERDICT_PARTIAL, RC_OK
    else:
        verdict, rc = VERDICT_OK, RC_OK

    payload: Dict[str, Any] = {
        "schema": SCHEMA,
        "root": root,
        "threshold": {
            "metric": "avg10",
            "value": warn_avg10,
            "label": "local (not calibrated)",
        },
        "resources": resources,
        "verdict": verdict,
        "findings": findings,
    }
    if interval_s is not None:
        payload["interval_s"] = interval_s
        payload["elapsed_us"] = elapsed_us
    return payload, rc


class _UsageError(Exception):
    pass


class _Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:  # noqa: D102
        raise _UsageError(message)


def build_parser() -> argparse.ArgumentParser:
    parser = _Parser(
        prog="mori-pressure.py",
        description="Read-only system PSI pressure survey for cpu/memory/io/irq.",
        allow_abbrev=False,
    )
    parser.add_argument("--root", default=DEFAULT_ROOT, help="directory holding the cpu/memory/io/irq PSI files")
    parser.add_argument("--warn-avg10", type=float, default=DEFAULT_WARN_AVG10,
                        help="PRESSURE_HIGH threshold on avg10 (default 10.0, local, not calibrated)")
    parser.add_argument("--interval", type=float, default=None,
                        help="read twice, about S seconds apart, and report delta/ratio (0 < S <= 10)")
    parser.add_argument("--selftest", action="store_true", help="run the frozen cases in cases.json")
    parser.add_argument("--cases", default=None,
                        help="with --selftest: run this case file instead of the frozen cases.json")
    return parser


def _emit(payload: Dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, sort_keys=True, indent=2) + "\n")


def _emit_error(message: str) -> None:
    _emit({"schema": SCHEMA, "root": DEFAULT_ROOT, "error": message})


def _cases_path() -> Optional[str]:
    script_dir = os.path.dirname(os.path.realpath(__file__))
    candidates = [
        os.path.join(script_dir, "fixtures", "mori-pressure", "cases.json"),
        os.path.join(script_dir, "..", "tools", "fixtures", "mori-pressure", "cases.json"),
    ]
    for candidate in candidates:
        if os.path.isfile(candidate):
            return candidate
    return None


def _snapshot_hook(snapshots: List[Dict[str, Any]]) -> Callable[[str, str], str]:
    counters = {name: 0 for name in RESOURCE_NAMES}
    error_aliases = {
        "EOPNOTSUPP": errno.EOPNOTSUPP,
        "EACCES": errno.EACCES,
        "EPERM": errno.EPERM,
        "ENOENT": errno.ENOENT,
    }

    def hook(name: str, path: str) -> str:
        idx = counters[name]
        counters[name] += 1
        snapshot = snapshots[min(idx, len(snapshots) - 1)]
        errors = snapshot.get("errors") or {}
        if name in errors:
            token = errors[name]
            code = error_aliases.get(token, errno.EIO)
            raise OSError(code, "injected %s for %s" % (token, name), path)
        files = snapshot.get("files") or {}
        if name in files:
            return files[name]
        raise OSError(errno.ENOENT, "No such file or directory", path)

    return hook


def _case_failures(case: Dict[str, Any]) -> List[str]:
    global _OPEN_HOOK, _SLEEP_HOOK
    problems: List[str] = []
    snapshots = case.get("snapshots") or []
    args = case.get("args") or []
    expect = case.get("expect") or {}
    parser = build_parser()
    try:
        ns = parser.parse_args(list(args))
    except _UsageError as exc:
        return ["case arguments are not usable: %s" % exc]
    if ns.selftest:
        return ["case must not request --selftest"]
    if len(snapshots) != (2 if ns.interval is not None else 1):
        return ["wrong number of snapshots"]
    _OPEN_HOOK = _snapshot_hook(snapshots)
    _SLEEP_HOOK = lambda seconds: None
    try:
        payload, rc = evaluate(ns.root, ns.warn_avg10, ns.interval)
    except ValueError as exc:
        return ["interval validation failed: %s" % exc]

    if rc != expect.get("exit"):
        problems.append("exit %s != %s" % (rc, expect.get("exit")))
    if payload.get("verdict") != expect.get("verdict"):
        problems.append("verdict %s != %s" % (payload.get("verdict"), expect.get("verdict")))
    for rname, rexpect in (expect.get("resources") or {}).items():
        actual = payload.get("resources", {}).get(rname)
        if actual is None:
            problems.append("resource %s missing" % rname)
            continue
        for key, value in rexpect.items():
            if key in ("some", "full"):
                actual_value = actual.get(key)
                if value is None:
                    if actual_value is not None:
                        problems.append("%s.%s is %r, expected null" % (rname, key, actual_value))
                else:
                    if not isinstance(actual_value, dict):
                        problems.append("%s.%s is not an object" % (rname, key))
                    else:
                        for k2, v2 in value.items():
                            if k2 not in actual_value:
                                problems.append("%s.%s.%s missing" % (rname, key, k2))
                            elif actual_value[k2] != v2:
                                problems.append("%s.%s.%s is %r, expected %r" % (
                                    rname, key, k2, actual_value[k2], v2))
            else:
                if key not in actual:
                    problems.append("%s.%s missing" % (rname, key))
                elif actual[key] != value:
                    problems.append("%s.%s is %r, expected %r" % (rname, key, actual[key], value))
    for pair in expect.get("findings_include") or []:
        if len(pair) < 2:
            continue
        fid, resource = pair[0], pair[1]
        if not any(f.get("id") == fid and f.get("resource") == resource for f in payload.get("findings") or []):
            problems.append("finding %s on %s missing" % (fid, resource))
    return problems


def _corrupted_expectations(case: Dict[str, Any]) -> List[Tuple[str, Dict[str, Any]]]:
    """Copies of a case whose expectation is deliberately wrong (round-24 wave-2 finding:
    a weakened matcher survived the frozen cases). The matcher must reject every copy."""
    out: List[Tuple[str, Dict[str, Any]]] = []
    expect = case.get("expect") or {}
    other = {"PRESSURE_OK": "PRESSURE_HIGH", "PRESSURE_HIGH": "PRESSURE_OK",
             "PRESSURE_PARTIAL": "PRESSURE_OK", "PRESSURE_UNAVAILABLE": "PRESSURE_OK"}
    bad = json.loads(json.dumps(case))
    bad["expect"]["verdict"] = other.get(expect.get("verdict"), "PRESSURE_OK")
    out.append(("verdict", bad))
    bad = json.loads(json.dumps(case))
    bad["expect"]["exit"] = (expect.get("exit", 0) + 1) % 3
    out.append(("exit", bad))
    bad = json.loads(json.dumps(case))
    bad["expect"]["findings_include"] = list(expect.get("findings_include") or []) + [["PRESSURE_HIGH", "absent-resource"]]
    out.append(("finding", bad))
    for rname, rexpect in sorted((expect.get("resources") or {}).items()):
        if "state" in rexpect:
            bad = json.loads(json.dumps(case))
            bad["expect"]["resources"][rname]["state"] = "malformed" if rexpect["state"] != "malformed" else "ok"
            out.append(("state", bad))
            break
    return out


def _selftest(cases_override: Optional[str] = None) -> int:
    global _SELFTEST_RUNNING, _OPEN_HOOK, _SLEEP_HOOK
    path = cases_override if cases_override is not None else _cases_path()
    if path is None:
        print("%s: FAIL 0/0" % SELFTEST_PREFIX)
        print("ERROR: cases file not found near %s" % os.path.dirname(os.path.realpath(__file__)))
        return RC_UNAVAILABLE
    try:
        with open(path, "r", encoding="utf-8") as fh:
            document = json.load(fh)
    except (OSError, ValueError) as exc:
        print("%s: FAIL 0/0" % SELFTEST_PREFIX)
        print("ERROR: cases file unreadable (%s): %s" % (path, exc))
        return RC_UNAVAILABLE
    if document.get("schema") != CASES_SCHEMA:
        print("%s: FAIL 0/0" % SELFTEST_PREFIX)
        print("ERROR: cases file schema %r != %r" % (document.get("schema"), CASES_SCHEMA))
        return RC_UNAVAILABLE
    cases = document.get("cases") or []
    total = len(cases)
    if not cases:
        print("%s: FAIL 0/0" % SELFTEST_PREFIX)
        print("ERROR: no cases supplied")
        return RC_UNAVAILABLE
    passed = 0
    failures: List[Tuple[str, str]] = []
    controls = 0
    rejected = 0
    accepted: List[str] = []
    prev_open, prev_sleep = _OPEN_HOOK, _SLEEP_HOOK
    _SELFTEST_RUNNING = True
    try:
        for case in cases:
            cid = str(case.get("id", "?"))
            pending = _case_failures(case)
            if pending:
                failures.append((cid, "; ".join(pending)))
                continue
            passed += 1
            for label, bad in _corrupted_expectations(case):
                controls += 1
                if _case_failures(bad):
                    rejected += 1
                else:
                    accepted.append("%s/%s" % (cid, label))
    finally:
        _OPEN_HOOK, _SLEEP_HOOK = prev_open, prev_sleep
        _SELFTEST_RUNNING = False
    if failures:
        print("%s: FAIL %d/%d" % (SELFTEST_PREFIX, passed, total))
        for cid, detail in failures:
            print("%s: %s" % (cid, detail))
        return 1
    if accepted:
        print("%s: FAIL %d/%d" % (SELFTEST_PREFIX, passed, total))
        print("MATCHER: accepted %d of %d corrupted expectations: %s" % (
            len(accepted), controls, ", ".join(accepted)))
        return 1
    print("%s: PASS %d/%d" % (SELFTEST_PREFIX, passed, total))
    print("MATCHER: rejected %d/%d corrupted expectations" % (rejected, controls))
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    try:
        ns = parser.parse_args(argv)
    except _UsageError as exc:
        _emit_error(str(exc))
        return RC_UNAVAILABLE
    if ns.cases is not None and not ns.selftest:
        _emit_error("--cases is only valid with --selftest")
        return RC_UNAVAILABLE
    if ns.selftest:
        return _selftest(ns.cases)
    if ns.interval is not None and not (0 < ns.interval <= MAX_INTERVAL_SECONDS):
        _emit_error("--interval must satisfy 0 < S <= 10")
        return RC_UNAVAILABLE
    if ns.warn_avg10 < 0:
        _emit_error("--warn-avg10 must not be negative")
        return RC_UNAVAILABLE
    try:
        payload, rc = evaluate(ns.root, ns.warn_avg10, ns.interval)
    except ValueError as exc:
        _emit_error(str(exc))
        return RC_UNAVAILABLE
    _emit(payload)
    return rc


if __name__ == "__main__":
    sys.exit(main())
