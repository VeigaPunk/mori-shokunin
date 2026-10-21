# GtMoriR17W1: round-17 wave1 member-report ground truth (C2, manual)

Scope: `.ufo/waves/round-17/wave1-dispatch.json` → `taskCall.tasks[*]` (70 members), each checked at the relative path from its last `Report:` line, `.ufo/waves/round-17/build/<name>.md`, under `/home/vgpnk/Projects/shokunin/mori-shokunin` (present, empty, missing) and under `/home/vgpnk/Projects/shokunin` (misrooted). Method: `jq` plus `stat`/`ls` only. Read-only. No census tool, no subagents, no git/jj, no installs or updates.

## Verdict

All 70 wave1 member reports are present in mori-shokunin (regular, non-symlink, >0 bytes). Empty 0, missing 0, misrooted 0. This agrees with the recorded wave1 closure counts (70 expected, 70 present, 0 missing, 0 reported dead). Nineteen of the 70 reports have mtimes after the settlement record (see Observations 1).

## Method and raw evidence

1. Names and report lines. `jq -r '.taskCall.tasks | to_entries[] | …'` gives 70 unique names, indices 0–69. Each task's `task` text contains exactly one `Report:` line (`select(test("Report:"))` count = 1 for all 70), so "last" is the only line. Every path ends in `/build/<name>.md` (`n=70, all_name_path_match=true`).
2. Presence. `jq -r '<report paths>' | xargs -d '\n' stat -c '%F|%s|%y|%n'`, cwd mori-shokunin: 70 × `regular file`, sizes 2,735 B (`SrcRfc6585.md`) to 57,543 B (`SeatFixtures.md`). No `symbolic link`, no `regular empty file`, no `No such file` lines.
3. Ancestors: `.ufo`, `.ufo/waves`, `.ufo/waves/round-17`, `.ufo/waves/round-17/build` are all `directory`, not symlinks.
4. Misroot. Same `stat`, cwd `/home/vgpnk/Projects/shokunin`: 70 × `No such file or directory`. The fleet root has `.ufo/waves/round-17/` but no `build/` under it.
5. Cross-check. `/usr/bin/jq` (jq-1.8.2) gives the identical ordered list of 70 report paths (`true`).

## Table (post = mtime after `wave-settlement.json`, 2026-10-20 17:33:57 −03; pre = not after)

| name | status | bytes | misrooted | mtime vs settlement |
|---|---|---:|---|---|
| SeatTool | present | 32903 | no | pre |
| SeatFixtures | present | 57543 | no | pre |
| SeatGate | present | 32641 | no | pre |
| CensusJj | present | 11298 | no | pre |
| JjGate | present | 14772 | no | pre |
| MisrootSweep | present | 19558 | no | pre |
| ContextCheck17 | present | 14206 | no | pre |
| TranscriptShapes | present | 21946 | no | post |
| RetryRecoveryShape | present | 12149 | no | post |
| SeatNaming | present | 21261 | no | post |
| DeadSeatCrossCheck | present | 13700 | no | post |
| WaveRegistryVsReports | present | 21357 | no | pre |
| OmpRetryConfig | present | 9039 | no | post |
| OmpRetryDocs | present | 19620 | no | post |
| CensusGitSites | present | 29566 | no | pre |
| HelperFailureWindows | present | 20442 | no | pre |
| LiveLaneHeadVsBranch | present | 11133 | no | pre |
| CensusConsumers | present | 17621 | no | post |
| PacmanTxnToday | present | 11471 | no | post |
| PacmanActorTrace | present | 8170 | no | post |
| ProvinceFrontier | present | 26981 | no | pre |
| R16LessonM7 | present | 11025 | no | pre |
| MisrootR16Facts | present | 12094 | no | pre |
| FleetRootUntracked | present | 12902 | no | pre |
| SkillRegistry | present | 33265 | no | pre |
| ScorecardAxisCheck | present | 19709 | no | pre |
| SiblingSeatDeathTools | present | 14255 | no | pre |
| JjEnvFacts | present | 11770 | no | post |
| TranscriptTailBounds | present | 9867 | no | post |
| SessionExitCorrelation | present | 8022 | no | post |
| SrcRfc6585 | present | 2735 | no | pre |
| SrcRfc9110 | present | 6162 | no | pre |
| SrcZaiErrorCodes | present | 4276 | no | pre |
| SrcJjGitCompat | present | 6445 | no | pre |
| SrcJjMetaedit | present | 5713 | no | pre |
| SrcGitMergeBase | present | 2874 | no | pre |
| SrcGitSymbolicRef | present | 5033 | no | pre |
| SrcPacmanLog | present | 4521 | no | pre |
| KnowledgeSeatTerminal | present | 10992 | no | pre |
| KnowledgeJjBranch | present | 18997 | no | pre |
| LessonMistakesDraft | present | 7738 | no | pre |
| QualityCriteriaDraft | present | 10936 | no | pre |
| ProvinceNotesDraft | present | 10078 | no | pre |
| OverlapTsukuroi | present | 12903 | no | post |
| OverlapKumitate | present | 7737 | no | pre |
| OverlapAuditLanes | present | 7017 | no | pre |
| OverlapJjSiblings | present | 6153 | no | post |
| ClaimSeparability | present | 5533 | no | pre |
| FrontierLinkage | present | 10167 | no | pre |
| ReviewC1Contract | present | 3584 | no | post |
| ReviewC2Contract | present | 6590 | no | pre |
| ReviewC1Metric | present | 8442 | no | pre |
| ReviewC2Metric | present | 9057 | no | pre |
| ReviewCarryForward | present | 6191 | no | pre |
| ReviewSpotcheckRouting | present | 8339 | no | pre |
| ReviewJjAuditRouting | present | 8334 | no | pre |
| ReviewSeatBreachDetect | present | 17571 | no | post |
| ReviewSchemaDrift | present | 4303 | no | post |
| ReviewExitSemantics | present | 3267 | no | pre |
| ReviewSkillRows | present | 7110 | no | pre |
| ReviewScorecardRubric | present | 5725 | no | pre |
| CriticC1 | present | 15046 | no | post |
| CriticC2 | present | 14565 | no | pre |
| CriticFrontier | present | 14072 | no | pre |
| CriticHarm | present | 17693 | no | pre |
| SentinelTranscripts | present | 15410 | no | pre |
| SentinelJjSandbox | present | 21921 | no | post |
| RevengerCensusHead | present | 7619 | no | pre |
| RevengerContextChecker | present | 8516 | no | pre |
| RevengerOmpTerminal | present | 5946 | no | pre |

## Totals

- Members 70. Unique names 70. Unique report paths 70. Report lines per task 1.
- present 70. empty 0. missing 0. symlink 0. other non-regular 0.
- misrooted 0 of 70 (fleet `.ufo/waves/round-17/build/` does not exist).
- mtime post-settlement 19. pre 51.
- `build/` holds 71 entries: 70 members plus 1 non-member, `swarm-registry.json` (10,417 B, mode 0600, 2026-10-20 15:54).

## Comparison with recorded closure counts (wave1 only)

| source | recorded | ground truth here | verdict |
|---|---|---|---|
| `wave-settlement.json` `.waves.wave1` | seats 70; expected_reports 70; present 70; missing []; reported_dead_seats 0 | 70 present, 0 missing, 0 dead by report basis | match |
| `wave-settlement.json` `.waves.wave1.role_mix` | executor 7, scout 23, scribe 13, connector 6, reviewer 12, critic 4, sentinel 2, revenger 3 | identical counts from dispatch `.agent` | match |
| `wave1-dispatch.json` `.counts` | spawn 70, resume 0, total 70 | 70 tasks; `resumeSends` = [] | match |
| `wave1-record.json` `.members` | 70 entries, kind spawn | same 70 names as dispatch (set-equal) | match |
| `wave1-task-response.json` | attempts 5; spawned_at 2026-10-20T15:52:53 −03 | LOG.md:1135–1136 "five attempts total, final dispatch at15:52:53−03" | match |
| LOG.md:1135 | validated 70 seats after four all-70 job-cap refusals | settlement `build_jobcap_refusals: 4` | match |
| LOG.md:1187–1189 | "settled:70/70 build and64/64 falsify reports,134 unique seats,0 reported dead, no replacements" | wave1 70/70 present | match (wave1 part; wave2 not checked here) |
| LOG.md:1282–1283 | "Both waves delivered 70/70 and 64/64 reports … 0 reported dead" | same | match |
| SCORECARD.md:1125–1126 | "all 134 reports delivered, 0 reported dead, no replacements" | 70 of the 134 | consistent; combined figure only |
| MANIFEST.json `rounds[]` with round 17 and lane "mori" (closed_at 2026-10-20T21:51:50Z), `verification.rechecks` | "134 reports present, 7 full-wave refusal receipts" | combined; refusals 4+3 = 7 per settlement | consistent; combined figure only |

MANIFEST has 14 round-17 entries across lanes. Only the lane "mori" entry is this wave's closure.

## Observations

1. Post-settlement mtimes (19 members). [INFERENCE] These look like batch writes, not single-seat output:
   - 7 files at 2026-10-21 03:21:03.893–.895 (TranscriptShapes, TranscriptTailBounds, OverlapTsukuroi, ReviewC1Contract, ReviewSeatBreachDetect, ReviewSchemaDrift, CriticC1). This is the same millisecond window as `wave1-dispatch.json` (03:21:03.895).
   - 2 at 03:26:22 (CensusConsumers, OverlapJjSiblings). 3 at 03:49:29 (DeadSeatCrossCheck, OmpRetryDocs, PacmanTxnToday). 3 at 03:51:11–03:51:26 (OmpRetryConfig, PacmanActorTrace, SessionExitCorrelation).
   - Singles: RetryRecoveryShape 03:30:02, SentinelJjSandbox 03:36:57, SeatNaming 04:05:48, JjEnvFacts 05:58:59.
   Presence is unaffected. No baseline hash exists, so content change is unverified. The settlement cannot attest to the current bytes of these 19 files. The 51 pre files were last written before the settlement record.
2. Registry vs record. `wave1-dispatch.json` was modified after settlement (2026-10-21 03:21:03). Its `registry.members` have `agentId: null` for 70 of 70. `wave1-record.json` has non-null `agentId` for 70 of 70. The name sets are identical. [INFERENCE] The registry was rewritten in the same post-settlement pass. Not verified.
3. Settlement wording vs dispatch. The settlement's top-level `resumed_writers` ("Original identities on new isolated base5c1dfb8 clones; no replacement/extra seats") does not reconcile with dispatch `counts.resume` = 0 and `resumeSends` = []. [INFERENCE] The note describes clone identity, not dispatch resumes.
4. Fleet root. `/home/vgpnk/Projects/shokunin/.ufo/waves/round-17/` contains only an empty `w1/` (0 entries, mtime 2026-10-20 12:27:49 −03). The round directory's own mtime is 15:56. No member-named file exists under the fleet root. Not misrooted.
5. Closure report placement. MANIFEST's mori round-17 `report` (`.ufo/reports/round-17/mori.md`) exists only under the fleet root (15,926 B, mtime 2026-10-20 18:16:10 −03). `mori-shokunin/.ufo/reports/` holds rounds 2–11 only. Not a member report; noted for placement.

## Tooling

- The bash tool's `jq` is a shell builtin reporting `jaq 3.1.1`. `/usr/bin/jq` and `~/.local/bin/jq` report `jq-1.8.2`. The ordered path lists match across the two builds (`true`).
- Installs or updates: none. pacman not used.

## Bounds

- No census tool run. No subagents. No git/jj commands. No transcript or ~/.omp log opened. The only write is this file.
- Wave2 checked only through the combined closure figures.
- "Present" means regular, non-symlink, >0 bytes. Report content completeness is not assessed.
- No checks requested of L1. The commands above reproduce the table.
