# MutStaleC2 — mutation-tester report (round 46, w1)

**Role:** mutation-tester · **Probe:** restore stale C2/auditor/mutant digests, tallies and line count in the `r45 gate conformance (C2)` row; run the frozen counter (`count-repins.py`); report exact result.

## Claimed invariant (frozen predicate)

`count-repins.py` reports `mismatches=0 rows=4` only when four specific SKILL.md rows match measured pins. The prior committed SKILL snapshot (do-nothing control) must remain red.

## Mutation (smallest behavior-bearing point)

Scratch copy `.scratch/MutStaleC2/mutant.md` = byte copy of production `SKILL.md` (912 lines, sha256 `15a3385d9329a0cb2d6fea931e3a032ec3ef0630fa9de152a78a402d5eb6dc47`). One row mutated — line 191 `| r45 gate conformance (C2) |` — restoring the five stale pin values recorded in the prior committed control snapshot (`control-skill.md:191`, v1/early-r45 values):

| element | current (measured) pin | stale restored (control) |
|---|---|---|
| selftest tally | `C2_SELFTEST pass=14 fail=0` | `C2_SELFTEST pass=10 fail=0` |
| counter digest | `153423c48ca90466e85b02707828f5c6b2cf39c87c68ee67e3f9abee956baf93` | `e8ee29eb8852…` |
| mutant digest | `9850b3fcc8885456c3e71458b34184d716d54880a91ae5b29c7d003f26708703` | `d67ffacdb3ec…` |
| auditor digest | `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832` | `64db765e60e3…` |
| line count | `743 lines` | `622 lines` |

All other 911 lines byte-identical. Mutant sha256 `931199ac2aec22e45a5dcbe9b6c4e420ec955bb50d221b175506a7b3c5a387d8`.

## Expected detector

Frozen counter on mutant snapshot should report `mismatches=1` (the C2 row loses its 5 needles) and exit 1 — mutant killed.

## Actual outputs

| snapshot | stdout | exit |
|---|---|---|
| pristine (baseline) | `MORI_R45_REPINS mismatches=0 rows=4` | 0 |
| mutant | `MORI_R45_REPINS mismatches=1 rows=4` + `r45 gate conformance (C2): stale/missing 5 pin(s)` | 1 |
| restored | `MORI_R45_REPINS mismatches=0 rows=4` | 0 |

## Verdict

**KILLED.** The frozen counter detects the restored stale C2/auditor/mutant digests, selftest tally and line count: `mismatches=1`, `stale/missing 5 pin(s)`, exit 1. No false green; the invariant held under this defect. Baseline failure not observed at any step (baseline exited 0), so no inconclusive result.

## Restoration evidence

- Before mutation: pristine & mutant both `15a3385d9329a0cb2d6fea931e3a032ec3ef0630fa9de152a78a402d5eb6dc47` (= production `SKILL.md`).
- After mutation: mutant `931199ac2aec22e45a5dcbe9b6c4e420ec955bb50d221b175506a7b3c5a387d8`.
- After restore: `cp pristine.md mutant.md`; `sha256sum` equal (`15a3385d…`); `cmp` = identical bytes; counter parity restored (exit 0, mismatches=0).
- Production `SKILL.md` untouched (all edits confined to `.scratch/MutStaleC2/`). No git/jj mutations. No tool installs/upgrades made; pacman not invoked.
