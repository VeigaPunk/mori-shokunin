# RevR18Dead: dead-seat vs. report-presence calibration, mori round 18 wave 1

Seat: MoriR20.RevR18Dead (leaf, read-only). Times are UTC-3, 2026-10-21, unless noted. Paths are lane-relative (`mori-shokunin/...`).

## Verdict

1. **2x2 at wave end:** dead with report **0**; dead without report **15**; alive with report **53**; alive without report **0**. Missing report and the record's dead list coincide exactly.
2. **That coincidence does not confirm the 15 deaths.** The only death evidence is one narrative record, `evidence/wave1-dead-seats.json`. Its alias, error payload, observation time and resume time are withheld (lines 2, 4), and the file was rewritten in place at 05:23:31. Every other readable record either shows no per-seat failure or leaves the error class unverified.
3. **"Missing report is not a dead seat" holds in the timeline.** At the first committed snapshot of the death record (03:22:18), report absence marked 16 seats missing, and one of them (ScoutFreezeLabels) was alive. At the audit time (03:41:08) it marked 18, and three of them (RedactOmpRetryConfig, RedactPacmanActorTrace, RedactSessionExitCorrelation) were alive and wrote their reports at 03:51:36. This supports the frozen rule at `round-20/contract.md:80-81`.
4. **Label the 15 "unreported at wave end; death unverified"** until per-seat terminal evidence is attached.

## 1. 2x2 table (final state)

Denominator: 68 dispatched members. `wave1-dispatch.json` `registry.members` (lines 25-434) and `taskCall.tasks` (lines 446-787) name the same 68 unique seats. The dead set is `evidence/wave1-dead-seats.json` `seats` (lines 6-22): 15 unique names, all within the 68. Report presence means the file named by each task's `Report:` trailer, `.ufo/waves/round-18/build/<name>.md`, exists in the lane.

| | report present | report absent |
|---|---|---|
| **dead (record)** | **0** | **15**, listed below |
| **alive (not in record)** | **53**, listed below | **0** |

Dead, report absent (15): AdjDeadSeatCrossCheck, AdjOmpRetryDocs, AdjRetryRecoveryShape, AdjSeatBreachDetect, AdjSeatLiveEvidence, AdjSeatNaming, AdjTranscriptTailBounds, AdjWave1SpecDispatch, ScoutAttemptReceipts, SweepR1314Md, SweepR15Md1, SweepR16Md1, SweepR17Build1, SweepR17Falsify1, SweepR17Falsify3.

Alive, report present (53): AdjConformanceAudit, AdjCriticC1, AdjDocumentRefs, AdjLesson17, AdjR16AttackPermission, AdjReviewC1Schema, AdjRound2Evidence, AdjSentinelTranscripts, AdjTranscriptShapes, ConnectFleetPrivacyRulings, ConnectKagiExposure, ConnectKumitateDispatch, CriticC1Metric, CriticC2Calibration, CriticC3Operability, CriticSeparability, DispatchLedger, FreezeOrder, RedactOmpRetryConfig, RedactPacmanActorTrace, RedactSessionExitCorrelation, RetentionGate, RevFreezeR17C1, RevFreezeR17C2, RevFreezeR17C3, ReviewRegisterOracle, ReviewRoutedDefects, ScoutFreezeLabels, ScoutProvinceRegistry, ScribeKnowledgeMinimization, ScribeLessonDraft, SentinelContextAudit, SentinelPrivacyDesign, SrcGdprArt5, SrcGitRevList, SrcNist800122, SrcNosekPrereg, SrcOtelSensitiveData, SrcOwaspLogging, SrcRfc8785, SrcSlsaProvenance, SweepR15Md2, SweepR16Md2, SweepR17Build2, SweepR17Build3, SweepR17Build4, SweepR17Build5, SweepR17Build6, SweepR17Build7, SweepR17CorpusText, SweepR17EvidenceJson, SweepR17Falsify2, SweepR17Falsify4.

Checks on the files:
- **53 present:** regular files, not symlinks, non-empty (2,109 to 17,423 bytes; median 7,653). Modification times run 03:02:43 to 03:51:36, all after the 03:01:44 attempt. None contains a `STATUS:` line. No fleet-root twin exists for any of the 68 (misroot: none).
- **15 absent:** no file in the lane's round-18 tree has a basename containing any of the 15 names, and there is no `.ufo/worktrees/round-18/<name>` directory. Outside the dispatch, registry and dead-record files, the names appear only in spec, plan, assignment, triage, audit and task-response files. None of those is a report. No fleet-root match.
- Round-18 task text required no `STATUS: started` first-write stub (0 of 68 tasks), so a seat's first observable output was its final report. `round-18/contract.md:5-7` says attempt 1 left no lane files and no seats, so every report under `build/` comes from this dispatch.

## 2. Time-sliced view

| Snapshot (UTC-3) | Evidence | Dead, no report | Alive, no report | Alive seats without report |
|---|---|---|---|---|
| 03:22:18 | git commit `b8f5c6c3` (also `ab9e22c5`), which integrates wave-1 reports and first contains the pre-minimization death record | 15 | 1 | ScoutFreezeLabels (its file is written 03:25:17) |
| 03:41:08 | `falsify/AuditDeadSeats.md` mtime; it cites the same record hash | 15 | 3 | RedactOmpRetryConfig, RedactPacmanActorTrace, RedactSessionExitCorrelation (written 03:51:36) |
| 04:06:30 | git commit `9db51685` | 15 | 0 | none |
| end (listing now) | `build/` | 15 | 0 | none |

Modification-time counts (1-second resolution, not git-verified): alive seats without a report at 03:05:00, 42; at 03:10:00, 22; at 03:13:30, 12; at 03:20:00, 5. Absence-only labelling at snapshots before 03:20 would have marked 20 to 57 seats dead.

## 3. The death record: what supports it, and what does not

Supports the labels (readable):
- `evidence/wave1-dead-seats.json` names the 15 seats, an error class of provider capacity / rate limit (`turn_rate_limit_exceeded`, line 2), one same-identity resume message each (line 3), and disposition "dead; not replaced" (line 23).
- Its pre-minimization blob hash (`0c7c2da4...`, line 5) is first committed at 03:22:18. The audit cites the same hash.

Does not support the labels, or cannot be checked:
1. **Withheld fields.** Alias, error payload and observation time are withheld (line 2), and `resumed_at` is withheld (line 4). The file was rewritten in place at 05:23:31 (current SHA-256 `83e92c90...`), and the minimized version was committed at 05:47:35 (`367927c5`). The un-minimized version remains in git history (`b8f5c6c3` and `ab9e22c5` at 03:22:18, `9db51685` and `c60f8d19` at 04:06:30). I hashed it and did not open it. Whether to read it is an L1 and privacy decision.
2. **`wave1-attempts.json` does not record the deaths**, contrary to the brief. It has one row: attempt 1, `result` "started", `started_ids` 68 (lines 11, 13). It has no failure, retry or resume entries.
3. **`evidence/c3-after-wave1-attempts.json`** (04:07:25): status `clean`, one row, one bound, no resume rows. It binds dispatch attempts and carries no per-seat terminal status.
4. **`build/swarm-registry.json`** holds 68 entries with `kind`, `role`, `agentId` and `item` only. It has no status field, and `updatedAt` is 03:01:55, unchanged since spawn.
5. **`wave1-dispatch.json`**: `counts.resume` is 0 (line 18) and `resumeSends` is empty (line 789). The file was written at 02:59:33, before attempt 1, so it cannot evidence the resume messages the record describes.
6. **`falsify/AuditDeadSeats.md`** (03:41:08) checked report absence for the 15 only (line 7). It did not test the 53 for presence. Its error-class comparison is "Unverified" for all 15 (lines 8, 12-26), and it reports that the last-line selector returned a non-error line. I opened no transcript, so I can neither confirm nor refute that.

Conclusion: no readable record independently shows that any of the 15 died. They are unreported at wave end, and their death label rests on the withheld record.

## 4. Role split (observational; cause is an inference)

| Role | Seats | Dead |
|---|---|---|
| scout | 21 | 7 |
| reviewer | 19 | 8 |
| scribe, critic, executor, revenger, sentinel, connector | 28 | 0 |

The exact one-sided hypergeometric probability that all 15 deaths fall among the 40 scout and reviewer seats by chance is 9.1e-5. The partition was chosen after seeing the dead list and is not corrected for other partitions.

[INFERENCE] The role dependence points to a route-level cause, such as a model or provider route shared by scouts and reviewers, rather than independent per-seat failure. The alias that would confirm this is withheld in the record, and I did not open OMP configuration.

## 5. Expected C2 output for this dispatch (derived by me, not tool output)

`wave1-dispatch.json` has schema `ufo-swarm-wave-dispatch-v1` (line 2) and a non-null `taskCall`, so a C2 scan discovers it. Applying the trailer rule at `round-20/contract.md:70-73` (`Report:` as the last line of a task; 68 of 68 parse, each equal to `build/<name>.md`):
- members 68; present 53; missing 15 (the list in section 1); empty 0; unsafe 0; unparsed 0; misrooted 0
- wave state `partial`
- the tool must not label the 15 `dead`, `failed` or `killed` (`contract.md:80-81`)

## 6. Method and bounds

- **Read:** the round-18 dispatch, attempts, dead-record, registry, task response, C3 check and audit; spec, plan, assignment and triage files (name occurrences only); the `build/` listing; `round-20/contract.md` lines 44-103; the `round-18/contract.md` header.
- **Git, read-only:** `git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --all --format='%H %cI %s' -- <three record paths>` (exit 0), and `git show <rev>:<path>` plus `git ls-tree -r --name-only <rev> -- .ufo/waves/round-18/build/` run from Python with `GIT_OPTIONAL_LOCKS=0`. Only hashes and file names were kept. No mutating git or jj command was run.
- **Fleet root:** existence checks and a filename-only walk of `.ufo`, read-only.
- **Not opened:** any transcript (`history://`, `agent://`), `~/.omp` (sessions or configuration), or the content of the un-minimized record. No agent or session identifiers were printed; registry `agentId` values were only counted.
- **Computation:** Python standard library in the eval kernel. The alive list was typed by hand and checked against the computed set (53 match; 53 + 15 = 68).
- **Installs or updates:** none. **Builds, tests, linters, census:** none run. **Writes:** this report only.

## 7. Confidence and open items

- **High:** the 2x2 counts and names; file presence and finality; the timeline (git commit times and modification times); the contents of the attempts, registry, dispatch and C3 files.
- **Medium:** "missing is not dead." The time slices confirm it, but this is not a formal test.
- **Low or unverifiable:** whether any of the 15 died. Live agent status was not checked, because transcript-adjacent reads are outside this seat's bounds. The L1 can check runtime status directly.
- **For L1:**
  - (a) label the 15 "unreported, death unverified" in closure;
  - (b) if per-seat terminal evidence is needed, obtain status-only fields from a non-author under the round-18 privacy rule, or record runtime status in the ledger;
  - (c) decide whether to read the pre-minimization blob;
  - (d) use the C2 `partial` and `missing` states, never `dead`.
