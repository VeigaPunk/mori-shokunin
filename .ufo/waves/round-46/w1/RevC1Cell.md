# RevC1Cell — C1 row selftest tally and counter digest vs freeze manifest and output

Seat: `L1Mori46.RevC1Cell` — reviewer, mori round 46 (calibration repair falsification).
Scope: the `r45 ledger counter (C1)` row in the repaired `SKILL.md`, its selftest tally
and the frozen predicate's digest, checked against the round-45 freeze manifest and
measured output. Read-only; no edits to code/production/other seats' files; no installs.

## Frozen predicate under test

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-46/count-repins.py`
(`sha256sum` = `ebb6a6d3fe08d78791a45643d1ebda2243e5fff271eaada1d7f682317c673327`, which
matches the counter SHA-256 pinned in `SCORECARD.md` claim C1 exactly).
It counts one row per key in `ROWS` (4 keys) and prints `MORI_R45_REPINS mismatches=N rows=4`.
For the C1 row (`r45 ledger counter (C1)`), needles are:
`C1_SELFTEST pass=16 fail=0` and `5f2deea0b35c5e1346229d265aa0c07bf7f365bf6c5acda87648045bce658d23`.

## Reproduced measurements

| Check | Command (read-only) | Measured | Consistent? |
|---|---|---|---|
| Counter digest, repaired snapshot | `python3 .ufo/waves/round-46/count-repins.py SKILL.md` | `MORI_R45_REPINS mismatches=0 rows=4`, rc 0 | ✓ claim "after … 0 (exit 0)" |
| Counter digest, do-nothing control | `python3 .ufo/waves/round-46/count-repins.py .ufo/waves/round-46/control-skill.md` | `MORI_R45_REPINS mismatches=4 rows=4`, rc 1; C1 contributes `stale/missing 2 pin(s)` | ✓ claim "before … 4 mismatches (exit 1)" |
| C1 instrument bytes | `sha256sum .ufo/waves/round-45/count-c1.py` | `5f2deea0b35c5e1346229d265aa0c07bf7f365bf6c5acda87648045bce658d23` | ✓ freeze manifest line 12 |
| C1 mutant bytes | `sha256sum .ufo/waves/round-45/fixtures/mutants/count-c1.py` | `50900a3fce687430721e6ab36f4d293c928ddef33a3249477c51667881d2ed07` | ✓ freeze manifest line 17 |
| C1 selftest tally (pristine) | `python3 .ufo/waves/round-45/count-c1.py --selftest` | 16 PASS arms, `C1_SELFTEST pass=16 fail=0`, rc 0 | ✓ row + needle |
| C1 selftest tally (mutant) | `python3 .ufo/waves/round-45/fixtures/mutants/count-c1.py --selftest` | `duplicate_id_rejected` FAILs, `C1_SELFTEST pass=15 fail=1`, rc 1 | ✓ "is caught" |

## C1 row identity

- `SKILL.md` line 190 is the only line starting `| r45 ledger counter (C1) |` (grep, one hit),
  and it contains both needles verbatim: `C1_SELFTEST pass=16 fail=0` rc 0 at sha256
  `5f2deea0b35c5e1346229d265aa0c07bf7f365bf6c5acda87648045bce658d23`. The needle hash equals the
  measured on-disk hash of `.ufo/waves/round-45/count-c1.py` and the freeze-manifest pin, so the
  `in` substring match is a real instrument pin, not a stray occurrence.
- Control snapshot `control-skill.md` line 190 carries the stale tally `C1_SELFTEST pass=10 fail=0`
  at `f80e75ac7421…`; both C1 needles are absent, so the counter flags 2 missing pins there
  (control stays red as required).

## Findings

- **No blocking finding for the frozen predicate.** All C1-gated pins verify: instrument bytes
  match the freeze manifest; the SKILL.md C1 row carries exactly the frozen tally + hash; the
  measured pristine selftest reproduces `pass=16 fail=0` rc 0; the frozen counter digest is
  green on the repaired snapshot and red (4 mismatches) on the control, matching the scorecard
  claims (including the counter SHA-256).
- **Minor prose defect in the C1 row (outside the predicate's gated pins).** The row states the
  mutant "disables duplicate-command detection"; the pinned mutant (`50900a3fce…`) disables
  **duplicate-id** (`if False:` at line 478, `# MUTANT: duplicate-id check disabled`), while the
  `duplicate_command_rejected` check stays intact and PASSes on the mutant run. "…and is caught"
  is true (`pass=15 fail=1`, rc 1). The predicate does not token-check the mutant's prose, so the
  digest is unaffected; the label in the repaired cell is inverted.

## Residual risk / verification gaps

- Verified byte-level pins and the counted digest only for C1 (C2/C3-prot44 cells are other seats'
  scope). The predicate only asserts substring presence, not that the cell's prose is semantically
  exact — the mutant-label defect above is the observed instance of that gap.
- The round-45 freeze manifest (`round-45/evidence/freeze-r45.txt`) is the manifest referenced;
  no round-46 landing/freeze manifest existed at review time (wave still in flight), so the
  "measured commit recorded in the round report" claim was not yet checkable.
- All counter runs above used the on-disk `count-repins.py`; its sha256 equals the pinned counter
  hash, so no drift between the pinned and exercised predicate.
