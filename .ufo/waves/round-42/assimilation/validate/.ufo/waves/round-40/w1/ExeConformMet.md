# ExeConformMet

## Commands and outputs

1. Ran exactly:

```sh
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b
```

Exit status: `0` (Bash tool result). Exact stdout:

```text
P-C10: at revision R, the round-40 conformance checker passes all nine checks on the round-40 counter bytes — the round-39 nine with three made sound — `timeout_scope` (every `timeout=` keyword in every counter resolves in the scope of its read site: a binding inside the enclosing function shadows the module map, a `global` rebinding is read at module scope, a module-level binding nested in `if`/`try`/`for`/`while` makes the name conditionally rebound and fails closed, and the value must be a finite positive number, so `1e400` fails and a fold raising `ZeroDivisionError` or `RecursionError` fails as a violation, not a setup error), `drain_bind` (every `Popen(` in every counter is drained in its own function by a `communicate(` bound to the same name, carrying its own timeout, with the result consumed — assigned to other than `_`, or returned — so a `wait(timeout=…)` plus `stdout.read()` drain fails even beside a decoy used communicate, an undrained second `Popen(` fails, and a tuple-wrapped or `_`-assigned communicate does not qualify), and `selftest_conjunct` (per counter: the counter's communicates all carry timeouts, stripping each communicate timeout one at a time is detected by that same rule, and the checker's own textual-mutation table carries a live `selftest_conjunct` entry whose anchor occurs in the counter — comm_violations are computed and reported per counter, not for the first counter only) — and the checker's `--selftest` applies eleven textual mutations to the counter of record, each flipping exactly its own check to FAIL.
check predicate          PASS (exit=0 equal=True)
check head_pin           PASS (pin=ede486b7a09afbacfb380d5871c46a8051a6dc2e tip=ede486b7a09afbacfb380d5871c46a8051a6dc2e)
check tool_resolve       PASS (exit=0 resolved=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/fixtures/witness-summary-only-live.txt)
check bounded_reads      PASS (count-c8.py: bounded=[] value=[])
check timeout_scope      PASS (count-c8.py: bounded=[] value=[])
check drain_bind         PASS (count-c8.py: violations=[])
check timeout_state      PASS (exit=1 timeout_reason=True pass=False)
check scratch            PASS (count-c8.py: mkdtemp_dir=True root=True)
check selftest_conjunct  PASS (count-c8.py: honest_comm=[] strips=6 detected=6 anchor=True entry_live=True)
CONFORM=met
```

2. Ran this byte comparison command:

```sh
set -o pipefail; python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b | tee /dev/stderr | cmp - /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/evidence/c10-after.txt; rc=$?; printf 'BYTE_DIFF_EXIT=%s\n' "$rc"; exit "$rc"
```

The checker stdout from this pipeline was the same as the output above. Comparison output:

```text
- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/evidence/c10-after.txt differ: char 1, line 1
BYTE_DIFF_EXIT=1
```

## Drift

The receipt is a wrapped transcript: it starts with `command: ...` and ends with `EXIT=0`, neither of which is checker stdout, so raw stdout versus the entire receipt differs at byte 1. Comparing the recorded checker-output lines shows a substantive `head_pin` drift too: `c10-after.txt` records `pin=265a955cc67be4eae97d2dc5a9338a25f31eb29b tip=265a955cc67be4eae97d2dc5a9338a25f31eb29b`; the replay printed `pin=ede486b7a09afbacfb380d5871c46a8051a6dc2e tip=ede486b7a09afbacfb380d5871c46a8051a6dc2e`. The other eight check lines and `CONFORM=met` match the receipt. The replay itself exited 0 and all nine checks passed; the receipt is not byte-identical to this replay.

Files changed: this report only. No production files changed. Risk: the present replay's head-pin differs from the committed after-receipt's scored-tip pin. Blockers: none.
