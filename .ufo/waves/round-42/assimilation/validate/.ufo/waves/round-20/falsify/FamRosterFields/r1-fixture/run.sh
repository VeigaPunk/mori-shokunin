#!/usr/bin/env bash
F=$(dirname "$0")
FLEET_CONF="$F/conf"; STATE_DIR="$F/state"; MORI_ROSTER_LANES=""
source "$F/resolve.sh"
resolve_roster
echo "roster_source=$ROSTER_SOURCE roster_n=$ROSTER_N conf_n=$CONF_N state_n=$STATE_N conf_dropped_n=$CONF_DROPPED_N state_dropped_n=$STATE_DROPPED_N"
echo "roster_lanes=$ROSTER_LANES"
