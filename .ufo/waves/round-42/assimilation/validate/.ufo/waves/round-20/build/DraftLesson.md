# DraftLesson — round-20 mistake rows M1 and M2

Draft written: `.ufo/waves/round-20/build/DraftLesson/round-20-mistakes.md` (`## Mistakes` table, rows M1 and M2, columns class · evidence pointer · captured-by · fix). Measured commit: `2061780117e6ca637725004897bd288d3ba7e988`. Read-only throughout; no lane, census, baseline, MANIFEST or git-index file was edited.

## Findings

### M1 — round-19 wave 1: 48 missing reports counted only by hand
- Counts re-derived from `.ufo/waves/round-19/wave1-settlement.json` with `jq`: `returned_agent_ids` 64; `reports_present` 16; `known_provider_failed` 8; `known_cancelled` 1; `no_report_terminal_cause_unestablished` 39. Non-present = 8 + 1 + 39 = 48.
- On-disk check: `.ufo/waves/round-19/build/` contains 16 `.md` reports, and their names match the 16 entries in `reports_present` exactly, plus `swarm-registry.json`.
- Dispatch source for the C2 tool: `.ufo/waves/round-19/wave1-run.json` has top-level `schema: ufo-swarm-wave-dispatch-v1` and an embedded `taskCall` with 64 tasks, each carrying a `Report:` trailer (`jq` count 64).
- MANIFEST closure note (mori round 19, `/home/vgpnk/Projects/shokunin/MANIFEST.json` line 10171): "W1 64 returned IDs,16 reports,8 known provider failures,1 cancellation,39 unknown no-report causes (not successful reviews/deaths inferred)". The arithmetic agrees.
- Captured-by: none. `tools/mori-dispatch-ledger.py` contains no report-presence check (grep for `report` returns no lines; its finding codes at :273–302 are start/payload only). `tools/mori-wave-settlement.py` is absent: `git cat-file -e 2061780117e6ca637725004897bd288d3ba7e988:tools/mori-wave-settlement.py` → rc 128.
- Fix (as stated in the row): the C2 tool must be shown to fail on this wave before it counts as a capture. Expected run on the mori lane root: `reports_present = 16` of 64, state `partial`, 48 non-present members listed in `missing`, exit 1, and no `dead`/`failed`/`killed` wording.

### M2 — r10 drift pin red for nine rounds without a complete classification
- Pin: `corpus/evidence/baseline-r10-20261015T2231Z.json`, sha256 `0993b23505deab2aeb05b2309bdf7dd6eaad2b82f27852491352511aa9670478`; only commit touching it is `5be8943` (`git log --follow`). Pin-time receipt `corpus/evidence/pin-r10-20261015T2231Z-drift.log`: `MORI_DRIFT: none`, exit 0.
- Red receipts (exit 1): `corpus/evidence/drift-r12-20261019T2204Z-classification.md` (round 12); `.ufo/waves/round-13/evidence/drift-retained-baseline.json`; `.ufo/waves/round-15/evidence/drift-current.json`; `.ufo/waves/round-20/evidence/c1-drift-entering.json` (rc 1, `token_count` / `unclassified_count` fields present).
- Count re-derived here with the contract's command shape on the captured stdout in `c1-drift-entering.json`: 50 drift tokens; 42 present in `.ufo/waves/round-13/evidence/drift-classification.json`; 8 unclassified (`+FINDING:COREDUMP_NOTICE_JOURNAL_USER`, `+FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER`, `+FINDING:UNIT_FAILURE_OUT_OF_SCOPE`, `+path`, `-FINDING:WATCHDOG_STALE`, `age_s`, `io_avg_unavailable`, `round`).
- The round-13 register's own verdict: "red retained; categories are not a regression-free proof; no re-pin". Round-13 lesson `corpus/lessons/round-13.md:93-95` records "All 42 reported tokens are assigned families"; that is the last complete classification, and it predates the 8 new tokens.
- Prose-only carry (no machine-readable register): `corpus/lessons/round-14.md:33` (re-pin to silence old drift rejected), `corpus/lessons/round-15.md:49`, `corpus/lessons/round-16.md:37` and `:160` (C15-5 carried debt), `corpus/lessons/round-17.md:79`, `corpus/lessons/round-18.md:67`.
- MANIFEST mori closures carry the same debt: round 14 (`notes`: "keep old red drift pin routed pending reasoned semantic review"), round 15 ("retain old red drift-pin debt"), round 16 ("carry r10 drift-pin red without re-pin").
- Gap: neither `corpus/lessons/round-19.md` nor the round-19 MANIFEST closure notes mention the pin. The round-19 red state is therefore [INFERENCE], not observed in a round-19 artifact; it is consistent with the unchanged pin hash and the round-20 red receipt.
- Context for the fix: `.ufo/waves/round-16/build/DraftDebt.md:37-39` claims the committed pair can never go green (69 vs 103 `volatile_fields`). This is that seat's claim; I did not re-verify it. The census sha at the entering tip is `87b8d680…ab28` (`c1-drift-entering.json`), which differs from the r10 pinned census `d7710981…` (`pin-r10-20261015T2231Z-drift.log`).
- Captured-by: none for a complete current classification. The r13 register is partial (42 of 50).
- Fix (as stated in the row): classify every token of the measured output into the closed set with an evidence pointer each; re-pin only if no token is `census-regression`, with a recorded reason; re-run `--drift` on the new baseline and record rc and tokens whatever they are.

## Observations for the C2 and C1 seats (not rows)
1. `.ufo/waves/round-19/wave1-settlement.json` and `wave2-settlement.json` are hand-written records, yet both carry `schema: mori-wave-settlement-v1`, the label the contract assigns to the not-yet-built tool's output. The C2 oracle should not treat that label as evidence that the tool ran.
2. `.ufo/waves/round-19/wave1-taskcall.json` has no top-level `schema` key (keys: `context`, `tasks`). The C2 tool would count it as `ignored_json`. The discoverable dispatch for wave 1 is `wave1-run.json`, which embeds `taskCall`.
3. `.ufo/waves/round-19/wave2-settlement.json` has `returned_agent_ids` 70 and a different key set (includes `reports_are_author_side_not_independent_closure`); I did not reconcile it against MANIFEST's "W2 70 returned IDs, 48 reports".
4. `.ufo/reports/round-15/mori.md` is cited by `corpus/lessons/round-16.md:37`, but no `.ufo/reports/round-15` directory exists in the lane (`ls .ufo/reports` ends at round-9). Not used as evidence here.

## Commands and tooling
- Read/grep: `read`, `grep` on the lane and MANIFEST. One shell `grep -rn` over the whole lane timed out at 300 s; it was my error (it should have been the grep tool), and I did not repeat it.
- Read-only shell: `jq`, `sha256sum`, `git cat-file -e`, `git log --follow`, `git log -1`, `comm`, `sort`, `wc`, `tr`. Scratch files written only to `/tmp/r20_*` (outside the repo; safe to delete).
- Tool installs/updates: none.
- No builds, linters, formatters, census runs (`tools/mori-census.sh` not run), or lane selftests were run.

## Not verified
- The DraftDebt "structurally impossible to go green" claim (see M2 context).
- The round-19 pin state (inferred, not observed).
- Whether the C2 tool, once built, produces `16`/`48` on wave 1; this is the fix's acceptance check and was not run.
