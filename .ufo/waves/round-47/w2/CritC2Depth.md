# CritC2Depth — C2 entry prose, checked against committed r47 sources

Seat: CritC2Depth (godspeed). Target: `corpus/knowledge/oom-tracepoints-r47.md` at landed tip
T = `68d66ca53d89be5c34a62f46af7c37449d9f9b63`. Attack: the five prose claims beyond what the
frozen counter checks, against the committed copies in `corpus/evidence/sources-r47/`.

## Baseline: the entry passes the frozen counter at T

```
$ TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-CritC2Depth \
  python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-47/count-c2.py \
  68d66ca53d89be5c34a62f46af7c37449d9f9b63
C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=68d66ca53d89be5c34a62f46af7c37449d9f9b63
exit=0
```

The prose below is therefore exactly the part the counter does not cover (contract "Named
limits": the counter does not check prose, lifecycle ordering claims, or the host kernel).

## Claim 1 — "only identity-bearing event is mark_victim: pid, comm and uid of the victim"

Evidence (`include_trace_events_oom.h`, committed copy):
- `mark_victim` `TP_STRUCT__entry` (lines 81–91) is the only one containing `__field(uid_t, uid)`
  and the only one reading the victim's task identity: `pid` + `__string(comm, task->comm)` + `uid`.
- `oom_score_adj_update` (lines 18–22) also carries `pid` + `comm` (`__array(char, comm, …)`),
  but of the task whose `oom_score_adj` was written — not the victim — and no `uid`.
- The four reaper events carry only `pid`; `reclaim_retry_zone` / `compact_retry` carry no task
  identity at all.

Verdict: **holds**, within the sentence's own scope ("of the victim"; "the only event in the set
that names the victim's command and uid" — entry lines 41–42, 56). Note: read as an unqualified
global "the only event carrying any identity", it would overreach, because `oom_score_adj_update`
does carry pid+comm; the entry's own table (row 1) discloses that, and the prose self-defines
"identity-bearing" as the victim's pid+comm+uid triple, so this is a scoped, accurate statement,
not an overreach in context.

## Claim 2 — "No event in the set carries a cgroup path, a memcg name, or the task that triggered the allocation failure"

Evidence: union of all `TP_STRUCT__entry` fields across the eight events (header lines 18–22,
46–55, 81–91, 123–125, 139–141, 155–157, 171–173, 194–201): pid, comm, oom_score_adj, node,
zone_idx, order, reclaimable, available, min_wmark, no_progress_loops, wmark_check, total_vm,
anon_rss, file_rss, shmem_rss, uid, pgtables, priority, result, retries, max_retries, ret. No
cgroup path, no memcg name, and no allocating-task identity: the two retry events take only a
zoneref/order/priority/result view (there is no task pointer in any `TP_PROTO` or entry).

Verdict: **holds**.

## Claim 3 — "A finish does not mean all memory was reclaimed; the partial case returns false and the caller retries later"

Evidence (`mm_oom_kill.c`, committed copy):
- Lines 584–587: `ret = __oom_reap_task_mm(mm); if (!ret) goto out_finish;` — the partial-reap
  path falls through to `out_finish:` and emits `trace_finish_task_reaping` (line 595). Finish is
  emitted on both the full and the partial path; only the `mmap_read_trylock`-fail / `MMF_OOM_SKIP`
  branches emit skip instead (lines 566–580).
- Lines 559–560 (function comment): "Returns true on success and false if none or part of the
  address space has been reclaimed and the caller should retry later."
- Lines 602–610: `MAX_OOM_REAP_RETRIES 10`; `while (attempts++ < … && !oom_reap_task_mm(…))
  schedule_timeout_idle(HZ/10);` — partial → false → retry.

Verdict: **holds**.

## Claim 4 — "One victim can produce several skip/start/finish triples across retries"

Evidence: same `oom_reap_task` loop — each of up to 10 attempts emits either `skip_task_reaping`
(lines 567, 578) or `start_task_reaping` + `finish_task_reaping` (lines 582, 595), and a false
return retries. A victim whose first attempt loses the lock (skip) and whose later successful
reap is partial (start+finish, retry) then gets a further skip or start/finish on the next attempt;
interleaved skip/start/finish sequences are therefore possible, and multiple reap attempts per
victim are the designed behavior. The entry explicitly tags this `[INFERENCE]` (line 50), so it is
presented as a consequence, not an observed fact.

Verdict: **holds** (as an inference; consistent with the committed code).

## Claim 5 — "the printed line for mark_victim reads total-vm=…kB anon-rss=…kB file-rss:…kB shmem-rss:…kB … two different separators (= and :)"

Evidence: `include_trace_events_oom.h` line 105 (the `TP_printk` for `mark_victim`), verbatim:
```
TP_printk("pid=%d comm=%s total-vm=%lukB anon-rss=%lukB file-rss:%lukB shmem-rss:%lukB uid=%u pgtables=%lukB oom_score_adj=%hd",
```
`total-vm=` / `anon-rss=` use `=`; `file-rss:` / `shmem-rss:` use `:` — exactly the mixed
separators claimed, and the field names contain hyphens. Header line 105 cited by the entry is
correct.

Verdict: **holds**.

## Supporting citations spot-checked (prose line numbers in the sources)

- Header: eight `TRACE_EVENT(` lines at 12, 34, 76, 118, 134, 150, 166, 183 — exactly as the
  entry claims (lines 16–18); `grep -c '^TRACE_EVENT('` → 8.
- `fs_proc_base.c:1158` `trace_oom_score_adj_update(task)` inside `__set_oom_adj` (starts 1106) ✓.
- `mm_page_alloc.c:4265` `trace_compact_retry(…)` inside `should_compact_retry` (starts 4202, the
  CONFIG_COMPACTION variant) ✓; `mm_page_alloc.c:4630` `trace_reclaim_retry_zone(…)` inside
  `should_reclaim_retry` (starts 4581) ✓.
- `mm_oom_kill.c`: 774 `trace_mark_victim(tsk, cred->uid.val)` in `mark_oom_victim` (751) ✓;
  673 `trace_wake_reaper(tsk->pid)` after the `MMF_OOM_SKIP` early return (663–667) ✓;
  582/595 start/finish and 567/578 skip in `oom_reap_task_mm` (562–599) ✓.

## Verdict

All five attacked prose claims **hold**; none break, none overreach their stated scope. The single
scope sensitivity is claim 1: the sentence is correct because it defines identity as the victim's
pid+comm+uid, and the entry's own table discloses that `oom_score_adj_update` also carries pid+comm
(writer, no uid). No correction required. The counter's `C2=met` at T is consistent with the
prose-level checks.
