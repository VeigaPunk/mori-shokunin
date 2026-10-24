# AuditEmpty — empty accounting boundary

## Axes

- **Omission accounting:** every required identity absent from accounting remains counted as omitted.
- **Lifecycle honesty:** cleanup or missing implementation capability must not be mistaken for independent disposition or settlement.
- **Pin safety:** incomplete/unknown evidence blocks baseline acceptance.

## Finding

**No implementation defect is established yet; the evaluator is not present to execute.** The concrete pre-implementation counterexample is the contract's own frozen input pair:

- `.ufo/waves/round-21/frozen/required.json:5-20` requires `aggregator-r10` and `aggregator-r10-resume`.
- `.ufo/waves/round-21/frozen/before-accounting.json:2-4` is schema-valid `mori-loss-accounting-v1` with `observations: []`.
- `.ufo/waves/round-21/contract.md:7,14` requires omissions to be counted, and specifies rc1 for an omission/blocker versus rc2 for setup/input failure; unresolved evidence blocks pin.

Therefore this input must report **omitted=2, retained=0, unresolved=0, disposed=0, invalid=0, pin_allowed=false**, with the expected-blocker rc1. Treating an empty but valid accounting list as malformed/setup failure (rc2), as zero omissions/success, or as evidence that no historical gaps existed would erase the observed loss. The minimal safe behavior is to compute `required_ids - accounting_ids` even when the accounting list is empty; reserve rc2 for malformed/unreadable inputs or other setup failures.

Keep capability status separate from accounting status: the evaluator is absent from entering revision `e9f340ce986f82a60baad1b8e5ead655ab818a1c` (`git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e e9f340ce986f82a60baad1b8e5ead655ab818a1c:tools/mori-evidence-loss.py` returned 128, “path … does not exist”). At review time, both the integrated tool path and `.scratch/round21/ImplLoss/tools/mori-evidence-loss.py` were also absent; the implementation owner reported that implementation was still in progress. This is **capability absent**, not an audit observation and not evidence that the two required historical observations were absent from the baseline itself.

The intended after-state is independently represented in `corpus/evidence/loss-accounting-r21.json:5-45`: two rows, both `unresolved`, both with `independent_disposition: null`. `.ufo/waves/round-21/evidence/historical-provenance.json:38-40` explicitly says settlement is unknown and same-identity cleanup is not settlement. Do not let the empty before-state manufacture a disposition or let same-identity cleanup permit pinning.

## Residual risk

No runnable changed evaluator exists yet, so the expected counters and return code above are derived from the frozen contract/input, **not observed runtime output**. Review the same empty-accounting case against the eventual integrated evaluator before treating C1 as implemented.

## Verification gaps

- No tests or production writes were run/performed.
- LSP is unavailable in this environment (`read xd://lsp` reported no such tool); no source implementation/callers were available for semantic references/definition/diagnostics.
- No evaluator execution occurred, and the historical absence of the evaluator means no before-runtime result can be claimed.
