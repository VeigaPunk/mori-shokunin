#!/usr/bin/env bash
# mori round-93 do-nothing, text-only, deletion and forgery controls (committed before any wave
# output). Usage: bash controls-r93.sh <lane-repo> <out-file>
# Every control must print an UNMET verdict (rc 1). A control that meets its predicate would
# mean the counter or the target is wrong, and the round stops.
set -u
LANE="${1:?lane repo}"
OUT="${2:?out file}"
ENTERING="7b3fe9d540c98b8b0390a0f9bbe78de4341092a5"
W="$(cd "$(dirname "$0")" && pwd)"
S="${TMPDIR:-/fast/scratch/hyaku}/mori-r93-controls"
mkdir -p "$S"
: > "$OUT"
say() { printf '%s\n' "$*" | tee -a "$OUT"; }
fixture() { # name -> prints a sandbox clone (shared objects, never the lane) at the ENTERING tree
  local d="$S/$1"
  rm -rf "$d" && mkdir -p "$S"
  git clone -q --shared --no-checkout "$LANE" "$d" || { say "FIXTURE_SETUP clone failed $1"; exit 2; }
  git -C "$d" checkout -q -B fixture "$ENTERING" || { say "FIXTURE_SETUP checkout failed $1"; exit 2; }
  echo "$d"
}
commit_fixture() { git -C "$1" add -A && git -C "$1" -c user.name=mori-shokunin -c user.email=mori@shokunin.local commit -q -m "fixture $2"; }
GIT=(git -c user.name=mori-shokunin -c user.email=mori@shokunin.local)
run() { # label counter rev repo
  say "## $1"
  python3 -I "$W/$2" "$3" --repo "$4" >>"$OUT" 2>&1
  say "rc=$?"
}

TWELVE="counter-semantics-r78 counter-win-r77 drift-pin-r10 execution-binding-r89 kernel-v7.3-recheck-r53 lane-silence-r2 rotation-receipt-grammar-r76 rotation-schedule-r74 rotation-series-r75 selftest-flake-r9 surfaces-r8 workstate-win-r71"

# ---- C1 calibration controls ----
run "C1 do-nothing at ENTERING (expect unmet, adm_fail=12)" count-c1.py "$ENTERING" "$LANE"

D=$(fixture c1-text-only)
sed -i 's/Each `verified-at` names the admission$/Each `verified-at` names the admission or a date/' "$D/corpus/lessons/round-92.md"
grep -q 'names the admission or a date' "$D/corpus/lessons/round-92.md" || { say "FIXTURE_SETUP text-only sed did not match"; exit 2; }
commit_fixture "$D" "c1 text-only: lesson sentence edited, data unchanged"
run "C1 text-only control: lesson sentence reworded, 12 data lines unchanged (expect unmet)" count-c1.py HEAD "$D"

D=$(fixture c1-strip)
for f in $TWELVE; do sed -i '/^verified-at:/d' "$D/corpus/knowledge/$f.md"; done
commit_fixture "$D" "c1 deletion: verified-at removed from the 12 files"
run "C1 deletion control: verified-at stripped from 12 files (expect unmet)" count-c1.py HEAD "$D"

D=$(fixture c1-forged-body)
# forgery: the verified-at hash is right in every file, but one of the 12 also edits a body line
python3 - "$D" "$TWELVE" <<'PY'
import subprocess, sys, os
d, names = sys.argv[1], sys.argv[2].split()
ENTERING = "7b3fe9d540c98b8b0390a0f9bbe78de4341092a5"
for n in names:
    rel = "corpus/knowledge/%s.md" % n
    ac = subprocess.run(["git", "-C", d, "log", "--diff-filter=A", "--format=%h", ENTERING, "--", rel],
                        capture_output=True, text=True).stdout.split()[-1]
    p = os.path.join(d, rel)
    lines = open(p, encoding="utf-8").read().split("\n")
    for i, ln in enumerate(lines[:12]):
        if ln.startswith("verified-at:"):
            lines[i] = "verified-at: %s (forged)" % ac
            break
    if n == names[0]:
        for j in range(12, len(lines)):
            if lines[j].strip():
                lines[j] = lines[j] + " [edited]"
                break
    open(p, "w", encoding="utf-8").write("\n".join(lines))
PY
commit_fixture "$D" "c1 forged: correct-looking verified-at plus one body edit"
run "C1 forgery control: verified-at forged correctly, one body line edited (expect unmet patched12)" count-c1.py HEAD "$D"

# ---- C2 operability controls ----
run "C2 do-nothing at ENTERING (expect unmet, home_literals>0)" count-c2.py "$ENTERING" "$LANE"

D=$(fixture c2-delete)
rm -f "$D/tools/mori-blind-check.sh" "$D/tools/mori-misroot-sweep.py" "$D/tools/mori-round17-context-check.py"
commit_fixture "$D" "c2 deletion: three tools removed"
run "C2 deletion control: three tools removed (expect unmet tools)" count-c2.py HEAD "$D"

D=$(fixture c2-rename)
sed -i 's#/home/vgpnk/#/home/someone/#g; s#/home/vgpnk#/home/someone#g' "$D"/tools/mori-blind-check.sh "$D"/tools/mori-misroot-sweep.py "$D"/tools/mori-round17-context-check.py
commit_fixture "$D" "c2 rename: vgpnk replaced by another user name"
run "C2 rename control: literal user renamed, still a host home path (expect unmet home_literals)" count-c2.py HEAD "$D"

say "## scratch"
rm -rf "$S"
say "controls done"
