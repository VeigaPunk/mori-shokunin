# Mo52CritC1Scope — attack on the K4 scope decision (round 52 wave w1)

Seat: `Mo52CritC1Scope` (critic). Lane: mori-shokunin. Reviewed revision: data commit
`8524904adb25e44f24d9f25aac7eae909625c18c` (entering `4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d`).
All reads are read-only over committed bytes; the working tree's tracked files equal the data commit
(`git diff 8524904a HEAD -- SCORECARD.md SHONEN.md corpus/QUALITY.md corpus/README.md` empty).

Assignment: attack the K4 scope paragraph in `.ufo/waves/round-52/contract.md:24-28` — is it honest, and is it
consistent with round-50 closure routed defect 3 (`corpus/lessons/round-50-verifier-spotcheck.md` §5 item 3)?
Find (a) any current-tense self-claim with a tally outside the two living files (`corpus/QUALITY.md`,
`corpus/README.md`) and SHONEN (confirm SKILL.md is covered by `tools/mori-pin-check.py`), and (b) any living
pin that is in fact a dated record.

## 0. The K4 scope paragraph (contract.md:24-28, verbatim)

> K4 scope, decided before data: LOG.md and the SCORECARD round sections are dated records (each tally sits under a
> `## Round N` heading and reports what was measured then); a tally there is history, not a current claim, so K4
> does not run them. QUALITY.md criteria carry `Check:` commands that a reader runs today, and README coverage rows
> carry the command that shows the bounded advance; those are the living pins K4 runs. The house rule for a stale
> check is supersession by a later row (QUALITY 111 supersedes 109's check), never an in-place rewrite.

## 1. The factual premise is true; the inference from it is false

Structural check (my own scan over committed bytes, pattern = `SELFTEST | pass=\d+ fail=\d+ | C[12]=met|unmet |
mismatches=\d+ | located=\d+ | (\d+/\d+) | [\d+/\d+]`, nearest preceding heading classified as round/date-name by
`(?i)round[- ]?\d | 20\d\d-\d\d-\d\d`):

- `LOG.md`: 74 tally-bearing lines; **0** before any heading, **0** under a non-round/date heading. (The first
  tally block at `LOG.md:14-18` sits under `## round 1`.) So "each tally sits under a round/date heading" is
  literally true for LOG.
- `SCORECARD.md`: 105 tally-bearing lines; **0** before any heading, **0** under a non-round/date heading
  (capability tables sit under `## Capabilities (round 12 demonstrations)` etc.). Same for SCORECARD.

The premise is therefore verified. The conclusion "a tally there is history, not a current claim" does not follow,
and is falsified by a concrete line inside one of the excluded sections:

**Counterexample — `SCORECARD.md:1070-1071` (inside `### Round-17 measured claims (L1, before fresh falsification)`,**
**a section the K4 decision classifies as history):**

> Depth5/freshness5/adjacency6 held unchanged. Existing census125/125,
> oracle28/28, r13 24/24, r14 44/44 and r15 63/63 with frozen red34/34 pass;

"Existing census125/125" is a present-tense assertion of current instrument state with a tally. It is not a claim
that something was measured *then* — it asserts what holds *now*. It went stale inside the same round, before the
round closed: later round-17 logs record the census selftest at 134/134 (`LOG.md:1229`, "the oracle-corrected
census selftest passed134/134"), and round-19 re-verification again records 134/134 (`LOG.md:1379`). The line is
today an un-run, un-corrected, false present-tense tally claim. It is outside `## Axes` (arm A), outside the
SHONEN boxes (arm B), outside `corpus/QUALITY.md`/`corpus/README.md` (arm C), and outside the locator arm (arm D).
Nothing in the frozen counter reads it.

This is exactly the staleness class K4 exists to catch, and the K4 decision's stated rule ("a tally there is
history") is what excludes it. The rule is a heuristic that misclassifies present-tense assertions that happen to
live under a round heading.

## 2. Consistency with round-50 routed defect 3

Defect 3 (`corpus/lessons/round-50-verifier-spotcheck.md:179-181`) says, verbatim: "Also take K4 beyond SHONEN
**(tally pins in QUALITY, README and LOG)**." Round-51 carried it unchanged (`round-51-verifier-spotcheck.md:181-182`,
item 4: "K4 beyond SHONEN, is still open. The lane routes it to round 52; carry it."). Round-52's K4 covers
QUALITY + README and drops LOG on the dated-record rationale.

The delivered machinery is correct on what it does run: at the data commit, arm C enumerated 7 living pins
(QUALITY 885, 909, 1360; README 607, 608, 727, 728), ran the three current ones to matching tallies, and marked the
four stale ones superseded — `C1=met items=42 living=7 superseded=4 mismatches=0` (`evidence/c1-at-data.txt:44`).
That satisfies the *quantitative* intent — every standing command-tally pin in the two living files is checked or
superseded.

But the *named target* LOG is dropped, and the rationale given for dropping it is the one falsified in §1:
- the exclusion is justified by file role, not by the row's framing. README's own round-table pins (`README.md:607-608`)
  are records of the round-39 count inside `## Round-39 coverage additions`, and round-52's own supersession note
  (`README.md:727`) calls the 607 tally "the round-39 count" — i.e. a dated record — yet K4 runs them as living;
- the identical object in LOG — e.g. `LOG.md:2262` under `## Round 38`: `python3 tools/mori-sources-appendonly.py
  --selftest` → `pass=12 fail=0` — is excluded as history. Same text, same tally, same round-dated section;
  different treatment purely by file.
- the asymmetry is safe in direction (running more pins catches more staleness), but it proves the stated rule is
  not the actual basis. The actual basis is the frozen `LIVING = ["corpus/QUALITY.md", "corpus/README.md"]` list in
  `count-c1.py:69`; the contract paragraph is a post-hoc rationale for it.

Verdict: **partially consistent**. The K4 decision does not close defect 3's LOG target, and it leaves at least
one live present-tense tally claim (`SCORECARD.md:1070`) un-run. It is honest about what it *does* run, but the
line "a tally there is history, not a current claim" is false as a general statement.

## 3. Current-tense self-claims with a tally outside QUALITY/README/SHONEN

1. `SCORECARD.md:1070-1071` — "Existing census125/125, oracle28/28, r13 24/24, r14 44/44 and r15 63/63 with
   frozen red34/34 pass". Present tense ("Existing"), five tallies, un-run, stale (census selftest is 134/134 in
   later round-17 and round-19 records). **HIGH.**
2. `PROVINCE.md:280-283` (under `## Round-24 appended scope notes (2026-10-22)`) — "the declared after-value command
   prints `MORI_PRESSURE_SELFTEST: PASS 12/12` (exit 0) and one live host run returned `PRESSURE_OK`". Present tense
   ("prints") instrument assertion with a tally; not in K4 scope, not dated at statement level (the section is
   dated). **MED.**
3. `PROVINCE.md:350-353` (under `## Round-25 appended scope notes (2026-10-22)`) — same shape: "prints
   `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` (exit 0)". **MED.**
4. SCORECARD capability tables (`## Capabilities (round 12 demonstrations)` rows, `SCORECARD.md:641-645`; round-17
   rows `:1065-1068`; later `### capabilities:` tables) — "What it can now do" cells with parenthetical tallies,
   e.g. `(77/77)` on `roster-r12-20261019T220912Z-selftest.log` (`:643`), `(28/28)` (`:644`), `(54/54)` (`:1067`).
   The tally is bound to a named, immutable, dated receipt file (the tally reads as the receipt's content, not as a
   claim about today), so these are defensible as evidence pointers; the column header "now" is still present-tense
   framing. **LOW** (recorded, not a K4 violation).

No other undated current-tense tally claims were found: corpus lessons are round/date-headed records; knowledge
entries assert kernel facts, not lane self-state; `corpus/SOURCES.md` carries registry rows, not tally claims.
SKILL.md prose tallies are all anchored to dates or revisions ("measured 2026-10-25", "re-run 2026-10-26",
"entering X", "at the data commit"; see §5).

## 4. Living pins that are in fact dated records

- `corpus/README.md:607` and `:608` — the round-39 coverage-table rows ("Counter conformance v2 … (r38 M19)" and
  "Ancestry-based timed supersede … (r38 F1/F2 + routed quote fix)") inside `## Round-39 coverage additions`. They
  report the round-39 measurement (`--selftest` → `pass=9 fail=0` / `pass=12 fail=0`). Round-52's own note
  (`README.md:727`) describes the 607 tally as "the round-39 count". These are dated records treated as living pins;
  at data they were correctly caught stale and marked superseded (`c1-at-data.txt:13-14`). **HIGH** (as a
  consistency counterexample to the K4 rationale; the handling itself is correct).
- `corpus/QUALITY.md:885` (criterion 109's check cell) and `:909` (criterion 112's check cell) pin round-38/-39-era
  tallies. These are *stale living check cells*, not dated records — the designated hazard class — and the house
  rule works on them: 885 is superseded by criterion 111's row (`QUALITY.md:899-903`) and 909 by criterion 141's row
  (`QUALITY.md:1356-1360`, "This row supersedes 112's check cell only"), both confirmed at data. Good behavior; no
  finding beyond noting the mechanism works.

## 5. SKILL.md coverage — confirmed, with one documented caveat

- `tools/mori-pin-check.py` main() defaults `--skill` to `<root>/SKILL.md` (`mori-pin-check.py:966`), and `check()`
  parses the whole file text: registry tables (including each gate's self-test cell), hidden-row detection over all
  lines, and command re-execution. The C1 arm B runs it at R through the SHONEN pins (`SHONEN.md` box 3:
  `python3 tools/mori-pin-check.py --selftest` → `(125/125)`, receipts under
  `.ufo/waves/round-52/evidence/selftests/mori-pin-check.txt`), so SKILL.md is covered. Confirmed.
- Caveat, documented by the lane itself: SKILL.md's decision row says "Still open: K4 (pins outside the self-test
  cell)" (`SKILL.md:1002`) — i.e. the pin-check instrument explicitly does **not** sweep tally tokens outside the
  registry's self-test cells. That is harmless for the *current* SKILL.md because every prose tally found outside
  tables is anchored to a date or revision (lines 202-205, 1033-1052, 1081-1105); no undated present-tense tally
  claim exists in SKILL.md. It is a named limit for the successor instrument, not a defect in this round's claim.

## 6. Verdict

The K4 scope decision is **factually accurate about the structure it describes (verified), but its central
inference — "a tally under a round heading is history, not a current claim" — is false**, falsified by
`SCORECARD.md:1070` ("Existing census125/125 …", un-run, stale since round 17), and it is applied asymmetrically:
README's round-39 coverage rows are dated records treated as living (`README.md:607-608`, self-described as "the
round-39 count" at `:727`), while byte-identical tallies in LOG are excluded. The round-50 defect 3 target
"(tally pins in QUALITY, README and LOG)" is therefore only partially closed: QUALITY+README are handled correctly;
LOG and the SCORECARD non-Axes round sections retain at least one live present-tense tally claim that no arm runs.
The frozen P-C1 verdict at the data commit (`C1=met … mismatches=0`) stands — the counter does everything it
promises on its declared surface — but the contract's K4 rationale overstates the completeness of that surface.

## 7. Routed items (round 53) and named limits

1. **Routed (counter/instrument, successor round):** extend arm C's `LIVING` scope (or add an arm) to scan
   SCORECARD non-Axes sections, PROVINCE admission-state lines, and LOG for present-tense tally assertions, or
   require an explicit date/revision stamp next to any tally assertion outside the living files. Until then, name
   this limit: K4 covers only `corpus/QUALITY.md` and `corpus/README.md`; tally claims elsewhere are unchecked.
2. **Routed (document fix, L1):** append a dated supersession/correction to the `SCORECARD.md:1070` inventory
   (census selftest 134/134, and re-check oracle/r13/r14/r15 values) following the README 727/728 pattern, or
   reframe the sentence as the dated record it was. Same pattern for `PROVINCE.md:280-283` and `:350-355`.
3. **Named limit (this round):** the K4 rationale line (contract.md:24-28) is not a reliable classifier of dated
   vs current tally claims; treat it as a scope statement, not a proof of absence.

## Findings

- **HIGH** — `SCORECARD.md:1070-1071`: present-tense tally claim ("Existing census125/125, oracle28/28, r13
  24/24, r14 44/44 and r15 63/63 …") outside all four C1 arms and outside K4; stale since round 17 (census
  selftest 134/134 at `LOG.md:1229`, `:1379`). Contradicts contract.md:24-28 "a tally there is history".
- **HIGH** — `corpus/README.md:607-608`: living pins that are dated records (round-39 coverage rows; `:727` calls
  607's tally "the round-39 count"); K4's file-role dichotomy treats identical LOG lines as history, so the stated
  rule is not the actual basis.
- **MED** — `PROVINCE.md:280-283` and `:350-355`: present-tense instrument assertions with tallies (12/12,
  21/21) not covered by any arm.
- **LOW** — `SCORECARD.md:641-645,1065-1068` and later capability tables: "What it can now do" cells carry
  tallies bound to dated receipt files; evidence-bound, but present-tense framing.
- **LOW** — `SKILL.md:1002`: pin-check's own K4 ("pins outside the self-test cell") stays open; currently harmless,
  as all SKILL.md prose tallies are date/revision-anchored.
