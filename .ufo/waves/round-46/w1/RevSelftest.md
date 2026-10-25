# RevSelftest — selftest command/output audit

Scope: verify the selftest runs and recorded output pertinent to the frozen round-46 repin predicate. Read-only review; no installs or code changes.

## Findings

No actionable discrepancy found in the recorded selftest commands and outputs within scope.

- `.ufo/waves/round-46/count-repins.py` is runnable as `python3 <script> <skill-path>`; its CLI accepts an optional positional path (default `SKILL.md`) and reads that file (`:22-26`). The exact current/control invocations and stdout/exit codes are recorded in `w1/ExecCounter.md:13-31`: repaired `SKILL.md` yields `mismatches=0 rows=4`, rc 0; `control-skill.md` yields `mismatches=4 rows=4`, rc 1.
- The three underlying selftests whose tallies are pinned by the counter are recorded in `w1/ScoutTally.md:6-48` as executable `python3 ... --selftest` commands. Their stated outputs are `GATE_REGISTRY_SELFTEST pass=15 fail=0`, `C1_SELFTEST pass=16 fail=0`, and `C2_SELFTEST pass=14 fail=0`, each with exit 0. `ScoutTally.md:51-63` maps the observed tallies back to the counter's relevant row needles.
- `w1/ExecCounter.md:33-35` records control provenance as byte equality with `git show HEAD:SKILL.md`; it also records the control's four per-row failures and exit 1. This is consistent with the control being red, not a stale selftest output being mistaken for green.

## Residual risk / verification gaps

This review checked that the command forms are runnable from the lane root and that recorded outputs are internally consistent with the counter and tally report. It did not independently execute any selftests; their execution evidence is in `ScoutTally.md` and `ExecCounter.md`. No broader claims about the counter's semantic completeness are made here.
