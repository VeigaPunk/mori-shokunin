# R12 prior evidence-loss warning

**Source:** `corpus/evidence/drift-r12-20261019T2204Z-classification.md`, § A, line 33; corroborating caveat line 41. The receipt reports an observation at `2026-10-19T22:03:56Z` (lines 7–8).

**Bounded source excerpts** (quoted from the cited lines):

> “Baseline had 11 IDs: `aggregator-r10`, `aggregator-r10-resume` … Live had 10 … The old aggregator directories no longer contain the registry/dispatch/run markers used by the probe; empty directories are not counted as unsettled. **Their disappearance does not prove settlement.**” (line 33)
>
> “Yes—coverage/evidence-loss regression; actual settlement is **[UNKNOWN]**” (line 33)
>
> “deleted wave markers make old waves disappear from the unsettled set without proving settlement.” (line 41)

**Observed:** The report classifies the missing `aggregator-r10` and `aggregator-r10-resume` unsettled-wave observations as a coverage/evidence-loss regression. It records that baseline contained both IDs and the live set did not; the probe treated directories lacking the stated markers as empty. The report also says the drift summary matched the underlying changed IDs (line 41).

**Inference:** Disappearance from the live unsettled set is not evidence that either wave settled; the historical warning identifies loss of required evidence, not a settlement outcome.

**Unresolved:** Whether either wave actually settled is explicitly unknown in the source. This is a historical-document finding only; no live census or source edit was performed.