# Mo53ScoutRunwayTools — resource-runway surface map at 2a4213bf8da72f7cd78189baa5bb9be825dca1df

Scope: reconnaissance only. Every file read via `git show`/`git grep` at the data commit `2a4213bf…`; the lane
tools were extracted with `git archive` into `/fast/scratch/hyaku/mori-r53/Mo53ScoutRunwayTools/arch` and only the
two read-only tools (`mori-commit-runway.py`, `mori-pressure.py`) were run live. The census was NOT run live
(UNVERIFIED for its live output; its behaviour below is from source lines). Host facts on 2026-10-26 were read from
`/proc/meminfo`, `/proc/sys/vm/*`, `/sys/devices/system/cpu/present`, `/proc/pressure/memory` and one `memory.max`.
This report carries no line that starts with the RECHECK or QUOTE words (none are used).

## 1. The sweep (command, output shape)

`git -C … grep -n -E 'meminfo|/proc/sys/vm|pressure|MemAvailable|CommitLimit|memory.max' 2a4213bf… -- tools corpus/knowledge SKILL.md`
→ hits per file (count of matching lines, via `awk -F: '{print $2}' | sort | uniq -c`): SKILL.md 33; `tools/mori-census.sh` 41;
`tools/mori-commit-runway.py` 25 (+ 25 in its `cases.json`); `tools/mori-pressure.py` 14; `tools/mori-routed-r24.py` 24
(only the pressure-evidence gate, it reads git objects, not the host); `tools/mori-round13/14/17-*-regressions.py`,
`mori-silence-cases.sh`, `mori-seat-terminal.py`, `mori-oom-killers` fixtures (fixture or text-match hits, no runtime read
of a memory file); entries: `system-pressure-r24.md` 43, `memavailable-estimate-r51.md` 26, `overcommit-commit-limit-r52.md` 13,
`audit-r11.md` 6, `kernel-v7.3-recheck-r53.md` 6, `commit-runway-read-r53.md` 5, `observability-surfaces-r2.md` 6,
`surfaces-r7.md` 9, `surfaces-r8.md` 6, `userspace-oom-killers-r26.md` 6, plus ≤2 each in
`harness-job-capacity-r25`, `census-cgroup-levels-r45`, `journal-alarm-routing-r14`, `oom-evidence-loss-r38`,
`oom-memcg-stat-r50`, `oom-victim-selection-r27`, `selftest-flake-r9`, `structured-journal-scopes-r13`.

A second sweep for the names the first omits (`SwapFree|SwapTotal|zoneinfo|/proc/vmstat|memory.swap|memory.high|Committed_AS|swappiness|watermark|min_free_kbytes|MemFree|AnonPages|Shmem`)
over `tools/*.sh tools/*.py` (non-fixture): `mori-census.sh` 56 lines (all `oom_kill`/`memory.events*`/`memory.peak` family — none for SwapFree,
zoneinfo, vmstat, Committed_AS), `mori-commit-runway.py` 8 (SwapTotal, Committed_AS), `mori-oom-killers.py` 2 (oom_kill), regression
scripts only as fixtures. Census has zero reads of `SwapFree`/`SwapTotal` (one `.swap` hit is a systemd unit-suffix regex, `mori-census.sh:1132`).
No tool reads `/proc/zoneinfo`, `/proc/vmstat` for reclaim counters, `memory.high`, `memory.swap.*` or `memory.stat`.

## 2. Surface table — what is read, what is printed, which runway question it answers

| surface | reads (path) | prints | runway question it answers | graded how |
|---|---|---|---|---|
| census cgroup arm, PSI (`mori-census.sh:1728-1763`) | `memory.pressure` of the user slice (`MORI_CGROUP_PRESSURE`, default sibling of `memory.events`, `:304-308`) | `psi_some`/`psi_full` avg10; `MEM_PRESSURE_HIGH` warn | Is the user slice stalling on memory right now? | `some avg10` integer part ≥ `MEM_PSI_WARN_AVG10` (10, labeled local) |
| census cgroup arm, fill (`:1765-1810`) | `memory.max`, `memory.current`; when `memory.max` is `max`, `/proc/meminfo` `MemTotal`+`MemAvailable` via `meminfo_field` (`:646`) | `mem_fill_scope=cgroup|host-ram|unavailable`, `mem_fill_pct`, `host_mem_avail_pct`; `MEM_FILL_HIGH`, `MEM_AVAIL_LOW` | How much of the slice limit is used; with no limit, what share of RAM is still startable | `MEM_FILL_WARN_PCT` / `MEM_AVAIL_MIN_PCT`, labeled local |
| census cgroup arm, peak (`:1813-`) | `memory.peak` | `mem_peak` + instance anchor | Highest memory this scope ever held since its cgroup was created | none (report only) |
| census cgroup arm, kills (`:1686-1847`) | `memory.events`, `memory.events.local`, service-scope `memory.events` | `CGROUP_OOM_KILL` crit, `CGROUP_OOM_KILL_CUMULATIVE` info | Did the kernel OOM-kill inside this cgroup? (a kill record, not runway) | count > 0 |
| census disk arm (`:1912-1968`) | `df -P` on `$ROOT` and `/tmp` (`MORI_DISK_TARGETS`, `:321`), `/proc/diskstats` | `DISK_LOW/CRITICAL`, since-boot write average | Disk-space runway of two targets | % used thresholds |
| `tools/mori-pressure.py` (r24) | `/proc/pressure/{cpu,memory,io,irq}` (one read or two with `--interval`) | `mori-pressure-v1`: per-resource state, some/full avg10/60/300, totals, `PRESSURE_HIGH` | Is the **host** stalling now (cpu, memory, io, irq)? | `--warn-avg10` default 10.0, labeled local |
| `tools/mori-commit-runway.py` (r53) | `/proc/meminfo` (MemTotal, SwapTotal, CommitLimit, Committed_AS, optional Hugetlb), 5 `/proc/sys/vm` files, `/sys/devices/system/cpu/present` | `mori-commit-runway-v1`: mode, headroom, (mode 2) usable/band, verdict | Could a *request* be refused with ENOMEM by the commit ledger, and under mode 2 is the room inside the per-CPU error band? | `usable_kb ≤ band_kb` under mode 2 only; mode 0/1 never LOW |
| `tools/mori-job-runway.py` (r25) | `~/.omp/agent/config.yml`, the installed binary | `mori-job-runway-v1`, `RUNWAY_*` | How many background jobs the harness lets a session run (a count cap, not memory) | none |
| `tools/mori-disk-rate.py` (r34) | `/proc/diskstats`, sysfs block class (two samples) | per-device write rate | Instantaneous disk write rate | none |
| `tools/mori-oom-killers.py` | oom_kill counters / userspace-killer state | killer inventory | Which killer could act | n/a |
| fleet (not lane) `scripts/hyaku/wave-slot.sh:68`, `inline-dispatcher.py:133` | `/proc/meminfo` `MemAvailable` | grant/spawn gate with MIN_AVAIL_MB / MEM_MIN_GB | Can the fleet start another seat now | fleet-owned, read-only here |

Knowledge entries (what they explain, none reads the host themselves): `memavailable-estimate-r51.md` (what `MemAvailable` is: `si_mem_available()`,
no swap term, 0 is a clamp, never rebuild as `MemFree+Cached`; runway threshold is a local threshold on a model, FR8 open);
`overcommit-commit-limit-r52.md` (the three modes, limit enforced only under mode 2); `commit-runway-read-r53.md` (band rule, 7 claim rows);
`system-pressure-r24.md` (PSI read states, avg10 is decayed stall time not bytes); `surfaces-r7.md`/`surfaces-r8.md`/`observability-surfaces-r2.md`
(why PSI + fill + avail were chosen; 108 `memory.max` files, 107 `max`, so the numeric-`memory.max` arm is fixture-only); `userspace-oom-killers-r26.md`
(earlyoom's `MemAvailable/(MemAvailable+AnonPages)` and swap-free rule); `oom-memcg-stat-r50.md` and `oom-victim-selection-r27.md`
(what the kill record carries: swap line, units, victim score) — kill-side, not runway-side.

## 3. Live reading on this host (read-only, 2026-10-26)

- `python3 -I -B tools/mori-commit-runway.py` (from the archive at the data commit) → exit 0, `verdict: COMMIT_HEURISTIC`, `mode: 0`, `cpus_present: 32`,
  `commit_limit_kb: 47583772`, `committed_as_kb: 41354964`, `headroom_kb: 6228808`, `limit_consistent: true`, `single_request_cap_kb: 63444672`, `findings: []`.
  `--selftest` → `MATCHER: rejected 23/23 corrupted expectations`, `MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23`, exit 0.
- Meminfo/vm at the same time: MemTotal 31721796, MemAvailable 17108824, SwapTotal 31722876, SwapFree 25108632, CommitLimit 47583772,
  Committed_AS 41325048 kB; `overcommit_memory=0`, `overcommit_ratio=50`, `overcommit_kbytes=0`, `admin_reserve_kbytes=8192`, `user_reserve_kbytes=131072`; `present` = `0-31`.
- `python3 -I -B tools/mori-pressure.py` → `PRESSURE_OK`, exit 0 (cpu some avg10 6.48, memory some/full avg10 0.00, io 0.00, irq full 0.99). `/proc/pressure/memory` read directly: avg10 0.00.
- User-slice `memory.max` = `max` (so the census fill arm is in its `host-ram` scope on this host; census itself not run, UNVERIFIED live).
- Swap in use right now: 31722876 − 25108632 = 6614244 kB (≈ 6.3 GiB) while MemAvailable is 17108824 kB: no mori tool reports it.

## 4. Where the new tool overlaps, and where it does not

1. **Census host-ram arm (`:1791-1796`)**: shares only the input file `/proc/meminfo` and the field `MemTotal`. Different question (startable memory vs refusable requests). Commit-runway never reads `MemAvailable` (the 22 `MemAvailable` hits in its `cases.json` are meminfo lines the tool ignores; `grep -c` on `mori-commit-runway.py` = 0). No duplicated verdict.
2. **`memavailable-estimate-r51.md`**: the r53 table, mode 1 row, sends the reader to `MemAvailable`; mode 0's `single_request_cap_kb = (RAM+swap)×page` restates r52's "mode 0 refuses a request larger than RAM+swap". Overlap is by cross-reference, consistent; no contradiction found. Both entries inherit FR8 (thresholds local).
3. **`mori-pressure.py`**: no shared input. A host in `COMMIT_LOW` can show `PRESSURE_OK` and vice versa; neither implies the other (stall time vs ledger).
4. **`overcommit-commit-limit-r52.md`**: the tool is the executable form of its mode table; the r52 rows (mode semantics) and r53 rows (batch/band) split cleanly: S497-S501 vs S511-S513. `SKILL.md:1146-1154` (r52 decision row) still says "mori reads `/proc/meminfo` and `/proc/sys/vm/overcommit_memory`" — true as a rule; the r53 row at `SKILL.md:1178+` adds the tool. Two decision tables about the same two lines now exist (r52 and r53); a reader must read both (LOW).
5. **Host-relevance**: this host runs mode 0, where the tool is structurally never LOW (verdict `COMMIT_HEURISTIC`, exit 0). On this host the r53 tool is a documented-nothing-to-alarm read; its band logic (mode 2) is only exercised by fixtures. This is the same shape as the r7 numeric-`memory.max` arm (fixture-only). The entry's sentence "Committed_AS exceeds it — COMMIT_HEURISTIC with over_limit_not_enforced" is a dated 2026-10-26 observation; my later live read shows Committed_AS (41.35 GB) below CommitLimit (47.58 GB) and `findings: []`, so the sentence is not reproducible now (the figure moves; I could not read the earlier moment: UNVERIFIED either way).

## 5. Runway questions still unanswered after this round

Ranked by how directly a seat-spawn or kill-prediction decision depends on them; "Where" = what exists now.

1. **Swap runway** (HIGH for the host this lane watches): `SwapFree`, swap-in/out rate and `memory.swap.max/current` are read by no lane tool; commit-runway reads only `SwapTotal` (for the limit recomputation). The host has 6.3 GiB swap in use and a `MemAvailable` the r51 entry says has no swap term; earlyoom's act rule (r26) is a conjunction on mem-avail % and swap-free %, so the lane cannot say which half of the killer's rule is close.
2. **Time dimension of memory** (HIGH): every memory arm is a single sample (census, commit-runway) or ≤10 s (`mori-pressure --interval`). No trend of `MemAvailable`/`Committed_AS`, no "minutes to floor". The lane has the two-sample shape for disk (`mori-disk-rate.py`, FR6) and PSI, none for memory bytes.
3. **Per-seat / per-scope memory** (MED): census reads the user slice as one scope (`memory.current`, `memory.peak`); no tool reads `memory.current` per seat or per `app.slice`/unit scope, so a 400-seat wave cannot be attributed. The question "what does one more seat cost" has no lane number (the fleet's `MIN_AVAIL_MB` floor is a fixed constant in `wave-slot.sh`).
4. **Reclaim activity** (MED): `/proc/vmstat` (`allocstall`, `pgscan_*`, `pgsteal_*`, `oom_kill`) and `/proc/zoneinfo` watermarks are unread; PSI tells stalls happened, the counters would say which reclaim path ran. The r51 entry names zone watermarks as an unrepresentable part of the estimate (`/proc/meminfo` alone cannot reproduce it).
5. **Composed verdict** (MED): three independent surfaces (census avail%, pressure, commit-runway) each print their own verdict; nothing states "this host can/cannot take N more seats". Each entry deliberately forbids reading one as another, so the composition has no owner (fleet gates read `MemAvailable` only, `wave-slot.sh:68`, `inline-dispatcher.py:133`).
6. **Tmpfs / other disk-like memory** (LOW-MED): census disk targets default to `$ROOT` and `/tmp` (`:321`); `/dev/shm` (8 GiB tmpfs, memory-backed, 13756 kB used now) and `/fast` (25 % used, the operator's scratch tier) are not in the default target list; `/dev/shm` growth consumes RAM, not disk.
7. **Numeric `memory.max` and `memory.high`** (LOW): the numeric arm stays fixture-only on this host (107/108 scopes `max`); `memory.high` throttling (`high` counter in `memory.events`) is not graded.
8. **Calibration** (open, FR8): all three graded thresholds (`MEM_PSI_WARN_AVG10`, `MEM_AVAIL_MIN_PCT`, `--warn-avg10`) and the new `COMMIT_LOW` are local/not calibrated; r53's own named limit.
9. **cgroup-scoped CPU/IO PSI and the resident trigger watcher** (FR12 remainder) unchanged.

Candidate next coverage item (for the L1 routing, not a counter change): a read-only swap-and-reclaim reader (`SwapTotal/SwapFree/SwapCached`, `/proc/vmstat` pswpin/pswpout/allocstall/oom_kill, optional two-sample delta) is the largest uncovered runway line that shares no input with the three existing surfaces beyond `/proc/meminfo`.

## 6. Tools and installs

None installed. No pacman. Nothing written outside this report and my scratch dir (removed at the end).

## Findings

- **MED** — `corpus/knowledge/commit-runway-read-r53.md` (Reading rules, last paragraph before Boundaries): the sentence "Committed_AS exceeds [the printed limit] — `COMMIT_HEURISTIC` with `over_limit_not_enforced`" is a point-in-time host claim; a live run at my read gave `findings: []` (Committed_AS 41354964 < CommitLimit 47583772). The entry dates it (2026-10-26), so it is not wrong, but it is not reproducible and the live leg of `count-c2.py` compares stable fields only. Suggest the L1 attach the receipt (`evidence/c2-at-data.txt` or a captured meminfo line) to that sentence, or drop the "exceeds" wording. I could not re-read the earlier host state (UNVERIFIED).
- **MED** — `tools/mori-commit-runway.py` (verdict logic): on this host (mode 0) the tool can only ever return `COMMIT_HEURISTIC` exit 0; the mode-2 band arm and `COMMIT_LOW` are exercised only by fixtures. The coverage move is real but not a live alarm here; matches the contract's own named limit; route to round 54 as "no live positive for the band" next to the numeric `memory.max` fixture-only precedent (`surfaces-r8.md:177-193`).
- **HIGH** (coverage gap, not a defect in this round's data) — no lane tool reads `SwapFree`/swap activity or any memory time series; the largest unanswered runway questions are swap runway and memory trend (§5 items 1-2). Routed item for round 54; concerns `PROVINCE.md` resource-runway line 26 and `tools/mori-census.sh` memory arm.
- **LOW** — `SKILL.md:1146-1154` (r52 decision row) and `SKILL.md:1178+` (r53 decision table) are two tables for the same `/proc/meminfo` pair; a reader of the r52 row that says "mori reads /proc/meminfo and /proc/sys/vm/overcommit_memory" is not pointed to the tool by that row.
- **LOW** — census default disk targets (`mori-census.sh:321`) exclude `/dev/shm` (memory-backed) and `/fast`; relevant to runway for seats whose scratch is `/fast/scratch` (observed 25 % used, `df -P /fast/scratch`).
- **LOW** — census was not run live by this seat; its fill/avail behaviour on this host (`memory.max` = `max` → host-ram arm) is inferred from source and one `memory.max` read: UNVERIFIED live.
