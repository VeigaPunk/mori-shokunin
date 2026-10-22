# Round 25 wave 2: ReviewAxesTable (C1 item D5, the SCORECARD `## Axes` table)

Seat: MoriR25.ReviewAxesTable. Leaf reviewer: no subagents, no background jobs. Read-only on the lane; this file is the only write.

Tip reviewed: lane HEAD `e0e33c1` (08:45 -0300). The Axes rows (SCORECARD.md:8-15) are unchanged since `e68855d`. The six commits after `07a31ae` only append text after SCORECARD.md:1547, add wave-2 files, a LOG entry and a lesson correction block. No tool changed.

## Verdict

- **Scores (six cells): held.** coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6 each match what the closure-admitted record supports. No wrong score found.
- **Last-change rounds: held on the score reading, weakened as a field.** On the score reading the table uses (round 12 for coverage and depth, round 13 for operability, round 1 for freshness, calibration and adjacency), all six are right. The column has no definition. On the verdict reading that the lane's closures and its own text use, five of six cells are wrong (M1).
- **Evidence pointers: held.** Nothing cited is false at the tip. Two pointers overstate their source (L1, L2).
- **Counted D5 as calibration evidence: weakened.** It passes at the tip (held 4 of 4, exit 0). But it compares the six scores with the lane's own round-24 declaration, which it calls "observed", and it checks one round-1 rule. It cannot catch a wrong Last-change round, a dead pointer or the verdict-reading mismatch (M2).

Nothing is wrong on the score reading. The findings are the definitional, provenance and predicate defects the calibration claim should fix before its counted check is read as a check of the table.

## Cell check at e0e33c1

| Axis | Score | Record support | Last change (table) | Score reading | Verdict reading (last admitted "improved") |
|---|---|---|---|---|---|
| coverage | 6 | r12 admitted 5 to 6 (MANIFEST `.rounds[313]`); r13 self-assessed 7 harmed and withdrawn (SCORECARD:743); r14 holds 6 (`[339]`); r24 "Score 6 → 6" (lesson:88; `[443]`) | round 12 (5 → 6) | right (SCORECARD:615) | r24 (`[443]`): table wrong |
| operability | 7 | r13 improved (`[327]`); r14 unchanged at 7 (SCORECARD:744, :793; `[339]`); held 7 r15-r24, verdict improved only in r18 (`[386]`) | round 13 (6 → 7) | right (SCORECARD:696) | r18 (`[386]`): table wrong |
| depth | 5 | r12 improved 4 to 5 (`[313]`); unchanged since | round 12 (4 → 5) | right (SCORECARD:613) | r12: right |
| freshness | 5 | r1 5; r12 unchanged 5 (SCORECARD:617); r20 harmed, score held (`[405]`); r21 improved at 5 (`[412]`) | round 1 | right on score lineage | r21 (`[412]`): table wrong |
| calibration | 5 | r1 5; r12 verdict improved but score held at 5 (SCORECARD:658; corpus/lessons/round-12.md:184); r20 harmed, held (`[405]`); r21-r24 improved at 5 (`[412]`, `[427]`, `[432]`, `[443]`; lesson:68) | round 1 | right on score lineage | r24 (`[443]`): table wrong |
| adjacency | 6 | r1 6; r12 unchanged 6 (SCORECARD:659); r13 harmed, held 6 (SCORECARD:745); r14, r18, r19 improved, 6 held (`[339]`, `[386]`, `[398]`); r24 unchanged | round 1 | right on score lineage | r19 (`[398]`): table wrong |

The score lineage is confirmed by history. `git log -L8,15:SCORECARD.md` shows the rows were created at `7ca17b1` with coverage 5, operability 6, depth 4, freshness 5, calibration 5, adjacency 6, and only `e68855d` changed them. Rounds 2 to 11 each state "No scalar score" (SCORECARD:122-123, 181-182, 240-241, 288, 335, 388, 438, 477-478, 519-520, 575-576), so no score moved before round 12.

## Findings

### M1. Medium. "Last change" has no definition; five of six cells fail the verdict reading the lane itself uses

- The column header (SCORECARD.md:8) has no definition. AXES.md:79 asks only for a "last-change round" per axis.
- The lane uses both meanings. Score reading: coverage 5 to 6 at round 12 (SCORECARD:611-615); operability 6 to 7 at round 13 (:693-696). Verdict reading: "freshness last moved round 10" (SCORECARD:1242-1243), while the Axes row says freshness "round 1" (:13). The calibration row cites the round-24 closure ("Score 5 → 5", lesson:68) on the same line that says "round 1" (:14).
- On the verdict reading (admitted closures' "improved", MANIFEST `.rounds[i]`), the last-change rounds are coverage 24, operability 18, depth 12, freshness 21, calibration 24, adjacency 19. The table has 12, 13, 12, 1, 1, 1.
- Consequence: a reader cannot tell which meaning applies, and the counted D5 tests neither (M2).
- Partly disclosed: none of the tail corrections defines the column.
- Smallest fix: put a definition in the table header, for example "round whose admitted closure last moved the score", and add the last improved verdict to any row where it differs, for example "(verdict improved r21; score unchanged)".

### M2. Medium. The counted D5 checks the table against the lane's own declaration, calls it "observed", and tests neither Last change nor pointers

- The pinned reference is SCORECARD.md:1499-1506 at `28b79d3d`. That block is the round-24 declaration. Its own line says "Targets, not results" (28b79d3d:1497). The four "held" values sit in the declaration (28b79d3d:1504). The tool calls it "the pinned observed state" (tools/mori-routed-r24.py:48, :141, :697), and so does contract A5.
- The predicate (tools/mori-routed-r24.py:718-741) checks three things: exactly one row per named axis; the score equals the pinned score; and, when a score differs from its round-1 value, Last change must not match `\bround\s+1\b`. It does not check any other Last-change round, that a cited round section exists, that any evidence path exists, or extra rows with other axis names (they are stored and ignored at :718-720; that is finding L7).
- What the counted check does show, re-run by me: at `e0e33c1`, `held 4, mismatches 0, exit 0`, with D1, D2, D3 and D5 held and hygiene held. At `28b79d3d`, `mismatches 4, exit 1`, and D5 reasons `coverage 5!=6`, `operability 6!=7`, `depth 4!=5`, matching `evidence/routed-r24-before-a5.txt`.
- Partly disclosed: the tail correction (SCORECARD.md:1573-1584) now says "D5 checks scores only" and that the pinned numbers are "declared by the lane". The table note (:17-19) and the tool still say "closure-admitted" and "observed".
- Consequence: "held 4 of 4" shows the table agrees with an earlier lane sentence, and that round 1 is not misquoted. It does not show agreement with the round records or the closures. My cell checks in this report are manual and are not counted.
- Smallest fix: (a) relabel the reference "lane round-24 declaration (targets)" in the tool, in contract A5 and in the table note; (b) if the claim should test more, add to D5 that each `round N` in Last change has a `Round N` heading at REV, that each backticked repo path in Evidence exists at REV (`git cat-file -e REV:path`), and that rows with unknown axis names fail.

### L1. Low. The table note still says "closure-admitted"

- SCORECARD.md:17-19: "The scores above are the ones the closure-admitted round-24 section records". The closure states numbers only for calibration (lesson:68, "Score 5 → 5") and coverage (lesson:88, "Score 6 → 6"). For operability, depth, freshness and adjacency it writes "unchanged" (lesson:106-109). The four numbers come from the declaration (28b79d3d:1504).
- Partly disclosed: the tail correction (SCORECARD.md:1582) says to read it as "declared by the lane, with calibration and coverage confirmed by the closure". The table note itself is unchanged.
- Also unreconciled: SCORECARD.md:620-623 (round 12: the top table is "left as filed") and :1079-1080 (round 17: the top table is "historical, not the active score/selection register"). The table is now the active register and no note says so.
- Smallest fix: rewrite :17-19 to the accurate provenance, and state that the table is the active register from round 25, superseding the round-12 and round-17 notes.

### L2. Low. The operability cell's evidence does not show the move, and its 7 rests on a rejected round

- Round 13 closed rejected-harmed: coverage and adjacency harmed, operability improved (MANIFEST `.rounds[327]`). The 7 survives because round 14, admitted, holds it (SCORECARD.md:744, "Operability's independently verified F01/F02 improvement remains **7**"; :793; `.rounds[339]` operability unchanged).
- The cell cites the census selftest, 134 cases (true, see V4), and "held 7 in every round table since round 13". The move itself was the round-13 rubric (SCORECARD.md:685-691: two named defects absent, honest controls hold, witnesses reproduce). A selftest count does not evidence that.
- "Every round table" is true for rounds 13 to 20, which have operability rows (:696, :793, :875, :984, :1117, :1151, :1220, :1260). Rounds 21 to 25 state the 7 only in prose (:1303-1304, :1343, :1361, :1429, :1456, :1527-1528, :1548), because those rounds have no operability row.
- Smallest fix: cite the round-13 rubric and the round-14 closure in the operability cell, and write "held in every round record since round 13 (prose from round 21)".

### L3. Low. The lesson overstates "every later round"

- corpus/lessons/round-25.md:97-98: "while every later round holds coverage 6, operability 7, depth 5". Rounds 2 to 11 have no scalar score. Coverage and depth stayed at 5 and 4 until round 12, and operability at 6 until round 13 (SCORECARD.md:613-616, :696).
- Partly disclosed: the appended correction (round-25.md:101-110) says the bullet "was true when written". It was not true for rounds 2 to 11.
- Smallest fix: write "from round 12 (coverage, depth) and round 13 (operability) onward".

### L4. Low. The Move log holds only the round-1 row

- SCORECARD.md:21-25 has one row (round 1). The Last-change moves (round 12 coverage and depth, round 13 operability) appear only in the round tables.
- Smallest fix: add the three moves as rows, or label the log "round 1 only".

### L5. Low. Judgement-shaped rows give a number without saying what kind of number it is

- AXES.md:52-55: for a subjectively moved axis the row "carries the verdict and the reviewer pointer instead of a number ... and the row says which one it is". Calibration and adjacency are the two axes whose AXES.md definitions are judgement-shaped (calibration: "gaps named honestly"; adjacency: "cross-domain awareness"). Their rows give numbers without saying whether the number is measured or reviewer-held. Adjacency has no reviewer pointer at all.
- Smallest fix: one clause per row, such as "reviewer-held; closure r24 unchanged", or the measured basis.

### L6. Nit. The saturation line is dated

- SCORECARD.md:637-641 (declared round 12): "owned axes sit at 6 and 6". Operability has been 7 since round 13. This is a dated declaration, not a table cell. Re-declare it when the table next changes.

### L7. Nit. D5 ignores rows with unknown axis names

- tools/mori-routed-r24.py:718-720 stores every row, and :722-741 checks only the six named axes. A row such as `| fleet | 9 | ... | round 1 |` would pass.
- Smallest fix: reject any row whose axis is not one of the six.

## What checked out

- **V1 Scores.** Each cell matches the record in the table above. Round 14 keeps coverage at 6 after round 13's withdrawn 7 (SCORECARD.md:743, :757).
- **V2 Last change, score reading.** All six agree with the round tables and closures, as shown above. Round 12's depth and coverage rows: SCORECARD.md:613 and :615. Round 13's operability row: :696.
- **V3 Pointers, all resolve at e0e33c1.** `corpus/knowledge/observability-surfaces-r2.md` and `corpus/knowledge/system-pressure-r24.md` exist. `corpus/README.md:404` is the heading "## Round21 correction". Lesson lines 68, 88 and 106-109 carry the quoted text. `corpus/lessons/round-12.md:184` and SCORECARD.md:658 support the calibration hold. PROVINCE.md:12-15 refuses dispatch and OS state; PROVINCE.md:335-344 makes harness configuration operator-owned. `tools/mori-job-runway.py:14-17` says it never writes a settings file.
- **V4 Live runs in a private clone (the fleet root was read, not written).**
  - `bash tools/mori-census.sh --selftest` at `07a31ae`: `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)`, exit 0. `git diff --stat c725aa37 HEAD -- tools/mori-census.sh` is empty, so the census has not changed since the round-24 measurement.
  - `MORI_SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin bash tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json` at `07a31ae`: exit 1, with `MORI_DRIFT:` listing changed findings and surfaces. The freshness pointer's "still red" holds at that time.
  - `python3 -I -B tools/mori-routed-r24.py --repo <clone> --rev e0e33c1`: items 4, held 4, mismatches 0, exit 0. At `--rev 28b79d3d1b76824f0c825aabe6cb6c5dc49961bf`: mismatches 4, exit 1.
- **V5 Tip movement.** `07a31ae` to `e0e33c1` touched no Axes row and no tool. `git diff 07a31ae e0e33c1 -- SCORECARD.md` changes only lines after 1547.

## Residual risk and verification gaps

- The drift result is live and will change. The committed record (corpus/README.md:365) says "red debt without a re-pin", which is older.
- The four "unchanged" values (operability, depth, freshness, adjacency) rest on a chain of admitted closures (rounds 14 to 22). I read their verdicts. I did not re-derive the rubric values behind them.
- I did not re-run the round-12 counting commands (coverage rows 9 to 23, depth source counts). The coverage and depth moves rest on the round-12 record.
- I did not run mutation tests and did not read SHONEN.
- MANIFEST rows for rounds 1 to 11 carry no verdicts. The "No scalar score" reading comes from the SCORECARD round text.
- This verdict covers `e0e33c1`. Later commits could change the table; re-check with the history command below.

## Commands for the main agent

```
git --no-pager -C <lane> log --format='%h %s' -L8,15:SCORECARD.md      # only e68855d changes rows 8-15
python3 -I -B tools/mori-routed-r24.py --repo <lane> --rev <tip>        # held 4, mismatches 0, exit 0 at e0e33c1
python3 -I -B tools/mori-routed-r24.py --repo <lane> --rev 28b79d3d1b76824f0c825aabe6cb6c5dc49961bf   # mismatches 4, exit 1
bash tools/mori-census.sh --selftest                                    # in a clone: PASS (134 cases ...), exit 0
```

## Tool installs and records

No tool was installed or updated. Read-only git subcommands ran in the lane (`log -L`, `show`, `grep`, `cat-file`, `rev-parse`, `diff --stat`). The lane was fetched into a private clone at `/fast/scratch/hyaku/mori-r25/w2-ReviewAxesTable`; nothing was written back. Python 3 standard library ran the lane's routed tool, and the census script ran in the clone. The clone and three scratch outputs were deleted after this report was written.
