# MutPsiFieldSwap — C2 selftest sensitivity probe (wave 2, round 24)

Seat: `MoriR24.MutPsiFieldSwap` (leaf mutation tester, no subagents).
Probe target: claim C2 (`tools/mori-pressure.py` selftest) at lane tip
`a730ecfefbdb5c31b1db13aca2c40eecd5e97abc` (branch master, the measured wave-2 tip).

## Mutant applied (single smallest behavior-bearing point)

File `tools/mori-pressure.py`, `_parse_resource`, the grammar-field mapping block
(lines 180–185 at the tip). Swapped the parser's field assignments for `avg10` and
`avg300` (both parse from the same line grammar; only the dict mapping changes):

```diff
         kinds[kind] = {
-            "avg10": float(match.group(2)),
+            "avg10": float(match.group(4)),
             "avg60": float(match.group(3)),
-            "avg300": float(match.group(4)),
+            "avg300": float(match.group(2)),
             "total": int(match.group(5)),
         }
```

One behavior-bearing point (the parser field mapping); all other code untouched.
Applied only in the scratch clone
`/fast/scratch/hyaku/mori-r24-a2/w2/MutPsiFieldSwap/repo` (git clone of the lane
repo, checkout of the tip above). No other file touched; `cases.json` never edited.

## Detector (same bounded detector, pristine vs mutated vs restored)

`python3 -I tools/mori-pressure.py --selftest` run from the clone root, with
`/usr/bin/python3` (Python 3.14.8), git 2.56.0. No tool installs were needed
(git, python3, sha256sum already present; nothing recorded per operator RULES).

### Pristine bytes (before mutation)

```
MORI_PRESSURE_SELFTEST: PASS 12/12
```
Exit 0. `sha256sum tools/mori-pressure.py` = `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5`.

### Mutated bytes

`sha256sum tools/mori-pressure.py` = `4e4913d623a66106a50b7b11f27c9a4eed6d78573e8d0ea4442567bf53eb0d11`.

```
MORI_PRESSURE_SELFTEST: FAIL 7/12
P01: cpu.some.avg10 is 0.12, expected 1.23; cpu.some.avg300 is 1.23, expected 0.12; memory.some.avg10 is 0.78, expected 2.34; memory.some.avg300 is 2.34, expected 0.78; memory.full.avg10 is 0.22, expected 1.11; memory.full.avg300 is 1.11, expected 0.22; io.some.avg10 is 1.09, expected 3.21; io.some.avg300 is 3.21, expected 1.09; io.full.avg10 is 0.54, expected 0.98; io.full.avg300 is 0.98, expected 0.54; irq.full.avg10 is 0.27, expected 0.31; irq.full.avg300 is 0.31, expected 0.27
P02: cpu.some.avg10 is 0.41, expected 0.53; cpu.some.avg300 is 0.53, expected 0.41; cpu.full.avg10 is 3.0, expected 40.0; cpu.full.avg300 is 40.0, expected 3.0
P03: irq.full.avg10 is 0.01, expected 0.05; irq.full.avg300 is 0.05, expected 0.01
P06: exit 0 != 1; verdict PRESSURE_OK != PRESSURE_HIGH; memory.some.avg10 is 3.25, expected 25.0; memory.some.avg300 is 25.0, expected 3.25; memory.full.avg10 is 0.22, expected 1.11; memory.full.avg300 is 1.11, expected 0.22; finding PRESSURE_HIGH on memory missing
P07: exit 0 != 1; verdict PRESSURE_OK != PRESSURE_HIGH; irq.full.avg10 is 1.0, expected 15.0; irq.full.avg300 is 15.0, expected 1.0; finding PRESSURE_HIGH on irq missing
```
Exit 1. Full output preserved at `…/MutPsiFieldSwap/mutated.out`.

Note on the tally semantics: `_selftest` prints `FAIL %d/%d` with **passed**/total
(`tools/mori-pressure.py:536`), so `FAIL 7/12` means 7 passed, 5 failed. The 5
failing cases are P01, P02, P03, P06, P07; the other 7 (P04, P05, P08, P09, P10,
P11, P12) pass under the mutant.

## Verdict: KILLED

The frozen cases kill the avg10↔avg300 swap mutant — the selftest flips from
`PASS 12/12` (exit 0) to `FAIL 7/12` (exit 1), 5 of 12 cases red.

Killing cases:
- **P01** — the primary killer, by construction: its topic states "every avg10,
  avg60, avg300 and total is pairwise distinct so a field swap cannot survive", and
  the fixture (cases.json:11-27) sets per-kind distinct values (e.g. cpu some
  avg10=1.23 vs avg300=0.12). The swapped parser emits avg10=0.12/avg300=1.23,
  which the `expect` block rejects on all four resources (cpu/memory/io some+full,
  irq full — 12 field mismatches in P01 alone).
- **P06** (memory some avg10=25.00): swap moves the value to avg300, so no
  threshold finding — exit flips 1→0, verdict HIGH→OK, `PRESSURE_HIGH on memory`
  finding missing.
- **P07** (irq full avg10=15.00): same mechanism, HIGH on irq lost.
- **P02** / **P03**: exact-value field expectations (cpu some/full, irq full) fail.

No additional case is needed; the missing-case discussion is moot because P01 is
explicitly swap-proof and kills the mutant.

## Restoration evidence (exact bytes)

Git checkout of the scratch clone restored the file:
- `sha256sum tools/mori-pressure.py` = `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5` — identical to the pristine before-mutation hash.
- `git status --short` clean (no stray files in the clone).
- Detector on restored bytes: `MORI_PRESSURE_SELFTEST: PASS 12/12`, exit 0.

Lane repo untouched: no writes to `/home/vgpnk/Projects/shokunin/mori-shokunin`
other than this report file; no git/jj mutation anywhere; no host writes, no PSI
triggers, no service changes.

## Environment / tooling record

- pytest: none needed. Used only available tools: git 2.56.0, /usr/bin/python3
  (3.14.8), sha256sum. Per operator RULES, nothing was installed; nothing to record.
- Scratch: `/fast/scratch/hyaku/mori-r24-a2/w2/MutPsiFieldSwap/repo`
  (clone), `pristine.out`, `mutated.out`.
