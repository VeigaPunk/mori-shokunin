# Round 90 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)

Subject: mori L1 round 90, lane HEAD `e5200affd7eba792e8b4ecf46ca6a3ae4bb07a8e`
(entering `d1c8488986512a6a0475af88cc52779ce4703e00`, base `037c02ca43a5ff36e23e449d0d6bcf50a1f2cbec`).
Report: `.ufo/reports/round-90/mori.md`. Checked against committed bytes; no lane-authored file was edited.

## 1. Conformance (PROTOCOL step 1)

| Check | Command / observed | Result |
|---|---|---|
| Report committed by lane identity | `git log --format='%an %H %s' -- .ufo/reports/round-90/mori.md` → `a48343d4…` (mori-shokunin, "round-90: mori report"); `8151e9ad…` (mori-shokunin, "hyaku sweep: L1 returned without committing; attribution defect") | pass; second commit is an attribution defect, recorded |
| SHONEN heading, one line per box | `## SHONEN` present; four `[~]` lines with pointers; lane `SHONEN.md` has four boxes | pass |
| Cited commits exist and are ancestors of `master` | `merge-base --is-ancestor` on `master`: 037c02ca, d1c84889, 11197820, 9441ef30, 0a1f019b, e5200aff → all yes | pass |
| Lane pushed, no round leftovers | `jj-lane.sh state …mori-shokunin` → `ahead=0 behind=0 tracked=0 untracked=0`; `git status --porcelain` empty; `git ls-remote origin refs/heads/master` → `e5200affd7eba792e8b4ecf46ca6a3ae4bb07a8e` | pass |
| Census validate | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → `mori ok …/corpus/SOURCES.md`, rc 0 (W04 warnings only); rows `grep -cE` 384 (037c02ca) → 389 (e5200aff); census `rows 389 tier.A 349 tier.B 19 tier.C 21 status.mined 331 status.queued 24 status.rejected 34` | pass, matches report |
| Wave shape | `w1-results.json` `seats: 13`; spec roles executor 4, reviewer 2, scribe 2, critic 1, mutation-tester 1, connector 1, scout 1, sentinel 1; no planner | conformance defect (prompt §3 names 1× planner; status-neutral) |
| Attack share | report: 4/13 = 31 % (reviewer, critic, mutation-tester); `corpus/lessons/round-90.md` Wave line: 5/13 (sentinel counted) | ≥25 % either way; the two figures disagree (defect R11) |
| Prompt embed | rendered prompt carries claims, frontier step, L2 floor, report contract, push scope, L0 channel. Commit-before-report ordering and commit-hash citation rule are not verbatim in the rendered text | template gap, operator-side, status-neutral |
| Dispatch digest (`.ufo/watchdog.log`, mutable; copied here) | `2026-11-04T20:28:54-03:00 launch mori round=90 pgid=506017 driver=hyaku-inline attempt=3` · `2026-11-04T20:35:57-03:00 lane-dead-no-report mori round=90; retry …` · `2026-11-04T22:32:23-03:00 launch mori round=90 pgid=2943360 driver=hyaku-inline attempt=1` · `2026-11-04T22:32:57-03:00 lane-dead-no-report …` · `2026-11-04T22:32:59-03:00 launch … pgid=2957642 attempt=2` · `2026-11-04T22:33:31-03:00 lane-dead-no-report …` · `2026-11-04T22:33:33-03:00 launch … pgid=2960690 attempt=3` · `2026-11-04T22:34:03-03:00 lane-dead-no-report …` · `2026-11-05T00:29:06-03:00 launch mori round=90 pgid=1522650 driver=hyaku-inline attempt=1` · `2026-11-05T00:50:10-03:00 complete mori round=90; hyaku-inline attempt=1` | the 00:29 launch produced the landed report; earlier launches ended without a report |

Report contract: all required sections present (Work performed, Landed changes, Before → after, Sources & frontier, Trend verdicts, SHONEN). Report is not a marker: it names real committed hashes, evidence pointers and measurements.

## 2. Claims (PROTOCOL §Gate standard: committed evidence, not re-execution of the lane's counters)

Method. The two counters are lane-owned gates; I did not execute them. For each claim I (a) verified the committed receipts against the bytes they name and (b) ran plain measurements over committed bytes.

Shared byte identity, plain `git show | sha256sum` at both revisions:
- `.ufo/waves/round-90/count-c1.py` `e3ca0885…` at 11197820 and e5200aff; equals receipt header `counter-sha256`.
- `.ufo/waves/round-90/count-c2.py` `332cd23c…`, same; equals receipt.
- `.ufo/waves/round-87/count-c2.py` `3fc9cc44…` (C1 subject); equals receipt `subject-sha256`.
- `.ufo/waves/round-88/count-c1.py` `efe4f1f7…`, `.ufo/waves/round-88/count-c2.py` `fe9ed6ac…` (C2 subjects); unchanged 11197820 → e5200aff.
- `.ufo/waves/round-90/battery/branch-heldout.json` `562b390b…`; unchanged 11197820 → e5200aff.
- `git diff --stat 11197820 e5200aff -- <all counter, subject, battery paths>` → empty.

### C1 — operability (score 7 unchanged) — **improved**

- Receipt, `evidence/after-r90.txt` (rev `11197820`): `C1=met branch_open=0 harm=0 newopen=0 open=22 cases=78`, rc 0; `BATTERY cases=18 branch_cases=14 branch_open=0 harm=0 newopen=0`.
- Before, `evidence/controls-r90.txt` (rev `037c02ca`): `C1=unmet branch_open=8 harm=0 newopen=0 open=30 cases=78`, rc 1.
- Plain re-derivation of the population: `round-89/r/Mo89R03Repair-evidence/cases.json` = 59 cases (30 reject, 29 met); `round-89/r/Mo89C02Critic-evidence/heldout-all.txt` = 23 `HCASE` lines (13 reject, 10 met); 4 command strings shared (python, distinct commands) → 78 distinct. Matches `cases=78`.
- Plain battery count (python `json`): 18 cases; `class`/`expect`: `reject/branch` 14, `met/prov` 4. Meets frozen `branch_cases >= 12`.
- Plain code check: `invocations_visited` absent at 037c02ca, present at e5200aff (`round-87/count-c2.py`, 721 → 930 lines); round-90 counter's `BRANCH` set has 8 ids (`branch_ids_frozen` check).
- Re-measured: population and battery composition only. Harm and open counts: evidence-verified (not re-run).
- Caveats, routed not waived: the critic's 21-string lookup wrapper reaches the frozen `C1=met` line (`Mo90C01Critic.md` §1, disclosed); battery `class`/`expect` labels are the author's words (§4c). The landed rule is a grammar walk and is the measured subject; the predicate cannot prove that.

### C2 — calibration (score 5 unchanged) — **improved**

- Receipt, `evidence/after-r90.txt` (rev `11197820`): `C2=met mutants=15 killed=15 survivors=0 unattributed=0 unanchored=0 isolated=0 literal_anchors=0 arms=29,27`, rc 0.
- Before, `evidence/controls-r90.txt` (rev `037c02ca`): `C2=unmet mutants=15 killed=12 survivors=3 … arms=28,26`, rc 1.
- Plain check of the three new arms (`git grep -c` over `.ufo/waves/round-88/`): `own_ok_arm_count`, `met_line_call_site`, `clone_root_negative` each 0 at 037c02ca; present at e5200aff (`round-88/count-c1.py`: `own_ok_arm_count` ×2; `round-88/count-c2.py`: `met_line_call_site` ×2, `clone_root_negative` ×2). Consistent with killed 12 → 15 and survivors 3 → 0.
- Landed subjects byte-identical to the candidates the reviewer measured per mutation: `w1/candidates/r88-count-c1.py` = `round-88/count-c1.py` (`efe4f1f7…`); `w1/candidates/r88-count-c2.py` = `round-88/count-c2.py` (`fe9ed6ac…`).
- Limit found by the lane's own reviewer, verified in the report text (`Mo90R02C2.md` F1, HIGH, open): the frozen kill clause `failset(out) == {arm}` is satisfied by a label-accurate forger whose counter output is byte-identical to the honest candidate's. Therefore the `C2=met` line alone does not establish honest kills. The discriminating evidence is the per-mutation matrix on the landed bytes (each declared count-c1 mutant reds with exactly its declared label, tally 28/1), which I did not re-run. The count-c2 side's per-mutation evidence rests on `Mo90E03ArmsB46.md` and `Mo90M01Mut.md`, not re-run here.
- Re-measured: arm presence and byte identity. Kill counts: evidence-verified only.
- F2 (MEDIUM, open): B4 pin sees one spelling of the call; equivalent call sites are outside P-C2.

### Harm and other axes

- `git diff d1c84889 e5200aff -- SCORECARD.md`: additive only (+64 lines, `## Round 90`); no score row or prior entry changed. Depth, freshness, coverage, adjacency: no claim, unchanged.
- No-harm evidence: `NOHARM harm=0 open=0 gained=3 cases=34` at tip is reported in the report and `corpus/QUALITY.md`, not in a committed receipt. Evidence-verified weakly (routed R10).
- Verdict per axis: operability **improved**; calibration **improved**; harmed: none measured.

## 3. Discernment spot-check (LEARNING.md; `corpus/lessons/round-90.md` `## Gate`)

Sample: ≥1 admit (items 1–4) and ≥1 reject (item 5). Plus one newly written `corpus/SOURCES.md` row checked for its ≤25-word quote (S612, item 1).

| # | Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|---|
| 1 | S612 POSIX §2.9.3 Lists | admit | Pinned copy `.ufo/waves/round-90/w1/Mo90S01Sources/sources/posix-shell-v3-chap02.html` (357953 bytes, sha256 `0889867a…` = row). Quote "shall have equal precedence and shall be evaluated with left associativity" occurs once in tag-stripped text (11 words, ≤25) | agree | The sentence states equal precedence and left associativity. It supports the AND-OR clause and does not overreach |
| 2 | S614 POSIX §2.15 `exit` | admit | Same pinned file. Quote "The exit utility shall cause the shell to exit from its current execution environment" occurs once (14 words) | agree | Grounds "sequencing after a literal exit" for the current environment only |
| 3 | S615 Python ast `walk` | admit | Pinned copy `python-ast-3.15.2.html`: 362493 bytes ✓. Quote "Recursively yield all descendant nodes … in no specified order." occurs once (18 words) | **agree on the decision; disagree on the recorded digest** | The row's full sha256 `7891c58897fe9f78…8b1f8a60ad1a6f0` is not the file's digest `7891c58897fe9f78…94b0f83b9a8a42f5`. The 16-character prefix matches the seat report (`Mo90S01Sources.md`). Defect R8 |
| 4 | S616 Python tokenize comments | admit | Live `https://docs.python.org/3/library/tokenize.html` re-opened 2026-11-05: "The scanner in this module returns comments as tokens as well" in the module introduction (line-wrapped). Pinned copy sha256 `6842ed0f…` = row; quote occurs once | agree | The scanner returns comments as tokens; grounds reading the token stream, not execution |
| 5 | Reject: `https://pubs.opengroup.org/onlinepubs/9799919799/utilities/exit.html` | reject | Live re-open 2026-11-05: HTTP 200 HTML, JavaScript-redirect notice and a link index to `V3_chap02.html#tag_19_22`; no DESCRIPTION text | agree with the reject and its flip condition | No specification text is present, so no quote can be located. **Curation disagreement:** the rejection is recorded only in the lesson, not as a `corpus/SOURCES.md` row with `REJECTED: <reason>; flip: <…>` (prompt §2b.1; CORPUS row rules). Defect R9 |

Result: decisions agree with the outside check on all five items (admits 1–4, reject 5). Two curation defects (items 3 and 5) are recorded and routed. Gate decisions are not changed.

## 4. Trend verdicts (evidence)

- **expansion — improved.** Five mined rows (S612–S616), one knowledge entry (`corpus/knowledge/branch-reachability-r90.md`), one held-out battery and one capability row (`SCORECARD.md` `## Round 90`) on ground the coverage map did not hold. Census `mori ok`, rc 0, 384 → 389 rows.
- **quality — improved.** Measured harm 0 and newopen 0 on the 78-case population and the 18-case battery (committed receipt). QUALITY 190–192 each carry a "shown able to fail" line. Open defects (F1 HIGH, F2, lookup table, survivors) are disclosed in the report and routed, not left unmarked.
- **discernment — unchanged.** The outside spot-check agrees on five of five decisions. The rule-shape gap (lookup table) and the kill-clause forgery (F1) remain open: the frozen counters cannot separate a real pass from a constructed one. The S615 digest and the missing rejection row are curation defects. No improvement is demonstrated.

## 5. Routed defects for mori round 91 (owner: mori lane)

- **R1 HIGH — forgeable kill attribution (F1, `Mo90R02C2.md`).** Add a negative control to both counters: a benign no-op edit on a pristine synthetic subject must stay green; a self-seal forger must fail it. This is not in the SCORECARD round-91 plan; add it.
- **R2 — P-C1 lookup-table reachability (QUALITY 191).** Already planned: counter-synthesized, per-run-nonce population.
- **R3 — battery trust.** `class`, `expect`, `reach` and `branch_cases >= 12` are read from the file. Add a guard or synthesize the population inside the counter (`Mo90C01Critic.md` §4c).
- **R4 — `--scratch` ignored by the C1 selftest** (`count-c1.py:223`; six synthetic directories left under `/tmp`). Counter amendment; already planned.
- **R5 — `BATTERY` line prints six fields** where the frozen sentence names four (`Mo90Se01Boundary.md` §5).
- **R6 — landed-rule mutant survivors (7 of 24)**: N10, N15, N17, N20, N21, N23, N24 (`Mo90M01Mut.md` Table 1).
- **R7 — F2 (MEDIUM): B4 pin is spelling-specific.** Spelling-independent arm or a source-level scan.
- **R8 — S615 row digest.** Correct the full sha256 by appended correction to the row: the pinned file's digest is `7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5`.
- **R9 — rejection not recorded as a row.** Add the `exit.html` rejection as a `REJECTED: …; flip: …` row in `corpus/SOURCES.md`, or record why not.
- **R10 — measured figures not in committed receipts.** The `rev=e5200aff…` lines and the `NOHARM` output are cited only in the report. Commit them as receipts, or cite byte identity (counter, subject and battery bytes are identical at 11197820 and e5200aff).
- **R11 — attack-share figure.** Report says 4/13; lesson says 5/13. Reconcile to the spec roles.
- **R12 — no planner seat in w1** (prompt §3 names 1× planner; planner is mandatory per judged round). Name a planner seat in the round-91 wave; the L1 holding the role is not a seat.
- **R13 — attribution.** Second report commit `8151e9ad` under lane identity, labelled as a hyaku sweep. Recorded; no action beyond the label.
- **R14 — operator-side (not lane).** Rendered prompt lacks a verbatim commit-before-report ordering and hash-citation clause.
- **R15 — fleet-root hygiene (not lane).** At closure the fleet root shows a staged zero-byte `mo.tip` and a modified `.scratch/run15-state.json`. The report names only `mo.tip`.

## 6. SHONEN

No box is checkable by a non-author from this round alone. Box 4 (no cross-domain bleed) is plausible from the diff, but its sweep was not run here. No `[x]` written. Operator decides promotion.
