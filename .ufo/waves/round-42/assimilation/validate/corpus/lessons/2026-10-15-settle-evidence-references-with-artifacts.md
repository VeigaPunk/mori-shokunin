# Lesson — settle evidence references alongside replacement artifacts

date: 2026-10-15 · lane: mori-shokunin · round: 11 · source seat: lessons-distiller

Source round: round 10, `LOG.md:477-500` and
`.ufo/reports/round-10/mori-goalwave.md:15-40`. Independently checked during the
round-11 audit at lane HEAD `d1e0dd90e6042723617fc75cdfb1987684d21ce4`;
round-10 evidence commit `5be89432ab4472f9193b2a787f78199ebeb58cc1` resolves
and is an ancestor of that HEAD. This is a lesson from one checked evidence
seam, not an admission verdict on the whole lane.

## The lesson

An executable can pass its acceptance checks while the instructions describing
its adopted evidence are not executable. When an artifact is replaced during a
wave, settling the script SHA and the final receipt does not settle every
consumer of the old artifact. Resolve the active recipes against the delivered
commit, and record which earlier artifact each replacement supersedes.

For mori's drift pin, distinguish these three claims:

- The census's drift mechanism works at the admitted bytes.
- The adopted baseline exists, matches its receipt, and can be compared now.
- The knowledge note's adopted-baseline table and rerun command identify that
  same artifact.

The checks below support the first two and expose a defect in the third. A
missing baseline is not census behavioral drift: the CLI correctly reports
that it could not perform the comparison.

## The independently checked seam

`corpus/knowledge/drift-pin-r10.md:191-200` is headed "The adopted lane
baseline (receipts-writer's artifact)" and names:

```text
| path | `corpus/evidence/baseline-r10-20261015T2210Z.json` |
| baseline sha256 | `bdf464968003ed48014ea8da23045a5112628dbf11cc164755fbdff0af4c5649` (6779 B, 39 lines) |
```

Its rerun recipe at `:226-227` still hashes and drifts that path. However, the
round report at `.ufo/reports/round-10/mori-goalwave.md:20-22`, the round log
at `LOG.md:482-484`, and the evidence index at `corpus/evidence/README.md:709-717`
name `baseline-r10-20261015T2231Z.json`. The committed pin receipt confirms the
latter path and its hash at `corpus/evidence/pin-r10-20261015T2231Z-pin.log:3-10`.

Commands below were run from the lane root; outputs are observed, not inferred.

```text
$ git cat-file -e 5be89432ab4472f9193b2a787f78199ebeb58cc1:corpus/evidence/baseline-r10-20261015T2210Z.json
fatal: path 'corpus/evidence/baseline-r10-20261015T2210Z.json' does not exist in '5be89432ab4472f9193b2a787f78199ebeb58cc1'
exit: 128

$ git ls-tree 5be89432ab4472f9193b2a787f78199ebeb58cc1 -- corpus/evidence/baseline-r10-20261015T2210Z.json corpus/evidence/baseline-r10-20261015T2231Z.json
100644 blob 3bcf93aec486fdea19badb61d4e6b77850e52ee0	corpus/evidence/baseline-r10-20261015T2231Z.json
exit: 0

$ bash tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2210Z.json
mori-census: --drift baseline missing: corpus/evidence/baseline-r10-20261015T2210Z.json
exit: 2

$ bash tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json
MORI_DRIFT: none
exit: 0
```

The active artifact was also byte-checked, not accepted merely because its
receipt named it:

```text
$ sha256sum tools/mori-census.sh tools/mori-silence-cases.sh corpus/evidence/baseline-r10-20261015T2231Z.json corpus/evidence/pin-r10-20261015T2231Z-pin.log
d7710981aa1c7571ff9d6fd7f75822811173010e5f4e298ac3c47fab274a0b20  tools/mori-census.sh
448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5  tools/mori-silence-cases.sh
0993b23505deab2aeb05b2309bdf7dd6eaad2b82f27852491352511aa9670478  corpus/evidence/baseline-r10-20261015T2231Z.json
04bae8a296667bb9a19956e2fd4e6e66fc7e6fff7d38b6683ef9e5fd9f83d6fd  corpus/evidence/pin-r10-20261015T2231Z-pin.log

$ git show 5be89432ab4472f9193b2a787f78199ebeb58cc1:corpus/evidence/baseline-r10-20261015T2231Z.json | sha256sum
0993b23505deab2aeb05b2309bdf7dd6eaad2b82f27852491352511aa9670478  -
```

A separate byte comparison using `git show <evidence-commit>:<path>` versus
`Path(path).read_bytes()` returned equality for both tools, the knowledge note,
the adopted `2231Z` baseline, and its pin receipt. Thus the missing-reference
finding is present in the delivered evidence, not caused by an audit-time edit.

The CLI checks were rerun at those exact tool hashes:

```text
$ bash tools/mori-census.sh --selftest
[last line] MORI_CENSUS_SELFTEST: PASS (66 cases, 66 passed, 0 failed)
exit: 0

$ bash tools/mori-silence-cases.sh
[last line] MORI_SILENCE_CASES: matched=28 total=28
exit: 0
```

The oracle run logged `SHUFFLE_SEED=3382903303` and `RUN_NONCE=3534338897`.
These are run identifiers, not an impossibility proof or independent promotion
verification. The executable checks' green results do not resolve the missing
artifact in the knowledge note.

## Applying it to later mori rounds

1. Give every active evidence claim a complete identity: command and overrides,
   code revision, input path and digest, expected output and exit contract.
   Check the path in the delivery commit, not only in a worker's live tree.
2. When a baseline or receipt is replaced, record a disposition row containing
   the superseded path/digest, replacement path/digest, landing commit, affected
   recipes, and any historical result that remains unverifiable. The artifacts
   need not be interchangeable merely because their formats are the same.
3. Sweep for the superseded path and digest before admission. For the seam above,
   searching `corpus/` for the `2210Z` filename and the full `bdf46496…` digest
   located the surviving references in `corpus/knowledge/drift-pin-r10.md`.
   Interpret each hit: a clearly historical citation may stay; an active
   "adopted baseline" or rerun recipe must resolve, or be explicitly superseded.
4. Execute the public rerun recipe as written, independently of selftest and
   oracle acceptance. Here that extra check distinguishes exit 2 "no comparison"
   from exit 0 "compared and equal" without changing a single census byte.
5. Preserve filed evidence. Correct append-only records with a named new entry,
   and route unresolved citation debt to the owning record rather than silently
   re-pinning, fabricating the old artifact, or rewriting the historical claim.

A falsifier for the lesson's proposed discipline is simple: after replacement,
any active recipe still naming an absent delivery-tree artifact is a remaining
reference defect, even when the tool's acceptance suite is green.

## Limits and disposition

- The note's historical claim at `corpus/knowledge/drift-pin-r10.md:207-214` — a
  clean comparison at 22:12:12Z against the `2210Z` artifact — was not independently
  reverified. Its baseline is absent from the delivered evidence commit. This
  does not prove that the historical experiment never occurred; the `2231Z`
  rerun does not retroactively verify different input bytes.
- The clean `2231Z` drift result is a live observation on this host during round
  11. A later host-state change may legitimately produce drift; the durable
  identity check is the committed artifact and its matching digest.
- The audit left the knowledge note, report, index, baseline, tools, scorecard,
  and log unchanged. This new lesson records the defect and a future integration
  discipline; it does not close the citation debt or attest any SHONEN box.
