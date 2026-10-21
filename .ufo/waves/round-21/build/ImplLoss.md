# Round 21 ImplLoss report

## Files changed

- Candidate: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/round21/ImplLoss/tools/mori-evidence-loss.py`
- This report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-21/build/ImplLoss.md`

No production files, fleet data, or sibling paths were modified. No tools were installed or updated.

## Implementation

- Added stdlib CLI subcommands `audit --root --required --accounting`, `classify --rule --cases`, and standalone `--selftest` (candidate lines 936–1217; audit lines 477–638; classifier lines 681–719).
- Input JSON rejects duplicate object keys; schema objects are closed; duplicate observation/case IDs fail with setup rc 2. Booleans are checked with exact `bool` types, not integer compatibility (candidate lines 60–74, 335–384, 641–678).
- Audit references require relative safe paths, full commit IDs, and SHA-256 values. File access rejects symlink components; current bytes are hashed and bound to the named commit tree/blob before a reference is accepted (candidate lines 77–179, 182–226, 230–333, 387–454). Required and accounting baseline provenance must be identical by path, revision, and digest (candidate lines 531–539).
- Audit reports numeric `omitted`, `retained`, `unresolved`, `disposed`, and `invalid` counts, with corresponding `*_ids` records, stable issue `finding_id`s, and `pin_allowed` (candidate lines 511–636). Valid unresolved observations remain blockers but are not misreported as invalid.
- A disposed declaration is structurally checked against a hash- and commit-verified JSON receipt containing the matching observation id, actor, wave id, disposition, and `independent: true`. It is reported as `structural_only` with `trust_basis: declared-record-not-authenticated`; it remains unresolved with `external_review_required` and cannot enable pin. No external acceptance/authentication interface was supplied, so the tool does not claim accepted closure or lifecycle completion (candidate lines 455–474, 546–601).
- Classification implements both frozen rule modes and emits the per-case decision, mismatches, and stable IDs. Output explicitly identifies the result as a caller-declared synthetic policy comparison, not pin authorization or lifecycle acceptance (candidate lines 641–719).
- `--selftest` creates a temporary isolated Git fixture and checks exact return codes and literal stable finding IDs for unresolved/empty accounting, absent/tampered/stale evidence, duplicate IDs, unsafe traversal/symlink, unknown state, baseline mismatch, both rules, strict booleans, and structural-but-unaccepted disposition records (candidate lines 725–1166). It was not run.

## Contract evidence

- The requested CLI schemas, blocking rules, exit codes, and selftest cases are specified in `.ufo/waves/round-21/contract.md:13-16`.
- The frozen classifier cases are in `.ufo/waves/round-21/contract.md:18-25`; frozen before/after rule objects and cases were read from `.ufo/waves/round-21/frozen/before-rule.json:1-6`, `.ufo/waves/round-21/frozen/after-rule.json:1-4`, and `.ufo/waves/round-21/frozen/cases.json:1-53`.
- The baseline-identity equality and external-review-only trust limits are co-evolved safety refinements from L1, not additional frozen acceptance claims.

## Verification, risks, blockers

- No build, lint, test, formatter, or CLI run was performed, per the wave instruction; L1 owns post-integration verification.
- No LSP route was available in this tool session. This is a new standalone CLI file; no existing symbol refactor was needed.
- Outside review/author authentication has no supplied input schema or authority. Consequently structurally valid disposed records remain unresolved and `pin_allowed` stays false; clearing that blocker requires an independently supplied acceptance mechanism outside this assignment. The classifier's independent-disposition booleans are synthetic case inputs only.
