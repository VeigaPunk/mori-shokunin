source: S571 (kernel/sched/psi.c at tag v7.3, cgroup pressure interface scope;
pinned copy `corpus/evidence/sources-r61/psi.c` sha256 c4edc1e7…) and S568
(Documentation/admin-guide/cgroup-v2.rst at tag v7.3; pinned copy
`corpus/evidence/sources-r61/cgroup-v2.rst` sha256 2750c11a…)
verified-at: 2026-10-30 (round 62; claims below are line-located against the
pinned copies; counting command
`python3 .ufo/waves/round-62/count-c2.py <rev>`)
recheck: on-release (re-open S571/S568 when a kernel release touches
kernel/sched/psi.c or the cgroup-v2 PSI interface files)

# Reading per-cgroup pressure files (round 62, FR12 remainder)

Scope: detection and report only. This entry grounds `tools/mori-cgroup-pressure.py`
(round-62 build): a one-shot, read-only survey of `<cgroup>/{cpu,memory,io,irq}.pressure`
plus the group's `cgroup.pressure` accounting switch. It complements, and does not
replace, the round-24 system-wide read (`mori-pressure.py`, `/proc/pressure/*`): the
system files are the same `psi_show()` over `psi_system` (K12), so the two probes read
one code path at two scopes. Claims:

- **K1** — `psi.c:1251` — `int psi_show(struct seq_file *m, struct psi_group *group, enum psi_res res)`: one show path serves both the system files and every cgroup pressure file; the group argument is the only difference.
- **K2** — `psi.c:1257-1258` — `if (static_branch_likely(&psi_disabled)) return -EOPNOTSUPP;`: with PSI disabled the reader reports EOPNOTSUPP, never zeros; an unavailable read is not evidence of no stall.
- **K3** — `psi.c:1261-1262` — `if (!irqtime_enabled() && res == PSI_IRQ) return -EOPNOTSUPP;`: IRQ pressure exists only when CONFIG_IRQ_TIME_ACCOUNTING accounting is on; on hosts without it the irq file is missing — absent, not zero.
- **K4** — `psi.c:1274` — `only_full = res == PSI_IRQ;`: the IRQ resource is declared full-only at the source of the format loop.
- **K5** — `psi.c:1277` — `for (full = 0; full < 2 - only_full; full++) {`: when `only_full` holds the loop emits exactly one line, so an IRQ pressure file carries `full` and no `some` line; a `some` line there is malformed, not a second sample.
- **K6** — `psi.c:1283` — `if (!(group == &psi_system && res == PSI_CPU && full)) {`: the CPU `full` line is skipped only for the system group, so per-cgroup `cpu.pressure` carries both `some` and `full`; the round-24 system-level "cpu full undefined" note does not extend to cgroups.
- **K7** — `psi.c:1112` — `int psi_cgroup_alloc(struct cgroup *cgroup)`: each cgroup gets its own PSI group at alloc time; per-cgroup numbers are first-class, not a division of the system numbers.
- **K8** — `psi.c:1216` — `void psi_cgroup_restart(struct psi_group *group)`: cgroup PSI groups are re-armed on hierarchy changes, so a cgroup's counters reflect its own membership window.
- **K9** — `cgroup-v2.rst:1246` — `This file accounts for all the processes in the cgroup.`: `cpu.pressure` covers exactly the cgroup's processes — the fleet-relevant scope for lane workloads running in `user.slice`.
- **K10** — `cgroup-v2.rst:1073-1074` — `This control attribute is not hierarchical, so disable or enable PSI`: the `cgroup.pressure` switch acts per cgroup only; a "0" here silences this group's accounting while descendants keep theirs — zeros downstream of a "0" are not evidence of no stall.
- **K11** — `cgroup-v2.rst:1086` — `Shows pressure stall information for IRQ/SOFTIRQ. See`: `irq.pressure` is a documented cgroup interface file, so probing it per cgroup is in-contract, not a /proc extrapolation.
- **K12** — `psi.c:1540` — `return psi_show(m, &psi_system, PSI_IO);`: the `/proc/pressure/io` handler wraps the same `psi_show` over `psi_system`; the round-24 tool and this tool therefore differ in scope, not in mechanism.

Limits (declared): the tool reads file bytes and never infers a cause — EOPNOTSUPP
paths (K2, K3) surface as absent/unavailable states, never as kernel diagnosis
(tsukuroi-owned). Thresholds stay local placeholders (FR8 open). No PSI trigger is
registered; the tool is a one-shot read and never writes cgroupfs. A zero or
non-advancing `total` is not evidence of no stall (K10; the round-24 carried limit).
Coverage-map: advances FR12's cgroup-scoped arm only; event-driven watchers stay
frontier.
