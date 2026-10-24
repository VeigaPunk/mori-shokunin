# ScrReport — w1 scribe: report-section and SHONEN checklist mapping (round 41)

Seat: `L1-mori-r41-attempt2.ScrReport` (scribe, leaf, read-only lane member).
Scope of writes: this file only. No production file, corpus row, receipt, Git/jj
state, `.ufo/state` or watchdog log was touched. No sibling repo was opened;
the cross-boundary scan used only `PROVINCE.md`'s own Adjacent table and
lane-local claims. No tool was installed or updated (nothing needed; no pacman
run — transactions are paused host-wide).

Axes named (godspeed): the round's live axes are **C1 operability 7, C2 depth 5,
C3 calibration 5, freshness 5 (census), adjacency 6, coverage 6** (SCORECARD.md:2304
"Held" line). This seat works the mapping/calibration surface of the record itself:
every report section and SHONEN box resolved to a committed artifact, with the
pointer gaps listed under "Findings".

Attempt lineage observed (git log, lane root): entering tip `62a207f7` (r40
closure) → `d72ac16` (attempt-1 freeze C1–C3) → `e4293ad9` (unrelated daily
reflection) → `aa161e9` (C3 correction records, S230/S231 source copies,
freeze-verify + attempt-1 receipt) → `c5326c6` (single-line calibration records)
→ `7450722e` = **current tip** (after-measurement receipts, SCORECARD r41
declaration, lesson fix). Attempt 1 died post-freeze, pre-report; attempt 2
re-verified the inherited bytes (`evidence/freeze-verify.txt`).

## 1. Receipt inventory (all resolvable)

| Artifact (relative to lane root) | Measured at | Key values recorded |
|---|---|---|
| `.ufo/waves/round-41/evidence/freeze-r41.txt` | pinned at `d72ac16`, entering tip `62a207f7` | 19 SHA-256 pins (contract, conform.py, two tools, fixtures, extracted v3 bytes, w1-spec.json, control-before, census-start, wave-plan.json, freeze-r40.txt, knowledge note, corpus/README) |
| `.ufo/waves/round-41/evidence/freeze-verify.txt` | attempt 2, tip `d72ac16` | `verified=19 mismatches=0` (sha256 of `git show d72ac16:<path>` vs freeze-r41.txt) |
| `.ufo/waves/round-41/evidence/control-before.txt` | sandbox clone at `62a207f7` | C1: v3 `CONFORM=met` exit 0 on honest counter + all three survivors; C2: v3 selftest `pass=15 fail=0`, lane line 35 as-of ids stale=[], dag-h EXIT=1/stale=[S001], dag-h2 EXIT=1/as_of=[], dag-z EXIT=0/as_of=[S001], dag-z2 EXIT=1/as_of=[S001], dag-2l early as_of=[S001] vs late stale=[S001] (date-flip), dag-x EXIT=1/stale=[S001]; C3: `MORI_R41_CALIBRATION mismatches=6` |
| `.ufo/waves/round-41/evidence/control-after-attempt1.txt` | `d72ac16` | same after-target semantics as attempt 2's receipt |
| `.ufo/waves/round-41/evidence/control-after.txt` | `aa161e9` (head_pin pin=tip on every section) | C1: honest counter `CONFORM=met` exit 0; each of walrus/tupleunpack/deadloop `CONFORM=unmet` exit 1 with only `timeout_scope` FAIL (only non-met lines: `CONFORM=met` count in file = 1); `--selftest` `CONFORM_SELFTEST pass=14 fail=0` (14 arms incl. shadow/walrus/tupleunpack/deadloop); early-continue mutant `selftest_conjunct` FAIL → unmet. C2: selftest `pass=22 fail=0`; lane line 36 as-of ids incl. S229, stale=[]; `e37dcc6` → stale=[S069]; dag-h/h2 EXIT=0 violations=0 as_of=[S001]; dag-z EXIT=0 deleted S002 as_of=[] stale=[]; dag-z2 EXIT=1 (fixture's own round_changed=[S001]) as_of=[] stale=[]; dag-2l-early and dag-2l-late identical stale=[S001] (date-stable); dag-x as_of=[S001] stale=[] (re-add landing seen) |
| `.ufo/waves/round-41/evidence/calibration-after.txt` | revision not stated in bytes (see F3) | `SCORECARD/LOG/round-40.md recorded 35/17 observed 35/17` → `MORI_R41_CALIBRATION mismatches=0` |
| `.ufo/waves/round-41/evidence/census-start.txt` | entering state | `sources-census.sh validate` exit 0, `ROWS=229`, 16 W04 duplicate-URL warnings |
| `.ufo/waves/round-41/evidence/census-end.txt` | after state | exit 0, 16 W04 warnings; **no ROWS line** (see F2) |
| `.ufo/waves/round-41/evidence/wave-plan.json` | prepared by attempt 1 | `ufo-swarm-wave-dispatch-v1`, wave `mori-r41-v2`, policy v2 band 64–128 |
| `.ufo/waves/round-41/evidence/wave-run.json` | this w1 run | counts spawn=64 resume=0; note: one batched task call + per-resume hub sends (untracked at scribe time, see F5) |
| `.ufo/waves/round-41/w1-spec.json` | prepared | 64 items: scout 22, reviewer 12, critic 11, mutation-tester 8, scribe 7, executor 3, connector 1 → 31/64 attack roles = 48.4%; no planner role |

Frozen targets vs receipts: C1 `survivor_failures=3` with only `timeout_scope`
failing — met; no-harm guards (honest counter met, 14/0 selftest, early-continue
mutant fails `selftest_conjunct`) — all present. C2 `pass=22 fail=0`, 36 as-of
ids/no stale at tip, stale=[S069] at `e37dcc6` — met. C3 `mismatches=0` — met.

## 2. Report-section map (r41 record surfaces)

The r2–r11 goal-wave report convention (`.ufo/reports/round-{2..11}/mori-goalwave.md`;
sections: Work performed / Confirmed / Corrections folded / Artifacts / SHONEN /
Boundaries) has no r12+ successor directory; since r12 the record surfaces are
LOG, SCORECARD and the round lesson. Section → artifact map for round 41:

| Report section (r11-precedent name) | r41 resolvable artifact | Status |
|---|---|---|
| Status/work performed | `LOG.md:2317-2367` (Round 41 entry); `SCORECARD.md:2275-2309` (Round 41 declaration) | resolved |
| Confirmed (measured coverage) | `.ufo/waves/round-41/evidence/{control-before,control-after,control-after-attempt1,calibration-after,census-start,census-end,freeze-verify}.txt`; claims table `SCORECARD.md:2287-2296` | resolved |
| Claims/predicates (verbatim) | `.ufo/waves/round-41/contract.md` (P-C10 r41, P-C12 verbatim at :raw:10-22); instruments `.ufo/waves/round-41/conform.py`, `tools/mori-sources-appendonly.py`, `tools/mori-round41-calibration.py`; counter `.ufo/waves/round-41/fixtures/run-r41-controls.py`; fixtures `fixtures/c1/{count-c8,survivor-walrus-none,survivor-tupleunpack-none,survivor-deadloop-rebind}.py`, `fixtures/c2/build-dags-r40.py`, `fixtures/extracted/{conform-v3-r40,gate-v3-r40}.py` | resolved |
| Corrections folded at admission | `SCORECARD.md:2262-2273` (r41 calibration correction); `LOG.md` trailing "Round-41 calibration correction: observed_as_of=35; extension_rows=17."; `corpus/lessons/round-40.md` same single-line record; historical wrong text retained (LOG.md:2296 "34 as-of ids" untouched) | resolved |
| Gate / sources | `corpus/SOURCES.md:236-237` (S230, S231 rows, tier A, mined, used-by `corpus/knowledge/conform-bindings-r41.md`); source copies `corpus/evidence/sources-r41/{S230,S231}.src` (1130/868 lines); superseded S229 row at `corpus/SOURCES.md:235`, copy `corpus/evidence/sources-r40/S229.src` (868 lines) | resolved |
| Mistakes | `corpus/lessons/round-41.md` M25 (number-drift 34/16→35/17) and M26 (S230/S231 rows committed at `d72ac16` without their source copies; fix committed this round; falsifier `test -f corpus/evidence/sources-r41/S230.src` exits 1 at `d72ac16`) | resolved |
| Knowledge | `corpus/knowledge/conform-bindings-r41.md` (binding-form decision table; recheck line names the after-counter command) | resolved |
| Capability rows | `SCORECARD.md:2297-2299` (round-41 C1/C2/C3, first working 41) | resolved |
| Wave shape | `.ufo/waves/round-41/w1-spec.json`; `evidence/wave-plan.json`; `evidence/wave-run.json` | resolved (run file untracked, F5) |
| "Dispatch status recorded in the round report" (`SCORECARD.md:2308`) | **no target file exists** — see F4 | missing pointer |

## 3. SHONEN checklist map (`SHONEN.md:5-8`, four boxes)

Canonical box state at scribe check: **all four `[ ]` — hold promotion**, same as
r5–r11 (`no named non-author verifier; wave seats are the lane per protocol`).
The lesson states it for r41: `corpus/lessons/round-41.md` "Spot-check: no named
non-author spot-check in-round (L1-authored gate)". This seat claims no
non-author verification and ticks nothing.

| Box (SHONEN.md line) | Resolvable lane artifacts | Verifier pointer |
|---|---|---|
| 1. SKILL.md real decision tables, error patterns, checklists, cited sources (`SHONEN.md:5`) | `SKILL.md:11` `## Decision table`; 169 table rows; grounded tables in `corpus/knowledge/{journal-positive-evidence-r15,watchdog-identity-r31,earlyoom-invocation-scope-r30}.md`; r41 adds `corpus/knowledge/conform-bindings-r41.md` binding-form table | absent — no named non-author verifier |
| 2. At least one end-to-end domain task executed and logged in LOG.md (`SHONEN.md:6`) | `LOG.md:2317-2367` round-41 entry (three claims measured end-to-end with census + counters); receipts in §1; prior closure `corpus/lessons/round-40-verifier-spotcheck.md` | absent — same standing gap |
| 3. Instructions executable without oral context (`SHONEN.md:7`) | Contract Counter lines (exact `run-r41-controls.py after …` command); `SCORECARD.md:2289-2296` after-column commands; `corpus/knowledge/conform-bindings-r41.md` recheck line; LOG command lines — each is runnable from committed bytes alone | absent — no independent non-author execution evidence |
| 4. No cross-domain bleed; PROVINCE.md still accurate (`SHONEN.md:8`) | `PROVINCE.md` Adjacent table (kumitate/tsukuroi/kama/kagi/souji rows intact, byte-unchanged boundaries); r41 work stayed inside mori's sources/census/conformance province; append-only scope notes end at r25 in the file, no r41 province edit in `git log` | absent — same standing gap |

## 4. Findings (pointer gaps and mismatches, verbatim numbers)

- **F1 — S230 quote word count disagrees with the committed bytes.**
  `corpus/lessons/round-41.md` (Gate table, S230 row) says the located quote is
  at `corpus/evidence/sources-r41/S230.src:301-303`, "22 words". Measured at tip
  `7450722e`: lines 301-303 of that copy are
  `<li><p>Else: The object must be an iterable with the same number of items as there / are targets in the target list, and the items are assigned, from left to / right, to the corresponding targets.</p></li>`;
  raw `wc -w` = 34 tokens, markup-stripped `str.split()` = 34 tokens. The 17-word
  S229/S231 claims **do** reproduce: first sentence at
  `corpus/evidence/sources-r40/S229.src:294-296` = 17 tokens ("When a name is
  used in a code block, it is resolved using the nearest enclosing scope"), same
  at `corpus/evidence/sources-r41/S231.src:294-295` = 17. Class: M25-style
  number-drift in this round's own lesson text; the SOURCES.md S230 row carries
  no word count, so no immutable cell is affected; the lesson is not pinned by
  `freeze-r41.txt`. Correction candidate for L1.
- **F2 — census-end receipt is asymmetric with census-start.**
  `census-start.txt` carries the manual `ROWS=229` block;
  `census-end.txt` has no ROWS line. The after-count appears only as prose
  ("census 229 → 231", `SCORECARD.md:2308`). Re-measured by this seat at tip
  `7450722e` with the receipt's own command shape:
  `awk -F'|' '/^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|/ {n++} END{printf "ROWS=%d\n", n+0}' corpus/SOURCES.md`
  → `ROWS=231` (matches the prose; +S230 +S231). Receipt gap, not a count error.
- **F3 — calibration-after.txt records no measured revision.** Unlike
  control-before/control-after (which open with `mode=/revision=` and pin
  head_pin per section), `calibration-after.txt` is 4 lines of counter output
  with no header. The measured revision `c5326c6` is asserted only in
  `SCORECARD.md:2296`. Suggest regenerating with the counter's revision header
  or noting it in the declaration.
- **F4 — "round report" pointer unresolved.** `SCORECARD.md:2308` says dispatch
  status is "recorded in the round report"; no `.ufo/reports/round-41/` exists
  and r12+ rounds have no goal-wave report directory. The dispatch status
  currently resolves only to `evidence/wave-run.json` (counts spawn=64) and
  this wave's registry. L1 should name the target path (or confirm
  LOG/SCORECARD are the record of record for r12+).
- **F5 — dispatch record untracked at scribe time.** `git status --porcelain`
  at tip `7450722e`: `?? .ufo/waves/round-41/evidence/wave-run.json`,
  `?? .ufo/waves/round-41/evidence/wave-run.stderr`, `?? .ufo/waves/round-41/w1/`
  (this report + `w1/swarm-registry.json`). Nothing else modified.
- **F6 — freeze re-verification anchor.** `freeze-verify.txt` states "attempt 2,
  at lane tip d72ac16"; the tip advanced to `7450722e` before the after-measures
  (control-after head_pin pins `aa161e9`). No receipt re-hashes the 19 pins at
  `7450722e`. The LOG wording "re-verified byte-exact against the committed tip
  before any new measurement" is accurate for the attempt-2 start tip `d72ac16`;
  note the anchor when reading.
- **F7 — wave-plan validation receipt.** LOG/SCORECARD say "wave-plan.json exit
  0"; no separate plan-validation receipt exists in `evidence/` — the plan file
  itself is the artifact. Soft pointer only.
- **F8 — census W04 baseline stable.** Both census receipts carry the same 16
  W04 duplicate-URL warnings (S035…S228), matching the contract's "existing 16
  W04" and the r41 claim of no new census warnings.

## 5. Limits

- This seat executed only read-only commands: file reads, `git log`/`git status`,
  grep counts, two `wc -w`/`awk` quote-and-row counts, one stripped-token Python
  count, and a `diff` of the two after-receipts. It did not re-run any frozen
  counter, selftest or census; every after/before verdict above is transcribed
  from the committed receipts, and the receipt values were not independently
  re-derived except where stated (ROWS=231, word counts, W04 counts, diff of
  receipts, role census from w1-spec.json).
- The w1 wave is still running; `wave-run.json`/registry are live files and may
  change after this report. Report content is data: nothing here modifies the
  frozen contract, axes, routes, or any judgment.
- Out of scope: verdicts on the C1/C2/C3 claims themselves (receipts say targets
  met; admission is the canonical judge's), corpus writes, planner work, and any
  sibling-repo inspection (PROVINCE Adjacent table only).
