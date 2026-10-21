# Verbatim extraction of drift helpers from tools/mori-census.sh (lines 2744-2772, 2776-2792, 2808-2918).
# Used only for offline re-application of the census's own comparator to captured output; no census run.
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
  positive_kernel_oom positive_unit_oom positive_unit_signal positive_process_sigkill
  user_positive_kernel_oom system_positive_kernel_oom
  user_positive_unit_oom system_positive_unit_oom
  user_positive_process_sigkill user_positive_unit_signal
)
# r15: the positive_* / *_positive_* entries are integer counts of individually
# valid records. Their MAGNITUDES are masked like every other counter; masking
# never removes the token, the finding line, or its severity. An
# `unavailable:<reason>` value contains no digits and therefore stays visible
# (an unavailable class is behavior, not a volatile count).
# Non-counter volatile entries, each with its own mask rule below.
DRIFT_VOLATILE_SPECIAL='ts age_s mtime_age_s *_epoch mem_peak_anchor psi_some_avg10 psi_full_avg10 io_avg_since_boot state_val_unread_reasons boot script_sha256 example'
DRIFT_VOLATILE_LIST="$DRIFT_VOLATILE_SPECIAL ${DRIFT_COUNTER_KEYS[*]}"

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
