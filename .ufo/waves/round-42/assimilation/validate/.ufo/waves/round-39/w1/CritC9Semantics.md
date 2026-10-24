# CritC9Semantics — P-C9 contract/code review

**Review recommendation: FAIL.** Two concrete sentences exceed the implementation without a disclosed P-C9 bound: the universal linear-history compatibility sentence, and the first-parent-state clause. This is an advisory falsification report, not a canonical runtime judgment. No admission, integration, remediation, or alternate runtime was performed.

**Axes:** depth (C3's ancestry semantics), calibration (claim/implementation correspondence), operability (round-change detection and exit status). The failures below concern C3; they do not independently falsify C1 or C2.

## Evidence identity and notation

All relative paths below are relative to `/home/vgpnk/Projects/shokunin/mori-shokunin`.

- **C** = `.ufo/waves/round-39/contract.md`.
- **G** = `tools/mori-sources-appendonly.py`, with line references matching the scored committed copy under the scratch directory below.
- **S** = `.ufo/waves/round-39/scratch/CritC9Semantics/`.
- **R**, **T**, **B** = `S/results.json`, `S/traces.json`, `S/baseline-receipts.json` respectively.

The exercised v2 bytes came from `git show 13bfba23b7ca063c76d3504a2ff6eb7b6a294932:tools/mori-sources-appendonly.py`, SHA-256 `62cd4132dbe141538371f79723c3caff66670fab9076494cd9cf65efccfc01e7`, matching `evidence/freeze-r39.txt:13`. V1 came from entering tip `13f3db7e5c7163e7ef300259ff597a42a79f81f1`, SHA-256 `9a6164e391479bcc9e50487f9eabbc95d4f25d57793f77575d33f8520fdb09fa`. The extraction and execution are reproducible in `S/probe.py:13-36,72-78`; observed extraction hashes are in command output `artifact://15868:1-2`.

## Sentence-by-sentence verdict table

P-C9 is one long sentence; its independently checkable clauses are separated here rather than hiding a failing conjunct inside an overall pass.

| Contract sentence/clause | Review verdict | Evidence and exact limit |
| --- | --- | --- |
| C:131: reports the `supersede_timing` line after its summary | PASS | G:397-405 emits those lines in order; R:16-18 exercises the CLI. |
| C:131: as-of only when the selected landing descends from the selected edit, by `git merge-base --is-ancestor` | PASS for the selected pair | G:144-159,350-357 really calls the primitive. Equality is accepted by that primitive; P-C9 explicitly names it. This does not establish that the selected edit/landing is uniquely meaningful on a DAG. |
| C:131: “its latest superseding row's landing commit” | UNDISCLOSED SELECTION POLICY | G:301 records first appearance per target/superseder pair; G:338-341 selects maximum path-walk index, not an ancestry-unique latest landing. Two incomparable superseders exchange priority, and the verdict flips, when only their date ordering changes. R:98-175; T:13-28. No P-C9 tie/order bound is stated. |
| C:131: “the commit of the id's last immutable-cell edit” | UNDISCLOSED SELECTION POLICY | G:344-347 overwrites a single hash in walk order. Two incomparable edits are not resolved by first-parent provenance or an ancestry-unique maximum. Clock-order variants choose different edit hashes and flip stale/as-of. R:218-297; T:33-48. |
| C:131: “an edit at a commit is a change against its first parent's state” | **FAIL: stronger than code** | G:304-312 searches parents until it finds a usable path state, so it can compare to the second parent instead. G:325 additionally exempts merge re-adds. The absent-first-parent fixture produces a real first-parent registry addition but no event: R:340-395; T:53-62. |
| C:131: “the path walk uses `--full-history`” | PASS, narrowly | G:263-264 uses the flag. The fallback at G:170 does not; P-C9 does not explicitly promise that every auxiliary query uses the flag. The flag alone does not cure the parent-state defect. |
| C:131: S069 stale at `e37dcc6`, no stale ids at the scored r39 tip | PASS | Fresh scored-byte CLI executions give `stale_supersede=[S069]` and `stale_supersede=[]`, respectively: B:3-34,39-70. Both exit 1 with the supplied round base; no exit-0 claim is made here. |
| C:131: selftest carries committed side-superseder and no-fabricated-merge-edit fixtures | PASS for those named fixtures, not general DAG completeness | G:550-557,763-769 exercises the two cases. Full shipped selftest actually returns `pass=12 fail=0`, exit 0: B:75-84. Existing named receipts are `evidence/c9-after-fixture-a.txt:3-6` and `c9-after-fixture-c.txt:3-6`. |
| C:133-136: output is byte-identical **in shape** to v1 | PASS | Same per-id/summary/timing formats; G:389-405. Different values below do not refute shape compatibility. |
| C:135-136: “on linear histories v1 and v2 agree” | **FAIL: stronger than code** | An entirely linear same-cell re-add changes summary, timing, and CLI exit: v1 exit 0 / as-of; v2 exit 1 / stale. R:3-94. The actual-lane receipt is narrower than this sentence. |
| C:145-149: literal declared selftest count `pass=11 fail=0` | DOCUMENTATION MISMATCH | Actual result is 12, not 11 (B:75-84); the assignment already names 12. This stale count is not my primary semantic objection. |

The only explicitly labeled “Disclosed bound” in C:61-65 concerns the C1 verbatim-clone limitation. C:119-154 contains no exception for re-add compatibility, absent-path first parents, or incomparable landing/edit selection. C:168's general “one command…no universal clauses” statement does not define those missing semantics or qualify C:135's explicit linear-history assertion.

## Counterexample 1 — linear re-add breaks the promised compatibility

Constructed committed history (no branching):

`B(original S001) -> E(edit S001 anchor a→b) -> S(add S002 supersedes S001) -> D(remove S001, retain S002) -> R(re-add S001 with the identical b cells)`.

Run each committed gate with `HEAD --repo S/linear-readd --round-base b757edc5657b6ffa63aa746d9f7ea095f6821873`.

| Gate | Exit | round_changed | as-of | stale |
| --- | --- | --- | --- | --- |
| r38 | 0 | `[]` | `[S001]` | `[]` |
| r39 | 1 | `[S001]` | `[]` | `[S001]` |

Evidence: R:13-18,52-57; the parent chain proving linearity is R:88-94. G:325-328 deliberately counts a re-add; T:3-8 confirms the new last edit is R, which the older superseder S does not descend from.

**Impact:** depth and calibration; operability is affected because the round gate's exit changes. This can be a desirable semantic improvement, not a reason to restore the old omission. But it is not compatible with C:135's universal sentence.

**Smallest safe correction:** retain the more conservative re-add event, replace the universal compatibility claim with the actually measured lane-history equivalence, and explicitly disclose same-cell re-add and same-commit landing differences. Since C:8-10 freezes predicates, any predicate change belongs in a new counter version, not an in-place retrospective reinterpretation.

## Counterexample 2 — nearest_path_commit changes the comparison parent

Committed DAG:

- `B -> D(delete corpus/SOURCES.md) -> N(non-registry commit)` is the merge's first-parent line.
- `B -> R(edit S001 a→b) -> S(add S002 supersedes S001)` is the side line.
- `M`, parents **N then S**, restores S's registry tree.

Observed facts:

1. `nearest_path_commit(N)` returns **D**, whose tree does **not** carry the path: R:343-351. Thus the helper's “whose tree carries <path>” docstring at G:163 is false for a deletion.
2. The actual first-parent diff of M adds `corpus/SOURCES.md`; the second-parent diff is empty: T:61-62.
3. G:304-312 rejects D's absent state and continues to S. The resulting ancestry test is R→S, not M→S: T:53-58.
4. `HEAD --repo S/missing-first-parent-path --round-base f1228bc91a454a8588a126534747c364ef1df4c0` returns **exit 0**, `round_changed=[]`, `superseded_as_of=[S001]`: R:354-359. S001 existed before the first-parent deletion; its restoration is not a first introduction.

**Impact:** depth and operability. This is an actual first-parent-state mismatch, not just ambiguity over two equally recent edits. It also demonstrates that the passing A/C/D fixture set is not saturation of the stated parent semantics.

**Smallest safe correction:** resolve the actual first parent's tree state, treating path absence as an empty registry state rather than permission to choose another parent. Distinguish true re-adds from first introductions using that parent's lineage; a blanket merge re-add exemption cannot implement the stated rule. Preserve the named no-fabricated-edit fixture while adding this absent-first-parent case. Alternatively, a deliberately weaker “first usable path-carrying parent, merge re-adds excluded” contract would need to be explicitly bounded and versioned; it is not what the frozen P-C9 says.

The ordinary fallback use case is not inherently broken: an unrelated commit whose tree still carries the registry correctly resolves the previous registry commit, and emits no new immutable edit. Positive control: R:400-447; T:65-70.

## Two incomparable-branch policies — genuine undisclosed tradeoffs

### Latest superseder

`B->E(target edit)->L(S002 superseder)` and `B->R(S003 superseder of the unedited target)` merge with L first. Both superseders survive. Their landing commits are incomparable (R:106-107,166-167). With R dated later, v2 selects S003 and reports stale; reversing only the date ordering selects S002 and reports as-of (R:113-115,173-175). The constructor's only variant is the dates: `S/probe.py:90-97`. The actual tested pairs are E→R versus E→L (T:13-28).

### Last edit

Both branches edit S001, one a→b, the other a→c. Only the b branch adds the superseder; the merge keeps its first parent's b state. With c dated later, v2 attributes the last edit to the discarded side-branch c commit and reports stale. Reverse the date ordering and it selects the b edit, reporting as-of (R:234-236,295-297; T:33-48). Neither edit descends from the other (R:226-228,287-289). The variant changes dates, not registry contents, topology, or parent order: `S/probe.py:99-106`.

**Assessment:** these do not falsify the low-level ancestry check for the pair the program chose. They expose the missing definition of “latest” and “last” on a partial order. Calling the whole result ancestry-based without disclosing its remaining walk-order authorities is stronger than the evidence. An arbitrary total-order policy is a product/contract tradeoff, not a mechanical parent-lookup fix. The smallest honest change is to explicitly define and bound the selected policy in a new version; a stronger ancestry policy would instead need explicit handling of incomparable maximal events. I do not choose that policy or substitute my review for the Rust judge.

## Exercised checks and boundaries

- Executed `python3 S/probe.py`: seven committed scratch histories, CLI evidence from unmodified pinned gate copies, and v1/v2 comparison. All subprocess statuses and stdout are retained in R.
- Executed `python3 -B S/trace.py`: recorded which ancestry pair the analyzer selects, actual first-/second-parent diffs, pinned lane runs, and the shipped selftest. The ancestry wrapper only records and forwards to the unchanged primitive; uninstrumented CLI evidence is retained separately in R. Outputs are T and B.
- No tool installation or update. No tracked lane files, fleet state, configs, routing, or runtime were changed. Git writes occurred only inside this seat's scratch repositories. No additional C1/C2 checks were run.

**Bottom line:** the actual-lane stale verdicts and shipped fixtures pass their narrow observations, but they cannot justify either the universal linear-history agreement sentence or the literal first-parent-state clause. Those are fixable report/implementation defects; incomparable-event selection remains an undisclosed contract choice, not evidence of completed ancestry semantics.
