# Round 80 — frozen contract (mori L1 MoriR80)

entering revision: `d58889220d3c6a18d461f2d31b5ab162ffef1e4e` (branch `master`, pushed, clean)
date: 2026-11-04
axes owned: coverage + operability; all six scored. Lowest non-retired axes at entering:
depth 5, freshness 5, calibration 5.

This file is frozen before the wave and before any data. The predicate, the counter and the
receipt label are the same sentence in all three places. A rule changed after a seat scored is
not the claim's rule.

## Claims (3)

| # | Claim (one sentence) | Axis | Type |
|---|---|---|---|
| C1 | `tools/mori-claim-sweep.py` lands and resolves the lane's self-assessment claims against committed bytes, taking the mismatch count from 1 to 0. | calibration | capability acquisition + calibration |
| C2 | `.ufo/waves/round-79/count-c2.py` carries one selftest arm per surviving mutant the round-79 mutation seat reported, so the frozen six-mutant harness kills 6 of 6 (from 3 of 6). | operability | operability (sourced: S595) |
| C3 | `PROVINCE.md` names every committed `tools/*.py|*.sh` instrument with its class and registry row, taking named instruments from 15 of 55 to 55 of 55. | coverage | coverage |

Distinct axes, causally separable: each after-state is re-derivable by one command over
committed bytes with the other two claims unlanded (C1's counter needs only the sweep tool and
the corrected SCORECARD row; C2's harness needs only count-c2.py's selftest; C3's counter needs
only PROVINCE.md).

### P-C1 (frozen predicate, calibration)

> At revision R, `tools/mori-claim-sweep.py` exists at R and, run with
> `--root <export of R> --pins .ufo/waves/round-80/claim-pins.json`, prints
> `CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0` and exits 0; the same sweep at the
> entering revision `d5888922` finds at least one mismatch, the named one being
> `SCORECARD.md`'s control-receipt capability row stating `18` while the committed
> `tools/mori-control-receipt.py --selftest` prints `pass=19 fail=0`.

Counter: `.ufo/waves/round-80/count-c1.py <rev>` → `C1=met|unmet …`, rc 0 met / 1 unmet / 2 setup.
Kill rule: any mismatch, a missing tool blob, or a sweep exit != 0 at R is `C1=unmet`.

### P-C2 (frozen predicate, operability; sourced by S595)

> At revision R, `.ufo/waves/round-80/mutate-c2.py --rev R` applies its six frozen mutants one
> at a time to a scratch copy of `.ufo/waves/round-79/count-c2.py` as it stands at R and runs
> `--selftest` after each; it prints `MUTATION_C2 survivors=0 killed=6 total=6` and exits 0.
> At the entering revision the same harness prints `survivors=2 killed=4 total=6` (measured at
> `d5888922` before this round: `drop_admitted` and `cut_clause_boundary` survive; the round-79
> mutation seat named three survivors and this harness's frozen six-mutant set is the one that
> grades).

Counter: `.ufo/waves/round-80/mutate-c2.py --rev <rev>` → `MUTATION_C2 survivors=S killed=K total=6`.
Kill rule: one surviving mutant, a harness setup failure, or a counter whose selftest is not red
under a mutant is `C2=unmet`. Grade is the selftest verdict only (declared; not a claim that the
predicate changed).

### P-C3 (frozen predicate, coverage)

> At revision R, the set of `tools/*.py` and `tools/*.sh` basenames named in `PROVINCE.md`
> contains every path that `git ls-tree -r --name-only R -- tools/` reports with that shape, and
> every named path exists at R; the counter prints `C3=met named=N present=M missing=0` and
> exits 0. At the entering revision it prints `C3=unmet named=14 present=55 missing=41 extra=0`
> rc 1 (measured at `d5888922`; a sibling lane's `tools/...` path named in PROVINCE is not a
> lane instrument and is excluded).

Counter: `.ufo/waves/round-80/count-c3.py <rev>` → `C3=met|unmet named=N present=M missing=K`.
Kill rule: any missing instrument, or a named path that does not exist at R, is `C3=unmet`.
`extra` (a named path absent from the tree) is a mismatch too: it must be 0.

## Do-nothing control (cheapest control that skips the claimed work)

`.ufo/waves/round-80/evidence/controls-r80.txt`, written before the wave, holds one section per
claim: at `d5888922` the sweep tool blob is absent (`git cat-file -e` rc 128); the harness at
`d5888922` reports `survivors=2`; `count-c3.py d5888922` reports `C3=unmet named=14 present=55
missing=41 extra=0`; and the SCORECARD row's `18` disagrees with the live `19`. Every claimed
after-state is absent at entering, so a do-nothing round cannot reach any target. The receipt
obeys the r79 control-receipt rule: every section that states a `key=<integer>` also carries the
`$ command` that produced it.

## Deliverables per claim

C1: `tools/mori-claim-sweep.py` (single file, stdlib, `python -I` safe, read-only, stdout only);
`.ufo/waves/round-80/claim-pins.json`; the SCORECARD control-receipt row corrected to the landed
arm count with a named correction paragraph; a capabilities-table row for the sweep; a SKILL gate
registry row 14; `.ufo/waves/round-80/count-c1.py`.
C2: three added selftest arms in `.ufo/waves/round-79/count-c2.py` (arms only — the predicate,
CLI and output grammar stay byte-identical, proven by a diff whose hunks lie inside the
selftest region); `.ufo/waves/round-80/mutate-c2.py`; before/after harness receipts.
C3: an append-only `## Instrument inventory (round 80)` section at the end of `PROVINCE.md`
naming every `tools/*` instrument with class, registry row (or `—`) and a one-line purpose;
`count-c3.py`.

## Sweep tool specification (frozen interface)

```
tools/mori-claim-sweep.py --root DIR [--pins FILE] [--carriers PATH[,PATH…]] [--selftest] [--help]
```

- Graded rows: the `## Axes` table of `SCORECARD.md`; every capabilities-table data row of
  `SCORECARD.md`; every `- [` checklist line of `SHONEN.md`.
- Arm `unresolved`: a backticked token matching `*(corpus|tools|.ufo)/…*` in a graded row that
  does not exist under `--root`, after stripping a `:N` / `:N-M` line suffix and an `@<sha>` rev
  suffix. Tokens inside fenced code blocks are ignored.
- Arm `tally`: for each `tallies` entry in the pins file, the tool's live `--selftest` count
  parsed by the frozen grammar (`pass=N … fail=0`, `PASS (N cases)`, `PASS N/N`, `pass=N`) must
  equal the pinned integer. An unparseable or failing selftest is a setup error, never a pass.
- Arm `stale`: each literal in the pins file's `stale_literals` must occur 0 times in the
  carriers (default `SCORECARD.md`, `SKILL.md`, `SHONEN.md`, `LOG.md`).
- Output: one `CLAIM_SWEEP_MISMATCH <class> <carrier>:<line> <detail>` per mismatch, then
  `CLAIM_SWEEP mismatches=M unresolved=U tallies=T stale=S carriers=C pointers=P`.
  rc 0 iff M=0, 1 if M>0, 2 setup (missing root/pins, malformed pins, unreadable carrier).
- Read-only: never writes a file, spawns only the pinned tools' `--selftest` (read-only
  children), no socket, no `/tmp` path of its own; honours `TMPDIR`/`--scratch` for any child
  work dir.

## Wave plan (frozen shape)

ONE v1 wave under `scripts/hyaku/ufo-wave-policy.json` (band 8–16): 14 seats —
4 executor, 3 scribe, 2 scout, 1 connector, 1 reviewer, 1 critic, 1 mutation-tester, 1 labrat.
Attack roles (reviewer, critic, mutation-tester, labrat) = 4/14 = 28.6%. Residual call: none.
Planner seat: the L1. Route: the host table decides; no `model` is passed.

## Source plan (frontier step)

One new row, `S595`: arXiv `2102.11378v2` ("Practical Mutation Testing at Scale"), abstract,
tier A scoped to the abstract's definition of mutation analysis; pin
`corpus/evidence/sources-r80/arXiv-2102.11378v2-abs.html`; duplicate sweep before the fetch;
entry `corpus/knowledge/mutation-adequacy-r80.md` cites the row and grounds C2's criterion.
Assimilation: `merge/mori/` stays closed behind the round-61 L0 (94/136 id collisions).

## Bounds

Lane repo only (`/home/vgpnk/Projects/shokunin/mori-shokunin`); never MANIFEST.json, the fleet
root, `.ufo/state/`, `.scratch/`, sibling lanes; no mutating git/jj command from a seat; scratch
under `/fast/scratch/hyaku/mori-r80/<seat>/` deleted on exit.
