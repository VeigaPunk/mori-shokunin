measured 2026-10-23T09:15:39Z

# JudgeCanary — canary test of the wave-2 row-judging rule (round 35 C1)

Attacks: the ruling recorded at `evidence/c1-controls.txt:40-44` — the residual rule that "the lane's own
register is held to (a) non-empty, closure-faithful capability and what cells and (b) evidence cells holding
only backticked paths, and wave-2 non-author reviewers judge every row on (a) and (b) as
supported/unsupported". Question: does that rule, applied as written, flag defective register rows that
P-C1 cannot see?

## Method

- Base table: the final `## Capabilities` table of `SCORECARD.md` at `cedb0ec4f3a4f672804deac388b7191258f01fcd`
  (18 data rows, header at file line 1959). Copied verbatim, then exactly 5 rows altered; keys, rounds and
  evidence cells unchanged. Altered bytes: `/fast/scratch/hyaku/mori-r35/JudgeCanary/altered-table.md`.
- Seed: `random.Random(20261023)`; `r.sample(range(18),5)` → rows `[5,6,8,16,17]` (0-based over the 18 data
  rows); `r.shuffle` of `[deny-A,deny-B,other-round,empty-cap,bag-of-words]` → order
  `[empty-cap,bag-of-words,deny-A,other-round,deny-B]` zipped to the sorted rows. Same `r` shuffled the
  bag-of-words tokens.
- Rule application: judged each row's capability/what cells against the MANIFEST `capabilities_added` string
  of its key (`git -C /home/vgpnk/Projects/shokunin show 37b51a24:MANIFEST.json`, lane==mori, admitted) and
  its evidence cell for backticked-paths-only.
- Counter run: clone `clone` under `/fast/scratch/hyaku/mori-r35/JudgeCanary/` (no-hardlinks clone of the
  lane, checkout `cedb0ec4`), appended the altered section as the new last `## Capabilities` section, commit
  `71fde3b6962a46792cc7d66492aa24b9bb8f3a4a`; scored with a scratch copy of the frozen counter
  (sha256 `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167`, matches receipt
  `c1-controls.txt:2`).

## Row → altered? → rule verdict

| # | key (short) | alteration | rule verdict |
|---|---|---|---|
| 1 | rounds[313].cap[0] source registry | — | supported (cap+what faithful to "sources-registry (34 rows; census clean)", evidence `corpus/SOURCES.md` backticked) |
| 2 | rounds[339].cap[0] typed journal alarm/triage | — | supported |
| 3 | rounds[345].cap[0] partial positive journal alarms | — | supported |
| 4 | rounds[353].cap[0] exact-start journal record window | — | supported |
| 5 | rounds[386].cap[0] retention gate | — | supported |
| 6 | rounds[386].cap[1] freeze-order check | **empty-cap**: capability cell emptied | **unsupported** (fails (a): non-empty) |
| 7 | rounds[386].cap[2] dispatch-attempt ledger verify | **bag-of-words**: what-cell = shuffled tokens of its own MANIFEST string ("bound STARTED_MISSING and ledger 1/1 tools/mori-dispatch-ledger.py 2/2 dispatch-attempt residual bound with w2 7/7 14/14 selftest w1 clean, verify") | **unsupported** (see note) |
| 8 | rounds[398].cap[0] blob-bound content-review gate | — | supported |
| 9 | rounds[427].cap[0] retention receipt reconciliation | **deny-A**: what-cell = "This capability was never demonstrated and does not work" | **unsupported** (contradicts closure) |
| 10 | rounds[443].cap[0] one-shot system pressure read | — | supported |
| 11 | rounds[443].cap[1] round-23 routed-item check | — | supported |
| 12 | rounds[455].cap[0] harness background-job runway read | — | supported |
| 13 | rounds[455].cap[1] round-24 routed-defect/Axes check | — | supported |
| 14 | rounds[462].cap[0] userspace OOM killer read | — | supported |
| 15 | rounds[476].cap[0] SOURCES freshness repair | — | supported |
| 16 | rounds[476].cap[1] amendment-A2 frozen cases | — | supported |
| 17 | rounds[495].cap[0] blind-writer gate | **other-round**: what-cell = row 16's text (round-28 amendment-A2 capability) on a round-31 row | **unsupported** (describes a different closure's capability) |
| 18 | rounds[495].cap[1] watchdog identity decision table | **deny-B**: same denial sentence | **unsupported** |

Flagged among altered rows: **5/5**. Flagged among unaltered rows: **0/13** — all 13 carry non-empty,
closure-faithful capability and what cells (checked against the 18 oracle strings above) and single/double
backticked evidence paths.

## Counter score of the altered register

`timeout 300 python3 count-c1.py 71fde3b6962a46792cc7d66492aa24b9bb8f3a4a --repo clone` (scratch copy,
sha256 above):

```
label=P-C1 rev=71fde3b6962a46792cc7d66492aa24b9bb8f3a4a manifest_rev=37b51a243302 register='## Capabilities' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
```
exit **0**. All 18 rows print `matched`, including the five defective ones — expected: the counter reads only
`cells[3]` (evidence) and `cells[4]` (round); cells 1–2 are never inspected (`count-c1.py:158-176`). P-C1
flags **none** of the four defect shapes.

Note on the bag-of-words row (the arguable shape): I rule it `unsupported` because (a) requires the
what-cell to state *what the capability can now do*; a shuffled token bag asserts nothing and is not
closure-faithful even though every token came from the row's own MANIFEST string. A reviewer reading
"closure-faithful" as merely "drawn from the record" would mark it supported — then 3 of 4 shapes flagged
and the claim would fail. The rule as written does not disambiguate; that is a rule-wording gap, not a
detection gap.

Tooling: no installs; stock `git`, `python3` only. Scratch confined to `/fast/scratch/hyaku/mori-r35/JudgeCanary/`
(counter copy, altered-table.md, clone `71fde3b6`); lane touched read-only plus this report.

VERDICT: holds — the rule flags all four defect shapes (5/5 altered rows unsupported, 0/13 unaltered
flagged) while the frozen P-C1 counter scores the same bytes `matched=18 C1=met` exit 0; residual risk is
the wording gap on "closure-faithful" for the word-salad shape.
