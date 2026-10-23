# Round 37 verifier spot-check — mori (non-author)

author: hyaku closure (non-author integrator, @m_flash)
date: 2026-10-23
lane round: mori 37 (attempt 1, `hyaku-inline`); lane tip observed at verification `1ae1d6d69282f6c4f51355308db6a4be9a8e3d42` (the filed report cites `0a05f7e6…`, an ancestor); fleet report `.ufo/reports/round-37/mori.md` at `31d412cde0f47253d1906a16db6aac8547b77445`, author `mori-shokunin <mori@shokunin.local>`.

## Step-1 conformance

- **Report identity.** `git log --format='%an <%ae> %H' -- .ufo/reports/round-37/mori.md` → three lane commits, final `31d412c` by `mori-shokunin <mori@shokunin.local>`. PASS.
- **`SHONEN` heading.** Present, one line per box, all four `[~]` with pointers; no `[x]` was written. PASS as report contract (author-asserted, not a promotion attestation).
- **Cited commits.** `git -C mori-shokunin merge-base --is-ancestor <h> master` for `842a320 842a32074…`, `e57c58b5`, `bcf65505`, `5dff52a1`, `52d636d5`, `4bec58eb`, `c31076ed`, `0a05f7e6`, `6bd57097`, `f10a320d`, `8ff9bba` → all PASS. Blobs `7518fef8` (count-c1) and `6213cf9a` (count-c2) exist; their sha256 (`86699627…`, `71c72929…`) match `evidence/freeze-r37.txt` at both `e57c58b5` and the tip — the frozen counter bytes never moved. The contract blob moved `61a768a3` → `d2d61144` only by the appended `## Post-data corrections` section (`git diff e57c58b5 1ae1d6d -- contract.md` is additions only); P-C1/P-C2 bytes are unchanged.
- **Lane state.** `scripts/hyaku/jj-lane.sh state mori-shokunin` → `branch=master local=1ae1d6d… remote=1ae1d6d… ahead=0 behind=0 tracked=0 untracked=2`. `git status --porcelain` → `?? .scratch/` (disclosed operator item) and `?? .ufo/waves/round-37/w1/RevR17JJ.md` (late wave-1 seat report, mtime 17:15:55, after the last lane commit 17:15:22). Disposition in *Routed defects / notes*. No uncommitted round work. PASS.
- **Prompt fidelity.** `.ufo/prompts/mori-round-37.md` (committed at fleet `e17606c`) carries the round contract: report path/filename l.101, `SHONEN` heading l.118, commit-hash citation l.107/281, commit-then-report ordering l.325, lane write scope in addendum §3; round-level mission/axes §1, L2 floor ≥8 in one batch §3 (matches `MISSION.md` §L2 — 8), commit-then-push and push scope §5, L0 side channel §5; the hyaku addendum §6 is present verbatim. No L2 route map is quoted (roles route through the host table), so the `MISSION.md` bucket cross-check is N/A. PASS.
- **Wave shape.** `w1-spec.json` carries 73 items: executor 24, reviewer 10, scout 8, scribe 7, critic 6, mutation-tester 5, connector 4, revenger 4, sentinel 3, simplifier 2 — exactly the report's mix; attack roles 10+6+5 = 21/73 = 28.8% ≥ 25%. `w1-plan.json` `counts.spawn=73`; `w1-validate.log` is empty (the exit-0 claim is report-asserted, not re-derivable from a 0-byte log). Spec/plan/taskCall/validate log are committed.
- **Report versus the lane's own corrections.** The filed report predates the lane's post-report corrections `5631efa`/`1ae1d6d` and still labels C2 freshness and counts 2/73 wave returns; the lane's later commits re-attribute C2 to operability and land 41 seat reports. The report is a record and its cited tip is a real ancestor, so this is status-neutral — but the correction was not swept (R1/R2).

## Per-claim re-check

Re-measured = I ran the command this session over committed bytes. Evidence-verified = I resolved the committed receipt/artifact and did not execute the surface.

### C1 — measurement discrimination (calibration; declared score 5, tied lowest) — **re-measured**

- **Before.** The printed command uses a lane-relative `--tool`; run from the lane root the round-36 counter resolves it inside each sandbox (`can't open file '//.ufo/waves/round-37/fixtures/memo-n1.py'`), so the printed form exits 1 (`C2=unmet`). With the lane-absolute fixture path it reproduces: `python3 .ufo/waves/round-36/count-c2.py bf0df77 --tool $LANE/.ufo/waves/round-37/fixtures/memo-n1.py --seed 11` → blind 24/24, real arm pass, `C2=met`, exit 0; same with `summary-only.py --seed 12` → `C2=met`, exit 0. Matches `evidence/c1-before-memo.txt` / `c1-before-summary.txt`. The defect is the command form, not the value (R4).
- **After.** `python3 .ufo/waves/round-37/count-c1.py c31076ed --seed 20261023` → blind 24/24 (coverage deletions=20 changed-back=15 superseded=9), real arm pass, `appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]`, challenge arm pass, `negative memo-n1.py rejected (challenge: …)`, `negative const.py rejected (blind 4/4 …)`, `negative summary-only.py rejected (blind 4/4 …)`, `C1=met`, exit 0. Seed `5097152322487907681` reproduces the report's re-score `C1=met`, exit 0; at the lane tip `1ae1d6d --seed 3737` → `C1=met`, exit 0.
- **Verdict: improved.** The r36 counter admits both a real-arm memoizer and a summary-only printer; the r37 counter rejects both while the honest tool passes all arms. QUALITY 106/107 cite lessons M2/M3 and show the old counter's `C2=met`.

### C2 — drift-probe hardening verification (corrected axis: operability; declared label freshness) — **re-measured (counter); gate/live surfaces evidence-verified**

- **Before.** `python3 .ufo/waves/round-37/count-c2.py 842a320` → `tool_present PASS`; `selftest FAIL` (4 arms: exit_code, missing_sources_exit2, row_states, summary); `cap_kill FAIL` (`huge_cap=None`), `redirect_kill FAIL` (`redirect_private_refused=None`), `knowledge FAIL`, `capability FAIL`, `readme FAIL`, `live FAIL`; `C2=unmet`, exit 1. Matches `evidence/c2-before.txt`.
- **After.** `count-c2.py c31076ed` and `count-c2.py 1ae1d6d` → all eight checks PASS (`selftest` 6 arms incl. `huge_cap`, `redirect_private_refused`; `cap_kill` exit 1 `huge_cap=FAIL`; `redirect_kill` exit 1 `redirect_private_refused=FAIL`; `knowledge` rows S205/S221–S225 + `8ff9bba`; `capability`; `readme`; `live`), `C2=met`, exit 0.
- **Gate evidence (verified, not executed in place).** The registered probe's six-arm selftest and the live sweep line `MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162` (exit 1) are resolved from `evidence/c2-after.txt` / `drift-live-r37.txt`; I did not re-run the live fetch. The r36 debt (d) receipt `evidence/r17-jj-selftest-r37.txt` shows `EXIT=0` with the `pre_fix: 9/204 red` line; the late seat `w1/RevR17JJ.md` independently kills the XDG-escape mutant (PASS, untracked, see notes).
- **Verdict: improved** (on the lane's corrected axis, operability; see R1 for the unswept label).

## Axis verdicts

| axis | verdict | evidence |
|---|---|---|
| calibration | **improved** (5 held) | C1 before/after re-measured above; r36 measurement-discrimination defect closed; QUALITY 106/107 grounded in M2/M3 |
| operability | **improved** (7 held) | two named mutation-killable arms; `cap_kill`/`redirect_kill` PASS under their own mutation; capability row + corpus binding (allowance: capability first-working mislabeled, R5) |
| freshness | **unchanged** (5) | the lane's own post-data correction re-attributes C2 to operability and claims no freshness move; the live sweep is byte reproducibility, not a freshness verdict (QUALITY 105). The freshness axes cell still carries the superseded r37 attribution (R1) |
| coverage | unchanged (6) | scores byte-identical at `842a320` and `1ae1d6d` (`sed -n '6,17p'` SCORECARD both sides: 6/7/5/5/5/6); round ground is recorded as coverage-map rows, no score move claimed |
| depth | unchanged (5) | no depth claim; the hardening entry deepens one technique, not the axis score |
| adjacency | unchanged (6) | changed-path sweep `842a320..1ae1d6d`: every path is inside `mori-shokunin`; no sibling, operator, `MANIFEST.json`, `PROTOCOL*`, `MISSION`, `AXES`, `CORPUS`, `.ufo/state` or watchdog path touched; `PROVINCE.md` untouched |

No axis harmed: SCORECARD scores are unchanged and the diff is the Round-37 section, capability rows and two evidence-cell clauses.

## Discernment spot-check (LEARNING.md — from outside)

The round's Gate records five admits and **no new reject** (`Rejected: none new`); the reject half is sampled from the carried rejection the lane's Gate still cites, and the round's S222 scope-qualified admit is treated as a reject-of-scope decision.

| item | decision | re-opened source | agree? | reason |
|---|---|---|---|---|
| S225 (Fetch Standard §4.5) | admitted, mined | committed copy `corpus/evidence/sources-r37/S225.src:8355` | **agree** | “redirect count is 20, then return a network error” (9 words, words in order across `<var>`/`<a>` markup — the lesson discloses the interleaving); the row's twenty-hop chain limit is faithful and its `teaches` correctly warns that final-URL-only checks leave hops unchecked |
| S221 (RFC 9110 §15.4) | admitted, mined | `S221.src:7232-7234` | **agree** | The 25-word quote is contiguous (line-wrapped) and states exactly the 3xx-class semantics the row teaches; the “3xx is not the body” grounding is sound |
| S222 (OWASP SSRF) | admitted with scope narrowed | `S222.src:5031` | **agree with the decision** | The 23-word quote grounds redirect-following as an input-validation bypass; the lane refuses the blanket “disable redirects” advice for a probe that must follow and records the final-destination-only limit — correct discernment. Its cited “search-log note” is absent from `corpus/SOURCES.md` (R3) |
| S211 (PMC mirror of Nosek 2018) — reject (carried) | rejected row kept | `corpus/SOURCES.md` S056 and S211 | **agree** | S056's source cell already carries `pmc.ncbi.nlm.nih.gov/articles/PMC5856500/`; a mirror row rechecks nothing new; the rejection is kept as evidence per the contract |

Census (closure step 3): `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → exit 0, `mori ok …`, W04 duplicate-URL lines only (S035 S037 S073–S076 S147–S150 S166 S168 S201 S218 S220); row count `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → 220 at `842a320`, 225 at `1ae1d6d`; `git diff --numstat 842a320 1ae1d6d -- corpus/SOURCES.md` → `7 0` (no row cell edited in place).

## Trend verdicts

- **expansion: improved** — five new rows S221–S225, all `mined`, each `used-by corpus/knowledge/source-drift-hardening-r37.md`; one new knowledge entry on ground the coverage map did not hold (redirect/SSRF/ptrace semantics), and the README coverage map gains both the missing r36 row and the r37 row (`count-c2.py` `readme PASS`); two capability rows demonstrated running; census exit 0 at closure. Measured: rows 220 → 225.
- **quality: improved** — the hardening entry names both policies with code lines, five disclosed limits, and the two arms are each killed by their own textual mutation (re-measured `cap_kill`/`redirect_kill` PASS); QUALITY 106/107 convert r36 routed defects into criteria with fail states; the r36 nine-row drift prose was re-verified (debt h). No admitted entry was found false or left unmarked. The disclosed P-C2 content-discrimination gap (M9) is routed, not hidden.
- **discernment: improved** — the round's own defects M1–M9 are mined with fixes and shown-able-to-fail evidence, four wave-1 corrections landed (contract/SCORECARD/lesson), and this outside spot-check agrees with every sampled decision (three admits, one carried reject). Caveats kept visible: the round's gate produced no new rejection (R3), and the correction sweep is incomplete (R1/R2) — both routed rather than folded into the grade.

## Routed defects (round 38; status-neutral)

1. **R1 — correction not swept.** The C2 re-attribution (C2 = operability, freshness not moved) is stated in `contract.md` (post-data section), `SCORECARD.md` (post-data corrections) and `corpus/lessons/round-37.md`, but the superseded freshness attribution remains in `SCORECARD.md:13` (“round-37 claim C2 verified …”), the operability axes row carries no round-37 pointer, `LOG.md`'s Round-37 entry still declares “C2 (freshness 5)”, and the filed report still labels C2 freshness. Fix: append a round-38 LOG correction naming the superseded text, move the round-37 pointer to the operability cell, and record the erratum in the next report.
2. **R2 — LOG.md append-only violation.** `5631efa` rewrote the filed Round-37 `LOG.md` entry in place (10 lines changed, 2 removed: census line, r17 line, M1–M5 line, Held line) instead of appending a correction. Fix: a round-38 appended correction entry naming the superseded text (also record M6–M9, debt (f) reopened, capability first-working).
3. **R3 — search-log note.** `corpus/SOURCES.md:280` ends mid-sentence at “unchecked-intermed…”, and the S222 scope-qualification note the lesson cites (“search-log note, `corpus/SOURCES.md`”) is absent; the round's Gate records no new reject. Fix: append the complete rule-5 note (question, where, date, identified/screened/included/excluded, exclusion reasons, stop rationale, S222 narrowing) and record a rejection when the next gate has one.
4. **R4 — before-receipt command not re-runnable.** The report and `evidence/c1-before-*.txt` print `--tool .ufo/waves/round-37/fixtures/…` (report) / `<lane>/…` (erratum), but the r36 counter executes `--tool` from each sandbox repo: the printed form yields `can't open file '//.ufo/…'` → `C2=unmet`, exit 1. Reproduction needs the lane-absolute path, which yields `C2=met`, exit 0 (observed). Fix: print `$LANE/…` with `LANE` defined, or teach the counter to resolve a lane-relative `--tool`.
5. **R5 — capability first-working.** `round-37 C2` (“source-drift re-fetch probe”) is registered first-working 37, but the probe's live run already worked in round 36 (`evidence/drift-live-r36.txt`); the r37-specific capability is the named mutation-killable arms. Fix: correct the cell to 36 or narrow its wording to the r37 addition.
6. **R6 — registry home.** The r37 named arms and the 4 MiB pin are not in the `SKILL.md` registry row (“source drift (r36)”, `SKILL.md:874`); a r37 row exists only as a draft in `w1/ScribeSkill.md`. §Gate standard requires the registry row at the lane's registry home. Fix: update the row's self-test/pinned-values cells (or state why the r36 row suffices).
7. **R7 — disclosed, carried.** P-C2's content half remains token-checkable (M9 → content-anchor arm); SentTools MEDIUM/LOW counter hygiene (`show()` bounds, relative `--tool`); debt (f) SIGTERM→5 s→SIGKILL re-filed as an operator-owned tradeoff; frozen r36 residuals (count-c1 docstring “v1”, delete+restore blind spot, unexercised 429 path). `count-c1.py` has no `--selftest` and should stay a claim counter, never registered as a gate.

## Notes

- **Untracked disposition.** `.ufo/waves/round-37/w1/RevR17JJ.md` (6,340 B, mtime 17:15:55, after the lane's last commit) is a late wave-1 seat report — `VERDICT: PASS`, independently kills the r17-jj XDG-escape mutant and confirms debt (d). It is not lane round work at report time; commit it with round 38's wave artifacts under the lane identity (or a bookkeeping helper commit), never delete. `.scratch/` is the disclosed operator item.
- **Wave trailing.** 41 w1 seat reports landed in `5631efa`/`1ae1d6d` after the filed report; the report's “2 of 73” is accurate for its commit and the later returns are committed wave evidence.
- **Dispatch digest (copied).** `2026-10-23T16:38:12-03:00 launch mori round=37 pgid=2384133 driver=hyaku-inline attempt=1`; orchestrator in-session completion `2026-10-23T~23:55Z complete mori round=37 (in-session L1): landed, lane HEAD c31076ed…`. No watchdog `complete mori round=37` line exists at closure (mutable log); the landed report is the completion evidence.
- **SHONEN for the operator.** All four boxes are `[~]` with resolvable pointers; this non-author resolved each (SKILL.md decision tables/registry, end-to-end counters + receipts, self-contained commands, `PROVINCE.md` untouched). The checklist is fully checkable by a non-author; promotion remains operator-owned and no `[x]` was written here.

## Erratum (closure-time, after the first commit)

- **A3 — hardening-commit attribution is wrong in the filed round.** `8ff9bba` touches no `tools/mori-source-drift.py` byte (`git show --name-only --format='' 8ff9bba | grep -c tools/mori-source-drift.py` → `0`); `git log -S 'FETCH_MAX_BYTES' -- tools/mori-source-drift.py` and `-S '_public_redirect_target'` both name `1caa242` as the commit that landed the 4 MiB read cap and the post-redirect public-destination policy (the r36 closure's own spot-check also records `1caa2423`). The filed report, the contract's C2 heading, `count-c2.py`'s `HARDENING_COMMIT` and `corpus/knowledge/source-drift-hardening-r37.md` all carry `8ff9bba`, so P-C2's `knowledge` check passes on a false pointer; the `cap_kill`/`redirect_kill` measurements are unaffected (re-measured PASS). The lane's trailing wave has the correction in flight (`contract.md` A3, lesson M10, `w1/ExecKnowledgeCheck`) but it is uncommitted at this closure — it must land in round 38 as an erratum naming the superseded text, and the filed report needs the erratum note.
- **A2 — live receipt is the entering sweep.** `evidence/drift-live-r37.txt` is the 220-row entering sweep; the correct post-round line is `rows=225 fresh=53 excerpt=0 drifted=10 unavailable=0 no-copy=162`, with the 220-row sweep under `drift-live-r37-start.txt`. The report's “live demonstration” is a demonstration on the entering tree, not the landed tip; it was never claimed as a freshness verdict (QUALITY 105).
- **Uncommitted trailing corrections at closure.** The lane's trailing wave is applying A1 (`count-c1.py` v2, real-drawn arm from `w1/RevC1Challenge`), A2 and A3 plus new seat reports to the lane working tree. At the moment of this erratum `git status --porcelain` shows 9 tracked modifications (`contract.md`, both counters, `drift-live-r37.txt`, `LOG.md`, `SCORECARD.md`, `corpus/README.md`, the r37 knowledge entry, `corpus/lessons/round-37.md`) and 25+ untracked wave returns (including `RevR17JJ.md`, `c1-after-v2.txt`, `freeze-r37-v2.txt`). These are post-report lane corrections, not the filed round's work; they are uncommitted at closure and named as a round-38 obligation. They do not change the frozen v1 bytes the filed report scores: the freeze pins `7518fef8`/`6213cf9a` still match `e57c58b5` and the pre-erratum tip `1ae1d6d`. The step-1 “no uncommitted round work” PASS above is therefore scoped to the filed state; the trailing edits are the named defect.

## Closure-time update — the A1–A3 corrections landed

The erratum above was written while the lane's trailing wave was mid-integration; its “uncommitted” bullet is superseded. Before this closure the lane committed the corrections and re-scored on new counter versions:

- `4bfa0490` — A1–A3: `count-c1.py` v2 adds the run-time-drawn ancestor-rev arm and makes the challenge title the lane's real title; `count-c2.py` v3 reconstructs the hardening commit and requires it to touch the tool; the drift receipt is regenerated as the 225-row tip sweep; `SKILL.md` gains the two Round-37 registry rows; lesson M10.
- `a1875349` — the v2/v3 receipts (`evidence/c1-after-v2.txt`, `c2-after-v3.txt`), `evidence/freeze-r37-v3.txt`, and an appended `LOG.md`/`SCORECARD.md` re-score (the append is the correct form for the earlier in-place rewrite).
- Final lane state at this verification: tip `e37dcc6d…` (includes this spot-check and its erratum), `ahead=0 behind=0`, tracked=0, untracked=1 (`.scratch/` only — the late `w1/RevR17JJ.md` was committed in `4bfa0490`).

Re-measured on the corrected counters at `e37dcc6`, over committed bytes:

- `python3 .ufo/waves/round-37/count-c1.py e37dcc6 --seed 20261023` → blind 24/24, real arm pass, **drawn arm pass** (`rev=4890c2d571 base=1caa242328`), challenge arm pass, `memo-n1`/`const`/`summary-only` rejected, `C1=met`, exit 0. Matches `evidence/c1-after-v2.txt` (seed 20261024).
- `python3 .ufo/waves/round-37/count-c2.py e37dcc6` → all eight checks PASS, `knowledge … cited_commit=True touches_tool=True`, `live PASS`, `C2=met`, exit 0. Matches `evidence/c2-after-v3.txt`.
- Freeze v3 pins verify at `e37dcc6`: contract `b68737e0`, count-c1 `3e15f9fd` (sha256 `5279ed9d…`), count-c2 `0eb8ff47` (sha256 `f173a642…`), drift tool `162ee87b` — all equal `evidence/freeze-r37-v3.txt`. The v1 pins (`7518fef8`/`6213cf9a`) remain the pins of the filed v1 bytes.

Resolution of the items in the erratum and the routed list:

- **A3 — corrected.** The knowledge entry, README, contract and counter now cite `1caa242`; the v3 `knowledge` check proves the commit touches `tools/mori-source-drift.py` (`touches_tool=True`). The filed fleet report (fleet `31d412cd`) still prints `8ff9bba` — a record cannot be rewritten, so an erratum naming the superseded sentence is still owed in round 38.
- **A2 — corrected.** `evidence/drift-live-r37.txt` is the 225-row tip sweep (`rows=225 fresh=53 excerpt=0 drifted=10 unavailable=0 no-copy=162`); the 220-row entering sweep is `drift-live-r37-start.txt`; S223 is disclosed as a byte-unstable page (S211 class).
- **R3 — resolved.** The Round-37 search log now carries the S222 “blanket disable-redirects” scope note.
- **R6 — resolved.** `SKILL.md` carries the two Round-37 registry rows (`source drift (r37)` probe with named arms and pinned values; `C1 counter challenge arm (r37)` probe with its verdict map and pins).
- **R1 — open.** The SCORECARD axes cells were not swept: the `freshness` cell still says “round-37 claim C2 verified …” while the post-data correction re-attributes C2 to operability and the `operability` cell carries no round-37 pointer. Route to round 38 (append-only correction).
- **R4 — open, minor.** The before-receipt command still prints `--tool <lane>/…`; the runnable form needs a defined `LANE` variable (reproduction with the absolute path gives `C2=met`, exit 0).
- **R5 — open, minor.** The `source-drift re-fetch probe` capability row still reads first-working 37; the probe's live run worked in round 36, so the cell is either 36 or the row narrows to the r37 named-arm verification.
- **R2 — historical.** The `5631efa` in-place rewrite of the filed LOG entry remains in history; `a187534` appends the amendment correctly. Round 38 records the breach and the superseded text.
- **Carried, disclosed:** P-C2's content-half gap (M9 → content-anchor arm), SentTools MEDIUM/LOW counter hygiene, debt (f) SIGTERM→grace→SIGKILL as an operator-owned tradeoff, and the frozen r36 residuals (count-c1 docstring “v1”, delete+restore blind spot, unexercised 429 path) stay routed to round 38.

Admission on the corrected state: both claims re-measured met (C1 v2, C2 v3), both filed v1 receipts also re-measured met, no axis harmed. The open R1/R4/R5/R2 items are documentation defects, routed, not measurement failures.
