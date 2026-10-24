# F2ScriptSha256 — static review

## Findings

### Medium — C2 accepts incorrect script metadata on the legacy invocation

- `tools/mori-round19-regressions.py:659-661` compares the independently computed tool digest only with `bound.provenance.script_sha256`. `run_harness` invokes both legacy and bound modes (`:1016-1044`), but the legacy result is used only for verdict comparison and private-marker scanning (`:703-714`); its script digest is not checked. Therefore a tool that reports the correct digest with `--rev` but a missing or incorrect digest without `--rev` satisfies the `script_sha256` assertion. The check also never asserts the legacy/bound distinction in the CLI's `provenance.status` field.
- The current CLI does emit a digest for both paths and labels them from whether a measured revision exists (`tools/mori-freeze-order.py:384-405`). The contract requires a script digest and says the legacy invocation is explicitly unbound. The frozen oracle lists only the single `script_sha256` check (`.ufo/waves/round-19/frozen/expected.json:22-35`), so the harness currently does not cover that legacy metadata contract. This is a checker acceptance gap, not evidence that the current CLI emits bad metadata.

## Checks that do not falsify the bound-path assertion

- The expected digest is independent of the CLI field: `tool_path` resolves and hashes the supplied regular file (`tools/mori-round19-regressions.py:882-901`); the harness passes that resolved file to the CLI and compares the hash with its bound output (`:659-661`, `:1016-1044`). The CLI separately hashes its own resolved source path (`tools/mori-freeze-order.py:384-386`). The harness also checks that the supplied tool file remains unchanged across the run (`tools/mori-round19-regressions.py:1069-1083`).
- A wrong bound digest is classified as a regression; a missing bound field is classified as capability-absent (`tools/mori-round19-regressions.py:615-619`, `:659-661`). In `after` mode either prevents a passing result (`:1087-1096`).

## Residual risk and verification gaps

- The `lsp` device is unavailable in this environment: `read xd://lsp` returned “No such tool.” Used lexical search and static source reads only; no LSP semantic checks were possible.
- No tests, builds, linters, or smoke runs were executed, as required. Findings are static only.