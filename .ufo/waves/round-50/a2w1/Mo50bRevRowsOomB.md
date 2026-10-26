# Mo50bRevRowsOomB — entailment review, claims-table rows 20-22 (S491)

Seat: reviewer (leaf, no subagents). Lane `mori-shokunin`, repo `/home/vgpnk/Projects/shokunin/mori-shokunin`,
fleet root `/home/vgpnk/Projects/shokunin`. MACHINE_ID: MACHINE_ID (32-hex machine id value withheld per lane rule).

Reviewed: rows 20-22 of the claims table of `corpus/knowledge/oom-memcg-stat-r50.md` at the landed data commit
`487941b9395e89678af0053cc443cdb49cdee6e3` (entry read via `git show 487941b…:corpus/knowledge/oom-memcg-stat-r50.md`,
83 lines; working tree untouched). Source under review: the committed copy
`corpus/evidence/sources-r50/oom_kill.c.v7.2` (1257 lines). Scratch
`/fast/scratch/hyaku/mori-r50/Mo50bRevRowsOomB/` (removed at end; every cited line is quoted verbatim below).

## Verdict (answers first)

**All three rows SUPPORTED. No replacement claim cells proposed.** Three LOW findings, all wording/citation-scope
notes, none a defect in what the rows assert:

| row | claim (abridged) | quote at | verdict |
|---|---|---|---|
| 20 | oom-kill context line: constraint + nodemask before victim name/pid/uid | oom_kill.c.v7.2:446-449 | SUPPORTED |
| 21 | vm + memcg kill counters incremented before the signal; count predates the death record | oom_kill.c.v7.2:934-936 | SUPPORTED |
| 22 | Tasks state table: total_vm and rss in pages, unlike kB victim line and byte-valued stats block | oom_kill.c.v7.2:424-425 | SUPPORTED |

## Integrity checks (before judging)

- `scripts/hyaku/disk-guard.sh status` → exit 0, 613.0G free on `/fast/scratch/hyaku`. No ENOSPC risk.
- Committed copies equal the landed blobs and the entry's pinned recheck hashes (sha256, working tree vs
  `git show 487941b…`):
  - `oom_kill.c.v7.2` = `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` (both) ✓
  - `cgroup-v2.7.2.html` = `2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34` (both) ✓
  - `memcontrol.c.v7.2` = `8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e` (both) ✓
  So every line number below is a line number in the pinned bytes.
- Quote fidelity: each quote cell matches its source region after whitespace-run normalization (python comparison in
  scratch; True/True/True). Row 22's cell collapses the header line's alignment spaces (see Finding F3); tokens identical.

## Row 20 — "The oom-kill context line records the constraint and nodemask before the victim name, pid and uid are appended."

Quote located: `oom_kill.c.v7.2` lines **446-449**, inside `dump_oom_victim` (444-454). Context, 15 lines around
(lines 444-454, verbatim):

```c
static void dump_oom_victim(struct oom_control *oc, struct task_struct *victim)
{
	/* one line summary of the oom killer context. */
	pr_info("oom-kill:constraint=%s,nodemask=%*pbl",
			oom_constraint_text[oc->constraint],
			nodemask_pr_args(oc->nodemask));
	cpuset_print_current_mems_allowed();
	mem_cgroup_print_oom_context(oc->memcg, victim);
	pr_cont(",task=%s,pid=%d,uid=%d\n", victim->comm, victim->pid,
		from_kuid(&init_user_ns, task_uid(victim)));
}
```

**SUPPORTED.**

- Constraint printed first: `oom_constraint_text[oc->constraint]` (448); the array (239-244) holds exactly
  `CONSTRAINT_NONE`, `CONSTRAINT_CPUSET`, `CONSTRAINT_MEMORY_POLICY`, `CONSTRAINT_MEMCG`.
- Nodemask printed second: `nodemask_pr_args(oc->nodemask)` (449).
- Victim name/pid/uid appended afterwards on the **same** line: `pr_cont(",task=%s,pid=%d,uid=%d\n", victim->comm,
  victim->pid, from_kuid(&init_user_ns, task_uid(victim)))` (452-453); the `\n` is at the end of the `pr_cont`, so
  "the oom-kill context line" (singular) is the right granularity — the comment at 446 itself calls it "one line
  summary of the oom killer context".
- The claim says "before … are appended", not "immediately before": `cpuset_print_current_mems_allowed()` (450) and
  the `oom_memcg=`/`task_memcg=` labels from `mem_cgroup_print_oom_context` (451, row 14's subject) sit between.
  The claim does not deny them; the ordering it asserts is exactly the code order. `dump_oom_victim` is the only
  printer of `oom-kill:constraint=` in the file (grep: one `pr_info` at 447).

## Row 21 — "The vm and memcg kill counters are incremented before the signal is sent, so the count predates the victim's death record."

Quote located: `oom_kill.c.v7.2` lines **934-936**, inside `__oom_kill_process` (912-…). Context, 15 lines around
(lines 930-945, verbatim):

```c
	/* Get a reference to safely compare mm after task_unlock(victim) */
	mm = victim->mm;
	mmgrab(mm);

	/* Raise event before sending signal: task reaper must see this */
	count_vm_event(OOM_KILL);
	memcg_memory_event_mm(mm, MEMCG_OOM_KILL);

	/*
	 * We should send SIGKILL before granting access to memory reserves
	 * in order to prevent the OOM victim from depleting the memory
	 * reserves from the user space under its control.
	 */
	do_send_sig_info(SIGKILL, SEND_SIG_PRIV, victim, PIDTYPE_TGID);
	mark_oom_victim(victim);
	pr_err("%s: Killed process %d (%s) total-vm:%lukB, anon-rss:%lukB, file-rss:%lukB, shmem-rss:%lukB, UID:%u pgtables:%lukB oom_score_adj:%d\n",
```

**SUPPORTED.**

- "The vm and memcg kill counters": `count_vm_event(OOM_KILL)` (935) is the vm event counter;
  `memcg_memory_event_mm(mm, MEMCG_OOM_KILL)` (936) is the memcg event call. Each is the only occurrence of its kind
  in the file (grep: `count_vm_event(OOM_KILL)` → 935 only; `memcg_memory_event_mm` → 936 only).
- "are incremented": verified on the committed memcg event path — `__memcg_memory_event`
  (`memcontrol.c.v7.2:1854-1883`) does `atomic_long_inc(&memcg->memory_events_local[event])` (1863) and
  `atomic_long_inc(&memcg->memory_events[event])` (1868), i.e. a real counter increment, not a notification-only
  path. Caveat in Finding F2: the wrapper `memcg_memory_event_mm` itself is defined outside the three committed
  copies.
- "before the signal is sent": `do_send_sig_info(SIGKILL, SEND_SIG_PRIV, victim, PIDTYPE_TGID)` is at 943; the
  counters at 935-936 precede it, and the source's own comment (934) states both the ordering and its reason
  ("task reaper must see this").
- "so the count predates the victim's death record": the kill record — the `Killed process` `pr_err` line — is
  printed at 945, after the counters (935-936) and after the signal (943); the victim's actual death is asynchronous
  after SIGKILL delivery. Under either reading of "death record" (the `Killed process` log record, or the death
  itself) the count predates it. The ordering asserted is entailed by the code order visible in the context
  (935-936 < 943 < 945). Wording caveat in Finding F2.

## Row 22 — "The Tasks state table prints total_vm and rss in pages, unlike the kB victim line and the byte-valued stats block."

Quote located: `oom_kill.c.v7.2` lines **424-425**, the `dump_tasks` header (function 422-441). Context, 15 lines
around (lines 422-428, verbatim):

```c
static void dump_tasks(struct oom_control *oc)
{
	pr_info("Tasks state (memory values in pages):\n");
	pr_info("[  pid  ]   uid  tgid total_vm      rss rss_anon rss_file rss_shmem pgtables_bytes swapents oom_score_adj name\n");

	if (is_memcg_oom(oc))
		mem_cgroup_scan_tasks(oc->memcg, dump_task, oc);
	else {
```

plus the row printer `dump_task` (379-406; the value line is 400-406, verbatim):

```c
	pr_info("[%7d] %5d %5d %8lu %8lu %8lu %8lu %9lu %8ld %8lu         %5hd %s\n",
		task->pid, from_kuid(&init_user_ns, task_uid(task)),
		task->tgid, task->mm->total_vm, get_mm_rss_sum(task->mm),
		get_mm_counter_sum(task->mm, MM_ANONPAGES), get_mm_counter_sum(task->mm, MM_FILEPAGES),
		get_mm_counter_sum(task->mm, MM_SHMEMPAGES), mm_pgtables_bytes(task->mm),
		get_mm_counter_sum(task->mm, MM_SWAPENTS),
		task->signal->oom_score_adj, task->comm);
```

**SUPPORTED.**

- "total_vm and rss in pages": the header announces "memory values in pages" (424) and lists the `total_vm`/`rss`
  columns (425); `dump_task` prints `task->mm->total_vm` and the mm-counter sums (`get_mm_rss_sum`,
  `get_mm_counter_sum(MM_ANONPAGES/FILEPAGES/SHMEMPAGES)`) raw — no `K()` pages→kB conversion — so the printed
  values are page counts, consistent with the header. (`pgtables_bytes` is bytes even in this table; the claim does
  not touch it, correctly.)
- "unlike the kB victim line": verifiable in the same committed copy — the victim line at 945 prints
  `total-vm:%lukB, anon-rss:%lukB, file-rss:%lukB, shmem-rss:%lukB` (row 16's quote). This half is supported by the
  row's cited source S491, though outside the quoted region (line 945 is ~520 lines from 424).
- "the byte-valued stats block": **not in S491 at all** — the block is formatted/printed by memcontrol.c
  (`memory_stat_format` at `memcontrol.c.v7.2:1751`, printed at 1828-1829) and its byte units are stated by S489
  (`cgroup-v2.7.2.html:1194`: "All memory amounts are in bytes."). This clause rests on rows 1 and 11 of the entry,
  not on this row's quote or context. See Finding F1.
- The claim is accurate against the committed copies and restates the entry's own unit-discipline point (the reading
  rules say the same: "the `Tasks state (memory values in pages)` table prints pages, and the stats block prints
  bytes"). Verdict stays SUPPORTED; no replacement cell proposed. If the L1 wants the row self-contained under S491,
  the minimal cut is "and the byte-valued stats block" (keeping the S491-internal contrast with the kB victim line);
  not required.

## Findings

- **LOW — F1** `corpus/knowledge/oom-memcg-stat-r50.md`, claims-table row 22: the contrast clause "and the
  byte-valued stats block" is supported by S489 (`cgroup-v2.7.2.html:1194`) and S490 (`memcontrol.c.v7.2:1751,
  1828-1829`), not by the row's cited S491 quote or its 15-line context; the "unlike the kB victim line" half is
  supported by S491 itself (`oom_kill.c.v7.2:945`) but outside the quoted region. The claim is true; recorded as a
  citation-scope note. No wording change required.
- **LOW — F2** row 21: "the victim's death record" is not a source term — the source's stated reason for the
  ordering is "task reaper must see this" (`oom_kill.c.v7.2:934`). The nearest referents (`mark_oom_victim` at 944,
  the `Killed process` record at 945) both postdate the counters at 935-936, so the ordering claim holds. Also, the
  wrapper `memcg_memory_event_mm` is defined outside the three committed copies (it lives in
  `include/linux/memcontrol.h`, not among the pinned sources; grep over the committed copies finds only the call
  site at 936); the increment itself is verified in the committed `__memcg_memory_event`
  (`memcontrol.c.v7.2:1863/1868`) and the ordering by the call-site comment plus code order 935-936 < 943 < 945.
  UNVERIFIED against committed bytes: only the wrapper→`__memcg_memory_event` linkage.
- **LOW — F3** row 22 quote cell: collapses the header line's alignment spaces (`[  pid  ]   uid  tgid total_vm
  rss` → `[ pid ] uid tgid total_vm rss`) relative to `oom_kill.c.v7.2:425`; token content identical (normalized
  comparison passed). Informational; the frozen counter's locating is unaffected and was not re-derived here.

No HIGH or MED findings. No replacement claim cells proposed: rows 20, 21, 22 all SUPPORTED.

## Verification summary (commands, outputs, exit codes)

- `mkdir -p /fast/scratch/hyaku/mori-r50/Mo50bRevRowsOomB/tmp` → ok; `TMPDIR` pointed there for the python step.
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → exit 0; `/fast/scratch/hyaku 24% 613.0G free`.
- `git show 487941b9395e89678af0053cc443cdb49cdee6e3:corpus/knowledge/oom-memcg-stat-r50.md` → 83 lines (read-only
  git; no index or worktree mutation). Rows 20-22 are the last three `| … | S491 | …` table rows.
- `sha256sum` of the three committed copies vs `git show 487941b…:<same path> | sha256sum` → identical pairs; equal
  to the entry's `recheck:` pins (values above).
- Quote locations (grep -n on the committed copy): `Tasks state (memory values in pages)` → 424; `one line summary
  of the oom killer context` → 446; `Raise event before sending signal` → 934; `Killed process` → 945;
  `count_vm_event(OOM_KILL)` → 935; `memcg_memory_event_mm` → 936; `do_send_sig_info(SIGKILL` → 943, 983;
  `mark_oom_victim(victim)` → 944, 1022; `oom_constraint_text[` → 239, 448; `static void dump_tasks` → 422;
  `static void dump_oom_victim` → 444; `static int dump_task` → 379; `pr_info("[%7d]` → 400;
  `pr_cont(",task=%s` → 452.
- Context reads (committed copy): 409-439, 431-461, 905-960, 379-408 — each ≥ 15 lines around its quote.
- `memcontrol.c.v7.2`: `__memcg_memory_event` 1854-1883, `atomic_long_inc` at 1863 and 1868; `memory_stat_format`
  1751; OOM meminfo print 1828-1829. `cgroup-v2.7.2.html:1194` "All memory amounts are in bytes."
- Normalized quote-vs-region comparison (python3 in scratch, read-only) → row 20 True, row 21 True, row 22 True.
- No tool installs were needed (stock python3/git/grep suffice); nothing to record under the tooling authorization.
- Scratch removed after this report was written.
