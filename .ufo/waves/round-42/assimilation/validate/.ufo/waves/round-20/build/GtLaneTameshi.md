# GtLaneTameshi: C2 independent ground truth for tameshi-shokunin dispatch files

Seat: MoriR20.GtLaneTameshi (leaf; no subagents). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Scope: every `*.json` under `.ufo/waves` whose top-level `schema` is `ufo-swarm-wave-dispatch-v1`.
Status: complete. Read-only on the lane. No lane file, git index, or jj state touched. No tool installed or updated.

## 1. Method

- Census: 106 `*.json` under `tameshi-shokunin/.ufo/waves` (`*/*.json` and `*/*/*.json`). 0 unparseable. Top-level `schema` tally (jq, `.schema // "<no-schema-key>"`): `ufo-swarm-registry-v1` 28, `ufo-swarm-wave-dispatch-v1` 16, `ufo-swarm-wave-v1` 4, `tameshi-r20-original-seat-outcomes-v1` 1, no `schema` key 56, JSON array 1 (`round-18/w3/rereads.json`).
- jq: the persistent shell's `jq` is a builtin that reports `jaq 3.1.1`. `/usr/bin/jq` reports `jq-1.8.2`. The 16-file list and all counts were identical under both.
- Independent cross-check: Python 3 stdlib (`json`, `os.path`, `hashlib`) over the same 106 files reproduced the same 16-file list and member/trailer counts. Path existence, size, and misroot checks were done only in Python, since jq has no filesystem access.
- Member count = keys of `registry.members` (an object) = `counts.total` = length of `taskCall.tasks`. Parity holds in all 16 files.
- Report trailer = last non-empty line of each `taskCall.tasks[].task`. Parsed with `^Report: write your scoped findings to (\S+)$`.
- Lane status of a parsed path `p`: present = regular file, size > 0; empty = size 0; missing = absent. Path is `/home/vgpnk/Projects/shokunin/tameshi-shokunin/<p>`.
- Misrooted = lane status is not present and `/home/vgpnk/Projects/shokunin/<p>` exists.
- Filename flag = basename matches `preview|undispatched|validation` (case-insensitive).
- Per-member rows (965): `.ufo/waves/round-20/build/MoriR20.GtLaneTameshi/member-paths.tsv`. Per-file summary: `.../file-summary.tsv`. File list: `.../dispatch-v1-files.txt`.

## 2. Per-file totals

| # | Dispatch file (under `.ufo/waves/`) | wave | members | trailers parsed / unparsed | present | empty | missing | misrooted | filename flag |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | round-12/dispatch.json | tameshi-r12-w1 | 32 | 32 / 0 | 30 | 0 | 2 | 0 | no |
| 2 | round-12/dispatch-w2.json | tameshi-r12-w2 | 32 | 32 / 0 | 32 | 0 | 0 | 0 | no |
| 3 | round-13/dispatch.json | tameshi-r13-w1 | 32 | 32 / 0 | 32 | 0 | 0 | 0 | no |
| 4 | round-14/dispatch.json | tameshi-r14-w1 | 32 | 32 / 0 | 32 | 0 | 0 | 0 | no |
| 5 | round-15/dispatch1.json | tameshi-r15-w1 | 66 | 66 / 0 | 57 | 0 | 9 | 0 | no |
| 6 | round-15/dispatch2.json | tameshi-r15-w2 | 32 | 32 / 0 | 32 | 0 | 0 | 0 | no |
| 7 | round-16/dispatch1.json | tameshi-r16-w1 | 68 | 68 / 0 | 68 | 0 | 0 | 0 | no |
| 8 | round-16/dispatch2.json | tameshi-r16-w2 | 67 | 67 / 0 | 67 | 0 | 0 | 0 | no |
| 9 | round-17/dispatch1.json | tameshi-r17-w1 | 67 | 67 / 0 | 67 | 0 | 0 | 0 | no |
| 10 | round-17/dispatch2.json | tameshi-r17-w2 | 99 | 99 / 0 | 92 | 0 | 7 | 0 | no |
| 11 | round-18/dispatch1.json | tameshi-r18-w1 | 73 | 73 / 0 | 73 | 0 | 0 | 0 | no |
| 12 | round-18/dispatch2.json | tameshi-r18-w2 | 93 | 93 / 0 | 93 | 0 | 0 | 0 | no |
| 13 | round-19/run1.json | tameshi-r19-w1 | 64 | 64 / 0 | 64 | 0 | 0 | 0 | no |
| 14 | round-19/run2.json | tameshi-r19-w2 | 64 | 64 / 0 | 64 | 0 | 0 | 0 | no |
| 15 | round-20/run1.json | tameshi-r20-w1 | 72 | 72 / 0 | 27 | 0 | 45 | 0 | no |
| 16 | round-20/validation-current.json | tameshi-r20-w1 | 72 | 72 / 0 | 27 | 0 | 45 | 0 | **yes: `validation`** (see F1) |
| | **Lane total, 16 files** | | **965** | **965 / 0** | **857** | **0** | **108** | **0** | 1 file, 72 members |

Lane totals, deduplicated: 893 unique report paths (965 minus 72 shared by files 15 and 16). Of these, 830 present, 63 missing, 0 empty, 0 misrooted.

Trailer shape: all 965 trailers are the single form `Report: write your scoped findings to <path>`. All paths are relative, end in `.md`, and sit directly in their `registry.reportDir`. None are absolute.

## 3. Findings

### F1. `round-20/validation-current.json` is a byte-identical copy of `round-20/run1.json`
- SHA-256 of both (Python `hashlib`): `e44c144664ad2c78d84b3bf3b8584b97a33f68eb78b65267d299f6b5a7271b12`. Both 114,468 bytes. Byte comparison: identical.
- The filename is the only signal that this file was never dispatched. Its content is the run1 dispatch: same wave id `tameshi-r20-w1`, same registry path, `counts.spawn` = 72, the same 72 task objects (72 of 72 identical), and the same 72 report paths.
- Round-20's outcome records (`original-outcomes.json`, `outcomes.json`) list exactly the same 72 seat names as run1 (verified). They describe one round-20 w1 wave, so file 16 adds no separate seats.
- Treat file 16 as a duplicate of file 15. Nothing in the file itself shows it was sent separately. Summing all 16 files double-counts 72 members.
- Local mtimes (host is UTC-03:00): run1 04:43:23; validation-current 07:25:59. [INFERENCE: a later re-save or validation copy.]

### F2. Round-20 gaps reconcile to original outcomes
- `original-outcomes.json` (`tameshi-r20-original-seat-outcomes-v1`): completed 24, failed 48 (total 72). Its `unsolicited_peer_wakeups` lists `A01ProvRound19Ruler`, `B10HistRound19`, `D07WordingErratum`. These seats were originally failed and woke later.
- Disk: 27 present = 24 original completed + those 3 wakeups (set equality verified). 45 missing = 48 failed minus 3 wakeups. No original completion is missing on disk.
- Later snapshot `outcomes.json` (its own note says it is not the original verdict): completed 27, failed 45, `report_exists` true for 26. The single disagreement is A01: snapshot says `report_exists:false`. Disk has `A01ProvRound19Ruler.md` at 9,917 bytes, mtime 06:44:51, later than the snapshot file's mtime of 06:41:52.
- For settlement, "present on disk" (27) and "original completed" (24) differ by exactly these 3 wakeups.

### F3. Round-15 gaps match a recorded failure; one listed failure has a report on disk
- The 9 missing reports in file 5 are `ReconUsage`, `ReconClean`, `ReconMismatch`, `ReconControl`, `ReconMapping`, `ReconUnavailable`, `ReconTamper`, `ReconJSON`, `ReconTypes`. They are exactly the `TameshiR15.Recon*` entries in `round-15/failures.json` `failed_agent_ids`.
- `failures.json`: `observed_error` = "Cursor RATE_LIMITED_CHANGEABLE: Gemini monthly usage limit, reset 2026-11-18". `replacement_identities` = [].
- `failed_agent_ids` also lists `TameshiR15.SiblingOverlap` (10 entries in total). Its trailer report `round-15/w1/SiblingOverlap.md` is present: 15,292 bytes, mtime 05:05:06, about 3 minutes before `failures.json` (05:08:13). The disk fact is used in the counts. [INFERENCE: the report was written before the failure was recorded.]

### F4. Round-17 gaps: no status record found in the wave JSON set
- 7 missing reports in file 10: `RegistryProvenance`, `SentinelLanded`, `SentinelTraceEscape`, `CriticC1`, `CriticC2`, `CriticNoHarm`, `CriticSeparability`.
- `round-17/w2/swarm-registry.json` has no status field (member keys: agentId, item, kind, role). `round-17/spawn3-residual.json` holds only tasks RR1–RR8. No failure record was found among the wave JSON files. Cause not established. [INFERENCE: not recorded in these files.]
- Name collision, not a misplaced report: `CriticNoHarm` and `CriticSeparability` also exist at `round-18/w2/CriticNoHarm.md` (9,905 bytes) and `round-18/w2/CriticSeparability.md` (6,926 bytes). Those are the round-18 dispatch2 members' own trailer-matched reports. They are not counted for round-17.

### F5. Round-12 gaps: no status record found
- `ControlGate` and `BashWitness` (file 1, `round-12/w1/`) are missing. `round-12/record-result.json` and `round-12/w1/swarm-registry.json` carry no status field.
- `.ufo/evidence/round-12/ControlGate/` and `.ufo/evidence/round-12/BashWitness/` exist (glob-level observation; contents not opened). Cause not established.

### F6. No misrooted reports
- 0 of 965 relative paths exist under `/home/vgpnk/Projects/shokunin/`.
- A basename sweep of `/home/vgpnk/Projects/shokunin/.ufo` for the 63 unique missing basenames returned 0 hits.
- Body text: 199 absolute `.ufo/waves/*.md` mentions equal `lane + trailer`. 0 equal `fleet + trailer`.
- Other absolute mentions are read inputs, not report write targets:
  - file 14 (`round-19/run2.json`): 64 read targets, all `tameshi-shokunin/.ufo/waves/round-19/w1/*.md`, all present on disk.
  - files 9 and 10 (`round-17`): 4 and 1 reads of fleet-root `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditTameshi.md`.
  - file 11 (`round-18/dispatch1.json`): 31 mentions across 23 distinct targets: round-17 w1/w2 reports, round-18 `sources/` and `staged/` files. The staged output `round-18/staged/LEG8-INTEGRATION.md` exists (2,846 bytes).
  - file 8 (`round-16/dispatch2.json`): 1 glob read of `round-16/w1/CR*.md`.

### F7. Other checks
- Present files: 0 symlinks, 0 whitespace-only. Empty files: 0.
- Duplicate report paths within a file: 0. Across files: 72, all from the file 15 and file 16 pair.
- `counts.resume` = 0 and `resumeSends` = [] in all 16 files. All members are `kind: spawn`.
- Grep for `ufo-swarm-wave-dispatch-v1` across `.ufo/waves` matches only line 2 (top-level `schema`) of these 16 files. No nested decoys.
- Row pointers: `grep -n missing .ufo/waves/round-20/build/MoriR20.GtLaneTameshi/member-paths.tsv` lists all 108 missing entries.

## 4. Excluded near-misses (not dispatch-v1)
- `round-20/dispatch.json`: no `schema` key. Top-level keys: coordinator, frozen_contract_commit, gate_installation_not_before, original_readers_finished_observed_at, outcome_evidence, prior_attempt, registry_assigned_at, seats, timestamp_basis, timestamp_evidence, wave1, wave1_dispatched_at. Not counted; content not displayed beyond key names.
- `ufo-swarm-wave-v1` (4 files): `round-19/plan1.json`, `round-19/plan2.json`, `round-20/plan1.json`, `fleet-round-1-interactive/plan.stdout.json`.
- `round-20/original-outcomes.json` (`tameshi-r20-original-seat-outcomes-v1`), 28 `ufo-swarm-registry-v1` files, and `round-18/w3/rereads.json` (JSON array).
- `round-20/spawn-header.json` is session-header-shaped and sits under `.ufo/waves`. The census read it: a jq key listing, plus an in-memory parse for the schema tally. Only top-level key names and the absent schema value were displayed. It is not a dispatch file. Its content was not displayed or analyzed; the read is flagged because it may fall under the transcript bound.

## 5. Summary for the C2 oracle
- dispatch-v1 files: 16. Declared member entries: 965. Unique report paths: 893.
- Trailers parsed: 965. Unparsed: 0.
- Lane present: 857 entries (830 unique). Empty: 0. Missing: 108 entries (63 unique).
- Misrooted: 0. Both roots: 0.
- Filename-flagged: 1 file (`round-20/validation-current.json`, 72 entries, byte-identical to `round-20/run1.json`).
- Gap explanations: round-15 (9) explained by `failures.json`. Round-20 (45 per file) explained by `original-outcomes.json`. Round-12 (2) and round-17 (7) unexplained in the wave JSON set [INFERENCE: seats that wrote no report].

## 6. Limits
- "Present" means a non-empty regular file exists at the path. Content was not validated.
- dispatch-v1 has no "dispatched" field. "Never dispatched" uses the filename only, as specified.
- Timestamps are host-local (UTC-03:00).
- Nothing was run from the lane's own tooling. No `tools/mori-*` script was executed.

## 7. Tools and installs
- None installed or updated. Commands used: `jq` (builtin reporting jaq 3.1.1), `/usr/bin/jq` (jq-1.8.2), Python 3 stdlib (`json`, `os`, `glob`, `hashlib`, `os.stat`), `stat`, `grep`, `glob`, and read tools.
- Writes limited to this report and `.ufo/waves/round-20/build/MoriR20.GtLaneTameshi/` (3 scratch TSV/TXT files).
