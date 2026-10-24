# AttackR01 — frozen R01 "actual isolated valid receipt returns0/exact finding"

Static review only. No tests, builds, selftests, or tool executions were run; nothing here is a
measurement. No tools were installed (nothing needed; host tooling sufficient). Reviewed against
`tools/mori-retention-reconcile.py` as committed at `8cb4afb` (HEAD moved from `e2f549b` to
`8cb4afb` while this review ran — observed via `git rev-parse`, not re-verified). Sources read:
`tools/mori-retention-gate.py` (existing gate, `7FA9`), `tools/mori-retention-reconcile.py`
(candidate impl, `2642`), `oracle-reconcile{,-v2}.py`, `frozen/fixture-builder{,-v2}.py`,
`frozen/requirements{,-v2}.json`, `frozen/expected-real.json`, `denominator-correction.md`, and
the committed r21 receipt `.ufo/waves/round-21/evidence/final/retention-floor.json` (metadata,
paths, counts, digests only — no matched line contents).

Axes: calibration (the gate R01 calibrates is the *capability* claim), correctness of the frozen
oracle, provenance of "actual" evidence.

## Findings by severity

### F1 — HIGH: two contradictory partition semantics coexist; R01 cannot discriminate either

`contract.md` line 13 still reads: "Policy-excluded means exactly the supplied policy path, never
broad regex/path exclusions." `denominator-correction.md` (committed before the impl) reverses
this: "policy_excluded is exactly the non-author-glob matched identities … The exact supplied
policy file is scanned normally, never excluded by path." `requirements-v2.json` + builder-v2 +
oracle-v2 + `expected-real.json` encode the correction; `requirements.json` + v1 builder +
v1 oracle encode the contract text. **The contract file itself was never annotated as superseded
on this point.** An implementer faithful to `contract.md` alone builds the v1 partition
(`exclusion_basis='supplied_policy_path'` style): it passes R01 (exit 0 + finding_id are identical
under both semantics on the canonical fixture, because raw counters are unchanged — only
`policy_excluded_hits`/`scanner_hits` membership differs) and fails R04 in the v2 oracle.
Conversely the committed impl (partition = `non_author_paths_glob`, `exclusion_basis`
non_author_paths_glob, `mori-retention-reconcile.py:203-205,221`) fails the v1 oracle's R04.
R01's "exact finding" is satisfied by both, so R01 gives false confidence while the authority
conflict is live. Action: annotate `contract.md` that line 13's policy-path sentence is superseded
by `denominator-correction.md` + `requirements-v2.json` (evidence-append-only style: add a
pointer line, do not rewrite history), and retire or tombstone the v1 builder/oracle/requirements
files so only one semantic authority remains loadable.

### F2 — HIGH: the "actual" arm is orphaned; frozen R01 exercises only a fabricated receipt

`frozen/expected-real.json` pins the real receipt precisely: input `77a5bbe…`, measured
`9fb1f911…`, three repo-relative input paths, three input SHA-256s, and an `expected` dict
(RECONCILED, receipt_match, 95/5/90, 4/4, non_author 5, allowlisted 86, forbidden 0, red,
clearance false, `exclusion_basis='non_author_paths_glob'`). Neither oracle consumes it — grep
both files: no `expected-real` reference exists. The only R01 arm measured is the synthetic
`valid` fixture, whose receipt is **fabricated by the builder**, not produced by running the gate
(`fixture-builder-v2.py:71-78` hand-builds `result`/`wrapper`). Preconditions for the real arm are
all verified statically: `9fb1f911` is an ancestor of `77a5bbe` (`merge-base --is-ancestor` → 0);
receipt/policy/allowlist blobs exist at `77a5bbe`; policy+allowlist bytes are identical at
measured vs input revisions (sha256 `db06e981…` / `f46c78ec…` at both); the inner receipt has
exactly the fields the impl requires (commit, policy_sha256, metric, routed, non_author, hits,
unallowlisted_hits, allowlisted_hits, forbidden_allowlist, warnings; no `population_*` keys);
stderr is `""`; stdout is a single JSON document with a trailing newline that `json.loads`
tolerates. So "actual" in R01 is currently satisfied only by construction in the oracle author's
sense, not by the real committed receipt. Action: wire `expected-real.json` into the oracle as an
explicit real arm asserting the `expected` dict verbatim (plus `receipt_match is True`,
`differences` absent/empty, stderr empty); if L1 instead redefines R01's "actual" as the synthetic
fixture, rename the requirement wording so "actual" doesn't claim more than the fixture is.

### F3 — MED: "validate lists/counts/finding_id and receipt exit" is unmeasured — no mutation arm touches auxiliary lists, wrapper exit_code, stderr, or inner commit

The impl validates all of these (`mori-retention-reconcile.py:189-218`: hits/unallowlisted/
allowlisted Counters, metric/routed/non_author/finding_id equality, forbidden/warnings Counters,
`wrapper['exit_code'] != retention_code` at :218), but **no frozen arm mutates any of them**. R05–
R10 mutate only `result['hits']` and `result['metric']`. A comparator that reads only
`hits`+`metric`+`finding_id`+`exit_code` passes all 24 requirements — i.e., the entire
list-validation surface is invisible to the oracle. Concrete counterexample fixture
(`'aux-tamper'` family, built on the `valid` arm):

```python
inner = json.loads(wrapper['stdout']); inner['unallowlisted_hits'] = []
# hits, metric, finding_id, exit_code all still correct → recomputation disagrees only on the list
# Expected: exit 1, finding_id RETENTION_RECONCILIATION_MISMATCH, differences ⊇ ['unallowlisted_hits']
```

Sibling arms worth the same line: `inner['allowlisted_hits'].pop()` → 1; `inner['warnings']`
injected with a stale-shaped row `{finding_id:'allowlist_stale',path,class,line_sha256,line:null}`
→ 1; `wrapper['exit_code']=0` (recomputed 1) → 1 (`'exit-code-lie'`); `inner['commit']` flipped to
the input revision → under the impl this is `receipt_revision_conflict` → 2; freeze that
classification explicitly (see F6.4).

### F4 — MED: "Read … via Git blobs, not worktree" has no discriminating arm

Every fixture path (`--receipt/--policy/--allowlist`) is identical in worktree and tree at fixture
time, so a worktree-reading mutant is indistinguishable. Counterexample `'worktree-shadow'`: after
the receipt commit, overwrite the *worktree* copy of `receipt.json` with the `drop` variant (do not
commit). Expected: unchanged result — exit 0, `RETENTION_RECONCILED`, `receipt_match: true`,
identical counters (the committed blob still reconciles). A worktree reader yields exit 1. Cheap
to add; currently unmeasured.

### F5 — MED: R01's oracle criterion is satisfied by a constant shim

`oracle-reconcile-v2.py:47` — `record('R01')` has no predicate: pass iff
`exit==0 and v['finding_id']=='RETENTION_RECONCILED' and stderr==''`. A tool printing
`{"finding_id":"RETENTION_RECONCILED"}` unconditionally passes R01. Sibling requirements reuse the
same cached invocation and do check counters/lists (R02/R03/R04/R12/R22/R23/R24), so the full
suite catches a shim — but R01 as a *frozen requirement* claims "exact accounting agreement"
(contract line 15), which its own criterion does not assert. It also never asserts
`receipt_match===true`, `differences` absence, or `schema==='mori-retention-reconciliation-v1'` —
an impl can emit `finding_id=RETENTION_RECONCILED` alongside `receipt_match:false` and pass R01.
Exact criterion fix in §C.

### F6 — MED/LOW ambiguities in "valid receipt" and "exact finding" that decide R01 either way

1. **Required inner field set is unspecified.** Contract says the wrapper's `stdout` "contain[s]
   retention JSON" and "required field/type/schema inconsistencies must fail closed" without
   enumerating required inner fields. Impl requires `commit`, `policy_sha256`, `metric`, `routed`,
   `non_author`, `hits`, `unallowlisted_hits`, `allowlisted_hits`, `forbidden_allowlist`,
   `warnings`, `finding_id` (any missing → exit 2). The frozen fixture's fabricated receipt
   contains exactly these — i.e., the fixture defines validity by the impl's assumption, which is
   circular. A receipt from a gate version missing `routed` is exit-2 under the impl, maybe exit-0
   under a looser tool. Pin the required inner field list (recommend: the ten fields above,
   matching gate `_scan_result` output).
2. **`stdout` containment vs document.** "stdout containing retention JSON": impl does
   `parse(wrapper['stdout'])` + `isinstance dict` (strict whole-document, whitespace-tolerant).
   A wrapper that logged a line before the JSON is exit-2 under the impl, exit-0 under a
   substring-parsing tool. Pin: stdout must be a single JSON document modulo insignificant
   whitespace; else SETUP.
3. **`stderr` must be `''`.** Impl requires exactly empty (:169). Contract is silent whether a
   diagnostic-noise receipt is invalid (2) or merely suspect (1). Recommend pinning exit-2/
   `receipt_stderr`.
4. **Triple revision binding.** Impl requires `measured_revision == argv --rev == inner.commit`
   and `inner.commit==measured` (:184-186); contract requires only "measured_revision full commit
   and ancestor of input." The r21 `retention-floor-entering.json` (measured `9fb1f911`, scanned
   `e9f340ce`, same hit multiset — see AttackR03 §3) is a genuine *valid-execution* receipt that
   reconciles vacuously if only ancestry is checked. Impl's strictness is right; pin it in
   contract text (the equal-revisions case is also covered: `merge-base --is-ancestor A A` → 0 is
   accepted, so input==measured is valid — freeze that too).
5. **`argv --repo` must be absolute.** Impl requires `recorded_repo.startswith('/')` (:176).
   A receipt produced with `--repo .` or a relative path is contract-consistent but impl-exit-2.
   Either pin "recorded --repo must be absolute" or accept relative recorded repos; do not leave
   it fixture-implicit (the frozen builder happens to use absolute paths).
6. **Unknown receipt hit class.** `inject`/`class` arms land under MISMATCH-1 in the oracle; a
   schema-strict tool may return SETUP-2 for class ∉ policy classes. Impl treats it as data (exit
   1 — correct for a "valid receipt that lies"). Pin: unknown class/digest-in-range-but-wrong is
   MISMATCH, never SETUP.
7. **Population-bearing receipts.** Impl hard-fails any `population_*`/`new_hits` key
   (`unsupported_population_receipt`, :194). Real gate receipts *can* carry those fields when run
   with `--expect-population`. Exit-2 is defensible ("unsupported") but must be declared — the
   contract doesn't mention population receipts at all.
8. **Auxiliary row shape.** Impl requires aux rows be exactly `HIT_FIELDS|{finding_id}` with
   `line:null` and matching `finding_id` kind (:131-133). Gate emits exactly that; any aux row
   with `line` non-null is exit-2. Pin.
9. **stderr empty on exit 0/1.** Oracle requires `cp.stderr==''` for every arm including R01;
   contract doesn't state it. Pin or drop the assertion.

### F7 — LOW: tree-path decoding divergence class — `strict` vs `replace`, unexercised

Gate scans paths with `path_bytes.decode('utf-8', errors='replace')` (`mori-retention-gate.py:202`);
impl `tree()` uses `errors='strict'` and raises `invalid_tree_path` → exit 2 (:76-77). A measured
tree containing a non-UTF-8 filename yields exit-0 reconciliation under the gate's own semantics
but SETUP under the impl — two defensible answers for a "valid receipt." The real measured tree
has zero non-UTF-8 paths (verified: 7715 blobs, all decode), so the real arm is unaffected today;
any *new* receipt measured on such a tree hits the gap. Fixture: add file `b'bad\xff.txt'`
containing the marker via `git add` (byte-path write), pin expected verdict — recommend exit 0
with `errors='replace'` path keying to match the gate that produced real receipts.

### F8 — LOW: oracle `--output` relativization makes R01 fail for binding reasons, not accounting

`oracle-reconcile{,-v2}.py:19,28`: `fixture_root = out.parent/(out.stem+'-fixtures')`. If
`--output` is relative, `f['repo']` is relative, the fabricated receipt's `argv --repo` is
relative, and the impl exits 2 (`receipt_repo_binding`) on the valid arm — R01 fails against a
correct tool. Fix in the oracle: `out = Path(a.output).resolve()` before `mkdir`. (The impl's
absolute-`--repo` requirement is itself unpinned — see F6.5.)

### F9 — OBS: selftest uses default `/tmp`

`mori-retention-reconcile.py:235` uses `tempfile.TemporaryDirectory()` with no `.scratch`/TMPDIR
enforcement (unlike the gate's selftest, which hard-requires `TMPDIR==<root>/.scratch`). Lane rule
forbids deliberate `/tmp` outputs; this is an executor-invocation concern (set `TMPDIR`), not an
R01 oracle defect, but the selftest's three arms are the contract's "actual isolated CLI
subprocess" clause and share the impl's own schema assumptions — they are not independent
evidence; only the oracle is.

### F10 — OBS: cached invocation and dict-order brittleness

The oracle caches each `(variant, receipt_override)` invocation; R01 asserts a single sample —
nondeterministic tools are invisible. R05's `hits[:-1]` drops the *last* hit (non-author.txt) and
R07–R09 mutate `hits[0]` (the policy self-hit); both selections depend on builder dict-insertion
order — deterministic today, but a reorder of the `files` dict silently changes which population
each mutation arm exercises. Parametrize arms by identity (`path=='non-author.txt'`), not index.

## C — Exact actionable criterion for R01 (proposed freeze text)

**Arms.** R01 passes iff *both* succeed; they are conjunctive, not alternatives:

- **R01a (synthetic):** `check` on the builder-v2 `valid` fixture.
- **R01b (actual):** `check --repo <mori-shokunin> --rev 77a5bbe8a0b41dfbfd2546d024d36e294b814bd0
  --receipt .ufo/waves/round-21/evidence/final/retention-floor.json
  --policy .ufo/waves/round-18/frozen/c1-policy.json
  --allowlist corpus/evidence/retention-allowlist.json`.

**Per-arm pass predicate (all conjuncts required):**

1. `exit_code == 0` and `stderr == ''`.
2. `stdout` parses as exactly one JSON object; `finding_id == 'RETENTION_RECONCILED'`;
   `schema == 'mori-retention-reconciliation-v1'`; `receipt_match is true` (JSON boolean);
   `differences` absent or `[]`; `privacy_clearance is false`; `retention_state == 'red'`.
3. Counter binding — R01a: `(raw_total, policy_excluded, scanner_total, raw_unallowlisted,
   scanner_unallowlisted, non_author, allowlisted, forbidden_allowlist) == (5,1,4,1,1,1,3,0)`;
   R01b: the `expected` dict of `frozen/expected-real.json` verbatim, including
   `exclusion_basis == 'non_author_paths_glob'`.
4. Identity binding — R01a: `sorted(scanner_hits)` equals the fixture's `expected_scanner_hits`
   and `policy_excluded_hits` equals `expected_policy_hits` (fold the current R04 identity check
   into R01a so R01 alone discriminates v1/v2 semantics); R01b: `inputs_sha256` equals the three
   frozen digests in `expected-real.json`, `input_revision == '77a5bbe…'`,
   `measured_revision == '9fb1f911…'`, `tool_sha256` equals sha256 of the invoked tool file,
   `argv` is a list of strings.
5. No matched text anywhere in the output object (already asserted for R23 on the same arm;
   bind it to R01a as well).

**New required arms so R01's agreement claim is measured, not assumed** (specs in F3/F4/F6):
`aux-tamper` → 1/MISMATCH; `exit-code-lie` → 1/MISMATCH; `worktree-shadow` → 0/RECONCILED
unchanged; `stderr-noise` → 2/SETUP `receipt_stderr`; `noisy-stdout` → 2/SETUP `receipt_result`;
`unknown-field` (extra wrapper key) → 0/RECONCILED (asserts the permissive direction the contract
requires); `inner-missing-field` → 2/SETUP; `nonutf8-path` → 0/RECONCILED with `errors='replace'`
path keying (recommended verdict; freeze explicitly either way).

**Oracle mechanics:** consume `expected-real.json` for R01b; `out = Path(a.output).resolve()`
before fixture_root derivation; parametrize drop/mutate arms by hit identity.

## Residual risk and verification gaps

- No execution was performed; every expected exit/counter above is derived statically from the
  gate, the impl, the builders, and verified git-plumbing facts (ancestor relation, byte-equal
  SHA-256s, tree contents at `9fb1f911`). The R01b expectations are `[INFERENCE]` consistent with
  `expected-real.json`, which was itself frozen before implementation.
- The impl's aux/exit/stderr validations (F3) exist in code but are oracle-invisible; mutants
  deleting them pass the frozen suite — that is a *measurement* gap, not an observed impl defect.
- v1 builder/oracle/requirements remain committed and loadable beside v2; any seat or
  verifier loading `oracle-reconcile.py` + `requirements.json` measures the superseded semantic.
- Sibling `build/AttackR03.md` argues the v1 (supplied-policy-path) semantics — it predates or
  ignores `denominator-correction.md`; L1 must disposition it against the correction doc rather
  than the contract text.
- `expected-real.json` binds counters only; if R01b is added, also pin `raw_hits`/`scanner_hits`
  identity digests (e.g., sha256 of the sorted hit list) so the real arm can't pass on
  count-agreement alone — the very mistake this round's lesson names.
