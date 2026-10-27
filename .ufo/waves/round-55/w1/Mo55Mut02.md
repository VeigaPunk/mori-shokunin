# Mo55Mut02 — C1 duplicate/omission mutation probes (round 55, wave w1)

Seat: Mo55Mut02 (mutation tester, leaf). Lane: mori-shokunin. Date: 2026-10-27.
Assignment: remove, duplicate and add rows in scratch fixtures; test the frozen C1 row binding.
Detector under test: frozen `.ufo/waves/round-55/count-c1.py` (P-C1), run end-to-end as
`python3 .ufo/waves/round-55/count-c1.py <rev> --repo <scratch-clone>` against real git commits.
No lane source was touched; all probes ran in an isolated clone inside the seat scratch.
This seat is not a C1 voter (not in `Mo55Rc01`–`Mo55Rc16`); this report emits no vote lines.

## Method

- Scratch: `/fast/scratch/hyaku/mori-r55/Mo55Mut02/` (removed after the run; this report is the durable record).
- Fixture: `git clone` of the lane repo into scratch; `git rev-parse --show-toplevel` asserted as the
  fixture dir before any fixture mutation; branch `mut-probes` cut from the measured data commit
  `b8b7064c2b54c8b6b22c288232a96c43fae1af47` ("measure the latter" of the two data corrections).
- Each mutation was committed with a scratch-only identity (`-c user.name=Mo55Mut02 -c user.email=mo55mut02@scratch.invalid`),
  then the frozen counter was run against the mutation commit. Pristine, mutated and restored bytes were
  hashed (sha256) before/after; the ledger was restored to the exact pristine bytes at the end and re-run.
- Detector binding logic exercised (from frozen `evaluate()`): `parse_ledger` collects all table rows;
  duplicates set `dup`, ledger hashes outside the frozen 78-hash scope set `extra`, and
  `rows != len(sc)` / `matched != len(sc)` / `status_ok` / `line_ok` / votes gates kill. The frozen scope
  is derived from the entering tip `ca52426ea496bc6592e3e867cc9d28843e45f196`, independent of ledger bytes.

## Baseline (pristine bytes, rev b8b7064c)

Command: `python3 .ufo/waves/round-55/count-c1.py b8b7064c2b54c8b6b22c288232a96c43fae1af47 --repo <clone>`

Ledger sha256 (pristine): `462e67c148d66ce1f886d21540474a19bd6244ae56c5fc1c5c8391ba6e7d5e8e`

Output (exit 1):

```
C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0 rev=b8b7064c2b54c8b6b22c288232a96c43fae1af47 failed=votes
```

This reproduces the assignment's data read exactly (scope=78 rows=78 matched=78 status_ok=78 line_ok=78,
pins/provenance/source_rows ok, 0 votes, exit 1). The single failure `votes` is the healthy in-progress
state: the scratch clone contains no `Mo55Rc01`–`Mo55Rc16` reports or `w1-results.json` at the measured
commit, so `voted=0`. All row-binding gates pass on pristine bytes: 78 rows, no dups, no extras,
69 same / 7 moved / 2 changed.

## Mutation probes

Every mutant below was killed by at least one row-binding gate *in addition to* the baseline `votes`
failure. Detector output lines are verbatim; all runs exited 1.

| # | Probe | Mutation commit | Ledger sha256 | Detector output | Exit | Verdict |
|---|-------|-----------------|---------------|-----------------|------|---------|
| M1 | Remove one row (`b50f210b822a`, mm/page_alloc.c:4630, moved) | `4c334a3514c46ded18604b11967913f9f39efac8` | `cfbeb65a711274ca0dfd4ceb06868c985b84b77047af454e78579376a1198ab9` | `C1=unmet scope=78 rows=77 matched=77 status_ok=77 line_ok=77 source_rows=ok pins=ok provenance=ok same=69 moved=6 changed=2 broken=0 holds=77 stale=0 voted=0 dissent=0 rev=4c334a3514c46ded18604b11967913f9f39efac8 failed=line,matched,rows,status,votes` | 1 | KILLED |
| M2 | Append verbatim duplicate of row `7b2d297eec60` | `94120cb9d8a3586ae7665ba2cb8372b080812a8b` | `e7bb9d1e3b290160939013172c112f33008068e0f7acdf3d86d3021b4eeb7294` | `C1=unmet scope=78 rows=79 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0 rev=94120cb9d8a3586ae7665ba2cb8372b080812a8b failed=rows,votes` | 1 | KILLED |
| M3 | Append fabricated row, out-of-scope hash `000000000000` | `bbc6c43db17716f43106fb729ba476afbd24bd3f` | `65cc3e754abbf2c792707ddc10dddb28149320119f8bd7f8708482e003e72119` | `C1=unmet scope=78 rows=79 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0 rev=bbc6c43db17716f43106fb729ba476afbd24bd3f failed=rows,votes` | 1 | KILLED |
| M4 | Append second copy of hash `b50f210b822a` with tampered v7.3 lines (4689→4690) | `08b4c78dadf2c4d0f0d8d13e3f832a4acc070f6d` | `cb534d81fca6d65ea02a8c13e24c3d42c6ec9ea5aeffbd76fc0c53dca27806af` | `C1=unmet scope=78 rows=79 matched=78 status_ok=77 line_ok=77 source_rows=ok pins=ok provenance=ok same=69 moved=6 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0 rev=08b4c78dadf2c4d0f0d8d13e3f832a4acc070f6d failed=line,rows,status,votes` | 1 | KILLED |
| M5 | Append malformed 6-cell row (not bindable to a 7-cell hash row) | `43e9c9483591a2f8594486cf76624fab1b4eccd5` | `a2f3ca97adea29725f385f7a20bc2f61d4a609e3a45cdc1e6d4edd8fb55bdd39` | `C1=unmet scope=78 rows=79 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0 rev=43e9c9483591a2f8594486cf76624fab1b4eccd5 failed=rows,votes` | 1 | KILLED |
| M6 | Swap the first two data rows (order probe) | `21040916afe83d21f5812ead187dec0fe2778e3e` | `62c66c4e923fd1c1091c4dbe1d8a177e85f160866a5a459ab0474ebedbf085da` | `C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0 rev=21040916afe83d21f5812ead187dec0fe2778e3e failed=votes` | 1 | SURVIVED |

## Analysis

- M1 (omission): killed via `rows` (77≠78), `matched` (77/78), and cascading `status`/`line`. The removed
  row was one of the 7 `moved` pointers, so `moved` drops 7→6, confirming the counter binds each scoped
  hash to its ledger row.
- M2 (verbatim duplicate): killed by `rows` alone (`dup=True`, rows=79). Content still matched 78/78
  because `byhash` keeps the last, identical, copy — the pure row-count/dup gate carries the kill.
- M3 (fabricated extra): killed by `rows` via the `extra` list — any ledger hash outside the frozen
  78-hash scope fails even though scoped rows still match 78/78.
- M4 (duplicate + tamper): killed three ways — `rows` (dup), plus `status` and `line` both drop to 77
  because the tampered second copy wins in `byhash` and its v7.3 lines (4690) fail the mechanical
  re-derivation for the 4630 block. Row binding is to the hash *and* the full cell content.
- M5 (malformed 6-cell row): killed by `rows` (79≠78) even though the extra row never binds to a hash —
  the raw parsed-row count is itself a gate.
- M6 (reorder): survived — every metric is identical to baseline (only `rev` differs). This is a
  coverage finding, not a contract gap: the frozen P-C1 predicates (no missing row, no dup, no extra,
  content-bound matched/status/line, pins, provenance, votes) are all order-independent. No contract
  change is warranted; the surviving mutant does not contradict any stated kill rule.

## Restoration evidence

- After the probes, the ledger was restored with `git checkout b8b7064c2b54c8b6b22c288232a96c43fae1af47 -- corpus/knowledge/kernel-v7.3-recheck-r55.md`.
- Restored sha256: `462e67c148d66ce1f886d21540474a19bd6244ae56c5fc1c5c8391ba6e7d5e8e` — byte-identical to the
  pristine hash recorded before any mutation.
- Re-run of the frozen counter on the restored pristine commit reproduced the baseline output
  byte-for-byte (`diff` of the two captured output files: identical; exit 1, `failed=votes`).
- The scratch directory `/fast/scratch/hyaku/mori-r55/Mo55Mut02/` (clone + captured outputs) was removed
  after the report was written; this report inlines all command/output evidence.

## Environment / hygiene

- Disk guard checked before heavy work: `/fast/scratch` at 26% use, ~595G free — no ENOSPC risk.
- No installs (none needed). No lane source edits; no fleet/sibling writes; no commits or pushes to the
  lane (all git mutations were inside the scratch clone only, identity `Mo55Mut02 <mo55mut02@scratch.invalid>`).
- Lane state verified untouched: only this report was written under `.ufo/waves/round-55/w1/`.

## Findings

- info — Frozen C1 row binding is robust against omission, verbatim duplication, fabricated extras,
  tampered duplicates, and malformed rows: 5/5 kill probes killed with exit 1 and distinct additional
  failure gates (`line,matched,rows,status` variants). Evidence: this file, sections "Baseline" and
  "Mutation probes".
- info — Row order is not part of the frozen invariant (M6 survived with output identical to baseline).
  Coverage finding only; no contract violation, no counter change indicated. Evidence: this file,
  probe M6 row and "Analysis".
- info — Baseline failure mode at the measured data commit `b8b7064c` is exactly `failed=votes` with all
  mechanical gates green, matching the round data read; the binding probes are distinguishable from the
  baseline by their additional failed gates. Evidence: this file, "Baseline" and "Restoration evidence".
