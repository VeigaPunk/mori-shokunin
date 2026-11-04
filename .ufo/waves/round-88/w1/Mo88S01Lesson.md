# Mo88S01Lesson — round-88 lesson draft, wave w1

round: 88 · attempt: 1 · wave: w1 · lane: mori · seat: Mo88S01Lesson (scribe, leaf — no subagent
dispatch) · date: 2026-11-04
axes: **calibration** (this seat's item); the round's two claims are **operability** (C1) and
**calibration** (C2). Detection and report only.

This is the seat draft for `.ufo/waves/round-88/w1/Mo88S01Lesson.md`. The L1 integrates it into
`corpus/lessons/round-88.md`; this seat did not write and did not touch the corpus file. The draft
carries §1 the round's two claims (frozen predicate sentences, after lines, wave shape), §2 two
mined mistakes with the measurements that expose them, and §3 an empty placeholder for the L1's
merged seat findings. **No Gate row, SOURCES row, QUALITY criterion or spot-check verdict is
written here** — those are the L1's, not this seat's.

## Read set and byte hashes

Siblings and the L1 land work while a wave runs. These are the bytes this seat actually read, hashed
at read time; the worktree copies of the frozen files were re-checked equal to `9c775ac2`:

| artifact | revision | sha256 | bytes |
|---|---|---|---|
| `.ufo/waves/round-88/contract.md` | `2a5e3ad9` (worktree = `9c775ac2`) | `bc154e2b065b34554a7016d4991b6aea423194da436116632082790a355fb00e` | 7001 |
| `.ufo/waves/round-88/evidence/controls-r88.txt` | `2a5e3ad9` (worktree = `9c775ac2`) | `7b53d4aa87e79b4c1cfd60c61975ea06dbc4496da713abe4c8d2fe231006f6be` | 4816 |
| `.ufo/waves/round-88/evidence/after-r88.txt` | `9c775ac2` (worktree identical) | `31678d6296ba6c2226dcb77a566ee6e9324a2e7d9d1a1c8aca25edc46754a380` | 1701 |
| `.ufo/waves/round-88/count-c1.py` at the freeze | `2a5e3ad9` | `d1048cf06ae31bd15add31858bc204a44b711203dbb2e2bd6057450475baf2a1` | 17850 |
| `.ufo/waves/round-88/count-c1.py` at the after value | `d5e2eda4` | `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2` | 17958 |
| `.ufo/waves/round-88/count-c2.py` | `2a5e3ad9` = `d5e2eda4` | `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7` | 16286 |
| `.ufo/waves/round-87/count-c1.py` at the first landing | `4d0f7bf0` | `ee505a3e1cb0fdcef4afa141aaeb25870c270af997943b90d270843674faeb13` | 17631 |
| `.ufo/waves/round-87/count-c1.py` at the after value | `d5e2eda4` | `85bc0f29865e3c9a9de49940dcf12eef20977aa77899b6ba3290fcb243c7cc2c` | 17739 |
| `.ufo/waves/round-87/count-c2.py` | `4d0f7bf0` = `d5e2eda4` | `7e577f533e1dac676d3f5b3d601f2c4c622c57c325e6091e6018b5781ae73fc0` | 23111 |

The after receipt's own `# counter-sha256:` lines name `3ba0f97b…` for `count-c1.py` and
`8904a3d0…` for `count-c2.py`; the C1 hash is the `d5e2eda4` bytes, not the freeze bytes (see the
freeze note in §2).

## 1. What the round did

Axes: **operability** (score 7) and **calibration** (score 5 — tied lowest at depth 5, freshness 5,
calibration 5). Two causally separable claims, frozen at `2a5e3ad9` before any after-value existed,
each with a do-nothing control in `evidence/controls-r88.txt`.

### C1 — operability — six surviving r87-counter clauses get the failing arm each

**Frozen predicate P-C1** — quoted **verbatim** from `contract.md:18-22`:

> At revision R `python3 -I .ufo/waves/round-88/count-c1.py R` prints
> `C1=met mutants=6 killed=6 survivors=0 total=6 arms=24` and exits 0, where each of the six `old`
> anchors occurs exactly once in `.ufo/waves/round-87/count-c1.py` at R, the pristine copy's own
> `--selftest` is green with exactly 24 arms, and each mutated copy's own `--selftest` is killed by
> the frozen kill rule.

Population (all six survive the entering selftest; from `.ufo/waves/round-87/w1/Mo87M01Mut.md`,
ranks 1, 3, 17, 18, 19, 20): `M1-met-no-guard` (the `met` refusal of unanchored/empty mutations),
`M2-met-drop-empty` (its `empty-mutation` half), `M3-killed-n` (the tail `killed=` split),
`M4-arms-total` (the tail `arms=` sum), `M5-split-field` (`target_split` reading `mutants` where it
means `killed`), `M6-anchor-guard` (the exactly-once guard, `!= 1` vs `== 0`). Six arms land inside
`.ufo/waves/round-87/count-c1.py`'s `selfcheck`, 18 → 24:

| arm | kills | fixture |
|---|---|---|
| `met_guard_unanchored` | M1 (and the undeclared `met-drop-unanchored` variant) | one killed anchor + one doubled anchor; `met` must be False with `total=1` |
| `met_guard_empty` | M1, M2 | one killed anchor + one empty mutation; `met` must be False with `total=1` |
| `killed_tally_mixed` | M3 | one killed + one survivor; tail `killed=1 survivors=1 total=2` |
| `arms_tally_passed` | M4 | a subject printing `pass=18`; tail `arms=18` |
| `target_split_killed_not_mutants` | M5 | `not target_split("mutants=6 killed=5 survivors=0 total=6 arms=24")` |
| `doubled_anchor_counted_type` | M6 | a doubled anchor is excluded, not graded: tail `mutants=0 total=0` |

**Kill rule** — quoted **verbatim** from `contract.md:47-51`:

> **Kill rule (frozen):** a mutant is killed iff the mutated copy's own `--selftest` exits non-zero
> **or** prints `fail=<n>` with n > 0, conditional on the pristine copy being green with exactly 24
> arms. An anchor that does not occur exactly once is `unanchored` and never counted killed; an
> empty mutation is `empty-mutation`; a red pristine, a wrong arm count, an unanchored anchor, an
> empty mutation or a red detector keeps the claim unmet. Exit 2 is setup, never a pass.

**Do-nothing control (C1)** — quoted **verbatim** from `contract.md:53-57`:

> **Do-nothing control (C1):** `.ufo/waves/round-88/evidence/controls-r88.txt` §C1 — the frozen
> counter over the entering bytes reads `C1=unmet mutants=6 killed=0 survivors=6 total=6 arms=18`
> (rc 1), and a label-only fixture that adds six passing `cases.append((label, True, ...))` rows to a
> copy of the r87 counter, printing `pass=24 fail=0` with no assertion behind them, still reads
> `C1=unmet … survivors=6` (rc 1). Labels and tallies alone are not the work.

**After line** — quoted **verbatim** from `evidence/after-r88.txt`:

```text
C1=met mutants=6 killed=6 survivors=0 total=6 arms=24 rev=d5e2eda49487
```

### C2 — calibration — the receipt gate refuses two counterfeit bodies

**Frozen predicate P-C2** — quoted **verbatim** from `contract.md:64-70`:

> At revision R `python3 -I .ufo/waves/round-88/count-c2.py R` prints
> `C2=met real=met fx=4 clean=1 refused=2 absent=1 arms=23` and exits 0, where the graded
> `.ufo/waves/round-87/count-c2.py` at R is green at exactly 23 selftest arms, still prints the
> r87 target line on the real seven-receipt population, and refuses every counterfeit fixture:
> a `clone` receipt with its `# replay:` line removed reads `missing-replay`, a receipt whose
> `# cmd:` prints its own body reads `cmd-binding`, and a `# supersedes:` naming a receipt
> outside the population reads `SUPERSEDE … absent=1`.

The fix in `.ufo/waves/round-87/count-c2.py` adds three refusal paths (`declared_replay_problem`,
`binding_problems`, `absent_supersede_targets`) and six arms, 17 → 23. The frozen fixture table
(`FIXTURES`; one commit each inside a `--shared` clone under `--scratch`): `clean`
(`record-sweep-r87.txt`, no mutation, `C2=met` + the r87 target tail), `stripped` (`# replay: clone`
removed, body fabricated, `missing-replay`), `vacuous` (`# cmd:` made to `printf` its own body,
`cmd-binding`), `absent-target` (`# supersedes:` → `gone-r88.txt`, a `SUPERSEDE … absent=1` line).

**Do-nothing control (C2)** — quoted **verbatim** from `contract.md:94-97`:

> **Do-nothing control (C2):** `controls-r88.txt` §C2 — the frozen r88 counter over the entering
> `1bd5ec3f` bytes reads `C2=unmet real=met fx=4 clean=1 refused=0 absent=1 arms=17` (rc 1): the
> entering gate accepts both counterfeits with the exact r87 target line (fixtures `0057dcc8` and
> `d206e324`), so the after value is not reachable by doing nothing.

**After line** — quoted **verbatim** from `evidence/after-r88.txt`:

```text
C2=met real=met fx=4 clean=1 refused=2 absent=1 arms=23 rev=d5e2eda49487
```

The receipt's fixture body around those two summary lines:

```text
REAL rc=0 C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=d5e2eda49487
FX clean rc=0 refused C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=d5e2eda49487
FX stripped rc=1 refused problems=missing-replay
FX vacuous rc=1 refused problems=cmd-binding
FX absent-target rc=1 refused supersede-absent=1
```

### Wave shape

One v1 wave, **12 seats**: 3 executor (`Mo88E01C1Arms`, `Mo88E02C2Gate`, `Mo88E03SecondImpl`),
1 scout (`Mo88Sc01Scope`), 2 scribe (`Mo88S01Lesson`, `Mo88S02Knowledge`), 2 reviewer
(`Mo88R01ReviewC1`, `Mo88R02ReviewC2`), 1 critic (`Mo88C01Critic`), 1 mutation-tester
(`Mo88M01Mut`), 1 connector (`Mo88K01Conn`), 1 simplifier (`Mo88Si01Simplify`); **attack 4/12 =
33.3 %** (`Mo88R01ReviewC1`, `Mo88R02ReviewC2`, `Mo88C01Critic`, `Mo88M01Mut` — the two reviews,
the critic's attack list and the mutation matrix). Validated under policy v1 (`w1-dispatch.json`
counts `spawn 12`); every seat report lands under `.ufo/waves/round-88/w1/`; seats do not commit.

### This seat's measurements (C1 side only)

Scratch `/fast/scratch/hyaku/mori-r88/Mo88S01Lesson`, deleted before yield. No fixture git repo and
no commit were made: committed bytes were read with `git show`, and the counters' own `grade()` was
driven from scratch modules with `importlib`. Run outputs below are verbatim.

| # | measurement | observed |
|---|---|---|
| 1 | frozen `count-c1.py` (`2a5e3ad9`, `d1048cf0…`) `--selftest` | `C1_COUNTER_SELFTEST pass=25 fail=0`, rc 0 |
| 2 | landed `count-c1.py` (`d5e2eda4`, `3ba0f97b…`) `--selftest` | `C1_COUNTER_SELFTEST pass=25 fail=0`, rc 0 |
| 3 | r87 subject (`d5e2eda4`) own `--selftest` | `C1_COUNTER_SELFTEST pass=24 fail=0`, rc 0 |
| 4 | frozen counter at the first landing `4d0f7bf0` | `C1=unmet mutants=6 killed=4 survivors=2 total=6 arms=24 detector=green rev=4d0f7bf0b0a0`, rc 1 |
| 5 | landed counter at the same `4d0f7bf0` | identical line and rc — the C1 defect is in the subject bytes, not in the counter's grading |
| 6 | landed counter at the after value `d5e2eda4` | `C1=met mutants=6 killed=6 survivors=0 total=6 arms=24 rev=d5e2eda49487`, rc 0 |
| 7 | frozen counter at `d5e2eda4` | identical `C1=met …` line, rc 0 — the after value does not depend on the post-freeze counter edit |
| 8 | `str.count` of the M1 anchor in `.ufo/waves/round-87/count-c1.py` at `1bd5ec3f`, `4d0f7bf0`, `d5e2eda4` | short form (no leading newline): **2** at all three; leading-newline form: **1** at all three |

Readings 4–6 are the before/after pair §2 relies on; reading 7 is the freeze-independence check;
reading 8 is the anchor-doubling measurement.

### Verbatim provenance

Quoted verbatim from `.ufo/waves/round-88/contract.md`: the P-C1 block (18-22), the P-C2 block
(64-70), the kill-rule sentence (47-51), the C1 do-nothing control sentence (53-57) and the C2
do-nothing control sentence (94-97). Quoted verbatim from
`.ufo/waves/round-88/evidence/after-r88.txt`: the two `C1=`/`C2=` after lines and the five
`REAL`/`FX` lines reproduced above. Everything else in this draft is this seat's prose or its own
measured output. The entering values are **not** this seat's measurement: they are the control
receipt's, quoted with attribution.

## 2. Mistakes

Two rows, both real and both measured this round. Each row names the class, the bytes that carry the
mistake, the rule that caught it, and the fix with the observation that makes the fix able to fail.

| Class | Evidence pointer | Captured-by | Fix delivered and what makes it able to fail |
|---|---|---|---|
| `fixture-satisfied-for-the-wrong-reason` — the first `met_guard_*` fixtures omitted the `COUNTER_SELFTEST pass=1 fail=0` line, so the arm's `met is False` came from the pristine check (`pristine-arms … arms=-1 want=1`), not from the `met` guard the arm names. With the guard removed the fixture still read `met=False`, so the arm could not distinguish the mutant. | `.ufo/waves/round-87/count-c1.py` at `4d0f7bf0`: `dup.py` fixture at `:234` and `empty.py` fixture at `:248`, each `…print('FAKE pass=1 fail=0')\n"` with no tally line. The same omission sat in the witnessing counter `.ufo/waves/round-88/count-c1.py` at the freeze (`2a5e3ad9`), `:201-202`. | The frozen C1 kill rule, on the population it grades: the mutated copy's own `--selftest` must fail. At `4d0f7bf0` the frozen counter read `C1=unmet mutants=6 killed=4 survivors=2 total=6 arms=24 detector=green rev=4d0f7bf0b0a0` (rc 1) with `EXTRA survivor … M1-met-no-guard` and `M2-met-drop-empty`. The counter's own 25 arms were green at the freeze *and* after the fix — this defect is invisible to the detector's own witness and visible only in the graded population. | `print('COUNTER_SELFTEST pass=1 fail=0')` added to both fixtures in both files at `d5e2eda4` (`.ufo/waves/round-87/count-c1.py:234-235,249-250`; `.ufo/waves/round-88/count-c1.py` same two fixtures). With the fixture's own tally parseable and equal to the declared 1 arm, `pristine_ok` stays true and the `met` guard is the sole reason `met` can read False. After: `C1=met mutants=6 killed=6 survivors=0 total=6 arms=24 rev=d5e2eda49487`, rc 0. |
| `anchor-not-unique-in-its-own-file` — the M1 anchor was the bare clause text, which the counter also stores as data in its own `MUTANTS` table; `base.count(old)` read 2 at every revision, so the anchor was refused `unanchored` and never graded. | `.ufo/waves/round-87/count-c1.py`: the clause text occurs in the counter's own `MUTANTS` table entry for `M1-unanchored-conjunct` at `:60` and in the runtime guard at `:180` — `str.count` returns 2 at `1bd5ec3f`, `4d0f7bf0` and `d5e2eda4`. | The exactly-once anchor guard (`if base.count(old) != 1:` → `extras.append("unanchored %s %s occurrences=%d" …)`), which never counts such an anchor killed. Measured refusal at both `4d0f7bf0` and `d5e2eda4`: `unanchored .ufo/waves/round-87/count-c1.py M1-met-no-guard occurrences=2`, tail `mutants=0 killed=0 survivors=0 total=0 arms=24`, `met=False`. | A leading-newline anchor, `'\n           and not any(… for e in extras))'`, which matches only the executable guard line (count 1 at all three revisions). Measured with the long anchor: at `4d0f7bf0` the mutant grades `MUTANT count-c1.py M1-met-no-guard survived rc=0`; at `d5e2eda4` it grades `killed rc=1`. The fix turns an ungradeable anchor into a graded one — it does not by itself kill the mutant, which is why the fixture fix above is a separate row. |

### The before/after pair for mistake 1

Before, frozen counter (or landed counter; both print the same line) over the first landing
`4d0f7bf0`:

```text
MUTANT count-c1.py M1-met-no-guard survived rc=0
MUTANT count-c1.py M2-met-drop-empty survived rc=0
MUTANT count-c1.py M3-killed-n killed rc=1
MUTANT count-c1.py M4-arms-total killed rc=1
MUTANT count-c1.py M5-split-field killed rc=1
MUTANT count-c1.py M6-anchor-guard killed rc=1
EXTRA survivor .ufo/waves/round-87/count-c1.py M1-met-no-guard
EXTRA survivor .ufo/waves/round-87/count-c1.py M2-met-drop-empty
C1=unmet mutants=6 killed=4 survivors=2 total=6 arms=24 detector=green rev=4d0f7bf0b0a0
```

After, landed counter over `d5e2eda4`:

```text
MUTANT count-c1.py M1-met-no-guard killed rc=1
MUTANT count-c1.py M2-met-drop-empty killed rc=1
MUTANT count-c1.py M3-killed-n killed rc=1
MUTANT count-c1.py M4-arms-total killed rc=1
MUTANT count-c1.py M5-split-field killed rc=1
MUTANT count-c1.py M6-anchor-guard killed rc=1
C1=met mutants=6 killed=6 survivors=0 total=6 arms=24 rev=d5e2eda49487
```

### Mechanism of mistake 1, measured arm-by-arm

The `met_guard_empty` fixture was driven directly through the r87 counter's own `grade()` — once
with the `4d0f7bf0` fixture body (no tally line) and once with the `d5e2eda4` body — against both
the pristine module and the M1-mutated module (the frozen M1 replacement, guard → `and True`):

| fixture body | module graded | `met` | extras | the arm's verdict |
|---|---|---|---|---|
| `empty.py` = `GUARD = 1` + `FAKE pass=1 fail=0` (the `4d0f7bf0` body) | pristine r87 counter | `False` | `pristine-arms … arms=-1 want=1`, `empty-mutation …` | passes |
| same | M1-mutated r87 counter | `False` (from `pristine-arms`, not from the guard) | same two extras | **passes → M1 survives** |
| `empty.py` + `COUNTER_SELFTEST pass=1 fail=0` (the `d5e2eda4` body) | pristine r87 counter | `False` | `empty-mutation …` | passes |
| same | M1-mutated r87 counter | **`True`** | `empty-mutation …` (present, but the mutation stops it from forcing `met` false) | **fails → M1 killed** |

The third/fourth rows are the whole point: the arm's assertion reads the presence of the
`empty-mutation` extra, which the M1 mutation does not remove — only `met` changes. A fixture whose
pristine copy is not green pins `met` to False independently of the guard, and the arm cannot fail.
The tally line is what makes `pristine_ok` true and lets `met` carry the guard's value.

### Freeze-bound fact observed (reported verbatim, not a mistake row)

The contract's freeze paragraph (`contract.md:99-103`) names this set frozen at `2a5e3ad9`:
`count-c1.py`, `count-c2.py`, the contract and `evidence/controls-r88.txt`, and says: *"No target,
population, fixture or kill rule moves after data."* Measured against that sentence:

- `.ufo/waves/round-88/count-c1.py` moved at `d5e2eda4`: `d1048cf0…`/17850 bytes at the freeze →
  `3ba0f97b…`/17958 bytes after; the diff changes only the counter's own selftest fixtures
  (`dup.py`, `empty.py` tally lines). `.ufo/waves/round-88/count-c2.py` did not move (`8904a3d0…`
  at both revisions).
- The after receipt's `# counter-sha256:` lines bind the moved bytes (`3ba0f97b…` for C1,
  `8904a3d0…` for C2), so the receipt reproduces from `d5e2eda4`, not from the freeze commit.
- Measured effect on the claim's values: none. The frozen counter at `d5e2eda4` prints `C1=met …`
  rc 0 (reading 7), and the landed counter at `4d0f7bf0` still prints `C1=unmet … killed=4
  survivors=2` rc 1 (reading 5). The move created neither the after value nor the before value.

This seat records the hash and the contract sentence for the judge and does not classify it.

## 3. Seat findings merged

<!-- L1: merge the wave's seat findings here. Left empty by this seat by design. No sibling's
report or verdict is restated anywhere in this draft; the only readings in it are the ones listed
in §1, each with its own command and output. The L1 owns the merge and its attribution. -->

## Limits of this seat's work

- **C2 was not run by this seat.** The C2 after line and the fixture lines are quoted from
  `evidence/after-r88.txt`; this seat did not execute `count-c2.py`, did not build a clone fixture
  and did not re-derive `refused=2`.
- **The controls were not rerun.** The entering `C1=…`/`C2=…` values are quoted from
  `evidence/controls-r88.txt` (same bytes as `2a5e3ad9`, hashed above).
- **The pre-fix control run at `1bd5ec3f` left no committed bytes.** What is measured here is the
  mechanism: the short anchor counts 2 at `1bd5ec3f` (reading 8), and a short-anchor grade refuses
  with `occurrences=2` (row 2). The older run itself is not in a receipt and is not claimed as
  this seat's observation.
- **No Gate, SOURCES census, QUALITY criterion, spot-check verdict or SCORECARD edit** was made or
  proposed here.
- **No fixture git repo or commit** was created: no `git init`, no commit identity used. The
  fixture-identity rule was therefore not engaged.
- **Tooling:** none installed or upgraded; no `pacman` transaction was attempted (host-wide pause
  respected), and no file under `~/.local/bin` or any other PATH directory was touched.
- Scratch `/fast/scratch/hyaku/mori-r88/Mo88S01Lesson` was deleted before yield. Nothing was
  written under `/tmp`. The only lane path written is this report.

## Verdict measured and the exact commands

Verdict this seat measured, C1 only: **before `C1=unmet mutants=6 killed=4 survivors=2 …`, after
`C1=met mutants=6 killed=6 survivors=0 …`; the anchor defect is `occurrences=2` and the fixture
defect is reproduced arm-by-arm.** C2: **not measured by this seat** (quoted from the receipt).

`S=/fast/scratch/hyaku/mori-r88/Mo88S01Lesson`; `L=/home/vgpnk/Projects/shokunin/mori-shokunin`.
Counters were extracted from committed bytes, never from the worktree copy:

```bash
git -C $L show 2a5e3ad96deb978ed1fb958e87b4be8221fb23b7:.ufo/waves/round-88/count-c1.py > $S/frozen-c1.py
git -C $L show d5e2eda494877a85edaa4e287d6ad81843d9a8a1:.ufo/waves/round-88/count-c1.py > $S/landed-c1.py
git -C $L show d5e2eda494877a85edaa4e287d6ad81843d9a8a1:.ufo/waves/round-87/count-c1.py > $S/subject-r87-after.py
sha256sum $S/frozen-c1.py $S/landed-c1.py

# readings 1-3
python3 -I $S/frozen-c1.py  --selftest --scratch $S/self-frozen   # C1_COUNTER_SELFTEST pass=25 fail=0, rc 0
python3 -I $S/landed-c1.py  --selftest --scratch $S/self-landed   # C1_COUNTER_SELFTEST pass=25 fail=0, rc 0
python3 -I $S/subject-r87-after.py --selftest --scratch $S/self-subject  # C1_COUNTER_SELFTEST pass=24 fail=0, rc 0

# readings 4-5 (before)
python3 -I $S/frozen-c1.py 4d0f7bf0b0a0d978fa65d9b93edc37a2e6556550 --repo $L --scratch $S/r-before-frozen
#   → C1=unmet mutants=6 killed=4 survivors=2 total=6 arms=24 detector=green rev=4d0f7bf0b0a0  (rc 1)
python3 -I $S/landed-c1.py 4d0f7bf0b0a0d978fa65d9b93edc37a2e6556550 --repo $L --scratch $S/r-before-landed
#   → identical line and rc

# readings 6-7 (after, both instruments)
python3 -I $S/landed-c1.py d5e2eda494877a85edaa4e287d6ad81843d9a8a1 --repo $L --scratch $S/r-after
#   → C1=met mutants=6 killed=6 survivors=0 total=6 arms=24 rev=d5e2eda49487  (rc 0)
python3 -I $S/frozen-c1.py d5e2eda494877a85edaa4e287d6ad81843d9a8a1 --repo $L --scratch $S/r-after-frozen
#   → identical met line, rc 0

# reading 8 (anchor occurrences)
python3 - <<'PY'
import subprocess
short='and not any(e.startswith(("empty-mutation", "unanchored")) for e in extras)'
long='\n           and not any(e.startswith(("empty-mutation", "unanchored")) for e in extras))'
for rev in ("1bd5ec3fa260458f74eb32a2e5bb157209c5934d","4d0f7bf0b0a0d978fa65d9b93edc37a2e6556550","d5e2eda494877a85edaa4e287d6ad81843d9a8a1"):
    src=subprocess.run(["git","-C","/home/vgpnk/Projects/shokunin/mori-shokunin","show",
                        f"{rev}:.ufo/waves/round-87/count-c1.py"],capture_output=True,text=True).stdout
    print(rev[:8], "short:", src.count(short), "long:", src.count(long))
PY
#   → short: 2  long: 1  at all three revisions

# row-2 refusal and long-anchor grading: $S/drive2.py loaded the committed r87 counter with
# importlib and called its own grade():
#   short-anchor grade: met=False tail='mutants=0 killed=0 survivors=0 total=0 arms=24'
#                       extras=['unanchored .ufo/waves/round-87/count-c1.py M1-met-no-guard occurrences=2']
#   long-anchor  grade at 4d0f7bf0: 'MUTANT count-c1.py M1-met-no-guard survived rc=0'
#   long-anchor  grade at d5e2eda4: 'MUTANT count-c1.py M1-met-no-guard killed rc=1'

# row-1 mechanism: $S/drive.py graded the met_guard_empty fixture (no tally / tally) against the
# pristine and M1-mutated modules; observed met=False/False and met=False/True respectively.
```

## Appendix — the two scratch drivers (reproduction copies, seat scratch deleted)

Both were run as `TMPDIR=$S/tD python3 -I $S/drive.py` and
`TMPDIR=$S/tE python3 -I $S/drive2.py`. The copies below are the seat's scratch files with only
unused imports/variables removed; they import the committed r87 counter as a module and call its
own `grade()`, and no fixture git repo or commit was made. The observed output printed above each
copy is the run's verbatim output.

```python
# drive.py — the §2 mechanism table (row 1). Observed:
#   [met_guard_empty fixture=no-tally module=pristine]  met=False extras=['pristine-arms … arms=-1 want=1', 'empty-mutation …']
#   [met_guard_empty fixture=no-tally module=M1-mutated] met=False extras=[same two]
#   [met_guard_empty fixture=tally    module=pristine]  met=False extras=['empty-mutation …']
#   [met_guard_empty fixture=tally    module=M1-mutated] met=True  extras=['empty-mutation …']
import importlib.util, os, subprocess, tempfile
S = "/fast/scratch/hyaku/mori-r88/Mo88S01Lesson"
L = "/home/vgpnk/Projects/shokunin/mori-shokunin"

def git_show(rev, path):
    return subprocess.run(["git","-C",L,"show",f"{rev}:{path}"],
                          capture_output=True, text=True, check=True).stdout

def load(src, name):
    p = os.path.join(S, name + ".py")
    open(p, "w").write(src)
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

BASE_REV = "4d0f7bf0b0a0d978fa65d9b93edc37a2e6556550"
src_before = git_show(BASE_REV, ".ufo/waves/round-87/count-c1.py")
M1_OLD = '\n           and not any(e.startswith(("empty-mutation", "unanchored")) for e in extras))'
M1_NEW = "\n           and True)"
assert src_before.count(M1_OLD) == 1
P = load(src_before, "mod_pristine")
M = load(src_before.replace(M1_OLD, M1_NEW), "mod_m1")

sensitive = ("import sys\nGUARD = 1\n"
             "ok = GUARD == 1\n"
             "print('FAKE pass=%d fail=%d' % (1 if ok else 0, 0 if ok else 1))\n"
             "print('COUNTER_SELFTEST pass=1 fail=0')\n"
             "sys.exit(0 if ok else 1)\n")
for tag, tally in (("no-tally", ""), ("tally", "print('COUNTER_SELFTEST pass=1 fail=0')\n")):
    files = {
        "tools/sensitive.py": sensitive,
        "tools/empty.py": "GUARD = 1\nprint('FAKE pass=1 fail=0')\n" + tally,
    }
    disk = lambda p: files[p]
    arms = {"sensitive.py": 1, "empty.py": 1}
    muts = [("tools/sensitive.py", "r88-kill", "GUARD = 1", "GUARD = 0"),
            ("tools/empty.py", "r88-empty", "GUARD = 1", "GUARD = 1")]
    for mtag, mod in (("pristine", P), ("M1-mutated", M)):
        sc = tempfile.mkdtemp(dir=S, prefix="grade-")
        met, tail, lines, extras = mod.grade(disk, sc, muts, arms)
        print(f"[met_guard_empty fixture={tag} module={mtag}] met={met} tail={tail!r}")
        print(f"   extras={extras}")
```

```python
# drive2.py — the §2 anchor table (row 2). Observed, at each of 4d0f7bf0 and d5e2eda4:
#   rev=… short.count=2 long.count=1
#   short-anchor grade: met=False tail='mutants=0 killed=0 survivors=0 total=0 arms=24'
#                       extras=['unanchored .ufo/waves/round-87/count-c1.py M1-met-no-guard occurrences=2']
#   long-anchor  grade at 4d0f7bf0: lines=['MUTANT count-c1.py M1-met-no-guard survived rc=0']
#   long-anchor  grade at d5e2eda4: lines=['MUTANT count-c1.py M1-met-no-guard killed rc=1']
import importlib.util, os, subprocess, tempfile
S = "/fast/scratch/hyaku/mori-r88/Mo88S01Lesson"
L = "/home/vgpnk/Projects/shokunin/mori-shokunin"

def git_show(rev, path):
    return subprocess.run(["git","-C",L,"show",f"{rev}:{path}"],
                          capture_output=True, text=True, check=True).stdout

def load(src, name):
    p = os.path.join(S, name + ".py"); open(p,"w").write(src)
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

for rev in ("4d0f7bf0b0a0d978fa65d9b93edc37a2e6556550",
            "d5e2eda494877a85edaa4e287d6ad81843d9a8a1"):
    src = git_show(rev, ".ufo/waves/round-87/count-c1.py")
    short = 'and not any(e.startswith(("empty-mutation", "unanchored")) for e in extras)'
    long_ = '\n           and not any(e.startswith(("empty-mutation", "unanchored")) for e in extras))'
    print(f"rev={rev[:8]} short.count={src.count(short)} long.count={src.count(long_)}")
    mod = load(src, "mod_" + rev[:8])
    disk = lambda p, b=src: b
    muts = [(".ufo/waves/round-87/count-c1.py", "M1-met-no-guard", short, "and True)")]
    sc = tempfile.mkdtemp(dir=S, prefix="anchor-")
    met, tail, lines, extras = mod.grade(disk, sc, muts, {"count-c1.py": 24})
    print("  short-anchor grade: met=%s tail=%r extras=%s" % (met, tail, extras))
    muts2 = [(".ufo/waves/round-87/count-c1.py", "M1-met-no-guard", long_, "\n           and True)")]
    sc = tempfile.mkdtemp(dir=S, prefix="anchor-")
    met2, tail2, lines2, extras2 = mod.grade(disk, sc, muts2, {"count-c1.py": 24})
    print("  long-anchor  grade: met=%s tail=%r lines=%s extras=%s" % (met2, tail2, lines2, extras2))
```
