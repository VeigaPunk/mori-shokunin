# ScribeGateDecisions — mori-r15-positive (C1 coverage)

Scope: report-only. Drafts admit/reject sample expectations and records why the dispatched seats are not an outside review. Counts are grounded in wave files only. No builds, tests, gates, or fixture executions were run. No production files were edited.

Installations: none performed. The parent host-safety notice (pacman pre-check, no -Sy/-Syu/-U/-R) was received and is noted; this task required no installs.

## 1. Grounded file facts

Sources: `.ufo/waves/round-15/{spec.json,dispatch.json,task-response.json,build/swarm-registry.json}` under `/home/vgpnk/Projects/shokunin/mori-shokunin`.

- Wave: `mori-r15-positive`; milestone "retain validated positives without fabricated totals"; reportDir `.ufo/waves/round-15/build`.
- `dispatch.json` counts: spawn 64, resume 0, total 64. Single batched `taskCall` (one-swarm-per-wave note). `resumeSends` is empty.
- `spec.json` items: 64. Role distribution (sums to 64):

| role | count | seats |
|---|---|---|
| executor | 24 | CensusPositive, HarnessBuild, ProvenanceCapture, SkillInterface, KnowledgePositive, IndexPositive, QualityDebt, RegistryFrontier, and 16 Pack* seats |
| scout | 8 | ReconFieldTypes, ReconBootScope, ReconResultEmitter, ReconParserContracts, ReconQueryBounds, ReconLegacySignal, ReconDirtyRevision, ReconProtectedTeaching |
| connector | 6 | ConnectPlannerWalk, ConnectSiblingOverlap, ConnectFrontier, ConnectNoHarmAxes, ConnectSourceChain, ConnectReceipts |
| reviewer | 8 | ReviewKernelPredicate, ReviewUnitPredicate, ReviewProcessPredicate, ReviewRawTotals, ReviewRouting, ReviewHarnessPacks, ReviewHarnessGate, ReviewDocumentation |
| critic | 8 | AttackFalsePositive, AttackSuppression, AttackSignalConfusion, AttackCountVacuity, AttackFixtureOracle, AttackNoHarm, AttackProvenance, AttackSourceOverreach |
| scribe | 6 | ScribeSourceCensus, ScribeRoutedDebt, ScribeNoHarmLedger, ScribeGateDecisions, ScribeReportContract, ScribeFixtureInventory |
| revenger | 2 | HistoryOriginalIntent, HistoryDirtyHistory |
| sentinel | 2 | SecurityPrivacy, SecurityTrust |

- `task-response.json`: "Spawned 64 background agents" using the eight roles above. All 64 seat IDs are `MoriR15.<Name>`.
- Pack seats (fixture producers): 16. Each is assigned one fixture file under `.ufo/waves/round-15/fixtures/`: KernelUser, KernelSystem, UnitUser, UnitSystem, SignalUser, ProcessUser, ForeignBoot, BootArray, NegativeInvalid, NegativeResults, NegativeStatus, CrossScope, SubjectUnknown, FanoutPositive, OrderMixed, CleanControls. Each is specified as 2–4 cases. Expected total: 32–64 cases.
- Fixture status on disk: `.ufo/waves/round-15/fixtures/` does **not exist** yet. Zero fixture packs are present. Count of produced cases: 0 (unverified; no packs have landed).
- `invalid_class` values named in seat prompts: `kernel_oom_notice`, `unit_failure_record`, `unit_sigkill_record`. No canonical enum was found in `spec.json` beyond these prompt mentions. The schema owner is not identified in the wave files. Treat the enum as unresolved.
- `build/swarm-registry.json` (schema `ufo-swarm-registry-v1`, 649 lines, `members` block) exists. Member count was not tallied in this report.

## 2. Why dispatched seats are not an outside review

1. All 64 seats come from one `dispatch.json` / one batched `taskCall` in one wave (`mori-r15-positive`), and share one `reportDir`. Every reviewer is a wave-internal lane, not a separate session or wave.
2. The 8 reviewer seats and 8 critic seats are internal gates. Their prompts are "read-only audit … only report", and they are assigned to the same wave registry. Nothing in the wave files identifies a reviewer as external to this wave, to the planner (L1), or to the main agent.
3. The only "outside" token in the wave text is `CensusPositive`: "Read round14 outside spotcheck all routed items." That refers to a prior-round input artifact (round 14 spot-check), not a current outside reviewer seat.
4. A regex scan for `outside|external|independent` over reviewer prompts returned one hit (`ReviewUnitPredicate`). That hit is a false positive: the word is "independent record semantics", not an outside reviewer.
5. Conclusion: the dispatched review is entirely internal to the wave. No outside review is evidenced in these files. Outside review remains unclaimed, and the report must not be presented as independently reviewed.

## 3. Draft admit/reject sample expectations (static, not executed)

Expectations are derived from the shared contract literals in `spec.json` context. They are drafts. They are not run results and must not be treated as observed behavior.

Literals (from contract): `_BOOT_ID` current = `11111111111111111111111111111111`; kernel MESSAGE_ID = `fe6faa94e7774663a0da52717891d8ef`; unit MESSAGE_ID = `d9b373ed55a64feb8242e02dbe79a49c`; process MESSAGE_ID = `98e322203f7a4ed290d09fe03c09fe15`. Unit result exact string `oom-kill` (OOM) or `signal` (signal). Process exact `killed` with scalar status `9`.

Field-name mapping: the contract does not name the process fields. The seat prompts name `EXIT_CODE` (exact `killed`) and `EXIT_STATUS` (scalar `9`). This mapping is **inferred** from prompts (INFERENCE) and is unverified against the r14 helper.

**Admit (expect positive = true, want_oom/want_signal as stated):**
- A1 kernel: one object record, scalar MESSAGE_ID matching kernel id, scalar `_BOOT_ID` current → `positive_kernel_oom` true.
- A2 unit OOM: MESSAGE_ID matches unit id, `UNIT_RESULT` exactly `oom-kill`, current boot → `positive_unit_oom` true.
- A3 unit signal: MESSAGE_ID matches unit id, `UNIT_RESULT` exactly `signal`, current boot → `positive_unit_signal` true.
- A4 process SIGKILL: MESSAGE_ID matches process id, `EXIT_CODE` exactly `killed`, `EXIT_STATUS` scalar `9`, current boot → `positive_process_sigkill` true.
- A5 mixed: one invalid record plus one valid current-boot record → aggregate class invalid (raw counts unavailable), but the positive token stays true. OOM fires once.

**Reject (expect positive = false for that record; never a numeric zero):**
- R1 kernel/unit/process with a different MESSAGE_ID value → excluded.
- R2 foreign `_BOOT_ID` (any value other than current) → excluded.
- R3 `MESSAGE_ID` as array, object, or null → excluded.
- R4 `_BOOT_ID` as array, null, or missing → excluded.
- R5 `UNIT_RESULT` as array, null, missing, or wrong case (`OOM-KILL`) → excluded, never evidence.
- R6 `EXIT_CODE` array, wrong code, or null → excluded.
- R7 `EXIT_STATUS` array or null → excluded (never valid SIGKILL).
- R8 top-level element that is not an object → excluded.

**Unresolved fact (flag, do not decide):**
- Whether `EXIT_STATUS` as string `"9"` counts as "scalar status 9". The contract says "scalar", which could admit strings. Requires the owner's decision; draft expects reject until resolved.

**Cross-scope expectations (draft):**
- A system-scope signal must not produce a user WARN.
- A user-scope negative record must not suppress a system-scope positive OOM.

## 4. Unresolved facts (honest)

- Fixture packs: 0 of 16 present. No case count, no id uniqueness, and no literal-value check has been performed on real files.
- `invalid_class` enum: not canonicalized in the wave files.
- Process field names (`EXIT_CODE` / `EXIT_STATUS`) and the string-`"9"` question: unresolved, see §3.
- Stub ignore-filter mode for the r14 helper `journal_stub_body`: named in seat prompts; not read or verified here (out of assignment).
- Outside review: none evidenced (see §2).
- No behavior was executed. All expectations are static drafts.

## 5. Handoff

- Checks for main agent to run once after integration: (a) `.ufo/waves/round-15/fixtures/*.json` count and case-id uniqueness; (b) literal expected values against §3; (c) resolve the string-`"9"` question and the `invalid_class` enum; (d) confirm reviewer independence claim is absent or explicitly internal.
- Changes: none to production. Report file only.
