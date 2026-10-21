# GtMoriR14 — C2 independent ground truth: mori round-14 wave member reports

Seat: MoriR20.GtMoriR14 (leaf scout, no subagents). Date: 2026-10-21. Manual, no settlement tooling; `jq` + `ls`/`stat` only. No tools installed (none needed). All paths read-only.

## Target

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-14/dispatch.json` (51,551 B, mtime Oct 20 02:54).

- Task count: `jq '.taskCall.tasks | length'` → **32**.
- Every task has ≥1 `Report: write your scoped findings to …` line (select-with-none check → `[]`); the **last** such line per task was extracted (`split("\n") | map(select(startswith("Report: write your scoped findings to"))) | last`).
- All 32 extracted paths are uniform: `.ufo/waves/round-14/build/<TaskName>.md`.

## Member status table

Checks per member: `stat -c '%F|%s'` under lane root `/home/vgpnk/Projects/shokunin/mori-shokunin` (stat without `-L`, so symlinks would surface as "symbolic link"; none did), and existence of the same relative path under fleet root `/home/vgpnk/Projects/shokunin` (misrooted).

| name | status | size (B) | misrooted (fleet root) |
|---|---|---|---|
| CensusRepair | present | 10775 | no |
| JournalRegression | present | 14330 | no |
| HarnessMigration | present | 16581 | no |
| KnowledgeRepair | present | 11457 | no |
| IndexCorrection | present | 7878 | no |
| QualityCriteria | present | 6420 | no |
| SkillRegistry | present | 13266 | no |
| CatalogSource | present | 15720 | no |
| EmitterSource | present | 24205 | no |
| JournalFields | present | 16947 | no |
| FleetPredicate | present | 11987 | no |
| SignalCoverage | present | 20225 | no |
| CgroupScope | present | 20909 | no |
| ProtectedInventory | present | 27674 | no |
| PlanningWalk | present | 18723 | no |
| SiblingBoundary | present | 24408 | no |
| SourceFrontier | present | 34479 | no |
| MutationAttribution | present | 9733 | no |
| HistoricalCorrections | present | 24667 | no |
| GateConformance | present | 20113 | no |
| OomAttack | present | 22015 | no |
| RoutingAttack | present | 17779 | no |
| CounterAttack | present | 20124 | no |
| NoHarmReview | present | 16438 | no |
| JournalSentinel | present | 24523 | no |
| FixtureSentinel | present | 26984 | no |
| MutationDesign | present | 7815 | no |
| ScopedFixtures | present | 42981 | no |
| ResultFixtures | present | 69313 | no |
| EvidenceScribe | present | 18173 | no |
| SourcesScribe | present | 10855 | no |
| ShonenScribe | present | 9820 | no |

**Totals: 32 present (regular non-symlink file, >0 B) · 0 empty · 0 missing · 0 misrooted.**
Min size 6,420 B (QualityCriteria), max 69,313 B (ResultFixtures). The wave `build/` dir also contains `swarm-registry.json`, which is not a member report.

Misroot check was meaningful, not vacuous: `/home/vgpnk/Projects/shokunin/.ufo` exists (directory), but none of the 32 relative member paths exist beneath it (`stat` → absent for all).

## Comparison with recorded settlement/closure counts

| source | recorded count for this wave | agreement |
|---|---|---|
| `mori-shokunin/LOG.md:775` | "One validated 32-seat campaign wave, `.ufo/waves/round-14/spec.json` and `dispatch.json`" | 32 = 32 ✓ |
| `mori-shokunin/LOG.md:861-862` | "One validated 32-seat wave: 9 executors, 6 scouts, 3 connectors, 3 reviewers, 4 critics, 3 scribes, 2 sentinels, 1 revenger, 1 mutation-tester" | sum = 32 ✓; role mix independently re-counted from `dispatch.json` (`jq '.taskCall.tasks[].agent' \| sort \| uniq -c`): 9 executor, 6 scout, 3 connector, 3 reviewer, 4 critic, 3 scribe, 2 sentinel, 1 revenger, 1 mutation-tester — exact match ✓ |
| `wave*-settlement.json` | **none exists for round-14.** Direct `ls` of `.ufo/waves/round-14/` shows only `build/ evidence/ frozen/ dispatch.json scoped-counter-contract.json sources-after.json sources-before.json spec.json`. Only settlement JSON in lane waves is `.ufo/waves/round-19/wave2-settlement.json` (different wave) | n/a — nothing to contradict |
| `mori-shokunin/SCORECARD.md` | no round-14 per-seat settlement count (its 32/32-style counts at :87, :139, :198-199, :244, :290-291, :528 belong to rounds 2/4/5/6/11) | no contradiction |
| `/home/vgpnk/Projects/shokunin/MANIFEST.json` (mori round-14 entry, campaign hyaku, `closed_at 2026-10-20T07:04:16Z`, `verdict: admitted`, ~:7477-7506) | lane-level closure record; **no per-seat settlement count**. Dispatch digest "2026-10-20T02:52:22-03:00 launch mori round=14 … 03:51:58 complete" matches wave-file mtimes (Oct 20 02:54 local). No MANIFEST reference to `waves/round-14` (grep: no matches) | no contradiction |
| `.ufo/waves/round-14/build/swarm-registry.json` (`ufo-swarm-registry-v1`, wave "mori-r14-repair", reportDir `.ufo/waves/round-14/build`) | `jq '.members \| keys \| length'` → **32**; same 32 names as dispatch | 32 = 32 ✓ |

**Verdict: ground truth 32/32 present and non-empty, zero misrooted — agrees with every recorded closure count for this wave (all say 32).**

## Side observation (outside C2 scope, factual only)

`MANIFEST.json` mori round-14 entry cites `"report": ".ufo/reports/round-14/mori.md"`, but the lane's report directory `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/reports/` contains only `round-2 … round-11` (`ls` → `ls: cannot access '…/.ufo/reports/round-14/': No such file or directory`). So the lane-level closure report cited by the fleet MANIFEST is absent at that path on disk today. Not part of the 32 member reports audited here; unadjudicated [INFERENCE: likely removed/reorganized after closure; not investigated further — lane history off-bounds].

## Method (reproducible)

- Names + last Report line: `jq -r '.taskCall.tasks[] | [.name, (.task | split("\n") | map(select(startswith("Report: write your scoped findings to"))) | last | sub("^Report: write your scoped findings to "; ""))] | @tsv' dispatch.json`
- Status: `stat -c '%F|%s' <lane>/<rel>` and `stat -c '%F' <fleet>/<rel>` per member (loop over the jq TSV).
- Counts: `jq '.taskCall.tasks | length'`; `jq '.taskCall.tasks[].agent' | sort | uniq -c`; `jq '.members | keys | length' swarm-registry.json`.
