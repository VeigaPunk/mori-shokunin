# R13 static falsification

## Finding

**Source-level behavior: holds, with high confidence. Oracle coverage: partial.** I found no static counterexample in the delivered tool for returning setup/exit 2 on an unresolvable measured revision or on the explicit revision-consistency conflicts. The frozen R13 run itself proves only the unresolvable case; it does not exercise the consistency-conflict branches.

## Branch trace

- The frozen contract defines R13 as measured-revision mismatch/unresolvable returning 2: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-22/contract.md:19` and `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-22/frozen/requirements-v2.json:4-30`.
- CLI call path in `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-retention-reconcile.py`: `main` calls `check` (lines 263-278; check call at 271). `check` first resolves its input revision (155), then requires the receipt's measured value to be a full object ID resolving to itself (162-163). The resolver delegates to Git and turns nonzero Git status into `Invalid` (53-66). Thus an unresolvable measured value reaches the `Invalid` setup handler in `main` and returns 2 (272-276).
- For resolvable values, `check` next requires the measured commit to be an ancestor of the selected input commit (164-165). After that, it independently requires the receipt's recorded `--rev` to equal the wrapper's measured value (178) and the inner retention result's commit to equal that same value (187). Each failed `require` raises `Invalid`, which the same `main` handler maps to setup/2. This ordering handles a non-ancestor before the later consistency comparisons; the explicit consistency branches are present in source.
- The `invalid-revision` arm in `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-22/frozen/fixture-builder-v2.py:88-93` puts forty zeroes in both the wrapper measured value and inner commit, while leaving the recorded command `--rev` at the original valid measured commit. The oracle invokes this fixture and checks exit/finding/stderr in `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-22/oracle-reconcile-v2.py:30-46,54`. The SUT fails during measured-value resolution, before checking the stale recorded `--rev` or inner commit. This is an R13 unresolvable-value test, not a revision-conflict test.
- R14's `diverged` arm uses a resolvable unrelated commit, but the ancestry check fails before the recorded-argument or inner-result consistency branches. It therefore does not cover those branches either.

## Smallest missing case and red control

The smallest counterexample to **complete R13 test coverage** (not to the source behavior) is a valid red fixture with one revision-consistency field changed while the rest remains valid: for example, keep the wrapper's measured commit and recorded `--rev` valid, but change only the inner result commit to a different resolvable commit. With the measured commit still an ancestor and policy/allowlist unchanged, the command reaches the inner-result comparison at line 187 and should return setup/2. No builder variant or oracle assertion creates this case. A corresponding one-field change to the wrapper's recorded `--rev` would exercise line 178 instead.

The oracle does have a valid red control: R02 runs the default fixture and requires red retention counts with privacy clearance false while reconciliation returns 0. However, it is a separate fixture/invocation from R13, not a paired same-repository/same-input-revision red control for the revision-conflict arm. The builder creates each variant under its own root, and R13 changes the measured value such that resolution aborts before the intended conflict branch. The shipping tool's `--selftest` also has a red valid invocation, but its negative receipt mutates hit accounting, not a measured-revision relation.

## Method and limits

Static source review only; no commands/tests were run. The `lsp` device is not mounted (`xd://lsp` returned unavailable), so I used literal search to locate relevant symbols and read their source sections; no semantic LSP result is claimed. I did not use prior authored reviews as verification. No source-level behavior outside R13 was evaluated.