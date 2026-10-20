#!/usr/bin/env python3
"""mori-seat-terminal.py — read-only terminal-status census of OMP seat transcripts.

Mori round 17 C1 coverage tool (contract C1, Amendment A1 items 1-8/10, and the
wave-2 PrivacyFinal hardening).

For a sessions directory it walks regular ``*.jsonl`` transcript files (symlinks,
FIFOs and devices are never read), validates the bounded header record
``{"type": "session", "version": 3}`` from the first 4096 bytes, reads at most the
last ``--max-tail-bytes`` (default 524288) from the same descriptor, and classifies
the LAST ``{"type": "message", "message": {...}}`` record visible in that tail.
Classes: completed, aborted, dead_rate_limit, dead_quota, dead_error_other,
error_unsettled, incomplete, unavailable.

Filesystem safety: a symlinked ``--sessions-dir`` (including a trailing-separator
spelling) is rejected with rc2; the sessions root is opened once with
``O_DIRECTORY|O_NOFOLLOW`` and the walk is descriptor-relative, opening every
child directory with ``O_NOFOLLOW`` relative to its parent descriptor, so a
swapped symlink ancestor cannot redirect the walk or a later read. Directory-walk
errors and ``lstat`` failures are fatal rc2 setup instead of a silently partial
clean scan; files are opened with ``O_NOFOLLOW|O_NONBLOCK`` and the opened
descriptor must be a regular file, so a regular-to-FIFO replacement cannot block
the scan. One descriptor supplies both the header and the tail, so the type check
covers the bytes actually read. The caller-selected root pathname itself is
resolved once and only its final component is O_NOFOLLOW-checked; ancestor
components above that pathname are caller scope. Every descendant component is
opened relative to a held descriptor with O_NOFOLLOW.

PERMITTED INPUT SET (decoded field projection)

  The record projector decodes exactly: top-level ``type``; top-level
  ``completedAt``/``timestamp`` when numeric; message ``role``, ``stopReason``,
  ``errorStatus``, ``completedAt``, ``timestamp``, ``provider``, ``model``; and
  from message ``errorMessage`` only derived metadata — retry-exhausted prefix
  boolean, ``after N retr(y|ies)`` count, ``(type=NNNN)`` digit string, and
  presence of the contract's literal quota/rate tokens. The header projector
  decodes only ``type`` and ``version``. Every other member (content, usage,
  credential_pin payloads, provider-specific blobs, anything else) is skipped
  structurally in place: its bytes are traversed for JSON structure but never
  decoded, copied into a view, or emitted. ``errorMessage`` is stream-decoded
  through its JSON escapes with a bounded carry window so escaped spellings of
  the approved ASCII tokens/codes are recognized, while the decoded text is
  never materialized; non-ASCII code points break token continuity. Complete
  numeric ``(type=...)`` codes are retained within the configured input-span
  bound; they are never converted to unbounded-size integers.

  Syntax is strict: strings validate JSON escape forms and UTF-8, numbers
  validate the complete JSON number grammar, and schema version, status, and
  epoch-millisecond fields accept integer-form numbers only (no float
  truncation). Lines whose structure, escapes, numbers or trailing bytes do not
  match are skipped. Approved string values are length-bounded (key/type 64,
  role/stopReason 256, provider/model 512, error code/retry count digits 12,
  numeric spans 32 bytes); values beyond the bound are ignored.

  The ``(type=...)`` business-code classification is Z.AI-specific: it is applied
  only when the terminal record's provider is exactly ``zai``. It is an observed
  classification hint, not an authenticated vendor cause.

Seat identity: ``key`` is the path relative to --sessions-dir without ``.jsonl``;
``seat`` is the file stem. Duplicate stems in different directories are separate
entries (counted in ``duplicate_stems``). Files directly in --sessions-dir whose
stem matches ``^\\d{4}-\\d\\d-\\d\\dT[\\d-]+Z_[0-9a-f-]+$`` are ``kind: "main"``;
they are emitted but excluded from ``totals``/``by_prefix``/
``by_provider_model`` and from the dead exit code, and counted in ``main_sessions``.

Settle window: a terminal assistant error whose ``completedAt``/``timestamp`` is
newer than scan time minus ``--settle-seconds`` (default 900) is ``error_unsettled``,
not dead. ``--now-ms`` overrides scan time. Dead classes therefore mean "the last
observed record is an error older than the settle window". An assistant error
with no usable numeric timestamp is ``unavailable`` with reason ``terminal-time``:
its age is unproven, so it is neither dead nor recent.

The ``(type=...)`` code table is Z.AI-only and scoped: 1113/1308 map to
dead_quota and 1302 maps to dead_rate_limit when the terminal provider is exactly
``zai``. An unmapped Z.AI code is not treated as rate evidence from HTTP 429
alone (explicit quota/rate text still classifies), and codes are ignored for
other providers. This is an observed classification hint, not an authenticated
vendor cause and not a full vendor code table.

Output is exactly one JSON object on stdout, schema ``mori-seat-terminal-v1``, key
``finding_id``. Exit 0 = scan complete with zero dead_* among seats; 1 = scan
complete with at least one dead_* seat; 2 = setup/unavailable (including
``prefix-matched-none``, ``root-symlink``, ``walk-error``, ``lstat-failed`` and
any uncaught internal error).

Limits (also in --help): a terminal error is the LAST OBSERVED state, not proof the
session will never resume; dead counts are seats, not distinct incidents; prefixes
are naming conventions, not authenticated lane membership; main sessions are not
seats.

``--selftest`` builds synthetic transcripts under a temporary directory (the
``TMPDIR`` environment variable when set), runs this CLI as a real subprocess for
every subprocess arm, and runs two direct safety arms. Existence of --selftest is
not permission to run it during a wave.
"""

import argparse
import errno
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import threading
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

# Contract token set. Bare "resource_exhausted" is NOT rate evidence (it can be
# quota or generic resource pressure); explicit status/rate spells still match.
RATE_TOKENS = (
    "429",
    "rate_limit",
    "Rate limit",
    "rate limit",
    "RATE_LIMITED",
)
RATE_TOKEN_BYTES = tuple(token.encode("ascii") for token in RATE_TOKENS)
QUOTA_TOKENS = ("quota", "usage limit", "402", "credits")
QUOTA_TOKEN_BYTES = tuple(token.encode("ascii") for token in QUOTA_TOKENS)
QUOTA_CODES = frozenset(("1113", "1308"))
RATE_CODES = frozenset(("1302",))
ZAI_PROVIDER = "zai"
RETRY_EXHAUSTED_PREFIX = "Retry budget exhausted"
RETRY_EXHAUSTED_PREFIX_BYTES = RETRY_EXHAUSTED_PREFIX.encode("ascii")

_RETRIES_RE = re.compile(rb"after (\d{1,12}) retr(?:y|ies)")
_INT_RE = re.compile(rb"-?(?:0|[1-9][0-9]*)")
MAIN_STEM_RE = re.compile(r"^\d{4}-\d\d-\d\dT[\d-]+Z_[0-9a-f-]+$")

EXT = ".jsonl"
SUPPORTED_SCHEMA_VERSION = 3
HEAD_BYTES = 4096
DEFAULT_MAX_TAIL_BYTES = 524288
DEFAULT_MAX_FILES = 20000
DEFAULT_SETTLE_SECONDS = 900

KEY_MAX = 64
TYPE_MAX = 64
ROLE_MAX = 256
STOP_MAX = 256
PROVIDER_MAX = 512
MODEL_MAX = 512
INT_SPAN_MAX = 32
MAX_JSON_DEPTH = 32
_NOT_HEADER = object()

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
_UNAVAILABLE_REASONS = frozenset(
    ("schema", "no-message", "unreadable", "terminal-time")
)

LIMITS = (
    "A terminal error is the LAST OBSERVED state, not proof the session will "
    "never resume; a terminal error newer than the settle window is reported as "
    "error_unsettled, and an error with no usable ms timestamp is unavailable "
    "with reason terminal-time because its age is unproven. Dead counts are "
    "seats (transcript files), not distinct incidents. Prefixes are naming "
    "conventions, not authenticated lane membership. Main sessions are not "
    "seats. Message text, content and usage are never emitted. A (type=...) "
    "business code is a Z.AI-only classification hint, never an authenticated "
    "vendor cause; an unmapped Z.AI code is not rate evidence from HTTP 429 "
    "alone, and codes are ignored for other providers."
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


# ---------------------------------------------------------------------------
# bounded byte-level JSON projection (no whole-line json.loads)
# ---------------------------------------------------------------------------


def _skip_ws(buf, pos):
    length = len(buf)
    while pos < length and buf[pos] in b" \t\r\n":
        pos += 1
    return pos


def _utf8_length(buf, pos):
    """Return the byte length of a strict UTF-8 sequence at pos, or None."""
    first = buf[pos]
    if first < 0x80:
        return 1
    if 0xC2 <= first <= 0xDF:
        follow = 1
    elif 0xE0 <= first <= 0xEF:
        follow = 2
    elif 0xF0 <= first <= 0xF4:
        follow = 3
    else:
        return None
    if pos + follow >= len(buf):
        return None
    for offset in range(1, follow + 1):
        if not (0x80 <= buf[pos + offset] <= 0xBF):
            return None
    if first == 0xE0 and buf[pos + 1] < 0xA0:
        return None
    if first == 0xED and buf[pos + 1] > 0x9F:
        return None
    if first == 0xF0 and buf[pos + 1] < 0x90:
        return None
    if first == 0xF4 and buf[pos + 1] > 0x8F:
        return None
    return follow + 1


def _scan_string(buf, pos):
    """Return the index after a strictly valid JSON string, or None."""
    if pos >= len(buf) or buf[pos] != 0x22:
        return None
    pos += 1
    length = len(buf)
    while pos < length:
        byte = buf[pos]
        if byte == 0x22:  # closing quote
            return pos + 1
        if byte < 0x20:  # raw control character is invalid in JSON
            return None
        if byte == 0x5C:  # backslash: only JSON escape forms are valid
            if pos + 1 >= length:
                return None
            escape = buf[pos + 1]
            if escape == 0x75:  # uXXXX
                if pos + 5 >= length:
                    return None
                for index in range(pos + 2, pos + 6):
                    if buf[index] not in b"0123456789abcdefABCDEF":
                        return None
                pos += 6
                continue
            if escape in b'"\\/bfnrt':
                pos += 2
                continue
            return None
        if byte >= 0x80:
            span = _utf8_length(buf, pos)
            if span is None:
                return None
            pos += span
            continue
        pos += 1
    return None


def _scan_number(buf, pos):
    """Return the index after a strictly valid JSON number, or None."""
    length = len(buf)
    if pos < length and buf[pos] == 0x2D:  # '-'
        pos += 1
    if pos >= length:
        return None
    if buf[pos] == 0x30:  # leading zero, no further digits allowed here
        pos += 1
        if pos < length and 0x30 <= buf[pos] <= 0x39:
            return None
    elif 0x31 <= buf[pos] <= 0x39:
        pos += 1
        while pos < length and 0x30 <= buf[pos] <= 0x39:
            pos += 1
    else:
        return None
    if pos < length and buf[pos] == 0x2E:  # fraction
        pos += 1
        if pos >= length or not (0x30 <= buf[pos] <= 0x39):
            return None
        while pos < length and 0x30 <= buf[pos] <= 0x39:
            pos += 1
    if pos < length and buf[pos] in (0x65, 0x45):  # exponent
        pos += 1
        if pos < length and buf[pos] in (0x2B, 0x2D):
            pos += 1
        if pos >= length or not (0x30 <= buf[pos] <= 0x39):
            return None
        while pos < length and 0x30 <= buf[pos] <= 0x39:
            pos += 1
    return pos


def _scan_value(buf, pos, depth=0):
    """Return (end, kind) for one JSON value, or None; strings stay undecoded."""
    if depth > MAX_JSON_DEPTH:
        return None
    pos = _skip_ws(buf, pos)
    if pos >= len(buf):
        return None
    byte = buf[pos]
    if byte == 0x22:
        end = _scan_string(buf, pos)
        return (end, "string") if end is not None else None
    if byte == 0x7B:  # object
        end = _walk_object(buf, pos, _ignore_member, depth + 1)
        return (end, "object") if end is not None else None
    if byte == 0x5B:  # array
        pos += 1
        pos = _skip_ws(buf, pos)
        if pos < len(buf) and buf[pos] == 0x5D:
            return pos + 1, "array"
        while True:
            scanned = _scan_value(buf, pos, depth + 1)
            if scanned is None:
                return None
            pos = _skip_ws(buf, scanned[0])
            if pos >= len(buf):
                return None
            if buf[pos] == 0x2C:
                pos = _skip_ws(buf, pos + 1)
                continue
            if buf[pos] == 0x5D:
                return pos + 1, "array"
            return None
    if byte == 0x2D or 0x30 <= byte <= 0x39:  # number
        end = _scan_number(buf, pos)
        return (end, "number") if end is not None else None
    if buf.startswith(b"true", pos):
        return pos + 4, "bool"
    if buf.startswith(b"false", pos):
        return pos + 5, "bool"
    if buf.startswith(b"null", pos):
        return pos + 4, "null"
    return None


def _ignore_member(key, value_start, value_end, kind):
    return None


def _walk_object(buf, pos, on_member, depth=0):
    """Validate an object at pos and call on_member per member; return end or None."""
    if depth > MAX_JSON_DEPTH:
        return None
    pos = _skip_ws(buf, pos)
    if pos >= len(buf) or buf[pos] != 0x7B:
        return None
    pos += 1
    pos = _skip_ws(buf, pos)
    if pos < len(buf) and buf[pos] == 0x7D:
        return pos + 1
    while True:
        key_start = pos
        key_end = _scan_string(buf, key_start)
        if key_end is None:
            return None
        key = _decode_bounded(buf, key_start, key_end, KEY_MAX)
        pos = _skip_ws(buf, key_end)
        if pos >= len(buf) or buf[pos] != 0x3A:
            return None
        pos = _skip_ws(buf, pos + 1)
        value_start = pos
        scanned = _scan_value(buf, value_start, depth + 1)
        if scanned is None:
            return None
        value_end, kind = scanned
        on_member(key, value_start, value_end, kind)
        pos = _skip_ws(buf, value_end)
        if pos >= len(buf):
            return None
        if buf[pos] == 0x2C:
            pos = _skip_ws(buf, pos + 1)
            continue
        if buf[pos] == 0x7D:
            return pos + 1
        return None


def _decode_bounded(buf, start, end, limit):
    """Decode a small approved string span; None when over the bound/invalid."""
    if end - start > limit + 2:
        return None
    chunk = buf[start:end]
    try:
        value = json.loads(chunk.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None
    if not isinstance(value, str) or len(value) > limit:
        return None
    return value


def _parse_int_span(buf, start, end):
    """Parse a bounded integer-form JSON number; floats/exponents are rejected."""
    if end - start > INT_SPAN_MAX:
        return None
    chunk = buf[start:end]
    if _INT_RE.fullmatch(chunk) is None:
        return None
    try:
        return int(chunk.decode("ascii"))
    except (UnicodeDecodeError, ValueError):
        return None


def _first_present(*values):
    for value in values:
        if value is not None:
            return value
    return None


def _iter_decoded(buf, start, end):
    """Yield decoded bytes of one JSON string span without materializing it.

    The span is already validated by _scan_string. ASCII code points reached
    through \\u escapes are yielded, so approved tokens are recognized through
    escapes; non-ASCII code points yield a sentinel that breaks token matches.
    """
    pos = start + 1
    stop = end - 1
    mappings = {
        0x22: 0x22,
        0x5C: 0x5C,
        0x2F: 0x2F,
        0x62: 0x08,
        0x66: 0x0C,
        0x6E: 0x0A,
        0x72: 0x0D,
        0x74: 0x09,
    }
    while pos < stop:
        byte = buf[pos]
        if byte != 0x5C:
            pos += 1
            yield byte
            continue
        pos += 1
        if pos >= stop:
            yield 0xFF
            return
        escape = buf[pos]
        pos += 1
        if escape == 0x75:  # uXXXX
            if pos + 4 > stop:
                yield 0xFF
                return
            value = 0
            valid = True
            for offset in range(4):
                code = buf[pos + offset]
                if 0x30 <= code <= 0x39:
                    digit = code - 0x30
                elif 0x41 <= code <= 0x46:
                    digit = code - 0x41 + 10
                elif 0x61 <= code <= 0x66:
                    digit = code - 0x61 + 10
                else:
                    valid = False
                    break
                value = (value << 4) | digit
            pos += 4
            if valid and value <= 0x7F:
                yield value
            else:
                yield 0xFF
            continue
        mapped = mappings.get(escape)
        if mapped is None:
            yield 0xFF
        else:
            yield mapped


def _error_metadata(buf, value_start, value_end):
    """Reduce a validated errorMessage span to bounded class metadata.

    The span is stream-decoded through its JSON escapes; the full decoded text
    is never materialized. Token and retry matching uses a 97-byte carry window
    (64 bytes retained). A small state machine retains numeric code strings;
    their maximum size is bounded by the selected input span, not a display cap.
    """
    prefix_target = RETRY_EXHAUSTED_PREFIX_BYTES
    prefix = bytearray()
    window = bytearray()
    rate_token = False
    quota_token = False
    retries = None
    retry_exhausted = False
    error_code = None

    code_prefix = b"(type="
    prefix_state = 0
    in_digits = False
    digit_count = 0
    digit_buf = bytearray()

    for byte in _iter_decoded(buf, value_start, value_end):
        if len(prefix) < len(prefix_target):
            prefix.append(byte)
            if len(prefix) == len(prefix_target):
                retry_exhausted = bytes(prefix) == prefix_target

        if in_digits:
            if 0x30 <= byte <= 0x39:
                digit_count += 1
                digit_buf.append(byte)
                continue
            in_digits = False
            if byte == 0x29 and digit_count >= 1:  # ')' closes a code token
                error_code = bytes(digit_buf).decode("ascii")

        if byte == code_prefix[prefix_state]:
            prefix_state += 1
            if prefix_state == len(code_prefix):
                prefix_state = 0
                in_digits = True
                digit_count = 0
                digit_buf = bytearray()
        else:
            prefix_state = 1 if byte == code_prefix[0] else 0

        window.append(byte)
        if not rate_token:
            for token in RATE_TOKEN_BYTES:
                if window.endswith(token):
                    rate_token = True
                    break
        if not quota_token:
            for token in QUOTA_TOKEN_BYTES:
                if window.endswith(token):
                    quota_token = True
                    break
        if retries is None:
            match = _RETRIES_RE.search(bytes(window))
            if match is not None:
                retries = int(match.group(1))
        if len(window) > 96:
            del window[:-64]

    return {
        "retry_exhausted": retry_exhausted,
        "retries": retries,
        "error_code": error_code,
        "rate_token": rate_token,
        "quota_token": quota_token,
    }


def _project_message_record(line):
    """Project one transcript line into the approved message view, or None.

    Unapproved members are skipped in place and never decoded or copied.
    """
    state = {
        "type": None,
        "message": None,
        "rec_completed": None,
        "rec_timestamp": None,
    }

    def on_member(key, value_start, value_end, kind):
        if key == "type" and kind == "string":
            state["type"] = _decode_bounded(line, value_start, value_end, TYPE_MAX)
        elif key == "message" and kind == "object":
            state["message"] = (value_start, value_end)
        elif key == "completedAt" and kind == "number":
            ms = _parse_int_span(line, value_start, value_end)
            if ms is not None:
                state["rec_completed"] = ms
        elif key == "timestamp" and kind == "number":
            ms = _parse_int_span(line, value_start, value_end)
            if ms is not None:
                state["rec_timestamp"] = ms
        # Every other member is skipped without decoding.

    end = _walk_object(line, 0, on_member)
    if end is None or _skip_ws(line, end) != len(line):
        return None
    if state["type"] != "message" or state["message"] is None:
        return None
    message_start = state["message"][0]

    view = {
        "role": None,
        "stop_reason": None,
        "error_status": None,
        "provider": None,
        "model": None,
        "msg_completed": None,
        "msg_timestamp": None,
        "retry_exhausted": False,
        "retries": None,
        "error_code": None,
        "rate_token": False,
        "quota_token": False,
    }

    def on_message_member(key, value_start, value_end, kind):
        if key == "role" and kind == "string":
            view["role"] = _decode_bounded(line, value_start, value_end, ROLE_MAX)
        elif key == "stopReason" and kind == "string":
            view["stop_reason"] = _decode_bounded(
                line, value_start, value_end, STOP_MAX
            )
        elif key == "provider" and kind == "string":
            view["provider"] = _decode_bounded(
                line, value_start, value_end, PROVIDER_MAX
            )
        elif key == "model" and kind == "string":
            view["model"] = _decode_bounded(line, value_start, value_end, MODEL_MAX)
        elif key == "errorStatus" and kind == "number":
            view["error_status"] = _parse_int_span(line, value_start, value_end)
        elif key == "completedAt" and kind == "number":
            ms = _parse_int_span(line, value_start, value_end)
            if ms is not None:
                view["msg_completed"] = ms
        elif key == "timestamp" and kind == "number":
            ms = _parse_int_span(line, value_start, value_end)
            if ms is not None:
                view["msg_timestamp"] = ms
        elif key == "errorMessage" and kind == "string":
            # Stream-decode the span through its JSON escapes; only derived
            # metadata is kept, never the decoded text.
            metadata = _error_metadata(line, value_start, value_end)
            view["retry_exhausted"] = metadata["retry_exhausted"]
            view["retries"] = metadata["retries"]
            view["error_code"] = metadata["error_code"]
            view["rate_token"] = metadata["rate_token"]
            view["quota_token"] = metadata["quota_token"]
        # Every other member is skipped without decoding.

    if _walk_object(line, message_start, on_message_member) is None:
        return None
    view["terminal_ms"] = _first_present(
        view["msg_completed"],
        view["msg_timestamp"],
        state["rec_completed"],
        state["rec_timestamp"],
    )
    return view


def _header_candidate(line):
    state = {"type": None, "version": None}

    def on_member(key, value_start, value_end, kind):
        if key == "type" and kind == "string":
            state["type"] = _decode_bounded(line, value_start, value_end, TYPE_MAX)
        elif key == "version" and kind == "number":
            state["version"] = _parse_int_span(line, value_start, value_end)

    end = _walk_object(line, 0, on_member)
    if end is None or _skip_ws(line, end) != len(line):
        return _NOT_HEADER
    if state["type"] != "session":
        return _NOT_HEADER
    return state["version"]


def _project_session_header(head):
    for line in head.split(b"\n"):
        candidate = _header_candidate(line)
        if candidate is not _NOT_HEADER:
            return candidate
    return None


def _project_tail(data):
    last = None
    for line in data.split(b"\n"):
        view = _project_message_record(line)
        if view is not None:
            last = view
    return last


# ---------------------------------------------------------------------------
# classification
# ---------------------------------------------------------------------------


def _classify(view, now_ms, settle_seconds):
    """Return (class, reason) for one projected terminal message view."""
    role = view["role"]
    stop_reason = view["stop_reason"]
    if role != "assistant":
        return "incomplete", None
    if stop_reason == "stop":
        return "completed", None
    if stop_reason == "aborted":
        return "aborted", None
    if stop_reason != "error":
        return "incomplete", None
    terminal_ms = view["terminal_ms"]
    if terminal_ms is None:
        # No usable age evidence: not proven dead, not proven recent.
        return "unavailable", "terminal-time"
    if terminal_ms > now_ms - settle_seconds * 1000:
        return "error_unsettled", None
    error_code = view["error_code"]
    code_present = error_code is not None
    if view["provider"] == ZAI_PROVIDER and code_present:
        if error_code in QUOTA_CODES:
            return "dead_quota", None
        if error_code in RATE_CODES:
            return "dead_rate_limit", None
        # Unmapped Z.AI business code: HTTP 429 alone is not cause
        # evidence; only explicit text clues may classify.
        if view["quota_token"]:
            return "dead_quota", None
        if view["rate_token"]:
            return "dead_rate_limit", None
        return "dead_error_other", None
    if view["quota_token"]:
        return "dead_quota", None
    if view["error_status"] == 429 or view["rate_token"]:
        return "dead_rate_limit", None
    return "dead_error_other", None


# ---------------------------------------------------------------------------
# file access: one nonblocking, no-follow descriptor per file
# ---------------------------------------------------------------------------


def _open_regular(path):
    """Open a path safely; return (fd, size) only for a regular file.

    Retained for the direct FIFO-safety arm; the scan itself never resolves a
    path string and uses ``_open_regular_at`` from the held root descriptor.
    """
    flags = os.O_RDONLY
    flags |= getattr(os, "O_NOFOLLOW", 0)
    flags |= getattr(os, "O_NONBLOCK", 0)
    try:
        fd = os.open(path, flags)
    except OSError:
        return None
    try:
        info = os.fstat(fd)
    except OSError:
        os.close(fd)
        return None
    if not stat.S_ISREG(info.st_mode):
        os.close(fd)
        return None
    return fd, info.st_size


def _dir_flags():
    return (
        os.O_RDONLY
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )


def _file_flags():
    return (
        os.O_RDONLY
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_NONBLOCK", 0)
    )


def _open_dir(path):
    try:
        return os.open(path, _dir_flags()), None
    except OSError as exc:
        return None, exc.errno


def _open_leaf(root_fd, relpath):
    """Open relpath under root_fd without following any symlink component."""
    parts = relpath.split("/")
    dir_fd = os.dup(root_fd)
    try:
        for part in parts[:-1]:
            try:
                next_fd = os.open(part, _dir_flags(), dir_fd=dir_fd)
            except OSError:
                return None
            os.close(dir_fd)
            dir_fd = next_fd
        try:
            return os.open(parts[-1], _file_flags(), dir_fd=dir_fd)
        except OSError:
            return None
    finally:
        os.close(dir_fd)


def _open_regular_at(root_fd, relpath):
    fd = _open_leaf(root_fd, relpath)
    if fd is None:
        return None
    try:
        info = os.fstat(fd)
    except OSError:
        os.close(fd)
        return None
    if not stat.S_ISREG(info.st_mode):
        os.close(fd)
        return None
    return fd, info.st_size


def _collect_entries(root_fd, max_files):
    """Descriptor-relative walk collecting regular *.jsonl paths.

    Every directory is opened O_NOFOLLOW|O_DIRECTORY relative to its parent
    descriptor, so a symlinked ancestor cannot redirect the walk even under
    directory replacement.
    """
    entries = []
    stack = [(root_fd, "", False)]
    while stack:
        dir_fd, rel_dir, owned = stack.pop()
        try:
            scan_fd = os.dup(dir_fd)
            try:
                iterator = os.scandir(scan_fd)
            except OSError:
                os.close(scan_fd)
                raise _SetupError("walk-error")
            try:
                try:
                    for entry in iterator:
                        try:
                            if entry.is_symlink():
                                continue
                            if entry.is_dir(follow_symlinks=False):
                                is_dir = True
                            elif entry.is_file(follow_symlinks=False):
                                is_dir = False
                            else:
                                continue
                        except OSError:
                            raise _SetupError("lstat-failed")
                        name = entry.name
                        child_rel = name if not rel_dir else rel_dir + "/" + name
                        if is_dir:
                            try:
                                child_fd = os.open(
                                    name, _dir_flags(), dir_fd=dir_fd
                                )
                            except OSError:
                                raise _SetupError("walk-error")
                            stack.append((child_fd, child_rel, True))
                            continue
                        if not name.endswith(EXT):
                            continue
                        entries.append(child_rel)
                        if len(entries) > max_files:
                            raise _SetupError(
                                "too-many-files",
                                files_seen=len(entries),
                                max_files=max_files,
                            )
                except OSError:
                    raise _SetupError("walk-error")
            finally:
                iterator.close()
                try:
                    os.close(scan_fd)
                except OSError:
                    pass
        finally:
            if owned:
                os.close(dir_fd)
    return entries


def _pread(fd, length, offset):
    chunks = []
    remaining = length
    while remaining > 0:
        chunk = os.pread(fd, remaining, offset)
        if not chunk:
            break
        chunks.append(chunk)
        offset += len(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def _analyze_fd(fd, size, max_tail_bytes, now_ms, settle_seconds):
    try:
        head = _pread(fd, min(size, HEAD_BYTES), 0)
        if _project_session_header(head) != SUPPORTED_SCHEMA_VERSION:
            return None, "unavailable", "schema"
        tail_length = min(size, max_tail_bytes)
        tail_start = size - tail_length
        tail = _pread(fd, tail_length, tail_start)
    except OSError:
        return None, "unavailable", "unreadable"
    if tail_start > 0:
        newline = tail.find(b"\n")
        tail = tail[newline + 1 :] if newline >= 0 else b""
    view = _project_tail(tail)
    if view is None:
        return None, "unavailable", "no-message"
    seat_class, reason = _classify(view, now_ms, settle_seconds)
    return view, seat_class, reason


def _analyze(path, max_tail_bytes, now_ms, settle_seconds):
    opened = _open_regular(path)
    if opened is None:
        return None, "unavailable", "unreadable"
    fd, size = opened
    try:
        return _analyze_fd(fd, size, max_tail_bytes, now_ms, settle_seconds)
    finally:
        os.close(fd)


# ---------------------------------------------------------------------------
# scan
# ---------------------------------------------------------------------------


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


def _raise_walk_error(_error):
    raise _SetupError("walk-error")


def _scan(
    sessions_dir,
    prefixes,
    max_tail_bytes,
    max_files,
    now_ms,
    settle_seconds,
):
    root_check = sessions_dir.rstrip(os.sep) or sessions_dir
    if os.path.islink(root_check):
        raise _SetupError("root-symlink")
    root_fd, open_errno = _open_dir(sessions_dir)
    if root_fd is None:
        if open_errno == errno.ELOOP or os.path.islink(root_check):
            raise _SetupError("root-symlink")
        raise _SetupError("unavailable-dir")
    prefix_filter = set(prefixes)
    records = []
    files_scanned = 0
    try:
        discovered = _collect_entries(root_fd, max_files)
        for relpath in discovered:
            stem = relpath.rsplit("/", 1)[-1][: -len(EXT)]
            key = relpath[: -len(EXT)]
            direct = "/" not in relpath
            kind = "main" if direct and MAIN_STEM_RE.match(stem) else "seat"
            prefix = stem.split(".", 1)[0]
            if kind == "seat" and prefix_filter and prefix not in prefix_filter:
                continue
            files_scanned += 1
            opened = _open_regular_at(root_fd, relpath)
            if opened is None:
                view = None
                seat_class = "unavailable"
                reason = "unreadable"
            else:
                fd, size = opened
                try:
                    view, seat_class, reason = _analyze_fd(
                        fd, size, max_tail_bytes, now_ms, settle_seconds
                    )
                finally:
                    os.close(fd)
            records.append(
                _seat_record(stem, key, kind, prefix, seat_class, reason, view)
            )
    finally:
        os.close(root_fd)

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


def _call_with_timeout(func, seconds):
    outcome = {}

    def run():
        try:
            outcome["value"] = func()
        except BaseException as exc:  # selftest capture only
            outcome["error"] = exc

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    thread.join(seconds)
    if thread.is_alive():
        return "timeout", None
    if "error" in outcome:
        return "error", outcome["error"]
    return "value", outcome.get("value")


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
            if reason not in _UNAVAILABLE_REASONS:
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
    restore_modes = []

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
                            completedAt=_SELFTEST_NOW_MS - 1000000,
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
            "resource-exhausted-other",
            [
                (
                    "sessions/Devin.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            completedAt=_SELFTEST_NOW_MS - 1000000,
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
                "seats": {"Devin.Seat": "dead_error_other"},
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
            "devin-free-model-rate-limit",
            [
                (
                    "sessions/DevinFree.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            completedAt=_SELFTEST_NOW_MS - 1000000,
                            errorMessage="Reached free model rate limit",
                            provider="devin",
                            model="swe-1",
                        )
                    ],
                )
            ],
            {
                "rc": 1,
                "finding_id": FINDING_DEAD,
                "seats": {"DevinFree.Seat": "dead_rate_limit"},
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
                            completedAt=_SELFTEST_NOW_MS - 1000000,
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
                            completedAt=_SELFTEST_NOW_MS - 1000000,
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
                        completedAt=_SELFTEST_NOW_MS - 1000000,
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

        add(
            "a1-quota-token-before-429",
            [
                (
                    "sessions/A1Quota.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            completedAt=_SELFTEST_NOW_MS - 1000000,
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

        add(
            "a1-code-before-tokens",
            [
                (
                    "sessions/Code1113.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            completedAt=_SELFTEST_NOW_MS - 1000000,
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
                            completedAt=_SELFTEST_NOW_MS - 1000000,
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
                            completedAt=_SELFTEST_NOW_MS - 1000000,
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

        add(
            "a2-nonzai-code-control",
            [
                (
                    "sessions/NonZai1113.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            completedAt=_SELFTEST_NOW_MS - 1000000,
                            errorMessage="(type=1113)",
                            provider="devin",
                            model="swe-1",
                        )
                    ],
                ),
                (
                    "sessions/NonZai1302.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            completedAt=_SELFTEST_NOW_MS - 1000000,
                            errorMessage="(type=1302)",
                            provider="opencode",
                            model="m1",
                        )
                    ],
                ),
            ],
            {
                "rc": 1,
                "finding_id": FINDING_DEAD,
                "seats": {
                    "NonZai1113.Seat": "dead_error_other",
                    "NonZai1302.Seat": "dead_error_other",
                },
                "files_scanned": 2,
            },
        )

        add(
            "a2-unknown-zai-code",
            [
                (
                    "sessions/UnknownCode.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            completedAt=_SELFTEST_NOW_MS - 1000000,
                            errorStatus=429,
                            errorMessage="(type=9999)",
                            provider="zai",
                            model="glm-4.6",
                        )
                    ],
                ),
                (
                    "sessions/UnknownText.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            completedAt=_SELFTEST_NOW_MS - 1000000,
                            errorStatus=429,
                            errorMessage="rate limit (type=9999)",
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
                    "UnknownCode.Seat": "dead_error_other",
                    "UnknownText.Seat": "dead_rate_limit",
                },
                "files_scanned": 2,
            },
        )

        add(
            "a2-error-no-terminal-time",
            [
                (
                    "sessions/NoTime.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            errorStatus=429,
                            errorMessage="rate_limit",
                            provider="zai",
                            model="glm-4.6",
                        )
                    ],
                )
            ],
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {"NoTime.Seat": "unavailable"},
                "records": {"NoTime.Seat": {"reason": "terminal-time"}},
                "files_scanned": 1,
            },
        )

        completed_line = (
            json.dumps(
                _msg("assistant", stopReason="stop", provider="p", model="m"),
                separators=(",", ":"),
            ).encode("utf-8")
            + b"\n"
        )

        strict_escape = (
            header_line
            + b'{"type":"message","message":{"role":"assistant","stopReason":"stop",'
            b'"content":"bad\\qescape","provider":"p","model":"m"}}\n'
            + completed_line
        )
        add(
            "a2-strict-escape",
            [("sessions/StrictEscape.Seat.jsonl", strict_escape)],
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {"StrictEscape.Seat": "completed"},
                "files_scanned": 1,
            },
        )

        strict_number = (
            header_line
            + b'{"type":"message","message":{"role":"assistant","stopReason":"error",'
            b'"completedAt":1699999000000,"errorStatus":42+9,"errorMessage":"quota",'
            b'"provider":"zai","model":"glm-4.6"}}\n'
            + completed_line
        )
        add(
            "a2-strict-number",
            [("sessions/StrictNumber.Seat.jsonl", strict_number)],
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {"StrictNumber.Seat": "completed"},
                "files_scanned": 1,
            },
        )

        escaped_code = (
            header_line
            + b'{"type":"message","message":{"role":"assistant","stopReason":"error",'
            b'"completedAt":1699999000000,'
            b'"errorMessage":"failure (type=\\u0031302)",'
            b'"provider":"zai","model":"glm-4.6"}}\n'
        )
        escaped_retry = (
            header_line
            + b'{"type":"message","message":{"role":"assistant","stopReason":"error",'
            b'"completedAt":1699999000000,'
            b'"errorMessage":"Retry budget exhausted after 2 retries: rate\\u005flimit",'
            b'"provider":"zai","model":"glm-4.6"}}\n'
        )
        add(
            "a2-escaped-error-tokens",
            [
                ("sessions/EscapedCode.Seat.jsonl", escaped_code),
                ("sessions/EscapedRetry.Seat.jsonl", escaped_retry),
            ],
            {
                "rc": 1,
                "finding_id": FINDING_DEAD,
                "seats": {
                    "EscapedCode.Seat": "dead_rate_limit",
                    "EscapedRetry.Seat": "dead_rate_limit",
                },
                "records": {
                    "EscapedCode.Seat": {"error_code": "1302"},
                    "EscapedRetry.Seat": {
                        "retry_exhausted": True,
                        "retries": 2,
                        "error_code": None,
                    },
                },
                "files_scanned": 2,
            },
        )

        add(
            "a2-long-zai-code",
            [
                (
                    "sessions/LongCode.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            completedAt=_SELFTEST_NOW_MS - 1000000,
                            errorStatus=429,
                            errorMessage="(type=1234567890123)",
                            provider="zai",
                            model="glm-4.6",
                        )
                    ],
                )
            ],
            {
                "rc": 1,
                "finding_id": FINDING_DEAD,
                "seats": {"LongCode.Seat": "dead_error_other"},
                "records": {"LongCode.Seat": {"error_code": "1234567890123"}},
                "files_scanned": 1,
            },
        )

        add(
            "a2-float-status-time",
            [
                (
                    "sessions/FloatStatus.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            errorStatus=429.0,
                            errorMessage="upstream failure",
                            completedAt=_SELFTEST_NOW_MS - 1000000,
                            provider="zai",
                            model="glm-4.6",
                        )
                    ],
                ),
                (
                    "sessions/FloatTime.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            errorStatus=429,
                            errorMessage="rate_limit",
                            timestamp=_SELFTEST_NOW_MS - 60000 + 0.5,
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
                    "FloatStatus.Seat": "dead_error_other",
                    "FloatTime.Seat": "unavailable",
                },
                "records": {
                    "FloatStatus.Seat": {"error_status": None},
                    "FloatTime.Seat": {
                        "reason": "terminal-time",
                        "terminal_ms": None,
                    },
                },
                "files_scanned": 2,
            },
        )

        float_version = (
            b'{"type":"session","version":3.0}\n' + completed_line
        )
        add(
            "a2-float-version",
            [("sessions/FloatVersion.Seat.jsonl", float_version)],
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {"FloatVersion.Seat": "unavailable"},
                "records": {"FloatVersion.Seat": {"reason": "schema"}},
                "files_scanned": 1,
            },
        )

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

        add(
            "a1-retry-singular-role",
            [
                (
                    "sessions/Singular.Seat.jsonl",
                    [
                        _msg(
                            "assistant",
                            stopReason="error",
                            completedAt=_SELFTEST_NOW_MS - 1000000,
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

        # Wave-2: non-message credential_pin payload never decoded/echoed.
        add(
            "a2-credential-pin-only",
            [
                (
                    "sessions/CredOnly.Seat.jsonl",
                    [
                        {
                            "type": "credential_pin",
                            "name": "fake",
                            "token": _SELFTEST_FAKE_TOKEN,
                            "credential": {"value": _SELFTEST_FAKE_TOKEN},
                        },
                        {
                            "type": "custom",
                            "content": _SELFTEST_FAKE_TOKEN,
                            "usage": {"cost": 3.25},
                            "payload": _SELFTEST_SECRET_TEXT,
                        },
                    ],
                )
            ],
            {
                "rc": 0,
                "finding_id": FINDING_OK,
                "seats": {"CredOnly.Seat": "unavailable"},
                "records": {"CredOnly.Seat": {"reason": "no-message"}},
                "files_scanned": 1,
            },
        )

        # Wave-2: a symlinked sessions root is rejected, trailing separator too.
        root_symlink_dir = os.path.join(root, "a2-root-symlink")
        real_sessions = os.path.join(root_symlink_dir, "real-sessions")
        os.makedirs(real_sessions)
        _materialize(
            os.path.join(real_sessions, "Seat.One.jsonl"),
            [_msg("assistant", stopReason="stop", provider="p", model="m")],
        )
        link_path = os.path.join(root_symlink_dir, "sessions-link")
        os.symlink(real_sessions, link_path)
        arms.append(
            (
                "a2-root-symlink",
                root_symlink_dir,
                ["--sessions-dir", link_path, "--now-ms", str(_SELFTEST_NOW_MS)],
                {
                    "rc": 2,
                    "finding_id": FINDING_SETUP,
                    "reason": "root-symlink",
                },
            )
        )
        arms.append(
            (
                "a2-root-symlink-trailing-slash",
                root_symlink_dir,
                [
                    "--sessions-dir",
                    link_path + os.sep,
                    "--now-ms",
                    str(_SELFTEST_NOW_MS),
                ],
                {
                    "rc": 2,
                    "finding_id": FINDING_SETUP,
                    "reason": "root-symlink",
                },
            )
        )

        # Wave-2: directory traversal denial is setup, never a partial clean.
        walk_dir = os.path.join(root, "a2-walk-error")
        walk_sessions = os.path.join(walk_dir, "sessions")
        blocked = os.path.join(walk_sessions, "blocked")
        os.makedirs(blocked)
        _materialize(
            os.path.join(walk_sessions, "Seat.One.jsonl"),
            [_msg("assistant", stopReason="stop", provider="p", model="m")],
        )
        os.chmod(blocked, 0)
        restore_modes.append(blocked)
        arms.append(
            (
                "a2-walk-error",
                walk_dir,
                ["--sessions-dir", walk_sessions, "--now-ms", str(_SELFTEST_NOW_MS)],
                {
                    "rc": 2,
                    "finding_id": FINDING_SETUP,
                    "reason": "walk-error",
                },
            )
        )

        for arm in arms:
            errors = _check_arm(tool, arm)
            if errors:
                failures.append("arm %s: %s" % (arm[0], "; ".join(errors[:8])))
            else:
                passed += 1

        # Direct safety arms (not subprocess): the open path and the walk-error
        # callback are exercised deterministically.
        extra_arms = 0
        extra_passed = 0

        fifo_safety_dir = os.path.join(root, "a2-fifo-open-safety")
        os.makedirs(fifo_safety_dir)
        fifo_safety_path = os.path.join(fifo_safety_dir, "fifo.jsonl")
        os.mkfifo(fifo_safety_path)
        extra_arms += 1
        outcome, value = _call_with_timeout(
            lambda: _analyze(
                fifo_safety_path,
                DEFAULT_MAX_TAIL_BYTES,
                _SELFTEST_NOW_MS,
                DEFAULT_SETTLE_SECONDS,
            ),
            10.0,
        )
        if outcome == "value" and value == (None, "unavailable", "unreadable"):
            extra_passed += 1
        elif outcome == "timeout":
            failures.append("arm a2-fifo-open-safety: _analyze blocked on FIFO")
        elif outcome == "error":
            failures.append(
                "arm a2-fifo-open-safety: raised %s" % type(value).__name__
            )
        else:
            failures.append("arm a2-fifo-open-safety: result=%r" % (value,))

        extra_arms += 1
        try:
            _raise_walk_error(OSError("selftest"))
        except _SetupError as exc:
            if exc.reason == "walk-error":
                extra_passed += 1
            else:
                failures.append(
                    "arm a2-walk-error-raiser: reason=%r" % (exc.reason,)
                )
        except Exception:
            failures.append("arm a2-walk-error-raiser: wrong exception type")
        else:
            failures.append("arm a2-walk-error-raiser: no exception raised")

        try:
            with open(tool, "rb") as handle:
                tool_sha256 = hashlib.sha256(handle.read()).hexdigest()
        except OSError:
            tool_sha256 = None

        total_arms = len(arms) + extra_arms
        total_passed = passed + extra_passed
        if failures:
            return _emit(
                {
                    "finding_id": "SELFTEST_FAIL",
                    "schema": "mori-seat-terminal-selftest-v1",
                    "arms": total_arms,
                    "passed": total_passed,
                    "failures": failures,
                    "tool_sha256": tool_sha256,
                },
                1,
            )
        return _emit(
            {
                "finding_id": "SELFTEST_OK",
                "schema": "mori-seat-terminal-selftest-v1",
                "arms": total_arms,
                "passed": total_passed,
                "tool_sha256": tool_sha256,
            },
            0,
        )
    finally:
        for mode_path in restore_modes:
            try:
                os.chmod(mode_path, 0o700)
            except OSError:
                pass
        shutil.rmtree(root, ignore_errors=True)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="mori-seat-terminal.py",
        description=(
            "Read-only terminal-status census of OMP seat transcripts (contract C1 "
            "+ Amendment A1 + wave-2 filesystem/privacy hardening). Walk a sessions "
            "directory for regular *.jsonl files (symlinks, FIFOs and devices never "
            "read), validate the first-4096-byte session header version 3, read at "
            "most the last --max-tail-bytes from the same descriptor, classify the "
            "last message record with a settle window, and tally per seat-name "
            "prefix and per provider/model. A symlinked sessions root, a directory "
            "walk error, or an lstat failure is rc2 setup, never a partial clean. " +
            LIMITS
        ),
        epilog=(
            "stdout carries exactly one JSON object (schema mori-seat-terminal-v1, "
            "key finding_id). Only an approved field set is decoded (record type "
            "and timestamps; message role, stopReason, errorStatus, timestamps, "
            "provider, model; errorMessage-derived retry/code/token metadata); "
            "content, usage, credential_pin payloads and all other members are "
            "structurally skipped without decoding. errorMessage text, content and "
            "usage are never emitted. Skipped values are still validated for strict "
            "JSON escapes, UTF-8 and complete number grammar; schema version, "
            "status and timestamp fields accept integer-form numbers only. Exit 0 "
            "= scan complete with zero dead_* "
            "seats; 1 = scan complete with at least one dead_* seat; 2 = "
            "setup/unavailable, prefix-matched-none, root-symlink, walk-error, "
            "lstat-failed, or any internal error. --selftest builds synthetic "
            "transcripts under TMPDIR and runs the CLI plus direct safety arms; "
            "its existence is not permission to run it during a wave."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--sessions-dir",
        metavar="DIR",
        help="directory of OMP seat transcripts (*.jsonl, walked recursively); a "
        "symlink is rejected with rc2 root-symlink",
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
