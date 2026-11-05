# Round 90 — mori (L1 MoriR90, resumed attempt) — lesson

Entering revision `d1c8488986512a6a0475af88cc52779ce4703e00` (the commit that preserved attempt
1's in-flight round-90 files after its L1 died on a provider failure; it adds only
`.ufo/waves/round-90/{contract.md,controls-r90.sh,count-c1.py,count-c2.py,w1-spec.json,evidence/}`,
and every graded subject is byte-identical to `037c02ca`). Frozen contract
`.ufo/waves/round-90/contract.md` (two claims, predicates P-C1/P-C2, kill rules and populations),
controls `.ufo/waves/round-90/evidence/controls-r90.txt` committed before any after-value.

## What the round did

- **C1 (operability)** — the round-87 receipt gate gained a subtract-only reachability pre-pass
  (`invocations_visited`) over the recorded command text: AND-OR short circuit from a literal
  status, sequencing after `exit`/`return`, unselected `if`/`elif`/`else` bodies, subshell status,
  `!` negation, loop bodies that cannot iterate, statements after `break`/`continue`, and an
  unmatched literal `case` arm. Landing: `.ufo/waves/round-87/count-c2.py` at `11197820`
  (26 selftest arms unchanged — the r88/r89 `arms=26` pins are therefore not moved). Frozen
  counter: `C1=met branch_open=0 harm=0 newopen=0 open=22 cases=78`, battery
  `branch_cases=14 branch_open=0` (`evidence/after-r90.txt`).
- **C2 (calibration)** — the three round-89 neighbouring survivors are armed: B1
  (`own_ok_arm_count`, a structural pin on `own_ok_of`'s pattern), B4 (`met_line_call_site`, an
  AST pin on the printed line's argument) and B6 (`clone_root_negative`, a structural pin on
  `clone_root_ok`). Landing: `.ufo/waves/round-88/count-c1.py` (29 arms) and
  `.ufo/waves/round-88/count-c2.py` (27 arms, see mistake 1 for the count) at `11197820`.
  Frozen counter: `C2=met mutants=15 killed=15 survivors=0 unattributed=0 unanchored=0
  isolated=0 literal_anchors=0 arms=29,27` (`evidence/after-r90.txt`).
- **Frontier** — S612–S616 admitted (POSIX 2.9.3/2.9.4.4/2.15 opened by seat Mo90S01Sources,
  quotes re-checked by the L1 against the pinned copies), knowledge
  `corpus/knowledge/branch-reachability-r90.md`, QUALITY 190–192.
- Wave: one v1 wave, 13 seats (4 executor, 1 scout, 2 scribe, 2 reviewer, 1 critic,
  1 mutation-tester, 1 connector, 1 sentinel; attack share 5/13). The L1 holds the canonical
  planner seat; the bounded planning data-walk rode `Mo90K01Conn` (cross-round pin map).

## Mistakes

| Class | Evidence pointer | Captured-by | Fix, and what makes it able to fail |
|---|---|---|---|
| `frozen-after-constant-unreachable` — P-C2 froze the after arm counts as `arms=29,27` (one arm added per declared mutant), but B4 and B6 are **both** subjects of `.ufo/waves/round-88/count-c2.py` and the kill rule needs two distinct FAIL labels, so a correct landing there is 26+2 = 28. The frozen `pristine-arms` check makes every kill ungradeable at 28, so the target as written cannot be met by the work it describes. The do-nothing control could not catch it: it grades behaviour, never the reachability of an after-constant. | `.ufo/waves/round-90/contract.md` P-C2 (`arms=29,27`); `count-c2.py:49` `ARMS_BY_FILE`; measured `pristine-arms .ufo/waves/round-88/count-c2.py arms=28 want=27` at the first integrated candidate; seat `w1/Mo90K01Conn.md` §5.1 and `w1/Mo90C01Critic.md` §2 reached the same arithmetic independently | none at freeze | The landing merges the only two mutation-free constant pins (`arms_pinned`: `SUBJECT_ARMS == 26`; `marker_literal`: the `missing-replay` label) into one `frozen_constants` arm that keeps **both** assertions — 26 + 2 − 1 = 27, no declared mutant touches either constant, and no assertion is dropped. Able to fail: the merged arm reds if either constant is edited, and `C2=met … arms=29,27` is only reachable with all fifteen labels isolated (measured; `evidence/after-r90.txt`). QUALITY 190. |
| `behavioural-negative-arm-collides-with-a-blunter-mutant` — the fix as dispatched (a behavioural negative on `own_ok_of`, and one on `clone_root_ok`) is structurally incompatible with two frozen mutants: `C1-own-ok` blunts `own_ok_of` to `return (True or …)` and `C2-clone-top` blunts `clone_root_ok` to `return True`, so each negative arm fails under the other mutant and its kill reads `isolated`, never `killed`. No behavioural assertion can separate "always True" from "prefix rule". | measured `isolated .ufo/waves/round-88/count-c1.py C1-own-ok … fails=own_ok_arm_count,own_ok_red` and `isolated … C2-clone-top … fails=clone_root_negative,clone_top_bound`; seat `w1/Mo90C01Critic.md` §2 | `w1/Mo90E02ArmB1.md`/`w1/Mo90E03ArmsB46.md` received the constraint only after their first pass (L1 measurement) | Three structural pins instead (QUALITY 192), each measured to red exactly its own declared label and to stay green under the blunter mutants. Able to fail: `C2=met` requires every one of the fifteen fail-sets to be exactly one label; the first-pass behavioural arms read `isolated=2`. |
| `class-target-reachable-by-a-lookup-table` — the frozen C1 predicate grades `binding_problems` on recorded text only: it never runs the gate's selftest, never reads an anchor and never checks that the rule generalizes, so a 21-string `frozenset` of the seven distinct frozen branch commands plus the battery's fourteen reaches the frozen met line. The battery's `class` field is the author's word, and battery and rule land in the same revision, so "written by a seat that did not author the rule" is procedural, not enforced. | seat `w1/Mo90C01Critic.md` §1 (measured `C1=met …` at `3c73e6562793` with a lookup wrapper) | none — the counter cannot see rule shape | Disclosed, not repaired: the landing is a general grammar walk, and the round's own harm batteries (`L1`, 48 valid commands) plus the r89 `noharm`/`heldout` batteries were re-run against it (`harm=0`). QUALITY 191 routes the fix to r91: a class claim's guard needs inputs the rule's author cannot read (counter-synthesized commands with a per-run nonce), not a JSON in the same tree. |
| `selftest-orientation-unrecorded` — the inherited round-90 `count-c1.py` was repaired before data (contract A1) because its four synthetic-gate arms passed `deny`/`allow` in the opposite orientation to `bound()`; no committed artefact holds the red reading, so the pre-repair failure is reconstructible only: swapping the two gate bodies reads `C1_COUNTER_SELFTEST pass=6 fail=6`. | `.ufo/waves/round-90/contract.md:65-71` (A1); `w1/Mo90S02Lesson.md` §Seat findings; `controls-r90.txt` §4 (`pass=12 fail=0`) | A1 states the rule (a counter's own selftest must be green before it grades) but no committed bytes preserve the failing state | The post-repair selftest is committed and green in both the controls and the after receipt; the reconstruction command is recorded here so the claim is checkable. Able to fail: the swapped orientation reds six arms by construction. |

## Gate

Sources admitted this round (access date 2026-11-05 for every row; every row `mined`, `recheck 90d`):

| Row | URL | Located quote (≤25 words) | Decision |
|---|---|---|---|
| S612 | https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html | "shall have equal precedence and shall be evaluated with left associativity" | admit — grounds the AND-OR short-circuit clause |
| S613 | https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html | "the exit status of the then or else compound-list that was executed, or zero, if none was executed" | admit — grounds the unselected if body |
| S614 | https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html | "The exit utility shall cause the shell to exit from its current execution environment" | admit — grounds sequencing after `exit` |
| S615 | https://docs.python.org/3/library/ast.html | "Recursively yield all descendant nodes in the tree starting at node (including node itself), in no specified order." | admit — grounds walk-order-independent pins |
| S616 | https://docs.python.org/3/library/tokenize.html | "The scanner in this module returns comments as tokens as well" | admit — grounds reading the token stream |

Rejected this round: `https://pubs.opengroup.org/onlinepubs/9799919799/utilities/exit.html` — the
fetch returned an HTTP 200 script-redirect page (6580 bytes) with no specification text, so no
quote could be located; flip condition: fetch a copy of the utilities page that carries §2.15 text
and locate the `exit` DESCRIPTION sentence there (the chap02 copy S614 uses already does).

Rows S612–S614 share S611's URL; the census records them as W04 (same URL across scopes), which is
a warning, not an error — the scopes are different sections of one specification page.

No existing row's `status`/`recheck`/`used-by` changed. Sourced claim: C1 rests on S612–S614 (the
rule and its three frozen classes) and C2's structural pins on S615; the knowledge entry cites them.

## Assimilation

None. `merge/mori/` was not taken this round (the claims are instrument repairs under the frozen
contract). `considerthese/2026-10-26.md` proposal 1 ("split pin-check mismatches into
environmental and stale") was read and does not fit either claim, so nothing is mined from it this
round; the status line for the 2026-10-25 proposals is unchanged.

## Limits of this round

- The critic measured that a lookup table reaches P-C1's line; the landing is not a lookup, but the
  frozen predicate cannot prove it. Stated in the report's discernment verdict.
- Items 5–8 of the knowledge entry (`!`, loop bodies, `break`, `case`) are [INFERENCE]: no opened
  source states them; the held-out battery is their only ground.
- The r88-c2 `SUBJECT_ARMS = 26` / `TARGET … arms=26` pins are now **stale statements** about the
  round-87 gate only if the gate's arm count moves. It did not move (26 before and after), so they
  remain true; the r89 counters' `28/26` pins on the r88 subjects are superseded by this landing
  and are named, never rewritten.
