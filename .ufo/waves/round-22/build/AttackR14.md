# AttackR14 — "target not ancestor returns 2": arm contamination, missing counterexample classes

Seat: MoriR22.AttackR14 (reviewer, read-only). Scope: frozen requirement R14 only — the contract clause "Receipt target measured_revision must be full commit and ancestor of input revision" (contract.md §CLI, §Frozen requirement IDs). Evidence: `.ufo/waves/round-22/frozen/fixture-builder.py`, `.ufo/waves/round-22/oracle-reconcile.py`, the untracked SUT draft `tools/mori-retention-reconcile.py`, and sibling static reports (GateGit.md, ReceiptBinding.md). Static review only: no tests, fixtures, or probes run; the only git use was read-only `status`/`log`/`ls-tree` on the lane repo. Nothing installed.

## Verdict

R14 is the weakest-discriminated requirement in the frozen suite. The single arm (`diverged`) is **self-contaminated** — it can pass on receipt-internal inconsistency without any ancestry logic — and it exercises only the "no common ancestor" case, so three plausible SUT classes satisfy all 24 arms while violating the ancestor clause. The untracked SUT draft handles R14 correctly (lines 161–163), but the frozen oracle cannot currently prove that property, and weaker drafts would not be caught.

## Findings by severity

### F1 (high): the `diverged` arm can pass with zero ancestry logic — stale `argv --rev`

`fixture-builder.py:88-91` (variant `diverged`) sets `wrapper['measured_revision']=other` and `result['commit']=other` but leaves `wrapper['argv']` unchanged, so the embedded `--rev` argument still names the original measured commit M1 — a different value from `measured_revision`. The receipt is therefore internally inconsistent on a second, ancestry-independent axis.

Any SUT that validates "the value after `--rev` in `argv` equals `measured_revision`" — a check the contract itself motivates ("required field/type/schema inconsistencies must fail closed"; the SUT draft enforces it as `receipt_revision_conflict`, line ~175) — returns exit 2 / `RETENTION_RECONCILIATION_SETUP` on this arm **without performing the ancestor check**, provided that check runs before (or instead of) ancestry. The oracle asserts only `exit_code==2`, `finding_id=='RETENTION_RECONCILIATION_SETUP'`, `stderr==''` and JSON-parseable stdout (`oracle-reconcile.py:42,54`), so the wrong reason is unobservable.

- Ancestry-less + argv-checking SUT → exit 2 → **R14 passes**.
- Ancestry-less + argv-ignoring SUT → recomputes on `other`'s tree, which is `rev-parse HEAD^{tree}` of M1 (identical hits and identical policy/allowlist bytes) → exit 0 → R14 correctly fails. The arm only discriminates SUTs missing *both* checks.

**Action (FixtureReconcile):** in the `diverged` arm, also set `wrapper['argv'][wrapper['argv'].index('--rev')+1]=other` before serialization. `expected_receipt_sha256` is already computed from the final bytes (`fixture-builder.py:105`), so no other change is needed. Expected after fix: exit 2, `RETENTION_RECONCILIATION_SETUP`, `stderr==''`, `error` ∈ bounded setup vocabulary.

### F2 (high): unrelated-root counterexample misses merge-base-existence and ref-containment SUTs

`other=git commit-tree HEAD^{tree}` creates an *unrelated root commit*: `merge-base(other, input)` is empty and `other` is unreachable from every ref. That is the weakest possible "not ancestor" case. Two plausible SUT classes pass all 24 arms yet violate R14:

- **Existence check:** `git merge-base <measured> <input>` succeeding (non-empty output / rc 0) treated as "related ⇒ acceptable". Accepts siblings/cousins sharing any ancestor.
- **Containment check:** `git branch --contains <measured>` / `git rev-list <some-ref> | grep` / "commit reachable from any ref". Accepts any commit on any side branch; also *rejects* the frozen `diverged` commit for the wrong reason (unreachable, not non-ancestral) — which still yields exit 2, so the arm cannot tell.

**Concrete counterexample fixture — `variant='cousin'`:**

1. After the M1 commit, create `M2 = git commit-tree <M1 tree> -p M1` (sibling lineage: child of M1, distinct commit).
2. `git branch r22-side M2` so M2 is reachable from a ref.
3. Receipt at input commit R (child of M1) declares `measured_revision=M2`, inner `commit=M2`, `argv --rev=M2` — all three consistent.
4. `merge-base(M2, R) == M1` exists; M2 is **not** an ancestor of R.

Expected: exit 2, `RETENTION_RECONCILIATION_SETUP`, `stderr==''`, JSON stdout; no counter assertions (setup failures carry none). This kills existence-check SUTs (merge-base exists → proceeds → 0/1) and containment SUTs (M2 reachable from `r22-side` → proceeds → 0/1). Do not assert a specific `git merge-base` exit code in the builder; assert only the semantic (SHA emitted vs not).

### F3 (medium): wrong-endpoint SUTs escape — no arm with `--rev ≠ HEAD`

Every fixture leaves HEAD on the input commit. A SUT that checks `merge-base --is-ancestor <measured> HEAD` (or the tip of the default branch) instead of the resolved `--rev` passes all arms: `diverged` still fails (orphan is no one's ancestor) and `valid` still passes. On a legitimate call with `--rev` pointing at an older commit while HEAD sits on a divergent tip, such a SUT accepts receipts whose measured revision is an ancestor of HEAD but not of `--rev`.

**Fixture — `variant='head-diverged'`:** build the cousin construction (M2 child of M1 under branch `r22-side`), commit the receipt as R on the main line, record `revision=R`, *then* `git checkout -q r22-side` (or commit one more child D on M2) so HEAD≠R. `make()` already returns `rev` before any HEAD move would matter — move HEAD *after* `rev-parse HEAD`. `measured=M2` is an ancestor of HEAD(=D-tip) but not of `--rev=R`. Expected: exit 2, `RETENTION_RECONCILIATION_SETUP`.

### F4 (medium): the "full commit" half of the clause is untested

R13's arm (`invalid-revision`) feeds an unresolvable all-zero SHA; no arm feeds a *resolvable* `measured_revision` that is not a full commit ID. A SUT that skips shape validation and does `rev-parse <measured>^{commit}` + `is-ancestor` accepts all of these, reconciles, and exits 0/1 where the clause requires 2:

- **`variant='measured-refname'`:** `measured_revision='master'` (resolves to M1), inner `commit='master'`, `argv --rev='master'` — self-consistent strings, so only the shape clause can reject. Also covers short-SHA/`HEAD~1` forms.
- **`variant='measured-tag'`:** create annotated tag T on M1; `measured_revision=sha256-of-T-object` — a full 40-hex *object* ID that is not a commit. A SUT doing `resolve(measured)==peel` equality passes it; the draft's `resolve(measured)==measured` (line 161) correctly rejects because `^{commit}` peels to M1≠T. Distinguishes peel-equal vs self-equal resolution.

Expected for both: exit 2, `RETENTION_RECONCILIATION_SETUP`. Ambiguity to record in the requirement note: whether a tag-object SHA or symbolic name counts as "full commit" — recommend the strict reading (full-length object ID that resolves to *itself* as a commit), matching GateGit.md §1 ("the reconciler needs its own full-id-equality check").

### F5 (low): no positive control proving "ancestor" is transitive, not direct-parent

Every receipt lands exactly 1 commit after its measured commit. A SUT testing `measured == rev^` (or `rev~1`) passes all arms *and* would even pass against today's real r21 receipt (measured is 1 commit before its landing commit — ReceiptBinding.md §"Observed facts" line 37), but exit-2s every valid receipt landed ≥2 commits later.

**Fixture — `variant='deep'`:** after receipt commit R, add a content-neutral commit (a file matching no policy class, not the policy/allowlist/receipt paths); `--rev=R+1`. Expected: exit 0, `RETENTION_RECONCILED`, same predicate as R03/R04 (`raw_total=5`, `policy_excluded=1`, `scanner_total=4`, identical scanner/policy hit identities). This pins transitive ancestry as the intended semantics — the contract word "ancestor" otherwise admits a parent-only reading.

### F6 (low): diagnostics and selftest gaps

- The draft maps the ancestor failure to `error:'git_read_failed'` (`git()` raising `Invalid` on any non-zero `merge-base` exit). Correct exit/finding, but indistinguishable from repo corruption; recommend a distinct bounded reason (`measured_not_ancestor`) so the R14 arm's *reason* is observable, not just its code. Also gives future arms a discriminating field should the oracle ever assert `error`.
- The draft selftest (`selftest()`, 3 arms) has no diverged arm; `--selftest` is the contract's independent CLI arm exposure — adding one `cousin`/`diverged` subprocess arm there is cheap defense-in-depth.
- `--rev` is resolved via `rev-parse --verify <sel>^{commit}`, which silently peels an annotated tag or accepts `HEAD~2` for `--rev`. Contract says "`--rev` is the exact committed input revision, resolved once" — ambiguous whether symbolic `--rev` is in-contract or must itself be a full commit ID. Not exploited by any arm; flag for a requirement note (strictest reading: apply the same full-id self-equality rule to `--rev`).

## Semantic ambiguities recorded

1. "ancestor" — git's `--is-ancestor` includes equality; a self-referential receipt is physically unbuildable (the containing commit's SHA is unknowable at write time), so equality semantics are moot but should be stated.
2. "target" — three receipt fields claim it: `measured_revision`, `argv --rev`, inner `commit`. The clause must bind all three to one full commit ID *and* ancestry must be evaluated on `measured_revision` vs the resolved `--rev`. F1 shows why a diverged arm must keep them consistent.
3. R13/R14 boundary — unresolvable ⇒ R13; resolvable non-ancestor ⇒ R14; resolvable but wrong-shape/non-commit object (tag, tree, refname) is currently orphaned between them. Recommend folding shape into R14's "full commit" clause explicitly.
4. Shallow/grafted clones can yield false non-ancestor; contract maps that to exit 2 (unevaluable, not defect) — consistent with the fail-closed design, worth one sentence in the requirement note (GateGit.md §3.4).
5. `git merge-base` (non-`--is-ancestor`) exit behavior with unrelated histories is version-sensitive; builders should assert SHA-output semantics, never a numeric code.

## Superficial-pass risk summary

| SUT flaw | Passes frozen R14 today? | Killed by |
|---|---|---|
| No ancestry check, no argv check | No (exits 0) | arm itself |
| No ancestry check, argv-consistency check | **Yes** (exit 2 on stale `--rev`) | F1 fix |
| `merge-base` existence only | **Yes** | F2 cousin arm |
| Ref-containment / `branch --contains` | **Yes** | F2 cousin arm |
| Ancestor-of-HEAD, not of `--rev` | **Yes** | F3 head-diverged arm |
| No full-commit shape check | **Yes** | F4 refname/tag arms |
| Direct-parent only | **Yes** (passes real receipt too) | F5 deep arm |
| Reversed `is-ancestor input measured` | No (killed by R01 valid arm) | existing suite |

## Residual risk and verification gaps

- The SUT draft's R14 handling (shape + self-equal resolve + `--is-ancestor` + fail-closed `git()`) is correct as read; **not verified by execution** — L1 measurement only.
- `GIT_NO_LAZY_FETCH=1`, `--no-replace-objects`, stripped `GIT_*` env, and `--end-of-options` in the draft are all correct for this clause; no R14 defect found there.
- Not assessed (out of R14 scope, but adjacent): whether `receipt_revision_conflict` should run before ancestry for diagnostic clarity — order is contract-free since both paths are exit 2.
- Recommended owner actions: FixtureReconcile adds the F1 fix plus `cousin`, `head-diverged`, `measured-refname`, `measured-tag`, `deep` variants; OracleReconcile records each new arm (`cousin`/`head-diverged`/`refname`/`tag` → code 2 `RETENTION_RECONCILIATION_SETUP`; `deep` → code 0 `RETENTION_RECONCILED` with the R03/R04 predicate). All changes land before implementation integration per the frozen-inputs rule; requirements.json's ID list needs no change if these arms fold under R13/R14 as suggested.
