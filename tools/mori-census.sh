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
#             (count, max, and ledger-vs-state mismatch — r7)
#   waves     .ufo/waves/* settlement (registry/dispatch/run × results/closeout)
#   journal   journalctl --user -b kill/OOM class counts (this boot)
#   cgroup    memory.events / memory.current / memory.pressure / memory.max
#             (user slice; r7 adds PSI + fill/avail grading, labeled local)
#   disk      df runway on fleet root + /tmp + optional scratch; r7 adds a
#             since-boot write average per target device (/proc/diskstats)
#   silence   per-lane launch/closure/authorship grading (PROTOCOL.md:153-168;
#             contract corpus/knowledge/silence-grading-r2.md) — states silent |
#             progressing | progressing-weak | young | not-open | unavailable
#   tmux      optional session list; r7 classifies every session fleet-relevant
#             vs foreign by pane current path under the fleet root (absence =
#             unavailable, not DRIFT)
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
#                      DEFERRAL: the INSTANTANEOUS write rate (two-sample
#                      delta) is NOT implemented; precondition to lift it —
#                      measure the wall-time a second sample adds and record it
#                      in the round note. This average is the "measured write
#                      rate" the r2 note required before touching 85/95.
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
# Live mode writes nothing. --selftest writes only under
# /tmp/mori-census-selftest.XXXXXX and asserts the fixture tree is unchanged.
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
#   MORI_DISKSTATS       default /proc/diskstats (write-rate counters; r7)
#   MORI_UPTIME          default /proc/uptime (since-boot divisor; r7)
#   MORI_MEMINFO         default /proc/meminfo
#   MORI_DF_BIN          default df
#   MORI_PGREP_BIN       default pgrep
#   MORI_JOURNALCTL_BIN  default journalctl
#   MORI_TMUX_BIN        default tmux
#   MORI_GIT_BIN         default git
#   MORI_DISK_TARGETS    space-separated paths for df (default: ROOT /tmp)
#   MORI_WATCHDOG_STALE_S MORI_WAVE_UNSETTLED_S MORI_DISK_WARN_PCT
#   MORI_DISK_CRIT_PCT    MORI_LANE_SILENCE_S
#   MORI_MEM_PSI_WARN_AVG10 MORI_MEM_FILL_WARN_PCT MORI_MEM_AVAIL_MIN_PCT
#                        labeled-local memory thresholds (round-7 block above)
#   MORI_TMUX_SCOPE_ROOT fleet root for session classification (default $ROOT)
#   MORI_ROSTER_LANES    space-separated lane ids for silence grading
#   MORI_NOW_EPOCH       pin "now" (selftest)
#   MORI_FIXTURE         selftest marker (optional)
#
# Finding ids (stable compare contract):
#   WATCHDOG_ABSENT WATCHDOG_STALE WATCHDOG_LOG_UNAVAILABLE
#   WATCHDOG_PROBE_UNAVAILABLE WATCHDOG_STATE_LAG WATCHDOG_STATE_AHEAD
#   WAVE_UNSETTLED_AGE
#   OOM_KILL_JOURNAL KILL_SIGNAL_JOURNAL SEGFAULT_JOURNAL UNIT_FAILURE_JOURNAL
#   CGROUP_OOM_KILL CGROUP_UNAVAILABLE MEM_PRESSURE_HIGH MEM_FILL_HIGH
#   MEM_AVAIL_LOW
#   DISK_LOW DISK_CRITICAL DISK_UNAVAILABLE DISK_IO_UNMEASURED
#   LANE_SILENT
#   TMUX_FOREIGN_SESSION TMUX_RELEVANCE_UNAVAILABLE
#
set -euo pipefail
# The journal is held in a shell variable (CAP_OUT) and the raw text can carry
# token-shaped lines (measured: 245 1password lines in this boot's user journal).
# Never trace: `bash -x` would print that variable, and the published
# `cmd=journalctl --user -b --no-pager` re-run prints MESSAGE by design.
set +o xtrace

VERSION=census-r4
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
DISKSTATS=${MORI_DISKSTATS:-/proc/diskstats}
UPTIME_FILE=${MORI_UPTIME:-/proc/uptime}
MEMINFO=${MORI_MEMINFO:-/proc/meminfo}
DF_BIN=${MORI_DF_BIN:-df}
PGREP_BIN=${MORI_PGREP_BIN:-pgrep}
JOURNALCTL_BIN=${MORI_JOURNALCTL_BIN:-journalctl}
TMUX_BIN=${MORI_TMUX_BIN:-tmux}
GIT_BIN=${MORI_GIT_BIN:-git}
DISK_TARGETS=${MORI_DISK_TARGETS:-"$ROOT /tmp"}
TMUX_SCOPE_ROOT=${MORI_TMUX_SCOPE_ROOT:-$ROOT}
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
ROSTER_LANES=${MORI_ROSTER_LANES:-"protocol aggregator kasegi kengaku kake kumitate kotoba kagi kama"}

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
usage: mori-census.sh [--selftest] [--help]

  (no flags)   live read-only census over fleet/host observability surfaces
  --selftest   hermetic fixture-tree proof (writes only under
               /tmp/mori-census-selftest.*); exit 0 pass, 1 fail
  --help       this text

Verdict: MORI_CENSUS: CLEAN|DRIFT (findings=N drift=M unavailable=U surfaces=S)
Exit:    0 CLEAN | 1 DRIFT | 2 setup/usage
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

have() { command -v "$1" >/dev/null 2>&1; }

cap() { # run read-only; capture stdout+stderr + rc without set -e trip
  set +e
  CAP_OUT=$("$@" 2>&1)
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
  LEDGER=''; LEDGER_RC=1
  if [ -d "$STATE_DIR" ]; then
    cap find "$STATE_DIR" -maxdepth 1 -type f -name '*.round'
    if [ "$CAP_RC" -eq 0 ]; then
      # The walk output is copied BEFORE load_ledger runs: load_ledger (like
      # every cap caller) overwrites CAP_OUT, and reading the state list out of
      # CAP_OUT after that call iterates the ledger instead of the state files
      # (measured live: 402 unreadable "values" = the ledger's line count).
      state_list=$CAP_OUT
      state_n=$(printf '%s\n' "$state_list" | grep -c . || true)
      load_ledger
      while IFS= read -r sf; do
        [ -n "$sf" ] || continue
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
  # r2 fields (`state_rounds=<n>`) with the r7 value fields appended.
  state_field="state_rounds=$state_n state_rounds_max=$state_max state_lag=$state_lag state_ahead=$state_ahead state_cmp=$state_cmp state_val_unreadable=$state_unread_vals"
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

# ---- surface: journal kill/OOM ----------------------------------------------
# Classes counted (content is evidence; never acted on):
#   oom_kill      Out of memory|oom-kill|oom_reaper|Killed process
#   kill_signal   status=9/KILL|Failed with result 'signal'|SIGKILL
#   segfault      segfault|general protection fault
#   unit_failure  Failed with result|Unit entered failed state
# DRIFT on oom_kill>0 or kill_signal>0 (mint demand). segfault/unit_failure = info.
probe_journal() {
  local cmd="$JOURNALCTL_BIN --user -b --no-pager"
  local text='' rc=0
  local c_oom=0 c_kill=0 c_seg=0 c_unit=0
  local st=ok

  if ! have "$JOURNALCTL_BIN" && [ ! -x "$JOURNALCTL_BIN" ]; then
    emit_surface journal unavailable "cmd=$cmd; journalctl=missing; ts=$TS_UTC"
    return 0
  fi

  cap "$JOURNALCTL_BIN" --user -b --no-pager
  rc=$CAP_RC
  text=$CAP_OUT
  # rc 0/1 both acceptable (1 can mean empty on some builds); other = unavailable
  if [ "$rc" -gt 1 ]; then
    emit_surface journal unavailable "cmd=$cmd; rc=$rc; ts=$TS_UTC"
    return 0
  fi

  c_oom=$(printf '%s\n' "$text" | grep -ciE 'Out of memory|oom-kill|oom_reaper|Killed process' || true)
  c_kill=$(printf '%s\n' "$text" | grep -ciE 'status=9/KILL|Failed with result .signal|SIGKILL' || true)
  # Segfaults are a STRUCTURED field (COREDUMP_SIGNAL=11), not the word
  # "segfault": a text grep over the user journal returns 0 while the same
  # journal holds 656 signal-11 entries (measured 2026-10-15). Count the text form
  # first (fixtures drive it), then take the JSON count as an ADDITIONAL signal on
  # a live host — never a replacement, so a stub journalctl cannot silence it.
  c_seg=$(printf '%s\n' "$text" | grep -ciE 'segfault|general protection fault' || true)
  if [ -z "${MORI_FIXTURE:-}" ]; then
    c_seg_json=$(cap "$JOURNALCTL_BIN" --user -b --no-pager -o json COREDUMP_SIGNAL=11 2>/dev/null; printf '%s' "${CAP_OUT:-}" | grep -c 'COREDUMP_SIGNAL' || true)
    case "$c_seg_json" in ''|*[!0-9]*) c_seg_json=0 ;; esac
    if [ "$c_seg_json" -gt "$c_seg" ] 2>/dev/null; then c_seg=$c_seg_json; fi
  fi
  # Unit failures are tsukuroi's domain unless the unit is a FLEET unit: the
  # unscoped grep matched desktop daemons (measured: pipewire-pulse.service
  # core-dump), which is OS triage, not fleet health.
  c_unit=$(printf '%s\n' "$text" | grep -ciE 'Failed with result|Unit entered failed state' || true)
  c_unit_fleet=$(printf '%s\n' "$text" | grep -iE 'Failed with result|Unit entered failed state' | grep -ciE 'shokunin|ufo-sighting|tmux-spawn|the-tick|fleet' || true)

  if [ "$c_oom" -gt 0 ]; then
    emit_finding OOM_KILL_JOURNAL crit "class=oom_kill count=$c_oom boot=current scope=user"
    st=drift
  fi
  if [ "$c_kill" -gt 0 ]; then
    emit_finding KILL_SIGNAL_JOURNAL warn "class=kill_signal count=$c_kill boot=current scope=user"
    st=drift
  fi
  if [ "$c_seg" -gt 0 ]; then
    emit_finding SEGFAULT_JOURNAL info "class=segfault count=$c_seg boot=current scope=user"
  fi
  if [ "$c_unit_fleet" -gt 0 ]; then
    emit_finding UNIT_FAILURE_JOURNAL info "class=unit_failure count=$c_unit_fleet scope=fleet-units"
  fi
  if [ "$c_unit" -gt "$c_unit_fleet" ] 2>/dev/null; then
    emit_finding UNIT_FAILURE_OUT_OF_SCOPE info "class=unit_failure count=$((c_unit - c_unit_fleet)) note=non-fleet units (desktop/OS) — tsukuroi owns these"
  fi

  emit_surface journal "$st" "cmd=$cmd; oom_kill=$c_oom kill_signal=$c_kill segfault=$c_seg unit_failure=$c_unit rc=$rc; ts=$TS_UTC"
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
  emit_surface cgroup "$st" "cmd=$cmd; oom_kill=$oom_kill oom=${oom:-?} high=${high:-?} max=${max:-?} current=${cur:-?}; local_oom_kill=${service_oom_kill:-unavailable} psi_some_avg10=${psi_some:-unavailable} psi_full_avg10=${psi_full:-unavailable} psi_source=$psi_state psi_warn_avg10=$MEM_PSI_WARN_AVG10 $fill_field; ts=$TS_UTC"
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
  emit_surface silence "$st" "cmd=$cmd; silent=$n_silent progressing=$n_prog progressing_weak=$n_weak young=$n_young not_open=$n_notopen unavailable=$n_unavail skipped=0 window_s=$LANE_SILENCE_S; ts=$TS_UTC"
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
  n=$(printf '%s\n' "$CAP_OUT" | grep -c . || true)

  declare -A SESS_CLASS=()
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
        "$TMUX_SCOPE_ROOT"|"$TMUX_SCOPE_ROOT"/*) SESS_CLASS[$sess]=fleet ;;
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

  if [ "$rel" = unavailable ]; then
    # Sessions were counted but not classified: disclose instead of implying a
    # classification that was never made.
    emit_finding TMUX_RELEVANCE_UNAVAILABLE info "session relevance unreadable reason=$reason probe=$TMUX_BIN list-panes -a sessions=$n unnoticed_but_counted"
    emit_surface tmux ok "cmd=$cmd; sessions=$n; relevance=unavailable reason=$reason rule=pane_cwd_under_fleet_root; ts=$TS_UTC"
  else
    emit_surface tmux ok "cmd=$cmd; sessions=$n; relevant=$n_fleet foreign=$n_foreign unclassified=$n_unclass rule=pane_cwd_under_fleet_root; ts=$TS_UTC"
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

# ---- hermetic selftest ------------------------------------------------------
run_selftest() {
  local bin FX PASS=0 FAIL=0
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
    out_of journal; exit "$(rc_of journal)" ;;
  df)
    # ignore args; emit fixture table
    out_of df; exit "$(rc_of df)" ;;
  tmux)
    # r7: the census asks two different questions — `tmux ls` (session count)
    # and `tmux list-panes -a -F ...` (pane cwd for relevance). Answer per
    # subcommand from $fx/stub/tmux[-panes]; an absent file is empty output
    # with rc 0, so the no-pane-data arm is drivable too.
    case " $* " in
      *" list-panes "*) out_of tmux-panes; exit "$(rc_of tmux-panes)" ;;
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
    # git answers per verb via stub/git-<verb>[.rc] (see the dispatcher above):
    # rev-parse / ls-files / cat-file / log / log1. Absent fixture files answer
    # empty output with rc 0.
    # lane file recent — touch in check with NOW
    printf 'x\n' > "$d/lanes/kagi-shokunin/LOG.md"
  }

  EXTRA_ENV=()
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
    set +e
    out=$(env -i \
      PATH="$bin:/usr/bin:/bin" \
      HOME="$work/home" \
      MORI_FIXTURE="$FX" \
      MORI_SHOKUNIN_ROOT="$FX/root" \
      MORI_UFO_DIR="$FX/ufo" \
      MORI_WATCHDOG_LOG="$FX/ufo/watchdog.log" \
      MORI_STATE_DIR="$FX/ufo/state" \
      MORI_WAVES_DIR="$FX/ufo/waves" \
      MORI_CGROUP_EVENTS="$FX/cgroup/memory.events" \
      MORI_CGROUP_SERVICE_EVENTS="$FX/cgroup/memory.events" \
      MORI_CGROUP_LOCAL_EVENTS="$FX/cgroup/memory.events" \
      MORI_CGROUP_CURRENT="$FX/cgroup/memory.current" \
      MORI_CGROUP_PRESSURE="$FX/cgroup/memory.pressure" \
      MORI_CGROUP_MAX="$FX/cgroup/memory.max" \
      MORI_MEMINFO="$FX/meminfo" \
      MORI_DISKSTATS="$FX/diskstats" \
      MORI_UPTIME="$FX/uptime" \
      MORI_DF_BIN="$bin/df" \
      MORI_PGREP_BIN="$bin/pgrep" \
      MORI_JOURNALCTL_BIN="$bin/journalctl" \
      MORI_TMUX_BIN="$bin/tmux" \
      MORI_GIT_BIN="$bin/git" \
      MORI_DISK_TARGETS="$FX/root" \
      MORI_ROSTER_LANES="kagi" \
      MORI_NOW_EPOCH="$env_now" \
      MORI_WATCHDOG_STALE_S=900 \
      MORI_WAVE_UNSETTLED_S=7200 \
      MORI_DISK_WARN_PCT=85 \
      MORI_DISK_CRIT_PCT=95 \
      MORI_LANE_SILENCE_S=7200 \
      "${EXTRA_ENV[@]+"${EXTRA_ENV[@]}"}" \
      bash "$SELF" 2>&1)
    rc=$?
    set -e
    if [ "$rc" -ne "$wrc" ]; then
      bad "$label: exit $rc want $wrc; tail=$(printf '%s' "$out" | tail -n3 | tr '\n' '|')"
    elif ! printf '%s\n' "$out" | grep -qE "^MORI_CENSUS: ${wverdict} "; then
      bad "$label: verdict want $wverdict; got=$(printf '%s\n' "$out" | grep '^MORI_CENSUS:' | head -n1)"
    elif printf '%s\n' "$out" | grep -qE 'integer expected|line [0-9]+: \[: '; then
      # r7: a probe whose normal path prints a bash diagnostic (e.g. a `[` test
      # called with a non-integer) is defective even when its answer happens to
      # be right — measured: `[: max: integer expected` on stderr from the
      # memory fill arm while the row still read correctly. The output is
      # captured with 2>&1, so this catches stderr noise in every case.
      bad "$label: shell diagnostic noise in census output: $(printf '%s\n' "$out" | grep -m1 -E 'integer expected|line [0-9]+: \[: ')"
    else
      miss=''
      for re in "$@"; do
        printf '%s\n' "$out" | grep -qE -- "$re" || miss="$miss |$re|"
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
    if [ "$rc" -ne "$wrc" ]; then
      bad "$label: exit $rc want $wrc"
    else
      miss=''
      for re in "${res[@]}"; do
        printf '%s\n' "$out" | grep -qE -- "$re" || miss="$miss |$re|"
      done
      if [ -n "$miss" ]; then bad "$label: missing $miss"; else ok "$label (exit $rc)"; fi
    fi
  }

  # --- cases ---------------------------------------------------------------
  PIN_NOW=1700000000

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

  FX="$work/fx/oom-journal"; mkdir -p "$FX"; fx_quiet "$FX"; mkdir -p "$FX/root"
  printf 'kernel: Out of memory: Killed process 4242\n' > "$FX/stub/journal"
  check 'drift: OOM_KILL_JOURNAL' 1 DRIFT \
    'FINDING OOM_KILL_JOURNAL' \
    '^MORI_CENSUS: DRIFT '

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
    '^SURFACE journal: ok'

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

  check_cli 'cli: unknown arg exit 2' 2 'mori-census:' -- --bogus
  check_cli 'cli: --help exit 0' 0 'usage: mori-census' -- --help

  printf 'MORI_CENSUS_SELFTEST: %s (%d cases, %d passed, %d failed)\n' \
    "$([ "$FAIL" -eq 0 ] && printf PASS || printf FAIL)" "$((PASS + FAIL))" "$PASS" "$FAIL"
  [ "$FAIL" -eq 0 ]
}

# ---- main -------------------------------------------------------------------
main() {
  local selftest=0
  while [ $# -gt 0 ]; do
    case "$1" in
      --selftest) selftest=1; shift ;;
      --help|-h) usage; exit 0 ;;
      verify|--verify) shift ;; # accepted alias
      *) die_usage "unknown argument: $1" ;;
    esac
  done
  if [ "$selftest" -eq 1 ]; then
    run_selftest
    return
  fi
  run_census live
}

main "$@"
