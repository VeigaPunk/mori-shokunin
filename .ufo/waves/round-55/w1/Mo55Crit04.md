# Mo55Crit04 — C1 change-semantics critic review (round 55, wave w1)

Seat: critic (non-voting). Scope: the 7 moved / 2 changed pointer rows in
`corpus/knowledge/kernel-v7.3-recheck-r55.md`; judge whether claim meaning changed across the
v7.2→v7.3 transition and whether any current `holds` disposition should be `stale`.
No vote lines emitted (critic seat).

## Method

- Read the frozen counter `.ufo/waves/round-55/count-c1.py` (`derive`, lines 213–243) to confirm
  the mechanical semantics: `same` = byte-identical block at same location; `moved` = byte-identical
  block at a new location; `changed` = v7.2 block does not occur anywhere in v7.3 (content edited or
  deleted).
- Independently re-extracted each of the 9 non-same rows' v7.2 and v7.3 blocks from the pinned
  evidence copies and byte-compared them (`diff`), then verified enclosing function/section context
  on both sides.
- Verified each evidence file's sha256 against the frozen pins in `count-c1.py` `COPIES`:
  all 10 files underlying the 9 rows match the pinned hashes exactly
  (mm_page_alloc v7.2 `439ae8ec…`, v7.3 `315ef97b…`; kernel_fork v7.2 `359882ea…`, v7.3 `fa32ca5a…`;
  cgroup-v2 v7.2 `a9433bb0…`, v7.3 `2750c11a…`; kernel-parameters v7.2 `23b1a690…`, v7.3 `b5a13c03…`;
  proc.rst v7.2 `e760f716…`, v7.3 `bc178ff5…`).
- Cross-read the citing claims in the three knowledge entries to test whether each entry claim
  survives the located change.

## Evidence per row

### Moved (7) — all byte-identical content; holds confirmed

1. `b50f210b822a` — `mm/page_alloc.c:4630 → 4689` (S527). Cited by
   `corpus/knowledge/oom-tracepoints-r47.md:25` as `should_reclaim_retry` at page_alloc.c:4630.
   Block (`trace_reclaim_retry_zone(z, order, reclaimable, …)`) byte-identical at both locations;
   enclosing function `should_reclaim_retry(gfp_t gfp_mask, unsigned order, …)` confirmed at
   v7.2:4581 and v7.3:4640. Claim (allocator's per-zone reclaim-retry decision before an OOM)
   unchanged. **holds correct.**
2. `db108c1ad61c` — `mm/page_alloc.c:4265 → 4311` (S527). Cited by oom-tracepoints-r47.md:31 as
   `should_compact_retry` at page_alloc.c:4265. Block (`trace_compact_retry(order, priority, …)`)
   byte-identical; enclosing function `should_compact_retry(...)` at v7.2:4202 and v7.3:4248.
   **holds correct.**
3. `eee4454705c0` — `Documentation/admin-guide/kernel-parameters.txt:5505-5507 → 5540-5542` (S532).
   Cited by `corpus/knowledge/system-pressure-r24.md:127` as the `psi=` boot-parameter doc
   (S094). Block ("psi= [KNL] Enable or disable pressure stall information / tracking. /
   Format: <bool>") byte-identical. **holds correct.**
4. `edd8b8c361b4` — `Documentation/admin-guide/cgroup-v2.rst:1215-1221 → 1240-1246` (S533).
   Cited by system-pressure-r24.md:143 (F9) as the `cpu.pressure` section. Block byte-identical
   ("A read-write nested-keyed file. … Shows pressure stall information for CPU. …"). **holds correct.**
5. `9a8d29e96280` — `Documentation/filesystems/proc.rst:1811-1812 → 1812-1813` (S502). Cited by
   `corpus/knowledge/oom-victim-selection-r27.md:66` as proc.rst giving the exported 0–2000 range
   (S082). Block ("effectively in range [0,2000].") byte-identical. **holds correct.**
6. `07a985363937` — `Documentation/admin-guide/cgroup-v2.rst:1450-1466 → 1477-1493` (S533).
   Cited by oom-victim-selection-r27.md:68 as memory.oom.group "sparing only tasks at -1000"
   (S092). Block byte-identical (the whole memory.oom.group section incl. the -1000 exception
   paragraph). **holds correct.**
7. `4eea9d9f5ae5` — `kernel/fork.c:1768-1769,1949-1966 → 1795-1796,1976-1993` (S534). Cited by
   oom-victim-selection-r27.md:84 ("Inheritance. fork copies both the value and its floor",
   S148). Both blocks byte-identical: `sig->oom_score_adj = current->signal->oom_score_adj;` /
   `sig->oom_score_adj_min = …` at 1768-1769 → 1795-1796, and the full `copy_oom_score_adj` body
   at 1949-1966 → 1976-1993. **holds correct.**

### Changed (2) — one-word documentation drift; holds still correct, caveat noted

8. `02b8d2d11094` — `Documentation/admin-guide/cgroup-v2.rst:1911-1915 → 1938-1942` (S533),
   the `memory.pressure` section. Precise diff of the two 5-line blocks:
   `2c2 < A read-only nested-keyed file. --- > A read-write nested-keyed file.`
   Only that one word differs. Entry claims citing this pointer
   (system-pressure-r24.md:43, :143 (F9), :242) assert only that each controller's pressure file
   has its own section at these line ranges. No claim anywhere in the entry asserts that
   `memory.pressure` is read-only (grep for read-only/read-only/read-write across the entry finds
   only the "Host observation (… read-only)" method note at line 2). The section still exists at
   v7.3; the location claim survives. **holds correct**, but the citation's underlying text changed
   by one word — voters should not describe this row as textually unchanged.
9. `77bd396cffd3` — `Documentation/admin-guide/cgroup-v2.rst:2171-2175 → 2202-2206` (S533),
   the `io.pressure` section. Identical one-word diff: `read-only` → `read-write` on line 2 of the
   block. Same citing claims (lines 43, 143, 242); no read-only claim exists in the entry.
   **holds correct**, same caveat as row 8.

## Counterexample tested (strongest available)

The strongest available counterexample to the ledger's all-`holds` disposition is the changed pair:
the kernel documentation flipped `memory.pressure` and `io.pressure` from "A read-only
nested-keyed file." to "A read-write nested-keyed file." between v7.2 and v7.3. If the entry had
claimed these files are read-only (or had cited the section *for* its read-only characterization),
the disposition would have to be `stale` and the claim would need a v7.3-based rewrite. Local
evidence rejects the counterexample: the entry's claims citing these two pointers use them purely
as section locators ("each controller's pressure file with its own section and line range"),
a claim that remains true at v7.3. The drift is a real semantic change in the cited text but is
orthogonal to every claim the lane entries make over these pointers.

For the 7 moved rows the strongest counterexample would be a content-preserving context change
(e.g., function rename or section repurposing around an identical block). Tested and rejected:
enclosing functions/sections verified on both sides for all 7 (details above); the identical
blocks sit in the same named functions/sections at v7.3.

## Conclusion

- All 7 `moved` dispositions are semantically sound: content byte-identical, context preserved,
  citing claims unaffected.
- Both `changed` dispositions are semantically sound for the entry's actual claims (section-location
  claims), with the one-word `read-only`→`read-write` drift recorded as a caveat for voters.
- **No current `holds` among the 9 non-same rows should be `stale`.**
- Frozen pins for every evidence file underlying these 9 rows match `count-c1.py` `COPIES` exactly;
  the semantic review stands on the pinned bytes.
- Mechanical layer (already reported by the L1 data read): scope=78 rows=78 matched=78
  status_ok=78 line_ok=78, pins/provenance/source_rows ok, 0 votes, exit 1 — this seat adds the
  semantic layer only; it does not re-litigate the mechanical checks.

## Findings

- **informational** — `02b8d2d11094` / `77bd396cffd3` (memory.pressure, io.pressure sections):
  v7.2→v7.3 documentation drift `read-only` → `read-write` (evidence:
  corpus/evidence/sources-r55/Documentation_admin-guide_cgroup-v2.rst.v7.2:1912 vs .v7.3:1939;
  v7.2:2172 vs v7.3:2203). Dispositions `holds` remain correct for the lane's section-location
  claims; voters must not call these rows textually unchanged.
- **informational** — all 7 moved rows re-verified byte-identical with enclosing context preserved
  (evidence: diff output reproduced in seat scratch; pins matched to count-c1.py COPIES).
- **none** — no stale-among-holds defects found in the 9 non-same rows.
