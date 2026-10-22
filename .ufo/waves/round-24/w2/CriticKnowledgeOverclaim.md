# Round 24 wave 2 — CriticKnowledgeOverclaim

Seat: MoriR24.CriticKnowledgeOverclaim (critic, leaf). Target: `corpus/knowledge/system-pressure-r24.md`
at measured tip `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc`. The lane HEAD has since moved to
`89849a76322a5d79cd45d5f87cf34229ecf41f75`; `git diff --stat a730ecf -- corpus/knowledge/system-pressure-r24.md`
prints nothing, so every line number below holds at both revisions.

Result: **6 kills, 4 partial kills, 4 minor citation or wording defects; the core code facts F1, F2, F3 (at v7.2),
F5, F6 and the host observation survive.** None of the findings changes tool behaviour or any frozen case; all
are knowledge-entry wording corrections. Two of them (K1, K3) also touch the SKILL.md decision table if it copies
the entry's "does not prove" column; I did not check that file (ReviewSkillProvince owns it).

## What I ran

- Fetched Linux v7.2 raw text into `/fast/scratch/hyaku/mori-r24-a2/w2/CriticKnowledgeOverclaim/src/`
  (raw.githubusercontent.com tag `v7.2`): `Documentation/accounting/psi.rst` (188 lines),
  `kernel/sched/psi.c` (1725), `Documentation/admin-guide/cgroup-v2.rst`, `init/Kconfig`,
  `Documentation/admin-guide/kernel-parameters.txt`, `include/linux/psi_types.h`, `include/linux/psi.h`,
  `kernel/cgroup/cgroup.c`, `kernel/time/sched_clock.c`, `kernel/time/Makefile`, `kernel/sched/sched.h`,
  `kernel/sched/cputime.c`, `kernel/sched/core.c`, `include/linux/sched/clock.h`, `arch/x86/kernel/tsc.c`,
  `arch/x86/Kconfig`; from git.kernel.org `plain/`: v7.2 `init/main.c`, v7.2 `kernel/sched/clock.c`, and
  `kernel/sched/psi.c` at v5.12, v5.13, v5.15, v5.18, v5.19, v6.0, v6.1-rc1, v6.1; commit patches
  `52b1364ba0b1` and `890d550d7dba`.
- Read-only host reads: `uname -r`, `/proc/cmdline`, `zcat /proc/config.gz | rg CONFIG_PSI…`,
  `ls /sys/module/kernel/parameters/`, `ls`/`cat /sys/fs/cgroup/{cgroup,cpu,irq}.pressure`,
  `cat /proc/pressure/{cpu,memory,io,irq}` beside `cat /sys/fs/cgroup/{cpu,memory,io,irq}.pressure`,
  current clocksource. No write anywhere outside scratch and this report; no trigger registered.
- No mutant clone: every target is prose in the knowledge entry, so counterexamples are source lines and host reads.

## Kills (statement contradicted by a source or by the host)

### K1 — F9 "A system-scope read says nothing about any cgroup's pressure, and vice versa" (entry:110; Limits :153-155)

- Counterexample: the root cgroup. `cgroup_psi()` returns `&psi_system` for the root:
  `return cgroup_ino(cgrp) == 1 ? &psi_system : cgrp->psi;` (v7.2 `include/linux/psi.h:39`). The root's
  `{cpu,memory,io,irq}.pressure` files exist (no `CFTYPE_NOT_ON_ROOT` on `cgroup_psi_files`,
  `cgroup.c:5549-5591`) and print the same group `/proc/pressure/*` prints (`psi.c:1540,1545,1550,1686`).
- Host: `/sys/fs/cgroup/{cpu,memory,io,irq}.pressure` and `/proc/pressure/{cpu,memory,io,irq}` were
  byte-identical in one read pass (for example io `some … total=126507158` and `full … total=121230778` in both).
- The entry contradicts itself: its own U7 says the root `cgroup.pressure` controls system accounting.
- Impacted axes: coverage (C2 knowledge accuracy).
- Smallest correction: "A system-scope read says nothing about any **non-root** cgroup's pressure; the root
  cgroup's pressure files print the same `psi_system` group as `/proc/pressure` (psi.h:39)." In Limits, write
  "Per-cgroup (non-root) … are a different population".

### K2 — F12 "The IRQ clock itself is a boot parameter … This is the switch behind the IRQ path of F6" (entry:123-127)

- `kernel/time/sched_clock.c` is built only under `CONFIG_GENERIC_SCHED_CLOCK`
  (`kernel/time/Makefile:23: obj-$(CONFIG_GENERIC_SCHED_CLOCK) += sched_clock.o`); `arch/x86/Kconfig`
  has no `GENERIC_SCHED_CLOCK` (rg: none). So `irqtime=` does not exist on x86.
- Host (x86_64): `/proc/config.gz` has no `CONFIG_GENERIC_SCHED_CLOCK` line, and
  `/sys/module/kernel/parameters/` has no `irqtime` entry. The parameter F12 names does not exist on the host
  the entry measured.
- On x86 the switch is `tsc=noirqtime` (`arch/x86/kernel/tsc.c:327-328`, documented at
  `kernel-parameters.txt:7930` "[x86] noirqtime") and `if (!no_sched_irq_time) enable_sched_clock_irqtime();`
  (`tsc.c:1544-1545`). It is also switched **off at run time** by `disable_sched_clock_irqtime()` when the
  sched clock is found unstable (v7.2 `kernel/sched/clock.c:176` "TSC found unstable after boot", and `:243`).
  `irqtime=` is not in `kernel-parameters.txt` at all (the only `irqtime` hit is :7930).
- F12 also contradicts U1, which says where the branch is switched on "was not located". F12 rests on a file
  the header lists as having no registry row.
- Impacted axes: coverage; it states an architecture-specific path (generic sched clock: arm, arm64, riscv and others) as the general
  switch.
- Smallest correction: "On architectures with `CONFIG_GENERIC_SCHED_CLOCK`, `irqtime=` and the clock rate decide
  (sched_clock.c:48-50,242-243). On x86 (this host) the TSC code enables it unless `tsc=noirqtime`
  (tsc.c:327-328,1544-1545), and `kernel/sched/clock.c:176,243` can disable it after boot." Update U1 to match.

### K3 — Version-bound facts stated as general in the decision table (entry:138, :142)

- Row "System CPU `full` line present" says "a nonzero value means the file is not the kernel's system CPU
  pressure file". The zeroing branch arrived with commit `890d550d7dba` ("sched/psi: report zeroes for CPU full
  at the system level"): absent from `psi.c` at v5.13, v5.15 and v5.18, present at v5.19 (rg
  "CPU FULL is undefined"). The commit message quotes a genuine kernel file with
  `full avg10=0.22 avg60=0.23 avg300=0.16 total=358783277`. A nonzero value is the kernel's shape on 5.13–5.18.
- Row "malformed" says "the kernel's own emitter produces exactly the documented shape (F2), so `malformed`
  means *this file is not a kernel PSI file of this resource*". v5.12 `psi.c:1021`:
  `for (full = 0; full < 2 - (res == PSI_CPU); full++)`, so a genuine pre-5.13 `/proc/pressure/cpu` has only a
  `some` line, and the tool's required-kinds rule calls it `malformed`. The entry's own S090 line
  (psi.rst:57-59, "has been reported since 5.13") already records this.
- U5 says other versions were "not checked", but both rows state their conclusion without the "at v7.2" qualifier.
- Impacted axes: coverage, freshness.
- Smallest correction: prefix both "means" clauses with "on v7.2 (since 5.19 for CPU `full` zeros, since 5.13
  for the CPU `full` line)", and add one U5 sentence that pre-5.13 and 5.13–5.18 genuine files violate the two
  rules.

### K4 — Limits "An event that starts and ends between two reads is invisible to a one-shot read, and `avg10` cannot recover it (F4)" (entry:151-152; row 1 at :136 "can be invisible")

- psi.rst:60-65: the averages give "insight into short term events", and the total is exported "to allow
  detection of latency spikes which wouldn't necessarily make a dent in the time averages". The total is
  cumulative (`psi.c:408-410`), and each 2-second sample feeds all three decaying averages (`calc_avgs`,
  `psi.c:342-360`; `update_averages`, `psi.c:548-573`). An event between two reads is counted in `total` and,
  attenuated, in `avg10`/`avg60`/`avg300` at the next read.
- What is true: a short event may leave `avg10` below the local threshold, and one read cannot place it in time.
- Impacted axes: coverage. The entry cites F4 for the opposite of what F4's source says.
- Smallest correction: "A short event is counted in `total` and decayed into the averages, but it may leave
  `avg10` under the threshold, and a single read cannot say when it happened." Row 1: "can stay under the
  threshold" instead of "can be invisible".

### K5 — F4 "refreshed on each read" (entry:59-61)

- `psi_show` refreshes the averages only if a 2-second period has elapsed:
  `if (now >= group->avg_next_update) group->avg_next_update = update_averages(group, now);` (`psi.c:1269-1270`).
  What each read does refresh is the per-CPU time collection that feeds `total` (`collect_percpu_times`, `psi.c:1268`).
- Impacted axes: coverage (small).
- Smallest correction: "the total is collected on each read; the averages are recomputed on a read only when the
  next 2-second update is due (psi.c:1268-1270)".

### K6 — F8 "the kernel accepts windows 'ranging from 500ms to 10s'" (entry:93-94)

- That is the documentation's sentence (psi.rst:102). The v7.2 code has no lower bound: no `WINDOW_MIN_US`
  in `psi.c` (rg: none); `psi_trigger_create` rejects only `window_us == 0 || window_us > WINDOW_MAX_US`
  (`psi.c:1372-1373`), plus the unprivileged multiple-of-2s rule (`psi.c:1379-1380`) and
  `threshold_us == 0 || threshold_us > window_us` (`psi.c:1383`). `WINDOW_MIN_US 500000` was in v5.12, v5.13,
  v5.15, v5.19, v6.0 and v6.1 (`v6.1 psi.c:163,1214`). At v7.2 the documentation is stale, and the entry
  attributes it to "the kernel" while citing code only for the upper bound.
- Impacted axes: freshness (doc versus code drift presented as code fact). F8 is not used by the tool.
- Smallest correction: "the documentation states 500ms to 10s; the v7.2 code enforces 0 < window ≤ 10s
  (psi.c:1372-1373) and, for unprivileged writers, a multiple of 2s (psi.c:1379-1380)".

## Partial kills (the conclusion holds, but the wording, label or provenance is wrong)

### P1 — U7 root `cgroup.pressure` wording (entry:186)

- "so `/proc/pressure` would stay frozen" is wrong for the averages. When the group is disabled,
  `psi_group_change` stops `test_states`/`record_times` (`psi.c:845-857`) and IRQ accounting skips it
  (`psi.c:1034-1035`). So `total` freezes, but `psi_show` still runs `update_averages` when a period is due
  (`psi.c:1269-1270`), each sample is `total - avg_total = 0` (`psi.c:551`), and `calc_avgs` decays the averages
  toward 0.00 (`psi.c:347-359`). The wave-1 source this note credits says exactly that
  (`.ufo/waves/round-24/w1/CriticC2Semantics.md:96`: "Its `total=` stays frozen, and the averages decay to
  0.00"). The entry dropped that detail. One more effect: right after a disable, `avg10` still carries the
  earlier values, so for a few periods a read can still report `PRESSURE_HIGH`.
- "Those two files have no registry row" is true of `psi.h` and `cgroup.c`, but the mechanism that stops
  accounting is `psi.c:845-857`, which is S091 (registered), and the switch's documented semantics are in
  `cgroup-v2.rst:1066-1081`, which is S092 (registered). Only the root-to-`psi_system` mapping (`psi.h:39`)
  and the missing `CFTYPE_NOT_ON_ROOT` (`cgroup.c:5585-5589`) lack rows. S092 itself says nothing about the
  root or system effect ("not hierarchical … does not affect PSI accounting in descendants"), so that part is
  code-only.
- "An interval read with an unchanged `total` is consistent with it but does not prove it" omits the direct,
  read-only witness: `/sys/fs/cgroup/cgroup.pressure` reads the flag (`cgroup_pressure_show`,
  `cgroup.c:4093-4100`; host value `1`), and a `0` also hides the root `{cpu,memory,io,irq}.pressure` files
  (`cgroup.c:4127-4129`).
- Smallest correction: "…stops `psi_system` accounting: totals freeze and the averages decay toward zero over the
  following reads (psi.c:845-857, 551, 1269-1270), so a one-shot read can report `PRESSURE_OK` under real
  pressure. The flag is directly readable at `/sys/fs/cgroup/cgroup.pressure` (this host: `1`)." Change the
  registry sentence to name only `psi.h:39` and `cgroup.c:5585-5589` as unregistered.

### P2 — The F7 `[INFERENCE]` label and U4 point at a dependency that does not exist (entry:85-88, :181-182)

- The conclusion ("the boot-parameter path removes the files") does not depend on the order of `psi_init()` and
  `psi_proc_init()`. `psi_proc_init` tests `psi_enable` directly (`psi.c:1712`), not `psi_disabled`.
  `psi_enable` has one writer, `setup_psi` (`psi.c:156`, `__setup("psi=")`). `__setup` parameters are parsed
  in `start_kernel` by `parse_args("Booting kernel", …)` (`init/main.c:1011`), before `sched_init()`
  (`init/main.c:1047`, which calls `psi_init()`, `core.c:9101`) and before `do_initcalls()` (`init/main.c:1445`,
  which runs `module_init(psi_proc_init)`). The conclusion is a direct code reading. The only open point is that
  `init/main.c` has no registry row.
- Consequence the entry misses (this is the strongest form of the "cause from error" question): at v7.2,
  `psi_disabled` is enabled only at `psi.c:231` under `!psi_enable`, and the files exist only under `psi_enable`.
  So the `psi_disabled` `EOPNOTSUPP` branch (`psi.c:1257-1258`) cannot be reached through a v7.2
  `/proc/pressure` read. The only reachable `/proc` `EOPNOTSUPP` is `irq` with IRQ time accounting off, which
  happens with `tsc=noirqtime` or after `kernel/sched/clock.c:176,243` (see K2). So:
  - F7 "makes every read fail" and the decision-table phrase "v7.2 returns it on the `psi_disabled` branch"
    (entry:140) describe dead code for `/proc` reads;
  - "the error alone does not say which" is true of the bare errno, but together with the resource name the
    branch is fixed at v7.2;
  - U3 "a real host **may** show `absent`" is "**must**" for cpu, memory and io, while `EOPNOTSUPP` is
    reachable on `irq`.
  The tool's "no cause inferred" rule (A2; `tools/mori-pressure.py:140-142`) still stands; this is entry
  accuracy, not tool behaviour.
- Smallest correction: drop the `[INFERENCE]` label and U4, and cite psi.c:156,1712 plus `init/main.c:1011,1445`
  (unregistered). In the `EOPNOTSUPP` row, say: "on v7.2 reachable only on `irq` (IRQ time accounting off:
  `tsc=noirqtime` on x86, or the sched clock marked unstable); the `psi_disabled` branch is unreachable while
  the files exist".

### P3 — IRQ semantics the sources do not state (entry:137 "`null` means *undefined*, not *zero*")

- psi.rst never mentions IRQ: it names cpu, memory and io only (psi.rst:36-38). cgroup-v2.rst:1083-1087 says
  `irq.pressure` "Shows pressure stall information for IRQ/SOFTIRQ. See … psi.rst", and psi.rst has nothing on
  IRQ. "Undefined" is psi.rst's word for system CPU `full` (psi.rst:57), borrowed here. The only upstream
  statement is the commit message (S096, `52b1364ba0b1`): "we don't use PSI_IRQ_SOME since IRQ/SOFTIRQ always
  happen in the current task on the CPU, make nothing productive could run even if it were runnable, so we only
  use PSI_IRQ_FULL". IRQ `some` is not tracked by design. The source does not call it undefined.
- No upstream document defines what IRQ `full` measures. The code accounts IRQ time only to a non-idle current
  task's groups (`if (!curr->pid) return;`, `psi.c:1017`) and skips same-group switches (`psi.c:1021-1022`).
  The entry thresholds IRQ `full` without stating this. That is not an overclaim, but it is a missing
  `[UNKNOWN]`.
- Smallest correction: "`null` means not tracked: the kernel has no IRQ `some` state (S095; S096 rationale),
  not zero". Add an `[UNKNOWN]`: no upstream document defines IRQ `full`; per `psi.c:1017`, IRQ time on an idle
  CPU is not counted.

### P4 — F10 "therefore not a stall event and not a kernel fault" (entry:112-116); F7 / decision table ENOENT cause list (entry:139)

- F10: `psi.c:408-410` shows that the code has no decrement path. That proves the design, not the absence of a
  defect, and the kernel keeps its own accounting-bug detector (`psi_bug`, `psi.c:144,837`). Correction:
  "…is not a stall event; the v7.2 code never decreases it, so a decrease means the two samples are not
  comparable [INFERENCE]".
- ENOENT row: "a missing file is consistent with either" lists two causes, but there are more. A kernel built
  without `CONFIG_PSI` has no `psi.c` and no `/proc/pressure` (stub branch `psi.h:48-70`). A pre-6.1 kernel has
  no `irq` file (S096; v6.0 `psi.c` has no `PSI_IRQ`, v6.1-rc1 has 6 matches). A `--root` may point somewhere
  else. Correction: "consistent with, among others: …", adding `CONFIG_PSI` off and kernel older than 6.1.

## Minor citation and wording defects

- M1 — F3 (entry:50-51) cites `psi.c:1538-1550` for "All four `/proc/pressure/*` readers". That range holds three
  (`psi.c:1540,1545,1550`); the `irq` reader is `psi.c:1684-1687` (`:1686`).
- M2 — F7 (entry:85-86): the sentence ends at "(psi.c:1711-1719)," and the next starts with a capital "The".
  The sentence is broken.
- M3 — F9 (entry:103) "lists `irq.pressure` beside `cpu`, `io` and `memory.pressure`". `irq.pressure` is in
  the core-files section (cgroup-v2.rst:1083); `cpu.pressure` (:1215), `memory.pressure` (:1911) and
  `io.pressure` (:2171) are each in their controller's section.
- M4 — F11 (entry:118) "The kernel source defines no 'warn at N %' rule" is a claim about the whole tree. Only
  `psi.c` and `psi.rst` were read; scope it to "psi.c and psi.rst define no …".

## Survivors (checked and confirmed)

- F1: psi.rst:36-38 quote; `proc_create("pressure/irq", 0666, …)` under `CONFIG_IRQ_TIME_ACCOUNTING`
  (`psi.c:1717-1719`); Kconfig help names cpu, memory and io only (`init/Kconfig:730-733`).
- F2: the emitter `seq_printf` format at `psi.c:1290-1296`; label order `some` then `full`.
- F3 at v7.2: zeroing branch `psi.c:1282-1288`; host `/proc/pressure/cpu` `full … total=0`.
- F5: `only_full` (`psi.c:1273-1277`); IRQ path adds only to `PSI_IRQ_FULL` (`psi.c:1040`); IRQ `some` trigger
  gives `-EINVAL` (`psi.c:1364-1367`; enum `PSI_IRQ_FULL`=6, so "some" decrements to 5 and fails); `psi_types.h:41-49,57-70`;
  commit message quote "we only use PSI_IRQ_FULL"; first release 6.1 (v6.0 `psi.c` no `PSI_IRQ`, v6.1-rc1 6
  matches).
- F6: `psi.c:1260-1263`. F7 code facts: `psi.c:149-158, 228-240, 1257-1258, 1553-1566, 1711-1720`;
  `kernel-parameters.txt:5505-5507`; `init/Kconfig:743-761`.
- F9 cgroup.c citations: `3970-4091`, `4127`.
- U1 citations: `sched.h:3492-3495, 3518-3521`; `include/linux/sched/clock.h:112-116`.
- Header host observation, re-read today: kernel `7.2.11-arch1-1`, `CONFIG_PSI=y`,
  `# CONFIG_PSI_DEFAULT_DISABLED is not set`, `CONFIG_IRQ_TIME_ACCOUNTING=y`, no `psi=` in `/proc/cmdline`,
  four files present, `irq` one `full` line, cpu `full` total 0. U2 correctly scopes this to one host.
- Cause from error: neither the entry nor the tool asserts a cause from an errno (`tools/mori-pressure.py:140-142`,
  "no cause inferred"). That survives. P2 and P4 concern incomplete or dead-branch cause lists, not
  asserted causes.

## Impact summary

| Finding | Kind | Axis | Touches tool or cases |
|---|---|---|---|
| K1 root cgroup = system group | kill | coverage | no |
| K2 `irqtime=` not on x86 | kill | coverage | no |
| K3 version-bound CPU `full` and malformed rules | kill | coverage, freshness | no (tool targets v7.2) |
| K4 "invisible" short events | kill | coverage | no |
| K5 averages "refreshed on each read" | kill | coverage | no |
| K6 500 ms minimum window | kill | freshness | no |
| P1 U7 frozen versus decaying, registry, direct witness | partial | coverage | no (a read-only check is a judge decision) |
| P2 misdirected `[INFERENCE]`; dead `psi_disabled` branch | partial | coverage | no |
| P3 IRQ "undefined" | partial | coverage | no |
| P4 "not a kernel fault"; incomplete ENOENT causes | partial | coverage | no |

These are fixable defects in the knowledge entry, not tradeoffs. None of them moves the C2 after-value
(`PASS 12/12`). Whether the entry, with K1–K6 open, still counts as "sourced" for the C2 knowledge part is the
judge's decision.

## Tooling

No installs or updates. I used curl, ripgrep, sed, git (read-only) and zcat, all already present.
Scratch: `/fast/scratch/hyaku/mori-r24-a2/w2/CriticKnowledgeOverclaim/src/`.
