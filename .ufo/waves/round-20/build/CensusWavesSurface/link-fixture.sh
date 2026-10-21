#!/usr/bin/env bash
# CensusWavesSurface: latent symlink-wave check for the verbatim probe harness.
# Writes only under a mktemp directory in /tmp, removed on exit. Read-only w.r.t. the fleet.
set -euo pipefail
H=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/build/CensusWavesSurface/probe-waves-harness.sh
F=$(mktemp -d /tmp/mori-r20-c2-link.XXXXXX)
trap 'rm -rf -- "$F"' EXIT
mkdir -p "$F/real" "$F/waves/plain-wave"
printf '%s\n' '{"schema":"ufo-swarm-wave-dispatch-v1","taskCall":null}' > "$F/real/dispatch.json"
cp "$F/real/dispatch.json" "$F/waves/plain-wave/dispatch.json"
touch -d @1600000000 "$F/real/dispatch.json" "$F/waves/plain-wave/dispatch.json"
ln -s "$F/real" "$F/waves/link-wave"
echo "# find -type d (what the cmd= text describes) lists: $(find "$F/waves" -maxdepth 1 -mindepth 1 -type d -printf '%f ')"
MORI_WAVES_DIR="$F/waves" MORI_NOW_EPOCH=1700000000 "$H"
