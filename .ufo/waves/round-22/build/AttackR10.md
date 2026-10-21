# AttackR10 — frozen requirement R10: "metric lie returns1"

Seat: MoriR22.AttackR10 (reviewer, leaf). Static review only; no tests/builds executed.
Reviewed: contract.md (df880b4), denominator-correction.md (e2f549b), frozen/fixture-builder-v2.py,
frozen/oracle-reconcile-v2.py, refinement-reconcile.py, tools/mori-retention-reconcile.py (8cb4afb),
tools/mori-retention-gate.py (receipt schema authority), real receipt
.ufo/waves/round-21/evidence/final/retention-floor.json.

## 1. What R10 currently exercises

- Oracle (`oracle-reconcile-v2.py:51`): `record('R10','metric',1,'RETENTION_RECONCILIATION_MISMATCH')`
  with **no predicate** — asserts only exit=1, finding_id, `stderr==''`.
- Builder (`fixture-builder-v2.py:84`): `elif variant=='metric': result['metric']=0`.
  Truthful `metric` is 1 (one unallowlisted hit, `unallowed.txt`). The lie flips 1→0.
- SUT (`mori-retention-reconcile.py`): type-gate at `:177`
  `for field in ('metric','routed','non_author'): require(integer(receipt.get(field)),'receipt_counter_type')`
  where `integer()` is `type(value) is int and value>=0`; value-compare at `:203`
  `receipt['metric'] != len(unallowed)` → appends `'metric'` to `differences` → exit `int(bool(differences))`=1.
- Verdict on the frozen arm: current SUT passes R10 and emits `differences==['metric']`,
  `receipt_match==false` — strictly stronger than the oracle asserts.

## 2. Concrete counterexample fixtures (builder deltas, all on `variant='metric'` base)

Each is a one-line mutation of `result` inside `wrapper['stdout']` before re-serialization,
committed exactly as the existing 'metric' arm (receipt blob at `--rev`, policy/allowlist
byte-identical at measured and input revisions).

| # | Fixture mutation | Honest expected result | Weak-impl that superficially passes R10 |
|---|---|---|---|
| CX1 | `metric=-1` | exit **2**, `RETENTION_RECONCILIATION_SETUP` | value-only compare (`receipt['metric']!=len(u)`) → exit 1, and passes R10 while failing closed-schema contract |
| CX2 | `metric=1.0` | exit **2**, SETUP | Python `1.0==1` → comparison-equal → exit 0 **and R10 still green** (arm untouched); also `True==1` bool bypass if `isinstance(x,int)` used without bool exclusion |
| CX3 | `del result['metric']` | exit **2**, SETUP | `receipt.get('metric')!=1` (`None!=1`) → exit 1 MISMATCH; absent-field conflated with lie |
| CX4 | `non_author=99` (metric untouched) | exit **1**, MISMATCH | tool that verifies only the literal `metric` field → exit 0; R10 green while a counter lie reconciles |
| CX5 | `wrapper['exit_code']=0` (metric truthful) | exit **1**, MISMATCH | exit_code is the same "metric lie" class (claims red run exited clean); no frozen arm covers it |
| CX6 | `finding_id='RETENTION_CLEAN'` (metric truthful) | exit **1**, MISMATCH | string-valued lie; verifies counter class must include finding_id |
| CX7 | on `clean-control` fixture (refinement builds it): `metric=2` | exit **1**, MISMATCH, and tool's own counters stay `raw_unallowlisted=0`/`metric=0` | asymmetric impl (`mismatch iff claimed<actual` — i.e. "receipt under-counts is a lie, over-counts is fine") exits 0 on CX7 yet passes frozen R10 which only mutates 1→0 |
| CX8 | `metric=5` (upward lie on red fixture) | exit **1**, MISMATCH | same asymmetric-check hole as CX7, opposite direction |
| CX9 | on `forbidden` fixture: `routed=0` (truth 2) | exit **1**, MISMATCH | `routed` is only nonzero under must_redact; R10's red-only arm never exercises a nonzero `routed` recompute |
| CX10 | duplicate JSON key `"metric":0,"metric":1` in stdout | exit **2**, SETUP (current SUT via `no_duplicates` object_pairs_hook) | stdlib `json.loads` takes last-wins → metric compares equal → exit 0; "valid receipt" superficially reconciles a contradictory document |

All CX expectations trace to contract.md:15 (exit2 for "invalid types/schema", fail-closed on
required fields) and exit1 for "valid receipt disagrees with recomputation".

## 3. Semantic ambiguities in the R10 wording

A1. **Lie/type boundary unspecified.** "metric lie returns1" does not state that a
    type-invalid (bool/float/string/null), negative, or absent `metric` is a setup
    failure (exit2), not a mismatch. SUT's reading (type-gate → 2, integer-value
    mismatch → 1) is the defensible one but is one of at least three reasonable
    readings; CX1–CX3 pin it down.
A2. **"metric" denotation unspecified.** Singular field vs. the whole scalar-claim
    class (`metric`, `routed`, `non_author`, `exit_code`, `finding_id`). SUT already
    checks all five (lines 177, 203–207); the requirement as worded lets an
    implementer check `metric` alone (CX4–CX6 pass unnoticed).
A3. **Metric ground truth.** `metric` must be pinned as
    `|{h ∈ raw_hits : path(h) ∉ non_author_paths_glob matches ∧ (path,class,line_sha256) ∉ effective_allowlist_keys}|`
    — i.e. recomputed from the corrected (v2) non-author partition plus
    must_redact-aware allowlist evaluation, matching gate `_scan_result` semantics.
    Without this, the corrected denominator scope (denominator-correction.md) leaves
    room for a tool that recomputes metric over a different universe and reconciles
    the wrong number.
A4. **Receipt-external counters unaddressed.** R10 says nothing about stdout-level
    provenance lies that keep counters equal (e.g. `stderr` non-empty, population_*
    keys injected). SUT already rejects both (lines 169, 183); requirement text
    should note they belong to setup/other axes, not R10, so reviewers don't
    double-count.
A5. **Directionality.** "lie" covers both under- and over-reporting; the single
    1→0 mutation only proves one direction (CX7/CX8 hole).

## 4. Superficial-pass risks (ranked)

R1 (highest): **Exit/finding-only arm.** Oracle asserts no `receipt_match is False`,
    no `differences` content, and emits no predicate. A tool that exits 1 on *any*
    receipt anomaly in this fixture (e.g. crash-mapped-to-1, or flagging a different
    field) passes R10 without having recomputed `metric` at all.
R2: **Value-equality metric check without type gate.** Passes R10 + accepts
    `metric=1.0`/`True` on a clean receipt (CX2) — a reconciled lie-in-type. The
    bool-metric arm exists but is folded conjunctively into R18 and would only fail
    R18, leaving R10 green — misleading per-requirement attribution.
R3: **metric-only scope.** Passes R10 while `routed`/`non_author`/`exit_code`/
    `finding_id` lies reconcile clean (CX4–CX6).
R4: **Asymmetric or one-direction check.** `claimed<actual`-only impls pass R10,
    fail CX7/CX8.
R5: **Last-wins JSON duplicate keys** (CX10) — reconciles a self-contradictory
    receipt; only caught if parsing rejects duplicate keys.
R6 (residual, out of R10 scope but adjacent): SUT lacks the refinement's expected
    `receipt_path_binding` rejection (`refinement-reconcile.py:16-17,32-33`) —
    `--allowlist copy-allowlist.json` identical-bytes substitution currently exits 0
    under the SUT but the refinement case demands 2. Flagging because a metric
    recomputation against a byte-equal-but-path-different allowlist is exactly the
    class of input-tree mismatch the contract wants unevaluable.
## 5. Exact actionable criterion for R10

Replace the bare `record('R10','metric',1,'RETENTION_RECONCILIATION_MISMATCH')` with
a predicate and split the type-side into the setup class:

```
record('R10','metric',1,'RETENTION_RECONCILIATION_MISMATCH',
    predicate=lambda v,f:
        v.get('receipt_match') is False
        and type(v.get('metric')) is int and v['metric']==1                              # tool emits its own truthful counter
        and v.get('raw_unallowlisted')==1 and v.get('scanner_unallowlisted')==1    # tool's own truth unaffected by the lie
        and set(v.get('differences',['metric']))=={'metric'}                       # sole divergence is metric when reported
)
```

Mandatory companion arms (minimal closure set):
- `metric-neg` (CX1), `metric-float` (CX2), `metric-absent` (CX3) → exit2/SETUP,
  conjuncted into R18 or a new R10b; asserts the lie/type boundary at A1.
- `non_author`/`routed`/`exit_code`/`finding_id` mutations (CX4–CX6, CX9) → exit1,
  proving R10's "metric" means the scalar-claim class, not one field.
- `metric-up` (CX8) and clean-fixture `metric=2` (CX7) → exit1, closing
  directionality; clean-fixture arm additionally asserts
  `raw_unallowlisted==0 and receipt_match is False`.
- Duplicate-`metric`-key receipt (CX10) → exit2, only if duplicate-key rejection is
  kept; otherwise pin last-wins in writing and expect exit0 (decision needed —
  contract is silent; fail-closed is consistent with R17/R19 spirit).

The pass criterion in words: a receipt whose only falsehood is a well-typed integer
`metric` unequal to the independently recomputed unallowlisted count returns exit1
with `finding_id=RETENTION_RECONCILIATION_MISMATCH`, `receipt_match=false`, empty
stderr, and no other field flagged; every non-integer, negative, absent, bool, or
duplicate-keyed metric returns exit2/SETUP instead; lies in `routed`, `non_author`,
`exit_code`, or `finding_id` behave identically to the `metric` lie.

## 6. Verification gaps

- Not run: oracle, refinement, selftest, or any SUT invocation (wave rule). All
  exit/finding claims above are traced statically from
  `mori-retention-reconcile.py:154-216` and the fixture/oracle sources cited.
- CX expectations assume SUT behavior per current committed file (8cb4afb);
  L1 integration may change details — recheck `integer()` ordering (type-gate
  before value-compare at :177 vs :203) after any edit.
- `differences` is a SUT-emitted field, not contract-required; the
  `set(differences)=={'metric'}` clause should be applied only when the field is
  emitted, or promoted into the contract field list if L1 wants it binding.
- No installs performed; no pacman transactions attempted.
