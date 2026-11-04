# Mo88M01Mut — r88 selftest mutation matrix

Axes: sensitivity, printed-target exposure, exact restoration, bounded runtime. Detection only. No lane counter edits, mutated lane-target runs, clones, fixture commits, installs, agents, or shell background jobs. Four bounded foreground worker threads.

Frozen revision: `d5e2eda494877a85edaa4e287d6ad81843d9a8a1`. Lane HEAD before: `9c775ac2131da13c4c4cfdf2b14077184076f557`; after: `9c775ac2131da13c4c4cfdf2b14077184076f557`.

## Hash integrity

| File | frozen SHA-256 | lane before | lane after |
|---|---|---|---|
| c1 | `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2` | `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2` | `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2` |
| c2 | `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7` | `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7` | `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7` |

Each probe runs pristine, mutant, exact-byte-restored with same detector (scratch directory differs). Baseline/restoration require rc=0 and pinned green tally: C1 pass=25 fail=0; C2 pass=17 fail=0. Otherwise inconclusive. Kill: nonzero exit or positive fail count. Complete actual outputs and hashes below.

Two initial setup attempts aborted before any detector because anchors also appeared inside frozen mutant string literals (anchor guard, then met guard). Both scratch trees removed by EXIT traps. Final driver excludes string-token occurrences when tightening ambiguous anchors; every recorded anchor below occurs exactly once.

## Matrix

| File | mutant | exact unique anchor → replacement (JSON) | verdict | rc; FAIL arms; tally |
|---|---|---|---|---|
| c1 | C1-target | `"TARGET = (6, 0, 6)" → "TARGET = (5, 0, 6)"` | killed | rc=1; FAIL target_split_ok 6/0/6/24<br>FAIL target_split_killed_not_mutants 5 != 6<br>C1_COUNTER_SELFTEST pass=23 fail=2 |
| c1 | C1-target-arms | `"TARGET_ARMS = 24" → "TARGET_ARMS = 18"` | killed | rc=1; FAIL target_split_ok 6/0/6/24<br>FAIL target_arms_free 18<br>FAIL per_file_arms_frozen 24<br>C1_COUNTER_SELFTEST pass=22 fail=3 |
| c1 | C1-kill-and | `"return rc != 0 or bool(FAIL.search(out))" → "return rc != 0 and bool(FAIL.search(out))"` | killed | rc=1; FAIL killed_boundary killed()<br>C1_COUNTER_SELFTEST pass=24 fail=1 |
| c1 | C1-green-drop-fail | `"return rc == 0 and \"fail=0\" in out and not FAIL.search(out)" → "return rc == 0 and \"fail=0\" in out"` | survived | rc=0; C1_COUNTER_SELFTEST pass=25 fail=0 |
| c1 | C1-arms-first | `"for m in ARMS.finditer(out):\n        pass" → "for m in ARMS.finditer(out):\n        break"` | survived | rc=0; C1_COUNTER_SELFTEST pass=25 fail=0 |
| c1 | C1-anchor | `"            if base.count(old) != 1:\n" → "            if base.count(old) == 0:\n"` | killed | rc=1; FAIL unanchored_excluded mutants=1 killed=0 survivors=1 total=1 arms=1<br>FAIL met_guard_unanchored mutants=2 killed=1 survivors=1 total=2 arms=2<br>FAIL doubled_anchor_counted_type mutants=1 killed=0 survivors=1 total=1 arms=1<br>C1_COUNTER_SELFTEST pass=22 fail=3 |
| c1 | C1-total-before-anchor | `"        for label, old, new in by_file[path]:\n" → "        for label, old, new in by_file[path]:\n            total += 1\n"` | killed | rc=1; FAIL killed_counted mutants=2 killed=2 survivors=0 total=2 arms=1<br>FAIL met_guard_unanchored mutants=3 killed=3 survivors=0 total=3 arms=2<br>FAIL met_guard_empty mutants=3 killed=3 survivors=0 total=3 arms=2<br>FAIL killed_tally_mixed mutants=4 killed=3 survivors=1 total=4 arms=2<br>FAIL doubled_anchor_counted_type mutants=1 killed=1 survivors=0 total=1 arms=1<br>C1_COUNTER_SELFTEST pass=20 fail=5 |
| c1 | C1-killed-total | `"    killed_n = total - survivors\n" → "    killed_n = total\n"` | killed | rc=1; FAIL killed_tally_mixed mutants=2 killed=2 survivors=1 total=2 arms=2<br>C1_COUNTER_SELFTEST pass=24 fail=1 |
| c1 | C1-arms-total | `"        arms_total += max(passed, 0)\n" → "        arms_total += 1\n"` | killed | rc=1; FAIL arms_tally_passed mutants=1 killed=1 survivors=0 total=1 arms=1<br>C1_COUNTER_SELFTEST pass=24 fail=1 |
| c1 | C1-split-field | `"return (fields.get(\"killed\"), fields.get(\"survivors\")," → "return (fields.get(\"mutants\"), fields.get(\"survivors\"),"` | killed | rc=1; FAIL target_split_killed_not_mutants 5 != 6<br>C1_COUNTER_SELFTEST pass=24 fail=1 |
| c1 | C1-own-ok | `"own_ok = (own.returncode == 0 and \"C1_COUNTER_SELFTEST\" in own_out" → "own_ok = (True or own.returncode == 0 and \"C1_COUNTER_SELFTEST\" in own_out"` | survived | rc=0; C1_COUNTER_SELFTEST pass=25 fail=0 |
| c1 | C1-expected-arms | `"EXPECTED_ARMS = 25" → "EXPECTED_ARMS = 24"` | killed | rc=1; FAIL own_arms_pinned 25/24<br>C1_COUNTER_SELFTEST pass=24 fail=1 |
| c1 | C1-met-guard | `"           and not any(e.startswith((\"empty-mutation\", \"unanchored\")) for e in extras))\n" → "           and True)\n"` | killed | rc=1; FAIL met_guard_unanchored mutants=1 killed=1 survivors=0 total=1 arms=2<br>FAIL met_guard_empty mutants=1 killed=1 survivors=0 total=1 arms=2<br>C1_COUNTER_SELFTEST pass=23 fail=2 |
| c1 | C1-printed-split | `"% (total, killed_n, survivors, total, arms_total))" → "% (total, total, survivors, total, arms_total))"` | killed | rc=1; FAIL killed_tally_mixed mutants=2 killed=2 survivors=1 total=2 arms=2<br>C1_COUNTER_SELFTEST pass=24 fail=1 |
| c1 | C1-arm-file-pin | `"ARMS_BY_FILE = {\"count-c1.py\": 24}" → "ARMS_BY_FILE = {\"count-c1.py\": 18}"` | killed | rc=1; FAIL per_file_arms_frozen 24<br>C1_COUNTER_SELFTEST pass=24 fail=1 |
| c1 | C1-pristine-guard | `"met = (pristine_ok and total > 0 and survivors == 0" → "met = (True and total > 0 and survivors == 0"` | killed | rc=1; FAIL pristine_arms_floor 24 wanted<br>FAIL red_pristine_reported mutants=1 killed=1 survivors=0 total=1 arms=0<br>C1_COUNTER_SELFTEST pass=23 fail=2 |
| c2 | C2-target | `"TARGET = \"real=met fx=4 clean=1 refused=2 absent=1 arms=23\"" → "TARGET = \"real=unmet fx=4 clean=1 refused=2 absent=1 arms=23\""` | survived | rc=0; C2_COUNTER_SELFTEST pass=17 fail=0 |
| c2 | C2-subject-arms | `"SUBJECT_ARMS = 23" → "SUBJECT_ARMS = 17"` | killed | rc=1; FAIL arms_pinned 23<br>C2_COUNTER_SELFTEST pass=16 fail=1 |
| c2 | C2-own-ok | `"own_ok = (own.returncode == 0" → "own_ok = (True or own.returncode == 0"` | survived | rc=0; C2_COUNTER_SELFTEST pass=17 fail=0 |
| c2 | C2-fixture-clean | `"return verdict.startswith(\"C2=met \" + REAL), verdict or \"no verdict line\"" → "return verdict.startswith(\"C2=met \"), verdict or \"no verdict line\""` | survived | rc=0; C2_COUNTER_SELFTEST pass=17 fail=0 |
| c2 | C2-fixture-problem | `"return problem in line.group(3), \"problems=\" + line.group(3)" → "return True, \"problems=\" + line.group(3)"` | killed | rc=1; FAIL wrong_problem_not_bound cmd-binding<br>C2_COUNTER_SELFTEST pass=16 fail=1 |
| c2 | C2-receipt-name | `"if m and m.group(1) == name:" → "if m:"` | survived | rc=0; C2_COUNTER_SELFTEST pass=17 fail=0 |
| c2 | C2-absent-lines | `"if SUPERSEDE.match(line)]" → "if SUPERSEDE.match(line) and False]"` | killed | rc=1; FAIL absent_target_refused absent=1<br>C2_COUNTER_SELFTEST pass=16 fail=1 |
| c2 | C2-stripped | `"head = [line for line in head if not REPLAY_LINE.match(line)]" → "head = [line for line in head if REPLAY_LINE.match(line)]"` | killed | rc=1; FAIL stripped_drops_replay no replay<br>C2_COUNTER_SELFTEST pass=16 fail=1 |
| c2 | C2-vacuous | `"if line.startswith(\"# cmd:\") else line) for line in head]" → "if False else line) for line in head]"` | killed | rc=1; FAIL vacuous_rewrites_cmd printf cmd<br>C2_COUNTER_SELFTEST pass=16 fail=1 |
| c2 | C2-absent-target | `"if SUPERSEDE_LINE.match(line) else line) for line in head]" → "if False else line) for line in head]"` | killed | rc=1; FAIL absent_rewrites_target gone target<br>C2_COUNTER_SELFTEST pass=16 fail=1 |
| c2 | C2-clone-top | `"if top.stdout.strip() != os.path.realpath(d):" → "if False:"` | survived | rc=0; C2_COUNTER_SELFTEST pass=17 fail=0 |
| c2 | C2-verdict-first | `"last = line\n    return last" → "last = line\n            break\n    return last"` | survived | rc=0; C2_COUNTER_SELFTEST pass=17 fail=0 |
| c2 | C2-absent-binding | `"return bool(lines) and verdict.startswith(\"C2=unmet\")," → "return verdict.startswith(\"C2=unmet\"),"` | killed | rc=1; FAIL absent_without_line no SUPERSEDE<br>C2_COUNTER_SELFTEST pass=16 fail=1 |
| c2 | C2-printed-target | `"print(\"C2=met %s rev=%s\" % (TARGET, rev[:12]))" → "print(\"C2=met %s rev=%s\" % (\"real=unmet fx=4 clean=1 refused=2 absent=1 arms=23\", rev[:12]))"` | survived | rc=0; C2_COUNTER_SELFTEST pass=17 fail=0 |
| c2 | C2-vacuous-body | `"        body = [\"RECORD_SWEEP fabricated=1\"]\n    elif kind == \"absent-target\":" → "        body = body\n    elif kind == \"absent-target\":"` | survived | rc=0; C2_COUNTER_SELFTEST pass=17 fail=0 |
| c2 | C2-no-supersedes | `"raise ValueError(\"fixture receipt has no '# supersedes:' line\")" → "pass"` | survived | rc=0; C2_COUNTER_SELFTEST pass=17 fail=0 |

Totals: **32 mutants; 20 killed; 12 survived; 0 inconclusive**.

## Ranked survivors and round-89 witnesses

Source-flow exposure rankings are inference, not observed lane-target effects. Tier 1 directly affects acceptance/printed-target integrity; tier 2 affects fixture construction. Main-only mutations were exercised only via --selftest.
1. **C1-arms-first**, tier 1: Two tally lines; red final tally dominates.
2. **C1-green-drop-fail**, tier 1: Reject mixed fail=0 and fail=2 output.
3. **C1-own-ok**, tier 1: Synthetic main invocation with red own detector, otherwise passing grading; require detector=red.
4. **C2-clone-top**, tier 1: Stub run with mismatched clone root; reject before writes/add/commit.
5. **C2-fixture-clean**, tier 1: Reject clean met with wrong population split.
6. **C2-own-ok**, tier 1: Synthetic main with red own detector and otherwise passing subject/fixtures.
7. **C2-printed-target**, tier 1: Exercise main with synthetic adapters; assert exact printed target.
8. **C2-receipt-name**, tier 1: Reason on different receipt must not satisfy fixture.
9. **C2-target**, tier 1: Assert entire TARGET including real=met, not only five substrings.
10. **C2-verdict-first**, tier 1: Two verdict lines; final verdict dominates.
11. **C2-no-supersedes**, tier 2: Absent-target without supersedes must raise ValueError.
12. **C2-vacuous-body**, tier 2: Assert vacuous body is fabricated not original TOKEN.

## Actual detector outputs and exact restoration hashes

### C1-target

Before: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`; mutant: `46ded58ca5e3f4667d28e37b8e055e3dd4be07541e8301622601c321b877fe2c`; restored: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-target/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-target/baseline`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

**mutated**, rc=1; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-target/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-target/mutated`
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
FAIL target_split_ok 6/0/6/24
PASS target_split_free 5/1/6
PASS target_arms_free 18
PASS per_file_arms_frozen 24
PASS labels_unique six labels
PASS met_guard_unanchored mutants=1 killed=1 survivors=0 total=1 arms=2
PASS met_guard_empty mutants=1 killed=1 survivors=0 total=1 arms=2
PASS killed_tally_mixed mutants=2 killed=1 survivors=1 total=2 arms=2
PASS arms_tally_passed mutants=1 killed=1 survivors=0 total=1 arms=18
FAIL target_split_killed_not_mutants 5 != 6
PASS doubled_anchor_counted_type mutants=0 killed=0 survivors=0 total=0 arms=1
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=23 fail=2
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-target/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-target/restored`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

### C1-target-arms

Before: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`; mutant: `3adffa9094572b9167de66938417df7878f33d3173323c45ef9cc716af4f8252`; restored: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-target-arms/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-target-arms/baseline`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

**mutated**, rc=1; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-target-arms/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-target-arms/mutated`
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
FAIL target_split_ok 6/0/6/24
PASS target_split_free 5/1/6
FAIL target_arms_free 18
FAIL per_file_arms_frozen 24
PASS labels_unique six labels
PASS met_guard_unanchored mutants=1 killed=1 survivors=0 total=1 arms=2
PASS met_guard_empty mutants=1 killed=1 survivors=0 total=1 arms=2
PASS killed_tally_mixed mutants=2 killed=1 survivors=1 total=2 arms=2
PASS arms_tally_passed mutants=1 killed=1 survivors=0 total=1 arms=18
PASS target_split_killed_not_mutants 5 != 6
PASS doubled_anchor_counted_type mutants=0 killed=0 survivors=0 total=0 arms=1
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=22 fail=3
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-target-arms/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-target-arms/restored`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

### C1-kill-and

Before: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`; mutant: `e759588e5afc354c9c9bb126eb3fb543801ff61644c515ef956ddfcbee3a0e1a`; restored: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-kill-and/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-kill-and/baseline`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

**mutated**, rc=1; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-kill-and/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-kill-and/mutated`
```text
PASS killed_counted mutants=1 killed=1 survivors=0 total=1 arms=1
PASS survivor_counted mutants=1 killed=0 survivors=1 total=1 arms=1
PASS arms_parse 24/0
PASS arms_tally_read arms from subject
PASS pristine_arms_floor 24 wanted
PASS green_boundary green()
FAIL killed_boundary killed()
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=24 fail=1
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-kill-and/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-kill-and/restored`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

### C1-green-drop-fail

Before: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`; mutant: `8e064c9f0e84c157ede4fb507aa0a76cf7b278593fc666d099c1001e10aa9753`; restored: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-green-drop-fail/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-green-drop-fail/baseline`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

**mutated**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-green-drop-fail/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-green-drop-fail/mutated`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-green-drop-fail/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-green-drop-fail/restored`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

### C1-arms-first

Before: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`; mutant: `055992f5fa9026a598c35005d0d7f8db49421b543a71bbcd290795bc7aaaa6cc`; restored: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-arms-first/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-arms-first/baseline`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

**mutated**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-arms-first/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-arms-first/mutated`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-arms-first/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-arms-first/restored`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

### C1-anchor

Before: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`; mutant: `0ea71011dd48081a88337a74a1b77b77598986d537ca63eb83e2cebf47519aad`; restored: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-anchor/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-anchor/baseline`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

**mutated**, rc=1; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-anchor/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-anchor/mutated`
```text
PASS killed_counted mutants=1 killed=1 survivors=0 total=1 arms=1
PASS survivor_counted mutants=1 killed=0 survivors=1 total=1 arms=1
PASS arms_parse 24/0
PASS arms_tally_read arms from subject
PASS pristine_arms_floor 24 wanted
PASS green_boundary green()
PASS killed_boundary killed()
FAIL unanchored_excluded mutants=1 killed=0 survivors=1 total=1 arms=1
PASS missing_tally_refused mutants=1 killed=0 survivors=1 total=1 arms=0
PASS zero_mutants_unmet no mutants
PASS empty_mutation_unmet mutants=0 killed=0 survivors=0 total=0 arms=1
PASS red_pristine_reported mutants=1 killed=1 survivors=0 total=1 arms=0
PASS target_split_ok 6/0/6/24
PASS target_split_free 5/1/6
PASS target_arms_free 18
PASS per_file_arms_frozen 24
PASS labels_unique six labels
FAIL met_guard_unanchored mutants=2 killed=1 survivors=1 total=2 arms=2
PASS met_guard_empty mutants=1 killed=1 survivors=0 total=1 arms=2
PASS killed_tally_mixed mutants=2 killed=1 survivors=1 total=2 arms=2
PASS arms_tally_passed mutants=1 killed=1 survivors=0 total=1 arms=18
PASS target_split_killed_not_mutants 5 != 6
FAIL doubled_anchor_counted_type mutants=1 killed=0 survivors=1 total=1 arms=1
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=22 fail=3
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-anchor/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-anchor/restored`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

### C1-total-before-anchor

Before: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`; mutant: `f715fa06f057fe7b6d42dee6860caec6883f315be2c3f11dd8f31285950d8e45`; restored: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-total-before-anchor/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-total-before-anchor/baseline`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

**mutated**, rc=1; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-total-before-anchor/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-total-before-anchor/mutated`
```text
FAIL killed_counted mutants=2 killed=2 survivors=0 total=2 arms=1
PASS survivor_counted mutants=2 killed=1 survivors=1 total=2 arms=1
PASS arms_parse 24/0
PASS arms_tally_read arms from subject
PASS pristine_arms_floor 24 wanted
PASS green_boundary green()
PASS killed_boundary killed()
PASS unanchored_excluded mutants=1 killed=1 survivors=0 total=1 arms=1
PASS missing_tally_refused mutants=2 killed=1 survivors=1 total=2 arms=0
PASS zero_mutants_unmet no mutants
PASS empty_mutation_unmet mutants=1 killed=1 survivors=0 total=1 arms=1
PASS red_pristine_reported mutants=2 killed=2 survivors=0 total=2 arms=0
PASS target_split_ok 6/0/6/24
PASS target_split_free 5/1/6
PASS target_arms_free 18
PASS per_file_arms_frozen 24
PASS labels_unique six labels
FAIL met_guard_unanchored mutants=3 killed=3 survivors=0 total=3 arms=2
FAIL met_guard_empty mutants=3 killed=3 survivors=0 total=3 arms=2
FAIL killed_tally_mixed mutants=4 killed=3 survivors=1 total=4 arms=2
PASS arms_tally_passed mutants=2 killed=2 survivors=0 total=2 arms=18
PASS target_split_killed_not_mutants 5 != 6
FAIL doubled_anchor_counted_type mutants=1 killed=1 survivors=0 total=1 arms=1
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=20 fail=5
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-total-before-anchor/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-total-before-anchor/restored`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

### C1-killed-total

Before: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`; mutant: `d0017abbf1d0b07027a703b37bb18821f0682ee689120452dc9c53dafa595662`; restored: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-killed-total/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-killed-total/baseline`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

**mutated**, rc=1; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-killed-total/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-killed-total/mutated`
```text
PASS killed_counted mutants=1 killed=1 survivors=0 total=1 arms=1
PASS survivor_counted mutants=1 killed=1 survivors=1 total=1 arms=1
PASS arms_parse 24/0
PASS arms_tally_read arms from subject
PASS pristine_arms_floor 24 wanted
PASS green_boundary green()
PASS killed_boundary killed()
PASS unanchored_excluded mutants=0 killed=0 survivors=0 total=0 arms=1
PASS missing_tally_refused mutants=1 killed=1 survivors=1 total=1 arms=0
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
FAIL killed_tally_mixed mutants=2 killed=2 survivors=1 total=2 arms=2
PASS arms_tally_passed mutants=1 killed=1 survivors=0 total=1 arms=18
PASS target_split_killed_not_mutants 5 != 6
PASS doubled_anchor_counted_type mutants=0 killed=0 survivors=0 total=0 arms=1
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=24 fail=1
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-killed-total/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-killed-total/restored`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

### C1-arms-total

Before: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`; mutant: `048aa622abd4a527c0429fb64082ff9ad09af13c1cddc7de8075917172632864`; restored: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-arms-total/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-arms-total/baseline`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

**mutated**, rc=1; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-arms-total/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-arms-total/mutated`
```text
PASS killed_counted mutants=1 killed=1 survivors=0 total=1 arms=1
PASS survivor_counted mutants=1 killed=0 survivors=1 total=1 arms=1
PASS arms_parse 24/0
PASS arms_tally_read arms from subject
PASS pristine_arms_floor 24 wanted
PASS green_boundary green()
PASS killed_boundary killed()
PASS unanchored_excluded mutants=0 killed=0 survivors=0 total=0 arms=1
PASS missing_tally_refused mutants=1 killed=0 survivors=1 total=1 arms=1
PASS zero_mutants_unmet no mutants
PASS empty_mutation_unmet mutants=0 killed=0 survivors=0 total=0 arms=1
PASS red_pristine_reported mutants=1 killed=1 survivors=0 total=1 arms=1
PASS target_split_ok 6/0/6/24
PASS target_split_free 5/1/6
PASS target_arms_free 18
PASS per_file_arms_frozen 24
PASS labels_unique six labels
PASS met_guard_unanchored mutants=1 killed=1 survivors=0 total=1 arms=2
PASS met_guard_empty mutants=1 killed=1 survivors=0 total=1 arms=2
PASS killed_tally_mixed mutants=2 killed=1 survivors=1 total=2 arms=2
FAIL arms_tally_passed mutants=1 killed=1 survivors=0 total=1 arms=1
PASS target_split_killed_not_mutants 5 != 6
PASS doubled_anchor_counted_type mutants=0 killed=0 survivors=0 total=0 arms=1
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=24 fail=1
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-arms-total/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-arms-total/restored`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

### C1-split-field

Before: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`; mutant: `2a2741eff1fbccbf44e5f29321164c77c07652b67aa27331c1a1e1925d6ae116`; restored: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-split-field/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-split-field/baseline`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

**mutated**, rc=1; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-split-field/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-split-field/mutated`
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
FAIL target_split_killed_not_mutants 5 != 6
PASS doubled_anchor_counted_type mutants=0 killed=0 survivors=0 total=0 arms=1
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=24 fail=1
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-split-field/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-split-field/restored`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

### C1-own-ok

Before: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`; mutant: `b89a4336be72dc4a972ccd409ad0601c3fed5924b36a6f1d0fb68b777f579bc6`; restored: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-own-ok/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-own-ok/baseline`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

**mutated**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-own-ok/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-own-ok/mutated`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-own-ok/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-own-ok/restored`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

### C1-expected-arms

Before: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`; mutant: `81b4f8e262fb52dd872be8492de5472314da48fcc0f1612409c50ce756903319`; restored: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-expected-arms/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-expected-arms/baseline`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

**mutated**, rc=1; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-expected-arms/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-expected-arms/mutated`
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
PASS marker_literal label
FAIL own_arms_pinned 25/24
C1_COUNTER_SELFTEST pass=24 fail=1
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-expected-arms/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-expected-arms/restored`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

### C1-met-guard

Before: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`; mutant: `64a739f6150fb3423f97bafd0e90a785c7b057d87b6313e74881af059c239748`; restored: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-met-guard/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-met-guard/baseline`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

**mutated**, rc=1; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-met-guard/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-met-guard/mutated`
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
FAIL met_guard_unanchored mutants=1 killed=1 survivors=0 total=1 arms=2
FAIL met_guard_empty mutants=1 killed=1 survivors=0 total=1 arms=2
PASS killed_tally_mixed mutants=2 killed=1 survivors=1 total=2 arms=2
PASS arms_tally_passed mutants=1 killed=1 survivors=0 total=1 arms=18
PASS target_split_killed_not_mutants 5 != 6
PASS doubled_anchor_counted_type mutants=0 killed=0 survivors=0 total=0 arms=1
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=23 fail=2
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-met-guard/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-met-guard/restored`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

### C1-printed-split

Before: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`; mutant: `53c407a18ffd3136686ae4fc32ae12cdc6dfda0adb22b615835b066838d0a39a`; restored: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-printed-split/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-printed-split/baseline`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

**mutated**, rc=1; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-printed-split/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-printed-split/mutated`
```text
PASS killed_counted mutants=1 killed=1 survivors=0 total=1 arms=1
PASS survivor_counted mutants=1 killed=1 survivors=1 total=1 arms=1
PASS arms_parse 24/0
PASS arms_tally_read arms from subject
PASS pristine_arms_floor 24 wanted
PASS green_boundary green()
PASS killed_boundary killed()
PASS unanchored_excluded mutants=0 killed=0 survivors=0 total=0 arms=1
PASS missing_tally_refused mutants=1 killed=1 survivors=1 total=1 arms=0
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
FAIL killed_tally_mixed mutants=2 killed=2 survivors=1 total=2 arms=2
PASS arms_tally_passed mutants=1 killed=1 survivors=0 total=1 arms=18
PASS target_split_killed_not_mutants 5 != 6
PASS doubled_anchor_counted_type mutants=0 killed=0 survivors=0 total=0 arms=1
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=24 fail=1
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-printed-split/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-printed-split/restored`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

### C1-arm-file-pin

Before: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`; mutant: `73535f96f45cad0d99a8b824e248852d98aecd56e1af294853e95b852f189de3`; restored: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-arm-file-pin/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-arm-file-pin/baseline`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

**mutated**, rc=1; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-arm-file-pin/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-arm-file-pin/mutated`
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
FAIL per_file_arms_frozen 24
PASS labels_unique six labels
PASS met_guard_unanchored mutants=1 killed=1 survivors=0 total=1 arms=2
PASS met_guard_empty mutants=1 killed=1 survivors=0 total=1 arms=2
PASS killed_tally_mixed mutants=2 killed=1 survivors=1 total=2 arms=2
PASS arms_tally_passed mutants=1 killed=1 survivors=0 total=1 arms=18
PASS target_split_killed_not_mutants 5 != 6
PASS doubled_anchor_counted_type mutants=0 killed=0 survivors=0 total=0 arms=1
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=24 fail=1
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-arm-file-pin/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-arm-file-pin/restored`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

### C1-pristine-guard

Before: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`; mutant: `cf2c07a95245c75328452bf56d5d5200d3a7670f12996c259ce56dc33495729f`; restored: `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-pristine-guard/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-pristine-guard/baseline`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

**mutated**, rc=1; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-pristine-guard/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-pristine-guard/mutated`
```text
PASS killed_counted mutants=1 killed=1 survivors=0 total=1 arms=1
PASS survivor_counted mutants=1 killed=0 survivors=1 total=1 arms=1
PASS arms_parse 24/0
PASS arms_tally_read arms from subject
FAIL pristine_arms_floor 24 wanted
PASS green_boundary green()
PASS killed_boundary killed()
PASS unanchored_excluded mutants=0 killed=0 survivors=0 total=0 arms=1
PASS missing_tally_refused mutants=1 killed=0 survivors=1 total=1 arms=0
PASS zero_mutants_unmet no mutants
PASS empty_mutation_unmet mutants=0 killed=0 survivors=0 total=0 arms=1
FAIL red_pristine_reported mutants=1 killed=1 survivors=0 total=1 arms=0
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=23 fail=2
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-pristine-guard/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C1-pristine-guard/restored`
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
PASS marker_literal label
PASS own_arms_pinned 25/25
C1_COUNTER_SELFTEST pass=25 fail=0
```

### C2-target

Before: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`; mutant: `92caa388d08c70ee2494923a490c70d0326d19138c70f36bb9a0ada768636e44`; restored: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-target/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-target/baseline`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**mutated**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-target/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-target/mutated`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-target/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-target/restored`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

### C2-subject-arms

Before: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`; mutant: `edc3f8b8b7d665f335611464487d469038cc4a1db22e52170c38ad502d859e14`; restored: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-subject-arms/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-subject-arms/baseline`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**mutated**, rc=1; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-subject-arms/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-subject-arms/mutated`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
FAIL arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=16 fail=1
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-subject-arms/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-subject-arms/restored`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

### C2-own-ok

Before: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`; mutant: `fa03b1a9dfe04301661b08d5c4220c908fb9372752ce26c1646ff3f73bcbfdd8`; restored: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-own-ok/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-own-ok/baseline`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**mutated**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-own-ok/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-own-ok/mutated`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-own-ok/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-own-ok/restored`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

### C2-fixture-clean

Before: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`; mutant: `c69b49c5c4e194ed0155d4c43229f8bb7850bae667ef9a40085f63d9796388b9`; restored: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-fixture-clean/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-fixture-clean/baseline`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**mutated**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-fixture-clean/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-fixture-clean/mutated`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-fixture-clean/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-fixture-clean/restored`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

### C2-fixture-problem

Before: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`; mutant: `fad48f9a39050fe8ad1996ab24edaeea42204681886d3d699df27968a800879f`; restored: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-fixture-problem/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-fixture-problem/baseline`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**mutated**, rc=1; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-fixture-problem/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-fixture-problem/mutated`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
FAIL wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=16 fail=1
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-fixture-problem/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-fixture-problem/restored`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

### C2-receipt-name

Before: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`; mutant: `24e709586c9a378b6d020022dc7e4cb52371560ec0bf9971de13b3623002a52c`; restored: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-receipt-name/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-receipt-name/baseline`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**mutated**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-receipt-name/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-receipt-name/mutated`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-receipt-name/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-receipt-name/restored`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

### C2-absent-lines

Before: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`; mutant: `55367c3f9ac95fde199a03db6853419b9c048b55955c289dbd35d32e753f4776`; restored: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-absent-lines/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-absent-lines/baseline`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**mutated**, rc=1; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-absent-lines/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-absent-lines/mutated`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
FAIL absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=16 fail=1
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-absent-lines/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-absent-lines/restored`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

### C2-stripped

Before: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`; mutant: `0ab42673e07af74529188303b39f9f25bfef0f27d3e39804bc92e15ed59e8f7a`; restored: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-stripped/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-stripped/baseline`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**mutated**, rc=1; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-stripped/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-stripped/mutated`
```text
PASS clean_identity identity
FAIL stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=16 fail=1
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-stripped/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-stripped/restored`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

### C2-vacuous

Before: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`; mutant: `7818d10d3dd077fca978d8e647fdc3e224aa3e9556b7ffdafb7a2fb570f0768b`; restored: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-vacuous/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-vacuous/baseline`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**mutated**, rc=1; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-vacuous/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-vacuous/mutated`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
FAIL vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=16 fail=1
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-vacuous/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-vacuous/restored`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

### C2-absent-target

Before: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`; mutant: `e907741c524913b104a4b954e37713bc964afc2823d4557f91eef477203b7448`; restored: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-absent-target/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-absent-target/baseline`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**mutated**, rc=1; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-absent-target/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-absent-target/mutated`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
FAIL absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=16 fail=1
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-absent-target/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-absent-target/restored`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

### C2-clone-top

Before: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`; mutant: `4b9ff9e40711f3f20aff90c8aeee0e9049abba6d54e4e143cfd09253db1bfcba`; restored: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-clone-top/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-clone-top/baseline`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**mutated**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-clone-top/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-clone-top/mutated`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-clone-top/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-clone-top/restored`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

### C2-verdict-first

Before: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`; mutant: `17bfc5b728a45ead70754a6ce6d14e38d789f68a8654bffe14efee7d0e280c8e`; restored: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-verdict-first/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-verdict-first/baseline`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**mutated**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-verdict-first/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-verdict-first/mutated`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-verdict-first/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-verdict-first/restored`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

### C2-absent-binding

Before: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`; mutant: `83ff4263e6d8b227ae4687c26a4b3589c6f0eef0a617ef075c1b0be34360f5fe`; restored: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-absent-binding/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-absent-binding/baseline`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**mutated**, rc=1; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-absent-binding/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-absent-binding/mutated`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
FAIL absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=16 fail=1
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-absent-binding/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-absent-binding/restored`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

### C2-printed-target

Before: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`; mutant: `73fca620a5d84b4cb76561f5094c816a5747980f7823eeca456f3fcb008a39f3`; restored: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-printed-target/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-printed-target/baseline`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**mutated**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-printed-target/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-printed-target/mutated`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-printed-target/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-printed-target/restored`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

### C2-vacuous-body

Before: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`; mutant: `cceb853d3fa97827efcea6a6635c0b9500e65ed0e178ca8127587d66de9d0b10`; restored: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-vacuous-body/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-vacuous-body/baseline`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**mutated**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-vacuous-body/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-vacuous-body/mutated`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-vacuous-body/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-vacuous-body/restored`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

### C2-no-supersedes

Before: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`; mutant: `c647b24c2c0f0d0bb9096823513b1903eacd20af050a20cb7e220cda2634a06e`; restored: `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7`.

**baseline**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-no-supersedes/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-no-supersedes/baseline`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**mutated**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-no-supersedes/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-no-supersedes/mutated`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

**restored**, rc=0; `python3 -I /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-no-supersedes/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88M01Mut/C2-no-supersedes/restored`
```text
PASS clean_identity identity
PASS stripped_drops_replay no replay
PASS vacuous_rewrites_cmd printf cmd
PASS absent_rewrites_target gone target
PASS unknown_kind_refused ValueError
PASS no_cmd_refused ValueError
PASS verdict_met C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=abc
PASS missing_replay_refused missing-replay
PASS cmd_binding_refused cmd-binding
PASS absent_target_refused absent=1
PASS wrong_problem_not_bound cmd-binding
PASS met_verdict_not_unmet met
PASS absent_without_line no SUPERSEDE
PASS fixture_kinds 4 kinds
PASS target_fields target
PASS arms_pinned 23
PASS marker_literal label
C2_COUNTER_SELFTEST pass=17 fail=0
```

## Conclusion

Measured: 20 killed, 12 survived, 0 inconclusive; 32/32 exact restorations; lane counters unchanged: True. Survivors are coverage findings, not authorization to change the frozen contract.

Extraction command: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show d5e2eda494877a85edaa4e287d6ad81843d9a8a1:<path>` for both round-88 counter paths. Every exact detector command is recorded above. Driver command: `S=/fast/scratch/hyaku/mori-r88/Mo88M01Mut; trap 'rm -rf -- "$S"' EXIT; TMPDIR="$S" python3 -I "$S/probe.py"`, cwd `/fast/scratch/hyaku/mori-r88/Mo88M01Mut`. Scratch tree deleted by EXIT trap before return. No lane-target commands run.
