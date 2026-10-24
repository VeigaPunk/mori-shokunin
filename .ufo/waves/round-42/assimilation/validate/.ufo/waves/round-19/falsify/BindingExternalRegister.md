# C2 external-register binding review

## Finding

- **Low — supplemental assertion does not gate safe-output leakage (test/oracle).** `tools/mori-round19-regressions.py:759-768` passes only when the subprocess returns exit 2. It separately records `private_value_leak`, but that boolean is not part of the row status; `counts` counts statuses only (`:928-934`). Thus the after-mode harness can count this assertion as passing even if the actual CLI subprocess emits the fixture marker. The assertion does exercise the CLI and checks the refusal exit code, but does not itself enforce the no-private-values part of safe refusal.

## Grounded runtime match

No external-register binding bypass found. `tools/mori-freeze-order.py:125-151` resolves a provenance-bound input path, rejects paths not beneath the resolved repository root before reading bytes, and verifies the bytes against the measured-revision Git blob. That path raises `input-revision-mismatch`; `tools/mori-freeze-order.py:362-389` emits the safe error result and returns 2, and `:692-707` propagates the CLI return code. The error result contains only the error class and empty claims (`:349-358`).

The supplemental fixture puts the repository at a child path and writes the valid register bytes to a sibling path outside it (`tools/mori-round19-regressions.py:521-543,753-760`). `c2_invocation` supplies the measured `--rev` and outside `--register` path (`:566-578`); `run_tool` calls the actual CLI through `subprocess.run` (`:182-200`). This supplemental check runs in after-mode and contributes to the harness result (`:1042-1045,1058-1059,1083-1092`). The frozen refinement requires exit 2 for an external register and requires provenance-bound inputs beneath `--repo` (`.ufo/waves/round-19/frozen/provenance-refinement.json:5-6,11`).

## Verification gaps

No tests or runtime checks were run, as instructed. The `lsp` device is unavailable (`read xd://lsp` returned “No such tool”); findings use literal source inspection only, not semantic LSP proof.