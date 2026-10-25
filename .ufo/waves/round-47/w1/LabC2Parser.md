# LabC2Parser — round 47 w1 seat report

Seat: LabC2Parser (leaf; C2 first falsifier). Hypothesis: `count-c2.py`'s
`parse_events()` extracts exactly the `TP_STRUCT__entry` fields of every
`TRACE_EVENT` in the committed v7.2 copy
`corpus/evidence/sources-r47/include_trace_events_oom.h`.

**Verdict: hypothesis CONFIRMED.** 8 events, 30 fields parsed; name
mismatch = 0, field mismatch = 0, no fields missed, no fields invented.
Inter-agreement: parser == hand reading of the header == host tracefs
formats (read-only).

## 1. Instrument integrity (frozen bytes)

Command `sha256sum` on the working tree (exit 0):

```
fc77b93338b3f49b9038eaac3832537b1be2e0ff9dff2476fef750153978901e  .../round-47/count-c2.py
82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d  .../sources-r47/include_trace_events_oom.h
452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e  .../sources-r47/mm_oom_kill.c
439ae8ec1e47cbf38770865e53e98bf2229e32a20c4b0f8178e6f19f34edbc50  .../sources-r47/mm_page_alloc.c
cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6  .../sources-r47/fs_proc_base.c
```

`count-c2.py` matches the frozen instrument (contract line 15); the header
and all three call-site copies match `PINS` (count-c2.py lines 35–40).

## 2. Module load, parse_events() output (TMPDIR = seat scratch)

Loaded via `importlib` (`spec_from_file_location`), `TMPDIR` and
`tempfile.tempdir` set to
`.scratch/r47-LabC2Parser/`. `parse_events(open(HDR).read())` printed:

```
EVENTS PARSED: 8
  compact_retry: ['max_retries', 'order', 'priority', 'result', 'ret', 'retries']
  finish_task_reaping: ['pid']
  mark_victim: ['anon_rss', 'comm', 'file_rss', 'oom_score_adj', 'pgtables', 'pid', 'shmem_rss', 'total_vm', 'uid']
  oom_score_adj_update: ['comm', 'oom_score_adj', 'pid']
  reclaim_retry_zone: ['available', 'min_wmark', 'no_progress_loops', 'node', 'order', 'reclaimable', 'wmark_check', 'zone_idx']
  skip_task_reaping: ['pid']
  start_task_reaping: ['pid']
  wake_reaper: ['pid']
```

## 3. Hand reading of the committed header (my reference)

All 8 `TRACE_EVENT`s and their `TP_STRUCT__entry` fields:

| event | line | fields (declaration form) |
|---|---|---|
| `oom_score_adj_update` | 12 | `pid` (`__field pid_t`), `comm` (`__array char TASK_COMM_LEN`), `oom_score_adj` (`__field short`) |
| `reclaim_retry_zone` | 34 | `node`, `zone_idx`, `order`, `reclaimable`, `available`, `min_wmark`, `no_progress_loops`, `wmark_check` (8 × `__field`) |
| `mark_victim` | 76 | `pid`, `comm` (`__string`), `total_vm`, `anon_rss`, `file_rss`, `shmem_rss`, `uid`, `pgtables`, `oom_score_adj` |
| `wake_reaper` | 118 | `pid` |
| `start_task_reaping` | 134 | `pid` |
| `finish_task_reaping` | 150 | `pid` |
| `skip_task_reaping` | 166 | `pid` |
| `compact_retry` | 183 (`#ifdef CONFIG_COMPACTION`) | `order`, `priority`, `result`, `retries`, `max_retries`, `ret` |

Total: 8 events, 30 fields. Programmatic diff of parser output vs this
reference: `NAME_MISMATCH: none`, `FIELD_MISMATCH: none`, all 8 rows OK.
The parser's `__array`/`__string` branches both fire exactly once
(`oom_score_adj_update.comm`, `mark_victim.comm`).

## 4. Host tracefs formats (read-only)

- First attempt `sudo -n cat /sys/kernel/tracing/events/oom/*/format` failed
  with `cat: '/sys/kernel/tracing/events/oom/*/format': No such file or
  directory` (EXIT=1): the glob is expanded by the non-root shell, which has
  no read permission on the `oom` events dir, so the literal pattern was
  passed to `cat`. Retried with expansion in the root shell:
  `sudo -n sh -c 'cat /sys/kernel/tracing/events/oom/*/format'` → EXIT=0.
- `/sys/kernel/debug/tracing/events/` does not exist (`ls` error, EXIT=2);
  only the sysfs tracefs at `/sys/kernel/tracing/` is mounted.
- Host exposes exactly 8 oom events with the same names: `compact_retry`,
  `finish_task_reaping`, `mark_victim`, `oom_score_adj_update`,
  `reclaim_retry_zone`, `skip_task_reaping`, `start_task_reaping`,
  `wake_reaper`. Per-event non-common field sets exactly match the parser
  output (the `common_type/common_flags/common_preempt_count/common_pid`
  fields in `format` are added by the tracing core, not by
  `TP_STRUCT__entry`). Spot checks: `mark_victim.comm` appears as
  `__data_loc char[] comm` (the `__string` form) and
  `oom_score_adj_update.comm` as `char comm[16]` (the `__array` form) — both
  captured.

## 5. Files changed

- Report only: `.ufo/waves/round-47/w1/LabC2Parser.md` (absolute
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-47/w1/LabC2Parser.md`).
- Scratch: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-LabC2Parser/`
  (created, used as TMPDIR).
- No production files touched; no git/jj mutation; no tool installs occurred
  (tooling-authorization record: N/A — no install/update needed).

## 6. Risks / notes

- Host comparison is separate own-work evidence per contract "named limits"; the
  counter itself never reads tracefs. Host kernel version not verified — the
  agreement is with the host's running kernel, which is not proven to be v7.2.
- `evaluate()`/`git_reader` and the full `C2=…` run were not exercised here
  (parent owns integration gates); this seat tested only `parse_events()`
  fidelity against the header and the host.
- No blocker; nothing UNVERIFIED except host kernel version identity (not
  obtainable read-only in scope and not required by the seat).
