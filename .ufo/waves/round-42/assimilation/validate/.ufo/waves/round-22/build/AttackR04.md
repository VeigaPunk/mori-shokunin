# AttackR04 — frozen R04 (scanner hit identities = raw minus excluded-path hits)

Seat: `MoriR22.AttackR04` (reviewer, leaf). Static review only: no tests, builds, gates, reconciler runs, or fixture executions. One arithmetic check was run locally over the already-committed r21 receipt JSON to derive the frozen multiset digests below (all inputs are committed metadata — path/line/class/digest — no matched text). No tools were installed or updated.

## 0. Effective semantics (must be stated before any attack)

`contract.md:19` freezes the literal text "R04 scanner hit identities exactly raw minus policy-path hits". `denominator-correction.md:9` supersedes the *basis*: "R04 compares scanner identities to raw minus independently matched non-author identities, not source-policy path". The frozen v2 stack implements the correction:

- `frozen/fixture-builder-v2.py:39` — `non_author_paths_glob:['non-author.txt']`; `:107-108` — `expected_policy_hits`/`expected_scanner_hits` partition on `'non-author.txt'`.
- `oracle-reconcile-v2.py:50` — R04 predicate: `sorted(v['scanner_hits'],key=(path,line)) == sorted(f['expected_scanner_hits'],key=(path,line)) and v['policy_excluded_hits']==f['expected_policy_hits']`.
- `frozen/expected-real.json:19-20,28` — `policy_excluded:5`, `scanner_total:90`, `exclusion_basis:"non_author_paths_glob"`.

So R04's effective post-correction criterion is: **the excluded partition is exactly the set of raw hit identities whose path matches `non_author_paths_glob` under the existing gate's `fnmatch.fnmatch` semantics; `scanner_hits` is raw minus that set; both are identity multisets, not counts.** Findings below attack the corrected requirement; where the literal contract text still misleads, that is itself a finding.

## 1. Findings by severity

### F1 (high) — The pinned contract text and the normative oracle still disagree on R04's basis; only out-of-band documents reconcile them

- `contract.md` (pinned byte-identical by `measure-round22.py:23` via `contract_sha256`) still says "policy-path hits". `requirements-v2.json` freezes only the ID list plus a `supersedes` pointer; `denominator-correction.md` is pinned alongside but nothing inside `contract.md` points to it.
- Concrete consequence, traced statically: an implementation faithful to the literal text computes on the real receipt `policy_excluded=4` (exact-path hits on `.ufo/waves/round-18/frozen/c1-policy.json`, per RawPartition.md:42) and `scanner_total=91`, so `realmatch` fails against `expected-real.json` (5/90). On the *synthetic* fixture the literal reading is worse than wrong — it is **coincidentally count-correct**: v1 fixture had policy-excluded=1 and non-author=1, so R03 `(5,1,4)` passes either way, and only R04's identity comparison separates the two bases. R04 is the sole frozen ID that discriminates the exclusion basis on synthetic input.
- The stale v1 artifacts (`oracle-reconcile.py`, `frozen/fixture-builder.py`, `frozen/requirements.json`) remain committed in place. They must stay byte-unchanged (historical evidence), and `measure-round22.py` invokes only v2 — but nothing inside `oracle-reconcile.py` marks it superseded. An operator running it against the shipped tool gets 24/24-looking results under dead semantics. (Also: v1 fixtures' allowlist rows lack the `rule` field, so the current impl exits 2 on them — the failure mode is loud, not silent, but the misleading file still invites the run.)
- **Exact criterion:** `requirements-v2.json` should carry, per ID, the one-line corrected requirement text (not just the ID), and `measure-round22.py` should additionally pin/require `--requirements frozen/requirements-v2.json` only. The v1 files stay untouched; the binding lives in the v2 metadata (it already carries `correction_sha256` — extend it with `"r04_basis":"non_author_paths_glob"` or a text map). Cost: one JSON field; prevents any future seat from re-deriving the literal misreading I almost shipped.

### F2 (high) — The synthetic R04 fixture never exercises a glob: `['non-author.txt']` has zero metacharacters, so literal-membership, `fnmatch`, `pathlib.PurePath.match`, and `glob`-module engines all pass

The whole R04 check reduces to set membership on one literal string. Three progressively weaker implementations are indistinguishable on it:

| excluded-set implementation | synthetic valid arm | real receipt |
|---|---|---|
| `h['path'] in {'non-author.txt'}` (literal set) | passes R04 | fails `realmatch` (excluded=0, `non_author` mismatch) |
| `pathlib.PurePath(h['path']).match(g)` | passes R04 | **passes** — real paths are same-depth as both real globs |
| `fnmatch.fnmatch(h['path'],g)` (correct, gate parity) | passes R04 | passes |

The real input catches literal impls, but **fnmatch-vs-pathlib divergence is invisible to both the synthetic and the real input**: `fnmatch`'s `*` crosses `/` (`corpus/lessons/round-*-verifier-spotcheck.md` also matches a deeper nested path); `PurePath.match`/`glob` do not. No fixture, refinement case, or `measure-round22.py` mutant exercises this. `PolicySemantics.md:39-42` documented the semantics as [INFERENCE] with "no fixture in the repo exercises it" — still true for the reconcile stack.

**Counterexample fixture — new additive variant `glob-partition`** (does not disturb the frozen 5/1/4 'valid' arm; R03's pinned counts are untouched). Policy for this variant: `non_author_paths_glob:['corpus/lessons/*-spotcheck.md','outside/*.txt']`, one class `{id:'R22',regex:'[R]22_SAMPLE'}`, `must_redact_paths:[]`, `'synthetic':TOKEN` self-hit as in v2. Files at measured tree:

| path | content | disposition |
|---|---|---|
| `policy.json` | as v2 (1 self-hit at `'synthetic'` line) | scanner; allowlisted |
| `allowed.txt` | `TOKEN allowed` ×2 | scanner; allowlisted |
| `unallowed.txt` | `TOKEN retained-red` | scanner; unallowlisted |
| `non-author.txt` | `TOKEN outside-author` | **scanner** (matches no glob now); allowlisted |
| `corpus/lessons/round-9-spotcheck.md` | `TOKEN n` | excluded; **also allowlisted** (overlap arm) |
| `outside/shallow.txt` | `TOKEN s` | excluded (same-depth `*`) |
| `outside/deep/nested.txt` | `TOKEN d` | excluded **only under fnmatch** — the discriminator |
| `kept/mirror.txt` | byte-identical to `outside/deep/nested.txt` (same blob OID) | scanner; unallowlisted — kills OID/content exclusion and proves per-path partition under blob caching |
| `mirror/policy.json` | byte-identical to `policy.json` (same OID) | scanner; unallowlisted — replicates the real r21 nested-policy-copy trap (RawPartition.md:9,110) |
| `binary.bin` | `TOKEN\x00…` | NUL-skipped |

Allowlist rows (with `rule:'b'`): policy.json, allowed.txt ×2, non-author.txt, `corpus/lessons/round-9-spotcheck.md` — 5 distinct `(path,class,sha)` keys. Builder must compute the excluded set by evaluating the policy's own globs with `fnmatch` (spec re-implementation), never by a hardcoded path list — see F7.

**Expected (variant `glob-partition`, receipt honest ⇒ exit 0, `RETENTION_RECONCILED`):**

- `raw_total=10`; `policy_excluded=3`; `scanner_total=7`; `non_author=3`; `allowlisted=5`; `raw_unallowlisted=3` (`unallowed.txt`, `kept/mirror.txt`, `mirror/policy.json`); `scanner_unallowlisted=3`; `forbidden_allowlist=0`; `retention_state='red'`; `privacy_clearance=false`; `exclusion_basis='non_author_paths_glob'`.
- Receipt values: `hits`=10, `metric=3`, `non_author=3`, `routed=0`, `finding_id='RETENTION_FINDINGS'`, `exit_code=1`.

Wrong implementations killed, with the observable each flips:

| defect | observable |
|---|---|
| literal path-set exclusion | `non_author=0` → receipt mismatch → exit 1 (also `policy_excluded=0`) |
| `PurePath.match` / `glob` engine | `outside/deep/nested.txt` stays in scanner → `scanner_total=8`, `policy_excluded=2`, identity sets wrong |
| exclusion by blob OID / content / basename | `kept/mirror.txt` and/or `mirror/policy.json` wrongly excluded → identity sets wrong (counts can coincidentally hold at 3 if exactly one extra is dropped) |
| count-subtraction `unallowlisted=raw−allowlisted−excluded` | gives 2 (the allowlisted∩excluded spotcheck hit is double-subtracted) vs correct 3 — the exact trap `denominator-correction.md:7` names |
| policy-path exclusion (literal contract reading) | excluded=`{policy.json}`=1, scanner=9 — fails identities even though `policy_excluded` is plausible |

### F3 (medium) — Oracle comparator weaknesses make future multi-hit fixtures falsely fail, and R04 never asserts partition completeness

`oracle-reconcile-v2.py:50` has three mechanical gaps:

1. **`sorted(key=(h['path'],h['line']))` is not a total order.** Two classes matching one line (the gate emits one hit per (line,class), `mori-retention-gate.py:95-102`) tie on the key; Python's stable sort then makes equality depend on each side's emission order — builder order (dict insertion, class order inside line) vs tool order (`ls-tree` order). A correct tool can false-fail. Current fixture is single-class so latent only. Fix: sort/compare by the full 4-tuple `(path,line,class,line_sha256)` — still a total order — or better:
2. **`v['policy_excluded_hits']==f['expected_policy_hits']` is order-sensitive list equality.** Fine with exactly one excluded hit; with ≥2 excluded hits the builder's `files`-insertion order and the tool's `ls-tree` order can legitimately differ → false fail. Fix: `Counter(identity(h))` multiset comparison both sides (GateRaw.md parity item 35 recommends `Counter` for exactly this reason).
3. **No completeness/disjointness assertion.** R04 checks `scanner` and `excluded` against fixture truth, but never asserts `Counter(scanner)+Counter(excluded)==Counter(raw_hits)` or that the two are disjoint, and `raw_hits` itself is never compared to fixture truth anywhere in the oracle (R22 only checks `raw_total==5` and no `binary.bin` path — count + one path). A tool emitting a fabricated `raw_hits` list that omits an awkward hit while `scanner_hits`/`policy_excluded_hits` are correct would pass every arm that doesn't run a receipt mutation. Fix: add `Counter(h4(v['raw_hits']))==Counter(h4(all expected hits))` plus `not (Counter(scanner)&Counter(excluded))` and sum-equality to the R04 predicate.

Positively: the `sorted(...) == sorted(...)` shape does enforce exact 4-field dicts — missing/extra keys flip equality or raise `KeyError` (caught → `ok=False`). And `data['runs']` retains the tool's raw stdout, so discrepancies are diagnosable.

### F4 (medium) — "digest-only identities" vs the oracle's full-hit-dict expectation is an unresolved shape fork

`contract.md:13` says "report excluded count and digest-only identities separately". The v2 oracle expects `policy_excluded_hits` to be **full 4-field hit dicts**; the worktree draft emits full dicts (consistent). But a literal reading of "digest-only" (e.g. `{path,class,line_sha256}` triples like the receipt's auxiliary/`forbidden_allowlist` rows, which drop `line`, or bare sha strings) produces an implementation that fails R04 while arguably honoring the contract. Freeze one of:

- **Recommended:** `policy_excluded_hits` = full hit dicts (uniform with `raw_hits`/`scanner_hits`); additionally emit `policy_excluded_sha256` and `scanner_sha256` as single multiset digests: `sha256('\n'.join(sorted(identity_digests)).encode())` where `identity_digest = sha256(json.dumps([path,line,class,line_sha256],separators=(',',':')).encode())` — the exact formula RawPartition.md:73 used and which I reproduce below.
- Or change the oracle to accept triples. Pick before integration; the field name `policy_excluded_hits` must not silently change shape later.

Real-input frozen values (computed by me from the committed `retention-floor.json`; method verified — my reproduction matches all five multiset digests RawPartition.md published, and the five member digests below equal its non-author residual list):

- `policy_excluded` member digests (5): `11c9a159…cc`, `47160199…be`, `6a8a60db…cf`, `b922918d…59`, `de3e7716…53` — multiset `22fc1f3c2801d2a504f27a916fd6849064404eb5abea53079e2752a86e5ec338`.
- `scanner_hits` (90) multiset `482bc9a85f23b44657feea4e6306494605518af926c074c3a8ae0f3537675153`.
- (For cross-check: raw 95 = `f32d12cc…`, policy-*path* 4 = `27f5af96…`, scanner-under-literal-reading 91 = `ece92e52…` — all reproduced from RawPartition, confirming the corrected partition is the 5/90 one.)

### F5 (medium) — `expected-real.json` checks scalars only; R04's identity claim is never asserted on the real input

`measure-round22.py:81` does `all(type(real.get(k)) is type(v) and real.get(k)==v …)` over `expected['expected']` — all scalars. `scanner_hits`, `policy_excluded_hits`, `raw_hits`, `exclusion_basis` correctness on real input rests entirely on scalar agreement. A tool emitting right counts with wrong identity lists passes `realmatch`. Two cheap closes:

- Add `excluded_multiset_sha256: "22fc1f3c…e338"` and `scanner_multiset_sha256: "482bc9a8…5153"` to `expected-real.json` and assert them in `realmatch` (metadata digests only — consistent with the "no matched text" bound).
- Add `v.get('exclusion_basis')=='non_author_paths_glob'` to the R04 oracle predicate; currently a tool emitting `'policy_path'` passes all 24 synthetic arms and is caught only by the real scalar comparison.

### F6 (low-medium) — Edge partitions R04 implicitly requires are uncovered

- **Excluded∩allowlisted overlap:** covered only by `refinement-reconcile.py` `non-author-overlap` — and only at counter level (`allowlisted==4, non_author==1, raw_unallowlisted==1`), never identity lists. The `glob-partition` fixture above embeds the overlap inside the frozen-style check.
- **Multiplicity:** raw multisets with two identical lines in one excluded file (same `line_sha256`, different `line`) are legal (identities differ by line); no fixture exercises excluded-set multiplicity >1.
- **R04 runs only on `valid`:** the `forbidden` variant never gets an identity-list check; a tool special-casing partition logic on `must_redact` state would pass.
- **Receipt-side coupling is right and should be stated:** the receipt's `hits` is the raw population (both real and synthetic receipts include excluded hits), while `unallowlisted_hits`/`metric`/`non_author` are scanner-side. A tool that validates receipt `hits` against the scanner set (or `unallowlisted` against raw) exits 1 on every valid receipt — the draft does this correctly (Counter comparisons at `tools/mori-retention-reconcile.py:207-213`).

### F7 (low) — Fixture-builder fragility that will silently corrupt the counterexample if it is rebuilt

- `fixture-builder-v2.py` hardcodes `'non_author':1` in the synthesized receipt and derives `expected_policy_hits`/`expected_scanner_hits` by **literal path equality** (`h['path']=='non-author.txt'`, `:107-108`). That is only safe while the glob list is literal. The `glob-partition` variant must instead compute the excluded set by evaluating the policy's glob list (`fnmatch`, matching gate semantics) and set `result['non_author']=len(excluded)` — otherwise the synthetic receipt is inconsistent with its own policy and every honest reconciler exits 1, invalidating the fixture.
- The builder also hardcodes `class:'R22'` and a single class (`:53`); multi-class policies would silently mis-generate expected hits. Constraint, not a defect today.

### F8 (low) — Draft impl candidate, static trace (informational, not measured)

`tools/mori-retention-reconcile.py` exists in the worktree only (untracked, `??`; `measure-round22.py:40-41` will require it committed at the measured revision). Traced statically against effective R04:

- **Consistent:** exclusion computed as `excluded=[h for h in hits if is_non_author(h)]` with `is_non_author = any(fnmatch.fnmatch(path,g))` (`:199-201`); `scanner` is raw minus that set; `exclusion_basis:'non_author_paths_glob'` emitted; `policy_excluded_hits`/`scanner_hits`/`raw_hits` are full 4-field dicts; hit order is `ls-tree` order (fine under multiset comparison); the OID blob cache keeps `path` in every identity, so the identical-copy case is handled per-path; receipt `hits` validated against raw recomputation.
- **R04-adjacent divergence (shared finding, not new):** `tree()` decodes paths with `errors='strict'` → exit 2 `invalid_tree_path` on non-UTF-8 tree paths where the gate uses `errors='replace'` and would have scanned them (GateRaw F1/F3, PolicySemantics §5 already record this contract tension).
- **Nothing to fix for R04 itself** under the corrected semantics; the v2-oracle R04 predicate plus the comparator fixes in F3 determine the verdict mechanically.

## 2. Exact actionable acceptance criterion for R04

Freeze this as the testable form (post-correction basis). A tool passes R04 iff, on a fixture whose `non_author_paths_glob` contains `*` metacharacters and a nested path (the `glob-partition` arm), and on the 'valid' arm:

1. `Counter(h4(v['policy_excluded_hits'])) == Counter(h4(h for h in expected_raw if any(fnmatch.fnmatch(h['path'],g) for g in globs)))` where `h4=(path,line,class,line_sha256)` and `globs` come from the *policy blob*, not the fixture path list.
2. `Counter(h4(v['scanner_hits'])) == Counter(h4(expected_raw)) − Counter(h4(excluded))`, `Counter(scanner)&Counter(excluded)==∅`, and `Counter(scanner)+Counter(excluded)==Counter(h4(v['raw_hits']))==Counter(h4(expected_raw))`.
3. Scalars: `policy_excluded==len(excluded)`, `scanner_total==len(scanner)`, `exclusion_basis=='non_author_paths_glob'`, `scanner_unallowlisted == raw_unallowlisted == len(scanner hits not allowlist-keyed)` (they are the same set by definition — divergence between these two counters is itself a defect signal).
4. Every element of the three lists has exactly keys `{path,line,class,line_sha256}`, `line` a true `int` `>=1`, `line_sha256` 64-lower-hex.
5. Hits at a byte-identical non-matching path (same blob OID) and at the literal policy path remain in `scanner_hits`; only glob-matched paths leave.
6. On real input: the two frozen multiset digests in F4 hold.
7. Exit 0/`RETENTION_RECONCILED` requires the receipt's own `hits` to equal the recomputed raw multiset (excluded hits included); `unallowlisted_hits`/`metric`/`non_author`/`finding_id`/`exit_code` recomputed and equal — partition disagreement anywhere is exit 1, never silently re-partitioned.

## 3. Residual risk and verification gaps

- The black-box oracle cannot prove the tool *recomputed* hits rather than echoing receipt lists — mitigated by R05–R10 mutants plus `measure-round22.py`'s `count-only`/`wrong-population` mutants and the real-input run, but **no mutant exercises a glob-engine swap**; recommend adding a fourth mutant replacing `fnmatch.fnmatch` with literal membership (killed by real input) and, once `glob-partition` lands, a `PurePath.match` mutant (killed only by the new arm).
- `sorted(key=(path,line))` and `list==list` comparators must be fixed before any fixture with ≥2 excluded hits or ≥2 classes/line ships, or the oracle manufactures false negatives (F3).
- `contract.md` text vs corrected semantics remains a live confusion source for wave-2 falsifiers; `requirements-v2.json` should carry corrected per-ID text (F1).
- The `digest-only identities` contract phrase vs full-dict oracle expectation must be frozen one way before integration (F4); I recommend full dicts + two multiset-digest fields, digests as supplied above.
- Open debts unchanged by anything here: `privacy_clearance` is hard-false, r21 permission control stays RED11/12, both historical dispositions unknown, baseline blocked. R04 satisfaction is accounting agreement only — a matched receipt is not clean retention.

## 4. What was verified vs not

- **Verified by reproduction:** all five RawPartition multiset digests recomputed byte-identically from the committed receipt → the partition arithmetic and digest formula are confirmed; the new excluded/scanner digests in F4 are therefore trustworthy frozen values.
- **Static-only:** the draft impl trace (F8), all expected fixture values (F2 table derived by hand, not executed), oracle comparator behavior (F3 read, not run).
- **Not done (per bounds):** no tool runs, no git fixture creation, no tests. `.scratch` untouched except nothing was written there.
