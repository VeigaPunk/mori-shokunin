#!/usr/bin/env python3
"""Wave-settlement results-file scanner (round 59, C2 — depth/coverage capability).

Reads one or more orchestrator `<wave>-results.json` files (the inline spawn
handoff's settlement artifact: written beside `<wave>-dispatch.json` when every
seat of the wave settles, per the round-59 contract) and validates each as a
`ufo-wave-results` object:

  top-level: object; `lane` nonempty str; `round` int >= 1; `wave` nonempty
  str; `seats` int == len(`results`); `results` a list.
  member entry: object with exactly the keys {name, agent, output, note};
  `name` nonempty str, unique inside the file; `agent` one of the ten frozen
  swarm roles; `output` str or null; `note` free (null observed everywhere).

Prints one `mori-settlement-scan-v1` JSON object:
  {schema, verdict, files:[{path, lane, round, wave, seats, members,
    empty_output, notes_nonnull, duplicates, role_counts}] , failures:[{path,
    reasons}]}
verdict SETTLEMENT_SCAN_OK iff every file validates; SETTLEMENT_SCAN_FAIL and
exit 1 otherwise; usage/setup exit 2.  A zero-file invocation exits 1
(nothing scanned is not a scan).

Usage:
  mori-settlement-scan.py <file> [<file> ...]
  mori-settlement-scan.py --selftest [--scratch DIR]

Selftest builds fixture result files under DIR (default:
TMPDIR/mori-settlement-scan*) and prints `SETSCAN_SELFTEST pass=N fail=0`.
Read-only: opens inputs read-only; writes only inside the selftest root.
"""
import json
import os
import sys
import tempfile
from collections import Counter
from pathlib import Path

SCHEMA = "mori-settlement-scan-v1"
ROLES = ("scout", "reviewer", "critic", "connector", "sentinel", "executor",
         "mutation-tester", "revenger", "simplifier", "scribe")
MEMBER_KEYS = {"name", "agent", "output", "note"}


def scan_file(path):
    """Return (summary, failures)."""
    fails = []
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except OSError:
        return None, [{"path": str(path), "reasons": ["unreadable"]}]
    try:
        d = json.loads(raw)
    except ValueError:
        return None, [{"path": str(path), "reasons": ["not_json"]}]
    if not isinstance(d, dict):
        return None, [{"path": str(path), "reasons": ["top_not_object"]}]
    results = d.get("results")
    if not isinstance(results, list):
        fails.append("results_not_list")
        results = []
    seats = d.get("seats")
    if not isinstance(seats, int) or seats != len(results):
        fails.append("seats_mismatch")
    for k in ("lane", "wave"):
        if not isinstance(d.get(k), str) or not d[k]:
            fails.append("%s_bad" % k)
    if not isinstance(d.get("round"), int) or d["round"] < 1:
        fails.append("round_bad")
    names = []
    empties = 0
    notes = 0
    role_counts = Counter()
    for i, m in enumerate(results):
        tag = "member[%d]" % i
        if not isinstance(m, dict):
            fails.append(tag + ":not_object")
            continue
        extra = set(m) - MEMBER_KEYS
        missing = MEMBER_KEYS - set(m)
        if extra:
            fails.append(tag + ":extra_keys=%s" % ",".join(sorted(extra)))
        if missing:
            fails.append(tag + ":missing_keys=%s" % ",".join(sorted(missing)))
            continue
        if not isinstance(m["name"], str) or not m["name"]:
            fails.append(tag + ":name_bad")
        else:
            names.append(m["name"])
        if m["agent"] not in ROLES:
            fails.append(tag + ":agent_bad=%r" % m["agent"])
        else:
            role_counts[m["agent"]] += 1
        if m["output"] is None:
            empties += 1
        elif not isinstance(m["output"], str):
            fails.append(tag + ":output_bad")
        elif not m["output"]:
            empties += 1
        if m["note"] is not None:
            notes += 1
    dups = sorted(n for n, c in Counter(names).items() if c > 1)
    if dups:
        fails.append("duplicate_names=%s" % ",".join(dups))
    summary = {"path": str(path), "lane": d.get("lane"),
               "round": d.get("round"), "wave": d.get("wave"),
               "seats": d.get("seats"), "members": len(results),
               "empty_output": empties, "notes_nonnull": notes,
               "duplicates": dups,
               "role_counts": dict(sorted(role_counts.items()))}
    return summary, ([{"path": str(path), "reasons": fails}] if fails else [])


def scan(paths):
    files = []
    failures = []
    for p in paths:
        s, f = scan_file(p)
        if s is not None:
            files.append(s)
        failures.extend(f)
    out = {"schema": SCHEMA,
           "verdict": "SETTLEMENT_SCAN_OK" if (files and not failures)
           else "SETTLEMENT_SCAN_FAIL",
           "files": files, "failures": failures}
    print(json.dumps(out, sort_keys=True))
    return 0 if (files and not failures) else 1


def selftest(scratch=None):
    base = Path(scratch or tempfile.mkdtemp(prefix="mori-settlement-scan-",
                                            dir=os.environ.get("TMPDIR") or None))
    base.mkdir(parents=True, exist_ok=True)
    passed = failed = 0

    def write(name, obj):
        f = base / (name + ".json")
        f.write_text(obj if isinstance(obj, str) else json.dumps(obj))
        return f

    def member(name, agent="reviewer", output="x", note=None, extra=None):
        m = {"name": name, "agent": agent, "output": output, "note": note}
        if extra:
            m.update(extra)
        return m

    def results(n=2, **kw):
        return {"lane": "mori", "round": 59, "wave": "w1", "seats": n,
                "results": [member("S%d" % i) for i in range(n)]} | kw

    def case(name, paths, want_rc, want=None):
        nonlocal passed, failed
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = scan([str(p) for p in paths])
        out = json.loads(buf.getvalue())
        good = (rc == want_rc)
        if want == "has_failure" and not out["failures"]:
            good = False
        if good:
            passed += 1
        else:
            failed += 1
            print("FAIL %s rc=%s out=%s" % (name, rc, out), file=sys.stderr)

    good = write("good", results(3))
    case("met", [good], 0)
    bad_seats = write("bad_seats", results(2, seats=5))
    case("seats_mismatch", [bad_seats], 1, "has_failure")
    dup = write("dup", {"lane": "mori", "round": 59, "wave": "w1", "seats": 2,
                        "results": [member("A"), member("A")]})
    case("dup_name", [dup], 1, "has_failure")
    extra = write("extra", {"lane": "mori", "round": 59, "wave": "w1", "seats": 1,
                            "results": [member("A", extra={"status": "x"})]})
    case("extra_key", [extra], 1, "has_failure")
    missing = write("missing", {"lane": "mori", "round": 59, "wave": "w1", "seats": 1,
                                "results": [{"name": "A", "agent": "reviewer",
                                             "output": "x"}]})
    case("missing_key", [missing], 1, "has_failure")
    badrole = write("badrole", {"lane": "mori", "round": 59, "wave": "w1", "seats": 1,
                                "results": [member("A", agent="planner")]})
    case("agent_bad", [badrole], 1, "has_failure")
    notjson = write("notjson", "{no")
    case("not_json", [notjson], 1, "has_failure")
    toplist = write("toplist", [1, 2])
    case("top_not_object", [toplist], 1, "has_failure")
    case("empty_args", [], 1)
    case("mixed", [good, bad_seats], 1, "has_failure")
    line = "SETSCAN_SELFTEST pass=%d fail=%d" % (passed, failed)
    print(line)
    return 0 if failed == 0 else 1


def main(argv):
    if "--selftest" in argv:
        i = argv.index("--scratch") if "--scratch" in argv else -1
        scratch = argv[i + 1] if 0 <= i < len(argv) - 1 else None
        return selftest(scratch)
    args = [a for a in argv if not a.startswith("--")]
    return scan(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
