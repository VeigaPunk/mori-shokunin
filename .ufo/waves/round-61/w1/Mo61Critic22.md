# Mo61Critic22 — cheapest-met attack on C2 (count-c2.py)

Scope: read-only over the lane; all counter runs executed against fixture git repos in
`/fast/scratch/hyaku/mori-r61/Mo61Critic22/fx/` (cleaned after this report was written). Frozen
counter copied byte-identical (sha256 `82d0fee6…` both sides) and invoked as
`python3 count-c2-frozen.py <rev> --repo <fixture> --scratch <scratch>`.

## Verdict

C2's frozen counter is satisfiable by a ledger that performs **zero real recheck** — the
strongest counterexample is an all-`changed` ledger whose quotes are arbitrary 5-word
windows of the v7.3 copies at self-chosen locations, with one mega SOURCES.md row. It prints
`C2=met … failed=none` rc=0. This is a fixable defect: the predicate measures ledger *shape*,
not recheck truth, because (a) `moved`/`changed` never consult the anchor's file or the
anchor's declared range, and (b) no v7.2 baseline exists in the repo, so no verdict is
falsifiable.

---

## F1 — `changed`/`moved` rows are content-free; whole-file spans accepted (KILL, demonstrated)

count-c2.py:148-149 — `fname, start, end = (span_of(anchor) if status == "same" else span_of(loc))`.
For `moved`/`changed` the lookup location is **the row's own `loc` cell**, which the writer
chooses freely: any file, any in-bounds range, unrelated to the anchor. The counter then
requires only that the quote be a byte substring of `lines[lo-1:hi]` of that file (:154-160).
Nothing ties the quote to the anchor's file, subject, or v7.2 line range.

Fixture repoM2 (`git -C …/fx/repoM2`, rev `828ed33d30e469a6ac3d48155f3af499cbf5c893`): the real
source entry (47 enumerated pointers) + 47 rows all `changed`; 34/47 rows quote a *different*
file than their anchor names; quotes are 5-word sliding windows from a handful of lines
(6 rows collapse onto `psi.rst:10`, 6 onto `cgroup-v2.rst:10`); one mega SOURCES.md row naming
all six copies. Sample rows written verbatim by the fixture:

```
| psi.rst:60-65 | changed | kernel-parameters.txt:2 | `AGP (Accelerated Graphics Port) is` |
| psi.rst:36-38 | changed | psi.c:3 | `stall information for CPU, memory` |
| Kconfig:730-731 | changed | psi.rst:10 | `memory or IO devices are` |
```

Counter output (frozen bytes):

```
C2=met pointers=47 rows=47 same=0 moved=0 changed=47 quotes_ok=47 spans_ok=47 sources=4 failed=none rev=828ed33d30e469a6ac3d48155f3af499cbf5c893
rc=0
```

Whole-file escalation (fixture repoW, rev `5752484bbd717e3d16baf75efe26f66ba59c490d`): `loc =
<file>:1-N` per row makes the location cell a pure no-op — also `C2=met`, rc=0.

Corollary: an all-`same` ledger is the *only* arm with teeth, and its teeth are shallow —
`same` requires any ≥5-word quote inside `lines[anchor_lo-1:anchor_hi]` of the v7.3 copy, but
there is no v7.2 copy committed to compare against, so `same` cannot distinguish "unchanged"
from "rewritten". Fixture repoSame confirmed 33/47 anchors pass `same` with arbitrary v7.3-range
quotes; the other 14 only failed because their v7.3 ranges hold <5 words (e.g. `psi.c:1712`
= `if (psi_enable) {`), forcing `moved`/`changed` — which F1 shows are free.

**Impacted axis:** freshness — the counter certifies a "recheck" that need not have happened.
**Smallest safe correction:** pin the six v7.2 copies alongside the v7.3 ones (their sha256
prefixes are already in SOURCES.md rows S090–S095) and bind the verdict to both: `same` →
quote is a byte substring of the v7.2 *and* v7.3 ranges; `moved` → quote is a substring of the
v7.2 anchor range and of the v7.3 stated loc; `changed` → require `fname == anchor's file` at
minimum (one-line: reject `loc_bad` when the loc file differs from the anchor file).

## F2 — source-side enumeration is unpinned and shrinkable to the floor (KILL, demonstrated)

`SOURCE_ENTRY` is read live at the measured rev (count-c2.py:94) with no sha check — unlike the
six copies, which are sha256-pinned (:110-115). The work-list is therefore **not frozen**: the
enumerated pointer set can shrink (fewer required rows) or grow (injected orphan rows that
fail a correct ledger) between freeze and measurement.

Fixture repoS (rev `1f23db88600b96ba0494d7336a58431ca1ce7a8e`): rewrote seven `psi.rst:N-M`
mentions in the entry to `psi.rst lines N-M` (regex-invisible). Enumerated set dropped
47 → 40, and a 40-row all-`changed` ledger passed:

```
pointers after rewrite: 40
C2=met pointers=40 rows=40 same=0 moved=0 changed=40 quotes_ok=40 spans_ok=40 sources=4 failed=none rev=1f23db88600b96ba0494d7336a58431ca1ce7a8e
rc=0
```

So the floor of 40 permits a silent 15% coverage cut (47→40). The poison direction is equally
live: any later prose edit mentioning `psi.c:NNN` in the entry becomes a mandatory row —
`set(anchor_list) != pset` (:127-133) — so a legitimate "rechecked" annotation can brick a
correct ledger or be exploited to force rows.

**Impacted axis:** freshness/calibration. **Smallest safe correction:** pin the source entry's
sha256 at freeze (same mechanism as `PINS`), or freeze the enumerated pointer list itself in
the counter; keep `pointer_floor` only as a sanity bound, not the work-list definition.

## F3 — the frozen regex under-enumerates the entry's real prose anchors (coverage gap)

`NAMES` only matches `file:N` or `file:N-M` with an explicit filename. Verified on the frozen
entry (sha256 `26b22ddf…`, unchanged entering→HEAD, blob `21d60f45…`): 47 enumerated vs 52
filename-prefixed anchors — five are comma-continuations the regex cannot see
(`psi.c:408-411`, `psi.c:572`, `psi.c:1545`, `psi.c:1550`, `psi_types.h:57-70`; occurrences
`psi.c:342-360,408-411,551,572` line 19, `psi.c:1540,1545,1550,1686` lines 89/148/241,
`psi_types.h:41-49,57-70` line 110). Four more anchors are bare-colon continuations with an
implied filename (`:1083-1087`, `:1215-1221`, `:1911-1915`, `:2171-2175` at lines 143/242 — the
S092 cgroup pressure-file sections). Total ≥9 of ~56 real prose anchors (~16%) never require a
row. The contract's wording ("one ledger row per v7.2 line pointer the counter enumerates")
absorbs this, but the *claim* ("the entry's prose anchors rechecked") overstates the check.

**Impacted axis:** freshness. **Smallest safe correction:** extend `NAMES` to expand
comma/bare-colon continuations, or state in the contract that the work-list is regex-defined.

## F4 — SOURCES.md binding collapses to one line and skips the "opened this round" check

The registry check (:173-180) is substring-level: a line needs `corpus/evidence/sources-r61/{f}`
+ `| S` + `| mined |` + `psi-v73-recheck-r61.md`. Fixture M2 passed all four cited files with a
**single** row whose source cell names all six copies — the contract requires "each cited copy
has a SOURCES.md row opened this round" but the counter checks neither the `opened` date, row
uniqueness per copy, nor the id's novelty.

**Smallest safe correction:** require a distinct `| S\d+ |` row per cited file and compare the
opened cell to the round date, not substring presence.

## F5 — contract/counter divergences (documentation-level)

- Contract's frozen met line cites `sources>=4 rows_src=ok provenance=ok` — `fmt()` (:191-196)
  never emits `rows_src`/`provenance` tokens and prints `same/moved/changed`/`rev` the contract
  omits; a literal receipt match cannot succeed.
- Contract says `changed` quote may be "anywhere in the copy"; the counter restricts it to the
  stated loc range (stricter, harmless direction but a misdescribed predicate).
- Counter enforces a 5-word quote minimum the contract does not state (`5 <= words <= 25`).
- `ROW` (:44-46) has no trailing `$` — a row with extra trailing cells still matches; and rows
  inside code fences/comments count, since matching is context-blind.
- `res["spans_ok"]` (:147) increments before the location check, so the printed `spans_ok`
  counts quote-shape, not located quotes.

## Cheapest met state (answer to the seat question)

With the frozen entry: **47 rows, all `changed`, loc = arbitrary in-bounds file ranges (up to
`file:1-N`), quotes = distinct ≥5-word windows of those ranges, ≥4 cited files, one SOURCES.md
line, three provenance header lines** — ~50 lines, no byte of v7.2 consulted. With a
source-entry edit permitted at measure-time: **40 rows** (floor). The only arm the counter can
truly verify is `same`, and even it is unfalsifiable without a committed v7.2 baseline.

Tooling: none installed. Fixture git used throwaway identity `t <t@t>` inside scratch repos only.
Scratch `/fast/scratch/hyaku/mori-r61/Mo61Critic22/` removed before yielding.
