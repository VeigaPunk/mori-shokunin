# GtLaneTabi: C2 independent ground truth for tabi-shokunin dispatch files

STATUS: complete. Read-only. No lane file edited. No installs or updates. No subagents.

- Seat: MoriR20.GtLaneTabi (leaf). Lane root: `/home/vgpnk/Projects/shokunin/tabi-shokunin`. Fleet root: `/home/vgpnk/Projects/shokunin`.
- Snapshot **T2 = 2026-10-21 07:36:48 to 07:36:54 (-03:00)**. The lane is live (round-20 in flight), so all counts are for this snapshot. §6 gives the drift from the first pass.
- Computed independently of the tool under test. `tools/mori-wave-settlement.py`, `tools/mori-census.sh` and `frozen/c2-expected.json` were not opened or run.

## 1. Method

- Discovery: `os.walk` over `.ufo/waves/` (hidden directories included, symlinks not followed), regular `*.json` only.
- Schema, per file: `/usr/bin/jq -c 'if type=="object" then {top:"object", schema:(.schema)} else {top:type} end'`. Dispatch means `.schema == "ufo-swarm-wave-dispatch-v1"` exactly.
- Members: `/usr/bin/jq -c '{wave, taskCall_null:(.taskCall==null), counts_total:.counts.total, tasks:[(.taskCall.tasks//[])[]|{name,agent,task}]}'`. Member count = `len(taskCall.tasks)`. `taskCall: null` = no-spawn.
- Trailer: a task line matching `^Report: write your scoped findings to (\S+)$`. "any" = some line matches (the last match is used). "final" = the matching line is the last line of the task text.
- Path status (`lstat`, `isfile`, `getsize`): present = regular, non-symlink, size > 0. empty = size 0. missing = absent. misrooted = missing under the lane root and a regular non-symlink file at the same relative path under the fleet root.
- The bare `jq` in the bash tool is a shell builtin that reports `jaq 3.1.1`. It was not used. `/usr/bin/jq` and `~/.local/bin/jq` both report `jq-1.8.2`; `/usr/bin/jq` was used.
- Evidence files (seat-owned only): `.ufo/waves/round-20/build/GtLaneTabi/members.tsv` (3932 member rows), `files.tsv` (67 file rows, full sha256), `summary.json` (lane totals, T2 window, first-pass record).

## 2. Discovery (T2)

| item | count |
|---|---|
| regular `*.json` under `.ufo/waves/` | 5160 |
| unreadable JSON (jq exit != 0) | 0 |
| symlinks, not followed | 6: 3x `alias.json` -> `../target.json` (target schema `tabi-webmcp-validation-cases-v1`), 3x `fixture-symlink.html` |
| non-dispatch regular JSON (ignored by exact match) | 5093, including 100 top-level arrays, 11 `ufo-swarm-wave-v1` plan files, 102 `ufo-swarm-registry-v1` |
| **dispatch-schema files** | **67** = 16 canonical + 51 under `final-clones/` (ExecFixtures 17, ExecFrozen 17, ExecCounter 17) |

## 3. Per-file totals (67 files, T2)

Legend: `[EF]` = `final-clones/ExecFixtures/.ufo/...`. `[FZ]` = `final-clones/ExecFrozen/.ufo/...`. `[EC]` = `final-clones/ExecCounter/.ufo/...`. `rounds/fleet-r1/` = `.ufo/rounds/fleet-round-1-interactive-20261015/`. Other paths are under `.ufo/waves/`.
"trailer any/final" = members whose task has a matching trailer line / whose matching trailer is the final line. Unparsed (any line) is 0 in every row. empty is 0 and misrooted is 0 in every row. name-suspect = basename contains `preview`, `undispatched` or `validation`.

| # | dispatch file | wave | taskCall | members | trailer any/final | present | empty | missing (misrooted) | name-suspect |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `round-12/w1/dispatch.json` | tabi-round-12-w1 | set | 32 | 32/32 | 0 | 0 | 32 (0) |  |
| 2 | `round-13/w1/dispatch.json` | tabi-round-13-w1 | set | 32 | 32/32 | 0 | 0 | 32 (0) |  |
| 3 | `round-14/w1/dispatch.json` | tabi-round-14-w1 | set | 32 | 32/32 | 32 | 0 | 0 (0) |  |
| 4 | `round-15/w1/validation.json` | tabi-round-15-w1 | set | 64 | 64/64 | 49 | 0 | 15 (0) | Y |
| 5 | `round-15/w2/validation.json` | tabi-round-15-w2 | set | 32 | 32/32 | 32 | 0 | 0 (0) | Y |
| 6 | `round-16/w1/validation.json` | tabi-round-16-w1 | set | 84 | 84/84 | 78 | 0 | 6 (0) | Y |
| 7 | `round-16/w2/validation.json` | tabi-round-16-w2 | set | 73 | 73/73 | 73 | 0 | 0 (0) | Y |
| 8 | `round-17/w1/validation.json` | tabi-round-17-w1 | set | 86 | 86/86 | 86 | 0 | 0 (0) | Y |
| 9 | `round-17/w2/validation.json` | tabi-round-17-w2 | set | 78 | 78/78 | 52 | 0 | 26 (0) | Y |
| 10 | `round-18/w1/validation.json` | tabi-round-18-w1 | set | 70 | 70/70 | 70 | 0 | 0 (0) | Y |
| 11 | `round-18/w2/validation.json` | tabi-round-18-w2 | set | 80 | 80/80 | 80 | 0 | 0 (0) | Y |
| 12 | `round-19/w1/validation.json` | tabi-round-19-w1 | set | 72 | 72/72 | 72 | 0 | 0 (0) | Y |
| 13 | `round-19/w2/dispatch.json` | tabi-round-19-w2 | set | 72 | 72/72 | 70 | 0 | 2 (0) |  |
| 14 | `round-19/w2/validation.json` | tabi-round-19-w2 | set | 72 | 72/72 | 70 | 0 | 2 (0) | Y |
| 15 | [EC] `rounds/fleet-r1/wave-validation.json` | — | null | 0 | 0/0 | 0 | 0 | 0 (0) | Y |
| 16 | [EC] `rounds/fleet-r1/wave.dispatch.json` | tabi-fleet-r1-interactive-20261015 | set | 32 | 32/0 | 0 | 0 | 32 (0) |  |
| 17 | [EC] `round-12/w1/dispatch.json` | tabi-round-12-w1 | set | 32 | 32/32 | 0 | 0 | 32 (0) |  |
| 18 | [EC] `round-13/w1/dispatch.json` | tabi-round-13-w1 | set | 32 | 32/32 | 0 | 0 | 32 (0) |  |
| 19 | [EC] `round-14/w1/dispatch.json` | tabi-round-14-w1 | set | 32 | 32/32 | 32 | 0 | 0 (0) |  |
| 20 | [EC] `round-15/w1/validation.json` | tabi-round-15-w1 | set | 64 | 64/64 | 49 | 0 | 15 (0) | Y |
| 21 | [EC] `round-15/w2/validation.json` | tabi-round-15-w2 | set | 32 | 32/32 | 32 | 0 | 0 (0) | Y |
| 22 | [EC] `round-16/w1/validation.json` | tabi-round-16-w1 | set | 84 | 84/84 | 78 | 0 | 6 (0) | Y |
| 23 | [EC] `round-16/w2/validation.json` | tabi-round-16-w2 | set | 73 | 73/73 | 73 | 0 | 0 (0) | Y |
| 24 | [EC] `round-17/w1/validation.json` | tabi-round-17-w1 | set | 86 | 86/86 | 86 | 0 | 0 (0) | Y |
| 25 | [EC] `round-17/w2/validation.json` | tabi-round-17-w2 | set | 78 | 78/78 | 52 | 0 | 26 (0) | Y |
| 26 | [EC] `round-18/w1/validation.json` | tabi-round-18-w1 | set | 70 | 70/70 | 70 | 0 | 0 (0) | Y |
| 27 | [EC] `round-18/w2/validation.json` | tabi-round-18-w2 | set | 80 | 80/80 | 80 | 0 | 0 (0) | Y |
| 28 | [EC] `round-19/w1/validation.json` | tabi-round-19-w1 | set | 72 | 72/72 | 72 | 0 | 0 (0) | Y |
| 29 | [EC] `round-19/w2/dispatch.json` | tabi-round-19-w2 | set | 72 | 72/72 | 70 | 0 | 2 (0) |  |
| 30 | [EC] `round-19/w2/validation.json` | tabi-round-19-w2 | set | 72 | 72/72 | 70 | 0 | 2 (0) | Y |
| 31 | [EC] `round-20/w1/dispatch.json` | tabi-round-20-w1 | set | 64 | 64/64 | 63 | 0 | 1 (0) |  |
| 32 | [EF] `rounds/fleet-r1/wave-validation.json` | — | null | 0 | 0/0 | 0 | 0 | 0 (0) | Y |
| 33 | [EF] `rounds/fleet-r1/wave.dispatch.json` | tabi-fleet-r1-interactive-20261015 | set | 32 | 32/0 | 0 | 0 | 32 (0) |  |
| 34 | [EF] `round-12/w1/dispatch.json` | tabi-round-12-w1 | set | 32 | 32/32 | 0 | 0 | 32 (0) |  |
| 35 | [EF] `round-13/w1/dispatch.json` | tabi-round-13-w1 | set | 32 | 32/32 | 0 | 0 | 32 (0) |  |
| 36 | [EF] `round-14/w1/dispatch.json` | tabi-round-14-w1 | set | 32 | 32/32 | 32 | 0 | 0 (0) |  |
| 37 | [EF] `round-15/w1/validation.json` | tabi-round-15-w1 | set | 64 | 64/64 | 49 | 0 | 15 (0) | Y |
| 38 | [EF] `round-15/w2/validation.json` | tabi-round-15-w2 | set | 32 | 32/32 | 32 | 0 | 0 (0) | Y |
| 39 | [EF] `round-16/w1/validation.json` | tabi-round-16-w1 | set | 84 | 84/84 | 78 | 0 | 6 (0) | Y |
| 40 | [EF] `round-16/w2/validation.json` | tabi-round-16-w2 | set | 73 | 73/73 | 73 | 0 | 0 (0) | Y |
| 41 | [EF] `round-17/w1/validation.json` | tabi-round-17-w1 | set | 86 | 86/86 | 86 | 0 | 0 (0) | Y |
| 42 | [EF] `round-17/w2/validation.json` | tabi-round-17-w2 | set | 78 | 78/78 | 52 | 0 | 26 (0) | Y |
| 43 | [EF] `round-18/w1/validation.json` | tabi-round-18-w1 | set | 70 | 70/70 | 70 | 0 | 0 (0) | Y |
| 44 | [EF] `round-18/w2/validation.json` | tabi-round-18-w2 | set | 80 | 80/80 | 80 | 0 | 0 (0) | Y |
| 45 | [EF] `round-19/w1/validation.json` | tabi-round-19-w1 | set | 72 | 72/72 | 72 | 0 | 0 (0) | Y |
| 46 | [EF] `round-19/w2/dispatch.json` | tabi-round-19-w2 | set | 72 | 72/72 | 70 | 0 | 2 (0) |  |
| 47 | [EF] `round-19/w2/validation.json` | tabi-round-19-w2 | set | 72 | 72/72 | 70 | 0 | 2 (0) | Y |
| 48 | [EF] `round-20/w1/dispatch.json` | tabi-round-20-w1 | set | 64 | 64/64 | 63 | 0 | 1 (0) |  |
| 49 | [FZ] `rounds/fleet-r1/wave-validation.json` | — | null | 0 | 0/0 | 0 | 0 | 0 (0) | Y |
| 50 | [FZ] `rounds/fleet-r1/wave.dispatch.json` | tabi-fleet-r1-interactive-20261015 | set | 32 | 32/0 | 0 | 0 | 32 (0) |  |
| 51 | [FZ] `round-12/w1/dispatch.json` | tabi-round-12-w1 | set | 32 | 32/32 | 0 | 0 | 32 (0) |  |
| 52 | [FZ] `round-13/w1/dispatch.json` | tabi-round-13-w1 | set | 32 | 32/32 | 0 | 0 | 32 (0) |  |
| 53 | [FZ] `round-14/w1/dispatch.json` | tabi-round-14-w1 | set | 32 | 32/32 | 32 | 0 | 0 (0) |  |
| 54 | [FZ] `round-15/w1/validation.json` | tabi-round-15-w1 | set | 64 | 64/64 | 49 | 0 | 15 (0) | Y |
| 55 | [FZ] `round-15/w2/validation.json` | tabi-round-15-w2 | set | 32 | 32/32 | 32 | 0 | 0 (0) | Y |
| 56 | [FZ] `round-16/w1/validation.json` | tabi-round-16-w1 | set | 84 | 84/84 | 78 | 0 | 6 (0) | Y |
| 57 | [FZ] `round-16/w2/validation.json` | tabi-round-16-w2 | set | 73 | 73/73 | 73 | 0 | 0 (0) | Y |
| 58 | [FZ] `round-17/w1/validation.json` | tabi-round-17-w1 | set | 86 | 86/86 | 86 | 0 | 0 (0) | Y |
| 59 | [FZ] `round-17/w2/validation.json` | tabi-round-17-w2 | set | 78 | 78/78 | 52 | 0 | 26 (0) | Y |
| 60 | [FZ] `round-18/w1/validation.json` | tabi-round-18-w1 | set | 70 | 70/70 | 70 | 0 | 0 (0) | Y |
| 61 | [FZ] `round-18/w2/validation.json` | tabi-round-18-w2 | set | 80 | 80/80 | 80 | 0 | 0 (0) | Y |
| 62 | [FZ] `round-19/w1/validation.json` | tabi-round-19-w1 | set | 72 | 72/72 | 72 | 0 | 0 (0) | Y |
| 63 | [FZ] `round-19/w2/dispatch.json` | tabi-round-19-w2 | set | 72 | 72/72 | 70 | 0 | 2 (0) |  |
| 64 | [FZ] `round-19/w2/validation.json` | tabi-round-19-w2 | set | 72 | 72/72 | 70 | 0 | 2 (0) | Y |
| 65 | [FZ] `round-20/w1/dispatch.json` | tabi-round-20-w1 | set | 64 | 64/64 | 63 | 0 | 1 (0) |  |
| 66 | `round-20/w1/dispatch.json` | tabi-round-20-w1 | set | 64 | 64/64 | 63 | 0 | 1 (0) |  |
| 67 | `round-20/w2/dispatch.json` | tabi-round-20-w2 | set | 64 | 64/64 | 49 | 0 | 15 (0) |  |

## 4. Lane totals (T2)

| metric | lane (67 files) | canonical (16) | clones (51) |
|---|---|---|---|
| members | 3932 | 1007 | 2925 |
| trailer parsed, any matching line | 3932 | 1007 | 2925 |
| trailer parsed, final line | 3836 | 1007 | 2829 |
| trailer mid-text (unparsed under the final-line rule) | 96 | 0 | 96 |
| unparsed, any line | 0 | 0 | 0 |
| present | 3357 | 876 | 2481 |
| empty | 0 | 0 | 0 |
| missing | 575 | 131 | 444 |
| misrooted | 0 | 0 | 0 |
| unsafe / symlink / not-regular | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| no-spawn (`taskCall: null`) | 3 | 0 | 3 |
| name-suspect | 43 | 10 | 33 |

- Final-line reading: parsed 3836, unparsed 96, present 3357, missing 479. All 96 mid-text rows are missing.
- Distinct report paths: 967 (806 present, 161 missing). The 3932 member rows reuse these paths, because each clone tree repeats the canonical paths.
- The 161 missing paths split into: 32 under an absent directory (`.ufo/rounds/fleet-round-1-interactive-20261015/seats/`), 63 with a same-stem non-empty `.txt` sibling, and 66 with no sibling file.

## 5. Findings

**F1. Trailer not on the final line (96 rows).** The three `wave.dispatch.json` files under `rounds/fleet-r1/` ([EF], [FZ], [EC]; 32 members each) end each task with `Report: write your scoped findings to .ufo/rounds/fleet-round-1-interactive-20261015/seats/<Name>.md`, then a blank line, then `| godspeed` as the last line. Observed for member TabiNote01 in the ExecFixtures copy, and for the first task of the lane-root copy. The `seats/` directory does not exist: `.ufo/rounds/fleet-round-1-interactive-20261015/` exists at the lane root and has no `seats/`. No file named after any of the 32 members exists under lane `.ufo/rounds/` or `.ufo/reports/` outside `final-clones`. The lane-root `.ufo/rounds/fleet-round-1-interactive-20261015/wave.dispatch.json` (dispatch schema, 32 tasks, wave `tabi-fleet-r1-interactive-20261015`) and `wave-validation.json` (dispatch schema, `taskCall: null`) are outside `.ufo/waves/`, so they are not in the list.

**F2. `.txt` reports under `.md` trailers (63 rows, canonical).** `round-12/w1` (31 of 32 missing) and `round-13/w1` (32 of 32 missing) have no file at any trailer path, because every trailer ends in `.md`. Of these 64 missing members, 63 have a same-stem non-empty `.txt` in the same directory. Examples: `.ufo/waves/round-12/w1/ApgSource.md` absent; `.ufo/waves/round-12/w1/ApgSource.txt` 11,257 B (first pass). Sibling sizes: round-12 5,302 to 16,917 B; round-13 3,093 to 24,884 B. `AriaEntry` (round-12) has no sibling. Under the trailer contract these are `missing`. I did not count them as present. Whether they should count is a decision for L1.

**F3. Other missing paths have no sibling (66).** round-15/w1 (15), round-16/w1 (6), round-17/w2 (26), round-19/w2 (2; the same 2 paths for dispatch and validation), round-20/w1 (1), round-20/w2 (15). In each case no file with the same stem exists in the directory.

**F4. The only no-spawn files (3).** `rounds/fleet-r1/wave-validation.json` in [EC], [EF] and [FZ]: `taskCall: null`, 0 tasks, `counts.total` 32, no `wave` value. This is the only evidence in the lane that matches "never dispatched" on both the filename and the content.

**F5. The name heuristic conflicts with content for 40 files.** The name flags 43 files, all with `validation` in the basename. No dispatch-schema file has `preview` or `undispatched` in its name. Three of the 43 are F4. The other 40 are `validation.json` (10 canonical, 30 clone). Each has `taskCall` set, 32 to 86 members, and 32 to 86 reports present (minimum 32 and maximum 86 across the 40). By content these waves spawned members and wrote reports, so the name alone does not show they were never dispatched. [INFERENCE: "validation" denotes a validation run, which the files do not record.] `round-19/w2/dispatch.json` and `round-19/w2/validation.json` are byte-identical in every tree (72 members, 70 present).

**F6. The registry gives no dispatch evidence.** Across the 64 files that have registry members, 0 of 3932 member entries carry a non-null `agentId`. Every `kind` is `spawn` [observed: `jq '.registry.members[] | .agentId'`].

**F7. No misrooted reports.** None of the 967 distinct trailer paths exists under `/home/vgpnk/Projects/shokunin` (`lexists` is false for all of them, including the 161 missing). `FLEET/.ufo/waves/round-12/w1` and `FLEET/.ufo/waves/round-20/w2` do not exist. `misrooted` = 0.

**F8. Round-20 is in flight. "Missing" is not "dead".** `round-20/w2/dispatch.json` (mtime 07:22) has 49 present and 15 missing at T2. The missing members are: SemanticLC07, CounterSourceIdentity, CounterManifestShape, CounterDuplicateIds, CounterNoteRows, CounterHeading, CounterPartial, CounterText, CounterGitRevision, WaveTracked, WaveOutScope, WaveSourceEntry, WaveMembership, ReviewBundles, ReviewReturnBoundary. Present report mtimes span 07:23:36 to 07:37:38, and the newest is after the T2 scan end. The peer roster given to this seat lists TabiR20.WaveTracked, TabiR20.WaveSourceEntry and TabiR20.WaveMembership as running. I did not check liveness. Treat the 15 as in flight. [INFERENCE] `round-20/w1` (mtime 06:50) is 63/64, missing member `ExecFixtures`. `round-19/w2` (mtime 05:39) is 70/72, missing `MutateC1` and `SentinelInvoke`, which have no sibling file.

**F9. Clones repeat canonical reports.** 45 of 51 clone dispatch files are byte-identical to a canonical file. The other 6 are the `wave.dispatch.json` and `wave-validation.json` pairs in the three clone trees, identical within each pair. For all 2925 clone member rows, the clone-root path status equals the lane-root status (0 mismatches). Lane-level member totals therefore count the same report paths three times (3932 rows, 967 distinct paths).

**F10. Symlinks.** Six symlinks are not followed (§2). The three `alias.json` targets have schema `tabi-webmcp-validation-cases-v1`, so excluding them does not change the 67.

**F11. Environment.** No install or update was needed. Bare `jq` in the bash tool resolves to a builtin (`jaq 3.1.1`). I used `/usr/bin/jq` (jq-1.8.2) explicitly.

## 6. Drift since the first pass

- First pass (completed before 07:31; 50 files): 3515 regular JSON, 4 symlinks, 50 dispatch files, 2957 members, 2508 present, 449 missing, `round-20/w2` 27 of 64 present.
- `final-clones/ExecCounter/` appeared between the first pass and T2. Its 17 dispatch files have mtime 07:34:25 and mirror ExecFixtures and ExecFrozen (975 members, 827 present, 148 missing per tree).
- `round-20/w2` rose from 27 to 49 present. At T1 (07:35:35) it was 41.
- Net change at T2: files 50 to 67, members 2957 to 3932, present 2508 to 3357 (+849 = +827 ExecCounter, +22 round-20/w2), missing 449 to 575.
- No pre-existing dispatch file was removed. All 50 pre-existing dispatch files have the same sha256 prefix at T2 as in the first pass. The only per-file count change among them is `round-20/w2`.

## 7. Unobserved or inferred

- Seat liveness: no process inspection. The round-20/w2 reading in F8 is [INFERENCE].
- Who created `final-clones/ExecCounter/`, and why: not determined.
- Whether `.ufo/rounds/fleet-round-1-interactive-20261015/seats/` existed earlier: not determined. It is absent now.
- Whether the `.txt` files are the intended report format: [INFERENCE] yes, from their content and naming.
- Stability: the lane was still changing at T1 and T2. Counts after 07:36:54 are not covered.

## 8. Comparison keys for L1 (T2)

- Whole set: dispatch 67; members 3932; present 3357; empty 0; missing 575; misrooted 0; no-spawn 3; mid-text 96; name-suspect 43; ignored non-dispatch regular JSON 5093; symlinks not followed 6.
- Canonical only (16 files): members 1007; present 876; missing 131.
- Final-line reading: parsed 3836; unparsed 96; present 3357; missing 479.
- Round-20/w2 at T2: 49 present of 64.
- Recompute with `files.tsv` sha256 values to confirm the tree state matches before comparing counts.

## 9. Artifacts

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/build/GtLaneTabi/members.tsv`: 3932 member rows (dispatch file, class, wave, member, agent, report path, trailer mode, lane status, same-stem sibling, fleet-root existence, clone-root status).
- `.../GtLaneTabi/files.tsv`: 67 file rows with totals and full sha256.
- `.../GtLaneTabi/summary.json`: lane totals, T2 window, first-pass record.
- Nothing was written in the lane or the fleet root. Scratch pickles are in `/tmp` only.
