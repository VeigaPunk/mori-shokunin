# FixtureSymlink — frozen v2 fixture variant `symlink` (R21) and its oracle predicate

Seat: MoriR22.FixtureSymlink (critic, static only). No fixture, oracle, tool, test or build was executed. No tool was installed. Evidence comes from file reads, `sha256sum`, and read-only `git -C` plumbing (`log`, `status`, `diff`, `ls-tree`, `cat-file -s`, `diff-tree`, `rev-list`, `ls-files`) on the lane and on the already-retained scratch fixture repos. No matched text is reproduced; the synthetic class token is named only as "the synthetic token".

## Bound inputs (verified)

The current bytes match the hashes frozen in `frozen/requirements-v2.json`:

| file | sha256 | last commit |
|---|---|---|
| `frozen/fixture-builder-v2.py` | 1b3e16f7… | e2f549b |
| `oracle-reconcile-v2.py` | dcd1c7c6… | e2f549b |
| `contract.md` | 1658c390… | — |
| `denominator-correction.md` | 968945b2… | — |

- Shipping SUT `tools/mori-retention-reconcile.py` has sha256 d6870fb6…, last touched by 3985b3d. This equals `tool_sha256` in `evidence/measure1/summary.json`.
- Lane HEAD is 5888b56.

## What the symlink variant actually builds

The relevant builder line is `fixture-builder-v2.py:95`: `(root/RECEIPT).symlink_to('allowed.txt')`, followed by `git add --all` and commit.

- **Commit 1 is the measured revision.** It is identical to the valid variant: `policy.json`, `allowed.txt`, `unallowed.txt`, `non-author.txt`, `binary.bin` and `allowlist.json`, all mode 100644.
- **Commit 2 is the input revision.** It adds only `receipt.json`, as mode 120000.
- Confirmed on the retained fixture `.scratch/round22/measure1/after-fixtures/symlink` at input revision 15842148:
  - `ls-tree` shows `120000 blob 8b38e5de… receipt.json`.
  - `cat-file -s` gives 11 bytes, which is the link-target filename.
  - `diff-tree` shows commit 2 adds only `receipt.json`.
  - `rev-list --count` gives 2.
- **No confounder.** Policy and allowlist bytes are identical at both revisions, the measured revision is a valid ancestor, and every path is safe. The only defect in this fixture is the symlink.
- **Expected-field truth.** `expected_receipt_sha256` is `None` for this variant. That is correct: a worktree `read_bytes()` would follow the link and hash `allowed.txt`'s content, which is not the committed blob. The other `expected_*` fields describe the valid measured tree and are not used by R21. I verified them statically against the valid measured tree:
  - Hits: `policy.json` has one hit on its `synthetic` line. Its `[R]22` regex line does not self-match, because `]` breaks the contiguous run. `allowed.txt` has 2 hits with the same line digest, `unallowed.txt` has 1, `non-author.txt` has 1, and `binary.bin` is skipped because it contains NUL.
  - Totals: raw 5, excluded 1 (the non-author identity), scanner 4. The allowlist has 2 deduplicated rows with `rule=b`.
  - This matches the correction: exclusion is by `non_author_paths_glob`, and the policy file is scanned normally. `expected_policy_hits` is a legacy key name, but it holds the non-author identity, which is the correct semantics.

## SUT path for this input (shipping source)

1. `check()` resolves the revision, then validates all three paths with `safe_path`, then calls `committed()` for the receipt first.
2. `committed()` runs `ls-tree -r -z --full-tree <rev> -- receipt.json` and requires mode `100644` or `100755` with kind `blob` (`mori-retention-reconcile.py:84-85`). Otherwise it raises `input_not_regular` before reading or parsing the blob.
3. The retained runs record exactly that. The R21 run's stdout in `after-observed.json:2193` and `restored-observed.json:2193` has `error=input_not_regular`, exit 2, and empty stderr.

The target reason is reached first and nothing else fires. In the SUT, the outcome is caused by the symlink.

## Counterexample: the frozen R21 predicate cannot tell the target reason from unrelated setup errors

`oracle-reconcile-v2.py:58` reads `record('R21','symlink',2,'RETENTION_RECONCILIATION_SETUP')`. The pass condition (`:42`) is only exit==2, `finding_id`==SETUP and stderr==''. There is no `error` code check, no output key-set check, and no leakage check. R23's leakage predicate covers only the valid variant.

The fixture's link-target blob is the 11-byte filename, which is not JSON. So each of the following implementations also passes R21:

- **C1, mode-blind.** Delete or relax the mode check at `:85`, for example by accepting `120000`. The tool then reads the 11-byte blob, `parse()` raises `invalid_json`, and it exits 2 with SETUP, so R21 passes. No other frozen variant contains a symlink, so this mutant would score 24/24 on the frozen oracle [INFERENCE: static. No such mutant was run, and the measure1 mutant set of count-only, false-clearance, wrong-population and setup-leak contains no mode-gate mutant].
- **C2, symlink-following.** A tool that reads the worktree or uses `cat-file --follow-symlinks` gets `allowed.txt`'s text content, which is not JSON. It fails with `invalid_json` and R21 passes.
- **C3, any unrelated setup failure.** Examples are a git failure or a schema error raised before the input checks. Any of these also yields exit 2 with SETUP and passes R21.
- **C4, leaky setup output.** This one was observed. The retained `mutant-setup-leak-observed.json` R21 row shows `pass:true` while its stdout carries an extra `detail` field containing synthetic matched text. `summary.json` records that this mutant got `unmet:0` on the frozen 24 and was killed only by the out-of-oracle `all-arm-output-safety` check.

Conclusion: the target reason is distinguishable in the retained evidence, because the `runs[].stdout` error code is preserved. It is not distinguishable by the frozen R21 pass/fail. A frozen R21 pass shows only "some setup error, no stderr". It does not show "a committed symlink was rejected". This confirms that the AttackR21 superficial-pass concern still holds against the current frozen oracle.

## Partial mitigation already retained, outside the frozen 24

`refinement-reconcile.py:76-78`, case `symlink-identical`, stages `receipt.json` as mode 120000 using the OID of the valid receipt. This is AttackR21's F1, applied to the receipt. The case asserts:

- `expected_error == input_not_regular`,
- the exact setup key set (`:103`),
- a result of pass in `refinement-observed.json:145-151`.

Read-only `ls-tree` on its retained fixture (rev 580bb62a) confirms `120000 blob 4de1712c… receipt.json`, with policy and allowlist at 100644.

This arm would kill C1 and C2, because a mode-blind tool reconciles a valid receipt and exits 0. It is refinement evidence, though, not a frozen requirement.

Remaining uncovered by any arm. All of these are handled correctly by the code (`committed()` is also used at the measured revision), but they are unexercised:

- Policy or allowlist inputs as symlinks at the input revision.
- A mode change only at the measured revision (AttackR21 F2).
- A symlinked parent directory (F4). [INFERENCE] `ls-tree` returns no row, which gives `missing_input_blob`.
- The over-application guard (F5): a non-input mode-120000 blob containing a hit must still be counted. The SUT scan skips only `kind!=blob`, which matches gate `:199`, but no fixture places a symlink in the measured tree.

`input_not_regular` is also shared with gitlink (160000) inputs. It is a sanitized code, but not specific to symlinks. That is a tradeoff, not a defect.

## Mutation and restoration provenance

- **Mutation.** The mutation is single and isolated (commit 2 only). It is retained as the loose object `symlink/.git/objects/8b/38e5…` and digested in `after-observed.json:656`.
- **Oracle digest gap.** The oracle's `fixture_files` excludes worktree symlinks by design (`is_file() and not is_symlink()`), so the oracle's own digest map has no entry for the link itself.
- **Link target in the archive.** The link target is preserved in `synthetic-workspaces.tar.gz`, as symlink members `*/symlink/receipt.json -> allowed.txt` for the after, restored and all four mutant runs. `measure-round22.py:134-135` byte-compares `linkname` against the archive.
- **Restoration.** `restored-control` reran the frozen oracle with the original tool. `mutations_ok` requires that tool's sha256 to equal the source. The restored R21 stdout is identical to the after run.
- **Provenance gap.** `synthetic-workspaces.tar.gz` (sha256 575435b6…, matching `summary.json`) is untracked at HEAD 5888b56. `git status` shows `??` and `ls-files --error-unmatch` fails. The committed summary binds a hash whose bytes are not in Git, so the symlink fixture's link-target provenance currently rests on an uncommitted file plus the digested loose object.

## Impacted axes

- **Calibration (C1).** A frozen R21 pass overstates what it discriminates. Mode-blind (C1), symlink-following (C2), unrelated-setup (C3) and leaky-setup (C4) tools all pass it.
- **Depth.** Rejection of policy and allowlist symlinks, rejection of a measured-revision-only mode change, and F5 population preservation are all unexercised.
- **Provenance/freshness.** The archive bytes are untracked.
- **Not impacted.** The expected identities and partitions are true. The SUT's actual outcome is caused by the symlink.

## Smallest safe correction (no frozen-file edits)

1. Keep the frozen R21 bytes unchanged. When judging, record its pass as "setup-class only, non-discriminating against a mode-blind tool", and cite the refinement `symlink-identical` row as the discriminating evidence.
2. Add refinement arms, not frozen ones:
   - `symlink-identical` for `policy.json` and `allowlist.json`, both expecting `input_not_regular`.
   - A policy symlink at the measured revision only, with identical blob bytes at the input revision as a regular file (expect `input_not_regular`).
   - An F5 arm: a non-input 120000 blob in the measured tree carrying one hit and a matching receipt. Expect exit 0, `receipt_match` true, and raw count increased by one.
3. Add a `mode-blind` mutant to `measure-round22.py`, replacing `mode in (b'100644',b'100755')` with a version that also accepts `b'120000'`. Its kill basis must be stated as refinement `symlink-identical`, not frozen24. Static expectation: it survives the frozen 24 and is killed by the refinement.
4. Commit `evidence/measure1/synthetic-workspaces.tar.gz`, or record its absence explicitly, so that the summary's archive hash binds to bytes that are in Git.

Checks for L1 after integration: rerun refinements together with the new mutant and restored control. Confirm the mode-blind mutant shows frozen24 `unmet==0` with the refinement killing it, and confirm the archive is tracked with sha256 equal to the summary.
