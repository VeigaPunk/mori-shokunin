# Mori round 41 — frozen claim and measurement contract

Attempt 1; entering lane tip `62a207f7521fa2e2fcd2e8b0260f047ccfce8862` (r40 closure `corpus/lessons/round-40-verifier-spotcheck.md`). Lowest live axes are depth 5, calibration 5 and freshness 5 (tie); C2 works depth and C3 works calibration. No exploratory claim.

The frozen no-op control is `.ufo/waves/round-41/evidence/control-before.txt`, measured in a disposable clone at the entering tip. Its C1 control passes all nine checks on the honest counter and prints `CONFORM=met` on each of the three routed survivors; its C2 control is the v3 gate, whose dag-h/h2, dag-z/z2 and date-reversed dag-2l outputs contradict the proposed predicate; its C3 control counts six self-assessment mismatches. The initial census is in `evidence/census-start.txt` (229 rows; exit 0, with the existing 16 W04 duplicate-URL warnings).

## C1 — operability 7 (capability acquisition)

**Claim:** the r41 checker fails closed on the three routed function-binding survivors while retaining the honest counter and its selftest. The tested binding inventory is source ordered and covers `Assign`/`AnnAssign`, `NamedExpr`, tuple/list destructuring, and for/with targets. Unresolved target values, unsupported local stores, global/nonlocal function rebinding, and multiple bindings that do not resolve to one finite-positive value fail closed. This is a bounded static subset, not a full Python control-flow proof.
**P-C10 (verbatim predicate):** P-C10 (round 41): the checker rejects the walrus, tuple/list-unpack, and empty-loop-rebind timeout survivors by recording function-local `Assign`/`AnnAssign`, `NamedExpr`, destructuring, and for/with targets in source order. Unresolved targets, unsupported local stores, and multiple bindings that do not all resolve to one finite-positive value fail closed. A `global` read uses the module map only without an in-function global rebind; nonlocal reads and rebinding fail closed. This is a bounded AST binding subset, not a full Python control-flow proof. Each `Popen(` still requires a consumed, same-name `communicate(timeout=…)` drain. `selftest_conjunct` requires the checker to apply each mutation arm and compare its failing-check set, not merely keep the table present. The fourteen-arm selftest includes the three r40 survivor constructions. `head_pin` reports the live repository HEAD; the `rev` argument scopes `timeout_state` only, so measurement receipts use a checkout at the measured commit.

**Frozen target:** `survivor_failures=3`: each of the three fixtures returns `CONFORM=unmet` exit 1 with only `timeout_scope` failing. No-harm guards: the honest counter remains `CONFORM=met`, the 14-arm selftest passes 14/0, and an early-continue mutant fails `selftest_conjunct`. Receipts use a checkout whose live HEAD equals the measured revision.

**Counter:** `python3 .ufo/waves/round-41/fixtures/run-r41-controls.py after <measured-tip> --output .ufo/waves/round-41/evidence/control-after.txt`; it records each exact command and exit.

**Kill rule:** the frozen v3 checker must be unable to reach the survivor target. The control receipt shows `CONFORM=met` on all three, exit 0. Source: S230, opened this round; `corpus/knowledge/conform-bindings-r41.md` cites it.

## C2 — depth 5 (capability acquisition)

**Claim:** P-C12 removes the routed gate-v3 counterexamples while preserving the lane-history classifications.

**P-C12 (verbatim predicate):** P-C12: at revision R, tools/mori-sources-appendonly.py reports the timing line `supersede_timing superseded_as_of=[...] stale_supersede=[...]`; an eligible pair requires both the superseded id and its superseding row to be present at R. Immutable cells and `teaches` use each commit's own header map, while edits remain first-parent comparisons only. A landing is a commit where the pair is absent from every direct parent tree; a delete/re-add therefore creates another landing. For each target, select a candidate landing that is not a strict ancestor of another eligible landing; incomparable maximal candidates tie-break by superseder id, then full landing hash. The selected landing decides `superseded_by` and timing. A never-edited id uses its first-sighting commit; the edit is as-of only when it is an ancestor of or equal to the selected landing. The landed tip target is 36 as-of ids and no stale ids, including S229 superseded by r41 correction row S231; S069 is stale at e37dcc6. Multiple incomparable edits to one id remain a named walk-order residual. Selftest covers the r40 never-edited, first-parent-lacks-path and delete/re-add cases, plus header permutations, superseder rows absent at R, both date orders of dag-2l, and a superseder deleted and re-added after an edit.
**Frozen target:** the single after-value is `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0`. No-harm guards: the landed-tip timing line has 36 as-of IDs and no stale IDs (S231 adds S229); at `e37dcc6`, stale remains `[S069]`.

**Counter:** `python3 .ufo/waves/round-41/fixtures/run-r41-controls.py after <measured-tip> --output .ufo/waves/round-41/evidence/control-after.txt`; the receipt contains the selftest, lane and fixture outputs.

**Kill rule:** the frozen v3 control must fail the routed classes: dag-h fabricates immutable changes, dag-h2 misses the supersede pair, dag-z/z2 report timing for a superseder absent at R, dag-2l changes with commit date, and dag-x misses the later re-add landing. See `control-before.txt`.

## C3 — calibration 5

**Claim:** append-only corrections in SCORECARD, LOG and the round-41 lesson reconcile the round-40 as-of and extension counts to the frozen r40 v3 gate. Historical wrong text remains and is explicitly superseded; LOG and corpus corrections are never rewritten in place.

**Frozen target:** `tools/mori-round41-calibration.py <measured-tip> --repo <repo> --reference-rev 62a207f7521fa2e2fcd2e8b0260f047ccfce8862` reports `MORI_R41_CALIBRATION mismatches=0`. The counter loads the reference gate bytes from the reference commit, derives observed as-of and extension counts, and compares the three current correction records.

**Before → after:** the committed r40 self-assessment carries 34 as-of ids and 16 extension rows, while the r40 gate derives 35 and 17; the frozen control reports six mismatches (the LOG extension value is missing). The target is zero mismatches.

**Causality:** C3 uses the frozen r40 gate reference and correction records, not P-C12, so it is independently measurable from C2.

## Source and freeze boundaries

S230 is the Python 3.13 language reference assignment-statements section, opened 2026-10-24; it grounds the C1 binding inventory. S231 will append-only supersede S229's bad located range/word count (the source copy quote is at `S229.src:294-296`, 17 words). No existing SOURCES row's immutable cells will be edited.

The old head-pin boundary is explicit: receipts named as measured-at a revision use a detached sandbox checkout at that revision. The checker does not claim its `rev` argument binds live HEAD. No dispatch occurs from this lane seat; the prepared 64-member v2 wave is separately recorded and remains undispatched for the orchestrator.