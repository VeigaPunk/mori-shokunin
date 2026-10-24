# FinalEvidence — C1 measured revision/hash boundary

## Finding — Medium, acceptance-blocking: the before/after count is not bound to an immutable measurement receipt

The contract requires C1 counts “from committed snapshots with the same new evaluator” (`.ufo/waves/round-21/contract.md:7`), and it defines per-evidence provenance as `{path,revision,sha256}` (`:14`). It does not require the measurement record to bind the before/after *input snapshots*, evaluator bytes, invocation, and outputs to those identities. The phrase “before” also does not say whether this is the entry revision or a later, reconstructed empty-register projection.

### Concrete counterexample

The entry revision `e9f340ce986f82a60baad1b8e5ead655ab818a1c` contains the two historical `WAVE_UNSETTLED_AGE` rows in `corpus/evidence/baseline-r10-20261015T2231Z.json:26-27`. Its tree does **not** contain `.ufo/waves/round-21/frozen/required.json` (read-only `git rev-parse e9f340ce986f82a60baad1b8e5ead655ab818a1c:.ufo/waves/round-21/frozen/required.json` returned “path … does not exist in 'e9f340…'”). The required list instead exists at current commit `8fed329636f53455ae2f53930c171c6186aff1fd`; its blob is `6124b34fd3e2382290e754e78c35a5d1e6b81e85`, and its raw-byte SHA-256 is `0385848e7b051d618ad71f69855974ca105382ae94e3e312e2236a04c0c837e9`. It names both IDs and points back to the entry baseline revision/hash (`frozen/required.json:5-20`). The empty `frozen/before-accounting.json` is also a later committed fixture at 8fed…, blob `17a91f3817aab034a84d1c15e6a24aafbcb6661e`, SHA-256 `a8938c0ee29776915b915abc5f7cb96ee357def4a67cd80befc8aba8c6bd6d14` (`:1-4`). The historical baseline itself is tied to e9… blob `3bcf93aec486fdea19badb61d4e6b77850e52ee0`, SHA-256 `0993b23505deab2aeb05b2309bdf7dd6eaad2b82f27852491352511aa9670478` (`evidence/historical-provenance.json:3-5`).

Thus a later empty-register fixture can be a valid **replay input**, but it is not an input present at the entry revision. If a report states only “before omitted=2; after omitted=0; same evaluator,” it can misrepresent a reconstructed replay as a measurement of the entry tree. Likewise, running the same command against mutable working-tree files and retaining only those counts does not establish that either run consumed the claimed committed bytes. This is an acceptance-proof gap, not evidence that an auditor actually misbehaves.

At the reviewed HEAD there is no committed `frozen/after-accounting.json` or `tools/mori-evidence-loss.py` (`git cat-file -e HEAD:<path>` returned “does not exist in HEAD” for each); no before/after audit output or evaluator digest is available. No runtime result is claimed.

### Smallest safe change

Add a compact C1 measurement-receipt requirement and label the “before” input accurately as a committed **reconstruction/replay** of the empty-register state, sourced from the entry baseline—not as an execution at e9. For each side, record:

- the full commit ID and path for required/accounting inputs, each Git blob ID and SHA-256 of the exact bytes, plus the committed identity/hash of every referenced evidence file;
- the evaluator path, full source commit, blob ID, raw-byte SHA-256, interpreter version, and identical command/argument shape for both runs;
- the exact return code, full raw stdout/stderr (or saved bytes with SHA-256), and complete parsed audit JSON for both runs.

Run only from those pinned committed bytes, never the mutable checkout. The receipt must show the C1 distinction from the JSON, not infer it from exit status: the reconstructed before run has `omitted=2`; the after run has `omitted=0`, `unresolved=2`, and `pin_allowed=false` (also retain/report every other count and issue). Both are expected to return rc 1 under the contract’s omission/unresolved semantics; equal rc values alone do not demonstrate the repair (`contract.md:14`).

## Residual risk and verification gaps

- Read-only contract, frozen-input, and historical-baseline review only. No tests, builds, pins, census, or production writes were run; no tool was installed or updated.
- No evaluator or after-accounting snapshot exists at the reviewed HEAD, so the actual count delta, output bytes, and same-instrument behavior remain unverified. The finding addresses only the C1 measurement identity/receipt requirement; it does not assess unrelated acceptance or policy issues.
- This review covers the contract and JSON data only; it makes no source-caller or diagnostic claim.
