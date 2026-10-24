# AuditDuplicate — duplicate required/accounting identities

## Axes

- **Identity integrity:** repeated `id` values cannot collapse distinct input rows.
- **Failure honesty:** malformed duplicate inputs fail as setup errors before audit accounting.
- **Scope:** only the round-21 duplicate-ID requirement was reviewed.

## Findings

No actionable duplicate-ID overwrite defect is established in the available candidate evaluator.

The contract requires `observations` arrays for required and accounting inputs (`.ufo/waves/round-21/contract.md:14`). In the candidate `.scratch/round21/ImplLoss/tools/mori-evidence-loss.py`, `_load_required` rejects a repeated `id` with `SetupError("duplicate_observation_id")` before adding the row to `seen`/`rows` (`:344-363`); `_load_accounting` does the same (`:366-383`). `audit()` only constructs `required_by_id` and `accounting_by_id` from those validated lists afterward (`:477-492`), so its dictionary comprehensions cannot silently overwrite a duplicate accepted by these loaders. `main()` serializes `SetupError` and returns rc 2 (`:978-980`). The candidate selftest contains separate duplicate-accounting and duplicate-required cases expecting that error/rc (`:838-841`, `:867-872`); these are source assertions, not observed test results.

**Concrete counterexamples:**

- Required input with two rows both carrying `id: "aggregator-r10"` must stop in `_load_required` on the second row with `duplicate_observation_id`, rather than letting the later baseline/evidence replace the first.
- Accounting input with two rows both carrying `id: "aggregator-r10"` must stop in `_load_accounting` on the second row, rather than letting the later state/provenance replace the first.

These are statically traced expected outcomes; I did not execute the CLI. **Smallest safe change:** none indicated in the current candidate. Preserve both pre-dictionary duplicate guards and their rc-2 behavior; no broader redesign is warranted.

## Diff and verification limits

The candidate file is present as an untracked file in `.scratch/round21/ImplLoss` (`git status --short --untracked-files=all` reported `?? tools/mori-evidence-loss.py`); that clone's HEAD is the contract's entering revision `e9f340ce986f82a60baad1b8e5ead655ab818a1c`, and the tracked `git diff` against it was empty. Thus this review could inspect the candidate snapshot but could not establish a committed implementation diff. The mounted-tool check `read xd://lsp` returned “No such tool”; no LSP status/references/definition/diagnostics were available. I used no grep as semantic proof. No tests, builds, linters, formatters, or production writes were performed.