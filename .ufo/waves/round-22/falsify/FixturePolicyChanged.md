# FixturePolicyChanged — falsification of frozen v2 variant `policy-changed` (R15)

Seat MoriR22.FixturePolicyChanged (critic). This was static analysis only. I executed no fixture, oracle, test, build or tool. I did run read-only `git -C` plumbing (`log`, `show`, `merge-base`), `sha256sum`, and `jq`/`rg` over the retained JSON evidence. No installs or updates were made.

## Inputs, bound by hash

| Input | sha256 | Binding |
|---|---|---|
| `denominator-correction.md` | 968945b2…24f9 | equals `requirements-v2.json.correction_sha256` |
| `contract.md` | 1658c390…a1 | equals `contract_sha256` |
| `frozen/fixture-builder-v2.py` | 1b3e16f7…15d1 | equals `fixture_builder_sha256`; blob at e2f549b has the same hash; e2f549b is an ancestor of the implementation commit 8cb4afb |
| `oracle-reconcile-v2.py` | dcd1c7c6…adb | equals `oracle_sha256` |
| `tools/mori-retention-reconcile.py` (shipping) | d6870fb6…0ce7 | equals `tool_sha256` in `evidence/measure1/after-observed.json` and `refinement-observed.json` |

## Verdict

R15 passes for the right reason in the current shipping tool. The frozen oracle cannot prove that, and the fixture itself carries two independent setup causes. This is a fixable coverage defect, not a tradeoff the judge must reject.

## What the variant does (builder lines 97–99)

- Commit 1 is the measured revision M. It holds `policy.json` with bytes P.
- After the receipt is written, the builder appends `\n`, so `policy.json` becomes P+`\n`. That change and `receipt.json` land together in commit 2, the input revision I. M is I's parent, so the ancestry check holds.
- There is no restoration step. The worktree stays at P+`\n`, which equals I.
- The change is byte-only and semantically null: the JSON parses identically. That kills any implementation that compares parsed policy instead of bytes. This is a real strength.

## Counterexample 1 (main): the fixture confounds the target reason with an unrelated setup error, and the frozen oracle cannot tell them apart

Evidence:
- The receipt stdout `policy_sha256` is `digest(files[POLICY])`, which is sha256(P) (builder line 73). The policy blob at I is P+`\n`.
- The fixture therefore carries two independent exit-2 causes:
  - The target cause: bytes at I differ from bytes at M. The shipping tool checks this at lines 164–165 and reports `policy_changed`.
  - A second cause: the receipt digest no longer matches the input blob. The shipping tool checks this at line 187 and reports `receipt_policy_digest`.
- The oracle's R15 arm (`oracle-reconcile-v2.py:54`) asserts only exit 2, `finding_id == RETENTION_RECONCILIATION_SETUP` and empty stderr. It has no `error` predicate.
- Static mutant: delete the `policy_changed` guard at shipping lines 164–165. Every check before line 187 is identical to the `valid` variant, which R01 shows passing. So the mutant reaches line 187 and exits 2 with `receipt_policy_digest`.
- Result: frozen R15 still passes under that mutant. R15 cannot fail when the very guard it names is deleted.

`measure-round22.py` lines 77–82 run four mutants: count-only, false-clearance, wrong-population and setup-leak. None of them targets this guard, so nothing in the measurement kills it.

Asymmetry with R16: the allowlist has no receipt-side digest. Deleting the `allowlist_changed` guard would make `allowlist-changed` reconcile with exit 0 (the rows parse identically), so R16 fails under that mutant. R16 is fail-capable; R15 is not. [INFERENCE: static trace, not executed.]

## Is the target reason distinguishable in practice?

Yes, but only outside the frozen 24:
- The retained frozen run at tool d6870fb6 shows `policy-changed` returning exit 2 with `{"error":"policy_changed",...}`, empty stderr, and only the five sanitized keys. The same holds in the restored control and in all four mutant observations.
- `refinement-reconcile.py` case `policy-change` asserts `error == 'policy_changed'`. Its retained observation is a pass, and it kills the guard-deletion mutant above, because that mutant would report `receipt_policy_digest`.
- The refinement case inherits the same confound: it leaves `value['policy_sha256']` stale. It discriminates only because the shipping tool runs the byte-equality check before the digest check.
- Remaining gap: a mutant that replaces the M-to-I byte comparison with a receipt-digest-to-I comparison, but still raises `policy_changed`, passes both harnesses. No control rebinds the receipt digest to the changed bytes. Such a mutant would apply the current policy historically, which the contract forbids ("mismatches unevaluable, not silently current policy applied historically"). Shipping scan line 194 uses classes parsed from I's policy over M's tree. That is safe only because of the guard at lines 164–165.

## Are the expected identities and partitions true for this variant?

- Raw and partition counts are true at M. The counts are raw 5, excluded 1, scanner 4, raw unallowlisted 1. The expected policy and scanner hit lists also hold.
  - The policy self-hit is the `"synthetic"` line. The regex literal `[R]22_SAMPLE` does not match itself. `binary.bin` is skipped because it contains NUL.
  - The five raw hits partition into 3 allowlisted (policy.json plus two in allowed.txt), 1 unallowlisted and 1 non-author. That is the identity-based split the correction requires; the policy file is scanned normally and is not excluded by path.
  - They are also invariant at I, because the appended newline adds only a trailing empty line with no hit and no line-number shift.
  - Consequence: this variant cannot separate scanning M from scanning I. Other seats own that axis.
- `expected_policy_sha256` is false for this variant's input revision. It is sha256(P), the M blob. The retained run shows 38ec0221…43b6, identical to the `valid` variant. The I blob is sha256(P+`\n`). R15 does not consume this field, and R24 uses only `valid`, so no pass is affected. But the retained `runs[].fixture` provenance mislabels this variant's input-policy digest.
- `expected_receipt_sha256` and `expected_allowlist_sha256` are true.
- `expected_policy_hits` is a name carried over from v1. Its value is the non-author identity, which is correct under the correction. Only the name is misleading.

## Mutation and restoration provenance

- The mutation is one commit after M. Measured and input revisions are recorded, at 78ae21d0… and a8e8b5df… in the retained run.
- The fixture dictionary does not record the mutation, nor the digest of the input-revision policy. The mutation can be recovered only from the `fixture_files` object-database digests and the workspace archive.
- No fixture restoration exists or is needed. `restored-control` in the measurement refers to restoring the tool source, not the fixture.

## Prior build note AttackR15.md, re-checked against current source

- CE1 (missing allowlist `rule`): obsolete. v2 builder line 59 sets `rule='b'`, and shipping `allow_rows` requires a, b or c.
- CE2 (no reason assertion): still true for frozen R15. It is partly mitigated by the refinement case's `error` assertion.
- CE3 (forged-digest control): still uncovered in both harnesses. The shipping tool does implement the M-to-I byte check, so this is a coverage gap, not a defect.
- CE4 (semantic-change precedence): the shipping tool checks bytes before parsing or recomputing (lines 164–166 run before 194). No fixture exercises it.
- CE5 (worktree reads): `dirty-worktree` in the refinement harness already discriminates worktree readers. The shipping tool reads blobs only.
- Proposed code `policy_bytes_changed`: the shipped code is `policy_changed`.
- Path-binding ambiguity: resolved. Shipping lines 172–182 bind the receipt argv paths, and refinement case `policy-path-substitution` exercises the binding.

## Impacted axes

- **Calibration**: the frozen R15 pass cannot be attributed to the guard it names, and the 24/24 count overstates R15's discriminating power.
- **Depth**: the historical-policy-application path is unguarded by any control that rebinds the receipt digest.
- **Operability**: no regression.

## Smallest safe correction

Do not edit the frozen v2 builder or oracle; they are hash-bound in `requirements-v2.json`. Instead, append to the co-evolved, non-frozen harnesses:

1. Add a `refinement-reconcile.py` case `policy-change-rebound-digest`. It applies the same policy +`\n` mutation and also sets `value['policy_sha256']` to the sha256 of the new bytes. Expect exit 2, `RETENTION_RECONCILIATION_SETUP`, `error == 'policy_changed'`. This isolates the M-to-I byte comparison. Static trace: the shipping tool returns `policy_changed` here, and a digest-only mutant returns exit 0.
2. Add a `measure-round22.py` mutant that deletes the `policy_changed` guard at shipping lines 164–165, with kill basis "refinement". Record it as not killed by frozen R15.
3. In claims, describe frozen R15 as exit-class evidence only.

The checks L1 should run after integration are `refinement-reconcile.py` and `measure-round22.py`.
