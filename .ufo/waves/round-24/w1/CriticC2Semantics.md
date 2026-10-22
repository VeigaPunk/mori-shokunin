# CriticC2Semantics — round 24 attempt 2, wave 1

Seat: critic, read-only, leaf. Target: C2 semantics in `.ufo/waves/round-24/contract.md`.
Contract line numbers below are taken at lane tip `f7eb430c` (working tree). The C2 text there is
byte-identical to the landed `29c1bf45` text. The only change since landing is Amendment A1
(C1 only, +7 lines), so subtract 7 to get the landed line numbers.

## Sources opened this round (fetched 2026-10-22 ≈08:15Z, tag `v7.2`, stored under `/fast/scratch/hyaku/mori-r24-a2/critic-c2sem/`)

| File (raw.githubusercontent.com/torvalds/linux/v7.2/…) | SHA256 (first 16) | Lines |
|---|---|---|
| `Documentation/accounting/psi.rst` | `11c6b7129103b454` | 188 |
| `kernel/sched/psi.c` | `452318beaca3e6d1` | 1725 |
| `include/linux/psi.h` | `cd80982f753aa56e` | — |
| `include/linux/psi_types.h` | `483269b27c82b438` | 216 |
| `kernel/cgroup/cgroup.c` | `3d4a256adea52d7e` | 7544 |
| `Documentation/admin-guide/cgroup-v2.rst` | `a9433bb0e16a67f0` | 3524 |
| `fs/seq_file.c` | `db28fa9bd5006c76` | 1144 |
| `kernel/sched/sched.h`, `kernel/sched/cputime.c` | `44e7152a593bade4`, `5c9a5f92d5b359c6` | — |
| `arch/x86/kernel/tsc.c`, `init/Kconfig`, `include/linux/sched/loadavg.h` | `1937481d0e40da07`, `a43f09d89309a6bd`, `70bb912e5fca1e25` | — |

Host: `uname -r` = `7.2.11-arch1-1`; `/proc/config.gz` has `CONFIG_PSI=y`, `# CONFIG_PSI_DEFAULT_DISABLED is not set`,
`CONFIG_IRQ_TIME_ACCOUNTING=y`; there is no `psi=` token in `/proc/cmdline`. All host reads were `cat` or Python `os.open(O_RDONLY)`.

## Verdict per question

| Question | Contract | Primary source | Verdict |
|---|---|---|---|
| Is system CPU full undefined? | :66-67 | psi.rst:57-58; psi.c:1282-1288 | **Agree, with one gap** (finding F5) |
| Does IRQ print only `full`? | :64-65 | psi.c:1273-1277, 1290-1291 | **Agree.** psi.rst does not document irq at all (F6) |
| PSI disabled: does it fail at open or at read, and with which errno? | :68, :83, :87 (P05) | psi.c:1712-1720, 230-233, 1257-1262; seq_file.c:231-233, 287-288 | **Disagree** (F1, F2) |
| Does `cgroup.pressure=0` matter for `/proc/pressure`? | not addressed | psi.h:37-40; cgroup.c:4123-4133, 5585-5589; psi.c:845-857, 1033-1035 | **Disagree.** It matters for the root cgroup only (F3) |
| Are the average windows and total units as assumed? | :61-62, :72-73 | psi.rst:60-63; psi.c:161-164, 372-411, 1266-1270, 1286-1287 | **Agree on units.** "avg10" is a decaying average, not a 10 s window (F7) |
| Is the threshold-kind choice justified? | :70-71 | psi.c:247-263, 1282-1288, 1006-1040 | **Partly.** The `full` arm for memory and io adds no verdict information (F4) |

## Findings

### F1 — A PSI-disabled kernel gives ENOENT, not EOPNOTSUPP (false provenance; fixable)

Contract :68 says "EOPNOTSUPP → `unsupported` (PSI disabled)". Fixture topic P05 (draft `wt-cases/tools/fixtures/mori-pressure/cases.json`) repeats it: "every resource open fails with EOPNOTSUPP (PSI disabled)". The wave-1 spec (`wave1-spec.json:40`) also tells the psi.c source scribe to cite "the disabled-PSI return path (EOPNOTSUPP)".

**Counterexample:** boot with `psi=0`, or use `CONFIG_PSI_DEFAULT_DISABLED=y` without `psi=1`. The `/proc/pressure` directory is never created, so every open fails with ENOENT. The tool would report four `absent` resources, not `unsupported`.

- psi.c:1712-1716 creates the files only when PSI is enabled:
  ```
  if (psi_enable) {
      proc_mkdir("pressure", NULL);
      proc_create("pressure/io", 0666, NULL, &psi_io_proc_ops);
  ```
- psi.c:230-233 sets `psi_disabled` only from the same `!psi_enable` boolean at init: `if (!psi_enable) { static_branch_enable(&psi_disabled); ...`. `psi_enable` is written only by the boot `__setup("psi=")` handler (psi.c:154-158). `psi_disabled` has no other writer in psi.c.
- So the psi.c:1257-1258 branch (`if (static_branch_likely(&psi_disabled)) return -EOPNOTSUPP;`) can never run for a `/proc/pressure` file. The file it would guard does not exist on a kernel where `psi_disabled` is set. (That branch is still reachable through cgroup files? No: `cgroup_psi_enabled()` returns false when `psi_disabled` is set (cgroup.c:4156-4159), so cgroup pressure files are not created either (cgroup.c:1799-1801).)
- `CONFIG_PSI=n`: init/Kconfig:731-732 says "If you say Y here, the kernel will create /proc/pressure/". [INFERENCE] With N, the directory is absent, giving ENOENT. I did not grep the whole tree for other creators.

**The only EOPNOTSUPP reachable through `/proc/pressure` in v7.2** is on the `irq` file, when PSI is enabled. It happens when `CONFIG_IRQ_TIME_ACCOUNTING=y` but IRQ time accounting is off at runtime:

- psi.c:1260-1262: `if (!irqtime_enabled() && res == PSI_IRQ) return -EOPNOTSUPP;`
- sched.h:3492-3494 defines `irqtime_enabled()` as the `sched_clock_irqtime` static key. On x86 that key is enabled only when the kernel was not booted with `tsc=noirqtime` (tsc.c:327-328 and tsc.c:1544-1545: `if (!no_sched_irq_time) enable_sched_clock_irqtime();`). It can also be cleared by `disable_sched_clock_irqtime()` (cputime.c:36-40).

**Impacted axes:** coverage (decision-table correctness), calibration (a SOURCES row would cite psi.c for a claim psi.c refutes), and false provenance in P05 and in the knowledge decision-table row that the spec requests (`wave1-spec.json:75`).

**Smallest safe correction (does not change tool behaviour or any frozen expectation):**
- Relabel contract :68 to: "ENOENT → `absent` (this includes PSI disabled at boot or at build time, and irq on kernels without `CONFIG_IRQ_TIME_ACCOUNTING`); EOPNOTSUPP → `unsupported` (in v7.2 only `irq` with IRQ time accounting off at runtime, for example `tsc=noirqtime`)."
- Have the knowledge entry and the SKILL.md table carry the same mapping.
- Treat P05's topic text as a counterfactual robustness case, not a model of PSI-disabled hosts. Its expected output (`unsupported` ×4, `PRESSURE_UNAVAILABLE`, exit 2) is still correct tool behaviour.

The realistic PSI-disabled shape (all four ENOENT, giving exit 2) has no frozen case. It is a coverage gap. It is not a defect in the cases.

### F2 — The real EOPNOTSUPP arrives at read(), not open(); an open-only injection hook leaves that path untested (fixable)

Contract :83 says "Error injection (EOPNOTSUPP, EACCES) uses an in-process open hook". The fixture `errors` model does not say whether the error comes from open or from read.

- psi.c:1689-1691: `psi_irq_open` is `return single_open(file, psi_irq_show, NULL);`. That only allocates the seq_file, so open succeeds.
- seq_file.c:231-233: on read, `err = m->op->show(m, p); if (err < 0) // hard error break;`. Then seq_file.c:287-288: `if (unlikely(!copied)) { copied = m->count ? -EFAULT : err;`. So `read()` returns `-EOPNOTSUPP`.

**Counterexample:** suppose the implementation wraps only `open()` in the errno mapping, which the open hook makes sufficient to pass P05. Then on a host booted with `tsc=noirqtime`, Python's `f.read()` raises `OSError(95)` outside the handler. The uncaught traceback exits with status 1. Status 1 is the contract's `PRESSURE_HIGH` code (:76-77), so an unsupported irq would look like high pressure to any exit-code consumer.

[INFERENCE] I did not trigger this on a live host, because irqtime is enabled here and the bounds forbid a reboot.

**Smallest safe correction:**
- Make the injection hook raise the injected errno at the first read on the opened object, or at both open and read.
- Document in the knowledge entry that ENOENT and EACCES come at open and EOPNOTSUPP comes at read.
- The tool maps OSError errnos the same way at both call sites.

This needs no change to cases.json; `errors` stays errno-only.

### F3 — Root `cgroup.pressure=0` silently freezes `/proc/pressure` while the files stay readable (contract silent; fixable as a documented limit, or as a check)

The assignment asked whether a cgroup with `cgroup.pressure=0` matters. For a non-root cgroup it does not. For the root cgroup it does, and the contract's "unavailable, never zero" rule (:69) does not catch it.

- psi.h:37-40: `return cgroup_ino(cgrp) == 1 ? &psi_system : cgrp->psi;`. The root cgroup's PSI group is `psi_system`, which is the same object `/proc/pressure/*` prints (psi.c:1540, 1545, 1550, 1686: `psi_show(m, &psi_system, ...)`).
- cgroup.c:5585-5589: the `cgroup.pressure` cftype has no `CFTYPE_NOT_ON_ROOT` flag. The host has `/sys/fs/cgroup/cgroup.pressure` (value `1`).
- cgroup.c:4123-4133: writing 0 does `cgroup_file_show(&cgrp->psi_files[i], enable)` and then `psi->enabled = enable;`. For root, that sets `psi_system.enabled = false` and hides only `/sys/fs/cgroup/{cpu,memory,io,irq}.pressure`. The `/proc/pressure` entries are procfs files (psi.c:1713-1718), so they stay.
- psi.c:845-857: when `!group->enabled`, `psi_group_change` flushes once, keeps only the `PSI_ONCPU` bit and returns, so no stall state accrues. psi.c:1033-1035 skips IRQ accounting for disabled groups.
- `psi_show` (psi.c:1251-1298) never checks `group->enabled`.

**Counterexample:** root writes `0` to `/sys/fs/cgroup/cgroup.pressure`, then memory thrashes. `/proc/pressure/memory` still opens and reads. Its `total=` stays frozen, and the averages decay to 0.00 as later reads compute empty periods (psi.c:1266-1270, 348-351). The tool reports `state: ok`, `PRESSURE_OK`, exit 0. With `--interval`, it reports `total_delta_us: 0`, `stall_ratio: 0.0`. Stopped accounting is read as zero pressure.

**Non-root `cgroup.pressure=0` does not affect `/proc/pressure`:**
- cgroup-v2.rst:1073-1075: "This control attribute is not hierarchical, so disable or enable PSI accounting in a cgroup does not affect PSI accounting in descendants".
- psi.c:793-794: `for_each_group` walks `iter->parent` and calls `psi_group_change` on every ancestor. The disabled group's early return (psi.c:845) affects only that group, so `psi_system` still accrues.
- The disabled cgroup's own pressure files are hidden (cgroup.c:4127-4129), so a census read of that slice's `memory.pressure` fails with ENOENT. That is census and Frontier scope, not C2.

**Related:** booting with `cgroup_disable=pressure` makes `cgroup_psi_enabled()` false (cgroup.c:4161). That disables `psi_cgroups_enabled` (psi.c:236-237), so tasks charge `psi_system` directly (psi.c:888-891). `/proc/pressure` is unaffected, and every cgroup `*.pressure` file is absent (cgroup.c:1799-1801).

**Impacted axes:** coverage (a silent-zero path), calibration (contract :67 and :69 claim "never zero" generally), and adjacency (the switch is operator or tsukuroi configuration; mori only observes it).

**Smallest safe correction, in order of size:**
1. Minimum: in the knowledge entry and the SKILL.md decision table, state that `/proc/pressure` zeros or zero deltas are not evidence of no stall when the root `cgroup.pressure` reads `0`. Record the host's value (`1` today) in the live evidence run.
2. Better, still within the frozen schema: when `--root` is the default, the tool also reads the cgroup2 root `cgroup.pressure` read-only. A `0` marks all four resources `unsupported` with a note `root cgroup.pressure=0: psi_system accounting stopped`. That yields `PRESSURE_UNAVAILABLE`. With a fixture `--root`, the check is skipped, so P01–P12 are unaffected.

Option 2 has no frozen case, so `PASS 12/12` would not exercise it. Adding a P13 changes the declared after-value, so that is a decision for the judge, not something to fix inside this round.

### F4 — The `full` arm for memory and io can never change the verdict; it only duplicates findings (tradeoff, low severity)

Contract :71: PRESSURE_HIGH fires when avg10 ≥ X on `some` of cpu/io/memory "or `full` of memory/io/irq".

- psi.c:247-257: `IO_FULL` is set only inside `if (tasks[NR_IOWAIT])`, which also sets `IO_SOME`. `MEM_FULL` is set only inside `if (tasks[NR_MEMSTALL])`, which sets `MEM_SOME`. The extra `MEM_FULL` at psi.c:871-872 needs the current task to be `in_memstall`. [INFERENCE] That task is counted in `NR_MEMSTALL`, so `MEM_SOME` is also set.
- Because the `full` state is a subset of `some`, per-CPU full time ≤ some time. The same weighting (psi.c:392-393, 409-411) and the monotone floor-and-decay (psi.c:355-359) keep avg10(full) ≤ avg10(some).
- So `full ≥ X` implies `some ≥ X`. Host evidence agrees: memory some 0.43 / full 0.25; io some 6.77 / full 6.51.

**Counterexample:** memory some 25.00, full 12.00. Two `[PRESSURE_HIGH, memory]` findings appear for one condition, and the verdict is the same without the full arm. If findings carry only `id` and `resource` (shared interface), the two cannot be told apart.

**Justified parts:**
- Excluding system cpu `full` is right, because it is hard-zeroed (psi.c:1282-1288).
- Using `full` for irq is right, because it is the only line (psi.c:1274-1277).
- psi.c:1017-1018 (`if (!curr->pid) return;`) and :1033-1040 show that irq `full` counts only IRQ or softirq time taken from a running non-idle task. IRQ load on idle CPUs is invisible, so a low irq full does not mean low IRQ load. The SKILL.md table should say so.
- One local 10.0 % default for every kind is honestly labelled "local, not calibrated" (:70).

**Smallest correction:**
- Add a `kind` field to each finding.
- Either drop `full` of memory and io from the default arm, or keep it as an annotation and document that it adds no verdict information at equal X.

No frozen expectation depends on a duplicate finding: P06 has full = 0.00 in the draft fixture.

### F5 — System cpu `full` is undefined: agree, but a nonzero value is impossible and should be noted (minor)

- psi.rst:57-58: "CPU full is undefined at the system level, but has been reported since 5.13, so it is set to zero for backward compatibility."
- psi.c:1282-1288: `/* CPU FULL is undefined at the system level */ if (!(group == &psi_system && res == PSI_CPU && full)) { ... }` leaves avg and total at 0.
- Host: `full avg10=0.00 avg60=0.00 avg300=0.00 total=0`.

So P02's input (cpu full avg10 40.00, total 987654) cannot come from a v7.2 `/proc/pressure/cpu`. That is fine as a robustness case. When the tool sees a nonzero value, it should add a note saying the source does not look like a v7.2 system file, without changing state or verdict. Notes are not matched by P02, so this is compatible with the frozen cases.

Also, under `--interval`, the cpu `full` delta and ratio are always 0. They need the same `full_system_undefined` handling: report null, or label them so they are not read as "no stall" (contract :67).

### F6 — `psi.rst` cannot source any irq claim (false-provenance risk for SOURCES rows)

- psi.rst:38-39: "exported through the respective file in /proc/pressure/ -- cpu, memory, and io." psi.rst:183-184 lists the cgroup files as "cpu.pressure, memory.pressure, and io.pressure" only.
- init/Kconfig:731-737 has the same three-file wording.

Irq facts must cite:
- psi.c:1273-1277 and 1290-1291, which print only full;
- psi.c:1682-1719, which shows the irq file exists only under `CONFIG_IRQ_TIME_ACCOUNTING` (so its absence gives ENOENT, which P04 models faithfully);
- cgroup-v2.rst:1083-1087 for `irq.pressure`.

A SOURCES row or decision-table line that cites psi.rst for irq would be false provenance.

### F7 — Units agree; "avg10" is an exponentially decaying average sampled about every 2 s, not a 10 s window (documentation precision)

- **Units:** avg values are percent with two decimals. psi.rst:60 says "The ratios (in %)". psi.c:1290 uses the format `avg10=%lu.%02lu`, and loadavg.h:43-44 shows `LOAD_FRAC` gives exactly two digits. psi.c:569-570 clamps each sample at the period, so values never exceed 100.00. `total` is microseconds: psi.rst:62-63 "(in us)" and psi.c:1286-1287 `div_u64(..., NSEC_PER_USEC)`.
- **Total is normalized to wall clock:** psi.c:372-378 says "average them into a single time sample that is normalized to wall clock time", and psi.c:409-411 does it. The total is not summed across CPUs, so contract :73 `stall_ratio = total_delta_us / (S * 1e6)` is a wall-clock share on the same scale as avg/100. Agree.
- **Averages:** psi.c:161-164 has `PSI_FREQ (2*HZ+1) /* 2 sec intervals */`, `EXP_10s 1677 /* 1/exp(2s/10s) */`, and so on. avg10, avg60 and avg300 are decaying averages with 10, 60 and 300 s time constants, updated at most once per ≈2 s (psi.c:1269-1270). Totals are refreshed on every read (psi.c:1266-1268 calls `collect_percpu_times`), so `--interval` deltas are meaningful for any S in (0, 10]. avg10 cannot track sub-2 s changes. The knowledge entry should not call avg10 a "10-second window".
- **`counter_regressed`:** `group->total` only ever increases (psi.c:409-411). A decrease within one boot cannot come from a live kernel; it means the source was swapped or the data is a fixture. The label is sound; the note should say "source changed", not "kernel counter reset".
- **Denominator, for CriticIntervalBoundary:** the denominator `S` is the requested sleep, not the measured time between the two reads. A fully stalled resource can therefore show a ratio slightly above 1.0. Using a measured monotonic elapsed time is the smaller-error choice. The selftest's injected no-op sleep would need to inject the elapsed time too, so this is a trade against P11's frozen `stall_ratio: 0.125`.

## Things I checked that hold

- **Line grammar (:61-63):** it matches psi.c:1290-1291 exactly, a single space between fields and a trailing `\n`. Non-irq resources print two lines (psi.c:1277, `full < 2 - only_full`).
- **Irq data index:** psi_types.h:41-46 and 58-65 give `PSI_IRQ = 3`. `res*2 + 0 = 6 = PSI_IRQ_FULL`, so the single irq line really is IRQ_FULL data. The trigger parser agrees (psi.c:1365).
- **Absent irq (P04):** an absent irq file is a permanent build-config state on kernels without `CONFIG_IRQ_TIME_ACCOUNTING` (psi.c:1717-1719). PARTIAL is correct there. Consumers should know that such hosts never reach `PRESSURE_OK`; that is a tradeoff, not a defect.
- **File mode and safety:** the files are mode 0666 (psi.c:1714-1718; host `ls -l` shows `-rw-rw-rw-`). Unprivileged users can register triggers (psi.rst:107-110), so the tool must open `O_RDONLY` and never write, to honour the "no trigger registration" bound. EACCES or EPERM on read is not produced by psi.c; [INFERENCE] it would come from an LSM or container policy.
- **Host evidence:** `/sys/fs/cgroup/cpu.pressure` equals `/proc/pressure/cpu` byte for byte at the same instant, both `some ... total=1483171` and `full ... total=0`. This confirms psi.h:39 (root cgroup is `psi_system`).

## Counterexample summary for the judge

| ID | Kind | Must the judge reject it? |
|---|---|---|
| F1 | False provenance in contract :68, P05 topic, and spec rows | No. Fixable by relabelling, with no behaviour change |
| F2 | Untested read-path errno; uncaught error would exit 1, the same code as HIGH | No. Fixable in the hook and tool |
| F3 | Silent zero when root `cgroup.pressure=0` | Fixable by documenting it (minimum) or by a read-only check. A test for it would change the declared 12/12, which is the judge's call |
| F4 | Redundant threshold arm | Tradeoff |
| F5, F6, F7 | Precision and provenance hygiene | No |

## Status after amendments A2 and A3 (checked at tip `f38dbbd`)

| Finding | Status | Where |
|---|---|---|
| F1 | Resolved | A2 (contract.md:112-117): PSI disabled gives ENOENT and `absent`; `unsupported` infers no cause; P05 is labelled defensive. The original text at :68 still says "(PSI disabled)", but A2 overrides it |
| F2 | **Open** | :83 still says "in-process open hook". No amendment places the injected EOPNOTSUPP at read, or requires the tool to map errnos at read |
| F3 | **Open** | No amendment mentions root `cgroup.pressure`. A2's bracket check (:118-121) passes on a frozen `psi_system` too: both raw totals are equal, and the tool's total lies between them |
| F4 | **Open** | :71 unchanged |
| F5 | Resolved | P02 is defensive (A2 :116-117); system CPU `full` delta and ratio are null (A3 :130) |
| F6 | Open | Hygiene for the knowledge entry and SOURCES rows |
| F7 | Denominator resolved | A3 :134-135 (nominal `stall_ratio`, optional `elapsed_us`). The "avg10 is not a 10 s window" wording is still for the knowledge entry |

## Not run

- I did not trigger a live EOPNOTSUPP (that needs a `tsc=noirqtime` boot) or a root `cgroup.pressure=0` write. Both are forbidden by the bounds, so F2 and F3 rest on source reading.
- I did not grep the whole kernel tree for other `/proc/pressure` creators.
- The draft tool (`/fast/scratch/hyaku/mori-r24-a2/wt-pressure/tools/mori-pressure.py`) did not exist when I checked, so I did not inspect its error handling.
- The draft cases.json in `wt-cases` is uncommitted (`?? tools/fixtures/`). I read it once, read-only.

## Tooling

No installs or updates. I used `curl`, `python3`, `grep` and `git` (read-only), all already present.
