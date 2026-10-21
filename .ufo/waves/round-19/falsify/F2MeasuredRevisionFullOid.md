# F2 — `measured_revision_full_oid`

## Findings

- **Medium — validation coverage / legacy-binding false acceptance.** `tools/mori-round19-regressions.py:559-579,629-647`; runtime contract at `tools/mori-freeze-order.py:397-404`. The harness invokes its legacy case without `--rev`, but the after-mode `measured_revision_full_oid` assertion reads only the bound invocation's provenance. The legacy result is checked for verdicts and private-marker leakage, not for unbound status or absent measured revision. A legacy result that incorrectly claims to be bound while retaining the same claim verdicts would therefore leave this assertion and the other C2 checks green. This misses the contract's explicit legacy/unbound distinction. The current runtime itself sets the revision to `None` when `--rev` is omitted and emits the corresponding unbound status (`mori-freeze-order.py:364-399`); the defect is in the regression oracle's coverage.

- **Low — supported SHA-256 full OID rejected by the oracle.** `tools/mori-round19-regressions.py:54-55,443-446,643-646`; runtime OID validation at `tools/mori-freeze-order.py:61-74`. The harness's OID pattern accepts only 40 lowercase hexadecimal characters, while the runtime accepts either 40- or 64-character full commit OIDs. Its synthetic repository is initialized without selecting the SHA-256 object format, so this case is not exercised. With a SHA-256-format fixture, the correct 64-character `measured` value would still fail the harness's regex despite matching the independently generated expected revision.

## Bound-field disposition and residual risk

For the bound invocation, the check compares the emitted revision with the independently generated fixture revision and requires a full-hex match (`mori-round19-regressions.py:642-647`). A wrong value is classified as a regression; a missing field is classified as capability absent, and after-mode rejects either regression or absent capability (`mori-round19-regressions.py:615-619,1087-1096`). No bound-value false acceptance was found in this assertion. The current runtime resolves and emits the revision through `_resolve_commit` and the provenance construction (`mori-freeze-order.py:61-74,362-405`).

## Verification gaps

Static source inspection only; no tests, smokes, or other verification were run. The LSP device is unavailable (`read xd://lsp` returned “No such tool”; mounted devices were `ast_edit` and `debug`), so no semantic LSP references, definitions, or diagnostics were available; source inspection was the fallback.