# Mo50bRevRowsOomA — entailment review, entry rows 16–19 (S491, oom_kill.c)

Seat: Mo50bRevRowsOomA (wave a2w1, mori round 50 attempt 2, leaf — no subagents dispatched).
Scope: rows 16–19 of the claims table of `corpus/knowledge/oom-memcg-stat-r50.md` — the four rows whose source cell is S491 — each judged against the committed copy `corpus/evidence/sources-r50/oom_kill.c.v7.2` (1257 lines), reading ≥ 15 lines around each quote.
Machine: MACHINE_ID. Date of review: 2026-10-26.

## Byte identity with the frozen data commit

Working tree HEAD at review time: `4548a34dc8b4072abaa4335c1f54a9efcfcc314a`.

```
$ git rev-parse HEAD
4548a34dc8b4072abaa4335c1f54a9efcfcc314a
$ git diff --stat 487941b9395e89678af0053cc443cdb49cdee6e3 -- corpus/knowledge/oom-memcg-stat-r50.md corpus/evidence/sources-r50/oom_kill.c.v7.2
(no output)
$ echo exit=$?
exit=0
```

Both files are byte-identical to the landed data commit 487941b9395e89678af0053cc443cdb49cdee6e3, so working-tree reads are reads of the frozen data. Only read-only git (`rev-parse`, `diff --stat`) was run; nothing in the lane repo, its jj state or any index was mutated.

Diagnostics note: no `lsp` device is mounted in this seat and no language server answers for these files, so caller/definition checks were done by line-numbered reads and grep over the committed copy (recorded per the fallback rule; grep output below is text evidence, not semantic proof — the semantic chain is cited line by line).

## Row-by-row review

Row numbering counts claim rows 1–22 after the header; rows 16–19 are contiguous and all cite S491.

### Row 16 — "The Killed process line carries total-vm, anon-rss, file-rss and shmem-rss in kB, plus pgtables and oom_score_adj."

Quote location: **line 945** (format string), argument lines **946–951**:

```c
945  pr_err("%s: Killed process %d (%s) total-vm:%lukB, anon-rss:%lukB, file-rss:%lukB, shmem-rss:%lukB, UID:%u pgtables:%lukB oom_score_adj:%d\n",
946  	message, task_pid_nr(victim), victim->comm, K(mm->total_vm),
947  	K(get_mm_counter_sum(mm, MM_ANONPAGES)),
948  	K(get_mm_counter_sum(mm, MM_FILEPAGES)),
949  	K(get_mm_counter_sum(mm, MM_SHMEMPAGES)),
950  	from_kuid(&init_user_ns, task_uid(victim)),
951  	mm_pgtables_bytes(mm) >> 10, victim->signal->oom_score_adj);
```

Context read 928–964 (`__oom_kill_process`, defined at 912): the pr_err sits after `do_send_sig_info(SIGKILL, …)` and `mark_oom_victim(victim)` (943–944), inside `task_lock(victim)`/`task_unlock(victim)`.

**Verdict: SUPPORTED.** Each of `total-vm`, `anon-rss`, `file-rss`, `shmem-rss` is printed with an explicit `%lukB` conversion in the quoted format string; `pgtables:%lukB` and `oom_score_adj:%d` are on the same line, and lines 946–951 bind them to `mm` counters and the victim's signal struct. The claim's "in kB" rests on the format string alone — no appeal to the `K()` macro's definition (which is not in this file; `#define K(` has no match in the committed copy — the kB reading does not need it). The line also carries `UID` (950), which the claim does not enumerate; an incomplete enumeration is not an overclaim.

### Row 17 — "The victim line's message prefix says whether the kill was global or a cgroup kill, choosing between two distinct strings."

Quote location: **lines 1169–1170**, in `out_of_memory()`:

```c
1169		oom_kill_process(oc, !is_memcg_oom(oc) ? "Out of memory" :
1170			 "Memory cgroup out of memory");
```

Context read 1152–1188, plus the branch above it (read 1120–1153). The message chain to the victim line is complete inside this file: `oom_kill_process(struct oom_control *oc, const char *message)` (1008) → `__oom_kill_process(victim, message)` (1042) → `pr_err("%s: Killed process …", message, …)` (945–946). So the chosen string is literally the `%s:` prefix of the row-16 victim line.

The only other message string in the file is `"Out of memory (oom_kill_allocating_task)"` at line 1151, and its branch is guarded at lines 1146–1150 by:

```c
1146	if (!is_memcg_oom(oc) && sysctl_oom_kill_allocating_task &&
1147	    current->mm && !oom_unkillable_task(current) &&
1148	    oom_cpuset_eligible(current, oc) &&
1149	    current->signal->oom_score_adj != OOM_SCORE_ADJ_MIN) {
```

**Verdict: SUPPORTED.** The quoted ternary is the kill path every memcg OOM takes (the allocating-task shortcut at 1146–1152 is excluded for memcg by `!is_memcg_oom(oc)`), so a victim line prefixed `Memory cgroup out of memory` is a cgroup kill and one prefixed `Out of memory…` is a global kill — the discrimination the claim asserts holds for every victim line this file can print.

### Row 18 — "A global OOM prints the system memory summary through __show_mem instead of the memcg stats block."

Quote location: **lines 465–468** (collapsed form of the if/else), inside `dump_header()` (defined 456):

```c
465	if (is_memcg_oom(oc))
466		mem_cgroup_print_oom_meminfo(oc->memcg);
467	else {
468		__show_mem(SHOW_MEM_FILTER_NODES, oc->nodemask, gfp_zone(oc->gfp_mask));
```

Context read 446–488: before the if/else, `dump_header` prints the `invoked oom-killer` line (458–459) and `dump_stack()`; after it, `mem_cgroup_show_protected_memory` and `dump_tasks` run for both branches.

**Verdict: SUPPORTED.** The branches are mutually exclusive: the memcg stats block (`mem_cgroup_print_oom_meminfo`, identified as the memory.stat formatter's print path by the entry's S490 rows) prints only when `is_memcg_oom(oc)`, and the else branch — the global case — calls `__show_mem` instead. Caveat recorded as a limit, not a defect: `__show_mem`'s body lives in mm/show_mem.c, outside the three frozen sources; the phrase "the system memory summary" rests on the call's name, its `SHOW_MEM_FILTER_NODES`/nodemask arguments and the entry's framing, not on a quote from this copy. Nothing in this file contradicts it.

### Row 19 — "The oom-kill summary and stats block are rate-limited while the victim line is not, so a burst of kills can print victims without a block."

Quote location: **lines 1030–1032**, inside `oom_kill_process()` (defined 1008), with the rate-limit state declared at ~1013–1014:

```c
1013	static DEFINE_RATELIMIT_STATE(oom_rs, DEFAULT_RATELIMIT_INTERVAL,
1014				      DEFAULT_RATELIMIT_BURST);
...
1030	if (__ratelimit(&oom_rs)) {
1031		dump_header(oc);
1032		dump_oom_victim(oc, victim);
1033	}
```

Context read 1010–1052 and 446–488. What is inside the guard: `dump_header` (the `invoked oom-killer` summary, `dump_stack`, the row-18 if/else that contains the memcg stats block, plus slab/tasks dumps) and `dump_oom_victim` (444, printing the `oom-kill:constraint=…` context line at 447). What is outside it: `__oom_kill_process(victim, message)` at **line 1042** — the call that reaches the row-16 `Killed process` pr_err (945) — and, in the `memory.oom.group` path, `oom_kill_memcg_member` (997–1006) whose `__oom_kill_process(task, message)` at **line 1003** prints one victim line per group member, invoked from `mem_cgroup_scan_tasks(…)` in the same unguarded tail (1044–1049).

**Verdict: SUPPORTED.** When `__ratelimit` returns 0, execution falls through 1033–1042 and the victim line(s) still print, so a burst can produce `Killed process` lines with no header and no stats block — exactly the claim's consequence, and the same limit the entry's `## Limits` bullet already states. `oom_rs` is function-static, so suppression persists across kills.

## Replacement claim cells

None proposed: all four rows are SUPPORTED. The quote cells correctly locate each claim, and no claim cell says more than its quote plus surrounding lines support.

## Environment and compliance

- Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bRevRowsOomA/` created with `tmp/`; `TMPDIR` pointed there; no fixture or clone was needed (review is line-reading only) and the directory is removed after this report is written.
- Disk guard before the (light) run: `/fast/scratch/hyaku 24% use, 613.3G free`; no ENOSPC.
- Tooling authorization: no tools installed or upgraded (pacman untouched per the host-wide pause).
- Host reads: none beyond the disk-guard status script; no kernel log MESSAGE text read, no cgroup/systemctl/journalctl operation.
- Files written: this report only.

## Findings

- LOW — row 17, `corpus/knowledge/oom-memcg-stat-r50.md` (source `corpus/evidence/sources-r50/oom_kill.c.v7.2` lines 1146–1152): the claim's "choosing between two distinct strings" describes the quoted ternary (1169–1170); a third global-only variant, `"Out of memory (oom_kill_allocating_task)"` (line 1151), exists under `sysctl_oom_kill_allocating_task`. It is excluded for memcg kills by `!is_memcg_oom(oc)` (1146), so the claim's global-vs-cgroup discrimination stays true; if the entry is ever revised, one clause could name the sysctl variant, but no edit is required.
- LOW — row 18, same entry (source lines 465–468): the phrase "system memory summary" characterizes `__show_mem`, whose body is not in any frozen source (it lives in mm/show_mem.c). Supported by the call's name and arguments; recorded so a later round re-checks the phrase if mm/show_mem.c is ever mined.
- LOW — row 19, same entry (source lines 1154–1166): `dump_header(oc)` is also called unguarded in `out_of_memory()`'s `if (!oc->chosen)` bail-out ("Out of memory and no killable processes…", dump_header ≈ line 1159), a path where no victim line follows. This does not contradict the kill-path claim (the quoted guard is the kill path), and it reinforces the entry's existing Limits bullet that a missing stats block is not evidence of a global kill; no edit required.
- INFO (verification gap) — row 16: the `K()` macro used for `total-vm`/`anon-rss`/`file-rss`/`shmem-rss` (lines 946–949) is defined outside this copy (`#define K(` has no match in `oom_kill.c.v7.2`); the claim's "in kB" is carried by the `%lukB` format fields, so nothing in the entry depends on the macro, but its pages→kB semantics are UNVERIFIED against the frozen sources.
