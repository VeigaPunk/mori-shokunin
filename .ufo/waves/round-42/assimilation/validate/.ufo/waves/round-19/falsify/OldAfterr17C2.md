# r17-C2 after-state review

## Findings

No actionable finding in the assigned row. Expected after-state is verdict `co-evolved`, effective label `unlabeled`, and overclaim `false`; the retained after receipt records those values (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-18/evidence/c2-after.json:1`).

## Derivation and attribution

The frozen row declares `r17-C2` as `unlabeled`, names `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round17-jj-regressions.py` as its frozen path and `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh` as its implementation path, and records an outside ruling of `co-evolved` (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-18/frozen/c2-register.json:20-23`). Applying the frozen ordering rule (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-18/frozen/c2-register.json:4-13`) to the ordered commit range gives an implementation touch before the last frozen-path touch, so the expected verdict is `co-evolved`; at least one commit also touches both paths. The delivered checker tracks the first implementation and last frozen-path indices and returns `co-evolved` when the frozen touch is not strictly before implementation (`/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-freeze-order.py:278-305`).

The append-only correction register contains only the `r17-C3` correction, not an `r17-C2` correction (`/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/freeze-register.json:4-12`). The checker therefore falls back to this row's declared label (`/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-freeze-order.py:322-327`); its overclaim predicate requires effective label `pre-build` and a non-`pre-build` verdict (`/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-freeze-order.py:314-317`). `unlabeled` consequently yields `false`, and the co-evolved outside ruling does not disagree with the verdict. The row is neither the one historical correction nor one of the three prospective labels: the refinement attributes the historical correction to `r17-C3` and the prospective labels to the three `r18` claims (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-19/frozen/provenance-refinement.json:8-12`), matching the stated C2 split (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-19/contract.md:7`). Attribution is preserved for this row.

## Residual risk and verification gaps

Scope is only `r17-C2`; this is not a review of the other five claims. No checker, tests, smoke, or verification command was run. The `lsp` device was unavailable (`xd://lsp` reported no such tool), so semantic LSP checks could not be made; source inspection and read-only Git history were used instead.