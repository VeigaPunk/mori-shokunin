# RevC3Manifest — reviewer report

Item: independently enumerate
`git -C <lane> diff-tree --no-renames --no-commit-id --name-only -r d72ac167535229d737b9fa844513431d9a12f5ea`
and diff against `corpus/knowledge/inheritance-d72ac16-r42.md`.

## Method

- `git diff-tree --no-renames --no-commit-id --name-only -r d72ac16` → 165 paths (matches the
  manifest's own `recheck:` trailer).
- Extracted every fenced path line from the manifest → 145 unique paths, no duplicates.
- `LC_ALL=C comm` set difference, cross-checked with Python set arithmetic.
  (First pass used locale collation and produced garbage both directions; redone under
  `LC_ALL=C`. Locale artifact only — no repo issue.)
- `git diff-tree --name-status` for added-vs-modified; `git cat-file -e <commit>^:<path>`
  and `git show` for the modified members; `freeze-r41.txt` / `freeze-r42.txt` read for the
  freeze-set cross-reference.

## Acceptance criteria

| Criterion | Result |
|---|---|
| Every one of the 145 inherited paths named | **PASS** — 145 fenced entries, all unique. |
| Category counts 67/7/71 | **PASS** — seat_reports 67 (`.ufo/waves/round-40/w1/*.md`), r40_evidence_scratch 7, `.scratch/` 71. Sum = 145. |
| No path named that d72ac16 did not add | **PASS on membership; FAIL on "add" for one member** — every manifest path is among the commit's 165 touched paths (0 false names). But see F1: one member was *modified*, not added. |
| 20-path freeze set excluded | **PASS** — `commit(165) − manifest(145)` = exactly the 20 freeze paths, and they equal the manifest's own prose enumeration (15 under `.ufo/waves/round-41/`, `tools/mori-round41-calibration.py`, `tools/mori-sources-appendonly.py`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/conform-bindings-r41.md`). |

Supplementary claims verified: header `165` count ✓; "only `.scratch/round22/` was named at
the time (LOG.md round-41 entry)" ✓ (LOG.md:2358 names exactly that tree); freeze-section
fence empty by construction ✓.

## Findings

### F1 — Medium: `freeze-r40.txt` is miscategorized and falsifies two manifest claims

`.ufo/waves/round-40/evidence/freeze-r40.txt` sits in the manifest's
`r40_evidence_scratch` list ("round-40 evidence … same sweep"), i.e. inside the 145
described as "inherited **uncommitted** lane outputs swept in **unnamed**", under the
assertion the manifest "names no path the commit did not **add**".

`git diff-tree --name-status` shows it was status **M**, not A (one of only 4 M-paths in
the whole commit; the other three — `corpus/README.md`, `corpus/SOURCES.md`,
`tools/mori-sources-appendonly.py` — are correctly on the excluded freeze side).
`git cat-file -e d72ac16^:…` confirms the file existed at the parent (committed in
`8d3badd0`). The commit appended three lines pinning r41-closure fixtures
(`conform-v3-conjunct-gutted.py`, `conform-r39-conjunct-gutted.py`).

Worse, the path is **named**: `freeze-r41.txt` line 20 pins it
(`7f4cf799…64157f2  .ufo/waves/round-40/evidence/freeze-r40.txt`) — it is a member of
the r41 freeze set by the receipt's own enumeration, so it was neither uncommitted nor
unnamed at freeze time. The honest split is 144 unnamed uncommitted adds + 1 tracked,
receipt-pinned file whose working-tree amendment rode the freeze commit. The 145-count
and 20-exclusion arithmetic remain correct; the provenance story for this one member is
wrong on three axes (committed/not-uncommitted, named/not-unnamed, modified/not-added).

### F2 — Low: wrong enumeration citation for the freeze set

Manifest line 187: the 20-path freeze set is "enumerated in
`.ufo/waves/round-42/evidence/freeze-r42.txt`". That file (19 hash lines) pins round-42
artifacts plus a re-pin subset; it does **not** enumerate the round-41 freeze set. The 20
paths are actually enumerated in `.ufo/waves/round-41/evidence/freeze-r41.txt` (19 pinned
paths; `corpus/SOURCES.md` deliberately unpinned per the receipt's own P-C12 note, and
`freeze-r41.txt` itself added by the commit). LOG.md round-42 (≈line 2420) repeats the
same wrong `evidence/freeze-r42.txt` citation — same defect, second site.

### F3 — Cosmetic: bare `evidence/freeze-r41.txt` on line 8

"(named in `evidence/freeze-r41.txt` …)" — no such path at repo root; the file is
`.ufo/waves/round-41/evidence/freeze-r41.txt`. Resolvable in context but inconsistent
with the fully-qualified citation style used elsewhere in the document.

## Residual risk / verification gaps

- Path membership, counts, and exclusion are verified exhaustively (set equality, not
  sampling). Not verified — out of this item's scope: blob contents of the 145, whether
  the 67 seat reports are the *right* 67 seats for the r40 w1 wave, and the manifest's
  "benign content" characterization.
- F1 suggests the r41 freeze pinned `freeze-r40.txt` at hash `7f4cf799…` and then the
  freeze commit itself modified it to `f0ef0b01` — a self-amendment worth a line in the
  r41 records (may already be covered by a sibling seat; flagged, not adjudicated here).

## Tooling

None installed or updated (pacman paused host-wide; stock `git`, `comm`, `python3`
sufficed).
