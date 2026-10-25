# RevContract — frozen-contract review

## Findings

- **High — C2 before-state is contradicted by the cited frozen receipt.** Contract §C2 says entering revision `2d85e33` failed `entry_absent,pins,source_row` (contract.md:67), but the receipt `.ufo/waves/round-47/evidence/control-c2-donothing-at-freeze.txt:1-3` actually scores freeze commit `63eecf2738db96f46b0bd02b1b2dfd66787493d0` and reports `failed=entry_absent,source_row` (no `pins`). This misstates the control's measured before/failure set; correct the claim evidence or distinguish entering revision from freeze revision. The control is still unmet, but its exact evidence differs.

- **Medium — C1 before-state is likewise not keyed to its stated revision.** Contract §C1 says “Before (entering `2d85e33`)” then cites `evidence/control-c1-donothing.txt`; that receipt's command does run the entering revision and reports the mismatch, so this is consistent. It also reports `tally_pins=26`, `digest_pins=5`, and the single mismatch at line 912 (receipt lines 1, 32-34), consistent with the stated calibration defect.

## Checks

- Frozen predicate P-C2: compared contract.md:56-63 with count-c2.py docstring lines 4-15. Sentence is identical in substantive wording/line-wrapped form.
- Freeze ordering control: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --format=%H -1 -- .ufo/waves/round-47/contract.md` → `63eecf2738db96f46b0bd02b1b2dfd66787493d0`, matching the required freeze commit.
- Before/after values, controls, kill rules, and named limits are declared for both claims in contract.md: C1 lines 33-46; C2 lines 67-78. C1 and C2 each have an unmet do-nothing control; the frozen C2 do-nothing receipt is unmet. C1 limits are explicit (line-count/truncated digests, digest scope, command determinism); C2 limits are explicit (no prose/lifecycle/host-kernel validation).
- C2 predicate wording is defined once in the contract and reproduced in the counter docstring. No tool installations.

## Residual risk / verification gaps

I reviewed the frozen contract and its named receipts only; I did not independently execute either counter or inspect every other control receipt. The C2 receipt named above is demonstrably at the freeze revision, not the entering revision, so the reported entering `pins` failure is unsupported by that receipt.