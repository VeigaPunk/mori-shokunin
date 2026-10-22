# Wave 2 falsify — MutPsiRegressed (C2 `counter_regressed` mutant probe)

Seat: `MoriR24.MutPsiRegressed` (leaf, no subagents). Roles: UFO-FSD mutation tester.

## Target claim
C2 after-value: `python3 -I tools/mori-pressure.py --selftest` at landed tip prints
`MORI_PRESSURE_SELFTEST: PASS 12/12`, exit 0 (contract.md:96-98; amendments A2/A3).

## Setup
- Lane tip measured: `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc` (master) — matches the
  wave-2 measured tip.
- Scratch clone: `/fast/scratch/hyaku/mori-r24-a2/w2/MutPsiRegressed`
  (`git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin <dir>`;
  checkout `a730ecf...`). Lane repo untouched: no git mutations, no jj, no pushes.
- Tooling: no installs/updates needed (system `python3`, `git`). Nothing to record
  under the operator tooling directive.
- Detector: exactly the declared after-value command, bounded to the selftest
  (`python3 -I tools/mori-pressure.py --selftest`, captures stdout + exit code).

## Mutant
Smallest behavior-bearing change implementing **counter_regressed never raised
(absolute delta)** in `tools/mori-pressure.py`, in `_combine_interval`
(the only place `STATE_REGRESSED` is assigned, lines 275-279):

- Pristine, line 272: `delta = value["total"] - prev["total"]`
- Mutated, line 272: `delta = abs(value["total"] - prev["total"])`

One expression/token-group changed. Effect: `delta` is always `>= 0`, so
`if delta < 0:` (line 275) never fires, `regressed` stays False, and cpu state
`counter_regressed` is never raised (delta fields become positive magnitudes).

## Results

| Copy | sha256 of tools/mori-pressure.py | Selftest output | Exit |
|---|---|---|---|
| Pristine | `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5` | `MORI_PRESSURE_SELFTEST: PASS 12/12` | 0 |
| Mutated | `e945ffbbd13e857ca99c69b669a7c744bca7dfef9cca1622bef3485b40c941cc` | `MORI_PRESSURE_SELFTEST: FAIL 11/12` + `P12: verdict PRESSURE_OK != PRESSURE_PARTIAL; cpu.state is 'ok', expected 'counter_regressed'` | 1 |

### Verdict: mutant KILLED (P12)
Frozen case P12 (cases.json:354-389, topic: cpu some total falls 200000 -> 100000
us between two interval reads) detects the mutant: the tool reports cpu `state: ok`
and verdict `PRESSURE_OK` instead of expected `counter_regressed` / `PRESSURE_PARTIAL`.
The selftest harness compares `rc`, `verdict`, and per-resource fields
(mori-pressure.py:457-486), so the state flip fails the case. No survivor; no
missing case to name — P12 already covers the decreasing-total branch for cpu.

## Restoration evidence
Line 272 restored to `delta = value["total"] - prev["total"]`. After restore:
- `sha256sum tools/mori-pressure.py` → `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5` (matches pristine, before-mutant hash).
- `git status --porcelain tools/mori-pressure.py` → empty (clean vs `a730ecf...`).

## Notes
- Mutant ran only in the scratch clone; lane bytes untouched. No cases.json edit.
- P12's assertion is the only case exercising `counter_regressed`; with the abs-delta
  mutant it is a hard kill (both state and verdict diverge), so the frozen suite is
  sensitive to this defect class.
