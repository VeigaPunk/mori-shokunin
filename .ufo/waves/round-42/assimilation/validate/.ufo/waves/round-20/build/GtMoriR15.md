# GtMoriR15: C2 independent ground truth, round-15 dispatch (`mori-r15-positive`)

Status: complete. Ground truth recorded. No discrepancy between the ground truth and any recorded count. Round 15 has no machine settlement artifact to compare against.

## Scope and method
- Dispatch: `.ufo/waves/round-15/dispatch.json` (schema `ufo-swarm-wave-dispatch-v1`; `counts` spawn 64 / resume 0 / total 64).
- Members: `jq -r '.taskCall.tasks[] | .name'`, 64 names, 64 unique.
- Report path: the last task line starting with `Report: write your scoped findings to `, resolved under `/home/vgpnk/Projects/shokunin/mori-shokunin/`.
- Presence: `-L` / `-e` tests, then `stat -c '%F|%s|%y'` on the mori-root path (`regular file`, size > 0 = present). Fleet check: the same relative path tested under `/home/vgpnk/Projects/shokunin` with `-L` / `-f` / `-e`.
- Read-only comparison sources: `build/swarm-registry.json`, `task-response.json`, `LOG.md` and `SCORECARD.md` in both roots, `MANIFEST.json`, and the C2 rules in `round-20/contract.md:68-81`.
- Not opened: `frozen/c2-expected.json`, `tools/mori-wave-settlement.py`, transcripts, `~/.omp` logs.
- Installs or updates: none. `jq`, `stat` and `ls` were already present.

## Totals
| metric | result |
|---|---|
| members (`taskCall.tasks`) | 64 (64 unique names) |
| trailer lines matching `^Report: write your scoped findings to \S+$` | 64 of 64, one per task, each the last line of its task |
| trailer path equals `.ufo/waves/round-15/build/<name>.md` | 64 of 64 |
| **present** (regular non-symlink, size > 0) | **64** |
| empty | 0 |
| **missing** | **0** |
| symlink / unsafe / unparsed | 0 / 0 / 0 |
| **misrooted** (missing under mori, regular file under fleet) | **0** |
| same relative path under fleet root | absent 64 of 64 |
| wave state (contract rule: every member present) | **settled, 64/64** |
| bytes (`stat %s`) | total 772,239; min 3,356 (ScribeSourceCensus); max 28,119 (ReconProtectedTeaching) |
| mtime (-0300) | 04:30:01 to 05:18:58; after dispatch.json birth 04:28:52, before closure stamp 05:35:38 |
| content | no `STATUS:` line in any file; 64 distinct first headings; no stub files |

## Per-member table
Status is `present` for every member. Bytes and mtime come from `stat`. Fleet column = same relative path under `/home/vgpnk/Projects/shokunin`.

| name | status | bytes | mtime | fleet same path |
|---|---|---|---|---|
| CensusPositive | present | 9642 | 04:56:27 | absent |
| HarnessBuild | present | 18483 | 05:18:58 | absent |
| ProvenanceCapture | present | 7783 | 04:41:49 | absent |
| SkillInterface | present | 15209 | 04:52:45 | absent |
| KnowledgePositive | present | 11540 | 04:40:13 | absent |
| IndexPositive | present | 4361 | 04:36:45 | absent |
| QualityDebt | present | 8735 | 04:38:44 | absent |
| RegistryFrontier | present | 9973 | 04:33:24 | absent |
| PackKernelUser | present | 6551 | 04:32:14 | absent |
| PackKernelSystem | present | 8624 | 04:36:03 | absent |
| PackUnitUser | present | 8192 | 04:33:53 | absent |
| PackUnitSystem | present | 6710 | 04:35:24 | absent |
| PackSignalUser | present | 7585 | 04:32:34 | absent |
| PackProcessUser | present | 5690 | 04:35:57 | absent |
| PackForeignBoot | present | 8412 | 04:33:51 | absent |
| PackBootArray | present | 8380 | 04:32:07 | absent |
| PackNegativeInvalid | present | 8636 | 04:35:33 | absent |
| PackNegativeResults | present | 8331 | 04:36:59 | absent |
| PackNegativeStatus | present | 7802 | 04:33:22 | absent |
| PackCrossScope | present | 11886 | 04:37:31 | absent |
| PackSubjectUnknown | present | 14769 | 04:48:08 | absent |
| PackFanoutPositive | present | 10517 | 04:37:18 | absent |
| PackOrderMixed | present | 19016 | 04:43:23 | absent |
| PackCleanControls | present | 6068 | 04:32:17 | absent |
| ReconFieldTypes | present | 17088 | 04:33:06 | absent |
| ReconBootScope | present | 11069 | 04:32:18 | absent |
| ReconResultEmitter | present | 18055 | 04:32:47 | absent |
| ReconParserContracts | present | 11647 | 04:32:44 | absent |
| ReconQueryBounds | present | 12318 | 04:32:15 | absent |
| ReconLegacySignal | present | 15868 | 04:32:13 | absent |
| ReconDirtyRevision | present | 17708 | 04:36:48 | absent |
| ReconProtectedTeaching | present | 28119 | 04:33:19 | absent |
| ConnectPlannerWalk | present | 26961 | 04:33:50 | absent |
| ConnectSiblingOverlap | present | 21421 | 04:33:59 | absent |
| ConnectFrontier | present | 18466 | 04:32:45 | absent |
| ConnectNoHarmAxes | present | 15192 | 04:33:39 | absent |
| ConnectSourceChain | present | 18327 | 04:32:50 | absent |
| ConnectReceipts | present | 23467 | 04:38:38 | absent |
| ReviewKernelPredicate | present | 9670 | 04:30:58 | absent |
| ReviewUnitPredicate | present | 7934 | 04:30:20 | absent |
| ReviewProcessPredicate | present | 7252 | 04:30:25 | absent |
| ReviewRawTotals | present | 8475 | 04:31:02 | absent |
| ReviewRouting | present | 8758 | 04:30:36 | absent |
| ReviewHarnessPacks | present | 10027 | 04:30:51 | absent |
| ReviewHarnessGate | present | 20161 | 04:56:35 | absent |
| ReviewDocumentation | present | 6654 | 04:30:44 | absent |
| ScribeSourceCensus | present | 3356 | 04:30:01 | absent |
| ScribeRoutedDebt | present | 9591 | 04:31:01 | absent |
| ScribeNoHarmLedger | present | 7979 | 04:30:05 | absent |
| ScribeGateDecisions | present | 7999 | 04:30:12 | absent |
| ScribeReportContract | present | 10729 | 04:35:28 | absent |
| ScribeFixtureInventory | present | 7839 | 04:35:59 | absent |
| AttackFalsePositive | present | 12633 | 04:32:32 | absent |
| AttackSuppression | present | 11756 | 04:36:30 | absent |
| AttackSignalConfusion | present | 17573 | 04:44:51 | absent |
| AttackCountVacuity | present | 20815 | 04:35:44 | absent |
| AttackFixtureOracle | present | 9913 | 04:32:26 | absent |
| AttackNoHarm | present | 18135 | 04:32:51 | absent |
| AttackProvenance | present | 12293 | 04:41:46 | absent |
| AttackSourceOverreach | present | 12347 | 04:37:09 | absent |
| SecurityPrivacy | present | 12346 | 04:44:36 | absent |
| SecurityTrust | present | 13100 | 04:33:27 | absent |
| HistoryOriginalIntent | present | 8354 | 04:31:30 | absent |
| HistoryDirtyHistory | present | 7949 | 04:31:29 | absent |

## Comparison with recorded counts
| source | recorded | versus ground truth |
|---|---|---|
| `dispatch.json` `counts` | spawn 64, resume 0, total 64 | match |
| `.ufo/waves/round-15/build/swarm-registry.json` | 64 members, all `kind: spawn`, all `agentId` bound, `createdAt` 07:28:52Z | match. Name set equals dispatch and `assignments.json` (64/64). Role equals task `agent` for 64/64 names |
| `task-response.json` text | "Spawned 64 background agents" | match |
| `LOG.md:883-885` | one validated 64-seat build wave: executor 24, scout 8, connector 6, reviewer 8, critic 8, scribe 6, sentinel 2, revenger 2 | match. jq role counts are identical |
| `LOG.md:891-892` | host-safety amendment sent to all 64 exact seat ids | match |
| `LOG.md:983-985` | all 64 original seat reports exist; outside closure still required (written at the final L1 measurement) | match (64 present). This is the only recorded report-presence count for round 15, and it is narrative, not a settlement file |
| `SCORECARD.md:815-897` (Round 15) | no settlement, report-presence or misroot count | nothing to compare |
| `MANIFEST.json` `rounds[345]` (only mori lane_round-15 entry: `lane` mori, `lane_round` 15; `closed_at` 2026-10-20T08:42:50Z) | launch 04:25:40 -03:00, complete 05:35:38 -03:00, `lanes` `{"mori":"ok"}`; notes say one validated 64-seat wave conforms | consistent (64 seats). No per-seat report count recorded |
| `wave*-settlement.json` | none in round-15, mori or fleet, including `evidence/`, `build/`, `frozen/`, `fixtures/`, `boundary-fixtures/` | no machine settlement record exists for this wave |
| fleet `LOG.md`, `SCORECARD.md`, fleet `.ufo/waves/round-15/*` (`round15-*.json`, `*.md`) | no mori round-15 settlement, report or misroot record | nothing to compare |

## Notes
1. **No machine settlement record for round 15.** Other rounds have one: round 17 `wave-settlement.json`, round 19 `wave1-settlement.json` and `wave2-settlement.json`. Those belong to other waves and were not compared. The C2 tool's output for this wave would be its first machine record.
2. **The misroot records are Round 16, not Round 15.** `SCORECARD.md:997-999` (2 misrooted reports relocated byte-exact) sits inside the Round 16 section (`SCORECARD.md:898-1001`). `LOG.md:1105-1109` (fleet `round-16/build` sweep, 2 own reports) sits inside the Round 16 section (`LOG.md:991-1117`). Round 15 has no misroot record, and none is present now.
3. `build/` holds 65 regular files: the 64 expected reports plus `swarm-registry.json`. The registry is not a report and is not a member.
4. **Timeline (observed).** The MANIFEST launch stamp 04:25:40 -03:00 precedes `dispatch.json` birth and registry `createdAt` (04:28:52 -03:00) by about 3 minutes. [INFERENCE: the launch was logged before the dispatch artifact was written.]
5. **Units.** An early jq pass reported bytes with jq `length`, which counts characters (total 768,748). Byte totals in this report come from `stat %s` (772,239) and supersede that figure.
6. **Procedure disclosure.** The first distribution check used awk, cut, sort, uniq and wc before I redid it with jq. The mtime column was trimmed with `cut -c1-19`. Member statuses and totals come from `stat` and jq. A wide glob search timed out and proves nothing, so the absence claims rest on `ls` listings of the round-15 directories and root.
7. **Scratch evidence (seat-owned)** under `.ufo/waves/round-20/build/GtMoriR15/`: `tasks.tsv` (name, trailer count, relative path); `final.tsv` (authoritative per-member record); `content.ndjson` (content checks; its `bytes` field is superseded by `final.tsv`); `members.tsv` and `report-lines.tsv` (earlier passes with the same statuses as `final.tsv`); `build-listing.{txt,json}`; `mtimes.tsv`.

## Target for L1 comparison
The round-15 entry of the C2 tool should read: state `settled`, 64 members, 64 present, 0 empty, 0 missing, 0 misrooted, 0 unsafe, 0 unparsed. Any other result for this entry is a tool defect to investigate. No check was run on the tool itself by this seat.
