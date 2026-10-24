#!/usr/bin/env python3
"""mori-round13-regressions.py — round-13 regression gate (migrated round 14).

REGISTERED GATE (registry home: this lane's SKILL.md; row `r13 regressions`).
It reads committed targets, compares them against the expected values pinned in
this file, and returns a verdict. It is no longer described as an evidence
harness: a verdict-producing tool is a gate under PROTOCOL §Gate standard.

Round-14 C1 migration. The round-13 strict contract expected every structured
journal notice to be INFO and the roll to be CLEAN. The non-author round-13
spot-check rejected that cutover as harmed: the historical critical OOM alarm
and the fleet/non-fleet unit-failure partition disappeared. The C1 family below
now measures the RESTORED semantics (the round-14 repair):

  * a positive kernel-OOM notice in EITHER journal scope, or a structured
    `UNIT_RESULT=oom-kill` unit result, emits ONE global critical
    `OOM_KILL_JOURNAL` line whose separate `user_notice`/`system_notice`/
    `user_unit_oom`/`system_unit_oom` counters are never summed, and rolls
    DRIFT;
  * fleet unit failures keep the historical INFO `UNIT_FAILURE_JOURNAL`
    (evidence: pre-cutover probe_journal in the round-13 frozen census);
  * non-fleet unit failures emit INFO `UNIT_FAILURE_OUT_OF_SCOPE` with
    `owner=tsukuroi` and do not flip the roll;
  * absent/non-string subject metadata (`UNIT`/`USER_UNIT`, never the manager
    emitter `_SYSTEMD_UNIT`) is the explicit INFO
    `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` class (`owner=unresolved`), and the raw
    six scoped counts still include those records;
  * a user-scope generic SIGKILL process-exit record keeps its WARN
    `KILL_SIGNAL_JOURNAL` and DRIFT;
  * oomd/coredump/segfault notices stay INFO, so a positive notice-only
    fixture is the CLEAN control that keeps the alarm specific to OOM.

The six scoped counters, boot validation, error controls and MESSAGE exclusion
are preserved exactly; only the severity/partition expectations migrated. The
F01/F02 claims and their original-frozen comparisons are unchanged.

Claims measured (stable ids; one FINDING line each)

  R13_SHONEN_CANONICAL_BYTES            canonical HEAD SHONEN bytes (unindented)
  R13_SHONEN_INDENT_WITNESS             the comparator rejects indented bytes
  R13_C1_SYSTEM_NOTICE_COUNTS           system scope: six structured counts + OOM alarm
  R13_C1_USER_SCOPE_INDEPENDENT         user scope: separate zero tokens, never summed
  R13_C1_USER_SCOPE_NONZERO             user-only kernel OOM => critical alarm + DRIFT
  R13_C1_NO_MESSAGE_TEXT                no synthetic MESSAGE key/value in stdout
  R13_C1_OOM_ALARM_DRIFT                kernel OOM notice => crit OOM_KILL_JOURNAL, DRIFT
  R13_C1_NOTICE_CLEAN_CONTROL           oomd/coredump/segfault notices stay INFO => CLEAN
  R13_C1_EMPTY_CLEAN_CONTROL            no records => six zero counts, CLEAN, no alarm
  R13_C1_UNIT_OOM_KILL_ALARM            UNIT_RESULT=oom-kill => crit alarm, raw count kept
  R13_C1_UNIT_FAILURE_ROUTING           fleet INFO / non-fleet INFO owner=tsukuroi / unknown
  R13_C1_SIGKILL_WARN_PRESERVED         generic user SIGKILL record keeps WARN => DRIFT
  R13_F01_EXACT_AUTHOR_LONG_HISTORY     12001-line history: subject commit grades progressing
  R13_F01_SIBLING_CONTROL_LONG_HISTORY  12000 sibling commits grade progressing-weak
  R13_F02_HONEST_28_OF_28               honest census scores 28/28 rc0
  R13_F02_REJECT_BANANA                 substituted roll rejected
  R13_F02_REJECT_DUPLICATE_VERDICT      two roll lines rejected
  R13_F02_REJECT_MISSING_VERDICT        no roll line rejected
  R13_F02_REJECT_NOT_FINAL_VERDICT      a trailing line after the roll rejected
  R13_F02_REJECT_VERDICT_FIRST          a roll moved off the last line rejected
  R13_F02_REJECT_CLEAN_DRIFT9           CLEAN roll with drift=9 rejected
  R13_F02_REJECT_DRIFT_DRIFT0           DRIFT roll with drift=0 rejected
  R13_F02_REJECT_CLEAN_RC1              CLEAN word with rc1 rejected (selective PASS set)
  R13_F02_REJECT_DRIFT_RC0              DRIFT word with rc0 rejected (selective PASS set)
  R13_MUTATION_F01_RED_BEFORE           frozen grade_lane transplanted => F01 returns
  R13_MUTATION_F02_RED_BEFORE           verdict gate reverted => BANANA accepted

Fixture provenance (no `/tmp` evidence, no live host reads)

  * Long-history fixtures reproduce corpus/knowledge/audit-r11.md Appendix B:
    one exact subject author followed by 12,000 sibling log records through a
    stub `git` (a 12,001-line writer into the membership test).
  * Adversarial wrappers reproduce Appendix C and its siblings: a proxy census
    that renames or duplicates the final roll, or mismatches the roll to rc.
  * The C1 fixture serves synthetic `journalctl -o json` records through a stub
    that implements exact field matching (`FIELD=value` argv, OR within one
    field) and projects only `--output-fields`. Records carry structured
    `UNIT`/`USER_UNIT`/`UNIT_RESULT` fields as well as catalog MESSAGE_IDs, so
    the probe's queries — not a canned answer table — select the records. The
    synthetic MESSAGE value is a canary; the host journal is never opened.
  * Every fixture is created under a fresh temp directory inside the explicit
    --output tree, never under the repository and never at a live MORI path,
    and removed after the run unless --keep-fixtures.

Pinned values (independent of the snapshot they verify)

  The default round-13 frozen directory is pinned by `FROZEN_PINS` below: the
  two script digests, the `inputs.json` digest and the base commit are committed
  constants, so a coordinated edit of a frozen file *and* its sibling manifest
  still reads `snapshot_tampered`. A custom `--frozen-dir` cannot be pinned
  ahead of time; it is verified against its own manifest and recorded as
  `unpinned (custom frozen dir)` rather than pretending to a pin.

Modes

  default          strict contract: every claim must pass.
  --baseline       run the frozen pre-fix bytes (or the paths given) once and
                   *record* the audit-predicted defects. Expected defects are
                   reported as `expected-defect`, never `pass`; an observation
                   that does not match the baseline table is `baseline-deviation`.
                   The frozen pre-fix census is also the primary original-byte
                   before evidence; keep those runs primary over mutation claims.
  --mutation ID    run the strict suite, then build one isolated mutant from the
                   named fixed target and require the pre-fix defect to reappear.
                   IDs: f01, f02, both.

Mutation provenance (do not read these as byte-exact restoration)

  * f01 transplants the WHOLE frozen `grade_lane` function into the fixed
    census. It is not a membership-lines-only reversal and not a single-line
    revert: the frozen function also carries its older environment-hardening and
    fsmonitor behavior. The mutant proves the frozen function's behavior
    reappears; the original frozen bytes under `--baseline` remain the primary
    historical evidence.
  * f02 replaces the fixed `verdict_grade` with a RECONSTRUCTED prefix-presence
    shim (`frozen_source=null`, `reverted_by=pre_fix_prefix_presence_shim`); the
    pre-fix oracle had no such function body to restore. It proves the single
    verdict-validation locus is sufficient for BANANA acceptance, not
    original-byte causality.

Exit codes (declared registry map: 0 clean · 1 failed · 2 could-not-evaluate)

  0  clean: every claim satisfied in the selected mode
  1  failed: a claim failed (or a baseline observation deviated)
  2  could-not-evaluate: usage, setup, unreadable target, snapshot_tampered,
     unavailable revision, or a requested mutation that could not be built

Evidence: <output>/evidence.json plus <output>/runs/<run-id>.{stdout,stderr}.
Evidence names the measured git revision (explicit `MORI_EVIDENCE_REVISION` or
`git rev-parse HEAD`), the dirty flag, the registry status and the pinned
digests. Starting with this revision it also retains the exact
`git status --porcelain --untracked-files=all` output (status codes and paths
only, never file bytes) at harness start and end, with parsed status/path
records, so a dirty boolean can no longer hide which paths moved.
`MORI_EVIDENCE_REVISION` is retained as `asserted_revision` and still selects
the historical `head`; the start/end scope separately records real
`git rev-parse HEAD` as `observed_head`, so a pin cannot make the comparison
vacuous. Files under harness-written output paths (runs/, wrappers/, mutants/,
evidence.json, the fixture root) are excluded from `status_changed`, but never
a path that is itself a resolved input. The driving script is hashed at import
and after the last run, so a post-import edit is visible even when porcelain
text is unchanged. `MORI_EVIDENCE_DIRTY` may still assert the historical dirty
boolean; evidence labels `dirty_source` (`env:MORI_EVIDENCE_DIRTY` or
`porcelain`) and retains the captured `dirty_captured` so an env assertion is
never presented as an observed status. Historical receipts cannot be
reconstructed: a past `dirty=true` was never accompanied by a path list, and
the worktree that produced it is gone, so only future runs carry the new
scope. Synthetic canary text is redacted before anything is written.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SCHEMA = "mori-round13-regressions-v2"
REPO = Path(__file__).resolve().parent.parent
DEFAULT_CENSUS = REPO / "tools/mori-census.sh"
DEFAULT_ORACLE = REPO / "tools/mori-silence-cases.sh"
DEFAULT_FROZEN = REPO / ".ufo/waves/round-13/frozen"
DEFAULT_SHONEN = REPO / "SHONEN.md"
REGISTRY_FILE = REPO / "SKILL.md"
GATE_REGISTRY_NAME = "r13 regressions"
GATE_ENTRY = "python3 tools/mori-round13-regressions.py --output <dir>"

# Committed expected values for the default historical frozen snapshot. They
# are constants in this file, not read from `.ufo/waves/round-13/frozen/inputs.json`,
# so editing a frozen file together with its sibling manifest still reads
# snapshot_tampered. `inputs.json` remains a secondary consistency check.
FROZEN_PINS = {
    "mori-census.sh":
        "3da5b098dc23aeb3e1c31ce82664b24a22c2847a168308a755525593881b3164",
    "mori-silence-cases.sh":
        "448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5",
    "inputs.json":
        "d91690dc0417aecd9bffd507b53cd4e2a32fc6614753c82ccbc0c5b590cfdc3f",
}
FROZEN_BASE_COMMIT = "6531ac6029e200a6392bb76673b6a17d3c895c96"

NOW_EPOCH = 1700000000
LAUNCH_EPOCH = 1699998000
LANE = "kagi"
ROUND = "7"
HISTORY_SIBLINGS = 12000

KERNEL_ID = "fe6faa94e7774663a0da52717891d8ef"
OOMD_ID = "d989611b15e44c9dbf31e3c81256e4ed"
COREDUMP_ID = "fc2e22bc6ee647b6b90729ab34a250b1"
UNIT_FAILURE_ID = "d9b373ed55a64feb8242e02dbe79a49c"
UNIT_SIGKILL_ID = "98e322203f7a4ed290d09fe03c09fe15"
JOURNAL_BOOT = "0123456789abcdef0123456789abcdef"
CANARY = "R13-SYNTHETIC-JOURNAL-MESSAGE-CANARY"

# Restored round-14 stable finding ids and severity map (L1 final ruling).
# The generic unit failure id is historical INFO (pre-cutover
# probe_journal:904-908); only the OOM alarm and the generic SIGKILL record flip
# the roll. ONE global OOM_KILL_JOURNAL line carries separate counters that are
# never summed; routing findings keep per-scope ids (duplicate ids would break
# --drift line pairing), and missing/ambiguous subject metadata is
# UNIT_FAILURE_UNATTRIBUTED_JOURNAL, never fleet or non-fleet.
OOM_FINDING = "OOM_KILL_JOURNAL"
OOM_COUNTERS = (
    "user_notice",
    "system_notice",
    "user_unit_oom",
    "system_unit_oom",
    "user_unit_oom_result_unknown",
    "system_unit_oom_result_unknown",
)
UNIT_FLEET_FINDING = "UNIT_FAILURE_JOURNAL"
UNIT_FLEET_FINDING_SYSTEM = "UNIT_FAILURE_JOURNAL_SYSTEM"
UNIT_OUT_OF_SCOPE_FINDING = "UNIT_FAILURE_OUT_OF_SCOPE"
UNIT_OUT_OF_SCOPE_FINDING_SYSTEM = "UNIT_FAILURE_OUT_OF_SCOPE_SYSTEM"
UNIT_UNATTRIBUTED_FINDING = "UNIT_FAILURE_UNATTRIBUTED_JOURNAL"
KILL_SIGNAL_FINDING = "KILL_SIGNAL_JOURNAL"
KILL_SIGNAL_FINDING_SYSTEM = "KILL_SIGNAL_JOURNAL_SYSTEM"
EXPECTED_SEVERITY = {
    OOM_FINDING: "crit",
    UNIT_FLEET_FINDING: "info",
    UNIT_FLEET_FINDING_SYSTEM: "info",
    UNIT_OUT_OF_SCOPE_FINDING: "info",
    UNIT_OUT_OF_SCOPE_FINDING_SYSTEM: "info",
    UNIT_UNATTRIBUTED_FINDING: "info",
    KILL_SIGNAL_FINDING: "warn",
    KILL_SIGNAL_FINDING_SYSTEM: "info",
}
# Historical fleet predicate restored over the structured SUBJECT unit
# (UNIT/USER_UNIT). _SYSTEMD_UNIT/_SYSTEMD_USER_UNIT describe the emitter and
# are never consulted.
FLEET_SUBJECT_RE = re.compile(
    r"shokunin|ufo-sighting|tmux-spawn|the-tick|fleet", re.IGNORECASE
)

# The six scoped counters are preserved exactly. `kind` keys the synthetic
# record builders; `token` is the SURFACE token the probe must emit.
C1_SURFACE_TOKENS = (
    ("kernel_oom_notice", "kernel"),
    ("oomd_notice", "oomd"),
    ("coredump_notice", "coredump"),
    ("segfault_signal11", "segfault"),
    ("unit_sigkill_record", "sigkill"),
    ("unit_failure_record", "unit_failure"),
)
C1_CLASS_KINDS = tuple(kind for _, kind in C1_SURFACE_TOKENS)
C1_PARTITION_TOKENS = (
    "unit_fleet", "unit_nonfleet", "unit_missing", "unit_ambiguous",
    "unit_malformed", "unit_oom", "unit_oom_fleet", "unit_oom_nonfleet",
    "unit_oom_subject_unknown", "unit_oom_result_unknown", "unit_signal",
)
C1_SYSTEM_COUNTS = {
    "kernel": 2,
    "oomd": 1,
    "coredump": 3,
    "segfault": 3,  # the three coredump records carry COREDUMP_SIGNAL=11
    "sigkill": 0,
    "unit_failure": 0,
}
C1_USER_COUNTS = {
    "kernel": 3,
    "oomd": 0,
    "coredump": 1,
    "segfault": 1,  # the single user coredump record carries COREDUMP_SIGNAL=11
    "sigkill": 0,
    "unit_failure": 0,
}
C1_NOTICE_ONLY_COUNTS = {
    "kernel": 0,
    "oomd": 1,
    "coredump": 2,
    "segfault": 2,
    "sigkill": 0,
    "unit_failure": 0,
}
C1_EMPTY_COUNTS = {kind: 0 for kind in C1_CLASS_KINDS}

VERDICT_RE = re.compile(
    r"^MORI_CENSUS: (CLEAN|DRIFT) "
    r"\(findings=[0-9]+ drift=[0-9]+ unavailable=[0-9]+ surfaces=[0-9]+\)$"
)
SURFACE_SCOPED_RE = re.compile(
    r"^SURFACE journal\.(user|system): (\S+) \((.*)\)\s*$", re.M
)
LANE_ROW_RE = re.compile(r"^SURFACE lane\.(\w+): (\S+) \((.*)\)\s*$", re.M)
FINDING_RE = re.compile(r"^FINDING (\w+) severity=(\w+) obs=(.*)$", re.M)
TOKEN_RE = re.compile(r"([A-Za-z0-9_.:-]+)=([^\s;]*)")
SUMMARY_RE = re.compile(r"^MORI_SILENCE_CASES: matched=(\d+) total=(\d+)\s*$", re.M)
PASS_CASE_RE = re.compile(r"^PASS (\S+)(?: \(state=(\S+) )?", re.M)

# The 28 registry ids, committed here as an independent expected contract (the
# runner does not read the oracle source). The selective wrappers must encode
# these exact PASS sets rather than a blanket tally.
ALL_CASE_IDS = (
    "silent-open",
    "completed-not-open",
    "young-under-gate",
    "young-age-equals-gate",
    "young-future-launch",
    "nolane-launch-not-open",
    "ledger-missing-not-silent",
    "repo-missing-unavailable",
    "unreadable-git-unavailable",
    "same-round-relaunch-silent",
    "legacy-steer-open-silent",
    "subject-postlaunch-progressing",
    "subject-hidden-behind-sibling-head",
    "sibling-clean-checkout-weak",
    "author-sibling-committer-subject-weak",
    "author-subject-committer-sibling-progress",
    "substring-name-mismatch-weak",
    "substring-email-mismatch-weak",
    "dirty-same-path-as-sibling-progress",
    "untracked-recent-progress",
    "committed-report-closes",
    "old-report-before-relaunch-silent",
    "report-eq-launch-no-close",
    "report-future-no-close",
    "untracked-report-progress",
    "main-repo-noise-silent",
    "readonly-no-mutation",
    "shape-invariance",
)
SILENT_IDS = frozenset((
    "silent-open",
    "same-round-relaunch-silent",
    "legacy-steer-open-silent",
    "old-report-before-relaunch-silent",
    "report-eq-launch-no-close",
    "main-repo-noise-silent",
))
AUTO_ID = "report-future-no-close"
MESSAGE_KEY_RE = re.compile(r'"MESSAGE"\s*:')
MESSAGE_EQ_RE = re.compile(r"(?<!_)MESSAGE=")

# Canonical promotion seed at HEAD (unindented markdown). The protocol block
# indentation is presentation, not file bytes: round-12 M3 / round-13 parent
# correction. A known earlier working-tree copy was indented (sha ac3a436e…);
# that was a raw-block transcription mismatch, not the canonical seed.
CANONICAL_SHONEN = (
    "# mori-shokunin — Promotion checklist\n"
    "\n"
    "Promotion to shokunin requires all of:\n"
    "\n"
    "- [ ] SKILL.md contains real decision tables, error patterns, checklists, cited sources\n"
    "- [ ] At least one end-to-end domain task executed and logged in LOG.md\n"
    "- [ ] Instructions executable by an agent without oral context\n"
    "- [ ] No cross-domain bleed (PROVINCE.md still accurate)\n"
)
CANONICAL_SHONEN_SHA256 = "508d5b46c1d661ec6f0c279dc2fd44af5d0cab4224231a10fdc8ab6e4bf70009"

# Status vocabulary. Only PASS is a new-contract pass; baseline statuses keep
# the distinction between "observed as expected pre-fix" and "passes today".
PASS = "pass"
FAIL = "fail"
EXPECTED_DEFECT = "expected-defect"
BASELINE_OK = "baseline-ok"
BASELINE_REJECTED = "baseline-rejected"
BASELINE_CONTROL = "baseline-control"
BASELINE_DEVIATION = "baseline-deviation"
BASELINE_MISMATCH = "baseline-mismatch"
UNAVAILABLE = "unavailable"
MUTATION_RED = "mutation-red"
MUTATION_MISS = "mutation-not-reproduced"
MUTATION_UNAVAILABLE = "mutation-unavailable"

STRICT_SUCCESS = {PASS}
BASELINE_SUCCESS = {
    EXPECTED_DEFECT,
    BASELINE_OK,
    BASELINE_REJECTED,
    BASELINE_CONTROL,
}
MUTATION_SUCCESS = {PASS, MUTATION_RED}

# Committed self-invocation cases (PROTOCOL §Gate standard): each runs the real
# gate as a subprocess over an isolated tree and asserts the exit code plus a
# stable finding id. Expected values are literals here, never derived from the
# gate's own functions or from the recomputation.
SELFTEST_CASES = (
    # (case id, expected rc, required finding ids, forbidden finding ids)
    ("isolated-stub-target-red", 1, ("R13_C1_SYSTEM_NOTICE_COUNTS",), ()),
    ("isolated-frozen-manifest-tamper", 2, ("R13_SNAPSHOT_TAMPERED",), ()),
)


# F02 mutation: the pre-fix verdict read, verbatim in behavior (audit-r11
# Appendix C, frozen oracle): a `MORI_CENSUS:` line starting any output was
# treated as a verdict. Used only to build an isolated mutant; never installed.
PRE_FIX_VERDICT_GRADE = """verdict_grade() { # R13 mutation: pre-fix prefix-presence semantics
  local out=$1
  local rc=$2
  if grep -q '^MORI_CENSUS:' <<<"$out"; then
    printf 'ok'
  else
    printf 'missing'
  fi
}"""


class SetupError(RuntimeError):
    pass


class SnapshotTampered(SetupError):
    """A target named under a frozen snapshot failed its inputs.json digest."""


def verify_inputs_file(inputs_path: Path):
    """Verify every {filename: digest} entry in one inputs.json.

    Read-only; returns {name: path}. Raises SnapshotTampered on any missing or
    mismatched file so a tampered snapshot can never produce a behavior run.
    """
    try:
        inputs = json.loads(inputs_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SnapshotTampered(
            "inputs_unreadable file=%s error=%s" % (inputs_path, exc)
        )
    verified = {}
    for name, expected in sorted(inputs.get("sha256", {}).items()):
        path = inputs_path.parent / name
        if not path.is_file():
            raise SnapshotTampered(
                "snapshot_missing file=%s inputs=%s base_commit=%s"
                % (path, inputs_path, inputs.get("base_commit", "unknown"))
            )
        actual = sha256_file(path)
        if actual != expected:
            raise SnapshotTampered(
                "snapshot_digest_mismatch file=%s expected=%s actual=%s "
                "inputs=%s base_commit=%s"
                % (path.name, expected, actual, inputs_path,
                   inputs.get("base_commit", "unknown"))
            )
        verified[name] = path
    return verified


def verify_frozen_pins(frozen_dir: Path) -> dict:
    """Verify the default historical snapshot against committed constants.

    This is the independent pin PROTOCOL §Gate standard requires: the expected
    digests live in this file, not only in the sibling `inputs.json` that a
    coordinated edit could rewrite with the snapshot. The manifest is checked
    as a secondary consistency layer (shape, base commit, per-file digests).
    """
    for name, expected in sorted(FROZEN_PINS.items()):
        path = frozen_dir / name
        if not path.is_file():
            raise SnapshotTampered(
                "snapshot_missing file=%s pinned=%s dir=%s"
                % (path, expected, frozen_dir)
            )
        actual = sha256_file(path)
        if actual != expected:
            raise SnapshotTampered(
                "snapshot_pin_mismatch file=%s expected=%s actual=%s dir=%s"
                % (name, expected, actual, frozen_dir)
            )
    inputs_path = frozen_dir / "inputs.json"
    try:
        inputs = json.loads(inputs_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SnapshotTampered(
            "inputs_unreadable file=%s error=%s" % (inputs_path, exc)
        )
    declared = inputs.get("sha256")
    targets = {"mori-census.sh", "mori-silence-cases.sh"}
    if not isinstance(declared, dict) or set(declared) != targets:
        raise SnapshotTampered(
            "pinned_inputs_shape file=%s keys=%s expected=%s"
            % (inputs_path, sorted(declared or {}), sorted(targets))
        )
    if inputs.get("base_commit") != FROZEN_BASE_COMMIT:
        raise SnapshotTampered(
            "pinned_base_mismatch file=%s expected=%s actual=%s"
            % (inputs_path, FROZEN_BASE_COMMIT, inputs.get("base_commit"))
        )
    for name in sorted(targets):
        if declared.get(name) != FROZEN_PINS[name]:
            raise SnapshotTampered(
                "pinned_manifest_mismatch file=%s expected=%s actual=%s"
                % (name, FROZEN_PINS[name], declared.get(name))
            )
    return {name: frozen_dir / name for name in sorted(targets)}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# Executing-gate digest captured at import, before CLI parsing or any run. A
# post-import edit then compares unequal instead of becoming a false start.
try:
    HARNESS_SHA_IMPORT = sha256_file(Path(__file__).resolve())
except OSError:
    HARNESS_SHA_IMPORT = None


def one_line(text, limit=240) -> str:
    text = " ".join(str(text).replace(CANARY, "<canary>").split())
    if len(text) > limit:
        text = text[: limit - 3] + "..."
    return text


def redact(text: str) -> str:
    return text.replace(CANARY, "<canary-redacted>")


def registry_row_status(text: str):
    """Pure matcher for this gate's registry row in SKILL.md text."""
    needles = (
        "mori-round13-regressions",
        "regressions-r13",
        "r13 regression",
        "round-13 regression",
        "round13 regression",
    )
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        lowered = line.lower()
        if any(needle in lowered for needle in needles):
            return "registered", one_line(line, 240)
    return "registration-missing", (
        "no SKILL.md Gates row names mori-round13-regressions.py / r13 regressions"
    )


def registry_status():
    """Truthful gate-registry status from this lane's own SKILL.md.

    A verdict-producing tool is a gate; this function never asserts
    "not-registered" as a permanent identity. It reports whether the committed
    registry row is present, missing, or unreadable, and returns the matched row
    for evidence.
    """
    try:
        text = REGISTRY_FILE.read_text(encoding="utf-8")
    except OSError as exc:
        return "registry-unreadable", "%s: %s" % (type(exc).__name__, exc)
    return registry_row_status(text)


def write_exec(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    path.chmod(0o755)


def json_dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


# ---------------------------------------------------------------------------
# revision provenance (evidence-only; the verdict never consumes it)
# ---------------------------------------------------------------------------


def porcelain_entry(line: str) -> dict:
    """Parse one porcelain v1 line into status/path fields (paths only)."""
    status = line[:2]
    rest = line[3:] if len(line) > 3 else ""

    def unquote(value):
        if len(value) >= 2 and value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        return value

    if " -> " in rest:
        orig, new = rest.rsplit(" -> ", 1)
        return {"status": status, "path": unquote(new),
                "orig_path": unquote(orig)}
    return {"status": status, "path": unquote(rest)}


def output_prefix(output: Path):
    """Posix prefix when --output lives inside REPO, else None."""
    try:
        rel = Path(output).resolve().relative_to(REPO.resolve())
    except (OSError, ValueError):
        return None
    prefix = rel.as_posix()
    return None if prefix in ("", ".") else prefix


def harness_owned_paths(output: Path, fixture_root=None, inputs=()):
    """Repo-relative paths this harness writes itself, never a measured input.

    A candidate is dropped when a resolved input lives at or below it, so a
    census, oracle, shonen or frozen file placed under --output remains in the
    comparison. The whole --output tree is never excluded.
    """
    prefix = output_prefix(output)
    if prefix is None:
        return []
    candidates = [
        prefix + "/runs",
        prefix + "/wrappers",
        prefix + "/mutants",
        prefix + "/evidence.json",
        prefix + "/evidence.json.tmp",
    ]
    if fixture_root is not None:
        try:
            rel = Path(fixture_root).resolve().relative_to(REPO.resolve())
        except (OSError, ValueError):
            rel = None
        if rel is not None:
            candidates.append(rel.as_posix())
    resolved = [str(Path(p).resolve()) for p in inputs if p]
    owned = []
    for candidate in candidates:
        candidate_abs = str((REPO / candidate).resolve())
        if any(path == candidate_abs or path.startswith(candidate_abs + os.sep)
               for path in resolved):
            continue
        owned.append(candidate)
    return owned


def _is_owned(path: str, owned) -> bool:
    for prefix in owned:
        if path == prefix or path.startswith(prefix + "/"):
            return True
    return False


def scope_porcelain(scope, owned):
    """Return (lines|None, excluded) with only harness-owned output removed."""
    if not scope or scope.get("porcelain") is None:
        return None, 0
    kept, excluded = [], 0
    for line in scope["porcelain"]:
        if _is_owned(porcelain_entry(line)["path"], owned):
            excluded += 1
            continue
        kept.append(line)
    return kept, excluded


def scope_facets(start, end, owned, output: Path) -> dict:
    """Per-facet start/end observations; no universal `moving:false`.

    `status_changed` compares porcelain with only harness-written entries
    removed. It cannot prove file contents were stationary (an already-dirty
    path keeps the same line); the evidence labels that limit instead of
    claiming movement was absent.
    """
    start = start or {}
    end = end or {}
    head_changed = None
    if start.get("head") and end.get("head"):
        head_changed = start["head"] != end["head"]
    start_scope, start_excluded = scope_porcelain(start, owned)
    end_scope, end_excluded = scope_porcelain(end, owned)
    status_changed = None
    added, removed = [], []
    if start_scope is not None and end_scope is not None:
        status_changed = start_scope != end_scope
        if status_changed:
            added = sorted(set(end_scope) - set(start_scope))
            removed = sorted(set(start_scope) - set(end_scope))
    return {
        "head_changed": head_changed,
        "status_changed": status_changed,
        "porcelain_added": added,
        "porcelain_removed": removed,
        "dirty_excluding_harness_output": {
            "start": None if start_scope is None else bool(start_scope),
            "end": None if end_scope is None else bool(end_scope),
        },
        "output_scope": {
            "path": str(Path(output).resolve()),
            "excluded_prefixes": list(owned),
            "excluded_entries": {"start": start_excluded,
                                 "end": end_excluded},
        },
        "not_measured": "content edits inside already-dirty tracked paths "
                        "other than the driving script; no other file bytes "
                        "are read",
    }


# ---------------------------------------------------------------------------
# final-roll grammar (mirrors tools/mori-silence-cases.sh verdict_grade)
# ---------------------------------------------------------------------------


def verdict_roll(out: str, rc: int):
    """Return (word|None, reason, line). reason in ok/missing/duplicate/malformed/inconsistent."""
    lines = [ln for ln in out.splitlines() if ln.startswith("MORI_CENSUS:")]
    if not lines:
        return None, "missing", ""
    if len(lines) > 1:
        return None, "duplicate (%d lines)" % len(lines), lines[0]
    line = lines[0]
    if not VERDICT_RE.match(line):
        return None, "malformed", line
    word = VERDICT_RE.match(line).group(1)
    if (word, rc) not in (("CLEAN", 0), ("DRIFT", 1)):
        return word, "inconsistent (word=%s rc=%s)" % (word, rc), line
    return word, "ok", line


def surface_rows(out: str):
    """Map scope -> (state, tokens) from the two `SURFACE journal.<scope>` rows."""
    rows = {}
    for m in SURFACE_SCOPED_RE.finditer(out):
        rows[m.group(1)] = (m.group(2), dict(TOKEN_RE.findall(m.group(3))))
    return rows


def findings(out: str):
    rows = []
    for m in FINDING_RE.finditer(out):
        fid, sev, rest = m.group(1), m.group(2), m.group(3)
        rows.append((fid, sev, dict(TOKEN_RE.findall(rest)), rest))
    return rows


def lane_row(out: str, lane: str = LANE):
    m = LANE_ROW_RE.search(out)
    if not m or m.group(1) != lane:
        return None, {}
    return m.group(2), dict(TOKEN_RE.findall(m.group(3)))


def pass_cases(out: str):
    """id -> observed state; count_check PASS lines (no state=) map to ''."""
    return {m.group(1): (m.group(2) or "") for m in PASS_CASE_RE.finditer(out)}


def count_value(tokens: dict) -> int:
    try:
        return int(tokens.get("count", "0") or 0)
    except (TypeError, ValueError):
        return 0


def _token_int(tokens, name: str):
    """Integer value of a named token, or None when absent/non-numeric.

    Unlike count_value this never defaults to 0: an `unavailable:<reason>` or
    absent counter must not be readable as a healthy zero.
    """
    if not tokens:
        return None
    value = tokens.get(name)
    if value is None or not re.fullmatch(r"[0-9]+", value):
        return None
    return int(value)


def oracle_summary(out: str):
    matches = SUMMARY_RE.findall(out)
    if not matches:
        return None
    matched, total = matches[-1]
    return int(matched), int(total)


VERDICT_FAIL_RE = re.compile(r"MORI_CENSUS verdict ([a-z-]+)")


def fail_reasons(out: str):
    """Reason heads from the oracle's verdict-contract FAIL lines.

    Known heads: missing, duplicate, malformed, inconsistent. OracleFix V1/V3
    may add tally/position heads; the harness requires a verdict-contract FAIL
    without hardcoding an unconfirmed word for those wrappers.
    """
    reasons = set()
    for line in out.splitlines():
        if not line.startswith("FAIL "):
            continue
        m = VERDICT_FAIL_RE.search(line)
        if m:
            reasons.add(m.group(1))
    return reasons


# ---------------------------------------------------------------------------
# synthetic fixtures
# ---------------------------------------------------------------------------


def journal_record(message_id: str, **fields) -> dict:
    """One synthetic structured journal record (boot-valid).

    MESSAGE carries the canary so leak mode can force it: honor mode projects
    it out because no query asks for MESSAGE, while a parser that echoes raw
    records exposes it.
    """
    rec = {
        "_BOOT_ID": JOURNAL_BOOT,
        "MESSAGE_ID": message_id,
        "MESSAGE": CANARY,
    }
    rec.update({key: str(value) for key, value in fields.items()})
    return rec


def notice_records(counts: dict) -> list:
    """Record pool for the catalog notice classes plus the signal-11 subset.

    The coredump query counts every COREDUMP_ID record; the segfault query
    counts only those carrying COREDUMP_SIGNAL=11. The first `segfault` records
    get the signal, so `coredump` >= `segfault` holds for every fixture.
    """
    pool = [journal_record(KERNEL_ID) for _ in range(int(counts.get("kernel", 0)))]
    pool += [journal_record(OOMD_ID) for _ in range(int(counts.get("oomd", 0)))]
    core = int(counts.get("coredump", 0))
    seg = int(counts.get("segfault", 0))
    if seg > core:
        raise SetupError("fixture coredump=%d < segfault=%d" % (core, seg))
    for i in range(core):
        extra = {"COREDUMP_SIGNAL": "11"} if i < seg else {}
        pool.append(journal_record(COREDUMP_ID, **extra))
    return pool


def unit_failure_records(subjects, result: str = "exit-code") -> list:
    """Unit-failure records; each subject is None or (field, unit-name).

    `result=None` omits UNIT_RESULT, the result-unknown fixture shape.
    """
    pool = []
    for subject in subjects:
        extra = {} if result is None else {"UNIT_RESULT": result}
        if subject is not None:
            field, name = subject
            extra[field] = name
        pool.append(journal_record(UNIT_FAILURE_ID, **extra))
    return pool


def sigkill_records(count: int) -> list:
    return [
        journal_record(UNIT_SIGKILL_ID, EXIT_CODE="killed", EXIT_STATUS="9")
        for _ in range(int(count))
    ]


def journal_stub_body(system_records, user_records, message_mode: str) -> str:
    """Synthetic journalctl with exact field matching and field projection.

    The stub is a tiny journalctl: `FIELD=value` argv words are ANDed across
    fields and ORed within one field, `-o json`/`--output=json` selects JSON,
    and `--output-fields` projects exactly those keys (unless leak mode forces
    MESSAGE). A query that does not match a fixture record yields an empty
    stream at rc 0, so a fixed answer cannot masquerade as a valid answer.
    Text mode never carries a class word: only the structured path can observe
    this fixture, which is the C1 point.

    Deliberate limits (documented, not defects): the projection is STRICTER
    than real journalctl (real `-o json` always includes `__CURSOR`,
    timestamps and `_BOOT_ID`; here only requested fields appear), so a missing
    core field can cause a false red, never a false green. Values are joined by
    0x1f and read line-by-line, and only backslash/quote are JSON-escaped, so a
    newline or control-character unit-name injection cannot be represented here;
    that injection belongs in the census selftest (or the r14 gate), not in this
    structured fixture.
    """

    def encode(records):
        return "\n".join(
            "\x1f".join("%s=%s" % (key, val) for key, val in sorted(rec.items()))
            for rec in records
        )

    template = r"""#!/usr/bin/env bash
# Synthetic structured journal for the mori round-13 gate; never opens the
# host journal. Records are FIELD=value pairs joined by 0x1f.
mode='@MODE@'
json=0; scope=system; fields=''
declare -a fk=() fv=()
declare -A VALS=()
declare -a PAIRS=()
for a in "$@"; do
  case "$a" in
    --user) scope=user ;;
    --system) scope=system ;;
    --output-fields=*) fields=${a#--output-fields=} ;;
    -o|--output=json|json) json=1 ;;
    [A-Z_]*=*)
      fk+=("${a%%=*}"); fv+=("${a#*=}") ;;
  esac
done
show_message=1
if [ "$mode" = honor ] && [ -n "$fields" ]; then
  case ",$fields," in
    *,MESSAGE,*) ;;
    *) show_message=0 ;;
  esac
fi
if [ "$json" != 1 ]; then
  # Legacy text mode: a header line only. No class words, no MESSAGE text.
  if [ "$scope" = system ]; then
    printf '+-- Journal begins at 2026-10-14, ends at 2026-10-19. --+\n'
  fi
  exit 0
fi
if [ "$scope" = user ]; then
  pool=$(cat <<'R13POOL'
@USER_POOL@
R13POOL
)
else
  pool=$(cat <<'R13POOL'
@SYSTEM_POOL@
R13POOL
)
fi
record_values() { # <line> -> fill VALS
  local line=$1 pair
  VALS=()
  IFS=$'\x1f' read -r -a PAIRS <<< "$line"
  for pair in "${PAIRS[@]}"; do
    VALS["${pair%%=*}"]="${pair#*=}"
  done
}
matches() { # <line>; AND across fields, OR within repeated field filters
  local line=$1 i key val
  local -A need=() hit=()
  record_values "$line"
  for ((i=0; i<${#fk[@]}; i++)); do
    key=${fk[i]}; val=${fv[i]}
    [ "${VALS[$key]+x}" ] || return 1
    need[$key]=1
    if [ "${VALS[$key]}" = "$val" ]; then hit[$key]=1; fi
  done
  for key in "${!need[@]}"; do
    [ "${hit[$key]:-0}" = 1 ] || return 1
  done
  return 0
}
emit_record() { # <line>
  local line=$1 key val pair sep=''
  local -a keys=()
  record_values "$line"
  mapfile -t keys < <(printf '%s\n' "${!VALS[@]}" | LC_ALL=C sort)
  printf '{'
  for key in "${keys[@]}"; do
    if [ "$key" = MESSAGE ]; then
      [ "$show_message" = 1 ] || continue
    elif [ -n "$fields" ]; then
      case ",$fields," in *,"$key",*) ;; *) continue ;; esac
    fi
    val=${VALS[$key]}
    val=${val//\\/\\\\}
    val=${val//\"/\\\"}
    printf '%s"%s":"%s"' "$sep" "$key" "$val"
    sep=','
  done
  printf '}\n'
}
while IFS= read -r line; do
  [ -n "$line" ] || continue
  if matches "$line"; then emit_record "$line"; fi
done <<< "$pool"
exit 0
"""
    return (
        template.replace("@MODE@", message_mode)
        .replace("@SYSTEM_POOL@", encode(system_records))
        .replace("@USER_POOL@", encode(user_records))
    )


def git_stub_body(subject: bool, siblings: int = HISTORY_SIBLINGS) -> str:
    """Appendix-B git stub: one optional exact subject line, then siblings."""
    subject_line = (
        "  printf '1699999000 kagi-shokunin <kagi@shokunin.local>\\n'\n"
        if subject
        else ""
    )
    return """#!/usr/bin/env bash
# Synthetic git (audit-r11 Appendix B): answers revision probes and a
# @N@-sibling log; never touches a real repository.
for a in "$@"; do
  case "$a" in
    rev-parse) printf '.git\\n'; exit 0 ;;
    ls-files) exit 0 ;;
    cat-file) exit 1 ;;
    log)
@SUBJECT@      for ((i=0; i<@N@; i++)); do
        printf '1699999000 aggregator-shokunin <aggregator@shokunin.local>\\n'
      done
      exit 0
      ;;
  esac
done
exit 2
""".replace("@SUBJECT@", subject_line).replace("@N@", str(siblings))


QUIET_STUBS = {
    "pgrep": "#!/usr/bin/env bash\nprintf '123 bash /path/shokunin-watchdog.sh\\n'\n",
    "tmux": "#!/usr/bin/env bash\nexit 1\n",
    "df": (
        "#!/usr/bin/env bash\n"
        "printf 'Filesystem 1024-blocks Used Available Capacity Mounted on\\n"
        "/dev/fake0 1000000 10000 990000 1%% /fake\\n'\n"
    ),
}


def build_common(base: Path) -> None:
    root = base / "root"
    ufo = root / ".ufo"
    for path in (
        ufo / "state",
        ufo / "waves",
        root / ("%s-shokunin" % LANE) / ".git",
        base / "home",
        base / "cg",
        base / "bin",
        base / "disk-target",
    ):
        path.mkdir(parents=True, exist_ok=True)
    log = ufo / "watchdog.log"
    log.write_text("TIMESTAMP launch %s round=%s ts=%d\n" % (LANE, ROUND, LAUNCH_EPOCH))
    os.utime(log, (NOW_EPOCH, NOW_EPOCH))
    (ufo / "state" / ("%s.round" % LANE)).write_text(ROUND + "\n")
    (base / "cg" / "memory.events").write_text(
        "low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\n"
    )
    (base / "cg" / "memory.current").write_text("100\n")
    (base / "cg" / "memory.max").write_text("max\n")
    (base / "cg" / "memory.pressure").write_text(
        "some avg10=0.00 avg60=0.00 avg300=0.00 total=100\n"
        "full avg10=0.00 avg60=0.00 avg300=0.00 total=50\n"
    )
    (base / "cg" / "memory.peak").write_text("100\n")
    (base / "meminfo").write_text("MemTotal: 100000 kB\nMemAvailable: 90000 kB\n")
    (base / "uptime").write_text("1000.00 1.00\n")
    (base / "diskstats").write_text("8 0 fake0 0 0 0 0 0 0 20000 0\n")
    for name, body in QUIET_STUBS.items():
        write_exec(base / "bin" / name, body)


def census_env(base: Path) -> dict:
    root = base / "root"
    ufo = root / ".ufo"
    return {
        "PATH": "%s:/usr/bin:/bin" % (base / "bin"),
        "HOME": str(base / "home"),
        "TZ": "UTC",
        "LC_ALL": "C",
        "LANG": "C",
        "MORI_SHOKUNIN_ROOT": str(root),
        "MORI_UFO_DIR": str(ufo),
        "MORI_WATCHDOG_LOG": str(ufo / "watchdog.log"),
        "MORI_STATE_DIR": str(ufo / "state"),
        "MORI_WAVES_DIR": str(ufo / "waves"),
        "MORI_TIMELINE_FILE": str(ufo / "watchdog.log"),
        "MORI_CGROUP_EVENTS": str(base / "cg" / "memory.events"),
        "MORI_CGROUP_SERVICE_EVENTS": str(base / "cg" / "memory.events"),
        "MORI_CGROUP_LOCAL_EVENTS": str(base / "cg" / "memory.events"),
        "MORI_CGROUP_CURRENT": str(base / "cg" / "memory.current"),
        "MORI_CGROUP_MAX": str(base / "cg" / "memory.max"),
        "MORI_CGROUP_PRESSURE": str(base / "cg" / "memory.pressure"),
        "MORI_CGROUP_PEAK": str(base / "cg" / "memory.peak"),
        "MORI_MEMINFO": str(base / "meminfo"),
        "MORI_UPTIME": str(base / "uptime"),
        "MORI_DISKSTATS": str(base / "diskstats"),
        "MORI_DF_BIN": str(base / "bin" / "df"),
        "MORI_PGREP_BIN": str(base / "bin" / "pgrep"),
        "MORI_JOURNALCTL_BIN": str(base / "bin" / "journalctl"),
        "MORI_TMUX_BIN": str(base / "bin" / "tmux"),
        "MORI_GIT_BIN": str(base / "bin" / "git"),
        "MORI_DISK_TARGETS": str(base / "disk-target"),
        "MORI_RUN_NONCE": "1313",
        "MORI_BOOT_ID": JOURNAL_BOOT,
        "MORI_ROSTER_LANES": LANE,
        "MORI_NOW_EPOCH": str(NOW_EPOCH),
        "MORI_WATCHDOG_STALE_S": "900",
        "MORI_WAVE_UNSETTLED_S": "7200",
        "MORI_DISK_WARN_PCT": "85",
        "MORI_DISK_CRIT_PCT": "95",
        "MORI_LANE_SILENCE_S": "900",
    }


def build_history_fixture(base: Path, subject: bool) -> None:
    build_common(base)
    write_exec(base / "bin" / "git", git_stub_body(subject, HISTORY_SIBLINGS))
    write_exec(base / "bin" / "journalctl", journal_stub_body([], [], "honor"))


def build_journal_fixture(base: Path, message_mode: str,
                          system_records=None, user_records=None) -> None:
    build_common(base)
    write_exec(base / "bin" / "git", git_stub_body(True, 0))
    write_exec(
        base / "bin" / "journalctl",
        journal_stub_body(system_records or [], user_records or [], message_mode),
    )


# ---------------------------------------------------------------------------
# harness
# ---------------------------------------------------------------------------


class Harness:
    def __init__(self, args):
        self.args = args
        self.repo = REPO
        self.output = Path(args.output).resolve()
        self.runs_dir = self.output / "runs"
        self.wrappers_dir = self.output / "wrappers"
        self.mutants_dir = self.output / "mutants"
        self.runs = []
        self.claims = []
        self.fixture_root = None
        self.frozen = {}
        self.frozen_pins = "not-supplied"
        self.inputs_sha256 = None
        self.revision = None
        self.dirty = None
        self.dirty_source = None
        self.dirty_captured = None
        self.revision_scope_start = None
        self.revision_scope_end = None
        self.harness_sha_start = None
        self.harness_sha_end = None
        self.harness_changed = None
        self.census = None
        self.oracle = None

    # -- setup -------------------------------------------------------------

    def resolve_targets(self):
        """Resolve the two target paths without reading or running them."""
        frozen_dir = Path(self.args.frozen_dir).resolve()
        if self.args.baseline:
            census = self.args.census or (frozen_dir / "mori-census.sh")
            oracle = self.args.oracle or (frozen_dir / "mori-silence-cases.sh")
        else:
            census = self.args.census or DEFAULT_CENSUS
            oracle = self.args.oracle or DEFAULT_ORACLE
        return Path(census).resolve(), Path(oracle).resolve()

    def snapshot_verify(self, census: Path, oracle: Path) -> None:
        """Digest-check every frozen input BEFORE any behavior or output write.

        Two entry points are covered: the sibling inputs.json next to an
        explicitly named target (e.g. --census frozen/mori-census.sh), and the
        --frozen-dir inputs.json used by --baseline and by mutation sources.

        For the DEFAULT historical frozen directory the digests come from the
        committed FROZEN_PINS constants, so editing a frozen file together with
        its sibling manifest still raises SnapshotTampered. A custom
        --frozen-dir cannot be pinned ahead of time; it is verified against its
        own manifest and disclosed as `unpinned (custom frozen dir)`.
        """
        frozen_map = {}
        inputs_hash = None
        frozen_dir = Path(self.args.frozen_dir).resolve()
        default_frozen = frozen_dir == DEFAULT_FROZEN.resolve()
        if default_frozen:
            frozen_map = verify_frozen_pins(frozen_dir)
            inputs_hash = sha256_file(frozen_dir / "inputs.json")
        else:
            inputs_path = frozen_dir / "inputs.json"
            if inputs_path.is_file():
                inputs_hash = sha256_file(inputs_path)
                frozen_map = verify_inputs_file(inputs_path)
        for path in (census, oracle):
            sibling = path.parent / "inputs.json"
            if sibling.is_file():
                if inputs_hash is None:
                    inputs_hash = sha256_file(sibling)
                verify_inputs_file(sibling)
        self.frozen = frozen_map
        self.inputs_sha256 = inputs_hash
        if default_frozen:
            self.frozen_pins = "verified"
        elif frozen_map:
            self.frozen_pins = "unpinned (custom frozen dir)"
        else:
            self.frozen_pins = "not-supplied"

    @staticmethod
    def revision_scope(captured="start"):
        """Capture real HEAD plus the exact porcelain scope (paths only).

        `GIT_OPTIONAL_LOCKS=0` and `core.fsmonitor=false` keep this probe from
        writing or consulting optional state. `MORI_EVIDENCE_REVISION` is
        recorded as an asserted revision only; the scope head is always real
        `git rev-parse HEAD`, so a pin cannot make start/end comparison
        vacuous. A capture failure is recorded, never raised here.
        """
        env = {
            "PATH": "/usr/bin:/bin",
            "HOME": os.environ.get("HOME", "/tmp"),
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_SYSTEM": "/dev/null",
            "GIT_OPTIONAL_LOCKS": "0",
        }

        def git(args):
            try:
                proc = subprocess.run(
                    ["git", "--no-optional-locks", "-C", str(REPO),
                     "-c", "core.fsmonitor=false"] + args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    env=env,
                    timeout=10,
                )
            except (OSError, subprocess.SubprocessError) as exc:
                return None, "unavailable:%s" % type(exc).__name__
            if proc.returncode != 0:
                return None, "unavailable:git-exit-%d" % proc.returncode
            return proc.stdout, "ok"

        out, state = git(["rev-parse", "HEAD"])
        if out is not None and out.strip():
            head, head_state = out.strip(), "ok:git-rev-parse-HEAD"
        else:
            head = None
            head_state = state if state != "ok" else "unavailable:empty"
        out, state = git(["status", "--porcelain", "--untracked-files=all"])
        porcelain = out.splitlines() if out is not None else None
        return {
            "captured": captured,
            "captured_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "repo": str(REPO),
            "head": head,
            "head_state": head_state,
            "asserted_revision": (
                os.environ.get("MORI_EVIDENCE_REVISION", "").strip() or None),
            "porcelain_source": "git --no-optional-locks -c core.fsmonitor=false "
                                "status --porcelain --untracked-files=all",
            "porcelain_state": state,
            "porcelain": porcelain,
            "paths": ([porcelain_entry(line) for line in porcelain]
                      if porcelain is not None else None),
            "porcelain_entries": len(porcelain) if porcelain is not None else None,
            "dirty": None if out is None else bool(out.strip()),
        }

    @staticmethod
    def revision_from_scope(scope):
        """Derive the historical (head, dirty) pair from one captured scope."""
        scope = scope or {}
        revision = scope.get("asserted_revision") or scope.get("head")
        if not revision:
            raise SetupError(
                "revision unavailable: git rev-parse failed and "
                "MORI_EVIDENCE_REVISION is unset (a verdict must name its "
                "revision; set the env or run inside the lane repository)"
            )
        dirty_env = os.environ.get("MORI_EVIDENCE_DIRTY", "").strip().lower()
        if dirty_env in ("true", "false"):
            dirty = dirty_env == "true"
        else:
            dirty = scope.get("dirty")
        return revision, dirty

    @staticmethod
    def dirty_source_label():
        """Name where the historical dirty boolean came from (CE7 label)."""
        if os.environ.get("MORI_EVIDENCE_DIRTY", "").strip().lower() in (
                "true", "false"):
            return "env:MORI_EVIDENCE_DIRTY"
        return "porcelain"

    @staticmethod
    def record_revision():
        """Name the measured revision; unavailable is could-not-evaluate.

        Contract preserved: returns (head, dirty) and raises when no revision
        is available. `MORI_EVIDENCE_REVISION` still pins the reported head,
        while revision_scope() separately records real `git rev-parse HEAD`
        for the start/end comparison. The dirty flag is recorded, never hidden.
        """
        return Harness.revision_from_scope(Harness.revision_scope("start"))

    def prepare(self) -> None:
        if not CANONICAL_SHONEN:
            raise SetupError("canonical SHONEN seed is empty")
        if sha256_bytes(CANONICAL_SHONEN.encode()) != CANONICAL_SHONEN_SHA256:
            raise SetupError("canonical SHONEN seed digest drifted from its constant")
        self.revision_scope_start = Harness.revision_scope("start")
        self.revision, self.dirty = Harness.revision_from_scope(
            self.revision_scope_start)
        self.dirty_source = Harness.dirty_source_label()
        self.dirty_captured = (self.revision_scope_start or {}).get("dirty")
        self.harness_sha_start = HARNESS_SHA_IMPORT
        census, oracle = self.resolve_targets()
        self.snapshot_verify(census, oracle)
        self.census, self.oracle = census, oracle
        for label, path in (("census", self.census), ("oracle", self.oracle)):
            if not path.is_file() or not os.access(path, os.R_OK):
                raise SetupError("%s not readable: %s" % (label, path))
        try:
            for path in (self.runs_dir, self.wrappers_dir, self.mutants_dir):
                path.mkdir(parents=True, exist_ok=True)
            self.fixture_root = Path(
                tempfile.mkdtemp(prefix="r13-fixtures-", dir=str(self.output))
            )
        except OSError as exc:
            raise SetupError("cannot create evidence tree under %s: %s"
                             % (self.output, exc))

    def cleanup(self) -> None:
        if self.fixture_root and not self.args.keep_fixtures:
            shutil.rmtree(self.fixture_root, ignore_errors=True)

    # -- run plumbing --------------------------------------------------------

    def run_process(self, run_id: str, argv, env, cwd=None, timeout=None) -> dict:
        timeout = timeout or self.args.timeout
        started = time.monotonic()
        timed_out = False
        error = None
        try:
            proc = subprocess.Popen(
                [str(x) for x in argv],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={str(k): str(v) for k, v in env.items()},
                cwd=str(cwd) if cwd else None,
                text=True,
                encoding="utf-8",
                errors="replace",
                start_new_session=True,
            )
        except OSError as exc:
            error = "%s: %s" % (type(exc).__name__, exc)
            stdout = stderr = ""
            rc = None
            proc = None
        if proc is not None:
            def kill_group(sig):
                try:
                    os.killpg(os.getpgid(proc.pid), sig)
                except (ProcessLookupError, PermissionError):
                    pass

            try:
                stdout, stderr = proc.communicate(timeout=timeout)
                rc = proc.returncode
            except subprocess.TimeoutExpired:
                timed_out = True
                # TERM lets the oracle's own EXIT trap clean its temp tree;
                # KILL after a short grace if it does not honor TERM.
                kill_group(signal.SIGTERM)
                try:
                    proc.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    kill_group(signal.SIGKILL)
                stdout, stderr = proc.communicate()
                rc = proc.returncode
            except BaseException:
                # Never orphan an isolated child on an interrupt or harness bug.
                kill_group(signal.SIGTERM)
                try:
                    proc.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    kill_group(signal.SIGKILL)
                proc.communicate()
                raise
        duration_ms = int((time.monotonic() - started) * 1000)
        canary_present = CANARY in (stdout or "") or CANARY in (stderr or "")
        safe_out = redact(stdout or "")
        safe_err = redact(stderr or "")
        out_path = self.runs_dir / (run_id + ".stdout")
        err_path = self.runs_dir / (run_id + ".stderr")
        out_path.write_text(safe_out, encoding="utf-8")
        err_path.write_text(safe_err, encoding="utf-8")
        record = {
            "id": run_id,
            "argv": [str(x) for x in argv],
            "cwd": str(cwd) if cwd else None,
            "rc": rc,
            "timed_out": timed_out,
            "canary_present": canary_present,
            "error": error,
            "duration_ms": duration_ms,
            "timeout_s": timeout,
            "stdout_path": str(out_path),
            "stderr_path": str(err_path),
            "stdout_sha256": sha256_bytes(safe_out.encode()),
            "stderr_sha256": sha256_bytes(safe_err.encode()),
            "stdout_bytes": len(safe_out.encode()),
            "stderr_bytes": len(safe_err.encode()),
            "env": {
                k: v
                for k, v in sorted(env.items())
                if k.startswith("MORI_") or k in ("PATH", "HOME", "TMPDIR")
            },
        }
        self.runs.append(record)
        rec = dict(record)
        rec["stdout"] = safe_out
        rec["stderr"] = safe_err
        return rec

    def fixture(self, name: str) -> Path:
        path = self.fixture_root / name
        path.mkdir(parents=True, exist_ok=False)
        return path

    def run_census(self, run_id: str, fixture: Path, extra_env=None) -> dict:
        env = census_env(fixture)
        if extra_env:
            env.update(extra_env)
        return self.run_process(
            run_id, ["bash", str(self.census)], env, cwd=fixture
        )

    # -- wrappers ------------------------------------------------------------

    def write_wrapper(self, name: str, target: Path, transform: str, exit_mode: str) -> Path:
        census_q = shlex.quote(str(target))
        if transform == "passthrough" and exit_mode == "keep":
            body = (
                "#!/usr/bin/env bash\n"
                "# generated by mori-round13-regressions.py (F02 honest passthrough)\n"
                "exec bash %s \"$@\"\n" % census_q
            )
        else:
            lines = [
                "#!/usr/bin/env bash",
                "# generated by mori-round13-regressions.py (F02 adversarial proxy)",
                "set +e",
                "out=$(bash %s \"$@\" 2>&1)" % census_q,
                "rc=$?",
            ]
            if transform == "banana":
                lines += [
                    "out=${out//MORI_CENSUS: CLEAN/MORI_CENSUS: BANANA}",
                    "out=${out//MORI_CENSUS: DRIFT/MORI_CENSUS: BANANA}",
                ]
            elif transform == "duplicate":
                lines.append(
                    "out=\"$out\"$'\\nMORI_CENSUS: CLEAN "
                    "(findings=0 drift=0 unavailable=0 surfaces=0)'"
                )
            elif transform == "drift-rc0":
                # rc-only: preserve every roll word, force exit 0. DRIFT-
                # emitting fixtures then carry DRIFT with rc0 (inconsistent).
                pass
            elif transform in ("clean-drift9", "drift-drift0"):
                if transform == "clean-drift9":
                    prefix = "MORI_CENSUS: CLEAN ("
                    repl = ("MORI_CENSUS: CLEAN "
                            "(findings=9 drift=9 unavailable=0 surfaces=8)")
                else:
                    prefix = "MORI_CENSUS: DRIFT ("
                    repl = ("MORI_CENSUS: DRIFT "
                            "(findings=0 drift=0 unavailable=0 surfaces=8)")
                pattern = shlex.quote(prefix) + "*"
                lines += [
                    "kept=''",
                    "while IFS= read -r ln; do",
                    "  case \"$ln\" in",
                    "    %s) ln=%s ;;" % (pattern, shlex.quote(repl)),
                    "  esac",
                    "  kept=\"$kept$ln\"$'\\n'",
                    "done <<<\"$out\"",
                    "out=$kept",
                ]
            elif transform == "not-final":
                lines.append("out=\"$out\"$'\\nTRAILER x'")
            elif transform == "verdict-first":
                lines += [
                    "verdict=''; kept=''",
                    "while IFS= read -r ln; do",
                    "  case \"$ln\" in MORI_CENSUS:*) verdict=$ln ;; "
                    "*) kept=\"$kept$ln\"$'\\n' ;; esac",
                    "done <<<\"$out\"",
                    "out=\"$verdict\"$'\\n'\"$kept\"",
                ]
            elif transform == "missing":
                lines += [
                    "kept=''",
                    "while IFS= read -r ln; do",
                    "  case \"$ln\" in MORI_CENSUS:*) continue ;; esac",
                    "  kept=\"$kept$ln\"$'\\n'",
                    "done <<<\"$out\"",
                    "out=$kept",
                ]
            elif transform == "passthrough":
                pass  # rc-only proxy (CLEAN rc1)
            else:
                raise SetupError("unknown wrapper transform: %s" % transform)
            if exit_mode == "keep":
                lines.append('printf \'%s\\n\' "$out"')
                lines.append('exit "$rc"')
            else:
                lines.append('printf \'%s\\n\' "$out"')
                lines.append("exit %s" % exit_mode)
            body = "\n".join(lines) + "\n"
        path = self.wrappers_dir / (name + ".sh")
        write_exec(path, body)
        return path

    def oracle_env(self, scratch: Path) -> dict:
        (scratch / "home").mkdir(parents=True, exist_ok=True)
        (scratch / "tmp").mkdir(parents=True, exist_ok=True)
        return {
            "PATH": "/usr/bin:/bin",
            "HOME": str(scratch / "home"),
            "TMPDIR": str(scratch / "tmp"),
            "TZ": "UTC",
            "LC_ALL": "C",
            "LANG": "C",
            "MORI_SHUFFLE_SEED": str(self.args.seed),
            "MORI_RUN_NONCE": str(self.args.nonce),
        }

    def run_oracle(self, run_id: str, wrapper: Path, oracle: Path = None) -> dict:
        scratch = self.fixture_root / ("oracle-" + run_id)
        scratch.mkdir(parents=True, exist_ok=True)
        return self.run_process(
            run_id,
            ["bash", str(oracle or self.oracle), str(wrapper)],
            self.oracle_env(scratch),
            cwd=self.repo,
        )

    def oracle_runs(self, census_target: Path) -> dict:
        spec = [
            ("R13_F02_HONEST_28_OF_28", "honest", "passthrough", "keep"),
            ("R13_F02_REJECT_BANANA", "banana", "banana", "keep"),
            ("R13_F02_REJECT_DUPLICATE_VERDICT", "duplicate", "duplicate", "keep"),
            ("R13_F02_REJECT_MISSING_VERDICT", "missing", "missing", "keep"),
            ("R13_F02_REJECT_NOT_FINAL_VERDICT", "not-final", "not-final", "keep"),
            ("R13_F02_REJECT_VERDICT_FIRST", "verdict-first", "verdict-first", "keep"),
            ("R13_F02_REJECT_CLEAN_DRIFT9", "clean-drift9", "clean-drift9", "keep"),
            ("R13_F02_REJECT_DRIFT_DRIFT0", "drift-drift0", "drift-drift0", "keep"),
            ("R13_F02_REJECT_CLEAN_RC1", "clean-rc1", "passthrough", "1"),
            ("R13_F02_REJECT_DRIFT_RC0", "drift-rc0", "passthrough", "0"),
        ]
        wrappers = {}
        for claim_id, tag, transform, exit_mode in spec:
            wrappers[tag] = (
                claim_id,
                self.write_wrapper("census-%s" % tag, census_target, transform, exit_mode),
            )

        results = {}

        def job(tag):
            claim_id, wrapper = wrappers[tag]
            results[tag] = (claim_id, self.run_oracle("oracle.%s" % tag, wrapper))

        with ThreadPoolExecutor(max_workers=max(1, self.args.jobs)) as pool:
            list(pool.map(job, [s[1] for s in spec]))
        return {tag: results[tag] for tag in [s[1] for s in spec]}

    # -- claims --------------------------------------------------------------

    def claim(self, claim_id, status, axis, details, run_ids=None):
        entry = {
            "id": claim_id,
            "axis": axis,
            "status": status,
            "details": one_line(details, 600),
            "runs": run_ids or [],
        }
        self.claims.append(entry)
        return entry

    # -- SHONEN --------------------------------------------------------------

    def check_shonen(self) -> None:
        target = Path(self.args.shonen).resolve()
        expected = CANONICAL_SHONEN.encode()
        expected_sha = CANONICAL_SHONEN_SHA256
        witness = "".join(
            ("    " + line) if line.strip("\n") else line
            for line in CANONICAL_SHONEN.splitlines(keepends=True)
        )
        witness_ok = (
            sha256_bytes(witness.encode()) != expected_sha
            and self._shonen_diff(witness.encode(), expected) is not None
        )
        self.claim(
            "R13_SHONEN_INDENT_WITNESS",
            (BASELINE_OK if self.args.baseline else PASS) if witness_ok else FAIL,
            "operability",
            "indented witness digest=%s canonical=%s rejected=%s"
            % (sha256_bytes(witness.encode())[:16], expected_sha[:16],
               "yes" if witness_ok else "no"),
        )
        if not target.is_file():
            self.claim(
                "R13_SHONEN_CANONICAL_BYTES",
                UNAVAILABLE,
                "operability",
                "SHONEN path missing: %s" % target,
            )
            return
        actual = target.read_bytes()
        actual_sha = sha256_bytes(actual)
        diff = self._shonen_diff(actual, expected)
        matched = actual == expected
        if matched:
            status = BASELINE_OK if self.args.baseline else PASS
            detail = "bytes match canonical seed sha=%s bytes=%d" % (
                actual_sha[:16], len(actual)
            )
        else:
            status = BASELINE_MISMATCH if self.args.baseline else FAIL
            detail = "differs from canonical seed expected=%s actual=%s %s" % (
                expected_sha[:16], actual_sha[:16], diff
            )
        self.claim(
            "R13_SHONEN_CANONICAL_BYTES", status, "operability", detail,
            run_ids=[],
        )

    @staticmethod
    def _shonen_diff(actual: bytes, expected: bytes):
        limit = min(len(actual), len(expected))
        for i in range(limit):
            if actual[i] != expected[i]:
                line = actual[:i].count(b"\n") + 1
                return "first diff byte=%d line=%d expected=%r actual=%r" % (
                    i, line, expected[i:i + 1], actual[i:i + 1]
                )
        if len(actual) != len(expected):
            return "length mismatch expected=%d actual=%d" % (
                len(expected), len(actual)
            )
        return None

    # -- C1 ------------------------------------------------------------------

    def check_c1(self) -> None:
        # Primary: system notices (2 kernel / 1 oomd / 3 coredump, all signal
        # 11). The restored contract turns the positive kernel notice into the
        # global critical alarm, so DRIFT is the expected roll by design.
        # Fixture directory names are deliberately neutral (fx-*): the census
        # echoes MORI_JOURNALCTL_BIN, so a case-id path would be a sniffing
        # channel. Run ids stay descriptive in evidence only.
        fixture = self.fixture("fx-a")
        build_journal_fixture(
            fixture, "honor",
            system_records=notice_records(C1_SYSTEM_COUNTS),
        )
        primary = self.run_census("c1.primary", fixture)

        # Leak probe: the stub forces a MESSAGE key into every JSON object. A
        # parser that echoes raw records leaks the canary; a projection does not.
        leak_fixture = self.fixture("fx-b")
        build_journal_fixture(
            leak_fixture, "always",
            system_records=notice_records(C1_SYSTEM_COUNTS),
        )
        leak = self.run_census("c1.leak", leak_fixture)

        # Independent user arm: positive user kernel notices prove the scopes
        # are separate and that the alarm fires for the user scope too.
        user_fixture = self.fixture("fx-c")
        build_journal_fixture(
            user_fixture, "honor",
            user_records=notice_records(C1_USER_COUNTS),
        )
        user_run = self.run_census("c1.user", user_fixture)

        # Positive non-OOM control: oomd/coredump/segfault only -> all INFO and
        # CLEAN. This is what keeps the restored alarm specific to OOM.
        notice_fixture = self.fixture("fx-d")
        build_journal_fixture(
            notice_fixture, "honor",
            system_records=notice_records(C1_NOTICE_ONLY_COUNTS),
        )
        notice_run = self.run_census("c1.notice", notice_fixture)

        # Empty control: six zero counters, no alarm, CLEAN.
        empty_fixture = self.fixture("fx-e")
        build_journal_fixture(empty_fixture, "honor")
        empty_run = self.run_census("c1.empty", empty_fixture)

        # Structured unit routing (all INFO => CLEAN, so the roll proves the
        # generic fleet/non-fleet failure is not escalated):
        #   system: 2 fleet, 1 missing subject, 1 both UNIT and USER_UNIT
        #   user:   1 non-fleet (desktop/OS, owner tsukuroi)
        routing_fixture = self.fixture("fx-f")
        build_journal_fixture(
            routing_fixture, "honor",
            system_records=(
                unit_failure_records([
                    ("UNIT", "shokunin-watchdog.service"),
                    ("UNIT", "ufo-sighting.service"),
                    None,
                ])
                + [journal_record(
                    UNIT_FAILURE_ID,
                    UNIT="shokunin-check.service",
                    USER_UNIT="shokunin-check.service",
                    UNIT_RESULT="exit-code",
                )]
            ),
            user_records=unit_failure_records([
                ("USER_UNIT", "pipewire-pulse.service"),
            ]),
        )
        routing_run = self.run_census("c1.routing", routing_fixture)

        # Structured unit OOM: two system UNIT_RESULT=oom-kill results (one
        # fleet subject, one absent subject) plus one fleet record whose result
        # is missing (result-unknown, never OOM). DRIFT from the crit line.
        oom_fixture = self.fixture("fx-g")
        build_journal_fixture(
            oom_fixture, "honor",
            system_records=(
                unit_failure_records([
                    ("UNIT", "shokunin-fleet-fixture.service"),
                    None,
                ], result="oom-kill")
                + unit_failure_records([
                    ("UNIT", "shokunin-fleet-fixture.service"),
                ], result=None)
            ),
        )
        oom_run = self.run_census("c1.unit-oom", oom_fixture)

        # Generic SIGKILL control: a user process-exit killed/9 record keeps
        # its WARN and DRIFT; it must never be reported as an OOM.
        sigkill_fixture = self.fixture("fx-h")
        build_journal_fixture(
            sigkill_fixture, "honor",
            user_records=sigkill_records(1),
        )
        sigkill_run = self.run_census("c1.sigkill", sigkill_fixture)

        out = primary["stdout"]
        srows = surface_rows(out)
        verdict_word, verdict_reason, _ = verdict_roll(out, primary["rc"])
        rows = findings(out)

        def scoped(rows_map, scope, expected, expected_tokens=None):
            """Check one scoped row: six counts, r14 partition tokens, boot.

            The six round-13 count tokens are pinned byte-identically. The r14
            added tokens must be present on an ok row and must partition the
            raw unit-failure count; `unit_unknown` is a derived bucket, so the
            invariant is checked on the concrete categories instead of guessing
            its definition.
            """
            state, tokens = rows_map.get(scope, (None, {}))
            ok = state == "ok"
            observed = []
            for stem, kind in C1_SURFACE_TOKENS:
                got = tokens.get(stem)
                observed.append("%s=%s" % (stem, got if got is not None else "<absent>"))
                if got != str(expected[kind]):
                    ok = False
            for name in C1_PARTITION_TOKENS:
                got = tokens.get(name)
                observed.append("%s=%s" % (name, got if got is not None else "<absent>"))
                if got is None:
                    ok = False
            if expected_tokens:
                for name, want in expected_tokens.items():
                    if tokens.get(name) != str(want):
                        ok = False
            # Counters that only the alarm/SIGKILL fixtures may raise default
            # to zero everywhere else; an unpinned nonzero value is a failure.
            pinned = expected_tokens or {}
            for name in ("unit_oom", "unit_signal"):
                if name not in pinned and _token_int(tokens, name) != 0:
                    ok = False
            raw = _token_int(tokens, "unit_failure_record")
            parts = [
                _token_int(tokens, name) for name in (
                    "unit_fleet", "unit_nonfleet", "unit_missing",
                    "unit_ambiguous", "unit_malformed",
                )
            ]
            if raw is not None and all(value is not None for value in parts):
                if sum(parts) != raw:
                    ok = False
                    observed.append("partition_mismatch=%s!=%d" % (parts, raw))
            oom = _token_int(tokens, "unit_oom")
            oom_parts = [
                _token_int(tokens, name) for name in (
                    "unit_oom_fleet", "unit_oom_nonfleet",
                    "unit_oom_subject_unknown",
                )
            ]
            if oom is not None and all(v is not None for v in oom_parts):
                if sum(oom_parts) != oom:
                    ok = False
                    observed.append("oom_partition_mismatch=%s!=%d" % (oom_parts, oom))
            all_zero = all(tokens.get(stem) == "0" for stem, kind in C1_SURFACE_TOKENS)
            boot = tokens.get("boot")
            if not (boot == JOURNAL_BOOT or
                    (all_zero and boot == "unavailable:no-records")):
                ok = False
            if tokens.get("scope") not in (None, scope):
                ok = False
            if "total" in tokens or "sum" in tokens:
                ok = False
            return ok, state, tokens, observed

        def oom_line(rec, rows_map):
            """Exactly one global crit OOM line, counters equal to the rows.

            L1 final schema: one line, six named counters, no `count=`/`total`/
            `sum`, and each counter equals the matching scoped SURFACE token
            (including an `unavailable:<reason>` value). Missing or duplicated
            lines are a failure, not an absent alarm.
            """
            hits = [row for row in findings(rec["stdout"]) if row[0] == OOM_FINDING]
            if len(hits) != 1:
                return None, "lines=%d" % len(hits)
            fid, sev, tok, rest = hits[0]
            note = "sev=%s" % sev
            ok = sev == EXPECTED_SEVERITY[OOM_FINDING]
            if any(name in tok for name in ("count", "total", "sum")):
                ok = False
                note += ",summed"
            pairs = {
                "user_notice": ("user", "kernel_oom_notice"),
                "system_notice": ("system", "kernel_oom_notice"),
                "user_unit_oom": ("user", "unit_oom"),
                "system_unit_oom": ("system", "unit_oom"),
                "user_unit_oom_result_unknown": (
                    "user", "unit_oom_result_unknown"),
                "system_unit_oom_result_unknown": (
                    "system", "unit_oom_result_unknown"),
            }
            for field, (scope, token) in pairs.items():
                got = tok.get(field)
                want = rows_map.get(scope, ("", {}))[1].get(token)
                if got is None or want is None or got != want:
                    ok = False
                    note += ",%s=%s!=%s" % (field, got, want)
            return tok, note if not ok else None

        system_ok, state, stokens, system_observed = scoped(
            srows, "system", C1_SYSTEM_COUNTS
        )
        if system_ok:
            _tok, oom_note = oom_line(primary, srows)
            if oom_note is not None:
                system_ok = False
                system_observed.append("oom=" + oom_note)
            if any(fid in (UNIT_FLEET_FINDING, UNIT_FLEET_FINDING_SYSTEM,
                           UNIT_OUT_OF_SCOPE_FINDING,
                           UNIT_OUT_OF_SCOPE_FINDING_SYSTEM,
                           UNIT_UNATTRIBUTED_FINDING,
                           KILL_SIGNAL_FINDING, KILL_SIGNAL_FINDING_SYSTEM)
                   for fid, sev, tok, rest in rows):
                system_ok = False
        if primary["timed_out"]:
            system_ok = False
        if self.args.baseline:
            # Pre-fix has no scoped structured rows: absent counts are the
            # expected defect; an unexpected full pass is a baseline deviation.
            status = EXPECTED_DEFECT if not system_ok else BASELINE_DEVIATION
        else:
            status = PASS if system_ok else FAIL
        self.claim(
            "R13_C1_SYSTEM_NOTICE_COUNTS", status, "coverage",
            "expected [%s]; observed [%s]; state=%s rc=%s verdict=%s/%s"
            % (
                " ".join("%s=%d" % (stem, C1_SYSTEM_COUNTS[kind])
                         for stem, kind in C1_SURFACE_TOKENS),
                " ".join(system_observed), state, primary["rc"],
                verdict_word, verdict_reason,
            ),
            run_ids=["c1.primary"],
        )


        # User scope zero arm: an independent row with zero class tokens, its
        # own boot anchor, and no summed field. The global OOM line has no
        # per-scope id suffix, so a user leak is detected from the finding's own
        # scope token and from the counter equality checked above, never from
        # `_USER` id suffixes.
        user_ok, ustate, utokens, user_observed = scoped(
            srows, "user", C1_EMPTY_COUNTS
        )
        if "user" not in srows:
            user_ok = False
        if any(tok.get("scope") == "user" for fid, sev, tok, rest in rows):
            user_ok = False
        if self.args.baseline:
            status = EXPECTED_DEFECT if not user_ok else BASELINE_DEVIATION
        else:
            status = PASS if user_ok else FAIL
        self.claim(
            "R13_C1_USER_SCOPE_INDEPENDENT", status, "coverage",
            "observed [%s] state=%s boot=%s scope_token=%s"
            % (" ".join(user_observed), ustate, utokens.get("boot", "<absent>"),
               utokens.get("scope", "<absent>")),
            run_ids=["c1.primary"],
        )

        # User scope nonzero arm: user-only kernel notices must produce the
        # global critical alarm and DRIFT, while every system class stays 0 and
        # the per-scope counters stay separate.
        nrows = surface_rows(user_run["stdout"])
        nu_ok, nustate, nutokens, nuser_observed = scoped(
            nrows, "user", C1_USER_COUNTS
        )
        ns_ok, nsstate, nstokens, nsystem_observed = scoped(
            nrows, "system", C1_EMPTY_COUNTS
        )
        unonzero_ok = nu_ok and ns_ok
        urows = findings(user_run["stdout"])
        uoom, uoom_note = oom_line(user_run, nrows)
        if uoom_note is not None:
            unonzero_ok = False
            uoom_observed = "oom=" + uoom_note
        else:
            if _token_int(uoom, "user_notice") != C1_USER_COUNTS["kernel"]:
                unonzero_ok = False
            if _token_int(uoom, "system_notice") != 0:
                unonzero_ok = False
            uoom_observed = "oom user_notice=%s system_notice=%s" % (
                uoom.get("user_notice"), uoom.get("system_notice"))
        if any(tok.get("scope") == "system" for fid, sev, tok, rest in urows):
            unonzero_ok = False
        uword, ureason, _ = verdict_roll(user_run["stdout"], user_run["rc"])
        if (uword, ureason, user_run["rc"]) != ("DRIFT", "ok", 1):
            unonzero_ok = False
        if self.args.baseline:
            status_u = EXPECTED_DEFECT if not unonzero_ok else BASELINE_DEVIATION
        else:
            status_u = PASS if unonzero_ok else FAIL
        self.claim(
            "R13_C1_USER_SCOPE_NONZERO", status_u, "coverage",
            "fixture user=%s; user=[%s] state=%s; system=[%s] state=%s; "
            "%s; verdict=%s/%s rc=%s"
            % (C1_USER_COUNTS, " ".join(nuser_observed), nustate,
               " ".join(nsystem_observed), nsstate, uoom_observed,
               uword, ureason, user_run["rc"]),
            run_ids=["c1.user"],
        )

        # MESSAGE-free output, on both the honoring and the leak-forcing stub.
        # run_process stores REDACTED stderr/stdout, so the literal canary can
        # never appear there; the pre-redaction `canary_present` flag and the
        # redaction marker are the leak evidence.
        message_text_ok = True
        leak_notes = []
        for label, rec in (("primary", primary), ("leak", leak)):
            blob = rec["stdout"] + "\n" + rec["stderr"]
            if rec.get("canary_present") or "<canary-redacted>" in blob:
                message_text_ok = False
                leak_notes.append("%s:canary" % label)
            if MESSAGE_KEY_RE.search(blob):
                message_text_ok = False
                leak_notes.append("%s:MESSAGE-key" % label)
            if MESSAGE_EQ_RE.search(blob):
                message_text_ok = False
                leak_notes.append("%s:MESSAGE=" % label)
        # The leak run must still report the structured counts: a parser that
        # drops all records to avoid MESSAGE would fail here. This is a
        # structured-parse requirement, not a MESSAGE-text requirement, so it
        # never gates the baseline's "no text leak" observation.
        leak_ok, _, _, _ = scoped(
            surface_rows(leak["stdout"]), "system", C1_SYSTEM_COUNTS
        )
        if not leak_ok:
            leak_notes.append("leak:counts")
        strict_message_ok = message_text_ok and leak_ok
        if self.args.baseline:
            status = BASELINE_OK if message_text_ok else BASELINE_DEVIATION
        else:
            status = PASS if strict_message_ok else FAIL
        self.claim(
            "R13_C1_NO_MESSAGE_TEXT", status, "coverage",
            "message-text absent=%s leak_counts=%s notes=%s"
            % ("yes" if message_text_ok else "no",
               "yes" if leak_ok else "no",
               ",".join(leak_notes) or "none"),
            run_ids=["c1.primary", "c1.leak"],
        )

        def one_finding(rows_list, fid, severity, **want):
            hits = [row for row in rows_list if row[0] == fid]
            if len(hits) != 1:
                return False
            _fid, sev, tok, _rest = hits[0]
            if sev != severity:
                return False
            for key, value in want.items():
                if tok.get(key) != str(value):
                    return False
            return True

        # The restored alarm: kernel OOM notices are critical and roll DRIFT.
        # Exactly one global line; the per-scope counters mirror the SURFACE
        # tokens and are never summed.
        oom_tok, oom_note = oom_line(primary, srows)
        cword, creason, _ = verdict_roll(primary["stdout"], primary["rc"])
        alarm_ok = (
            oom_note is None
            and _token_int(oom_tok, "system_notice")
            == C1_SYSTEM_COUNTS["kernel"]
            and _token_int(oom_tok, "user_notice") == 0
            and (cword, creason, primary["rc"]) == ("DRIFT", "ok", 1)
        )
        if self.args.baseline:
            status = EXPECTED_DEFECT if not alarm_ok else BASELINE_DEVIATION
        else:
            status = PASS if alarm_ok else FAIL
        self.claim(
            "R13_C1_OOM_ALARM_DRIFT", status, "coverage",
            "verdict=%s/%s rc=%s oom=%s"
            % (cword, creason, primary["rc"],
               oom_note if oom_note is not None
               else "system_notice=%s user_notice=%s" % (
                   (oom_tok or {}).get("system_notice"),
                   (oom_tok or {}).get("user_notice"))),
            run_ids=["c1.primary"],
        )

        # Positive non-OOM notice fixture: still INFO and CLEAN. This is the
        # control that keeps the restored alarm specific to OOM; severity creep
        # on oomd/coredump/segfault fails here.
        nrows2 = surface_rows(notice_run["stdout"])
        nsys_ok, nsys_state, nsys_tok, nsys_obs = scoped(
            nrows2, "system", C1_NOTICE_ONLY_COUNTS
        )
        nusr_ok, nusr_state, nusr_tok, nusr_obs = scoped(
            nrows2, "user", C1_EMPTY_COUNTS
        )
        nfnd = findings(notice_run["stdout"])
        nword, nreason, _ = verdict_roll(notice_run["stdout"], notice_run["rc"])
        n_alarm = any(fid == OOM_FINDING for fid, sev, tok, rest in nfnd)
        n_route = any(
            fid in (
                UNIT_FLEET_FINDING, UNIT_FLEET_FINDING_SYSTEM,
                UNIT_OUT_OF_SCOPE_FINDING, UNIT_OUT_OF_SCOPE_FINDING_SYSTEM,
                UNIT_UNATTRIBUTED_FINDING,
                KILL_SIGNAL_FINDING, KILL_SIGNAL_FINDING_SYSTEM,
            )
            for fid, sev, tok, rest in nfnd
        )
        notice_roll_ok = (
            (nword, nreason, notice_run["rc"]) == ("CLEAN", "ok", 0)
            and not n_alarm and not n_route
        )
        notice_ok = notice_roll_ok and nsys_ok and nusr_ok
        if self.args.baseline:
            status = BASELINE_CONTROL if notice_roll_ok else BASELINE_DEVIATION
        else:
            status = PASS if notice_ok else FAIL
        self.claim(
            "R13_C1_NOTICE_CLEAN_CONTROL", status, "coverage",
            "verdict=%s/%s rc=%s system=[%s] user=[%s] alarm=%s routing=%s"
            % (nword, nreason, notice_run["rc"], " ".join(nsys_obs),
               " ".join(nusr_obs), "yes" if n_alarm else "no",
               "yes" if n_route else "no"),
            run_ids=["c1.notice"],
        )

        # Empty negative control: six zero counters and no alarm. This is the
        # test against an unconditional DRIFT implementation.
        erows = surface_rows(empty_run["stdout"])
        esys_ok, esys_state, esys_tok, esys_obs = scoped(
            erows, "system", C1_EMPTY_COUNTS
        )
        eusr_ok, eusr_state, eusr_tok, eusr_obs = scoped(
            erows, "user", C1_EMPTY_COUNTS
        )
        efnd = findings(empty_run["stdout"])
        eword, ereason, _ = verdict_roll(empty_run["stdout"], empty_run["rc"])
        e_alarm = any(fid == OOM_FINDING for fid, sev, tok, rest in efnd)
        e_route = any(
            fid in (
                UNIT_FLEET_FINDING, UNIT_FLEET_FINDING_SYSTEM,
                UNIT_OUT_OF_SCOPE_FINDING, UNIT_OUT_OF_SCOPE_FINDING_SYSTEM,
                UNIT_UNATTRIBUTED_FINDING,
                KILL_SIGNAL_FINDING, KILL_SIGNAL_FINDING_SYSTEM,
            )
            for fid, sev, tok, rest in efnd
        )
        empty_roll_ok = (
            (eword, ereason, empty_run["rc"]) == ("CLEAN", "ok", 0)
            and not e_alarm and not e_route
        )
        empty_ok = empty_roll_ok and esys_ok and eusr_ok
        if self.args.baseline:
            status = BASELINE_CONTROL if empty_roll_ok else BASELINE_DEVIATION
        else:
            status = PASS if empty_ok else FAIL
        self.claim(
            "R13_C1_EMPTY_CLEAN_CONTROL", status, "coverage",
            "verdict=%s/%s rc=%s system=[%s] user=[%s] alarm=%s routing=%s"
            % (eword, ereason, empty_run["rc"], " ".join(esys_obs),
               " ".join(eusr_obs), "yes" if e_alarm else "no",
               "yes" if e_route else "no"),
            run_ids=["c1.empty"],
        )

        # Structured UNIT_RESULT=oom-kill is an OOM alarm in its own right,
        # independent of subject attribution. The raw unit-failure total keeps
        # all three records (two oom results + one missing result).
        orows = surface_rows(oom_run["stdout"])
        osys_ok, osys_state, osys_tok, osys_obs = scoped(
            orows, "system", dict(C1_EMPTY_COUNTS, unit_failure=3),
            expected_tokens={
                "unit_oom": 2,
                "unit_oom_fleet": 1,
                "unit_oom_subject_unknown": 1,
                "unit_oom_result_unknown": 1,
                "unit_missing": 1,
                "unit_signal": 0,
            },
        )
        ousr_ok, ousr_state, ousr_tok, ousr_obs = scoped(
            orows, "user", C1_EMPTY_COUNTS
        )
        oom2, oom2_note = oom_line(oom_run, orows)
        oword, oreason, _ = verdict_roll(oom_run["stdout"], oom_run["rc"])
        unit_oom_ok = (
            osys_ok and ousr_ok and oom2_note is None
            and _token_int(oom2, "system_unit_oom") == 2
            and _token_int(oom2, "system_unit_oom_result_unknown") == 1
            and _token_int(oom2, "user_unit_oom") == 0
            and (oword, oreason, oom_run["rc"]) == ("DRIFT", "ok", 1)
        )
        if self.args.baseline:
            status = EXPECTED_DEFECT if not unit_oom_ok else BASELINE_DEVIATION
        else:
            status = PASS if unit_oom_ok else FAIL
        self.claim(
            "R13_C1_UNIT_OOM_KILL_ALARM", status, "coverage",
            "verdict=%s/%s rc=%s system=[%s] user=[%s] oom=%s"
            % (oword, oreason, oom_run["rc"], " ".join(osys_obs),
               " ".join(ousr_obs),
               oom2_note if oom2_note is not None
               else "system_unit_oom=%s system_unit_oom_result_unknown=%s"
               % ((oom2 or {}).get("system_unit_oom"),
                  (oom2 or {}).get("system_unit_oom_result_unknown"))),
            run_ids=["c1.unit-oom"],
        )

        # Structured fleet/non-fleet/unknown partition. All findings are INFO,
        # so the roll stays CLEAN: a generic failure is not escalated. Raw
        # counts must equal the partition even when subject metadata is absent
        # or ambiguous (2 fleet + 1 missing + 1 ambiguous in system; 1
        # non-fleet in user).
        rrows = surface_rows(routing_run["stdout"])
        rsys_ok, rsys_state, rsys_tok, rsys_obs = scoped(
            rrows, "system", dict(C1_EMPTY_COUNTS, unit_failure=4),
            expected_tokens={
                "unit_fleet": 2,
                "unit_nonfleet": 0,
                "unit_missing": 1,
                "unit_ambiguous": 1,
                "unit_malformed": 0,
                "unit_signal": 0,
            },
        )
        rusr_ok, rusr_state, rusr_tok, rusr_obs = scoped(
            rrows, "user", dict(C1_EMPTY_COUNTS, unit_failure=1),
            expected_tokens={
                "unit_fleet": 0,
                "unit_nonfleet": 1,
                "unit_missing": 0,
                "unit_ambiguous": 0,
                "unit_signal": 0,
            },
        )
        rfnd = findings(routing_run["stdout"])
        rword, rreason, _ = verdict_roll(routing_run["stdout"], routing_run["rc"])
        fleet_ok = one_finding(
            rfnd, UNIT_FLEET_FINDING_SYSTEM, EXPECTED_SEVERITY[
                UNIT_FLEET_FINDING_SYSTEM], count=2, scope="system"
        )
        nonfleet_ok = one_finding(
            rfnd, UNIT_OUT_OF_SCOPE_FINDING, EXPECTED_SEVERITY[
                UNIT_OUT_OF_SCOPE_FINDING], count=1, scope="user",
            owner="tsukuroi"
        )
        unknown_ok = one_finding(
            rfnd, UNIT_UNATTRIBUTED_FINDING, EXPECTED_SEVERITY[
                UNIT_UNATTRIBUTED_FINDING], count=2, scope="system",
            owner="unresolved", reason="subject-metadata-unknown"
        )
        routing_ok = (
            rsys_ok and rusr_ok and fleet_ok and nonfleet_ok and unknown_ok
            and not any(fid == OOM_FINDING for fid, sev, tok, rest in rfnd)
            and not any(fid.startswith("KILL_SIGNAL")
                        for fid, sev, tok, rest in rfnd)
            and (rword, rreason, routing_run["rc"]) == ("CLEAN", "ok", 0)
        )
        if self.args.baseline:
            status = EXPECTED_DEFECT if not routing_ok else BASELINE_DEVIATION
        else:
            status = PASS if routing_ok else FAIL
        self.claim(
            "R13_C1_UNIT_FAILURE_ROUTING", status, "coverage",
            "verdict=%s/%s rc=%s system=[%s] user=[%s] fleet=%s nonfleet=%s "
            "unattributed=%s"
            % (rword, rreason, routing_run["rc"], " ".join(rsys_obs),
               " ".join(rusr_obs), "yes" if fleet_ok else "no",
               "yes" if nonfleet_ok else "no",
               "yes" if unknown_ok else "no"),
            run_ids=["c1.routing"],
        )

        # Generic SIGKILL: the user killed/9 process-exit record keeps WARN and
        # DRIFT, and must never be relabeled as an OOM.
        krows = surface_rows(sigkill_run["stdout"])
        ksys_ok, ksys_state, ksys_tok, ksys_obs = scoped(
            krows, "system", C1_EMPTY_COUNTS
        )
        kusr_ok, kusr_state, kusr_tok, kusr_obs = scoped(
            krows, "user",
            dict(C1_EMPTY_COUNTS, sigkill=1),
            expected_tokens={},
        )
        kfnd = findings(sigkill_run["stdout"])
        kword, kreason, _ = verdict_roll(sigkill_run["stdout"], sigkill_run["rc"])
        kill_ok = one_finding(
            kfnd, KILL_SIGNAL_FINDING, EXPECTED_SEVERITY[KILL_SIGNAL_FINDING],
            count=1, scope="user", process_sigkill=1, user_unit_signal=0
        )
        sigkill_ok = (
            ksys_ok and kusr_ok and kill_ok
            and not any(fid == OOM_FINDING for fid, sev, tok, rest in kfnd)
            and (kword, kreason, sigkill_run["rc"]) == ("DRIFT", "ok", 1)
        )
        if self.args.baseline:
            status = EXPECTED_DEFECT if not sigkill_ok else BASELINE_DEVIATION
        else:
            status = PASS if sigkill_ok else FAIL
        self.claim(
            "R13_C1_SIGKILL_WARN_PRESERVED", status, "coverage",
            "verdict=%s/%s rc=%s system=[%s] user=[%s] kill_warn=%s"
            % (kword, kreason, sigkill_run["rc"], " ".join(ksys_obs),
               " ".join(kusr_obs), "yes" if kill_ok else "no"),
            run_ids=["c1.sigkill"],
        )

    # -- F01 -----------------------------------------------------------------

    def f01_arm(self, run_id: str, subject: bool) -> dict:
        fixture = self.fixture("fx-i" if subject else "fx-j")
        build_history_fixture(fixture, subject)
        return self.run_census(run_id, fixture)

    def check_f01(self) -> None:
        subject = self.f01_arm("f01.subject", True)
        sibling = self.f01_arm("f01.sibling", False)

        state, tokens = lane_row(subject["stdout"])
        word, reason, _ = verdict_roll(subject["stdout"], subject["rc"])
        observed = (
            "state=%s basis=%s subject_commits=%s other_authored_commits=%s "
            "verdict=%s/%s rc=%s"
            % (state, tokens.get("basis"), tokens.get("subject_commits"),
               tokens.get("other_authored_commits"), word, reason, subject["rc"])
        )
        strict_subject_ok = (
            state == "progressing"
            and tokens.get("basis") == "row-A"
            and tokens.get("subject_commits") == "yes"
            and subject["rc"] == 0
            and word == "CLEAN" and reason == "ok"
        )
        if self.args.baseline:
            defect_present = (
                state == "progressing-weak"
                and tokens.get("basis") == "row-C"
                and subject["rc"] == 0
            )
            status = EXPECTED_DEFECT if defect_present else BASELINE_DEVIATION
        else:
            status = PASS if strict_subject_ok else FAIL
        self.claim(
            "R13_F01_EXACT_AUTHOR_LONG_HISTORY", status, "operability",
            "%s; expected post-fix state=progressing basis=row-A subject_commits=yes"
            % observed,
            run_ids=["f01.subject"],
        )

        state2, tokens2 = lane_row(sibling["stdout"])
        word2, reason2, _ = verdict_roll(sibling["stdout"], sibling["rc"])
        sibling_ok = (
            state2 == "progressing-weak"
            and tokens2.get("basis") == "row-C"
            and tokens2.get("other_authored_commits") == str(HISTORY_SIBLINGS)
            and sibling["rc"] == 0
            and word2 == "CLEAN" and reason2 == "ok"
        )
        sibling_observed = (
            "state=%s basis=%s other_authored_commits=%s verdict=%s/%s rc=%s"
            % (state2, tokens2.get("basis"),
               tokens2.get("other_authored_commits"), word2, reason2,
               sibling["rc"])
        )
        if self.args.baseline:
            status2 = BASELINE_CONTROL if sibling_ok else BASELINE_DEVIATION
        else:
            status2 = PASS if sibling_ok else FAIL
        self.claim(
            "R13_F01_SIBLING_CONTROL_LONG_HISTORY", status2, "operability",
            "%s; expected progressing-weak row-C with %d siblings"
            % (sibling_observed, HISTORY_SIBLINGS),
            run_ids=["f01.sibling"],
        )

    # -- F02 -----------------------------------------------------------------

    def f02_status(self, claim_id: str, rec: dict, tag: str) -> None:
        matched_total = oracle_summary(rec["stdout"])
        reasons = fail_reasons(rec["stdout"])
        if rec["timed_out"] or rec["rc"] is None:
            status = UNAVAILABLE
            detail = "run did not complete (timeout=%s error=%s)" % (
                rec["timed_out"], rec["error"]
            )
        elif matched_total is None:
            status = FAIL if not self.args.baseline else BASELINE_DEVIATION
            detail = "no MORI_SILENCE_CASES summary; rc=%s stderr=%s" % (
                rec["rc"], one_line(rec["stderr"], 160)
            )
        else:
            matched, total = matched_total
            detail = "matched=%d total=%d rc=%d verdict_reasons=%s" % (
                matched, total, rec["rc"], ",".join(sorted(reasons)) or "none"
            )
            if self.args.baseline:
                status, detail = self._f02_baseline(tag, matched, total, rec, reasons, detail)
            else:
                status, detail = self._f02_strict(tag, matched, total, rec, reasons, detail)
        self.claim(claim_id, status, "operability", detail, run_ids=["oracle." + tag])

    @staticmethod
    def _f02_strict(tag, matched, total, rec, reasons, detail):
        passes = pass_cases(rec["stdout"])

        def selective(must_pass, must_not_pass, auto_allowed_state):
            missing = must_pass - set(passes)
            forbidden = set(passes) & must_not_pass
            extras = set(passes) - must_pass - {AUTO_ID}
            auto_state = passes.get(AUTO_ID)
            auto_ok = auto_state is None or auto_state in auto_allowed_state
            ok = (
                not missing and not forbidden and not extras and auto_ok
                and matched == len(passes) and total == 28 and rec["rc"] == 1
            )
            return ok, "PASS_set=%s auto=%s" % (sorted(must_pass), auto_state)

        if tag == "honest":
            ok = (matched == 28 and total == 28 and rec["rc"] == 0
                  and not reasons and len(passes) == 28)
            must = "matched=28 total=28 rc=0"
        elif tag == "banana":
            ok = (matched == 0 and total == 28 and rec["rc"] == 1
                  and "malformed" in reasons)
            must = "0/28 rc=1 reason=malformed"
        elif tag == "duplicate":
            ok = (matched == 0 and total == 28 and rec["rc"] == 1
                  and "duplicate" in reasons)
            must = "0/28 rc=1 reason=duplicate"
        elif tag == "missing":
            ok = (matched == 0 and total == 28 and rec["rc"] == 1
                  and "missing" in reasons)
            must = "0/28 rc=1 reason=missing"
        elif tag == "not-final":
            ok = (matched == 0 and total == 28 and rec["rc"] == 1
                  and "not-final" in reasons)
            must = "0/28 rc=1 reason=not-final"
        elif tag == "verdict-first":
            ok = (matched == 0 and total == 28 and rec["rc"] == 1 and bool(reasons))
            must = "0/28 rc=1 with a verdict rejection"
        elif tag == "clean-rc1":
            ok, extra = selective(
                set(SILENT_IDS), set(ALL_CASE_IDS) - set(SILENT_IDS) - {AUTO_ID},
                {"silent"},
            )
            ok = ok and "inconsistent" in reasons
            must = "only silent fixtures pass (6 or 7/28) rc=1 inconsistent " + extra
        elif tag == "drift-rc0":
            ok, extra = selective(
                set(ALL_CASE_IDS) - set(SILENT_IDS) - {AUTO_ID}, set(SILENT_IDS),
                {"progressing-weak", "progressing", "young", "not-open", "unavailable"},
            )
            ok = ok and "inconsistent" in reasons
            must = "only CLEAN fixtures pass (21 or 22/28) rc=1 inconsistent " + extra
        elif tag == "clean-drift9":
            ok, extra = selective(
                set(SILENT_IDS), set(ALL_CASE_IDS) - set(SILENT_IDS) - {AUTO_ID},
                {"silent"},
            )
            ok = ok and "inconsistent" in reasons
            must = "only DRIFT fixtures pass (6 or 7/28) rc=1 inconsistent " + extra
        elif tag == "drift-drift0":
            ok, extra = selective(
                set(ALL_CASE_IDS) - set(SILENT_IDS) - {AUTO_ID}, set(SILENT_IDS),
                {"progressing-weak", "progressing", "young", "not-open", "unavailable"},
            )
            ok = ok and "inconsistent" in reasons
            must = "only CLEAN fixtures pass (21 or 22/28) rc=1 inconsistent " + extra
        else:
            ok = False
            must = "known wrapper"
        return (PASS if ok else FAIL), "%s; expected %s" % (detail, must)

    @staticmethod
    def _f02_baseline(tag, matched, total, rec, reasons, detail):
        # Pre-fix (audit-r11 Appendix C and siblings): rename, duplicate and
        # non-final rolls still score 28/28 because only ^MORI_CENSUS: presence
        # and the first match are read; tallies are never inspected. Missing is
        # already refused as a crash; rc-only proxies are refused only by the
        # independent rc/state wants.
        if tag == "honest":
            ok = matched == 28 and total == 28 and rec["rc"] == 0
            status = BASELINE_OK if ok else BASELINE_DEVIATION
            must = "28/28 rc=0"
        elif tag in ("banana", "duplicate", "not-final", "verdict-first",
                     "clean-drift9", "drift-drift0"):
            ok = matched == 28 and total == 28 and rec["rc"] == 0
            status = EXPECTED_DEFECT if ok else BASELINE_DEVIATION
            must = "accepted 28/28 (expected pre-fix defect)"
        elif tag == "missing":
            # The frozen readonly case checks mutation + nonce only, so it is
            # the single pre-fix PASS; shape's verdict-presence test and every
            # assert_case fail.
            ok = matched == 1 and total == 28 and rec["rc"] == 1
            status = BASELINE_REJECTED if ok else BASELINE_DEVIATION
            must = "rejected (readonly guard only: 1/28) rc=1"
        elif tag == "clean-rc1":
            # The six/seven DRIFT fixtures pass on want-rc; the frozen readonly
            # and shape guards ignore rc, adding two more PASSes.
            ok = matched in (8, 9) and total == 28 and rec["rc"] == 1
            status = BASELINE_REJECTED if ok else BASELINE_DEVIATION
            must = "8 or 9/28 rc=1 (want-rc refusal only)"
        elif tag == "drift-rc0":
            # Every CLEAN fixture passes (21 or 22, including readonly/shape).
            ok = matched in (21, 22) and total == 28 and rec["rc"] == 1
            status = BASELINE_REJECTED if ok else BASELINE_DEVIATION
            must = "21 or 22/28 rc=1 (want-rc refusal only)"
        else:
            ok = False
            status = BASELINE_DEVIATION
            must = "known wrapper"
        return status, "%s; expected %s" % (detail, must)

    def check_f02(self, results: dict) -> None:
        for tag in ("honest", "banana", "duplicate", "missing", "not-final",
                    "verdict-first", "clean-drift9", "drift-drift0",
                    "clean-rc1", "drift-rc0"):
            claim_id, rec = results[tag]
            self.f02_status(claim_id, rec, tag)

    # -- mutations -----------------------------------------------------------

    @staticmethod
    def replace_function(target_text: str, func: str, replacement: str):
        pattern = re.compile(
            r"(?m)^%s\(\) \{\n.*?^\}" % re.escape(func), re.S
        )
        hits = list(pattern.finditer(target_text))
        if len(hits) != 1:
            raise SetupError(
                "mutation anchor %s: %d matches in target" % (func, len(hits))
            )
        hit = hits[0]
        return (
            target_text[: hit.start()] + replacement + target_text[hit.end():],
            replacement,
        )

    @staticmethod
    def transplant(target_text: str, source_text: str, func: str):
        pattern = re.compile(
            r"(?m)^%s\(\) \{\n.*?^\}" % re.escape(func), re.S
        )
        target_hits = list(pattern.finditer(target_text))
        source_hits = list(pattern.finditer(source_text))
        if len(target_hits) != 1:
            raise SetupError(
                "mutation anchor %s: %d matches in target" % (func, len(target_hits))
            )
        if len(source_hits) != 1:
            raise SetupError(
                "mutation anchor %s: %d matches in frozen source" % (func, len(source_hits))
            )
        before = target_hits[0]
        mutant = (
            target_text[: before.start()]
            + source_hits[0].group(0)
            + target_text[before.end():]
        )
        return mutant, source_hits[0].group(0)

    def build_mutant(self, kind: str):
        target = self.census if kind == "f01" else self.oracle
        target_text = target.read_text(encoding="utf-8")
        if kind == "f01":
            source = self.frozen.get(target.name)
            if source is None:
                raise SetupError(
                    "frozen source for %s missing from %s"
                    % (target.name, self.args.frozen_dir)
                )
            source_text = source.read_text(encoding="utf-8")
            func = "grade_lane"
            needed = (
                "is_root_lane", "ps_walk", "ps_report_closed", "in_lane_scope",
                "epoch_mtime", "is_int", "cap", "emit_finding", "emit_surface",
                "iso_to_epoch", "ledger_ts_fallback", "resolve_roster",
            )
            missing = [
                name for name in needed
                if not re.search(r"(?m)^%s\(\) \{" % re.escape(name), target_text)
            ]
            if missing:
                raise SetupError(
                    "mutation f01: fixed census lacks helper(s) used by the "
                    "frozen grade_lane: %s" % ",".join(missing)
                )
            mutant_text, transplanted = self.transplant(
                target_text, source_text, func
            )
            origin = {
                "attribution": (
                    "whole frozen grade_lane function transplanted; not a "
                    "membership-lines-only or byte-exact single-line revert; "
                    "the frozen body also carries its older environment-"
                    "hardening/fsmonitor behavior"
                ),
                "frozen_source": str(source),
                "frozen_sha256": sha256_file(source),
            }
        else:
            # F02's fix IS the verdict gate. Revert only its locus: the gate
            # returns ok on mere `^MORI_CENSUS:` prefix presence, exactly the
            # pre-fix oracle's read (audit-r11 Appendix C). Every call site
            # (assert_case, readonly, shape) then sees the old semantics; no
            # other oracle behavior is touched.
            func = "verdict_grade"
            mutant_text, transplanted = self.replace_function(
                target_text, func, PRE_FIX_VERDICT_GRADE
            )
            origin = {
                "attribution": (
                    "reconstructed prefix-presence verdict_grade shim; the "
                    "pre-fix oracle had no such function body, so this proves "
                    "single-locus sufficiency, not original-byte restoration"
                ),
                "frozen_source": None,
                "frozen_sha256": None,
                "reverted_by": "pre_fix_prefix_presence_shim",
                "shim_sha256": sha256_bytes(transplanted.encode()),
            }
        if mutant_text == target_text:
            raise SetupError("mutation %s: revert was a no-op" % kind)
        path = self.mutants_dir / ("%s-%s.sh" % (kind, target.name))
        write_exec(path, mutant_text)
        syntax = subprocess.run(
            ["bash", "-n", str(path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if syntax.returncode != 0:
            raise SetupError(
                "mutation %s: mutant fails bash -n: %s"
                % (kind, one_line(syntax.stderr))
            )
        info = {
            "kind": kind,
            "function": func,
            "target": str(target),
            "target_sha256": sha256_file(target),
            "mutant": str(path),
            "mutant_sha256": sha256_file(path),
            "transplanted_chars": len(transplanted),
        }
        info.update(origin)
        return info

    def check_mutations(self, kinds) -> None:
        for kind in kinds:
            try:
                info = self.build_mutant(kind)
            except SetupError as exc:
                self.claim(
                    "R13_MUTATION_%s_RED_BEFORE" % kind.upper(),
                    MUTATION_UNAVAILABLE, "operability", str(exc),
                )
                continue
            if kind == "f01":
                fixture = self.fixture("fx-k")
                build_history_fixture(fixture, True)
                rec = self.run_process(
                    "mutation.f01.subject",
                    ["bash", info["mutant"]],
                    census_env(fixture),
                    cwd=fixture,
                )
                state, tokens = lane_row(rec["stdout"])
                word, reason, _ = verdict_roll(rec["stdout"], rec["rc"])
                reproduced = (
                    state == "progressing-weak"
                    and tokens.get("basis") == "row-C"
                    and rec["rc"] == 0
                )
                self.claim(
                    "R13_MUTATION_F01_RED_BEFORE",
                    MUTATION_RED if reproduced else MUTATION_MISS,
                    "operability",
                    "transplanted whole frozen %s (not a byte-exact one-line "
                    "revert; includes its env-hardening/fsmonitor deltas): "
                    "state=%s basis=%s other=%s verdict=%s/%s rc=%s; "
                    "expected pre-fix progressing-weak row-C"
                    % (info["function"], state, tokens.get("basis"),
                       tokens.get("other_authored_commits"), word, reason, rec["rc"]),
                    run_ids=["mutation.f01.subject"],
                )
                info["observed"] = {"state": state, "basis": tokens.get("basis"),
                                    "rc": rec["rc"], "reproduced": reproduced}
            else:
                wrapper = self.write_wrapper(
                    "census-banana-mutant", self.census, "banana", "keep"
                )
                rec = self.run_oracle(
                    "mutation.f02.banana", wrapper, oracle=Path(info["mutant"])
                )
                summary = oracle_summary(rec["stdout"])
                accepted = (
                    summary == (28, 28) and rec["rc"] == 0
                    and not fail_reasons(rec["stdout"])
                )
                self.claim(
                    "R13_MUTATION_F02_RED_BEFORE",
                    MUTATION_RED if accepted else MUTATION_MISS,
                    "operability",
                    "reconstructed prefix-presence shim replaced %s "
                    "(frozen_source=null; not original bytes): matched=%s "
                    "total=%s rc=%s; expected pre-fix BANANA accepted 28/28"
                    % (info["function"],
                       summary[0] if summary else None,
                       summary[1] if summary else None, rec["rc"]),
                    run_ids=["mutation.f02.banana"],
                )
                info["observed"] = {
                    "matched": summary[0] if summary else None,
                    "total": summary[1] if summary else None,
                    "rc": rec["rc"], "accepted": accepted,
                }
            self.mutations.append(info)

    # -- driver --------------------------------------------------------------

    def run(self) -> int:
        self.prepare()
        self.mutations = []
        self.check_shonen()
        self.check_c1()
        self.check_f01()
        results = self.oracle_runs(self.census)
        self.check_f02(results)
        if self.args.mutation != "none":
            kinds = ["f01", "f02"] if self.args.mutation == "both" else [self.args.mutation]
            self.check_mutations(kinds)

        success = MUTATION_SUCCESS if self.args.mutation != "none" else (
            BASELINE_SUCCESS if self.args.baseline else STRICT_SUCCESS
        )
        hard_fail = [
            c for c in self.claims
            if c["status"] not in success and c["status"] != MUTATION_UNAVAILABLE
        ]
        mutation_unavailable = [
            c for c in self.claims if c["status"] == MUTATION_UNAVAILABLE
        ]
        if hard_fail:
            code = 1
        elif mutation_unavailable:
            # Declared verdict map: 0 clean / 1 failed / 2 could-not-evaluate.
            # A mutation that could not be built is the last class.
            code = 2
        else:
            code = 0
        # End scope: all runs and checks are complete, evidence is not written.
        self.revision_scope_end = Harness.revision_scope("end")
        try:
            self.harness_sha_end = sha256_file(Path(__file__).resolve())
        except OSError:
            self.harness_sha_end = None
        if self.harness_sha_start and self.harness_sha_end:
            self.harness_changed = self.harness_sha_start != self.harness_sha_end
        else:
            self.harness_changed = None
        self.emit(code)
        return code

    def emit(self, code: int) -> None:
        for claim in self.claims:
            print(
                "FINDING %s status=%s axis=%s observed=\"%s\""
                % (claim["id"], claim["status"], claim["axis"], claim["details"])
            )
        for rec in sorted(self.runs, key=lambda r: r["id"]):
            print(
                "RUN %s rc=%s timeout=%s duration_ms=%d stdout_sha256=%s"
                % (rec["id"], rec["rc"], str(rec["timed_out"]).lower(),
                   rec["duration_ms"], rec["stdout_sha256"][:16])
            )
        counts = {}
        for claim in self.claims:
            counts[claim["status"]] = counts.get(claim["status"], 0) + 1
        gate_state, gate_row = registry_status()
        inputs = [self.census, self.oracle, Path(self.args.shonen).resolve(),
                  *self.frozen.values()]
        owned = harness_owned_paths(self.output, self.fixture_root, inputs)
        facets = scope_facets(self.revision_scope_start,
                              self.revision_scope_end, owned, self.output)
        evidence = {
            "schema": SCHEMA,
            "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "revision": {
                "head": self.revision,
                "dirty": self.dirty,
                "dirty_source": self.dirty_source,
                "dirty_captured": self.dirty_captured,
                "source": (
                    "MORI_EVIDENCE_REVISION" if os.environ.get(
                        "MORI_EVIDENCE_REVISION") else "git rev-parse HEAD"
                ),
                # The asserted pin annotates the receipt; observed_head and the
                # start/end scope always measure real git rev-parse HEAD.
                "asserted_revision": (
                    os.environ.get("MORI_EVIDENCE_REVISION", "").strip()
                    or None),
                "observed_head": (
                    (self.revision_scope_start or {}).get("head")),
                "start": self.revision_scope_start,
                "end": self.revision_scope_end,
                **facets,
            },
            "harness": {
                "path": str(Path(__file__).resolve()),
                "executed_sha256": HARNESS_SHA_IMPORT,
                "start_sha256": self.harness_sha_start,
                "end_sha256": self.harness_sha_end,
                "changed": self.harness_changed,
            },
            "mode": "baseline" if self.args.baseline else (
                "mutation" if self.args.mutation != "none" else "strict"
            ),
            "targets": {
                "census": {"path": str(self.census), "sha256": sha256_file(self.census)},
                "oracle": {"path": str(self.oracle), "sha256": sha256_file(self.oracle)},
                "shonen": {
                    "path": str(Path(self.args.shonen).resolve()),
                    "sha256": (
                        sha256_file(Path(self.args.shonen).resolve())
                        if Path(self.args.shonen).resolve().is_file() else None
                    ),
                },
                "frozen": {
                    name: {"path": str(path), "sha256": sha256_file(path)}
                    for name, path in sorted(self.frozen.items())
                },
                "frozen_inputs": {
                    "path": str(Path(self.args.frozen_dir).resolve() / "inputs.json"),
                    "sha256": getattr(self, "inputs_sha256", None),
                },
                "frozen_pins": {
                    "state": self.frozen_pins,
                    "expected": FROZEN_PINS,
                    "base_commit": FROZEN_BASE_COMMIT,
                },
            },
            "entropy": {"shuffle_seed": self.args.seed, "run_nonce": self.args.nonce},
            "expectations": {
                "counts": {
                    "system": C1_SYSTEM_COUNTS,
                    "user": C1_USER_COUNTS,
                    "notice_only": C1_NOTICE_ONLY_COUNTS,
                },
                "severity": EXPECTED_SEVERITY,
                "oom_counters": list(OOM_COUNTERS),
                "fleet_predicate": FLEET_SUBJECT_RE.pattern,
                "selftest_cases": [case[0] for case in SELFTEST_CASES],
            },
            "claims": self.claims,
            "runs": sorted(self.runs, key=lambda r: r["id"]),
            "mutations": getattr(self, "mutations", []),
            "summary": {
                "claims": len(self.claims),
                "counts": counts,
                "exit": code,
                "gate": {
                    "name": GATE_REGISTRY_NAME,
                    "status": gate_state,
                    "registry": str(REGISTRY_FILE),
                    "row": gate_row,
                    "exit_map": {
                        "0": "clean",
                        "1": "failed",
                        "2": "could-not-evaluate",
                    },
                },
            },
        }
        evidence_path = self.output / "evidence.json"
        json_dump(evidence_path, evidence)
        print(
            "MORI_R13_REGRESSIONS: claims=%d %s exit=%d"
            % (
                len(self.claims),
                " ".join("%s=%d" % (k, v) for k, v in sorted(counts.items())),
                code,
            )
        )
        print("EVIDENCE %s" % evidence_path)
        if gate_state == "registered":
            print("GATE registered name=%s registry=%s" % (
                GATE_REGISTRY_NAME, REGISTRY_FILE))
            print("GATE-ROW %s" % gate_row)
        else:
            print("GATE %s name=%s registry=%s row=%s" % (
                gate_state, GATE_REGISTRY_NAME, REGISTRY_FILE, gate_row))


# ---------------------------------------------------------------------------
# selftest: pure parser checks + real isolated gate self-invocation
# ---------------------------------------------------------------------------


def _isolated_args(root: Path, shonen: Path, census: Path,
                   oracle: Path, frozen: Path):
    return [
        "--census", str(census),
        "--oracle", str(oracle),
        "--shonen", str(shonen),
        "--frozen-dir", str(frozen),
        "--output", str(root / "out"),
        "--timeout", "30",
        "--jobs", "1",
    ]


def run_isolated_case(case) -> tuple:
    """Run the real gate as a subprocess over an isolated tree.

    No repository target is read or run: SHONEN is a temp copy of the canonical
    seed, the census/oracle are tiny stubs, and every fixture lives under the
    fresh temp root. The case asserts the process exit code, the stable finding
    ids, and the absence of the false "GATE not-registered" identity.
    """
    case_id, expected_rc, required, forbidden = case
    root = Path(tempfile.mkdtemp(prefix="r13-selftest-"))
    try:
        shonen = root / "SHONEN.md"
        shonen.write_bytes(CANONICAL_SHONEN.encode())
        census = root / "census-stub.sh"
        write_exec(census, "#!/usr/bin/env bash\nexit 0\n")
        oracle = root / "oracle-stub.sh"
        write_exec(
            oracle,
            "#!/usr/bin/env bash\n"
            "printf 'MORI_SILENCE_CASES: matched=0 total=28\\n'\n"
            "exit 1\n",
        )
        if case_id.endswith("manifest-tamper"):
            frozen = root / "frozen"
            frozen.mkdir()
            write_exec(frozen / "mori-census.sh", "#!/usr/bin/env bash\nexit 0\n")
            write_exec(
                frozen / "mori-silence-cases.sh",
                "#!/usr/bin/env bash\nexit 1\n",
            )
            (frozen / "inputs.json").write_text(
                json.dumps({
                    "base_commit": FROZEN_BASE_COMMIT,
                    "sha256": {
                        "mori-census.sh": "0" * 64,
                        "mori-silence-cases.sh": sha256_file(
                            frozen / "mori-silence-cases.sh"),
                    },
                }) + "\n",
                encoding="utf-8",
            )
        else:
            frozen = root / "no-frozen"
        argv = [sys.executable, str(Path(__file__).resolve())]
        argv += _isolated_args(root, shonen, census, oracle, frozen)
        env = {
            "PATH": "/usr/bin:/bin",
            "HOME": os.environ.get("HOME", "/tmp"),
            "TMPDIR": str(root),
            "LANG": "C",
            "LC_ALL": "C",
            "TZ": "UTC",
        }
        try:
            proc = subprocess.run(
                argv,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=env,
                cwd=str(root),
                timeout=180,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            return False, "spawn failed: %s" % exc
        out = proc.stdout or ""
        problems = []
        if proc.returncode != expected_rc:
            problems.append("rc=%s!=%s" % (proc.returncode, expected_rc))
        for fid in required:
            if not re.search(r"(?m)^FINDING %s status=" % re.escape(fid), out):
                problems.append("missing:%s" % fid)
        for fid in forbidden:
            if re.search(r"(?m)^FINDING %s status=" % re.escape(fid), out):
                problems.append("forbidden:%s" % fid)
        gate_lines = [ln for ln in out.splitlines() if ln.startswith("GATE ")]
        if not gate_lines:
            problems.append("no-GATE-line")
        if any("not-registered" in ln for ln in gate_lines):
            problems.append("false-not-registered")
        if CANARY in out or "<canary-redacted>" in out:
            problems.append("canary-leak")
        if MESSAGE_KEY_RE.search(out) or MESSAGE_EQ_RE.search(out):
            problems.append("message-leak")
        evidence_path = root / "out" / "evidence.json"
        if not evidence_path.is_file():
            problems.append("no-evidence")
        else:
            try:
                summary = json.loads(
                    evidence_path.read_text(encoding="utf-8")).get("summary", {})
            except (OSError, ValueError):
                summary = {}
            if summary.get("exit") != expected_rc:
                problems.append(
                    "evidence-exit=%s!=%s" % (summary.get("exit"), expected_rc))
        return (not problems), ",".join(problems) or "ok"
    finally:
        shutil.rmtree(root, ignore_errors=True)


def selftest() -> int:
    failures = []
    checks = []

    def check(label, cond):
        checks.append(label)
        if not cond:
            failures.append(label)

    ok = "MORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=0 surfaces=8)"
    drift = "MORI_CENSUS: DRIFT (findings=1 drift=1 unavailable=0 surfaces=8)"
    check("clean-ok", verdict_roll(ok, 0)[:2] == ("CLEAN", "ok"))
    check("drift-ok", verdict_roll(drift, 1)[:2] == ("DRIFT", "ok"))
    check("missing", verdict_roll("no roll", 0)[1] == "missing")
    check("duplicate", verdict_roll(ok + "\n" + ok, 0)[1].startswith("duplicate"))
    banana = ok.replace("CLEAN", "BANANA")
    check("banana-malformed", verdict_roll(banana, 0)[1] == "malformed")
    check("clean-rc1", verdict_roll(ok, 1)[1].startswith("inconsistent"))
    check("drift-rc0", verdict_roll(drift, 0)[1].startswith("inconsistent"))
    emitted = findings("FINDING EXAMPLE severity=info obs=count=2 scope=system ts=x")
    check(
        "emitted-finding-schema",
        bool(emitted) and emitted[0][:3]
        == ("EXAMPLE", "info", {"count": "2", "scope": "system", "ts": "x"}),
    )
    check(
        "lane-row",
        lane_row(
            "SURFACE lane.kagi: progressing (lane=kagi round=7 basis=row-A "
            "subject_commits=yes; ts=x)"
        )[0] == "progressing",
    )
    scoped_out = (
        "SURFACE journal.user: ok (scope=user kernel_oom_notice=0 "
        "oomd_notice=0 coredump_notice=0 segfault_signal11=0 "
        "unit_sigkill_record=0 unit_failure_record=0; boot=0123; "
        "unit_signal=0 unit_oom=0; rc=0; ts=x)\n"
        "SURFACE journal.system: ok (scope=system kernel_oom_notice=2 "
        "oomd_notice=1 coredump_notice=3 segfault_signal11=3 "
        "unit_sigkill_record=0 unit_failure_record=0; boot=0123; "
        "unit_signal=0 unit_oom=0; rc=0; ts=x)\n"
    )
    rows = surface_rows(scoped_out)
    check("scoped-two-rows", set(rows) == {"user", "system"})
    check("scoped-user-zero", rows.get("user", ("", {}))[1].get("kernel_oom_notice") == "0")
    check("scoped-system-count", rows.get("system", ("", {}))[1].get("kernel_oom_notice") == "2")
    check("scoped-boot", rows.get("user", ("", {}))[1].get("boot") == "0123")
    check("token-int", _token_int({"count": "3"}, "count") == 3)
    check("token-int-unavailable", _token_int({"count": "unavailable:rc-1"}, "count") is None)
    check("token-int-absent", _token_int({}, "count") is None)
    check(
        "fleet-predicate",
        bool(FLEET_SUBJECT_RE.search("shokunin-watchdog.service"))
        and bool(FLEET_SUBJECT_RE.search("UFO-SIGHTING.service"))
        and not FLEET_SUBJECT_RE.search("pipewire-pulse.service"),
    )
    check(
        "pass-cases",
        pass_cases("PASS silent-open (state=silent via lane finding=1 rc=1 nonce=1)\n")
        == {"silent-open": "silent"},
    )
    check(
        "pass-cases-stateless",
        pass_cases("PASS readonly-no-mutation\n") == {"readonly-no-mutation": ""},
    )
    check("count-value-int", count_value({"count": "3"}) == 3)
    check("count-value-bad", count_value({"count": "unavailable"}) == 0)
    check("summary", oracle_summary("MORI_SILENCE_CASES: matched=28 total=28\n") == (28, 28))
    check(
        "fail-reasons",
        fail_reasons("FAIL x: MORI_CENSUS verdict duplicate (2 lines)\n")
        == {"duplicate"},
    )
    witness = "".join(
        ("    " + ln) if ln.strip("\n") else ln
        for ln in CANONICAL_SHONEN.splitlines(keepends=True)
    )
    check("shonen-constant", sha256_bytes(CANONICAL_SHONEN.encode()) == CANONICAL_SHONEN_SHA256)
    check("shonen-witness", witness.encode() != CANONICAL_SHONEN.encode())
    check(
        "shonen-witness-diff",
        Harness._shonen_diff(witness.encode(), CANONICAL_SHONEN.encode()) is not None,
    )
    check(
        "shonen-canonical-diff-none",
        Harness._shonen_diff(CANONICAL_SHONEN.encode(), CANONICAL_SHONEN.encode()) is None,
    )
    # Wrapper shell fragments must round-trip through shlex quoting unchanged.
    check("shell-quote", shlex.quote("a b'c") == "'a b'\"'\"'c'")
    # Registry matcher (pure) and committed case table.
    sample_row = (
        "| r13 regressions | gate | `python3 tools/mori-round13-regressions.py "
        "--output <dir>` | 0 clean · 1 failed · 2 could-not-evaluate | "
        "`--selftest` | `FROZEN_PINS` | `--output` | mori |"
    )
    check(
        "registry-row-present",
        registry_row_status("| name |\n" + sample_row + "\n")[0] == "registered",
    )
    check(
        "registry-row-absent",
        registry_row_status("| name |\n| census | gate |\n")[0]
        == "registration-missing",
    )
    check(
        "frozen-pin-shape",
        set(FROZEN_PINS) == {
            "mori-census.sh", "mori-silence-cases.sh", "inputs.json"}
        and all(re.fullmatch(r"[0-9a-f]{64}", value)
                for value in FROZEN_PINS.values()),
    )
    try:
        verify_frozen_pins(Path(DEFAULT_FROZEN).resolve())
        pins_ok = True
    except SnapshotTampered:
        pins_ok = False
    check("frozen-pins-match-default", pins_ok)
    check(
        "selftest-cases-committed",
        len(SELFTEST_CASES) == 2
        and len({case[0] for case in SELFTEST_CASES}) == len(SELFTEST_CASES),
    )
    case_failures = []
    for case in SELFTEST_CASES:
        case_ok, detail = run_isolated_case(case)
        print("SELFTEST: case %s %s %s" % (
            case[0], "ok" if case_ok else "bad", detail))
        if not case_ok:
            case_failures.append(case[0])
    if failures or case_failures:
        print("SELFTEST: fail pure=%s cases=%s" % (
            " ".join(failures) or "none", " ".join(case_failures) or "none"))
        return 1
    print("SELFTEST: pass checks=%d cases=%d" % (
        len(checks), len(SELFTEST_CASES)))
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def write_snapshot_evidence(args, exc) -> None:
    """Retain the tamper observation under the explicit --output path."""
    if not args.output:
        return
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)
    frozen_dir = Path(args.frozen_dir).resolve()
    inputs_path = frozen_dir / "inputs.json"
    targets = {}
    pairs = (
        ("census", args.census or (frozen_dir / "mori-census.sh" if args.baseline
                                   else DEFAULT_CENSUS)),
        ("oracle", args.oracle or (frozen_dir / "mori-silence-cases.sh" if args.baseline
                                   else DEFAULT_ORACLE)),
    )
    for label, raw in pairs:
        path = Path(raw).resolve()
        targets[label] = {
            "path": str(path),
            "sha256": sha256_file(path) if path.is_file() else None,
        }
    expected = {}
    if inputs_path.is_file():
        try:
            expected = json.loads(inputs_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            expected = {"error": "unreadable inputs.json"}
    try:
        scope = Harness.revision_scope("setup")
        revision, dirty = Harness.revision_from_scope(scope)
    except SetupError:
        scope, revision, dirty = None, None, None
    gate_state, gate_row = registry_status()
    evidence = {
        "schema": SCHEMA,
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "revision": {
            "head": revision,
            "dirty": dirty,
            "dirty_source": Harness.dirty_source_label(),
            "dirty_captured": (scope or {}).get("dirty"),
            "asserted_revision": (
                (scope or {}).get("asserted_revision")),
            "scope": scope,
        },
        "mode": "setup",
        "finding": "snapshot_tampered",
        "observed": str(exc),
        "targets": targets,
        "frozen_inputs": {
            "path": str(inputs_path),
            "sha256": sha256_file(inputs_path) if inputs_path.is_file() else None,
            "declared": expected,
        },
        "summary": {
            "claims": 1,
            "counts": {"fail": 1},
            "exit": 2,
            "gate": {
                "name": GATE_REGISTRY_NAME,
                "status": gate_state,
                "registry": str(REGISTRY_FILE),
                "row": gate_row,
                "exit_map": {
                    "0": "clean",
                    "1": "failed",
                    "2": "could-not-evaluate",
                },
            },
        },
    }
    path = out / "evidence.json"
    json_dump(path, evidence)
    print("EVIDENCE %s" % path)
    if gate_state == "registered":
        print("GATE registered name=%s registry=%s" % (
            GATE_REGISTRY_NAME, REGISTRY_FILE))
    else:
        print("GATE %s name=%s registry=%s row=%s" % (
            gate_state, GATE_REGISTRY_NAME, REGISTRY_FILE, gate_row))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Round-13 regression gate (registered in this lane's SKILL.md; "
            "C1 semantics migrated to the restored round-14 OOM alarm and "
            "structured fleet routing)."
        ),
        epilog=(
            "Mutation provenance: f01 transplants the WHOLE frozen grade_lane "
            "(not a membership-lines-only or byte-exact one-line revert; it "
            "includes the frozen body's environment-hardening deltas). f02 "
            "replaces verdict_grade with a RECONSTRUCTED prefix-presence shim "
            "(frozen_source=null), not original function bytes; it proves the "
            "single validation locus is sufficient for BANANA acceptance. The "
            "original frozen bytes under --baseline remain the primary "
            "historical before evidence."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--census", help="census under test (default tools/mori-census.sh)")
    ap.add_argument("--oracle", help="oracle under test (default tools/mori-silence-cases.sh)")
    ap.add_argument("--output", help="required evidence directory (created if absent)")
    ap.add_argument("--baseline", action="store_true",
                    help="record frozen pre-fix defects; never marks the new contract pass")
    ap.add_argument("--mutation", choices=("none", "f01", "f02", "both"), default="none",
                    help="after the strict suite, build the isolated mutant: f01 "
                         "whole frozen grade_lane transplant; f02 reconstructed "
                         "prefix-presence shim (neither is original-byte restoration)")
    ap.add_argument("--shonen", default=str(DEFAULT_SHONEN),
                    help="promotion seed to compare (default SHONEN.md)")
    ap.add_argument("--frozen-dir", default=str(DEFAULT_FROZEN),
                    help="frozen original scripts + inputs.json")
    ap.add_argument("--timeout", type=int, default=120,
                    help="per-run timeout seconds (default 120)")
    ap.add_argument("--jobs", type=int, default=3,
                    help="parallel oracle wrapper runs (default 3)")
    ap.add_argument("--seed", type=int, default=1313,
                    help="pinned MORI_SHUFFLE_SEED for reproducible order")
    ap.add_argument("--nonce", type=int, default=1313,
                    help="pinned MORI_RUN_NONCE for reproducible fixtures")
    ap.add_argument("--keep-fixtures", action="store_true",
                    help="keep fixture trees under the output dir for inspection")
    ap.add_argument("--selftest", action="store_true",
                    help="pure parser checks plus real isolated gate "
                         "self-invocation (asserts exit code and stable finding ids)")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if not args.output:
        ap.error("--output is required (explicit evidence path)")
    if args.baseline and args.mutation != "none":
        ap.error("--baseline and --mutation are separate measurements")
    if args.timeout <= 0 or args.jobs <= 0:
        ap.error("--timeout and --jobs must be positive")

    harness = Harness(args)
    try:
        code = harness.run()
    except SnapshotTampered as exc:
        print("FINDING R13_SNAPSHOT_TAMPERED status=fail axis=operability "
              "observed=\"%s\"" % one_line(exc))
        print("MORI_R13_REGRESSIONS: setup snapshot_tampered exit=2")
        try:
            write_snapshot_evidence(args, exc)
        except OSError as werr:
            print("mori-round13-regressions: evidence write failed: %s" % werr,
                  file=sys.stderr)
        code = 2
    except SetupError as exc:
        print("mori-round13-regressions: setup: %s" % exc, file=sys.stderr)
        code = 2
    except KeyboardInterrupt:
        print("mori-round13-regressions: interrupted", file=sys.stderr)
        code = 2
    except Exception as exc:  # noqa: BLE001 - gate contract: never a false fail
        # An unexpected harness error is could-not-evaluate (2), never failed
        # (1): the declared verdict map must not be forged by a traceback.
        print(
            "mori-round13-regressions: internal error (could-not-evaluate): "
            "%s: %s" % (type(exc).__name__, exc),
            file=sys.stderr,
        )
        code = 2
    finally:
        harness.cleanup()
    return code


if __name__ == "__main__":
    sys.exit(main())
