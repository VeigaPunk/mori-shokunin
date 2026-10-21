# F1ProvenanceOnly — static review

## Findings

### Medium — the C1 harness can accept a contradictory clean result

- `.ufo/waves/round-19/frozen/expected.json:10,15-20` requires the `provenance_only` case to exit 1 and report `CONTENT_REVIEW_UNRESOLVED`. The harness creates that case by changing the first synthetic row's basis (`tools/mori-round19-regressions.py:329-356`) and checks the child process return code and required finding (`:392-413`).
- `tools/mori-round19-regressions.py:244-274` accepts `status` as absent or any of the three status labels and never validates the result's `schema` or JSON `exit_code`. Consequently a response with process return code 1 and the required finding, but JSON `status: clean` and `exit_code: 0`, passes `c1_output_valid`; `c1_case_rows` then records `pass` (`:414-417`). The after harness can therefore finish clean despite a contradictory clean claim for this frozen failure case.
- The current content-review path itself maps `provenance-only` to `CONTENT_REVIEW_UNRESOLVED` (`tools/mori-content-review.py:314-330`) and `finish` maps that finding to `failed` / exit 1 (`:191-199`), so this is a harness false-acceptance gap, not evidence that the current CLI mishandles this input. Require the result schema, JSON exit code, and status to agree with the frozen expectation for every case (including failed / 1 here).

### Low — the provenance-only case does not enforce the no-echo output contract

- The fixture changes only the content basis (`tools/mori-round19-regressions.py:354-356`). The sole value-leak check is a search for the private sentinel (`:227-231`, `:398-399`); this case does not inject that sentinel. `c1_output_valid` checks selected receipt fields and finding-row shape, but permits unrecognized top-level and metadata fields (`:244-274`). Thus a child response that adds an echoed review reason or blob content in an extra field can still pass this case.
- The current CLI's result construction does not copy review reasons or blob contents into its result, and its JSON emission serializes only that result (`tools/mori-content-review.py:202-240,272-337,339-341`); no direct leak was found in the statically traced input. To make this case regression-sensitive, validate an allowlisted response shape and assert review reasons/content are not emitted, rather than relying on the sentinel check used for a different case.

## Static trace

The frozen oracle's required exit/finding are consistent with the current CLI: the fixture's valid review row has a matching blob digest and `retain` decision, but `content_basis == "provenance-only"` adds the unresolved finding (`tools/mori-content-review.py:314-330`). The CLI records revision and input digests (`:218-235`), population blob paths and full digests (`:272-283`), counts and path-level findings; `finish` returns failed / 1 (`:176-199`). The result does not include the input reason or blob bytes. The harness resolves the expected data from the pinned oracle and uses it for the case exit and finding (`tools/mori-round19-regressions.py:823-862,392-413`).

## Residual risk and verification gaps

- The `lsp` device is unavailable in this environment: `read xd://lsp` returned “No such tool.” Used static source reads and read-only Git diff/revision inspection only; no LSP semantic checks were possible.
- No tests, builds, linters, or smoke runs were executed, as required. Findings are static only.
