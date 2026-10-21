# GtMoriR17W2: C2 independent ground truth, round-17 wave2 (`mori-r17-w2-falsify`)

Seat: MoriR20.GtMoriR17W2 (leaf; no subagents). Manual check with `/usr/bin/jq` (jq-1.8.2) and `stat`/`ls` plus coreutils plumbing. `tools/mori-wave-settlement.py` and `tools/mori-census.sh` were not run. Read-only throughout; the only write is this file.

Dispatch under test: `mori-shokunin/.ufo/waves/round-17/wave2-dispatch.json` (regular file, 92356 B, schema `ufo-swarm-wave-dispatch-v1`).

## Method

1. **Members.** `jq -r '.taskCall.tasks[].name'` gives 64 names; `uniq -d` finds 0 duplicates. Role mix from `.taskCall.tasks[].agent`: reviewer 27, scout 17, connector 4, critic 4, sentinel 2, mutation-tester 4, executor 3, scribe 3 (total 64).
2. **Report path.** For each task, the last line matching `^Report: write your scoped findings to (\S+)$`. Every task has exactly one matching line, and it is the final line (16 of 16). All 64 resolve to `.ufo/waves/round-17/falsify/<name>.md`, with no absolute paths and no `..`. A jq equality check reports `matches=64 of 64`.
3. **Presence (lane root `/home/vgpnk/Projects/shokunin/mori-shokunin`).** `stat -c '%F|%s|%n'` on the 64 paths returns 64 × `regular file`, with no symlinks and no zero-byte files. The components `.ufo`, `.ufo/waves`, `.ufo/waves/round-17` and `.ufo/waves/round-17/falsify` all stat as `directory` (not links). `ls -la .ufo/waves/round-17/falsify/` lists 65 entries: the 64 `.md` reports plus `swarm-registry.json` (9209 B, schema `ufo-swarm-registry-v1`, not a report).
4. **Misrooted (fleet root `/home/vgpnk/Projects/shokunin`).** `stat` on `…/shokunin/.ufo/waves/round-17/falsify/<name>.md` for all 64 returns `No such file or directory`. `ls` on `…/shokunin/.ufo/waves/round-17/falsify/` also reports no such directory. The fleet `round-17/` holds only an empty `w1/`.

## Result

| name | status |
|---|---|
| CaseReview01 | present |
| CaseReview02 | present |
| CaseReview03 | present |
| CaseReview04 | present |
| CaseReview05 | present |
| CaseReview06 | present |
| CaseReview07 | present |
| CaseReview08 | present |
| CaseReview09 | present |
| CaseReview10 | present |
| CaseReview11 | present |
| CaseReview12 | present |
| CaseReview13 | present |
| CaseReview14 | present |
| CaseReview15 | present |
| CaseReview16 | present |
| CaseReview17 | present |
| CaseReview18 | present |
| CaseReview19 | present |
| CaseReview20 | present |
| CaseReview21 | present |
| CaseReview22 | present |
| CaseReview23 | present |
| CaseReview24 | present |
| CaseReview25 | present |
| CaseReview26 | present |
| CaseReview27 | present |
| ReopenRfc6585 | present |
| ReopenRfc9110 | present |
| ReopenZai | present |
| ReopenJjCompat | present |
| ReopenJjAuthor | present |
| ReopenGitAncestor | present |
| ReopenGitSymbolic | present |
| ReopenPacmanLog | present |
| ReceiptInputs | present |
| ReceiptStreams | present |
| ReceiptPins | present |
| ReceiptC2Controls | present |
| ReceiptC3 | present |
| WaveContextHashes | present |
| SourceCensus | present |
| StaleSupersession | present |
| CensusNewBranches | present |
| SeparateThree | present |
| AdjacentOwnership | present |
| TrendGrounding | present |
| PatternConsistency | present |
| CriticC1Final | present |
| CriticC2Final | present |
| CriticC3Final | present |
| CriticOverall | present |
| PrivacyFinal | present |
| SandboxFinal | present |
| MutQuota | present |
| MutBranch | present |
| MutMisroot | present |
| MutContext | present |
| CountC1 | present |
| CountC2 | present |
| CountC3 | present |
| LessonAudit | present |
| ReportTrace | present |
| ConformanceAudit | present |

## Totals

- Members 64 · present **64** · empty **0** · missing **0** · misrooted **0** (0 of 64 relative paths exist under the fleet root) · unsafe **0** · unparsed **0**
- Wave state under the contract rule (every member present): **settled**
- Sizes (lane root, `stat %s`): minimum 4867 B (CaseReview12), maximum 19474 B (LessonAudit). No report is near the 400 B marker bound.

Per-member bytes, in dispatch order:

```
CaseReview01 7146     CaseReview02 8116     CaseReview03 7001     CaseReview04 9391
CaseReview05 8218     CaseReview06 7707     CaseReview07 7255     CaseReview08 6165
CaseReview09 7494     CaseReview10 6671     CaseReview11 5468     CaseReview12 4867
CaseReview13 5619     CaseReview14 6584     CaseReview15 5978     CaseReview16 6393
CaseReview17 6232     CaseReview18 6568     CaseReview19 6039     CaseReview20 7312
CaseReview21 6418     CaseReview22 5879     CaseReview23 8540     CaseReview24 5026
CaseReview25 7534     CaseReview26 6448     CaseReview27 5850     ReopenRfc6585 11666
ReopenRfc9110 8749    ReopenZai 13276       ReopenJjCompat 9780   ReopenJjAuthor 13577
ReopenGitAncestor 13067 ReopenGitSymbolic 15784 ReopenPacmanLog 12463 ReceiptInputs 13900
ReceiptStreams 8101   ReceiptPins 13568     ReceiptC2Controls 15289 ReceiptC3 11789
WaveContextHashes 9883 SourceCensus 9979    StaleSupersession 7722 CensusNewBranches 16383
SeparateThree 13044   AdjacentOwnership 4966 TrendGrounding 14718 PatternConsistency 10942
CriticC1Final 12819   CriticC2Final 10765   CriticC3Final 10536   CriticOverall 10048
PrivacyFinal 16767    SandboxFinal 11574    MutQuota 14213        MutBranch 15346
MutMisroot 11012      MutContext 13825      CountC1 8890          CountC2 5595
CountC3 10555         LessonAudit 19474     ReportTrace 19469     ConformanceAudit 18481
```

## Recorded-count comparison

| Source (read-only) | Recorded for wave2 | Ground truth | Result |
|---|---|---|---|
| `.ufo/waves/round-17/wave-settlement.json` `.waves.wave2` | seats 64, expected_reports 64, present 64, missing [], reported_dead_seats 0; role_mix equals the dispatch role mix | 64 / 0 / 0 | match |
| `LOG.md:1186-1189` (Round-17 fresh falsification landing) | "64/64 falsify reports, 134 unique seats, 0 reported dead, no replacements" | 64 | match |
| `LOG.md:1280-1282` (Round-17 final cleanup) | "Both waves delivered 70/70 and 64/64 reports"; misroot probe "found 0 candidates" | 64; misrooted 0 | match |
| `SCORECARD.md:1061-1062`, `1078-1081` | Qualitative only. Wave2 is named, with no count and "neither is self-certified here" | none recorded | no conflict |
| `MANIFEST.json` `.rounds[372]` (round 17, lane mori, closed_at 2026-10-20T21:51:50Z), `.verification.rechecks` | "134 reports present, 7 full-wave refusal receipts" (both waves combined) | wave2 64 verified here | consistent. Not split per wave. The wave1 share (70) is [INFERENCE]: taken from `wave-settlement.json` and LOG, not re-verified here |
| `wave2-dispatch.json` `.counts` | spawn 64, resume 0, total 64 | 64 tasks | match |
| `falsify/swarm-registry.json` (also copied to `wave2-record.json`) | 64 members, all `kind: spawn`, 0 null `agentId` | 64 | match |
| `wave2-assignments.json` keys | 64 names | identical to dispatch names (`cmp`) | match |
| `wave2-dispatch-attempts.json` and `wave2-task-response.json` | refusals 64, 64, 64, then 0; "Spawned 64 background agents" | 3 falsify job-cap refusals, matching `wave-settlement.json` `falsify_jobcap_refusals: 3` | consistent |

No discrepancy. Ground truth is 64/64 present, and it agrees with every recorded wave2 count.

## Notes for L1

1. The shell's `jq` is a harness builtin (`type -a jq` reports "shell builtin"; `jq --version` prints `jaq 3.1.1`). It was not used. Ground truth came from `/usr/bin/jq` (jq-1.8.2). `~/.local/bin/jq` is also jq-1.8.2.
2. `wave2-record.json` is not a settlement record. Its `path` field is `.ufo/waves/round-17/falsify/swarm-registry.json`, schema `ufo-swarm-registry-v1`, wave `mori-r17-w2-falsify`. Under the contract's discovery rule it would count as `ignored_json`, not as a dispatch.
3. Round 17 has no `wave2-settlement.json`. `wave-settlement.json` covers both waves (`waves.wave1`, `waves.wave2`). `round-19/` has `wave1-settlement.json` and `wave2-settlement.json`. These belong to another round and were not read.
4. The misroot relocations at `LOG.md:1105-1109` and `SCORECARD.md:997-999` (2 reports) concern round 16, not this wave.
5. `LOG.md:1356` ("wave2 retains48 reports") sits in the Round 19 section (starts `LOG.md:1299`) and was not compared.
6. Presence is structural, as the contract defines it. Report contents were not read or validated.

## Tooling

No installs or updates. Used the preinstalled `/usr/bin/jq` 1.8.2 and coreutils (`stat`, `ls`, `xargs`, `sort`, `uniq`, `cmp`, `wc`). Created `/tmp/GtMoriR17W2.*` scratch files and removed them. No pacman, no package operations.

## Unobserved

- The wave1 share of the MANIFEST combined figure (134 = 64 + 70) is [INFERENCE] and was not re-verified here.
- Report content and the wave1 dispatch were not checked. Both are outside this scope.
