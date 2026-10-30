corpus/knowledge/psi-v73-recheck-r61.md
=======================================

source: recheck of `corpus/knowledge/system-pressure-r24.md` (v7.2 line
anchors) against Linux v7.3, per the entry's `recheck:` trigger and the
round-53 release-recheck rule (`corpus/knowledge/kernel-v7.3-recheck-r53.md`).
verified-at: 2026-10-30 (round 61; six v7.3 copies pinned under
`corpus/evidence/sources-r61/`, sha256 in `.ufo/waves/round-61/count-c2.py`
`PINS`; fetch receipts `.ufo/waves/round-61/w1/Mo61ExecFetch.md`; v7.2
baseline sha256s in the round lesson `## Gate`)
recheck: on the next kernel release that touches `kernel/sched/psi.c`,
`include/linux/psi_types.h`, `Documentation/accounting/psi.rst`,
`Documentation/admin-guide/cgroup-v2.rst`, `init/Kconfig` PSI help, or
`Documentation/admin-guide/kernel-parameters.txt` (v7.4 gate)

One row per v7.2 line pointer the r24 entry enumerates (deduped, in
first-mention order). `same` = byte-identical at the same v7.3 lines;
`moved` = byte-identical at the stated new span; `changed` = span text
differs at the stated v7.3 span (difflib-mapped). The anchor column keeps
the r24 v7.2 pointer; the location column is a v7.3 span.

| anchor (v7.2) | status | v7.3 location | quote |
|---|---|---|---|
| psi.rst:60-65 | same | - | `(in us) is tracked and exported as well, to allow detection of latency` |
| psi.c:342-360 | same | - | `/* Fill in zeroes for periods of no activity */` |
| psi.c:1268-1270 | same | - | `group->avg_next_update = update_averages(group, now);` |
| psi.c:1372-1373 | same | - | `if (window_us == 0 || window_us > WINDOW_MAX_US)` |
| psi.c:1379-1380 | same | - | `if (!privileged && window_us % 2000000)` |
| psi.c:1712 | same | - | `if (psi_enable) {` |
| psi.c:1017 | same | - | `if (!curr->pid)` |
| psi.c:1540 | same | - | `return psi_show(m, &psi_system, PSI_IO);` |
| psi.c:1686 | same | - | `return psi_show(m, &psi_system, PSI_IRQ);` |
| psi.rst:36-38 | same | - | `Pressure information for each resource is exported through the` |
| psi.c:1710-1721 | same | - | `proc_create("pressure/cpu", 0666, NULL, &psi_cpu_proc_ops);` |
| Kconfig:730-731 | moved | Kconfig:736-737 | `If you say Y here, the kernel will create /proc/pressure/ with the` |
| psi.rst:40-43 | same | - | `full avg10=0.00 avg60=0.00 avg300=0.00 total=0` |
| psi.c:1290-1296 | same | - | `full || only_full ? "full" : "some",` |
| psi.rst:45-56 | same | - | `The "some" line indicates the share of time in which at least some` |
| psi.rst:57-59 | same | - | `CPU full is undefined at the system level, but has been reported` |
| psi.c:1282-1288 | same | - | `if (!(group == &psi_system && res == PSI_CPU && full)) {` |
| psi.c:1284-1288 | same | - | `for (w = 0; w < 3; w++)` |
| psi.c:160-164 | same | - | `/* Running averages - we need to be higher-res than loadavg */` |
| psi.c:1268 | same | - | `collect_percpu_times(group, PSI_AVGS, NULL);` |
| psi.c:1269-1270 | same | - | `if (now >= group->avg_next_update)` |
| psi.c:600-602 | same | - | `if (now >= group->avg_next_update) {` |
| psi.c:1273-1296 | same | - | `for (full = 0; full < 2 - only_full; full++) {` |
| psi.c:1032-1042 | same | - | `if (group->rtpoll_states & (1 << PSI_IRQ_FULL))` |
| psi.c:1364-1367 | same | - | `if (res == PSI_IRQ && --state != PSI_IRQ_FULL)` |
| psi_types.h:41-49 | same | - | `enum psi_res {` |
| psi.c:1717-1719 | same | - | `proc_create("pressure/irq", 0666, NULL, &psi_irq_proc_ops);` |
| psi.c:1260-1263 | same | - | `if (!irqtime_enabled() && res == PSI_IRQ)` |
| psi.c:1257-1258 | same | - | `return -EOPNOTSUPP;` |
| psi.c:228-240 | same | - | `if (!psi_enable) {` |
| psi.c:149-158 | same | - | `return kstrtobool(str, &psi_enable) == 0;` |
| psi.c:1553-1566 | same | - | `static int psi_cpu_open(struct inode *inode, struct file *file)` |
| psi.c:1711-1719 | same | - | `proc_create("pressure/io", 0666, NULL, &psi_io_proc_ops);` |
| kernel-parameters.txt:5505-5507 | moved | kernel-parameters.txt:5540-5542 | `psi=		[KNL] Enable or disable pressure stall information` |
| Kconfig:743-760 | moved | Kconfig:749-766 | `If you are paranoid and not sure what the kernel will be` |
| psi.rst:67-88 | same | - | `Users can register triggers and use poll() to be woken up when resource` |
| psi.rst:102-104 | same | - | `monitoring update interval is 50ms and max is 1s. Min limit is set to` |
| psi.c:167 | same | - | `#define WINDOW_MAX_US 10000000	/* Max window size is 10s */` |
| psi.c:1596-1598 | same | - | `if (seq->private) {` |
| psi.rst:178-187 | same | - | `Per-cgroup psi monitors can be specified and used the same way as` |
| cgroup-v2.rst:1066-1081 | same | - | `A read-write single value file that allowed values are "0" and "1".` |
| psi.c:408-410 | same | - | `for (s = 0; s < NR_PSI_STATES - 1; s++)` |
| psi.rst:70-88 | same | - | `time window, e.g. 100ms of total stall time within any 500ms window to` |
| psi.c:845-857 | same | - | `* avoid a delta sample underflow when PSI is later re-enabled.` |
| psi.c:551 | same | - | `sample = group->total[PSI_AVGS][s] - group->avg_total[s];` |
| psi.c:1538-1550 | same | - | `static int psi_cpu_show(struct seq_file *m, void *v)` |
| cgroup-v2.rst:1066-1087 | same | - | `The reason this control attribute exists is that PSI accounts stalls for` |

