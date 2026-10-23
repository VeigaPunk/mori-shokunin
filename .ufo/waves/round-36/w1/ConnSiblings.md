measured 2026-10-23T12:04:24Z
# ConnSiblings — sibling-overlap scan (round 36, C1/C2)

Axes: freshness (C1) and operability (C2). Searched sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin` (read-only) plus `/home/vgpnk/Projects/shokunin/scripts/` for equivalents of (1) SOURCES drift re-fetcher and (2) SOURCES append-only gate. No sibling repo was edited.

## Hits — C1 (drift / source re-check)

1. `kake-shokunin/scripts/source_recheck.py:1` — round-36 C1 "source re-check audit" for recorded fetches (manifest + body files), offline, classify quote match. Same vocabulary (`unavailable`, quote match) but different contract surface (manifest-driven recorded fetch, not SOURCES rows with committed copies). **Cite** as prior art for offline quote-match logic; do not reuse (different input contract; mori's tool reads `corpus/SOURCES.md` and committed copy files under `corpus/evidence/sources-r<N>/`). Adjacency risk: low — kake owns `source_recheck*`; no shared path. (`source_recheck_selftest.py`, `source_recheck_hardening_selftest.py` beside it.)
2. `kasegi-shokunin/corpus/instruments/source-recheck.py:1` — rechecks pinned quotes against checked-in snapshots (`sha256` of local files), emits `<id> <status>`. Local-only, no network/fetch. **Cite** only; no reuse (no live fetch, no excerpt/drifted classification). Adjacency risk: low.
3. `tabi-shokunin/scripts/check-sources.mjs:1` and `kumitate-shokunin/scripts/sources-check.mjs:1` — registry validators (schema/enums/citations), not drift re-fetchers. **Cite** for shared SOURCES-CONTRACT-v1 row shape only. Adjacency risk: none for C1.
4. `tsukuroi-shokunin/tools/check-freshness-r17.py:1` — narrow append-only freshness-recheck gate for a JSON registry; not a SOURCES-row fetcher. **Cite** only. Adjacency risk: none.

## Hits — C2 (append-only gate / deleted rows)

5. `kama-shokunin/tools/sources-append-only.py:63` — `MUTABLE_CELLS = {"status","recheck","used-by"}`, `IMMUTABLE_CELLS` (line 67), `parse_registry()` (line 148), deleted-row detection via id diff, immutable-cell diff, superseder detection. Direct conceptual overlap with mori C2 (append-only, deleted rows, superseding rows). **Cite** as prior art / cross-check; do not reuse (different output contract: mori must print `changed <id> superseded_by=...`, `deleted <id>`, and the `appendonly_violations=...` summary with `round_changed`; kama's exit/labels differ). Adjacency risk: **high** — kama owns the `sources-append-only` surface; mori's tool name/contract must remain distinct to avoid shadowing. (`echo-recheck.py` in same dir is unrelated.)
6. `kotoba-shokunin/verifiers/check_sources_append_only.py:30` — `PERMITTED = ("status","recheck","used-by")`, `compare()` (line 64), `scan()` over git history (line 99), deleted-row breach + in-place immutable breach. Same overlap as #5. **Cite**; do not reuse. Adjacency risk: **high** — kotoba owns this verifier path; mori must keep its own `tools/` location and contract labels.
7. `tsukuroi-shokunin/tools/check-appended-notices.py:1` and `check-recheck-commands.py:1` — append-only notice/recheck-command guards, not SOURCES-row append-only. **Cite** only. Adjacency risk: low.

## Fleet-level context (not a tool equivalent)

8. `scripts/sources-census.sh:1` — fleet-wide census/validate/overdue/shared over `corpus/SOURCES.md` (SOURCES-CONTRACT-v1). Read-only census, no fetch, no deleted-row history diff. **Cite** for row-shape/fleet codes (E01–E12, W02/W03); mori's C1/C2 do not conflict. Adjacency risk: none — fleet owns census; mori consumes, never re-implements census.

## Recommended disposition for L1

- Build mori's own `tools/mori-source-drift.py` and `tools/mori-sources-appendonly.py` per the frozen contract; do not import or shell out to siblings.
- Cite kake (quote-match offline logic) and kama/kotoba (append-only comparison shape) in the round lesson as prior art; keep mori's output labels/exit codes distinct.
- No adjacency conflict requires a rename, but mori must not place files under sibling lanes or reuse their paths.

VERDICT: overlap
</content>
