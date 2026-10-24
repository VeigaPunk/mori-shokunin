# RuleLossUnknown review

## Finding

**Medium — the old-rule probe does not consume the committed Q67 before-rule object.** This is a verification gap, not an observed defect in the classifier branch.

Concrete frozen counterexample: `.ufo/waves/round-21/frozen/cases.json:5-10` defines `loss-unknown` as `required_evidence_lost=true`, `independent_disposition=false`, `ordinary_state_change=true`, with expected `census-regression,false`. The explicit historical model at `.ufo/waves/round-21/frozen/before-rule.json:2-5` has `evidence_loss_blocks=false` and cites Q67. Under the candidate classifier, that false gate takes the `live-state,true` branch (`.scratch/round21/ImplLoss/tools/mori-evidence-loss.py:677-694`), so this frozen case must mismatch; the contract specifies mismatch exit code 1 (`.ufo/waves/round-21/contract.md:15-18`). With the after-rule's true gate, the same input takes the `census-regression,false` branch (`mori-evidence-loss.py:683-685`). This is source-derived, not a runtime observation.

The proposed probe instead builds `PRISTINE` from a new-rule object and flips only its boolean to form `MUTANT` (`.ufo/waves/round-21/build/MutOldPermission/probe_old_permission.py:49-67`). Its detector runs those generated files, not `frozen/before-rule.json` (`probe_old_permission.py:114-145`). It reduces each result to `(returncode, mismatched)` and checks aggregate signatures (`probe_old_permission.py:139-145,208-221`); it does not assert the returned decision for the named `loss-unknown` row. Although the generated false rule is equivalent for the candidate classifier's current decision branch, it does not demonstrate that the evaluator reads the committed old rule object as required by the contract.

**Smallest safe change:** in the isolated probe, add one classifier invocation using the exact `frozen/before-rule.json` and frozen cases, then assert its `loss-unknown` decision has observed `live-state,true`, expected `census-regression,false`, and `matched=false` (and `rc=1`). Keep the after-rule/frozen-case invocation as the matching control. This directly checks the old/new objects and independent frozen expectation without changing the frozen policy or classifier design.

## Residual risk and verification gaps

- The candidate classifier's branch is consistent with the frozen `loss-unknown` expectation by source inspection; no runtime result was collected, per assignment.
- No `lsp` device is mounted (`write xd://lsp` returned “No such tool”), so status/references/definition/diagnostics were unavailable. No text-grep result is offered as semantic proof.
- No tests were run, no tools were installed, and no production files were written.
