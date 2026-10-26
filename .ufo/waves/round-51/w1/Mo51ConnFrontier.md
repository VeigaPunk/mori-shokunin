# Mo51ConnFrontier — Frontier mapping: MemAvailable entry (round 51, wave w1)

Seat: Mo51ConnFrontier (leaf, frontier mapping). Date: 2026-10-26. Lane: mori-shokunin.
Scratch: `/fast/scratch/hyaku/mori-r51/Mo51ConnFrontier/` (created; removed on finish).
Tool installs: none (no tool was installed or upgraded this seat).

## Assignment

Map where the C2 entry `corpus/knowledge/memavailable-estimate-r51.md` sits in the lane's
coverage (resource runway; FR8 thresholds; FR12 pressure); propose a README coverage-map row and
a dated Frontier note in the house style of the newest rows; name the next runway question the
lane cannot yet answer (one sentence + the sources it would need).

## Evidence read (read-only; all absolute paths)

- Contract: `mori-shokunin/.ufo/waves/round-51/contract.md` (C2 surface, P-C2, named limits).
- Entry: `mori-shokunin/corpus/knowledge/memavailable-estimate-r51.md` (opened; 21 claim rows,
  5 sources S492–S496, reading rules, boundaries; `coverage-map: resource runway (new ground; no
  FR row held it)` at `:10`).
- Rows: `mori-shokunin/corpus/SOURCES.md:271-275` (S492–S496; each row's used-by cell names
  `corpus/knowledge/memavailable-estimate-r51.md`; each lists its committed copy and sha256).
- Copies present: `mori-shokunin/corpus/evidence/sources-r51/` → `proc.rst.v7.2`,
  `show_mem.c.v7.2`, `meminfo.c.v7.2`, `mm_inline.h.v7.2`, `34e431b0.patch` (5 files).
- C2 at data: `mori-shokunin/.ufo/waves/round-51/evidence/c2-at-data.txt` →
  `C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok
  provenance=ok entailed=0 dissent=0 rev=87e0c374… failed=entailment` (exit 1).
- Row hashes: `mori-shokunin/.ufo/waves/round-51/evidence/c2-hashes-at-data.txt` (21 rows).
- Sweep: `mori-shokunin/.ufo/waves/round-51/evidence/sweep-memavailable.txt` —
  `si_mem_available`, `totalreserve`, `wmark_low`, `folio_is_file_lru`, `34e431b0`,
  `show_mem.c` → 0 occurrences in `SOURCES.md`/`knowledge/`/`SKILL.md` at `aa3af1ec`;
  `MemAvailable` occurs only as a read value (7 files), never defined; `merge/mori` sweep rc=1
  (no file).
- Census read sites: `mori-shokunin/corpus/knowledge/surfaces-r7.md:83` (host-ram arm:
  `host_mem_avail_pct` graded at `MORI_MEM_AVAIL_MIN_PCT` default 10 → `MEM_AVAIL_LOW` warn);
  `mori-shokunin/corpus/knowledge/observability-surfaces-r2.md:234` (same arm, r7 update).
- Dispatcher gate (contract C2 surface): seat spawns gated on `MemAvailable` (`MEM_MIN_GB`,
  `.scratch/goal-20261026-hyaku-run9.md` host limits).
- Frontier rows: `mori-shokunin/PROVINCE.md:44-57` (FR1–FR14) and `:321` (FR15);
  `mori-shokunin/corpus/README.md` Frontier table (`:339-354`) — FR8 (thresholds remain labeled
  local) and FR12 (event-driven pressure; one-shot system pressure read admitted round 24,
  resident watcher still frontier). Newest coverage-map additions: round 49 and round 50 sections
  (`corpus/README.md:677-696`, table `| coverage-map row | entry | ground | sweep |` + dated
  append-only note).

## Where the entry sits

1. **Resource runway (Core ground, not a new FR row).** The entry fills a definitional hole in
   the lane's Core resource-runway surface: the census reads `MemAvailable/MemTotal` and grades
   `MEM_AVAIL_LOW` off it (`surfaces-r7.md:83`, `observability-surfaces-r2.md:234`), and the
   orchestrator's dispatcher gates seat spawns on `MemAvailable` (`MEM_MIN_GB`), but before
   round 51 the lane held no source stating what the number is (sweep: `si_mem_available` and
   friends 0 occurrences; `MemAvailable` only as a read value). The entry's own coverage-map
   line says "resource runway (new ground; no FR row held it)" — so the row belongs in the
   README coverage-map additions table, not in the FR1–FR15 frontier table.
2. **FR8 (alert-threshold calibration) — touched, not advanced.** The entry's Reading rule 6
   mandates reporting any `MemAvailable` threshold as local, "as the lane already does for its
   other thresholds (FR8)"; the entry's Boundaries repeat that the dispatcher floor is the
   orchestrator's. FR8 stays open (thresholds remain labeled local); the entry adds the reason
   they must be: the number is a model (`min`-of-half/holdback rule), and the proc document
   says the model's accuracy varies by system.
3. **FR12 (event-driven pressure and CPU/IRQ PSI) — adjacent, untouched.** FR12's admitted
   ground is the one-shot system `/proc/pressure/*` read (`tools/mori-pressure.py`, round 24)
   and the still-frontier resident watcher / cgroup-scoped CPU/IO/IRQ pressure. The new entry is
   about what `MemAvailable` is (a static estimate of startable memory), not about stall-time
   probes; it reads no pressure file, adds no probe, and changes no census surface. The useful
   map note is that `MemAvailable` (model of startable memory) and PSI (measured stall time) are
   complementary runway readings and must not be conflated: a high `MemAvailable` does not prove
   low pressure and vice versa.

## Proposed README coverage-map row (append to `corpus/README.md` round-51 additions)

House style taken from the round-49/round-50 additions (`corpus/README.md:677-696`):
`| coverage-map row | entry | ground | sweep |` + dated append-only note.

```markdown
## Round-51 coverage additions

| coverage-map row | entry | ground | sweep |
|---|---|---|---|
| Resource runway — what /proc/meminfo's MemAvailable is at kernel v7.2: an estimate (si_mem_available()) of startable memory — free pages minus totalreserve_pages, plus the file-LRU page-cache and reclaimable kernel terms, each less min(half, summed low watermarks), clamped at zero — printed in kB beside MemFree; why Cached (which counts tmpfs/shmem pages parked on anon LRU lists) must never be rebuilt into the estimate | `knowledge/memavailable-estimate-r51.md` (S492–S496, opened 2026-10-26; S492 shares its URL and bytes with S082 at a different scope; S496 is the 2014 commit that added MemAvailable) | resource-runway Core ground (the census grades host `MemAvailable/MemTotal` — `surfaces-r7.md:83`, `observability-surfaces-r2.md:234`; the orchestrator gates seat spawns on `MemAvailable`); FR8/FR12 context: the threshold stays labeled local (FR8 open) and no pressure probe is added (FR12 untouched); states what the number is at v7.2, never a typical host value, and configures nothing (watermarks/swap are tsukuroi's; the dispatcher floor is the orchestrator's) | `si_mem_available`, `totalreserve`, `wmark_low`, `folio_is_file_lru`, `34e431b0`, `show_mem.c` → 0 occurrences in `SOURCES.md`/`knowledge/`/`SKILL.md` at `aa3af1ec`; `MemAvailable` occurs only as a read value (7 files), never defined (`.ufo/waves/round-51/evidence/sweep-memavailable.txt`) |
```

## Proposed dated Frontier note (append-only; no frontier row rewritten)

```markdown
Dated note (append-only, 2026-10-26): round 51 supplies the source behind the resource-runway
read — `MemAvailable` is the kernel's estimate (`si_mem_available()`), not a count of free
pages, and `MemFree + Cached` overstates startable memory because `Cached` includes tmpfs and
shmem pages that sit on anon LRU lists and never enter the estimate
(`knowledge/memavailable-estimate-r51.md`, S492–S496); no frontier row is rewritten (FR8 stays
open — the entry reports its threshold as local — and FR12 is untouched). Still frontier: the
estimate cannot be recomputed exactly from `/proc/meminfo` alone (`totalreserve_pages` is not
exported as one line), no host value is claimed as typical, and the Cached-vs-Shmem gap rule is
[INFERENCE] from the sources, not measured on this host.
```

## Next runway question the lane cannot yet answer

One sentence: **"Can the lane quantify, on this host, how much of the gap between `Cached` and
the estimate's file-LRU term is `Shmem`/swap-cache/buffers — i.e., how far below the naive
`MemFree + Cached` gate the dispatcher's `MemAvailable` floor actually sits — without triggering
any reclamation?"**

Sources it would need (all read-only, none currently owned as sources):
- the five frozen v7.2 copies already opened (S492–S496 — the formula, the Cached base, the
  anon-LRU placement);
- read-only live `/proc/meminfo` samples (allowed host read) to pair `MemAvailable`,
  `MemFree`, `Cached`, `Shmem`, `SReclaimable`/`KReclaimable` across the census's sampling
  window;
- `/proc/zoneinfo` and the kernel source that computes `totalreserve_pages`
  (`mm/page_alloc.c` / `include/linux/mmzone.h` — an unopened source) to bound what the
  estimate's reserve term adds, since it is not exported as one line;
- the orchestrator's dispatcher-floor file (`.scratch/goal-20261026-hyaku-run9.md`,
  `MEM_MIN_GB`) to frame the comparison.
A full accuracy measurement would require reclaiming cache — a mutation, prohibited — so the
lane can bound, never measure, the model error; any resulting host numbers are measurements,
never "typical" values (entry boundary).

## Verification

I did not run the frozen counters (not this seat's item); I read their receipts. The C2
receipt at the landed tip shows all 21 claims located with the only unmet arm being the recorded
non-L1 judgment arm (`failed=entailment`), which is this wave's attack item and is unaffected by
this mapping. UNVERIFIED: the exact rendered location of the round-51 additions section in
`corpus/README.md` (I propose appending after the round-50 additions, which is the file's last
section); the L1 integrates.

## Findings

- **MED — `corpus/README.md` coverage map has no row for the MemAvailable entry.** The entry
  exists, sources S492–S496 are mined and used-by-listed, and the copies are present, but the
  README coverage map (top table ends at r45; additions through round 50) does not name it.
  Proposed row above.
- **MED — `PROVINCE.md` / README Frontier tables: the entry must not be read as an FR advance.**
  The entry's coverage-map line says "no FR row held it"; it sits on Core resource-runway ground
  and touches FR8/FR12 only as context. Any integration that adds an FR row or claims an FR8/
  FR12 advance would overstate (the proposed row and note above keep FR8/FR12 open).
- **LOW — `corpus/knowledge/memavailable-estimate-r51.md` Reading rule 4 is unmeasured.** The
  "compare Shmem when Cached is large but MemAvailable is small" rule is marked [INFERENCE], not
  measured; the boundary correctly refuses a "typical" host claim. This is the named next runway
  question.
- **LOW — S492 duplicates S082's URL/bytes at a different scope.** The contract flags this as a
  W04 warning; the row states it. No action needed, but the row wording should keep the
  different-scope note (it does).
