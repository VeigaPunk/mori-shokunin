# Mo90M01Mut — mutation probe of the candidate branch rule and the three new C2 arms

Seat: Mo90M01Mut (mutation-tester), judged on **operability**. Round 90, wave 1.
Entering revision for every read: `d1c8488986512a6a0475af88cc52779ce4703e00`
(`git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD` printed it on the seat's
first read). The wave landed while I measured: **`11197820c6dc44140d09eee3172ae91814d383bf`**
(the subjects) and then **`9441ef306250b2cd7bb3373ded473d15077187e0`** (after receipt and prose;
the four subjects are byte-identical at both). The integrated subjects are byte-identical to the
candidates I mutated:

| subject | path | sha256 | role |
|---|---|---|---|
| gate | `.ufo/waves/round-87/count-c2.py` = `w1/candidates/r87-gate.py` | `3fc9cc44a4f7ba6462aa36db48618f90018cb407981a532c183bdf13c6f1b377` | `invocations_visited` pre-pass; Table 1 |
| c1 arms | `.ufo/waves/round-88/count-c1.py` | `efe4f1f75cd7fce4fe1ce56558f76b4ccea84f6a9d684c99ea53c27322ef40e3` | 29 arms, B1 |
| c2 arms | `.ufo/waves/round-88/count-c2.py` | `fe9ed6acd300e6002196bdd474d865b0ef8a29c1b33b56c44f004e21da08fe51` | 27 arms, B4/B6 |
| battery | `.ufo/waves/round-90/battery/branch-heldout.json` | `562b390bad89dd570e6cc9e102af846797e9c09bf36a120e6ef61050b8b58f74` | 18 cases, 14 branch |

The candidate files churned three times under me. `w1/candidates/r87-gate-e01.py`
(`ab0c9104…`) is the gate author's own final snapshot (`Mo90E01Gate` states it applies only to
that sha); `79350315` was an earlier integrator rewrite (graded; superseded); `3fc9cc44` adds
`control_atoms` and is what landed. Every table below names its sha; I graded the bytes that
exist in the tree, and the two frozen counters at the landed rev both read `met`.

At the landing commit and again at the current tip, read-only, with the frozen counters:

```
python3 -I .ufo/waves/round-90/count-c1.py 0a1f019b16d8 --repo <lane> --scratch <S>/tmp
C1=met branch_open=0 harm=0 newopen=0 open=22 cases=78 rev=0a1f019b16d8
BATTERY cases=18 branch_cases=14 branch_open=0 harm=0 newopen=0 open=0 gained=0 paths=1

python3 -I .ufo/waves/round-90/count-c2.py 0a1f019b16d8 --repo <lane> --scratch <S>/tmp
C2=met mutants=15 killed=15 survivors=0 unattributed=0 unanchored=0 isolated=0 literal_anchors=0 arms=29,27 rev=0a1f019b16d8
```

(the same output at `11197820`, `9441ef30` and `0a1f019b`; the four subjects are byte-identical
across them)

## Method (one live `--shared` clone, commit-per-mutant)

```
S=/fast/scratch/hyaku/mori-r90/Mo90M01Mut
git clone --shared -q /home/vgpnk/Projects/shokunin/mori-shokunin $S/clone
git -C $S/clone checkout -q --detach d1c8488986512a6a0475af88cc52779ce4703e00
git -C $S/clone rev-parse --show-toplevel        # printed $S/clone before every commit
```

Each mutant is one exact-string replacement (anchor occurrence asserted `== 1`) written over
`.ufo/waves/round-87/count-c2.py` in the clone, committed there, and graded by the frozen counter
against the entering gate at `30a29797`:

```
TMPDIR=$S/tmp python3 -I $S/clone/.ufo/waves/round-90/count-c1.py <mutrev> \
    --repo $S/clone --scratch $S/tmp
```

The clone carries the independent held-out battery byte-for-byte, so the counter's `BATTERY`
population is graded too. Drivers `$S/drive_gate.py` (specs `$S/spec-candidate2.json`,
`$S/spec-committed.json`) and `$S/drive_arms.py`; after every gate run the bytes were restored and
`pristine_sha == restored_sha` printed `True`.

Pristine reading at the graded rev `cf184e2c`, rc 0:

```
C1=met branch_open=0 harm=0 newopen=0 open=22 cases=78 rev=cf184e2c5488
BATTERY cases=18 branch_cases=14 branch_open=0 harm=0 newopen=0 open=0 gained=0
```

Verdicts: `killed` = the frozen counter's printed numbers differ from pristine in the main
population or the battery population (or the counter aborts); `survived` = identical in both.

## Table 1 — 24 single-point mutants of the final reachability rule (`3fc9cc44`)

Columns: main population `{branch_open, harm, newopen, open}` and battery `{branch_open, harm}`.
`branch_open` counts the 8 frozen ids the gate still binds.

| id | single-point mutant | main bo | harm | newopen | open | bat bo | bat harm | verdict |
|---|---|---:|---:|---:|---:|---:|---:|---|
| P0 | pristine candidate | 0 | 0 | 0 | 22 | 0 | 0 | baseline (`C1=met`) |
| N01 | drop the not-live skip in `binds` (committed behaviour restored) | 8 | 0 | 0 | 30 | 14 | 0 | killed |
| N02 | swap `&&`/`||` in the AND-OR state machine | 3 | 0 | 0 | 18 | 2 | 0 | killed |
| N03 | invert the statically-succeeding head status | 2 | 0 | 0 | 17 | 5 | 0 | killed |
| N04 | drop the `exit`/`return` termination case | 3 | 0 | 0 | 25 | 6 | 0 | killed |
| N05 | accept any `exit` argument as terminating | — | — | — | — | — | — | killed (counter aborts, rc=1) |
| N06 | invert the exit status test | 1 | 0 | 0 | 23 | 1 | 0 | killed |
| N07 | drop the statically-failing `false` case | 3 | 0 | 0 | 25 | 1 | 0 | killed |
| N08 | drop the `terminated` conjunct on `;`/`&` | 2 | 0 | 0 | 24 | 6 | 0 | killed |
| N09 | drop the if-condition conjunct on the `then` body | 1 | 0 | 0 | 23 | 0 | 0 | killed |
| N10 | drop the already-selected conjunct on the `elif` body | 0 | 0 | 0 | 22 | 0 | 0 | **survived** |
| N11 | invert the `else` body test | 0 | 0 | 0 | 22 | 2 | 0 | killed (battery) |
| N12 | drop the loop-condition conjunct on the `do` body | 0 | 0 | 0 | 22 | 3 | 0 | killed (battery) |
| N13 | invert the empty-`for` list verdict | 0 | 0 | 0 | 22 | 1 | 0 | killed (battery) |
| N14 | drop the `until` status inversion | 0 | 0 | 0 | 22 | 1 | 0 | killed (battery) |
| N15 | drop the unmatched-`case`-arm subtraction | 0 | 0 | 0 | 22 | 0 | 0 | **survived** |
| N16 | treat every literal `case` arm as matched | 0 | 0 | 0 | 22 | 1 | 0 | killed (battery) |
| N17 | drop the literal-word guard (expansions treated as literals) | 0 | 0 | 0 | 22 | 0 | 0 | **survived** |
| N18 | invert the `!` negation mapping | 0 | 0 | 0 | 22 | 1 | 0 | killed (battery) |
| N19 | drop break/continue termination | 0 | 0 | 0 | 22 | 1 | 0 | killed (battery) |
| N20 | drop the nesting-level check in `binds` | 0 | 0 | 0 | 22 | 0 | 0 | **survived** |
| N21 | `same_path` accepts a parent prefix (old-rule control) | 0 | 0 | 0 | 22 | 0 | 0 | **survived** |
| N22 | invert the not-live skip (live commands dropped: harm direction) | 8 | 34 | 0 | 8 | 14 | 4 | killed |
| N23 | drop the `control_atoms` split (glued `)||` stays one token) | 0 | 0 | 0 | 22 | 0 | 0 | **survived** |
| N24 | do not split a glued `)` before its separator | 0 | 0 | 0 | 22 | 0 | 0 | **survived** |

Frozen ids rebound (main population): N01 all eight; N02 `N-A10,H02,H09`; N03 `N-A09,H01`;
N04 `N-A08,H03,H09`; N06 `H09`; N07 `N-A10,H02,H04`; N08 `N-A08,H03`; N09 `H04`; N22 all eight.
N05 aborts the counter before any field line (`ValueError: invalid literal for int() with base
10: ''` in `simple_status`, from a bare `exit` in `N-A08`/`H03`): red, but with no diagnosis.

**17 killed / 7 survived** (N10, N15, N17, N20, N21, N23, N24). No mutant except the deliberate
inversion N22 (`harm=34`, battery `harm=4`) makes a `met` case harm; the candidate itself is
`harm=0`, and every non-inverting mutant keeps `harm=0`.

Survivors and the one-line case that would kill each (coverage gaps, not permission to change the
contract):

* **N10** `elif` already-selected conjunct: `if false; then A; elif true; then python3 -I T;
  elif true; then python3 -I T; fi` — the second `elif` must be dead; battery `B11` does not
  distinguish it.
* **N15** unmatched-`case`-arm subtraction: a `case` whose unmatched arm names the path after an
  arm that exits, in a shape `B03`/`B12` do not cover.
* **N17** literal-word guard: `case $x in foo) python3 -I T;; esac` (dynamic subject must stay
  bound; dropping the guard lets `arm_live` prove a live arm dead).
* **N20** nesting-level check: a 4-deep `bash -c` nest of the bound path (same gap as r89 A34).
* **N21** parent-prefix `same_path`: a command naming a *prefix* of the bound path (`tools`,
  `tools/mori-record-sweep.py/..`); nothing in either population does.
* **N23/N24** the new `control_atoms` split: a glued control token in a *branch* position, e.g.
  `(exit 1)&& python3 -I T` or `(exit 1)|| printf x; python3 -I T` — no counted case and no
  battery case has a glued `)`+operator, so the split is unexercised in both directions.

## Table 2 — 21 single-point mutants of the committed gate's reachability rule (control)

Subject `.ufo/waves/round-87/count-c2.py` at `d1c84889` (sha256 `10c126f8f684fbc0…`); same
counter, battery present. Every mutant keeps `branch_open=8` on the main population and 14 on the
battery: the old surface cannot move the branch class at all.

| id | single-point mutant | main bo | harm | newopen | open | bat bo | verdict |
|---|---|---:|---:|---:|---:|---:|---|
| P0 | pristine committed gate | 8 | 0 | 0 | 30 | 14 | baseline |
| G01 | drop the excluded-position conjunct (data positions bind) | 8 | 0 | 2 | 38 | 14 | killed |
| G02 | `same_path`: drop the absolute-token refusal | 8 | 0 | 0 | 30 | 14 | **survived** |
| G03 | `same_path`: accept a parent prefix | 8 | 0 | 0 | 30 | 14 | **survived** |
| G04 | `same_path`: drop the realpath identity conjunct | 8 | 0 | 0 | 30 | 14 | **survived** |
| G05 | `binding_problems`: invert the static replay-status test | 8 | 0 | 5 | 41 | 14 | killed |
| G06 | `binding_problems`: any-missing → all-missing | 8 | 0 | 0 | 30 | 14 | **survived** |
| G07 | `binds`: drop the nesting-level check | 8 | 0 | 0 | 30 | 14 | **survived** |
| G08 | `binds`: invert the nesting-level check (`depth >= DEPTH`) | 8 | 0 | 0 | 36 | 14 | killed |
| G09 | `strip_comments`: `&&`→`||` in the comment-start test | 0 | 34 | 0 | 0 | 0 | killed |
| G10 | `head_index`: `&&`→`||` in the env `-C/-S` refusal | 8 | 0 | 0 | 30 | 14 | **survived** |
| G11 | `python_excluded`: drop the `-c/-m` exit case | 8 | 0 | 0 | 30 | 14 | **survived** |
| G12 | `python_excluded`: drop the `--` exit case | 8 | 0 | 0 | 30 | 14 | **survived** |
| G13 | `python_excluded`: drop the stdin `-` exit case | 8 | 0 | 0 | 30 | 14 | **survived** |
| G14 | `invocations`: a redirect target becomes an ordinary word | 8 | 0 | 0 | 30 | 14 | **survived** |
| G15 | `excluded_words`: drop the `echo/printf/:/true/false` operand exclusion | 8 | 0 | 1 | 35 | 14 | killed |
| G16 | `strip_comments`: drop backslash-escape handling | 8 | 1 | 0 | 30 | 14 | killed |
| G17 | `strip_comments`: any character closes a quote | 8 | 0 | 0 | 30 | 14 | **survived** |
| G18 | `binds`: drop recursion into a quoted command string | 8 | 3 | 0 | 30 | 14 | killed |
| G19 | `python_excluded`: drop the `--check-hash-based-pycs` value exclusion | 8 | 0 | 0 | 30 | 14 | **survived** |
| G20 | `entering_binds`: drop quote stripping from the fallback | 8 | 0 | 0 | 30 | 14 | **survived** |
| G21 | `same_path`: drop the empty-token guard | 8 | 0 | 0 | 30 | 14 | **survived** |

**7 killed / 14 survived** on the committed surface.

## Table 3 — the three declared C2 mutants on the landed arm candidates

Driver `$S/drive_arms.py`; each mutated copy run as
`python3 -I <copy> --selftest --scratch <dir>`; the full `FAIL` label set is captured from the
output. Anchors are verbatim from the frozen `MUTANTS` tuple in `.ufo/waves/round-90/count-c2.py`
and each occurred exactly once.

| mutant | subject | pristine tally | mutant tally | rc | complete FAIL label set | verdict |
|---|---|---|---:|---:|---|---|
| B1 `own_ok_arm_count` | `count-c1.py` | `pass=29 fail=0` | `pass=28 fail=1` | 1 | `{own_ok_arm_count}` | killed, attributed |
| B4 `met_line_call_site` | `count-c2.py` | `pass=27 fail=0` | `pass=26 fail=1` | 1 | `{met_line_call_site}` | killed, attributed |
| B6 `clone_root_negative` | `count-c2.py` | `pass=27 fail=0` | `pass=26 fail=1` | 1 | `{clone_root_negative}` | killed, attributed |

No FAIL set is a strict superset and none is empty, so `unattributed=0` and `isolated=0` for all
three; the frozen counter credits each kill (Table above, `C2=met … arms=29,27`). On the
pre-candidate committed bytes the same B4/B6 mutations produced no `FAIL` line, and on the first
28-arm c2 candidate the frozen counter read `arms=29,28` and `C2=unmet`; the landed 27-arm merge
is what meets the pin.

## Survivors per subject, with the exact command

| subject | mutants | survivors | command |
|---|---:|---:|---|
| landed gate `3fc9cc44` | 24 | **7** | `python3 -I $S/drive_gate.py $S/spec-candidate2.json auto`, each row graded by `python3 -I $S/clone/.ufo/waves/round-90/count-c1.py <rev> --repo $S/clone --scratch $S/tmp` |
| author snapshot `ab0c9104` (appendix) | 21 | **7** | `python3 -I $S/drive_gate.py $S/spec-candidate.json auto`, same counter |
| committed gate `10c126f8` | 21 | **14** | `python3 -I $S/drive_gate.py $S/spec-committed.json committed`, same counter |
| `count-c1.py` `efe4f1f7` | 1 (B1) | **0** | `python3 -I $S/drive_arms.py` |
| `count-c2.py` `fe9ed6ac` | 2 (B4,B6) | **0** | same |

## Appendix — the gate author's first snapshot, `ab0c9104` (in-tree as `r87-gate-e01.py`)

Graded with the same counter and battery. It closed 8/8 frozen ids but only 4/14 battery cases
(`branch_open=10`), so it read `C1=unmet`; the integrator rewrite removed this gap.

| id | mutant (v1 rule) | main bo | harm | newopen | open | bat bo | verdict |
|---|---|---:|---:|---:|---:|---:|---|
| P0 | pristine v1 snapshot | 0 | 0 | 0 | 22 | 10 | baseline |
| C01 | drop the pre-pass call | 8 | 0 | 0 | 30 | 14 | killed |
| C02 | swap `&&`/`||` in `evaluate` | 5 | 0 | 0 | 27 | 12 | killed |
| C03 | invert the static-success head status | 2 | 0 | 0 | 24 | 11 | killed |
| C04 | drop the `exit`/`return` termination case | 3 | 0 | 0 | 25 | 13 | killed |
| C05 | accept any `exit` argument as terminating | 0 | 0 | 0 | 22 | 10 | **survived** |
| C06 | invert the exit status test | 1 | 0 | 0 | 23 | 11 | killed |
| C07 | drop the statically-failing `false` case | 3 | 0 | 0 | 25 | 10 | killed |
| C08 | drop the static-status conjunct on the right operand | 5 | 0 | 0 | 27 | 12 | killed |
| C09 | drop the `terminated` conjunct in list sequencing | 2 | 0 | 0 | 24 | 12 | killed |
| C09b | invert the status-preservation test after termination | 0 | 0 | 0 | 22 | 10 | **survived** |
| C10 | drop the `if`-branch handling | 1 | 0 | 0 | 23 | 10 | killed |
| C11 | swap the `if` condition test on the then body | 1 | 0 | 0 | 23 | 10 | killed |
| C12 | invert the dead-word marking | 8 | 33 | 0 | 11 | 14 | killed |
| C13 | drop the unsupported-grammar guard | 0 | 0 | 0 | 22 | 9 | killed (battery only) |
| C14 | drop the decoded/token equality guard | 0 | 0 | 0 | 22 | 10 | **survived** |
| C15 | drop the single-word decoded guard | 0 | 0 | 0 | 22 | 10 | **survived** |
| C16 | drop the parenthesised-group parse | 1 | 0 | 0 | 23 | 13 | killed |
| C17 | let a group's `exit` terminate its parent | 0 | 0 | 0 | 22 | 10 | **survived** |
| C18 | drop the list-stop check | 2 | 0 | 0 | 24 | 13 | killed |
| C19 | drop the nesting-level check in `binds` | 0 | 0 | 0 | 22 | 10 | **survived** |
| C20 | `same_path` accepts a parent prefix | 0 | 0 | 0 | 22 | 10 | **survived** |

**14 killed / 7 survived** on `ab0c9104`. (The intermediate rewrite `79350315` read `C1=met` and
17/22 killed with survivors N10,N15,N17,N20,N21; `3fc9cc44` adds `control_atoms` and the two
survivors N23/N24.)

## Findings

1. **Both frozen claims hold on the landed bytes, and the mutation probe does not overturn them.**
   C1: `met`, 8/8 frozen ids and 14/14 battery branch cases refused, `harm=0`, `newopen=0`.
   C2: `met`, 15/15 killed, `isolated=0`, `unattributed=0`, `unanchored=0`,
   `literal_anchors=0`, `arms=29,27`.
2. **17/24 single-point mutants of the landed rule are killed**, covering every hinted class:
   drop-a-conjunct (N08, N09), `&&`/`||` swap (N02), drop-the-`exit`-case (N04), invert a
   static-status test (N03, N06, N18), nesting check (N20, survives), parent prefix (N21,
   survives). Seven survive; each has a concrete kill case above.
3. **The harm axis is pinned only by inversion.** None of the 23 non-inverting mutants raises
   `harm`; only N22 (live commands marked dead) does (`harm=34`, battery `harm=4`). A
   single-point defect in this rule therefore tends to *open* a branch rather than refuse a valid
   replay — the subtract-only direction holds structurally, and `harm=0` is not an accident of
   the population choosing.
4. **The battery is load-bearing for the claim, not decoration**: seven mutants (N11–N14, N16,
   N18, N19) are killed *only* by a battery delta, and the author's first snapshot was red on the
   battery alone. Without it, those seven would read as survivors on the 78-case population.
5. **A counter-aborting gate reads red but undiagnosed**: N05 makes `simple_status` raise
   `ValueError`; the frozen counter prints no field line (`rc=1`, traceback on stderr). That is
   `unmet`, not exit 2, so a crash and a field drift look alike unless stderr is read.
6. **Unpinned newest change**: the `control_atoms` split (N23/N24) has no distinguishing case in
   either population; a glued `)`+operator branch (`(exit 1)&& python3 -I T`) would pin it.

## Evidence and scope

* Pristine selftests: `r87-gate.py --selftest` → `C2_COUNTER_SELFTEST pass=26 fail=0`;
  `count-c1.py --selftest` → `pass=29 fail=0`; `count-c2.py --selftest` → `pass=27 fail=0`.
* Restoration: `pristine_sha == restored_sha` printed `True` for every gate run
  (`3fc9cc44…`, `79350315…`, `ab0c9104…`, `10c126f8…`); the clone's gate ends at the landed bytes.
* Nothing outside this report was written by me under
  `/home/vgpnk/Projects/shokunin/mori-shokunin`; the lane tip after my reads is `0a1f019b`, and
  the counters above were run read-only against it with scratch under `$S/tmp`.
* Tools installed: none. Scratch `/fast/scratch/hyaku/mori-r90/Mo90M01Mut` was removed after the
  numbers above were captured.
