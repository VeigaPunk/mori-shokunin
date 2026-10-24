# r18-C2 after-state review

## Findings

No actionable finding for this row. The retained after-state records `r18-C2` as verdict `pre-build`, effective label `pre-build`, and overclaim `false` (`.ufo/waves/round-18/evidence/c2-after.json:1`). The frozen row declares `pre-build` and has no outside ruling (`.ufo/waves/round-18/frozen/c2-register.json:34-37`). The append-only corrections register corrects only `r17-C3`, so it does not replace `r18-C2`'s declared label (`corpus/evidence/freeze-register.json:4-12`). The delivered checker selects a correction when present, otherwise the declared label, and marks a pre-build label as overclaimed only when the verdict differs from pre-build (`tools/mori-freeze-order.py:310-326`). Its row result is consistent with the retained after-state.

Attribution is preserved: this is one of the three prospective r18 labels, not the single historical correction. The frozen refinement states one historical correction and three prospective labels, and identifies the historical relabel as r17-C3 (`.ufo/waves/round-19/frozen/provenance-refinement.json:8-12`).

## Residual risk and verification gaps

Static review only, as required; no checker, tests, or other runtime was executed. LSP was unavailable (`xd://lsp` returned “No such tool”; only `ast_edit` and `debug` devices were mounted), so no references/definition/diagnostics checks were possible. No grep-based semantic claim is made.