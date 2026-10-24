STATUS: complete

# GtLaneSouji: C2 independent fleet ground truth, souji-shokunin wave dispatches

Scope: every `*.json` under `/home/vgpnk/Projects/shokunin/souji-shokunin/.ufo/waves`, filtered to top-level `schema == "ufo-swarm-wave-dispatch-v1"`. The lane was read only; nothing in it was edited, and no git or jj command ran.

## Method (no fleet tool used; `tools/mori-wave-settlement.py` not touched)

- Enumeration: `find ... -type f -name '*.json'` = 55; the glob tool = 55; Python `glob` = 55. All 55 parse, and each top level is a JSON object. `.ufo/waves` holds 818 files in total and 0 symlinks.
- Schema filter: `/usr/bin/jq -e '.schema == "ufo-swarm-wave-dispatch-v1"'` selects **12** files. Stdlib `json` selects the same 12.
- Members = `len(.registry.members)`. Checked against `.counts.total` and `len(.taskCall.tasks)`, and task `name`s checked against the member keys. All three agree in every file.
- Trailer extraction: `.taskCall.tasks[] | .name as $n | (.task | split("\n")[]) as $l | select($l | test("Report"))`. A trailer is a line that, after trimming, starts with `Report:`. It is parsed when the task has exactly one such line and that line matches `^Report: write your scoped findings to (\S+)$`.
- Lane class (path relative to `souji-shokunin/`): present = regular file with non-whitespace content; empty = 0 bytes or whitespace only; missing = no entry.
- Misrooted = lane class missing or empty AND the same relative path exists as a non-directory under `/home/vgpnk/Projects/shokunin/`.
- Name flag = basename contains `preview`, `undispatched`, or `validation`.
- Per-trailer detail (783 rows: file, task, trailer count, path, lane class, bytes, fleet exists, misrooted, form): `mori-shokunin/.ufo/waves/round-20/build/GtLaneSouji/trailers.tsv`.

Tool provenance: in the persistent bash tool, `jq` is a shell builtin that runs **jaq 3.1.1** (`type -a jq`; `jq --version` printed `jaq 3.1.1`). I did not use it. All jq results come from `/usr/bin/jq` (jq-1.8.2). `~/.local/bin/jq` is also jq-1.8.2, and that is what a bare `jq` resolves to from a subprocess. **No tool was installed or updated**; pacman was not used.

## Per-file totals (the 12 dispatch-schema files)

| File (under `.ufo/waves/`) | Members | Parsed trailers | Unparsed | Present | Empty | Missing | Misrooted | Name flag |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| round-13/w1-dispatch.json | 32 | 32 | 0 | 32 | 0 | 0 | 0 | no |
| round-14/w1-dispatch.json | 32 | 32 | 0 | 32 | 0 | 0 | 0 | no |
| round-15/w1-dispatch.json | 64 | 64 | 0 | 64 | 0 | 0 | 0 | no |
| round-16/w1-dispatch.json | 65 | 65 | 0 | 63 | 0 | 2 | 0 | no |
| round-16/w2-dispatch.json | 79 | 79 | 0 | 78 | 0 | 1 | 0 | no |
| round-17/w1-dispatch.json | 78 | 78 | 0 | 78 | 0 | 0 | 0 | no |
| round-17/w2-dispatch.json | 71 | 71 | 0 | 43 | 0 | 28 | 0 | no |
| round-18/w1-dispatch.json | 91 | 91 | 0 | 91 | 0 | 0 | 0 | no |
| round-18/w2-dispatch.json | 79 | 79 | 0 | 79 | 0 | 0 | 0 | no |
| round-20/final-dispatch.json | 64 | 64 | 0 | 63 | 0 | 1 | 1 | no |
| round-20/recovery-dispatch.json | 64 | 64 | 0 | 39 | 0 | 25 | 0 | no |
| round-20/w1-dispatch.json | 64 | 64 | 0 | 0 | 0 | 64 | 0 | no |
| **Lane total (12 files)** | **783** | **783** | **0** | **662** | **0** | **121** | **1** | **0 of 12** |

Notes: "Missing" includes the 1 misrooted entry. In all 12 files, `counts.total` = members = tasks, task names equal the member keys, and `resumeSends` is empty. Every trailer sits under the file's `registry.reportDir`. No trailer appears in the shared `taskCall.context`, `note`, or `policy`.

## Lane totals (55 JSON under `.ufo/waves`)

- 12 `ufo-swarm-wave-dispatch-v1` (the table above)
- 15 `ufo-swarm-registry-v1`
- 1 `ufo-swarm-wave-v1` (`round-20/w1-plan.json`, not a dispatch schema)
- 27 with no `schema` key (specs, assignments, start/attempt logs, `round-18/dead-seats.json`, `round-15/w2-skipped.json`)
- Members 783 = tasks 783 = parsed trailers 783; unparsed 0; multi-trailer 0; bad form 0
- Lane root: 662 present, 0 empty, 121 missing (of which 1 misrooted)
- Misrooted: 1
- Name flag: 0 of 12

## Findings

### F1. Misrooted: `round-20/final-dispatch.json`, member `AuditCase07`
- Trailer: `.ufo/waves/round-20/final/AuditCase07.md`
- Lane root: missing.
- Fleet root: `/home/vgpnk/Projects/shokunin/.ufo/waves/round-20/final/AuditCase07.md` exists, 8,784 bytes. Its header is `# AuditCase07: round-20 C1 case \`deliver-exact-patch\` (source-only falsifier)`.
- [INFERENCE] The report was written under the fleet root by mistake.
- Basename search over the whole fleet `.ufo/waves` (1,954 files) found this one copy and no other.

### F2. `round-20/w1`: spawned, but 0 of 64 reports on disk
- `round-20/w1-started.json` text: "Spawned 64 background agents…". Its 64 job names equal the 64 `registry.members` of `round-20/w1-dispatch.json` (64 of 64 match).
- The lane directory `round-20/w1/` contains only `swarm-registry.json`.
- Basename search over lane and fleet `.ufo/waves` finds 63 of the 64 names nowhere. `ScoutS038` exists only at `round-19/w1/ScoutS038.md` (see F4).
- Classification: dispatched and unsettled. This is not a never-dispatched case.

### F3. Never-dispatched evidence
- Filename criterion: none of the 12 names contains `preview`, `undispatched`, or `validation`. Result: 0 of 12 flagged.
- Content cross-check, round 20: the spawn records match the dispatch member sets exactly (64 of 64 each).
  - `w1-started.json` ↔ `w1-dispatch.json`
  - `final-attempt-1.json` ↔ `final-dispatch.json`
  - `recovery-attempt-4.json` ↔ `recovery-dispatch.json`
- Recovery start failures: `recovery-started.json` and `recovery-attempt-2.json` / `recovery-attempt-3.json` each record "Failed to start background task jobs … Background job limit reached (100)". `recovery-attempt-4.json` spawned 64.
- The only explicit never-dispatched record in the lane is `round-15/w2-skipped.json` (no `schema` key, so outside the 12): `planned_seats: 32`, `dispatched_seats: 0`, `status: "skipped-by-operator-wrapup"`. No round-15 w2 dispatch file exists.
- Registry `agentId` is null for all 783 members across all 12 files, so it is not a dispatch receipt.
- The spawn state of the other 9 dispatch files is unobserved. Their reports are present in most cases, which [INFERENCE] suggests they ran.
- Round 19 has no dispatch-schema file (only `w1-spec.json`, `w1b-spec.json`, `w2-spec.json`, and `w1/swarm-registry.json`). Its dispatch state is unobserved [INFERENCE].

### F4. Basename collisions: a basename-only check would overcount
- `round-17/w2` `RerunGateReplays` → `round-18/w2/RerunGateReplays.md` (3,808 bytes). A different round, so classed missing here.
- `round-17/w2` `RevQualityRows` → `round-18/w2/RevQualityRows.md` (7,718 bytes). Classed missing here.
- `round-20/w1` `ScoutS038` → `round-19/w1/ScoutS038.md` (5,082 bytes). Classed missing here.

### F5. Parser hazards
- 90 task lines across the 12 files contain "Report" but are not trailers (for example, "Report only, no shared docs.").
- One inline `Report:` sits inside a task body. It is in `round-18/w1`, task `ScoutFrontier`: "…Report: which frontier row (F1..) or province surface…". Line-start anchoring excludes it; a substring match would count it.

### F6. Unreferenced files in trailer directories (not counted)
- `round-17/w2`: `GateExactIds.md`.
- `round-18/w1`: 27 files that no trailer targets (`*.patch`, `*Fix.md`, `MatrixR18.run-matrix.py`).

### F7. Other observations
- Present reports range from 1,457 to 170,776 bytes. None is under 200 bytes.
- Basename integrity: all 783 trailer basenames equal `<member>.md`, so no missing count is a parse artifact.

## Missing trailer targets by file

- round-16/w1 (2): PreservationRepin, SentinelStoreAccess
- round-16/w2 (1): SentinelCensusFinal
- round-17/w2 (28): FixtureOracleD1, FixtureOracleD2, MutateCensusD1, RevEmitSoftDiag, RevCensusHeaderTruth, RerunCensusSelftest, RevVProbeRows, RevRelativeRow, RerunJjFixture, RevJjNovelIdentical, RevJjNovelPaths, RevForEachRefExclude, RerunReceiptSelftests, RevQuarantineRunbook, RevVadv54Harness, RevStubReceipt, RevKnowledgeEntry, RerunGateReplays, RevFrozenRegenerated, RevLessonMistakesDraft, RevQualityRows, RevScorecardDraft, RevOpenResidualTable, RevD5D7Lines, ConnSiblingAdjacency2, RevOperatorSweepFp2, RevMisrootSweep, RevHelperPhantomOrder
- round-20/final (1): AuditCase07 (misrooted, F1)
- round-20/recovery (25): GrantReport, GrantJson, GrantTsv, GrantOwnOnly, GrantScratchW2, GrantSymlinkLimits, ReceiptDrift, SignalClassification, RelativeTargets, InputHelper, InputR13Corpus, InputR13History, InputGitEnv, InputRevision, Counter13, Counter14, ConsumerScorecard, ConsumerLog, SourceAdmit, SourceRevParse, SourceCuration, RejectionLearning, WaveAccounting, ClaimNoTrade, ErrataBinding
- round-20/w1 (64): every member of the dispatch. The full list is in `trailers.tsv` (rows with class `missing`).

## Cross-checks performed

- jq and stdlib `json` agree on member count, task count, `counts.total`, and name sets for all 12 files.
- Trailer pairs (file, member, path): jq 783 = stdlib 783, set-equal.
- Presence: `os.lexists` / `os.stat` (662 present, 121 missing) and per-directory `os.listdir` agree.
- Misroot: basename search over lane `.ufo/waves` (818 files) found 3 cross-round collisions (F4). Over fleet `.ufo/waves` (1,954 files) it found 1 hit (F1).

## Limits

- "Present" means non-empty. Report content was not judged for settlement.
- Misroot was checked only against `/home/vgpnk/Projects/shokunin/<rel>`, as specified. `/var/tmp` and seat worktrees were not searched.
- The spawn-state cross-check covers only the 3 round-20 dispatches and the round-15 w2 skip record. Other dispatches are inferred from report presence [INFERENCE].
- The fleet root was read only: directory entries under `.ufo/waves`, plus the first 160 bytes of one file.

## Bounds

- Lane: read-only. No edits, no git or jj, no subagents.
- Writes: this report, plus `mori-shokunin/.ufo/waves/round-20/build/GtLaneSouji/trailers.tsv`.
- Not run: `tools/mori-census.sh`, `tools/mori-wave-settlement.py`, builds, linters, or lane tests.
- Not opened: retained transcripts or `~/.omp` session logs.
- Installs or updates: none.
