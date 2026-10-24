# ReviewQualityLesson: round 24 wave 2 falsify (QUALITY 72–75, lesson M1–M7)

Seat: `MoriR24.ReviewQualityLesson` (reviewer, leaf; no subagents). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.

Revisions. The measured tip is `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc`. Every finding is at that tip unless marked. Lane HEAD when I started was `13208d2`, two wave-2 commits past the tip. Lane `master` at write time is `7c77fba`. Between the tip and `7c77fba` the routed check (`tools/mori-routed-check.py`), `corpus/QUALITY.md`, `SCORECARD.md`, `LOG.md` and the prose checker are byte-identical. `corpus/lessons/round-24.md` changed (M3 wording, rows M8–M9 added, a wave-2 selftest section) and `tools/mori-pressure.py` changed. Re-checks at `7c77fba` are marked.

## Verdict

- The routed check does what the declaration says. At the tip it reports `held 4` of `items 4`, exit 0. At `c725aa37` with `--round 23` it is red on R4 with the eight ordering rows that criterion 75 cites. All twelve mutants that should turn a row red do so.
- The claims around it do not hold as written. M1's "applied ratchet" has no result in the bytes, and the checker would fail on this round's own additions. The R2 scan that enforces criterion 73 misses two line forms and does not match the criterion's word "asserts". M4's "carries no cause" has no test that can fail. M7's report pointer and seat list are wrong, and its fix is instruction text.
- Recommendation: do not admit criteria 72–75, or M1, M4 and M7, in their current wording. Fix F1–F3 or narrow the claims to the checks that actually run.

## Findings by severity

### High

**F1. M1's "applied ratchet" result does not exist, and the checker is red on this round's own additions.**
- Lesson line 54 says the check was "Applied as a ratchet to this round's added lines (result in the round-24 SCORECARD section)". The round-24 SCORECARD section (`SCORECARD.md:1494-1506`) is a declaration, headed "Targets, not results." A search of the tip for `ratchet` and `PROSE_FUSED` finds no result in the round-24 SCORECARD or LOG sections. The only round-24 matches are the lesson row and the checker's own output strings. The LOG declaration (`LOG.md:1766-1778`) has no result either.
- `w1/MineMistake.md:196-197` says landing the checker "is a new claim, so this row is a lesson for the next round, not a round-24 claim". The lesson row contradicts that.
- Run on the round's added lines (table below): 28 hits, exit 1. None is a fused word-and-number token of the kind M1 describes. They are identifiers (`MoriR24`, `CriticC1`, `CriticC2`, `Round24`), technical names (`cgroup2`, `avg10`, `avg60`, `avg300`, `man5`, `man7`), a version fragment (`arch1`), and `sha256` tokens with a leading parenthesis (lesson lines 25–30).
- Fix: delete the ratchet clause, or record the real result after fixing the predicate (F5).

**F2. R2 misses two classes of added line, so its "no added line matches" result is not complete.**
- (a) Diff header ambiguity. `tools/mori-routed-check.py:249` tests `raw.startswith("+++ ")` before the added-line branch at `:260`. An added line whose text starts with two plus signs and a space appears in the diff as three plus signs and a space. It is read as a file header and dropped. Probe X10 (the key-and-true text with that prefix, on a scratch clone at `7c77fba`, tool bytes identical to the tip): R2 held 4 of 4. Controls at the tip: the same text without the space, and the same text with a leading `x`, both turn R2 red. So exactly the leading form escapes.
- (b) Binary classification. Probe X13 added a file under `corpus/knowledge/` that contains a NUL byte and the key-and-true text. Git prints `Binary files /dev/null and b/corpus/knowledge/binary-probe.md differ`, which yields no `+` lines. R2 held 4 of 4, and the file is absent from `detail.scanned_paths`.
- Fix: treat `+++ ` as a header only before the first `@@` of each file block. Diff with `--text`, or scan the added blob bytes directly. Add both probes as sandbox controls.

**F3. Criterion 73 claims "asserts privacy clearance" and "stays visible"; its predicate checks neither.**
- `corpus/QUALITY.md:321` says "no added line … asserts privacy clearance", which is the criterion's wording.
  - The R2 pattern (`tools/mori-routed-check.py:50-52`) matches only the key name, an optional quote, a separator, an optional quote and the word true. The contract's R2 wording (`.ufo/waves/round-24/contract.md:23`) is the same narrow pattern.
  - Probe X1 (a markdown table cell carrying the key name and the value true, with no separator) held 4 of 4.
  - Probe X2 (a prose sentence stating that clearance is granted for the retention hits, with no value) held 4 of 4. The gap is between the criterion text and the predicate.
- `corpus/QUALITY.md:319` says "The retention debt stays visible". R2 pins the two receipts and the two retention tools, which matches the criterion. But it scans additions only. Probe X3 deleted the debt row at `corpus/knowledge/retention-reconciliation-r22.md:17` (its value is false) and held 4 of 4.
- Fix: narrow criterion 73 to the diff form it checks and name the residuals. Or widen the predicate to table cells and prose, and pin the debt rows.

### Medium

**F4. M4 ("unsupported carries no cause") has no test that can fail.**
- Mutant: `tools/mori-pressure.py:142` changed so the EOPNOTSUPP note says the cause is PSI disabled at boot. At the tip, `python3 -I tools/mori-pressure.py --selftest` prints `MORI_PRESSURE_SELFTEST: PASS 12/12`, exit 0. At `7c77fba` it prints PASS 12/12 and `MATCHER: rejected 48/48 corrupted expectations`.
- Why: at the tip, `_case_failures` compares only the fields a case lists. P05 lists state, some and full, not notes. `notes` occurs 0 times in `tools/fixtures/mori-pressure/cases.json` at the tip, and in both case files at `7c77fba`. At `7c77fba`, `_corrupted_expectations` (`tools/mori-pressure.py:501-523`) corrupts verdict, exit, findings and one state, never notes.
- The kernel facts in M4 match the fetched v7.2 `kernel/sched/psi.c`. `psi_show` returns `-EOPNOTSUPP` on the `psi_disabled` branch and on IRQ without IRQ time accounting. `psi_proc_init` creates the `/proc/pressure/*` files only when `psi_enable` is set. I read the code text; I did not recompute the S091 digest.
- Fix: pin the unsupported note text, or add a matcher check for cause words, with a mutant that must go red.

**F5. The committed prose checker, which is M1's fix, has coverage and predicate defects.**
- Directory surfaces are silently empty. `DEFAULT_SURFACES` lists `corpus/lessons` and `corpus/knowledge` (`.ufo/waves/round-24/evidence/prose-fused-check.py:29-30`). `git show <rev>:corpus/lessons` returns a tree listing, so `--all-surfaces` at `c725aa37` reports 0 hits for both directories with no error. Its total of 682 equals SCORECARD 256 + LOG 326 + SKILL 40 + corpus/README 30 + PROVINCE 19 + QUALITY 11. MineMistake's per-file list (`w1/MineMistake.md:102-105`, including `corpus/lessons/round-23.md` 72, `round-22.md` 39 and the verifier spot-check 4) is not what this tool prints, and that list does not sum to 682.
- The `sha` exemption (`:45`, `startswith("sha")`) misses any token with a leading parenthesis. Probe: a bare `sha256` token passes, and `(sha256` is flagged. Lesson lines 25–30 are of this kind.
- Code spans are removed before scanning (`:38`). A fused token inside backticks passes (probe: a fused exit token inside a code span gives PASS). M1's own examples sit in code spans.
- Two-letter prefixes pass (probe: `FR12`, `S090`, `R24`, `M1` give PASS). `FR12` is a lane frontier ID.
- No identifier allowlist: `MoriR24`, `cgroup2`, `utf8` and `ext4` are flagged.
- `--section-from` (`:85-90`, `:103-107`) runs to end of file and numbers lines from the section start. The 53 count reproduces only with `--section-from "## Round23 declaration"` on the `c725aa37` file, or with MineMistake's `sed -n '1413,1493p'`. The lesson row gives neither.
- The committed tool has no added-lines mode, so the "ratchet" is not implemented in committed bytes.
- "Exit 0 after mechanical separation" depends on a scratch file (`/fast/scratch/hyaku/mori-r24-a2/SCORECARD.c725aa37.defused.md`). The separation is described only in prose (`w1/MineMistake.md:365-368`). It inserts a space exactly where the predicate matches, so exit 0 holds by construction.
- What does reproduce: 256 on the whole `c725aa37` SCORECARD, 53 on the round-23 section, and exit 1 with one hit on an injected exit 1 line. The committed checker's bytes equal MineMistake's scratch checker (sha256 `ddf08f53…`).

**F6. M2's measurement copy differs from the frozen register beyond the tip. The lesson says only "with the tip set".**
- Against `.ufo/waves/round-24/frozen/c2-freeze-register.json`, the committed copy sets the tip, drops the register's own path from `frozen`, and rewrites `frozen_by` and `note`. The copy's note admits the drop. The lesson does not.
- The drop does not change the verdict. A scratch register with the tip set and the self-path kept also gives `pre-build`, exit 0.
- The committed evidence (`evidence/freeze-order-c2.json`) was produced with `--rev 06a7686` and `--tip-for`, status bound. A run of the copy without `--rev` is unbound. Both print `pre-build`, exit 0.
- Confirmed: the original register exits 2 `invalid-register` (validator at `tools/mori-freeze-order.py:183-196`), and the frozen file is unchanged since `f6a2970`.

**F7. M3, M7 and A5 each contain a claim the bytes contradict.**
- M3 (lesson row at the tip) says "the knowledge entry cites only S090–S096". The knowledge entry cites S097 at line 1 and line 185 (U6), and `PROVINCE.md:258` cites it too. The S097 registry row in `corpus/SOURCES.md` lists only the lesson as a user. A5 (`.ufo/waves/round-24/contract.md:163`) says S097 is "cited by nothing". At `7c77fba` the lesson sentence was reworded and the S097 user list widened. A5 is unchanged.
- M7 says "the round's `/tmp` residue is listed in the report". No round-24 file lists it, and a search for residue finds nothing. M7 names six seats; at least nine wrote under `/tmp`. The three it omits are SrcPsiRst (`w1/SrcPsiRst.md:32`), DraftKnowledgeEntry (`w1/DraftKnowledgeEntry.md:25` on, run from `/tmp/mori-r24-draft`) and ScoutToolConventions (`w1/ScoutToolConventions.md:75-76`). The real gap is that the wave-1 spec allows `$TMPDIR` as a second root ("or $TMPDIR").
- M7's fix ("wave-2 context names the scratch root") is instruction text. QUALITY 54 says instruction text is never runtime prevention. So M7 is not shown able to fail.

**F8. "Thirteen sandbox mutants" (`corpus/QUALITY.md:312`) is wrong. The battery has twelve expected-red mutants.**
- `w1/BuildRoutedCheck.md:190` says 13 mutants. Its §4 table has a control (M0) and fourteen mutants, of which two (M2b, M2c) are green negative controls. The expected-red set is M1, M1b, M1c, M2, M2d, M2e, M3, M3b, M4, M5, M6, M7: twelve.
- My re-run at the tip (scratch script `prose/battery.sh`, log `prose/battery.log`): M0 held 4 of 4. All twelve expected-red mutants turned their row red: R1 by M1, M1b, M1c; R2 by M2, M2d, M2e; R3 by M3, M3b; R4 by M4, M5, M6, M7. M2b and M2c held. The per-mutant results match the report. Only the count is wrong.
- Minor: M2d and M2e are described as "one byte". The report's own battery (`mut-routed/battery.sh`, the M2d and M2e blocks) inserts eight bytes (`#MUTANT` and a newline) at offset 200. My battery changes one byte with `dd`.

**F9. Criterion 75: "started" wording, file-name discovery, and an unbounded `at`.**
- "every wave spec has a started ledger row" (`corpus/QUALITY.md:329`) differs from the predicate, where the last row's result is `started` or `partial` (`tools/mori-routed-check.py:643`). Probe X4 (final row `partial`, no `started` row, verify clean) held 4 of 4. The dispatch-ledger verifier also treats `partial` as a started row (`tools/mori-dispatch-ledger.py:285-297`). So the predicate agrees with the tool, and the criterion text does not.
- Ledgers and specs are found by file-name regex only (`tools/mori-routed-check.py:480-481`). Probe X9 (non-JSON content under a name that does not match) held 4 of 4. Criterion 75's "every ledger of the round" depends on that naming.
- `at` has no upper bound. Probe X11 (`at` set to 2099) held 4 of 4. The criterion's lane-written limit covers this in part, but the criterion does not say so.

**F10. Criterion 72's heading ("the quota capability stays absent") is broader than its checks.**
- Probe X12 appended a quota-capability line to the existing `tools/mori-census.sh`, with no new path. R1 held 4 of 4. R1 checks added paths with `quota` in the name (`:84-85`), two fixed absent paths (`:73-76`), the round-23 tree pin, and the exact byte string of the historical case name under `tools/` (`:70`, `:398`).
- Probe X5 used a spelling variant of the historical case name in a new `tools/` file. It held 4 of 4.
- The enumerated checks in criterion 72 match the code. The heading does not.

**F11. Criterion 74's "not reconstructed" is pinned only inside `.ufo/waves/round-23` and two blobs.** Probe X8 added a reconstructed transient-source note under `.ufo/waves/round-24/`. R3 held 4 of 4. The criterion should say this is not checked.

**F12. The "able to fail" evidence for R1–R4 and for M1 is not committed.**
- The battery (`/fast/scratch/hyaku/mori-r24-a2/mut-routed/battery.sh`), the defused file and the draft checker (`/fast/scratch/hyaku/mori-r24-a2/mori-prose-fused.py`) all live outside the lane. QUALITY 23 requires a committed generator and digest for `/tmp` evidence. The same reasoning applies to scratch.
- Fix: commit the battery generator and a digest under `.ufo/waves/round-24/`.

### Low

**F13. M6's able-to-fail check is not cited.** The nine quoted hits reproduce at `c725aa37` (list below). At the tip there are 21 hits under `.ufo/waves/`, all outside R2 scope as intended. The lesson's fix cites only amendment A1. The controls that prove the scope (M2b, M2c) are in the battery, and the lesson does not point to them.

**F14. M5: R1–R3 cannot be red at `c725aa37` by construction.** The base equals the rev there, so the "equals base" predicates compare a tree with itself. The lesson and A4 already say so ("regression guards"). Only R4 is measured on the real defect. R1–R3 are shown red only by mutants. This is acceptable as long as the criteria keep saying "regression guard", and they do.

## Criteria 72–75 against the tool's real predicate

| Criterion | Stated predicate (`corpus/QUALITY.md`) | Tool predicate (`tools/mori-routed-check.py`) | Match | Probe |
|---|---|---|---|---|
| 72 (R1) | No added quota-named path under `tools/` or `corpus/knowledge/`. No tool names the historical case. Round-23 tree OID equals base. "Stays absent." | Added-path filter `:84-85`; fixed absent paths `:73-76`; tree pin; byte needle `:70`, `:398` | Partial. Heading is broader. Spelling variant passes. | X5 held, X12 held |
| 73 (R2) | Round-23 receipts and both retention tools byte-identical. No added line "asserts" privacy clearance. Debt "stays visible." | Blob pins `:91-96`; scope `:57-64`; pattern `:50-52`; header parse `:249` | No for "asserts". No for "visible". No for complete additions. | X1, X2, X3, X10, X13 |
| 74 (R3) | Round-23 tree (evidence, rejected) byte-identical. Limitations "not reconstructed." | Round-23 tree pin; two blobs; rejected tree | Yes for bytes. "Not reconstructed" beyond the pinned tree is unchecked. | X8 held |
| 75 (R4) | Every ledger verifies clean. Each row's `at` no earlier than the last dispatch-file commit. Every wave spec has a started row. Red on round 23 with eight rows. | Verify exit and status `:574`; time rule `:612`; last row started or partial `:643`; name discovery `:480-481` | Yes for verify, time and the round-23 red. "Started" wording no. Discovery and unbounded `at` are residuals. | X4, X9, X11 held; round-23 red reproduced |

## M1–M7 pointers and able-to-fail

| ID | Pointer followable? | Able to fail shown? | Verdict |
|---|---|---|---|
| M1 | Partly. Counts reproduce with the committed tool given the heading or the sed slice. The "mechanical separation" file is scratch-only. The ratchet result does not exist. | Injected exit 1 line: yes. Exit 0 after separation: circular and scratch-only. Ratchet on added lines: red, 28 hits. | Not shown as claimed (F1, F5) |
| M2 | Yes: register, copy, evidence, validator lines | Yes: the original register exits 2 `invalid-register` | Shown. Copy edits undisclosed (F6). |
| M3 | Yes: S097 row, knowledge entry | None | Claim false at the tip (F7) |
| M4 | Yes: psi.c, amendment A2, knowledge row `corpus/knowledge/system-pressure-r24.md:140` | No: a cause note survives selftest and matcher (F4) | Not shown |
| M5 | Yes: A4 text, CriticC1Vacuity, `--round 23` run | Yes for R4: eight rows red at `c725aa37` | Shown |
| M6 | Yes: nine hits at `c725aa37`; A1 | Not cited. Controls M2b and M2c held in the battery. | Shown only by the battery (F13) |
| M7 | Dangling: no residue list. Seat list incomplete. | None (instruction text only) | Not shown (F7) |

## Round-24 added lines through `prose-fused-check.py` (hits)

Method: added lines per surface from `git diff --unified=0 c725aa37 a730ecf -- <path>`, with new-file line numbers kept. Each extracted file was run from the clone with `python3 -I .ufo/waves/round-24/evidence/prose-fused-check.py --file <added-lines file>`. The full files at the tip were also run, and hits on added lines were kept. The two methods agree.

| Surface | Added lines | Exit | Hits (new-file line: token) |
|---|---|---|---|
| SCORECARD.md | 14 (1493–1506) | 1 | 1494: MoriR24 |
| LOG.md | 14 (1765–1778) | 1 | 1766: MoriR24 |
| corpus/lessons/round-24.md | 60 (1–60) | 1 | 3: MoriR24. 25–30: sha256 (six). 58: CriticC1, 1Vacuity. |
| SKILL.md | 33 | 1 | 611: Round24. 626: cgroup2. 637: Round24. |
| corpus/SOURCES.md | 9 | 1 | 96: avg10, avg60, avg300, cgroup2, avg10. 99: cgroup2 twice. 103: man5, man7. |
| corpus/knowledge/system-pressure-r24.md | 196 | 1 | 2: arch1. 4: MoriR24. 99: cgroup2. 186: CriticC2, 2Semantics. |
| corpus/QUALITY.md | 26 | 0 | none |
| PROVINCE.md | 53 | 0 | none |
| corpus/README.md | 39 | 0 | none |

Totals: 28 hits on the six surfaces that have hits, and 0 on the other three. On the three surfaces asked for (SCORECARD, LOG, lesson), there are 11 hits, all identifiers or sha256 tokens. None is an M1-class fused token. The overall exit is 1, so a ratchet at this tip would fail.

The checker's `--all-surfaces` run at `c725aa37` gives `FAIL hits=682`. Both directory surfaces contribute 0 (F5).

## Confirmed (ran, and it holds)

- Landed tool bytes equal the measured bytes: `sha256sum tools/mori-routed-check.py` gives `64921a0c…`, and the blob is `3337232b…`. These match `w1/BuildRoutedCheck.md` §0.
- Tip: `--rev a730ecf --round 24` gives `held 4`, `items 4`, exit 0. The round-24 wave-1 call is recorded 16 s after its dispatch commit (`at` epoch 1792656853, commit epoch 1792656837), so the R4 ordering holds.
- `--rev c725aa37 --round 23` gives `held 3`, exit 1. R4 is red with eight `dispatch_committed_after_dispatch` rows in `.ufo/waves/round-23/wave1-ledger.json`. Dispatch commit `22772c1` is 2026-10-21T15:10:59-03:00, which is 18:10:59Z. Criterion 75's red claim holds.
- `--rev c725aa37 --round 24` gives `held 3`, exit 1, `no_round_ledger`. This matches the SCORECARD before-value.
- A bad revision and a bad repository both give exit 2.
- At `7c77fba`, `--round 24` gives `held 4`, exit 0. The wave-2 call is recorded 8 s after its dispatch commit (`at` epoch 1792659404, commit epoch 1792659396).
- R2 reports no matches among the tip's added lines in the scanned surfaces.
- M1 numbers: 256 on the whole `c725aa37` file, 53 on the round-23 section, and an injected exit 1 line gives 1 hit. The committed checker's bytes equal MineMistake's scratch checker.
- M2: the original register exits 2 `invalid-register`. The copy exits 0 `pre-build`. The register is unchanged since `f6a2970`.
- M5: the critic's point that base equals rev is accurate. A4's `--round 23` measurement is the right real-defect check.
- M6: nine quoted hits at `c725aa37` under `.ufo/waves/`: `round-22/falsify/MutationScope.md:58,69`; `round-22/measure-round22.py:87`; `round-23/falsify/C1R04.md:170`; `C1R15.md:238`; `C1R17.md:153,163`; `ReviewDebtHold.md:200,274`.
- Criteria 72–75 cite round-23 spot-check lines 62–65 for items 1–4, and the cited text matches.
- The routed check, `corpus/QUALITY.md`, `SCORECARD.md`, `LOG.md` and the prose checker are unchanged from the tip through `7c77fba`.

## Residual risk and verification gaps

- Not verified: S-row digests. I read the kernel code and matched its text, but I did not recompute sha256 of fetched bytes or check line anchors, since the reader output has no line numbers.
- Not reviewed (after the tip, or outside scope): M8–M9 and the wave-2 selftest section in the lesson, the C2 live bracket check, the census, and the other QUALITY lines.
- X10 ran on a clone at `7c77fba`. Its routed tool bytes are identical to the tip. All other probes ran at the tip.
- I ran my own battery (`prose/battery.sh`), not the report's `battery.sh`, which targets another seat's sandbox. Results match the report's table except for the count.
- The 28-hit run uses my added-line extraction, because the committed checker has no added-lines mode.
- Scratch register variants (keep-self, drop-self) were made by a short JSON rewrite of the `tip` field in scratch. No repo file was edited.
- Probe outcomes describe the current bytes. A later fix can change them.

## What I ran

1. Lane, read-only: `git rev-parse`, `git log --oneline`, `git merge-base --is-ancestor a730ecf HEAD` (rc 0), `git diff --stat a730ecf 13208d2`, `git diff --name-only a730ecf 7c77fba -- <paths>`, `git diff --shortstat c725aa37 a730ecf -- SCORECARD.md LOG.md corpus/lessons/round-24.md` (88 insertions, 0 deletions), `git cat-file -t`, `git show`, and `git log -1 --format='%h %cI %ct' c725aa37 -- .ufo/waves/round-23/wave1-run.json` (gives `22772c1 2026-10-21T15:10:59-03:00 1792606259`).
2. Clones, all in scratch: `clone/` at the tip (fetched `master` once, then returned to the tip). `mut/` at the tip (fetched `master`, then reset to the tip after its checks). `tool/` holds a copy of the landed routed-check bytes.
3. Routed check: tip `r24` (exit 0, held 4). `c725aa37` `r23` (exit 1, held 3). `c725aa37` `r24` (exit 1, held 3). `deadbeef…` (exit 2). `/nonexistent` (exit 2). `7c77fba` `r24` (exit 0, held 4). Outputs are in `prose/routed_*.json`.
4. Prose check: nine surface extractions and runs (table above), a full-file cross-check, `--all-surfaces` at `c725aa37` (`prose/allsurf_c725.out`), `--section-from "## Round23 declaration"` (53), the whole file (256), an injected exit 1 line (1 hit), 11 precision probes, and one sha probe.
5. Freeze check: original register, copy, keep-self and drop-self variants (`prose/freeze_*.out`, `prose/regtest/*.out`).
6. Mutant battery at the tip, in `mut/` (`prose/battery.log`, `prose/battery-out/*.json`):

| Probe | Change to the committed tree (sandbox clone) | Result at the tip |
|---|---|---|
| M0 | none (control) | held 4/4 |
| M1, M1b, M1c | quota tool path, quota note, historical name under `tools/` | R1 red |
| M2 | key-and-true line under `corpus/knowledge/` | R2 red |
| M2b, M2c | same text under `.ufo/` and `tools/` | held (negative controls) |
| M2d, M2e | one byte changed in each retention tool | R2 red |
| M3 | last byte of the overwrite receipt | R3 red and R1 red |
| M3b | file added under the round-23 tree | R1 and R3 red |
| M4 | ledger `at` set to 07:00Z | R4 red |
| M5 | newline appended to the dispatch payload | R4 red |
| M6 | attempts ledger removed | R4 red, `no_round_ledger` |
| M7 | final ledger row `refused`, `started_ids` 0 | R4 red |
| X1 | markdown table cell with the key name and value true, no separator | held |
| X2 | prose sentence that privacy clearance is granted | held |
| X3 | debt row at `corpus/knowledge/retention-reconciliation-r22.md:17` deleted | held |
| X4 | final row `partial`, no `started` row | held |
| X5 | spelling variant of the historical case name in a new tools file | held |
| X8 | reconstructed note under `.ufo/waves/round-24/` | held |
| X9 | non-JSON ledger-like file under a non-matching name | held |
| X10 | added line starting with two plus signs and a space, then key and true | held (run at `7c77fba`) |
| X11 | `at` set to 2099 | held |
| X12 | quota-capability line appended to `tools/mori-census.sh` | held |
| X13 | added file containing a NUL byte, then key and true | held |

   Controls for X10 at the tip: the same text without the space, and with a leading `x`, both red.

7. Selftest: tip baseline gives PASS 12/12, rc 0. The note mutant also gives PASS 12/12, rc 0. At `7c77fba`, the baseline and the mutant both give PASS 12/12 with `MATCHER: rejected 48/48`.
8. Kernel source: fetched the raw v7.2 `kernel/sched/psi.c` through the reader (the `psi_show` region and the `psi_proc_init` block) and matched the code text.
9. Greps and reads: S097 citations; `/tmp` mentions in `w1/`; quoted-hit counts (9 at `c725aa37`, 21 at the tip); the lesson table; `corpus/QUALITY.md` lines 312–332; contract amendments A2, A4 and A5; MineMistake lines 54–60, 98–105, 196–197 and 365–368; the wave-1 spec's scratch wording.

## Tooling and writes

- Installs or upgrades: none. Versions in use: Python 3.14.8, git 2.56.0, plus host `sha256sum`, `dd`, `stat` and bash. No pacman, uv, npm or cargo use.
- Scratch: `/fast/scratch/hyaku/mori-r24-a2/w2/ReviewQualityLesson/` (about 596 MB: clones, tool copy, prose outputs). This seat wrote nothing under `/tmp`.
- Lane writes: this report only (`.ufo/waves/round-24/w2/ReviewQualityLesson.md`). No git write, no index change, no jj command, no PSI or cgroup write, and no service change.
