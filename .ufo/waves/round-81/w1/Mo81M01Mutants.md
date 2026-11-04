# Mo81M01Mutants — independent bounded mutation probe
Axes: operability, calibration, coverage, depth, freshness, adjacency. Detection/report only. No source fixes, commits, installs, services, credentials, fleet-root writes, or subagent dispatch. Only this report survives.
## Population and limits
`tools/mori-record-sweep.py` was absent on the first population read, so the specified fallback `.ufo/waves/round-81/count-c2.py` is used. The C1 snapshot includes the in-wave eight-arm fix; C3 is the observed four-arm worktree version. These are per-file tip-worktree snapshots, not a claim about the final committed round. Sibling edits after capture are outside this probe. Every mutant is a single anchored replacement in a new scratch copy at the same relative path. No lane executable was modified.
Pristine copies are green first: C1 rc=0 pass=8 fail=0; C3 rc=0 pass=4 fail=0; fallback C2 rc=0 pass=15 fail=0. An initial C2 copy accidentally retained the read tool’s 300-line pagination footer and failed with SyntaxError before executing any test. It was replaced with the complete 322-line source before all mutation runs; that acquisition error is not a killed mutant or a source defect.
## Detector and controls
Each run executes the file’s own `--selftest --scratch` through an otherwise transparent `runpy` launcher. The launcher intercepts subprocess git calls only to assert that init/add/commit targets are beneath the assigned scratch and, before add/commit, that `git rev-parse --show-toplevel` equals the fixture target. The existing selftests initialize/commit synthetic repos only there; no lane git mutation was invoked. The selftest grading code is unchanged. Detector: killed iff rc != 0 or stdout contains fail>0, conditional on green pristine and restored runs. Each subprocess had a 120-second bound. Environment overrides: `TMPDIR=/fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`; cwd=/fast/scratch/hyaku/mori-r81/Mo81M01Mutants.
## Mutant table
| file | label | old → new (literal anchored substring) | selftest rc | verdict |
|---|---|---|---|---|
| `.ufo/waves/round-80/count-c1.py` | ignore_row_disagreement | `if readings and len(set(readings)) == 1:` → `if readings:` | 1 | killed |
| `.ufo/waves/round-80/count-c1.py` | ignore_mismatch_lines | `and not any(line.startswith("CLAIM_SWEEP_MISMATCH")` → `and not any(False and line.startswith("CLAIM_SWEEP_MISMATCH")` | 1 | killed |
| `.ufo/waves/round-80/count-c1.py` | ignore_stale_field | `and tallies == 0 and stale == 0 and stated == live)` → `and tallies == 0 and stated == live)` | 1 | killed |
| `.ufo/waves/round-80/count-c1.py` | ignore_sweep_exit | `met = (p.returncode == 0 and sweep_consistent` → `met = (sweep_consistent` | 0 | survived |
| `.ufo/waves/round-80/count-c3.py` | ignore_missing | `met = not missing and not extra` → `met = not extra` | 1 | killed |
| `.ufo/waves/round-80/count-c3.py` | ignore_extra | `met = not missing and not extra` → `met = not missing` | 1 | killed |
| `.ufo/waves/round-80/count-c3.py` | accept_sibling | `if SIBLING.search(before):` → `if False and SIBLING.search(before):` | 1 | killed |
| `.ufo/waves/round-80/count-c3.py` | drop_right_boundary | `(?![\w.-])` → `` | 0 | survived |
| `.ufo/waves/round-81/count-c2.py` | pending_all_sections | `section is None or not ROUND_SECTION.match(section) or not ROW.match(line)` → `section is None or not ROW.match(line)` | 1 | killed |
| `.ufo/waves/round-81/count-c2.py` | pending_substring | `if cell == "PENDING":` → `if "PENDING" in cell:` | 0 | survived |
| `.ufo/waves/round-81/count-c2.py` | ignore_command_exit | `or result.returncode != 0 or stated != live:` → `or stated != live:` | 0 | survived |
| `.ufo/waves/round-81/count-c2.py` | first_binding_only | `for binding in bindings:` → `for binding in bindings[:1]:` | 0 | survived |

## Coverage findings: exact missing arms

These are selftest coverage findings, not assertions that pristine production grading is wrong. The proposed arms below were not added or executed. Locations refer to the captured bytes.

- `.ufo/waves/round-80/count-c1.py:110` (ignore_sweep_exit): sweep_nonzero_clean_summary: all-zero summary with exit 1 must be unmet. Its current own selftest remains green after this graded behaviour is inverted.
- `.ufo/waves/round-80/count-c3.py:31` (drop_right_boundary): suffix_boundary: PROVINCE only `tools/mori-census.sh.bak` with present={mori-census.sh} must be unmet. Its current own selftest remains green after this graded behaviour is inverted.
- `.ufo/waves/round-81/count-c2.py:73` (pending_substring): pending_exact_only: cell NOT_PENDING or `PENDING` must count zero. Its current own selftest remains green after this graded behaviour is inverted.
- `.ufo/waves/round-81/count-c2.py:133` (ignore_command_exit): pinned_nonzero_equal: binding states pointers=233, command prints pointers=233 and exits 1: pinned=1. Its current own selftest remains green after this graded behaviour is inverted.
- `.ufo/waves/round-81/count-c2.py:125` (first_binding_only): second_binding_stale: first binding agrees, second differs: pinned=1. Its current own selftest remains green after this graded behaviour is inverted.

The command-exit survivor is masked by the existing sweep_mismatch arm also carrying mismatches=1. The pinned-command survivor is masked by the stale fixture already disagreeing numerically. The first-binding survivor has no multi-binding fixture. None permits changing the frozen contract.

## Exact commands and actual output

Workspace creation: `mkdir -p /fast/scratch/hyaku/mori-r81/Mo81M01Mutants` produced no output, rc=0. Source and mutant copies were created with file tools, not shell edits.

### Pristine .ufo/waves/round-80/count-c1.py

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/pristine/.ufo/waves/round-80/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
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
```

### Pristine .ufo/waves/round-80/count-c3.py

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/pristine/.ufo/waves/round-80/count-c3.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
PASS complete named=3 present=3 missing=0 extra=0
PASS missing_one named=2 present=3 missing=1 extra=0
PASS extra_stale named=4 present=3 missing=0 extra=1
PASS sibling_and_directory_ignored named=3 present=3 extra=[]
C3_COUNTER_SELFTEST pass=4 fail=0
rc=0
```

### Pristine .ufo/waves/round-81/count-c2.py

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/pristine/.ufo/waves/round-81/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
case pending in round table pass 
case pending outside a round section ignored pass 
case pending prose ignored pass 
case stated first row pass 
case live single pass 
case live conflicting pass 
case pins schema pass 
case export roundtrip pass 
case clean record met pass {'pending': 0, 'pinned': 0, 'tool': 'present', 'agree': 1, 'met': True}
case pending record unmet pass C2=unmet pending=1 pinned=0 tool=present agree=0
case stale pinned unmet pass C2=unmet pending=0 pinned=1 tool=present agree=0
case tool absent unmet pass C2=unmet pending=0 pinned=0 tool=absent agree=0
case tool disagree unmet pass C2=unmet pending=0 pinned=0 tool=present agree=0
case space path export pass 
case space path met pass None
C2_COUNTER_SELFTEST pass=15 fail=0
rc=0
```

### ignore_row_disagreement

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_row_disagreement/.ufo/waves/round-80/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
PASS conformant C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19
PASS stale_row C1=unmet tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=18 live_tally=19
PASS sweep_mismatch C1=unmet tool=present sweep=1 mismatches=1 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19
PASS inconsistent_summary C1=unmet tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=1 row_tally=19 live_tally=19
PASS contradicting_summaries C1=unmet tool=present sweep=0 mismatches=1 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19
PASS mismatch_line C1=unmet tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19
FAIL second_stale_row C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19
PASS repo_path_with_space C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19
C1_COUNTER_SELFTEST pass=7 fail=1
rc=1
```

After exact-byte restoration, same command and detector:

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_row_disagreement/.ufo/waves/round-80/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
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
```

### ignore_mismatch_lines

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_mismatch_lines/.ufo/waves/round-80/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
PASS conformant C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19
PASS stale_row C1=unmet tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=18 live_tally=19
PASS sweep_mismatch C1=unmet tool=present sweep=1 mismatches=1 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19
PASS inconsistent_summary C1=unmet tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=1 row_tally=19 live_tally=19
PASS contradicting_summaries C1=unmet tool=present sweep=0 mismatches=1 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19
FAIL mismatch_line C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19
PASS second_stale_row C1=unmet tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=None live_tally=19
PASS repo_path_with_space C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19
C1_COUNTER_SELFTEST pass=7 fail=1
rc=1
```

After exact-byte restoration, same command and detector:

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_mismatch_lines/.ufo/waves/round-80/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
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
```

### ignore_stale_field

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_stale_field/.ufo/waves/round-80/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
PASS conformant C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19
PASS stale_row C1=unmet tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=18 live_tally=19
PASS sweep_mismatch C1=unmet tool=present sweep=1 mismatches=1 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19
FAIL inconsistent_summary C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=1 row_tally=19 live_tally=19
PASS contradicting_summaries C1=unmet tool=present sweep=0 mismatches=1 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19
PASS mismatch_line C1=unmet tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19
PASS second_stale_row C1=unmet tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=None live_tally=19
PASS repo_path_with_space C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19
C1_COUNTER_SELFTEST pass=7 fail=1
rc=1
```

After exact-byte restoration, same command and detector:

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_stale_field/.ufo/waves/round-80/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
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
```

### ignore_sweep_exit

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_sweep_exit/.ufo/waves/round-80/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
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
```

After exact-byte restoration, same command and detector:

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_sweep_exit/.ufo/waves/round-80/count-c1.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
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
```

### ignore_missing

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_missing/.ufo/waves/round-80/count-c3.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
PASS complete named=3 present=3 missing=0 extra=0
FAIL missing_one named=2 present=3 missing=1 extra=0
PASS extra_stale named=4 present=3 missing=0 extra=1
PASS sibling_and_directory_ignored named=3 present=3 extra=[]
C3_COUNTER_SELFTEST pass=3 fail=1
rc=1
```

After exact-byte restoration, same command and detector:

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_missing/.ufo/waves/round-80/count-c3.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
PASS complete named=3 present=3 missing=0 extra=0
PASS missing_one named=2 present=3 missing=1 extra=0
PASS extra_stale named=4 present=3 missing=0 extra=1
PASS sibling_and_directory_ignored named=3 present=3 extra=[]
C3_COUNTER_SELFTEST pass=4 fail=0
rc=0
```

### ignore_extra

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_extra/.ufo/waves/round-80/count-c3.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
PASS complete named=3 present=3 missing=0 extra=0
PASS missing_one named=2 present=3 missing=1 extra=0
FAIL extra_stale named=4 present=3 missing=0 extra=1
PASS sibling_and_directory_ignored named=3 present=3 extra=[]
C3_COUNTER_SELFTEST pass=3 fail=1
rc=1
```

After exact-byte restoration, same command and detector:

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_extra/.ufo/waves/round-80/count-c3.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
PASS complete named=3 present=3 missing=0 extra=0
PASS missing_one named=2 present=3 missing=1 extra=0
PASS extra_stale named=4 present=3 missing=0 extra=1
PASS sibling_and_directory_ignored named=3 present=3 extra=[]
C3_COUNTER_SELFTEST pass=4 fail=0
rc=0
```

### accept_sibling

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/accept_sibling/.ufo/waves/round-80/count-c3.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
PASS complete named=3 present=3 missing=0 extra=0
PASS missing_one named=2 present=3 missing=1 extra=0
PASS extra_stale named=4 present=3 missing=0 extra=1
FAIL sibling_and_directory_ignored named=4 present=3 extra=['tsukuroi-census.sh']
C3_COUNTER_SELFTEST pass=3 fail=1
rc=1
```

After exact-byte restoration, same command and detector:

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/accept_sibling/.ufo/waves/round-80/count-c3.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
PASS complete named=3 present=3 missing=0 extra=0
PASS missing_one named=2 present=3 missing=1 extra=0
PASS extra_stale named=4 present=3 missing=0 extra=1
PASS sibling_and_directory_ignored named=3 present=3 extra=[]
C3_COUNTER_SELFTEST pass=4 fail=0
rc=0
```

### drop_right_boundary

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/drop_right_boundary/.ufo/waves/round-80/count-c3.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
PASS complete named=3 present=3 missing=0 extra=0
PASS missing_one named=2 present=3 missing=1 extra=0
PASS extra_stale named=4 present=3 missing=0 extra=1
PASS sibling_and_directory_ignored named=3 present=3 extra=[]
C3_COUNTER_SELFTEST pass=4 fail=0
rc=0
```

After exact-byte restoration, same command and detector:

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/drop_right_boundary/.ufo/waves/round-80/count-c3.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
PASS complete named=3 present=3 missing=0 extra=0
PASS missing_one named=2 present=3 missing=1 extra=0
PASS extra_stale named=4 present=3 missing=0 extra=1
PASS sibling_and_directory_ignored named=3 present=3 extra=[]
C3_COUNTER_SELFTEST pass=4 fail=0
rc=0
```

### pending_all_sections

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/pending_all_sections/.ufo/waves/round-81/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
case pending in round table pass 
case pending outside a round section ignored FAIL 
case pending prose ignored pass 
case stated first row pass 
case live single pass 
case live conflicting pass 
case pins schema pass 
case export roundtrip pass 
case clean record met pass {'pending': 0, 'pinned': 0, 'tool': 'present', 'agree': 1, 'met': True}
case pending record unmet pass C2=unmet pending=1 pinned=0 tool=present agree=0
case stale pinned unmet pass C2=unmet pending=0 pinned=1 tool=present agree=0
case tool absent unmet pass C2=unmet pending=0 pinned=0 tool=absent agree=0
case tool disagree unmet pass C2=unmet pending=0 pinned=0 tool=present agree=0
case space path export pass 
case space path met pass None
C2_COUNTER_SELFTEST pass=14 fail=1
rc=1
```

After exact-byte restoration, same command and detector:

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/pending_all_sections/.ufo/waves/round-81/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
case pending in round table pass 
case pending outside a round section ignored pass 
case pending prose ignored pass 
case stated first row pass 
case live single pass 
case live conflicting pass 
case pins schema pass 
case export roundtrip pass 
case clean record met pass {'pending': 0, 'pinned': 0, 'tool': 'present', 'agree': 1, 'met': True}
case pending record unmet pass C2=unmet pending=1 pinned=0 tool=present agree=0
case stale pinned unmet pass C2=unmet pending=0 pinned=1 tool=present agree=0
case tool absent unmet pass C2=unmet pending=0 pinned=0 tool=absent agree=0
case tool disagree unmet pass C2=unmet pending=0 pinned=0 tool=present agree=0
case space path export pass 
case space path met pass None
C2_COUNTER_SELFTEST pass=15 fail=0
rc=0
```

### pending_substring

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/pending_substring/.ufo/waves/round-81/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
case pending in round table pass 
case pending outside a round section ignored pass 
case pending prose ignored pass 
case stated first row pass 
case live single pass 
case live conflicting pass 
case pins schema pass 
case export roundtrip pass 
case clean record met pass {'pending': 0, 'pinned': 0, 'tool': 'present', 'agree': 1, 'met': True}
case pending record unmet pass C2=unmet pending=1 pinned=0 tool=present agree=0
case stale pinned unmet pass C2=unmet pending=0 pinned=1 tool=present agree=0
case tool absent unmet pass C2=unmet pending=0 pinned=0 tool=absent agree=0
case tool disagree unmet pass C2=unmet pending=0 pinned=0 tool=present agree=0
case space path export pass 
case space path met pass None
C2_COUNTER_SELFTEST pass=15 fail=0
rc=0
```

After exact-byte restoration, same command and detector:

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/pending_substring/.ufo/waves/round-81/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
case pending in round table pass 
case pending outside a round section ignored pass 
case pending prose ignored pass 
case stated first row pass 
case live single pass 
case live conflicting pass 
case pins schema pass 
case export roundtrip pass 
case clean record met pass {'pending': 0, 'pinned': 0, 'tool': 'present', 'agree': 1, 'met': True}
case pending record unmet pass C2=unmet pending=1 pinned=0 tool=present agree=0
case stale pinned unmet pass C2=unmet pending=0 pinned=1 tool=present agree=0
case tool absent unmet pass C2=unmet pending=0 pinned=0 tool=absent agree=0
case tool disagree unmet pass C2=unmet pending=0 pinned=0 tool=present agree=0
case space path export pass 
case space path met pass None
C2_COUNTER_SELFTEST pass=15 fail=0
rc=0
```

### ignore_command_exit

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_command_exit/.ufo/waves/round-81/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
case pending in round table pass 
case pending outside a round section ignored pass 
case pending prose ignored pass 
case stated first row pass 
case live single pass 
case live conflicting pass 
case pins schema pass 
case export roundtrip pass 
case clean record met pass {'pending': 0, 'pinned': 0, 'tool': 'present', 'agree': 1, 'met': True}
case pending record unmet pass C2=unmet pending=1 pinned=0 tool=present agree=0
case stale pinned unmet pass C2=unmet pending=0 pinned=1 tool=present agree=0
case tool absent unmet pass C2=unmet pending=0 pinned=0 tool=absent agree=0
case tool disagree unmet pass C2=unmet pending=0 pinned=0 tool=present agree=0
case space path export pass 
case space path met pass None
C2_COUNTER_SELFTEST pass=15 fail=0
rc=0
```

After exact-byte restoration, same command and detector:

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_command_exit/.ufo/waves/round-81/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
case pending in round table pass 
case pending outside a round section ignored pass 
case pending prose ignored pass 
case stated first row pass 
case live single pass 
case live conflicting pass 
case pins schema pass 
case export roundtrip pass 
case clean record met pass {'pending': 0, 'pinned': 0, 'tool': 'present', 'agree': 1, 'met': True}
case pending record unmet pass C2=unmet pending=1 pinned=0 tool=present agree=0
case stale pinned unmet pass C2=unmet pending=0 pinned=1 tool=present agree=0
case tool absent unmet pass C2=unmet pending=0 pinned=0 tool=absent agree=0
case tool disagree unmet pass C2=unmet pending=0 pinned=0 tool=present agree=0
case space path export pass 
case space path met pass None
C2_COUNTER_SELFTEST pass=15 fail=0
rc=0
```

### first_binding_only

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/first_binding_only/.ufo/waves/round-81/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
case pending in round table pass 
case pending outside a round section ignored pass 
case pending prose ignored pass 
case stated first row pass 
case live single pass 
case live conflicting pass 
case pins schema pass 
case export roundtrip pass 
case clean record met pass {'pending': 0, 'pinned': 0, 'tool': 'present', 'agree': 1, 'met': True}
case pending record unmet pass C2=unmet pending=1 pinned=0 tool=present agree=0
case stale pinned unmet pass C2=unmet pending=0 pinned=1 tool=present agree=0
case tool absent unmet pass C2=unmet pending=0 pinned=0 tool=absent agree=0
case tool disagree unmet pass C2=unmet pending=0 pinned=0 tool=present agree=0
case space path export pass 
case space path met pass None
C2_COUNTER_SELFTEST pass=15 fail=0
rc=0
```

After exact-byte restoration, same command and detector:

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/guarded-selftest.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/first_binding_only/.ufo/waves/round-81/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/runs
case pending in round table pass 
case pending outside a round section ignored pass 
case pending prose ignored pass 
case stated first row pass 
case live single pass 
case live conflicting pass 
case pins schema pass 
case export roundtrip pass 
case clean record met pass {'pending': 0, 'pinned': 0, 'tool': 'present', 'agree': 1, 'met': True}
case pending record unmet pass C2=unmet pending=1 pinned=0 tool=present agree=0
case stale pinned unmet pass C2=unmet pending=0 pinned=1 tool=present agree=0
case tool absent unmet pass C2=unmet pending=0 pinned=0 tool=absent agree=0
case tool disagree unmet pass C2=unmet pending=0 pinned=0 tool=present agree=0
case space path export pass 
case space path met pass None
C2_COUNTER_SELFTEST pass=15 fail=0
rc=0
```

## SHA-256 restoration evidence

| file | pristine before = restored after |
|---|---|
| `.ufo/waves/round-80/count-c1.py` | `d438530460091a8f73b8ae28007436e96dd7e51daf6830d9c636dcdcf6f58b41` |
| `.ufo/waves/round-80/count-c3.py` | `6b96d8e8d6e53c4361cf83ebff691fb0a47c72d43267deb4e4ea8fd66441e3ba` |
| `.ufo/waves/round-81/count-c2.py` | `ad60408fcd1ef4c939f07379e175f304a2744e34f634e11a2f3ecc55f3336c8a` |

| mutant | mutated hash (between before/after) |
|---|---|
| ignore_row_disagreement | `49aa034b52ae427bae8e4899f6adc1397de2bb563ddac63d3c99bc7dda8561c8` |
| ignore_mismatch_lines | `28cfe523e1f3d4dad1088517f218820e8c6aefaec672203cde65a92f93d83d92` |
| ignore_stale_field | `c8b0db73f8a314aadb65cb576a6104c1cb4fd3cb5889523fb68bdab86cb1a3b0` |
| ignore_sweep_exit | `a774b24bb7e696eacad38a765bc77ff802dd5f3ae2e87572fd195b01f96332a3` |
| ignore_missing | `dd2ebf12bf52e3abd44943dd38fe66f11e90b73926750373bd185b844a96581c` |
| ignore_extra | `78785d3e9acfd6f3a7c4357d10719b64832c2b761b37de856e18921d956528be` |
| accept_sibling | `cacfdb6c508791ae7d544615b83a8686f17a04864d8d8bbe81b97c14c8179257` |
| drop_right_boundary | `a908081339deefdd10996b51ab95346c11a2208ee2ba28f86becff6adc2706b4` |
| pending_all_sections | `4c127f2eb24ad92755477ec21f4f2373ed28941c5882f12a907e22db45ec913c` |
| pending_substring | `cc8aa36e17df69d985b962817d3ef50cb27887f4aaafd471688d5e7fc2a1fbc8` |
| ignore_command_exit | `b8fee692fcda2cb58fb12dc5cf14bb0096c62412481d47c20f1d186c8fe44b50` |
| first_binding_only | `b5fe729d9cc8b3594315893c9eaee62a6d46fdfe168fbcd574d008e274752078` |

Actual final hash command and output (every mutant restored to its file’s pristine hash):

```text
$ sha256sum /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/pristine/.ufo/waves/round-80/count-c1.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/pristine/.ufo/waves/round-80/count-c3.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/pristine/.ufo/waves/round-81/count-c2.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_row_disagreement/.ufo/waves/round-80/count-c1.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_mismatch_lines/.ufo/waves/round-80/count-c1.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_stale_field/.ufo/waves/round-80/count-c1.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_sweep_exit/.ufo/waves/round-80/count-c1.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_missing/.ufo/waves/round-80/count-c3.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_extra/.ufo/waves/round-80/count-c3.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/accept_sibling/.ufo/waves/round-80/count-c3.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/drop_right_boundary/.ufo/waves/round-80/count-c3.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/pending_all_sections/.ufo/waves/round-81/count-c2.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/pending_substring/.ufo/waves/round-81/count-c2.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_command_exit/.ufo/waves/round-81/count-c2.py /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/first_binding_only/.ufo/waves/round-81/count-c2.py
d438530460091a8f73b8ae28007436e96dd7e51daf6830d9c636dcdcf6f58b41  /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/pristine/.ufo/waves/round-80/count-c1.py
6b96d8e8d6e53c4361cf83ebff691fb0a47c72d43267deb4e4ea8fd66441e3ba  /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/pristine/.ufo/waves/round-80/count-c3.py
ad60408fcd1ef4c939f07379e175f304a2744e34f634e11a2f3ecc55f3336c8a  /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/pristine/.ufo/waves/round-81/count-c2.py
d438530460091a8f73b8ae28007436e96dd7e51daf6830d9c636dcdcf6f58b41  /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_row_disagreement/.ufo/waves/round-80/count-c1.py
d438530460091a8f73b8ae28007436e96dd7e51daf6830d9c636dcdcf6f58b41  /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_mismatch_lines/.ufo/waves/round-80/count-c1.py
d438530460091a8f73b8ae28007436e96dd7e51daf6830d9c636dcdcf6f58b41  /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_stale_field/.ufo/waves/round-80/count-c1.py
d438530460091a8f73b8ae28007436e96dd7e51daf6830d9c636dcdcf6f58b41  /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_sweep_exit/.ufo/waves/round-80/count-c1.py
6b96d8e8d6e53c4361cf83ebff691fb0a47c72d43267deb4e4ea8fd66441e3ba  /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_missing/.ufo/waves/round-80/count-c3.py
6b96d8e8d6e53c4361cf83ebff691fb0a47c72d43267deb4e4ea8fd66441e3ba  /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_extra/.ufo/waves/round-80/count-c3.py
6b96d8e8d6e53c4361cf83ebff691fb0a47c72d43267deb4e4ea8fd66441e3ba  /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/accept_sibling/.ufo/waves/round-80/count-c3.py
6b96d8e8d6e53c4361cf83ebff691fb0a47c72d43267deb4e4ea8fd66441e3ba  /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/drop_right_boundary/.ufo/waves/round-80/count-c3.py
ad60408fcd1ef4c939f07379e175f304a2744e34f634e11a2f3ecc55f3336c8a  /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/pending_all_sections/.ufo/waves/round-81/count-c2.py
ad60408fcd1ef4c939f07379e175f304a2744e34f634e11a2f3ecc55f3336c8a  /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/pending_substring/.ufo/waves/round-81/count-c2.py
ad60408fcd1ef4c939f07379e175f304a2744e34f634e11a2f3ecc55f3336c8a  /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/ignore_command_exit/.ufo/waves/round-81/count-c2.py
ad60408fcd1ef4c939f07379e175f304a2744e34f634e11a2f3ecc55f3336c8a  /fast/scratch/hyaku/mori-r81/Mo81M01Mutants/first_binding_only/.ufo/waves/round-81/count-c2.py
rc=0
```

Cleanup command:

```sh
S=/fast/scratch/hyaku/mori-r81/Mo81M01Mutants; trap 'rm -rf -- "$S"' EXIT; rm -rf -- "$S"; test ! -e "$S" && printf 'SCRATCH_REMOVED path=%s rc=0\n' "$S"
```

Actual output: `SCRATCH_REMOVED path=/fast/scratch/hyaku/mori-r81/Mo81M01Mutants rc=0`. All scratch deleted before report delivery.

## Verified / not verified

Verified: 3 pristine-green own selftests; 12 independent single-replacement mutant selftests; all 12 exact-restored selftests green; 15 final hashes match captured pristine bytes; scratch removal. Not verified: new record tool (absent at first read), later sibling bytes, final revision C1/C2 keeper results, standing battery, production correctness beyond this bounded detector. No defect in another seat’s bytes is claimed beyond the five located selftest coverage gaps.

Self-evaluation: accuracy 4 (bounded to snapshots, not final tip); completeness 4 (allowed fallback, no new-tool grading); clarity 4 (full outputs are long); actionability 4 (specific proposed arms, deliberately unimplemented); conciseness 4 (restored logs retained for evidence). Overall 4.0. Highest-impact action is adding the five named discriminating arms; final-tip reruns belong to L1.

MUTANTS killed=7 total=12 survivors=5
