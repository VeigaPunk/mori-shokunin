# Mo50bRevRowsMemcgB — entailment review, rows 12–15 (S490) of corpus/knowledge/oom-memcg-stat-r50.md

MACHINE_ID: 432d02b544a5459ebbff9c42ec68334d

- Round: mori round 50 (attempt 2), wave a2w1. Leaf reviewer seat: no subagents dispatched (none allowed).
- Reviewed data: `corpus/knowledge/oom-memcg-stat-r50.md` at `487941b9395e89678af0053cc443cdb49cdee6e3`, rows 12–15 of the claims table (all four source cells are S490).
- Verdicts: **row 12 SUPPORTED, row 13 SUPPORTED, row 14 SUPPORTED, row 15 SUPPORTED.** No OVERCLAIM, no WRONG; no replacement claim cells are required.
- Tooling: nothing installed or upgraded (no pacman, no uv, no npm, no binaries); read-only git only (`rev-parse`, `show`); no repo/index/jj mutation; no kernel-log reads; no host state changed.

## Method

Commands (all read-only, exit 0):

1. Identity of the committed copy vs the landed blob:

   ```
   $ A=$(sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r50/memcontrol.c.v7.2 | cut -d' ' -f1)
   $ B=$(git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 487941b9395e89678af0053cc443cdb49cdee6e3:corpus/evidence/sources-r50/memcontrol.c.v7.2 | sha256sum | cut -d' ' -f1)
   worktree=8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e
   landed =8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e
   MATCH
   ```

   The working-tree copy equals the landed blob and equals the sha256 the entry's `recheck:` line pins for S490. All memcontrol.c line numbers below are lines of that copy (6068 lines). The oom_kill.c copy (sha256 `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e`, 1257 lines) and the S489 HTML copy were extracted from the same commit for call-site corroboration.

2. Independent quote-location check (whitespace-collapsed substring of each quote cell against the copy — not the counter's code; 22 data rows parsed from the entry's table):

   ```
   row 12: source=S490 quote_len=85  LOCATED  raw span lines 4913-4915
   row 13: source=S490 quote_len=107 LOCATED  raw span lines 1774-1778
   row 14: source=S490 quote_len=88  LOCATED  raw span lines 1779-1782
   row 15: source=S490 quote_len=127 LOCATED  raw span lines 1996-1998
   ```

3. Source cell sanity: S490 is `corpus/SOURCES.md` line 269 at the landed commit — URL `https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c`, `mined`, opened `2026-10-26`, used-by `corpus/knowledge/oom-memcg-stat-r50.md`. Its mined line-range field is `mm/memcontrol.c:1546-1608,1693-1748,1751,1770,1787-1830,4905-4919` — see Finding F1.

4. Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bRevRowsMemcgB/` (`disk-guard.sh status` before start: `/fast/scratch/hyaku` 24% used, 613.2G free, rc 0). Everything cited is copied into this report; the scratch tree is removed at the end of the seat.

## Row 12 — the memory.stat file and the block share one formatter

- Claim cell: "The memory.stat file is produced by the same memory_stat_format call, so the file and the block write their keys through one formatter."
- Quote cell: `` `seq_buf_init(&s, buf, SEQ_BUF_SIZE); memory_stat_format(memcg, &s); seq_puts(m, buf);` ``
- Quote location: memcontrol.c.v7.2 lines 4913–4915, inside `memory_stat_show` (4905–4918).

Context (lines 4905–4918):

```c
int memory_stat_show(struct seq_file *m, void *v)
{
	struct mem_cgroup *memcg = mem_cgroup_from_seq(m);
	char *buf = kmalloc(SEQ_BUF_SIZE, GFP_KERNEL);
	struct seq_buf s;

	if (!buf)
		return -ENOMEM;
	seq_buf_init(&s, buf, SEQ_BUF_SIZE);
	memory_stat_format(memcg, &s);
	seq_puts(m, buf);
	kfree(buf);
	return 0;
}
```

Registration — the file the claim names: `static struct cftype memory_files[] = {` (5002) carries

```c
	{
		.name = "stat",
		.seq_show = memory_stat_show,
	},
```

(5052–5055), and the table is wired as the default-hierarchy file set: `.dfl_cftypes = memory_files` (5087; the v1 table is a separate `mem_cgroup_legacy_files`, 5089). On the default hierarchy the cgroup core prefixes the controller name, so this is the `memory.stat` file; the S489 committed copy (cgroup-v2.7.2.html) documents `memory.stat` (2 occurrences).

Block side (row 11's quote, same source): `mem_cgroup_print_oom_meminfo` (1791) formats the "Memory cgroup stats for <path>:" block through the same function — `seq_buf_init(&s, buf, SEQ_BUF_SIZE); memory_stat_format(memcg, &s); seq_buf_do_printk(&s, KERN_INFO);` (1827–1829). `memory_stat_format` itself (1751–1756) dispatches by hierarchy (`memcg_stat_format` on the default/v2 hierarchy, `memcg1_stat_format` otherwise), so on the v2 hierarchy this entry scopes to, file and block go through the same inner formatter as well.

**Verdict: SUPPORTED.** The quote plus its context shows the memory controller's `stat` file seq_show producing the file's content through `memory_stat_format`, and the block side goes through the same function (line 1828). "One formatter" is exact at the `memory_stat_format` level.

Phrasing note (Finding F2, no replacement required): "the same memory_stat_format call" is singular, while the source has two call sites of the same function (1828 block, 4914 file); a literal same-call-site reading is impossible (one call cannot produce both a file read and an OOM-time block). The claim's "so" clause ("through one formatter") states the intended, correct content.

## Row 13 — the global_oom else branch

- Claim cell: "When no cgroup is named the OOM context prints global_oom instead of a cgroup path, marking a system-wide kill."
- Quote cell: `` `if (memcg) { pr_cont(",oom_memcg="); pr_cont_cgroup_path(memcg->css.cgroup); } else pr_cont(",global_oom");` ``
- Quote location: memcontrol.c.v7.2 lines 1774–1778, inside `mem_cgroup_print_oom_context` (1770–1784).

Context (lines 1761–1784):

```c
/**
 * mem_cgroup_print_oom_context: Print OOM information relevant to
 * memory controller.
 * @memcg: The memory cgroup that went over limit
 * @p: Task that is going to be killed
 *
 * NOTE: @memcg and @p's mem_cgroup can be different when hierarchy is
 * enabled
 */
void mem_cgroup_print_oom_context(struct mem_cgroup *memcg, struct task_struct *p)
{
	rcu_read_lock();

	if (memcg) {
		pr_cont(",oom_memcg=");
		pr_cont_cgroup_path(memcg->css.cgroup);
	} else
		pr_cont(",global_oom");
	if (p) {
		pr_cont(",task_memcg=");
		pr_cont_cgroup_path(task_cgroup(p, memory_cgrp_id));
	}
	rcu_read_unlock();
}
```

Caller (oom_kill.c.v7.2, `dump_oom_victim` 444–453) — the labels are appended to the one-line oom-kill context:

```c
	pr_info("oom-kill:constraint=%s,nodemask=%*pbl",
			oom_constraint_text[oc->constraint],
			nodemask_pr_args(oc->nodemask));
	cpuset_print_current_mems_allowed();
	mem_cgroup_print_oom_context(oc->memcg, victim);
	pr_cont(",task=%s,pid=%d,uid=%d\n", victim->comm, victim->pid,
		from_kuid(&init_user_ns, task_uid(victim)));
```

The kernel's own split: `static inline bool is_memcg_oom(struct oom_control *oc) { return oc->memcg != NULL; }` (oom_kill.c 72–75); `dump_header` (456–469) prints the memcg stats block when `is_memcg_oom(oc)` and `__show_mem(SHOW_MEM_FILTER_NODES, ...)` otherwise (465–468). And memcontrol.c's own comment on `mem_cgroup_get_oom_group` (1940) says `@oom_domain: memcg in case of memcg OOM, NULL in case of system-wide OOM` — the kernel itself uses "system-wide" for the NULL case.

**Verdict: SUPPORTED.** The else branch fires exactly when there is no memory cgroup that went over limit (doc comment 1764), and it prints `,global_oom` where the if branch prints `,oom_memcg=<path>`. "Marking a system-wide kill" is the kernel's own vocabulary for that condition (memcontrol.c 1940; oom_kill.c 72–75 and 465–468).

Limit note (Finding F3): the label's exact condition is `oc->memcg == NULL`; a cpuset- or nodemask-constrained global OOM also prints `global_oom`, and the `constraint=` field on the same line (oom_kill.c 447 — the entry's row 20) carries that scoping.

## Row 14 — the task_memcg label

- Claim cell: "A second label on the same line records the victim's own memory cgroup path, next to the OOM cgroup path."
- Quote cell: `` `if (p) { pr_cont(",task_memcg="); pr_cont_cgroup_path(task_cgroup(p, memory_cgrp_id)); }` ``
- Quote location: memcontrol.c.v7.2 lines 1779–1782, same function as row 13 (context above).

**Verdict: SUPPORTED.**

- "Second label on the same line": both labels are `pr_cont` continuations; the caller (oom_kill.c 447–453) starts the line with `pr_info("oom-kill:constraint=...")`, appends `oom_memcg=<path>` (or `global_oom`), then `task_memcg=<path>`, and ends the line with `,task=%s,pid=%d,uid=%d\n`. So `task_memcg=` sits on the same line, immediately after the OOM cgroup path.
- "The victim's own memory cgroup path": the doc comment names @p "Task that is going to be killed" (1765) and the caller passes the victim (oom_kill.c 451); `task_cgroup(p, memory_cgrp_id)` is p's memory cgroup.
- "Own" is exactly the distinction the function's NOTE draws: "@memcg and @p's mem_cgroup can be different when hierarchy is enabled" (1767–1768) — which the entry's Reading rules already quote.

## Row 15 — the oom.group announcement

- Claim cell: "A group kill announces itself with its own line naming every task in the cgroup as about to be killed."
- Quote cell: `` `pr_info("Tasks in "); pr_cont_cgroup_path(memcg->css.cgroup); pr_cont(" are going to be killed due to memory.oom.group set\n");` ``
- Quote location: memcontrol.c.v7.2 lines 1996–1998, in `mem_cgroup_print_oom_group` (1994–1999).

Context (lines 1994–1999):

```c
void mem_cgroup_print_oom_group(struct mem_cgroup *memcg)
{
	pr_info("Tasks in ");
	pr_cont_cgroup_path(memcg->css.cgroup);
	pr_cont(" are going to be killed due to memory.oom.group set\n");
}
```

Call site (oom_kill.c.v7.2, `oom_kill_process` 1008; group-kill path 1044–1052):

```c
	/*
	 * If necessary, kill all tasks in the selected memory cgroup.
	 */
	if (oom_group) {
		memcg_memory_event(oom_group, MEMCG_OOM_GROUP_KILL);
		mem_cgroup_print_oom_group(oom_group);
		mem_cgroup_scan_tasks(oom_group, oom_kill_memcg_member,
				      (void *)message);
		mem_cgroup_put(oom_group);
	}
```

**Verdict: SUPPORTED.**

- "Its own line": one `pr_info` message ending in `\n` (1996–1998), separate from the oom-kill: line and the victim line.
- "A group kill announces itself": printed on the group-kill path, inside `if (oom_group)` (oom_kill.c 1047–1052), right after the `MEMCG_OOM_GROUP_KILL` event.
- "Naming every task in the cgroup as about to be killed": the line declares "Tasks in <path> are going to be killed" — the cgroup's task set, declared collectively as about to be killed; the kernel then scans and kills the members (`mem_cgroup_scan_tasks(oom_group, oom_kill_memcg_member, ...)`, oom_kill.c 1050–1051). The named cgroup is the oom_group found by walking up the hierarchy (`mem_cgroup_get_oom_group`, memcontrol.c 1937–1947), which may be an ancestor of the victim's own cgroup; the claim's "the cgroup" covers that.

Limit note (Finding F4): the announcement's wording is broader than the action that follows — `oom_kill_memcg_member` (oom_kill.c 998–1006) kills a member only if `task->signal->oom_score_adj != OOM_SCORE_ADJ_MIN && !is_global_init(task)`. The claim is scoped to what the line announces, so it stands.

## Findings

- **F1 (LOW)** — `corpus/SOURCES.md`, S490 row (line 269 at 487941b): the mined line-range field `mm/memcontrol.c:1546-1608,1693-1748,1751,1770,1787-1830,4905-4919` does not cover the quoted spans of rows 13–15: row 13's quote spans 1774–1778 and row 14's 1779–1782 (only the 1770 signature line is listed for `mem_cgroup_print_oom_context`), and row 15's quote spans 1996–1998 (`mem_cgroup_print_oom_group`, 1994–1999, absent from the list). The C2 counter does not check this field (`source_rows=ok` is about mined/opened/URL/used-by), so this is a description gap, not a counter failure — but a future re-miner following the listed ranges would miss these quotes. Suggested data correction (L1, data only): extend the list, e.g. `1546-1608,1693-1748,1751,1770-1784,1787-1830,1994-1999,4905-4919`.
- **F2 (LOW, optional)** — entry row 12: "the same memory_stat_format call" is singular while the source has two call sites of one function (1828, 4914). The claim is supported as written (the "so" clause fixes the reading), so no replacement is needed. If the L1 wants the reading forced, a floor-keeping replacement is: "The memory.stat file is produced by a call to the same memory_stat_format function, so the file and the block write their keys through one formatter." (≥ 6 words; ≥ 3 words of 3+ letters absent from the quote: file, produced, same, function, block, write, their, keys, through, one, formatter; unique in the table.)
- **F3 (LOW)** — entry row 13: "marking a system-wide kill" is a gloss for the kernel's global OOM. The label's exact condition is `oc->memcg == NULL` (oom_kill.c.v7.2 72–75); cpuset- or nodemask-constrained global OOMs also print `global_oom`, and the `constraint=` field on the same line (oom_kill.c.v7.2 447; the entry's row 20) carries that scoping. Consistent with the source (memcontrol.c 1940 uses the same "system-wide" wording); recorded as a limit, no replacement proposed.
- **F4 (LOW)** — entry row 15: the announcement's wording ("Tasks in <path> are going to be killed") is broader than the member kill that follows, which skips tasks with `oom_score_adj == OOM_SCORE_ADJ_MIN` and global init (oom_kill.c.v7.2 998–1006). The claim is scoped to the announcement, so it stands; recorded as context for readers, no replacement proposed.
- No HIGH or MED findings. All four reviewed rows are SUPPORTED; no claim cell says more than its quote plus context, none is contradicted by the source, and no replacement cells are required.

## Cleanup

- Scratch `/fast/scratch/hyaku/mori-r50/Mo50bRevRowsMemcgB/` removed after this report was written (everything cited is in this report).
- No files outside this report were created or modified; no tooling was installed or upgraded.
