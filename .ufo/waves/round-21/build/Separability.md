# Separability review — C1 accounting vs C2 classification

## Finding

**No actionable separability defect found in the contract and proposed probes reviewed.** C1 and C2 are distinct observables, not two counts of one outcome:

- `contract.md:14` defines `audit --required ... --accounting ...` and its `omitted`, `retained`, `unresolved`, `disposed`, and `pin_allowed` result; `contract.md:15` separately defines `classify --rule ... --cases ...` and the case-mismatch count. C1 uses retained historical observations and provenance; C2 compares decisions made from an old/new rule object against frozen expectations.
- The C1 probe report (`build/MutLostIdentity.md:27-35`) proposes removing only `aggregator-r10-resume` from an isolated accounting copy. Its expected signature is omitted `0→1`, retained `2→1`, unresolved `2→1`, disposed `0`, and `pin_allowed=false` throughout; the expected audit rc remains 1. It does not claim a disposition or settlement.
- The C2 frozen cases (`frozen/cases.json:5-19`) include `loss-unknown` and `loss-cleanup-only`: both have required evidence lost and no independent disposition, while `ordinary_state_change` differs. The C2 probe report (`build/MutOldPermission.md:45`) expects only these two cases to mismatch when the rule is changed to the old permissive value, then return to zero mismatches after restoration. Its other cases are negative controls.

### Concrete counterexample

Keep the active rule unchanged and remove the `aggregator-r10-resume` row from the private accounting copy: C1 observes one omitted identity and one fewer unresolved row, while the pin remains blocked; C2's rule/cases and mismatch count are untouched. Conversely, keep the complete accounting unchanged and set the isolated rule's `evidence_loss_blocks` to false: C2 should misclassify the two frozen lost-evidence cases despite their different ordinary-state values, while C1's accounting counts are untouched. These are independently observable changes, so adding the C1 omission delta to the C2 mismatch count would double-count unlike quantities.

### Smallest safe change

No contract/interface change is indicated. Preserve the two separate command/result paths and their isolated mutations. When the implementation is available, assert the C1 accounting signature (including persistent `pin_allowed=false`) and the C2 decision/mismatch signature independently; do not aggregate either count into the other or infer C2 success from an audit blocker.

## Residual risk and verification gaps

- The designated implementation path `tools/mori-evidence-loss.py` was not present when read, so implementation behavior and actual changed-code diff could not be reviewed. The two lane reports explicitly describe their probes as proposed/unexecuted; their expected signatures are not measured results.
- The `lsp` device is unavailable in this environment (`read xd://lsp` returned “No such tool”); no semantic caller/definition/diagnostics checks were possible. No grep fallback was used.
- No tests or runtime probes were run. This is a recommendation about separation based on the round-21 contract, frozen fixtures, and the proposed probe specifications—not an implementation verdict.