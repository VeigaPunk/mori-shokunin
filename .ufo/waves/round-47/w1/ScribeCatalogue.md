# ScribeCatalogue — round 47 w1 C2 catalogue draft

Seat: ScribeCatalogue (leaf, no subagents). Scope: draft the C2 catalogue table for
`corpus/knowledge/oom-tracepoints-r47.md` from the committed Linux v7.2
`include/trace/events/oom.h` copy. I wrote only this report file; no production file was
edited. No tool installs were needed (read/grep only, plus one read-only `sha256sum`).
No lane tools were run, so no `TMPDIR` scratch was created.

## Draft table (for L1 integration into corpus/knowledge/oom-tracepoints-r47.md)

```markdown
source: S475 — committed Linux v7.2 include/trace/events/oom.h copy (corpus/evidence/sources-r47/include_trace_events_oom.h), fetched 2026-10-25 from https://raw.githubusercontent.com/torvalds/linux/v7.2/include/trace/events/oom.h
verified-at: 2026-10-25
recheck: 180d — grep -c '^TRACE_EVENT(' include_trace_events_oom.h -> 8

| tracepoint | fields | emitted in | what an observer reads |
| `oom_score_adj_update` | `pid`, `comm`, `oom_score_adj` | `fs/proc/base.c` (fs_proc_base.c:1158) | pid, comm, and oom_score_adj value |
| `reclaim_retry_zone` | `node`, `zone_idx`, `order`, `reclaimable`, `available`, `min_wmark`, `no_progress_loops`, `wmark_check` | `mm/page_alloc.c` (mm_page_alloc.c:4630) | node/zone, order, reclaimable/available/min_wmark pages, progress loops, wmark flag |
| `mark_victim` | `pid`, `comm`, `total_vm`, `anon_rss`, `file_rss`, `shmem_rss`, `uid`, `pgtables`, `oom_score_adj` | `mm/oom_kill.c` (mm_oom_kill.c:774) | pid, comm, vm/rss totals in kB, uid, pgtables, oom_score_adj |
| `wake_reaper` | `pid` | `mm/oom_kill.c` (mm_oom_kill.c:673) | pid of the task the reaper wakes for |
| `start_task_reaping` | `pid` | `mm/oom_kill.c` (mm_oom_kill.c:582) | pid of the task whose reaping starts |
| `finish_task_reaping` | `pid` | `mm/oom_kill.c` (mm_oom_kill.c:595) | pid of the task whose reaping finished |
| `skip_task_reaping` | `pid` | `mm/oom_kill.c` (mm_oom_kill.c:567, 578) | pid of the task skipped by the reaper |
| `compact_retry` | `order`, `priority`, `result`, `retries`, `max_retries`, `ret` | `mm/page_alloc.c` (mm_page_alloc.c:4265) | order, compaction priority/feedback, retries, should_retry flag |
```

## Field-set verification against header line numbers (include_trace_events_oom.h)

Each row's field set was taken from that event's `TP_STRUCT__entry` block. Line numbers are
from the committed copy read in full.

| event | TRACE_EVENT line | TP_STRUCT__entry lines | field → line | TP_printk lines |
|---|---|---|---|---|
| oom_score_adj_update | 12 | 18–22 | pid 19, comm 20, oom_score_adj 21 | 30–31 |
| reclaim_retry_zone | 34 | 46–55 | node 47, zone_idx 48, order 49, reclaimable 50, available 51, min_wmark 52, no_progress_loops 53, wmark_check 54 | 68–73 |
| mark_victim | 76 | 81–91 | pid 82, comm 83 (`__string`), total_vm 84, anon_rss 85, file_rss 86, shmem_rss 87, uid 88, pgtables 89, oom_score_adj 90 | 105–115 |
| wake_reaper | 118 | 123–125 | pid 124 | 131 |
| start_task_reaping | 134 | 139–141 | pid 140 | 147 |
| finish_task_reaping | 150 | 155–157 | pid 156 | 163 |
| skip_task_reaping | 166 | 171–173 | pid 172 | 179 |
| compact_retry | 183 | 194–201 | order 195, priority 196, result 197, retries 198, max_retries 199, ret 200 | 212–218 |

Note: `compact_retry` is defined inside `#ifdef CONFIG_COMPACTION` (line 182) but is still a
TRACE_EVENT in the committed copy; the counter (`count-c2.py`) parses it as event 8 of 8.

## Call-site verification (committed copies under corpus/evidence/sources-r47/)

| event | kernel path (committed copy) | `trace_<name>(` line(s) |
|---|---|---|
| oom_score_adj_update | fs/proc/base.c (fs_proc_base.c) | 1158 |
| reclaim_retry_zone | mm/page_alloc.c (mm_page_alloc.c) | 4630 |
| mark_victim | mm/oom_kill.c (mm_oom_kill.c) | 774 |
| wake_reaper | mm/oom_kill.c (mm_oom_kill.c) | 673 |
| start_task_reaping | mm/oom_kill.c (mm_oom_kill.c) | 582 |
| finish_task_reaping | mm/oom_kill.c (mm_oom_kill.c) | 595 |
| skip_task_reaping | mm/oom_kill.c (mm_oom_kill.c) | 567, 578 |
| compact_retry | mm/page_alloc.c (mm_page_alloc.c) | 4265 |

Each row's `emitted in` cell names exactly one of `mm/oom_kill.c`, `mm/page_alloc.c`,
`fs/proc/base.c`; the cited committed copy contains `trace_<name>(`. Other `trace_*` calls
in `mm_page_alloc.c` (e.g. `trace_mm_page_alloc_extfrag` 751/2402/2434,
`trace_mm_page_free` 1326, `trace_mm_page_free_batched` 3078, `trace_mm_page_alloc` 5326/7939,
`trace_mm_calculate_totalreserve_pages` 6396, `trace_mm_setup_per_zone_lowmem_reserve` 6440,
`trace_mm_setup_per_zone_wmarks` 6505) are not OOM-header events and are not in the catalogue.

## Provenance / frozen-bytes evidence

sha256 of the committed copies (read-only `sha256sum`), matching the counter's frozen PINS
(e.g. PINS has fs_proc_base.c = `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6`):

- include_trace_events_oom.h: `82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d`
- mm_oom_kill.c: `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e`
- mm_page_alloc.c: `439ae8ec1e47cbf38770865e53e98bf2229e32a20c4b0f8178e6f19f34edbc50`
- fs_proc_base.c: `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6`

## Findings / notes

- The staged assimilation entry `oom-tracing-tracepoints-r42.md` claims "exactly three named
  tracepoints" (mark_victim, start_task_reaping, finish_task_reaping — as named by source
  S507's paper). The committed kernel header defines **eight** TRACE_EVENTs; this catalogue
  covers all eight, so the FR13 knowledge entry supersedes the staged "three" claim with the
  full kernel-side event set.
- Counter-format alignment: header first cell `tracepoint` with cells `fields` and
  `emitted in` present; each row has four cells; field sets are comma-separated backticked
  names only (set equality with `parse_events`); each emitted-in cell carries exactly one
  backticked kernel path (line-number citations are plain text, which `SPAN` ignores).
