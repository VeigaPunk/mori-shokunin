# Mo50bCritStagedClaims — attack on the C2 assimilation (staged r46/r47) and on the landed entry's forbidden claims

Seat: leaf critic. Round 50 attempt 2, wave a2w1. Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Reviewed at the attempt-2 landed data rev `487941b9395e89678af0053cc443cdb49cdee6e3`; working tree equals it for every
file I cite (`git show 487941b…:corpus/knowledge/oom-memcg-stat-r50.md | sha256sum` =
`0fac741cce21d76eda26b9b0a915509e34be499b52041cb7e6c3b1c8cb97c109` = `sha256sum corpus/knowledge/oom-memcg-stat-r50.md`;
`git status --porcelain corpus/knowledge/oom-memcg-stat-r50.md corpus/SOURCES.md corpus/evidence/sources-r50/` empty).
Line numbers are 1-based on those bytes.

Nothing was installed or upgraded (no pacman, no uv, no npx); no clone, no fixture; scratch
`/fast/scratch/hyaku/mori-r50/Mo50bCritStagedClaims/` was created and removed (`mkdir -p` → `ls -d` → `rm -rf`;
`scratch_removed=yes`). `disk-guard.sh status` before the run: rc 0, `/fast/scratch/hyaku` 23 % used, 618.4 G free.
No kernel log was read or grepped (lane rule S351 / QUALITY 15); no cgroup limit was created or changed; the
`/sys/fs/cgroup` reads in §1.3 are read-only `cat`/`grep` of one user-session slice and are labelled CORROBORATION
(host `7.2.11-arch1-1`), never as frozen-set evidence. No credential material and no private URL is reproduced; the
terminal scope handle is abbreviated `<scope>`.

Counter/predicate/control/kill-rule changes proposed: **none**. Everything below is (a) staged-entry verdict input,
or (b) landed data the L1 may correct. The frozen counter still prints `C2=met …`; no finding here is a counter
defect.

---

## 1. The three questions, answered from the frozen copies

### 1.1 Is tmpfs counted in `file` **and** in `shmem`? — YES, and the two are not two charges

Doc (S489, `corpus/evidence/sources-r50/cgroup-v2.7.2.html`), inside the `memory.stat` `<dl>` (line 1393):

```
1412| <dt>file</dt><dd><p>Amount of memory used to cache filesystem data,
1413| including tmpfs and shared memory.</p>
1434| <dt>shmem</dt><dd><p>Amount of cached filesystem data that is swap-backed,
1435| such as tmpfs, shm segments, shared anonymous mmap()s</p>
1458| <dt>file_thp</dt><dd><p>Amount of cached filesystem data backed by transparent
1461| <dt>shmem_thp</dt><dd><p>Amount of shm, tmpfs, shared anonymous mmap()s backed by
```

Code (S490, `corpus/evidence/sources-r50/memcontrol.c.v7.2`), the formatter's key table:

```
1547|	{ "anon",			NR_ANON_MAPPED			},
1548|	{ "file",			NR_FILE_PAGES			},
1549|	{ "kernel",			MEMCG_KMEM			},
1550|	{ "kernel_stack",		NR_KERNEL_STACK_KB		},
1551|	{ "pagetables",			NR_PAGETABLE			},
1553|	{ "percpu",			MEMCG_PERCPU_B			},
1554|	{ "sock",			MEMCG_SOCK			},
1555|	{ "vmalloc",			NR_VMALLOC			},
1556|	{ "shmem",			NR_SHMEM			},
...
1723|			seq_buf_printf(s, "slab %llu\n", size);
```

Answer: both keys exist and both are populated by page-cache-type pages (1548, 1556; the doc says so twice at
1412–1413 and again, as superset/subset, at 1458 vs 1461). The distinction that matters is **classification, not
charge**: the scope's charge is one number (`memory.current`), and `file`/`shmem` are two overlapping views of it.
Therefore:

- r46's sentence "Because tmpfs is charged as `file`" (`scope-charge-fields-r46.md:25`) is true but narrow — the same
  pages are also counted under `shmem` (1434–1435), so a reader who checks only `file` cannot tell tmpfs from ordinary
  page cache, and a reader who adds the two double counts. r46 never says "add", so this is incompleteness, not error.
- The landed entry has it right: row 3 (`oom-memcg-stat-r50.md:23`) states the doc's `file` fact, and reading rule
  lines 52–53 says "`shmem` is the swap-backed subset inside `file` … Do not add `file` and `shmem`."
- UNVERIFIED in the frozen set: no frozen file shows a tmpfs page incrementing **both** `NR_FILE_PAGES` and
  `NR_SHMEM` (that increment lives in `mm/shmem.c`, which was not frozen this round). The subset relation is
  doc-derived. That is a limit of the frozen evidence, not a defect in the entry.

### 1.2 Does the victim line's `shmem-rss` count tmpfs pages the victim did not map? — NO

S491, `corpus/evidence/sources-r50/oom_kill.c.v7.2`:

```
945|	pr_err("%s: Killed process %d (%s) total-vm:%lukB, anon-rss:%lukB, file-rss:%lukB, shmem-rss:%lukB, UID:%u pgtables:%lukB oom_score_adj:%d\n",
947|		K(get_mm_counter_sum(mm, MM_ANONPAGES)),
948|		K(get_mm_counter_sum(mm, MM_FILEPAGES)),
949|		K(get_mm_counter_sum(mm, MM_SHMEMPAGES)),
```

`mm` here is `victim->mm` (`oom_kill.c.v7.2:931`). The same three counters feed the `Tasks state` table (403–405, header at 424–425
`rss_anon rss_file rss_shmem`). What those counters are (host header, CORROBORATION, `7.2.11-arch1-1`,
`include/linux/mm.h`, no frozen counterpart):

```
3349| static inline unsigned long get_mm_counter_sum(struct mm_struct *mm, int member)
3351|	return percpu_counter_sum_positive(&mm->rss_stat[member]);
3399| static inline unsigned long get_mm_rss_sum(struct mm_struct *mm)
3401|	return get_mm_counter_sum(mm, MM_FILEPAGES) +
3402|		get_mm_counter_sum(mm, MM_ANONPAGES) +
3403|		get_mm_counter_sum(mm, MM_SHMEMPAGES);
```

So the victim line reports an **mm's RSS buckets** — pages resident in that mm's own mappings — never the cgroup's
charge. A tmpfs page charged to the cgroup but mapped into nobody (or into another process) appears in the block's
`file`/`shmem`, and can never appear in the victim's `shmem-rss`. Three consequences:

- r46's "the victim's own `anon-rss` would never show it" (`:26-27`) is true and understated: *no* victim-line field
  shows it unless the victim itself maps the pages.
- r46's "without the victim process growing at all" (`:26`) is false in the mapped case: if the victim mmaps the
  tmpfs file (or its own writes land in a shared mapping), `shmem-rss` and `pgtables` grow, and the victim line does
  show the pages. The claim needs the qualifier "when the victim does not map them".
- Reading a group kill's victim lines as "the cgroup's composition, per process" is also wrong for the same reason:
  the block is the cgroup (see 1.3), the victim lines are per-mm RSS.

### 1.3 Does `anon` in the memcg block cover every task in the cgroup? — yes, and *more*: it is subtree-aggregated

The formatter and the counter it reads (S490):

```
1707|	mem_cgroup_flush_stats(memcg);
1717|		size = memcg_page_state_output(memcg, memory_stats[i].idx);
1669|	return memcg_page_state(memcg, item) *
 757| unsigned long memcg_page_state(struct mem_cgroup *memcg, int idx)
 765|	x = READ_ONCE(memcg->vmstats->state[i]);
 629|	/* Aggregated (CPU and subtree) page state & events */
 633|	/* Non-hierarchical (CPU aggregated) page state & events */
 894|	x = READ_ONCE(memcg->vmstats->state_local[i]);       /* memcg_page_state_local */
 721| * mem_cgroup_flush_stats - flush the stats of a memory cgroup subtree
 684|	for (; statc_pcpu; statc_pcpu = statc->parent_pcpu) {   /* update walks ancestors */
```

`memcg_page_state` reads the `state[]` array the struct comment labels "Aggregated (CPU and subtree)" (629), while
the local variant reads `state_local[]` (894, comment 633). The block therefore prints the cgroup's **and its
descendants'** counters. Who is charged at all is decided by the charge path:

```
5137| int __mem_cgroup_charge(struct folio *folio, struct mm_struct *mm, gfp_t gfp)
5142|	memcg = get_mem_cgroup_from_mm(mm);
1142|		memcg = mem_cgroup_from_task(rcu_dereference(mm->owner));
```

i.e. the charge goes to the memcg of the **mm owner** at charge time (or to `active_memcg` / `current->mm` / root when
`mm` is NULL, 1128–1138). Answer, precisely: `anon` (like every key) covers every charge attributed to that memcg and
its subtree — every task in the cgroup and in any descendant cgroup at the moment of the fault — not "the cgroup's
own tasks only" and not "the tasks in it now". [INFERENCE] a page charged while its owner was in another cgroup stays
on that other cgroup's counter; nothing in the frozen copies shows migration.

CORROBORATION (host, read-only; not frozen-set evidence). `user.slice` holds **0** processes directly
(`cat …/user.slice/cgroup.procs | wc -l` → `0`) yet reports the child's numbers:

```
user.slice          memory.current 21295431680
                    anon  7541837824   file 10708361216   kernel 2988158976   sock 311296
user-1000.slice     memory.current 21296144384
                    anon  7531470848   file 10725994496   kernel 2971000832
```

A local-only `memory.stat` on `user.slice` would be ~0; it is 21.2 GB ≈ the child's total. Subtree aggregation holds
on this host's 7.2.11. (The child's `current` exceeding the parent's by 0.7 MB is a read-order race; no conclusion is
drawn from that delta.)

---

## 2. Counterexamples against the staged entries

### 2.1 r46 (`/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/scope-charge-fields-r46.md`)

**CX-1 — the block carries the composition; "none of the breakdown" is false.** `mem_cgroup_print_oom_meminfo`
prints the usage line and then the full `memory.stat` body in one function, with no branch or rate limit between:

```
1791| void mem_cgroup_print_oom_meminfo(struct mem_cgroup *memcg)
1805|	pr_info("memory: usage %llukB, limit %llukB, failcnt %lu\n",
1824|	pr_info("Memory cgroup stats for ");
1827|	seq_buf_init(&s, buf, SEQ_BUF_SIZE); memory_stat_format(memcg, &s);
1829|	seq_buf_do_printk(&s, KERN_INFO);
```

Against r46 `:29-35` ("carries **none** of the breakdown … not in the journal at all") and `:39-41` ("never the
composition") and `:45-47` ("The kernel's record cannot separate the scope's `file` bucket from its `anon` bucket").
(This overlaps `Mo50bScoutStagedCharge.md` finding 1; my addition is CX-2, which the scout did not make.)

**CX-2 — "no `memory.current`, no `memory.max`" is refuted by the usage line itself.** `memory.current` *is*
`page_counter_read(&memcg->memory)` scaled by the page size, and the OOM printer prints exactly that counter as kB;
the `limit` field is `memcg->memory.max`:

```
4623| static u64 memory_current_read(struct cgroup_subsys_state *css,
4628|	return (u64)page_counter_read(&memcg->memory) * PAGE_SIZE;
1806|		K((u64)page_counter_read(&memcg->memory)),
1807|		K((u64)READ_ONCE(memcg->memory.max)), memory_failcnt);
```

So r46's sweep saw the total and the limit and reported them absent "under their file names": the block carries
`memory.current` and `memory.max` as `usage` and `limit` in kB. The only way to hold the usage line and lose the stats
body is a `SEQ_BUF_SIZE` overflow (`1757-1758`, warning only) or a capture/log loss; the `__ratelimit` guard wraps
`dump_header` and `dump_oom_victim` together (`oom_kill.c:1030-1033`), so it can drop block *and* summary while the
unguarded `Killed process` line survives — the asymmetry the landed entry states at lines 70-72, not the reverse.

**CX-3 — "a child … consumes the scope's cap" is conditional, not general.** The charge follows the charging mm's
owner memcg (1.3: 5142, 1142). A child placed in the runner's own cgroup — or in any cgroup that is neither the scope
nor a descendant — charges *that* cgroup; the scope's `memory.max` is untouched and the scope's block stays at
`file 0`. r46 `:24-27` states the mechanism without the precondition, which is exactly the case where r47-style
`file 0` evidence would *not* refute it.

**CX-4 — "without the victim process growing at all" fails when the victim maps the pages** (1.2). r46 `:25-27`.

Verdict on r46: refuse as written (the contract already refuses it); the tmpfs-→-`shmem`-as-well part (`:25`) and the
missing precondition and qualifier are the three edits a future adoption would need. Nothing of r46's central
negative survives — the landed entry states the opposite (`oom-memcg-stat-r50.md:11-12,31-32`) and is right to.

### 2.2 r47 (`…/scope-composition-in-the-block-r47.md`)

**CY-1 — its five-field list cannot be a whole block.** The formatter's table
(`corpus/evidence/sources-r50/memcontrol.c.v7.2:1546-1609`) declares 20 unconditional keys plus the derived `slab`
line, then the event counters; r47 `:19-20` lists `anon, file, shmem, kernel_stack, slab` only. Either the block was truncated
(`1757-1758`) or the sweep filtered lines. In both cases a byte comparison against the usage line ("the roughly
1.3 MiB that the usage line does not itemise") is not established.

**CY-2 — "kernel memory is 386 248 bytes" is not the `kernel` key.** It is `kernel_stack 131072 + slab 255176`
(r47 `:26`), while the block's `kernel` key is `MEMCG_KMEM` (1549), and `pagetables` / `percpu` / `sock` are separate
keys (1551, 1553, 1554) that the residual attribution at `:35-36` calls "not itemised". Internal inconsistency; if
those keys were absent from the captured block, that is CY-1 again. (Scout finding 4 covers the arithmetic; CY-2
ties it to the formatter's key table.)

**CY-3 — "refuted, not merely unsupported" is over-scoped.** With subtree aggregation (1.3) r47's `file 0`/`shmem 0`
does refute, for that kill, "tmpfs charge was on *this* scope (or a descendant of it)". It does not refute "tmpfs
pages — charged to some other cgroup, or freed before the kill — contributed to the pressure". The defensible
sentence is the scoped one: *for this kill, this scope's `file` and `shmem` buckets were zero.*

**CY-4 — "the `file` bucket, which is where tmpfs is charged" (`:34`) is incomplete** (1.1): tmpfs also lands in
`shmem`. The conclusion survives because both are zero, but the parenthetical would teach a reader to check only
`file`.

Verdict on r47: its positive observation is the one the landed entry adopts (and the code confirms, CX-1/CX-2); its
arithmetic and its "refuted" are not adoptable. Keeping it out of the corpus is correct.

---

## 3. Landed entry — forbidden-claim audit

Forbidden set = the contract's C2 limits, the r47 refutation, the assimilation rule ("the staged r46 tmpfs hypothesis …
is not adopted as a claim"), and the lane's host rule. Each row is the claim that must **not** appear; "absent" is
checked by reading `corpus/knowledge/oom-memcg-stat-r50.md` in full and grepping the sensitive nouns.

| # | forbidden claim | present? | evidence (entry lines) |
|---|---|---|---|
| F1 | tmpfs (or a child's tmpfs) *was*/is the charge behind a kill | absent | `grep -n tmpfs` → lines 23, 24, 52-53 only, all key definitions |
| F2 | a child can hit the cap without the victim growing (r46 mechanism as general fact) | absent | `grep -n child` → no match, rc 1 |
| F3 | `file` and `shmem` are disjoint / additive | absent, and denied | line 53 "Do not add `file` and `shmem`" |
| F4 | the journal block lacks the composition (`memory.stat`/current/max) | absent, and denied | lines 11-12, 31-32 |
| F5 | the block's charge is the victim's own memory | absent, and denied | lines 56-58, 61 |
| F6 | cgroup v1 behaves the same | absent, and denied | lines 68-69 |
| F7 | a missing block means the kill was global | absent, and denied | lines 70-72 |
| F8 | the victim line's counters are the cgroup's charge (or vice versa) | absent, and denied | lines 56-57 |
| F9 | any host block / past kill on this host was read | absent, and denied | lines 75-76 |
| F10 | a missing key means zero (CONFIG-conditional keys) | absent, and denied | lines 49-51 |
| F11 | `usage` equals the sum of the block's keys | absent | no summation rule anywhere; line 61 denies what the block cannot tell |

Conclusion: the landed entry makes **none** of the claims it must not make. Every forbidden direction is either
unstated or explicitly closed in Reading rules/Limits/Boundaries. This part of the seat's assignment passes.

Two related soundness checks, for completeness (both supported):

- line 15 "a stats block means the kill was charged to a scope" — sound: the block is printed only on
  `is_memcg_oom(oc)` (`oom_kill.c:465-468`), and the rate-limit escape is covered at lines 70-72.
- line 30 "a second line reports swap usage … on cgroup v2" — sound: `if (cgroup_subsys_on_dfl(…)) pr_info("swap: …")`
  at `memcontrol.c:1808-1812`, v1's `memory+swap`/`kmem` lines under `CONFIG_MEMCG_V1` at `1813-1821`.
- line 29 failcnt claim — sound (`1801-1803`), exactly as quoted.

---

## 4. Defects found in the landed entry (correctable data, not counter issues)

### D1 — MED — the block is subtree-aggregated, and the entry never says so

`oom-memcg-stat-r50.md:56` says "The block is the cgroup's charge, not the victim's." True, but for FR1 attribution
the missing half is that the block is the cgroup **and its descendants** (629 vs 633, 765 vs 894, 1717, 1707;
corroborated live in 1.3). Without it, a reader can take a nonzero `anon` as evidence about the cgroup's *own* tasks,
when a descendant cgroup's tasks can hold all of it — the same gap the `oom-kill:` path plus `task_memcg` (1774-1782,
NOTE 1767-1768) cannot close. This is the exact fact that also makes r46's "child" case *visible* in the block, so
the assimilation theme is incomplete without it.

Smallest safe correction — add one Reading-rule bullet after line 55:

> The stats block is subtree-aggregated: its keys come from the counter array the struct labels "Aggregated (CPU and
> subtree)" (`memcontrol.c.v7.2:629`, read at `757-765`, formatted at `1717`), so `anon` covers the cgroup's tasks and
> its descendants' charge at fault time (`5137-5147`, `1142`) and cannot say which of them held it.

Integration note: `corpus/SOURCES.md:269` (S490) currently declares `mm/memcontrol.c:1546-1608,1693-1748,1751,1770,
1787-1830,4905-4919`. The anchors above (629-641, 757-771, 1137-1148, 5137-5147) are outside that cell, so the L1
should extend the cell when adding the bullet (sha256, URL, mined date, used-by unchanged; the C2 counter does not read
the lines cell).

### D2 — LOW — row 1's "block" support is a different doc sentence than the quoted one

Row 1 (`:21`) says "Every memory amount the block prints is a byte count" and quotes the **Memory Interface Files**
preamble (HTML 1192-1196). The support for "the block" is the `memory.stat` entry's own sentence
`All memory amounts are in bytes.` (HTML 1397, inside the `memory.stat` `<dd>` at 1393). The claim is supported; the
quote is a sibling sentence. Not a defect, but if the L1 adopts `Mo50bRevRowsCgroupA.md`'s replacement cell, keep the
noun bound to the *stats* block: the burst's other lines print kB and pages (entry lines 46-48), so a bare "the block"
read as the whole burst would be false.

### D3 — LOW — "one victim line per killed mm" (line 60) is not what the code does

Group kill: the iteration is per **process** (`css_task_iter_start(…, CSS_TASK_ITER_PROCS, …)`,
`memcontrol.c:1374`) and each member goes through `__oom_kill_process` (`oom_kill.c:998-1005`), so lines are per killed
process, and two processes can share one mm and still each get a line. Single kill: processes sharing `victim->mm` are
`SIGKILL`ed in the loop at `oom_kill.c:960-985` with **no** `Killed process` line. So the line count is not a count of
killed processes either. Safe wording: "one victim line per task the killer selects; processes sharing the victim's mm
are killed with no line, so a `Killed process` count is neither the number of killed processes nor a per-mm count".

### D4 — LOW — row 15 claim says the group-kill line names "every task"

The line prints `pr_info("Tasks in "); pr_cont_cgroup_path(memcg->css.cgroup); pr_cont(" are going to be killed …")`
(`memcontrol.c:1996-1998`): it names the **cgroup path**, not the tasks. The claim would be exact as "…declares every
task in the named cgroup about to be killed".

### D5 — LOW — "shmem is the swap-backed subset inside `file`" (line 52-53) is doc-only in this evidence set

Consistent with 1548/1556 and with the doc's 1412-1413 vs 1434-1435 (and the 1458/1461 pair), but no frozen line shows
a tmpfs page incrementing both counters (`mm/shmem.c` unfrozen). No change needed; if the L1 wants the relation
code-backed, that needs a fourth source, not a reword.

None of D1–D5 changes the C2 counter output, the claims count, quote location, provenance or pins, so none is a
kill-rule trigger; D1 is the one worth landing because it is an attribution gap in the entry's own reading rules.

---

## 5. Regression, duplicate-authority and provenance checks

- **No duplicate authority / hidden regression inside the lane.** `grep -rn "never the composition\|not in the journal
  at all\|only the composition can say\|memory.stat" corpus/knowledge SKILL.md` outside the new entry → no match
  (empty output). No earlier mori entry carries r46's false rule, so the landed entry is the only statement and it is
  the correct one. A wider `grep -rn "memcg block\|Memory cgroup stats for\|memcg OOM" --include=*.md corpus SKILL.md
  LOG.md` finds only the new entry plus four `corpus/SOURCES.md` rows (`:9` S003, `:10` S004, `:268-270` S489-S491).
- **Provenance independently re-derived.** `sha256sum cgroup-v2.7.2.html memcontrol.c.v7.2 oom_kill.c.v7.2` →
  `2d716cb7…bf34`, `8a28e0bc…1fd5e`, `452f1348…756b4e` — identical to the entry's `recheck:` line (`:7`, "all three
  matched the committed copies") and to the digests in `corpus/SOURCES.md:268-270`. Order in the recheck command
  matches S489→S490→S491.
- **Source rows** (`corpus/SOURCES.md:268-270`): each is `mined`, opened `2026-10-26`, names its frozen URL, names its
  copy and digest, and lists `corpus/knowledge/oom-memcg-stat-r50.md` in used-by — matches the counter's
  `source_rows=ok`.
- **Known duplicate-URL authority (acknowledged W04, not a defect):** `corpus/SOURCES.md:9` S003 is the same
  `oom_kill.c` at tag v7.2 and already mines line 945 (the victim record); S491 re-mines 912-951. S004 is the same
  `memcontrol.c` at a master commit. So one byte change in `mm/oom_kill.c:945` would invalidate two rows' scopes at
  once. The contract already records this as a W04 warning; nothing to fix this round.
- **Saturation:** rows 1-7 rest on one document (the interface page), rows 28-42 on two code files. The entry does not
  claim more; the doc half cannot state what the kernel prints, and the entry does not use it that way (the print
  claims all cite S490/S491). No premature-saturation claim is made.

---

## 6. Impacted axes and the smallest safe correction set

| item | axis | effect | smallest safe change |
|---|---|---|---|
| D1 subtree aggregation | depth | reading rule under-specifies FR1 attribution; the block's `anon` can be a descendant's | add the bullet in D1 + extend S490's `lines` cell |
| D2 row 1 scope | depth | citation-scope note only | none (keep "the block" = stats block if A's cell is adopted) |
| D3 victim-line count | depth | one sentence in Reading rules is not the code's behaviour | reword line 59-60 as in D3 |
| D4 row 15 | depth | claim names the wrong object | "…declares every task in the named cgroup…" |
| D5 shmem ⊂ file | depth | doc-only relation | none; record as a limit |
| r46/r47 refusals | depth | staged entries stay out; landed entry already correct | none (contract's decision stands) |

Calibration, coverage, freshness, operability and adjacency are untouched: nothing here changes `SCORECARD.md` cells,
`SHONEN.md` pins, the instruments' tallies, the settling logic or FR1's adjacency, and the C2 counter still prints
`C2=met … claims=22 located=22 … sources=3 source_rows=ok pins=ok provenance=ok`.

---

## 7. UNVERIFIED / named limits of this review

- No frozen copy contains `mm/shmem.c`, so "a tmpfs page increments both `NR_FILE_PAGES` and `NR_SHMEM`" is doc-derived
  (1412-1413, 1434-1435) and consistent with the key table (1548, 1556), but not shown by code in this evidence set.
- `MM_SHMEMPAGES`' increment site (`mm/rmap.c` or `mm/memory.c`) is likewise not in the frozen set; the per-mm RSS
  characterisation rests on `get_mm_counter_sum` → `mm->rss_stat[]` (host header 3349-3352, CORROBORATION) and on
  `get_mm_rss_sum = file+anon+shmem` (3399-3403).
- The subtree-aggregation corroboration (§1.3) is one host slice at one instant on `7.2.11-arch1-1`, not the frozen
  v7.2 copies, and `memory.current`/`memory.stat` were read at different instants (child and parent `current` differ by
  0.7 MB in read order). No conclusion is drawn from that delta.
- Nothing here proves entailment. The C2 named limit "a located quote proves the quoted words occur … not that the
  claim cell follows from them" is exactly the space D2/D4 live in; the counter cannot see a claim scoped to the wrong
  noun, nor a reading-rule sentence that contradicts a claims row. Named limit, not a new counter weakness.
- No host OOM block was read (lane rule): the answers in §1 are what the kernel prints, not what any past kill on this
  host printed.

## Findings

1. **MED** — `corpus/knowledge/oom-memcg-stat-r50.md:56` (Reading rules): the OOM stats block is subtree-aggregated
   (`corpus/evidence/sources-r50/memcontrol.c.v7.2:629` "Aggregated (CPU and subtree)", `:765` read, `:1717` formatted,
   `:633`/`:894` the local variant) and the entry never says so, so "`anon` covers every task in the cgroup" is true only
   as "every charge attributed to the cgroup and its descendants at fault time" (`:5137-5147`, `:1142`). Add the bullet
   in §4/D1; extend `corpus/SOURCES.md:269`'s S490 line cell to cover the new anchors.
2. **MED** — `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/scope-charge-fields-r46.md:29-35`
   (and `:39-41`, `:45-47`): "carries none of the breakdown … not in the journal at all" is false against
   `memcontrol.c.v7.2:1805`, `:1824`, `:1827-1829`; the usage line is `memory.current` in kB and its `limit` is
   `memory.max` (`:4623-4628` vs `:1805-1807`). Refuse (contract already does); landed entry lines 11-12, 31-32 are
   correct.
3. **MED** — same staged r46 `:24-27`: "a child that writes into `/tmp` consumes the scope's cap" needs the
   precondition that the child's mm-owner memcg is the scope or a descendant (`memcontrol.c.v7.2:5142`, `:1142`);
   otherwise the charge lands elsewhere and the scope's `file` stays zero. Not adoptable as stated.
4. **MED** — same staged r46 `:26`: "without the victim process growing at all" fails when the victim maps the tmpfs
   pages — the victim line's `shmem-rss` is `get_mm_counter_sum(mm, MM_SHMEMPAGES)`, a per-mm RSS bucket
   (`oom_kill.c.v7.2:945-951`, `:403-405`; host `include/linux/mm.h:3349-3352,3399-3403`). Needs a qualifier.
5. **MED** — `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/scope-composition-in-the-block-r47.md:25-26,35-36`:
   "kernel memory is 386 248 bytes" is `kernel_stack + slab`, not the `kernel`/`MEMCG_KMEM` key
   (`memcontrol.c.v7.2:1549`), and the residual is attributed to keys the formatter prints (`:1551`, `:1553`, `:1554`);
   the five-field list at `:19-20` cannot be a whole block (`:1546-1609`) — truncated (`:1757-1758`) or filtered.
   Arithmetic not adoptable.
6. **LOW** — same staged r47 `:32-34`: "refuted, not merely unsupported" generalises one block at one instant; the
   defensible scope is "for this kill, this scope's `file` and `shmem` were zero" (CM: a charge in another cgroup, or
   freed before the kill, survives).
7. **LOW** — same staged r47 `:34`: "the `file` bucket, which is where tmpfs is charged" is incomplete — tmpfs is also
   counted under `shmem` (`cgroup-v2.7.2.html:1412-1413` vs `:1434-1435`; keys `memcontrol.c.v7.2:1548`, `:1556`).
8. **LOW** — `corpus/knowledge/oom-memcg-stat-r50.md:21` (row 1): "the block prints … bytes" is supported by the
   `memory.stat` dd's own sentence (`cgroup-v2.7.2.html:1397`), not by the quoted interface-files preamble
   (`:1192-1196`). Citation-scope note; keep the noun bound to the stats block if the cell is rewritten.
9. **LOW** — `corpus/knowledge/oom-memcg-stat-r50.md:59-60` (Reading rules): "prints one victim line per killed mm" —
   group kills iterate per process (`memcontrol.c.v7.2:1374`; `oom_kill.c.v7.2:998-1005`) and shared-mm processes are
   killed with no line (`oom_kill.c.v7.2:960-985`).
10. **LOW** — `corpus/knowledge/oom-memcg-stat-r50.md:35` (row 15): "naming every task in the cgroup" — the line names
    the cgroup path (`memcontrol.c.v7.2:1996-1998`), not the tasks.
11. **LOW** — `corpus/SOURCES.md:9` (S003) and `:270` (S491): same `mm/oom_kill.c` at tag v7.2, both scoping line 945;
    one byte change would invalidate two rows. Known W04 warning per the contract; recorded, not fixed.
12. **PASS** — landed-entry forbidden-claim audit §3: none of F1–F11 is present; the entry denies F3–F10 explicitly
    (lines 49-53, 56-58, 61, 68-72, 75-76) and does not import r46's central negative or r47's arithmetic.
13. **PASS** — provenance: the three copy digests re-derived independently match the entry's recheck line and
    `corpus/SOURCES.md:268-270`; source rows are `mined`, `2026-10-26`, URL-named and used-by the entry.
