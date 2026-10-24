# Freeze-order code review — `e2bfbd6`

## Findings, by severity

### Low — path lookup errors can be misreported as `absent`

`tools/mori-freeze-order.py:68-70` implements `_path_exists` as `cat-file -e` followed by a boolean return-code check. Unlike `_changed_paths` (`:73-80`), it does not distinguish a normal missing path from another `cat-file` failure. `_row_result` uses that boolean to assign `absent` at `:240-249`. If a commit resolves but a tree/blob needed for the path lookup is unreadable or missing from a damaged object database, the checker can report `absent` rather than `could-not-evaluate`; this loses the distinction required by the exit-2 contract (`.ufo/waves/round-18/contract.md:47-53`). **[INFERENCE]** No such object-store failure occurred in the requested run. This is an error-path robustness issue, not a finding about the six observed claim results.

## Frozen-rule conclusion and L1 discrepancy

Yes: **the literal rule counts `no-implementation` as an overclaim when the effective label is `pre-build`.** The frozen label rule says `overclaim = effective label pre-build and verdict != pre-build` (`.ufo/waves/round-18/frozen/c2-register.json:13`). QUALITY 55 explicitly gives that rule priority over a conflicting acceptance example (`corpus/QUALITY.md:176-179`), and QUALITY 52 says a `no-implementation` verdict does not support a pre-build label (`:161-165`). The target implementation matches the frozen rule exactly: it returns `no-implementation` when there is no implementation commit (`tools/mori-freeze-order.py:242-243`) and then marks every non-`pre-build` verdict as an overclaim for a `pre-build` label (`:254-261`). Selftest arm 6 encodes the same expectation (`:481-493`); it was not run in this review.

The contrary statement in `build/FreezeOrder.md:29` describes an earlier implementation/acceptance reading, not the literal rule. Its recorded baseline run at `:14-17` used tips at the freeze commit and reports all three round-18 rows as `no-implementation`; that run also predates the requested corrected-label/tip evaluation. The handoff's recorded tool digest (`:25`, `c87819a…`) differs from the target source digest below, so that old run is not byte-identical evidence for the target implementation. The integration owner should preserve the rule and correct the contradictory handoff, not change the rule to fit the old example.

## Requested read-only check

I ran the requested command with the supplied corrections and `r18-C1..C3` tips at `e2bfbd6f8dccc51fc06455efc41f720301112dd4`. Exit **0**. Before the run, the worktree's tool, register, and correction-file SHA-256 values were checked against `git show <e2bf…>:<path>`; each worktree digest matched its e2bf object:
```sh
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-freeze-order.py check \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
  --register /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-18/frozen/c2-register.json \
  --corrections /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/freeze-register.json \
  --tip-for r18-C1=e2bfbd6f8dccc51fc06455efc41f720301112dd4 \
  --tip-for r18-C2=e2bfbd6f8dccc51fc06455efc41f720301112dd4 \
  --tip-for r18-C3=e2bfbd6f8dccc51fc06455efc41f720301112dd4
```
The command returned `EXIT=0`.

- `tools/mori-freeze-order.py`: `4c15e4557e1f9df9e3849a9f42bbd715c494aeeb9687be7a5cc236f239c6add8`
- `.ufo/waves/round-18/frozen/c2-register.json`: `a654f3802d62126a3e93fee275e3b16e9cd8ac1da28d6994ebd1ffe304609efb`
- `corpus/evidence/freeze-register.json`: `a3d734bf2e331a75df02d4bef18819a9ee96bcb793e4d4cf8daf77f4b0627c77`

The observed lane `HEAD` was `95c615836c2cf74ee11539c4289a1ce06a81cfcb`; the matched object digests establish that the three files used by the requested check were nevertheless byte-identical to their e2bf versions. Results:

| Claim | Verdict | `co_committed` | Effective label | Overclaim | Oracle disagreement |
|---|---|---:|---|---:|---:|
| r17-C1 | co-evolved | true | unlabeled | false | false |
| r17-C2 | co-evolved | true | unlabeled | false | false |
| r17-C3 | co-evolved | true | co-evolved | false | false |
| r18-C1 | pre-build | false | pre-build | false | false |
| r18-C2 | pre-build | false | pre-build | false | false |
| r18-C3 | pre-build | false | pre-build | false | false |

Totals: `claims=6`, `overclaims=0`, `oracle_disagreements=0`, `could_not_evaluate=0`. None of these six rows is `no-implementation` at the requested e2bf tips; their `pre-build` results are therefore not evidence that such a verdict is exempt from overclaiming.

## Requested edge checks

- **Merges / first parent:** `_changed_paths` invokes `diff-tree -m --first-parent` (`tools/mori-freeze-order.py:73-81`). On merge `6531ac6029e200a6392bb76673b6a17d3c895c96`, these read-only commands each exited 0; the first and second produced the same path set, while the third differed:
  ```sh
  git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff-tree --no-commit-id --name-only -r -m --first-parent 6531ac6029e200a6392bb76673b6a17d3c895c96
  git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff-tree --no-commit-id --name-only -r 6531ac6029e200a6392bb76673b6a17d3c895c96^1 6531ac6029e200a6392bb76673b6a17d3c895c96
  git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff-tree --no-commit-id --name-only -r 6531ac6029e200a6392bb76673b6a17d3c895c96^2 6531ac6029e200a6392bb76673b6a17d3c895c96
  ```
- **Renames:** the implementation does not pass `-M` (`:75-78`), so it compares literal paths rather than treating a rename as preservation of a frozen path. A rename away from a registered path makes that path absent at tip; renaming/re-adding that path is still a touch when its name appears in a commit's changed-path set. No rename fixture was run.
- **Deleted then re-added paths:** changed paths are evaluated per commit, and every frozen-path hit updates `last_frozen` (`:229-238`); final presence is checked separately (`:240-241`). Thus a final deletion is `absent`; a re-add makes the path present and the latest touching commit governs the strict ordering. This is code-path review, not a fixture execution.
- **Frozen before base:** when no frozen path is touched in the range, the code requires all frozen paths to exist at `base` before returning `pre-build` (`:244-247`). If no implementation touch exists, it returns `no-implementation` first (`:242-243`), after which the literal label rule still counts a `pre-build` label as overclaim (`:260`).

## Residual risk and verification gaps

- The `lsp` device is not mounted (`read xd://lsp` returned “No such tool”), so LSP status/references/definition/diagnostics could not be obtained. Literal `grep` fallback was used only to locate textual references; it is not semantic call-graph proof. No semantic absence claim is made.
- No selftest, build, lint, or formatter was run. The requested checker and read-only Git comparisons were run; no tools were installed or updated.
- The merge observation covers one existing merge. Rename and delete/re-add semantics were reviewed from the code, not exercised with fixtures.
