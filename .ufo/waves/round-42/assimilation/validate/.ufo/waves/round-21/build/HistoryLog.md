# HistoryLog findings

**Axes:** C1 freshness; C2 calibration.

## R20 statement requiring qualification

The target is L1 MoriR20’s C1 paragraph in `LOG.md:1370-1375`: it records all 50 drift tokens classified (including `regression 0`), unclassified `8 → 0`, the r20 baseline pin, and post-pin drift `none`. Those are historical outputs, but the implied C1 freshness improvement/acceptance is superseded. Do not rewrite or erase the counts, timestamp, or pin event.

The r10 baseline still contains `WAVE_UNSETTLED_AGE` warnings for `aggregator-r10` and `aggregator-r10-resume` (`corpus/evidence/baseline-r10-20261015T2231Z.json:26-27`). The r20 classifier assigned the shared warning token `live-state` while documenting that both markers disappeared and cleanup receipts account for removal, not settlement (`corpus/evidence/drift-classification-r20.json:210-215`). The round-20 adjudication says the wave lifecycle is unknown and post-pin `none` means unchanged since pin, not healthy (`.ufo/waves/round-20/falsify/AdjudicateWaves.md:5-12,23-30`). Round-21 provenance records the removal and cleanup under the same actor and leaves `independent_wave_disposition` null and `settlement` unknown (`.ufo/waves/round-21/evidence/historical-provenance.json:19-40`).

QUALITY69 expressly supersedes QUALITY67: missing required evidence without independently evidenced per-identity disposition is `census-regression`, blocks baseline acceptance, and the r20 baseline is historical rather than an accepted reference (`corpus/QUALITY.md:263-274`). The contract requires both identities remain unresolved and baseline acceptance blocked while disposition is unknown (`.ufo/waves/round-21/contract.md:7-9`). Therefore neither the `regression 0` result under the old cause-only rule nor the post-pin `none` establishes freshness or acceptance. This is an evidence-assurance classification, not a finding that either wave is still unsettled.

## Append-only status and remaining unknown

`LOG.md:1384-1403` already appends the r21 correction: it supersedes the r20 C1 improvement and unqualified classification acceptance, records the rejected-harmed freshness/calibration ruling, preserves historical records, and says the r20 pin is invalid for acceptance. That is the appropriate append-only correction; the r20 paragraph should remain as historical record. No LOG/source edit, census, or pin was performed.

**Confidence:** high that the r20 acceptance reading needs correction and that the r21 LOG entry supplies it. **Unresolved:** independent per-wave disposition is absent in the examined provenance; actual lifecycle state for both identities remains unknown.