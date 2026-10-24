# WaveRegistryVsReports — registry/dispatch task names vs report files on disk (round 17)

Seat: `MoriR17.WaveRegistryVsReports-5` (leaf, read-only advisor; no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`, entering tip `24526ea9617cd020fee16c28fe4d4a2789dc28cb`.
Snapshot: **2026-10-20T19:02:49Z** (= 16:02:49 -03). Every count below is point-in-time.
Writes: this report only. No VCS mutation, no transcript content read, no `/tmp` write, no install.

## Verdict

**ISSUES (for the orchestrator tally), not for any lane's delivery.** Every round-17 registry member in
tabi, tsukuroi, souji, tameshi and kama resolves to at most one exact `<Task>.md`; no near-miss or
misplaced report exists. In the three lanes the transcript scan covers, the missing-report set
reconciles exactly with the terminal classes: **98 non-delivering seats = 94 `dead_rate_limit` + 4
`aborted`** (tabi 26 = 22+4, tsukuroi 44 = 44, souji 28 = 28); 40 of the 94 dead seats are named in
lane records, and all 40 are in the missing set. Tameshi adds **7 non-delivering seats of unknown
class** (not covered by the transcript scan). The quoted orchestrator tally **17 / 43 / 28+** disagrees
with the independent path: **26 / 44 / 28** under "no report on disk", **18 / 44 / 28** under the narrow
zai-retry-budget metric. Kama falsify is **in flight** (12 missing at snapshot, falling) and is not a
death count; kama build is complete (82/82).

## Method (read-only)

1. For each wave, read the wave's own record: `swarm-registry.json` / `record.json` / `record-result.json`
   / `registry*.json` → `members` (task name) and `reportDir`.
2. Read the sibling `spec.json` / `*-spec.json` / `assignments.json` / `dispatch*.json` and the spawn
   echo (`spawn-result.*`, `dispatch-result.json`, `*-dispatch-attempts.*`).
3. A task counts as delivered iff **`<reportDir>/<member-name>.md` exists as a regular file**. Exact
   name, no case folding, no prefix matching. Reports count only for names that are registry members;
   non-member `.md` files are reported as orphans.
4. Rejected false explanations: (a) zero-byte or placeholder reports — none (smallest member report
   1,519 B; zero zero-byte files in every wave); (b) a differently-cased/near-miss filename — 0 hits
   for every missing name in every wave; (c) a report placed elsewhere in the lane's round-17 tree —
   0 hits for every closed-wave missing name. Kama falsify is the one exception at the 18:57Z check:
   `ConnectKagi` / `ConnectKumitate` had same-name **wave-1** reports under `build/advice`; those are
   not falsify deliveries, and both falsify reports had landed by the 19:02:49Z snapshot; (d) a seat
   that was registered but never spawned — spawn echoes carry
   exactly the assigned id set in all six waves where the echo is machine-readable, 0 assigned-but-
   not-spawned (tabi w1 86, tabi w2 78, tsukuroi build 72, tsukuroi falsify 81, kama build 82, kama
   falsify 80).
5. "Closed" means the report directory stopped changing before the snapshot and a lane-level landing/
   summary/commit exists at or after the last report. "In flight" means reports were appearing within
   the last minute; those are **never** counted as deaths (kama falsify and mori build, §6).
6. Transcript terminal classes are quoted, not re-derived: `build/DeadSeatCrossCheck.md:85-91`
   (`scan_utc 2026-10-20T18:59:29Z`), classes per `contract.md:40-50`. That seat read only the
   contract's field list; no content is reproduced here.

## 1. Result table (snapshot 19:02:49Z)

| lane | wave | dispatch spawn | registry members | member reports | missing | wave state |
|---|---|---:|---:|---:|---:|---|
| tabi | w1 | 86 | 86 | 86 | 0 | closed (last report 14:44) |
| tabi | w2 | 78 | 78 | 52 | **26** | closed (last report 14:30; deaths to 14:58) |
| tsukuroi | build | 72 | 74 | 72 | **0 dispatched** (2 phantom keys) | closed (last report 13:52) |
| tsukuroi | falsify | 81 | 81 | 37 | **44** | closed (outcome 14:43; last report 15:16) |
| souji | w1 | 78 | 78 | 78 | 0 | closed (last report 15:47) |
| souji | w2 | 71 | 71 | 43 (+1 orphan) | **28** | closed (root resumed; last report 15:32) |
| tameshi | w1 | 67 | 67 | 67 | 0 | closed (last report 13:41) |
| tameshi | w2 | 99 | 99 | 92 | **7** | closed (last report 13:48) |
| tameshi | w3 | 8 | — (residual spec) | 8 | 0 | closed (job-cap refusal recovered) |
| kama | build | 82 | 82 | 82 | 0 | closed (summary at 13:24) |
| kama | falsify | 80 | 80 | 68 | 12 | **IN FLIGHT** (last report 19:01:44Z) |
| mado (extra) | w1 | 70 | 70 | 69 | 1 | closed; lane now on round 19 |
| mado (extra) | w2 | 78 | 78 | 78 | 0 | closed |
| mori (own) | build | 70 | 70 | 61 | 9 | **IN FLIGHT** |

Closed waves of the five named lanes: **722 dispatched, 617 delivered, 105 missing**.
Of those 105: **98 are in the three transcript-scanned lanes** (tabi, tsukuroi, souji) and **7 in
tameshi**.

## 2. Missing inventories (closed waves)

### tabi w2 — 26 missing

Roles (registry): reviewer 21, connector 3, revenger 1, sentinel 1.

```
ConnJjSiblingsAfter      ConnReadmeC2           ConnUnmappedOverlaps
RevAttachedIdentity      RevBindSelftestCases   RevC1Fallback
RevC3Counter             RevDiffBind            RevDiffRound
RevDiffUser              RevFreshnessWhyNot     RevIdentityChain
RevLabelOnly             RevLessonDraft         RevLocalVsPushed
RevNoteVsSources         RevOtherScriptsHead    RevReceiptConc
RevReceiptDecl           RevReceiptErrors       RevRouted4
RevRoutedHardenedAfter   RevSearchLog           RevSitesInventory
RevSkillDraft            SentinelC3After
```

Four of these are named as deaths by the transcript scan: `RevLabelOnly` (18th zai
retry-budget death, `DeadSeatCrossCheck.md:159`) and `RevBindSelftestCases`,
`RevLocalVsPushed`, `RevNoteVsSources` (the three zai 429 records without a retry-budget prefix,
`DeadSeatCrossCheck.md:123`). All four are in the missing set.

Tabi w2 had no dispatch refusal: attempt 1 `refused: 0` and the result text spawned 78
(`w2/dispatch-attempts.json:1-7`, `w2/dispatch-result.json`). The missing seats were spawned and
then stopped producing reports.

### tsukuroi falsify — 44 missing

Roles: reviewer 35, connector 5, revenger 3, simplifier 1. Every critic, sentinel, scout,
mutation-tester and 7 reviewers delivered; the gap is concentrated in the late-role batches.

```
FxAuditLiveAgree      FxAuditSelftest       FxBindLocaClar
FxBindRootDacCorr     FxBindSourScopCorr    FxBindUpdaRech
FxC1Rerun             FxC3Rerun             FxConnPlannerGap
FxConnSibling         FxConsistentPre42     FxEntryEfifallback
FxEntryLinux          FxEntryLinuxlts       FxEntrySnapshot1Linux
FxEntrySnapshot2Linux FxEntrySnapshot2Linuxlts FxFreshArchNewsGate
FxFreshDrivFirmPlan   FxFreshInitV42Sysr    FxFreshOverreach
FxFreshPartUpgrRech   FxFreshSnapEaccMech   FxFreshUpdaSafeV3
FxFrozenMarker        FxL0Correction        FxLessonGate
FxLogEntry            FxOwnS051             FxOwnS056
FxQuality2527         FxReadmeFrontier      FxRecheckBlocks
FxRecheckRerun        FxRejectedReadings    FxRevengerPlymouth
FxRevengerSnapperCopy FxRevengerSwitchRoot  FxScorecardRound17
FxSeatScopeRerun      FxSeparability        FxSimplifyAudit
FxSkillContract       FxW04
```

`FxFrozenMarker` is the 44th/last zai death (`DeadSeatCrossCheck.md:160`). The lane's own
`falsify/outcome.json` lists 36 `dead_seats_provider_429` (`:15-52`) and 16
`still_running_at_landing` (`:53`); by the snapshot 8 of those 16 delivered and 8 did not
(`FxBindSourScopCorr`, `FxFreshUpdaSafeV3`, `FxFrozenMarker`, `FxReadmeFrontier`,
`FxRecheckRerun`, `FxRevengerSnapperCopy`, `FxRevengerSwitchRoot`, `FxSeparability`). The
outcome is a 14:43 point-in-time tally; it is stale, not contradicted (see §5).

### souji w2 — 28 missing

Roles: reviewer 27, connector 1.

```
ConnSiblingAdjacency2  FixtureOracleD1        FixtureOracleD2
MutateCensusD1         RerunCensusSelftest    RerunGateReplays
RerunJjFixture         RerunReceiptSelftests  RevCensusHeaderTruth
RevD5D7Lines           RevEmitSoftDiag        RevForEachRefExclude
RevFrozenRegenerated   RevHelperPhantomOrder  RevJjNovelIdentical
RevJjNovelPaths        RevKnowledgeEntry      RevLessonMistakesDraft
RevMisrootSweep        RevOpenResidualTable   RevOperatorSweepFp2
RevQualityRows         RevQuarantineRunbook   RevRelativeRow
RevScorecardDraft      RevStubReceipt         RevVProbeRows
RevVadv54Harness
```

Wave 2 recorded one job-cap refusal for `RerunMatrixLanded` at 14:28:37, then spawned 71 at
14:31:37 (`w2-dispatch-attempts.txt:1-2`), so the 28 were spawned. The w2 report directory also
holds `GateExactIds.md`, a name that belongs to w1 and is not a w2 registry member; counting it
as a delivery would wrongly turn 28 missing into 27. The lane root transcript
`SoujiR17-3.jsonl` was `dead_rate_limit` in one pass and `incomplete` (resumed) at the canonical
scan (`DeadSeatCrossCheck.md:194-196`), i.e. the L1 itself was hit and resumed before landing
the wave.

### tameshi w2 — 7 missing

Roles: critic 5, sentinel 2.

```
CriticC1  CriticC2  CriticNoHarm  CriticSeparability  RegistryProvenance
SentinelLanded  SentinelTraceEscape
```

No lane outcome/landing summary lists these seats, and the transcript scan did not cover the
`TameshiR17` prefix. Cause is `[UNKNOWN]`; the role pattern matches the late-batch losses in
tabi/tsukuroi/souji `[INFERENCE]`. The wave's initial dispatch was refused once by the job cap
and then spawned all 99 (`dispatch2-refusals.txt:1`); the seven were spawned.

### tameshi w3 — 0 missing

`spawn3-residual.json` carries 8 tasks (`RR1`–`RR8`), all 8 reports exist. The one refusal
(`dispatch3-refusals.txt:1`, job cap at 13:46:30, retried every 180 s) cost no seat.

## 3. The tsukuroi build "2 missing" are registry phantoms, not seats

`build/record-result.json` has 74 members, but `build/spec.json` and `build/dispatch.json` have
72 (`counts.spawn = 72`), and all 72 spec-named reports exist. The two extra keys are
`BootChainEntry` (scribe) and `BootChainJson` (executor), both with `agentId: null`, absent from
`assignments.json` and `spec.json`. The spec's actual names are `BootChainEntryAudit` and
`BootChainJsonAudit`, and `BootChainEntryAudit.md` / `BootChainJsonAudit.md` are both present.
The registry was seeded from a different naming source; **0 dispatched seats are missing**.
This is the only registry-vs-spec name divergence found in any wave.

## 4. Cross-check against transcript terminal classes

Source: `build/DeadSeatCrossCheck.md:88-91` (scan 18:59:29Z, 469 files, contract classes). The
three wave report sets did not change between that scan and this snapshot (last report mtimes
14:30 / 15:16 / 15:32, all earlier).

### 4.1 Count reconciliation

Per lane, the transcript scan includes one lane-root transcript; `TabiR17.jsonl` and
`TsukuroiR17.jsonl` end `completed` (`DeadSeatCrossCheck.md:179`), `SoujiR17-3.jsonl` ends
`incomplete` (`:194-196`).

| lane | registry seats | transcript seat classes (root excluded) | present reports | missing reports | decomposition |
|---|---:|---|---:|---:|---|
| tabi | 164 | completed 137, aborted 4, dead_rate_limit 22, incomplete 1 | 138 | 26 | 138 = 137 completed + 1 incomplete; 26 = 22 dead + 4 aborted |
| tsukuroi | 153 | completed 107, aborted 2, dead_rate_limit 44 | 109 | 44 | 109 = 107 completed + 2 aborted; 44 = 44 dead |
| souji | 149 | completed 121, dead_rate_limit 28, root incomplete | 121 | 28 | 121 = 121 completed; 28 = 28 dead |
| **total** | **466** | completed 365, aborted 6, dead 94, incomplete 1 | **368** | **98** | **368 = 365 + 2 aborted + 1 incomplete; 98 = 94 dead + 4 aborted** |

Observed name-level checks:

- `tsukuroi/falsify/outcome.json` names 36 dead seats (`:15-52`); **36/36 have no report**.
- `DeadSeatCrossCheck.md` names 4 tabi dead seats (`:123`, `:159`); **4/4 have no report**.

Count-forced `[INFERENCE]`: the marginal totals admit only one join — completed→delivered (365),
dead_rate_limit→missing (94), aborted 2 delivered + 4 missing, incomplete 1 delivered. So in the
covered lanes **report absence = dead + the aborted that did not deliver**; no completed seat failed
to deliver and no `dead_rate_limit` seat delivered. This is exact at the count level and confirmed
for all 40 dead seats that lane records name.

### 4.2 Agreement / disagreement against the quoted orchestrator tally

`DeadSeatCrossCheck.md:3` quotes the orchestrator: "tabi r17 lost 17, tsukuroi r17 43, souji r17
28+". That report observed **18 / 44 / 28** under the narrow zai retry-budget metric (`:89-91`,
`:159-160`). This path adds the no-deliverable dimension:

| lane | claim | narrow zai metric (transcripts) | no report on disk | delta vs claim (no-report) |
|---|---:|---:|---:|---:|
| tabi | 17 | 18 | **26** | +9 |
| tsukuroi | 43 | 44 | **44** | +1 |
| souji | 28+ | 28 | **28** | 0 |

- **Tabi.** 26 = 18 zai retry-budget + 3 zai 429-without-retry-prefix + 1 anthropic 429 + 4 aborted.
  The claim undercounts whichever definition is meant; the no-deliverable count is 26.
- **Tsukuroi.** 44 under both the narrow metric and report absence. The claim's 43 is one low.
- **Souji.** 28 under both; "28+" is satisfied exactly.

This path therefore **agrees** with the transcript scan in all three covered lanes and **disagrees**
with the orchestrator's 17/43 the same way the transcript scan does, and by more under "lost" =
"delivered nothing".

### 4.3 Agreement with lane-authored records

- **kama build:** `completion-summary.json` records `dispatched: 82`, `terminal.completed: 82`,
  `failed: 0`, `advice_reports: 82`, `missing_reports: []` (`:3,16-21,31`). Observed 82/82. Agrees
  exactly. (The 1 refused task call at 14:59Z, `:30`, was retried and all 82 spawned.)
- **tabi w1:** `w2/ScoutSeatTally.md:56` says no permanently dead seat and 86/86 reports; observed
  86/86. Agrees. That report explicitly leaves wave 2 unchecked
  (`w2/DraftLog2.md:36`); the 26 above fill that gap.
- **tsukuroi falsify:** the 14:43 outcome's 36-dead + 16-running split is **stale, not
  contradicted**: 8 running seats later delivered, 8 later died. The snapshot's 44 missing equals
  the transcript's 44 dead exactly. The discrepancy is timing (deaths at 14:36–15:10, tally at
  14:43), and it shows why a mid-wave "still running" label is not a final class.

## 5. In-flight waves: missing must not be counted as dead

- **kama falsify** (registry created 16:27:57Z, updated/spawned 18:35:49Z): 29 missing at the 18:57Z snapshot, 19 at 18:59Z,
  12 at 19:02:49Z, reports still appearing (`.../falsify/advice` newest mtime 19:01:44Z). All 80
  were spawned (`spawn-result.json`; `attempts.json` shows capacity-gated retries, no refusal).
  **0 deaths observed; 12 outstanding.**
- **mori build** (own wave, registry updated 18:54:21Z): 61/70 reports at 19:02:49Z and landing
  while this seat ran (the 9 outstanding included this seat, then unwritten). **Not a death count.**

This is the strongest control in the dataset: the same predicate ("member has no `<Task>.md`")
falls by 17 in ~6 minutes in a live wave. Any dead-seat tally must state the wave's closure.

## 6. Registry / dispatch defects found (non-fatal)

1. **tsukuroi build:** 2 phantom members (`BootChainEntry`, `BootChainJson`), `agentId: null`,
   absent from spec/assignments/dispatch; real reports exist under the `…Audit` names. Do not
   count as dead seats.
2. **souji w2:** orphan `GateExactIds.md` (a w1 member name) in the w2 report dir. Excluded from
   the 43; including it gives a wrong 27-missing count.
3. **kama build:** every registry `agentId` is `null` (created pre-spawn). `agentId: null` is not
   evidence of non-dispatch; use `dispatch.json` counts and the 82-id spawn echo.
4. **mado w1 (extra scope):** `TripwireCore` has no report, but mado's newest round is 19
   (tip `7b4839d`, 15:56:40); round-17 w1 is historical residue, not a current seat.
5. **Job-cap refusals are not seat deaths:** tameshi w2 (refused once, then 99 spawned), tameshi
   w3 (refused, retried, 8/8 delivered), souji w2 (refused once, then 71 spawned). The failure
   mode to watch is post-spawn silence, not dispatch refusal.

## 7. Dead-seat counts this path supports

| group | seats | evidence class | confidence |
|---|---:|---|---|
| tabi r17 w2 | 22 dead_rate_limit + 4 aborted = **26** no-report | transcripts 18:59:29Z + reports | high (count-exact; 4 names observed) |
| tsukuroi r17 falsify | **44** dead_rate_limit = 44 no-report | transcripts + reports | high (count-exact; 36 names observed) |
| souji r17 w2 | **28** dead_rate_limit = 28 no-report | transcripts + reports | high (count-exact) |
| tameshi r17 w2 | **7** no-report, class unknown | reports only | medium (cause `[UNKNOWN]`) |
| kama r17 build | 0 | reports + lane summary | high |
| kama r17 falsify | 0 observed; 12 outstanding | reports (in flight) | not count-able yet |
| tabi w1, tsukuroi build, souji w1, tameshi w1/w3, mado w2 | 0 | reports | high |

Totals: **94 confirmed `dead_rate_limit` seats** (22 + 44 + 28) and **105 non-delivering closed-wave
seats** (94 dead + 4 aborted + 7 tameshi unknown). The four aborted tabi seats are not rate-limit
deaths under `contract.md:41`; do not merge them into a 429 tally.

## 8. Limits

- **Report absence is not a terminal class.** A seat can complete without writing (not observed
  here: 365/365 completed seats delivered), or write before dying (observed once: the tabi
  incomplete seat delivered). The 94/44/28 equalities are exact at the count level in this
  snapshot; per-seat class joins are `[INFERENCE]` outside the named seats.
- **Live state.** DeadSeatCrossCheck itself saw a `dead_rate_limit` become `incomplete` on
  resume (`:194-196`), and Souji's first pass read 29 dead vs 28 canonical (`:94-96`). Any
  reclassification after 19:02:49Z changes these numbers.
- **Prefix coverage.** The transcript scan covers only `TabiR17`, `TsukuroiR17`, `SoujiR17`
  (`:102`). Tameshi (`TameshiR17`), kama (`KamaR17`), mado and mori are **not** covered; tameshi's
  7 remain class-unknown.
- **Lane-root extra file.** Each lane's transcript inventory contains one lane-root file; the
  arithmetic above excludes it explicitly. A future re-run that forgets this adds a phantom seat.
- **Naming.** Some lanes use abbreviated task names (`FxBindLocaClar`, `FxFreshUpdaSafeV3`), but the
  same names are the dispatch names in `spec.json`, so exact-name matching is correct. Do not
  "repair" them to longer prose names.
- **No transcript content** was read by this seat; class counts are quoted from the in-lane
  DeadSeatCrossCheck report.

## 9. Reproduce (read-only; rc 0)

Run from the fleet root. The snapshot script that produced §1 (member names vs exact `<Task>.md`;
prints counts, missing lists, orphans):

```bash
python3 - <<'PY'
import json,os,time
cases=[
 ('tabi','w1','tabi-shokunin/.ufo/waves/round-17/w1/record.json','tabi-shokunin/.ufo/waves/round-17/w1'),
 ('tabi','w2','tabi-shokunin/.ufo/waves/round-17/w2/record.json','tabi-shokunin/.ufo/waves/round-17/w2'),
 ('tsukuroi','build','tsukuroi-shokunin/.ufo/waves/round-17/build/record-result.json','tsukuroi-shokunin/.ufo/waves/round-17/build'),
 ('tsukuroi','falsify','tsukuroi-shokunin/.ufo/waves/round-17/falsify/record-result.json','tsukuroi-shokunin/.ufo/waves/round-17/falsify'),
 ('souji','w1','souji-shokunin/.ufo/waves/round-17/registry.json','souji-shokunin/.ufo/waves/round-17/w1'),
 ('souji','w2','souji-shokunin/.ufo/waves/round-17/registry-w2.json','souji-shokunin/.ufo/waves/round-17/w2'),
 ('tameshi','w1','tameshi-shokunin/.ufo/waves/round-17/record1.json','tameshi-shokunin/.ufo/waves/round-17/w1'),
 ('tameshi','w2','tameshi-shokunin/.ufo/waves/round-17/record2.json','tameshi-shokunin/.ufo/waves/round-17/w2'),
 ('kama','build','kama-shokunin/.ufo/waves/round-17/build/advice/swarm-registry.json','kama-shokunin/.ufo/waves/round-17/build/advice'),
 ('kama','falsify','kama-shokunin/.ufo/waves/round-17/falsify/advice/swarm-registry.json','kama-shokunin/.ufo/waves/round-17/falsify/advice'),
]
print(time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
for lane,wave,rf,rd in cases:
    m=json.load(open(rf))['members']
    fs={x[:-3] for x in os.listdir(rd) if x.endswith('.md')}
    miss=sorted(set(m)-fs)
    print(lane,wave,'members',len(m),'reports',len(fs&set(m)),'missing',len(miss),
          'orphan',sorted(fs-set(m)),'|',','.join(miss))
PY
echo "rc=$?"
```

Observed at run time: `2026-10-20T19:02:49Z`, rc 0; output matches §1 (tabi w2 26, tsukuroi
falsify 44, souji w2 28, tameshi w2 7, kama falsify 12 at that instant). Recheck at
`2026-10-20T19:07:40Z`: tabi w2 52/26, tsukuroi falsify 37/44, souji w2 43/28, newest mtimes
unchanged (14:30:30 / 15:16:19 / 15:32:12).

Auxiliary checks run, all rc 0:

- `git -C <lane>-shokunin log -1 --format='%H %cI %s'` for tabi, tsukuroi, souji, tameshi, kama,
  mado, mori (closure/ordering evidence; no VCS mutation).
- spawn-echo comparison (`- \`<AgentId>\` (job ...)` sets vs `assignments.json` values): 0
  assigned-but-not-spawned in all six machine-readable waves.
- sizes: `min(member report bytes) ≥ 1519`, 0 zero-byte reports in every wave.

## 10. Tool installs

None. No pacman/uv/npx/cargo action was needed; no sudo was used. No `/tmp` write, no background
job, no journal query, no VCS mutation.
