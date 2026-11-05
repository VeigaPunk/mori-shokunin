# Mo90C01Critic — design falsification of P-C1 and P-C2

Seat: Mo90C01Critic (critic). Judged on: operability (C1), calibration (C2).
Entering revision verified: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD`
→ `d1c8488986512a6a0475af88cc52779ce4703e00`. Gate blob identical at `037c02ca` and `d1c8488`
(`git show <rev>:.ufo/waves/round-87/count-c2.py | sha256sum` → `10c126f8…` both).
Read-only on the lane: no production file touched, no lane commit. All experiments ran in
`$HYAKU_SCRATCH/mori-r90/Mo90C01Critic/` (clone + fixture commits there; `rev-parse
--show-toplevel` asserted before every fixture commit). No tool installed or upgraded. Scratch
removed before this report was written.

| # | question | verdict |
|---|---|---|
| 1 | is C1 reachable only by the claimed work? | **No — a 20-entry command-text lookup reaches the frozen target; the battery is the only guard and it is not held out** |
| 2 | does C2's isolation rule close the r89 canary hole? | **Partly — it closes the multi-label canary, but the dispatched B1/B4/B6 arms cannot survive it, and a single-label source-shape pin satisfies it by construction** |
| 3 | are the two claims causally separable? | **Asymmetric — C1 is standalone; C2's subject hard-codes C1's subject's arm count as an unobserved constant** |
| 4 | is any axis harmed? | **Yes — two measured (3 `met` cases are outside `harm`'s reach; `arms=27` forces deleting an existing arm) and one latent (battery `class` is self-declared, so an executing command could be required to be refused)** |

## 1. C1's target is reachable by a lookup table (measured)

Fixture: `git clone --shared` of the lane, the **committed** gate plus one appended block: a
21-string `frozenset` and a wrapper `binding_problems` that returns `["cmd-binding"]` when `cmd`
is in the set and otherwise delegates to the unchanged rule. The 21 = the 7 distinct frozen branch
texts + the 14 branch commands of the battery the sibling seat had just written
(`.ufo/waves/round-90/battery/branch-heldout.json`, untracked at the time; copied in and committed
in the clone). No control-flow reasoning, no shell parsing, no new function.

```
$ python3 -I .ufo/waves/round-90/count-c1.py 3c73e6562793 --repo <clone> --scratch <S>/tmp
C1=met branch_open=0 harm=0 newopen=0 open=22 cases=78 rev=3c73e6562793     rc=0
BATTERY cases=18 branch_cases=14 branch_open=0 harm=0 newopen=0 paths=1
```

That is the frozen sentence verbatim, against the real held-out battery. (An independent run with
a battery I authored reached the same line at `rev=7d85b75e6132`, `branch_cases=13`.) The frozen
table is 21 entries, not 22, because two frozen ids share one command text: `N-A10-false-and` and
`C02:H02-false-and` are byte-identical
(`.ufo/waves/round-89/r/Mo89R03Repair-evidence/cases.json:233` / `heldout-all.txt:6`) — the "eight
class counterfeits" are **seven distinct recorded strings**.

Why nothing stops it: `count-c1.py:120-126` `bound()` is the whole graded interface —
`gate.binding_problems(cmd, [("0"*64, BOUND)], True, repo)` on the *recorded text*; `gate_at`
(:107) only imports the module; the counter never runs the gate's `--selftest`, never reads an
anchor, never checks that the change added an arm. `load_battery` (:89) takes `class` straight
from the committed JSON, so the battery's authority is exactly the battery author's word. The
contract's "written by a seat that did not author the rule" is procedural: battery and rule land
in the same tree at the same revision, so the rule author can read every battery string, and the
counter cannot tell.

**Constants, not measurements.** `cases=78` is pinned by the counter's own arm
(`counted_population`, :262; `load_cases()` returns 81 rows, three carry `reach`).
`open=22` is a constant of the frozen split: 33 counted provenance rejects − 11 the entering gate
already refuses (measured at `037c02ca`: `22 open / 5 refused→refused / 6 bound→refused`, 8
branch, 37 met = 78). The only moving field is `branch_open` 8→0 plus the battery line;
`harm`/`newopen` are guards, trivially satisfied by any gate that keeps the committed behaviour.

**What would stop a table:** cases the author cannot read. That means commands *synthesized by
the counter at grade time* (template + per-run nonce), not a JSON in the repo. Nothing else does:
a battery committed "by another seat" is just 14 more table entries when both land in the same
revision.

## 2. C2: isolation closes the canary, the population forbids its own fix

The isolation rule does what it says (`count-c2.py:150-168` `killed`/`isolated`; detector arms
`isolation_multi_fail`, `canary_unattributed` — controls `C2_COUNTER_SELFTEST pass=21 fail=0`).
Measured against the real population, however:

* prescribed E02 arm (`own_ok_arm_count`, behavioural) + E03 arm (`clone_root_negative`,
  behavioural) + the two new arms in `count-c2.py`:
  `isolated .ufo/waves/round-88/count-c1.py C1-own-ok arm=own_ok_red fails=own_ok_arm_count,own_ok_red`
  and `isolated ... C2-clone-top arm=clone_top_bound fails=clone_root_negative,clone_top_bound`
  → `met=False`. Any arm that expects `own_ok_of`/`clone_root_ok` to return **False** also fails
  under the declared mutants that blunt those helpers (`return (True or …)`, `return True`), so
  the prescribed fixes are structurally incompatible with the frozen 15-mutant population.
* E03's AST pin is *unsatisfiable as written*: `FAIL met_line_call_site ast` on the untouched
  subject, because `round-88/count-c2.py:269-270` calls `met_line("abcdef1234567890")` inside
  `selfcheck`. The instruction "assert every Call to `met_line` passes `ast.Name(id='rev')`"
  describes a pin that reds the pristine copy. Scoped to `main`'s body it is green.

The only reachable configuration I found is three **source-shape** pins (B1: the pin text read back
from `__file__`; B4: AST scope on `main`; B6: `"startswith" not in clone_root_ok`'s body, which is
the one negative that survives `return True`) plus deleting `marker_literal`:

```
met=True mutants=15 killed=15 survivors=0 unattributed=0 unanchored=0 isolated=0 literal_anchors=0 arms=29,27
```

So the target is reachable — but all three "kills" grade source shape, and `killed` =
"exactly one FAIL label" cannot distinguish that from a behavioural kill. The same pattern is
already shipped in both counters (`round-88/count-c2.py:296`, `round-90/count-c2.py:406`, both
labelled `marker_literal`). What a structural pin leaves open: every reformatting-equivalent
defect, the subject calling the helper anywhere else with a literal (its own selftest does), and
the whole class of "arm restates the code it guards".

## 3. Coupling: none in reachability, one in truthfulness

C1 reads only `.ufo/waves/round-87/count-c2.py` at R, `.ufo/waves/round-90/battery/` at R, and the
round-89 case files **from the checkout** (`count-c1.py:44-46`, `load_cases` :74). C2 reads only
`.ufo/waves/round-88/count-c{1,2}.py` **at R** (`count-c2.py:46-47`, `loader` :212-214) and their
`--selftest`. Neither counter reads the other's subject. Measured: a clean checkout grades C1 with
no C2 artefact present (demo above), and `count-c2.py --selftest` is green with the gate untouched.

The measurable coupling is in C2's subject, not its target: `round-88/count-c2.py:34`
`SUBJECT_ARMS = 26` **is the round-87 gate's arm count**, asserted as an arm at :265 and checked
against the real subject only in `main` (:353). The r90 counter runs `--selftest`
(`count-c2.py:117`), so :353 is never observed. Today the constant is still true (gate at R and
the E01 candidate both print `C2_COUNTER_SELFTEST pass=26 fail=0`); the moment C1 adds or removes
a gate arm, `arms=29,27` still reads met while round-88's own receipt is red — a false pin that
C2's target cannot see. Latent, not active: C1's landing as dispatched does not change the count.

Second asymmetry: C1's population is a property of the **checkout**, not of R (`cases=78` can only
be read at the revision the counter happens to live in), while C2's is read with `git show R:`.
Third: `ENTERING = "30a2979…"` (`count-c1.py:50`) is the round-88 gate, not the round's entering
`037c02ca`; measured at `037c02ca`, `POPULATION … gained=2 open=30`, so control 1
("do-nothing") is not a no-op — it grades round 89's landing.

## 4. Harm to the axes

**(a) A valid command can be refused with `harm=0`.** `harm` only counts `met` cases the *entering*
gate binds (`tally`, :127-147). Measured at `037c02ca`: `N-E08-PWD-absolute` is `expect=met`,
refused by the gate and reported `refused-both`; `N-E07-double-slash` and `N-E14-escaped-path-chars`
are `entering=refused too. A rule at R that refuses all three reads `harm=0`.

**(b) The frozen `arms=27` forces an existing pin out.** 26 arms at entering
(`C2_COUNTER_SELFTEST pass=26 fail=0`), two declared arms required, and the frozen counter wants 27.
Measured with both new arms and nothing removed: `EXTRA pristine-arms … arms=28 want=27 → met=False`.
Dropping `marker_literal` (the only existing arm no declared mutant references) gives 27 and
`met=True`. That deletion is not disclosed in §P-C2 or in the population sentence, and it removes
the file's only `__file__` canary — the harness silently trades one self-referential arm for two.

**(c) Battery `class` is self-declared — no executing-command guard.** A battery branch case whose
command actually executes the bound path still counts as `branch_open` if refused, and `harm` never
looks at battery branch cases (`tally`'s battery call counts only the battery's `met` rows, :127-147).
Latent, not realised: the battery now on disk is clean — probe with the bound path replaced by
`touch <marker>` gives **0 of 14** branch cases executing. But nothing in the counter checks it: a
draft battery built from the E04 prompt's own shape list (`true &&`, `while :; do break; done` then
the command, `(exit 1); python3`) produced **4 of 13** executing cases and still read
`harm=0 branch_open=0`. Verified shell semantics: `bash -c 'true && echo EXECUTES-after-true-and'`
prints, and `while :; do break; done; touch <marker>` creates the marker. The battery is also
untracked right now; the counter reads it with `git ls-tree R`, so an uncommitted battery grades
`cases=0`.

## Smallest safe corrections

1. **C1 — synthesize the held-out population in the counter.** Replace `load_battery`'s file read
   with template expansion + a per-run nonce (`while false; do %s; done`, `false && %s`,
   `(exit 3) && %s`, `true || %s`, `if false; then %s; fi`, each with the bound path and its
   arguments interpolated), and keep the `BATTERY` line's shape. A command text that does not
   exist in the tree before the run cannot be table-matched; ~25 lines inside `count-c1.py`, no
   target change. Additionally reject at load time any battery branch case whose command, with the
   bound path replaced by a marker, still executes the marker — the battery on disk passes (0/14),
   but the counter has no field that would notice the next one that does not.
2. **C2 — declare the shape arms and the deletion, and stop prescribing behavioural arms for
   B1/B6.** The frozen kill rule makes B1/B6 unkillable behaviourally (measured `isolated=2`);
   the honest move is a `shape=2` field in the target and a named `marker_literal` replacement, so
   the after value says "13 behavioural + 2 source-shape" instead of "15 killed". If the target
   string is immutable, then `arms=27` must be read as 26 + 2 − 1 and the contract must say which
   arm goes. Scope the B4 pin to `main`'s body; as written it reds the pristine copy.
3. **Both — fix the baselines.** `ENTERING` should be the round's entering revision (`037c02ca`),
   and `load_cases` should read R03/C02 with `git show R:` so `cases=78` is a property of R.
   Extend `harm` to cases the entering gate refused (currently 3 counted `met` cases are
   unreachable to it), or report them as `refused_both` in the target so the reader sees them.

No score move is claimed; the lane is untouched.
