#!/usr/bin/env python3
"""Hyaku driver-liveness reader (round 56, C1 — coverage advance, frontier FR5).

Under the hyaku inline driver no shokunin-watchdog daemon runs, so the census
watchdog surface fires WATCHDOG_ABSENT every round; the driver's own
launch/complete/dead lines in .ufo/watchdog.log are a second liveness source
nobody reads (FR5 named open ground, corpus/README.md).  This probe reads that
log and reports per-lane driver-activity facts.  Detection and report only:
every field is a log-shape fact (counts, ages, pairing state); the probe emits
no wellness or failure verdict about a lane and never remediates.

Frozen line grammar (two writers, one log; every variant observed in the
committed live log 2026-09-28..2026-10-27):
  <iso8601-ts> launch <lane> round=<n> pgid=<pid> driver=hyaku-inline attempt=<a>   # inline.sh:149
  <iso8601-ts> launch <lane> round=<n> pgid=<pid>                                   # shokunin-watchdog.sh:266
  <iso8601-ts> launch <lane> round=<n> pgid=<pid> mission=<id>                      # steered launch, old driver
  <iso8601-ts> launch <lane> round=<n> mission=<id>                                 # steered launch, no pgid
  <iso8601-ts> launch <lane> round=<n> runId=<id>                                   # ufo-fsd launch
  <iso8601-ts> launch <lane> round=<n>                                              # bare launch
  <iso8601-ts> complete <lane> round=<n>; hyaku-inline attempt=<a>                  # inline.sh:176
  <iso8601-ts> complete <lane> round=<n>; advancing to round=<n+1>                  # shokunin-watchdog.sh:405
  <iso8601-ts> complete <lane> round=<n>; respawning                                # legacy respawn (120 in log)
  <iso8601-ts> lane-dead-no-report <lane> round=<n>; retry same round [(<free>)]    # inline.sh:182 / :448
  <iso8601-ts> launch-fail <lane> round=<n> :: <reason>                             # shokunin-watchdog.sh:241-249
  <iso8601-ts> wrap <lane> round=<n> landed[; NOT respawning (fleet-wrap)]          # shokunin-watchdog.sh:398
A ts-first line that is not one of these is an other_line (driver prose such as
`steer ...` or `watchdog tick ...`): counted, capped examples, never a lane
event and never malformed.  A line whose first token is not an ISO-8601
timestamp, or an event line with an unrecognized rest, is malformed: counted,
capped examples, never silent.

Output: one JSON object, schema mori-driver-liveness-v1: log shape (lines,
malformed, mtime age), per-lane rows (launches/completes/deads/launch_fails,
last launch ts + age vs --now, in_flight = last event is a launch, unclosed
= launches with no same-(lane,round,attempt) complete — a pairing count, not a
failure claim), state-dir entry shapes (*.round regular/symlink/dir/other,
values never read, symlinks never followed), and verdict
DRIVER_LIVENESS_OK | DRIVER_LIVENESS_UNAVAILABLE (missing/unreadable/empty
log — unavailable is never zero).  rc 0 / 2 (setup).  Read-only: opens its
inputs read-only, writes nothing.

Usage: mori-driver-liveness.py [--fleet-root DIR] [--log PATH] [--state-dir DIR]
           [--now EPOCH] [--fixture DIR] [--selftest]
--fixture DIR: read DIR/watchdog.log and DIR/state/ (a frozen synthetic tree)
instead of the live paths — the selftest's only network-free mode.
"""
import argparse
import datetime
import json
import os
import re
import sys

LINE_RE = re.compile(
    r"^(\S+) (launch|complete|lane-dead-no-report|launch-fail|wrap) ([A-Za-z0-9_-]+) round=(\d+)(.*)$")
LAUNCH_REST_RE = re.compile(
    r"^(?: pgid=(\d+)(?: driver=(\S+))?(?: slot=(\d+))?(?: attempt=(\d+))?(?: mission=(\S+))?"
    r"| pid=(\d+)| mission=(\S+)| runId=(\S+))?$")
COMPLETE_REST_RE = re.compile(r"^; (?:hyaku-inline attempt=(\d+)|advancing to round=(\d+)|respawning)$")
DEAD_REST_RE = re.compile(r"^; retry same round(?: \((.*)\))?$")
LAUNCHFAIL_RE = re.compile(r"^ :: (.*)$")
WRAP_REST_RE = re.compile(r"^ (?:landed|complete)(?:; NOT respawning \(fleet-wrap\))?$")
MAX_MALFORMED_EXAMPLES = 3


def _repo_path(*parts):
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), *parts)


def parse_ts(tok):
    try:
        return datetime.datetime.fromisoformat(tok).timestamp()
    except (ValueError, OverflowError):
        return None


def parse_log(text):
    lanes = {}
    malformed = 0
    other_lines = 0
    examples = []
    newest_ts = None
    nlines = 0

    def _bad(raw):
        nonlocal malformed
        malformed += 1
        if len(examples) < MAX_MALFORMED_EXAMPLES:
            examples.append(raw[:120])

    for raw in text.split("\n"):
        if raw.strip() == "":
            continue
        nlines += 1
        first = raw.split(" ", 1)[0]
        if parse_ts(first) is None:
            _bad(raw)
            continue
        m = LINE_RE.match(raw)
        if not m:
            other_lines += 1  # ts-first driver prose (steer, watchdog tick, ...)
            continue
        ts_tok, event, lane, round_s, rest = m.groups()
        ts = parse_ts(ts_tok)
        if ts is None:
            _bad(raw)
            continue
        newest_ts = ts if newest_ts is None else max(newest_ts, ts)
        row = lanes.setdefault(lane, {
            "launches": 0, "completes": 0, "deads": 0, "launch_fails": 0, "wraps": 0,
            "last_launch_ts": None, "last_event": None, "rounds": set(),
            "open_launches": [], "attempts": {}})
        row["rounds"].add(int(round_s))
        key = (int(round_s), None)

        def close_round():
            if key in row["open_launches"]:
                row["open_launches"].remove(key)
            elif (int(round_s), None) in row["open_launches"]:
                row["open_launches"].remove((int(round_s), None))

        if event == "launch":
            m2 = LAUNCH_REST_RE.match(rest)
            if not m2:
                _bad(raw)
                continue
            if m2.group(4) is not None:
                key = (int(round_s), int(m2.group(4)))
                row["attempts"].setdefault(int(m2.group(4)), 0)
            row["launches"] += 1
            row["last_launch_ts"] = ts
            row["last_event"] = "launch"
            row["open_launches"].append(key)
        elif event == "complete":
            m2 = COMPLETE_REST_RE.match(rest)
            if not m2:
                _bad(raw)
                continue
            if m2.group(1) is not None:
                key = (int(round_s), int(m2.group(1)))
            row["completes"] += 1
            row["last_event"] = "complete"
            close_round()
        elif event == "wrap":
            if not WRAP_REST_RE.match(rest):
                _bad(raw)
                continue
            row["wraps"] += 1
            row["last_event"] = "wrap"
            close_round()
        elif event == "lane-dead-no-report":
            if not DEAD_REST_RE.match(rest):
                _bad(raw)
                continue
            row["deads"] += 1
            row["last_event"] = "dead"
            row["open_launches"] = [k for k in row["open_launches"] if k[0] != int(round_s)]
        else:  # launch-fail
            if not LAUNCHFAIL_RE.match(rest):
                _bad(raw)
                continue
            row["launch_fails"] += 1
            row["last_event"] = "launch-fail"
    out = {}
    for lane, row in sorted(lanes.items()):
        out[lane] = {
            "launches": row["launches"], "completes": row["completes"],
            "deads": row["deads"], "launch_fails": row["launch_fails"],
            "wraps": row["wraps"],
            "rounds_seen": len(row["rounds"]),
            "last_launch_ts": row["last_launch_ts"],
            "in_flight": row["last_event"] == "launch",
            "unclosed": len(row["open_launches"]),
        }
    return out, {"lines": nlines, "malformed": malformed, "other_lines": other_lines,
                 "examples": examples, "newest_ts": newest_ts}


def state_shapes(state_dir):
    shapes = {"regular": 0, "symlink": 0, "dir": 0, "other": 0}
    if not state_dir or not os.path.isdir(state_dir):
        return None
    try:
        for name in sorted(os.listdir(state_dir)):
            if not name.endswith(".round"):
                continue
            p = os.path.join(state_dir, name)
            if os.path.islink(p):
                shapes["symlink"] += 1  # never followed
            elif os.path.isfile(p):
                shapes["regular"] += 1
            elif os.path.isdir(p):
                shapes["dir"] += 1
            else:
                shapes["other"] += 1
    except OSError:
        return None
    return shapes


def run(log_path=None, state_dir=None, now=None):
    now = now if now is not None else datetime.datetime.now().timestamp()
    report = {"schema": "mori-driver-liveness-v1"}
    if not log_path or not os.path.isfile(log_path):
        report["log"] = {"path": log_path, "state": "absent"}
        report["verdict"] = "DRIVER_LIVENESS_UNAVAILABLE"
        report["rc"] = 2
        return report, 2
    try:
        with open(log_path, "r", encoding="utf-8", errors="surrogateescape") as f:
            text = f.read()
    except OSError:
        report["log"] = {"path": log_path, "state": "unreadable"}
        report["verdict"] = "DRIVER_LIVENESS_UNAVAILABLE"
        report["rc"] = 2
        return report, 2
    if text.strip() == "":
        report["log"] = {"path": log_path, "state": "empty"}
        report["verdict"] = "DRIVER_LIVENESS_UNAVAILABLE"
        report["rc"] = 2
        return report, 2
    lanes, shape = parse_log(text)
    try:
        mtime_age = now - os.stat(log_path).st_mtime
    except OSError:
        mtime_age = None
    shape["mtime_age_s"] = mtime_age
    shape["path"] = log_path
    report["log"] = shape
    for lane, row in lanes.items():
        if row["last_launch_ts"] is not None:
            row["last_launch_age_s"] = round(now - row["last_launch_ts"], 3)
        else:
            row["last_launch_age_s"] = None
    report["lanes"] = lanes
    report["state_dir"] = state_shapes(state_dir)
    report["verdict"] = "DRIVER_LIVENESS_OK"
    report["notes"] = [
        "in_flight/unclosed are log-shape facts, not health verdicts",
        "state *.round values are never read here; symlinks never followed",
        "lane-dead-no-report clears that round's open launches (a retry follows)",
    ]
    report["rc"] = 0
    return report, 0


# --------------------------------------------------------------------------
# selftest over frozen fixtures under .ufo/waves/round-56/fixtures/driver/
# --------------------------------------------------------------------------

def _fixture_dir():
    d = _repo_path(".ufo", "waves", "round-56", "fixtures", "driver")
    return d if os.path.isdir(d) else None


def _load_fixture(name):
    d = _fixture_dir()
    if d is None:
        return None
    log = os.path.join(d, name, "watchdog.log")
    state = os.path.join(d, name, "state")
    if not os.path.isfile(log):
        return None
    return log, state if os.path.isdir(state) else None


CASES = []


def case(fn):
    CASES.append(fn)
    return fn


@case
def t_hyaku_pairing():
    f = _load_fixture("hyaku-pairing")
    if not f:
        return None
    rep, rc = run(log_path=f[0], state_dir=f[1], now=1_800_000_000)
    lane = rep.get("lanes", {}).get("mori", {})
    return (rc == 0 and rep["verdict"] == "DRIVER_LIVENESS_OK" and lane.get("launches") == 1
            and lane.get("completes") == 1 and lane.get("in_flight") is False
            and lane.get("unclosed") == 0 and rep["log"]["malformed"] == 0)


@case
def t_attempt_rollover():
    f = _load_fixture("attempt-rollover")
    if not f:
        return None
    rep, rc = run(log_path=f[0], state_dir=f[1], now=1_800_000_000)
    lane = rep.get("lanes", {}).get("mori", {})
    return (rc == 0 and lane.get("deads") == 1 and lane.get("launches") == 2
            and lane.get("completes") == 1 and lane.get("in_flight") is False
            and lane.get("unclosed") == 0)


@case
def t_legacy_grammar():
    f = _load_fixture("legacy-grammar")
    if not f:
        return None
    rep, rc = run(log_path=f[0], state_dir=f[1], now=1_800_000_000)
    lane = rep.get("lanes", {}).get("mori", {})
    return (rc == 0 and lane.get("launches") == 1 and lane.get("completes") == 1
            and lane.get("in_flight") is False and rep["log"]["malformed"] == 0)


@case
def t_in_flight():
    f = _load_fixture("in-flight")
    if not f:
        return None
    rep, rc = run(log_path=f[0], state_dir=f[1], now=1_800_000_000)
    lane = rep.get("lanes", {}).get("mori", {})
    return (rc == 0 and lane.get("in_flight") is True and lane.get("unclosed") == 1
            and lane.get("last_launch_age_s") is not None)


@case
def t_malformed_refusal():
    f = _load_fixture("malformed")
    if not f:
        return None
    rep, rc = run(log_path=f[0], state_dir=f[1], now=1_800_000_000)
    return (rc == 0 and rep["log"]["malformed"] >= 3
            and len(rep["log"]["examples"]) <= 3
            and rep.get("lanes", {}).get("mori", {}).get("launches") == 1)


@case
def t_launch_fail_and_dead_legacy():
    f = _load_fixture("fails-and-dead")
    if not f:
        return None
    rep, rc = run(log_path=f[0], state_dir=f[1], now=1_800_000_000)
    lane = rep.get("lanes", {}).get("mori", {})
    return (rc == 0 and lane.get("launch_fails") == 1 and lane.get("deads") == 1
            and lane.get("in_flight") is False)


@case
def t_missing_log():
    rep, rc = run(log_path="/nonexistent/mori-driver-liveness-test.log", now=1_800_000_000)
    return rc == 2 and rep["verdict"] == "DRIVER_LIVENESS_UNAVAILABLE" and rep["log"]["state"] == "absent"


@case
def t_empty_log():
    import tempfile
    tmp = tempfile.mkdtemp(prefix="mori-driver-liveness-", dir=os.environ.get("TMPDIR") or None)
    p = os.path.join(tmp, "watchdog.log")
    with open(p, "w") as fh:
        fh.write("")
    rep, rc = run(log_path=p, now=1_800_000_000)
    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    return rc == 2 and rep["log"]["state"] == "empty"


@case
def t_state_shapes():
    f = _load_fixture("state-shapes")
    if not f:
        return None
    rep, rc = run(log_path=f[0], state_dir=f[1], now=1_800_000_000)
    s = rep.get("state_dir") or {}
    return (rc == 0 and s.get("regular") == 1 and s.get("symlink") == 1
            and s.get("dir") == 1 and "values" not in json.dumps(s))


@case
def t_two_lanes():
    f = _load_fixture("two-lanes")
    if not f:
        return None
    rep, rc = run(log_path=f[0], state_dir=f[1], now=1_800_000_000)
    lanes = rep.get("lanes", {})
    return (rc == 0 and set(lanes) == {"mori", "kake"}
            and lanes["mori"]["launches"] == 1 and lanes["kake"]["launches"] == 1
            and lanes["mori"]["in_flight"] is True and lanes["kake"]["in_flight"] is False)


@case
def t_variants():
    f = _load_fixture("variants")
    if not f:
        return None
    rep, rc = run(log_path=f[0], state_dir=f[1], now=1_800_000_000)
    lanes = rep.get("lanes", {})
    kagi, kengaku, kasegi = lanes.get("kagi", {}), lanes.get("kengaku", {}), lanes.get("kasegi", {})
    kama, kotoba = lanes.get("kama", {}), lanes.get("kotoba", {})
    return (rc == 0 and rep["log"]["malformed"] == 0 and rep["log"]["other_lines"] == 2
            and kagi.get("launches") == 1 and kagi.get("completes") == 1
            and kengaku.get("launches") == 1 and kengaku.get("completes") == 1
            and kasegi.get("launches") == 1 and kasegi.get("unclosed") == 1
            and kama.get("deads") == 1 and kama.get("launches") == 1
            and kama.get("in_flight") is True
            and kotoba.get("wraps") == 1 and kotoba.get("in_flight") is False
            and lanes.get("mado", {}).get("wraps") == 1)


@case
def t_other_lines_not_malformed():
    f = _load_fixture("malformed")
    if not f:
        return None
    rep, rc = run(log_path=f[0], state_dir=f[1], now=1_800_000_000)
    return (rc == 0 and rep["log"]["malformed"] == 5
            and rep["log"]["other_lines"] == 1
            and rep.get("lanes", {}).get("mori", {}).get("launches") == 1)


@case
def t_no_health_verdict():
    f = _load_fixture("in-flight")
    if not f:
        return None
    rep, rc = run(log_path=f[0], state_dir=f[1], now=1_800_000_000)
    blob = json.dumps(rep)
    return ("healthy" not in blob and "failed lane" not in blob and "unhealthy" not in blob
            and rep.get("verdict") in ("DRIVER_LIVENESS_OK", "DRIVER_LIVENESS_UNAVAILABLE"))


def selftest():
    passed = failed = skipped = 0
    fails = []
    for fn in CASES:
        try:
            ok = fn()
        except Exception as e:  # noqa: BLE001
            ok = False
            fails.append("%s:EXC:%s" % (fn.__name__, e))
        if ok is None:
            skipped += 1
            continue
        if ok:
            passed += 1
        else:
            failed += 1
            if fn.__name__ not in fails:
                fails.append(fn.__name__)
    line = "DRIVER_LIVENESS_SELFTEST pass=%d fail=%d skipped=%d" % (passed, failed, skipped)
    if fails:
        line += " failed=" + ",".join(fails)
    print(line)
    return 0 if failed == 0 else 1


def main(argv):
    ap = argparse.ArgumentParser(prog="mori-driver-liveness.py")
    ap.add_argument("--fleet-root", default=None)
    ap.add_argument("--log", dest="log_path", default=None)
    ap.add_argument("--state-dir", default=None)
    ap.add_argument("--now", type=float, default=None)
    ap.add_argument("--fixture", default=None)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.fixture:
        log_path = os.path.join(a.fixture, "watchdog.log")
        state_dir = os.path.join(a.fixture, "state")
        if not os.path.isdir(state_dir):
            state_dir = None
    else:
        root = a.fleet_root
        if root is None:
            root = os.path.dirname(_repo_path())
        log_path = a.log_path or os.path.join(root, ".ufo", "watchdog.log")
        state_dir = a.state_dir if a.state_dir is not None else os.path.join(root, ".ufo", "state")
    rep, rc = run(log_path=log_path, state_dir=state_dir, now=a.now)
    print(json.dumps(rep, indent=1, sort_keys=True))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
