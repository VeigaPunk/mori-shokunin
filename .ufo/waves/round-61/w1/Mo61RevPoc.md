# Mo61RevPoc — reconstruction of the round-60 C3 proof (Reviewer13) and check of the r61 `r60hole` static arm

Seat: Mo61RevPoc (leaf, read-only on the lane; no commits in the lane, no fleet/sibling writes).
Frozen base: `ac496c7cde8cad965079858accae3bedfe4a73f2`. Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Scratch: `/fast/scratch/hyaku/mori-r61/Mo61RevPoc/` (cleaned before yield; receipts below are copied here).
Clone: `git clone --shared --no-checkout` of the lane into scratch, `rev-parse --show-toplevel` asserted equal to the clone path before every mutation. The only mutation was one scratch-clone commit `dddc3909a36fbbe0a478ccc4b32c52cd14c6aaf6` (parent `ac496c7c`, identity `t <t@t>`, scratch clone only), touching one line of `.ufo/waves/round-60/count-c1.py`. The lane was never mutated.

## Answer

1. **The hole reproduces exactly as Reviewer13 stated.** At a scratch revision whose committed `round-60/count-c1.py` sha is `58314559…` (PIN_C1 in the r60 counter is `795c1f31…`), the pinned r60 `count-c3.py` (sha `fabde06c…`, verified) prints a **met** line and exit 0. The count-c1 mismatch is recorded internally (`failed=['count_c1_sha']`) and discarded, because `met` at `count-c3.py:255` is `c2_ok and toolgate and old_hole and containment and expectgate` and `failed` is printed only when unmet (`:307-308`).
2. **The `containment=ok beside failed=g2_escape_written` shape is reproducible** but it is an *unmet* line, not a met line: `met` requires `containment`, which requires `not (g2.parent/"escape.txt").exists()` (`:227-228`, `:217-219`), and `failed` is printed only on unmet. A met line and a `failed=` suffix cannot co-occur in r60. Trigger: a pre-existing `escape.txt` in the `--scratch` root (`g2.parent`, because `g2 = scratch/"g2"`, `:211`). With that file present, the three materialize refusals still held (failed contains no `g2_parent_escape` / `g2_inside_rejected` / `g2_symlink_escape`), so the lie is produced by the scratch state, not by a containment defect in pinned count-c2.
3. **The r61 `r60hole` static arm correctly asserts the hole over the frozen bytes.** `arm_r60hole(frozen)` returns `(True, '')` (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c3.py:87-103`). It is an honest red-before for the bytes it pins, but its logic has the gaps listed in §4 (static, substring-based, first-match-only), and the selftest's tamper case passes through the sha gate, not the hole logic.

## 1. Live reproduction (commands and receipts)

```
$ git -C "$C" -c user.name=t -c user.email=t@t commit -qam "poc: count-c1 sha != PIN_C1 (scratch only)"
NEW=dddc3909a36fbbe0a478ccc4b32c52cd14c6aaf6 parent=ac496c7cde8cad965079858accae3bedfe4a73f2
committed c1 sha at NEW: 58314559cb6de2fe          # != 795c1f3193a76406… (PIN_C1)

(A) python3 r60-count-c3.py $NEW --repo $C --scratch runA2        # clean scratch
C3=met toolgate=ok containment=ok expectgate=ok cases=6 rev=dddc3909a36fbbe0a478ccc4b32c52cd14c6aaf6
rc=0

(B) same rev, scratch pre-seeded: runB2/escape.txt
C3=unmet toolgate=ok containment=ok expectgate=ok cases=6 rev=dddc39… failed=count_c1_sha,g2_escape_written
rc=1

(B0) control: base rev ac496c7c (c1 pinned), scratch pre-seeded escape.txt
C3=unmet toolgate=ok containment=ok expectgate=ok cases=6 rev=ac496c7c… failed=g2_escape_written
rc=1

base control: unmodified clone at ac496c7c, clean scratch
C3=met toolgate=ok containment=ok expectgate=ok cases=6 rev=ac496c7c…   rc=0
```

Reading: (A) vs base shows the c1 mismatch has zero effect on the verdict. (B) vs (B0) shows the c1 mismatch is independent of the containment token. Both met and unmet forms print `containment=ok`.

In-process (driver `/fast/scratch/hyaku/mori-r61/Mo61RevPoc/drive.py`, imports the pinned r60 module from scratch, no file writes to the lane):

```
A in-process measure at NEW: met=True failed=['count_c1_sha'] {'cases': 6}
G3 forced-miss line: C3=unmet toolgate=ok containment=ok expectgate=ok cases=6 rev=dddc39… failed=count_c1_sha,g3_no_tamper_flag
```

The G3 forced-miss used an in-process monkeypatch of `run_counter` for the `c2-g3.py` run only (no file change). It shows `expectgate=ok` printed beside `failed=g3_no_tamper_flag`: the same token-binding defect on the third gate. Source: `r60 count-c3.py:298-306` (token expressions test the literal `"<tok>" not in failed`, which no append site emits).

Mechanism, from the pinned bytes (`/fast/scratch/hyaku/mori-r61/Mo61RevPoc/r60-count-c3.py`, sha `fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514`, equal to the contract pin):
- `:146-150` count-c1 sha mismatch appends `count_c1_sha` to `failed`.
- `:255` `met` has no c1 conjunct.
- `:297-309` `failed` is printed only when `met` is false.
- `:221-228` G2 appends `g2_*` names; no `containment` literal is ever appended.
- `:300-305` `containment=ok` iff `"containment" not in failed` and `"g2_skipped" not in failed`; the first is always true, so the token is constant `ok` whenever G2 executed.
- `:298` the same pattern holds for `toolgate` and `expectgate`.

## 2. Frozen-counter arm check (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c3.py`)

Source-level run of `arm_r60hole` (module loaded from the lane path, bytecode writes disabled):

```
r61 arm_r60hole(frozen):        (True, '')          # frozen bytes: hole confirmed
variant V0-frozen:              (True, '')
variant V1-c1-conjunct:         (False, 'r60_hole_absent')
variant V2-containment-appended:(False, 'r60_append_site:containment')
variant V3-tokentest-removed:   (True, '')          # see §4a
variant V4-later-met-conjunct:  (True, '')          # see §4b
variant V5-single-quote-append: (True, '')          # see §4c
r60-tamper arm result:          (False, 'r60_bytes_pin')   # see §4d
```

Selftest (run from the lane root, read-only, scratch writes only): `C3_SELFTEST pass=8 fail=0`, rc 0.

Variants V1-V5 patch only the in-memory `R60_SHA` on the imported module so the logic is reached; the lane file is untouched.

## 3. Static arm vs live PoC: where the stories agree and diverge

Agree:
- Cause: the r60 `met` has no c1 conjunct (static arm `:94`; live `:255`, A-run shows `met=True` with `count_c1_sha` in `failed`).
- Printed-token defect: no `containment` / `toolgate` / `expectgate` append site (static arm `:99`; live `:300-305`).

Diverge (report-only; no fix applied):
- **D1. The live lie is constant-true, not a containment-only effect.** Once G2 runs, `containment=ok` prints regardless of r1/r2/r3 or the escape check (live `:300-302`). The static arm's "no append site" test captures the cause, but it does not state that the printed token is a function of `g2_skipped` alone. A repaired token that tests the real containment boolean would still have to be distinguished from this.
- **D2. The B-run trigger is a scratch-root artifact.** `containment=ok beside failed=g2_escape_written` appears only when `--scratch/escape.txt` pre-exists (because `g2.parent` is the scratch root). The static arm and the selftest never model that environment input; it appears only in the live PoC.
- **D3. The static arm proves shape, not output.** It reads bytes and never runs the r60 counter, so the printed `met` line and the `failed` list are not observed by the arm. Only §1 shows the lie in output.

## 4. Defects in the static arm and selftest (findings; counters are frozen; no amendment proposed)

a. **Substring test without boundaries.** `r61 count-c3.py:101` checks `f'"{tok}" not in failed' in text` as a substring. V3 replaces `"containment" not in failed` with `"containment" not in failedX`, and the arm still returns True. The token-binding check is blind to the identifier it names.

b. **First-match-only met parse.** `:91` uses `re.search` and reads only the first line matching `^\s*met = \((.*)\)`. V4 appends `met = met and c1_ok` after the real met line, which closes the live hole (`met` then carries c1), and the arm still returns True ("hole present"). False red-before, not a false green on the frozen bytes.

c. **Quote-sensitive append check.** `:99` searches for `failed.append("<tok>"` with double quotes only. V5 (single-quoted append) closes the live hole and the arm still returns True.

d. **The selftest tamper case does not exercise the hole logic.** `r61 count-c3.py:238-243` ("r60-tamper-detected") tampers the r60 bytes, but `arm_r60hole` refuses them at `:88` on the sha pin (`(False, 'r60_bytes_pin')`), so `not b["r60hole_ok"]` holds for a reason unrelated to the hole. A broken `"c1" in` / append / token check would not fail the selftest. The "r60hole-real-bytes" case (`:261`) passes only on the frozen bytes.

## 5. Verdict on the question asked

- The r60 hole reproduces end-to-end as Reviewer13 stated (§1, A and B).
- The r61 `r60hole` arm asserts the hole correctly over the frozen bytes (§2, V0 True).
- The arm's logic and its selftest are weaker than the live PoC (§4a-d); the static story omits the scratch-root trigger (D2) and the constant-token nature of the printed tokens (D1). These are findings to route to the lesson; no counter edit, no amendment proposed here.

## Confidence and limits

- High: the live reproduction and the r60 bytes (sha-checked: `fabde06c…`, PIN_C1 `795c1f31…`, PIN_C2 `8c4814f5…` for the r60 c2 pin at `ac496c7c`).
- High: arm behaviour on variants V0-V5 and the tamper path (executed).
- Medium: whether D1-D3 meet the frozen kill rule; that is the L1's call.
- Not run: any r60 check against the lane's committed round-61 counter files at a rev containing them (r61 counters absent at `ac496c7c`; the r61 live arm at the PoC rev reports `livepins=FAIL` as expected).

## Tooling

No tools installed or updated. Only `git`, `python3` (system), `sha256sum`. No pacman.

## Receipts (small, copied into this report)

- `sha256(r60 count-c3 at ac496c7c) = fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514` (matches R60_SHA).
- `sha256(r60 count-c1 at ac496c7c) = 795c1f3193a76406a40561ac60fedb3eee75fc38df2b2efb3fc5295d617ddbae` (= PIN_C1 in r60 counter).
- `sha256(r60 count-c2 at ac496c7c) = 8c4814f54c564a7f00beec5249de092a2d3b2c4043e07be773d80e8e3ccdf976`.
- `sha256(r61 count-c1) = a6684e69…` (= PIN_C1 in r61), `sha256(r61 count-c2) = 82d0fee6…` (= PIN_C2 in r61), both in the lane worktree.
- PoC commit `dddc3909…` (scratch clone only) c1 blob sha `58314559cb6de2fe…`.

Scratch cleaned after this report was written.
