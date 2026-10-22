# Review: C1 predicate table against routed defects D1–D4

Seat: MoriR25.ReviewContractAgainstSpotcheck (leaf reviewer, read-only; no subagents, no background jobs).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Spotcheck tip: `28b79d3d`. Lane HEAD when reviewed: `6a92d5e` (round-25 amendment A2).
Scope: the C1 table in `.ufo/waves/round-25/contract.md` against routed defects D1–D4 at `corpus/lessons/round-24-verifier-spotcheck.md:135-146`. I review the original table (as assigned) and amendment A1, which is the current binding text.

## Bottom line

- **Original C1 table.** D1 is the only predicate that enforces the routed "full stdout", but it does so by executing R's selftest. The contract header (`contract.md:14`) and the fleet closure rule (`PROTOCOL.md:415-417`) rule that out. D2 is the weakest: it checks three literal strings in one file, and it would pass a tree that still contradicts the Corrections block in three other places. D3 checks for a string, not for the tally. D4 checks one ignore line and omits the `.scratch/` bound.
- **Amendment A1** (`contract.md:97-124`) closes most of the original gaps (listed below). It also weakens D1: "full stdout" becomes "body contains two lines". Its D2 still passes the residual described under H2.
- Blocking before landing: H1 (D1), H2 (D2). Medium: M1–M4.

## Contract state (what I reviewed)

- Original table: `contract.md:10` (C1 heading), `:14` (reads git objects only), `:17-22` (rows D1–D4), `:24` (Output), `:28` (Before), `:30` (Declared after).
- The file changed during my review. My first read ended at the "Held and observed" line (old line 95). The file now has 161 lines: A1 at `:97-124`, A2 (C2 only) from `:137`. The on-disk sha1 (`7fc5bc36…`) equals the committed `6a92d5e` blob. Lane commits after the spotcheck tip: `7634be7` (claims), `0099a39`, `129832e`, `09f55b6` (C2 tool and a `__pycache__/` ignore line), `51ddd01` (A1), `6a92d5e` (A2).
- A1 says it "replaces the original C1 after-value" (`:123`). Counted items are D1–D3. D4 is a hygiene row that still gates exit (`:111-114`).
- Before-state confirmed at `28b79d3d`: D1 evidence file absent (`git cat-file -e` exit 128); D2 three phrases present and no `(K4)` in a Corrections section; D3 no line containing both `Correction` and `PASS 7/7` (lesson `:79-80` says `S01–S06`, `PASS 6/6`); D4 `.gitignore` has two lines only. All four are red, matching `:28`.

## Governing text used

- Routed items: spotcheck D1 `:137`; D2 `:138-141` and `:143`; D3 `:144`; D4 `:145`; carried bound `:146`.
- Fleet `PROTOCOL.md` (read-only): a numeric claim carries its counting command (`:352-353`); "Claimed ≠ re-executed" (`:361-362`); "Corrections sweep every mention", grepping `corpus/README.md`, `SKILL.md` and `knowledge/` (`:363-365`); a drift pin is a committed expected-output file the script diffs against (`:370-373`); self-test with expected values committed in the repo (`:385-389`); a verdict names its revision (`:393-395`); a child lane's registry home is its own `SKILL.md` (`:398-401`); the integrator verifies committed evidence and "does not execute a sibling's gate" (`:415-417`).
- Lane `corpus/QUALITY.md:73` (criterion 31: a self-test tally names the revision and is measured on the delivered gate's bytes); `:127-130` (criterion 46: sweep province, index and knowledge prose).

## Findings

### H1 (High): A1 D1 drops the routed "full stdout"

- Routed (`:137`): "Commit future selftest outputs with the measured revision and the full stdout."
- A1 D1 (`contract.md:107`): the body must "contain the line `MORI_PRESSURE_SELFTEST: PASS 12/12` and a line starting `MATCHER: rejected 48/48`". The re-run is "reported, never needed for `held`".
- Observed: the real stdout at `28b79d3d` is 82 bytes, two lines, exit 0, and byte-identical on a second run (sha1 `b9cadb7e…` both times). In a /tmp check, the real stdout plus `MORI_PRESSURE_SELFTEST: FAIL 11/12` and a Traceback line passes the A1 containment check, and it is not byte-equal to the real output.
- Original D1 enforced byte equality (`contract.md:19`), but only by running R's selftest. That conflicts with `contract.md:14` and `PROTOCOL.md:415-417`. Neither version satisfies all three constraints (no execution in `held`, full stdout, measured revision).
- Repair that satisfies all three: commit the expected body (the two lines) as a file under `tools/fixtures/mori-pressure/` (already bound by `fixtures_tree`), and require the body to equal it byte for byte. This is the committed expected-output pin the protocol names (`PROTOCOL.md:370-373`). Keep `--rerun` for the author's write-time run.

### H2 (High): D2 passes a body that still contradicts the Corrections block

- Routed (`:138-143`): fix body lines in place; "Corrections sweep every mention" (`PROTOCOL.md:363-365`); stop relying on the banner.
- Residual statements at `28b79d3d` (`corpus/knowledge/system-pressure-r24.md`, blob `d4ccce42`, unchanged at `4f05dd5a` and `6a92d5e`) that the Corrections block supersedes, beyond the three routed lines:
  - **Row 176 (K3):** "`malformed` means *this file is not a kernel PSI file of this resource*". Corrections `:13-16` say this holds on v7.2 only, and that genuine pre-5.13 cpu files read malformed. Row 172 is scoped ("at v7.2"), so row 176 is the inconsistent one. The wave-2 K3 finding (`.ufo/waves/round-24/w2/CriticKnowledgeOverclaim.md:67-84`, quote at `:75`) named this statement.
  - **Row 173 (P4):** "a missing file is consistent with either", which lists two causes. Corrections `:30-33` list five.
  - **Row 177 (P4):** "so a decrease means the two samples are not comparable readings of the same counter", with no `[INFERENCE]` label. Corrections `:31` label it `[INFERENCE]`; facts `:149-150` carry the label; row 177 does not.
  - Banner `:11` ("this section wins") is intact.
- Predicate coverage: the original (`contract.md:20`) tests three literal strings and the `(K4)` token. A1 (`:108`) tests regexes for the same three, plus two positives (K5, P3) and a `(k4)` + `total` token. Neither tests rows 173, 176, 177 or line 11.
- Observed (/tmp simulation of A1 D2): on a copy where only the three routed lines are fixed and a K4 note is added, A1 D2 holds (TEST B). The original also holds on that copy, by reading the text (its three literals are gone and the token is present). That second result is read from the predicate, not run.
- The lane's own reviewer found the same class: `.ufo/waves/round-24/w2/ReviewKnowledgeTable.md:54-70` (F-6). Its items 8 and 10 map to rows 173 and 177.

### M1 (Medium): D2 checks one file; the standard requires every file the lane touches

- `PROTOCOL.md:363-365` names `corpus/README.md`, `SKILL.md` and `knowledge/`. `QUALITY.md:127-130` adds province, index and knowledge prose. Both predicates read only `corpus/knowledge/system-pressure-r24.md`.
- Current state: a tracked-file grep outside `.ufo/` finds the routed phrases and the K3/P4 wording only in the entry, in the spotcheck lesson (`round-24-verifier-spotcheck.md:139-141`, which quotes them as the defect), and in `SCORECARD.md:1521` (`PASS 7/7` only). No sibling residue today. The predicate would not catch one.

### M2 (Medium): D2 has no positive check for the corrected wording

- Original: literal strings only, so a same-meaning rewording passes. A1 regexes cover "every read" and "spike … may be invisible" variants, but not "could be invisible" or "may go unseen", and nothing checks row 170's replacement. The critic's K4 replacement is "can stay under the threshold" (`CriticKnowledgeOverclaim.md`, K4 section, `:85-100`); no predicate requires it.
- No positive K3 check for row 176.
- The routed "correction note" check is only the `(K4)` token, which any sentence containing it satisfies.

### M3 (Medium): D3 checks for a string; the tally is reproducible but not re-derived

- Original (`contract.md:21`) and A1 (`:109`) accept any line containing `Correction` and `PASS 7/7`.
- Observed: `python3 -I -B tools/mori-pressure.py --selftest --cases tools/fixtures/mori-pressure/supplementary-cases.json` (the flag is at `tools/mori-pressure.py:391`) prints `MORI_PRESSURE_SELFTEST: PASS 7/7`, `MATCHER: rejected 28/28 corrupted expectations`, exit 0, at `28b79d3d` (run in a /tmp extract). The claim is true now and checkable by a committed command.
- `PROTOCOL.md:352-353` requires a numeric claim to carry its counting command. Neither predicate requires one.

### M4 (Medium): D3 drift at REV is invisible

- The count n is pinned to `4f05dd5a` (7 cases). A REV with an eighth case and a lesson still saying `PASS 7/7` holds. A1 adds a commit binding, but the cited commit only needs to show 7 cases.
- No drift today: `supplementary-cases.json` is blob `4d00f164` at `4f05dd5a`, `28b79d3d` and `6a92d5e`.

### L1 (Low): D4 omits the `.scratch/` bound

- Routed (`:145`): "Leave `.scratch/` (round 22) to its owner's disposition, with no deletion by closure." Neither D4 predicate (`contract.md:22`, `:111-114`) mentions it, and the contract does not list it as an unchecked bound.
- `.scratch/` is present (`test -d`). It is untracked, so git-object reads cannot check it. The honest fix is to declare it unchecked.

### L2 (Low): D1 over-binds fixtures

- `fixtures_tree` covers `supplementary-cases.json`, which the default selftest does not read (the default run prints `PASS 12/12`). A supplementary-only edit would stale the D1 evidence. This is over-strict and not a routed gap.

## Closed by A1 (verified by reading the predicate text)

- D2 paraphrase and spacing: regexes and whitespace folding (`contract.md:108`).
- D2 heading rename and row deletion: exactly one `## corrections` heading; `## facts` and `## decision table` present; data-row count not below `28b79d3d` (`:108`).
- D3 S07 and commit binding (`:109`).
- D4 negation lines and tracked `tools/` pycache (`:111-114`).

## Requirements omitted (summary)

Original C1 table:
1. D2 sibling-file sweep (`PROTOCOL.md:363-365`).
2. D2 "every mention": rows 173, 176, 177.
3. D2 "stop relying on the banner": line 11 untested.
4. D2 corrected wording: no positive check for rows 170 or 176.
5. D3 counting command and a count taken at REV.
6. D4 `.scratch/` no-deletion bound (undeclared).
7. Tension, not an omission: D1 executes a sibling's gate, against `contract.md:14` and `PROTOCOL.md:415-417`.

A1 C1 table:
1. D1 "full stdout" (H1).
2. D2 items 1–4 above (H2, M1, M2), except that A1 adds K5 and P3 positives.
3. D3 items 5 (M3, M4).
4. D4 item 6 (L1).

## Outside the routed set (not counted; for the planner)

- **P-1:** The C1 tool (`tools/mori-routed-r24.py`) is absent at `6a92d5e` (`git cat-file` exit 128). Neither C1 table version requires a `--selftest` with committed expected values, though the tool returns a verdict on exit codes 0/1/2 (`PROTOCOL.md:380-389`). The C2 tool has one.
- **P-2:** No registry row before results are cited (`QUALITY.md:73`; a child lane's registry home is its `SKILL.md`, `PROTOCOL.md:398-401`). The C1 table names none.
- **P-3:** The D4 hygiene row scans `tools/` only. 212 tracked `__pycache__` entries exist at `28b79d3d` and at `6a92d5e`, none under `tools/`. The entries I read are under `.ufo/waves/round-20/falsify/SelftestC2/`. Not routed; the ignore rule does not untrack them.

## Recommended contract changes (before landing)

1. D1: pin the two-line expected body as a committed file under `tools/fixtures/mori-pressure/`; require byte equality; keep `--rerun` out of `held`.
2. D2: fix rows 173, 176 and 177 in place (scope row 176 to v7.2; list all five P4 causes; add `[INFERENCE]` to row 177). Remove or qualify the banner at `:11`. Extend the sweep to `corpus/README.md`, `SKILL.md`, every `corpus/knowledge/*.md`, and province/index prose. Add a positive check for row 170's replacement.
3. D3: require the correction line to carry the counting command, and have the check run it in an extract or compare against a pinned expected line. Take n from the file at REV.
4. D4: declare `.scratch/` an unchecked bound in the contract.
5. P-1 to P-3: add a self-test, a registry row and the tracked-bytecode scope to the C1 spec.

## Checks run (read-only; /tmp scratch is out of lane and not durable evidence)

- Existence and ancestry: `git cat-file -e` for the D1 evidence file and the C1 tool at `28b79d3d` and `6a92d5e` (exit 128 both); `merge-base --is-ancestor` of `4f05dd5a` and `c484f6d` into the tip (exit 0 both).
- Blob identity: knowledge entry `d4ccce42` (at `4f05dd5a`, `28b79d3d`, `6a92d5e`); lesson `779a0795`; `tools/mori-pressure.py` `5785c5b2`; fixtures tree `060f60f6`; supplementary cases `4d00f164`.
- Stale evidence at `89849a7`: one line, `MORI_PRESSURE_SELFTEST: PASS 12/12`, no MATCHER line.
- Selftest run from a /tmp extract of `28b79d3d` (`git archive 28b79d3d tools | tar -x`): default run gives 82 bytes, exit 0, byte-identical on re-run. The `--cases` supplementary run gives `PASS 7/7`, exit 0.
- /tmp simulations of A1 D2 (TEST A, unfixed tip: HELD false, K5=1, K4=1, P3=1, no `(k4)`; TEST B, three routed lines fixed plus a K4 note, rows 173/176/177 left: HELD true) and of A1 D1 (containment holds on a padded body; byte equality fails).
- Tracked grep outside `.ufo/` for the routed phrases and the K3/P4 wording: the entry, the spotcheck lesson and `SCORECARD.md:1521` only.
- Tracked `__pycache__` count: 212 in total, 0 under `tools/`, at `28b79d3d` and `6a92d5e`.
- `.scratch/` exists (`test -d`).
- `SCORECARD.md:1514` and `:1521` still carry the text A1 cites at `6a92d5e`.

## Residual risk and verification gaps

- No predicate was executed as written: the C1 tool is not landed and the D1 evidence file does not exist. The TEST A/B and D1 padding checks run predicate text against /tmp copies. TEST B is my construction; the lane does not contain it.
- The original D2 result on TEST B is read from the predicate text, not run.
- The round-24 fleet report ("all six statements corrected") lives in the fleet repo and was not opened. Nothing here relies on it.
- I did not verify whether the knowledge entry counts as append-only, which decides whether an in-place fix is allowed. The routed text assumes it is not.
- A2 (C2) and the carried R4 bound are out of scope.

## Tool installs and writes

- Installed or updated: none.
- Written: this report only. /tmp scratch (extracts, stdout captures, simulation output) is outside the lane and not durable evidence. Disclosed per `QUALITY.md:98` (criterion 38). Removed after writing.
