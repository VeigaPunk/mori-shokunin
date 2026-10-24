# GtMoriR18W1 — C2 independent ground truth: mori round-18 wave1-dispatch member census

Date: 2026-10-21. Scope: manual, no settlement tool. Derivation used **jq + stat only** (both preexisting on host; no tools installed/updated). Read-only; no bounds crossed.

## Source

- Dispatch: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-18/wave1-dispatch.json` (regular file, 135847 bytes). Top-level keys: `compaction,counts,note,policy,registry,resumeSends,schema,taskCall,wave`; `taskCall.tasks` length = **68**; task fields `agent,name,task`.
- Dispatch self-declared counts: `.counts` = `{"spawn":68,"resume":0,"total":68}`; `.wave` = `mori-r18-w1-build`.
- Extraction: for each task, last line matching `Report: write your scoped findings to ` (jq `split("\n") | map(select(test(...))) | last`). All 68 tasks carry the trailer (0 without); all 68 extracted paths start with `.ufo/waves/round-18/build/` (68/68).
- Presence: `stat`/test at `/home/vgpnk/Projects/shokunin/mori-shokunin/<rel>`; `present` = regular non-symlink file with size >0. Misroot = same relative path exists under `/home/vgpnk/Projects/shokunin/<rel>` (file or symlink).

## Table (name | status | bytes | misrooted-under-root)

| Name | Status | Bytes | Misrooted |
|---|---|---:|---|
| RetentionGate | present | 4021 | no |
| FreezeOrder | present | 3193 | no |
| DispatchLedger | present | 3834 | no |
| AdjRound2Evidence | present | 10179 | no |
| AdjR16AttackPermission | present | 4834 | no |
| AdjCriticC1 | present | 5979 | no |
| AdjDeadSeatCrossCheck | missing | - | no |
| AdjOmpRetryDocs | missing | - | no |
| AdjDocumentRefs | present | 5915 | no |
| AdjRetryRecoveryShape | missing | - | no |
| AdjReviewC1Schema | present | 5921 | no |
| AdjSeatBreachDetect | missing | - | no |
| AdjSeatNaming | missing | - | no |
| AdjSentinelTranscripts | present | 5728 | no |
| AdjTranscriptShapes | present | 7434 | no |
| AdjTranscriptTailBounds | missing | - | no |
| AdjSeatLiveEvidence | missing | - | no |
| AdjConformanceAudit | present | 7708 | no |
| AdjWave1SpecDispatch | missing | - | no |
| AdjLesson17 | present | 3049 | no |
| RedactPacmanActorTrace | present | 3633 | no |
| RedactOmpRetryConfig | present | 4578 | no |
| RedactSessionExitCorrelation | present | 5515 | no |
| SweepR17Build1 | missing | - | no |
| SweepR17Build2 | present | 8717 | no |
| SweepR17Build3 | present | 14366 | no |
| SweepR17Build4 | present | 7474 | no |
| SweepR17Build5 | present | 10421 | no |
| SweepR17Build6 | present | 8196 | no |
| SweepR17Build7 | present | 13347 | no |
| SweepR17Falsify1 | missing | - | no |
| SweepR17Falsify2 | present | 13386 | no |
| SweepR17Falsify3 | missing | - | no |
| SweepR17Falsify4 | present | 9105 | no |
| SweepR16Md1 | missing | - | no |
| SweepR16Md2 | present | 2109 | no |
| SweepR15Md1 | missing | - | no |
| SweepR15Md2 | present | 9312 | no |
| SweepR1314Md | missing | - | no |
| SweepR17EvidenceJson | present | 7640 | no |
| SweepR17CorpusText | present | 5821 | no |
| SrcOwaspLogging | present | 7990 | no |
| SrcNist800122 | present | 8228 | no |
| SrcOtelSensitiveData | present | 8786 | no |
| SrcGdprArt5 | present | 8277 | no |
| SrcNosekPrereg | present | 10031 | no |
| SrcGitRevList | present | 13066 | no |
| SrcSlsaProvenance | present | 9609 | no |
| SrcRfc8785 | present | 12364 | no |
| RevFreezeR17C1 | present | 5943 | no |
| RevFreezeR17C2 | present | 7653 | no |
| RevFreezeR17C3 | present | 7616 | no |
| ScoutFreezeLabels | present | 15939 | no |
| ReviewRegisterOracle | present | 8564 | no |
| ScoutAttemptReceipts | missing | - | no |
| CriticC1Metric | present | 7757 | no |
| CriticC2Calibration | present | 6550 | no |
| CriticC3Operability | present | 7426 | no |
| CriticSeparability | present | 7451 | no |
| SentinelPrivacyDesign | present | 9382 | no |
| SentinelContextAudit | present | 6716 | no |
| ConnectKagiExposure | present | 6194 | no |
| ConnectKumitateDispatch | present | 7168 | no |
| ConnectFleetPrivacyRulings | present | 10299 | no |
| ScribeLessonDraft | present | 17423 | no |
| ScribeKnowledgeMinimization | present | 10128 | no |
| ReviewRoutedDefects | present | 12624 | no |
| ScoutProvinceRegistry | present | 7393 | no |

## Totals

| Status | Count |
|---|---:|
| present | 53 |
| missing | 15 |
| empty | 0 |
| symlink / directory / no-trailer | 0 |
| **total tasks** | **68** |
| misrooted (path exists under `/home/vgpnk/Projects/shokunin`) | **0** |

53 + 15 = 68 ✓. Misroot check: `/home/vgpnk/Projects/shokunin/.ufo` exists (directory) but `/home/vgpnk/Projects/shokunin/.ufo/waves/round-18/build` does not exist (stat: "No such file or directory"), and none of the 68 relative paths resolve under the root.

## Settlement / closure cross-check (all read-only)

| Record | Count recorded | Agreement |
|---|---|---|
| `wave*-settlement.json` for round-18 | **none exists** (`stat` on `.ufo/waves/round-18/{wave1,wave2}-settlement.json` → No such file; settlement files first appear in round-19) | nothing to compare |
| `/home/vgpnk/Projects/shokunin/MANIFEST.json` mori round-18 closure row, `notes` (MANIFEST.json:9486) | "W1 **68** seats with **15** provider-capacity deaths (resumed once each, no replacements), w2 67 seats, total 135" | exact match: 68 seats, 15 no-report → 53 reports |
| `SCORECARD.md:1134` (Round 18 section) | "Waves: w1 **68** seats (**15** dead on provider capacity), w2 67 seats (0 dead); round total 135" | exact match |
| `LOG.md:1289-1297` (Round 18 section) | no wave member/report counts recorded (C1/C2/C3 metrics only) | no contradiction |
| `.ufo/waves/round-18/wave1-attempts.json` | attempt 1, `tasks_count` 68, `started_ids` 68, result "started" | matches dispatch `.counts` {spawn:68,total:68} |
| `.ufo/waves/round-18/evidence/wave1-dead-seats.json` | `seats` list of **15** (provider-capacity class `turn_rate_limit_exceeded`, one same-identity resume each; alias/time withheld by r19 minimization) | **set-identical** to my 15 filesystem-missing names (sorted lists equal) |

## Verdict

Independent ground truth **agrees** with every recorded settlement/closure count found: 68 dispatched wave-1 seats, 53 reports present (>0 bytes, regular files), 15 missing, 0 empty, 0 misrooted. The 15 missing are exactly the recorded provider-capacity dead seats (`evidence/wave1-dead-seats.json`), and MANIFEST/SCORECARD both record 68/15 for wave 1. No discrepancy found.

Misattribution guards (naive greps that could mislead):
- `SCORECARD.md:~996` "Operator wrap-up: wave1=64 … relocating 2 misrooted reports" belongs to **Round 16**, not round 18.
- `MANIFEST.json:10171` "W1 64 returned IDs, 16 reports, 8 known provider failures…" belongs to mori **round 19**, not round 18.

## Commands (evidence)

- `jq -r '.taskCall.tasks[] | .name as $n | ((.task // "") | split("\n") | map(select(test("Report: write your scoped findings to"))) | last | sub("^.*Report: write your scoped findings to "; ""))' wave1-dispatch.json` → 68 paths (all `.ufo/waves/round-18/build/<Name>.md`).
- Per path: `[ -L ]` → symlink; `[ -f ]` + `stat -c %s` → present(>0)/empty(0); `[ -d ]` → directory; else missing; same test at `/home/vgpnk/Projects/shokunin/<rel>` → misrooted.
- Aggregate rerun: `TOTAL=68 missing=15 present=53 misrooted=0` (awk over the same pipeline).
- `stat -c '%n %F %s'` on dispatch (135847), wave1-attempts.json (450), evidence/wave1-dead-seats.json (1002); wave1/wave2-settlement.json absent.

No tool installs or updates were needed or performed. Unobserved: nothing material; provider alias/error payload in `wave1-dead-seats.json` is deliberately withheld upstream (not needed for counts).
