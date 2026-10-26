# Mo50bConnCrossClaim — cross-claim and cross-round pattern finding (round 50, attempt 2, wave a2w1)

Seat: Mo50bConnCrossClaim (connector, leaf). Lane: mori-shokunin.
Landed tip read: `487941b9395e89678af0053cc443cdb49cdee6e3`; entering tip `7197160b927f04db294c9553fb48fadcc7a3f4e3`; freeze `950e99be6757a52b00e9eb70ae1a1a7bbe2ea379`.
Method: read-only. Read `contract.md`, `count-c1.py`, `count-c2.py`, the `## Mistakes` tables of
`corpus/lessons/round-45.md` … `round-49.md` and all five verifier spot-checks, plus targeted `git show` /
`git log -S` / `git diff` over lane history and a JSON parse of the fleet `MANIFEST.json` at the pinned fleet
revision `e014499613f63f8a467821219b0296121119ca53`. Ran the two frozen counters once each at the landed tip
(TMPDIR under my scratch). No lane file edited; no clone; no subagents. All paths below are relative to
`/home/vgpnk/Projects/shokunin/mori-shokunin` unless absolute.

## 1. The shared failure class

Every recurrence in scope is one class: **self-description drift** — a written claim about observable state
(a registry pin, a selftest tally, a report count, a Last-change cell) diverges from what the instruments,
the fleet record, or the seat's own receipts actually show at the committed revision, and no gate that runs
automatically at the boundary compares them. Each instance was found one round late, by an outside party
(the hyaku closure verifier) or by a seat's manual cross-check, never by an in-lane scheduled check.

Three sub-classes, same mechanism (write once, never re-derive):

1. **Pin/tally drift** — a pinned selftest tally or digest no longer matches the tool at the same revision.
2. **Count drift** — a numeric claim in prose (report/lesson/LOG) is not re-derived from its own cited command.
3. **Record drift** — a standing table (SCORECARD Axes, SHONEN) lags the closure record it summarizes.

## 2. Recurrence table

| class | rounds | instance | criterion that should have caught it | why it did not |
|---|---|---|---|---|
| pin/tally | r45 | `SKILL.md:184,190,191,194` pinned tallies/digests the committed tools do not have; closure graded calibration **harmed** (`corpus/lessons/round-45-verifier-spotcheck.md:50-68`) | QUALITY 40 (tally universe recomputed from delivered artifacts); the r45 frozen counter itself | the counter did row-wide substring tests with no runtime measurement; QUALITY 40 was not applied to registry cells |
| pin/tally | r46 | r45's repair tool `count-repins.py` still green when stale-pin strings sit in another cell of the same row (`corpus/lessons/round-46.md` M1) | CORPUS.md "A fix is shown able to fail" | the fix was shown able to fail only as a text predicate; no semantic-cell parse, no live re-measurement |
| count | r45/r46 | "29/29" freeze-manifest tally vs measured 27 OK (`round-45-verifier-spotcheck.md:33-37`; `round-46.md` M2) | CORPUS.md "A count carries its command" | the count was copied between report and LOG; nobody re-ran the cited `sha256sum -c` at filing |
| pin/tally | r47 | `SKILL.md:912` pinned `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` from round 40 while the tool printed 22 since the r41 freeze (`corpus/lessons/round-47.md` M1) | QUALITY 40 (recomputed tallies) | "nothing ran it on registry cells" — the criterion existed, no instrument implemented it for SKILL.md |
| pin/tally | r48 | `SKILL.md:168` pinned a truncated sha256 `c39e5a73…` for the r14 harness; no file in the tree carries it (`corpus/lessons/round-48.md` M4) | QUALITY 123 (re-run from committed bytes) | it covers tallies and full digests, not truncated digests; v3 rule R6 closed this hole only after the closure found it |
| count | r49 | report said "48 wave-1 reports"; 47 on disk at filing; lesson and LOG still carry the wrong number (`round-49-verifier-spotcheck.md` D-c) | QUALITY 77 (sweep every mention) / 117 / 124 | the count was plan prose; no instrument re-derives lesson/LOG prose counts (confirmed again by `Mo50bScoutMistakeSweep.md` S49-c: still OPEN) |
| pin/tally | r49 | wave-1 dispatch told `Mo49ScribeSkillRows` to pin `C1_SELFTEST pass=42`; the frozen counter prints 44 (`corpus/lessons/round-49.md` M5) | none | "the plan text was not run"; a seat caught it manually in-round |
| record | r29 → r50 | r29 M1 is the same SCORECARD Axes-table drift (cells cited no closure later than round 24; `corpus/lessons/round-29.md:26-29`); fixed by a round-scoped `count-c1.sh` that was then retired, and the drift returned in r50 | r29's own counter proved the shape works | the counter was a one-round artifact, never registered as a standing gate; nothing re-ran it at r47/r48/r49 landings |

## 3. The latest recurrence, observed

The r50 entering state is the same class at both surfaces C1 measures.

**(a) SHONEN pins.** `git show`/`git diff` over `SHONEN.md`:

- `91fbbc2a` (round-48 wave 2) introduced `python3 tools/mori-pin-check.py --selftest` `(60/60)` and
  `python3 tools/mori-unlanded-check.py --selftest` `(13/13)`. At round 48 that was true
  (`w2/R48SimpV3.md:45` → `PIN_CHECK_SELFTEST pass=60 fail=0`).
- `git diff 14c5110d 43d84666 -- SHONEN.md` and `git diff 43d84666 7197160b -- SHONEN.md` are both **empty**:
  SHONEN was not touched at the round-49 landing or after.
- Round 49 grew the tools: `SKILL.md:938` moved `pass=60` → `PIN_CHECK_SELFTEST pass=114 fail=0` at data commit
  `64c2d5fc` (`git log -S "PIN_CHECK_SELFTEST pass=114" -- SKILL.md` → `64c2d5fc`), and the unlanded check grew
  to 17 arms (LOG round-49 entry: "selftest 114 … (17 arms)").
- So from the r49 landing until the r50 entering freeze, SHONEN asserted 60/60 and 13/13 while the tools printed
  114/114 and 17/17. The r49 verifier flagged the adjacent form problem (D-d: tallies prose-only, unverified by
  it) but did not run the tool, so the value drift rode through closure.

**(b) SCORECARD Axes cells.** `git show <rev>:SCORECARD.md` over the standing `## Axes` table: the Last-change
cells are byte-identical at `dd17d927` (r47 landing), `14c5110d` (r48), `43d84666` (r49) and `7197160b`
(r50 entering): coverage `round 26`, operability `round 31`, depth `round 31`, freshness `round 28`,
calibration `round 25`, adjacency `round 19`. My parse of the fleet `MANIFEST.json` at
`e014499613f63f8a467821219b0296121119ca53` (rounds 44–49, `verdicts` per axis) shows the latest admitted
`improved` per axis is 47 / 47 / 49 / 28 / 49 / 19. Windows: calibration stale since the r46 landing, coverage
and operability since r47, depth since r48 — three consecutive landings wrote closures and no in-lane check
compared the table.

**(c) The frozen counter catches it — once.** Observed:

```
$ python3 .ufo/waves/round-50/count-c1.py 7197160b927f04db294c9553fb48fadcc7a3f4e3   # control receipt, evidence/control-c1-do-nothing.txt
… mismatches=6 … (4 axis cells + both pins) → C1=unmet, exit=1
$ python3 .ufo/waves/round-50/count-c1.py 487941b9395e89678af0053cc443cdb49cdee6e3   # my run, TMPDIR=scratch
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=487941b9…, exit 0
```

## 4. One standing check that would have caught the latest recurrence

**A single self-description reconciler, run by the L1 at every landing from committed bytes, before the report
is filed** (one tool, three passes):

1. **Pin pass** — parse every selftest/tally pin in `SKILL.md` decision-table cells and `SHONEN.md`, re-run each
   pinned command in a `git archive` of the landed revision, compare prefix/pass/fail (this is
   `tools/mori-pin-check.py` generalised off SKILL.md onto SHONEN, plus C1's pin half).
2. **Record pass** — compare SCORECARD `## Axes` Last-change cells against the fleet `MANIFEST.json` at the
   **latest admitted mori closure** (a parameter read from the fleet, not a frozen constant).
3. **Count pass** — re-derive every numeric claim in the round's report/lesson/LOG from its own cited command
   and fail on disagreement (the r45 29/29, r49 48-vs-47, r49 M5 family).

Exit non-zero on any mismatch; the receipt is committed with the round. It would have caught the r50 recurrence
at the r49 landing (pass 1 red on 60/60 vs 114; pass 2 red on 31/25 vs 49), the r47/r48 pin drifts at their
own landings, and the r45/r46/r49 count drifts at filing.

## 5. Is C1's counter the standing check? — no, it is only a one-round measurement

C1's counter is the right *shape* (live pin re-run + MANIFEST comparison) and it did catch this recurrence, but
as frozen it is a one-round claim, not the standing check:

1. **Frozen expected values.** `count-c1.py:41,43` hard-code `THROUGH = 49` and
   `FLEET_REV = "e014499613f63f8a467821219b0296121119ca53"`. Run at the round-51 landing it still asks "latest
   mori round ≤ 49", so new closures cannot move its targets — it would print `C1=met` against today's cells
   while rounds 50+ closures make them stale. A drift detector whose expectations never advance detects nothing
   new.
2. **Single-file surface.** The contract's named limits state it: "a pin split across lines or outside backticks
   in another file is not enumerated (the hidden scan covers SHONEN.md only)". The r45–r48 pin-drift home is
   `SKILL.md`; C1 covers only the two SHONEN pins and the six Axes cells the contract happened to name. K4 is
   closed "for SHONEN.md only; the rest stays routed" (contract, routed-defect carrier 7).
3. **No count re-derivation.** C1 checks pins and cells, not prose counts — the r45/r46/r49 count-drift
   sub-class passes it unchanged.
4. **No standing schedule.** It is a wave-claim counter with a kill rule; nothing runs it at landings. The
   round-29 precedent is exact: r29 built a counter for this same Axes-table drift, proved it red→green, and
   the drift recurred five rounds later because the counter was round-scoped and retired rather than
   registered and re-run (cf. `mori-pin-check.py`, which *is* registered in SKILL.md and *did* keep catching
   SKILL.md pins — the asymmetry is the evidence: registration is what makes a check standing).

The standing check is the generalisation of C1's two halves plus a count pass, parameterised and registered —
C1's counter is its round-50 frozen instance, valuable as feasibility proof (its do-nothing control printed
`mismatches=6` exactly as the recurrence predicted), not as the check itself.

## 6. Contradictions and risks

- **Frozen vs living:** the counters, predicates and kill rules are frozen for this round; the standing check is
  a proposal for the L1/operator only. Stated, per the wave rules, not actionable here.
- **Verifier limits:** the r49 verifier explicitly did not run lane gates (D-d), so "the outside check will
  catch it" is not a reliable backstop — the r49 closure *noticed* the prose-only form and missed the 60-vs-114
  value. My recurrence table's "captured-by: none" column is the load-bearing fact.
- **MANIFEST trust:** the record pass trusts the fleet-written MANIFEST (same limit C1 names); a fleet-side
  error would propagate. Low risk in practice; named for honesty.
- **Scope of claim 2:** SHONEN pins were stale for one closure boundary (r49 landing → r50 freeze), not since
  r48's landing; "since round 48" in the contract refers to when the pins were *written*. The Axes cells were
  stale for up to three closures (calibration). Both readings are drift under the same class; the windows
  differ and I state them separately rather than smoothing them into one scalar.

## 7. Findings

- **HIGH — `.ufo/waves/round-50/count-c1.py:41,43`** (`THROUGH = 49`, `FLEET_REV` constant): the counter is a
  one-round measurement; without generalisation + registration the drift class it just caught recurs (it has
  recurred in r29, r45, r46, r47, r48, r49). See §5.
- **HIGH — the standing check does not exist**: no instrument runs the pin/record/count reconciliation at
  landings; every historical catch was one round late and outside-party (`round-45-verifier-spotcheck.md:50-68`,
  `round-46.md` M1/M2, `round-47.md` M1, `round-48.md` M4, `round-49-verifier-spotcheck.md` D-c/D-d). Proposal in §4.
- **MED — `corpus/lessons/round-49.md:212` and the `LOG.md` round-49 entry still carry "48 reports on disk"**:
  the routed defect-3 correction (48-vs-47) is not yet appended; observed `grep` hits at `round-49.md:7` and
  `:212`. Consistent with `Mo50bScoutMistakeSweep.md` S49-c (OPEN).
- **MED — dispatch text carries unverified numbers** (r49 M5, `pass=42` vs 44): no criterion runs plan/dispatch
  prose against the instruments it cites; a standing check's count pass covers reports/lessons/LOG but not the
  dispatch spec unless the L1 includes it.
- **LOW — `variants=26` vs 27 `variant` lines** (r49 D-f): mechanism reported by `Mo50bScoutMistakeSweep.md` S49-f
  (`.ufo/waves/round-49/count-c1.py:304` counts `len(results)-1`), not re-verified by me; documentation still
  unwritten; contract carrier 6 names it.
