# The OOM tracepoints at Linux v7.2: eight events, and which one names the victim

source: S475 — Linux include/trace/events/oom.h at tag v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/trace/events/oom.h — committed copy `corpus/evidence/sources-r47/include_trace_events_oom.h` (sha256 `82f04ad4…`); S476 — mm/oom_kill.c, mm/page_alloc.c, fs/proc/base.c at v7.2 (emitting call sites); S477 — this host's tracefs `events/oom/` listing and formats (own-work); S478 — ROMA full text, p. 3016 (what an eBPF observer hooks); S005 — the same header at master `c03c1a14`, byte-identical
verified-at: 2026-10-25
recheck: on-release — `python3 .ufo/waves/round-47/count-c2.py <rev>` re-derives every name, field set and call site below from the committed copies; `curl -fsSL https://raw.githubusercontent.com/torvalds/linux/<tag>/include/trace/events/oom.h | grep -c '^TRACE_EVENT('` on a new tag
coverage-map: FR13
ground: frontier item **FR13** — "eBPF kill/OOM tracing … a resident tracer is outside the census, so retain this as knowledge/frontier only" (`corpus/README.md` Frontier table)

## Claim

Linux v7.2 defines **eight** trace events in the `oom` system — not three. One of them,
`mark_victim`, carries the victim's identity and memory at the moment the kernel marks it;
four (`wake_reaper`, `start_task_reaping`, `finish_task_reaping`, `skip_task_reaping`)
carry only a pid and trace the OOM reaper; the other three record allocator retry
decisions (`reclaim_retry_zone`, `compact_retry`) and `oom_score_adj` writes
(`oom_score_adj_update`). The count is mechanical: `grep -c '^TRACE_EVENT(' 
corpus/evidence/sources-r47/include_trace_events_oom.h` → `8` (S475, header lines 12, 34,
76, 118, 134, 150, 166, 183).

## Catalogue (S475 fields, S476 call sites)

| tracepoint | fields | emitted in | what an observer reads |
|---|---|---|---|
| `oom_score_adj_update` | `pid`, `comm`, `oom_score_adj` | `fs/proc/base.c` | a task's `oom_score_adj` was written (`__set_oom_adj`, base.c:1158) |
| `reclaim_retry_zone` | `node`, `zone_idx`, `order`, `reclaimable`, `available`, `min_wmark`, `no_progress_loops`, `wmark_check` | `mm/page_alloc.c` | the allocator's per-zone reclaim-retry decision before an OOM (`should_reclaim_retry`, page_alloc.c:4630) |
| `mark_victim` | `pid`, `comm`, `total_vm`, `anon_rss`, `file_rss`, `shmem_rss`, `uid`, `pgtables`, `oom_score_adj` | `mm/oom_kill.c` | the victim chosen: pid, comm, uid and its memory at mark time (`mark_oom_victim`, oom_kill.c:774) |
| `wake_reaper` | `pid` | `mm/oom_kill.c` | the victim was queued for the OOM reaper (`wake_oom_reaper`, oom_kill.c:673) |
| `start_task_reaping` | `pid` | `mm/oom_kill.c` | the reaper began unmapping the victim's memory (`oom_reap_task_mm`, oom_kill.c:582) |
| `finish_task_reaping` | `pid` | `mm/oom_kill.c` | the reaper finished, fully or partly (`oom_reap_task_mm`, oom_kill.c:595) |
| `skip_task_reaping` | `pid` | `mm/oom_kill.c` | the reaper skipped this attempt: mmap lock not taken, or `MMF_OOM_SKIP` set (`oom_reap_task_mm`, oom_kill.c:567, 578) |
| `compact_retry` | `order`, `priority`, `result`, `retries`, `max_retries`, `ret` | `mm/page_alloc.c` | the allocator's compaction-retry decision (`should_compact_retry`, page_alloc.c:4265) |

Field names are the `TP_STRUCT__entry` names (S475), not the `TP_printk` labels: the
printed line for `mark_victim` reads `total-vm=…kB anon-rss=…kB file-rss:…kB shmem-rss:…kB`
(header line 105), so a parser keyed on the printed text sees hyphens and two different
separators (`=` and `:`) for the same family of fields.

## Lifecycle at v7.2 (S476)

1. `mark_oom_victim()` sets `TIF_MEMDIE`, records the victim's `oom_mm`, thaws it, then emits
   `trace_mark_victim(tsk, cred->uid.val)` (oom_kill.c:751-775). This is the only event in
   the set that names the victim's command and uid.
2. `wake_oom_reaper()` links the task onto `oom_reaper_list` and emits
   `trace_wake_reaper(tsk->pid)` (oom_kill.c:656-674) — unless the victim already exited on
   its own (`MMF_OOM_SKIP`), in which case nothing is emitted.
3. `oom_reap_task_mm()` emits `skip_task_reaping` when it cannot take the mmap read lock or
   the mm is already marked skip; otherwise `start_task_reaping`, then `finish_task_reaping`
   on both the full and the partial-reap path (`out_finish`, oom_kill.c:562-599). A
   `finish` therefore does not mean all memory was reclaimed; the partial case returns
   false and the caller retries later. [INFERENCE] One victim can produce several
   skip/start/finish triples across retries.

## What it changes for mori

- FR13 stops being a topic and becomes a named event set with field schemas. The only
  identity-bearing event is `mark_victim`: **pid, comm and uid of the victim**. No event in
  the set carries a cgroup path, a memcg name, or the task that triggered the allocation
  failure — the kernel's own record names the victim, not the culprit. Attribution of a kill
  to a fleet seat still has to come from the journal/cgroup evidence the lane already holds
  (FR1, FR10).
- The staged assimilation entry `oom-tracing-tracepoints-r42.md` (shokuknow
  `merge/mori/`) headlined "exactly three named tracepoints". The paper it cites says "It
  leverages eBPF to hook into OOM-related kernel tracepoints such as mark_victim,
  start_task_reaping, and finish_task_reaping" (S478, p. 3016, §I) — three examples, not an
  inventory — and the header defines eight. That headline is refused; see
  `corpus/lessons/round-47.md` `## Gate`.

## Boundaries

- **Knowledge only.** A resident tracer (eBPF, `perf`, tracefs `enable`) is outside the
  one-shot census and outside this lane's detection-and-report remit; mori never enables an
  event or writes tracefs. The host reading (S477) was `sudo -n ls`/`cat` of
  `/sys/kernel/tracing/events/oom/` only.
- Tracepoint sets and field layouts are kernel-version specific: this entry holds for the
  v7.2 tag copies pinned by sha256 in `.ufo/waves/round-47/count-c2.py`; S005 holds the
  `mark_victim` schema at an earlier master commit. Re-derive on a new tag before relying
  on it.
- Reading tracefs requires root on this host (`ls /sys/kernel/tracing/events/oom` as the
  user → `Permission denied`, 2026-10-25); an unreadable tracefs is `unavailable`, never
  "no OOM events".
