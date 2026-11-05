#!/usr/bin/env bash
# mori round-93 POST-FREEZE battery extension (added after the mutation seat Mo93M01Mut found
# three conjuncts that no frozen control flips: C1 admission prefix test, C1 census clause, C2
# bare-username clause). The frozen counters and controls-r93.sh are unchanged; this script only
# adds controls. Base for every control here is the LANDED revision, where each claim is met, so
# every control must read unmet (rc 1). Usage: bash controls-r93-ext.sh <lane-repo> <landed-rev> <out>
set -u
LANE="${1:?lane repo}"
LAND="${2:?landed revision}"
OUT="${3:?out file}"
W="$(cd "$(dirname "$0")" && pwd)"
S="${TMPDIR:-/fast/scratch/hyaku}/mori-r93-ext"
ENTERING="7b3fe9d540c98b8b0390a0f9bbe78de4341092a5"
mkdir -p "$S"
: > "$OUT"
say() { printf '%s\n' "$*" | tee -a "$OUT"; }
run() { # label counter rev repo
  say "## $1"
  python3 -I "$W/$2" "$3" --repo "$4" >>"$OUT" 2>&1
  say "rc=$?"
}
fixture_at() { # name rev -> sandbox clone (shared objects, never the lane) checked out at rev
  local d="$S/$1"
  rm -rf "$d" && mkdir -p "$S"
  git clone -q --shared --no-checkout "$LANE" "$d" || { say "FIXTURE_SETUP clone failed $1"; exit 2; }
  git -C "$d" checkout -q -B fixture "$2" || { say "FIXTURE_SETUP checkout failed $1"; exit 2; }
  echo "$d"
}
commit_fixture() { git -C "$1" add -A && git -C "$1" -c user.name=mori-shokunin -c user.email=mori@shokunin.local commit -q -m "fixture $2"; }

run "landed base C1 (expect met, rc 0)" count-c1.py "$LAND" "$LANE"
run "landed base C2 (expect met, rc 0)" count-c2.py "$LAND" "$LANE"

# C1 admission prefix test: each of the 12 mismatch files names ANOTHER file's admission commit.
# The original value text is rebuilt from ENTERING so no own hash survives in the parenthesis.
D=$(fixture_at c1-wrong-hash "$LAND")
python3 - "$D" "$ENTERING" <<'PY'
import subprocess, sys, os
d, ENT = sys.argv[1], sys.argv[2]
TWELVE = ["counter-semantics-r78.md", "counter-win-r77.md", "drift-pin-r10.md",
          "execution-binding-r89.md", "kernel-v7.3-recheck-r53.md", "lane-silence-r2.md",
          "rotation-receipt-grammar-r76.md", "rotation-schedule-r74.md", "rotation-series-r75.md",
          "selftest-flake-r9.md", "surfaces-r8.md", "workstate-win-r71.md"]
def git(*a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True).stdout
def adm(f):
    return git("log", "--diff-filter=A", "--format=%h", ENT, "--", "corpus/knowledge/" + f).split()[-1]
def original(f):
    for ln in git("show", ENT + ":corpus/knowledge/" + f).split("\n")[:12]:
        if ln.startswith("verified-at:"):
            return ln.split(":", 1)[1].strip()
    raise SystemExit("no verified-at at ENTERING for " + f)
for i, f in enumerate(TWELVE):
    other = TWELVE[(i + 1) % len(TWELVE)]
    p = os.path.join(d, "corpus/knowledge", f)
    lines = open(p, encoding="utf-8").read().split("\n")
    for j, ln in enumerate(lines[:12]):
        if ln.startswith("verified-at:"):
            lines[j] = "verified-at: %s (%s)" % (adm(other), original(f))
            break
    open(p, "w", encoding="utf-8").write("\n".join(lines))
PY
commit_fixture "$D" "c1 wrong-hash: each of the 12 verified-at names another file's admission commit"
run "C1 wrong-hash control on landed base (expect unmet, adm_fail=12)" count-c1.py HEAD "$D"

# C1 census clause: a malformed registry row (12 cells) on the landed base
D=$(fixture_at c1-census-break "$LAND")
printf '%s\n' '| S999 | malformed row with twelve cells | docs | A | scope | anchor | teaches | mined | 2026-11-05 | 90d | corpus/knowledge/audit-r11.md | extra |' >> "$D/corpus/SOURCES.md"
commit_fixture "$D" "c1 census break: malformed 12-cell row appended"
run "C1 census-break control on landed base (expect unmet, census)" count-c1.py HEAD "$D"

# C2 bare-username clause: the operator name in a tool with no /home/ form
D=$(fixture_at c2-bare-name "$LAND")
printf '%s\n' '# maintainer: vgpnk' >> "$D/tools/mori-blind-check.sh"
commit_fixture "$D" "c2 bare name: operator name in a comment, no home path"
run "C2 bare-username control on landed base (expect unmet, vgpnk_refs=1)" count-c2.py HEAD "$D"

say "## scratch"
rm -rf "$S"
say "ext controls done"
