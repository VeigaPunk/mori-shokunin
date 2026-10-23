measured 2026-10-23T07:47:04Z

VERDICT: accounting table complete

No tool installed. Axes: roster identity (spec = dispatch = registry), report presence (path, bytes, first line), commit vs scratch, attempt death lines.

Sources read: `.ufo/waves/round-34/wa-spec.json` (52 items, keys name/role/prompt), `wa-dispatch.json` (52 tasks), `wa/swarm-registry.json`, `wa/*.md`; `wave1-spec.json` (35), `wave1-dispatch.json` (35), `w1/swarm-registry.json`, `w1/*.md`; `c0/*.md`, `contract.md:113-114`, `evidence/c1-controls.txt`; `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log`. Read-only `git -C mori-shokunin`.

Commit boundary (`git rev-parse HEAD` = `5216d78dd1bc4ce57356555b509c9135a9702088`, which has ancestor `fd2521351c6cef47384aef30afbe1e4db7e6912e`). `git ls-tree -r fd252135 -- .ufo/waves/round-34` contains `wa-spec.json` and `wa-dispatch.json` (blob sizes 73787 and 80429, equal to disk) plus `wa-run.json`, the ten `c0/*.md`, contract, counters, and five evidence files. It does not contain `wa/*.md`, `wa/swarm-registry.json`, `wave1-spec.json`, `wave1-dispatch.json`, or `w1/`. `git cat-file -e fd252135:.ufo/waves/round-34/wa/ExecRerunLane.md` exits 128 ("exists on disk, but not in"). Same for `wave1-spec.json` and `w1/swarm-registry.json`, and the same wa path at HEAD. `git diff --name-status fd252135 -- .ufo/waves/round-34` is only the three `wb-*` files added after that commit (HEAD subject: wave B spec/dispatch). `git log` of `wave1-spec.json`, `w1`, and `wa` is empty. So wave-A and wave-1 seat reports below are on-disk scratch, not lane commits. C0 report bytes match the `fd252135` blobs (`git cat-file -s` vs `stat`; no mismatch).

## Attempt deaths

`watchdog.log:847` (attempt 1): `2026-10-23T02:26:43-03:00 lane-dead-no-report mori round=34; retry same round (hyaku-inline attempt=1: L1 died with the orchestrator process exit at 05:25:25Z (attempt 1; landed commits kept, uncommitted files untrusted))`

`watchdog.log:867` (attempt 2): `2026-10-23T03:40:32-03:00 lane-dead-no-report mori round=34; retry same round (hyaku-inline attempt=2: L1 died with the orchestrator process (omp SIGSEGV) at 06:19:06Z (attempt 2; landed commits kept, uncommitted files untrusted))`

No later `mori round=34` line through `watchdog.log:880` (file ends there). Attempt 3 is launched at `watchdog.log:868` and has no death line in this log. Launch lines contain process-group ids and are not copied.

## Wave A — attempt 2, 52 seats

`wa-spec.json` order equals `wa-dispatch.json` task order; each `tasks[].agent` equals the spec `role` (0 mismatches). `wa/swarm-registry.json`: schema `ufo-swarm-registry-v1`, wave `mori-r34-wa`, `createdAt`=`updatedAt`=`2026-10-23T05:37:34.977Z`, 52 members, every `kind=spawn`, every `agentId` null, roles match the spec (0 mismatches). `wa-run.json` (in `fd252135`): `counts` spawn 52, resume 0, total 52; embedded registry also 52 members and 0 agentIds. On-disk `wa/*.md`: 51 files, no extra names. Every present report's first line is exactly `measured` plus the timestamp below. Bytes are `stat` size.

| # | seat | role | bytes | first line |
|---|---|---|---|---|
| 00 | ExecRerunLane | executor | 11504 | measured 2026-10-23T05:43:10Z |
| 01 | ExecRerunClone | executor | 12045 | measured 2026-10-23T05:50:19Z |
| 02 | ExecCliEdges | executor | 26326 | measured 2026-10-23T06:04:40Z |
| 03 | ExecReadOnlyTrace | executor | 11841 | measured 2026-10-23T05:53:40Z |
| 04 | ExecLatencyBudget | executor | 12605 | measured 2026-10-23T06:05:56Z |
| 05 | ExecHandOracle | executor | 15326 | measured 2026-10-23T05:54:03Z |
| 06 | MutPrecedence | mutation-tester | 9929 | measured 2026-10-23T05:43:28Z |
| 07 | MutClassOrder | mutation-tester | 9079 | measured 2026-10-23T05:43:06Z |
| 08 | MutParse | mutation-tester | 10966 | measured 2026-10-23T05:48:33Z |
| 09 | MutRateHost | mutation-tester | 12430 | measured 2026-10-23T05:43:19Z |
| 10 | MutLiveArm | mutation-tester | 10676 | measured 2026-10-23T05:44:18Z |
| 11 | LabLoadRate | executor | 9547 | measured 2026-10-23T06:08:01Z |
| 12 | LabStackedHost | executor | 10155 | measured 2026-10-23T05:47:33Z |
| 13 | LabIntervalError | executor | 10745 | measured 2026-10-23T06:07:12Z |
| 14 | LabFixtureLayouts | executor | 8654 | measured 2026-10-23T05:47:22Z |
| 15 | LabFixturePartStacked | executor | 8240 | measured 2026-10-23T05:46:29Z |
| 16 | LabFixtureVirtualUnknown | executor | 8900 | measured 2026-10-23T06:12:08Z |
| 17 | LabScaleHost | executor | — | NO REPORT |
| 18 | CritResidualA | critic | 11784 | measured 2026-10-23T06:05:31Z |
| 19 | CritPostDataShortcut | critic | 9568 | measured 2026-10-23T05:47:46Z |
| 20 | CritGeneratorCoverage | critic | 14549 | measured 2026-10-23T06:13:18Z |
| 21 | RevToolCode | reviewer | 7264 | measured 2026-10-23T05:40:48Z |
| 22 | RevToolDocstring | reviewer | 6543 | measured 2026-10-23T05:39:36Z |
| 23 | ScoutEntryVsTool | scout | 8927 | measured 2026-10-23T05:41:38Z |
| 24 | ReopenS191 | reviewer | 4869 | measured 2026-10-23T05:41:24Z |
| 25 | ReopenS192 | reviewer | 4221 | measured 2026-10-23T05:39:05Z |
| 26 | ReopenS193 | reviewer | 5245 | measured 2026-10-23T05:39:44Z |
| 27 | ReopenS194 | reviewer | 3205 | measured 2026-10-23T05:38:55Z |
| 28 | ReopenS195 | reviewer | 2557 | measured 2026-10-23T05:38:49Z |
| 29 | ReopenS196 | reviewer | 5388 | measured 2026-10-23T05:40:20Z |
| 30 | ReopenS197 | reviewer | 5201 | measured 2026-10-23T05:39:38Z |
| 31 | ReopenS198 | reviewer | 6167 | measured 2026-10-23T05:38:48Z |
| 32 | ReopenS182Anchor | reviewer | 3301 | measured 2026-10-23T05:38:58Z |
| 33 | JudgeRow3r | reviewer | 4425 | measured 2026-10-23T05:38:55Z |
| 34 | JudgeRow6r | reviewer | 5940 | measured 2026-10-23T05:39:11Z |
| 35 | JudgeRow7r | reviewer | 4836 | measured 2026-10-23T05:39:05Z |
| 36 | JudgeRow13r | reviewer | 6175 | measured 2026-10-23T05:39:13Z |
| 37 | JudgeRow8Correction | reviewer | 4767 | measured 2026-10-23T05:39:44Z |
| 38 | JudgeSkillCorrection | reviewer | 6330 | measured 2026-10-23T05:39:45Z |
| 39 | JudgeSkillRound34 | reviewer | 7696 | measured 2026-10-23T05:39:35Z |
| 40 | JudgeLessonItem5 | reviewer | 7274 | measured 2026-10-23T05:39:47Z |
| 41 | JudgeLessonItem6 | reviewer | 5828 | measured 2026-10-23T05:39:33Z |
| 42 | JudgeLessonItem7 | reviewer | 5261 | measured 2026-10-23T05:39:35Z |
| 43 | JudgeLessonItem8 | reviewer | 6411 | measured 2026-10-23T05:39:32Z |
| 44 | RevAppendOnly | reviewer | 4146 | measured 2026-10-23T05:38:57Z |
| 45 | RevPreDataReceipts | reviewer | 5733 | measured 2026-10-23T05:41:52Z |
| 46 | ReviewC2Judge | reviewer | 6748 | measured 2026-10-23T05:40:31Z |
| 47 | MutQ98 | mutation-tester | 9971 | measured 2026-10-23T05:44:10Z |
| 48 | ConnectorShapes | connector | 2838 | measured 2026-10-23T06:08:43Z |
| 49 | ScribeMistakeM1 | scribe | 1840 | measured 2026-10-23T05:38:05Z |
| 50 | ScribeScorecardLog | scribe | 7858 | measured 2026-10-23T05:38:13Z |
| 51 | SentinelPrivacy | sentinel | 1606 | measured 2026-10-23T05:41:20Z |

Role totals: executor 13, mutation-tester 6, critic 3, reviewer 25, scout 1, connector 1, scribe 2, sentinel 1.

Seat with no report: **LabScaleHost** (executor, spec index 17). It is in the spec, the dispatch, and the registry. There is no `wa/LabScaleHost.md`.

## Wave 1 — attempt 1, 35 seats

`wave1-spec.json` order equals `wave1-dispatch.json`; `tasks[].agent` equals spec `role` (0 mismatches). Both files are on disk and absent from `fd252135` and HEAD. `w1/swarm-registry.json`: wave `mori-r34-w1`, `createdAt` `2026-10-23T05:13:48.713Z`, `updatedAt` `2026-10-23T05:15:27.916Z`, 35 members, roles match, every `agentId` is `MoriR34.` plus the seat name. `wave1-run.json` (also not in the tip tree) counts spawn 35, resume 0, total 35, but its embedded registry still has 0 agentIds — dispatch snapshot, not the updated registry file. On-disk `w1/*.md`: 30 files, no extra names. Present first lines are exactly `measured` plus the timestamp.

| # | seat | role | bytes | first line |
|---|---|---|---|---|
| 00 | ExecDiskRateTool | executor | — | NO REPORT |
| 01 | ExecHostEvidence | executor | 11568 | measured 2026-10-23T05:18:36Z |
| 02 | SrcPartitionsCore | scribe | 5451 | measured 2026-10-23T05:16:21Z |
| 03 | SrcHolder | scribe | 4383 | measured 2026-10-23T05:15:04Z |
| 04 | SrcDriverCoreDevice | scribe | 3819 | measured 2026-10-23T05:15:31Z |
| 05 | SrcGenhdSlaves | scribe | 3901 | measured 2026-10-23T05:14:24Z |
| 06 | SrcSysfsBlockAbi | scribe | 8531 | measured 2026-10-23T05:19:20Z |
| 07 | SrcLoopParent | scribe | 5771 | measured 2026-10-23T05:15:25Z |
| 08 | SrcSysstatClass | scribe | 3746 | measured 2026-10-23T05:15:41Z |
| 09 | SrcUtilLinuxSysfs | scribe | 5289 | measured 2026-10-23T05:15:47Z |
| 10 | DraftEntryTool | scribe | 9182 | measured 2026-10-23T05:14:39Z |
| 11 | DraftFrontierProvince | scribe | 5524 | measured 2026-10-23T05:14:22Z |
| 12 | DraftSkillRound34 | scribe | 4155 | measured 2026-10-23T05:14:25Z |
| 13 | DraftQuality98 | scribe | 9760 | measured 2026-10-23T05:18:40Z |
| 14 | DraftMistakes | scribe | 6219 | measured 2026-10-23T05:18:37Z |
| 15 | RepairRow03 | scribe | 5510 | measured 2026-10-23T05:14:20Z |
| 16 | RepairRow06 | scribe | 5062 | measured 2026-10-23T05:15:00Z |
| 17 | RepairRow07 | scribe | 4061 | measured 2026-10-23T05:15:46Z |
| 18 | RepairRow13 | scribe | 5123 | measured 2026-10-23T05:14:29Z |
| 19 | RepairRow08Boundary | scribe | 8056 | measured 2026-10-23T05:16:36Z |
| 20 | RepairLessonSec1 | scribe | 6085 | measured 2026-10-23T05:14:37Z |
| 21 | RepairWordEdits | scribe | 3546 | measured 2026-10-23T05:14:21Z |
| 22 | RepairTimeLabels | scribe | 4890 | measured 2026-10-23T05:14:33Z |
| 23 | RepairLocatorS117 | scribe | 4961 | measured 2026-10-23T05:14:48Z |
| 24 | ReviewRulesR1R2R6 | reviewer | 10030 | measured 2026-10-23T05:22:50Z |
| 25 | ReviewRuleR3 | reviewer | — | NO REPORT |
| 26 | ReviewRuleR5 | reviewer | — | NO REPORT |
| 27 | ReviewRuleR7 | reviewer | — | NO REPORT |
| 28 | ReviewPredicateParity | reviewer | 11184 | measured 2026-10-23T05:23:15Z |
| 29 | CriticC1AxisFit | critic | — | NO REPORT |
| 30 | CriticC2Exploratory | critic | 15617 | measured 2026-10-23T05:17:32Z |
| 31 | MutOracleR2R5 | mutation-tester | 10578 | measured 2026-10-23T05:19:00Z |
| 32 | MutOracleR3R6R7 | mutation-tester | 9386 | measured 2026-10-23T05:21:10Z |
| 33 | ConnectorSiblings | connector | 5545 | measured 2026-10-23T05:40:00Z |
| 34 | ScoutCensusDisk | scout | 11660 | measured 2026-10-23T05:20:17Z |

Role totals: executor 2, scribe 22, reviewer 5, critic 2, mutation-tester 2, connector 1, scout 1.

Seats with no report (5), all present in spec, dispatch, and registry: **ExecDiskRateTool** (executor), **ReviewRuleR3** (reviewer), **ReviewRuleR5** (reviewer), **ReviewRuleR7** (reviewer), **CriticC1AxisFit** (critic). No matching `w1/*.md` for any of them.

## C0 — 10 seats, all reported

No `c0-spec.json`, `c0-dispatch.json`, or `c0/swarm-registry.json` in `.ufo/waves/round-34/` (directory listing). Roles are the sentence at `contract.md:113-114`: CtlJunk, CtlAllNull, CtlNaive, CtlSinceBoot, CtlEcho, CtlCheapest as critic; CtlAllDisk, CtlNoReset, CtlLabelKey, CtlSysBlock as mutation-tester. All ten `c0/*.md` are in `fd252135`, bytes match the blobs, first line is exactly `measured` plus the timestamp. No seat lacks a report.

| seat | role | bytes | first line | c1-controls.txt rows |
|---|---|---|---|---|
| CtlJunk | critic | 3827 | measured 2026-10-23T04:56:38Z | 02 C-junk |
| CtlAllNull | critic | 5264 | measured 2026-10-23T04:56:50Z | 03 C-allnull |
| CtlNaive | critic | 6153 | measured 2026-10-23T04:57:38Z | 04 C-naive |
| CtlSinceBoot | critic | 13380 | measured 2026-10-23T05:02:18Z | 07 C-sinceboot |
| CtlEcho | critic | 19523 | measured 2026-10-23T05:06:01Z | 09 C-echo-v1, 10 v2, 11 v3 |
| CtlCheapest | critic | 14984 | measured 2026-10-23T04:58:52Z | 13 C-emptylive, 14 C-zero-singleread, 15 C-echo-ppid, 16 C-echo-literal2 |
| CtlAllDisk | mutation-tester | 9809 | measured 2026-10-23T04:57:09Z | 05 C-alldisk |
| CtlNoReset | mutation-tester | 8215 | measured 2026-10-23T04:56:07Z | 06 C-noreset |
| CtlLabelKey | mutation-tester | 14142 | measured 2026-10-23T04:57:07Z | 08 C-labelkey |
| CtlSysBlock | mutation-tester | 8712 | measured 2026-10-23T04:57:34Z | 12 C-sysblock, 18 POS-sysblock-seat-baseline |

`c1-controls.txt:1` says the file was measured `2026-10-23T05:13:09Z` by L1 after all ten C0 seats returned. Rows 01 C-absent (`c1-controls.txt:2`) and 17 POS-l1-oracle-copy (`c1-controls.txt:50`) name no `c0/*.md` seat. [INFERENCE] those two rows are L1 receipts, not missing C0 seats: the contract names exactly these ten, and `c0/` has exactly these ten reports.

## Gaps left inside an otherwise closed table

Report bodies were not scored. Scratch dirs outside `wa/`, `w1/`, and `c0/` were not searched, so a missing markdown file is absence at the report path, not proof the seat wrote nothing elsewhere.
