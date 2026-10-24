# Round 21 — AuditNoDiscovery

Axes reviewed: required-population integrity, omission measurement, pin-blocking evidence.

## High — a non-empty subset can hide a required baseline observation

The current oracle rejects an empty or duplicate `required` list, but it does not bind that list to the committed baseline population. It derives its omission denominator from the caller-supplied list itself.

Evidence:
- `frozen/required.json:5-11,14-20` names both `aggregator-r10` and `aggregator-r10-resume`, each pointing to the same baseline revision and SHA-256.
- `corpus/evidence/baseline-r10-20261015T2231Z.json:26-27` contains the two corresponding baseline wave observations. `evidence/historical-provenance.json:3-5` records the baseline revision, path, and digest.
- `.ufo/waves/round-21/oracle-loss.py:35-36` checks only that `required` is non-empty and has unique IDs. At `:58-60`, it computes `expected_omitted` from that same caller-supplied ID set. At `:93-97`, it records input hashes but does not compare the required-set identity or hash to an expected committed baseline population.
- `.ufo/waves/round-21/frozen/before-accounting.json:1-4` is empty, so the full two-ID required fixture correctly counts two omissions today.

Concrete counterexample ([INFERENCE] from the oracle and CLI contract; the new CLI is not present in `tools/` for runtime confirmation): remove the `aggregator-r10-resume` object from the required input, leaving the valid, non-empty `aggregator-r10` object. Use the existing empty before-accounting and an after-accounting containing only `aggregator-r10` as unresolved with valid provenance. The oracle then computes omissions as 1 before and 0 after from its reduced denominator. Its audit checks require rc 1 and `pin_allowed=false` in both phases (`oracle-loss.py:64-71`); those are consistent with one omission before and one unresolved row after. The oracle does not assert that two unresolved rows remain, so this reduced-population run can satisfy its measured checks while omitting the second committed baseline identity. This is a false C1 population/count result, even though pin remains blocked for the one row it sees.

Smallest safe change: derive the target ID set from the authenticated committed baseline at `e9f340ce986f82a60baad1b8e5ead655ab818a1c` / SHA-256 `0993b23505deab2aeb05b2309bdf7dd6eaad2b82f27852491352511aa9670478`; require the non-empty `required` input to match that exact target set and its evidence references; and compute omissions against the baseline-derived set, not the input set. Reject empty, missing, or extra IDs as setup/input failure (`rc=2`) with pin disallowed. The independent oracle should enforce the same population binding and check the expected unresolved count of two after accounting.

## Residual risk and verification gaps

- The contract describes `audit` as returning `rc=0` for complete accounting with zero unresolved, but does not explicitly require a non-empty required population or equality to the committed baseline set. Empty required plus empty accounting is therefore a spec-level vacuity risk ([INFERENCE]); the oracle's non-empty guard does not bind non-empty subsets.
- `tools/mori-evidence-loss.py` was not present in the inspected `tools/` listing, so its runtime behavior is unverified. No tests or runtime checks were run, per scope.
- The `xd://lsp` device is not mounted (`No such tool`); no LSP status/references/definition/diagnostics were available. Findings use direct reads of the cited files only.
