# RetryRecoveryShape — `message.retryRecovery` schema and the seat terminal rule

Seat: `MoriR17.RetryRecoveryShape-5` (scout, round 17 wave 1). Assignment: for the OMP session
directory named below, report (a) the key schema and value types of `message.retryRecovery`
without any text values, (b) how often an error record is followed by a later assistant stop in
the same file, and (c) whether "last message record" is the right terminal rule for C1's
`mori-seat-terminal.py`, with counts.

Target directory (read-only):

```
<session-store path withheld>
```

All `<file>:<line>` citations below are relative to that directory; line numbers are 1-based
`*.jsonl` line numbers.

## Method and field discipline

- Read-only scans with Python 3 stdlib `json` through the eval device; each full pass over all
  files took < 0.5 s. `ls -la <dir>` and `ls -1 *.jsonl | wc -l` via bash, rc 0.
- Only the allowed fields were extracted: `type`, `customType`, `message.role`,
  `message.stopReason`, `message.errorStatus`, `message.provider`, `message.model`, the
  contract's class tokens in `message.errorMessage`, and the `retryRecovery` key shape.
  No `content`, `usage`, `errorMessage` text or any other field was read out or printed.
  Text-valued `retryRecovery` members are reported as **cardinality only**.
- No writes outside this report; no tool installs (nothing needed); no VCS/jj commands; no
  journal, no pacman, no background work.

## Corpus at snapshot time (observation)

| pass | UTC time | `*.jsonl` | message records |
|---|---|---|---|
| first pass (this seat) | ~18:5x | 109 | 15,612 |
| scan A | 18:56:22Z | 110 | 15,688 |
| scan B | 18:56:36Z | 110 | — |
| consolidated | 18:56:52Z | 110 | 15,734 |

The directory is **live**. It is not a frozen corpus:

- 5/110 files grew between 18:56:22Z and 18:56:36Z (14 s): `KaidokuR19.jsonl` +23,900 B,
  `MadoR19.jsonl` +5,143 B, `RuntimeRevivedCompletion-2.jsonl` +8,938 B,
  `SoujiR17-3.jsonl` +26,096 B, `TsukuroiR18-2.jsonl` +64,868 B; by 18:56:52Z the deltas were
  +41,615 / +12,761 / +22,171 / +64,431 / +258,370 B.
- One file appeared between the first pass and scan A (109 → 110).
- Three files whose last message record was `assistant`/`error` at the first pass had appended
  records by scan A (see §2). Their terminal class flipped `dead_rate_limit` → `incomplete`.

Confidence: high for every count; all counts are snapshots at the stated timestamp.

## 1. `message.retryRecovery` — key schema and value types (no text values)

Present in **54** message records across **18** files. In all 54: `message.role == "assistant"`
and `message.stopReason == "error"` (0/54 on any other role, 0/54 on any non-error record, 0/54
on any *terminal* record). Key set is identical in all 54 occurrences:

```
(attempt, kind, note, recoveredAt, recovery, status, supersededBy)
```

| key | JSON type | cardinality / domain | notes |
|---|---|---|---|
| `attempt` | int | 4 distinct: `1`×27, `2`×12, `3`×9, `4`×6 | retry-cascade depth |
| `kind` | str | 1 distinct | constant across all 54 (text not read) |
| `note` | str | 3 distinct | short comment strings |
| `recoveredAt` | str | 27 distinct | timestamp-shaped strings (string, not number) |
| `recovery` | str | 2 distinct | enum-like |
| `status` | str | 1 distinct | constant across all 54 |
| `supersededBy` | dict | 1 shape, always exactly 4 keys | see below |

`supersededBy` nested schema (54/54 identical):

| nested key | JSON type | domain |
|---|---|---|
| `model` | str | text, not read |
| `provider` | str | text, not read |
| `responseId` | str | opaque id, not read |
| `timestamp` | int | epoch-ms, range 1792506861887 … 1792522301090, 25 distinct |

No arrays, booleans, or nulls anywhere in the value; no optional keys; no per-provider shape
variation in this corpus.

Representative records: `JjLaneHelperV2-2.jsonl:65,84,470`;
`JjTrialChousa-2.jsonl:125,126,127`.

Interpretation (observed, not inferred): `retryRecovery` is attached to an error record that has
been **superseded by a later response** (`supersededBy.responseId` + `timestamp`). It is not a
death marker and it is never present on a terminal record — the tool's C1 `retry_exhausted`
output is a different datum (see §2). One pass also showed 4/54 `retryRecovery` errors with no
later `assistant`/`stop` (continuation was `toolUse`-only), so `retryRecovery` ≠ "finished".

## 2. Error records and later assistant stop (counts)

Message records at 18:56:52Z: 15,734. Role/stop distribution from the 18:56:36Z pass (15,706
message records): roles `toolResult` 8,705, `assistant` 6,867, `user` 133, `custom` 1 (a single
`message.role == "custom"` record with null `stopReason`; generator unknown; never terminal);
stop reasons `toolUse` 6,679, `stop` 118, `error` 70, null 8,839.

Error records = `role == "assistant"` ∧ `stopReason == "error"`: **70 records in 24 files**.

| measure | count | share |
|---|---|---|
| followed by a later assistant `stop` in the same file | **63** | 63/70 = 90.0 % |
| followed by any later assistant message (any stopReason) | 70 | 100 % (67/70 at first pass) |
| followed by no later message at all | 0 | 0 % (3/70 at first pass) |
| files with ≥1 error and ≥1 later assistant stop | **17 of 24** | 70.8 % |

Record immediately after an error (70 events):

| next message record | count | share |
|---|---|---|
| `assistant` / `error` (retry cascade) | 37 | 52.9 % |
| `assistant` / `toolUse` (work continues) | 31 | 44.3 % |
| `assistant` / `stop` (clean recovery) | 2 | 2.9 % |
| none (error was last record) | 0 | 0 % |

Terminal-error observations from this seat's earlier passes (all three had **no** later message
then; all three have appended records now):

- `KaidokuR19.jsonl:125` — now followed by `toolUse`/`toolResult` records.
- `SoujiR17-3.jsonl:466` — now followed by `toolUse` records and a `session_exit` at line 467.
- `TabiR18.jsonl:102` — now followed by `toolUse` records and a `session_exit` at line 103.

So an `assistant`/`error` record is terminal in well under 5 % of observations even in a corpus
that includes real rate-limit death: 70 error records, 3 that were momentarily terminal, 0 at the
current EOF.

Classification tokens over the 70 error records (contract ordering: rate-limit before quota):

| signal | count |
|---|---|
| `errorStatus == 429` (int) | 24 / 70 |
| `errorStatus` null | 46 / 70 |
| rate-limit token set matched in `errorMessage` | **70 / 70** |
| quota token set matched | 3 / 70 |
| both rate-limit and quota tokens (ordering decides) | 3 / 70 (4.3 %) |
| `errorMessage` non-empty | 70 / 70 |
| prefix `Retry budget exhausted` | **0 / 70** |
| `stopReason == "aborted"` anywhere in corpus | 0 (no pass observed one) |

Consequences for C1, observed: the `errorStatus == 429` test alone catches 34 % of rate-limit
errors; the token test is load-bearing. The rate-limit-before-quota ordering changes exactly 3
records here (all correctly rate-limit). `dead_quota`, `aborted` and `retry_exhausted` have zero
positive cases in this corpus — the contract's motivated "Retry budget exhausted" shape does not
appear in this directory.

## 3. Is "last message record" the right terminal rule? — variant counts

Snapshot 18:56:36Z, 110 files, one class per file:

| rule | completed | incomplete | dead_rate_limit | unavailable | verdict |
|---|---|---|---|---|---|
| **R1 last message record (contract)** | 100 | 10 | 0 | 0 | reference |
| R2 last record of any type | 3 | 6 | 0 | **101** | wrong: 101/110 lose all signal |
| R3 last assistant message (skip trailing toolResult/user) | 100 | 10 | 0 | 0 | identical to R1 here |
| R4 any error record → dead | 83 | 3 | **24** | 0 | wrong: 24 dead vs 0 terminal; every error is followed later by an assistant message, and 17 of the 24 files by an assistant `stop` |
| R5 any assistant stop → completed | 100 | 10 | 0 | 0 | identical to R1 here |

R2 fails because of the trailing record layout after the last message record (consolidated pass):

| trailing sequence after last message record | files |
|---|---|
| `custom:session_exit` | 97 |
| nothing (file ends on a message record) | 8 |
| `custom:tool_execution_start` | 3 |
| `custom:tool_execution_start`, `model_usage` | 2 |

`session_exit` is **not** a terminal signal either:

- 99/110 files carry a `session_exit`; 5 of them have message records **after** their first exit
  (`KaidokuR18.jsonl` exits at 285 and 698, `MadoR18.jsonl` at 292 and 472, `TsukuroiR17.jsonl` at
  362 and 851, `SoujiR17-3.jsonl` at 467, `TabiR18.jsonl` at 103) — i.e. the session resumed after
  an exit record.
- 2 of the 10 non-completed seats carry an exit (`SoujiR17-3.jsonl`, `TabiR18.jsonl`), so exit
  presence does not mean clean completion.
- 3 completed seats have **no** exit (`SmokeFlashCascade.jsonl`, `SmokeOpusCascade.jsonl`,
  `SmokeZflCascade.jsonl`).
- Class × exit flag: (completed, exit) 97, (completed, no exit) 3, (incomplete, no exit) 8,
  (incomplete, exit) 2.

Decision: **keep "last message record"** as the terminal rule. It is the only rule tested that
neither inflates deaths (R4: 24 vs 0) nor erases classification (R2: 101 unavailable). Two
qualifications, both cheap and observable:

1. Say "last **observed** message record at the EOF byte offset read", and emit/report the file
   size or offset and a scan timestamp. In this directory the class of 3 files changed between
   two passes minutes apart and 5/110 files grew in 14 s, so two scans' dead counts are not
   comparable and a dead count can go to zero on re-scan. The contract's stated limitation
   ("last observed state, not proof the session will never resume") is exactly right and is not
   hypothetical — it was the observed outcome for `SoujiR17-3`, `TabiR18`, `KaidokuR19`.
2. Because "last assistant message" (R3) is equal to R1 on all 110 files, the rule can be
   documented as "last message record" without losing the ability to distinguish a file that ends
   on `toolResult` (still working) from one that ends on `assistant`/`stop`. The 10 incomplete
   seats at the consolidated pass are 6 ending on `toolResult` and 4 on `assistant`/`toolUse`;
   none ends on `user`.

### Tail-window and parse hazards (advisory for C1)

- Largest last-message line observed: **16,162 B**, i.e. 16.2× headroom under the default
  `--max-tail-bytes 262144`. Largest line of any type: 332,457 B, a `custom_message` record that
  the record-type filter skips.
- 0/110 files lacked a final newline across 4 passes, so no torn tail was observed. Residual
  risk [INFERENCE]: a live append can tear the final line; the contract's "skip lines that fail"
  then silently falls back to the previous message record, which is usually `toolUse` → the seat
  reads `incomplete` instead of `dead_*`. Cheap, contract-compatible mitigation to consider:
  count skipped unparseable lines and report the count (or treat a newline-less final parse
  failure as `incomplete` rather than falling back).
- Dropping the first (possibly partial) line is safe here: every file's first record is `title`
  (110/110), never a message.

## Remaining unknowns

- Text values of `kind`, `status`, `recovery`, `note`, `supersededBy.model/provider/responseId`
  were deliberately not read; only cardinality is known. C1 does not need them (it emits
  `retry_exhausted`/`retries`/`error_code` from `errorMessage` instead).
- Whether the 3 resumed error-then-exit files are the *same* seat retrying or a restarted process
  is not decidable from the allowed fields; `session_exit` appearing *before* the next `toolUse`
  suggests process restart rather than retry [INFERENCE].
- Other session directories (other dates/providers) were not sampled; this corpus has a single
  `retryRecovery` shape, zero `Retry budget exhausted` prefixes, zero `aborted`, and one
  `message.role == "custom"` oddity whose emitter is unknown.
- The live seats' next record cannot be predicted; all 10 incomplete classifications are
  snapshots, not outcomes.

Tool installs/updates this seat: none (no package, uv/npx install, or binary added).
