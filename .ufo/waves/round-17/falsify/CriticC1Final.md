# CriticC1Final — post-A1 falsification of final C1

Seat: `MoriR17.CriticC1Final-4` (critic; advice only, not admission). Date: 2026-10-20.
Attacked claim: **C1 coverage** — `tools/mori-seat-terminal.py` at measured commit
`273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7`, under contract.md + Amendment A1
(`contract.md:109-123`). Scope ordered by the assignment: settle window vs permanent death,
default tail loss, duplicate stems, main files, exact-prefix matching, and whether the final
evidence overclaims complete coverage or incident count. No live transcript scan was run;
evidence is the retained live receipt `evidence/seat-live.json`, the fixture packs, the gate
manifests and wave-1 counterexample reports (`build/CriticC1.md`, `build/TranscriptShapes.md`,
`build/SeatNaming.md`, `build/CriticFrontier.md`, `falsify/MutQuota.md`, `falsify/CountC1.md`).
No installs, no probes, no writes outside this report.

Verified before attacking: `sha256sum` of the delivered tool, gate and expected.json match
`PINNED_INPUTS.json:8-13` (`5819c3c0…`, `21285c2b…`, `b684c63b…`).

## What survives (verified, not re-attacked)

- The 54/54 gate is self-consistent: `count-c1.json` rc0 `[54,0]`; manifests reconcile
  (`falsify/CountC1.md` already recounted independently; I re-verified summary `matched 54,
  mismatched 0, capability_absent 0`).
- All **94** `dead_rate_limit` seats in `seat-live.json` have non-null `terminal_ms`, all
  strictly older than `now_ms − settle` (ages 81.7–206 min vs 15 min window); the settle gate
  works on this corpus. `error_unsettled: 0` is plausible: deaths were 1.4–3.4 h old.
- Exact-prefix matching is correct end-to-end: `--prefix SoujiR17` now rc2
  `prefix-matched-none` (wave-1 SeatNaming F1 false-clean is closed); fixture
  `prefix_filter_souji` pins `SoujiR17-3`, and `SoujiR17-30.Trap`/`TsukuroiR17Extra.Xtrap`
  confirm no substring bleed (`expected.json` `prefix_all` seats).
- `duplicate_stems`, `main_sessions`, `kind`, `key` are all emitted; the live receipt shows
  `main_sessions: 0`, `duplicate_stems: 0`, and 466/469 entries with `key != seat` (nested
  `<Parent>/` keys) — relative-path keying works.
- Incident-count framing in the receipts/lesson is honest: 469 = scanned files under 3
  prefixes (not the ~2509-file corpus); 94 = seats, `retry_exhausted` 90 reported separately;
  lessons `round-17.md:152-158` says "observations", "not a constant incident count", and
  retains "resumed-after-error remains a measured counterexample". **No incident-count
  overclaim found.**
- 93/94 dead carry `error_code "1302"` → `dead_rate_limit` via the S043 code table; A1.10's
  mapped codes work (MutQuota killed the precedence mutant independently).

## Findings

### F1 — MED, fixable: null `terminal_ms` ⇒ `dead_*` contradicts A1's own dead definition

`mori-seat-terminal.py:260-261`: `if terminal_ms is not None and terminal_ms > now_ms −
settle*1000: error_unsettled`. When **all four** timestamp sources are absent
(`message.completedAt`, `message.timestamp`, `record.completedAt`, `record.timestamp`;
extraction at `:235-240`), the error falls straight through to `dead_*`.

A1:113 defines dead as "last observed record is an error **older than the settle window**".
A timestamp-free error has *no observed age* — it could have been written one second before
the scan. The class asserts aged evidence that does not exist.

- **Fixture-blessed, still semantically wrong:** `fixtures/seat/ErrorOther/bare-error.jsonl`
  is the only terminal-error fixture with no timestamp (measured: 30 error fixtures carry a
  timestamp, 1 does not) and `expected.json` pins it `dead_error_other`. So the gate actively
  protects this hole rather than catching it.
- **Live impact:** none in this receipt (94/94 dead had timestamps — verified above). But a
  provider that omits `completedAt` on error records gets instant `dead_*` at scan time with
  zero settle protection; during a mass-death event those seats would inflate `_DEAD` while
  potentially minutes old.
- **Smallest safe correction:** timestamp-free terminal errors → `error_unsettled` (or a new
  `error_age_unknown` counted in `totals` and the rc1 trigger), since the settle test cannot
  *prove* age either direction. Alternative: keep `dead_*` but state the null-timestamp rule
  in `LIMITS` (`:138-145`) and `--help`, where it is currently silent.

### F2 — LOW-MED, fixable: S043 vendor-code table is half-mapped; unmapped 429 quota codes still inflate `dead_rate_limit`

`QUOTA_CODES = {"1113","1308"}`, `RATE_CODES = {"1302"}` (`:87-88`); any other `(type=NNNN)`
falls through to the token tests (`:263-272`). S043's live table (`falsify/ReopenZai.md`,
lines 16/31/33 verified byte-identical 2026-10-20; wave-1 CriticFrontier `:130-133` lists the
rest) puts **1305** (overload), **1309** (plan expired), **1310** (weekly/monthly limit),
**1311, 1313–1321** (usage-window limits) all on HTTP 429. Of those only 1113/1308 were
mapped. Concretely: `(type=1310)` "Weekly/Monthly Limit Exhausted" contains no `QUOTA_TOKENS`
member → `dead_rate_limit`; `(type=1309)` "plan expired" likewise. Quota deaths on the exact
provider that motivated C1 (`contract.md:13-15`) still land in the rate bucket whenever the
vendor uses any code outside {1113, 1308}. MutQuota proved the mapped pair; the unmapped set
is the residual.

- **Smallest safe correction:** extend `QUOTA_CODES` to the full S043 usage/balance/plan set
  (1308–1311, 1313–1321) and route *any* other `(type=NNNN)` on a 429 to `dead_error_other`
  (unknown code is not evidence of rate limiting). One fixture per added code family; the
  gate mechanism already exists.

### F3 — LOW-MED, contract tradeoff: `error_unsettled` does not trigger rc1 → transient false clean

`dead = any(class.startswith("dead_"))` (`:484`) excludes `error_unsettled`. A scan within 15
min of a mass-death event emits `MORI_SEAT_TERMINAL_OK` + rc0 while `totals.error_unsettled`
is nonzero. A1 chose this ("not dead"), and `totals` does carry the count explicitly — but
the finding name reads as "no terminal errors observed". Today `seat-live` shows the mirror
image: the *same* corpus reported rc1 once the errors aged past 900 s, meaning the finding
flips on wall-clock, not on seat state. Tradeoff for the judge; smallest softening is a
`MORI_SEAT_TERMINAL_UNSETTLED` third finding value or a `pending_errors` count in the
top-level JSON — both already-emitted data, no new fields needed conceptually.

### F4 — Coverage gap, contract tradeoff: `unavailable` and `kind:main` seats are invisible to the finding

- `unavailable` never affects rc. Schema drift to a future version makes **every** seat
  `unavailable` (`_header_ok` `:302-316`) → totals all-zero dead → `MORI_SEAT_TERMINAL_OK`
  rc0: a **false clean under a completely blind scan**. Wave-1 `build/ReviewSchemaDrift.md`
  recommended rc2 on unsupported version; A1.6 instead made it a per-seat class — the
  reviewer warning ("do not emit partial seat totals as though coverage were complete") is
  half-answered: totals are emitted and honest, but `finding_id`/rc assert OK regardless of
  the `unavailable` share. Smallest fix: rc2 when `unavailable` == seat total (blind scan),
  or a `classified_fraction` field.
- `kind:"main"` files are analyzed but cannot produce rc1: a dead top-level session yields
  `dead_*` only inside `seats[]`, invisible to `totals`/`finding_id` (`:460-483`). Contract
  A1.3 chose exclusion; it is explicit in output (`kind`, `main_sessions`) — but "main files
  remain explicit" holds only inside the per-seat array, not in any total. Minor: a
  `main_dead` count would make it load-bearing.

### F5 — LOW-MED, fixable: default tail loss is still silent and `no-message` conflates two failure modes

TranscriptShapes R1 measured giant trailing `custom` records up to 464,352 B — inside the new
512 KiB default, so today's corpus resolves. But the boundary is untested upward: the largest
TailBoundary fixture is 482,025 B < 524,288. Any record ≥512 KiB at EOF (codex waves produced
464 KB; nothing bounds growth) → `_read_tail` drops the partial first line → zero parseable
message records → `unavailable`, `reason:"no-message"` — **the same reason as a genuinely
message-free file** (`_analyze` `:399-405`). The truncation path is invisible: the receipt
cannot distinguish "file too big for window" from "no messages", and `seat-live` reports
`unavailable: 0` as if coverage were complete rather than as "nothing exceeded the window".
Smallest fix: when the read started mid-file (`start > 0`) and no message record survives,
emit `reason:"tail-exhausted"` (or escalate once to 4× window before unavailable — the
measured cost was ≤0.3% extra I/O, TranscriptShapes §8.1).

### F6 — LOW: `files_scanned` counts post-filter files, not discovered files

`files_scanned` increments only for analyzed files — mains plus prefix-matching seats
(`:450-452`), i.e. 469 in the live receipt while ~2,509 `*.jsonl` exist in that directory.
`files_discovered` (the walk population, also the `--max-files` denominator) is never
emitted. An operator reading `files_scanned` as coverage sees a filtered subset presented
with an unqualified name. Smallest fix: emit both `files_discovered` and `files_scanned`.

### F7 — LOW: `duplicate_stems` blind spot at the seat/main boundary

`stem_counts` is built only over `seat_records` (`:481-482`). A stem existing once as a
`kind:main` file and once as a nested seat is not counted as a duplicate; also only
prefix-matching seats enter the count, so `duplicate_stems` under `--prefix` is a filtered
count, not a directory property. Both are small; document or include mains in the collision
set.

### Non-findings (checked, no defect)

- **Permanent-death overclaim in final evidence:** none found. `LIMITS` (`:138-145`) states
  "LAST OBSERVED … not proof the session will never resume"; lesson round-17.md:152-158
  keeps "resumed-after-error remains a measured counterexample". The `dead_*`/`_DEAD`
  vocabulary vs "aged terminal error" semantics is the wave-1 CriticC1 F1 tradeoff L1
  explicitly retained in the gate decision (lessons `:28-30`); F1/F3 above are the residual
  holes in that retained choice, not the naming itself.
- **"54→0" is not "54 defects fixed":** `unit` in PINNED_INPUTS.json:23 and lesson :116-119
  both frame it as unmet capability assertions = absent tool. Honest.
- **Coverage completeness:** the lesson does not claim corpus coverage; fixture scope is
  disclosed as synthetic (`contract.md:79-82`). Honest.
- **`seats` array includes mains** with `kind:"main"` — contract-conformant, visible.
- **Resumption via in-place rewrite** (wave-1 CriticC1 §2.3: same record gained
  `retryRecovery`) cannot extend the tail, so a `dead_*` verdict is stable against that
  mechanism; resumption via appended records is what the tail anchors on. Consistent.
- **`error_unsettled` boundary `>` (strict):** fixture `boundary` at exactly
  `now_ms−settle` → `dead_rate_limit` — matches A1 "newer than … minus N is unsettled".

## Correction table

| # | Defect | Axis | Fixable? | Smallest correction |
|---|---|---|---|---|
| F1 | null terminal_ms ⇒ dead contradicts aged-dead definition | correctness, provenance | yes | null-ts terminal error → `error_unsettled`/`error_age_unknown`, or state the rule in LIMITS + --help; add one fixture |
| F2 | S043 quota codes beyond 1113/1308 land in `dead_rate_limit` | correctness | yes | extend `QUOTA_CODES`; unknown `(type=NNNN)` on 429 → `dead_error_other` |
| F3 | `error_unsettled` excluded from rc1 → transient false clean | correctness (finding semantics) | judge tradeoff | `pending_errors` count or a third finding value |
| F4 | all-`unavailable` scan reports `_OK`; dead `kind:main` invisible to finding | coverage | yes (partially contract) | rc2 when classified seats == 0; `main_dead` total |
| F5 | >512 KiB trailing record ⇒ `unavailable`/`no-message`, truncation invisible | coverage, provenance | yes | `tail-exhausted` reason or one-step window escalation; giant-record fixture |
| F6 | `files_scanned` is post-filter; discovery count absent | coverage | yes | emit `files_discovered` |
| F7 | seat/main stem collisions and filtered counts absent from `duplicate_stems` | correctness | yes | include mains; document prefix scoping |

Attacked scope: every named element of the assignment — settle window (F1, F3), tail loss
(F5), duplicate stems (F7), main files (F4), exact-prefix matching (verified clean), and
evidence overclaim on coverage/incident count (no overclaim found; F4/F6 are residual
explicitness gaps). Not a blanket pass: F1 is the strongest finding — a
`dead_*` verdict that can assert settle-window age the record never had.
