# MutRoutedTreePin — wave 2 falsify: C1 R1/R3 whole-tree-pin mutant

Date: 2026-10-22. Seat: MoriR24.MutRoutedTreePin (mutation tester, leaf; no subagent dispatch).
Lane: /home/vgpnk/Projects/shokunin/mori-shokunin. Measured lane tip: `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc`.
Scratch: /fast/scratch/hyaku/mori-r24-a2/w2/MutRoutedTreePin/ (clone + outputs).

## Assignment

Attack C1 `tools/mori-routed-check.py` with the mutant "R1/R3 round-23 tree pin replaced by the
two-blob check"; find a real tamper (e.g. a new file under `.ufo/waves/round-23/evidence`) that
now passes. Run unmutated and mutated tool at relevant revisions and on committed tamper commits
in the scratch clone.

## 1. Mutant applied (smallest behavior-bearing point)

The whole-round-23-tree pin (amendment A4 guard) exists twice: `ROUND23_TREE_PATH` comparison in
`_check_r1` (lines 363-371) and in `_check_r3` (lines 445-453). Mutant removes both blocks and
the `"round23_tree"` detail keys, leaving exactly the pre-A4 predicates:
R1 = frozen-tree pin + quota absence + historical-case scan; R3 = two-blob check
(`R3_BLOB_PATHS`) + rejected-tree pin. This matches "tree pin replaced by the two-blob check".

- Pristine tool sha256: `64921a0c30aed1d9a2a7a03c377825add37ebecd7aded8fbfe8f30c02dafbd14` (== committed blob `a730ecf:tools/mori-routed-check.py`).
- Mutated tool sha256: `73f69cdb5f82b724b4917556007eba43de220bbe53f2fa84ef4d9e363678af8e` (working-tree only, never committed).
- `git diff` vs pristine (12 lines removed in R1, 11 in R3): `_check_r1` loses `base_tree/rev_tree` computation, `detail["round23_tree"]`, and the `round23_tree_unreadable/not_a_tree/changed` reasons; `_check_r3` identical. `python3 -m py_compile` passes.

## 2. Baseline (unmutated tool, pristine clone)

| --rev | --round | exit | held | R1/R2/R3/R4 |
|---|---|---|---|---|---|
| a730ecf (tip) | 24 | 0 | 4 | all held ([] reasons) |
| c725aa37 (base) | 23 | 1 | 3 | R4 RED (attempt_ledger_not_clean, ledger_finding:AT_INVALID/LEGACY_ROW_UNBOUND/STARTED_MISSING, dispatch_path_missing x8, dispatch_committed_after_dispatch x8) |

Round-23 tree OID at base and tip both `3e5b2c9d36485558ae79862daa9d0ca9a9e04426` — the whole-tree pin is what keeps R1/R3 green at the tip.

## 3. Committed tamper commits (scratch clone only, never pushed)

| tag | commit | tamper |
|---|---|---|
| T_NEWFILE | `4b75a33f624d035e9877f67da0a75eb40be5d6d1` | add `.ufo/waves/round-23/evidence/quota-evidence-fake.json` (quota-capability claim, 44 lines) — changes round-23 tree OID to `968e132d099e81b397868d1f74ef2978b037e2f6` |
| T_BLOBEDIT | `79529644cc0cf7e384b753e7207a4aeeaabab23b` | one-byte append to `.ufo/waves/round-23/evidence/harness-receipt-overwrite.json` (the R3 two-blob check target) |
| T_FROZEN | `ba75ef50f6f5ff8518bdc22c7957c2699eb3c8d4` | one-byte append to `.ufo/waves/round-23/frozen/c1-requirements.json` (the R1 frozen-tree pin target) |

All three change only `.ufo/waves/round-23/**`; R2 scan scope (SCORECARD/PROVINCE/SKILL/LOG/README/corpus) and round-24 R4 inputs are untouched.

## 4. Results

### Unmutated tool (pristine bytes; T_NEWFILE run repeated with the pristine copy to avoid worktree ambiguity)

| --rev | exit | held | R1 | R2 | R3 | R4 |
|---|---|---|---|---|---|---|
| T_NEWFILE | **1** | **2** | RED round23_tree_changed | held | RED round23_tree_changed | held |
| T_BLOBEDIT | 1 | 2 | RED round23_tree_changed | held | RED round23_tree_changed, capture_evidence_changed | held |
| T_FROZEN | 1 | 2 | RED round23_tree_changed, frozen_tree_changed | held | RED round23_tree_changed | held |

The pristine tool kills all three tarpers. T_NEWFILE is exactly the tamper class the target mutant loses.

### Mutated tool

| --rev | exit | held | R1 | R2 | R3 | R4 |
|---|---|---|---|---|---|---|
| a730ecf (control) | 0 | 4 | held | held | held | held |
| **T_NEWFILE** | **0** | **4** | **held ([] reasons)** | held | **held ([] reasons)** | held |
| T_BLOBEDIT | 1 | 3 | held | held | RED capture_evidence_changed | held |
| T_FROZEN | 1 | 3 | RED frozen_tree_changed | held | held | held |
| c725aa37 (base, round 23) | 1 | 3 | held | held | held | RED (same as baseline) |

## 5. Verdict

**MUTANT SURVIVES** (coverage finding, not a contract change).

- The real tamper T_NEWFILE — a new file under `.ufo/waves/round-23/evidence/` faking quota-capability evidence — passes the mutated tool: `held: 4`, exit 0, R1 and R3 held with no reasons. The pristine tool kills it (`held: 2`, exit 1, `round23_tree_changed` on both R1 and R3).
- The mutant is NOT killed by an existing control: wave-1 BuildRoutedCheck's mutant M3b ("add a file under `.ufo/waves/round-23/`" → R3 RED `round23_tree_changed`) is the same tamper class, and it was measured only against the pristine tool; replayed against the mutant it passes. There is no existing test asserting the whole-tree invariant beyond the pinned subtrees (frozen, rejected) and pinned blobs (R2 retention + R3 harness/tmpfs).
- The mutant is not vacuous: it still detects blob edits (T_BLOBEDIT → R3 RED `capture_evidence_changed`, the retained two-blob check) and frozen-tree edits (T_FROZEN → R1 RED `frozen_tree_changed`). The lost coverage is precisely: any change under `.ufo/waves/round-23/` outside `frozen/`, `rejected/` and the pinned blob paths — new/renamed/moved files anywhere else in the round-23 tree (evidence/, build/, cases-*, falsify/, top-level files, contract.md edits).
- R4 and the base before-value are unaffected by the mutation (c725aa37 round 23 still `held: 3`, same R4 reasons).

## 6. Restoration evidence

- `tools/mori-routed-check.py` restored to committed bytes: sha256 `64921a0c30aed1d9a2a7a03c377825add37ebecd7aded8fbfe8f30c02dafbd14` (matches `a730ecf:tools/mori-routed-check.py`).
- Clone worktree clean: `git status --porcelain` empty after restoring a stray deleted committed `__pycache__` file (accidental `find -exec rm` during cleanup; restored via `git checkout --` in the scratch clone only) and removing untracked `tools/__pycache__/`.
- Tamper commits live only on local scratch branches `tamper/newfile`, `tamper/blobedit`, `tamper/frozen`; nothing pushed; clone remote unchanged.
- Lane repo untouched: no git/jj mutation; only this report was created in the lane.

## 7. Tooling

No installs or upgrades (git 2.56.0, Python 3.14.8 pre-existing; pacman transactions paused host-wide; nothing needed). Commands used: `git clone --no-hardlinks`, `git checkout/switch -c`, `git add/commit -q` (scratch only), `python3 -I tools/mori-routed-check.py --repo <clone> --rev <rev> --round N`, `python3 -m py_compile`, `sha256sum`, `git diff -u`, `git rev-parse`, `git ls-tree`.
