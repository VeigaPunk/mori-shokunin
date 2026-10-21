# RuleOrdinaryAging — scoped C2 review

## Axes

- **C2 calibration:** evidence loss without independent disposition blocks; ordinary state changes alone remain `live-state`, pin allowed.
- **False-positive control:** an any-change rule must be rejected by the frozen negative control.
- **Evidence boundary:** distinguish isolated candidate source from an integrated, exercised implementation.

## Finding

**No actionable defect in the scoped ordinary-aging rule was found in the inspected candidate source.** The integrated `tools/mori-evidence-loss.py` was absent when checked; the available candidate is untracked in the isolated clone, so this is source review, not an integrated or runtime verdict.

## Concrete counterexample to a universal stop-on-any-change rule

`frozen/cases.json:37-42` supplies `ordinary-aging` with `required_evidence_lost=false`, `independent_disposition=false`, and `ordinary_state_change=true`, while requiring `live-state` and `expected_pin_allowed=true`. An implementation that treats `ordinary_state_change` itself as a stop condition would return `census-regression,false` for this row and fail the frozen expectation. This is the concrete false-positive guard; it is not evidence that such a regression currently runs.

The isolated candidate's `classify()` checks the loaded rule, `required_evidence_lost`, and absence of independent disposition at `.scratch/round21/ImplLoss/tools/mori-evidence-loss.py:681-697`. It does not include `ordinary_state_change` in that decision. The flag is schema/type-checked at `:655-678`. Therefore, by source inspection, the stated `ordinary-aging` input follows the `else` branch and matches `live-state,true`. The self-test fixture contains the same row and checks the after-rule classification at `:879-899`; this test was not run.

The paired guard is `loss-unknown` (`frozen/cases.json:4-11`): it has `ordinary_state_change=true` but required evidence is lost and there is no independent disposition, so it must block. Together these rows distinguish evidence-loss-first behavior from both “any change blocks” and “a change excuses lost evidence.”

## Smallest safe change

No source edit is indicated for the inspected candidate. Preserve the existing predicate at `ImplLoss/tools/mori-evidence-loss.py:687`: block only when the loaded new rule enables evidence-loss blocking, required evidence is lost, and no independent disposition exists. Keep `ordinary-aging` as a frozen expected-output case; do not add `ordinary_state_change` or a generic state-change test to the blocking predicate. Do not modify production while the integrated target is absent.

## Verification gaps and boundaries

- `tools/mori-evidence-loss.py` was not found at the integrated path; `.scratch/round21/ImplLoss/tools/mori-evidence-loss.py` was reported untracked by read-only Git status. No integrated diff or runtime behavior is established.
- No tests, self-tests, build, or production writes were run.
- LSP status was requested first, but `xd://lsp` is not mounted; no semantic references/definition/diagnostics checks were available. This report relies on the directly read contract, frozen case, and candidate source, not grep as semantic proof.
- No tools were installed or updated.
