# C2 after-state rederivation: r17-C1

**Result:** expected verdict `co-evolved`; effective label `unlabeled`; overclaim `false`. This agrees with the retained after-state row.

The frozen register's rule selects the latest correction for a claim, otherwise its declared label. The corrections register has no r17-C1 correction, so its label remains `unlabeled`. The delivered checker marks an overclaim only for an effective `pre-build` label whose verdict is not `pre-build`; r17-C1 therefore contributes no overclaim. Its verdict also agrees with the frozen outside ruling.

**Attribution preserved:** yes. The sole historical correction remains r17-C3; the three prospective labels remain the r18-C1/C2/C3 claims. r17-C1 does not add a historical defect or shift the historical-1/prospective-3 split.

The integrated checker diff adds input-revision binding and provenance metadata; the verdict decision tree and overclaim predicate remain unchanged. No actionable mismatch found in this assigned row.

**Verification gap:** static reading only; no execution was performed. An LSP device was unavailable (`xd://lsp` reported no such tool; mounted devices were `ast_edit` and `debug`).

**Evidence (path:line — class):**
- `.ufo/waves/round-18/evidence/c2-after.json:1` — retained after-state row.
- `.ufo/waves/round-18/frozen/c2-register.json:13-19` — label rule and r17-C1 declaration/ruling.
- `corpus/evidence/freeze-register.json:4-13` — append-only correction scope.
- `tools/mori-freeze-order.py:203-233,249-319,322-328` — correction selection, verdict and overclaim logic.
- `.ufo/waves/round-18/frozen/c2-register.json:30-41` — prospective r18 claim set.
- `.ufo/waves/round-19/frozen/provenance-refinement.json:8-12` — historical/prospective attribution.