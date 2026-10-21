# GtMoriR18W2: C2 independent ground truth, round-18 wave 2

**Scope.** Wave `mori-r18-w2-falsify`, dispatch `.ufo/waves/round-18/wave2-dispatch.json`, lane root `/home/vgpnk/Projects/shokunin/mori-shokunin`, fleet root `/home/vgpnk/Projects/shokunin`. Manual check per assignment: counts computed with `jq` and `stat` only (`xargs` used as pipe plumbing). Notes were located with `glob`/`grep` and read with `read`, all read-only. No `tools/mori-wave-settlement.py`, no census run, no build, lint, git or jj command, no subagent. The only file written is this report.

**Result.** Wave state **settled**: 67 of 67 members have a non-empty regular report file.

Totals: **present 67 · empty 0 · missing 0 · misrooted 0 · unsafe 0 · unparsed 0 · total 67.**

## Table (name|status)

```
MutRetentionGate|present
ReviewRetentionGateCode|present
RecountPopulation|present
AttackMinPacmanActorTrace|present
AttackMinOmpRetryConfig|present
AttackMinSessionExit|present
AttackTokRound2Json|present
AttackTokR16AttackPermission|present
AttackTokCriticC1|present
AttackTokDeadSeatCrossCheck|present
AttackTokOmpRetryDocs|present
AttackTokPackageRefs|present
AttackTokRetryRecoveryShape|present
AttackTokReviewC1Schema|present
AttackTokSeatBreachDetect|present
AttackTokSeatNaming|present
AttackTokTranscriptShapes|present
AttackTokTailBounds|present
AttackTokSeatLive|present
AttackTokConformanceAudit|present
AttackTokR17Wave1Spec|present
AttackTokIdentityEdits|present
SentinelHashRisk|present
ResweepR13|present
ResweepR14|present
ResweepR15|present
ResweepR16|present
ResweepR17|present
ResweepCorpusRoot|present
ResweepRound18|present
CriticC1Admission|present
CriticTriageRule|present
MutFreezeOrder|present
ReviewFreezeOrderCode|present
RevFreezeR18|present
CriticCorrectionRow|present
MutDispatchLedger|present
ReviewDispatchLedgerCode|present
RecomputePayloadDigest|present
CriticC3Scoring|present
SentinelLedgerPrivacy|present
ReopenOwaspAsvs|present
ReopenNist|present
ReopenOtel|present
ReopenGdprStrac|present
ReopenNosekWagenmakers|present
ReopenGitDocs|present
ReopenSlsaProGit|present
ReopenRfc8785PyJson|present
ReviewKnowMinimization|present
ReviewKnowFreezeOrder|present
ReviewKnowDispatchLedger|present
ReviewQuality51to55|present
ReviewRegistryRows|present
ReviewProvinceNotes|present
ReviewSourcesRows|present
ConnectTsukuroiPackage|present
PreservationCheck|present
ConformanceAuditR18|present
AuditMisrootsScratch|present
AuditDeadSeats|present
CriticTrendVerdicts|present
CriticLowestAxis|present
ReviewRoutedDisposition|present
SentinelContextWave2|present
ReviewOutOfMetricRegister|present
CriticSeparabilityW2|present
```

Each report path is `.ufo/waves/round-18/falsify/<name>.md`, relative to the lane root.

## Totals

| status | count |
|---|---:|
| present | 67 |
| empty | 0 |
| missing | 0 |
| misrooted | 0 |
| unsafe | 0 |
| unparsed | 0 |
| total | 67 |

Expected output for any settlement tool on this wave: state `settled`, present 67, missing none, misrooted 0.

## Method and evidence

1. **Members.** `jq '.taskCall.tasks | length'` gives 67. `.counts` is `{"spawn":67,"resume":0,"total":67}`. `.compaction.applied` is `false`, so the task text is as dispatched.
2. **Trailer.** Each task has exactly one line matching `^Report: write your scoped findings to (\S+)$`. That line is the last non-blank line in all 67 tasks, and no task text contains CR. Every path is relative, with no leading `/` and no `..`. The basename equals `<name>.md` for 67 of 67. Names are unique (67) and paths are unique (67).
3. **Presence.** Each path was stat'd under the lane root and under the fleet root:
   `jq -r '<extract path per task, emit lane and fleet absolute paths>' .ufo/waves/round-18/wave2-dispatch.json | xargs stat -c '{"type":"%F","size":%s,"mtime":%Y,"path":"%n"}' 2>/dev/null | jq -s --slurpfile d .ufo/waves/round-18/wave2-dispatch.json '<join by path>'`
   Rules: present = lane `regular file` with size > 0; empty = lane regular with size 0; missing = no lane stat; misrooted = missing and the fleet path is a regular file.
   Result: all 67 are `regular file`. None is `symbolic link` or empty. Sizes range from 2716 B (`AttackTokDeadSeatCrossCheck.md`) to 24776 B (`ReviewRoutedDisposition.md`). Lane mtimes run from 2026-10-21T06:38:33Z to 2026-10-21T07:06:12Z.
4. **Ancestors.** `.`, `.ufo`, `.ufo/waves`, `.ufo/waves/round-18` and `.ufo/waves/round-18/falsify` are all `directory`, so no symlink lies on the path.
5. **Misrooting.** `/home/vgpnk/Projects/shokunin/.ufo/waves/round-18` does not exist (`stat`: No such file or directory). None of the 67 relative paths exists under the fleet root, so misrooted = 0.
6. **Tool identities.** `jq --version` is `jaq 3.1.1`. `stat --version` is `stat 0.8.0`, not GNU coreutils. `ls` is a shell builtin with elided output; no count depends on it. `stat -c %F /bin` returns `symbolic link`, which confirms the link test. No tool was installed or updated.

## Recorded counts for round-18 wave 2 compared with the independent result

| Source | Recorded for wave 2 | Independent result | Verdict |
|---|---|---|---|
| `wave2-dispatch.json` `.counts` | spawn 67, resume 0, total 67 | 67 members | match |
| `falsify/swarm-registry.json` (createdAt 06:28:44Z, updatedAt 06:36:18Z) | 67 members; names and roles equal the tasks; agentId set on 67 (`MoriR18Recovery.<name>-2`) | 67 names and roles identical | match |
| `wave2-attempts.json` | attempt 1 at 03:32:51 -03:00 refused, started_ids 0; attempt 2 at 03:36:07 -03:00 started, started_ids 67, tasks_count 67 | 67 present | match; attempt 1 started no seats |
| `SCORECARD.md:1135` | `w2 67 seats (0 dead)` | 67 present, 0 missing | match |
| `MANIFEST.json` `rounds[386]` notes (mori closure, closed_at 2026-10-21T07:34:23Z) | `w2 67 seats` | 67 | match |
| `MANIFEST.json` `rounds[386]` capabilities and verification (`MANIFEST.json:9475`) | `w2 2/2 bound clean` (C3 dispatch-attempt ledger) | 2 attempt records; per-seat reports 67 | different unit; not a retention count |
| `LOG.md:1289-1297` (round-18 section) | no wave-2 count | none | none recorded |
| `wave*-settlement.json` for round 18 | none exists. The glob `.ufo/waves/**/*settlement*` found only round-17 `wave-settlement.json`, round-19 `wave1-settlement.json` and `wave2-settlement.json`, and round-20 build tools | none | none recorded |
| Retained-report count for wave 2 | not recorded in any named source | 67 | gap |

Not comparable: `LOG.md:1354-1356` ("wave2 retains48 reports and22 provider failures") is round 19. Its section header is at `LOG.md:1299`. It is not round-18 wave 2.

Corroboration outside the named list (`wave2-task-response.txt`, not a settlement record): attempt 1 reports `Background job limit reached (100)`, and attempt 2 reports `Spawned 67 background agents`, with IDs ending in `-2`.

## Findings

1. **Gap in the closure record.** `SCORECARD.md:1135` and `MANIFEST.json` `rounds[386]` record seat counts and deaths, not a retained-report count for wave 2. Another round-18 closure does record one: kaidoku `rounds[363]` gives "W2 98 (94 reports...)". The mori closure does not, and that is the gap C2 is meant to close.
2. **The two registries disagree on agent identity.** The dispatch's own `registry.members` has `agentId: null` for 0 of 67 members. `swarm-registry.json` has an ID for 67 of 67. A check that binds seat to report must read the swarm registry.
3. **Timeline is consistent.** Attempt 2 started at 06:36:07Z. The swarm registry was last updated at 06:36:18Z. The reports were written between 06:38:33Z and 07:06:12Z. Closure was recorded at 07:34:23Z. [INFERENCE] The 67 files were written by the attempt-2 seats. mtime alone does not prove authorship.
4. **Empty branch unexercised.** No wave-2 member is empty, so this tree does not exercise the empty classification.
5. **Out-of-scope reference, wave 1.** Wave 1 is `mori-r18-w1-build` with 68 members and reports under `.ufo/waves/round-18/build/`. The same stat method gives 53 present and 15 missing. `SCORECARD.md:1135` records "15 dead on provider capacity". The counts match. I did not match names to seats, so that correspondence is [INFERENCE].

## Reproduction

Run from `/home/vgpnk/Projects/shokunin/mori-shokunin`. Expect `present=67` with the table above. Missing members are those with no lane stat. Misrooted members are those whose fleet path is a regular file.
