# AttackR11 — frozen R11 "forbidden allowlist cannot become clean"

Seat: `MoriR22.AttackR11` (reviewer). Static review only: no tests, builds, linters, selftests, or tool executions were run. The only computation performed was `sha256` of the constant synthetic line literals below (pure arithmetic on stated bytes, not a measurement). Sources read: `contract.md`, `tools/mori-retention-gate.py`, `tools/mori-retention-reconcile.py`, `.ufo/waves/round-22/frozen/fixture-builder-v2.py`, `.ufo/waves/round-22/frozen/fixture-builder.py`, `.ufo/waves/round-22/oracle-reconcile.py`, `.ufo/waves/round-22/oracle-reconcile-v2.py`, `.ufo/waves/round-22/frozen/expected-real.json`, `.ufo/waves/round-21/evidence/final/retention-floor.json` (field names and types only; no matched text), and sibling build reports (`GateAllow.md`, `CriticAdmission.md`, `CriticPopulation.md`, `PolicySemantics.md`, `AttackR18.md`).

## 1. Requirement as frozen

`contract.md:19`: **"R11 forbidden allowlist cannot become clean"**. Supporting contract text: "Validate lists/counts/finding_id and receipt exit against independent recomputation" (`:13`); "raw partitions reproduce existing … allowlist semantics, including forbidden must_redact entries" (`:13`); "Exit1 RETENTION_RECONCILIATION_MISMATCH: valid receipt disagrees with recomputation" (`:15`); "explicit … forbidden_allowlist … retention_state, privacy_clearance=false" (`:13`); "A matched receipt is not clean retention" (`:7`).

## 2. Gate semantics R11 must pin (evidence)

In `tools/mori-retention-gate.py`:

- **Forbidden classification precedes hit matching** (L239-258): `row['path'] in must_paths` → `allowlist_forbidden` row `{finding_id, path, line: None, class, line_sha256}`. It is forbidden even when the key matches **no** hit, never stale, and **never** added to `allowed_keys` (the `elif` at L249).
- **Non-suppression**: because the forbidden row never enters `allowed_keys`, hits at the must-redact path stay in `unallowlisted_hits` and count in `metric` and `routed` (L260-268). A forbidden allowlist cannot even allow *other* rows' hits at its own path.
- **Finding precedence** (L280-288): `allowlist_forbidden` > `RETENTION_FINDINGS` > `allowlist_stale` > `RETENTION_CLEAN`; exit 1 iff `metric or forbidden_rows or population_match is False`. A forbidden row forces exit 1 and `allowlist_forbidden` **even with metric 0, and masks non-zero metric**.
- Exit-0 results exist in two flavors: `RETENTION_CLEAN` (no stale) and `allowlist_stale` (advisory). "Clean" in R11 therefore spans both flavors: any receipt-side state softer than `allowlist_forbidden` when recomputation says forbidden.

## 3. What the committed artifact set actually does for R11

**Candidate impl** `tools/mori-retention-reconcile.py` — traced, not executed:

- L198-202: recomputes `forbidden` before hit-match, never inserts into `allowed_keys`; `unallowed` at L207 keeps must-path hits. `retention_code=int(bool(unallowed or forbidden))` (L209); precedence at L210 reproduces the gate's order. Receipt `forbidden_allowlist`/`warnings` are shape-validated via `auxiliary` (L128-136, L190-191: exact key set `{path,line,class,line_sha256,finding_id}`, per-row `finding_id` literal, `line is None`, no duplicate keys) and compared as Counters at L216-217; `finding_id` and wrapper `exit_code` compared at L215, 218. `retention_state` is derived from recomputation (L224), and 'clean-at-frozen-regex-scope' is emitted only when recomputed `unallowed` and `forbidden` are both empty. On the R11 surface, the candidate's logic is consistent with the gate as of this snapshot.

**Committed oracle** (`oracle-reconcile.py:52`, identical in `oracle-reconcile-v2.py:52`):

```python
record('R11','forbidden',predicate=lambda v,f:v['forbidden_allowlist']==1
   and v['raw_unallowlisted']==3 and v['retention_state']=='red'
   and v['privacy_clearance'] is False)
```

against the `forbidden` variant of `fixture-builder-v2.py` (L44-46, 68-71): `must_redact_paths=['allowed.txt']`, one forbidden row (2 hits at `allowed.txt` move into `unallowlisted_hits`), honest receipt `finding_id=allowlist_forbidden`, `metric=3`, `routed=2`, `exit_code=1`. `record()` defaults `code=0`, `finding='RETENTION_RECONCILED'`.

**Coverage verdict: R11 is honest-only.** The builder never mutates `forbidden_allowlist`, `warnings`, `finding_id`, `exit_code`, `allowlisted_hits` or `unallowlisted_hits` (confirmed by `CriticAdmission.md:17` and `CriticPopulation.md:77`). No arm forces the SUT to compare any receipt-side classification field. The predicate reads only the SUT's *own recomputed* counters, all derivable from hits + allowlist + policy.

## 4. The counterexample (superficial SUT + laundering receipts the committed oracle cannot catch)

### 4.1 Superficial SUT S*

S* is otherwise correct and passes **all 24 committed arms**: it compares `hits`, `metric`, `routed`, `non_author`, `allowlisted_hits`, `unallowlisted_hits` against recomputation, validates types, and recomputes `retention_state` honestly — **but never compares** `forbidden_allowlist`, `warnings`, `finding_id`, or the wrapper `exit_code`. (A weaker mutant skipping partition lists also survives every arm, per `CriticPopulation.md:76`; S* is the strongest laundering-capable member of the surviving family.)

S* behavior under the honest `forbidden` fixture: all checked fields agree → exit 0, `RETENTION_RECONCILED`, `forbidden_allowlist=1`, `raw_unallowlisted=3`, `retention_state='red'` → **committed R11 arm passes**.

### 4.2 Fixture F11 — R11 laundering arms

Base = `fixture-builder-v2.py` `variant='forbidden'` exactly. Measured-tree contents and derived expectations (digest values computed arithmetically over the stated literal bytes):

| File | Content | Hits |
|---|---|---|
| `policy.json` | schema `mori-retention-policy-v1`, one class `{id:"R22", regex:"[R]22_SAMPLE"}`, `must_redact_paths:["allowed.txt"]`, `non_author_paths_glob:["non-author.txt"]`, `synthetic:"R22_SAMPLE"` | 1 (`policy.json`, its `synthetic` key line; class R22; sha256 = that serialized line's digest, fixture-derived) |
| `allowed.txt` | `R22_SAMPLE allowed\nR22_SAMPLE allowed\n` | 2 (lines 1-2, `line_sha256=32439be8…87308`) |
| `unallowed.txt` | `R22_SAMPLE retained-red\n` | 1 (`f748b07e…25aff`) |
| `non-author.txt` | `R22_SAMPLE outside-author\n` | 1 (`b53ec2f9…d5c68`, non-author) |
| `binary.bin` | `R22_SAMPLE\x00must-not-count` | 0 (NUL → skipped) |

`allowlist.json` rows = gate-shaped `{path,class,line_sha256,reason,rule:'b'}` for `policy.json` and `allowed.txt`. Recomputed truth at the measured revision: `raw_total=5`, `policy_excluded=1` (non-author basis), `scanner_total=4`, `non_author=1`, `forbidden_allowlist=1` row `(allowed.txt,R22,32439be8…)`, `allowed` = {policy hit}, `unallowed` = {unallowed.txt:1, allowed.txt:1, allowed.txt:2}, `metric=3`, `routed=2`, recomputed `finding_id=allowlist_forbidden`, recomputed `exit_code=1`.

All arms below keep `hits`, `allowlisted_hits`, `unallowlisted_hits`, `metric`, `routed`, `non_author`, `commit`, `policy_sha256` **byte-identical to the honest receipt** so the only divergence is the laundering field set. Required expectations assume contract semantics; each is one isolated CLI subprocess arm.

| Arm | Receipt stdout mutation | S* result | Required |
|---|---|---|---|
| **F11a** (control) | honest `forbidden` receipt as built | 0, RECONCILED | **0**, `RETENTION_RECONCILED`, `receipt_match:true`, `forbidden_allowlist:1`, `raw_unallowlisted:3`, `scanner_unallowlisted:3`, `non_author:1`, `retention_state:"red"`, `privacy_clearance:false` |
| **F11b** (coherent stale-laundering) | `forbidden_allowlist:[]`; `warnings:[{finding_id:"allowlist_stale",path:"allowed.txt",line:null,class:"R22",line_sha256:"32439be8…"}]`; `finding_id:"RETENTION_FINDINGS"`; wrapper `exit_code:1` | **0, RECONCILED** | **1**, `RETENTION_RECONCILIATION_MISMATCH`, `receipt_match:false`; emitted counters identical to F11a (`forbidden_allowlist:1`) |
| **F11c** (explicit clean claim) | `forbidden_allowlist:[]`; `warnings` unchanged `[]`; `finding_id:"RETENTION_CLEAN"`; wrapper `exit_code:0` | **0, RECONCILED** — a receipt asserting gate exit 0 + CLEAN is certified | **1**, MISMATCH, `receipt_match:false`, `retention_state:"red"` |
| **F11d** (row-drop laundering) | `forbidden_allowlist:[]`; `finding_id:"RETENTION_FINDINGS"`; `exit_code:1`; warnings `[]` | **0, RECONCILED** | **1**, MISMATCH |
| **F11e** (schema edge, borderline) | delete key `forbidden_allowlist` entirely | 0 or 2 | **2**, `RETENTION_RECONCILIATION_SETUP` — a required receipt field absent is a fail-closed schema inconsistency, not a disagreement (see §6-2; freeze this) |
| **F11f** (precedence, optional) | F11b plus `warnings` also carrying a genuinely stale row; `finding_id:"RETENTION_FINDINGS"`, `exit_code:1` | 0 | **1**, MISMATCH — forbidden must outrank findings+stale on recomputation |

F11b is the strongest arm: the forged receipt is **internally gate-coherent** — `warnings` + `metric>0` + `RETENTION_FINDINGS` + `exit_code 1` is a state the gate actually emits — so no self-consistency check catches it. Only recomputing `forbidden` from `must_redact_paths` does. It launders "a must-redact allowlist entry" into "an advisory stale row" inside a still-red receipt, the minimal R11 violation: the forbidden row never appears anywhere.

### 4.3 Fixture F11g — classification-order arm (new fixture variant needed)

A SUT that classifies "stale before must-path" (`elif` order swapped) passes the committed R11 arm **only because** the fixture's forbidden row matches real hits — wait, no: swapping order still yields forbidden at line 2? Recheck: if the SUT checks `key in hit_allow_keys` first and the forbidden row's key *does* match a hit (it does here), a "match→allowed" SUT adds it to `allowed_keys` — that collapses `metric`/`unallowed` and is caught by the honest arm's `raw_unallowlisted==3` predicate. The order defect that survives is "stale-first" classification, which diverges only when the forbidden row matches **no hit**. F11g: change `allowed.txt`'s content so its lines no longer match the row's `line_sha256` (or point the row at a different digest), keeping `must_redact_paths=['allowed.txt']`. Recomputed: `forbidden=1` row, `allowed`={policy}, `unallowed`={unallowed.txt + 2 allowed.txt hits}, `metric=3`, `routed=2`, `finding_id=allowlist_forbidden`, `exit_code=1`. A stale-first SUT recomputes `forbidden_allowlist=0` and emits `allowlist_stale` as the finding — it would still emit `retention_state='red'` and can pass an output-only predicate if the predicate forgot `forbidden_allowlist==1`; keep that assertion so this arm kills it at recomputation level too. A "forbidden only when row matches hit" SUT emits the same wrong recomputation. **Required: exit 0, `forbidden_allowlist==1`, `retention_state='red'`, recomputed-finding `allowlist_forbidden`.**

## 5. Exact actionable criterion (oracle + selftest)

1. Keep the F11a honest arm and strengthen it: assert `receipt_match is True` and `finding_id=="RETENTION_RECONCILED"` (the current predicate asserts neither; an arm that returns MISMATCH for the wrong reason could still satisfy the counter predicates if the SUT's own recomputation is honest).
2. **R11 = F11b + F11c + F11d as mandatory isolated CLI arms**, each expecting exit `1`, `finding_id=="RETENTION_RECONCILIATION_MISMATCH"`, `receipt_match is False`, `privacy_clearance is False`, and recomputed counters equal to F11a (`forbidden_allowlist==1`, `raw_unallowlisted==3`, `retention_state=="red"`). Where the SUT emits a `differences` list, F11b must include `'forbidden_allowlist'`, `'warnings'`, and `'finding_id'`; F11c must include `'forbidden_allowlist'`, `'finding_id'`, `'exit_code'`; F11d must include `'forbidden_allowlist'`.
3. F11e is mandatory once §6-2 is frozen: exit `2`, `RETENTION_RECONCILIATION_SETUP`, sanitized error token, no counter fields required, `receipt_match is not True`.
4. F11g as a fixture-builder variant with the honest-receipt expectations in §4.3.
5. **Recomputation-side obligations the oracle must pin as output assertions** (so "cannot become clean" is anchored in the emitted record, not just in receipt rejection): whenever recomputed `forbidden` is non-empty, the SUT must emit `forbidden_allowlist >= 1`, `retention_state` ∈ red-designating values (never the clean token — pin the vocabulary, see §6-1), and `privacy_clearance is False`. `retention_state` must be derived from the recomputed partitions, never echoed from receipt `finding_id`/`exit_code`.
6. **Receipt-side obligations**: the SUT must compare, as multisets keyed by `(path,class,line_sha256)`, receipt `forbidden_allowlist` rows (each `{finding_id:"allowlist_forbidden",path,line:null,class,line_sha256}`) and `warnings` rows (`allowlist_stale`) against recomputation; must compare receipt `finding_id` against the recomputed precedence `allowlist_forbidden > RETENTION_FINDINGS > allowlist_stale > RETENTION_CLEAN`; and must compare wrapper `exit_code` against `int(bool(unallowed or forbidden))`. Any disagreement on a well-typed receipt → exit 1. Any type/shape violation (row `line` non-null, wrong per-row `finding_id`, duplicate `(path,class,sha)` keys, extra/missing keys, missing `forbidden_allowlist`/`warnings` list) → exit 2, and exit 2 is checked **before** comparisons (type precedence, per AttackR18 §48-49).
7. Fixture-integrity assertions for each laundering arm: the mutant receipt differs from the honest receipt in exactly the declared field set; `hits`/`unallowlisted_hits`/`allowlisted_hits`/`metric`/`routed`/`non_author` are byte-identical to F11a. Otherwise a nonzero exit can come from an unrelated divergence and the arm proves nothing about R11.
8. Do not extend R11 to demand exit ≥1 on F11a. The honest forbidden receipt must reconcile at exit 0; the contract explicitly tolerates `retention_state=red` under `RETENTION_RECONCILED` (§6-1).

## 6. Semantic ambiguities (with smallest safe resolutions)

1. **"Clean" is undefined in the reconcile output vocabulary.** The receipt uses gate ids (`RETENTION_CLEAN`, `allowlist_stale`, `RETENTION_FINDINGS`, `allowlist_forbidden`); the tool emits `RETENTION_RECONCILED`/`MISMATCH`/`SETUP` plus an unenumerated `retention_state` (the candidate invents `clean-at-frozen-regex-scope`). Two defensible readings:
   - (a) *Receipt-cleanliness*: a receipt whose claimed state is cleaner than recomputed (CLEAN or stale where recomputation says forbidden) disagrees → exit 1. Reconciliation exit is untouched.
   - (b) *Output-cleanliness*: the tool must never label a forbidden run clean — `retention_state` red-designating + `forbidden_allowlist>0` whenever recomputed forbidden is non-empty.
   Reading (a) alone lets S* launder; (b) alone lets a validator-blind S* pass. **Resolution: R11 is (a)∧(b).** Reading "R11 ⇒ reconcile exits nonzero on the honest arm" is wrong: `:15` says exit 0 means "exact accounting agreement (even retention_state=red)"; demanding nonzero breaks R01/R02 and the entire red-receipt use case. Freeze this.
2. **Missing vs empty `forbidden_allowlist`/`warnings` keys.** Absent required keys: schema inconsistency (exit 2, fail-closed) or value disagreement (exit 1)? Contract "required field/type/schema inconsistencies must fail closed" supports 2; a receipts-as-data reading supports 1. Currently unfrozen → a SUT emitting either is unjudgeable. **Recommend exit 2** (absent required fields are malformed receipts), frozen by F11e.
3. **Wrapper `exit_code` domain.** The candidate accepts only {0,1} (L168). A receipt honestly wrapping a gate *setup* run (`exit_code:2`, stderr free text) is well-formed JSON: is it exit-2 (unsupported) or exit-1 (disagreement)? **Recommend 1** — it is a well-typed claim that disagrees with recomputation — but either way it must be frozen; today it is silent.
4. **Forged-row shape precedence.** A receipt `forbidden_allowlist` row with `line:5` instead of `null`: type defect (2), never a value disagreement (1). Already implied by fail-closed, worth one conjunctive assertion on an existing arm rather than a new R-id (AttackR18 R18g already flags the `line:null→false` cousin).
5. **`retention_state` vocabulary is unbounded.** "red"/"clean-at-frozen-regex-scope" are candidate-invented. R11 cannot distinguish a real red label from a laundered one unless the vocabulary is pinned. **Freeze**: `retention_state` = `"red"` iff recomputed `unallowed` or `forbidden` non-empty, else `"clean-at-frozen-regex-scope"`; oracle asserts exact membership. Adjacent stale-only question: gate exit 0 with stale rows — does `retention_state` stay "clean-at-…"? Recommend yes (stale is advisory per contract) but pin it.
6. **No-hit forbidden row is uncovered gate semantics** (`GateAllow.md:70` lists "forbidden row matching no hit" and "forbidden + stale" as uncovered gate-selftest combinations). Nothing in the r22 fixture forces `must` check before hit-match; only F11g does.
7. **Contract/v2 basis drift (adjacent, not R11):** contract `:13` still says "exactly the supplied policy path" while `requirements-v2.json` supersedes to `non_author_paths_glob` (`exclusion_basis` in expected-real.json and impl L221). The R11 fixture uses the glob on `non-author.txt`; harmless here, but the contract line and the frozen v2 set disagree and someone must own that reconciliation note.

## 7. Superficial-pass risks (enumeration)

- **Honest-only arm**: committed state — no receipt-side mutation ever reaches the forbidden/warnings/finding/exit fields, so field-ignoring SUTs pass 24/24.
- **Predicate asserts only emitted counters** (`forbidden_allowlist==1`): true by recomputation alone; says nothing about receipt validation.
- **`retention_state` hard-coded `"red"`**: survives — every committed fixture is red; no arm reaches the clean token branch (`CriticAdmission.md:98`). F11c plus vocabulary pinning §6-5 is the cheap guard; a genuinely-clean fixture arm would be the real one (out of R11's scope but noted).
- **Receipts treated as provenance only** ("SUT-S3" of `CriticAdmission.md`): recomputes everything, compares nothing — passes all arms while certifying any forged clean receipt.
- **Multiset vs set collapse** on `forbidden_allowlist`: duplicate keys are already a shape rejection (2), so Counter vs set is safe *only if* duplicates are rejected first — pin the order (validate, then compare).
- **Exit-2-or-1 confusion on F11e**: an oracle asserting "nonzero" or `!=0` accepts either and pins nothing; assert the exact code.
- **Selftest provenance**: the candidate's `--selftest` (L233-257) exercises only valid/unsafe-path/unknown-flag arms — zero R11 coverage; do not let "selftest pass" be cited for R11.
- **`v1` builder carry-over**: `fixture-builder.py:68` emits forbidden rows retaining `rule` (6 keys), which a gate-faithful shape validator rejects with exit 2 — R11 unpassable on v1 artifacts; only the v2 builder is usable for R11.

## 8. Residual risk and verification gaps

- The committed impl's R11 logic is correct by code reading, but **no executed evidence exists**; this is a static review. L1 runs the oracle at integration.
- F11b/c/d were not run against the candidate (forbidden by wave rules); expectations are derived from the contract and gate semantics, not observed output.
- `expected-real.json` asserts `forbidden_allowlist:0` on the real r21 receipt — the real corpus never exercises the forbidden path; R11 lives or dies entirely on the synthetic arms.
- The laundering surface is exactly the three fields R11 exists for; if L1 accepts the oracle unchanged, a field-ignoring SUT is admissible and the capability claim overstates agreement guarantees (calibration axis — this round's claim).

## Installs

None.