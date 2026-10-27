# Mo58Reviewer17 — C1 MANIFEST binding

**Finding — C1 counter false-greens when capability keys/names do not bind to the two MANIFEST entries.** At freeze `fe8801120a67c1a6b8899d7d0423839caa09e7d0`, `count-c1.py` reports the real SCORECARD rows as `C1=met rows=2 pointers=ok manifest=ok binding=ok`; its selftest reports `pass=4 fail=0`. The pinned SCORECARD rows at lines 1989–1990 identify row 0 as “dual-shape seat-output vote binding” and row 1 as “strict per-event driver-liveness probe.” Fleet `MANIFEST.json` `rounds[832].capabilities_added[0..1]` contain corresponding longer descriptions.

The counter does not join the SCORECARD row keys/names to the MANIFEST entries. In `measure()`, row selection uses `any(k in ln for k in R56_KEYS)` and then only checks `len(rows) == 2`; MANIFEST checking independently tests hardcoded substring hints in `caps[idx]`. Thus it never requires one row for each key, compares a row name with `caps[j]`, or requires the key to occur in the key cell. The MANIFEST check also accepts any altered description retaining the hardcoded hint.

**Bounded adversarial method / observed results:** using the frozen counter code, I made isolated throwaway git fixtures from the freeze SCORECARD and the counter’s four existing pointer targets; each fixture was asserted to have itself as `git rev-parse --show-toplevel`. The baseline and each mutant below returned exit 0 with `C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none`:

- duplicate key: both rows carry `rounds[832].capabilities_added[0]` (key `[1]` absent);
- swapped keys: the driver-liveness row has key `[0]` and vote-binding row key `[1]`;
- unrelated replacement names in both SCORECARD capability cells;
- both MANIFEST descriptions replaced by unrelated text that merely retains `vote binding` / `driver-liveness`;
- first row keyed `[0]`, second row keyed `[999]`, with key `[1]` only mentioned in its prose.

This demonstrates false-green variants against the claimed verification of the two admitted capabilities and their exact keys; it is not a finding that the actual frozen rows are inconsistent. The existing wrong-key selftest only tests a nonmatching `[999]` row without a key mention elsewhere, so it does not cover these constructions. I did not modify production/corpus/registry files or run any checks beyond the baseline/selftest and bounded fixture probes.
