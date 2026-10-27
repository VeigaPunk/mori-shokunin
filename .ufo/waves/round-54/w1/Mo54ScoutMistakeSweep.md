# Round-54 mistake sweep — frontier

Scope: verifier spot-checks rounds 49–53. This is a capture-status sweep, not a re-verification of the original events. `CAPTURED` means a later lesson/criterion/erratum/scorecard note explicitly records the disposition; it does not imply that a procedural defect is operationally impossible. `OPEN` means the defect or residual remains routed without a located closing record in the requested targets.

## Commands and observed source

Read commands (absolute paths):

- `read /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-{49,50,51,52,53}-verifier-spotcheck.md`
- `read /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/QUALITY.md`

Grep commands (literal search, absolute paths):

- `grep -nE 'round-49-verifier-spotcheck|round-50-verifier-spotcheck|round-51-verifier-spotcheck|round-52-verifier-spotcheck|round-53-verifier-spotcheck|D[1-9]|routed defect|correction|at-landed|at-salvage|successor-freeze' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/QUALITY.md`
- `grep -nE 'D[1-9]|routed defect|disagree|correction|at-landed|at-salvage|successor-freeze|round-49-verifier-spotcheck|round-50-verifier-spotcheck|round-51-verifier-spotcheck|round-52-verifier-spotcheck|round-53-verifier-spotcheck' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-{49,50,51,52,53}.md /home/vgpnk/Projects/shokunin/mori-shokunin/SCORECARD.md`

Observed: round-49–53 spotchecks are present. QUALITY explicitly cites round-50/51 lessons in criteria 134–143; criteria 146–149 cite later closure defects. The round-50/51/52 lessons contain itemized routed dispositions. SCORECARD has explicit round-52 and round-53 corrections, and the contract/round-54 records explicitly name prior D2/D3 as this round's checks. No LSP semantic server was available/used; this task is a literal documentary search.

## Disagreements and routed defects

### Round 49 spot-check

- D-a: report author date precedes cited lane tip. **CAPTURED (pointer):** round-50 lesson §Round-49 routed defects item 1 records the attempt-2 filing convention, while noting `fleet-commit.sh` remains fleet-owned and the code invariant is not fixed; round-50 spotcheck D-a confirms the second report commit postdates the tip. Treat as recorded, not a general fix.
- D-b: 49-seat wave below 64–100 range; no second wave/WAVE-DONE and two absent reports. **CAPTURED (pointer):** round-50 lesson item 5 determines the two late reports and carries the round-shape handling into its section. It does not erase the historical deviation.
- D-c: 48-vs-47 report count correction absent from lesson/LOG. **CAPTURED:** round-50 lesson items 2, 3 and appended correction section correct the count and name the report-vs-directory-entry distinction; QUALITY 133 captures defect mining as a practice.
- D-d: missing committed selftest outputs. **CAPTURED:** round-50 lesson item 2 points to committed receipts and round-50 spotcheck verifies them.
- D-e: `.scratch` debris remained despite ignore; cleanup partial. **CAPTURED (partial; residual routed):** round-50 lesson item 4 records deletion/counts but identifies live producers and routes them to round 51; round-51 lesson item 2 documents the producer fix and the zero residue measurement. Historical cleanup is captured; producer recurrence remains an explicit limit, not evidence of permanent prevention.
- D-f: 26 variants vs 27 lines. **CAPTURED:** round-50 lesson item 6 explains that the `real` control is excluded from the variant count and identifies the opaque duplicate; arithmetic discrepancy is resolved.
- D-g: “understates” argument for a different capture. **CAPTURED:** round-50 lesson item 8 gives provenance-first wording and says the entry carries no host claim.
- Routed K4 / R11 / randomised handle / wave-2 residuals from the spotcheck: **OPEN / carried limits.** Round-50 lesson item 7 says K4/R11 stay routed and the handle rule was not met; later round-51/52 lessons route the calibration and instrument limits, but no located record establishes that every named residual was closed.

### Round 50 spot-check

- D-a: first report commit author timestamp before lane tip due fleet commit behavior. **CAPTURED (owner/routing, not repaired):** round-50 closure records fleet ownership; round-51 spotcheck reports a timely report commit. The underlying fleet helper behavior remains outside mori's control.
- D-b: over 100 seats across attempts and frozen two-wave shape not followed. **CAPTURED (historical disposition):** round-50 lesson M3 and its round-shape section record attempt-1 death/salvage and count; round-51 lesson and spotcheck describe its one v2 wave within the 64–128 band. This does not make the first attempt conformant.
- D-c: wrong considerthese suggestion selected. **CAPTURED:** round-50 lesson records supersession and why the old baseline was unreproducible; round-51/round-52 closure notes carry the selected suggestion lineage.
- D-d: prior closure rerun not hermetic; round-40 script hardcodes lane path and scratch. **CAPTURED:** round-51 lesson item 1 identifies `round-40/conform.py` among writers; round-51 closure routed-defect dispositions and QUALITY 137 cover the external-tree behavior. Prior frozen-file edit hazard is treated separately below.
- Round-49 defects 2 and 4 (selftest receipts and `.scratch` residue) are explicitly marked closed in round-50 spotcheck; **CAPTURED** by that check and round-50 lesson.
- Round-50 routed successor calibration counter/K4, C2 entailment, contract deviations in LOG, round shape and residual writers: **CAPTURED or OPEN by item.** The entailment defect is **CAPTURED** by QUALITY 140/143, with round-51/52 lesson evidence and a hardened predicate. Round-51 lesson items 1/2 and QUALITY 137 capture the scratch writers. K4 is **CAPTURED** by QUALITY 141 and round-52 lesson M1 for QUALITY/README pins, but the prior spotcheck specifically said “beyond SHONEN”; no evidence here closes every other living surface. Contract deviation logging has **CAPTURED** evidence in round-51 lesson/LOG disposition; no broad guarantee beyond those recorded deviations.

### Round 51 spot-check

- D-a: registered counter lacked selftest mode. **CAPTURED:** round-52 lesson routed disposition item 1 states both counters ship `--selftest`; round-52 spotcheck confirms receipts.
- D-b: receipt command used placeholder scratch path. **OPEN:** no specific correction of the literal-command defect was found in round-52/53 lesson, QUALITY or SCORECARD search results.
- D-c: S493 locator drift. **CAPTURED:** round-51 lesson routed item 5 and `corpus/lessons/round-51-erratum.md` are the explicit erratum; round-52 lesson item 5 confirms it.
- D-d: famzah author comment misattributed as reader comment. **CAPTURED:** same round-51 erratum and round-52 lesson item 5.
- D-e: frozen round-40 file edited in place. **CAPTURED (design/routing; not a blanket closure):** round-52 lesson M4 names it and routes successor-freeze design; round-52 disposition item 6 records no in-place edit that round and routes design to round 53. No universal successor-freeze closure found in the requested later lesson/QUALITY/SCORECARD evidence: **OPEN** as a general hazard.
- Four self-authored single-vote replacement rows, fenced-line acceptance and non-dispatch voter acceptance / C1 survivors / remaining writers. **CAPTURED in successive steps:** QUALITY 143 captures two non-author votes and unfenced frozen voter list; round-52 lesson M5 and routed-disposition items 2–3 document the fix/remaining mutants; round-53 lesson and round-54 contract explicitly carry the v7.3 release recheck and its voter constraints. Any named counter weakness remains a limit, not silently fixed.
- Fleet-owned dispatcher findings (fail-open unreadable meminfo, GiB/MiB floor mismatch): **OPEN / operator-owned**, as round-51 spotcheck explicitly states.

### Round 52 spot-check

- D1: report retained `[FILL]` placeholders. **CAPTURED:** QUALITY 147 specifies command-based self-citation; round-53 spotcheck verifies the report hash and command convention.
- D2: SCORECARD C1 row used at-data tally while citing at-landed receipt. **CAPTURED:** round-52 lesson routed item 1 / correction and SCORECARD appended correction give 43/28 values.
- QUALITY 141 stale living tally and QUALITY 142 pointer locator: round-52 lesson M1/M2 and QUALITY 141/142 explicitly capture these.
- M4: frozen round-40 file edited in place. **OPEN as general policy** (see round-51 D-e above); round-52 disposition says no edit in that round and routes design.
- M5: entailment arm defect. **CAPTURED:** QUALITY 143 and round-52 lesson M5.
- Round-51 C1 counter survivors / K4 beyond SHONEN / residual locator-arm gaps: **OPEN or explicitly carried:** round-52 lesson routed dispositions item 3 and SCORECARD planned round 53 identify survivors; no later source located here declares all of them closed.

### Round 53 spot-check

- D1: salvage authorship attribution. **CAPTURED:** round-53 spotcheck records/discloses the operator salvage and re-verification; it is historical attribution, not a lane repair.
- D2: SCORECARD cited at-salvage instead of at-landed receipts. **CAPTURED:** QUALITY 148, round-54 SCORECARD correction and round-54 contract routed item name at-landed receipts and the correction.
- D3: eight tracked lane-root strays / empty `--repo/`. **CAPTURED:** QUALITY 149, round-54 contract, round-54 D3 receipt and round-54 contract's explicit relocation requirement record the byte-exact relocation under wave history and directory cleanup.
- Named round-53 limits (filename-keyed voter identity, C2 counter/selftest, mode-2 live leg, source anchors resting on one seat): **CAPTURED as limits/routes, not all resolved.** Round-54 freezes the separate voter identity binding and named limits; no evidence in these spotchecks proves an actual live mode-2 host leg or independent source re-fetch for every row. Those remain limits, not closure claims.
- Round-52 scorecard locator and report placeholder defects are also captured by round-53 QUALITY 142/147, as above.

## Summary

`CAPTURED`: corrections and historical dispositions are plainly preserved for report counts, variant arithmetic, erratum attribution/locators, selftest receipts, scorecard receipt mismatches, report self-citation, root misroots, and the specific counter-hardening lessons/criteria. `OPEN`: literal scratch placeholder in the round-51 receipt; fleet-owned author timestamp mechanism; broad no-in-place-edit/successor-freeze guarantee; named counter survivors and K4 scope not demonstrably closed across all surfaces; fleet-owned dispatcher findings; live mode-2 / independently verified source limitations. Findings are documentary and limited to the requested lessons, QUALITY and SCORECARD surfaces.

## Findings

- MED — `corpus/lessons/round-51-verifier-spotcheck.md` D-b: placeholder scratch path has no located correction in later target records (OPEN).
- MED — `corpus/lessons/round-51-verifier-spotcheck.md` D-e / `corpus/lessons/round-52.md` M4: successor-freeze design is routed/captured, but no general closure evidence located (OPEN).
- LOW — `corpus/lessons/round-49-verifier-spotcheck.md` D-a and `corpus/lessons/round-50-verifier-spotcheck.md` D-a: timestamp mechanism is recorded and fleet-owned; not established fixed.
- LOW — `corpus/lessons/round-53-verifier-spotcheck.md` D1: salvage authorship is disclosed and historically captured, not rewritten.
