# ScoutDigests — recorded C1/C2/auditor/mutant SHA vs committed files

Wave: mori-r46-calibration-repair · Round 46 · Seat: ScoutDigests (scout, leaf)
Date: 2026-10-25 · Lane repo: /home/vgpnk/Projects/shokunin/mori-shokunin

## Scope

Independently compare the SHA pins recorded in the frozen predicate
`.ufo/waves/round-46/count-repins.py` (`ROWS` needles) against the actual sha256 and
line counts of the committed files they name. No editing; read-only queries.

## Result: all 4 recorded digests byte-match committed files

| Recorded SHA (count-repins.py needle) | Role in predicate | Committed file | Actual sha256 (computed) | Lines | Match |
|---|---|---|---|---|---|
| `5f2deea0b35c5e1346229d265aa0c07bf7f365bf6c5acda87648045bce658d23` | C1 counter digest | `.ufo/waves/round-45/count-c1.py` | `5f2deea0b35c5e1346229d265aa0c07bf7f365bf6c5acda87648045bce658d23` | 1172 | exact |
| `153423c48ca90466e85b02707828f5c6b2cf39c87c68ee67e3f9abee956baf93` | C2 counter digest | `.ufo/waves/round-45/count-c2.py` | `153423c48ca90466e85b02707828f5c6b2cf39c87c68ee67e3f9abee956baf93` | 1139 | exact |
| `9850b3fcc8885456c3e71458b34184d716d54880a91ae5b29c7d003f26708703` | C2 mutant digest | `.ufo/waves/round-45/fixtures/mutants/count-c2.py` | `9850b3fcc8885456c3e71458b34184d716d54880a91ae5b29c7d003f26708703` | 1139 | exact |
| `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832` | Auditor digest (C2 row and r44 registry rows) | `tools/mori-gate-registry.py` | `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832` | 743 | exact (incl. recorded "743 lines") |

All five source paths are tracked by git (`git ls-files --error-unmatch` passes for all);
`tools/mori-gate-registry.py` and the round-45 files show no pending working-tree diff
(git status porcelain lists only ` M SKILL.md` and `?? .ufo/waves/round-46/`).

## Per-row needle presence in the committed SKILL.md

Predicate rows match exactly one SKILL.md row each (startswith `| <row> |`; grep count =
1 for each name; no duplicates). All needles appear verbatim:

- **r44 gate registry (C2)** — SKILL.md:184 — contains `GATE_REGISTRY_SELFTEST pass=15 fail=0`, auditor sha256 `8b82ac99…f5832`, `743 lines`.
- **r45 ledger counter (C1)** — SKILL.md:190 — contains `C1_SELFTEST pass=16 fail=0` and counter sha256 `5f2deea0…d23`.
- **r45 gate conformance (C2)** — SKILL.md:191 — contains `C2_SELFTEST pass=14 fail=0`, counter sha256 `153423c48…af93`, mutant sha256 `9850b3fcc…08703`, auditor sha256 `8b82ac99…f5832`, `743 lines`.
- **r44 gate registry (C2) — write scope superseded** — SKILL.md:194 — contains `GATE_REGISTRY_SELFTEST pass=15 fail=0`, auditor sha256 `8b82ac99…f5832`, `743 lines`.

## Findings summary

1. Every SHA pin recorded in `count-repins.py` is a real, committed file whose sha256
   matches byte-for-byte. No stale/mismatched digest found.
2. The auditor line-count pin "743 lines" matches `tools/mori-gate-registry.py` exactly
   (wc -l = 743). Count-c1/count-c2 mutant line counts are not pinned by the predicate.
3. The rows the predicate scans exist exactly once each in SKILL.md (lines 184/190/191/194);
   row names match the predicate keys exactly, so the `len(matches) != 1` guard sees one row
   per key.

## Confidence and remaining unknowns

- Confidence: high for the digest/line-count comparison — computed directly with
  `sha256sum`/`wc -l` on the committed paths; cross-checked against round-45 freeze manifest
  (`evidence/freeze-r45.txt` pins the same `8b82ac99…f5832` for `tools/mori-gate-registry.py`)
  and round-45 seat reports.
- Not rerun here (out of digest-scope): the selftest tallies themselves
  (`pass=16/14/15 fail=0`) — asserted in SKILL.md rows 184/190/191/194; execution is
  ScoutTally/ExecCounter's seat. This report does not claim the tallies are true, only that
  the digest pins and the "743 lines" needle are consistent with committed bytes.
- Note: current working-tree `SKILL.md` is modified vs HEAD (the wave's in-progress repair);
  the digest-bearing files under round-45 and tools/ are unmodified committed snapshots, so
  the comparison applies to the committed state of the source instruments.
