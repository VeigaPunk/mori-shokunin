# RevC2Cell — C2 row counter, pins, tally, and auditor line count

## Evidence

- Frozen counter: `.ufo/waves/round-46/count-repins.py` defines four row keys. For `r45 gate conformance (C2)`, it requires `C2_SELFTEST pass=14 fail=0`, counter SHA-256 `153423c48ca90466e85e02707828f5c6b2cf39c87c68ee67e3f9abee956baf93`, mutant SHA-256 `9850b3fcc8885456c3e71458b34184d716d54880a91ae5b29c7d003f26708703`, auditor SHA-256 `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832`, and `743 lines` (counter lines 12–16).
- I ran `python /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-46/count-repins.py` from the lane root. Observed stdout: `MORI_R45_REPINS mismatches=0 rows=4`; shell tool reported successful exit (0).
- The targeted current `SKILL.md` row 191 contains the `C2_SELFTEST pass=14 fail=0` tally; it is also independently recorded by `ScoutTally.md` as output of `python3 .ufo/waves/round-45/count-c2.py --selftest`, exit 0, with 14 distinct PASS arm names (lines 37–49).
- `ExecAuditorLines.md` records all four measured SHA-256 values equal the pins and `wc -l tools/mori-gate-registry.py` = 743 (lines 9–33); its reproduced command is stated at line 18. This covers the auditor (`tools/mori-gate-registry.py`), C1 counter, C2 counter, and C2 mutant files.
- Mutant evidence: `MutStaleC2.md` reports a scratch mutant restoring the stale C2 tally/digests/line count; the frozen counter reported `mismatches=1 rows=4`, specifically five missing C2 pins, exit 1, while pristine/restored snapshots returned mismatches 0 (lines 9–43). The scratch change was outside production files.
- Control evidence: `ExecCounter.md` reports the frozen counter on current candidate as green, and on `.ufo/waves/round-46/control-skill.md` as `mismatches=4 rows=4`, exit 1; it documents the control as byte-identical to committed `HEAD:SKILL.md` (lines 13–35).

## Finding

No actionable defect found in this scoped C2 calibration evidence. The C2 row has the expected tally and measured pins, the auditor line count is consistent, stale-pin mutation is detected, and the prior committed control remains red. This is evidence for the named predicate on the inspected snapshots, not a broader correctness claim.

## Residual risk / verification gap

The counter validates literal needles within uniquely matching rows; it does not independently establish correctness of the underlying instruments. The separate tally and digest reports supply that evidence here. I did not rerun those instruments or mutate files; their reported command outputs are cited above. No installs/upgrades made.

Report: `.ufo/waves/round-46/w1/RevC2Cell.md`
