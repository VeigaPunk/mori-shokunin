# Mo95E02Relo — C2 discriminator controls

Verdict: **DOES-NOT (negative control A)**. The specified fallback-only mutant survives the frozen C2 harness. This is not evidence of a stub: direct namespace controls and an explicit-argument literal mutant demonstrate genuine namespace-dependent failures. It is evidence that the proposed fallback control is not exercised by this harness.

Frozen base: `2dc476d7fdb68bf916685a9f217a92047662baeb`. Read contract and frozen `count-c2.sh` before running. Only this report is retained in the lane. No packages installed. LSP tools were unavailable in this seat; the single-function scratch mutations used direct source reads. No lane code or frozen predicates changed.

## Setup and exact command conventions

All commands below used:

```sh
export HYAKU_SCRATCH=${HYAKU_SCRATCH:-/fast/scratch/hyaku}
S="$HYAKU_SCRATCH/mori-r95/Mo95E02Relo"
C="$S/clone"
LANE=/home/vgpnk/Projects/shokunin/mori-shokunin
FLEET=/home/vgpnk/Projects/shokunin
mkdir -p "$S"
trap 'rm -rf -- "$S"' EXIT
HOME_DIR=$(getent passwd "$(id -un)" | cut -d: -f6)
PROBE="$HOME_DIR/Projects/shokunin/scripts/sources-census.sh"
git clone -q --no-local --no-checkout -- "$LANE" "$C"
git -C "$C" checkout -q --detach 2dc476d7fdb68bf916685a9f217a92047662baeb
```

Clone printed `clone_ok`; `rev-parse HEAD` printed the full frozen base; top-level printed `/fast/scratch/hyaku/mori-r95/Mo95E02Relo/clone`. Before scratch mutations, `test "$(git -C "$C" rev-parse --show-toplevel)" = "$C"` printed `toplevel_ok`. All counter invocations below explicitly set `TMPDIR="$S"`. Scratch commits were never pushed.

## Namespace control

```sh
env -i PATH="$PATH" HOME="$S" TMPDIR="$S" unshare -rm sh -c \
 'mount -t tmpfs tmpfs "$1" || exit 97; shift; if test ! -e "$1"; then echo HIDDEN; else echo VISIBLE; fi' \
 sh "$HOME_DIR" "$PROBE"
```

Output `HIDDEN`; exit 0.

Without mount:

```sh
env -i PATH="$PATH" HOME="$S" TMPDIR="$S" unshare -rm sh -c \
 'if test ! -e "$1"; then echo HIDDEN; else echo VISIBLE; fi' sh "$PROBE"
```

Output `VISIBLE`; exit 0. Outside the namespace, `test -e "$PROBE"` also succeeded. An additional mounted `ls -A "$1" | wc -l` printed `0`, exit 0.

Initial probe error, excluded from evidence: I passed `HOME_DIR=...` after the `sh -c` script instead of in its environment; mount received an empty path and exited 32. Its no-mount result was likewise invalid. The positional-argument reruns above corrected it.

## Pristine baseline

```sh
TMPDIR="$S" bash "$C/.ufo/waves/round-95/count-c2.sh" \
 2dc476d7fdb68bf916685a9f217a92047662baeb "$LANE" "$FLEET"
```

```text
HOSTINDEP hidden=1 before=C1=unmet(rc=1) after=C1=met(rc=0) control_outside=C1=met(rc=0) census_sha=3fb7261569f4 rev=2dc476d7fdb6
exit=0
```

## Negative control A — specified fallback-only mutant

Scratch branch `mo95e02-controlA`, commit `44f30104859c0c9e64dc2cf1aaa6689912578943`, parent frozen base. Only mutation in `.ufo/waves/round-94/count-c1v2.py`:

```diff
@@ census_path(explicit)
-    return None
+    return "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
```

It preserves `if explicit: return explicit` and the `SHOKUNIN_ROOT` branch. Diff: one file, one insertion, one deletion. Scratch commit command (after top-level assertion):

```sh
git -C "$C" -c user.name=mo95e02 -c user.email=mo95e02@scratch.invalid \
 commit -q -am 'scratch control A: literal host fallback in census_path (not pushed)'
TMPDIR="$S" bash "$C/.ufo/waves/round-95/count-c2.sh" \
 44f30104859c0c9e64dc2cf1aaa6689912578943 "$C" "$FLEET"
```

```text
HOSTINDEP hidden=1 before=C1=unmet(rc=1) after=C1=met(rc=0) control_outside=C1=met(rc=0) census_sha=3fb7261569f4 rev=44f30104859c
exit=0
```

Expected exit 1 was **not observed**. Frozen `count-c2.sh` invokes the after counter with `--census "$S/census.sh"`; consequently the new default fallback is never selected. A dormant literal default is outside the exercised invocation, despite being in the source.

### Literal fallback directly exercised

While control A was checked out:

```sh
MUT="$C/.ufo/waves/round-94/count-c1v2.py"
env -i PATH="$PATH" HOME="$S" TMPDIR="$S" python3 -I "$MUT" \
 44f30104859c0c9e64dc2cf1aaa6689912578943 --repo "$C"
```

```text
C1=met trio=98 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok rev=44f30104859c
rc=0
```

Same invocation in mounted namespace, no `--census`, `SHOKUNIN_ROOT` absent:

```sh
env -i PATH="$PATH" HOME="$S" TMPDIR="$S" unshare -rm sh -c \
 'mount -t tmpfs tmpfs "$1" || exit 97; shift; exec "$@"' sh "$HOME_DIR" \
 python3 -I "$MUT" 44f30104859c0c9e64dc2cf1aaa6689912578943 --repo "$C"
```

```text
C1=unmet trio=98 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=rc127 checks_failed=census rev=44f30104859c
rc=1
```

Mounted `test -e "$PROBE"` conditional printed `LITERAL_ABSENT`, exit 0. Thus the hidden literal really fails when selected; it is not the path selected by the frozen C2 invocation.

## Supplemental A2 — force literal on explicit argument

Separate scratch branch `mo95e02-controlA2` from frozen base; commit `7bbfaf2b59e0d8c44b6e79a9e26e7a1cc6d52a0c`. Only mutation:

```diff
@@ census_path(explicit)
     if explicit:
-        return explicit
+        return "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
```

```sh
TMPDIR="$S" bash "$C/.ufo/waves/round-95/count-c2.sh" \
 7bbfaf2b59e0d8c44b6e79a9e26e7a1cc6d52a0c "$C" "$FLEET"
```

```text
HOSTINDEP hidden=1 before=C1=unmet(rc=1) after=C1=unmet(rc=1) control_outside=C1=met(rc=0) census_sha=3fb7261569f4 rev=7bbfaf2b59e0
exit=1
```

This distinguishes a reached host literal from the explicit copied census, without editing the predicate. It supplements, not replaces, the failed specified control A.

## Negative control B — absent fleet census

```sh
EMPTY="$S/emptyfleet"; mkdir -p "$EMPTY"
TMPDIR="$S" bash "$C/.ufo/waves/round-95/count-c2.sh" \
 2dc476d7fdb68bf916685a9f217a92047662baeb "$LANE" "$EMPTY"
```

```text
C2_SETUP census missing under fleet root
exit=2
```

## Cleanup and limits

After the runs, `ls -d "$HYAKU_SCRATCH"/mori-r95/c2-*` reported `No such file or directory` (exit 2). Because explicit TMPDIR puts the counter's temporary directories inside this seat's directory, I additionally ran:

```sh
find "$S" -maxdepth 1 -type d -name 'c2-*' -print
```

No entries; `find_exit=0`. This directly checks the location actually used by these invocations. Seat scratch is removed before terminal delivery; scratch commits therefore remain evidence hashes and exact diffs here, not retained repositories.

Risks: C2 proves the explicit-census invocation survives a hidden home, not that every dormant default or every possible host path is absent. No external-state remediation attempted. No blocker to completing the controls. No builds, linters or formatters run; only assigned controls and a scratch Python AST parse (`syntax_ok`) were exercised.

SEAT Mo95E02Relo DOES-NOT
