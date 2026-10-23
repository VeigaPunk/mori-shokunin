# ScoutFrontierRows — r38 coverage-map and Round-38 rows

Verdict: **PASS**. Both new r38 notes are in `corpus/README.md` `## Coverage map` and in `## Round-38 coverage additions` at scored tip `f725f3076972e6e70595b5ac8279be524a111ff8` (HEAD). Neither is missing from the map or the section.

Axes: map presence, Round-38 section presence, Frontier-table presence, scored-tip line identity. No install.

## Observed

`git rev-parse HEAD` = `f725f3076972e6e70595b5ac8279be524a111ff8` (`f725f30 round-38: C1 counter v4.1 + freeze v2 pins, C4 byte-capped reads, wave-1 spec/dispatch, attempt-2 evidence`). `git diff --stat f725f307… -- corpus/README.md` is empty: the working-tree README matches the scored tip. `git grep` of the two filenames at entering tip `e33bb561712b32f46861362a3fa43762fa70ae4f` returned no hits.

`git grep -n` of `source-drift-content-anchor-r38`, `containment-timed-supersede-r38`, and `Round-38 coverage` at `f725f307… -- corpus/README.md` hits only lines 47, 48, 593, 597, and 598.

### Coverage map (`## Coverage map`, lines 3–48)

Header `| Note | Holds | Sources |` at line 5. The two new rows are the last map rows. Line 46 is the preceding `knowledge/source-drift-hardening-r37.md`. Line 49 is blank; line 50 is `## Known gaps`.

- **Line 47** — `knowledge/source-drift-content-anchor-r38.md`
  - Holds: the content half of the drift-corpus binding: named `anchor:` code strings that must resolve in the probe's bytes, capability paths that must resolve from the repo root, one named drifted row per summary count, and a named-row selftest arm killed by its own mutation; three fabricated token witnesses rejected
  - Sources: S205; S221–S226; `.ufo/waves/round-38/count-c4.py`; `.ufo/waves/round-38/evidence/c4-after.txt`
- **Line 48** — `knowledge/containment-timed-supersede-r38.md`
  - Holds: containment decided on the resolved canonical path (S226), and the timed supersede reading: a disposition postdates the edit or the gate lists it in `stale_supersede`; S069's disposition at the round-38 tip
  - Sources: S226; S069; `tools/mori-sources-appendonly.py`; `.ufo/waves/round-38/evidence/gate-after.txt`

### Round-38 section (`## Round-38 coverage additions`, lines 593–598)

Header `| Ground | Entry | Bounded advance |` at line 595. The file ends on line 598. Headings from line 530 at the scored tip: Round-31 coverage additions (531), Round-31 Frontier note (537), Round-34 Frontier note (544), Round-36 coverage additions (565), Round-37 coverage additions (587), Round-38 coverage additions (593). No later heading.

- **Line 597** — Entry cites `knowledge/source-drift-content-anchor-r38.md`; `.ufo/waves/round-38/count-c4.py`
  - Ground: Content-anchor verification (calibration/discrimination): a corpus binding is checked for resolvability — named code anchors, capability paths, one named drifted row per summary count, and a named-row arm killed by its own mutation — not for token presence (r37 M9)
  - Bounded advance: `python3 .ufo/waves/round-38/count-c4.py <rev>` rejects three fabricated token witnesses and prints `C4=met` on the real binding; the r37 counter prints `C2=met` on the same fabricated binding (`evidence/v3-token-control.txt`). Bounded: an anchor proves presence in the bytes, not semantics; the mutation arm is the separate statement.
- **Line 598** — Entry cites `knowledge/containment-timed-supersede-r38.md`; `tools/mori-sources-appendonly.py` (`supersede_timing`); S226
  - Ground: Timed supersede disposition (depth/gate): a supersede row only disposes an edit when its landing commit postdates the edit; presence is not disposition
  - Bounded advance: `python3 tools/mori-sources-appendonly.py <rev> --round-base f10a320d` prints `supersede_timing superseded_as_of=[...] stale_supersede=[...]`; at `e37dcc6` S069 is stale, at the round-38 tip it is as-of. Bounded: commit order in the path's history; the in-place change stays listed (QUALITY 102).

### Frontier table (`## Frontier`, lines 335–353)

Id table is FR1–FR14 only (data rows 339–352). `git show f725f307…:corpus/README.md` lines 335–353 contain neither filename. There is no `## Round-38 Frontier note`. Absence from this table is not a fail: acceptance fails only if an entry is missing from the map or the Round-38 section.

### Note files (existence only)

- `corpus/knowledge/source-drift-content-anchor-r38.md:1` — “the content half of a corpus binding: anchors that must resolve”
- `corpus/knowledge/containment-timed-supersede-r38.md:1` — “containment on the resolved path, and a supersede that postdates the edit”

## Inference

[INFERENCE] The Round-38 index for these two notes is the coverage-map pair (47–48) plus the coverage-additions pair (597–598), not a new FR id. Round 37 indexed `source-drift-hardening-r37.md` the same way (map line 46; Round-37 section line 591) with no new Frontier row.

## Unresolved

Whether a later admission step was supposed to add an FR row or a “Frontier note — no existing row closed” paragraph. Not required for this check; not present in the README at `f725f307`.

## Confidence

High. Line numbers are `git grep` / `git show` at the scored tip, and the working tree does not differ from that blob for `corpus/README.md`.
