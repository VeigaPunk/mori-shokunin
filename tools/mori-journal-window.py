#!/usr/bin/env python3
"""mori-journal-window — bounded MESSAGE-free same-boot journal window probe.

Mori round-16 C1 coverage tool. Reads a mori-journal-anchor-v1 anchor file and
asks journalctl for the record stream starting AT the anchor cursor. The window
is available only when the first parsed record carries the anchor's exact
cursor bytes and exact _BOOT_ID; that record is then dropped. Every later
record must be a JSON object from the same boot with a unique valid scalar
cursor. Byte equality is a conservative acceptance test only (S039/S040): a
cursor alias or a seek to the next closest entry is indistinguishable from a
vacuumed/rotated anchor, so any first-record mismatch is reported as
anchor-not-first-record and never as deletion, vacuum, or missing-entry proof.

Stdout contract: exactly one JSON object. Raw cursor strings, record bytes and
stderr bytes are never echoed; only SHA-256 digests of the anchor file and the
optional end cursor are reported.

Sources: S014 journalctl(1), S015 systemd.journal-fields(7), S039
sd_journal_seek_cursor(3), S040 sd_journal_test_cursor(3);
corpus/knowledge/journal-cursor-window-r16.md,
corpus/knowledge/journal-positive-evidence-r15.md.
"""

import argparse
import hashlib
import json
import math
import os
import re
import selectors
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time

FINDING_OK = "MORI_JOURNAL_WINDOW_OK"
FINDING_UNAVAILABLE = "MORI_JOURNAL_WINDOW_UNAVAILABLE"
FINDING_SETUP = "MORI_JOURNAL_WINDOW_SETUP"

ANCHOR_SCHEMA = "mori-journal-anchor-v1"
ANCHOR_MAX_BYTES = 8192
CURSOR_MAX_LEN = 4096

OUTPUT_FIELDS = "__CURSOR,_BOOT_ID,MESSAGE_ID,UNIT_RESULT,EXIT_CODE,EXIT_STATUS"

# r15 positive predicates (corpus/knowledge/journal-positive-evidence-r15.md)
MSGID_KERNEL_OOM = "fe6faa94e7774663a0da52717891d8ef"
MSGID_UNIT_FAILURE = "d9b373ed55a64feb8242e02dbe79a49c"
MSGID_UNIT_SIGKILL = "98e322203f7a4ed290d09fe03c09fe15"

DEFAULT_TIMEOUT_S = 10.0
MAX_TIMEOUT_S = 120.0
DEFAULT_MAX_BYTES = 8 * 1024 * 1024
CEIL_MAX_BYTES = 64 * 1024 * 1024
KILL_GRACE_S = 2.0

_BOOT_ID_RE = re.compile(r"^[0-9a-f]{32}$")
_TIMEOUT_RE = re.compile(r"^[0-9]+(\.[0-9]+)?$")
_INT_RE = re.compile(r"^[0-9]+$")


class _JObj(dict):
    """dict marker carrying a duplicate-key flag from the pairs hook."""

    dup = False


def _pairs_hook(pairs):
    out = _JObj()
    for k, v in pairs:
        if k in out:
            out.dup = True
        out[k] = v
    return out


def _reject_constant(_x):
    raise ValueError("non-strict JSON constant")


def _json_loads_strict(text):
    return json.loads(
        text,
        parse_constant=_reject_constant,
        object_pairs_hook=_pairs_hook,
    )


def _valid_cursor(c):
    return (
        isinstance(c, str)
        and 0 < len(c) <= CURSOR_MAX_LEN
        and c[0] != "-"
        and all(0x20 <= ord(ch) <= 0x7E for ch in c)
    )


def _sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def _emit(obj):
    sys.stdout.write(json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n")


def _fail(finding_id, reason, scope=None, anchor_sha256=None):
    obj = {"finding_id": finding_id, "reason": reason}
    if scope is not None:
        obj["scope"] = scope
    if anchor_sha256 is not None:
        obj["anchor_sha256"] = anchor_sha256
    _emit(obj)
    return 2


def _kill_reap(proc):
    """SIGKILL only our owned journal child's process group, then bounded reap."""
    if proc.returncode is None:
        try:
            if os.getpgid(proc.pid) == proc.pid:
                os.killpg(proc.pid, signal.SIGKILL)
            else:
                proc.kill()
        except (ProcessLookupError, PermissionError, OSError):
            try:
                proc.kill()
            except (ProcessLookupError, PermissionError, OSError):
                pass
    try:
        proc.wait(timeout=KILL_GRACE_S)
    except subprocess.TimeoutExpired:
        pass  # D-state or unreapable: bound honoured by returning anyway
    for stream in (proc.stdout, proc.stderr, proc.stdin):
        try:
            if stream is not None:
                stream.close()
        except OSError:
            pass


def _capture(argv, timeout_s, max_bytes):
    """Run journalctl with bounded concurrent collection of both streams.

    Returns dict: out (bytes, capped), err_len (int), overflow, timed_out,
    rc (int or None), or {"error": reason} when the spawn itself failed.
    Never stores or returns stderr content.
    """
    deadline = time.monotonic() + timeout_s
    try:
        proc = subprocess.Popen(
            argv,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
            start_new_session=True,
        )
    except FileNotFoundError:
        return {"error": "journalctl-missing"}
    except (PermissionError, OSError):
        return {"error": "journalctl-spawn-failed"}

    out = bytearray()
    err_len = 0
    overflow = False
    timed_out = False
    sel = selectors.DefaultSelector()
    open_fds = 0
    try:
        sel.register(proc.stdout.fileno(), selectors.EVENT_READ, "out")
        sel.register(proc.stderr.fileno(), selectors.EVENT_READ, "err")
        open_fds = 2
        while open_fds and not overflow:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                timed_out = True
                break
            events = sel.select(min(remaining, 0.2))
            for key, _mask in events:
                try:
                    chunk = os.read(key.fd, 65536)
                except OSError:
                    chunk = b""
                if not chunk:
                    try:
                        sel.unregister(key.fd)
                    except (KeyError, ValueError):
                        pass
                    open_fds -= 1
                    continue
                if key.data == "out":
                    out += chunk
                    if len(out) > max_bytes:
                        overflow = True
                else:
                    err_len += len(chunk)
                    if err_len > max_bytes:
                        overflow = True
    finally:
        try:
            sel.close()
        except Exception:
            pass

    if overflow or timed_out:
        _kill_reap(proc)
        rc = proc.returncode
    else:
        try:
            rc = proc.wait(timeout=max(0.0, deadline - time.monotonic()))
        except subprocess.TimeoutExpired:
            timed_out = True
            _kill_reap(proc)
            rc = proc.returncode
        finally:
            for stream in (proc.stdout, proc.stderr):
                try:
                    if stream is not None:
                        stream.close()
                except OSError:
                    pass

    return {
        "out": bytes(out),
        "err_len": err_len,
        "overflow": overflow,
        "timed_out": timed_out,
        "rc": rc,
    }


def _scalar_status_nine(v):
    """r15 'scalar status 9' with jq numeric-equality parity: string "9" or
    any JSON number equal to 9 (9, 9.0, 9e0). Bool, null, array, object and
    every other value are rejected."""
    if isinstance(v, bool):
        return False
    if isinstance(v, str):
        return v == "9"
    if isinstance(v, (int, float)):
        return v == 9
    return False


def _read_anchor(path):
    """Return (raw_bytes, None) or (None, setup_reason). Bounded regular-file read."""
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except FileNotFoundError:
        return None, "anchor-file-missing"
    except OSError:
        return None, "anchor-file-unreadable"
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            return None, "anchor-file-invalid"
        buf = bytearray()
        while len(buf) <= ANCHOR_MAX_BYTES:
            try:
                chunk = os.read(fd, ANCHOR_MAX_BYTES + 1 - len(buf))
            except BlockingIOError:
                return None, "anchor-file-unreadable"
            except OSError:
                return None, "anchor-file-unreadable"
            if not chunk:
                break
            buf += chunk
        if len(buf) > ANCHOR_MAX_BYTES:
            return None, "anchor-file-invalid"
        return bytes(buf), None
    finally:
        os.close(fd)


def _validate_anchor(raw):
    """Return (anchor_dict, None) or (None, setup_reason)."""
    try:
        text = raw.strip().decode("utf-8")
        obj = _json_loads_strict(text)
    except (UnicodeDecodeError, ValueError, RecursionError):
        return None, "anchor-invalid-json"
    if not isinstance(obj, dict) or getattr(obj, "dup", False):
        return None, "anchor-invalid-schema"
    if obj.get("schema") != ANCHOR_SCHEMA:
        return None, "anchor-invalid-schema"
    scope = obj.get("scope")
    if scope not in ("user", "system"):
        return None, "anchor-invalid-schema"
    boot_id = obj.get("boot_id")
    if not isinstance(boot_id, str) or not _BOOT_ID_RE.fullmatch(boot_id):
        return None, "anchor-invalid-schema"
    cursor = obj.get("cursor")
    if not _valid_cursor(cursor):
        return None, "anchor-invalid-schema"
    extra = set(obj) - {"schema", "scope", "boot_id", "cursor"}
    if extra:
        return None, "anchor-invalid-schema"
    return obj, None


def _evaluate(records, anchor):
    """Validate record stream and compute the window. Returns (reason, stats)."""
    first = records[0]
    if not isinstance(first, dict) or getattr(first, "dup", False):
        return "record-invalid", None
    if first.get("__CURSOR") != anchor["cursor"]:
        return "anchor-not-first-record", None
    if first.get("_BOOT_ID") != anchor["boot_id"]:
        return "anchor-boot-mismatch", None

    seen = {anchor["cursor"]}
    kernel_oom = unit_oom = unit_signal = process_sigkill = 0
    last_cursor = None

    for rec in records[1:]:
        if not isinstance(rec, dict) or getattr(rec, "dup", False):
            return "record-invalid", None
        boot = rec.get("_BOOT_ID")
        if not isinstance(boot, str):
            return "record-invalid", None
        if boot != anchor["boot_id"]:
            return "foreign-boot", None
        cursor = rec.get("__CURSOR")
        if not _valid_cursor(cursor):
            return "record-invalid", None
        if cursor in seen:
            return "duplicate-cursor", None
        seen.add(cursor)
        last_cursor = cursor

        mid = rec.get("MESSAGE_ID")
        if not isinstance(mid, str):
            continue
        if mid == MSGID_KERNEL_OOM:
            kernel_oom += 1
        elif mid == MSGID_UNIT_FAILURE:
            result = rec.get("UNIT_RESULT")
            if result == "oom-kill":
                unit_oom += 1
            elif result == "signal":
                unit_signal += 1
        elif mid == MSGID_UNIT_SIGKILL:
            if rec.get("EXIT_CODE") == "killed" and _scalar_status_nine(
                rec.get("EXIT_STATUS")
            ):
                process_sigkill += 1

    stats = {
        "records_after_anchor": len(records) - 1,
        "positive_kernel_oom": kernel_oom,
        "positive_unit_oom": unit_oom,
        "positive_unit_signal": unit_signal,
        "positive_process_sigkill": process_sigkill,
        "last_cursor": last_cursor,
    }
    return None, stats


def _parse_records(raw):
    """Parse captured stdout bytes as JSONL. Returns (records, None) or (None, reason)."""
    if not raw:
        return None, "empty-capture"
    lines = raw.split(b"\n")
    if lines and lines[-1] == b"":
        lines.pop()
    if not lines:
        return None, "empty-capture"
    records = []
    for line in lines:
        if not line.strip():
            return None, "malformed-json"
        try:
            records.append(_json_loads_strict(line.decode("utf-8")))
        except (UnicodeDecodeError, ValueError, RecursionError):
            return None, "malformed-json"
    return records, None


def _resolve_journalctl(path):
    if path:
        return path, None
    default = "/usr/bin/journalctl"
    if os.path.isfile(default) and os.access(default, os.X_OK):
        return default, None
    found = shutil.which("journalctl")
    if found:
        return found, None
    return None, "journalctl-missing"


def _run(args):
    scope = args.scope
    if scope not in ("user", "system"):
        return _fail(FINDING_SETUP, "invalid-args")

    if not _TIMEOUT_RE.fullmatch(args.timeout):
        return _fail(FINDING_SETUP, "invalid-args", scope=scope)
    timeout_s = float(args.timeout)
    if not (math.isfinite(timeout_s) and 0.0 < timeout_s <= MAX_TIMEOUT_S):
        return _fail(FINDING_SETUP, "invalid-args", scope=scope)

    if not _INT_RE.fullmatch(args.max_bytes):
        return _fail(FINDING_SETUP, "invalid-args", scope=scope)
    max_bytes = int(args.max_bytes)
    if not (0 < max_bytes <= CEIL_MAX_BYTES):
        return _fail(FINDING_SETUP, "invalid-args", scope=scope)

    raw, reason = _read_anchor(args.anchor)
    if raw is None:
        return _fail(FINDING_SETUP, reason, scope=scope)
    anchor, reason = _validate_anchor(raw)
    if anchor is None:
        return _fail(FINDING_SETUP, reason, scope=scope)
    # Fingerprint only bytes that passed schema validation: rejected content
    # may be an arbitrary small file and must not be fingerprinted.
    anchor_sha256 = _sha256_bytes(raw)
    if anchor["scope"] != scope:
        return _fail(
            FINDING_SETUP, "anchor-scope-mismatch", scope=scope,
            anchor_sha256=anchor_sha256,
        )

    journalctl, reason = _resolve_journalctl(args.journalctl)
    if journalctl is None:
        return _fail(
            FINDING_UNAVAILABLE, reason, scope=scope, anchor_sha256=anchor_sha256
        )

    scope_flag = "--system" if scope == "system" else "--user"
    argv = [
        journalctl,
        scope_flag,
        "--no-pager",
        "--quiet",
        "--no-tail",
        "--output=json",
        "--output-fields=" + OUTPUT_FIELDS,
        "--cursor=" + anchor["cursor"],
    ]

    cap = _capture(argv, timeout_s, max_bytes)
    if "error" in cap:
        return _fail(
            FINDING_UNAVAILABLE, cap["error"], scope=scope,
            anchor_sha256=anchor_sha256,
        )

    # Fixed reason priority: overflow > stderr > timeout > rc > parse.
    if cap["overflow"]:
        return _fail(
            FINDING_UNAVAILABLE, "overflow", scope=scope,
            anchor_sha256=anchor_sha256,
        )
    if cap["err_len"] > 0:
        return _fail(
            FINDING_UNAVAILABLE, "stderr-nonempty", scope=scope,
            anchor_sha256=anchor_sha256,
        )
    if cap["timed_out"]:
        return _fail(
            FINDING_UNAVAILABLE, "timeout", scope=scope,
            anchor_sha256=anchor_sha256,
        )
    if cap["rc"] != 0:
        return _fail(
            FINDING_UNAVAILABLE, "rc-nonzero", scope=scope,
            anchor_sha256=anchor_sha256,
        )

    records, reason = _parse_records(cap["out"])
    if records is None:
        return _fail(
            FINDING_UNAVAILABLE, reason, scope=scope,
            anchor_sha256=anchor_sha256,
        )

    reason, stats = _evaluate(records, anchor)
    if reason is not None:
        return _fail(
            FINDING_UNAVAILABLE, reason, scope=scope,
            anchor_sha256=anchor_sha256,
        )

    end_cursor_sha256 = None
    if stats["last_cursor"] is not None:
        end_cursor_sha256 = _sha256_bytes(stats["last_cursor"].encode("utf-8"))

    _emit(
        {
            "finding_id": FINDING_OK,
            "scope": scope,
            "anchor_sha256": anchor_sha256,
            "records_after_anchor": stats["records_after_anchor"],
            "positive_kernel_oom": stats["positive_kernel_oom"],
            "positive_unit_oom": stats["positive_unit_oom"],
            "positive_unit_signal": stats["positive_unit_signal"],
            "positive_process_sigkill": stats["positive_process_sigkill"],
            "evidence_basis": "validated-record-subsets",
            "end_cursor_sha256": end_cursor_sha256,
            "cursor_semantics": "byte-equality-acceptance-only",
        }
    )
    return 0


_STUB = """#!/bin/sh
# Isolated selftest journalctl stub. Never reads the journal.
printf '%s\\n' "$@" > "${MJW_ARGV_FILE:-/dev/null}" 2>/dev/null
if [ -n "$MJW_STDOUT_FILE" ]; then
    cat "$MJW_STDOUT_FILE"
fi
if [ -n "$MJW_FLOOD" ]; then
    head -c "$MJW_FLOOD" /dev/zero
fi
if [ -n "$MJW_STDERR" ]; then
    printf '%s' "$MJW_STDERR" >&2
fi
if [ -n "$MJW_STDERR_FLOOD" ]; then
    head -c "$MJW_STDERR_FLOOD" /dev/zero >&2
fi
if [ -n "$MJW_SLEEP" ]; then
    sleep "$MJW_SLEEP"
fi
exit "${MJW_RC:-0}"
"""

_BOOT = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
_ANCHOR_CURSOR = "s=selftest0000000001;i=1;b=" + _BOOT + ";m=1;t=1;x=1"


def _selftest_case_lines(*records):
    return "".join(r + "\n" for r in records)


def _rec(cursor, **fields):
    obj = {"__CURSOR": cursor, "_BOOT_ID": _BOOT}
    obj.update(fields)
    return json.dumps(obj)


def _run_selftest():
    tool = os.path.abspath(__file__)
    failures = []

    kernel = _rec(
        "s=st2;i=2", MESSAGE_ID="fe6faa94e7774663a0da52717891d8ef"
    )
    unit_oom = _rec(
        "s=st3;i=3",
        MESSAGE_ID="d9b373ed55a64feb8242e02dbe79a49c",
        UNIT_RESULT="oom-kill",
    )
    unit_sig = _rec(
        "s=st4;i=4",
        MESSAGE_ID="d9b373ed55a64feb8242e02dbe79a49c",
        UNIT_RESULT="signal",
    )
    sigkill = _rec(
        "s=st5;i=5",
        MESSAGE_ID="98e322203f7a4ed290d09fe03c09fe15",
        EXIT_CODE="killed",
        EXIT_STATUS="9",
    )

    cases = [
        {
            "id": "ok-empty-window",
            "stdout": _selftest_case_lines(_rec(_ANCHOR_CURSOR)),
            "want_rc": 0,
            "want_id": FINDING_OK,
            "want": {"records_after_anchor": 0, "positive_kernel_oom": 0},
        },
        {
            "id": "ok-positives-all-classes",
            "stdout": _selftest_case_lines(
                _rec(_ANCHOR_CURSOR), kernel, unit_oom, unit_sig, sigkill
            ),
            "want_rc": 0,
            "want_id": FINDING_OK,
            "want": {
                "records_after_anchor": 4,
                "positive_kernel_oom": 1,
                "positive_unit_oom": 1,
                "positive_unit_signal": 1,
                "positive_process_sigkill": 1,
                "evidence_basis": "validated-record-subsets",
            },
            "check_argv": True,
        },
        {
            "id": "setup-anchor-bad-schema",
            "anchor": {"schema": "other", "scope": "user",
                       "boot_id": _BOOT, "cursor": _ANCHOR_CURSOR},
            "stdout": _selftest_case_lines(_rec(_ANCHOR_CURSOR)),
            "want_rc": 2,
            "want_id": FINDING_SETUP,
        },
        {
            "id": "setup-anchor-scope-mismatch",
            "anchor": {"schema": ANCHOR_SCHEMA, "scope": "system",
                       "boot_id": _BOOT, "cursor": _ANCHOR_CURSOR},
            "stdout": _selftest_case_lines(_rec(_ANCHOR_CURSOR)),
            "want_rc": 2,
            "want_id": FINDING_SETUP,
        },
        {
            "id": "setup-anchor-file-missing",
            "no_anchor_file": True,
            "stdout": "",
            "want_rc": 2,
            "want_id": FINDING_SETUP,
        },
        {
            "id": "unavailable-empty-capture",
            "stdout": "",
            "want_rc": 2,
            "want_id": FINDING_UNAVAILABLE,
        },
        {
            "id": "unavailable-anchor-not-first",
            "stdout": _selftest_case_lines(
                _rec("s=other;i=9", MESSAGE_ID="fe6faa94e7774663a0da52717891d8ef")
            ),
            "want_rc": 2,
            "want_id": FINDING_UNAVAILABLE,
        },
        {
            "id": "unavailable-foreign-boot",
            "stdout": _selftest_case_lines(
                _rec(_ANCHOR_CURSOR),
                _rec("s=st9;i=9").replace(_BOOT, "b" * 32),
            ),
            "want_rc": 2,
            "want_id": FINDING_UNAVAILABLE,
        },
        {
            "id": "unavailable-duplicate-cursor",
            "stdout": _selftest_case_lines(
                _rec(_ANCHOR_CURSOR),
                _rec("s=st10;i=10"),
                _rec("s=st10;i=10"),
            ),
            "want_rc": 2,
            "want_id": FINDING_UNAVAILABLE,
        },
        {
            "id": "unavailable-record-invalid",
            "stdout": _selftest_case_lines(_rec(_ANCHOR_CURSOR)) + "null\n",
            "want_rc": 2,
            "want_id": FINDING_UNAVAILABLE,
        },
        {
            "id": "unavailable-malformed-json",
            "stdout": _selftest_case_lines(_rec(_ANCHOR_CURSOR)) + "{bad\n",
            "want_rc": 2,
            "want_id": FINDING_UNAVAILABLE,
        },
        {
            "id": "unavailable-stderr",
            "stdout": _selftest_case_lines(_rec(_ANCHOR_CURSOR)),
            "stderr": "stub-stderr-canary",
            "want_rc": 2,
            "want_id": FINDING_UNAVAILABLE,
        },
        {
            "id": "unavailable-rc-nonzero",
            "stdout": _selftest_case_lines(_rec(_ANCHOR_CURSOR)),
            "rc": 5,
            "want_rc": 2,
            "want_id": FINDING_UNAVAILABLE,
        },
        {
            "id": "unavailable-timeout",
            "stdout": "",
            "sleep": 5,
            "timeout": "0.4",
            "want_rc": 2,
            "want_id": FINDING_UNAVAILABLE,
        },
        {
            "id": "unavailable-overflow",
            "stdout": "",
            "flood": 1048576,
            "max_bytes": "1024",
            "want_rc": 2,
            "want_id": FINDING_UNAVAILABLE,
        },
        {
            "id": "unavailable-stderr-overflow",
            "stdout": "",
            "stderr_flood": 65536,
            "max_bytes": "1024",
            "want_rc": 2,
            "want_id": FINDING_UNAVAILABLE,
            "want": {"reason": "overflow"},
        },
    ]

    passed = 0
    for case in cases:
        ok, detail = _run_selftest_case(tool, case)
        if ok:
            passed += 1
        else:
            failures.append({"id": case["id"], "detail": detail})

    _emit(
        {
            "finding_id": "MORI_JOURNAL_WINDOW_SELFTEST",
            "cases": len(cases),
            "passed": passed,
            "failed": len(failures),
            "failures": failures,
        }
    )
    return 0 if not failures else 2


def _run_selftest_case(tool, case):
    with tempfile.TemporaryDirectory(prefix="mori-journal-window-selftest-") as td:
        anchor_path = os.path.join(td, "anchor.json")
        stub_path = os.path.join(td, "journalctl-stub.sh")
        payload_path = os.path.join(td, "payload.jsonl")
        argv_path = os.path.join(td, "argv.txt")

        anchor = case.get(
            "anchor",
            {
                "schema": ANCHOR_SCHEMA,
                "scope": case.get("scope", "user"),
                "boot_id": _BOOT,
                "cursor": _ANCHOR_CURSOR,
            },
        )
        if not case.get("no_anchor_file"):
            with open(anchor_path, "w", encoding="utf-8") as fh:
                json.dump(anchor, fh)

        with open(payload_path, "w", encoding="utf-8") as fh:
            fh.write(case.get("stdout", ""))

        with open(stub_path, "w", encoding="utf-8") as fh:
            fh.write(_STUB)
        os.chmod(stub_path, 0o700)

        env = dict(os.environ)
        env["MJW_STDOUT_FILE"] = payload_path
        env["MJW_ARGV_FILE"] = argv_path
        if case.get("stderr"):
            env["MJW_STDERR"] = case["stderr"]
        else:
            env.pop("MJW_STDERR", None)
        if case.get("rc") is not None:
            env["MJW_RC"] = str(case["rc"])
        else:
            env.pop("MJW_RC", None)
        if case.get("sleep") is not None:
            env["MJW_SLEEP"] = str(case["sleep"])
        else:
            env.pop("MJW_SLEEP", None)
        if case.get("flood") is not None:
            env["MJW_FLOOD"] = str(case["flood"])
        else:
            env.pop("MJW_FLOOD", None)
        if case.get("stderr_flood") is not None:
            env["MJW_STDERR_FLOOD"] = str(case["stderr_flood"])
        else:
            env.pop("MJW_STDERR_FLOOD", None)

        cmd = [
            sys.executable,
            tool,
            "--anchor",
            anchor_path,
            "--scope",
            case.get("scope", "user"),
            "--journalctl",
            stub_path,
            "--timeout",
            case.get("timeout", "5"),
            "--max-bytes",
            case.get("max_bytes", str(DEFAULT_MAX_BYTES)),
        ]
        try:
            proc = subprocess.run(
                cmd,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30,
                env=env,
            )
        except subprocess.TimeoutExpired:
            return False, "outer-timeout"

        if proc.returncode != case["want_rc"]:
            return False, "rc=%r want %r" % (proc.returncode, case["want_rc"])
        try:
            out = json.loads(proc.stdout.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            return False, "stdout-not-json"
        if not isinstance(out, dict) or out.get("finding_id") != case["want_id"]:
            return False, "finding_id=%r" % out.get("finding_id")

        # No-echo invariants: raw cursor, record bytes, stderr bytes.
        blob = proc.stdout + proc.stderr
        for forbidden in (
            _ANCHOR_CURSOR.encode(), b"s=st2;i=2", b"stub-stderr-canary",
        ):
            if forbidden and forbidden in blob:
                return False, "echoed-forbidden-bytes"
        if proc.returncode == 2 and case["want_id"] == FINDING_UNAVAILABLE:
            for key in (
                "records_after_anchor",
                "positive_kernel_oom",
                "positive_unit_oom",
                "positive_unit_signal",
                "positive_process_sigkill",
            ):
                if isinstance(out.get(key), int):
                    return False, "numeric-total-on-unavailable"

        for key, want in case.get("want", {}).items():
            if out.get(key) != want:
                return False, "%s=%r want %r" % (key, out.get(key), want)

        if case.get("check_argv"):
            try:
                with open(argv_path, "r", encoding="utf-8") as fh:
                    seen = [line.rstrip("\n") for line in fh]
            except OSError:
                return False, "argv-file-missing"
            joined = "\n".join(seen)
            if "--user" not in seen or "--system" in seen:
                return False, "scope-flag-wrong"
            for needed in (
                "--no-pager",
                "--quiet",
                "--no-tail",
                "--output=json",
                "--output-fields=" + OUTPUT_FIELDS,
                "--cursor=" + _ANCHOR_CURSOR,
            ):
                if needed not in seen:
                    return False, "missing-arg:%s" % needed
            for forbidden in (
                "--after-cursor", "-f", "--follow", "--cursor-file",
                "--vacuum-size", "--vacuum-time", "--vacuum-files",
                "--rotate", "--sync", "--flush", "-b", "--boot",
            ):
                if forbidden in seen or any(
                    a.startswith(forbidden + "=") for a in seen
                ):
                    return False, "forbidden-arg:%s" % forbidden
            fields = joined.split("--output-fields=")
            if len(fields) > 1 and "MESSAGE," in fields[1].split("\n")[0]:
                return False, "message-field-requested"
        return True, ""


class _ArgError(Exception):
    """Safe argparse failure signal; never carries argv or exception text."""


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise _ArgError()


def _build_parser():
    parser = _Parser(
        description="bounded same-boot journal window probe (mori round-16)",
        add_help=False,
    )
    parser.add_argument("--anchor", default=None)
    parser.add_argument("--scope", default=None)
    parser.add_argument("--journalctl", default=None)
    parser.add_argument("--timeout", default=str(DEFAULT_TIMEOUT_S))
    parser.add_argument("--max-bytes", default=str(DEFAULT_MAX_BYTES))
    parser.add_argument("--selftest", action="store_true")
    return parser


def main(argv):
    parser = _build_parser()
    try:
        args = parser.parse_args(argv)
    except (SystemExit, _ArgError, argparse.ArgumentError):
        return _fail(FINDING_SETUP, "invalid-args")

    if args.selftest:
        return _run_selftest()

    if not args.anchor:
        return _fail(FINDING_SETUP, "invalid-args")
    return _run(args)


if __name__ == "__main__":
    try:
        _rc = main(sys.argv[1:])
    except SystemExit:
        raise
    except BaseException:
        try:
            _emit({"finding_id": FINDING_SETUP, "reason": "internal-error"})
        except BaseException:
            pass
        _rc = 2
    sys.exit(_rc)
