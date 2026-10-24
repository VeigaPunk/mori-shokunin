# Round-14 dirty receipt: historical trace and provenance limits

## Axes and conclusion

- **Coverage:** R14 exercised structured journal alarms, six raw counters per scope, unit-result routing, and fail-closed aggregate behavior. It did **not** exercise the R15 requirement to retain a positive alarm from an individually valid record when another record invalidates the aggregate class.
- **Provenance:** R14 has committed harness and measurement receipts; the later source entries S014/S015/S037/S038 explain query mechanics and field meaning. These establish supported record vocabulary and distinctions, not event completeness or live conformance.
- **Non-harm:** Keep R14's unavailable raw-count semantics on an invalid class; the intentional R15 change is preserving independently validated positive evidence, not manufacturing a total or treating invalid records as zero.

## Evidence chain (committed lane data)

| Commit / artifact | What it records | Limit relevant to C1 |
|---|---|---|
| `a5cc313` — “pin rejected cutover and repair expectations” | The frozen pre-repair census and expected behavior were pinned. | A pinned historical control, not evidence about the later R15 behavior. |
| `8d22d18` — “restore structured OOM alarms and subject-unit triage” | The R14 repair baseline and its structured alarm/routing design. | Its class-level validation still rejects a mixed invalid stream as a whole. |
| `5601d1201926124f7884bc694568abac2ead6d5c` | `red-before-accepted.json`, `green-after-accepted.json`, `c1-measurement.json`, `live-measurement.json`, and `drift-current.json` identify this measured commit. | These are observations at that commit, not current R15 execution. |
| `52512ae` — “land red-green repair evidence and calibrated verdicts” | Commits the accepted R14 report and evidence bundle. `build/JournalRegression.md` names harness `c39e5a7352666d09dc662293e1ea7be47ee3523b53247a5a6ae02e7dda19288d`. | The bundle preserves its own assumptions; it does not broaden what the harness tested. |

The accepted red-before receipt used the frozen target and reports exit 1, 43/43 claims failing. The accepted green receipt reports exit 0, 44/44 claims passing (43 cases plus the frozen-control claim). `c1-measurement.json` narrows the meaningful before/after behavior differential to six selected arms—user/system kernel OOM, unit `oom-kill`, fleet/nonfleet routing, and user unit signal—6 failing on frozen bytes and 0 on the repaired census. It separately records parity of all 12 raw-count cells (six counters in each of user and system scopes). The report explicitly cautions that 43/43 failing is **not** 43 production defects: the frozen schema lacks the added unit tokens/query fields, including in controls. The receipts record observations, not fixture specifications; shared case IDs and harness bytes do not establish byte-identical temporary fixture trees.

The R14 live-measurement receipt is a different, bounded observation: at `2026-10-20T06:44:08Z`, it reports all six selected class counts as zero before and after in both scopes, with 12/12 count comparisons matched and two scoped rows. Its census executions both returned exit 1; the saved output includes unrelated watchdog, wave, roster, and other drift findings. This supports only that those queried counts were zero in that capture. It is not a positive-record test, a proof that no events occurred outside the query/retention boundary, or a test of mixed valid/invalid records.

`drift-current.json` is another exit-1 receipt at `5601d12`: `bash tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json`, stderr empty, census SHA-256 `0e41cb83fce2e8c5c711171e1cde2e6fa2809dcfce630eccabe52bcbe41516d9`. Its `MORI_DRIFT` output contains delta markers for `JOURNAL_CLASSES_UNMEASURED`, `ROSTER_SET_MISMATCH`, and `WATCHDOG_STATE_LAG`, among other surfaces and findings. The `+`/`-` markers are a comparison against that R10 baseline; they are not journal-record evidence or a positive alarm oracle. Thus this is a *dirty* broad drift receipt, not a clean-status claim and not an R15 gate result.

## Last-known-good invariant and R15 divergence

The R14 contract (`round-14/scoped-counter-contract.json`) keeps the six raw totals separate by `user`/`system`, treats them as record/notice counts rather than unique victims, never sums scopes, and keeps positive OOM alarms independent of subject classification. The R14 regression report documents a retained `R14_SEC_DUP_MSGID_MIXED` control: a matching OOM `MESSAGE_ID` alongside a `MESSAGE_ID` array makes the **aggregate class** `record-invalid`, avoiding a fabricated zero; the stored green evidence marks that old expectation as passed.

That edge is the relevant divergence. R14's all-or-nothing class behavior can suppress a real positive alarm when the same stream also contains an invalid record. R15 C1 intentionally changes only the positive-evidence path: a positive token may be derived from each object record that independently satisfies the scalar matching `MESSAGE_ID` and scalar current `_BOOT_ID` checks (and, for unit/process positives, the exact required result fields). A matching valid positive must still alarm even when another record invalidates the aggregate. Raw aggregate/split counts remain unavailable for the invalid class. The R14 control is therefore historical evidence of the old behavior, not a contrary acceptance rule for R15 and not proof that R15 has implemented the new rule.

## What the reopened provenance establishes—and does not

`corpus/SOURCES.md` records the following source scopes:

- **S014** (`journalctl(1)`): scope selection, cursor/query mechanics, and field-limited JSON output. This supports querying structured fields by scope; it does not guarantee retained-event completeness or validate the parser's per-record acceptance logic.
- **S015** (`systemd.journal-fields(7)`): `MESSAGE` is display text rather than metadata; `MESSAGE_ID` is a typed key; underscore-prefixed fields are trusted. This supports avoiding text matching and explains the boot-metadata trust distinction. It does not make a matching `MESSAGE_ID` an authenticated claim about a unique victim or prove that a queried result set is exhaustive.
- **S037** (`systemd.journal-fields(7)`): `UNIT`/`USER_UNIT` describe the unit a manager logs about, while `_SYSTEMD_UNIT` describes the emitting process and need not be the failed subject. This supports subject-field selection and prevents treating the emitter as the subject; it does not authenticate fleet ownership or establish exhaustive attribution.
- **S038** (pinned systemd `service.c`): `SERVICE_FAILURE_OOM_KILL` maps to the exact result string `oom-kill`. This supports that structured selector's vocabulary, not that an event occurred, that all such events were retained, or that there was one unique victim.

These sources make the field-level C1 rule explainable and auditable. They cannot, by themselves, prove that R15's implementation accepts every valid positive independently, rejects every unsafe record, reuses the same captured stderr-free valid JSON stream, preserves all raw unavailable tokens, or emits each alarm once. Those are implementation and fixture/harness questions outside this historical investigation. No gate, build, test, formatter, or runtime was executed here; this report reads committed R14 evidence and source-registry provenance only.

## Confidence

**High** for the R14 receipt values and stated old mixed-record expectation: they are recorded in the accepted JSON/report artifacts committed by `52512ae`. **High** that the saved live receipt is limited to the zero counts and non-clean drift stated above. **Medium** for mapping that old behavior to the intended R15 divergence: it follows directly from the R14 contract/report and the R15 shared contract, but this seat did not evaluate R15 implementation or fixture execution.