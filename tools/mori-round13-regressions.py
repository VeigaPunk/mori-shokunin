#!/usr/bin/env python3
"""mori-round13-regressions.py — isolated integration regressions for round 13.

EVIDENCE HARNESS, NOT A GATE. It is deliberately not registered in any gate
registry; it exists so the round-13 claims can be re-measured from committed
inputs with their original commands and outputs retained. If an operator later
registers it, `--selftest` covers the harness's own pure verdict/parser logic
and touches no repository path.

Claims measured (stable ids; one FINDING line each)

  R13_SHONEN_CANONICAL_BYTES            canonical HEAD SHONEN bytes (unindented)
  R13_SHONEN_INDENT_WITNESS             the comparator rejects indented bytes
  R13_C1_SYSTEM_NOTICE_COUNTS           system scope: structured MESSAGE_ID counts
  R13_C1_USER_SCOPE_INDEPENDENT         user scope: separate zero tokens, never summed
  R13_C1_USER_SCOPE_NONZERO             user-only fixture counts stay on user tokens
  R13_C1_NO_MESSAGE_TEXT                no synthetic MESSAGE key/value in stdout
  R13_C1_CLEAN_VERDICT                  notices INFO => exactly one CLEAN/rc0 roll
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
  * The C1 fixture serves synthetic `journalctl -o json` records keyed by the
    exact argv CensusFix documented (scope + MESSAGE_ID / COREDUMP_SIGNAL).
    The synthetic MESSAGE value is a canary; the host journal is never opened.
  * Every fixture is created under a fresh temp directory inside the explicit
    --output tree, never under the repository and never at a live MORI path,
    and removed after the run unless --keep-fixtures.

Modes

  default          strict contract: every claim must pass.
  --baseline       run the frozen pre-fix bytes (or the paths given) once and
                   *record* the audit-predicted defects. Expected defects are
                   reported as `expected-defect`, never `pass`; an observation
                   that does not match the baseline table is `baseline-deviation`.
  --mutation ID    run the strict suite, then transplant the named frozen
                   function body into an isolated copy of the fixed target and
                   require the pre-fix defect to reappear. IDs: f01, f02, both.

Exit codes

  0  every claim satisfied in the selected mode
  1  a claim failed (or a baseline observation deviated)
  2  usage / setup error
  3  all contract claims held but a requested mutation could not be built

Evidence: <output>/evidence.json plus <output>/runs/<run-id>.{stdout,stderr}.
Synthetic canary text is redacted before anything is written.
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

SCHEMA = "mori-round13-regressions-v1"
REPO = Path(__file__).resolve().parent.parent
DEFAULT_CENSUS = REPO / "tools/mori-census.sh"
DEFAULT_ORACLE = REPO / "tools/mori-silence-cases.sh"
DEFAULT_FROZEN = REPO / ".ufo/waves/round-13/frozen"
DEFAULT_SHONEN = REPO / "SHONEN.md"

NOW_EPOCH = 1700000000
LAUNCH_EPOCH = 1699998000
LANE = "kagi"
ROUND = "7"
HISTORY_SIBLINGS = 12000

KERNEL_ID = "fe6faa94e7774663a0da52717891d8ef"
OOMD_ID = "d989611b15e44c9dbf31e3c81256e4ed"
COREDUMP_ID = "fc2e22bc6ee647b6b90729ab34a250b1"
MESSAGE_IDS = (KERNEL_ID, OOMD_ID, COREDUMP_ID)
JOURNAL_BOOT = "0123456789abcdef0123456789abcdef"
CANARY = "R13-SYNTHETIC-JOURNAL-MESSAGE-CANARY"

# CensusFix round-13 surface rows (corrected 2026-10-20): TWO rows, six
# classes, boot-anchored, no summed field.
#   SURFACE journal.user: ok (... scope=user kernel_oom_notice=N ... ;
#                              boot=<32 lowercase hex>; unit=notice ...)
#   SURFACE journal.system: (same, scope=system)
C1_SURFACE_TOKENS = (
    ("kernel_oom_notice", KERNEL_ID, "kernel"),
    ("oomd_notice", OOMD_ID, "oomd"),
    ("coredump_notice", COREDUMP_ID, "coredump"),
    ("segfault_signal11", None, "segfault"),
)
C1_RECORD_TOKENS = ("unit_sigkill_record", "unit_failure_record")
C1_SYSTEM_COUNTS = {
    "kernel": 2,
    "oomd": 1,
    "coredump": 3,
    "segfault": 3,  # the three coredump records carry COREDUMP_SIGNAL=11
}
C1_USER_COUNTS = {
    "kernel": 3,
    "oomd": 0,
    "coredump": 1,
    "segfault": 1,  # the single user coredump record carries COREDUMP_SIGNAL=11
}
C1_FINDINGS = {
    "system": {
        "KERNEL_OOM_NOTICE_JOURNAL_SYSTEM": ("kernel", 2),
        "OOMD_NOTICE_JOURNAL_SYSTEM": ("oomd", 1),
        "COREDUMP_NOTICE_JOURNAL_SYSTEM": ("coredump", 3),
        "SEGFAULT_SIGNAL11_JOURNAL_SYSTEM": ("segfault", 3),
    },
    "user": {
        "KERNEL_OOM_NOTICE_JOURNAL_USER": ("kernel", 0),
        "OOMD_NOTICE_JOURNAL_USER": ("oomd", 0),
        "COREDUMP_NOTICE_JOURNAL_USER": ("coredump", 0),
        "SEGFAULT_SIGNAL11_JOURNAL_USER": ("segfault", 0),
    },
}
UNMEASURED_CLASSES = ("oom_kill_text", "other_signals", "other_unit_failure_text")

VERDICT_RE = re.compile(
    r"^MORI_CENSUS: (CLEAN|DRIFT) "
    r"\(findings=[0-9]+ drift=[0-9]+ unavailable=[0-9]+ surfaces=[0-9]+\)$"
)
SURFACE_JOURNAL_RE = re.compile(r"^SURFACE journal: (\S+) \((.*)\)\s*$", re.M)
SURFACE_SCOPED_RE = re.compile(
    r"^SURFACE journal\.(user|system): (\S+) \((.*)\)\s*$", re.M
)
LANE_ROW_RE = re.compile(r"^SURFACE lane\.(\w+): (\S+) \((.*)\)\s*$", re.M)
FINDING_RE = re.compile(r"^FINDING (\w+) (\w+) (.*)$", re.M)
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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def one_line(text, limit=240) -> str:
    text = " ".join(str(text).replace(CANARY, "<canary>").split())
    if len(text) > limit:
        text = text[: limit - 3] + "..."
    return text


def redact(text: str) -> str:
    return text.replace(CANARY, "<canary-redacted>")


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


def surface_body(out: str, name: str = "journal"):
    m = SURFACE_JOURNAL_RE.search(out) if name == "journal" else None
    if not m:
        return None, {}
    return m.group(1), dict(TOKEN_RE.findall(m.group(2)))


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


def journal_stub_body(system_counts: dict, user_counts: dict, message_mode: str) -> str:
    """Synthetic journalctl with independent system and user scopes.

    Keys output by argv exactly as CensusFix documented: scope (--user/--system)
    and either MESSAGE_ID=<id> or COREDUMP_SIGNAL=11. A mismatched id yields no
    records (rc 0), so a fixed-record stub cannot masquerade as a valid answer.
    Text mode carries neither ids nor class words: only the structured path can
    observe this fixture, which is the C1 point.
    """

    def blocks(counts: dict):
        emit_all = []
        emit_cases = []
        for token, mid, kind in C1_SURFACE_TOKENS:
            if mid is None:
                continue
            n = int(counts.get(kind, 0))
            emit_all.append("      emit %s %d %s" % (mid, n, kind))
            emit_cases.append("        %s) emit %s %d %s ;;" % (mid, mid, n, kind))
        return "\n".join(emit_all), "\n".join(emit_cases)

    system_all, system_cases = blocks(system_counts)
    user_all, user_cases = blocks(user_counts)
    template = r"""#!/usr/bin/env bash
# Synthetic structured journal for mori round-13 regressions.
# Never opens the host journal. One JSON object per line, no MESSAGE unless the
# probe's --output-fields asks for it (or leak mode forces the key).
canary='@CANARY@'
boot='@BOOT@'
json=0; user=0; fields=''; want=(); signal11=0; fieldq=0
for a in "$@"; do
  case "$a" in
    --user) user=1 ;;
    --system) user=0 ;;
    --output-fields=*) fields=${a#--output-fields=} ;;
    *json*) json=1 ;;
    MESSAGE_ID=*) want+=("${a#MESSAGE_ID=}"); fieldq=1 ;;
    COREDUMP_SIGNAL=11) signal11=1; fieldq=1 ;;
    [A-Z_]*=*) fieldq=1 ;;
  esac
done
show_message=1
if [ '@MODE@' = honor ] && [ -n "$fields" ]; then
  case ",$fields," in *,MESSAGE,*) ;; *) show_message=0 ;; esac
fi
emit() { # <id> <n> <kind>
  local id=$1 n=$2 kind=$3 i msg='' extra=''
  [ "$n" -gt 0 ] || return 0
  if [ "$show_message" = 1 ]; then
    msg=',"MESSAGE":"'"$canary"'"'
  fi
  if [ "$kind" = coredump ]; then
    extra=',"COREDUMP_SIGNAL":"11"'
  fi
  for ((i=0; i<n; i++)); do
    printf '{"__CURSOR":"s=r13_%s_%s_%s","__REALTIME_TIMESTAMP":"1700000000000000","__MONOTONIC_TIMESTAMP":"1000","_BOOT_ID":"%s","_TRANSPORT":"journal","MESSAGE_ID":"%s"%s%s}\n' \
      "$kind" "$id" "$i" "$boot" "$id" "$extra" "$msg"
  done
}
if [ "$json" = 1 ]; then
  if [ "$user" = 1 ]; then
    if [ ${#want[@]} -gt 0 ]; then
      for id in "${want[@]}"; do
        case "$id" in
@USER_EMIT_CASES@
        esac
      done
    elif [ "$signal11" = 1 ]; then
      emit @COREDUMP@ @USER_COREDUMP_N@ coredump
    elif [ "$fieldq" = 1 ]; then
      : # a structured filter with no fixture match: zero records, rc 0
    else
@USER_EMIT_ALL@
    fi
  else
    if [ ${#want[@]} -gt 0 ]; then
      for id in "${want[@]}"; do
        case "$id" in
@EMIT_CASES@
        esac
      done
    elif [ "$signal11" = 1 ]; then
      emit @COREDUMP@ @COREDUMP_N@ coredump
    elif [ "$fieldq" = 1 ]; then
      : # a structured filter with no fixture match: zero records, rc 0
    else
@EMIT_ALL@
    fi
  fi
else
  if [ "$user" = 0 ]; then
    printf '+-- Journal begins at 2026-10-14, ends at 2026-10-19. --+\n'
  fi
fi
exit 0
"""
    return (
        template.replace("@CANARY@", CANARY)
        .replace("@BOOT@", JOURNAL_BOOT)
        .replace("@MODE@", message_mode)
        .replace("@COREDUMP@", COREDUMP_ID)
        .replace("@COREDUMP_N@", str(int(system_counts.get("coredump", 0))))
        .replace("@USER_COREDUMP_N@", str(int(user_counts.get("coredump", 0))))
        .replace("@USER_EMIT_ALL@", user_all)
        .replace("@USER_EMIT_CASES@", user_cases)
        .replace("@EMIT_ALL@", system_all)
        .replace("@EMIT_CASES@", system_cases)
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
    write_exec(base / "bin" / "journalctl", journal_stub_body({}, {}, "honor"))


def build_journal_fixture(base: Path, message_mode: str,
                          system_counts=None, user_counts=None) -> None:
    build_common(base)
    system_counts = C1_SYSTEM_COUNTS if system_counts is None else system_counts
    user_counts = {} if user_counts is None else user_counts
    write_exec(base / "bin" / "git", git_stub_body(True, 0))
    write_exec(
        base / "bin" / "journalctl",
        journal_stub_body(system_counts, user_counts, message_mode),
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
        A mismatch raises SnapshotTampered; main emits the stable token
        `snapshot_tampered` with setup rc2.
        """
        frozen_map = {}
        inputs_hash = None
        frozen_dir = Path(self.args.frozen_dir).resolve()
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

    def prepare(self) -> None:
        if not CANONICAL_SHONEN:
            raise SetupError("canonical SHONEN seed is empty")
        if sha256_bytes(CANONICAL_SHONEN.encode()) != CANONICAL_SHONEN_SHA256:
            raise SetupError("canonical SHONEN seed digest drifted from its constant")
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
            try:
                stdout, stderr = proc.communicate(timeout=timeout)
                rc = proc.returncode
            except subprocess.TimeoutExpired:
                timed_out = True
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                except ProcessLookupError:
                    pass
                stdout, stderr = proc.communicate()
                rc = proc.returncode
        duration_ms = int((time.monotonic() - started) * 1000)
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
        fixture = self.fixture("c1-journal")
        build_journal_fixture(fixture, "honor")
        primary = self.run_census("c1.primary", fixture)
        # Leak probe: the stub ignores --output-fields and forces a MESSAGE key
        # into every JSON object. A parser that echoes raw records leaks the
        # canary; a parser that projects only counts does not.
        leak_fixture = self.fixture("c1-journal-leak")
        build_journal_fixture(leak_fixture, "always")
        leak = self.run_census("c1.leak", leak_fixture)
        # Independent user arm: nonzero user counts prove the scopes are not
        # conflated (the zero arm alone cannot distinguish "separate" from
        # "omitted").
        user_fixture = self.fixture("c1-journal-user")
        build_journal_fixture(
            user_fixture, "honor",
            system_counts={},
            user_counts=C1_USER_COUNTS,
        )
        user_run = self.run_census("c1.user", user_fixture)

        out = primary["stdout"]
        srows = surface_rows(out)
        verdict_word, verdict_reason, _ = verdict_roll(out, primary["rc"])
        rows = findings(out)
        zero_counts = {kind: 0 for kind in C1_SYSTEM_COUNTS}

        def scoped(rows_map, scope, expected):
            """Check one scoped row's six class tokens, boot and no-sum shape."""
            state, tokens = rows_map.get(scope, (None, {}))
            ok = state == "ok"
            observed = []
            for stem, mid, kind in C1_SURFACE_TOKENS:
                got = tokens.get(stem)
                observed.append("%s=%s" % (stem, got if got is not None else "<absent>"))
                if got != str(expected[kind]):
                    ok = False
            for name in C1_RECORD_TOKENS:
                got = tokens.get(name)
                observed.append("%s=%s" % (name, got if got is not None else "<absent>"))
                if got != "0":
                    ok = False
            all_zero = all(
                tokens.get(stem) == "0" for stem, mid, kind in C1_SURFACE_TOKENS
            ) and all(tokens.get(name) == "0" for name in C1_RECORD_TOKENS)
            boot = tokens.get("boot")
            # The landed probe emits the validated boot only when a record was
            # seen; an all-zero scope has no record, so it renders
            # `unavailable:no-records`. That is the correct zero anchor, not a
            # boot mismatch (a mismatched record grades the class unavailable).
            if not (boot == JOURNAL_BOOT or
                    (all_zero and boot == "unavailable:no-records")):
                ok = False
            if tokens.get("scope") not in (None, scope):
                ok = False
            if "total" in tokens or "sum" in tokens:
                ok = False
            return ok, state, tokens, observed

        system_ok, state, stokens, system_observed = scoped(
            srows, "system", C1_SYSTEM_COUNTS
        )
        for fid, (kind, count) in C1_FINDINGS["system"].items():
            if count > 0 and not any(
                r[0] == fid and r[2].get("count") == str(count) for r in rows
            ):
                system_ok = False
        if primary["rc"] != 0 or primary["timed_out"]:
            system_ok = False
        if self.args.baseline:
            # Pre-fix has no scoped structured rows: absent counts are the
            # expected defect; an unexpected full pass is a baseline deviation.
            status = EXPECTED_DEFECT if not system_ok else BASELINE_DEVIATION
        else:
            status = PASS if system_ok else FAIL
        self.claim(
            "R13_C1_SYSTEM_NOTICE_COUNTS", status, "coverage",
            "expected [%s]; observed [%s]; state=%s rc=%s system_findings=%s"
            % (
                " ".join("%s=%d" % (stem, C1_SYSTEM_COUNTS[kind])
                         for stem, mid, kind in C1_SURFACE_TOKENS),
                " ".join(system_observed), state, primary["rc"],
                ",".join(f for f, s, t, r in rows if f.endswith("_SYSTEM")) or "none",
            ),
            run_ids=["c1.primary"],
        )

        # User scope zero arm: an independent row with zero class tokens, its
        # own boot anchor, and no summed field. No user finding at zero.
        user_ok, ustate, utokens, user_observed = scoped(srows, "user", zero_counts)
        if "user" not in srows:
            user_ok = False
        if any(fid.endswith("_USER") for fid, sev, tok, rest in rows):
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

        # User scope nonzero arm: the same fixture machinery with only user
        # records. Counts must land on the user row while every system class
        # stays 0; the rows are never summed.
        nrows = surface_rows(user_run["stdout"])
        nu_ok, nustate, nutokens, nuser_observed = scoped(
            nrows, "user", C1_USER_COUNTS
        )
        ns_ok, nsstate, nstokens, nsystem_observed = scoped(
            nrows, "system", zero_counts
        )
        unonzero_ok = nu_ok and ns_ok
        urows = findings(user_run["stdout"])
        for fid, (kind, count) in C1_FINDINGS["user"].items():
            match = [
                r for r in urows
                if r[0] == fid and r[2].get("count") == str(count)
            ]
            if count > 0 and not match:
                unonzero_ok = False
            if count == 0 and any(r[0] == fid for r in urows):
                unonzero_ok = False
        if any(fid.endswith("_SYSTEM") for fid, sev, tok, rest in urows):
            unonzero_ok = False
        uword, ureason, _ = verdict_roll(user_run["stdout"], user_run["rc"])
        if uword != "CLEAN" or ureason != "ok" or user_run["rc"] != 0:
            unonzero_ok = False
        if self.args.baseline:
            status_u = EXPECTED_DEFECT if not unonzero_ok else BASELINE_DEVIATION
        else:
            status_u = PASS if unonzero_ok else FAIL
        self.claim(
            "R13_C1_USER_SCOPE_NONZERO", status_u, "coverage",
            "fixture user=%s; user=[%s] state=%s; system=[%s] state=%s; "
            "verdict=%s/%s rc=%s"
            % (C1_USER_COUNTS, " ".join(nuser_observed), nustate,
               " ".join(nsystem_observed), nsstate, uword, ureason,
               user_run["rc"]),
            run_ids=["c1.user"],
        )

        # MESSAGE-free output, on both the honoring and the leak-forcing stub.
        message_text_ok = True
        leak_notes = []
        for label, rec in (("primary", primary), ("leak", leak)):
            blob = rec["stdout"] + "\n" + rec["stderr"]
            if CANARY in blob:
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

        # Verdict: notices are INFO, so exactly one well-formed CLEAN matching
        # rc 0; the unmeasured kill classes are named, never counted, and the
        # two rows are separately shaped.
        coverage_finding = any(
            fid == "JOURNAL_CLASSES_UNMEASURED" and sev == "info"
            for fid, sev, tok, rest in rows
        )
        row_shape_ok = "system" in srows and "user" in srows
        for scope in ("system", "user"):
            rstate, rtokens = srows.get(scope, (None, {}))
            unmeasured = rtokens.get("unmeasured", "")
            all_zero = all(
                rtokens.get(stem) == "0" for stem, mid, kind in C1_SURFACE_TOKENS
            ) and all(rtokens.get(name) == "0" for name in C1_RECORD_TOKENS)
            boot = rtokens.get("boot")
            if rstate != "ok":
                row_shape_ok = False
            if rtokens.get("unit") != "notice":
                row_shape_ok = False
            if rtokens.get("field") != "user:MESSAGE_ID":
                row_shape_ok = False
            if not all(cls in unmeasured for cls in UNMEASURED_CLASSES):
                row_shape_ok = False
            if rtokens.get("rc") != "0":
                row_shape_ok = False
            if not (boot == JOURNAL_BOOT or
                    (all_zero and boot == "unavailable:no-records")):
                row_shape_ok = False
        kill_rows = [
            fid for fid, sev, tok, rest in rows
            if fid in (
                "OOM_KILL_JOURNAL",
                "KILL_SIGNAL_JOURNAL",
                "KILL_SIGNAL_JOURNAL_SYSTEM",
                "UNIT_FAILURE_JOURNAL",
                "UNIT_FAILURE_JOURNAL_SYSTEM",
                "UNIT_FAILURE_OUT_OF_SCOPE",
            )
            and count_value(tok) > 0
        ]
        clean_verdict_ok = (
            verdict_word == "CLEAN" and verdict_reason == "ok"
            and primary["rc"] == 0
        )
        clean_full_ok = (
            clean_verdict_ok
            and row_shape_ok
            and coverage_finding
            and not kill_rows
        )
        if self.args.baseline:
            # The roll itself is the baseline observation; the C1 schema is
            # the expected pre-fix gap, so a clean roll without it is an
            # expected defect, never a contract pass.
            status = (
                BASELINE_OK if clean_full_ok
                else EXPECTED_DEFECT if clean_verdict_ok
                else BASELINE_DEVIATION
            )
        else:
            status = PASS if clean_full_ok else FAIL
        self.claim(
            "R13_C1_CLEAN_VERDICT", status, "coverage",
            "verdict=%s reason=%s rc=%s rows=%s row_shape=%s "
            "coverage_finding=%s positive_kill_rows=%s"
            % (verdict_word, verdict_reason, primary["rc"],
               ",".join(sorted(srows)) or "none",
               "yes" if row_shape_ok else "no",
               "yes" if coverage_finding else "no",
               ",".join(kill_rows) or "none"),
            run_ids=["c1.primary"],
        )

    # -- F01 -----------------------------------------------------------------

    def f01_arm(self, run_id: str, subject: bool) -> dict:
        fixture = self.fixture("f01-" + ("subject" if subject else "sibling"))
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
                fixture = self.fixture("mutation-f01")
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
                    "transplanted %s: state=%s basis=%s other=%s verdict=%s/%s rc=%s; "
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
                    "transplanted %s: matched=%s total=%s rc=%s; expected pre-fix "
                    "BANANA accepted 28/28"
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
            code = 3
        else:
            code = 0
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
        evidence = {
            "schema": SCHEMA,
            "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
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
            },
            "entropy": {"shuffle_seed": self.args.seed, "run_nonce": self.args.nonce},
            "claims": self.claims,
            "runs": sorted(self.runs, key=lambda r: r["id"]),
            "mutations": getattr(self, "mutations", []),
            "summary": {
                "claims": len(self.claims),
                "counts": counts,
                "exit": code,
                "gate": "not-registered (evidence harness)",
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
        print("GATE not-registered (evidence harness; --selftest available)")


# ---------------------------------------------------------------------------
# selftest (pure logic; no repository path is read or written)
# ---------------------------------------------------------------------------


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
        "unit=notice field=user:MESSAGE_ID; "
        "unmeasured=oom_kill_text,other_signals,other_unit_failure_text; rc=0; ts=x)\n"
        "SURFACE journal.system: ok (scope=system kernel_oom_notice=2 "
        "oomd_notice=1 coredump_notice=3 segfault_signal11=3 "
        "unit_sigkill_record=0 unit_failure_record=0; boot=0123; "
        "unit=notice field=user:MESSAGE_ID; "
        "unmeasured=oom_kill_text,other_signals,other_unit_failure_text; rc=0; ts=x)\n"
    )
    rows = surface_rows(scoped_out)
    check("scoped-two-rows", set(rows) == {"user", "system"})
    check("scoped-user-zero", rows.get("user", ("", {}))[1].get("kernel_oom_notice") == "0")
    check("scoped-system-count", rows.get("system", ("", {}))[1].get("kernel_oom_notice") == "2")
    check("scoped-boot", rows.get("user", ("", {}))[1].get("boot") == "0123")
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
    if failures:
        print("SELFTEST: fail %s" % " ".join(failures))
        return 1
    print("SELFTEST: pass checks=%d" % len(checks))
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
    evidence = {
        "schema": SCHEMA,
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
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
            "gate": "not-registered (evidence harness)",
        },
    }
    path = out / "evidence.json"
    json_dump(path, evidence)
    print("EVIDENCE %s" % path)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Round-13 isolated integration regressions (evidence harness).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--census", help="census under test (default tools/mori-census.sh)")
    ap.add_argument("--oracle", help="oracle under test (default tools/mori-silence-cases.sh)")
    ap.add_argument("--output", help="required evidence directory (created if absent)")
    ap.add_argument("--baseline", action="store_true",
                    help="record frozen pre-fix defects; never marks the new contract pass")
    ap.add_argument("--mutation", choices=("none", "f01", "f02", "both"), default="none",
                    help="after the strict suite, transplant the frozen function back")
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
                    help="run pure harness logic checks only (no repository paths read)")
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
    finally:
        harness.cleanup()
    return code


if __name__ == "__main__":
    sys.exit(main())
