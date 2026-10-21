# AttackR05 — frozen requirement R05: "dropped receipt hit returns1"

Static review only; no code executed, no fixtures run, no tests. Evidence: contract.md,
denominator-correction.md, frozen/fixture-builder-v2.py, oracle-reconcile-v2.py,
tools/mori-retention-reconcile.py (committed 8cb4afb), tools/mori-retention-gate.py.
LSP device unavailable in this seat → file-level reads used; noted per role.

## 1. Pinned semantics (the load-bearing fact for R05)

The receipt's `hits` list is the **raw** population, not the scanner partition. In the
existing gate, `_scan_result` emits `result["hits"] = hits` — the unpartitioned raw scan
output (tools/mori-retention-gate.py:296). `non_author`-globbed hits appear in `hits`
but in neither `allowlisted_hits` nor `unallowlisted_hits`. Therefore R05 means:

> `Counter(receipt.hits) == Counter(recomputed_raw_hits_at_measured_revision)` must hold,
> including the policy_excluded (non-author) identity; any deficit → exit 1,
> finding_id `RETENTION_RECONCILIATION_MISMATCH`, stderr empty, privacy_clearance=false.

An implementation comparing receipt `hits` against `scanner_hits` (raw minus excluded)
is wrong even though both are 4-long in the fixture.

## 2. Verified current wiring (static trace)

- Fixture: `frozen/fixture-builder-v2.py:79` — `variant=='drop'` does
  `result['hits']=result['hits'][:-1]`. `hits` is built in `files` dict order
  (policy.json, allowed.txt, unallowed.txt, non-author.txt; binary.bin NUL-skipped),
  so the dropped identity is `non-author.txt:1` — exactly the v2 `policy_excluded` hit,
  present ONLY in `hits` (receipt still claims `non_author:1`). Well chosen: it is the
  one hit invisible to every partition list.
- Oracle: `oracle-reconcile-v2.py:51` — `record('R05','drop',1,'RETENTION_RECONCILIATION_MISMATCH')`
  asserts exit 1 + exact finding_id + `stderr==''`.
- Impl: `tools/mori-retention-reconcile.py:189,212-213` — `claimed['hits']` Counter vs
  `Counter(hit_key(h) for h in hits)` (raw scan) → `differences=['hits']` → exit 1.
  Trace confirms all preliminaries pass on the 'drop' receipt (measured is ancestor of
  rev, policy/allowlist byte-identical, argv bindings resolve), so the mismatch comes
  solely from the hits multiset. Correct.
- Correction note: the v2 denominator correction is what makes 'drop' a real
  discriminator — under corrected semantics `scanner_hits == receipt_hits_after_drop`
  exactly, so a scanner-side comparison exits 0 and is caught. Under the superseded
  v1 reading, 'drop' would exit 1 via the wrong mechanism (receipt≠scanner either way),
  i.e., a superficial pass the fixture could not detect. Retain v2 frozen inputs.

## 3. Findings by severity

### F1 (high) — R05 as frozen does NOT force recomputation; an internal-consistency-only SUT passes

The 'drop' receipt is **internally inconsistent**: it claims `non_author:1` while its
own `hits` contains zero non-author hits. A hypothetical implementation that never runs
`git ls-tree`/`cat-file` at all — that only cross-checks receipt fields against each
other — still flags this receipt (hits length 4 vs claimed non_author 1 / list
cardinality) and returns exit 1 + MISMATCH. It passes R05 without performing the one
thing the capability is for. Joint requirements (R03 counters) constrain this only if
the oracle's counter predicates run on the *valid* arm — which they do — but R05 itself
carries no recomputation proof.

**Concrete counterexample fixture CF-R05-1 ("self-consistent forged-clean drop"):**
base 'valid'; remove `unallowed.txt:1` from `result['hits']` **and**
`result['unallowlisted_hits']`; set `metric:0`, `finding_id:'RETENTION_CLEAN'`,
`wrapper['exit_code']:0`. Every declared field is now mutually consistent — the receipt
reads as a clean run. Only recomputation against the measured tree detects the drop.
Expected: exit 1, `RETENTION_RECONCILIATION_MISMATCH`, `receipt_match:false`,
recomputed counters `raw_total:5, policy_excluded:1, scanner_total:4,
raw_unallowlisted:1, scanner_unallowlisted:1`, stderr empty.
Actionable criterion: add this variant; R05 passes only if exit==1 with those counters —
a receipt-internal validator necessarily returns 0 (or omits counters) and fails.

### F2 (medium) — exit-1 vs exit-2 precedence is unpinned when a receipt is both malformed and disagreeing

Contract: "reject duplicate receipt hits" (R19 → 2) and "dropped receipt hit returns1"
(R05 → 1) with no stated precedence when both hold.

**Concrete counterexample fixture CF-R05-2 ("drop masked by duplicate"):**
base 'valid'; `result['hits'] = result['hits'][:-1] + [deepcopy(result['hits'][0])]`.
Count stays 5 (defeats length-only checks); multiset differs (non-author missing,
policy.json:1 doubled). Current impl exits 2 — `normalize_hits` raises
`duplicate_receipt_hit` at line 125 before the multiset comparison at line 212.
A multiset-diff-first implementation exits 1. Both defensible under the contract text.
Actionable criterion: pin **schema validation precedes population comparison** —
any receipt failing required-field/type/duplicate checks exits 2
(`RETENTION_RECONCILIATION_SETUP`), never 1, because an ill-formed receipt is not a
"valid receipt [that] disagrees". Then encode CF-R05-2 expecting 2; this matches the
committed impl's ordering and makes it explicit rather than incidental.

### F3 (medium) — oracle R05 arm does not pin recomputed output on the mismatch path

`record(...,1,'RETENTION_RECONCILIATION_MISMATCH')` checks only exit/finding/stderr.
An impl may pass R05 while emitting receipt-echoed or absent counters,
`receipt_match:true`, or no `differences` diagnostic on the exit-1 path.
Actionable criterion: extend the R05 (and sibling R06–R10) predicate to require
`v['receipt_match'] is False`, `v['raw_total']==5`, `v['scanner_total']==4`,
`v['raw_unallowlisted']==1`, `v['policy_excluded']==1`, `v['privacy_clearance'] is False` —
recomputed truth must be emitted even while the receipt disagrees (contract line 13
lists these counters unconditionally).

### F4 (low) — drop confinement ambiguity: drops in partition lists are an uncovered sibling case

"Receipt hit" most naturally scopes to `hits`, but the receipt also declares
`allowlisted_hits`/`unallowlisted_hits`. 'drop' truncates `hits` only. An impl checking
`hits` alone passes R05 while missing a receipt that keeps `hits` intact but drops from
`unallowlisted_hits` (a distinct defect family, arguably R10-adjacent).
Actionable criterion: the comparison rule must state that **each declared population
list is independently multiset-compared** to its recomputed partition — already true in
impl lines 212–217; worth one oracle variant (`drop` applied to
`unallowlisted_hits` only → exit 1) to freeze it.

### F5 (low) — per-hit unknown-field tolerance is ambiguous

Contract: "unknown receipt fields need not be rejected" (top-level) vs impl's strict
`set(hit)==HIT_FIELDS` (line 123 → exit 2 for a hit carrying an extra key). If a future
receipt writer annotates hit objects, a dropped-hit receipt containing annotated hits
exits 2, not 1 — R05's "returns1" silently overridden by a tolerance question.
Actionable criterion: state explicitly that the unknown-field tolerance applies to
top-level receipt and auxiliary rows only; hit objects are closed 4-tuples (impl's
current behavior) — or normalize extra keys away before comparison. Pick one; do not
leave it emergent.

## 4. Residual risk / verification gaps

- The committed `--selftest` (lines 233–257) has **no exit-1 arm**: three arms expect
  0/2/2. The only MISMATCH coverage is the external oracle. Contract's selftest clause
  ("assertions include exit and finding_id") is met literally, but an R05 regression is
  invisible to selftest. Recommend a fourth arm: same synthetic repo, receipt.json with
  the sample hit removed → expect 1 + MISMATCH.
- Multiset vs set is vacuous here (raw 4-tuples unique by path+line; receipt duplicates
  rejected). No defect — noted so reviewers don't over-read "multiset" wording.
- Order-insensitivity verified: Counter comparison; a receipt with reordered `hits`
  is agreement (correct — "exact hit multiset" is unordered).
- No runs performed; all traces above are static readings of committed code and frozen
  fixtures. Measured confirmation belongs to L1 integration.

## 5. Exact actionable criterion (R05 acceptance)

1. Fixture `drop` (existing) → exit 1, `RETENTION_RECONCILIATION_MISMATCH`,
   stderr empty; plus F3 predicates (`receipt_match:false`, recomputed counters
   5/1/4/1/1, `privacy_clearance:false`).
2. New fixture CF-R05-1 (self-consistent forged-clean drop) → same expectations;
   fails any non-recomputing implementation.
3. New fixture CF-R05-2 (drop + compensating duplicate) → exit 2,
   `RETENTION_RECONCILIATION_SETUP`; codifies schema-before-comparison precedence.
4. Contract clarification: per-hit objects closed; per-declared-list independent
   multiset comparison; setup-validation precedes population comparison.
