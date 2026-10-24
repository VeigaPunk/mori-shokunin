# FixtureInvalidRevision — frozen v2 `invalid-revision` variant (R13) falsification

Seat MoriR22.FixtureInvalidRevision (critic). Static only: no fixture, oracle, SUT, test, build or formatter execution; no production edits; no delegation; no installs or updates (none needed). The only commands run were `sha256sum` and read-only `git -C <lane> log/status/diff --stat/cat-file -t/ls-tree`. I read the already-retained measurement evidence; nothing was re-measured. No matched text appears below.

## Inputs and bindings (verified)

| artifact | sha256 / commit | binding |
|---|---|---|
| `denominator-correction.md` | `968945b2…24f9` | equals `requirements-v2.json.correction_sha256` |
| `contract.md` | `1658c390…21a1` | equals `contract_sha256` |
| `frozen/fixture-builder-v2.py` | `1b3e16f7…15d1` | equals `fixture_builder_sha256`; committed in `e2f549b`, before SUT `8cb4afb` |
| `oracle-reconcile-v2.py` | `dcd1c7c6…adb` | equals `oracle_sha256`; same `e2f549b` |
| `frozen/requirements-v2.json` | `48ea2369…bea` | equals `after-observed.json.requirements_sha256` |
| `tools/mori-retention-reconcile.py` (current shipping) | `d6870fb6…0ce7` | equals `tool_sha256` in `evidence/measure1/after-observed.json` and `refinement-observed.json` |

So the frozen inputs predate the implementation, and the retained measurement ran against exactly the current shipping source.

## Variant mechanics (builder lines 75–100)

- `wrapper` is built with `argv … '--rev', measured …` (line 77). The `invalid-revision` branch (line 88) then sets `wrapper['measured_revision']='0'*40` and `result['commit']='0'*40`. It never touches `wrapper['argv']`. Line 93 re-serializes `stdout` from the mutated `result`.
- The measured tree, policy, allowlist and input commit are byte-identical to `valid`. Only `receipt.json` differs, at those two fields. Because author and committer dates and identities are fixed, the true measured commit is deterministic across same-content variants. Every retained run shows `a8e8b5df…6a34`. `rev` is a child of that commit.
- Mutation provenance and restoration: each `make()` builds fresh local objects and its own fixture directory. The branch reassigns scalar keys only, so the shared `hits`, `allowed` and expected lists are not aliased. Nothing needs to be restored. (The aliasing does affect the `inject`, `digest` and `line` variants, but none of them consult the expected lists, so it is out of scope here.)
- Expected identities and partitions returned for this variant are true for the measured tree, checked statically and against the retained fixture record: raw 5, consisting of 1 policy-file hit (allowlisted, scanned normally), 2 hits in allowed.txt, 1 in unallowed.txt and 1 in non-author.txt. That gives excluded = the single non-author identity, scanner 4, and raw_unallowlisted 1. This matches the correction. R13 consults none of these values.
- Provenance gap: the returned `measured_revision` field is the mutated claim (the all-zero value, recorded at after-observed line 1550), not the true commit. The evidence row therefore never shows that the receipt's argv `--rev` still names the true measured commit. That fact can only be recovered by opening the receipt blob or by the determinism argument above.

## Verdict

**The target reason cannot be told apart from an unrelated setup error, either at the oracle level or from the SUT's output.** The `RETENTION_RECONCILIATION_SETUP` result for R13 is real, and white-box reading of the SUT shows it reaches the revision check first. However, the frozen R13 pass shows only that the run exited 2 for some reason.

### Counterexample 1 (calibration, blocking for any attribution claim): identical bytes for R13 and R14

The oracle records R13 with no predicate. It checks only exit 2, `finding_id`, and empty stderr. The SUT turns a nonexistent measured OID into `git_read_failed`. The reason is that `resolve()` → `git()` raises `Invalid('git_read_failed')` before the outer `require(…,'receipt_revision')` can run (reconcile.py lines 59, 64, 161). Line 161's `receipt_revision` label is therefore never emitted for an unresolvable OID. The same code is produced when merge-base exits 1 (not an ancestor) or exits with another error, when `--rev` fails to resolve, and when ls-tree or cat-file fails.

Retained evidence (after-observed.json): the invalid-revision stdout at line 1557 and the diverged stdout at line 1627 are byte-identical. Both read `{"error":"git_read_failed","finding_id":"RETENTION_RECONCILIATION_SETUP",…}`.

Concrete unrelated-setup counterexample [INFERENCE, not executed]: the builder strips only some `GIT_*` variables (`GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_CONFIG_COUNT`, trace and config-key variables). It inherits `GIT_OBJECT_DIRECTORY` and `GIT_ALTERNATE_OBJECT_DIRECTORIES`, whereas the SUT drops all `GIT_*`. With `GIT_OBJECT_DIRECTORY` set in the operator environment, fixture objects land outside `.git/objects`. The SUT's first `resolve(--rev)` would then fail, giving `git_read_failed` on every variant. R13 (and R14) would pass with byte-identical stdout while R01 fails. In the retained run R01 passed, so the aggregate was not masked. The R13 row on its own would not have revealed this.

R13 does not enforce the sanitized-code clause either. `mutant-setup-leak` (which adds a matched-text `detail` field to every SETUP payload) left R13 `pass:true` (mutant-setup-leak-observed.json line 841). That mutant was killed only by the post-hoc all-arm output-safety check in `measure-round22.py`, not by R13.

### Counterexample 2 (fixture confound): two independent defects in one arm

Because argv `--rev` is not co-mutated, the variant carries two independent defects:
- the wrapper and inner commit are unresolvable;
- argv `--rev` differs from `measured_revision`.

A conforming SUT that checks the argv binding before resolvability would emit `receipt_revision_conflict` and pass R13 without ever exercising the "unresolvable" clause. The shipping SUT checks resolvability first (line 161, before line 184), but only reading the code shows that. The defence in depth also makes R13 insensitive to deleting the resolvability clause: removing `resolve(...)==measured` lets the null OID fail at merge-base, and removing that lets it fail at `committed(measured, …)` ls-tree. Each produces the same `git_read_failed` [INFERENCE from git's documented merge-base behaviour for invalid names, S046]. The variant is not a minimal mutation.

### Coverage now outside the frozen 24 (re-verified against current source and retained evidence, not copied from build notes)

- "Mismatch" half: `refinement-reconcile.py` `inner-commit-split` (inner commit differs from wrapper and argv; expects `receipt_revision_conflict`) and `wrong-command-revision` (argv only) both passed against tool `d6870fb6` (refinement-observed lines 598 and 123).
- Revision form: the shipping SUT requires lowercase full-hex `OID` plus literal equality with `rev-parse --verify --end-of-options X^{commit}`. Refinement `measured-tag` (expects `receipt_revision`) passed (line 623) and guards the equality clause. Abbreviated, `HEAD~n`, empty and uppercase forms are rejected statically by the regex or the equality check. A tree OID fails `^{commit}` → `git_read_failed`.
- The build-wave AttackR13 findings that applied to v1 are resolved in v2 and the current source: the allowlist `rule` field is now `'b'`; the revision is validated before scanning; dirty-worktree is covered by the refinement `dirty-worktree` control and by blob-only reads.
- **Still unguarded:** no control anywhere (frozen or refinement) asserts an error code for a *consistent* nonexistent measured OID, where wrapper, inner and argv all agree. Even if one did, the only code available is `git_read_failed`, which the refinement runner also expects for `diverged-consistent`, `cousin` and `head-cousin`.

## Impacted axes

- calibration: R13 overstates attribution, since any exit-2 counts as a pass.
- depth: "unresolvable" and "not ancestor" are merged into one diagnostic.
- operability: an operator cannot tell a bad receipt revision from a broken repository or environment.
- coverage, freshness, adjacency: no change.

## Fixable defect versus judged tradeoff

- **Fixable (SUT, diagnostic only; exit semantics unchanged).** In `check()`, wrap the measured-revision `resolve` so that any `Invalid` becomes `receipt_revision`. Wrap `merge-base --is-ancestor` so that exit 1 becomes `receipt_not_ancestor` and any other nonzero becomes `receipt_ancestry_unevaluable` (S046). Update the refinement expectations for `diverged-consistent`, `cousin` and `head-cousin` in the same change, then re-measure under the new tool hash.
- **Fixable (non-frozen control layer, no postdiction).** Add a refinement case `unresolvable-consistent`: set wrapper, inner commit and argv `--rev` all to one well-formed nonexistent OID; expect exit 2 with the error `receipt_revision`; require the five-key SETUP payload. This exercises the clause in isolation and removes the confound without editing the frozen builder.
- **Fixable (builder hygiene, v3 only, disclosed as a deviation).** Strip every `GIT_*` except the fixed identity and date variables, matching the SUT. Also co-mutate argv `--rev` in `invalid-revision`, or rename the arm as a two-defect arm.
- **The judge must reject** any claim that the frozen R13 pass demonstrates the unresolvable-revision check, or that R13 covers the "mismatch" half. The judge need not reject C1 on R13 grounds. Exit-2 behaviour holds, and attribution rests on white-box reading plus the non-frozen refinement controls, which should be cited as such.

## Smallest safe correction

Keep the frozen v2 artifacts byte-unchanged. Make the SUT emit `receipt_revision` when the measured OID fails to resolve, and distinct codes for the two ancestry outcomes. Add the refinement arm `unresolvable-consistent`, with its error code asserted and argv co-mutated. Report R13 as "exit-2 class; attribution via refinement controls" until both are measured.

Checks for L1 after integration: the frozen oracle, the refinement runner and the measured-mutant run against the new tool hash.

No tool installs or updates were performed.
