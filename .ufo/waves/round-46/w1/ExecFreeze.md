# ExecFreeze — freeze manifest recomputation vs successful checks

**Seat**: `L1Mori46.ExecFreeze` (executor, leaf)
**Assignment**: Recompute freeze manifest checks and count non-comment lines versus successful checks.
**Wave**: mori-r46-calibration-repair. **Lane repo**: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
**Scope**: read-only recomputation; no edits, no git/jj operations, no installs/upgrades.

---

## 1. What the freeze manifest is

The manifest that feeds round-46's frozen predicate is `.ufo/waves/round-45/evidence/freeze-r45.txt`
(written by the L1 at the round-45 landing commit). It records 27 `<sha256>  <repo-relative path>`
entries. The four digests baked into `count-repins.py` are exactly four of these manifest entries
(§3). No other freeze manifest exists under round-46 (the round-46 wave dir contains only
`count-repins.py`, `control-skill.md`, the spec/dispatch JSONs, and the swarm registry); no repo tool
consumes freeze manifests (grep over `tools/` for `freeze-r4|freeze.*manifest|manifest.*freeze`:
no matches), so the checks are recomputed directly with `sha256sum`/`hashlib`.

## 2. Recomputed check results

Method: parse each line; count comment lines (`#` prefix) and blank lines; for every non-comment
entry, compute the live sha256 of the resolved path and compare to the recorded pin. All 27 paths
resolve; none is missing.

| Metric | Count |
|---|---|
| Total lines in `freeze-r45.txt` | 31 |
| Comment lines (`# …`, incl. the external census entry) | 3 |
| Blank lines | 1 |
| **Non-comment entries (= checks)** | **27** |
| Checks that pass (live sha256 == pinned sha256) | **25** |
| Checks that fail (live sha256 != pinned sha256) | **2** |

Failed checks (the only two entries whose live bytes differ from the pins):

| Manifest line | Path | Pinned sha256 (prefix) | Live sha256 (prefix) |
|---|---|---|---|
| 4 | `SKILL.md` | `ed71e8f6e68c…` | `15a3385d9329…` |
| 5 | `corpus/SOURCES.md` | `9d1bcdcf9f40…` | `900b3f9226fc…` |

All 25 remaining entries — including every counter, mutant, witness, fixture, and tool — match their
pins exactly. The external entry is commented out (line 31) but was still verified:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` live sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30` == recorded pin. ✓

## 3. The predicate's pins are the manifest's pins (and all four hold)

`count-repins.py` `ROWS` requires four needles classes; each digest needle equals a freeze-manifest
pin for the corresponding instrument:

| Predicate row | Digest needle | Manifest entry | Live file matches pin? |
|---|---|---|---|
| `r45 ledger counter (C1)` | `5f2deea0b35c5e1346229d265aa0c07bf7f365bf6c5acda87648045bce658d23` | `…/round-45/count-c1.py` (line 12) | yes |
| `r45 gate conformance (C2)` | `153423c48ca90466e85b02707828f5c6b2cf39c87c68ee67e3f9abee956baf93` | `…/round-45/count-c2.py` (line 13) | yes |
| `r45 gate conformance (C2)` | `9850b3fcc8885456c3e71458b34184d716d54880a91ae5b29c7d003f26708703` | `…/round-45/fixtures/mutants/count-c2.py` (line 18) | yes |
| `r44 gate registry (C2)` and `… — write scope superseded` | `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832` | `tools/mori-gate-registry.py` (line 24) | yes |

So every digest the predicate checks is a valid, currently-holding freeze-manifest pin. The measure
pins (the self-test tallies and the `743 lines` count) are row content, not manifest entries.

## 4. Predicate runs (frozen counter, read-only)

```
$ python3 .ufo/waves/round-46/count-repins.py SKILL.md
MORI_R45_REPINS mismatches=0 rows=4
rc=0

$ python3 .ufo/waves/round-46/count-repins.py .ufo/waves/round-46/control-skill.md
MORI_R45_REPINS mismatches=4 rows=4
r44 gate registry (C2): stale/missing 1 pin(s)
r45 ledger counter (C1): stale/missing 2 pin(s)
r45 gate conformance (C2): stale/missing 5 pin(s)
r44 gate registry (C2) — write scope superseded: stale/missing 3 pin(s)
rc=1
```

- Live `SKILL.md` (rows at lines 184, 190, 191, 194, each present exactly once with all needles):
  **green** (`mismatches=0 rows=4`, rc 0).
- Control `control-skill.md`: **red** (`mismatches=4`, rc 1) — and its sha256
  `ed71e8f6e68c059deefb1f9bcfec42f12f2ae3bdb21aff6d5bc9bca2561cb9ad` is byte-identical to the
  freeze manifest's `SKILL.md` pin (manifest line 4), confirming the control is the exact frozen
  snapshot.

## 5. Findings

1. **25/27 non-comment freeze-manifest checks succeed; 2 fail.** The two failures are
   `SKILL.md` and `corpus/SOURCES.md` — both documentation files whose live bytes differ from the
   round-45 pins. The four instrument digests the predicate depends on are all still green.
2. **The manifest's own state does not drive the predicate.** `count-repins.py` checks only the
   four named SKILL.md rows and never reads `freeze-r45.txt`; a stale `SKILL.md`/`SOURCES.md`
   manifest entry (or any other manifest entry) does not flip the predicate. The predicate is a
   four-row spot check, not a full-manifest verifier — the 27-entry manifest is wider than what the
   predicate guards.
3. **Control identity confirmed.** `control-skill.md` == the frozen `SKILL.md` pin; running the
   counter on it yields the required red (`mismatches=4`), so the do-nothing control bites.
4. **Green live state is consistent with its pins.** Current `SKILL.md` differs from the manifest
   pin (it post-dates the freeze) yet still satisfies all four rows' needles; the row content is
   aligned with the still-holding instrument pins.

## 6. Risks / blockers / notes

- No blocker. No files written outside this report; no git/jj mutations; no tool installs.
- The two stale manifest entries are expected drift from the round-46 working-tree edits; whether
  the manifest should be re-pinned is outside this seat's judgment (report-only).
- Exact commands used: `sha256sum` over the 27 manifest paths; a read-only Python comparison of
  `freeze-r45.txt` pins vs live hashes; `count-repins.py` runs on `SKILL.md` and
  `control-skill.md` (stdout + rc captured).
