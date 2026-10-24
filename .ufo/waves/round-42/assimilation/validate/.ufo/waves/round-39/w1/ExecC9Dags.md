# C9 DAG fixture comparison

## Method

Extracted the gate bytes with `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 13f3db7e5c7163e7ef300259ff597a42a79f81f1:tools/mori-sources-appendonly.py` and `git ... show 13bfba23b7ca063c76d3504a2ff6eb7b6a294932:tools/mori-sources-appendonly.py` to `.ufo/waves/round-39/scratch/ExecC9Dags/gate-r38.py` and `gate-v2.py`. Ran the requested `run-c9-dags.py` command once per file, writing results to `scratch/ExecC9Dags/r38.txt` and `v2.txt`. The runner writes each fixture's stdout and exit code (runner lines 44–52); its `supersede_timing` output is the timing verdict, not wall-clock duration.

## Results

| Gate / fixture | `supersede_timing` | `round_changed` | Exit | Receipt comparison |
|---|---|---|---:|---|
| r38 / A (side-branch superseder) | `superseded_as_of=[] stale_supersede=[S001]` | `[S001]` | 1 | Matches `c9-red-a.txt` lines 6–8; run `r38.txt` lines 6–8. |
| r38 / C (merge does not fabricate edit) | `superseded_as_of=[S001] stale_supersede=[]` | `[S001]` | 1 | Matches `c9-red-a.txt` lines 13–15; run `r38.txt` lines 13–15. |
| r38 / D (landing is last edit commit) | `superseded_as_of=[] stale_supersede=[S001]` | `[S001]` | 1 | Matches `c9-red-a.txt` lines 20–22; run `r38.txt` lines 20–22. |
| v2 / A (side-branch superseder) | `superseded_as_of=[] stale_supersede=[S001]` | `[S001]` | 1 | Matches `c9-after-fixture-a.txt` lines 4–6; run `v2.txt` lines 6–8. |
| v2 / C (merge does not fabricate edit) | `superseded_as_of=[S001] stale_supersede=[]` | `[]` | 0 | Matches `c9-after-fixture-c.txt` lines 4–6; run `v2.txt` lines 13–15. |
| v2 / D (landing is last edit commit) | `superseded_as_of=[S001] stale_supersede=[]` | `[S001]` | 1 | Matches `c9-after-fixture-d.txt` lines 4–6; run `v2.txt` lines 20–22. |

**Acceptance: PASS.** Every fixture's timing verdict, `round_changed`, and exit line agrees with its committed receipt. No contradictions found. Exact run outputs: `.ufo/waves/round-39/scratch/ExecC9Dags/r38.txt` and `v2.txt` (each fixture block includes its header and all three reported lines).