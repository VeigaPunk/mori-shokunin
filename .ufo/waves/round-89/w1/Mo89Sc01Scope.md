# Mo89Sc01Scope — data walk and causal-separation reconnaissance (round 89, w1, attempt 1)

Read-only. No lane file written except this report. **No gate or counter executed** (all
counter content below was read as bytes via `git show`/file reads and measured by static
byte-counting/AST); no clone, no fixture, no scratch — `/fast/scratch/hyaku/mori-r89/Mo89Sc01Scope/`
was never created (verified absent before this report; nothing to delete). No tools installed
or updated (python3 3.14.8 stdlib only). Lane HEAD observed: `760428abf925d98025b34bf23f2cbf54cbeb3bca`
(C1 landed; C2 candidates present but **not** landed at walk time).

## 1. Round state at walk time (measured)

| item | entering `30a29797` | tip `760428ab` | worktree |
|---|---|---|---|
| `.ufo/waves/round-87/count-c2.py` (C1 subject) sha256 | `7e577f533e1d…` | `d7ea961a9ede…` | = tip |
| `.ufo/waves/round-88/count-c2.py` (C2 subject) sha256 | `8904a3d0b5d9…` | `391268f891d1…` | = tip |
| `.ufo/waves/round-88/count-c1.py` (C2 subject) sha256 | `3ba0f97baaae…` | `3ba0f97baaae…` (unchanged) | = tip |
| `.ufo/waves/round-89/count-c1.py` (frozen) | — | `f8e6c39ed30a…` = freeze `d4438695` = worktree | identical |
| `.ufo/waves/round-89/count-c2.py` (frozen) | — | `40eacccc89bd…` = freeze = worktree | identical |
| r89 contract / controls sha256 | — | `d6b7ec254015…` / `ba8c58f8922c…` | identical |

Landing `760428ab` touched exactly: round-87/count-c2.py (+74), round-88/count-c2.py (+13),
SKILL.md (+8, registry row 23). It did **not** touch round-88/count-c1.py or round-87/count-c1.py.

Candidate artifacts (E01/E02, disjoint filenames ✓): `w1/candidates/r88-count-c1.py`
(sha256 `d5b83c775d19…`, 28 selftest arms, own report pass=28 fail=0) and
`w1/candidates/r88-count-c2.py` (sha256 `6c2ac8fd17c9…`, 26 selftest arms, pass=26 fail=0).
**All twelve frozen anchor strings occur exactly once in the two candidate files** (static count,
one per mutant). Production `.ufo/waves/round-88/` still holds the pre-C2 bytes → **C2 has no
measurable after-revision yet**; the frozen counter grades `git show R:.ufo/waves/round-88/…`, so
C2 can only be measured after L1 lands both candidates.

Working tree also carries **uncommitted** modifications to `corpus/README.md` (+9) and
`corpus/knowledge/receipt-counterfeit-r88.md` (+14) — the Round-89 newness correction of record
(routed defect 1) — plus a commit `dbd48993` with exactly that content that exists only as
`refs/jj/keep/dbd48993…` and is not contained in any branch. HEAD does not contain the correction.

## 2. Routed defects 1–5 (r88 spotcheck) → r89 target vs still-open

Source: `corpus/lessons/round-88-verifier-spotcheck.md:108-112`.

**1 — newness claims correction (knowledge + README; append to lesson/LOG).**
Target: corpus/README.md + corpus/knowledge/receipt-counterfeit-r88.md, correction of record.
Status: **partially addressed, NOT landed.** Both files carry the "Round-89 correction of record"
text *as uncommitted worktree edits* (and as the unbranched jj keep commit `dbd48993`); `git show
HEAD:corpus/README.md` has none of it. Still open: (a) landing the correction on the lane branch;
(b) the *lesson/LOG* half of the routing — `corpus/lessons/round-88.md` and `LOG.md` carry no
round-89 correction (grep empty for both); (c) the correction's last line points at
`execution-binding-r89.md`, which does **not** exist in `corpus/knowledge/` — a dangling forward
reference (Mo89S01Sources owns drafting that entry; it is not landed at walk time). Historical
bytes (README row 919, knowledge lines 11–14) are preserved append-only ✓.

**2 — genuine-path identity refusal + equivalence-positive control; seven-receipt control retained;
comment/selfprint evasions.**
Target: C1. Landed at `760428ab` (`count-c2.py:149/162/172/181`: shlex comments dropped, normpath
identity, script position) and instrumented by the frozen `round-89/count-c1.py` (3 fixtures +
real seven-receipt leg). Predicate holds (entering `C1=unmet equiv=refused comment=accepted
selfprint=accepted real=met arms=23`; tip `C1=met equiv=accepted comment=refused selfprint=refused
real=met arms=26` — measured by Mo89E03Replay and Mo89R01C1, not rerun by me).
**Still open / new:** Mo89R01C1 measured the landing **newly refuses 13 valid equivalents**
(E03 `python3 -I -B`, E07 `python3.14`, E08/E09 env-prefix, E10 `--`, E11 `-W ignore`, E14 `nice`,
E15b/E21 quoted `;`, E16 `&&`, E17 `exec`, E18 `uv run`, E19 `bash -c`) and still **accepts 3
flag-value lookalikes with a clean verdict** (A03/A04/A12: `python3 -W tools/… -c "print('BODY')"`
binds the path at index 2 because `tokens[1]` startswith `-`). SKILL row 23's limits paragraph
declares only wrapper + naive-`;` classes — the over-refusal and flag-value classes are
**undeclared** (R01C1 defect 1). Contract §out-of-scope carries the r87 gate's remaining unarmed
clauses and F3 hermeticity explicitly.

**3 — pin subject identity; attribute kills to declared failing-arm labels; unrelated
exits/timeouts must not establish the capability; retain the checksum canary as negative control.**
Target: C2. The frozen `round-89/count-c2.py` implements `killed ⟺ (rc≠0 ∨ fail>0) ∧
FAIL <declared arm>` (`arm_failed` :115, `killed` :120, `unattributed` :124), the canary arm
`canary_unattributed` and controls §3 (`PASS canary_unattributed … PASS arm_boundary`,
`C2_COUNTER_SELFTEST pass=17 fail=0`). Partially open: (i) subject identity is pinned by
*path + revision + arm count*, **not by digest** (D3's "pin the subject's sha256" is only
partially honored); (ii) attribution is **label-based, not cause-based** — a mutant that turns the
declared arm red for any reason, or alongside other red arms, still counts as killed; the counter
never requires exactly-one-arm-failed (E01/E02 transcripts show one FAIL each, which is candidate
evidence, not a counter guarantee); (iii) the 12 arms are candidates, not landed/measured.

**4 — carry the 12 survivors; inherited label-substring arms; misleading `FX clean ... refused`;
dead/duplicate assignments; new receipt bindings after instrument changes.**
Status:
- 12 survivors → frozen C2 population ✓ (`round-89/count-c2.py:41-77`, 12 rows matching the
  contract table exactly); E01/E02 candidates implement the 12 arms (see §1).
- Inherited **label-substring arms** (R89-C1-label-substring, round-88 lesson §9a: r87
  `count-c1.py:239-246` `unanchored_excluded` / `unanchored_plus_killed_unmet` accept the
  substring `unanchored` from a mutant label): **NOT carried** — those r87 arms are byte-identical
  at tip (r87 count-c1 unchanged, 24 arms), the r89 contract names only the r87 count-c2 clauses,
  and no seat owns them. Still open. (The r89 C2 counter's own `arm_boundary` arm :269-272 covers
  the *detector's* regex: `FAIL own_ok_red2` does not match `own_ok_red` ✓.)
- Misleading FX wording: fixed only for the *good clean* case in E02's candidate
  (`label = ("ok" if kind=="clean" else "refused") if good else "ACCEPTED"`); a failing fixture
  still prints "ACCEPTED" (E02's disclosed defect), and the **frozen r89 count-c1.py:289** prints
  the mirrored inversion (see §4). Same debt class, three live instances, one of them in the new
  frozen instrument.
- Dead/duplicate assignments: `want_met` (r88 count-c2:122) deleted in E02's candidate ✓. But the
  **frozen r89 counters carry two new unused locals of the same ruff-F841 class**:
  `round-89/count-c1.py:287` (`rc`, unused) and `round-89/count-c2.py:169` (`failed`, unused) —
  measured by AST. Frozen, unfixable this round; must be disclosed.
- New receipt bindings after instrument changes: **not yet done** — `.ufo/waves/round-89/evidence/`
  holds only `controls-r89.txt`; no after-r89 receipt exists, while C1's landing already changed
  r88/count-c2.py (8904a3d0 → 391268f8) and C2's landing will change both r88 counters again. The
  r88 receipt `after-r88.txt` pins `3ba0f97b…` / `8904a3d0…` at rev `d5e2eda4` — still valid *at
  its own revision*, but it no longer describes the current instruments.

**5 — E4/M5 visibility; don't relabel pre-data; F3 host-path replay and r87 receipt gaps remain
open unless corrected with their own evidence; new receipts don't retroactively supply old stdout.**
Status: E4 and the M5-sketch erratum (E2) remain visible only in `.ufo/waves/round-88/contract.md`
(Errata E2/E4) and `corpus/lessons/round-88.md:171-175`; **the r89 contract does not restate them**.
Not relabeled ✓ (r88 artifacts unchanged). F3 host-path replay: **still open** — the two r86
`required` receipts carry `--repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch .`
(verified in `round-86/evidence/after-c1-r86.txt` / `replay-defeat-r86.txt` headers), so the r87
gate's `replay=4` leg — and therefore **C1's `real=met` leg** — is host-path bound. The contract
carries F3 as out of scope but does not state that the C1 predicate inherits it.

## 3. The five absent entering anchors (independently measured)

Anchor-occurrence census of the twelve frozen `MUTANTS` anchors
(`round-89/count-c2.py:41-77`), per file and revision:

| mutant label | declared arm | file | entering `30a29797` | tip `760428ab` | E01/E02 candidate |
|---|---|---|---|---|---|
| C1-arms-first | arms_last_tally | r88 c1 | 1 | 1 | 1 |
| C1-green-drop-fail | green_mixed_fail | r88 c1 | 1 | 1 | 1 |
| C1-own-ok | own_ok_red | r88 c1 | **0** | **0** | 1 |
| C2-target | target_full | r88 c2 | **0** | **1** | 1 |
| C2-printed-target | met_line_derived | r88 c2 | **0** | **0** | 1 |
| C2-fixture-clean | clean_wrong_split | r88 c2 | 1 | 1 | 1 |
| C2-receipt-name | receipt_name_bound | r88 c2 | 1 | 1 | 1 |
| C2-clone-top | clone_top_bound | r88 c2 | **0** | **0** | 1 |
| C2-own-ok | own_ok_red | r88 c2 | **0** | **0** | 1 |
| C2-verdict-first | verdict_last_wins | r88 c2 | 1 | 1 | 1 |
| C2-no-supersedes | absent_without_supersedes | r88 c2 | 1 | 1 | 1 |
| C2-vacuous-body | vacuous_body_fabricated | r88 c2 | 1 | 1 | 1 |

This is exactly the contract's five ("the two `own_ok_of` helpers, `met_line`, `clone_root_ok`
and the `arms=26` target") = {C1-own-ok, C2-own-ok, C2-printed-target, C2-clone-top, C2-target}.
Decomposition: **four** are supplied by E01/E02's helper extractions; **one — `C2-target` — was
supplied by C1's landing itself** (r88 count-c2 TARGET migrated arms=23 → arms=26 at `760428ab`,
anchor occurrence 0 → 1). So at the entering revision C2 reports `mutants=7 unanchored=5`
(controls-r89.txt §1 ✓); at the current tip it would report 8 anchored / 4 absent; `C2=met
unanchored=0` is reachable only after both candidates land on top of `760428ab`. Confirms
Mo89R02C2's identical census.

## 4. No-work counter confounds

**C1 (frozen `round-89/count-c1.py`):**
1. **FX-label inversion** (count-c1.py:289-290): the per-fixture line prints "accepted" when the
   *expectation held* — `FX comment accepted problems=cmd-binding` reads as if the receipt were
   accepted. The summary `state[kind]` maps the observed disposition correctly (want if good,
   flipped otherwise), so the frozen target line is unaffected — but the printed FX lines in
   `evidence/controls-r89.txt` read backwards ("FX comment refused problems=-" at entering = the
   receipt was accepted). Mo89R01C1 defect 5; Mo89M01Mut was told to inspect it. Frozen → disclose,
   don't fix. Same debt class as the routed "misleading `FX clean ... refused`".
2. **Fixture-set narrowness (the honest no-work/overfit confound):** the predicate's entire
   equivalence/anti-evasion surface is 3 rewritten `# cmd:` lines of ONE receipt
   (`record-sweep-r87.txt`) with ONE bound path (`tools/mori-record-sweep.py`) and ONE interpreter
   form (`python3 -I`). A rule that recognizes exactly those three command shapes satisfies the
   whole frozen predicate; it cannot see R01C1's 13 refusals or 3 accepted lookalikes. The three
   fixtures are well-built (all three replay-match the body, so refusal is attributable to the
   binding rule), but the predicate certifies the shapes, not the class.
3. **`arms=26` is a count, not an identity.** The counter checks the subject's printed tally
   `C2_COUNTER_SELFTEST pass=26 fail=0` (arms == (26,0)); it never requires the gate's three new
   arms to be the named ones (contrast the r87 gate's own `SUBJECT_LABELS` check). Control 2a
   measured the no-work leg: three label-only arms reach `arms=26` and the met line still fails —
   so the arm-count token in the C1 target carries no discrimination by itself.
4. **Self-reported subject greenness:** the subject-leg trusts the gate's own printed tally
   (`arms == (26,0)`). No digest pin of the subject anywhere in the C1 counter. Same D3 family as
   (3) in the routed list.
5. **Host dependence (F3 inheritance):** `real=met` requires the seven receipts including the two
   r86 `required` rows whose cmds carry `--repo /home/vgpnk/Projects/shokunin/mori-shokunin
   --scratch .` — the C1 predicate is host-path bound (carried by contract, but not stated inside
   the C1 claim text).
6. The equiv fixture's acceptance is a genuine positive (binding accepted **and** clone replay
   byte-matched at the receipt's own rev 25a74d4c) — but the replay runs at the *old* revision's
   bytes, so the control tests the rule's spelling acceptance, not the current tree's tool output.

**C2 (frozen `round-89/count-c2.py`):**
7. **Attribution is by label, not cause.** `killed()` (:120) requires red ∧ the declared arm's
   FAIL line; it does not require the *other* arms to stay green, nor that the failure is caused
   by the mutated construct. A subject arm that fails whenever its own bytes differ from a pinned
   digest (or any text-detecting check tied to the mutant's replacement text) would be "killed
   with attribution" while testing no semantics. This is the r88 checksum-canary class moved one
   level down; the counter's `canary_unattributed` arm covers only "red with no declared FAIL".
   Mitigated in practice: I read E01/E02's candidate arms and they are behavioral (arms_last_tally
   asserts last-of-two-tallies == (2,0); green_mixed_fail asserts green() refuses mixed output;
   own_ok_red asserts own_ok_of(1,…) is False; target_full asserts TARGET == the full arms=26
   literal; met_line_derived/clone_top_bound/verdict_last_wins/… call the extracted helpers) —
   but that is reading evidence, not a counter guarantee.
8. **No subject digest pin** (same as routed D3 above): identity is path@revision + exact-once
   anchor + pristine arm count 28/26.
9. **`arms_of` takes the LAST tally** (`for m in ARMS.finditer(out): pass`, count-c2.py:127-135) —
   the same "last wins" idiom the C1-arms-first mutant removes in the *subject*; a subject printing
   a later fabricated tally would shift the counted pristine arm total. The pristine arms are
   self-reported (28/26), and `ARMS_BY_FILE` is keyed by basename ("count-c1.py"/"count-c2.py") —
   collision-prone if a same-basename subject ever appears at another path.
10. **Skip-work control 2b is partially confounded** (corroborating Mo89R02C2 F1): the control's
    count-c1 patch appends the 3 labels *after* `own_arms_pinned` and rewrites
    `ARMS_BY_FILE {"count-c1.py": 24}` → 28 while `per_file_arms_frozen` still pins the literal 24
    → the patched count-c1 pristine is **red** (`FAIL per_file_arms_frozen 24`; `FAIL
    own_arms_pinned 25/28`; `pass=26 fail=2`), so its two "unattributed" readings are caused by
    the red pristine, not by the attribution rule. Only the count-c2 half (9 labels → 26 arms,
    green; 5 survivors) cleanly demonstrates "labels without assertions don't kill". The contract's
    own control-2 expected line froze the confounded `arms=26,26`; Mo89S02Record was told to
    record it as a confound. Also §2b runs at the *entering* revision, where 5 of 12 anchors are
    absent — so control 2b exercises 7 of 12 mutants, never the count-c2 count.
11. At entering, C2's tail prints `mutants=7` for a 12-label population (anchored-only counting).
    A reader could mistake `mutants=7` for the population size; `unanchored=5` is the separate
    field. Cosmetic, frozen.

## 5. Causal separability: C1's arms-26 migration vs C2's target-26 mutation

Measured chain:
1. C1's landing (`760428ab`) changed **r88/count-c2.py — a C2 subject**: `SUBJECT_ARMS` 23→26,
   `TARGET` arms=23→26, `arms_pinned` arm (:250) and `target_fields` arm (:247) re-pointed. It did
   NOT touch r88/count-c1.py (sha 3ba0f97b unchanged) or r87/count-c1.py (24 arms unchanged).
2. The frozen C2 anchor for `C2-target` is that migrated literal
   (`TARGET = "real=met fx=4 clean=1 refused=2 absent=1 arms=26"`): occurrence **0 at entering,
   1 at tip**. Consequence: **C2 cannot be measured as met on any tree that lacks the C1 landing**;
   the claims are serialized, and the C2 population is partly a regression test of C1's own
   migration output.
3. `arms=26` is overloaded across at least four distinct facts: (i) r87 gate selftest arms
   (r89 count-c1 `SUBJECT_ARMS=26`; r88 count-c2 `SUBJECT_ARMS=26` + `arms_pinned` + `target_fields`);
   (ii) r88 count-c2's own selftest arms after E02 (r89 count-c2 `ARMS_BY_FILE["count-c2.py"]=26`);
   (iii) the r89 C2 target tail `arms=28,26` (= r88 c1 selftest arms 28, r88 c2 selftest arms 26);
   (iv) the C2-target mutation's literal. E02's candidate must simultaneously keep `SUBJECT_ARMS=26`
   (r87-gate pin), keep `TARGET arms=26` (mutation anchor), and hold exactly 26 own arms
   (ARMS_BY_FILE) — three 26s in one file, two of them coincidental. My checks confirm the
   candidate satisfies all three.
4. Blast radius of the pinned 26: arming the seven carried r87 clauses later (SCORECORD Planned
   r89 item 2, contract-carried) moves the r87 gate off 26 arms and breaks, in one stroke:
   r89 count-c1 `SUBJECT_ARMS=26`; r88 count-c2 `SUBJECT_ARMS`/`TARGET`/`arms_pinned`/
   `target_fields`; the frozen C2-target anchor (unanchored → C2=unmet). The r89 instruments
   therefore pin the r87 gate's arm count at 26 for as long as they are frozen — the contract's
   out-of-scope declaration is load-bearing, and the *reason* it names ("arming them would couple
   the two claims") is exactly this measured chain.
5. Base-of-candidate hazard: E02's candidate must be exported from `760428ab` (it was). Built from
   the entering revision instead, its `SUBJECT_ARMS=23`/`TARGET arms=23` would unanchor C2-target
   and contradict E02's `target_full` assertion → pristine-red → C2=unmet. Safe direction, but a
   wasted-integration trap. E01's candidate is insensitive (its file was untouched by C1).
6. Digest consequence: C1's landing invalidated the r88 receipt's `counter-sha256` binding for
   count-c2.py *relative to current bytes* (8904a3d0 → 391268f8; the receipt still verifies at its
   own rev `d5e2eda4`, where `sha256_at(repo, fields["rev"], bpath)` measures). C2's landing will
   invalidate both r88 counters' digests again → the "new receipt bindings after instrument
   changes" clause (routed D4) is a mandatory L1 deliverable, currently missing.

## 6. Existing learner patterns for shell/path binding

- **`tools/mori-pin-check.py`** — the lane's closest existing pattern for the exact question the
  new rule answers: `INTERPRETERS = ("python3","python","bash","sh")` (:181);
  `derive_command` tokenizes with `shlex.split` and requires `words[0] in INTERPRETERS`
  (:538-560) — i.e. an interpreter-allowlist + argv-position notion; and `split_env` (:495-503)
  strips leading `VAR=value` assignment words (K2, round-48) — a ready-made fix shape for the
  env-prefix refusals R01C1 measured (E08/E09) that the landed `script_position` does not reuse.
  `inside_tree` (:372-378) is normpath + realpath containment with the `root + os.sep` suffix fix.
- **`tools/mori-gate-registry.py:118-134`** — `safe_relpath` (posixpath.normpath, rejects
  absolute/`..`) + `inside_repo` (os.path.realpath containment): the lane's canonical-path
  identity pattern, grounded by `corpus/knowledge/containment-timed-supersede-r38.md`
  (S226/S228: containment is decided on the resolved canonical path; lexical rejection is only a
  pre-filter; realpath does not require the path to exist).
- **`corpus/knowledge/execution-evidence-r86.md`** — "a recorded command and its stdout are not a
  verified binding": the epistemic frame for C1's honest limit (naming/position ≠ execution).
- **`corpus/QUALITY.md` 184/185** — 184: the token check is "necessary … not execution provenance"
  with "argv reached through a shell wrapper" out of scope; 185: "no-harm is checked against
  semantically equivalent valid inputs as well as the original population" — the criterion
  R01C1's 13-refusal table shows the frozen fixture set does not satisfy. 184's text still
  describes the *token* rule and is now stale w.r.t. the landed script-position rule (corpus
  correction owed with D1; the landed knowledge entry `execution-binding-r89.md` is the vehicle).
- **`corpus/knowledge/receipt-counterfeit-r88.md`** — the three named r88 limits (comment token,
  self-print, spelling≠identity) that C1 targets, plus the (uncommitted) Round-89 correction.
- The r87 gate's own prior `PATHISH` regex (:68) + `export_rev` whitespace-token export — the
  pre-89 "pathish token" pattern; note `./tools/x.py` still passes PATHISH and `git cat-file -e
  rev:./tools/x.py` resolves (rc 0, verified), so clone-replay of the `./` spelling works.

## 7. Ownership and true dependencies

- **Owner:** mori lane (L1 MoriR89 integrates; PROVINCE: detection/report only, own-evidence
  accounting is mori's, not kumitate's lifecycle authority — connector seat's call).
- Files and their claim roles: r87/count-c2.py = C1 subject (registered gate, SKILL rows 21/23);
  r88/count-c1.py + r88/count-c2.py = C2 subjects (SKILL row 22 supersedes row 21; row 23
  supersedes row 21's gate arm count and row 22's r88 arm counts); r89/count-c1.py + count-c2.py
  = frozen counters (row 23). Contract write scope: those files + round-89/** + SKILL.md row +
  corpus/** + SCORECARD.md + LOG.md. **PROVINCE.md is outside the contract's write scope** — and
  PROVINCE currently has no round-87/88/89 appended scope notes at all (last is Round-86, line
  671), although r82–r86 each appended one for exactly this class of change (rule change on an
  existing instrument). Naming the gap is in scope for this report; closing it would need a
  contract-scope amendment.
- Landing dependencies (serialized): C1 landed (`760428ab`) → L1 lands E01+E02 candidates at
  `.ufo/waves/round-88/count-c1.py` / `count-c2.py` (the frozen counter grades those paths at R)
  → measure C2 at that revision (`C2=met … arms=28,26`) → issue new receipts binding the new
  digests (r89 counters `f8e6c39e`/`40eacccc`, r87 gate `d7ea961a`, r88 counters post-C2) →
  SCORECARD/LOG/lesson updates, E4/M5 carry-forward, QUALITY-184 correction, and the D1
  lesson/LOG append.
- Measurement constraints L1 must not miss: the C2 after-revision must descend from `760428ab`;
  both candidates' selftests must run standalone (they do — pure-function selfchecks); the r88
  count-c1 candidate's EXPECTED_ARMS must stay 28 with the new arms inserted before
  `own_arms_pinned` (E01 ✓); the r88 count-c2 candidate must keep `SUBJECT_ARMS=26` and the exact
  `TARGET` literal (E02 ✓), and must hold exactly 26 own arms (E02 ✓, 26 = 17+9).
- Corpus dependency: `corpus/knowledge/execution-binding-r89.md` must land with the D1 correction
  or the knowledge entry's forward reference dangles (it already does in the worktree text).

## 8. Considerthese note (per seat brief)

`considerthese/2026-10-26.md` is the latest daily reflection and it stops at round 50 — the lane
has since run rounds 51–89 with no newer file. Proposal 2 ("follow unfixed critic flags forward")
is the mechanism this round implements (the five routed defects); proposal 3 ("re-execute what
closures only evidence-verified") is Mo89E03Replay; proposal 1 (pin-check env/stale split) and
proposal 4 (adoption status line) are already adopted per LOG.md's adoption lines.

## 9. Tooling

None installed or updated (python3 3.14.8 stdlib only, per RULES.md; pacman pause respected).

## Trailer

Report: .ufo/waves/round-89/w1/Mo89Sc01Scope.md
