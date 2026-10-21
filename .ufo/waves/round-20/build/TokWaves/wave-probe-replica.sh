#!/usr/bin/env bash
# Read-only replica of tools/mori-census.sh probe_waves (census lines 876-929 at
# the entering tip; body byte-identical to the r10 pin, see TokWaves.md). Writes
# nothing; prints one line per wave directory. Used only to classify the
# -FINDING:WAVE_UNSETTLED_AGE token of the round-20 C1 drift receipt.
set -u
WAVES_DIR=${1:-/home/vgpnk/Projects/shokunin/.ufo/waves}
WAVE_UNSETTLED_S=${MORI_WAVE_UNSETTLED_S:-7200}
NOW_EPOCH=$(date +%s)
echo "now_epoch=$NOW_EPOCH threshold_s=$WAVE_UNSETTLED_S waves_dir=$WAVES_DIR"
for d in "$WAVES_DIR"/*; do
  [ -d "$d" ] || continue
  base=$(basename -- "$d")
  case "$base" in round-*|.*) continue ;; esac
  has_reg=0 has_disp=0 has_run=0 has_settle=0 settle_why=-
  [ -f "$d/swarm-registry.json" ] && has_reg=1
  [ -f "$d/dispatch.json" ] && has_disp=1
  [ -f "$d/run.json" ] && has_run=1
  if [ -f "$d/results.json" ] || [ -f "$d/closeout.json" ] || [ -f "$d/mission-result.json" ] || [ -f "$d/closeout.md" ]; then
    has_settle=1; settle_why=file
  else
    for cand in "$d/swarm-registry.json" "$d/dispatch.json" "$d/run.json" "$d/spec.json"; do
      [ -f "$cand" ] || continue
      if grep -qE '"(closed|settled)"[[:space:]]*:[[:space:]]*true|"status"[[:space:]]*:[[:space:]]*"closed"' "$cand" 2>/dev/null; then
        has_settle=1; settle_why="typed:$(basename -- "$cand")"; break
      fi
    done
  fi
  listing=$(find "$d" -type f -printf '%T@ %p\n' 2>&1); frc=$?
  age=0; newest=''; newest_path=''
  if [ "$frc" -eq 0 ]; then
    top=$(printf '%s\n' "$listing" | sort -n | tail -1)
    newest=${top%% *}; newest=${newest%%.*}
    newest_path=${top#* }
    if [ -n "$newest" ]; then age=$((NOW_EPOCH - newest)); fi
  fi
  if [ "$has_settle" -eq 1 ]; then
    class=settled
  elif [ "$has_reg" -eq 1 ] || [ "$has_disp" -eq 1 ] || [ "$has_run" -eq 1 ]; then
    if [ "$frc" -ne 0 ]; then class=age_unreadable
    elif [ "$age" -gt "$WAVE_UNSETTLED_S" ]; then class=AGED_UNSETTLED
    else class=unsettled_young
    fi
  else
    class=empty
  fi
  printf '%s|class=%s|reg=%s disp=%s run=%s|settle=%s|find_rc=%s|age_s=%s|newest=%s\n' \
    "$base" "$class" "$has_reg" "$has_disp" "$has_run" "$settle_why" "$frc" "$age" "$newest_path"
done
