# mori round-88 — frozen contract (claims, counters, controls)

lane: mori · round: 88 · attempt 1 · date: 2026-11-04 · L1: MoriR88
entering revision: `1bd5ec3fa260458f74eb32a2e5bb157209c5934d` (lane branch `master`, `ahead=0`)
axes: **operability** (score 7) and **calibration** (score 5, tied lowest: depth 5, freshness 5,
calibration 5). Detection and report only.

Two claims. Each is causally separable: C1 grades six selftest arms added to the r87 count-c1.py
counter; C2 grades the r87 count-c2.py receipt gate's refusal of two counterfeit bodies and the
real population's unchanged target line. Neither counter reads the other's work, and neither
edits the other's instrument.

## C1 — operability — six surviving r87-counter clauses get the failing arm each

**Frozen predicate P-C1** (identical sentence here, in `.ufo/waves/round-88/count-c1.py` and in
the receipt label):

> At revision R `python3 -I .ufo/waves/round-88/count-c1.py R` prints
> `C1=met mutants=6 killed=6 survivors=0 total=6 arms=24` and exits 0, where each of the six `old`
> anchors occurs exactly once in `.ufo/waves/round-87/count-c1.py` at R, the pristine copy's own
> `--selftest` is green with exactly 24 arms, and each mutated copy's own `--selftest` is killed by
> the frozen kill rule.

Population (all six survive the entering selftest; measured by the round-87 mutation matrix
`.ufo/waves/round-87/w1/Mo87M01Mut.md`, ranks 1, 3, 17, 18, 19, 20):

| mutant | file | clause |
|---|---|---|
| `M1-met-no-guard` | count-c1.py | the `met` refusal of unanchored/empty mutations |
| `M2-met-drop-empty` | count-c1.py | the `empty-mutation` half of that refusal |
| `M3-killed-n` | count-c1.py | the tail `killed=` split of the survivor tally |
| `M4-arms-total` | count-c1.py | the tail `arms=` sum over the subjects' own tallies |
| `M5-split-field` | count-c1.py | `target_split` reading `mutants` where it means `killed` |
| `M6-anchor-guard` | count-c1.py | the exactly-once anchor guard (`!= 1` vs `== 0`) |

Arms to land (one per clause, inside `.ufo/waves/round-87/count-c1.py`'s `selfcheck`; 18 → 24):

| arm | kills | fixture |
|---|---|---|
| `met_guard_unanchored` | M1 (and the undeclared `met-drop-unanchored` variant) | one killed anchor + one doubled anchor; `met` must be False with `total=1` |
| `met_guard_empty` | M1, M2 | one killed anchor + one empty mutation; `met` must be False with `total=1` |
| `killed_tally_mixed` | M3 | one killed + one survivor; tail `killed=1 survivors=1 total=2` |
| `arms_tally_passed` | M4 | a subject printing `pass=18`; tail `arms=18` |
| `target_split_killed_not_mutants` | M5 | `not target_split("mutants=6 killed=5 survivors=0 total=6 arms=24")` |
| `doubled_anchor_counted_type` | M6 | a doubled anchor is excluded, not graded: tail `mutants=0 total=0` |

**Kill rule (frozen):** a mutant is killed iff the mutated copy's own `--selftest` exits non-zero
**or** prints `fail=<n>` with n > 0, conditional on the pristine copy being green with exactly 24
arms. An anchor that does not occur exactly once is `unanchored` and never counted killed; an
empty mutation is `empty-mutation`; a red pristine, a wrong arm count, an unanchored anchor, an
empty mutation or a red detector keeps the claim unmet. Exit 2 is setup, never a pass.

**Do-nothing control (C1):** `.ufo/waves/round-88/evidence/controls-r88.txt` §C1 — the frozen
counter over the entering bytes reads `C1=unmet mutants=6 killed=0 survivors=6 total=6 arms=18`
(rc 1), and a label-only fixture that adds six passing `cases.append((label, True, ...))` rows to a
copy of the r87 counter, printing `pass=24 fail=0` with no assertion behind them, still reads
`C1=unmet … survivors=6` (rc 1). Labels and tallies alone are not the work.

## C2 — calibration — the receipt gate refuses two counterfeit bodies

**Frozen predicate P-C2** (identical sentence here, in `.ufo/waves/round-88/count-c2.py` and in
the receipt label):

> At revision R `python3 -I .ufo/waves/round-88/count-c2.py R` prints
> `C2=met real=met fx=4 clean=1 refused=2 absent=1 arms=23` and exits 0, where the graded
> `.ufo/waves/round-87/count-c2.py` at R is green at exactly 23 selftest arms, still prints the
> r87 target line on the real seven-receipt population, and refuses every counterfeit fixture:
> a `clone` receipt with its `# replay:` line removed reads `missing-replay`, a receipt whose
> `# cmd:` prints its own body reads `cmd-binding`, and a `# supersedes:` naming a receipt
> outside the population reads `SUPERSEDE … absent=1`.

Frozen fixture table (`FIXTURES` in the counter; each is one commit inside a `--shared` clone
under `--scratch`):

| fixture | receipt | mutation | required reading |
|---|---|---|---|
| `clean` | `record-sweep-r87.txt` | none | `C2=met` + the r87 target tail |
| `stripped` | `record-sweep-r87.txt` | `# replay: clone` removed, body fabricated | `C2=unmet`, `problems=missing-replay` |
| `vacuous` | `record-sweep-r87.txt` | `# cmd:` → `printf '<body>'` printing the body itself | `C2=unmet`, `problems=cmd-binding` |
| `absent-target` | `claim-sweep-r87.txt` | `# supersedes:` → `gone-r88.txt` (outside the population) | `C2=unmet`, a `SUPERSEDE … absent=1` line |

The fix in `.ufo/waves/round-87/count-c2.py` (17 → 23 selftest arms):

1. `declared_replay_problem()`: a population row declared `required` or `clone` whose receipt
   carries no `# replay:` line is `missing-replay` — never clean, never replayed.
2. `binding_problems()`: on a replayed row every `# counter-sha256:` path must appear as a
   `# cmd:` token, else `cmd-binding`; legacy rows keep the header-only rule (their `# limits:`
   records that the body is a worktree run).
3. `absent_supersede_targets()`: the post-loop `SUPERSEDE … absent=1` check is a helper with its
   own arm; the call site iterates it.
4. Six new arms: `missing_replay_required`, `missing_replay_clone`, `binding_in_cmd_ok`,
   `binding_not_in_cmd`, `binding_skipped_for_legacy`, `absent_target_helper`.

**Do-nothing control (C2):** `controls-r88.txt` §C2 — the frozen r88 counter over the entering
`1bd5ec3f` bytes reads `C2=unmet real=met fx=4 clean=1 refused=0 absent=1 arms=17` (rc 1): the
entering gate accepts both counterfeits with the exact r87 target line (fixtures `0057dcc8` and
`d206e324`), so the after value is not reachable by doing nothing.

## Freeze

Frozen at this commit, before any after-value existed: `count-c1.py`, `count-c2.py`, this
contract, `evidence/controls-r88.txt`. No target, population, fixture or kill rule moves after
data. A miss is an honest stop.

## Scope exclusion (declared before data)

The SCORECARD `## Planned (round 88)` item 3 (a dated full-census snapshot for the r86 value
channel's `differs`/`masked`/`absent` split) is **not claimed this round**: the r87 closure's
routed defects 2–4 make the receipt gate's own refusal forgeable, and that is the higher-severity
class. The item stays open for a later round rather than being widened into this one.

### Erratum E1 — the C1 detector's own fixture change at `d5e2eda4` (appended post-data, disclosed)

The first subject landing (`4d0f7bf0b0a0d978fa65d9b93edc37a2e6556550`) was graded by this frozen
counter and read `C1=unmet mutants=6 killed=4 survivors=2`, rc 1. The two survivors (`M1`,
`M2`) exposed that two of the *counter's own* selftest arms were satisfied for the wrong reason:
their witness fixtures (`dup.py`, `empty.py`) printed no `COUNTER_SELFTEST` line, so `arms_of`
read `(-1, -1)` and the arm's `met is False` came from `pristine-ok`, not from the guard the arm
names.

Fix commit `d5e2eda494877a85edaa4e287d6ad81843d9a8a1` changes exactly two fixture string literals
inside **this counter's** `selfcheck` (`dup.py` and `empty.py` gain
`print('COUNTER_SELFTEST pass=1 fail=0')`).

Disclosed because it moves instrument bytes after a data point existed:

- **No target, population or kill rule moved.** `TARGET`, `TARGET_ARMS`, `MUTANTS`, `ARMS_BY_FILE`
  and the kill rule are byte-identical between the freeze and `d5e2eda4`.
- **No subject byte moved.** The graded subject `.ufo/waves/round-87/count-c1.py` carries the same
  six arms and the same 24-arm tally at `4d0f7bf0` and `d5e2eda4`; the changed literals live in
  the r88 counter, not in the subject.
- **The entering control is unchanged** (`C1=unmet … survivors=6 … arms=18`), and the frozen
  label-only control still reads `C1=unmet … survivors=6 total=6 arms=24` under *both* counter
  byte sets (the wave's `Mo88E01C1Arms` measured the freeze bytes and the after bytes against one
  fixture: both refused).
- The after-value is therefore measured at `d5e2eda4`, not at `4d0f7bf0`; the unsuccessful first
  landing is kept in the record as the finding that exposed the defect.

### Erratum E2 — the C1 arm-table fixture cell for M5 (appended post-report, disclosed)

The C1 arm table above gives `target_split_killed_not_mutants` the fixture
`not target_split("mutants=6 killed=5 survivors=0 total=6 arms=24")`. The landed arm (in
`.ufo/waves/round-87/count-c1.py` at `d5e2eda4`, line 310-312) reads `arms=54`, not `arms=24`.
`arms=54` is the correct value: that counter's own `TARGET_ARMS` is 54, so the fixture must leave
`killed=5` as the only mismatch; with `arms=24` the arms field would also mismatch and the arm
would pass under the M5 mutant for the wrong reason. The code is right and the table cell is
wrong. No target, population or kill rule moves; the frozen predicate P-C1 never names this
fixture value. Recorded so a reader does not "fix" the code to match the cell.

### Erratum E3 — the two predicates' scope, against the wave's own attacks (appended post-wave, disclosed)

The wave's critic (`w1/Mo88C01Critic.md`) reproduced both after lines and then attacked them. Its
findings, accepted and routed:

1. **C1's kill rule does not bind the subject's identity.** A fabricated subject whose `--selftest`
   prints `COUNTER_SELFTEST pass=24 fail=0` and dies on any change to a pinned marker canary is
   graded `C1=met` by the frozen counter (fixture rev `79143f945e424b79892e730c431d5659ca0d07a7`,
   rc 0): every mutant "dies" by checksum, and the frozen kill rule — rc≠0 or `fail=<n>`, n>0 —
   cannot attribute a kill to a declared arm. `C1=met` therefore does **not** by itself prove the
   six arms exist or do anything. What does prove it, for the real subject, is the landed diff and
   the two independent re-measurements (`w1/Mo88E01C1Arms.md`, `w1/Mo88R01ReviewC1.md`), each of
   which maps every mutant to its named new arm on the real bytes. The frozen predicate is
   unchanged and true at the measured revision; the instrument is weaker than the claim's intent.
   Routed **R89-C1-subject-identity** (pin the subject's sha256 in the counter; make a kill count
   only when the contract-declared arm label appears in the mutant's `FAIL` lines).
2. **C2's "a `# cmd:` that prints its own body" sentence is fixture-wide, not class-wide.** A
   receipt whose self-printing command also names the bound path as a bare token passes: the
   critic's fixture `3e84f588bad2…` prints the full frozen target line. The pinned predicate names
   the two exact counterfeits (stripped header, `printf '<body>'` without the path) and holds; the
   contract's prose overstates the class. Routed **R89-C2-selfprint-evasion**.
3. **C2's token rule is spelling, not path identity.** `'tools/x.py'` and `"tools/x.py"` are
   accepted (quotes are stripped) but `./tools/mori-record-sweep.py` — the same file, replay rc 0,
   body matched — is refused (`cmd-binding`). The real seven-receipt population is unaffected
   (`C2=met … unexpected=0`), so P-C2's no-harm scope stands. Routed **R89-C2-path-identity**.
4. **Legacy-row wording.** The operational call site evaluates `binding_problems` on any row whose
   declared mode is `required`/`clone` *or* that carries a parsed replay marker; a legacy row that
   carried a `# replay:` line would be evaluated. No real legacy row does, so the population is
   unaffected. The table's "legacy rows keep the header-only rule" is a statement about the
   measured population, not a branch guard.
5. **`rc=2`/timeout counts as killed.** Same family as item 1; the kill rule's "exit non-zero" is
   not a proof of arm coverage.

No target, population, fixture or kill rule moved: all five items are scope statements about what
the measured lines do and do not prove, and each is routed with a round-89 witness.

### Erratum E4 — correction of E1 and final admission limits

E1's statement **“No subject byte moved” is false**. Commit `d5e2eda4` changed the
`dup.py`/`empty.py` tally literals in **both** `.ufo/waves/round-87/count-c1.py` (the subject)
and `.ufo/waves/round-88/count-c1.py` (the detector). The subject change makes its six added
arms load-bearing; the detector change strengthens its own analogous witnesses. The populations,
numeric targets and kill rule stayed fixed, but detector fixture bytes changed after the
first `killed=4 survivors=2` observation. This is post-data instrument drift, not a pre-data
amendment. The original freeze and after digests are retained in `Mo88S01Lesson.md`.

The critic executed the original freeze counter over the final real subject and reproduced
the target (`Mo88C01Critic.md:10-17`); that does not cancel the checksum-canary forgery.
C1's real arm improvements are directly measured, but the counter alone cannot prove its
intended property. C2's exact fixtures verify, while its new token rule rejects the genuine
`./tools/mori-record-sweep.py` spelling. The seven-row control is not a no-harm proof outside
those rows. **Final L1 recommendation: honest stop, not admission** — C1 instrument assurance
unprovable and C2 operability trade observed. No counter is repaired after these attacks.

E2's “post-report” refers to the seat report, not the fleet round report; E3 was written after
seat reports but before the formal WAVE-DONE handoff. The fleet report is filed only after
the parent sent `WAVE-DONE mori r88 w1` and supplied `w1-results.json`.
