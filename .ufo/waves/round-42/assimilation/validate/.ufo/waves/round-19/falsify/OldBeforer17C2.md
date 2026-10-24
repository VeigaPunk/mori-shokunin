# r17-C2 before-state falsification

## Finding

No actionable defect in the assigned row. Expected before-state: verdict `co-evolved`, effective label `unlabeled`, overclaim `false`. The retained before-state records these values for `r17-C2` (`.ufo/waves/round-18/evidence/c2-before.json:1`). The frozen register declares `r17-C2` as `unlabeled` (`.ufo/waves/round-18/frozen/c2-register.json:20-23`); the corrections register has no correction for this ID and its appended correction is for `r17-C3` (`corpus/evidence/freeze-register.json:4-13`). The checker selects a correction only when present, otherwise the declared label, and counts an overclaim only for effective label `pre-build` with a non-`pre-build` verdict (`tools/mori-freeze-order.py:315-329`). Thus this row stays `unlabeled` and does not contribute an overclaim; its `co-evolved` verdict also agrees with the frozen outside ruling.

## Historical/prospective attribution

Preserved: the contract distinguishes one historical-overclaim correction from three prospective labels, rather than treating all four before-state overclaims as historical defects (`.ufo/waves/round-19/contract.md:7`). The retained before-state marks `r17-C2` as not overclaimed; the appended correction targets the separate `r17-C3` row. This row therefore does not inflate the historical count. Applying that correction removes the one historical overclaim while leaving the three prospective pre-build labels distinct. This is a static derivation, not an execution result.

## Residual risk and verification gaps

Scope is only `r17-C2`; no conclusion is offered on the remaining rows. No checker, test, smoke, or other verification was run. The `lsp` device was unavailable (`read xd://lsp` returned “No such tool”; only `ast_edit` and `debug` were mounted), so references/definition/diagnostics could not be requested; source inspection was the fallback. Read-only commit comparison from the assigned integrated revision to repository `HEAD` found no differences for the checker and the three cited retained C2 artifacts.
