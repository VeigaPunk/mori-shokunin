# Mo81E04Battery — round 81 w1

Axes: operability, calibration, coverage, depth, freshness, adjacency. Detection/report only; no scalar score change claimed.

## Deliverables

Created only these assigned files:
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/battery.sh`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/evidence/battery-entering.txt`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/w1/Mo81E04Battery.md`

The executable Bash script uses `set -u`, changes to its own lane root, discovers instruments using `grep -l -- '--selftest' tools/*.py tools/*.sh` (expanded into an array to handle absent globs), executes Python instruments with `python3 -I` and shell instruments with `bash`, then the two r80 revision counters and two r81 counter selftests in the assigned order. It prints each exact child command and full merged stdout/stderr, one instrument rc line, and the final tally; any instrument red makes the battery exit 1. Each child has `timeout --kill-after=5s 120s`; timeout would be rc 124, not green.

`--rev <sha>` changes only the r80 counters' target, defaulting to `44bc941a0e3e9676fa33a882b43d6e9793cbf74d`. `HYAKU_SCRATCH` selects the scratch parent; absent an override it uses `/fast/scratch/hyaku/mori-r81/Mo81E04Battery`. A unique child contains TMPDIR and inherited child scratch, removed by EXIT trap. No tool was edited, no package installed, and no commit/push or host remediation was performed.

## Executed command and retained evidence

Executed once with cwd `/home/vgpnk/Projects/shokunin/mori-shokunin`:

```sh
bash /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/battery.sh
```

Actual invocation was Python `subprocess.run(['bash', battery_path], cwd=lane_root, stdout=PIPE, stderr=STDOUT, text=True)`; captured text was written without alteration to the absolute evidence path above. Result: process rc 1, final line **`BATTERY 57/61`**. The receipt contains every command and all 66,767 output bytes, including all four red blocks reproduced below. This tally measures instrument return codes, not total fixture counts or independent claim admission. No timeout occurred.

Scope precision: this is the assigned default-revision battery, not a git export of every entering tool. The two r80 counters grade committed `44bc941a` bytes; discovery and all selftests run current worktree bytes. Concurrently landed `tools/mori-record-sweep.py` was discovered and returned `RECORD_SWEEP_SELFTEST pass=26 fail=0`. Thus do not describe all 61 instrument implementations as frozen entering bytes.

All red commands and their **complete output**:

```text
$ timeout --kill-after=5s 120s python3 -I tools/mori-content-review.py --selftest
{"exit_code":2,"findings":[{"code":"CONTENT_REVIEW_SELFTEST_TMPDIR"}],"schema":"mori-content-review-result-v1","status":"could-not-evaluate"}
tools/mori-content-review.py --selftest rc=2

$ timeout --kill-after=5s 120s python3 -I tools/mori-freeze-order.py --selftest
SELFTEST freeze-order FAIL 0/11
tools/mori-freeze-order.py --selftest rc=1

$ timeout --kill-after=5s 120s python3 -I tools/mori-retention-gate.py --selftest
SELFTEST retention-gate FAIL 0/21
tools/mori-retention-gate.py --selftest rc=2

$ timeout --kill-after=5s 120s python3 -I tools/mori-round19-regressions.py --selftest
R19_SELFTEST setup=explicit-lane-tmpdir-invalid
tools/mori-round19-regressions.py --selftest rc=2
```

Other required final instruments:

```text
C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19 rev=44bc941a0e3e
round-80/count-c1.py rc=0
C3=met named=56 present=56 missing=0 extra=0 rev=44bc941a0e3e
round-80/count-c3.py rc=0
C1_COUNTER_SELFTEST pass=7 fail=0
round-81/count-c1.py --selftest rc=0
C2_COUNTER_SELFTEST pass=15 fail=0
round-81/count-c2.py --selftest rc=0
BATTERY 57/61
```

Their exact producing commands are directly above these blocks in the retained raw receipt; each uses the timeout prefix shown above.

## Setup blockers, not production regression verdicts

Source inspection explains every red without re-running a reported failure:

- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-content-review.py:355-365`: `selftest_tmpdir()` requires TMPDIR to resolve beneath its own lane root, rejecting the required `/fast` scratch.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-freeze-order.py:509-514`: `_selftest()` rejects scratch outside its checkout, before any fixture runs. Its rc 1/FAIL wording does not turn this into eleven observed failing fixtures.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-retention-gate.py:459,467-468`: requires TMPDIR exactly equal to its lane's `.scratch`, explicitly forbidden by the seat write scope.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round19-regressions.py:888-891`: requires canonical TMPDIR beneath its own lane root, rejecting `/fast` scratch.

These are pre-existing tool/scratch-contract incompatibilities; no defect in another seat's new bytes was established. No tool change, lane-scratch workaround, suppressed return code, or narrowed denominator was attempted. A fully green battery under the assigned scratch policy is not established and cannot be obtained by this seat without changing those constraints. Routed to MoriR81.

QUALITY 167 warning explicitly retained: `mori-disk-rate.py` and `mori-round41-calibration.py` are known to print `pass=0 fail=0` at rc 0 with TMPDIR unset. This script exports a real TMPDIR inside its own scratch. Actual run printed `MORI_DISK_RATE_SELFTEST pass=14 fail=0` and `MORI_R41_CALIBRATION_SELFTEST pass=10 fail=0`, both rc 0: fixtures exercised, not false-green 0/0.

## Cleanup and limits

Run scratch was `/fast/scratch/hyaku/mori-r81/Mo81E04Battery/battery.9FjZeiGi`; the EXIT trap removed it. Post-run Python `not os.path.exists('/fast/scratch/hyaku/mori-r81/Mo81E04Battery/battery.9FjZeiGi')` printed `scratch_removed=True`. The parent seat directory remains an empty reusable scratch parent, not a retained fixture.

No extra gate rerun, build, lint, formatter, `--rev` override execution, alternate scratch override execution, or synthetic timeout test was performed. The script's argument branches and timeout policy are implementation, not separately exercised checks. No LSP service is mounted; this Bash-only new-file task required no supported symbol refactor. The parent owns post-integration gates.

Self-evaluation: accuracy 4 (worktree/committed-revision distinction disclosed); completeness 4 (all requested executions retained, but four setup arms unavailable); clarity 4 (raw receipt plus complete reds); actionability 4 (exact blockers and rerunnable script); conciseness 4 (full red output intentionally retained). Overall 4.0; do not infer green no-harm from this red battery.

## L1-requested classification amendment

Final classification: **`BATTERY pass=57 setup=4 fail=0`**. The four nonzero instrument return codes above are **setup-refused environment constraints (lane-scoped scratch), not fixture failures**. None of their blocked fixture arms is claimed passed. This classification supersedes the word “red” as an instrument-failure description above, without changing any raw byte or rc.

After the one execution, L1 requested a classified summary. The raw 66,767-byte run remains intact at the start of the entering receipt; a clearly marked post-run classification and four reasons/source references were appended (total receipt now 67,384 bytes). No second run was performed. The updated script now emits both the requested `BATTERY <passed>/<total>` and `BATTERY pass=<n> setup=<m> fail=<k>` lines, recognizing only exact known setup output/rc combinations; other nonzero output remains failure. It returns 1 for failures, 2 for setup-only incompleteness, and 0 only for all-pass. These final classification changes were not rerun; the historical process rc 1 belongs to the earlier script, not an execution of the amended script.

The script does not create `lane/.scratch`. Its own temporary writes are inside its unique child of the caller-selected `HYAKU_SCRATCH` parent (or the documented `/fast` default); child scratch variables point there too. Discovery and the counters read lane bytes, while child selftests may perform their designed synthetic writes within scratch. No claim is made that this wrapper independently enforces every child's write scope.

A lane-shaped directory name alone, e.g. `<scratch>/lane/.scratch`, would **not** satisfy any of the four tools as currently invoked: each derives the lane root from its own `__file__`, not the directory's name. [INFERENCE] Relocating a complete tool/fixture tree under `<scratch>/lane` and invoking those copied tools could satisfy all four path guards: content-review and freeze-order accept canonical descendants of that copied root, retention-gate needs precisely `<scratch>/lane/.scratch`, and round19-regressions needs a canonical proper descendant. Correct full execution would additionally require their referenced policies, fixtures and repository context; no relocated execution was attempted or established. Such copying/re-rooting is deliberately not implemented in this assigned battery.
