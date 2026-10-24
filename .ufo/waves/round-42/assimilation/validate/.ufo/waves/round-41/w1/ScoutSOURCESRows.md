# Scout report — S230/S231 SOURCES rows (round 41, w1)

Question: are S230/S231 placed inside the single `## Registry` table, and does
S231's teaches cell open `supersedes S229`? Verified in
`corpus/SOURCES.md` at lane working-tree tip.

## Observed

- Single `## Registry` heading at `corpus/SOURCES.md:3`; table header row at
  `:5`. Exactly one Registry table exists in the file.
- The Registry table runs contiguously through `corpus/SOURCES.md:237`;
  `## Paths` begins at `:239` (only a blank line between). The file is 296
  lines; no `| S…` row appears outside lines 7–237.
- `S230` row at `corpus/SOURCES.md:236`; `S231` row at `:237` — both inside the
  Registry table, directly after S229 (`:235`). No duplicate id rows
  (231 `| S` rows total for S001–S231).
- S231 teaches cell (line 237) opens literally
  `supersedes S229 — the exact resolution quote is 17 words at
  S229.src:294-296; the version-pinned URL and immutable anchor correction ride
  this row.` — matches the S205/S206 correction-row contract (teaches begins
  `supersedes S0NN —`) and the contract's stated intent that S231
  append-only-corrects S229's located range/word count.
- Anchor check: `corpus/evidence/sources-r40/S229.src:294-296` contains
  "When a name is used in a code block, it is resolved using the nearest
  enclosing scope." — the 17-word quote S231 asserts; S229's own located quote
  (`:254-256`) was the imprecise one.
- `## Paths` at `:247` carries a "S231 → S230" reading-order entry,
  consistent with the correction chain.
- No old row's immutable cells (id/source/kind/tier/scope/anchor/teaches)
  differ; S229's row is intact and unmodified (S229's status/teaches were not
  edited in place — the correction rides S231 only).

## Inference

- Placement defect from r40 (S229 landed at EOF, repaired at T3 `ede486b7`)
  did not recur: S230/S231 sit inside the Registry before `## Paths`.
- Row arithmetic consistent with `evidence/census-start.txt` (229 rows at
  round start): 229 + S230 + S231 = 231 observed rows.

## Confidence

High — direct line-level reads of `corpus/SOURCES.md` and
`corpus/evidence/sources-r40/S229.src`.

## Remaining unknowns

None within scope. (I did not run `scripts/sources-census.sh`; this was a
read-only row-placement check.)
