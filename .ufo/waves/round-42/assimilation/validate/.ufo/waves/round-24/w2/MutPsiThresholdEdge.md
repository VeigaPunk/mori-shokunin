# MutPsiThresholdEdge — C2 tools/mori-pressure.py threshold comparison probe

Seat: `MoriR24.MutPsiThresholdEdge` (wave 2, attempt 2). Lane tip measured:
`a730ecfefbdb5c31b1db13aca2c40eecd5e97abc` (cloned to
`/fast/scratch/hyaku/mori-r24-a2/w2/MutPsiThresholdEdge/lane`, detached HEAD at that rev).

## Mutant

Single smallest behavior-bearing edit in `tools/mori-pressure.py`, `_findings()` line 297:

- Before: `if avg10 >= warn_avg10 and (best is None or avg10 > best[1]):`
- After:  `if avg10 > warn_avg10 and (best is None or avg10 > best[1]):`

This flips the documented threshold (`avg10 >= X` per module docstring,
mori-pressure.py:26-28) to strict greater-than, so an avg10 exactly equal to
`warn_avg10` no longer triggers `PRESSURE_HIGH`.

## Detector

`python3 -I tools/mori-pressure.py --selftest` (run inside the clone; frozen
cases at `tools/fixtures/mori-pressure/cases.json`, schema `mori-pressure-cases-v1`,
12 cases P01-P12; cases run with default `--warn-avg10 10.0` — only P11/P12 pass
`--interval 1`, none override the threshold).

## Results

Pristine:
```
$ python3 -I tools/mori-pressure.py --selftest
MORI_PRESSURE_SELFTEST: PASS 12/12
$ echo $?
0
```
`sha256sum` of pristine `tools/mori-pressure.py`: `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5`

Mutated:
```
$ python3 -I tools/mori-pressure.py --selftest
MORI_PRESSURE_SELFTEST: PASS 12/12
$ echo $?
0
```
`sha256sum` of mutated `tools/mori-pressure.py`: `4a6c2dc0bade7b0061ef4f181caa4fe67da3794c8aef88160f988e2eebc146a3`
Diff confirmed the single `>=` → `>` change at line 297 (git diff, one hunk).

## Verdict: SURVIVED

The frozen cases do not kill the mutant; baseline is a clean PASS so the result
is conclusive, not inconclusive.

Reason: no frozen case exercises the exact boundary. I enumerated every snapshot
line in all 12 cases: the only avg10 values at/above the default threshold 10.0
are memory some `25.00` (P06), irq full `15.00` (P07), and cpu full `40.00`
(P02, which is excluded from thresholding — system cpu full is reported but never
used for a threshold). All are strictly greater than 10.0, so `>=` and `>` behave
identically on every case. No case has any eligible kind's avg10 exactly equal to
`warn_avg10` (10.0), so the open interval vs closed interval difference is never
observed. P01/P03/P04/P08-P12 all sit below 10.0 and are insensitive to the flip.

## Missing case (precise)

A case with a threshold-eligible kind's `avg10` exactly equal to `warn_avg10`
(default 10.0), all other values below threshold, expecting:

- `"verdict": "PRESSURE_HIGH"`, `"exit": 1`
- a finding `{"id": "PRESSURE_HIGH", "resource": <kind-eligible resource>}`
- e.g. memory some `avg10=10.00` (cpu/io/irq below), i.e. one file line
  `some avg10=10.00 avg60=... avg300=... total=...`

Under the `>` mutant that case would evaluate PRESSURE_OK (exit 0) and fail the
selftest expectation. (Not added to cases.json — explicitly out of scope.)

## Restoration evidence

Restored line 297 to `>=` via reverse edit. `sha256sum` of restored
`tools/mori-pressure.py` = `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5`
(identical to pristine); `git status --porcelain` empty and `git diff --stat`
empty in the clone; selftest re-runs `PASS 12/12` (exit 0) after restoration.
No commit/push made; fleet repo untouched (only the report file created in the
lane repo).

## Tooling

No tool installed or updated. Used system `python3` 3.14.8 (already present) and
git (already present); no pacman/uv/npx actions needed.
