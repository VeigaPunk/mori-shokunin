# Mo89C02Critic — residual critic (replaces Mo89C01Critic): reach the C1 / noharm / C2 targets without the claimed work

Seat: Mo89C02Critic · round 89 attempt 1 residual · judged on calibration, operability.
Instruments (lane bytes, unchanged d4438695 → tip; `git diff --quiet d4438695 HEAD` on both counters rc 0):
- `count-c1.py` sha256 `f8e6c39ed30acffd0e6f5272575df3ce7333c7a403b611a4bd1118aac16d9376`
- `count-c2.py` sha256 `40eacccc89bd3b394a6ffb0d6a5fd604143c41ec4375d8a4399e749b65420a3c`
- `noharm-c1.py` sha256 `3b8c7b14fe0d8099de0865235b6ae0c5f981e8189050c41cc1bc2922426d7c7d`

Revisions measured: subject positive control `9f4d20b9290faff54354d6ab6b08982d98d5e72c`; do-nothing `30a29797012281b9fd0c748b38b929ac67f8c754`; C1 first landing `760428abf925d98025b34bf23f2cbf54cbeb3bca`; C2 landing `7ce712d4e0fd295d812fc3047ceeb114c3c2a58c`. The lane tip moved to `bb50c332fad4667c8e76d4379ad8ae76ca1bb09b` during the run; `git diff --stat 9f4d20b9 bb50c332 -- .ufo/waves/round-87/count-c2.py .ufo/waves/round-88 .ufo/waves/round-89/count-c{1,2}.py .ufo/waves/round-89/noharm-c1.py` is empty, so every subject result at 9f4d20b9 holds byte-for-byte at bb50c332 [the counters were not rerun at bb50c332 itself].

Method: one `git clone --shared` of the lane at `/fast/scratch/hyaku/mori-r89/Mo89C02Critic/clone` (`rev-parse --show-toplevel` asserted equal before any commit), forgery commits only through `git -C <clone>` (driver `forge.py`), then the **lane's frozen counters** run `python3 -I <lane>/.ufo/waves/round-89/<counter> <rev> --repo <clone> [--scratch <own dir>]` with TMPDIR set per run. Forgery patches, drivers and every stdout are in `Mo89C02Critic-evidence/`. No lane, corpus or production write; no tool installed.

## Results table (all rc and lines copied from the evidence files)

| run | revision | rc | summary line |
|---|---|---|---|
| count-c1 positive control | 9f4d20b9 | 0 | `C1=met equiv=accepted comment=refused selfprint=refused real=met arms=26` |
| count-c1 do-nothing (d) | 30a29797 | 1 | `C1=unmet equiv=refused comment=accepted selfprint=accepted real=met arms=23 subject=arms:(23, 0)` |
| count-c1 forge-a1 (`./`→bind, `#`/`print(`→refuse) | d0047219 | **0** | `C1=met … arms=26` |
| count-c1 forge-a2 (six literal strings special-cased) | 35f42d92 | **0** | `C1=met … arms=26` |
| count-c1 forge-b (battery lookup table, else bind) | 4fa06653 | **0** | `C1=met … arms=26` |
| noharm positive control | 9f4d20b9 | 0 | `NOHARM harm=0 open=0 gained=3 cases=34` |
| noharm 760428ab | 760428ab | 1 | `NOHARM harm=13 open=6 gained=2 cases=34` |
| noharm do-nothing | 30a29797 | 1 | `NOHARM harm=0 open=11 gained=0 cases=34` |
| noharm forge-a1 | d0047219 | 1 | `NOHARM harm=2 open=4 gained=3` (caught) |
| noharm forge-a2 | 35f42d92 | 1 | `NOHARM harm=0 open=9 gained=1` (caught) |
| noharm forge-b | 4fa06653 | **0** | `NOHARM harm=0 open=0 gained=3` (**passes, same line as the real repair**) |
| count-c2 positive control | 9f4d20b9 | 0 | `C2=met mutants=12 killed=12 survivors=0 unattributed=0 unanchored=0 arms=28,26` |
| count-c2 do-nothing (d) | 30a29797 | 1 | `C2=unmet mutants=7 killed=0 survivors=7 unattributed=0 unanchored=5 arms=25,17` |
| count-c2 forge-c1 (canary on 7ce712d4 subjects) | 7c001f07 | **0** | `C2=met … killed=12 … arms=28,26` |
| count-c2 forge-c2 (entering subjects, pad_NN arms, dead anchors, canary) | 27d85a30 | 1 | `C2=unmet … killed=0 … unattributed=12` (blocked) |
| count-c2 forge-c2b (same, pad arms *named* by the declared arms) | 169482fb | **0** | `C2=met mutants=12 killed=12 survivors=0 unattributed=0 unanchored=0 arms=28,26` |
| count-c2 `grade()` syntax-error mutant probe | 9f4d20b9 r88 count-c1.py | — | `mutants=1 killed=0 unattributed=1` (blocked) |

## (a) C1 forgery — reaches target (assurance gap)
forge-a1 is the **entering** gate (30a29797 bytes, the r88 substring rule, no parser) plus the three r89 selftest arms copied verbatim and a 4-line `binding_problems`: any cmd containing `./` binds; any `#` or `print(` refuses; else the substring rule. count-c1 prints `C1=met … arms=26` rc 0 — the real population still grades `C2=met receipts=7 … bound=9`. forge-a2 (literal special-casing of the three frozen fixture strings + the three arm strings, nothing else changed) also reaches `C1=met`. **count-c1 cannot tell a binding rule from a lookup of its own six strings** — it is a 3-fixture + 3-arm instrument. noharm-c1 **does** catch both (a1 `harm=2 open=4`, a2 `open=9`), so the pair count-c1+noharm blocks these two; count-c1 alone does not. Classification: reaches target for count-c1 (assurance gap); blocked by the noharm battery.

## (b) noharm forgery — reaches target (fixed battery is overfittable)
forge-b = entering gate + r89 arms + `binding_problems` that is a dict of the 34 battery commands (+ six fixture/arm strings + the r88 arm string) and **binds every other command**. Result: `NOHARM harm=0 open=0 gained=3` rc 0 — identical line to the real repair — and `C1=met` rc 0. One forger, 40 table entries, no parsing. On my 23-case held-out set (`heldout-all.txt`) forge-b leaves **13/13 counterfeits open** (e.g. `echo ./tools/mori-record-sweep.py`, `printf … # ./tools/…`). Plainly: the noharm battery is fixed and public, so `harm=0 open=0` certifies only "agrees on 34 strings", not the rule; quantified at 1 forger / 40 entries / 0 detection. It also counts a `met` case refused by both gates as `refused-both`, not harm (forge-a2 shows E05/E12 so classified). Classification: reaches target (assurance gap, both C1 instruments together).

## The real repair under the held-out set — in-claim counterexample (C1 harmed/partial)
Same harness as noharm (`probe.py`, gate loaded via `git show <rev>:.ufo/waves/round-87/count-c2.py`), cases **not** in the battery:
- 9f4d20b9 `HELDOUT open=5 harm=1 cases=23`; 760428ab `open=2 harm=5`; 30a29797 `open=10 harm=0`.
- The repair **binds commands that never execute the script** — and 760428ab refused three of them (regression vs the first landing that noharm does not see):
  - `true || python3 -I tools/mori-record-sweep.py …; printf '%s\n' '<BODY>'` (9f4d20b9 bound; 760428ab refused)
  - `false && python3 -I tools/mori-record-sweep.py …; printf …` (bound; 760428ab refused)
  - `(exit 1) && python3 -I tools/… …; printf …` (bound; 760428ab refused)
  - `printf '<BODY>'; exit 0; python3 -I tools/… …` (bound by all three gates)
- New harm vs entering: `(cd . && python3 -I tools/mori-record-sweep.py …)` — a valid equivalent replay — **refused** by 9f4d20b9 (and 760428ab); entering bound it.
- **End-to-end** (`e2e.py`: the frozen count-c1 `clone_fixture`/`run_graded` with these `# cmd:` lines committed into `record-sweep-r87.txt` in a --shared clone, graded by the gate at 9f4d20b9): H01 `||`, H02 `false &&`, H03 `exit` each grade **`RECEIPT … met problems=-`** with the whole population `C2=met … bound=9`; M07 subshell grades `failed problems=cmd-binding`. At 760428ab H01/H02 grade `failed problems=cmd-binding`. So the binding rule as landed lets a receipt whose body comes from `printf` pass, while naming the script only in a non-executing branch — exactly the C1 counterfeit class ("executed script"), reached by a seat with no special access.
- Out of claim (provenance, not execution): `python3 -I tools/… >/dev/null; printf '<BODY>'` binds and grades met at every revision — the script runs but the body is not its output. The binding claim does not cover body provenance; recorded, not scored.

## (c) C2 forgery — reaches target (assurance gap); two variants blocked
- **Checksum canary, claimed-work subjects (forge-c1)**: 7ce712d4 r88 `count-c1.py`/`count-c2.py` + a 5-line block before the tally: hash own source (minus the `CANARY_SHA` lines), and on mismatch mark **every** arm `FAIL`. count-c2: `killed=12` rc 0. The kill is attributed by label only; the canary makes any edit anywhere "kill" every declared arm.
- **No claimed work (forge-c2b)**: the **entering** 30a29797 r88 subjects (arms 25,17; five anchors absent) + the five missing anchors pasted as dead raw strings (`_DEAD_NN = r'''…'''`) + 3/9 pad arms `cases.append(("<declared arm>", True, "pad"))` + the canary. count-c2 prints `C2=met mutants=12 killed=12 survivors=0 unattributed=0 unanchored=0 arms=28,26` rc 0 (`count-c2-forge-c2b.txt`). Every declared arm is a no-op `True`; five of twelve mutants mutate a string literal. The frozen kill rule (`(rc≠0 ∨ fail>0) ∧ FAIL <declared arm>`) checks the label, not that the labelled arm exercises the mutated behaviour, and the anchor check (`count==1`) does not require the anchor to be live code.
- Blocked: forge-c2 (same with arms named `pad_NN`) → `unattributed=12` rc 1 — the label check catches a canary that cannot name the declared arms. A syntax-error mutant (`count-c2.grade()` on the 9f4d20b9 r88 count-c1.py, anchor + ` ((`) → `unattributed=1 killed=0` — syntax-error "kills" are not counted.
Classification: canary-with-labels reaches target (assurance gap); label-less canary and syntax-error kills blocked by instrument.

## (d) do-nothing control — unmet (confirmed)
30a29797: count-c1 rc 1 `C1=unmet … arms=23`; count-c2 rc 1 `C2=unmet mutants=7 killed=0 survivors=7 unanchored=5 arms=25,17`; noharm rc 1 `open=11`.

## Impacted axes and smallest safe corrections
- **operability (C1)**: the landed rule binds non-executing branches (`||`, `false &&`, `(exit 1) &&`, `exit` before) and refuses a valid subshell; it regressed three counterfeits vs 760428ab. Smallest fix in the subject: treat an invocation after `||`, after a statically-false `&&` left side, or after `exit`, as not executed — simplest sound form: bind only invocations reachable by an unconditional `;`/`&&`-from-start chain whose earlier members are allow-listed (`cd`, `env`, assignments) and refuse `||`/`exit`/`(exit …)`; and descend into `( … )` subshells. Add the four H-counterfeits and M07 as arms and as noharm cases.
- **calibration (instruments)**: count-c1 and noharm are fixed public string sets — a lookup table passes both (forge-b). Smallest correction: a **held-out** noharm battery generated at grading time (e.g. the H/M cases here plus randomized wrapper/flag/position compositions of the bound path) that the subject author cannot see before scoring. count-c2: require each declared arm to be **green on the pristine and red only on its own mutant** while staying green on the other eleven mutants (a canary turns all arms red on every mutant and fails this), and require each anchor to lie outside string literals (`ast`/`tokenize` check). These are instrument changes for a future contract — not admissible as post-freeze edits to this round's counters.

Classifications: (a) a1/a2 reach count-c1 target, blocked by noharm · (b) forge-b reaches both C1 targets — assurance gap · (c) forge-c1, forge-c2b reach C2 target — assurance gap; forge-c2 (unlabelled) and syntax-error blocked by instrument · (d) unmet, as frozen · held-out: real repair harmed (5 open, 1 harm; 3 regressions vs 760428ab; e2e met on 3 counterfeits).

Commands (rc in evidence headers): `TMPDIR=<scratch>/tmp python3 -I forge.py a1 a2 b c1 c2` and `… c2 labeled` (rc 0); per-run `python3 -I <lane>/.ufo/waves/round-89/{count-c1,count-c2,noharm-c1}.py <rev> --repo <clone> [--scratch …]`; `python3 -I probe.py <clone> <revs…>`; `python3 -I e2e.py <clone> <rev>`. Forgery patch sha256 prefixes: a1 769bf66d, a2 f1d9c54e, b b8f7883f, c1 cf2b6ae7, c2 286b62bd, c2b aaf12e65. Scratch removed before yield.

VERDICT Mo89C02Critic C1 harmed
VERDICT Mo89C02Critic C2 partial
