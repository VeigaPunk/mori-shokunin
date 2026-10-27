# Mo57Critic27 — C1 capability-row mutation findings

Axes: calibration (C1 predicate fidelity); operability (counter detects incorrect rows).

Evidence: frozen predicate is `contract.md:5`; frozen counter is `.ufo/waves/round-57/count-c1.py:10-13`. Its row selector uses substring matches for either capability at line 11; line 12 checks only exactly two selected lines, that each line contains `.ufo/waves/round-56/`, and that each contains `| 56 |` somewhere. It does not parse columns or resolve evidence pointers.

I exercised the frozen counter logic unchanged against isolated scratch git repositories (only its hard-coded repository path was redirected to each scratch fixture):

| Case | Mutation | Result |
|---|---|---|
| baseline | `driver-liveness`, `vote-binding`, round-56-looking paths, first-working 56 | `C1=met rows=2`, exit 0 |
| name | changed names to `driver-liveness-FAKE` and `vote-binding-FAKE` | **incorrectly `C1=met rows=2`, exit 0**; substring selector still matches |
| evidence | paths changed to `.ufo/waves/round-56/evidence/DOES-NOT-EXIST/c1.txt` / `c2.txt` | **incorrectly `C1=met rows=2`, exit 0**; no path resolution |
| first-working | changed the first-working column in both rows from 56 to 57 | `C1=unmet rows=2`, exit 1 |

Counterexample to the round-field check: because `| 56 |` is searched anywhere in each full row, put `| 56 |` in the `what` cell and leave first-working as 57; the row will still pass. The counter's line 12 is not validating the designated column.

Verdict: C1 mutation resistance is incomplete. Direct name changes and invalid evidence paths are accepted; first-working changes are rejected only when the row contains no other matching `| 56 |`. This directly weakens calibration and counter operability, not the frozen contract itself.

Smallest safe correction (for the counter owner, not applied here): parse the capabilities table into named columns; require exactly one row for each exact capability name, first-working cell exactly `56`, and evidence cell resolving to the expected round-56 artifact(s) at revision `R`. Add mutation tests for each cell independently, including an unrelated `| 56 |` in another cell. Do not alter the frozen predicate.
