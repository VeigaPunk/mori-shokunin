# ReviewFreeze — freeze commit order and measured-input provenance

Seat: MoriR22.ReviewFreeze (review, detection/report only, no lane writes outside this file).
Reviewed lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Anchored at HEAD
`3985b3d92be5105a36456bc26235bd1d8399b115` ("round-22: bind receipt paths and
retain discriminating controls"). Integration was still in-flight during review
(untracked `measure-round22.py` edit in worktree, `falsify/` staging); findings
are scoped to commits up to 3985b3d. No tool installs performed. Nothing was
executed: every measurement statement below is `[INFERENCE]` or a read-only
artifact observation, never a claimed pass.

## Findings by severity

### HIGH

**F1 — `expected-real.json` was committed inside the same commit as the SUT, so
the only real-receipt expected values are not frozen before integration.**

`contract.md:19` (frozen at df880b4): "Expected values and fixture generator
must be committed before implementation integration." Fixture builder v2,
oracle v2 and requirements-v2 were frozen at `e2f549b` before SUT `8cb4afb` —
satisfied for the synthetic oracle. But `frozen/expected-real.json`, the only
code-independent-looking expected record for the real r21 receipt
(finding_id=RETENTION_RECONCILED, raw95/5/90/4, `retention_state:"red"`,
`privacy_clearance:false`), first exists at `8cb4afb`, the implementation
commit. Order is trivially "before integration" only because it shares the
commit that *is* the integration. The values were authored while the SUT was
being written, in the same author session (L1 authored both, per
`corpus/lessons/round-22.md` "Implementation and verification provenance").
The expected values are not derived by rerunning the r21 receipt — no rerun
happened; they are L1's transcription of the receipt's own claimed fields
(I verified the transcription: 95/4/5/0 from the receipt stdout parse).
So for the real-input arm, frozen requirement IDs do not prove code-independent
expected values: the expectation is same-author, same-commit, and the only
independence is that the receipt bytes themselves predate the round.

Verified self-consistency (all three digests in `expected-real.json` match
blobs at `input_revision` 77a5bbe: receipt `4001e2d9…`, policy `db06e981…`,
allowlist `f46c78ec…`; policy/allowlist blob OIDs identical at `9fb1f91`
and HEAD; `9fb1f91` is an ancestor of `77a5bbe`). The *values* are correct;
the *provenance class* is "frozen at integration time," weaker than the
contract's pre-integration freeze and not disclosed as such in
`requirements-v2.json` or the SCORECARD entry (SCORECARD says only
"frozen in `.ufo/waves/round-22/frozen/expected-real.json`", which reads
as the stronger claim).

**F2 — Frozen requirement IDs did not pin semantics: R03/R04 were silently
redefined between the v1 freeze and the v2 freeze, and `contract.md` still
states the superseded meaning.**

`contract.md:13` (still authoritative text at HEAD) defines
"Policy-excluded means exactly the supplied policy path" — that is, excluding
the policy *file*. `denominator-correction.md` + `requirements-v2.json`
(e2f549b) redefine it as the non-author-glob identities. The contract blob
was never amended; `requirements-v2.json.contract_sha256` still pins the old
contract bytes (`1658c390…`, verified). The `supersedes` field scopes to
"source-file-exclusion interpretation only", and v1
`frozen/requirements.json` remains committed with the stale meaning. An
implementer reading contract.md + requirements.json (both still in-tree,
both hash-pinned) builds the v1 denominator — which on the real receipt
would compute scanner=91, not 90. This is not hypothetical: I verified
from the real receipt that the supplied policy path carries exactly the 4
*allowlisted* hits and the nested copy carries the 4 unallowlisted ones, so
v1 semantics are observably wrong on the real input. ID freeze guaranteed
literal ID stability only; the semantic underneath shifted. Mitigation is
real but fragile: `measure-round22.py` pins `denominator-correction.md`
via `correction_sha256` and uses requirements-v2, so the measurement
pipeline is consistent; the hazard is purely the self-inconsistent
document set.

### MEDIUM

**F3 — Oracle independence is one-author: fixture builder recomputes expected
hits with its own reimplementation of gate semantics, and the embedded
"receipts" are builder-produced, so the oracle cannot detect a shared
misreading of gate semantics.**

`oracle-reconcile-v2.py` derives `expected_scanner_hits` /
`expected_policy_hits` from `FIX.make()` — `fixture-builder-v2.py`'s own
NUL-skip/`errors='replace'`/`split('\n')`/regex scan — and synthesizes every
receipt by the same code. This is independent of the *SUT* (builder is
separate source; SUT `scan()` at `tools/mori-retention-reconcile.py:138-152`
is separately written) but *correlated with the gate through L1's own
reading of it*. I traced all three implementations: the gate
(`_blob_hits`, `_scan_result`), the builder, and the SUT agree on hit
identity `(path,line,class,line_sha256)`, multiset comparison, non-author
fnmatch partition, allowlist key `(path,class,line_sha256)` and rule-field
validation, so no *observed* defect results. But the independence class of
the frozen expected values is honestly "L1's second implementation", not
"code-independent ground truth". The strongest real independence in the
round is the actual `retention-floor.json` produced by the r21-era gate
process — and its expected values are the F1 caveat. There is also no
frozen oracle arm that invokes the SUT against the real receipt; the real
arm lives in the co-evolved measurement harness (F5), not in frozen24.

**F4 — Coverage gaps in the frozen24 oracle leave contract requirements
without any discriminating arm.**

- Contract exit-2 condition "unsupported policy" (contract.md:15) has no
  arm; SUT raises `policy_schema`/`policy_regex` — untested.
- R20 ("unsafe input path": absolute, dotdot, empty, controls) is armed
  only by `receipt_override='../receipt.json'` — one dotdot arm of five
  named path classes; absolute/empty/control chars never exercised on any
  of the three path flags.
- R22 NUL-blob coverage is single-branch: `binary.bin` is skipped in
  `raw_hits` assertion, but no arm checks a *receipt that claims a NUL-blob
  hit* (the symmetric lie direction R07/R08 cover only for real hits).
- Blob-vs-worktree reading (contract requires Git-blob reads) is never
  discriminated: fixture worktree is always clean, so a SUT reading files
  instead of blobs would pass every arm. Refinement cases ('policy-change',
  'allowlist-change', 'symlink-identical') do force blob reads and would
  catch it — but those are co-evolved, post-implementation additions.
- R13's "measured revision mismatch" wording in contract.md covers two
  classes (unresolvable vs resolved-but-wrong-tree); only the unresolvable
  arm exists. The M3 revision-conflict guard (wrapper/argv/inner-commit
  disagreement) is exercised only by the refinement layer
  ('wrong-command-revision') and measure's `contradictory-entering-receipt`
  — again post-implementation, co-evolved.

**F5 — The measurement-time provenance chain is unpinned and drifting.**

- `measure-round22.py` executes `oracle-reconcile-v2.py` and
  `refinement-reconcile.py` as *worktree* files. The oracle is digest-
  verified against `requirements-v2.json` pins (verified: all four pin
  digests match). The refinement runner is *not* pinned — its
  `runner_sha256` is recorded post-hoc inside its own output, and
  `measure-round22.py` itself was still modified-uncommitted at my HEAD
  anchor (adding `safe_outputs` + the 'setup-leak' mutant). Whatever
  version of the harness happens to be on disk at measurement time is
  what runs; only its argv is captured, not its identity.
- The SUT is correctly bound: `measure-round22.py` requires
  `git show <rev>:tools/mori-retention-reconcile.py` to equal the executed
  bytes (`measured_code_not_committed`), and `--revision` is the measured
  commit. That binding is good. The weak link is everything around it.

### LOW / DISCLOSED-AS-SUCH

**F6 — Co-evolved refinements are honestly labeled but extensive.**

The LOG entry at 3985b3d explicitly labels the post-implementation layer
"co-evolved, not re-frozen24": the SUT gained receipt path binding
(`recorded_option` + `receipt_path_binding`) and a 4th selftest arm
(exact 0/1/2 finding coverage — previously only 3 arms, no MISMATCH arm),
`refinement-reconcile.py` grew to 18 discriminating controls, and
measurement adds 4 mutants including the denominator-swap 'wrong-population'
mutant that directly tests the v1/v2 distinction. All of this postdates the
v2 freeze and is disclosed as such. Honest, but it means a large share of
the observable discrimination (path forgery, symlink-same-bytes, revision
conflict, real-receipt agreement) comes from the unfreezeable-by-design
second tier; the frozen24 set alone does not cover it.

**F7 — Fixture expressiveness hides an R-class: the synthetic tree cannot
distinguish non-author and policy-path exclusion by count.**

`non-author.txt` has 1 hit and `policy.json` has 1 hit, so v1 and v2 give
identical R03 counts (5/1/4); only R04's identity list discriminates, and
only because 'non-author.txt' and 'policy.json' are different paths. A
fixture where the two paths carry equal-hit counts was fine here but is a
fragile coincidence — the discriminating arm on the real input is the
actual receipt, not the fixture. Additionally `fnmatch` glob semantics are
unexercised beyond a literal filename (no `*`/`?`/subdir pattern).

## Measured-input provenance — what I verified read-only

- Real receipt path `…/retention-floor.json` exists at `77a5bbe`, parse
  yields 95/86/4/5/0 exactly as `expected-real.json` expects; receipt is
  absent at `9fb1f91` (contract requires it only at input revision — correct).
- `9fb1f911…` (receipt `measured_revision`) is an ancestor of `77a5bbe`
  and HEAD; `merge-base --is-ancestor` verified.
- Policy/allowlist blobs byte-identical between `9fb1f91` and HEAD —
  the "input-tree mismatch" preflight would evaluate cleanly on the real arm.
- Frozen hash bindings: `requirements-v2.json`'s `contract_sha256`,
  `correction_sha256`, `fixture_builder_sha256`, `oracle_sha256` all match
  the committed blobs at e2f549b. `expected-real.json` itself is *not*
  digest-pinned by requirements-v2 (it postdates it) — another F1 detail.
- Entering-capability-absence control in `measure-round22.py` is real:
  `git cat-file -e BASE:tools/mori-retention-reconcile.py` must fail;
  verified the tool does not exist at `77a5bbe`.
- SUT reads all three inputs via `git ls-tree`/`cat-file` blobs at the
  resolved revisions, never the worktree (`committed()`/`scan()`), strips
  `GIT_*` env, uses `--no-replace-objects` and `--end-of-options` —
  addresses the replace-ref/env substitution class CriticTrust raised for
  tree content (replace-ref ancestry forgery is also neutralized since
  both the receipt read and the merge-base check run under the flag).

## Commit order (verified)

```
df880b4 10:51:49  freeze contract + requirements-v1 + wave1 dispatch
306e06e 10:52:31  retain context checks
e825c7f 10:54:32  freeze fixture-builder v1 + oracle v1 (+ live wave1 artifacts)
e2f549b 10:55:59  CORRECTION: denominator-correction + v2 frozen triple
8cb4afb 11:02:25  SUT + expected-real.json + refinement runner  ← F1, F2
3985b3d 11:09:37  SUT path-binding hardening + refinement→18 + measure harness
```

Ordering contract clause is *nominally* satisfied for requirements.json and
the synthetic oracle (e825c7f < 8cb4afb), corrected once before
implementation (e2f549b < 8cb4afb), and *nominally-but-weakly* satisfied
for real-input expected values (same commit as the SUT — F1).

## Residual risk

1. If `expected-real.json` is presented downstream as "frozen before
   implementation," that claim is false as-committed; the honest label is
   "authored alongside the implementation it measures."
2. `contract.md` remains self-contradicting on the exclusion definition;
   any consumer that re-derives expectations from contract text alone will
   land on the v1 (wrong) denominator.
3. The measured real-receipt agreement, whenever run, will prove the SUT
   recomputes the gate's population under committed bytes — it cannot
   attest the original r21 execution, which the knowledge note already
   discloses (`receipt_authenticity:"unattested"` is present in SUT output;
   honest).
4. All verdict-forming remains unrun at this anchor; no frozen24 pass count,
   no mutant kills, no real-reconciliation output exists in `evidence/`.
   Anything reported later must be tied to the measured commit's blob, and
   the harness byte identity should be committed before the run, not after.

## Verification gaps (my own scope)

- I did not execute the oracle, selftest, refinement runner, or measurement
  driver (read-only seat; wave rules forbid verification runs).
- Sibling seats' reports were sampled only for collision avoidance
  (CriticAdmission F1-adjacent, CriticTrust substitution, RequirementTrace
  coverage); their findings may overlap this report's F4/F5 partially.
- The in-flight wave-2 attack reports in `build/` may already duplicate
  F3/F4 observations; I did not exhaustively diff all 40+ reports.
