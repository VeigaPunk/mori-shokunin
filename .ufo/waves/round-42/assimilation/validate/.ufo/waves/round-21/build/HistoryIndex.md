# History-index scout — round-21 pin acceptance

## Finding

**Coverage-map item requiring acceptance supersession:** the round-20 row `Drift baseline re-pin` in `corpus/README.md:397-402`, specifically its bounded advance (“closed-class classification of all 50 r10 drift tokens … and a new baseline”). Read as current acceptance, that row could endorse the re-pin. It must be interpreted only as a historical account of the round-20 work, not as approval of `baseline-r20-20261021T1051Z.json`.

The append-only correction already present in `corpus/README.md:404-414` makes that distinction explicit: lines 406-409 say the row is historical, not an acceptance endorsement, and that the r20 baseline is unchanged but invalid for acceptance; lines 410-414 retain the two unresolved observations and preserve the FR3 settlement boundary. Thus the correction supersedes the acceptance implication without deleting or rewriting the coverage row.

## Observed evidence

- `corpus/knowledge/drift-repin-r20.md:54-78` preserves the historical pin and comparison observations (`MORI_PIN: ok`, then `MORI_DRIFT: none`); these document what happened and what the comparison reported, not current admissibility.
- Its appended erratum at `corpus/knowledge/drift-repin-r20.md:80-97` expressly supersedes acceptance readings of sections 2-5, keeps baseline/register bytes, labels the baseline invalid for acceptance, and says the post-pin `none` is only a historical comparison. It reports no round-21 census, pin, or drift run.
- `corpus/evidence/loss-accounting-r21.json:5-44` retains both `aggregator-r10` and `aggregator-r10-resume` with `state: unresolved`, baseline/deletion/cleanup references, and `independent_disposition: null`.
- `.ufo/waves/round-21/evidence/historical-provenance.json:19-40` identifies the removal and cleanup evidence and records `independent_wave_disposition: null`, `settlement: unknown`; the note says same-identity preservation proves cleanup, not settlement.
- The separate r10 coverage-map entry at `corpus/README.md:18` records the original r10 pin as an adopted baseline. It is historical background, distinct from the round-20 re-pin claim; do not remove it or conflate its original adoption with the later r20 acceptance ruling.

## Assessment and limits

**Inference (high confidence, limited to the coverage map):** the intended supersession is the r20 row’s possible present-tense acceptance implication, not its factual historical entry. The README’s appended Round21 correction already supplies that supersession while retaining historical observations and artifacts. Do not infer either wave settled, independently disposed, or dead; both dispositions remain unknown. No live census, pin, drift run, or source edit was performed.

The LSP device is not present in this seat’s mounted tool inventory; these are direct document observations with literal path/line citations, not semantic reference results. This scout did not assess whether every external baseline-acceptance consumer enforces the erratum.