# PackKernelSystem — round-16 report

## Files changed
- `.ufo/waves/round-16/fixtures/KernelSystem.json` (created, 4 cases, all `scope:"system"`)

## Source bytes verified before writing
Exact catalog MESSAGE_IDs read from `tools/mori-census.sh` (hashline snapshot C872):
- `JOURNAL_ID_KERNEL_OOM=fe6faa94e7774663a0da52717891d8ef` (line 1032) — the kernel-OOM
  notice id; `positive_kernel_oom` counts only this id (`JOURNAL_JQ_POS_KERNEL`, line 1053).
- `JOURNAL_ID_OOMD=d989611b15e44c9dbf31e3c81256e4ed` (line 1033).
- `JOURNAL_ID_COREDUMP=fc2e22bc6ee647b6b90729ab34a250b1` (line 1034).
- `JOURNAL_ID_UNIT_SIGKILL=98e322203f7a4ed290d09fe03c09fe15` (line 1035).
- `JOURNAL_ID_UNIT_FAILURE=d9b373ed55a64feb8242e02dbe79a49c` (line 1036).
- r15 predicates confirmed: exact string-equality on `MESSAGE_ID`, `UNIT_RESULT`
  `oom-kill`/`signal`, `EXIT_CODE=killed` + `EXIT_STATUS` "9"|9 (lines 976-984,
  1052-1055). No tolerance for near-miss ids.

Shared case schema copied byte-compatible from landed sibling packs
(`fixtures/KernelUser.json` #3AE7, `fixtures/MissingAnchor.json` #9081):
`{cases:[{id, scope, anchor{schema,scope,boot_id,cursor}, stdout(JSONL), stderr,
returncode, want_rc, want_id, want?}]}`; `want` is omitted on rc2 refusal cases.

## Cases authored
| id | stream after anchor | want |
|---|---|---|
| kernsys_oom_after_anchor_single | 1 same-boot fe6faa94 record | rc0 OK, records_after_anchor=1, positive_kernel_oom=1, all other positives 0 |
| kernsys_oom_fanout_after_anchor | 2 same-boot fe6faa94 records | rc0 OK, records_after_anchor=2, positive_kernel_oom=2 |
| kernsys_wrong_ids_after_anchor_never_kernel_positive | d989611b (oomd), fc2e22bc (coredump), **near-miss fe6faa94…d8ee** (one nibble off the kernel-OOM id) | rc0 OK, records_after_anchor=3, positive_kernel_oom=0 — exact-string predicate must not admit any of the three wrong ids |
| kernsys_oom_foreign_boot_after_anchor_refuses | 1 same-boot fe6faa94 then 1 fe6faa94 from boot `cccc…` | rc2 MORI_JOURNAL_WINDOW_UNAVAILABLE — foreign-boot record invalidates the window even though a valid positive exists |

Anchor: schema `mori-journal-anchor-v1`, scope `system`, boot `bbbb…` (32 hex),
realistic journalctl cursor string `s=…;i=40;b=bbbb…;m=4a40;t=…;x=a1b2c3d4`.
First JSONL record of each stream replays the exact anchor `__CURSOR`+`_BOOT_ID`
(the record the tool must prove and drop); later records carry distinct `__CURSOR`
values (incremented `i`/`m`/`x`) in the same boot. No `MESSAGE`, no numeric
totals leaked into fixture expectations beyond `want` counts.

## Notes / risks
- Wrong-MESSAGE_ID records remain valid window records (object, same boot, unique
  scalar cursor) — the contract's per-record gate does not require a catalog id,
  so rc0 with `positive_kernel_oom=0` is the intended arm, matching the
  KernelUser sibling convention.
- Foreign-boot case uses the kernel-OOM id on the foreign record deliberately:
  it asserts unavailable rather than a salvaged positive count, per the
  contract's "foreign boot -> rc2 unavailable, no numeric positive totals".
- No runs executed (contract). One local `python3 json.load` pass over the
  fixture file verified JSON/field-shape only — no invocation of the production
  tool, journalctl, harness, gate, or any live probe; no outside-lane writes and
  no /tmp output. Harness/tool digest pinning is WindowHarness's lane; no schema
  deviations needed coordination.
- No tools installed; no installs or updates performed this wave.
