#!/usr/bin/env bash
# Offline re-application of mori-census.sh run_drift() to ALREADY-CAPTURED census stdout.
# Runs no census. Helpers are the verbatim extraction in drift-helpers-extracted.sh.
# usage: drift-offline.sh <pin-baseline> <captured-census-stdout> [diff-out]
set -u
HERE=$(cd -- "$(dirname -- "$0")" && pwd)
# shellcheck disable=SC1091
source "$HERE/drift-helpers-extracted.sh"
PIN=$1
RAW=$2
DIFF_OUT=${3:-}
marker='# --- canonical output follows ---'
in_block=0
have_vol=0
base_vol=''
base_str=''
base_lines=()
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
done < "$PIN"
vol_token=''
if [ "$base_vol" != "$DRIFT_VOLATILE_LIST" ]; then vol_token=volatile_fields; fi
canon=$(drift_normalize < "$RAW")
new_lines=()
new_str=''
while IFS= read -r line; do
  new_lines+=("$line")
  new_str+="$line"$'\n'
done <<< "$canon"
echo "have_volatile_header=$have_vol base_block_lines=${#base_lines[@]} fresh_block_lines=${#new_lines[@]} volatile_list_match=$([ -z "$vol_token" ] && echo yes || echo no)"
if [ -n "$DIFF_OUT" ]; then
  printf '%s\n' "${base_lines[@]}" > "$DIFF_OUT.pin"
  printf '%s\n' "${new_lines[@]}" > "$DIFF_OUT.fresh"
  diff -u "$DIFF_OUT.pin" "$DIFF_OUT.fresh" > "$DIFF_OUT" || true
fi
if [ "$base_str" = "$new_str" ]; then
  echo "MORI_DRIFT: ${vol_token:-none}"
  exit 0
fi
DRIFT_BASE_LINES=("${base_lines[@]}")
DRIFT_NEW_LINES=("${new_lines[@]}")
drift_report
echo "MORI_DRIFT: ${DRIFT_REPORT:-none}${vol_token:+ $vol_token}"
exit 1
