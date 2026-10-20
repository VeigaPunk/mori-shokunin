#!/usr/bin/env python3
"""mori-seat-terminal.py — read-only terminal-status census of OMP seat transcripts.

Mori round 17 C1 coverage tool (contract C1 + Amendment A1 items 1-8,10).

For a sessions directory it walks regular ``*.jsonl`` transcript files (symlinks,
FIFOs and devices are never read), validates the bounded header record
``{"type": "session", "version": 3}`` from the first 4096 bytes, reads at most the
last ``--max-tail-bytes`` (default 524288), and classifies the LAST
``{"type": "message", "message": {...}}`` record visible in that tail. Classes:
completed, aborted, dead_rate_limit, dead_quota, dead_error_other, error_unsettled,
incomplete, unavailable.

Only selected message fields are read (role, stopReason, errorStatus, errorMessage
tokens and error code, completedAt/timestamp in ms epoch, provider, model) and only
derived scalars are emitted. errorMessage text, message content and usage are never
written to stdout. Detection and report only: nothing is edited, resumed or
re-routed.

Seat identity: ``key`` is the path relative to --sessions-dir without ``.jsonl``;
``seat`` is the file stem. Duplicate stems in different directories are separate
entries (counted in ``duplicate_stems``). Files directly in --sessions-dir whose
stem matches ``^\\d{4}-\\d\\d-\\d\\dT[\\d-]+Z_[0-9a-f-]+$`` are ``kind: "main"``;
they are emitted but excluded from ``totals``/``by_prefix``/
``by_provider_model`` and from the dead exit code, and counted in ``main_sessions``.

Settle window: a terminal assistant error whose ``completedAt``/``timestamp`` is
newer than scan time minus ``--settle-seconds`` (default 900) is ``error_unsettled``,
not dead. ``--now-ms`` overrides scan time. Dead classes therefore mean "the last
observed record is an error older than the settle window".

Output is exactly one JSON object on stdout, schema ``mori-seat-terminal-v1``, key
``finding_id``. Exit 0 = scan complete with zero dead_* among seats; 1 = scan
complete with at least one dead_* seat; 2 = setup/unavailable (including
``prefix-matched-none`` and any uncaught internal error).

Limits (also in --help): a terminal error is the LAST OBSERVED state, not proof the
session will never resume; dead counts are seats, not distinct incidents; prefixes
are naming conventions, not authenticated lane membership; main sessions are not
seats.

``--selftest`` builds synthetic transcripts under a temporary directory (the
``TMPDIR`` environment variable when set), runs this CLI as a real subprocess for
every arm, and asserts exit code, finding, per-seat class and tally shape.
Existence of --selftest is not permission to run it during a wave.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from collections import Counter

SCHEMA = "mori-seat-terminal-v1"
FINDING_OK = "MORI_SEAT_TERMINAL_OK"
FINDING_DEAD = "MORI_SEAT_TERMINAL_DEAD"
FINDING_SETUP = "MORI_SEAT_TERMINAL_SETUP"

CLASSES = (
    "completed",
    "aborted",
    "dead_rate_limit",
    "dead_quota",
    "dead_error_other",
    "error_unsettled",
    "incomplete",
    "unavailable",
)
DEAD_PREFIX = "dead_"

RATE_TOKENS = (
    "429",
    "rate_limit",
    "Rate limit",
    "rate limit",
    "RATE_LIMITED",
    "resource_exhausted",
)
QUOTA_TOKENS = ("quota", "usage limit", "402", "credits")
QUOTA_CODES = frozenset(("1113", "1308"))
RATE_CODES = frozenset(("1302",))
RETRY_EXHAUSTED_PREFIX = "Retry budget exhausted"

_RETRIES_RE = re.compile(r"after (\d+) retr(?:y|ies)")
_ERROR_CODE_RE = re.compile(r"\(type=(\d+)\)")
MAIN_STEM_RE = re.compile(r"^\d{4}-\d\d-\d\dT[\d-]+Z_[0-9a-f-]+$")

EXT = ".jsonl"
SUPPORTED_SCHEMA_VERSION = 3
HEAD_BYTES = 4096
DEFAULT_MAX_TAIL_BYTES = 524288
DEFAULT_MAX_FILES = 20000
DEFAULT_SETTLE_SECONDS = 900

_SCAN_KEYS = frozenset(
    (
        "schema",
        "finding_id",
        "sessions_dir",
        "files_scanned",
        "now_ms",
        "settle_seconds",
        "totals",
        "retry_exhausted",
        "main_sessions",
        "duplicate_stems",
        "by_prefix",
        "by_provider_model",
        "seats",
    )
)
_SEAT_KEYS = frozenset(
    (
        "seat",
        "key",
        "kind",
        "prefix",
        "class",
        "provider",
        "model",
        "error_status",
        "retry_exhausted",
        "retries",
        "error_code",
        "terminal_ms",
        "reason",
    )
)
_UNREADABLE_REASONS = frozenset(("schema", "no-message", "unreadable"))

LIMITS = (
    "A terminal error is the LAST OBSERVED state, not proof the session will "
    "never resume; a terminal error newer than the settle window is reported as "
    "error_unsettled. Dead counts are seats (transcript files), not distinct "
    "incidents. Prefixes are naming conventions, not authenticated lane "
    "membership. Main sessions are not seats. Message text, content and usage "
    "are never emitted."
)


class _SetupError(Exception):
    def __init__(self, reason, **extra):
        self.reason = reason
        self.extra = extra
        super().__init__(reason)


def _zero_totals():
    return {name: 0 for name in CLASSES}


def _emit(payload, rc):
    sys.stdout.write(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    )
    return rc


def _setup(reason, sessions_dir, **extra):
    payload = {
        "schema": SCHEMA,
        "finding_id": FINDING_SETUP,
        "reason": reason,
        "sessions_dir": sessions_dir,
    }
    payload.update(extra)
    return _emit(payload, 2)


def _int_arg(raw, name, minimum):
    try:
        value = int(raw)
    except (TypeError, ValueError):
        raise _SetupError("invalid-" + name)
    if value < minimum:
        raise _SetupError("invalid-" + name)
    return value


def _as_ms(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value == value:
        if value not in (float("inf"), float("-inf")):
            return int(value)
    return None


def _first_ms(*values):
    for value in values:
        parsed = _as_ms(value)
        if parsed is not None:
            return parsed
    return None


def _message_view(record):
    """Return the selected fields of a message record, or None to skip it."""
    if not isinstance(record, dict) or record.get("type") != "message":
        return None
    message = record.get("message")
    if not isinstance(message, dict):
        return None
    role = message.get("role")
    stop_reason = message.get("stopReason")
    error_status = message.get("errorStatus")
    error_message = message.get("errorMessage")
    provider = message.get("provider")
    model = message.get("model")
    if not isinstance(error_message, str):
        error_message = ""
    retries_match = _RETRIES_RE.search(error_message)
    code_match = _ERROR_CODE_RE.search(error_message)
    return {
        "role": role if isinstance(role, str) else None,
        "stop_reason": stop_reason if isinstance(stop_reason, str) else None,
        "error_status": (
            error_status
            if isinstance(error_status, int) and not isinstance(error_status, bool)
            else None
        ),
        "error_message": error_message,
        "provider": provider if isinstance(provider, str) else None,
        "model": model if isinstance(model, str) else None,
        "terminal_ms": _first_ms(
            message.get("completedAt"),
            message.get("timestamp"),
            record.get("completedAt"),
            record.get("timestamp"),
        ),
        "retries": int(retries_match.group(1)) if retries_match else None,
        "error_code": code_match.group(1) if code_match else None,
        "retry_exhausted": error_message.startswith(RETRY_EXHAUSTED_PREFIX),
    }


def _classify(view, now_ms, settle_seconds):
    role = view["role"]
    stop_reason = view["stop_reason"]
    error_message = view["error_message"]
    if role != "assistant":
        return "incomplete"
    if stop_reason == "stop":
        return "completed"
    if stop_reason == "aborted":
        return "aborted"
    if stop_reason != "error":
        return "incomplete"
    terminal_ms = view["terminal_ms"]
    if terminal_ms is not None and terminal_ms > now_ms - settle_seconds * 1000:
        return "error_unsettled"
    if view["error_status"] == 429 or any(
        token in error_message for token in RATE_TOKENS
    ):
        return "dead_rate_limit"
    error_code = view["error_code"]
    if error_code in QUOTA_CODES:
        return "dead_quota"
    if error_code in RATE_CODES:
        return "dead_rate_limit"
    if any(token in error_message for token in QUOTA_TOKENS):
        return "dead_quota"
    return "dead_error_other"


def _read_head(path):
    """Read at most the first HEAD_BYTES; None when the file is unreadable."""
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError:
        return None
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            return None
        chunks = []
        remaining = min(info.st_size, HEAD_BYTES)
        while remaining > 0:
            chunk = os.read(fd, remaining)
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        return b"".join(chunks)
    except OSError:
        return None
    finally:
        os.close(fd)


def _header_ok(head):
    """True only when the header record's version is the supported integer 3."""
    for line in head.split(b"\n"):
        try:
            record = json.loads(line.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            continue
        if isinstance(record, dict) and record.get("type") == "session":
            version = record.get("version")
            return (
                isinstance(version, int)
                and not isinstance(version, bool)
                and version == SUPPORTED_SCHEMA_VERSION
            )
    return False


def _read_tail(path, max_tail_bytes):
    """Read at most the last max_tail_bytes; None when the file is unreadable."""
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError:
        return None
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            return None
        size = info.st_size
        start = size - max_tail_bytes
        if start < 0:
            start = 0
        os.lseek(fd, start, os.SEEK_SET)
        chunks = []
        remaining = size - start
        while remaining > 0:
            chunk = os.read(fd, min(remaining, 1 << 20))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        data = b"".join(chunks)
    except OSError:
        return None
    finally:
        os.close(fd)
    if start > 0:
        newline = data.find(b"\n")
        data = data[newline + 1 :] if newline >= 0 else b""
    return data


def _terminal_view(data):
    """Last parseable message record in the tail, as a selected-field view."""
    last = None
    for line in data.split(b"\n"):
        try:
            record = json.loads(line.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            continue
        view = _message_view(record)
        if view is not None:
            last = view
    return last


def _seat_record(seat, key, kind, prefix, seat_class, reason, view):
    return {
        "seat": seat,
        "key": key,
        "kind": kind,
        "prefix": prefix,
        "class": seat_class,
        "provider": view["provider"] if view is not None else None,
        "model": view["model"] if view is not None else None,
        "error_status": view["error_status"] if view is not None else None,
        "retry_exhausted": view["retry_exhausted"] if view is not None else False,
        "retries": view["retries"] if view is not None else None,
        "error_code": view["error_code"] if view is not None else None,
        "terminal_ms": view["terminal_ms"] if view is not None else None,
        "reason": reason,
    }


def _provider_model_key(record):
    provider = record["provider"] if record["provider"] is not None else "unknown"
    model = record["model"] if record["model"] is not None else "unknown"
    return "%s/%s" % (provider, model)


def _analyze(path, max_tail_bytes, now_ms, settle_seconds):
    """Return (view, class, reason) for one transcript file."""
    head = _read_head(path)
    if head is None:
        return None, "unavailable", "unreadable"
    if not _header_ok(head):
        return None, "unavailable", "schema"
    data = _read_tail(path, max_tail_bytes)
    if data is None:
        return None, "unavailable", "unreadable"
    view = _terminal_view(data)
    if view is None:
        return None, "unavailable", "no-message"
    return view, _classify(view, now_ms, settle_seconds), None


def _scan(
    sessions_dir,
    prefixes,
    max_tail_bytes,
    max_files,
    now_ms,
    settle_seconds,
):
    if not os.path.isdir(sessions_dir):
        raise _SetupError("unavailable-dir")
    prefix_filter = set(prefixes)
    discovered = []
    for dirpath, dirnames, filenames in os.walk(sessions_dir, followlinks=False):
        dirnames.sort()
        filenames.sort()
        for name in filenames:
            if not name.endswith(EXT):
                continue
            path = os.path.join(dirpath, name)
            try:
                info = os.lstat(path)
            except OSError:
                continue
            if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
                continue
            discovered.append(path)
            if len(discovered) > max_files:
                raise _SetupError(
                    "too-many-files",
                    files_seen=len(discovered),
                    max_files=max_files,
                )

    records = []
    files_scanned = 0
    for path in discovered:
        relpath = os.path.relpath(path, sessions_dir)
        stem = os.path.basename(relpath)[: -len(EXT)]
        key = relpath[: -len(EXT)]
        direct = os.path.dirname(relpath) == ""
        kind = "main" if direct and MAIN_STEM_RE.match(stem) else "seat"
        prefix = stem.split(".", 1)[0]
        if kind == "seat" and prefix_filter and prefix not in prefix_filter:
            continue
        files_scanned += 1
        view, seat_class, reason = _analyze(
            path, max_tail_bytes, now_ms, settle_seconds
        )
        records.append(
            _seat_record(stem, key, kind, prefix, seat_class, reason, view)
        )

    seat_records = [record for record in records if record["kind"] == "seat"]
    if prefix_filter and not seat_records:
        raise _SetupError(
            "prefix-matched-none",
            prefixes=sorted(prefix_filter),
            files_scanned=files_scanned,
        )

    totals = _zero_totals()
    by_prefix = {}
    by_provider_model = {}
    retry_count = 0
    for record in seat_records:
        seat_class = record["class"]
        totals[seat_class] += 1
        by_prefix.setdefault(record["prefix"], _zero_totals())[seat_class] += 1
        key = _provider_model_key(record)
        by_provider_model.setdefault(key, _zero_totals())[seat_class] += 1
        if record["retry_exhausted"]:
            retry_count += 1

    stem_counts = Counter(record["seat"] for record in seat_records)
    duplicate_stems = sum(count - 1 for count in stem_counts.values() if count > 1)
    main_sessions = sum(1 for record in records if record["kind"] == "main")
    dead = any(record["class"].startswith(DEAD_PREFIX) for record in seat_records)

    records.sort(key=lambda record: record["key"])
    payload = {
        "schema": SCHEMA,
        "finding_id": FINDING_DEAD if dead else FINDING_OK,
        "sessions_dir": sessions_dir,
        "files_scanned": files_scanned,
        "now_ms": now_ms,
        "settle_seconds": settle_seconds,
        "totals": totals,
        "retry_exhausted": retry_count,
        "main_sessions": main_sessions,
        "duplicate_stems": duplicate_stems,
        "by_prefix": by_prefix,
        "by_provider_model": by_provider_model,
        "seats": records,
    }
    return payload, 1 if dead else 0


# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------

_SELFTEST_FAKE_TOKEN = "sk-SELFTEST-FAKE-TOKEN-9f3c2b7a"
_SELFTEST_SECRET_TEXT = "CREDENTIAL-SENTINEL-TEXT-4a7e"
_FORBIDDEN_MARKERS = (
    _SELFTEST_FAKE_TOKEN,
    _SELFTEST_SECRET_TEXT,
    "errorMessage",
    "credential_pin",
    '"content"',
    '"usage"',
)

_SELFTEST_NOW_MS = 1700000000000


def _msg(role, **fields):
    body = {"role": role}
    body.update(fields)
    return {"type": "message", "message": body}


def _materialize(path, content, with_header=True):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    if isinstance(content, bytes):
        with open(path, "wb") as handle:
            handle.write(content)
        return
    records = []
    if with_header:
        records.append({"type": "session", "version": SUPPORTED_SCHEMA_VERSION})
    records.extend(content)
    with open(path, "w", encoding="utf-8") as handle:
        for record in records:
            handle.write(
                json.dumps(record, ensure_ascii=True, separators=(",", ":")) + "\n"
            )


def _check_arm(tool, arm):
    name, cwd, args, want = arm
    errors = []
    proc = subprocess.run(
        [sys.executable, str(tool)] + list(args),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(cwd),
        timeout=180,
    )
    if proc.returncode != want["rc"]:
        errors.append("rc=%d want=%d" % (proc.returncode, want["rc"]))
    if proc.stderr:
        errors.append("stderr not empty (%d bytes)" % len(proc.stderr))
    text = proc.stdout.decode("utf-8", "replace")
    try:
        payload = json.loads(text)
    except ValueError:
        errors.append("stdout is not exactly one JSON document")
        return errors
    if not isinstance(payload, dict):
        errors.append("stdout JSON is not an object")
        return errors
    for index, marker in enumerate(_FORBIDDEN_MARKERS):
        if marker in text:
            errors.append("stdout echoes forbidden marker #%d" % index)
    if payload.get("schema") != SCHEMA:
        errors.append("schema=%r" % (payload.get("schema"),))
    if payload.get("finding_id") != want["finding_id"]:
        errors.append(
            "finding_id=%r want=%r"
            % (payload.get("finding_id"), want["finding_id"])
        )
    if "reason" in want and payload.get("reason") != want["reason"]:
        errors.append("reason=%r want=%r" % (payload.get("reason"), want["reason"]))
    if "seats" not in want:
        return errors

    if set(payload) != set(_SCAN_KEYS):
        errors.append("top-level keys=%r" % (sorted(payload),))
    if payload.get("now_ms") != want["now_ms"]:
        errors.append("now_ms=%r want=%r" % (payload.get("now_ms"), want["now_ms"]))
    if payload.get("settle_seconds") != want["settle_seconds"]:
        errors.append(
            "settle_seconds=%r want=%r"
            % (payload.get("settle_seconds"), want["settle_seconds"])
        )
    seats = payload.get("seats")
    if not isinstance(seats, list):
        errors.append("seats is not a list")
        return errors

    keys = []
    records = {}
    for record in seats:
        if not isinstance(record, dict):
            errors.append("seat entry is not an object")
            continue
        if set(record) != set(_SEAT_KEYS):
            errors.append("seat %r keys=%r" % (record.get("key"), sorted(record)))
            continue
        key = record.get("key")
        seat = record.get("seat")
        kind = record.get("kind")
        seat_class = record.get("class")
        reason = record.get("reason")
        if not isinstance(key, str) or not isinstance(seat, str):
            errors.append("key/seat is not a string")
            continue
        if kind not in ("seat", "main"):
            errors.append("key %r kind=%r" % (key, kind))
            continue
        if seat_class not in CLASSES:
            errors.append("key %r class=%r not a contract class" % (key, seat_class))
            continue
        if kind == "main":
            if "/" in key or MAIN_STEM_RE.match(seat) is None:
                errors.append("key %r kind=main but stem/pattern mismatch" % (key,))
        elif "/" not in key and MAIN_STEM_RE.match(seat) is not None:
            errors.append("key %r should be kind main" % (key,))
        if key.split("/")[-1] != seat:
            errors.append("key %r seat=%r mismatch" % (key, seat))
        if record.get("prefix") != seat.split(".", 1)[0]:
            errors.append("key %r prefix=%r" % (key, record.get("prefix")))
        if seat_class == "unavailable":
            if reason not in _UNREADABLE_REASONS:
                errors.append("key %r unavailable reason=%r" % (key, reason))
        elif reason is not None:
            errors.append("key %r class=%r reason=%r" % (key, seat_class, reason))
        if not isinstance(record.get("retry_exhausted"), bool):
            errors.append("key %r retry_exhausted is not bool" % (key,))
        for field in ("retries", "error_status", "terminal_ms"):
            value = record.get(field)
            if value is not None and (
                not isinstance(value, int) or isinstance(value, bool)
            ):
                errors.append("key %r %s is not int/null" % (key, field))
        for field in ("provider", "model", "error_code"):
            value = record.get(field)
            if value is not None and not isinstance(value, str):
                errors.append("key %r %s is not string/null" % (key, field))
        if key in records:
            errors.append("duplicate key %r" % (key,))
            continue
        keys.append(key)
        records[key] = record

    if keys != sorted(keys):
        errors.append("seats are not sorted by key")
    got_classes = {key: records[key]["class"] for key in records}
    want_seats = want["seats"]
    if got_classes != want_seats:
        errors.append("seat classes=%r want=%r" % (got_classes, want_seats))
    want_kinds = want.get("kinds", {})
    for key, kind in want_kinds.items():
        record = records.get(key)
        if record is None:
            errors.append("missing seat record %r" % (key,))
        elif record.get("kind") != kind:
            errors.append("key %r kind=%r want=%r" % (key, record.get("kind"), kind))
    for key, subset in want.get("records", {}).items():
        record = records.get(key)
        if record is None:
            errors.append("missing seat record %r" % (key,))
            continue
        for field, value in subset.items():
            if record.get(field) != value:
                errors.append(
                    "key %r field %s=%r want=%r"
                    % (key, field, record.get(field), value)
                )

    expected_totals = {name: 0 for name in CLASSES}
    for key, seat_class in want_seats.items():
        if want_kinds.get(key, "seat") == "seat":
            expected_totals[seat_class] += 1
    if payload.get("totals") != expected_totals:
        errors.append("totals=%r want=%r" % (payload.get("totals"), expected_totals))

    seat_records = [record for record in seats if record.get("kind") == "seat"]
    main_records = [record for record in seats if record.get("kind") == "main"]
    if payload.get("main_sessions") != want.get("main_sessions", 0):
        errors.append(
            "main_sessions=%r want=%r"
            % (payload.get("main_sessions"), want.get("main_sessions", 0))
        )
    if payload.get("main_sessions") != len(main_records):
        errors.append(
            "main_sessions=%r differs from main entries=%d"
            % (payload.get("main_sessions"), len(main_records))
        )
    stem_counts = Counter(record.get("seat") for record in seat_records)
    expected_duplicates = sum(
        count - 1 for count in stem_counts.values() if count > 1
    )
    if payload.get("duplicate_stems") != want.get("duplicate_stems", 0):
        errors.append(
            "duplicate_stems=%r want=%r"
            % (payload.get("duplicate_stems"), want.get("duplicate_stems", 0))
        )
    if payload.get("duplicate_stems") != expected_duplicates:
        errors.append(
            "duplicate_stems=%r recomputed=%d"
            % (payload.get("duplicate_stems"), expected_duplicates)
        )

    retry_top = payload.get("retry_exhausted")
    if isinstance(retry_top, bool) or not isinstance(retry_top, int):
        errors.append("top-level retry_exhausted is not an int seat count")
    else:
        expected_retry = sum(
            1 for record in seat_records if record.get("retry_exhausted") is True
        )
        if retry_top != expected_retry:
            errors.append(
                "retry_exhausted=%r want count=%d" % (retry_top, expected_retry)
            )

    expected_prefix = {}
    expected_pm = {}
    for record in seat_records:
        seat_class = record.get("class")
        if seat_class not in CLASSES:
            continue
        expected_prefix.setdefault(record.get("prefix"), _zero_totals())[
            seat_class
        ] += 1
        key = "%s/%s" % (
            record.get("provider") if record.get("provider") is not None else "unknown",
            record.get("model") if record.get("model") is not None else "unknown",
        )
        expected_pm.setdefault(key, _zero_totals())[seat_class] += 1
    if payload.get("by_prefix") != expected_prefix:
        errors.append(
            "by_prefix=%r want=%r" % (payload.get("by_prefix"), expected_prefix)
        )
    if payload.get("by_provider_model") != expected_pm:
        errors.append(
            "by_provider_model=%r want=%r"
            % (payload.get("by_provider_model"), expected_pm)
        )

    dead_present = any(
        record.get("class", "").startswith(DEAD_PREFIX) for record in seat_records
    )
    expected_finding = FINDING_DEAD if dead_present else FINDING_OK
    if payload.get("finding_id") != expected_finding:
        errors.append(
            "finding_id=%r disagrees with seat classes (%s)"
            % (payload.get("finding_id"), expected_finding)
        )
    if "files_scanned" in want and payload.get("files_scanned") != want["files_scanned"]:
        errors.append(
            "files_scanned=%r want=%r"
            % (payload.get("files_scanned"), want["files_scanned"])
        )
    return errors


def _selftest():
    tool = __file__
    root = tempfile.mkdtemp(prefix="mori-seat-terminal-selftest-")
    failures = []
    passed = 0
    arms = []

    try:

        def add(name, files, want, extra=(), with_header=True):
            arm_dir = os.path.join(root, name)
            sessions = os.path.join(arm_dir, "sessions")
            os.makedirs(sessions, exist_ok=True)
            for relpath, content in files:
                _materialize(
                    os.path.join(arm_dir, relpath),
                    content,
                    with_header=with_header,
                )
            if "seats" in want:
                want.setdefault("files_scanned", len(files))
                want.setdefault("now_ms", _SELFTEST_NOW_MS)
                want.setdefault("settle_seconds", DEFAULT_SETTLE_SECONDS)
                want.setdefault("main_sessions", 0)
                want.setdefault("duplicate_stems", 0)
            args = ["--sessions-dir", sessions] + list(extra)
            args += ["--now-ms", str(_SELFTEST_NOW_MS)]
            arms.append((name, arm_dir, args, want))

        add(
            "stop-completed",
            [
                (
                    "sessions/SeatA.One.jsonl",
                    [_msg("assistant", stopReason="stop", provider="zai", model="glm-5")],
                )
            ],
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {"SeatA.One": "completed"},
                "files_scanned": 1,
            },
        )

        add(
            "error-then-stop",
            [
                (
                    "sessions/Late.A.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            errorStatus=429,
                            errorMessage="rate_limit hit",
                            provider="zai",
                            model="glm-5",
                        ),
                        _msg("assistant", stopReason="stop", provider="zai", model="glm-5"),
                    ],
                )
            ],
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {"Late.A": "completed"},
                "files_scanned": 1,
            },
        )

        add(
            "retry-exhausted-429-zai",
            [
                (
                    "sessions/Zai.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            errorStatus=429,
                            errorMessage=(
                                "Retry budget exhausted after 10 retries: 429 Too Many "
                                "Requests (type=1302)"
                            ),
                            provider="zai",
                            model="glm-4.6",
                        )
                    ],
                )
            ],
            {
                "rc": 1,
                "finding_id": FINDING_DEAD,
                "seats": {"Zai.Seat": "dead_rate_limit"},
                "records": {
                    "Zai.Seat": {
                        "error_status": 429,
                        "retry_exhausted": True,
                        "retries": 10,
                        "error_code": "1302",
                        "provider": "zai",
                        "model": "glm-4.6",
                    }
                },
                "files_scanned": 1,
            },
        )

        add(
            "devin-resource-exhausted",
            [
                (
                    "sessions/Devin.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            errorMessage="resource_exhausted: upstream capacity",
                            provider="devin",
                            model="swe-1",
                        )
                    ],
                )
            ],
            {
                "rc": 1,
                "finding_id": FINDING_DEAD,
                "seats": {"Devin.Seat": "dead_rate_limit"},
                "records": {
                    "Devin.Seat": {
                        "error_status": None,
                        "retry_exhausted": False,
                        "retries": None,
                        "error_code": None,
                    }
                },
                "files_scanned": 1,
            },
        )

        add(
            "weekly-quota",
            [
                (
                    "sessions/Quota.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            errorMessage="weekly usage limit reached: quota 7/7 used",
                            provider="zai",
                            model="glm-4.6",
                        )
                    ],
                )
            ],
            {
                "rc": 1,
                "finding_id": FINDING_DEAD,
                "seats": {"Quota.Seat": "dead_quota"},
                "files_scanned": 1,
            },
        )

        add(
            "thinking-loop-error",
            [
                (
                    "sessions/Think.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            errorMessage="thinking loop detected; no progress",
                            provider="zai",
                            model="glm-4.6",
                        )
                    ],
                )
            ],
            {
                "rc": 1,
                "finding_id": FINDING_DEAD,
                "seats": {"Think.Seat": "dead_error_other"},
                "files_scanned": 1,
            },
        )

        add(
            "aborted",
            [
                (
                    "sessions/Abort.Seat.jsonl",
                    [_msg("assistant", stopReason="aborted", provider="p", model="m")],
                )
            ],
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {"Abort.Seat": "aborted"},
                "files_scanned": 1,
            },
        )

        add(
            "tooluse-terminal",
            [
                (
                    "sessions/ToolUse.Seat.jsonl",
                    [_msg("assistant", stopReason="toolUse", provider="p", model="m")],
                )
            ],
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {"ToolUse.Seat": "incomplete"},
                "files_scanned": 1,
            },
        )

        add(
            "toolresult-last",
            [
                (
                    "sessions/ToolResult.Seat.jsonl",
                    [
                        _msg("assistant", stopReason="toolUse", provider="p", model="m"),
                        _msg("toolResult", provider="p", model="m"),
                    ],
                )
            ],
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {"ToolResult.Seat": "incomplete"},
                "files_scanned": 1,
            },
        )

        add(
            "empty-file",
            [("sessions/Empty.Seat.jsonl", b"")],
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {"Empty.Seat": "unavailable"},
                "records": {"Empty.Seat": {"reason": "schema", "terminal_ms": None}},
                "files_scanned": 1,
            },
        )

        header_line = (
            json.dumps({"type": "session", "version": 3}, separators=(",", ":")).encode(
                "utf-8"
            )
            + b"\n"
        )
        malformed = (
            header_line
            + b"not json\n"
            + b"null\n"
            + b'{"type":"custom"}\n'
            + json.dumps(
                _msg("assistant", stopReason="stop", provider="p", model="m"),
                separators=(",", ":"),
            ).encode("utf-8")
            + b"\n{broken"
        )
        add(
            "malformed-lines",
            [("sessions/Malformed.Seat.jsonl", malformed)],
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {"Malformed.Seat": "completed"},
                "files_scanned": 1,
            },
        )

        add(
            "partial-first-line-after-tail-cut",
            [
                (
                    "sessions/Partial.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="aborted",
                            content="x" * 4096,
                            provider="p",
                            model="m",
                        ),
                        _msg("assistant", stopReason="stop", provider="p", model="m"),
                    ],
                )
            ],
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {"Partial.Seat": "completed"},
                "files_scanned": 1,
            },
            extra=("--max-tail-bytes", "512"),
        )

        add(
            "credential-pin-never-echoed",
            [
                (
                    "sessions/Cred.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="stop",
                            content=_SELFTEST_FAKE_TOKEN,
                            errorMessage=_SELFTEST_SECRET_TEXT,
                            usage={"cost": 9.5},
                            provider="p",
                            model="m",
                        ),
                        {
                            "type": "credential_pin",
                            "name": "fake",
                            "token": _SELFTEST_FAKE_TOKEN,
                            "credential": {"value": _SELFTEST_FAKE_TOKEN},
                        },
                        {"type": "session_init", "config": {"token": _SELFTEST_FAKE_TOKEN}},
                        {"type": "custom", "payload": _SELFTEST_SECRET_TEXT},
                    ],
                )
            ],
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {"Cred.Seat": "completed"},
                "files_scanned": 1,
            },
        )

        symlink_dir = os.path.join(root, "symlink-skipped")
        symlink_sessions = os.path.join(symlink_dir, "sessions")
        os.makedirs(symlink_sessions)
        outside = os.path.join(symlink_dir, "outside")
        os.makedirs(outside)
        _materialize(
            os.path.join(outside, "dead.jsonl"),
            [
                _msg(
                    "assistant",
                    stopReason="error",
                    errorMessage="quota exhausted",
                    provider="p",
                    model="m",
                )
            ],
        )
        os.symlink(
            os.path.join(outside, "dead.jsonl"),
            os.path.join(symlink_sessions, "LinkedSeat.X.jsonl"),
        )
        arms.append(
            (
                "symlink-skipped",
                symlink_dir,
                [
                    "--sessions-dir",
                    symlink_sessions,
                    "--now-ms",
                    str(_SELFTEST_NOW_MS),
                ],
                {
                    "rc": 0,
                    "finding_id": FINDING_OK,
                    "seats": {},
                    "files_scanned": 0,
                    "now_ms": _SELFTEST_NOW_MS,
                    "settle_seconds": DEFAULT_SETTLE_SECONDS,
                    "main_sessions": 0,
                    "duplicate_stems": 0,
                },
            )
        )

        prefix_files = [
            (
                "sessions/TameshiR17.X.jsonl",
                [
                    _msg(
                        "assistant",
                        stopReason="error",
                        errorMessage="weekly quota exhausted",
                        provider="zai",
                        model="glm-4.6",
                    )
                ],
            ),
            (
                "sessions/KamaR17.Y.jsonl",
                [_msg("assistant", stopReason="stop", provider="devin", model="swe-1")],
            ),
        ]
        add(
            "prefix-keep-kama",
            list(prefix_files),
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {"KamaR17.Y": "completed"},
                "files_scanned": 1,
            },
            extra=("--prefix", "KamaR17"),
        )
        add(
            "prefix-keep-tameshi",
            list(prefix_files),
            {
                "rc": 1,
                "finding_id": FINDING_DEAD,
                "seats": {"TameshiR17.X": "dead_quota"},
                "files_scanned": 1,
            },
            extra=("--prefix", "TameshiR17"),
        )

        add(
            "max-files-setup",
            [
                (
                    "sessions/One.Seat.jsonl",
                    [_msg("assistant", stopReason="stop", provider="p", model="m")],
                ),
                (
                    "sessions/Two.Seat.jsonl",
                    [_msg("assistant", stopReason="stop", provider="p", model="m")],
                ),
            ],
            {
                "rc": 2,
                "finding_id": FINDING_SETUP,
                "reason": "too-many-files",
            },
            extra=("--max-files", "1"),
        )

        unavailable_dir = os.path.join(root, "unavailable-dir")
        os.makedirs(unavailable_dir)
        arms.append(
            (
                "unavailable-dir",
                unavailable_dir,
                [
                    "--sessions-dir",
                    os.path.join(unavailable_dir, "missing"),
                    "--now-ms",
                    str(_SELFTEST_NOW_MS),
                ],
                {
                    "rc": 2,
                    "finding_id": FINDING_SETUP,
                    "reason": "unavailable-dir",
                },
            )
        )

        add(
            "message-beyond-tail",
            [
                (
                    "sessions/Beyond.Seat.jsonl",
                    [
                        _msg("assistant", stopReason="stop", provider="p", model="m"),
                        {"type": "custom", "pad": "y" * 4096},
                    ],
                )
            ],
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {"Beyond.Seat": "unavailable"},
                "records": {"Beyond.Seat": {"reason": "no-message"}},
                "files_scanned": 1,
            },
            extra=("--max-tail-bytes", "512"),
        )

        add(
            "invalid-max-tail-bytes",
            [
                (
                    "sessions/Args.Seat.jsonl",
                    [_msg("assistant", stopReason="stop", provider="p", model="m")],
                )
            ],
            {
                "rc": 2,
                "finding_id": FINDING_SETUP,
                "reason": "invalid-max-tail-bytes",
            },
            extra=("--max-tail-bytes", "0"),
        )

        add(
            "empty-sessions-dir",
            [],
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {},
                "files_scanned": 0,
            },
        )

        add(
            "non-object-message-skipped",
            [
                (
                    "sessions/NonObject.Seat.jsonl",
                    [{"type": "message", "message": "not-an-object"}],
                )
            ],
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {"NonObject.Seat": "unavailable"},
                "records": {"NonObject.Seat": {"reason": "no-message"}},
                "files_scanned": 1,
            },
        )

        # A1 item 1: quota tokens are tested before rate-limit.
        add(
            "a1-quota-token-before-429",
            [
                (
                    "sessions/A1Quota.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            errorStatus=429,
                            errorMessage="usage limit reached: quota exhausted",
                            provider="zai",
                            model="glm-4.6",
                        )
                    ],
                )
            ],
            {
                "rc": 1,
                "finding_id": FINDING_DEAD,
                "seats": {"A1Quota.Seat": "dead_quota"},
                "files_scanned": 1,
            },
        )

        # A1 item 10: error codes are tested before token tests.
        add(
            "a1-code-before-tokens",
            [
                (
                    "sessions/Code1113.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            errorStatus=429,
                            errorMessage="rate limit hit (type=1113)",
                            provider="zai",
                            model="glm-4.6",
                        )
                    ],
                ),
                (
                    "sessions/Code1308.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            errorStatus=429,
                            errorMessage="quota and rate_limit (type=1308)",
                            provider="zai",
                            model="glm-4.6",
                        )
                    ],
                ),
                (
                    "sessions/Code1302.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            errorStatus=429,
                            errorMessage="quota exceeded (type=1302)",
                            provider="zai",
                            model="glm-4.6",
                        )
                    ],
                ),
            ],
            {
                "rc": 1,
                "finding_id": FINDING_DEAD,
                "seats": {
                    "Code1113.Seat": "dead_quota",
                    "Code1308.Seat": "dead_quota",
                    "Code1302.Seat": "dead_rate_limit",
                },
                "records": {
                    "Code1113.Seat": {"error_code": "1113"},
                    "Code1308.Seat": {"error_code": "1308"},
                    "Code1302.Seat": {"error_code": "1302"},
                },
                "files_scanned": 3,
            },
        )

        # A1 item 2: settle window; timestamp fallback for one seat.
        add(
            "a1-settle-window",
            [
                (
                    "sessions/Fresh.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            errorStatus=429,
                            errorMessage="rate_limit",
                            timestamp=_SELFTEST_NOW_MS - 60000,
                            provider="zai",
                            model="glm-4.6",
                        )
                    ],
                ),
                (
                    "sessions/Stale.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            errorStatus=429,
                            errorMessage="rate_limit",
                            completedAt=_SELFTEST_NOW_MS - 1000000,
                            provider="zai",
                            model="glm-4.6",
                        )
                    ],
                ),
            ],
            {
                "rc": 1,
                "finding_id": FINDING_DEAD,
                "seats": {
                    "Fresh.Seat": "error_unsettled",
                    "Stale.Seat": "dead_rate_limit",
                },
                "records": {
                    "Fresh.Seat": {"terminal_ms": _SELFTEST_NOW_MS - 60000},
                    "Stale.Seat": {"terminal_ms": _SELFTEST_NOW_MS - 1000000},
                },
                "files_scanned": 2,
            },
        )

        # A1 item 3 (and 8): relative keys, duplicate stems, main exclusion.
        main_stem = "2026-10-20T15-00-00Z_abcdef12"
        add(
            "a1-keys-duplicates-main",
            [
                (
                    "sessions/a/Dup.Seat.jsonl",
                    [_msg("assistant", stopReason="stop", provider="zai", model="glm-5")],
                ),
                (
                    "sessions/b/Dup.Seat.jsonl",
                    [_msg("assistant", stopReason="stop", provider="zai", model="glm-5")],
                ),
                (
                    "sessions/Unique.Seat.jsonl",
                    [_msg("assistant", stopReason="stop", provider="zai", model="glm-5")],
                ),
                (
                    "sessions/%s.jsonl" % main_stem,
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            errorStatus=429,
                            errorMessage="rate_limit",
                            completedAt=_SELFTEST_NOW_MS - 1000000,
                            provider="zai",
                            model="glm-5",
                        )
                    ],
                ),
            ],
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {
                    "a/Dup.Seat": "completed",
                    "b/Dup.Seat": "completed",
                    "Unique.Seat": "completed",
                    main_stem: "dead_rate_limit",
                },
                "kinds": {main_stem: "main"},
                "records": {
                    "a/Dup.Seat": {"seat": "Dup.Seat", "kind": "seat"},
                    "b/Dup.Seat": {"seat": "Dup.Seat", "kind": "seat"},
                    main_stem: {"seat": main_stem, "kind": "main"},
                },
                "main_sessions": 1,
                "duplicate_stems": 1,
                "files_scanned": 4,
            },
        )

        # A1 item 4: a prefix that matches zero seats is never a clean scan.
        add(
            "a1-prefix-none",
            [
                (
                    "sessions/KamaR17.Y.jsonl",
                    [_msg("assistant", stopReason="stop", provider="devin", model="swe-1")],
                )
            ],
            {
                "rc": 2,
                "finding_id": FINDING_SETUP,
                "reason": "prefix-matched-none",
            },
            extra=("--prefix", "NomatchR17"),
        )

        # A1 item 5: only regular files; a FIFO is never opened.
        fifo_dir = os.path.join(root, "a1-fifo-skipped")
        fifo_sessions = os.path.join(fifo_dir, "sessions")
        os.makedirs(fifo_sessions)
        os.mkfifo(os.path.join(fifo_sessions, "Fifo.Seat.jsonl"))
        _materialize(
            os.path.join(fifo_sessions, "Real.Seat.jsonl"),
            [_msg("assistant", stopReason="stop", provider="p", model="m")],
        )
        arms.append(
            (
                "a1-fifo-skipped",
                fifo_dir,
                [
                    "--sessions-dir",
                    fifo_sessions,
                    "--now-ms",
                    str(_SELFTEST_NOW_MS),
                ],
                {
                    "rc": 0,
                    "finding_id": FINDING_OK,
                    "seats": {"Real.Seat": "completed"},
                    "files_scanned": 1,
                    "now_ms": _SELFTEST_NOW_MS,
                    "settle_seconds": DEFAULT_SETTLE_SECONDS,
                    "main_sessions": 0,
                    "duplicate_stems": 0,
                },
            )
        )

        # A1 item 5: an undecodable line is skipped, never a crash.
        undecodable = (
            header_line
            + b"\xff\xfe\n"
            + json.dumps(
                _msg("assistant", stopReason="stop", provider="p", model="m"),
                separators=(",", ":"),
            ).encode("utf-8")
            + b"\n"
        )
        add(
            "a1-undecodable-line",
            [("sessions/Undecodable.Seat.jsonl", undecodable)],
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {"Undecodable.Seat": "completed"},
                "files_scanned": 1,
            },
        )

        # A1 item 6: unsupported header version.
        add(
            "a1-schema-version-2",
            [
                (
                    "sessions/SchemaV2.Seat.jsonl",
                    [
                        {"type": "session", "version": 2},
                        _msg("assistant", stopReason="stop", provider="p", model="m"),
                    ],
                )
            ],
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {"SchemaV2.Seat": "unavailable"},
                "records": {"SchemaV2.Seat": {"reason": "schema"}},
                "files_scanned": 1,
            },
            with_header=False,
        )

        # A1 item 6: absent header.
        add(
            "a1-schema-absent",
            [
                (
                    "sessions/SchemaAbsent.Seat.jsonl",
                    [_msg("assistant", stopReason="stop", provider="p", model="m")],
                )
            ],
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {"SchemaAbsent.Seat": "unavailable"},
                "records": {"SchemaAbsent.Seat": {"reason": "schema"}},
                "files_scanned": 1,
            },
            with_header=False,
        )

        # A1 item 7: singular retry token and non-assistant terminal role.
        add(
            "a1-retry-singular-role",
            [
                (
                    "sessions/Singular.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            errorStatus=429,
                            errorMessage=(
                                "Retry budget exhausted after 1 retry: rate_limit"
                            ),
                            provider="zai",
                            model="glm-4.6",
                        )
                    ],
                ),
                (
                    "sessions/Developer.Seat.jsonl",
                    [
                        _msg(
                            "developer",
                            stopReason="error",
                            errorStatus=429,
                            errorMessage="rate_limit",
                            provider="p",
                            model="m",
                        )
                    ],
                ),
            ],
            {
                "rc": 1,
                "finding_id": FINDING_DEAD,
                "seats": {
                    "Singular.Seat": "dead_rate_limit",
                    "Developer.Seat": "incomplete",
                },
                "records": {
                    "Singular.Seat": {
                        "retries": 1,
                        "retry_exhausted": True,
                    },
                    "Developer.Seat": {"reason": None},
                },
                "files_scanned": 2,
            },
        )

        # A1 item 8: explicit output-shape arm (finding_id, new keys, key/kind/
        # terminal_ms/reason) with a single completed seat.
        add(
            "a1-output-shape",
            [
                (
                    "sessions/Shape.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="stop",
                            completedAt=_SELFTEST_NOW_MS - 5000,
                            provider="zai",
                            model="glm-5",
                        )
                    ],
                )
            ],
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {"Shape.Seat": "completed"},
                "records": {
                    "Shape.Seat": {
                        "key": "Shape.Seat",
                        "kind": "seat",
                        "prefix": "Shape",
                        "terminal_ms": _SELFTEST_NOW_MS - 5000,
                        "reason": None,
                    }
                },
                "files_scanned": 1,
            },
        )

        for arm in arms:
            errors = _check_arm(tool, arm)
            if errors:
                failures.append("arm %s: %s" % (arm[0], "; ".join(errors[:8])))
            else:
                passed += 1

        try:
            with open(tool, "rb") as handle:
                tool_sha256 = hashlib.sha256(handle.read()).hexdigest()
        except OSError:
            tool_sha256 = None

        if failures:
            return _emit(
                {
                    "finding_id": "SELFTEST_FAIL",
                    "schema": "mori-seat-terminal-selftest-v1",
                    "arms": len(arms),
                    "passed": passed,
                    "failures": failures,
                    "tool_sha256": tool_sha256,
                },
                1,
            )
        return _emit(
            {
                "finding_id": "SELFTEST_OK",
                "schema": "mori-seat-terminal-selftest-v1",
                "arms": len(arms),
                "passed": passed,
                "tool_sha256": tool_sha256,
            },
            0,
        )
    finally:
        shutil.rmtree(root, ignore_errors=True)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="mori-seat-terminal.py",
        description=(
            "Read-only terminal-status census of OMP seat transcripts (contract C1 "
            "+ Amendment A1). Walk a sessions directory for regular *.jsonl files "
            "(symlinks, FIFOs and devices never read), validate the first-4096-byte "
            "session header version 3, read at most the last --max-tail-bytes of "
            "each, classify the last message record with a settle window, and tally "
            "per seat-name prefix and per provider/model. " + LIMITS
        ),
        epilog=(
            "stdout carries exactly one JSON object (schema mori-seat-terminal-v1, "
            "key finding_id); errorMessage text, content and usage are never "
            "emitted. Exit 0 = scan complete with zero dead_* seats; 1 = scan "
            "complete with at least one dead_* seat; 2 = setup/unavailable, "
            "prefix-matched-none, or any internal error. --selftest builds "
            "synthetic transcripts under TMPDIR and runs this CLI as a subprocess; "
            "its existence is not permission to run it during a wave."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--sessions-dir",
        metavar="DIR",
        help="directory of OMP seat transcripts (*.jsonl, walked recursively)",
    )
    parser.add_argument(
        "--prefix",
        metavar="P",
        action="append",
        help="keep only seats whose prefix (text before the first '.') equals P; "
        "repeatable; matching zero seats is rc2 prefix-matched-none",
    )
    parser.add_argument(
        "--max-tail-bytes",
        metavar="N",
        default=str(DEFAULT_MAX_TAIL_BYTES),
        help="read at most the last N bytes of each file (default %d)"
        % DEFAULT_MAX_TAIL_BYTES,
    )
    parser.add_argument(
        "--max-files",
        metavar="N",
        default=str(DEFAULT_MAX_FILES),
        help="stop with rc2 MORI_SEAT_TERMINAL_SETUP reason=too-many-files above "
        "N regular transcript files (default %d)" % DEFAULT_MAX_FILES,
    )
    parser.add_argument(
        "--settle-seconds",
        metavar="N",
        default=str(DEFAULT_SETTLE_SECONDS),
        help="a terminal error newer than scan time minus N seconds is "
        "error_unsettled, not dead (default %d)" % DEFAULT_SETTLE_SECONDS,
    )
    parser.add_argument(
        "--now-ms",
        metavar="MS",
        default=None,
        help="override scan time in ms epoch (fixtures pin this)",
    )
    parser.add_argument(
        "--selftest",
        action="store_true",
        help="run the hermetic subprocess selftest; takes no scan arguments",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = _parse_args(argv)
    if args.selftest:
        if args.sessions_dir is not None or args.prefix:
            return _emit(
                {
                    "schema": SCHEMA,
                    "finding_id": FINDING_SETUP,
                    "reason": "selftest-takes-no-scan-args",
                    "sessions_dir": args.sessions_dir,
                },
                2,
            )
        return _selftest()
    if args.sessions_dir is None:
        return _setup("sessions-dir-required", None)
    try:
        max_tail_bytes = _int_arg(args.max_tail_bytes, "max-tail-bytes", 1)
        max_files = _int_arg(args.max_files, "max-files", 0)
        settle_seconds = _int_arg(args.settle_seconds, "settle-seconds", 0)
        if args.now_ms is None:
            now_ms = int(time.time() * 1000)
        else:
            now_ms = _int_arg(args.now_ms, "now-ms", 0)
        payload, rc = _scan(
            args.sessions_dir,
            args.prefix or [],
            max_tail_bytes,
            max_files,
            now_ms,
            settle_seconds,
        )
    except _SetupError as exc:
        return _setup(exc.reason, args.sessions_dir, **exc.extra)
    except Exception:
        return _setup("internal-error", args.sessions_dir)
    return _emit(payload, rc)


if __name__ == "__main__":
    sys.exit(main())
