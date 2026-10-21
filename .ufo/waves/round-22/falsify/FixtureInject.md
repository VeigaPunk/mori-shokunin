# FixtureInject — frozen v2 `inject` variant (R06) and its oracle predicate

Seat MoriR22.FixtureInject, critic. Static analysis only. No fixture, oracle, tool, test or build was executed. Read-only inputs:
- correction and contract (`denominator-correction.md`, `contract.md`)
- `frozen/fixture-builder-v2.py`, `oracle-reconcile-v2.py`, `frozen/requirements-v2.json`, `refinement-reconcile.py`, `measure-round22.py`
- shipping `tools/mori-retention-reconcile.py` and `tools/mori-retention-gate.py`
- retained `evidence/measure1/*-observed.json` and `refinement-observed.json`, parsed for exit, finding, differences and fixture metadata fields only

No matched text appears in this report. The synthetic token is called "the token".

Installs: none.

## Pins verified against current source
- The loaded SHA-256 values equal the pins in `requirements-v2.json`:
  - `fixture-builder-v2.py` is 1b3e16f7…
  - `oracle-reconcile-v2.py` is dcd1c7c6…
  - `contract.md` is 1658c390…
  - `denominator-correction.md` is 968945b2…
- The three v2 artifacts are first committed in e2f549b. The SUT is first committed in 8cb4afb. e2f549b is an ancestor of 8cb4afb, so the fixture was frozen before implementation.
- The shipping tool is d6870fb6… (last changed in 3985b3d) and is clean in the worktree. measure1 at 4f7cfce ran this exact tool hash, both in `after-observed` and in the summary.
- `refinement-reconcile.py` was added in 8cb4afb together with the implementation. It is co-evolved, not pre-registered.

## Axes
- **A1 attribution:** R06 passes only because of the injected identity, not a setup error, crash or unrelated mismatch.
- **A2 expectation truth:** the expected identities and partitions that the fixture emits for this variant are true.
- **A3 mutation confinement and provenance:** the mutation touches only the receipt and is reproducible. No restoration is needed.
- **A4 population over scalar (lesson M1):** detection needs identity comparison, not count agreement.

## Trace of `make(root,'inject')` through the shipping SUT
Measured tree: `policy.json`, `allowed.txt`, `unallowed.txt`, `non-author.txt`, `binary.bin` (contains NUL) and `allowlist.json`.

Hits (5, matching the gate's `_blob_hits`: same split, digest and decode, per class per line):
- `policy.json` line 12 (the `synthetic` key; the regex line does not match)
- `allowed.txt` lines 1 and 2
- `unallowed.txt` line 1
- `non-author.txt` line 1

`allowlist.json` and `binary.bin` contribute no hits. The receipt is not in the measured tree.

The mutation appends `{path:injected.txt, line:1, class:R22, line_sha256:0×64}` to `result['hits']` only. `wrapper['stdout']` is re-serialized after the mutation (line 93), so the mutation reaches the committed receipt. `exit_code` stays 1, which is consistent with recomputation.

Every SUT setup guard passes for this variant:
- safe paths, regular blobs, wrapper schema
- 40-hex measured revision that resolves to itself
- ancestor check
- policy and allowlist bytes unchanged
- policy schema, and allowlist rows with `rule=b`
- exit type, empty stderr, argv repo/policy/allowlist/`--rev` bindings
- inner `commit` and `policy_sha256`
- integer counters
- `normalize_hits`: the injected hit has exactly 4 fields, a positive int line, a 64-hex sha, and is not a duplicate
- empty auxiliaries, and no population keys

The only difference at comparison (line 212) is the `hits` multiset. Partitions, metric, routed, non_author, finding_id, forbidden, warnings and exit all agree.

Retained measure1 confirms this: inject exits 1 with `RETENTION_RECONCILIATION_MISMATCH`, `differences:["hits"]`, `raw_total` 5, `scanner_total` 4, `receipt_match:false` and empty stderr.

## Findings

### F1 — Setup error versus target reason: distinguishable (A1 holds for setup and crash)
- The oracle requires `exit==1`, a JSON `finding_id==MISMATCH`, and `stderr==''`.
- The SUT emits SETUP only with exit 2.
- An uncaught exception (not in the caught set) produces a traceback on stderr and non-JSON stdout, so it cannot pass.

Fragility: `make()` records `str(root)` unresolved in the receipt argv. If the oracle `--output` is relative, `receipt_repo_binding` fires and every arm returns 2. This fails closed (R01 fails too), so it cannot cause a false pass. `measure-round22.py` passes an absolute scratch path, and every retained repo path is absolute.

### F2 — The R06 predicate does not attribute the reason, and the arm is internally incoherent (A1 and A4 defect)
**Counterexample A — scalar agreement passes R06.** The retained `mutant-count-only-observed.json` shows R06 passing (count 6≠5). The same file shows R05 and R10 passing. That mutant is killed only by R07, R08 and R09. R06 by itself is satisfied by a scalar count check, which is exactly what lesson M1 says cannot establish population agreement.

**Counterexample B — unrelated extra reasons pass.** The retained `mutant-wrong-population` inject run gives `differences:["hits","unallowlisted_hits","metric"]` and still passes R06. The predicate accepts any mismatch.

**Counterexample C — no recomputation needed.** The inject receipt is internally inconsistent: 6 hits against 3 allowlisted + 1 unallowlisted + 1 non_author = 5. A SUT that never scans, and only checks receipt-internal cardinality, passes R06.

**Frozen24 never isolates the raw `hits` multiset under preserved cardinality.** `result['hits']` is the same list object as `hits`, and `hits[0]` is the same dict as `allowlisted_hits[0]`. So the digest, line and class arms also change `allowlisted_hits`; retained differences are `["hits","allowlisted_hits"]` for all three. Drop and inject change the count. A SUT can pass all 24 frozen arms while never comparing the receipt's raw `hits` against recomputation, as long as it compares:
- the partition lists,
- the scalar counters,
- and `len(hits)` against the partition sum.

Only the co-evolved refinement `path-only` kills that SUT.

**Contract ambiguity.** The frozen arm is the "hits only" A′ arm that build note AttackR06 flagged as ambiguous. The contract says "required field/type/schema inconsistencies must fail closed". A defensible SUT could return 2 for an internally inconsistent receipt and would then fail R06. The frozen expectation pins this as exit 1 without stating the pin.

**Impacted axes:** calibration (the R06 pass overstates identity detection) and depth (the M1 criterion is not fail-capable through R06).

This is not a shipping defect. The current SUT compares the full multiset, and its observed reason is exactly `hits`.

### F3 — False expected identities in the inject fixture record (A2 defect, provenance only)
Because of the same aliasing, `inject` appends to the `hits` list from which the return dict computes `expected_scanner_hits`.

Retained `after-observed.json`, `runs[variant=inject].fixture`:
- `expected_scanner_hits` has 5 entries, including the phantom `injected.txt`
- `expected_scanner_total` is 4
- `expected_raw_total` is 5

The record contradicts itself. The `duplicate` variant has the same defect: 5 entries with `policy.json` listed twice.

No predicate consumes these fields: R04 reads only the valid variant, and R06 and R19 have no predicate. So no verdict changes, but the retained run evidence carries false expectations.

`expected_policy_hits` (the single non-author identity) and the hard-coded 5/1/4 counts are true for the inject tree.

### F4 — Mutation confinement and provenance hold (A3 holds)
Each variant gets a fresh `exist_ok=False` directory, and the oracle cache is keyed by variant, so nothing needs restoring.

In retained evidence, valid and inject share:
- an identical measured commit OID (deterministic author, committer, dates and tree)
- identical policy and allowlist digests
- identical `expected_policy_hits`

The only difference in their worktree file digests is `receipt.json`.

The mutation is pre-commit and receipt-only, and it never touches the measured tree.

### F5 — Residual gap across frozen24 and the 27 refinements: non-author identity forgery (A4)
Consider a SUT that compares receipt identities only for the scanner population, plus raw `len(hits)` and the `non_author` scalar. It passes every frozen and refinement arm:
- drop: count
- inject, digest, line, class, `path-only`, `forged-clean`: scanner identities
- list-only arms and non-author overlap: partition lists
- non-author counter: scalar

It accepts a count-preserving swap of the non-author hit's identity. Non-author hits appear only in raw `hits`, which the contract calls authoritative.

The shipping SUT is not vulnerable to this. The gap is in oracle coverage.

## Smallest safe corrections
The frozen files are hash-pinned, so do not edit them. Add co-evolved refinement arms or criteria instead.

1. **`non-author-swap` refinement.** Parse the receipt, set `line_sha256` to 0×64 (or `line+=1`) on the `non-author.txt` hit in `hits` only, and re-serialize. Expect:
   - exit 1 with MISMATCH
   - `receipt_match:false`
   - `(raw_total,policy_excluded,scanner_total)==(5,1,4)`
   - `non_author==1`
2. **`inject-coherent` refinement.** Append the fabricated scanner-path hit to both `hits` and `unallowlisted_hits`, and set `metric+=1`. Expect exit 1 and recomputed `raw_unallowlisted==1`. This defeats internal-cardinality-only SUTs.
3. **Attribution criterion for R06** (refinement side, contract fields only):

   ```
   receipt_match is False and (raw_total,policy_excluded,scanner_total)==(5,1,4) and raw_unallowlisted==1
   ```

   This shows the verdict comes from recomputation, not from the receipt's 6.
4. **Explicit pin in L1's disposition.** A well-typed, internally inconsistent receipt is exit 1, not a schema failure.
5. **Annotation.** Mark `runs[].fixture.expected_scanner_hits` for the `inject` and `duplicate` variants as aliasing-contaminated, so they are not used as expectations. A future v3 builder should store `copy.deepcopy(hits)` in `result`.

None of these changes the 24 requirement meanings, privacy_clearance=false, the retained four unallowlisted hits, or any historical disposition.
