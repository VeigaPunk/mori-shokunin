# ExecCounter — frozen counter run vs current SKILL and committed round-45 control

Seat: `L1Mori46.ExecCounter` (executor). Lane: `mori-shokunin`. Wave: round-46 w1 (calibration repair falsification).
Task: run the frozen counter `count-repins.py` against the current SKILL and the committed round-45 control; report outputs and exit codes. No files edited besides this report; no git/jj mutations; no installs.

## Instrument

Frozen counter: `.ufo/waves/round-46/count-repins.py` (untracked round-46 instrument, used as-is, unmodified).
It defines `ROWS` = 4 rows and checks each row for exactly one match (`line.startswith("| <row> |")`) and the presence of every expected pin needle in that row. It prints `MORI_R45_REPINS mismatches=<n> rows=4` (+ one `stale/missing` line per failing row) and exits 0 if no errors, 1 otherwise.

## Runs (exact commands, stdout, exit codes)

### 1. Current SKILL.md — `python3 .ufo/waves/round-46/count-repins.py SKILL.md` (repo root, working tree)

```
MORI_R45_REPINS mismatches=0 rows=4
```

Exit code: **0** (green).

### 2. Committed round-45 control — `python3 .ufo/waves/round-46/count-repins.py .ufo/waves/round-46/control-skill.md`

```
MORI_R45_REPINS mismatches=4 rows=4
r44 gate registry (C2): stale/missing 1 pin(s)
r45 ledger counter (C1): stale/missing 2 pin(s)
r45 gate conformance (C2): stale/missing 5 pin(s)
r44 gate registry (C2) — write scope superseded: stale/missing 3 pin(s)
```

Exit code: **1** (red).

## Control provenance

`control-skill.md` is **byte-identical** to the committed round-45 SKILL snapshot at HEAD: `git show HEAD:SKILL.md` ≡ `control-skill.md` (verified with `diff -q`). HEAD is `18fd68b0` "round-45: SKILL.md registry refresh, corpus entry + row + README map, QUALITY 120-122, lesson, selftest branches" — the last commit that touched SKILL.md. So the control is the prior committed r45 SKILL snapshot: the do-nothing control. It remains red (mismatches=4, exit 1), as the predicate requires.

## Working-tree delta

`git diff HEAD -- SKILL.md` shows exactly **4 lines replaced** (4 insertions / 4 deletions), one per counter-tracked row — r44 gate registry (C2), r45 ledger counter (C1), r45 gate conformance (C2), r44 gate registry (C2) — write scope superseded. No row added/removed; each row still occurs exactly once in current SKILL.md.

## Per-row pin evidence (independent re-check, same needle logic as the counter)

| Row | Current SKILL.md | Control |
|---|---|---|
| r44 gate registry (C2) | row count 1, missing pins NONE → OK | row count 1, missing `GATE_REGISTRY_SELFTEST pass=15 fail=0` → STALE |
| r45 ledger counter (C1) | row count 1, missing pins NONE → OK | row count 1, missing `C1_SELFTEST pass=16 fail=0`, `5f2deea0b35c5e1346229d265aa0c07bf7f365bf6c5acda87648045bce658d23` → STALE |
| r45 gate conformance (C2) | row count 1, missing pins NONE → OK | row count 1, missing `C2_SELFTEST pass=14 fail=0`, `153423c48ca90466e85b02707828f5c6b2cf39c87c68ee67e3f9abee956baf93`, `9850b3fcc8885456c3e71458b34184d716d54880a91ae5b29c7d003f26708703`, `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832`, `743 lines` → STALE |
| r44 gate registry (C2) — write scope superseded | row count 1, missing pins NONE → OK | row count 1, missing `GATE_REGISTRY_SELFTEST pass=15 fail=0`, `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832`, `743 lines` → STALE |

Total: current carries all 12 expected pins across the 4 rows; the control misses 11 pins (1+2+5+3). No duplicate rows anywhere; each of the 4 rows occurs exactly once in both snapshots.

## Findings

1. `count-repins.py` against **current SKILL.md**: `MORI_R45_REPINS mismatches=0 rows=4`, **exit 0**.
2. `count-repins.py` against **committed round-45 control** (`control-skill.md` = `git show HEAD:SKILL.md` byte-identical): `MORI_R45_REPINS mismatches=4 rows=4`, **exit 1** — the do-nothing control stays red.
3. The current SKILL.md working-tree change is confined to the 4 counter-tracked rows (4-line replacement), and the counter's green result is consistent with the pins being present row-by-row (all 12 needles found, no duplicates).
4. Predicate as stated (counter green `rows=4` exactly when the four rows carry the measured pins; committed r45 snapshot remains red) is **observed to hold** for these two inputs. Verdict scope: this seat reports outputs and exit codes only; falsification analysis is other seats' scope.

## Risks / notes

- The counter greps row text by `startswith("| <row> |")`; the em-dash row name matches the SKILL.md text exactly (verified 1 match per row in both files).
- Control red output depends on the control snapshot being the committed r45 file, which was verified byte-identical to HEAD's SKILL.md.
- No other behavior asserted here.
