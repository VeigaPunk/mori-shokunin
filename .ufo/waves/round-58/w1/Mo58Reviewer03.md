# Mo58Reviewer03 — C1 MANIFEST binding

**Finding — High: C1 accepts altered capability names and does not bind each key to its corresponding MANIFEST entry.** The frozen counter's `measure()` selects rows by presence of either literal key, checks only `len(rows) == 2`, and independently tests hardcoded `MANIFEST_HINTS = {0: "vote binding", 1: "driver-liveness"}` against `MANIFEST.json` `rounds[832].capabilities_added[idx]`. It never compares a SCORECARD capability name with a MANIFEST capability name, nor validates one distinct row per key. It also opens fleet `MANIFEST.json` from the live filesystem rather than revision-pinned bytes.

**Evidence.** At freeze revision `fe8801120a67c1a6b8899d7d0423839caa09e7d0`, SCORECARD rows 1989–1990 are respectively `dual-shape seat-output vote binding` (key `[0]`) and `strict per-event driver-liveness probe` (key `[1]`). The current fleet `MANIFEST.json` `rounds[832]` identifies round 56 / lane `mori`; its two `capabilities_added` values begin with those same names. Frozen counter SHA-256 and working-tree counter SHA-256 both equal `6ecdb627bb55522c258dc484ed5c530cfd6f7c57c6a89b4c38179df4c0f84e4b`; the counter at the freeze revision returned `C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none` (rc 0).

**Bounded adversarial method/results.** Copied the frozen counter unchanged into explicit scratch fixture lanes, verified counter SHA, and used `git -C <fixture-lane>` for each throwaway repo. Fixture counter cases, each with existing evidence paths and ≥10 register-key rows:

- Replaced both SCORECARD capability names with unrelated strings while retaining keys and valid pointers: **met**, rc 0.
- Replaced MANIFEST capability values with unrelated/superseded descriptions retaining only the hardcoded hint substrings: **met**, rc 0.
- Put a foreign identity (`round: 999`, `lane: foreign-lane`) at `rounds[832]`, with values `vote binding` / `driver-liveness`: **met**, rc 0.
- Put both keys on one row and duplicated key `[0]` on the second row: **met**, rc 0.
- Negative control, replacing key `[0]` with `[999]`: **unmet rows=1 failed=rows**, rc 1.
- Same lane tree hash and same revision in two fixture fleets; changing only live MANIFEST values from hint-containing to `entry one` / `entry two` flipped **met** to **unmet** (`failed=manifest`).

All eight fixture cases matched expected outcomes (0 surprises). Scratch fixtures and driver are under `/fast/scratch/hyaku/mori-r58/Mo58Reviewer03/`; cleanup performed before yielding.

**Residual risk / verification gaps.** This demonstrates counter acceptance behavior, not an actual fleet mutation. Freeze-time MANIFEST bytes were not available as a revision-pinned input in the counter; the observed live MANIFEST identity and values above are the comparison basis. The correct-name baseline and wrong-key negative control passed.