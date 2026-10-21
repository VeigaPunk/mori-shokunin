# C1 critic — freshness re-pin

## Verdict

A classified re-pin can be a real freshness move, but only if the classifications are independently adjudicated against the changes being normalized. As frozen, the re-pin gate is self-certifying: the L1 may author the register, count its keys against its own drift output, and then pin the current census. `unclassified 8→0` proves token-key coverage only—not that a class or its reason is correct. Without a non-author review, the count is bookkeeping, and a bad current state can become the new expected state.

## Strongest falsifier: `-FINDING:WAVE_UNSETTLED_AGE`

- The measured entry capture includes this token (`.ufo/waves/round-20/evidence/c1-drift-entering.json:49`). The r10 baseline still has separate `aggregator-r10` and `aggregator-r10-resume` warning rows (`corpus/evidence/baseline-r10-20261015T2231Z.json:26-27`).
- The drift renderer discards the per-wave identity for this removal: `drift_line_id` identifies a finding by finding name alone (`tools/mori-census.sh:2805-2817`), and an unmatched old row is reported as `-$id` (`:2888-2904`). The contract then sorts/uniques tokens and counts only missing register keys (`.ufo/waves/round-20/contract.md:36-47`). Thus this token cannot itself say which old wave disappeared, how many instances disappeared, or whether each was explicitly settled.
- There is already relevant non-author counterevidence. The round-12 receipt identifies its author as the L2 scout (`corpus/evidence/drift-r12-20261019T2204Z-classification.md:3`). It records that commit `e20f4fa` deleted evidence under both aggregator-r10 wave directories (`:30`), and explicitly says the old directories' missing registry/dispatch/run markers do **not** prove settlement; it classified the change as an evidence-strength regression (`:33`, `:41`). The census itself treats waves without settle or launch markers as empty, not as settled (`tools/mori-census.sh:893-899,917-923`).
- The prior register had already classified the generic removal only as `[INFERENCE]` about current activity (`.ufo/waves/round-13/evidence/drift-classification.json:37`). If the r20 register now calls this `live-state` or `census-schema-change`, the contract's gate would permit re-pin despite the documented evidence-loss counterexample. **[INFERENCE]** The inspected r12 receipt proves this failure mode is real, but does not establish the current settlement state of every wave at the r20 measurement time.

This is stronger than an abstract concern about the new class labels: the actual entry token is identity-lossy, and the existing independent receipt documents that missing wave markers can erase a warning without establishing closure.

## Why the count is not an independent check

The contract's `comm -23` compares sorted drift tokens to `.tokens|keys[]` (`.ufo/waves/round-20/contract.md:36-47`). A register author can make the result zero by adding keys; that does not validate the class, the reason, the evidence pointer, or whether the pointer establishes the stated cause. No non-author approval is part of the frozen acceptance condition. Separately, `--pin` records a DRIFT census and still succeeds; the census documentation explicitly says its CLEAN/DRIFT roll does not decide the pin exit (`tools/mori-census.sh:192-194`). So the safety decision rests entirely on the same author-authored classification the key-count measures.

## Non-author evidence that would decide this case

Have a non-author reviewer reconcile the r10 baseline-only wave IDs against the raw current canonical census and the exact wave records, then require an independent, explicit closeout/settlement record for each removed warning (for example, an owner-produced closure receipt or retained registry/result/closeout evidence). A deletion commit or absence of marker files is not closure evidence. If any removed wave lacks explicit closure evidence, treat the disappearance as unresolved/evidence loss and block the re-pin; do not classify the aggregate token as benign live-state. Preserve the per-wave ID mapping in the evidence so a single generic finding key cannot stand in for multiple row outcomes.

## Impacted axes

- **Freshness:** the new timestamp/reference is fresher, but freshness improvement is unproven if the pin can normalize unadjudicated regressions.
- **Calibration:** high risk; L1-authored labels and L1-counted keys are not independent evidence that the `census-regression` gate was correctly applied.
- **Depth:** the generic finding token hides row identity and multiplicity needed to audit the wave change.

## Smallest safe correction

Keep the r10 baseline unchanged and make the re-pin conditional on a non-author sign-off of the register. For `-FINDING:WAVE_UNSETTLED_AGE`, require row-level old/new wave IDs plus independent explicit settlement evidence; make any unexplained evidence disappearance a re-pin blocker. Keep the `8→0` count as a mechanical completeness check, not as the semantic acceptance proof.