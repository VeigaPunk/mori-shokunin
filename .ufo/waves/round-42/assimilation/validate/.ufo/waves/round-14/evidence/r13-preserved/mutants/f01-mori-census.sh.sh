#!/usr/bin/env bash
# mori-census.sh — read-only fleet/host observability census (mori-shokunin r3).
#
# Domain: whether the fleet, its waves and its host are alive and progressing.
# Product: verdict + surface lines + stable finding ids. Never remediates.
#
# Verdict: MORI_CENSUS: CLEAN|DRIFT
# Exit:    0 CLEAN | 1 DRIFT | 2 setup/usage
#
# Surfaces:
#   watchdog  pid + .ufo/watchdog.log freshness + .ufo/state/*.round values
#             (count, max, ledger-vs-state mismatch — r7; r8 adds every
#             non-regular `*.round` entry, by reason)
#   waves     .ufo/waves/* settlement (registry/dispatch/run × results/closeout)
#   journal   structured per-scope notice/record counts (this boot): catalog
#             MESSAGE_ID classes + COREDUMP_SIGNAL=11, no MESSAGE, user and
#             system separate; r14 restores the OOM crit alarm (kernel-OOM unit
#             notice in either scope, or UNIT_RESULT=oom-kill) and splits unit
#             failures into fleet / non-fleet (owner tsukuroi) / unknown from
#             the subject UNIT/USER_UNIT metadata
#   cgroup    memory.events / memory.current / memory.pressure / memory.max /
#             memory.peak (user slice; r7 adds PSI + fill/avail grading, r8 the
#             scope high-watermark with its instance anchor; thresholds labeled
#             local)
#   disk      df runway on fleet root + /tmp + optional scratch; r7 adds a
#             since-boot write average per target device (/proc/diskstats)
#   silence   per-lane launch/closure/authorship grading (PROTOCOL.md:153-168;
#             contract corpus/knowledge/silence-grading-r2.md) — states silent |
#             progressing | progressing-weak | young | not-open | unavailable
#   tmux      optional session list; r7 classifies every session fleet-relevant
#             vs foreign by pane current path under the fleet root; r8 adds a
#             timeout-bounded per-session freshness probe for the relevant ones
#             (absence = unavailable, not DRIFT)
#
# ROUND-7 GAP CLOSURE — sources are the "Gaps" sections of
# corpus/knowledge/observability-surfaces-r2.md, one entry per gap:
#   1 tmux relevance   IMPLEMENTED: probe_tmux reads `tmux list-panes -a` pane
#                      data and classifies each session by pane current path
#                      under $ROOT (fleet root; the class is a rule, not a
#                      guess). Rule boundary disclosed on the row: a session
#                      whose panes all sit outside the fleet root is foreign
#                      even if its process tree works on fleet files.
#   2 memory pressure  IMPLEMENTED: memory.pressure PSI `some`/`full` avg10 is
#                      read and the `some` average is graded against
#                      MORI_MEM_PSI_WARN_AVG10 (labeled local); fill pressure is
#                      current/max when the cgroup has a numeric max, else the
#                      host MemAvailable/MemTotal floor at MORI_MEM_AVAIL_MIN_PCT
#                      with the scope named on the row (`fill_scope=`). Both
#                      numbers are LOCAL placeholders for this host, not
#                      measured for it and never tuned as universal.
#   3 disk write-rate  IMPLEMENTED as an AVERAGE SINCE BOOT: sectors_written*512
#                      /uptime per target's device from MORI_DISKSTATS, no
#                      sampling interval added to census runtime. The row carries
#                      it as `io_avg_since_boot=<dev>:<rate>Bps/<uptime>s` with
#                      the divisor folded in, and every target it could not
#                      measure appears in `io_avg_unavailable=<dev>:<reason>`
#                      (never as 0 B/s). BOUNDED
#                      DEFERRAL (r7): the INSTANTANEOUS write rate (two-sample
#                      delta) is NOT implemented; r7 named the precondition to
#                      lift it — measure the wall-time a second sample adds.
#                      The ROUND-8 block below satisfies that precondition with
#                      a measured number (median +213 ms for the 0.2 s variant,
#                      minimum +210 ms vs a 50 ms budget), so the deferral now
#                      stands on measurement, not on an estimate. This average
#                      is the "measured write rate" the r2 note required before
#                      touching 85/95.
#   4 state_rounds     IMPLEMENTED: `.ufo/state/*.round` VALUES are read; the
#                      maximum is reported and every value is compared with the
#                      last `launch <lane> round=N` ledger line for that lane
#                      (the watchdog's own state: it writes the state file and
#                      then the launch line in the same tick,
#                      scripts/shokunin-watchdog.sh:80-81). A value below the
#                      ledger round is WATCHDOG_STATE_LAG, above it is
#                      WATCHDOG_STATE_AHEAD; both are INFO (a state file can be
#                      inconsistent without the fleet being unhealthy, so
#                      neither may flip the roll — the gap being closed is
#                      invisibility, not severity).
# All r7 threshold defaults are LOCAL to this fleet host and are labeled local
# on every row and finding; none is a scalar score and none is universal.
#
# ROUND-8 GAP CLOSURE — the four residuals named in
# corpus/knowledge/surfaces-r7.md (`Honest residuals`), one entry per residual,
# each closed with a measured probe + selftest cases or an explicit deferral
# that now carries its measured numbers:
#   1 instantaneous disk write-rate — DEFERRED, cost now MEASURED (r7 deferred
#     it with no number). Method: the r7 bytes plus a two-sample block (one
#     extra read of MORI_DISKSTATS before and after a bounded dwell) run 30x per
#     arm in isolation (/tmp/r8m/micro-disk.log) and 5x per arm through the whole
#     gate, interleaved (/tmp/r8m/disk-cost.log), host load ~68:
#       isolated, ms: floor (two date calls) min 0 median 3 max 7;
#         two extra diskstats reads, no dwell: min 5 median 16 p90 27 max 32;
#         pure `sleep 0.2`: min 202 median 206 max 215;
#         reads + 0.2 s dwell: min 210 median 229 p90 240 max 265;
#         reads + 1.0 s dwell: min 1011 median 1025 max 1051.
#     The 0.2 s variant adds ~213 ms median over the two-read floor, and its
#     MINIMUM (210 ms) is 4.2x the 50 ms budget — it fails this round's
#     condition, so the instantaneous rate stays unimplemented and the numbers
#     above replace r7's precondition (the dwell is the entire cost; the extra
#     reads alone are 16 ms median, 27 ms p90). Gate-level wall time could not
#     resolve a 200 ms effect under today's load (medians of 5 interleaved runs:
#     r7 base 13583 / +reads 12551 / +0.2 s 16272 / +1.0 s 17438 ms, spread
#     >10 s) and is reported as unusable, not as the decision.
#   2 tmux per-session freshness — IMPLEMENTED: for every session classified
#     fleet-relevant, ONE `tmux display-message -p -t <session>
#     '#{session_activity}'` under run_timeout (bound MORI_TMUX_TIMEOUT_S,
#     default 2 s; rc 124 = bound fired). idle = NOW_EPOCH - session_activity is
#     graded against MORI_TMUX_IDLE_WARN_S (default 3600, LABELED LOCAL) as the
#     INFO finding TMUX_SESSION_IDLE — a quiet pane is evidence, not proof, so
#     the local number may not flip the roll. Unavailable semantics throughout:
#     rc from the bound, non-integer probe output and a missing `timeout` binary
#     each set freshness=unavailable with its reason; the last one refuses to run
#     the probe at all, because an unbounded client call to a wedged server is
#     the one read in this gate that can block forever. Only relevant sessions
#     are probed: a foreign session's quiet is not fleet evidence.
#   3 `*.round` symlink/dir invisibility — IMPLEMENTED: the state walk no longer
#     filters on `-type f`. Every `*.round` ENTRY is classified before any read
#     (symlink | directory | other non-regular | regular) and a non-regular entry
#     is counted as an unreadable value WITH its reason
#     (WATCHDOG_STATE_ENTRY_UNREADABLE) and split out on the row as
#     `state_val_unread_reasons=file:N symlink:N dir:N other:N`. Symlinks are
#     never followed: a link's target is arbitrary bytes, and following it would
#     let a foreign file's integer into the rows. `state_rounds` keeps its r7
#     meaning (regular entries) so existing state dirs read exactly as before.
#   4 memory-probe residuals — the r7 note §2 named three; each now carries a
#     measurement taken read-only 2026-10-15T20:09-20:12Z (21 PSI/avail samples,
#     3 s apart, /tmp/r8m/mem-samples.log; cgroup walk /tmp/r8m/cgroup-max-census.sh):
#       threshold placement: psi_some_avg10 observed 0.00-0.39 (full 0.00-0.39)
#         against MEM_PSI_WARN_AVG10=10, and host MemAvailable/MemTotal 49-53%
#         against MEM_AVAIL_MIN_PCT=10 — the two placeholders sit 25x and 4.9x
#         away from everything this host produced in the window. They stay
#         labeled local: a distribution is not a calibration.
#       scope observability: the walk found 108 memory.max files — 107 the
#         literal `max`, exactly 1 numeric (system.slice/polkit.service =
#         33554432 B), 0 unreadable — so the closed-container fill ratio is
#         constructible in 1 of 108 scopes on this host and not in the fleet's
#         user slice. memory.peak is the live scope-local substitute and IS
#         readable here (slice 28812898304, service 28801970176, both with
#         max=max), so the row now carries mem_peak + mem_peak_source +
#         mem_peak_anchor (the scope dir mtime: a cumulative high-watermark is
#         comparable only within its cgroup instance).
#       live vs fixture-only evidence: the same window is this host's own
#         pressure record while a 32-seat wave ran (host mem avail 49-53%, PSI
#         some avg10 <= 0.39, slice peak constant 28812898304). The fixture arms
#         still prove arithmetic and direction; they no longer stand alone.
# r8 thresholds: MORI_TMUX_IDLE_WARN_S and MORI_TMUX_TIMEOUT_S are local to this
# host (the timeout is a latency bound, the idle number a labeled-local
# placeholder), and the INFO severity of TMUX_SESSION_IDLE is what keeps a local
# placeholder from producing a false DRIFT.
#
# ROUND-10 DRIFT PIN — a behavioral baseline for the census's own output
# (the freshness item carried since round 2; SCORECARD r9: "a committed
# behavioral baseline plus a --drift mode with a declared volatile-fields
# list, so census behavioral drift is itself detected").
#   --pin <path>    run the census (live, read-only), normalize its FULL
#                   output, and write it to <path>. The file header records
#                   the census bytes' sha256, the pin clock, and the DECLARED
#                   VOLATILE FIELD LIST (values that legitimately change
#                   run-to-run; masked to <V> in the canonical block):
#                     timestamps/ages  ts age_s mtime_age_s *_epoch
#                                      mem_peak_anchor
#                     gauges/decimals  psi_some_avg10 psi_full_avg10
#                     rates            io_avg_since_boot (the "N Bps/up s"
#                                      pair; device names are kept)
#                     counters         the DRIFT_COUNTER_KEYS list in the code
#                                      block below (pids, state_rounds*, wave
#                                      counts, journal counts, cgroup gauges,
#                                      lane/tmux counts, verdict tallies,
#                                      DISK finding sizes, row-B files, ...)
#                     compounds        state_val_unread_reasons
#                     stamps           script_sha256 (behavior, not revision,
#                                      is compared), example (row-B path)
#                   Write failure = exit 2. The census's own CLEAN/DRIFT roll
#                   is recorded in the canonical block but never decides the
#                   pin's exit code: pinning a DRIFT host is still a pin.
#   --drift <path>  run the census, normalize with the CURRENT script's
#                   volatile list, and diff against the baseline:
#                     equal  -> 'MORI_DRIFT: none' (exit 0)
#                     differ -> 'MORI_DRIFT: <changed non-volatile field
#                               names>' (exit 1): a changed value names its
#                               key; a removed/added field names -key/+key;
#                               a removed/added line names -<id>/+<id>
#                               (e.g. -FINDING WATCHDOG_ABSENT); a line
#                               differing only outside key=value tokens names
#                               its id (e.g. VERDICT, SURFACE watchdog); a
#                               pure reorder names output-order.
#                     baseline missing/unreadable/malformed -> exit 2.
#                   The check is behavioral, not revision-bound: two different
#                   census SHAs with the same normalized output are 'none'
#                   (comment-only edits), while a change to the volatile list
#                   itself surfaces as drift on every affected field.
# Live mode writes nothing. --selftest writes only under
# /tmp/mori-census-selftest.XXXXXX and asserts the fixture tree is unchanged.
# --pin writes exactly the named baseline file; --drift writes nothing.
#
# Env overrides (selftest / operator pin); empty = live host defaults:
#   MORI_SHOKUNIN_ROOT   fleet root (default: parent of tools/../ or cwd probe)
#   MORI_UFO_DIR         default $ROOT/.ufo
#   MORI_WATCHDOG_LOG    default $UFO/watchdog.log
#   MORI_TIMELINE_FILE   launch/close ledger for lane silence; default $WATCHDOG_LOG
#   MORI_STATE_DIR       default $UFO/state
#   MORI_WAVES_DIR       default $UFO/waves
#   MORI_CGROUP_EVENTS   default user-slice memory.events path
#   MORI_CGROUP_CURRENT  default user-slice memory.current path
#   MORI_CGROUP_PRESSURE default <events dir>/memory.pressure (PSI; r7)
#   MORI_CGROUP_MAX      default <events dir>/memory.max (fill limit; r7)
#   MORI_CGROUP_PEAK     default <events dir>/memory.peak (high-watermark; r8)
#   MORI_DISKSTATS       default /proc/diskstats (write-rate counters; r7)
#   MORI_UPTIME          default /proc/uptime (since-boot divisor; r7)
#   MORI_MEMINFO         default /proc/meminfo
#   MORI_DF_BIN          default df
#   MORI_PGREP_BIN       default pgrep
#   MORI_JOURNALCTL_BIN  default journalctl
#   MORI_JQ_BIN          default jq (safe JSON parser for journal records; r13)
#   MORI_TMUX_BIN        default tmux
#   MORI_TIMEOUT_BIN     default timeout (bounds the r8 tmux freshness probe)
#   MORI_GIT_BIN         default git
#   MORI_DISK_TARGETS    space-separated paths for df (default: ROOT /tmp)
#   MORI_WATCHDOG_STALE_S MORI_WAVE_UNSETTLED_S MORI_DISK_WARN_PCT
#   MORI_DISK_CRIT_PCT    MORI_LANE_SILENCE_S
#   MORI_MEM_PSI_WARN_AVG10 MORI_MEM_FILL_WARN_PCT MORI_MEM_AVAIL_MIN_PCT
#                        labeled-local memory thresholds (round-7 block above)
#   MORI_TMUX_SCOPE_ROOT fleet root for session classification (default $ROOT)
#   MORI_TMUX_IDLE_WARN_S labeled-local session idle threshold (r8, default 3600)
#   MORI_TMUX_TIMEOUT_S  per-call bound for the r8 freshness probe (default 2)
#   MORI_JOURNAL_TIMEOUT_S per-journalctl-query bound (r13, local default 2; rc 124/137
#                        grades the class unavailable, never a partial count)
#   MORI_BOOT_ID         expected current boot id (32 lowercase hex, dashless);
#                        default read from /proc/sys/kernel/random/boot_id (r13)
#   MORI_BOOT_ID_FILE    default /proc/sys/kernel/random/boot_id (r13)
#   MORI_FLEET_CONF      parsed (never sourced) lane declarations; default $ROOT/shokunin.conf
#   MORI_NOW_EPOCH       pin "now" (selftest)
#   MORI_FIXTURE         selftest marker (optional)
#
# Finding ids (stable compare contract):
#   WATCHDOG_ABSENT WATCHDOG_STALE WATCHDOG_LOG_UNAVAILABLE
#   WATCHDOG_PROBE_UNAVAILABLE WATCHDOG_STATE_LAG WATCHDOG_STATE_AHEAD
#   WATCHDOG_STATE_ENTRY_UNREADABLE
#   WAVE_UNSETTLED_AGE
#   OOM_KILL_JOURNAL
#   OOMD_NOTICE_JOURNAL_{USER,SYSTEM}
#   COREDUMP_NOTICE_JOURNAL_{USER,SYSTEM}
#   SEGFAULT_SIGNAL11_JOURNAL_{USER,SYSTEM}
#   KILL_SIGNAL_JOURNAL KILL_SIGNAL_JOURNAL_SYSTEM
#   UNIT_FAILURE_JOURNAL UNIT_FAILURE_JOURNAL_SYSTEM
#   UNIT_FAILURE_OUT_OF_SCOPE UNIT_FAILURE_OUT_OF_SCOPE_SYSTEM
#   UNIT_FAILURE_UNATTRIBUTED_JOURNAL
#   JOURNAL_CLASSES_UNMEASURED
#   CGROUP_OOM_KILL CGROUP_UNAVAILABLE MEM_PRESSURE_HIGH MEM_FILL_HIGH
#   MEM_AVAIL_LOW
#   DISK_LOW DISK_CRITICAL DISK_UNAVAILABLE DISK_IO_UNMEASURED
#   ROSTER_SET_MISMATCH
#   TMUX_FOREIGN_SESSION TMUX_RELEVANCE_UNAVAILABLE TMUX_SESSION_IDLE
#   TMUX_FRESHNESS_UNAVAILABLE
#
set -euo pipefail
# The journal is held in a shell variable (CAP_OUT) and even a hostile stub could
# return MESSAGE text the probe never asked for. Never trace: `bash -x` would
# print that variable. Only validated counts and _BOOT_ID values reach stdout.
set +o xtrace

VERSION=census-r6
SELF=$(readlink -f -- "${BASH_SOURCE[0]}" 2>/dev/null || {
  p=$0
  case "$p" in /*) printf '%s' "$p" ;; *) printf '%s' "$PWD/$p" ;; esac
})
SCRIPT_DIR=$(cd -- "$(dirname -- "$SELF")" && pwd)
# tools/ -> lane root -> prefer lane's parent (shokunin root) when layout matches
LANE_ROOT=$(cd -- "$SCRIPT_DIR/.." && pwd)
DEFAULT_ROOT=$LANE_ROOT
case "$(basename -- "$LANE_ROOT")" in
  *-shokunin) DEFAULT_ROOT=$(cd -- "$LANE_ROOT/.." && pwd) ;;
esac

# ---- defaults (overridable) -------------------------------------------------
ROOT=${MORI_SHOKUNIN_ROOT:-$DEFAULT_ROOT}
UFO=${MORI_UFO_DIR:-$ROOT/.ufo}
WATCHDOG_LOG=${MORI_WATCHDOG_LOG:-$UFO/watchdog.log}
# The launch/close ledger is the watchdog log on this fleet; the override exists
# so a scenario driver can point the probe at the same bytes it writes
# (tools/mori-silence-cases.sh exports MORI_TIMELINE_FILE).
TIMELINE_FILE=${MORI_TIMELINE_FILE:-$WATCHDOG_LOG}
STATE_DIR=${MORI_STATE_DIR:-$UFO/state}
WAVES_DIR=${MORI_WAVES_DIR:-$UFO/waves}
CGROUP_EVENTS=${MORI_CGROUP_EVENTS:-/sys/fs/cgroup/user.slice/user-$(id -u).slice/memory.events}
CGROUP_CURRENT=${MORI_CGROUP_CURRENT:-/sys/fs/cgroup/user.slice/user-$(id -u).slice/memory.current}
# r7: pressure and limit siblings of the events file, so an operator who pins
# MORI_CGROUP_EVENTS pins the whole scope (the selftest does exactly that).
CGROUP_PRESSURE=${MORI_CGROUP_PRESSURE:-${CGROUP_EVENTS%.events}.pressure}
CGROUP_MAX=${MORI_CGROUP_MAX:-${CGROUP_EVENTS%.events}.max}
CGROUP_PEAK=${MORI_CGROUP_PEAK:-${CGROUP_EVENTS%.events}.peak}
DISKSTATS=${MORI_DISKSTATS:-/proc/diskstats}
UPTIME_FILE=${MORI_UPTIME:-/proc/uptime}
MEMINFO=${MORI_MEMINFO:-/proc/meminfo}
DF_BIN=${MORI_DF_BIN:-df}
PGREP_BIN=${MORI_PGREP_BIN:-pgrep}
JOURNALCTL_BIN=${MORI_JOURNALCTL_BIN:-journalctl}
JQ_BIN=${MORI_JQ_BIN:-jq}
TMUX_BIN=${MORI_TMUX_BIN:-tmux}
TIMEOUT_BIN=${MORI_TIMEOUT_BIN:-timeout}
GIT_BIN=${MORI_GIT_BIN:-git}
DISK_TARGETS=${MORI_DISK_TARGETS:-"$ROOT /tmp"}
TMUX_SCOPE_ROOT=${MORI_TMUX_SCOPE_ROOT:-$ROOT}
# r8 per-session freshness. TMUX_TIMEOUT_S bounds ONE tmux client call (a
# `tmux display-message` against a wedged server can block a client forever, and
# this gate must never hang); rc 124 from the bound is graded unavailable, never
# a verdict. TMUX_IDLE_WARN_S is a LOCAL placeholder for this host, like the
# memory block above: it exists so session idleness stops being unmeasured, it
# carries `threshold_label=local` on the finding, and it fires INFO only — a
# quiet pane is evidence a reader must see, not proof the fleet is unhealthy.
TMUX_TIMEOUT_S=${MORI_TMUX_TIMEOUT_S:-2}
# r13: a field-filtered journalctl read scans the boot's journal; one wedged or
# enormous store must not hang the census. Every structured query is bounded and
# rc 124/137 grades the class unavailable, never a partial count. 2 s is a LOCAL
# placeholder for this host's store (the same bound the r8 tmux probe uses), not
# a measured cost of a journal scan.
JOURNAL_TIMEOUT_S=${MORI_JOURNAL_TIMEOUT_S:-2}
# r13 boot anchor: journal _BOOT_ID is 32 lowercase hex without dashes; the proc
# file is a dashed UUID. Every counted record must carry this exact id, so a
# stale, mixed or wrongly scoped stream is unavailable rather than counted. An
# invalid/absent anchor disables counting (never a fake 0).
BOOT_ID_FILE=${MORI_BOOT_ID_FILE:-/proc/sys/kernel/random/boot_id}
BOOT_ID_EXPECTED=${MORI_BOOT_ID:-}
if [ -z "$BOOT_ID_EXPECTED" ] && [ -r "$BOOT_ID_FILE" ]; then
  BOOT_ID_EXPECTED=$(tr -d -- '-\n' < "$BOOT_ID_FILE" 2>/dev/null || true)
fi
case "$BOOT_ID_EXPECTED" in
  *[!0-9a-f]*) BOOT_ID_EXPECTED='' ;;
esac
if [ "${#BOOT_ID_EXPECTED}" -ne 32 ]; then BOOT_ID_EXPECTED=''; fi
TMUX_IDLE_WARN_S=${MORI_TMUX_IDLE_WARN_S:-3600}
WATCHDOG_STALE_S=${MORI_WATCHDOG_STALE_S:-900}
WAVE_UNSETTLED_S=${MORI_WAVE_UNSETTLED_S:-7200}
# PROPOSAL, NOT MEASURED. No write-rate evidence exists for either number: the
# fleet's own reported disk failures are quota events (EDQUOT), which a capacity-%
# probe cannot see. 85/95 is the single R1 proposal pair; do not install a
# "better" percent without a measured write rate, and do not OR a byte floor
# against df -P's 1024-block Available column (a unit trap that false-fires today).
DISK_WARN_PCT=${MORI_DISK_WARN_PCT:-85}
DISK_CRIT_PCT=${MORI_DISK_CRIT_PCT:-95}
LANE_SILENCE_S=${MORI_LANE_SILENCE_S:-7200}
# r7 memory thresholds. LOCAL PLACEHOLDERS for this host, deliberately not
# derived from a measurement of it: the r2 note's rule is that a number is
# either measured or labeled, and there is no measured memory-pressure
# distribution yet. They exist so the four r2 gaps stop being unmeasured, and
# they must be recalibrated here (not carried as universal) by any operator who
# reuses this gate elsewhere.
MEM_PSI_WARN_AVG10=${MORI_MEM_PSI_WARN_AVG10:-10}
MEM_FILL_WARN_PCT=${MORI_MEM_FILL_WARN_PCT:-85}
MEM_AVAIL_MIN_PCT=${MORI_MEM_AVAIL_MIN_PCT:-10}
FLEET_CONF=${MORI_FLEET_CONF:-$ROOT/shokunin.conf}
ROSTER_LANES=${MORI_ROSTER_LANES:-}
ROSTER_SOURCE=
ROSTER_N=0
CONF_N=0
STATE_N=0
CONF_DROPPED_N=0
STATE_DROPPED_N=0

SCRIPT_SHA256=$(sha256sum "$SELF" 2>/dev/null | cut -d' ' -f1)
[ -n "$SCRIPT_SHA256" ] || SCRIPT_SHA256=unavailable

NOW_EPOCH=${MORI_NOW_EPOCH:-}
if [ -z "$NOW_EPOCH" ]; then NOW_EPOCH=$(date +%s); fi
TS_UTC=$(date -u -d "@$NOW_EPOCH" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -r "$NOW_EPOCH" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u +%Y-%m-%dT%H:%M:%SZ)

# ---- counters / findings ----------------------------------------------------
N_FINDINGS=0
N_DRIFT=0
N_UNAVAIL=0
N_SURFACES=0
ROLL=CLEAN
declare -a FINDING_LINES=()
declare -a SURFACE_LINES=()

usage() {
  cat <<'EOF'
usage: mori-census.sh [--selftest] [--pin <path>] [--drift <path>] [--help]

  (no flags)   live read-only census over fleet/host observability surfaces
  --pin <path>     run the census and write a normalized behavioral baseline
                   to <path>: full output with the declared volatile fields
                   masked to <V>; the volatile list is recorded in the header
  --drift <path>   run the census, normalize, and diff against the baseline:
                   'MORI_DRIFT: none' (exit 0) or the changed non-volatile
                   fields (exit 1); missing/unreadable/malformed baseline 2
  --selftest   hermetic fixture-tree proof (writes only under
               /tmp/mori-census-selftest.*); exit 0 pass, 1 fail
  --help       this text

Verdict: MORI_CENSUS: CLEAN|DRIFT (findings=N drift=M unavailable=U surfaces=S)
Exit:    0 CLEAN | 1 DRIFT | 2 setup/usage (also --pin/--drift contract exits)
Read-only: live mode creates no files; never remediates.
EOF
}

die_usage() { printf 'mori-census: %s\n' "$1" >&2; usage >&2; exit 2; }

# severity: info does not flip ROLL; warn|crit flips to DRIFT
emit_finding() { # id severity observation
  local id=$1 sev=$2 obs=$3
  N_FINDINGS=$((N_FINDINGS + 1))
  # A finding must be a REUSABLE observation: stamp the clock and the script
  # revision so a later reader can re-run the same probe against the same code.
  FINDING_LINES+=("FINDING $id severity=$sev obs=$obs ts=$TS_UTC script_sha256=$SCRIPT_SHA256")
  case "$sev" in
    warn|crit)
      N_DRIFT=$((N_DRIFT + 1))
      ROLL=DRIFT
      ;;
  esac
}

emit_surface() { # name state detail
  local name=$1 state=$2 detail=$3
  N_SURFACES=$((N_SURFACES + 1))
  SURFACE_LINES+=("SURFACE $name: $state ($detail)")
  if [ "$state" = unavailable ]; then
    N_UNAVAIL=$((N_UNAVAIL + 1))
  fi
}

# Resolve the silence roster from an explicit override or parsed fleet inputs.
# Config is data, never shell code; state symlinks are never followed.
resolve_roster() {
  local line id sf conf_available=0 state_available=0 conf_csv state_csv in_lanes=0
  local -a conf_ids=() state_ids=() state_sorted=() roster_ids=() conf_only=() state_only=()
  local -A conf_seen=() state_seen=()

  ROSTER_N=0
  CONF_N=0
  STATE_N=0
  CONF_DROPPED_N=0
  STATE_DROPPED_N=0

  if [ -n "${MORI_ROSTER_LANES:-}" ]; then
    ROSTER_LANES=$MORI_ROSTER_LANES
    ROSTER_SOURCE=env
    for id in $ROSTER_LANES; do ROSTER_N=$((ROSTER_N + 1)); done
    return 0
  fi

  if [ -f "$FLEET_CONF" ] && [ -r "$FLEET_CONF" ]; then
    conf_available=1
    # Only rows inside a LANES="…" assignment are lane declarations (the conf
    # appends blocks as LANES="$LANES …"); rows of any other variable are never
    # read as lanes. The assignment ends at the next double quote.
    while IFS= read -r line || [ -n "$line" ]; do
      if [ "$in_lanes" -eq 0 ]; then
        [[ $line =~ ^[[:space:]]*LANES=\" ]] || continue
        in_lanes=1
        line=${line#*\"}
      fi
      if [[ $line =~ ^([a-z0-9][a-z0-9-]*)\| ]]; then
        id=${BASH_REMATCH[1]}
        if [[ ! $id =~ ^[a-z0-9][a-z0-9-]{0,47}$ ]]; then
          CONF_DROPPED_N=$((CONF_DROPPED_N + 1))
        elif [[ ! ${conf_seen[$id]+seen} ]]; then
          conf_seen[$id]=1
          conf_ids+=("$id")
        fi
      fi
      [[ $line == *'"'* ]] && in_lanes=0
    done < "$FLEET_CONF"
  fi

  if [ -d "$STATE_DIR" ] && [ -r "$STATE_DIR" ]; then
    state_available=1
    for sf in "$STATE_DIR"/*.round; do
      [ -L "$sf" ] && continue
      [ -f "$sf" ] || continue
      id=${sf##*/}
      id=${id%.round}
      if [[ ! $id =~ ^[a-z0-9][a-z0-9-]{0,47}$ ]]; then
        STATE_DROPPED_N=$((STATE_DROPPED_N + 1))
        continue
      fi
      if [[ ! ${state_seen[$id]+seen} ]]; then
        state_seen[$id]=1
        state_ids+=("$id")
      fi
    done
  fi

  CONF_N=${#conf_ids[@]}
  STATE_N=${#state_ids[@]}
  if [ "${#state_ids[@]}" -gt 0 ]; then
    mapfile -t state_sorted < <(printf '%s\n' "${state_ids[@]}" | LC_ALL=C sort)
  fi

  roster_ids=("${conf_ids[@]}")
  for id in "${state_sorted[@]}"; do
    [[ ${conf_seen[$id]+seen} ]] || roster_ids+=("$id")
  done

  if [ "${#roster_ids[@]}" -gt 0 ]; then
    if [ "$CONF_N" -gt 0 ] && [ "$STATE_N" -gt 0 ]; then
      ROSTER_SOURCE=conf+state
    elif [ "$CONF_N" -gt 0 ]; then
      ROSTER_SOURCE=conf
    else
      ROSTER_SOURCE=state
    fi
  else
    # A missing/unreadable input is not a failure; retain the historical
    # fallback only when neither source yielded any valid lane id.
    ROSTER_SOURCE=builtin
    roster_ids=(protocol aggregator kasegi kengaku kake kumitate kotoba kagi kama)
  fi

  ROSTER_LANES=${roster_ids[*]}
  ROSTER_N=${#roster_ids[@]}

  # An unavailable source is not an empty source and cannot prove a mismatch.
  if [ "$conf_available" -eq 1 ] && [ "$state_available" -eq 1 ]; then
    for id in "${conf_ids[@]}"; do
      [[ ${state_seen[$id]+seen} ]] || conf_only+=("$id")
    done
    for id in "${state_sorted[@]}"; do
      [[ ${conf_seen[$id]+seen} ]] || state_only+=("$id")
    done
    if [ "${#conf_only[@]}" -gt 0 ] || [ "${#state_only[@]}" -gt 0 ]; then
      conf_csv=none
      state_csv=none
      if [ "${#conf_only[@]}" -gt 0 ]; then
        conf_csv=$(printf '%s,' "${conf_only[@]}")
        conf_csv=${conf_csv%,}
      fi
      if [ "${#state_only[@]}" -gt 0 ]; then
        state_csv=$(printf '%s,' "${state_only[@]}")
        state_csv=${state_csv%,}
      fi
      emit_finding ROSTER_SET_MISMATCH info "conf_only=$conf_csv state_only=$state_csv"
    fi
  fi
}



have() { command -v "$1" >/dev/null 2>&1; }

cap() { # run read-only; capture stdout+stderr + rc without set -e trip
  set +e
  CAP_OUT=$("$@" 2>&1)
  CAP_RC=$?
  set -e
}

# run_timeout <secs> <cmd...> — cap() under a wall-clock bound. rc 124 means the
# bound fired. r8: the only caller is the per-session tmux freshness probe, whose
# client call is the one read in this gate that can block indefinitely (a
# wedged tmux server answers nobody). A caller that cannot bound the call
# reports `unavailable reason=no-timeout-bin` instead of running it unbounded —
# "never hang" beats "maybe measure".
run_timeout() {
  local secs=$1
  shift
  set +e
  CAP_OUT=$("$TIMEOUT_BIN" -k 1 "$secs" "$@" 2>&1)
  CAP_RC=$?
  set -e
}

read_file() { # first line or empty
  local f=$1
  [ -r "$f" ] || return 0
  head -n1 -- "$f" 2>/dev/null | tr -d '\r' || true
}

cgroup_field() { # file key -> value
  local f=$1 k=$2
  [ -r "$f" ] || return 0
  awk -v key="$k" '$1 == key { print $2; exit }' "$f" 2>/dev/null || true
}

# num_of — SHAPE-VALIDATED numeric first line of a file, empty otherwise.
# r7 readers of operator-pinnable paths (memory.max, memory.pressure,
# memory.current's numeric arm) print only what this returns: a value that is
# not a plain non-negative integer is dropped, so no arbitrary file's bytes can
# reach a row through these fields. That is the same print-safety rule the
# CGROUP_CURRENT prefix check enforces differently for the echoed line.
num_of() {
  local f=$1 v
  v=$(read_file "$f")
  v=${v//[[:space:]]/}
  is_int "$v" || return 0
  printf '%s' "$v"
}

# is_decimal — digits with at most one dot (PSI avg10 shape). Anything else is
# refused by the caller rather than echoed, keeping operator-pinned paths from
# printing foreign bytes.
is_decimal() {
  case "${1:-}" in ''|*[!0-9.]*) return 1 ;; esac
  case "${1//[0-9]/}" in ''|.) return 0 ;; *) return 1 ;; esac
}

# meminfo_field <Key> -> kB integer or empty (shape-validated, never raw echo)
meminfo_field() {
  local k=$1 v
  v=$(awk -v key="$k:" '$1 == key { print $2; exit }' "$MEMINFO" 2>/dev/null || true)
  is_int "$v" || return 0
  printf '%s' "$v"
}

# psi_avg10 <psiy-text> <some|full> -> avg10 token or empty; awk only (no
# pipeline into a consumer), so an empty or short PSI file cannot trip pipefail.
psi_avg10() {
  printf '%s\n' "$1" | awk -v kind="$2" '$1 == kind { for (i = 2; i <= NF; i++) if ($i ~ /^avg10=/) { sub(/^avg10=/, "", $i); print $i; exit } }' || true
}

# load_ledger — rc-gated read of the launch/close ledger into LEDGER.
# `cat` on an unreadable file must never abort the gate (the pipefail lesson:
# corpus/lessons/2026-10-15-errexit-pipefail-silent-crash.md). LEDGER_RC is the
# read's rc so a caller can disclose an unprovable comparison instead of
# reporting a fabricated 0; an unreadable ledger is not evidence of agreement.
load_ledger() {
  LEDGER=''; LEDGER_RC=1
  [ -r "$TIMELINE_FILE" ] || return 0
  cap cat -- "$TIMELINE_FILE"
  LEDGER_RC=$CAP_RC
  LEDGER=$CAP_OUT
}

# ledger_last_launch_round <lane> -> last `launch <lane> round=<N>` round in
# file order (empty when the lane has no launch line). Same candidate-line
# filter and last-wins rule as ledger_anchor, deliberately: two independent
# readings of one grammar that disagree would be a bug in one of them.
ledger_last_launch_round() {
  local lane=$1 line f1 f2 f3 f4 f5 f6 rest round
  local out=''
  while IFS= read -r line; do
    line=${line%$'\r'}
    case "$line" in
      [0-9]*T*) ;;
      *' ts='[0-9]*) ;;
      *) continue ;;
    esac
    read -r f1 f2 f3 f4 f5 f6 rest <<< "$line" || true
    [ "$f2" = launch ] || continue
    [ "$f3" = "$lane" ] || continue
    case "$f4" in round=*) ;; *) continue ;; esac
    round=${f4#round=}; round=${round%%;*}
    is_int "$round" || continue
    out=$round
  done <<< "${LEDGER:-}"
  printf '%s' "$out"
}

epoch_mtime() {
  local f=$1
  stat -c %Y -- "$f" 2>/dev/null || stat -f %m -- "$f" 2>/dev/null || printf ''
}

# ---- surface: watchdog ------------------------------------------------------
probe_watchdog() {
  local detail pids pid_n log_state age= stale=0 cmd_bits=''
  cmd_bits="pgrep -af shokunin-watchdog; stat $WATCHDOG_LOG; ls $STATE_DIR"

  pid_n=0
  pids=''
  if have "$PGREP_BIN" || [ -x "$PGREP_BIN" ]; then
    cap "$PGREP_BIN" -af shokunin-watchdog
    # Filter the pgrep line itself and empty
    pids=$(printf '%s\n' "$CAP_OUT" | grep -E 'shokunin-watchdog' | grep -vF 'pgrep' || true)
    if [ -n "$pids" ]; then
      pid_n=$(printf '%s\n' "$pids" | grep -c . || true)
    fi
  else
    emit_surface watchdog unavailable "cmd=$cmd_bits; pgrep=missing; ts=$TS_UTC"
    emit_finding WATCHDOG_PROBE_UNAVAILABLE info "pgrep unavailable — daemon liveness UNKNOWN, not absent"
    return 0
    emit_finding WATCHDOG_LOG_UNAVAILABLE info "pgrep binary missing — cannot assess pid"
    # still try log
  fi

  if [ ! -e "$WATCHDOG_LOG" ]; then
    log_state=missing
    emit_finding WATCHDOG_LOG_UNAVAILABLE info "watchdog.log absent path=$WATCHDOG_LOG"
  elif [ ! -r "$WATCHDOG_LOG" ]; then
    log_state=unreadable
    emit_finding WATCHDOG_LOG_UNAVAILABLE info "watchdog.log unreadable path=$WATCHDOG_LOG"
  else
    log_state=ok
    age=$((NOW_EPOCH - $(epoch_mtime "$WATCHDOG_LOG")))
    if [ "$age" -gt "$WATCHDOG_STALE_S" ]; then
      stale=1
      emit_finding WATCHDOG_STALE warn "watchdog.log mtime_age_s=$age threshold_s=$WATCHDOG_STALE_S path=$WATCHDOG_LOG"
    fi
  fi

  # r4: this used to be a bare `find | wc -l | tr` pipeline — under `set -euo
  # pipefail` an unreadable `.ufo/state` failed the whole pipeline and killed the
  # census before any verdict (rc 1, header only; canary B in
  # corpus/lessons/2026-10-15-errexit-pipefail-silent-crash.md, re-measured at
  # fe22a14f). The walk is rc-gated now, like the wave-age read at `:296-302`:
  # an unreadable state dir renders the count `unavailable` with a disclosure
  # field and every other surface still reports. A missing or empty dir cannot
  # fail the walk, so it keeps the plain provable count.
  #
  # r7: the count alone could not see a FROZEN round counter (r2 note §1 Gaps).
  # The VALUES are read now, the maximum is reported, and each value is compared
  # with the watchdog's own record of that lane's last launch round — the
  # ledger's last `launch <lane> round=N` line, which the driver writes in the
  # same tick right after the state file (scripts/shokunin-watchdog.sh:80-81).
  # A value below that round is WATCHDOG_STATE_LAG, above it is
  # WATCHDOG_STATE_AHEAD; both INFO. An inconsistent state file is evidence a
  # reader must see, not proof the fleet is unhealthy, so neither flips the
  # roll: the gap closed here is invisibility, not severity.
  local state_n=0 state_read=ok state_field='' state_max=0 state_lag=0 state_ahead=0
  local state_unread_vals=0 state_cmp=0 sf lane_id v lr state_list=''
  local state_unread_sym=0 state_unread_dir=0 state_unread_other=0
  LEDGER=''; LEDGER_RC=1
  if [ -d "$STATE_DIR" ]; then
    # r8: the walk no longer filters on `-type f`. A symlink or a directory named
    # `*.round` was INVISIBLE to the r7 walk (the residual named in
    # surfaces-r7.md §4): not counted, not read, not compared, not disclosed. The
    # entry list now carries every `*.round` entry and each entry is CLASSIFIED
    # before any read, so a non-regular entry is counted as an unreadable value
    # WITH its reason instead of vanishing. Symlinks are never followed: a link
    # points outside the walk's contract (its target is arbitrary bytes, and
    # reading it would let a foreign file's integer enter the rows). `state_rounds`
    # keeps its r7 meaning — regular files — so an existing state dir reads
    # exactly as before; `state_val_unread_reasons` discloses the rest.
    cap find "$STATE_DIR" -maxdepth 1 -name '*.round'
    if [ "$CAP_RC" -eq 0 ]; then
      # The walk output is copied BEFORE load_ledger runs: load_ledger (like
      # every cap caller) overwrites CAP_OUT, and reading the state list out of
      # CAP_OUT after that call iterates the ledger instead of the state files
      # (measured live: 402 unreadable "values" = the ledger's line count).
      # Sorted, so the row's reason counts and the finding ORDER cannot depend on
      # the filesystem's directory order; `|| true` keeps an empty list from
      # tripping pipefail (the r3 lesson class).
      state_list=$(printf '%s\n' "$CAP_OUT" | LC_ALL=C sort || true)
      load_ledger
      while IFS= read -r sf; do
        [ -n "$sf" ] || continue
        if [ -L "$sf" ]; then
          state_unread_sym=$((state_unread_sym + 1))
          emit_finding WATCHDOG_STATE_ENTRY_UNREADABLE info "reason=symlink-not-followed entry=$(basename -- "$sf") path=$sf"
          continue
        fi
        if [ -d "$sf" ]; then
          state_unread_dir=$((state_unread_dir + 1))
          emit_finding WATCHDOG_STATE_ENTRY_UNREADABLE info "reason=is-directory entry=$(basename -- "$sf") path=$sf"
          continue
        fi
        if [ ! -f "$sf" ]; then
          state_unread_other=$((state_unread_other + 1))
          emit_finding WATCHDOG_STATE_ENTRY_UNREADABLE info "reason=non-regular entry=$(basename -- "$sf") path=$sf"
          continue
        fi
        state_n=$((state_n + 1))
        # read_file is [ -r ]-gated; a mode-000 file yields empty, counted as an
        # unreadable VALUE rather than silently as a zero.
        v=$(read_file "$sf")
        v=${v//[[:space:]]/}
        lane_id=$(basename -- "$sf"); lane_id=${lane_id%.round}
        if ! is_int "$v"; then
          state_unread_vals=$((state_unread_vals + 1))
          continue
        fi
        if [ "$v" -gt "$state_max" ]; then state_max=$v; fi
        [ "$LEDGER_RC" -eq 0 ] || continue
        lr=$(ledger_last_launch_round "$lane_id")
        is_int "$lr" || continue
        state_cmp=$((state_cmp + 1))
        if [ "$v" -lt "$lr" ]; then
          state_lag=$((state_lag + 1))
          emit_finding WATCHDOG_STATE_LAG info "lane=$lane_id state_round=$v ledger_round=$lr path=$sf"
        elif [ "$v" -gt "$lr" ]; then
          state_ahead=$((state_ahead + 1))
          emit_finding WATCHDOG_STATE_AHEAD info "lane=$lane_id state_round=$v ledger_round=$lr path=$sf"
        fi
      done <<< "$state_list"
    else
      state_read=unreadable
    fi
  fi

  if [ "$pid_n" -eq 0 ]; then
    emit_finding WATCHDOG_ABSENT warn "no shokunin-watchdog process matched by pgrep -af"
  fi

  local st=ok
  if [ "$pid_n" -eq 0 ] || [ "$stale" -eq 1 ]; then st=drift; fi
  if [ "$log_state" = missing ] || [ "$log_state" = unreadable ]; then
    # log missing alone is unavailable if we also lack pids assessment path
    if [ "$pid_n" -eq 0 ] && [ "$log_state" != ok ]; then st=drift; fi
  fi

  # The disclosure only appears when the walk failed; a readable dir keeps the
  # r2 fields (`state_rounds=<n>`) with the r7 value fields appended. r8 adds the
  # non-regular reasons: state_val_unreadable is the TOTAL of every entry that
  # could not contribute a value (unreadable regular value, symlink, directory,
  # other non-regular), and the reasons field splits it by class so an operator
  # can tell a permission problem from a stray symlink.
  state_field="state_rounds=$state_n state_rounds_max=$state_max state_lag=$state_lag state_ahead=$state_ahead state_cmp=$state_cmp state_val_unreadable=$((state_unread_vals + state_unread_sym + state_unread_dir + state_unread_other)) state_val_unread_reasons=file:$state_unread_vals symlink:$state_unread_sym dir:$state_unread_dir other:$state_unread_other"
  if [ "$state_read" = unreadable ]; then
    state_field='state_rounds=unavailable state_unreadable=1'
  elif [ "$LEDGER_RC" -ne 0 ]; then
    state_field="$state_field state_ledger=unreadable"
  fi
  detail="cmd=$cmd_bits; pids=$pid_n; log=$log_state; age_s=${age:-?}; stale_threshold_s=$WATCHDOG_STALE_S; $state_field; ts=$TS_UTC"
  emit_surface watchdog "$st" "$detail"
}

# ---- surface: waves ---------------------------------------------------------
# Settlement join (r1):
#   train-style: swarm-registry.json + dispatch.json + (results.json|closeout.json)
#   12h-style:   run.json + task-response.json + optional results.json
# Settled if results.json OR closeout.json OR mission-result.json exists.
# Dispatched-but-unsettled if registry|dispatch|run present and no settle file.
# Age = NOW - newest file mtime in the wave dir (observation only).
# Unsettled + age > WAVE_UNSETTLED_S => WAVE_UNSETTLED_AGE (DRIFT).
# Never call unsettled "failed".
probe_waves() {
  local cmd="find $WAVES_DIR -maxdepth 1 -mindepth 1 -type d"
  local n_total=0 n_settled=0 n_unsettled=0 n_empty=0 n_aged=0 n_age_unread=0
  local d base has_reg has_disp has_run has_settle newest age st

  if [ ! -d "$WAVES_DIR" ]; then
    emit_surface waves unavailable "cmd=$cmd; waves_dir=missing path=$WAVES_DIR; ts=$TS_UTC"
    return 0
  fi

  st=ok
  for d in "$WAVES_DIR"/*; do
    [ -d "$d" ] || continue
    base=$(basename -- "$d")
    case "$base" in round-*|.*) continue ;; esac
    n_total=$((n_total + 1))
    has_reg=0 has_disp=0 has_run=0 has_settle=0
    [ -f "$d/swarm-registry.json" ] && has_reg=1
    [ -f "$d/dispatch.json" ] && has_disp=1
    [ -f "$d/run.json" ] && has_run=1
    # Settlement is a TYPED token, not just a filename: this host's wave dirs
    # close out with `closeout.md` (markdown) and/or a registry carrying
    # `"closed": true`, neither of which a results-file test sees. Measured
    # 2026-10-15: w5..w11 are closed with ADMIT verdicts and no results file, so a
    # filename-only test aged five settled waves into false WAVE_UNSETTLED_AGE.
    if [ -f "$d/results.json" ] || [ -f "$d/closeout.json" ] || [ -f "$d/mission-result.json" ] || [ -f "$d/closeout.md" ]; then
      has_settle=1
    else
      for cand in "$d/swarm-registry.json" "$d/dispatch.json" "$d/run.json" "$d/spec.json"; do
        [ -f "$cand" ] || continue
        if grep -qE '"(closed|settled)"[[:space:]]*:[[:space:]]*true|"status"[[:space:]]*:[[:space:]]*"closed"' "$cand" 2>/dev/null; then
          has_settle=1; break
        fi
      done
    fi

    # r2: this age used to be read through a `find | sort | tail | cut` command
    # substitution whose nonzero pipeline rc (pipefail) aborted the whole census
    # under `set -e` when the walk hit an unreadable subtree — the same construct
    # the silence probe carried at line 517 of the r1 file. The rc is graded now:
    # an unreadable wave age is counted and disclosed, and never compared against
    # a threshold the read cannot prove.
    cap find "$d" -type f -printf '%T@\n'
    newest=''
    if [ "$CAP_RC" -eq 0 ]; then
      newest=$(printf '%s\n' "$CAP_OUT" | sort -n | tail -1 | cut -d. -f1)
    else
      n_age_unread=$((n_age_unread + 1))
    fi
    age=0
    if [ -n "${newest:-}" ]; then age=$((NOW_EPOCH - newest)); fi

    if [ "$has_settle" -eq 1 ]; then
      n_settled=$((n_settled + 1))
    elif [ "$has_reg" -eq 1 ] || [ "$has_disp" -eq 1 ] || [ "$has_run" -eq 1 ]; then
      n_unsettled=$((n_unsettled + 1))
      if [ "$age" -gt "$WAVE_UNSETTLED_S" ]; then
        n_aged=$((n_aged + 1))
        emit_finding WAVE_UNSETTLED_AGE warn "wave=$base age_s=$age threshold_s=$WAVE_UNSETTLED_S reg=$has_reg disp=$has_disp run=$has_run settle=0"
        st=drift
      fi
    else
      n_empty=$((n_empty + 1))
    fi
  done

  emit_surface waves "$st" "cmd=$cmd; total=$n_total settled=$n_settled unsettled=$n_unsettled aged_unsettled=$n_aged empty=$n_empty age_unreadable=$n_age_unread threshold_s=$WAVE_UNSETTLED_S; ts=$TS_UTC"
}

# ---- surface: journal notice/record classes (r13; r14 alarm + routing) ------
# Authority: corpus/knowledge/kill-classes-by-message-id-r12.md and
# corpus/knowledge/structured-journal-scopes-r13.md (catalog ids, notice !=
# kill, scopes never summed), S013/S035/S036 (pinned catalog + unit.c
# emitters), S015 (UNIT=/USER_UNIT= name the unit a manager logs ABOUT;
# _SYSTEMD_* describe the emitting process), QUALITY #15/#16.
#
# A journal class is counted by a stable STRUCTURED field, never by MESSAGE text
# (QUALITY #15; lessons/round-12.md#M13). Counts are scoped RECORD counts: one
# kernel kill can produce several per-unit notices, a fc2e22bc record is a
# coredump notice, and d989611b is systemd-oomd's per-unit notice. None is a
# victim or fleet-cause count. Every non-underscore journal field here is
# client-supplied, so counts carry `trust=client-supplied`; `_BOOT_ID` is
# requested and validated on every record, and a validated boot id is the only
# journal value echoed. User and system journals are separate SURFACE rows
# (journal.user / journal.system) and are never summed.
#
# Classes (6 queries per scope):
#   kernel_oom_notice    MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef  notice
#   oomd_notice          MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed  notice
#   coredump_notice      MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1  notice
#   segfault_signal11    COREDUMP_SIGNAL=11 (RECORD subset of coredump records)
#   unit_sigkill_record  MESSAGE_ID=98e322203f7a4ed290d09fe03c09fe15
#                        EXIT_CODE=killed EXIT_STATUS=9 (unit process, SIGKILL)
#   unit_failure_record  MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c (Unit failed)
# The unit_failure query additionally requests UNIT,USER_UNIT,UNIT_RESULT and
# splits ONE record set in ONE jq pass (no second query, so the subsets cannot
# race): a fleet | non-fleet | unknown subject partition (sum == total) and the
# UNIT_RESULT=oom-kill subset.
#
# R14 routing rules:
#   subject      exactly one of UNIT/USER_UNIT present, in EITHER journal scope
#                (USER_UNIT records can legitimately appear in the system
#                journal). Both present — even with equal values — neither
#                present, or a value that is not a valid systemd unit name
#                (string, 1..255, systemd charset incl. @ : and \xHH escapes,
#                known unit suffix) is UNKNOWN, never non-fleet.
#                _SYSTEMD_UNIT/_SYSTEMD_USER_UNIT are the EMITTER and are never
#                read for classification.
#   fleet        case-insensitive substring match of the frozen r12 marker set
#                (`classification_rule=unit-name-token`) against the subject
#                name only. "non-fleet" means "no marker" — a routing hint for
#                tsukuroi, not proof that a unit is unrelated to fleet work.
#   findings     UNIT_FAILURE_JOURNAL(_SYSTEM) info, fleet-only;
#                UNIT_FAILURE_OUT_OF_SCOPE(_SYSTEM) info owner=tsukuroi;
#                UNIT_FAILURE_UNATTRIBUTED_JOURNAL info (ONE id, scope=user|system,
#                owner=unresolved reason=subject-metadata-unknown). Only the OOM
#                crit and the user KILL_SIGNAL warn (process SIGKILL OR unit
#                result signal) flip the roll.
#   universe     r13's UNIT_FAILURE_JOURNAL_SYSTEM counted ALL system unit
#                failures; r14 makes it fleet-only. Pre-r13 history had no
#                system scope, so this split is new semantics, not a silent
#                reuse of the id.
#   oom          a kernel-OOM unit notice (fe6faa94) in EITHER scope, or a unit
#                that failed with UNIT_RESULT=oom-kill in either scope, emits
#                EXACTLY ONE global OOM_KILL_JOURNAL crit. Per-scope/per-source
#                counters (user_notice, system_notice, user_unit_oom,
#                system_unit_oom) are separate, appear once and are never
#                summed. Drift counts that alarm LINE, not records or kills; the
#                result path can come from the kernel OOM killer or from
#                systemd-oomd. Subject validity never gates the alarm.
#   unknown      a non-string/missing UNIT_RESULT contributes only to
#                unit_oom_result_unknown: never a fabricated known 0 and never
#                oom evidence.
# No query asks for MESSAGE. A nonzero journalctl rc (never parsed as a count),
# an absent journalctl/jq, malformed JSON, a record without the validated
# fields, a non-matching MESSAGE_ID, or records from more than one boot makes
# that class unavailable — it is never reported as 0, and its split tokens read
# unavailable:<reason> (a timeout is unavailable, never an alarm). A
# system-scope zero says the queried journal scope held no matching records; it
# does not say whether a service was active or inactive.
#
# The prior TEXT classes are gone, not aliased: the old probe grepped MESSAGE
# text, which is not metadata (QUALITY #15) and cannot be a reliable kill
# counter: a historical MESSAGE-selected text sample (round-12 M19, r13 errata)
# counted 5 kernel "Killed process" text matches against 7 user + 9 system
# fe6faa94 notices in the same boot; that is not a victim census and the text
# counts are not reproduced here. JOURNAL_CLASSES_UNMEASURED names each remaining
# unmeasured class with a reason that distinguishes a retired text heuristic, an
# unimplemented structured field, and the possibility that no record was
# retained at all. Remaining text-only surfaces are never a look-alike 0.
JOURNAL_ID_KERNEL_OOM=fe6faa94e7774663a0da52717891d8ef
JOURNAL_ID_OOMD=d989611b15e44c9dbf31e3c81256e4ed
JOURNAL_ID_COREDUMP=fc2e22bc6ee647b6b90729ab34a250b1
JOURNAL_ID_UNIT_SIGKILL=98e322203f7a4ed290d09fe03c09fe15
JOURNAL_ID_UNIT_FAILURE=d9b373ed55a64feb8242e02dbe79a49c
# One jq pass validates every record and emits `<records>\t<boots>\t<boot>`.
# Slurped empty input is `[]` -> `0	0	none` at rc 0: a valid empty query is 0.
JOURNAL_JQ_TAIL='then [length, ([.[]._BOOT_ID] | unique | length), ([.[]._BOOT_ID][0] // "none")] | @tsv else (if all(.[]; type == "object" and (._BOOT_ID | type) == "string" and ((._BOOT_ID | length) > 0)) then ([.[]._BOOT_ID] | unique | length) as $b | if $b > 1 then "multi-boot" elif all(.[]; ._BOOT_ID == $boot) then "record-invalid" else "boot-mismatch" end else "record-invalid" end) end'
JOURNAL_JQ_MSGID="if all(.[]; type == \"object\" and (._BOOT_ID | type) == \"string\" and (._BOOT_ID == \$boot) and (.MESSAGE_ID == \$id)) $JOURNAL_JQ_TAIL"
JOURNAL_JQ_SIGKILL="if all(.[]; type == \"object\" and (._BOOT_ID | type) == \"string\" and (._BOOT_ID == \$boot) and (.MESSAGE_ID == \$id) and (.EXIT_CODE == \"killed\") and ((.EXIT_STATUS | tostring) == \"9\")) $JOURNAL_JQ_TAIL"
JOURNAL_JQ_SIGSEGV="if all(.[]; type == \"object\" and (._BOOT_ID | type) == \"string\" and (._BOOT_ID == \$boot) and (.MESSAGE_ID == \$id) and ((.COREDUMP_SIGNAL | tostring) == \"11\")) $JOURNAL_JQ_TAIL"

# r14 unit-failure split: ONE jq pass over the d9b373ed record set, so the
# subsets cannot race a second journal scan. Column order (15 columns, checked
# exactly by journal_query):
#   total fleet nonfleet unknown missing ambiguous malformed
#   oom oom_fleet oom_nonfleet oom_subject_unknown oom_result_unknown signal
#   boots boot
# Invariants: fleet+nonfleet+unknown == total. oom and signal are MUTUALLY
# EXCLUSIVE result subsets (one UNIT_RESULT string per record); each overlaps
# the fleet/nonfleet/unknown subject buckets, so neither is disjoint from them.
#   subject  exactly one of UNIT/USER_UNIT present (has(), so a null field still
#            counts as present). Both present — even equal — neither present, or
#            a non-string/invalid name is UNKNOWN, never non-fleet. Valid names
#            are strings 1..255 over the ASCII safe set [A-Za-z0-9_.:@-] plus
#            ONLY literal \xHH escape sequences (a bare backslash or \q is
#            malformed), with a known unit suffix.
#   oom      UNIT_RESULT is the STRING "oom-kill". A non-string/array/null/
#            missing UNIT_RESULT is oom_result_unknown, never oom evidence.
#   signal   UNIT_RESULT is the STRING "signal" (the pre-r13 text class warned
#            on "Failed with result 'signal'"; it is a result ordinal, not proof
#            of SIGKILL).
#   output   only integers and the validated _BOOT_ID token; no unit or result
#            value is ever printed (unit bytes never reach a row or finding).
FLEET_UNIT_TOKENS='shokunin|ufo-sighting|tmux-spawn|the-tick|fleet'
JOURNAL_JQ_UNITS='def subject:
  ((has("UNIT") | if . then 1 else 0 end) + (has("USER_UNIT") | if . then 1 else 0 end)) as $np
  | if $np == 0 then {kind:"missing"}
    elif $np > 1 then {kind:"ambiguous"}
    else
      (.UNIT // .USER_UNIT) as $v
      | if ($v | type) == "string"
           and ($v | length) > 0
           and ($v | length) <= 255
           and ($v | test("^([A-Za-z0-9_.:@-]|\\\\x[0-9A-Fa-f]{2})+$"))
           and ($v | test("\\.(service|socket|device|mount|automount|swap|target|path|timer|slice|scope)$"))
        then {kind:"unit", name:($v | ascii_downcase)}
        else {kind:"malformed"} end
    end;
def fleet: .kind == "unit" and (.name | test($fleet));
def oom: ((.UNIT_RESULT? | type) == "string" and .UNIT_RESULT == "oom-kill");
def sig: ((.UNIT_RESULT? | type) == "string" and .UNIT_RESULT == "signal");
def resunk: ((.UNIT_RESULT? | type) != "string");
if all(.[]; type == "object" and (._BOOT_ID | type) == "string" and (._BOOT_ID == $boot) and (.MESSAGE_ID == $id)) then
  [ .[] | {s: subject, o: oom, g: sig, ru: resunk} ] as $r
  | [ ($r|length),
      ($r|map(select(.s|fleet))|length),
      ($r|map(select(.s.kind=="unit" and ((.s|fleet)|not)))|length),
      ($r|map(select(.s.kind!="unit"))|length),
      ($r|map(select(.s.kind=="missing"))|length),
      ($r|map(select(.s.kind=="ambiguous"))|length),
      ($r|map(select(.s.kind=="malformed"))|length),
      ($r|map(select(.o))|length),
      ($r|map(select(.o and (.s|fleet)))|length),
      ($r|map(select(.o and .s.kind=="unit" and ((.s|fleet)|not)))|length),
      ($r|map(select(.o and .s.kind!="unit"))|length),
      ($r|map(select(.ru))|length),
      ($r|map(select(.g))|length),
      ([.[]._BOOT_ID]|unique|length),
      ([.[]._BOOT_ID][0] // "none")
    ] | @tsv
else (if all(.[]; type == "object" and (._BOOT_ID | type) == "string" and ((._BOOT_ID | length) > 0)) then ([.[]._BOOT_ID] | unique | length) as $b | if $b > 1 then "multi-boot" elif all(.[]; ._BOOT_ID == $boot) then "record-invalid" else "boot-mismatch" end else "record-invalid" end) end'


# journal_query <scope-flag> <output-fields> <match words> <jq-filter> [jq args...]
# -> JQ_N JQ_BOOTS JQ_BOOT JQ_VEC JQ_STATUS
# JOURNAL_Q_WIDTH (a caller-prefixed assignment) is the exact column count the
# filter must emit; the default 3 is the legacy <records>\t<boots>\t<boot>.
# The match words are whitespace-split (journalctl wants one FIELD=value per
# argv element; every value here is whitespace-free).
journal_query() {
  local flag=$1 fields=$2 match=$3 filter=$4
  shift 4
  local -a m=()
  read -r -a m <<< "$match"
  JQ_N=''; JQ_BOOTS=''; JQ_BOOT=''; JQ_STATUS=''; JQ_VEC=''
  if ! have "$TIMEOUT_BIN" && [ ! -x "$TIMEOUT_BIN" ]; then
    # Never run an unbounded journal scan when the bound is unavailable.
    JQ_STATUS=no-timeout-bin
    return 0
  fi
  # The coprocess is `wc -c`: it drains stderr continuously (a large warning can
  # never block the producer on a full pipe) and emits only the byte count, never
  # the bytes. Coproc descriptors are not available inside the capture's
  # command-substitution subshell, so duplicate them into ordinary persistent
  # dynamic fds and close the originals: the capture redirects to `$w`, and `wc`
  # sees EOF when OUR `$w` closes, not when a leaked original is collected. The
  # PID is captured first because bash may clear the coproc array once reaped.
  local w r err_pid cin cout
  coproc JOURNAL_ERR { wc -c; }
  err_pid=$JOURNAL_ERR_PID; cin=${JOURNAL_ERR[1]}; cout=${JOURNAL_ERR[0]}
  exec {w}>&"$cin"
  exec {r}<&"$cout"
  exec {cin}>&-
  exec {cout}<&-
  set +e
  CAP_OUT=$("$TIMEOUT_BIN" -k 1 "$JOURNAL_TIMEOUT_S" "$JOURNALCTL_BIN" "$flag" -b --no-pager -o json --output-fields="$fields" "${m[@]}" 2>&"$w")
  CAP_RC=$?
  set -e
  exec {w}>&-
  local err_bytes=0
  IFS= read -r err_bytes <&"$r" || true
  err_bytes=${err_bytes//[[:space:]]/}
  case "$err_bytes" in ''|*[!0-9]*) err_bytes=0 ;; esac
  wait "$err_pid" 2>/dev/null || true
  exec {r}<&-
  unset JOURNAL_ERR JOURNAL_ERR_PID
  if [ "$CAP_RC" -ne 0 ]; then
    # A producer failure is unavailable: never parse or count its partial bytes.
    case "$CAP_RC" in
      124|137) JQ_STATUS=timeout ;;
      *) JQ_STATUS="rc-$CAP_RC" ;;
    esac
    return 0
  fi
  if [ "$err_bytes" -gt 0 ]; then
    # Presence only: the bytes were counted and discarded, never stored/echoed.
    JQ_STATUS=stderr-nonempty
    return 0
  fi
  local raw=$CAP_OUT parsed jrc n nb boot width=${JOURNAL_Q_WIDTH:-3}
  local -a vec=()
  set +e
  parsed=$("$JQ_BIN" -s -r "$@" "$filter" <<< "$raw" 2>/dev/null)
  jrc=$?
  set -e
  if [ "$jrc" -ne 0 ]; then JQ_STATUS=malformed-json; return 0; fi
  case "$parsed" in
    record-invalid|multi-boot|boot-mismatch) JQ_STATUS=$parsed; return 0 ;;
  esac
  # r14: a filter may emit more columns than the legacy <n>\t<boots>\t<boot>.
  # The column COUNT is checked exactly, every count column must be a plain
  # non-negative integer, the boot column must be the 32-hex id (or `none` for
  # the proven-empty vector). A short/long/injected row is malformed, never a
  # partial count.
  IFS=$'\t' read -r -a vec <<< "$parsed" || true
  if [ "${#vec[@]}" -ne "$width" ]; then JQ_STATUS=malformed-json; return 0; fi
  local i
  for ((i = 0; i < width - 2; i++)); do
    is_int "${vec[$i]}" || { JQ_STATUS=malformed-json; return 0; }
  done
  n=${vec[0]}
  nb=${vec[$((width - 2))]}
  boot=${vec[$((width - 1))]}
  if ! is_int "$nb"; then JQ_STATUS=malformed-json; return 0; fi
  if [ "$nb" -eq 0 ]; then
    [ "$n" -eq 0 ] || { JQ_STATUS=record-invalid; return 0; }
    JQ_N=0; JQ_BOOTS=0; JQ_STATUS=ok
    JQ_VEC=$parsed
    return 0
  fi
  if [ "$nb" -ne 1 ]; then JQ_STATUS=multi-boot; return 0; fi
  # The only journal-derived string this probe echoes is a boot id. systemd
  # emits exactly 32 lowercase hex chars; anything else could forge tokens or an
  # extra output line, so it grades the class unavailable instead.
  case "$boot" in
    *[!0-9a-f]*) JQ_STATUS=record-invalid; return 0 ;;
  esac
  if [ "${#boot}" -ne 32 ]; then JQ_STATUS=record-invalid; return 0; fi
  JQ_N=$n; JQ_BOOTS=$nb; JQ_BOOT=$boot; JQ_VEC=$parsed; JQ_STATUS=ok
}

journal_finding_id() { # <scope> <class>
  case "$1:$2" in
    user:oomd_notice)          printf '%s' OOMD_NOTICE_JOURNAL_USER ;;
    system:oomd_notice)        printf '%s' OOMD_NOTICE_JOURNAL_SYSTEM ;;
    user:coredump_notice)      printf '%s' COREDUMP_NOTICE_JOURNAL_USER ;;
    system:coredump_notice)    printf '%s' COREDUMP_NOTICE_JOURNAL_SYSTEM ;;
    user:segfault_signal11)    printf '%s' SEGFAULT_SIGNAL11_JOURNAL_USER ;;
    system:segfault_signal11)  printf '%s' SEGFAULT_SIGNAL11_JOURNAL_SYSTEM ;;
    user:unit_sigkill_record)  printf '%s' KILL_SIGNAL_JOURNAL ;;
    system:unit_sigkill_record) printf '%s' KILL_SIGNAL_JOURNAL_SYSTEM ;;
  esac
}

probe_journal() {
  local cmd_tmpl="$JOURNALCTL_BIN <--user|--system> -b --no-pager -o json --output-fields=_BOOT_ID,MESSAGE_ID[,...] MESSAGE_ID=<id>"
  local flag scope cls key n subj d st rc_n uf
  local -a classes=(kernel_oom_notice oomd_notice coredump_notice segfault_signal11 unit_sigkill_record unit_failure_record)
  local -A ids=( [kernel_oom_notice]=$JOURNAL_ID_KERNEL_OOM [oomd_notice]=$JOURNAL_ID_OOMD [coredump_notice]=$JOURNAL_ID_COREDUMP [unit_failure_record]=$JOURNAL_ID_UNIT_FAILURE [segfault_signal11]='' [unit_sigkill_record]='' )
  local -A jn=() js=() sboot=() src=() ucnt=()
  local -a vec=() unit_fields=(fleet nonfleet unknown missing ambiguous malformed oom oom_fleet oom_nonfleet oom_subject_unknown oom_result_unknown signal)
  local oom_fire=0 oom_paths='' oom_fields=''
  local ko uo uou ps us kill_fire=0 kill_paths=''
  local oom_path_k=0 oom_path_u=0

  # Named coverage loss, not a look-alike zero. Each unmeasured class carries a
  # reason that separates a RETIRED TEXT HEURISTIC from an unimplemented
  # STRUCTURED class from the possibility that no record was retained at all
  # (MESSAGE text is not an acceptable substitute, Q15). Emitted on every run,
  # including a run where journalctl itself is missing.
  emit_finding JOURNAL_CLASSES_UNMEASURED info "classes=kernel_victim_text,gpf_text,other_signals,uncataloged_unit_failure basis=unmeasured reasons=kernel_victim_text:text-heuristic-retired,gpf_text:text-heuristic-retired,other_signals:structured-field-unimplemented,uncataloged_unit_failure:text-heuristic-retired counted_structured=kernel_oom_notice,oomd_notice,coredump_notice,segfault_signal11,unit_sigkill_record,unit_failure_record absent_records=possible:no-retained-record-is-not-no-event note=other_signals has structured EXIT_CODE/EXIT_STATUS records (S036) but only EXIT_STATUS=9 is implemented here; the retired text classes are not aliases and are never counted"
  if ! have "$JOURNALCTL_BIN" && [ ! -x "$JOURNALCTL_BIN" ]; then
    for scope in user system; do
      emit_surface "journal.$scope" unavailable "cmd=$cmd_tmpl; scope=$scope; journalctl=missing; unit=notice trust=client-supplied rc=na; ts=$TS_UTC"
    done
    return 0
  fi
  if ! have "$JQ_BIN" && [ ! -x "$JQ_BIN" ]; then
    for scope in user system; do
      emit_surface "journal.$scope" unavailable "cmd=$cmd_tmpl; scope=$scope; parser=missing bin=$JQ_BIN; unit=notice trust=client-supplied rc=na; ts=$TS_UTC"
    done
    return 0
  fi
  if [ -z "$BOOT_ID_EXPECTED" ]; then
    for scope in user system; do
      emit_surface "journal.$scope" unavailable "cmd=$cmd_tmpl; scope=$scope; boot_id=unavailable source=$BOOT_ID_FILE; unit=notice trust=client-supplied rc=na; ts=$TS_UTC"
    done
    return 0
  fi

  for flag in --user --system; do
    scope=${flag#--}
    src[$scope]=0
    for cls in "${classes[@]}"; do
      key="$scope:$cls"
      case "$cls" in
        segfault_signal11)
          journal_query "$flag" '_BOOT_ID,MESSAGE_ID,COREDUMP_SIGNAL' "MESSAGE_ID=$JOURNAL_ID_COREDUMP COREDUMP_SIGNAL=11" "$JOURNAL_JQ_SIGSEGV" --arg boot "$BOOT_ID_EXPECTED" --arg id "$JOURNAL_ID_COREDUMP" ;;
        unit_sigkill_record)
          journal_query "$flag" '_BOOT_ID,MESSAGE_ID,EXIT_CODE,EXIT_STATUS' "MESSAGE_ID=$JOURNAL_ID_UNIT_SIGKILL EXIT_CODE=killed EXIT_STATUS=9" "$JOURNAL_JQ_SIGKILL" --arg boot "$BOOT_ID_EXPECTED" --arg id "$JOURNAL_ID_UNIT_SIGKILL" ;;
        unit_failure_record)
          # One record set, one jq pass: the class total and its fleet /
          # non-fleet / unknown / oom / signal subsets share the validated
          # records, so no subset can disagree with or race the total.
          JOURNAL_Q_WIDTH=15 journal_query "$flag" '_BOOT_ID,MESSAGE_ID,UNIT,USER_UNIT,UNIT_RESULT' "MESSAGE_ID=${ids[$cls]}" "$JOURNAL_JQ_UNITS" --arg boot "$BOOT_ID_EXPECTED" --arg id "${ids[$cls]}" --arg fleet "$FLEET_UNIT_TOKENS"
          if [ "$JQ_STATUS" = ok ]; then
            IFS=$'\t' read -r -a vec <<< "$JQ_VEC"
            ucnt["$scope:total"]=${vec[0]}
            ucnt["$scope:fleet"]=${vec[1]}
            ucnt["$scope:nonfleet"]=${vec[2]}
            ucnt["$scope:unknown"]=${vec[3]}
            ucnt["$scope:missing"]=${vec[4]}
            ucnt["$scope:ambiguous"]=${vec[5]}
            ucnt["$scope:malformed"]=${vec[6]}
            ucnt["$scope:oom"]=${vec[7]}
            ucnt["$scope:oom_fleet"]=${vec[8]}
            ucnt["$scope:oom_nonfleet"]=${vec[9]}
            ucnt["$scope:oom_subject_unknown"]=${vec[10]}
            ucnt["$scope:oom_result_unknown"]=${vec[11]}
            ucnt["$scope:signal"]=${vec[12]}
          fi ;;
        *)
          journal_query "$flag" '_BOOT_ID,MESSAGE_ID' "MESSAGE_ID=${ids[$cls]}" "$JOURNAL_JQ_MSGID" --arg boot "$BOOT_ID_EXPECTED" --arg id "${ids[$cls]}" ;;
      esac
      jn[$key]=$JQ_N; js[$key]=$JQ_STATUS
      case "$JQ_STATUS" in
        rc-*) if [ "${src[$scope]}" -eq 0 ]; then src[$scope]=${JQ_STATUS#rc-}; fi ;;
      esac
      # Every ok filter already enforced _BOOT_ID == BOOT_ID_EXPECTED, so the
      # scope boot for the row is just the validated one. Mixed/foreign boots
      # never reach here: they graded multi-boot/boot-mismatch above.
      if [ "$JQ_STATUS" = ok ] && [ -n "$JQ_BOOT" ]; then sboot[$scope]=$JQ_BOOT; fi
    done
  done

  # Positive counts only: 0 is a surface value, not a finding. The OOM alarm and
  # the user KILL_SIGNAL warn are single global lines; the fleet/non-fleet/
  # unattributed routing is one line per scope (below); every other class keeps
  # one line per scope.
  for scope in user system; do
    for cls in "${classes[@]}"; do
      case "$cls" in
        kernel_oom_notice|unit_failure_record) continue ;;
        unit_sigkill_record) if [ "$scope" = user ]; then continue; fi ;;
      esac
      key="$scope:$cls"
      [ "${js[$key]}" = ok ] || continue
      n=${jn[$key]}
      [ "$n" -gt 0 ] || continue
      case "$cls" in
        segfault_signal11)
          subj="class=segfault_signal11 unit=record source_field=COREDUMP_SIGNAL value=11 count=$n scope=$scope basis=scoped-record-count boot=${sboot[$scope]}" ;;
        unit_sigkill_record)
          subj="class=unit_sigkill_record unit=record message_id=$JOURNAL_ID_UNIT_SIGKILL signal=9 count=$n scope=$scope attribution=none note=unit process exited on SIGKILL; cause unknown (a kernel OOM can also deliver SIGKILL) boot=${sboot[$scope]}" ;;
        *)
          subj="class=$cls unit=notice message_id=${ids[$cls]} count=$n scope=$scope trust=client-supplied basis=scoped-record-count boot=${sboot[$scope]}" ;;
      esac
      emit_finding "$(journal_finding_id "$scope" "$cls")" info "$subj"
    done
  done

  # ---- unit-failure routing (r14) -----------------------------------------
  # One validated record set split three ways by the SUBJECT unit metadata:
  # fleet (historical marker set, owner=mori), non-fleet (owner=tsukuroi; the
  # desktop/OS diagnosis route), unattributed (owner=unresolved). All three are
  # INFO and none flips the roll: only the OOM crit and the user KILL_SIGNAL
  # warn do. No unit byte is echoed — only integer counts.
  for scope in user system; do
    key="$scope:unit_failure_record"
    [ "${js[$key]}" = ok ] || continue
    fleetn=${ucnt["$scope:fleet"]}
    nonfleetn=${ucnt["$scope:nonfleet"]}
    unknownn=${ucnt["$scope:unknown"]}
    if [ "$fleetn" -gt 0 ]; then
      if [ "$scope" = user ]; then
        emit_finding UNIT_FAILURE_JOURNAL info "class=unit_failure_record unit=record message_id=$JOURNAL_ID_UNIT_FAILURE count=$fleetn subject=fleet owner=mori classification_rule=unit-name-token scope=user basis=scoped-record-count boot=${sboot[$scope]} note=unit entered failed state; the subject unit name carries a fleet marker (any UNIT_RESULT, oom-kill included); marker match is a routing rule, not proof of fleet ownership"
      else
        emit_finding UNIT_FAILURE_JOURNAL_SYSTEM info "class=unit_failure_record unit=record message_id=$JOURNAL_ID_UNIT_FAILURE count=$fleetn subject=fleet owner=mori classification_rule=unit-name-token scope=system basis=scoped-record-count boot=${sboot[$scope]} note=unit entered failed state; the subject unit name carries a fleet marker (any UNIT_RESULT, oom-kill included); marker match is a routing rule, not proof of fleet ownership"
      fi
    fi
    if [ "$nonfleetn" -gt 0 ]; then
      if [ "$scope" = user ]; then
        emit_finding UNIT_FAILURE_OUT_OF_SCOPE info "class=unit_failure_record count=$nonfleetn subject=nonfleet owner=tsukuroi classification_rule=unit-name-token scope=user basis=scoped-record-count boot=${sboot[$scope]} note=non-fleet units (desktop/OS) — tsukuroi owns these; no fleet marker in the subject unit name (a routing hint, not proof of non-fleet ownership)"
      else
        emit_finding UNIT_FAILURE_OUT_OF_SCOPE_SYSTEM info "class=unit_failure_record count=$nonfleetn subject=nonfleet owner=tsukuroi classification_rule=unit-name-token scope=system basis=scoped-record-count boot=${sboot[$scope]} note=non-fleet units (desktop/OS) — tsukuroi owns these; no fleet marker in the subject unit name (a routing hint, not proof of non-fleet ownership)"
      fi
    fi
    if [ "$unknownn" -gt 0 ]; then
      if [ "$scope" = user ]; then
        emit_finding UNIT_FAILURE_UNATTRIBUTED_JOURNAL info "class=unit_failure_record count=$unknownn missing=${ucnt["$scope:missing"]} ambiguous=${ucnt["$scope:ambiguous"]} malformed=${ucnt["$scope:malformed"]} subject=unknown owner=unresolved reason=subject-metadata-unknown scope=user basis=scoped-record-count boot=${sboot[$scope]} note=subject UNIT/USER_UNIT absent, both present, or not a valid unit name; the raw count stays in SURFACE unit_failure_record; never classified fleet or non-fleet"
      else
        emit_finding UNIT_FAILURE_UNATTRIBUTED_JOURNAL info "class=unit_failure_record count=$unknownn missing=${ucnt["$scope:missing"]} ambiguous=${ucnt["$scope:ambiguous"]} malformed=${ucnt["$scope:malformed"]} subject=unknown owner=unresolved reason=subject-metadata-unknown scope=system basis=scoped-record-count boot=${sboot[$scope]} note=subject UNIT/USER_UNIT absent, both present, or not a valid unit name; the raw count stays in SURFACE unit_failure_record; never classified fleet or non-fleet"
      fi
    fi
  done

  # ---- OOM alarm (r14 restoration) -----------------------------------------
  # EXACTLY ONE global OOM_KILL_JOURNAL crit line per census. The four counters
  # are per scope and per source, appear once, and are NEVER summed. A
  # kernel-OOM unit notice in either scope is an alarm even though it is a
  # notice, not a unique-victim count; a unit that failed with UNIT_RESULT
  # oom-kill is an alarm regardless of subject classification. The result path
  # may come from the kernel OOM killer or from systemd-oomd. An unavailable
  # source keeps its own unavailable:<reason> token and does not alarm; another
  # positive source still does. Drift counts this alarm LINE, not records and
  # not kills.
  for scope in user system; do
    key="$scope:kernel_oom_notice"
    if [ "${js[$key]}" = ok ]; then ko=${jn[$key]}; else ko="unavailable:${js[$key]}"; fi
    key="$scope:unit_failure_record"
    if [ "${js[$key]}" = ok ]; then
      uo=${ucnt["$scope:oom"]}
      uou=${ucnt["$scope:oom_result_unknown"]}
    else
      uo="unavailable:${js[$key]}"
      uou="unavailable:${js[$key]}"
    fi
    case "$ko" in
      unavailable:*) ;;
      *) if [ "$ko" -gt 0 ]; then oom_fire=1; oom_path_k=1; fi ;;
    esac
    case "$uo" in
      unavailable:*) ;;
      *) if [ "$uo" -gt 0 ]; then oom_fire=1; oom_path_u=1; fi ;;
    esac
    if [ "$scope" = user ]; then
      oom_fields="$oom_fields user_notice=$ko user_unit_oom=$uo user_unit_oom_result_unknown=$uou"
    else
      oom_fields="$oom_fields system_notice=$ko system_unit_oom=$uo system_unit_oom_result_unknown=$uou"
    fi
  done
  if [ "$oom_path_k" -eq 1 ]; then oom_paths=kernel_oom_notice; fi
  if [ "$oom_path_u" -eq 1 ]; then oom_paths="${oom_paths:+$oom_paths,}unit_result_oom_kill"; fi
  if [ "$oom_fire" -eq 1 ]; then
    emit_finding OOM_KILL_JOURNAL crit "class=oom_kill alarm=1 paths=$oom_paths$oom_fields scope=user,system trust=client-supplied basis=scoped-record-count boot=$BOOT_ID_EXPECTED note=one alarm line per census; per-scope/per-source counters are separate and never summed; a per-unit notice or unit result is not a unique-victim, kill-total or fleet-cause count (kernel OOM or systemd-oomd); drift counts this alarm line, not records"
  fi

  # ---- user KILL_SIGNAL warn (r14) -----------------------------------------
  # The pre-r13 text class warned on a user unit process killed by SIGKILL and
  # on a user unit whose failure result was 'signal'. Both structured paths
  # keep the SAME one warn line with separate counters (never summed): the
  # unit-process SIGKILL records and the UNIT_RESULT=signal unit failures. A
  # user signal result alone is DRIFT. The system scope keeps no such warn.
  key='user:unit_sigkill_record'
  if [ "${js[$key]}" = ok ]; then ps=${jn[$key]}; else ps="unavailable:${js[$key]}"; fi
  key='user:unit_failure_record'
  if [ "${js[$key]}" = ok ]; then us=${ucnt["user:signal"]}; else us="unavailable:${js[$key]}"; fi
  case "$ps" in
    unavailable:*) ;;
    *) if [ "$ps" -gt 0 ]; then kill_fire=1; kill_paths=process_sigkill; fi ;;
  esac
  case "$us" in
    unavailable:*) ;;
    *) if [ "$us" -gt 0 ]; then kill_fire=1; kill_paths="${kill_paths:+$kill_paths,}unit_result_signal"; fi ;;
  esac
  if [ "$kill_fire" -eq 1 ]; then
    emit_finding KILL_SIGNAL_JOURNAL warn "class=kill_signal paths=$kill_paths count=$ps process_sigkill=$ps user_unit_signal=$us scope=user attribution=none basis=scoped-record-count boot=$BOOT_ID_EXPECTED note=unit process exited on SIGKILL and/or unit failed with result signal; cause unknown (a kernel OOM can also deliver SIGKILL); counters are separate and never summed"
  fi

  for scope in user system; do
    st=ok
    d="cmd=$JOURNALCTL_BIN --$scope -b --no-pager -o json --output-fields=_BOOT_ID,MESSAGE_ID[,...] MESSAGE_ID=<id>; scope=$scope"
    # The six r13 class counts keep their names and order.
    for cls in "${classes[@]}"; do
      key="$scope:$cls"
      if [ "${js[$key]}" = ok ]; then
        d="$d $cls=${jn[$key]}"
      else
        st=unavailable
        d="$d $cls=unavailable:${js[$key]}"
      fi
    done
    # r14 unit split: validated integers only. When the unit class is
    # unavailable every split token names the same reason — never a 0 that would
    # read as "no fleet/non-fleet failures".
    key="$scope:unit_failure_record"
    for uf in "${unit_fields[@]}"; do
      if [ "${js[$key]}" = ok ]; then
        d="$d unit_$uf=${ucnt["$scope:$uf"]}"
      else
        d="$d unit_$uf=unavailable:${js[$key]}"
      fi
    done
    rc_n=${src[$scope]:-0}
    # The current boot is known even when this scope held zero matching records,
    # so an empty class still reports the validated boot context, not a hole.
    d="$d; boot=${sboot[$scope]:-$BOOT_ID_EXPECTED}"
    d="$d; unit=notice notice_classes=kernel_oom_notice,oomd_notice,coredump_notice record_classes=segfault_signal11,unit_sigkill_record,unit_failure_record trust=client-supplied field=$scope:MESSAGE_ID oomd_activity=unmeasured rc=$rc_n"
    d="$d; unit_subject_fields=UNIT,USER_UNIT unit_query_output_fields=_BOOT_ID,MESSAGE_ID,UNIT,USER_UNIT,UNIT_RESULT fleet_predicate=unit_name_substring_i fleet_tokens=$FLEET_UNIT_TOKENS fleet_owner=mori nonfleet_owner=tsukuroi unattributed_owner=unresolved classification_rule=unit-name-token nonfleet_basis=no-fleet-marker"
    d="$d; unmeasured=kernel_victim_text,gpf_text,other_signals,uncataloged_unit_failure unmeasured_reasons=kernel_victim_text:text-heuristic-retired,gpf_text:text-heuristic-retired,other_signals:structured-field-unimplemented,uncataloged_unit_failure:text-heuristic-retired absent_records=possible:no-retained-record-is-not-no-event; ts=$TS_UTC"
    emit_surface "journal.$scope" "$st" "$d"
  done
}

# ---- surface: cgroup memory -------------------------------------------------
probe_cgroup() {
  local cmd="cat $CGROUP_EVENTS; cat $CGROUP_CURRENT; cat $CGROUP_PRESSURE; cat $CGROUP_MAX"
  local oom_kill='' oom='' high='' max='' cur='' st=ok

  if [ ! -r "$CGROUP_EVENTS" ]; then
    emit_surface cgroup unavailable "cmd=$cmd; events=unreadable path=$CGROUP_EVENTS; ts=$TS_UTC"
    emit_finding CGROUP_UNAVAILABLE info "memory.events unreadable path=$CGROUP_EVENTS"
    return 0
  fi

  oom_kill=$(cgroup_field "$CGROUP_EVENTS" oom_kill)
  # Cgroup v2 memory.events counters are CUMULATIVE across the boot, so the parent
  # user slice can report a kill that is days old and belongs to a desktop process.
  # Measured 2026-10-15: parent user-1000.slice oom_kill=1 while
  # user@1000.service (the scope that actually contains fleet processes) reads 0,
  # and the event was a terminal python3 on 2026-10-13. Firing `crit` on the parent
  # counter forced a permanent false DRIFT and absorbed tsukuroi's OS triage into
  # mori. The fleet-relevant reading is the session service.
  # Prefer `memory.events.local` — it counts kills in THIS cgroup only, so it is
  # immune to two traps the cumulative/ancestor reads hit: (1) propagation, since
  # a parent's counter includes a descendant's kill (measured: parent slice 1,
  # memory.events.local 0), and (2) a restart, since user@1000.service started
  # 2026-10-14 13:11:07, AFTER the 2026-10-13 23:44:30 kill, so a service-only
  # read would miss an ancestor event entirely. A walk of 101 cgroups found no
  # live cgroup with local oom_kill > 0.
  LOCAL_EVENTS=${MORI_CGROUP_LOCAL_EVENTS:-${CGROUP_EVENTS%.events}.events.local}
  SERVICE_EVENTS=${MORI_CGROUP_SERVICE_EVENTS:-/sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/memory.events}
  service_oom_kill=''
  if [ -r "$LOCAL_EVENTS" ]; then
    service_oom_kill=$(cgroup_field "$LOCAL_EVENTS" oom_kill)
  elif [ -r "$SERVICE_EVENTS" ]; then
    service_oom_kill=$(cgroup_field "$SERVICE_EVENTS" oom_kill)
  fi
  oom=$(cgroup_field "$CGROUP_EVENTS" oom)
  high=$(cgroup_field "$CGROUP_EVENTS" high)
  max=$(cgroup_field "$CGROUP_EVENTS" max)
  # A cgroup counter path must stay inside /sys/fs/cgroup: read_file echoes the
  # first line into the surface row, so an operator-pointed MORI_CGROUP_CURRENT at
  # any other file would print that file's first line. Refuse out-of-tree paths
  # (shape-only refusal, never a read).
  local cg_real
  cg_real=$(realpath -m -- "$CGROUP_CURRENT" 2>/dev/null || printf '%s' "$CGROUP_CURRENT")
  case "$cg_real" in
    /sys/fs/cgroup/*) cur=$(read_file "$cg_real") ;;
    *) cur='refused:outside-sysfs-cgroup' ;;
  esac
  oom_kill=${oom_kill:-0}

  # ---- r7: memory pressure (r2 note §4 Gaps: "unmeasured — no number proposed")
  # PSI is the kernel's own stall accounting, so it is the pressure reading that
  # needs no invented model: `some` = at least one task stalled, `full` = all
  # did. Only shape-validated decimals are printed (is_decimal), so an
  # operator-pinned MORI_CGROUP_PRESSURE at an arbitrary file cannot leak its
  # bytes into the row. Graded on the integer part of `some avg10` against
  # MEM_PSI_WARN_AVG10, a LOCAL placeholder (see the defaults block).
  local psi_some='' psi_full='' psi_state=ok psi10=''
  if [ -r "$CGROUP_PRESSURE" ]; then
    cap cat -- "$CGROUP_PRESSURE"
    if [ "$CAP_RC" -eq 0 ]; then
      psi_some=$(psi_avg10 "$CAP_OUT" some)
      psi_full=$(psi_avg10 "$CAP_OUT" full)
      is_decimal "$psi_some" || psi_some=''
      is_decimal "$psi_full" || psi_full=''
    else
      psi_state=unreadable
    fi
  elif [ -e "$CGROUP_PRESSURE" ]; then
    # Present but not readable is a DIFFERENT fact from absent, and the state
    # field must not claim the file does not exist (measured: a mode-000
    # MORI_CGROUP_PRESSURE was reported `absent` before this branch existed).
    psi_state=unreadable
  else
    psi_state=absent
  fi
  if [ -n "$psi_some" ]; then
    psi10=${psi_some%%.*}
    if is_int "$psi10"; then
      psi10=$((10#$psi10))
      if [ "$psi10" -ge "$MEM_PSI_WARN_AVG10" ]; then
        emit_finding MEM_PRESSURE_HIGH warn "psi_some_avg10=$psi_some threshold_avg10=$MEM_PSI_WARN_AVG10 threshold_label=local path=$CGROUP_PRESSURE"
        st=drift
      fi
    fi
  fi

  # ---- r7: fill pressure -----------------------------------------------------
  # current/limit when the cgroup has a numeric memory.max (the general case:
  # any container or scope with a set limit). This host's user slice reads
  # `max` (unlimited), so the closed-container ratio does not exist here and the
  # fallback is the host's own MemAvailable/MemTotal ratio — a different scope,
  # named on the row (`mem_fill_scope=host-ram`), graded against a LOCAL floor.
  # The current value used for the ratio is the shape-validated numeric read
  # (num_of); the `current=` field above keeps its existing refusal semantics.
  # The limit keeps the literal token `max` (cgroup v2 says "unlimited" with it),
  # which num_of would drop, so it is read with its own shape test: `max` or
  # digits, nothing else may pass into the row.
  local mem_limit='' limit_raw='' fill_pct='' fill_scope='' avail_pct='' mtotal='' mavail='' cur_num=''
  limit_raw=$(read_file "$CGROUP_MAX"); limit_raw=${limit_raw//[[:space:]]/}
  case "$limit_raw" in
    max) mem_limit=max ;;
    '') ;;
    *) if is_int "$limit_raw"; then mem_limit=$limit_raw; fi ;;
  esac
  cur_num=$(num_of "$CGROUP_CURRENT")
  # Branch order matters: the literal `max` is tested FIRST, because
  # `[ max -gt 0 ]` is a bash arithmetic-argument error — measured live as
  # `tools/mori-census.sh: line 705: [: max: integer expected` on stderr while
  # the elif still produced the right answer. A probe must not print shell
  # diagnostics in its normal path (the selftest now fails on that noise).
  if [ "$mem_limit" = max ]; then
    fill_scope=host-ram
    mtotal=$(meminfo_field MemTotal)
    mavail=$(meminfo_field MemAvailable)
    if [ -n "$mtotal" ] && [ "$mtotal" -gt 0 ] && [ -n "$mavail" ]; then
      avail_pct=$((mavail * 100 / mtotal))
      if [ "$avail_pct" -le "$MEM_AVAIL_MIN_PCT" ]; then
        emit_finding MEM_AVAIL_LOW warn "scope=host-ram host_mem_avail_pct=$avail_pct floor_pct=$MEM_AVAIL_MIN_PCT threshold_label=local note=slice memory.max is unlimited, so fill pressure is graded at host scope"
        st=drift
      fi
    else
      fill_scope=unavailable
    fi
  elif [ -n "$mem_limit" ] && [ "$mem_limit" -gt 0 ] && [ -n "$cur_num" ]; then
    fill_scope=cgroup
    fill_pct=$((cur_num * 100 / mem_limit))
    if [ "$fill_pct" -ge "$MEM_FILL_WARN_PCT" ]; then
      emit_finding MEM_FILL_HIGH warn "scope=cgroup mem_fill_pct=$fill_pct threshold_pct=$MEM_FILL_WARN_PCT threshold_label=local current=$cur_num limit=$mem_limit"
      st=drift
    fi
  else
    fill_scope=unavailable
  fi

  # ---- r8: scope high-watermark (the free pressure signal r7 left unread) -----
  # surfaces-r7.md §2 named three memory residuals; two of them are "the only
  # live-observable arm is the host-ram ratio" and "the fixture arms prove
  # arithmetic, not this host's pressure". `memory.peak` is the kernel-maintained
  # high-watermark of THIS scope, readable even when memory.max is the literal
  # `max` (measured on this host: slice peak 28812898304 with max=max), so it is
  # the scope-local live measurement that does not need an invented model or a
  # dwell. Shape-gated by num_of (no arbitrary file's bytes can reach the row),
  # and reported WITH its instance anchor: a peak is cumulative since the cgroup
  # instance was created, so `mem_peak_anchor` (the scope directory's mtime, the
  # nearest free anchor) travels with the number — comparing peaks across a
  # restart without it is unsound (corpus/lessons/2026-10-15-free-lunch-
  # measurements-counter-baselines.md, point 3).
  local peak='' peak_src='' peak_anchor=''
  if [ -r "$CGROUP_PEAK" ]; then
    peak=$(num_of "$CGROUP_PEAK")
    if [ -n "$peak" ]; then
      peak_src=ok
      peak_anchor=$(epoch_mtime "$(dirname -- "$CGROUP_PEAK")")
      is_int "$peak_anchor" || peak_anchor=''
    else
      peak_src=shape-refused
    fi
  elif [ -e "$CGROUP_PEAK" ]; then
    peak_src=unreadable
  else
    peak_src=absent
  fi

  # presence flag semantics (tsukuroi note): oom_kill is a flag/counter, not a meter to clear
  if [ -n "$service_oom_kill" ] && [ "$service_oom_kill" -gt 0 ] 2>/dev/null; then
    emit_finding CGROUP_OOM_KILL crit "local_oom_kill=$service_oom_kill path=${LOCAL_EVENTS} (local counter: kills in this cgroup only)"
    st=drift
  elif [ "$oom_kill" -gt 0 ] 2>/dev/null; then
    emit_finding CGROUP_OOM_KILL_CUMULATIVE info "parent_slice_oom_kill=$oom_kill service_scope_oom_kill=${service_oom_kill:-unavailable} note=cumulative boot counter; attribute the event before treating it as fleet evidence"
  fi

  # r7 disclosure for r2 defect 3: the bare `oom_kill=` above is the PARENT
  # cumulative counter; the session-service reading that can actually name a
  # fleet kill is now printed next to it instead of living only inside finding
  # text.
  local fill_field
  if [ -n "$fill_pct" ]; then
    fill_field="mem_fill_pct=$fill_pct mem_fill_scope=cgroup"
  elif [ "$fill_scope" = host-ram ] && [ -n "$avail_pct" ]; then
    fill_field="mem_fill_pct=unavailable mem_fill_scope=host-ram host_mem_avail_pct=$avail_pct"
  else
    fill_field="mem_fill_pct=unavailable mem_fill_scope=unavailable"
  fi
  emit_surface cgroup "$st" "cmd=$cmd; oom_kill=$oom_kill oom=${oom:-?} high=${high:-?} max=${max:-?} current=${cur:-?}; local_oom_kill=${service_oom_kill:-unavailable} psi_some_avg10=${psi_some:-unavailable} psi_full_avg10=${psi_full:-unavailable} psi_source=$psi_state psi_warn_avg10=$MEM_PSI_WARN_AVG10 $fill_field mem_peak=${peak:-unavailable} mem_peak_source=$peak_src mem_peak_anchor=${peak_anchor:-unavailable}; ts=$TS_UTC"
}

# ---- surface: disk runway ---------------------------------------------------
# r7 write-rate helpers. The r2 note required a MEASURED write rate before any
# threshold could be revisited for disk; /proc/diskstats holds per-boot
# counters, so the only rate derivable without a sampling interval is the
# AVERAGE SINCE BOOT — reported with that name and never as an instantaneous
# rate. No sampling interval is added to census runtime (bounded deferral
# recorded in the header block).
dev_of() { # <df source> -> device basename (dm-0, nvme0n1p2) or empty
  local src=$1 real
  case "$src" in /dev/*) ;; *) return 0 ;; esac
  real=$(readlink -f -- "$src" 2>/dev/null || printf '%s' "$src")
  printf '%s' "${real#/dev/}"
}

io_of() { # <devname> -> "<rate>Bps" or "unavailable:<reason>"; reads up_s
  local dev=$1 line sectors
  if [ -z "${up_s:-}" ]; then printf 'unavailable:no-uptime'; return 0; fi
  if [ ! -r "$DISKSTATS" ]; then printf 'unavailable:no-diskstats'; return 0; fi
  cap awk -v d="$dev" 'NF >= 10 && $3 == d { print; exit }' "$DISKSTATS"
  if [ "$CAP_RC" -ne 0 ]; then printf 'unavailable:diskstats-rc%s' "$CAP_RC"; return 0; fi
  line=$CAP_OUT
  if [ -z "$line" ]; then printf 'unavailable:device-not-in-diskstats'; return 0; fi
  # field 10 of a diskstats line = sectors written (field 8 is writes completed);
  # 512 bytes per sector is the counter's unit, not an assumption about the
  # device's physical sector size. The `|| true` is the pipefail lesson applied
  # to a new pipeline: a failed extraction must grade `counter-parse`, never
  # abort the gate under `set -e` (the r3 crash class).
  sectors=$(printf '%s\n' "$line" | awk '{print $10}' || true)
  if ! is_int "$sectors"; then printf 'unavailable:counter-parse'; return 0; fi
  printf '%sBps' "$((sectors * 512 / up_s))"
}

probe_disk() {
  local cmd="$DF_BIN -P"
  local st=ok t line fs size used avail pctp pct target_found=0
  local up_s='' up_raw dev io_val io_meas='' io_unmeas=''

  if ! have "$DF_BIN" && [ ! -x "$DF_BIN" ]; then
    emit_surface disk unavailable "cmd=$cmd; df=missing; ts=$TS_UTC"
    return 0
  fi

  up_raw=$(read_file "$UPTIME_FILE"); up_raw=${up_raw%% *}; up_raw=${up_raw%%.*}
  if is_int "$up_raw" && [ "$up_raw" -gt 0 ]; then up_s=$up_raw; fi

  for t in $DISK_TARGETS; do
    if [ ! -e "$t" ]; then
      emit_finding DISK_UNAVAILABLE info "target_absent path=$t"
      continue
    fi
    target_found=1
    cap "$DF_BIN" -P "$t"
    if [ "$CAP_RC" -ne 0 ]; then
      emit_finding DISK_UNAVAILABLE info "df_failed path=$t rc=$CAP_RC"
      continue
    fi
    # second line of df -P
    line=$(printf '%s\n' "$CAP_OUT" | awk 'NR==2 {print}')
    if [ -z "$line" ]; then
      emit_finding DISK_UNAVAILABLE info "df_empty path=$t"
      continue
    fi
    fs=$(printf '%s\n' "$line" | awk '{print $1}')
    size=$(printf '%s\n' "$line" | awk '{print $2}')
    used=$(printf '%s\n' "$line" | awk '{print $3}')
    avail=$(printf '%s\n' "$line" | awk '{print $4}')
    pctp=$(printf '%s\n' "$line" | awk '{print $5}')
    pct=${pctp%%%}
    if [ -z "$pct" ] || ! [ "$pct" -eq "$pct" ] 2>/dev/null; then
      emit_finding DISK_UNAVAILABLE info "df_parse path=$t line=$line"
      continue
    fi
    if [ "$pct" -ge "$DISK_CRIT_PCT" ]; then
      emit_finding DISK_CRITICAL crit "path=$t fs=$fs size=$size used=$used avail=$avail used_pct=$pct threshold=$DISK_CRIT_PCT"
      st=drift
    elif [ "$pct" -ge "$DISK_WARN_PCT" ]; then
      emit_finding DISK_LOW warn "path=$t fs=$fs size=$size used=$used avail=$avail used_pct=$pct threshold=$DISK_WARN_PCT"
      st=drift
    fi
    # r7: write rate for this target's device. A tmpfs/overlay target has no
    # diskstats entry at all, and that is disclosed as a reason, not as 0 B/s.
    dev=$(dev_of "$fs")
    if [ -z "$dev" ]; then
      io_unmeas="${io_unmeas:+$io_unmeas }${fs:-unknown-source}:not-a-block-device"
    else
      io_val=$(io_of "$dev")
      case "$io_val" in
        # The divisor travels WITH the rate (`<dev>:<rate>Bps/<up>s`) rather than
        # as a field of its own. Measured reason: a standalone `io_up_s=` read
        # from /proc/uptime made two runs of the SAME fixture differ by a second
        # and the oracle's shape-invariance case (byte-compare of normalized
        # stdout) failed intermittently — a live-varying value must not appear
        # when no fixture-driven rate was measured.
        *Bps) io_meas="${io_meas:+$io_meas }$dev:$io_val/${up_s}s" ;;
        unavailable:*) io_unmeas="${io_unmeas:+$io_unmeas }$dev:${io_val#unavailable:}" ;;
        *) io_unmeas="${io_unmeas:+$io_unmeas }$dev:unknown" ;;
      esac
    fi
  done

  # A measured-nothing disclosure: when no target device yielded a rate, the
  # row would otherwise read as if the probe simply had nothing to say.
  if [ "$target_found" -eq 1 ] && [ -z "$io_meas" ]; then
    emit_finding DISK_IO_UNMEASURED info "no target device yielded a since-boot write average unmeasured=${io_unmeas:-none} basis=since-boot"
  fi

  if [ "$target_found" -eq 0 ]; then
    emit_surface disk unavailable "cmd=$cmd; targets=$DISK_TARGETS; none present; ts=$TS_UTC"
  else
    emit_surface disk "$st" "cmd=$cmd; targets=$DISK_TARGETS; warn_pct=$DISK_WARN_PCT crit_pct=$DISK_CRIT_PCT; io_basis=since-boot io_avg_since_boot=${io_meas:-none} io_avg_unavailable=${io_unmeas:-none}; ts=$TS_UTC"
  fi
}

# ---- surface: lane silence (r2: launch-aware, authorship-aware) -------------
# Authority: PROTOCOL.md:153-168. Contract: corpus/knowledge/silence-grading-r2.md.
# Decision rows, first match wins:
#   1 unavailable  ledger unreadable, repo absent, git rc!=0, tree unreadable,
#                  launch ts unparseable
#   2 not-open     no launch/steer line for the lane
#   3 young        launch epoch in the future
#   4 closed       a later same-round complete/wrap line (no grade)
#   6 closed       report at HEAD, newest path commit ct in (launch, NOW]
#   7 not-open     .ufo/state/<lane>.round advanced past the anchor round
#   8 young        age_s <= LANE_SILENCE_S (only age > gate is gradeable-old)
#   9 authorship   A progressing (exact subject-authored commit in (launch, NOW])
#                  B progressing (untracked/dirty file newer than the anchor;
#                    attribution inference, disclosed on the row)
#                  C progressing-weak (other-authored commits only)
#                  D silent — the ONLY LANE_SILENT emission
# Ledger grammar (live-measured): "<ISO-8601+offset> launch <lane> round=<N>
# <tail>" where <tail> is pid=|runId=|mission= or absent; legacy "<ISO> steer
# <lane> -> round <N>"; closes "<ISO> complete|wrap <lane> round=<N>...". Tails
# are ignored; 'launch' outranks the legacy 'steer'; the LAST matching line in
# file order wins (the clock is not the tie-breaker); launch-fail and
# lane-round-failed never start a mission. Epoch = first parseable timestamp
# token (field 1; the synthetic "ts=<epoch>" form is accepted as a fallback).
# Identity: exact "%an <%ae>" line "<lane>-shokunin <lane>@shokunin.local>"
# (never %cn/%ce, never a substring, never read from repo config).
# Scope: a child lane scans its own repo; the main-repo lanes (protocol,
# aggregator) scan the fleet root minus nested *-shokunin/** checkouts and
# .ufo/** driver churn — .ufo/reports/** stays, it is the lane's own deliverable
# path, not churn. Row A drops .ufo entirely (a committed report is graded by
# row 6, not as progress); row B keeps .ufo/reports/**.
# unavailable != unhealthy: only row D flips the roll.
lane_repo() {
  case "$1" in
    protocol|aggregator) printf '%s' "$ROOT" ;;
    *) printf '%s/%s-shokunin' "$ROOT" "$1" ;;
  esac
}

is_root_lane() { case "$1" in protocol|aggregator) return 0 ;; *) return 1 ;; esac; }
is_int() { case "${1:-}" in ''|*[!0-9]*) return 1 ;; *) return 0 ;; esac; }

in_lane_scope() { # <lane> <repo-relative path>
  local lane=$1 path=$2
  is_root_lane "$lane" || return 0
  case "$path" in
    *-shokunin/*) return 1 ;;
    .ufo/reports/*) return 0 ;;
    .ufo|.ufo/*) return 1 ;;
  esac
  return 0
}

iso_to_epoch() { # <iso-8601+offset> -> epoch, empty when unparseable
  local out
  if ! out=$(date -u -d "$1" +%s 2>/dev/null); then out=''; fi
  printf '%s' "$out"
}

ledger_ts_fallback() { # <ledger line> -> epoch from a "ts=<epoch>" token, else empty
  local tok v
  for tok in $1; do
    case "$tok" in
      ts=*)
        v=${tok#ts=}
        if is_int "$v"; then printf '%s' "$v"; return 0; fi
        ;;
    esac
  done
  printf ''
}

# ledger_anchor <lane>: one pass over the ledger;
#   sets LA_LINE LA_EPOCH LA_ROUND LA_CLOSED (LA_LINE=0 = no start line at all)
ledger_anchor() {
  local lane=$1 n=0 line f1 f2 f3 f4 f5 f6 rest ep round
  local l_ln=0 l_ep='' l_round='' s_ln=0 s_ep='' s_round=''
  # r4: closes are remembered as "<line> <round>" pairs, one per close line, so
  # the anchor round's own later close can be found after the pass (the r3 code
  # kept only the LAST close line anywhere — see the complete|wrap arm).
  local close_pairs='' cl cr
  LA_LINE=0; LA_EPOCH=''; LA_ROUND=''; LA_CLOSED=0
  while IFS= read -r line; do
    n=$((n + 1))
    line=${line%$'\r'}
    # Candidate ledger lines: the live grammar's field 1 is an ISO-8601 token, so
    # the line starts with a digit; the superseded synthetic grammar prefixes a
    # "TIMESTAMP" token and carries the epoch in "ts=<epoch>", accepted here so
    # that fallback is reachable at all.
    case "$line" in
      [0-9]*T*) ;;
      *' ts='[0-9]*) ;;
      *) continue ;;
    esac
    read -r f1 f2 f3 f4 f5 f6 rest <<< "$line" || true
    case "$f2" in
      launch)
        [ "$f3" = "$lane" ] || continue
        case "$f4" in round=*) ;; *) continue ;; esac
        round=${f4#round=}; round=${round%%;*}
        ep=$(iso_to_epoch "$f1")
        if [ -z "$ep" ]; then ep=$(ledger_ts_fallback "$line"); fi
        l_ln=$n; l_ep=$ep; l_round=$round
        ;;
      steer)
        [ "$f3" = "$lane" ] || continue
        [ "$f4" = '->' ] || continue
        [ "$f5" = round ] || continue
        ep=$(iso_to_epoch "$f1")
        if [ -z "$ep" ]; then ep=$(ledger_ts_fallback "$line"); fi
        s_ln=$n; s_ep=$ep; s_round=$f6
        ;;
      complete|wrap)
        [ "$f3" = "$lane" ] || continue
        case "$f4" in round=*) ;; *) continue ;; esac
        round=${f4#round=}; round=${round%%;*}
        # r4: keyed per round, not "last close anywhere". Measured misgrade at
        # fe22a14f: `complete <lane> round=7` followed by `complete <lane>
        # round=5` erased the r7 close and graded the closed r7 anchor silent.
        close_pairs="$close_pairs$n $round"$'\n'
        ;;
    esac
  done <<< "$LEDGER"
  if [ "$l_ln" -gt 0 ]; then
    LA_LINE=$l_ln; LA_EPOCH=$l_ep; LA_ROUND=$l_round
  elif [ "$s_ln" -gt 0 ]; then
    LA_LINE=$s_ln; LA_EPOCH=$s_ep; LA_ROUND=$s_round
  fi
  # r4: the anchor is closed only by a close line for the ANCHOR ROUND that is
  # later in file order than the anchor launch. Any such close qualifies (the
  # last one for the round is also the latest), and closes for other rounds are
  # irrelevant — whether they sit before or after this anchor.
  if [ "$LA_LINE" -gt 0 ] && [ -n "$close_pairs" ]; then
    while read -r cl cr; do
      [ -n "$cl" ] || continue
      if [ "$cl" -gt "$LA_LINE" ] && [ "$cr" = "$LA_ROUND" ]; then
        LA_CLOSED=1
        break
      fi
    done <<< "$close_pairs"
  fi
}

# Tree readability gate: an unreadable subtree grades unavailable, it must never
# abort the run. r1's `find | sort | tail | cut` command substitution did abort
# here: the nonzero pipeline rc (pipefail) tripped `set -e` and killed the census
# before any verdict (measured with the unreadable-.git fixture; harness case 9).
ps_walk() { # <lane> <repo> -> PS_WALK_RC
  local lane=$1 repo=$2
  if is_root_lane "$lane"; then
    cap find "$repo" -path '*/.git' -prune -o -name '*-shokunin' -prune -o -type d -printf ''
  else
    cap find "$repo" -path '*/.git' -prune -o -type d -printf ''
  fi
  PS_WALK_RC=$CAP_RC
}

# Row 6: report present at HEAD AND newest commit touching it in (launch, NOW].
# The report path is repo-relative to the fleet root for every lane
# (PROTOCOL.md:137; driver report_of()), and best-effort: an unreadable report
# repo does not make a lane unavailable (the lane's own repo is the primary
# evidence source).
ps_report_closed() { # <lane> <round> <launch_epoch> -> rc 0 = closed
  local lane=$1 round=$2 launch=$3
  local rpath=".ufo/reports/round-$round/$lane.md" ct
  cap env GIT_OPTIONAL_LOCKS=0 "$GIT_BIN" -C "$ROOT" cat-file -e "HEAD:$rpath"
  [ "$CAP_RC" -eq 0 ] || return 1
  cap env GIT_OPTIONAL_LOCKS=0 "$GIT_BIN" -C "$ROOT" log -1 --format=%ct -- "$rpath"
  [ "$CAP_RC" -eq 0 ] || return 1
  ct=${CAP_OUT%%$'\n'*}
  ct=${ct//[[:space:]]/}
  is_int "$ct" || return 1
  [ "$ct" -gt "$launch" ] || return 1
  [ "$ct" -le "$NOW_EPOCH" ] || return 1
  return 0
}

# grade_lane <lane>: sets GL_STATE GL_ROUND GL_LAUNCH GL_AGE GL_BASIS GL_EXTRA
grade_lane() {
  local lane=$1 repo
  repo=$(lane_repo "$lane")
  GL_STATE=''; GL_ROUND='-'; GL_LAUNCH='-'; GL_AGE='-'; GL_BASIS=''; GL_EXTRA=''

  # -- row 1: unreadable inputs ------------------------------------------------
  if [ ! -r "$TIMELINE_FILE" ]; then
    GL_STATE=unavailable; GL_BASIS='row-1'
    GL_EXTRA="reason=ledger-unreadable path=$TIMELINE_FILE"
    return 0
  fi
  if [ ! -d "$repo" ]; then
    GL_STATE=unavailable; GL_BASIS='row-1'
    GL_EXTRA="reason=repo-absent repo=$repo"
    return 0
  fi
  cap env GIT_OPTIONAL_LOCKS=0 "$GIT_BIN" -C "$repo" rev-parse --git-dir
  if [ "$CAP_RC" -ne 0 ]; then
    GL_STATE=unavailable; GL_BASIS='row-1'
    GL_EXTRA="reason=git-unreadable rc=$CAP_RC repo=$repo"
    return 0
  fi
  ps_walk "$lane" "$repo"
  if [ "$PS_WALK_RC" -ne 0 ]; then
    GL_STATE=unavailable; GL_BASIS='row-1'
    GL_EXTRA="reason=tree-unreadable rc=$PS_WALK_RC repo=$repo"
    return 0
  fi

  # -- rows 2-8: launch anchor, closure, age ----------------------------------
  ledger_anchor "$lane"
  if [ "$LA_LINE" -eq 0 ]; then
    GL_STATE=not-open; GL_BASIS='row-2'; GL_EXTRA='reason=no-launch-line'
    return 0
  fi
  if ! is_int "$LA_EPOCH"; then
    GL_STATE=unavailable; GL_BASIS='row-1'; GL_EXTRA='reason=launch-ts-unparseable'
    return 0
  fi
  GL_ROUND=$LA_ROUND; GL_LAUNCH=$LA_EPOCH
  if [ "$LA_EPOCH" -gt "$NOW_EPOCH" ]; then
    GL_STATE=young; GL_BASIS='row-3'; GL_EXTRA='reason=launch-in-future'
    return 0
  fi
  if [ "$LA_CLOSED" -eq 1 ]; then
    GL_STATE=not-open; GL_BASIS='row-4'
    GL_EXTRA="reason=ledger-close round=$LA_ROUND"
    return 0
  fi
  local round_state
  round_state=$(read_file "$STATE_DIR/$lane.round")
  if is_int "$round_state" && is_int "$LA_ROUND" && [ "$round_state" -gt "$LA_ROUND" ]; then
    GL_STATE=not-open; GL_BASIS='row-7'
    GL_EXTRA="reason=round-advanced state_round=$round_state anchor_round=$LA_ROUND"
    return 0
  fi
  local age=$((NOW_EPOCH - LA_EPOCH))
  GL_AGE=$age
  if [ "$age" -le "$LANE_SILENCE_S" ]; then
    GL_STATE=young; GL_BASIS='row-8'; GL_EXTRA="reason=age_le_gate gate_s=$LANE_SILENCE_S"
    return 0
  fi

  # -- facts shared by rows 6 and 9 --------------------------------------------
  cap env GIT_OPTIONAL_LOCKS=0 "$GIT_BIN" -c core.quotePath=false -C "$repo" ls-files -mo --exclude-standard
  if [ "$CAP_RC" -ne 0 ]; then
    GL_STATE=unavailable; GL_BASIS='row-1'
    GL_EXTRA="reason=git-ls-files-error rc=$CAP_RC repo=$repo"
    return 0
  fi
  local lsm=$CAP_OUT

  if ps_report_closed "$lane" "$LA_ROUND" "$LA_EPOCH"; then
    GL_STATE=not-open; GL_BASIS='row-6'
    GL_EXTRA="reason=committed-report round=$LA_ROUND path=.ufo/reports/round-$LA_ROUND/$lane.md"
    return 0
  fi

  # -- row 9: authorship -------------------------------------------------------
  local has_head=0 subj=0 sib=0 sibn=0 n_rowb=0 example='' path mt inwin
  cap env GIT_OPTIONAL_LOCKS=0 "$GIT_BIN" -C "$repo" rev-parse --verify -q HEAD
  if [ "$CAP_RC" -eq 0 ]; then
    has_head=1
    local lg_args=(--since="@$LA_EPOCH" --format='%ct %an <%ae>')
    # Rows A/C scan all post-launch commits (a subject commit hidden behind a
    # later sibling HEAD still counts). The pathspecs bind the main-repo lanes to
    # the root's own scope; a child lane's repo is the lane scope entire.
    if is_root_lane "$lane"; then
      lg_args+=(-- . ':(exclude).ufo' ':(exclude,glob)**/*-shokunin/**')
    fi
    cap env GIT_OPTIONAL_LOCKS=0 "$GIT_BIN" -C "$repo" log "${lg_args[@]}"
    if [ "$CAP_RC" -ne 0 ]; then
      GL_STATE=unavailable; GL_BASIS='row-1'
      GL_EXTRA="reason=git-log-error rc=$CAP_RC repo=$repo"
      return 0
    fi
    # --since is committer-date based and inclusive at equality (measured on git
    # 2.55.0), so the strict window (launch, NOW] is applied by an explicit %ct
    # comparison here — that is what keeps a commit at ct == launch out of both
    # attribution and closure.
    inwin=$(printf '%s\n' "$CAP_OUT" | awk -v lo="$LA_EPOCH" -v hi="$NOW_EPOCH" \
      '$1 ~ /^[0-9]+$/ && $1+0 > lo+0 && $1+0 <= hi+0 { print }')
    if [ -n "$inwin" ]; then
      sibn=$(printf '%s\n' "$inwin" | awk 'END { print NR }')
      if printf '%s\n' "$inwin" | sed -E 's/^[0-9]+ //' | grep -Fxq -- "$lane-shokunin <$lane@shokunin.local>"; then
        subj=1
      else
        sib=1
      fi
    fi
  fi

  if [ "$subj" -eq 1 ]; then
    GL_STATE=progressing; GL_BASIS='row-A'
    GL_EXTRA='subject_commits=yes window=launch..NOW'
    return 0
  fi

  # Row B: untracked or dirty files newer than the anchor. Only paths git already
  # flags are examined, so a clean tracked file can never be promoted (the
  # spec's named falsifier); ignored trees never enter (`--exclude-standard`).
  if [ -n "$lsm" ]; then
    while IFS= read -r path; do
      [ -n "$path" ] || continue
      in_lane_scope "$lane" "$path" || continue
      mt=$(epoch_mtime "$repo/$path")
      is_int "$mt" || continue
      if [ "$mt" -gt "$LA_EPOCH" ]; then
        n_rowb=$((n_rowb + 1))
        [ -n "$example" ] || example=$path
      fi
    done <<< "$lsm"
  fi
  if [ "$n_rowb" -gt 0 ]; then
    GL_STATE=progressing; GL_BASIS='row-B'
    GL_EXTRA="rowb_files=$n_rowb attribution=inference example=$example"
    return 0
  fi

  if [ "$sib" -eq 1 ]; then
    GL_STATE=progressing-weak; GL_BASIS='row-C'
    GL_EXTRA="other_authored_commits=$sibn"
    return 0
  fi
  GL_STATE=silent; GL_BASIS='row-D'
  GL_EXTRA="no_subject_commits=yes no_other_commits=yes no_fresh_files=yes has_head=$has_head"
}

probe_silence() {
  local cmd="git -C <repo> log --since=@<launch> --format='%ct %an <%ae>'; git -C <repo> ls-files -mo; git -C <root> cat-file -e HEAD:.ufo/reports/round-<N>/<lane>.md"
  local st=ok lane n_silent=0 n_prog=0 n_weak=0 n_young=0 n_notopen=0 n_unavail=0 n_lanes=0
  resolve_roster
  if [ -r "$TIMELINE_FILE" ]; then
    LEDGER=$(cat -- "$TIMELINE_FILE" 2>/dev/null || true)
  else
    LEDGER=''
  fi

  for lane in $ROSTER_LANES; do
    n_lanes=$((n_lanes + 1))
    grade_lane "$lane"
    case "$GL_STATE" in
      silent)
        n_silent=$((n_silent + 1)); st=drift
        emit_finding LANE_SILENT warn "lane=$lane round=${GL_ROUND} launch_epoch=${GL_LAUNCH} age_s=${GL_AGE} gate_s=$LANE_SILENCE_S basis=row-D"
        ;;
      progressing) n_prog=$((n_prog + 1)) ;;
      progressing-weak) n_weak=$((n_weak + 1)) ;;
      young) n_young=$((n_young + 1)) ;;
      not-open) n_notopen=$((n_notopen + 1)) ;;
      unavailable) n_unavail=$((n_unavail + 1)) ;;
    esac
    # The per-lane row is the state the scenario driver reads; it is not counted
    # as an extra surface (surfaces=N stays the surface list).
    SURFACE_LINES+=("SURFACE lane.$lane: $GL_STATE (lane=$lane round=${GL_ROUND} launch_epoch=${GL_LAUNCH} age_s=${GL_AGE} basis=${GL_BASIS} ${GL_EXTRA}; ts=$TS_UTC)")
  done

  # A missing surface is unavailable, never unhealthy; only row D flips the roll.
  if [ "$n_silent" -eq 0 ] && [ "$n_lanes" -gt 0 ] && [ "$n_unavail" -eq "$n_lanes" ]; then
    st=unavailable
  fi
  emit_surface silence "$st" "cmd=$cmd; roster_source=$ROSTER_SOURCE roster_n=$ROSTER_N conf_n=$CONF_N state_n=$STATE_N conf_dropped_n=$CONF_DROPPED_N state_dropped_n=$STATE_DROPPED_N; silent=$n_silent progressing=$n_prog progressing_weak=$n_weak young=$n_young not_open=$n_notopen unavailable=$n_unavail skipped=0 window_s=$LANE_SILENCE_S; ts=$TS_UTC"
}

# ---- surface: tmux (optional) -----------------------------------------------
# r7 relevance classification (r2 note §7 Gaps: "sessions=1 cannot distinguish a
# fleet session from any other tmux server"). Rule, receipt-backed by the
# fleet's own pane record (read-only, in the fleet root):
#   .ufo/interactive-l1-20261015T050057Z/interactive-panes.json
#   schema shokunin-interactive-panes-v1, tmuxSession ufo_sighting, every lane
#   pane cwd under <root>/<lane>-shokunin
# so: a session is fleet-RELEVANT iff at least one of its panes has a current
# path equal to or under MORI_TMUX_SCOPE_ROOT (default the fleet root), and
# FOREIGN otherwise. Boundary, disclosed on the row: the rule is path-based, so
# a fleet worker whose pane cwd sits outside the fleet root is reported foreign;
# a session with no readable pane line is neither (relevance=unavailable).
probe_tmux() {
  local cmd="$TMUX_BIN ls"
  if ! have "$TMUX_BIN" && [ ! -x "$TMUX_BIN" ]; then
    emit_surface tmux unavailable "cmd=$cmd; tmux=missing; ts=$TS_UTC"
    return 0
  fi
  cap "$TMUX_BIN" ls
  # rc 1 often means no server — unavailable, not drift
  if [ "$CAP_RC" -ne 0 ]; then
    emit_surface tmux unavailable "cmd=$cmd; rc=$CAP_RC; ts=$TS_UTC"
    return 0
  fi
  local n rel=ok reason='' n_fleet=0 n_foreign=0 n_unclass=0
  local fmt line sess path
  local fresh_state=ok fresh_reason='' n_probed=0 n_idle=0 n_fresh_unavail=0
  n=$(printf '%s\n' "$CAP_OUT" | grep -c . || true)

  declare -A SESS_CLASS=()
  # r8: fleet sessions in PANE-ORDER (deduplicated by the classification below).
  # The freshness probe walks this list, so its findings cannot depend on bash's
  # hash iteration order (the r7 foreign loop still uses the map's order; the
  # list is only for the new probe).
  declare -a FLEET_SESS=()
  fmt=$'#{session_name}\t#{pane_current_path}'
  cap "$TMUX_BIN" list-panes -a -F "$fmt"
  if [ "$CAP_RC" -ne 0 ]; then
    rel=unavailable; reason="panes-rc=$CAP_RC"
  else
    while IFS= read -r line; do
      [ -n "$line" ] || continue
      # Pane lines are tab-separated by the format above; anything else (a bare
      # `tmux ls` table from a stub, a truncated line) is not pane data and is
      # not guessed at.
      case "$line" in *$'\t'*) ;; *) continue ;; esac
      sess=${line%%$'\t'*}; path=${line#*$'\t'}
      [ -n "$sess" ] || continue
      # One fleet pane is enough for the whole session; a foreign pane never
      # demotes a session already marked fleet.
      case "$path" in
        "$TMUX_SCOPE_ROOT"|"$TMUX_SCOPE_ROOT"/*)
          if [ "${SESS_CLASS[$sess]:-}" != fleet ]; then
            SESS_CLASS[$sess]=fleet
            FLEET_SESS+=("$sess")
          fi ;;
        *) if [ "${SESS_CLASS[$sess]:-}" != fleet ]; then SESS_CLASS[$sess]=foreign; fi ;;
      esac
    done <<< "$CAP_OUT"
    if [ "${#SESS_CLASS[@]}" -eq 0 ]; then
      rel=unavailable; reason=no-pane-data
    else
      for sess in "${!SESS_CLASS[@]}"; do
        case "${SESS_CLASS[$sess]}" in
          fleet) n_fleet=$((n_fleet + 1)) ;;
          *) n_foreign=$((n_foreign + 1))
             emit_finding TMUX_FOREIGN_SESSION info "session=$sess relevance=foreign rule=pane_cwd_under_fleet_root scope_root=$TMUX_SCOPE_ROOT" ;;
        esac
      done
      if [ "$n" -gt "$((n_fleet + n_foreign))" ] 2>/dev/null; then
        n_unclass=$((n - n_fleet - n_foreign))
      fi
    fi
  fi

  # ---- r8: per-session freshness (the residual r7 left unmeasured) ------------
  # The r7 row named the sessions but said nothing about whether a fleet session
  # is alive or has gone quiet; surfaces-r7.md §1(b) names that as the remaining
  # measurement. For every session classified fleet (only those — a foreign
  # session's idle time is not fleet evidence), ask the server for the session's
  # own activity timestamp: ONE `display-message -p -t <session>` per session,
  # wrapped in run_timeout so a wedged server can never hang the gate. Idle is
  # NOW - session_activity, and only an INFO finding can result: a quiet pane is
  # evidence, not proof (a long-running worker writes no output, and tmux updates
  # session_activity on the server's own events), so the local threshold must not
  # flip the roll. rc from the bound, non-integer output from a broken/stub
  # server, and a missing `timeout` binary each grade unavailable with a reason —
  # never an idle=0 guess.
  if [ "$rel" = ok ] && [ "$n_fleet" -gt 0 ]; then
    if ! have "$TIMEOUT_BIN" && [ ! -x "$TIMEOUT_BIN" ]; then
      fresh_state=unavailable; fresh_reason=no-timeout-bin
      n_fresh_unavail=$n_fleet
      emit_finding TMUX_FRESHNESS_UNAVAILABLE info "reason=no-timeout-bin sessions=$n_fleet timeout_bin=$TIMEOUT_BIN unbounded_probe_refused"
    else
      local act idle
      for sess in "${FLEET_SESS[@]+"${FLEET_SESS[@]}"}"; do
        run_timeout "$TMUX_TIMEOUT_S" "$TMUX_BIN" display-message -p -t "$sess" '#{session_activity}'
        act=$CAP_OUT; act=${act//[[:space:]]/}
        if [ "$CAP_RC" -ne 0 ]; then
          n_fresh_unavail=$((n_fresh_unavail + 1))
          fresh_reason="rc-$CAP_RC"
          emit_finding TMUX_FRESHNESS_UNAVAILABLE info "session=$sess reason=rc-$CAP_RC timeout_s=$TMUX_TIMEOUT_S probe=display-message"
          continue
        fi
        if ! is_int "$act"; then
          n_fresh_unavail=$((n_fresh_unavail + 1))
          fresh_reason=unparseable
          emit_finding TMUX_FRESHNESS_UNAVAILABLE info "session=$sess reason=unparseable-probe-output timeout_s=$TMUX_TIMEOUT_S probe=display-message"
          continue
        fi
        n_probed=$((n_probed + 1))
        idle=$((NOW_EPOCH - act))
        [ "$idle" -ge 0 ] || idle=0
        if [ "$idle" -gt "$TMUX_IDLE_WARN_S" ]; then
          n_idle=$((n_idle + 1))
          emit_finding TMUX_SESSION_IDLE info "session=$sess idle_s=$idle threshold_s=$TMUX_IDLE_WARN_S threshold_label=local basis=session_activity"
        fi
      done
      if [ "$n_fresh_unavail" -gt 0 ]; then
        fresh_state=unavailable
        # Several sessions: some measured, some not. The row must not claim the
        # last failure as the whole reason — `mixed` says "at least one relevant
        # session could not be measured", and the per-session findings above name
        # each failure.
        [ "$n_probed" -eq 0 ] || fresh_reason=mixed
      fi
    fi
  else
    fresh_state=unavailable
    if [ "$rel" = unavailable ]; then fresh_reason=relevance-unavailable; else fresh_reason=no-relevant-sessions; fi
  fi

  if [ "$rel" = unavailable ]; then
    # Sessions were counted but not classified: disclose instead of implying a
    # classification that was never made.
    emit_finding TMUX_RELEVANCE_UNAVAILABLE info "session relevance unreadable reason=$reason probe=$TMUX_BIN list-panes -a sessions=$n unnoticed_but_counted"
    emit_surface tmux ok "cmd=$cmd; sessions=$n; relevance=unavailable reason=$reason rule=pane_cwd_under_fleet_root freshness=unavailable reason=$fresh_reason; ts=$TS_UTC"
  else
    emit_surface tmux ok "cmd=$cmd; sessions=$n; relevant=$n_fleet foreign=$n_foreign unclassified=$n_unclass rule=pane_cwd_under_fleet_root freshness=$fresh_state probed=$n_probed idle=$n_idle freshness_unavailable=$n_fresh_unavail idle_warn_s=$TMUX_IDLE_WARN_S${fresh_reason:+ reason=$fresh_reason}; ts=$TS_UTC"
  fi
}

# ---- live run ---------------------------------------------------------------
run_census() {
  local mode=${1:-live}
  printf 'mori-census %s — ts=%s — mode=%s — read-only\n' "$VERSION" "$TS_UTC" "$mode"

  probe_watchdog
  probe_waves
  probe_journal
  probe_cgroup
  probe_disk
  probe_silence
  probe_tmux

  local line
  for line in "${SURFACE_LINES[@]:-}"; do printf '%s\n' "$line"; done
  for line in "${FINDING_LINES[@]:-}"; do printf '%s\n' "$line"; done

  printf 'MORI_CENSUS: %s (findings=%d drift=%d unavailable=%d surfaces=%d)\n' \
    "$ROLL" "$N_FINDINGS" "$N_DRIFT" "$N_UNAVAIL" "$N_SURFACES"

  case "$ROLL" in
    CLEAN) exit 0 ;;
    DRIFT) exit 1 ;;
    *) exit 2 ;;
  esac
}

# ---- drift pin (r10): behavioral baseline + drift check ---------------------
# Contract in the header block above. Design constraints:
#   - NO live pipes in this section: the census output is captured into a
#     variable and normalized by ONE sed pass fed by a here-string (the r9
#     lesson's flake class was a live-piped early-exit consumer, not a reader);
#   - every mask rule is a fixed regex over the emitted grammar, so an edit
#     that changes a key NAME, drops a field, or changes a state word surfaces
#     as drift instead of being silently masked;
#   - the declared VOLATILE list is this check's blind spot BY CONSTRUCTION; it
#     is recorded verbatim in the baseline header so an auditor can see exactly
#     what is masked, and a change to the list itself surfaces as drift on
#     every affected field. Non-volatile fields the check cannot name
#     individually fall back to the line's id (state words, command text).

# Roster source/count fields intentionally remain non-volatile: roster changes
# alter behavior and must be reported by --drift.
# Integer-valued live measurements (counters/gauges/file-presence flags).
# Longest-first where one key is a prefix of another (state_rounds_max before
# state_rounds before state_round; used_pct before used; availability counts
# before the verdict words they shadow).
DRIFT_COUNTER_KEYS=(
  age_unreadable aged_unsettled avail count current disp drift empty findings
  foreign freshness_unavailable has_head high host_mem_avail_pct idle idle_s
  ledger_round local_oom_kill max mem_fill_pct mem_peak not_open
  oom oom_kill other_authored_commits pids probed progressing progressing_weak
  reg relevant round rowb_files run sessions settle settled silent
  size skipped state_ahead state_cmp state_lag state_round state_rounds
  state_rounds_max state_val_unreadable surfaces total unclassified
  unavailable unsettled used used_pct young
  kernel_oom_notice oomd_notice coredump_notice segfault_signal11
  unit_sigkill_record unit_failure_record
  user_unit_oom_result_unknown system_unit_oom_result_unknown
  user_unit_oom system_unit_oom user_notice system_notice
  unit_oom_subject_unknown unit_oom_result_unknown unit_oom_fleet unit_oom_nonfleet
  unit_nonfleet unit_fleet unit_unknown unit_missing unit_ambiguous unit_malformed
  unit_oom unit_signal user_unit_signal process_sigkill
)
# Non-counter volatile entries, each with its own mask rule below.
DRIFT_VOLATILE_SPECIAL='ts age_s mtime_age_s *_epoch mem_peak_anchor psi_some_avg10 psi_full_avg10 io_avg_since_boot state_val_unread_reasons boot script_sha256 example'
DRIFT_VOLATILE_LIST="$DRIFT_VOLATILE_SPECIAL ${DRIFT_COUNTER_KEYS[*]}"

# drift_normalize — stdin: raw census output; stdout: canonical form (volatile
# values replaced by <V>, line order and non-volatile bytes preserved).
drift_normalize() {
  local cre=${DRIFT_COUNTER_KEYS[*]}
  cre=${cre// /|}
  sed -E \
    -e 's/\bstate_val_unread_reasons=file:[0-9]+ symlink:[0-9]+ dir:[0-9]+ other:[0-9]+/state_val_unread_reasons=<V>/g' \
    -e 's/\bmtime_age_s=[0-9]+/mtime_age_s=<V>/g' \
    -e 's/\bts=[^ ;)]*/ts=<V>/g' \
    -e 's/\bage_s=[0-9]+/age_s=<V>/g' \
    -e 's/\b([a-z_]+_epoch)=[0-9]+/\1=<V>/g' \
    -e 's/\bmem_peak_anchor=[0-9]+/mem_peak_anchor=<V>/g' \
    -e 's/\bboot=[^ ;)]*/boot=<V>/g' \
    -e 's/\bpsi_(some|full)_avg10=[0-9.]+/psi_\1_avg10=<V>/g' \
    -e 's/[0-9]+Bps\/[0-9]+s/<V>Bps\/<V>s/g' \
    -e 's/\bscript_sha256=[0-9a-f]+/script_sha256=<V>/g' \
    -e 's/\bexample=[^ ;]*/example=<V>/g' \
    -e "s/\\b(${cre})=[0-9]+/\\1=<V>/g"
}

# cap_census — capture the whole census for pin/drift. run_census ends with
# `exit`, which inside the command substitution ends only that subshell; its rc
# (0/1) is kept in CENSUS_RC. The captured TEXT is the frozen input every
# comparison reads — no consumer ever reads a live pipe (r9 race lesson).
cap_census() {
  set +e
  CENSUS_CAPTURE=$(run_census live 2>&1)
  CENSUS_RC=$?
  set -e
}

# drift_line_id — pairing identity of a canonical line. SURFACE/FINDING keep
# their name/id; the header and the verdict line are singletons. Colon-joined
# so every identity is ONE whitespace-free token.
drift_line_id() {
  local head rest
  case "$1" in
    SURFACE\ *) head=${1%%:*}; printf 'SURFACE:%s' "${head#SURFACE }" ;;
    FINDING\ *) rest=${1#FINDING }; printf 'FINDING:%s' "${rest%% severity=*}" ;;
    MORI_CENSUS:*) printf 'VERDICT' ;;
    mori-census\ *) printf 'HEADER' ;;
    '') printf 'BLANK' ;; # a zero-findings run prints one blank line (pre-existing `"${FINDING_LINES[@]:-}"` expansion); name it instead of an empty `+`
    *) printf '%s' "$1" ;;
  esac
}

# drift_scan <line> — set globals DRIFT_KEYS (first-seen order) and
# DRIFT_KEYVAL (assoc). A token counts as a field only when it is key=value
# with a key-shaped key, so shell text like `-af` or `(cmd=df` contributes
# nothing. A duplicated key's values are concatenated, so one occurrence
# cannot hide behind another. `set -f` keeps a literal glob in command text
# from pathname-expanding mid-scan.
drift_scan() {
  local tok key
  set -f
  DRIFT_KEYS=()
  declare -gA DRIFT_KEYVAL=()
  DRIFT_KEYVAL=()
  for tok in $1; do
    tok=${tok#(}
    tok=${tok%;}
    tok=${tok%)}
    case "$tok" in *=*) ;; *) continue ;; esac
    key=${tok%%=*}
    case "$key" in ''|*[!A-Za-z0-9_]*) continue ;; esac
    [ -n "${DRIFT_KEYVAL[$key]+set}" ] || DRIFT_KEYS+=("$key")
    DRIFT_KEYVAL[$key]="${DRIFT_KEYVAL[$key]:-}${tok#*=}"
  done
  set +f
}

# drift_field_report <base-line> <new-line> <id> — print one changed
# non-volatile field per line (a changed value names its key; a removed/added
# field names -key/+key). A difference that lives outside key=value tokens
# (state word, command text, verdict roll) falls back to the line's id.
drift_field_report() {
  local bl=$1 nl=$2 id=$3 k
  local -a bkeys=() nkeys=() changed=()
  local -A bval=() nval=()
  drift_scan "$bl"
  bkeys=("${DRIFT_KEYS[@]}")
  for k in "${bkeys[@]}"; do bval[$k]=${DRIFT_KEYVAL[$k]}; done
  drift_scan "$nl"
  nkeys=("${DRIFT_KEYS[@]}")
  for k in "${nkeys[@]}"; do nval[$k]=${DRIFT_KEYVAL[$k]}; done
  for k in "${bkeys[@]}"; do
    if [ -z "${nval[$k]+set}" ]; then changed+=("-$k"); continue; fi
    [ "${bval[$k]}" = "${nval[$k]}" ] || changed+=("$k")
  done
  for k in "${nkeys[@]}"; do
    [ -n "${bval[$k]+set}" ] || changed+=("+$k")
  done
  if [ "${#changed[@]}" -eq 0 ]; then changed+=("$id"); fi
  printf '%s\n' "${changed[@]}"
}

# drift_report — globals in: DRIFT_BASE_LINES / DRIFT_NEW_LINES (the two
# canonical line arrays; the joined strings were already compared unequal by
# the caller). Out: DRIFT_REPORT = one space-joined token list naming the
# changed non-volatile fields.
drift_report() {
  DRIFT_REPORT=''
  local -a base_used=() new_used=() rep=()
  local i j id matched fields
  # pass 1 — exact matches (multiset), so a removed/added line is not
  # mispaired with a same-id sibling and mis-reported as a field change.
  for i in "${!DRIFT_BASE_LINES[@]}"; do
    for j in "${!DRIFT_NEW_LINES[@]}"; do
      [ "${new_used[$j]:-0}" = 1 ] && continue
      if [ "${DRIFT_NEW_LINES[$j]}" = "${DRIFT_BASE_LINES[$i]}" ]; then
        base_used[$i]=1; new_used[$j]=1; break
      fi
    done
  done
  # pass 2 — same-id pairing for the remainder: name the changed fields.
  for i in "${!DRIFT_BASE_LINES[@]}"; do
    [ "${base_used[$i]:-0}" = 1 ] && continue
    id=$(drift_line_id "${DRIFT_BASE_LINES[$i]}")
    matched=-1
    for j in "${!DRIFT_NEW_LINES[@]}"; do
      [ "${new_used[$j]:-0}" = 1 ] && continue
      [ "$(drift_line_id "${DRIFT_NEW_LINES[$j]}")" = "$id" ] || continue
      matched=$j; break
    done
    if [ "$matched" -ge 0 ]; then
      new_used[$matched]=1
      fields=$(drift_field_report "${DRIFT_BASE_LINES[$i]}" "${DRIFT_NEW_LINES[$matched]}" "$id")
      while IFS= read -r f; do [ -n "$f" ] && rep+=("$f"); done <<< "$fields"
    else
      rep+=("-$id")
    fi
  done
  # pass 3 — anything left on the new side was added.
  for j in "${!DRIFT_NEW_LINES[@]}"; do
    [ "${new_used[$j]:-0}" = 1 ] && continue
    rep+=("+$(drift_line_id "${DRIFT_NEW_LINES[$j]}")")
  done
  # The joined strings differed, yet no line/field was named: a pure reorder
  # (pass 1 is order-independent). Say so instead of a false 'none'.
  if [ "${#rep[@]}" -eq 0 ]; then rep+=("output-order"); fi
  local joined sorted
  joined=$(printf '%s\n' "${rep[@]}")
  sorted=$(LC_ALL=C sort -u <<< "$joined")
  DRIFT_REPORT=${sorted//$'\n'/ }
}

run_pin() { # <path>
  local path=$1 canon text
  cap_census
  canon=$(drift_normalize <<< "$CENSUS_CAPTURE")
  text=''
  text+='# mori-drift-baseline v1 — written by mori-census.sh --pin'$'\n'
  text+="# census_sha256=$SCRIPT_SHA256"$'\n'
  text+="# pinned_ts=$TS_UTC"$'\n'
  text+="# volatile_fields=$DRIFT_VOLATILE_LIST"$'\n'
  text+='# volatile_note=values of these fields are masked to <V>; --drift re-normalizes with the CURRENT list and reports every changed non-volatile line/field. Changing the list is itself drift; census_sha256 is informational (behavior, not revision, is compared).'$'\n'
  text+='# --- canonical output follows ---'$'\n'
  text+="$canon"$'\n'
  if ! printf '%s' "$text" > "$path" 2>/dev/null; then
    printf 'mori-census: --pin failed to write baseline path=%s\n' "$path" >&2
    exit 2
  fi
  printf 'MORI_PIN: ok path=%s\n' "$path"
  exit 0
}

run_drift() { # <path>
  local path=$1 line marker='# --- canonical output follows ---'
  local in_block=0 have_vol=0 base_str='' canon new_str='' base_vol='' vol_token=''
  local -a base_lines=() new_lines=()
  if [ ! -e "$path" ]; then
    printf 'mori-census: --drift baseline missing: %s\n' "$path" >&2
    exit 2
  fi
  if [ ! -r "$path" ]; then
    printf 'mori-census: --drift baseline unreadable: %s\n' "$path" >&2
    exit 2
  fi
  while IFS= read -r line; do
    line=${line%$'\r'}
    if [ "$in_block" -eq 1 ]; then
      base_lines+=("$line")
      base_str+="$line"$'\n'
    elif [ "$line" = "$marker" ]; then
      in_block=1
    else
      case "$line" in
        '# volatile_fields='*) have_vol=1; base_vol=${line#'# volatile_fields='} ;;
      esac
    fi
  done < "$path"
  if [ "$in_block" -ne 1 ]; then
    printf 'mori-census: --drift baseline malformed (canonical marker absent): %s\n' "$path" >&2
    exit 2
  fi
  if [ "$have_vol" -ne 1 ]; then
    printf 'mori-census: --drift baseline malformed (volatile_fields contract absent): %s\n' "$path" >&2
    exit 2
  fi
  if [ "${#base_lines[@]}" -eq 0 ]; then
    printf 'mori-census: --drift baseline malformed (empty canonical block): %s\n' "$path" >&2
    exit 2
  fi
  # The declared contract is compared too: a baseline pinned under a DIFFERENT
  # volatile list is drifting even when this run's output happens not to
  # exercise the changed mask (the recorded list is the contract, and the
  # comparison makes "changing the list is itself drift" literal).
  if [ "$base_vol" != "$DRIFT_VOLATILE_LIST" ]; then vol_token=volatile_fields; fi

  cap_census
  canon=$(drift_normalize <<< "$CENSUS_CAPTURE")
  while IFS= read -r line; do
    new_lines+=("$line")
    new_str+="$line"$'\n'
  done <<< "$canon"

  if [ "$base_str" = "$new_str" ]; then
    if [ -n "$vol_token" ]; then
      printf 'MORI_DRIFT: %s\n' "$vol_token"
      exit 1
    fi
    printf 'MORI_DRIFT: none\n'
    exit 0
  fi
  DRIFT_BASE_LINES=("${base_lines[@]}")
  DRIFT_NEW_LINES=("${new_lines[@]}")
  drift_report
  printf 'MORI_DRIFT: %s\n' "${DRIFT_REPORT:-none}${vol_token:+ $vol_token}"
  exit 1
}

# ---- hermetic selftest ------------------------------------------------------
run_selftest() {
  local bin FX PASS=0 FAIL=0 OUT_FILE
  # The trap path must NOT be a `local`: the EXIT trap fires after this function
  # returns, when a local is out of scope, so `rm -rf -- "${work:-}"` expanded to
  # `rm -rf -- ''` and every run leaked its temp dir (measured: 45 leftovers).
  # A non-local holder keeps the path visible to the trap.
  MORI_SELFTEST_WORK=$(mktemp -d /tmp/mori-census-selftest.XXXXXX)
  local work="$MORI_SELFTEST_WORK"
  # chmod first: the unreadable-subtree cases (silence tree-unreadable, waves
  # age-unreadable) leave mode-000 dirs behind, and `rm -rf` cannot descend into
  # what it cannot read.
  trap 'chmod -R u+rwX "${MORI_SELFTEST_WORK:-}" 2>/dev/null; rm -rf -- "${MORI_SELFTEST_WORK:-}"' EXIT INT TERM
  bin="$work/bin"
  # r9: the one capture file every harness match greps (see the note at check()).
  OUT_FILE="$work/.last-out"
  mkdir -p "$bin" "$work/fx"

  # dispatcher stubs — answer only from MORI_FIXTURE tree. git is arg-aware: the
  # r2 silence probe asks distinct questions (rev-parse / ls-files / cat-file /
  # `log` for authorship vs `log -1` for the newest report-path commit), so the
  # stub answers per verb from $fx/stub/git-<verb>[.rc]; an absent file answers
  # empty output with rc 0.
  cat > "$bin/.dispatch" <<'STUB'
#!/usr/bin/env bash
set -uo pipefail
name=${0##*/}
fx=${MORI_FIXTURE:-}
[ -n "$fx" ] || { printf 'fixture dispatcher: MORI_FIXTURE unset\n' >&2; exit 97; }
rc_of() { local f="$fx/stub/$1.rc"; if [ -f "$f" ]; then cat "$f"; else printf 0; fi; }
out_of() { local f="$fx/stub/$1"; if [ -f "$f" ]; then cat "$f"; fi; }
case "$name" in
  pgrep)
    out_of pgrep; exit "$(rc_of pgrep)" ;;
  journalctl)
    # r13: the probe asks six structured questions per scope. Answer by
    # scope+class from $fx/stub/journal-<scope>-<class>[.rc]; a missing slot
    # falls back to $fx/stub/journal[.rc] (the quiet baseline is an empty file,
    # i.e. a valid zero). class = kernel_oom | oomd | coredump | unit_sigkill |
    # unit_failure | segfault.
    jscope=system
    jcls=all
    for a in "$@"; do
      case "$a" in
        --user) jscope=user ;;
        --system) jscope=system ;;
        MESSAGE_ID=fe6faa94*) jcls=kernel_oom ;;
        MESSAGE_ID=d989611b*) jcls=oomd ;;
        MESSAGE_ID=fc2e22bc*) jcls=coredump ;;
        MESSAGE_ID=98e32220*) jcls=unit_sigkill ;;
        MESSAGE_ID=d9b373ed*) jcls=unit_failure ;;
        COREDUMP_SIGNAL=11) jcls=segfault ;;
      esac
    done
    jslot="$fx/stub/journal-$jscope-$jcls"
    if [ -f "$jslot" ] || [ -f "$jslot.rc" ] || [ -f "$jslot.err" ]; then
      [ -f "$jslot" ] && cat "$jslot"
      [ -f "$jslot.err" ] && cat "$jslot.err" >&2
      exit "$(rc_of "journal-$jscope-$jcls")"
    fi
    out_of journal; exit "$(rc_of journal)" ;;
  df)
    # ignore args; emit fixture table
    out_of df; exit "$(rc_of df)" ;;
  tmux)
    # r7: the census asks two different questions — `tmux ls` (session count)
    # and `tmux list-panes -a -F ...` (pane cwd for relevance). Answer per
    # subcommand from $fx/stub/tmux[-panes]; an absent file is empty output
    # with rc 0, so the no-pane-data arm is drivable too.
    # r8 adds the third question, `display-message -p -t <sess>
    # #{session_activity}` (per-session freshness), answered from
    # $fx/stub/tmux-activity. `tmux-activity-sleep` makes this stub SLEEP before
    # answering — the hang-guard arm: it exists only under /tmp, is bounded by
    # the census's own run_timeout, and is never pointed at a real tool.
    case " $* " in
      *" list-panes "*) out_of tmux-panes; exit "$(rc_of tmux-panes)" ;;
      *" display-message "*)
        # The sleep is backgrounded with its own stdout/stderr redirected: when
        # the census's bound kills this stub, no orphan may still hold the
        # command-substitution pipe open (that would make the "bounded" probe
        # wait out the sleep anyway and hide a broken bound).
        if [ -f "$fx/stub/tmux-activity-sleep" ]; then sleep "$(cat "$fx/stub/tmux-activity-sleep")" >/dev/null 2>&1 & wait; fi
        out_of tmux-activity; exit "$(rc_of tmux-activity)" ;;
      *) out_of tmux; exit "$(rc_of tmux)" ;;
    esac ;;
  git)
    verb=''
    for a in "$@"; do
      case "$a" in
        rev-parse) verb=rev-parse; break ;;
        ls-files) verb=ls-files; break ;;
        cat-file) verb=cat-file; break ;;
        log)
          case " $* " in *" -1 "*) verb=log1 ;; *) verb=log ;; esac
          break ;;
      esac
    done
    [ -n "$verb" ] || verb=other
    out_of "git-$verb"; exit "$(rc_of "git-$verb")" ;;
esac
printf 'fixture dispatcher: unknown %s\n' "$name" >&2
exit 96
STUB
  chmod 700 "$bin/.dispatch"
  local c
  for c in pgrep journalctl df tmux git; do ln -s .dispatch "$bin/$c"; done

  ok() { PASS=$((PASS + 1)); printf 'PASS %s\n' "$*"; }
  bad() { FAIL=$((FAIL + 1)); printf 'FAIL %s\n' "$*" >&2; }

  # The braces keep a failed walk (an intentionally unreadable fixture subtree)
  # from tripping pipefail inside this command substitution: the hash covers what
  # is readable, in both the before and the after pass.
  fx_hash() { { find "$1" -type f -exec sha256sum {} + 2>/dev/null || true; } | LC_ALL=C sort | sha256sum | cut -d' ' -f1; }
  fx_no_mutation() {
    local d=$1 before=$2 after
    after=$(fx_hash "$d")
    if [ "$after" != "$before" ]; then bad "fixture mutated ($d)"; fi
  }

  # Build a quiet baseline fixture under $1
  fx_quiet() {
    local d=$1 uid=1000
    mkdir -p "$d/ufo/state" "$d/ufo/waves" "$d/stub" \
      "$d/cgroup" "$d/lanes/kagi-shokunin" "$d/root"
    # fresh watchdog log
    printf '2026-10-14T12:00:00Z tick=1\n' > "$d/ufo/watchdog.log"
    # pin mtime to NOW via later touch in check
    printf '1\n' > "$d/ufo/state/kagi.round"
    printf 'mission-x\n' > "$d/ufo/state/kagi.mission"
    # one settled wave
    mkdir -p "$d/ufo/waves/wave-settled"
    printf '{"wave":"wave-settled"}\n' > "$d/ufo/waves/wave-settled/swarm-registry.json"
    printf '{"wave":"wave-settled"}\n' > "$d/ufo/waves/wave-settled/dispatch.json"
    printf '{"schema":"ufo-swarm-results-v1","members":[]}\n' > "$d/ufo/waves/wave-settled/results.json"
    # cgroup quiet
    printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\n' > "$d/cgroup/memory.events"
    printf '123456\n' > "$d/cgroup/memory.current"
    # r7 cgroup siblings: PSI quiet (some/full avg10=0.00) and the unlimited
    # limit token this host's user slice reports, so the baseline drives the
    # host-ram fill arm; MemTotal is present so that arm is provable, not
    # silently unavailable.
    printf 'some avg10=0.00 avg60=0.00 avg300=0.00 total=100\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=50\n' > "$d/cgroup/memory.pressure"
    printf 'max\n' > "$d/cgroup/memory.max"
    printf 'MemTotal: 32000000 kB\nMemAvailable: 20000000 kB\n' > "$d/meminfo"
    # r7 disk-rate fixtures: one diskstats line for the df stub's device and an
    # uptime divisor. sectors written = field 10 = 20000, uptime = 1000 s, so
    # the baseline rate is exactly 20000*512/1000 = 10240 Bps.
    printf '8 0 fx 100 0 1000 0 500 0 20000 0 0 0 0 0 0\n' > "$d/diskstats"
    printf '1000.00 4000.00\n' > "$d/uptime"
    # stubs
    printf '1234 bash /path/scripts/shokunin-watchdog.sh\n' > "$d/stub/pgrep"
    printf 0 > "$d/stub/pgrep.rc"
    : > "$d/stub/journal"; printf 0 > "$d/stub/journal.rc"
    printf 'Filesystem 1024-blocks Used Available Capacity Mounted on\n/dev/fx 1000000 10000 990000 2%% /fx\n' > "$d/stub/df"
    printf 0 > "$d/stub/df.rc"
    printf 'fx_session: 1 windows\n' > "$d/stub/tmux"; printf 0 > "$d/stub/tmux.rc"
    # r7 pane fixture: one session whose pane cwd is the fixture fleet root, so
    # the baseline exercises the relevance rule as fleet-relevant (tab-separated,
    # the format the probe asks tmux for).
    printf 'fx_session\t%s\n' "$d/root" > "$d/stub/tmux-panes"; printf 0 > "$d/stub/tmux-panes.rc"
    # r8 freshness fixture: the pinned epoch, i.e. idle = NOW - activity = 0 for
    # the baseline (a fresh fleet session fires nothing). Cases that want the
    # idle arm rewrite this file with an older epoch; absence of the file means
    # the dispatcher answers empty (the unparseable arm).
    printf '1700000000\n' > "$d/stub/tmux-activity"; printf 0 > "$d/stub/tmux-activity.rc"
    # git answers per verb via stub/git-<verb>[.rc] (see the dispatcher above):
    # rev-parse / ls-files / cat-file / log / log1. Absent fixture files answer
    # empty output with rc 0.
    # lane file recent — touch in check with NOW
    printf 'x\n' > "$d/lanes/kagi-shokunin/LOG.md"
  }

  EXTRA_ENV=()

  # sut_env — the ONE fixture environment every census invocation gets
  # (check() and the r10 pd_run helper). Kept in one place so a pin/drift case
  # can never grade a different environment than the fixture it is compared
  # against; ${PIN_NOW} is read here, so a case changes the pinned clock by
  # setting PIN_NOW before invoking.
  sut_env() {
    SUT_ENV=(
      PATH="$bin:/usr/bin:/bin"
      HOME="$work/home"
      MORI_FIXTURE="$FX"
      MORI_SHOKUNIN_ROOT="$FX/root"
      MORI_UFO_DIR="$FX/ufo"
      MORI_FLEET_CONF="$FX/root/shokunin.conf"
      MORI_WAVES_DIR="$FX/ufo/waves"
      MORI_CGROUP_EVENTS="$FX/cgroup/memory.events"
      MORI_CGROUP_SERVICE_EVENTS="$FX/cgroup/memory.events"
      MORI_CGROUP_LOCAL_EVENTS="$FX/cgroup/memory.events"
      MORI_CGROUP_CURRENT="$FX/cgroup/memory.current"
      MORI_CGROUP_PRESSURE="$FX/cgroup/memory.pressure"
      MORI_CGROUP_MAX="$FX/cgroup/memory.max"
      MORI_MEMINFO="$FX/meminfo"
      MORI_DISKSTATS="$FX/diskstats"
      MORI_UPTIME="$FX/uptime"
      MORI_DF_BIN="$bin/df"
      MORI_PGREP_BIN="$bin/pgrep"
      MORI_JOURNALCTL_BIN="$bin/journalctl"
      MORI_TMUX_BIN="$bin/tmux"
      MORI_GIT_BIN="$bin/git"
      MORI_DISK_TARGETS="$FX/root"
      MORI_ROSTER_LANES="kagi"
      MORI_NOW_EPOCH="${PIN_NOW:-1700000000}"
      MORI_BOOT_ID=0123456789abcdef0123456789abcdef
      MORI_WATCHDOG_STALE_S=900
      MORI_WAVE_UNSETTLED_S=7200
      MORI_DISK_WARN_PCT=85
      MORI_DISK_CRIT_PCT=95
      MORI_LANE_SILENCE_S=7200
    )
  }

  check() { # LABEL WANT_RC WANT_VERDICT [WANT_RE...]
    local label=$1 wrc=$2 wverdict=$3
    shift 3
    local out rc before re miss='' env_now
    env_now=${PIN_NOW:-1700000000}
    # Freshen quiet paths to env_now — UNLESS the case is a staleness proof, which
    # needs the very paths this would refresh to stay old. Without the opt-out a
    # WATCHDOG_STALE / WAVE_UNSETTLED_AGE / LANE_SILENT case can never fire: the
    # harness would hand the gate an age of 0 (measured: 3 red cases, r1 landing).
    if [ "${SKIP_FRESHEN:-0}" != 1 ]; then
      if [ -f "$FX/ufo/watchdog.log" ]; then touch -d "@$env_now" "$FX/ufo/watchdog.log" 2>/dev/null || touch "$FX/ufo/watchdog.log"; fi
      if [ -f "$FX/lanes/kagi-shokunin/LOG.md" ]; then touch -d "@$env_now" "$FX/lanes/kagi-shokunin/LOG.md" 2>/dev/null || true; fi
      if [ -d "$FX/ufo/waves" ]; then find "$FX/ufo/waves" -type f -exec touch -d "@$env_now" {} + 2>/dev/null || true; fi
    fi

    before=$(fx_hash "$FX")
    sut_env
    set +e
    out=$(env -i "${SUT_ENV[@]}" "${EXTRA_ENV[@]+"${EXTRA_ENV[@]}"}" bash "$SELF" 2>&1)
    rc=$?
    set -e
    # r9 FIX: every match below greps the ONE capture file, never a live pipe.
    # The replaced idiom (`printf '%s\n' "$out" | grep -qE …`) raced: grep -q
    # exits at the first match while printf is still writing, printf takes
    # SIGPIPE mid-stream, pipefail makes the pipeline rc 141, and a regex that
    # IS present is scored as missing — a random false-FAIL, green on rerun.
    # Measured at these output sizes (2.5-4 KB): 15/8000 invocations rc=141 with
    # the match present (match near the top of the stream), 0/10000 with the
    # match at the end. Once the text is in a file there is no writer left for
    # grep to kill.
    # corpus/lessons/2026-10-15-selftest-grep-sigpipe-race.md.
    printf '%s\n' "$out" > "$OUT_FILE"
    if [ "$rc" -ne "$wrc" ]; then
      bad "$label: exit $rc want $wrc; tail=$(printf '%s' "$out" | tail -n3 | tr '\n' '|')"
    elif ! grep -qE "^MORI_CENSUS: ${wverdict} " "$OUT_FILE"; then
      bad "$label: verdict want $wverdict; got=$(grep -m1 '^MORI_CENSUS:' "$OUT_FILE" || true)"
    elif grep -qE 'integer expected|line [0-9]+: \[: ' "$OUT_FILE"; then
      # r7: a probe whose normal path prints a bash diagnostic (e.g. a `[` test
      # called with a non-integer) is defective even when its answer happens to
      # be right — measured: `[: max: integer expected` on stderr from the
      # memory fill arm while the row still read correctly. The output is
      # captured with 2>&1, so this catches stderr noise in every case.
      bad "$label: shell diagnostic noise in census output: $(grep -m1 -E 'integer expected|line [0-9]+: \[: ' "$OUT_FILE" || true)"
    else
      miss=''
      for re in "$@"; do
        grep -qE -- "$re" "$OUT_FILE" || miss="$miss |$re|"
      done
      if [ -n "$miss" ]; then
        bad "$label: missing match $miss"
      else
        ok "$label (exit $rc $wverdict)"
      fi
    fi
    fx_no_mutation "$FX" "$before"
    EXTRA_ENV=()
  }

  check_cli() {
    local label=$1 wrc=$2; shift 2
    local res=() out rc miss=''
    while [ $# -gt 0 ] && [ "$1" != '--' ]; do res+=("$1"); shift; done
    [ "${1:-}" = '--' ] && shift
    set +e
    out=$(bash "$SELF" "$@" 2>&1)
    rc=$?
    set -e
    printf '%s\n' "$out" > "$OUT_FILE"
    if [ "$rc" -ne "$wrc" ]; then
      bad "$label: exit $rc want $wrc"
    else
      miss=''
      for re in "${res[@]}"; do
        grep -qE -- "$re" "$OUT_FILE" || miss="$miss |$re|"
      done
      if [ -n "$miss" ]; then bad "$label: missing $miss"; else ok "$label (exit $rc)"; fi
    fi
  }

  # r10: pin/drift runners. pd_run executes the census under the SAME fixture
  # env check() uses (sut_env), with arbitrary args, capturing all output into
  # a file; PD_RC carries the exit. pd_check asserts on that file the same way
  # check_cli() does (grep over a captured file, never a live pipe).
  pd_run() { # <script> <outfile> <args...>
    local scr=$1 outf=$2
    shift 2
    sut_env
    set +e
    env -i "${SUT_ENV[@]}" "${EXTRA_ENV[@]+"${EXTRA_ENV[@]}"}" bash "$scr" "$@" > "$outf" 2>&1
    PD_RC=$?
    set -e
    EXTRA_ENV=()
  }

  pd_check() { # <label> <rc> <want-rc> <file> <re...>
    local label=$1 rc=$2 wrc=$3 file=$4
    shift 4
    local miss='' re tailtext=''
    if [ "$rc" -ne "$wrc" ]; then
      tailtext=$(tail -n2 "$file" 2>/dev/null)
      bad "$label: exit $rc want $wrc; tail=${tailtext//$'\n'/|}"
      return 0
    fi
    for re in "$@"; do
      grep -qE -- "$re" "$file" || miss="$miss |$re|"
    done
    if [ -n "$miss" ]; then
      bad "$label: missing match $miss"
    else
      ok "$label (exit $rc)"
    fi
  }

  # --- cases ---------------------------------------------------------------
  PIN_NOW=1700000000

  # --- r12 roster sources ---------------------------------------------------
  # Parsed config is input data, not shell code. A quote-terminated lane row
  # and comments are accepted; the embedded and top-level touch commands must
  # never execute.
  FX="$work/fx/roster-parse"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  canary="$work/roster-config-executed"
  rm -f "$FX/ufo/state/kagi.round"
  printf '5\n' > "$FX/ufo/state/alpha.round"
  printf '5\n' > "$FX/ufo/state/x.round"
  printf '5\n' > "$FX/ufo/state/beta.round"
  printf '# ignored|comment|row\nLANES="\nalpha|alpha-shokunin|axis\nx|$(touch %s)|y\nbeta|beta-shokunin|axis "\ntouch %s\nOTHER="\nshadow|shadow-shokunin|axis\n"\n' \
    "$canary" "$canary" > "$FX/root/shokunin.conf"
  EXTRA_ENV=(MORI_ROSTER_LANES=)
  check 'roster: parse conf order, quote-terminated row and comments without sourcing' 0 CLEAN \
    'roster_source=conf\+state roster_n=3 conf_n=3 state_n=3 conf_dropped_n=0 state_dropped_n=0' \
    '^SURFACE lane\.alpha:' \
    '^SURFACE lane\.x:' \
    '^SURFACE lane\.beta:' \
    '^MORI_CENSUS: CLEAN '
  if [ -e "$canary" ]; then bad 'roster: config was not sourced (canary absent)'; else ok 'roster: config was not sourced (canary absent)'; fi
  if grep -qE '^SURFACE lane\.shadow:' "$OUT_FILE"; then bad 'roster: rows outside LANES= are not lanes'; else ok 'roster: rows outside LANES= are not lanes'; fi

  FX="$work/fx/roster-env"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf 'LANES="\nalpha|alpha-shokunin|axis\n"\n' > "$FX/root/shokunin.conf"
  EXTRA_ENV=(MORI_ROSTER_LANES=kagi)
  check 'roster: MORI_ROSTER_LANES override wins' 0 CLEAN \
    'roster_source=env roster_n=1 conf_n=0 state_n=0' \
    '^SURFACE lane\.kagi:' \
    '^MORI_CENSUS: CLEAN '

  FX="$work/fx/roster-builtin"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  rm -rf "$FX/ufo/state"
  EXTRA_ENV=(MORI_ROSTER_LANES=)
  check 'roster: absent conf and state select historical builtin' 0 CLEAN \
    'roster_source=builtin roster_n=9 conf_n=0 state_n=0' \
    '^SURFACE lane\.protocol:' \
    '^SURFACE lane\.kama:' \
    '^MORI_CENSUS: CLEAN '

  FX="$work/fx/roster-conf-only"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf 'LANES="\nalpha|alpha-shokunin|axis\n"\n' > "$FX/root/shokunin.conf"
  rm -f "$FX/ufo/state/"*.round
  EXTRA_ENV=(MORI_ROSTER_LANES=)
  check 'roster: conf-only set retained when state set is empty' 0 CLEAN \
    'roster_source=conf roster_n=1 conf_n=1 state_n=0' \
    'FINDING ROSTER_SET_MISMATCH severity=info obs=conf_only=alpha state_only=none' \
    '^SURFACE lane\.alpha:' \
    '^MORI_CENSUS: CLEAN '

  FX="$work/fx/roster-conf-unreadable"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf 'LANES="\nalpha|alpha-shokunin|axis\n"\n' > "$FX/root/shokunin.conf"
  chmod 000 "$FX/root/shokunin.conf"
  EXTRA_ENV=(MORI_ROSTER_LANES=)
  check 'roster: unreadable conf is not treated as an empty set' 0 CLEAN \
    'roster_source=state roster_n=1 conf_n=0 state_n=1' \
    '^SURFACE lane\.kagi:' \
    '^MORI_CENSUS: CLEAN '
  if grep -qE '^FINDING ROSTER_SET_MISMATCH' "$OUT_FILE"; then bad 'roster: unreadable conf does not manufacture mismatch'; else ok 'roster: unreadable conf does not manufacture mismatch'; fi

  FX="$work/fx/roster-mismatch"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf 'LANES="alpha|alpha-shokunin|axis\nbeta|beta-shokunin|axis"\n' > "$FX/root/shokunin.conf"
  printf '5\n' > "$FX/ufo/state/zeta.round"
  printf '5\n' > "$FX/ufo/state/delta.round"
  EXTRA_ENV=(MORI_ROSTER_LANES=)
  check 'roster: mismatch is INFO and names both set differences' 0 CLEAN \
    'FINDING ROSTER_SET_MISMATCH severity=info obs=conf_only=alpha,beta state_only=delta,kagi,zeta' \
    'roster_source=conf\+state roster_n=5 conf_n=2 state_n=3' \
    '^MORI_CENSUS: CLEAN '

  FX="$work/fx/roster-shapes"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  long_id=$(printf '%050d' 0 | tr '0' 'a')
  printf '99\n' > "$FX/vault"
  ln -s "$FX/vault" "$FX/ufo/state/rogue.round"
  printf '5\n' > "$FX/ufo/state/$long_id.round"
  printf 'LANES="\nkagi|kagi-shokunin|axis\n' > "$FX/root/shokunin.conf"
  printf '%s|ignored|axis\n"\n' "$long_id" >> "$FX/root/shokunin.conf"
  EXTRA_ENV=(MORI_ROSTER_LANES=)
  check 'roster: invalid ids dropped and counted; symlink counter excluded' 0 CLEAN \
    'roster_source=conf\+state roster_n=1 conf_n=1 state_n=1 conf_dropped_n=1 state_dropped_n=1' \
    '^MORI_CENSUS: CLEAN '
  if grep -qE '^SURFACE lane\.rogue:' "$OUT_FILE"; then bad 'roster: state symlink excluded from roster'; else ok 'roster: state symlink excluded from roster'; fi

  # ISO-8601 with offset, the live ledger's timestamp grammar (field 1)
  ts_iso() { date -u -d "@$1" +%Y-%m-%dT%H:%M:%S+00:00 2>/dev/null || date -u -r "$1" +%Y-%m-%dT%H:%M:%S+00:00; }

  FX="$work/fx/clean"; mkdir -p "$FX"; fx_quiet "$FX"
  # df target must exist
  mkdir -p "$FX/root"
  check 'clean: all quiet' 0 CLEAN \
    '^SURFACE watchdog: ok' \
    '^MORI_CENSUS: CLEAN '

  FX="$work/fx/wd-absent"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  : > "$FX/stub/pgrep"; printf 1 > "$FX/stub/pgrep.rc"
  check 'drift: WATCHDOG_ABSENT' 1 DRIFT \
    'FINDING WATCHDOG_ABSENT' \
    '^MORI_CENSUS: DRIFT '

  FX="$work/fx/wd-stale"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  # age log far in the past relative to PIN_NOW
  printf 'old\n' > "$FX/ufo/watchdog.log"
  touch -d '@1600000000' "$FX/ufo/watchdog.log" 2>/dev/null || true
  # prevent check() from freshening this case's log: use empty touch guard via separate path
  # override: re-stale after check's freshen by using PIN and EXTRA — simpler: set STALE threshold 0 via env
  EXTRA_ENV=(MORI_WATCHDOG_STALE_S=900)
SKIP_FRESHEN=1
    check 'drift: WATCHDOG_STALE' 1 DRIFT \
    'FINDING WATCHDOG_STALE' \
    '^MORI_CENSUS: DRIFT '
  SKIP_FRESHEN=0

  # --- r4: watchdog state-dir rc-gate -----------------------------------------
  # The state walk was a bare `find | wc -l | tr` pipeline: an unreadable
  # `.ufo/state` failed it under pipefail and killed the census before any
  # verdict (canary B; re-measured at fe22a14f: rc 1, header only, 0 verdict
  # lines). The three variants pin the rc-graded contract: unreadable ->
  # disclosed `unavailable` count, missing/empty -> provable 0 (the walk cannot
  # fail), each with a full verdict and every other surface still reporting.
  FX="$work/fx/wd-state-unreadable"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root/kagi-shokunin"
  chmod 000 "$FX/ufo/state"
  check 'watchdog: unreadable state dir -> unavailable-disclosed, no crash' 0 CLEAN \
    '^SURFACE watchdog: ok' \
    'state_rounds=unavailable' \
    'state_unreadable=1' \
    '^MORI_CENSUS: CLEAN '

  FX="$work/fx/wd-state-missing"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root/kagi-shokunin"
  rm -rf "$FX/ufo/state"
  check 'watchdog: missing state dir -> provable 0, no crash' 0 CLEAN \
    '^SURFACE watchdog: ok' \
    'state_rounds=0'

  FX="$work/fx/wd-state-empty"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root/kagi-shokunin"
  rm -f "$FX/ufo/state"/*
  check 'watchdog: empty state dir -> provable 0, no crash' 0 CLEAN \
    '^SURFACE watchdog: ok' \
    'state_rounds=0'

  FX="$work/fx/wave-aged"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  mkdir -p "$FX/ufo/waves/wave-hang"
  printf '{}\n' > "$FX/ufo/waves/wave-hang/swarm-registry.json"
  printf '{}\n' > "$FX/ufo/waves/wave-hang/dispatch.json"
  # an unsettled wave (registry+dispatch, no results) backdated well past the
  # window: the fixture must prove the AGE comparison, not just that the finding
  # can fire — a 0 threshold with a freshly-created file proves nothing.
  mkdir -p "$FX/ufo/waves/wave-hang"
  printf '{"wave":"wave-hang"}\n' > "$FX/ufo/waves/wave-hang/swarm-registry.json"
  printf '{"wave":"wave-hang"}\n' > "$FX/ufo/waves/wave-hang/dispatch.json"
  find "$FX/ufo/waves/wave-hang" -type f -exec touch -d '@1600000000' {} + 2>/dev/null || true
  EXTRA_ENV=(MORI_WAVE_UNSETTLED_S=900)
  SKIP_FRESHEN=1
  check 'drift: WAVE_UNSETTLED_AGE' 1 DRIFT \
    'FINDING WAVE_UNSETTLED_AGE' \
    'wave=wave-hang'
  SKIP_FRESHEN=0

  FX="$work/fx/wave-fresh-unsettled"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  mkdir -p "$FX/ufo/waves/wave-live"
  printf '{}\n' > "$FX/ufo/waves/wave-live/run.json"
  # unsettled but age under threshold (default 7200, mtime=PIN_NOW) → must NOT fire
  check 'clean: unsettled young wave does not fire' 0 CLEAN \
    '^SURFACE waves: ok'

  # --- r13 structured journal scopes + r14 alarm/routing --------------------
  # One SURFACE row per scope (journal.user / journal.system); catalog MESSAGE_ID
  # classes plus field-validated signal-11 and unit records; never summed, never
  # a MESSAGE read. r14: one global OOM_KILL_JOURNAL crit line (per-scope/per-
  # source counters, no sum), fleet/non-fleet/unattributed unit routing, and the
  # user KILL_SIGNAL warn for process SIGKILL OR unit result 'signal'.
  BOOT13=0123456789abcdef0123456789abcdef
  jrec() { # <slot-file> <message-id> [extra json]
    printf '{"_BOOT_ID":"%s","MESSAGE_ID":"%s"%s,"MESSAGE":"MORI_JOURNAL_CANARY"}\n' \
      "$BOOT13" "$2" "${3:-}" >> "$1"
  }

  FX="$work/fx/journal-matrix"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  for i in 1 2 3; do jrec "$FX/stub/journal-user-kernel_oom" fe6faa94e7774663a0da52717891d8ef; done
  jrec "$FX/stub/journal-user-coredump" fc2e22bc6ee647b6b90729ab34a250b1
  jrec "$FX/stub/journal-user-coredump" fc2e22bc6ee647b6b90729ab34a250b1
  jrec "$FX/stub/journal-user-segfault" fc2e22bc6ee647b6b90729ab34a250b1 ',"COREDUMP_SIGNAL":"11"'
  jrec "$FX/stub/journal-user-unit_sigkill" 98e322203f7a4ed290d09fe03c09fe15 ',"EXIT_CODE":"killed","EXIT_STATUS":"9"'
  jrec "$FX/stub/journal-user-unit_failure" d9b373ed55a64feb8242e02dbe79a49c
  for i in 1 2 3 4 5; do jrec "$FX/stub/journal-system-kernel_oom" fe6faa94e7774663a0da52717891d8ef; done
  for i in 1 2; do jrec "$FX/stub/journal-system-oomd" d989611b15e44c9dbf31e3c81256e4ed; done
  jrec "$FX/stub/journal-user-oomd" d989611b15e44c9dbf31e3c81256e4ed
  jrec "$FX/stub/journal-system-coredump" fc2e22bc6ee647b6b90729ab34a250b1
  jrec "$FX/stub/journal-system-segfault" fc2e22bc6ee647b6b90729ab34a250b1 ',"COREDUMP_SIGNAL":"11"'
  jrec "$FX/stub/journal-system-unit_sigkill" 98e322203f7a4ed290d09fe03c09fe15 ',"EXIT_CODE":"killed","EXIT_STATUS":"9"'
  jrec "$FX/stub/journal-system-unit_failure" d9b373ed55a64feb8242e02dbe79a49c ',"USER_UNIT":"kagi-shokunin.service","UNIT_RESULT":"resources"'
  check 'journal: all twelve scoped cells counted; one OOM crit; user SIGKILL warn; routing info' 1 DRIFT \
    '^SURFACE journal\.user: ok .*scope=user' \
    '^SURFACE journal\.system: ok .*scope=system' \
    'kernel_oom_notice=3 oomd_notice=1 coredump_notice=2 segfault_signal11=1 unit_sigkill_record=1 unit_failure_record=1' \
    'unit_fleet=0 unit_nonfleet=0 unit_unknown=1 unit_missing=1 unit_ambiguous=0 unit_malformed=0 unit_oom=0 unit_oom_fleet=0 unit_oom_nonfleet=0 unit_oom_subject_unknown=0 unit_oom_result_unknown=1 unit_signal=0' \
    'unit_subject_fields=UNIT,USER_UNIT' \
    'unit_query_output_fields=_BOOT_ID,MESSAGE_ID,UNIT,USER_UNIT,UNIT_RESULT' \
    '^SURFACE journal\.system: ok .*kernel_oom_notice=5 oomd_notice=2 coredump_notice=1 segfault_signal11=1 unit_sigkill_record=1 unit_failure_record=1 unit_fleet=1' \
    '^SURFACE journal\.system: ok .*unit_unknown=0' \
    "boot=$BOOT13" \
    'FINDING OOM_KILL_JOURNAL severity=crit .*paths=kernel_oom_notice .*user_notice=3 .*user_unit_oom=0 .*system_notice=5 .*system_unit_oom=0 ' \
    'FINDING OOMD_NOTICE_JOURNAL_USER .*count=1 .*scope=user' \
    'FINDING OOMD_NOTICE_JOURNAL_SYSTEM .*count=2 .*scope=system' \
    'FINDING COREDUMP_NOTICE_JOURNAL_USER .*count=2 .*scope=user' \
    'FINDING COREDUMP_NOTICE_JOURNAL_SYSTEM .*count=1 .*scope=system' \
    'FINDING SEGFAULT_SIGNAL11_JOURNAL_USER .*unit=record .*count=1 .*scope=user' \
    'FINDING SEGFAULT_SIGNAL11_JOURNAL_SYSTEM .*unit=record .*count=1 .*scope=system' \
    'FINDING KILL_SIGNAL_JOURNAL severity=warn .*paths=process_sigkill .*count=1 .*process_sigkill=1 .*user_unit_signal=0 .*scope=user' \
    'FINDING KILL_SIGNAL_JOURNAL_SYSTEM .*count=1 .*scope=system' \
    'FINDING UNIT_FAILURE_JOURNAL_SYSTEM severity=info .*count=1 .*subject=fleet .*scope=system' \
    'FINDING UNIT_FAILURE_UNATTRIBUTED_JOURNAL severity=info .*count=1 .*missing=1 .*ambiguous=0 .*malformed=0 .*owner=unresolved .*reason=subject-metadata-unknown .*scope=user' \
    'unit=notice .*trust=client-supplied' \
    '^MORI_CENSUS: DRIFT '
  # The OOM alarm is one line: no summed count= and each counter exactly once.
  if grep -qE '^FINDING OOM_KILL_JOURNAL .*count=' "$OUT_FILE"; then bad 'journal: OOM line carries a summed count='; fi
  for f in user_notice system_notice user_unit_oom system_unit_oom; do
    if [ "$(grep -oE "\\b$f=[^ ]+" "$OUT_FILE" | wc -l)" -ne 1 ]; then bad "journal: OOM field $f not exactly once"; fi
  done
  # The fixtures carry MESSAGE text; the census must never print it (a read of
  # MESSAGE is the M13 defect this probe replaces).
  if grep -q 'MORI_JOURNAL_CANARY' "$OUT_FILE"; then bad 'journal: MESSAGE canary leaked to census output'; fi

  FX="$work/fx/journal-oom-system"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  jrec "$FX/stub/journal-system-kernel_oom" fe6faa94e7774663a0da52717891d8ef
  check 'journal: system kernel-OOM notice alone alarms crit' 1 DRIFT \
    'FINDING OOM_KILL_JOURNAL severity=crit .*paths=kernel_oom_notice .*user_notice=0 .*system_notice=1' \
    '^MORI_CENSUS: DRIFT '

  FX="$work/fx/journal-unit-rc1-oom"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  jrec "$FX/stub/journal-user-kernel_oom" fe6faa94e7774663a0da52717891d8ef
  : > "$FX/stub/journal-user-unit_failure"; printf 1 > "$FX/stub/journal-user-unit_failure.rc"
  check 'journal: unit query rc1 unavailable; kernel OOM still crit, split tokens unavailable' 1 DRIFT \
    'FINDING OOM_KILL_JOURNAL severity=crit .*user_notice=1 .*user_unit_oom=unavailable:rc-1' \
    'unit_failure_record=unavailable:rc-1' \
    'unit_fleet=unavailable:rc-1' 'unit_oom=unavailable:rc-1' 'unit_signal=unavailable:rc-1' \
    '^MORI_CENSUS: DRIFT '
  if grep -qE '^FINDING UNIT_FAILURE_' "$OUT_FILE"; then bad 'journal: routing finding emitted from an unavailable unit class'; fi

  FX="$work/fx/journal-unit-fleet"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  jrec "$FX/stub/journal-user-unit_failure" d9b373ed55a64feb8242e02dbe79a49c ',"USER_UNIT":"kagi-shokunin.service","UNIT_RESULT":"resources"'
  check 'journal: fleet unit failure is INFO and CLEAN (owner mori)' 0 CLEAN \
    'unit_failure_record=1 unit_fleet=1 unit_nonfleet=0 unit_unknown=0' \
    'FINDING UNIT_FAILURE_JOURNAL severity=info .*count=1 .*subject=fleet .*owner=mori .*scope=user' \
    '^MORI_CENSUS: CLEAN '
  if grep -qE '^FINDING UNIT_FAILURE_OUT_OF_SCOPE' "$OUT_FILE"; then bad 'journal: fleet failure also routed non-fleet'; fi

  FX="$work/fx/journal-unit-nonfleet"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  # User journal with UNIT= is the cross-scope shape (live user records normally
  # carry USER_UNIT; the system-journal arm below carries USER_UNIT). Kept to
  # prove the subject is read scope-independently, not by journal scope.
  jrec "$FX/stub/journal-user-unit_failure" d9b373ed55a64feb8242e02dbe79a49c ',"UNIT":"pipewire-pulse.service","UNIT_RESULT":"resources"'
  check 'journal: non-fleet unit failure is INFO, CLEAN, owner tsukuroi' 0 CLEAN \
    'unit_failure_record=1 unit_fleet=0 unit_nonfleet=1 unit_unknown=0' \
    'FINDING UNIT_FAILURE_OUT_OF_SCOPE severity=info .*count=1 .*subject=nonfleet .*owner=tsukuroi .*scope=user' \
    '^MORI_CENSUS: CLEAN '
  if grep -qE '^FINDING UNIT_FAILURE_JOURNAL ' "$OUT_FILE"; then bad 'journal: non-fleet failure also routed fleet'; fi

  FX="$work/fx/journal-unit-dual-subject"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  jrec "$FX/stub/journal-user-unit_failure" d9b373ed55a64feb8242e02dbe79a49c ',"UNIT":"kagi-shokunin.service","USER_UNIT":"kagi-shokunin.service","UNIT_RESULT":"resources"'
  check 'journal: both subject fields present -> unknown even when equal' 0 CLEAN \
    'unit_failure_record=1 unit_fleet=0 unit_nonfleet=0 unit_unknown=1' \
    'unit_ambiguous=1' \
    'FINDING UNIT_FAILURE_UNATTRIBUTED_JOURNAL severity=info .*count=1 .*ambiguous=1 .*owner=unresolved' \
    '^MORI_CENSUS: CLEAN '

  FX="$work/fx/journal-unit-escaped"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  jrec "$FX/stub/journal-user-unit_failure" d9b373ed55a64feb8242e02dbe79a49c ',"USER_UNIT":"app-Hyprland-xdg\\x2dterminal\\x2dexec-dd9e67bd.scope","UNIT_RESULT":"resources"'
  check 'journal: legal systemd \xHH unit name classifies (non-fleet)' 0 CLEAN \
    'unit_fleet=0 unit_nonfleet=1 unit_unknown=0' \
    'unit_malformed=0' \
    'FINDING UNIT_FAILURE_OUT_OF_SCOPE severity=info .*count=1' \
    '^MORI_CENSUS: CLEAN '

  FX="$work/fx/journal-unit-bad-escape"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  jrec "$FX/stub/journal-user-unit_failure" d9b373ed55a64feb8242e02dbe79a49c ',"USER_UNIT":"x\\qy.service","UNIT_RESULT":"resources"'
  check 'journal: illegal backslash escape is malformed, never non-fleet' 0 CLEAN \
    'unit_fleet=0 unit_nonfleet=0 unit_unknown=1' \
    'unit_malformed=1' \
    'FINDING UNIT_FAILURE_UNATTRIBUTED_JOURNAL severity=info .*malformed=1' \
    '^MORI_CENSUS: CLEAN '

  FX="$work/fx/journal-unit-signal"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  jrec "$FX/stub/journal-user-unit_failure" d9b373ed55a64feb8242e02dbe79a49c ',"USER_UNIT":"kagi-shokunin.service","UNIT_RESULT":"signal"'
  check 'journal: user unit result signal alone warns and DRIFTS' 1 DRIFT \
    'unit_signal=1' \
    'FINDING KILL_SIGNAL_JOURNAL severity=warn .*paths=unit_result_signal .*count=0 .*process_sigkill=0 .*user_unit_signal=1 .*scope=user' \
    '^MORI_CENSUS: DRIFT '

  FX="$work/fx/journal-unit-oom-fleet"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  jrec "$FX/stub/journal-user-unit_failure" d9b373ed55a64feb8242e02dbe79a49c ',"USER_UNIT":"kagi-shokunin.service","UNIT_RESULT":"oom-kill"'
  check 'journal: fleet unit oom-kill alarms crit and stays in the fleet route' 1 DRIFT \
    'FINDING OOM_KILL_JOURNAL severity=crit .*paths=unit_result_oom_kill .*user_notice=0 .*user_unit_oom=1' \
    'FINDING UNIT_FAILURE_JOURNAL severity=info .*count=1 .*subject=fleet' \
    'unit_oom=1 unit_oom_fleet=1 unit_oom_nonfleet=0 unit_oom_subject_unknown=0' \
    '^MORI_CENSUS: DRIFT '

  FX="$work/fx/journal-unit-oom-unknown"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  jrec "$FX/stub/journal-system-unit_failure" d9b373ed55a64feb8242e02dbe79a49c ',"UNIT_RESULT":"oom-kill"'
  check 'journal: subjectless unit oom-kill alarms crit; raw count and unattributed kept' 1 DRIFT \
    'FINDING OOM_KILL_JOURNAL severity=crit .*paths=unit_result_oom_kill .*user_notice=0 .*system_unit_oom=1' \
    'unit_failure_record=1' \
    'unit_unknown=1 unit_missing=1' \
    'unit_oom=1' \
    'unit_oom_subject_unknown=1' \
    'FINDING UNIT_FAILURE_UNATTRIBUTED_JOURNAL severity=info .*count=1 .*scope=system' \
    '^MORI_CENSUS: DRIFT '

  FX="$work/fx/journal-unit-result-array"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  jrec "$FX/stub/journal-user-unit_failure" d9b373ed55a64feb8242e02dbe79a49c ',"USER_UNIT":"kagi-shokunin.service","UNIT_RESULT":["oom-kill"]'
  check 'journal: array UNIT_RESULT is unknown, not oom evidence; CLEAN' 0 CLEAN \
    'unit_oom=0' 'unit_oom_result_unknown=1' \
    'FINDING UNIT_FAILURE_JOURNAL severity=info .*count=1' \
    '^MORI_CENSUS: CLEAN '
  if grep -qE '^FINDING OOM_KILL_JOURNAL' "$OUT_FILE"; then bad 'journal: array UNIT_RESULT produced an OOM alarm'; fi

  FX="$work/fx/journal-unit-injection"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  jrec "$FX/stub/journal-user-unit_failure" d9b373ed55a64feb8242e02dbe79a49c ',"USER_UNIT":"x.service\nFINDING OOM_KILL_JOURNAL severity=crit","UNIT_RESULT":"resources"'
  check 'journal: UNIT newline injection never reaches output (unknown bucket)' 0 CLEAN \
    'unit_unknown=1' 'unit_malformed=1' \
    'FINDING UNIT_FAILURE_UNATTRIBUTED_JOURNAL severity=info .*malformed=1' \
    '^MORI_CENSUS: CLEAN '
  if grep -qE '^FINDING OOM_KILL_JOURNAL severity=crit$' "$OUT_FILE"; then bad 'journal: UNIT bytes forged a finding line'; fi
  if grep -q 'x.service' "$OUT_FILE"; then bad 'journal: UNIT name bytes leaked to output'; fi

  FX="$work/fx/journal-unit-system-userunit"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  jrec "$FX/stub/journal-system-unit_failure" d9b373ed55a64feb8242e02dbe79a49c ',"USER_UNIT":"ufo-sighting-ctl.service","UNIT_RESULT":"resources"'
  check 'journal: system journal USER_UNIT subject classifies fleet (scope-independent)' 0 CLEAN \
    'unit_fleet=1 unit_nonfleet=0 unit_unknown=0' \
    'FINDING UNIT_FAILURE_JOURNAL_SYSTEM severity=info .*count=1 .*subject=fleet .*scope=system' \
    '^MORI_CENSUS: CLEAN '

  FX="$work/fx/journal-text-only"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  # Every queried slot answers a valid empty stream; the legacy text lives only
  # in the global journal file, so a text-counting probe would read it while the
  # structured queries must stay 0.
  : > "$FX/stub/journal"
  for cls in kernel_oom oomd coredump unit_sigkill unit_failure segfault; do
    : > "$FX/stub/journal-user-$cls"; : > "$FX/stub/journal-system-$cls"
  done
  printf 'kernel: Out of memory: Killed process 4242 status=9/KILL\nFailed with result signal SIGKILL\n' > "$FX/stub/journal"
  check 'journal: legacy text ids are not counted (Q15)' 0 CLEAN \
    '^SURFACE journal\.user: ok .*kernel_oom_notice=0' \
    '^SURFACE journal\.system: ok .*kernel_oom_notice=0' \
    'unit_oom=0' 'unit_signal=0'
  if grep -qE '^FINDING (OOM_KILL_JOURNAL|KILL_SIGNAL_JOURNAL|SEGFAULT_JOURNAL|UNIT_FAILURE_JOURNAL|UNIT_FAILURE_OUT_OF_SCOPE|UNIT_FAILURE_UNATTRIBUTED_JOURNAL)' "$OUT_FILE"; then
    bad 'journal: legacy text class produced a finding'
  fi

  FX="$work/fx/journal-user-rc1"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  : > "$FX/stub/journal-user-kernel_oom"; printf 1 > "$FX/stub/journal-user-kernel_oom.rc"
  check 'journal: user producer rc1 -> user unavailable, system still counted' 0 CLEAN \
    '^SURFACE journal\.user: unavailable .*kernel_oom_notice=unavailable:rc-1' \
    '^SURFACE journal\.user: unavailable .*rc=1' \
    '^SURFACE journal\.system: ok .*kernel_oom_notice=0'

  FX="$work/fx/journal-system-rc2"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  : > "$FX/stub/journal-system-oomd"; printf 2 > "$FX/stub/journal-system-oomd.rc"
  check 'journal: system producer rc2 -> system unavailable, user ok' 0 CLEAN \
    '^SURFACE journal\.system: unavailable .*oomd_notice=unavailable:rc-2' \
    '^SURFACE journal\.system: unavailable .*rc=2' \
    '^SURFACE journal\.user: ok .*oomd_notice=0'

  FX="$work/fx/journal-system-rc1"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  : > "$FX/stub/journal-system-coredump"; printf 1 > "$FX/stub/journal-system-coredump.rc"
  check 'journal: system producer rc1 -> system unavailable, user still counted' 0 CLEAN \
    '^SURFACE journal\.system: unavailable .*coredump_notice=unavailable:rc-1' \
    '^SURFACE journal\.user: ok .*coredump_notice=0'

  FX="$work/fx/journal-stderr"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  : > "$FX/stub/journal-user-unit_sigkill"
  printf 'warning: partial journal access MORI_STDERR_CANARY\n' > "$FX/stub/journal-user-unit_sigkill.err"
  check 'journal: nonempty stderr -> unavailable, never counted' 0 CLEAN \
    '^SURFACE journal\.user: unavailable .*unit_sigkill_record=unavailable:stderr-nonempty' \
    '^SURFACE journal\.system: ok '
  if grep -q 'MORI_STDERR_CANARY' "$OUT_FILE"; then bad 'journal: stderr bytes leaked to census output'; fi

  FX="$work/fx/journal-malformed"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf '{not json\n' > "$FX/stub/journal-user-coredump"
  check 'journal: malformed JSON -> unavailable, never 0' 0 CLEAN \
    '^SURFACE journal\.user: unavailable .*coredump_notice=unavailable:malformed-json' \
    '^SURFACE journal\.system: ok '

  FX="$work/fx/journal-identity-mismatch"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  # A record carrying a DIFFERENT catalog id must not be counted for the query.
  jrec "$FX/stub/journal-system-kernel_oom" d989611b15e44c9dbf31e3c81256e4ed
  check 'journal: record identity mismatch -> unavailable' 0 CLEAN \
    '^SURFACE journal\.system: unavailable .*kernel_oom_notice=unavailable:record-invalid'

  FX="$work/fx/journal-foreign-boot"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf '{"_BOOT_ID":"ffffffffffffffffffffffffffffffff","MESSAGE_ID":"fe6faa94e7774663a0da52717891d8ef","MESSAGE":"MORI_JOURNAL_CANARY"}\n' \
    > "$FX/stub/journal-user-kernel_oom"
  check 'journal: record from another boot -> unavailable' 0 CLEAN \
    '^SURFACE journal\.user: unavailable .*kernel_oom_notice=unavailable:boot-mismatch'

  FX="$work/fx/journal-multi-boot"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf '{"_BOOT_ID":"ffffffffffffffffffffffffffffffff","MESSAGE_ID":"d989611b15e44c9dbf31e3c81256e4ed"}\n' \
    >> "$FX/stub/journal-user-oomd"
  printf '{"_BOOT_ID":"eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee","MESSAGE_ID":"d989611b15e44c9dbf31e3c81256e4ed"}\n' \
    >> "$FX/stub/journal-user-oomd"
  check 'journal: records from several boots -> unavailable:multi-boot' 0 CLEAN \
    '^SURFACE journal\.user: unavailable .*oomd_notice=unavailable:multi-boot'

  FX="$work/fx/journal-no-jq"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  EXTRA_ENV=(MORI_JQ_BIN="$work/absent-jq")
  check 'journal: absent JSON parser -> both scopes unavailable, no counts' 0 CLEAN \
    '^SURFACE journal\.user: unavailable .*parser=missing' \
    '^SURFACE journal\.system: unavailable .*parser=missing'

  FX="$work/fx/journal-no-bin"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  EXTRA_ENV=(MORI_JOURNALCTL_BIN="$work/absent-journalctl")
  check 'journal: absent journalctl -> both scopes unavailable' 0 CLEAN \
    '^SURFACE journal\.user: unavailable .*journalctl=missing' \
    '^SURFACE journal\.system: unavailable .*journalctl=missing'

  FX="$work/fx/journal-no-boot"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  EXTRA_ENV=(MORI_BOOT_ID=not-a-boot-id)
  check 'journal: invalid boot anchor -> both scopes unavailable' 0 CLEAN \
    '^SURFACE journal\.user: unavailable .*boot_id=unavailable' \
    '^SURFACE journal\.system: unavailable .*boot_id=unavailable'

  FX="$work/fx/cgroup-oom"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf 'low 0\nhigh 0\nmax 0\noom 1\noom_kill 1\noom_group_kill 0\n' > "$FX/cgroup/memory.events"
  check 'drift: CGROUP_OOM_KILL' 1 DRIFT \
    'FINDING CGROUP_OOM_KILL'

  FX="$work/fx/disk-crit"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf 'Filesystem 1024-blocks Used Available Capacity Mounted on\n/dev/fx 1000000 960000 40000 96%% /fx\n' > "$FX/stub/df"
  check 'drift: DISK_CRITICAL' 1 DRIFT \
    'FINDING DISK_CRITICAL'

  FX="$work/fx/disk-ok"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf 'Filesystem 1024-blocks Used Available Capacity Mounted on\n/dev/fx 1000000 10000 990000 2%% /fx\n' > "$FX/stub/df"
  check 'clean: disk under warn' 0 CLEAN \
    '^SURFACE disk: ok'

  FX="$work/fx/lane-silent"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  # r2 grades silence against the LAUNCH anchor, not a rolling window and not the
  # repo's file mtimes. The fixture writes a real-grammar launch line into the
  # ledger with the pinned clock and leaves the lane repo readable, with no
  # post-launch subject commit, no other-lane commit and no fresh file — the
  # only row-D shape, and the only case allowed to emit LANE_SILENT.
  mkdir -p "$FX/root/kagi-shokunin"
  printf 'old\n' > "$FX/root/kagi-shokunin/LOG.md"
  touch -d '@1600000000' "$FX/root/kagi-shokunin/LOG.md" 2>/dev/null || true
  printf '%s launch kagi round=7 pid=4242\n' "$(ts_iso $((PIN_NOW - 2000)))" >> "$FX/ufo/watchdog.log"
  printf 1 > "$FX/stub/git-cat-file.rc"
  PIN_NOW=1700000000
  SKIP_FRESHEN=1
  EXTRA_ENV=(MORI_LANE_SILENCE_S=900)
  check 'drift: LANE_SILENT' 1 DRIFT \
    'FINDING LANE_SILENT' \
    'lane=kagi round=7 launch_epoch=1699998000 age_s=2000' \
    '^SURFACE lane\.kagi: silent '
  SKIP_FRESHEN=0

  # --- r2 silence grading: launch-aware, closure-aware, authorship-aware -------
  # Contract corpus/knowledge/silence-grading-r2.md. The ledger is the watchdog
  # log in the live grammar ("<ISO-8601+offset> launch <lane> round=<N> <tail>");
  # git answers per verb through the fixture dispatcher (git-log / git-log1 /
  # git-cat-file / git-ls-files / git-rev-parse). No case branches on fixture
  # shape or on MORI_FIXTURE: the probe reads the same facts live and here.

  FX="$work/fx/sil-subject-progressing"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root/kagi-shokunin"
  printf '%s launch kagi round=7 pid=4242\n' "$(ts_iso $((PIN_NOW - 2000)))" >> "$FX/ufo/watchdog.log"
  printf '%s\n' "1699998600 kagi-shokunin <kagi@shokunin.local>" > "$FX/stub/git-log"
  printf 1 > "$FX/stub/git-cat-file.rc"
  EXTRA_ENV=(MORI_LANE_SILENCE_S=900)
  check 'silence: subject commit post-launch -> progressing' 0 CLEAN \
    '^SURFACE lane\.kagi: progressing ' \
    'basis=row-A'

  FX="$work/fx/sil-prelaunch-silent"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root/kagi-shokunin"
  printf '%s launch kagi round=7 pid=4242\n' "$(ts_iso $((PIN_NOW - 2000)))" >> "$FX/ufo/watchdog.log"
  # The lane's only commit predates the launch: a repo HEAD (or a file mtime) is
  # not the clock — the launch anchor is. Nothing is credited after it => silent.
  printf '%s\n' "1699995000 kagi-shokunin <kagi@shokunin.local>" > "$FX/stub/git-log"
  printf 1 > "$FX/stub/git-cat-file.rc"
  EXTRA_ENV=(MORI_LANE_SILENCE_S=900)
  check 'silence: pre-launch commit only -> silent' 1 DRIFT \
    '^SURFACE lane\.kagi: silent ' \
    'FINDING LANE_SILENT' \
    'launch_epoch=1699998000 age_s=2000'

  FX="$work/fx/sil-eq-launch-silent"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root/kagi-shokunin"
  printf '%s launch kagi round=7 pid=4242\n' "$(ts_iso $((PIN_NOW - 2000)))" >> "$FX/ufo/watchdog.log"
  # A commit whose ct EQUALS the launch is not post-launch (measured: git --since
  # is inclusive at equality, so the strict window needs an explicit comparison).
  printf '%s\n' "1699998000 kagi-shokunin <kagi@shokunin.local>" > "$FX/stub/git-log"
  printf 1 > "$FX/stub/git-cat-file.rc"
  EXTRA_ENV=(MORI_LANE_SILENCE_S=900)
  check 'silence: commit at ct==launch is not post-launch -> silent' 1 DRIFT \
    '^SURFACE lane\.kagi: silent ' \
    'FINDING LANE_SILENT'

  FX="$work/fx/sil-weak-not-promoted"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root/kagi-shokunin"
  printf '%s launch kagi round=7 pid=4242\n' "$(ts_iso $((PIN_NOW - 2000)))" >> "$FX/ufo/watchdog.log"
  # Near-miss identity: the NAME is a superstring of the lane's, the email is
  # exact. It is not the lane, so it must not be promoted to progressing.
  printf '%s\n' "1699998600 kagi-helper-shokunin <kagi@shokunin.local>" > "$FX/stub/git-log"
  printf 1 > "$FX/stub/git-cat-file.rc"
  EXTRA_ENV=(MORI_LANE_SILENCE_S=900)
  check 'silence: other-authored commit only -> progressing-weak' 0 CLEAN \
    '^SURFACE lane\.kagi: progressing-weak ' \
    'basis=row-C'

  # F01 / audit-r11 Appendix B: a large history used to make the authorship
  # membership test a live pipe into an early-exit grep. One exact subject record
  # at the head of 12,000 siblings MUST still grade progressing; the exact count
  # of sibling records is asserted in the negative arm.
  FX="$work/fx/sil-f01-long-subject"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root/kagi-shokunin"
  printf '%s launch kagi round=7 pid=4242\n' "$(ts_iso $((PIN_NOW - 2000)))" >> "$FX/ufo/watchdog.log"
  { printf '1699998600 kagi-shokunin <kagi@shokunin.local>\n'
    for ((i = 0; i < 12000; i++)); do printf '1699998600 aggregator-shokunin <aggregator@shokunin.local>\n'; done
  } > "$FX/stub/git-log"
  printf 1 > "$FX/stub/git-cat-file.rc"
  EXTRA_ENV=(MORI_LANE_SILENCE_S=900)
  check 'silence: 12k-history exact subject -> progressing (F01)' 0 CLEAN \
    '^SURFACE lane\.kagi: progressing ' \
    'basis=row-A'

  FX="$work/fx/sil-f01-long-siblings"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root/kagi-shokunin"
  printf '%s launch kagi round=7 pid=4242\n' "$(ts_iso $((PIN_NOW - 2000)))" >> "$FX/ufo/watchdog.log"
  for ((i = 0; i < 12000; i++)); do printf '1699998600 aggregator-shokunin <aggregator@shokunin.local>\n'; done > "$FX/stub/git-log"
  printf 1 > "$FX/stub/git-cat-file.rc"
  EXTRA_ENV=(MORI_LANE_SILENCE_S=900)
  check 'silence: 12k-history siblings only -> progressing-weak, exact count' 0 CLEAN \
    '^SURFACE lane\.kagi: progressing-weak ' \
    'other_authored_commits=12000'

  FX="$work/fx/sil-young-eq-gate"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root/kagi-shokunin"
  # age == gate is YOUNG: only age > LANE_SILENCE_S is gradeable-old, so a
  # subject commit in the window is not even reached at this age.
  printf '%s launch kagi round=7 pid=4242\n' "$(ts_iso $((PIN_NOW - 900)))" >> "$FX/ufo/watchdog.log"
  printf '%s\n' "1699999600 kagi-shokunin <kagi@shokunin.local>" > "$FX/stub/git-log"
  EXTRA_ENV=(MORI_LANE_SILENCE_S=900)
  check 'silence: strict age gate (age == gate) -> young' 0 CLEAN \
    '^SURFACE lane\.kagi: young ' \
    'basis=row-8'

  FX="$work/fx/sil-synthetic-ts"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root/kagi-shokunin"
  # The superseded synthetic grammar prefixes a "TIMESTAMP" token and carries the
  # epoch in ts=<epoch>: the anchor must come from that token, and the row must
  # show the parsed epoch (the live grammar's field 1 cannot supply it).
  printf 'TIMESTAMP launch kagi round=7 ts=%s\n' "$((PIN_NOW - 2000))" >> "$FX/ufo/watchdog.log"
  printf '%s\n' "1699998600 kagi-shokunin <kagi@shokunin.local>" > "$FX/stub/git-log"
  printf 1 > "$FX/stub/git-cat-file.rc"
  EXTRA_ENV=(MORI_LANE_SILENCE_S=900)
  check 'silence: synthetic ts= ledger anchor' 0 CLEAN \
    '^SURFACE lane\.kagi: progressing ' \
    'launch_epoch=1699998000 age_s=2000'

  FX="$work/fx/sil-bad-ts"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root/kagi-shokunin"
  # A launch line whose timestamp cannot be parsed is an unreadable input, not a
  # licence to guess an epoch: unavailable, never silent, never zero-age.
  printf '%s launch kagi round=7 pid=4242\n' '2026-10-15T99:99:99+00:00' >> "$FX/ufo/watchdog.log"
  EXTRA_ENV=(MORI_LANE_SILENCE_S=900)
  check 'silence: unparseable launch ts -> unavailable' 0 CLEAN \
    '^SURFACE lane\.kagi: unavailable ' \
    'reason=launch-ts-unparseable'

  FX="$work/fx/sil-report-closed"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root/kagi-shokunin"
  printf '%s launch kagi round=7 pid=4242\n' "$(ts_iso $((PIN_NOW - 2000)))" >> "$FX/ufo/watchdog.log"
  # Report present at HEAD and its newest path commit is in (launch, NOW] =>
  # closed, so the subject commit below must NOT be graded: closure wins.
  printf 0 > "$FX/stub/git-cat-file.rc"
  printf '%s\n' "1699998600" > "$FX/stub/git-log1"
  printf '%s\n' "1699998700 kagi-shokunin <kagi@shokunin.local>" > "$FX/stub/git-log"
  EXTRA_ENV=(MORI_LANE_SILENCE_S=900)
  check 'silence: committed report in window -> not-open' 0 CLEAN \
    '^SURFACE lane\.kagi: not-open ' \
    'basis=row-6'

  # --- r4: close tracking is per anchor round ---------------------------------
  # r3 remembered only the LAST close line anywhere, so an r5 close after an r7
  # close erased the r7 close and the closed r7 anchor graded silent (critic
  # defect 1; re-measured at fe22a14f). File order + anchor round decide.
  FX="$work/fx/sil-close-out-of-order"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root/kagi-shokunin"
  printf '%s launch kagi round=7 pid=4242\n' "$(ts_iso $((PIN_NOW - 2000)))" >> "$FX/ufo/watchdog.log"
  printf '%s complete kagi round=7; respawning\n' "$(ts_iso $((PIN_NOW - 1900)))" >> "$FX/ufo/watchdog.log"
  # A later-file-order close for an OLDER round must not erase the r7 close.
  printf '%s complete kagi round=5; respawning\n' "$(ts_iso $((PIN_NOW - 1800)))" >> "$FX/ufo/watchdog.log"
  EXTRA_ENV=(MORI_LANE_SILENCE_S=900)
  check 'silence: close r7 then close r5 -> r7 anchor stays closed' 0 CLEAN \
    '^SURFACE lane\.kagi: not-open ' \
    'basis=row-4' \
    'reason=ledger-close round=7'

  FX="$work/fx/sil-close-other-round"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root/kagi-shokunin"
  # The complementary guard: a close for a DIFFERENT round must never close the
  # anchor, wherever it sits — closes are keyed on the anchor round.
  printf '%s launch kagi round=7 pid=4242\n' "$(ts_iso $((PIN_NOW - 2000)))" >> "$FX/ufo/watchdog.log"
  printf '%s complete kagi round=5; respawning\n' "$(ts_iso $((PIN_NOW - 1900)))" >> "$FX/ufo/watchdog.log"
  EXTRA_ENV=(MORI_LANE_SILENCE_S=900)
  check 'silence: close for another round does not close the anchor' 1 DRIFT \
    '^SURFACE lane\.kagi: silent ' \
    'FINDING LANE_SILENT'

  FX="$work/fx/sil-git-unreadable"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root/kagi-shokunin"
  printf '%s launch kagi round=7 pid=4242\n' "$(ts_iso $((PIN_NOW - 2000)))" >> "$FX/ufo/watchdog.log"
  printf 128 > "$FX/stub/git-rev-parse.rc"
  EXTRA_ENV=(MORI_LANE_SILENCE_S=900)
  check 'silence: git rc!=0 -> unavailable, never silent' 0 CLEAN \
    '^SURFACE lane\.kagi: unavailable ' \
    'reason=git-unreadable'

  FX="$work/fx/sil-tree-unreadable"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root/kagi-shokunin/locked"
  printf '%s launch kagi round=7 pid=4242\n' "$(ts_iso $((PIN_NOW - 2000)))" >> "$FX/ufo/watchdog.log"
  # The r1 crash shape: the walk hits a subtree it cannot read and the nonzero
  # pipeline rc (pipefail) killed the census before any verdict. r2 grades
  # unavailable and still prints the verdict.
  chmod 000 "$FX/root/kagi-shokunin/locked"
  EXTRA_ENV=(MORI_LANE_SILENCE_S=900)
  check 'silence: unreadable subtree -> unavailable verdict, no crash' 0 CLEAN \
    '^SURFACE lane\.kagi: unavailable ' \
    'reason=tree-unreadable' \
    '^MORI_CENSUS: CLEAN '

  FX="$work/fx/wave-age-unreadable"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  mkdir -p "$FX/ufo/waves/wave-locked/nested"
  printf '{"wave":"wave-locked"}\n' > "$FX/ufo/waves/wave-locked/swarm-registry.json"
  printf '{"wave":"wave-locked"}\n' > "$FX/ufo/waves/wave-locked/dispatch.json"
  # backdate so a PROVEN age would exceed the threshold and fire; the walk fails
  # on the locked subdir, so the age is disclosed as unreadable and nothing fires
  find "$FX/ufo/waves/wave-locked" -type f -exec touch -d '@1600000000' {} + 2>/dev/null || true
  chmod 000 "$FX/ufo/waves/wave-locked/nested"
  EXTRA_ENV=(MORI_WAVE_UNSETTLED_S=900)
  SKIP_FRESHEN=1
  check 'waves: unreadable wave age -> no crash, no false finding' 0 CLEAN \
    '^SURFACE waves: ok' \
    'age_unreadable=1'
  SKIP_FRESHEN=0

  FX="$work/fx/cgroup-unavail"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  rm -f "$FX/cgroup/memory.events"
  check 'clean: CGROUP_UNAVAILABLE is not DRIFT' 0 CLEAN \
    'FINDING CGROUP_UNAVAILABLE' \
    '^SURFACE cgroup: unavailable' \
    '^MORI_CENSUS: CLEAN '

  FX="$work/fx/journal-empty-ok"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  : > "$FX/stub/journal"
  check 'clean: empty journal' 0 CLEAN \
    '^SURFACE journal\.user: ok .*kernel_oom_notice=0 .*oomd_notice=0 .*coredump_notice=0' \
    '^SURFACE journal\.system: ok .*kernel_oom_notice=0 .*oomd_notice=0 .*coredump_notice=0' \
    '^SURFACE journal\.user: ok .*boot=0123456789abcdef0123456789abcdef'

  # --- r7 coverage cases: the four r2 surface gaps ----------------------------
  # Each probe gets a firing case and a near-miss case, and every case here is
  # driven through the same fixture env as the rest of the suite (no case
  # branches on fixture shape; the probe reads the same fields live).

  # Gap 1 — tmux relevance. Two sessions: one fleet pane (cwd under the fixture
  # fleet root), one foreign pane. The rule must separate them and the foreign
  # one must be NAMED, not merely counted.
  FX="$work/fx/tmux-mixed"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf 'fx_session: 1 windows\nother_session: 1 windows\n' > "$FX/stub/tmux"
  printf 'fx_session\t%s\nother_session\t/srv/other\n' "$FX/root" > "$FX/stub/tmux-panes"
  check 'tmux: fleet vs foreign pane classification' 0 CLEAN \
    'relevant=1 foreign=1 unclassified=0' \
    'FINDING TMUX_FOREIGN_SESSION .*session=other_session' \
    '^MORI_CENSUS: CLEAN '

  # The count-only shape the frozen oracle's stub answers with (no tab): pane
  # data is absent, so relevance is DISCLOSED as unavailable rather than
  # guessed foreign, and the session count is still reported.
  FX="$work/fx/tmux-nopane"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf 'fx_session: 1 windows\n' > "$FX/stub/tmux-panes"
  check 'tmux: no pane data -> relevance unavailable, count intact' 0 CLEAN \
    '^SURFACE tmux: ok' \
    'sessions=1' \
    'relevance=unavailable reason=no-pane-data' \
    'FINDING TMUX_RELEVANCE_UNAVAILABLE' \
    '^MORI_CENSUS: CLEAN '

  FX="$work/fx/tmux-panerc"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf 1 > "$FX/stub/tmux-panes.rc"
  check 'tmux: pane probe rc!=0 -> relevance unavailable' 0 CLEAN \
    'relevance=unavailable reason=panes-rc=1' \
    '^MORI_CENSUS: CLEAN '

  # Gap 2 — memory pressure. PSI: above the local threshold fires, just below it
  # does not (the direction is proved, not assumed).
  FX="$work/fx/mem-psi-high"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf 'some avg10=25.00 avg60=1.00 avg300=0.10 total=900\nfull avg10=12.00 avg60=0.50 avg300=0.05 total=400\n' > "$FX/cgroup/memory.pressure"
  check 'drift: MEM_PRESSURE_HIGH at local PSI threshold' 1 DRIFT \
    'FINDING MEM_PRESSURE_HIGH .*threshold_avg10=10 threshold_label=local' \
    'psi_some_avg10=25.00' \
    'psi_full_avg10=12.00'

  FX="$work/fx/mem-psi-under"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf 'some avg10=9.99 avg60=1.00 avg300=0.10 total=900\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\n' > "$FX/cgroup/memory.pressure"
  check 'clean: PSI just under the local threshold does not fire' 0 CLEAN \
    'psi_some_avg10=9.99' \
    '^MORI_CENSUS: CLEAN '

  # Fill arm with a numeric slice limit, both sides of the labeled-local pct.
  FX="$work/fx/mem-fill-high"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf '1000\n' > "$FX/cgroup/memory.max"
  printf '900\n' > "$FX/cgroup/memory.current"
  check 'drift: MEM_FILL_HIGH vs numeric cgroup limit' 1 DRIFT \
    'FINDING MEM_FILL_HIGH .*scope=cgroup mem_fill_pct=90' \
    'mem_fill_pct=90 mem_fill_scope=cgroup'

  FX="$work/fx/mem-fill-under"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf '1000\n' > "$FX/cgroup/memory.max"
  printf '100\n' > "$FX/cgroup/memory.current"
  check 'clean: cgroup fill under threshold does not fire' 0 CLEAN \
    'mem_fill_pct=10 mem_fill_scope=cgroup' \
    '^MORI_CENSUS: CLEAN '

  # Host-ram arm (this host's shape: memory.max is the literal `max`).
  FX="$work/fx/mem-avail-low"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf 'MemTotal: 32000000 kB\nMemAvailable: 2000000 kB\n' > "$FX/meminfo"
  check 'drift: MEM_AVAIL_LOW at unlimited-slice host scope' 1 DRIFT \
    'FINDING MEM_AVAIL_LOW .*host_mem_avail_pct=6 floor_pct=10 threshold_label=local' \
    'mem_fill_scope=host-ram host_mem_avail_pct=6'

  # Gap 3 — disk write rate. The rate is arithmetic on the fixture counters
  # (20000 sectors * 512 / 500 s = 20480 Bps): a wrong divisor or a wrong
  # diskstats field fails this case, so it proves the math and not just that a
  # number appeared.
  FX="$work/fx/disk-io"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf '500.00 1000.00\n' > "$FX/uptime"
  check 'disk: since-boot write average from diskstats' 0 CLEAN \
    'io_basis=since-boot io_avg_since_boot=fx:20480Bps/500s' \
    '^MORI_CENSUS: CLEAN '

  FX="$work/fx/disk-io-nodev"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf '8 0 sdz 1 0 1 0 1 0 1 0 0 0 0 0 0\n' > "$FX/diskstats"
  check 'disk: device missing from diskstats -> unmeasured disclosed' 0 CLEAN \
    'io_avg_unavailable=fx:device-not-in-diskstats' \
    'FINDING DISK_IO_UNMEASURED' \
    '^MORI_CENSUS: CLEAN '

  FX="$work/fx/disk-io-nouptime"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  rm -f "$FX/uptime"
  check 'disk: missing uptime -> rate unavailable, not zero' 0 CLEAN \
    'io_avg_since_boot=none' \
    'io_avg_unavailable=fx:no-uptime' \
    'FINDING DISK_IO_UNMEASURED'

  # Gap 4 — state_rounds values vs the watchdog's own record. LAG and AHEAD are
  # INFO by design, so both cases must stay CLEAN while the inconsistency is
  # visible in the row and as a finding.
  FX="$work/fx/state-lag"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf '5\n' > "$FX/ufo/state/kagi.round"
  printf '%s launch kagi round=7 pid=4242\n' "$(ts_iso $((PIN_NOW - 2000)))" >> "$FX/ufo/watchdog.log"
  check 'watchdog: state value below ledger launch -> LAG info' 0 CLEAN \
    'FINDING WATCHDOG_STATE_LAG .*lane=kagi state_round=5 ledger_round=7' \
    'state_rounds_max=5 state_lag=1 state_ahead=0 state_cmp=1' \
    '^MORI_CENSUS: CLEAN '

  FX="$work/fx/state-ahead"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf '9\n' > "$FX/ufo/state/kagi.round"
  printf '%s launch kagi round=7 pid=4242\n' "$(ts_iso $((PIN_NOW - 2000)))" >> "$FX/ufo/watchdog.log"
  check 'watchdog: state value above ledger launch -> AHEAD info' 0 CLEAN \
    'FINDING WATCHDOG_STATE_AHEAD .*lane=kagi state_round=9 ledger_round=7' \
    'state_rounds_max=9 state_lag=0 state_ahead=1 state_cmp=1' \
    '^MORI_CENSUS: CLEAN '

  FX="$work/fx/state-match"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf '7\n' > "$FX/ufo/state/kagi.round"
  printf '%s launch kagi round=7 pid=4242\n' "$(ts_iso $((PIN_NOW - 2000)))" >> "$FX/ufo/watchdog.log"
  check 'clean: matching state and ledger compare, no mismatch finding' 0 CLEAN \
    'state_rounds_max=7 state_lag=0 state_ahead=0 state_cmp=1 state_val_unreadable=0' \
    '^MORI_CENSUS: CLEAN '

  FX="$work/fx/state-val-unreadable"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  chmod 000 "$FX/ufo/state/kagi.round"
  check 'watchdog: unreadable round value counted, no crash' 0 CLEAN \
    'state_val_unreadable=1' \
    'state_rounds=1' \
    '^MORI_CENSUS: CLEAN '

  # --- r8 cases: symlink/dir `*.round` entries, tmux freshness, mem peak --------
  # Each new arm gets a positive case (the disclosure appears with the right
  # reason) and, where a wrong implementation could still pass it, a negative
  # one (the near-miss value must NOT be read/counted the way the positive case
  # would allow).

  # A symlink named `*.round` used to be INVISIBLE (the r7 walk filtered on
  # -type f). It must now be counted WITH its reason — and it must NOT be
  # followed: the link target here holds `99`, so a probe that followed it would
  # report state_rounds_max=99 instead of the real file's 7.
  FX="$work/fx/state-symlink"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf '7\n' > "$FX/ufo/state/kagi.round"
  printf '99\n' > "$FX/vault"
  ln -s "$FX/vault" "$FX/ufo/state/zz.round"
  check 'watchdog: symlink *.round counted with reason, never followed' 0 CLEAN \
    'state_rounds=1 state_rounds_max=7' \
    'state_val_unreadable=1 state_val_unread_reasons=file:0 symlink:1 dir:0 other:0' \
    'FINDING WATCHDOG_STATE_ENTRY_UNREADABLE .*reason=symlink-not-followed' \
    '^MORI_CENSUS: CLEAN '

  # A directory named `*.round`: not a value, not a crash, counted with reason.
  FX="$work/fx/state-dirfield"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf '7\n' > "$FX/ufo/state/kagi.round"
  mkdir -p "$FX/ufo/state/yy.round"
  check 'watchdog: directory *.round counted with reason' 0 CLEAN \
    'state_rounds=1 state_rounds_max=7' \
    'state_val_unreadable=1 state_val_unread_reasons=file:0 symlink:0 dir:1 other:0' \
    'FINDING WATCHDOG_STATE_ENTRY_UNREADABLE .*reason=is-directory' \
    '^MORI_CENSUS: CLEAN '

  # All four classes at once: an unreadable regular value, a symlink, a
  # directory and a non-regular (fifo) entry. The counts must partition by class
  # and the total must equal their sum; state_rounds keeps its meaning (regular
  # entries, readable or not) so the pre-r8 rows stay comparable.
  FX="$work/fx/state-kinds"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf '7\n' > "$FX/ufo/state/kagi.round"
  printf '99\n' > "$FX/vault"
  ln -s "$FX/vault" "$FX/ufo/state/zz.round"
  mkdir -p "$FX/ufo/state/yy.round"
  mkfifo "$FX/ufo/state/ww.round"
  printf '4\n' > "$FX/ufo/state/xx.round"
  chmod 000 "$FX/ufo/state/xx.round"
  check 'watchdog: all four non-value classes counted by reason' 0 CLEAN \
    'state_rounds=2 state_rounds_max=7' \
    'state_val_unreadable=4 state_val_unread_reasons=file:1 symlink:1 dir:1 other:1' \
    'FINDING WATCHDOG_STATE_ENTRY_UNREADABLE .*reason=non-regular' \
    '^MORI_CENSUS: CLEAN '

  # tmux freshness, positive: the baseline fixture's pinned activity equals NOW,
  # so the fleet session is fresh, exactly one session is probed, none idle.
  FX="$work/fx/tmux-fresh"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  check 'tmux: fresh fleet session -> probed, not idle' 0 CLEAN \
    'freshness=ok probed=1 idle=0 freshness_unavailable=0 idle_warn_s=3600' \
    '^MORI_CENSUS: CLEAN '

  # tmux freshness, idle arm — and the RELEVANCE filter: two sessions exist, but
  # only the fleet-relevant one is probed (probed=1 proves the foreign session
  # was not), and the idle finding names the fleet session.
  FX="$work/fx/tmux-idle"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf 'fx_session: 1 windows\nother_session: 1 windows\n' > "$FX/stub/tmux"
  printf 'fx_session\t%s\nother_session\t/srv/other\n' "$FX/root" > "$FX/stub/tmux-panes"
  printf '1699900000\n' > "$FX/stub/tmux-activity"
  check 'tmux: idle fleet session -> INFO finding, foreign session not probed' 0 CLEAN \
    'FINDING TMUX_SESSION_IDLE .*session=fx_session idle_s=100000 threshold_s=3600 threshold_label=local' \
    'freshness=ok probed=1 idle=1 freshness_unavailable=0' \
    '^MORI_CENSUS: CLEAN '

  # The three unavailable arms: a probe that answers junk (a stub/foreign server
  # shape), a probe that fails, and no bound binary at all. None may produce
  # idle=0; each names its reason.
  FX="$work/fx/tmux-act-junk"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf 'fx_session: 1 windows\n' > "$FX/stub/tmux-activity"
  check 'tmux: non-integer activity -> freshness unavailable, never idle=0' 0 CLEAN \
    'freshness=unavailable probed=0 idle=0 freshness_unavailable=1' \
    'FINDING TMUX_FRESHNESS_UNAVAILABLE .*reason=unparseable-probe-output' \
    '^MORI_CENSUS: CLEAN '

  FX="$work/fx/tmux-act-rc"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf 1 > "$FX/stub/tmux-activity.rc"
  check 'tmux: activity probe rc!=0 -> freshness unavailable reason=rc-1' 0 CLEAN \
    'freshness=unavailable probed=0 idle=0 freshness_unavailable=1 idle_warn_s=3600 reason=rc-1' \
    'FINDING TMUX_FRESHNESS_UNAVAILABLE .*reason=rc-1' \
    '^MORI_CENSUS: CLEAN '

  # HANG GUARD: the stub sleeps 3 s; the census bounds the call at 1 s (env) and
  # returns rc 124 as unavailable. The sleeping binary lives ONLY under the /tmp
  # fixture tree (and redirects its own fds, so the command substitution cannot
  # block on an orphan); a broken bound would either hang this case or answer
  # reason=unparseable instead of rc-124, both failing.
  FX="$work/fx/tmux-act-sleep"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf '3\n' > "$FX/stub/tmux-activity-sleep"
  EXTRA_ENV=(MORI_TMUX_TIMEOUT_S=1)
  check 'tmux: sleeping probe is bounded -> rc-124 unavailable, no hang' 0 CLEAN \
    'freshness=unavailable probed=0 idle=0 freshness_unavailable=1 idle_warn_s=3600 reason=rc-124' \
    'FINDING TMUX_FRESHNESS_UNAVAILABLE .*reason=rc-124' \
    '^MORI_CENSUS: CLEAN '

  FX="$work/fx/tmux-act-notimeout"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  EXTRA_ENV=(MORI_TIMEOUT_BIN=/nonexistent/timeout)
  check 'tmux: no timeout binary -> freshness refused, never run unbounded' 0 CLEAN \
    'freshness=unavailable probed=0 idle=0 freshness_unavailable=1 idle_warn_s=3600 reason=no-timeout-bin' \
    'FINDING TMUX_FRESHNESS_UNAVAILABLE .*reason=no-timeout-bin' \
    '^MORI_CENSUS: CLEAN '

  # r8 memory arm: the scope high-watermark is free and shape-gated. The anchor
  # is the scope dir mtime, pinned in the fixture, so the row is deterministic.
  FX="$work/fx/mem-peak"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf '28801970176\n' > "$FX/cgroup/memory.peak"
  touch -d '@1699999000' "$FX/cgroup"
  check 'cgroup: scope high-watermark read with its instance anchor' 0 CLEAN \
    'mem_peak=28801970176 mem_peak_source=ok mem_peak_anchor=1699999000' \
    '^MORI_CENSUS: CLEAN '

  # Negative: a pinned peak path carrying foreign bytes (not an integer) must be
  # REFUSED, not echoed — the same print-safety rule the PSI and max readers hold.
  FX="$work/fx/mem-peak-junk"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf 'token-looking-secret-value\n' > "$FX/cgroup/memory.peak"
  check 'cgroup: non-integer peak refused, bytes never echoed' 0 CLEAN \
    'mem_peak=unavailable mem_peak_source=shape-refused' \
    '^MORI_CENSUS: CLEAN '

  # --- r10 drift-pin cases -----------------------------------------------------
  # The carried freshness item: --pin records a canonical baseline of the
  # census's own output; --drift re-runs and names any changed non-volatile
  # field. Five arms on ONE deterministic fixture: clean round-trip, volatile
  # churn (a new ts with moved ages) staying clean, two injected source
  # regressions (a changed field, a removed finding), and the missing-baseline
  # contract. The mutants are /tmp copies of THIS script run through the real
  # --drift path, so the graded comparison is the shipped one. The fixture is
  # pinned with a stale watchdog log AND no process match, so two warn findings
  # (WATCHDOG_STALE, WATCHDOG_ABSENT) are in the baseline; the removal mutant
  # isolates one line without flipping the roll (a roll flip would legitimately
  # also name VERDICT, which this arm must not need).
  FX="$work/fx/drift-pin"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root/kagi-shokunin"
  : > "$FX/stub/pgrep"; printf 1 > "$FX/stub/pgrep.rc"
  PD_DIR="$work/dp"; mkdir -p "$PD_DIR"
  PIN_NOW=1700000000
  touch -d "@$((PIN_NOW - 1000))" "$FX/ufo/watchdog.log" 2>/dev/null || true
  touch -d "@$PIN_NOW" "$FX/lanes/kagi-shokunin/LOG.md" 2>/dev/null || true
  find "$FX/ufo/waves" -type f -exec touch -d "@$PIN_NOW" {} + 2>/dev/null || true
  dp_before=$(fx_hash "$FX")

  pd_run "$SELF" "$PD_DIR/pin.out" --pin "$PD_DIR/base.txt"
  pd_check 'drift: --pin writes a baseline' "$PD_RC" 0 "$PD_DIR/pin.out" '^MORI_PIN: ok path='
  # The baseline must carry its own contract or the drift side can never be
  # audited: the volatile list in the header, the marker, and the canonical
  # header line of the census output itself.
  pd_check 'drift: baseline records the volatile contract' 0 0 "$PD_DIR/base.txt" \
    '^# volatile_fields=ts ' \
    '^# --- canonical output follows ---$' \
    '^mori-census '

  pd_run "$SELF" "$PD_DIR/d1.out" --drift "$PD_DIR/base.txt"
  pd_check 'drift: pin -> drift is clean' "$PD_RC" 0 "$PD_DIR/d1.out" '^MORI_DRIFT: none$'

  # Volatile churn: the same fixture pinned, then drifted at NOW+300 s — every
  # ts/age is new but masked, so the report must stay clean. (The fixture
  # mtimes stay at the pin clock, so the ages really do move.)
  PIN_NOW=1700000300
  pd_run "$SELF" "$PD_DIR/d2.out" --drift "$PD_DIR/base.txt"
  pd_check 'drift: volatile churn (new ts, moved ages) stays clean' "$PD_RC" 0 "$PD_DIR/d2.out" '^MORI_DRIFT: none$'
  PIN_NOW=1700000000

  # Injected source regression 1: one emitted non-volatile value changes
  # (disk warn_pct 85 -> 86). The mutant is a /tmp copy of THIS script; the
  # field must be named, alone.
  sed 's/warn_pct=[$]DISK_WARN_PCT/warn_pct=$((DISK_WARN_PCT+1))/' "$SELF" > "$PD_DIR/mutant-field.sh"
  if cmp -s "$SELF" "$PD_DIR/mutant-field.sh"; then
    bad 'drift: one-field regression (mutation anchor no longer matches the source)'
  else
    pd_run "$PD_DIR/mutant-field.sh" "$PD_DIR/d3.out" --drift "$PD_DIR/base.txt"
    pd_check 'drift: one-field regression names the field' "$PD_RC" 1 "$PD_DIR/d3.out" '^MORI_DRIFT: warn_pct$'
  fi

  # Injected source regression 2: a finding disappears (line-level detection —
  # the removed line is named by its id, not absorbed silently).
  sed 's/emit_finding WATCHDOG_ABSENT warn/:/' "$SELF" > "$PD_DIR/mutant-finding.sh"
  if cmp -s "$SELF" "$PD_DIR/mutant-finding.sh"; then
    bad 'drift: finding-removal regression (mutation anchor no longer matches the source)'
  else
    pd_run "$PD_DIR/mutant-finding.sh" "$PD_DIR/d4.out" --drift "$PD_DIR/base.txt"
    pd_check 'drift: removed finding is named' "$PD_RC" 1 "$PD_DIR/d4.out" '^MORI_DRIFT: -FINDING:WATCHDOG_ABSENT$'
  fi

  # Contract: a missing baseline is exit 2 with a diagnostic, never a verdict.
  pd_run "$SELF" "$PD_DIR/d5.out" --drift "$PD_DIR/no-such-baseline.txt"
  pd_check 'drift: missing baseline exits 2 with a diagnostic' "$PD_RC" 2 "$PD_DIR/d5.out" 'baseline missing'
  # Contract: the recorded volatile list is compared too — a baseline pinned
  # under a different list is drifting even when this run's output is not.
  sed 's/^# volatile_fields=.*/# volatile_fields=ts/' "$PD_DIR/base.txt" > "$PD_DIR/base-oldlist.txt"
  pd_run "$SELF" "$PD_DIR/d6.out" --drift "$PD_DIR/base-oldlist.txt"
  pd_check 'drift: changed volatile contract is reported' "$PD_RC" 1 "$PD_DIR/d6.out" '^MORI_DRIFT: volatile_fields$'
  fx_no_mutation "$FX" "$dp_before"

  check_cli 'cli: unknown arg exit 2' 2 'mori-census:' -- --bogus
  check_cli 'cli: --help exit 0' 0 'usage: mori-census' -- --help
  check_cli 'cli: --pin without a path exits 2' 2 'mori-census:' -- --pin
  check_cli 'cli: --drift without a path exits 2' 2 'mori-census:' -- --drift

  printf 'MORI_CENSUS_SELFTEST: %s (%d cases, %d passed, %d failed)\n' \
    "$([ "$FAIL" -eq 0 ] && printf PASS || printf FAIL)" "$((PASS + FAIL))" "$PASS" "$FAIL"
  [ "$FAIL" -eq 0 ]
}

# ---- main -------------------------------------------------------------------
main() {
  local selftest=0 pin_path='' drift_path=''
  while [ $# -gt 0 ]; do
    case "$1" in
      --selftest) selftest=1; shift ;;
      --pin) [ $# -ge 2 ] || die_usage '--pin requires a baseline path'; pin_path=$2; shift 2 ;;
      --drift) [ $# -ge 2 ] || die_usage '--drift requires a baseline path'; drift_path=$2; shift 2 ;;
      --help|-h) usage; exit 0 ;;
      verify|--verify) shift ;; # accepted alias
      *) die_usage "unknown argument: $1" ;;
    esac
  done
  if [ "$selftest" -eq 1 ]; then
    run_selftest
    return
  fi
  if [ -n "$pin_path" ]; then
    run_pin "$pin_path"
    return
  fi
  if [ -n "$drift_path" ]; then
    run_drift "$drift_path"
    return
  fi
  run_census live
}

main "$@"
