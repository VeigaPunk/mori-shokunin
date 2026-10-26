# Mo50bRevRowsMemcgA — entailment review, rows 8–11 (S490), oom-memcg-stat-r50.md

- Scope: rows 8–11 of the claims table (source S490) of `corpus/knowledge/oom-memcg-stat-r50.md` at 487941b9395e89678af0053cc443cdb49cdee6e3.
- Method: each row's quote located in the committed copy `corpus/evidence/sources-r50/memcontrol.c.v7.2`, read with ≥15 lines of context (single window 1782–1840 covers all four quotes; the enclosing function is `mem_cgroup_print_oom_meminfo`, lines 1791–1830). Judged per row: SUPPORTED / OVERCLAIM / WRONG.
- Integrity: working-tree copy at review time is byte-identical to the landed blob — `git show 487941b:corpus/evidence/sources-r50/memcontrol.c.v7.2 | sha256sum` = `8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e`, identical to the file's sha256 and to the hash the entry's `recheck:` line pins. Everything below is judged against those bytes.
- Auxiliary semantics (`K()`, page_counter `failcnt`, `seq_buf_do_printk`) are defined outside this file; they were confirmed against fresh v7.2-tag fetches quoted in "Auxiliary verification" below. No tool installed; no pacman use; scratch was `/fast/scratch/hyaku/mori-r50/Mo50bRevRowsMemcgA/` (removed after this report was written; cited lines are copied into it above/below). No heavy run, so disk-guard was not needed.

## Shared context (committed copy, lines 1791–1830)

Line numbers are from grep/read on the committed copy; the window 1782–1840 was read, satisfying the ±15-lines rule for every quote (earliest quote at 1800, latest at 1829; the function ends at 1830).

```c
1791: void mem_cgroup_print_oom_meminfo(struct mem_cgroup *memcg)
1792: {
1793: 	/* Use static buffer, for the caller is holding oom_lock. */
1794: 	static char buf[SEQ_BUF_SIZE];
1795: 	struct seq_buf s;
1796: 	unsigned long memory_failcnt;
1797: 
1798: 	lockdep_assert_held(&oom_lock);
1799: 
1800: 	if (cgroup_subsys_on_dfl(memory_cgrp_subsys))
1801: 		memory_failcnt = atomic_long_read(&memcg->memory_events[MEMCG_MAX]);
1802: 	else
1803: 		memory_failcnt = memcg->memory.failcnt;
1804: 
1805: 	pr_info("memory: usage %llukB, limit %llukB, failcnt %lu\n",
1806: 		K((u64)page_counter_read(&memcg->memory)),
1807: 		K((u64)READ_ONCE(memcg->memory.max)), memory_failcnt);
1808: 	if (cgroup_subsys_on_dfl(memory_cgrp_subsys))
1809: 		pr_info("swap: usage %llukB, limit %llukB, failcnt %lu\n",
1810: 			K((u64)page_counter_read(&memcg->swap)),
1811: 			K((u64)READ_ONCE(memcg->swap.max)),
1812: 			atomic_long_read(&memcg->memory_events[MEMCG_SWAP_MAX]));
1813: #ifdef CONFIG_MEMCG_V1
1814: 	else {
1815: 		pr_info("memory+swap: usage %llukB, limit %llukB, failcnt %lu\n",
1816: 			K((u64)page_counter_read(&memcg->memsw)),
1817: 			K((u64)memcg->memsw.max), memcg->memsw.failcnt);
1818: 		pr_info("kmem: usage %llukB, limit %llukB, failcnt %lu\n",
1819: 			K((u64)page_counter_read(&memcg->kmem)),
1820: 			K((u64)memcg->kmem.max), memcg->kmem.failcnt);
1821: 	}
1822: #endif
1823: 
1824: 	pr_info("Memory cgroup stats for ");
1825: 	pr_cont_cgroup_path(memcg->css.cgroup);
1826: 	pr_cont(":");
1827: 	seq_buf_init(&s, buf, SEQ_BUF_SIZE);
1828: 	memory_stat_format(memcg, &s);
1829: 	seq_buf_do_printk(&s, KERN_INFO);
1830: }
```

## Row 8 — "The first usage line prints usage, limit and failcnt in that order, with usage and limit converted to kB."

Quote at line 1805; arguments at 1806–1807.

**SUPPORTED.**

- Order: the format string prints `usage`, `limit`, `failcnt` in that order and the argument list (1806–1807) supplies them in the same order — `page_counter_read(&memcg->memory)`, `memcg->memory.max`, `memory_failcnt`.
- Conversion: usage and limit are wrapped in `K()` while failcnt is a plain `%lu`, exactly matching "usage and limit converted to kB" (and implying failcnt is not). `K(x)` is `((x) << (PAGE_SHIFT-10))` — pages to kB (mm/internal.h at v7.2, line 641; see Auxiliary verification) — consistent with the `%llukB` suffix in the quote.
- "First": within this function the `memory:` line (1805) always precedes every other usage line — the v2 `swap:` line (1809) and, on v1 (`CONFIG_MEMCG_V1`, 1813–1822), the `memory+swap` (1815) and `kmem` (1818) lines. It is the first usage line on either hierarchy.

## Row 9 — "On a cgroup v2 hierarchy the printed failcnt comes from the MEMCG_MAX event counter, not from a per-page charge failure count."

Quote at lines 1800–1803; the value feeds the `memory:` line's failcnt slot at 1807.

**SUPPORTED.**

- `cgroup_subsys_on_dfl(memory_cgrp_subsys)` is the cgroup-v2 (default hierarchy) test; on that path the printed failcnt is `atomic_long_read(&memcg->memory_events[MEMCG_MAX])` (1801), an event counter. The committed S489 copy (`corpus/evidence/sources-r50/cgroup-v2.7.2.html`, `memory.events` → `max`, line ~1377) defines that event: "The number of times the cgroup's memory usage was about to go over the max boundary."
- The negative half: the value is not `memcg->memory.failcnt`, which is what the else branch (1803) shows is the alternative source on a non-default (v1) hierarchy — the page_counter charge-failure counter. The contrast the claim draws is exactly the code's two branches.
- Wording nit (does not affect the v2 assertion, no replacement proposed): "per-page charge failure count" is slightly imprecise for the v1 counter — v7.2 `mm/page_counter.c` increments `failcnt` once per failed charge attempt (line 151, after an `nr_pages`-sized add at line 141), i.e. per failed charge (possibly multi-page), not per page.

## Row 10 — "A second line reports swap usage, limit and failcnt on cgroup v2, so the block carries two usage lines."

Quote at line 1809; guard at 1808; arguments at 1810–1812.

**OVERCLAIM.** The first clause is supported; the tail clause is the defect.

- Supported: the `swap:` line is the second `pr_info` of the function, guarded by `if (cgroup_subsys_on_dfl(memory_cgrp_subsys))` (1808), and reports swap usage, limit and failcnt (`MEMCG_SWAP_MAX`, 1812) on cgroup v2.
- Defect — exact words to cut: **"so the block carries two usage lines"**. The two usage lines are separate `pr_info` calls (1805, 1809) printed *before* the stats block; the block proper is the `memory_stat_format` buffer introduced by the `Memory cgroup stats for <path>:` header (1824–1826) and printed at 1827–1829. Nothing in the source carries the usage lines inside the stats block. The entry's own vocabulary agrees: the intro calls the whole output a "burst" and reserves "block" for the `Memory cgroup stats for <path>:` block; row 11 says "The stats block is filled by memory_stat_format"; Limits says "The block is formatted into a static `SEQ_BUF_SIZE` buffer". Row 10's tail is the only cell that uses "block" for the usage-line section, so under the entry's own terminology the tail is false; the usage lines belong to the meminfo printout of `mem_cgroup_print_oom_meminfo` (1791).

Replacement claim cell (only the tail changes; ≥6 words, ≥3 words of 3+ letters not in the quote — second, reports, swap, usage, limit, failcnt, cgroup, meminfo, printout, carries, lines):

> A second line reports swap usage, limit and failcnt on cgroup v2, so the meminfo printout carries two usage lines.

Minimal alternative (cut the tail clause entirely, still a valid cell):

> A second line reports swap usage, limit and failcnt on cgroup v2.

## Row 11 — "The stats block is filled by memory_stat_format and printed at KERN_INFO, so its lines reach the kernel log like any other message."

Quote at lines 1827–1829.

**SUPPORTED.**

- The block's content is exactly what `memory_stat_format(memcg, &s)` writes into the seq_buf (1828) after `seq_buf_init` (1827); `seq_buf_do_printk(&s, KERN_INFO)` (1829) prints it at KERN_INFO.
- "its lines reach the kernel log like any other message": v7.2 `lib/seq_buf.c` lines 115–133 show `seq_buf_do_printk` walks the buffer line by line and issues a plain `printk("%s%.*s", lvl, ...)` per line at the given level — the block's lines go through printk at KERN_INFO like any other message (see Auxiliary verification). Nothing here conditions or suppresses the print (the rate limit lives at the `dump_header` caller in oom_kill.c, which the entry already covers under Limits).

## Auxiliary verification (outside the committed copies)

The committed copy is `mm/memcontrol.c` only; three semantics it references live in sibling files. Fetched from the same pinned tag (`https://raw.githubusercontent.com/torvalds/linux/v7.2/...`, 2026-10-26, into scratch, now removed; cited lines copied here):

- `mm/internal.h` — sha256 `67945b89d943e98e6f239ea93fa81139b0fd30408c7f927da9fc1c118d7e587f`, line 641:
  ```c
  #define K(x) ((x) << (PAGE_SHIFT-10))
  ```
- `mm/page_counter.c` — sha256 `71c9bfd3611f44b641d8ea77c385aa3d861124f19a61cfe49b12e412cd8a5246`, lines 141–152:
  ```c
  		new = atomic_long_add_return(nr_pages, &c->usage);
  		if (new > c->max) {
  			atomic_long_sub(nr_pages, &c->usage);
  			/*
  			 * This is racy, but we can live with some
  			 * inaccuracy in the failcnt which is only used
  			 * to report stats.
  			 */
  			if (track_failcnt)
  				data_race(c->failcnt++);
  ```
- `lib/seq_buf.c` — sha256 `19ac6b1e91cfdcfed3f1ccca27be001c46540cdd96e4b11dbfdb2a2fd6f64c4c`, lines 115–133:
  ```c
  void seq_buf_do_printk(struct seq_buf *s, const char *lvl)
  {
  	const char *start, *lf;
  
  	if (s->size == 0 || s->len == 0)
  		return;
  
  	start = seq_buf_str(s);
  	while ((lf = strchr(start, '\n'))) {
  		int len = lf - start + 1;
  
  		printk("%s%.*s", lvl, len, start);
  		start = ++lf;
  	}
  
  	/* No trailing LF */
  	if (start < s->buffer + s->len)
  		printk("%s%s\n", lvl, start);
  }
  ```

These fetches only resolve macro/helper semantics; every row judgment above is anchored on the committed copy lines 1791–1830 and, for row 9's event semantics, the committed S489 HTML.

## Findings

- **MED** — `corpus/knowledge/oom-memcg-stat-r50.md`, claims table row 10, tail clause "so the block carries two usage lines": mis-scoped against `corpus/evidence/sources-r50/memcontrol.c.v7.2` — the usage lines are printed at lines 1805 and 1809 before the stats block header (1824–1826); the stats block is only the `memory_stat_format` buffer (1827–1829). Also inconsistent with the entry's own use of "block" (intro, row 11, Limits). OVERCLAIM; cut the clause or adopt the replacement cell proposed above.
- **LOW** — `corpus/knowledge/oom-memcg-stat-r50.md`, claims table row 9, phrase "per-page charge failure count": v7.2 `mm/page_counter.c` counts failed charge attempts (possibly multi-page), not pages; wording nit in the negative half only, the v2 assertion is correct as written. No replacement cell needed.
- Rows 8 and 11: SUPPORTED, no findings.

Residual risk / verification gaps: the three auxiliary semantics were verified against fresh v7.2 fetches, not lane-committed copies (the lane commits only the three cited sources; their hashes are recorded above for recheck). Rows outside 8–11 were not reviewed. The C1/C2 counters were not re-run (out of scope; frozen).
