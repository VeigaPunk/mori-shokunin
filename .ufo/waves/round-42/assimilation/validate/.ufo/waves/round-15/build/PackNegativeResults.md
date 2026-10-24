# Round 15 — Negative unit-result fixtures (`NegativeResults.json`)

**Seat:** `MoriR15.PackNegativeResults` (executor, leaf). **Axis:** coverage. **Milestone:** retain validated positives without fabricated totals.
**Write scope:** `.ufo/waves/round-15/fixtures/NegativeResults.json` (owned) and this report. No production, gate, harness, sibling pack or manifest edit. No commit. No tool installed or updated. No census, stub, gate, selftest or fixture was executed: every expectation below is derived from source text and the round-15 contract, not measured.

## 1. Edge owned

`UNIT_RESULT` that is an array, `null`, absent, or a wrong-case string must never be evidence of `positive_unit_oom` or `positive_unit_signal`. The pack also proves the converse: an independently valid record in the same stream still yields exactly one alarm, and the malformed-result record does not inflate the positive count. Scope is unit-failure (`d9b373ed…`) records only.

Pack: 4 cases, 5 records, no `MESSAGE` key, no canary strings, distinct `__CURSOR`s, fixed literals `_BOOT_ID=11111111111111111111111111111111` and unit id `d9b373ed55a64feb8242e02dbe79a49c`. Case ids are unique across the whole `fixtures/` directory (checked against all packs present at write time). Fixture snapshot: sha256 `0cf958fd6cde2f18bba1c9ee258f449df9d5ce8c146c5d9763d83c60664dcf82`, 4376 bytes.

## 2. Cases and static expectations

| id | scope | result shape | want_oom | want_signal | invalid_class |
|---|---|---|---|---|---|
| `neg-results-user-array-oom-only` | user | `["oom-kill","signal"]` | false | false | null |
| `neg-results-system-null-with-valid-oom` | system | `null` + valid `"oom-kill"` | **true** | false | null |
| `neg-results-user-missing-with-valid-signal` | user | key absent + valid `"signal"` | false | **true** | null |
| `neg-results-user-wrong-case-only` | user | `"OOM-KILL"` + `"Signal"` | false | false | null |

Derived per-scope expectations (r14 raw tokens preserved, r15 positive tokens added):

| case | raw `unit_failure_record` | `unit_oom` | `unit_signal` | `unit_oom_result_unknown` | `positive_unit_oom` | `positive_unit_signal` | roll |
|---|---|---|---|---|---|---|---|
| 1 user | 1 ok | 0 | 0 | 1 | 0 | 0 | CLEAN, drift 0 |
| 2 system | 2 ok | 1 | 0 | 1 | 1 (system row; user 0) | 0 | DRIFT 1, one OOM `crit` |
| 3 user | 2 ok | 0 | 1 | 1 | 0 | 1 (user row; system 0) | DRIFT 1, one user `KILL_SIGNAL_JOURNAL warn` |
| 4 user | 2 ok | 0 | 0 | 0 | 0 | 0 | CLEAN, drift 0 |

`positive_kernel_oom` and `positive_process_sigkill` are 0 on both scope rows in all four cases (no `fe6faa94…` / `98e32220…` record). Case 2's OOM line carries `paths=unit_result_oom_kill`, `system_unit_oom=1`, `system_unit_oom_result_unknown=1`, `user_unit_oom=0`. Case 3's warn carries `paths=unit_result_signal`, `process_sigkill=0`, `user_unit_signal=1` (the `count=` field counts process SIGKILLs and is 0; the alarm is the unit-result path). All four cases use the valid non-fleet subject `neg-results.service`, so an `UNIT_FAILURE_OUT_OF_SCOPE*` info finding appears and never flips the roll.

## 3. Why `invalid_class` is `null` in every case

The unit-failure aggregate is validated on record identity only. The working tree's `JOURNAL_JQ_UNITS` outer guard requires every element to be an object with scalar `_BOOT_ID == $boot` and `MESSAGE_ID == $id` (`tools/mori-census.sh` read snapshot sha256 `87cd66bc…`, `JOURNAL_JQ_UNITS` at `:1061` onward; the unit query passes `--output-fields=_BOOT_ID,MESSAGE_ID,UNIT,USER_UNIT,UNIT_RESULT` with only `MESSAGE_ID=${ids[$cls]}` as the match word). `UNIT_RESULT` is deliberately outside that guard:

- `def oom:` requires `UNIT_RESULT` to be the **string** `"oom-kill"` (`:1076`).
- `def sig:` requires the **string** `"signal"` (`:1077`).
- `def resunk:` counts every non-string/missing value as `unit_oom_result_unknown` (`:1078`), documented as "never oom evidence" and "never a fabricated known 0" (`:1052-1057`).

The census file is under active edit by CensusPositive; the anchors above are from the hash-stamped snapshot, not a stable line map.

So an array/`null`/missing result is a *valid identity record with an unknown result*, not a `record-invalid` stream: the raw `unit_failure_record` count stays available (1 or 2) and the split shows one unknown. A wrong-case string is a valid scalar nonmatch (`oom=0`, `signal=0`, `resunk=0`). Marking any of these `invalid_class="unit_failure_record"` would assert unavailability that the preserved r14 semantics do not produce.

The r15 positive contract agrees: positives come from individually valid records, and "a parsed stream with no individually valid record is a real 0 for the positive token" — only capture/stderr/JSON-parse failure makes a positive token `unavailable:<reason>` (`tools/mori-census.sh:955-990` at snapshot `87cd66bc…`, `JOURNAL_JQ_POS_UNIT` at `:1036`). Hence array/`null`/missing produce `positive_* = 0` (with the unknown preserved in the raw split), not `1` and not a fabricated alarm.

## 4. Required harness setting (stub mode and environment)

`tools/mori-round14-regressions.py` (`journal_stub_body` `:582`; modes docstring `:585-599`; snapshot sha256 `3aaa1e22…`) supports `honor`, `leak`, `ignore-filters`, `dup-kernel`, `mismatch-kernel`, `malformed`, `text`, `hang`. `Case.mode` defaults to `honor` (`:929`).

**The loader MUST build these cases in `honor` mode** (AND of every `FIELD=value` argv word, `:688-708`; `--output-fields` projection plus the four `ALWAYS` metadata fields, `:713-725`). Under `honor`:

- The unit-failure query's only match word is `MESSAGE_ID=d9b373ed…`, so all five records are returned and split in one jq pass; result shape is examined in-stream, exactly as production does.
- The kernel query (`MESSAGE_ID=fe6faa94…`) and the process query (`MESSAGE_ID=98e32220… EXIT_CODE=killed EXIT_STATUS=9`) filter these `d9` records out, so they cannot poison `kernel_oom_notice` or `unit_sigkill_record`.

**Do not use `ignore-filters` (or `dup-kernel`/`mismatch-kernel`) for this pack.** All five records carry a scalar current `_BOOT_ID`, so a leaked stream would fail the kernel/process jq identity guard and grade both classes `unavailable:record-invalid`. That is multi-class poisoning the single `invalid_class` field cannot express, and it is not what a real journalctl returns for those match words. If a future harness deliberately uses leak mode, these cases must not be loaded with `invalid_class=null`.

**Environment override:** r14 `census_env` pins `MORI_BOOT_ID` to `JOURNAL_BOOT` (`0123456789abcdef0123456789abcdef`; `tools/mori-round14-regressions.py:818-871`, pin at `:851`); the round-15 pack contract uses `11111111111111111111111111111111`. The loader must override `MORI_BOOT_ID` (or `boot_id`) for every pack case, otherwise all records are `boot-mismatch` and the pack is meaningless. Per-scope record lists map directly to `journal/<scope>.records` (`build_fixture`, `:1850-1855`); no per-class slots are needed.

## 5. Coordination

HarnessBuild was messaged twice with the case list, the `invalid_class=null` rationale, the exact positive matrix, the `honor`-mode requirement, and the `MORI_BOOT_ID` override. No reply was required or received before this report. CensusPositive's contract block (read at the snapshot above) settles the only ambiguity: parsed stream with no valid result record ⇒ real 0 positive, and the raw class stays available with `oom_result_unknown`.

## 6. Risks / residual limits

- The harness loader is owned by HarnessBuild and did not exist at write time; if it derives positive expectations by stringifying `UNIT_RESULT`, it would compute the same zeros but would not test the SUT's type check. The pack's array element includes both literals deliberately: any first- or any-element coercion fabricates an alarm and fails `want_oom`/`want_signal`.
- If the loader defaults to `ignore-filters`, these cases fail for the wrong reason (§4); this is a loader defect, not a SUT finding.
- `invalid_class` cannot express "raw class available, positive unknown-result excluded"; that distinction lives in the raw `unit_oom_result_unknown` split and the zero positive token, both stated above.
- Expectations are source-derived, not executed. The L1 post-integration gate is the first real run.
