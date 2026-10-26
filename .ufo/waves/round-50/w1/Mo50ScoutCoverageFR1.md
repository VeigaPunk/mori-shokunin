# Mo50ScoutCoverageFR1 — coverage and adjacency scan for `oom-memcg-stat-r50.md`

Scope: read-only. Nothing in the lane was edited; no scratch dir was created, so none needs removal. No kernel log message text was read.

## Verdict (answers first)

- **New ground for mori: yes, partly.** The memcg OOM *dump block* is not held anywhere in the lane. FR1 is the row it belongs to (ground: kernel OOM event-time attribution), and the entry advances the *what the kernel prints* half of FR1. It closes nothing.
- **Sibling ownership: none contests it.** tsukuroi holds adjacent host evidence (live `memory.stat` readings, global-OOM dump instances, the `Memory cgroup out of memory` label). No sibling holds the memcg block format, the `memory.stat` key meanings or the `memcontrol.c` source. Adjacent, not owned.
- **Must link:** `kernel-oom-line-attribution-r12.md`, `oom-tracepoints-r47.md`, `oom-victim-context-r41.md`, `census-cgroup-levels-r45.md` (details below). Also `oom-kill-counter-kernel-only-r12.md` and `oom-evidence-loss-r38.md`.
- **Boundaries line:** see the last section.

## 1. Lane coverage (observed)

### corpus/README.md

- **FR1 Frontier row** (`corpus/README.md:341`, same text as `PROVINCE.md:44`): "Kernel OOM event-time attribution and fleet correlation". First evidence is `knowledge/kernel-oom-line-attribution-r12.md:10-16` and `audit-r11.md:203-204`. The boundary says structured journal notices advanced in round 13, kernel victim/summary token validation and fleet task correlation remain frontier, and catalog-ID records are not authenticated unique kills.
- **Latest FR1 touches in the map:**
  - Round-42: FR1 gains `oom-evidence-loss-r38.md` and `oom-victim-context-r41.md`.
  - Round-45: `census-cgroup-levels-r45.md`, which states "no FR1 or FR12 advance".
  - Round-49: `journal-reach-r49.md` (S485–S488).
  - Round-47 covers FR13 only (`oom-tracepoints-r47.md`).
- **S489–S491 are not yet in `corpus/SOURCES.md`.** The last row is S488. The L1 must add them.

### Lane-wide grep for the memcg block ground

Command, run in `corpus/` over `knowledge lessons SOURCES.md README.md ../PROVINCE.md ../SKILL.md`:

```
grep -rnE 'Memory cgroup stats|memory_stat_format|failcnt|mem_cgroup_print_oom_meminfo|mem_cgroup_print_oom_context|memory\.stat' ...
```

Result: **one hit**, `knowledge/kernel-oom-line-attribution-r12.md:1`, which is the `source:` line. It mentions `memcontrol.c`, not the block. There is no lane text on `Memory cgroup stats for <path>:`, `memory_stat_format`, the failcnt line, or any `memory.stat` key.

### What the four named entries hold

| Entry | Holds | Gap the new entry fills |
|---|---|---|
| `kernel-oom-line-attribution-r12.md` | The `oom-kill:constraint=…,oom_memcg=…,task_memcg=…,task=…,pid=…,uid=…` summary and the `Killed process` line, as event-time attribution tokens. Cites S003 `oom_kill.c:447-453,945-947` and S004 `memcontrol.c:1820-1826`. S004 is a master commit copy, not v7.2. Rule: token-only, no `MESSAGE` echo. | It never shows the usage/limit/failcnt lines or the `Memory cgroup stats` block. The new entry gives a v7.2 copy (S490). |
| `oom-tracepoints-r47.md` | The eight `oom` trace events, v7.2 tag copies pinned by sha256. Only `mark_victim` names the victim (pid, comm, uid). No event carries a cgroup path. | A different channel (tracefs, root-only, FR13). The new entry is the printk dump channel. |
| `oom-victim-context-r41.md` | Abstract-only claim that kernel victim selection has no container context. It says nothing about a host running one workload per cgroup. | The memcg dump is the kernel record that *does* name the cgroup (`oom_memcg=`, `task_memcg=`, the stats path). The entry can state what that record carries without contradicting r41. |
| `census-cgroup-levels-r45.md` | `memory.events` is hierarchical and `.local` is not, quoted from the cgroup-v2 doc. The census row's counting scope is silent. | `memory.events` counts. The new entry covers `memory.stat` keys and the OOM printk, a different file. It must not restate the events/local distinction. |

- **Also relevant:** `oom-kill-counter-kernel-only-r12.md` (`oom_kill` moves only at the kernel victim site), `oom-victim-selection-r27.md` (`memory.oom.group`, victim choice), and `oom-evidence-loss-r38.md` (absence of a record is not absence of an OOM).

## 2. Sibling grep (read-only; mori skipped)

Command and output:

```
$ cd /home/vgpnk/Projects/shokunin; grep -rlE 'memory\.stat|Memory cgroup stats|failcnt' /home/vgpnk/Projects/shokunin/*-shokunin/corpus /home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md | grep -v '/mori-shokunin/'
/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/kill-event-deep-r8.md
/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/memory-arm-ver-s8.md
/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md
/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/kill-oom-boundary-r33.md
exit=0
```

These are all tsukuroi. The kumitate, kama, kagi, souji and other sibling corpora and PROVINCEs have zero hits.

A narrower pattern, `memory\.stat|Memory cgroup stats|failcnt|memory_stat_format|Killed process|mem_cgroup_print_oom`, over the four hits shows what each one holds:

| tsukuroi file | What it holds | Overlap |
|---|---|---|
| `oom-event-plane.md:266-271` | Live slice `memory.stat` readings (`pswpin`/`pswpout`, `pgscan_direct`, `anon`/`file`/`slab`) as swap-thrash evidence. Also the rule that `memory.current` includes page cache (`:271`). | These are host readings, with no key glossary and no OOM printed block. `Killed process` is quoted only for a *global* OOM victim (`:67`). |
| `kill-event-deep-r8.md:30,183,333` | The count of `Out of memory: Killed process` against `Memory cgroup out of memory` lines (1 versus 0 in 13 boots). Another slice `memory.stat` reading. | Counts and an instance only. |
| `memory-arm-ver-s8.md:58,64,146` | The census arm's `memory.stat` `pswpin`/`pswpout` reading. | Census tooling, not kernel print. |
| `kill-oom-boundary-r33.md:13,29,36` | Boundary table (OS/journal evidence versus fleet). S182 (`oom_kill.c`, `Out of memory` versus `Memory cgroup out of memory`, lines 1168-1170, victim record 945-951). | The only sibling touch of the global-versus-memcg label. Source overlap on `oom_kill.c` at v7.2 (S119/S149/S182 in tsukuroi `SOURCES.md`). |

Also checked: `grep -rlE 'dump_header|mem_cgroup_print_oom|oom_kill\.c|memcontrol\.c'` over sibling corpora hits only tsukuroi (`kill-event-deep-r8`, `oom-event-plane`, `memory-pressure-r25.md/.json`, `kill-oom-boundary-r33`, lessons r25/r29/r33, `SOURCES.md`). Only the `oom_kill.c` rows carry real source overlap: tsukuroi cites the same file at v7.2 as S119, S149 and S182. **`memcontrol.c` appears in no tsukuroi `SOURCES.md` row.** The only `SOURCES.md` hits for it are mori's own S004.

**Province context:** tsukuroi `PROVINCE.md:30` says host memory and kill-event measurements support OS triage. Its `ADJ-04` row routes host pressure needing fleet or wave correlation to mori. Mori `PROVINCE.md:66` already records tsukuroi as the only sibling with `memory.events`/`systemd-oomd` ground, "adjacent host diagnosis, not contested fleet ownership".

## 3. Ownership and source overlap notes

- **No sibling owns the same ground.** The kernel's memcg OOM print format, the `memory.stat` key glossary (units: bytes for most keys, event counts for `pg*`/`workingset_*`) and `memcontrol.c` have no sibling coverage. The tsukuroi hits are live readings or label counts.
- **Source overlap:** S490 (`memcontrol.c`) is new to the fleet. S491 (`oom_kill.c` at v7.2) is the same URL as tsukuroi S119, S149 and S182. This is the same pattern as mori's own S003, S149/S150 and S182 rows. Sources are not merged across lanes (the existing rule at `PROVINCE.md:90`). Mori's row should be its own and may cite the tsukuroi overlap.
- **Honest limits [UNKNOWN]:** I did not open `corpus/evidence/sources-r50/*`, `count-c2.py` or `contract.md`, which the seat brief did not ask for. I did not verify the kernel print format myself. Everything above about what the kernel prints comes from the lane's and tsukuroi's existing entries, not from the v7.2 copies.

## 4. Links the entry must carry

1. `knowledge/kernel-oom-line-attribution-r12.md`. It supplies the summary and victim tokens. The new entry adds the usage/limit/failcnt lines and the stats block, and S490 gives v7.2 line numbers where r12 cites a master copy.
2. `knowledge/oom-victim-context-r41.md`, because the memcg dump is the one kernel record that does carry a cgroup path.
3. `knowledge/oom-tracepoints-r47.md`, because the tracepoint channel names the victim but no cgroup, while the printk channel names the cgroup.
4. `knowledge/census-cgroup-levels-r45.md`, as a different file (`memory.stat`, not `memory.events`) with a shared hierarchical-versus-local reading discipline. Do not restate its findings.
5. `knowledge/oom-kill-counter-kernel-only-r12.md` for how a memcg OOM kill moves the `oom_kill` counters at the victim site.
6. `knowledge/oom-evidence-loss-r38.md` for the point that a missing block does not mean no OOM.
7. Optional, with the correct path (`../../tsukuroi-shokunin/corpus/knowledge/kill-oom-boundary-r33.md` and `oom-event-plane.md`), for the global-versus-memcg label and the live slice readings, cited as adjacent only.

## 5. Coverage-map and Frontier handling for the L1

- **Coverage-map row:** add a "Round-50 coverage additions" block. Ground: "FR1 the kernel's memcg OOM print block and `memory.stat` key meanings". The map has the OOM summary token (r12) and `memory.events` (r45) but not this.
- **FR1 Frontier row:** do not rewrite it. Add a dated append-only note like the round-49 one, saying the entry advances the FR1 "what the kernel prints" half only.
- **Do not claim:** FR1 closure, kernel victim attribution, fleet correlation, or any probe or census change. The entry is knowledge only.

## 6. The Boundaries line

> Boundaries: this entry records only what Linux v7.2 `mm/memcontrol.c`, `mm/oom_kill.c` and the cgroup-v2 page say the kernel prints and what each `memory.stat` key means; it reads no kernel log text, adds no probe or census change, claims neither victim attribution nor a fleet-cause finding (FR1 event-time attribution and fleet correlation stay Frontier), and leaves host OS memory diagnosis and live `memory.stat` readings to tsukuroi.

## Findings

- **MED**: `corpus/SOURCES.md` has no rows for S489 (cgroup-v2 v7.2 page, staged S533 renumbered), S490 (`memcontrol.c` v7.2) or S491 (`oom_kill.c` v7.2). The last row is S488, so the L1 must append them before the entry cites them.
- **MED**: `knowledge/kernel-oom-line-attribution-r12.md:1,12` cites `memcontrol.c:1820-1826` from a master commit (`c03c1a14…`), not the v7.2 tag. The new entry's v7.2 line numbers may differ, so it should say so rather than reuse the r12 numbers.
- **LOW**: `oom_kill.c` at v7.2 is already tsukuroi S119, S149 and S182. Mori S491 is a separate lane row with the same URL. Cite the overlap; do not merge the rows.
- **LOW**: `census-cgroup-levels-r45.md` carries "no FR1 or FR12 advance". The new entry must not reword it. Only add the FR1 "what the kernel prints" half in the round-50 map block.
- **LOW**: nothing in the lane or siblings defines `memory.stat` units or keys. Any units claim in the new entry is unsupported until the cgroup-v2 v7.2 quote backs it.
