# Mo81E01SweepFix — r81 w1 scoped counter repairs

## Scope and behavior

Axes: operability (primary), calibration, coverage, depth, freshness, adjacency. No score changes claimed.

Changed implementation: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c1.py`.
Produced report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/w1/Mo81E01SweepFix.md`.
No other implementation files edited; count-c3.py and both frozen contracts untouched by this seat.

- MEDIUM-7: collect every CLAIM_SWEEP summary; require one distinct summary, every summary parseable, all four graded fields zero, no CLAIM_SWEEP_MISMATCH line, and exit zero. Report each graded field's maximum across parsed summaries, preserving receipt token grammar. Identical repeated summaries are allowed; different summaries are not.
- MEDIUM-8: inspect every matching capability-table row and every `selftest N in-memory` reading; return the common scalar only when all agree. Missing phrases or conflicting counts yield None and an unmet verdict against the live count. Removed the old blanket exclusion of rows containing the word Capability.
- LOW-10: argv-only git archive followed by argv-only tar with archive bytes on stdin; archive failure is checked independently. No shell interpolation.
- Preserve four existing selftest cases; add contradicting summaries, independent mismatch-line/zero-summary, second stale row, and repo path containing spaces. Fixture repos assert their toplevel before add/commit. CLI/output labels unchanged; predicate restatement at lines 4–12 unchanged.

### Edit hunk ranges

Ranges below identify original→resulting source regions from edit-tool evidence, not a subsequently run git diff:

| Original lines | Resulting lines | Change |
|---|---|---|
| 14–19 | 14–19 | Document all-row/all-summary coverage and retained limit |
| 45–47 | 45–50 | argv archive/tar export |
| 51–60 | 54–67 | all-row tally consensus, including missing-phrase mismatch |
| 83–87 | 90–104 | parse all summaries, detect mismatch lines and conflicts |
| 93–94 | 110–112 | include consistency in verdict |
| 108–110; insertion after 116 | 126–144 | four added fixtures, spaced repo path, synthetic output bodies |
| 126–128 | 154–158 | generate one or multiple capability rows |
| insertion after 130 | 161–162 | assert fixture repository toplevel before add/commit |

Selftest tally before: **4 declared arms**, from the original source and inherited r80 reviewer receipt (not independently executed before editing). After: **8 passed, 0 failed**, executed below. Four additional arms rather than three independently cover both MEDIUM-7 shapes.

## Exact exercised verification

The L1 explicitly directed these checks in-wave. Executed using a synchronous Python subprocess driver invoking bash, with cwd `/home/vgpnk/Projects/shokunin/mori-shokunin`. Each Python command below was wrapped with `timeout 120s`; none timed out. Environment: `TMPDIR=/fast/scratch/hyaku/mori-r81/Mo81E01SweepFix`. The driver created that scratch directory and installed `trap 'rm -rf -- "$S"' EXIT`; bash exited normally with driver_rc=0 and empty stderr. Scratch cleanup was executed by that trap; no separate post-cleanup filesystem probe was run.

```text
$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c1.py --selftest
PASS conformant C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19
PASS stale_row C1=unmet tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=18 live_tally=19
PASS sweep_mismatch C1=unmet tool=present sweep=1 mismatches=1 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19
PASS inconsistent_summary C1=unmet tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=1 row_tally=19 live_tally=19
PASS contradicting_summaries C1=unmet tool=present sweep=0 mismatches=1 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19
PASS mismatch_line C1=unmet tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19
PASS second_stale_row C1=unmet tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=None live_tally=19
PASS repo_path_with_space C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19
C1_COUNTER_SELFTEST pass=8 fail=0
rc=0
$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c1.py 44bc941a0e3e9676fa33a882b43d6e9793cbf74d --scratch /fast/scratch/hyaku/mori-r81/Mo81E01SweepFix
C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19 rev=44bc941a0e3e
rc=0
$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/count-c1.py 44bc941a0e3e9676fa33a882b43d6e9793cbf74d --scratch /fast/scratch/hyaku/mori-r81/Mo81E01SweepFix
A2_summary_contradicts_mismatch_line expected=unmet got=met rc=0
A3_two_contradicting_summaries expected=unmet got=met rc=0
A4_second_carrier_row_stale expected=unmet got=met rc=0
A5_repo_path_with_space expected=met got=setup rc=2
B1_subdir_path_counts_as_naming expected=unmet got=met rc=0
B2_own_lane_prefix_excluded expected=met got=unmet rc=1
B6_directory_named_as_tool expected=met got=unmet rc=1
C1=unmet wrong=7 fixtures=7 real_c1=met real_c3=met rev=44bc941a0e3e
rc=1
```

The third command intentionally grades committed entering bytes, not this seat's worktree edits. Its wrong=7 reproduces the do-nothing control; it is not a failure of the newly executed eight-arm r80 selftest and does not establish a landed after-reading.

## Limits, risks, blockers

- Verified: eight r80 selftest arms green, including all four inherited cases; modified r80 counter still grades real entering lane C1 met with row/live 19; r81 entering control stays wrong=7 with both real arms met.
- Not verified: r81 gate at a revision containing these repairs and sibling C3 repairs. L1 must run that after committing/integrating; this seat neither commits nor substitutes worktree bytes for revision bytes. No build, formatter, lint, full battery, or additional checks run.
- The counter trusts the sweep's findings, not an independent reimplementation of every sweep pin. That pre-existing named limit remains.
- Archive bytes are buffered in memory as required by the assigned two-subprocess export interface.
- No supported LSP tool is exposed in this seat's tool inventory; source locations were resolved using read/grep instead. No empty LSP response was treated as absence.
- No new defect in another seat's implementation bytes established; sibling implementations were outside this seat's review scope. The r81 third-command output is expected for its explicitly requested entering revision, not a file:line defect.
- No tool installed or updated; no credentials or external state read or changed. No remaining scoped implementation blocker.

## Self-evaluation

Accuracy 4/5: exact observed outputs retained; no landed after-reading yet. Completeness 4/5: all three fixes and requested checks complete, while committed integration remains L1-owned. Clarity 4/5: original/resulting range table is edit evidence rather than a generated diff. Actionability 4/5: L1 still needs the committed r81 gate. Conciseness 4/5: full fixture output retained to satisfy evidence requirements. Overall 4.0/5. Highest-value next action is the L1's post-integration revision gate; this report does not predeclare it green.
