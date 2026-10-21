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
