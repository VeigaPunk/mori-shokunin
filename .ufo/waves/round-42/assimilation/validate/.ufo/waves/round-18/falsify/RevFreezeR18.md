# Round 18 freeze-order falsification

## Axes and result

Axes examined: **freeze-order correctness**, **requirement-universe completeness**, and **post-implementation acceptance drift**. The commit-history result is high-confidence; the completeness verdict distinguishes the frozen rules from the contradictory acceptance examples.

**Headline:** all three registered claim sets have the same strict pre-implementation order: last frozen-path touch `29b0dc7`; first implementation-path touch `b8f5c6c`; no later committed edit of any registered frozen path through `e2bfbd6`. No frozen path was changed after the freeze commit in the inspected range. However, the register is not a complete inventory of the requirement surface: `contract.md` was also created at the freeze commit but is not listed in any claim's `frozen` array. More importantly, contract acceptance examples conflicted with the frozen rules for C1 and C2. The conflict was resolved after implementation in favor of those already-frozen rules; the effective acceptance changed, but the registered rule files did not.

## Reconstructed rule and history evidence

`frozen/c2-register.json:4-14` defines the rule: `I` is the first-parent commit touching an implementation path; no such commit yields `no-implementation`. `L` is the last commit touching a frozen path. `pre-build` requires `L` absent with frozen paths present at base, or `L` strictly before `I`; equal or later `L` is `co-evolved`. The separate label rule counts an overclaim whenever the effective label is `pre-build` and the verdict is anything other than `pre-build` (`:13`). Thus `no-implementation` is not equivalent to demonstrated `pre-build`.

Read-only history commands and results:

- `git -C <repo> rev-list --reverse --topo-order d005cdd..e2bfbd6f8dccc51fc06455efc41f720301112dd4` — exit 0; order: `29b0dc79e193b9d67845e39850a091a84bad66bd`, `11db4df00bca48f49fada47a2a19b371e86f8778`, `b8f5c6c38e591fed20c1e121af187e58c959c1fe`, `daceeec8c04e0f44cc5130369e86f21fbaf5a3ad`, `e2bfbd6f8dccc51fc06455efc41f720301112dd4`.
- `git -C <repo> show -s --format=%H%n%P <commit>` for each listed commit — exit 0; each commit has exactly the immediately preceding commit as its sole parent, beginning with `29b0dc7` parented by `d005cdd`. There are no merges in this range, so the first-parent comparison is unambiguous.
- For each commit, `git -C <repo> diff-tree --no-commit-id --name-status -r <commit> -- <registered frozen paths, implementation paths, contract.md, corpus/evidence/freeze-register.json, corpus/QUALITY.md>` — exit 0. The relevant changes are:
  - `29b0dc7`: adds the six spec files `contract.md`, the three C1 inputs (`frozen/c1-policy.json`, `frozen/c1-population.json`, `frozen/c1-population-cmd.py`), `frozen/c2-register.json`, and `frozen/c3-ledger-format.json`.
  - `11db4df`: none of those paths.
  - `b8f5c6c`: adds all three implementation tools and `corpus/evidence/freeze-register.json`; no frozen path or contract change.
  - `daceeec`: modifies `corpus/QUALITY.md`; no registered frozen path, contract, or implementation path change.
  - `e2bfbd6`: none of those scoped paths.
- `git -C <repo> diff-tree --no-commit-id -p -r daceeec8c04e0f44cc5130369e86f21fbaf5a3ad -- corpus/QUALITY.md` — exit 0; adds criteria 51–55, including QUALITY 55. `git -C <repo> grep -n -F '55. Acceptance examples in a contract' d005cdd -- corpus/QUALITY.md` — exit 1 (no match at base). Therefore this resolution criterion postdates the `b8f5c6c` implementation commit.

The path-specific history uses literal paths (no rename detection); the checked history reports additions at freeze and additions at implementation, with no delete/re-add or later frozen-path touch. The full commit range was inspected, not only the endpoints.

## Claim-by-claim verdicts

| Claim | Last frozen touch (`L`) | First implementation touch (`I`) | Later frozen-path edit? | Freeze verdict |
|---|---|---|---|---|
| **r18-C1** | `29b0dc7` — adds policy, baseline population, and population command | `b8f5c6c` — adds `tools/mori-retention-gate.py` | None through `e2bfbd6` | **pre-build** |
| **r18-C2** | `29b0dc7` — adds `frozen/c2-register.json` | `b8f5c6c` — adds `tools/mori-freeze-order.py` | None through `e2bfbd6` | **pre-build** |
| **r18-C3** | `29b0dc7` — adds `frozen/c3-ledger-format.json` | `b8f5c6c` — adds `tools/mori-dispatch-ledger.py` | None through `e2bfbd6` | **pre-build** |

These are chronology verdicts at the measured tip, where each implementation exists and the frozen touch strictly precedes it. At the freeze commit itself, the C2 rule yields `no-implementation`; it does not yield `pre-build` merely because no implementation exists yet.

## Completeness and effective acceptance drift

**Shared omission.** The C2 register lists each claim’s specific rule/input files, but not `.ufo/waves/round-18/contract.md`. That contract is nonetheless present in the same `29b0dc7` freeze commit and is not modified later in the inspected range. Adding it as a co-frozen requirement document would leave `L=29b0dc7` for all three claims, so it does not reverse any chronology verdict. It does matter for completeness because it contains acceptance examples that disagree with the registered rules.

- **C1 — rule inputs frozen; acceptance example inconsistent.** The C1 set includes its policy, expected base population, and population-generation command. The policy says the scan covers every tracked blob (`frozen/c1-policy.json:4-5`); there is no general exclusion for the newly added frozen files. The executor handoff reports that scanning `29b0dc7` produced four new rows relative to the `d005cdd` population (120 metric hits versus 116) and did not meet the requested “identical hits plus zero new” example (`build/RetentionGate.md:22-24`). The round-18 lesson records this as a contract-acceptance/frozen-rule contradiction (`corpus/lessons/round-18.md:59`), and QUALITY 55 says the frozen rule wins (`corpus/QUALITY.md:176-180`). **Verdict:** registered C1 policy/replay inputs were frozen in time, but the full acceptance surface was under-inventoried and internally inconsistent; the effective freeze-commit acceptance was corrected after implementation to allow the policy-driven self-hit finding rather than suppress/reclassify it. This is an acceptance correction, not a later edit of the frozen C1 policy.

- **C2 — rule frozen; acceptance behavior initially contradicted it.** The contract itself says r18 claims verify `pre-build` and counts uncorrected pre-build overclaims (`contract.md:31-37`); the frozen register defines the precise label/verdict comparison (`frozen/c2-register.json:6-13`). The initial implementation handoff states it followed an acceptance baseline that excluded `no-implementation` rows from overclaims, contrary to the literal frozen label rule (`build/FreezeOrder.md:27-30`). The lesson records that L1 later changed the tool and selftest to follow the frozen rule; at the freeze commit this now yields four overclaims (`corpus/lessons/round-18.md:59`). QUALITY 55 codifies that resolution only in `daceeec`, after implementation. **Verdict:** chronology remains pre-build and the C2 register itself was not revised; nevertheless, effective acceptance changed after implementation from the contradictory example to the frozen formula. The contract’s omission from the register concealed a requirement conflict, not a late mutation of the frozen formula.

  The appended correction file `corpus/evidence/freeze-register.json` is not part of the frozen rule set: the contract explicitly makes the `1 → 0` result depend on an appended correction (`contract.md:31-35`), while the register defines how such rows affect the effective label (`frozen/c2-register.json:13`). This is retrospective correction data, not a frozen rule. Consequently, the correction is evidence of record repair, not a prospective calibration trial; the independent C2 critique reaches the same qualification (`build/CriticC2Calibration.md:5-7,12-14`).

- **C3 — no acceptance contradiction found.** The format, payload identity, and verification rule are frozen in `frozen/c3-ledger-format.json:4-21`; the contract’s attempt-ledger acceptance examples are at `contract.md:39-43,66-69`. Both documents entered at `29b0dc7`, neither was edited later, and the inspected records disclose no C3 equivalent of the C1/C2 conflict. **Verdict:** chronology is pre-build; the registry still omits the shared contract from its formal frozen-path list, but the omitted document was co-frozen and no effective post-implementation C3 requirement change was found.

**Overall verdict:** **No** committed L1 touch of a registered frozen path occurs after `29b0dc7` in the inspected range. **No** chronology failure: C1, C2, and C3 each have `L < I`. **Yes**, the frozen-path arrays are incomplete as a full requirement-universe manifest because they omit the co-committed contract. **Yes**, effective acceptance was repaired after implementation for C1 and C2 under QUALITY 55; the underlying frozen rules remained unchanged, and the later criterion directs the integrator to resolve contradictions in their favor.

## Confidence and execution boundary

Confidence is **high** for commit ordering and absence of committed frozen-path edits: complete `rev-list` order, sole-parent links, and path-filtered `diff-tree` results agree. Confidence is **high** that the recorded C1/C2 acceptance conflicts were resolved post-implementation: the executor handoffs, round-18 lesson, and added QUALITY criterion agree. The statement that this constitutes an “effective acceptance change” is an interpretation of those records; it does **not** mean the frozen rule files changed. The check is limited to committed history through `e2bfbd6`; it does not establish uncommitted working-tree touches.

No tools were installed or updated.