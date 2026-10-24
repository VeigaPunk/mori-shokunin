# RuleIndependentSettlement review

## Findings

### Medium — A valid per-wave disposition never clears the local freshness blocker

The contract requires baseline acceptance to be blocked while disposition is unknown (`.ufo/waves/round-21/contract.md:7`) and permits a valid `disposed` row with a `settlement` or `cleanup-accounted` record (`contract.md:14`). The boundary is explicitly local: an audit disposition concerns Mori's census-baseline acceptance, not lifecycle settlement or global closure (`PROVINCE.md:175-181`).

**Concrete counterexample (static trace of the isolated candidate, not a runtime result):** provide a `state: "disposed"` row with all baseline/deletion/cleanup references valid, a distinct actor, and a hash-verified record whose id, wave id, disposition and independent flag match. After the structural checks pass, the candidate appends the row to `disposed` and also appends `external_review_required` to `unresolved` (`.scratch/round21/ImplLoss/tools/mori-evidence-loss.py:581-596`). The gate requires `unresolved` to be empty, so it returns `pin_allowed: false` and rc 1 (`:612-632`). Thus even an explicit per-wave settlement cannot dispose the local blocker; this adds an always-on prerequisite not present in the contract. The candidate's own positive selftest expects that same valid structural disposition to return rc 0 and `pin_allowed: true` (`:908-920`), contrary to the audit path. This static inconsistency was not executed.

**Smallest safe change:** treat a structurally valid per-wave disposition as resolving the local census-baseline unknown, while preserving `status: "structural_only"` / `trust_basis: "declared-record-not-authenticated"` and making `pin_allowed` explicitly local to Mori's baseline. Do not infer lifecycle settlement, global closure, result acceptance, or reap/re-dispatch permission. If outside adjudication is intended to be a prerequisite even for this local gate, it needs an explicit input/state and corresponding contract/frozen-case change; silently converting every `disposed` row back to unresolved does not implement the current contract.

### Medium — A disposition can name a different wave from the row it disposes

The contract requires an explicit per-wave id (`contract.md:14`); the retained required ids are `aggregator-r10` and `aggregator-r10-resume` (`corpus/evidence/loss-accounting-r21.json:5-6,26-27`). In the candidate, `wave_id` is checked only for valid syntax (`.scratch/round21/ImplLoss/tools/mori-evidence-loss.py:562-565`); `_disposition_record_matches` checks that the record repeats that same supplied value, but never checks it against `observation_id` (`:455-475`, `:578-580`).

**Concrete counterexample (static):** for row `aggregator-r10-resume`, supply matching hash-bound disposition metadata and record with `id: "aggregator-r10-resume"` but `wave_id: "aggregator-r10"`. The record matches the row id and its declared wave id, so the check accepts the pair as a structural disposition for the resume observation even though the explicit wave is the other required observation. The current external-review blocker keeps this candidate from setting `pin_allowed`, but does not correct the misattributed `disposed` row.

**Smallest safe change:** require `wave_id == observation_id` before accepting the record (or use a separately authenticated mapping if the contract intends distinct identifiers). Add the mismatched-wave case to the existing selftest.

## Residual risk and verification gaps

- `independent: true` and a distinct actor string are not authentication. The candidate itself labels its record structural-only and says it is not authenticated; the reviewed files do not provide a trust source that verifies actor identity. Do not report global/lifecycle closure from this evidence. The current committed loss register still has both required observations unresolved with null dispositions (`corpus/evidence/loss-accounting-r21.json:3-45`).
- `tools/mori-evidence-loss.py` is absent from the main tree; the reviewed implementation is the untracked isolated candidate `.scratch/round21/ImplLoss/tools/mori-evidence-loss.py`. Findings concern that candidate and the written contract, not an observed production behavior.
- No `lsp` device/server is mounted (`read xd://lsp` returned the mounted-device inventory without it), so status/references/definition/diagnostics were unavailable. No text grep was used as semantic proof. No tests, builds, or tools were run/installed; no production files were changed.