# F2Check21 — C2 invalid-revision assertion

Axes reviewed: assertion fidelity, invalid-input error classification, and bound-versus-legacy separation.

## Finding

- **P3 — Misclassified invalid-input failure** — `tools/mori-round19-regressions.py:720-727` (classification). In `after` mode, a missing/unparseable response for the invalid-`--rev` invocation sets `unavailable=True`, so `set_result` reports `capability_absent` rather than `regression` (`:613-617`). Counterexample: the tool produces a valid bound receipt, but its invalid-revision path exits without valid JSON; `parsed_stdout` is then `None` and this assertion is classified as absent capability. The passed `invalid_failure` is not used by this predicate. This does not permit a clean acceptance: `after` mode fails when any capability is absent (`:1090-1099`), but the receipt misstates the failure class.

## Assertion trace and residual risk

- The expected file names this check at `.ufo/waves/round-19/frozen/expected.json:34`; the harness pins/validates that oracle and the C2 name order (`tools/mori-round19-regressions.py:807-866`, `:40-52`). Its independent predicate checks the CLI exit code, the top-level `error` field, and an empty `claims` list (`:720-725`).
- The harness supplies the invalid revision through `--rev` on a bound invocation (`:557-577`, `:1019-1029`). The implementation resolves `args.rev` before loading inputs, emits its preflight error result and exits 2 if unresolved (`tools/mori-freeze-order.py:349-369`). This matches the contract's unknown-`--rev` requirement. The preflight result has no `provenance`; that is not contradicted by the contract, which requires exit 2 for unknown `--rev`.
- Legacy behavior is distinct: the legacy invocation omits `--rev` (`:557-577`), and the existing `same_verdicts_as_base` predicate checks legacy `status=unbound` / null measured revision against bound status (`:640-643`, `:705-715`). The invalid-revision assertion is not accidentally using the legacy path.

## Verification gaps

No tests, builds, or runtime checks were run, as required. The `lsp` device is unavailable in this environment (`xd://lsp` is not mounted), so no LSP status/references/definition/diagnostics were available; source review used the requested file ranges and targeted text search only.