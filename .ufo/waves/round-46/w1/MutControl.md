# MutControl — counter on old committed SKILL control

Seat: `MutControl` (mutation-tester, round-46 lane w1)
Date run: 2026-10-25
Repo: `/home/vgpnk/Projects/shokunin/mori-shokunin` (HEAD `9834fed4dd8a2ee201ebc4183e2435f4c7272674`)

## Task

> Run counter on old committed SKILL control and report mismatch count.

No code/production edits made; read-only run. No tool installs.

## What the control is

- `git show HEAD:SKILL.md | sha256sum` = `ed71e8f6e68c059deefb1f9bcfec42f12f2ae3bdb21aff6d5bc9bca2561cb9ad`
- `sha256sum .ufo/waves/round-46/control-skill.md` = `ed71e8f6e68c059deefb1f9bcfec42f12f2ae3bdb21aff6d5bc9bca2561cb9ad`
- Identical → `.ufo/waves/round-46/control-skill.md` is the prior committed SKILL snapshot (HEAD, round-45 state). Working-tree `SKILL.md` differs from HEAD (`git status`: ` M SKILL.md`; `git diff --numstat`: `4 4 SKILL.md`) — the round-46 edit is uncommitted.

## Command (exact)

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin
python3 .ufo/waves/round-46/count-repins.py .ufo/waves/round-46/control-skill.md
```

## Output (verbatim)

```
MORI_R45_REPINS mismatches=4 rows=4
r44 gate registry (C2): stale/missing 1 pin(s)
r45 ledger counter (C1): stale/missing 2 pin(s)
r45 gate conformance (C2): stale/missing 5 pin(s)
r44 gate registry (C2) — write scope superseded: stale/missing 3 pin(s)
rc=1
```

## Findings

1. **Mismatch count: 4** (rows=4). Every one of the four frozen rows exists exactly once in the control, but each is missing/contains stale pins — no row-count errors, only pin mismatches.
2. **Control is red as required.** rc=1. The do-nothing control (prior committed SKILL) does not satisfy the frozen predicate `count-repins.py reports mismatches=0 rows=4`.
3. Per-row pin shortfalls (needle counts from `count-repins.py` `ROWS`):
   - `r44 gate registry (C2)`: 1 missing pin (`GATE_REGISTRY_SELFTEST pass=15 fail=0`)
   - `r45 ledger counter (C1)`: 2 missing pins (`C1_SELFTEST pass=16 fail=0`, sha256 pin)
   - `r45 gate conformance (C2)`: 5 missing pins (`C2_SELFTEST pass=14 fail=0`, 3 sha256 pins, `743 lines`)
   - `r44 gate registry (C2) — write scope superseded`: 3 missing pins (`GATE_REGISTRY_SELFTEST pass=15 fail=0`, sha256 `8b82ac…`, `743 lines`)

## Verdict

Control = red: `mismatches=4` (rc=1). The prior committed SKILL snapshot is NOT a false green; the frozen predicate distinguishes it from a repaired SKILL. Baseline failure, not a killed mutant — no mutation was performed by this seat.

## Restoration evidence

Nothing was mutated. Control bytes untouched; identity hash recorded above (before/after identical, single read).

## Trailer

- Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`
- Report path (absolute): `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-46/w1/MutControl.md`
- No pacman, no installs, no git/jj mutations, no sibling/fleet writes.
