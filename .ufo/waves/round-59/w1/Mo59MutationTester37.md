# Mo59MutationTester37 — boundary mutations against C2 frozen predicate

Seat role: mutation-tester. Scope assigned: a claim line that parses but whose
claim file is a symlink or empty; a SOURCES row whose `used-by` cell is
`corpus/knowledge/wave-settlement-artifacts-r59.md,` (trailing comma). Work was
read-only on the lane; all mutation probes ran on an isolated fixture repo and
materialized roots under `$HYAKU_SCRATCH/mori-r59/Mo59MutationTester37/`
(scratch cleaned after this report; all receipts embedded below). No production
edits, no lane VCS writes, no fleet/sibling writes.

## Detector

- Frozen counter `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-59/count-c2.py`
  sha256 `2df3ae84f6d66f9ee46cd46cf2cb199ca85e7400301c5a0e9dd94b7b375877be`
  (verified identical at worktree, `HEAD`, and freeze rev `60b3a76a`).
- Counter-level: `python3 count-c2.py HEAD --repo <fixture> --scratch <dir>` —
  the full `measure()` pipeline (git materialization + `eval_entry`).
- Predicate-level: frozen `eval_entry()` imported by path and run on a live
  directory — the same function the entry/trees arms call, on the surface git
  materialization cannot express (symlinks).
- Fixture repo `fixture.QLAZ` (throwaway, `git init` under scratch, toplevel
  asserted), content assembled from lane rev `7b86704d` (C2 data landed).
  F0 commit `b9ff8e466023d31de3ba4f4e3055763f12a65f00`.

## Baselines (pristine)

- Lane end-to-end at `7b86704d`:
  `C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=7b86704d`, exit 0.
- Fixture F0 end-to-end: identical line with `rev=HEAD`, exit 0 — valid substrate.
- `eval_entry` on as-landed materialized root: `ok=true, reasons=[], claims=13 files=6`.

## Mutation results

| Mutant | Where | Expected detector | Actual output | Verdict |
|---|---|---|---|---|
| M1a: `w1-results-r55.json` committed as symlink (mode 120000, target `.ufo/waves/round-55/w1-results.json`) | counter | UNMET via pin/tree | `C2=unmet … failed=entry,pins,tree,tree:corpus/evidence/sources-r59/w1-results-r55.json` exit 1 | **KILLED** |
| M1a': claim file is a live symlink → byte-equal artifact outside root | `eval_entry` | UNMET (claim requires a committed *copy*) | `ok=true reasons=[] claims=13 files=6` exit 0 | **SURVIVED** (latent — see F2) |
| M1b: claim file truncated to 0 bytes | counter + `eval_entry` | UNMET | `C2=unmet … failed=entry,pins,tree` exit 1; fn `pin:2 span:2` | **KILLED** |
| M2: S555 `used-by` cell = `corpus/knowledge/wave-settlement-artifacts-r59.md,` | counter + `eval_entry` | UNMET via `rows:usedby` | `C2=unmet … entry=ok rows=bad … failed=rows` exit 1; fn `rows:usedby=S555` | **KILLED** |
| M4: second S555 row (same cells, comma'd used-by) appended at EOF | counter + `eval_entry` | UNMET (registry holds a contradictory row) | `C2=met … claims=13 files=6` exit 0; fn `ok=true` | **SURVIVED** — finding F1 |
| M4b: same shadow row inserted *before* the good S555 row | counter + `eval_entry` | UNMET | `C2=unmet … failed=rows` exit 1; fn `rows:usedby=S555` | **KILLED** |

Both assigned boundary mutants (symlink/empty claim file; used-by trailing
comma) are killed by the frozen detector. One adjacent mutant survived
end-to-end (F1) and one survived at the predicate surface (F2).

## Finding F1 — first-hit-wins SOURCES row match (counter-level SURVIVOR)

`eval_entry` rows binding (count-c2.py:172–189): for each `source:` sid it scans
`corpus/SOURCES.md` lines, takes the FIRST row matching `ROW` (`break` at line
178), and validates only that row. A second row for the same sid — even one
with a contradictory `used-by` (`…/wave-settlement-artifacts-r59.md,`) or status
— is never examined. Evidence: committing a duplicate S555 row with a corrupted
`used-by` anywhere after the good row yields the full frozen target line
`C2=met … claims=13 files=6` exit 0 (fixture commit after F0, output above).
Inserting the same row before the good row yields `C2=unmet … failed=rows`.
So the binding checks "a correct row exists", not "the sid's rows agree" —
duplicated/mutated rows hide behind the first hit. Bounded: requires a
duplicate sid row in SOURCES.md; does not weaken any single-row check.

## Finding F2 — `eval_entry` accepts symlinked claim files (predicate-level SURVIVOR, latent)

count-c2.py:140–149 does `fb_path.read_bytes()` with no regular-file check.
On a live directory a claim file that is a symlink to byte-equal bytes outside
the corpus copy tree passes pins/spans and scores `ok=true`. This is NOT
end-to-end exploitable through the frozen pipeline: committed symlinks
materialize via `git show` as the link-path text (mode-120000 blob
`0236f759…` in C-M1a), so pin mismatch → UNMET. Reported as a coverage note:
the predicate's "byte-exact committed copy" is enforced by git flattening,
not by `eval_entry` itself.

## Corroborating observation (not a routed finding)

At probe start the working-tree entry carried K11 citing
`corpus/evidence/sources-r59/w1-results-r53.json` — outside the frozen
`ARTIFACTS` set (count-c2.py:55–68) — which would have forced `files:outside`
→ `entry` arm UNMET. The build corrected it while probing (commit `7b86704d`
"K11 demoted to prose (r53 copy outside frozen ARTIFACTS)"); all evidence
above is post-correction bytes (entry sha256
`441a751de67f1cef9db265666a6f77734d7a9d964fe2efcf3756e4394716ce21`).

## Restoration evidence

After every mutation: `git -C fixture.QLAZ reset --hard F0` → `restored=F0`
(HEAD `b9ff8e46…`), and sha256 re-verified:
`w1-results-r55.json` = `2e5b0a0f94d1fa5b90b2804d370db87d25d5197fa65bc4f26441d939b8d9763b`,
`SOURCES.md` = `46c333d2e90fbc61ecd3c6486975990e3dd94a35931369420c95244fe30b2d63`
after each of the 5 cycles. Function-level root restored from a pristine copy
with identical hashes after each of the 5 cycles. Fixture and roots lived only
under scratch; the lane was never mutated (all lane reads via `git show` /
read-only `git ls-tree`).

## Method bounds

Mutations exercised at the smallest behavior-bearing point: one committed copy
file (symlink, empty), one registry cell (trailing comma), one duplicate row
(order pair). No other arms touched; selftest/scan/drift/trees stayed `ok`
throughout, isolating the entry/rows/pins/tree arms under test.
