# CaseReview15 — C1 `nested_directories` / `prefix_all`

## Verdict

**Specific falsifier: `nested_directories` does not assert the required relative `key` identity.** The retained current output has correct keys, but the expected case and gate accept a path-collapsed counterexample. `prefix_all` withstands the scoped prefix-attribution attack. This is not a blanket C1 pass.

## Finding — Medium: nested-key contract is not asserted

Amendment A1 defines `key` as the path relative to `--sessions-dir` without `.jsonl` (`.ufo/waves/round-17/contract.md:114`). The `nested_directories` case instead keys `want.seats` by the three stems (`.ufo/waves/round-17/fixtures/seat/expected.json:771-795`). The gate explicitly permits expected seat stems (`tools/mori-round17-seat-regressions.py:27-32`), and `compare_want` falls back to row `seat` when a wanted identifier is not found as a `key` (`tools/mori-round17-seat-regressions.py:1238-1246`). It then checks for missing/unexpected seat classes, not the fixture-relative path (`:1247-1260`). `_validate_seat_item` only checks that a supplied key is a safe string (`:1071-1078`); it does not bind the key to the source file path. For this unfiltered case, the `files_scanned` guard checks the file/row count (`:1428-1435`) but not each row's key.

**Static counterexample (not executed):** keep the three correct `seat`/`class` rows and every other output field, but set `key` to `deep-seat`, `deep-two`, and `shallow-seat` instead of `a/b/c/deep-seat`, `a/b/deep-two`, and `a/shallow-seat`. Those are distinct safe strings; the expected stem identifiers then match via `by_key`, all class/totals/finding checks remain unchanged, and the row count remains three. Thus the gate can report a match while the A1 relative-key contract is violated. The current tool constructs the correct relative key from `os.path.relpath` (`tools/mori-seat-terminal.py:443-447`), and the retained after stdout shows those correct keys (`evidence/seat-after/runs/nested_directories.stdout:1`); that observed good output does not make the expected assertion discriminate the counterexample.

## `prefix_all` — no falsifier found in this scope

The fixture contains genuine near-prefix controls: `SoujiR17-3.W` and `.Z` share the intended stem prefix while `SoujiR17-30.Trap` differs; likewise `TsukuroiR17.X`/`.Y` versus `TsukuroiR17Extra.Xtrap` (`fixtures/seat/PrefixAttribution/{SoujiR17-3.W,SoujiR17-3.Z,SoujiR17-30.Trap,TsukuroiR17.X,TsukuroiR17.Y,TsukuroiR17Extra.Xtrap}.jsonl:2`). The expected map names all seven files with their expected classes (`expected.json:799-827`). The persisted output groups `SoujiR17-30` and `TsukuroiR17Extra` separately from their near matches and gives the expected completed/aborted/quota/rate-limit seat classes (`evidence/seat-after/runs/prefix_all.stdout:1`). The tool derives prefix from the stem before the first dot (`tools/mori-seat-terminal.py:445-450`); the gate requires each row's prefix to equal that derivation (`tools/mori-round17-seat-regressions.py:1046-1050`) and checks `by_prefix` against the row-derived totals (`:1413-1420`). Thus the absence of a literal `want.by_prefix` table does not make attribution vacuous here: changing either a near-match prefix or the resulting aggregate would fail validation.

The class expectations are supported by the synthetic record bytes: the nested fixtures have `assistant/stop`, `toolResult`, and `assistant/aborted` terminals (`fixtures/seat/NestedDirs/a/b/c/deep-seat.jsonl:2`, `a/b/deep-two.jsonl:2`, `a/shallow-seat.jsonl:2`; classifier branches at `tools/mori-seat-terminal.py:251-258`). In `PrefixAttribution`, the two error timestamps are 2,000,000 ms before the pinned `now_ms=1761000000000`, older than the default 900-second settle window; `quota exceeded` maps to quota and `429 rate_limit` to rate limit (`fixtures/seat/PrefixAttribution/SoujiR17-3.Z.jsonl:2`, `TsukuroiR17.Y.jsonl:2`, case args at `expected.json:801-804`; classifier at `tools/mori-seat-terminal.py:257-273`). The other five records are explicit `stop` or `aborted` messages. Both expected cases declare all eight totals, including zeros, and every fixture seat; gate validation requires the complete totals key set (`tools/mori-round17-seat-regressions.py:1018-1027`) and compares wanted totals and seat classes (`:1215-1260`). Both expect rc 0/1, so a setup rc 2 cannot satisfy the case.

## Retained measurements and count

L1 before-manifest entries for both IDs are `capability_absent`, with `observed: null` (`evidence/seat-before/run-manifest.json`, entries `nested_directories` and `prefix_all`). After-manifest entries are `match`, with 3/3 and 7/7 files respectively, exact expected totals, no reasons, and unchanged before/after pack hashes (`evidence/seat-after/run-manifest.json`, same IDs). The retained raw after stdout is at `evidence/seat-after/runs/nested_directories.stdout:1` and `.../prefix_all.stdout:1`; no tool or selftest was run for this review.

Read-only count command:

```sh
jq -s '[.[] | [.cases[] | select(.id == "nested_directories" or .id == "prefix_all")] | length]' \
  .ufo/waves/round-17/fixtures/seat/expected.json \
  .ufo/waves/round-17/evidence/seat-before/run-manifest.json \
  .ufo/waves/round-17/evidence/seat-after/run-manifest.json
```

`rc=0`; output: `[2, 2, 2]` (expected table, before manifest, after manifest).

A read-only `sha256sum` over the ten fixture files returned rc 0 and each digest matched its persisted pin (`fixtures/seat/expected.json:38-53`). The expected table's digest `b684c63bf3cebe70f24d3d02f3f0df4f63aad3f547a365a3ca1864f5f57cb01f` matches `PINNED_INPUTS.json:13`.

## Verification gap

No `lsp` device is mounted: requesting `xd://lsp` returned “No such tool” and listed available devices without an LSP route. Therefore status/references/definition/diagnostics were unavailable; literal grep was used only to locate source lines, not as semantic proof. No installs or updates were made.
