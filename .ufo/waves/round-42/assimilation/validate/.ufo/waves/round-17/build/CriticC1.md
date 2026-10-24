# CriticC1 — attack on C1 (seat terminal-status), mori round 17 wave 1

Seat: `MoriR17.CriticC1-5` (critic; advice only, not a judgment). Date: 2026-10-20.
Axes considered: coverage (C1's declared axis), correctness/provenance, authority (no duplicates),
province integrity, falsifiability.

## Verdict (summary)

Detecting seat terminal state is **defensibly inside mori's province**, but only as a
consume-only liveness observation (frontier FR14). C1 as written has three fixable defects that the
L1 must correct before it can claim the coverage move:

1. **"dead" is false naming.** Retained transcripts and a live race in this wave both show seats that
   C1 would call `dead_*` later continuing and completing.
2. **It creates a second, contradicting failure taxonomy.** The canonical one is kumitate/ufo-fsd
   `classify_failure_fields`. C1 reverses its rate-vs-usage order and drops its digit guard.
3. **The planned demonstration is circular.** It confirms the needles on the incident that chose
   them and cannot falsify the claim that these seats died.

**Strongest falsifier:** the resurrection replay/rescan in §4.

## 1. Province: whose is seat-death detection?

- **For mori:** the domain is "whether the fleet, its waves and its host are alive and progressing"
  (`mori-shokunin/PROVINCE.md:3-4`). Mori already names agent-workload telemetry as frontier, with
  the limit "mori is consume-only; telemetry emission belongs to the emitting lanes and
  orchestration" (`PROVINCE.md:57`, FR14). A read-only terminal-state tally is consumption, so it
  belongs there. kama's domain is *local* serving (`kama-shokunin/PROVINCE.md:3-4`), so remote
  provider 429s are not kama's.
- **Against mori:**
  - mori refuses "dispatch and orchestration mechanism (→ kumitate)" (`PROVINCE.md:12`).
  - kumitate owns "OMP task/hub" (`kumitate-shokunin/PROVINCE.md:3`) and names the "OMP transcript
    task-oracle" as one of its four observation-truth sources (`kumitate-shokunin/SKILL.md:97-98`).
  - kumitate's knowledge already covers transcript, seat-coverage and failure-class authority:
    `native_transcript.rs`, `native_seat_coverage.rs`, `ENTRY_FAILURE_CLASSES` and
    `classifyFailure` (`kumitate-shokunin/SKILL.md:425-445`).
  - FR3 says "mori reports filesystem shape; kumitate owns orchestration/result semantics"
    (`PROVINCE.md:46`). Per-seat outcome classes (rate limit / quota) are result semantics.
- **Ruling (advice):** C1 is in province only if it **observes and tallies** terminal state and
  takes its *failure-class vocabulary* from the canonical authority without inventing one. It must
  be filed as advancing FR14, not as new Core "seat death". As drafted (`contract.md:39-51`, its own
  class list and order), it absorbs kumitate's classification authority. That is a duplicate
  authority (see §3).

## 2. Is a terminal error a death? No — counterexamples observed

All reads below were field-limited: `type`, `customType`, `message.role`, `stopReason`,
`errorStatus`, `provider`, `model`, contract tokens matched on `errorMessage` as booleans only,
and `retryRecovery` key shape. Scope:
`<session-store path withheld>`,
2508 `*.jsonl` files, no symlinks followed. Snippets ran in the eval kernel; no files were written.

### Retained-history resurrection

For each `session_exit` custom record, I classified the last message record before it. In
**10 files** that class was `dead_rate_limit` (unrecovered error, then the session exited), yet the
file later continued:

| Count | Provider/model | Final class |
|---|---|---|
| 6 | zai/glm-5.3-flash | completed |
| 3 | anthropic/claude-opus-5-5 | completed |
| 1 | zai/glm-5.3-flash | incomplete |

- Prefixes: TameshiR17 ×7, KaidokuR18, MadoR18, TsukuroiR17. The last three are root L1 files
  (`KaidokuR18.jsonl`, `MadoR18.jsonl`, `TsukuroiR17.jsonl`).
- A scan taken between the exit and the resume would have counted them dead.
- `session_init` occurs more than once in **574/2508 files** (2:350, 3:190, 4:16, 5:12, 6:5, 8:1).
  Resumption is routine, not an edge case.

### Live race inside this wave

1. **~15:55-03:00:** `MoriR17/MoriR17.RevengerOmpTerminal-5.jsonl` held 7 message records. The last
   was assistant `error`, `errorStatus` 429, zai/glm-5.3-flash, tokens `429`/`Rate limit`/
   `type=1302`, no `retryRecovery`, and no `session_exit`. C1 → `dead_rate_limit`, rc1.
2. **15:57:42:** the same file held 36 message records. A `session_init` followed the error, then
   the seat resumed with `toolUse`/`toolResult`. Its mtime was 15:56:57.
3. The **same record (message index 6) now carries `retryRecovery` with `recoveredAt`**.
4. So the file is rewritten in place, not purely appended [observed: the same record position
   gained a key]. **A missing `retryRecovery` on a terminal error means "not yet recovered", not
   "dead".**
5. Two more seats show unrecovered 429s followed by continued work: `KaidokuR19.jsonl`
   (error@72, then `toolUse`) and `KamaR17/KamaR17.MistakesTable.jsonl` (rescanned 15:57).
6. Mid-file errors are common: 836 files contain ≥1 assistant error, and **518** of those reach a
   later `stop`.

### What does discriminate

- Of 173 terminal `dead_*` files in scan 1, **170 have a `session_exit` after the terminal error**.
  Only 3 had none, and all 3 were live seats still retrying (above).
- `retryRecovery` without `recoveredAt` occurs 1330 times, all non-terminal.
- So `session_exit`-after-error is a far better "ended" signal. It is still not final: the 10
  resurrections above all had an exit.

### Impacted axes and correction

- **Correctness/provenance:** the finding name `MORI_SEAT_TERMINAL_DEAD` and the `dead_*` classes
  assert death; the evidence supports only "terminal error at observation". The `--help`
  disclaimer at `contract.md:65-66` does not repair a finding key whose name states the opposite.
- **Smallest safe correction:**
  1. Read `customType == "session_exit"` and count `type == "session_init"` (both type-only
     fields, already permitted) to emit per seat `exit_after_terminal` (bool) and `resumes`
     (`session_init` count − 1).
  2. A terminal error **without** a following `session_exit` → new class `error_pending` (or
     `incomplete`), never `dead_*`.
  3. Rename the classes to `terminal_rate_limit` / `terminal_quota` / `terminal_error_other` and
     the finding to `MORI_SEAT_TERMINAL_ERROR`. Alternatively keep the names but define them
     strictly as "error terminal + exit observed".
  4. Add an `observed_at` UTC timestamp and a per-seat mtime age to the JSON.

## 3. Duplicate, contradicting classification authority

The canonical rule table is `ufo-fsd-alpha/crates/ufo-core-runtime/src/native_text.rs:88-97`. Its JS
mirror is `scripts/collect-omp-native-handoff-lib/base.mjs:758`. kumitate's rule is "Vocabularies
are single-sourced; learn the source, cite it, never restate a second copy"
(`kumitate-shokunin/SKILL.md:425-426`). C1 diverges from it:

| Aspect | Canonical (`native_text.rs`) | C1 (`contract.md`) |
|---|---|---|
| Order | `UsageLimit` row before `RateLimit` row (`native_text.rs:89-90`; "the **first** matching row wins, so the order IS the contract", `:85-87`) | Rate-limit before quota (`contract.md:51`) |
| Case | Case-insensitive: the haystack is `json_lower` of status, id and message (`:116-133`) | Case-sensitive literals (`contract.md:43-46`) |
| Status codes | Digit-guarded `contains_status_code` (`:135`) | Raw substring `429` / `402` |
| Needles | Also `too many requests`, `tokens_exceeded`, a `model_unavailable` class, and others | Adds `resource_exhausted`, `credits`, `402`, which canonical lacks |

Measured divergence in this session dir (all assistant error records):

- **285 records** carry rate tokens (or status 429) **and** a quota/usage token: commandcode/
  deepseek-v4.1-flash 278, devin/swe-2 3, cursor/claude-opus-5-5 1, google-antigravity/
  claude-opus-5-5 1, cursor/claude-haiku-5-5-1m 1, cursor/claude-haiku-5-5 1. C1 calls these rate
  limit; the canonical order calls the usage-token ones `usage_limit` [INFERENCE for the 3 devin
  rows, whose only quota token is an embedded `402`].
- **1 terminal** divergence: cursor/claude-haiku-5-5, tokens `RATE_LIMITED` + `usage limit`.
  C1 says `dead_rate_limit`; canonical says `usage_limit`.
- **3 devin/swe-2 error records** whose only quota token is `402` embedded in a longer digit run.
  C1's raw substring would class them `dead_quota` if terminal; canonical's digit guard would not.
- **1 terminal devin/swe-2** record contains `429` only as an embedded substring (it also carries
  `resource_exhausted`, so its C1 class is unchanged).
- **12 terminal devin/swe-2 `resource_exhausted`** seats: C1 counts them as rate limit. Canonical has
  no such needle [INFERENCE: it yields Unknown or another class; not measured, because testing
  non-contract needles is outside my transcript field permission].
- Measured gap from C1's case-sensitivity: 0 records in this corpus (no case-only misses).

- **Impacted axes:** authority (a second taxonomy), correctness (opposite verdict on usage-vs-rate),
  and the future cost of every consumer that joins mori counts with kumitate `failureClass` rows.
- **Smallest safe correction:** mirror `FAILURE_RULES` order, needles and digit guard verbatim, with
  citation to `native_text.rs:88-97`. Emit the canonical class names (`rate_limit`, `usage_limit`,
  `model_unavailable`, …) as a `failure_class` field, and keep mori's own field only for the
  terminal/exit state. If mori needs `resource_exhausted` → rate limit, record it as a reported gap
  routed to kumitate, not a local extension. This is fixable, not a tradeoff.

## 4. Is the live demonstration circular? Yes, on three counts

1. **Needles chosen from the incident they are shown on.** The tokens `429`, `Rate limit`,
   `(type=1302)` and "Retry budget exhausted" were picked from today's zai deaths
   (`contract.md:13-15`). Running on the same session dir then "finds" ≈171 rate-limit deaths by
   construction. It tests substring matching, not the claim that the seats died.
2. **The DeadSeatCrossCheck oracle is not independent.** It compares against the orchestrator's
   statement "tabi 17, tsukuroi 43, souji 28+" (wave1-spec item DeadSeatCrossCheck). [INFERENCE] That
   statement was itself derived from the same task errors/transcripts, so agreement is
   self-consistency. My scan-1 tallies by prefix:
   - TabiR17: 22 `dead_rate_limit` (vs 17), plus 4 aborted.
   - TsukuroiR17: 44 (vs 43).
   - SoujiR17-3: 29 (vs 28+).
   - **Prefix defect:** that last prefix is `SoujiR17-3`, so `--prefix SoujiR17` returns **0 seats**.
     The prefix rule (`contract.md:33-34`) misattributes the lane. Correction: strip a trailing
     `-\d+` from the prefix, or make `--prefix` a prefix match. State which.
3. **Fixture gate = spec conformance.** Fixtures are synthetic from the contract's own shapes
   (`contract.md:71-74`), and `expected.json` is written from the same contract. A green gate
   proves that the tool matches the contract, not that the contract matches reality.
   - A live run inside wave 1 also includes this wave's own seats: MoriR17 had 61 incomplete,
     9 completed and 1 `dead_rate_limit` at scan 1.
   - That one "dead" Mori seat was alive two minutes later (§2).

### Strongest falsifier the L1 must run (resurrection test)

The test is deterministic, uses retained data and stays within the field limits.

**(a) Replay.** For every `*.jsonl` in the session dir:
1. Walk the records in order, keeping only `type`, `customType`, `message.role`/`stopReason`/
   `errorStatus` and the contract-token booleans.
2. At each `session_exit` record, and at each assistant error record, compute the class C1 *would
   have emitted* if the file had ended there.
3. Count the seats whose would-be class was `dead_*` at some cut point but whose class at EOF is not
   `dead_*`.

**Falsification rule:** a count above 0 refutes "dead". I measured **10** with exit-gated cuts. The
L1 should rerun it on the post-wave tree, including the error-record cuts, which will be larger.

**(b) Double scan.** Run the delivered tool at T0 (mid-wave) and at T1 (after wave-1 settlement)
over the same dir, then join on seat id.
- Count every seat with `dead_*` at T0 and non-dead at T1. One observed instance already exists
  (`MoriR17.RevengerOmpTerminal-5`, 15:55 → 15:57).
- If both (a) and (b) are 0 after the §2 correction (`dead_*` requires `exit_after_terminal`), the
  re-scoped claim survives.

**(c) Authority-agreement falsifier.**
- Run C1's class and a verbatim port of `native_text.rs:88-97` over the same terminal records.
- Any disagreement must be 0 or declared row by row. Today it is ≥1 terminal and 285 overall
  (§3).

Replay snippet core (Python, read-only, prints counts only; the session-dir path is the one in §2):

```python
for line in open(p, 'rb'):
    r = json.loads(line)  # wrap in try/except and skip bad lines
    if r.get('type') == 'custom' and r.get('customType') == 'session_exit':
        cut_points.append(len(msgs))
    elif r.get('type') == 'message' and isinstance(r.get('message'), dict):
        m = r['message']
        msgs.append(cls_from(m['role'], m.get('stopReason'), m.get('errorStatus'),
                             token_bools(m.get('errorMessage'))))
# a seat is resurrected if any msgs[k-1] at a cut k is dead_*
# and msgs[-1] is not dead_*
```

## Corrections table

| # | Defect | Axis | Fix or tradeoff | Smallest correction |
|---|---|---|---|---|
| 1 | `dead_*` / `_DEAD` asserted while seats resume | correctness, provenance | fixable | Gate `dead_*` on `session_exit` after the terminal error; add `error_pending`, `exit_after_terminal`, `resumes` and `observed_at`; or rename to `terminal_*` / `_TERMINAL_ERROR` |
| 2 | Second failure taxonomy, opposite order, no digit guard | authority | fixable | Mirror `native_text.rs:88-97` verbatim and cite it; emit canonical `failure_class`; route `resource_exhausted` to kumitate as a gap |
| 3 | Circular demonstration | falsifiability | fixable | Run the §4 (a)/(b)/(c) falsifiers; do not use orchestrator counts as the oracle |
| 4 | `SoujiR17-3` prefix misattribution | correctness | fixable | Normalize a trailing `-\d+` in the prefix, or make `--prefix` a prefix match; fixture it |
| 5 | Province framing | province | tradeoff for the judge | File C1 as an FR14 consume-only advance with an Adjacent row naming kumitate as taxonomy owner; no Core "seat death" claim |

## Limits

- Field-limited reads only; no `errorMessage` text, content or usage was printed. Token matches
  were computed as booleans, with an extra digit-guard boolean for `429`/`402`.
- No tool or selftest was run. The C1 tool is not yet delivered to me, so all classes above are my
  re-implementation of `contract.md:39-51`.
- The kumitate/canonical comparison used only contract tokens. Canonical-only needles were not
  tested [INFERENCE where stated].
- No installs, no files written except this report, no VCS commands.
