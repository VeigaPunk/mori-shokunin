#!/usr/bin/env python3
"""mori-round15-regressions.py — isolated fixture-pack gate for the r15 C1 repair.

WHAT THIS GATE IS

  A small verdict-producing gate for the round-15 "retain validated positives
  without fabricated totals" repair. It consumes JSON fixture packs (the shared
  six-key schema), builds each case with the round-14 helper module imported
  through a hashed compile/exec of the helper bytes (build_fixture/census_env/
  Case plus the r14 output parsers).
  runs the census under test and the pinned entering census, and grades both.

  It does NOT reimplement the census or copy the r14 harness. The imported r14
  helper digest is a verdict-driving input: a run whose helper bytes differ from
  the pinned expectation is a could-not-evaluate error (exit 2).

CLAIMS (one line per case)

  * want_oom / want_signal match one alarm line each: OOM_KILL_JOURNAL
    severity=crit (global, at most once) and KILL_SIGNAL_JOURNAL severity=warn
    (user only, at most once). Roll and rc must follow: DRIFT/1 for any alarm,
    CLEAN/0 otherwise; drift counts alarm lines.
  * invalid_class reads unavailable:<reason> on every scope that actually holds
    a record failing that class predicate. Reasons are derived independently
    from the fixture bytes (record-invalid, multi-boot, boot-mismatch),
    mirroring the census's all()/fallback shape. An empty or clean opposite
    scope is never asserted unavailable.
  * The four per-scope positive tokens positive_kernel_oom,
    positive_unit_oom, positive_unit_signal, positive_process_sigkill are
    exact integers derived independently from the fixture records (not from
    the SUT), even when the named raw aggregate is unavailable. On a capture
    or parser failure (selftest controls) the affected scope's tokens must read
    unavailable:<reason> and no alarm may fire.
  * Alarm findings preserve raw counts: their per-scope raw fields byte-equal
    the SURFACE journal tokens, an unavailable raw class stays unavailable, the
    OOM line carries no summed count=, and the KILL line's count equals its raw
    process_sigkill token. Both alarm lines carry the scoped positive evidence
    fields, positive_basis=validated-subset-lower-bound, the matching
    positive_validation label, and an alarm_basis derived from raw versus
    positive source arms.
  * Every emitted FINDING carries script_sha256 equal to the executed census
    copy, no census argv requests MESSAGE, and the PATH journalctl tripwire
    stays empty.

PINS AND TRUST

  The entering census bytes are pinned in-script by SHA-256
  0e41cb83fce2e8c5c711171e1cde2e6fa2809dcfce630eccabe52bcbe41516d9 at commit
  0fa5e0de194bcc270a927a166664113e6821442b. The bytes come from
  --frozen, else the pinned git blob `git show <commit>:tools/mori-census.sh`
  cross-checked byte-for-byte against an on-disk frozen copy when present; a
  digest mismatch is SnapshotTampered and exit 2, never a silent source switch.

  Fixture expectations are committed evidence, not derived trust. Generate the
  expected table after the packs settle:

      python3 tools/mori-round15-regressions.py \
          --pin-fixtures .ufo/waves/round-15/expected.json

  A normal run reads that file (default --expected), and refuses to evaluate
  when a fixture pack digest, a case expectation, the gate bytes, the imported
  r14 helper bytes, the frozen bytes, or the pinned constants disagree. The
  expected table records every fixture SHA-256 and the static per-case
  positive/invalid/alarm expectations. No fixture may carry a MESSAGE key.

STUB MODES (derived, never read from the pack)

  invalid_class == null                  -> r14 honor
  invalid_class == kernel_oom_notice     -> r14 dup-kernel (kernel query only
                                            ignores argv filters, so a wrong-id
                                            or array MESSAGE_ID sibling reaches
                                            the aggregate without poisoning the
                                            other class queries)
  any other non-null invalid_class       -> r14 ignore-filters (the only generic
                                            r14 mode; only the named invalid
                                            class is asserted, so collateral raw
                                            invalidation is not graded)

  All census subprocesses get the r14 census_env dictionary with MORI_BOOT_ID
  and the boot_id file forced to 11111111111111111111111111111111. Host journal
  access is impossible: MORI_JOURNALCTL_BIN always names the generated stub.

FROZEN CONTROL

  The entering census is ALWAYS run against the same fixtures; there is no CLI
  bypass. A case whose expected alarm depends on a class the frozen snapshot
  cannot see is "red-relevant". It is confirmed only when the frozen run
  completed cleanly (no timeout/exec error/tripwire/hash/surface/roll/rc/setup
  failure), carries no unwanted alarm, has roll/rc/drift consistent with its
  actual OOM/WARN lines (each at most one), and specifically misses at least one
  wanted alarm arm. A retained wanted arm is allowed: the entering witness may
  still see one source while losing the mixed-stream source. Any other frozen
  failure is control_inconclusive and exits 2; an unexpected alarm from the
  frozen snapshot is also exit 2. Every non-red case must pass the legacy
  behavior evaluator. SUT failures and frozen-control failures are reported
  separately; a frozen miss is never counted as a SUT bug.

EXIT MAP

  0  every SUT expectation passed and the frozen control reproduced the
     entering red state (red-relevant cases miss alarms; all others pass)
  1  a SUT fixture expectation failed
  2  usage/setup/pin/fixture-schema/control error: could not evaluate

Usage

  python3 tools/mori-round15-regressions.py --pin-fixtures .ufo/waves/round-15/expected.json
  python3 tools/mori-round15-regressions.py --census tools/mori-census.sh \
      --fixtures .ufo/waves/round-15/fixtures --output /tmp/r15-gate
  python3 tools/mori-round15-regressions.py --selftest
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import types
from dataclasses import dataclass
from pathlib import Path

SCHEMA = "mori-round15-regressions-v1"
EXPECTED_SCHEMA = "mori-round15-regressions-expected-v1"
REPO = Path(__file__).resolve().parent.parent
DEFAULT_CENSUS = REPO / "tools/mori-census.sh"
DEFAULT_FIXTURES = REPO / ".ufo/waves/round-15/fixtures"
DEFAULT_FROZEN = REPO / ".ufo/waves/round-15/frozen/mori-census.sh"
DEFAULT_EXPECTED = REPO / ".ufo/waves/round-15/expected.json"
R14_PATH = REPO / "tools/mori-round14-regressions.py"

PINNED_FROZEN_SHA256 = (
    "0e41cb83fce2e8c5c711171e1cde2e6fa2809dcfce630eccabe52bcbe41516d9"
)
PINNED_BASE_COMMIT = "0fa5e0de194bcc270a927a166664113e6821442b"
BOOT = "11111111111111111111111111111111"

KERNEL_ID = "fe6faa94e7774663a0da52717891d8ef"
OOMD_ID = "d989611b15e44c9dbf31e3c81256e4ed"
COREDUMP_ID = "fc2e22bc6ee647b6b90729ab34a250b1"
SIGKILL_ID = "98e322203f7a4ed290d09fe03c09fe15"
FAILURE_ID = "d9b373ed55a64feb8242e02dbe79a49c"

CLASS_IDS = {
    "kernel_oom_notice": KERNEL_ID,
    "oomd_notice": OOMD_ID,
    "coredump_notice": COREDUMP_ID,
    "segfault_signal11": COREDUMP_ID,
    "unit_sigkill_record": SIGKILL_ID,
    "unit_failure_record": FAILURE_ID,
}
POSITIVE_TOKENS = (
    "positive_kernel_oom",
    "positive_unit_oom",
    "positive_unit_signal",
    "positive_process_sigkill",
)
OOM_ID = "OOM_KILL_JOURNAL"
KILL_ID = "KILL_SIGNAL_JOURNAL"
REQUIRED_KEYS = {
    "id",
    "user",
    "system",
    "want_oom",
    "want_signal",
    "invalid_class",
}
ALLOWED_KEYS = REQUIRED_KEYS | {"capture"}
CASE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,80}$")
INT_RE = re.compile(r"^[0-9]+$")
POS_INT_RE = re.compile(r"^[1-9][0-9]*$")


class SetupError(Exception):
    """Usage, fixture, expected-table or pin failure: exit 2."""


class SnapshotTampered(SetupError):
    """Pinned frozen/helper/fixture bytes do not match: exit 2."""


R14 = None  # set by load_r14(); the imported r14 helper module


# ---------------------------------------------------------------------------
# small utilities
# ---------------------------------------------------------------------------


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rel_or_abs(path: Path) -> str:
    path = Path(path).resolve()
    try:
        return str(path.relative_to(REPO))
    except ValueError:
        return str(path)


def atomic_json(path: Path, obj) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    os.replace(tmp, path)


def atomic_bytes(path: Path, data: bytes, mode: int | None = None) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(data)
    if mode is not None:
        tmp.chmod(mode)
    os.replace(tmp, path)


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def one_line(text, limit=520) -> str:
    cleaned = " ".join(str(text).split())
    return cleaned if len(cleaned) <= limit else cleaned[: limit - 3] + "..."


def has_message_key(obj) -> bool:
    if isinstance(obj, dict):
        if "MESSAGE" in obj:
            return True
        return any(has_message_key(value) for value in obj.values())
    if isinstance(obj, list):
        return any(has_message_key(value) for value in obj)
    return False


def status_is_9(value) -> bool:
    """Scalar status 9: integer 9 or string "9"; bool/float/array/null rejected.

    The r14 stub filters on str(value) == "9", so a float 9.0 is not delivered
    by honor filtering; rejecting it keeps the static expectation aligned.
    """
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return value == 9
    if isinstance(value, str):
        return value == "9"
    return False


def signal_is_11(value) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return value == 11
    if isinstance(value, str):
        return value == "11"
    return False


# ---------------------------------------------------------------------------
# r14 helper import (verdict-driving input)
# ---------------------------------------------------------------------------


def load_r14():
    """Read the helper bytes once, hash them, and execute exactly those bytes.

    No SourceFileLoader/__pycache__ path is used: compile/exec on the bytes that
    were hashed removes the bytecode-vs-source window from the verdict input.
    """
    global R14
    if not R14_PATH.is_file():
        raise SetupError("r14 helper module not readable: %s" % R14_PATH)
    data = R14_PATH.read_bytes()
    digest = sha256_bytes(data)
    name = "_mori_round14_helpers"
    module = types.ModuleType(name)
    module.__file__ = str(R14_PATH)
    module.__package__ = ""
    sys.modules[name] = module
    try:
        code = compile(data, str(R14_PATH), "exec")
        exec(code, module.__dict__)  # noqa: S102 - explicit hashed local input
    except Exception as exc:  # noqa: BLE001 - setup failure, not a verdict
        sys.modules.pop(name, None)
        raise SetupError(
            "r14 helper import failed: %s: %s" % (type(exc).__name__, exc)
        )
    needed = (
        "Case",
        "build_fixture",
        "census_env",
        "verdict_roll",
        "surface_rows",
        "findings",
        "read_argv_log",
        "message_argv_violations",
        "journal_stub_body",
        "sha256_file",
        "redact",
    )
    missing = [name for name in needed if not hasattr(module, name)]
    if missing:
        raise SetupError(
            "r14 helper module lacks required symbol(s): %s" % ",".join(missing)
        )
    # The census must never fall back to the host journal through this gate.
    probe = module.census_env(Path("/nonexistent-r15-probe"))
    if not probe.get("MORI_JOURNALCTL_BIN"):
        raise SetupError("r14 census_env has no MORI_JOURNALCTL_BIN stub binding")
    R14 = module
    return module, digest


# ---------------------------------------------------------------------------
# fixture loading and independent expectations
# ---------------------------------------------------------------------------


@dataclass
class CaseSpec:
    cid: str
    pack: str
    user: tuple
    system: tuple
    want_oom: bool
    want_signal: bool
    invalid_token: object  # raw invalid_class (str | None)
    invalid_cls: object  # bare class (str | None)
    mode: str
    capture: object
    positives: dict
    invalid: dict
    red_relevant: bool
    user_rc: int
    system_rc: int
    user_stderr: str
    system_stderr: str

    def expectation(self) -> dict:
        return {
            "id": self.cid,
            "pack": self.pack,
            "want_oom": self.want_oom,
            "want_signal": self.want_signal,
            "invalid_class": self.invalid_cls,
            "mode": self.mode,
            "capture": self.capture,
            "positives": self.positives,
            "invalid": self.invalid,
            "red_relevant": self.red_relevant,
        }


def split_invalid(raw):
    if raw is None:
        return None
    if not isinstance(raw, str) or not raw:
        raise SetupError("invalid_class must be a nonempty string or null")
    scope = None
    cls = raw
    if ":" in raw:
        prefix, rest = raw.split(":", 1)
        if prefix in ("user", "system"):
            scope, cls = prefix, rest
    if cls not in CLASS_IDS:
        raise SetupError("unknown invalid_class value: %s" % raw)
    return (scope, cls)


def normalize_capture(raw):
    if raw is None:
        return None
    if not isinstance(raw, dict):
        raise SetupError("capture must be an object")
    kind = raw.get("kind")
    if kind == "malformed":
        return {
            "kind": "malformed",
            "scope": None,
            "status": "malformed-json",
            "scopes": ["user", "system"],
        }
    if kind not in ("rc", "stderr"):
        raise SetupError("unknown capture kind: %r" % (kind,))
    scope = raw.get("scope")
    if scope not in ("user", "system"):
        raise SetupError("capture scope must be user or system")
    if kind == "rc":
        rc = raw.get("rc")
        if isinstance(rc, bool) or not isinstance(rc, int) or not 1 <= rc <= 255:
            raise SetupError("capture rc must be an integer 1..255")
        status = "timeout" if rc in (124, 137) else "rc-%d" % rc
        return {"kind": "rc", "scope": scope, "status": status,
                "scopes": [scope], "rc": rc}
    return {"kind": "stderr", "scope": scope,
            "status": "stderr-nonempty", "scopes": [scope]}


def record_matches(rec, cls) -> bool:
    """Strict per-record predicate: current scalar boot + scalar MESSAGE_ID."""
    if not isinstance(rec, dict):
        return False
    boot = rec.get("_BOOT_ID")
    mid = rec.get("MESSAGE_ID")
    if not isinstance(boot, str) or boot != BOOT:
        return False
    if not isinstance(mid, str) or mid != CLASS_IDS[cls]:
        return False
    if cls == "segfault_signal11":
        return signal_is_11(rec.get("COREDUMP_SIGNAL"))
    if cls == "unit_sigkill_record":
        return (rec.get("EXIT_CODE") == "killed"
                and status_is_9(rec.get("EXIT_STATUS")))
    return True


def derive_unavailable(records, cls):
    """Return the census fallback status when this class query is invalid."""
    if not any(not record_matches(rec, cls) for rec in records):
        return None
    if not all(
        isinstance(rec, dict)
        and isinstance(rec.get("_BOOT_ID"), str)
        and len(rec["_BOOT_ID"]) > 0
        for rec in records
    ):
        return "record-invalid"
    boots = sorted({rec["_BOOT_ID"] for rec in records})
    if len(boots) > 1:
        return "multi-boot"
    if boots[0] == BOOT:
        return "record-invalid"
    return "boot-mismatch"


def stub_matches(rec, cls) -> bool:
    """r14 journal_stub_body honor-mode FIELD=value filtering (str compare)."""
    if not isinstance(rec, dict):
        return False
    if str(rec.get("MESSAGE_ID")) != CLASS_IDS[cls]:
        return False
    if cls == "segfault_signal11":
        return str(rec.get("COREDUMP_SIGNAL")) == "11"
    if cls == "unit_sigkill_record":
        return (str(rec.get("EXIT_CODE")) == "killed"
                and str(rec.get("EXIT_STATUS")) == "9")
    return True


def class_query_available(records, cls, mode) -> bool:
    """Would the whole-stream aggregate for this class in this scope be ok?

    This mirrors r14 stub filtering plus the census all() validation. It is
    used only to decide whether the frozen snapshot would still see a source,
    so a mixed case whose alarm survives through another class is not claimed
    as red. Under ignore-filters every record reaches every class query; under
    dup-kernel only the kernel query ignores filters.
    """
    if mode == "ignore-filters":
        query_set = list(records)
    elif mode == "dup-kernel" and cls == "kernel_oom_notice":
        query_set = list(records)
    else:
        query_set = [rec for rec in records if stub_matches(rec, cls)]
    return all(record_matches(rec, cls) for rec in query_set)


def count_positives(records):
    kernel = sum(1 for rec in records if record_matches(rec, "kernel_oom_notice"))
    unit_oom = 0
    unit_signal = 0
    for rec in records:
        if not record_matches(rec, "unit_failure_record"):
            continue
        result = rec.get("UNIT_RESULT")
        if not isinstance(result, str):
            continue
        if result == "oom-kill":
            unit_oom += 1
        elif result == "signal":
            unit_signal += 1
    process = sum(1 for rec in records if record_matches(rec, "unit_sigkill_record"))
    return {
        "positive_kernel_oom": kernel,
        "positive_unit_oom": unit_oom,
        "positive_unit_signal": unit_signal,
        "positive_process_sigkill": process,
    }


def mode_for(invalid_cls, capture):
    if capture:
        return "malformed" if capture["kind"] == "malformed" else "honor"
    if invalid_cls is None:
        return "honor"
    if invalid_cls == "kernel_oom_notice":
        return "dup-kernel"
    return "ignore-filters"


def analyze_case(pack_name: str, obj: dict) -> CaseSpec:
    if not isinstance(obj, dict):
        raise SetupError("%s: case is not an object" % pack_name)
    unknown = set(obj) - ALLOWED_KEYS
    if unknown:
        raise SetupError("%s: case has unknown key(s): %s"
                         % (pack_name, ",".join(sorted(unknown))))
    missing = REQUIRED_KEYS - set(obj)
    if missing:
        raise SetupError("%s: case lacks key(s): %s"
                         % (pack_name, ",".join(sorted(missing))))
    cid = obj.get("id")
    if not isinstance(cid, str) or not CASE_ID_RE.match(cid):
        raise SetupError("%s: unsafe or missing case id: %r" % (pack_name, cid))
    user = obj.get("user")
    system = obj.get("system")
    if not isinstance(user, list) or not isinstance(system, list):
        raise SetupError("%s/%s: user and system must be lists" % (pack_name, cid))
    want_oom = obj.get("want_oom")
    want_signal = obj.get("want_signal")
    if not isinstance(want_oom, bool) or not isinstance(want_signal, bool):
        raise SetupError("%s/%s: want_oom/want_signal must be booleans"
                         % (pack_name, cid))
    if has_message_key(user) or has_message_key(system):
        raise SetupError("%s/%s: fixture records may not carry a MESSAGE key"
                         % (pack_name, cid))
    raw_invalid = obj.get("invalid_class")
    split = split_invalid(raw_invalid)
    capture = normalize_capture(obj.get("capture"))
    invalid_scope, invalid_cls = split if split is not None else (None, None)
    if capture is not None:
        if invalid_cls is not None:
            raise SetupError("%s/%s: capture-control cases cannot expect an "
                             "invalid aggregate" % (pack_name, cid))
    mode = mode_for(invalid_cls, capture)

    user_counts = count_positives(user)
    system_counts = count_positives(system)
    positives = {"user": user_counts, "system": system_counts}

    # A failed capture makes every positive token in that scope unavailable;
    # it never becomes a fabricated zero.
    if capture is not None:
        for scope in capture["scopes"]:
            positives[scope] = {
                token: "unavailable:" + capture["status"]
                for token in POSITIVE_TOKENS
            }

    oom_triggers = []
    signal_triggers = []
    failed_scopes = capture["scopes"] if capture is not None else ()
    for scope, counts in (("user", user_counts), ("system", system_counts)):
        if scope in failed_scopes:
            continue
        if counts["positive_kernel_oom"] > 0:
            oom_triggers.append((scope, "positive_kernel_oom"))
        if counts["positive_unit_oom"] > 0:
            oom_triggers.append((scope, "positive_unit_oom"))
    if "user" not in failed_scopes and user_counts["positive_unit_signal"] > 0:
        signal_triggers.append(("user", "positive_unit_signal"))
    if "user" not in failed_scopes and user_counts["positive_process_sigkill"] > 0:
        signal_triggers.append(("user", "positive_process_sigkill"))

    if want_oom != bool(oom_triggers):
        raise SetupError(
            "%s/%s: want_oom=%s contradicts independently valid OOM records=%d"
            % (pack_name, cid, want_oom, len(oom_triggers))
        )
    if want_signal != bool(signal_triggers):
        raise SetupError(
            "%s/%s: want_signal=%s contradicts independently valid USER "
            "signal records=%d" % (pack_name, cid, want_signal,
                                   len(signal_triggers))
        )

    invalid = {}
    if invalid_cls is not None:
        scopes = [invalid_scope] if invalid_scope else ["user", "system"]
        for scope in scopes:
            reason = derive_unavailable(
                {"user": user, "system": system}[scope], invalid_cls
            )
            if reason is not None:
                invalid[scope] = reason
        if not invalid:
            raise SetupError(
                "%s/%s: invalid_class=%s names no actually failing record"
                % (pack_name, cid, invalid_cls)
            )

    # red_relevant: every independently valid alarm source for an expected
    # alarm is hidden because its class aggregate is unavailable in that scope.
    # Availability mirrors the selected stub mode and the census all()
    # validation, so collateral invalidation under ignore-filters counts.
    records_by_scope = {"user": user, "system": system}

    def source_hidden(scope, token):
        if token == "positive_kernel_oom":
            cls = "kernel_oom_notice"
        elif token in ("positive_unit_oom", "positive_unit_signal"):
            cls = "unit_failure_record"
        elif token == "positive_process_sigkill":
            cls = "unit_sigkill_record"
        else:  # pragma: no cover - fixed token set above
            return False
        return not class_query_available(records_by_scope[scope], cls, mode)

    oom_red = bool(want_oom) and bool(oom_triggers) and all(
        source_hidden(scope, token) for scope, token in oom_triggers
    )
    signal_red = bool(want_signal) and bool(signal_triggers) and all(
        source_hidden(scope, token) for scope, token in signal_triggers
    )

    user_rc = system_rc = 0
    user_stderr = system_stderr = ""
    if capture is not None and capture["kind"] == "rc":
        if capture["scope"] == "user":
            user_rc = capture["rc"]
        else:
            system_rc = capture["rc"]
    if capture is not None and capture["kind"] == "stderr":
        text = "synthetic round15 producer stderr\n"
        if capture["scope"] == "user":
            user_stderr = text
        else:
            system_stderr = text

    return CaseSpec(
        cid=cid,
        pack=pack_name,
        user=tuple(user),
        system=tuple(system),
        want_oom=want_oom,
        want_signal=want_signal,
        invalid_token=raw_invalid,
        invalid_cls=invalid_cls,
        mode=mode,
        capture=capture,
        positives=positives,
        invalid=invalid,
        red_relevant=bool(oom_red or signal_red),
        user_rc=user_rc,
        system_rc=system_rc,
        user_stderr=user_stderr,
        system_stderr=system_stderr,
    )


def load_packs(fixtures_dir: Path):
    if not fixtures_dir.is_dir():
        raise SetupError("fixtures directory not readable: %s" % fixtures_dir)
    paths = sorted(fixtures_dir.glob("*.json"))
    if not paths:
        raise SetupError("no fixture packs under %s" % fixtures_dir)
    specs = []
    entries = []
    seen = {}
    for path in paths:
        try:
            raw = path.read_bytes()
        except OSError as exc:
            raise SetupError("cannot read fixture pack %s: %s" % (path, exc))
        try:
            data = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise SetupError("fixture pack %s is not valid UTF-8 JSON: %s"
                             % (path, exc))
        if not isinstance(data, list) or not data:
            raise SetupError("fixture pack %s must be a nonempty JSON list"
                             % path.name)
        case_rows = []
        for obj in data:
            spec = analyze_case(path.name, obj)
            if spec.cid in seen:
                raise SetupError(
                    "duplicate case id %s in %s and %s"
                    % (spec.cid, seen[spec.cid], path.name)
                )
            seen[spec.cid] = path.name
            specs.append(spec)
            case_rows.append(spec.expectation())
        entries.append({
            "name": path.name,
            "sha256": sha256_bytes(raw),
            "cases": case_rows,
        })
    return specs, entries


# ---------------------------------------------------------------------------
# frozen pin materialisation
# ---------------------------------------------------------------------------


def _verify_frozen_bytes(data: bytes, source: str) -> str:
    digest = sha256_bytes(data)
    if digest != PINNED_FROZEN_SHA256:
        raise SnapshotTampered(
            "frozen census sha256=%s expected=%s source=%s"
            % (digest, PINNED_FROZEN_SHA256, source)
        )
    if b"positive_kernel_oom" in data:
        raise SnapshotTampered(
            "pinned frozen bytes already carry r15 positive metadata: %s"
            % source
        )
    return digest


def resolve_frozen(args):
    """Return (bytes, digest, source). Never trusts a mutable manifest.

    The immutable source is the pinned commit's blob; a present on-disk frozen
    copy is cross-checked against it and may only be used when git cannot
    materialize the blob.
    """
    if args.frozen:
        path = Path(args.frozen).resolve()
        if not path.is_file():
            raise SetupError("frozen census not readable: %s" % path)
        data = path.read_bytes()
        source = "path:" + rel_or_abs(path)
        return data, _verify_frozen_bytes(data, source), source

    try:
        data = _git(["show", "%s:tools/mori-census.sh" % PINNED_BASE_COMMIT])
    except SetupError as exc:
        # Only a git materialization failure may fall back to the on-disk copy.
        if DEFAULT_FROZEN.is_file():
            data = DEFAULT_FROZEN.read_bytes()
            source = "path:" + rel_or_abs(DEFAULT_FROZEN)
            return data, _verify_frozen_bytes(data, source), source
        raise SetupError(
            "cannot materialize pinned frozen census from commit %s: %s"
            % (PINNED_BASE_COMMIT, exc)
        ) from exc

    source = "git:%s:tools/mori-census.sh" % PINNED_BASE_COMMIT
    # A failed pin check on the git blob is SnapshotTampered and must propagate;
    # it is never a reason to silently switch provenance.
    digest = _verify_frozen_bytes(data, source)
    if DEFAULT_FROZEN.is_file():
        local = DEFAULT_FROZEN.read_bytes()
        local_digest = _verify_frozen_bytes(
            local, "path:" + rel_or_abs(DEFAULT_FROZEN)
        )
        if local_digest != digest or local != data:
            raise SnapshotTampered(
                "on-disk frozen copy differs from the pinned git blob"
            )
    return data, digest, source


# ---------------------------------------------------------------------------
# revision provenance (paths only; never file contents)
# ---------------------------------------------------------------------------


def _git(args, timeout=60):
    env = {k: v for k, v in os.environ.items()}
    env["GIT_OPTIONAL_LOCKS"] = "0"
    try:
        proc = subprocess.run(
            ["git", "-c", "core.fsmonitor=false", "-C", str(REPO),
             "--no-optional-locks", *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise SetupError("git %s failed: %s" % (" ".join(args), exc))
    if proc.returncode != 0:
        raise SetupError(
            "git %s failed rc=%d: %s"
            % (" ".join(args), proc.returncode,
               proc.stderr.decode("utf-8", "replace").strip()[:300])
        )
    return proc.stdout


def capture_revision(phase: str, output: Path | None = None) -> dict:
    head = _git(["rev-parse", "HEAD"]).decode("ascii", "replace").strip()
    raw = _git(["status", "--porcelain=v1", "-z", "--untracked-files=all"])
    paths = []
    entries = raw.split(b"\0")
    i = 0
    while i < len(entries):
        entry = entries[i]
        i += 1
        if len(entry) < 4:
            continue
        status = entry[:2].decode("ascii", "replace")
        # XY<space>PATH; a rename/copy is followed by the original path with
        # no status prefix of its own.
        paths.append(entry[3:].decode("utf-8", "replace"))
        if status[0] in ("R", "C") and i < len(entries):
            old = entries[i]
            i += 1
            if old:
                paths.append(old.decode("utf-8", "replace"))
    paths = sorted(set(paths))
    excluded_prefixes = []
    outside = list(paths)
    if output is not None:
        try:
            out_rel = str(Path(output).resolve().relative_to(REPO))
        except ValueError:
            out_rel = None
        if out_rel:
            excluded_prefixes = [out_rel + "/", out_rel]
            outside = [
                p for p in paths
                if not (p == out_rel or p.startswith(out_rel + "/"))
            ]
    return {
        "phase": phase,
        "head": head,
        "pinned_base_commit": PINNED_BASE_COMMIT,
        "head_is_pinned_base": head == PINNED_BASE_COMMIT,
        "dirty": bool(paths),
        "dirty_path_count": len(paths),
        "dirty_paths": paths,
        "dirty_outside_harness_output": bool(outside),
        "dirty_outside_harness_output_count": len(outside),
        "dirty_outside_harness_output_paths": outside,
        "output_scope": {
            "excluded_prefixes": excluded_prefixes,
            "note": "paths only; fixture/frozen/census inputs are never excluded",
        },
        "status_mode": "porcelain-v1-z-untracked-all-paths-only",
    }


def revision_compare_core(rev: dict) -> dict:
    """The stable compare: observed HEAD + dirty scope outside harness output.

    Full dirty_paths and content digests are retained separately; output files
    created during the run must not make the revision look unstable.
    """
    return {
        "head": rev["head"],
        "dirty_outside_harness_output_paths":
            rev["dirty_outside_harness_output_paths"],
    }


# ---------------------------------------------------------------------------
# expected manifest
# ---------------------------------------------------------------------------


def build_expected(gate_sha: str, r14_sha: str, frozen_sha: str,
                   frozen_source: str, fixtures) -> dict:
    return {
        "schema": EXPECTED_SCHEMA,
        "base_commit": PINNED_BASE_COMMIT,
        "pinned_frozen_sha256": PINNED_FROZEN_SHA256,
        "frozen_sha256": frozen_sha,
        "frozen_source": frozen_source,
        "gate_sha256": gate_sha,
        "r14_helper": rel_or_abs(R14_PATH),
        "r14_helper_sha256": r14_sha,
        "fixtures": fixtures,
    }


def compare_expected(exp: dict, current: dict, gate_sha: str, r14_sha: str,
                     frozen_sha: str) -> None:
    if exp.get("schema") != EXPECTED_SCHEMA:
        raise SetupError("expected table has wrong schema: %r"
                         % exp.get("schema"))
    if exp.get("base_commit") != PINNED_BASE_COMMIT:
        raise SnapshotTampered("expected base_commit disagrees with the pin")
    if exp.get("pinned_frozen_sha256") != PINNED_FROZEN_SHA256:
        raise SnapshotTampered("expected frozen pin disagrees with the pin")
    if exp.get("gate_sha256") != gate_sha:
        raise SnapshotTampered(
            "gate bytes changed since expected table was pinned "
            "(expected=%s current=%s); re-run --pin-fixtures"
            % (exp.get("gate_sha256"), gate_sha)
        )
    if exp.get("r14_helper_sha256") != r14_sha:
        raise SnapshotTampered(
            "imported r14 helper bytes changed since pin "
            "(expected=%s current=%s); re-run --pin-fixtures"
            % (exp.get("r14_helper_sha256"), r14_sha)
        )
    if exp.get("frozen_sha256") != frozen_sha:
        raise SnapshotTampered(
            "frozen bytes differ from the expected table (expected=%s current=%s)"
            % (exp.get("frozen_sha256"), frozen_sha)
        )
    exp_fix = {entry["name"]: entry for entry in exp.get("fixtures", [])}
    cur_fix = {entry["name"]: entry for entry in current["fixtures"]}
    if set(exp_fix) != set(cur_fix):
        raise SnapshotTampered(
            "fixture pack set changed since pin (expected=%s current=%s)"
            % (sorted(exp_fix), sorted(cur_fix))
        )
    for name in sorted(exp_fix):
        if exp_fix[name].get("sha256") != cur_fix[name].get("sha256"):
            raise SnapshotTampered(
                "fixture pack %s changed since pin (expected=%s current=%s)"
                % (name, exp_fix[name].get("sha256"),
                   cur_fix[name].get("sha256"))
            )
        if canonical(exp_fix[name].get("cases")) != canonical(
                cur_fix[name].get("cases")):
            raise SnapshotTampered(
                "fixture pack %s expectations changed since pin" % name
            )


# ---------------------------------------------------------------------------
# execution and grading
# ---------------------------------------------------------------------------


@dataclass
class Target:
    label: str
    source: str
    executed: Path
    sha256: str


def materialize_target(label: str, source: str, data: bytes,
                       output: Path) -> Target:
    executed = output / "targets" / ("%s.mori-census.sh" % label)
    atomic_bytes(executed, data, mode=0o755)
    digest = sha256_file(executed)
    if digest != sha256_bytes(data):
        raise SetupError("%s executed copy digest drifted" % label)
    return Target(label=label, source=source, executed=executed, sha256=digest)


def build_case_fixture(root: Path, spec: CaseSpec, r14) -> None:
    if root.is_symlink():
        raise SetupError("case fixture root must not be a symlink: %s" % root)
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True, exist_ok=False)
    case = r14.Case(
        cid=spec.cid,
        title=spec.cid,
        user=spec.user,
        system=spec.system,
        mode=spec.mode,
        user_rc=spec.user_rc,
        system_rc=spec.system_rc,
        user_stderr=spec.user_stderr,
        system_stderr=spec.system_stderr,
    )
    r14.build_fixture(root, case)
    # r14's build_common/census_env predate the shared r15 boot literal. Force
    # both the file and the env-visible expected boot to the shared value.
    (root / "boot_id").write_text(BOOT + "\n", encoding="utf-8")


def fixture_env(root: Path, r14) -> dict:
    env = r14.census_env(root)
    env["MORI_BOOT_ID"] = BOOT
    env["MORI_BOOT_ID_FILE"] = str(root / "boot_id")
    return env


def reset_probe_logs(root: Path) -> None:
    for name in ("argv.log", "tripwire.log"):
        path = root / "journal" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")


def execute_census(target: Target, root: Path, env: dict, output: Path,
                   run_id: str, timeout: int):
    argv = ["bash", str(target.executed)]
    started = time.monotonic()
    timed_out = False
    error = None
    raw_out = raw_err = ""
    rc = None
    try:
        proc = subprocess.Popen(
            argv,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={str(k): str(v) for k, v in env.items()},
            cwd=str(root),
            text=True,
            encoding="utf-8",
            errors="replace",
            start_new_session=True,
        )
    except OSError as exc:
        error = "%s: %s" % (type(exc).__name__, exc)
        proc = None
    if proc is not None:
        try:
            raw_out, raw_err = proc.communicate(timeout=timeout)
            rc = proc.returncode
        except subprocess.TimeoutExpired:
            timed_out = True
            try:
                os.killpg(os.getpgid(proc.pid), 9)
            except (ProcessLookupError, PermissionError):
                pass
            raw_out, raw_err = proc.communicate()
            rc = proc.returncode
    duration_ms = int((time.monotonic() - started) * 1000)
    out_path = output / "runs" / (run_id + ".stdout")
    err_path = output / "runs" / (run_id + ".stderr")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(raw_out or "", encoding="utf-8")
    err_path.write_text(raw_err or "", encoding="utf-8")
    record = {
        "run": run_id,
        "target": target.label,
        "argv": argv,
        "cwd": str(root),
        "rc": rc,
        "timed_out": timed_out,
        "error": error,
        "duration_ms": duration_ms,
        "stdout_path": rel_or_abs(out_path),
        "stderr_path": rel_or_abs(err_path),
        "stdout_sha256": sha256_bytes((raw_out or "").encode("utf-8")),
        "stderr_sha256": sha256_bytes((raw_err or "").encode("utf-8")),
    }
    return raw_out or "", raw_err or "", rc, timed_out, error, record


def evaluate(spec: CaseSpec, out: str, err: str, rc, timed_out, error,
             target: Target, argv_rows, tripwire: str, profile: str):
    """Return (ok, reasons, observed). Never echoes fixture record bytes."""
    reasons = []
    word, vreason, counts = R14.verdict_roll(out, rc)
    want_word = "DRIFT" if (spec.want_oom or spec.want_signal) else "CLEAN"
    want_rc = 1 if want_word == "DRIFT" else 0
    want_drift = int(spec.want_oom) + int(spec.want_signal)

    if timed_out:
        reasons.append("harness_timeout")
    if error:
        reasons.append("exec_error")
    if rc != want_rc:
        reasons.append("rc=%s want=%s" % (rc, want_rc))
    if word != want_word:
        reasons.append("verdict=%s/%s want=%s" % (word, vreason, want_word))
    elif vreason != "ok":
        reasons.append("verdict_reason=%s" % vreason)
    if counts["drift"] != want_drift:
        reasons.append("drift=%d want=%d" % (counts["drift"], want_drift))
    if tripwire.strip():
        reasons.append("bare_journalctl_tripwire")
    violations = R14.message_argv_violations(argv_rows)
    if violations:
        reasons.append("census_requested_MESSAGE")
    if len(argv_rows) > 12:
        reasons.append("journal_query_calls=%d want<=12 (no extra query)"
                       % len(argv_rows))

    rows = R14.findings(out)
    oom = [row for row in rows if row["id"] == OOM_ID]
    kill = [row for row in rows if row["id"] == KILL_ID]
    if len(oom) != int(spec.want_oom):
        reasons.append("oom_lines=%d want=%d" % (len(oom), int(spec.want_oom)))
    if len(kill) != int(spec.want_signal):
        reasons.append("kill_lines=%d want=%d"
                       % (len(kill), int(spec.want_signal)))
    if spec.want_oom and oom and oom[0]["sev"] != "crit":
        reasons.append("oom_severity=%s want=crit" % oom[0]["sev"])
    if spec.want_signal and kill and kill[0]["sev"] != "warn":
        reasons.append("kill_severity=%s want=warn" % kill[0]["sev"])

    for row in rows:
        if row.get("script_sha256") != target.sha256:
            reasons.append("finding_script_sha_mismatch:%s" % row["id"])
            break

    scopes = {}
    duplicates = []
    for scope in ("user", "system"):
        matches = [m for m in R14.SURFACE_SCOPED_RE.finditer(out)
                   if m.group(1) == scope]
        if len(matches) > 1:
            duplicates.append(scope)
        if matches:
            scopes[scope] = (matches[-1].group(2),
                             dict(R14.TOKEN_RE.findall(matches[-1].group(3))))
    if duplicates:
        reasons.append("duplicate_surface:%s" % ",".join(duplicates))
    for scope in ("user", "system"):
        if scope not in scopes:
            reasons.append("missing_surface:%s" % scope)

    # Named invalid aggregate: only scopes that actually hold a failing
    # record, and only the class the pack names.
    for scope, reason in spec.invalid.items():
        row = scopes.get(scope)
        if row is None:
            continue  # already reported as missing_surface
        expected = "unavailable:" + reason
        actual = row[1].get(spec.invalid_cls)
        if actual != expected:
            reasons.append("%s:%s=%r want=%s"
                           % (scope, spec.invalid_cls, actual, expected))

    if profile == "sut":
        records_by_scope = {"user": tuple(spec.user),
                            "system": tuple(spec.system)}

        def arm_state(scope, token):
            value = spec.positives[scope][token]
            if not isinstance(value, int) or value <= 0:
                return None
            cls = {
                "positive_kernel_oom": "kernel_oom_notice",
                "positive_unit_oom": "unit_failure_record",
                "positive_unit_signal": "unit_failure_record",
                "positive_process_sigkill": "unit_sigkill_record",
            }[token]
            if class_query_available(records_by_scope[scope], cls, spec.mode):
                return "raw"
            return "positive"

        def expected_alarm_basis(tokens):
            states = [s for s in tokens if s is not None]
            if "raw" in states and "positive" in states:
                return "scoped-record-count+validated-positive-records"
            if "raw" in states:
                return "scoped-record-count"
            if "positive" in states:
                return "validated-positive-records"
            return None

        for scope in ("user", "system"):
            row = scopes.get(scope)
            if row is None:
                continue
            for token, expected in spec.positives[scope].items():
                actual = row[1].get(token)
                if isinstance(expected, int):
                    if actual is None or not INT_RE.match(actual) \
                            or int(actual) != expected:
                        reasons.append("%s:%s=%r want=%d"
                                       % (scope, token, actual, expected))
                elif actual != expected:
                    reasons.append("%s:%s=%r want=%s"
                                   % (scope, token, actual, expected))
            if row[1].get("positive_basis") != \
                    "validated-subset-lower-bound":
                reasons.append("%s:positive_basis=%r want="
                               "validated-subset-lower-bound"
                               % (scope, row[1].get("positive_basis")))

        if spec.want_oom and oom:
            tokens = oom[0]["tokens"]
            if "count" in tokens:
                reasons.append("oom_line_carries_summed_count")
            positive_fields = []
            for scope in ("user", "system"):
                row = scopes.get(scope)
                if row is None:
                    continue
                surface = row[1]
                # Raw fields preserve the SURFACE tokens byte-for-byte.
                for field, token in (
                    (scope + "_notice", "kernel_oom_notice"),
                    (scope + "_unit_oom", "unit_oom"),
                    (scope + "_unit_oom_result_unknown",
                     "unit_oom_result_unknown"),
                ):
                    actual = tokens.get(field)
                    want = surface.get(token)
                    if actual is None:
                        reasons.append("oom_field_missing:%s" % field)
                    elif want is None:
                        reasons.append("surface_token_missing:%s" % token)
                    elif actual != want:
                        reasons.append("oom_raw_mismatch:%s" % field)
                # Positive evidence is scope-prefixed and byte-equals the
                # scope's SURFACE positive token.
                for suffix in ("positive_kernel_oom",
                               "positive_unit_oom"):
                    field = "%s_%s" % (scope, suffix)
                    actual = tokens.get(field)
                    want = surface.get(suffix)
                    if actual is None:
                        reasons.append("oom_field_missing:%s" % field)
                        continue
                    positive_fields.append((field, actual))
                    if want is None:
                        reasons.append("surface_token_missing:%s" % suffix)
                    elif actual != want:
                        reasons.append("oom_positive_mismatch:%s" % field)
            names = [field for field, value in positive_fields
                     if POS_INT_RE.match(value or "")]
            if not names:
                reasons.append("oom_positive_evidence_missing")
            expected_basis = expected_alarm_basis([
                arm_state(scope, token)
                for scope in ("user", "system")
                for token in ("positive_kernel_oom", "positive_unit_oom")
            ])
            if tokens.get("alarm_basis") != expected_basis:
                reasons.append("oom_alarm_basis=%r want=%s"
                               % (tokens.get("alarm_basis"), expected_basis))
            if tokens.get("positive_basis") != \
                    "validated-subset-lower-bound":
                reasons.append("oom_positive_basis=%r" %
                               tokens.get("positive_basis"))
            if tokens.get("positive_validation") != \
                    "scalar-id+current-boot":
                reasons.append("oom_positive_validation=%r" %
                               tokens.get("positive_validation"))
            if tokens.get("raw_basis") != "scoped-record-count":
                reasons.append("oom_raw_basis=%r" % tokens.get("raw_basis"))
            path_kernel = (
                any(INT_RE.match(tokens.get(f) or "") and int(tokens[f]) > 0
                    for f in ("user_notice", "system_notice"))
                or any(f in ("user_positive_kernel_oom",
                             "system_positive_kernel_oom")
                       for f in names)
            )
            path_unit = (
                any(INT_RE.match(tokens.get(f) or "") and int(tokens[f]) > 0
                    for f in ("user_unit_oom", "system_unit_oom"))
                or any(f in ("user_positive_unit_oom",
                             "system_positive_unit_oom")
                       for f in names)
            )
            expected_paths = ",".join(
                p for p, on in (("kernel_oom_notice", path_kernel),
                                ("unit_result_oom_kill", path_unit)) if on
            )
            if tokens.get("paths") != expected_paths:
                reasons.append("oom_paths=%r want=%s"
                               % (tokens.get("paths"), expected_paths))

        if spec.want_signal and kill:
            tokens = kill[0]["tokens"]
            row = scopes.get("user")
            surface = row[1] if row is not None else {}
            positive_fields = []
            for field, suffix in (
                ("user_positive_process_sigkill",
                 "positive_process_sigkill"),
                ("user_positive_unit_signal", "positive_unit_signal"),
            ):
                actual = tokens.get(field)
                want = surface.get(suffix)
                if actual is None:
                    reasons.append("kill_field_missing:%s" % field)
                    continue
                positive_fields.append((field, actual))
                if want is None:
                    reasons.append("surface_token_missing:%s" % suffix)
                elif actual != want:
                    reasons.append("kill_positive_mismatch:%s" % field)
            names = [field for field, value in positive_fields
                     if POS_INT_RE.match(value or "")]
            if not names:
                reasons.append("kill_positive_evidence_missing")
            process = tokens.get("process_sigkill")
            count = tokens.get("count")
            if process is None or count is None:
                reasons.append("kill_raw_field_missing")
            elif process != count:
                reasons.append("kill_count_not_process_sigkill")
            for field, token in (
                ("process_sigkill", "unit_sigkill_record"),
                ("user_unit_signal", "unit_signal"),
            ):
                actual = tokens.get(field)
                want = surface.get(token)
                if actual is None:
                    reasons.append("kill_field_missing:%s" % field)
                elif want is None:
                    reasons.append("surface_token_missing:%s" % token)
                elif actual != want:
                    reasons.append("kill_raw_mismatch:%s" % field)
            expected_basis = expected_alarm_basis([
                arm_state("user", "positive_process_sigkill"),
                arm_state("user", "positive_unit_signal"),
            ])
            if tokens.get("alarm_basis") != expected_basis:
                reasons.append("kill_alarm_basis=%r want=%s"
                               % (tokens.get("alarm_basis"), expected_basis))
            if tokens.get("positive_basis") != \
                    "validated-subset-lower-bound":
                reasons.append("kill_positive_basis=%r" %
                               tokens.get("positive_basis"))
            if tokens.get("positive_validation") != \
                    "scalar-id+current-boot+exact-fields":
                reasons.append("kill_positive_validation=%r" %
                               tokens.get("positive_validation"))
            if tokens.get("raw_basis") != "scoped-record-count":
                reasons.append("kill_raw_basis=%r" % tokens.get("raw_basis"))
            path_process = (
                (INT_RE.match(process or "") and int(process) > 0)
                or "user_positive_process_sigkill" in names
            )
            raw_unit = tokens.get("user_unit_signal") or ""
            path_unit_signal = (
                (INT_RE.match(raw_unit) and int(raw_unit) > 0)
                or "user_positive_unit_signal" in names
            )
            expected_paths = ",".join(
                p for p, on in (("process_sigkill", path_process),
                                ("unit_result_signal", path_unit_signal)) if on
            )
            if tokens.get("paths") != expected_paths:
                reasons.append("kill_paths=%r want=%s"
                               % (tokens.get("paths"), expected_paths))

    observed = {
        "rc": rc,
        "verdict": word,
        "drift": counts["drift"],
        "oom_lines": len(oom),
        "kill_lines": len(kill),
        "findings": len(rows),
        "surface_scopes": sorted(scopes),
        "profile": profile,
    }
    return (not reasons), reasons, observed


# ---------------------------------------------------------------------------
# pin mode
# ---------------------------------------------------------------------------


def run_pin(args, gate_sha: str, r14_sha: str) -> int:
    fixtures_dir = Path(args.fixtures).resolve()
    specs, entries = load_packs(fixtures_dir)
    _, frozen_sha, frozen_source = resolve_frozen(args)
    manifest = build_expected(gate_sha, r14_sha, frozen_sha, frozen_source,
                              entries)
    target = Path(args.pin_fixtures).resolve()
    atomic_json(target, manifest)
    print("PINNED %s" % target)
    print("PIN fixtures=%d cases=%d frozen_sha256=%s"
          % (len(entries), len(specs), frozen_sha))
    print("PIN gate_sha256=%s r14_helper_sha256=%s" % (gate_sha, r14_sha))
    red = sum(1 for spec in specs if spec.red_relevant)
    print("PIN red_relevant_cases=%d" % red)
    if red == 0:
        print("PIN WARNING no red-relevant case; a normal run will exit 2 "
              "until a mixed-positive fixture is present")
    return 0


# ---------------------------------------------------------------------------
# main run
# ---------------------------------------------------------------------------


def guard_output(output: Path, fixtures_dir: Path, expected_path: Path,
                 extra_protected=()) -> None:
    raw = Path(output)
    if raw.is_symlink():
        raise SetupError("--output must not be a symlink: %s" % raw)
    out = raw.resolve()
    if out.exists() and not out.is_dir():
        raise SetupError("--output exists and is not a directory: %s" % out)

    def reject_cover(protected: Path, label: str) -> None:
        pp = Path(protected).resolve()
        if out == pp or out.is_relative_to(pp) or pp.is_relative_to(out):
            raise SetupError(
                "--output must not cover, equal or sit under %s (%s); "
                "declared inputs are never output"
                % (label, rel_or_abs(pp))
            )

    reject_cover(fixtures_dir, "the fixture directory")
    reject_cover(DEFAULT_FROZEN, "the frozen census file")
    reject_cover(DEFAULT_FROZEN.parent, "the frozen census directory")
    # The expected file itself is a declared input. Its parent directory may
    # contain a safe evidence subdirectory, so only covering the file is
    # refused here.
    expected = Path(expected_path).resolve()
    if out == expected or expected.is_relative_to(out):
        raise SetupError(
            "--output must not cover or equal the expected table (%s)"
            % rel_or_abs(expected)
        )
    for protected in extra_protected:
        reject_cover(Path(protected), "a declared input")

    if out == REPO or REPO.is_relative_to(out):
        raise SetupError("--output must not equal or contain the repository root")
    for protected in (REPO / "tools", REPO / ".git", REPO / "corpus"):
        if out == protected or out.is_relative_to(protected):
            raise SetupError(
                "--output must not be inside protected tree %s"
                % rel_or_abs(protected)
            )


def guard_output_subpaths(output: Path) -> None:
    for name in ("fixtures", "targets", "runs"):
        path = Path(output) / name
        if path.is_symlink():
            raise SetupError(
                "output subpath must not be a symlink: %s" % path
            )
        if path.exists() and not path.is_dir():
            raise SetupError(
                "output subpath exists and is not a directory: %s" % path
            )


def classify_control(want_oom: bool, want_signal: bool, red_relevant: bool,
                     frozen_ok: bool, reasons, observed: dict,
                     timed_out: bool, error) -> str:
    """Classify one frozen-control run; never confirms an arbitrary failure.

    A red-relevant witness must have completed, carry no integrity failure,
    have internally consistent actual roll/rc/drift for its actual alarm lines,
    never carry an alarm that was not wanted, and specifically miss at least one
    wanted alarm arm. A retained wanted arm is allowed: the entering census may
    still see one source while losing the mixed-stream source. Only a witness
    with at least one specifically missing wanted OOM/WARN is confirmed.
    """
    if not red_relevant:
        return "pass" if frozen_ok else "unexpected_fail"
    if frozen_ok:
        return "unexpected_pass"
    if timed_out or error:
        return "control_inconclusive"
    allowed_prefixes = (
        "rc=", "verdict=", "drift=", "oom_lines=", "kill_lines=",
    )
    if any(not str(reason).startswith(allowed_prefixes)
           for reason in reasons):
        return "control_inconclusive"

    oi = observed.get("oom_lines")
    ki = observed.get("kill_lines")
    if oi not in (0, 1) or ki not in (0, 1):
        return "control_inconclusive"
    if not want_oom and oi != 0:
        return "control_inconclusive"
    if not want_signal and ki != 0:
        return "control_inconclusive"

    actual_alarms = oi + ki
    if observed.get("drift") != actual_alarms:
        return "control_inconclusive"
    rc = observed.get("rc")
    word = observed.get("verdict")
    if actual_alarms == 0:
        if word != "CLEAN" or rc != 0:
            return "control_inconclusive"
    else:
        if word != "DRIFT" or rc != 1:
            return "control_inconclusive"

    missing_oom = bool(
        want_oom and oi == 0
        and any(str(reason).startswith("oom_lines=0") for reason in reasons)
    )
    missing_signal = bool(
        want_signal and ki == 0
        and any(str(reason).startswith("kill_lines=0") for reason in reasons)
    )
    if not (missing_oom or missing_signal):
        return "control_inconclusive"
    return "red_confirmed"


def run_gate(args, r14, gate_sha: str, r14_sha: str) -> int:
    if not args.output:
        raise SetupError("--output DIR is required unless --pin-fixtures/--selftest")
    output_raw = Path(args.output)
    output = output_raw.resolve()
    fixtures_dir = Path(args.fixtures).resolve()
    census_path = Path(args.census).resolve()
    expected_path = Path(args.expected).resolve()
    extra_protected = (Path(args.frozen),) if args.frozen else ()
    guard_output(output_raw, fixtures_dir, expected_path, extra_protected)
    guard_output_subpaths(output)

    gate_path = Path(__file__).resolve()

    if not expected_path.is_file():
        raise SetupError(
            "expected table missing: %s; generate it once with "
            "`python3 tools/mori-round15-regressions.py --pin-fixtures %s`"
            % (expected_path, rel_or_abs(DEFAULT_EXPECTED))
        )
    try:
        expected_raw = expected_path.read_bytes()
        expected = json.loads(expected_raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        raise SetupError("cannot read expected table %s: %s"
                         % (expected_path, exc))

    specs, entries = load_packs(fixtures_dir)
    current = {
        "fixtures": entries,
        "base_commit": PINNED_BASE_COMMIT,
        "pinned_frozen_sha256": PINNED_FROZEN_SHA256,
    }
    frozen_bytes, frozen_sha, frozen_source = resolve_frozen(args)
    compare_expected(expected, current, gate_sha, r14_sha, frozen_sha)

    if not census_path.is_file():
        raise SetupError("census not readable: %s" % census_path)
    census_bytes = census_path.read_bytes()

    if args.case:
        wanted = [part for part in args.case.split(",") if part]
        known = {spec.cid for spec in specs}
        missing = [part for part in wanted if part not in known]
        if missing:
            raise SetupError("unknown --case id(s): %s" % ",".join(missing))
        wanted_set = set(wanted)
        specs = [spec for spec in specs if spec.cid in wanted_set]
    if not specs:
        raise SetupError("no cases selected")

    output.mkdir(parents=True, exist_ok=True)
    for sub in ("targets", "runs", "fixtures"):
        (output / sub).mkdir(parents=True, exist_ok=True)
    atomic_bytes(output / "expected.json", expected_raw)
    target_expected_sha = sha256_bytes(expected_raw)

    sut = materialize_target("sut", rel_or_abs(census_path), census_bytes,
                             output)
    frozen = materialize_target("frozen", frozen_source, frozen_bytes, output)

    revision_start = capture_revision("start", output)
    run_records = []
    case_records = []
    sut_failures = 0
    behavior_failures = 0
    red_required = 0
    red_confirmed = 0
    frozen_unexpected_pass = []
    frozen_unexpected_fail = []
    frozen_inconclusive = []

    for spec in specs:
        root = output / "fixtures" / spec.cid
        build_case_fixture(root, spec, r14)
        env = fixture_env(root, r14)

        reset_probe_logs(root)
        out, err, rc, timed_out, error, run = execute_census(
            sut, root, env, output, "sut.%s" % spec.cid, args.timeout
        )
        argv_rows = r14.read_argv_log(root / "journal" / "argv.log")
        tripwire = (root / "journal" / "tripwire.log").read_text(
            encoding="utf-8", errors="replace")
        run["journal_argv_count"] = len(argv_rows)
        run["journal_argv_sha256"] = sha256_bytes(
            canonical(argv_rows).encode("utf-8")
        )
        sut_ok, sut_reasons, sut_observed = evaluate(
            spec, out, err, rc, timed_out, error, sut, argv_rows, tripwire,
            "sut"
        )
        behavior_ok, behavior_reasons, behavior_observed = evaluate(
            spec, out, err, rc, timed_out, error, sut, argv_rows, tripwire,
            "behavior"
        )
        run["case"] = spec.cid
        run["evaluated"] = "sut"
        run_records.append(run)
        if not sut_ok:
            sut_failures += 1
        if not behavior_ok:
            behavior_failures += 1

        frozen_record = None
        reset_probe_logs(root)
        fout, ferr, frc, ftimed, ferror, frun = execute_census(
            frozen, root, env, output, "frozen.%s" % spec.cid,
            args.timeout
        )
        fargv = r14.read_argv_log(root / "journal" / "argv.log")
        ftrip = (root / "journal" / "tripwire.log").read_text(
            encoding="utf-8", errors="replace")
        frun["journal_argv_count"] = len(fargv)
        frun["journal_argv_sha256"] = sha256_bytes(
            canonical(fargv).encode("utf-8")
        )
        fok, freasons, fobserved = evaluate(
            spec, fout, ferr, frc, ftimed, ferror, frozen, fargv, ftrip,
            "frozen"
        )
        frun["case"] = spec.cid
        frun["evaluated"] = "frozen"
        run_records.append(frun)
        control = classify_control(
            spec.want_oom, spec.want_signal, spec.red_relevant, fok,
            freasons, fobserved, ftimed, ferror
        )
        if spec.red_relevant:
            red_required += 1
            if control == "red_confirmed":
                red_confirmed += 1
            elif control == "unexpected_pass":
                frozen_unexpected_pass.append(spec.cid)
            else:
                frozen_inconclusive.append(spec.cid)
        elif control == "pass":
            pass
        else:
            frozen_unexpected_fail.append(spec.cid)
        frozen_record = {
            "status": "pass" if fok else "fail",
            "control": control,
            "reasons": freasons,
            "observed": fobserved,
            "run": frun["run"],
            "census_sha256": frozen.sha256,
        }

        case_records.append({
            "id": spec.cid,
            "pack": spec.pack,
            "want_oom": spec.want_oom,
            "want_signal": spec.want_signal,
            "invalid_class": spec.invalid_cls,
            "invalid_reasons": spec.invalid,
            "mode": spec.mode,
            "positives": spec.positives,
            "red_relevant": spec.red_relevant,
            "sut": {
                "status": "pass" if sut_ok else "fail",
                "reasons": sut_reasons,
                "observed": sut_observed,
                "run": run["run"],
                "census_sha256": sut.sha256,
            },
            "sut_behavior": {
                "status": "pass" if behavior_ok else "fail",
                "reasons": behavior_reasons,
                "observed": behavior_observed,
            },
            "frozen": frozen_record,
        })
        # Packs, expected values and captures retain the replay authority.
        # Discard the generated per-case sandbox after both targets finish.
        shutil.rmtree(root)

    revision_end = capture_revision("end", output)
    # Moving input: re-hash every verdict-driving input after the run.
    _, after_entries = load_packs(fixtures_dir)
    if canonical(after_entries) != canonical(entries):
        raise SetupError("fixture packs changed while the gate was running")
    end_hashes = {
        "gate_sha256": sha256_file(gate_path),
        "r14_helper_sha256": sha256_file(R14_PATH),
        "expected_sha256": sha256_file(expected_path),
        "census_source_sha256": sha256_file(census_path),
        "census_executed_sha256": sha256_file(sut.executed),
        "frozen_executed_sha256": sha256_file(frozen.executed),
    }
    load_hashes = {
        "gate_sha256": gate_sha,
        "r14_helper_sha256": r14_sha,
        "expected_sha256": target_expected_sha,
        "census_source_sha256": sha256_bytes(census_bytes),
        "census_executed_sha256": sut.sha256,
        "frozen_executed_sha256": frozen.sha256,
    }
    if canonical(end_hashes) != canonical(load_hashes):
        raise SetupError(
            "a verdict-driving input changed while the gate was running "
            "(gate/r14/expected/census/frozen); refusing a mixed-revision verdict"
        )
    revision_stable = (
        canonical(revision_compare_core(revision_start))
        == canonical(revision_compare_core(revision_end))
    )
    summary = {
        "sut_total": len(specs),
        "sut_pass": len(specs) - sut_failures,
        "sut_fail": sut_failures,
        "sut_behavior_fail": behavior_failures,
        "sut_behavior_note": (
            "legacy behavioral assertions only (stable ids/severity/roll/raw "
            "invalid semantics); new-schema positive fields are deliberately "
            "excluded so a red-before run can report behavior separately"
        ),
        "frozen_control": "selected",
        "frozen_red_required": red_required,
        "frozen_red_confirmed": red_confirmed,
        "frozen_unexpected_pass": frozen_unexpected_pass,
        "frozen_unexpected_fail": frozen_unexpected_fail,
        "frozen_inconclusive": frozen_inconclusive,
        "sut_failures_are_not_frozen_failures": True,
    }
    manifest = {
        "schema": SCHEMA,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "gate": {"path": rel_or_abs(gate_path), "sha256": gate_sha},
        "r14_helper": {"path": rel_or_abs(R14_PATH), "sha256": r14_sha},
        "expected": {
            "path": rel_or_abs(expected_path),
            "sha256": target_expected_sha,
            "stored_copy": "expected.json",
        },
        "census": {
            "source": rel_or_abs(census_path),
            "source_sha256": sha256_bytes(census_bytes),
            "executed_copy": rel_or_abs(sut.executed),
            "executed_sha256": sut.sha256,
        },
        "frozen": {
            "source": frozen_source,
            "executed_copy": rel_or_abs(frozen.executed),
            "executed_sha256": frozen.sha256,
            "pinned_sha256": PINNED_FROZEN_SHA256,
            "base_commit": PINNED_BASE_COMMIT,
        },
        "revision": {
            "start": revision_start,
            "end": revision_end,
            "stable": revision_stable,
            "head_changed": revision_start["head"] != revision_end["head"],
            "status_changed": (
                revision_start["dirty_outside_harness_output_paths"]
                != revision_end["dirty_outside_harness_output_paths"]
            ),
            "asserted_revision": PINNED_BASE_COMMIT,
            "asserted_revision_note": (
                "annotation only; comparisons always use real rev-parse HEAD"
            ),
        },
        "inputs": {
            "at_load": load_hashes,
            "at_end": end_hashes,
            "unchanged": canonical(load_hashes) == canonical(end_hashes),
            "fixture_packs": entries,
        },
        "cases": case_records,
        "runs": run_records,
        "summary": summary,
    }
    atomic_json(output / "run-manifest.json", manifest)

    print("GATE %s" % SCHEMA)
    print("EXPECTED %s sha256=%s" % (expected_path, target_expected_sha))
    print("CENSUS %s sha256=%s" % (census_path, sut.sha256))
    print("FROZEN %s sha256=%s pinned=%s"
          % (frozen_source, frozen.sha256, PINNED_FROZEN_SHA256))
    print("REVISION head=%s dirty_paths=%d stable=%s"
          % (revision_end["head"], revision_end["dirty_path_count"],
             manifest["revision"]["stable"]))
    for record in case_records:
        if record["sut"]["status"] == "pass":
            print("CASE %s sut=PASS" % record["id"])
        else:
            print("CASE %s sut=FAIL reasons=%s"
                  % (record["id"], "; ".join(record["sut"]["reasons"])))
        if record["sut_behavior"]["status"] != "pass":
            print("SUT_BEHAVIOR %s status=FAIL reasons=%s"
                  % (record["id"], "; ".join(record["sut_behavior"]["reasons"])))
        if record["frozen"] is not None:
            print("FROZEN %s control=%s actual=%s"
                  % (record["id"], record["frozen"]["control"],
                     record["frozen"]["status"]))
    print("SUMMARY sut_pass=%d sut_fail=%d sut_behavior_fail=%d "
          "frozen_control=%s frozen_red=%d/%d frozen_unexpected_pass=%d "
          "frozen_unexpected_fail=%d frozen_inconclusive=%d"
          % (summary["sut_pass"], summary["sut_fail"],
             summary["sut_behavior_fail"], summary["frozen_control"],
             red_confirmed, red_required, len(frozen_unexpected_pass),
             len(frozen_unexpected_fail), len(frozen_inconclusive)))
    print("MANIFEST %s" % (output / "run-manifest.json"))

    if sut_failures:
        print("GATE FAIL exit=1 (SUT fixture expectation failed)")
        return 1
    if red_required == 0:
        print("GATE ERROR exit=2 (no red-relevant case selected; "
              "the entering control cannot be evaluated)")
        return 2
    if frozen_unexpected_pass or frozen_unexpected_fail or frozen_inconclusive:
        print("GATE ERROR exit=2 (frozen control did not conclusively reproduce "
              "the entering red state; control_inconclusive is a control/"
              "fixture problem, not a SUT bug count)")
        return 2
    print("GATE PASS exit=0")
    return 0


# ---------------------------------------------------------------------------
# selftest (isolated wrappers; never executes the production census)
# ---------------------------------------------------------------------------


_WRAPPER = r'''#!/usr/bin/env python3
import hashlib, os, subprocess, sys

CASE = os.path.basename(os.getcwd())
SHA = hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest()
BEHAVIOR = @BEHAVIOR@
BOOT = "11111111111111111111111111111111"
RC = 0
RAW = ("kernel_oom_notice oomd_notice coredump_notice segfault_signal11 "
       "unit_sigkill_record unit_failure_record unit_oom "
       "unit_oom_result_unknown unit_signal")
POS = ("positive_kernel_oom positive_unit_oom positive_unit_signal "
       "positive_process_sigkill")

def zeros():
    return {k: "0" for k in (RAW + " " + POS).split()}

def surface(scope, state, tokens):
    tokens = dict(tokens)
    tokens.setdefault("positive_basis", "validated-subset-lower-bound")
    tokens.setdefault("positive_validation", "scalar-id+current-boot")
    print("SURFACE journal.%s: %s (%s)" % (
        scope, state, " ".join("%s=%s" % (k, v) for k, v in tokens.items())))

def emit_ok():
    surface("user", "ok", zeros())
    surface("system", "ok", zeros())
    print("MORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=0 surfaces=2)")

def emit_red():
    if CASE == "self_capture_rc":
        t = zeros()
        for k in t:
            t[k] = "unavailable:rc-5"
        surface("user", "unavailable", t)
        surface("system", "ok", zeros())
    elif CASE == "self_capture_stderr":
        t = zeros()
        for k in t:
            t[k] = "unavailable:stderr-nonempty"
        surface("user", "unavailable", t)
        surface("system", "ok", zeros())
    elif CASE == "self_capture_malformed":
        t = zeros()
        for k in t:
            t[k] = "unavailable:malformed-json"
        surface("user", "unavailable", t)
        surface("system", "unavailable", t)
    elif CASE in ("self_mixed_positive", "self_adversarial_nonobject"):
        u = zeros()
        u["kernel_oom_notice"] = "unavailable:record-invalid"
        surface("user", "unavailable", u)
        surface("system", "ok", zeros())
    elif CASE == "self_signal_mixed":
        u = zeros()
        for k in ("unit_failure_record", "unit_sigkill_record", "unit_signal",
                  "unit_oom", "unit_oom_result_unknown", "kernel_oom_notice"):
            u[k] = "unavailable:record-invalid"
        surface("user", "unavailable", u)
        surface("system", "ok", zeros())
    else:
        surface("user", "ok", zeros())
        surface("system", "ok", zeros())
    print("MORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=1 surfaces=2)")

def emit_green():
    global RC
    if CASE in ("self_mixed_positive", "self_adversarial_nonobject"):
        u = zeros()
        u["kernel_oom_notice"] = "unavailable:record-invalid"
        u["positive_kernel_oom"] = "1"
        s = zeros()
        surface("user", "unavailable", u)
        surface("system", "ok", s)
        print("FINDING OOM_KILL_JOURNAL severity=crit obs=class=oom_kill "
              "alarm=1 paths=kernel_oom_notice user_notice=unavailable:"
              "record-invalid system_notice=0 user_unit_oom=0 "
              "system_unit_oom=0 user_unit_oom_result_unknown=0 "
              "system_unit_oom_result_unknown=0 "
              "user_positive_kernel_oom=1 system_positive_kernel_oom=0 "
              "user_positive_unit_oom=0 system_positive_unit_oom=0 "
              "positive_basis=validated-subset-lower-bound "
              "positive_validation=scalar-id+current-boot "
              "alarm_basis=validated-positive-records "
              "raw_basis=scoped-record-count "
              "scope=user,system script_sha256=%s" % SHA)
        print("MORI_CENSUS: DRIFT (findings=1 drift=1 unavailable=1 surfaces=2)")
        RC = 1
        return
    if CASE == "self_signal_mixed":
        u = zeros()
        for k in ("unit_failure_record", "unit_sigkill_record", "unit_signal",
                  "unit_oom", "unit_oom_result_unknown", "kernel_oom_notice"):
            u[k] = "unavailable:record-invalid"
        u["positive_unit_signal"] = "1"
        surface("user", "unavailable", u)
        surface("system", "ok", zeros())
        print("FINDING KILL_SIGNAL_JOURNAL severity=warn obs=class=kill_signal "
              "paths=unit_result_signal count=unavailable:record-invalid "
              "process_sigkill=unavailable:record-invalid "
              "user_unit_signal=unavailable:record-invalid "
              "user_positive_process_sigkill=0 "
              "user_positive_unit_signal=1 "
              "positive_basis=validated-subset-lower-bound "
              "positive_validation=scalar-id+current-boot+exact-fields "
              "alarm_basis=validated-positive-records "
              "raw_basis=scoped-record-count "
              "scope=user script_sha256=%s" % SHA)
        print("MORI_CENSUS: DRIFT (findings=1 drift=1 unavailable=1 surfaces=2)")
        RC = 1
        return
    if CASE == "self_capture_rc":
        t = zeros()
        for k in t:
            t[k] = "unavailable:rc-5"
        surface("user", "unavailable", t)
        surface("system", "ok", zeros())
        print("MORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=1 surfaces=2)")
        return
    if CASE == "self_capture_stderr":
        t = zeros()
        for k in t:
            t[k] = "unavailable:stderr-nonempty"
        surface("user", "unavailable", t)
        surface("system", "ok", zeros())
        print("MORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=1 surfaces=2)")
        return
    if CASE == "self_capture_malformed":
        t = zeros()
        for k in t:
            t[k] = "unavailable:malformed-json"
        surface("user", "unavailable", t)
        surface("system", "unavailable", t)
        print("MORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=2 surfaces=2)")
        return
    emit_ok()

def emit_tampered_id():
    global RC
    if CASE in ("self_mixed_positive", "self_adversarial_nonobject"):
        u = zeros()
        u["kernel_oom_notice"] = "unavailable:record-invalid"
        u["positive_kernel_oom"] = "1"
        surface("user", "unavailable", u)
        surface("system", "ok", zeros())
        print("FINDING OOM_KILL_TYPO severity=crit obs=class=oom_kill "
              "paths=kernel_oom_notice "
              "user_notice=unavailable:record-invalid system_notice=0 "
              "user_unit_oom=0 system_unit_oom=0 "
              "user_unit_oom_result_unknown=0 "
              "system_unit_oom_result_unknown=0 "
              "user_positive_kernel_oom=1 system_positive_kernel_oom=0 "
              "user_positive_unit_oom=0 system_positive_unit_oom=0 "
              "positive_basis=validated-subset-lower-bound "
              "positive_validation=scalar-id+current-boot "
              "alarm_basis=validated-positive-records "
              "raw_basis=scoped-record-count "
              "script_sha256=%s" % SHA)
        print("MORI_CENSUS: DRIFT (findings=1 drift=1 unavailable=1 surfaces=2)")
        RC = 1
        return
    emit_green()

def emit_tampered_rc():
    global RC
    if CASE not in ("self_mixed_positive", "self_adversarial_nonobject",
                    "self_signal_mixed"):
        emit_green()
        return
    import contextlib, io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        emit_green()
    body = [line for line in buf.getvalue().splitlines()
            if not line.startswith("MORI_CENSUS:")]
    print("\n".join(body))
    # One finding remains, but the verdict and rc claim a clean run.
    RC = 0
    print("MORI_CENSUS: CLEAN (findings=1 drift=0 unavailable=1 surfaces=2)")

if BEHAVIOR == "green":
    emit_green()
elif BEHAVIOR == "red":
    emit_red()
elif BEHAVIOR == "tampered_id":
    emit_tampered_id()
elif BEHAVIOR == "tampered_rc":
    emit_tampered_rc()
else:
    sys.exit(97)
sys.exit(RC)
'''


def _selftest_pack() -> list:
    return [
        {
            "id": "self_mixed_positive",
            "user": [
                {"_BOOT_ID": BOOT, "MESSAGE_ID": KERNEL_ID},
                {"_BOOT_ID": BOOT, "MESSAGE_ID": OOMD_ID},
            ],
            "system": [],
            "want_oom": True,
            "want_signal": False,
            "invalid_class": "kernel_oom_notice",
        },
        {
            "id": "self_adversarial_nonobject",
            "user": [
                {"_BOOT_ID": BOOT, "MESSAGE_ID": KERNEL_ID},
                "x",
            ],
            "system": [],
            "want_oom": True,
            "want_signal": False,
            "invalid_class": "kernel_oom_notice",
        },
        {
            "id": "self_signal_mixed",
            "user": [
                {"_BOOT_ID": BOOT, "MESSAGE_ID": FAILURE_ID,
                 "USER_UNIT": "kagi-shokunin.service",
                 "UNIT_RESULT": "signal"},
                {"_BOOT_ID": BOOT, "MESSAGE_ID": [FAILURE_ID, FAILURE_ID]},
            ],
            "system": [],
            "want_oom": False,
            "want_signal": True,
            "invalid_class": "unit_failure_record",
        },
        {
            "id": "self_negative",
            "user": [],
            "system": [],
            "want_oom": False,
            "want_signal": False,
            "invalid_class": None,
        },
        {
            "id": "self_capture_rc",
            "user": [],
            "system": [],
            "want_oom": False,
            "want_signal": False,
            "invalid_class": None,
            "capture": {"kind": "rc", "scope": "user", "rc": 5},
        },
        {
            "id": "self_capture_stderr",
            "user": [],
            "system": [],
            "want_oom": False,
            "want_signal": False,
            "invalid_class": None,
            "capture": {"kind": "stderr", "scope": "user"},
        },
        {
            "id": "self_capture_malformed",
            "user": [],
            "system": [],
            "want_oom": False,
            "want_signal": False,
            "invalid_class": None,
            "capture": {"kind": "malformed"},
        },
    ]


def _selftest_control_classifier() -> None:
    """Pure helper-level checks for F1; executes no census subprocess."""
    observed_clean = {
        "rc": 0, "verdict": "CLEAN", "drift": 0,
        "oom_lines": 0, "kill_lines": 0,
    }
    red_reasons = [
        "rc=0 want=1",
        "verdict=CLEAN/ok want=DRIFT",
        "drift=0 want=1",
        "oom_lines=0 want=1",
    ]
    retained_oom_missed_signal = {
        "rc": 1, "verdict": "DRIFT", "drift": 1,
        "oom_lines": 1, "kill_lines": 0,
    }
    retained_kill_missed_oom = {
        "rc": 1, "verdict": "DRIFT", "drift": 1,
        "oom_lines": 0, "kill_lines": 1,
    }
    checks = [
        ("red_completed",
         classify_control(True, False, True, False, red_reasons,
                          observed_clean, False, None), "red_confirmed"),
        ("red_partial_retained_oom",
         classify_control(True, True, True, False,
                          ["drift=1 want=2", "kill_lines=0 want=1"],
                          retained_oom_missed_signal, False, None),
         "red_confirmed"),
        ("red_partial_retained_kill",
         classify_control(True, True, True, False,
                          ["drift=1 want=2", "oom_lines=0 want=1"],
                          retained_kill_missed_oom, False, None),
         "red_confirmed"),
        ("red_no_wanted_arm_missing",
         classify_control(True, False, True, False, [],
                          retained_oom_missed_signal, False, None),
         "control_inconclusive"),
        ("red_unwanted_warn",
         classify_control(True, False, True, False, ["kill_lines=1 want=0"],
                          dict(retained_oom_missed_signal, kill_lines=1,
                               drift=2), False, None), "control_inconclusive"),
        ("red_timeout",
         classify_control(True, False, True, False, red_reasons,
                          observed_clean, True, None), "control_inconclusive"),
        ("red_exec_error",
         classify_control(True, False, True, False, red_reasons,
                          observed_clean, False, "OSError"), "control_inconclusive"),
        ("red_integrity_failure",
         classify_control(True, False, True, False,
                          red_reasons + ["finding_script_sha_mismatch:X"],
                          observed_clean, False, None), "control_inconclusive"),
        ("red_alarm_not_missing",
         classify_control(True, False, True, False, red_reasons,
                          dict(observed_clean, oom_lines=1), False, None),
         "control_inconclusive"),
        ("red_unexpected_pass",
         classify_control(True, False, True, True, [], observed_clean,
                          False, None), "unexpected_pass"),
        ("nonred_pass",
         classify_control(False, False, False, True, [], observed_clean,
                          False, None), "pass"),
        ("nonred_fail",
         classify_control(False, False, False, False, ["rc=1 want=0"],
                          observed_clean, False, None), "unexpected_fail"),
    ]
    for name, got, want in checks:
        if got != want:
            raise SetupError(
                "selftest control classifier %s: got=%s want=%s"
                % (name, got, want)
            )


def _selftest_run(gate: Path, args, root: Path, expect_rc: int,
                  marker: str | None):
    argv = [sys.executable, str(gate)] + [str(a) for a in args]
    env = {k: v for k, v in os.environ.items() if not k.startswith("MORI_")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        argv,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        timeout=300,
    )
    transcript = root / ("selftest-%d.log" % int(time.time() * 1000))
    transcript.write_text(
        "argv=%r\nrc=%d\n--- stdout ---\n%s\n--- stderr ---\n%s\n"
        % (argv, proc.returncode, proc.stdout, proc.stderr),
        encoding="utf-8",
    )
    problems = []
    if proc.returncode != expect_rc:
        problems.append("rc=%d want=%d" % (proc.returncode, expect_rc))
    if marker and marker not in (proc.stdout + proc.stderr):
        problems.append("missing marker %r" % marker)
    if problems:
        raise SetupError(
            "selftest invocation failed: %s; transcript=%s"
            % ("; ".join(problems), transcript)
        )
    return proc


def selftest() -> int:
    gate = Path(__file__).resolve()
    root = Path(tempfile.mkdtemp(prefix="mori-r15-selftest-"))
    fixtures = root / "fixtures"
    fixtures.mkdir(parents=True)
    pack = fixtures / "Selftest.json"
    pack.write_text(json.dumps(_selftest_pack(), indent=2) + "\n",
                    encoding="utf-8")
    expected = root / "expected.json"
    wrappers = root / "wrappers"
    wrappers.mkdir()

    def write_wrapper(name: str, behavior: str) -> Path:
        impl = wrappers / (name + "_impl.py")
        impl.write_text(_WRAPPER.replace("@BEHAVIOR@", repr(behavior)),
                        encoding="utf-8")
        stub = wrappers / (name + ".sh")
        stub.write_text(
            '#!/usr/bin/env bash\nexec python3 "$IMPL" "$0"\n'
            .replace("$IMPL", str(impl)),
            encoding="utf-8",
        )
        stub.chmod(0o755)
        return stub

    green = write_wrapper("green", "green")
    red = write_wrapper("red", "red")
    tampered_id = write_wrapper("tampered_id", "tampered_id")
    tampered_rc = write_wrapper("tampered_rc", "tampered_rc")
    base = ["--fixtures", fixtures, "--expected", expected]

    _selftest_control_classifier()
    print("SELFTEST control classifier checks: PASS")
    _selftest_run(gate, base + ["--pin-fixtures", expected],
                  root, 0, "PINNED")
    for name, wrapper in (("green", green), ("red", red),
                          ("tampered_id", tampered_id),
                          ("tampered_rc", tampered_rc)):
        _selftest_run(
            gate,
            base + ["--census", wrapper,
                     "--output", root / ("out-" + name)],
            root,
            0 if name == "green" else 1,
            "GATE PASS" if name == "green" else "GATE FAIL",
        )
    # A frozen path whose bytes are not the pinned entering census is a pin
    # error before any execution: exit 2.
    _selftest_run(
        gate,
        base + ["--census", green, "--output", root / "out-pin-tamper",
                 "--frozen", red],
        root,
        2,
        "GATE ERROR",
    )
    # A pinned fixture digest change must be refused, even with a green SUT.
    exp = json.loads(expected.read_text(encoding="utf-8"))
    exp["fixtures"][0]["sha256"] = "0" * 64
    tampered_expected = root / "expected-tampered.json"
    tampered_expected.write_text(json.dumps(exp, indent=2) + "\n",
                                 encoding="utf-8")
    _selftest_run(
        gate,
        ["--fixtures", fixtures, "--expected", tampered_expected,
         "--census", green, "--output", root / "out-expected-tamper"],
        root,
        2,
        "GATE ERROR",
    )
    # The green transcript must retain argv/rc/stdout/stderr evidence and
    # per-case positive/invalid assertions.
    manifest_path = root / "out-green" / "run-manifest.json"
    if not manifest_path.is_file():
        raise SetupError("selftest green run left no run-manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if len(manifest.get("runs", [])) != 2 * len(_selftest_pack()):
        raise SetupError("selftest green manifest lost SUT or frozen run records")
    controls = {case["id"]: case.get("frozen", {}).get("control")
                for case in manifest.get("cases", [])}
    red_ids = {
        "self_mixed_positive",
        "self_adversarial_nonobject",
        "self_signal_mixed",
    }
    for cid, control in controls.items():
        want = "red_confirmed" if cid in red_ids else "pass"
        if control != want:
            raise SetupError(
                "selftest full frozen control %s: got=%r want=%r"
                % (cid, control, want)
            )
    for run in manifest["runs"]:
        for key in ("argv", "rc", "stdout_path", "stderr_path",
                    "stdout_sha256", "stderr_sha256"):
            if key not in run:
                raise SetupError("selftest run record lacks %s" % key)
    print("SELFTEST PASS selftest_root=%s" % root)
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="mori round-15 fixture-pack regression gate"
    )
    parser.add_argument("--census", default=str(DEFAULT_CENSUS))
    parser.add_argument("--fixtures", default=str(DEFAULT_FIXTURES))
    parser.add_argument("--output")
    parser.add_argument("--frozen", default=None)
    parser.add_argument("--expected", default=str(DEFAULT_EXPECTED))
    parser.add_argument("--pin-fixtures", default=None, metavar="PATH")
    parser.add_argument("--case", default=None,
                        help="comma-separated case-id subset (diagnostics)")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--selftest", action="store_true")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    if args.selftest:
        if args.output or args.pin_fixtures:
            print("GATE ERROR exit=2 (--selftest takes no run/pin flags)")
            return 2
        try:
            return selftest()
        except SetupError as exc:
            print("SELFTEST ERROR: %s" % one_line(exc))
            print("GATE ERROR exit=2")
            return 2
    try:
        if args.timeout < 1 or args.timeout > 3600:
            raise SetupError("--timeout must be 1..3600")
        gate_sha = sha256_bytes(Path(__file__).resolve().read_bytes())
        # Read/hash/execute the helper bytes once; a broken helper is a clean
        # exit 2 even in pin mode.
        r14, r14_sha = load_r14()
        if args.pin_fixtures:
            return run_pin(args, gate_sha, r14_sha)
        return run_gate(args, r14, gate_sha, r14_sha)
    except SetupError as exc:
        label = "PIN ERROR" if isinstance(exc, SnapshotTampered) else "GATE ERROR"
        print("%s: %s" % (label, one_line(exc)))
        print("GATE ERROR exit=2")
        return 2


if __name__ == "__main__":
    sys.exit(main())
