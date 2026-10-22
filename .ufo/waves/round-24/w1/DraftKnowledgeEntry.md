# Draft knowledge entry — C2 system pressure (round 24, wave 1)

Seat: `MoriR24.DraftKnowledgeEntry` (leaf, draft only — no product, corpus, SKILL.md or tool edit was made).
Scope: draft `corpus/knowledge/system-pressure-r24.md` for the C2 claim in `.ufo/waves/round-24/contract.md`,
in the style of `corpus/knowledge/wave-settlement-r20.md` and `corpus/knowledge/journal-cursor-window-r16.md`:
scope; facts each with a source pointer (URL + line anchor); a decision table mapping every observable file
state to the C2 tool state and to what that state does **not** prove; limits; `[UNKNOWN]` marks.

Bounds honoured: lane repo untouched except this report file; no `git`/`jj` mutation in the lane repo
(read-only reads only); no PSI trigger registered; no `/proc`, `/sys` or cgroup write; no service, package
or host change; no subagent dispatched (leaf seat).

## 1. Sources opened this round (this seat, by hand)

All four files were fetched as raw text from the pinned upstream tag and read locally. Line numbers below are
line numbers **of the fetched file** (they are the anchors this draft cites).

| # | Pointer | Bytes / lines | sha256 | Opened by |
|---|---|---|---|---|
| P1 | `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst` | 6792 B / 188 lines | `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692` | `MoriR24.DraftKnowledgeEntry` (this seat) |
| P2 | `https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c` | 48859 B / 1725 lines | `452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5` | `MoriR24.DraftKnowledgeEntry` (this seat) |
| P3 | `https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/cgroup/cgroup.c` | 202860 B / 7544 lines | `3d4a256adea52d7e3f3b60dbb39622c82aa30dc398c01b5a135d2ccac3379a8c` | `MoriR24.DraftKnowledgeEntry` (this seat, one corroborating fetch for the cgroup-scope row) |
| P4 | `https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/time/sched_clock.c` | 9270 B / 333 lines | `fe4ce32b7f1a5431b87ba5098fedf7153f6f259d74f4c8f61b4ed70fa9250c7a` | `MoriR24.DraftKnowledgeEntry` (this seat, one corroborating fetch for the `irqtime=` boot parameter) |

Commands (read-only, executed from `/tmp/mori-r24-draft`, outside the lane repo):

```
curl -fsSL https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst -o psi.rst
curl -fsSL https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c            -o psi.c
curl -fsSL https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/cgroup/cgroup.c       -o kernel_cgroup_cgroup.c
curl -fsSL https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/time/sched_clock.c    -o kernel_time_sched_clock.c
sha256sum psi.rst psi.c kernel_cgroup_cgroup.c kernel_time_sched_clock.c
```

Two upstream fetches were refused by the host during the round and one file was searched for a symbol that
is not in it: `include/linux/irq.h` (HTTP 429 once), `kernel/irq/irq.c` (refused), and `include/linux/psi.h`,
`include/linux/sched/psi.h`, `include/linux/interrupt.h`, `include/linux/sched.h`, `include/linux/kernel.h`,
`kernel/time/time.c`, `fs/proc/interrupts.c`, `kernel/time/ntp.c`, `include/linux/sched/task.h`,
`include/linux/sched/clock.h` were read for `irqtime_enabled` — it was **not found** in any of them (see §4,
`[UNKNOWN]` U1). Tooling installs: none were needed and none were made.

## 2. Draft entry — proposed `corpus/knowledge/system-pressure-r24.md`

> Draft only. The `source:` row, the `recheck:` command and the S-id mapping are left for the L1.
> Everything else below is drafted from the pointers in §1.

---

```markdown
source: (L1 to map) Linux v7.2 `Documentation/accounting/psi.rst`; Linux v7.2 `kernel/sched/psi.c`;
Linux v7.2 `kernel/cgroup/cgroup.c` (cgroup pressure files); Linux v7.2 `kernel/time/sched_clock.c`
(`irqtime=` boot parameter). Existing row S001 covers the same PSI documentation text on the rendered
docs.kernel.org page with different line anchors; this note cites the pinned v7.2 raw file.
verified-at: 2026-10-22 — the four files above were opened as raw text and read statically by this seat.
No host `/proc/pressure` file was read, no PSI trigger was registered, no cgroup file was written, and no
live pressure observation was taken by this seat. Host kernel configuration, boot parameters and live
values were not verified here.
recheck: `python3 -I tools/mori-pressure.py --selftest` (L1 runs it at the landed tip); the live host run
and the SCORECARD capability row are the L1's, not this note's.

# System pressure (PSI) for CPU, IO and IRQ — one-shot read, and what each file state does not prove

## Scope

System pressure stall information is exported by the kernel as text files under `/proc/pressure/`. This note
records what those files are, exactly which shapes the kernel emits, which error codes the kernel returns,
and how each observable file state maps onto the round-24 C2 tool state
(`tools/mori-pressure.py`, contract `.ufo/waves/round-24/contract.md` C2).

It is a **reading** note. It describes one-shot, system-scope reads. It does not register a PSI trigger,
does not poll, does not read cgroup-scoped pressure, and does not set any threshold the kernel or a vendor
defines. The tool's vocabulary (`ok`, `absent`, `unsupported`, `unreadable`, `malformed`,
`counter_regressed`), its verdicts (`PRESSURE_OK | PRESSURE_HIGH | PRESSURE_PARTIAL | PRESSURE_UNAVAILABLE`)
and its exit codes are the tool's own contract, not kernel vocabulary.

## Facts

Every fact below carries the upstream pointer this seat opened.

**F1 — the file set.** System PSI is exported through one file per resource under `/proc/pressure/`. The
upstream documentation names exactly three of them: "Pressure information for each resource is exported
through the respective file in /proc/pressure/ -- cpu, memory, and io."
([psi.rst:36-38](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)).
The kernel creates a fourth: `proc_create("pressure/irq", 0666, NULL, &psi_irq_proc_ops)` under
`#ifdef CONFIG_IRQ_TIME_ACCOUNTING` ([psi.c:1710-1721](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)).
So on v7.2 the kernel can expose an IRQ file the documentation does not mention; the documentation is not an
inventory of the file set.

**F2 — the file shape.** Each file holds two lines of the form
`some avg10=0.00 avg60=0.00 avg300=0.00 total=0` and
`full avg10=0.00 avg60=0.00 avg300=0.00 total=0`
([psi.rst:40-43](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)).
The kernel's emitter is one `seq_printf`:
`"%s avg10=%lu.%02lu avg60=%lu.%02lu avg300=%lu.%02lu total=%llu\n"`, i.e. always two fraction digits and an
integer total, one line per kind, in the order `some` then `full` ([psi.c:1290-1296](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)).
The `some` line is "the share of time in which at least some tasks are stalled on a given resource"; the
`full` line is "the share of time in which all non-idle tasks are stalled on a given resource simultaneously"
([psi.rst:45-56](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)).

**F3 — system CPU `full` is undefined, and the kernel writes zeros there.** "CPU full is undefined at the
system level, but has been reported since 5.13, so it is set to zero for backward compatibility."
([psi.rst:57-59](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)). The
kernel implements it by skipping the read: `if (!(group == &psi_system && res == PSI_CPU && full))` leaves
both the averages and the total at zero for that one line ([psi.c:1282-1288](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)).
All four `/proc/pressure/*` readers pass the system group (`psi_show(m, &psi_system, …)`,
([psi.c:1538-1550](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)), so the system CPU
`full` line is always zeros at v7.2.

**F4 — units and windows.** The three averages are "ratios (in %) … tracked as recent trends over ten,
sixty, and three hundred second windows"; "The total absolute stall time (in us) is tracked and exported as
well" ([psi.rst:60-65](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)).
The kernel converts the accumulated nanoseconds to microseconds when it prints the total:
`total = div_u64(group->total[PSI_AVGS][…], NSEC_PER_USEC)` ([psi.c:1284-1288](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)).
The averages are exponentially decayed, sampled at `PSI_FREQ = (2*HZ+1)` ("2 sec intervals"), and refreshed
on each read ([psi.c:160-164](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c),
[psi.c:1265-1272](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)).

**F5 — IRQ pressure has only a `full` line.** `only_full = res == PSI_IRQ;` and the print loop runs
`for (full = 0; full < 2 - only_full; full++)`, and the label is `"full"` when `only_full` is set
([psi.c:1273-1296](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)). The IRQ accounting
path adds only to `PSI_IRQ_FULL` ([psi.c:1032-1042](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)),
and a trigger request naming `some` for IRQ is refused with `-EINVAL`
([psi.c:1364-1367](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)).
An IRQ file therefore carries one `full` line; a missing `some` line for IRQ is the kernel's shape, not a defect.

**F6 — the IRQ file is conditional, and a read of it can fail.** `pressure/irq` is created only under
`CONFIG_IRQ_TIME_ACCOUNTING` ([psi.c:1717-1719](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)),
and `psi_show` returns `-EOPNOTSUPP` for IRQ when IRQ time accounting is not enabled:
`if (!irqtime_enabled() && res == PSI_IRQ) return -EOPNOTSUPP;`
([psi.c:1260-1263](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)).

**F7 — PSI can be disabled, and the errors surface on read.** The `psi_disabled` static key makes every read
fail: `if (static_branch_likely(&psi_disabled)) return -EOPNOTSUPP;`
([psi.c:1257-1258](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)). The key is enabled at
init when `psi_enable` is false ([psi.c:228-240](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c));
`psi_enable` is false either by `CONFIG_PSI_DEFAULT_DISABLED` or by the `psi=` boot parameter
([psi.c:149-158](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)). The open handlers are
plain `single_open` ([psi.c:1553-1566](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)),
so the failure appears on **read**, not on open. Separately, the proc files themselves are created only when
`psi_enable` is true ([psi.c:1711-1719](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)),
so on v7.2 the boot-parameter path removes the files rather than leaving them to fail with `EOPNOTSUPP`
[this is an [INFERENCE] from those two code paths; the boot ordering of `psi_init()` and `psi_proc_init()` was
not measured].

**F8 — the event-driven interface exists and is not used here.** A user registers a trigger by writing
`"<some|full> <stall amount in us> <time window in us>"` into the file and polling the same descriptor
([psi.rst:67-88](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)); the
kernel accepts windows "ranging from 500ms to 10s" ([psi.rst:102-104](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst),
`WINDOW_MAX_US 10000000` at [psi.c:167](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c));
a second trigger on the same descriptor fails with `EBUSY`
([psi.c:1596-1598](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)). This note and the
C2 tool use none of it: the tool reads and never writes.

**F9 — cgroup scope is a different surface.** "In a system with a CONFIG_CGROUPS=y kernel and the cgroup2
filesystem mounted, pressure stall information is also tracked for tasks grouped into cgroups. Each
subdirectory in the cgroupfs mountpoint contains cpu.pressure, memory.pressure, and io.pressure files; the
format is the same as the /proc/pressure/ files." ([psi.rst:178-187](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)).
The v7.2 kernel's cgroup file set also carries IRQ: `cgroup_irq_pressure_show`/`_write`
([cgroup.c:4077-4091](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/cgroup/cgroup.c)) and the
comment "show or hide {cpu,memory,io,irq}.pressure files"
([cgroup.c:4127](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/cgroup/cgroup.c)). The system readers
and the cgroup readers are different groups: the former pass `&psi_system`
([psi.c:1538-1550](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)), the latter pass
`cgroup_psi(cgrp)` ([cgroup.c:3970-4091](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/cgroup/cgroup.c)).
A system-scope read says nothing about any cgroup's pressure, and vice versa.

**F10 — the kernel accumulates the total monotonically.** The running total is
`group->total[aggregator][s] += div_u64(deltas[s], max(nonidle_total, 1UL));`
([psi.c:408-410](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)). A `total` that
*decreases* between two reads of the same file is therefore not a stall event and not a kernel fault: the two
samples are not comparable readings of the same counter.

**F11 — no upstream threshold exists.** The kernel source defines no "warn at N %" rule. The only thresholds
in the documentation are the user's own trigger values, given as examples ("100ms of total stall time within
any 500ms window", "some 150000 1000000") ([psi.rst:70-88](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)).
A tool threshold is therefore the tool's own, and must be labeled as local.

**F12 — the IRQ clock itself is a boot parameter.** `static int irqtime = -1; core_param(irqtime, irqtime,
int, 0400);` and `if (irqtime > 0 || (irqtime == -1 && rate >= 1000000)) enable_sched_clock_irqtime();`
([sched_clock.c:48-50, 242-243](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/time/sched_clock.c));
the declarations live in `include/linux/sched/clock.h:112-116`. This is the switch behind the IRQ path of F6.

## Decision table

Observable state of one resource file → the state the C2 tool reports → what that state does **not** prove.
Tool states and verdicts are the contract's vocabulary (contract C2); the "not proved" column is what the
sources above forbid.

| Observable file state | Tool state (C2) | Verdict / exit | What it does NOT prove |
|---|---|---|---|
| All four files present, kernel shape (F2), low values | each resource `ok` | `PRESSURE_OK`, exit 0 | That there was no stall: `avg10` is a decayed 10-second trend resampled every ~2 s (F4), so a shorter spike between two reads can be invisible. That the host is healthy. That the reading covers per-cgroup pressure (F9). That the local threshold was meaningful (F11). |
| IRQ file carries only a `full` line (F5) | `irq` = `ok`, `some: null` | unchanged by the resource itself | That IRQ "some" pressure is zero — the kernel never emits an IRQ `some` line (F5); `null` means *undefined*, not *zero*. That IRQ pressure is low. That the IRQ file is complete for the host: it is created only under `CONFIG_IRQ_TIME_ACCOUNTING` (F6). |
| System CPU `full` line present | `cpu` = `ok`, `full_system_undefined: true`; the `full` values are reported but never thresholded (contract C2) | unchanged by the resource itself | That the system had no full CPU stall: CPU `full` is undefined at the system level (F3) and must never be read as evidence of no stall. That a nonzero system CPU `full` value reports a stall — at v7.2 the kernel writes zeros there (F3), so a nonzero value means the file is not the kernel's system CPU pressure file, not that the system stalled. |
| File missing (ENOENT) | `absent` — unavailable, never zero | `PRESSURE_PARTIAL`, exit 0 (if others are `ok`); `PRESSURE_UNAVAILABLE`, exit 2 if every resource is absent | That the resource was not under pressure. That PSI is disabled — that is the `EOPNOTSUPP` path (F7), and on v7.2 the `psi=` path removes the files instead (F7). That any other resource is fine. |
| Read fails `EOPNOTSUPP` | `unsupported` — unavailable, never zero | as above | That there was no pressure. That the threshold was met or missed. That IRQ pressure is zero. `EOPNOTSUPP` is the kernel's own "PSI disabled" / "IRQ time accounting unavailable" code (F6, F7); it is an observation about the kernel's capability, not about load. |
| Read fails `EACCES`/`EPERM` | `unreadable` — unavailable, never zero | as above | That the resource was idle or unpressured. That access is the *only* reason for the failure — `unreadable` records that this seat could not read, nothing about the resource's state. |
| Line shape does not match, duplicate kind, or a required kind missing (`cpu`/`memory`/`io` need `some` **and** `full`) | `malformed` | `PRESSURE_PARTIAL`, exit 0 (if others are `ok`) | That the kernel misbehaved: the kernel's own emitter produces exactly the documented shape (F2), so `malformed` means *this file is not a kernel PSI file of this resource*, or that the two samples were inconsistent — it is a refusal, not a fault finding. That the missing kind is zero. That the pressure was low. |
| Interval mode: second `total` < first `total` | `counter_regressed` | `PRESSURE_PARTIAL`, exit 0 | That pressure dropped, that counts were lost, or that the counter is broken: the kernel accumulates totals monotonically (F10), so a decrease means the two samples are not comparable readings of the same counter. No rate is derived from it. |
| `avg10` ≥ the tool's `--warn-avg10` on `some` of `cpu`/`io`/`memory` or `full` of `memory`/`io`/`irq` | finding `PRESSURE_HIGH` on that resource | `PRESSURE_HIGH`, exit 1 | That the threshold is calibrated: 10.0 is a labeled-local placeholder with no upstream basis (F11). That any specific workload was harmed. That CPU `full` (excluded by contract) or IRQ `some` (does not exist, F5) had no pressure. |
| Any resource `absent`/`unsupported`/`unreadable`/`malformed` while the others are `ok` | as above | `PRESSURE_PARTIAL`, exit 0 | That the observed resources are the whole system, or that the missing resource was fine. That exit 0 means "no pressure anywhere". |
| Every resource unavailable | all unavailable | `PRESSURE_UNAVAILABLE`, exit 2 | That the system is unpressured. That the tool is broken: exit 2 is also the usage-error code. |

## Limits

- **One-shot only.** The tool reads a file and stops. It registers no trigger and does not poll, although the
  kernel supports exactly that ([F8]: write a threshold, poll the descriptor). An event that starts and ends
  between two reads is invisible to a one-shot read, and `avg10` cannot recover it (F4).
- **No cgroup scope.** Only `/proc/pressure` is read, i.e. the system group (F9). Per-cgroup `cpu.pressure`,
  `memory.pressure`, `io.pressure` and (at v7.2) `irq.pressure` exist and are a different population (F9).
  The census's user-slice `memory.pressure` is likewise a different scope; the two are never summed or
  compared as one number.
- **Threshold local.** `--warn-avg10` (default 10.0) is a local placeholder. The kernel defines no such
  threshold (F11), and the documentation's trigger numbers are examples (F8). The threshold may be tuned to
  suit a host; it must always be reported as labeled-local, and the value must never be presented as a
  vendor or kernel constant.
- **The kernel's CPU `full` is excluded from the threshold** by contract, and reported with
  `full_system_undefined: true`. It is not evidence of no stall in either direction (F3).
- **The tool's grammar is looser than the kernel's emitter.** The kernel always prints two fraction digits
  and an integer total (F2); the tool's grammar accepts any decimal. That looseness is the tool's rule, not
  the kernel's, and a file the kernel did not produce can still pass it.
- **Interval mode is a two-point slope.** `total_delta_us` and `stall_ratio` are derived from two reads of a
  cumulative, microsecond-denominated counter (F4, F10) — not a window average, and not comparable across
  hosts or across intervals.
- **Detection and report only.** No host write, no PSI trigger registration, no cgroup write, no service or
  package change (round-24 bounds).
- **The verdict vocabulary and exit codes are the tool's own** (contract C2). The kernel's vocabulary is
  `EOPNOTSUPP`, `EBUSY`, `EINVAL` and file shapes; the kernel never emits `PRESSURE_OK`.

## [UNKNOWN]

- **U1 — `irqtime_enabled()`.** The predicate psi.c calls at [psi.c:1014](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)
  and [psi.c:1261-1262](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c) was **not located**
  in any source this seat opened: it is absent from `include/linux/psi.h`, `include/linux/sched/psi.h`,
  `include/linux/interrupt.h`, `include/linux/irq.h`, `include/linux/sched.h`, `include/linux/kernel.h`,
  `kernel/time/time.c`, `kernel/time/ntp.c`, `fs/proc/interrupts.c`, `include/linux/sched/task.h` and
  `include/linux/sched/clock.h` (each fetched and grepped on 2026-10-22). Consequently this note does not
  claim **who** (root vs unprivileged) can read `/proc/pressure/irq`, or under what runtime condition the
  IRQ path returns `EOPNOTSUPP`. Sibling seats `SrcPsiTypes` / `SrcPsiIrqCommit` own that.
- **U2 — host configuration.** Whether this host builds `CONFIG_PSI`, `CONFIG_PSI_DEFAULT_DISABLED`,
  `CONFIG_IRQ_TIME_ACCOUNTING`, and whether it was booted with `psi=` or `irqtime=`, was not verified: this
  seat ran no host command against `/proc`, `/sys` or `/proc/cmdline`. `ScoutHostKernelConfig` owns that.
- **U3 — live reachability of `EOPNOTSUPP`.** Because the located disable path removes the files (F7), a
  real host may show `absent` rather than `EOPNOTSUPP`; this seat did not observe either. The claim that the
  two are distinct observations is a code-path reading, not a measurement.
- **U4 — boot ordering.** The relative order of `psi_init()` and `psi_proc_init()` was not verified, so the
  "boot-parameter disable ⇒ absent files" statement in F7 is labeled [INFERENCE].
- **U5 — version bounds.** Every kernel pointer here is the `v7.2` tag. Whether `pressure/irq` and cgroup
  `irq.pressure` exist in earlier or later kernels was not checked.
- **U6 — the man page.** `proc_pressure(5)` was not opened by this seat (`SrcProcPressureMan` owns it), so
  this note makes no claim about its wording, including whether it lists `irq`.
- **U7 — S-id mapping.** The `source:` row above is unresolved. This note cites URLs and line anchors only;
  the registry rows and the `S001` reconciliation are the L1's and the Registry seat's.

## Not claimed

- No trigger, no watcher, no poll loop, no daemon, no cgroup read, no write of any kind.
- No health claim: `PRESSURE_OK` is the absence of a threshold crossing in a local threshold, on a system
  scope, at one instant.
- No calibration of `--warn-avg10`, no comparison of these values across hosts, and no aggregation of system
  and cgroup scopes.
- No claim that CPU `full` is zero because the system was idle; it is undefined at the system level (F3).
- No claim that a missing or unreadable resource was unpressured; it was not observed.
```

---

## 3. Notes for the L1

1. **S-id mapping is yours.** This draft cites URLs + line anchors only. Suggested new registry rows (no ids
   assigned here):
   - *Linux v7.2 PSI documentation* — `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst`,
     kind `docs`, tier A, anchors `36-38`, `40-43`, `45-56`, `57-59`, `60-65`, `67-88`, `102-104`, `178-187`,
     sha256 `11c6b71…b82692`.
   - *Linux v7.2 `kernel/sched/psi.c`* — kind `code`, tier A, anchors `149-158`, `160-167`, `228-240`,
     `408-410`, `1006-1046`, `1251-1296`, `1335-1380`, `1538-1566`, `1568-1620`, `1684-1721`,
     sha256 `452318…312c5`.
   - *Linux v7.2 `kernel/cgroup/cgroup.c`* — kind `code`, tier A, anchors `3970-4091`, `4103-4137`,
     sha256 `3d4a25…79a8c`.
   - *Linux v7.2 `kernel/time/sched_clock.c`* — kind `code`, tier A, anchors `48-50`, `242-243`,
     sha256 `fe4ce3…50c7a`.
2. **S001 collision — decide explicitly.** `corpus/SOURCES.md` S001 already carries the PSI documentation
   ("Pressure interface:74-77; Monitoring for pressure thresholds:104-119; Cgroup2 interface"), but those
   anchors are the **rendered docs.kernel.org** page, not the v7.2 raw file (whose lines are 36-38 / 67-88 /
   178-187). Either S001 is re-pinned to the v7.2 raw file or a separate row is added; this note's citations
   resolve against the raw file. Left unresolved in the draft.
3. **Contract-vs-source tension, reported verbatim.** Contract C2 says: "Open/read errors: ENOENT → `absent`;
   EOPNOTSUPP → `unsupported` (PSI disabled)". The opened v7.2 source shows the boot-parameter disable path
   *removes* the files (`if (psi_enable) { proc_mkdir("pressure", NULL); … }`, psi.c:1712-1718) while the
   `psi_disabled` read path returns `-EOPNOTSUPP` (psi.c:1257-1258) — the two conditions are set from the same
   `psi_enable` flag (psi.c:149-158, 228-240). On v7.2 a `psi=0` boot therefore tends to produce `absent`,
   not `EOPNOTSUPP`. The tool's mapping is unchanged either way (both are "unavailable, never zero"); only
   the parenthetical "(PSI disabled)" is in tension with the source. Flagged, not resolved here.
4. **Doc-vs-kernel divergence, reported verbatim.** psi.rst:36-38 lists "cpu, memory, and io" and
   psi.rst:181-185 lists "cpu.pressure, memory.pressure, and io.pressure", while psi.c:1717-1719 creates
   `pressure/irq` and cgroup.c:4077-4091 implements a cgroup IRQ pressure file. The documentation is not an
   inventory of the pressure surfaces at v7.2. `SrcPsiRst` and `SrcCgroupV2` may want the same divergence in
   their notes; the L1 should keep one wording.
5. **SKILL.md decision table.** The contract says the SKILL.md decision table will cite these rows; that edit
   belongs to `DraftSkillTable`, not to this seat. For that seat, the C2 row candidates are: "is there
   system-wide CPU/IO/IRQ pressure?" → `python3 -I tools/mori-pressure.py [--root DIR] [--warn-avg10 X]
   [--interval S]`, never: registering a PSI trigger, reading cgroup pressure, tuning the threshold to fit an
   observation, or reading `PRESSURE_OK` as "no pressure anywhere" (system scope only; threshold labeled
   local; CPU `full` undefined). Nothing was written to `SKILL.md`.
6. **Tool-independent facts this note can support for the L1's other seats**: the file grammar (F2), the
   IRQ `full`-only shape (F5), the `EOPNOTSUPP` conditions (F6, F7), the read-time-not-open-time failure (F7),
   the monotonic total (F10), the absence of any upstream threshold (F11).

## 4. What this seat did not do

- Did not read the host's `/proc/pressure/*`, `/proc/interrupts`, `/sys/fs/cgroup/**` or `/proc/cmdline`.
- Did not run, build or inspect `tools/mori-pressure.py`; did not read
  `tools/fixtures/mori-pressure/cases.json` (the frozen-cases seat owns it) — the decision table above is
  written against the **contract's** C2 vocabulary, not against an implementation.
- Did not land `corpus/knowledge/system-pressure-r24.md`, edit `SKILL.md` or `corpus/SOURCES.md`, or touch the
  lane repo's git/jj state. The only file written is this report.
- Did not dispatch any subagent (leaf seat) and did not message any peer.
- Installed no tool and upgraded no package; no host service was restarted.
