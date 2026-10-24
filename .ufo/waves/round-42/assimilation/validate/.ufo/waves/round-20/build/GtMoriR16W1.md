# GtMoriR16W1: C2 independent ground truth, mori round-16 wave1 member reports

Scope: `.ufo/waves/round-16/wave1-dispatch.json` (read-only), checked with jq, stat, ls, and read-only reads of lane and fleet records. No oracle or tool run, no builds, no subagents, no writes except this file. Tool installs or updates: none.

Headline: 64/64 member reports are present under the lane (regular, non-symlink, >0 B). 0 empty, 0 missing, 0 misrooted at the same relative path. Every recorded wave1 count is 64 and matches. Two items do not reconcile: (a) the lane's round-16 record counts 2 fleet-root misroots, but fleet evidence shows a third own-lane artifact (`MoriR16.Lesson`); (b) no round-16 `wave1-settlement.json` exists.

## 1. Per-member status (name|status)

`present` = regular non-symlink file at `/home/vgpnk/Projects/shokunin/mori-shokunin/<trailer path>`, size >0 B. The same relative path under `/home/vgpnk/Projects/shokunin/` is absent for all 64 (misrooted: none).

```
WindowTool|present
WindowHarness|present
PackExactAnchor|present
PackKernelUser|present
PackKernelSystem|present
PackUnitOom|present
PackUnitSignal|present
PackProcessSignal|present
PackMissingAnchor|present
PackBootBoundary|present
PackCursorShape|present
PackRecordShape|present
PackMalformedCapture|present
PackProducerFailure|present
PackStderr|present
PackBounds|present
PackTypedFields|present
PackAnchorValidation|present
ContextGuard|present
ReceiptCapture|present
Knowledge|present
SkillRegistry|present
Registry|present
Quality|present
Lesson|present
FrontierIndex|present
Province|present
ClaimRubric|present
CursorDocs|present
SeekDocs|present
FieldDocs|present
SourcePlan|present
RoutedDebt|present
ExistingPredicates|present
LiveSurfaceRecipe|present
GatePatterns|present
DriftDebt|present
SourceCensus|present
SiblingScope|present
WindowAlarmBoundary|present
BootContinuity|present
BudgetPricing|present
HistoricalCorrections|present
SourceChain|present
ReviewCLI|present
ReviewAnchor|present
ReviewCounts|present
ReviewCapture|present
ReviewHarness|present
ReviewFixtures|present
ReviewRegistry|present
ReviewCorpus|present
ReviewLesson|present
ReviewNoHarm|present
AttackMissingCursor|present
AttackMixedBoot|present
AttackOutputLeak|present
AttackBound|present
AttackVacuity|present
AttackClaims|present
AttackPermission|present
AttackPreservation|present
SecretSafety|present
HostSafety|present
```

## 2. Totals

| Quantity | Value | How obtained |
|---|---|---|
| tasks in `taskCall.tasks` | 64 | `jq length`; `counts.total` = 64; `registry.members` = 64 |
| last `Report:` trailers extracted | 64 (64 unique paths) | one exact-match line per task; each path is `.ufo/waves/round-16/build/<name>.md` |
| present (regular, non-symlink, >0 B) | **64** | `stat -c %F` = `regular file` for all 64; sizes 3146 to 31345 B |
| empty (regular, 0 B) | **0** | no `regular empty file` |
| missing under mori-shokunin | **0** | no stat errors |
| symlink / other type | 0 / 0 | `%F` values |
| misrooted: same relative path under fleet root | **0** | 64/64 `No such file or directory` |
| own-lane artifact archived elsewhere in fleet | 1 | `.ufo/waves/hyaku/misroots/MoriR16.Lesson` (see 4.1) |

## 3. Comparison with recorded settlement and closure counts

| Source (read-only) | Recorded | Computed here | Result |
|---|---|---|---|
| mori `LOG.md:1009-1012` | 64 seats; role mix 20 executor / 8 scribe / 10 scout / 6 connector / 10 reviewer / 8 critic / 2 sentinel | 64 tasks; `jq` agent counts identical | match |
| mori `LOG.md:1025` | "All 64 wave1 seats completed" | 64 present | match |
| mori `LOG.md:1105-1109`; `.ufo/waves/round-16/evidence/misroot-sweep.json` | 2 fleet-root misroots relocated (FieldDocs, ReviewLesson), cmp 0, fleet copies deleted; "All 64 reports now reside under the lane" | both present under lane; 0 same-path copies at fleet; 64 under lane | match (2 and 64) |
| mori `SCORECARD.md:997-999` | wave1=64; "All 64 reports are retained after relocating 2 misrooted reports" | 64 present | match |
| fleet `MANIFEST.json` rounds[353] (round 16 mori closure, verdict admitted, closed_at 2026-10-20T13:21:05Z) | "wave1 64 seats, 0 model fields" | 64; dispatch has no model fields | match |
| fleet `MANIFEST.json` rounds[349] (ops wrap-up, closed_at 2026-10-20T09:30:51Z) | closure_debt lists "mori r16" | debt cleared later by rounds[353] | timeline consistent |
| `.ufo/waves/round-16/operator-wrapup.json` | wave1 "dispatched64"; round_total_seats 64 | 64 | match |
| `.ufo/waves/round-16/wave1-record.json` (registry copy) | 64 members | 64; name sets equal; member role equals dispatch agent for 64/64 | match |
| fleet `.ufo/watchdog.log` lines 466 and 473 | launch 2026-10-20 05:44:37-03:00; complete 06:19:40-03:00 | lane-level only | no member count recorded |
| `.ufo/waves/round-16/wave1-task-response.json` | "Spawned 64 background agents"; 64 progress entries | 64 entries, all `pending` at spawn | spawn-time snapshot, not a settlement record |
| `wave*-settlement.json` for round 16 | none exists | mori glob `.ufo/waves/*/*settle*` returns round-17/wave-settlement.json, round-19/wave1-settlement.json, round-19/wave2-settlement.json; fleet glob returns none; round-16 root, build, evidence, frozen, fixtures have none | absent; no file to compare |
| fleet `LOG.md` and `SCORECARD.md` | no mori round-16 wave count | grep for `mori` within 120 chars of r16 / round 16 / wave1 / 64: no matches | none recorded |

## 4. Discrepancies and caveats

4.1 **Misroot count: 2 recorded, 3 in fleet evidence.** The lane record (LOG.md:1105-1109, SCORECARD.md:997-999, misroot-sweep.json) lists two relocated misroots. The fleet closure entry (MANIFEST rounds[353], route item 1) names an "undisclosed fleet-root write MoriR16.Lesson ... archived .ufo/waves/hyaku/misroots/MoriR16.Lesson". That file exists (regular, 847 B) and its first line is a BootContinuity disclosure. The name matches the registry agentId of member `Lesson`. [INFERENCE: attribution rests on name and the closure note; contents were not examined beyond line 1.] The mori LOG and SCORECARD first mention `MoriR16.Lesson` in round 17 (LOG.md:1130, SCORECARD.md:1013), not in the round-16 record. This check cannot count it, because its path is not `.ufo/waves/round-16/build/Lesson.md`. The lane's own `build/Lesson.md` is present (6362 B).

4.2 **No round-16 settlement file.** No `wave1-settlement.json` or other `*settle*` file exists under the mori round-16 root, `build/`, `evidence/`, `frozen/`, or `fixtures/`, or under fleet `.ufo/waves/*/`. The comparison above uses narrative records and `operator-wrapup.json`. Round-17 and round-19 settlement files were not used.

4.3 **`wave1-dispatch.json` was modified after spawn.** Its mtime is 2026-10-21 05:54:19 -0300. The spawn record `wave1-task-response.json` is 2026-10-20 05:48:35 and `wave1-record.json` is 2026-10-20 05:48:56. The same mtime batch covers `wave1-spec.json`, `wave2-spec.json`, and `wave1-context-corrected-not-dispatched.json`. No record I read explains the modification, and no digest of the dispatch file is recorded. Content checks against the spawn record:
- `taskCall.context` (4537 chars) contains no "live-journal" or "live journal" phrase. The corrected fixture has 2 matching strings. This fits LOG.md:1048-1050 ("never historical dispatch").
- Each spawn-time text (`progress[].task`, 1822 to 2117 chars) contains every non-empty line of its dispatch task (64/64). It contains the dispatch task after collapsing newline runs (64/64). It contains its own `Report:` line (64/64).
- Byte-exact containment fails for all 64 at block boundaries. Example, WindowTool at offset 444: dispatch `tool calls.\n\n\nOwn ONLY`, delivered `tool calls.\nOwn ONLY`. [INFERENCE: transport whitespace normalization.]
- The shared-context phrase ("Mori round16 C1 coverage") is absent from all 64 spawn-time texts (0/64). The response does not show how shared context was delivered. [INFERENCE: separate channel.]

Conclusion: the checked content matches what was spawned, apart from whitespace. Byte identity of the whole file is unproven.

4.4 **Presence means existence and size only.** Report content is not judged. The smallest report is 3146 B, so none is a bare placeholder.

4.5 **Two relocated members.** FieldDocs and ReviewLesson were fleet-root misroots at sweep time; the fleet `round-16/build/` was untracked then (`misroot-sweep.json` observed_stdout). They are present under the lane now. Their recorded lane SHA-256 values (`e451a53…`, `e6eaf75…`) were not recomputed, because sha256 is outside the jq/stat/ls set. Fleet `.ufo/waves/round-16/build/` is absent now. Fleet `.ufo/waves/round-16/` holds protocol-lane artifacts (before.md, dispatch.md, gate/, clobber/), which are unrelated to this wave.

4.6 **Model roles.** The spawn record shows modelRole m_swe 20, m_haiku 24, m_opus 10, m_fast 10. These are harness-assigned. The dispatch file has no model fields; its task keys are name, agent, task only. This is consistent with "0 model fields".

## 5. Unobserved or inferred

- [INFERENCE] `MoriR16.Lesson` archive is an own-lane misroot of member `Lesson` (4.1).
- [INFERENCE] Transport whitespace normalization explains the boundary differences (4.3).
- Not observed: the cause of the 2026-10-21 mtime change; the shared-context delivery channel; any SHA-256 values.

## 6. Commands (read-only)

```
jq -r '.taskCall.tasks[] | .task | split("\n") | map(select(startswith("Report: write your scoped findings to "))) | last | sub("^Report: write your scoped findings to "; "")' wave1-dispatch.json | xargs -I{} stat -c '%n|%F|%s' <lane-root>/{}
#   -> 64 x "regular file"
... same with <fleet-root>/{}
#   -> 64 x "No such file or directory"
... | jq -Rs '<classify lines>'
#   -> lane_total 64, present 64, empty 0, missing 0, symlink 0, other 0, min 3146, max 31345
#   -> fleet_missing 64, fleet_present_any 0
stat -c '%n|%F' .ufo .ufo/waves .ufo/waves/round-16 .ufo/waves/round-16/build
#   -> all "directory"
ls -la .ufo/waves/round-16/build
#   -> 65 files: 64 .md + 1 .json (swarm-registry.json, stat-confirmed)
jq on wave1-dispatch.json, wave1-record.json, wave1-task-response.json, operator-wrapup.json, MANIFEST.json rounds[349] and rounds[353]
grep (LOG.md, SCORECARD.md, fleet LOG.md, fleet SCORECARD.md); glob `*settle*` at wave depth
```

For L1 and the oracle: expected present 64, empty 0, missing 0, misrooted-same-path 0. Route to L1: the 2-vs-3 misroot discrepancy (4.1) and the absent round-16 settlement file (4.2).
