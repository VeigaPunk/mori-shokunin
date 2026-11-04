# Mo82E01C1Regress — regression sensitivity

Axes: operability, freshness, depth, coverage, calibration, adjacency. Detection/report only; no scalar changes.

## Produced paths (absolute)

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/simulate-regression.sh`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/evidence/regression-sim-r82.txt`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/w1/Mo82E01C1Regress.md`

The simulator is durable source ready for the L1's commit; this leaf did not commit anything. It archives the three real counters and their support files from a named revision, deletes exactly one fixture per scenario, and creates disposable revision objects only in its scratch repository. Source Git objects are shared read-only through an alternate; new blob/tree/commit objects are written with the standard Git object encoding directly in scratch, so no source index, refs, hooks or Git mutation command is needed to produce the simulated revisions. The harness is invoked with `--repo` pointing exclusively at that scratch repository. Each scenario starts from the same base, not from the previous deletion.

`HYAKU_SCRATCH` selects the scratch root. An explicit `TMPDIR` is honored beneath that root's `mori-r82/Mo82E01C1Regress` directory; an outside directory is rejected rather than writing outside this seat's permission. Without `TMPDIR`, a temporary subdirectory is allocated inside the trapped simulation directory. No hardcoded temporary system path. The simulation tree is removed by EXIT trap; the enclosing seat scratch directory from this execution was also removed in the driver's `finally` block.

## Requested execution and retained evidence

Exact command, all 33 mutant readings, summaries, command return codes, and full simulated revision identifiers are retained verbatim in `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/evidence/regression-sim-r82.txt`.

```text
$ env HYAKU_SCRATCH=/fast/scratch/hyaku TMPDIR=/fast/scratch/hyaku/mori-r82/Mo82E01C1Regress/tmp bash /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/simulate-regression.sh 20551e56 /home/vgpnk/Projects/shokunin/mori-shokunin
BASE_REVISION=20551e564da8bbb941c6a2ace7405192ceb74969
HARNESS_SHA256=ba0646a3d308c70a35c6499b18631373475a483cabfe4e46cfcdfe94125b6ac3
REGRESSION_PASS ignore_sweep_exit
REGRESSION_PASS drop_right_boundary
REGRESSION_PASS pending_substring
REGRESSION_SIM pass=3 fail=0
rc=0
```

The block above selects the run's identifying and final output lines; the receipt is unabridged. Each harness invocation returned **1**, correctly rejecting the regression, and printed `C1=unmet harness=present killed=10 survivors=1 total=11 pristine=green` followed by its revision label:

| deleted fixture | expected and observed survivor | disposable revision |
|---|---|---|
| `zero_summary_nonzero_exit` in r80 C1 selftest tuple | `ignore_sweep_exit`, rc 0 | `0d9060ec79dea55b8457a104c04fc2545ece2aaa` |
| `suffix_trap` fixture block in r80 C3 | `drop_right_boundary`, rc 0 | `f72380d641343bc3b1892e10c5e5391d9318096e` |
| `pending substring is not a cell` check in r81 C2 | `pending_substring`, rc 0 | `403de966a25ce0c3b93a9895a2c48de3f59e0056` |

The task's `sweep_zero_summary_nonzero_exit` spelling differs from the actual fixture label, `zero_summary_nonzero_exit` (`.ufo/waves/round-80/count-c1.py:127`). The simulator recognizes either spelling and **deletes the tuple entry**, not its expectation or the production guard.

## Per-mutant kill attribution

“r81-added” below specifically means the five survivor-closing arms added by commit `482dc48d49670de0f7645d0d8e87e18816145256`. “Older” means present before that closure; some older arms themselves were added earlier in r81. It does not mean all those arms predate round 81.

| counter | mutant | killing fixture | attribution |
|---|---|---|---|
| r80 C1 | `ignore_row_disagreement` | `second_stale_row` | Older, before five-arm closure |
| r80 C1 | `ignore_mismatch_lines` | `mismatch_line` | Older, before five-arm closure |
| r80 C1 | `ignore_stale_field` | `inconsistent_summary` | Older, before five-arm closure |
| r80 C1 | `ignore_sweep_exit` | `zero_summary_nonzero_exit` | r81-added survivor arm; deletion sensitively demonstrated here |
| r80 C3 | `ignore_missing` | `missing_one` | Older, before five-arm closure |
| r80 C3 | `ignore_extra` | `extra_stale` | Older, before five-arm closure |
| r80 C3 | `drop_right_boundary` | `suffix_trap` | r81-added survivor arm; deletion sensitively demonstrated here |
| r81 C2 | `pending_all_sections` | `pending outside a round section ignored` | Older, before five-arm closure |
| r81 C2 | `pending_substring` | `pending substring is not a cell` | r81-added survivor arm; deletion sensitively demonstrated here |
| r81 C2 | `ignore_command_exit` | `failing command unmet` | r81-added survivor arm |
| r81 C2 | `first_binding_only` | `second binding counted` | r81-added survivor arm |

Attribution evidence: `.ufo/waves/round-81/w1/Mo81M01Mutants.md` independently records the pre-closure seven kills and five survivors; the commit diff below shows the exact five new arm additions. The present simulation reports all other mutants killed in each scenario. The two nonselected C2 arms were **not individually deleted** by this seat; their fixture attribution is source/history evidence, not an extra unperformed deletion experiment.

Research command (rc 0):

```text
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show --format=fuller 482dc48d -- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c3.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/count-c2.py
```

Relevant exact added output lines:

```diff
+            ("zero_summary_nonzero_exit", "exitone", 19, 19, False),
+    cases.append(("suffix_trap", r["met"] is False,
+    check("pending substring is not a cell", not pending_cells(
+    check("failing command unmet", verdict is not None and verdict["pinned"] == 2, str(verdict))
+    check("second binding counted", verdict is not None and verdict["pinned"] == 2, str(verdict))
```

The initial history command used `git log --oneline --follow --format='%h %s'` for r80 C1, then `git log --oneline --format='%h %s'` for r80 C3 and r81 C2, followed by `git rev-parse HEAD` and a first-five-line status listing. Its rc was 0. Output identified `482dc48d` as the five-survivor-arm commit, `1106afd3` as the earlier r81 implementation/arm commit, and `6b021d29` as the r81 C2 freeze. The observed HEAD was `08e13729b60382e121956c461f4ad0fd9194553a`; this is **not** the simulation's measured base, which was explicitly pinned to `20551e56` above.

## Verification, risks, and blockers

- Verified by the requested execution: three independent deletions each expose exactly one intended survivor; every pristine copy remains green in each run. No deleted arm produced `survivors=0`; no detector defect was observed in these three scenarios.
- No other seat's production bytes were edited. No install, credential read, external remediation, commit, push, dispatch or new worker was performed.
- LSP definition/reference/refactor tools are not exposed in this seat's tool inventory; source/AST and committed diff inspection were used instead. This is actual tooling unavailability, not an empty symbol search.
- Existing counter selftests create synthetic repositories under their explicit scratch directory. This execution is the assignment's explicitly requested falsifier run, not a general integration gate. No unrelated test, build, formatter or lint run was performed.
- The retained receipt identifies the invoked working harness by SHA-256 and its revision input by full SHA. It does not claim a final landed-r82 gate result. Re-run the same simulator against the L1's landed revision to bind that result to the final harness bytes.
- The deleted-fixture scratch commits intentionally disappear at cleanup. Their identifiers are reproducibly generated from the pinned base and deletions; durable replay uses the committed simulator, not a removed scratch pathname.
- The script uses SHA-1 Git object encoding and Python's `tarfile` data-filter support, matching this successfully exercised repository/runtime; SHA-256 object-format repositories were not tested.
- Remaining blocker: only the L1 can satisfy the request's **committed** qualification by committing these three assigned files. The implementation and requested receipt are complete; no uncommitted content is mislabeled as landed evidence here.

## Self-evaluation

| axis | score | evidence / improvement |
|---|---:|---|
| Accuracy | 4 | Full receipt binds base and harness digest; final landed harness is outside this run's evidence. |
| Completeness | 4 | All three requested regression classes executed; commit ownership remains L1-only. |
| Clarity | 4 | Explicit older-versus-five-arm distinction prevents historical misattribution; receipt avoids duplicating all output here. |
| Actionability | 4 | One replay command and exact paths; L1 must land and run at its final revision. |
| Conciseness | 4 | Attribution table is compact; scratch object production needs a short explanation because Git mutation commands are forbidden. |

Overall 4.0. Highest-impact improvements: bind the simulator receipt to the final landed revision at L1 integration; retain the harness digest with that run. Would the user agree? Likely for the scoped sensitivity proof; this report explicitly does not assert the parent-owned commit or final gate has occurred.
