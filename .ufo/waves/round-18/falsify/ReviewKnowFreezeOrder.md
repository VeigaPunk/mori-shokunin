# Review: `corpus/knowledge/freeze-order-r18.md` at `e2bfbd6f8dccc51fc06455efc41f720301112dd4`

## Verdict

The C2 rule is mostly consistent with the frozen register and the source receipts, and the note correctly says that matching a previously known oracle is not independent evidence of discernment. However, the final claim of a post-implementation self-application is not supported by the cited measurement receipt; the source/measurement anchors are not precise enough for the QUALITY bar; and two stated limitations are incomplete or incorrect. Fixes are listed below.

## Findings, by severity

### High — post-implementation self-application is asserted without a supporting measurement (target `corpus/knowledge/freeze-order-r18.md:35`)

The cited implementation handoff records the baseline check at the freeze commit `29b0dc79e193b9d67845e39850a091a84bad66bd`, not at a later measured tip: `.ufo/waves/round-18/build/FreezeOrder.md:14-17`. That receipt says all three r18 claims had `no-implementation` at that tip. The same receipt records the co-commit selftest arm separately at `:20-23`. `CriticC2Calibration.md:7,20-34` explicitly distinguishes the freeze-tip no-implementation result from the later positive self-application that must be measured after implementation. `draft-verdicts.md:9` states a provisional result and gives the freeze/first-implementation boundary, but not the exact measured tip, command, or captured output.

**Fix:** Replace the assertion of self-application at the measured tip with the narrower supported statement that the selftest has a co-commit arm. Add the exact post-implementation measured commit, full command, output/exit status, and tool identity as a committed receipt before claiming the positive self-application. Keep the `29b0...` no-implementation check as a separate falsifier, not the positive result.

### Medium — commit-order proxy is described too strongly and omits the key prior-knowledge limit (target `:7-11`)

S056 supports the prediction/postdiction distinction, but the mapping from preregistration to lane commit order is an inference. The opened-source receipt says explicitly that Git order is only a proxy for “before observation”: it cannot prove the author did not know the outcome already, and the C2 label certifies commit ordering only (`.ufo/waves/round-18/build/SrcNosekPrereg.md:32-35`; registry scope `corpus/SOURCES.md:62`). Calling it “the observable equivalent” at `:8` is stronger than that evidence and fails to mark the inference separately as required by `corpus/QUALITY.md:5`.

**Fix:** Mark the mapping `[INFERENCE]` and call it a commit-order proxy. State alongside the rule that it does not establish when the author learned the outcome or whether the requirement set was complete. Do not imply preregistration equivalence or causal prevention.

### Medium — the displayed recheck commands are not runnable as written (target `:3`)

`<tip>` and `<empty dir>` are literal placeholders, not shell-safe arguments. The frozen register itself contains `<measured round-18 commit>` for each r18 tip (`.ufo/waves/round-18/frozen/c2-register.json:30-40`); the checker requires valid `--tip-for ID=REV` overrides and returns `could-not-evaluate` for unresolved placeholder tips (`tools/mori-freeze-order.py:187-196,200-214`). The selftest also requires `TMPDIR` to resolve inside the script checkout (`tools/mori-freeze-order.py:401-418`), so the placeholder does not identify a usable scratch location.

**Fix:** Provide an actual measured commit hash (or clearly define a shell variable that the reader must set to one) for every override. Give a concrete, checkout-local `TMPDIR` path with valid shell quoting. Document the required working directory; do not leave angle-bracket placeholders in a command presented as the recheck recipe.

### Medium — rename limitation at `:36` is inaccurate for the checker as implemented

The tool calls `diff-tree` without `-M` or `--no-renames` (`tools/mori-freeze-order.py:73-81`), but its environment only suppresses global/system configuration and does not disable repository-local `diff.renames` (`:28-37`). The official Git `git-config` page says `diff.renames` defaults to `true` and controls rename detection (reader lines 3561-3566; https://git-scm.com/docs/git-config, accessed 2026-10-21). Thus “without `-M`” does not establish that a rename is necessarily reported as delete plus add; the effective behavior can depend on Git configuration. The source scribe receipt does not cover rename-detection semantics (`.ufo/waves/round-18/build/SrcGitRevList.md:57-70,91-94`).

**Fix:** Make the tool’s behavior deterministic by passing `--no-renames` if delete-plus-add is the intended limit, or describe the limit as configuration-dependent and pin/record the configuration. Add the relevant source anchor to the source registry/receipt if the note retains this claim. The Git option text is also at https://git-scm.com/docs/git-diff-tree, reader lines 747-752 (accessed 2026-10-21).

### Medium — historical result and coverage claims lack per-claim measured anchors (target `:28-35`)

The header points generally to source receipts and re-derivation files (`:1-2`), but the result bullets do not give the required path:line plus command/evidence anchor for their measurements. QUALITY requires every claim to carry a measured anchor (`corpus/QUALITY.md:4`). Receipts do exist: the r17 derivations report the C1/C2/C3 verdicts and co-commit observations (`.ufo/waves/round-18/build/RevFreezeR17C1.md:43-50`, `RevFreezeR17C2.md:47-65`, `RevFreezeR17C3.md:73-79`); the correction is recorded in `corpus/evidence/freeze-register.json:3-11`. The note should link these at the claims, with the actual commands or stable receipt identifiers where available.

The omitted coverage caveat matters too: the C1 and C3 reviewers say their registered frozen sets omit additional fixture/replay inputs, although adding the defensible paths does not change the verdict (`RevFreezeR17C1.md:53-57`; `RevFreezeR17C3.md:84-107`). The current note reports the three results without this qualification, while naming only rename/merge limits at `:36-37`.

**Fix:** Add exact anchors and state that the r17 results are classifications over the registered path sets. Disclose the C1/C3 input-set qualifications and the receipts’ conclusion that expanded path sets do not change those verdicts. Do not imply complete input coverage.

### Low — “independently re-derived” is ambiguous next to the correct non-independence caveat (target `:2,33-35`)

The separate r17 derivation receipts support that the verdicts were re-derived (`RevFreezeR17C1.md:5-7`, `RevFreezeR17C2.md:11-21`, `RevFreezeR17C3.md:13-15`). But the C2 critique says the L1 already knew the outside rulings, so the 3/3 is retrospective concordance, not an independent calibration trial (`.ufo/waves/round-18/build/CriticC2Calibration.md:5-6,14`). The note correctly states this at `:33-35`, but “independently” in the header can be read as a claim of independent/blinded calibration.

**Fix:** Say “separately re-derived” and explicitly distinguish separate derivations from a blinded or independent calibration trial. Keep the caveat at `:33-35`.

### Medium — side-branch membership is not separated from first-parent merge diffs (target `:36`)

The tool enumerates `base..tip` without `--first-parent` (`tools/mori-freeze-order.py:84-89`) and computes merge changes against the first parent (`:73-81`). The source receipt points out that side-branch commits can be I or L and says this must be stated (`.ufo/waves/round-18/build/SrcGitRevList.md:59-64,119`). “Merges are judged against their first parent” alone can be read as limiting the history walk to the first-parent chain.

**Fix:** State the two facts separately: the commit range includes reachable side-branch commits; a merge’s changed-path comparison uses its first parent.

## Direct answers to the requested checks

- **Opened source or committed receipt:** S056 and S058 are present in `corpus/SOURCES.md:62,64`, and their committed opening receipts exist. The frozen rule is in `.ufo/waves/round-18/frozen/c2-register.json:4-14`. Most r17 result claims have derivation receipts, but the note needs per-claim line/command anchors; the post-implementation self-application is not demonstrated by the cited `FreezeOrder.md` receipt.
- **Limits:** rename and merge limits are attempted, but the rename statement is not established by the current code/configuration, and the note omits the outcome-knowledge limit plus the C1/C3 registered-input coverage qualifications. It should also clarify that the traversal includes side-branch commits.
- **Runnable recheck:** no. The literal placeholders in line 3 must be replaced, and `TMPDIR` must be a concrete checkout-local path.
- **Privacy proof / canonical JSON:** neither claim appears in this 37-line file. No finding on either; the JSON output contract elsewhere is not, by itself, a canonical-JSON claim.
- **Independence:** the body correctly rejects independent-evidence status for the known-oracle agreement. The header wording should be narrowed to avoid suggesting blinded calibration.

## Verification gaps and command record

No build, test, or selftest was run. I did not execute the recheck recipe. No LSP device is mounted: `read xd://lsp` returned “No such tool”; no LSP status/references/definition/diagnostics were available. Literal `git grep` searches were used only to locate anchors, not as semantic proof.

Read-only lane commands with observed exit codes:

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show e2bfbd6f8dccc51fc06455efc41f720301112dd4:corpus/knowledge/freeze-order-r18.md | cat -n >/dev/null` — 0.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show e2bfbd6f8dccc51fc06455efc41f720301112dd4:.ufo/waves/round-18/build/FreezeOrder.md | cat -n >/dev/null` — 0.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n -E 'Every claim carries a source|Observation, inference and unknown' e2bfbd6f8dccc51fc06455efc41f720301112dd4 -- corpus/QUALITY.md` — 0.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n -E 'S056|S058' e2bfbd6f8dccc51fc06455efc41f720301112dd4 -- corpus/SOURCES.md` — 0.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff d005cdde0e009dea6c0cc29b37163de536528658 e2bfbd6f8dccc51fc06455efc41f720301112dd4 -- corpus/knowledge/freeze-order-r18.md` — 0 (the file is new in the attacked-tip diff).
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n -E 'r18-C2|measured tip|29b0dc79e193b9d67845e39850a091a84bad66bd' e2bfbd6f8dccc51fc06455efc41f720301112dd4 -- .ufo/waves/round-18/build/FreezeOrder.md .ufo/waves/round-18/build/CriticC2Calibration.md` — 0.

No tools were installed or updated.