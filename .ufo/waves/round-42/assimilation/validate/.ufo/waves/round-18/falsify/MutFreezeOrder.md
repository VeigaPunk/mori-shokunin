# MutFreezeOrder — isolated C2 mutation probes

## Result and axes

**6 killed, 2 survived, 0 inconclusive across the eight assigned single-point mutants.** The survivors are date-order traversal (M04) and case-insensitive oracle comparison (M07). Every mutation was restored before the next was applied. This is advisory detector evidence, not an integration, admission, or round judgment.

Axes: **frozen-rule fidelity**, **behavioral detection strength**, and **exact restoration / isolation**. The two survivors identify coverage gaps; they do not authorize changing the frozen rule.

## Scope and authority

- Attacked clone: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/MutFreezeOrder/`.
- Observed clone HEAD: `e2bfbd6f8dccc51fc06455efc41f720301112dd4`.
- Only mutated file: `tools/mori-freeze-order.py` inside that clone. Source references below use this file's original/restored line numbers at the attacked tip.
- Required ordering and labeling: `.ufo/waves/round-18/frozen/c2-register.json:5-14`. In particular: reverse topological traversal, recursive first-parent changes, strict `L < I`, separately reported co-commit, no-implementation distinct from pre-build, last correction wins, and exact verdict/ruling inequality.
- Tool/selftest and exit-status contract: `.ufo/waves/round-18/contract.md:31-37,47-53,62-65`.
- L1 reading attacked: `.ufo/waves/round-18/draft-verdicts.md:9` calls C2 narrowly improved and expressly disclaims independent evidence from 3/3 oracle agreement. The required companion reading, `.ufo/waves/round-18/out-of-metric-triage.md:3-6,25-31`, concerns privacy triage and remaining coverage/debt; no privacy repair was attempted here.
- Frozen C1 policy, population summary, population recipe, and C3 ledger format were read as context only; none was executed or modified.

## Commands and detector protocol

The only direct VCS invocation was the read-only provenance command below, exit **0**, which printed the HEAD above:

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/MutFreezeOrder show -s --format=%H HEAD
```

Every detector invocation used this exact command, with working directory `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/MutFreezeOrder` and a 45-second command deadline:

```sh
sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/MutFreezeOrder/tools/mori-freeze-order.py && env TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/MutFreezeOrder/.scratch GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/MutFreezeOrder/tools/mori-freeze-order.py --selftest
```

There were **17 detector runs**: initial pristine baseline, then eight mutation/restoration pairs. Each successful restoration run is also the immediately preceding pristine baseline for the next mutant, with no intervening source change. Thus every mutant has a passing pristine run, a mutated run, and a passing restored run under the same detector. All hash commands succeeded; all detector runs completed without a deadline failure.

Only the tool's own `--selftest` created/committed fixture repositories. Its implementation puts them under the supplied clone-local TMPDIR (`tools/mori-freeze-order.py:320-355,401-425`) and isolates Git configuration (`:28-38,321-334`). No direct mutating VCS command, other tool's selftest, background job, service, live journal query, package transaction, or other runtime was invoked.

## Mutants, expected detectors, and actual outputs

In this table, expected child-check assertions describe the existing selftest code, not separately observed child output. The detector captures child stdout/stderr and emits only its aggregate count (`tools/mori-freeze-order.py:376-398,560-565`). Actual outputs below are the aggregate selftest outputs observed here. A `FAIL n/11` reports n completed arms, **not** n detected mutants.

| ID | Single-point mutation | Expected detector / existing arm | Actual mutated output | Exit | Probe verdict |
|---|---|---|---|---:|---|
| M01 | `:249`: `last_frozen < first_impl` → `last_frozen <= first_impl` | Arm 2, co-committed: child exit 1, `co-evolved`, `co_committed=true`, `overclaim=true` (`:438-449`). | `SELFTEST freeze-order FAIL 1/11` (stderr; stdout empty) | 1 | **Killed** |
| M02 | `:238`: set `co_committed = False` instead of `True` when both path sets are touched. | Arm 2 explicitly asserts `co_committed=true` (`:446-448`). | `SELFTEST freeze-order FAIL 1/11` (stderr; stdout empty) | 1 | **Killed** |
| M03 | `:76`: remove `"-r"` from the `diff-tree` arguments. | Arm 1 has nested `tools/impl.py` and requires child exit 0 / `pre-build` (`:427-436`). | `SELFTEST freeze-order FAIL 0/11` (stderr; stdout empty) | 1 | **Killed** |
| M04 | `:85`: `"--topo-order"` → `"--date-order"` in `rev-list`. | A distinguishing branched/timestamped graph would need to fail. Existing merge arm 10 only requires `co-evolved` (`:535-550`). | `SELFTEST freeze-order PASS 11/11` (stdout; stderr empty) | 0 | **Survived** |
| M05 | `:243`: no-implementation branch returns `"pre-build"` instead of `"no-implementation"`. | Arm 6 requires child exit 1 / `no-implementation`, effective label `pre-build`, and `overclaim=true` (`:481-494`). | `SELFTEST freeze-order FAIL 5/11` (stderr; stdout empty) | 1 | **Killed** |
| M06 | `:269`: `label = claim["declared"]`, ignoring corrections instead of looking up the corrected label. | Arm 7 requires child exit 0 / `co-evolved`, effective label `co-evolved`, and `overclaim=false` (`:496-512`). | `SELFTEST freeze-order FAIL 6/11` (stderr; stdout empty) | 1 | **Killed** |
| M07 | `:261`: compare `verdict.lower() != ruling.lower()` instead of `verdict != ruling`. | Arm 8 checks ordinary unequal lowercase values, `pre-build` versus `co-evolved`, so it does not discriminate this loose comparison (`:514-524`). | `SELFTEST freeze-order PASS 11/11` (stdout; stderr empty) | 0 | **Survived** |
| M08 | `:314`: return 0 instead of 2 when `totals["could_not_evaluate"]` is nonzero, swallowing unknown-revision failure status. | Arm 9 supplies a missing tip revision and requires child exit 2 / `could-not-evaluate` (`:526-533`). | `SELFTEST freeze-order FAIL 8/11` (stderr; stdout empty) | 1 | **Killed** |

[INFERENCE] The completed-arm counts locate the first failing arm as 2, 2, 1, 6, 7, and 9 respectively. The detector does not print the exception or failed assertion, so no more specific child-output or exception claim is made. The same unchanged detector passed on pristine and restored bytes around each failure; none is a baseline failure mislabeled as a kill.

## Hash and restoration evidence

Initial and every restored source SHA-256, denoted **P**:

```text
4c15e4557e1f9df9e3849a9f42bbd715c494aeeb9687be7a5cc236f239c6add8
```

Each mutation changed one displayed source line through the edit tool. Its inverse restored that line; the edit tool returned the original snapshot tag `0E73` after every restoration. The next hash/detector command observed P and passed. No mutant was retained.

| ID | Before SHA-256 | Mutated SHA-256 | Restored SHA-256 | Restored detector output / exit |
|---|---|---|---|---|
| M01 | P | `d49dc583bd21f10f6459272668502220e8ee933bb3b588a5c578cad6760e7fd2` | P | `SELFTEST freeze-order PASS 11/11` / 0 |
| M02 | P | `a2bd0ebd5f8a1217b63eb0bfbff58ed3a5e77df1f8e0ac8314d21fc0826536db` | P | `SELFTEST freeze-order PASS 11/11` / 0 |
| M03 | P | `e5a99ad6ddbab55abe273ba0d35121427ab2889b0290c799e0aead213f5d1b4e` | P | `SELFTEST freeze-order PASS 11/11` / 0 |
| M04 | P | `3c1de5eb9260827bf8c2a5ac3e539e13fa44c028a49c348b47e21ce35b55582d` | P | `SELFTEST freeze-order PASS 11/11` / 0 |
| M05 | P | `9a01b74732e8e322f38bb2294a6243976ab5adc470ebd9dcfca8ee5beace7264` | P | `SELFTEST freeze-order PASS 11/11` / 0 |
| M06 | P | `7826900866260ce7afbab071b3a679a6594a30c054cb8b2580875a9eddeb00b7` | P | `SELFTEST freeze-order PASS 11/11` / 0 |
| M07 | P | `3666b8ad72a7c4f2e12b824bd2091892efd9e925f61e2b90d25b08b4377cedb0` | P | `SELFTEST freeze-order PASS 11/11` / 0 |
| M08 | P | `6b1e220476813d2de0d2b5e5216ceb1d282142dfbecff0aa9e96c5e1be5c9368` | P | `SELFTEST freeze-order PASS 11/11` / 0 |

The initial pristine detector also printed `SELFTEST freeze-order PASS 11/11`, exit 0. Every PASS above had empty stderr; only the failing selftests printed to stderr. Hash equality is the recorded restoration evidence; no repository status or cleanliness claim is used to infer absence of prohibited actions.

## Missing detector arms and limits

### M04 — traversal-order discrimination

**Observed:** substituting `--date-order` for the frozen `--topo-order` survives all 11 arms. The fixture Git environment does not set author/committer dates (`tools/mori-freeze-order.py:321-334`). Arm 10 builds a two-branch merge, but it also introduces a final first-parent frozen edit and checks only the resulting `co-evolved` verdict (`:535-550`).

**Missing arm:** [INFERENCE, not executed] a deliberately dated divergent DAG whose reverse date order interleaves branches differently from reverse topological order, with relevant frozen/implementation touches positioned so that the classification or separately asserted traversal changes. The fixture must establish that its two command orderings actually differ and assert the frozen-rule result, rather than merely adding another merge that both algorithms grade alike. `--date-order` still respects parent-before-child constraints after reversal; an ordinary linear history is not sufficient. This finding is detector insufficiency, not a demonstrated wrong result for the six real register claims.

### M07 — exact oracle equality

**Observed:** the sole outside-ruling disagreement fixture supplies lowercase `co-evolved` against lowercase `pre-build` (`tools/mori-freeze-order.py:514-524`), which remains unequal after lowercasing. Register validation accepts any string ruling (`:140-149`); the frozen rule is exact inequality (`.ufo/waves/round-18/frozen/c2-register.json:13`).

**Missing arm:** [INFERENCE, not executed] a normal `pre-build` result with outside ruling `PRE-BUILD`, declared label `unlabeled`: require `oracle_disagreement=true` and exit 1. The M07 comparison would erase that disagreement and return success. A matching exact-case oracle fixture would also exercise the false branch, which arm 8 does not assert.

### Adjacent unexercised boundaries (static reading only)

These were not additional mutation probes and are not claimed as independently reproduced defects:

- Last correction wins: arm 7 supplies only one correction row (`tools/mori-freeze-order.py:504-511`), not competing sequential labels. [INFERENCE] A first-row-wins defect is not challenged by that fixture.
- Unknown **base** and explicit reasons: arm 9 exercises a missing overridden tip and checks exit/verdict, but does not assert `reason` or exercise the separate unknown-base branch (`:215-220,526-533`). [INFERENCE] M08 being killed by the tip arm does not establish independent base-branch coverage.
- Negative co-commit flag: arm 2 asserts the true flag; arms for separated commits do not explicitly assert false (`:427-469`). [INFERENCE] Always-true reporting would need its own assertion.

## Disposition and execution bounds

The six kills support detection of the particular strict-boundary, co-commit, nested-diff, implementation-absence, ignored-correction, and swallowed-error-status defects above. The two survivors limit any claim that the current selftest protects the entire frozen algorithm. They do **not** establish that the unmutated attacked tip misclassifies the real claims or change the L1's metric.

No production fix, test addition, integration, permanent source change, lane VCS mutation, or another runtime invocation was performed. Writes were the eight temporary source mutations and inverses inside the assigned clone, that tool's own TMPDIR fixtures, and this report. No probe output or scratch was written to `/tmp`; no outside scratch/helper file was created. No tool was installed or updated (tool/version/channel/reason: none). No web source was used, so there are no external URLs to cite. Probe complete; all eight source restorations are evidenced above.
