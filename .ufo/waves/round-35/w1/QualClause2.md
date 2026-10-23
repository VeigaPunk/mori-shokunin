measured 2026-10-23T08:51:53Z

# Round 35 W1 — QualClause2

Axes: routed-clause coverage; cell-only checkability; consistency with QUALITY numbering and style.

## Behavior

A depth-claim decision table's verdict cells must tell the reader what to run, read, or report next. The reader-action check evaluates each cell's own text, not its header or neighboring cells. The requirement answers round 33 §8 item 1, clause 2 (`corpus/lessons/round-33-verifier-spotcheck.md:226-228`), reiterated in round 34 §6 item 1 (`corpus/lessons/round-34-verifier-spotcheck.md:196-197`).

## Draft

```DRAFT QUALITY 100
100. In a depth claim's decision table, every verdict body cell names a reader action—what to run, read, or report next—with an imperative verb and a resolvable object (a command, path, or field); a label such as `candidate` alone fails. Check: for each verdict body cell selected by table position, assess the cell text alone, excluding the header and neighboring cells; require the imperative and resolvable object in that text, so no cell passes by inheriting meaning from its header. Lesson: `corpus/lessons/round-33-verifier-spotcheck.md:226-228` and `corpus/lessons/round-34-verifier-spotcheck.md:196-197`. Passing example: `corpus/knowledge/disk-write-rate-r33.md:20` says `Convert a sector delta to bytes by multiplying by 512`, an action with an object. Failing example: `corpus/knowledge/watchdog-identity-r31.md:21` gives only `candidate`, a category rather than an action. Not covered: factual or safety correctness of an action, source support, or whether the larger depth claim rejects no-decision controls.
```

The numbering and layout follow QUALITY's numbered criteria with a Check, lesson, failure example, and limits (`corpus/QUALITY.md:681-765`; earlier form at `corpus/QUALITY.md:665-679`). The requested examples are table body cells: the disk-write-rate row 1 verdict is action phrased; the watchdog-identity first row verdict is only `candidate` (`corpus/knowledge/disk-write-rate-r33.md:18-22`; `corpus/knowledge/watchdog-identity-r31.md:19-23`).

## Findings

Round 34 §6 item 1 records that the round-33 clause 2 remains unanswered (`corpus/lessons/round-34-verifier-spotcheck.md:196-197`).
VERDICT: claims holds

For the proposed reader-action property only, disk-write-rate row 1 instructs converting a sector delta by multiplying by 512 (`corpus/knowledge/disk-write-rate-r33.md:20`).
VERDICT: rows supported

For the proposed reader-action property only, watchdog-identity row 1's verdict is `candidate`, not an action (`corpus/knowledge/watchdog-identity-r31.md:21`).
VERDICT: rows unsupported

## Gates

No tests or automated checks were run; this assignment drafts a criterion and does not audit every cell in either entry. Timestamp command: `timeout 5 date -u +%FT%TZ` → `2026-10-23T08:51:53Z`.

## Touched surfaces

Created only `.ufo/waves/round-35/w1/QualClause2.md` (this report). `corpus/QUALITY.md` and both example entries were read only; no product or criterion file was changed. No tool was installed or updated.

## Out of scope

No criterion was integrated into `QUALITY.md`; no automated checker, depth-claim contract, or table was changed.

## Artifact

`.ufo/waves/round-35/w1/QualClause2.md`
