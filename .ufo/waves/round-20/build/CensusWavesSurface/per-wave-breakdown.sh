#!/usr/bin/env bash
# CensusWavesSurface companion (documentation only, read-only, writes nothing).
# Lists, per directory, the class that probe_waves (tools/mori-census.sh:876-928) assigns
# using the same tests, in the same order, with the same regex. The aggregate counts the
# census prints come from the verbatim harness (probe-waves-harness.sh); this listing only
# shows which directory sits in which class and why.
# usage: per-wave-breakdown.sh [WAVES_DIR] [NOW_EPOCH] [THRESHOLD_S]
set -uo pipefail
W=${1:-/home/vgpnk/Projects/shokunin/.ufo/waves}
NOW=${2:-$(date +%s)}
THRESH=${3:-7200}
HAS_JQ=0
command -v jq >/dev/null 2>&1 && HAS_JQ=1
printf 'COMPANION waves_dir=%s now_epoch=%s threshold_s=%s jq=%s\n' "$W" "$NOW" "$THRESH" "$HAS_JQ"
for d in "$W"/*; do
  [ -d "$d" ] || continue
  base=$(basename -- "$d")
  case "$base" in
    round-*|.*) printf 'EXCLUDED %s\n' "$base"; continue ;;
  esac
  reg=0; disp=0; run=0; settle=0; token=-
  [ -f "$d/swarm-registry.json" ] && reg=1
  [ -f "$d/dispatch.json" ] && disp=1
  [ -f "$d/run.json" ] && run=1
  if [ -f "$d/results.json" ] || [ -f "$d/closeout.json" ] || [ -f "$d/mission-result.json" ] || [ -f "$d/closeout.md" ]; then
    settle=1
    for f in results.json closeout.json mission-result.json closeout.md; do
      if [ -f "$d/$f" ]; then token=$f; break; fi
    done
  else
    for cand in swarm-registry.json dispatch.json run.json spec.json; do
      [ -f "$d/$cand" ] || continue
      if grep -qE '"(closed|settled)"[[:space:]]*:[[:space:]]*true|"status"[[:space:]]*:[[:space:]]*"closed"' "$d/$cand" 2>/dev/null; then
        settle=1; token="grep:$cand"; break
      fi
    done
  fi
  newest=$(find "$d" -type f -printf '%T@\n' 2>/dev/null | sort -n | tail -1 | cut -d. -f1)
  age=-
  if [ -n "${newest:-}" ]; then age=$((NOW - newest)); fi
  files=$(find "$d" -type f 2>/dev/null | wc -l)
  subdirs=$(find "$d" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
  members=n/a
  if [ "$HAS_JQ" = 1 ] && [ -f "$d/dispatch.json" ]; then
    members=$(jq -r 'if (.taskCall|type)=="object" and (.taskCall.tasks|type)=="array" then (.taskCall.tasks|length|tostring) elif .taskCall==null then "taskCall-null" else "other" end' "$d/dispatch.json" 2>/dev/null || echo unparsed)
  fi
  if [ "$settle" -eq 1 ]; then cls=settled
  elif [ "$reg" -eq 1 ] || [ "$disp" -eq 1 ] || [ "$run" -eq 1 ]; then cls=unsettled
  else cls=empty; fi
  aged=0
  if [ "$cls" = unsettled ] && [ "$age" != - ] && [ "$age" -gt "$THRESH" ]; then aged=1; fi
  printf 'WAVE %s class=%s aged=%s reg=%s disp=%s run=%s settle=%s token=%s age_s=%s files=%s subdirs=%s dispatch_tasks=%s\n' \
    "$base" "$cls" "$aged" "$reg" "$disp" "$run" "$settle" "$token" "$age" "$files" "$subdirs" "$members"
done
