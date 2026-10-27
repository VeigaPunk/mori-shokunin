# Hardware memory-failure kills at Linux v7.3: the kill a census of OOM lines does not see

source: S521 — Linux mm/memory-failure.c at tag v7.3 — https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/memory-failure.c?h=v7.3 — committed copy `corpus/evidence/sources-r54/memory-failure.c.v7.3` (sha256 `94d24a605b61…`)
source: S522 — Linux Documentation/mm/hwpoison.rst at tag v7.3 — copy `corpus/evidence/sources-r54/hwpoison.rst.v7.3`; S523 — Documentation/ABI/stable/sysfs-devices-node at v7.3 — copy `corpus/evidence/sources-r54/sysfs-devices-node.v7.3`; S524 — include/trace/events/memory-failure.h at v7.3 — copy `corpus/evidence/sources-r54/memory-failure-trace.h.v7.3`
source: S507 — Documentation/admin-guide/sysctl/vm.rst at v7.3 (copy `corpus/evidence/sources-r53/vm.rst.v7.3`); S502 — Documentation/filesystems/proc.rst at v7.3 (copy `corpus/evidence/sources-r53/proc.rst.v7.3`)
verified-at: 2026-10-27 — every quote located in the committed v7.3 copy by `python3 .ufo/waves/round-54/count-c2.py <rev>`; host read 2026-10-27 on kernel 7.2.11-arch1-1 (`.ufo/waves/round-54/evidence/sweeps.txt`)
recheck: on-release — re-fetch the six files at the new tag and re-run `count-c2.py`; on this host, re-read `/sys/devices/system/node/node*/memory_failure/*`, `HardwareCorrupted` and `/proc/sys/vm/memory_failure_*` when the kernel moves past 7.2
coverage-map: kill and OOM events — a kill class outside the OOM killer (README `## Round-54 coverage additions`)
author: MoriR54 (L1); the wave's ENTAILMENT voters judge each row (`.ufo/waves/round-54/w1/Mo54En*.md`)

## Claim

The kernel kills processes for a reason other than memory exhaustion. When hardware reports a corrupted page
(an uncorrected ECC error, a machine check), `mm/memory-failure.c` unmaps the page and signals the processes that
map it: **SIGBUS** with a machine-check code, or **SIGKILL** when the unmap failed. None of this passes through the
OOM killer, so it raises no `oom_kill` count in `memory.events`, prints no `Out of memory` or `oom-kill:` line and
emits no `oom:mark_victim` event. A census that reads only OOM evidence will see a process die with no cause on
record. The evidence the kernel does leave is its own: lines under the prefix `Memory failure:`, five per-node
counters, the `HardwareCorrupted` line of `/proc/meminfo`, and the `ras:memory_failure_event` tracepoint.

## Claims (located quotes, v7.3)

| claim | source | quote |
|---|---|---|
| Every message the memory-failure handler prints starts with the same prefix, "Memory failure:", which names the kernel component that wrote the line. | S521 | `#define pr_fmt(fmt) "Memory failure: " fmt #include <linux/kernel.h>` |
| Before signalling a process that maps a poisoned page, the handler logs at error level the page frame number, the command name and the pid. | S521 | `pr_err("%#lx: Sending SIGBUS to %s:%d due to hardware memory corruption\n", pfn, t->comm, task_pid_nr(t));` |
| A task that consumed the poisoned data itself is sent a forced SIGBUS whose code is BUS_MCEERR_AR, meaning action required. | S521 | `if ((flags & MF_ACTION_REQUIRED) && (t == current)) ret = force_sig_mceerr(BUS_MCEERR_AR,` |
| Other processes sharing the page are signalled through the ordinary path, deliberately not forced, so they may block the signal for a while. | S521 | `Don't use force here, it's convenient if the signal * can be temporarily blocked.` |
| When unmapping the corrupted page failed, the process receives SIGKILL instead of SIGBUS and the log line says it was forcibly killed. | S521 | `pr_err("%#lx: forcibly killing %s:%d because of failure to unmap corrupted page\n", pfn, tk->tsk->comm, task_pid_nr(tk->tsk)); do_send_sig_info(SIGKILL,` |
| A signal that could not be delivered gets its own error line, so a sending line alone does not prove that the process received anything. | S521 | `pr_err("%#lx: Cannot send advisory machine check signal to %s:%d\n",` |
| Each handled page ends in one error-level line that names the page type and the outcome of the recovery attempt. | S521 | `pr_err("%#lx: recovery action for %s: %s\n", pfn, action_page_types[type], action_name[result]);` |
| The outcome printed in that line is one of four fixed words, so a parser can classify every recovery line exactly. | S521 | `[MF_IGNORED] = "Ignored", [MF_FAILED] = "Failed", [MF_DELAYED] = "Delayed", [MF_RECOVERED] = "Recovered",` |
| Only the Recovered and Delayed outcomes count as success for the caller; Ignored and Failed make the recovery step return an error. | S521 | `return (result == MF_RECOVERED \|\| result == MF_DELAYED) ? 0 : -EBUSY;` |
| The per-node counters advance in the recovery step for every page type except pages already poisoned and raw PFN mappings, so a repeated failure of a poisoned page is not counted again. | S521 | `if (type != MF_MSG_ALREADY_POISONED && type != MF_MSG_PFN_MAP) { num_poisoned_pages_inc(pfn); update_per_node_mf_stats(pfn, result); }` |
| The v7.3 panic switch fires only when a reserved kernel page is reported with the Ignored outcome, and it is off unless set. | S521 | `if (!sysctl_panic_on_unrecoverable_mf) return false; return type == MF_MSG_KERNEL && result == MF_IGNORED;` |
| In early-kill mode the signal goes out when the background check finds the error, before any process touches the page again. | S522 | `Send SIGBUS to the application as soon as the error is detected` |
| Late kill is the default: a process is signalled only when it runs into the page, so the kill can come long after the error was detected. | S522 | `Send SIGBUS when the application runs into the corrupted page. This is best for memory error unaware applications and default` |
| With recovery switched off, no process is killed for a memory error because the whole machine panics instead. | S522 | `vm.memory_failure_recovery sysctl set to zero: All memory failures cause a panic. Do not attempt recovery.` |
| An early-kill SIGBUS can be caught and handled, so a logged signal need not be followed by the death of that process. | S507 | `The kill is done using a catchable SIGBUS with BUS_MCEERR_AO, so processes can handle this if they want to.` |
| Version 7.3 adds a sysctl that turns an unrecoverable error on kernel-owned pages into a panic, where the default ignores it and keeps running. | S507 | `When enabled, this sysctl triggers a panic on memory failure events hitting kernel-owned pages that the handler cannot recover:` |
| Each NUMA node exposes in sysfs a running total of raw poisoned pages, readable without the kernel log. | S523 | `The total number of raw poisoned pages (pages containing corrupted data due to memory errors) on a NUMA node.` |
| The ignored counter on a node counts pages the kernel gave up recovering, usually because that page type has no recovery support. | S523 | `Of the raw poisoned pages on a NUMA node, how many pages are ignored by memory error recovery attempt,` |
| The tracepoint belongs to the ras trace system for historical reasons, so it is enabled as ras:memory_failure_event and not under oom. | S524 | `For historical versions, memory_failure_event is in ras subsystem, * some user programs depend on it. */ #define TRACE_SYSTEM ras` |
| The traced line repeats the page type and outcome strings of the logged recovery line after the pfn, so traced and logged outcomes can be matched. | S524 | `TP_printk("pfn %#lx: recovery action for %s: %s",` |
| The meminfo field reports, in kilobytes for the whole host, how much memory the kernel has marked as corrupted. | S502 | `HardwareCorrupted The amount of RAM/memory in KB, the kernel identifies as corrupted.` |

## Decision table — reading a death that has no OOM record

Count with the structured surfaces (the per-node counters, `HardwareCorrupted`); read the kernel lines only to
attribute an event the counters already show. The lines are kernel text with no `MESSAGE_ID`, so a tally of them
is a text-selected record count, never a structured count (QUALITY 15).

| evidence on the host | what it means | what it does not mean |
|---|---|---|
| `Memory failure: 0x…: Sending SIGBUS to <comm>:<pid> due to hardware memory corruption` | the handler signalled that process for a poisoned page it maps (early kill, `BUS_MCEERR_AO`) or touched (`BUS_MCEERR_AR`, forced) | that the process died: the AO signal is catchable, and a `Cannot send advisory machine check signal` line means it was not delivered |
| `Memory failure: 0x…: forcibly killing <comm>:<pid> because of failure to unmap corrupted page` | SIGKILL from the memory-failure handler | an OOM kill; `memory.events oom_kill` does not move |
| `Memory failure: 0x…: recovery action for <page type>: Ignored\|Failed\|Delayed\|Recovered` | one handled page and its outcome; the per-node counter of that outcome and `total` advance (not for `already poisoned page` or `non struct page pfn`) | which process, if any, was signalled — read the SIGBUS/SIGKILL lines for that |
| `/sys/devices/system/node/node<N>/memory_failure/{total,ignored,failed,delayed,recovered}` above 0 | pages poisoned on that node since boot, by outcome | a kill: a free or clean page can be recovered with no process signalled |
| `HardwareCorrupted:` above `0 kB` in `/proc/meminfo` | memory the kernel has marked poisoned, host-wide | which node or which process |
| a panic `Memory failure: 0x…: unrecoverable page` | v7.3 `panic_on_unrecoverable_memory_failure` was 1 and a reserved kernel page came back Ignored | a process kill — the host went down |
| no line and all counters 0 (this host, 2026-10-27) | no memory failure handled since boot | that the hardware is healthy: corrected errors are counted by EDAC/rasdaemon, not here |

| sysctl (v7.3) | value → behaviour |
|---|---|
| `vm.memory_failure_recovery` | 1 (default): attempt recovery and kill per mode; 0: every memory failure panics |
| `vm.memory_failure_early_kill` | 0 (default, this host): unmap everywhere, signal only a process that later touches the page; 1: signal every process mapping it as soon as the error is found |
| `vm.panic_on_unrecoverable_memory_failure` | new in v7.3, absent on this host's 7.2.11; 1: panic when a kernel-owned page cannot be recovered; 0 (default): ignore and continue |

## On this host (read-only, 2026-10-27)

Kernel 7.2.11-arch1-1: `node0/memory_failure/{total,ignored,failed,delayed,recovered}` all `0`,
`HardwareCorrupted: 0 kB`, `memory_failure_recovery` 1, `memory_failure_early_kill` 0, `enable_soft_offline` 1;
`/proc/sys/vm/panic_on_unrecoverable_memory_failure` does not exist (the v7.3 switch is not in 7.2). No line of
this class has been observed live; every row above is read from source.

## Boundaries

- Detection and report only. Mori never injects poison (`madvise(MADV_HWPOISON)`, the hwpoison-inject debugfs files
  the documentation lists for testing), never unpoisons a page and never writes a memory-failure sysctl; those are
  host-repair actions (tsukuroi / operator ground).
- Corrected-error accounting (EDAC, `rasdaemon`, MCE decoding) is hardware-health ground this entry does not hold:
  it covers what the kernel does once a page is declared poisoned, not how the error was detected.
- Soft offline (`enable_soft_offline`, migration of a page with corrected errors) kills nothing and is out of scope
  here.
- The rows are v7.3 bytes; the host runs 7.2.11. The kill and recovery lines, the counters and the two older
  sysctls exist on 7.2 as read live above; the panic switch does not.
