# QualityDeferred — round 21 disclosure review

## Finding — Medium: do not credit Q64, Q65, Q66, or Q68 as fixed by C1/C2

**Concrete counterexample.** The round-21 claims are limited to retaining two named historical loss observations and superseding Q67's cause-only classification rule (`.ufo/waves/round-21/contract.md:7-16`). The existing round-20 falsification contains independent counterexamples outside those two claims:

- **Q64:** aggregate W2 evidence labels 22 missing seats “provider failures” without per-seat records (`.ufo/waves/round-20/falsify/ReviewQuality.md:58-73`, especially :61). Correctly recording `aggregator-r10` and `aggregator-r10-resume` as unresolved does not substantiate those other cause labels.
- **Q65:** the counting command scores a register containing `census-regression` on `+SURFACE:lane.audio` as zero mismatches while the strict checker reports a regression; the re-pin clause also has no census-regression gate (`.ufo/waves/round-20/falsify/ReviewQuality.md:41-54`, especially :46-50). A blocker for the two unknown historical observations does not establish that this separate drift-token/pin defect is repaired.
- **Q66:** a marker variant such as `STATUS: started\r\n` is counted as a delivered report (`.ufo/waves/round-20/falsify/ReviewQuality.md:75-82`, especially :78-80). Neither retained-loss accounting nor Q67 classification changes marker parsing.
- **Q68:** the reported falsifier includes a bound artifact changing without a mapping row; the round-20 evidence names bound round-16 `wave1-dispatch.json` and `wave1-spec.json` whose working copies differed from the historical revision (`.ufo/waves/round-20/falsify/ReviewQuality.md:84-92`, especially :87-90). C1/C2 do not establish the mapping or historical-input rule for reruns.

These are counterexamples recorded by the round-20 review, not newly exercised against a round-21 implementation. They show why C1/C2 success cannot be used as evidence that these routed defects were fixed.

**Smallest safe change.** Keep the C1/C2 implementation scoped. In the round-21 claim summary/quality erratum, add an explicit debt disclosure naming Q64, Q65, Q66 and Q68 as *not fixed or re-evaluated by these claims*, with the relevant counterexample pointers above; do not credit these criteria or the broader drift/settlement behavior as improved. This satisfies the contract's explicit disclosure requirement without broadening the repair (`.ufo/waves/round-21/contract.md:27`).

## Residual risk and verification gaps

- This is a pre-implementation, bounded contract review. No round-21 implementation or final claim summary was present in the inspected build listing, so the report identifies the required disclosure and does not claim a current implementation failure.
- The LSP device is unavailable in this environment: `read xd://lsp` returned “No such tool”; no semantic references/definition/diagnostics result is claimed. The source-level evidence above is from direct reads of the cited files; search was used only to locate relevant records.
- No tests, build, lint, census, pin, install, or production write was performed.
