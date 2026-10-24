# the ancestry half of a supersede disposition: reachability, not walk order

source: S227 — gitrevisions(7), the two-dot range notation as reachability
set-difference; S069/S073/S226 — the lane's own containment-disposition history
(`corpus/knowledge/containment-timed-supersede-r38.md`).
verified-at: 2026-10-24 — `python3 tools/mori-sources-appendonly.py --selftest`
(12 cases) and `python3 .ufo/waves/round-39/fixtures/run-c9-dags.py
<ufo/waves/round-39/scratch/gate-r38.py|tools/mori-sources-appendonly.py> <lane>
<out>` over the committed DAG fixtures; receipts
`.ufo/waves/round-39/evidence/c9-red-a.txt`, `c9-after-fixture-a.txt`,
`c9-after-fixture-c.txt`, `c9-after-lane.txt`.
recheck: on the next change to tools/mori-sources-appendonly.py's walk, edit
detection or timing code, and with the S227 cadence.

## Why walk order is not ancestry

The round-38 gate decided "superseded-as-of" by comparing path-log *indices*:
an id was as-of when the superseding row's landing index exceeded the id's last
edit index (`landing > last_edit[cid]` over `git log -- path`). Two round-38
residual seats (lesson F1/F2, `.ufo/waves/round-38/resid/ResidGateTiming.md`)
showed what that means on any history with a side branch:

- F1: index order is not the descendant relation. A superseding row that lands
  on a branch incomparable with the edit can sort after it in the walk and be
  reported as-of for a disposition that never descends from the edit.
- F2: edit detection compared each commit's snapshot with the previous *walk
  record* instead of its parent, fabricating edits and reversions across a
  merge (committed fixture C: the round-38 bytes print
  `round_changed=[S001]` exit 1 where no first-parent edit exists).
- The lane itself was not immune to the walk defect: the default
  `git log -- corpus/SOURCES.md` walk silently drops TREESAME commits
  (`6531ac60` appears only under `--full-history`, 53 vs 52 commits), so every
  round-38 index was computed over a simplified history.

gitrevisions(7) states the relation the predicate actually names (S227): a
range `r1..r2` is "commits that are reachable from r2 excluding those that are
reachable from r1" — reachability set-difference, independent of walk order,
commit dates, or history simplification. "Descends from" is that reachability
relation; the round-39 gate computes it with `git merge-base --is-ancestor`.

## The round-39 semantics (gate P-C9)

anchor: --full-history
anchor: nearest_path_commit(repo, parent, path)
anchor: supersede_timing superseded_as_of=

- The walk carries parent hashes (`git log --format=%H%x09%P --reverse
  --full-history`) so no reachable path commit is silently dropped.
- An edit at a commit is a change of the id's immutable cells against its
  first parent's state (resolved through `nearest_path_commit` for parents
  that do not touch the registry, e.g. verifier commits between registry
  commits) — not against the previous walk record.
- `supersede_timing`: an id is `superseded_as_of` only when
  `git merge-base --is-ancestor <last_edit_commit> <landing_commit>` exits 0
  (the landing commit descends from, or is, the last edit commit); otherwise
  stale. The output line shape is byte-identical to round 38 and the
  lane-history receipts are byte-identical (`c9-after-lane.txt` diffs clean
  against the round-38 receipts at both the tip and `e37dcc6`).

## Observable corrections on committed fixtures

- Fixture A (side branch carries the pre-edit value; supersede row on the
  side; merge): round-38 bytes print `stale=[S001]` — the right verdict reached
  through fabricated intermediate edits (F2), visible in the full receipt.
- Fixture C (diamond): round-38 bytes print `round_changed=[S001]` exit 1; the
  ancestry gate prints `round_changed=[]` exit 0. F2 observable.
- Fixture D (both branches make the same edit; supersede row rides the side
  branch, so the row's landing commit IS the id's last edit commit): the
  predicate's plain words read as-of; the round-38 bytes print stale. F1
  observable against the predicate text.

## Limits

- The lane registry history is a single chain of path commits (52 + 1
  TREESAME); no merge over `corpus/SOURCES.md` has occurred, so no round-38
  receipt is falsified — the correction is semantic, and the byte-identical
  lane receipts are the no-harm evidence.
- "Latest superseding row" remains max-first-landing-index per (target, by)
  on the full-history walk; two *different* superseding rows on incomparable
  branches are still chosen by walk order (r38 ResidGateTiming residual 2; no
  fixture constructs a wrong verdict from it).
- "The id's last immutable-cell edit" on a DAG where two incomparable commits
  edit the id is order-defined (latest in the full-history walk); fixture D's
  verdict follows that reading, matching the predicate's "landing is the last
  edit commit" case.
