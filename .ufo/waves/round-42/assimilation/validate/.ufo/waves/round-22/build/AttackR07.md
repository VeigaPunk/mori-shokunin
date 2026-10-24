# AttackR07 — attack on frozen R07: "altered digest returns 1"

Scope: R07 only. Static review; no tests/builds/oracle runs (wave bounds). No `lsp`
device is mounted in this seat — caller/definition/diagnostic checks unavailable;
review is by direct file reads (recorded per role fallback rule).

## 1. What R07 actually pins

- Frozen arm: `oracle-reconcile.py:51` maps `R07 → variant 'digest'`, expecting
  `exit_code==1`, `finding_id=='RETENTION_RECONCILIATION_MISMATCH'`, `stderr==''`,
  and stdout parseable as a JSON dict. No predicate.
- Mutation: `fixture-builder.py:80` / `fixture-builder-v2.py:81`:
  `result['hits'][0]['line_sha256']='0'*64` on the embedded retention result inside
  the `mori-r21-command-receipt-v1` wrapper's `stdout`.
- Semantics: a *valid-schema* digest (`[0-9a-f]{64}`) whose value disagrees with
  independent recomputation must be exit **1**, not 2. Malformed digests are a
  schema question (see §4).

## 2. Canonical counterexample and expected outcome (v2 builder semantics)

Under `frozen/fixture-builder-v2.py`, variant `digest`:
- `hits[0]` is the `policy.json` hit (the `'synthetic': 'R22_SAMPLE'` line — the
  `[R]22_SAMPLE` regex does **not** match its own literal source line).
- Because the builder shares hit dict objects across lists, the same mutation also
  lands in `allowlisted_hits[0]` (see Defect B).
- Expected of a correct SUT: exit 1, `finding_id=RETENTION_RECONCILIATION_MISMATCH`,
  `receipt_match=false`, `privacy_clearance=false`, counters unchanged —
  `raw_total=5, policy_excluded=1, scanner_total=4, raw_unallowlisted=1,
  scanner_unallowlisted=1, non_author=1, allowlisted=3, forbidden_allowlist=0,
  retention_state='red'`. Differences limited to `{'hits','allowlisted_hits'}`.
- Verified by inspection that the committed SUT (`tools/mori-retention-reconcile.py`,
  HEAD 3985b3d) meets R07's letter under v2: `normalize_hits` accepts `0`*64
  (`SHA.fullmatch` passes), then `claimed['hits']`/`claimed['allowlisted_hits']`
  Counters differ from recomputation → `differences` non-empty → exit 1. SUT
  verdict remains L1/oracle business; this is evidence-shape review only.

## 3. Findings (severity order)

### A. BLOCKER — committed oracle/fixture pair cannot produce R07's intended evidence
- `oracle-reconcile.py:13` hard-imports `frozen/fixture-builder.py` (v1). v1
  allowlist rows lack the `rule` field (`row={k:v for k,v in h.items() if
  k!='line'}; row['reason']=…`), but gate-schema requires
  `{path,class,line_sha256,reason,rule}` (gate `_validate_allowlist`,
  `expected_fields` line 142; SUT `allow_rows` requires the same set).
  → Every arm including `digest` exits **2 `RETENTION_RECONCILIATION_SETUP`**
  against a correct SUT: R07 "fails" with the wrong failure kind, masking true
  digest behavior.
- Pin mismatch: `requirements-v2.json` pins `fixture_builder_sha256=1b3e16f7…`
  (matches v2 file ✓) and `oracle_sha256=dcd1c7c6…`, but the committed/checked-out
  oracle hashes `90d85e5a…` and still names `fixture-builder.py`. No committed blob
  matching the pinned oracle exists in history (checked all revs touching the
  path). Actionable criterion: the oracle actually executed for R07 evidence must
  import `fixture-builder-v2.py` and its self-reported `oracle_sha256` must equal
  the `dcd1c7c6…` pin; otherwise the R07 run is off-pin regardless of pass/fail.

### B. Aliasing makes R07 non-attributable; partition lists go unvalidated by design
- Builder inserts the *same dict objects* into `hits` and
  `allowlisted_hits`/`unallowlisted_hits` (`allowed`/`unallowed` are filtered
  references, `allowlisted_hits`:allowed_effective). So `digest`, `line`, and
  `class` arms each coherently mutate **two** receipt fields.
- Consequence: R07 cannot distinguish a SUT that validates only `hits` from one
  that validates only `allowlisted_hits`; and a SUT that validates `hits` but
  ignores `allowlisted_hits`/`unallowlisted_hits`/`forbidden_allowlist`/`warnings`
  entirely still passes R05–R09 and R07 — no variant mutates a partition list
  while `hits` stays intact.
- Actionable criterion: add a partition-only arm, e.g. deep-copy hits into the
  partition lists at build time (`copy.deepcopy`) then mutate only
  `unallowlisted_hits[0]['line_sha256']` (or `allowlisted_hits` for a policy hit).
  Correct SUT: exit 1, difference `unallowlisted_hits` only, `hits` matching.
  A hits-only validator exits 0 → caught.

### C. Arm binding is exit+finding only — wrong-reason passes admitted
- `record()` asserts nothing else for R07. A SUT that returns MISMATCH without
  recomputing (constant mismatch, or diff driven by an unrelated bug) passes R07
  while failing the capability claim.
- Actionable predicate for the R07 record:
  `v.get('receipt_match') is False and v.get('raw_total')==5 and
  v.get('scanner_total')==4 and v.get('raw_unallowlisted')==1 and
  v.get('retention_state')=='red' and v.get('privacy_clearance') is False`.
  (`receipt_match` is in the contract's explicit output list, so asserting it is
  contract-safe; `differences` is SUT-specific — do not require it.)

## 4. Semantic ambiguities in "altered digest"

1. **Which digest?** The receipt carries ≥5 digest surfaces: hit `line_sha256`
   (in `hits`, `allowlisted_hits`, `unallowlisted_hits`), `policy_sha256`,
   `commit`, and auxiliary (`forbidden_allowlist`/`warnings`) row digests.
   Only `hits[0].line_sha256` is pinned. `policy_sha256` mutation forks: the SUT
   treats it as input inconsistency → exit 2 (`receipt_policy_digest`), but exit 1
   ("valid receipt disagrees with recomputation") is defensible; the contract
   doesn't resolve it. Pin a decision + arm.
2. **Malformed vs wrong value.** `0`*64 → 1; non-64-hex or uppercase hex →
   schema reject → 2 (SUT `SHA` is lowercase-only, matching gate `SHA256_RE`).
   Oracle has no malformed-digest arm; the 1-vs-2 boundary is unpinned. Add arms:
   `'zz'*32` (expect 2) and `'A'*64` (expect 2).
3. **Auxiliary digests.** `forbidden_allowlist`/`warnings` rows carry
   `line_sha256` (line=None). Mutating one in the `forbidden` variant should
   yield 1; no oracle arm exercises it — a SUT skipping `auxiliary()` validation
   passes undetected.
4. **Attribution optional.** Nothing requires `differences`/error code naming;
   a SUT may emit MISMATCH for *any* disagreement and still satisfy R07's letter.

## 5. Superficial-pass catalog (what R07 does and doesn't catch)

| SUT shortcut | R07 outcome |
|---|---|
| Counter/length-only `hits` comparison | Fails R07 correctly (identity multiset required) |
| Identity = (path,line,class), ignores `line_sha256` | Fails R07 correctly — the arm's only discriminator is the digest field |
| Validates `hits` only, ignores partition/auxiliary lists | **Passes** R07 (Defect B) |
| Constant MISMATCH / mismatch for wrong reason | **Passes** R07 (Defect C); only caught jointly via R01-style clean arms |
| Scans worktree instead of measured-revision blobs | **Not exercised** by `digest` arm (receipt.json contains no token hits; blob-vs-worktree blind spot is only indirectly bound by R24) |

## 6. Verification gaps / residual risk

- Everything above is static reasoning; no oracle/SUT run was performed (forbidden
  this wave). Observed fixture-aliasing claim verified by reading the builder's
  list construction (`allowed=[h for h in hits …]` filters, not copies).
- The v1→v2 exclusion-semantics correction (commit e2f549b) means R07 results are
  only meaningful under the v2 builder + v2-pinned oracle; evidence produced under
  the committed oracle (v1 builder) should be treated as off-pin.
- Real-receipt R01 path exists (`expected-real.json` ↔ r21 `retention-floor.json`:
  95 raw / 5 non-author / 90 scanner / 4 unallowlisted); no R07-style mutation arm
  exists against the *real* receipt — synthetic-only coverage is a residual gap
  for R07's "existing receipt" wording.
- No installs/updates performed; no tooling changes. Repo state observed dirty
  with sibling build artifacts; fixture/oracle files read-only as found.
