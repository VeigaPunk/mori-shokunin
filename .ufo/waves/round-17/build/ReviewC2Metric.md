# ReviewC2Metric — C2 operability measure and controls

Date: 2026-10-20. Scope: assess whether the paired `failed jj sandbox assertions` comparison is a defensible C2 measure, identify its controls, and record safe live evidence. Axes: **C2 behavior** (branch-anchored census), **measurement validity** (paired, attributable failures), and **safety** (no lane mutation).

## Finding — Medium: a raw failed-assertion count is not, by itself, an honest operability score

It is defensible only as a **narrow differential regression result** for the C2 behavior, not as a general measure of lane operability or jj health. Contract C2 specifies running the gate against the entering census and the delivered census (`.ufo/waves/round-17/contract.md:81-94`). The implementation assignment asks for real jj-colocated sandboxes, isolated configuration, and per-case assertions (`.ufo/waves/round-17/wave1-dispatch.json:482-483`; the full JjGate prompt is in `wave1-spec.json:22-31`). Report outcomes by case and assertion for both revisions; do not report only `failed_before - failed_after`. A scalar can hide a newly broken control offset by a fixed regression, and a skipped/capability-absent case is not a pass. [INFERENCE]

The valid expected pattern is: the predeclared C2 regression assertions fail on the exact entering census and pass on the delivered census; every control passes on both; the same sandbox construction, input state, and assertion inventory are used for both. Require the manifest to show per-case `pass|fail|skip`, expected result, and assertion identity, plus separate target-regression and control totals. The gate assignment already requires per-case assertions and a failed count; preserve that detail in the result rather than treating the aggregate as the evidence.

The regression assertions should establish the intended differences:

- **HEAD ahead of the branch / jj commit without moving the bookmark:** entering behavior can credit the off-branch `HEAD` commit; delivered behavior should emit `HEAD_BRANCH_MISMATCH` and must not credit that commit as branch progress. This is directly motivated by the measured HEAD/bookmark divergence in `JjAuditMori.md:62-77` and census use of `HEAD` in row 9 at `tools/mori-census.sh:2194-2207`.
- **Lane committer with a different ambient author, on the branch:** delivered behavior should emit `LANE_AUTHOR_MISMATCH`; entering behavior has no such finding. The predicate is deliberately narrow: post-launch, branch commit, lane committer identity, different author (`contract.md:88-90`). Audit evidence shows why committer identity alone did not prove lane author identity (`JjAuditMori.md:79-98`).
- **Report committed only on the off-branch `HEAD`:** entering behavior can call it closed because `ps_report_closed` checks `HEAD:<path>` and logs from default `HEAD`; delivered behavior must leave it open because closure is branch-anchored (`tools/mori-census.sh:2092-2109`; C2 contract `:85-87`).

## Controls that must pass on both entering and delivered census

1. **Helper-shaped jj commit control:** `metaedit --update-author`, commit, then move the bookmark. Both versions should give the established lane-progress result, with neither new mismatch finding. The JjGate prompt explicitly names this as a control (`wave1-dispatch.json:482-483`); the prior sandbox trial observed lane author and committer identity after the helper-shaped commit (`JjTrialMori.md:92-115`). This is also the control showing a detached HEAD *at* the branch tip is not itself a mismatch.
2. **Detached HEAD at the branch tip:** both versions should preserve the existing verdict and emit no `HEAD_BRANCH_MISMATCH`; detachment alone is not divergence. The gate prompt names this control (`wave1-dispatch.json:482-483`).
3. **Plain attached git lane at the branch tip:** identical verdict and no new mismatch findings on either version; explicitly named in the gate prompt (`wave1-dispatch.json:482-483`).
4. **Report present and committed on the branch after launch:** both versions should retain the existing row-6 closure result. This is the positive counterpart to the off-branch-only regression case; branch anchoring must not break ordinary closure (`tools/mori-census.sh:2092-2109`).
5. **No false `LANE_AUTHOR_MISMATCH`:** a branch commit whose committer is not the lane identity must not trigger this finding; similarly, a properly lane-authored/helper-shaped commit must not trigger it. This checks the contract's committer-qualified condition rather than simply flagging every author mismatch (`contract.md:88-90`). [INFERENCE]

The first three controls are explicitly named in the executor assignment; the fourth and fifth are necessary paired assertions against accidental behavior changes in the two changed predicates. A control is not “a test that happens to pass”; assert its expected output and verdict under both binaries.

## Live observation without lane mutation

A read-only observation of the current lane is available, but it supports only the attached-at-tip control, not the failure cases:

```
repo=/home/vgpnk/Projects/shokunin/mori-shokunin
 git -C "$repo" symbolic-ref -q HEAD
   rc=0  refs/heads/master
 git -C "$repo" rev-parse HEAD
   rc=0  24526ea9617cd020fee16c28fe4d4a2789dc28cb
 git -C "$repo" rev-parse --verify -q refs/heads/master
   rc=0  24526ea9617cd020fee16c28fe4d4a2789dc28cb
 git -C "$repo" merge-base --is-ancestor HEAD refs/heads/master
   rc=0
 test -d "$repo/.jj"
   true (.jj present)
```

These commands were run read-only on 2026-10-20. The live lane is colocated now, but HEAD is attached and equals the branch tip; there is no observed HEAD/branch mismatch. The same current-state observation appears in `build/SrcJjGitCompat.md:55-85`. Producing the stale-bookmark or ambient-author condition in the live lane would require changing its refs/commits, which is out of bounds. Therefore **no live census run or live mutation is needed or appropriate for this metric**. The safe direct behavioral evidence is the dedicated real-jj sandbox gate with `HOME`, `XDG_CONFIG_HOME`, `JJ_CONFIG`, and `GIT_CONFIG_GLOBAL` redirected under its scratch root, and all census host probes isolated, as specified in `wave1-dispatch.json:482-483`. That is sandbox evidence, not a live production-operability observation.

Prior evidence also bounds claims: the earlier jj trial's census selftest passed under colocation (`JjTrialMori.md:137-152`), but the audit found the census selftest uses a stub git dispatcher and returns before the revision probes (`JjAuditMori.md:192-198`). That pass is not evidence of branch-anchored behavior against real jj state.

## Residual risks and verification gaps

- **Error versus mismatch:** `git merge-base --is-ancestor` returns 0 for ancestor, 1 for non-ancestor, and another nonzero for errors. The C2 contract says the check “fails” (`contract.md:86-88`), which is ambiguous. Treat only rc 1 as `HEAD_BRANCH_MISMATCH`; route other errors to an unavailable/error path, otherwise a broken lookup can be reported as real lane drift. Source note: `build/SrcGitMergeBase.md:9-12,29-30`. [INFERENCE]
- **Branch-resolution fallback:** C2 requires symbolic HEAD, then `refs/remotes/origin/HEAD`, then the unique local `master`/`main` (`contract.md:81-84`). In the helper, `detect_branch()` itself has the first two steps only; `cmd_state` separately implements the unique-local-branch fallback (`/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh:113-125,153-167`). Keep the resolver's fallback and ambiguous/missing-ref behavior explicit in tests. [INFERENCE]
- **No delivered C2 implementation was present in the lane checkout at review time.** Read-only `git status --short` reported `M .gitignore` and `?? .ufo/waves/round-17/`; `git diff --stat` reported only the one-line `.gitignore` change, and `git diff -- tools/mori-census.sh tools/mori-round17-jj-regressions.py` produced no diff. The current tool listing had no `mori-round17-jj-regressions.py`. Consequently this is an assessment of the proposed metric and required case matrix, not a verified verdict on the eventual delivered implementation or its manifest.
- **Semantic LSP checks unavailable:** attempted `read xd://lsp`; the device returned `No such tool: xd://lsp` and listed mounted tools without an LSP device. No `references`, `definition`, or `diagnostics` request could be made. Exact source ranges and the routed audit/trial reports above are evidence; no grep result is offered as semantic proof.
- No gate, selftest, build, live census, or mutating jj/git command was run for this review. No tools were installed or updated.

## Review verdict

Use the paired assertion comparison only as a case-by-case C2 regression delta with the three named controls (and the closure/author false-positive controls above) passing both revisions. It is not a standalone live operability metric. The current live read proves only a safe attached-at-tip control state; it cannot prove the delivered census detects stale bookmarks or author mismatches.
