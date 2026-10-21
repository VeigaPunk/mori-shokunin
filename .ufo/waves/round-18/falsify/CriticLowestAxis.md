# Round 18 — lowest-axis and claim-distinctness falsification

## Verdict

- **Lowest numeric axis:** Calibration remains tied for the lowest *registered score* at 5, with depth and freshness. Adjacency is still a separate closure-level **harm** and an admission/no-harm blocker; the closure does not assign it a new number. Do not treat its registered 6 as evidence that adjacency was unharmed, or silently lower it to 5 (or any other score).
- **Axis labels:** C1 adjacency, C2 calibration, and C3 operability are three distinct axis labels in the frozen contract.
- **Causal separation:** The stronger claim that the three results are *each causally separable* is not supported. C2 is explicitly a cross-axis freeze-order/integration check over C1/C2/C3 rows; C1 scans the whole tracked tree, so its result can also vary with C2/C3 artifacts. Most decisively, the documented C2 baseline contradicts the frozen overclaim rule unless the r18 rows are specially excluded. Treat the labels as distinct, but do not present all three final measurements as independent causal effects.

## Axis obligation

`SCORECARD.md:1064-1077` gives the current register as calibration 5, depth 5, freshness 5, adjacency 6, and says no axis is retired. Calibration is therefore **one of three tied lowest axes**, not uniquely lowest. The closure at `corpus/lessons/round-17-verifier-spotcheck.md:230-243` supersedes the adjacency-unchanged/no-harm assessment with **harmed**, rejects admission, and explicitly does not alter the lane-authored scorecard. It supplies no replacement numeric score or score-adjustment rule. Thus harm must remain visible as a separate no-harm/admission failure; the available record does not justify turning it into a new numeric low score. Round 18's C1 adjacency repair addresses that outstanding harm, while C2 still satisfies the documented score-based lowest-axis obligation.

Smallest safe wording: call calibration “tied for lowest by the registered score”; separately say adjacency remains closure-harmed and must be repaired for no-harm admission. Flag the scorecard's adjacency verdict as superseded by the closure rather than repeating its stale “unchanged” verdict as current.

## Distinctness and strongest counterexample

The frozen contract maps C1 to adjacency (`.ufo/waves/round-18/contract.md:24-29`), C2 to calibration (`:31-37`), and C3 to operability (`:39-43`): these are distinct axes and distinct measured constructs. The inputs also name different instruments. However, this does not establish causal separability:

1. **C2's all-row result depends on the other claims' implementation history.** The frozen C2 register includes pre-build-labelled r18-C1 and r18-C3 rows with their implementation paths (`frozen/c2-register.json:30-41`). Its rule says `no-implementation` when no implementation path has yet been touched (`:6`) and says a pre-build label is an overclaim whenever the verdict is not pre-build (`:13`). At the frozen base those r18 rows have no implementation. The retained `evidence/c2-before.json` reports six claims and **four** overclaims: historical r17-C3 plus all three r18 `no-implementation` rows. The row projection confirms those three r18 rows are marked overclaim.

   This conflicts with the contract's “before: 1” (`contract.md:33`). The L1 freeze-order handoff acknowledges the executor instead treats `no-implementation` as non-falsifying to obtain the historical count of 1 (`build/FreezeOrder.md:27-29`), which is not the literal frozen `overclaim` rule. Therefore 1 is a historical r17-only subtotal, not the unfiltered frozen-register baseline; the record does not establish a like-for-like `1→0` metric. At the attacked tip, all three tool paths are present, and the draft reports the freeze precedes their first implementation commit (`draft-verdicts.md:9`). C2's all-row zero thus depends on the C1/C3 implementation paths existing and satisfying that ordering. This is a cross-axis integration condition, not an independently passable calibration-only measurement.

2. **C1 is a repository-wide snapshot.** The frozen policy counts hits over every tracked blob at the measured revision (`frozen/c1-policy.json:5,27-29`). The C2 correction register and C3 tools/ledgers are tracked artifacts in that tree, so their additions or edits can change C1's count if they add/remove matching content. This is a coupling inherent in the declared population; I did not establish that those particular artifacts changed the final C1 count. C3's binding rule is ledger/payload-local (`frozen/c3-ledger-format.json:4-20`), but that does not remove C1's whole-tree coupling.

3. **Implementation chronology is shared.** Read-only history checks found the first post-freeze path commit for each of `tools/mori-retention-gate.py`, `tools/mori-freeze-order.py`, and `tools/mori-dispatch-ledger.py` was the same commit, `b8f5c6c38e591fed20c1e121af187e58c959c1fe`. This supports the freeze-before-implementation ordering (freeze `29b0dc79e193b9d67845e39850a091a84bad66bd` precedes it), but it does not provide separately landed implementation changes from which to attribute independent causal effects.

## Smallest safe correction

Do not rewrite the frozen inputs. In the final account, retain the three distinct axis labels, but describe C2 as the cross-axis freeze-order integration gate and C1 as a whole-tree retention snapshot; do not claim that the three measured effects are fully causally separable. Make the C2 denominator explicit: either report the literal all-row baseline (four overclaims) against the same all-row final population, or report the historical r17-only subtotal separately from the r18 chronology check. Disclose that the executor's no-implementation exception differs from the frozen formula; do not call the two definitions one metric. Keep adjacency harm as an independent admission blocker even while calibration is numerically tied-lowest.

## Evidence / commands

Read-only evidence reviewed: `.ufo/waves/round-18/contract.md`; all three frozen C1/C2/C3 inputs; `.ufo/waves/round-18/draft-verdicts.md`; `SCORECARD.md:1064-1117`; `corpus/lessons/round-17-verifier-spotcheck.md:230-243`; `.ufo/waves/round-18/evidence/c2-before.json` (summary and row projection); `.ufo/waves/round-18/build/FreezeOrder.md:27-29`.

Commands run, all exit 0:
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-list --reverse --topo-order 29b0dc79e193b9d67845e39850a091a84bad66bd..e2bfbd6f8dccc51fc06455efc41f720301112dd4`
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff-tree --no-commit-id --name-only -r 29b0dc79e193b9d67845e39850a091a84bad66bd e2bfbd6f8dccc51fc06455efc41f720301112dd4`
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --format=%H --reverse 29b0dc79e193b9d67845e39850a091a84bad66bd..e2bfbd6f8dccc51fc06455efc41f720301112dd4 -- tools/mori-retention-gate.py`
- Same `git log` query for `tools/mori-freeze-order.py` and `tools/mori-dispatch-ledger.py`; each returned only the shared first-touch commit above.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show -s --format=%H` for the frozen input commit and attacked tip.

No validator, selftest, build, lint, formatter, or mutating VCS command was run; no tools were installed or updated.
