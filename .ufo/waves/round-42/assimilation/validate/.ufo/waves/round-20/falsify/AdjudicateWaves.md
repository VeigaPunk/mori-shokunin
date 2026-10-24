BROKEN

## Counterexample and class

For the removed old-wave evidence, the safe class is `census-regression` (unresolved loss of observability), not `live-state`. The fleet change explains why the inputs disappeared; it does not establish that either wave settled. The frozen contract names the four classes and makes `census-regression` a pin blocker, but does not define their semantics; therefore the register's cause-based `live-state` choice is not compelled by the contract. Given the stated blocker and the evidence available, treating unproven settlement as benign live state is unsafe.

The concrete counterexample is `aggregator-r10` and `aggregator-r10-resume`: both were warning rows in the r10 baseline, then their marker files disappeared in the fleet sweep. The census emits `WAVE_UNSETTLED_AGE` only when a directory has a registry/dispatch/run marker and exceeds the age threshold; otherwise its branch counts the directory as empty. The round-12 receipt explicitly says the missing markers “does not prove settlement.” The current register itself records this blind spot, but assigns `live-state` anyway. This is evidence loss that can turn a warning into absence without proving closure. The separate `obs` change for the newly aged `shokunin-train-20261016-w24` is live-state; the lossy aggregate drift token does not justify treating the removed old-wave evidence the same way.

## Would re-pinning hide a condition?

It would hide the change from the **drift comparison**, not erase current census output. The r20 baseline still contains ten `WAVE_UNSETTLED_AGE` warning rows and a `MORI_CENSUS: DRIFT` verdict, including the current w24 warning. Thus raw census output continues to expose those current warnings, while a post-pin `MORI_DRIFT: none` means only “unchanged since this pin,” not healthy. The actual settlement state of the deleted aggregator waves is unknown; the evidence does not establish that those waves are still unsettled, nor that the census can currently see them.

## Evidence

- Frozen gate and missing class definitions: `.ufo/waves/round-20/contract.md:22-47` (only `census-regression` blocks re-pin).
- Baseline rows: `corpus/evidence/baseline-r10-20261015T2231Z.json:26-36`.
- Probe condition and empty branch: `tools/mori-census.sh:917-927`; warning contract: `tools/mori-census.sh:860-864`.
- Independent prior receipt: `corpus/evidence/drift-r12-20261019T2204Z-classification.md:33,39-41` (removed markers do not prove settlement; identifies evidence-loss regression).
- Current pin preserves ten warnings and DRIFT: `corpus/evidence/baseline-r20-20261021T1051Z.json:54-69`.
- Current register admits the blind spot while using `live-state`: `corpus/evidence/drift-classification-r20.json:207-211`; row-pairing and old/new wave mapping: `.ufo/waves/round-20/build/TokWaves.md:59-81,92`.
- Pin/drift semantics: `tools/mori-census.sh:192-210`.

## Impacted axes and smallest safe correction

- **Freshness:** re-pinning would baseline an unresolved loss of evidence and suppress that change in future drift comparisons.
- **Calibration:** “live-state” is used as a pass-through despite the recorded blind spot; code-byte identity alone does not establish that the observed wave state is complete.
- **Depth:** the generic finding token loses row identity and multiplicity.

Keep the r10 baseline unchanged and block this re-pin as `census-regression` until a non-author record accounts for each removed wave (explicit settlement or an evidenced cleanup disposition). Preserve the row mapping; classify the newly aged w24 observation separately as `live-state`. A `blind_spot` note is not a substitute for satisfying the contract's pin gate.

No census, `--pin`, or `--drift` command was run for this review.