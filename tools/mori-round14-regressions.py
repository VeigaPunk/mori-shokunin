#!/usr/bin/env python3
"""mori-round14-regressions.py — isolated behavioral gate for the round-14 C1 repair.

WHAT THIS GATE IS

  A verdict-producing regression gate, not an evidence-only harness. It runs
  synthetic journal streams through two census snapshots with exactly the same
  fixtures and the same strict expectations:

    red   .ufo/waves/round-14/frozen/mori-census.sh (pinned SHA-256 in this file)
    green tools/mori-census.sh (the repaired census)

  The red snapshot digest is a constant here, not a manifest read (a sibling
  manifest can be edited with the frozen file). The bytes are read once,
  hashed, copied into the fixture tree, read back, and executed from that copy.
  Every emitted FINDING's script_sha256 must equal the executed copy's digest.
  `--census` names the snapshot under test; `--frozen` names the red control.
  When both name the same bytes the gate is a red-before run: the defective
  snapshot fails and the gate exits 1.

CLAIMS (stable ids; one FINDING line each)

  R14_BASELINE_EMPTY                 empty streams -> CLEAN rc0, six zeros + unit zeros
  R14_OOM_ALARM_USER                 user kernel OOM notice -> one global OOM_KILL_JOURNAL crit
  R14_OOM_ALARM_SYSTEM               system kernel OOM notice -> same global alarm
  R14_UNIT_OOM_KILL                  fleet UNIT_RESULT=oom-kill -> global alarm user_unit_oom
  R14_UNIT_OOM_NONFLEET              nonfleet oom-kill -> alarm + OUT_OF_SCOPE owner=tsukuroi
  R14_UNIT_OOM_SYSTEM                system oom-kill -> global alarm system_unit_oom
  R14_UNIT_OOM_MISSING_SUBJECT       oom-kill without UNIT/USER_UNIT -> alarm + raw count + unattributed
  R14_UNIT_OOM_SUBJECT_ARRAY         USER_UNIT array -> alarm + raw count + unattributed
  R14_UNIT_FAILED_FLEET              fleet failed -> UNIT_FAILURE_JOURNAL info owner=mori, CLEAN
  R14_UNIT_FAILED_NONFLEET           nonfleet failed -> UNIT_FAILURE_OUT_OF_SCOPE info owner=tsukuroi
  R14_UNIT_FAILED_UNKNOWN            only _SYSTEMD_UNIT emitter -> UNIT_FAILURE_UNATTRIBUTED_JOURNAL
  R14_UNIT_VALID_ESCAPE_KNOWN        valid \\xHH unit escape stays a known subject
  R14_UNIT_INVALID_ESCAPE_UNKNOWN    invalid escape -> unknown, never fleet; raw count kept
  R14_USER_UNIT_IN_SYSTEM            USER_UNIT subject in system scope -> fleet classification
  R14_SUBJECT_AMBIGUOUS              UNIT and USER_UNIT both present -> unattributed, never nonfleet
  R14_UNIT_RESULT_MISSING            UNIT_RESULT absent -> raw count + unit_oom_result_unknown
  R14_UNIT_RESULT_ARRAY_UNKNOWN      array UNIT_RESULT -> unknown result, not oom evidence
  R14_UNIT_PARTITION                 fleet+nonfleet+unknown == raw unit_failure_record
  R14_SIGKILL_WARN                   user unit-process SIGKILL -> KILL_SIGNAL_JOURNAL warn, DRIFT
  R14_UNIT_SIGNAL_WARN               user UNIT_RESULT=signal -> KILL_SIGNAL warn, DRIFT, no OOM
  R14_UNIT_SIGNAL_SYSTEM_INFO        system UNIT_RESULT=signal -> routing info only, CLEAN
  R14_FANOUT_ONE_SIGNAL_PER_KIND     fan-out: one global OOM line + one SIGKILL line, drift=2
  R14_SCOPED_PARITY                  six raw counts per scope unchanged; never summed
  R14_SCOPE_NOT_SUMMED               user 3 / system 5 stay separate fields, never summed
  R14_NOTICE_INFO_CLEAN              oomd+coredump+segfault only -> CLEAN rc0, no OOM alarm
  R14_QUERY_ERROR_UNAVAILABLE        journalctl rc5 -> unavailable:rc-5, never a fake zero
  R14_PARTIAL_ERROR_SYSTEM_ALARMS    user rc1 + system notice -> global alarm still fires
  R14_UNIT_QUERY_ERROR_KERNEL_ALARM  unit query rc1 + user notice -> kernel path alarms
  R14_STDERR_UNAVAILABLE             producer stderr -> unavailable:stderr-nonempty
  R14_MALFORMED_UNAVAILABLE          malformed JSON -> unavailable:malformed-json
  R14_WRONG_BOOT_UNAVAILABLE         foreign _BOOT_ID -> unavailable:boot-mismatch
  R14_MULTI_BOOT_UNAVAILABLE         several boots -> unavailable:multi-boot
  R14_IGNORE_FILTERS_INVALID         kernel query returns another class -> record-invalid
  R14_SEC_DUP_MSGID_MIXED            valid OOM + MESSAGE_ID array -> record-invalid, no fake zero
  R14_SEC_UNIT_CANARY                newline/token unit canary never reaches output
  R14_MESSAGE_CANARY                 MESSAGE bytes/unit subject never emitted; no MESSAGE request
  R14_TEXT_ONLY_NOT_ADMITTED         MESSAGE text alone never counts as OOM (Q15)
  R14_TIMEOUT_UNAVAILABLE            producer timeout -> unavailable:timeout, no fake zero
  R14_FROZEN_CONTROL                 every required red case fails on the pinned frozen bytes
  R14_SNAPSHOT_TAMPERED              pinned frozen digest mismatch (setup, rc2)

SETTLED r14 SCHEMA PINS (L1 final ruling, relayed by CensusRepair)

  OOM: exactly ONE global FINDING OOM_KILL_JOURNAL severity=crit per census
  when any of user_notice/system_notice/user_unit_oom/system_unit_oom > 0.
  No count= total and no summed field. The line carries, once:
    user_notice=<n|unavailable:reason> system_notice=<...>
    user_unit_oom=<...> system_unit_oom=<...>
    user_unit_oom_result_unknown=<...> system_unit_oom_result_unknown=<...>
  Each field byte-equals that scope's SURFACE token (kernel_oom_notice /
  unit_oom / unit_oom_result_unknown). One alarm line = drift +1; drift counts
  alarm lines, never record counts.

  SURFACE journal.user / journal.system keep, in order:
    kernel_oom_notice oomd_notice coredump_notice segfault_signal11
    unit_sigkill_record unit_failure_record
  and add on the same row, in order:
    unit_fleet unit_nonfleet unit_unknown unit_missing unit_ambiguous
    unit_malformed unit_oom unit_oom_fleet unit_oom_nonfleet
    unit_oom_subject_unknown unit_oom_result_unknown unit_signal
  When the unit query is ok: fleet+nonfleet+unknown == unit_failure_record;
  unit_oom and unit_signal are subsets and are never deducted. When the unit
  query is unavailable, every added token reads unavailable:<same reason>.
  The six raw counts are unchanged from r13.

  Findings:
    UNIT_FAILURE_JOURNAL severity=info count=A scope=user subject=fleet owner=mori
    UNIT_FAILURE_JOURNAL_SYSTEM (same, scope=system)
    UNIT_FAILURE_OUT_OF_SCOPE severity=info count=B scope=user
      subject=nonfleet owner=tsukuroi
    UNIT_FAILURE_OUT_OF_SCOPE_SYSTEM (same, scope=system)
    UNIT_FAILURE_UNATTRIBUTED_JOURNAL severity=info count=N scope=user|system
      owner=unresolved reason=subject-metadata-unknown
      (ONE literal id in both scopes; no _SYSTEM alias)
  KILL_SIGNAL_JOURNAL warn (user only) fires for user process SIGKILL records OR
  user UNIT_RESULT=signal records; its fields are process_sigkill= and
  user_unit_signal= (separate, never summed). System signal results stay info.
  Both UNIT and USER_UNIT present (even equal) => unattributed, never fatal.
  Non-string or missing UNIT_RESULT => unit_oom_result_unknown, not oom.
  Retired: KERNEL_OOM_NOTICE_JOURNAL_USER, KERNEL_OOM_NOTICE_JOURNAL_SYSTEM.
  Only the global crit OOM line and the user SIGKILL/signal warn flip the roll.

  Retained control, not a green waiver: R14_SEC_DUP_MSGID_MIXED shows the
  inherited all-or-nothing validation grades a stream containing one valid OOM
  record plus a malformed MESSAGE_ID record as record-invalid/unavailable. It
  is honest (never a fake zero) but it can silence a valid alarm; that residual
  limitation is named in the seat report for L1 routing.

CONTRACT

  Exit 0  every claim satisfied (green snapshot) and the frozen control showed
          the required red cases failing.
  Exit 1  a claim failed, or the frozen control did not reproduce the defects.
  Exit 2  usage/setup/pin error.

  No live journal is read. Every journalctl call resolves to a generated stub;
  a PATH tripwire records any accidental bare `journalctl`. Fixture roots are
  opaque and live under --output, never under the repository. The host
  environment is not inherited: each census run gets an explicit env built by
  census_env(). Canary bytes are checked on the RAW capture and redacted from
  every retained artifact. The journal stub projects each record onto the
  requested --output-fields (plus the four always-printed metadata fields), so
  a census that never requests UNIT/USER_UNIT/UNIT_RESULT cannot classify them
  and goes red.

Usage

  python3 tools/mori-round14-regressions.py --output DIR
  python3 tools/mori-round14-regressions.py --census PATH --output DIR
  python3 tools/mori-round14-regressions.py --census .ufo/waves/round-14/frozen/mori-census.sh --output DIR   # red-before: exit 1
  python3 tools/mori-round14-regressions.py --census tools/mori-census.sh \
      --frozen .ufo/waves/round-14/frozen/mori-census.sh --output DIR
  python3 tools/mori-round14-regressions.py --selftest
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

SCHEMA = "mori-round14-regressions-v1"
REPO = Path(__file__).resolve().parent.parent
DEFAULT_CENSUS = REPO / "tools/mori-census.sh"
DEFAULT_FROZEN_DIR = REPO / ".ufo/waves/round-14/frozen"
DEFAULT_FROZEN = DEFAULT_FROZEN_DIR / "mori-census.sh"

# Pinned by GateConformance/L1: the red input is these exact bytes. The sibling
# inputs.json/expected.json are cross-checked but never trusted as the source.
PINNED_BASE_COMMIT = "dbe85009253c092fe50e4e93056fceeae273ec31"
PINNED_SHA256 = {
    "mori-census.sh": "39abda0a67028575d888d9157b8548dec0b4944c3d8c165691e88ab657fc3985",
    "mori-silence-cases.sh": "34cd5770889ec6e7521b477aa9976cece7a64e07b83774c12ce2aea73161abfa",
}

NOW_EPOCH = 1700000000
LAUNCH_EPOCH = 1699998000
LANE = "kagi"
ROUND = "7"
JOURNAL_BOOT = "0123456789abcdef0123456789abcdef"
FOREIGN_BOOT_A = "ffffffffffffffffffffffffffffffff"
FOREIGN_BOOT_B = "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"

KERNEL_ID = "fe6faa94e7774663a0da52717891d8ef"
OOMD_ID = "d989611b15e44c9dbf31e3c81256e4ed"
COREDUMP_ID = "fc2e22bc6ee647b6b90729ab34a250b1"
SIGKILL_ID = "98e322203f7a4ed290d09fe03c09fe15"
FAILURE_ID = "d9b373ed55a64feb8242e02dbe79a49c"

FLEET_UNIT = "kagi-shokunin.service"
NONFLEET_UNIT = "pipewire-pulse.service"
EMITTER_UNIT = "kagi-shokunin.service"

CANARY = "R14-SYNTHETIC-JOURNAL-MESSAGE-CANARY"
UNIT_CANARY = "R14-UNIT-SUBJECT-CANARY"
STDERR_CANARY = "R14-SYNTHETIC-STDERR-CANARY"
UNIT_VALID_CANARY = "r14-valid-subject-canary"
VALID_CANARY_UNIT = UNIT_VALID_CANARY + ".service"
CANARIES = (CANARY, UNIT_CANARY, STDERR_CANARY, UNIT_VALID_CANARY)

CLASS_NAMES = (
    "kernel_oom_notice",
    "oomd_notice",
    "coredump_notice",
    "segfault_signal11",
    "unit_sigkill_record",
    "unit_failure_record",
)
UNIT_TOKENS = (
    "unit_fleet",
    "unit_nonfleet",
    "unit_unknown",
    "unit_missing",
    "unit_ambiguous",
    "unit_malformed",
    "unit_oom",
    "unit_oom_fleet",
    "unit_oom_nonfleet",
    "unit_oom_subject_unknown",
    "unit_oom_result_unknown",
    "unit_signal",
)

OOM_ID = "OOM_KILL_JOURNAL"
OOM_FIELDS = (
    ("user_notice", "user", "kernel_oom_notice"),
    ("system_notice", "system", "kernel_oom_notice"),
    ("user_unit_oom", "user", "unit_oom"),
    ("system_unit_oom", "system", "unit_oom"),
)
OOM_RESULT_FIELDS = (
    ("user_unit_oom_result_unknown", "user", "unit_oom_result_unknown"),
    ("system_unit_oom_result_unknown", "system", "unit_oom_result_unknown"),
)
FLEET_ID = {
    "user": "UNIT_FAILURE_JOURNAL",
    "system": "UNIT_FAILURE_JOURNAL_SYSTEM",
}
OUT_ID = {
    "user": "UNIT_FAILURE_OUT_OF_SCOPE",
    "system": "UNIT_FAILURE_OUT_OF_SCOPE_SYSTEM",
}
# L1 final: ONE literal in both scopes, distinguished by scope=user|system.
UNKNOWN_ID = "UNIT_FAILURE_UNATTRIBUTED_JOURNAL"
KILL_ID = "KILL_SIGNAL_JOURNAL"
KILL_SYSTEM_ID = "KILL_SIGNAL_JOURNAL_SYSTEM"
RETIRED_PREFIX = "KERNEL_OOM_NOTICE_JOURNAL"
FORBID_OOM = (OOM_ID,)

VERDICT_RE = re.compile(
    r"^MORI_CENSUS: (CLEAN|DRIFT) "
    r"\(findings=([0-9]+) drift=([0-9]+) unavailable=([0-9]+) surfaces=([0-9]+)\)$"
)
FINDING_RE = re.compile(r"^FINDING (\w+) severity=(\w+) obs=(.*)$", re.M)
SCRIPT_SHA_RE = re.compile(r"script_sha256=([0-9a-f]{64})")
SURFACE_SCOPED_RE = re.compile(
    r"^SURFACE journal\.(user|system): (\S+) \((.*)\)\s*$", re.M
)
BARE_JOURNAL_RE = re.compile(r"^SURFACE journal: ", re.M)
TOKEN_RE = re.compile(r"([A-Za-z0-9_.:+-]+)=([^\s;]*)")
MESSAGE_KEY_RE = re.compile(r'"MESSAGE"\s*:')
MESSAGE_EQ_RE = re.compile(r"(?<!_)MESSAGE=")

FROZEN_RED_REQUIRED = (
    "R14_OOM_ALARM_USER",
    "R14_OOM_ALARM_SYSTEM",
    "R14_UNIT_OOM_KILL",
    "R14_UNIT_OOM_NONFLEET",
    "R14_UNIT_OOM_SYSTEM",
    "R14_UNIT_OOM_BOTH_SCOPES",
    "R14_UNIT_OOM_MISSING_SUBJECT",
    "R14_UNIT_OOM_SUBJECT_ARRAY",
    "R14_UNIT_FAILED_FLEET",
    "R14_UNIT_FAILED_NONFLEET",
    "R14_UNIT_FAILED_UNKNOWN",
    "R14_UNIT_VALID_ESCAPE_KNOWN",
    "R14_UNIT_INVALID_ESCAPE_UNKNOWN",
    "R14_UNIT_SUBJECT_NULL_UNKNOWN",
    "R14_USER_UNIT_IN_SYSTEM",
    "R14_SUBJECT_AMBIGUOUS",
    "R14_UNIT_RESULT_MISSING",
    "R14_UNIT_RESULT_ARRAY_UNKNOWN",
    "R14_UNIT_RESULT_NOT_OOM_STRINGS",
    "R14_UNIT_PARTITION",
    "R14_FANOUT_ONE_SIGNAL_PER_KIND",
    "R14_SCOPED_PARITY",
    "R14_SCOPE_NOT_SUMMED",
    "R14_PARTIAL_ERROR_SYSTEM_ALARMS",
    "R14_UNIT_QUERY_ERROR_KERNEL_ALARM",
    "R14_UNIT_SIGNAL_WARN",
    "R14_UNIT_SIGNAL_SYSTEM_INFO",
    "R14_SEC_VALID_UNIT_CANARY",
    "R14_MESSAGE_CANARY",
)


# ---------------------------------------------------------------------------
# utilities
# ---------------------------------------------------------------------------


class SetupError(Exception):
    """Usage or fixture setup failure: exit 2."""


class SnapshotTampered(Exception):
    """Pinned frozen bytes do not match the in-script digest: exit 2."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def redact(text: str) -> str:
    out = text
    for canary in CANARIES:
        out = out.replace(canary, "<canary-redacted>")
    return out


def one_line(text, limit=520) -> str:
    cleaned = " ".join(redact(str(text)).split())
    if len(cleaned) > limit:
        cleaned = cleaned[: limit - 3] + "..."
    return cleaned


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
# census output parsing
# ---------------------------------------------------------------------------


def verdict_roll(out: str, rc):
    """Return (word|None, reason, counts dict)."""
    counts = {"findings": 0, "drift": 0, "unavailable": 0, "surfaces": 0}
    lines = [ln for ln in out.splitlines() if ln.startswith("MORI_CENSUS:")]
    if not lines:
        return None, "missing", counts
    if len(lines) > 1:
        return None, "duplicate(%d)" % len(lines), counts
    m = VERDICT_RE.match(lines[0])
    if not m:
        return None, "malformed", counts
    word = m.group(1)
    counts = {
        "findings": int(m.group(2)),
        "drift": int(m.group(3)),
        "unavailable": int(m.group(4)),
        "surfaces": int(m.group(5)),
    }
    if (word, rc) not in (("CLEAN", 0), ("DRIFT", 1)):
        return word, "inconsistent(word=%s rc=%s)" % (word, rc), counts
    return word, "ok", counts


def surface_rows(out: str):
    """Map scope -> (state, tokens) from SURFACE journal.<scope> rows."""
    rows = {}
    for m in SURFACE_SCOPED_RE.finditer(out):
        rows[m.group(1)] = (m.group(2), dict(TOKEN_RE.findall(m.group(3))))
    return rows


def findings(out: str):
    """Return [{'id','sev','tokens','obs','script_sha256'}] in file order."""
    rows = []
    for m in FINDING_RE.finditer(out):
        rest = m.group(3)
        sha = SCRIPT_SHA_RE.search(rest)
        rows.append(
            {
                "id": m.group(1),
                "sev": m.group(2),
                "tokens": dict(TOKEN_RE.findall(rest)),
                "obs": rest,
                "script_sha256": sha.group(1) if sha else None,
            }
        )
    return rows


def count_ids(rows, ids) -> int:
    return sum(1 for r in rows if r["id"] in ids)


# ---------------------------------------------------------------------------
# fixture builders (self-contained; r13 build_common/census_env patterns)
# ---------------------------------------------------------------------------


def journal_stub_body(base: Path, mode: str) -> str:
    """Generated synthetic journalctl (never opens the host journal).

    Emulates the structured subset the census may request: --user/--system,
    -o json, --output-fields, and exact FIELD=value filters. Modes:
      honor          filter records, honor --output-fields plus the four
                     always-printed metadata fields
      leak           ignore --output-fields and force MESSAGE=<canary>
      ignore-filters return every record of the scope regardless of filters
      dup-kernel     ignore filters only for the kernel MESSAGE_ID query (a
                     mixed valid + malformed-MESSAGE_ID stream)
      malformed      emit a non-JSON line with rc 0
      text           non-JSON calls print journal/text.txt; JSON calls emit
                     records (which may lack MESSAGE_ID)
      hang           sleep past the census timeout
    Per-scope <scope>.rc and <scope>.stderr files drive producer failures.
    """
    template = r'''#!/usr/bin/env python3
import json, os, re, sys, time
BASE = @BASE@
MODE = @MODE@
CANARY = @CANARY@
KERNEL_ID = @KERNEL_ID@
FAILURE_ID = @FAILURE_ID@
ALWAYS = ("__CURSOR", "__REALTIME_TIMESTAMP", "__MONOTONIC_TIMESTAMP", "_BOOT_ID")
args = sys.argv[1:]
scope = "system"
fields = None
want = []
json_out = False
grep = None
i = 0
while i < len(args):
    a = args[i]
    if a == "--user":
        scope = "user"
    elif a == "--system":
        scope = "system"
    elif a == "-o":
        i += 1
        if i < len(args) and args[i] == "json":
            json_out = True
    elif a.startswith("--output-fields="):
        fields = [f for f in a.split("=", 1)[1].split(",") if f]
    elif a.startswith("--grep="):
        grep = a.split("=", 1)[1]
    elif a in ("--no-pager", "-b", "--boot", "--quiet", "-q"):
        pass
    elif "=" in a and not a.startswith("-"):
        k, v = a.split("=", 1)
        want.append((k, v))
    i += 1
try:
    with open(os.path.join(BASE, "journal", "argv.log"), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(args) + "\n")
except OSError:
    pass
if MODE == "hang":
    time.sleep(30)
    sys.exit(0)
if MODE == "unit-rc" and any(
        k == "MESSAGE_ID" and v == FAILURE_ID for k, v in want):
    urc_path = os.path.join(BASE, "journal", scope + ".unit_rc")
    if os.path.exists(urc_path):
        try:
            urc = int(open(urc_path, encoding="utf-8").read().strip() or "0")
        except ValueError:
            urc = 0
        if urc != 0:
            sys.stderr.write("synthetic unit query failure scope=%s rc=%d\n"
                             % (scope, urc))
            sys.exit(urc)
rc_path = os.path.join(BASE, "journal", scope + ".rc")
if os.path.exists(rc_path):
    try:
        rc = int(open(rc_path, encoding="utf-8").read().strip() or "0")
    except ValueError:
        rc = 0
    if rc != 0:
        sys.stderr.write("synthetic journal producer failure scope=%s rc=%d\n" % (scope, rc))
        sys.exit(rc)
err_path = os.path.join(BASE, "journal", scope + ".stderr")
if os.path.exists(err_path):
    text = open(err_path, encoding="utf-8", errors="replace").read()
    if text:
        sys.stderr.write(text)
if MODE == "malformed":
    sys.stdout.write("{not json\n")
    sys.exit(0)
records = []
rec_path = os.path.join(BASE, "journal", scope + ".records")
if os.path.exists(rec_path):
    with open(rec_path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except ValueError:
                records.append({"_malformed": line})
if MODE == "text" and not json_out:
    text_path = os.path.join(BASE, "journal", "text.txt")
    if os.path.exists(text_path):
        sys.stdout.write(open(text_path, encoding="utf-8", errors="replace").read())
    sys.exit(0)
ignore = MODE == "ignore-filters"
if MODE in ("dup-kernel", "mismatch-kernel") and any(
        k == "MESSAGE_ID" and v == KERNEL_ID for k, v in want):
    ignore = True
elif MODE == "mismatch-kernel":
    # Only the kernel query receives the wrong-class record; every other
    # slot answers a valid empty stream, like the r13 per-slot stub.
    records = []
if not ignore:
    kept = []
    for rec in records:
        ok = True
        for k, v in want:
            if str(rec.get(k)) != v:
                ok = False
                break
        if ok:
            kept.append(rec)
    records = kept
if grep:
    try:
        rx = re.compile(grep)
        records = [r for r in records if rx.search(json.dumps(r))]
    except re.error:
        pass
for rec in records:
    if MODE == "leak":
        emit = dict(rec)
        emit["MESSAGE"] = CANARY
    elif fields is not None:
        emit = {k: rec[k] for k in fields if k in rec}
        for k in ALWAYS:
            if k in rec:
                emit[k] = rec[k]
    else:
        emit = {k: v for k, v in rec.items() if k != "MESSAGE"}
    sys.stdout.write(json.dumps(emit) + "\n")
sys.exit(0)
'''
    return (
        template.replace("@BASE@", repr(str(base)))
        .replace("@MODE@", repr(mode))
        .replace("@CANARY@", repr(CANARY))
        .replace("@KERNEL_ID@", repr(KERNEL_ID))
        .replace("@FAILURE_ID@", repr(FAILURE_ID))
    )


def git_stub_body() -> str:
    """Synthetic git: a post-launch subject commit keeps the lane progressing.

    Without it the fixture would grade LANE_SILENT and mask journal verdicts.
    """
    return """#!/usr/bin/env bash
# synthetic git: no repository is read
for a in "$@"; do
  case "$a" in
    rev-parse) printf '.git\\n'; exit 0 ;;
    ls-files) exit 0 ;;
    cat-file) exit 1 ;;
    log)
      printf '1699999000 kagi-shokunin <kagi@shokunin.local>\\n'
      exit 0
      ;;
  esac
done
exit 2
"""


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
        base / "tmp",
        base / "cg",
        base / "bin",
        base / "journal",
        base / "disk-target",
    ):
        path.mkdir(parents=True, exist_ok=True)
    log = ufo / "watchdog.log"
    log.write_text("TIMESTAMP launch %s round=%s ts=%d\n" % (LANE, ROUND, LAUNCH_EPOCH))
    os.utime(log, (NOW_EPOCH, NOW_EPOCH))
    (ufo / "state" / ("%s.round" % LANE)).write_text(ROUND + "\n")
    (base / "cg" / "memory.events").write_text(
        "low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\n"
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
    (base / "boot_id").write_text(JOURNAL_BOOT + "\n")
    for name, body in QUIET_STUBS.items():
        write_exec(base / "bin" / name, body)
    write_exec(base / "bin" / "git", git_stub_body())
    # PATH tripwire: any bare `journalctl` is recorded and refused. The census
    # is pointed at journal/journalctl-stub explicitly, so this stays empty.
    write_exec(
        base / "bin" / "journalctl",
        "#!/usr/bin/env bash\n"
        "printf '%s\\n' \"$*\" >> %r\n"
        "exit 96\n" % str(base / "journal" / "tripwire.log"),
    )


def census_env(base: Path) -> dict:
    root = base / "root"
    ufo = root / ".ufo"
    return {
        "PATH": "%s:/usr/bin:/bin" % (base / "bin"),
        "HOME": str(base / "home"),
        "TMPDIR": str(base / "tmp"),
        "TZ": "UTC",
        "LC_ALL": "C",
        "LANG": "C",
        "MORI_SHOKUNIN_ROOT": str(root),
        "MORI_UFO_DIR": str(ufo),
        "MORI_FLEET_CONF": str(root / "shokunin.conf"),
        "MORI_WATCHDOG_LOG": str(ufo / "watchdog.log"),
        "MORI_TIMELINE_FILE": str(ufo / "watchdog.log"),
        "MORI_STATE_DIR": str(ufo / "state"),
        "MORI_WAVES_DIR": str(ufo / "waves"),
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
        "MORI_JOURNALCTL_BIN": str(base / "journal" / "journalctl-stub"),
        "MORI_TMUX_BIN": str(base / "bin" / "tmux"),
        "MORI_GIT_BIN": str(base / "bin" / "git"),
        "MORI_DISK_TARGETS": str(base / "disk-target"),
        "MORI_BOOT_ID": JOURNAL_BOOT,
        "MORI_BOOT_ID_FILE": str(base / "boot_id"),
        "MORI_ROSTER_LANES": LANE,
        "MORI_NOW_EPOCH": str(NOW_EPOCH),
        "MORI_WATCHDOG_STALE_S": "900",
        "MORI_WAVE_UNSETTLED_S": "7200",
        "MORI_DISK_WARN_PCT": "85",
        "MORI_DISK_CRIT_PCT": "95",
        "MORI_LANE_SILENCE_S": "900",
        "MORI_TMUX_IDLE_WARN_S": "3600",
        "MORI_JOURNAL_TIMEOUT_S": "10",
        "MORI_RUN_NONCE": "1414",
    }


_REC_SEQ = itertools.count(1)


def jrec(mid, **extra):
    """One synthetic structured journal record (no MESSAGE text)."""
    rec = {
        "__CURSOR": "s=r14-%s-%d" % (mid[:8], next(_REC_SEQ)),
        "__REALTIME_TIMESTAMP": "1700000000000000",
        "__MONOTONIC_TIMESTAMP": "1000",
        "_BOOT_ID": JOURNAL_BOOT,
        "_TRANSPORT": "journal",
        "MESSAGE_ID": mid,
    }
    rec.update(extra)
    return rec


def unit_fail(**extra):
    return jrec(FAILURE_ID, **extra)


def sigkill(**extra):
    return jrec(SIGKILL_ID, EXIT_CODE="killed", EXIT_STATUS="9", **extra)


def kernel_oom(**extra):
    return jrec(KERNEL_ID, **extra)


def zeros():
    return {name: "0" for name in CLASS_NAMES}


def unit_zeros():
    return {name: "0" for name in UNIT_TOKENS}


# ---------------------------------------------------------------------------
# expectations
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FindingExpect:
    ids: tuple
    sev: str
    all_of: tuple = ()
    any_of: tuple = ()


@dataclass(frozen=True)
class SurfaceExpect:
    state: object  # str | None (None accepts any state)
    tokens: dict
    partial: bool = False


@dataclass
class Case:
    cid: str
    title: str
    user: tuple = ()
    system: tuple = ()
    mode: str = "honor"
    user_rc: int = 0
    system_rc: int = 0
    user_unit_rc: int = 0
    system_unit_rc: int = 0
    user_stderr: str = ""
    system_stderr: str = ""
    text: str = ""
    env: tuple = ()
    expect_rc: int = 0
    expect_verdict: str = "CLEAN"
    expect_drift: int = 0
    expect_findings: tuple = ()
    exact_counts: tuple = ()
    forbid_ids: tuple = ()
    forbid_prefixes: tuple = ()
    surfaces: tuple = ()
    require_script_sha: bool = True


def surface(state="ok", partial=False, **kw):
    tokens = {}
    tokens.update(zeros())
    tokens.update(unit_zeros())
    for key, value in kw.items():
        tokens[key] = str(value)
    return SurfaceExpect(state=state, tokens=tokens, partial=partial)


def unavailable_surface(status):
    tokens = {name: "unavailable:" + status for name in CLASS_NAMES}
    tokens.update({name: "unavailable:" + status for name in UNIT_TOKENS})
    return SurfaceExpect(state="unavailable", tokens=tokens)


def unit_unavailable_surface(status, **class_counts):
    """Unit block unavailable while the notice classes keep their own counts."""
    tokens = zeros()
    tokens["unit_failure_record"] = "unavailable:" + status
    tokens.update({name: "unavailable:" + status for name in UNIT_TOKENS})
    for key, value in class_counts.items():
        tokens[key] = str(value)
    return SurfaceExpect(state="unavailable", tokens=tokens)


def partial_surface(state=None, **kw):
    return SurfaceExpect(
        state=state, tokens={k: str(v) for k, v in kw.items()}, partial=True
    )


def oom_expect(user_notice, system_notice, user_unit_oom, system_unit_oom,
               user_unknown=0, system_unknown=0):
    parts = []
    for key, value in (
        ("user_notice", user_notice),
        ("system_notice", system_notice),
        ("user_unit_oom", user_unit_oom),
        ("system_unit_oom", system_unit_oom),
        ("user_unit_oom_result_unknown", user_unknown),
        ("system_unit_oom_result_unknown", system_unknown),
    ):
        parts.append(r"\b%s=%s\b" % (re.escape(key), re.escape(str(value))))
    return FindingExpect((OOM_ID,), "crit", all_of=tuple(parts))


def fleet_expect(scope, count=1):
    return FindingExpect(
        (FLEET_ID[scope],),
        "info",
        all_of=(
            r"\bcount=%d\b" % count,
            r"\bscope=%s\b" % scope,
            r"\bsubject=fleet\b",
            r"\bowner=mori\b",
        ),
    )


def out_expect(scope, count=1):
    return FindingExpect(
        (OUT_ID[scope],),
        "info",
        all_of=(
            r"\bcount=%d\b" % count,
            r"\bscope=%s\b" % scope,
            r"\bsubject=nonfleet\b",
            r"\bowner=tsukuroi\b",
        ),
    )


def unknown_expect(scope, count=1):
    return FindingExpect(
        (UNKNOWN_ID,),
        "info",
        all_of=(
            r"\bcount=%d\b" % count,
            r"\bscope=%s\b" % scope,
            r"\bowner=unresolved\b",
            r"\breason=subject-metadata-unknown\b",
        ),
    )


def build_cases():
    cases = []

    def add(case):
        cases.append(case)

    # 1. Empty control: both scopes valid and empty; every raw count is a real 0.
    add(Case(
        "R14_BASELINE_EMPTY",
        "empty streams -> CLEAN rc0, six raw zeros + unit zeros",
        forbid_ids=FORBID_OOM + (KILL_ID, KILL_SYSTEM_ID) + tuple(OUT_ID.values()),
        forbid_prefixes=(FLEET_ID["user"], FLEET_ID["system"],
                         UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(("user", surface()), ("system", surface())),
    ))

    # 2/3. Restored global OOM alarm; separate scope counters, no count= total.
    add(Case(
        "R14_OOM_ALARM_USER",
        "user kernel OOM notice -> global OOM_KILL_JOURNAL crit + DRIFT",
        user=(kernel_oom(),),
        expect_rc=1,
        expect_verdict="DRIFT",
        expect_drift=1,
        expect_findings=(oom_expect(1, 0, 0, 0),),
        exact_counts=((OOM_ID, 1),),
        forbid_prefixes=(FLEET_ID["user"], FLEET_ID["system"],
                         UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", surface(kernel_oom_notice=1)),
            ("system", surface()),
        ),
    ))
    add(Case(
        "R14_OOM_ALARM_SYSTEM",
        "system kernel OOM notices -> same global alarm, system_notice=2",
        system=(kernel_oom(), kernel_oom()),
        expect_rc=1,
        expect_verdict="DRIFT",
        expect_drift=1,
        expect_findings=(oom_expect(0, 2, 0, 0),),
        exact_counts=((OOM_ID, 1),),
        forbid_prefixes=(FLEET_ID["user"], FLEET_ID["system"],
                         UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", surface()),
            ("system", surface(kernel_oom_notice=2)),
        ),
    ))

    # 4-6. UNIT_RESULT=oom-kill: alarm independent of subject; routing separate.
    add(Case(
        "R14_UNIT_OOM_KILL",
        "fleet UNIT_RESULT=oom-kill -> global alarm + fleet info",
        user=(unit_fail(UNIT_RESULT="oom-kill", USER_UNIT=FLEET_UNIT),),
        expect_rc=1,
        expect_verdict="DRIFT",
        expect_drift=1,
        expect_findings=(oom_expect(0, 0, 1, 0), fleet_expect("user", 1)),
        exact_counts=((OOM_ID, 1),),
        forbid_ids=tuple(OUT_ID.values()),
        forbid_prefixes=(UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", surface(unit_failure_record=1, unit_fleet=1,
                             unit_oom=1, unit_oom_fleet=1)),
            ("system", surface()),
        ),
    ))
    add(Case(
        "R14_UNIT_OOM_NONFLEET",
        "nonfleet oom-kill -> global alarm + OUT_OF_SCOPE owner=tsukuroi",
        user=(unit_fail(UNIT_RESULT="oom-kill", USER_UNIT=NONFLEET_UNIT),),
        expect_rc=1,
        expect_verdict="DRIFT",
        expect_drift=1,
        expect_findings=(oom_expect(0, 0, 1, 0), out_expect("user", 1)),
        exact_counts=((OOM_ID, 1),),
        forbid_prefixes=(FLEET_ID["user"], FLEET_ID["system"],
                         UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", surface(unit_failure_record=1, unit_nonfleet=1,
                             unit_oom=1, unit_oom_nonfleet=1)),
            ("system", surface()),
        ),
    ))
    add(Case(
        "R14_UNIT_OOM_SYSTEM",
        "system fleet oom-kill -> global alarm system_unit_oom=1",
        system=(unit_fail(UNIT_RESULT="oom-kill", UNIT=FLEET_UNIT),),
        expect_rc=1,
        expect_verdict="DRIFT",
        expect_drift=1,
        expect_findings=(oom_expect(0, 0, 0, 1), fleet_expect("system", 1)),
        exact_counts=((OOM_ID, 1),),
        forbid_ids=tuple(OUT_ID.values()),
        forbid_prefixes=(UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", surface()),
            ("system", surface(unit_failure_record=1, unit_fleet=1,
                               unit_oom=1, unit_oom_fleet=1)),
        ),
    ))

    # 6b. Both scopes contribute unit oom results: one global alarm carries two
    # separate non-summed counters.
    add(Case(
        "R14_UNIT_OOM_BOTH_SCOPES",
        "user and system unit oom-kill -> one alarm, two separate counters",
        user=(unit_fail(UNIT_RESULT="oom-kill", USER_UNIT=FLEET_UNIT),),
        system=(unit_fail(UNIT_RESULT="oom-kill", UNIT=FLEET_UNIT),),
        expect_rc=1,
        expect_verdict="DRIFT",
        expect_drift=1,
        expect_findings=(
            oom_expect(0, 0, 1, 1),
            fleet_expect("user", 1),
            fleet_expect("system", 1),
        ),
        exact_counts=((OOM_ID, 1),),
        forbid_ids=tuple(OUT_ID.values()),
        forbid_prefixes=(UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", surface(unit_failure_record=1, unit_fleet=1,
                             unit_oom=1, unit_oom_fleet=1)),
            ("system", surface(unit_failure_record=1, unit_fleet=1,
                               unit_oom=1, unit_oom_fleet=1)),
        ),
    )) 

    add(Case(
        "R14_UNIT_OOM_MISSING_SUBJECT",
        "oom-kill with only _SYSTEMD_UNIT -> alarm + raw count + unattributed",
        user=(unit_fail(UNIT_RESULT="oom-kill", _SYSTEMD_UNIT=EMITTER_UNIT),),
        expect_rc=1,
        expect_verdict="DRIFT",
        expect_drift=1,
        expect_findings=(oom_expect(0, 0, 1, 0), unknown_expect("user", 1)),
        exact_counts=((OOM_ID, 1),),
        forbid_ids=tuple(OUT_ID.values()),
        forbid_prefixes=(FLEET_ID["user"], FLEET_ID["system"], RETIRED_PREFIX),
        surfaces=(
            ("user", surface(unit_failure_record=1, unit_unknown=1,
                             unit_missing=1, unit_oom=1,
                             unit_oom_subject_unknown=1)),
            ("system", surface()),
        ),
    ))
    add(Case(
        "R14_UNIT_OOM_SUBJECT_ARRAY",
        "USER_UNIT array -> alarm + raw count + unattributed, not unavailable",
        user=(unit_fail(UNIT_RESULT="oom-kill",
                        USER_UNIT=[FLEET_UNIT, NONFLEET_UNIT]),),
        expect_rc=1,
        expect_verdict="DRIFT",
        expect_drift=1,
        expect_findings=(oom_expect(0, 0, 1, 0), unknown_expect("user", 1)),
        exact_counts=((OOM_ID, 1),),
        forbid_ids=tuple(OUT_ID.values()),
        forbid_prefixes=(FLEET_ID["user"], FLEET_ID["system"], RETIRED_PREFIX),
        surfaces=(
            ("user", surface(unit_failure_record=1, unit_unknown=1,
                             unit_malformed=1, unit_oom=1,
                             unit_oom_subject_unknown=1)),
            ("system", surface()),
        ),
    ))

    # 9. Fleet generic failure: INFO (historical severity), roll stays CLEAN.
    add(Case(
        "R14_UNIT_FAILED_FLEET",
        "fleet UNIT_RESULT=resources -> UNIT_FAILURE_JOURNAL info owner=mori, CLEAN",
        user=(unit_fail(UNIT_RESULT="resources", UNIT=FLEET_UNIT),),
        expect_findings=(fleet_expect("user", 1),),
        forbid_ids=FORBID_OOM + tuple(OUT_ID.values()),
        forbid_prefixes=(UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", surface(unit_failure_record=1, unit_fleet=1)),
            ("system", surface()),
        ),
    ))

    # 10. Nonfleet failure: named adjacent owner, INFO, CLEAN.
    add(Case(
        "R14_UNIT_FAILED_NONFLEET",
        "nonfleet result -> UNIT_FAILURE_OUT_OF_SCOPE info owner=tsukuroi, CLEAN",
        user=(unit_fail(UNIT_RESULT="resources", USER_UNIT=NONFLEET_UNIT),),
        expect_findings=(out_expect("user", 1),),
        forbid_ids=FORBID_OOM,
        forbid_prefixes=(FLEET_ID["user"], FLEET_ID["system"],
                         UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", surface(unit_failure_record=1, unit_nonfleet=1)),
            ("system", surface()),
        ),
    ))

    # 11. Emitter-only metadata is not a subject.
    add(Case(
        "R14_UNIT_FAILED_UNKNOWN",
        "only _SYSTEMD_UNIT emitter -> unattributed, never nonfleet",
        user=(unit_fail(UNIT_RESULT="resources", _SYSTEMD_UNIT=EMITTER_UNIT),),
        expect_findings=(unknown_expect("user", 1),),
        forbid_ids=FORBID_OOM + tuple(OUT_ID.values()),
        forbid_prefixes=(FLEET_ID["user"], FLEET_ID["system"], RETIRED_PREFIX),
        surfaces=(
            ("user", surface(unit_failure_record=1, unit_unknown=1,
                             unit_missing=1)),
            ("system", surface()),
        ),
    ))

    # 11b/11c. Escape handling: literal \xHH escapes stay a known unit name,
    # while an arbitrary backslash escape is not a unit name (unknown, never
    # fleet even when the raw bytes contain a fleet marker).
    add(Case(
        "R14_UNIT_VALID_ESCAPE_KNOWN",
        "valid \\xHH unit escape stays a known (non-fleet) subject",
        user=(unit_fail(
            UNIT_RESULT="resources",
            USER_UNIT=r"app-Hyprland-xdg\x2dterminal\x2dexec-dd9e67bd.scope"),),
        expect_findings=(out_expect("user", 1),),
        forbid_ids=FORBID_OOM,
        forbid_prefixes=(FLEET_ID["user"], FLEET_ID["system"],
                         UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", surface(unit_failure_record=1, unit_nonfleet=1,
                             unit_unknown=0, unit_malformed=0)),
            ("system", surface()),
        ),
    ))
    add(Case(
        "R14_UNIT_INVALID_ESCAPE_UNKNOWN",
        "invalid escape in subject -> unknown, never fleet; raw count kept",
        user=(unit_fail(UNIT_RESULT="resources", USER_UNIT=r"shokunin\q.service"),),
        expect_findings=(unknown_expect("user", 1),),
        forbid_ids=FORBID_OOM + tuple(OUT_ID.values()),
        forbid_prefixes=(FLEET_ID["user"], FLEET_ID["system"], RETIRED_PREFIX),
        surfaces=(
            ("user", surface(unit_failure_record=1, unit_fleet=0,
                             unit_nonfleet=0, unit_unknown=1,
                             unit_malformed=1)),
            ("system", surface()),
        ),
    ))

    add(Case(
        "R14_UNIT_SUBJECT_NULL_UNKNOWN",
        "null UNIT subject -> unknown, never fleet; raw count kept",
        user=(unit_fail(UNIT_RESULT="resources", UNIT=None),),
        expect_findings=(unknown_expect("user", 1),),
        forbid_ids=FORBID_OOM + tuple(OUT_ID.values()),
        forbid_prefixes=(FLEET_ID["user"], FLEET_ID["system"], RETIRED_PREFIX),
        surfaces=(
            ("user", surface(unit_failure_record=1, unit_fleet=0,
                             unit_nonfleet=0, unit_unknown=1,
                             unit_malformed=1)),
            ("system", surface()),
        ),
    ))

    # 12. USER_UNIT is a valid subject even in the system journal.
    add(Case(
        "R14_USER_UNIT_IN_SYSTEM",
        "system-scope USER_UNIT fleet subject -> fleet classification",
        system=(unit_fail(UNIT_RESULT="resources", USER_UNIT=FLEET_UNIT),),
        expect_findings=(fleet_expect("system", 1),),
        forbid_ids=FORBID_OOM + tuple(OUT_ID.values()),
        forbid_prefixes=(UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", surface()),
            ("system", surface(unit_failure_record=1, unit_fleet=1)),
        ),
    ))

    # 13. Both subject fields present: unattributed, never nonfleet, never fatal.
    add(Case(
        "R14_SUBJECT_AMBIGUOUS",
        "UNIT and USER_UNIT both present -> unattributed, never nonfleet",
        user=(unit_fail(UNIT_RESULT="resources", UNIT=FLEET_UNIT,
                        USER_UNIT=NONFLEET_UNIT),),
        expect_findings=(unknown_expect("user", 1),),
        forbid_ids=FORBID_OOM + tuple(OUT_ID.values()),
        forbid_prefixes=(FLEET_ID["user"], FLEET_ID["system"], RETIRED_PREFIX),
        surfaces=(
            ("user", surface(unit_failure_record=1, unit_unknown=1,
                             unit_ambiguous=1)),
            ("system", surface()),
        ),
    ))

    # 14. UNIT_RESULT absent: raw total kept, oom subset explicitly unknown.
    add(Case(
        "R14_UNIT_RESULT_MISSING",
        "UNIT_RESULT absent -> raw count + unit_oom_result_unknown, not oom",
        user=(unit_fail(USER_UNIT=FLEET_UNIT),),
        expect_findings=(fleet_expect("user", 1),),
        forbid_ids=FORBID_OOM + tuple(OUT_ID.values()),
        forbid_prefixes=(UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", surface(unit_failure_record=1, unit_fleet=1,
                             unit_oom=0, unit_oom_result_unknown=1)),
            ("system", surface()),
        ),
    ))

    # 14b. A non-string UNIT_RESULT (array) is unknown, never oom evidence.
    add(Case(
        "R14_UNIT_RESULT_ARRAY_UNKNOWN",
        "array UNIT_RESULT -> unit_oom_result_unknown, not oom",
        user=(unit_fail(UNIT_RESULT=["oom-kill"], USER_UNIT=FLEET_UNIT),),
        expect_findings=(fleet_expect("user", 1),),
        forbid_ids=FORBID_OOM + tuple(OUT_ID.values()),
        forbid_prefixes=(UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", surface(unit_failure_record=1, unit_fleet=1,
                             unit_oom=0, unit_oom_result_unknown=1,
                             unit_signal=0)),
            ("system", surface()),
        ),
    ))

    # 14c. Only a missing/non-string UNIT_RESULT is result-unknown. Arbitrary
    # strings (including uppercase OOM-KILL and empty) are non-oom strings and
    # must not fabricate either oom evidence or result-unknown counts.
    add(Case(
        "R14_UNIT_RESULT_NOT_OOM_STRINGS",
        "non-oom result strings are neither oom nor result-unknown",
        user=(
            unit_fail(UNIT_RESULT="OOM-KILL", USER_UNIT=FLEET_UNIT),
            unit_fail(UNIT_RESULT="", USER_UNIT=FLEET_UNIT),
        ),
        expect_findings=(fleet_expect("user", 2),),
        forbid_ids=FORBID_OOM + tuple(OUT_ID.values()),
        forbid_prefixes=(UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", surface(unit_failure_record=2, unit_fleet=2,
                             unit_oom=0, unit_oom_result_unknown=0,
                             unit_signal=0)),
            ("system", surface()),
        ),
    ))

    # 15. Partition: fleet+nonfleet+unknown == raw count in one scope.
    add(Case(
        "R14_UNIT_PARTITION",
        "fleet+nonfleet+unknown partition = raw unit_failure_record count",
        user=(
            unit_fail(UNIT_RESULT="resources", USER_UNIT=FLEET_UNIT),
            unit_fail(UNIT_RESULT="resources", USER_UNIT=NONFLEET_UNIT),
            unit_fail(UNIT_RESULT="resources"),
        ),
        expect_findings=(
            fleet_expect("user", 1),
            out_expect("user", 1),
            unknown_expect("user", 1),
        ),
        forbid_ids=FORBID_OOM,
        forbid_prefixes=(RETIRED_PREFIX,),
        surfaces=(
            ("user", surface(unit_failure_record=3, unit_fleet=1,
                             unit_nonfleet=1, unit_unknown=1,
                             unit_missing=1)),
            ("system", surface()),
        ),
    ))

    # 16. Generic SIGKILL warn preserved; no OOM alarm invented.
    add(Case(
        "R14_SIGKILL_WARN",
        "user unit-process SIGKILL -> KILL_SIGNAL_JOURNAL warn + DRIFT",
        user=(sigkill(),),
        expect_rc=1,
        expect_verdict="DRIFT",
        expect_drift=1,
        expect_findings=(
            FindingExpect((KILL_ID,), "warn",
                          all_of=(r"\bscope=user\b", r"\bcount=1\b")),
        ),
        forbid_ids=FORBID_OOM + tuple(OUT_ID.values()),
        forbid_prefixes=(FLEET_ID["user"], FLEET_ID["system"],
                         UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", surface(unit_sigkill_record=1)),
            ("system", surface()),
        ),
    ))

    # 16b. User UNIT_RESULT=signal keeps the pre-r13 warn behavior (the legacy
    # text class warned on "Failed with result 'signal'"); it is a result
    # ordinal, not proof of SIGKILL, and it must not be read as OOM.
    add(Case(
        "R14_UNIT_SIGNAL_WARN",
        "user UNIT_RESULT=signal -> KILL_SIGNAL_JOURNAL warn + DRIFT, no OOM",
        user=(unit_fail(UNIT_RESULT="signal", USER_UNIT=FLEET_UNIT),),
        expect_rc=1,
        expect_verdict="DRIFT",
        expect_drift=1,
        expect_findings=(
            FindingExpect((KILL_ID,), "warn",
                          all_of=(r"\bscope=user\b", r"\bcount=0\b",
                                  r"\bprocess_sigkill=0\b",
                                  r"\buser_unit_signal=1\b")),
            fleet_expect("user", 1),
        ),
        forbid_ids=FORBID_OOM + tuple(OUT_ID.values()),
        forbid_prefixes=(UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", surface(unit_failure_record=1, unit_fleet=1,
                             unit_signal=1, unit_oom=0)),
            ("system", surface()),
        ),
    ))
    # 16c. The same result in the system scope stays INFO routing only.
    add(Case(
        "R14_UNIT_SIGNAL_SYSTEM_INFO",
        "system UNIT_RESULT=signal -> fleet info, CLEAN, no KILL warn",
        system=(unit_fail(UNIT_RESULT="signal", UNIT=FLEET_UNIT),),
        expect_findings=(fleet_expect("system", 1),),
        forbid_ids=FORBID_OOM + (KILL_ID, KILL_SYSTEM_ID) + tuple(OUT_ID.values()),
        forbid_prefixes=(UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", surface()),
            ("system", surface(unit_failure_record=1, unit_fleet=1,
                               unit_signal=1)),
        ),
    ))

    # 17. One-kill fan-out: one global OOM line, one SIGKILL line, drift=2.
    add(Case(
        "R14_FANOUT_ONE_SIGNAL_PER_KIND",
        "fan-out: one global OOM line + one SIGKILL line; drift=2",
        user=(
            kernel_oom(),
            unit_fail(UNIT_RESULT="oom-kill", USER_UNIT=FLEET_UNIT),
            sigkill(),
        ),
        system=(kernel_oom(),),
        expect_rc=1,
        expect_verdict="DRIFT",
        expect_drift=2,
        expect_findings=(
            oom_expect(1, 1, 1, 0),
            fleet_expect("user", 1),
            FindingExpect((KILL_ID,), "warn", all_of=(r"\bscope=user\b",)),
        ),
        exact_counts=((OOM_ID, 1),),
        forbid_ids=tuple(OUT_ID.values()),
        forbid_prefixes=(UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", surface(kernel_oom_notice=1, unit_failure_record=1,
                             unit_sigkill_record=1, unit_fleet=1,
                             unit_oom=1, unit_oom_fleet=1)),
            ("system", surface(kernel_oom_notice=1)),
        ),
    ))

    # 18. Raw r13 count parity, both scopes, distinct values.
    add(Case(
        "R14_SCOPED_PARITY",
        "six raw counts per scope unchanged; never summed",
        user=(
            kernel_oom(), kernel_oom(), kernel_oom(),
            jrec(COREDUMP_ID, COREDUMP_SIGNAL="11"),
            sigkill(), sigkill(),
            jrec(COREDUMP_ID, COREDUMP_SIGNAL="6"),
            jrec(SIGKILL_ID, EXIT_CODE="killed", EXIT_STATUS="15"),
            jrec(SIGKILL_ID, EXIT_CODE="exited", EXIT_STATUS="9"),
            unit_fail(UNIT_RESULT="resources", USER_UNIT=FLEET_UNIT),
        ),
        system=(
            kernel_oom(), kernel_oom(),
            jrec(OOMD_ID),
            jrec(COREDUMP_ID, COREDUMP_SIGNAL="11"),
            jrec(COREDUMP_ID, COREDUMP_SIGNAL="11"),
            jrec(COREDUMP_ID, COREDUMP_SIGNAL="11"),
            jrec(COREDUMP_ID, COREDUMP_SIGNAL="6"),
            jrec(SIGKILL_ID, EXIT_CODE="killed", EXIT_STATUS="15"),
            unit_fail(UNIT_RESULT="resources", UNIT=FLEET_UNIT),
            unit_fail(UNIT_RESULT="resources", UNIT=NONFLEET_UNIT),
        ),
        expect_rc=1,
        expect_verdict="DRIFT",
        expect_drift=2,
        expect_findings=(
            oom_expect(3, 2, 0, 0),
            fleet_expect("user", 1),
            fleet_expect("system", 1),
            out_expect("system", 1),
            FindingExpect((KILL_ID,), "warn", all_of=(r"\bscope=user\b",)),
        ),
        exact_counts=((OOM_ID, 1),),
        forbid_prefixes=(UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", surface(kernel_oom_notice=3, oomd_notice=0,
                             coredump_notice=2, segfault_signal11=1,
                             unit_sigkill_record=2, unit_failure_record=1,
                             unit_fleet=1)),
            ("system", surface(kernel_oom_notice=2, oomd_notice=1,
                               coredump_notice=4, segfault_signal11=3,
                               unit_sigkill_record=0, unit_failure_record=2,
                               unit_fleet=1, unit_nonfleet=1)),
        ),
    ))

    # 19. Scope separation with different positive values: no summed field.
    add(Case(
        "R14_SCOPE_NOT_SUMMED",
        "user 3 / system 5 stay separate fields, never a sum",
        user=(kernel_oom(), kernel_oom(), kernel_oom()),
        system=(kernel_oom(), kernel_oom(), kernel_oom(), kernel_oom(), kernel_oom()),
        expect_rc=1,
        expect_verdict="DRIFT",
        expect_drift=1,
        expect_findings=(oom_expect(3, 5, 0, 0),),
        exact_counts=((OOM_ID, 1),),
        forbid_ids=(KILL_ID, KILL_SYSTEM_ID) + tuple(OUT_ID.values()),
        forbid_prefixes=(FLEET_ID["user"], FLEET_ID["system"],
                         UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", surface(kernel_oom_notice=3)),
            ("system", surface(kernel_oom_notice=5)),
        ),
    ))

    # 20. Info-only notices stay CLEAN.
    add(Case(
        "R14_NOTICE_INFO_CLEAN",
        "oomd+coredump+segfault notices only -> CLEAN rc0, no OOM alarm",
        user=(jrec(OOMD_ID), jrec(COREDUMP_ID, COREDUMP_SIGNAL="11")),
        system=(jrec(OOMD_ID), jrec(COREDUMP_ID, COREDUMP_SIGNAL="11")),
        forbid_ids=FORBID_OOM + (KILL_ID, KILL_SYSTEM_ID) + tuple(OUT_ID.values()),
        forbid_prefixes=(FLEET_ID["user"], FLEET_ID["system"],
                         UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", surface(oomd_notice=1, coredump_notice=1,
                             segfault_signal11=1)),
            ("system", surface(oomd_notice=1, coredump_notice=1,
                               segfault_signal11=1)),
        ),
    ))

    # 20b. systemd-oomd notices alone are INFO, never the OOM alarm (the r12
    # record is a per-unit notice, not a unique-victim or fleet-cause count).
    add(Case(
        "R14_OOMD_ONLY_INFO",
        "oomd notices only -> INFO, CLEAN, no OOM alarm",
        user=(jrec(OOMD_ID),),
        system=(jrec(OOMD_ID), jrec(OOMD_ID)),
        expect_findings=(
            FindingExpect(("OOMD_NOTICE_JOURNAL_USER",), "info",
                          all_of=(r"\bcount=1\b", r"\bscope=user\b")),
            FindingExpect(("OOMD_NOTICE_JOURNAL_SYSTEM",), "info",
                          all_of=(r"\bcount=2\b", r"\bscope=system\b")),
        ),
        forbid_ids=FORBID_OOM + (KILL_ID, KILL_SYSTEM_ID) + tuple(OUT_ID.values()),
        forbid_prefixes=(FLEET_ID["user"], FLEET_ID["system"],
                         UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", surface(oomd_notice=1)),
            ("system", surface(oomd_notice=2)),
        ),
    ))

    # 21. Producer rc: unavailable, not a fake zero.
    add(Case(
        "R14_QUERY_ERROR_UNAVAILABLE",
        "journalctl rc5 -> unavailable:rc-5, never zero",
        user_rc=5,
        surfaces=(
            ("user", unavailable_surface("rc-5")),
            ("system", surface()),
        ),
        forbid_ids=FORBID_OOM + (KILL_ID,) + tuple(OUT_ID.values()),
        forbid_prefixes=(RETIRED_PREFIX,),
    ))

    # 22. One scope failing must not suppress the other scope's alarm.
    add(Case(
        "R14_PARTIAL_ERROR_SYSTEM_ALARMS",
        "user rc1 + system notices -> global alarm still fires",
        user_rc=1,
        system=(kernel_oom(), kernel_oom()),
        expect_rc=1,
        expect_verdict="DRIFT",
        expect_drift=1,
        expect_findings=(
            oom_expect("unavailable:rc-1", 2, "unavailable:rc-1", 0,
                       user_unknown="unavailable:rc-1"),
        ),
        exact_counts=((OOM_ID, 1),),
        forbid_prefixes=(FLEET_ID["user"], FLEET_ID["system"],
                         UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", unavailable_surface("rc-1")),
            ("system", surface(kernel_oom_notice=2)),
        ),
    ))

    # 22b. Only the unit query fails: the kernel-notice path still alarms and
    # the unit tokens name the failure reason; no routing finding is invented.
    add(Case(
        "R14_UNIT_QUERY_ERROR_KERNEL_ALARM",
        "user unit query rc1 + user notice -> kernel path still alarms",
        mode="unit-rc",
        user=(kernel_oom(),),
        user_unit_rc=1,
        expect_rc=1,
        expect_verdict="DRIFT",
        expect_drift=1,
        expect_findings=(
            oom_expect(1, 0, "unavailable:rc-1", 0,
                       user_unknown="unavailable:rc-1"),
        ),
        exact_counts=((OOM_ID, 1),),
        forbid_prefixes=(FLEET_ID["user"], FLEET_ID["system"],
                         OUT_ID["user"], OUT_ID["system"],
                         UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", unit_unavailable_surface("rc-1", kernel_oom_notice=1)),
            ("system", surface()),
        ),
    ))

    # 23. Producer stderr: unavailable, bytes never retained.
    add(Case(
        "R14_STDERR_UNAVAILABLE",
        "producer stderr -> unavailable:stderr-nonempty, no fake zero",
        user_stderr="warning: partial journal access %s\n" % STDERR_CANARY,
        surfaces=(
            ("user", unavailable_surface("stderr-nonempty")),
            ("system", surface()),
        ),
        forbid_ids=FORBID_OOM + tuple(OUT_ID.values()),
        forbid_prefixes=(RETIRED_PREFIX,),
    ))

    # 24. Malformed JSON: unavailable, not zero and not an alarm.
    add(Case(
        "R14_MALFORMED_UNAVAILABLE",
        "malformed JSON -> unavailable:malformed-json",
        mode="malformed",
        surfaces=(
            ("user", unavailable_surface("malformed-json")),
            ("system", unavailable_surface("malformed-json")),
        ),
        forbid_ids=FORBID_OOM + tuple(OUT_ID.values()),
        forbid_prefixes=(RETIRED_PREFIX,),
    ))

    # 25. Foreign boot: unavailable, no alarm.
    add(Case(
        "R14_WRONG_BOOT_UNAVAILABLE",
        "foreign _BOOT_ID -> unavailable:boot-mismatch, no alarm",
        user=(kernel_oom(_BOOT_ID=FOREIGN_BOOT_A),),
        surfaces=(
            ("user", surface(state="unavailable",
                             kernel_oom_notice="unavailable:boot-mismatch")),
            ("system", surface()),
        ),
        forbid_ids=FORBID_OOM + tuple(OUT_ID.values()),
        forbid_prefixes=(RETIRED_PREFIX,),
    ))

    # 26. Mixed boots: unavailable:multi-boot on the queried class only.
    add(Case(
        "R14_MULTI_BOOT_UNAVAILABLE",
        "several boots -> unavailable:multi-boot",
        user=(jrec(OOMD_ID, _BOOT_ID=FOREIGN_BOOT_A),
              jrec(OOMD_ID, _BOOT_ID=FOREIGN_BOOT_B)),
        surfaces=(
            ("user", surface(state="unavailable",
                             oomd_notice="unavailable:multi-boot")),
            ("system", surface()),
        ),
        forbid_ids=FORBID_OOM + tuple(OUT_ID.values()),
        forbid_prefixes=(RETIRED_PREFIX,),
    ))

    # 27. Producer returns a different class for the kernel query: identity
    # validation must refuse it instead of counting a look-alike.
    add(Case(
        "R14_IGNORE_FILTERS_INVALID",
        "kernel query returns another class -> unavailable:record-invalid",
        mode="mismatch-kernel",
        user=(jrec(OOMD_ID),),
        surfaces=(
            ("user", surface(state="unavailable",
                             kernel_oom_notice="unavailable:record-invalid")),
            ("system", surface()),
        ),
        forbid_ids=FORBID_OOM + tuple(OUT_ID.values()),
        forbid_prefixes=(RETIRED_PREFIX,),
    ))

    # 28. Retained control: a malformed duplicate MESSAGE_ID in an otherwise
    # valid stream still grades that class unavailable (honest, never a fake
    # zero). The all-or-nothing validation is inherited from r13; the
    # alarm-silencing limitation is named in the report, not waived by a green
    # expectation.
    add(Case(
        "R14_SEC_DUP_MSGID_MIXED",
        "valid OOM + MESSAGE_ID array -> class record-invalid, never a fake zero",
        mode="dup-kernel",
        user=(kernel_oom(), kernel_oom(MESSAGE_ID=[KERNEL_ID])),
        surfaces=(
            ("user", surface(state="unavailable",
                             kernel_oom_notice="unavailable:record-invalid")),
            ("system", surface()),
        ),
        forbid_ids=FORBID_OOM + tuple(OUT_ID.values()),
        forbid_prefixes=(RETIRED_PREFIX,),
    ))

    # 29. Security: newline/token unit canary never reaches output; raw count
    # survives, and no OOM alarm is invented from the unit bytes.
    add(Case(
        "R14_SEC_UNIT_CANARY",
        "newline/token unit canary never emitted; raw count kept",
        user=(unit_fail(UNIT_RESULT="resources",
                        USER_UNIT=UNIT_CANARY + "\nFINDING FAKE_OOM severity=crit obs=x"),),
        forbid_ids=FORBID_OOM,
        forbid_prefixes=(RETIRED_PREFIX,),
        surfaces=(
            ("user", partial_surface(unit_failure_record=1)),
            ("system", surface()),
        ),
    ))

    # 29b. A VALID canary-embedded unit name follows the classification path;
    # it must be classified (non-fleet here) but its bytes must never reach
    # output. The canary string exists only in the record, not in a fixture
    # path, so any occurrence is a real leak.
    add(Case(
        "R14_SEC_VALID_UNIT_CANARY",
        "valid canary unit name is classified but never emitted",
        user=(unit_fail(UNIT_RESULT="resources", UNIT=VALID_CANARY_UNIT),),
        expect_findings=(out_expect("user", 1),),
        forbid_ids=FORBID_OOM,
        forbid_prefixes=(FLEET_ID["user"], FLEET_ID["system"],
                         UNKNOWN_ID, RETIRED_PREFIX),
        surfaces=(
            ("user", surface(unit_failure_record=1, unit_nonfleet=1,
                             unit_unknown=0, unit_malformed=0)),
            ("system", surface()),
        ),
    ))

    # 30. MESSAGE leak: the producer forces MESSAGE into every record; the
    # census must still count structurally and never emit or request it.
    add(Case(
        "R14_MESSAGE_CANARY",
        "MESSAGE bytes and unit subject bytes never emitted; no MESSAGE request",
        mode="leak",
        user=(kernel_oom(),
              unit_fail(UNIT_RESULT="resources", UNIT=UNIT_CANARY)),
        system=(jrec(OOMD_ID),),
        expect_rc=1,
        expect_verdict="DRIFT",
        expect_drift=1,
        expect_findings=(oom_expect(1, 0, 0, 0),),
        exact_counts=((OOM_ID, 1),),
        surfaces=(
            ("user", partial_surface(kernel_oom_notice=1,
                                     unit_failure_record=1)),
            ("system", surface(oomd_notice=1)),
        ),
    ))

    # 31. Text-only OOM: MESSAGE text is never admitted as a structured alarm.
    add(Case(
        "R14_TEXT_ONLY_NOT_ADMITTED",
        "MESSAGE text only -> no OOM alarm, canary absent",
        mode="text",
        user=({"__CURSOR": "s=r14-text", "_BOOT_ID": JOURNAL_BOOT,
               "_TRANSPORT": "journal",
               "MESSAGE": "kernel: Out of memory: Killed process 4242 %s" % CANARY},),
        text=("-- Journal begins --\n"
              "kernel: Out of memory: Killed process 4242 %s\n"
              "Failed with result signal SIGKILL\n" % CANARY),
        forbid_ids=FORBID_OOM + (KILL_ID,),
        forbid_prefixes=(RETIRED_PREFIX,),
        surfaces=(("user", surface()), ("system", surface())),
    ))

    # 32. Timeout: producer sleeps past the bound; class unavailable:timeout.
    add(Case(
        "R14_TIMEOUT_UNAVAILABLE",
        "producer timeout -> unavailable:timeout, no fake zero",
        mode="hang",
        env=(("MORI_JOURNAL_TIMEOUT_S", "1"),),
        surfaces=(
            ("user", unavailable_surface("timeout")),
            ("system", unavailable_surface("timeout")),
        ),
        forbid_ids=FORBID_OOM + tuple(OUT_ID.values()),
        forbid_prefixes=(RETIRED_PREFIX,),
    ))

    return cases


# ---------------------------------------------------------------------------
# fixture materialisation and census execution
# ---------------------------------------------------------------------------


def build_fixture(base: Path, case: Case) -> None:
    build_common(base)
    journal = base / "journal"
    for scope, records in (("user", case.user), ("system", case.system)):
        body = "".join(json.dumps(rec) + "\n" for rec in records)
        (journal / (scope + ".records")).write_text(body, encoding="utf-8")
    if case.user_rc:
        (journal / "user.rc").write_text(str(case.user_rc) + "\n", encoding="utf-8")
    if case.system_rc:
        (journal / "system.rc").write_text(str(case.system_rc) + "\n", encoding="utf-8")
    if case.user_unit_rc:
        (journal / "user.unit_rc").write_text(
            str(case.user_unit_rc) + "\n", encoding="utf-8")
    if case.system_unit_rc:
        (journal / "system.unit_rc").write_text(
            str(case.system_unit_rc) + "\n", encoding="utf-8")
    if case.user_stderr:
        (journal / "user.stderr").write_text(case.user_stderr, encoding="utf-8")
    if case.system_stderr:
        (journal / "system.stderr").write_text(case.system_stderr, encoding="utf-8")
    if case.text:
        (journal / "text.txt").write_text(case.text, encoding="utf-8")
    write_exec(journal / "journalctl-stub", journal_stub_body(base, case.mode))
    (journal / "argv.log").write_text("", encoding="utf-8")
    (journal / "tripwire.log").write_text("", encoding="utf-8")


def read_argv_log(path: Path):
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except ValueError:
            rows.append(["<unreadable-argv>"])
    return rows


def message_argv_violations(argv_rows):
    bad = []
    for tokens in argv_rows:
        for token in tokens:
            if token.startswith("--output-fields="):
                fields = token.split("=", 1)[1].split(",")
                if "MESSAGE" in fields:
                    bad.append("output-fields:MESSAGE")
            elif token == "MESSAGE" or token.startswith("MESSAGE="):
                bad.append("match:MESSAGE")
            elif token.startswith("--grep=") and "MESSAGE" in token:
                bad.append("grep:MESSAGE")
    return bad


def integer_token(tokens, name):
    value = tokens.get(name)
    if value is None or not re.fullmatch(r"[0-9]+", value):
        return None
    return int(value)


def evaluate(case: Case, out: str, err: str, rc, target_sha: str,
             argv_rows, tripwire: str):
    """Return (ok, reasons, observed). Reasons never contain raw canaries."""
    reasons = []
    word, vreason, vcounts = verdict_roll(out, rc)
    if rc != case.expect_rc:
        reasons.append("rc=%s want=%s" % (rc, case.expect_rc))
    if word != case.expect_verdict:
        reasons.append("verdict=%s/%s want=%s" % (word, vreason, case.expect_verdict))
    elif vreason != "ok":
        reasons.append("verdict_reason=%s" % vreason)
    if vcounts["drift"] != case.expect_drift:
        reasons.append("drift=%d want=%d" % (vcounts["drift"], case.expect_drift))

    rows = findings(out)
    srows = surface_rows(out)

    if case.require_script_sha:
        for row in rows:
            if row["script_sha256"] != target_sha:
                reasons.append("finding_script_sha:%s=%s"
                               % (row["id"], row["script_sha256"]))
                break

    for row in rows:
        if row["id"].startswith(RETIRED_PREFIX):
            reasons.append("retired_alarm_id:%s" % row["id"])
            break
    for row in rows:
        if "total" in row["tokens"] or "sum" in row["tokens"]:
            reasons.append("sum_token:finding:%s" % row["id"])
            break

    for exp in case.expect_findings:
        cand = [r for r in rows if r["id"] in exp.ids]
        matched = []
        for row in cand:
            if row["sev"] != exp.sev:
                continue
            if any(not re.search(pat, row["obs"]) for pat in exp.all_of):
                continue
            if exp.any_of and not any(re.search(pat, row["obs"]) for pat in exp.any_of):
                continue
            matched.append(row)
        if not matched:
            reasons.append("missing_finding:%s/%s" % ("/".join(exp.ids), exp.sev))

    for fid in case.forbid_ids:
        if any(r["id"] == fid for r in rows):
            reasons.append("forbidden_finding:%s" % fid)
    for prefix in case.forbid_prefixes:
        hits = sorted({r["id"] for r in rows if r["id"].startswith(prefix)})
        if hits:
            reasons.append("forbidden_finding:%s" % ",".join(hits))
    for fid, want in case.exact_counts:
        got = count_ids(rows, (fid,))
        if got != want:
            reasons.append("alarm_lines:%s=%d want=%d" % (fid, got, want))

    # Global OOM invariants: no count= total, and every scope counter is
    # byte-equal to that scope's raw SURFACE token. This is the no-sum contract.
    for row in rows:
        if row["id"] != OOM_ID:
            continue
        if "count" in row["tokens"]:
            reasons.append("oom_total_count_token=%s" % row["tokens"]["count"])
        for field, scope, surface_key in OOM_FIELDS + OOM_RESULT_FIELDS:
            value = row["tokens"].get(field)
            if value is None:
                reasons.append("oom_missing_field:%s" % field)
                continue
            state, tokens = srows.get(scope, (None, {}))
            surface_value = tokens.get(surface_key)
            if surface_value is None:
                reasons.append("oom_surface_missing:%s.%s" % (scope, surface_key))
            elif value != surface_value:
                reasons.append(
                    "oom_field:%s=%s surface.%s.%s=%s"
                    % (field, value, scope, surface_key, surface_value)
                )

    if set(srows) != {"user", "system"}:
        reasons.append("scoped_rows=%s want=user,system"
                       % (",".join(sorted(srows)) or "none"))
    if BARE_JOURNAL_RE.search(out):
        reasons.append("bare_surface_journal_row")

    exp_by_scope = dict(case.surfaces)
    for scope in ("user", "system"):
        state, tokens = srows.get(scope, (None, {}))
        if "total" in tokens or "sum" in tokens:
            reasons.append("sum_token:%s" % scope)
        if tokens.get("scope") not in (None, scope, "user,system"):
            reasons.append("scope_leak:%s=%s" % (scope, tokens.get("scope")))
        exp = exp_by_scope.get(scope)
        if exp is not None:
            if exp.state is not None and state != exp.state:
                reasons.append("surface.%s=%s want=%s" % (scope, state, exp.state))
            for key, want in exp.tokens.items():
                got = tokens.get(key)
                if got != want:
                    reasons.append("surface.%s.%s=%s want=%s"
                                   % (scope, key, got, want))
            if not exp.partial and state in ("ok", "unavailable"):
                for name in CLASS_NAMES + UNIT_TOKENS:
                    if name not in tokens:
                        reasons.append("surface.%s.missing_token:%s" % (scope, name))
        # Partition and subset invariants on any parseable row.
        failure = integer_token(tokens, "unit_failure_record")
        fleet = integer_token(tokens, "unit_fleet")
        nonfleet = integer_token(tokens, "unit_nonfleet")
        unknown = integer_token(tokens, "unit_unknown")
        oom = integer_token(tokens, "unit_oom")
        if None not in (failure, fleet, nonfleet, unknown):
            if fleet + nonfleet + unknown != failure:
                reasons.append(
                    "unit_partition:%s fleet=%d nonfleet=%d unknown=%d "
                    "failure=%d" % (scope, fleet, nonfleet, unknown, failure)
                )
        missing = integer_token(tokens, "unit_missing")
        ambiguous = integer_token(tokens, "unit_ambiguous")
        malformed = integer_token(tokens, "unit_malformed")
        if None not in (unknown, missing, ambiguous, malformed):
            if missing + ambiguous + malformed != unknown:
                reasons.append(
                    "unit_unknown_partition:%s missing=%d ambiguous=%d "
                    "malformed=%d unknown=%d"
                    % (scope, missing, ambiguous, malformed, unknown)
                )
        oom_fleet = integer_token(tokens, "unit_oom_fleet")
        oom_nonfleet = integer_token(tokens, "unit_oom_nonfleet")
        oom_unknown = integer_token(tokens, "unit_oom_subject_unknown")
        if None not in (oom, oom_fleet, oom_nonfleet, oom_unknown):
            if oom_fleet + oom_nonfleet + oom_unknown != oom:
                reasons.append(
                    "unit_oom_partition:%s fleet=%d nonfleet=%d unknown=%d "
                    "oom=%d" % (scope, oom_fleet, oom_nonfleet, oom_unknown, oom)
                )
        if None not in (failure, oom) and oom > failure:
            reasons.append("unit_oom_exceeds_total:%s oom=%d failure=%d"
                           % (scope, oom, failure))

    blob = out + "\n" + err
    for canary in CANARIES:
        if canary in blob:
            reasons.append("canary_leaked:%s" % canary.split("-")[1].lower())
    if "FAKE_OOM" in blob:
        reasons.append("unit_token_injection")
    if MESSAGE_KEY_RE.search(blob):
        reasons.append("MESSAGE_key_emitted")
    if MESSAGE_EQ_RE.search(blob):
        reasons.append("MESSAGE_field_emitted")
    bad_argv = message_argv_violations(argv_rows)
    if bad_argv:
        reasons.append("message_argv:%s" % ",".join(sorted(set(bad_argv))))
    # Field-projection faithfulness: the census must issue exactly one unit
    # query per journal scope and request the subject/result fields. The stub
    # projects records onto those fields, so a census that never asks for them
    # cannot classify a subject; the argv check makes that failure explicit
    # instead of trusting a SURFACE string.
    unit_calls = [tokens for tokens in argv_rows
                  if any(token == "MESSAGE_ID=" + FAILURE_ID for token in tokens)]
    if len(unit_calls) != 2:
        reasons.append("unit_query_calls=%d want=2" % len(unit_calls))
    required_fields = {"_BOOT_ID", "MESSAGE_ID", "UNIT", "USER_UNIT", "UNIT_RESULT"}
    for tokens in unit_calls:
        fields = None
        for token in tokens:
            if token.startswith("--output-fields="):
                fields = set(token.split("=", 1)[1].split(","))
        if fields is None or not required_fields <= fields:
            reasons.append("unit_query_fields_missing")
            break
    if tripwire.strip():
        reasons.append("path_journalctl_tripwire")

    observed = {
        "verdict": word,
        "verdict_reason": vreason,
        "counts": vcounts,
        "findings": [
            {"id": r["id"], "sev": r["sev"], "obs": one_line(r["obs"], 240)}
            for r in rows
        ],
        "surfaces": {
            scope: {"state": state, "tokens": tokens}
            for scope, (state, tokens) in sorted(srows.items())
        },
        "journal_argv_calls": len(argv_rows),
        "tripwire": bool(tripwire.strip()),
    }
    return (not reasons), reasons, observed


# ---------------------------------------------------------------------------
# harness
# ---------------------------------------------------------------------------


@dataclass
class Target:
    label: str
    original: Path
    executed: Path
    sha256: str


class Harness:
    def __init__(self, args):
        self.args = args
        self.output = Path(args.output).resolve()
        self.fixture_root = None
        self.targets = {}
        self.cases = build_cases()
        if args.only:
            wanted = [part for part in args.only.split(",") if part]
            known = {case.cid for case in self.cases}
            missing = [part for part in wanted if part not in known]
            if missing:
                raise SetupError("unknown --only case id(s): %s"
                                 % ",".join(missing))
            self.cases = [case for case in self.cases if case.cid in set(wanted)]
        self.claims = []
        self.runs = []
        self.pairs = []
        self.index = 0
        self.frozen_only = False

    # -- setup -------------------------------------------------------------

    def prepare(self):
        if not self.cases:
            raise SetupError("no cases")
        census = Path(self.args.census).resolve() if self.args.census else DEFAULT_CENSUS
        self.targets["sut"] = self.load_target("sut", census, pinned=False)

        frozen_arg = self.args.frozen
        if not self.args.no_frozen_control:
            frozen = Path(frozen_arg).resolve() if frozen_arg else DEFAULT_FROZEN
            if frozen.is_file():
                self.targets["frozen"] = self.load_target(
                    "frozen", frozen, pinned=True)
            else:
                raise SetupError("pinned frozen control not readable: %s" % frozen)
            if self.targets["frozen"].sha256 == self.targets["sut"].sha256:
                self.targets["sut"].label = "frozen"
                self.frozen_only = True

        try:
            self.output.mkdir(parents=True, exist_ok=True)
            (self.output / "targets").mkdir(parents=True, exist_ok=True)
            self.fixture_root = Path(
                tempfile.mkdtemp(prefix="r14-fixtures-", dir=str(self.output))
            )
        except OSError as exc:
            raise SetupError("cannot create evidence tree under %s: %s"
                             % (self.output, exc))

    def load_target(self, label: str, path: Path, pinned: bool) -> Target:
        if not path.is_file() or not os.access(path, os.R_OK):
            raise SetupError("%s census not readable: %s" % (label, path))
        data = path.read_bytes()
        digest = sha256_bytes(data)
        if pinned:
            expected = PINNED_SHA256["mori-census.sh"]
            if digest != expected:
                raise SnapshotTampered(
                    "frozen census sha256=%s expected=%s" % (digest, expected)
                )
            self.crosscheck_manifest(digest)
        copy_dir = self.output / "targets"
        copy_dir.mkdir(parents=True, exist_ok=True)
        executed = copy_dir / ("%s.mori-census.sh" % label)
        executed.write_bytes(data)
        executed.chmod(0o755)
        if sha256_file(executed) != digest:
            raise SetupError("%s executed copy digest drifted" % label)
        return Target(label=label, original=path, executed=executed, sha256=digest)

    def crosscheck_manifest(self, digest: str) -> None:
        """Cross-check, never trust: a contradictory manifest is a pin error."""
        manifest = Path(self.args.frozen_dir).resolve() / "inputs.json"
        if not manifest.is_file():
            return
        try:
            declared = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise SnapshotTampered("unreadable frozen manifest: %s" % exc)
        got = declared.get("sha256", {}).get("mori-census.sh")
        if got and got != digest:
            raise SnapshotTampered(
                "manifest census sha256=%s differs from pinned bytes" % got
            )

    # -- run plumbing ------------------------------------------------------

    def run_process(self, run_id: str, argv, env, cwd, timeout: int):
        started = time.monotonic()
        timed_out = False
        error = None
        raw_out, raw_err, rc = "", "", None
        try:
            proc = subprocess.Popen(
                [str(x) for x in argv],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={str(k): str(v) for k, v in env.items()},
                cwd=str(cwd),
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
        safe_out = redact(raw_out or "")
        safe_err = redact(raw_err or "")
        out_path = self.output / "runs" / (run_id + ".stdout")
        err_path = self.output / "runs" / (run_id + ".stderr")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(safe_out, encoding="utf-8")
        err_path.write_text(safe_err, encoding="utf-8")
        self.runs.append({
            "run": run_id,
            "argv": [str(x) for x in argv],
            "cwd": str(cwd),
            "rc": rc,
            "timed_out": timed_out,
            "error": error,
            "duration_ms": duration_ms,
            "stdout_path": str(out_path),
            "stderr_path": str(err_path),
            "stdout_sha256": sha256_bytes(safe_out.encode()),
            "stderr_sha256": sha256_bytes(safe_err.encode()),
            "env": {k: v for k, v in sorted(env.items())
                    if k.startswith("MORI_") or k in ("PATH", "HOME", "TMPDIR")},
        })
        return raw_out or "", raw_err or "", rc, timed_out, error

    def run_case(self, target: Target, case: Case):
        self.index += 1
        fixture = self.fixture_root / ("case-%03d" % self.index)
        fixture.mkdir(parents=True, exist_ok=False)
        build_fixture(fixture, case)
        env = census_env(fixture)
        for key, value in case.env:
            env[key] = value
        run_id = "%s.%s" % (target.label, case.cid)
        raw_out, raw_err, rc, timed_out, error = self.run_process(
            run_id, ["bash", str(target.executed)], env, fixture,
            self.args.timeout,
        )
        argv_rows = read_argv_log(fixture / "journal" / "argv.log")
        tripwire_path = fixture / "journal" / "tripwire.log"
        tripwire = tripwire_path.read_text(encoding="utf-8", errors="replace") \
            if tripwire_path.is_file() else ""
        ok, reasons, observed = evaluate(
            case, raw_out, raw_err, rc, target.sha256, argv_rows, tripwire
        )
        if timed_out:
            reasons = list(reasons) + ["harness_timeout"]
            ok = False
        if error:
            reasons = list(reasons) + ["exec_error:%s" % error]
            ok = False
        return {
            "case": case.cid,
            "target": target.label,
            "run": run_id,
            "status": "pass" if ok else "fail",
            "reasons": reasons,
            "observed": observed,
            "census_sha256": target.sha256,
            "census_executed": str(target.executed),
            "census_source": str(target.original),
            "argv": ["bash", str(target.executed)],
            "rc": rc,
            "timed_out": timed_out,
            "journal_argv_calls": len(argv_rows),
            "tripwire": bool(tripwire.strip()),
            "fixture": str(fixture),
            "stdout_path": str(self.output / "runs" / (run_id + ".stdout")),
            "stderr_path": str(self.output / "runs" / (run_id + ".stderr")),
        }

    # -- orchestration -----------------------------------------------------

    def record_claim(self, case: Case, result: dict):
        self.claims.append({
            "id": case.cid,
            "title": case.title,
            "axis": "coverage",
            "status": result["status"],
            "target": result["target"],
            "run": result["run"],
            "details": one_line(
                "rc=%s verdict=%s drift=%s; %s"
                % (result["rc"],
                   result["observed"].get("verdict"),
                   result["observed"].get("counts", {}).get("drift"),
                   "; ".join(result["reasons"]) or "all expectations matched")
            ),
        })

    def run(self) -> int:
        self.prepare()
        sut = self.targets["sut"]
        frozen = self.targets.get("frozen")
        green_results = {}
        for case in self.cases:
            result = self.run_case(sut, case)
            green_results[case.cid] = result
            self.record_claim(case, result)

        frozen_results = {}
        frozen_claim = None
        if frozen is not None and not self.frozen_only:
            for case in self.cases:
                frozen_results[case.cid] = self.run_case(frozen, case)
            missing_red = [
                cid for cid in FROZEN_RED_REQUIRED
                if cid in frozen_results and frozen_results[cid]["status"] != "fail"
            ]
            frozen_claim = {
                "id": "R14_FROZEN_CONTROL",
                "title": "pinned frozen bytes reproduce every required defect",
                "axis": "coverage",
                "status": "pass" if not missing_red else "fail",
                "target": "frozen",
                "run": "frozen.*",
                "details": one_line(
                    "red_cases=%d required=%d missing=%s"
                    % (sum(1 for r in frozen_results.values()
                           if r["status"] == "fail"),
                       len(FROZEN_RED_REQUIRED),
                       ",".join(missing_red) or "none")
                ),
            }
            self.claims.append(frozen_claim)
            for case in self.cases:
                red = frozen_results[case.cid]
                green = green_results[case.cid]
                self.pairs.append({
                    "case": case.cid,
                    "red": {
                        "status": red["status"],
                        "rc": red["rc"],
                        "reasons": red["reasons"],
                        "stdout_sha256": sha256_bytes(
                            Path(red["stdout_path"]).read_bytes()),
                        "stderr_sha256": sha256_bytes(
                            Path(red["stderr_path"]).read_bytes()),
                    },
                    "green": {
                        "status": green["status"],
                        "rc": green["rc"],
                        "reasons": green["reasons"],
                        "stdout_sha256": sha256_bytes(
                            Path(green["stdout_path"]).read_bytes()),
                        "stderr_sha256": sha256_bytes(
                            Path(green["stderr_path"]).read_bytes()),
                    },
                })

        failed = [c for c in self.claims if c["status"] != "pass"]
        code = 1 if failed else 0
        self.emit(code, green_results, frozen_results, frozen_claim)
        return code

    # -- evidence ----------------------------------------------------------

    def emit(self, code, green_results, frozen_results, frozen_claim):
        for claim in self.claims:
            print(
                'FINDING %s status=%s axis=%s observed="%s"'
                % (claim["id"], claim["status"], claim["axis"], claim["details"])
            )
        for rec in sorted(self.runs, key=lambda r: r["run"]):
            print(
                "RUN %s rc=%s timeout=%s duration_ms=%d"
                % (rec["run"], rec["rc"], str(rec["timed_out"]).lower(),
                   rec["duration_ms"])
            )
        counts = {}
        for claim in self.claims:
            counts[claim["status"]] = counts.get(claim["status"], 0) + 1
        evidence = {
            "schema": SCHEMA,
            "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "mode": "red-before" if self.frozen_only else "strict-with-frozen-control",
            "targets": {
                label: {
                    "source": str(target.original),
                    "executed": str(target.executed),
                    "sha256": target.sha256,
                }
                for label, target in sorted(self.targets.items())
            },
            "harness": {
                "path": str(Path(__file__).resolve()),
                "sha256": sha256_file(Path(__file__).resolve()),
            },
            "pinned": {
                "base_commit": PINNED_BASE_COMMIT,
                "sha256": PINNED_SHA256,
                "crosschecked_manifest": str(
                    Path(self.args.frozen_dir).resolve() / "inputs.json"),
            },
            "claims": self.claims,
            "frozen_required_red": list(FROZEN_RED_REQUIRED),
            "pairs": self.pairs,
            "runs": sorted(self.runs, key=lambda r: r["run"]),
            "cases": {
                "green": green_results,
                "frozen": frozen_results,
            },
            "summary": {
                "claims": len(self.claims),
                "counts": counts,
                "exit": code,
                "frozen_control": frozen_claim["status"] if frozen_claim else "skipped",
            },
        }
        path = self.output / "evidence.json"
        json_dump(path, evidence)
        print(
            "MORI_R14_REGRESSIONS: claims=%d %s exit=%d"
            % (len(self.claims),
               " ".join("%s=%d" % (k, v) for k, v in sorted(counts.items())),
               code)
        )
        print("EVIDENCE %s" % path)
        print("GATE mori-round14-regressions (pinned frozen control)")


# ---------------------------------------------------------------------------
# selftest: pure parsers + the real gate over isolated fixtures
# ---------------------------------------------------------------------------


def selftest() -> int:
    failures = []
    checks = []

    def check(label, cond, detail=""):
        checks.append(label)
        if not cond:
            failures.append("%s%s" % (label, (": " + detail) if detail else ""))

    clean = "MORI_CENSUS: CLEAN (findings=3 drift=0 unavailable=1 surfaces=8)"
    drift = "MORI_CENSUS: DRIFT (findings=4 drift=2 unavailable=0 surfaces=8)"
    check("verdict-clean", verdict_roll(clean, 0)[:2] == ("CLEAN", "ok"))
    check("verdict-drift", verdict_roll(drift, 1)[:2] == ("DRIFT", "ok"))
    check("verdict-drift-count", verdict_roll(drift, 1)[2]["drift"] == 2)
    check("verdict-missing", verdict_roll("no roll", 0)[1] == "missing")
    check("verdict-inconsistent", verdict_roll(drift, 0)[1].startswith("inconsistent"))

    unit_row = " ".join("%s=0" % n for n in UNIT_TOKENS)
    sample = (
        "FINDING OOM_KILL_JOURNAL severity=crit obs=class=user_notice=1 "
        "system_notice=0 user_unit_oom=0 system_unit_oom=0 "
        "user_unit_oom_result_unknown=0 system_unit_oom_result_unknown=0 "
        "ts=x script_sha256=%s\n"
        "SURFACE journal.user: ok (scope=user kernel_oom_notice=1 oomd_notice=0 "
        "coredump_notice=0 segfault_signal11=0 unit_sigkill_record=0 "
        "unit_failure_record=0 %s boot=%s; rc=0)\n"
        "SURFACE journal.system: ok (scope=system kernel_oom_notice=0 "
        "oomd_notice=0 coredump_notice=0 segfault_signal11=0 "
        "unit_sigkill_record=0 unit_failure_record=0 %s boot=%s; rc=0)\n"
        % ("a" * 64, unit_row, JOURNAL_BOOT, unit_row, JOURNAL_BOOT)
    )
    rows = findings(sample)
    check("finding-parse", bool(rows) and rows[0]["id"] == OOM_ID)
    check("finding-sev", bool(rows) and rows[0]["sev"] == "crit")
    check("finding-sha", bool(rows) and rows[0]["script_sha256"] == "a" * 64)
    srows = surface_rows(sample)
    check("surface-scopes", set(srows) == {"user", "system"})
    check("surface-count", srows["user"][1].get("kernel_oom_notice") == "1")
    check("surface-no-sum", "total" not in srows["system"][1])
    check("surface-scope", srows["system"][1].get("scope") == "system")
    check("surface-unit-token", srows["user"][1].get("unit_oom") == "0")
    check("unit-token-count", len(UNIT_TOKENS) == 12)

    # Real gate invocation over the pinned frozen bytes. This is a red-before
    # run: the defective snapshot must fail and the gate must say so with the
    # stable case ids, not merely print helper results.
    tmp = Path(tempfile.mkdtemp(prefix="r14-selftest-"))
    base_env = {
        "PATH": "/usr/bin:/bin",
        "HOME": str(tmp / "home"),
        "TMPDIR": str(tmp / "tmp"),
        "TZ": "UTC",
        "LC_ALL": "C",
        "LANG": "C",
    }
    (tmp / "home").mkdir(parents=True, exist_ok=True)
    (tmp / "tmp").mkdir(parents=True, exist_ok=True)
    try:
        red_out = tmp / "red"
        proc = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()),
             "--census", str(DEFAULT_FROZEN),
             "--frozen", str(DEFAULT_FROZEN),
             "--output", str(red_out),
             "--timeout", "60",
             "--only", "R14_OOM_ALARM_USER,R14_UNIT_OOM_KILL,"
                       "R14_UNIT_FAILED_NONFLEET"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", errors="replace",
            env=base_env, cwd=str(tmp),
        )
        check("real-gate-red-rc", proc.returncode == 1,
              "rc=%s stderr=%s" % (proc.returncode, one_line(proc.stderr, 200)))
        check("real-gate-red-oom-id",
              "FINDING R14_OOM_ALARM_USER status=fail" in proc.stdout)
        check("real-gate-red-unit-id",
              "FINDING R14_UNIT_OOM_KILL status=fail" in proc.stdout)
        check("real-gate-red-evidence", (red_out / "evidence.json").is_file())

        tampered = tmp / "tampered-mori-census.sh"
        tampered.write_bytes(DEFAULT_FROZEN.read_bytes() + b"\n")
        tampered.chmod(0o755)
        tamper_out = tmp / "tamper"
        proc2 = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()),
             "--census", str(tampered),
             "--frozen", str(tampered),
             "--output", str(tamper_out),
             "--timeout", "60"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", errors="replace",
            env=base_env, cwd=str(tmp),
        )
        check("real-gate-tamper-rc", proc2.returncode == 2,
              "rc=%s" % proc2.returncode)
        check("real-gate-tamper-id",
              "R14_SNAPSHOT_TAMPERED" in (proc2.stdout + proc2.stderr))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if failures:
        print("SELFTEST: fail %s" % " | ".join(failures))
        return 1
    print("SELFTEST: pass checks=%d (parsers + real-gate red rc1/tamper rc2)"
          % len(checks))
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def write_tamper_evidence(args, exc) -> None:
    if not args.output:
        return
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)
    evidence = {
        "schema": SCHEMA,
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "mode": "setup",
        "finding": "snapshot_tampered",
        "observed": one_line(exc),
        "pinned": {"base_commit": PINNED_BASE_COMMIT, "sha256": PINNED_SHA256},
        "summary": {"claims": 1, "counts": {"fail": 1}, "exit": 2},
    }
    json_dump(out / "evidence.json", evidence)
    print("EVIDENCE %s" % (out / "evidence.json"))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Round-14 isolated journal regression gate "
                    "(red-before frozen control + green repaired census).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--census", default=str(DEFAULT_CENSUS),
                    help="census under test (default tools/mori-census.sh)")
    ap.add_argument("--output", help="required evidence directory")
    ap.add_argument("--frozen", default=None,
                    help="pinned red census (default .ufo/waves/round-14/frozen/mori-census.sh)")
    ap.add_argument("--frozen-dir", default=str(DEFAULT_FROZEN_DIR),
                    help="directory holding the committed frozen manifest")
    ap.add_argument("--no-frozen-control", action="store_true",
                    help="skip the red control (green-only measurement)")
    ap.add_argument("--timeout", type=int, default=60,
                    help="per-census timeout seconds (default 60)")
    ap.add_argument("--only", default=None,
                    help="comma-separated case ids for a focused run")
    ap.add_argument("--keep-fixtures", action="store_true",
                    help="retain fixture trees under --output")
    ap.add_argument("--selftest", action="store_true",
                    help="parse checks + real gate red/tamper invocations")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if not args.output:
        ap.error("--output is required")
    if args.timeout <= 0:
        ap.error("--timeout must be positive")

    harness = None
    try:
        harness = Harness(args)
        code = harness.run()
    except SnapshotTampered as exc:
        print('FINDING R14_SNAPSHOT_TAMPERED status=fail axis=coverage '
              'observed="%s"' % one_line(exc))
        print("MORI_R14_REGRESSIONS: setup snapshot_tampered exit=2")
        try:
            write_tamper_evidence(args, exc)
        except OSError as werr:
            print("mori-round14-regressions: evidence write failed: %s" % werr,
                  file=sys.stderr)
        code = 2
    except SetupError as exc:
        print('FINDING R14_SETUP status=fail axis=operability observed="%s"'
              % one_line(exc))
        print("MORI_R14_REGRESSIONS: setup %s exit=2" % one_line(exc, 120))
        code = 2
    except KeyboardInterrupt:
        print("mori-round14-regressions: interrupted", file=sys.stderr)
        code = 2
    finally:
        if harness is not None and harness.fixture_root \
                and not args.keep_fixtures:
            shutil.rmtree(harness.fixture_root, ignore_errors=True)
    return code


if __name__ == "__main__":
    sys.exit(main())
