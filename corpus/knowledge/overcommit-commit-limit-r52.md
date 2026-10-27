# CommitLimit and Committed_AS: the overcommit ledger, enforced only under mode 2

source: S497 — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/mm/overcommit-accounting.rst — docs, tier A, Documentation/mm/overcommit-accounting.rst at tag v7.2 (the three modes, the accounting rules), opened 2026-10-26
source: S498 — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/sysctl/vm.rst — docs, tier A, Documentation/admin-guide/sysctl/vm.rst at tag v7.2 (overcommit_memory, overcommit_ratio, overcommit_kbytes, the two reserves), opened 2026-10-26
source: S499 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/util.c — code, tier A, mm/util.c at tag v7.2 (vm_commit_limit, __vm_enough_memory, vm_memory_committed, the policy switch), opened 2026-10-26
source: S500 — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/mman.h — code, tier A, include/linux/mman.h at tag v7.2 (vm_acct_memory, vm_unacct_memory), opened 2026-10-26
source: S501 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/mmap.c — code, tier A, mm/mmap.c at tag v7.2 (MAP_NORESERVE handling, the reserve initialisers), opened 2026-10-26
verified-at: 2026-10-26
recheck: on-release — `for u in https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/mm/overcommit-accounting.rst https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/sysctl/vm.rst https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/util.c https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/mman.h https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/mmap.c; do curl -fsSL "$u" | sha256sum; done` -> 767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f, bf8ca0265fefc019250697b6ee47a0679709b2ee45f4d1893b3dfd95c1f8c1ce, e702754c45bd7bd69e5da22a6505c9c1016eaafe6e883b746cc3cdbd413ebe7c, d7bf787c910d9a7cbabee3a50c512ce3aad78d63659b0c968adca16b5916b058, 449b858385c7ece0ff88a8b41893efadb70a437fb8585a296c4ef0461a4c1545
coverage-map: resource runway (new ground; no FR row held it; sweep `.ufo/waves/round-52/evidence/sweep-overcommit.txt`)

mori reports resource runway. Round 51 said what `MemAvailable` is: an estimate of how much memory can be given to
new work before swapping. This entry covers the other two runway lines of `/proc/meminfo`, `CommitLimit` and
`Committed_AS`, printed at `fs/proc/meminfo.c:125-126` in the round-51 copy (S494, as `vm_commit_limit()` and
`vm_memory_committed()`). They answer a different question: can an allocation be *refused* (ENOMEM at request time)
before memory runs out? At v7.2 the answer depends on `vm.overcommit_memory`. Under mode 2 the kernel refuses a
request once the committed total would reach the limit. Under the default mode 0 it refuses only a single request
larger than all RAM plus swap. Under mode 1 it never refuses. `CommitLimit` is printed under every mode, but it is
enforced only under mode 2.

## Claims

| claim | source | quote |
|---|---|---|
| Mode 0 is the default and refuses only allocations that are plainly too large, so it still lets the host overcommit. | S497 | `Heuristic overcommit handling. Obvious overcommits of address space are refused. Used for a typical system.` |
| Only under mode 2 is the committed total capped, at swap plus a share of RAM that defaults to one half. | S497 | `The total address space commit for the system is not permitted to exceed swap + a configurable amount (default is 50%) of physical RAM.` |
| Under mode 2 the documented failure is an allocation error at request time rather than a kill when pages are later touched. | S497 | `in most situations this means a process will not be killed while accessing pages but will receive errors on memory allocation as appropriate.` |
| The documentation says the current limit and the committed amount are both published by the kernel for reading, as two meminfo lines. | S497 | `The current overcommit limit and amount committed are viewable in` |
| Under mode 2 a mapping request carrying MAP_NORESERVE is still charged against the commit limit. | S497 | `In mode 2 the MAP_NORESERVE flag is ignored.` |
| Shared and read-only file mappings add nothing to the committed total, because the file itself backs those pages. | S497 | `SHARED or READ-only - 0 cost (the file is the map not swap)` |
| The documentation still lists ptrace pages as unaccounted, so the committed total is not a complete ledger of every commitment. | S497 | `To Do ===== * Account ptrace pages (this is hard)` |
| In mode 0 a single request is compared with all RAM plus all swap, not with what is currently free. | S498 | `When this flag is 0, the kernel compares the userspace memory request size against total memory plus swap and rejects obvious overcommits.` |
| Mode 1 never refuses an allocation on commit grounds; the kernel behaves as though memory were unlimited until it is exhausted. | S498 | `When this flag is 1, the kernel pretends there is always enough memory until it actually runs out.` |
| The ratio setting is a percentage cap on physical RAM that applies only in mode 2, with swap added on top. | S498 | `When overcommit_memory is set to 2, the committed address space is not permitted to exceed swap plus this percentage of physical RAM.` |
| The kbytes and ratio knobs are mutually exclusive, so a ratio that reads 0 can simply mean the kbytes knob is in force. | S498 | `Only one of them may be specified at a time. Setting one disables the other (which then appears as 0 when read).` |
| Mode 2 also holds back a user reserve sized from the requesting process and capped by the user_reserve_kbytes knob. | S498 | `When overcommit_memory is set to 2, "never overcommit" mode, reserve min(3% of current process size, user_reserve_kbytes) of free memory.` |
| The admin reserve exists so that root can still log in and kill a runaway process when memory runs short. | S498 | `That should provide enough for the admin to log in and kill a process, if necessary, under the default overcommit 'guess' mode.` |
| CommitLimit is RAM minus hugetlb pages, scaled by the ratio percentage, with every swap page then added on top. | S499 | `allowed = ((totalram_pages() - hugetlb_total_pages()) * sysctl_overcommit_ratio / 100); allowed += total_swap_pages;` |
| When the kbytes knob is nonzero it replaces the ratio term entirely, after conversion from kilobytes to pages. | S499 | `if (sysctl_overcommit_kbytes) allowed = sysctl_overcommit_kbytes >> (PAGE_SHIFT - 10);` |
| In the default heuristic mode a request fails only when its own size exceeds all RAM plus all swap together. | S499 | `if (pages > totalram_pages() + total_swap_pages) goto error; return 0;` |
| Every request is charged to the committed counter before the mode is examined, so the counter grows under modes 0 and 1 too. | S499 | `vm_acct_memory(pages); /* * Sometimes we want to use more memory than we have */ if (sysctl_overcommit_memory == OVERCOMMIT_ALWAYS) return 0;` |
| The never-overcommit test compares a fast approximate read of the per-CPU committed counter with the computed limit. | S499 | `if (percpu_counter_read_positive(&vm_committed_as) < allowed) return 0;` |
| Processes lacking CAP_SYS_ADMIN see the mode-2 limit lowered further by the admin reserve, converted to pages. | S499 | `if (!cap_sys_admin) allowed -= sysctl_admin_reserve_kbytes >> (PAGE_SHIFT - 10);` |
| A refused request leaves a rate-limited kernel log warning that names the pid, the command and the byte count. | S499 | `pr_warn_ratelimited("%s: pid: %d, comm: %s, bytes: %lu not enough memory for the allocation\n",` |
| The compiled-in default for the ratio knob is fifty, meaning half of physical RAM under mode 2. | S499 | `static int sysctl_overcommit_ratio __read_mostly = 50;` |
| Under the loose modes the per-CPU counter may drift far from its true sum, which is why switching to mode 2 syncs every CPU first. | S499 | `The deviation of sync_overcommit_as could be big with loose policy * like OVERCOMMIT_ALWAYS/OVERCOMMIT_GUESS.` |
| Charging the committed total is a batched add into a per-CPU counter, not a write to one global variable. | S500 | `static inline void vm_acct_memory(long pages) { percpu_counter_add_batch(&vm_committed_as, pages, vm_committed_as_batch); }` |
| Releasing a commitment uses the same batched add with the page count negated. | S500 | `static inline void vm_unacct_memory(long pages) { vm_acct_memory(-pages); }` |
| For ordinary mappings MAP_NORESERVE drops commit charging only when the mode is something other than never-overcommit. | S501 | `We honor MAP_NORESERVE if allowed to overcommit */ if (sysctl_overcommit_memory != OVERCOMMIT_NEVER) vm_flags \|= VM_NORESERVE;` |
| Hugetlb file mappings are charged strictly unless the caller passes MAP_NORESERVE, a carve-out the mode-2 rule does not mention. | S501 | `hugetlb applies strict overcommit unless MAP_NORESERVE */ if (file && is_file_hugepages(file)) vm_flags \|= VM_NORESERVE;` |
| At boot the user reserve knob is set to the smaller of one thirty-second of free memory and 128 MiB. | S501 | `sysctl_user_reserve_kbytes = min(free_kbytes / 32, SZ_128K);` |
| At boot the admin reserve knob is set to the smaller of one thirty-second of free memory and 8 MiB. | S501 | `sysctl_admin_reserve_kbytes = min(free_kbytes / 32, SZ_8K);` |

## Reading rules (mori)

| reading | what it means at v7.2 | what it does not mean |
|---|---|---|
| `Committed_AS` > `CommitLimit` under mode 0 or 1 | normal: the limit is printed, not enforced (`util.c.v7.2:969-977`) | memory pressure, or an imminent OOM kill |
| `Committed_AS` near `CommitLimit` under mode 2 | new private writable mappings, `brk` and `fork` can fail with ENOMEM before `MemAvailable` is low | that running processes will be killed: mode 2 refuses at request time |
| kernel line `__vm_enough_memory: pid: N, comm: X, bytes: B not enough memory for the allocation` | a commit refusal (rate-limited, so not a count) | an OOM kill; the OOM report is a different block (`oom-memcg-stat-r50.md`) |
| `vm.overcommit_ratio` reads 0 | possibly `vm.overcommit_kbytes` in force (setting one zeroes the other) | that the limit is swap only |

A host read needs `/proc/sys/vm/overcommit_memory` with the two meminfo lines; mori reads them and never writes a
`vm.*` sysctl. Choosing or changing the overcommit mode is host configuration, which the operator owns. Host
OS-state triage is tsukuroi's ground (`../tsukuroi-shokunin/PROVINCE.md:8-14,28`: detection and report, the operator
remediates); this entry claims no sysctl ownership for either lane.

## Boundaries

- The entry claims what the v7.2 bytes say; other kernels and this host's sysctl values are not claimed.
- `Committed_AS` is a per-CPU counter; the meminfo line is its full sum (`util.c.v7.2:937-940`), and the mode-2
  test uses a cheaper approximate read (`util.c.v7.2:994`). The two can differ by up to the batch size per CPU.
- The ledger has known holes: ptrace pages are listed as unaccounted (S497), and hugetlb file mappings with
  `MAP_NORESERVE` stay uncharged even under mode 2 (S501).
- No threshold for `Committed_AS/CommitLimit` is proposed (FR8 stays open).
