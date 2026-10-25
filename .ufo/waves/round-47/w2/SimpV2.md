# SimpV2 — simplicity pass over v2 `tools/mori-pin-check.py` at T

Seat: SimpV2 (leaf, no subagents). Target: **v2 `tools/mori-pin-check.py` at landed tip T
(`68d66ca53d89be5c34a62f46af7c37449d9f9b63`)** — dead code, duplicated logic (pin_keys vs
pin_bindings vs the check loop), unused constants. Method: analyze T bytes; prove every proposed
deletion on a scratch copy (`+ --selftest`); never edit tracked files.

- Working-tree `tools/mori-pin-check.py` == T blob (git rev-parse T:… = git hash-object = `a2dfb73ad9b58f69c318d088dd312ff980aa6f6d`); scratch copy sha256 `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6`.
- No tools were installed (none needed); operator RULES.md read; no pacman transaction attempted.

## Verdict

**Attacks confirmed; every proposed deletion is proven behavior-preserving on the full selftest
suite (34/34 arms) and on the real registry at T.** No unused constants and no unreachable
functions exist. The duplication is real and is consolidated without changing a single output byte.

## Findings

### F1 — duplicated SELFTEST-prefix regex (pin_keys vs pin_commands)
`pin_keys` re-implements tally-pin extraction with its own regex
`re.match(r"([A-Z][A-Z0-9_]*SELFTEST)", m.group(1))` over the same `SPAN_RE` walk that
`pin_commands` already does (`re.match(r"([A-Z][A-Z0-9_]*SELFTEST)(.*)$", span, re.S)`). Two
copies of the pin-recognition rule. **Deletion:** `pin_keys` now reuses `pin_commands` (via the
shared cell-level iterator of F2); the second regex is gone — one source of truth.

### F2 — duplicated ordinal counting + argv normalization (pin_bindings vs check loop)
The same loop body appears twice: ordinal-per-prefix counting and the
`None if words is None else tuple("<REV>" if w == rev else w for w in words)` normalization occur
in `pin_bindings` (baseline side) and inline in the `check()` live loop.
**Deletion:** extracted `normalize_argv(words, rev)` and a cell-level generator
`pin_bindings_cell(cells, idx, rev, eidx)` yielding `(prefix, ordinal, pinned, argv, norm)`;
both `pin_bindings` and the live `check()` loop consume it. One ordinal/normalization rule.

### F3 — command_from_span: duplicated branch + duplicated return guard
The function had an `if "--selftest" not in span:` arm whose tail repeated the exact same
`return argv if argv is not None and argv_ok(argv, rev) else None` as the outer arm, plus an
`argv = None` pre-assignment. **Deletion:** collapsed to a single if/elif/else chain with one
return guard.

### F4 — unused constants: none found
All eight module-level constants are referenced: `TIMEOUT_S`, `HEX_RE`, `PATH_RE`, `SPAN_RE`,
`REV_WORDS`, `INTERPRETERS`, `SAFE_PATH`, `PY_FLAGS` (verified by inspection of every use).
`REV_WORDS`/`PY_FLAGS`/`TIMEOUT_S` are single-use but are not dead — kept (they document intent).
No unreachable function exists: every `def` in the file has at least one caller.

### Applied diff (scratch copy only)
`orig-mori-pin-check.py` (T bytes, 633 lines) → `mori-pin-check-v2.py` (639 lines; +6 net
lines, −1 duplicated regex, −2 duplicated loops, −1 duplicated guard):

1. `command_from_span`: single `if "--selftest" in span / elif .py fullmatch / elif .sh
   fullmatch / else None` + one shared return guard.
2. New `normalize_argv` + `pin_bindings_cell`; `pin_keys` rebuilt on them (duplicated regex
   deleted); `pin_bindings` rebuilt on `pin_bindings_cell`.
3. Live `check()` loop: ordinal dict + inline norm deleted; loop now iterates
   `pin_bindings_cell(cells, idx, rev, row["eidx"])` and uses the yielded `(prefix, n, pinned,
   words, norm)` — identical `bkey`/rebound compare.

## Evidence (all runs: TMPDIR=`/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-SimpV2`, never /tmp)

### Baseline — original T bytes, scratch copy
```
$ python3 .scratch/r47w2-SimpV2/orig-mori-pin-check.py --selftest
… 34 PASS lines …
PIN_CHECK_SELFTEST pass=34 fail=0
EXIT=0
```
Full output: `.scratch/r47w2-SimpV2/baseline.out` (34/34 arms PASS).

### Modified scratch copy, same suite
```
$ python3 .scratch/r47w2-SimpV2/mori-pin-check-v2.py --selftest
PIN_CHECK_SELFTEST pass=34 fail=0
EXIT=0
$ diff .scratch/r47w2-SimpV2/baseline.out .scratch/r47w2-SimpV2/modified.out   # → no output, exit 0
DIFF_IDENTICAL
```
Byte-identical to baseline: every one of the 34 selftest arms (v1 arms + v2 arms + rc/CLI arms)
is preserved exactly, including `v2_rebound_to_other_tool`, `v2_entry_rebound`,
`v2_hidden_row_and_duplicate`, `baseline_row_deleted`, `baseline_all_present` — the arms that
exercise `pin_keys`/`pin_bindings`/rebound.

### Real registry at T — original vs modified, byte-identical
```
$ python3 .scratch/r47w2-SimpV2/orig-mori-pin-check.py --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev 68d66ca53d89be5c34a62f46af7c37449d9f9b63 --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
$ python3 .scratch/r47w2-SimpV2/mori-pin-check-v2.py <same args>
ORIG_EXIT=0  MOD_EXIT=0
REAL_DIFF_IDENTICAL   # diff of the two outputs empty, exit 0
PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=26 rev=68d66ca53d89be5c34a62f46af7c37449d9f9b63 baseline=yes
```
Outputs at `.scratch/r47w2-SimpV2/real-T-orig.out`, `real-T-mod.out`.

### Tracked tree untouched
`git diff 68d66ca -- tools/mori-pin-check.py` → empty; the only lane writes are this report and
scratch under `.scratch/r47w2-SimpV2/`. (Note: `evidence/selftest-pin-check.txt` in the repo is
an older 22-arm receipt predating the v2 arms; the current T tool and the SKILL.md pin both say
`pass=34` — my baseline run above is the current truth.)

## Semantic-caller proof note
No LSP server answers this file (device `xd://lsp` is not mounted; mounted devices are only
ast_edit/debug/tripo/unity-cli) — recorded, per the simplifier rule. Text-grep fallback (not
semantic proof) shows no Python module ever imports `mori-pin-check` or its helpers; all literal
references are SKILL.md registry rows, evidence receipts, and jj op logs. All deleted/consolidated
names (`pin_keys`, `pin_bindings`, inline norms) are internal to this single file.

## Tradeoffs
- +6 lines net for −3 duplicated rule copies; slightly longer file, materially fewer sources of
  truth for pin parsing and ordinal/normalization. Verified byte-identical on 34 selftest arms
  and on the full real-tree run (28 pins + 5 digests + baseline) — no behavioral axis harmed.
- No further deletion is safe: `pin_keys`/`pin_bindings` are still required by the baseline
  dropped/rebound checks; every constant is live; every function is called. The next deletion
  would harm an axis (baseline guarding or error reporting).
- Suggestion for a later round (not done here): none — further simplification would require a
  behavior change, which this seat must not make.
