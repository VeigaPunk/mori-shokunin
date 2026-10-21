# GtLaneKagi: C2 independent ground truth, kagi-shokunin `ufo-swarm-wave-dispatch-v1` files

Seat: MoriR20.GtLaneKagi (leaf, no subagents). Lane `/home/vgpnk/Projects/shokunin/kagi-shokunin` was read only.
Snapshot: **2026-10-21T10:38:39Z** (07:38:39 -0300). The lane is live. Round-25 was dispatched during this run and its counts moved between every scan. The older waves did not change.

**Headline:** 7 dispatch files, 479 members, 479/479 trailers parsed, 384 reports present, 0 empty, 95 missing, 0 misrooted, 0/7 filename flags. The 95 missing are 13 older-wave reports (no file under those names exists anywhere in the fleet tree) plus 82 round-25 reports still in flight.

## 1. Method
- JSON tool: `/usr/bin/jq` 1.8.2-1 (pacman package, called by absolute path). The session `jq` is a shell builtin that maps to jaq 3.1.1 and was not used.
- Schema filter: `jq -r 'if type=="object" then (.schema|tostring) else "NONOBJECT:"+type end'` over every `*.json` under `.ufo/waves`, any depth. `find -name '*.json' | wc -l` agrees (98 at first enumeration, 103 at the final scan).
- Per dispatch file: `.registry.members` keys, `.taskCall.tasks[].name`, `.counts.total`, `.registry.reportDir`, and task-text lines starting with `Report: write your scoped findings to `.
- Parse rule: exactly one such line per task. The path must start with `.ufo/waves/`, contain no whitespace, and contain no `..`.
- Lane status: present = regular file with size > 0; empty = size 0; missing = absent. Misrooted = lane status not present AND `/home/vgpnk/Projects/shokunin/<same relative path>` exists.
- Per-member rows: `mori-shokunin/.ufo/waves/round-20/build/GtLaneKagi/kagi-wave-dispatch-members.tsv` (479 rows, 10:38:39Z).
- Not used: `tools/mori-wave-settlement.py`, `tools/mori-census.sh`, and the frozen oracle `frozen/c2-expected.json` (not opened, for independence).
- Installs or updates: none.

## 2. Schema filter (10:38:39Z)
| top-level `.schema` | JSON files |
|---|---:|
| `ufo-swarm-wave-dispatch-v1` | 7 |
| `ufo-swarm-registry-v1` | 7 |
| absent | 82 |
| numeric `1` (`round-22/falsify/PinPaths/fixture-inputs.json`) | 1 |
| top-level array, no schema | 6 |
| jq parse errors | 0 |

Dispatch files (paths relative to the lane root):
1. `round-22/build-dispatch.json` (wave kagi-r22-build)
2. `round-22/falsify-dispatch.json` (kagi-r22-falsify)
3. `round-23/falsify-dispatch.json` (kagi-r23-falsify)
4. `round-23/parent-build-dispatch.json` (kagi-r23-parent-build)
5. `round-24/build-dispatch.json` (kagi-r24-build)
6. `round-24/falsify-dispatch.json` (kagi-r24-falsify-recovery)
7. `round-25/build-dispatch.json` (kagi-r25-build)

## 3. Per-file totals (10:38:39Z)
| dispatch file | members | trailers parsed / unparsed | present | empty | missing | misrooted | filename flag |
|---|---:|---:|---:|---:|---:|---:|:-:|
| round-22/build-dispatch.json | 64 | 64 / 0 | 60 | 0 | 4 | 0 | no |
| round-22/falsify-dispatch.json | 66 | 66 / 0 | 66 | 0 | 0 | 0 | no |
| round-23/falsify-dispatch.json | 64 | 64 / 0 | 64 | 0 | 0 | 0 | no |
| round-23/parent-build-dispatch.json | 66 | 66 / 0 | 66 | 0 | 0 | 0 | no |
| round-24/build-dispatch.json | 67 | 67 / 0 | 66 | 0 | 1 | 0 | no |
| round-24/falsify-dispatch.json | 64 | 64 / 0 | 56 | 0 | 8 | 0 | no |
| round-25/build-dispatch.json | 88 | 88 / 0 | 6 | 0 | 82 | 0 | no |
| **lane total** | **479** | **479 / 0** | **384** | **0** | **95** | **0** | **0 of 7** |

Also checked for all 7 files: registry member names equal task names and are unique; `counts.total` equals member count; `resumeSends` is empty; `compaction.applied` is false; every trailer path lies under the file's `registry.reportDir`; no two members share a report path; no present file is a `STATUS:` stub (size ≤ 64 bytes): 0.

## 4. Missing reports (95)
Older waves (13):
- **round-22/build (4):** `.ufo/waves/round-22/build/{DraftE1,DraftE3,DraftCriteria,DraftHistory}.md`. `round-22/task-receipt-build.json` reads "Spawned 64 background agents" and lists `KagiR22.DraftE1`, `DraftE3`, `DraftCriteria`, `DraftHistory`. The members were spawned and no report exists. [INFERENCE] not completed, based on absence only.
- **round-24/build (1):** `round-24/build/ProbeAbsPath.md`. `round-24/build-task-result.txt` reads "Spawned 67" and lists `KagiR24.ProbeAbsPath-2`. [INFERENCE] same basis.
- **round-24/falsify (8):** `round-24/falsify/{FIdentityR1110,FIdentityR2104,FPolicyCitations,FNormWhitespace,FSeparability,FMigration,FGateDecisions,FWaveEvidence}.md`. `round-24/falsify-task-result.txt` reads "Spawned 64" and lists all 8 (`KagiR24-2.<name>-9`). That log records `'status': 'pending'` on all 64 entries, so it is a spawn-time record and not a completion record. [INFERENCE] not completed.

Round-25 (82 of 88 pending):
- Timeline. Dispatch file written 07:31:38 -0300. `round-25/build-refusals.json` attempt 1 at 07:32:04 -0300: `refused: 88, started: 0`. The first task log, since overwritten, read "Failed to start background task jobs: … Background job limit reached (100)" with `results: []`. Attempt 2 at 07:35:04 -0300: `refused: 0, started: null`. `round-25/build-task-result.txt` (rewritten 07:35:04) reads "Spawned 88 background agents", with job IDs suffixed `-2`.
- Progress. Reports present: 3 at 10:36:58Z, 6 at 10:38:39Z (ScribeQuality, ScribeSkillRows, ScribeReadmeFrontier, ScribeLog, CritC3, MutCitations). Round-25 is dispatched and in flight, not undispatched. [INFERENCE] the remaining 82 are still running.

## 5. Misrooted
- None of the 479 relative paths exists under `/home/vgpnk/Projects/shokunin` (`fleet_missing` = 479).
- Basename search, `find /home/vgpnk/Projects/shokunin` with node_modules and .git pruned, for the 13 older missing names: no hits.
- Case-insensitive prefix search under `kagi-shokunin/.ufo/waves` for the same names: no hits.
- Positive control on the same find expression within the waves tree: `AttackEntry01.md` and `ScribeQuality.md` were found.

## 6. Filename heuristic (preview | undispatched | validation)
- 0 of the 7 dispatch filenames match.
- Same-named sidecars are outside the filter (not dispatch JSON), and all are 0 bytes: `round-24/falsify-validation.stderr`, `round-25/build-validation.stderr`, `round-23/falsify-dispatch.err`.
- `round-22/falsify/inputs/custom-preview-claim.json` has no schema and is not a dispatch file.

## 7. Parser notes for the C2 tool
- Trailer form: 479 of 479 members have exactly one line matching `^Report: write your scoped findings to `, and the path is the last token. No other trailer form occurs.
- Naive substring matching over-counts. `round-23/falsify` has 115 lines containing `Report:` for 64 tasks, because 51 body lines contain the prose "Write your report at the Report: trailer path (relative to …)". `round-22/falsify` has 82 lines matching `[Rr]eport` for 66 tasks. Anchor on `^Report: write your scoped findings to `.
- Job-ID suffixes differ by log: `-2` (round-24/build, round-25), `-9` (round-24/falsify). Match on member name, not job ID.
- `round-24/fix-task-result.txt` records "Spawned 2 background agents using executor" (including `FixGateConfinement`). The lane has no `fix` dispatch JSON, so a scan keyed on `ufo-swarm-wave-dispatch-v1` misses this wave.
- Dispatch logs exist for round-22 (receipts), round-24/build and round-24/falsify (task results), and round-25 (task result and refusals). None exist for round-23 (either wave). For round-23, the dispatch evidence is the JSON plus the reports, all present.

## 8. Drift between snapshots (use the same snapshot for any pin)
| snapshot | JSON files | dispatch files | members | present | missing |
|---|---:|---:|---:|---:|---:|
| first enumeration, before round-25 files existed | 98 | 6 | 391 | not computed | not computed |
| ~10:32Z, round-25 dispatch written, 0 reports | 101 | 7 | 479 | 378 | 101 |
| 10:36:58Z | 103 | 7 | 479 | 381 | 98 |
| 10:38:39Z (this report) | 103 | 7 | 479 | 384 | 95 |

## 9. Limits
- Snapshot only. Re-scan before pinning, since round-25 changed between each scan.
- "Present" means a non-empty regular file. Content was not validated beyond the STATUS-stub check.
- No log shows completion. Every spawn-time log records `pending` (64 of 64 round-24/falsify, 88 of 88 round-25, 2 of 2 fix).
- `started: null` in round-25 attempt 2 is unexplained. The "Spawned 88" log line is the evidence that attempt 2 started.
- Lane writes: none. Writes made by this seat: this report and `build/GtLaneKagi/kagi-wave-dispatch-members.tsv`.
