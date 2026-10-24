# ReviewHygieneDebt — routed-defect triage R1–R8 (mori round 26, wave 1)

Seat: MoriR26.ReviewHygieneDebt (leaf reviewer). Date: 2026-10-22.
Scope: classify R1–R8 of `corpus/lessons/round-25-verifier-spotcheck.md:172-202` against the
entering-tip bytes `248408f5` (read-only `git show`/`git ls-tree` in the lane), recommend
fix-now vs named debt, and answer the L0 history-question check. This is a recommendation;
it changes no contract, claim, route or judgment.

Method and limits: every code claim below was read from committed bytes at `248408f5`
(extracted to `/fast/scratch/hyaku/mori-r26/MoriR26.ReviewHygieneDebt/tip/`), and the runway
parser claims were exercised by importing the tip blob in a scratch interpreter (output
quoted inline). No lsp device exists in this session and the review targets pinned git
objects, so working-tree diagnostics do not apply; byte-level checks are recorded instead.
No tool was installed or upgraded (tooling directive: no need arose; pacman pause respected).
Privacy: no OMP settings values, session ids, session-store paths, journal MESSAGE text, or
`--avoid`/`--prefer` values appear below; counts, states and paths only.

## R1 — runway false numbers + tool hardening — (b) code

Routed text: `RUNWAY_DEFAULT`, effective 100, exit 0 for configs omp reads as 50 (quoted,
escaped or anchored `async` headers; flow children, flow roots, indented roots), plus the
ReviewRunwayCode list (`set` for files Bun refuses to parse; `--selftest --cases ""` runs the
frozen cases silently; uncaught exceptions exit 1, the `RUNWAY_CLAMPED` code; no FIFO or
`/dev/zero` guard; untested CLI-exit and unreadable-binary paths; probe corpus not committed
as fixtures).

Tip state (verified, scratch import of `248408f5:tools/mori-job-runway.py`):

```
normal block                 -> ('set', 50)
indented root (doc indented 2) -> ('absent', None)   # -> RUNWAY_DEFAULT, effective 100, exit 0
flow root                    -> ('malformed', None)
flow child                   -> ('malformed', None)
quoted header                -> ('malformed', None)
spaced header                -> ('malformed', None)
anchored header              -> ('malformed', None)
escaped key (as\u0079nc:)    -> ('absent', None)     # -> RUNWAY_DEFAULT, effective 100, exit 0
```

So part of the routed parenthetical is already closed at the tip by amendment A2 (quoted,
spaced, anchored headers, flow roots and flow children abstain; the spotcheck measured the
pre-A2 tool `09f55b62`, see `SCORECARD.md:1559-1561`). Still open, each a false number where
omp reads 50: **indented roots** and **escaped keys** (`_parse_config`, tools/mori-job-runway.py:241-368 —
an indented top-level `async:` is skipped at :283-284 and a non-`async` normalized key falls
through to `absent` at :303).

Remaining items confirmed in code:
- `--cases ""` silently runs the frozen cases: `_resolve_cases` `if cases_override:` (tools/mori-job-runway.py:517-521).
- No catch-all around `evaluate()` in `main()` (tools/mori-job-runway.py:679-690): an uncaught
  exception exits 1, which the verdict map publishes as `RUNWAY_CLAMPED`.
- No FIFO/char-device/size guard before `handle.read()` in `_read_config_text` (:220-238).
- Probe corpus not committed as re-derivable fixtures: the tip has only
  `tools/fixtures/mori-job-runway/cases.json` and `supplementary-cases.json` (git ls-tree).
- No committed CLI-exit or unreadable-binary test arms (`_selftest` runs the cases file only, :600-610).

Estimate: ~40–80 lines in the tool (abstain on indented roots and escape-decoded keys; reject
empty `--cases`; catch-all → exit 2 with an error object; `os.fstat` FIFO/char-device guard;
CLI test arms) plus ~8–12 new cases in the supplementary file written by a seat other than the
tool seat and committed before the parser change.

Operability risk: low direct — the tool is read-only and this host's live verdict
(`RUNWAY_CLAMPED`) is correct. The real hazard is the committed claim: the frozen 21/21 and
24/24 PASS lines are recorded in `SCORECARD.md:1546,1556,1569`, so a parser change that flips
one frozen case falsifies a recorded claim. Cases land first; frozen cases must stay green.

## R2 — SCORECARD capability row overclaim — (a) prose

Exact place: `SCORECARD.md:1569`, the round-25 capability row cell "…a verdict that never turns
an unreadable, ambiguous or unparseable input into a number". Fix: append a dated, scoped
correction to the round-25 corrections block (`SCORECARD.md:1574-1586` is the established
pattern): the guarantee holds only for the forms rule 1 reads; at the tip the indented-root
and escaped-key forms still yield `RUNWAY_DEFAULT`/effective 100/exit 0 (R1 evidence). If R1
lands this round, the correction says "until `<fix commit>`". D5/D1 predicates do not read
this row, so the fix is gate-safe. Recommend: fix now.

## R3 — SKILL round-25 block — (a) prose

Exact place: the refusal table `SKILL.md:656-661`, in place (QUALITY 77 prefers an in-place
rewrite over a shadowing note):
- Row 1 (:658): garbled host sentence "this host's the operator's OMP settings file says 200".
- Row 2 (:659): "a bash or eval call was made while the cap was full → nothing" holds only for
  the auto-background branch; the spotcheck names eval `agent()` and `workpool()` and explicit
  `async: true` bash as refusing paths (S103 `eval.md:258`; upstream `agent-bridge.ts:210`,
  `workpool.ts:175,363` — cited from the routed list, not re-verified upstream this round).
- Row 3 (:660): lists too few refusing paths; add the two above.
- Row 4 (:661): add the false-number caveat or a pointer to the R2 correction.
Recommend: fix now. No predicate reads these rows; gate-safe.

## R4 — SCORECARD calibration residuals — (a) prose

Three exact places:
- `SCORECARD.md:11` — Axes operability row, Last change "round 13 (6 → 7)". Round 13 was
  rejected-harmed; 7 was first admitted in round 14. Reword the cell to "round 14 (6 → 7;
  round 13's 7 was self-assessed and the round rejected-harmed)". D5 stays green: the
  predicate checks the score and forbids a "round 1" token when the score differs from the
  round-1 value (tools/mori-routed-r24.py:164-165,739-741); "round 14" matches neither trap.
- `SCORECARD.md:1584` — "D5 checks scores only, not evidence pointers or Last change text."
  False: the D5 predicate reads Last change and fails a differing-score row that says
  "round 1" (tools/mori-routed-r24.py:50-51,739-741). Reword to name the round-1 token check.
- `SCORECARD.md:620-621` — "the table is left as filed; this section's scores supersede it".
  Stale since the round-25 A5 rewrite (`e68855d5`) rewrote the round-1 Axes scores; reword as
  a dated record ("the round-1 table was left as filed until round 25; A5 rewrote the scores,
  see the correction at :19-23").
Recommend: fix now.

## R5 — gate conformance — (a) prose half + (b) code half

Prose half: add registry rows for `tools/mori-routed-r24.py` and `tools/mori-job-runway.py`
at the registry home (the `SKILL.md:162-196` table and/or the per-round "registry additions"
blocks at `SKILL.md:637-643`; neither tool has a row there today — verified by table read).
Recommend: fix now.

Code half (all sites verified at `248408f5:tools/mori-routed-r24.py`):
- No committed self-test: argparse has only `--repo/--rev/--rerun` (:892-902). A selftest in
  the house style (temp git sandbox, as `tools/mori-retention-gate.py:411+` does) is ~80–150 lines.
- D1 compares the body with a constant (`EXPECTED_BODY`, :97-101) and the rerun "is reported
  only: it never decides whether D1 holds" (:511-517), so only `--rerun` detects a forged
  byte-equal PASS. Fix (make held require rerun equality, or publish an `unverified` state) is
  ~30–60 lines and changes the verdict map.
- D5 reads columns by position ("the axis is the second field, the score the third, and the
  last change the second-to-last", :640-661). Parse by header name: ~15–25 lines.
- D2's heading handling lives in `_blocks`/`_section_span` (:341-390); route heading-level
  handling through it: ~10–20 lines.
- D3 holds while the uncorrected `PASS 6/6` line survives beside the correction (`_check_d3`
  searches only for the correction line, :758-800): ~10 lines.
- Missing-baseline fail-open: `_blob_bytes` returns None for both absent path and read failure
  (:290-295), and a None base blob or base score parse (:670-688) becomes a mismatch → exit 1
  (:917-933) instead of could-not-evaluate → exit 2: ~15–25 lines.
- Promisor clone writes: `_git` (:206-222) runs plain `git --no-optional-locks -C …` with no
  `--no-lazy-fetch`, so a lazy fetch can write objects into the measured repo (the
  flag-plus-refuse-older-git pattern is established fleet-side; kama L0 row 87) [INFERENCE on
  exact git mechanics; the defect is the routed claim]: ~10–15 lines.
- Sub-directory `--repo` changes results: ls-tree pathspecs are cwd-relative (:259, :273-287)
  while `rev:path` cat-file paths are toplevel-relative, so a sub-repo call reads a different
  tree. Resolve the toplevel or use `--full-tree`/`:/` pathspecs: ~10 lines.
Total: ~150–260 lines plus the selftest.

Operability risk: medium. This tool is committed gate evidence
(`.ufo/waves/round-25/evidence/routed-r24-*-a5.txt`; `SCORECARD.md:1556`); changing D1's held
semantics changes the verdict map, so the SKILL/SCORECARD pointers must move in the same
change or the recorded `"held": 4` results stop being reproducible. Recommend: prose rows now;
code half now if wave-2 capacity allows, else named debt.

## R6 — lesson wording — (a) prose

Places in `corpus/lessons/round-25.md`, rewritten in place:
- :4-5 — "amendments A1–A4 each landed before the code it governs": false for A4 (the
  spotcheck: A4 came ~15 s after the tool) and A5 is unlisted. Reword as a dated record.
- :9 — "The harness job cap is 100, whatever the config says": false below a configured 100
  (effective = `max(1, min(100, configured))`, the round's own S099/S102 facts).
- :16-17 — "only registration paths (explicit async bash, task spawns) throw": omits the eval
  `agent()`/`workpool()` registration paths (S103; same upstream anchors as R3 row 3).
- :18-20 — refusal-count wording: "48 failed tool calls" is a unit error. The wave-2 recount
  committed at the tip (`.ufo/waves/round-25/w2/ScoutRefusalRecount.md` F2) measures 48 text
  occurrences in 29 failed tool-result records, only 26 of them the refusal itself.
- :97-99 — "The SCORECARD Axes table at its top still shows round-1 scores": false at the tip
  (A5/`e68855d5` fixed it) and currently shadowed by the appended correction at :102-105;
  rewrite the bullet in place per QUALITY 77 and keep the appended note as the dated record.
Recommend: fix now. Gate-safe: D3's target is `round-24.md`, untouched.

## R7 — knowledge corrections — (a) prose

Places:
- `corpus/knowledge/harness-job-capacity-r25.md:266-271` — U1 "only the default moved (15 to
  100)": false; the routed spotcheck records the "(1-100)" setting description removed
  2026-05-03 and the clamp expression rewritten 2026-09-24.
- `corpus/knowledge/harness-job-capacity-r25.md:164-165` — the F10 parenthetical "(64, 66, 68,
  88 in those records)" mis-cites the two records it names: `GtLaneKasegi.md` and
  `GtLaneKama.md` contain 64 and 66 and no 68/88 refusal counts (verified by grep over both
  tip blobs; the `:48` and `:72` line anchors themselves carry the quoted sentences and are
  correct). Drop 68/88 or cite the records that hold them.
- `corpus/knowledge/system-pressure-r24.md:143` and `:158` — the two routed imprecisions;
  plus the `psi.c:1538-1550` citation at :148, which the lane's own lesson already scopes
  ("the corrections give `1540,1545,1550` plus `1686`", `corpus/lessons/round-25.md:88-89`).
  Put the new correction rows inside the entry's `## corrections` section so D2 stays green
  (the predicate requires the `(k4)`/total line inside corrections and the banned phrases
  absent outside it, tools/mori-routed-r24.py:103-118,596-617).
Recommend: fix now.

## R8 — no-harm check — (c) history disposition; the scan run is process

- Real-tree scan at every candidate tip: already bound for this round by the contract
  ("the lane retention scan (R8) is run at the entering tip and at every candidate tip; its
  value at the landed tip must not exceed the entering value", `.ufo/waves/round-26/contract.md`
  §Held). Entry point is documented (`SCORECARD.md:1484-1489`; `SKILL.md:178`): run
  `python3 -I tools/mori-retention-gate.py scan --repo "$PWD" --rev <REV> --policy
  .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json`
  at the entering tip and at each candidate tip, and commit the outputs as round evidence.
  Classification: prose/process, no code required. Optional hardening (an `--expect-metric`
  ceiling so a growth fails the run) is ~10–20 lines and can ride later.
- History disposition of the earlier pushed commits: **(c) operator-owned**, per the routed
  text itself ("goes to the operator (with kagi); the lane takes no rewrite action").

## L0 check (report only, nothing private quoted)

The history-in-the-public-remote question is filed in the fleet queue
`/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` (the mori round-26 history-disposition
row). It has **no** `L0 ANSWER` line: the only two `L0 ANSWER` lines in the file are on rows
52–53, which answer a different question (planner-seat validation). The history question is
therefore still open with the operator.

## Recommendation summary

| Item | Class | Fix now? | One-line reason |
|---|---|---|---|
| R2, R3, R4, R6, R7 | (a) prose | Yes | In-place dated corrections; no counted-claim or gate impact when placed as specified above. |
| R5 registry rows | (a) prose | Yes | Two tools missing from their own registry home; five-minute fix. |
| R5 code (selftest + closures) | (b) ~150–260 lines | Yes if capacity, else named debt `routed-r24-harden` | Forged-PASS blind spot is real but one of several independent evidences; needs a verdict-map migration in the same change. |
| R1 | (b) ~40–80 lines + 8–12 cases | Yes if capacity, else named debt `runway-forms-abstention` | Two open false-number forms at the tip (indented roots, escaped keys); advisory tool, but frozen-case claims force cases-first sequencing. |
| R8 scan execution | process | Yes (already contract-bound) | Round-26 contract already mandates the run; just commit the evidence at each tip. |
| R8 history disposition | (c) operator | Not lane-actionable | Operator-owned with kagi; L0 row open, no answer yet. |

Residual risk and verification gaps: the R3 row-2/row-3 upstream anchors
(`agent-bridge.ts:210`, `workpool.ts:175,363`) and R7's 2026-05-03/2026-09-24 setting-history
dates are taken from the routed spotcheck and were not re-fetched upstream this round; the
`--no-lazy-fetch` git mechanics are [INFERENCE] as noted; the `system-pressure-r24.md:143/:158`
imprecision contents are the spotcheck's routing, not independently re-derived. None of these
change the classifications.
