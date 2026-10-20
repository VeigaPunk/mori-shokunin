# ReviewUnitPredicate: unit OOM / signal predicate audit (round 15, C1)

Scope: read-only audit of `tools/mori-census.sh` unit OOM and signal predicates against the
round-15 contract (per-scope validated-positive tokens: `positive_kernel_oom`,
`positive_unit_oom`, `positive_unit_signal`, `positive_process_sigkill`). No gates, builds,
tests, or production edits were run or made. Nothing was installed (host-safety amendment
received; no install was needed for a read-only audit).

## Named axes
- Coverage (judged): valid current-boot positives must still drive the OOM crit and user
  KILL_SIGNAL warn when an adjacent record invalidates the aggregate class.
- Operability (context): aggregate tokens stay unavailable when invalid; no fabricated totals.

## Current-state finding
- `grep` for `positive_` in `tools/mori-census.sh` returns **zero hits**. The positive
  evidence tokens do not exist yet. Every OOM/signal gate is aggregate-only.

## Findings (by severity)

### F1 (high): aggregate gate discards independently valid positives
- `journal_query` (`tools/mori-census.sh:1046-1136`) validates the WHOLE stream at once.
  Any invalid record makes the entire class `record-invalid` / `multi-boot` /
  `boot-mismatch` (`:1102-1104`, `:1122`, `:1127`, `:1132-1134`).
- The class-level jq filters are all-or-nothing: `JOURNAL_JQ_MSGID` (`:974`),
  `JOURNAL_JQ_SIGKILL` (`:975`), and the unit filter's `if all(.[]; ...)` guard
  (`:1019`, fallback `:1037`).
- `probe_journal` only populates `ucnt[...]` when `JQ_STATUS=ok` (`:1202-1217`).
- OOM gate: `ko`/`uo`/`uou` fall to `unavailable:<status>` (`:1305`, `:1311-1312`) and
  `oom_fire` only sets from positive numeric aggregates (`:1314-1321`). One malformed or
  foreign-boot record therefore suppresses the crit even when a valid current-boot
  `fe6faa94` or `UNIT_RESULT="oom-kill"` record exists.
- KILL gate: `ps` (`:1341`) and `us` (`:1343`) are aggregate-only; the user warn at
  `:1344-1353` cannot fire for valid positives behind an invalid sibling.
- Fix: compute positives per record, independent of aggregate status (see Fix plan). Keep
  the raw/aggregate tokens exactly as they are (unavailable when invalid).

### F2 (high): positive pass must run before the aggregate early returns
- The aggregate early returns at `:1102` (malformed-json), `:1104` (record-invalid,
  multi-boot, boot-mismatch), and `:1122`/`:1127` all happen before `JQ_VEC` is set.
  A positive pass placed in `probe_journal` after `journal_query` returns would see no
  stream. The positive pass must run inside `journal_query` (or expose `$raw` for it) on
  the SAME captured stdout (`CAP_OUT`), after the capture checks at `:1083-1095`
  (`CAP_RC` nonzero and stderr-nonempty both make positives unavailable with the same reason)
  and before the `:1102` aggregate branch.
- No second `journalctl` call is needed; the contract says "same captured stream".

### F3 (medium): OOM finding must OR positives, keep raw tokens
- `:1314-1321` must also set `oom_fire=1` (and `oom_path_k`/`oom_path_u`) when
  `positive_kernel_oom` or `positive_unit_oom` is >0 in either scope.
- `:1323-1325` must append `positive_kernel_oom=<n|unavailable:reason>` and
  `positive_unit_oom=<n|unavailable:reason>` per scope (`user`/`system`) so the single
  `OOM_KILL_JOURNAL` line carries the evidence. Keep `user_notice`, `user_unit_oom`,
  `*_result_unknown` exactly as they are.
- `:1331` drift semantics unchanged: one alarm line per census.

### F4 (medium): user KILL_SIGNAL gate must use the positive tokens
- `:1340-1354`: gate on `positive_process_sigkill` (user scope) and `positive_unit_signal`
  (user scope). Keep `count=$ps`, `process_sigkill=$ps`, `user_unit_signal=$us` raw tokens
  and add `positive_process_sigkill=` / `positive_unit_signal=` fields to the same line.
- System scope stays info-only. Do not add a system KILL warn.

### F5 (low): surface row should expose positives for auditability
- The per-scope `journal.<scope>` surface (`:1356-1388`) should append the four positive
  tokens (user scope gets `positive_process_sigkill`, both scopes get
  `positive_kernel_oom`, `positive_unit_oom`, `positive_unit_signal`). This is additive
  only; do not change the raw token names or order at `:1360-1368`, `:1373-1379`.
- Do NOT add positives to the unit routing (`:1264-1291`); the owner partition stays
  aggregate-only unavailable per the contract.

### F6 (low): predicate hardening notes (jq)
- `subject` (`:1001-1014`) is irrelevant to the positive OOM predicate; subject validity
  must not gate `positive_unit_oom` (`:938-945` already states this for the alarm).
- `JOURNAL_JQ_SIGKILL` (`:975`) uses `(.EXIT_STATUS | tostring) == "9"`. For the positive
  filter add an explicit scalar guard: `((.EXIT_STATUS|type) == "string" or (.EXIT_STATUS|type) == "number") and ((.EXIT_STATUS|tostring) == "9")`, and
  `(.EXIT_CODE|type) == "string" and .EXIT_CODE == "killed"`. Arrays/objects must be excluded
  explicitly, not by tostring accident.
- Guard every field access behind `type == "object"` in the per-record filter. jq `and`
  short-circuits, so `type == "object" and (._BOOT_ID|type) == "string" and ...` is safe
  against non-object records (for example, bare strings).
- `MESSAGE_ID` and `_BOOT_ID` must be checked with `(|type) == "string"` before equality.
  Arrays or nulls must be excluded, never coerced.

## Fix plan (per-record positive pass, one jq over `$raw`)
Emit four integer columns plus a status, all computed from the same stream:

- positive_kernel_oom: object AND scalar string `_BOOT_ID == $boot` AND string
  `MESSAGE_ID == fe6faa94e7774663a0da52717891d8ef`.
- positive_unit_oom: as above with MESSAGE_ID `d9b373ed55a64feb8242e02dbe79a49c` AND string
  `UNIT_RESULT == "oom-kill"` (exact string; subject ignored).
- positive_unit_signal: as above with `UNIT_RESULT == "signal"`.
- positive_process_sigkill: object AND `_BOOT_ID == $boot` AND `MESSAGE_ID == 98e322203f7a4ed290d09fe03c09fe15` AND string `EXIT_CODE == "killed"` AND scalar `EXIT_STATUS` tostring `"9"`.

Status rules:
- capture rc nonzero (timeout/rc-N), stderr nonempty, or jq parse failure: every positive
  token reads `unavailable:<reason>` (never 0).
- valid capture, empty stream (`[]`): valid 0 for every positive. (Note: only this is a valid zero.)
- valid capture with some invalid records: the valid current-boot records still count;
  invalid records are excluded and never counted as zero.
- a non-array or non-object top-level input: parser failure, unavailable.

Where each positive lives:
- OOM crit: `:1303-1332` (ORed into `oom_fire`, appended to `oom_fields`).
- KILL warn: `:1340-1354` (user only).
- Surface: `:1356-1388` (additive tokens).

## Fixture expectations (for harness owner; not executed here)
Literal, SUT-independent expectations per the contract:
- Valid kernel OOM + one invalid sibling (foreign `_BOOT_ID`) in system scope -> OOM crit
  fires, `positive_kernel_oom=1`, `system_notice=unavailable:boot-mismatch`.
- Valid unit `oom-kill` + one non-string `UNIT_RESULT` (array) in user scope -> OOM crit
  fires, `positive_unit_oom=1`, `user_unit_oom_result_unknown=unavailable:record-invalid`.
- Valid process SIGKILL (`EXIT_STATUS` 9) + one malformed `EXIT_STATUS` ([9]) -> user KILL
  warn fires, `positive_process_sigkill=1`, `process_sigkill=unavailable:record-invalid`.
- Capture rc 124 with otherwise valid records -> every positive unavailable:timeout, no OOM
  or KILL fire from positives.

## Verification gaps
- Live `journalctl`/`jq` behavior with real `_BOOT_ID`/`UNIT_RESULT` types not observed;
  this audit is static only.
- No `.ufo/waves/round-15/fixtures/` pack exists yet (directory absent at audit time).
- Round-14 regression fixtures in `tools/mori-round14-regressions.py` are not yet extended for
  positive tokens.

## Installs / tooling
- None performed. Read-only audit; no package installs, no updates, no service restarts.
