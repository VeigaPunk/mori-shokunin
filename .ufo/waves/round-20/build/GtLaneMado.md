STATUS: complete

# GtLaneMado: C2 independent ground truth, mado-shokunin dispatch-v1 settlement

Seat `MoriR20.GtLaneMado`. Leaf member, no subagents. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin` was read-only (no writes, no git/jj). Fleet root `/home/vgpnk/Projects/shokunin`.

Manual ground truth, independent of `tools/mori-wave-settlement.py` (not run) and `tools/mori-census.sh` (not run). `frozen/c2-expected.json` was not opened. Definitions follow `round-20/contract.md` §C2:
- Discovery: regular `*.json` under `.ufo/waves` with top-level `schema == ufo-swarm-wave-dispatch-v1`.
- Members: `taskCall.tasks[]`.
- Trailer: last line of a task matching `^Report: write your scoped findings to (\S+)$`.
- `present`: regular non-symlink file, size > 0. `misrooted`: missing under the lane root, but a regular file at the same relative path under the fleet root.

## Tooling
- Nothing installed or updated.
- `/usr/bin/jq` is jq-1.8.2 and was used for every jq step. `~/.local/bin/jq` is also jq-1.8.2.
- Observed: in this seat's persistent shell, `jq` is a builtin that runs jaq 3.1.1 (`jq --version` printed `jaq 3.1.1`). No figure here depends on it.
- Python 3.14.8 stdlib (`json`, `os.lstat`, `hashlib`, `subprocess`) for cross-checks.

## Discovery (lane-relative)

| Item | Count | Evidence |
|---|---|---|
| Regular `*.json` under `.ufo/waves` | 428 | `find -type f -name '*.json' \| wc -l` = 428; python `os.walk(followlinks=False)` = 428; walk errors 0 |
| Symlinks under `.ufo/waves` (not followed) | 11 | `find -type l`; none named `*.json` (two are `.jsonl`); 0 JSON files reachable only through symlinked directories |
| `ufo-swarm-wave-dispatch-v1` | 16 | jq `.schema` agrees with python `json` for all 428 files (0 mismatches) |
| `ignored_json` (other schema) | 410 | includes `ufo-swarm-registry-v1` ×25 and `ufo-swarm-wave-v1` ×2 (`fleet-round-1-interactive/plan.json`, `round-21/w1-plan.json`) |
| `unreadable_json` | 2 | below |

Unreadable (invalid JSON, neither is dispatch):
- `round-18/tripwire/frozen/malformed-expected-json/expected.json`: 50 bytes, `{"schema": "mado-tripwire-frozen-v1", "inputs": [` then EOF. jq rc 5, "Unfinished JSON term at EOF".
- `round-20/w2/AdvVcsForms/scan-all.json`: 29,232 bytes. Line 1 `MADO_TRIPWIRE: findings` is not JSON. jq rc 5, "Invalid numeric literal at line 1, column 14". The body after line 1 parses with schema `mado-tripwire-verdict-v1`.

Informational, not discovered: `round-17/w1/reports/RevEvidenceLabelsR15.md:83` names the dispatch schema in prose (`.md`). `fleet-round-1-interactive/validation.json` has no top-level `schema` (ignored).

## Per-file totals (16 dispatch-v1 files)

| # | Dispatch file (lane-relative) | Wave | Members | Parsed / unparsed | Present | Empty | Missing (under lane) | Misrooted | State | Name suggests never dispatched |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | fleet-round-1-interactive/dispatch-preview.json | mado-fleet-1-interactive | 32 | 32 / 0 | 0 | 0 | 32 | 0 | unsettled | **yes** (`preview`) |
| 2 | round-13/w1/dispatch.json | mado-r13-w1 | 32 | 32 / 0 | 31 | 0 | 1 | 0 | partial | no |
| 3 | round-14/w1/dispatch.json | mado-r14-w1 | 32 | 32 / 0 | 32 | 0 | 0 | 0 | settled | no |
| 4 | round-15/w1/dispatch.json | mado-r15-w1 | 64 | 64 / 0 | 64 | 0 | 0 | 0 | settled | no |
| 5 | round-16/w1/dispatch.json | mado-r16-w1 | 64 | 64 / 0 | 64 | 0 | 0 | 0 | settled | no |
| 6 | round-16/w2/dispatch.json | mado-r16-w2 | 32 | 32 / 0 | 32 | 0 | 0 | 0 | settled | no |
| 7 | round-17/w1/dispatch.json | mado-r17-w1 | 70 | 70 / 0 | 69 | 0 | 1 | 0 | partial | no |
| 8 | round-17/w2/dispatch.json | mado-r17-w2 | 78 | 78 / 0 | 78 | 0 | 0 | 0 | settled | no |
| 9 | round-18/w1/dispatch.json | mado-r18-w1 | 88 | 88 / 0 | 88 | 0 | 0 | 0 | settled | no |
| 10 | round-18/w2/dispatch.json | mado-r18-w2 | 73 | 73 / 0 | 59 | 0 | 14 | 0 | partial | no |
| 11 | round-19/w1/dispatch.json | mado-r19-w1 | 86 | 86 / 0 | 61 | 0 | 25 | 0 | partial | no |
| 12 | round-19/w2/dispatch.json | mado-r19-w2 | 67 | 67 / 0 | 67 | 0 | 0 | 0 | settled | no |
| 13 | round-20/w1/dispatch.json | mado-r20-w1 | 85 | 85 / 0 | 85 | 0 | 0 | 0 | settled | no |
| 14 | round-20/w2/dispatch.json | mado-r20-w2 | 78 | 78 / 0 | 76 | 0 | 2 | 0 | partial | no |
| 15 | round-21/w1-run.json | mado-r21-w1 | 65 | 65 / 0 | 50 | 0 | 15 | 0 | partial | no |
| 16 | round-21/w2-run.json | mado-r21-w2 | 84 | 84 / 0 | 58 | 0 | 26 | 0 | partial | no |

`taskCall` is an object in all 16 files, so none is `no-spawn`. `unsafe` is 0 in every file.

## Lane totals
- Files 16. Members 1030. Parsed 1030. Unparsed 0. Unsafe 0.
- Present 914. Empty 0. Missing under lane 116 (strict missing 116, misrooted 0).
- States: settled 8, partial 7, unsettled 1, no-spawn 0, unavailable 0.
- Filename never-dispatched flag: 1 (`dispatch-preview.json`). No dispatch-v1 filename contains `undispatched` or `validation`.
- Expected contract exit for this lane: 1 (7 partial, 1 unsettled).
- Duplicates: 0 duplicate member names within a file; 0 report paths shared across members; 1030 unique report paths.
- Trailer: every one of the 1030 tasks ends with the canonical trailer on its last line. No task carries another `Report:` line, and there are no CR, trailing-blank or lenient-only variants.

## Missing members (sorted; report absent under the lane root)
- dispatch-preview.json (32): MadoArcSynthesis, MadoBarLauncher, MadoBarSemantics, MadoBindRules, MadoCloseout, MadoConnectAxes, MadoCriticAdmission, MadoDriftWatch, MadoExecutorEvidence, MadoHealthReport, MadoHyprConfig, MadoHyprLive, MadoIdleLock, MadoMutationProof, MadoMutationSweep, MadoPlaneCensus, MadoProvinceAudit, MadoRouteHypr, MadoRouteIdle, MadoRouteOmarchy, MadoRouteTerminals, MadoRouteThemes, MadoRouteWalker, MadoRouteWaybar, MadoScribeProvenance, MadoSnapshotReceipt, MadoStandingGate, MadoTerminals, MadoThemeFiles, MadoWalkerDepth, MadoWalkerR9, MadoWalkerSurface
- round-13/w1 (1): ProtocolRecon
- round-17/w1 (1): TripwireCore
- round-18/w2 (14): CriticAdmission, CriticHonestyW2, FetchBodyPolicy, FetchVerifyFix, GateRerun, RevengeOldWalkerNotes, ReviewFrozenExpected, ReviewGateDiff, ReviewLesson18, ReviewQuality2426, ReviewSkillRegistry, ReviewTripwireDiff, ReviewWalkerUnknowns, TwFrozenHarden
- round-19/w1 (25): ConnCarriedLedger, ConnFrontierPlan, ConnJjAuditsFleet, ConnRegistryTools, ConnSiblingAnchors, ConnSiblingSupersede, RevDraftBashCVar, RevDraftHelperFn, RevF1F2Repro, RevFreshPinsCounter, RevGateWalkerRow, RevJjDisposition, RevNavigationU, RevPipeRcTip, RevPreReg19, RevQualityOverlap, RevR18Mining, RevReceiptChecker, RevSkillHeadGuidance, RevSourcesContract, RevTwRecallPrecision, RevengeFrozenValidation, RevengeS094Anchor, RevengeWalkerPinHistory, SimplifyTripwireTip
- round-20/w2 (2): ConnConsumers, SentinelPostWaveScan
- round-21/w1-run.json (15): ConnScope, CriticResources, OracleBashSuffix, OracleCallbackBoundArgs, OracleClassAnnotation, OracleClassTargetDormant, OracleGitAddDry, OracleGitAddNn, OracleHasattr, OracleIdFunction, OracleIssubclass, OraclePureDeque, OraclePureFrozen, OracleRecursiveString, SourcePartial
- round-21/w2-run.json (26): AtkAnnotation, AtkBashSuffix, AtkGetattrName, AtkGitAddNn, AtkGitCommitZn, AtkHasattr, AtkIsinstance, AtkJjWorkspace, AtkMethodcallerStored, AtkNamespaceRight, AtkPrintFunction, AtkPrintLambda, AtkPureFrozen, AtkReboundArg, AtkRecursiveString, AtkResetBoundary, AtkShadowPrint, AtkThreadInline, AtkUnusedCall, DocsRejection, GateCase2LateRegistrationAf, GateHistoryC2IndependentTrue, GatePopulationEmpty, RecallDunders, SourceCommit, SourceImap

Per-member rows: `build/GtLaneMado/members.tsv`.

## Checks (command → result)
1. POSIX `[ -s ]` / `[ -e ]` on all 1030 report paths under the lane root: 914 P, 116 M. 0 disagreements with the lstat-based status.
2. `os.lstat` on the 116 missing paths: 116 × `ENOENT`.
3. Misrooted: `lstat` and `[ -f ]` on `/home/vgpnk/Projects/shokunin/<same relative path>` for the 116. 0 regular files. The fleet root does contain its own `.ufo/waves`, so the probe was meaningful.
4. Member extraction: `/usr/bin/jq` and python `json` agree on name, agent, task text, wave and taskCall type for all 16 files.
5. `registry.members` count equals `taskCall.tasks` count in all 16 files (1030 on each side).
6. Report files were examined only via lstat and `test -s`. No report bodies were read.

## Observations for L1
- **dispatch-preview.json.** The name is the only dispatch-status signal. Its text has no `preview`, `undispatched`, `validation` or `dry-run` wording (grep: 0 matches). `taskCall` is an object with 32 tasks, `counts` is spawn 32 / resume 0, its `reportDir` `.ufo/waves/fleet-round-1-interactive/reports` does not exist, and 32 of 32 reports are missing. Under the contract, `no-spawn` applies only when `taskCall` is null, so the expected state is `unsettled`. "Never dispatched" is [INFERENCE] from the name and the absent reportDir. The file cannot prove it.
- `registry.members[*].agentId` is null for all 1030 members in all 16 files. It does not distinguish dispatched from undispatched waves.
- Orphans (present in a reportDir, referenced by no trailer): `swarm-registry.json` in 15 reportDirs, `round-13/w1/reports/MistakeFix.py`, `round-19/w1/reports/TwMerge.md`. A case-insensitive prefix search of every reportDir for the 116 missing names found no near-name file.

## Files written (seat build dir only)
- `.ufo/waves/round-20/build/GtLaneMado.md`: this report.
- `.ufo/waves/round-20/build/GtLaneMado/ground-truth.json`: contract-shaped summary. Discovery counts, 16 waves (lane-relative `dispatch_path`, `dispatch_sha256`, `members` as a count, `counts` per status, `state`, sorted `missing`), and totals.
- `.ufo/waves/round-20/build/GtLaneMado/members.tsv`: 1030 member rows (file, wave, idx, name, agent, report_rel, status, lane_size, fleet_size, flags, last_line).
- `.ufo/waves/round-20/build/GtLaneMado/files.tsv`: 16 per-file rows.

All paths are relative to the mori lane root. These files contain paths and statuses only.
