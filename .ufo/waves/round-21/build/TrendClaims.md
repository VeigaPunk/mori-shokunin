# TrendClaims — outside-sample audit of round21 trend claims

Seat: MoriR21.TrendClaims-4 (reviewer, detection/report only). Scope: the bounded requirement
"New repairs alone do not establish expansion; quality/discernment claims need precise outside
sample, no self-certification." No production writes, no tests, no tool installs. All paths
relative to `mori-shokunin/`.

## Findings by severity

### F1 HIGH — the calibration trend claim is currently certified only by the rule's own truth table; the two outside-adjudicated real events are cited but never exercised

The executed C2 measurement (selftest assertions `.scratch/round21/ImplLoss/tools/mori-evidence-loss.py:1054-1063,1082-1094`: before-rule `mismatched==2`, after-rule `mismatched==0` over `frozen/cases.json`) cannot support a discernment/calibration *trend* claim, because the six frozen rows are mechanically derivable from the rule parameter itself (`classify` at `:681-714` implements exactly "lost ∧ ¬independent → census-regression"; the contract's "Frozen rule cases" section is that same predicate enumerated). Before/after mismatch counts of 2/0 are algebraically guaranteed for any `(false, true)` rule pair — they certify implementation fidelity against the design, not that the design decides any real event better. This is the self-certification shape: author, expectation author, and rule author are the same decision (freeze at 3b792db makes it *pre-implementation*, not *outside*).

Meanwhile the round record contains exactly the precise outside sample the claim needs, authored by the non-author round-20 closure (outside every round21 claim author):

- `aggregator-r10` / `aggregator-r10-resume` unresolved evidence loss ⇒ `census-regression`, pin blocked — fleet `MANIFEST.json` `/rounds/405/verification/C1_class_ruling`; `.ufo/waves/round-20/falsify/AdjudicateWaves.md:5,29`.
- `shokunin-train-20261016-w24` new aging ⇒ `live-state`, not blocked — `AdjudicateWaves.md:7,29`.

Both are only quoted in prose (e.g. `corpus/lessons/round-21.md` M1/M2, `build/HistoryScore.md:9`); no `classify` run ever consumes them. Peer `build/CriticCalibration.md:15-17` found the adjacent gap (six rows "do not contain any of those three identities nor bind them to source evidence"; the classifier "consumes already-decided booleans").

**Counterexample, demonstrated.** I authored a two-row outside-labeled case file from the adjudication (proposal: `build/TrendClaims/real-cases-outside-proposal.json`, provenance in `build/TrendClaims/README.md`) and ran the unmodified scratch classifier read-only:

- before-rule (`frozen/before-rule.json`): `real-aggregator-r10-loss` observed `live-state`/pin-allowed against expected `census-regression`/blocked → `mismatched:1`, rc 1. The Q67 model is measurably *contradicted by the real adjudicated event* — that is the falsifiable content behind "calibration harmed, superseded".
- after-rule (`frozen/after-rule.json`): both rows matched → `mismatched:0`, rc 0. The w24 control staying `live-state` shows the new rule is not a blanket blocker — discernment on the negative direction, outside-labeled.

**Smallest safe change (no frozen bytes, no production edits):** (1) land the two-row outside-sample file as round21 lane evidence with its non-author provenance (adoption is the integration owner's call; my seat-dir copy is a proposal); (2) in the scorecard's already-reserved "exercised outcomes are appended after integration" line (`SCORECARD.md` Round21 section, after `:1305`), record before-rule 1/2 real-sample mismatch, after-rule 0/2, and word C2 as "matches the outside-adjudicated sample; the six frozen cases remain implementation-consistency evidence, not evidence of discernment". Two case rows + two classify runs; nothing else.

### F2 MEDIUM — "independently exercised" in the landed lesson overstates the independence that exists

`corpus/lessons/round-21.md:8`: "supersede QUALITY67's universal cause-only rule with **independently exercised** evidence-loss-first decisions." Independence actually present: expectations frozen pre-implementation (3b792db) and the non-author round-20 adjudication supplying real ground truth (unexercised — F1). Independence not present: the harness/evaluator author is the claim author (OracleLoss died; "its author provenance is L1" is disclosed in the same file), and `.ufo/waves/round-21/trust-refinement.md` states the tool's independence fields are "necessary structural evidence, not proof of independence". Under the round's own standard, "independently exercised" reads as actor-independent exercise, which did not occur. **Smallest safe change:** appended erratum (append-only; never rewrite landed bytes) reserving "independent" for (i) the pre-implementation freeze and (ii) outside disposition review, and describing the classifier exercise as "same-actor harness against pre-implementation frozen expectations". Once F1 lands, the real-sample expectations carry non-author adjudication — the strongest independence actually available this round.

### F3 LOW (guard, not defect) — "0 omitted" must stay scoped to the 2 contract-required identities

`frozen/required.json` scopes C1 to exactly `aggregator-r10`/`aggregator-r10-resume`, outside-anchored at `corpus/evidence/baseline-r10-20261015T2231Z.json:26-27` (verified: those lines are the two `WAVE_UNSETTLED_AGE` rows for these identities). The same retained baseline carries nine further unsettled-age rows (`:28-36`) that are *not* evidenced disappearances; pulling them in would over-claim, so the narrow scope is correct. But a repair that adds rows to its own register trivially reaches 0 on that register; the appended exercised-outcome line must therefore repeat "of the 2 contract-required identities" so "0 omitted" cannot inflate into a global freshness claim. As landed, C1 holds freshness 5→5 and keeps the pin blocked (`corpus/evidence/loss-accounting-r21.json`: both rows `unresolved`, `independent_disposition:null`; audit rc 1 by design) and no expansion credit is taken from the repair (`SCORECARD.md` Round21: "Author expansion is not claimed for historical repair/source-row volume"; `corpus/QUALITY.md:277-278` "This supersession does not assert those separate gates were repaired"; lessons "Carried defects (not round21 improvement claims)"). The "expansion improved" trend remains the round-20 closure's verdict, not a round21 repair claim — firewall intact on all three surfaces.

## Verified non-findings (do not double-fix)

- `classify` reads the actual rule object and decides only from it plus case booleans; no phase presumption; emits per-case observed decisions, `mismatched`, `matched`, `rule_source` (`:681-714`). Contract requirement met.
- Before-rule fidelity: `evidence_loss_blocks:false` ⇒ always `live-state`/pin-allowed reproduces Q67's cause-only permission; Q67's `blind_spot` clause only annotates, never blocks (`corpus/QUALITY.md:245-250`) — the constant-false model is faithful, including for the real loss case (ordinary_state_change:true does not rescue it; demonstrated above).
- The contract's other outside-sample requirement is met: source lesson cites reopened S066 (decision semantics only, not mori policy authority) and re-rejects S072, with non-author Main spotcheck (`.ufo/waves/round-21/evidence/source-spotcheck.json`; lessons Gate table). My finding is scoped to the *measurement*, not the sourcing.

## Residual risk and verification gaps

- I did not execute `audit` against `corpus/evidence/loss-accounting-r21.json` + `frozen/required.json`; the C1 conclusion rests on reading the landed rows. Audit-path findings belong to the Audit* peers.
- The w24 control's expected value rests on one outside document (`AdjudicateWaves.md`); `AdjudicateStale.md` could provide a second stale-class anchor — not re-read by this seat.
- Landed-vs-committed state of corpus bytes (QUALITY69, lessons/round-21.md, loss-accounting-r21.json) was not verified against Git; treated as read at observation time.
- No coordination assumed with FixtureLoss/ImplLoss lanes; `build/TrendClaims/` holds proposal files only.

Commands run (read-only): two `python3 .scratch/round21/ImplLoss/tools/mori-evidence-loss.py classify --rule <frozen rule> --cases build/TrendClaims/real-cases-outside-proposal.json` invocations, stdout only. No tools installed. No frozen, corpus, or production bytes modified; seat output limited to `build/TrendClaims.md`, `build/TrendClaims/README.md`, `build/TrendClaims/real-cases-outside-proposal.json`.
