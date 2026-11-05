# Mo90E02ArmB1 — structural B1 arm, revised per L1

Axes: calibration (assigned C2); operability (C1 unchanged, not measured).

## Delivered change

Complete candidate: `.ufo/waves/round-90/w1/candidates/r88-count-c1.py`.
Entering source: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show d1c8488986512a6a0475af88cc52779ce4703e00:.ufo/waves/round-88/count-c1.py`.
The command `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD d1c8488986512a6a0475af88cc52779ce4703e00` printed that full hash twice.

Added exactly one arm, `own_ok_arm_count`; EXPECTED_ARMS is 29 and `own_arms_pinned` remains last. Existing arms are untouched. Added `import ast` and updated the docstring pin.

L1 reported that the originally requested functional negative also failed under C1-own-ok, violating isolation. Per L1's subsequent instruction, the final arm instead parses its own source, selects the top-level own_ok_of FunctionDef, and checks its source segment retains EXPECTED_ARMS and `pass=%d fail=0`. This supersedes the initial functional candidate and its earlier report.

## Measured final behavior

Three scratch copies ran concurrently with TMPDIR set to the seat scratch root. Both mutations were extracted from the frozen counter's MUTANTS AST; each anchor occurred exactly once in the final candidate.

- Pristine: rc=0; `C1_COUNTER_SELFTEST pass=29 fail=0`.
- B1-own-ok-arm-count: rc=1; `C1_COUNTER_SELFTEST pass=28 fail=1`; full FAIL-label set `{own_ok_arm_count}`.
- C1-own-ok: rc=1; `C1_COUNTER_SELFTEST pass=28 fail=1`; full FAIL-label set `{own_ok_red}`.

Both sampled kills are attributed and isolated.

### Exact mutation replacements

#### B1-own-ok-arm-count

```python
'r"C1_COUNTER_SELFTEST pass=%d fail=0" % EXPECTED_ARMS, out)'
# replaced with
'r"C1_COUNTER_SELFTEST pass=[0-9]+ fail=0", out)'
```

#### C1-own-ok

```python
'    return (rc == 0 and "C1_COUNTER_SELFTEST" in out'
# replaced with
'    return (True or rc == 0 and "C1_COUNTER_SELFTEST" in out'
```

## Retained complete outputs

### candidate

Command: `python3 -I /fast/scratch/hyaku/mori-r90/Mo90E02ArmB1/candidate.py --selftest --scratch /fast/scratch/hyaku/mori-r90/Mo90E02ArmB1`

Exit: 0

```text
PASS killed_counted mutants=1 killed=1 survivors=0 total=1 arms=1
PASS survivor_counted mutants=1 killed=0 survivors=1 total=1 arms=1
PASS arms_parse 24/0
PASS arms_tally_read arms from subject
PASS pristine_arms_floor 24 wanted
PASS green_boundary green()
PASS killed_boundary killed()
PASS unanchored_excluded mutants=0 killed=0 survivors=0 total=0 arms=1
PASS missing_tally_refused mutants=1 killed=0 survivors=1 total=1 arms=0
PASS zero_mutants_unmet no mutants
PASS empty_mutation_unmet mutants=0 killed=0 survivors=0 total=0 arms=1
PASS red_pristine_reported mutants=1 killed=1 survivors=0 total=1 arms=0
PASS target_split_ok 6/0/6/24
PASS target_split_free 5/1/6
PASS target_arms_free 18
PASS per_file_arms_frozen 24
PASS labels_unique six labels
PASS met_guard_unanchored mutants=1 killed=1 survivors=0 total=1 arms=2
PASS met_guard_empty mutants=1 killed=1 survivors=0 total=1 arms=2
PASS killed_tally_mixed mutants=2 killed=1 survivors=1 total=2 arms=2
PASS arms_tally_passed mutants=1 killed=1 survivors=0 total=1 arms=18
PASS target_split_killed_not_mutants 5 != 6
PASS doubled_anchor_counted_type mutants=0 killed=0 survivors=0 total=0 arms=1
PASS arms_last_tally last of two tallies
PASS green_mixed_fail mixed tallies refused
PASS own_ok_red own_ok_of()
PASS own_ok_arm_count own_ok_of() arm count
PASS marker_literal label
PASS own_arms_pinned 29/29
C1_COUNTER_SELFTEST pass=29 fail=0
```

### B1-own-ok-arm-count

Command: `python3 -I /fast/scratch/hyaku/mori-r90/Mo90E02ArmB1/B1-own-ok-arm-count.py --selftest --scratch /fast/scratch/hyaku/mori-r90/Mo90E02ArmB1`

Exit: 1

```text
PASS killed_counted mutants=1 killed=1 survivors=0 total=1 arms=1
PASS survivor_counted mutants=1 killed=0 survivors=1 total=1 arms=1
PASS arms_parse 24/0
PASS arms_tally_read arms from subject
PASS pristine_arms_floor 24 wanted
PASS green_boundary green()
PASS killed_boundary killed()
PASS unanchored_excluded mutants=0 killed=0 survivors=0 total=0 arms=1
PASS missing_tally_refused mutants=1 killed=0 survivors=1 total=1 arms=0
PASS zero_mutants_unmet no mutants
PASS empty_mutation_unmet mutants=0 killed=0 survivors=0 total=0 arms=1
PASS red_pristine_reported mutants=1 killed=1 survivors=0 total=1 arms=0
PASS target_split_ok 6/0/6/24
PASS target_split_free 5/1/6
PASS target_arms_free 18
PASS per_file_arms_frozen 24
PASS labels_unique six labels
PASS met_guard_unanchored mutants=1 killed=1 survivors=0 total=1 arms=2
PASS met_guard_empty mutants=1 killed=1 survivors=0 total=1 arms=2
PASS killed_tally_mixed mutants=2 killed=1 survivors=1 total=2 arms=2
PASS arms_tally_passed mutants=1 killed=1 survivors=0 total=1 arms=18
PASS target_split_killed_not_mutants 5 != 6
PASS doubled_anchor_counted_type mutants=0 killed=0 survivors=0 total=0 arms=1
PASS arms_last_tally last of two tallies
PASS green_mixed_fail mixed tallies refused
PASS own_ok_red own_ok_of()
FAIL own_ok_arm_count own_ok_of() arm count
PASS marker_literal label
PASS own_arms_pinned 29/29
C1_COUNTER_SELFTEST pass=28 fail=1
```

### C1-own-ok

Command: `python3 -I /fast/scratch/hyaku/mori-r90/Mo90E02ArmB1/C1-own-ok.py --selftest --scratch /fast/scratch/hyaku/mori-r90/Mo90E02ArmB1`

Exit: 1

```text
PASS killed_counted mutants=1 killed=1 survivors=0 total=1 arms=1
PASS survivor_counted mutants=1 killed=0 survivors=1 total=1 arms=1
PASS arms_parse 24/0
PASS arms_tally_read arms from subject
PASS pristine_arms_floor 24 wanted
PASS green_boundary green()
PASS killed_boundary killed()
PASS unanchored_excluded mutants=0 killed=0 survivors=0 total=0 arms=1
PASS missing_tally_refused mutants=1 killed=0 survivors=1 total=1 arms=0
PASS zero_mutants_unmet no mutants
PASS empty_mutation_unmet mutants=0 killed=0 survivors=0 total=0 arms=1
PASS red_pristine_reported mutants=1 killed=1 survivors=0 total=1 arms=0
PASS target_split_ok 6/0/6/24
PASS target_split_free 5/1/6
PASS target_arms_free 18
PASS per_file_arms_frozen 24
PASS labels_unique six labels
PASS met_guard_unanchored mutants=1 killed=1 survivors=0 total=1 arms=2
PASS met_guard_empty mutants=1 killed=1 survivors=0 total=1 arms=2
PASS killed_tally_mixed mutants=2 killed=1 survivors=1 total=2 arms=2
PASS arms_tally_passed mutants=1 killed=1 survivors=0 total=1 arms=18
PASS target_split_killed_not_mutants 5 != 6
PASS doubled_anchor_counted_type mutants=0 killed=0 survivors=0 total=0 arms=1
PASS arms_last_tally last of two tallies
PASS green_mixed_fail mixed tallies refused
FAIL own_ok_red own_ok_of()
PASS own_ok_arm_count own_ok_of() arm count
PASS marker_literal label
PASS own_arms_pinned 29/29
C1_COUNTER_SELFTEST pass=28 fail=1
```

## Bounds and handoff

No production edits, commits, clones, installations, builds, lint or formatter runs. No LSP tool was exposed in this seat; unavailable, not an empty symbol result. All scratch copies and fixtures were removed in finally; observed `SCRATCH_REMOVED True`.

No blocker. The structural arm is intentionally a source-shape pin, not a general behavioral proof. This seat did not run the complete frozen revision-grade C2 matrix; parent owns integration and that gate.

Self-evaluation: accuracy 5 (complete outputs); completeness 5 (revised candidate and both isolated FAIL sets); clarity 4 (long logs preserve evidence); actionability 5 (complete replacement); conciseness 4 (logs intentionally retained). Overall 4.6. Improvement: review summaries first, preserve logs for independent comparison. The user can inspect exact commands, exit codes and all labels.
