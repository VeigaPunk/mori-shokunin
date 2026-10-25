# CritControl — round 46 calibration repair falsification

Seat: `L1Mori46.CritControl` — assignment: *try to make the do-nothing control incorrectly pass; identify control/measurement asymmetry*.

## 1. Control identity (verified)

The do-nothing control is byte-identical to the prior committed SKILL snapshot:

- `jj file show -r baabc9929f0f SKILL.md` → sha256 `ed71e8f6e68c059deefb1f9bcfec42f12f2ae3bdb21aff6d5bc9bca2561cb9ad`
- `.ufo/waves/round-46/control-skill.md` → sha256 `ed71e8f6e68c059deefb1f9bcfec42f12f2ae3bdb21aff6d5bc9bca2561cb9ad`
- `diff` between the two: 0 lines.

Control is red as claimed:

```
$ python3 .ufo/waves/round-46/count-repins.py .ufo/waves/round-46/control-skill.md
MORI_R45_REPINS mismatches=4 rows=4
r44 gate registry (C2): stale/missing 1 pin(s)
r45 ledger counter (C1): stale/missing 2 pin(s)
r45 gate conformance (C2): stale/missing 5 pin(s)
r44 gate registry (C2) — write scope superseded: stale/missing 3 pin(s)
exit=1
```

Current repaired `SKILL.md` scores `mismatches=0 rows=4`, exit 0. The four hardcoded needle hashes verify against the live instrument files (sha256sum): `8b82ac99…` = `tools/mori-gate-registry.py` (743 lines), `5f2deea0…` = `.ufo/waves/round-45/count-c1.py`, `153423c48…` = `.ufo/waves/round-45/count-c2.py`, `9850b3fc…` = fixture mutant `count-c2.py`.

## 2. Falsification: control made to pass without re-pinning (reproduced)

The predicate matches each needle as a **substring anywhere in the whole row line** (`needle not in matches[0]`), and it never verifies which table or which cell the row lives in. It therefore cannot distinguish a repaired row from a row that merely *mentions* the measured pins anywhere.

Reproducible demonstration: take the control, append nothing but prose to the four target rows (no cell value changed; the stale selftest text `pass=6 fail=0` etc. is untouched), then run the frozen counter:

```bash
# /tmp/control_attack1.md = control-skill.md with only these four appended line tails:
#   | r44 gate registry (C2) |                    + " appended-prose: GATE_REGISTRY_SELFTEST pass=15 fail=0"
#   | r45 ledger counter (C1) |                   + " appended-prose: C1_SELFTEST pass=16 fail=0 5f2deea0b35c5e1346229d265aa0c07bf7f365bf6c5acda87648045bce658d23"
#   | r45 gate conformance (C2) |                + " appended-prose: C2_SELFTEST pass=14 fail=0 153423c48… 9850b3fc… 8b82ac99… 743 lines"
#   | r44 gate registry (C2) — write scope superseded | + " appended-prose: GATE_REGISTRY_SELFTEST pass=15 fail=0 8b82ac99… 743 lines"
python3 .ufo/waves/round-46/count-repins.py /tmp/control_attack1.md
# => MORI_R45_REPINS mismatches=0 rows=4 ; exit=0
```

Evidence the pin cells were not repaired: the `atk` line prefixes are identical to the control's (`ctl`) for lines 184/190/191/194; the stale `pass=6 fail=0` selftest fragment remains in the row; the needles only appear in the appended trailing prose. The do-nothing control flips green via text mention alone.

Corollary (measurement asymmetry): the counter performs **zero runtime measurement**. `subprocess` is imported but never used; the script only reads the file text and pattern-matches hardcoded constants. The "measured pins" are frozen literals from the repair moment. If the instruments drift later (selftest counts change, line counts change, hashes change), the snapshot text keeps passing — the freeze validates presence of text, not correspondence to any live measurement.

## 3. Additional asymmetry observations

- **Line-prefix identity**: rows are found by `line.startswith("| " + row + " |")` only. The predicate cannot tell which section/table the row belongs to, so the needles satisfy the check from any table (registry, changelog, appendix) as long as the prefix matches and there is exactly one such line.
- **One pin string satisfies several rows**: `8b82ac99…`/`743 lines` are required in rows 184, 191 and 194; `GATE_REGISTRY_SELFTEST pass=15 fail=0` in rows 184 and 194. Nothing anchors a needle to its own row's pin cell.
- **“Four rows” over-counts distinct registries**: `ROWS` has 4 entries, but two of them describe the same logical r44 gate registry (row 184 and its “write scope superseded” superseding row, line 194). The distinct registry rows are three (r44 gate registry, r45 ledger counter, r45 gate conformance); the fourth check is a duplicate registry entry with an extra needle set.
- **Per-row mismatch granularity**: mismatches are counted per row, not per pin (each of the four control rows reports one mismatch regardless of how many needles it misses: 1/2/5/3). The outcome is binary per row, hiding pin-level distance-to-correctness.

## 4. Smallest safe correction

1. Parse the matched row into cells and require the **designated pin cell** (e.g., the selftest cell) to equal the expected value exactly, not a whole-line substring.
2. Re-measure at check time (re-run the selftest / recompute sha256 of the instruments) rather than comparing against hardcoded literals; fail when the snapshot pins differ from the live measurement.
3. Count mismatches per needle (or per cell), not per row; report `rows=` from the actual matched row count, and reject any duplicate/ambiguous prefix rows anywhere in the file.
4. Consider dropping the superseded duplicate row from the requirement set, or make the supersession explicit (one requirement per logical registry).

## 5. Evidence-only notes

- No repo files edited; scratch files used only under `/tmp` (`/tmp/control_attack1.md`, `/tmp/skill_*.md`). No git/jj mutations.
- The unmodified control remains red (verified). The falsification shows the freeze's *sufficiency gap*: prose mention of the pins passes it, so it does not force actual re-pinning; and its static literals make it blind to future instrument drift.
