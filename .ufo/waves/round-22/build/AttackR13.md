# AttackR13 — R13 "measured revision mismatch/unresolvable returns 2" (static review only)

Seat MoriR22.AttackR13. Static review only: no tests, builds, oracle or fixture runs; no installs. Findings come from reading files and read-only `git -C` plumbing (`cat-file --batch-check`, `rev-parse --verify`, `merge-base --is-ancestor`, `ls-tree`) against the lane repo only. No fixture repos were created. No matched text appears here. No measurement is claimed.

## Inputs read

- Contract `.ufo/waves/round-22/contract.md` (R13 text; CLI/evidence clauses; sha256 matches `requirements.json.contract_sha256`).
- Frozen `oracle-reconcile.py` and `frozen/fixture-builder.py` (the only candidates; no Impl/Fixture candidate exists — `.scratch/round22` is absent, no `tools/mori-retention-reconcile*` file found; nothing polled).
- `tools/mori-retention-gate.py` `_scan_git_revision` (lines 161–204) and `_validate_allowlist` (136–158): the receipt producer and the semantics the reconciler must independently reproduce.
- Real receipt `.ufo/waves/round-21/evidence/final/retention-floor.json` (wrapper/inner keys and scalar fields only).
- `build/GateGit.md` (revision-resolution semantics) and `build/AttackR15.md` (fixture allowlist defect; setup-attribution defect pattern).
- `.scratch/SrcGitCommit-git-rev-parse.html` (gitrevisions disambiguation rules).

## Verdict

R13 as frozen is scored by a single arm (`invalid-revision`, `measured_revision='0'*40`) and an assertion of only `exit==2`, `finding_id==RETENTION_RECONCILIATION_SETUP`, empty stderr. It exercises only the "unresolvable" half and cannot attribute the 2 to the revision check. Three defect classes let a wrong implementation pass, and two blind spots let a wrong requirement be scored.

Verified on the lane repo (git 2.56.0, sha1): `0*40^{commit}` reports `missing`; `HEAD^{commit}` resolves to a commit; a 40-hex **uppercase** string resolves via `rev-parse` (output lowercased); `merge-base --is-ancestor` is non-strict (self → exit 0).

## R13 partition (the boundary that must be frozen)

The contract gives `measured_revision` three independent conditions. R13 owns the first two plus internal consistency; R14 owns the third:

1. **Form**: literal full object-id hex (40 in sha1 repos), not a revspec. Refs, `HEAD`, abbreviations, `@{n}`, `~`/`^` expressions, non-hex, non-string → exit 2.
2. **Resolves to a commit object in `--repo`**: missing oid → 2; oid naming a tag/tree/blob → 2 (peeling is not allowed — the receipt must name the commit itself).
3. (R14) Ancestor of the resolved input revision.
4. **Internal consistency**: `wrapper.measured_revision` must equal the inner `stdout.commit` (the receipt's claimed scan revision) and, under the R24 provenance binding, the `argv --rev` token. In the real receipt all three are identical (`9fb1f911…`). Any divergence → 2, not 1.

## Counterexample 1 (blocking): the arm cannot attribute the failure

`record('R13','invalid-revision',2,'RETENTION_RECONCILIATION_SETUP')` has no predicate. Every setup failure in the tool shares that finding_id. Compounded by the inherited fixture defect: `fixture-builder.py` emits allowlist rows without the `rule` field that `tools/mori-retention-gate.py:142–152` requires (`expected_fields` includes `rule` ∈ {"a","b","c"}). A reconciler that faithfully reproduces allowlist semantics exits 2 (`invalid_allowlist_row`) **before** its revision check, on every variant — R13 is then scored pass without revision logic running at all (same blocking defect AttackR15 filed for R15; R13 is equally exposed).

Required correction: add `row['rule']='a'` in the builder (L1 decision — the file is frozen), and freeze an R13-specific error code, asserted in the oracle:

```python
record('R13','invalid-revision',2,'RETENTION_RECONCILIATION_SETUP',
       predicate=lambda v,f: v.get('error') in
           {'measured_revision_invalid','measured_revision_unresolvable'}
           and 'receipt_match' not in v and f['measured_revision'] not in json.dumps(v))
```

The last clause matters: `measured_revision` is attacker-controlled; echoing it into `error` or stderr violates the sanitized-code clause (and, for text values, R23).

## Counterexample 2 (blocking): symbolic-name measured revision passes a gate-idiom implementation

The most probable implementation copies the gate's idiom: `cat-file --batch-check` fed `<mrev>^{commit}` (gate lines 180–186), which peels **any** revspec. Verified: `HEAD^{commit}` resolves to a commit. The gate itself documents this is not a full-id check (GateGit §1).

Fixture `measured-ref-form`: `wrapper['measured_revision']='HEAD~1'` (and `result['commit']='HEAD~1'`). In the generated linear repo, `HEAD~1` at receipt-generation time is exactly the measured commit. A peeling implementation resolves it to the true measured commit, ancestry and policy bytes pass, recomputation matches → **exit 0**. Contract-correct: exit 2. Companion arms, all expecting exit 2 / `measured_revision_invalid`:

- `measured-abbrev`: `measured[:12]` — resolves under the unique-substring rule → 0 under a naive peel.
- `measured-head`: `'HEAD'` (resolves to the receipt commit's parent context per rev-parse rule 1).
- `measured-tag`: `git tag -a r13tag <measured>` (before the second commit, builder-side); `measured_revision=<tag_oid>`. `^{commit}` peels a tag OID to the commit; `merge-base --is-ancestor` and `ls-tree` also peel → a type-unchecked implementation returns 0. `cat-file -t` returns `tag` → must be 2.
- `measured-tree`: `measured_revision=<measured>^{tree}` oid — type check `!= commit` → 2; also catches implementations that skip ancestry and `ls-tree` the name directly (works on a tree, identical content → 0).
- `measured-empty`: `''` — fed to batch-check stdin as `^{commit}\n` it resolves `HEAD^{commit}`; without a literal-equality check this is a silent 0.

## Counterexample 3 (blocking): the "mismatch" half is completely unexercised

`invalid-revision` corrupts `wrapper.measured_revision` and `result['commit']` **together**; `diverged` also keeps them equal. No arm ever separates the three copies of the revision. An implementation that validates only `wrapper.measured_revision` and ignores the inner `stdout.commit` (and `argv --rev`) passes all current arms while accepting a receipt whose claimed scan commit contradicts its wrapper.

Fixture `measured-commit-mismatch`: valid wrapper (`measured_revision` = real measured commit, still an ancestor), but inner `stdout.commit='0'*40`. Expected: exit 2 `receipt_commit_mismatch`, not 0 (claim contradiction, fail closed) and not 1 (receipt-vs-recomputation disagreement is reserved for *content* partitions). Inverse arm (wrapper corrupt, inner honest) is already `invalid-revision`. Companion: `argv_rev_mismatch` — argv `--rev` token ≠ `measured_revision` → 2 (`receipt_argv_mismatch`); the real receipt binds all three, so the binding is checkable.

## Counterexample 4: setup-vs-mismatch precedence is untested for R13

An implementation that recomputes at `--rev` first and returns 1 on hit disagreement before checking `measured_revision` fails R13's "unresolvable" arm correctly only by accident of ordering it happens to check schema first. Pin the order: `invalid-revision-dirty-content` — `measured_revision='0'*40` AND `result['hits']` mutated (e.g. drop one). Expected: exit 2 with the R13 code, never 1. Setup always precedes mismatch.

## Counterexample 5: blob-vs-worktree receipt read

Contract: "Read receipt/policy/allowlist via Git blobs, not worktree." Every fixture keeps worktree == input commit, so a worktree reader is indistinguishable. Fixture `invalid-revision-worktree-fixed`: commit the `invalid-revision` receipt, then overwrite the worktree `receipt.json` (unstaged) with a wrapper whose `measured_revision` is the real commit. Blob reader → 2 (`measured_revision_unresolvable`); worktree reader → 0. This is the cheapest R13-keyed enforcement of the blob-read clause.

## Semantic ambiguities L1 must freeze

1. **"Full commit" = literal equality.** Canonical check: feed `measured_revision` (no `^{commit}`) to `cat-file --batch-check='%(objectname) %(objecttype)'`; require output `<same-literal-string> commit`. One check rejects refs, tags (returns `tag`), trees/blobs, abbreviations (resolves to a different-length string), and revspecs. Uppercase hex resolves (verified) but output is lowercase → literal-equality rejects it; freeze "lowercase only, byte-equal" matching the gate's `OBJECT_ID_RE` and real-receipt production, OR normalize — but reject is safer and receipts are always lowercase.
2. **Ambiguous hex/ref collision.** gitrevisions(7) disambiguates a name as a ref before object-prefix matching (6-rule list, doc lines 3073–3102); a branch named `<40-hex>` pointing at an ancestor commit would let a naive resolve pass the ancestor check with a hijacked object. Literal-equality check on the batch-check output defeats it: the resolved oid differs from the input string. [INFERENCE — the doc ordering is confirmed, the collision itself is not constructible read-only.]
3. **Newline/whitespace injection.** `measured_revision` reaches batch-check via stdin in the gate idiom; without the gate's line-178 NUL/LF pre-check, `'hex\nHEAD'` becomes two queries and line-2 resolves `HEAD`. Require the form regex (and NUL/LF/whitespace rejection) **before** any subprocess feed; also argv-side, `'--all'`-style values must never reach git as options.
4. **Self-ancestry.** `merge-base --is-ancestor` is non-strict (verified: self → 0). The strict variant (measured == input) is physically unconstructible for a receipt committed inside `--rev`: a blob cannot name the commit that contains it (hash preimage). Freeze non-strict; no arm needed.
5. **`--rev` form.** "Exact committed input revision, resolved once" — apply the same literal-full-hex + commit-type rule to `--rev`; a symbolic `--rev` re-resolved per call violates "resolved once". Oracle has no arm; flag for RequirementTrace/L1 ruling.
6. **`measured_revision` must be verified against the blob object, not merely existence**: `cat-file -e` passes for trees/blobs; the type word must equal `commit` (already covered by counterexample 2's `measured-tree`).
7. **Exit-2 payload shape.** Propose `{finding_id, error, privacy_clearance:false}`; no `raw_total`/`scanner_total`/`receipt_match:true`; `error` is a frozen enum code, never the offending value, exception text, or git stderr; process stderr empty (oracle already asserts `cp.stderr==''`).

## Expected fixture assertion (R13, all arms)

Every R13 arm: `returncode==2`; stdout parses to a dict with `finding_id=='RETENTION_RECONCILIATION_SETUP'`; `error` equals the arm's frozen code (`measured_revision_invalid` / `measured_revision_unresolvable` / `receipt_commit_mismatch` / `receipt_argv_mismatch`); `stderr==''`; no reconciliation counters; `privacy_clearance` is `false` if present. Counters: N/A — a setup failure emits no population counters.

## Real-repo regression check (plumbing only)

The real receipt (`blob 5c81c3f9…` at entering rev) has `measured_revision` = `argv --rev` = inner `commit` = `9fb1f911…3897`, a verified ancestor of entering `77a5bbe8` (`merge-base --is-ancestor` → 0). All proposed R13 checks hold on it (literal 40-hex lowercase, type commit, three-way binding equal), so none convert the real R02/R24 run into a spurious 2.

## Impacted axes

- **calibration**: un-attributed exit-2 inflates the R13 pass signal.
- **depth**: symbolic/tag/abbrev forms and the wrapper/inner binding are the real revision-semantics surface; untested.
- **operability**: a pass today is consistent with the revision code never executing.

## Exact actionable criterion (R13)

R13 passes iff all hold:

1. The `valid` control returns exit 0 `RETENTION_RECONCILED` (requires the frozen allowlist `rule` fix).
2. Every arm in counterexamples 1–5 returns exit 2, `finding_id=RETENTION_RECONCILIATION_SETUP`, the arm's frozen `error` code, empty stderr, no counters, no echoed revision value: `invalid-revision`, `measured-ref-form`, `measured-abbrev`, `measured-head`, `measured-tag`, `measured-tree`, `measured-empty`, `measured-commit-mismatch`, `argv_rev_mismatch`, `invalid-revision-dirty-content`, `invalid-revision-worktree-fixed`.
3. The implementation binds the measured revision by literal full-hex + `commit` object-type equality (counterexample 2 check), checks ancestry separately, and resolves the receipt/policy/allowlist only through the once-resolved commit oids.

No tool installs or updates were performed (existing git 2.56.0 / python 3.14.8 sufficed).
