# MutDigestTrust — proposed trust-boundary probe

Status: **proposal written; not executed**. No target invocation, production mutation, census, pin, broad test, build, lint or formatter was run. No tools were installed or updated.

## Axes and scope

- **C1 freshness:** challenge whether otherwise structurally valid declared-disposition evidence is refused when its bytes or file type become untrustworthy. A synthetic declaration is not independent historical acceptance.
- **Calibration of the conclusion:** a refusal counts only with successful pristine and restored controls; this probe does not verify C2's separate `classify` evaluator or establish historical settlement.
- Design constraints: one changed evidence leaf per case, identical evaluator and command across each three-phase sequence, exact restoration, bounded execution and seat-local writes.

Authority: `.ufo/waves/round-21/contract.md:7,14-16`. Line 14 requires committed relative provenance, hash validation beneath `--root`, rejection of symlink components, and prohibits unknown/malformed/stale evidence from resolving a row. The same line specifies `mori-evidence-loss-audit-v1`, `pin_allowed`, counts and rc0/1/2 semantics.

## Candidate

`.ufo/waves/round-21/build/MutDigestTrust/proposed-probe.py`

The standalone stdlib script snapshots the supplied lane-local audit implementation, creates two independent synthetic Git repositories beneath this seat, and proposes exactly six bounded audit calls: pristine / mutated / restored for each case. Independent repositories run concurrently; each case's causal sequence is ordered. Each subprocess has a ten-second timeout. No repository is cloned, no historical wave evidence is used, and synthetic cleanup/disposition actors differ. The fixture deliberately uses a synthetic wave ID, never `aggregator-r10` or `aggregator-r10-resume`.

The evidence files are committed first; their actual commit OID and SHA-256 values are used in the required/accounting objects, which are then committed. Both original disposition bytes and an identical-bytes twin exist as regular committed files before any mutation. See `proposed-probe.py:99` for construction and `:274` for the snapshot/receipt entry point.

The implementation seat confirmed the planned cleanup/disposition reference fields and matching disposition JSON payload (`id`, `actor`, `wave_id`, `disposition`, `independent`). The candidate includes those payload fields and actual full commit IDs. Its required `evidence` value is a relative `path:positive-line` string (`evidence/baseline.json:1`), not a second reference object. This is declared-record validation, **not actor authentication**; the implementation's announced trust basis is `declared-record-not-authenticated`.

## Mutants and expected detector

The latest candidate emits integer counts for `omitted`, `retained`, `unresolved`, `disposed`, and `invalid`, plus corresponding `<field>_ids` row arrays. The script requires each count to agree with its array and every listed ID to equal the fixture wave. Source: `.scratch/round21/ImplLoss/tools/mori-evidence-loss.py:620-634` (read-only snapshot `#0E4A`). The earlier array-only envelope was superseded before any execution.

| Case | Smallest changed point | Unchanged controls | Expected observation |
|---|---|---|---|
| `digest-mismatch` | Append one legal JSON whitespace byte to `evidence/disposition.json` (`proposed-probe.py:222-223`). | JSON semantics, all provenance references including digest and revision, cleanup actor, disposition actor, wave ID, accounting state and evaluator. | rc1; correct audit schema; `omitted=0`, `disposed=0`, `invalid>=1` with the fixture row in `invalid_ids`, `pin_allowed=false`; exact `independent_disposition:hash_mismatch` issue/finding ID. |
| `symlink-substitution` | Replace that regular disposition leaf with a relative symlink to the pre-existing identical-bytes twin (`proposed-probe.py:225-227`). | Resolved content digest, in-root location, provenance objects, actors, wave ID, accounting state and evaluator. | Same refusal oracle, with exact `independent_disposition:unsafe_path` issue/finding ID. The content digest is intentionally unchanged, isolating link substitution from digest tampering and out-of-root traversal. |

The common **healthy structural control** (`proposed-probe.py:166`) explicitly follows the implementation seat's later co-evolved trust refinement: rc1, correct schema, `omitted=0`, `retained=1`, `unresolved=1`, `disposed=1`, `invalid=0`, `pin_allowed=false`; the disposed ID has `status=structural_only`, the unresolved ID has `reason=external_review_required`, and the sole issue is the exact external-review finding. This does **not** treat rc1 alone as success: every count, ID and required marker must match. The refusal detector at `:182` checks the fixture ID, field, reason, and full stable finding ID `mori-evidence-loss:audit:synthetic-round21-mut-digest-trust:independent_disposition:<reason>`. Each three-phase sequence uses identical command/evaluator bytes.

A mutant is **killed** only after both explicitly specified healthy controls, exact restoration, unchanged protected files, and a correctly injected mutation are established, followed by the specified refusal. A valid observed result accepting the mutation, enabling pin, or still counting the untrustworthy receipt structurally disposed is **survived**, even if some other rule blocks pin. Failed controls, setup/input errors, timeouts, malformed output, or a nonconforming refusal are **inconclusive**, never a claimed kill.

## Restoration and receipts

The `finally` block (`proposed-probe.py:232-239`) unlinks the substituted leaf before writing, restores the saved original bytes and regular-file mode, compares SHA-256/type/mode, and invokes the same detector again. It does not write through the symlink. Other evidence files, both input documents, the Git index, and evaluator snapshot are fingerprinted and must remain unchanged. Each audit invocation records target state before and after to reject a mutating detector. Scratch repositories are retained for L1 inspection rather than destructively reset or removed.

When L1 elects to run this proposal, it writes a fresh `probe-*/result.json` beneath the named directory, containing the exact command arguments, actual stdout/stderr and their SHA-256 values, exit codes/timeouts, parsed JSON, before/mutated/after file states, restoration checks, and per-case verdicts. Exit 0 means both mutants killed, 1 means at least one survived with no inconclusive case, and 2 means at least one inconclusive case or setup failure.

## Control revision and static finding disposition

**[INFERENCE — not executed]** Earlier implementation snapshot `#3ED0` rejected a valid disposition reference: `.scratch/round21/ImplLoss/tools/mori-evidence-loss.py:562-564` required seven metadata keys, while `:580-583` passed that full object to `_check_reference`, whose `:415-419` allowed only basic provenance keys. This was reported without editing sibling source. The implementation seat subsequently reported that validator fixed; no runtime confirmation was performed here. Preserve this as a candidate-development finding, **not a current verified blocker or historical production defect**.

The implementation seat explicitly identified its subsequent external-review behavior as a **co-evolved trust refinement, not the frozen contract's final-disposition result**. The latest observed source records a healthy declared receipt as both `structural_only` disposed and `external_review_required` unresolved (`.scratch/round21/ImplLoss/tools/mori-evidence-loss.py:582-595`, snapshot `#0E4A`). No outside-acceptance schema or fixture interface was supplied, and this probe fabricates none. Its receipt names `control_oracle=co-evolved-structural-only-external-review-v1` and `frozen_contract_acceptance_claim=false`. The changed healthy control is disclosed, not silently treated as proof of frozen-contract rc0/final settlement. The assigned digest/symlink refusal invariant is unchanged: a mutated receipt must disappear from even the structural disposed set and produce the specific invalid-evidence finding.


## Deferred invocation — not run by this seat

```sh
TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-21/build/MutDigestTrust/proposed-probe.py --audit-script /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-evidence-loss.py
```

The production tool path was absent in the scoped discovery output during drafting; `--audit-script` can select an isolated lane-local candidate. `.scratch/round21/ImplLoss/tools/mori-evidence-loss.py` was subsequently read only to align the proposed fixture, array envelope and finding IDs; it was never executed. Fixture acceptance and CLI behavior remain unverified; implementation differences must produce an inconclusive positive control, not a presumed invariant failure. No historical independent disposition may be inferred from these synthetic fixtures, and this report grants no pin permission.

## Actual outputs and verdict

- Mutant execution: **not run**, as assigned. No runtime audit outputs or pristine/mutated/restored evidence hashes exist yet; no killed/survived verdict is claimed.
- Restoration evidence now: no target bytes were modified. Runtime restoration evidence is deferred to the generated receipt.
- Authored script fingerprint command actually exercised:
  `sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-21/build/MutDigestTrust/proposed-probe.py`
- Actual final artifact output: `5f7870a6184ea3b51871d39465e8a4dc9ed670bdf3b9f183412f1274970d6a88  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-21/build/MutDigestTrust/proposed-probe.py`

Report: `.ufo/waves/round-21/build/MutDigestTrust.md`
Candidate: `.ufo/waves/round-21/build/MutDigestTrust/proposed-probe.py`
