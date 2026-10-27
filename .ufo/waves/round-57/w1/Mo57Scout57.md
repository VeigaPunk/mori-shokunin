# Mo57Scout57 — round-56 capability-table defect

## Evidence and verdict

- Frozen C1 is specifically a test that the **current SCORECARD capabilities table** has rows named `driver-liveness` and `vote-binding`, each with a resolving round-56 evidence pointer and first-working round 56 (`.ufo/waves/round-57/contract.md:5`). This is not merely a test that the demonstrations exist.
- The current register is the canonical `## Capabilities` described at `SCORECARD.md:1951-1961`: it represents capabilities admitted by non-author closure, keyed to closure additions; rows enter only through a demonstrated capability admitted by closure. It explicitly supersedes the initial none-yet table and per-round tables.
- That register does not show either round-56 capability. The only rows with those names occur in the round-56 claim narrative, not the canonical table: `SCORECARD.md:2897-2905` records the C1 driver-liveness probe and C2 vote binder as claims, and shows their counters met at freeze/landed. The round-56 lesson also records them as claims and names their evidence artifacts (`corpus/lessons/round-56.md:7-9,31-33`).
- The historical table at `SCORECARD.md:596-602` is explicitly an initial snapshot; later text says it is superseded (`SCORECARD.md:1957-1961`). Adding rows there would not satisfy a predicate about the current register.

**Verdict:** C1's suspected defect is an admission/register gap, not absence of round-56 demonstration evidence. The round-56 claim counters establish their frozen technical predicates, but do not by themselves establish non-author closure/admission into the canonical capability register. The counterexample to “the demonstrations imply rows” is the present canonical register: round-56 claims/evidence are recorded, while those names are absent there.

## Falsifiable correction recommendation

Do not manually insert two capability rows solely to satisfy C1. First obtain/locate a non-author closure that admits both named capabilities (or establish that the relevant closure already does so), then add the corresponding canonical register rows with evidence pointers resolving in the lane repo and first-working round `56`. Falsify the correction by checking the canonical table at the candidate revision: both names must occur exactly as rows, each pointer must resolve, and each first-working cell must equal 56; a narrative-only mention or the obsolete initial table is a failing counterexample. The frozen counter `python3 .ufo/waves/round-57/count-c1.py R` is the contract's direct predicate check (`contract.md:5`); do not alter its predicate.

## Limits

I did not run LSP: the assignment is source-evidence scouting, and no LSP device was exposed in the available tools. I did not run the counter or inspect closure artifacts, so whether a qualifying non-author closure already exists remains unresolved. The cited SCORECARD and lesson lines are observed text; the admission-gate interpretation follows the SCORECARD's stated register rules.