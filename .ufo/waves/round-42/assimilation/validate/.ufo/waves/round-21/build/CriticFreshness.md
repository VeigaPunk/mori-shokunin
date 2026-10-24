# Freshness critic — acceptance blockers

## Verdict

**C1 is a real but bounded repair:** retaining `aggregator-r10` and `aggregator-r10-resume` as unresolved observations fixes their omission from the retained loss register; it does not establish settlement or by itself revoke the already-persisted r20 baseline. **Do not accept freshness until r20 is explicitly invalidated for baseline acceptance, while preserved byte-for-byte as historical evidence.** Later comparisons must remain runnable as diagnostics and must not restore acceptance or settle either row.

## Blocker 1 — the extant r20 pin has no specified invalidation path

- The round21 contract says “No new pin” and that r10/r20 baseline bytes remain unchanged (`.ufo/waves/round-21/contract.md:3`). It requires operationally blocking baseline acceptance while disposition is unknown (`:7`), but its interface defines only `audit --required/--accounting` and `classify --rule/--cases`; the audit reports `pin_allowed` and has no existing-pin identity, invalidation record, or consumer gate (`:13-16`). The `pin_allowed:false` rule is therefore not evidence that a previously pinned path has ceased to be acceptable.
- The old artifact is present at `corpus/evidence/baseline-r20-20261021T1051Z.json:1-3`; it has a `pinned_ts`. The r20 timeline records `MORI_PIN: ok` for that exact path (`.ufo/waves/round-20/evidence/c1-repin-timeline.txt:7-10`), and the recorded post-pin comparison is `MORI_DRIFT: none`, rc 0 (`.ufo/waves/round-20/evidence/c1-drift-r20-postpin.txt:1-2`).
- This is not a hypothetical identity loss: the r10 baseline has distinct `WAVE_UNSETTLED_AGE` rows for both aggregator IDs (`corpus/evidence/baseline-r10-20261015T2231Z.json:26-27`). R20 classified the aggregate `-FINDING:WAVE_UNSETTLED_AGE` as `live-state` while explicitly noting those IDs were emptied, and its `blind_spot` says cleanup is not settlement evidence (`corpus/evidence/drift-classification-r20.json:210-214`). R21's own provenance leaves independent disposition `null` and settlement `unknown` (`.ufo/waves/round-21/evidence/historical-provenance.json:38-40`).

**Strongest counterexample:** an unresolved audit can correctly return `pin_allowed:false` while the r20 file still exists with a successful pin receipt and a successful `none` comparison. Without an invalidation state consulted by baseline-acceptance consumers, a consumer can continue treating that file as accepted. I did not establish that a particular consumer currently does so; the contract does not specify the exclusion needed to rule it out.

## Blocker 2 — comparison results must not become disposition or admission

The contract requires the same evaluator to count committed before/after snapshots and defines a complete unresolved audit as expected rc 1 (`.ufo/waves/round-21/contract.md:7,14`). It does not define a separate nonblocking comparison outcome or say how the comparison consumes the expected rc1 result. Nor may an equality/clean result be read as settlement: r20's `none` result coexists with the recorded unknown disposition above. As written, a later comparison could be confused with pin status, or an expected unresolved rc1 could suppress the requested comparison/report.

## Smallest safe correction

1. Keep both r20 baseline bytes unchanged, but append a committed, hash/revision-bound invalidation/withdrawal record naming `corpus/evidence/baseline-r20-20261021T1051Z.json` and the unresolved wave IDs. Require every baseline-acceptance path to consult that status; unknown dispositions mean the old file is historical-only and **not admissible as an accepted baseline**. Do not delete or rewrite it.
2. Keep before/after and later comparisons as a distinct diagnostic path: expose their counts/results even when the audit's expected rc is 1; permit comparisons against the retained historical r20 bytes, but do not let comparison rc/result change invalidation, `pin_allowed`, or either row's unresolved status. Only the independently evidenced per-wave disposition required by the contract can resolve a row.

## Impacted axes

- **C1 freshness:** primary blocker—retention improves observability, but freshness acceptance is not repaired while an old accepted pin can survive unresolved loss.
- **C2 calibration:** operational-rule blocker—an evidence-loss-first decision that blocks only a future pin does not supersede the old cause-only acceptance outcome for the existing r20 pin.
