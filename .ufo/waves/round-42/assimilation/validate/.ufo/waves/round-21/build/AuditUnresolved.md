# AuditUnresolved — complete C1 accounting and closure honesty

## Axes

- **Evidence retention:** preserve both required historical observation identities rather than converting missing evidence into an empty success.
- **Status accuracy:** distinguish an expected unresolved blocker from malformed or invalid accounting.
- **Closure honesty:** never allow an unauthenticated declaration to stand in for independent disposition.

## Findings (severity order)

### High — A declared disposed record can make the candidate report acceptance without external review

The current two-row unresolved accounting remains blocked, but the candidate's disposed path does not satisfy the directly relevant trust refinement. `.ufo/waves/round-21/trust-refinement.md:5,9` requires the actual audit to preserve a submitted disposed declaration as structural status while returning an external-review-required blocker; no authenticated external acceptance mechanism is supplied.

Concrete counterexample: for each required ID, submit `state: "disposed"` with valid baseline/deletion/cleanup references and a committed hash-pinned disposition JSON matching that row's ID, wave ID, actor, allowed disposition, and `independent: true`; set the actor string different from the cleanup actor. The candidate verifies those claimed fields and bytes (`.scratch/round21/ImplLoss/tools/mori-evidence-loss.py:455-474,568-578`), then marks the row disposed when its issue count is zero (`:579-588`). Its `pin_allowed` predicate accepts all-required disposed rows (`:600-607`) despite the explicit `trust_basis: "declared-record-not-authenticated"` (`:617`). There is no external-review check. Thus a caller-authored declaration can produce `pin_allowed=true` / rc 0, contrary to the trust refinement; hash consistency and different actor strings do not authenticate the asserted reviewer.

**Smallest safe change:** keep structurally valid rows visible as declared `disposed`, but do not let that status clear the real acceptance blocker absent externally authenticated review evidence. The lane currently has no such authentication input, so fail closed with an external-review-required finding and `pin_allowed=false` for declared dispositions. Do not count this as proof of settlement.

### Medium — Valid unresolved rows are also reported as invalid

The exact current accounting is complete but unresolved: `.ufo/waves/round-21/frozen/required.json:5-20` names `aggregator-r10` and `aggregator-r10-resume`; `corpus/evidence/loss-accounting-r21.json:5-23,26-45` has both rows carrying baseline, deletion, and cleanup provenance and `independent_disposition: null`. `.ufo/waves/round-21/evidence/historical-provenance.json:38-40` says disposition is null, settlement unknown, and same-identity cleanup is not settlement.

For these rows, the candidate's audit loop adds an ID to `omitted` only when no accounting row exists (`.scratch/round21/ImplLoss/tools/mori-evidence-loss.py:514-522`), and adds each present `state: "unresolved"` row to `unresolved` (`:540-545`). Therefore the source-level expected result for this input is `omitted=0`, `unresolved=2`, `disposed=0`, `pin_allowed=false`, rc 1 (assuming the referenced evidence validates). This repairs the representation loss without declaring either wave settled.

However, the unresolved branch calls `add_issue(..., "unresolved")` (`:540-545`), and `add_issue` unconditionally adds every issue ID to `invalid_ids` (`:497-508`). The output consequently also reports both normal unresolved rows in `invalid` (`:595-598`). The `pin_allowed` check and return code remain blocked by unresolved state (`:600-619`), but the output conflates the expected rc-1 blocker with bad evidence. The current selftest only checks rc, pin blocking, and an unresolved finding; it does not assert zero omissions, both unresolved IDs, or absence from `invalid` (`:806-811`).

**Smallest safe change:** retain the unresolved finding and its stable ID, but allow `add_issue` to record a non-invalidating blocker (or omit the redundant issue, since `unresolved` already contains the finding). Use that path only for valid `unresolved` + null disposition. Keep malformed, stale, contradictory, or unexpected disposition evidence invalid. Extend the existing unresolved selftest to assert `omitted=[]`, both required IDs in `unresolved`, `invalid=[]`, `pin_allowed=false`, and rc 1.

## Residual risk and verification gaps

- Verdict on the requested unresolved case: **yes**, this data model retains the two historical identities as unresolved and blocks acceptance; it does not fake closure for those rows. The invalid-count defect misstates their validity, and the separate disposed-path defect prevents claiming the candidate is closure-safe in general.
- The inspected evaluator is the isolated candidate `.scratch/round21/ImplLoss/tools/mori-evidence-loss.py`; no integrated `tools/mori-evidence-loss.py` appeared in the `tools/` directory listing. These are static conclusions, not observed CLI output. No tests, candidate execution, census, pin, or production writes were performed.
- `read xd://lsp` reported that no `lsp` tool is mounted. References/definition/diagnostics were unavailable; no grep output is used as semantic proof. No tools were installed.
