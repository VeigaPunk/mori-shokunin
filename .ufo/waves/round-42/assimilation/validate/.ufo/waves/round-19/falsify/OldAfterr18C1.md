# Scoped C2 rederivation: r18-C1 after

## Finding

No actionable row-level mismatch. The expected after-state for `r18-C1` is **verdict `pre-build`, effective label `pre-build`, overclaim `false`**, matching the retained after receipt (`.ufo/waves/round-18/evidence/c2-after.json:1`). The frozen register declares this claim `pre-build` (`.ufo/waves/round-18/frozen/c2-register.json:30-33`). The append-only corrections register changes only `r17-C3` to `co-evolved`; it contains no correction for `r18-C1` (`corpus/evidence/freeze-register.json:4-11`). The delivered checker maps corrections by claim ID and otherwise uses the declared label (`tools/mori-freeze-order.py:203-233,323-329`); its overclaim rule is a `pre-build` effective label paired with any verdict other than `pre-build` (`tools/mori-freeze-order.py:311-318`). Thus the retained `pre-build` verdict and label produce no overclaim for this row.

**Historical1 versus prospective3 attribution is preserved for this row.** `r18-C1` remains one of the three prospective r18 pre-build labels, not a historical defect correction. The sole historical correction is the r17-C3 relabel; the r18 closure states the three r18 labels were prospective (`corpus/lessons/round-18-verifier-spotcheck.md:84-94`), and the refinement records the same one-plus-three split (`.ufo/waves/round-19/frozen/provenance-refinement.json:8-12`).

## Residual risk and verification gaps

The retained r18 after receipt has no measured-revision, tip, input-digest, or command provenance; the r18 closure explicitly records that limitation (`corpus/lessons/round-18-verifier-spotcheck.md:90-94,177-179`). The delivered checker contains provenance-bound input loading and receipt metadata (`tools/mori-freeze-order.py:362-405`), but it was not invoked here. The LSP device is unavailable in this environment (`xd://lsp` is not mounted); this is a static rederivation from the listed retained artifacts and checker source, not a replay. No tests, builds, lint, or verification runs were performed.

Report: .ufo/waves/round-19/falsify/OldAfterr18C1.md
