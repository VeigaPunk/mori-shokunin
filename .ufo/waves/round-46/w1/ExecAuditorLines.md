# ExecAuditorLines — auditor digest and line count vs registry rows

Round 46 (mori-r46-calibration-repair), 2026-10-25. Lane repo:
`/home/vgpnk/Projects/shokunin/mori-shokunin`.
Seat: ExecAuditorLines. Scope: check the auditor digests and the `743 lines`
claim pinned in the four `count-repins.py` registry rows against the measured
files. No code edited; no installs; pacman untouched.

## 1. Pinned digest vs measured sha256 (working tree)

| Pinned registry row | Pinned sha256 | Measured file | Measured sha256 | Match |
|---|---|---|---|---|
| r44 gate registry (C2) / r45 gate conformance (C2) / r44 gate registry (C2) — write scope superseded | `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832` | `tools/mori-gate-registry.py` | `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832` | YES |
| r45 ledger counter (C1) | `5f2deea0b35c5e1346229d265aa0c07bf7f365bf6c5acda87648045bce658d23` | `.ufo/waves/round-45/count-c1.py` | `5f2deea0b35c5e1346229d265aa0c07bf7f365bf6c5acda87648045bce658d23` | YES |
| r45 gate conformance (C2) | `153423c48ca90466e85b02707828f5c6b2cf39c87c68ee67e3f9abee956baf93` | `.ufo/waves/round-45/count-c2.py` | `153423c48ca90466e85b02707828f5c6b2cf39c87c68ee67e3f9abee956baf93` | YES |
| r45 gate conformance (C2) (mutant) | `9850b3fcc8885456c3e71458b34184d716d54880a91ae5b29c7d003f26708703` | `.ufo/waves/round-45/fixtures/mutants/count-c2.py` | `9850b3fcc8885456c3e71458b34184d716d54880a91ae5b29c7d003f26708703` | YES |

Reproduce: `sha256sum tools/mori-gate-registry.py .ufo/waves/round-45/count-c1.py .ufo/waves/round-45/count-c2.py .ufo/waves/round-45/fixtures/mutants/count-c2.py` (run in lane root).

All 4 pinned digests match the current files byte-for-byte. Identical hashes
are independently recorded in the round-45 freeze
`.ufo/waves/round-45/evidence/freeze-r45.txt` (lines 12, 13, 18, 24) and in
`registry-audit-all.txt` (v2 run sha `8b82ac99…`), so the pins reflect the
measured round-45 instrument bytes, not new text minted for this wave.

## 2. Line-count pin vs measured line count

- Pin `743 lines` (rows `r45 gate conformance (C2)` and
  `r44 gate registry (C2) — write scope superseded`; row
  `r44 gate registry (C2)` carries `(743 lines)`).
- Measured: `wc -l tools/mori-gate-registry.py` = **743** (31165 bytes).
- Match: YES. Consistent with round-45 evidence (`MutAuditor.md`, 743 lines /
  31165 bytes; `SentInstruments.md`, 31165 bytes).

## 3. Needle presence per snapshot (what the predicate sees)

`count-repins.py` has 11 needles across its 4 ROWS
(1 + 2 + 5 + 3). Each row must occur exactly once and contain its needles.

| Snapshot | Rows present (each exactly once) | Needles found | Predicate effect |
|---|---|---|---|
| Working-tree `SKILL.md` (repair candidate) | 4/4 (`:184`, `:190`, `:191`, `:194`) | 11/11 | GREEN premise holds: `mismatches=0 rows=4` |
| `control-skill.md` (do-nothing control; `==` committed `HEAD:SKILL.md`) | 4/4 | 0/11 | RED preserved: all four rows miss their pins |

Per-needle counts (`grep -Fc` over the whole file):
- `SKILL.md`: `GATE_REGISTRY_SELFTEST pass=15 fail=0` ×3, `C1_SELFTEST pass=16 fail=0` ×1, `5f2deea0…` ×1, `C2_SELFTEST pass=14 fail=0` ×1, `153423c48c…` ×1, `9850b3fc…` ×1, `8b82ac99…` ×3, `743 lines` ×3 → 11/11.
- `control-skill.md`: all eight probes = 0 → 0/11.

Predicate row matching: `lines.startswith("| " + row + " |")` — row keys match
only lines 184 / 190 / 191 / 194 respectively (line 194's key includes the
`— write scope superseded` suffix, so it does not collide with line 184).
No duplicates observed in either snapshot.

`diff` of lines 183–196 vs control shows the only differences are in the
selftest/pin cells of exactly these four rows (e.g. row 184: current `pass=15
fail=0` + sha256 + `(743 lines)` vs control `pass=6 fail=0`; row 194: current
`pass=15 fail=0` + sha256 + `743 lines` vs control v1/v2 `pass=6/pass=10`).

## 4. Findings

1. All four pinned auditor digests match the files in the working tree; the
   `743 lines` line-count pin matches `tools/mori-gate-registry.py` exactly.
   The registry rows describe the files actually present.
2. The current working-tree `SKILL.md` carries all 11 needles in their correct
   rows, so `count-repins.py` would report `mismatches=0 rows=4` on it.
3. The control (`control-skill.md`, byte-identical to committed
   `HEAD:SKILL.md`) carries 0 of 11 needles and therefore stays red on all four
   rows, as required for the do-nothing control.

## 5. Risks / notes

- Working-tree `SKILL.md` is modified vs HEAD (`git status`: `M SKILL.md`);
  the repair pins live in the uncommitted candidate, not in the committed
  snapshot (the committed snapshot is the red control). The four auditor files
  are clean at HEAD `9834fed4dd8a2ee201ebc4183e2435f4c7272674`.
- Measurements are of the current working tree; no git mutations performed.
- `count-repins.py` execution itself is owned by the ExecCounter seat; this
  report supplies the digest/line-count and needle-presence evidence only.
