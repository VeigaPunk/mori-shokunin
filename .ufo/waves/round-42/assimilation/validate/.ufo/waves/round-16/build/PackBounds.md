# PackBounds — .ufo/waves/round-16/fixtures/Bounds.json

## Files changed
- `.ufo/waves/round-16/fixtures/Bounds.json` (new, 3587 bytes, 4 cases)

## Cases

| id | scope | flag | expected |
|---|---|---|---|
| `timeout_user_anchor_plus_kernel_oom_and_sigkill` | user | `timeout:true` | rc2 `MORI_JOURNAL_WINDOW_UNAVAILABLE` |
| `timeout_system_anchor_plus_unit_oom` | system | `timeout:true` | rc2 `MORI_JOURNAL_WINDOW_UNAVAILABLE` |
| `overflow_user_cap_on_newline_after_positive` | user | `overflow:true` + `"max_bytes":235` | rc2 `MORI_JOURNAL_WINDOW_UNAVAILABLE` |
| `exact_limit_user_total_equals_max_bytes` | user | `"max_bytes":347` (no flag) | rc0 `MORI_JOURNAL_WINDOW_OK` |

Non-vacuity (critic AttackBound, adopted):
- Timeout prefixes are non-vacuous: case 1 carries anchor + kernel-oom positive
  (`fe6faa94…`, user scope) + unit SIGKILL positive (`98e32220…` EXIT_CODE=killed
  EXIT_STATUS=9); case 2 carries anchor + unit-oom positive (`d9b373ed…`
  UNIT_RESULT=oom-kill, system scope). Any parsed prefix must never yield
  numeric positive totals.
- Overflow case pins `max_bytes=235`: the decoded stdout's first 235 bytes end
  **exactly** on the `\n` terminating record 2 (anchor + one kernel-oom
  positive are complete within the cap), with one additional valid record
  beyond the cap. This catches a slice-to-cap-then-parse false-OK.
- Exact-limit case pins `max_bytes=347` equal to the total decoded stdout byte
  length (anchor + one benign padded `fc2e22bc…` coredump-notice record);
  catches off-by-one refusal. Asserted: records_after_anchor=1, all four
  positive counts 0, evidence_basis=validated-record-subsets.

## Catalog ids used (verified against tools/mori-census.sh@f1f8d1b6…, lines 1032–1036)
- `fe6faa94e7774663a0da52717891d8ef` kernel_oom_notice
- `98e322203f7a4ed290d09fe03c09fe15` unit_sigkill_record (+EXIT_CODE=killed, EXIT_STATUS=9)
- `d9b373ed55a64feb8242e02dbe79a49c` unit_failure_record (+UNIT_RESULT)
- `fc2e22bc6ee647b6b90729ab34a250b1` coredump_notice (benign/padding)

## Schema conventions (mirrored from landed sibling packs ExactAnchor/BootBoundary)
- Refusal cases use `"want": {}`; refusal asserted via `want_rc`/`want_id` only.
- `boot_id` `aaaaaaaa…`; anchor record is the first stdout line carrying the
  exact anchor `__CURSOR`; all stdout payloads are pure ASCII (byte length ==
  char length).

## Schema extension proposed (blocking coordination sent to WindowHarness)
- `"max_bytes": N` — optional per-case field; harness should invoke the tool
  with `--max-bytes N` measured against the UTF-8 length of the *decoded*
  `stdout` string. Without harness support, cases 3–4 degrade to unconsumed
  keys.
- Wrapper must write `stdout` byte-exact (no added trailing newline) or the
  exact-limit case flips to rc2.
- `timeout:true`/`overflow:true` are spec-authority flags; my cases assume the
  wrapper delays past the tool timeout / is paired with a byte bound the
  harness supplies when `max_bytes` is absent (case 3 supplies it explicitly).
- `want` reason-token assertion (`{"reason":"timeout"|"overflow"}`) was
  offered to WindowHarness; pending answer, sibling convention `want:{}` was used.

## Risks / open items
- If WindowHarness does not implement `max_bytes`, cases 3–4 need rewrite to a
  wrapper-flood overflow (re-coordination, not silent fallback).
- No stable `reason` substring is asserted for refusals (sibling convention);
  if the harness adds reason matching, `timeout`/`overflow` tokens strengthen
  cases 1–3.

## L1 compliance disclosure (required)
- No live journalctl queries, no probe loops, no tests/gates/builds/formatters
  run. One local `eval` python cell used only to compute fixture JSONL byte
  lengths/padding (static arithmetic, no file writes outside assigned path,
  no subprocess, no network). No outside-lane writes. No installs.
- Report only: advisory, no verification executed.
