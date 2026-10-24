# GtLaneKake: C2 independent ground truth for kake-shokunin dispatch files

Status: complete. Manual, read-only, leaf seat (no subagents). Nothing was written under the lane root or the fleet root. No tool, package or binary was installed or updated.

Lane root: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Fleet root: `/home/vgpnk/Projects/shokunin`.

**Summary.** 5 dispatch-schema files, 325 members, 261 present, 0 empty, 64 missing, 0 misrooted (frozen definition), 0 unparsed, 0 unsafe. Wave states: 2 settled, 3 partial. One file carries the filename flag (`round-21/wave1-validation.json`), and its own evidence contradicts non-dispatch. Observed outside the frozen rules: 18 of the 21 missing `round-22/w2` report paths have a same-lane successor under `round-23/w1` (section 5).

## 1. Method
- **Discovery:** recursive walk of `kake-shokunin/.ufo/waves`, hidden directories included, symlinks not followed. 177 regular `*.json`, 0 symlinks, 0 unreadable. Non-JSON regular files in the same tree (out of scope, not read): 377.
- **Schema (`/usr/bin/jq`, jq-1.8.2):** `if type=="object" then (if has("schema") then (.schema|tostring) else "NO_SCHEMA_KEY" end) else "NON_OBJECT" end`. Matched per file against Python `json`: 0 mismatches. The bare `jq` in this shell is a builtin that reports `jaq 3.1.1`; it was not used.
- **Members:** `jq -c '.taskCall.tasks[] | {name, agent, task}'`. Every dispatch file has an object `taskCall`; none is null. `counts.spawn` equals the task count in all five files.
- **Report path:** last line of each `task` must match `^Report: write your scoped findings to (\S+)$`. Safety: relative, no `..` component, resolves inside the lane root.
- **Status:** present = regular, non-symlink, size > 0; empty = size 0; missing = absent under the lane root. Misrooted = missing under the lane root and a regular file at the same relative path under the fleet root (frozen C2 definition).
- **Wave state:** C2 contract rules. **Filename flag:** basename contains `preview`, `undispatched` or `validation`.

## 2. Per-file totals

| # | File (under `.ufo/waves/`) | Wave | Members | Parsed / unparsed | Present | Empty | Missing (of which misrooted) | Unsafe | Wave state | Filename flag |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | round-21/wave1-validation.json | kake-r21-build | 64 | 64 / 0 | 64 | 0 | 0 (0) | 0 | settled | **yes** ("validation") |
| 2 | round-22/w1-dispatch.json | kake-r22-w1 | 64 | 64 / 0 | 60 | 0 | 4 (0) | 0 | partial | no |
| 3 | round-22/w2-dispatch.json | kake-r22-w2 | 64 | 64 / 0 | 43 | 0 | 21 (0) | 0 | partial | no |
| 4 | round-23/w1-dispatch.json | kake-r23-w1 | 69 | 69 / 0 | 69 | 0 | 0 (0) | 0 | settled | no |
| 5 | round-23/w2-dispatch.json | kake-r23-w2 | 64 | 64 / 0 | 25 | 0 | 39 (0) | 0 | partial | no |
| | **Lane total** | | **325** | **325 / 0** | **261** | **0** | **64 (0)** | **0** | 2 settled, 3 partial | 1 file |

Each dispatch file: `counts` = {spawn = members, resume = 0}; `resumeSends` = []; `compaction.applied` = false.

## 3. Lane totals
- JSON under `.ufo/waves`: 177 = 5 dispatch + 5 `ufo-swarm-registry-v1` + 164 with no `schema` key + 3 top-level arrays. By round directory: round-21 20, round-22 63, round-23 94.
- `ignored_json` = 172. `unreadable_json` = 0. Symlinks = 0.
- Members 325 · parsed 325 · unparsed 0 · unsafe 0 · present 261 · empty 0 · missing 64 · misrooted 0.
- Wave states: settled 2 (rows 1, 4); partial 3 (rows 2, 3, 5); unsettled 0; unavailable 0; no-spawn 0.
- Dispatch-named JSON excluded by schema: `round-21/wave1-dispatch-result.json` (keys `details`, `text`) and `round-23/recovery-dispatch.json` (recovery-record keys). Across all 177 files, only the five dispatch-schema files carry a top-level `taskCall`.

## 4. Missing members (no lane-root file; no same-path fleet file)
- **round-22/w1 (4)**, scribe: Knowledge, LessonDraft, RegistryDraft, TrendDraft. Expected `.ufo/waves/round-22/w1/<Name>.md`.
- **round-22/w2 (21)**, reviewer 9: Attack23, BoundaryAttributes, BoundaryHeadRecovery, BoundaryInertContexts, BoundaryManifestKeys, BoundaryReadOnly, BoundaryReplayIntegrity, BoundaryTraversal, BoundaryURLAuthority. Scout 8: ReopenGoogleCanonical, ReopenGoogleTroubleshoot, ReopenHTMLBase, ReopenHTMLLink, ReopenHTMLTemplate, ReopenPythonParser, ReopenPythonURL, ReopenRFC6596. Connector 4: ConnectBrowser, ConnectCapability, ConnectProof, ConnectSource.
- **round-23/w2 (39)**, reviewer 29: AttackBaseGuard, AttackControlChars, AttackDuplicatePages, AttackForeignStack, HoldFireJournalCodes, HoldGhpSubpathSpotcheck, HoldKeeperTimerInert, HoldKimiSubpathAudit, HoldMirrorPitfalls, HoldOriginRepos, HoldProbeDeltaAlerting, HoldPropertyMap, HoldPublishChannels, HoldPublishQueue, HoldSitemapOrphanAudit, HoldSpeedrunPipeline, ReviewKnowledgeDelta, ReviewUpstreamFixes, StaleFreeReadVerbs, StaleGhpSubpathSpotcheck, StaleKeeperTimerInert, StaleMirrorPitfalls, StaleOpsAutomation, StaleOriginRepos, StaleProbeDeltaAlerting, StalePublishChannels, StalePublishQueue, StaleSpeedrunPipeline, StaleVaultProperties. Scout 9: RecheckBurnerchromeKimi, RecheckCharterGhp, RecheckCharterKimi, RecheckDs4ccKimi, RecheckLucarioGhp, RecheckPlazir15Ghp, RecheckPlazir15Kimi, RecheckVaultIndexKimi, ReopenS031. Connector 1: ConnectR23Axes.

## 5. Same-lane successors of missing round-22/w2 reports (observed; outside the frozen definitions)
- 17 missing `round-22/w2` names have an identically named, present report at `round-23/w1/<Name>.md`: ReopenGoogleCanonical, ReopenHTMLBase, ReopenHTMLLink, ReopenHTMLTemplate, ReopenPythonParser, BoundaryAttributes, BoundaryHeadRecovery, BoundaryInertContexts, BoundaryManifestKeys, BoundaryReadOnly, BoundaryReplayIntegrity, BoundaryTraversal, BoundaryURLAuthority, ConnectBrowser, ConnectCapability, ConnectProof, ConnectSource.
- `Attack23` has a renamed successor: round-23/w1 member `Attack23WrongHost` (`round-23/w1/Attack23WrongHost.md`, present).
- Evidence: these 18 round-23/w1 task texts open with "Carried from round-22 dead wave-2 seat ..." (5 of them read "(never ran)"). They are the only tasks in the five dispatch files with that phrase. This is task text; the run state is not verified.
- No successor for ReopenRFC6596, ReopenGoogleTroubleshoot or ReopenPythonURL: no same-basename file in the 694 lane files scanned, and no reference in any dispatch text.
- No carry-over text for round-22/w1 (Knowledge, LessonDraft, RegistryDraft, TrendDraft) or round-23/w2 (39 names). Round-23/w1 `ScribeLessonDraft` contains "LessonDraft" as a substring but is a different member with no carry-over phrase [INFERENCE: not a successor].
- Effect: under the frozen rules the 18 remain `missing` for round-22/w2 (no fleet copy, so not `misrooted`), and round-23/w1 is `settled` on its own 69. The frozen spec has no successor state, so a tool run will not show this. Whether the C2 expected output should record carried-over successors is a decision for L1; this seat does not decide it.

## 6. Filename-flag evaluation
- `round-21/wave1-validation.json`: flag YES ("validation"). Contrary evidence: `counts.spawn` = 64 and `resume` = 0; all 64 reports present under `round-21/w1/`; every present report's mtime (2026-10-20 08:55Z to 09:11Z) is later than the file's own mtime (08:54Z). The name alone does not show non-dispatch; the lane evidence shows dispatch and reporting.
- Other four files: no keyword. No dispatch file name contains `preview` or `undispatched`.

## 7. Cross-checks (all pass)
- jq vs Python schema per file: 0 mismatches over 177 files.
- Trailers: strict and lenient parse agree 325/325; each text has exactly one trailer line, equal to the parsed path; no duplicate report paths across the 325 members; no duplicate member names within a file.
- Report-directory reconciliation: entries = present members + non-member entries only. `round-21/w1` 65 = 64 + `swarm-registry.json`; `round-22/w1` 61 = 60 + registry; `round-22/w2` 45 = 43 + registry + `raw/`; `round-23/w1` 70 = 69 + registry; `round-23/w2` 26 = 25 + registry. No unmatched `.md` in any report directory; none of the 64 missing basenames is present in its directory.
- mtime ordering: for all five files, 0 present reports older than the dispatch file.
- Fleet root: `.ufo/waves/round-22` and `.ufo/waves/round-23` do not exist (`round-21` does). `os.path.lexists` is false for all 64 missing expected paths. Misrooted = 0.
- Informational fleet search: basenames of the 64 missing reports searched in the `.ufo/waves` trees of the fleet root and 16 sibling directories (57,653 files; kake excluded). 18 hits, none under any sibling `round-22` or `round-23` directory. Each hit either predates the relevant dispatch (round-22/w1 at 2026-10-20 21:33Z; round-23/w2 at 2026-10-21 07:29Z) or is a clone copy with the same size as its original (tabi `round-20/final-clones/*/.ufo/waves/round-16/w2/ReopenS031.md`, 12,819 bytes) [INFERENCE: name collisions, not misroutes].
- Same-lane basename search (694 files under kake-shokunin, `.git`/`.jj` excluded): 17 hits, all `round-23/w1/<Name>.md`, the section 5 successors.

## 8. Expected C2 tool output for this lane (hand-derived; no tool run)
- `dispatch_files` 5 · `ignored_json` 172 · `unreadable_json` 0 · members 325 · present 261 · empty 0 · missing 64 · misrooted 0 · unsafe 0 · unparsed 0.
- States: round-21 wave1-validation `settled`; round-22/w1 `partial`; round-22/w2 `partial`; round-23/w1 `settled`; round-23/w2 `partial`. No `unsettled`, `unavailable` or `no-spawn`.
- Exit: 1 (three partial waves).
- `missing` lists as in section 4.

## 9. Limits and tooling record
- "Present" = existence, non-symlink, size > 0. Content is not judged: e.g. `round-23/w2/MutateCounterSelftest.md` (807,816 bytes) is present and was not read.
- "Dead" and "never ran" come from task text; run state not verified. No seat logs, session logs or transcripts were opened.
- Ground truth covers kake-shokunin only; the fleet-root and sibling searches are informational.
- Timestamps are used only for ordering checks.
- Tool installs/updates: none. Used `/usr/bin/jq` (jq-1.8.2); `~/.local/bin/jq` is also jq-1.8.2. No pacman use (transactions paused host-wide).
