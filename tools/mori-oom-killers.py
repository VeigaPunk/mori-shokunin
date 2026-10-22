#!/usr/bin/env python3
"""Read-only survey of this host's userspace OOM killers (FR10).

Round 26, claim C2 (coverage axis, frontier FR10).  The tool reads what the
two userspace killers are set to do and whether they have acted.  It never
writes: the only outputs are stdout and stderr.  Python 3 standard library
only; runs under ``python3 -I -B``.

Modes (contract C2 of ``.ufo/waves/round-26/contract.md``):

* ``--inputs FILE`` -- run the pure reader on one JSON inputs object, print
  one JSON result object, exit with the verdict code.
* ``--selftest [--cases FILE]`` -- run every frozen case through the same pure
  reader.  The default cases path is resolved from the script location
  (``<script dir>/fixtures/mori-oom-killers/cases.json``).  A missing or empty
  cases file is a setup error (exit 2), never a silent fall-back.
* no arguments -- collect the inputs object live, then run the same pure
  reader.
* ``--dump-inputs`` -- print the live inputs object with every ``MESSAGE``
  redacted (see ``redact_inputs``).

Inputs object::

    {"earlyoom_show": "<systemctl show text>" | null,
     "oomd_show": "<systemctl show text>" | null,
     "earlyoom_journal": [{"MESSAGE": ..., "__MONOTONIC_TIMESTAMP": ...}] | null,
     "oomd_notices": <int> | null}

``null`` means the read failed.  The result object uses schema
``mori-oom-killers-v1``::

    {"schema": ..., "earlyoom": {...}, "oomd": {...}, "verdict": ...}

Privacy: the result never carries ``MESSAGE`` text, process names, command
lines, uids or the ``--avoid``/``--prefer`` expressions.  It holds states,
numbers, the version string and counts only.  ``--dump-inputs`` keeps the
``MESSAGE`` text only for the grammar lines that carry the version and the
thresholds; every other message is replaced by its grammar class name, so a
receipt can never carry a process name.

Message grammar (earlyoom ``v1.9.0``: ``main.c:161`` version line,
``main.c:414``/``main.c:416`` thresholds, ``main.c:519``/``main.c:523`` low
memory warnings, ``main.c:295`` dry-run flag, ``kill.c:627`` actions,
``kill.c:318`` escalation, ``kill.c:654`` failed kill), matched after
stripping leading whitespace and anchored at the start of the line.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SCHEMA = "mori-oom-killers-v1"

EARLYOOM_UNIT = "earlyoom.service"
OOMD_UNIT = "systemd-oomd.service"
OOMD_NOTICE_MESSAGE_ID = "d989611b15e44c9dbf31e3c81256e4ed"
SHOW_PROPERTIES = "LoadState,ActiveState,UnitFileState,ActiveEnterTimestampMonotonic"

VERIFIED_VERSION = "1.9.0"
GRAMMAR_VERIFIED = "verified-1.9.0"
GRAMMAR_UNVERIFIED = "unverified"

VERDICT_ACTED = "KILLER_ACTED"
VERDICT_UNKNOWN = "KILLERS_UNKNOWN"
VERDICT_QUIET = "KILLERS_QUIET"

EXIT_QUIET = 0
EXIT_ACTED = 1
EXIT_UNKNOWN = 2

EXIT_BY_VERDICT = {
    VERDICT_QUIET: EXIT_QUIET,
    VERDICT_ACTED: EXIT_ACTED,
    VERDICT_UNKNOWN: EXIT_UNKNOWN,
}

# Grammar classes.  The class name is what a redacted MESSAGE is replaced
# with; it never contains text taken from the message.
CLASS_VERSION = "version"
CLASS_TERM_THRESHOLDS = "term_thresholds"
CLASS_KILL_THRESHOLDS = "kill_thresholds"
CLASS_SIGTERM_ACTION = "sigterm_action"
CLASS_SIGKILL_ACTION = "sigkill_action"
CLASS_ESCALATION = "escalation"
CLASS_KILL_FAILED = "kill_failed"
CLASS_LOW_MEMORY_TERM = "low_memory_term"
CLASS_LOW_MEMORY_KILL = "low_memory_kill"
CLASS_DRYRUN = "dryrun"
CLASS_UNCLASSIFIED = "unclassified"

# Only these classes are free of process names, command lines and uids, so
# only their text survives a --dump-inputs redaction.
SAFE_CLASSES = frozenset({CLASS_VERSION, CLASS_TERM_THRESHOLDS, CLASS_KILL_THRESHOLDS})

_PCT = r"[0-9]+(?:\.[0-9]+)?"
RE_VERSION = re.compile(r"^earlyoom\s+(\S+)")
RE_TERM_THRESHOLDS = re.compile(
    r"^sending SIGTERM when mem avail <=\s*(" + _PCT + r")% and swap free <=\s*(" + _PCT + r")%"
)
RE_KILL_THRESHOLDS = re.compile(
    r"^SIGKILL when mem avail <=\s*(" + _PCT + r")% and swap free <=\s*(" + _PCT + r")%"
)
RE_SIGTERM_ACTION = re.compile(r"^sending SIGTERM to process ")
RE_SIGKILL_ACTION = re.compile(r"^sending SIGKILL to process ")

PREFIX_ESCALATION = "escalating to SIGKILL after "
PREFIX_KILL_FAILED = "kill failed: "
PREFIX_LOW_MEMORY_TERM = "low memory! at or below SIGTERM limits"
PREFIX_LOW_MEMORY_KILL = "low memory! at or below SIGKILL limits"
PREFIX_DRYRUN = "dryrun mode enabled"
# Post-freeze rules (contract amendment A2, round-26 wave-1 CriticC2Width):
# kill.c:282 at v1.9.0 — one send line under -g signals a whole process group.
PREFIX_PROCESS_GROUP = "killing whole process group "
# journald rate limiting (systemd v262 journald-manager.c:1294) — lines were lost.
PREFIX_SUPPRESSED = "Suppressed "
SUPPRESSED_MARK = " messages from " + "earlyoom.service"


class SetupError(Exception):
    """A setup problem: bad arguments, unreadable or empty cases file."""


# --------------------------------------------------------------------- grammar


def classify(message):
    """Return the grammar class name of one journal ``MESSAGE``."""
    if not isinstance(message, str):
        return CLASS_UNCLASSIFIED
    text = message.lstrip()
    if RE_VERSION.match(text):
        return CLASS_VERSION
    if RE_TERM_THRESHOLDS.match(text):
        return CLASS_TERM_THRESHOLDS
    if RE_KILL_THRESHOLDS.match(text):
        return CLASS_KILL_THRESHOLDS
    if RE_SIGTERM_ACTION.match(text):
        return CLASS_SIGTERM_ACTION
    if RE_SIGKILL_ACTION.match(text):
        return CLASS_SIGKILL_ACTION
    if text.startswith(PREFIX_ESCALATION):
        return CLASS_ESCALATION
    if text.startswith(PREFIX_KILL_FAILED):
        return CLASS_KILL_FAILED
    if text.startswith(PREFIX_LOW_MEMORY_TERM):
        return CLASS_LOW_MEMORY_TERM
    if text.startswith(PREFIX_LOW_MEMORY_KILL):
        return CLASS_LOW_MEMORY_KILL
    if text.startswith(PREFIX_DRYRUN):
        return CLASS_DRYRUN
    return CLASS_UNCLASSIFIED


def decode_message(value):
    """Decode one journal ``MESSAGE`` to text.

    A byte array is decoded as UTF-8 with replacement, as contracted.
    """
    if isinstance(value, str):
        return value
    if isinstance(value, (list, tuple)):
        try:
            return bytes(bytearray(int(b) & 0xFF for b in value)).decode("utf-8", "replace")
        except (TypeError, ValueError):
            return ""
    return ""


# ------------------------------------------------------------------- unit state


def parse_show(text):
    """Parse a ``systemctl show -p ...`` text into a property mapping."""
    props = {}
    if not isinstance(text, str):
        return props
    for line in text.splitlines():
        line = line.strip()
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        props[key.strip()] = value.strip()
    return props


def unit_state(text):
    """Map a show text to ``active``/``inactive``/``absent``/``unavailable``.

    ``unavailable`` covers both a failed read (``None``) and a show text that
    does not name ``ActiveState``; the two differ for the verdict only in the
    reason, which the verdict does not carry.
    """
    if not isinstance(text, str):
        return "unavailable"
    props = parse_show(text)
    if props.get("LoadState") == "not-found":
        return "absent"
    if "ActiveState" not in props:
        return "unavailable"
    if props["ActiveState"] == "active":
        return "active"
    if props["ActiveState"] == "inactive":
        return "inactive"
    # failed, activating, deactivating, reloading, maintenance, refreshing:
    # an earlier invocation may have acted and the current one is not
    # running steadily, so the state is not readable as active or inactive.
    return "unavailable"


def _monotonic_usec(value):
    """Parse a ``__MONOTONIC_TIMESTAMP`` (microseconds) value."""
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def _entry_text(entry):
    if not isinstance(entry, dict):
        return ""
    return decode_message(entry.get("MESSAGE"))


def _entry_timestamp(entry):
    if not isinstance(entry, dict):
        return None
    if "__MONOTONIC_TIMESTAMP" not in entry:
        return None
    return _monotonic_usec(entry.get("__MONOTONIC_TIMESTAMP"))


# ------------------------------------------------------------------- the reader


def read_inputs(inputs):
    """Pure reader: inputs object -> ``(result object, exit code)``.

    No side effects, no I/O: the same function backs ``--inputs``,
    ``--selftest`` and the live mode.
    """
    if not isinstance(inputs, dict):
        raise SetupError("inputs must be a JSON object")

    earlyoom_show = inputs.get("earlyoom_show")
    oomd_show = inputs.get("oomd_show")
    journal = inputs.get("earlyoom_journal")
    oomd_notices = inputs.get("oomd_notices")

    if not isinstance(earlyoom_show, str):
        earlyoom_show = None
    if not isinstance(oomd_show, str):
        oomd_show = None
    if journal is not None:
        if not isinstance(journal, list):
            journal = None
        else:
            journal = [e for e in journal if isinstance(e, dict)]
    if oomd_notices is not None:
        if isinstance(oomd_notices, bool) or not isinstance(oomd_notices, int):
            oomd_notices = None

    earlyoom_state = unit_state(earlyoom_show)
    oomd_state = unit_state(oomd_show)

    earlyoom_props = parse_show(earlyoom_show) if earlyoom_show is not None else {}

    # Scope: lines of the current earlyoom invocation, i.e. lines whose
    # monotonic timestamp is at or after ActiveEnterTimestampMonotonic.
    # Only an active unit has a current invocation.
    scoped = []
    scope_known = False
    if earlyoom_state == "active" and journal is not None:
        aetm = _monotonic_usec(earlyoom_props.get("ActiveEnterTimestampMonotonic"))
        if aetm is None or aetm == 0:
            # 0 means no active-enter transition recorded this boot
            # (org.freedesktop.systemd1(5)); like a missing value it cannot
            # bound the invocation.
            # The invocation cannot be bounded; keep every line of the boot as
            # a candidate (evidence is never dropped) but the scope stays
            # incomplete.
            scoped = list(journal)
        else:
            scope_known = True
            for entry in journal:
                stamp = _entry_timestamp(entry)
                if stamp is None:
                    # A record that cannot be placed in or out of the current
                    # invocation is malformed input: abstain (contract rule 4)
                    # rather than count a line that may belong to an earlier
                    # invocation (round-26 wave-1 case c35, supplementary file).
                    raise SetupError("journal record without a numeric __MONOTONIC_TIMESTAMP")
                if stamp >= aetm:
                    scoped.append(entry)

    version = None
    term_thresholds = None
    kill_thresholds = None
    counts = {
        "sigterm": 0,
        "sigkill": 0,
        "escalations": 0,
        "kill_failed": 0,
        "low_memory_warnings": 0,
    }
    dryrun = False
    process_group_lines = 0
    suppressed = False

    for entry in scoped:
        text = _entry_text(entry).lstrip()
        if not text:
            continue
        if RE_VERSION.match(text):
            version = RE_VERSION.match(text).group(1)
            continue
        match = RE_TERM_THRESHOLDS.match(text)
        if match:
            term_thresholds = (float(match.group(1)), float(match.group(2)))
            continue
        match = RE_KILL_THRESHOLDS.match(text)
        if match:
            kill_thresholds = (float(match.group(1)), float(match.group(2)))
            continue
        if RE_SIGTERM_ACTION.match(text):
            counts["sigterm"] += 1
        elif RE_SIGKILL_ACTION.match(text):
            counts["sigkill"] += 1
        elif text.startswith(PREFIX_ESCALATION):
            counts["escalations"] += 1
        elif text.startswith(PREFIX_KILL_FAILED):
            counts["kill_failed"] += 1
        elif text.startswith(PREFIX_LOW_MEMORY_TERM) or text.startswith(PREFIX_LOW_MEMORY_KILL):
            counts["low_memory_warnings"] += 1
        elif text.startswith(PREFIX_DRYRUN):
            dryrun = True
        elif text.startswith(PREFIX_PROCESS_GROUP):
            process_group_lines += 1
        elif text.startswith(PREFIX_SUPPRESSED) and SUPPRESSED_MARK in text:
            suppressed = True

    # A6: in dry-run mode earlyoom still prints "sending SIG… to process"
    # (kill.c:626-629) but sends nothing (kill.c:271-273); those lines are
    # reported separately and are never positive evidence.
    dryrun_send_lines = 0
    if dryrun:
        dryrun_send_lines = counts["sigterm"] + counts["sigkill"]
        counts["sigterm"] = 0
        counts["sigkill"] = 0

    # A1b: a journald "Suppressed N messages from earlyoom.service" notice in
    # scope means lines were lost, so the scope is not complete.
    scope_complete = scope_known and version is not None and not suppressed
    grammar = GRAMMAR_VERIFIED if version == VERIFIED_VERSION else GRAMMAR_UNVERIFIED

    thresholds = None
    if term_thresholds is not None and kill_thresholds is not None:
        thresholds = {
            "term_mem_pct": term_thresholds[0],
            "term_swap_pct": term_thresholds[1],
            "kill_mem_pct": kill_thresholds[0],
            "kill_swap_pct": kill_thresholds[1],
        }

    if earlyoom_state != "active":
        # No current invocation: no version, no thresholds, no action counts.
        # An inactive or absent killer reports actions: null (unavailable),
        # never zero counts.
        version = None
        grammar = GRAMMAR_UNVERIFIED
        thresholds = None
        scope_complete = False
        actions = None
        dryrun = False
    elif journal is None:
        # The journal read failed: the counts are unavailable, not zero.
        version = None
        grammar = GRAMMAR_UNVERIFIED
        thresholds = None
        scope_complete = False
        actions = None
        dryrun = False
    else:
        actions = dict(counts)
    if actions is None:
        dryrun_send_lines = None
        process_group_lines = None

    oomd = {
        "state": oomd_state,
        "notices_this_boot": oomd_notices,
    }

    acted = (
        (actions is not None and (actions["sigterm"] or actions["sigkill"] or actions["escalations"]))
        or (oomd_notices is not None and oomd_notices > 0)
    )

    unknown = False
    if not acted:
        # A needed read is null.
        if earlyoom_show is None:
            unknown = True
        if oomd_show is None:
            unknown = True
        if earlyoom_state == "active" and journal is None:
            unknown = True
        if oomd_state != "absent" and oomd_notices is None:
            unknown = True
        # A show text that lacks ActiveState.
        if earlyoom_state == "unavailable" or oomd_state == "unavailable":
            unknown = True
        # An active earlyoom with an incomplete scope or an unverified grammar.
        if earlyoom_state == "active" and not scope_complete:
            unknown = True
        if earlyoom_state == "active" and grammar == GRAMMAR_UNVERIFIED:
            unknown = True

    if acted:
        verdict = VERDICT_ACTED
    elif unknown:
        verdict = VERDICT_UNKNOWN
    else:
        verdict = VERDICT_QUIET

    result = {
        "schema": SCHEMA,
        "earlyoom": {
            "state": earlyoom_state,
            "version": version,
            "grammar": grammar,
            "thresholds": thresholds,
            "scope_complete": scope_complete,
            "actions": actions,
            "dryrun": dryrun,
            # Counts are earlyoom log lines, not processes signalled or killed.
            "dryrun_send_lines": dryrun_send_lines,
            "process_group_lines": process_group_lines,
        },
        "oomd": oomd,
        "verdict": verdict,
    }
    return result, EXIT_BY_VERDICT[verdict]


# --------------------------------------------------------------- live collection


def _run(argv):
    """Run one read-only command; return its stdout text or ``None``."""
    try:
        proc = subprocess.run(
            argv,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("utf-8", "replace")


def _collect_journal():
    out = _run(
        [
            "journalctl",
            "-q",
            "-b",
            "-u",
            EARLYOOM_UNIT,
            "-o",
            "json",
            "--output-fields=MESSAGE",
        ]
    )
    if out is None:
        return None
    entries = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        if not isinstance(obj, dict):
            continue
        entry = {}
        if "MESSAGE" in obj:
            entry["MESSAGE"] = obj["MESSAGE"]
        if "__MONOTONIC_TIMESTAMP" in obj:
            entry["__MONOTONIC_TIMESTAMP"] = obj["__MONOTONIC_TIMESTAMP"]
        entries.append(entry)
    return entries


def _collect_oomd_notices():
    out = _run(
        [
            "journalctl",
            "-q",
            "-b",
            "MESSAGE_ID=" + OOMD_NOTICE_MESSAGE_ID,
            "-o",
            "json",
            "--output-fields=MESSAGE_ID",
        ]
    )
    if out is None:
        return None
    return sum(1 for line in out.splitlines() if line.strip())


def _system_journal_readable():
    """A1c: `journalctl -q` hides "inaccessible system journal" warnings, so an
    empty answer can mean "not readable".  Require one PID 1 record this boot."""
    out = _run(["journalctl", "-q", "-b", "-n", "1", "_PID=1", "-o", "json", "--output-fields=_PID"])
    return out is not None and any(line.strip() for line in out.splitlines())


def collect_live():
    """Collect the inputs object from this host (read-only)."""
    readable = _system_journal_readable()
    return {
        "earlyoom_show": _run(["systemctl", "show", EARLYOOM_UNIT, "-p", SHOW_PROPERTIES]),
        "oomd_show": _run(["systemctl", "show", OOMD_UNIT, "-p", SHOW_PROPERTIES]),
        "earlyoom_journal": _collect_journal() if readable else None,
        "oomd_notices": _collect_oomd_notices() if readable else None,
    }


def redact_inputs(inputs):
    """Replace every ``MESSAGE`` that is not a version/threshold line with its
    grammar class name, so a receipt can never carry a process name."""
    if not isinstance(inputs, dict):
        return inputs
    journal = inputs.get("earlyoom_journal")
    if not isinstance(journal, list):
        return inputs
    redacted = []
    for entry in journal:
        if not isinstance(entry, dict):
            redacted.append(entry)
            continue
        item = dict(entry)
        if "MESSAGE" in item:
            klass = classify(decode_message(item["MESSAGE"]))
            if klass not in SAFE_CLASSES:
                item["MESSAGE"] = klass
        redacted.append(item)
    out = dict(inputs)
    out["earlyoom_journal"] = redacted
    return out


# ------------------------------------------------------------------- selftest


def default_cases_path():
    """The frozen cases file, resolved from the script location."""
    return Path(__file__).resolve().parent / "fixtures" / "mori-oom-killers" / "cases.json"


def _lookup(result, dotted):
    """Resolve a dotted path in the result object."""
    current = result
    for part in dotted.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return False, None
    return True, current


def _values_equal(actual, expected):
    """Compare one result value with one expected value."""
    if isinstance(expected, bool) or isinstance(actual, bool):
        return isinstance(expected, bool) and isinstance(actual, bool) and expected == actual
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        return float(actual) == float(expected)
    # A threshold written as the string "10.00" and the number 10.0 are the
    # same value; both spellings are accepted.
    if isinstance(actual, str) and isinstance(expected, (int, float)):
        try:
            return float(actual) == float(expected)
        except ValueError:
            return False
    if isinstance(expected, str) and isinstance(actual, (int, float)):
        try:
            return float(expected) == float(actual)
        except ValueError:
            return False
    return actual == expected


def run_selftest(cases_path):
    """Run every case through the pure reader; return the exit code."""
    try:
        raw = Path(cases_path).read_text(encoding="utf-8")
    except OSError as exc:
        raise SetupError("cannot read cases file {0}: {1}".format(cases_path, exc))
    if not raw.strip():
        raise SetupError("cases file {0} is empty".format(cases_path))
    try:
        data = json.loads(raw)
    except ValueError as exc:
        raise SetupError("cases file {0} is not valid JSON: {1}".format(cases_path, exc))
    if not isinstance(data, dict):
        raise SetupError("cases file {0} is not a JSON object".format(cases_path))
    if "schema" in data and data["schema"] != "mori-oom-killers-cases-v1":
        print(
            "mori-oom-killers: warning: unexpected cases schema {0!r}".format(data["schema"]),
            file=sys.stderr,
        )
    cases = data.get("cases")
    if not isinstance(cases, list):
        raise SetupError("cases file {0} has no 'cases' list".format(cases_path))
    if not cases:
        raise SetupError("cases file {0} has no cases".format(cases_path))

    passed = 0
    failures = []
    for index, case in enumerate(cases):
        case_id = "case-{0}".format(index)
        if isinstance(case, dict) and isinstance(case.get("id"), str):
            case_id = case["id"]
        problems = []
        if not isinstance(case, dict):
            failures.append((case_id, ["case is not a JSON object"]))
            continue
        inputs = case.get("inputs")
        expect = case.get("expect")
        if not isinstance(inputs, dict):
            problems.append("case has no 'inputs' object")
        if not isinstance(expect, dict):
            problems.append("case has no 'expect' object")
        if problems:
            failures.append((case_id, problems))
            continue
        try:
            result, code = read_inputs(inputs)
        except SetupError as exc:
            # Contract rule 4: a setup error is verdict KILLERS_UNKNOWN, exit 2,
            # with an error field; the case's expectations still apply.
            result, code = {"verdict": "KILLERS_UNKNOWN", "error": str(exc)}, 2
        if "verdict" in expect and result["verdict"] != expect["verdict"]:
            problems.append(
                "verdict: got {0!r} expected {1!r}".format(result["verdict"], expect["verdict"])
            )
        if "exit" in expect and code != expect["exit"]:
            problems.append("exit: got {0!r} expected {1!r}".format(code, expect["exit"]))
        fields = expect.get("fields")
        if fields is not None:
            if not isinstance(fields, dict):
                problems.append("expect.fields is not an object")
            else:
                for dotted in sorted(fields):
                    expected = fields[dotted]
                    found, actual = _lookup(result, dotted)
                    if not found:
                        problems.append(
                            "{0}: missing in result (expected {1})".format(
                                dotted, json.dumps(expected, sort_keys=True)
                            )
                        )
                    elif not _values_equal(actual, expected):
                        problems.append(
                            "{0}: got {1} expected {2}".format(
                                dotted,
                                json.dumps(actual, sort_keys=True),
                                json.dumps(expected, sort_keys=True),
                            )
                        )
        if problems:
            failures.append((case_id, problems))
        else:
            passed += 1

    total = len(cases)
    if passed == total and total > 0:
        print("MORI_OOM_KILLERS_SELFTEST: PASS {0}/{1}".format(passed, total))
        return 0
    print("MORI_OOM_KILLERS_SELFTEST: FAIL {0}/{1}".format(passed, total))
    for case_id, problems in failures:
        for problem in problems:
            print("FAIL {0}: {1}".format(case_id, problem))
    return 1


# --------------------------------------------------------------------- the CLI


def _build_parser():
    parser = argparse.ArgumentParser(
        prog="mori-oom-killers.py",
        description="Read-only survey of this host's userspace OOM killers.",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--inputs", metavar="FILE", help="run the pure reader on one JSON inputs object")
    group.add_argument(
        "--selftest",
        action="store_true",
        help="run the frozen cases through the same pure reader",
    )
    group.add_argument(
        "--dump-inputs",
        action="store_true",
        help="print the live inputs object with every MESSAGE redacted",
    )
    parser.add_argument(
        "--cases",
        metavar="FILE",
        help="cases file for --selftest (default: <script dir>/fixtures/mori-oom-killers/cases.json)",
    )
    return parser


def _emit_error(message):
    """Print a setup/internal error as a result object with verdict unknown."""
    result = {
        "schema": SCHEMA,
        "earlyoom": None,
        "oomd": None,
        "verdict": VERDICT_UNKNOWN,
        "error": message,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    print("mori-oom-killers: " + message, file=sys.stderr)


def _load_inputs(path):
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise SetupError("cannot read inputs file {0}: {1}".format(path, exc))
    try:
        data = json.loads(raw)
    except ValueError as exc:
        raise SetupError("inputs file {0} is not valid JSON: {1}".format(path, exc))
    if not isinstance(data, dict):
        raise SetupError("inputs file {0} is not a JSON object".format(path))
    return data


def main(argv):
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.selftest:
        cases_path = Path(args.cases) if args.cases else default_cases_path()
        return run_selftest(cases_path)

    if args.dump_inputs:
        inputs = collect_live()
        print(json.dumps(redact_inputs(inputs), indent=2, sort_keys=True))
        return EXIT_QUIET

    if args.inputs:
        inputs = _load_inputs(args.inputs)
    else:
        inputs = collect_live()

    result, code = read_inputs(inputs)
    print(json.dumps(result, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except SetupError as exc:
        _emit_error(str(exc))
        sys.exit(EXIT_UNKNOWN)
    except SystemExit:
        raise
    except Exception as exc:  # never exit 1 on an uncaught exception
        _emit_error("internal error: {0}: {1}".format(type(exc).__name__, exc))
        sys.exit(EXIT_UNKNOWN)
