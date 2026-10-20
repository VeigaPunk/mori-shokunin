# ReviewProcessPredicate — round-15 C1 (coverage) read-only audit

Scope: process positive predicate (`EXIT_CODE=killed` + scalar `EXIT_STATUS=9`) and the
positive-evidence path it must feed. Target: `tools/mori-census.sh` (census-r6 label, r13/r14
journal scopes). Read-only: no production edits, no builds, tests, linters, or smoke runs.

## Current state (verified by grep, 2026-10-20)

- `positive_kernel_oom`, `positive_unit_oom`, `positive_unit_signal`, `positive_process_sigkill`
  appear nowhere under `tools/` or `corpus/`. They exist only in wave spec/dispatch files.
  The required feature is **not yet implemented**; every finding below is a required fix.

## Process predicate anchors

1. `tools/mori-census.sh:975` — `JOURNAL_JQ_SIGKILL`:
   `(.EXIT_CODE == "killed") and ((.EXIT_STATUS | tostring) == "9")`
   - Arrays are rejected only by accident: `[9] | tostring` is `"[9]"`, not `"9"`. Nothing checks
     scalar type explicitly. A spec-level "reject arrays" guarantee should not rest on tostring.
   - `EXIT_STATUS` numeric `9.0` tostrings to `"9.0"` in jq 1.7 (rejected), while numeric `9`
     is accepted. Behaviour is inconsistent across jq versions and no fixture covers it.
   - This filter is the **aggregate** predicate. It is wrapped by `JOURNAL_JQ_TAIL` (`:973`), so
     any single non-matching record makes the whole class `record-invalid`. That is the
     positive-loss defect, not a predicate defect.

2. Required predicate (per-record, scalar-typed, exact):
   ```
   def scalar_str($v): ($v|type) == "string";
   type == "object"
   and (._BOOT_ID|type) == "string" and ._BOOT_ID == $boot
   and (.MESSAGE_ID|type) == "string" and .MESSAGE_ID == $id
   and (.EXIT_CODE|type) == "string" and .EXIT_CODE == "killed"
   and (.EXIT_STATUS|type) == "string" and .EXIT_STATUS == "9"
   ```
   Journal `-o json` emits every field as a string, so requiring `type == "string"` for
   `EXIT_STATUS` loses no real record. If numeric `9` must stay accepted for fixtures, accept
   `type == "number" and . == 9` explicitly. Do not rely on `tostring`.

## Positive-evidence path: the missing wiring

3. `journal_query` (`:1046-1136`) has no positive channel. Early returns at `:1054`, `:1089`
   (rc-N/timeout), `:1093` (stderr-nonempty), `:1102` (malformed-json), `:1104` (record-invalid /
   multi-boot / boot-mismatch) all discard the parsed stream. Positives must be computed from
   the same `CAP_OUT` **only** when `CAP_RC=0`, `err_bytes=0`, and the parse succeeded. Otherwise
   `positive_*=unavailable:<JQ_STATUS>`. Do not run a second journalctl query.
   Required: a separate `JOURNAL_JQ_POS_*` filter (or one filter emitting a column count) run on
   `"$CAP_OUT"` after the `:1099` parse. It must NOT be gated by the `all(.[])` aggregate test.
   It must return integer counts of individually valid records. `JQ_VEC`/`JQ_N` must not be
   relied on, because they are empty on the record-invalid path.

4. Call site `probe_journal` (`:1190-1230`): the `unit_sigkill_record` branch (`:1195-1196`) is the
   only place the process class is queried. The positive count must be captured there from the
   same `journal_query` invocation (e.g. `ppos[$scope]=...`). Do not add a new query.

## Alarm gating (the actual C1 defect)

5. OOM block `:1303-1332`:
   - `:1305` and `:1307-1313` set `ko`/`uo` to `unavailable:<status>` when the aggregate is invalid.
   - `:1314-1321` then never set `oom_fire`. Result: a valid `fe6faa94` or `oom-kill` record next to
     an invalid one stays silent. Required: also set `oom_fire=1` and `oom_path_k`/`oom_path_u`
     from `positive_kernel_oom` / `positive_unit_oom` (`>0`), independent of `ko`/`uo`.
   - `:1323-1325` `oom_fields` must add `user_positive_kernel_oom=`, `user_positive_unit_oom=`
     (and system counterparts). Keep existing raw `user_notice=`/`user_unit_oom=` tokens unchanged.
   - `:1328-1329` `oom_paths` values must stay `kernel_oom_notice` / `unit_result_oom_kill`.
     Harness regexes (`:3036`, `:3068`) match `paths=kernel_oom_notice` exactly. Do not add a
     `positive_*` value into `paths=`.

6. KILL_SIGNAL block `:1340-1354`:
   - `:1341` `ps` and `:1343` `us` become `unavailable:*` on invalid aggregate; `:1344-1351` then
     skip the fire. Required: fire from `positive_process_sigkill` / `positive_unit_signal` and add
     `process_sigkill_positive=` / `user_unit_signal_positive=` fields to `:1353`.
   - `:1353` `count=$ps process_sigkill=$ps` is retained; `count=` is the raw counter and may show
     `unavailable:record-invalid` while `paths=process_sigkill` is set from positives. That is
     acceptable only if the positive field is printed alongside it. The harness `:3043` regex
     tolerates appended fields.

7. Unit `oom`/`sig` predicates (`:1016-1017`) are exact-string and type-guarded; they are correct
   for `positive_unit_oom` (`UNIT_RESULT` exact `oom-kill`) and `positive_unit_signal`
   (`UNIT_RESULT` exact `signal`). Positive must NOT require a valid subject (`UNIT`/`USER_UNIT`):
   subject validity never gates the alarm (`:945`). The positive unit filter should reuse
   `oom`/`sig` without `subject`.

## Must-not-regress

- Existing raw tokens remain aggregate-only: `unit_fleet=`, `unit_oom=`, `signal=` etc. stay
  `unavailable:<reason>` when invalid (`:1373-1379`). Do not print positives into them.
- Positive on `rc-*`, `timeout`, `stderr-nonempty`, `malformed-json`: `unavailable:<reason>`,
  never `0`. Harness case `:3067` (rc1 unit query) must still show `unit_oom=unavailable:rc-1`
  and must not alarm. Add `positive_unit_oom=unavailable:rc-1` expectation there.
- OOM fires exactly once (`:1330`). Positive fire must reuse the same single `emit_finding`.
- No new route/actuation: findings only.

## Harness gaps for the owning seat (not edited here)

- Existing journal fixtures (`:3012-3025`) always carry valid `_BOOT_ID`/`MESSAGE_ID`. No case
  covers: a valid `killed`/`9` record beside a malformed or foreign-boot record (positive must
  survive, raw count stays unavailable); `EXIT_STATUS` as `["9"]`, `[9]`, `{"x":9}` (must be
  rejected); `UNIT_RESULT` as array (must not count as oom-kill); `stderr-nonempty` with valid
  positives (must be unavailable).
- Required distinct cases for the process predicate: (a) valid `killed`/`"9"` + foreign-boot
  invalid, (b) `EXIT_STATUS=["9"]` only, (c) `EXIT_CODE=["killed"]` with `EXIT_STATUS="9"`,
  (d) numeric `EXIT_STATUS=9` if numeric acceptance is retained.

## Severity

- HIGH: no positive channel exists; OOM and KILL alarms stay silent when any adjacent record is
  invalid (`:1314-1321`, `:1344-1351`). This is the C1 defect.
- MEDIUM: process predicate relies on tostring for scalar/array rejection (`:975`). Correct today
  for arrays but not explicit; numeric `9.0` behaviour depends on jq version.
- LOW: `count=` on the KILL finding mixes raw and positive semantics unless positive fields are
  printed beside it.

## Verification gaps

- Not executed (per assignment). Jq tostring behaviour for `9.0` is from jq 1.7 documentation,
  not measured on this host.

## Tooling

- No installs or updates performed. Host-safety override received (pacman dry-run gate and
  no `-Sy/-Syu/-U/-R`); none was needed for this read-only audit.
