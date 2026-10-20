# Round 15 fixture pack inventory (ScribeFixtureInventory)

Status: COMPLETE for the inventory scope. Read-only. No tests, builds, or harness runs. Counts come from jq over the files; no behavioral verification.

Revision: the first version of this report said the packs were missing. That was true at the time. All 16 packs have since landed, and this version replaces it.

## Census (observed)

- Files: 16 under `.ufo/waves/round-15/fixtures/`, all valid JSON arrays.
- Cases: 63 total. Per file: 4 each, except FanoutPositive.json with 3. Every file is within the 2–4 range.
- Duplicate case ids across all files: 0.
- Id charset: all ids match `^[A-Za-z0-9_-]+$`.
- Case key set: all 63 cases have exactly `id, invalid_class, system, user, want_oom, want_signal`.
- Types: `want_oom` and `want_signal` are boolean in all 63 cases. `user` and `system` are arrays in all 63 cases.
- `invalid_class` values: `kernel_oom_notice` 20, `unit_failure_record` 18, `unit_sigkill_record` 14, `null` 11. The 11 null-class cases are listed in "Open issues".
- Boot ids in records: the valid current boot `11111111111111111111111111111111` is the dominant value. Other values are `22222222222222222222222222222222` (foreign), `ffffffffffffffffffffffffffffffff`, and array forms (for example `["1111…","2222…"]`) and null/missing.

## Per-pack ids and expectations (case id, want_oom, want_signal, invalid_class)

BootArray (4): bootarray-user-kernel-oom-boot-array-current (T,F,kernel_oom_notice); bootarray-user-kernel-oom-boot-null (T,F,kernel_oom_notice); bootarray-system-kernel-oom-boot-array-multi (T,F,kernel_oom_notice); bootarray-user-unit-signal-boot-null (F,T,unit_failure_record).

CleanControls (4): clean-empty-user-and-system (F,F,null); clean-user-kernel-oom-homogeneous-three (T,F,null); clean-user-unit-signal-single (F,T,null); clean-user-process-sigkill-single (F,T,null).

CrossScope (4): crossscope_system_unit_signal_no_user_warn (F,F,null); crossscope_system_process_sigkill_no_user_warn (F,F,null); crossscope_user_boot_array_kernel_negative_vs_system_kernel_oom (T,F,kernel_oom_notice); crossscope_user_foreign_unit_negative_vs_system_unit_oom (T,F,unit_failure_record).

FanoutPositive (3): fanout-positive-msgid-array-kernel (T,T,kernel_oom_notice); fanout-positive-unit-boot-array (T,T,unit_failure_record); fanout-positive-process-boot-missing (T,T,unit_sigkill_record).

ForeignBoot (4): foreignboot_user_kernel_mixed (T,F,kernel_oom_notice); foreignboot_system_unit_oom_mixed (T,F,unit_failure_record); foreignboot_user_unit_signal_mixed (F,T,unit_failure_record); foreignboot_user_unit_oom_with_foreign_process_sigkill (T,F,unit_sigkill_record).

KernelSystem (4): kernsys_array_same_id_retains_valid_oom (T,F,kernel_oom_notice); kernsys_array_only_never_positive (F,F,kernel_oom_notice); kernsys_empty_array_retains_valid_oom (T,F,kernel_oom_notice); kernsys_multi_array_ordered_retains_valid_oom (T,F,kernel_oom_notice).

KernelUser (4): kernuser_wrong_oomd_id_retains_valid_oom (T,F,kernel_oom_notice); kernuser_two_valid_coredump_id_single_oom (T,F,kernel_oom_notice); kernuser_sigkill_id_without_status_retains_valid_oom (T,F,kernel_oom_notice); kernuser_missing_message_id_retains_valid_oom (T,F,kernel_oom_notice).

NegativeInvalid (4): NEG_INVALID_KERNEL_MSGID_ARRAY_USER (F,F,kernel_oom_notice); NEG_INVALID_UNIT_MSGID_ARRAY_USER (F,F,unit_failure_record); NEG_INVALID_SIGKILL_BOOT_ARRAY_SYSTEM (F,F,unit_sigkill_record); NEG_INVALID_KERNEL_BOOT_MISSING_SYSTEM (F,F,kernel_oom_notice).

NegativeResults (4): neg-results-user-array-oom-only (F,F,null); neg-results-system-null-with-valid-oom (T,F,null); neg-results-user-missing-with-valid-signal (F,T,null); neg-results-user-wrong-case-only (F,F,null).

NegativeStatus (4): negative-status-code-array-killed (F,F,unit_sigkill_record); negative-status-status-array-string9 (F,F,unit_sigkill_record); negative-status-status-null (F,F,unit_sigkill_record); negative-status-wrong-code-exited-adjacent-kernel-oom (T,F,unit_sigkill_record).

OrderMixed (4): order-kernel-forward-unit-oom-mixed (T,F,kernel_oom_notice); order-kernel-reversed-unit-oom-mixed (T,F,kernel_oom_notice); order-unit-signal-duplicated-array-poison (F,T,unit_failure_record); order-process-sigkill-duplicated-status-array-poison (F,T,unit_sigkill_record).

ProcessUser (4): process-user-valid-string9-plus-status-array (F,T,unit_sigkill_record); process-user-valid-numeric9-plus-status-null (F,T,unit_sigkill_record); process-user-status-array-only-no-positive (F,F,unit_sigkill_record); process-user-valid-string9-plus-wrong-scalar-137 (F,T,unit_sigkill_record).

SignalUser (4): signal_user_valid_only (F,T,null); signal_user_valid_plus_array_multivalue (F,T,unit_failure_record); signal_user_valid_plus_array_oom_claim (F,T,unit_failure_record); signal_user_array_only_not_positive (F,F,unit_failure_record).

SubjectUnknown (4): psu_missing_subject_foreign_boot (T,F,unit_failure_record); psu_array_subject_msgid_array (T,F,unit_failure_record); psu_ambiguous_subject_kernel_msgid_array (T,F,kernel_oom_notice); psu_system_ambiguous_subject_foreign_sigkill (T,F,unit_sigkill_record).

UnitSystem (4): unitsys_system_oom_valid_plus_unit_missing_boot (T,F,unit_failure_record); unitsys_system_oom_valid_plus_kernel_missing_boot (T,F,kernel_oom_notice); unitsys_system_oom_valid_plus_process_missing_boot (T,F,unit_sigkill_record); unitsys_system_oom_missing_boot_only (F,F,unit_failure_record).

UnitUser (4): unituser_msgid_array_retains_valid_oom (T,F,unit_failure_record); unituser_msgid_missing_retains_valid_oom (T,F,unit_failure_record); unituser_msgid_object_retains_valid_oom (T,F,unit_failure_record); unituser_malformed_signal_sibling_no_warn (T,F,unit_failure_record).

## Expectation taxonomy (as present in the packs)

1. Positive OOM (`want_oom: true`): valid current-boot OOM in user or system scope, sometimes beside an invalid record.
2. Positive user signal (`want_signal: true`): user UNIT_RESULT `oom-kill`/`signal`, or process `killed` with status 9.
3. Negatives: array, missing, object, or wrong-case MESSAGE_ID; array/missing/foreign `_BOOT_ID`; foreign-boot records; wrong-case or array UNIT_RESULT; process EXIT_CODE/status array, null, or wrong scalar; system-only signal that must not raise the user WARN.
4. Subject ambiguity: absent, array, or ambiguous subject does not suppress a valid global OOM.
5. Cardinality and order: several valid positives plus one invalid record (FanoutPositive, OrderMixed) are expected to give one OOM and one user WARN; reversed and duplicated orders are expected to give the same result.
6. Clean controls: empty and homogeneous valid inputs.

Each expectation is one boolean per case. These are expectations as written by the pack authors. I did not check them against the production parser; that is out of scope.

## Open issues (not resolved by this inspection)

- `invalid_class: null` on 11 cases, four of which contain malformed records by design. Examples: `neg-results-user-array-oom-only`, `neg-results-user-wrong-case-only`, `neg-results-user-missing-with-valid-signal`, and `neg-results-system-null-with-valid-oom`. The taxonomy only classifies MESSAGE_ID/boot/process-status invalid classes; UNIT_RESULT wrong-case/array/missing is not classified. This may be intentional, but it is not stated in the schema. The harness owner should confirm which meaning `null` carries.
- Every file is valid JSON and every key set matches the contract. Whether each pack's `want_*` values follow the independent-record semantics has not been checked against the production code.
- Whether the r14 stub supports the ignore-filters mode that KernelUser requested remains unverified.
- Whether each seat stayed inside its own file has not been checked beyond file names.

## Tooling

No installs or updates were performed.
