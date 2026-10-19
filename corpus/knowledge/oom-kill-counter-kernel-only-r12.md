source: S002 — https://docs.kernel.org/admin-guide/cgroup-v2.html — current cgroup-v2 docs, “memory.events”/“memory.events.local” and `oom_kill` (opened 2026-10-19); S003 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c — v7.2 `__oom_kill_process` lines 935–936; S004 — https://raw.githubusercontent.com/torvalds/linux/c03c1a14507dfaf8b856c2608f9ac216021fc222/mm/memcontrol.c — master commit c03c1a14 `__memory_events_show` lines 4965–4966; S007 — https://www.freedesktop.org/software/systemd/man/latest/systemd-oomd.service.html — systemd 262 Description; S011 — https://raw.githubusercontent.com/systemd/systemd/v261/src/oom/oomd-util.c — v261 `oomd_cgroup_kill` lines 269–316; S016 — https://raw.githubusercontent.com/rfjakob/earlyoom/8477c902fce09be26e5668acba05df216871e7ae/README.md — README at commit 8477c902 “What does it do” / “Why not trigger the kernel oom killer?”
verified-at: 2026-10-19 (lane base 20e2255; host kernel 7.2.3-arch1-3, systemd 261 (261.2-1-arch))
recheck: curl -fsSL https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c | grep -nF 'count_vm_event(OOM_KILL)'; curl -fsSL https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c | grep -nF 'memcg_memory_event_mm(mm, MEMCG_OOM_KILL)'; curl -fsSL https://raw.githubusercontent.com/torvalds/linux/c03c1a14507dfaf8b856c2608f9ac216021fc222/mm/memcontrol.c | grep -nF 'atomic_long_read(&events[MEMCG_OOM_KILL])'; grep -c '^oom_kill ' /proc/vmstat → 935: count_vm_event(OOM_KILL); 936: memcg_memory_event_mm(mm, MEMCG_OOM_KILL); 4966: atomic_long_read(&events[MEMCG_OOM_KILL])); 1

## Claim
For the inspected upstream v7.2 implementation, `/proc/vmstat` `oom_kill` and cgroup `memory.events` / `memory.events.local` `oom_kill` are incremented at the kernel OOM-victim path. A zero is only zero in the sampled counter value and scope; it never means no memory-related kills by userspace, nor is it a complete event-history guarantee across destroyed cgroups.

Adjacent: `tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md:245–257,359–367` treats `memory.events oom_kill` as a per-cgroup presence flag, not an event meter; `kill-event-deep-r8.md:120–135` records the counter map. This note adds the upstream increment-site basis and does not promote a sampled row into fleet-wide history.

## Evidence
- S003, `mm/oom_kill.c:935–936`, inside `__oom_kill_process`: “`count_vm_event(OOM_KILL);`” and “`memcg_memory_event_mm(mm, MEMCG_OOM_KILL);`”. The calls precede the kernel's SIGKILL of that OOM victim.
- S004, `mm/memcontrol.c:4965–4966`, prints the cgroup `oom_kill` value from `events[MEMCG_OOM_KILL]`. S002, `memory.events:1448–1458,1491–1494`, defines the field as “The number of processes belonging to this cgroup killed by any kind of OOM killer”; `memory.events.local:1505–1509` makes the local-vs-hierarchical distinction. The documentation phrase is broader than the increment site: cite the implementation, not the description alone.
- S011, v261 `oomd-util.c:269,274–280,306`, records oomd kills in `user.oomd_ooms` and `user.oomd_kill`, using the cgroup kill path and a SIGKILL fallback. S007, systemd 262 Description, describes oomd as selecting a cgroup and sending SIGKILL to its processes. Neither is the kernel OOM-victim path above.
- S016, README master:55–56 describes earlyoom's SIGTERM path; `:68–69` says `--kernel-oom` triggers the kernel OOM killer; the `:148–149` example documents its later SIGKILL stage. Its normal SIGTERM/SIGKILL actions are not kernel OOM kills.
- Host counter key: `grep -c '^oom_kill ' /proc/vmstat` → `1` matching key (presence only; not the scalar value). Mount: `grep -E '^cgroup2 ' /proc/mounts` → `cgroup2 /sys/fs/cgroup cgroup2 rw,nosuid,nodev,noexec,relatime,nsdelegate,memory_recursiveprot,memory_hugetlb_accounting 0 0` (no `memory_localevents`, so `memory.events` is hierarchical).

## Observed
The upstream call sites, cgroup rendering, cgroup-v2 wording, and userspace-killer paths above were re-opened on 2026-10-19. Host `oom_kill` key presence is measured by the command shown; no claim about the scalar's current value is made.

## [INFERENCE]
A userspace killer that directly kills via cgroup control or signals does not execute these kernel OOM accounting calls, so those actions do not increment these counters. `earlyoom --kernel-oom` delegates to the kernel; the counters can move if that route actually reaches a kernel OOM victim. The host kernel is `7.2.3-arch1-3`, while the implementation opened here is upstream v7.2; exact distro-source identity was not checked.

## [UNKNOWN]
No tree-wide sweep of every kernel writer of `OOM_KILL` / `MEMCG_OOM_KILL` was performed; the source-level claim is anchored to the opened v7.2 victim path, not a proof about every downstream kernel. The current scalar value and any userspace kill count were not measured.

## What it changes for mori
For the SKILL.md `Did something get killed?` decision row (`:17`) and `CGROUP_OOM_KILL` error-pattern row (`:28`), label this counter as kernel-OOM-only. Never turn a zero into “no memory kills”; use separate class/event evidence for userspace killers.

## Delivery paths this cannot see
These counters cannot see systemd-oomd's `cgroup.kill` / `kill()` delivery or earlyoom's ordinary SIGTERM/SIGKILL delivery, and do not identify PID, event time, or fleet membership. `earlyoom --kernel-oom` is the explicit delegation exception, not evidence that ordinary earlyoom signals are counted.

## Fills (coverage-map ground; Frontier row)
Coverage-map ground: kernel-vs-userspace OOM counter semantics. Frontier F1: userspace OOM killers and their records; this entry establishes why the kernel counter is not a substitute.
