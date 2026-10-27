# Mo55Mut01 — C1 mutation probe: one wrong v7.3 location (round 55, wave 1)

Seat: Mo55Mut01 (mutation tester, leaf). Lane: mori-shokunin. Scope: scratch-only; no lane/fleet/sibling writes.
Detector: frozen counter `.ufo/waves/round-55/count-c1.py` (unchanged bytes; run with `--repo` pointing at a
disposable scratch clone). Scratch: `/fast/scratch/hyaku/mori-r55/Mo55Mut01` (deleted after the probe; all
evidence inlined below). Disk guard checked before work: no ENOSPC (594 GiB free on /fast/scratch).

I am a non-voter. This report intentionally contains **no** line beginning `RECHECK`, `ENTAIL`, `REPLACE`, or
`QUOTE`; synthetic fixture vote text inside the scratch clone is described, not quoted.

## Claimed invariant under test

Frozen C1 (predicate = counter docstring, contract §C1) rejects a ledger whose claimed v7.3 location for a
scoped pointer is wrong: statuses and line consistency are independently re-derived by the counter from the
pinned v7.2/v7.3 source copies (`derive()` at `.ufo/waves/round-55/count-c1.py:217`, per-row accounting and
`failed` arms at `:307`, `:375`, `:378`, `:395`, `:397`).

## Harness

- Scratch clone of the lane repo at measured data commit `b8b7064c2b54c8b6b22c288232a96c43fae1af47`
  (`git rev-parse --show-toplevel` asserted == clone dir before any fixture commit).
- Because the live wave currently has 0 settled voters, a pristine run fails only on `votes`
  (baseline failure is inconclusive per seat rules). To obtain a green baseline I committed **synthetic,
  scratch-only fixture voters** (`Mo55Rc01.md`, `Mo55Rc02.md` + `w1-results.json` output binding inside the
  clone): each file's final-vote lines are exactly the 78 ledger dispositions mechanically rendered as
  `` `RECHECK <hash> <holds|stale>` `` lines, both repeated in the results output strings so the counter's
  binding check passes. This fixture satisfies the counter's mechanical vote rules; it is labelled synthetic
  and never touched the lane.

## Mutation (exactly one behavior-bearing point)

Ledger `corpus/knowledge/kernel-v7.3-recheck-r55.md`, one cell in one row: pointer row hash `909839af93ac`
(`fs/proc/base.c:1158`, claimed v7.3 lines `1158`, status `same`) — v7.3 lines changed `1158` → `1160`.
Line 1160 of the pinned v7.3 copy is real but different code (`if (mm) {`); the v7.2 block still exists in
v7.3 at its true line 1158, so the claimed `same` location is factually wrong.

Committed as F1 `b15e8efe4c2c1454591963a86e683f067494752d`; diff (one cell only):

```diff
-| `909839af93ac` | corpus/knowledge/oom-tracepoints-r47.md | `fs/proc/base.c:1158` | S526 | 1158 | same | holds |
+| `909839af93ac` | corpus/knowledge/oom-tracepoints-r47.md | `fs/proc/base.c:1158` | S526 | 1160 | same | holds |
```

## Detector runs (pristine / mutant / restored)

Command form (same frozen counter bytes for all runs):
`python3 <lane>/.ufo/waves/round-55/count-c1.py <rev> --repo /fast/scratch/hyaku/mori-r55/Mo55Mut01/clone`

- **R0 — pristine `b8b7064c…`, no voters.** Exit 1.
  `C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0 rev=b8b7064c2b54c8b6b22c288232a96c43fae1af47 failed=votes`
  (Matches the tasking data read: everything mechanical passes at the measured commit; only votes outstanding.
  Inconclusive as a baseline by itself — hence the fixture.)
- **R1 — pristine bytes + synthetic fixture voters (F0 `5f1310f6…`).** Exit 0.
  `C1=met scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=78 dissent=0 rev=5f1310f609e3ef537c1fbca0c14271b27f54539b`
  Green baseline: ledger at `b8b7064c` derives cleanly on every arm; `same=69 moved=7 changed=2` reproduces the
  frozen contract numbers; `--scope` lists 78 rows and includes the mutation target hash.
- **R2 — mutant (F1 `b15e8efe…`), one wrong v7.3 location.** Exit 1.
  `C1=unmet scope=78 rows=78 matched=78 status_ok=77 line_ok=77 source_rows=ok pins=ok provenance=ok same=68 moved=7 changed=2 broken=0 holds=78 stale=0 voted=78 dissent=0 rev=b15e8efe4c2c1454591963a86e683f067494752d failed=line,status`
  The counter independently re-derived the v7.3 content at the claimed lines, found it inconsistent with both
  the v7.2 block and the claimed `same` status, and rejected the ledger on both the `line` and `status` kill arms.
- **R3 — restored (re-run at F0 after `git checkout b8b7064c…`).** Exit 0, output byte-identical to R1.

## Hash and restoration evidence

- Pristine ledger blob (at `b8b7064c`): sha256 `462e67c148d66ce1f886d21540474a19bd6244ae56c5fc1c5c8391ba6e7d5e8e`.
- F0 fixture ledger blob: identical to pristine (asserted in driver).
- Mutant ledger blob (at F1): sha256 `3d7fa76d979c8785259830187d3f0b8c15909243692423008901a695040fb0cb`.
- Restored ledger blob after checkout: `462e67c1…e7d5e8e` — equal to pristine (asserted in driver).
- Scratch clone and all fixture/mutant objects removed after the report was written (`rm -rf` of the seat
  scratch dir). Lane repo received exactly one write: this report file. No commits/pushes to any repo other
  than the two scratch-clone fixture commits above.

## Verdict

**Mutant killed.** A single wrong v7.3 location (one cell, one row) flips C1 `met` → `unmet`, exit 0 → 1,
with `failed=line,status` (`status_ok` and `line_ok` 78 → 77). Frozen C1 demonstrably rejects a wrong pointer;
the pristine ledger at the measured data commit passes every mechanical arm.

## Coverage observation (analysis only, not an exercised second mutant)

[INFERENCE] From `derive()`'s logic (`count-c1.py:217-236`): for rows whose frozen status is already
`changed` (2 of 78), substituting a different v7.3 location whose content merely differs from the v7.2 block
still derives `changed`, so the status arm alone would not distinguish it (the `line` arm fires only if the
v7.2 block verbatim still occurs in v7.3). That blind spot is bounded: it applies solely to `changed` rows,
and pins/provenance/votes arms are unaffected. Not probed here per the one-mutation seat rule; flagged for
the record as a possible future control.

## Findings

- **none (invariant confirmed)** — frozen C1 rejects one wrong v7.3 location. Evidence: this report, section
  "Detector runs" R1 vs R2 (mutant `failed=line,status`, exit 1); counter arms at
  `.ufo/waves/round-55/count-c1.py:375,378,395,397`; mutation diff above.
- **low / observation (not exercised)** — status-arm blind spot for hypothetical wrong locations on the 2
  `changed` rows. Evidence: `.ufo/waves/round-55/count-c1.py:217-236` (read-only analysis; no probe run).
