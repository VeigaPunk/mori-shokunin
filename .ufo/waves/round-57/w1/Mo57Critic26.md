# Mo57Critic26 — C1 counter attack

## Counterexample, evidence, verdict

No qualifying junk-row fixture found against the frozen C1 predicate. The assigned target is explicitly the two rows in the **current SCORECARD capabilities table** (`.ufo/waves/round-57/contract.md:5`), not tool behavior. The counter at `.ufo/waves/round-57/count-c1.py:7-13` reads `SCORECARD.md` at revision R; between `## Capabilities` and `## Saturation` it accepts exactly two lines containing the two names, each containing `.ufo/waves/round-56/` and `| 56 |`. Consequently, a no-op probe or bogus selftest is irrelevant to this claim: the counter does not execute the probe or test its behavior. A fixture containing only an inert tool and junk rows is rejected (`C1=unmet rows=0 evidence=bad`, exit 1) if it does not satisfy those SCORECARD row conditions.

The strongest plausible false-green is an arbitrarily described pair of capability rows with fabricated-but-shaped evidence paths. However, those are still two rows naming the capabilities, with a round-56 path and first-working value 56; the frozen predicate says “resolvable round-56 evidence pointer,” whereas the counter only performs substring checks and does not resolve the path. That is a counter enforcement gap, not a do-nothing/junk-row construction that fails the target: a purported junk row with a dangling pointer does not provide the required resolvable pointer. Treat any C1=met result on such rows as insufficient evidence for the full contract, not as proof the target was attained.

Evidence: contract `.ufo/waves/round-57/contract.md:5`; counter `.ufo/waves/round-57/count-c1.py:7-13`; SCORECARD round-56 claim-table rows are at `SCORECARD.md:2901-2904`, not capabilities rows. A scratch repo was initialized and its top-level asserted before fixture commit; the no-op test did not pass the counter, and the scratch contents were removed. No production files or frozen predicate/counter changed.

## Axes / smallest safe correction

Impacted axis: calibration (C1). Counter falsifier: none found. Residual correctness concern: frozen counter does not establish pointer resolution, so closure should manually resolve both cited round-56 evidence paths at R; do not broaden or alter the frozen counter. No correction to the exact predicate is indicated by this attempted do-nothing attack.

Report: .ufo/waves/round-57/w1/Mo57Critic26.md