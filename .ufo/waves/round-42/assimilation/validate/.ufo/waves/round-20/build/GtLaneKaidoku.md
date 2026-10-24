# GtLaneKaidoku: C2 independent ground truth, kaidoku-shokunin (`ufo-swarm-wave-dispatch-v1`)

Status: complete. Seat `MoriR20.GtLaneKaidoku` (leaf, no subagents). Read-only: no writes in the lane, no git or jj commands, no report bytes opened (existence and size only). Rules applied from `.ufo/waves/round-20/contract.md`, C2 section.

## 1. Method and evidence

- **Enumeration.** `glob` truncated at 200 entries, so the lane was enumerated with `os.walk` (symlinks not followed) and `find <lane>/.ufo/waves -type f -name '*.json'`. Both return **3,411** JSON files.
- **jq binary.** `/usr/bin/jq` is jq-1.8.2 (`pacman -Qo`: owned by `jq 1.8.2-1`). The bare `jq` in this bash tool is a shell builtin that reports `jaq 3.1.1`; my initial structure inspection used it, but every reported count was produced with `/usr/bin/jq`. No install or update was needed or performed. pacman was only queried (`-Q`, `-Qo`).
- **Schema filter.** `/usr/bin/jq -r 'if type=="object" then (if has("schema") then (.schema|if type=="string" then . else "<non-string>" end) else "<absent>" end) else "<non-object>" end' FILE`. A file is a dispatch file iff the output is `ufo-swarm-wave-dispatch-v1`.
- **Members.** `/usr/bin/jq -r '.taskCall | if . == null then "NOSPAWN" else (.tasks[] | [(.name|tostring), (.agent|tostring), ((.task // "")|split("\n")|last // "")] | @tsv) end' FILE`. Member count is `.taskCall.tasks|length`.
- **Trailer rule** (contract C2, "Expected report path"). The last line of `task` must match `^Report: write your scoped findings to (\S+)$`. A path is safe iff it is relative, has no `..` component, and resolves inside the lane root.
- **Status rules.** `present` = regular, non-symlink, size > 0. `empty` = size 0. `missing` = absent under the lane root. `misrooted` = missing under the lane root but a regular file at the same relative path under `/home/vgpnk/Projects/shokunin`. `unsafe`. `unparsed` = no trailer on the last line.
- **Wave-state rules.** `settled` = all present. `partial` = at least one present and at least one not. `unsettled` = none present. `no-spawn` = `taskCall` null. `unavailable` = no member with a safe parsed path.
- **Two independent passes agree.** Python (`json`, `os.stat`) and jq plus `find -printf '%s\t%p'` gave identical member names, order, trailer paths and statuses for all **959** members (0 mismatches). The dispatch-file set matched a raw-bytes scan for the schema string (14 = 14). A `_grep` for the exact `"schema": "ufo-swarm-wave-dispatch-v1"` pair across every file type under `.ufo/waves` returned the same 14 files, so no dispatch file sits outside the `*.json` scan.

## 2. Per-file totals (14 dispatch-v1 files)

Each wave's trailers point into a single directory, `.ufo/waves/round-NN/wN/`. Columns: members, parsed, unparsed, unsafe, present, empty, missing, misrooted, state, filename flag (`preview|undispatched|validation` in the name).

| # | File (lane-relative) | Wave | Report dir | Members | Parsed | Unparsed | Unsafe | Present | Empty | Missing | Misrooted | State | Filename flag |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 1 | `.ufo/waves/round-14/dispatch.json` | kaidoku-r14-w1 | `round-14/w1` | 32 | 32 | 0 | 0 | 32 | 0 | 0 | 0 | settled | no |
| 2 | `.ufo/waves/round-15/dispatch.json` | kaidoku-r15-w1 | `round-15/w1` | 32 | 32 | 0 | 0 | 32 | 0 | 0 | 0 | settled | no |
| 3 | `.ufo/waves/round-16/wave1-dispatch.json` | kaidoku-r16-w1 | `round-16/w1` | 64 | 64 | 0 | 0 | 36 | 0 | 28 | 0 | partial | no |
| 4 | `.ufo/waves/round-16/wave2-dispatch.json` | kaidoku-r16-w2 | `round-16/w2` | 32 | 32 | 0 | 0 | 32 | 0 | 0 | 0 | settled | no |
| 5 | `.ufo/waves/round-17/wave1-dispatch.json` | kaidoku-r17-w1 | `round-17/w1` | 78 | 78 | 0 | 0 | 78 | 0 | 0 | 0 | settled | no |
| 6 | `.ufo/waves/round-17/wave2-dispatch.json` | kaidoku-r17-w2 | `round-17/w2` | 69 | 69 | 0 | 0 | 67 | 0 | 2 | 0 | partial | no |
| 7 | `.ufo/waves/round-18/wave1-dispatch.json` | kaidoku-r18-w1 | `round-18/w1` | 89 | 89 | 0 | 0 | 89 | 0 | 0 | 0 | settled | no |
| 8 | `.ufo/waves/round-18/wave2-dispatch.json` | kaidoku-r18-w2 | `round-18/w2` | 98 | 98 | 0 | 0 | 94 | 0 | 4 | 0 | partial | no |
| 9 | `.ufo/waves/round-19/wave1-dispatch.json` | kaidoku-r19-w1 | `round-19/w1` | 90 | 90 | 0 | 0 | 48 | 0 | 42 | 0 | partial | no |
| 10 | `.ufo/waves/round-19/wave2-dispatch.json` | kaidoku-r19-w2 | `round-19/w2` | 72 | 72 | 0 | 0 | 72 | 0 | 0 | 0 | settled | no |
| 11 | `.ufo/waves/round-20/wave1-dispatch.json` | kaidoku-r20-w1 | `round-20/w1` | 100 | 100 | 0 | 0 | 98 | 0 | 2 | 0 | partial | no |
| 12 | `.ufo/waves/round-20/wave2-dispatch.json` | kaidoku-r20-w2 | `round-20/w2` | 71 | 71 | 0 | 0 | 71 | 0 | 0 | 0 | settled | no |
| 13 | `.ufo/waves/round-21/wave1-dispatch.json` | kaidoku-r21-w1 | `round-21/w1` | 64 | 64 | 0 | 0 | 26 | 0 | 38 | 0 | partial | no |
| 14 | `.ufo/waves/round-21/wave2-dispatch.json` | kaidoku-r21-w2 | `round-21/w2` | 68 | 68 | 0 | 0 | 49 | 0 | 19 | 0 | partial | no |
| | **Total** | 14 waves | | **959** | **959** | **0** | **0** | **824** | **0** | **135** | **0** | 7 settled, 7 partial | 0 |

Each file's own `counts.spawn` and `counts.total` equal its member count, `counts.resume` is 0, and `resumeSends` is 0 for all 14.

## 3. Lane totals

| Quantity | Value |
|---|---|
| JSON files under `.ufo/waves` (all regular) | 3,411; 0 JSON-named symlinks |
| Files with top-level `schema` = `ufo-swarm-wave-dispatch-v1` | 14 |
| `taskCall: null` (no-spawn) | 0 |
| Members (`taskCall.tasks[*]`) | 959 |
| Trailers parsed / unparsed | 959 / 0 (100% parsed) |
| Unsafe paths | 0 |
| Present | 824 (85.9%) |
| Empty | 0 |
| Missing | 135 (14.1%) |
| Misrooted | 0 |
| Distinct report paths / duplicated paths | 959 / 0 |
| Wave states | settled 7, partial 7, unsettled 0, no-spawn 0, unavailable 0 |
| Dispatch filenames matching `preview` / `undispatched` / `validation` | 0 of 14 |
| Other JSON, not dispatch-v1 (`ignored_json`, strict single-document parse) | 3,358 |
| Unreadable JSON (`unreadable_json`, strict single-document parse) | 39 |

Expected output of a correct `scan --lane-root` on this lane: 14 waves, 959 members, present 824, missing 135, misrooted 0, unsafe 0, unparsed 0, empty 0, states settled 7 and partial 7, `ignored_json` 3,358, `unreadable_json` 39. For a parser that accepts multi-value JSON streams, the last two become 3,361 and 36 (see §4.1).

## 4. Edge cases and cross-checks

1. **Parser-dependent unreadable count.** Strict single-document parsing (Python `json`) gives 39. `jq` rejects 36 of them. The 3 it accepts are multi-value streams: `.ufo/waves/arc3-loop1-round6/claims/c2/CR-4/evidence/compile-rerun.json` (3 values), `.ufo/waves/arc3-loop1-round6/claims/c3/EX-15/cmdA-before.json` (2 values), `.ufo/waves/arc3-loop1-round6/claims/c3/SC-1/commandA-before.json` (2 values). None of the 39 contains the dispatch schema string. The 36 `jq`-rejected files fall into three kinds: non-JSON text (for example `.ufo/waves/arc3-loop1-round3/claims/c1/EX-12/std-output.json`, which starts `>>> Cannot retry compila`); truncated JSON (for example `.ufo/waves/arc3-loop1-round1/claims/c2/RV-6/table-trunc.json`, 22 bytes, ending mid-object); or a complete object followed by trailing non-JSON text (for example `.ufo/waves/arc3-loop1-round2/claims/c2/CR-2/evidence/landed3__live-repo.json`, where jq emits the object and then fails at line 296).
2. **Symlinks.** 11 symlink entries sit under `.ufo/waves`, none JSON-named: 10 file symlinks (two of them self-referencing `symlink-loop` entries under `round-18/verify/scratch-custody/` and `round-19/verify/scratch-custody/`) and one directory symlink, `.ufo/waves/arc3-loop1-round4/tools/vyper-venv/lib64 -> lib`. The directory target is inside the scanned tree and is walked under its real path, so nothing is lost or double-counted.
3. **Near-miss schema.** `.ufo/waves/round-21/wave1-plan.json` has `schema: ufo-swarm-wave-v1` (not dispatch-v1), so it is ignored.
4. **Filename flags.** None of the 14 dispatch filenames matches `preview|undispatched|validation`. The only lane JSON basename with those words is `.ufo/waves/round-16/w2/PreviewNotValidation-cases.json`, a non-object top-level value, not dispatch-v1, ignored.
5. **Misrooted: none.** The fleet tree `/home/vgpnk/Projects/shokunin/.ufo/waves` (1,954 regular files) has no file at any of the 135 missing relative paths. Every missing member's parent directory exists in the lane, so the report directories are present and the reports themselves are absent.
6. **Same-name hits elsewhere (not counted).** Six missing members have a same-basename file in another round's `w1` directory: `round-16/w1/SiblingOverlap.md` (matches in round-14 and round-19), `round-19/w1/CriticC1.md`, `CriticC2.md`, `CriticC3.md` (matches in round-18 and round-20), `round-19/w1/SentinelSandbox.md` (round-18), `round-19/w1/ReviewSkillRegistry.md` (round-20). Seat names recur across rounds, so these are not misroutes under the contract's definition and are not counted as present.
7. **No near-named file in the same directory** for any missing member (case-insensitive substring check): 0.
8. **Orphans (not referenced by the wave's own trailers, not counted).** 70 files across the 14 report directories. Each directory holds one `swarm-registry.json`; the rest are candidate or draft files such as `round-14/w1/RegistryDeltaDraft.candidate.md`, `round-17/w1/draft-report.md` and `round-17/w2/measure-base.json`.
9. **Staleness** [INFERENCE: mtime comparison only; checkouts can reset mtimes]. No present report is older than its dispatch file. The smallest present report is 1,738 bytes (round-21 wave2); none is under 200 bytes. Report content was not read, so "present" does not show that a report is substantive.

## 5. Spawn history (non-dispatch JSON, not counted by the scan)

`refused` is the count recorded in each attempt entry. Reading it as members refused at spawn is [INFERENCE].

| File | Recorded spawn outcomes | Dispatch file: present / members |
|---|---|---|
| `round-17/wave1-dispatch-attempts.json` | 3 entries: refused 78 and 78 (text: "Background job limit reached (100)"), then refused 0 | 78 / 78 |
| `round-17/wave2-dispatch-attempts.json` | 1 entry: refused 0 | 67 / 69 |
| `round-20/wave1-dispatch-attempts.json` | 2 entries: refused 100 (result null), then refused 0 | 98 / 100 |
| `round-20/wave2-dispatch-attempts.json` | 3 entries: refused 71, 71, then 0 | 71 / 71 |
| `round-21/wave1-dispatch-attempts.json` | 1 entry: failed start, all 64 refused ("Background job limit reached (100)") | 26 / 64 |
| `round-21/wave1-registration-recovery.json` | `.text` begins "Spawned 64 background agents using executor, reviewer, scout, connector, scribe, critic, sentinel." | (same wave) |
| `round-21/wave2-attempts.json` | 2 entries: failed start, all 68 refused ("Background job limit reached (100)"), then "Spawned 68 background agents using reviewer, scout, connector, mutation-tester." | 49 / 68 |

- **Round-21 wave 1 gap.** The attempts file logs only the refused start. The 26 present reports are consistent with the recovery record's spawn of 64 agents. [INFERENCE] That recovery record is the successful spawn behind this dispatch file. Seat transcripts were not opened, per the bounds.
- **Never-dispatched question.** Every one of the 14 dispatch files has at least 26 present reports, so none is an unrun wave on report evidence. The filename check is 0 of 14.

## 6. Missing members by file (135)

Sorted by name, as the contract's `missing` field would list them.

**round-16/wave1-dispatch.json (28):** ArchOrder, AttackApplicability, AttackPatchContent, AttackRegistry, AttackScores, AttackVersionLabel, AttackZero, BaseName, ControlProvenance, DiagnosticChain, DiffLoop, EvidenceOrigin, Frontier, FunctionLookup, Installed124, Installed125, InvalidSemantics, InvocationChain, LowestAxis, PatchEngine, PatchZero, PriorRoutes, ReadOrder, Separation, SiblingOverlap, TypeLookup, UnixSet, VersionFormatting

**round-17/wave2-dispatch.json (2):** PinsAttack, TemporalSweepAttack

**round-18/wave2-dispatch.json (4):** GatePRODUCERREV, GateSUMSRUNLOG, ShonenLines, TruthREGISTRY

**round-19/wave1-dispatch.json (42):** AliasRevSemantics, C1CensusDiag, CarrierCensus125, CitationDriftAliases, CriticC1, CriticC2, CriticC3, CriticCarried, CriticSeparability, Doctor67, GenPredictionsR19, GhidraGoDetect, GoDlJsonSource, HeadRevLintNested, JjRedBeforeSafety, KnowledgeEntrySkeleton, LinkNoBuildinfo, MeasureR19, PriorRunTimes, ProvincePinsTool, ProvinceRewriteDraft, R12Queue, ReaReleaseNotes, ReadmeFrontier, ReviewCarrierRunEnv, ReviewCitationDrift, ReviewCustodyPair, ReviewDecisionRule, ReviewHeadRevLint, ReviewMeasureR18, ReviewProvinceStale, ReviewR18Mistakes, ReviewRevpin, ReviewSkillRegistry, RoutedR18Tool, RunCarriersR19, SentinelReaRun, SentinelSandbox, SimplifyR19Tools, ValidatorDigestGuard, VerifyR19, VetMisreadTrace

**round-20/wave1-dispatch.json (2):** ConnJjSelftests, ConnSiblingHarmony

**round-21/wave1-dispatch.json (38):** C1CaseBoundary, C1DirectoryCite, C1HarmonyWitness, C1PositiveWitness, C1RefusalRecord, C1ToonBoundary, C2BoundTypes, C2ExtractorExit, C2IndexTypes, C2MissingIndex, ConnCountDesign, ConnLearning, ConnNoHarm, ConnPriorC1C3, CriticBudget, CriticClaimC1, CriticClaimC2, CriticPopulation, CriticSeparability, CriticSources, ExecFailureCompare, ExecFrozenBattery, ExecVerbBinding, ScoutBindingSchema, ScoutEvidenceJson, ScoutFailureLogs, ScoutHarmonyShape, ScoutRoutes, ScoutSourcePython, ScoutSourceQuotes, ScoutWasmErrors, ScribeMistake, ScribeNullLesson, ScribeRegistry, ScribeResiduals, ScribeSourceGate, ScribeTrend, SentinelParserScope

**round-21/wave2-dispatch.json (19):** R21Attack05, R21Attack11, R21Attack13, R21Attack16, R21Attack18, R21Attack21, R21Attack22, R21Attack25, R21Attack34, R21Attack38, R21Attack41, R21Attack50, R21Attack51, R21Attack52, R21Attack54, R21Attack55, R21Attack59, R21Attack61, R21Attack64

## 7. Verdict for the C2 comparison

- Dispatch-v1 files: **14**. Members: **959**. Parsed: **959**. Unparsed: **0**. Unsafe: **0**.
- Present: **824**. Empty: **0**. Missing: **135**. Misrooted: **0**.
- Wave states: **7 settled, 7 partial**. No unsettled, no-spawn or unavailable waves.
- Filename-based never-dispatched flags: **0**.
- The only reconciliation item is the parser-dependent unreadable count (39 strict, 36 under jq), which does not touch the dispatch set.
