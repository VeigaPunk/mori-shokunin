# Control — the staged claim as a table (three tracepoints)

source: S475 — Linux v7.2 include/trace/events/oom.h
verified-at: 2026-10-25
recheck: on-release

| tracepoint | fields | emitted in |
|---|---|---|
| `mark_victim` | `pid`, `comm`, `total_vm`, `anon_rss`, `file_rss`, `shmem_rss`, `uid`, `pgtables`, `oom_score_adj` | `mm/oom_kill.c` |
| `start_task_reaping` | `pid` | `mm/oom_kill.c` |
| `finish_task_reaping` | `pid` | `mm/oom_kill.c` |
