source: S597 (pending Gate landing)
verified-at: 2026-11-04
recheck: 365d

# Record revision precision (round 82)

Axes: depth, operability, calibration; freshness, coverage and adjacency are held as boundaries, not claimed numerical improvements. The source id is assigned by this round's Gate; S597 was absent from `corpus/SOURCES.md` when this entry was written. No URL or external-source guarantee is inferred. The arm and population below come from the frozen round-82 assignment and `.ufo/waves/round-82/contract.md`, not an external source.

## K1 — Defect class

A record row states a measured value and a revision, but that revision does not contain the claimed value or graded bytes: a true value at a later tip does not validate an earlier label. D80-4 names the measured r80 revision `97ce0c96`, distinct from the evidence-only final tip `44bc941a`; D81-1 repeats the revision-precision class with `pointers=240` attributed to `075574c8`, where the independently graded count is 237 and `SCORECARD.md` contains no `pointers=240`. The 237 count is inherited review evidence from `corpus/lessons/round-81-verifier-spotcheck.md`, not a recount by this entry's author. That review identifies `482dc48d` as a revision where 240 holds.

## K2 — Ordered decisions in the revision arm

For every revision binding, inspect the carrier's first table row containing `row_contains`; report its first failed requirement. A missing row fails `row-value` (the implementation's fallback location is line 1). A failure is detection, not automatic repair.

| Decision | Exact message form | Reader action |
|---|---|---|
| row-value | `REVISION_MISMATCH <carrier>:<line> row-value` | Locate the first matching table row and reconcile its stated `key=value` with the binding. Restore a missing row or append a named correction; never treat a later matching row as the first one. |
| rev-unresolvable | `REVISION_MISMATCH <carrier>:<line> rev-unresolvable` | Resolve the revision to a commit in the declared repository. A missing or invalid revision is unavailable evidence, not a green value. |
| path-absent | `REVISION_MISMATCH <carrier>:<line> path-absent` | Check the named path at that revision; a present path at today's tip does not establish historical presence. |
| rev-bytes | `REVISION_MISMATCH <carrier>:<line> rev-bytes` | Inspect `git show <rev>:<path>`. Correct the record's revision/value with retained provenance; do not substitute later bytes silently. |

The token is an exact bounded numeric `key=value`, not a prefix of a larger identifier or value. Git reads use `--git DIR`, defaulting to `--root`; all bindings are graded, not only the first. The existing pending/pinned arms remain separate, and the summary gains `revisions=<count>`. These semantics were read from the in-flight implementation, not established by a gate execution by this author.

## K3 — Original frozen real-binding population

The seat assignment freezes these three bindings; all use carrier `SCORECARD.md` and historical path `SCORECARD.md`:

| row_contains | key | value | rev | path |
|---|---|---|---|---|
| `mori-claim-sweep.py` | pointers | 240 | `482dc48d` | SCORECARD.md |
| `mori-record-sweep.py` | pass | 26 | `142998f5` | SCORECARD.md |
| `Control-receipt binding guard` | pass | 19 | `142998f5` | SCORECARD.md |

Read-only historical token counts measured by this author were respectively 1, 1 and 1. This proves token presence only, not that the complete bindings pass: the last binding's current carrier row states its tally as `19/19`, not `pass=19`, so its row-value requirement was not satisfied at the observed worktree snapshot. The standalone `pass=19` occurrence at the named revision is correction prose, illustrating the lower bound's limit.

Presence of `key=value` in the named path's bytes at the named revision is a cheap, sufficient lower bound for this narrow byte-consistency check: it rejects a claimed value entirely absent from that historical file without rerunning its producer. It does not prove the command's output, only the record's arithmetic at this limited textual level. It cannot tell a coincidental occurrence in an unrelated line from the graded one, nor independently recompute 237 or 240. It is necessary textual support, not sufficient proof of the underlying measurement or of complete record integrity.

### Population conflict retained

The observed contract worktree appends `Pre-data amendment A1`, which says “The "Real bindings" table's first row is replaced” but supplies three replacement rows. L1 MoriR82 subsequently instructed this seat: “A1 is the authority; document A1's three bindings, not the superseded three.” The original seat assignment instead requires “the real binding population (the three frozen bindings).” These conflicting instructions are retained for adjudication, not silently reconciled by treating artifact prose as new authority. The original population above is historical and is not claimed green.

### A1 population designated by the integration owner

L1 identifies these as the replacement real bindings, superseded pre-data according to A1; this author has not executed them or established their landed status. Carrier and historical path are `SCORECARD.md` throughout.

| row_contains | key | value | rev | path |
|---|---|---|---|---|
| `row_tally=19` | row_tally | 19 | `075574c83eae` | SCORECARD.md |
| `survivors=0` | survivors | 0 | `075574c83eae` | SCORECARD.md |
| `wrong=0 fixtures=7` | wrong | 0 | `482dc48d` | SCORECARD.md |

A1 explains that original binding 1 conflicts with the r81 pinned arm's landed-value rule: its `pointers=` value moves when the record grows, whereas the revision binding fixes that value historically. Original binding 3 independently fails `row-value` by the inspection above. Those are two distinct reasons to replace the original population, not evidence that the replacement has passed. Historical claim-table rows avoid that moving-count coupling. Integration receipts, not this entry, establish the final population and C3 result.

## K4 — Worked D81-1 byte-absence example

Executed read-only against the lane repository:

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 075574c8:SCORECARD.md | grep -c 'pointers=240'
```

Observed stdout:

```text
0
```

The executed batch used `cd /home/vgpnk/Projects/shokunin/mori-shokunin` and the equivalent `git show` pipeline; its exact command is retained in the seat report. GNU grep returns 1 for no matching lines even though it prints `0`. No revision-arm gate was executed here. The absence is the D81-1 `rev-bytes` shape when a carrier row does state `pointers=240`; this example alone does not derive the historical graded count 237.

## Boundaries

This gate grades mori's own record and its explicitly registered bindings, never another lane's. It is not a lifecycle or admission decision and does not certify fleet health, source admission, settlement, command relevance or exhaustive historical correctness. Detection and report only: no remediation, host/unit/service/credential changes, foreign record audit or orchestration control. The source Gate, implementation, pins, final revision and integration receipts have separate owners; a contract target or source citation is not execution evidence.
