# TrendClaims seat — outside-sample proposal provenance

`real-cases-outside-proposal.json` is a reviewer-authored PROPOSAL (not frozen bytes, not
production). Its two rows take expected values from outside adjudication, authored by the
non-author round-20 closure, not by any round-21 claim author:

- `real-aggregator-r10-loss` — expected `census-regression`, pin blocked.
  Basis: fleet `MANIFEST.json` `/rounds/405/verification/C1_class_ruling` (`admitted=false`,
  `rejected-harmed`); `.ufo/waves/round-20/falsify/AdjudicateWaves.md:5` ("the safe class is
  `census-regression` (unresolved loss of observability)") and `:29` ("block this re-pin as
  `census-regression` until a non-author record accounts for each removed wave").
  Real-event binding: `corpus/evidence/baseline-r10-20261015T2231Z.json:26-27` (warning rows
  for both identities), removal `e20f4fa` (removal-metadata.txt), `independent_disposition`
  still null in `corpus/evidence/loss-accounting-r21.json`.
- `real-w24-aging` — expected `live-state`, pin allowed.
  Basis: `.ufo/waves/round-20/falsify/AdjudicateWaves.md:7` ("the newly aged
  `shokunin-train-20261016-w24` is live-state") and `:29` ("classify the newly aged w24
  observation separately as `live-state`").

Observed demonstrations (2026-10-21, read-only, stdout only, scratch tool
`.scratch/round21/ImplLoss/tools/mori-evidence-loss.py`):

- before-rule (`frozen/before-rule.json`, Q67 model): `real-aggregator-r10-loss` observed
  `live-state`/pin-allowed vs expected `census-regression`/blocked → `mismatched=1`, rc 1.
- after-rule (`frozen/after-rule.json`, Q69 model): both rows matched → `mismatched=0`, rc 0.

No frozen file, corpus byte, or production path was modified by this seat. The two
`classify` invocations emitted JSON to stdout only and performed no writes.
