# AttackCountVacuity: attacking fake zero and fake totals from validated-positive subsets (round 15, C1)

Role: report-only critic. Nothing in production was edited, and no build, test, census, or stub
was executed. I made no installs. The host-safety amendment arrived mid-task, and no tool was
needed. All reasoning is static, against `tools/mori-census.sh#DC7D` and
`tools/mori-round14-regressions.py#ECA7`.

Axes: coverage (judged) — milestone "retain validated positives without fabricated totals".
Context axis: operability (raw tokens and unavailable semantics must not regress).

Entering state: `positive_` has zero hits in `tools/mori-census.sh`. The four tokens do not exist
yet. This attack therefore targets the contract and the plan in
`build/ReviewUnitPredicate.md`, not landed code.

External ground truth (fetched): systemd's Journal JSON Format
(https://systemd.io/JOURNAL_EXPORT_FORMATS/) states that a field set more than once in one entry
is serialized as an **array**, a non-printable or non-UTF-8 field as a **number array**, and a
skipped huge field as **null**. So an excluded record is not necessarily a corrupt one. It can be
a real current-boot OOM notice or SIGKILL record whose field was multi-valued. Excluding it is
correct; reporting the remaining subset as a total is not.

---

## CV1 (high) — a bare integer positive on an invalid aggregate is a fake zero or total

- **Counterexample.** The user kernel-OOM query returns exactly one record:
  `{"_BOOT_ID":"11111111111111111111111111111111","MESSAGE_ID":["fe6faa94e7774663a0da52717891d8ef","fe6faa94e7774663a0da52717891d8ef"]}`.
  This is a multi-valued MESSAGE_ID, legitimate per the systemd doc.
  - The aggregate filter `JOURNAL_JQ_MSGID` (`:974`) fails `all(...)`. The else-branch of
    `JOURNAL_JQ_TAIL` (`:973`) prints `record-invalid`. `journal_query` returns at `:1104`.
    The row reads `kernel_oom_notice=unavailable:record-invalid` (`:1366`).
  - The per-record positive pass correctly excludes the record (non-scalar MESSAGE_ID), so it
    finds 0.
  - If that is emitted as `positive_kernel_oom=0`, the row's only numeric OOM quantity is a zero
    sitting next to an unavailable raw. Readers, harness regexes, and drift all see "0 kernel OOM
    notices this boot", but the one excluded record *was* a kernel OOM notice.
  - Mixed variant: `[valid OOM, the record above]` gives `positive_kernel_oom=1`. That reads as
    "one notice", while the true number of fe6faa94 records is 2. It is a lower bound presented
    as a count.
- **Contract clause violated:** "unsafe/nonmatching records excluded, never interpreted as
  numeric-zero total".
- **Impacted axes:** coverage (false negative evidence), operability (unavailable becomes a
  look-alike 0 — the exact r13 lesson "never a look-alike 0", `:950-953`, `:1369-1371`).
- **Smallest required behavior.** Keep the four contract names and encode the basis in the value:
  - Parsed aggregate `ok`: `positive_<cls>=N`. N MUST equal the raw value (see CV6).
  - Parsed aggregate `record-invalid|multi-boot|boot-mismatch`: `positive_<cls>=subset:N:<status>`,
    for example `positive_kernel_oom=subset:0:record-invalid`. Fire logic uses N.
  - Capture or parse failure (`timeout`, `rc-*`, `stderr-nonempty`, `malformed-json`,
    `no-timeout-bin`): `positive_<cls>=unavailable:<same reason as raw>`.
  - No bare integer ever appears on a non-`ok` aggregate. The value self-declares as a lower
    bound, which also fixes CV3 without a new token name.
  - Equivalent alternative: a companion `positive_<cls>_basis=subset:<status>` token. That widens
    the interface, so the value form is smaller.

## CV2 (high) — substituting positives into existing count fields fabricates totals

- **Anchors:** `KILL_SIGNAL_JOURNAL ... count=$ps process_sigkill=$ps user_unit_signal=$us`
  (`:1353`); `user_notice=$ko user_unit_oom=$uo ...` / `system_notice=... system_unit_oom=...`
  (`:1323`, `:1325`).
- **Counterexample.** The user SIGKILL query returns `[valid {EXIT_CODE:"killed",EXIT_STATUS:"9"},
  {same but EXIT_STATUS:["9","9"]}]`. Real journalctl's `EXIT_STATUS=9` match admits the
  multi-valued entry.
  - The aggregate is `record-invalid` and `ps=unavailable:record-invalid`. The positive is 1, and
    the warn must fire.
  - The tempting implementation (fire from the positive and set `ps`/`count` to it) prints
    `count=1`. That is a fabricated raw total: two SIGKILL records exist.
- **Required.** `count=`, `process_sigkill=`, `user_unit_signal=`, `user_notice=`,
  `user_unit_oom=`, `*_unit_oom_result_unknown=`, `system_*` stay exactly the raw
  `ko`/`uo`/`uou`/`ps`/`us` (unavailable when invalid). Positives are **appended** as separate
  per-scope fields, never assigned into the raw variables.
  - Expected literal for this case:
    `count=unavailable:record-invalid process_sigkill=unavailable:record-invalid ... positive_process_sigkill=subset:1:record-invalid`.
  - Forbidden: `count=1`.
- **Impacted axes:** coverage (finding honesty), operability (raw semantics regress).

## CV3 (medium) — `basis=scoped-record-count` is false provenance on a subset-only fire

- **Anchors:** `basis=scoped-record-count` is hardcoded at `:1331` (OOM crit) and `:1353`
  (KILL warn).
- **Counterexample.** In the CV1 mixed variant, the crit fires only from a validated subset while
  every raw OOM counter is `unavailable:*`. The line still claims a scoped-record-count basis, but
  no complete scoped count exists.
- **Smallest correction.** The CV1 value form (`subset:N:<status>`) carries the provenance inside
  the positive fields, so `basis=` can stay byte-identical (no drift churn). Without CV1's form,
  the line would need `basis=` qualified when any firing path is subset-only.
- **Impacted axis:** coverage (provenance).

## CV4 (medium) — no upgrade of surface state from positives

- **Anchor:** `st=unavailable` is set when any class token is unavailable (`:1365`) and emitted at
  `:1387`.
- **Counterexample.** An implementation that marks `journal.user: ok` because positives were
  computed would tell a reader that the class set is complete.
- **Required.** Surface state is computed from raw class status only, as now. Positives are
  additive tokens. A row with `kernel_oom_notice=unavailable:record-invalid` stays
  `SURFACE journal.user: unavailable`.

## CV5 (high) — cross-stream double counting under the ignore-filters stub

- **Anchor:** the stub in `ignore-filters` mode returns every record of the scope to *every*
  class query (`mori-round14-regressions.py:510-528`). `probe_journal` runs six class queries per
  scope (`:1190-1220`).
- **Counterexample.** `user:[one valid kernel OOM record]` in ignore-filters mode. Every user class
  stream now contains that record.
  - Suppose the positive pass is a shared helper that evaluates all four predicates
    (kernel/unit-oom/unit-signal/process) on whatever stream it is handed, then accumulates.
  - Then `positive_kernel_oom` counts the record once per stream: 6 for the user scope, or
    2 if run on only the kernel and unit streams. That is a fabricated total from duplicate
    delivery.
- **Required.** Each positive is counted only from its own class stream, with that stream's own
  `$id`:
  - `positive_kernel_oom` comes from the `kernel_oom_notice` query only.
  - `positive_unit_oom` and `positive_unit_signal` come from the `unit_failure_record` query only.
  - `positive_process_sigkill` comes from the `unit_sigkill_record` query only.
  - oomd, coredump, and segfault streams contribute nothing.
  - Expected literal for the case: user `positive_kernel_oom` value N = 1, `want_oom=true`.
- **Impacted axis:** coverage (fabricated totals).

## CV6 (medium) — on a valid aggregate, positive must equal raw

- **Invariant.** When the class status is `ok`:
  - `positive_kernel_oom == kernel_oom_notice`
  - `positive_unit_oom == unit_oom`
  - `positive_unit_signal == unit_signal`
  - `positive_process_sigkill == unit_sigkill_record`

  Any difference means the positive predicate is not the per-record restriction of the
  aggregate predicate.
- **Counterexample A (numeric status).** The aggregate accepts
  `(.EXIT_STATUS | tostring) == "9"` (`:975`), so it accepts both the string `"9"` and the
  number `9`. The stub's honor filter `str(9) == "9"` also passes it (`:523`).
  - A string-only positive prints `positive_process_sigkill=0` while `unit_sigkill_record=1`.
  - The same record behind an invalid sibling would then be silently dropped, and the warn lost.
- **Counterexample B (subject gating).** In r14 case `:3134-3138`, a subjectless `oom-kill` gives
  `unit_oom=1`.
  - A positive that reuses `subject`/`fleet` (`:1001-1015`) gives 0.
  - Behind an invalid sibling, the global crit is lost. That contradicts `:945` "Subject validity
    never gates the alarm".
- **Required:**
  - Process positive accepts a scalar string `"9"` or number `9` (type in string/number, then
    `tostring == "9"`), and `EXIT_CODE` must be the string `"killed"`.
  - Unit positives ignore subject entirely.
  - Harness asserts the invariant on every `invalid_class == null` case.

## CV7 (medium) — positive-pass failures must not collapse to 0, and must not change raw reasons

- **(a) Unguarded field access.** `"x"._BOOT_ID` is a jq runtime error. A positive filter that
  does not short-circuit on `type == "object"` exits nonzero.
  - If the positive pass lives in the same jq invocation, the whole class becomes
    `malformed-json` (`:1102`). That changes the raw reason from `record-invalid` and loses the
    alarm.
  - If it is a separate jq invocation whose failure is defaulted to 0, it prints a fake zero.
  - Required: guard every access behind `type == "object" and` (jq `and` short-circuits). A
    positive-pass failure maps to `unavailable:<reason>`, never 0.
- **(b) Status parsing.** `case "$parsed" in record-invalid|multi-boot|boot-mismatch)` is an
  exact match (`:1103-1105`). If the filter now prints `record-invalid\t<positives>`, it misses
  that branch. The width check at `:1112` then turns it into `malformed-json`.
  - This regresses r14's pinned reasons: `:3222` `unavailable:record-invalid`, `:3228`
    `unavailable:boot-mismatch`, `:3236` `unavailable:multi-boot`.
  - Required: split off the status word, keep the raw reason byte-identical, and run `is_int` on
    every positive column (the same discipline as `:1114-1116`) so record bytes cannot forge a
    value.

## CV8 (high) — fixture and harness vacuity: the schema cannot see CV1–CV6, and the stub hides invalid records

- **(a) Schema blind spot.** The schema's oracle is `{want_oom, want_signal, invalid_class}`.
  - A `NegativeInvalid` case (`want_oom=false`) passes whether the SUT prints
    `positive_kernel_oom=0` (fake zero), `subset:0:record-invalid`, or `unavailable:*`.
  - A `FanoutPositive` case passes with `positive_kernel_oom=6` (CV5).
  - `invalid_class` is a single string with no scope, so a CrossScope case (user invalid, system
    valid) cannot say which scope's raw token must be unavailable.
- **(b) Honor-mode filtering drops the very records under test.** The stub compares
  `str(rec.get(k)) != v` for each match word (`:518-528`).
  - `MESSAGE_ID:["fe6f…"]` becomes `"['fe6f…']"` and is filtered out.
  - The same happens to `EXIT_STATUS:["9"]` and `EXIT_CODE:["killed"]`.
  - These records never reach jq. The aggregate stays `ok` and the case is green on the
    **entering** census too. That is vacuous, the opposite of how real journalctl matches
    multi-valued fields.
  - Only `_BOOT_ID` (not a match word, `-b` is ignored at `:450`) and unit-stream fields other
    than MESSAGE_ID survive honor mode. r14 already needed `dup-kernel` mode for exactly this
    (`:1555-1559`).
- **(c) Non-object records can't be expressed.**
  - In honor mode, a JSON string line makes `rec.get` raise, so the stub dies with rc 1. The case
    then tests `unavailable:rc-1`, not record handling.
  - In ignore-filters mode, it is emitted as `{}` (`:540-543`: `k in "x"` is a substring test).
  - Non-JSON lines become the object `{"_malformed": …}` (`:504`), never a jq parse error.
- **Required (harness owner, smallest):**
  1. For each case with `invalid_class != null`, assert the SUT row token
     `<invalid_class>=unavailable:` appears in at least one named scope. Better: the pack states
     the scope. This proves the invalid record reached jq.
  2. Every case with `invalid_class != null` and `want_oom` or `want_signal` true must be red on
     the frozen entering census (`0e41cb83…`). A case green on both is vacuous and must fail the
     gate.
  3. Cases whose invalid field is a match word (MESSAGE_ID, EXIT_CODE, EXIT_STATUS) must use
     `ignore-filters`, or a per-class `dup-*` mode like `dup-kernel`, so the stream actually
     carries the record.
  4. Assert no bare integer `positive_<cls>=[0-9]+` when the same scope's raw class token is
     `unavailable:`.
  5. On `invalid_class == null` cases, assert positive == raw (CV6).
  6. Assert the positive N equals a static count derived from the case records (CV5).

## CV9 (tradeoff, not a defect) — drift masking

- `positive_*` keys are not in `DRIFT_COUNTER_KEYS` (`:2254-2270`). Because `_` is a word
  character, `\b(oom|count)=` (`:2292`) does not mask `positive_unit_oom=` either.
- Positive values are therefore unmasked: any count change flips drift. With the positive above
  0, the crit already flips DRIFT, so the extra exposure is real but bounded.
- Adding the keys changes `DRIFT_VOLATILE_LIST`, which yields `MORI_DRIFT: volatile_fields`
  against existing baselines (`:2482`). That needs a recorded re-pin reason.
- With the CV1 value form, a `=[0-9]+` mask can never erase the `subset:` marker. L1 decides;
  this is not a count-vacuity defect.

---

## Correction summary (ordered by harm)

1. **CV1/CV3.** Positive values are an `ok`-path integer, `subset:N:<status>` on a parsed-invalid
   aggregate, and `unavailable:<raw reason>` on capture or parse failure. Never a bare integer
   beside an unavailable raw.
2. **CV2/CV4.** Raw variables and surface state are untouched. Positives are appended, never
   substituted (`:1305`, `:1311-1312`, `:1341`, `:1343`, `:1323-1325`, `:1353`, `:1365`).
3. **CV5.** One class stream per positive, using that stream's `$id`.
4. **CV6.** Positive predicate = per-record restriction of the aggregate predicate: number `9`
   accepted, subject ignored. Invariant positive == raw when `ok`.
5. **CV7.** Object-guarded jq. Separate status-word parsing keeps r14 reasons byte-identical.
   `is_int` on positive columns.
6. **CV8.** Harness proves each invalid record reached jq, red-controls every positive-preservation
   case, uses a non-honor stub mode for match-word fields, and checks positive values, not just
   alarm booleans.

## Verification gaps

- Static only. jq behavior for `tostring` on numbers such as `9.0` was not checked.
- No fixture packs existed in `.ufo/waves/round-15/fixtures/` at read time.
- Live journalctl matching on multi-valued fields is `[INFERENCE]` from the systemd JSON doc
  plus match semantics. It was not observed on this host.

Installs: none.

---

## Addendum (after peer `MoriR15.ReviewHarnessPacks` message; re-read of live files)

### Updated anchors

- **Stub anchors moved.** The stub file changed (`#ECA7` → `#9B04`), so the CV5/CV8 citations
  `:510-528` now sit at `:691-707`:
  - `ignore = MODE == "ignore-filters"` is at `:691`; `dup-kernel` is at `:692-694`.
  - The honor filter `str(rec.get(k)) != v` is at `:704`.
  - ReviewHarnessPacks confirmed CV8(b). There is no `dup-*` mode for EXIT_CODE or EXIT_STATUS
    arrays, only for the kernel MESSAGE_ID.
  - I agree with its schema addition: a per-case stub mode `honor|ignore-filters|dup-<cls>`,
    with ignore-filters mandatory when an invalid record carries a match-word field.
- **Red-control digest mapped.** `git show 0fa5e0d:tools/mori-census.sh | sha256sum` gives
  `0e41cb83fce2e8c5c711171e1cde2e6fa2809dcfce630eccabe52bcbe41516d9`.
  - So 0e41cb83 is the HEAD (`0fa5e0d`) blob of `tools/mori-census.sh`, the entering census
    named in the HarnessBuild spec.
  - It is not `.ufo/waves/round-14/frozen/mori-census.sh`, which hashes to `39abda0a…`.
  - The working tree is now `6e1f8d42…` (dirty, integration in progress). The harness must
    materialize the red control from the git blob, not from the working tree.
- **Census line anchors moved.** Integration is landing in `tools/mori-census.sh`
  (`#DC7D` → `#2EED`, +65 lines). Old → new anchors:
  - `:973-976` → `:1020-1023`
  - `:1103-1105` → `:1168-1170`
  - `:1331` → `:1396`
  - `:1353` → `:1418`
  - `:2254-2270` → `:2319-`

### Status of each counterexample against the in-flight integration (`#2EED`, partial; not final)

- **CV1 STILL OPEN — adopted in the doc.** `:978-981` says "a parsed stream with no individually
  valid record is a real 0 for the positive token (it is NOT a class total)".
  - That disclaimer lives in a code comment. Output would still print a bare
    `positive_kernel_oom=0` beside `kernel_oom_notice=unavailable:record-invalid`.
  - The CV1 counterexample (a lone multi-valued MESSAGE_ID OOM record) still yields that look-alike
    zero. The correction stands: `subset:N:<status>` on parsed-invalid aggregates.
  - The planned `user:<v>,system:<v>` alarm-field form (`:988-990`) has the same issue per
    scope value.
- **CV5 satisfied by design.** Positives use the class's own `$id` in `JOURNAL_JQ_POS_PRE`
  (`:1031`), run on that class's own stream.
- **CV6 satisfied in the filters.**
  - A: `JOURNAL_JQ_POS_SIGKILL` (`:1033`) accepts the string `"9"` or the number `9`.
  - B: `JOURNAL_JQ_POS_UNIT` (`:1034`) has no subject gate.
- **CV7(a) satisfied.** `select(type == "object" and …)` short-circuits (`:1031`).
- **CV7(b) STILL OPEN in the parser.** `journal_query` (`:1161-1200`) is not yet updated.
  - The planned output is two lines (`<aggregate>, (<positive>|@tsv)`, `:1025-1026`). The
    first line `record-invalid` would no longer exact-match `:1169` as `$parsed` (it now
    contains a newline).
  - `read -a` takes only the first line (`:1176`), so the width check gives `malformed-json`.
  - Required: split line 1 / line 2 before `:1168`, and keep the raw reason byte-identical
    (r14 `record-invalid`/`boot-mismatch`/`multi-boot` checks).
- **CV2/CV3/CV4 unverifiable yet.** `JQ_POS_VEC` is not consumed anywhere in `:1215-1470`, so
  the alarm, field, and surface wiring has not landed.

Still report-only. No production or harness edits. No installs.

---

## L1 adjudication (recorded verbatim in substance; supersedes the CV1 correction above)

### CV1: the `subset:N:<status>` value form is REJECTED

- **Ruling.** A numeric `positive_<cls>=0` means *exactly zero individually qualified witnesses
  in the successfully parsed captured stream*. It does NOT mean a complete total or an absence of
  events.
- **What L1 holds sufficient for honesty:**
  - The raw class token stays `unavailable:<reason>`.
  - A `positive_basis=validated-subset-lower-bound` token is emitted.
  - The documentation states explicitly that zero is not absence.
- **Capture or parser failure.** Production always prints `unavailable:<reason>` for positives,
  never a numeric value.
- **Effect on this report:**
  - The CV1 smallest-correction (value encoding) is withdrawn as a requirement.
  - The CV3 provenance concern is answered by `positive_basis=validated-subset-lower-bound`
    rather than by the value form.
  - CV2 and CV4 still apply as written: raw fields and surface state are never substituted or
    upgraded.
- **Residual for L1's own integration check (not a new claim).** At re-read time,
  `positive_basis` had zero hits in `tools/mori-census.sh`. The ruling's honesty argument depends
  on that token and the zero-not-absence doc text landing on every surface and alarm line that
  carries a positive value.
- **Harness consequence.** CV8 item 4 ("no bare integer positive beside an unavailable raw")
  becomes:
  - a numeric positive is allowed beside an unavailable raw;
  - `positive_basis=validated-subset-lower-bound` must be present on that line;
  - the positive value must equal the static count of qualified records in the case.

### CV7: must be caught by the final r14 suite

- The status-word parsing regression must be caught by the final r14 suite: two-line jq output
  turning `record-invalid`, `boot-mismatch` or `multi-boot` into `malformed-json`.
- r14 already pins those reasons. In the selftest at `#E6E4`, they sit at `:3375`
  (`record-invalid`), `:3381` (`boot-mismatch`) and `:3389` (`multi-boot`). The integration is
  still moving, so these anchors may shift again.
- No tests were run by this seat.
