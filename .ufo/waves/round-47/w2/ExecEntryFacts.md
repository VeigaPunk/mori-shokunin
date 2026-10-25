# ExecEntryFacts — round 47 wave w2

Seat: `ExecEntryFacts` (executor / leaf). Skill: godspeed.
Target: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/oom-tracepoints-r47.md` — verify every line number, function name and field claim against the committed copies in `corpus/evidence/sources-r47/` (`include_trace_events_oom.h`, `mm_oom_kill.c`, `mm_page_alloc.c`, `fs_proc_base.c`).

**Verdict: HOLDS.** Every line-number, function-name, field-set and call-site claim checked against the committed copies is true. No break found. One claim (S005 master byte-identity) is not derivable from the committed copies alone and was verified live against upstream; the rest are fully verified against the committed copies.

No tools were installed or updated (RULES.md record: none — built-in grep/awk/sed/sha256sum/curl only; no pacman/uv/npm touched).

## Checks and evidence

All paths absolute under `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r47/`.

### S475 — header count, event names, line numbers, sha256

| Claim | Source line | Verdict |
|---|---|---|
| `grep -c '^TRACE_EVENT('` → `8` | `include_trace_events_oom.h` — `grep -c '^TRACE_EVENT('` → `8`, exit 0 | holds |
| Header lines 12, 34, 76, 118, 134, 150, 166, 183 hold the eight TRACE_EVENT definitions | same file — `grep -n '^TRACE_EVENT('` → exactly 12 `oom_score_adj_update`, 34 `reclaim_retry_zone`, 76 `mark_victim`, 118 `wake_reaper`, 134 `start_task_reaping`, 150 `finish_task_reaping`, 166 `skip_task_reaping`, 183 `compact_retry` | holds |
| sha256 `82f04ad4…` of committed header | `sha256sum` → `82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d` | holds |
| Field sets per event (TP_STRUCT__entry) | header lines 18–22, 46–55, 81–91, 123–125, 139–141, 155–157, 171–173, 194–201 | holds (exact match, see table below) |
| `mark_victim` printk line 105 reads `total-vm=…kB anon-rss=…kB file-rss:…kB shmem-rss:…kB` | header line 105: `TP_printk("pid=%d comm=%s total-vm=%lukB anon-rss=%lukB file-rss:%lukB shmem-rss:%lukB uid=%u pgtables=%lukB oom_score_adj=%hd", …)` — hyphens and mixed `=`/`:` separators confirmed | holds |
| "Field names are TP_STRUCT__entry names, not TP_printk labels" | e.g. `total_vm` (line 84) vs `total-vm` (line 105); `shmem_rss` (87) vs `shmem-rss` (105) | holds |

Field-set detail (claim vs TP_STRUCT__entry):

| Event | Claimed fields | Verified __field/__string set |
|---|---|---|
| `oom_score_adj_update` | pid, comm, oom_score_adj | pid_t pid, char comm[TASK_COMM_LEN], short oom_score_adj (18–21) |
| `reclaim_retry_zone` | node, zone_idx, order, reclaimable, available, min_wmark, no_progress_loops, wmark_check | node, zone_idx, order, reclaimable, available, min_wmark, no_progress_loops, wmark_check (46–54) |
| `mark_victim` | pid, comm, total_vm, anon_rss, file_rss, shmem_rss, uid, pgtables, oom_score_adj | pid, comm (__string), total_vm, anon_rss, file_rss, shmem_rss, uid, pgtables, oom_score_adj (81–90) |
| `wake_reaper` / `start_task_reaping` / `finish_task_reaping` / `skip_task_reaping` | pid | pid only (123–124, 139–140, 155–156, 171–172) |
| `compact_retry` | order, priority, result, retries, max_retries, ret | order, priority, result, retries, max_retries, ret (194–200) |

### S476 — call sites (grep -n over committed copies; awk-enclosing-function)

| Claim (table / lifecycle) | Committed source line | Enclosing function (awk) | Verdict |
|---|---|---|
| `__set_oom_adj`, base.c:1158 emits `trace_oom_score_adj_update` | `fs_proc_base.c:1158` `trace_oom_score_adj_update(task);` | `static int __set_oom_adj(struct file *file, int oom_adj, bool legacy)` def 1106 | holds |
| `should_reclaim_retry`, page_alloc.c:4630 emits `trace_reclaim_retry_zone` | `mm_page_alloc.c:4630` `trace_reclaim_retry_zone(z, order, reclaimable, available, min_wmark, *no_progress_loops, wmark);` | `should_reclaim_retry(gfp_t gfp_mask, unsigned order, …)` def 4581 | holds |
| `mark_oom_victim`, oom_kill.c:774 emits `trace_mark_victim` | `mm_oom_kill.c:774` `trace_mark_victim(tsk, cred->uid.val);` | `static void mark_oom_victim(struct task_struct *tsk)` def 751 | holds |
| `wake_oom_reaper`, oom_kill.c:673 emits `trace_wake_reaper` | `mm_oom_kill.c:673` `trace_wake_reaper(tsk->pid);` | `static void wake_oom_reaper(struct timer_list *timer)` def 656 | holds |
| `oom_reap_task_mm`, oom_kill.c:582 emits `trace_start_task_reaping` | `mm_oom_kill.c:582` | `static bool oom_reap_task_mm(struct task_struct *tsk, struct mm_struct *mm)` def 562 | holds |
| `oom_reap_task_mm`, oom_kill.c:595 emits `trace_finish_task_reaping` | `mm_oom_kill.c:595` | same, def 562 | holds |
| `oom_reap_task_mm`, oom_kill.c:567, 578 emit `trace_skip_task_reaping` | `mm_oom_kill.c:567` and `:578` | same, def 562 | holds |
| `should_compact_retry`, page_alloc.c:4265 emits `trace_compact_retry` | `mm_page_alloc.c:4265` `trace_compact_retry(order, priority, compact_result, retries, max_retries, ret);` | `should_compact_retry(gfp_t gfp_mask, struct alloc_context *ac, int order, …)` def 4202 (CONFIG_COMPACTION branch; non-COMPACTION stub at 4279 contains no trace) | holds |

### S476 lifecycle statements (mm_oom_kill.c)

| Claim | Verified evidence | Verdict |
|---|---|---|
| `mark_oom_victim()` (751–775): sets TIF_MEMDIE, records oom_mm, thaws, then emits | 758 `test_and_set_tsk_thread_flag(tsk, TIF_MEMDIE)`; 762 `cmpxchg(&tsk->signal->oom_mm, NULL, mm)`; 771 `thaw_process(tsk)`; 774 trace (last statement before `put_cred` at 775) | holds |
| "Only event naming the victim's command and uid" | header: only `mark_victim` has both `comm` and `uid` fields; `oom_score_adj_update` has comm but no uid; reaper events pid-only; retry events no identity | holds |
| `wake_oom_reaper()` (656–674): links onto `oom_reaper_list`, emits; no emit if `MMF_OOM_SKIP` | 670–671 assignment to `oom_reaper_list`; 673 trace; 663–667 early `return` on `mm_flags_test(MMF_OOM_SKIP, mm)` before trace | holds |
| `oom_reap_task_mm()` (562–599): skip when no mmap read lock or MMF_OOM_SKIP; else start, then finish on full and partial path via `out_finish`; partial returns false | 566 `if (!mmap_read_trylock(mm))` → 567 skip; 577 `mm_flags_test(MMF_OOM_SKIP, mm)` → 578 skip; 582 start; 586 `if (!ret) goto out_finish;` (partial); `out_finish:` at 594 → 595 finish; `return ret` at 599 | holds |
| [INFERENCE] one victim can produce several skip/start/finish triples across retries | explicitly tagged inference in the doc, not a factual claim; consistent with 586–587 partial-retry path | holds (as inference) |

### S005 — "same header at master c03c1a14, byte-identical"

Not derivable from the committed copies (different source). Verified live: `curl -fsSL https://raw.githubusercontent.com/torvalds/linux/c03c1a14/include/trace/events/oom.h` → sha256 `82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d`, `cmp` → BYTE-IDENTICAL with the committed copy; `grep -c '^TRACE_EVENT('` → 8. **holds** (bonus check, outside the committed-copy line-claim scope).

### UNVERIFIED (out of scope for committed-copy line claims)

- S477 (host tracefs `events/oom/` listing/formats) — a host observation, not a line/function/field claim against `sources-r47/`; not re-verified here (host reads are read-only; the doc itself labels the tracefs read root-only).
- S478 (ROMA paper p. 3016) — external paper quote; no committed copy in `sources-r47/` to check against.
- The `recheck` protocol line (`count-c2.py` re-derivation) belongs to the C2 seat, not this one.

## Summary

All 8 TRACE_EVENT line numbers, all 8 event names, all 8 field sets, the `mark_victim` printk line-105 rendering claim, and all 8 call-site line/function claims hold exactly against the committed copies. sha256 prefix `82f04ad4…` confirmed. No breaks, no discrepancies.

Report path: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-47/w2/ExecEntryFacts.md`
