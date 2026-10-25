# CritSelfAssessment — SCORECARD/SHONEN self-assessment vs observed registry state

Seat: `CritSelfAssessment` (round-46 w1). Scope: check the lane's self-assessment
in `SCORECARD.md` (round-46 declaration, `## Gates` registry rows) and
`SHONEN.md` against the observed repo/fleet state. No edits made; evidence only.

## Method (all commands run from the lane root)

```
python3 .ufo/waves/round-46/count-repins.py SKILL.md
python3 .ufo/waves/round-46/count-repins.py .ufo/waves/round-46/control-skill.md
python3 .ufo/waves/round-46/count-repins.py /tmp/skill-parent.md
python3 tools/mori-gate-registry.py --selftest
python3 .ufo/waves/round-45/count-c1.py --selftest
python3 .ufo/waves/round-45/count-c2.py --selftest
sha256sum .ufo/waves/round-46/count-repins.py tools/mori-gate-registry.py \
  .ufo/waves/round-45/count-c1.py .ufo/waves/round-45/count-c2.py \
  .ufo/waves/round-45/fixtures/mutants/count-c2.py
wc -l tools/mori-gate-registry.py
jj file show -r 'ulqqunkl' SKILL.md > /tmp/skill-parent.md   # parent commit = round-45 landing
diff /tmp/skill-parent.md .ufo/waves/round-46/control-skill.md
```

## Finding 1 — SCORECARD round-46 declaration matches observed behavior

SCORECARD.md:2559-2561 declares: frozen counter `count-repins.py`, predicate
`MORI_R45_REPINS mismatches=0 rows=4`, counter SHA-256
`ebb6a6d3fe08d78791a45643d1ebda2243e5fff271eaada1d7f682317c673327`, control
red at 4 mismatches/exit 1, repaired registry green at 0/exit 0.

Observed (reproduced):

| claim | observed |
|---|---|
| counter SHA-256 | `sha256sum .ufo/waves/round-46/count-repins.py` → `ebb6a6d3fe08d78791a45643d1ebda2243e5fff271eaada1d7f682317c673327` — exact match |
| repaired registry green | `python3 .ufo/waves/round-46/count-repins.py SKILL.md` → `MORI_R45_REPINS mismatches=0 rows=4`, rc 0 |
| control red | `python3 .ufo/waves/round-46/count-repins.py .ufo/waves/round-46/control-skill.md` → `MORI_R45_REPINS mismatches=4 rows=4` (`r44 gate registry (C2): stale/missing 1`, `r45 ledger counter (C1): stale/missing 2`, `r45 gate conformance (C2): stale/missing 5`, `r44 gate registry (C2) — write scope superseded: stale/missing 3`), rc 1 |
| control is the prior committed SKILL snapshot | `jj file show -r 'ulqqunkl' SKILL.md` (parent = round-45 landing `9834fed4`) is byte-identical to `control-skill.md` (`diff -q` clean, both 912 lines) — the control is genuinely the committed snapshot, and it is red under the counter |

## Finding 2 — the four rows' pins match measured tool bytes

Each pin in the repaired rows (SKILL.md:184,190,191,194) was independently
re-measured:

| row | pin in row | measured |
|---|---|---|
| r44 gate registry (C2) | `GATE_REGISTRY_SELFTEST pass=15 fail=0`, sha256 `8b82ac99…`, 743 lines | `python3 tools/mori-gate-registry.py --selftest` → `GATE_REGISTRY_SELFTEST pass=15 fail=0`, rc 0; sha256 `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832`; `wc -l` → 743 |
| r45 ledger counter (C1) | `C1_SELFTEST pass=16 fail=0`, sha256 `5f2deea0…` | `python3 .ufo/waves/round-45/count-c1.py --selftest` → `C1_SELFTEST pass=16 fail=0`, rc 0; sha256 `5f2deea0b35c5e1346229d265aa0c07bf7f365bf6c5acda87648045bce658d23` |
| r45 gate conformance (C2) | `C2_SELFTEST pass=14 fail=0`, sha256 `153423c4…`, mutant sha256 `9850b3fc…`, auditor sha256 `8b82ac99…`, 743 lines | `python3 .ufo/waves/round-45/count-c2.py --selftest` → `C2_SELFTEST pass=14 fail=0`, rc 0; sha256 `153423c48ca90466e85b02707828f5c6b2cf39c87c68ee67e3f9abee956baf93`; `5f2deea0…`'s sibling `9850b3fcc8885456c3e71458b34184d716d54880a91ae5b29c7d003f26708703` = `.ufo/waves/round-45/fixtures/mutants/count-c2.py`; `8b82ac99…` = auditor |
| r44 gate registry (C2) — write scope superseded | `GATE_REGISTRY_SELFTEST pass=15 fail=0`, sha256 `8b82ac99…`, 743 lines | same as row 184; "re-run 2026-10-25" is today's date |

No stale residue remains in the four repaired rows: the old pins recorded at the
round-45 landing (`pass=6 fail=0`, `pass=10 fail=0`, `f80e75ac…`, `e8ee29eb…`,
`d67ffacd…`, `64db765e…/622` per fleet MANIFEST round-45 `verification.rechecks`)
appear nowhere in SKILL.md:184/190/191/194 (grep: zero hits; the only `622`
is a substring of the correct ledger-counter sha256).

## Finding 3 — SHONEN.md is stale relative to observed state (under-claim)

`SHONEN.md` (promotion checklist, mtime 2026-10-20) shows all four boxes
unchecked. Two boxes' conditions are observably met by the registry/bytes:

- box 1 "SKILL.md contains real decision tables, error patterns, checklists, cited sources":
  SKILL.md has `## Decision table`, `## Error patterns`, `## Checklist (executable)`,
  `## Gates` and cited sources throughout (142 KB, 912 lines);
- box 2 "At least one end-to-end domain task executed and logged in LOG.md":
  LOG.md carries rounds 40–46 with measured before→after commands and evidence.

The all-unchecked state therefore does not match observed repo state under the
AXES.md calibration definition ("SHONEN.md/SCORECARD entries match observed repo
state", `fleet root AXES.md:15`). The mismatch is conservative (an under-claim:
no readiness is asserted; fleet MANIFEST still ranks the lane shonen and the
round-45 closure was `rejected-harmed`), so it misrepresents nothing upward, but
the checklist is stale.

## Finding 4 — minor naming nit in the declaration

SCORECARD.md:2561 calls the four rows "four round-45 SKILL.md registry rows";
two of the four row names are round-44 (`r44 gate registry (C2)` and its
write-scope superseder). This is not a substantive mismatch: the fleet round-45
verifier flagged exactly these four lines (SKILL.md:184/190/191/194) as the
stale-pin rows at `baabc992` (MANIFEST round-45 `verification.rechecks`), so
"round-45" refers to the flagging/repair round.

## Finding 5 — predicate limitation (not a defect of the repair)

`count-repins.py` checks substring presence per row (needles in the row line).
It would still pass a row that carried both an old pin and the new pin; it does
not *enforce* absence of stale values. Today's repaired content is clean (Finding
2), so the stronger "match measured pins only" reading also holds for the current
bytes; the limitation matters for future edits.

## Verdict

The SCORECARD round-46 self-assessment (declaration + four `## Gates` row pins)
is consistent with the observed registry state on every checkable point: green
only on the repaired (working-copy) SKILL.md, red on the committed do-nothing
control, and every pin re-measures to the committed tool bytes. The one
inconsistency found is SHONEN.md's stale all-unchecked state (Finding 3), an
under-claim in the safe direction.

Impacted axes: calibration (SCORECARD/shonen entries must match observed repo
state; the four row pins now do — SHONEN.md alone is stale).

Smallest safe correction: update `SHONEN.md`'s checkbox state (or annotate the
two observably-met boxes as met-pending-formal-admission) so the checklist
reflects the repo state; no other correction needed for the round-46 claim.
