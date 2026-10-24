# mori round 42 — frozen contract (L1 mori-r42, attempt 1)

Entering tip `9de7323de482699743619cfa2ee444e7418421e3` (round 41 closed ADMITTED;
closure `corpus/lessons/round-41-verifier-spotcheck.md`). Lowest non-retired axes:
depth 5, calibration 5, freshness 5 (tied). C2 works calibration (routed defects 1–3),
C3 works depth (routed defect 4), C1 works operability (routed defect 1's survivor
lanes). This file, the three counters and the v4 control receipts are frozen before
any seat runs; pins in `evidence/freeze-r42.txt`.

## Axis claims

| # | claim | axis / score | before (one command over committed bytes) | after (measured at the landed tip) |
|---|---|---|---|---|
| C1 | close the three surviving round-41 mutant lanes: the conform checker gains three selftest arms — `timeout_scope_walrus_positive` (walrus target binds a finite-positive value), `timeout_scope_tupleunpack_positive` (sound element-wise tuple unpack binds a finite-positive value), `timeout_scope_source_order` (DFS-vs-source order divergence pins the first failing-binding reason string) — each killed by exactly its own checker mutation | operability 7 | r41 v4 checker bytes print `CONFORM_SELFTEST pass=14 fail=0` and each of the three committed v41 mutants (walrus-branch deletion, tuple-extraction deletion, sort deletion) survives: `evidence/control-c1-v4.txt` | `python3 .ufo/waves/round-42/count-c1.py <landed tip>` prints `C1=met` exit 0 (`evidence/c1-after.txt`); do-nothing control (v4 bytes) prints `C1=unmet` |
| C2 | report-accuracy errata: the r41 fleet report's three false claims are corrected in append-only lane records naming the superseded text | calibration 5 | `python3 .ufo/waves/round-42/count-c2.py 9de7323d` prints `C2=unmet` exit 1 (`evidence/control-c2-before.txt`) | same counter at the landed tip prints `C2=met` exit 0 (`evidence/c2-after.txt`) |
| C3 | name the inheritance: the 145 files committed unnamed inside `d72ac167` are named by category and provenance in a committed manifest | depth 5 | `python3 .ufo/waves/round-42/count-c3.py 9de7323d` prints `C3=unmet` exit 1 (`evidence/control-c3-before.txt`) | same counter at the landed tip prints `C3=met` exit 0 (`evidence/c3-after.txt`) |

## P-C1 (predicate, same sentence in contract, counter code, receipt label)

At the landed tip, `.ufo/waves/round-42/conform.py` audits the round-41 honest
counter with `CONFORM_SELFTEST pass=17 fail=0` exit 0; each of the three committed
checker mutants at `.ufo/waves/round-42/fixtures/mutants/`
(`conform-mut-walrus-branch.py`, `conform-mut-tuple-extract.py`,
`conform-mut-sort-deletion.py` — each derived from the v5 bytes by the frozen text
transformations below and byte-verified against the pins) prints
`CONFORM_SELFTEST pass=16 fail=1` exit 1 failing exactly
`timeout_scope_walrus_positive`, `timeout_scope_tupleunpack_positive`,
`timeout_scope_source_order` respectively; the routed four verdicts are unchanged
(honest counter `CONFORM=met`; the three round-41 survivors `CONFORM=unmet` with only
`timeout_scope` failing); and the frozen v4 control bytes print `pass=14 fail=0`
with all three v4-derived mutants surviving.

Frozen mutant text transformations (apply exactly once to the checker source; the
counter re-derives and byte-compares against the committed mutant files):

- `walrus-branch`: remove the block
  `        elif isinstance(sub, ast.NamedExpr):\n            if isinstance(sub.target, ast.Name) and sub.target.id == name:\n                add(sub.target, "value", sub.value)\n`
- `tuple-extract`: replace the eight-line element-wise extraction block
  (`    if isinstance(value, (ast.Tuple, ast.List)) \\\n` through the
  `            yield target_name, None, "unresolved destructuring"\n` line under
  `    else:`, i.e. the `if` arm, the `else:` line and its two-line body) with the
  two lines
  `    for target_name in _name_targets(target, name):\n        yield target_name, None, "unresolved destructuring"\n`
- `sort-deletion`: remove the line `    events.sort(key=lambda event: (event[0], event[1]))\n`

C1 no-harm (frozen): the nine static checks keep their round-41 semantics (honest
counter passes all nine; the three survivors fail exactly `timeout_scope`);
`tools/mori-sources-appendonly.py --selftest` prints `pass=22 fail=0` and its lane
line is unchanged from round 41 (36 as-of ids, `stale=[]` at the tip).

## P-C2 (predicate)

At the landed tip, LOG.md's round-42 entry and SCORECARD.md's round-42 declaration
each record the three corrections — (a) the round-41 fleet report's
`8/8 mutants killed` is superseded by `5/8 killed, 3 SURVIVED` naming
`.ufo/waves/round-41/w1/MutC1Walrus.md`, `MutC1Tuple.md`, `MutC1DropSort.md`; (b)
`34 attack seats (53%)` is superseded by `31 attack seats of 64 (48.4%)` under the
spec definition 12 reviewer + 11 critic + 8 mutation-tester (executors are not attack
roles); (c) `2 scouts, 4 scribes` is superseded by `1 scout, 5 scribes` with the
returned total 19 unchanged — and no lane-owned round-42 record re-asserts a
superseded value uncontradicted.

C2 evidence basis (measured at freeze): w1 holds exactly 19 seat-report files
(`Scr*` = 5, `Scout*` = 1, `Exe*` = 3, `Mut*` = 8, `Rev*` = 1, `Connect*` = 1);
w1-spec.json role counts are reviewer 12, critic 11, mutation-tester 8, executor 3,
scribe 7, scout 22, connector 1 (64 total); the three MutC1* reports each contain
`SURVIVED`.

## P-C3 (predicate)

At the landed tip, `corpus/knowledge/inheritance-d72ac16-r42.md` names every path
added unnamed by commit `d72ac167535229d737b9fa844513431d9a12f5ea` — exactly 145
paths in three categories: 67 `.ufo/waves/round-40/w1/*.md` seat reports, 7
`.ufo/waves/round-40/` evidence/scratch files (`evidence/freeze-r40.txt` and the six
`.ufo/waves/round-40/scratch/mutconform-arms2/*` files), and 71 `.scratch/*` files
— each with category and provenance, and the manifest names no path `d72ac16` did
not add. The named-freeze set (20 paths, enumerated in `evidence/freeze-r42.txt`):
15 under `.ufo/waves/round-41/`, `tools/mori-round41-calibration.py`,
`tools/mori-sources-appendonly.py`, `corpus/README.md`, `corpus/SOURCES.md`,
`corpus/knowledge/conform-bindings-r41.md`.

## Kill rules (frozen before data)

- C1: a do-nothing control is the v4 checker bytes — `pass=14`, all three mutants
  survive; any candidate whose honest selftest is not `pass=17 fail=0`, whose mutant
  run fails other or additional arms, or whose routed-four verdicts move, prints
  `C1=unmet`.
- C2: a do-nothing control is the entering tip (no records) — `C2=unmet`; candidate
  records asserting `8/8`, `34 attack`, `53%`, or `2 scouts, 4 scribes` as current
  values, or omitting the superseded-text naming, print `C2=unmet`.
- C3: a do-nothing control is the entering tip (no manifest) — `C3=unmet`; a manifest
  missing any of the 145 paths, or naming a path outside the `d72ac16` addition set,
  prints `C3=unmet`.

## Wave

One v2 wave, 64 seats, attack = reviewer 12 + critic 11 + mutation-tester 8 = 31
(48.4% ≥ 25% band floor), build = scout 12 + scribe 10 + executor 8 + connector 1 +
simplifier 1 + revenger 1 = 33. §3 L2 floor inside the wave; the L1 holds the
canonical planner seat (orchestrator ruling 2026-10-19); a bounded planning data-walk
rides scout/connector items. Per the round-41 routed wave-shape gap (defect 5), at
least three mutation-tester/critic seats attack the C2 and C3 counters directly.
Seat reports under `.ufo/waves/round-42/w1/`; candidate byte files only under
`.ufo/waves/round-42/candidates/<SeatName>/`.
