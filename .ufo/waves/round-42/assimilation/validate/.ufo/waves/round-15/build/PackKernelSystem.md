# PackKernelSystem — round-15 fixture pack

## Assignment and scope

Own only `.ufo/waves/round-15/fixtures/KernelSystem.json`. Focus: a system-scope
kernel OOM record that is individually valid on the current boot, adjacent to a
record whose `MESSAGE_ID` is an array (never a scalar match). The intended
production behavior under test: the raw `kernel_oom_notice` aggregate stays
unavailable (`record-invalid`) while the independently valid scalar record still
produces `positive_kernel_oom` and the single OOM alarm. No production file was
edited. No harness, stub, or census command was executed.

## Files changed

- `.ufo/waves/round-15/fixtures/KernelSystem.json` (new; 4 cases). Schema is
  exactly `{id, user, system, want_oom, want_signal, invalid_class}` per the
  shared contract; no extra keys, no `MESSAGE`, no canaries.
  Post-write bytes: 1900; SHA-256
  `9c60778498e62a47f6dc16cb80ac52be4548a37b4fa7887485e96e8da6edcc3b`.
  The pack makes no provenance claim of its own; the harness must hash these
  bytes as it reads them (AttackProvenance CE6) rather than trusting this
  recorded digest, which is only a drift cross-check.
- `.ufo/waves/round-15/build/PackKernelSystem.md` (this report).

Constants used: `_BOOT_ID=11111111111111111111111111111111`, kernel
`fe6faa94e7774663a0da52717891d8ef`, unit
`d9b373ed55a64feb8242e02dbe79a49c`. All records are current-boot object maps
with scalar `_BOOT_ID` and either scalar or array `MESSAGE_ID`; every array
member is a string. User stream is empty in every case, so `want_signal=false`
also asserts that a system kernel/notice stream never produces the user
`KILL_SIGNAL_JOURNAL` WARN.

## Cases and expected alarm semantics

1. `kernsys_array_same_id_retains_valid_oom` — valid scalar kernel record then
   `MESSAGE_ID:[kernel-id]`. `want_oom=true`, `want_signal=false`,
   `invalid_class=kernel_oom_notice`. The array contains the queried id but is
   still not a scalar match: it must poison the raw aggregate without being
   treated as a numeric-zero count, while the scalar record keeps the alarm.
2. `kernsys_array_only_never_positive` — two array-only records
   (`[kernel-id]`, `[unit-id]`), no scalar valid record. `want_oom=false`,
   `want_signal=false`, `invalid_class=kernel_oom_notice`. Aggregate unavailable
   and no fabricated OOM: an invalid class is never an implicit zero and never a
   positive.
3. `kernsys_empty_array_retains_valid_oom` — valid scalar kernel record then
   `MESSAGE_ID:[]`. `want_oom=true`, `want_signal=false`,
   `invalid_class=kernel_oom_notice`. Empty array is neither a match nor a zero
   total; the independent positive survives.
4. `kernsys_multi_array_ordered_retains_valid_oom` — multi-id array
   `[kernel-id, unit-id]` before the valid scalar kernel record.
   `want_oom=true`, `want_signal=false`, `invalid_class=kernel_oom_notice`.
   Order independence: invalidity first does not discard the later scalar
   positive.

These four are concretely distinct in array arity/content and in ordering; case
2 is the negative control that separates "invalid aggregate" from "positive
evidence".

## Stub behavior retained from r14 (exact evidence)

`journal_stub_body` in `tools/mori-round14-regressions.py:404` is the reference
stub. Relevant behavior:

- Mode list (`:412-413`): `ignore-filters` returns every record of the scope
  regardless of filters; `dup-kernel` ignores filters only for the kernel
  `MESSAGE_ID` query (mixed valid + malformed stream); `mismatch-kernel` does the
  same for the kernel query and empties every other slot.
- Filtering (`:523`): `if str(rec.get(k)) != v` — an array-valued `MESSAGE_ID`
  stringifies to `"['fe6f…']"` and never equals the requested 32-hex id. In
  default `honor` mode the array record is dropped from the kernel query.
- Projection (`:539`): `--output-fields=_BOOT_ID,MESSAGE_ID` emits exactly those
  keys plus any present `ALWAYS` metadata (`:428`); these packs contain only the
  two requested fields, so the array reaches jq unchanged.
- No `MESSAGE` is requested or emitted; these records carry none.

Census-side (context, not re-verified): `JOURNAL_JQ_MSGID` at
`tools/mori-census.sh:974` requires every record to have
`._BOOT_ID` string equal to the boot and `.MESSAGE_ID == $id`; an array fails
that all-record predicate and lands in `record-invalid`. The round-15 positive
selector must run per record over the same captured stream, so only the scalar
record increments `positive_kernel_oom`.

## Required harness setting

`invalid_class=kernel_oom_notice` is only exercised if the stub actually
delivers the array-`MESSAGE_ID` record to the kernel-class query:

- Use r14 mode **`dup-kernel`** for these cases. The kernel query
  (`MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef`) then returns the whole system
  stream, producing `unavailable:record-invalid`; every other class query keeps
  honoring its own `MESSAGE_ID=<id>` filter and these packs leave it empty, so
  only `kernel_oom_notice` becomes unavailable — matching the single
  `invalid_class` field.
- `mismatch-kernel` is also acceptable (kernel sees the stream, all other slots
  are a valid empty stream), but it discards records that `dup-kernel` would
  have filtered normally, so `dup-kernel` is the preferred, more realistic
  setting.
- Do **not** use `ignore-filters` for this pack. That mode also returns the
  array record on the unit-failure and process-sigkill queries, invalidating
  `unit_failure_record` / `unit_sigkill_record` in addition to the one class
  named by `invalid_class`; a harness that asserts only the named class would
  pass for the wrong reason, and one that asserts other classes stay available
  would fail.
- Default `honor` mode does not exercise this edge at all: the array record is
  filtered before the census sees it, the aggregate stays valid, and
  `invalid_class` would be vacuous. If the harness cannot select a mode per
  pack/case, it must at minimum select `dup-kernel` whenever the case's
  `invalid_class` is `kernel_oom_notice`, or derive the mode from the presence
  of an array-valued `MESSAGE_ID` in the scope.

I sent this same shape/mode note to `MoriR15.HarnessBuild` for coordination.

### Confirmed loader convention (HarnessBuild reply)

- `invalid_class="kernel_oom_notice"` selects r14 stub mode `dup-kernel`; the
  gate does not use `ignore-filters` for a kernel-named invalid class.
- The affected scope is inferred from the poison record location — here
  `system` only — so the gate asserts
  `kernel_oom_notice=unavailable:record-invalid` on SURFACE `journal.system`,
  not on `journal.user`.
- Case 2: `want_oom=false` is checked as zero `OOM_KILL_JOURNAL` lines and
  `positive_kernel_oom=0` in the system surface.
- Cases 1/3/4: `want_oom=true` is checked as exactly one `OOM_KILL_JOURNAL`
  crit, `journal.system positive_kernel_oom=1` (each case has exactly one
  scalar valid kernel record), and the raw kernel aggregate unavailable as
  `record-invalid`. Positive fields are independent integer counts, not totals.
- No extra schema keys are consumed; `MESSAGE` keys are rejected with exit 2
  (this pack has none). The harness overwrites `boot_id` to
  `11111111111111111111111111111111` after fixture build.
- Derived invalidity rule: all records are objects, all `_BOOT_ID` equal the
  current boot, and at least one `MESSAGE_ID` is not scalar-matching → the
  class is `record-invalid`. This matches all four cases; case 2 contains only
  array-valued `MESSAGE_ID`s, so its aggregate is unavailable while its
  positive count is zero.

No fixture change was needed after confirmation.

## Risks and limitations

- The fixture asserts alarm presence (`want_oom`) and aggregate unavailability
  (`invalid_class`); it does not assert that `positive_kernel_oom=1` vs `>0`.
  The production contract is existential (any independently valid record), so
  both satisfy this pack; a stricter count assertion belongs to a harness
  positive-field check.
- `want_oom=true` in cases 1/3/4 depends on the intended round-15 selector
  counting a scalar kernel record even when the class aggregate is invalid. If
  the patched census still suppresses the alarm on `record-invalid`, these cases
  correctly fail; that is the regression being closed, not a fixture defect.
- Case 2's `want_oom=false` does not imply the aggregate is a valid zero; the
  `invalid_class` field carries that unavailability expectation.
- No execution was performed, so the stub-mode projection was reasoned from the
  r14 source, not observed. No tool installs were needed or made.

## Tooling

No installs or updates.
