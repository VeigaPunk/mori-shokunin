# r17-C1 before-state rederivation

## Finding
No actionable discrepancy in the assigned row.

- **Expected verdict:** `co-evolved`. The retained before-state row records this verdict; the frozen claim's outside ruling agrees. The delivered checker selects `co-evolved` when the last frozen-path change is not strictly before the first implementation change (`.ufo/waves/round-18/evidence/c2-before.json:1`; `.ufo/waves/round-18/frozen/c2-register.json:16-19`; `tools/mori-freeze-order.py:295-305`).
- **Effective label:** `unlabeled`. That is r17-C1's frozen declaration, and the corrections register has no r17-C1 correction; its sole row corrects r17-C3. The checker falls back to the declaration when there is no correction for that claim (`.ufo/waves/round-18/frozen/c2-register.json:16-19`; `corpus/evidence/freeze-register.json:4-12`; `tools/mori-freeze-order.py:322-327`).
- **Overclaim:** `false`. The checker only marks a row overclaimed when its effective label is `pre-build` and its verdict is not `pre-build`; r17-C1's effective label is `unlabeled` (`tools/mori-freeze-order.py:314-317`). This matches the retained before-state row (`.ufo/waves/round-18/evidence/c2-before.json:1`).
- **Attribution:** preserved. The correction register has one historical correction, for r17-C3; the frozen register separately declares the three r18-C1/C2/C3 rows `pre-build`. This retains the contract's one-historical-correction versus three-prospective-label distinction, not four historical defects (`corpus/evidence/freeze-register.json:4-12`; `.ufo/waves/round-18/frozen/c2-register.json:30-41`; `.ufo/waves/round-19/contract.md:7`). r17-C1 is neither the corrected historical overclaim nor one of those three prospective labels.

## Residual risk and verification gaps
This is a static rederivation limited to r17-C1; no checker execution or tests were run, as required. An LSP device/status interface is not exposed in the available tool inventory, so no LSP references/definition/diagnostics checks were available. No conclusion is made about the other five rows.