# Mo53a2RevScorecard — residual review

Reviewed SCORECARD.md at `34d97cd3eaea8c13b0f065afc52aac1e5cf518a5` (contract `.ufo/waves/round-53/contract.md`, read first). Axes: scorecard claim/count fidelity, capability admission, and route completeness.

## Evidence and checks

- `python3 .ufo/waves/round-53/count-c1.py 34d97cd3eaea8c13b0f065afc52aac1e5cf518a5` → `C1=met scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=46 dissent=0 rev=34d97cd3eaea8c13b0f065afc52aac1e5cf518a5`, exit 0.
- `python3 .ufo/waves/round-53/count-c2.py 34d97cd3eaea8c13b0f065afc52aac1e5cf518a5 --scratch /fast/scratch/hyaku/mori-r53/Mo53a2RevScorecard/c2` → `C2=met tool=present selftest=pass n=31 fixtures=80 agree=80 disagree=0 registry=ok live=ok rev=34d97cd3eaea8c13b0f065afc52aac1e5cf518a5`, exit 0. Thus both frozen counters still read met at the reviewed tip.
- Round-53 after cells match the salvage receipts: C1 `held=44 absent=2 holds=46 changed=0 voted=46 dissent=0` (`evidence/c1-at-salvage.txt`); C2 `n=31 fixtures=80 agree=80 disagree=0 registry=ok live=ok` (`evidence/c2-at-salvage.txt`).
- Round-52 correction: `evidence/c1-at-landed.txt:45` prints `items=43 ... locators=28 ... mismatches=0 errors=0 hidden=0 lane_writes=0`, rc 0, matching the correction; it distinguishes the superseded 42/27 at-data receipt.
- Capability row: AXES.md §Capabilities permits entry only after a passing demonstration. SCORECARD line 2825 points to `--selftest` PASS 31/31 and `evidence/c2-at-salvage.txt`; the passing demonstration is additionally the 80/80 counter fixture arm above. The row accurately describes the capability and does not pre-claim it.

## Route reconciliation

The lesson's routed residuals include C1 filename-keyed voter identity; C2 exit-code arm and archive-importable REF; four other v7.2 release-triggered entries plus S511–S513; and the frozen-counter weakness set. SCORECARD Planned (round 54) names these explicitly in its C1/C2 counter-weaknesses clause and lists the uncovered release scope. It also carries the round-52 standing limits and unfinished round-53 planned work. Comparing the lesson's w1 HIGH/MED list against Planned (round 54): the HIGH findings (C1 filename identity and C2 exit-code arm / archive REF) are named; the MED items are covered collectively by “frozen-counter weaknesses routed from wave w1” rather than individually enumerated. The latter is less auditable than naming every item, but is not a silent omission because the lesson section is directly referenced. No un-routed HIGH/MED finding identified.

## Findings

- LOW — `SCORECARD.md:2845-2846`: Planned (round 54) refers readers to the lesson's integrated-findings section for the frozen-counter weaknesses rather than listing the MED weaknesses individually. This is a traceability weakness, not a missing route: the linked lesson contains the specific findings. No replacement required for correctness.
- No MED/HIGH findings. The round-52 correction, round-53 After counts, and capability demonstration are supported by cited receipts and the rerun counters.

Scratch `/fast/scratch/hyaku/mori-r53/Mo53a2RevScorecard/` was removed by the shell trap after the counter run.
