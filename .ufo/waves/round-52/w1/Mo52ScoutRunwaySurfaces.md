# Mo52ScoutRunwaySurfaces — per-surface reconnaissance of resource runway at 8524904a

Scope: every lane instrument and knowledge entry at `8524904adb25e44f24d9f25aac7eae909625c18c` that reads
`/proc/meminfo`, `/proc/sys/vm` or `/proc/pressure`, what it reads and prints, which runway question it answers,
and the gaps after this round's entry. Read-only; no scratch files kept (the scratch dir was created empty and
removed). No pacman, no sysctl write, no tool installed.

## Commands run (all read-only)

- `git -C <lane> grep -n -E 'meminfo|/proc/sys/vm|pressure/memory|MemAvailable|CommitLimit' 8524904a -- tools corpus/knowledge SKILL.md` → rc 0, ~80 lines.
- `git grep -n -i -E '/proc/pressure|proc/sys|memory\.pressure|memory\.high|memory\.max|memory\.events|swap|vmstat|zoneinfo|overcommit|Committed|min_free|watermark|psi_' 8524904a -- tools/mori-census.sh tools/mori-job-runway.py tools/mori-pressure.py tools/mori-oom-killers.py`
- `git grep -n -i -E 'SwapFree|SwapTotal|swappiness|zswap|zram|oom_score|vm\.|min_free_kbytes|mem_avail|MemFree|memory\.swap|memory\.low|memory\.min|hugetlb|vm_enough' 8524904a -- tools/*.py tools/*.sh SKILL.md`
- `git grep -c -E 'SwapFree|SwapTotal|swappiness|overcommit|Committed_AS|CommitLimit' 8524904a -- tools/mori-census.sh tools/mori-pressure.py tools/mori-oom-killers.py tools/mori-job-runway.py SKILL.md` → no file listed (git grep -c lists matching files only): 0 hits in all five.
- Host reads: `grep` of six `/proc/meminfo` lines, four `/proc/sys/vm/*` files, `/proc/pressure/memory` `some` line.

## 1. Instruments (tools/) that read the three paths

| surface | path read | what it reads | what it prints | runway question answered |
|---|---|---|---|---|
| `tools/mori-census.sh` (`MEMINFO=${MORI_MEMINFO:-/proc/meminfo}` :313; `meminfo_field` :647; fill arm :1791-1796, row :1858) | `/proc/meminfo` | exactly two lines: `MemTotal`, `MemAvailable`, only when the user slice's `memory.max` is the literal `max` (host-ram fallback) | `host_mem_avail_pct=<MemAvailable*100/MemTotal>` with `mem_fill_scope=host-ram`; finding `MEM_AVAIL_LOW` (warn) at ≤ `MORI_MEM_AVAIL_MIN_PCT` (default 10, labelled local) | **memory left before swapping starts** (the estimate, as a share of RAM); host scope only |
| `tools/mori-census.sh` (psi block :1735-1763; `psi_avg10` :656; paths `MORI_CGROUP_PRESSURE` default `<user slice>/memory.pressure` :224) | `memory.pressure` of the **user slice cgroup**, not `/proc/pressure/memory` | `some` and `full` avg10 only (shape-gated decimals) | `psi_some_avg10`, `psi_full_avg10`; finding `MEM_PRESSURE_HIGH` at `some avg10 ≥ 10` (labelled local; observed 0.00–0.39 in r8) | **stall time**, cgroup scope, one smoothed window |
| `tools/mori-census.sh` (cgroup fill arm :1766-1810) | `memory.current` / `memory.max` / `memory.peak` / `memory.events` (cgroup, not the three paths) | numeric limit, current, high-watermark, oom/oom_kill counters | `mem_fill_pct`, `MEM_FILL_HIGH`, `mem_peak`, `oom_kill` | cgroup-closed-container fill; kill count (listed because it is the sibling of the host-ram arm) |
| `tools/mori-pressure.py` (`DEFAULT_ROOT = "/proc/pressure"` :87; docstring :1-60) | `/proc/pressure/{cpu,memory,io,irq}` | `some`/`full` avg10/avg60/avg300/total per resource; with `--interval S` two reads | JSON `mori-pressure-v1`: states, `total_delta_us`, `stall_ratio`, `PRESSURE_HIGH` at avg10 ≥ 10 (local) | **stall time**, system scope; the only surface with a delta (the two-sample stall ratio the census lacks) |
| `tools/mori-oom-killers.py` (:103-106, :437-439) | none of the three paths: parses earlyoom log text (`mem avail <= N% and swap free <= N%`) | thresholds printed by earlyoom | `term_swap_pct`, `kill_swap_pct`, `mem avail` terms | what a userspace killer's thresholds are, not a host value |
| `tools/mori-job-runway.py` | none: reads omp `config.yml` and the omp binary | `async.maxJobs`, binary clamp | `RUNWAY_*` verdict | **harness job** runway, not memory. Name collision with "runway": it answers nothing about RAM |
| fixture writers: `tools/mori-census.sh` selftest :3198, :4450; `mori-silence-cases.sh` :400; `mori-round13/14/17-*-regressions.py` | synthetic `MORI_MEMINFO` files with `MemTotal`/`MemAvailable`/`MemFree` | fixtures only | n/a | prove arithmetic, not this host (as surfaces-r8 already says) |

Not read by any tool: `/proc/sys/vm/*` (the only `/proc/sys` read in `tools/` is `kernel/random/boot_id`, census :248-249, :341), `/proc/vmstat`, `/proc/zoneinfo`, `/proc/swaps`.
Zero hits in `tools/` and `SKILL.md` for `SwapFree|SwapTotal|swappiness|zswap|zram|overcommit|Committed_AS|CommitLimit|min_free_kbytes|MemFree` (census MemFree: none; only fixtures).

## 2. Out-of-lane reader the lane entries lean on (read-only)

`scripts/hyaku/wave-slot.sh` :21 `MIN_AVAIL_MB=${HYAKU_WAVE_MIN_AVAIL_MB:-6144}`, :68 `mem_avail_mb()` awk on `/proc/meminfo` `MemAvailable`: the dispatcher's allocation gate (a wave waits while `MemAvailable < 6144 MB`). `harness-job-capacity-r25.md:178` cites it. The lane's census floor (10 % of MemTotal) and the dispatcher floor (6144 MB) are different units and were never compared in a receipt. `scripts/hyaku/disk-guard.sh` is disk pressure only.

## 3. Knowledge entries (corpus/knowledge/) that read or define the paths

| entry | paths / lines it covers | runway question answered |
|---|---|---|
| `memavailable-estimate-r51.md` (S492-S496) | `/proc/meminfo` `MemAvailable`, `MemFree`, `Cached`, `Shmem`; `meminfo.c` printer, kB shift helper; floors as `min(half, low-watermark sum)` | memory left before swap (what the estimate is, why `MemFree+Cached` is wrong, 0 as clamp, threshold is local) |
| `overcommit-commit-limit-r52.md` (S497-S501; this round's entry) | `/proc/meminfo` `CommitLimit` (meminfo.c:125) and `Committed_AS` (:126); `/proc/sys/vm/overcommit_memory`, `overcommit_ratio`, `overcommit_kbytes`, `admin/user_reserve_kbytes` as sysctls to read | allocation refusal at request time (ENOMEM) before RAM runs out; enforced only under mode 2; heuristic mode 0 refuses one request > RAM+swap; reading rules for `Committed_AS > CommitLimit`, ratio 0, the `__vm_enough_memory` log line |
| `system-pressure-r24.md` (S090-S095, S145) | `/proc/pressure/{cpu,memory,io,irq}`, `psi=`, trigger window | stall time, system scope; what each file state does and does not prove |
| `surfaces-r7.md` :83, `surfaces-r8.md` :169-191, `observability-surfaces-r2.md` :234, `census-cgroup-levels-r45.md`, `drift-pin-r10.md` | census memory arm: cgroup PSI, fill, host-ram ratio, peak; scope naming; placeholder calibration (PSI some 10 vs ≤0.65 observed; avail floor 10 % vs 49-54 % observed) | stall time and fill at cgroup scope; threshold placement |
| `oom-memcg-stat-r50.md` :42, `oom-victim-selection-r27.md`, `userspace-oom-killers-r26.md` :58-61 | OOM report blocks (`__show_mem` vs memcg stats), badness in pages (RAM + swap), earlyoom's `MemAvailable + AnonPages` denominator | what happens after the runway is gone (kill) |
| `harness-job-capacity-r25.md` :178 | cites the dispatcher's `MemAvailable ≥ 6144 MB` gate | which floor spawns obey |
| `audit-r11.md` :342-349 | fixture `MORI_MEMINFO` | n/a |
| `SKILL.md` :1119-1123 (round-51 rows) and :41 | decision rows for `MemAvailable` runway, unit-free ratio, Cached/Shmem, local thresholds; row :41 `MEM_PRESSURE_HIGH`/fill/avail | memory left before swap. No SKILL.md row mentions `CommitLimit`/`Committed_AS` at this rev (the sweep receipt also says 0 at entering; the L1 integrates the entry's row later) |

## 4. Runway questions mapped to coverage

| question | instrument that measures it | entry that explains it |
|---|---|---|
| memory left before swap | census host-ram ratio (`MemAvailable/MemTotal`, host scope, only when slice limit is `max`) | memavailable-estimate-r51 |
| allocation refusal (ENOMEM at request time) | **none** | overcommit-commit-limit-r52 (explains only) |
| stall time, system | `mori-pressure.py` (one-shot, optional two-sample delta) | system-pressure-r24 |
| stall time, user slice | census `memory.pressure` avg10 | surfaces-r7/r8 |
| kill / OOM event | census `oom_kill` counters; `mori-oom-killers.py` for earlyoom logs | oom-memcg-stat-r50, oom-victim-selection-r27, userspace-oom-killers-r26 |
| swap left | **none** | none |

## 5. Gaps after this round's entry

G1 (MED) No instrument reads `CommitLimit`, `Committed_AS` or `/proc/sys/vm/overcommit_memory`. The new entry's reading rules need all three at once ("A host read needs `/proc/sys/vm/overcommit_memory` with the two meminfo lines"); `meminfo_field` (census :647) could read the meminfo pair, but nothing prints the mode, so `Committed_AS ≥ CommitLimit` cannot be read correctly by any lane output. The entry is knowledge-only; detection is a gap carried to a later round (the entry itself leaves FR8, the threshold, open).
G2 (MED) Swap is unread: `SwapTotal`, `SwapFree`, swap in `/proc/swaps`, `swappiness` have 0 hits in `tools/` and `SKILL.md`; the r51 entry's own question ("before swapping") has no swap figure to pair with. `memavailable-estimate-r51.md` states MemAvailable has no swap term and SKILL row 1121 tells readers not to count free swap, but no instrument prints it. Observed in a one-off host read: SwapTotal 31722876 kB, SwapFree 25859924 kB, so swap was ~18 % used while MemAvailable was ~54 % of RAM; the census ratio alone does not show that.
G3 (MED) Host `/proc/pressure/memory` is read only by `mori-pressure.py`, which is not in the census; the census reads only the user slice's `memory.pressure` (scope mismatch by design, named in r24). No single report places host-ram avail, host PSI and the slice PSI side by side. The census has no two-sample stall ratio.
G4 (MED) Two floors on the same line are uncompared: census `MEM_AVAIL_MIN_PCT=10` of MemTotal (≈3.1 GB on this host's 31.7 GB) vs the dispatcher's `6144 MB` (`wave-slot.sh:21`; ≈19 % of MemTotal here). The dispatcher floor is the stricter one by about 2x on this host; the census would stay silent while the dispatcher is already refusing grants. SKILL row 1119 tells a reader to compare them but no output prints both.
G5 (LOW) `/proc/sys/vm/*` is never read (`overcommit_*`, `swappiness`, `min_free_kbytes`, reserves); the r51 entry says the estimate holds back min(half the term, summed low watermarks) from floors that come from `min_free_kbytes` and `/proc/zoneinfo`; no lane surface reads either, so the entry's "host value" claims remain unverifiable by lane tools (the entry already says it claims no host value).
G6 (LOW) The kernel-log refusal line (`__vm_enough_memory: ... not enough memory for the allocation`, named in the new entry) is not read by any instrument; lane rule (QUALITY 15) forbids grepping kernel-log MESSAGE text for kill records, and the entry's rate-limited line is a refusal, not a kill, so whether that rule applies is undecided. UNVERIFIED: I did not read QUALITY 15's exact wording at this rev.
G7 (LOW) `tools/mori-job-runway.py` is named "runway" but measures harness job caps, not memory; a reader scanning the coverage map for "runway" could miscount it as memory coverage. The new entry's coverage-map line says "resource runway (new ground)"; its scope is memory only.
G8 (LOW) Zero hits for `/proc/vmstat`, `/proc/zoneinfo`, `pgscan`/`allocstall` counters, `memory.events` `high`/`max` counts as runway signals, hugetlb pages (which the new entry's CommitLimit formula subtracts): none are read.

## 6. Host snapshot (read-only, one reading, not claimed typical)

`MemTotal 31721796 kB`, `MemAvailable 17077092 kB`, `SwapTotal 31722876 kB`, `SwapFree 25859924 kB`, `CommitLimit 47583772 kB`, `Committed_AS 42314068 kB`; `vm.overcommit_memory=0`, `overcommit_ratio=50`, `overcommit_kbytes=0`, `swappiness=100`; `/proc/pressure/memory` `some avg10=0.00 avg60=0.00 avg300=0.00 total=54265443`. Consistency check: CommitLimit = (RAM − hugetlb) × 50 % + swap = 15860898 + 31722876 = 47583774 kB with hugetlb ≈ 0 and page rounding, matching the printed 47583772 kB to 2 kB. Mode 0, so `Committed_AS` (42.3 GB) being 89 % of `CommitLimit` is, per the entry's own first reading rule, normal and not enforced. Observed once; no claim about other hosts or times. The entry claims no host sysctl values, so this is not a row correction.

## Findings

- MED — `tools/mori-census.sh` (memory arm :1766-1810): no reader for `CommitLimit`, `Committed_AS`, `/proc/sys/vm/overcommit_memory` (G1); the new entry `corpus/knowledge/overcommit-commit-limit-r52.md` "Reading rules" table has no instrument behind it.
- MED — `tools/` (all): swap (`SwapTotal`/`SwapFree`) is unread (G2); the r51 "before swapping" question has no paired swap figure.
- MED — `tools/mori-census.sh:1735-1763` vs `tools/mori-pressure.py:87`: host PSI and slice PSI are different surfaces with no joint report and no two-sample delta in the census (G3).
- MED — `tools/mori-census.sh:369` (10 % floor) vs `scripts/hyaku/wave-slot.sh:21` (6144 MB): unlabelled units/floors that no receipt compares; on this host the dispatcher floor is the stricter (G4).
- LOW — `/proc/sys/vm/*`, `/proc/zoneinfo`, `/proc/vmstat` unread by any lane instrument (G5, G8).
- LOW — `corpus/knowledge/overcommit-commit-limit-r52.md` "A host read needs ... mori reads them": the sentence describes what a host read would need; no mori surface at 8524904a reads `overcommit_memory` (grep: 0 hits in `tools/`), so "mori reads them" is true only for a manual read, not an instrument. Suggest the L1 word it as "a reader reads them" or name the manual `cat` (data correction available to the L1; not a counter issue).
- LOW — `tools/mori-job-runway.py`: name collision with memory runway (G7).
- LOW — SKILL.md has no `CommitLimit`/`Committed_AS` row at this rev (0 hits); the r51 rows 1119-1123 are the only runway decision rows (the L1 integrates the r52 row later).
