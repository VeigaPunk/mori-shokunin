# MutDuplicate — mutation probe: added duplicate target row vs `count-repins.py`

Seat: mutation-tester, mori round 46 wave 1. Leaf seat; no subagents dispatched.
No tool installs/upgrades made; no pacman transactions; no git/jj mutations.

Target counter (never edited by me):
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-46/count-repins.py`
sha256 `ebb6a6d3fe08d78791a45643d1ebda2243e5fff271eaada1d7f682317c673327`.

Subject file (never edited by me): `SKILL.md` (lane root), sha256
`15a3385d9329a0cb2d6fea931e3a032ec3ef0630fa9de152a78a402d5eb6dc47`, 912 lines.
Do-nothing control: `.ufo/waves/round-46/control-skill.md`, sha256
`ed71e8f6e68c059deefb1f9bcfec42f12f2ae3bdb21aff6d5bc9bca2561cb9ad`.

Scratch: `/tmp/MutDuplicate-scratch-skill.md` — byte-identical copy of the
live `SKILL.md` (same sha256), mutated only there. Production `SKILL.md` was
never written; lane hashes measured before and after the probe (below).

## Mutation

Inserted a **byte-exact duplicate** of the target row `r45 gate conformance
(C2)` (SKILL.md line 191, one of the four rows the frozen predicate pins)
directly after its original line. The "added duplicate target row" is the
single behavior-bearing point: the counter's row lookup is
`[line for line in lines if line.startswith("| " + row + " |")]`, and the
invariant demands exactly one such line per row.

Scratch line count: 912 → 913. Mutated scratch sha256
`48206c32654a3f06f2ba85e8bafe7e2eed2a8083ab97f5b6abea322df651983f`.

## Detector runs (same counter, same CLI)

| input | counter stdout | rc |
|---|---|---|
| pristine `SKILL.md` (and pristine scratch, identical bytes) | `MORI_R45_REPINS mismatches=0 rows=4` | 0 |
| mutated scratch (duplicate target row) | `MORI_R45_REPINS mismatches=1 rows=4`<br>`r45 gate conformance (C2): expected one row, found 2` | 1 |
| do-nothing control `control-skill.md` | `MORI_R45_REPINS mismatches=4 rows=4` + 4 `stale/missing` lines | 1 |

## Verdict

**KILLED.** The counter catches the added duplicate target row: the exact-one-row
invariant trips on `len(matches) == 2`, and the verdict flips
`mismatches=0 rows=4` rc 0 → `mismatches=1 rows=4` rc 1 with the row-naming
error line. This is the designed behavior of the frozen predicate (green only
when each of the four rows matches measured pins exactly once). The do-nothing
control remains red (rc 1, 4 mismatches), so the red baseline is preserved.

Coverage note: this exercised the `len(matches) != 1` branch of all four rows'
shared lookup (row `r45 gate conformance (C2)` selected). The branch is
row-agnostic; the same probe applied to any of the other three target rows hits
the same code path, and the needles check is untouched by this mutation.

## Restoration evidence

Production hashes re-measured after the probe — all unchanged:

```
15a3385d9329a0cb2d6fea931e3a032ec3ef0630fa9de152a78a402d5eb6dc47  SKILL.md
ed71e8f6e68c059deefb1f9bcfec42f12f2ae3bdb21aff6d5bc9bca2561cb9ad  .ufo/waves/round-46/control-skill.md
ebb6a6d3fe08d78791a45643d1ebda2243e5fff271eaada1d7f682317c673327  .ufo/waves/round-46/count-repins.py
```

No sibling seat's files touched; only the scratch copy in `/tmp` and this report
were written.

## Reproduce

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin
cp SKILL.md /tmp/MutDuplicate-scratch-skill.md
python3 .ufo/waves/round-46/count-repins.py /tmp/MutDuplicate-scratch-skill.md   # mismatches=0 rows=4, rc 0
# insert a byte-exact copy of SKILL.md line 191 after line 191 in the scratch
python3 .ufo/waves/round-46/count-repins.py /tmp/MutDuplicate-scratch-skill.md   # mismatches=1 rows=4, rc 1
```
