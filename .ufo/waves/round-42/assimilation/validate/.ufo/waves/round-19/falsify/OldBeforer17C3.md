# C2 row review: r17-C3 at the before state

## Axis

C2 calibration — historical label correction versus prospective r18 labels.

## Finding — before evidence mixes historical and prospective overclaims

The retained before row is **verdict `co-evolved`, effective label `pre-build`, overclaim `true`** (`.ufo/waves/round-18/evidence/c2-before.json:1`). That is the expected historical result: the frozen register declares `pre-build` and records the co-evolved outside ruling (`.ufo/waves/round-18/frozen/c2-register.json:24-29`); the correction register was not present in the contract's before revision d005cdde0e009dea6c0cc29b37163de536528658 (read-only `git cat-file -e` check), so it must not be applied retroactively to this before snapshot.

At the later corrected state, the expected row keeps verdict `co-evolved` but has effective label `co-evolved` and overclaim `false`: the append-only correction targets r17-C3 (`corpus/evidence/freeze-register.json:4-11`), and the checker selects that correction over the declaration (`tools/mori-freeze-order.py:203-233,323-329`) before applying its overclaim predicate (`tools/mori-freeze-order.py:311-318`). Its revision-bound input check also rejects a correction file absent from the measured revision (`tools/mori-freeze-order.py:125-151,376-382`), preserving the pre-correction historical result.

Row-level attribution is preserved: this is the single historical correction; it does not relabel r18-C1..C3, which are the three prospective claims. However, the retained before JSON totals four overclaims, while the round-18 contract states a historical before count of one (`.ufo/waves/round-18/contract.md:31-36`). The extra three are the prospective r18 rows marked `no-implementation` in that before snapshot, so the aggregate must not be presented as four historical defects; the distinction survives only when counted by row identity.

## Residual risk and verification gaps

The before artifact has no provenance/command metadata, so its exact invocation cannot be established from that JSON. No checker execution or tests were run. The LSP device is unavailable in this environment; checker references above use the required literal source-reading fallback, not semantic LSP results.