# Critic — correction row and C2 verdict

## Axes and verdict

- **Primary axis: calibration** (the C2 freeze-order claim; SCORECARD.md:1110-1116 shows calibration at 5, tied with depth and freshness).
- No evidence from this scoped review changes coverage, operability, depth, freshness, or adjacency.

**Critic verdict:** Keep the appended r17-C3 correction as a valid retrospective record correction. Do **not** treat the `1 → 0` count alone as calibration-behavior improvement: it is the result of changing the effective label after the outside ruling was known. I would mark the present C2 axis verdict **unchanged / improvement not established**, not “improved, narrowly,” until the independent r18 freeze-order evidence and the frozen-rule inconsistency below are resolved. This is a critique recommendation, not admission.

## Correction-row fidelity

The correction at `corpus/evidence/freeze-register.json:6-11` faithfully preserves the closure’s partial ruling. It keeps the useful calibration repair (the witness and miss/hit+sibling oracle precede the final tool change) distinct from the stronger, unsupported assertion that all final controls were preregistered before implementation. That matches `corpus/lessons/round-17-verifier-spotcheck.md:207-213,398-402`; the effective `co-evolved` label also agrees with the frozen verdict rule and outside ruling (`.ufo/waves/round-18/frozen/c2-register.json:4-13,24-29`). The correction should not be read as withdrawing credit for the actual calibration repair.

There is a bounded completeness caveat, not a verdict reversal: `build/RevFreezeR17C3.md:84-107` finds the frozen set omits the four `c3-tree` replay inputs, but establishes that adding them leaves the last frozen touch at `2be8294` and the result `co-evolved`. The correction’s summary remains directionally faithful; if its rationale is intended as a complete input inventory, mention the full replay-control set rather than only the recipe and final expected record.

## Counterexample to the C2 draft score

`draft-verdicts.md:9` reports one pre-existing overclaim, cites `evidence/c2-before.json`, and then calls the zero-after result a narrow improvement. But the cited JSON at `evidence/c2-before.json:1` contains six claim rows and **four** `overclaim: true` results: r17-C3 plus r18-C1/C2/C3, each r18 row having `verdict: no-implementation` and effective label `pre-build`. Thus the cited artifact does not support the stated total of one.

This is not merely a display discrepancy. The frozen rule defines `no-implementation` when no implementation touch exists and defines an overclaim as effective label `pre-build` with any verdict other than `pre-build` (`frozen/c2-register.json:4-13`). Yet `build/FreezeOrder.md:27-29` explicitly says the implementation suppresses `no-implementation` rows from the overclaim total to satisfy the expected baseline. `build/CriticC2Calibration.md:20-34` specifies the counterexample that must remain distinguishable: at the freeze commit, r18-C2 is `no-implementation`, not `pre-build`, and the check must fail with that pre-build label counted as an overclaim. The implementation’s suppression contradicts that frozen label rule and falsifier. Accordingly, the draft’s claimed baseline is not supported by its cited evidence, and its prospective r18 claim cannot cure the inconsistency merely by asserting a later `pre-build` result.

The historical `1 → 0` change itself is a **relabel/correction**, not a new calibration trial: the correction is prompted by the already-available closure, and the frozen register contains the outside rulings and their locations (`frozen/c2-register.json:15-29`; `CriticC2Calibration.md:5-8,12-14`). Oracle concordance is retrospective reproduction, not blinded independent calibration. A genuinely verified r18 freeze can be separate positive process evidence, but only when evaluated at the completed post-implementation tip and with the required negative/failure-capability check; the cited critique sets out those conditions at `CriticC2Calibration.md:18-38`.

## Other round-17 freeze-like wording

The survey does **not** identify another supported r17 `pre-build` label that needs a second C2 correction row. Most omitted C3 references are pre-run or measurement-time pinning/binding, C2’s fixed-universe statements assert before/after constancy, and the wave-2 process-control snapshot postdates initial build dispatch (`build/ScoutFreezeLabels.md:32-62,75-86`). Those do not contradict the register’s scope or the closure’s ruling.

One residual wording hazard is real: `corpus/lessons/round-17.md:135-139` calls the initial `c3-expected.json` “Frozen,” while the later M18 correction at `:245` says the initial expectation/recipe postdated that run (`build/ScoutFreezeLabels.md:40,87`). The later correction already supplies the counter-record, so this is not a second `pre-build` overclaim for the C2 count and need not become another register label correction. If the historical paragraph is still presented without its correction context, add a short cross-reference/clarification that “Frozen” means only the later measurement pin, not preregistration before the initial run.

## Smallest safe correction

1. Keep the r17-C3 correction row and its `co-evolved` label; do not revise the closure’s partial credit.
2. Reconcile C2 reporting with the frozen rule without silently treating `no-implementation` as `pre-build`: report the historical r17 overclaim count separately from the r18 self-application diagnostics, and show the r18 freeze-tip rows as `no-implementation` plus overclaim under the literal rule. Recompute/repair the cited C2 evidence and draft totals accordingly; if the metric was intended to be r17-only, state that scope explicitly rather than presenting the all-claim total as one.
3. Describe the r17 `1 → 0` as “historical overclaim corrected” (record accuracy). Credit calibration improvement only if the separate r18 post-implementation result and the specified failing no-implementation/co-commit checks are evidenced under a consistent implementation of the frozen rule.
4. Cross-reference the lesson’s `:138` wording to the existing correction at `:245`; no additional overclaim row for the other pre-run/constancy references.

This review used read-only file reads only. No shell commands, tests, selftests, installs, or VCS mutations were run.