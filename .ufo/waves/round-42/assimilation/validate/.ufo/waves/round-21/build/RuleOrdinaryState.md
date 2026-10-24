# RuleOrdinaryState review

## Scope and evidence

- Contract requires classification under the new rule to be `census-regression,false` only when evidence is lost and there is no independent disposition; otherwise it is `live-state,true` (`.ufo/waves/round-21/contract.md:15`). The frozen cases explicitly require `ordinary-state` (`required_evidence_lost:false`, `independent_disposition:false`, `ordinary_state_change:false`) to remain `live-state,true` (`.ufo/waves/round-21/frozen/cases.json:45-50`).
- The assigned clone contains `tools/mori-evidence-loss.py`, reported by `git status --short` as untracked (`?? tools/mori-evidence-loss.py`); `git diff` does not include untracked contents. Its classifier at `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/round21/ImplLoss/tools/mori-evidence-loss.py:681-687` checks only `evidence_loss_blocks && required_evidence_lost && !independent_disposition` and otherwise returns `live-state,true`. It does not use `ordinary_state_change` in the decision.
- No LSP device is mounted in this session (`xd://lsp` returned “No such tool”); semantic references/definition/diagnostics were unavailable. No tests were run.

## Concrete counterexample and minimal safe rule

Counterexample input is the frozen `ordinary-state` case: `false,false,false`. A classifier that treats `ordinary_state_change == false` (or absence of an ordinary change) as sufficient for regression would return `census-regression,false`, contradicting the frozen expectation `live-state,true` at `cases.json:45-50`.

The smallest safe handling is the predicate already present at `tools/mori-evidence-loss.py:682-687`: keep `ordinary_state_change` out of class selection, and use only `evidence_loss_blocks && required_evidence_lost && !independent_disposition` for `census-regression,false`; all other cases stay `live-state,true`. For the frozen `ordinary-state` input, that branch returns the required `live-state,true`; no code change is indicated for this requirement.

## Findings by severity

- **No confirmed code finding.** The ordinary-state case is satisfied by the inspected classifier branch. This is source review only; no runtime result was collected.

## Residual risk and verification gaps

- The implementation now exists in the assigned clone, and its visible classification branch meets this case. Runtime behavior remains unverified because no tests or executions were performed.
- LSP-based checks were unavailable; no tests or production writes were performed.
