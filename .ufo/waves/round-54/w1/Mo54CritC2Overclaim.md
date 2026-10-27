# Mo54CritC2Overclaim — prose attack on C2 entry

Seat: `Mo54CritC2Overclaim`; scope: `corpus/knowledge/memory-failure-kills-r54.md` outside claim table, measured at `78295c764093ff1f6cee08d7246679900bde7265`. Read-only. No vote lines. Scratch created at `/fast/scratch/hyaku/mori-r54/Mo54CritC2Overclaim/`; no fixture or clone used. Removed before completion.

## Axes

- **Calibration**: precise scope of negative assertions and causal descriptions.
- **Depth**: decision table distinguishes handler signals, outcomes, counters, and process death.
- **Operability**: host observation is tied to a reproducible observation boundary.

## Findings

### MED — `## Claim`, lines 13–17: signal scope and the literal “Out of memory” negative are overbroad

The source copy `corpus/evidence/sources-r54/memory-failure.c.v7.3` contradicts two generalizations. At lines 282–305, `kill_proc` describes signaling all collected processes, but collection at lines 500–539 only selects a process for optional-action handling when early-kill is configured (globally or per-process); in action-required handling, the current process is selected, with opted-in peers also possible. The v7.3 documentation at `sources-r53/vm.rst.v7.3:495-517` says default late mode unmaps the page and kills a process that tries to access it. Thus “signals the processes that map it” without qualification falsely suggests all mappers are signalled in the default mode.

The negative “prints no `Out of memory` … line” is literally false: `memory-failure.c.v7.3:390-393` prints `pr_err("Out of memory while machine check handling\n")` when a GFP_ATOMIC allocation fails in `__add_to_kill`. This is a handler-allocation diagnostic, not an OOM-killer victim event. In contrast, the OOM evidence assertion is supported: `memory-failure.c.v7.3` has no `oom_kill`, `mark_victim`, or `out_of_memory` references; its only OOM-adjacent text is the allocation diagnostic. The v7.3 OOM path is in `sources-r54/oom_kill.c.v7.3`: `trace_mark_victim` at line 774, `MEMCG_OOM_KILL` at 936, and OOM-kill invocations at 1151/1169. The r47 trace header identifies `TRACE_SYSTEM oom` and `TRACE_EVENT(mark_victim)` (`sources-r47/include_trace_events_oom.h:2,76`). Do not make the narrow true statement about OOM accounting appear to prove the broader string absence.

Smallest safe replacement for lines 13–19:

```text
Hardware memory errors can lead to process signals outside the OOM-killer path. When a poisoned page is handled, the memory-failure path may send SIGBUS to the task accessing it (action-required) and may send catchable advisory SIGBUS to other mapped processes selected for early kill; if recovery cannot unmap a mapping, some collected tasks can instead receive SIGKILL. This is not an OOM-killer victim path: it does not increment the memcg `oom_kill` event or emit `oom:mark_victim`. The handler can nevertheless print `Out of memory while machine check handling` if its GFP_ATOMIC allocation for tracking a task fails; that is an allocation diagnostic, not an OOM-kill record. Other evidence includes `Memory failure:` handler lines, per-node counters, `HardwareCorrupted`, and `ras:memory_failure_event`.
```

This drops the unsupported implication that every such event kills a process or signals every mapper, while preserving the OOM distinction. Note also that source `memory-failure.c.v7.3:295-306` conditions forced `BUS_MCEERR_AR` on `MF_ACTION_REQUIRED && t == current`; otherwise it uses `BUS_MCEERR_AO`, so wording should avoid implying every mapping receives either signal.

### MED — decision table line 56: SIGKILL explanation overstates condition

The table says the “forcibly killing” line means SIGKILL “from the memory-failure handler” and says memcg `oom_kill` does not move; the latter is sound. But its “what it does not mean” is fine, while the `## Claim` that frames SIGKILL as the generic consequence of unmapping failure needs precision. `memory-failure.c.v7.3:462-484` sends SIGKILL only when a collected task has `tk->addr == -EFAULT`; the general `!unmap_success` path at `:1656-1680` enables force-kill handling but otherwise calls `kill_proc`, which sends SIGBUS. At `:403-416`, comments explain the `-EFAULT` / no-device-mapping condition. The log text itself says failure to unmap, but the code’s actual SIGKILL discriminator is missing address, not every failed unmap.

Replacement for decision table line 56 (and align claim lines 14–15):

```text
| `Memory failure: 0x…: forcibly killing <comm>:<pid> because of failure to unmap corrupted page` | SIGKILL was sent by the handler for a collected task whose user address could not be resolved (`-EFAULT`) | an OOM kill; `memory.events oom_kill` does not move |
```

The quoted log wording is real; avoid paraphrasing it as though every unmap failure yields SIGKILL.

### LOW — decision table line 60: “host went down” is not warranted by the panic line alone

At `memory-failure.c.v7.3:1268-1297`, the configured panic condition is exactly `type == MF_MSG_KERNEL && result == MF_IGNORED` with sysctl enabled, and the literal panic is `Memory failure: %#lx: unrecoverable page`. A panic does not itself establish that the host went down (for example, panic configuration can reboot); the sysctl documentation `sources-r53/vm.rst.v7.3:926-1003` explicitly says `panic` may reboot. The entry’s cell says “the host went down,” which overclaims the consequence of a panic line. The panic text also lacks the sysctl name, so that configuration cannot be inferred from the log alone.

Replacement for line 60:

```text
| a panic `Memory failure: 0x…: unrecoverable page` | consistent with `panic_on_unrecoverable_memory_failure=1` and an ignored reserved-kernel-page failure | a process kill; the line alone does not prove which panic setting caused it or whether the machine rebooted |
```

The sysctl table’s defaults at lines 65–67 are supported: `memory-failure.c.v7.3:72-78` initializes recovery and soft-offline to 1 and early-kill/panic to 0; `sources-r53/vm.rst.v7.3:495-539, 926-1003` agrees. The panic condition is narrower than the loose phrase “a kernel-owned page cannot be recovered”: source `:1271-1275` checks only `MF_MSG_KERNEL` plus `MF_IGNORED`; high-order kernel pages use a separate type (`:878-880, 2478`) and do not satisfy it. The entry’s current prose “reserved kernel page” is precise; retain that specificity.

### LOW — decision table line 61 and `## On this host`, lines 69–74: evidence boundary

Read-only host surfaces were observed as stated: kernel `7.2.11-arch1-1`; node0 five counters all `0`; `HardwareCorrupted: 0 kB`; `memory_failure_recovery=1`, `memory_failure_early_kill=0`, `enable_soft_offline=1`; panic sysctl absent. The frozen sweeps receipt (`.ufo/waves/round-54/evidence/sweeps.txt:19-30`) records these values, but does not record a kernel-log inspection. A current-boot boolean presence query did find neither `Memory failure` nor `Out of memory` in `journalctl -k -b` (both `grep -qm1` exit 1). Thus the observed “no line” is true for that query/current boot, but the committed evidence does not establish absence over the entire uptime or after journal/log rotation. Keep the claim scoped to observed journal/current-boot evidence rather than treating zero counters as proof no message was emitted.

Safer line 74:

```text
The read-only current-boot journal presence check found no `Memory failure` line; the frozen host receipt records zero counters, not a kernel-log search. No live event was observed in these checks, and every decision-table row is otherwise interpreted from source.
```

### LOW — Boundaries lines 81–82

The boundary is sound: this entry covers handling after a page is declared poisoned, not corrected-error detection/accounting. `soft_offline_in_use_page` at `memory-failure.c.v7.3:2844-2965` migrates or invalidates and its kernel comment explicitly says “without killing anything”; no counterexample to the soft-offline boundary found. The accounting wording “Corrected-error accounting (EDAC, `rasdaemon`, MCE decoding)” lumps distinct functions together without specifying whether those sources count, report, or decode; this does not undermine the scope boundary, but may mislead. Narrow replacement:

```text
Corrected-error detection and reporting (including EDAC/rasdaemon and MCE decoding) are hardware-health ground this entry does not hold; it covers what the kernel does once a page is declared poisoned, not how the error was detected.
```

## Commands and observed outputs

- `grep -n 'Out of memory\|oom_kill\|mark_victim\|out_of_memory' corpus/evidence/sources-r54/memory-failure.c.v7.3` → `392: pr_err("Out of memory while machine check handling\n");`.
- `grep -n 'mark_victim\|oom_kill\|MEMCG_OOM\|oom_kill:' corpus/evidence/sources-r54/oom_kill.c.v7.3` → `trace_mark_victim` line 774, `MEMCG_OOM_KILL` line 936, OOM-kill calls lines 1151/1169.
- `grep -n 'TRACE_EVENT\|TRACE_SYSTEM\|mark_victim' corpus/evidence/sources-r47/include_trace_events_oom.h` → `TRACE_SYSTEM oom` line 3, `TRACE_EVENT(mark_victim` line 76.
- `journalctl -k -b --no-pager | grep -qm1 -F 'Memory failure'; echo "... exit=$?"` → exit 1; same query for `Out of memory` → exit 1. Presence check only, not a count.
- Host read-only command over `/sys/devices/system/node/node0/memory_failure/*`, `/proc/meminfo`, `/proc/sys/vm/*`, `uname -r` → five zeroes, `HardwareCorrupted: 0 kB`, values above, kernel `7.2.11-arch1-1`, absent panic sysctl.

No tools installed or updated.

## Findings

- **MED — `corpus/knowledge/memory-failure-kills-r54.md:13-17`**: all-mappers signal scope is too broad for default late-kill; and “prints no `Out of memory`” is false due to the handler's allocation-failure diagnostic at source line 392. Replace with an explicit distinction between OOM-killer evidence and this unrelated diagnostic.
- **MED — `corpus/knowledge/memory-failure-kills-r54.md:14-15,56`**: SIGKILL is not the generic outcome of failed unmapping; the code’s discriminator is an unresolved user address (`-EFAULT`), while other collected tasks can receive SIGBUS.
- **LOW — `corpus/knowledge/memory-failure-kills-r54.md:60`**: a panic line does not alone prove the specific sysctl caused it or that the host went down/rebooted.
- **LOW — `corpus/knowledge/memory-failure-kills-r54.md:74`**: zero counters and frozen sweeps receipt do not substantiate no kernel message over the entire boot; record the actual journal-search scope.
- **LOW — `corpus/knowledge/memory-failure-kills-r54.md:81-82`**: corrected-error accounting wording conflates detection/reporting; tighten terms. Soft-offline “kills nothing” boundary is supported by v7.3 code and comment.
