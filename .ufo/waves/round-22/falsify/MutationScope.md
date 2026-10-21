# MutationScope — nonexecuted mutation designs

## Scope and evidence

Axes: smallest behavior-bearing mutation; independent finite-oracle sensitivity; corrected population identity; no production/evidence changes.

Read the effective correction first, then the entire retained contract, the v2 requirement manifest, the current shipping source, and the v2 oracle/fixture source. The correction supersedes the retained contract's source-file subtraction: exclusion is by independently matched `non_author_paths_glob`, the supplied policy file remains scanned normally, and accounting agreement never grants privacy clearance.

Source anchors observed in this review:

- Shipping source: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-retention-reconcile.py`, read snapshot `B5AF`, lines 203–228 and 119–126.
- Effective correction: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-22/denominator-correction.md`, lines 5–11.
- Requirement manifest: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-22/frozen/requirements-v2.json`, snapshot `8F86`.
- Detector: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-22/oracle-reconcile-v2.py`, snapshot `6BDE`, lines 40–61.
- Fixtures: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-22/frozen/fixture-builder-v2.py`, snapshot `74BD`, lines 38–75, 79–87, and 103–108.

All three edits below are **designs only**, each applied independently to the same pristine source in any subsequently authorized isolated probe. No edit was applied. No SUT, oracle, selftest, fixture builder, test, build, formatter, or other runtime was invoked. No original evidence was changed. Predictions are marked `[INFERENCE]`; they are not observed kills or passing-baseline claims.

## M1 — replace receipt identity equality with count equality

**Target:** shipping source line 213, inside the loop over `hits`, `allowlisted_hits`, and `unallowlisted_hits`.

Replace exactly:

```python
        if claimed[field]!=Counter(hit_key(h) for h in actual): differences.append(field)
```

with:

```python
        if sum(claimed[field].values())!=len(actual): differences.append(field)
```

This one-line defect preserves list/type/duplicate validation but discards `(path, line, class, line_sha256)` identity when deciding agreement. Summing Counter values deliberately compares population cardinality, not distinct-key cardinality.

**Expected affected requirements:** R07 altered digest, R08 altered line, R09 altered class. The oracle registers these three variants at line 51 and requires exit 1 plus `RETENTION_RECONCILIATION_MISMATCH` with empty stderr. The fixture changes only one field of the first raw receipt hit, without changing any list cardinality (fixture lines 81–83). Those altered values remain syntactically valid under `normalize_hits`.

**[INFERENCE] Expected distinguishing output:** each of those variants instead returns exit 0, `finding_id=RETENTION_RECONCILED`, `receipt_match=true`, and `differences=[]`. The other receipt lists, counters, finding, and recorded exit still agree with recomputation, so they do not supply a second mismatch. Each of R07/R08/R09 must therefore fail under the frozen oracle.

**[INFERENCE] Controls:** R05 dropped hit and R06 injected hit still change cardinality and remain mismatches; R10 still fails its metric comparison. R04 alone does not detect this defect: the returned scanner identities are independently recomputed and unchanged. Thus the same-cardinality receipt mutations, not count subtraction or output-list inspection alone, are the required killers.

**Actual output / verdict:** none; **INCONCLUSIVE — not executed**, not an observed killed or surviving mutant.

## M2 — grant privacy clearance on reconciliation output

**Target:** shipping source line 225, the `check` result dictionary only.

Replace exactly:

```python
            'privacy_clearance':False,'input_revision':revision,'measured_revision':measured,
```

with:

```python
            'privacy_clearance':True,'input_revision':revision,'measured_revision':measured,
```

Do not modify the separate selftest summary or setup-error dictionaries. This isolates the production result's false-to-true regression rather than making an unrelated global replacement.

**Expected affected requirements:**

- R02: valid retained-red fixture explicitly requires `privacy_clearance is False` (oracle line 48).
- R11: forbidden-allowlist fixture independently requires the same false value (line 52).
- R23: valid-fixture output safety predicate also requires it (line 60).

**[INFERENCE] Expected distinguishing output:** valid and forbidden-fixture results still return exit 0 and `RETENTION_RECONCILED`, with their red retention state and recomputed counts unchanged, but now emit `privacy_clearance=true`. R02/R11/R23 must fail specifically on that boolean. R01's status/finding-only check would not kill this mutant by itself.

This challenges the explicit invariant that exact accounting, including agreement about retained findings, is not privacy clearance. No clean-count assumption is needed for detection.

**Actual output / verdict:** none; **INCONCLUSIVE — not executed**, not an observed killed or surviving mutant.

## M3 — replace non-author exclusion with exact policy-source exclusion

**Target:** shipping source line 203. Keep both subsequent list comprehensions unchanged so one predicate substitution controls both partitions.

Replace exactly:

```python
    is_non_author=lambda h:any(fnmatch.fnmatch(h['path'],pattern) for pattern in patterns)
```

with:

```python
    is_non_author=lambda h:h['path']==paths['policy']
```

This deliberately restores the rejected source-file interpretation at one behavior-bearing point. It excludes only the exact supplied policy path, not identical blobs or arbitrary nested copies.

**Expected affected requirement:** corrected R04, whose oracle compares complete scanner hit dictionaries against the fixture's independent expected scanner identities and separately compares excluded identities (oracle line 50; fixture lines 107–108). R12's existing non-author semantics are also implicated; R03's scalar triple alone is insufficient.

**[INFERENCE] Expected distinguishing output on the valid fixture:**

- The scalar triple remains `raw_total=5`, `policy_excluded=1`, `scanner_total=4`: the fixture has one policy-source hit and a different one-hit non-author path.
- `policy_excluded_hits` contains the policy-source identity instead of the non-author identity.
- `scanner_hits` wrongly omits the policy-source identity and includes the non-author identity. R04's identity predicate is false despite unchanged cardinalities.
- The policy-source identity is allowlisted; the newly included non-author identity is not. Consequently `raw_unallowlisted` and `scanner_unallowlisted` become 2 instead of 1.
- The exact comparison logic then produces `differences=["unallowlisted_hits","metric"]`, exit 1, `finding_id=RETENTION_RECONCILIATION_MISMATCH`, and `receipt_match=false`.

The frozen valid-fixture records all require exit 0 and `RETENTION_RECONCILED`, so those records also reject this result. In particular, the **complete R03 record fails its common status/finding precondition**, even though its `(5,1,4)` predicate remains true. This distinction prevents incorrectly claiming that a scalar-only detector establishes population agreement. R04 remains the direct identity-specific detector required by the correction.

**Actual output / verdict:** none; **INCONCLUSIVE — not executed**, not an observed killed or surviving mutant.

## Restoration and observation limits

Only this assigned report was written. No scratch fixture or mutated source file was created, no production edit occurred, and no restoration was necessary. The observed shipping read snapshot was `B5AF`; that tool snapshot identifier is **not** a SHA-256 digest. Before/mutated/restored SHA-256 values were not measured, and there are no baseline/mutant/restored detector outputs or exit statuses to report. None are invented or borrowed from earlier build-wave notes.

Empirical kill claims require a separately authorized pristine/mutated/restored run of the same frozen v2 detector against exact independently preserved bytes; a failing pristine baseline would be inconclusive. This report supplies the exact candidate edits and fail-capable requirement bindings, not a substitute for that measurement.

Tool installations/updates: none. Production changes, source remediation, delegation, background jobs, VCS mutations, and session reads: none.
