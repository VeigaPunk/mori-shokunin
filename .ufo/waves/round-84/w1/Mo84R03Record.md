# Mo84R03Record — record discipline and revision-precision attack (round 84, wave w1)

Seat: Mo84R03Record (reviewer/recorder, leaf — no subagents). Date: 2026-11-04.
Scope: read-only on lane files except this report. Lane HEAD at measurement: `39190f8a`
(freeze `daa77bd5` + A1 `dbdb1aaa` + A2 `39190f8a`). Entering revision `5adf4337`.
All experiments ran under `/fast/scratch/hyaku/mori-r84/Mo84R03Record/` (deleted before yield).
No tools installed; no pacman transaction; no lane, OS or orchestration state touched; no
mutating git/jj command against any real repo.

Frozen authority read: committed `.ufo/waves/round-84/contract.md` at `39190f8a` (the worktree
copy additionally carries uncommitted pre-data amendments A3/A4), the three frozen counters,
`evidence/controls-r84.txt`, `SCORECARD.md ## Planned (round 84)`, QUALITY 168/169
(`corpus/QUALITY.md:1818-1851`), `Mo83R01C1.md` §6, `round-83-verifier-spotcheck.md`.

Conventions below: "contract" = committed bytes at `39190f8a` unless noted; "worktree" = the
lane working tree as it stood during this seat (several sibling seats' outputs in flight,
listed where relevant).

---

## 0. Verdict

The three claims are gradeable as frozen, and every entering control and the C1 population
control reproduce exactly under my own runs. I found **no target reachable by a stub** on C1
(graded from real subject bytes), **output-forgeability residuals** on C2 and C3 (named, not
blocking, consistent with the registry's standing "adaptive output forgery" named limit), and
**five prose-vs-code divergences** inside the frozen contract itself (F1–F5), of which two are
internally contradictory contract text (F1, F4). The largest record risks for the round are:
(a) measurement-protocol step 1 is only half-landed — the freeze-commit population-control
receipt is not committed at HEAD (it exists only as the untracked
`evidence/controls-verify-r84.txt`); (b) the executing-counter-bytes-vs-graded-revision gap is
real, now canonicalized by uncommitted A4 for the population control but unaddressed for the
after-receipts; (c) SKILL.md is untouched while PROVINCE (uncommitted) already names "registry
row 18".

---

## 1. Same-sentence check (contract predicate ↔ counter code ↔ receipt label)

### C1

- **Predicate ↔ receipt label: MATCH.** `count-c1.py:316-319` prints
  `C1=%s %s detector=%s rev=%s`; the population control I ran prints exactly the contract's
  frozen line plus the `rev=` suffix (the suffix is present in the committed
  `controls-r84.txt` format too, so the "same sentence" holds modulo the revision stamp).
- **F1 — the frozen four-mutant table is not the counter's table (prose stale post-A2).**
  Contract lines 40-43 still carry the pre-A2 anchors: M24b old =
  `return rc == 0 and "fail=0" in out and not FAIL.search(out)` (occurs **2×** in the graded
  r83 bytes — `green()` body and the r83 counter's own MUTANTS table literal,
  `git show 5adf4337:.ufo/waves/round-83/count-c1.py` lines 33 and 129), M24c/M24d old =
  `and not unclassified and residual == 0` (occurs **0×** — the `met` expression wraps the two
  conjuncts across lines 241-242). The counter at HEAD (MUTANTS tuple, count-c1.py:34-46) and
  the A2 amendment's corrected table (contract lines 188-191) agree with each other:
  M24b old = 4-space-indented `return …` (unique), M24c old = `and not unclassified`,
  M24d old = `and residual == 0`, both new = empty. Measured at the freeze revision:
  each A2 anchor occurs exactly once (1/1/1, my grep counts). **A reader hand-deriving anchors
  from the contract's top table gets 2/0/0 and would conclude the target is unreachable — the
  operative table is the A2 amendment's, and the top table should carry a supersede pointer.**
- **F2 — the `blind_case_tally` prose is arithmetically wrong (fixed only in uncommitted A4).**
  Contract line 61: the arm's fixture "must print `killed=0 survivors=1`". The counter's arm
  (count-c1.py:213-220) asserts `killed==1 and survivors==1 and total==2 and not met` — one
  killed mutant *makes* `killed=1`; asserting `killed=0` fails on the pristine counter (A4
  records the measurement `pass=7 fail=1`). Under the M24a mutant the fixture prints
  `killed=2`, which is what kills it. The receipt never prints the arm assertion, so this is a
  contract-sentence defect, not a grading defect.
- **F3 — "both `old` anchors" is wrong.** Contract line 64 says "both `old` anchors above must
  still occur exactly once"; there are four. Stale wording; after A2 the c2-side anchors are
  the two wrapped conjuncts, not the single-line form the table above the sentence shows.
- **F4 — code is weaker than the target on the killed/equivalent split.** `grade()`'s met is
  `pristine_ok and total > 0 and survivors == 0 and no unanchored/empty/coupling extras`
  (count-c1.py:176-180): it does **not** require `total==4`, `killed==2` or `equivalent==2`.
  A run printing `C1=met mutants=4 killed=3 equivalent=1 survivors=0 total=4` (e.g. if an
  M24c mutant were killed by a new arm instead of adjudicated) would exit 0 and miss the frozen
  target string. The record must check the **literal target line**, not rc 0 alone. The
  predicate sentence's `killed=K equivalent=E` placeholders encode this gap.
- Kill rule, green rule, unanchored/empty-mutation/coupling handling, pristine-before-mutants
  ordering, and the in-same-invocation detector gate (`met and own_ok`, count-c1.py:318) all
  match the prose exactly. The two named seat arms `blind_case_tally` and
  `green_requires_fail_zero` exist verbatim in the counter's selfcheck (I ran it:
  `C1_COUNTER_SELFTEST pass=11 fail=0`).

### C2

- **Predicate ↔ receipt label: MATCH.** Met line prints `C2=%s arm=all-rows defeated=%d
  fixtures=%d/3 bindings=%d revisions=%d arms=%d rev=%s` (count-c2.py:297-299).
- Frozen rule (all-rows on both sides, `row-value` at line 1 for an empty carrier selection,
  `rev-bytes` for an empty blob) is what the fixture verdicts enforce: `new_red` requires
  rc 1 + `revisions>=1` + `REVISION_MISMATCH` + a `row-value`/`rev-bytes` token (count-c2.py:265-269).
- **F5 — code is weaker than the fixture table on the mismatch kind and line.** The contract's
  table (lines 88-96) fixes carrier-ambiguous → `row-value` at row 2 and rev-ambiguous →
  `rev-bytes` at row 2; the counter accepts either token from either fixture, and never checks
  the row number. Same class as F3: the receipt's `defeated=2` is guaranteed, the per-fixture
  kind is not. Same class also for `arms=44`: the code enforces `arms >= ARMS_FLOOR(44)`
  (count-c2.py:249), the target names 44 exactly.
- `bindings=3` is enforced twice: exact-set population match against
  `.ufo/waves/round-82/record-pins.json` (verified byte-equal to the FROZEN tuple) and the real
  run's printed `bindings=3` + `revisions=0` + rc 0 (count-c2.py:294-295).
- Fixture construction matches the frozen table byte-for-byte (ROW_A/ROW_B/body_a/body_b,
  count-c2.py:117-139); the entering-tool side is pinned to `OLD_REV = 5adf4337` (line 22).

### C3

- **Predicate ↔ receipt label: MATCH.** Met tail requires `delta==classified`, `tokens==64`,
  `classified==union>0`, `residual==0`, `live==derived`, and
  `deltas==union-live_agree==len(pairs)` with every pair a frozen class word, no token twice
  (count-c3.py:206-212). The subject prints `LIVE_DELTA <token> <class>` via its notes channel
  (one per line, verified against the r83 counter's `for note in notes: print(note)`), which is
  exactly what the counter's `DELTA_LINE` parses.
- The four delta selftest arms are required by name and PASS (`delta_absent_live`,
  `delta_added_live`, `delta_class_changed`, `delta_agreed`, count-c3.py:186-189); arms floor 16.
- **Prose clause the code cannot enforce:** "no new selftest arm may construct a case where
  `residual` or `unclassified` is non-zero while every other `met` conjunct holds" — a seat
  obligation only; and the "exactly one line for every union token that is not `agreed`" is
  enforced as a count equality plus uniqueness, so a subject that printed one agreed token and
  dropped one non-agreed token would keep the counts equal (named limit, theoretical — the
  graded subject derives the lines from the same data it classifies).

### Cross-claim binding (a strength to record)

C3's seat edits the same bytes C1 grades: the r84 C1 counter re-checks the four A2 anchors and
the three M24d coupling markers in `.ufo/waves/round-83/count-c2.py` at R, so a C3 seat that
broke `and not unclassified` / `and residual == 0` / `agreed == len(snapshot_tokens)` /
`residual += duplicates` / `duplicates == 0` would flip C1 to `unanchored`/`coupling-absent`
→ unmet. The in-flight C3 worktree diff (E03, +41 lines) preserves all five; verified by
inspection of the diff hunk (the `met` conjunct lines are untouched).

---

## 2. Entering-control check

All three controls re-run by me, verbatim, from the lane worktree with
`HYAKU_SCRATCH=/fast/scratch/hyaku/mori-r84/Mo84R03Record`:

```text
$ python3 -I .ufo/waves/round-84/count-c1.py 5adf4337b6510dd246b247092c11cbaa97c930d3
C1=unmet harness=absent rev=5adf4337b651        rc=1     # byte-identical to controls-r84.txt
$ python3 -I .ufo/waves/round-84/count-c2.py 5adf4337b6510dd246b247092c11cbaa97c930d3
C2=unmet arm=absent rev=5adf4337b651           rc=1     # byte-identical to controls-r84.txt
$ python3 -I .ufo/waves/round-84/count-c3.py 5adf4337b6510dd246b247092c11cbaa97c930d3
C3=unmet delta=absent rev=5adf4337b651         rc=1     # byte-identical to controls-r84.txt
```

Each is red for the named reason, verified at the byte level:

- C1 `harness=absent`: `git show 5adf4337:.ufo/waves/round-84/count-c1.py` fails — the r84
  counter did not exist at the entering revision. Not stub-satisfiable: the control is a
  historical fact.
- C2 `arm=absent`: `git show 5adf4337:tools/mori-record-sweep.py | grep -c ALL_ANCHOR_ROWS` → 0
  (marker absent; `REVISION_MISMATCH` present). The entering tool's own selftest prints
  `RECORD_SWEEP_SELFTEST pass=40 fail=0` (I ran it from a scratch export) — the frozen 40 → 44
  delta baseline is real.
- C3 `delta=absent`: `git show 5adf4337:.ufo/waves/round-83/count-c2.py | grep -c LIVE_DELTA` → 0
  and `delta=classified` absent; entering selftest tally is 12 (the QUALITY 171 baseline).
- **Population control at the freeze commit** (contract P-C1): I ran the worktree (A2) counter
  at `daa77bd5`:
  `C1=unmet mutants=4 killed=0 equivalent=2 survivors=2 total=4 pristine=green detector=green rev=daa77bd5684c` rc 1 —
  exactly the frozen line. I also ran the pre-A2 counter bytes (materialized from
  `git show daa77bd5:.ufo/waves/round-84/count-c1.py`): it prints `unanchored ×3`,
  `mutants=1 … survivors=1` — confirming uncommitted A4's warning that the daa77bd5-committed
  counter copy must not be run as the control (seat Mo84E04Controls independently documents the
  same in untracked `evidence/controls-verify-r84.txt` §5(b)).

**Could a stub satisfy the gates?** C1: no — the verdict is computed from the graded r83
bytes; a marker-carrying stub can wear `harness=present` but cannot reach `met` (the r83
reviewer proved the same shape at r83). C2: **in principle yes** — every gate after the
presence check (selftest print, fixture verdicts, real-run summary) is output-graded, so a tool
that prints `RECORD_SWEEP_SELFTEST pass=44 fail=0`, the right `REVISION_MISMATCH` lines with
rc 1 on the ambiguous fixtures and a clean `revisions=0 bindings=3` rc 0 summary on the real
pins would pass without implementing all-rows selection. C3: partially — a stub subject would
have to keep the four C1 coupling substrings intact (else C1 breaks) and print a consistent
selftest + live tail; harder than C2 but not impossible. These are the standing registry named
limits (SKILL.md:357 "adaptive output forgery remains outside…"), recorded here so the round's
record does not overclaim "stub-proof".

---

## 3. Revision discipline

**Where each after-value must be measured:** at the integration revision, per the measurement
protocol step 2, with the counters run from worktree bytes byte-identical to that revision's
counters (or with the executing bytes' identity recorded).

| Counter | Graded bytes source | Worktree-vs-revision exposure |
|---|---|---|
| C1 | subjects + harness presence via `git show rev:path` (loader, count-c1.py:288-291) | The detector selftest runs the **worktree** counter (`os.path.abspath(__file__)`, line 302). The receipt cites `rev=` but the grading logic is worktree. No check compares the counter's own bytes to R. |
| C2 | tool, pins, entering tool, carriers all via `git show` (lines 237-244, 253-256, 281-283) | **Enforced drift check** (lines 284-289): every pins carrier's worktree bytes must equal `git show rev:<carrier>` else exit 2 "measure at the landed tip". A worktree run therefore cannot be cited as a revision run for the carrier side. The counter itself still runs from worktree bytes (same exposure as C1, unguarded). |
| C3 | subject exported from `git show rev:path` into scratch (line 165-166) | The subject's **live census read is live fleet state by design** — unrevisioned and mutable; the snapshot/baseline/cards are read via the subject's own `git show`-based loader. Receipt must be timestamped as an observation (as r83 did). |

**Paths where a worktree run could be cited as a revision run (named for the record):**

1. **All three counters execute worktree bytes; none verifies its own bytes against R.** A4
   canonicalizes this for the population control ("the control is the worktree counter at HEAD
   grading the freeze revision's r83 bytes") but the measurement protocol's after-step does not
   carry the same clarification. `after-r84.txt` must either be taken from a clean checkout at
   the integration revision or state the sha256 of the executing counter bytes (A4's own
   pattern: "count-c1.py blob a5db2cc"). This is the single largest revision-precision gap in
   the round's machinery.
2. C2's drift check covers only `carrier_paths(pins)` — today `{SCORECARD.md}`. Sound for the
   frozen population (all three bindings carry SCORECARD.md), and it exits 2 (never a pass).
3. C3's live reading is time-varying: the no-harm battery at daa77bd5 measured
   `live_tokens=64 live_agree=64` (controls-verify-r84.txt §2) while the r83 closure cites
   63/63 at c4845c83. Any record citing a live number must carry its as-of stamp.
4. The r83 C2 counter derives `--fleet-root` from the repo path (`parent dir if repo endswith
   "-shokunin"`); correct on this host, environment-coupled elsewhere (the Mo83R01C1 §7.1 class
   persists). Not a defect here; a named limit for receipts taken on other hosts.

---

## 4. Record obligations (what this round must update, and what the contract omits)

**Named by the contract:** `.ufo/waves/round-84/evidence/after-r84.txt` with the three commands
at the integration revision; SCORECARD/LOG citing that revision; honest-stop rule.

**Omitted by the contract — the lane's standing record still must carry them:**

| # | File | Exact claim it must carry | State at my run |
|---|---|---|---|
| R1 | `.ufo/waves/round-84/evidence/after-r84.txt` | the three frozen commands + rc at the integration revision, plus the executing counters' selftest tallies and the **r83 counters' selftest tallies at the final bytes** (D83-1 fix direction: "commit the run tallies for the final bytes beside the after receipt") — expected: r83 c1 `pass=8 fail=0` (6+2 arms), r83 c2 `pass=16 fail=0` (12+4), tool `pass=44 fail=0` | not yet written |
| R2 | `SCORECARD.md` `## Round 84` verdict section | the three claims with entering → integration strings at named revisions; retire `## Planned (round 84)` (replace with round 85) | Planned section still present |
| R3 | `SCORECARD.md` `### Capabilities (round 84)` + r83-row updates | new: the r84 C1 four-mutant gate (M24a–M24d, killed=2 equivalent=2), the record sweep `ALL_ANCHOR_ROWS` row (arms 40 → 44), the `LIVE_DELTA` classifier capability; **stale r83 rows**: count-c1 "6 detector arms" → 8, count-c2 "12 selftest arms" and its `C2=met … live_agree=%d` expected string (the tail gains `delta=classified classified= union= absent_live= added_live= class_changed= deltas=`), record sweep "40 selftest arms" → 44 | untouched |
| R4 | `LOG.md` `## Round 84` entry | the round-80..83 format: three claims, entering/integration revisions, the no-harm battery line, and **dispositions of routed defects D83-1 (final-tally receipts), D83-2 ("7 arms" vs executed-count precision — state the arm delta exactly), D83-3 (count precision)** | no round-84 entry exists |
| R5 | `corpus/lessons/round-84.md` `## Gate` | the three claims, keeper commands, frozen targets, measured revisions; an **A2 disposition line connecting the lesson's "Measured conflict" paragraph** (written pre-A2 against the pre-A2 counter) to amendment A2 that resolved it | scribe draft exists (in flight); its conflict paragraph is pre-A2 text |
| R6 | `corpus/QUALITY.md` | criteria 170 (all-anchor-rows), 171 (LIVE_DELTA), 172 (counter-must-probe-itself) | drafted in worktree (uncommitted, S02) |
| R7 | `SKILL.md` gate registry | **row 18 for `tools/mori-record-sweep.py` ALL_ANCHOR_ROWS** (PROVINCE already names it) and **row 17 refresh**: its C2 verdict string (`C2=met snapshot=bound asof=1 tokens=64 agreed=64 residual=0 live=derived`) goes stale the moment the C3 tail change lands | **SKILL.md untouched — this is the most at-risk obligation** |
| R8 | `PROVINCE.md` | round-84 appended scope notes (record sweep rule change; LIVE_DELTA evidence-not-instrument) | drafted in worktree (uncommitted); must not commit before R7 (it names "registry row 18") |
| R9 | freeze-commit population-control receipt | measurement protocol step 1 says **both** receipts are committed under `evidence/`; committed at HEAD: only `controls-r84.txt`. The population control receipt exists only as the **untracked** `evidence/controls-verify-r84.txt` (E04) | gap — commit it (or an L1-equivalent) |
| R10 | `corpus/README.md` + `corpus/SOURCES.md` + `corpus/knowledge/equivalent-mutant-adjudication-r84.md` + `corpus/evidence/sources-r84/` | S599 frontier row (equivalent-mutant cost/bias ground for the A1-style adjudication) + knowledge entry + README index row | drafted in worktree (uncommitted) |
| R11 | `SHONEN.md` | none — the contract claims no box move; do not touch | unchanged |

**Flagged omission:** the contract never mentions D83-1/D83-2/D83-3; the L1's integration
record must discharge them explicitly or they roll forward a third round.

---

## 5. Numbers discipline (every cited number → its re-derivation command)

| Number | Re-derivation |
|---|---|
| C1 `mutants=4 total=4` | `python3 -c "import importlib.util;…"` over the MUTANTS tuple at R, or count rows of the A2 table (contract lines 188-191); graded receipt re-prints them |
| C1 `killed=2 equivalent=2 survivors=0` | only from `python3 -I .ufo/waves/round-84/count-c1.py R` — no independent static source; the record must cite the receipt line, not rc alone (F3) |
| C1 pristine/detector green | same receipt; detector tally also re-runnable: `python3 -I .ufo/waves/round-84/count-c1.py --selftest` → `C1_COUNTER_SELFTEST pass=11 fail=0` (verified, mine) |
| C1 equivalence coupling (3 markers, each 1×) | `git show R:.ufo/waves/round-83/count-c2.py | grep -F -c 'agreed == len(snapshot_tokens)'` etc. — verified 1/1/1 at `5adf4337`/`daa77bd5` |
| C1 anchor counts (A2 set) | `grep -F -c` of each of the four A2 anchors at R — verified 1/1/1/1 at `daa77bd5` |
| C1 r83-counter arm delta | `python3 -I .ufo/waves/round-83/count-c1.py --selftest` at the final bytes — 6 now (verified), 8 expected after E01 (state the delta exactly, D83-2 class) |
| C2 `arms=44` | `python3 -I tools/mori-record-sweep.py --selftest` at R → `RECORD_SWEEP_SELFTEST pass=44 fail=0`; entering baseline 40 verified by me from a scratch export of `5adf4337:tools/mori-record-sweep.py` |
| C2 `defeated=2 fixtures=3/3` | only from the C2 receipt; per-fixture kind (`row-value` vs `rev-bytes`, row 2) is **not** code-enforced (F5) — if the record cites the kinds, it must paste the tool's own MISMATCH lines from the receipt |
| C2 `bindings=3` | `python3 -c "import json;print(len(json.load(open('.ufo/waves/round-82/record-pins.json'))['revisions']))"` → 3; population equality enforced by `population_ok` against the FROZEN tuple |
| C2 `revisions=0` | the real-run line inside the C2 receipt |
| C2 carrier-row multiplicities | `grep -c "row_tally=19" SCORECARD.md` → 1; `grep -c "survivors=0" SCORECARD.md` → 5; `grep -c "wrong=0 fixtures=7" SCORECARD.md` → 1 (verified: worktree and `5adf4337` agree) |
| C3 `tokens=64` | snapshot census: `sed -n '10p' .ufo/waves/round-82/evidence/drift-r82-live.txt | sed 's/^MORI_DRIFT://' | tr -s ' ' '\n' | grep -v '^$' | grep -v '^none$' | sort -u | wc -l` → 64 (verified); the counter re-derives it as `tokens == 64` from the subject's own tail (A3's point: it is the snapshot count, not a live count) |
| C3 `classified=/union=/absent_live=/added_live=/class_changed=/deltas=` | only from the C3 receipt (the live side is mutable; cite with the run's as-of stamp) |
| C3 arm delta 12 → 16 | `python3 -I .ufo/waves/round-83/count-c2.py --selftest` at the final bytes; the four delta arms must each print PASS (counter-enforced by name) |
| Scores 7 / 5 / 5 | unchanged; no closure states a new number this round |

---

## 6. Verified / not verified

**Verified (my own runs, outputs quoted above):** all three entering controls byte-identical to
`controls-r84.txt`; the C1 population control at `daa77bd5` (worktree counter) exactly as
frozen; the pre-A2 counter's different (`mutants=1`, unanchored ×3) reading at `daa77bd5`;
all three counter selftests green (11/9/9 arms); A2 anchor uniqueness at the freeze revision;
the three frozen pins' carrier-row multiplicities at worktree and entering revision; snapshot
token census 64/64 unique; entering tool selftest `pass=40`; the C2 fixture-construction code
against the frozen fixture table; the C3 receipt-format code against the in-flight subject
diff (notes channel carries `LIVE_DELTA` lines one per line; met/tail fields all parse under
the counter's FIELD regex); cross-claim coupling preservation in the in-flight E03 diff.

**Not verified:** any after-value (no seat work had landed committed at my run — E01's arms,
the C2 tool bytes, and E03's selftest arms were all still in flight); the C2 drift check under
real drift (no code path exercised — read-verified only); behavior of the counters on any host
but this one (fleet-root derivation); the C2/C3 stub-forgibility residuals (theoretical, named
only).

**Defects found in other seats' bytes:** none committed. Observations on in-flight worktree
bytes: (a) `corpus/lessons/round-84.md`'s "Measured conflict" paragraph is pre-A2 and now
superseded — it needs an A2 disposition line at integration (R5); (b) the PROVINCE draft names
"registry row 18 in SKILL.md" before that row exists — commit ordering constraint (R7 before
R8); (c) `evidence/controls-verify-r84.txt` (E04) satisfies the population-control receipt but
is untracked — R9. All three are integration-ordering notes, not byte defects.

**Tooling:** no installs, no upgrades; python3 (system) + git only. No pacman transaction.
Scratch `/fast/scratch/hyaku/mori-r84/Mo84R03Record/` deleted on exit.
