#!/usr/bin/env python3
"""mori-round16-regressions.py — isolated fixture-pack gate for the r16
journal-window capability.

This harness measures `tools/mori-journal-window.py` against shared fixture
packs.  It never reads the live journal: every run injects a per-case
executable journalctl wrapper whose entire environment is controlled by the
harness (PATH contains only a tripwire `journalctl` canary, so a tool that
ignores --journalctl cannot reach a real producer and is caught).

Fixture pack schema (one JSON object per file under --fixtures DIR):

    {"cases": [{
        "id": "unique-case-id",
        "scope": "user" | "system",
        "anchor": {"schema": "mori-journal-anchor-v1",
                   "scope": "user", "boot_id": "<32 lowercase hex>",
                   "cursor": "<opaque printable scalar>"} | null,
        "anchor_raw": "<verbatim anchor file bytes>"   # optional, implies SETUP
        "stdout": "<JSONL journalctl stdout string>",
        "stderr": "<journalctl stderr string>",
        "returncode": <int 0-255>,
        "timeout": true,                              # optional
        "overflow": true,                             # optional
        "max_bytes": <int>,                           # optional
        "want_rc": 0 | 2,
        "want_id": "MORI_JOURNAL_WINDOW_OK" |
                   "MORI_JOURNAL_WINDOW_UNAVAILABLE" |
                   "MORI_JOURNAL_WINDOW_SETUP",
        "want": {"<output key>": <scalar>, ...}       # optional on rc2
    }]}

`want` is a strict subset match against the tool's single stdout JSON object:
every `want` key must equal the same-typed value in the output.  On want_rc=0
cases `want` must carry records_after_anchor plus all four positive_* counts,
and the harness independently re-derives every expectation from the shared
contract before any tool runs — a pack whose wants disagree with its own
capture is a setup error (rc2), never a tool failure.  On want_rc=2 cases no
count/evidence key may appear in `want`.

The wrapper contract: stdout/stderr payload bytes are emitted byte-exact (no
added newline); `timeout` cases emit via a short-lived grandchild so a tool
that only waits on EOF still hits its own --timeout bound; `overflow` cases
append a finite pad sized so total bytes = effective max_bytes + 1.

Gate return codes:

    0  every case matched its declared expectation
    1  at least one case mismatched, or every case recorded capability_absent
       because --tool does not exist (entering "before" measurement; never
       green, never a production bug claim)
    2  setup/tamper: bad args, unreadable or unpinned inputs, fixture or tool
       digest mismatch, inputs moved during the run, unsafe --output

Pin the input digests once with `--pin-fixtures PATH`, then run with
`--expected PATH`.  The pin manifest records every pack digest, this gate's
digest, and the tool digest at pin time (null when the tool did not exist yet:
digest validation is skipped with a manifest note, the capability_absent path
is unchanged).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import selectors
import stat
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

SCHEMA = "mori-round16-regressions-v1"
EXPECTED_SCHEMA = "mori-round16-regressions-expected-v1"
MANIFEST_SCHEMA = "mori-round16-regressions-manifest-v1"
PACK_SCHEMA = "mori-journal-window-pack-v1"
ANCHOR_SCHEMA = "mori-journal-anchor-v1"

REPO = Path(__file__).resolve().parent.parent
DEFAULT_TOOL = REPO / "tools/mori-journal-window.py"
DEFAULT_FIXTURES = REPO / ".ufo/waves/round-16/fixtures"
DEFAULT_EXPECTED = REPO / ".ufo/waves/round-16/expected.json"

FINDING_OK = "MORI_JOURNAL_WINDOW_OK"
FINDING_UNAVAILABLE = "MORI_JOURNAL_WINDOW_UNAVAILABLE"
FINDING_SETUP = "MORI_JOURNAL_WINDOW_SETUP"
FINDING_IDS = (FINDING_OK, FINDING_UNAVAILABLE, FINDING_SETUP)

# Canonical round-16 pack set; enforced only when --fixtures resolves to the
# committed round-16 fixture directory (the shared gate).  Other directories
# (selftest, experiments) need >=1 pack meeting the schema rules.
CANONICAL_PACKS = (
    "AnchorValidation.json", "BootBoundary.json", "Bounds.json",
    "CursorShape.json", "ExactAnchor.json", "KernelSystem.json",
    "KernelUser.json", "MalformedCapture.json", "MissingAnchor.json",
    "ProcessSignal.json", "ProducerFailure.json", "RecordShape.json",
    "Stderr.json", "TypedFields.json", "UnitOom.json", "UnitSignal.json",
)

# r15 catalog ids (verbatim from tools/mori-census.sh); the oracle uses them
# only to cross-check pack wants, never to grade the tool.
KERNEL_OOM_ID = "fe6faa94e7774663a0da52717891d8ef"
UNIT_FAILURE_ID = "d9b373ed55a64feb8242e02dbe79a49c"
PROCESS_EXIT_ID = "98e322203f7a4ed290d09fe03c09fe15"

COUNT_KEYS = (
    "records_after_anchor",
    "positive_kernel_oom",
    "positive_unit_oom",
    "positive_unit_signal",
    "positive_process_sigkill",
)
# Keys a successful window must carry; keys never allowed in any tool output;
# keys forbidden on refusal output (no fabricated totals on unavailable).
OK_REQUIRED = {
    "finding_id", "scope", "evidence_basis",
} | set(COUNT_KEYS)
FORBIDDEN_KEYS = {
    "MESSAGE", "alarm", "severity", "victims", "victim_count",
}
RC2_FORBIDDEN_KEYS = set(COUNT_KEYS) | {"evidence_basis", "end_cursor"}

OUTPUT_FIELDS = "__CURSOR,_BOOT_ID,MESSAGE_ID,UNIT_RESULT,EXIT_CODE,EXIT_STATUS"
BOOT_ID_RE = re.compile(r"^[0-9a-f]{32}$")
CASE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,80}$")
CANARY_TOKEN_RE = re.compile(r"[A-Z][A-Z0-9_]{10,}")

CASE_REQUIRED_KEYS = {
    "id", "scope", "anchor", "stdout", "stderr", "returncode",
    "want_rc", "want_id",
}
CASE_ALLOWED_KEYS = CASE_REQUIRED_KEYS | {
    "want", "anchor_raw", "timeout", "overflow", "max_bytes",
}
PACK_ALLOWED_KEYS = {"cases", "note"}

TOOL_TIMEOUT_NORMAL = 10          # --timeout passed for ordinary cases
TOOL_TIMEOUT_CASE = 2             # --timeout passed for timeout:true cases
WRAPPER_SLEEP_S = 5               # finite grandchild sleep (kill-bounded)
MAX_BYTES_SLACK = 4096            # headroom added for ordinary cases
CAPTURE_CAP = 4 * 1024 * 1024     # per-stream harness cap on tool output
RUN_TIMEOUT_S = 30                # harness per-run deadline


class SetupError(Exception):
    """Usage, fixture, expected-table or pin failure: exit 2."""


# ---------------------------------------------------------------------------
# small utilities
# ---------------------------------------------------------------------------


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
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
    tmp = path.parent / (".%s.tmp" % path.name)
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    os.replace(tmp, path)


def atomic_bytes(path: Path, data: bytes, mode: int | None = None) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.parent / (".%s.tmp" % path.name)
    tmp.write_bytes(data)
    if mode is not None:
        os.chmod(tmp, mode)
    os.replace(tmp, path)


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def one_line(text, limit=520) -> str:
    cleaned = " ".join(str(text).split())
    return cleaned if len(cleaned) <= limit else cleaned[: limit - 3] + "..."


def _reject_constant(token):
    raise ValueError("non-JSON constant %r" % token)


def _unique_pairs(pairs):
    seen = set()
    out = {}
    for key, value in pairs:
        if not isinstance(key, str):
            raise ValueError("non-string object key")
        if key in seen:
            raise ValueError("duplicate key %r" % key)
        seen.add(key)
        out[key] = value
    return out


def strict_json(text):
    """Parse text; reject duplicate keys and NaN/Infinity constants."""
    return json.loads(text, object_pairs_hook=_unique_pairs,
                      parse_constant=_reject_constant)


def strict_eq(actual, want) -> bool:
    """Type-strict equality: True != 1, "1" != 1."""
    return type(actual) is type(want) and actual == want


def cursor_ok(value, require_str=True) -> bool:
    """Shared anchor/record cursor shape: opaque printable scalar <=4096."""
    if require_str and not isinstance(value, str):
        return False
    if isinstance(value, str):
        if len(value) == 0 or len(value) > 4096:
            return False
        return all(32 <= ord(ch) <= 126 for ch in value)
    return False


def status_is_9(value) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return value == 9
    if isinstance(value, str):
        return value == "9"
    return False


# ---------------------------------------------------------------------------
# shared-contract oracle: re-derive every expectation from the capture itself
# ---------------------------------------------------------------------------


def _parse_jsonl(stdout: str):
    """Return (records, error).  Mirrors the contract's line-JSON parse."""
    lines = stdout.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]          # one terminal newline, byte-exact
    if not lines:
        return None, "empty-capture"
    records = []
    for line in lines:
        if line == "":
            return None, "malformed-json"
        try:
            records.append(strict_json(line))
        except ValueError:
            return None, "malformed-json"
    return records, None


def _positive_counts(records, boot: str) -> dict:
    counts = {key: 0 for key in COUNT_KEYS}
    counts["records_after_anchor"] = len(records)
    for rec in records:
        msgid = rec.get("MESSAGE_ID")
        if not isinstance(msgid, str):
            continue
        if msgid == KERNEL_OOM_ID:
            counts["positive_kernel_oom"] += 1
        elif msgid == UNIT_FAILURE_ID:
            if rec.get("UNIT_RESULT") == "oom-kill":
                counts["positive_unit_oom"] += 1
            elif rec.get("UNIT_RESULT") == "signal":
                counts["positive_unit_signal"] += 1
        elif msgid == PROCESS_EXIT_ID:
            if rec.get("EXIT_CODE") == "killed" \
                    and status_is_9(rec.get("EXIT_STATUS")):
                counts["positive_process_sigkill"] += 1
    return counts


def validate_anchor_shape(anchor) -> str | None:
    """Return a stable defect slug or None when the anchor is schema-exact."""
    if not isinstance(anchor, dict):
        return "anchor-not-object"
    if anchor.get("schema") != ANCHOR_SCHEMA:
        return "anchor-schema"
    if anchor.get("scope") not in ("user", "system"):
        return "anchor-scope-value"
    boot = anchor.get("boot_id")
    if not isinstance(boot, str) or not BOOT_ID_RE.match(boot):
        return "anchor-boot-id"
    if not cursor_ok(anchor.get("cursor")):
        return "anchor-cursor"
    if set(anchor) - {"schema", "scope", "boot_id", "cursor"}:
        return "anchor-extra-keys"
    return None


def derive_expectation(case: dict) -> dict:
    """The shared contract applied to one case's declared inputs.

    Returns {"rc": int, "id": finding-id, "counts": {...} | None}.
    This is the oracle packs are checked against; the tool is graded only
    against the case's declared wants afterwards.
    """
    anchor = case.get("anchor")
    if "anchor_raw" in case or anchor is None:
        return {"rc": 2, "id": FINDING_SETUP, "counts": None,
                "why": "anchor-file"}
    defect = validate_anchor_shape(anchor)
    if defect is not None:
        return {"rc": 2, "id": FINDING_SETUP, "counts": None, "why": defect}
    if anchor["scope"] != case["scope"]:
        return {"rc": 2, "id": FINDING_SETUP, "counts": None,
                "why": "anchor-scope-mismatch"}

    out_bytes = case["stdout"].encode("utf-8")
    if case.get("timeout"):
        return {"rc": 2, "id": FINDING_UNAVAILABLE, "counts": None,
                "why": "timeout"}
    effective_max = case.get("max_bytes")
    if effective_max is None:
        effective_max = len(out_bytes) + MAX_BYTES_SLACK
    if case.get("overflow") or len(out_bytes) > effective_max:
        return {"rc": 2, "id": FINDING_UNAVAILABLE, "counts": None,
                "why": "overflow"}
    if case["returncode"] != 0:
        return {"rc": 2, "id": FINDING_UNAVAILABLE, "counts": None,
                "why": "rc-nonzero"}
    if case["stderr"] != "":
        return {"rc": 2, "id": FINDING_UNAVAILABLE, "counts": None,
                "why": "stderr"}

    records, error = _parse_jsonl(case["stdout"])
    if error is not None:
        return {"rc": 2, "id": FINDING_UNAVAILABLE, "counts": None,
                "why": error}
    first = records[0]
    if not isinstance(first, dict):
        return {"rc": 2, "id": FINDING_UNAVAILABLE, "counts": None,
                "why": "anchor-record-not-object"}
    if first.get("__CURSOR") != anchor["cursor"] \
            or first.get("_BOOT_ID") != anchor["boot_id"]:
        return {"rc": 2, "id": FINDING_UNAVAILABLE, "counts": None,
                "why": "anchor-missing"}

    rest = records[1:]
    seen_cursors = {anchor["cursor"]}
    for rec in rest:
        if not isinstance(rec, dict):
            return {"rc": 2, "id": FINDING_UNAVAILABLE, "counts": None,
                    "why": "record-not-object"}
        if rec.get("_BOOT_ID") != anchor["boot_id"]:
            return {"rc": 2, "id": FINDING_UNAVAILABLE, "counts": None,
                    "why": "foreign-boot"}
        cur = rec.get("__CURSOR")
        if not cursor_ok(cur):
            return {"rc": 2, "id": FINDING_UNAVAILABLE, "counts": None,
                    "why": "cursor-shape"}
        if cur in seen_cursors:
            return {"rc": 2, "id": FINDING_UNAVAILABLE, "counts": None,
                    "why": "cursor-duplicate"}
        seen_cursors.add(cur)

    return {"rc": 0, "id": FINDING_OK,
            "counts": _positive_counts(rest, anchor["boot_id"]),
            "why": "ok"}


# ---------------------------------------------------------------------------
# fixture loading
# ---------------------------------------------------------------------------


@dataclass
class CaseSpec:
    cid: str
    pack: str
    scope: str
    anchor: dict | None
    anchor_raw: str | None
    stdout: str
    stderr: str
    returncode: int
    timeout: bool
    overflow: bool
    max_bytes: int | None
    want_rc: int
    want_id: str
    want: dict
    oracle: dict

    def expected_journalctl_calls(self) -> int:
        return 0 if self.want_id == FINDING_SETUP else 1


def analyze_case(pack_name: str, obj) -> CaseSpec:
    if not isinstance(obj, dict):
        raise SetupError("%s: case is not an object" % pack_name)
    unknown = set(obj) - CASE_ALLOWED_KEYS
    if unknown:
        raise SetupError("%s: case has unknown key(s): %s"
                         % (pack_name, ",".join(sorted(unknown))))
    missing = CASE_REQUIRED_KEYS - set(obj)
    if missing:
        raise SetupError("%s: case lacks key(s): %s"
                         % (pack_name, ",".join(sorted(missing))))

    cid = obj["id"]
    if not isinstance(cid, str) or not CASE_ID_RE.match(cid):
        raise SetupError("%s: unsafe or missing case id: %r" % (pack_name, cid))
    scope = obj["scope"]
    if scope not in ("user", "system"):
        raise SetupError("%s/%s: scope must be user|system" % (pack_name, cid))
    anchor = obj["anchor"]
    anchor_raw = obj.get("anchor_raw")
    if anchor is not None and not isinstance(anchor, dict):
        raise SetupError("%s/%s: anchor must be an object or null"
                         % (pack_name, cid))
    if anchor_raw is not None and not isinstance(anchor_raw, str):
        raise SetupError("%s/%s: anchor_raw must be a string"
                         % (pack_name, cid))
    for field in ("stdout", "stderr"):
        if not isinstance(obj[field], str):
            raise SetupError("%s/%s: %s must be a JSONL string"
                             % (pack_name, cid, field))
    rc = obj["returncode"]
    if isinstance(rc, bool) or not isinstance(rc, int) or not 0 <= rc <= 255:
        raise SetupError("%s/%s: returncode must be int 0..255"
                         % (pack_name, cid))
    timeout = obj.get("timeout", False)
    overflow = obj.get("overflow", False)
    if not isinstance(timeout, bool) or not isinstance(overflow, bool):
        raise SetupError("%s/%s: timeout/overflow must be booleans"
                         % (pack_name, cid))
    if timeout and overflow:
        raise SetupError("%s/%s: timeout and overflow are exclusive"
                         % (pack_name, cid))
    max_bytes = obj.get("max_bytes")
    if max_bytes is not None and (isinstance(max_bytes, bool)
                                or not isinstance(max_bytes, int)
                                or max_bytes < 1):
        raise SetupError("%s/%s: max_bytes must be an int >= 1"
                         % (pack_name, cid))

    want_rc = obj["want_rc"]
    want_id = obj["want_id"]
    want = obj.get("want", {})
    if isinstance(want_rc, bool) or want_rc not in (0, 2):
        raise SetupError("%s/%s: want_rc must be 0 or 2" % (pack_name, cid))
    if want_id not in FINDING_IDS:
        raise SetupError("%s/%s: want_id must be one of %s"
                         % (pack_name, cid, "/".join(FINDING_IDS)))
    if (want_rc == 0) != (want_id == FINDING_OK):
        raise SetupError("%s/%s: want_rc=%s contradicts want_id=%s"
                         % (pack_name, cid, want_rc, want_id))
    if not isinstance(want, dict):
        raise SetupError("%s/%s: want must be an object (use {} to assert "
                         "rc+finding_id only)" % (pack_name, cid))
    for key, value in want.items():
        if not isinstance(key, str):
            raise SetupError("%s/%s: want keys must be strings"
                             % (pack_name, cid))
        if isinstance(value, float) or isinstance(value, (list, dict)):
            raise SetupError("%s/%s: want.%s must be a scalar"
                             % (pack_name, cid, key))
    if want_rc == 0:
        missing_wants = [k for k in COUNT_KEYS if k not in want]
        if missing_wants:
            raise SetupError("%s/%s: rc0 cases must pin want keys: %s"
                             % (pack_name, cid, ",".join(missing_wants)))
    else:
        banned = [k for k in want if k in RC2_FORBIDDEN_KEYS
                  or k in FORBIDDEN_KEYS or k.startswith("positive_")]
        if banned:
            raise SetupError("%s/%s: rc2 want must not pin count/evidence "
                             "keys: %s" % (pack_name, cid, ",".join(banned)))

    # Structural coherence: anchor provenance must agree with the finding id.
    oracle = derive_expectation(obj)
    if oracle["rc"] != want_rc or oracle["id"] != want_id:
        raise SetupError(
            "%s/%s: declared wants rc=%s id=%s contradict the shared "
            "contract reading of this capture (rc=%s id=%s via %s)"
            % (pack_name, cid, want_rc, want_id,
               oracle["rc"], oracle["id"], oracle["why"]))
    if want_rc == 0:
        for key in COUNT_KEYS:
            if not strict_eq(want[key], oracle["counts"][key]):
                raise SetupError(
                    "%s/%s: want.%s=%r contradicts capture-derived %r"
                    % (pack_name, cid, key, want[key],
                       oracle["counts"][key]))
    if want_id != FINDING_SETUP:
        # A query-bearing expectation needs a schema-exact anchor whose scope
        # matches the case scope; anything else is setup-level by contract.
        if validate_anchor_shape(anchor) is not None \
                or anchor["scope"] != scope:
            raise SetupError(
                "%s/%s: non-SETUP expectation requires a schema-exact "
                "anchor with scope == case scope" % (pack_name, cid))

    # MESSAGE-free observation: fixture records never carry display text.
    if oracle["rc"] == 0 or oracle["why"] not in ("malformed-json",
                                                "empty-capture"):
        parsed, _ = _parse_jsonl(obj["stdout"])
        if parsed:
            for rec in parsed:
                if isinstance(rec, dict) and "MESSAGE" in rec:
                    raise SetupError(
                        "%s/%s: fixture records may not carry a MESSAGE key"
                        % (pack_name, cid))

    return CaseSpec(
        cid=cid, pack=pack_name, scope=scope, anchor=anchor,
        anchor_raw=anchor_raw, stdout=obj["stdout"], stderr=obj["stderr"],
        returncode=rc, timeout=timeout, overflow=overflow,
        max_bytes=max_bytes, want_rc=want_rc, want_id=want_id,
        want=dict(want), oracle=oracle,
    )


def load_packs(fixtures_dir: Path):
    fixtures_dir = Path(fixtures_dir).resolve()
    if fixtures_dir.is_symlink() or not fixtures_dir.is_dir():
        raise SetupError("fixtures directory not readable: %s" % fixtures_dir)
    paths = sorted(fixtures_dir.glob("*.json"))
    if not paths:
        raise SetupError("no fixture packs under %s" % fixtures_dir)
    if fixtures_dir == DEFAULT_FIXTURES:
        names = {p.name for p in paths}
        missing = [n for n in CANONICAL_PACKS if n not in names]
        extra = sorted(names - set(CANONICAL_PACKS))
        if missing or extra:
            raise SetupError(
                "canonical fixture dir must hold exactly the %d shared "
                "packs; missing=%s extra=%s"
                % (len(CANONICAL_PACKS), ",".join(missing) or "-",
                   ",".join(extra) or "-"))

    specs = []
    entries = []
    seen = {}
    for path in paths:
        try:
            raw = path.read_bytes()
        except OSError as exc:
            raise SetupError("cannot read fixture pack %s: %s" % (path, exc))
        try:
            data = strict_json(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise SetupError("fixture pack %s is not valid UTF-8 JSON: %s"
                             % (path, exc))
        if not isinstance(data, dict):
            raise SetupError("fixture pack %s must be a JSON object"
                             % path.name)
        unknown = set(data) - PACK_ALLOWED_KEYS
        if unknown:
            raise SetupError("%s: unknown pack key(s): %s"
                             % (path.name, ",".join(sorted(unknown))))
        cases = data.get("cases")
        if not isinstance(cases, list) or len(cases) < 2:
            raise SetupError("%s: pack must hold a 'cases' list of >=2 cases"
                             % path.name)
        case_rows = []
        for obj in cases:
            spec = analyze_case(path.name, obj)
            if spec.cid in seen:
                raise SetupError("duplicate case id %s in %s and %s"
                                 % (spec.cid, seen[spec.cid], path.name))
            seen[spec.cid] = path.name
            specs.append(spec)
            case_rows.append(spec.cid)
        entries.append({
            "name": path.name,
            "sha256": sha256_bytes(raw),
            "cases": case_rows,
        })
    return specs, entries


# ---------------------------------------------------------------------------
# expected (pin) table
# ---------------------------------------------------------------------------


def build_expected(gate_sha: str, tool_path: Path, entries) -> dict:
    present = tool_path.is_file()
    return {
        "schema": EXPECTED_SCHEMA,
        "gate": "tools/mori-round16-regressions.py",
        "gate_sha256": gate_sha,
        "tool": {
            "path": rel_or_abs(tool_path),
            "present": present,
            "sha256": sha256_file(tool_path) if present else None,
        },
        "fixtures_dir": rel_or_abs(DEFAULT_FIXTURES),
        "packs": entries,
    }


def load_expected(path: Path) -> dict:
    if not Path(path).is_file():
        raise SetupError(
            "expected table missing: %s; pin inputs once with "
            "`python3 %s --pin-fixtures PATH`"
            % (path, rel_or_abs(Path(__file__))))
    try:
        raw = Path(path).read_bytes()
        expected = strict_json(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        raise SetupError("cannot read expected table %s: %s" % (path, exc))
    if not isinstance(expected, dict) \
            or expected.get("schema") != EXPECTED_SCHEMA:
        raise SetupError("expected table %s has schema %r want %r"
                         % (path,
                            expected.get("schema")
                            if isinstance(expected, dict) else None,
                            EXPECTED_SCHEMA))
    if not isinstance(expected.get("packs"), list) or not expected["packs"]:
        raise SetupError("expected table %s carries no pack entries" % path)
    return {"raw": raw, "doc": expected}


def compare_expected(expected: dict, entries, gate_sha: str) -> None:
    """Fixture + gate digest validation; runs even when the tool is absent."""
    doc = expected["doc"]
    if doc.get("gate_sha256") != gate_sha:
        raise SetupError(
            "gate digest mismatch: expected table was pinned for gate "
            "sha256=%s but this file hashes %s; re-pin with --pin-fixtures"
            % (doc.get("gate_sha256"), gate_sha))
    pinned = {}
    for row in doc["packs"]:
        if not isinstance(row, dict) or not isinstance(row.get("name"), str) \
                or not isinstance(row.get("sha256"), str):
            raise SetupError("expected table pack row malformed")
        pinned[row["name"]] = row["sha256"]
    current = {row["name"]: row["sha256"] for row in entries}
    if set(pinned) != set(current):
        raise SetupError(
            "fixture pack set drifted: pinned=%s current=%s"
            % (",".join(sorted(pinned)), ",".join(sorted(current))))
    for name, sha in sorted(pinned.items()):
        if current[name] != sha:
            raise SetupError(
                "fixture pack tampered since pin: %s pinned=%s current=%s"
                % (name, sha, current[name]))


def check_tool_digest(expected: dict, tool_path: Path) -> str | None:
    """Validate the tool digest.  Returns a manifest note or raises rc2.

    Callers must run this only after confirming the tool file exists; an
    absent tool takes the capability_absent path before any digest check.
    """
    pinned = expected["doc"].get("tool")
    if not isinstance(pinned, dict):
        raise SetupError("expected table lacks a tool entry")
    pin_sha = pinned.get("sha256")
    actual = sha256_file(tool_path)
    if pin_sha is None:
        return "tool digest unpinned at --pin-fixtures time; recorded only"
    if pin_sha != actual:
        raise SetupError(
            "tool digest mismatch: pinned=%s current=%s for %s; an existing "
            "but different tool is a tamper/setup failure, never a baseline"
            % (pin_sha, actual, rel_or_abs(tool_path)))
    return None


# ---------------------------------------------------------------------------
# revision provenance (paths only; never file contents)
# ---------------------------------------------------------------------------


def _git(args, timeout=30):
    env = dict(os.environ)
    env["GIT_PAGER"] = "cat"
    try:
        proc = subprocess.run(
            ["git", "-C", str(REPO)] + args, capture_output=True,
            timeout=timeout, env=env)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout


def capture_revision() -> dict:
    head_raw = _git(["rev-parse", "HEAD"])
    status_raw = _git(["status", "--porcelain"])
    return {
        "head": head_raw.decode("ascii", "replace").strip()
        if head_raw else None,
        "porcelain": status_raw.decode("utf-8", "replace")
        if status_raw is not None else None,
    }


# ---------------------------------------------------------------------------
# output guards
# ---------------------------------------------------------------------------


def guard_output(output: Path, protected) -> None:
    raw = Path(output)
    if raw.is_symlink():
        raise SetupError("--output must not be a symlink: %s" % raw)
    out = raw.resolve()
    if out.exists():
        if not out.is_dir():
            raise SetupError("--output exists and is not a directory: %s"
                             % out)
        if any(out.iterdir()):
            raise SetupError("--output directory must be empty: %s" % out)
    for protected_path, label in protected:
        pp = Path(protected_path).resolve()
        if out == pp or out.is_relative_to(pp) or pp.is_relative_to(out):
            raise SetupError(
                "--output must not cover, equal or sit under %s (%s); "
                "declared inputs are never output" % (label, rel_or_abs(pp)))
    if out == REPO or REPO.is_relative_to(out):
        raise SetupError("--output must not equal or contain the repository "
                         "root")
    for protected_path in (REPO / "tools", REPO / ".git", REPO / "corpus"):
        if out == protected_path or out.is_relative_to(protected_path):
            raise SetupError("--output must not be inside protected tree %s"
                             % rel_or_abs(protected_path))


# ---------------------------------------------------------------------------
# per-case materialisation
# ---------------------------------------------------------------------------


def materialize_case(root: Path, spec: CaseSpec, effective_max: int,
                     sleep_s: int) -> dict:
    """Write anchor file, payloads and the executable journalctl wrapper."""
    root = Path(root)
    if root.is_symlink() or (root.exists() and not root.is_dir()):
        raise SetupError("case dir unsafe: %s" % root)
    root.mkdir(parents=True, exist_ok=True)

    anchor_path = root / "anchor.json"
    if spec.anchor is not None:
        if spec.anchor_raw is not None:
            atomic_bytes(anchor_path, spec.anchor_raw.encode("utf-8"))
        else:
            atomic_bytes(
                anchor_path,
                (json.dumps(spec.anchor, indent=2, sort_keys=True) + "\n")
                .encode("utf-8"))
    # anchor None: file intentionally absent; the path is still passed.

    out_payload = root / "payload-stdout.bin"
    err_payload = root / "payload-stderr.bin"
    atomic_bytes(out_payload, spec.stdout.encode("utf-8"))
    atomic_bytes(err_payload, spec.stderr.encode("utf-8"))

    pad = 0
    if spec.overflow:
        pad = max(1, effective_max - len(spec.stdout.encode("utf-8")) + 1)

    argv_log = root / "journalctl-argv.txt"
    wrapper = root / "journalctl-stub.py"
    lines = [
        "#!%s" % sys.executable,
        "import os, sys, time",
        "_OUT = %r" % str(out_payload),
        "_ERR = %r" % str(err_payload),
        "_LOG = %r" % str(argv_log),
        "_PAD = %d" % pad,
        "_SLEEP = %d" % sleep_s,
        "_RC = %d" % spec.returncode,
        "def _emit():",
        "    data = open(_OUT, 'rb').read() + b'x' * _PAD",
        "    off = 0",
        "    while off < len(data):",
        "        off += os.write(1, data[off:])",
        "    err = open(_ERR, 'rb').read()",
        "    off = 0",
        "    while off < len(err):",
        "        off += os.write(2, err[off:])",
        "with open(_LOG, 'w') as fh:",
        "    fh.write('\\x00'.join(sys.argv[1:]))",
    ]
    if spec.timeout:
        # AttackBound arm: a non-exec grandchild holds the pipe open so a
        # tool that only waits on EOF still hits its own --timeout bound,
        # and a tool that kills only the wrapper pid leaves a bounded
        # (<_SLEEP) orphan that dies on SIGPIPE.  The wrapper exits now.
        lines += [
            "pid = os.fork()",
            "if pid == 0:",
            "    try:",
            "        time.sleep(_SLEEP)",
            "        _emit()",
            "    except (BrokenPipeError, OSError):",
            "        pass",
            "    finally:",
            "        os._exit(0)",
            "sys.exit(_RC)",
        ]
    else:
        lines += [
            "_emit()",
            "sys.exit(_RC)",
        ]
    atomic_bytes(wrapper, ("\n".join(lines) + "\n").encode("utf-8"),
                 mode=0o755)

    return {
        "anchor_path": anchor_path,
        "wrapper": wrapper,
        "argv_log": argv_log,
    }


def write_tripwire(output: Path) -> Path:
    """A PATH directory whose only `journalctl` is a bare-invocation canary."""
    bindir = Path(output) / "tripwire-bin"
    bindir.mkdir(parents=True, exist_ok=True)
    marker = Path(output) / "tripwire-hit"
    canary = bindir / "journalctl"
    atomic_bytes(canary, (
        "#!/bin/sh\n"
        "printf 'bare-journalctl-invoked\\n' >> %s\n"
        "exit 0\n" % marker
    ).encode("utf-8"), mode=0o755)
    return bindir


# ---------------------------------------------------------------------------
# bounded tool subprocess
# ---------------------------------------------------------------------------


def run_tool(argv: list, env: dict, cwd: Path, timeout_s: int, cap: int):
    """Run the tool with both streams byte-capped.  Never unbounded.

    Returns (out_bytes, err_bytes, rc, timed_out, capped, error).
    """
    started = time.monotonic()
    try:
        proc = subprocess.Popen(
            argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, env={str(k): str(v) for k, v in
                                         env.items()},
            cwd=str(cwd), start_new_session=True)
    except OSError as exc:
        return b"", b"", None, False, False, "%s: %s" % (type(exc).__name__,
                                                       exc)

    sel = selectors.DefaultSelector()
    bufs = {}
    for name, pipe in (("out", proc.stdout), ("err", proc.stderr)):
        os.set_blocking(pipe.fileno(), False)
        sel.register(pipe, selectors.EVENT_READ, name)
        bufs[name] = bytearray()
    timed_out = capped = False
    deadline = started + timeout_s
    while sel.get_map():
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            timed_out = True
            break
        events = sel.select(min(remaining, 0.2))
        for key, _ in events:
            try:
                chunk = os.read(key.fileobj.fileno(), 65536)
            except OSError:
                chunk = b""
            if not chunk:
                sel.unregister(key.fileobj)
                key.fileobj.close()
                continue
            bufs[key.data] += chunk
            if len(bufs[key.data]) > cap:
                capped = True
                break
        if capped:
            break
    if timed_out or capped:
        try:
            os.killpg(os.getpgid(proc.pid), 9)
        except (ProcessLookupError, PermissionError):
            pass
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:  # D-state/unkillable: report, move on
        pass
    sel.close()
    return (bytes(bufs["out"]), bytes(bufs["err"]), proc.returncode,
            timed_out, capped, None)


# ---------------------------------------------------------------------------
# grading
# ---------------------------------------------------------------------------


def _journalctl_argv_rows(log_path: Path):
    if not log_path.is_file():
        return []
    raw = log_path.read_bytes()
    if raw.endswith(b"\x00"):
        raw = raw[:-1]
    if not raw:
        return []
    return [row.decode("utf-8", "replace").split("\x00")
            for row in raw.split(b"\n")]


# Canonical one-scope cursor invocation per the shared contract and the
# L1 argv directive: exactly one scope flag, one --cursor=<exact anchor>,
# --no-pager/--quiet/--no-tail/--output=json, the exact allowed field list;
# every filter/seek-alternative flag is forbidden so a canned fixture stream
# can never hide a wrong production query.
JCTL_EXACT_ARGS = (
    "--no-pager", "--quiet", "--no-tail", "--output=json",
    "--output-fields=" + OUTPUT_FIELDS,
)
JCTL_FORBIDDEN_PREFIXES = (
    "--after-cursor", "--cursor-file", "--vacuum", "--rotate",
    "--sync", "--flush", "--grep", "--since", "--until",
)
JCTL_FORBIDDEN_ARGS = (
    "--reverse", "-b", "--boot", "-n", "--lines", "-f", "--follow",
    "-u", "--unit", "--user-unit", "-t", "--identifier", "-p",
    "--priority", "-g", "-k", "--dmesg", "MESSAGE",
)


def check_journalctl_argv(spec: CaseSpec, rows) -> list:
    """Assert the single canonical contract query; return reasons (never
    the cursor or record bytes)."""
    reasons = []
    want_calls = spec.expected_journalctl_calls()
    if len(rows) != want_calls:
        reasons.append("journalctl_calls=%d want=%d"
                       % (len(rows), want_calls))
        return reasons
    if not rows:
        return reasons
    argv = rows[0]

    scope_flag = "--user" if spec.scope == "user" else "--system"
    other_flag = "--system" if spec.scope == "user" else "--user"
    if argv.count(scope_flag) != 1 or other_flag in argv:
        reasons.append("journalctl_argv:scope_flag")

    cursor_args = [a for a in argv if a.startswith("--cursor=")]
    if spec.anchor is not None:
        want_cursor = "--cursor=" + spec.anchor["cursor"]
        if cursor_args != [want_cursor]:
            reasons.append("journalctl_argv:cursor_arg_mismatch")
    elif cursor_args:
        reasons.append("journalctl_argv:cursor_on_null_anchor")

    for exact in JCTL_EXACT_ARGS:
        if argv.count(exact) != 1:
            reasons.append("journalctl_argv:exact_arg_count:%s"
                           % exact.split("=", 1)[0])
    fields_args = [a for a in argv if a.startswith("--output-fields=")]
    if fields_args and fields_args[0].split("=", 1)[1].split(",") != \
            OUTPUT_FIELDS.split(","):
        reasons.append("journalctl_argv:output_fields_mismatch")
    elif fields_args and "MESSAGE" in \
            fields_args[0].split("=", 1)[1].split(","):
        reasons.append("journalctl_argv:message_field_requested")

    allowed = set(JCTL_EXACT_ARGS) | {scope_flag} | set(cursor_args)
    for arg in argv:
        if arg in allowed:
            continue
        if arg in JCTL_FORBIDDEN_ARGS or arg.startswith(
                JCTL_FORBIDDEN_PREFIXES):
            reasons.append("journalctl_argv:forbidden_arg:%s"
                           % arg.split("=", 1)[0])
        else:
            reasons.append("journalctl_argv:unexpected_arg:%s"
                           % arg.split("=", 1)[0])
    if len(argv) != len(set(argv)):
        reasons.append("journalctl_argv:duplicate_args")
    return reasons


def leak_check(spec: CaseSpec, tool_stdout: str, parsed) -> list:
    """Raw cursors, raw records and stderr canaries never reach stdout."""
    reasons = []
    end_cursor = parsed.get("end_cursor") if isinstance(parsed, dict) \
        else None
    cursors = []
    if spec.anchor is not None and cursor_ok(spec.anchor.get("cursor")):
        cursors.append(spec.anchor["cursor"])
    records, _ = _parse_jsonl(spec.stdout)
    lines = spec.stdout.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    if records:
        for rec, line in zip(records, lines):
            if isinstance(rec, dict):
                cur = rec.get("__CURSOR")
                if isinstance(cur, str):
                    cursors.append(cur)
            if len(line) >= 24 and line in tool_stdout:
                reasons.append("raw_record_echoed")
                break
    for cur in set(cursors):
        if len(cur) >= 16 and cur != end_cursor and cur in tool_stdout:
            reasons.append("raw_cursor_echoed")
            break
    for line in spec.stderr.split("\n"):
        text = line.strip()
        if len(text) >= 16 and text in tool_stdout:
            reasons.append("stderr_canary_echoed")
            break
    for token in set(CANARY_TOKEN_RE.findall(spec.stderr)):
        if token in tool_stdout:
            reasons.append("stderr_token_echoed:%s" % token[:16])
            break
    return reasons


def evaluate(spec: CaseSpec, out: bytes, err: bytes, rc, timed_out, capped,
             error, argv_rows, tripwire_hit: bool) -> tuple:
    """Return (ok, reasons, observed).  Reasons never echo record bytes."""
    reasons = []
    if timed_out:
        reasons.append("harness_timeout")
    if capped:
        reasons.append("tool_output_cap_exceeded")
    if error:
        reasons.append("exec_error")
    if rc != spec.want_rc:
        reasons.append("rc=%s want=%d" % (rc, spec.want_rc))

    text = out.decode("utf-8", "replace")
    parsed = None
    try:
        parsed = strict_json(text.strip() if text.strip() else text)
        if not isinstance(parsed, dict):
            reasons.append("stdout_not_json_object")
            parsed = None
    except (UnicodeDecodeError, ValueError):
        reasons.append("stdout_not_single_json_object")
        parsed = None

    finding_id = parsed.get("finding_id") if parsed else None
    if finding_id != spec.want_id:
        reasons.append("finding_id=%r want=%s" % (finding_id, spec.want_id))

    if parsed is not None:
        banned = FORBIDDEN_KEYS & set(parsed)
        if banned:
            reasons.append("forbidden_keys:%s" % ",".join(sorted(banned)))
        if any(k.startswith("positive_") and k not in COUNT_KEYS
               for k in parsed):
            reasons.append("unknown_positive_key")

        if spec.want_rc == 0:
            for key in sorted(OK_REQUIRED):
                if key not in parsed:
                    reasons.append("missing_key:%s" % key)
            for key in COUNT_KEYS:
                value = parsed.get(key)
                if isinstance(value, bool) or not isinstance(value, int) \
                        or value < 0:
                    reasons.append("%s not a non-bool int >= 0" % key)
            if parsed.get("scope") != spec.scope:
                reasons.append("scope=%r want=%s"
                               % (parsed.get("scope"), spec.scope))
            if parsed.get("evidence_basis") != "validated-record-subsets":
                reasons.append("evidence_basis=%r want="
                               "validated-record-subsets"
                               % parsed.get("evidence_basis"))
            total = parsed.get("records_after_anchor")
            subsets = [parsed.get(k) for k in COUNT_KEYS[1:]]
            if isinstance(total, int) and not isinstance(total, bool) \
                    and all(isinstance(v, int) and not isinstance(v, bool)
                            for v in subsets):
                if total < sum(subsets):
                    reasons.append("records_after_anchor=%d < sum of "
                                   "positive subsets=%d"
                                   % (total, sum(subsets)))
        else:
            leaked = [k for k in parsed if k in RC2_FORBIDDEN_KEYS
                      or k.startswith("positive_")]
            if leaked:
                reasons.append("rc2 carries count/evidence keys: %s"
                               % ",".join(sorted(leaked)))
            if spec.want_id == FINDING_UNAVAILABLE \
                    and not isinstance(parsed.get("reason"), str):
                reasons.append("unavailable missing stable string reason")

        for key, want in spec.want.items():
            if key not in parsed:
                reasons.append("want.%s absent" % key)
            elif not strict_eq(parsed[key], want):
                reasons.append("want.%s=%r got %r"
                               % (key, want, parsed[key]))
        reasons.extend(leak_check(spec, text, parsed))

    reasons.extend(check_journalctl_argv(spec, argv_rows))
    if tripwire_hit:
        reasons.append("bare_journalctl_tripwire")

    observed = {
        "rc": rc,
        "finding_id": finding_id,
        "keys": sorted(parsed) if isinstance(parsed, dict) else None,
        "journalctl_calls": len(argv_rows),
        "stdout_bytes": len(out),
        "stderr_bytes": len(err),
    }
    return (not reasons), reasons, observed


# ---------------------------------------------------------------------------
# pin mode
# ---------------------------------------------------------------------------


def run_pin(args, gate_sha: str) -> int:
    fixtures_dir = Path(args.fixtures).resolve()
    specs, entries = load_packs(fixtures_dir)
    target = Path(args.pin_fixtures).resolve()
    if target.is_relative_to(fixtures_dir):
        raise SetupError("pin target must not live inside the fixtures "
                         "directory (it would become a pack): %s" % target)
    tool_path = Path(args.tool).resolve()
    manifest = build_expected(gate_sha, tool_path, entries)
    manifest["fixtures_dir"] = rel_or_abs(fixtures_dir)
    atomic_json(target, manifest)
    tool_row = manifest["tool"]
    print("PINNED %s" % target)
    print("PIN packs=%d cases=%d gate_sha256=%s"
          % (len(entries), len(specs), gate_sha))
    print("PIN tool=%s present=%s sha256=%s"
          % (tool_row["path"], tool_row["present"], tool_row["sha256"]))
    if not tool_row["present"]:
        print("PIN NOTE tool absent at pin time; digest validation is "
              "skipped until a re-pin with the landed tool")
    return 0


# ---------------------------------------------------------------------------
# gate mode
# ---------------------------------------------------------------------------


def write_manifest(output: Path, doc: dict) -> None:
    atomic_json(Path(output) / "run-manifest.json", doc)


def run_gate(args, gate_sha: str) -> int:
    if not args.output:
        raise SetupError("--output DIR is required unless "
                         "--pin-fixtures/--selftest")
    output_raw = Path(args.output)
    output = output_raw.resolve()
    fixtures_dir = Path(args.fixtures).resolve()
    tool_path = Path(args.tool).resolve()
    expected_path = Path(args.expected).resolve()
    guard_output(output_raw, [
        (fixtures_dir, "the fixture directory"),
        (expected_path, "the expected table"),
        (tool_path, "the tool under test"),
        (tool_path.parent, "the tool directory"),
    ])

    specs, entries = load_packs(fixtures_dir)
    expected = load_expected(expected_path)
    compare_expected(expected, entries, gate_sha)

    output.mkdir(parents=True, exist_ok=True)
    for sub in ("runs", "cases", "wrappers"):
        (output / sub).mkdir(parents=True, exist_ok=True)
    atomic_bytes(output / "expected.json", expected["raw"])

    if args.case:
        wanted = [p for p in args.case.split(",") if p]
        known = {s.cid for s in specs}
        missing = [p for p in wanted if p not in known]
        if missing:
            raise SetupError("unknown --case id(s): %s" % ",".join(missing))
        wanted_set = set(wanted)
        specs = [s for s in specs if s.cid in wanted_set]
    if not specs:
        raise SetupError("no cases selected")

    start_hashes = {row["name"]: row["sha256"] for row in entries}
    revision = capture_revision()
    tool_present = tool_path.is_file() and not tool_path.is_symlink()
    tool_sha = sha256_file(tool_path) if tool_present else None
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "gate": "tools/mori-round16-regressions.py",
        "gate_sha256": gate_sha,
        "tool": {
            "path": rel_or_abs(tool_path),
            "present": tool_present,
            "sha256": tool_sha,
        },
        "fixtures": {
            "dir": rel_or_abs(fixtures_dir),
            "start_hashes": start_hashes,
            "end_hashes": None,
            "inputs_moved": None,
        },
        "expected": {
            "path": rel_or_abs(expected_path),
            "sha256": sha256_bytes(expected["raw"]),
        },
        "git": revision,
        "cases": [],
        "summary": None,
        "verdict": None,
        "exit_code": None,
    }

    if not tool_present:
        # Entering-capability baseline: fixtures and gate digests validated
        # above; the tool digest is never consulted.  Every finite case
        # records capability_absent, distinct from any real red.
        for spec in specs:
            manifest["cases"].append({
                "id": spec.cid, "pack": spec.pack, "ok": False,
                "status": "capability_absent",
                "reasons": ["capability_absent"],
                "observed": None,
            })
        manifest["summary"] = {
            "total": len(specs), "matched": 0, "mismatched": 0,
            "capability_absent": len(specs),
        }
        manifest["verdict"] = "capability_absent"
        manifest["exit_code"] = 1
        write_manifest(output, manifest)
        print("GATE capability_absent: --tool %s does not exist; %d cases "
              "recorded absent (rc1), digests enforced" % (tool_path,
                                                           len(specs)))
        return 1

    note = check_tool_digest(expected, tool_path)
    if note:
        manifest["tool"]["note"] = note

    tripwire_bin = write_tripwire(output)
    env = {
        "PATH": str(tripwire_bin),
        "LC_ALL": "C",
        "TZ": "UTC",
    }
    matched = mismatched = 0
    for spec in specs:
        case_dir = output / "cases" / spec.cid
        if spec.timeout:
            tool_timeout = TOOL_TIMEOUT_CASE
            sleep_s = WRAPPER_SLEEP_S
        else:
            tool_timeout = TOOL_TIMEOUT_NORMAL
            sleep_s = 0
        if spec.max_bytes is not None:
            effective_max = spec.max_bytes
        elif spec.overflow:
            effective_max = len(spec.stdout.encode("utf-8"))
        else:
            effective_max = len(spec.stdout.encode("utf-8")) \
                + MAX_BYTES_SLACK

        paths = materialize_case(case_dir, spec, effective_max, sleep_s)
        argv = [
            sys.executable, str(tool_path),
            "--anchor", str(paths["anchor_path"]),
            "--scope", spec.scope,
            "--journalctl", str(paths["wrapper"]),
            "--timeout", str(tool_timeout),
            "--max-bytes", str(effective_max),
        ]
        run_timeout = max(args.run_timeout, tool_timeout + sleep_s + 15)
        out, err, rc, timed_out, capped, error = run_tool(
            argv, env, case_dir, run_timeout, args.capture_cap)

        out_path = output / "runs" / ("%s.stdout" % spec.cid)
        err_path = output / "runs" / ("%s.stderr" % spec.cid)
        atomic_bytes(out_path, out)
        atomic_bytes(err_path, err)

        argv_rows = _journalctl_argv_rows(paths["argv_log"])
        tripwire_hit = (output / "tripwire-hit").exists()
        ok, reasons, observed = evaluate(
            spec, out, err, rc, timed_out, capped, error,
            argv_rows, tripwire_hit)
        if ok:
            matched += 1
        else:
            mismatched += 1
        manifest["cases"].append({
            "id": spec.cid, "pack": spec.pack,
            "ok": ok,
            "status": "match" if ok else "mismatch",
            "reasons": reasons,
            "observed": observed,
            "argv_sha256": sha256_bytes(
                canonical([[a if not a.startswith("--cursor=")
                            else "--cursor=sha256:" +
                            sha256_bytes(a.encode())[:16]
                            for a in row] for row in argv_rows]
                          ).encode("utf-8")),
            "stdout_sha256": sha256_bytes(out),
            "stderr_sha256": sha256_bytes(err),
        })

    # Moving-input refusal: re-hash every pack at end; any drift is tamper.
    end_hashes = {}
    moved = []
    for row in entries:
        path = fixtures_dir / row["name"]
        digest = sha256_file(path) if path.is_file() else None
        end_hashes[row["name"]] = digest
        if digest != row["sha256"]:
            moved.append(row["name"])
    manifest["fixtures"]["end_hashes"] = end_hashes
    manifest["fixtures"]["inputs_moved"] = bool(moved)

    if moved:
        manifest["summary"] = {
            "total": len(specs), "matched": matched,
            "mismatched": mismatched, "capability_absent": 0,
        }
        manifest["verdict"] = "tamper:moving-input"
        manifest["exit_code"] = 2
        write_manifest(output, manifest)
        print("GATE tamper: inputs moved during run: %s"
              % ",".join(moved), file=sys.stderr)
        return 2

    verdict = "ok" if mismatched == 0 else "mismatch"
    manifest["summary"] = {
        "total": len(specs), "matched": matched,
        "mismatched": mismatched, "capability_absent": 0,
    }
    manifest["verdict"] = verdict
    manifest["exit_code"] = 0 if mismatched == 0 else 1
    write_manifest(output, manifest)
    print("GATE %s: %d/%d cases matched (%s)"
          % (verdict, matched, len(specs), rel_or_abs(output)))
    return manifest["exit_code"]


# ---------------------------------------------------------------------------
# selftest — real isolated subprocess arms; never the production tool
# ---------------------------------------------------------------------------


_STUB_TOOL = r'''
import json, os, re, selectors, subprocess, sys

FINDING_OK = "MORI_JOURNAL_WINDOW_OK"
FINDING_UNAVAILABLE = "MORI_JOURNAL_WINDOW_UNAVAILABLE"
FINDING_SETUP = "MORI_JOURNAL_WINDOW_SETUP"
KERNEL_OOM_ID = "fe6faa94e7774663a0da52717891d8ef"
UNIT_FAILURE_ID = "d9b373ed55a64feb8242e02dbe79a49c"
PROCESS_EXIT_ID = "98e322203f7a4ed290d09fe03c09fe15"
BOOT_RE = re.compile(r"^[0-9a-f]{32}$")


def emit(obj, rc):
    sys.stdout.write(json.dumps(obj, sort_keys=True) + "\n")
    sys.exit(rc)


def setup_fail(reason):
    emit({"finding_id": FINDING_SETUP, "reason": reason}, 2)


def unavailable(reason):
    emit({"finding_id": FINDING_UNAVAILABLE, "reason": reason}, 2)


def scalar_cursor(v):
    return isinstance(v, str) and 0 < len(v) <= 4096 \
        and all(32 <= ord(c) <= 126 for c in v)


def main():
    args = sys.argv[1:]
    opts = {}
    i = 0
    while i < len(args):
        if args[i].startswith("--") and "=" in args[i]:
            k, v = args[i].split("=", 1)
            opts[k] = v
        elif args[i].startswith("--"):
            opts[args[i]] = args[i + 1]
            i += 1
        i += 1
    anchor_path = opts.get("--anchor")
    scope = opts.get("--scope")
    journalctl = opts.get("--journalctl")
    timeout = int(opts.get("--timeout", "10"))
    max_bytes = int(opts.get("--max-bytes", "1048576"))
    if scope not in ("user", "system") or not journalctl:
        setup_fail("args")

    try:
        anchor = json.loads(open(anchor_path).read())
    except (OSError, ValueError):
        setup_fail("anchor-unreadable")
    if not isinstance(anchor, dict) \
            or anchor.get("schema") != "mori-journal-anchor-v1" \
            or anchor.get("scope") not in ("user", "system") \
            or not isinstance(anchor.get("boot_id"), str) \
            or not BOOT_RE.match(anchor["boot_id"]) \
            or not scalar_cursor(anchor.get("cursor")) \
            or set(anchor) - {"schema", "scope", "boot_id", "cursor"}:
        setup_fail("anchor-invalid")
    if anchor["scope"] != scope:
        setup_fail("anchor-scope-mismatch")

    argv = [journalctl,
            "--cursor=" + anchor["cursor"],
            "--no-pager", "--no-tail", "--quiet", "--output=json",
            "--output-fields=__CURSOR,_BOOT_ID,MESSAGE_ID,UNIT_RESULT,"
            "EXIT_CODE,EXIT_STATUS"]
    argv.append("--user" if scope == "user" else "--system")
    proc = subprocess.Popen(argv, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, start_new_session=True)
    sel = selectors.DefaultSelector()
    bufs = {"o": bytearray(), "e": bytearray()}
    for name, p in (("o", proc.stdout), ("e", proc.stderr)):
        os.set_blocking(p.fileno(), False)
        sel.register(p, selectors.EVENT_READ, name)
    deadline = __import__("time").monotonic() + timeout
    over = tout = False
    while sel.get_map():
        rem = deadline - __import__("time").monotonic()
        if rem <= 0:
            tout = True
            break
        for key, _ in sel.select(min(rem, 0.1)):
            chunk = os.read(key.fileobj.fileno(), 65536)
            if not chunk:
                sel.unregister(key.fileobj)
                key.fileobj.close()
                continue
            bufs[key.data] += chunk
            if len(bufs["o"]) > max_bytes:
                over = True
                break
        if over:
            break
    if tout or over:
        try:
            os.killpg(os.getpgid(proc.pid), 9)
        except (ProcessLookupError, PermissionError):
            pass
    proc.wait()
    if tout:
        unavailable("timeout")
    if over:
        unavailable("overflow")
    if proc.returncode != 0:
        unavailable("rc-%d" % proc.returncode)
    if bufs["e"]:
        unavailable("stderr")

    lines = bytes(bufs["o"]).decode("utf-8").split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    if not lines:
        unavailable("empty-capture")
    records = []
    for line in lines:
        try:
            records.append(json.loads(line))
        except ValueError:
            unavailable("malformed-json")
    first = records[0]
    if not isinstance(first, dict) \
            or first.get("__CURSOR") != anchor["cursor"] \
            or first.get("_BOOT_ID") != anchor["boot_id"]:
        unavailable("anchor-missing")
    seen = {anchor["cursor"]}
    rest = records[1:]
    for rec in rest:
        if not isinstance(rec, dict):
            unavailable("record-not-object")
        if rec.get("_BOOT_ID") != anchor["boot_id"]:
            unavailable("foreign-boot")
        cur = rec.get("__CURSOR")
        if not scalar_cursor(cur) or cur in seen:
            unavailable("cursor-invalid")
        seen.add(cur)

    counts = {"records_after_anchor": len(rest),
              "positive_kernel_oom": 0, "positive_unit_oom": 0,
              "positive_unit_signal": 0, "positive_process_sigkill": 0}
    for rec in rest:
        mid = rec.get("MESSAGE_ID")
        if mid == KERNEL_OOM_ID:
            counts["positive_kernel_oom"] += 1
        elif mid == UNIT_FAILURE_ID:
            if rec.get("UNIT_RESULT") == "oom-kill":
                counts["positive_unit_oom"] += 1
            elif rec.get("UNIT_RESULT") == "signal":
                counts["positive_unit_signal"] += 1
        elif mid == PROCESS_EXIT_ID:
            st = rec.get("EXIT_STATUS")
            if rec.get("EXIT_CODE") == "killed" and \
                    (st == 9 and not isinstance(st, bool) or st == "9"):
                counts["positive_process_sigkill"] += 1
    out = {"finding_id": FINDING_OK, "scope": scope,
           "evidence_basis": "validated-record-subsets",
           "anchor_sha256": "selftest"}
    out.update(counts)
    if rest:
        out["end_cursor"] = rest[-1]["__CURSOR"]
    emit(out, 0)


main()
'''

_BOOT = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
_ANCHOR = {"schema": ANCHOR_SCHEMA, "scope": "user", "boot_id": _BOOT,
           "cursor": "selftest-anchor-cursor-0001"}


def _st_jsonl(*records) -> str:
    return "".join(json.dumps(r, separators=(",", ":")) + "\n"
                   for r in records)


def _st_anchor_rec(cursor=None, boot=None) -> dict:
    return {"__CURSOR": cursor or _ANCHOR["cursor"],
            "_BOOT_ID": boot or _BOOT}


def _selftest_fixtures(root: Path, bad: bool = False) -> Path:
    fixtures = root / ("fixtures-bad" if bad else "fixtures")
    fixtures.mkdir(parents=True, exist_ok=True)
    positive = {"__CURSOR": "cursor-pos-1", "_BOOT_ID": _BOOT,
                "MESSAGE_ID": KERNEL_OOM_ID}
    benign = {"__CURSOR": "cursor-benign-1", "_BOOT_ID": _BOOT,
              "MESSAGE_ID": "53e1f4e67ea6409d93dd65b5a12cfaa8"}
    alpha_ok = {
        "id": "st-alpha-ok", "scope": "user", "anchor": dict(_ANCHOR),
        "stdout": _st_jsonl(_st_anchor_rec(), positive, benign),
        "stderr": "", "returncode": 0, "want_rc": 0,
        "want_id": FINDING_OK,
        "want": {"scope": "user", "records_after_anchor": 2,
                 "positive_kernel_oom": 1, "positive_unit_oom": 0,
                 "positive_unit_signal": 0, "positive_process_sigkill": 0},
    }
    alpha_refuse = {
        "id": "st-alpha-foreign", "scope": "user",
        "anchor": dict(_ANCHOR),
        "stdout": _st_jsonl(_st_anchor_rec(),
                            {"__CURSOR": "cursor-x", "_BOOT_ID":
                             "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"}),
        "stderr": "", "returncode": 0, "want_rc": 2,
        "want_id": FINDING_UNAVAILABLE, "want": {},
    }
    beta_rc = {
        "id": "st-beta-rc5", "scope": "user", "anchor": dict(_ANCHOR),
        "stdout": _st_jsonl(_st_anchor_rec(), positive),
        "stderr": "", "returncode": 5, "want_rc": 2,
        "want_id": FINDING_UNAVAILABLE, "want": {},
    }
    beta_stderr = {
        "id": "st-beta-stderr", "scope": "user", "anchor": dict(_ANCHOR),
        "stdout": _st_jsonl(_st_anchor_rec()),
        "stderr": "journal: MORI_STDERR_CANARY selftest\n",
        "returncode": 0, "want_rc": 2,
        "want_id": FINDING_UNAVAILABLE, "want": {},
    }
    gamma_timeout = {
        "id": "st-gamma-timeout", "scope": "user",
        "anchor": dict(_ANCHOR), "stdout": _st_jsonl(_st_anchor_rec()),
        "stderr": "", "returncode": 0, "timeout": True,
        "want_rc": 2, "want_id": FINDING_UNAVAILABLE, "want": {},
    }
    gamma_overflow = {
        "id": "st-gamma-overflow", "scope": "user",
        "anchor": dict(_ANCHOR), "stdout": _st_jsonl(_st_anchor_rec(),
                                                   positive),
        "stderr": "", "returncode": 0, "overflow": True,
        "want_rc": 2, "want_id": FINDING_UNAVAILABLE, "want": {},
    }
    packs = {
        "Alpha.json": [alpha_ok, alpha_refuse],
        "Beta.json": [beta_rc, beta_stderr],
        "Gamma.json": [gamma_timeout, gamma_overflow],
    }
    if bad:
        # A wrong non-count subset key keeps the pack schema-consistent
        # (oracle checks only the count tokens) but the stub answers the
        # contract-correct value, producing a real rc1 mismatch.
        packs["Alpha.json"][0] = dict(
            alpha_ok, want=dict(alpha_ok["want"], scope="system"))
    for name, cases in packs.items():
        (fixtures / name).write_text(json.dumps({"cases": cases}, indent=2),
                                     encoding="utf-8")
    return fixtures


def _selftest_run(gate: Path, argv: list, expect_rc: int, label: str):
    proc = subprocess.run(
        [sys.executable, str(gate)] + argv,
        capture_output=True, text=True, timeout=300)
    if proc.returncode != expect_rc:
        raise AssertionError(
            "%s: gate rc=%s want=%s\nstdout: %s\nstderr: %s"
            % (label, proc.returncode, expect_rc,
               one_line(proc.stdout), one_line(proc.stderr)))
    return proc


def _manifest(output: Path) -> dict:
    return strict_json((Path(output) / "run-manifest.json").read_text())


def selftest() -> int:
    gate = Path(__file__).resolve()
    checks = []
    with tempfile.TemporaryDirectory(prefix="mori-r16-selftest-") as td:
        root = Path(td)
        tool_dir = root / "tools"
        tool_dir.mkdir()
        stub = tool_dir / "mori-journal-window.py"
        stub.write_text(_STUB_TOOL, encoding="utf-8")
        fixtures = _selftest_fixtures(root)
        expected = root / "expected.json"

        _selftest_run(gate, ["--pin-fixtures", str(expected),
                             "--fixtures", str(fixtures),
                             "--tool", str(stub)], 0, "pin")
        checks.append("pin_rc0")

        green = root / "out-green"
        _selftest_run(gate, ["--tool", str(stub), "--fixtures", str(fixtures),
                             "--expected", str(expected),
                             "--output", str(green)], 0, "green")
        man = _manifest(green)
        assert man["verdict"] == "ok", man["verdict"]
        assert man["summary"]["matched"] == man["summary"]["total"] == 6
        assert all(c["status"] == "match" for c in man["cases"])
        checks.append("green_rc0_verdict_ok")

        absent_out = root / "out-absent"
        _selftest_run(gate, ["--tool", str(tool_dir / "absent-tool.py"),
                             "--fixtures", str(fixtures),
                             "--expected", str(expected),
                             "--output", str(absent_out)], 1, "absent")
        man = _manifest(absent_out)
        assert man["verdict"] == "capability_absent"
        assert all(c["status"] == "capability_absent" for c in man["cases"])
        checks.append("absent_rc1_capability_absent")

        tampered = tool_dir / "tampered-tool.py"
        tampered.write_text(_STUB_TOOL + "\n# drift\n", encoding="utf-8")
        _selftest_run(gate, ["--tool", str(tampered),
                             "--fixtures", str(fixtures),
                             "--expected", str(expected),
                             "--output", str(root / "out-tamper")],
                      2, "tool-tamper")
        checks.append("tool_drift_rc2")

        bad_fixtures = _selftest_fixtures(root, bad=True)
        bad_expected = root / "expected-bad.json"
        _selftest_run(gate, ["--pin-fixtures", str(bad_expected),
                             "--fixtures", str(bad_fixtures),
                             "--tool", str(stub)], 0, "pin-bad")
        _selftest_run(gate, ["--tool", str(stub),
                             "--fixtures", str(bad_fixtures),
                             "--expected", str(bad_expected),
                             "--output", str(root / "out-mismatch")],
                      1, "mismatch")
        man = _manifest(root / "out-mismatch")
        assert man["verdict"] == "mismatch"
        checks.append("bad_want_rc1_mismatch")

        # Fixture tamper after pin: flip one byte, digests must refuse rc2.
        pack = fixtures / "Alpha.json"
        pack.write_bytes(pack.read_bytes() + b" ")
        _selftest_run(gate, ["--tool", str(stub),
                             "--fixtures", str(fixtures),
                             "--expected", str(expected),
                             "--output", str(root / "out-packtamper")],
                      2, "pack-tamper")
        checks.append("pack_drift_rc2")

    print("SELFTEST ok: %s" % ",".join(checks))
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="round-16 mori-journal-window fixture gate")
    parser.add_argument("--tool", default=str(DEFAULT_TOOL),
                        help="tool under test (absent path records "
                             "capability_absent, never green)")
    parser.add_argument("--fixtures", default=str(DEFAULT_FIXTURES))
    parser.add_argument("--expected", default=str(DEFAULT_EXPECTED))
    parser.add_argument("--output", help="run output directory (must be "
                                         "empty or absent)")
    parser.add_argument("--pin-fixtures", metavar="PATH",
                        help="write the expected digest table and exit")
    parser.add_argument("--case", help="comma-separated case id filter")
    parser.add_argument("--run-timeout", type=int, default=RUN_TIMEOUT_S,
                        help="harness per-run deadline seconds")
    parser.add_argument("--capture-cap", type=int, default=CAPTURE_CAP,
                        help="per-stream byte cap on tool output")
    parser.add_argument("--selftest", action="store_true",
                        help="run isolated subprocess self-checks; never "
                             "touches the production tool or fixtures")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    if args.selftest:
        try:
            return selftest()
        except (AssertionError, SetupError) as exc:
            print("SELFTEST FAIL: %s" % one_line(exc), file=sys.stderr)
            return 1
    try:
        gate_sha = sha256_file(Path(__file__).resolve())
        if args.pin_fixtures:
            return run_pin(args, gate_sha)
        return run_gate(args, gate_sha)
    except SetupError as exc:
        print("SETUP: %s" % one_line(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
