# TranscriptShapes — key-only census of terminal records across every shokunin session transcript

Seat: `MoriR17.TranscriptShapes-5` (scout, leaf member, no subagent dispatch). Lane:
`/home/vgpnk/Projects/shokunin/mori-shokunin`, entering tip `24526ea9617cd020fee16c28fe4d4a2789dc28cb`.
Access date: 2026-10-20. This report is evidence for **C1** (`tools/mori-seat-terminal.py`,
"seat terminal-status capability") only. No edit, no judgment of the claim, no routing, no VCS
operation. Nothing written outside this report.

Installs/updates: **none**. No pacman, uv, npx, or binary download was needed or attempted.

## Method and field discipline

Target (read-only):

```
<session-store path withheld>
```

- Enumerated with `os.walk`, regular files ending `.jsonl`, symlinks skipped.
  **5084 files, 4,093,463,484 bytes (4.09 GB)**, depths 1/2/3 = 15/596/4473 files.
- Every file was read as a **byte-windowed tail mirroring the contract**: `seek(size-262144)`,
  `read()`; when the read did not start at byte 0 the first (partial) line was dropped exactly
  as `mori-seat-terminal.py` must. 4611 files were windowed on the first snapshot.
  Records are found by scanning the tail **backwards** and stopping at the first
  `type == "message"` record with a dict `message` (identical result to a forward scan of the
  window; the reverse form is what the tool should do, and it is ~50× cheaper).
- Field discipline: only `type`, `customType`, `message.role`, `message.stopReason`,
  `message.errorStatus`, `message.provider`, `message.model`, the contract's class tokens inside
  `message.errorMessage`, and `retryRecovery` key presence were read. No `content`, `usage`,
  `errorMessage` text, `data`, or any other field was printed or stored. All outputs below are
  counts, integers, provider/model strings, and class names.
- Commands: Python 3.14 stdlib `json` via the eval device (top-level `python3` in-window passes,
  rc 0, wall time per full corpus pass 0.66–0.8 s); `du -sh`, `find | wc -l` via bash, rc 0.
- LSP: not applicable — the artefact under study is a JSONL data corpus, not a source tree, so no
  language server answers these symbols. Grep-equivalent JSON probing is the direct evidence here;
  this is recorded rather than presented as semantic proof.

**The corpus is live and moved under the scan.** Numbers below are labelled by snapshot:

| snapshot | UTC | files | completed | incomplete | dead_rate_limit | aborted | dead_quota | unavailable |
|---|---|---|---|---|---|---|---|---|
| A | ~18:55Z | 5084 | 4375 | 287 | 264 | 117 | 29 | 12 |
| B | 19:00:14Z | 5085 | 4438 | 238 | 251 | 117 | 29 | 12 |
| C | 19:01:26Z | 5085 | 4452 | 224 | 251 | 117 | 29 | 12 |

Delta A→B in ~5 min: **+63 completed, −49 incomplete, −13 dead_rate_limit**, +1 new file; B→C in
72 s: **+14 completed, −14 incomplete**. See §7 R2. Snapshot C is the one used for every
"class × last-record" cross-tab below, so those tables are internally consistent.

## 1. Terminal record `(type, role, stopReason)` census

Snapshot A, one tuple per file for the **last** `message` record (seed 5084 files):

| terminal `type` | `role` | `stopReason` | files |
|---|---|---|---|
| `message` | `assistant` | `stop` | 4375 |
| `message` | `assistant` | `error` | 293 |
| `message` | `toolResult` | *(absent/None)* | 282 |
| `message` | `assistant` | `aborted` | 117 |
| *(no message record in tail)* | — | — | 12 |
| `message` | `assistant` | `toolUse` | 4 |
| `message` | `user` | *(absent/None)* | 1 |

Facts that matter for the contract:

- The observed `stopReason` vocabulary over the 5072 terminal records that exist is exactly
  `stop | error | aborted | toolUse | absent`. No other value occurs. The contract's class ladder
  covers every observed value; `dead_error_other` and any "other role" branch have **zero**
  terminal occurrences in this corpus.
- `role` at terminal is only `assistant | toolResult | user`. A `developer` role **does exist**
  mid-transcript (seen in
  `<session-id withheld>`) but never as a terminal
  record here. The contract has no rule for a `developer`-terminal transcript; implement a
  defensive fallthrough to `incomplete` rather than an unguarded `if/elif` that can crash.
- `toolResult` and `user` terminal records never carry a `stopReason`.

## 2. `errorStatus` values

Across all 5084 terminal records: `429` → **170**, `402` → **27**, absent → **4887**.
Type is `int` for all 197 present values (`NoneType` otherwise); **no string-typed status
occurs**, so `errorStatus == 429` is safe here — but see §5 for why the status test alone is
insufficient: 96 of 293 terminal errors carry **no** status at all.

## 3. `provider` / `model` of terminal errors (293 records, snapshot A)

| provider/model | terminal errors | resulting class |
|---|---|---|
| `zai/glm-5.3-flash` | 132 | 132 `dead_rate_limit` |
| `devin/swe-2` | 64 | 64 `dead_rate_limit` |
| `anthropic/claude-opus-5-5` | 30 | 30 `dead_rate_limit` |
| `charm-hyper/deepseek-v4.1-flash` | 27 | 27 `dead_quota` |
| `openai-codex/gpt-6-luna` | 24 | 24 `dead_rate_limit` |
| `anthropic/claude-haiku-5-5` | 7 | 7 `dead_rate_limit` |
| `openai-codex/gpt-6.1-sol` | 6 | 6 `dead_rate_limit` |
| `devin/gpt-6-1-sol` | 2 | 2 `dead_quota` |
| `cursor/claude-haiku-5-5` | 1 | 1 `dead_rate_limit` |

Totals: **264 `dead_rate_limit` + 29 `dead_quota` = 293** — i.e. every terminal error in the
corpus lands in a `dead_*` class; `dead_error_other` is empty. Largest provider groups
(terminal record, all classes) for calibration: `commandcode/deepseek/deepseek-v4.1-flash` 1109
(1084 completed / 25 aborted), `anthropic/claude-haiku-5-5` 872, `anthropic/claude-opus-5-5` 686,
`opencode-go/deepseek-v4.1-flash` 587, `devin/swe-2` 398, `openai-codex/gpt-6-luna` 332,
`zai/glm-5.3-flash` 188 (52 completed, 4 aborted, **132 dead**), `openai-codex/gpt-6.1-sol` 177,
`google-antigravity/gemini-3.8-flash` 143, `xai-oauth/grok-4.7` 90,
`xai-oauth/grok-composer-2.5-fast` 60, `charm-hyper/deepseek-v4.1-flash` 49,
`alibaba-token-plan/qwen3.8-flash` 20 (17 aborted), `devin/glm-5-3-flash-1m` 17.

`zai/glm-5.3-flash` is the single worst death ratio in the corpus (132/188 = 70 %).

## 4. Class-token matching, in contract order

Token multiset observed on the 293 terminal `errorMessage` values (`|` = same message):

| tokens matched | count | contract class |
|---|---|---|
| `429` + `Rate limit` | 132 | `dead_rate_limit` |
| `resource_exhausted` only | 63 | `dead_rate_limit` |
| `429` + `rate_limit` | 37 | `dead_rate_limit` |
| `rate_limit` only | 30 | `dead_rate_limit` |
| `402` + `credits` | 27 | `dead_quota` |
| `quota` only | 2 | `dead_quota` |
| `429` + `resource_exhausted` | 1 | `dead_rate_limit` |
| `RATE_LIMITED` + `usage limit` | 1 | **`dead_rate_limit`** (contract order) |

Findings:

- **Token matching is load-bearing, not a fallback.** 96/293 terminal errors (32.8 %) have
  `errorStatus` absent — 63 `resource_exhausted`, 30 `rate_limit`, 2 `quota`,
  1 `429|resource_exhausted`. An `errorStatus`-only implementation would report 96
  `dead_error_other`.
- **One record matches both families**: `RATE_LIMITED` + `usage limit`. The contract's stated
  order (rate-limit tested before quota) yields `dead_rate_limit`; a "usage limit" message is
  semantically a quota event for the operator reading the tally. Observed once, so the tally
  effect is 1 seat — but the *test order* is therefore observable in output, and must be tested
  by a fixture with exactly this shape.
- **`402` as a bare substring is the risky token** (request ids, byte counts, timestamps can
  contain `402`). Measured: every one of the 27 `402` matches also carries `errorStatus == 402`
  and `credits` — **zero spurious `402`-only hits in 5084 files**. Likewise `429` never appears
  without a real rate-limit context. So the substring rule is safe *at today's corpus*, not
  proven safe in general; a fixture with a numeric id containing `402` is the cheap falsifier.
- `resource_exhausted` (gRPC status) is the only rate-limit token for 63 records and never
  co-occurs with `quota` in this corpus, so the ordering hazard is currently latent, not active.

## 5. Retry-marker fidelity (`retry_exhausted`, `retries`, `error_code`)

Over the 293 terminal errors:

- `errorMessage` startswith `Retry budget exhausted` → **149** (50.9 %).
- `after N retries` present → **149**, and `N == 10` for **all 149** (matching the contract's
  quoted `Retry budget exhausted after 10 retries`; no other N occurs in the corpus).
- `(type=NNNN)` present → **122**, and the code is **`1302` for all 122** (the zai
  `429 ... (type=1302)` shape). 149 − 122 = 27 retry-exhausted messages carry no code token.
- `errorMessage` length: min 0, median 136, max 239 bytes — the `--max-tail-bytes` budget is
  never stressed by the message itself.

[INFERENCE] `retries` is effectively a constant here, so a fixture that varies `N` (e.g.
`after 3 retries`) is required or the parser's regex is untested against the general shape.

## 6. `retryRecovery` on terminal records

Key **presence** was checked without reading any value: `retryRecovery` is absent from
**5072/5072** terminal `message` records (4792 non-error + 280 error at that window), i.e.
**never** present. This is consistent with the sibling report `build/RetryRecoveryShape.md`
(which studies one session directory); this census extends the observation corpus-wide. It also
means `retryRecovery` cannot serve as a terminal-state anchor for C1 — the anchor has to stay the
last `message` record plus `errorMessage` tokens.

## 7. Misclassification risks, ranked

### R1 — Giant records defeat the tail window → false `unavailable` (observed, 11/12)

11 of the 12 `unavailable` files are **not** message-free. Each contains 29–120 message records
and, when scanned whole, ends on `assistant / stop / openai-codex / gpt-6-luna` → the correct
class is `completed`. They read `unavailable` only because a **single `custom` record larger than
262144 bytes** sits at the end of the file, so the whole window is one partial line:

| file | size | largest record (last 512 KiB) | true class |
|---|---|---|---|
| `W2RoundKagi.Critic-3.jsonl` | 1 651 323 | 464 352 | completed |
| `W2RoundMado-8.R12Critic-3.jsonl` | 1 832 798 | 362 478 | completed |
| `W2RoundGameDev3d.R108PreCritic-5.jsonl` | 1 223 887 | 356 298 | completed |
| `W2RoundTabi.TabiCritic2.jsonl` | 1 329 785 | 342 673 | completed |
| `W2RoundSouji-8.R12Critic.jsonl` | 1 726 619 | 314 032 | completed |
| `W2RoundGameDev2d.R105Critic.jsonl` | 1 170 115 | 267 594 | completed |
| `W2RoundKama.KamaCritic.jsonl` | 2 927 188 | 286 899 | completed |
| `W2RoundChousa.R24Planner-2.jsonl` | 2 123 339 | 287 331 | completed |
| `W2RoundTameshi.Critic-3.jsonl` | 2 690 950 | 330 570 | completed |
| `W2RoundGameDev3d.R108Planner-5.jsonl` | 2 140 685 | 301 080 | completed |
| `KaikokuSourcesR13.SourceCritic.jsonl` | 929 299 | 309 599 | completed |

The twelfth is genuinely message-free: the 785-byte
`<session-id withheld>` (0 records of type
`message`, only `session_init` / `thinking_level_change`).

**Measured fix (falsifier, already run):** escalating the window resolves them exactly —
window 262144 → 0/12 resolved; 524288 → 11/12; 1048576 → 11/12; and a 1 MiB window leaves
**0 of 4651** truncated files without a terminal message record. Corpus max record size in the
last 512 KiB is 464 352 bytes; p99 222 037, p95 163 200. So: on "no message record in window",
retry once with the window doubled (or 4×) before declaring `unavailable`; declare `unavailable`
only if the **whole file** has no `message` record. Cost is one extra read for ≤0.3 % of files.
As delivered today the tool under-reports `completed` by 11 and inflates `unavailable` from 1 to 12.

### R2 — The corpus drifts mid-scan; a `dead_*` verdict is not stable (observed, 13/293 in 5 min)

A second pass ~5 min after the first found 13 files that were `dead_rate_limit` at snapshot A and
are not error-terminal at snapshot B:

- 6 became `assistant / stop` → **recovered to `completed`** (all `zai/glm-5.3-flash`):
  `MoriR17.OverlapJjSiblings-5`, `MoriR17.RevengerCensusHead-5`, `MoriR17.ReviewC2Contract-5`,
  `MoriR17.ReviewC2Metric-5`, `MoriR17.ReviewScorecardRubric-5`, `MoriR17.ReviewSkillRows-5`.
- 7 now terminate on a record with **no** `stopReason` (i.e. a newer `toolResult`/`user` record was
  appended) → the seat **kept working after the rate-limit error**: `KaidokuR19`,
  `KamaR17.KQRowsReview`, `KamaR17.MistakesTable`, `KamaR17.RevengerR13Diff`,
  `KamaR17.RoutedDefects`, `SoujiR17-3`, `TabiR18`.
- Provider split of the drift: `zai/glm-5.3-flash` 10, `anthropic/claude-opus-5-5` 3. File mtimes
  of the drifted files were 1.2 s – 200 s old at snapshot B.

Consequences, all of them contract-visible:
1. `dead_rate_limit` must be documented as *"last observed state at scan time"* — the contract
   already says this in spirit, but the corpus shows a **whole-seat recovery rate of 13/264 ≈ 5 %
   inside 5 minutes**, which is not a theoretical nicety.
2. `retry_exhausted=True` does **not** imply death: the harness can fall back to another model
   (`resolvedModelIsFallback` exists on session records) and the seat continues. [INFERENCE] that
   fallback is the mechanism; the observed fact is error → later `stop`.
3. Two runs of the gate minutes apart are **not** comparable; a fixture-driven selftest is
   mandatory and a live-corpus rc1 is not a regression signal.
4. Six of the drifting seats are `-5` members of **this wave**, so a C1 run during round 17 also
   reports on seats that are still writing.

### R3 — `incomplete` conflates "running now" with "died mid-turn"

287 `incomplete` at snapshot A; **101 of them had mtime < 10 min** and only 4 were older than a
day. Prefix split of the fresh ones: `MoriR17` 60, `KamaR17` 32, `MadoR19` 4, `TameshiR17` 2,
plus 3 singletons. A terminal `toolResult`/`toolUse` record is the *normal* state of a live seat
between turns, so `incomplete` is dominated by live seats in an in-flight wave and cannot be read
as a death count. The contract's mandated `--help` caveat ("last observed state, not proof the
session will never resume") covers the semantics; the *tally* still invites the wrong reading.

**Validated liveness discriminator that costs no extra field reads** (the last *record* of the
file, `(type, customType)` only). Snapshot C, `incomplete` only, cross-tabbed with mtime age:

| last record | age < 10 min | 10 min–1 h | 1–24 h | > 1 d | total |
|---|---|---|---|---|---|
| `custom / session_exit` | **0** | **0** | 181 | 4 | 185 |
| `message` (bare) | 95 | 0 | 0 | 0 | 95 |
| `custom / tool_execution_start` | 5 | 0 | 0 | 0 | 5 |
| `custom_message / irc:incoming` | 1 | 0 | 0 | 0 | 1 |
| `model_usage` | 0 | 1 | 0 | 0 | 1 |

The separation is **perfect in this corpus, in both directions**: every one of the 101
`incomplete` files whose last record is not `session_exit` was written in the last 10 minutes
(live now), and every one of the 185 whose last record *is* `session_exit` is ≥ 1 h old
(shut down mid-turn, no final assistant message). `session_exit` itself is a one-shot EOF marker,
not a per-turn one: 39/40 randomly sampled files carry exactly one in the last 1 MiB (one resumed
session carries two). Its presence across classes — completed 4365, dead_rate_limit 251,
incomplete 185, aborted 94, dead_quota 29, unavailable 11, i.e. 4935/5085 — means it does **not**
prove a clean exit; it proves the transcript stopped being written.

Exposing a `transcript_closed` boolean derived only from the last record's `(type, customType)`
therefore lets an operator subtract live seats from the `incomplete` tally with zero false
positives on today's corpus (101 live vs 185 closed). This is a contract-shape suggestion for L1,
not a defect in the delivered rule.

### R4 — `aborted` is one prefix's teardown, not a death class

117 `aborted`, of which **50 have mtime < 10 min and all 50 are `KaidokuR19`**. `KaidokuR19`
carries 50 aborted / 91 transcripts; no other prefix has more than 4. `aborted` here means
"interrupted", which for a wave teardown is normal operation. The contract correctly keeps it out
of `dead_*` and out of the rc1 trigger; worth stating in the report header that a large `aborted`
block is evidence about *one* prefix's shutdown, not about provider health.

### R5 — Prefix/seat derivation hazards (naming, not class)

- Seat ids (basename minus `.jsonl`) are **unique: 5084 distinct ids, 0 collisions** across
  5084 files, so `seats` keyed by seat id is unambiguous in this corpus. That is a property of
  the naming convention, not a guarantee — two session directories that reuse a seat name would
  collide silently, because the contract keys seats by basename only.
- **611 distinct prefixes.** 15 of them are **top-level session ids** of the form
  `<ISO-timestamp>_<uuid>` (files at depth 1, e.g.
  `<session-id withheld>`), whose "prefix" is the
  whole id. They are not seats, yet they enter `seats`, `totals` and `by_prefix`. Effect on the
  snapshot: 15 of 5084 files (0.3 %) are non-seat transcripts, and `by_prefix` carries 15
  singleton keys of unbounded length.
- The other 596 prefixes appear both as a parent transcript `<Prefix>.jsonl` (prefix == seat id)
  and as child transcripts `<Prefix>.<task>.jsonl`. So `by_prefix[P]` includes the group's own
  parent transcript; the group total is not "N subagents", it is "N subagents + 1".

### R6 — Field-shape hygiene (all clean, listed because the tool must not regress them)

- **No partial writes:** 0 files end without a trailing `\n`; 0 unparsable lines in any window;
  0 files smaller than 4 bytes. The "drop the first line when the read did not start at byte 0"
  rule fired for 4650 files and never discarded the terminal record (the oldest record is never
  the terminal one — except in the R1 case, where the *first* line is a partial giant record).
- `message` is always a dict when `type == "message"` in this corpus; the contract's
  `isinstance(..., dict)` guard is still required for `custom` payloads.
- Record **types** observed in tails: `message`, `custom`, `custom_message`, `session_init`,
  `thinking_level_change`, `model_usage`, `title_change`, `title`, `session`, `model_change`,
  `credential_pin`; `customType` values on `custom` records include `session_exit` and
  `tool_execution_start`. The contract's "skip every record that is not `message`" rule is what
  keeps `credential_pin` records unread — **verified present** as the trailing record
  (`type == "credential_pin"`) in 2 files, so that skip is load-bearing, not hypothetical.

### R7 — Exit-code semantics vs a historical corpus

With 264 `dead_rate_limit` + 29 `dead_quota` in the default scope, `rc1` is permanent and `rc0`
is unreachable on this directory; every run also re-reports deaths from 2026-10-14. That is
correct per the contract ("≥1 `dead_*` in scope") but the finding name
`MORI_SEAT_TERMINAL_DEAD` should be read as *"dead transcripts exist in scope"*, never as
*"N seats are dead now"* — the drift in R2 shows the two differ by ~5 % per 5 minutes.
`--max-files 20000` never triggers (5085 files); the 4.09 GB corpus is read in 0.66 s because
only tails are read, which is a strong argument for keeping the tail-window design.

## 8. Remaining unknowns

1. **`custom`/`session_exit` payload** — whether it carries an exit status, error, or interruption
   reason is **not verified**. My field allowance excludes the record's `data` keys, so I did not
   read them. If it does carry a terminal status it would be a better anchor than the last
   `message` record; the sibling `RetryRecoveryShape.md` boundary note applies. Marked
   [INFERENCE] until someone with that allowance checks it.
2. **Liveness at scan time** is inferable in this corpus (R3: `session_exit`-absent tails were
   101/101 fresh), but "fresh mtime" and "live" are the same observation only as long as the
   writer keeps flushing; a seat killed between records while the transcript is still open would
   look identical to a running one. The discriminator separates *open* from *closed*, never
   *alive* from *hung*.
3. The 11 R1 files are all `openai-codex/gpt-6-luna` transcripts from earlier waves; the rate of
   >262144-byte records in *other* session roots (other projects) is unmeasured, so the 0.3 %
   windowing-failure rate is a lower bound, not a population estimate.
4. Whether `alibaba-token-plan/qwen3.8-flash` (17 aborted / 3 completed) and `KaidokuR19`
   (50 aborted) share a single teardown cause is not answerable from terminal records alone.

## 9. Advisory summary for C1 (L1 decides)

1. Escalate the tail window (262144 → 524288 → 1048576) on "no message record found" instead of
   emitting `unavailable`; `unavailable` only when the whole file lacks a `message` record.
   Removes 11/12 false `unavailable` and 11 under-counted `completed` at ≤0.3 % extra I/O.
2. Keep `errorMessage` token matching — it carries 32.8 % of terminal errors with no
   `errorStatus`. Do not substitute `errorStatus`.
3. Keep the rate-before-quota order and pin it with the observed `RATE_LIMITED` + `usage limit`
   fixture; pin `402` against a spurious numeric-id fixture.
4. State in `--help`, alongside the three mandated limits: a `dead_*` seat was measured to resume
   (13/264 within 5 minutes, 6 to `completed`), so counts are snapshots.
5. Consider exposing `transcript_closed` from the last record's `(type, customType)` only — it is
   the one liveness signal available without reading payload, and on this corpus it separated
   open transcripts (101/101 written in the last 10 min) from closed ones (185/185 ≥ 1 h old)
   with zero overlap.
6. Expect 15 non-seat top-level session ids in `by_prefix` and one parent transcript per group
   when reading the `seats`/`by_prefix` counts.
