# Mo54ScribeSkill — draft `## Round54` section for SKILL.md

Seat: scribe (SKILL.md prose), round 54 wave w1, lane mori-shokunin.
Scope: one fenced draft, house shape of `## Round53` (SKILL.md:1178-1207); every row cites
`corpus/knowledge/memory-failure-kills-r54.md` or `corpus/knowledge/kernel-v7.3-recheck-r54.md` with a line.
SKILL.md was **not** edited (its working-tree modification predates this seat: the L1's own uncommitted
`## Round54` at SKILL.md:1211-1247 — see Findings 1 and 2).
All commands below ran read-only from `/home/vgpnk/Projects/shokunin/mori-shokunin` or from the scratch dir; nothing
was written outside this report. Scratch `/fast/scratch/hyaku/mori-r54/Mo54ScribeSkill/` was created, never used for
a clone (no clone was needed: every cited byte is already committed in the lane), and removed at exit.

## What I ran

| # | command | observed |
|---|---|---|
| 1 | `wc -l SKILL.md corpus/knowledge/memory-failure-kills-r54.md corpus/knowledge/kernel-v7.3-recheck-r54.md` | `1247`, `86`, `109` — line references below are to these lengths |
| 2 | `git log --oneline -6 -- SKILL.md`; `git status --porcelain SKILL.md` | last commit `7b90a3c6` (round-53); ` M SKILL.md` — the Round54 section at 1211-1247 is uncommitted working-tree text, not this seat's |
| 3 | `grep -n '' corpus/knowledge/memory-failure-kills-r54.md` | line map: `:11` `## Claim`, `:13-19` claim, `:25-45` claim rows, `:47-51` decision intro, `:53-61` decision rows, `:63-67` sysctls, `:69-74` host, `:76-86` boundaries |
| 4 | `grep -n 'Sending SIGBUS to\|forcibly killing\|recovery action for %s\|Cannot send advisory\|pr_fmt(fmt)\|panic_on_unrecoverable_mf\|MF_IGNORED\] =' corpus/evidence/sources-r54/memory-failure.c.v7.3` | `37` pr_fmt `"Memory failure: "`; `292` Sending SIGBUS; `470` forcibly killing; `483` Cannot send advisory; `872` `[MF_IGNORED] = "Ignored"`; `1268`,`1271` `panic_on_unrecoverable_mf()`; `1291` `pr_err("%#lx: recovery action for %s: %s\n"…` |
| 5 | `grep -n 'num_poisoned_pages_inc\|update_per_node_mf_stats\|result == MF_RECOVERED\|kill_procs(' …/memory-failure.c.v7.3` | `86`, `1287-1288` (counter advance), `1297` `return (result == MF_RECOVERED \|\| result == MF_DELAYED) ? 0 : -EBUSY;`, `462` `kill_procs(` |
| 6 | `grep -n 'as soon as the error is detected\|runs into the corrupted page\|All memory failures cause a panic' corpus/evidence/sources-r54/hwpoison.rst.v7.3` | `60` panic-on-zero-recovery; `64` early-kill wording; `70` late-kill default |
| 7 | `grep -n 'total number of raw poisoned pages\|how many pages are ignored\|memory_failure/' corpus/evidence/sources-r54/sysfs-devices-node.v7.3` | `192`, `196` `total`; `199` `ignored`; `208`,`216`,`224` `failed`/`delayed`/`recovered` |
| 8 | `grep -n 'TRACE_SYSTEM ras\|TP_printk\|historical' corpus/evidence/sources-r54/memory-failure-trace.h.v7.3` | `4` historical note; `7` `#define TRACE_SYSTEM ras`; `93` `TP_printk("pfn %#lx: recovery action for %s: %s",` |
| 9 | `grep -n 'memory_failure_recovery\|memory_failure_early_kill\|panic_on_unrecoverable_memory_failure\|BUS_MCEERR_AO' corpus/evidence/sources-r53/vm.rst.v7.3` | `495` early_kill; `514` catchable `BUS_MCEERR_AO`; `523` recovery; `926` `panic_on_unrecoverable_memory_failure`; `1002` example write |
| 10 | `grep -n 'HardwareCorrupted' corpus/evidence/sources-r53/proc.rst.v7.3` | `1100` sample meminfo line; `1269` field definition |
| 11 | `uname -r` | `7.2.11-arch1-1` |
| 12 | host read (read-only, 2026-10-27): `grep HardwareCorrupted /proc/meminfo`; `cat /sys/devices/system/node/node*/memory_failure/*`; `cat /proc/sys/vm/memory_failure_{recovery,early_kill}`; `cat /proc/sys/vm/enable_soft_offline`; test `-e /proc/sys/vm/panic_on_unrecoverable_memory_failure` | `HardwareCorrupted:     0 kB`; `node0/{delayed,failed,ignored,recovered,total}=0`; `memory_failure_recovery=1`; `memory_failure_early_kill=0`; `enable_soft_offline=1`; panic switch `ABSENT`. One node dir: `node0` only. Agrees field for field with the L1 sweep at `.ufo/waves/round-54/evidence/sweeps.txt:20-31` |
| 13 | `ls -ld /sys/kernel/tracing`; `ls /sys/kernel/tracing/events/ras/`; `id -u`; `cat /proc/sys/kernel/perf_event_paranoid` | tracefs `drwx------ root root`; `Permission denied`; uid `1000`; `perf_event_paranoid=2` — the tracefs event format is **unavailable** unprivileged, not absent |
| 14 | `grep 'memory_failure_event' /proc/kallsyms \| awk '{print $2, $3}'` | 22 symbols on 7.2.11 incl. `__tracepoint_memory_failure_event`, `__traceiter_memory_failure_event`, `event_memory_failure_event` — the tracepoint exists on this kernel even though tracefs is root-only |
| 15 | `cat .ufo/waves/round-54/evidence/c1-at-data.txt`, `c2-at-data.txt` | `C1=unmet scope=31 rows=31 matched=31 status_ok=31 line_ok=31 quote_ok=31 source_rows=ok pins=ok provenance=ok held=31 absent=0 holds=31 changed=0 voted=0 dissent=0 … failed=votes` exit=1; `C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 … failed=entailment` exit=1 |
| 16 | vote snapshot at drafting time (mid-wave, **not** a tally): `grep -hE '^RECHECK [0-9a-f]{12} holds' .ufo/waves/round-54/w1/Mo54Rc*.md \| sort -u \| wc -l`; `grep -hE '^RECHECK [0-9a-f]{12} changed' …`; `grep -hnE '^ENTAIL [0-9a-f]{12} overclaim' .ufo/waves/round-54/w1/Mo54En*.md` | 24 distinct hashes carry a `holds` line; 0 carry `changed`; four hashes carry an `overclaim` line: `c98ac2ffa163`, `734269273c22`, `8248e6d24be8`, `257f4acfda4e` |
| 17 | `ls corpus/evidence/sources-r54/`; `find .ufo/waves/round-54 -name '*memory-failure*'` | v7.3 copies only (`memory-failure.c.v7.3`, `hwpoison.rst.v7.3`, `sysfs-devices-node.v7.3`, `memory-failure-trace.h.v7.3`); **no v7.2 `memory-failure.c` copy anywhere in the lane's round-54 evidence** |

Exit codes: every read returned 0 except command 13's `ls` (permission denied, expected) — noted as a limit, not a
failure.

## Draft (fenced; drop-in replacement for the section at SKILL.md:1211-1247)

```markdown
## Round54 — hardware memory-failure kills, and the v7.3 recheck of the remaining v7.2 rows

The kernel kills processes for a reason that is not memory exhaustion. `mm/memory-failure.c` unmaps a page the
hardware reported corrupted and signals its mappers — SIGBUS with a machine-check code, or SIGKILL when the unmap
failed — and none of it passes through the OOM killer, so `memory.events oom_kill` does not move, no
`oom-kill:`/`Out of memory` line is printed and no `oom:mark_victim` event is emitted
(`corpus/knowledge/memory-failure-kills-r54.md:13-19`). Every line the handler prints carries the one prefix
`Memory failure: ` (`memory-failure-kills-r54.md:25`; `corpus/evidence/sources-r54/memory-failure.c.v7.3:37`).
Citations name a line of `corpus/knowledge/memory-failure-kills-r54.md` or of
`corpus/knowledge/kernel-v7.3-recheck-r54.md` (written `<basename>:<line>`); the source bytes are v7.3 and this host
runs 7.2.11.

### Kernel line → class → next read (decision table)

| `Memory failure: 0x…` line | class | next read | never read it as | source |
|---|---|---|---|---|
| `Sending SIGBUS to <comm>:<pid> due to hardware memory corruption` | a machine-check SIGBUS to the task mapping the page: forced `BUS_MCEERR_AR` for the task that touched it, ordinary `BUS_MCEERR_AO` for the other mappers | the recovery-action line for the same pfn, then whether that task exited | a death: the AO signal is catchable and may be blocked | `memory-failure-kills-r54.md:26-28,39,55` |
| `forcibly killing <comm>:<pid> because of failure to unmap corrupted page` | SIGKILL issued by the memory-failure handler | the recovery-action line for that pfn; `memory.events oom_kill`, which will not have moved | an OOM kill | `memory-failure-kills-r54.md:29,56` |
| `Cannot send advisory machine check signal to <comm>:<pid>` | the signal for that task was not delivered | that task's own exit status | delivery — a sending line alone does not prove the process received anything | `memory-failure-kills-r54.md:30` |
| `recovery action for <page type>: Ignored\|Failed\|Delayed\|Recovered` | one handled page and its outcome; only `Recovered` and `Delayed` are the success pair | the per-node counter of that outcome, and the SIGBUS/SIGKILL lines for the process side | proof that any process was signalled | `memory-failure-kills-r54.md:31-33,57` |
| a panic on `unrecoverable page` | the handler panicked on a kernel-owned page that came back `Ignored` | the boot that follows — the previous boot ended there | a process kill; nothing survived to be read | `memory-failure-kills-r54.md:35,60` |

### Counters and meminfo (structured surfaces: count here, attribute from the lines)

| surface | counts | never | source |
|---|---|---|---|
| `/sys/devices/system/node/node<N>/memory_failure/total` | raw poisoned pages on node N, since boot | a kill | `memory-failure-kills-r54.md:41,58` |
| `…/memory_failure/{ignored,failed,delayed,recovered}` | that node's poisoned pages by recovery outcome | a process, or (added across nodes) a host figure this entry does not hold | `memory-failure-kills-r54.md:42,57` |
| `HardwareCorrupted:` in `/proc/meminfo`, in kB | memory the kernel identifies as corrupted, host-wide | a per-node or per-process figure | `memory-failure-kills-r54.md:45,59` |
| no line and every counter 0 (this host, 2026-10-27) | no memory failure handled since boot | hardware health: corrected errors are counted by EDAC/rasdaemon, not here | `memory-failure-kills-r54.md:61,81-82` |

### Sysctls (read, never write — `memory-failure-kills-r54.md:78-79`)

| sysctl | value → behaviour | this host | source |
|---|---|---|---|
| `vm.memory_failure_recovery` | 1: attempt recovery and kill per mode; 0: every memory failure panics | 1 | `memory-failure-kills-r54.md:38,65,72` |
| `vm.memory_failure_early_kill` | 0 (default): unmap everywhere, signal only a process that later touches the page (late kill, the default); 1: signal every process mapping the page at detection | 0 | `memory-failure-kills-r54.md:36-37,66,72` |
| `vm.panic_on_unrecoverable_memory_failure` | 1: panic when a kernel-owned page cannot be recovered; 0 (default): ignore and continue; documented in the v7.3 `vm.rst` (`corpus/evidence/sources-r53/vm.rst.v7.3:926`) | file absent | `memory-failure-kills-r54.md:40,67,73` |

### v7.3 bytes vs this host's 7.2.11 (read 2026-10-27)

| surface | at v7.3 | on this host | source |
|---|---|---|---|
| kill / recovery lines | `mm/memory-failure.c` v7.3 (`memory-failure.c.v7.3:292,470,483,1291`) | no line of this class observed; the entry states what the kernel prints, not a past kill here | `memory-failure-kills-r54.md:25-31,73-74` |
| per-node counters | sysfs ABI v7.3 (`sysfs-devices-node.v7.3:192-224`) | one node, `node0`; `total`/`ignored`/`failed`/`delayed`/`recovered` all 0 | `memory-failure-kills-r54.md:41-42,71` |
| `HardwareCorrupted` | documented (`proc.rst.v7.3:1269`) | `0 kB` | `memory-failure-kills-r54.md:45,59,72` |
| `ras:memory_failure_event` | `TRACE_SYSTEM ras`, printk `pfn %#lx: recovery action for %s: %s` (`memory-failure-trace.h.v7.3:7,93`) | symbol `__tracepoint_memory_failure_event` present in `/proc/kallsyms`; the tracefs event dir is root-only `0700`, so its `format` is unavailable unprivileged | `memory-failure-kills-r54.md:43-44,73` |
| `panic_on_unrecoverable_memory_failure` | documented at v7.3 (`vm.rst.v7.3:926`) | `/proc/sys/vm/panic_on_unrecoverable_memory_failure` absent | `memory-failure-kills-r54.md:67,73` |

Soft offline (`enable_soft_offline`, migration of a page with corrected errors) kills nothing and stays out of this
table (`memory-failure-kills-r54.md:83-84`).

### Error patterns (memory-failure kills)

| observation | reading | source |
|---|---|---|
| a process died; `memory.events oom_kill`, the OOM catalog-ID notices and `oom:mark_victim` are all silent | a death with no OOM record is **not yet unexplained**: read `/sys/devices/system/node/node*/memory_failure/*` and `HardwareCorrupted` before calling it unexplained — a second kill source sits outside the OOM path | `memory-failure-kills-r54.md:15-19,49-51,56` |
| `Memory failure:` lines are tallied | kernel text carries no `MESSAGE_ID`: count with the per-node counters and read the lines for pfn/comm/pid attribution only | `memory-failure-kills-r54.md:49-51` |
| a `Sending SIGBUS` line is read as a death | the AO signal is catchable and a `Cannot send advisory machine check signal` line means it was never delivered | `memory-failure-kills-r54.md:30,39,55` |
| the event is sought among `oom` tracepoints | it is `ras:memory_failure_event`, under `ras` | `memory-failure-kills-r54.md:43` |
| the panic switch is expected on this host | the v7.3 documentation describes it; the file does not exist on 7.2.11 | `memory-failure-kills-r54.md:67,73` |

### Release recheck rule, round 54

The round-53 rule holds and gains a located line. Scope: every remaining claim row of the lane that pins Linux v7.2
— 31 rows at the entering tip (22 `oom-memcg-stat-r50.md`, 8 `commit-runway-read-r53.md`, 1
`quota-observability-r48.md`) (`kernel-v7.3-recheck-r54.md:11-14`). Per row the ledger holds the counter's `status` (`held` when the v7.2
quote still occurs, whitespace collapsed, in the v7.3 copy; `absent` otherwise), a v7.3 `source` row, the `line` on
which the quote begins at v7.3, and a `disposition` that is a reading of the new file, not of the quote
(`kernel-v7.3-recheck-r54.md:15-17,21`); the column reads `holds` provisionally until the round's RECHECK seats return (`kernel-v7.3-recheck-r54.md:7`).

A v7.2 prose anchor is not a v7.3 position. Shift it by the `moved` column of `## Where the quotes moved` before
quoting v7.3: `mm/memcontrol.c` +45 at the OOM report block and +84 at the `memory.stat` reader, `mm/mm_init.c` +4,
the rendered cgroup-v2 page +31, while `mm/oom_kill.c`, `lib/percpu_counter.c`,
`include/linux/percpu_counter.h` and `include/uapi/asm-generic/errno.h` did not move at all
(`kernel-v7.3-recheck-r54.md:57-65`, table `kernel-v7.3-recheck-r54.md:67-99`). A located quote is not entailment: whether the claim follows from its quote is
judged row by row, separately (`memory-failure-kills-r54.md:9`).

Release-drift leads on mori ground, recorded as leads and never as claims: `memory.pressure` and `io.pressure` are
documented read-write at 7.3 (7.2: read-only); the `io.stat` throttle field is `delay_nsec` in nanoseconds (7.2:
`delay`, microseconds), so an io observer keyed on the old name or unit reads wrong; and the `cpu.stat` CFS
bandwidth stats are documented non-hierarchical (`kernel-v7.3-recheck-r54.md:103-109`). They belong to the entries that own those surfaces.
```

## Grounding checks (each cited source line re-read, not inferred)

| cited | bytes observed | command |
|---|---|---|
| `memory-failure-kills-r54.md:26-28,39,55` | claim rows "Sending SIGBUS…", "forced SIGBUS … BUS_MCEERR_AR", "Don't use force here…", S507 "catchable SIGBUS with BUS_MCEERR_AO", decision row for the sending line | #3, #9 |
| `memory-failure-kills-r54.md:29,56` | "forcibly killing …" claim row and its decision row ("an OOM kill; `memory.events oom_kill` does not move") | #3 |
| `memory-failure-kills-r54.md:30` | "Cannot send advisory machine check signal" row | #3, #4 (`memory-failure.c.v7.3:483`) |
| `memory-failure-kills-r54.md:31-33,57` | recovery-action row, four outcome words, `return (result == MF_RECOVERED \|\| result == MF_DELAYED) ? 0 : -EBUSY;`, decision row | #3, #5 |
| `memory-failure-kills-r54.md:35,60` | `panic_on_unrecoverable_mf()` guard row; panic decision row | #3, #4 (`:1268-1271`) |
| `memory-failure-kills-r54.md:41-42,58` | node `total` row; `ignored` row; decision row "pages poisoned on that node since boot, by outcome" | #3, #7 |
| `memory-failure-kills-r54.md:45,59` | `HardwareCorrupted` claim row; decision row | #3, #10 |
| `memory-failure-kills-r54.md:61,81-82` | "no line and all counters 0" row; EDAC/rasdaemon boundary | #3 |
| `memory-failure-kills-r54.md:38,65,72` / `memory-failure-kills-r54.md:36-37,66,72` / `memory-failure-kills-r54.md:40,67,73` | the three sysctl rows, their host values at `:72`, the panic switch absence at `:73` | #3, #12 |
| `memory-failure-kills-r54.md:43-44` | tracepoint `ras` row and `TP_printk("pfn %#lx: recovery action for %s: %s"` row | #3, #8 |
| `memory-failure-kills-r54.md:78-79,83-84` | never-inject / never-write and soft-offline boundaries | #3 |
| `kernel-v7.3-recheck-r54.md:11-14,15-17,21,7` | scope sentence (31 rows, 22/8/1) and the status/line/disposition definition; provisional `holds` | `grep -n ''` on `kernel-v7.3-recheck-r54.md` (command 3's sibling; lines quoted in the draft) |
| `kernel-v7.3-recheck-r54.md:57-65,67-99` | "Where the quotes moved" prose (`:60-64`: memcontrol +45/+84, mm_init +4, cgroup-v2 page +31) and the 31-row table | same |
| `kernel-v7.3-recheck-r54.md:103-109` | the three drift leads | same |

Host claims in the draft are the host read at commands 11-14, dated 2026-10-27 (kernel `7.2.11-arch1-1`); they are the
seat's own observation and agree with `.ufo/waves/round-54/evidence/sweeps.txt:20-31`.

## Constraints observed

- No write outside this report: SKILL.md, SHONEN.md, SCORECARD.md, LOG.md, PROVINCE.md, `corpus/`, `tools/`,
  `considerthese/` and every other `round-54/` file were read only. `git status --porcelain SKILL.md` was the sole
  git call, read-only.
- No clone was taken (every cited byte is a committed lane file); scratch existed only as an empty `tmp/` and was
  removed. No pacman, no installs, no `~/.local/bin` writes.
- Host: reads only. No sysctl write, no poison injection, no module load, no systemctl, no cgroup change, no
  allocation. `Memory failure:` text was never counted.
- No subagent dispatch (leaf seat). No vote lines emitted; no line of this report begins with a vote token.

## Out of scope (not drafted, deliberately)

- Gate-registry rows for the round's two scoring counters (`count-c1.py`, `count-c2.py`): not requested by this seat,
  and their selftest tallies are the L1's to record (round 50 registered its counters; a registry row drafted from an
  unrun selftest would be a pin guessed, not measured).
- Any change to the frozen counters, predicates, controls or kill rules. The counter weakness observed at command 15
  (`voted=0` at data, `failed=votes`) is a staging fact of the wave, not a defect.
- Entry prose corrections: the ledger and entry are the L1's to correct; Findings 3 and 4 name two such candidates
  with the line.

## Findings

| severity | finding | file / line |
|---|---|---|
| HIGH | The uncommitted Round54 draft says the panic sysctl "is new in v7.3". An ENTAILMENT voter judged exactly that wording ("Version 7.3 adds") an overclaim on the same proposition (hash `734269273c22`, `.ufo/waves/round-54/w1/Mo54En07.md:70`): the v7.3 `vm.rst` never says when the sysctl was added. The landed section must state the v7.3 documentation and the host's absence, not introduction-in-7.3. My draft does. | `SKILL.md:1227` |
| MED | The same draft's `HardwareCorrupted` row says "memory the kernel marked poisoned". The C2 row it is derived from drew an `overclaim` vote (`257f4acfda4e`, `.ufo/waves/round-54/w1/Mo54En11.md:88`): S502 says "the kernel identifies as corrupted", recognition, not a marking act. | `SKILL.md:1219` |
| MED | The draft at `SKILL.md:1211-1247` cites only S-numbers and QUALITY ids — no ledger line per row. The house shape used by Round53 puts a source cell on every row, and a reader cannot resolve `S521` to a line without `corpus/SOURCES.md`; my draft cites `memory-failure-kills-r54.md:<line>` on every row. | `SKILL.md:1211-1247` |
| MED | Entry wording overstates its own live evidence: "The kill and recovery lines, the counters and the two older sysctls exist on 7.2 as read live above". The live read (`.ufo/waves/round-54/evidence/sweeps.txt:20-31`, re-observed at command 12) covers the counters and the sysctls only; no v7.2 `mm/memory-failure.c` exists anywhere in the lane's evidence (`sources-r54/` holds v7.3 copies only; `find .ufo/waves/round-54 -name '*memory-failure*'` is empty). The line formats on 7.2 are **UNVERIFIED**. | `corpus/knowledge/memory-failure-kills-r54.md:85-86` |
| LOW | C2 row `c98ac2ffa163` carries an `overclaim` vote on its closing clause ("a repeated failure of a poisoned page is not counted again"; `.ufo/waves/round-54/w1/Mo54En05.md:43`). Any SKILL row or later entry prose must keep to the quoted guard (counter advanced for page types other than already-poisoned and PFN-map) and not restate the inference. My draft carries no counter-advance row at all. | `corpus/knowledge/memory-failure-kills-r54.md:34` |
| LOW | The `ras:memory_failure_event` tracepoint cannot be read on this host unprivileged: `/sys/kernel/tracing` is `drwx------ root root` (uid 1000 gets `Permission denied`). Its existence on 7.2.11 is nevertheless observed from `/proc/kallsyms` (22 symbols incl. `__tracepoint_memory_failure_event`). A future row that needs the event's `format` must say `unavailable (tracefs root-only)`, never absent. | host read, commands 13-14 |
| LOW | At data, C1 reads `voted=0 … failed=votes` and C2 `entailed=0 … failed=entailment` (`.ufo/waves/round-54/evidence/c1-at-data.txt`, `c2-at-data.txt`, exit 1 each). The vote snapshot at drafting (24 distinct `holds`, no `changed`, four `overclaim`) is mid-wave and is not a tally; a SKILL.md sentence that implies either predicate is met would be premature. My draft states the recheck rule only, with no verdict. | `.ufo/waves/round-54/evidence/c1-at-data.txt:3`, `c2-at-data.txt:3` |
