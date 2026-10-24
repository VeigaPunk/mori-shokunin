#!/usr/bin/env bash
# CensusWavesSurface: read-only checks behind the C2 before-state report.
# Reads the fleet .ufo/waves and the lane .ufo/waves; writes nothing.
set -uo pipefail
W=/home/vgpnk/Projects/shokunin/.ufo/waves
L=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves
echo "# dispatch shape of the aged unsettled waves and the 26-task wave (jq)"
for w in shokunin-train-20261013 shokunin-train-20261013-w2 shokunin-train-20261013-w3 shokunin-train-20261013-w4 shokunin-train-20261016-w24; do
  printf '%s: ' "$w"
  jq -c '{has_taskCall: has("taskCall"), taskCall_type: (.taskCall|type), tasks: (try (.taskCall.tasks|length) catch null), top_keys: keys}' "$W/$w/dispatch.json"
done
echo "# depth-2 dispatch.json (probe-visible names): count"
find "$W" -mindepth 2 -maxdepth 2 -name dispatch.json -type f | wc -l
echo "# depth-2 dispatch.json containing trailer text 'Report: write your scoped findings to': count"
n=0
for f in $(find "$W" -mindepth 2 -maxdepth 2 -name dispatch.json -type f); do
  if grep -q 'Report: write your scoped findings to' "$f"; then n=$((n + 1)); fi
done
echo "$n"
echo "# fleet json (any depth) carrying trailer text"
grep -rl --include='*.json' 'Report: write your scoped findings to' "$W" 2>/dev/null
echo "# lane json (any depth) carrying trailer text: count"
grep -rl --include='*.json' 'Report: write your scoped findings to' "$L" 2>/dev/null | wc -l
echo "# depth-2 dispatch.json schema values"
for f in $(find "$W" -mindepth 2 -maxdepth 2 -name dispatch.json -type f); do jq -r '.schema // "absent"' "$f"; done | sort | uniq -c
echo "# fleet json files, any depth: count"
find "$W" -type f -name '*.json' | wc -l
echo "# fleet json with top-level schema ufo-swarm-wave-dispatch-v1, any depth: count"
find "$W" -type f -name '*.json' -print0 | xargs -0 jq -r 'select(type=="object" and .schema=="ufo-swarm-wave-dispatch-v1") | input_filename' 2>/dev/null | wc -l
echo "# depth-1 directories (find -type d) / of which round-*"
find "$W" -maxdepth 1 -mindepth 1 -type d | wc -l
find "$W" -maxdepth 1 -mindepth 1 -type d -name 'round-*' | wc -l
echo "# live grep-token match in shokunin-train-20261013-w5/swarm-registry.json (jq paths of true closed/settled)"
jq -c '[paths(scalars) as $p | select((getpath($p)==true) and (($p|map(tostring)|join("."))|test("closed|settled"))) | $p|map(tostring)|join(".")]' "$W/shokunin-train-20261013-w5/swarm-registry.json"
echo "# lane census SHA-256 (must equal 87b8d680...ab28)"
sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh
