# ScrScorecardRow — round 40 wave 1 (L1 mori-r40 attempt 1), scorecard draft

- Seat: scribe (`ScrScorecardRow`)
- Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`
- Scored tip T1: `265a955cc67be4eae97d2dc5a9338a25f31eb29b`
- Entering tip: `bb1f2457bb8d3e8d5dfe98488b91e8c02e378ca3`
- Round tip read time (HEAD, T2): `ede486b7a09afbacfb380d5871c46a8051a6dc2e`
- Report path: `.ufo/waves/round-40/w1/ScrScorecardRow.md`
- Deliverable: corrected round-40 SCORECARD declaration + C1/C2 results rows (draft in §5).
- Product files edited: **none**. `SCORECARD.md` already carries a round-40 section
  (committed at `8d3badd`); it is outside this seat's write scope and was not modified.

## 1. Behavior

Read the frozen contract, the landed receipts, the existing SCORECARD round-40
section (`SCORECARD.md:2216-2260`, committed `8d3badd`), lesson M24
(`corpus/lessons/round-40.md:24`) and the round-40 LOG bullet; re-derived the C2
lane line from committed gate bytes at T1 and T2; counted every receipt's id
list; cross-checked the same-wave seat reports (`CritLaneLine`, `ExeGateLane`,
`MutGateEligible`, `CritPredParenthetical`, `MutGateReadd`, `MutGateFirstParent`,
`CritNewSurvivor`, `MutConformArms`, `ExeSurvivorSweep`); drafted the declaration
+ rows. No product, judge, corpus or fleet edits.

## 2. Commands run and observed outputs

All commands run from `/home/vgpnk/Projects/shokunin/mori-shokunin`.

1. `python3 tools/mori-sources-appendonly.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --repo .`
   → `EXIT=1`; summary `appendonly_violations=18 ids=[S041,…,S193] deleted=[] superseded=[35 ids] round_changed=[]`;
   last line (see §3) lists **35** `superseded_as_of` ids, `stale_supersede=[]`.
2. `git show 265a955cc:tools/mori-sources-appendonly.py | sha256sum`
   → `bde5a9a34c7eb3bcbee39d669b8d187caeb51807ad1bdcd85a05c1bcd06777ec` — equal to
   `sha256sum tools/mori-sources-appendonly.py` and to the `freeze-r40.txt` pin.
3. `git show 265a955cc:tools/mori-sources-appendonly.py > /tmp/gate-at-t1.py && python3 /tmp/gate-at-t1.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --repo .`
   → `EXIT=1`; same 35-id `supersede_timing` line, `stale_supersede=[]`.
4. Programmatic diff of the last `supersede_timing` and `appendonly_violations`
   lines from (1) against `evidence/c11-after-lane.txt` → `timing identical: True`,
   `violations identical: True`.
5. Count script over the receipts:
   `c11-before-lane.txt` → 18 as-of ids, `stale=[]`, S226 absent;
   `c11-after-lane.txt` → 35 as-of ids, `stale=[]`, S226 present;
   extension = 17 ids `S067,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S226`
   (16 earlier + S226);
   `c11-after-e37dcc6.txt` → 33 as-of + `stale_supersede=[S069]` = 34 eligible, S226 absent.
6. `git show 265a955cc:corpus/SOURCES.md` + regex check → each of the 17 extension
   ids is the target of a `teaches: supersedes <id>` row present at T1; S226's own
   row teaches `supersedes S069`.
7. `python3 tools/mori-sources-appendonly.py --selftest`
   → `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0`, `EXIT=0`.
8. `python3 tools/mori-sources-appendonly.py e37dcc6 --repo .`
   → `supersede_timing superseded_as_of=[33 ids] stale_supersede=[S069]`, `EXIT=1`.
9. `python3 tools/mori-sources-appendonly.py ede486b7 --repo .`
   → the same 35-id as-of line, `stale_supersede=[]` (T2 equals T1 for this field).
10. `python3 .ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b`
    → `check selftest_conjunct PASS (count-c8.py: honest_comm=[] strips=6 detected=6 anchor=True entry_live=True)`,
    `CONFORM=met`, `EXIT=0`. A full-output rerun at T2 prints
    `check head_pin PASS (pin=ede486b7a09afbacfb380d5871c46a8051a6dc2e tip=ede486b7a09afbacfb380d5871c46a8051a6dc2e)`,
    `CONFORM=met` — the pin is the live lane HEAD, not the `rev` argument
    (see F7).
11. `python3 .ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --selftest`
    → `CONFORM_SELFTEST pass=11 fail=0`, `EXIT=0`, wall time 61.49 s.
12. `python3 .ufo/waves/round-40/fixtures/run-c11-dags.py tools/mori-sources-appendonly.py /home/vgpnk/Projects/shokunin/mori-shokunin .ufo/waves/round-40/scratch/scr-dag-{n,p,r}.txt dag-{n,p,r}`
    → dag-n `as_of=[S001] stale=[]` `EXIT=0`; dag-p `changed S001 superseded_by=S002`,
    `as_of=[S001] stale=[]` `EXIT=1`; dag-r `as_of=[S008] stale=[]`, no `changed`
    line, `EXIT=1`. (Scratch receipts deleted after capture; outputs recorded here.)
13. Control re-runs:
    `python3 .ufo/waves/round-40/fixtures/extracted/conform-v2-r39.py 265a955cc… --counter .ufo/waves/round-40/fixtures/generated/survivor-decoy.py`
    → `CONFORM=met`; same script on `survivor-divzero.py` → `EXIT=2` (no CONFORM line);
    `python3 .ufo/waves/round-40/conform.py 265a955cc… --counter …/survivor-decoy.py`
    → `CONFORM=unmet`.
14. `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
    (fleet repo, read-only) → `EXIT=0`; 17 output lines; last line
    `mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`;
    byte-identical to `evidence/census-end.txt` after blank-line filtering
    (`CENSUS_BYTES_EQUAL=yes`). S229 introduces no new warning class; the 16 W04
    duplicate-URL rows are the standing fleet debt.

## 3. Measured lane line (marked)

Measured at T1 by (1) and by the committed T1 gate bytes in (3); byte-identical to
`evidence/c11-after-lane.txt`:

```
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226] stale_supersede=[]
```

**Count: 35 as-of ids** (not 34), `stale_supersede=[]`; the 17-id extension over
v2's edit-bounded 18 is S226 plus 16 earlier never-edited superseded rows
(S067,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140).

## 4. Findings — conflicts reported verbatim

**F1 (material, erratum-class).** The brief, contract and predicate carry a
parenthetical mis-prediction; the landed receipts and my re-derivation disagree
with the *propagated* figure by one:

- Contract `P-C11` (`contract.md:119`): `… S226 joins superseded_as_of (19 ids) at the landed tip, no id is stale at the tip, S069 is stale at e37dcc6 …`
  — repeated in the frozen gate predicate (`tools/mori-sources-appendonly.py:87`)
  and in `contract.md:137`: `` `supersede_timing superseded_as_of=[19 ids incl. S226] stale_supersede=[]` ``.
- Wave brief (`evidence/wave-plan.txt` context): "Lane line at the tip carries 34 as-of ids including S226, none stale; at e37dcc6 stale=[S069]."
- Lesson M24 (`corpus/lessons/round-40.md:24`): "the measured lane line at T1 lists **34** as-of ids — the eligible-set extension admits every never-edited superseded row present at R (16 rows: S226 plus 15 earlier)".
- `LOG.md:2296-2298`: "lane line at T1 lists 34 as-of ids incl. S226 … measured 34".
- Existing `SCORECARD.md:2234-2236`: "16 never-edited superseded rows (S226 plus 15 earlier) … the measured value is **34 as-of ids** at T1"; kill rule `SCORECARD.md:2241`: "prints 18 ids ≠ 34".

Measured: **35** (`c11-after-lane.txt`; re-derived identically, §2 items 1/3/4).
The extension is 17 ids, not 16: 18 + 16 earlier + S226 = 35. The 34 figure equals
the **`e37dcc6`-era total eligible** count (33 as-of + S069 stale), not the T1
as-of count `[INFERENCE]` on provenance; the arithmetic error itself is observed.
This is the same number-drift class as the 19-ids mis-prediction and needs the
same append-only erratum treatment in SCORECARD, lesson M24 and LOG. The claim's
discriminator is unaffected: S226 present, `stale=[]` at T1, `stale=[S069]` at
`e37dcc6`.

Corroborated independently in this wave: `CritLaneLine.md:5,15` ("the wave
brief's '34 as-of ids' count is wrong — the committed receipt carries 35"),
`ExeGateLane.md:7` ("The measured as-of list contains 35 IDs, not the assigned
expected count of 34"), `MutGateEligible.md:133-137` ("18 (v2, before) + 17
never-edited additions = 35"), and `CritPredParenthetical.md:5-7,43-46` (which
also names the e37dcc6 union as the plausible provenance of 34, matching the
`[INFERENCE]` above). All four re-derived the line from committed bytes.

**F2 (wording, not behavior).** Existing `SCORECARD.md:2242` kill rule: "a gate
keeping the re-add changed event prints `stale=[S008]` on dag-r". The frozen v2
red does not show that: `c11-red-readd.txt` prints `superseded_as_of=[]
stale_supersede=[]` with `round_changed=[S008]`, and the v3 after prints
`as_of=[S008] stale=[]` (`c11-after-fixture-r.txt`). The `stale=[S008]` half is a
*mutant* prediction and is corroborated by this wave's mutation probe
(`MutGateReadd.md:54,76-77`: a mutant keeping the re-add as the last edit prints
`as_of=[] stale=[S008]` on dag-r and is killed). The rule holds; the draft
attributes it to the mutant, not to `c11-red-readd.txt`.

**F3 (minor, receipt wording).** Existing `SCORECARD.md:2226` before cell says the
r39 checker prints `CONFORM=met` exit 0 "on nine survivor fixtures". The receipts
show **eight** `met` files (`shadow-none`, `shadow-neg`, `cond`, `inf`, `decoy`,
`underscore`, `second-popen`, `tuple`) and `survivor-divzero.py` at `EXIT=2` with
no FAIL line (`c10-red-divzero.txt`). The draft states the split.

**F4 (non-error, wording risk).** On dag-p the v3 receipt still prints
`changed S001 superseded_by=S002` (`c11-after-fixture-p.txt`). This is the side
branch's own first-parent edit (the gate selftest expects `ids=["S001"]` for
dag-p); the merge itself contributes nothing and the v3 verdict is `as_of=[S001]
stale=[]`. The draft does not claim the changed line disappears.

**F5 (material, C1 residual — peer falsification).** A same-wave critic reports
three one-edit counters derived from the frozen `count-c8.py` — walrus binding
(`(timeout := None)`), tuple-unpack binding (`timeout, _ = None, None`) and a
dead-loop rebind (`timeout = None` then `for _ in (): timeout = GIT_TIMEOUT_S`,
a BFS-order seam in `_function_bindings`) — that print `CONFORM=met` exit 0 while
the runtime `communicate(timeout=…)` value is `None`
(`.ufo/waves/round-40/w1/CritNewSurvivor.md`, with a runtime probe showing the
2 s unbounded wait). The nine frozen survivors and the eleven selftest arms
behave exactly as the after receipts declare, so C1's *declared* receipts stand;
the predicate's universal "every `timeout=`" sentence is not computed for those
binding forms. The draft carries this as a residual line, not as a claim
extension.

**F6 (material, C1 selftest coverage).** The wave's conform-arms mutation probe
neuters the conditional-rebind rule; the mutant survives `--selftest`
(`pass=11 fail=0`, byte-identical arms) and is killed only by the cond survivor
after-receipt (`CONFORM=met` flip) (`.ufo/waves/round-40/w1/MutConformArms.md`).
The frozen `pass=11 fail=0` receipt is exact; the eleven arms do not cover that
semantics. The draft keeps the receipt and adds the residual.

**F7 (reproducibility nuance).** `head_pin` reads the lane's live HEAD, not the
`rev` argument: at T2 a live run prints `pin=ede486b7… tip=ede486b7…` and still
`CONFORM=met` (my run, §2 item 10; same observation in `ExeSurvivorSweep.md:39`),
while `c10-after.txt` at T1 prints `pin=265a955cc… tip=265a955cc…`. The `rev`
argument feeds `timeout_state`. The receipt is not weakened, but replaying it at
T2 cannot reproduce the T1 pin without the T1 checkout.

## 5. Draft — SCORECARD.md round-40 declaration + C1/C2 results rows

Paste-ready fragment; it is the landed section with F1–F3 folded in and the
F5/F6 residual appended. Scores are stated as axes with the round's "held"
reading per the assignment.

---

## Round 40 declaration (attempt 1 resumed, L1 mori-r40) — conformance v3 scope-aware timeouts + per-Popen drains (C1, operability), gate v3 P-C11 eligible set + first-parent reference (C2, depth)

Entering tip `bb1f2457bb8d3e8d5dfe98488b91e8c02e378ca3` (round 39 admitted; closure
`corpus/lessons/round-39-verifier-spotcheck.md`). Instruments landed at
`265a955cc67be4eae97d2dc5a9338a25f31eb29b` (T1); evidence + corpus records at the
round tip. Contract `.ufo/waves/round-40/contract.md`; pins `evidence/freeze-r40.txt`
(gate sha256 `bde5a9a3…`, conform `5025b966…`). Lowest non-retired axes calibration 5
and depth 5 (tied) — C2 works depth; C1 works operability (routed defects 1–2 class).

| Claim | Axis / score | Before (one command over committed bytes) | After (measured at T1) |
|---|---|---|---|
| C1 conformance v3: `timeout_scope` resolves every `timeout=` at its read site (function-local shadow, `global`, conditional rebind fail closed; finite-positive fold), `drain_bind` requires a consumed `communicate(timeout=…)` bound to the same name as each `Popen(`, and `selftest_conjunct` reads the checker's own mutation table with per-counter comm_violations (r39 w1 findings 4/8/12; routed defects 1–2) | operability 7 (held) | the r39 checker bytes (`fixtures/extracted/conform-v2-r39.py`, sha256 `fe0be179…`) print `CONFORM=met` exit 0 on eight of the nine survivor fixtures; the ninth, `survivor-divzero.py`, exits 2 with no FAIL line (`evidence/c10-red-shadow-none.txt`, `-shadow-neg`, `-cond`, `-inf`, `-decoy`, `-underscore`, `-second-popen`, `-tuple`, `-divzero`); the two-counter audit prints `CONFORM=met` (`c10-red-multicounter.txt`); the conjunct-gutted r39 copy prints `CONFORM_SELFTEST pass=8 fail=0` (`c10-red-conjunct.txt`) | `python3 .ufo/waves/round-40/conform.py 265a955cc…` → `CONFORM=met` exit 0 (`evidence/c10-after.txt`); `--selftest` → `CONFORM_SELFTEST pass=11 fail=0` (`c10-after-selftest.txt`); each of the nine survivors → `CONFORM=unmet` exit 1 with the named check FAIL — `timeout_scope` on shadow-none/shadow-neg/cond/inf/divzero (fold error: division by zero), `drain_bind` on decoy/underscore/second-popen/tuple (`c10-after-<fixture>.txt`); the two-counter audit → `CONFORM=unmet` exit 1 with per-counter `drain_bind` and `selftest_conjunct` FAIL (`c10-after-multicounter.txt`); the conjunct-gutted v3 copy → `CONFORM_SELFTEST pass=0 fail=10` with `selftest_conjunct` in every failing list (`c10-after-conjunct.txt`) |
| C2 gate v3 (P-C11): the `supersede_timing` eligible set is every superseded id present at R (a never-edited id's last immutable-cell edit is its first-sighting commit); an edit at a commit is a change against the first parent's state only — a first-parent-lacks-path merge contributes no edits, and a linear delete-then-re-add contributes no changed event (r39 w1 findings 2/5; routed defects 3–4) | depth 5 (held) | the v2 gate bytes (`fixtures/extracted/gate-v2-bb1f2457.py`, sha256 `62cd4132…`) print the lane line with 18 as-of ids and S226 absent (`evidence/c11-before-lane.txt`); on dag-n `superseded=[]` / `superseded_as_of=[]` (`c11-red-neveredited.txt`); on dag-p `stale_supersede=[S001]` (`c11-red-firstparent.txt`); on dag-r `superseded_as_of=[]` with `round_changed=[S008]` and no `changed` line (`c11-red-readd.txt`) | `python3 tools/mori-sources-appendonly.py --selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` (`c11-after-selftest.txt`); at T1 the lane line lists **35** as-of ids including S226, `stale_supersede=[]` (`c11-after-lane.txt`, marked below); at `e37dcc6` → 33 as-of + `stale_supersede=[S069]` (34 eligible) (`c11-after-e37dcc6.txt`); dag-n `as_of=[S001]`, dag-p `as_of=[S001] stale=[]` (its `changed S001` line is the side branch's own first-parent edit; the merge contributes none), dag-r `as_of=[S008] stale=[]` with no `changed` line (`c11-after-fixture-{n,p,r}.txt`) |

Measured lane line at T1 (`evidence/c11-after-lane.txt`; re-derived byte-identically
by `python3 tools/mori-sources-appendonly.py 265a955cc… --repo .`):

```
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226] stale_supersede=[]
```

**Correction folded same-round (erratum-class, number-drift; append-only note):**
the contract's P-C11 parenthetical "(19 ids)" (`contract.md:119`, repeated in the
frozen gate predicate `tools/mori-sources-appendonly.py:87` and the contract's
after-cell `contract.md:137`) mis-predicted the eligible-set extension; the first
correction of this section, lesson M24 and `LOG.md`'s round-40 C2 bullet then
recorded **34**. The measured value at T1 is **35 as-of ids**: v2's edit-bounded
set prints 18, and v3 adds **17** never-edited superseded rows — S226 plus 16
earlier ids (S067,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140),
each a supersede target present at R (`git show 265a955cc:corpus/SOURCES.md`).
34 is the `e37dcc6`-era eligible total (33 as-of + S069 stale), not the T1 as-of
count; M24's "16 rows: S226 plus 15 earlier" is one low on the earlier block. The
predicate's semantic sentence is the claim; the arithmetic is corrected here, in
lesson M24, and in LOG. The discriminator is unchanged: S226 present, `stale=[]`
at T1, `stale=[S069]` at `e37dcc6`; v2's edit-bounded set omits all 17 extension
ids.

Kill rules as frozen: a do-nothing control cannot print `CONFORM=met` (the r39
checker on the survivors is the committed control: it prints `met` on eight and
exits 2 on `survivor-divzero.py`); a checker that only adds function-local
shadowing still accepts the decoy drain; a v3 whose own mutation table lacks the
`selftest_conjunct` entry fails that arm (`c10-after-conjunct.txt`); a gate keeping
the edit-bounded eligible set prints 18 ids ≠ 35 with S226 absent
(`c11-before-lane.txt`); a gate with the second-parent fall-through fabricates the
dag-p stale verdict (`c11-red-firstparent.txt`); a gate keeping the re-add as the
last edit fails fixture R (v2's frozen dag-r red prints `superseded_as_of=[]`; the
gate selftest's hand-written dag-r expectation pins `as_of=[S008]`, and the
mutation probe prints `stale=[S008]` for that mutant, `MutGateReadd.md`).

Residual found in-wave (not part of the frozen claim): three one-edit
binding-form counters (walrus, tuple unpacking, dead-loop rebind of a
function-local `timeout`) print `CONFORM=met` while the runtime
`communicate(timeout=…)` value is `None`
(`.ufo/waves/round-40/w1/CritNewSurvivor.md`), and a mutant that neuters the
conditional-rebind rule survives `--selftest` (`MutConformArms.md`). The nine
frozen survivors, the two-counter audit and the eleven selftest arms behave
exactly as the receipts above declare; `timeout_scope`'s universal "every
`timeout=`" sentence is not computed for those binding forms. C1's declared
receipts stand and the score is held as stated; the residual is routed to the
closure for grading.

Capability rows (demonstrated running this round; closure admits them):

| key | name | what it can now do | evidence | first working |
|---|---|---|---|---|
| round-40 C1 | counter conformance v3 | Audits every counter's `timeout=` keywords at their read sites (function-local shadow, `global`, conditional rebind, finite-positive fold), binds every `Popen(` drain to a consumed same-name `communicate(timeout=…)`, and reads its own mutation table for the communicate-timeout conjunct with per-counter comm_violations; eleven-mutation selftest | `.ufo/waves/round-40/conform.py`; `evidence/c10-after.txt`; `c10-after-selftest.txt` | 40 |
| round-40 C2 | ancestry supersede reading v3 | Separates as-of from stale over every superseded id present at R (never-edited ids test against their first-sighting commit), with edits measured against the first parent's own state only — no second-parent fall-through, no re-add changed event | `tools/mori-sources-appendonly.py` (P-C11); `evidence/c11-after-lane.txt`; `c11-after-fixture-n.txt` | 40 |

Held: coverage 6, operability 7 (C1 moves the surface; score held on the round's
honest read — closure rules), depth 5 (C2 moves the surface; score held, same
read), calibration 5, freshness 5, adjacency 6 — no scalar score moves this round;
both claims are checker-semantics moves whose receipts are the improvement.
Sourced claim: C1 rests on S229 (opened this round;
`corpus/knowledge/conform-scope-r40.md`). No retirement, waiver, exploratory claim
or promotion. Frontier: S229 row; census 228 → 229 (exit 0 both ends,
`evidence/census-start.txt`, `census-end.txt`).
Round shape: ONE v2 wave, 66 seats, validated under policy v2
(`evidence/wave-plan.txt`, `w1-spec.json`); policy band 64–128.

---

## 6. Gates

- C2 lane line re-derived from **committed** T1 gate bytes (sha256 `bde5a9a3…`,
  equal to the freeze pin) and byte-diffed against `c11-after-lane.txt`: identical.
- T2 (`ede486b7`) prints the same 35-id as-of line, so the finding is not a
  stale-receipt artifact.
- C1 primary receipt re-derived: `CONFORM=met`; `--selftest pass=11 fail=0`.
- C2 selftest re-derived: `pass=15 fail=0`; e37dcc6 verdict reproduced.
- Three DAG fixtures re-derived; verdicts match the landed after receipts.
- Before-control spot-checks re-derived: r39 bytes accept the decoy survivor and
  crash (exit 2) on the divzero survivor; v3 rejects the decoy.
- Census re-run read-only: exit 0, bytes equal to `census-end.txt`.
- No build, lint, formatter, commit, push or judge run by this seat.

## 7. Touched surfaces / artifacts

- Written: this report; temporary `scr-dag-{n,p,r}.txt` under
  `.ufo/waves/round-40/scratch/` (deleted after capture; outputs recorded in §2);
  the DAG runner's own temp dirs under `.scratch/` (runner removes them).
- Read: contract, all `c10-*`/`c11-*` receipts, SCORECARD, LOG, lesson M24, gate
  v3, conform v3, registry at T1.
- Not touched: `SCORECARD.md`, contract, instruments, `evidence/`, `corpus/`,
  fleet repo, sibling lanes, lane jj state, lane Git index, `.ufo/state/`,
  `.ufo/watchdog.log`. No tool installs.

## 8. Out of scope / known limits

- The assignment asked to "mark the measured 34-id lane line"; **34 is not
  reproducible**. The receipt and two independent re-derivations give 35. This
  report marks the measured 35 and reports the 34 as F1 for canonical
  adjudication rather than writing an unobserved number.
- `SCORECARD.md`, `LOG.md` and lesson M24 carry the 34 figure today; correcting
  them is the L1/integrator's append-only action (product docs outside this
  seat's write scope). The draft in §5 is the paste-ready corrected text.
- The nine survivor receipts were not all re-run individually; they are landed
  ground truth, and the before/after control was independently spot-checked
  (decoy, divzero). Unrun checks are not claimed as run.
- C1 residual (F5/F6): the frozen nine-fixture claim and the `pass=11` selftest
  receipt are met, but same-wave peer probes show binding-form survivors and a
  conditional-rebind mutant that the selftest does not catch. The scorecard draft
  states this as a residual; the canonical judge/closure owns its grading.
- Replay nuance (F7): `head_pin` pins the live HEAD, so a T2 replay of the
  conform receipt passes on `ede486b7` and cannot reproduce the T1 pin without
  the T1 checkout; the C2 gate line is revision-addressed and was re-derived
  byte-identically at both T1 and T2.
