# mori round 29 — claim contract (attempt 1, L1 MoriR29)

Entering tip `7118f320a5ef18d20c1e361eff77db0e1a97b2d6` (round-28 verifier spot-check; round 28 admitted). Written
before any round-29 implementation. Targets, not results. A declared claim is never withdrawn; a miss is reported as
a miss. Pinned fleet revision for closure-record inputs: `63729047644f839fe4c8cc97abd0d8bf741a5787` (fleet
`MANIFEST.json` holds mori rounds 12–28 with verdicts).

## Why these two claims

- Lowest-scoring active axes in the standing table are depth, freshness and calibration (5 each,
  `SCORECARD.md:12-14`). Calibration was last claimed in round 25. C1 works calibration: "SHONEN.md/SCORECARD
  entries match observed repo state" (`AXES.md:15`).
- C2 is the round-28 spot-check routed defect 2 (`corpus/lessons/round-28-verifier-spotcheck.md:126-127`): two
  breach shapes of rules A2-07 and A2-10 have no frozen case. It works operability (7).
- Causally separable: C1 touches only the `## Axes` table of `SCORECARD.md` (and its counter); C2 touches only a new
  case file under `tools/fixtures/mori-oom-killers/`, its counter and, only if a judged tool error requires it,
  `tools/mori-oom-killers.py`. Neither counter reads the other claim's files.
- Sourced claim: C2. The case writers and the fix rest on SOURCES rows opened this round (S153 onward) for the
  earlyoom dry-run/version log lines and the journal monotonic-timestamp field; the round-29 lesson `## Gate` holds
  each row's URL, access time, sha256 and located quote, and the case file's top-level `sources` key cites them.

## C1 — calibration (score 5, tied lowest): the standing Axes table agrees with the admitted closure record

Statement: at the landed tip the C1 counter prints `mismatches=0` and `C1=met`, exit 0, over the six rows of the
`## Axes` table of `SCORECARD.md`.

A mismatch is any of, per axis row (the counter enumerates all six rows; full set):

1. **Stale closure.** Let R be the largest round N in 12–28 such that the pinned fleet `MANIFEST.json` records mori
   round N with verdict `admitted` and the lane file `corpus/lessons/round-N-verifier-spotcheck.md` at `<rev>` holds
   a per-axis table line `| <axis> | improved |`. If R exists, the row must cite `round-R-verifier-spotcheck.md`.
2. **Unadmitted last change.** The row's `Last change` cell opens with `round N`; for N ≥ 12 the pinned MANIFEST
   must record mori round N as `admitted`.
3. **Dead pointer.** Every backticked `path:L` or `path:L-M` token in the row names a file that exists at `<rev>`
   with at least max(L, M) lines.
4. **Score without basis.** The row's score differs from the score at `7118f320` while the row cites no
   `round-N-verifier-spotcheck.md` with N an admitted round whose per-axis line for that axis reads `improved`.

Counting command (committed bytes only; exit 0 met, 1 unmet, 2 bad revision or missing input):

```sh
bash /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-29/count-c1.sh <lane-rev> 63729047644f839fe4c8cc97abd0d8bf741a5787
```

The counter is written in wave 1 and committed before any edit of the Axes table. Before: measured at `7118f320`
when the counter lands (`evidence/c1-before.txt`). Declared after (at the landed tip): `mismatches=0`, `C1=met`,
exit 0. Score policy (binding on the fix, not on the counter): a score cell changes only where an admitted closure
states the new number or the admitted round's declaration proposed it and its closure verdict is `improved`;
otherwise the row records "improved (closure round N), score held" with the closure pointer.

## C2 — operability (score 7): blind frozen cases for the A2-07 and A2-10 shapes routed by the round-28 check

Rule text: `.ufo/waves/round-27/contract.md:47-58` (A2-07, A2-10) and `.ufo/waves/round-26/contract.md:152-200`.

Statement: `tools/fixtures/mori-oom-killers/cases-a2-r29.json` is assembled from cases written by eight blind seats
(four per rule; every case carries an `author` key naming its seat) that read no tool source, no tool output, no
critic or design report and no lesson; it is committed before the L1 runs the tool on it; it is unchanged after that
commit; and at the landed tip the C2 counter prints `C2=met`, exit 0: at least 12 cases, at least 6 per rule, each
rule's cases by at least 3 distinct authors, each case pinning its rule's required field (A2-07:
`earlyoom.actions.sigterm`, `earlyoom.actions.sigkill` or `earlyoom.dryrun_send_lines`; A2-10:
`earlyoom.scope_complete`, `earlyoom.actions.sigterm` or `earlyoom.earlier_invocation_send_lines`), tool self-test
`PASS N/N` on the new file, `PASS 30/30` on `cases-a2.json` (blob equal to its `d21b8bd3` blob) and `PASS 32/32` on
`cases.json` (blob equal to its `fc09f96c` blob).

Counting command:

```sh
bash /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-29/count-c2.sh <lane-rev>
```

Committed before the case file. Before: at `7118f320` the new file is absent, `C2=unmet`, exit 1
(`evidence/c2-before.txt`); the tool's tally on the frozen file at the freeze commit is recorded as the substantive
before (`evidence/c2-freeze-selftest.txt`). Declared after: `C2=met`, exit 0.

Mismatch judging (carried from round-28 amendment A2, fixed before any tool run): a non-author judge seat of the
falsify wave reads only the rule text, the case and the tool's output for that case and rules `tool error`, `case
error` or `unclear text`. On `tool error` the L1 may change the tool, never the case file; the change must keep `PASS
32/32` and `PASS 30/30` and may not turn any `KILLER_ACTED` of either older file into another verdict. `case error`
or `unclear text` on any case is a C2 miss, reported as one. A case is never dropped, renamed or re-tagged after the
freeze commit.

## Held, not claimed

Depth 5, freshness 5 (round 28 proposed 6; C1 decides the row), coverage 6, adjacency 6 observed. No retirement,
waiver, exploratory claim or promotion. No-harm check: lane retention scan unallowlisted metric at the landed tip
must not exceed its value at `7118f320` (`python3 -I -B tools/mori-retention-gate.py scan --repo <lane> --rev <rev>
--policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json`); the
round-26 and round-28 self-tests keep their tallies.

## Routed hygiene (round-28 spot-check §6; never a counted claim)

1. Late round-28 outputs: each re-verified in wave 1 and committed as evidence or disposed, named in the lesson.
2. Blindness (lesson M6): wave 1 has no seat that reads or runs the tool; a check that fails on the round-28 freeze
   state is the mined mistake's fix.
3. Gate tables record reject decisions met during source work (new QUALITY criterion).
4. Tip receipts: the last batch adds only receipts and each receipt header names the parent it measures and says the
   landed tip adds only receipt files.
5. Census count: corrected by an appended note in `corpus/lessons/round-28.md` (ten W04, four new: S147–S150).
6. Carried debt (MutCountC1 F1/F2/F3/F6/F10, S146 teaches, reader-sweep citations, old `used-by`, r25 R1/R5):
   inventoried, carried by name unless a wave-1 item closes one.

## Amendment A1 (round 29, before the C1 counter lands and before any Axes-table edit)

Raised by wave-1 CriticC1Design F1–F6 (`w1/CriticC1Design.md:147-175`), CriticScorePolicy (kind 4 vacuous; freshness 6
unprovable) and AxisCalibration/AxisDepth (rounds 19–22 have no lane spot-check file; round 12 has no per-axis table).
Every change makes C1 harder to meet; all six rows stay counted; no data existed when it was written. It replaces
mismatch kinds 1, 2 and 4, extends 3 and adds 5:

- **Closure authority:** the pinned fleet MANIFEST. Imp(a) = { N in 12..28 : the mori round-N entry has verdict
  `admitted` and `verdicts.a == "improved"` }; R(a) = max Imp(a). Cite(N) = the lane file
  `corpus/lessons/round-N-verifier-spotcheck.md` when it exists at `<rev>`, else the literal token
  `MANIFEST.json@63729047 mori round N`.
1. **Stale closure:** if R(a) exists the row carries a backticked `Cite(R):L` token (lane file) or the literal token
   (no lane file). When Cite(R) is a lane file with a per-axis table, line L must match `^| a | improved |`.
2. **Last change:** the cell opens with `round N` (else mismatch); N is an admitted round, and N ≥ R(a) when R(a)
   exists. If the cell carries `(X → Y)`, Y equals the score cell. A held score is written `round N (improved, score
   held)`.
3. **Dead pointer:** every backticked token containing `/` or ending in `.md`/`.json`/`.py`/`.sh` names a file that
   exists at `<rev>`; `path:L`/`path:L-M` also need max(L, M) lines.
4. **Score without basis:** the score cell is an integer 0..10, or `unprovable-but-better` with a named non-author
   reviewer citing an admitted closure that records that verdict. A numeric score differs from its `7118f320` value
   only if the row cites `Cite(N):L` for an admitted N whose line L states `X → Y` for that axis, X = the `7118f320`
   score, Y = the new score; either direction. An `improved` verdict alone, or a number a declaration proposed, is
   never a basis.
5. **Closure disagreement:** for every N in 12..28 with a lane per-axis table, each `| a | <verdict> |` line equals
   the MANIFEST `verdicts.a` for round N.

The counter prints one line per row (axis, score, basis, R, kinds hit), then `mismatches=<n>` and `C1=met|unmet`.
Score policy (C1 above): "or the admitted round's declaration proposed it" is deleted. Uncounted residual named in
the lesson: the truth of each row's evidence prose beyond its pointers (a wave-2 non-author read).

## Amendment A2 (round 29, before the C2 counter lands and before the L1 opens any case draft; CriticRoutingCoverage F1, F3, F4, F6, F7)

Every change makes a claim harder to meet or corrects a misstatement; nothing is narrowed.

- **C1 kind 2b:** when the Last change cell states `(X → Y)` for round N, the pinned MANIFEST `verdicts.a` of mori
  round N must be `improved` (catches `round 14 (6 → 7)` against a round-14 `unchanged`).
- **C2 shape lines (counted, rule-text terms):** the counter prints `shape_a207=<cases>/<authors>` = cases of rule
  A2-07 whose counted scope (bounded: records stamped at or after a non-zero ActiveEnterTimestampMonotonic of an
  active unit; unbounded: every stamped record of an active unit whose ActiveEnterTimestampMonotonic is missing or 0)
  holds at least two version lines, one segment between version lines holding `dryrun mode enabled` and another
  segment without it holding a send line; and `shape_a210=<cases>/<authors>` = cases of rule A2-10 holding a send
  record without a numeric `__MONOTONIC_TIMESTAMP` while either the unit is active with ActiveEnterTimestampMonotonic
  missing or 0, or the unit is not active. `C2=met` additionally requires each shape ≥ 2 cases from ≥ 2 authors.
- **C2 statement, counted vs disclosed:** the counted after-value is the counter's `C2=met`. "Eight blind seats",
  "read no tool source …" and "committed before the L1 runs the tool" are process conditions, each reported with its
  evidence (writer files-opened lists, `check-blind-wave.sh` receipt at the freeze commit, commit order); a failed
  condition is reported as a C2 defect, never dropped.
- **Correction (F6):** "wave 1 has no seat that reads or runs the tool" is false as written: BuildCountC2 runs the
  tool's `--selftest` on the two older case files (marker lines only). No wave-1 seat reads tool source.
- **Correction (F7):** the case writers fetch upstream sources themselves; rows S153 onward are opened in the same
  wave by source scribes, so the sourced claim rests on those rows through the lesson Gate and the case file's
  `sources` key, not through the writers' reading.

## Amendment A3 (round 29, before the C2 counter lands; CriticC2Design F1–F3)

- **Provenance (F2, counted):** every case of `cases-a2-r29.json` must equal (canonical JSON, keys sorted) a case in
  the first fenced JSON array of its author's committed report `.ufo/waves/round-29/w1/<author>.md` at `<rev>`, and
  every case of those eight reports whose author is listed must appear in the file (no selection). The counter prints
  `provenance=<matched>/<cases> unselected=<n>`; `C2=met` needs all matched and `unselected=0`.
- **Field map (F1):** the round-28 A1 map (A2-07 pins `earlier_invocation_send_lines > 0`) belongs to the round-28
  file and is kept there by `PASS 30/30`. The round-29 map pins the in-scope fields because the routed A2-07 shape is
  inside the counted scope; this is a different file, not a relaxed one.
- **Shared directory (F3):** critic reports sit in the writers' `w1/` directory again; the blindness evidence is the
  `check-blind-wave.sh` receipt at the freeze commit (no non-writer report cites tool lines or tool output) plus each
  writer's files-opened list.

## Amendment A4 (round 29, before the C2 counter lands and before the L1 opens any case draft; CriticC2Design residuals R1–R3)

- **Decisive pins (R1):** a case counts toward `shape_a207` only if its `expect.fields` pins `earlyoom.actions.sigterm`
  or `earlyoom.actions.sigkill` as an integer above 0; toward `shape_a210` only if it pins one of
  `earlyoom.actions.sigterm`, `earlyoom.actions.sigkill`, `earlyoom.actions.escalations` or
  `earlyoom.earlier_invocation_send_lines` as an integer (any value).
- **Fixed writer set (R2):** the writer set is exactly CaseA207a–d and CaseA210a–d; `unselected` counts every case
  of every one of those reports present at `<rev>`; a report absent at `<rev>` is printed as `writer_absent=<name>`
  (a reported death, not a pass condition by itself).
- **Blindness as a miss (R3):** the `check-blind-wave.sh` run at the freeze commit on `.ufo/waves/round-29/w1` with
  writer regex `^CaseA2(07|10)[a-d]\.md$` must print `blind_violations=0`; otherwise C2 is a miss, reported as one.
- Carried, not counted (R4): a full-output differential between the freeze-time tool and any changed tool on every
  case input is produced as a wave-2 receipt and judged; an A2-07 shape with a non-active earlyoom has no blind
  writer this round and stays named debt.
