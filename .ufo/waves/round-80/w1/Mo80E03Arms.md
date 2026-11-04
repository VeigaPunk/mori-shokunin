# Mo80E03Arms — C2 selftest arms

Axes: calibration, operability, coverage. Assigned move: operability only; no score change claimed.

## 1. Implementation

Added the three requested cases inside `selfcheck()` in `.ufo/waves/round-79/count-c2.py`, preserving the existing four cases and labels. The new admission case strips coverage from the reused baseline manifest rows, then adds precisely the requested coverage candidates: non-admitted round 60 and admitted round 47. This prevents the original admitted round 78 from masking the intended admission test. Other axes keep their conformant baseline fixtures.

## 2. Exact retained diff

Command run (exit 0):

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff -U0 -- .ufo/waves/round-79/count-c2.py
```

Output:

```diff
diff --git i/.ufo/waves/round-79/count-c2.py w/.ufo/waves/round-79/count-c2.py
index 84f15b0a..80b4164d 100755
--- i/.ufo/waves/round-79/count-c2.py
+++ w/.ufo/waves/round-79/count-c2.py
@@ -161,0 +162,16 @@ def selfcheck(scratch):
+    admitted = dict(good)
+    admitted["coverage"] = "round 47 (improved, score held)"
+    admitted_rounds = [
+        (rn, adm, {a: v for a, v in verdicts.items() if a != "coverage"})
+        for rn, adm, verdicts in rounds
+    ] + [(60, False, {"coverage": "improved"}),
+         (47, True, {"coverage": "improved"})]
+    cases.append(("nonadmitted_below_ceiling_ignored_met",
+                  admitted, admitted_rounds, True))
+    later_verdict = dict(good)
+    later_verdict["depth"] = "round 78 (score held); round 40 (improved, score held)"
+    cases.append(("verdict_after_clause_boundary_unmet",
+                  later_verdict, rounds, False))
+    later_round = dict(good)
+    later_round["operability"] = "round 40 (score held); round 78 (improved, score held)"
+    cases.append(("later_round_in_cell_ignored_unmet", later_round, rounds, False))
```

The only hunk is an insertion inside `selfcheck()`. Predicate, `grade()`, `expectations()`, module docstring, CLI, summary grammar, and existing case labels are unchanged by this diff.

## 3. Before evidence and acceptance not exercised

Read the frozen contract, harness and entering control receipt with the read tool. The following is **quoted pre-existing evidence**, not a command rerun by this seat:

```text
$ python3 -I .ufo/waves/round-80/mutate-c2.py --rev d5888922
mutant drop_admitted survived rc=0 C2_COUNTER_SELFTEST pass=4 fail=0
mutant raise_ceiling killed rc=1 C2_COUNTER_SELFTEST pass=3 fail=1
mutant count_other_verdicts killed rc=1 C2_COUNTER_SELFTEST pass=3 fail=1
mutant cut_clause_boundary survived rc=0 C2_COUNTER_SELFTEST pass=4 fail=0
mutant any_round_in_cell killed rc=1 C2_COUNTER_SELFTEST pass=3 fail=1
mutant met_ignores_mismatch killed rc=1 C2_COUNTER_SELFTEST pass=1 fail=3
MUTATION_C2 survivors=2 killed=4 total=6 rev=d58889220d3c
rc=1
```

Source: `.ufo/waves/round-80/evidence/controls-r80.txt`, read before editing. The harness docstring instead says three survivors; the measured control and frozen contract say two. No frozen file was changed.

After selftest tally: **not measured by this seat**. After harness line: **not measured by this seat**. The higher-priority fleet-executor instructions prohibit tests during the editing wave and prohibit commits; therefore the requested selftest and scratch fixture commit/harness run were not executed. No clone, scratch directory, fixture commit, tool installation, background job, or external state change was made by this seat. The mutation seat requested snapshot readiness and was told the edits were stable; its independent observations are not claimed here.

Parent acceptance commands (not run here):

```sh
python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/count-c2.py --selftest --scratch <parent-owned-scratch>
python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/mutate-c2.py --rev <integrated-commit> --scratch <parent-owned-scratch>
```

Required targets, not observed results: `C2_COUNTER_SELFTEST pass=7 fail=0` and `MUTATION_C2 survivors=0 killed=6 total=6`, each exit 0.

## 4. Vacuity analysis and risks

Source inspection of the frozen mutant anchors supports these **inferences**, not executed mutation results:

- Admission arm: original expects coverage round 47 and returns met true; `drop_admitted` chooses round 60 and makes that arm fail. Not vacuous against its intended mutant.
- Clause-boundary arm: original reads depth round 78 with no verdict and returns met false; `cut_clause_boundary` reads the later `improved` token and returns met true. Not vacuous against its intended mutant.
- Later-round arm: original reads operability round 40 with no verdict and returns met false; `any_round_in_cell` chooses round 78/improved and returns met true. Not vacuous against its intended mutant. The existing conformant arm already kills this mutant; the added arm is independently sensitive but redundant for the aggregate kill count.

Behavior outside selftesting intentionally unchanged. The existing selfcheck fixture driver creates git repositories without asserting their top-level paths before its add/commit operations; left unchanged because the assignment requires preserving the existing code and this seat did not execute it. No LSP interface is exposed in the mounted tool inventory; no unsupported claim of LSP analysis is made.

## 5. Own defects and self-evaluation

An initial peer message used contradictory wording about the later-round arm being vacuous, then immediately explained the correct nonvacuous behavior; a second message explicitly corrected the wording. No code correction was necessary. An initial commentary exposed internal planning instead of the requested tool-only posture; subsequent work used tool calls.

Self-evaluation: accuracy 4/5 (source-backed diff, but behavioral results unmeasured); completeness 4/5 (implementation and exact diff complete, acceptance reserved to parent by role); clarity 4/5 (explicit observed/inferred/unmeasured separation, initial peer wording corrected); actionability 4/5 (parent commands supplied, integrated revision still required); conciseness 4/5 (exact requested diff retained despite repetition). Mean 4.0/5. Highest-impact next action: parent executes the acceptance commands once after integration. The user should agree with the implementation scope, but acceptance remains unverified here.

## 6. Correction after independent masking finding (supersedes section 4's later-round claim)

After the first handoff, `Mo80M01Mutant` reported its independent snapshot harness killed all six mutants, but the new later-round arm itself still passed under `any_round_in_cell`: the other baseline cells also contained later round-40 clauses, so their mismatches masked the corrected operability cell. This disproved my initial inference of independent sensitivity. The peer-reported aggregate result is not a run by this seat and is not evidence for the final corrected bytes.

Fixed the new fixture initialization only: strip later clauses from every baseline cell before setting the requested operability cell. Thus the other axes remain conformant under the mutant; only operability selects between round 40/no verdict and round 78/improved. Independent sensitivity is now an inference for the corrected bytes, pending the parent's run. Existing four arms remain unchanged. The earlier claim in section 5 that no code correction was necessary is superseded by this correction.

Final requested diff command, rerun after the correction (exit 0):

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff -U0 -- .ufo/waves/round-79/count-c2.py
```

```diff
diff --git i/.ufo/waves/round-79/count-c2.py w/.ufo/waves/round-79/count-c2.py
index 84f15b0a..40a9edd6 100755
--- i/.ufo/waves/round-79/count-c2.py
+++ w/.ufo/waves/round-79/count-c2.py
@@ -161,0 +162,16 @@ def selfcheck(scratch):
+    admitted = dict(good)
+    admitted["coverage"] = "round 47 (improved, score held)"
+    admitted_rounds = [
+        (rn, adm, {a: v for a, v in verdicts.items() if a != "coverage"})
+        for rn, adm, verdicts in rounds
+    ] + [(60, False, {"coverage": "improved"}),
+         (47, True, {"coverage": "improved"})]
+    cases.append(("nonadmitted_below_ceiling_ignored_met",
+                  admitted, admitted_rounds, True))
+    later_verdict = dict(good)
+    later_verdict["depth"] = "round 78 (score held); round 40 (improved, score held)"
+    cases.append(("verdict_after_clause_boundary_unmet",
+                  later_verdict, rounds, False))
+    later_round = {a: cell.split(";")[0] for a, cell in good.items()}
+    later_round["operability"] = "round 40 (score held); round 78 (improved, score held)"
+    cases.append(("later_round_in_cell_ignored_unmet", later_round, rounds, False))
```

No acceptance command was run by this seat after correction. No scratch was created. Accuracy self-rating revised to 3/5: my first vacuity analysis missed aggregate masking; the independent reviewer caught it and the fixture correction addresses that specific cause. Remaining self-ratings unchanged; mean 3.8/5. Final acceptance remains parent-owned.
