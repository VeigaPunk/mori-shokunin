# CritVerdict — claim vs predicate vs receipt label: falsifier

Seat: `L1Mori46.CritVerdict` (critic). Lane: `mori-shokunin`. Wave: round-46 w1 (calibration repair falsification).
Task: compare claim, predicate and receipt label; report a falsifier. Scope: evidence only; no edits to code/production/other seats' files; no git/jj mutations.

## 1. What was compared

- **Claim (canonical, frozen context + `corpus/lessons/round-46.md`):** `count-repins.py` reports `mismatches=0 rows=4` **only when four specific SKILL.md rows match measured pins**; the prior committed SKILL snapshot (do-nothing control) must remain red.
- **Predicate:** `.ufo/waves/round-46/count-repins.py` (frozen, sha256 `ebb6a6d3fe08d78791a45643d1ebda2243e5fff271eaada1d7f682317c673327`). Mechanics: for each of `ROWS` (4 hard-coded row labels) it (a) requires exactly one line `startswith("| <row> |")`, and (b) requires every pin needle (selftest-tally string, digest, line count) to occur as a **substring of that one line**. One error per row; `len(errors)` printed as `mismatches`.
- **Receipt labels (measured pins):** the tally strings the instruments actually print when run, and the digests of the committed files, recorded in `.ufo/waves/round-45/evidence/freeze-r45.txt`.

## 2. Observed green/red behavior (reproduced)

| Input | Output | rc |
|---|---|---|
| current `SKILL.md` (working tree) | `MORI_R45_REPINS mismatches=0 rows=4` | 0 |
| `.ufo/waves/round-46/control-skill.md` (committed round-45 snapshot) | `MORI_R45_REPINS mismatches=4 rows=4` + 4 `stale/missing` lines | 1 |

Control red is real (11 of 12 needles absent across the four rows). Green is real on the current working tree (all 12 needles present, one row each).

## 3. Receipt labels vs predicate needles — exact match

Direct execution of the instruments (committed bytes):

- `python3 .ufo/waves/round-45/count-c1.py --selftest` → `C1_SELFTEST pass=16 fail=0` rc 0 — needle `C1_SELFTEST pass=16 fail=0` ✓
- `python3 .ufo/waves/round-45/count-c2.py --selftest` → `C2_SELFTEST pass=14 fail=0` rc 0 — needle `C2_SELFTEST pass=14 fail=0` ✓
- `python3 tools/mori-gate-registry.py --selftest` → `GATE_REGISTRY_SELFTEST pass=15 fail=0` rc 0 — needle `GATE_REGISTRY_SELFTEST pass=15 fail=0` ✓

Digest / line-count pins vs committed bytes and freeze manifest:

| Needle | Committed file | sha256 (computed) | / |
|---|---|---|---|
| `5f2deea0b35c5e1346229d265aa0c07bf7f365bf6c5acda87648045bce658d23` | `.ufo/waves/round-45/count-c1.py` | `5f2deea0…` | ✓ (in freeze-r45.txt) |
| `153423c48ca90466e85b02707828f5c6b2cf39c87c68ee67e3f9abee956baf93` | `.ufo/waves/round-45/count-c2.py` | `153423c48c…` | ✓ (in freeze-r45.txt) |
| `9850b3fcc8885456c3e71458b34184d716d54880a91ae5b29c7d003f26708703` | `.ufo/waves/round-45/fixtures/mutants/count-c2.py` | `9850b3fcc8…` | ✓ (in freeze-r45.txt) |
| `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832` + `743 lines` | `tools/mori-gate-registry.py` | `8b82ac9990…`, `wc -l` = 743 | ✓ (in freeze-r45.txt) |

So the *pins themselves* are genuine, measured receipts (tally strings byte-identical to instrument stdout; digests byte-identical to committed files and to the round-45 freeze manifest).

## 4. Falsifier 1 — reachable false green: the predicate cannot see *which cell* carries the pin

The needle check is a whole-row substring search; it never attributes a needle to the receipt cell. A row whose **self-test receipt cell does NOT match the measured pin** still turns green if the literal needle bytes exist anywhere else on the same line.

Replay (scratch copy, no repo file touched):

1. Copy current `SKILL.md` to `/tmp/false-green-skill.md`.
2. In row 190 (`r45 ledger counter (C1)`) replace the receipt cell `→ measured \`C1_SELFTEST pass=16 fail=0\`` with `→ measured \`C1_SELFTEST pass=17 fail=0\`` (now stale, does not match the measured pin), and append the literal needle text as an annotation at the end of the same table line: `<needle-attested: C1_SELFTEST pass=16 fail=0>`.
3. `python3 .ufo/waves/round-46/count-repins.py /tmp/false-green-skill.md` → **`MORI_R45_REPINS mismatches=0 rows=4` rc 0**.

Result: the row's receipt cell is stale (`pass=17`), so the row does **not** match the measured pin (`pass=16`), yet the predicate reports green. The claim's biconditional "green ⇒ four rows match measured pins" is therefore false in a reachable state. The predicate establishes *"the needle literal occurs somewhere in each target row"*, not *"the receipt cells carry the measured pins"*.

## 5. Falsifier 2 — receipt label `rows=4` is a hard-coded constant, not a measurement

`rows=` always prints `len(ROWS)` = 4 regardless of input. Replay: feed the predicate a file with **none** of the four target rows:
`MORI_R45_REPINS mismatches=4 rows=4` (rc 1). The `rows=4` token is identical in the red and green receipts; it carries no information about how many SKILL.md rows matched. The claim's phrasing ("reports mismatches=0 rows=4 only when four specific … rows match") invites reading `rows=4` as an observed count of matched rows; it is a constant label. The only informative signal is `mismatches`.

## 6. Impacted axes

- **Green-verdict sufficiency (truth axis):** green does not imply the four rows match the measured pins in the receipt-cell sense (Falsifier 1). Necessary-and-sufficient claim overclaims on the sufficient side.
- **Receipt labeling (reporting axis):** `rows=4` constant is misleading (Falsifier 2).
- **Not impacted / confirmed sound:** control redness (do-nothing control stays red, rc 1); needle↔receipt-label equality for all three selftest tallies; digest pins' provenance against committed files and the freeze manifest; duplicate-row detection (`expected one row, found 2` → red, verified by sibling MutDuplicate and here by code reading: `len(matches)!=1` → error); missing-row detection (`found 0` → red).

## 7. Smallest safe correction

1. **Anchor each needle to its semantic cell:** parse the table row into cells (`split("|")`) and require each needle inside the cell where the pin legitimately belongs (selftest-tally receipt in the self-test cell; digest/line-count receipt in the self-test or pinned-values cell). This preserves every current green/red outcome (the control lacks the pins in those cells, so it stays red) while excluding relocate-the-needle false greens.
2. Optionally drop or rename `rows=` in the receipt (it is constant; `targets=4` would be honest), or, if `rows=` is meant to be measured, actually count matched rows and print that count.

Reproduction commands are inline in §3–§5; all runs were on scratch copies or the frozen instrument, none modified repo files.
