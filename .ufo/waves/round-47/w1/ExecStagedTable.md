# W1 — ExecStagedTable: mechanistic tracepoint census of the staged r42 entry

Seat: `ExecStagedTable` (leaf, no subagents spawned). Godspeed framing applied: all reads
ran in one parallel batch.

## Scope

Mechanically compare three artifacts:

1. Staged entry: `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/oom-tracing-tracepoints-r42.md`
2. Committed kernel header copy: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r47/include_trace_events_oom.h`
3. Staged SOURCES row S507 (line 43): `/home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md`

No files were modified; no tools were installed or updated (no tooling changes this seat).
Host reads were read-only; no tracing enabled.

## Evidence (command + output + exit code)

### 1. Header TRACE_EVENT count (committed copy)

```
$ grep -c '^TRACE_EVENT(' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r47/include_trace_events_oom.h
8
exit=0
```

All 8 header events (from full read of the header, `[#74BD]`):

| # | TRACE_EVENT name | line |
|---|------------------|------|
| 1 | `oom_score_adj_update` | 12 |
| 2 | `reclaim_retry_zone` | 34 |
| 3 | `mark_victim` | 76 |
| 4 | `wake_reaper` | 118 |
| 5 | `start_task_reaping` | 134 |
| 6 | `finish_task_reaping` | 150 |
| 7 | `skip_task_reaping` | 166 |
| 8 | `compact_retry` | 183 (inside `#ifdef CONFIG_COMPACTION`, still a `TRACE_EVENT` invocation) |

### 2. Backticked identifiers in the staged entry

Regex `` `[^`]+` `` over the staged entry matched exactly seven backticked spans
(lines 6, 15, 16, 31, 33, 43):

- line 6: `` `pdftotext -enc UTF-8 roma.pdf - | grep -c 'mark_victim'` `` — a full
  command string, not an identifier (its `mark_victim` is a literal substring of the
  command, not a backticked identifier)
- line 15: `` `mark_victim` ``
- line 16: `` `start_task_reaping` ``, `` `finish_task_reaping` ``
- line 31: `` `lsm_oom_kill_check()` ``
- line 33: `` `lsm_oom_cleanup_container()` ``
- line 43: `` `host-oom-activity-r42.md` `` — a file reference, not a code identifier

### 3. S507 row quote (SOURCES.append.md line 43, raw)

- § quote column (the paper's own words): 「It leverages eBPF to hook into OOM-related
  kernel tracepoints such as mark_victim, start_task_reaping, and finish_task_reaping」
  — names 3 identifiers, **not backticked**.
- Claim column: backticked `` `mark_victim` ``, `` `start_task_reaping` ``, `` `finish_task_reaping` ``, `` `lsm_oom_kill_check()` ``, `` `lsm_oom_cleanup_container()` ``.

## Table: identifier × header × staged entry × staged quote

| identifier | in header (TRACE_EVENT)? | in staged entry? | in staged quote (S507 § column)? |
|---|---|---|---|
| `mark_victim` | yes (line 76) | yes (line 15) | yes |
| `start_task_reaping` | yes (line 134) | yes (line 16) | yes |
| `finish_task_reaping` | yes (line 150) | yes (line 16) | yes |
| `lsm_oom_kill_check()` | no (LSM hook, not a TRACE_EVENT) | yes (line 31) | no (named only in the row's claim column) |
| `lsm_oom_cleanup_container()` | no (LSM hook, not a TRACE_EVENT) | yes (line 33) | no (named only in the row's claim column) |
| `host-oom-activity-r42.md` | no (file reference) | yes (line 43) | no |
| `oom_score_adj_update` | yes (line 12) | no | no |
| `reclaim_retry_zone` | yes (line 34) | no | no |
| `wake_reaper` | yes (line 118) | no | no |
| `skip_task_reaping` | yes (line 166) | no | no |
| `compact_retry` | yes (line 183) | no | no |

## Findings

1. **Header defines 8 TRACE_EVENTs; the staged entry claims exactly 3.** Mechanical
   counts: header `grep -c '^TRACE_EVENT('` = 8 (exit 0); backticked tracepoint
   identifiers in the staged entry = 3 (`mark_victim`, `start_task_reaping`,
   `finish_task_reaping`). The staged entry's headline claim ("exactly three named
   tracepoints") excludes 5 of the committed header's events: `oom_score_adj_update`,
   `reclaim_retry_zone`, `wake_reaper`, `skip_task_reaping`, `compact_retry`.
2. **The staged S507 quote is consistent with the entry's claim, not with the header.**
   The § quote names exactly the same three tracepoints as the entry. The two LSM hooks
   (`lsm_oom_kill_check`, `lsm_oom_cleanup_container`) appear only in the row's claim
   column, not in the quoted paper text — they are not tracepoints and correctly absent
   from the header.
3. **The 5 unclaimed header events touch the same OOM lifecycle surface the entry
   describes** (victim mark/reap phases plus retry/score events): `mark_victim`
   (chosen by the entry), `wake_reaper`/`start_task_reaping`/`finish_task_reaping`/
   `skip_task_reaping` (reaper lifecycle — entry claims only start+finish),
   `oom_score_adj_update` (score update), `reclaim_retry_zone` and `compact_retry`
   (reclaim/compaction retries).
4. **Entry-internal aside (out of table scope):** the entry's `recheck:` command
   `grep -c 'mark_victim'` -> 3 counts string occurrences in the paper PDF, not kernel
   tracepoints; it is a count of a different thing and says nothing about header event
   count.

## Risks / blockers

- None for this seat's measurement. The staged entry is at odds with the committed
  header (3 claimed vs 8 defined), which is the C2 falsifier the wave targets; the
  discrepancy is fully characterized above.
- UNVERIFIED: nothing — all three sources were read directly (staged entry, committed
  header copy, S507 raw row); the header count command ran with exit 0.
