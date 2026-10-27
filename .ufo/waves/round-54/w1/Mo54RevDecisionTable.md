# Mo54RevDecisionTable — the two decision tables of `corpus/knowledge/memory-failure-kills-r54.md` at `78295c76`

Scope: the entry's evidence decision table (`## Decision table — reading a death that has no OOM record`, 7 rows)
and its sysctl table (3 rows), checked against the committed copies S521 `corpus/evidence/sources-r54/memory-failure.c.v7.3`,
S522 `corpus/evidence/sources-r54/hwpoison.rst.v7.3`, S507 `corpus/evidence/sources-r53/vm.rst.v7.3`,
S523 `corpus/evidence/sources-r54/sysfs-devices-node.v7.3`, plus S502 `corpus/evidence/sources-r53/proc.rst.v7.3`
for the `HardwareCorrupted` cell; then the SKILL.md round-54 rows for operator actionability. Line-text rule:
format string → printed form with `pr_fmt` = `"Memory failure: "` (`memory-failure.c.v7.3:37`) and `%#lx` → `0x…`.

Evidence base: the entry file in the working tree is byte-identical to the data commit —
`git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 78295c764093ff1f6cee08d7246679900bde7265 -- corpus/knowledge/memory-failure-kills-r54.md`
printed nothing, rc 0. The SKILL.md round-54 rows are a working-tree draft, not in the data commit:
`git show 78295c764093ff1f6cee08d7246679900bde7265:SKILL.md | grep -c "Memory failure"` → `0`, and
`git status --porcelain` lists `M SKILL.md`; I reviewed the draft as it stands. Pin check:
`sha256sum corpus/evidence/sources-r54/memory-failure.c.v7.3` →
`94d24a605b61f94ad1d10ab3db26aed12cb6113af15431ff873da5b98ca48003`, matching the entry's S521 pin `94d24a605b61…`.
Disk guard before work: `scripts/hyaku/disk-guard.sh status` → `/fast/scratch/hyaku 26% 596.7G` free; scratch
`/fast/scratch/hyaku/mori-r54/Mo54RevDecisionTable/` (removed at the end).

## What held (row by row, file:line in the committed copies)

| checked | evidence | verdict |
|---|---|---|
| row 1 line text `Memory failure: 0x…: Sending SIGBUS to <comm>:<pid> due to hardware memory corruption` | `pr_err("%#lx: Sending SIGBUS to %s:%d due to hardware memory corruption\n", pfn, t->comm, task_pid_nr(t));` S521:292-293 + pr_fmt S521:37 | exact |
| row 1 means: early kill `BUS_MCEERR_AO` vs touched `BUS_MCEERR_AR` forced | AR branch `(flags & MF_ACTION_REQUIRED) && (t == current)` → `force_sig_mceerr(BUS_MCEERR_AR, …)` S521:295-297; else `send_sig_mceerr(BUS_MCEERR_AO, …)` with the comment "Don't use force here, it's convenient if the signal can be temporarily blocked." S521:299-303; early-kill population = `PF_MCE_EARLY` thread or the global sysctl (`find_early_kill_thread` S521:500-511, `task_early_kill` S521:513-522) | holds |
| row 2 line text `…: forcibly killing <comm>:<pid> because of failure to unmap corrupted page` | S521:470-472, `do_send_sig_info(SIGKILL, …)` S521:473-474 | exact |
| row 2 means "SIGKILL from the memory-failure handler"; does-not-mean "an OOM kill; `memory.events oom_kill` does not move" | the SIGKILL is sent by `kill_procs` in the handler's force-kill branch S521:468-474; nothing in the file touches memcg OOM accounting | holds |
| row 3 line text `…: recovery action for <page type>: Ignored\|Failed\|Delayed\|Recovered` | `pr_err("%#lx: recovery action for %s: %s\n", pfn, action_page_types[type], action_name[result]);` S521:1291-1292; `action_name` has exactly the four words S521:871-876 | exact |
| row 3 means: per-node counter of that outcome and `total` advance, not for `already poisoned page` / `non struct page pfn` | gate `if (type != MF_MSG_ALREADY_POISONED && type != MF_MSG_PFN_MAP)` S521:1286-1289; `update_per_node_mf_stats` bumps the outcome counter and `++mf_stats->total` S521:1235-1264; the two page-type strings are exactly "already poisoned page" / "non struct page pfn" S521:897-898 | holds |
| row 3 "only Recovered and Delayed are success" (SKILL row 6) | `return (result == MF_RECOVERED || result == MF_DELAYED) ? 0 : -EBUSY;` S521:1299 | holds |
| row 4 counter names `…/memory_failure/{total,ignored,failed,delayed,recovered}` | `MF_ATTR_RO(total); MF_ATTR_RO(ignored); MF_ATTR_RO(failed); MF_ATTR_RO(delayed); MF_ATTR_RO(recovered);` under attribute group `.name = "memory_failure"` S521:126-160; the same five `What:` entries S523:192-230 | holds |
| row 4 does-not-mean "a kill: a free or clean page can be recovered with no process signalled" | free-buddy recovery path S521:2464-2476; kill list freed without signalling when no force-kill S521:462-468 | holds |
| row 5 `HardwareCorrupted:` above `0 kB` | proc.rst:1269-1271 "The amount of RAM/memory in KB, the kernel identifies as corrupted."; meminfo sample `HardwareCorrupted:     0 kB` proc.rst:1100 | holds |
| row 6 means condition: sysctl 1 + kernel page + Ignored | `if (!sysctl_panic_on_unrecoverable_mf) return false; return type == MF_MSG_KERNEL && result == MF_IGNORED;` S521:1268-1275; `MF_MSG_KERNEL` string "reserved kernel page" S521:879 | holds (scope nuance → F4) |
| sysctl defaults | `sysctl_memory_failure_recovery __read_mostly = 1` S521:74; `sysctl_memory_failure_early_kill __read_mostly` (0) S521:72; `sysctl_panic_on_unrecoverable_mf __read_mostly` (0) S521:78; vm.rst:995 "0 Try to continue operation (default)." | all three defaults correct |
| sysctl names under `vm.` | `register_sysctl_init("vm", memory_failure_table)` S521:2710 with procnames `memory_failure_early_kill` / `memory_failure_recovery` / `enable_soft_offline` / `panic_on_unrecoverable_memory_failure` S521:135-172 | holds |
| recovery=0 behaviour "every memory failure panics" | `if (!sysctl_memory_failure_recovery) panic("Memory failure on page %lx", pfn);` S521:2395-2396; hwpoison.rst:59-60 "All memory failures cause a panic. Do not attempt recovery." | holds (printed form missing → F2) |
| early_kill=0 behaviour "unmap everywhere, signal only a process that later touches the page" | vm.rst:507-508 "Only unmap the corrupted page from all processes and only kill a process who tries to access it." | holds |
| SKILL rows 1-3, 5-6 and the error patterns | mirror the entry table plus a "next read" column; attributions `kill_proc`/`kill_procs`/`action_result` correct | hold |

## Findings and fenced corrections

### F1 (MED) — the panic row's line text is not a `Memory failure:`-prefixed log line

Entry row 6 and SKILL row 7 show the evidence as `Memory failure: 0x…: unrecoverable page`. The call is
`panic("Memory failure: %#lx: unrecoverable page", pfn)` (S521:1294-1295) — `panic()` is not a `pr_*` macro, so
`pr_fmt` does not apply; the console line is the panic banner `Kernel panic - not syncing: %s`
(`kernel/panic.c:640`, fetched copy sha256 `7c00ccaf178a60ec6449365e7b240602d0f7d9ac92fba8b80f84acbee81d2344`):
the message never appears as a line starting with the class prefix, so an operator scanning the kernel log for
`Memory failure:`-prefixed lines misses the one event that took the host down. The recovery-action line
`…: recovery action for reserved kernel page: Ignored` always precedes the panic (same `action_result` body,
S521:1291-1295), which is the in-log companion to look for.

Correction for the entry's row 6:

```
| a panic whose banner reads `Kernel panic - not syncing: Memory failure: 0x…: unrecoverable page` (S521 `action_result` panics after printing the recovery-action line; the banner prefix is `kernel/panic.c`'s, so the message is not a `Memory failure:`-prefixed log line) | v7.3 `panic_on_unrecoverable_memory_failure` was 1 and a kernel-owned page the handler cannot recover came back Ignored — printed page type `reserved kernel page` (S521, S507) | a process kill — the host went down |
```

Correction for SKILL row 7:

```
| a panic with banner `Kernel panic - not syncing: Memory failure: 0x…: unrecoverable page` | v7.3 `panic_on_unrecoverable_memory_failure` was 1 and a kernel-owned page the handler cannot recover came back Ignored — printed page type `reserved kernel page`; the recovery-action line for the same pfn precedes it (S521, S507) | — the host went down | a process kill |
```

### F2 (MED) — the `vm.memory_failure_recovery=0` panic prints a different form, absent from both tables

The sysctl row says "0: every memory failure panics" but no evidence row shows what that panic looks like. The
call is `panic("Memory failure on page %lx", pfn)` (S521:2395-2396): `%lx` has no `#`, so the banner reads
`Kernel panic - not syncing: Memory failure on page <hex>` — no `0x`, no colon, no "unrecoverable" wording. It
matches none of the table's evidence patterns; an operator on a recovery=0 host (non-default) would find no row
for the one line they see. Correction for the entry's sysctl row 1:

```
| `vm.memory_failure_recovery` | 1 (default): attempt recovery and kill per mode; 0: every memory failure panics — banner `Kernel panic - not syncing: Memory failure on page <hex>` (S521 `memory_failure`: `panic("Memory failure on page %lx", pfn)`, `%lx` without `#`, so no `0x` and no colon) |
```

and the same clause appended to the SKILL sysctl paragraph (F5's block below carries it).

### F3 (MED) — the delivery-failure marker named in row 1 is the conditional one; the always-on one is missing

Entry row 1's does-not-mean cell and SKILL row 4's next-read cell say a `Cannot send advisory machine check
signal` line means the signal was not delivered. That line (S521:483-484) fires only inside `kill_procs`'
force-kill branch, after `kill_proc` already returned < 0 — and `kill_proc` itself then always prints the general
marker `pr_info("Error sending signal to %s:%d: %d\n", …)` (S521:307-309), printed as
`Memory failure: Error sending signal to <comm>:<pid>: <errno>`, on every failed send whatever the path. The
tables name the subset marker and omit the general one. Correction for the entry's row 1 does-not-mean cell:

```
| that the process died: the AO signal is catchable, and a failed send prints `Memory failure: Error sending signal to <comm>:<pid>: <errno>` (S521 `kill_proc`); under the force-kill path the same failure also prints `Memory failure: 0x…: Cannot send advisory machine check signal to <comm>:<pid>` (S521 `kill_procs`) |
```

Correction for SKILL row 4:

```
| kernel line `Memory failure: 0x…: Sending SIGBUS to <comm>:<pid> due to hardware memory corruption` | SIGBUS to that process: forced `BUS_MCEERR_AR` if it touched the page, ordinary `BUS_MCEERR_AO` otherwise (S521 `kill_proc`) | whether the process exited (the AO signal is catchable; a failed send prints `Memory failure: Error sending signal to <comm>:<pid>: <errno>`, and under the force-kill path also `Memory failure: 0x…: Cannot send advisory machine check signal to <comm>:<pid>`) | a death, or a count — kernel text is attribution, never a tally (QUALITY 15) |
```

### F4 (LOW) — `reserved kernel page` is the printed string for four kernel-owned populations

The panic fires on `type == MF_MSG_KERNEL && result == MF_IGNORED` (S521:1274), and the v7.3 `MF_MSG_KERNEL`
call site is the `-ENOTRECOVERABLE` case commented "Stable unhandlable kernel-owned page (PG_reserved, slab,
page tables, large-kmalloc). No recovery possible." (S521:2486-2490); vm.rst:935-941 lists the same set
(`PageReserved`, `PageSlab`, `PageTable`, `PageLargeKmalloc`). So the printed page type `reserved kernel page`
covers all four populations — the means cell should not be read as PG_reserved-only. Note also that
`high-order kernel page` (`MF_MSG_KERNEL_HIGH_ORDER`, S521:2478) and `get hwpoison page`
(`MF_MSG_GET_HWPOISON`, S521:2494) Ignored lines do not panic. The F1 correction block already carries the
"kernel-owned page the handler cannot recover" wording; optionally extend its does-not-mean cell with:
"not fired by `high-order kernel page` or `get hwpoison page` Ignored lines (S521 `panic_on_unrecoverable_mf`
checks `MF_MSG_KERNEL` only)".

### F5 (LOW) — early_kill=1 compressed: "signal every process mapping it" drops "not reloadable"

vm.rst:503-506: "1: Kill all processes that have the corrupted and not reloadable page mapped as soon as the
corruption is detected. Note this is not supported for a few types of pages, like kernel internally allocated
data or the swap cache…", and vm.rst:499-501: pages with a valid copy on disk are handled transparently. The
entry's "signal every process mapping it as soon as the error is found" and SKILL's "1 = signal every mapper at
detection" drop that qualifier; row 4's does-not-mean cell ("a free or clean page can be recovered with no
process signalled") already mitigates. Correction for the entry's sysctl row 2:

```
| `vm.memory_failure_early_kill` | 0 (default, this host): unmap everywhere, signal only a process that later touches the page; 1: signal the processes that have the corrupted and not reloadable page mapped as soon as the error is found (S507: a page with a valid copy on disk is handled transparently; not supported for kernel-internal data or the swap cache) |
```

Correction for the SKILL sysctl paragraph:

```
Sysctls (read, never write): `vm.memory_failure_recovery` 1 = recover and kill per mode, 0 = every memory failure
panics (banner `Kernel panic - not syncing: Memory failure on page <hex>`, no `0x`, no colon — S521
`memory_failure`); `vm.memory_failure_early_kill` 0 (default; this host) = signal only a process that later
touches the page, 1 = signal the processes holding the corrupted and not reloadable page at detection (a page
with a valid copy on disk is handled transparently; not supported for kernel-internal data or the swap cache —
S507); `vm.panic_on_unrecoverable_memory_failure` is new in v7.3 and absent on this host's 7.2.11 (entry sysctl
table). The event-time hook is `ras:memory_failure_event` — under `ras`, not `oom` (S524); its traced text
starts `pfn 0x…`, without the `Memory failure: ` prefix (S524 `TP_printk`).
```

### F6 (LOW) — the SIGBUS/SIGKILL lines print only when the handler decides a kill is required, and the `forcibly killing` text can name unmap failure when the trigger was not

`kill_procs` signals only under `forcekill` ("Only do anything when FORCEKILL is set, otherwise just free the
list", S521:462-468), and in `hwpoison_user_mappings` `forcekill = folio_test_dirty(folio) || (flags &
MF_MUST_KILL) || !unmap_success` (S521:1678-1680). So a clean reloadable page produces only the recovery-action
line, and the `forcibly killing … because of failure to unmap corrupted page` text (S521:470-471) prints
whenever the force-kill branch runs with an unresolvable address — including when the trigger was a dirty page
or `MF_MUST_KILL` with the unmap successful. The line's SIGKILL attribution (row 2's means cell) is unaffected;
the "because of failure to unmap" clause is the kernel's fixed text, not a reliable trigger report. The entry's
claims-table row 5 ("When unmapping the corrupted page failed, the process receives SIGKILL instead of SIGBUS")
reads the same way: under a failed unmap, tasks with a resolvable address still get the advisory SIGBUS
(S521:481-482) and only the `-EFAULT`-address subset gets SIGKILL (S521:469-474) — an entailment-seat matter I
flag as context, since it shapes how rows 1 and 2 combine for one page.

### F7 (LOW) — same-file lines under other prefixes

`memory-failure.c` redefines `pr_fmt` to `"Unpoison: "` at S521:2716-2717, so the unpoison path (software-injected
pages only; hwpoison.rst:78-79: "Once any hardware memory failure happens, this feature is disabled") prints
under `Unpoison: `, not the class prefix. The trace event's text is `pfn %#lx: recovery action for %s: %s`
(S524:93) — also without the `Memory failure: ` prefix. Neither is kill evidence; noted so a prefix-scoped grep
is not read as exhaustive over the file's output. The entry's Claim paragraph ("lines under the prefix
`Memory failure:`") is accurate for the kill/recovery path this entry covers.

### F8 (LOW) — `vm.enable_soft_offline` is a fourth memory-failure sysctl under `vm`, absent from the sysctl table

Registered in the same table (S521:155-162, default 1 at S521:76), read as 1 on this host and named in the
entry's "On this host" section and Boundaries (soft offline out of scope). Omission is consistent with the
boundary; recorded so the sysctl table is not read as the complete `vm` memory-failure set.

## SKILL.md actionability (could a mori operator act with these rows alone?)

Yes, with the F1-F3 gaps fixed. The draft's four-column table (evidence → read as → next read → never read as)
gives the operator the two structured surfaces to count (`/sys/devices/system/node/node*/memory_failure/total`,
`HardwareCorrupted` in `/proc/meminfo`), the kernel line forms for attribution, the read-only sysctls, the
`ras:` (not `oom`) tracepoint, and error patterns that already forbid counting kernel text (QUALITY 15) and
reading a `Sending SIGBUS` line as a death. What would block action today: the panic row's evidence text is not
a greppable line start (F1), the recovery=0 panic has no row at all (F2), and the delivery-failure line an
operator would actually see on the ordinary path is absent (F3). One process note: these rows are an
uncommitted working-tree draft — the data commit `78295c76` contains no memory-failure text in SKILL.md — so
the L1 integrates them together with the fenced corrections above.

## Findings

- MED F1 — entry decision-table row 6 and SKILL row 7: panic evidence text `Memory failure: 0x…: unrecoverable
  page` is the panic message body, printed only inside the banner `Kernel panic - not syncing: …`
  (`memory-failure.c.v7.3:1294-1295`, `kernel/panic.c:640`); not a `Memory failure:`-prefixed log line. Fenced
  correction above.
- MED F2 — entry sysctl row `vm.memory_failure_recovery` (and SKILL sysctl paragraph): the recovery=0 panic
  prints `Kernel panic - not syncing: Memory failure on page <hex>` (`memory-failure.c.v7.3:2395-2396`, `%lx`
  without `#` — no `0x`, no colon) and has no evidence row in either table. Fenced correction above.
- MED F3 — entry row 1 does-not-mean cell and SKILL row 4 next-read cell: the named non-delivery marker
  `Cannot send advisory machine check signal` fires only under the force-kill path (`memory-failure.c.v7.3:481-484`);
  the always-on marker `Memory failure: Error sending signal to <comm>:<pid>: <errno>` (`:307-309`) is missing
  from both tables. Fenced correction above.
- LOW F4 — `reserved kernel page` (the panic condition's page type, `memory-failure.c.v7.3:879,1274,2486-2490`;
  `vm.rst.v7.3:935-941`) covers PG_reserved, slab, page tables and large-kmalloc; `high-order kernel page` and
  `get hwpoison page` Ignored lines do not panic.
- LOW F5 — early_kill=1 cell drops the doc's "not reloadable" qualifier and the unsupported-page-types note
  (`vm.rst.v7.3:499-506`); mitigated by row 4's does-not-mean cell. Fenced correction above.
- LOW F6 — SIGBUS/SIGKILL lines print only under a force-kill decision (`memory-failure.c.v7.3:462-468,1678-1680`);
  the `forcibly killing … because of failure to unmap corrupted page` text can print when the trigger was a
  dirty page or `MF_MUST_KILL` with the unmap successful; under a failed unmap, tasks with resolvable addresses
  still get the advisory SIGBUS (`:481-482`) — context for the claims-table row 5 wording.
- LOW F7 — same file prints `Unpoison: `-prefixed lines (`:2716-2717`, software-injected pages only) and the
  trace text starts `pfn 0x…` without the class prefix (`memory-failure-trace.h.v7.3:93`).
- LOW F8 — `vm.enable_soft_offline` (`memory-failure.c.v7.3:155-162,76`) is absent from the sysctl table;
  consistent with the entry's soft-offline boundary, noted for completeness.

No HIGH finding: every line text that the tables present as a `Memory failure:`-prefixed log line matches the
kernel's printed form exactly, every means cell I could falsify held, and all three sysctl defaults are correct
against code, doc and the host read.

Report: .ufo/waves/round-54/w1/Mo54RevDecisionTable.md
