# F2 — `register_sha256`

## Finding — Moderate, regression-harness coverage gap

`tools/mori-round19-regressions.py:657-659,707-712` validates the digest only in the bound receipt. The legacy receipt is parsed at `:648-650`, but no `register_sha256` assertion reads its provenance. The legacy checks at `:668-671,719-721` cover script digest and unbound status/revision, not register digest. Thus a regression that removes or corrupts only the no-`--rev` receipt's register digest, while preserving the bound receipt, passes the register-digest checks and is not rejected by the legacy checks. The contract describes the legacy invocation as unbound and lists the digest among its provenance metadata without limiting it to bound mode.

This is a harness gap, not a current CLI defect: `tools/mori-freeze-order.py:375-380,396-404` obtains the register digest for either invocation and emits it in the shared provenance object. The bound-path expectation is independently derived from synthetic fixture bytes (`mori-round19-regressions.py:522-547`) and compared to the bound receipt. A wrong bound digest is a regression; a missing bound digest is classified as capability-absent (`:657-659,711-712`), and after-mode rejects any capability absence (`:1105-1107`).

## Residual risk

The frozen `register_sha256` assertion does not falsify loss or corruption of that field on legacy invocations; the integrated CLI currently emits the field there.

## Verification gaps

No tests, smokes, or verifiers were run, as required. LSP status/references/definition/diagnostics were unavailable: `read xd://lsp` returned “No such tool”; only `ast_edit` and `debug` devices were mounted. Review used source reads and a read-only diff only.
