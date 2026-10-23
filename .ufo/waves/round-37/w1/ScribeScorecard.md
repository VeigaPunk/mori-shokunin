# Round 37 SCORECARD receipt-command audit

**Axes:** command traceability and scope fidelity. **Scope / behavior.** Read-only comparison of the Round-37 declaration and measured-outcome tables in `SCORECARD.md` with each cited receipt. Gate: each before/after cell's command must appear in the receipt it cites. I did not rerun counters or alter product/evidence files.

| Claim | SCORECARD cell | Command named or implied by the cell | Cited receipt | Command present? |
|---|---|---|---|---|
| C1 | Declaration — Before (`SCORECARD.md:2044`) | `python3 .ufo/waves/round-36/count-c2.py bf0df77 --tool .ufo/waves/round-37/fixtures/memo-n1.py --seed 11` | `evidence/c1-before-memo.txt` | **No** — full receipt has the tool path, results, seed and exit, but no counter invocation (`:1-10`). |
| C1 | Declaration — Before (`SCORECARD.md:2044`) | `python3 .ufo/waves/round-36/count-c2.py bf0df77 --tool .ufo/waves/round-37/fixtures/summary-only.py --seed 12` (the cell abbreviates this as “same counter with” the summary-only fixture) | `evidence/c1-before-summary.txt` | **No** — full receipt has the tool path, results, seed and exit, but no counter invocation (`:1-10`). |
| C1 | Declaration — declared after-value (`SCORECARD.md:2044`) | `python3 .ufo/waves/round-37/count-c1.py <landed tip>` | `evidence/c1-after.txt` | **No** — receipt records the tool path, arms, verdict and seed, not the counter invocation (`:1-16`). |
| C2 | Declaration — Before (`SCORECARD.md:2045`) | `python3 .ufo/waves/round-37/count-c2.py 842a320` | `evidence/c2-before.txt` | **No** — receipt has checks and verdict, not the counter invocation (`:1-11`). |
| C2 | Declaration — declared after-value (`SCORECARD.md:2045`) | Same counter at the landed tip (`python3 .ufo/waves/round-37/count-c2.py <landed tip>`) | `evidence/c2-after.txt` | **No** — receipt has checks and verdict, not the counter invocation (`:1-11`). |
| C1 | Measured outcome — After (`SCORECARD.md:2065`) | `python3 .ufo/waves/round-37/count-c1.py e57c58b5` | `evidence/c1-after.txt` | **No** — receipt records results but no counter invocation (`:1-16`). |
| C2 | Measured outcome — After (`SCORECARD.md:2066`) | `python3 .ufo/waves/round-37/count-c2.py e57c58b5` | `evidence/c2-after.txt` | **No** — receipt records checks and verdict but no counter invocation (`:1-11`). |

**Gate result.** 0/6 before/after cells satisfy the receipt-command requirement (the C1 Before cell contains two command references, both absent from their respective receipts). The cited receipts establish outcomes, but not the commands claimed by these SCORECARD cells. Locations: `SCORECARD.md:2044-2045,2065-2066`; receipts under `.ufo/waves/round-37/evidence/` as listed above.

**Touched surfaces.** Inspected `SCORECARD.md`, the round contract and the four cited C1/C2 receipts; created only this report. No installs. No counter executions or product/evidence edits.

**Out of scope / limits.** This audit checks command presence only; it does not reassess counter correctness, reported outcomes, mutations, or the C1/C2 claims. No work was rerun.

**Artifact:** `.ufo/waves/round-37/w1/ScribeScorecard.md`

VERDICT: FAIL — all audited before/after cells cite receipts that omit their command.