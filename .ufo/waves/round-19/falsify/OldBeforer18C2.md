# r18-C2 before-state rederivation

## Finding

No actionable defect in the scoped row. Expected `r18-C2` result at the retained before state: **verdict `no-implementation`; effective label `pre-build`; overclaim `true`**. The retained receipt reports that tuple (`.ufo/waves/round-18/evidence/c2-before.json:1`). The frozen rule assigns `no-implementation` when no implementation-path commit occurs and defines a pre-build label as an overclaim for every verdict other than `pre-build` (`.ufo/waves/round-18/frozen/c2-register.json:6-14,34-37`). The delivered checker follows that rule: it emits `no-implementation` when no implementation commit was found and computes the overclaim from the effective label and verdict (`tools/mori-freeze-order.py:284-305,314-317`).

## Historical / prospective attribution

**Preserved per claim, not as a separate aggregate field.** The correction register contains only the `r17-C3` correction (`corpus/evidence/freeze-register.json:4-11`); the checker applies corrections by claim ID and otherwise retains each row's declared label (`tools/mori-freeze-order.py:322-328`). Thus `r18-C2` remains `pre-build` and is still `overclaim=true` at the before state. The before receipt's four overclaims comprise the one historical `r17-C3` overclaim plus the three prospective `r18-C1..C3` rows; the `r18-C2` flag is not evidence of a fourth historical defect. This matches the frozen round-19 expectation that missing implementations are not counted as historical defects (`.ufo/waves/round-19/frozen/expected.json:22-36`). A reader using only the aggregate overclaim total would lose that distinction; preserve the row IDs and correction target when describing the count.

## Verification gaps

No checker execution or tests were run; this was a static rederivation from retained sanitized artifacts and source. The LSP device was unavailable (`read xd://lsp` returned “No such tool”), so no status, references, definition, or diagnostics were obtained. Literal search was used only for path discovery, not as semantic evidence. No old unredacted source was read.