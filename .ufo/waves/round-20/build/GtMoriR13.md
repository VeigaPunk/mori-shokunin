STATUS: complete

# GtMoriR13: manual ground truth, round-13 dispatch (wave `mori-r13-build`)

Seat GtMoriR13, leaf (no subagents). Read-only. Nothing was written outside this report. No installs or updates were performed. Ground truth uses `jq` and `ls`/`stat` only; comparison sources were read but not used to derive the status column.

Input: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-13/dispatch.json` (schema `ufo-swarm-wave-dispatch-v1`, `wave` = `mori-r13-build`).

Tool note: bare `jq` in this shell is a builtin (`jq --version` → `jaq 3.1.1`). The key extractions (names, trailers, last-line test, registry equality, counts, closure lookup) were re-run with `/usr/bin/jq` (`jq-1.8.2`). Results were identical.

## 1. Method and observed evidence

1. Names: `jq -r '.taskCall.tasks[] | .name'` gives 32 names, from CensusFix to OriginalIntent.
2. Trailer: `jq -r '.taskCall.tasks[] | .name + "|" + (.task | split("\n") | map(select(test("Report: write your scoped findings to"))) | last | sub("^Report: write your scoped findings to "; ""))'`.
   - 32/32 tasks have exactly one trailer line, and it is the last non-empty line of the task body (checked with both jq binaries).
   - Every path is `.ufo/waves/round-13/build/<Name>.md`. Regex `^\.ufo/waves/round-13/build/[A-Za-z]+\.md$` matched 32/32, so no stray whitespace.
3. Mori root, `stat -c '%F|%s|%n'` on `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-13/build/<Name>.md`:
   - 32 × `regular file`, sizes 5877 (ReviewPromotion.md) to 35632 (CountDesign.md) bytes, all > 0.
   - No `symbolic link`, no `regular empty file`, no `No such file`.
   - Parent components are real directories: `mori-shokunin`, `.ufo`, `.ufo/waves`, `.ufo/waves/round-13`, `.ufo/waves/round-13/build`.
4. Fleet root (misrooted check), `stat` on `/home/vgpnk/Projects/shokunin/.ufo/waves/round-13/build/<Name>.md`:
   - 32 × `No such file or directory`.
   - The directory `/home/vgpnk/Projects/shokunin/.ufo/waves/round-13/build` does not exist. Its parent `.ufo/waves/round-13` exists (directory, 1224 B). A listing of that parent shows only fleet-level round-13 artifacts (for example `closure-check.r13.py`, `PROTOCOL.compact.md`, `mutants/`, `fixtures/`), none named as a member.
5. Mori `build/` contents, `ls -la`: "33 files, 0 dirs (1 .json, 32 .md)". The 32 `.md` names equal the 32 dispatch names. The extra file is `swarm-registry.json`. No strays.
6. Registry check, `jq`: `dispatch.json` `.registry.members` keys, sorted, equal the sorted task names (`true`). `build/swarm-registry.json` `.members` keys, sorted, equal the sorted task names (`true`). The swarm-registry `reportDir` is `.ufo/waves/round-13/build`.

## 2. Table: name|status (dispatch order)

```
name|status
CensusFix|present
OracleFix|present
RegressionHarness|present
JournalKnowledge|present
HistoryKnowledge|present
JournalFixtureDesign|present
OracleFixtureDesign|present
CountDesign|present
JournalSource|present
CatalogSource|present
FieldsSource|present
PipeSource|present
PlanningWalk|present
PriorReview|present
ProtectedInventory|present
DriftScope|present
SiblingOverlap|present
ClaimConnections|present
SourceChain|present
FrontierConnection|present
ReviewCensus|present
ReviewOracle|present
ReviewEvidence|present
ReviewSources|present
ReviewPromotion|present
ClaimAttack|present
JSONAttack|present; mtime after closure (see A1)
VerdictAttack|present
EvidenceScribe|present
MistakeScribe|present
Safety|present; mtime after closure (see A1)
OriginalIntent|present
```

## 3. Totals

| metric | count |
|---|---|
| dispatched members (`taskCall.tasks[*].name`) | 32 |
| trailers extracted (exactly one per task, last non-empty line) | 32 |
| present (regular, non-symlink, > 0 B) | 32 |
| empty (regular, 0 B) | 0 |
| missing | 0 |
| symlink or other non-regular | 0 |
| misrooted (same relative path exists under fleet root) | 0 |
| path anomalies (regex mismatch, extra trailers) | 0 |
| total | 32 |

## 4. Recorded settlement or closure counts for round 13, compared with ground truth (32 / 0 / 0 / 0)

| # | source (read-only) | what it records for round 13 | agreement |
|---|---|---|---|
| a | `dispatch.json` `.counts` | `spawn` 32, `resume` 0, `total` 32 | total matches. Dispatch-side count, not settlement. |
| b | `dispatch.json` `.registry.members` | 32 keys, equal to task names (`true`) | matches |
| c | `build/swarm-registry.json` | 32 members, same names (`true`); roles connector 4, critic 3, executor 8, revenger 1, reviewer 5, scout 8, scribe 2, sentinel 1 (sum 32); `updatedAt` 2026-10-20T04:07:16.476Z; no per-member status or settled field | count matches. Registry never recorded completion (A2). |
| d | `LOG.md:729-730` | "One validated 32-seat batch"; "Eight executors, eight scouts, four connectors, five reviewers, three critics, two scribes, one sentinel, one revenger" (sum 32) | matches c |
| e | `LOG.md:756` | "One validated 32-seat wave completed" | total matches. No per-seat states. |
| f | `SCORECARD.md:658-759` (round-13 section) | no seat count. Axis table headed "outside closure pending" (`:689`). Outside closure: "rejected round 13 as harmed" (`:735-738`). | no count |
| g | `MANIFEST.json` `.rounds[327]` (round 13, `closure`, 2026-10-20) | "launch mori round=13" at 01:04:44-03:00; "complete mori round=13" at 01:43:25-03:00; "Real report 953c786c…"; no seat count | no per-seat count |
| h | `MANIFEST.json` `.rounds[339]` (round 14 closure) | routes debt "capture exact dirty-path scope for r13 preserved receipt" | no count |
| i | `wave*-settlement.json` for round 13 | none. `.ufo/waves/*/*settle*` returns only `round-19/wave1-settlement.json`, `round-19/wave2-settlement.json`, `round-17/wave-settlement.json`. | none recorded |
| j | `.ufo/waves/round-13/evidence/score-counts.json` | rubric counters (coverage 0→2, operability defects 2→0, 19 behavior passes, 2 mutation-red) | not a seat count |
| k | `.ufo/reports/round-13/` | absent. `.ufo/reports` lists round-2 to round-11 only. | none |
| l | `.ufo/waves/round-20/frozen/c2-expected.json` | 14 fixture cases (`all-present`, `misrooted`, …); none concerns round 13. Rule for `all-present`: exit 0, `settled`. | none (rule only) |
| x | `SCORECARD.md:807` "our 32 dispatched seats" | sits in the round-14 section (`### Round-14 measured result` at `:760`). Round-14 also has "all 32 seats completed" at `LOG.md:803-804`. | excluded, not round 13 |

Conclusion: no per-seat settlement or closure record exists for round 13. Every recorded total is 32 and agrees with 32 present, 0 empty, 0 missing, 0 misrooted. The recorded totals cannot separate settled from unsettled. [INFERENCE] Applying the c2 oracle's `all-present` rule to this wave gives exit 0, state `settled`, present 32, missing 0, empty 0, misrooted 0. This was not observed on round 13.

## 5. Anomalies

- A1. Two present reports have mtimes after the wave closed.
  - `JSONAttack.md`: 2026-10-21 05:55:54.223799935 -0300, 21457 B.
  - `Safety.md`: 2026-10-21 04:06:17.221160530 -0300, 20193 B.
  - Wave complete: 2026-10-20 01:43:25 -0300 (`MANIFEST.json` `.rounds[327]`).
  - The other 30 reports are between 2026-10-20 01:09:01.938922788 (CatalogSource.md) and 01:26:58.339373798 (CensusFix.md).
  - `build/` mtime is still 2026-10-20 01:25:18.660471643, so nothing was created or renamed in `build/` after that. Both files were rewritten in place [INFERENCE from directory mtime].
  - Cause not observed. Both pass the size rule. They would fail any check that requires writes inside the wave window.
- A2. `swarm-registry.json` `updatedAt` (01:07:16 -0300) precedes every report. The registry never recorded member completion.
- A3. Timeline, observed without interpretation: MANIFEST launch 01:04:44 -0300; `dispatch.json` last modified and registry `createdAt` both 01:06:53 -0300.

## 6. Caveats

- The broad glob `.ufo/**/*settlement*` timed out after 5 s, so it proves nothing. The narrowed glob `.ufo/waves/*/*settle*` completed. Round-13 absence also rests on listing the round-13 directory (`dispatch.json`, `spec.json`, `sources-*.json`, `build/`, `evidence/`, `frozen/`) and on the `evidence/` and `frozen/` listings. None contains a settlement file.
- A directory listing of `.ufo/waves/round-13` via the read tool omitted `build/`. `stat` and `ls` confirm it exists with 33 entries. This is a listing quirk, noted only.
- `ls` output format varied between calls, so exact sizes and types come from `stat -c`.
- Report contents were not opened. Status uses type, size and path only, as specified. Content quality is not assessed.
- Not run: `tools/mori-wave-settlement.py`, `tools/mori-census.sh`, builds, linters, and any git or jj command.
- Tooling record: no installs or updates (`jq` builtin jaq 3.1.1; cross-check binary `/usr/bin/jq` jq-1.8.2, pre-existing).
