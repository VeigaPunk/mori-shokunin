#!/usr/bin/env bash
# mori round-26 capture.sh — read-only host capture for FR10 (userspace OOM
# killers: earlyoom and systemd-oomd).
#
# Usage: capture.sh OUTPUT_FILE
#   Writes exactly one file: OUTPUT_FILE (truncated at start). No other path
#   is created, and nothing else on the host is written.
#
# Read-only by construction. The only commands run are queries:
#   uname -r
#   systemctl --version | head -1
#   pacman -Q earlyoom systemd             (query only, no database change)
#   systemctl is-active / is-enabled        (earlyoom.service, systemd-oomd.service)
#   systemctl show -p <properties>          (read-only property query)
#   journalctl -q -b -u earlyoom.service -o json --output-fields=MESSAGE
#   journalctl -q -b MESSAGE_ID=<id> -o json --output-fields=MESSAGE_ID
# No unit is started, stopped, enabled, disabled or masked; no package is
# installed, removed or downgraded; no configuration file is read into the
# output; no network access.
#
# Privacy. The daemon's process-selection expressions, the unit ExecStart
# command line and the contents of the daemon's default configuration file
# are never read into the output. The daemon journal is consumed in memory:
# journalctl writes the bodies to a pipe and python3 reads them there,
# emitting only derived lines. Exactly three journal-derived text lines may
# reach the output (the version line and the two threshold lines); every
# other journal fact is written as a count.
#
# Error handling. Only `set -u` is used: there is no `set -e` and no
# `set -o pipefail`, so a failing probe is reported rather than aborting the
# run, and no pipeline failure is masked by a later stage. Every probe
# records its own exit status next to its value, so "unavailable" and
# "zero" stay distinguishable. A missing probe never becomes a zero.

set -u

OUT=${1:-}
if [ -z "${OUT}" ]; then
    printf 'usage: %s OUTPUT_FILE\n' "${0##*/}" >&2
    exit 2
fi

exec 3>"${OUT}"

rec() {
    printf 'ts=%s %s\n' "$(date --iso-8601=seconds)" "$1" >&3
}

# --- header ---------------------------------------------------------------

rec "# mori round-26 FR10 host capture (userspace OOM killers)"
rec "capture_script=.ufo/waves/round-26/capture/capture.sh"
rec "capture_started=$(date --iso-8601=seconds)"
rec "capture_scope=current boot; earlyoom.service and systemd-oomd.service"

# --- kernel and versions --------------------------------------------------

uname_r=$(uname -r 2>/dev/null); rc=$?
rec "uname_release=${uname_r} uname_rc=${rc}"

sv=$(systemctl --version 2>/dev/null); rc=$?
sv_first=$(printf '%s\n' "${sv}" | head -n 1)
rec "systemd_version_line=${sv_first} systemd_version_rc=${rc}"

pq=$(pacman -Q earlyoom systemd 2>/dev/null); rc=$?
rec "pacman_query_rc=${rc}"
printf '%s\n' "${pq}" | while IFS= read -r line; do
    [ -n "${line}" ] || continue
    name=${line%% *}
    ver=${line#* }
    rec "package_${name}=${ver}"
done

# --- unit state -----------------------------------------------------------

for unit in earlyoom.service systemd-oomd.service; do
    v=$(systemctl is-active "${unit}" 2>/dev/null); rc=$?
    rec "unit_${unit}_is_active=${v} unit_${unit}_is_active_rc=${rc}"
    v=$(systemctl is-enabled "${unit}" 2>/dev/null); rc=$?
    rec "unit_${unit}_is_enabled=${v} unit_${unit}_is_enabled_rc=${rc}"
done

show=$(systemctl show earlyoom.service systemd-oomd.service \
    -p Id,LoadState,ActiveState,UnitFileState,ActiveEnterTimestampMonotonic 2>/dev/null); rc=$?
rec "unit_show_rc=${rc}"
printf '%s\n' "${show}" | while IFS= read -r line; do
    [ -n "${line}" ] || continue
    key=${line%%=*}
    val=${line#*=}
    rec "unit_show_${key}=${val}"
done

# --- managed OOM policy of the user scopes --------------------------------
#
# systemctl prints one blank-line separated block per unit, in the order the
# units were given on the command line (verified by re-running the same
# query with Id added). The unit order is recorded next to the values so the
# attribution can be checked against the command. `--` is required so the "-"
# prefixed unit name is not read as an option.

moo_units='user@1000.service,user-1000.slice,user.slice,-.slice'
moo=$(systemctl show -p ManagedOOMSwap,ManagedOOMMemoryPressure -- \
    user@1000.service user-1000.slice user.slice -.slice 2>/dev/null); rc=$?
rec "managed_oom_show_rc=${rc} managed_oom_show_units=${moo_units}"
printf '%s\n' "${moo}" | awk -v units="${moo_units}" -v ts="$(date --iso-8601=seconds)" '
    BEGIN { n = split(units, u, ","); idx = 1; block = 0 }
    /^[[:space:]]*$/ {
        if (block > 0) { idx++; block = 0 }
        next
    }
    {
        block++
        eq = index($0, "=")
        prop = substr($0, 1, eq - 1)
        val = substr($0, eq + 1)
        if (idx <= n) printf "ts=%s managed_oom_%s_%s=%s\n", ts, u[idx], prop, val
    }
    END { printf "ts=%s managed_oom_blocks=%d managed_oom_units_listed=%d\n", ts, idx - (block > 0 ? 0 : 1), n }
' >&3

# --- earlyoom journal, current boot ---------------------------------------
#
# The journal bodies never reach the output file: journalctl writes them to
# the pipe and python3 reads them in memory, emitting only derived lines.

scope_start=$(systemctl show earlyoom.service -p ActiveEnterTimestampMonotonic --value 2>/dev/null); rc=$?
rec "earlyoom_scope_start_monotonic=${scope_start} earlyoom_scope_start_rc=${rc}"

# The reader program is held in a shell variable, not in a heredoc, so the
# script creates no temporary file: the only path it writes is $1.
PYCODE='
import json
import re
import sys

scope_raw = sys.argv[1] if len(sys.argv) > 1 else ""
try:
    scope_start = int(scope_raw)
except (TypeError, ValueError):
    scope_start = None

RE_VERSION = re.compile(r"^earlyoom ([0-9A-Za-z][^\s]*)$")
RE_TERM = re.compile(r"^sending SIGTERM when mem avail <= *([0-9.]+)% and swap free <= *([0-9.]+)%")
RE_KILL = re.compile(r"^SIGKILL when mem avail <= *([0-9.]+)% and swap free <= *([0-9.]+)%")

PREFIX_COUNTS = [
    ("sending_sigterm_to_process", "sending SIGTERM to process "),
    ("sending_sigkill_to_process", "sending SIGKILL to process "),
    ("escalating", "escalating to SIGKILL after "),
    ("kill_failed", "kill failed: "),
    ("low_memory_sigterm", "low memory! at or below SIGTERM limits"),
    ("low_memory_sigkill", "low memory! at or below SIGKILL limits"),
    ("mem_avail_report", "mem avail: "),
    ("dryrun_enabled", "dryrun mode enabled"),
    # kill.c:282 at v1.9.0 -- one send line under -g signals a whole group.
    ("process_group_lines", "killing whole process group "),
    # earlyoom counts the messages it did not forward to the journal.
    ("suppressed_messages", "Suppressed "),
]

# A "Suppressed " line only counts when it also names the unit the messages
# were dropped for, so an unrelated line that happens to start with the same
# word is not counted as a suppressed-message record.
SUPPRESSED_MARK = " messages from " + "earlyoom.service"


def decode(value):
    """journalctl may hand MESSAGE over as a string or as a byte array."""
    if isinstance(value, str):
        return value
    if isinstance(value, (list, tuple)):
        try:
            return bytes(bytearray(value)).decode("utf-8", "replace")
        except Exception:
            return ""
    return ""


entries = []
for raw in sys.stdin:
    raw = raw.strip()
    if not raw:
        continue
    try:
        obj = json.loads(raw)
    except ValueError:
        continue
    if not isinstance(obj, dict):
        continue
    mono = obj.get("__MONOTONIC_TIMESTAMP")
    try:
        mono = int(mono)
    except (TypeError, ValueError):
        mono = None
    entries.append((mono, decode(obj.get("MESSAGE")).strip()))

unknown_mono = sum(1 for mono, _ in entries if mono is None)
if scope_start is None:
    scoped = list(entries)
else:
    scoped = [e for e in entries if e[0] is None or e[0] >= scope_start]

out = []


def emit(key, value):
    out.append("%s=%s" % (key, value))


emit("journal_entries_total", len(entries))
emit("journal_entries_without_timestamp", unknown_mono)
emit("journal_entries_in_scope", len(scoped))
emit("journal_scope_start_monotonic", "" if scope_start is None else scope_start)


def classify(items):
    counts = dict((name, 0) for name, _ in PREFIX_COUNTS)
    for _, text in items:
        for name, prefix in PREFIX_COUNTS:
            if not text.startswith(prefix):
                continue
            if name == "suppressed_messages" and SUPPRESSED_MARK not in text:
                continue
            counts[name] += 1
            break
    return counts


boot_counts = classify(entries)
scope_counts = classify(scoped)
for name, _ in PREFIX_COUNTS:
    emit("journal_count_boot_%s" % name, boot_counts[name])
    emit("journal_count_scope_%s" % name, scope_counts[name])


def find_invocation(items):
    """Index and text of the last version line seen in the item list."""
    idx = -1
    text = ""
    for i, (_, msg) in enumerate(items):
        m = RE_VERSION.match(msg)
        if m:
            idx = i
            text = msg
    return idx, text


def find_after(items, start, pattern):
    """First match of pattern at or after index start: (index, text, groups)."""
    for i in range(max(start, 0), len(items)):
        m = pattern.match(items[i][1])
        if m:
            return i, items[i][1], m
    return -1, "", None


idx, version_text = find_invocation(scoped)
source = "scope"
if idx < 0:
    idx, version_text = find_invocation(entries)
    source = "boot_fallback" if idx >= 0 else "none"

emit("journal_version_line_source", source)
emit("journal_scope_complete", 1 if source == "scope" else 0)

if version_text:
    emit("journal_version_line_text", version_text)
    m = RE_VERSION.match(version_text)
    emit("journal_version", m.group(1) if m else "")
else:
    emit("journal_version_line_text", "unavailable")
    emit("journal_version", "unavailable")

base = scoped if source == "scope" else entries
_, term_text, term_m = find_after(base, idx + 1, RE_TERM)
if term_text:
    emit("journal_threshold_term_line_text", term_text)
    emit("journal_threshold_term_mem_pct", term_m.group(1))
    emit("journal_threshold_term_swap_pct", term_m.group(2))
else:
    emit("journal_threshold_term_line_text", "unavailable")
    emit("journal_threshold_term_mem_pct", "unavailable")
    emit("journal_threshold_term_swap_pct", "unavailable")

_, kill_text, kill_m = find_after(base, idx + 1, RE_KILL)
if kill_text:
    emit("journal_threshold_kill_line_text", kill_text)
    emit("journal_threshold_kill_mem_pct", kill_m.group(1))
    emit("journal_threshold_kill_swap_pct", kill_m.group(2))
else:
    emit("journal_threshold_kill_line_text", "unavailable")
    emit("journal_threshold_kill_mem_pct", "unavailable")
    emit("journal_threshold_kill_swap_pct", "unavailable")

sys.stdout.write("\n".join(out) + "\n")
'

# The trailing marker line carries the exit status of both pipeline stages;
# it is separated from the derived data so that a stage failure is visible
# instead of being swallowed by the next stage.
journal_raw=$(journalctl -q -b -u earlyoom.service -o json --output-fields=MESSAGE 2>/dev/null \
    | python3 -c "${PYCODE}" "${scope_start}"
             printf '__capture_rc__ %s %s\n' "${PIPESTATUS[0]}" "${PIPESTATUS[1]}")

printf '%s\n' "${journal_raw}" | awk -v ts="$(date --iso-8601=seconds)" '
    /^__capture_rc__ / {
        printf "ts=%s earlyoom_journal_journalctl_rc=%s earlyoom_journal_reader_rc=%s\n", ts, $2, $3
        next
    }
    { printf "ts=%s %s\n", ts, $0 }
' >&3

# --- systemd-oomd notices, system journal, current boot --------------------

oomd_id=d989611b15e44c9dbf31e3c81256e4ed
oomd_out=$(journalctl -q -b "MESSAGE_ID=${oomd_id}" -o json --output-fields=MESSAGE_ID 2>/dev/null); rc=$?
oomd_count=$(printf '%s' "${oomd_out}" | awk 'END { print NR }')
rec "oomd_notice_message_id=${oomd_id} oomd_notice_count=${oomd_count} oomd_notice_rc=${rc}"

rec "capture_finished=$(date --iso-8601=seconds)"

exec 3>&-
exit 0
