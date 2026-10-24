#!/usr/bin/env bash
# CensusWavesSurface (round 20, C2 before-state): probe harness. NOT the census.
# Lines after this header are copied byte-for-byte from tools/mori-census.sh by sed:
#   288-292 LANE_ROOT/DEFAULT_ROOT   295-303 ROOT..WAVES_DIR   352 WAVE_UNSETTLED_S
#   379-380 SCRIPT_SHA256            382-384 NOW_EPOCH/TS_UTC  386-393 counters
#   419-440 emit_finding/emit_surface  561-566 cap            856-932 probe_waves
# Not copied: the census's SELF/SCRIPT_DIR lines (281-286, BASH_SOURCE-based) and its
# entry point (main "$@"), so the census itself never runs here. SELF and SCRIPT_DIR
# are set below to the same values the census derives for this checkout.
set -euo pipefail
SELF=/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh
SCRIPT_DIR=/home/vgpnk/Projects/shokunin/mori-shokunin/tools
LANE_ROOT=$(cd -- "$SCRIPT_DIR/.." && pwd)
DEFAULT_ROOT=$LANE_ROOT
case "$(basename -- "$LANE_ROOT")" in
  *-shokunin) DEFAULT_ROOT=$(cd -- "$LANE_ROOT/.." && pwd) ;;
esac
ROOT=${MORI_SHOKUNIN_ROOT:-$DEFAULT_ROOT}
UFO=${MORI_UFO_DIR:-$ROOT/.ufo}
WATCHDOG_LOG=${MORI_WATCHDOG_LOG:-$UFO/watchdog.log}
# The launch/close ledger is the watchdog log on this fleet; the override exists
# so a scenario driver can point the probe at the same bytes it writes
# (tools/mori-silence-cases.sh exports MORI_TIMELINE_FILE).
TIMELINE_FILE=${MORI_TIMELINE_FILE:-$WATCHDOG_LOG}
STATE_DIR=${MORI_STATE_DIR:-$UFO/state}
WAVES_DIR=${MORI_WAVES_DIR:-$UFO/waves}
WAVE_UNSETTLED_S=${MORI_WAVE_UNSETTLED_S:-7200}
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
cap() { # run read-only; capture stdout+stderr + rc without set -e trip
  set +e
  CAP_OUT=$("$@" 2>&1)
  CAP_RC=$?
  set -e
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
probe_waves
printf 'HARNESS waves_dir=%s wave_unsettled_s=%s now_epoch=%s census_sha256=%s\n' "$WAVES_DIR" "$WAVE_UNSETTLED_S" "$NOW_EPOCH" "$SCRIPT_SHA256"
for line in "${SURFACE_LINES[@]:-}"; do printf '%s\n' "$line"; done
for line in "${FINDING_LINES[@]:-}"; do printf '%s\n' "$line"; done
printf 'HARNESS roll=%s findings=%d drift=%d unavailable=%d surfaces=%d\n' "$ROLL" "$N_FINDINGS" "$N_DRIFT" "$N_UNAVAIL" "$N_SURFACES"
