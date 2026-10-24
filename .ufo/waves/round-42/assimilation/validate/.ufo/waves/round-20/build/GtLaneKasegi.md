# GtLaneKasegi: C2 independent ground truth for kasegi-shokunin wave-dispatch files

Seat: MoriR20.GtLaneKasegi (leaf scout, no subagents). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin` was read only. No lane write, no git/jj, no tool under test (`tools/mori-wave-settlement.py`) and no oracle file opened. Observation time: 2026-10-21 07:30:37 -03.

## Method
1. Discovery: glob `kasegi-shokunin/.ufo/waves/**/*.json` (hidden on, gitignore off) returned 13 files. Cross-check `find kasegi-shokunin/.ufo -name '*.json'`: 13 under `.ufo/waves`, plus 24 under `.ufo/rounds/round-21` (outside scope, no dispatch-v1 file there).
2. Top-level schema: `jq '.schema // "NO_SCHEMA_KEY"'` over all 13 files.
3. Members: `jq '.taskCall.tasks'` on `round-23/build-dispatch.json`. Per member, the last `^Report:` line of `.task` is the trailer. The prefix `write your scoped findings to ` is stripped to get the path.
4. Lane status of each path: regular file with size > 0 = present; size 0 = empty; absent = missing. Misrooted = missing under the lane root but present at the same relative path under `/home/vgpnk/Projects/shokunin`.
5. Filename test: preview / undispatched / validation.
6. Tools: jq, find, python3 (stdlib, run via eval). No installs or updates.

## Files whose top-level schema is ufo-swarm-wave-dispatch-v1
Exactly one: `.ufo/waves/round-23/build-dispatch.json` (`"schema"` at line 2; `"taskCall"` at line 740; context at line 741).

| File (under `.ufo/waves/`) | Top-level schema | Dispatch-v1? |
|---|---|---|
| round-23/build-dispatch.json | ufo-swarm-wave-dispatch-v1 | YES |
| round-23/build/swarm-registry.json | ufo-swarm-registry-v1 | no |
| round-23/claims.json, build-spec.json, before-instruments.json, build-assignments.json, opened-source-snapshots.json, source-open-transcript.json, build-refusal-1.json, build-refusal-2.json, build-attempt-3.json, build-attempt-4.json, build-attempt-5.json | no `schema` key | no |

## Per-file totals: round-23/build-dispatch.json

| Metric | Value |
|---|---|
| Members (`taskCall.tasks[]`) | 64 |
| `counts` block | spawn 64, resume 0, total 64 |
| `build/swarm-registry.json` members | 64, same names as the dispatch tasks |
| Report trailers parsed | 64 (all `.ufo/waves/round-23/build/<Name>.md`, relative, no `..`, no absolute) |
| Report trailers unparsed | 0 |
| Naive parse `^Report:\s*(\S+)` | 64 would yield `write`. Prefix stripping is required. |
| Present under lane root (non-empty regular file) | 44 (sizes 2,665 B RecheckManifest.md to 16,548 B CraVuln.md) |
| Empty under lane root | 0 |
| Missing under lane root | 20 |
| Misrooted (missing in lane, present at same path under fleet root) | 0. `/home/vgpnk/Projects/shokunin/.ufo/waves/round-23/build/` does not exist. 0 of 64 names resolve there. |
| Filename suggests never dispatched | No. `build-dispatch.json` contains none of preview / undispatched / validation. |
| `resumeSends` / `compaction.applied` | `[]` / `false` |

## Lane totals
- JSON under `.ufo/waves`: 13. dispatch-v1: 1. registry-v1: 1. no schema key: 11.
- Dispatch members: 64. Parsed 64, unparsed 0. Present 44, empty 0, missing 20. Misrooted 0.
- Dispatch-v1 files flagged by filename: 0 of 1.
- `round-23/build/`: 45 entries = 44 expected report `.md` files + `swarm-registry.json`. No stray files.

## Dispatch status: content evidence (filename gives no signal)
Local times from mtimes (-03). Registry UTC stamps agree with these.
- 18:33:30 `build-dispatch.json` written (registry `createdAt` 21:33:30Z).
- 18:33:57 `build-refusal-1.json:2`: `Failed to start background task jobs: KasegiR23.FixMirror: Background job limit reached (100)`. All 64 names refused.
- 18:34:17 `build-refusal-2.json`, 18:37:24 `build-attempt-3.json`, 18:38:19 `build-attempt-4.json`: same refusal, all 64 names.
- 18:41:53 `build-attempt-5.json:2`: `Spawned 64 background agents using executor, scribe, scout, reviewer, critic, connector, revenger, sentinel.` `details.progress` has 64 entries, all `pending`. All 64 names appear in the spawn list.
- 18:42:19 `build/swarm-registry.json` (`updatedAt` 21:42:19Z): 64 entries, `kind: spawn`. No status or report field.
- 18:43:50 to 18:48:23: 44 report files written, all newer than the dispatch file.
- No wave file modified after 18:48:23. Snapshot at 07:30 on 10-21: about 12.7 h later, 20 spawned members have no report.

Reading: the file was not "never dispatched". The wave was dispatched on attempt 5 after four refused attempts. [INFERENCE] The 20 missing members were spawned but did not write their report at the lane path. The artifacts record no per-member completion, so I cannot tell whether they failed, stalled, or wrote elsewhere.

## Missing reports (20) by role
| Agent | Missing / total | Names |
|---|---|---|
| scribe | 6 / 6 | DraftF06, DraftF07, DraftF08, LessonRules, GateDraft, RegistryDraft |
| reviewer | 7 / 19 | BountyParent, RelativeSymlink, RootBoundary, AliasBoundary, DirectBounty, NoisyTokens, FixtureExpected |
| scout | 5 / 16 | CnaVersion, CraIncident, CraDates, SafeHarborLocation, CnaCurrentRoute |
| connector | 1 / 4 | ConnectClaims |
| revenger | 1 / 4 | RevDeletions |
| executor, critic, sentinel | 0 / 3, 0 / 8, 0 / 4 | none |

Search for those 20 names:
- Exact `<Name>.md` under `kasegi-shokunin/.ufo` and `/home/vgpnk/Projects/shokunin/.ufo` (depth 6): no match. A control search for present names found their files, so the regex works.
- Name variants (`<Name>[^/]*`, files, same roots plus the 14 `/tmp/kasegi-r23-*` clones): no match.
- Exact path in the clones (depth 7): no match. Unreadable system dirs under `/tmp` returned permission errors. None is a kasegi clone.

## Per-member table
Index is the position in `taskCall.tasks[]` (0-based). Every trailer is `.ufo/waves/round-23/build/<Name>.md`.

| i | Member | Agent | Lane report |
|---|---|---|---|
| 0 | FixMirror | executor | present |
| 1 | CountMirror | executor | present |
| 2 | RecheckSources | executor | present |
| 3 | DraftF06 | scribe | missing |
| 4 | DraftF07 | scribe | missing |
| 5 | DraftF08 | scribe | missing |
| 6 | FirstRoles | scout | present |
| 7 | FirstTimes | scout | present |
| 8 | FirstSharing | scout | present |
| 9 | CnaScope | scout | present |
| 10 | CnaFix | scout | present |
| 11 | CnaVersion | scout | missing |
| 12 | CraVuln | scout | present |
| 13 | CraIncident | scout | missing |
| 14 | CraDates | scout | missing |
| 15 | CraRecipients | scout | present |
| 16 | SafeHarborLocation | scout | missing |
| 17 | CvssRecheck | scout | present |
| 18 | CvdRecheck | scout | present |
| 19 | AiRecheck | scout | present |
| 20 | CweRecheck | scout | present |
| 21 | CnaCurrentRoute | scout | missing |
| 22 | BountyParent | reviewer | missing |
| 23 | RelativeSymlink | reviewer | missing |
| 24 | BountySymlink | reviewer | present |
| 25 | NestedEscape | reviewer | present |
| 26 | GlobEscape | reviewer | present |
| 27 | PlaceholderEscape | reviewer | present |
| 28 | BraceEscape | reviewer | present |
| 29 | RootBoundary | reviewer | missing |
| 30 | AliasBoundary | reviewer | missing |
| 31 | DirectBounty | reviewer | missing |
| 32 | LaneRelative | reviewer | present |
| 33 | OverrideAbsent | reviewer | present |
| 34 | RangeLimits | reviewer | present |
| 35 | EmptyCorpus | reviewer | present |
| 36 | NoisyTokens | reviewer | missing |
| 37 | GeneratedReport | reviewer | present |
| 38 | AxisFit | critic | present |
| 39 | CoverageDenom | critic | present |
| 40 | Causal | critic | present |
| 41 | Q1Executable | critic | present |
| 42 | ImmutableSources | critic | present |
| 43 | HistoricalRows | critic | present |
| 44 | RedBefore | critic | present |
| 45 | NoHarm | critic | present |
| 46 | OverlapResearch | connector | present |
| 47 | OverlapVault | connector | present |
| 48 | OverlapWeb | connector | present |
| 49 | ConnectClaims | connector | missing |
| 50 | RevPlaceholder | revenger | present |
| 51 | RevPointers | revenger | present |
| 52 | RevDeletions | revenger | missing |
| 53 | RevAuthority | revenger | present |
| 54 | LessonRules | scribe | missing |
| 55 | GateDraft | scribe | missing |
| 56 | RegistryDraft | scribe | missing |
| 57 | FixtureSafety | sentinel | present |
| 58 | RecheckSafety | sentinel | present |
| 59 | SourceSafety | sentinel | present |
| 60 | FleetScope | sentinel | present |
| 61 | FixtureExpected | reviewer | missing |
| 62 | RecheckManifest | reviewer | present |
| 63 | CountCommands | reviewer | present |

## Leads (lane-authored, not verified here)
- `.ufo/waves/round-23/build/FleetScope.md:13` (in the lane, written by a sibling seat) says the upstream renderer `ufo-swarm-wave.mjs:208-209` builds report paths from `reportDir/name.md` without binding them to the lane cwd. That would be a misrooting mechanism. I did not open the renderer, and this wave has 0 misrooted paths by the fleet-root test.

## Unobserved ([INFERENCE] or not checked)
- Cause of the 20 missing reports (failed, stalled, still running, or written elsewhere). No per-job completion record exists in these files, and I did not open session transcripts.
- Process state of the 20 background jobs. Not observable from read-only artifacts.
