# ScribeScorecard — round-45 claim outcomes and round-46 measured calibration claim

Seat: scribe (leaf). Scope: review what round-45 claimed and what its measurements showed,
then adversarially check the round-46 frozen calibration predicate (`count-repins.py`) and its
do-nothing control. Evidence only; no code or files touched outside this report. No installs,
no git/jj mutations, no pacman.

---

## 1. Round-45 claim outcomes (from wave-1 seat reports and evidence)

Round-45 froze three claims (`.ufo/waves/round-45/contract.md`): C1 (hardened ledger gate),
C2 (registry predicate), C3 (assimilation). The wave-1 after-measurement state, per the seat
reports:

| claim | instrument (sha256, freeze-r45.txt pin) | measured outcome |
|---|---|---|
| C1 | `count-c1.py` `5f2deea…` | Counter delivered; selftest `C1_SELFTEST pass=16 fail=0` rc 0 (`w1/ExecLedgerCounter.md:88,227`); mutant (duplicate-id disabled) `pass=15 fail=1` rc 1. The round's real ledger was uncommitted at measurement, so `C1=unmet … failed=ledger_present` on the tip (correct by design); `C1=met` proven on an honest fixture ledger (`ExecLedgerCounter.md:132-136`). Ledger values were worktree-measured (5 mismatches at the tip), to be re-measured at the commit carrying the edits. |
| C2 | `count-c2.py` `153423c48…`; mutant `count-c2.py` `9850b3f…`; auditor `tools/mori-gate-registry.py` `8b82ac…` | Counter selftest `C2_SELFTEST pass=14 fail=0` rc 0 (`w1/ExecC2Counter.md:101`); mutant `pass=13 fail=1`. `C2=unmet` at entering tip (v1 auditor, `unregistered=14`), `C2=met` rc 0 at WORK once the v2 auditor + six registry rows landed: `tables=7 registered=39 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0 writescope_mismatch=0`; auditor `GATE_REGISTRY_SELFTEST pass=15 fail=0` (`ExecC2Counter.md:201`). |
| C3 | `count-c3.py` `37fd7c24…` | Counter selftest `C3_SELFTEST pass=19 fail=0` rc 0 (`w1/ExecC3Counter.md:164`); mutant `pass=17 fail=2`. Real lane at mid-wave: `C3=unmet` on `rows_present S473` and `readme_row` (F2/F3, both fixed downstream by the L1); end-to-end `C3=met` proven in sandbox with real census (`3fb72615…`). |

So the round-45 outcome was: all three instruments delivered and selftest/mutant-verified; C2
reached `met` on the working tree after the registry rows landed; C1/C3 needed the commit-time
re-measurement the reports explicitly handed to the L1.

### Tally/digest pins in the current SKILL.md rows trace to those measurements
- `C1_SELFTEST pass=16 fail=0` → `ExecLedgerCounter.md:88,227`.
- `C2_SELFTEST pass=14 fail=0` → `ExecC2Counter.md:101`.
- `GATE_REGISTRY_SELFTEST pass=15 fail=0` → `ExecRegistryAuditor.md:109`, `ExecC2Counter.md:201`, and re-measured here today (below).
- Digests `5f2deea…`, `153423c48…`, `9850b3f…`, `8b82ac…` → `evidence/freeze-r45.txt` manifest entries; all four recompute on the current working-tree files (below).
- `743 lines` → `wc -l tools/mori-gate-registry.py` = 743 (below); consistent with `w1/SimpInstruments.md:60`.

---

## 2. Round-46 measured calibration claim — predicate semantics

The frozen predicate (`count-repins.py`, 42 lines):

- `ROWS` = 4 named rows, each with a set of needles (tally strings, sha256 digests, `743 lines`).
- For each row: find lines starting with `"| " + row + " |"`; require exactly one; require every
  needle to be a substring of that row. Any row failing either test is an error; count errors.
- Prints `MORI_R45_REPINS mismatches=<n> rows=4`; exit 0 iff no errors.

`rows=4` is constant (`len(ROWS)`), so the falsifiable content is `mismatches=0` ⇔ all four
named rows exist exactly once and each contains all of its needles.

---

## 3. Measurements (all re-run here, 2026-10-25)

### 3.1 Current SKILL.md — green
```
$ python3 .ufo/waves/round-46/count-repins.py SKILL.md
MORI_R45_REPINS mismatches=0 rows=4
exit=0
```
Row census in current `SKILL.md`: each of the four names occurs exactly once (grep counts 1/1/1/1).

### 3.2 Do-nothing control — red (as required)
`control-skill.md` sha256 = `ed71e8f6e68c059deefb1f9bcfec42f12f2ae3bdb21aff6d5bc9bca2561cb9ad` —
byte-identical to the round-45 freeze-manifest pin of the prior committed `SKILL.md`
(`evidence/freeze-r45.txt`: `ed71e8f6…  SKILL.md`). It differs from the current `SKILL.md`
in exactly the four target rows (4 removed + 4 added lines; identical 912-line length). On it:
```
$ python3 .ufo/waves/round-46/count-repins.py .ufo/waves/round-46/control-skill.md
MORI_R45_REPINS mismatches=4 rows=4
r44 gate registry (C2): stale/missing 1 pin(s)
r45 ledger counter (C1): stale/missing 2 pin(s)
r45 gate conformance (C2): stale/missing 5 pin(s)
r44 gate registry (C2) — write scope superseded: stale/missing 3 pin(s)
exit=1
```
The control's stale pins are the pre-repair values (e.g. `pass=6`, old tallies) — i.e. the
repair is precisely the delta between control and current rows.

### 3.3 "Only when the four rows match measured pins" — mutation probes
Run on temp copies of the current `SKILL.md` (nothing in the repo touched):

| mutation | result |
|---|---|
| none (base) | `mismatches=0 rows=4`, exit 0 |
| stale C1 digest (replace `5f2deea…` with zeros) | `mismatches=1` (`r45 ledger counter (C1): stale/missing 1 pin(s)`), exit 1 |
| delete row `r45 ledger counter (C1)` | `mismatches=1` (`expected one row, found 0`), exit 1 |
| duplicate row `r45 gate conformance (C2)` | `mismatches=1` (`expected one row, found 2`), exit 1 |
| stale auditor digest (`8b82ac…` → `deadbeef…`) | `mismatches=2` (both rows carrying that needle), exit 1 |

So stale pins, missing rows and duplicate rows each force red; green is reachable only when all
four rows are unique and carry the needles.

### 3.4 Needles are the measured values (recomputed)
```
5f2deea… = sha256 .ufo/waves/round-45/count-c1.py
153423c48… = sha256 .ufo/waves/round-45/count-c2.py
9850b3f… = sha256 .ufo/waves/round-45/fixtures/mutants/count-c2.py
8b82ac… = sha256 tools/mori-gate-registry.py
743 = wc -l tools/mori-gate-registry.py
GATE_REGISTRY_SELFTEST pass=15 fail=0  (re-run: python3 tools/mori-gate-registry.py --selftest, rc 0)
```
The installed auditor's selftest was re-run here and reproduced `pass=15 fail=0` rc 0 exactly.

---

## 4. Findings

1. **The calibration claim holds as stated.** `mismatches=0 rows=4` is emitted iff the four
   specific SKILL.md rows each exist exactly once and contain their measured pins; stale,
   missing and duplicate rows all force red, and the repaired pins match the round-45 measured
   tallies/digests and the current committed instrument bytes.
2. **The do-nothing control stays red.** The control is the prior committed SKILL snapshot
   (freeze pin `ed71e8f6…`); it reports `mismatches=4 rows=4`, rc 1.
3. **Limitations (not defects) for the record:**
   - Needle matching is substring-based and cell-agnostic: a needle anywhere in the row
     satisfies the check, so a future edit that moves a tally/digest to another cell of the
     same row would still pass. The current rows place them in the intended cells.
   - Row identity is `startswith("| <name> |")`; a differently-spaced duplicate (e.g.
     `|r45 ledger counter (C1) |`) is invisible to the duplicate detection, though deleting
     the canonical row still goes red (`found 0`).
   - The predicate checks presence of the pins, not that the pins are the *only* claims in the
     cells; it does not audit other round-45 remnants elsewhere in SKILL.md (that is
     RevSkillSweep's scope).
   - `rows=4` is a constant of the script, not a measurement.

---

## 5. Evidence paths (all relative to the lane repo)
- `.ufo/waves/round-46/count-repins.py` (predicate), `w1-spec.json`, `w1-dispatch.json`.
- `.ufo/waves/round-46/control-skill.md` (control; sha256 `ed71e8f6…` = freeze pin).
- `.ufo/waves/round-45/contract.md`, `evidence/freeze-r45.txt`, `evidence/control-c1|c2|c3.txt`.
- `.ufo/waves/round-45/w1/ExecLedgerCounter.md`, `ExecC2Counter.md`, `ExecC3Counter.md`,
  `ExecRegistryAuditor.md`, `SimpInstruments.md`, `CritAxisHarm.md`, `ScribeRegistryRows.md`.

## 6. Handoff
- Main: the round-46 calibration claim is supported by reproducible measurements; control stays
  red. Re-run `python3 .ufo/waves/round-46/count-repins.py` on the committed SKILL.md and on
  the control snapshot as the integration gate.
