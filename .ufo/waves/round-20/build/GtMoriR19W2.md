# GtMoriR19W2: C2 independent ground truth for round-19 wave 2

Seat: GtMoriR19W2 (leaf; manual; no subagents). Method: `jq`, `test`/`stat`/`ls` only. No candidate tool, no census, no lane or fleet writes. Installs or updates: none. Scratch files: `.ufo/waves/round-20/build/GtMoriR19W2/`.

Source: `.ufo/waves/round-19/wave2-run.json`, wave `mori-r19-attempt2-falsify`, schema `ufo-swarm-wave-dispatch-v1`.

## Totals

| Item | Count |
|---|---:|
| Tasks in `taskCall.tasks[]` (distinct names) | 70 |
| Tasks with exactly one `Report: write your scoped findings to <path>` line | 70 (last = only) |
| present (regular, non-symlink, >0 bytes) | 48 |
| empty (0 bytes) | 0 |
| missing | 22 |
| symlink / other type | 0 / 0 |
| misrooted (same relative path exists under `/home/vgpnk/Projects/shokunin`) | 0 of 70 |

Result: every recorded closure count for this wave agrees with the ground truth (70 returned, 48 reports, 22 provider failures, 0 replacements). No discrepancy found.

## name|status

All 70 report paths are `.ufo/waves/round-19/falsify/<name>.md`, relative to `/home/vgpnk/Projects/shokunin/mori-shokunin`.

```
name|status
F1CompleteSafe|missing
F1MissingReview|missing
F1DuplicateReview|missing
F1UnknownDecision|missing
F1DigestDrift|present
F1PrivateContent|missing
F1ProvenanceOnly|present
F1OutOfPopulation|present
F1InvalidRevision|present
F1TamperedPopulationPin|present
F2MeasuredRevisionFullOid|present
F2RegisterSha256|present
F2CorrectionsSha256|missing
F2ScriptSha256|present
F2ResolvedBasePerClaim|present
F2ResolvedTipPerClaim|missing
F2OverrideRecorded|missing
F2CommandArgv|missing
F2Check18|missing
F2SameVerdictsAsBase|present
F2NoPrivateValues|present
F2Check21|present
BindingDirtyRegister|missing
BindingExternalRegister|present
BindingDirtyCorrections|missing
BindingExternalCorrections|present
OldBeforer17C1|present
OldBeforer17C2|present
OldBeforer17C3|present
OldBeforer18C1|present
OldBeforer18C2|present
OldBeforer18C3|present
OldAfterr17C1|present
OldAfterr17C2|present
OldAfterr17C3|present
OldAfterr18C1|present
OldAfterr18C2|present
OldAfterr18C3|missing
Decision01|missing
Decision02|missing
Decision03|present
Decision04|present
Decision05|present
Decision06|present
Decision07|missing
Decision08|missing
Decision09|present
Decision10|present
Decision11|present
Decision12|present
Decision13|present
Decision14|missing
Decision15|present
Decision16|present
Decision17|present
Decision18|present
Decision19|present
Decision20|present
SourceS064|missing
SourceS065|present
SourceS055|present
SourceS057|present
SourceS059|present
SourceS063|missing
CriticCoverage|present
CriticAttribution|missing
CriticNoHarm|present
ConnectFinal|missing
SentinelOutput|present
HomeSix|present
```

Totals: present 48, missing 22, empty 0, misrooted 0, total 70.

## Method and evidence

1. `jq` over `taskCall.tasks[]`: each `task` string was split by line and matched on `Report: write your scoped findings to`. All 70 tasks matched exactly one line. Every path ends in `.md` and contains no spaces, backticks or quotes. Output: `build/GtMoriR19W2/tasks.tsv`.
2. For each path, the primary check tested the symlink case first (`[ -L ]`), then regular file (`[ -f ]`) with `stat -c %s` > 0 for present. Missing is the no-entry case. The misrooted check ran the same tests on `/home/vgpnk/Projects/shokunin/<rel>`. Output: `build/GtMoriR19W2/status.tsv`.
3. The directory chain `.ufo`, `.ufo/waves`, `.ufo/waves/round-19`, `.ufo/waves/round-19/falsify` is real directories per `stat -c %F`, with no symlinked component. The fleet root has `.ufo/waves/` but no `round-19/` (`stat` ENOENT), so no misrooted copy can exist for this wave.
4. The `falsify/` directory holds 49 entries: 48 `.md` reports plus `swarm-registry.json` (10603 B, not a member report, excluded). The 48 present files are exactly the `falsify/` `.md` set.

## Recorded-count comparison (read-only)

| Source | Recorded for wave 2 | Ground truth | Verdict |
|---|---|---|---|
| `wave2-settlement.json` `returned_agent_ids` | 70 | 70 tasks | match |
| `wave2-settlement.json` `reports_present` | 48 names | 48 present | match, set-equal (`comm` diff empty) |
| `wave2-settlement.json` `provider_failed_no_report` | 22 names | 22 missing | match, set-equal (`comm` diff empty) |
| `wave2-settlement.json` `replacements`, `slot_released` | 0, true | no filesystem equivalent | recorded; not independently checkable |
| `wave2-attempts.json` (attempt 1, 2026-10-21T05:49:29-03:00) `tasks_count`, `started_ids` | 70, 70 | 70 | match |
| `wave2-actual-ids.json` | 70 unique IDs | 70 task names | match: ID suffixes equal the 70 names (`comm` diff empty) |
| `LOG.md` lines 1354-1356 (round-19 section) | 48 reports, 22 provider failures | 48, 22 | match |
| `MANIFEST.json` `.rounds[398].notes` (round 19, lane mori, closure) | W2: 70 returned IDs, 48 reports, 22 provider failures, 0 replacements | 70, 48, 22, 0 | match |
| `SCORECARD.md` round-19 section, lines 1153-1231 | no wave-2 count recorded (line 1216 "census134/134" is a different measure) | n/a | nothing to compare |

Other wave-count sentences belong to other rounds and were not compared:
- `LOG.md` 1187-1188 and 1282-1283 (round-17 section, 70/70 build and 64/64 falsify).
- `SCORECARD.md` 1135 (round-18 section, w2 67 seats).
- `SCORECARD.md` 997-999 and `LOG.md` 1025-1028 (round-16 section, wave 2 skipped).

No round-19 misroot count appears in LOG or SCORECARD. Round-16/17 misroot counts (`LOG.md` 1105-1109, 1280-1281; `SCORECARD.md` 998) are other rounds. The round-19 `evidence/misroot-sweep.json` records `own_candidates` 0, `moves_or_deletions` 0, `exit_code` 0 for a fleet-root `git status` taken after the round-19 workers settled. That is a point-in-time observation and agrees with misrooted = 0.

## Caveats

- `present` is a size test only. Report contents were not read or judged.
- `wave2-settlement.json` sets `reports_are_author_side_not_independent_closure: true`. The 48 are author-side reports, not independent closure. A tool's "closure" label must not be derived from them.
- `error_classes` in the settlement (`turn_rate_limit_exceeded after5 retries`, `HTTP429 vendor type1302 after5 retries`) are recorded cause text and were not verified.
- The 48 present files have mtimes from 2026-10-21 05:52:07 to 06:15:22 (-03:00), after the wave-2 dispatch at 05:49:29. That is consistent with this attempt, not stale output. [INFERENCE: no stale output contradicts it.]
- Wave 1 (64 seats) was out of scope and not compared.
- `payload_sha256` in `wave2-attempts.json` was not verified.
- `settlement.native_calls` = 1 was not compared.

## For L1 acceptance

Expected candidate values for this wave: total 70, present 48, empty 0, missing 22, misrooted 0, returned 70, replacements 0. The missing set must equal `settlement.provider_failed_no_report` (22 names). The present set must equal `settlement.reports_present` (48 names).
