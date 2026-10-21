# RedactSessionExitCorrelation — round-18 redaction draft for SessionExitCorrelation.md

Seat: `MoriR18Recovery.RedactSessionExitCorrelation` (leaf; no subagent dispatch; no VCS mutation; no file written except this report).

## Behavior

Read the round-17 original of `.ufo/waves/round-17/build/SessionExitCorrelation.md` at 29b0dc7 (read-only `git show`), the spot-check routing at `corpus/lessons/round-17-verifier-spotcheck.md:322-350` and `:388-397`, and the frozen C1 policy `.ufo/waves/round-18/frozen/c1-policy.json`. Drafted a minimized replacement body (below, under `## Replacement`). It keeps the seat identity, task, verdict-level conclusions, non-private counts, the INFERENCE label, and a provenance line. It withholds all private values. The lane file itself was not written; the L1 integrates.

## Gates

- Provenance: original blob `61578ee9ad2204e8c4d5c93e778668bc9e583aee` (`git rev-parse 29b0dc7:.ufo/waves/round-17/build/SessionExitCorrelation.md`); SHA-256 of blob content `437b902fbc1c74174e06549a107e2dfbab315d8bca0dcfc55dde36175a57a7bf` (`git show ... | sha256sum`, rc 0).
- Scan of the original blob against every C1 class (python `re`, per-line, UTF-8 decode with errors=replace; counts only, no matched text printed):
  - R1 session_identity: 1 line
  - R2 session_store_path: 1 line
  - R3 tool_output_artifact: 0
  - R4 private_document: 0
  - R5 shell_history: 0
  - R6 privileged_config: 0
  - R7 operator_config_ref: 0
  - R8 routing_table_key: 0
  - R9 session_record_value: 3 lines
- Scan of the draft replacement body against every class (python `re` on the exact body text, same method): **R1 0, R2 0, R3 0, R4 0, R5 0, R6 0, R7 0, R8 0, R9 0; total 0.**
- Post-write scan of this report file: see `## Self-scan` below.
- The draft contains no session directory names, no numbered tool-log names, no document references, no history references, no privileged-config reference, no config line numbers, and no model routing or provider values.

## Touched surfaces

- Written: this report only, `.ufo/waves/round-18/build/RedactSessionExitCorrelation.md`.
- Read: lane file at 29b0dc7 (via `git show`); lesson lines `corpus/lessons/round-17-verifier-spotcheck.md:322-350` and `:388-397`; `.ufo/waves/round-18/frozen/c1-policy.json`.
- Not touched: lane checkout, MANIFEST, `.ufo/state`, sibling lanes, OMP configuration, any session store, any clone.

## Findings

- The original retains: a session-directory identity (R1 hit), a session-store path (R2 hit), and three lines of non-allowlisted custom-record field values (R9 hits). The lesson's routing (`:339-346`) matches what the scan shows for this file.
- The replacement carries the same verdict-level answers as the original: 168/168 error-terminal seats carry a disposal marker; 75 of 2197 completed seats lack one (all open or in flight); `aborted` 80/80 carry a marker; `incomplete` 5/64 carry one. Also retained: the 4 resume files, multi-marker counts, drift counts, tail-window caveat count, the advisory reading, and the INFERENCE label on `dead_*` irreversibility.
- Withheld from the replacement (private or non-allowlisted): session-directory name and path; per-file names and record indices; lane names (replaced by a lane count); per-provider and per-model breakdown (omitted); error-text prefix (replaced by a class count); error-code digits (replaced by presence counts); the verbatim question (paraphrased); the constant values of the disposal-detail fields (withheld by name-free description).
- The replacement reports only counts that the original already reported as counts; no new claims were added.

## Out-of-scope / residual risk (not decided here)

- R-class regexes are a recall floor, not a privacy proof (c1-policy `known_limit`). The reading sweep of the replacement found no further private context, but that is a reading, not a proof.
- Already-pushed history still carries the original; exposure assessment and any history action belong to the operator/kagi. This draft does not rewrite history or authorize rotation.
- Other must-redact files (`PacmanActorTrace.md`, `OmpRetryConfig.md`) and the lesson file are out of this seat's assignment.

## Commands run (all read-only)

- `git -C <lane> show 29b0dc7:.ufo/waves/round-17/build/SessionExitCorrelation.md | cat -n` — rc 0
- `git -C <lane> rev-parse 29b0dc7:.ufo/waves/round-17/build/SessionExitCorrelation.md` — rc 0; output `61578ee9ad2204e8c4d5c93e778668bc9e583aee`
- `git show ... | sha256sum` — rc 0; `437b902fbc1c74174e06549a107e2dfbab315d8bca0dcfc55dde36175a57a7bf`
- `cat .ufo/waves/round-18/frozen/c1-policy.json` — rc 0
- `read` of `corpus/lessons/round-17-verifier-spotcheck.md:322-350` and `:388-397`
- In-process python: loaded the frozen class regexes and scanned the original blob and the draft body per line; counts above. No file written, no scratch, nothing under /tmp.

Tool installs/upgrades: none. No pacman, no journal query, no VCS mutation.

## Replacement

```text
# SessionExitCorrelation — terminal message class × disposal marker

Seat: `MoriR17.SessionExitCorrelation-5` (leaf, advisory; no subagent dispatch, no VCS mutation).

Privacy repair (round-18). The round-17 original of this file retained non-allowlisted custom-record field values, a session-directory identity and per-file identifiers. This replacement keeps the seat's question, method, counts and conclusions and withholds every private value. Provenance: original blob `61578ee9ad2204e8c4d5c93e778668bc9e583aee` (`git rev-parse 29b0dc7:.ufo/waves/round-17/build/SessionExitCorrelation.md`), SHA-256 `437b902fbc1c74174e06549a107e2dfbab315d8bca0dcfc55dde36175a57a7bf` of the blob content. Git history remains the record of the original.

Question (paraphrased; the verbatim wording named a session directory and is withheld): for one assigned session directory, cross-tabulate the terminal message class (contract.md) with the disposal marker (the last `session_exit` custom record) per file. Does any error-terminal seat show a disposal marker, or any stop-terminal seat lack one? Counts only.

## Scope and snapshot

- Sessions directory: one OMP session directory of one project (path withheld; identify it by the provenance blob). It holds 109 top-level `*.jsonl` transcripts, 24 lane subdirectories, and two further subdirectories with no `*.jsonl`.
- The corpus is live. Pinned snapshot window T0 = 2026-10-20T18:58:49.194Z to T1 = 18:58:54.205Z, 2509 `*.jsonl` files, each read once and parsed in one pass, so per-file counts and classes are mutually consistent.
- Reproduction requires a re-read; counts move minute to minute. Drift measured across two passes is reported below and is part of the finding.

## Method

- Terminal class: exact replica of the contract.md C1 rules on the last `type=="message"` record with a dict `message`: `completed` (assistant, stop), `aborted` (assistant, aborted), `dead_rate_limit` (assistant, error, and `errorStatus==429` or an errorMessage class token from the contract list), `dead_quota` (next, quota-class token from the contract list), `dead_error_other`, `incomplete` (role toolResult or user, or any other assistant stopReason), `unavailable` (no message record).
- Disposal side: the last `type=="custom"` record with `customType=="session_exit"` in the same file. Only the record's two disposal-detail fields were consulted, plus `errorStatus`, the contract's errorMessage class tokens, and error-code presence. Values of the disposal-detail fields are withheld here (non-allowlisted session-record values). No message content, usage, or error text is reproduced.
- Full-file scan for both sides; the tail-window consequence is quantified separately.

## Cross-tabulation (pinned snapshot, 2509 files)

Disposal markers found: 2428 records over 2375 files. The disposal-detail fields carry one constant value across all 2428 records (value withheld), so the cross-tab collapses to presence or absence.

| terminal class | files | last marker present | marker with the constant value | no marker |
|---|---:|---:|---:|---:|
| `completed`   | 2197 | 2122 | 2122 | **75** |
| `aborted`     |   80 |   80 |   80 | 0 |
| `dead_rate_limit` | 166 | 166 | 166 | 0 |
| `dead_quota`  |    2 |    2 |    2 | 0 |
| `dead_error_other` | 0 | 0 | 0 | 0 |
| `incomplete`  |   64 |    5 |    5 | 59 |
| `unavailable` |    0 |    0 | 0 | 0 |
| **total**     | **2509** | **2375** | **2375** | **134** |

Marker multiplicity per file: 0 in 134 files, 1 in 2330, 2 in 37, 3 in 8 (max 3). Markers that are the file's final record: 2371 of 2428 (2375 files minus the 4 resume cases below).

## Answers (counts)

1. **Error-terminal seat showing a disposal marker: YES, 168 of 168 (100%).** `dead_rate_limit` 166/166 and `dead_quota` 2/2. In every one of the 168 the marker is the file's final record, positioned after the terminal error message.
   Dead-seat field aggregates (contract fields only): `errorStatus` 429 in 153, null in 15; error-text class prefix (text withheld) in 119; error code present in 122, absent in 46. Per-provider and per-model counts are omitted (session-record values).
2. **Stop-terminal seat lacking a marker: YES, 75 of 2197 `completed` (3.4%).** All 75 are open or in flight: 16 with mtime within 1 minute of the snapshot, 59 within 10 minutes, none older than 7 minutes. They span three lanes (lane names withheld). One example transcript has 64 records, a final message of assistant/stop, and zero markers.
3. Bonus counts on the same axis: `aborted` shows a marker in 80/80 files even though the terminal record is stopReason aborted. `incomplete` shows a marker in 5 of 64 files; in those 5 the marker was written after a toolResult or user terminal record, i.e. disposal can be recorded mid-turn.

## Falsifiers of "the disposal marker marks the end of a seat"

- 4 files have message records after their last marker: the seat resumed after disposal. Two of the four end in the `incomplete` class; one of the four holds three markers.
- Multi-marker files: 45 files hold 2 or 3 markers (37 with 2, 8 with 3), all with identical constant values. "The last" marker is therefore a per-file choice, and earlier ones are historical.
- Drift across two passes about 2 minutes apart (2508 to 2509 files): 34 seats flipped `incomplete` to `completed`; 56 files gained exactly one marker (presence only, never lost); 0 seats moved out of `dead_rate_limit` or `dead_quota`, and 0 out of `completed`, in that window. Total no-marker files fell from 190 to 134 while `completed`-without-marker rose from 48 to 75 (new turns finish faster than sessions dispose).
- Tail-window caveat: with the C1 default tail of 262144 bytes, the last marker falls outside the tail in 3 of 2375 files. All three are large and resumed. A tail-only reader would report them as having no marker at all. On the terminal-message side the 256 KiB tail changed the class of 0 of 2509 files versus a full-file scan (both passes).

## Reading for C1 (advisory, not a verdict)

- The disposal-detail fields are constant across all 2428 records. They record process disposal, not outcome. They cannot discriminate completion from rate-limit death, and must not be used as an outcome signal, for example never as a clean-shutdown predicate in a seat-health tool.
- Presence of a marker is a reasonable "this transcript has been disposed at least once" marker, nothing stronger: 168 error-terminal seats are disposed, 75 stop-terminal seats are not disposed, and 4 seats continue after a disposal.
- The C1 tool's `dead_*` classes do not encode resumability. The two-minute drift shows `incomplete` to `completed` is common and `dead_*` to other classes was not observed in that window [INFERENCE: a longer window would be needed to certify `dead_*` irreversibility; not observed here].

## Limits / remaining unknowns

- Single session directory of one project under one OMP runtime. Other directories and projects were not scanned, so the absence of other disposal-field values globally is not established.
- Counts are a moving snapshot of a live corpus; the tables are valid for T0 to T1 only.
- Files with zero parseable message records: 0 (`unavailable` = 0), so no class was guessed.
- Terminal class was taken from the last message record in the whole file; equality with the tail-window rule was measured (0 divergences), but only for this snapshot.
- The original copy printed non-allowlisted field values; this replacement withholds them. Error text, content and usage were not reproduced here.

## Commands run (read-only) and tooling

- Directory listing of the assigned session directory; counts of top-level transcript files (2509 total) and of disposal-marker occurrences (2428); per-file filter. All rc 0.
- Parsing and classification in-process, reading each file once. No scripts or artifacts written, nothing under /tmp, no writes outside the report.
- Tool installs or upgrades: none. No pacman, no VCS command, no journal query.
```

## Self-scan

Python `re`, per line, all nine frozen C1 classes, run on this file after the write: R1 0, R2 0, R3 0, R4 0, R5 0, R6 0, R7 0, R8 0, R9 0; total 0. The embedded replacement body is byte-identical to the scanned draft (7983 bytes, sha256 fcacbcc60ad8b4c8c30c074b1005d6993d653a9c9d8d0ca941028fc69daf6765).
