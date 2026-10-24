# MutPsiRatio — round-24 wave-2 mutation probe (C2 attacker)

**Seat:** MoriR24.MutPsiRatio
**Claim under test:** C2 (`tools/mori-pressure.py` selftest sensitivity; declared
after-value `MORI_PRESSURE_SELFTEST: PASS 12/12` over frozen
`tools/fixtures/mori-pressure/cases.json`).
**Lane range:** clone of `/home/vgpnk/Projects/shokunin/mori-shokunin` at
`/fast/scratch/hyaku/mori-r24-a2/w2/MutPsiRatio/mori-shokunin`, checkout
`a730ecfefbdb5c31b1db13aca2c40eecd5e97abc` (`round-24: wave-1 seat reports,
S090 wording correction, contract amendment A5`).
**Mutant:** `stall_ratio` divided by CPU count instead of the requested interval
(one of the two assigned flavors; the elapsed-time flavor would require
multi-line signature changes and crashes under the selftest no-op sleep, so the
CPU-count flavor is the single smallest faithful mutant).

## Mutant applied (single-line, `tools/mori-pressure.py:274`)

```diff
-        value["stall_ratio"] = round(delta / (interval_s * 1e6), 6)
+        value["stall_ratio"] = round(delta / (os.cpu_count() * 1e6), 6)
```

`os` is already imported (`tools/mori-pressure.py:57`), so this is exactly one
changed line, verified by `git diff` (single hunk, `-271,7 +271,7`).

## Expected detector

`python3 -I tools/mori-pressure.py --selftest` must print
`MORI_PRESSURE_SELFTEST: PASS 12/12` and exit 0 on the pristine byte (the C2
declared after-value).

## Runs

### Baseline (pristine bytes, before mutation)
Command: `python3 -I tools/mori-pressure.py --selftest`
Output:
```
MORI_PRESSURE_SELFTEST: PASS 12/12
```
Exit: `0`.
Pristine `sha256sum tools/mori-pressure.py` = `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5`.

### Mutated copy
Command: `python3 -I tools/mori-pressure.py --selftest`
Output:
```
MORI_PRESSURE_SELFTEST: FAIL 11/12
P11: cpu.some.stall_ratio is 0.003906, expected 0.125; memory.some.stall_ratio is 0.003125, expected 0.1; io.some.stall_ratio is 0.00125, expected 0.04; irq.full.stall_ratio is 0.000188, expected 0.006
```
Exit: `1`.

## Verdict: KILLED

The frozen case **P11** (`cases.json:305-352`, `args: ["--interval", "1"]`)
asserts the four `stall_ratio` values on the denominator `interval_s * 1e6`:

| resource.kind | delta (us) | expected | mutant (÷ 32 CPUs × 1e6) | result |
|---|---|---|---|---|
| cpu.some | 125000 | 0.125 | 0.003906 | mismatch |
| memory.some | 100000 | 0.1 | 0.003125 | mismatch |
| io.some | 40000 | 0.04 | 0.00125 | mismatch |
| irq.full | 6000 | 0.006 | 0.000188 | mismatch |

Host `os.cpu_count()` = 32 (observed), so every ratio is divided by 32× the
nominal denominator; all four assertions fire and the selftest fails
`11/12` with exit 1. P12 does not assert ratios (only states), so P11 is the
sole detecting case. No case covers this defect: P11 is the only case that pins
`stall_ratio` to the requested interval, but it cannot distinguish "divided by
interval" from "divided by any fixed factor that happens to equal
`interval_s * 1e6`" — the asserted values are baked-in constants, not computed
from the reported `interval_s` (P11 is the only case with `--interval`; P12
only checks states). A surviving-mutant scenario would be a divisor that equals
1e6 on this host (e.g. `os.cpu_count()` on a 1-CPU machine); the missing case
that would kill the mutant robustly is one asserting `stall_ratio` against a
denominator derived from the reported `interval_s` (e.g. an interval other than
1 s, like `--interval 0.5` or `--interval 2`, and/or a case where the ratio is
recomputed from `payload["interval_s"]` rather than a hard-coded expectation).

## Restoration evidence

- Restore: `git checkout a730ecfefbdb5c31b1db13aca2c40eecd5e97abc -- tools/mori-pressure.py` in the scratch clone.
- After restore: `sha256sum tools/mori-pressure.py` = `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5` — identical to pristine baseline hash.
- `git diff --stat` after restore: empty (working tree clean).
- Post-restore selftest: `MORI_PRESSURE_SELFTEST: PASS 12/12`, exit 0.

No lane files touched outside the permitted report; no git mutation in
`/home/vgpnk/Projects/shokunin/mori-shokunin`; no tools installed (Python 3.14.8
system binary used throughout; no installs needed).
