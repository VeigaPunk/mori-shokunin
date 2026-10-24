# MutC2Record — mutation probe: LOG round-42 tally erratum re-asserted

Role: mutation-tester (round-42 v2 wave). Target: `.ufo/waves/round-42/count-c2.py`
(frozen counter, sha256 `693f293cddab0c0108822ab51dd566373e4d78ce020f8f91b733d3f7817c3ade`).
Sandbox: `/tmp/r42-mutc2-record` (`git clone --no-hardlinks` of the lane repo; lane Git/jj
never written). Attack tip: `34b926730c30e0251e1aec531863d8355dc491f1`.

## Mutant

Single behavior-bearing flip in the C2 record, not the counter: LOG.md round-42 errata
item (a) was changed from the superseded-by correction back to a re-assertion of the old
`8/8` tally, with `5/8`, `SURVIVED` and the `superseded` qualifier removed from the
window. Committed on scratch branch `mutc2` (parent = attack tip):

- mutant commit `74f4166d7deaa56ffc18e27b046577f2da0b6a38`
- diff: `LOG.md | 8 ++++----`, 1 file, 4 insertions / 4 deletions

```
-  that is **superseded by 5/8 killed, 3 SURVIVED** — the survivors are named
-  by `.ufo/waves/round-41/w1/MutC1Walrus.md`, `MutC1Tuple.md`,
-  `MutC1DropSort.md`, each carrying `SURVIVED`. The same three lanes are
-  what C1's v5 arms now kill.
+  that tally stands exactly as written: all eight mutant lanes were killed,
+  no lane survived, and the lane-owned record here keeps the eight-of-eight
+  figure as the accurate one; the three-survivor claim in the round-41
+  verifier note does not apply.
```

The replacement was padded to >200 chars so item (b)'s own `superseded` string falls
outside `bad()`'s `m.start()-200 .. m.end()+200` window; otherwise the sweep's whitelist
would mask the re-assertion. `SCORECARD.md` and all fixtures were left untouched.

## Expected detector behavior

`count-c2.py` at the mutant should fail two checks and print `C2=unmet` with exit 1:
`log_erratum_tally` (no `5/8`, no `SURVIVED` in the round-42 LOG entry) and
`sweep_log_clean` (uncontradicted `8/8 mutants killed`). All fixture and SCORECARD checks
should stay PASS.

## Actual output

Pristine baseline in the sandbox, both revs (red-before control is the lane's own
`evidence/control-c2-before.txt` at `9de7323d`, `C2=unmet` EXIT=1):

- `count-c2.py 34b9267…` → all 12 checks PASS, `C2=met`, rc 0
- `count-c2.py HEAD` (`f3ec0977`) → all 12 checks PASS, `C2=met`, rc 0

Mutant `74f4166d`, full output:

```
check evidence_returned_total PASS (w1 md reports=19 want 19)
check evidence_roles         PASS (Scr=5 Scout=1 want 5/1)
check evidence_attack_seats  PASS (attack=31/64 reviewer=12 critic=11 mut=8 exec=3)
check evidence_survivors     PASS (SURVIVED reports=3 want 3)
check log_erratum_tally      FAIL (round-42 LOG entry present=True)
check log_erratum_attack     PASS (round-42 LOG entry present=True)
check log_erratum_roles      PASS (round-42 LOG entry present=True)
check score_erratum_tally    PASS (round-42 SCORECARD section present=True)
check score_erratum_attack   PASS (round-42 SCORECARD section present=True)
check score_erratum_roles    PASS (round-42 SCORECARD section present=True)
check sweep_log_clean        FAIL (uncontradicted=false-claim hits: ['8/8 mutants killed'])
check sweep_score_clean      PASS (uncontradicted=false-claim hits: [])
C2=unmet
rc=1
```

Exactly the two predicted checks flipped; no crash, no collateral failure.

## Verdict

**KILLED.** The mutated record is detected: `C2=unmet`, exit 1. The counter is sensitive
to a re-asserted superseded tally in either of the two intended predicates (per-record
tally check and the uncontradicted-sweep), so the erratum is load-bearing rather than
merely present. (Coverage note only, no contract change: the tally check is
string-presence based — `5/8`, `SURVIVED` — and the sweep is a 200-char keyword
whitelist; both fired here, which is the property under test.)

## Restoration evidence

Restored by detaching the sandbox back to the pristine attack tip; lane bytes re-derived
from `git show` and compared:

| state | rev | LOG.md sha256 | detector |
|---|---|---|---|
| pristine | 34b9267 | `2b4eb708…b09869c54` | `C2=met`, rc 0 |
| mutant | 74f4166d | `ee13c420…55f733ea0f` | `C2=unmet`, rc 1 |
| restored | 34b9267 | `2b4eb708…b09869c54` | `C2=met`, rc 0 |

- `git status --porcelain` in the sandbox after restore: empty.
- Restored `LOG.md` / `SCORECARD.md` hashes equal the lane's committed blobs at
  34b9267 (`git show 34b9267:LOG.md | sha256sum` → `2b4eb708…b09869c54`;
  SCORECARD → `b57c9c03…9308cdac87`).
- The lane repo was read-only throughout (`git rev-parse HEAD` still `f3ec0977`); no
  fleet, sibling, jj or index writes; no pacman/upgrades; no tool installs needed
  (`python3`, `git` already present).

Report: .ufo/waves/round-42/w1/MutC2Record.md
