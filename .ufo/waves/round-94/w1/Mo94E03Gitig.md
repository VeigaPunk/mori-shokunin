# Mo94E03Gitig — D3 mistake fix (untracked orchestrator dispatch markers)

Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`. Freeze `6b65e7c11f318481d5efa0429cdabb50743a2cc2`; entering base `84b152308fa6c2f224ad75dff68e525dab9057ac`. Scratch `S=/fast/scratch/hyaku/mori-r94/Mo94E03Gitig`, trap `rm -rf -- "$S"` EXIT. One shared no-checkout clone; verify clone added for apply-check. No tools installed (none needed). No mutating git outside scratch fixtures; lane git calls read-only (`rev-parse`, `ls-files`).

## 1. Setup

```
mkdir -p "$S" && trap 'rm -rf -- "$S"' EXIT && export S
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/mori-shokunin "$S/clone"   # done.
git -C "$S/clone" checkout -q --detach 6b65e7c11f318481d5efa0429cdabb50743a2cc2
git -C "$S/clone" rev-parse HEAD
# -> 6b65e7c11f318481d5efa0429cdabb50743a2cc2
test "$(git -C "$S/clone" rev-parse --show-toplevel)" = "$S/clone"   # -> OK (toplevel asserted)
```

## 2. Red (before)

```
git -C "$S/clone" check-ignore -v .ufo/waves/round-93/w1.ready.dispatched
# (no output) red_rc=1   <- NOT ignored at the freeze commit; matches claim before-state
```

Baseline `.gitignore` (5 lines, newline-terminated): sha256 `d0f7cf01feb8287c330f0d2b2478f056a9f956061b459b6cb6f0cd2fafe0f545`.

## 3. Fix (append exactly one line)

```
printf '%s\n' '.ufo/waves/*/*.ready.dispatched' >> "$S/clone/.gitignore"
```

Existing lines byte-identical: proven by restore round-trip — removed line 6 via edit, sha256 again `d0f7cf01…`, re-appended, final `git status --porcelain` shows only ` M .gitignore`.

## 4. Green (after)

```
git -C "$S/clone" check-ignore -v .ufo/waves/round-93/w1.ready.dispatched
# -> .gitignore:6:.ufo/waves/*/*.ready.dispatched	.ufo/waves/round-93/w1.ready.dispatched
# green_rc=0
git -C "$S/clone" check-ignore -v .ufo/waves/round-94/w1.ready
# (no output) plain_rc=1   <- plain .ready stays NOT ignored
git -C "$S/clone" check-ignore -v .ufo/waves/round-94/w1.ready.dispatched
# -> .gitignore:6:.ufo/waves/*/*.ready.dispatched	.ufo/waves/round-94/w1.ready.dispatched
# future_rc=0   <- pattern covers future rounds' dispatched markers
```

## 5. `ls-files -ci --exclude-standard` — EXPECTATION NOT MET, reported as observed

Seat expectation "prints nothing" fails on the freeze-commit tree for two independent reasons, both measured:

```
git -C "$S/clone" ls-files -ci --exclude-standard | sort > baseline   # baseline_rc=0
# at UNTOUCHED freeze commit: baseline=437 lines
#   of which matching .ready.dispatched: 0  -> all 437 are pre-existing
#   (.scratch/* and tools/__pycache__/*.pyc tracked while matching pre-existing rules)
# after the appended line: post=470 lines
comm -13 baseline post | grep -vc '\.ready\.dispatched$'   # -> 0 (delta is pure)
# delta=33 lines; all 33 confirmed tracked via git ls-files --error-unmatch (notracked=0)
```

Delta population: the 33 **tracked** legacy `*.ready.dispatched` markers of rounds 47–61 and 79–91 (e.g. `.ufo/waves/round-47/w1.ready.dispatched` … `.ufo/waves/round-91/w1.ready.dispatched`), newly matched by the rule. Attribution method: baseline captured with `.gitignore` restored byte-identical (sha256 check), comm with `LC_ALL=C` sort, per-file `--error-unmatch`.

Interpretation for the L1: for tracked files an ignore rule changes no git behavior (they stay tracked; modifications still reported); it only shows in `check-ignore`/`ls-files -ci` metadata. The rule's operative effect is on untracked and future markers — exactly the D3 target. The "prints nothing" criterion is unmeetable at the freeze commit even before any change (baseline 437), so it cannot discriminate this patch; the discriminating criteria (red 1 → green 0, plain `.ready` still 1) all pass.

## 6. Target population in the lane (read-only)

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-files --others --exclude-standard -- .ufo/waves | grep '\.ready\.dispatched$'
# -> .ufo/waves/round-92/w1.ready.dispatched
#    .ufo/waves/round-93/w1.ready.dispatched
#    .ufo/waves/round-94/w1.ready.dispatched
# scan_rc=0   <- exactly the untracked=3 markers named in the contract
```

Lane `.gitignore` blob at base: `git rev-parse 84b15230:.gitignore` -> `8f0b99aef129cc069f0b4c73009ff4a3d547450a` — identical to the patch's before-blob.

## 7. Patch and apply-check

```
mkdir -p .../round-94/w1/patches
git -C "$S/clone" diff -- .gitignore > .../round-94/w1/patches/gitignore-d3.patch   # patch_rc=0
# 184 bytes; sha256 2583705b3781a1bcfdfa8ef50280521cb3114fa125f746169466bfefd61583e7
git clone --shared --no-checkout .../mori-shokunin "$S/verify"
git -C "$S/verify" checkout -q --detach 84b152308fa6c2f224ad75dff68e525dab9057ac   # HEAD -> 84b15230...
test "$(git -C "$S/verify" rev-parse --show-toplevel)" = "$S/verify"   # toplevel OK
git -C "$S/verify" apply --check .../patches/gitignore-d3.patch   # applycheck_rc=0
```

Patch content (single-line addition; applies clean at the entering base):

```
diff --git i/.gitignore w/.gitignore
index 8f0b99ae..47c2c2d1 100644
--- i/.gitignore
+++ w/.gitignore
@@ -3,3 +3,4 @@
 __pycache__/
 *.pyc
 .scratch/
+.ufo/waves/*/*.ready.dispatched
```

## Verdict

- Red 1 → Green 0 naming rule: PASS (observed).
- Plain `.ufo/waves/round-94/w1.ready` stays unignored (rc 1): PASS (observed).
- `ls-files -ci --exclude-standard` empty: FAIL — baseline already 437 tracked-ignored files at the freeze commit; the rule additionally matches 33 tracked legacy dispatched markers. Attribution and counts above; L1 decides whether to keep the rule (no status effect for tracked files) or accept the metadata delta.
- Patch produced and applies clean at base `84b15230`: PASS (observed, `apply --check` rc 0).
- Lane untouched (only this report + patch file written under `w1/`); scratch deleted before yield.
