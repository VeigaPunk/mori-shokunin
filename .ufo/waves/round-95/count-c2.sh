#!/usr/bin/env bash
# mori round-95 C2 counter (operability, capability acquisition). Frozen predicate P-C2r95
# (`.ufo/waves/round-95/contract.md` section C2; this header, the contract and the receipt share the sentence):
#
#   bash .ufo/waves/round-95/count-c2.sh <rev> <lane-repo> <fleet-root>
#
# Inside an unprivileged user+mount namespace the account home directory is replaced by an empty tmpfs, so
# the host-literal fleet path is absent. Both counters are the lane's PRE-EXISTING artifacts at <rev>:
#   before  = round-93 counter  .ufo/waves/round-93/count-c1.py (host-bound: its CENSUS constant is the host path)
#   after   = round-94 counter  .ufo/waves/round-94/count-c1v2.py (fleet root by --census; no host path)
# Predicate: exit 0 iff (a) the namespace hid the home directory, (b) BEFORE prints C1=unmet or crashes with
# non-zero rc, (c) AFTER prints `C1=met` with rc 0 on the same revision, and (d) positive control: the BEFORE
# counter run OUTSIDE the namespace prints `C1=met` rc 0 (so the namespace, not the counter logic, is the cause).
# Prints one line: HOSTINDEP hidden=<0|1> before=<...> after=<...> control_outside=<...> census_sha=<12> rev=<12>
# exit 2 on setup failure. Scratch lives under $TMPDIR (default $HYAKU_SCRATCH/mori-r95, else /fast/scratch/hyaku);
# the git clone is --no-local so no object alternates point into the hidden home directory.
set -u
rev=${1:?rev}; lane=${2:?lane-repo}; fleet=${3:?fleet-root}
if [ ! -f "$fleet/scripts/sources-census.sh" ]; then echo "C2_SETUP census missing under fleet root"; exit 2; fi
home_dir=$(getent passwd "$(id -un)" | cut -d: -f6)
if [ -z "$home_dir" ] || [ ! -d "$home_dir" ]; then echo "C2_SETUP account home unresolved"; exit 2; fi
root=${TMPDIR:-${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mori-r95}
mkdir -p "$root" || { echo "C2_SETUP scratch root unwritable"; exit 2; }
S=$(mktemp -d "$root/c2-XXXXXX") || { echo "C2_SETUP mktemp failed"; exit 2; }
trap 'rm -rf -- "$S"' EXIT
git clone -q --no-local --no-checkout -- "$lane" "$S/clone" || { echo "C2_SETUP clone failed"; exit 2; }
git -C "$S/clone" checkout -q --detach "$rev" || { echo "C2_SETUP revision unresolvable: $rev"; exit 2; }
mkdir -p "$S/home" && cp "$fleet/scripts/sources-census.sh" "$S/census.sh" || { echo "C2_SETUP census copy failed"; exit 2; }
census_sha=$(sha256sum "$S/census.sh" | cut -c1-12)
rev12=$(git -C "$S/clone" rev-parse --short=12 HEAD)
before_src="$S/clone/.ufo/waves/round-93/count-c1.py"
after_src="$S/clone/.ufo/waves/round-94/count-c1v2.py"
probe="$home_dir/Projects/shokunin/scripts/sources-census.sh"

# Run a command inside the namespace: home directory replaced by an empty tmpfs.
in_ns() {
  env -i PATH="$PATH" HOME="$S/home" TMPDIR="$S" \
    unshare -rm sh -c 'mount -t tmpfs tmpfs "$1" || exit 97; shift; exec "$@"' sh "$home_dir" "$@"
}
verdict() { printf '%s' "$1" | grep -o 'C1=[a-z]*' | head -1; }

hidden=0
if in_ns sh -c 'test ! -e "$1"' sh "$probe"; then hidden=1; fi
b_out=$(in_ns python3 -I "$before_src" "$rev" --repo "$S/clone" 2>&1); b_rc=$?
a_out=$(in_ns python3 -I "$after_src" "$rev" --repo "$S/clone" --census "$S/census.sh" 2>&1); a_rc=$?
c_out=$(env -i PATH="$PATH" HOME="$S/home" TMPDIR="$S" python3 -I "$before_src" "$rev" --repo "$S/clone" 2>&1); c_rc=$?

b_v=$(verdict "$b_out"); a_v=$(verdict "$a_out"); c_v=$(verdict "$c_out")
[ -z "$b_v" ] && b_v=NONE
[ -z "$c_v" ] && c_v=NONE
[ "$a_v" = "C1=met" ] && [ "$a_rc" -eq 0 ] && a_ok=1 || a_ok=0
[ "$b_v" = "C1=unmet" ] || [ "$b_rc" -ne 0 ] && b_ok=1 || b_ok=0
[ "$c_v" = "C1=met" ] && [ "$c_rc" -eq 0 ] && c_ok=1 || c_ok=0
printf 'HOSTINDEP hidden=%s before=%s(rc=%s) after=%s(rc=%s) control_outside=%s(rc=%s) census_sha=%s rev=%s\n' \
  "$hidden" "$b_v" "$b_rc" "$a_v" "$a_rc" "$c_v" "$c_rc" "$census_sha" "$rev12"
if [ "$hidden" = 1 ] && [ "$b_ok" = 1 ] && [ "$a_ok" = 1 ] && [ "$c_ok" = 1 ]; then exit 0; fi
exit 1
