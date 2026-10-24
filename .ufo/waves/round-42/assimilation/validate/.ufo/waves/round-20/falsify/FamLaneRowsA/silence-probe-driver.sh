#!/usr/bin/env bash
# FamLaneRowsA scratch harness (read-only). Sources a scratch COPY of a census
# script with its trailing `main "$@"` line removed (the *-stripped.sh files),
# then runs only probe_silence() (the lane-row grader) and prints the SURFACE
# lane rows it produced. Inputs come from the environment: MORI_SHOKUNIN_ROOT,
# MORI_TIMELINE_FILE, MORI_NOW_EPOCH. Nothing here writes to fleet or lane repos.
set +e
census="$1"
. "$census"
set +e
probe_silence
printf '%s\n' "${SURFACE_LINES[@]}"
