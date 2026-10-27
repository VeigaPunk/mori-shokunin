# Mo52MutC1Controls — round 52 w1 mutation-tester seat

Seat: `Mo52MutC1Controls` (leaf; no subagents). Lane: `mori-shokunin`.
Task: name, for each C1 arm and sub-rule, the control whose verdict would change if that rule were removed; list the rules no control isolates; demonstrate 3 mutants by running mutated counter copies against the witness control commit rebuilt in scratch with `controls/c1-data.py`.
Run: 2026-10-26. Environment: python 3.14.8, git 2.56.0, tar (GNU) 1.35; disk-guard status OK (610G free on /fast, no ENOSPC). Tool installs: none needed, none performed (RULES.md read).
Scratch: `/fast/scratch/hyaku/mori-r52/Mo52MutC1Controls/` (removed after this report; every cited output is copied inline below).

## 1. Rebuilt control commits (witness and the six others)

Recipe mirrors `controls/c1-controls.py` but writes receipts only under scratch (the frozen c1-controls.py writes into the lane's `evidence/`, which this seat must not do). One clone per seat: `git clone -q --no-local <lane> $S/clone-c1`; toplevel asserted before first commit; per control `git checkout -q --detach` at entering tip `E=4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d`, apply parts with `TMPDIR=$S/tmp`, `git add -A`, commit as `mori-control <control@mori.invalid>`.

| control | parts (c1-data.py) | rebuilt commit |
|---|---|---|
| do-nothing | — | E |
| axes-only | axes,locator | 6f2dcea06eccc2d46fde3fee88c0ac7c911ccce4 |
| receipts-only | receipts | 732e0e892f544c9706aefb9fb14a9635d3f58091 |
| living-only | living | 7175ce88ce0050a5632b667647f1fe850125307a |
| rewrite-in-place | axes,locator,receipts,rewrite | e09b7e1797d113019be8e68069512d5d6620541a |
| delete-stale-pins | axes,locator,receipts,delete | 4bb39a7f836736d16a675e882691767af9ebcf0a |
| repeat-stale-tally | axes,locator,receipts,repeat | c25220ae31e0faa94d810b600693df43e73bea51 |
| witness | axes,locator,receipts,living | 6d3878af9ace6acffd8c10b5d914323f136f52c6 |

Baseline: frozen counter run on each rebuilt control (`$ python3 .ufo/waves/round-52/count-c1.py <rev> --repo $S/clone-c1 --fleet-repo /home/vgpnk/Projects/shokunin --scratch $S/base/c1-<name>`). All eight receipts reproduce `evidence/control-c1-*.txt` byte-for-byte on item lines and the `C1=` line (modulo `rev=` hash, which differs because the rebuilt commits are new); exit codes match (do-nothing/axes-only/receipts-only/living-only/rewrite/delete/repeat exit 1, witness exit 0). Pristine selftest: `C1_SELFTEST pass=42 fail=0`, exit 0.

## 2. Mutants (single behavior-bearing point each)

Copies of the frozen counter in scratch, then one deletion each (all `py_compile` clean):

| mutant | rule removed | exact deletion (count-c1.py line refs) |
|---|---|---|
| M1 A4 | `(A)` Last-change cell's first `round N` equals N* | `check_axes`: `if got_n != n: problems.append("round=%s" % got_n)` (lines 201-202) |
| M2 B7 | `(B)` receipt `selftests/<stem>.txt` at R holds the observed line | `check_pins`: `elif not has_receipt: items.append(("pin", …, " receipt_missing", …))` (lines 284-285) |
| M3 C5 | `(C)` a later line carrying `supersedes` + the stale span-and-tally verbatim supersedes it | `superseded()`: second loop `for l in lines[line_no:]: if "supersedes" in l and span in l: return True` (lines 316-318) |
| M4 C2 | `(C)` every pin present at entering tip E stays present byte-for-byte at R | `check_living`: `for _, _, span, _ in living_pins(old): if span not in text: items.append(… "pin_removed_or_rewritten" …)` (lines 331-333) |

Selftest deltas of the same frozen suite (exit codes recorded): M1 `C1_SELFTEST pass=41 fail=1` (stale_round_unmet flips), M2 `pass=41 fail=1` (receipt_missing_unmet flips), M3 `pass=33 fail=9` (readme_fix supersession checks flip), M4 `pass=40 fail=2` (living_rewritten_in_place_unmet, living_pin_deleted_unmet flip). The counter's own selftest therefore does exercise each of these four rules even where the controls do not.

## 3. Mutant × control matrix (sequential rerun, confirmed against rebuilt baselines)

Verdict per cell: **S** = receipt unchanged (mutant survived; no control isolates the rule). **K** = receipt changed (the control isolates the rule); **K→met** / **K→unmet** = changed with exit-code flip.

| control | M1 (A4) | M2 (B7) | M3 (C5) | M4 (C2) |
|---|---|---|---|---|
| do-nothing (E) | K | K | S | S |
| axes-only | S | K | S | S |
| receipts-only | K | S | S | S |
| living-only | K | K | K | S |
| rewrite-in-place | S | S | S | K→met |
| delete-stale-pins | S | S | S | K→met |
| repeat-stale-tally | S | S | K | S |
| witness | S | S | K→unmet | S |

Details: M1 changes only item text on do-nothing/receipts-only/living-only (operability/depth axis lines lose `round=47`/`round=50`, state stays mismatch via `evidence_missing`; exit unchanged). M2 flips the two SHONEN pins from `receipt_missing` mismatch to ok on do-nothing/axes-only/living-only. M3 reverts README:607/608 from `superseded` to live pins (`unrunnable` and tally mismatch) on living-only/repeat/witness; only witness flips exit (met→unmet). M4 removes the three `pin_removed_or_rewritten` items on rewrite-in-place and delete-stale-pins; both flip exit to `C1=met`.

Survival counts: M1 5/8, M2 5/8, M3 5/8, M4 6/8 — 21 of 32 cells (66%) kept the control verdict, the round-51 closure's class ("single-arm mutants keep every control verdict") is reproduced.

## 4. Arm / sub-rule → isolating control

Legend: weak = receipt text changes but no exit flip; strong = exit flips; analysis = derived from the control receipts + manifest, not run as a mutant (listed separately).

**Arm A (axes)**
| sub-rule | controls whose verdict/reading changes if removed | isolation |
|---|---|---|
| A1 exactly one `## Axes` heading outside fences | none | no control isolates |
| A2 exactly one row per axis | none | no control isolates |
| A3 four cells per row | none | no control isolates |
| A4 Last-change first `round N` == N* | do-nothing, receipts-only, living-only | weak (M1) |
| A5 verdict word as whole word in `round N`…`;` segment | none | no control isolates |
| A6 Evidence cell names spotcheck if exists at R else MANIFEST.json | do-nothing, receipts-only, living-only | weak (analysis) |
| A7 Score cell == newest closure's per-axis score | none | no control isolates |
| A8 only `admitted` rounds count | none (no higher non-admitted round ≤51 would win an axis in MANIFEST.json @ f0b61b4…) | no control isolates |
| A9 round ≤ THROUGH=51 cutoff | none (mori rounds in manifest end at 51) | no control isolates |
| A10 lane == mori filter | all controls (removing admits other lanes' same-named axes up to round 108; every axis row mismatches; witness flips) | strong (analysis; incidental to manifest content) |
| A11 grading `improved`/`harmed` | none (all six targets are `improved`) | no control isolates |

**Arm B (shonen)**
| sub-rule | controls whose verdict/reading changes if removed | isolation |
|---|---|---|
| B1 ≥4 boxes floor | none (boxes=4 on all controls) | no control isolates |
| B2 ≥2 pins floor | none (pins=2 everywhere) | no control isolates |
| B3 pin backtick form `(N/M)` or → `PREFIX pass=N fail=M` | none | no control isolates |
| B4 path bound `python3 <repo-relative>.py --selftest` | none | no control isolates |
| B5 path regular file at R (100644/100755, not symlink) | none | no control isolates |
| B6 run at R; last `PREFIX pass=P fail=F` line gives pinned numbers | none | no control isolates |
| B7 receipt at `selftests/<stem>.txt` holds observed line | do-nothing, axes-only, living-only | weak (M2) |
| B8 no other tally token in SHONEN.md | none (hidden=0 everywhere) | no control isolates |

**Arm C (living)**
| sub-rule | controls whose verdict/reading changes if removed | isolation |
|---|---|---|
| C1 single-line pins enumerated (LPIN) | all controls (arm-level; count changes) | arm-level |
| C2 entering-tip pins preserved byte-for-byte | rewrite-in-place, delete-stale-pins | strong (M4; both → met) |
| C3 good pin: argv parses, path regular, rc=0, tally+prefix match | do-nothing, axes-only, receipts-only, repeat-stale-tally | strong on repeat (→ met; analysis), weak elsewhere |
| C4 QUALITY later numbered criterion `supersedes N's check` | all controls (QUALITY:885 ceases to be superseded everywhere; sup count drops) | weak (analysis) |
| C5 later line `supersedes` + stale span verbatim | living-only, repeat-stale-tally, witness | strong on witness (M3; met→unmet) |
| C6 quoted stale pin skipped next to its same-line replacement | living-only, witness, repeat (living/sup counts rise) | weak (analysis) |

**Arm D (locators)**
| sub-rule | controls whose verdict/reading changes if removed | isolation |
|---|---|---|
| D1 every backticked `path:N[-M]` enumerated | all controls (arm-level) | arm-level |
| D2 path exists at R | none | no control isolates |
| D3 bounds a≥1, b≤len(lines) | none | no control isolates |
| D4 quoted string (ws-collapsed) occurs in N..M | all controls (two quote items change text on every receipt) | weak (analysis) |
| D5 `proposed A → B` occurs in N..M | all controls (SCORECARD:1771/1781 pair item changes on every receipt) | weak (analysis) |
| D6 range-only default ok | all controls (plain-range items vanish) | arm-level |

**Infra**: `lane_writes`, `hidden`, floors, `axes` count, manifest tag — none fires on any control; removing any of them changes no control reading. No control isolates them (the selftest covers lane_writes/hidden/floors/axes count).

## 5. Rules no control isolates (coverage gaps)

A1, A2, A3, A5, A7, A8, A9, A11, B1, B2, B3, B4, B5, B6, B8, D2, D3, and the infra gates. For these, the controls are arm-level probes: they only prove the arm can fail (do-nothing) and that the data fixes it (witness), not that the individual rule is live. The rules the controls DO isolate: A4, A6 (weak), A10 (incidental), B7 (weak), C2 (strong), C3 (strong on repeat), C4 (weak), C5 (strong on witness), C6 (weak), D4, D5 (weak). Demonstrated by runs: A4, B7, C5, C2.

## 6. Evidence note: parallel runs contaminate the conform pin

First (parallel, `xargs -P 4`) matrix run made the README:607 conform pin return `got=no_tally_rc=2` on rewrite-in-place for all four mutants, while sequential reruns reproduce the frozen `CONFORM_SELFTEST_pass=9_fail=0_rc=0`. Cause: the living-arm tool `corpus/…/.ufo/waves/round-39/conform.py` hardcodes `LANE` (line 53) and writes its selftest mutation counters into the real lane's `.ufo/waves/round-39/scratch/`; concurrent counter invocations make it intermittently exit 2. See Findings.

## 7. Commands (literal; receipts per round-52 rule)

- Control build: `git clone -q --no-local /home/vgpnk/Projects/shokunin/mori-shokunin $S/clone-c1`; per control `git -C $S/clone-c1 reset -q --hard 4f266ef2… && TMPDIR=$S/tmp python3 <lane>/.ufo/waves/round-52/controls/c1-data.py $S/clone-c1 <parts> && git -C $S/clone-c1 add -A && git -C $S/clone-c1 -c user.name=mori-control -c user.email=control@mori.invalid commit -q -m "control <name>"`.
- Baselines: `python3 <lane>/.ufo/waves/round-52/count-c1.py <rev> --repo $S/clone-c1 --fleet-repo /home/vgpnk/Projects/shokunin --scratch $S/base/c1-<name>`.
- Mutants: `python3 $S/mutants/count-c1.<M>.py <rev> --repo $S/clone-c1 --fleet-repo /home/vgpnk/Projects/shokunin --scratch $S/out/c1-<M>-<name>`.
- Selftests: `python3 <counter> --selftest` (pristine pass=42 fail=0; mutants as in §2).

## Findings

- **HIGH** — `corpus/…/.ufo/waves/round-39/conform.py:53-54` (hardcoded `LANE`/`SCRATCH_ROOT`) makes the C1 living arm write into the real lane: every run that reaches the README conform pin creates untracked files under `.ufo/waves/round-39/scratch/mori-conform-selftest-*/counter-*.py` in `/home/vgpnk/Projects/shokunin/mori-shokunin` (observed in `git status --porcelain --ignored`; files created at run times 21:31-21:32). `lane_writes` does not see them because the counter runs `git status` on `--repo` (a clone here), not on the real lane. Detection/report only; routed.
- **MED** — under 4-way concurrent counter invocations the conform pin intermittently returns rc=2 / no tally (`no_tally_rc=2`), flipping README:607 to mismatch on good data; sequential runs are stable. C1 results from parallel waves may contain false conform-pin mismatches.
- **LOW** — the control suite gives no rule-level isolation for A1-A3, A5, A7-A9, A11, B1-B6, B8, D2-D3 and the infra gates; the witness control alone isolates C5 among the demonstrated mutants. The frozen selftest does cover these rules (42 checks) — routed: round-53 controls should target A4/A6/B7/C2/C3/C5/D4/D5 (isolated) or rely on the selftest for the rest.
- **LOW** — M4 (C2, append-only preservation) is isolated by rewrite-in-place and delete-stale-pins only; both flip to `C1=met` when the rule is removed, i.e. the two controls exist solely to detect in-place/rewrite rewriting of the stale pins.
