# AttackR02 — attack on frozen requirement R02 (retention denominator reconciliation)

Seat: MoriR22.AttackR02. Static review only; no tests, builds, or fixture runs executed.
Scope: R02 exclusively. Read: contract.md, denominator-correction.md (e2f549b),
frozen/requirements{,-v2}.json, frozen/fixture-builder{,-v2}.py, oracle-reconcile{,-v2}.py,
tools/mori-retention-gate.py (existing gate semantics), tools/mori-retention-reconcile.py
(impl candidate at 8cb4afb), and the real receipt .ufo/waves/round-21/evidence/final/retention-floor.json.

## 0. Governing text

Frozen R02 (contract.md:19): "retained red yields raw/scanner_unallowlisted>0 but
privacy_clearance=false and reconciliation0". Decomposed conjuncts:

- C-a: exit_code == 0 and finding_id == RETENTION_RECONCILED (contract.md:15: "Exit0 …
  exact accounting agreement (even retention_state=red)").
- C-b: raw_unallowlisted > 0 AND scanner_unallowlisted > 0, as ints (contract.md:15
  "Explicit booleans not accepted as ints" applies symmetrically to honest output fields).
- C-c: retention_state == 'red' — the only vocabulary value the contract names.
- C-d: privacy_clearance is false, unconditionally (contract.md:13 explicit field list
  "privacy_clearance=false"; "A zero delta/new-hit count is not privacy clearance";
  "A matched receipt is not clean retention").
- C-e (implicit, load-bearing): the counters and state derive from the tool's own
  recomputation, not echoed from the receipt's claims. Otherwise C-b validates nothing.

Denominator-correction.md (committed before impl) supersedes the frozen contract's
source-policy-path subtraction: `policy_excluded` = non_author_paths_glob-matched
identities; `scanner_total` = raw hits not in non-author paths; "scanner_unallowlisted
remains 4 in the real input"; "privacy_clearance remains hard-coded false". Verified
against the real r21 receipt: 95 raw hits = 86 allowlisted + 4 unallowlisted + 5
non-author (round-17-verifier-spotcheck ×3, round-18-verifier-spotcheck ×2). The policy
file itself carries 4 allowlisted hits; its nested copy carries the 4 unallowlisted hits.

## 1. Exact actionable criterion for R02

Oracle arm must assert, on a valid retained-red receipt (current 'valid' fixture or the
real receipt bound to its measured tree):

1. `exit == 0`, `v['finding_id'] == 'RETENTION_RECONCILED'`, `v['receipt_match'] is True`,
   `stderr == ''`.
2. `isinstance(v['raw_unallowlisted'], int) and not isinstance(v['raw_unallowlisted'], bool)`
   and it equals the recomputed unallowlisted multiset cardinality (== receipt metric for an
   honest receipt). Same guard for `scanner_unallowlisted`. `==1` alone is insufficient:
   `True == 1` passes in Python (see §4).
3. `v['retention_state'] == 'red'` where 'red' is computed as
   `recomputed_unallowlisted > 0 or forbidden_allowlist > 0` (impl equivalent:
   recomputed gate exit code), never from wrapper `exit_code` or inner `finding_id`.
4. `v['privacy_clearance'] is False` — assert under BOTH red and zero-metric agreement
   fixtures. No current arm exercises the zero-value case (superficial-pass hole, §3 FX-3).
5. Discriminating lie-arms proving the counters are recomputed, not receipt-derived
   (§2 FX-1, FX-2). Without them, a receipt-echo implementation satisfies the frozen
   predicate while validating nothing.

Expected on the v2 'valid' fixture: exit 0 / RETENTION_RECONCILED / raw_unallowlisted=1 /
scanner_unallowlisted=1 / retention_state='red' / privacy_clearance=false /
raw_total=5 / policy_excluded=1(non-author)/ scanner_total=4 / non_author=1 /
forbidden_allowlist=0 / receipt_match=true.

## 2. Concrete counterexample fixtures (expected exit / finding / counters)

All are one-field mutations of the committed v2 builder 'valid' arm; each fits the
existing `make(root, variant)` shape and needs no new fixture machinery.

### FX-1 'unallowlisted-lie' — receipt partition lie, agreement must fail
Mutation: `result['unallowlisted_hits'] = []` (keep `metric=1`, `hits` unchanged,
`finding_id='RETENTION_FINDINGS'`, `exit_code=1`).
Honest expected: exit **1**, RETENTION_RECONCILIATION_MISMATCH. Impl at 8cb4afb
correctly flags `unallowlisted_hits` in `differences` (claimed Counter ≠ recomputed).
R02 attack surface: an impl that validates `hits`+`metric` only (or emits
`raw_unallowlisted = len(receipt['unallowlisted_hits'])`) returns exit 0 with
raw/scanner_unallowlisted=0 — superficially "reconciled" while the receipt hid its
retained hit behind the scalar. This is THE fixture that proves C-e. Cheapest variant:
shuffle one `unallowlisted_hits` entry's `line_sha256` while leaving `hits` intact.

### FX-2 'exit-lie' — wrapper exit lie on a self-consistent red receipt
Mutation: `wrapper['exit_code'] = 0`, inner result unchanged (metric=1, hits intact).
Honest expected: exit **1**, RETENTION_RECONCILIATION_MISMATCH (recomputed gate
exit = 1). Impl flags `exit_code` in `differences` ✔.
Kills: impls that propagate the wrapper's exit as the reconciliation exit, skip the
exit-vs-recomputation check, or derive `retention_state`/red solely from wrapper
`exit_code` (that mutant returns 0 here — the exact "reconciliation0 on red" the
frozen text demands). No existing arm touches `wrapper['exit_code']`.

### FX-3 'clean-agree' — zero-metric agreement, privacy_clearance probe
Fixture: allowlist rows additionally cover `unallowed.txt`'s hit (3 rows: policy-hit,
allowed.txt dedup, unallowed.txt). Inner result: metric=0, routed=0, non_author=1,
unallowlisted_hits=[], allowlisted_hits=3, finding_id='RETENTION_CLEAN',
wrapper exit_code=0. (non-author.txt hit remains non-author AND allowlisted — legal
overlap per gate partition order.)
Honest expected: exit **0** / RETENTION_RECONCILED / raw_unallowlisted=0 /
scanner_unallowlisted=0 / retention_state≠'red' / **privacy_clearance=false** /
receipt_match=true.
Kills: `privacy_clearance = not unallowlisted` derivations (emits true → caught),
`retention_state` hard-coded 'red' (caught iff oracle asserts ≠'red'), and
privacy_clearance-as-`False`-only-on-error paths. This is the only arm that tests
C-d at value 0; today's suite asserts it only at value 1.

### FX-4 'finding-lie' (cheap, optional) — inner finding_id lie
Mutation: `result['finding_id'] = 'RETENTION_CLEAN'`, everything else consistent.
Expected: exit **1** MISMATCH (impl compares inner finding vs recomputed
retention_finding ✔). Kills impls that skip finding_id reconciliation; guards the
"receipt exit" clause reading that includes declared verdict.

### FX-5 'red-nonauthor' — semantics discriminator for the ambiguous conjunct (§3 A-1)
Fixture: `non-author.txt` hit NOT allowlisted (drop nothing else), so it is non-author
AND non-allowlisted. Files: policy(1 hit, allowlisted), allowed.txt(2, allowlisted),
unallowed.txt(1, unallowlisted), non-author.txt(1, unallowlisted-in-raw-set),
binary.bin skipped. Honest receipt inner: metric=1, non_author=1, unallowlisted_hits=[unallowed.txt].
Expected counters decide the ambiguous reading:
- Partition-copy reading (v2 builder's own convention): raw=1, scanner=1 — always
  identical counters (degenerate but consistent with expected_raw_unallowlisted=1).
- Raw-set reading ("raw reports the raw population distinctly", contract.md:11):
  raw=2, scanner=1.
MUST be decided before this arm is usable; see A-1.

## 3. Semantic ambiguities (with recommended resolution)

- **A-1 raw_unallowlisted vs scanner_unallowlisted is degenerate under the corrected
  semantics.** Gate `unallowlisted` excludes non-author by construction
  (mori-retention-gate.py: `not _is_non_author(...) and key not in allowed_keys`), so
  unallowlisted-over-raw ≡ unallowlisted-over-scanner identically. The contract demands
  both counters "distinctly" yet no fixture can make them differ; impl emits the same
  integer twice (correct-but-tautological). Alternatively raw_unallowlisted could mean
  "raw hits failing the allowlist predicate" — then a non-author unallowlisted hit counts
  (raw=2, scanner=1 in FX-5). The v2 builder's `expected_raw_unallowlisted`=1 and the
  correction's "scanner_unallowlisted remains 4" imply partition-copy. RECOMMENDATION:
  L1 must pin one reading in the correction lineage; FX-5 discriminates. If partition-copy
  is intended, state that the counters are identical by construction so reviewers stop
  hunting phantom divergence.
- **A-2 'retained red' definition.** Red = recomputed gate verdict (`unallowlisted>0 or
  forbidden>0`, impl's `retention_code`), not receipt-declared. Frozen text supports
  recomputed (the receipt may lie). Impl already computes it this way; oracle never
  discriminates the two — FX-2 fixes that.
- **A-3 Non-red retention_state vocabulary.** Only 'red' is contracted. Impl emits
  'clean-at-frozen-regex-scope' — uncontracted. Either freeze a two-value vocabulary or
  assert `retention_state != 'red'` iff recomputed unallowlisted==0 and forbidden==0
  (FX-3). R23's string-leak check is unaffected either way.
- **A-4 Receipt stderr non-empty.** Contract lists `stderr` as a wrapper field but never
  says empty; impl requires `==''` → exit 2 on any non-empty stderr. Is that "required
  field/type inconsistency" (2) or a valid-but-divergent receipt (1)? Unwritten. Cheapest
  consistent call: treat `stderr` non-empty-or-non-string like `exit_code` — a validated
  wrapper claim → MISMATCH(1) if non-empty, SETUP(2) if non-string. Currently a real
  receipt carrying a warning line is unevaluable rather than mismatched.
- **A-5 Inner stdout must be exactly one JSON document.** Impl strict-parses; a real
  wrapper whose stdout has surrounding lines → SETUP(2), not MISMATCH. Contract silent;
  strict parse is defensible (receipt shape declares "stdout containing retention JSON"
  as a field) but should be pinned — R17's "malformed JSON" covers the wrapper, not
  explicitly the inner doc.
- **A-6 argv binding strength.** Impl binds `--rev` == measured_revision and
  `--policy`/`--allowlist` to the input paths (absolute under `--repo` or repo-relative),
  SETUP(2) on divergence. Contract only promises argv "appears in receipt" — nothing
  requires binding it to inputs. Over-strictness risk: a receipt run with `--policy` given
  as a worktree-relative variant spelling is setup-failed rather than reconciled. Pin:
  argv binding is informational (R24 provenance) or validated — pick one.
- **A-7 'reconciliation0'** is the tool's exit code (0 on agreement), orthogonal to the
  receipt's own exit_code (1 on red). Reading it as receipt exit propagates the red → the
  exact bug FX-2 kills.

## 4. Superficial-pass risks (what sails through today's suite)

1. **Receipt-echo counters.** Impl outputs `raw_unallowlisted = receipt['metric']` (or
   `len(receipt['unallowlisted_hits'])`). Valid fixture: emits 1/1, exit 0 — R02 passes
   while no independent partition exists. FX-1 catches the list variant; a metric-echo
   needs FX-1 plus R10 already present. Add FX-1 unconditionally.
2. **Wrapper-exit propagation.** Exit = wrapper exit_code → 1 on the red fixture → R02
   fails today, but only vacuously; the converse mutant (always-0 when lists agree)
   passes R01+R02 and only FX-2 catches it.
3. **bool coercion.** Oracle v2 `v['raw_unallowlisted']==1` accepts `True`. An impl
   emitting `"raw_unallowlisted": true` passes R02 verbatim. Criterion must type-guard
   (`isinstance int, not bool`) — contract.md:15's bool ban covers emitted fields too.
4. **privacy_clearance only ever tested at red.** `privacy_clearance = (metric==0)`
   passes every current arm. FX-3 is the only test of the contract's strongest clause.
5. **Hard-coded state.** `retention_state='red'` literal passes R02+R11; FX-3 catches.
6. **Equal counters never discriminated.** raw=scanner on every fixture means a
   single-counter impl is indistinguishable. Until A-1 is pinned (or FX-5 adopted), the
   "distinctly" clause is unfalsifiable — record it as such rather than pretending coverage.
7. **Oracle arm placement.** Oracle evaluates R02 on the shared 'valid' fixture; its
   predicate is value-exact (==1) only because the fixture has exactly one unallowlisted
   hit. Frozen text says >0 — keep ==1 (stronger, fixture-bound) but document that the
   generic clause is >0 so a future fixture with metric=2 isn't silently mis-scored.

## 5. Impl-candidate posture vs R02 (static)

tools/mori-retention-reconcile.py @8cb4afb recomputes hits/partitions independently
(scan over ls-tree blobs, fnmatch non-author, 3-tuple allowlist keys), compares
hits/unallowlisted_hits/allowlisted_hits multisets, metric/routed/non_author/finding_id/
forbidden/warnings/wrapper-exit, emits recomputed counters and hard-codes
privacy_clearance=False on every path including error paths. Against R02 it is
structurally sound; its remaining exposure is exactly §4 items 1–4 (untested mutant
space), A-3 (uncontracted 'clean-at-frozen-regex-scope'), and A-4/A-6 (strictness
choices the contract never pinned). No defect asserted; no run performed.

## 6. Verdict

R02 as frozen is passable but under-armed: the oracle arm asserts the happy path only.
Land FX-1 (list lie) and FX-2 (exit lie) as MISMATCH arms and FX-3 (clean agreement)
as the zero-value privacy_clearance arm; type-guard the counter assertions; pin A-1,
A-3, A-4, A-6 in the correction lineage. Until then a receipt-echo or exit-propagating
implementation can satisfy the letter of R02 while performing no reconciliation.

## Residual risk / verification gaps

- Not run: no fixture generated, no oracle or impl executed (wave bound). All expected
  values above are derived from gate semantics + committed builders, not observed.
- A-1 unresolved: if L1 adopts the raw-set reading, impl's duplicated counter is an
  under-report on FX-5-class inputs and the v2 `expected_raw_unallowlisted` encoding
  is wrong; if partition-copy, the "distinct" reporting clause is cosmetic.
- Receipt stderr/argv strictness (A-4/A-6) decides whether real historical receipts with
  extra wrapper fields remain evaluable.
- Tooling: no installs performed or needed (read-only seat; pacman paused anyway).
