#!/usr/bin/env python3
"""Read-only harness background-job runway survey (omp harness).

Round 25, claim C2 (coverage axis, new PROVINCE ground).  The omp harness
computes a per-session background-job cap from two sources: the configured
``async.maxJobs`` setting (``~/.omp/agent/config.yml``) and a clamp compiled
into the installed binary (``maxRunningJobs: () => Math.min(100, XPe.get(R))``).
No mori tool read that runway before this one.

Scope (contract C2 rules 1-7):

* ``--config PATH`` (default ``~/.omp/agent/config.yml``) and ``--binary PATH``
  (default: the real path of ``omp`` found on ``PATH``).
* The tool is read-only: it reads one config file and one binary, never runs
  ``omp``, never writes a settings file and never touches any other
  configuration surface (project-level or environment overrides are out of
  scope).  The only writes are the temporary files of ``--selftest``.
* Rule 1 ``configured``: a column-0 line exactly ``async:`` (optional trailing
  ``# comment``) opens a block that runs to the next non-blank, non-comment
  line at column 0.  Direct children sit at the indentation of the block's
  first non-blank, non-comment line; deeper lines are ignored.  A direct child
  ``maxJobs: <value>`` gives the value.  State ``set`` with the integer when the
  value is an unquoted decimal integer; ``malformed`` (value null) when the
  value is anything else, when ``maxJobs`` appears twice as a direct child, or
  when ``async:`` carries an inline value (for example
  ``async: {maxJobs: 50}``); ``absent`` when the file does not exist, has no
  ``async:`` line, or the block has no direct ``maxJobs``; ``unreadable`` when
  the path exists but cannot be read as a file (for example it is a directory).
  Keys under other top-level blocks never count.
* Rule 2 ``clamp``: every match in the binary bytes of
  ``maxRunningJobs:\\s*\\(\\)\\s*=>\\s*Math\\.min\\(\\s*(\\d+)\\s*,\\s*[\\w$]+\\.get\\([\\w$]+\\)\\s*\\)``.
  State ``found`` with the value when there is at least one match and all
  matches carry the same number (``sites`` = match count); ``ambiguous``
  (value null) when the numbers differ; ``absent`` (value null) when there is
  no match; ``unreadable`` when the binary cannot be read.  An absent clamp is
  never read as "no clamp".
* Rule 3 ``setting_default``: every match of
  ``id:\\s*"async\\.maxJobs",[^}]{0,300}?default:\\s*(\\d+)``.  Same states as
  the clamp.
* Rule 4 ``effective``: null unless the clamp is ``found`` and either
  configured is ``set``, or configured is ``absent`` and the default is
  ``found``.  Then base = configured value if ``set``, else the default value,
  and effective = max(1, min(clamp, base)).
* Rule 5 ``verdict`` / exit: effective null -> ``RUNWAY_UNKNOWN``, exit 2.
  Configured ``set`` and effective != configured -> ``RUNWAY_CLAMPED``, exit 1.
  Configured ``set`` and equal -> ``RUNWAY_AS_CONFIGURED``, exit 0.  Configured
  ``absent`` -> ``RUNWAY_DEFAULT``, exit 0.  Usage errors exit 2.
* Rule 6 output: one JSON object, ``schema: mori-job-runway-v1``,
  ``config_path``, ``binary_path``, ``binary_sha256`` (null when unreadable),
  ``configured {state, value}``, ``clamp {state, value, sites}``,
  ``setting_default {state, value, sites}``, ``effective``, ``verdict``.
* Rule 7 ``--selftest`` loads ``tools/fixtures/mori-job-runway/cases.json``
  (resolved from the script's own path), writes each case's ``config`` and
  ``binary`` into a fresh temporary directory (``config: null`` -> no file;
  ``config: {"dir": true}`` -> a directory at that path), runs the same
  evaluation, and compares the case's ``expect`` fields (only the keys present
  in ``expect``).  It prints ``MORI_JOB_RUNWAY_SELFTEST: PASS n/N`` (or
  ``FAIL n/N`` plus one line per failing case) and exits 0 only when all pass.

The live count of running background jobs is not readable from outside the
session and stays frontier: this tool reports the cap the binary computes, not
how many jobs run now.

Python 3 standard library only; read-only; safe under ``python3 -I -B``.
"""

from __future__ import annotations

import argparse
import errno
import hashlib
import json
import mmap
import os
import re
import shutil
import sys
import tempfile
from typing import Any, Dict, List, Optional, Tuple

SCHEMA = "mori-job-runway-v1"
SELFTEST_PREFIX = "MORI_JOB_RUNWAY_SELFTEST"

RC_OK = 0
RC_CLAMPED = 1
RC_UNKNOWN = 2

VERDICT_UNKNOWN = "RUNWAY_UNKNOWN"
VERDICT_CLAMPED = "RUNWAY_CLAMPED"
VERDICT_AS_CONFIGURED = "RUNWAY_AS_CONFIGURED"
VERDICT_DEFAULT = "RUNWAY_DEFAULT"

DEFAULT_CONFIG = os.path.join("~", ".omp", "agent", "config.yml")

# Rule 2: the compiled clamp site.
CLAMP_RE = re.compile(
    rb"maxRunningJobs:\s*\(\)\s*=>\s*Math\.min\(\s*(\d+)\s*,\s*[\w$]+\.get\([\w$]+\)\s*\)"
)
# Rule 3: the setting definition carrying its default.
DEFAULT_RE = re.compile(rb'id:\s*"async\.maxJobs",[^}]{0,300}?default:\s*(\d+)')

# Rule 1: line grammar of the config file.
ASYNC_PREFIX = "async:"
MAXJOBS_RE = re.compile(r"^maxJobs[ \t]*:")
INTEGER_RE = re.compile(r"^[+-]?[0-9]+$")


# --------------------------------------------------------------------------
# rule 1: configured
# --------------------------------------------------------------------------


def _strip_comment(text: str) -> str:
    """Drop a trailing ``# comment`` and surrounding blanks."""
    cut = text.find("#")
    if cut >= 0:
        text = text[:cut]
    return text.strip()


def _is_blank_or_comment(line: str) -> bool:
    stripped = line.strip()
    return stripped == "" or stripped.startswith("#")


def _indent_of(line: str) -> int:
    return len(line) - len(line.lstrip(" \t"))


def _read_config_text(path: str) -> Tuple[str, Optional[str]]:
    """Return ``(state, text)`` for the config file.

    ``state`` is ``"ok"``, ``"absent"`` (no such file) or ``"unreadable"``.
    """
    try:
        with open(path, "r", encoding="utf-8", errors="strict") as handle:
            return "ok", handle.read()
    except FileNotFoundError:
        return "absent", None
    except IsADirectoryError:
        return "unreadable", None
    except UnicodeDecodeError:
        return "unreadable", None
    except OSError as exc:
        if exc.errno == errno.ENOENT:
            return "absent", None
        return "unreadable", None


def _parse_config(text: str) -> Tuple[str, Optional[int]]:
    """Apply rule 1 to the config text; return ``(state, value)``."""
    lines = text.splitlines()

    async_index: Optional[int] = None
    inline_value = False
    for index, line in enumerate(lines):
        if not line.startswith(ASYNC_PREFIX):
            continue
        rest = line[len(ASYNC_PREFIX):].strip()
        if rest == "" or rest.startswith("#"):
            if async_index is None:
                async_index = index
        else:
            # `async:` carries an inline value (for example `async: {maxJobs: 50}`).
            inline_value = True

    if inline_value:
        return "malformed", None
    if async_index is None:
        return "absent", None

    # The block runs to the next non-blank, non-comment line at column 0.
    block: List[str] = []
    for line in lines[async_index + 1:]:
        if line[:1] not in ("", " ", "\t") and not _is_blank_or_comment(line):
            break
        block.append(line)

    child_indent: Optional[int] = None
    for line in block:
        if _is_blank_or_comment(line):
            continue
        child_indent = _indent_of(line)
        break
    if child_indent is None:
        return "absent", None

    values: List[str] = []
    for line in block:
        if _is_blank_or_comment(line):
            continue
        if _indent_of(line) != child_indent:
            # Deeper (or oddly indented) lines are not direct children.
            continue
        body = line.strip()
        if not MAXJOBS_RE.match(body):
            continue
        values.append(body.split(":", 1)[1])

    if not values:
        return "absent", None
    if len(values) > 1:
        return "malformed", None

    raw = _strip_comment(values[0])
    if raw == "" or not INTEGER_RE.match(raw):
        return "malformed", None
    return "set", int(raw)


def configured_state(path: str) -> Tuple[str, Optional[int]]:
    """Rule 1 over one config path."""
    state, text = _read_config_text(path)
    if state == "absent":
        return "absent", None
    if state == "unreadable":
        return "unreadable", None
    return _parse_config(text)  # type: ignore[arg-type]


# --------------------------------------------------------------------------
# rules 2 and 3: binary byte searches
# --------------------------------------------------------------------------


def _binary_sites(path: Optional[str], pattern: "re.Pattern[bytes]") -> Tuple[str, Optional[int], int]:
    """Return ``(state, value, sites)`` for one byte pattern.

    ``found`` (value, sites), ``ambiguous`` (null, sites), ``absent`` (null, 0)
    or ``unreadable`` (null, 0).
    """
    if path is None:
        return "unreadable", None, 0
    try:
        handle = open(path, "rb")
    except OSError:
        return "unreadable", None, 0
    try:
        size = os.fstat(handle.fileno()).st_size
        if size == 0:
            return "absent", None, 0
        try:
            with mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ) as mapped:
                numbers = [int(m.group(1)) for m in pattern.finditer(mapped)]
        except (ValueError, OSError):
            return "unreadable", None, 0
    finally:
        handle.close()

    if not numbers:
        return "absent", None, 0
    if len(set(numbers)) != 1:
        return "ambiguous", None, len(numbers)
    return "found", numbers[0], len(numbers)


def _sha256(path: Optional[str]) -> Optional[str]:
    if path is None:
        return None
    digest = hashlib.sha256()
    try:
        with open(path, "rb") as handle:
            while True:
                chunk = handle.read(1024 * 1024)
                if not chunk:
                    break
                digest.update(chunk)
    except OSError:
        return None
    return digest.hexdigest()


# --------------------------------------------------------------------------
# rules 4 to 6: evaluation and output
# --------------------------------------------------------------------------


def _effective(
    configured: Tuple[str, Optional[int]],
    clamp: Tuple[str, Optional[int], int],
    setting_default: Tuple[str, Optional[int], int],
) -> Optional[int]:
    configured_state_name, configured_value = configured
    clamp_state_name, clamp_value, _ = clamp
    default_state_name, default_value, _ = setting_default

    if clamp_state_name != "found" or clamp_value is None:
        return None
    if configured_state_name == "set":
        base = configured_value
    elif configured_state_name == "absent" and default_state_name == "found":
        base = default_value
    else:
        return None
    if base is None:
        return None
    return max(1, min(clamp_value, base))


def _verdict(
    configured: Tuple[str, Optional[int]],
    effective: Optional[int],
) -> Tuple[str, int]:
    configured_state_name, configured_value = configured
    if effective is None:
        return VERDICT_UNKNOWN, RC_UNKNOWN
    if configured_state_name == "set":
        if effective != configured_value:
            return VERDICT_CLAMPED, RC_CLAMPED
        return VERDICT_AS_CONFIGURED, RC_OK
    if configured_state_name == "absent":
        return VERDICT_DEFAULT, RC_OK
    return VERDICT_UNKNOWN, RC_UNKNOWN


def evaluate(config_path: str, binary_path: Optional[str]) -> Tuple[Dict[str, Any], int]:
    """Run rules 1-5 over one config path and one binary path."""
    configured = configured_state(config_path)
    clamp = _binary_sites(binary_path, CLAMP_RE)
    setting_default = _binary_sites(binary_path, DEFAULT_RE)
    effective = _effective(configured, clamp, setting_default)
    verdict, rc = _verdict(configured, effective)

    payload: Dict[str, Any] = {
        "schema": SCHEMA,
        "config_path": config_path,
        "binary_path": binary_path,
        "binary_sha256": _sha256(binary_path),
        "configured": {"state": configured[0], "value": configured[1]},
        "clamp": {"state": clamp[0], "value": clamp[1], "sites": clamp[2]},
        "setting_default": {
            "state": setting_default[0],
            "value": setting_default[1],
            "sites": setting_default[2],
        },
        "effective": effective,
        "verdict": verdict,
    }
    return payload, rc


# --------------------------------------------------------------------------
# rule 7: selftest
# --------------------------------------------------------------------------


def _cases_path() -> Optional[str]:
    script_dir = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
    for candidate in (
        os.path.join(script_dir, "fixtures", "mori-job-runway", "cases.json"),
        os.path.join(script_dir, "..", "tools", "fixtures", "mori-job-runway", "cases.json"),
    ):
        if os.path.isfile(candidate):
            return candidate
    return None


def _compare(expected: Any, actual: Any, path: str) -> List[str]:
    """Compare only the keys present in ``expected``."""
    problems: List[str] = []
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return ["%s: expected an object, got %r" % (path, actual)]
        for key, value in expected.items():
            child = "%s.%s" % (path, key) if path else key
            if key not in actual:
                problems.append("%s: missing from result" % child)
                continue
            problems.extend(_compare(value, actual[key], child))
        return problems
    if expected != actual:
        problems.append("%s: expected %r, got %r" % (path, expected, actual))
    return problems


def _materialize(case: Dict[str, Any], directory: str) -> Tuple[str, str]:
    """Write one case's config and binary into ``directory``."""
    config_path = os.path.join(directory, "config.yml")
    binary_path = os.path.join(directory, "omp.bin")

    config = case.get("config")
    if isinstance(config, dict) and config.get("dir"):
        os.mkdir(config_path)
    elif isinstance(config, str):
        with open(config_path, "w", encoding="utf-8") as handle:
            handle.write(config)

    binary = case.get("binary")
    if isinstance(binary, str):
        with open(binary_path, "w", encoding="utf-8") as handle:
            handle.write(binary)
    return config_path, binary_path


def _selftest() -> int:
    path = _cases_path()
    if path is None:
        print("%s: FAIL 0/0" % SELFTEST_PREFIX)
        print("CASES: fixtures/mori-job-runway/cases.json not found next to the script")
        return RC_UNKNOWN
    try:
        with open(path, "r", encoding="utf-8") as handle:
            document = json.load(handle)
    except (OSError, ValueError) as exc:
        print("%s: FAIL 0/0" % SELFTEST_PREFIX)
        print("CASES: cannot read %s: %s" % (path, exc))
        return RC_UNKNOWN

    cases = document.get("cases") or []
    total = len(cases)
    passed = 0
    failures: List[str] = []
    for case in cases:
        case_id = str(case.get("id", "?"))
        with tempfile.TemporaryDirectory(prefix="mori-job-runway-") as directory:
            config_path, binary_path = _materialize(case, directory)
            payload, rc = evaluate(config_path, binary_path)
        observed = dict(payload)
        observed["exit"] = rc
        expect = case.get("expect") or {}
        problems = _compare(expect, observed, "")
        if problems:
            failures.append("%s: %s" % (case_id, "; ".join(problems)))
        else:
            passed += 1

    if failures:
        print("%s: FAIL %d/%d" % (SELFTEST_PREFIX, passed, total))
        for line in failures:
            print("CASE %s" % line)
        return RC_UNKNOWN
    print("%s: PASS %d/%d" % (SELFTEST_PREFIX, passed, total))
    return RC_OK


# --------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------


class _UsageError(Exception):
    """A usage error (exit 2)."""


def _default_binary() -> Optional[str]:
    found = shutil.which("omp")
    if not found:
        return None
    return os.path.realpath(found)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mori-job-runway.py",
        description="Read-only survey of the omp harness background-job runway.",
    )
    parser.add_argument(
        "--config",
        default=DEFAULT_CONFIG,
        help="path of the omp agent config file (default: ~/.omp/agent/config.yml)",
    )
    parser.add_argument(
        "--binary",
        default=None,
        help="path of the installed omp binary (default: the real path of omp on PATH)",
    )
    parser.add_argument(
        "--selftest",
        action="store_true",
        help="run the frozen cases and print MORI_JOB_RUNWAY_SELFTEST: PASS n/N",
    )
    return parser


def _emit(payload: Dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, indent=2) + "\n")


def _emit_error(message: str) -> None:
    sys.stdout.write(
        json.dumps(
            {"schema": SCHEMA, "error": message, "verdict": VERDICT_UNKNOWN},
            indent=2,
        )
        + "\n"
    )


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    try:
        ns = parser.parse_args(argv)
    except _UsageError as exc:  # pragma: no cover - argparse exits first
        _emit_error(str(exc))
        return RC_UNKNOWN
    if ns.selftest:
        return _selftest()

    config_path = os.path.abspath(os.path.expanduser(ns.config))
    if ns.binary is None:
        binary_path = _default_binary()
    else:
        binary_path = os.path.abspath(os.path.expanduser(ns.binary))
    payload, rc = evaluate(config_path, binary_path)
    _emit(payload)
    return rc


if __name__ == "__main__":
    sys.exit(main())
