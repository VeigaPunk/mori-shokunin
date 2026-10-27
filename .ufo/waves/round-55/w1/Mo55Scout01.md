# Mo55Scout01 — C1 extractor scope datawalk

## Findings

- **INFO — extractor input scope is the four named legacy entries, not every kernel-v7.2 citation in the corpus.** The frozen `count-c1.py` predicate states that SCOPE is every pointer its frozen extractor finds in ENTRIES at entering tip (counter lines 8–12); the explicit list is `oom-tracepoints-r47.md`, `system-pressure-r24.md`, `watchdog-identity-r31.md`, and `oom-victim-selection-r27.md` (counter lines 49–51). This matches contract.md C1's four-entry scope and its explicit exclusion example (contract C1 paragraph).

- **INFO — observed line-bearing and line-free examples.** In `oom-tracepoints-r47.md`, the header count cites `header lines 12, 34, 76, 118, 134, 150, 166, 183` (lines 16–18); the counter explicitly recognizes `header line(s)` tokens for that entry (count-c1.py lines 10–12). In `system-pressure-r24.md`, line-bearing citations include `psi.rst:36-38` and `psi.c:1710-1721` (lines 63–70). In `oom-victim-selection-r27.md`, cited line pointers include `kill.c:525-527,551-578` and `base.c:597` (lines 24–38). These illustrate line-pointer candidates, not an independent reproduction of the total 78.

- **INFO — excluded line-free citations are source IDs without `<file>:<lines>` tokens, not additional pointer rows.** The clearest declared case is `watchdog-identity-r31.md`: its source list at line 1 enumerates Linux v7.2 S163/S164/S165/S167 and other S-ids without line coordinates, and contract.md C1 explicitly says this entry has cited v7.2 kernel S-ids but no matching line pointers and contributes no pointer. Source-only references such as `oom-tracepoints-r47.md`'s “S478, p. 3016” (lines 61–65), `system-pressure-r24.md`'s bare S093 label (line 70), and `oom-victim-selection-r27.md`'s bare source identifiers in its source metadata (line 1) are not extracted as file-line pointers unless a qualifying filename-and-line or header-lines token appears.

- **UNVERIFIED — exact 78-group recomputation.** No counter execution or independent parser run was performed for this bounded datawalk. The source establishes the declared frozen rule and examples, but the exact extracted group set/count and duplicate handling remain the counter's unrerun computation.

No vote lines emitted (non-voter). No installations or source/production edits.

## Evidence / commands

- `read` of `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-55/contract.md` (C1 paragraph).
- `read` of `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-55/count-c1.py` (lines 5–20, 49–60).
- `read` of the four entries: `corpus/knowledge/{oom-tracepoints-r47,system-pressure-r24,watchdog-identity-r31,oom-victim-selection-r27}.md` (ranges cited above).
- Disk guard command: `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`; exit 0; reported free space `/tmp` 125.1G, `/var/tmp` 589.9G, `/fast/scratch/hyaku` 594.6G. No heavy work undertaken.

Severity: INFO / UNVERIFIED as labeled. Evidence paths and lines: contract.md C1; count-c1.py 5–20, 49–60; entry paths and lines above.