# ScribeLifecycle — round 47 w1

## Behavior

The committed v7.2 copy `corpus/evidence/sources-r47/mm_oom_kill.c` contains these lifecycle trace calls. Line numbers below are the copy's line numbers (1-based).

| Tracepoint | Enclosing function | Line | What the code shows |
|---|---|---:|---|
| `trace_mark_victim` | `mark_oom_victim` | 774 | After setting the victim thread flag, associating `oom_mm`, thawing the task, and incrementing `oom_victims`, the function gets credentials and calls the tracepoint with the task and UID. |
| `trace_wake_reaper` | `wake_oom_reaper` | 673 | After adding the task to `oom_reaper_list` and releasing the spinlock, the timer callback traces the PID, then wakes `oom_reaper_wait`. |
| `trace_start_task_reaping` | `oom_reap_task_mm` | 582 | Called after acquiring `mmap_read_lock` successfully and checking that `MMF_OOM_SKIP` is not set, before `__oom_reap_task_mm`. |
| `trace_finish_task_reaping` | `oom_reap_task_mm` | 595 | Called at `out_finish`, after `__oom_reap_task_mm`; both its success and partial-reap path reach this label. |
| `trace_skip_task_reaping` | `oom_reap_task_mm` | 567, 578 | Called and returned immediately if the read trylock fails; otherwise called when `MMF_OOM_SKIP` is set, before unlocking and returning. |

### Code excerpts (≤25 quoted code words each)

- `mark_oom_victim`, line 774: `trace_mark_victim(tsk, cred->uid.val);`
- `wake_oom_reaper`, line 673: `trace_wake_reaper(tsk->pid);`
- `oom_reap_task_mm`, line 582: `trace_start_task_reaping(tsk->pid);`
- `oom_reap_task_mm`, line 595: `trace_finish_task_reaping(tsk->pid);`
- `oom_reap_task_mm`, lines 566–568: `if (!mmap_read_trylock(mm)) { trace_skip_task_reaping(tsk->pid); return false; }`
- `oom_reap_task_mm`, lines 577–579: `if (mm_flags_test(MMF_OOM_SKIP, mm)) { trace_skip_task_reaping(tsk->pid); goto out_unlock; }`

### Ordering

In the code, `mark_oom_victim` calls the mark tracepoint at line 774; `queue_oom_reaper` schedules `wake_oom_reaper` using a timer at line 693, and that callback calls the wake tracepoint at 673; the reaper path later calls `oom_reap_task_mm`, where start precedes finish on the normal/partial-reap path, while either of two checks can instead trace skip. **[INFERENCE]** The requested conceptual progression is kill marked → reaper woken → reaping start → finish or skip. These calls reside in separate functions and asynchronous timer/reaper paths; this source does not establish that every victim emits every event or that all emissions for a given task are totally ordered as that single sequence. In particular, skip can occur before start, and has no finish call on those branches.

## Gates

No counter or build/test gate was run; this seat records source observations only.

## Touched surfaces

- Wrote only `.ufo/waves/round-47/w1/ScribeLifecycle.md`.
- Read frozen `.ufo/waves/round-47/contract.md` and `corpus/evidence/sources-r47/mm_oom_kill.c`.

## Out of scope

No production files, host state, lane state/index, or fixture repository was changed. No tools were installed. No subagents were dispatched.

## Findings and limits

The copy supports the function, line, and branch descriptions above. The lifecycle ordering beyond local source order is explicitly marked [INFERENCE]; this report does not claim runtime observations or validate the C2 counter.

Report: .ufo/waves/round-47/w1/ScribeLifecycle.md
