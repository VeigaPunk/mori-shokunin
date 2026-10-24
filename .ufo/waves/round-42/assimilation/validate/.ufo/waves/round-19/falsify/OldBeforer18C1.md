# C2 before-state falsification — r18-C1

Axes: historical-attribution fidelity; single-row rule conformance; evidence/verification limits.

## Finding — Medium: historical baseline conflates a prospective row

For the retained before-state, **r18-C1** is expected to be `no-implementation`, with effective label `pre-build` and `overclaim=true`. The before artifact records that row; the frozen rule defines no implementation touch as `no-implementation` and counts every non-`pre-build` verdict under an effective `pre-build` label as an overclaim. The corrections register contains only an r17-C3 correction, so it does not change r18-C1’s effective label. Evidence: `.ufo/waves/round-18/evidence/c2-before.json:1`; `.ufo/waves/round-18/frozen/c2-register.json:6-13,30-33`; `corpus/evidence/freeze-register.json:4-12`; `tools/mori-freeze-order.py:315-328`.

The distinction is preserved by row identity (r18-C1 is a prospective round-18 claim), but **not by the C2 aggregate**: the retained before artifact reports four overclaims, while the round-18 contract describes the historical before count as one r17-C3 overclaim. This row therefore contributes one prospective overclaim to the same undifferentiated total; the checker does not preserve a history-only `1` separately from the prospective claims. The row’s literal evaluation is consistent with the frozen rule; the discrepancy is the aggregate’s attribution against the contract’s stated historical baseline. I did not independently rederive the other five rows. Evidence: `.ufo/waves/round-18/evidence/c2-before.json:1`; `.ufo/waves/round-18/contract.md:31-36`; `.ufo/waves/round-18/frozen/c2-register.json:13,30-33`.

## Residual risk and verification gaps

This review attacks r18-C1 only; it does not independently adjudicate the other five rows. No checker was executed. The `lsp` device is unavailable (`xd://lsp` reports no such tool; only `ast_edit` and `debug` are mounted), so no LSP status/references/definition/diagnostics queries were possible.