PARTIAL — C2 claims HOLD on committed evidence (14/14 frozen, selftest 21/21 re-run here). C1 mechanical claims HOLD only under `LC_ALL=C`; the frozen counting command as written does NOT reproduce "8→0" under this host's `en_US.UTF-8` locale (measured 37→33). C1 semantic adjudication of the two dissent tokens and all wave-2 results are L1-TBD. No census run, no writes to lane/fleet files, no tool installs.

# Scope and method

Seat DraftLog (leaf, no subagents). Read-only on committed history: `git show`, `git diff --quiet`, `jj log --ignore-working-copy`, `jq`/`comm` on committed JSON and text. Named files only; `.ufo/interactive-sessions/`, `.ufo/worktrees/`, `.jj/` not touched. Scratch: `/tmp/r20-draftlog/`, `/tmp/r20-drift-entering.txt`, `/tmp/r20-prepin.txt`. Installs/updates: none (tools used: git, jq 1.8.2 at /usr/bin/jq, python3 3.14.8, comm/sort).

Uncommitted state observed: `.ufo/waves/round-20/wave2-dispatch-receipt.json`, `wave2-run.json`, `wave2-spec.json`, `wave2-task-response.txt`, `wave2-taskcall.json` exist in the working copy and are in no round-20 commit (`jj file list -r 8f8c58e` warns "No matching entries"). Not cited below.

# Draft LOG.md entry (append after LOG.md:1360, EOF)

## Round 20 (mori20attempt1) — classified drift re-pin and per-seat wave settlement — 2026-10-21

Motivation: `corpus/lessons/round-20.md` M1 (round-19 wave 1 returned 64 IDs, kept 16 reports; the gaps were counted by hand at closure) and M2 (r10 drift pin red for nine rounds; r13 register had no class or evidence pointer). Frozen score tie at 5 (depth, freshness, calibration); freshness selected; calibration was selected in rounds 17–19 (`.ufo/waves/round-20/contract.md:1-8`).

Freeze **e4d9384da2a0d7c39387ca29e9fbc7d6a4b2b935** (2026-10-21 07:23 -03): `contract.md` (sha256 prefix `2bbe9d56`), `frozen/c2-expected.json` (14 cases, prefix `0984806922`), `evidence/c1-drift-entering.json` (observed 07:18 -03, before the freeze; census sha `87b8d680…ab28`, rc 1, 50 tokens).

C2 tool, independent oracle, live scans, wave-1 dispatch: **2eeae048c441ba4712c42380c347eb64b5a331fb** (07:47 -03). `tools/mori-wave-settlement.py` (682 lines, blob prefix `c6e60919`); `build/OracleHarness/c2-oracle.py` (drives the tool as a subprocess; does not import it).

C1 register, pin, corpus: **8f8c58ee4d923131cfa61a669777ec481d5eca1d** (07:57 -03). `corpus/evidence/drift-classification-r20.json`, `corpus/evidence/baseline-r20-20261021T1051Z.json` (sha `e528bc15…8433`), `corpus/knowledge/drift-repin-r20.md`, `corpus/knowledge/wave-settlement-r20.md`, `corpus/lessons/round-20.md`, sources S066–S072 (`corpus/SOURCES.md`), QUALITY 64–68 (`corpus/QUALITY.md`), SKILL.md and PROVINCE.md sections, wave-1 reports.

Byte-stability across `2061780..8f8c58e`: `tools/mori-census.sh` unchanged (sha `87b8d680…ab28`); `corpus/evidence/baseline-r10-20261015T2231Z.json` unchanged (sha `0993b235…0478`); frozen `contract.md` and `c2-expected.json` unchanged after `e4d9384`.

## Claims

- **C1 freshness.** Every token of the entering drift is classified from the closed set `census-schema-change | roster-change | live-state | census-regression` with an evidence pointer and reason (50/50). Zero `census-regression`, so the re-pin was permitted by the frozen rule. Re-pinned at 10:53:07Z; post-pin `--drift` at 10:55:31Z returned `MORI_DRIFT: none` rc 0. Carried dissent, not resolved by the author: `-FINDING:WATCHDOG_STALE` and `-FINDING:WAVE_UNSETTLED_AGE` (VolatileContract H2/H3, C1Critic) argue false-clean census-regression; the L1 classed both live-state with `blind_spot` (4 register entries carry `blind_spot`). Adjudication: **L1-TBD** (wave-2 critics and non-author closure).
- **C2 coverage.** `tools/mori-wave-settlement.py` settles per-seat report presence per dispatch file. Frozen 14 cases: capability-absent 14 before, 14/14 matched after, 0 mismatched. Live demonstration: mori round-19 wave 1 `partial`, 16 of 64 present, 48 missing; round-19 wave 2 `partial`, 48 present, 22 missing; round-20 wave 1 `settled`, 76 of 76 at 10:54Z. A missing report is recorded as `missing`, never as dead.
- **Co-evolved refinements (disclosed, not frozen).** R1 last matching trailer line after rstrip; R2 `stub` status for marker-only files (the M3 fix); R3 `name_hint`; R4 `duplicate_of` / `unique_dispatch_sha256`; R5 `duplicate_report_paths`; a missing-`taskCall` case. Seven refinement cases; the frozen 14 are loaded unchanged.

## Measurements

C1 (`.ufo/waves/round-20/evidence/c1-drift-entering.json`, `c1-drift-r10-prepin.txt`, `c1-drift-r20-postpin.txt`):
- Entering 50 tokens. r13 register 42 keys. Unclassified 8 → 0 against the r20 register, when both sorts run under `LC_ALL=C`. Register classes 29 `census-schema-change`, 19 `live-state`, 2 `roster-change`, 0 `census-regression`.
- Pre-pin `10:51:14Z` 49 tokens, rc 1; the only change from entering is `-FINDING:WATCHDOG_STALE` (STALE firing again). Unclassified 7 → 0.
- Post-pin `10:55:31Z` `MORI_DRIFT: none` rc 0 (`c1-drift-r20-postpin.txt`).
- Stability window: a scratch pin at 10:22:12Z drifted within 65 s (lane row-A→row-6 move, `build/TokPinFlap.md`). `MORI_DRIFT: none` means unchanged since pin, not healthy.

C2 (`evidence/c2-before.json`, `c2-after.json`, `c2-after-oracle-v0-fixture-defect.json`, `c2-live-mori.json`, `c2-live-fleet.json`, `wave1-settlement-scan.json`):
- Counting command `jq -s '[.[].counts.capability_absent]' c2-before.json c2-after.json` = `[14,0]`; `.counts.matched` = 14.
- Oracle v0 scored 13/14 on a fixture defect (`taskCall: {"tasks": null}` for the frozen `no-spawn` case). Harness repaired to `taskCall: null`; v0 bytes and red result retained.
- Fleet (21 lanes, `mori-r20-fleet-live-v1`, ~10:46Z): 196 waves, 12,307 members, 10,678 present, 1,622 missing, 1 misrooted (souji-shokunin), 45 unreadable JSON. Exit 0 on 6 lanes (no waves), exit 1 on 15. Revenger: 1 wave, 0 of 32 present. Per-wave identity not recorded in that file. Mori: 671 members, 580 present, 85 missing, 2 unreadable JSON.
- Mori wave-1 scan at 10:54Z (`wave1-settlement-scan.json`): 11 waves, 8 settled, 3 partial, 671 members, 586 present, 85 missing, stub 0, unparsed 0, unsafe 0, `ignored_json` 475, `unreadable_json` 2, 11 unique dispatch SHA-256.

## Mistakes (lesson table; fix and fail-capability in corpus/lessons/round-20.md)

M1 wave settlement (`SURFACE waves` grades directories only) → C2 tool. M2 carried-red freshness → closed-class register and counting command. M3 vacuous count: 18 `STATUS: started` markers counted present at ~10:40Z → `stub` status (R2). M4 oracle fixture defect → harness repaired, v0 kept. M5 frozen-text number error ("nine census revisions" vs seven; "found only by hand" wording) → erratum in the lesson, frozen bytes unchanged. M6 classification dispute (WATCHDOG_STALE / WAVE_UNSETTLED_AGE) → `blind_spot` field; adjudication L1-TBD. M7 misroot of DraftProvince to the fleet root, self-detected, stray file removed; fleet `.ufo/waves/round-20/final/AuditCase07.md` belongs to souji and is not touched. M8 scope: broad greps surfaced snippets from `.ufo/interactive-sessions/*.jsonl`; not opened or quoted; disclosed, no compliance credit.

## Dead seats

- Round-20 wave 1 (mori-r20-build; dispatch 10:26:45Z–10:27Z, one batched task call, taskCall sha `cd8bcea3…6295`): 76 spawned, 76 IDs returned, 0 replacements (`wave1-dispatch-receipt.json`). Reports 76/76 present at 10:54Z. At ~10:46Z 70 present and 6 `stub` (`c2-live-mori.json`), so the 6 were marker-only then and non-stub by 10:54Z.
- Dead seats reported: **0**. The tool has no dead/failed state by design. No provider failure or cancellation appears in the committed wave-1 artifacts (text search; only task names matched).
- Carried, unchanged: round-19 wave 1 16 reports, 8 observed provider failures, 1 cancellation, 39 unknown-cause seats; round-19 wave 2 48 reports, 22 provider failures (`LOG.md:1354-1356`). These are not reclassified here.
- Wave 2 (round-20 falsify): **L1-TBD**; receipts exist only uncommitted in the working copy.

## Re-verification

- Committed receipt: post-pin `MORI_DRIFT: none`, rc 0 (`c1-drift-r20-postpin.txt`).
- Seat recheck (no census run): `comm` with `LC_ALL=C` on one sort only, as written in `contract.md:36-41`, returns **37** on the r13 register and **33** on the r20 register under this host's `en_US.UTF-8`. Both sorts under `LC_ALL=C` return **8** and **0**. The `comm` sort warnings ("file 1 is not in sorted order") are the cause. `build/DraftDriftNote.md:42` already recorded this. The frozen counting command must be run with `LC_ALL=C` on both sorts; frozen bytes unchanged.
- Set recheck, pre-pin file: 49 tokens; unclassified 7 vs r13, 0 vs r20 (`LC_ALL=C`).
- No committed counting-command output file exists for "8→0"; the number is recorded in `corpus/knowledge/drift-repin-r20.md:54` only.
- Frozen hashes: `contract.md` `2bbe9d56…` and `c2-expected.json` `0984806922…` at `e4d9384` (unchanged through `8f8c58e`); `mori-census.sh` `87b8d680…` at `8f8c58e` (unchanged vs `2061780`); r10 baseline `0993b235…` unchanged; r20 baseline `e528bc15…`.
- C2 selftest run from lane root: `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (21 cases, 21 passed, 0 failed)`, rc 0; lane tool byte-equal to blob `2eeae04`. Caveat: run from a `/tmp` copy it prints `FAIL (0 cases, 0 passed, 0 failed)`, rc 1, because the frozen oracle is located by walking up from the tool path. It reports FAIL, not a capability error.
- Post-pin re-verification at a later time: **L1-TBD**.

## L1-TBD

- C1 adjudication of `-FINDING:WATCHDOG_STALE` and `-FINDING:WAVE_UNSETTLED_AGE` (dissent recorded in register `dissent` and knowledge §3), and any non-author sign-off of the register.
- Wave-2 falsify results and their settlement scan.
- Whether to amend the C1 counting command text (locale) in a later round; the frozen bytes stay as they are.
- Final C2 numbers after wave 2 and the non-author closure; QUALITY 64–68 status.

# Other notes for the L1

- The lesson and knowledge do not state the locale dependence of the frozen C1 command. Recommend a sentence in `drift-repin-r20.md` §4 and in the LOG entry above.
- `wave1-settlement-scan.json` (10:54Z) and `c2-live-fleet.json` (~10:46Z) differ by exactly the 6 stubs in mori (586 vs 580 present). Both are consistent; they are different times.
- `c2-live-fleet.json` uses schema `mori-r20-c2-fleet-live-v1` (a harness wrapper), not the tool's `mori-wave-settlement-v1`, and carries no per-wave detail for revenger; state that in the entry if the fleet totals are quoted.
