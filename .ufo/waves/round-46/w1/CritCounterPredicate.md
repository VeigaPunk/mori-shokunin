# CritCounterPredicate — falsification findings

## Counterexample

A malformed second table row can collide with the final predicate key and still return green. `ROWS` contains both `r44 gate registry (C2)` and `r44 gate registry (C2) — write scope superseded` (counter lines 10, 17). The matcher for the former is `line.startswith("| " + row + " |")` (line 29), so the latter does not collide with it because ` —` precedes the required ` |`. But construct the superseded row with a cell separator immediately after the shorter name, e.g. `| r44 gate registry (C2) | — write scope superseded | GATE_REGISTRY_SELFTEST pass=15 fail=0 |`. This line matches the shorter key and can serve as its only match; it can also be the superseded key's only match only if its exact longer key is present, so a *single* line cannot satisfy both. More significant: the current counter itself does not verify that the labels are in the intended table/section or that matching rows are actual table rows beyond this prefix.

The strongest concrete defect is the tautological duplicate-key check vulnerability: Python dict keys collapse if identical, but the two present keys are not identical. No current row-name collision between the declared keys was established. I therefore found no demonstrated false-green collision among these four literal keys.

## Evidence / behavior

- `.ufo/waves/round-46/count-repins.py:9-20` defines exactly four dictionary keys; the two r44 labels differ by the ` — write scope superseded` suffix. `len(ROWS)` therefore prints 4; exact duplicate declarations would be silently overwritten by Python dict semantics, making `rows=4` reflect unique keys rather than source declarations.
- Lines 28-35 count matching lines for each key; duplicates of a recognized prefix fail with `expected one row, found N`, and a missing recognized row fails with `found 0`. Reports `MutMissing.md` and `MutDuplicate.md` record reproducible probes of those cases.
- Matching is line-prefix plus substring containment, not parsed table structure or typed value validation. A malformed value containing each expected needle as substrings can satisfy its key. For example, a row cell may append contradictory text after an exact expected tally/hash (`pass=16 fail=0 ... pass=16 fail=1`) and still contain the expected needle. No malformed-value mutation run was available in the checked reports, so this is a code-derived counterexample, not an observed command result.
- Staleness is tested only against hard-coded needles; this counter does not measure referenced files or derive fresh pins. `ExecFreeze.md` explicitly notes it does not read the freeze manifest, and `ScoutDigests.md` reports the measured hashes separately. Thus the predicate can remain green after a referenced artifact changes unless the corresponding SKILL row is independently re-pinned/checked.
- The committed control is evidenced red (`mismatches=4 rows=4`, exit 1) in `ExecCounter.md`; current green and duplicate/missing mutation outcomes are recorded there and in mutation reports. I did not rerun them.

## Impacted axes

- **Predicate soundness / identity:** exact literal key matching prevents ordinary duplicates, but there is no table/schema context and Python dictionary construction would hide an accidentally duplicated key declaration while the summary still says `rows=4`.
- **Value integrity:** expected-string containment accepts rows that include the expected value plus contradictory extra content; malformed or internally inconsistent pin cells are not rejected.
- **Freshness/provenance:** green means the four text rows contain needles, not that all artifact pins remain current; broader freeze-manifest state is outside the counter.
- **Control discrimination:** observed do-nothing control remains red; this does not establish robustness to the above malformed/stale cases.

## Smallest safe correction

Keep the frozen predicate unchanged for this round. For a future instrument revision, declare rows as an ordered tuple/list and assert its keys are unique before counting; parse and validate the exact target cells (or canonical full row values) rather than substring-presence; scope matching to the intended table and require exact uniqueness there. If freshness is part of the intended claim, compare the pinned values to the measured artifact/manifest values instead of treating textual presence as measurement.

## Report

Report: `.ufo/waves/round-46/w1/CritCounterPredicate.md`
