# MutStaleC1 — restore stale C1 digest/tally, run counter

Seat: `L1Mori46.MutStaleC1` (mutation-tester, leaf member, no subagents).
Task: *Restore stale C1 digest/tally and run counter; report exact result.*
Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`.

## 1. Targeted invariant (frozen predicate)

`count-repins.py` (`.ufo/waves/round-46/count-repins.py`, sha256 `ebb6a6d3fe08d78791a45643d1ebda2243e5fff271eaada1d7f682317c673327`)
reports `mismatches=0 rows=4` only when the four SKILL.md rows listed in its `ROWS`
table contain the measured pins. For the C1 row `r45 ledger counter (C1)` the
meas needles are:

- `C1_SELFTEST pass=16 fail=0`
- `5f2deea0b35c5e1346229d265aa0c07bf7f365bf6c5acda87648045bce658d23` (digest of `.ufo/waves/round-45/count-c1.py`, verified: `sha256sum .ufo/waves/round-45/count-c1.py` = `5f2deea0…`; measured selftest on those bytes printed `C1_SELFTEST pass=16 fail=0` rc 0)

The prior committed SKILL snapshot (`.ufo/waves/round-46/control-skill.md`, sha256
`ed71e8f6e68c059deefb1f9bcfec42f12f2ae3bdb21aff6d5bc9bca2561cb9ad`) is the
do-nothing control and must remain red.

## 2. Probe (one mutation, smallest behavior-bearing point)

- Isolated scratch copy: `.scratch/MutStaleC1/SKILL.md` = byte copy of the green
  SKILL.md state at probe time (sha256 `15a3385d9329a0cb2d6fea931e3a032ec3ef0630fa9de152a78a402d5eb6dc47`).
  `SKILL.md` itself was never modified by this seat.
- Mutation: replace the single C1 row line (`| r45 ledger counter (C1) | …`,
  line 190) with the stale C1 row bytes from the control snapshot (also line 190)
  — i.e. restore the stale selftest tally and stale counter digest. Result:
  `.scratch/MutStaleC1/SKILL.mut`, sha256 `6ce6815f0bad97b5fef56b8f6c811f150316d64016afe22779cb97da4b48810b`.
  Only that one line differs from the pristine copy.
- Stale C1 pins restored (taken verbatim from control line 190):
  - `C1_SELFTEST pass=10 fail=0` (vs measured `pass=16 fail=0`)
  - `sha256 f80e75ac7421…` (vs measured full `5f2deea0…`; control row renders the digest truncated)
- Detector: `python3 .ufo/waves/round-46/count-repins.py <file>`, run on pristine,
  mutated and control bytes.

## 3. Results (exact outputs)

| input | sha256 | stdout | rc |
|---|---|---|---|
| pristine (copy-time SKILL.md bytes) | `15a3385d…` | `MORI_R45_REPINS mismatches=0 rows=4` | 0 |
| mutated (stale C1 restored) | `6ce6815f…` | `MORI_R45_REPINS mismatches=1 rows=4` + `r45 ledger counter (C1): stale/missing 2 pin(s)` | 1 |
| control (prior committed snapshot) | `ed71e8f6…` | `MORI_R45_REPINS mismatches=4 rows=4` + four stale/missing error lines (C1: `stale/missing 2 pin(s)`) | 1 |

Killed/se survived check: the counter killed the stale-C1 mutant — it flipped from
green (`mismatches=0`, rc 0) to `mismatches=1 rows=4`, rc 1, naming exactly the C1
row with `stale/missing 2 pin(s)`. No surviving mutant; no false green observed for
this probe.

## 4. Grounding of the measured pins

- `sha256sum .ufo/waves/round-45/count-c1.py` = `5f2deea0b35c5e1346229d265aa0c07bf7f365bf6c5acda87648045bce658d23` (matches the current C1 row's claimed digest).
- `TMPDIR=$PWD/.scratch/MutStaleC1/tmp python3 .ufo/waves/round-45/count-c1.py --selftest` on those bytes → 16 × `selftest PASS`, final line `C1_SELFTEST pass=16 fail=0`, rc 0. So `pass=16 fail=0` is a genuine measured tally of the pinned bytes, and the control row's `pass=10 fail=0` / `f80e75ac7421…` are the stale (pre-repair round-45 byte-state, cf. `round-45/evidence/control-c1.txt` churn note naming `f80e75ac` at 07:47–08:00) values.

## 5. Reproducibility note (concurrent drift)

During the probe the live `SKILL.md` changed on disk (lines 190/191 rewording;
sha went `15a3385d…` → `ec31c0f8422b6c5bf0e03586bc874a4ea85e30ed368c35b89778cc465ea36afa`).
The needle set in the live file is unchanged (all four rows still contain every pin;
live run = `mismatches=0 rows=4`, rc 0). This report's detector runs are pinned to
the snapshot bytes (`15a3385d…`, mutated `6ce6815f…`, control `ed71e8f6…`) so the
concurrent edit does not affect the verdict.

## 6. Restoration evidence

- `.scratch/MutStaleC1/SKILL.md` is still byte-identical to the copied source state
  (`15a3385d…`), verified after all runs. No production file, lane file, sibling
  seat file, or git/jj state was touched by this seat; only additive scratch
  artifacts exist under `.scratch/MutStaleC1/` (`SKILL.md`, `SKILL.mut`,
  `stale-c1-row.txt`, `tmp/`).
- No tools installed/upgraded; no pacman transactions run.
