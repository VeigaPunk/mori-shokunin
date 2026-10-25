# ScribeRowHost — round 47 wave w1 report (own-work SOURCES row S477)

Seat: `ScribeRowHost` (leaf scribe — no subagents dispatched). Date: 2026-10-25.
Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Contract read: `.ufo/waves/round-47/contract.md` (freeze `63eecf2738db96f46b0bd02b1b2dfd66787493d0`; entering tip `2d85e33d14198d388fd3cda9cc15ec07e57e7a53`).

Scope: own-work SOURCES row S477 for this host's tracefs oom reading — detection and report only.
No tracefs writes; host state untouched; `sudo -n` used only for read-only `ls`/`cat`.

## Tooling

No tools installed or upgraded (nothing was needed; existing `bash`, `ls`, `cat`, `uname`, `sudo`, `stat` used).
No `pacman` transactions. Tooling directive `~/.omp/agent/RULES.md` read.

## Observed evidence (command + output + exit code)

### Host kernel identity

```
$ uname -r
7.2.11-arch1-1        (exit 0)
$ uname -m
x86_64                (exit 0)
```

### Tracefs oom event listing (read-only, `sudo -n ls`)

```
$ sudo -n ls /sys/kernel/tracing/events/oom
compact_retry
enable
filter
finish_task_reaping
mark_victim
oom_score_adj_update
reclaim_retry_zone
skip_task_reaping
start_task_reaping
wake_reaper
(exit 0)
```

Type check via `sudo -n ls -la /sys/kernel/tracing/events/oom`: `enable` and `filter` are regular files
(`-rw-r----- 1 root root`), the other eight entries are directories. `enable`/`filter` are subsystem control
files, not tracepoints — the host therefore exposes exactly **8 oom trace events**:

`oom_score_adj_update`, `reclaim_retry_zone`, `mark_victim`, `wake_reaper`, `start_task_reaping`,
`finish_task_reaping`, `skip_task_reaping`, `compact_retry`.

### Event format captures (read-only, `sudo -n cat`)

For each of the 8 events, `sudo -n cat /sys/kernel/tracing/events/oom/<event>/format` exited 0 and was captured:

| event | tracefs ID |
|---|---|
| compact_retry | 577 |
| skip_task_reaping | 578 |
| finish_task_reaping | 579 |
| start_task_reaping | 580 |
| wake_reaper | 581 |
| mark_victim | 582 |
| reclaim_retry_zone | 583 |
| oom_score_adj_update | 584 |

### Control reads (read-only)

```
$ sudo -n cat /sys/kernel/tracing/events/oom/enable
0                       (exit 0)  -> all oom tracepoints currently disabled
$ sudo -n cat /sys/kernel/tracing/events/oom/filter
### global filter ###
# Use this to set filters for multiple events.
# Only events with the given fields will be affected.
# If no events are modified, an error message will be displayed here
                        (exit 0)  -> control file, not an event
```

```
$ ls /sys/kernel/tracing/events/oom
ls: cannot open file '/sys/kernel/tracing/events/oom': Permission denied
(exit 2)  -> unprivileged access denied; readable only as root
```

## Comparison: each format's non-common fields vs committed v7.2 header TP_STRUCT__entry

Header compared: `corpus/evidence/sources-r47/include_trace_events_oom.h` (committed copy of Linux
v7.2 `include/trace/events/oom.h`). "Non-common" = the fields after the four `common_*` fields
(`common_type`, `common_flags`, `common_preempt_count`, `common_pid`).

| event | format non-common fields (name: type) | header TP_STRUCT__entry fields | equal |
|---|---|---|---|
| oom_score_adj_update | pid: pid_t, comm: char[16], oom_score_adj: short | pid: pid_t, comm: char[TASK_COMM_LEN], oom_score_adj: short | yes |
| reclaim_retry_zone | node: int, zone_idx: int, order: int, reclaimable: unsigned long, available: unsigned long, min_wmark: unsigned long, no_progress_loops: int, wmark_check: bool | identical set | yes |
| mark_victim | pid: int, comm: __data_loc char[] (string), total_vm: unsigned long, anon_rss: unsigned long, file_rss: unsigned long, shmem_rss: unsigned long, uid: uid_t, pgtables: unsigned long, oom_score_adj: short | identical set (`comm` = `__string`) | yes |
| wake_reaper | pid: int | pid: int | yes |
| start_task_reaping | pid: int | pid: int | yes |
| finish_task_reaping | pid: int | pid: int | yes |
| skip_task_reaping | pid: int | pid: int | yes |
| compact_retry | order: int, priority: int, result: int, retries: int, max_retries: int, ret: bool | identical set | yes |

The `comm[16]` field implies TASK_COMM_LEN=16, matching the header's `__array(char, comm, TASK_COMM_LEN)`.
`mark_victim`'s dynamic `__data_loc char[] comm` matches the header's `__string(comm, task->comm)`.

All 8 events exist on this host and every non-common field set equals the v7.2 header's
TP_STRUCT__entry field set (names and types, order preserved).

## Draft SOURCES row S477 (own-work, tier A, scope = this host's running kernel only)

```text
| S477 | own-work: this host's tracefs oom events — sudo -n ls and cat under /sys/kernel/tracing/events/oom on kernel 7.2.11-arch1-1, receipt .ufo/waves/round-47/evidence/host-tracefs.txt | own-work | A | this host's running kernel only, read-only on 2026-10-25: which oom events it exposes and their field layouts; not any other host or kernel | receipt lines for the listing and each event format; mark_victim format fields pid comm total_vm anon_rss file_rss shmem_rss uid pgtables oom_score_adj; events/oom/enable reads 0; unprivileged ls is Permission denied | The running kernel exposes the same eight oom events as the v7.2 header, all disabled, readable only as root | mined | 2026-10-25 | 90d | corpus/knowledge/oom-tracepoints-r47.md |
```

Notes for the L1: `corpus/SOURCES.md` line 256 already carries an S477 row in the working tree with the
same content as this draft; I did not edit SOURCES.md (seat rule). The raw captures backing the receipt
anchor currently live in `.scratch/r47-ScribeRowHost/` (see Artifacts); if the canonical receipt
`.ufo/waves/round-47/evidence/host-tracefs.txt` is wanted, the L1 can promote the bytes — seat writes are
limited to the report file and scratch.

## Gate quote

Verbatim from the captured receipt files (receipt lines cited in the row's anchor):

1. From `format-mark_victim.txt` (event with the richest field set):
```
	name: mark_victim
ID: 582
...
	field:int pid;	offset:8;	size:4;	signed:1;
	field:__data_loc char[] comm;	offset:12;	size:4;	signed:0;
	field:unsigned long total_vm;	offset:16;	size:8;	signed:0;
	field:unsigned long anon_rss;	offset:24;	size:8;	signed:0;
	field:unsigned long file_rss;	offset:32;	size:8;	signed:0;
	field:unsigned long shmem_rss;	offset:40;	size:8;	signed:0;
	field:uid_t uid;	offset:48;	size:4;	signed:0;
	field:unsigned long pgtables;	offset:56;	size:8;	signed:0;
	field:short oom_score_adj;	offset:64;	size:2;	signed:1;
```
2. From `oom-events-ls.txt` (event listing receipt): the directory entries `compact_retry … wake_reaper`
   (eight events, plus `enable`/`filter` control files).
3. From `control-reads.txt`: `0` (events/oom/enable), and the global-filter comment block for `filter`.

## Findings

- Host kernel `7.2.11-arch1-1` (x86_64) exposes exactly the same 8 oom trace events as the committed
  Linux v7.2 `include/trace/events/oom.h` copy: `oom_score_adj_update`, `reclaim_retry_zone`,
  `mark_victim`, `wake_reaper`, `start_task_reaping`, `finish_task_reaping`, `skip_task_reaping`,
  `compact_retry`.
- For each of the 8 events, the format's non-common fields equal that event's TP_STRUCT__entry field set
  in the v7.2 header (names and types; order preserved) — no differences found.
- All 8 tracepoints are currently disabled (`events/oom/enable` reads `0`).
- `enable` and `filter` are control files, not events; excluded from the event count.
- The oom tracefs subtree is readable only as root on this host (unprivileged `ls` exits 2,
  Permission denied).
- No tracefs writes, no host state changes, no tracing enabled. Detection and report only.

## Out-of-scope

- C1/C2 counters and their scoring are not this seat's (leaf scribe; not an independent judge). The v7.2
  header field comparison above is one input to S475/S477 provenance, not a C2 verdict.
- No verification that the committed header copy matches the upstream github raw bytes at tag v7.2
  (that is S475's row, this seat did not re-derive its sha256).
- Not this host's other tracefs subsystems; only `events/oom`.

## Artifacts (raw captures, scratch dir)

Scratch: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-ScribeRowHost/`

| file | sha256 |
|---|---|
| oom-events-ls.txt | dc4e5473d65e2b510576ff6a3be87af8f4d9de39a89d98c32454c4e7d4ec8e2a |
| oom-events-ls-la.txt | 81366db42136ef7bb38b738880de4b40f750dd79f372599200092b02cb8b513b |
| control-reads.txt | a07a970fbedb2977b0671d3a84a807cc2d2dca3bd075e637d353152fec58a154 |
| format-compact_retry.txt | a1a537aee924ceef6d23ef6cfebdb31649d3836b75282e90a197162b4f4204b1 |
| format-skip_task_reaping.txt | b1fa436057b78511839d805d45e7f5736f3e52708d14e79e4a34e5fdb68ab727 |
| format-finish_task_reaping.txt | f1a877eeb046a7cf879e4a43ca14313ef8a68708daa6ecd99ed12ada7af31405 |
| format-start_task_reaping.txt | 80d29377e48caf93433d285025add1c945c27d7d868e8e921c36da871690814d |
| format-wake_reaper.txt | c610446ef3c6cc74ce4a5926e16ba198cf0dc643caeb8c21870bcb4960a9a35c |
| format-mark_victim.txt | 0c660ad2946c1ea2db0fba9518f4fbb18c9d8bb8b222fb48167c521c73f8ebe2 |
| format-reclaim_retry_zone.txt | 6d2ea0b86fb764414fbea37012f94fefcbaf2388db4fc84b3eb1e6d369a9e419 |
| format-oom_score_adj_update.txt | 616b54e611ef0bb9ca449da8548cb1390d819fdb2d90b97032c13a714efa6b95 |
| plain-ls.txt | (unprivileged denial receipt; error text in file) |

Report file: `.ufo/waves/round-47/w1/ScribeRowHost.md` (this file).
