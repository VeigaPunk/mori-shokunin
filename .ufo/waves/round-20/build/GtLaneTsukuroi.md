# GtLaneTsukuroi: C2 independent ground truth for tsukuroi-shokunin `ufo-swarm-wave-dispatch-v1` waves

**Seat:** MoriR20.GtLaneTsukuroi (leaf scout). **Lane:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (read-only; nothing written in the lane). **Fleet root:** `/home/vgpnk/Projects/shokunin`. **Observed:** 2026-10-21, about 07:30 to 07:45 (-03:00). Counts can change while round-20 is still writing.

**Constraints honored:** manual one-off queries only. `tools/mori-wave-settlement.py` and `tools/mori-census.sh` were not run. `frozen/c2-expected.json` was not opened. No subagents. No transcripts or `~/.omp` logs opened. **Installs or updates: none.** Tools used: `/usr/bin/jq` (jq-1.8.2), python3 3.14.8 stdlib (`json`, `os`, `re`), `stat`, `find`.

## 1. Result summary

- 227 `*.json` files under `.ufo/waves`. All are regular files; 0 symlinks, 0 hidden, 0 parse errors (jq and Python `json` agree).
- **14** have top-level `"schema": "ufo-swarm-wave-dispatch-v1"` (line 2 of each file). The other 213 files are 23 `ufo-swarm-registry-v1`, 3 `ufo-swarm-wave-v1`, 19 files across 17 other named schemas, and 168 with no top-level `schema` key.
- Members **834**. Trailers parsed **834**, unparsed **0**. Present **767**, empty **0**, missing **67**. Misrooted **0**. Filename flag **0/14**.

## 2. Per-file totals

| # | Dispatch file (lane-relative) | Wave | Members | Trailers parsed / unparsed | Present | Empty | Missing | Misrooted | Filename flag |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | `.ufo/waves/round-12/dispatch.json` | tsukuroi-round12 | 32 | 32 / 0 | 30 | 0 | 2 | 0 | no |
| 2 | `.ufo/waves/round-12/resumed/dispatch.json` | tsukuroi-round12-resumed | 32 | 32 / 0 | 32 | 0 | 0 | 0 | no |
| 3 | `.ufo/waves/round-13/correction/dispatch.json` | tsukuroi-r13-correction | 32 | 32 / 0 | 32 | 0 | 0 | 0 | no |
| 4 | `.ufo/waves/round-14/repair/dispatch.json` | tsukuroi-r14-repair | 32 | 32 / 0 | 32 | 0 | 0 | 0 | no |
| 5 | `.ufo/waves/round-15/build/dispatch.json` | tsukuroi-r15-build | 64 | 64 / 0 | 64 | 0 | 0 | 0 | no |
| 6 | `.ufo/waves/round-16/build/dispatch.json` | tsukuroi-r16-build | 64 | 64 / 0 | 64 | 0 | 0 | 0 | no |
| 7 | `.ufo/waves/round-17/build/dispatch.json` | tsukuroi-r17-build | 72 | 72 / 0 | 72 | 0 | 0 | 0 | no |
| 8 | `.ufo/waves/round-17/falsify/dispatch.json` | tsukuroi-r17-falsify | 81 | 81 / 0 | 37 | 0 | 44 | 0 | no |
| 9 | `.ufo/waves/round-18/build/dispatch.json` | tsukuroi-r18-build | 81 | 81 / 0 | 80 | 0 | 1 | 0 | no |
| 10 | `.ufo/waves/round-18/falsify/dispatch.json` | tsukuroi-r18-falsify | 76 | 76 / 0 | 76 | 0 | 0 | 0 | no |
| 11 | `.ufo/waves/round-19/build/dispatch.json` | tsukuroi-r19-build | 68 | 68 / 0 | 68 | 0 | 0 | 0 | no |
| 12 | `.ufo/waves/round-19/falsify/dispatch.json` | tsukuroi-r19-falsify | 72 | 72 / 0 | 66 | 0 | 6 | 0 | no |
| 13 | `.ufo/waves/round-20/build/dispatch.json` | tsukuroi-r20-build | 64 | 64 / 0 | 50 | 0 | 14 | 0 | no |
| 14 | `.ufo/waves/round-20/falsify/dispatch.json` | tsukuroi-r20-falsify | 64 | 64 / 0 | 64 | 0 | 0 | 0 | no |
| | **Lane total (14 files)** | | **834** | **834 / 0** | **767** | **0** | **67** | **0** | **0 / 14** |

Invariants checked for all 14 files: `taskCall.tasks` length = `registry.members` length = `counts.total` = `counts.spawn`. `counts.resume` = 0 and `resumeSends` is empty. Every member `kind` is `spawn`. Task names equal registry keys as sets, with no duplicate names.

Definitions: **present** = file exists with size > 0. **empty** = exists with size 0. **missing** = no entry at the path. **misrooted** = missing or empty under the lane root, but a file exists at `/home/vgpnk/Projects/shokunin/<same relative path>`.

## 3. Trailer parse

- Rule: a member's trailer is the one line in `taskCall.tasks[i].task` that begins `Report: write your scoped findings to `, followed by one non-space token to end of line. That token is the path, relative to the lane root.
- Result: 834 of 834 tasks have exactly one such line. Zero tasks have zero or multiple trailer lines. The jq-1.8.2 regex matches 834 of 834 tasks (count check). Paths extracted by jq and paths parsed by Python `json` are identical sets for every file.
- All 834 paths are relative (no leading `/`), start with their file's `registry.reportDir`, have basename `<member>.md`, and are unique across all 14 files.
- The context rule at `round-20/build/dispatch.json:421` ("Every Report: trailer path is relative to /home/vgpnk/Projects/shokunin/tsukuroi-shokunin ... NEVER fleet root") is not a member trailer and is not counted.

## 4. Missing reports (67), by name under the lane root

- round-12/dispatch.json (2): `Census.md`, `Matrix.md`
- round-17/falsify/dispatch.json (44): `FxC1Rerun`, `FxEntryLinux`, `FxEntryLinuxlts`, `FxEntrySnapshot2Linux`, `FxEntrySnapshot2Linuxlts`, `FxEntrySnapshot1Linux`, `FxEntryEfifallback`, `FxConsistentPre42`, `FxL0Correction`, `FxRejectedReadings`, `FxAuditLiveAgree`, `FxAuditSelftest`, `FxOwnS051`, `FxOwnS056`, `FxFreshInitV42Sysr`, `FxFreshUpdaSafeV3`, `FxFreshPartUpgrRech`, `FxFreshSnapEaccMech`, `FxFreshDrivFirmPlan`, `FxFreshArchNewsGate`, `FxFreshOverreach`, `FxBindLocaClar`, `FxBindRootDacCorr`, `FxBindSourScopCorr`, `FxBindUpdaRech`, `FxC3Rerun`, `FxSkillContract`, `FxRecheckRerun`, `FxRecheckBlocks`, `FxSeatScopeRerun`, `FxQuality2527`, `FxLessonGate`, `FxW04`, `FxFrozenMarker`, `FxSeparability`, `FxReadmeFrontier`, `FxScorecardRound17`, `FxLogEntry`, `FxRevengerSnapperCopy`, `FxRevengerPlymouth`, `FxRevengerSwitchRoot`, `FxConnSibling`, `FxSimplifyAudit`, `FxConnPlannerGap` (all `.md`)
- round-18/build/dispatch.json (1): `RerunExecLog.md`
- round-19/falsify/dispatch.json (6): `FxCritC1`, `FxCritCensus`, `FxOut003`, `FxInCensusForm`, `FxWriterClasses`, `FxConnSiblingWrites`
- round-20/build/dispatch.json (14): `ExecBinder`, `ExecRegistry`, `ExecAdjacency`, `ExecSystemctl`, `OwnAnchor08`, `OwnAnchor10`, `AdjBoundary02`, `BindTagObject`, `CritAdjacency`, `CritOperability`, `CritCalibration`, `CritNoHarm`, `CritSeparable`, `RevSelectorMechanism`

## 5. Misroot checks

- **Defined test:** 0 of 834 trailer paths exist at `/home/vgpnk/Projects/shokunin/<path>`. `os.path.exists` and `stat` agree. Misrooted is therefore 0 for the 67 missing and for the 767 present.
- **Diagnostic name search** (basenames only; not part of the criterion). I searched the 67 missing basenames across the lane (1,634 files) and the fleet root (about 23.6M files). Both walks pruned `.git`, `.jj`, and `node_modules`. Only 4 of 67 basenames have any hit, and none sits at the same relative path:
  - `CritNoHarm.md` and `CritOperability.md` exist at lane `.ufo/waves/round-18/build/`. Their mtimes are 2026-10-20 16:24 and 16:18. Their content is round-18 (`Baseline 842a531`; "after round-18 judge hardening"). These are name collisions with two round-20 build members, not misroutes.
  - `CritNoHarm.md` also exists at `kagi-shokunin/.ufo/waves/round-23/falsify/` (header "round 23", seat KagiR23.CritNoHarm).
  - `FxCritC1.md` exists at `chousa-shokunin/.ufo/waves/round-25/falsify/` (header "Round 25 — Claim 1 falsification").
  - `Matrix.md` exists at `kake-shokunin/.ufo/waves/round-22/w1/` (name-only hit; not opened).
  - The other 63 missing basenames have no file anywhere in the lane or fleet root outside the pruned `.git`, `.jj`, `node_modules` directories.

## 6. Filename criterion (`preview` | `undispatched` | `validation`)

- 0 of 14 dispatch-v1 filenames match. All 14 are `dispatch.json`, in directories build, falsify, correction, repair, resumed, or the round root.
- Across all 227 wave JSON, three basenames match `validation`: `fleet-r1-interactive/validation.json`, `fleet-r1-interactive/validation-2.json`, and `round-15/build/validation.json`. None has a top-level `schema`. Their top-level keys are `dispatchAllowed, observedAt, reason, runs, taskCalls`; `argv, dispatchAllowed, exitCode, observedAt, reason, registryPersisted`; and `exit, stderr`. They are outside the dispatch-v1 set. [observed]

## 7. Supplementary observations (context for the settlement oracle; not required criteria)

1. **Dispatch snapshot vs live registry.** In all 14 `dispatch.json` files every `registry.members[*].agentId` is `null` (e.g. `round-20/build/dispatch.json:28`). The sibling `swarm-registry.json` in each directory carries non-null agentIds: 834 across the 14 files. In round-17/build, 72 of 74 keyed objects are non-null, and 72 equals the member count. [observed]
2. **Agent-ID namespaces** (text before the first dot). round-12 resumed `TsukuroiR12`; round-13 `TsukuroiR13`; round-14 `TsukuroiR14`; round-15 `TsukuroiR15`; round-16 `TsukuroiR16`; round-17 build and falsify `TsukuroiR17`; round-18 build and falsify `TsukuroiR18-2`; round-19 build `TsukuroiR19`; round-19 falsify, round-20 build, and round-20 falsify `TsukuroiR19Recovery` (e.g. `TsukuroiR19Recovery.ExecBinder-2`). The round-12 root registry uses many non-uniform prefixes, not analysed. [observed]
3. **round-20/build: recorded spawn results conflict with the report files.** [observed]
   - `native-task-result.json` (mtime 05:25:44): its `text` records 64 seat refusals, each "Background job limit reached (100)". `details.results` is null.
   - `native-task-result-retry-2.json` (mtime 06:18:02): `attempt: 2`, `status: "refused-before-spawn"`, `spawned: 0`, `seat_count: 64`.
   - Even so, 50 reports were written between 06:20:36 and 06:39:04. `swarm-registry.json` (mtime 06:23:13) lists 64 `TsukuroiR19Recovery.*` agentIds. Neither native-task-result JSON records a successful spawn.
   - Which mechanism produced the 50 reports is not established by these files. [INFERENCE, unverified; transcripts are out of bounds.] No `.md` in `round-20/build` was written after 06:39:04, so the 14 missing seats look idle. [INFERENCE]
   - The filename criterion says "not flagged", but the recorded spawn evidence conflicts with that. The settlement check should not infer dispatch from filename alone.
4. **round-20/falsify is consistent.** `native-task-result.json` (mtime 06:46:00): `attempt: 1`, `requested: 64`, `spawned: 64`, no error. All 64 reports were written between 06:46:58 and 07:05:22. [observed]
5. **Freshness heuristic.** All 767 present reports have mtime at or after their wave's `dispatch.json` mtime; none are older. This is a heuristic only, since mtime is not provenance. [observed]

## 8. Evidence and reproduction

- Row-level table, 834 rows plus header: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/build/GtLaneTsukuroi/ground-truth-rows.tsv`. Columns: dispatch, wave, member, agent, trailer, report_path, lane_status, fleet_status, misroot, reportdir, name.
- Commands:
  - `find .ufo/waves -name '*.json' | wc -l` gives 227.
  - `jq -r '.schema'` per file gives 14 matches.
  - `/usr/bin/jq -r '[input_filename, .schema, taskCall.tasks length, registry.members length, counts.total, trailer-regex match count] | @tsv'` (filter abbreviated) over the 14 files gives identical counts.
  - A second parse with Python `json` gives the same 14 matches and identical path sets.
  - `stat -c %s` and `os.path.getsize` give 0 disagreements over 834 paths.
- The bare `jq` in the persistent shell is a builtin reporting `jaq 3.1.1`. The authoritative counts above come from `/usr/bin/jq` (jq-1.8.2).

## 9. Caveats

- This is a point-in-time snapshot. The round-20 build and falsify waves were still writing until about 07:05 and may change.
- "Present" means a non-empty file. I did not validate report content, verdicts, or seat identity beyond the path and name match.
- "Missing" is not "never run". See section 7.3.
- Not checked: native-task-result and spawn-result files for rounds 12 to 19 (not opened); those registries were read only for agentId counts and prefixes. Contents of sibling lanes beyond the header reads in section 5 were not read.
