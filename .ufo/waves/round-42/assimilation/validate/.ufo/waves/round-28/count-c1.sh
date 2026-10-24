#!/usr/bin/env bash
# Round 28, claim C1 counter (freshness), as amended by contract amendment A1 (before any superseding row exists;
# wave-1 CriticC1Design findings 1-3). First-published SOURCES cells restored, the eight carried row defects
# superseded by rows re-opened this round, and the live readers moved to the new rows. Reads committed bytes only
# (git objects at <rev>), never the working tree.
# Usage: bash .ufo/waves/round-28/count-c1.sh <rev>
# Prints row_identity=<summary line of the round-27 QUALITY 81 check at <rev>>, superseding=<k>/8 ids=..., the per-row
# failures (`fail <new id> <reason>`), readers_left=<n> (live reader lines still citing a superseded id), then
# C1=met|unmet.
# Exit 0 when C1=met, 1 when C1=unmet, 2 on a bad revision, a missing input or a usage error.
set -u
LANE=/home/vgpnk/Projects/shokunin/mori-shokunin
CHECK=.ufo/waves/round-27/check-row-identity.py
SRC=corpus/SOURCES.md
LESSON=corpus/lessons/round-28.md
# Fixed map new id -> superseded id (contract C1; routed defects 3 and 4 of round-27-verifier-spotcheck.md).
MAP="S145:S096 S146:S097 S147:S101 S148:S127 S149:S128 S150:S129 S151:S131 S152:S140"
# Live readers: every file that states lane knowledge today. History files (LOG, SCORECARD, lessons, .ufo) are exempt.
READERS="SKILL.md PROVINCE.md corpus/README.md corpus/knowledge"
[ $# -eq 1 ] || { echo "usage: count-c1.sh <rev>"; exit 2; }
R=$(git -C "$LANE" rev-parse --verify -q "$1^{commit}") || { echo "bad_rev"; exit 2; }
T=$(mktemp -d) || exit 2
trap 'rm -rf "$T"' EXIT
# the check script is taken from the round-27 landed tip df886be1 (frozen), never from the working tree
git -C "$LANE" show "df886be1cc75f1052002698bdb4a3d18a2eaf6c6:$CHECK" > "$T/check.py" || { echo "check_absent"; exit 2; }
git -C "$LANE" show "$R:$SRC" > "$T/sources.md" 2>/dev/null || { echo "sources_absent"; exit 2; }
git -C "$LANE" show "$R:$LESSON" > "$T/lesson.md" 2>/dev/null || : > "$T/lesson.md"
ri=$(python3 -I -B "$T/check.py" "$R" 2>/dev/null | grep -E '^rows=[0-9]+ changed=' | tail -n 1)
[ -n "$ri" ] || { echo "row_identity=error"; echo "C1=unmet"; exit 2; }
out=$(python3 -I -B - "$T/sources.md" "$T/lesson.md" "$MAP" "$LANE" "$R" <<'PY'
import re, subprocess, sys
sources, lesson, mp, lane, rev = sys.argv[1:6]
pairs = dict(p.split(":") for p in mp.split())
sep = re.compile(r"(?<!\\)\|")
rows = {}
for line in open(sources, encoding="utf-8").read().split("\n"):
    if re.match(r" {0,3}\|[ \t]*S[0-9]{3,}[ \t]*\|", line):
        c = [x.strip() for x in sep.split(line.strip())]
        if len(c) == 13:
            rows[c[1]] = c
gate = open(lesson, encoding="utf-8").read()
gsec = gate.split("\n## Gate", 1)[1].split("\n## ", 1)[0] if "\n## Gate" in gate else ""
def exists_with_id(path, rid):
    p = subprocess.run(["git", "-C", lane, "grep", "-q", "-w", "-F", rid, rev, "--", path], capture_output=True)
    return p.returncode == 0
ok, fails = [], []
for new, old in sorted(pairs.items()):
    r, o = rows.get(new), rows.get(old)
    if r is None or o is None:
        fails.append(f"fail {new} row_absent"); continue
    m = re.match(r"supersedes (S[0-9]{3}) — (.+)$", r[7])
    if not m or m.group(1) != old:
        fails.append(f"fail {new} prefix"); continue
    if m.group(2).strip() == o[7].strip():
        fails.append(f"fail {new} teaches_unchanged"); continue
    status, used = r[8], r[11]
    # mined rows need real readers; a rejected row may supersede only a rejected row (CORPUS: rejections stay rows)
    if status == "mined":
        if used in ("", "—", "-"):
            fails.append(f"fail {new} used_by_empty"); continue
    elif not (status == "rejected" and o[8] == "rejected"):
        fails.append(f"fail {new} status={status}"); continue
    paths = [] if used in ("", "—", "-") else [u.strip() for u in used.split(",") if u.strip()]
    bad = [p for p in paths if not exists_with_id(p, new)]
    if bad:
        fails.append(f"fail {new} used_by_not_citing={','.join(bad)}"); continue
    # one Gate line for the new id: https URL, a 64-hex sha256 and a quoted span
    gl = [l for l in gsec.split("\n") if re.match(rf"\|\s*{new}\s*\|", l)]
    if not gl or not any(re.search(r"https://", l) and re.search(r"\b[0-9a-f]{64}\b", l) and re.search(r"[\"“].+[\"”]", l) for l in gl):
        fails.append(f"fail {new} gate_line"); continue
    ok.append(old)
print(len(ok), ",".join(sorted(ok)) or "none")
for f in fails:
    print(f)
PY
) || { echo "counter_error"; exit 2; }
k=$(printf '%s\n' "$out" | head -n 1 | cut -d' ' -f1)
ids=$(printf '%s\n' "$out" | head -n 1 | cut -d' ' -f2)
# live readers still citing a superseded id as a word
olds=$(printf '%s\n' $MAP | cut -d: -f2 | paste -sd'|')
left=$(git -C "$LANE" grep -n -w -E "$olds" "$R" -- $READERS 2>/dev/null | grep -v -E 'tsukuroi' | wc -l)
echo "row_identity=$ri"
echo "superseding=$k/8 ids=$ids"
printf '%s\n' "$out" | tail -n +2
echo "readers_left=$left"
case "$ri" in
  *" changed=0 removed=0 bad=0") ok_ri=1 ;;
  *) ok_ri=0 ;;
esac
if [ "$ok_ri" -eq 1 ] && [ "$k" -eq 8 ] && [ "$left" -eq 0 ]; then echo "C1=met"; exit 0; fi
echo "C1=unmet"; exit 1
