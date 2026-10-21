# GtLaneKama: C2 independent fleet ground truth, kama-shokunin dispatch files

Seat: MoriR20.GtLaneKama (leaf scout; read-only; no subagents, no swarms).
Lane root: `/home/vgpnk/Projects/shokunin/kama-shokunin`. Fleet root (misroot check): `/home/vgpnk/Projects/shokunin`.
Scan (UTC): 2026-10-21T10:34:51Z. The lane is live. The first `find` counted 293 JSON files and this scan counted 296. The three extra are round-21/build `spec.json`, `dispatch.json` and `advice/swarm-registry.json` (mtimes 10:28:34Z to 10:28:38Z).

## Method
- Discovery: every regular `*.json` under `.ufo/waves` (296; symlinks 0). Top-level `.schema == "ufo-swarm-wave-dispatch-v1"` tested with `/usr/bin/jq` 1.8.2-1. Python `json` agrees (19 = 19, identical set).
- Members: `taskCall.tasks[*]`. Report path = last line of each task matching `^Report: write your scoped findings to (\S+)$`. A jq re-extraction of every trailer and member count agrees with Python (0 mismatches).
- Status: `present` (regular, non-symlink, size > 0), `empty` (size 0), `missing`, `misrooted` (missing under the lane root but a regular non-symlink file at the same relative path under the fleet root), `unsafe` (absolute, contains `..`, or resolves outside the lane root), `unparsed`.
- Wave state (contract rules): `no-spawn` (taskCall null), `unavailable` (no safe parsed path), `settled` (all present), `partial` (at least one present and one not), `unsettled` (none present).
- Not run: `tools/mori-wave-settlement.py`, `tools/mori-census.sh`. Not opened: `frozen/c2-expected.json` (kept independent). Nothing was written except this report.

## Summary
- 19 top-level dispatch files; 1198 member entries; 1123 unique report paths. 75 round-18 paths are shared by `build/dispatch.json` and `build/dispatch-95.json` with identical status.
- Trailers: 1198/1198 parsed; 0 unparsed; 0 unsafe; 0 symlink; 0 empty; 0 misrooted.
- Status, member basis: 989 present, 209 missing. Unique-path basis: 914 present, 209 missing.
- Mechanical wave states: 10 settled, 7 partial, 2 unsettled, 0 no-spawn, 0 unavailable.
- Filename rule: 0 of 19 names contain `preview`, `undispatched` or `validation`.
- The mechanical rule over-reports missing reports. Of the 209 missing, 86 are seats whose lane records show they were never spawned (round-18/build/dispatch-95.json 20; round-19/falsify 66). Another 86 are round-21/build seats refused on attempt 1 with no successful spawn recorded as of scan. Only 37 are seats that were spawned and left no report (section 3).

## 1. Per-file totals

| # | File (under .ufo/waves/) | Wave | Members | Parsed | Unparsed | Unsafe | Present | Empty | Missing | Misrooted | State | Filename hint |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 1 | round-11/dispatch.json | kama-round-11 | 32 | 32 | 0 | 0 | 30 | 0 | 2 | 0 | partial | none |
| 2 | round-11/verification-dispatch.json | kama-round-11-verification | 32 | 32 | 0 | 0 | 32 | 0 | 0 | 0 | settled | none |
| 3 | round-12/dispatch.json | (null) | 32 | 32 | 0 | 0 | 32 | 0 | 0 | 0 | settled | none |
| 4 | round-13/dispatch.json | (null) | 32 | 32 | 0 | 0 | 32 | 0 | 0 | 0 | settled | none |
| 5 | round-14/dispatch.json | (null) | 32 | 32 | 0 | 0 | 32 | 0 | 0 | 0 | settled | none |
| 6 | round-15/build/dispatch.json | (null) | 64 | 64 | 0 | 0 | 60 | 0 | 4 | 0 | partial | none |
| 7 | round-15/falsify/dispatch.json | (null) | 32 | 32 | 0 | 0 | 32 | 0 | 0 | 0 | settled | none |
| 8 | round-16/build/dispatch.json | (null) | 81 | 81 | 0 | 0 | 81 | 0 | 0 | 0 | settled | none |
| 9 | round-16/falsify/dispatch.json | (null) | 79 | 79 | 0 | 0 | 79 | 0 | 0 | 0 | settled | none |
| 10 | round-17/build/dispatch.json | (null) | 82 | 82 | 0 | 0 | 82 | 0 | 0 | 0 | settled | none |
| 11 | round-17/falsify/dispatch.json | (null) | 80 | 80 | 0 | 0 | 73 | 0 | 7 | 0 | partial | none |
| 12 | round-18/build/dispatch-95.json | (null) | 95 | 95 | 0 | 0 | 75 | 0 | 20 | 0 | partial | none |
| 13 | round-18/build/dispatch.json | (null) | 75 | 75 | 0 | 0 | 75 | 0 | 0 | 0 | settled | none |
| 14 | round-18/falsify/dispatch.json | (null) | 76 | 76 | 0 | 0 | 66 | 0 | 10 | 0 | partial | none |
| 15 | round-19/build/dispatch.json | (null) | 64 | 64 | 0 | 0 | 64 | 0 | 0 | 0 | settled | none |
| 16 | round-19/falsify/dispatch.json | (null) | 66 | 66 | 0 | 0 | 0 | 0 | 66 | 0 | unsettled | none |
| 17 | round-20/build/dispatch.json | (null) | 72 | 72 | 0 | 0 | 71 | 0 | 1 | 0 | partial | none |
| 18 | round-20/falsify/dispatch.json | falsify | 86 | 86 | 0 | 0 | 73 | 0 | 13 | 0 | partial | none |
| 19 | round-21/build/dispatch.json | (null) | 86 | 86 | 0 | 0 | 0 | 0 | 86 | 0 | unsettled | none |

## 2. Lane totals

- Member basis: members 1198; parsed 1198; unparsed 0; unsafe 0; symlink 0; present 989; empty 0; missing 209; misrooted 0.
- Unique-path basis: 1123 paths; present 914; missing 209.
- Wave states: settled 10; partial 7; unsettled 2; no-spawn 0; unavailable 0.
- Filename hints: 0 of 19. Nearest name is `round-11/verification-dispatch.json` ("verification", not "validation"): spawned 32, 32/32 present, so it was dispatched.

## 3. Dispatch evidence per file (sibling records; beyond the filename rule)

| File (under .ufo/waves/) | State | Evidence (observed unless marked) |
|---|---|---|
| round-11/dispatch.json | partial | Spawned 32 (spawn-result.json spawn_count 32). 2 missing: Measure, Safety. No completion or failure summary in dir. |
| round-11/verification-dispatch.json | settled | Spawned 32 (verification-spawn.json). 32/32 present. Wave kama-round-11-verification. |
| round-12/dispatch.json | settled | Spawned 32 (spawn-result.json). 32/32 present. |
| round-13/dispatch.json | settled | Spawned 32 (spawn-result.json). 32/32 present. |
| round-14/dispatch.json | settled | Spawned 32 (spawn-result.json). 32/32 present. |
| round-15/build/dispatch.json | partial | Spawned 64 via direct-spawn-result.json after two refused eval attempts. 4 missing = completion-summary failed_ids CaseAudit00, CaseAudit04, CaseAudit14, CaseAudit19: spawned, then failed. |
| round-15/falsify/dispatch.json | settled | completion-summary: spawns 32, completed 32, failed 0. 32/32 present. |
| round-16/build/dispatch.json | settled | completion-summary: dispatched 81, advice_reports 81. 81/81 present. |
| round-16/falsify/dispatch.json | settled | completion-summary: dispatched 79, advice_reports 79. 79/79 present. Lane misroots note: RevengerRunReceipts.md moved by L1; fleet copy absent now. |
| round-17/build/dispatch.json | settled | First attempt refused (refused-result-1.json, 2026-10-20T15:03:50Z). Retry spawn-result.json 'Spawned 82' (15:15:50Z). 82/82 present. |
| round-17/falsify/dispatch.json | partial | spawn-result.json 'Spawned 80'. completion-summary: terminal completed 71, failed 9, advice_reports 73; 7 missing reports listed by name. |
| round-18/build/dispatch-95.json | partial | NEVER SPAWNED (20 members). completion-summary refused_attempts: members 95, spawned 0 (refused-result-1.json). The 20 names (ConnectMori ... SimplifyC1Plan) appear in refused-result-1.json and not in spawn-result.json, which spawned only the 75 members of dispatch.json. |
| round-18/build/dispatch.json | settled | completion-summary: spawned 75, completed 75, dead []. 75/75 present. |
| round-18/falsify/dispatch.json | partial | spawn-result.json 'Spawned 76' (2026-10-20T23:15:12Z). 10 missing. No completion note in dir. |
| round-19/build/dispatch.json | settled | 64/64 present. No spawn-result file in dir. |
| round-19/falsify/dispatch.json | unsettled | NEVER SPAWNED. refused-attempt-1.json (2026-10-21T06:39:21Z): seats 66, refused 66, spawned 0, 'Background job limit reached (100)'. No retry record in dir. |
| round-20/build/dispatch.json | partial | Attempt 1 refused all 72 (spawned 0); attempt 2 spawned 72 (dispatch-attempts.txt). completion-summary dead_original_seats CellDesign and SrcGateStandard: CellDesign missing; SrcGateStandard report present (6468 B). |
| round-20/falsify/dispatch.json | partial | Attempt 1 refused all 86 (spawned 0; refused-attempt-1.json); completion-summary spawned 86. 13 missing = lane dead seats after retries (seat-failures.json: new_replacement_seats_spawned 0). |
| round-21/build/dispatch.json | unsettled | LIVE at scan. dispatch-attempts.txt: attempt1 2026-10-21T07:29:16Z refused all 86. spawn-result.txt (mtime 10:29:13Z) holds a refusal naming 86 seats, with no 'Spawned' text. dispatch.json written 10:28:38Z (registry createdAt 10:28:38.215Z). [INFERENCE] a second attempt was refused; no successful spawn recorded. |

Reconciliation of the 209 missing members:
- Never spawned, confirmed by lane records: 86 (round-18/build/dispatch-95.json 20; round-19/falsify/dispatch.json 66).
- Not spawned as of scan, wave live: 86 (round-21/build/dispatch.json).
- Spawned, no report: 37 (round-11/dispatch 2; round-15/build 4; round-17/falsify 7; round-18/falsify 10; round-20/build 1; round-20/falsify 13).

## 4. Discrepancies and cautions for L1
1. `counts.spawn` equals the member count in all 19 files. It records the plan, not an observed spawn. Example: round-19/falsify says spawn 66 while refused-attempt-1.json says spawned 0.
2. The mechanical rule cannot separate refused-never-spawned seats from spawned-no-report seats. It reads only dispatch and report files. Result: round-19/falsify is `unsettled`, round-21/build is `unsettled`, round-18/build/dispatch-95.json is `partial` (75/95), and 172 of the 209 missing are not report failures.
3. A first refusal is not a final state. Retries spawned these waves: round-15/build (direct spawn after two refused eval attempts), round-17/build (82), round-20/build (attempt 2 spawned 72 after attempt 1 refused all 72, spawned 0), round-20/falsify (86 after attempt 1 refused all 86, spawned 0). Spawn state must come from the successful attempt's record.
4. Lane labels disagree with report presence. round-20/build completion-summary lists dead_original_seats [CellDesign, SrcGateStandard]; SrcGateStandard's report is present (6468 B), so the tool would count it present. round-17/falsify completion-summary says terminal failed 9, while 7 reports are missing (80 dispatched minus 73 advice files).
5. Naive text search overcounts. 22 JSON files contain the literal `ufo-swarm-wave-dispatch-v1`; the top-level rule admits 19. The 3 extra are wrappers whose `stdout` string embeds a dispatch JSON: .ufo/waves/round-15/build/validation.json, .ufo/waves/round-15/falsify/validation-final.json, .ufo/waves/round-15/falsify/validation.json.
6. Parser disagreement. `round-20/build/out/GateSelftestCrash/receipt-B-surrogate-summary-exit.json` is rejected by jq 1.8.2 (invalid surrogate-pair escape, column 4516) but accepted by Python json. `round-20/build/out/RegReceiptSixPin/nonjson.json` is rejected by both. Unreadable count: 2 under jq semantics, 1 under Python semantics.
7. Misroot history. round-16/falsify/completion-summary.json records RevengerRunReceipts.md "left at fleet root, moved by L1" and two self-relocated reports. Today: 0 misrooted; the fleet-root copy is absent.
8. Snapshot. round-21/build is live. Re-run the counts after it settles.

## 5. JSON totals (lane, at scan)

- `*.json` under .ufo/waves: 296 regular files; 0 symlinks.
- Top-level dispatch schema: 19.
- Unreadable: 1 (Python) or 2 (jq).
- Other parseable JSON, ignored under the contract rule: 276 (Python) or 275 (jq). Composition: 168 objects with no `schema` key; 17 top-level arrays; 20 ufo-swarm-registry-v1; 2 ufo-swarm-wave-v1; the rest other schemas.

## 6. Tooling

- No installs or updates. `pacman -Q jq` was a query only; no pacman transaction was run.
- Used `/usr/bin/jq` (jq 1.8.2-1). Bare `jq` on PATH resolves to `~/.local/bin/jq` (jaq 3.1.1) and was not used.

## Appendix A: Members not present (sorted by name)

### round-11/dispatch.json (2)
Measure (missing), Safety (missing)

### round-15/build/dispatch.json (4)
CaseAudit00 (missing), CaseAudit04 (missing), CaseAudit14 (missing), CaseAudit19 (missing)

### round-17/falsify/dispatch.json (7)
C1AdmissionCritic (missing), C2AdmissionCritic (missing), C2SourcedClaim (missing), ControlsSafety (missing), MistakesFailCapable (missing), SeparabilityNoHarm (missing), TrendVerdicts (missing)

### round-18/build/dispatch-95.json (20)
ConnectKengaku (missing), ConnectMori (missing), ConnectRevengerLane (missing), ConnectSouji (missing), CritScopeCreep (missing), CritTrendPreview (missing), RevExitTables (missing), RevLowestAxis (missing), RevOperatorLessons (missing), RevReportContract (missing), RevengerK6Exit (missing), RevengerZeroObsDecision (missing), ScoutAutomakeExitCodes (missing), ScoutLlamaApiKeyPublic (missing), ScoutPortsSafety (missing), ScoutPySignal (missing), ScribeLessonSkeleton (missing), ScribeLogEntry (missing), ScribeScorecardRound18 (missing), SimplifyC1Plan (missing)

### round-18/falsify/dispatch.json (10)
CheckDecoder (missing), CounterC2 (missing), FaultCache (missing), FreshFault (missing), GateInternalFault (missing), GateLoadingCounts (missing), PriorKills (missing), RerunC2H (missing), ScoreCapabilities (missing), Separability (missing)

### round-19/falsify/dispatch.json (66)
ABoundary (missing), AC1DocBinding (missing), AC1DocWiden (missing), AC1Json (missing), AC1Registry (missing), AC1ShortRev (missing), AC1StaleToken (missing), AC1Unreadable (missing), AC1Uppercase (missing), ACensus (missing), AGateLegacy (missing), AGateSelftest (missing), AGateSixPins (missing), AGateTreeConsistent (missing), AGateTreeMalformed (missing), AGateTreeNoPin (missing), AGateTreeNull (missing), AGateTreePin (missing), AGridAbsent (missing), AGridSelftest (missing), ANoHarm (missing), AR18Defects (missing), ARerunC1 (missing), ARerunC1Selftest (missing), ARunnerArgv (missing), ASeparation (missing), CConnect (missing), CTameshi (missing), ECheckerJson (missing), EGridFailClosed (missing), EGridSchema (missing), EHarnessDry (missing), ELessonGate (missing), EPinMissing (missing), ERunnerAssert (missing), ESourcesRow (missing), KAxisHarm (missing), KClaimC1 (missing), KClaimC2 (missing), KReport (missing), KSourced (missing), KTrends (missing), MDefaultDocs (missing), MShaOff (missing), MTreeSubstr (missing), MUpper (missing), NSentinelHost (missing), NSentinelSecret (missing), PClaimWording (missing), PSimplify (missing), SCensusRows (missing), SDeterminism (missing), SDriftScan (missing), SInstruction (missing), SLdsoQuotes (missing), SLdsoScope (missing), SMisroot (missing), SProvider (missing), SQuality (missing), STreeMembers (missing), VAncestry (missing), VDrift (missing), VOverwrite (missing), WDraftFrontier (missing), WDraftLesson (missing), WDraftReport (missing)

### round-20/build/dispatch.json (1)
CellDesign (missing)

### round-20/falsify/dispatch.json (13)
C1ErrorCensus (missing), C2GgufMeasure (missing), CellCitationMissingToken (missing), CellCitationValidToken (missing), CitationGateLive1 (missing), CitationR18Assignments (missing), CitationR18C1CheckpointExit (missing), CitationR18C2Preofficial (missing), CitationR18FalsifySpec (missing), FixtureBadMagicNearMiss (missing), FixtureV3Minimal (missing), FixtureVersion99 (missing), R18C2EvidenceScope (missing)

### round-21/build/dispatch.json (86)
AuditCutoffCritic (missing), AuditEarlyRounds (missing), AuditErrataMutants (missing), AuditExitContract (missing), AuditGitEnvExec (missing), AuditGitEnvSentinel (missing), AuditHexWordFP (missing), AuditLaneDocHashes (missing), AuditRegexMutants (missing), AuditReport10 (missing), AuditReport11 (missing), AuditReport12 (missing), AuditReport13 (missing), AuditReport14 (missing), AuditReport15 (missing), AuditReport16 (missing), AuditReport17 (missing), AuditReport18 (missing), AuditReport19 (missing), AuditReport20 (missing), AuditSeparateCitation (missing), C1C2Separability (missing), C1ClaimCritic (missing), CapabilityRuleReader (missing), ClosureNotesSweep (missing), ConnectorFleetReportChecks (missing), ConnectorHistory (missing), ConnectorPatterns (missing), ConnectorRoutingNotes (missing), ConnectorSiblingLinks (missing), ErrataR18R10 (missing), ErrataR20Omitted (missing), ErrataR20Splice (missing), KnowledgeSonameEntry (missing), LessonDraftC1 (missing), LessonDraftC2 (missing), LinksBackCompatRegrade (missing), LinksDigestEncoding (missing), LinksDigestFix (missing), LinksGateMutants (missing), LinksGateReview (missing), LinksGridMutants (missing), LinksGridReview (missing), LinksGridSonameCells (missing), LinksLoaderProof (missing), LinksNeededCensus (missing), LinksPolicyCritic (missing), LinksProducerReview (missing), LinksProducerSelftestCase (missing), LinksRealReceipt (missing), LinksTreeDeterminism (missing), LogEntryDraft (missing), MistakeSweep (missing), NoHarmCritic (missing), OperatorTeachings (missing), QualityCriterion (missing), R20FollowupsCheck (missing), RegressErrorCensus (missing), RegressGgufCitation (missing), RegressInstallTreeGrid (missing), RegressProbeSnapshot (missing), RegressSkillGates (missing), ReportFormatDraft (missing), RevengeGateConsumers (missing), RevengeInstallTreeIntent (missing), RevengeOmissionCause (missing), RevengeSpliceOrigin (missing), ScorecardDraft (missing), ShonenMap (missing), SimplifyAudit (missing), SimplifyGrid (missing), SkillRowAudit (missing), SkillRowLinks (missing), SourcesContractReader (missing), SrcGitCatFile (missing), SrcGitLogDiffFilter (missing), SrcGitRevisions (missing), SrcGnuTarSymlink (missing), SrcGoDirhash (missing), SrcJjRebaseTimestamps (missing), SrcLdSoNeeded (missing), SrcLdconfig (missing), SrcNixNar (missing), SrcPythonReadlink (missing), SrcReproducibleBuildsArchive (missing), SrcTldpSoname (missing)

## Appendix B: Dispatch-file provenance

| File | Wave | Bytes | mtime (UTC) | sha256 |
|---|---|---:|---|---|
| round-11/dispatch.json | kama-round-11 | 50876 | 2026-10-20T02:13:17Z | 618e5d7bd022b576e4467e0dd5bc2a6ce6f41b45492339221821afcd220af492 |
| round-11/verification-dispatch.json | kama-round-11-verification | 40257 | 2026-10-20T03:43:16Z | f34da406475d4e59f83448ce529375814896d6e64a37f327e4a6c9f581edae5b |
| round-12/dispatch.json | (null) | 47765 | 2026-10-20T04:18:38Z | bc476e62c212c0499740708fc90ab447cdfbad9d9ab37203a5dc6ff4d589358d |
| round-13/dispatch.json | (null) | 46428 | 2026-10-20T04:54:16Z | 3ca00d54a13bcd3322d19e5ddc1b30b489fcd7ee58a6554e4ce7ceb9b1558ef9 |
| round-14/dispatch.json | (null) | 44915 | 2026-10-20T06:26:44Z | 07fbdcb4e7d8ca625221192e2f8e2854dd2aa00011b68637472b98661352fc47 |
| round-15/build/dispatch.json | (null) | 91441 | 2026-10-20T08:01:51Z | 3b8d9da217518a2861d72f025def30608a55b09d6f46094e81c98add33784457 |
| round-15/falsify/dispatch.json | (null) | 39532 | 2026-10-20T08:18:25Z | e318064fc6a895ccabb06a31ae629b508a0c2249dcd9eb77c4516d3aaa6876e3 |
| round-16/build/dispatch.json | (null) | 132812 | 2026-10-20T13:50:49Z | c9484afc86504d75211d6060c8e214048184634f5ec3be9eb43dc5aedda3cdae |
| round-16/falsify/dispatch.json | (null) | 109521 | 2026-10-20T13:52:57Z | 0ef929dc4df003ee14578c8f834ba3e28e932f5da397445e2e003c7182b2d0c0 |
| round-17/build/dispatch.json | (null) | 148800 | 2026-10-20T15:03:04Z | 7c80f4c8bf6bdbd65d9367cc66fb1cfa156b1ff1d0e50f8a47710bd8428daf6a |
| round-17/falsify/dispatch.json | (null) | 110612 | 2026-10-20T16:28:11Z | 61c2fadfe6f2b7b5ebe6b702d944053a22663996415c38b147867c3c2c0385c4 |
| round-18/build/dispatch-95.json | (null) | 171837 | 2026-10-20T20:59:16Z | 59ec84c1fa30c392f8de8b27277550dcad15d006585b4462086e479b92b36744 |
| round-18/build/dispatch.json | (null) | 142296 | 2026-10-20T20:59:16Z | 470ae3ad6fd13e6142cf45143a34c9d99581ea339c606aa23756513c857434e4 |
| round-18/falsify/dispatch.json | (null) | 87937 | 2026-10-20T23:14:51Z | e41f27bff52806312aa85323fecc3d637481eedbb47fe202eca4d2803606b249 |
| round-19/build/dispatch.json | (null) | 100979 | 2026-10-21T06:26:39Z | de806ed858ec94c32a886fde9e8a478ef6b6eb7d7ae881d667454a488cddcead |
| round-19/falsify/dispatch.json | (null) | 85559 | 2026-10-21T06:38:58Z | 59112a66b5a1c77d20d0ac5c058a407e01504a63774b276579bb0d006608e59c |
| round-20/build/dispatch.json | (null) | 116016 | 2026-10-21T07:15:41Z | 20d28bd4227e8b7408809d310c98f6380320f7eba4ad9c6bca69fc83cfca3408 |
| round-20/falsify/dispatch.json | falsify | 116075 | 2026-10-21T09:02:55Z | fadfb7fed49a3d91b4302dac1f53799e2099c1212754bc64d7c03186e6e8e7eb |
| round-21/build/dispatch.json | (null) | 151687 | 2026-10-21T10:28:38Z | 801484e0e7f849a8668d44974111d00ad8a427678bdaf4e5878fc74f789ed29a |
