# AttackSuppression — a valid positive hidden behind an invalid record, mixed JSON shape, data order

Role: critic, report-only. I made no production edits and ran no census, harness, jq or tests. Axis: **coverage** (milestone: retain validated positives without fabricated totals).

Target: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh`. CensusPositive was editing this file while I reviewed it, so I give line anchors with the snapshot tag I read. Fixture packs read: `.ufo/waves/round-15/fixtures/{BootArray,ForeignBoot,KernelSystem,KernelUser,NegativeInvalid,ProcessUser,SignalUser}.json`. Harness reference: `tools/mori-round14-regressions.py`.

Installs: none.

## S1 — FIXED in flight: jq precedence zeroed `positive_unit_signal` (critical)

**Anchor.** Snapshot `#6933`/`#BA66`, `:1034`/`:1036`:

```
JOURNAL_JQ_POS_UNIT="[[.[] | select(P_oom)] | length, [.[] | select(P_sig)] | length]"
```

**Defect.** In jq, `,` binds tighter than `|`. The grammar declares `%right '|'` before `%left ','` (`[INFERENCE]` from jq's src/parser.y; the source was not read locally). So the filter parses as:

```
[ [sel_oom] | (length, [.[] | select(P_sig)]) | length ]
```

- The signal subset is taken over the array that is already oom-only.
- `oom-kill` and `signal` are mutually exclusive, so the result is always `[n_oom, 0]`.

**Counterexample.** `fixtures/ForeignBoot.json` `foreignboot_user_unit_signal_mixed`:
- user records: `{_BOOT_ID:1111…, MESSAGE_ID:d9b373ed…, UNIT_RESULT:"signal"}` and `{_BOOT_ID:2222…, MESSAGE_ID:d9b373ed…, UNIT_RESULT:"signal"}`.
- The aggregate is `multi-boot`, so raw `unit_signal` is unavailable.
- The positive vector is `[0, 0]`, so `KILL_SIGNAL_JOURNAL` is suppressed.

The same happens in SignalUser cases 2–3 and BootArray case 4. The defect is hidden on clean streams because the raw path still warns there. It shows up only on the mixed streams this claim exists for.

**Status.** I messaged CensusPositive. Snapshot `#ED14` `:1036` now reads `[([…] | length), ([…] | length)] | @tsv`, which is correct.

**Required behavior.** Keep each length in parentheses. Add a census selftest or harness case with a mixed stream containing one valid signal record and one foreign-boot record, and assert the exact literal `positive_unit_signal=1`.

## S2 — FIXED in flight: an earlier plan would have broken every kernel/sigkill query

**Anchor.** The snapshot `#6933` comment at `:1025` planned `<aggregate>, (<positive> | @tsv)` as two lines from one jq run.

**Defects in that plan:**
- `POS_KERNEL` and `POS_SIGKILL` end in `| length`, which is a number. `number | @tsv` is a jq error (`@tsv` takes only arrays). That gives `jrc≠0`, then `malformed-json` on every kernel/sigkill query, clean ones included. The r14 OOM and KILL alarms would be lost everywhere.
- Output of two lines breaks the exact match `case "$parsed" in record-invalid|multi-boot|boot-mismatch` (old `:1161`). The width check would then rewrite `multi-boot`/`boot-mismatch` as `malformed-json`, which is a regression in the raw reason tokens.

**Status.** Snapshot `#52DF`/`#D1E3` replaced the plan with `journal_positive_scan` (`:1100-1130`). It is a separate jq run over the same `$raw` and does not query the journal again. It is called on every semantic-failure return: `:1204-1208`, `:1227-1230`, `:1236-1239`, `:1246-1249`, `:1252-1255`.
- The kernel/sigkill selectors print a bare integer (no `@tsv`).
- Unit prints `n\tn`.
- Output with a newline is rejected (`:1121`).
- The width and integer checks are at `:1124-1128`.

## S3 — OPEN at last read: the healthy (ok) path leaves `JQ_POS_VEC` empty

**Anchor.** `#D1E3`:
- `:1150` resets `JQ_POS_VEC=''` (good: no stale value leaks across classes or scopes).
- The scan runs only on semantic failure (`:1138-1140`: "a healthy class pays no extra jq process").
- The ok return (`:1231` onward) never sets `JQ_POS_VEC`.

**Counterexample.** A clean user stream with one `fe6faa94…` current-boot record (`signal_user_valid_only`-style, kernel variant):
- The raw value is `kernel_oom_notice=1` and status is `ok`.
- If `probe_journal` reads positives only from `JQ_POS_VEC`, it renders `positive_kernel_oom=user:unavailable`.
- If the alarm is driven only by positives, the r14 OOM crit disappears on a healthy class. That would regress every r14 matrix arm (census selftest `journal: all twelve scoped cells counted; one OOM crit…`).

**Smallest required behavior (probe side).** For a class with `js=ok`:
- `positive_kernel_oom = jn[kernel]`
- `positive_unit_oom = ucnt[oom]`
- `positive_unit_signal = ucnt[signal]`
- `positive_process_sigkill = jn[sigkill]`

These are identical by construction: the ok branch already proved every record valid. For a semantic failure, use `JQ_POS_VEC`. For an rc, stderr, timeout, no-timeout-bin or parse failure, use `unavailable:<that class's JQ_STATUS>`.

**Invariant to assert in the harness:** `js=ok ⇒ positive == raw subset`.

## S4 — OPEN: alarm assembly traps (wiring not landed at my last read)

`OOM_KILL_JOURNAL`/`KILL_SIGNAL_JOURNAL` are still driven only by raw counts in `#D1E3` (alarm block after `:1360`). The following must hold when the wiring lands:

1. **Single alarm line.** Keep one `oom_fire`/`kill_fire` flag fed by both raw>0 and positive>0. A second `emit_finding` for the positive path doubles the crit/warn lines. Drift counts alarm lines, so that is a false drift.
2. **`paths=` derives from positives.** Today `oom_path_k`/`oom_path_u`/`kill_paths` are set only from raw (r14 anchor `:1314-1329`, `:1344-1351`). A fire from positives alone would print `paths=` with an empty value, which breaks the grammar.
3. **Raw fields stay byte-identical.**
   - In the OOM line: `user_notice=` and `user_unit_oom=` (plus their `system_*` counterparts).
   - In the KILL line: `count=`, `process_sigkill=` and `user_unit_signal=`.
   - Each must keep `unavailable:<reason>` and never take the positive integer.
   - Positive evidence goes only into the new `positive_*` fields.
4. **Guard the integer test.** Use a `case "$v" in unavailable:*)` guard, as the r14 pattern does, before `[ "$v" -gt 0 ]`. Without it, `[ "unavailable:rc-1" -gt 0 ]` prints `integer expression expected` to census stderr. The result is a silent non-fire plus stray stderr that a harness checking stderr would flag.
5. **Scope isolation.**
   - The KILL warn reads only `user:` positives.
   - `system:` `positive_unit_signal`/`positive_process_sigkill` must never feed it.
   - OOM reads both scopes and is never summed.
6. **No OOMD inheritance.** The `*)` query branch (r14 `:1219`) shares `JOURNAL_JQ_MSGID` with oomd and coredump. `JOURNAL_Q_POSITIVE_FILTER` must be set only on the kernel, unit and sigkill calls, and positives must be stored per `scope:class` key. A positive from `d989611b` that lands in `positive_kernel_oom` would turn an INFO notice into a crit.
   - **Status in snapshot `#ED61`: landed.** A dedicated `kernel_oom_notice` branch (`:1343`) and the sigkill/unit calls (`:1347`, `:1354`) carry the positive filter. The oomd/coredump `*)` branch (`:1372`) does not. Positives are stored per key as `jpos[$key]=$JQ_POS_VEC` (`:1374`). The alarm block that reads `jpos` had not landed at this read, so S3 and S4 items 1–5, 7 and 8 stay open.
7. **No resurrected routing.** Positives must not emit `UNIT_FAILURE_JOURNAL`, `UNIT_FAILURE_OUT_OF_SCOPE` or `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` from the positive subset. The owner partition stays aggregate-only and unavailable.
8. **No boot from an invalid stream.** `boot=` on the alarm lines stays `$BOOT_ID_EXPECTED` (r14 `:1331`, `:1353`). `JQ_BOOT` and `sboot` from an invalid stream are never set and never used. In the aggregate, `[.[]._BOOT_ID][0]` is first-record-dependent and is computed only on the ok branch.

## S5 — Mixed JSON shape: the selectors hold; the harness can't deliver some shapes

**Selectors (snapshot `#ED14` `:1033-1036`).**
- `JOURNAL_JQ_POS_BASE` is a chain of `select`s, starting with `select(type == "object")` before any index. That guard removes non-object elements such as `"x"`, `9`, `true` and `[…]`, so they cannot raise `Cannot index …` and fail the whole scan.
- An identity array (`MESSAGE_ID:["fe6f…"]`, `_BOOT_ID:["1111…"]`) is excluded by `type == "string"`.
- `EXIT_STATUS` accepts only string `"9"` or number `9`. Arrays, null, bool, `"09"` and `"137"` are rejected.
- `UNIT_RESULT` must be the exact string.
- No `tostring` appears on the positive path. (The aggregate `JOURNAL_JQ_SIGKILL` `:1022` keeps `tostring`, and that is unchanged r14 behavior.)

**Data order.** Each selector is `[.[] | select(…)] | length`. That is invariant to order and does not short-circuit, so `[invalid, valid]` and `[valid, invalid]` give the same count. KernelSystem case 4 (array first, scalar second) pins this.

**Harness delivery gap** (`tools/mori-round14-regressions.py`). This adds to AttackFixtureOracle's stub-mode findings; it is not a repeat of them.
- **`honor` mode.** `:523` calls `str(rec.get(k))`. A record that is not a dict (a JSON list, string or null line) raises `AttributeError`, so the stub exits 1 with a traceback. Every query in that scope becomes `rc-1`, and positives are unavailable for the wrong reason.
- **`ignore-filters` mode.**
  - `:539-543` builds `{k: rec[k] for k in fields if k in rec}`. A list record projects to `{}`. A string record does substring tests and can raise `TypeError`.
  - Non-JSON lines are rewritten as `{"_malformed": line}` objects (`:501-504`).
  - So the r14 Python stub can never hand the census a non-object element or an unparsable line mixed with a valid record.

**Required behavior.** Pin the object guard in the census internal selftest. Its stub `cat`s slot files verbatim (`#2EED` `:2625-2627`). Write the raw lines into `$FX/stub/journal-user-kernel_oom`:

1. `{"_BOOT_ID":"<BOOT13>","MESSAGE_ID":"fe6faa94e7774663a0da52717891d8ef"}`
2. `"x"`
3. `[1]`
4. `9`

Expected:
- `kernel_oom_notice=unavailable:record-invalid` (raw).
- `positive_kernel_oom` user value `1`.
- One `OOM_KILL_JOURNAL severity=crit`.
- DRIFT.

Pair it with a negative arm: the same lines with the valid record removed must give positive `0`, no crit and CLEAN. The control arm is a truncated `{"_BOOT_ID":` line next to a valid record. jq `-s` then fails to parse, so both raw and positive are `unavailable:malformed-json` and there is no crit. That is accepted: the spec does not repair arbitrary malformed JSON. The harness cannot express this arm because its stub turns the line into an object.

## S6 — Residuals I found no exploit for

- The bash post-checks on the ok branch (`nb==0 && n>0`, `nb≠1`, boot not 32-hex) now also run the scan (`:1227`, `:1236`, `:1246`, `:1252`). They can fire only if `BOOT_ID_EXPECTED` is itself malformed, which is the same r14 outcome.
- rc, stderr, timeout and no-timeout-bin returns happen before any jq run, so positives stay empty. That matches the contract: unavailable on capture failure.

## Impacted axes

- **Coverage** (target): S1 and S3 directly decide whether hidden positives are retained (S1) and whether healthy-class positives keep their honesty (S3).
- **Operability/no-harm:**
  - S2 (fixed): plan defects that would have regressed every r14 alarm.
  - S4: the raw tokens and the single alarm-line count, which drift depends on.
  - S5: test delivery.

## Checks for L1 after integration

- Census `--selftest`, including the S5 raw-line arms.
- The round-15 harness with these assertions:
  - exact `positive_unit_signal=1` on `foreignboot_user_unit_signal_mixed`;
  - `count_ids(OOM_KILL_JOURNAL)==1`;
  - the r14 matrix arm still has one crit and one warn, with `positive_* == raw` there.
