# C8 replay and scratch-isolation receipt

Axes: honest conformance, bypass discrimination, concurrent scratch isolation.

## Honest sequential replays

Ran `python3 .ufo/waves/round-39/conform.py 13bfba23b7ca063c76d3504a2ff6eb7b6a294932` twice sequentially.

- Run 1: exit **0**, `CONFORM=met`; all nine checks PASS (`scratch/ExecC8Replay/honest-1.txt:2-11`). Captured command output: `HONEST_1_EXIT=0`.
- Run 2: exit **0**, `CONFORM=met`; all nine checks PASS (`scratch/ExecC8Replay/honest-2.txt:2-11`). Captured command output: `HONEST_2_EXIT=0`.

## Rebuilt M19 bypass fixtures

Ran `make-m19-bypass.py` for `13f3db7e5c7163e7ef300259ff597a42a79f81f1`, writing only under `scratch/ExecC8Replay/fixtures/`. Builder exit **0** (`FIXTURE_BUILD_EXIT=0`); it reported `derived 2 drain(s) into bypass-none.py; bypass-wait.py from the primary communicate drain` (`scratch/ExecC8Replay/fixture-build.txt:1`; source selects the requested revision at `fixtures/make-m19-bypass.py:23-33`).

- `bypass-none.py`: checker exit **1**, `CONFORM=unmet`. Failures: `predicate`, `timeout_value`, `timeout_state`, `scratch`; load-bearing `timeout_value` FAIL reports both `communicate` values as non-numeric constants (`scratch/ExecC8Replay/bypass-none.txt:2,6,8-11`). Captured command output: `BYPASS_NONE_EXIT=1`.
- `bypass-wait.py`: checker exit **1**, `CONFORM=unmet`. Failures: `predicate`, `drain_shape`, `timeout_state`, `scratch`, `selftest_conjunct`; load-bearing `drain_shape` FAIL says the `Popen` was not drained by a used `communicate` in its function (`scratch/ExecC8Replay/bypass-wait.txt:2,7-11`). Captured command output: `BYPASS_WAIT_EXIT=1`.

## Concurrent replay and scratch dirs

Launched two `python3 conform.py <rev>` processes concurrently (each wrapped by `strace -f -e trace=mkdir,mkdirat` to record directory creation). Both exited **0** and printed `CONFORM=met`; each passed all nine checks (`scratch/ExecC8Replay/concurrent-1.txt:2-11`, `scratch/ExecC8Replay/concurrent-2.txt:2-11`; captured command output: `CONCURRENT_1_EXIT=0`, `CONCURRENT_2_EXIT=0`).

Scratch directories created by those two conformance processes: **none**. The traces contain only process-exit/SIGCHLD events and no `mkdir`/`mkdirat` calls (`scratch/ExecC8Replay/concurrent-1.trace:1-18`, `scratch/ExecC8Replay/concurrent-2.trace:1-18`); thus there is no shared or seed-derived scratch path from these invocations. The before/after snapshots show an unrelated `RevC7Kill` directory appeared under the scratch root during this window (`scratch/ExecC8Replay/concurrent-dirs-before.txt:2124-2126`, `scratch/ExecC8Replay/concurrent-dirs-after.txt:2124-2126`); it is not attributable to these traced processes.

## Risk / blocker

The honest sequential runs reported `head_at_measurement=20260b0c804fa2882d0ed3b916a11d2ab6cc1406`, while the concurrent runs reported `296b2c569360c48d421cd70790edc4c6a52e2670` (`scratch/ExecC8Replay/honest-1.txt:3`, `scratch/ExecC8Replay/honest-2.txt:3`, `scratch/ExecC8Replay/concurrent-1.txt:3`, `scratch/ExecC8Replay/concurrent-2.txt:3`). The checkout tip changed during this replay window; actor and cause are unknown. All four honest results still report `CONFORM=met` against the requested revision.