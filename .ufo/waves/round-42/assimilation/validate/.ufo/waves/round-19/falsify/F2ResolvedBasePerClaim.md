# C2 `resolved_base_per_claim` review

## Findings

- **Low — oracle gap** (`tools/mori-round19-regressions.py:488-520, 673-696`; frozen criterion: `.ufo/waves/round-19/frozen/expected.json:27`). Every synthetic claim uses the same `base` value (`mori-round19-regressions.py:490, 495, 501, 506, 512, 517`), while the assertion compares every emitted `base_revision` to the single `fixture["base"]` (`:683-686`). A faulty implementation that resolves only one claim's base and copies it to every output row therefore still satisfies this check. The fixture does not independently establish that each claim's own base was resolved. Use claims with at least two distinct valid bases and expected resolved OIDs keyed by claim ID. The current CLI does resolve `claim["base"]` for each row (`tools/mori-freeze-order.py:267-271`); this is a test-oracle blind spot, not an observed current CLI failure.

## Residual risk

A present but incorrect base value on this fixture is marked `regression` (`mori-round19-regressions.py:683-692`). A missing `base_revision` is marked `capability_absent` (`:691-693`); in `after` mode that still prevents acceptance (`:1105-1107`). The `before` mode intentionally records metadata assertions as `capability_absent` (`:637-644`), so the legacy baseline is not reported as a historical defect. The assertion's ID map also collapses duplicate claim IDs (`:677-682`); the separate `same_verdicts_as_base` check rejects duplicate IDs (`:588-598`).

## Verification gaps

No tests, smoke runs, or verifiers were run, as directed. The LSP device was unavailable (`xd://lsp` is not mounted; status lookup returned no tool topic), so no semantic LSP references/definition/diagnostics were available. Source review used the integrated files; their contents have no diff from the designated integrated commit for these paths.
