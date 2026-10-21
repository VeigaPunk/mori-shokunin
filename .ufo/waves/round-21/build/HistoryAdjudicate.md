# Round-20 wave adjudication: acceptance blocker

## Finding

- **Acceptance blocker:** Keep the r10 baseline unchanged and do not re-pin while the disappeared `aggregator-r10` and `aggregator-r10-resume` evidence is unresolved. The prior adjudication classifies this as `census-regression`, the pin-blocking class; a fleet change explaining marker disappearance does not establish settlement. Its cited frozen-contract gate says only `census-regression` blocks re-pin, while the contract does not define the class semantics. (`.ufo/waves/round-20/falsify/AdjudicateWaves.md:5,15,29`.)
- **Independent disposition required to clear it:** A **non-author record must account for each removed wave**, showing either explicit settlement or an evidenced cleanup disposition. The finding is per wave, not a general explanation for the fleet sweep. A `blind_spot` note alone does not meet the pin gate. (`.ufo/waves/round-20/falsify/AdjudicateWaves.md:7,29`.) A historical cleanup by the same identity does not establish independent settlement (round-21 assignment context).
- **Do not conflate:** The newly aged `shokunin-train-20261016-w24` observation is separately classified `live-state`; it does not resolve the old-wave evidence loss. Re-pinning would suppress the change from later drift comparisons, not clear current census warnings. (`.ufo/waves/round-20/falsify/AdjudicateWaves.md:7,11,29`.)

## Observed / unresolved

The report identifies both aggregator waves as r10 baseline warning rows whose marker files disappeared, and cites the round-12 receipt as explicitly saying that missing markers do not prove settlement. It states that the census can count a directory as empty without the relevant markers. The actual settlement state of the removed waves remains unknown; available evidence establishes neither that they remain unsettled nor that census can currently observe them. (`.ufo/waves/round-20/falsify/AdjudicateWaves.md:7,11,16-18`.)

**Confidence:** High that the stated acceptance gate is blocked and requires per-wave non-author disposition; actual settlement remains unresolved.

**Actions taken:** Read the prior falsification report and wrote this finding only. No census, pin/drift command, or source edit was performed.