# MutPsiCpuFullThreshold — mutation test report (round 24, wave 2)

Seat: `MoriR24.MutPsiCpuFullThreshold`
Target: C2 `tools/mori-pressure.py` selftest sensitivity
Clone: `/fast/scratch/hyaku/mori-r24-a2/w2/MutPsiCpuFullThreshold/clone` (git clone --no-hardlinks of the lane repo), checkout `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc` (measured lane tip). Lane repo untouched; no git mutations in the lane (scratch clone only). No host writes.

## Mutant

Claimed invariant: system `cpu` `full` is reported but never used for a threshold (contract.md:66-67; `tools/mori-pressure.py:83-85` `FULL_UNDEFINED`, `tools/mori-pressure.py:193-194` note). The smallest behavior-bearing code mutant implementing "system cpu full included in the threshold" is a one-line change to the threshold table:

```
-    "cpu": ("some",),
+    "cpu": ("some", "full"),
```

(`tools/mori-pressure.py:78`, inside `THRESHOLD_KINDS`). No other line changed; `FULL_UNDEFINED` label and `_resource_payload` untouched so the mutant is exactly the threshold-inclusion behavior.

## Detector

`python3 -I tools/mori-pressure.py --selftest` (run from repo root). Tool `python3 --version` = 3.14.8 (pre-existing; no tool installed or updated this session — tooling directive recorded, nothing to add).

## Results

| Run | SHA256 of tools/mori-pressure.py | Output | Exit |
|---|---|---|---|
| Pristine (before mutant) | `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5` | `MORI_PRESSURE_SELFTEST: PASS 12/12` | 0 |
| Mutated | `b9f523ee3579832fba8e23f723fac7ebc271e4ac0df2404970369eb1821df9c0` | `MORI_PRESSURE_SELFTEST: FAIL 11/12`<br>`P02: exit 1 != 0; verdict PRESSURE_HIGH != PRESSURE_OK` | 1 |
| Restored | `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5` (identical to pristine) | `MORI_PRESSURE_SELFTEST: PASS 12/12` | 0 |

Restoration evidence: post-restore `sha256sum` byte-identical to pristine; `git diff --stat` in the clone is empty (no working-tree changes); restored run passes 12/12.

## Verdict: KILLED

The frozen case **P02** kills the mutant. `tools/fixtures/mori-pressure/cases.json:48-77`:
- P02 topic: "system cpu full carries a nonzero value; it is reported but labelled full_system_undefined and is never used for a threshold, so the verdict stays PRESSURE_OK".
- Snapshot: cpu `full avg10=40.00` (well above `--warn-avg10` default 10.0).
- Expect: `exit 0`, `verdict PRESSURE_OK`, cpu full_system_undefined true, `findings_include: []`.

With the mutant, `_findings` (`tools/mori-pressure.py:283-309`) iterates `THRESHOLD_KINDS["cpu"]` = `("some","full")`, sees cpu full avg10 40.0 ≥ 10.0 and emits `PRESSURE_HIGH` on cpu/full; verdict flips to `PRESSURE_HIGH`, exit 1. Selftest reports exactly this: `P02: exit 1 != 0; verdict PRESSURE_HIGH != PRESSURE_OK`.

No missing case: the frozen suite already pins the excluded-from-threshold property at the exact spot the mutant touches (cpu full above threshold must stay OK). No change to `cases.json` (per bounds). No other case regressed (11/12 still pass).

## Evidence

- Mutant line: `tools/mori-pressure.py:78` (before/after shown above; file hash evidence above).
- P02 frozen case: `tools/fixtures/mori-pressure/cases.json:48-77` (topic line 49, cpu full line 54, expect lines 62-77).
- Threshold table and undefined comment: `tools/mori-pressure.py:77-85`; `_findings` threshold scan `tools/mori-pressure.py:283-309`; selftest runner `tools/mori-pressure.py:496-541`.
- Commands: `sha256sum tools/mori-pressure.py`; `python3 -I tools/mori-pressure.py --selftest`; `echo "EXIT=$?"`; post-restore `git diff --stat`.
