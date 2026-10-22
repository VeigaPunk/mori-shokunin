#!/usr/bin/env bash
# Round-26 C2 counter (amendment A1). Usage: bash count-c2.sh <rev>. Runs the tool from a git archive of <rev>.
L=/home/vgpnk/Projects/shokunin/mori-shokunin; R=${1:?rev}; C=tools/fixtures/mori-oom-killers/cases.json; T=tools/mori-oom-killers.py
git -C "$L" rev-parse -q --verify "$R^{commit}" >/dev/null || { echo bad_rev; exit 2; }
F=$(git -C "$L" log --format=%H --diff-filter=A "$R" -- "$C" | tail -1); B=$(git -C "$L" log --format=%H --diff-filter=A "$R" -- "$T" | tail -1)
[ -n "$F" ] && [ -n "$B" ] || { echo "absent cases_commit=${F:-none} tool_commit=${B:-none}"; exit 2; }
git -C "$L" merge-base --is-ancestor "$F" "$B" && [ "$F" != "$B" ] && echo freeze_order=ok || echo freeze_order=bad
echo "cases_changed_since_freeze=$(git -C "$L" diff --name-only "$F" "$R" -- "$C" | wc -l)"
echo "N=$(git -C "$L" show "$F:$C" | jq '.cases|length')"
D=$(mktemp -d); git -C "$L" archive "$R" | tar -x -C "$D"; python3 -I -B "$D/$T" --selftest; echo "exit=$?"; rm -rf "$D"
