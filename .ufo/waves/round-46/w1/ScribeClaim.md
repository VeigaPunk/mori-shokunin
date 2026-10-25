# ScribeClaim — round-46 calibration claim: falsifiability & source support

Seat: `L1Mori46.ScribeClaim` (scribe). Scope: review only — no edits, no runs
that mutate the repo, no tool installs. Findings only.

## 1. Predicate identity and reproducibility

- Frozen counter `.ufo/waves/round-46/count-repins.py` exists; SHA-256 measured
  `ebb6a6d3fe08d78791a45643d1ebda2243e5fff271eaada1d7f682317c673327`, which
  matches the counter hash stated in `SCORECARD.md:2561` exactly.
- Output/exit contract as claimed: prints
  `MORI_R45_REPINS mismatches=<n> rows=4`; exit 0 when `n=0`, exit 1 otherwise.
  Deterministic pure function of the passed snapshot path; no git, network, or
  environment dependence.

## 2. Falsifiability — red-before / green-after reproduced

| snapshot | result (measured) |
|---|---|
| `control-skill.md` (committed do-nothing control) | `mismatches=4 rows=4`, exit 1 — all four rows flagged: r44 gate registry 1 stale pin, r45 C1 2, r45 C2 5, r44 superseding 3 |
| current `SKILL.md` | `mismatches=0 rows=4`, exit 0 |

Mutation sensitivity (temp copies of `SKILL.md`, no repo files touched):

- single-pin drift `GATE_REGISTRY_SELFTEST pass=15→14` → `mismatches=2`, exit 1
  (both rows carrying that pin fail);
- single-pin drift `C1_SELFTEST pass=16→15` → `mismatches=1`, exit 1;
- rename one row (`r45 ledger counter (C1)`) → `expected one row, found 0`, exit 1.

The predicate is therefore not vacuous: it reacts to per-pin drift, missing rows,
and renamed rows, and the committed control reproduces the exact entering defect
(four stale cells). Documented shape limits: needles are substring checks inside
one exact row-name match (a cell carrying both old and new pin would pass), `rows=4`
is the hardcoded `len(ROWS)`, and only the four named rows are examined — not every
registry cell. These bound the claim's precision but do not falsify it.

## 3. Source support — pins trace to measured values

Instrument byte pins verified against current worktree files:

| pin | source | measured |
|---|---|---|
| `5f2deea0b35c5e13…` | `.ufo/waves/round-45/count-c1.py` | sha256 matches |
| `153423c48ca90466e85b02…` | `.ufo/waves/round-45/count-c2.py` | sha256 matches |
| `9850b3fcc8885456c3e714…` | `.ufo/waves/round-45/fixtures/mutants/count-c2.py` | sha256 matches |
| `8b82ac999091ebe65e765e…` | `tools/mori-gate-registry.py` | sha256 matches; `wc -l` = 743 lines |

Selftest tallies traced to recorded measured runs:

- `GATE_REGISTRY_SELFTEST pass=15 fail=0` — `w1/CritAxisHarm.md:73` (15 arms, run),
  `w1/RevAudit.md:11` (rc 0);
- `C1_SELFTEST pass=16 fail=0` — `LOG.md:2642`, `w1/CritAxisHarm.md:75`;
- `C2_SELFTEST pass=14 fail=0` — `w1/ExecC2Counter.md:9,101` (rc 0).

Falsification anchor for the "before" state: the round-45 verifier spot-check
(`corpus/lessons/round-45-verifier-spotcheck.md:50-66`) documents the four cells
at `baabc992` carrying stale pins (`pass=10`, `pass=6`, wrong auditor digest, 622
lines) — the same four rows the control now reproduces as 4 mismatches;
`w1/CritAxisHarm.md:84-98` flagged the same cells in-round.

## 4. Scope notes

- Claim wording "four round-45 SKILL.md registry rows" is slightly loose: two of
  the four checked rows are r44-labeled (`r44 gate registry (C2)` and its
  superseding variant); both are rows of the round-45 SKILL.md registry snapshot.
- The counter checks SKILL.md text against recorded measurements; it does not
  re-hash instruments at runtime. The recorded measurements were independently
  verified against current worktree bytes above.

## 5. Verdict (findings only)

- Claim is falsifiable as specified: deterministic counter, committed red
  control reproduces the defect, green target reproduces the repair, and the
  predicate demonstrably flips red on single-pin drift and row rename.
- Claim is source-supported: all four byte pins and 743-line count match the
  actual instruments; all three selftest tallies match recorded measured runs in
  round-45 wave reports/LOG; the from-state defect is independently documented
  by the round-45 verifier spot-check.
- No unsupported verdict offered beyond the above; no code edited; no tools
  installed (none needed); no git/jj operations performed.
