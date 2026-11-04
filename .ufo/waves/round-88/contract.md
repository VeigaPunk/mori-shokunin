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
