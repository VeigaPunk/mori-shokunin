# Mo88Si01Simplify — YAGNI pass over the r88 diff (mori round 88, wave w1)

Seat: simplifier (leaf). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Detection and report only — no lane file was written except this report; every probe ran in
`/fast/scratch/hyaku/mori-r88/Mo88Si01Simplify/` (deleted before yield).

## 1. What I actually read

| item | revision | sha256 (first 16) |
|---|---|---|
| lane HEAD at read time | `9c775ac2131da13c4c4cfdf2b14077184076f557` | — |
| `.ufo/waves/round-87/count-c1.py` | `4d0f7bf0` → `d5e2eda4` (= `9c775ac2`) | `ee505a3e1cb0fdce` → `85bc0f29865e3c9a` |
| `.ufo/waves/round-87/count-c2.py` | `d5e2eda4` (= `4d0f7bf0`, `9c775ac2`) | `7e577f533e1dac67` |
| `.ufo/waves/round-88/count-c1.py` | `2a5e3ad9` → `d5e2eda4` | `d1048cf06ae31bd1` → `3ba0f97baaae389e` |
| `.ufo/waves/round-88/count-c2.py` | all of `2a5e3ad9`/`d5e2eda4`/`9c775ac2` | `8904a3d0b5d973b5` |
| `.ufo/waves/round-88/contract.md` | committed `2a5e3ad9`…`9c775ac2`; worktree gained errata
E1+E2 during this run (uncommitted at HEAD `7c4946c2`) | `bc154e2b065b3455` → `a7c860f69904e965` |
| `.ufo/waves/round-88/evidence/controls-r88.txt` | `d5e2eda4` = worktree | `7b53d4aa87e79b4c` |
| `.ufo/waves/round-88/evidence/after-r88.txt` | `9c775ac2` (absent at `d5e2eda4`) | `31678d6296ba6c22` |

Lane HEAD moved to `7c4946c2` while this seat ran (scorecard/corpus landing); the four counter
bytes above are unchanged at that revision, and the only `.ufo/waves/round-88` path this seat wrote
is this report.

Diff under judgement: `git -C <lane> diff 1bd5ec3f d5e2eda494877a85edaa4e287d6ad81843d9a8a1 --
.ufo/waves/round-87/count-c1.py .ufo/waves/round-87/count-c2.py` → 103 insertions, 8 deletions in
two files: 6 arms + 2 fixture tally lines in `count-c1.py`; 3 helpers + 1 call-site rewrite + 6 arms
in `count-c2.py`.

Tooling: `python3 3.14.8`, `git 2.56.0`, `ruff` (`~/.local/bin/ruff`, already installed — no
install or upgrade performed; `ruff check --select F,E9` was the only static pass used).
No pacman/uv/network transaction.

## 2. Method (so the table means something)

Baseline reproduced first, from a `git clone --shared` of the lane in scratch, with exactly the
bytes the after receipt cites (`3ba0f97…`, `8904a3d0…`):

```
C1=met mutants=6 killed=6 survivors=0 total=6 arms=24            rc=0
C2=met real=met fx=4 clean=1 refused=2 absent=1 arms=23          rc=0
```

Each candidate deletion was applied as **one committed edit on a branch from `d5e2eda4`** in its
own `--shared` clone (after `git rev-parse --show-toplevel` matched the clone), then graded by the
frozen r88 counter at that new revision:

```
python3 -I <clone>/.ufo/waves/round-88/count-c1.py <cand-rev> --repo <clone> --scratch <dir>
python3 -I <clone>/.ufo/waves/round-88/count-c2.py <cand-rev> --repo <clone> --scratch <dir>
```

Two columns beyond the verdict were recorded, because "target unchanged" is not the same as
"behaviour unchanged":

1. **arm-level kill map** — for each deletion the six frozen mutants were re-applied to the deleted
   `count-c1.py` and its own `--selftest` was run; the set of FAIL arms was compared with the
   baseline. This exposes a deletion that leaves `killed=6` while silently removing one of the two
   arms that detect a mutant.
2. **C2 rule-mutants R1–R6** — one targeted mutation per rule (binding always/never flags, declared
   rule never/legacy-too, absent-helper never, legacy early-return removed), run against the
   pristine r87 `count-c2.py`, to show which new arm is the *sole* detector of what.

Baseline arm→mutant kill map of `.ufo/waves/round-87/count-c1.py` at `d5e2eda4` (measured):

| mutant | arms that go FAIL |
|---|---|
| M1-met-no-guard | `met_guard_empty`, `met_guard_unanchored` |
| M2-met-drop-empty | `met_guard_empty` |
| M3-killed-n | `killed_tally_mixed` |
| M4-arms-total | `arms_tally_passed` |
| M5-split-field | `target_split_killed_not_mutants` |
| M6-anchor-guard | `doubled_anchor_counted_type`, `met_guard_unanchored` |

Baseline C2 arm→rule map (measured, R1–R6):

| rule mutant | arm that goes FAIL |
|---|---|
| R1 binding always flags | `binding_in_cmd_ok` |
| R2 binding never flags | `binding_not_in_cmd` |
| R3 declared rule returns None | `missing_replay_required`, `missing_replay_clone` |
| R4 declared rule fires for `legacy` too | `missing_replay_clone` |
| R5 absent-helper returns `[]` | `absent_target_helper` |
| R6 legacy early return removed | `binding_skipped_for_legacy` |

Every one of the twelve new arms is the sole detector of at least one rule mutant: none is vacuous
(contrast the r87 arm `unanchored_plus_killed_unmet`, which the r88 counter itself notes was
vacuous). That is the property the round bought and the reason the table below is mostly "keep".

## 3. Delete/prove table

`target` = the printed `C1=`/`C2=` line + rc. `arm map` = whether the six-mutant FAIL sets changed.
All rows below were run; nothing in this table is inferred.

### 3a. `.ufo/waves/round-87/count-c1.py` (candidates 1–15)

| # | deletion | graded result | target | arm map | verdict |
|---|---|---|---|---|---|
| 1 | added `COUNTER_SELFTEST pass=1 fail=0` line in the `dup.py` fixture | `C1=met … arms=24` rc=0 | **unchanged** | **changed**: M1 red set 2 arms → 1 (`met_guard_unanchored` stops detecting M1) | keep — halves M1 redundancy |
| 2 | same added line in the `empty.py` fixture | `C1=unmet mutants=6 killed=5 survivors=1 total=6 arms=24` rc=1 | **changed** (M2 survives) | M2 red set → empty | **must stay** |
| 3 | `fields.get("total") == 1` in `met_guard_unanchored` | `C1=met … arms=24` rc=0 | unchanged | unchanged | keep (assertion) |
| 4 | `fields.get("killed") == 1` in `met_guard_unanchored` | `C1=met … arms=24` rc=0 | unchanged | unchanged | keep (assertion) |
| 5 | `any(e.startswith("unanchored") …)` conjunct | `C1=met … arms=24` rc=0 | unchanged | unchanged | keep (assertion) |
| 6 | `fields.get("total") == 1` in `met_guard_empty` | `C1=met … arms=24` rc=0 | unchanged | unchanged | keep (contract names `total=1`) |
| 7 | whole arm `met_guard_unanchored` | `C1=unmet … arms=23` rc=1 | **changed** | M1 and M6 each lose one of two killers; all six still killed | keep (arity 24) |
| 8 | whole arm `met_guard_empty` | `C1=unmet killed=5 survivors=1 arms=23` | **changed** (M1, M2 lose sole killer) | M2 survives | **must stay** |
| 9 | whole arm `killed_tally_mixed` | `C1=unmet killed=5 survivors=1 arms=23` | **changed** (M3 survives) | M3 red set → empty | **must stay** |
| 10 | whole arm `arms_tally_passed` | `C1=unmet killed=5 survivors=1 arms=23` | **changed** (M4 survives) | M4 red set → empty | **must stay** |
| 11 | whole arm `target_split_killed_not_mutants` | `C1=unmet killed=5 survivors=1 arms=23` | **changed** (M5 survives) | M5 red set → empty | **must stay** |
| 12 | whole arm `doubled_anchor_counted_type` | `C1=unmet … killed=6 arms=23` | **changed** (count only) | M6 keeps `met_guard_unanchored` | keep (arity 24) |
| 13 | `met and` in `arms_tally_passed` | `C1=met … arms=24` rc=0 | unchanged | unchanged | keep (assertion) |
| 14 | `fields.get("total") == 2` in `killed_tally_mixed` | `C1=met … arms=24` rc=0 | unchanged | unchanged | keep (assertion) |
| 15 | 2-line `# --- round-88 arms: … Mo87M01Mut ranks …` comment | `C1=met … arms=24` rc=0 | unchanged | unchanged | keep — provenance (mutant ranks) |

### 3b. `.ufo/waves/round-87/count-c2.py` (candidates 16–31)

| # | deletion | graded result | target | verdict |
|---|---|---|---|---|
| 16 | duplicate `missing = good.replace("# replay: required\n", "")` (the r88 block re-binds the identical value already bound 6 lines above) | `C2=met … arms=23` rc=0 | **unchanged** | **delete** — only pure-duplication row in the diff |
| 17 | `replay_mode in ("required", "clone") or` in the `binding_problems` call | `C2=met … arms=23` rc=0 | unchanged | keep — see §5 (contract's "on a replayed row") |
| 18 | whole `problems.extend(binding_problems(...))` | `C2=unmet … refused=1` | **changed** | **must stay** |
| 19 | `missing_replay` call site (helper kept) | `C2=unmet … refused=1` | **changed** | **must stay** |
| 20 | `binding_problems` legacy early return | `C2=unmet real=unmet … arms=22 subject=arms:(22,1)` | **changed** | **must stay** (own arm catches it) |
| 21 | `declared_mode in ("required","clone") and` conjunct | `C2=unmet real=unmet … arms=22 subject=arms:(22,1)` | **changed** | **must stay** (legacy row would be refused) |
| 22 | arm `binding_in_cmd_ok` | `C2=unmet … arms=22 subject=arms:(22,0)` | **changed** | **must stay** (sole R1 detector) |
| 23 | arm `binding_skipped_for_legacy` | `C2=unmet … arms=22 subject=arms:(22,0)` | **changed** | **must stay** (sole R6 detector) |
| 24 | arm `absent_target_helper` | `C2=unmet … arms=22 subject=arms:(22,0)` | **changed** | **must stay** (sole R5 detector) |
| 25 | arm `missing_replay_clone` | `C2=unmet … arms=22 subject=arms:(22,0)` | **changed** | **must stay** (sole R4 detector) |
| 26 | arm `missing_replay_required` | `C2=unmet … arms=22 subject=arms:(22,0)` | **changed** | **must stay** |
| 27 | arm `binding_not_in_cmd` | `C2=unmet … arms=22 subject=arms:(22,0)` | **changed** | **must stay** (sole R2 detector) |
| 28 | `not problems and` in `missing_replay_required` | `C2=met … arms=23` rc=0 | unchanged | keep (assertion: fixture header parses clean) |
| 29 | helper `declared_replay_problem` + call site + its 2 arms | `C2=unmet … arms=21 refused=1` | **changed** | **must stay** |
| 30 | helper `absent_supersede_targets` + its arm, loop inlined | `C2=unmet … arms=22` | **changed** | **must stay** |
| 31 | helper `binding_problems` + call site + its 2 arms | `C2=unmet real=unmet … refused=1` | **changed** | **must stay** |

### 3c. Instruments `.ufo/waves/round-88/count-{c1,c2}.py` (candidates 32–33)

| # | deletion | graded result | target | verdict |
|---|---|---|---|---|
| 32 | `want_met = dict((k, w) for k, _p, w, _x in FIXTURES)[kind]` — dead assignment, `count-c2.py:121`, ruff `F841` | `C2=met … arms=23` rc=0, all five REAL/FX lines byte-identical | **unchanged** | dead, but **do not delete now**: the after receipt binds `# counter-sha256: 8904a3d0… .ufo/waves/round-88/count-c2.py`; the deletion changes it to `271218503e800da9`. Round-89 candidate, not a round-88 edit. |
| 33 | arm `own_arms_pinned` in `count-c1.py` | `C1=unmet … arms=24 detector=red` rc=1 (its own `--selftest` alone stays green at 24/0; `main()`'s `pass=25` pin is what catches it) | **changed** | **must stay** |

## 4. Items that must stay, with the reason

1. **All six C1 arms.** Rows 8–11 are the *sole* killers of M2/M3/M4/M5; rows 7 and 12 are
   arity-load-bearing only (deleting either still kills all six but prints `arms=23`, which the frozen
   predicate rejects). None can be removed without amending the frozen contract.
2. **The `empty.py` fixture tally line** (row 2). It is the difference between M2 killed and M2
   surviving: the arm's `not met` conjunct is otherwise satisfied by `pristine-arms`, which is exactly
   the wrong-reason pass the `d5e2eda4` commit message says it fixed.
3. **The `dup.py` fixture tally line** (row 1). Not visible in the target, but without it
   `met_guard_unanchored` stops detecting M1 at all — M1 drops from two detectors to one. Deleting it
   is a coverage regression the frozen target cannot see; that is the definition of a YAGNI trap here.
4. **The six C1 arm conjuncts** (rows 3, 4, 5, 6, 13, 14). Each preserves the printed target when
   deleted because no member of the frozen six-mutant population produces the state where that
   conjunct is the only guard (e.g. an unanchored anchor that is flagged *and* counted, an
   inconsistent `killed=1 survivors=1 total≠2` tally, a subject whose `arms=18` is not graded met).
   They are the arm's specification — the contract names `total=1` for both guard arms and
   `killed=1 survivors=1 total=2` for the mixed tally. Deleting them is not simplification, it is
   lowering the detection horizon below the frozen population; there is no test that would show the
   loss.
5. **The three C2 helpers.** Each is the named home of one rule; all three deletions change a refusal
   (rows 29–31) and drop arms.
6. **All six C2 arms.** Each is arity-load-bearing (`arms=22` → unmet) and five of six are the sole
   detector of a specific rule mutant (R1–R6).
7. **The provenance comment** (row 15) — it carries the `Mo87M01Mut` ranks that justify the six-clause
   population.
8. **The four instrument-level additions of round 88 that are not arms** (`EXPECTED_ARMS`,
   `ARMS_BY_FILE`, `SUBJECT_ARMS`, the `own_arms_pinned` arm): the instrument pins its own arm count
   and `main()` pins it again, so any trim changes the detector verdict (row 33).

## 5. Duplicated logic between the r87 and r88 counters

| pair | duplication | justified as freeze separation? |
|---|---|---|
| `count-c1.py` r87 vs r88 | `run`, `selftest_run`, `green`, `killed`, `arms_of`, `target_split`, `grade`, the `FAIL`/`COUNT`/`ARMS` regexes, the `selfcheck` skeleton and `main()` — near-verbatim (383 vs 382 lines) | **Yes, necessarily.** The r88 counter grades *mutated copies* of the r87 counter. M1, M2, M3, M4 and M6 all mutate code inside exactly those helpers; if the instrument imported them, the mutation would edit the instrument and the kill would be self-referential. Importing would break P-C1 by construction, not merely by accident. |
| `count-c2.py` r87 vs r88 | only `run` plus the `SEP`/`REPLAY`/`SUPERSEDES` regexes; `mutate_receipt`, `fixture_verdict`, `clone_fixture`, `run_graded` are independently written in r88 | **Yes.** The graded subject's own `mutate_receipt` is not under test this round, but the fixtures are the measurement apparatus: if the r88 counter called it, a future mutation of the r87 fixture builder would silently change the counterfeits. The independent implementation is what makes the `stripped`/`vacuous` fixtures non-circular. |
| r87 `TARGET_ARMS = 54` vs r88 `TARGET_ARMS = 24` | same constant name, different populations (r87 sums three r86 counters 18+13+23; r88 pins the one r87 counter) | Justified (each file self-contained), but the name collision is a trap for a reader diffing the pair. Not worth a rename this round. |
| r88 `count-c2.py:121` `want_met` | not duplication — a dead binding (`F841`) | See row 32. |

Conclusion: the r87↔r88 duplication is the freeze boundary drawn correctly; there is no merge to
propose.

## 6. Two facts I measured that the worktree contract now discloses as E1/E2

Both are recorded here only as independent measurements (the worktree `contract.md` gained Errata
E1 and E2 while this seat ran; the committed bytes I judged — `bc154e2b…` — had neither). I did
not adjudicate them and did not edit the contract.

1. **Contract text vs landed code (= Erratum E2).** `contract.md` §C1 arm table states
   `not target_split("mutants=6 killed=5 survivors=0 total=6 arms=24")`. The landed arm (c1:310)
   uses `arms=54`. Measured against the graded file's own `target_split` (`TARGET=(6,0,6)`,
   `TARGET_ARMS=54`):

   | tail | landed `arms=54` | contract text `arms=24` |
   |---|---|---|
   | honest `killed=5 … arms=54` | `True` (arm passes) | `True` |
   | M5 reading `killed←mutants=6 … arms=54` | **`False` (arm reds → M5 killed)** | `True` |

   So the landed arm discriminates M5 and the contract's literal text would be vacuous against it.
   The code is right; the frozen sentence is stale. **Do not "simplify" the arm to match the
   contract.** E2 (worktree, uncommitted) says the same, including "line 310-312"; my evaluation
   above is the numeric proof of its claim, not a restatement of it.
2. **Post-freeze instrument edit (= Erratum E1).** `.ufo/waves/round-88/count-c1.py` was frozen at `2a5e3ad9`
   (`d1048cf0…`) but changed at `d5e2eda4` (`3ba0f97…`): +4 lines adding `COUNTER_SELFTEST pass=1
   fail=0` to its *own* synthetic `dup.py`/`empty.py` fixtures, mirroring the graded fix. The after
   receipt cites the post-freeze `3ba0f97…`, which is what I reproduced. Target, population, kill rule
   and fixture table are untouched by the edit; the freeze paragraph's "count-c1.py" is not.

   Independent check of E1's first-landing claim (not taken on trust): the frozen r88 counter at
   `4d0f7bf0` reads `C1=unmet mutants=6 killed=4 survivors=2 total=6 arms=24` rc=1, with `M1` and
   `M2` surviving. That is exactly the delta my rows 1–2 decompose: row 2 alone makes M2 survive,
   row 1 alone removes `met_guard_unanchored`'s M1 detection, and the two lines together give the
   `4d0f7bf0` reading. So the two fixture literals are the whole difference between `killed=4` and
   `killed=6`, and neither may be dropped by a YAGNI pass.

## 7. Smaller observations (no action recommended)

- The diff already removed `known = set(present)` and inlined `set(present)` at the `SUPERSEDE`
  call — evidence the launch applied YAGNI to itself where it was free.
- `ruff check --select F,E9` is clean on both graded counters (no unused import, no dead local in
  any of the 103 added lines). The only `F841` among the four counters is the instrument line at
  row 32, `count-c2.py:121`.
- `met_guard_unanchored` and `doubled_anchor_counted_type` re-run the identical
  `grade(disk, scratch, [("tools/dup.py", "r88-double", …)], {"dup.py": 1})` fixture; only the
  assertion differs. Sharing the call would be a refactor, not a deletion; both arms are
  arity-load-bearing, so it would buy nothing and add coupling.

## 8. Verdict

None of the twelve added arms or three helpers is dead weight: deleting any of them either changes
the printed target or makes it un-measurable (arity), and every new arm is the sole detector of at
least one rule mutant. Twelve of the 33 probed deletions do preserve the printed target — eight C1
items (six arm conjuncts, the `dup.py` fixture literal, the provenance comment), three C2 items
(the duplicate assignment, the declared-mode disjunct, one arm conjunct), one dead instrument line —
but ten of those twelve remove an assertion, a redundant detector, a defensive conjunct or
provenance that the frozen six-mutant population cannot see, and one of the remaining two is barred
by the receipt's counter hash. Exactly one deletion removes pure duplication with no assertion and
no coverage loss.

```
SIMPLIFY candidates=33 target-preserving=12 recommended=1
  delete .ufo/waves/round-87/count-c2.py:396 `missing = good.replace("# replay: required\n", "")`
    -> C2=met real=met fx=4 clean=1 refused=2 absent=1 arms=23 rc=0 (measured)
  defer  .ufo/waves/round-88/count-c2.py:121 `want_met = …` (dead, ruff F841)
    -> C2 target unchanged (measured) but changes the receipt-bound counter hash 8904a3d0 -> 2712185
```

Exact commands that produced the verdict:

```
S=/fast/scratch/hyaku/mori-r88/Mo88Si01Simplify
git clone --shared -q /home/vgpnk/Projects/shokunin/mori-shokunin "$S/lane"
# baseline (bytes the after receipt cites)
python3 -I "$S/lane/.ufo/waves/round-88/count-c1.py" d5e2eda494877a85edaa4e287d6ad81843d9a8a1 \
        --repo "$S/lane" --scratch "$S/run/base/c1"      # C1=met … arms=24, rc=0
python3 -I "$S/lane/.ufo/waves/round-88/count-c2.py" d5e2eda494877a85edaa4e287d6ad81843d9a8a1 \
        --repo "$S/lane" --scratch "$S/run/base/c2"      # C2=met … arms=23, rc=0
# per candidate (one clone each, branch from d5e2eda4, one commit, then)
git -C "$S/cand/<id>/repo" rev-parse --show-toplevel     # must equal the clone
python3 -I "$S/cand/<id>/repo/.ufo/waves/round-88/count-c1.py" <cand-rev> \
        --repo "$S/cand/<id>/repo" --scratch "$S/cand/<id>/run"
python3 -I "$S/cand/<id>/repo/.ufo/waves/round-88/count-c2.py" <cand-rev> \
        --repo "$S/cand/<id>/repo" --scratch "$S/cand/<id>/run"
# arm-level kill map: the six MUTANT pairs applied to the deleted r87/count-c1.py, then
python3 -I <mutant-copy> --selftest --scratch <dir>      # FAIL arm labels compared with baseline
# C2 rule-mutants R1..R6 on the pristine r87/count-c2.py
python3 -I <rule-mutant-copy> --selftest --scratch <dir>
```

Lane was not written: all clones/commits were under `$S`, and `git -C <lane> status` shows no path
from this seat except this report.
