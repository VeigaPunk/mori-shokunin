# Mo50bCritReadingRules — attack on the prose of `## Reading rules` and `## Limits`

Seat: critic, mori round 50 (attempt 2), wave a2w1. Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`,
landed data `487941b9395e89678af0053cc443cdb49cdee6e3`. Target: `corpus/knowledge/oom-memcg-stat-r50.md`,
sections `## Reading rules` and `## Limits` only. No counter, predicate, control or kill rule is questioned
here; no corpus, tool, SKILL/SHONEN/SCORECARD/LOG file was written. This file is the only thing I wrote.

Attack method: for every factual sentence in those two sections, locate the line in the three frozen copies
(`corpus/evidence/sources-r50/memcontrol.c.v7.2`, `oom_kill.c.v7.2`, `cgroup-v2.7.2.html`) that supports,
contradicts, or fails to reach it. Lines are cited as `memcontrol.c:<n>`, `oom_kill.c:<n>`, `doc:<n>` (raw HTML
line of the frozen copy). Where the mechanism lives outside the frozen set (a header, `mm/shmem.c`, `lib/seq_buf.c`)
I fetched the same v7.2 tag to know the truth, but every such citation is marked **outside the frozen set** and is
corroboration only — the entry cannot rest a sentence on it.

Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bCritReadingRules/`, `TMPDIR` set to its `tmp/`; removed at seat end
(see “Scratch and hygiene”).

---

## 0. Provenance check before judging (the Limits provenance sentence)

The entry’s first Limit says the copies are “read from the frozen copies whose sha256 the counter pins”. Observed:

```
$ cd corpus/evidence/sources-r50 && sha256sum *
2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34  cgroup-v2.7.2.html
8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e  memcontrol.c.v7.2
452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e  oom_kill.c.v7.2
```

These are the digests in the entry’s `recheck:` line and in `count-c2.py:42,44,46`. Refetching the three URLs
today and comparing (`curl -fsSL <url> -o up-*; sha256sum up-*; diff -q up-memcontrol.c <copy>`):

```
2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34  up-cgroup.html
8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e  up-memcontrol.c
452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e  up-oom_kill.c
IDENTICAL            (diff -q, exit 0)
```

**Verdict: supported and observed.** The copies are byte-identical to tag `v7.2` today; the counter does pin them
(`count-c2.py:39-46`, digest comparison at `:119`). The same sentence’s tail — “later kernels add or rename keys
and can change the report path” — is a prediction about kernels that are not in the evidence base. **UNVERIFIED**
(only the first half is documented in-copy: `doc:1398-1400` says new entries can show up in the middle).

---

## 1. Verdicts, sentence by sentence — `## Reading rules`

### R1a “Units are per line. The usage and swap lines print kB (`K()` converts from pages) …”

**Verdict: kB supported; the parenthetical is outside the evidence base.**
`memcontrol.c:1805` (`"memory: usage %llukB, limit %llukB, failcnt %lu\n"`) and `:1809` (same for `swap:`), both fed
from `page_counter_read()` (`:1806`, `:1810`). That `page_counter_read()` is in pages is shown in-copy:
`mem_cgroup_margin()` documents its return as “in pages” and computes it from `page_counter_read()`
(`memcontrol.c:1515-1526`, “in pages” at :1515-1516). But `K()` is **not defined anywhere in the three frozen copies**
(`grep -n "define K(" memcontrol.c.v7.2` → no match; likewise `include/linux/memcontrol.h`,
`include/linux/page_counter.h`, which are also not frozen). Upstream `mm/internal.h:641` at tag v7.2 is
`#define K(x) ((x) << (PAGE_SHIFT-10))` — **outside the frozen set**. The fact is therefore true, but the sentence’s
mechanism (“converts from pages”) rests on a file the entry does not cite and the counter does not check.

### R1b “… the `Killed process` fields print kB …”

**Verdict: supported.** `oom_kill.c:945-951`: `total-vm`, `anon-rss`, `file-rss`, `shmem-rss` via `K(...)`, and
`pgtables:%lukB` fed by `mm_pgtables_bytes(mm) >> 10` (i.e. bytes→kB). `UID` and `oom_score_adj` are not memory
values, which the sentence does not claim to cover.

### R1c “… the `Tasks state (memory values in pages)` table prints pages …”

**Verdict: contradicted for one column (and one other column is unitless).**
Header at `oom_kill.c:424-425`; the row is printed at `:401-407`. `total_vm`, `rss`, `rss_anon`, `rss_file`,
`rss_shmem`, `swapents` are page counters (`:402-405`), but the `pgtables_bytes` column is
`mm_pgtables_bytes(task->mm)` passed raw (`:404`) — **bytes**, which the same file confirms by dividing it by
`PAGE_SIZE` before mixing it into a page-based score (`oom_kill.c:228-229`). `oom_score_adj` is a score. So “the
table prints pages” is false for `pgtables_bytes`; the kernel’s own header text is itself imprecise there and the
entry repeats it without qualification.

### R1d “… and the stats block prints bytes”

**Verdict: false as written, true only for memory *amounts*. This is the entry’s largest prose defect.**
`memory_stat_format()` on a v2 hierarchy runs `memcg_stat_format()` (`memcontrol.c:1751-1753`), which prints every
key through `memcg_page_state_output()` (`:1717-1718`). The output unit is chosen per item:

- `memcg_page_state_unit()` (`:1612-1626`): bytes-already keys return `1` (`MEMCG_PERCPU_B`, `MEMCG_ZSWAP_B`,
  `NR_SLAB_RECLAIMABLE_B`, `NR_SLAB_UNRECLAIMABLE_B`), `NR_KERNEL_STACK_KB` returns `SZ_1K`, default `PAGE_SIZE`.
- `memcg_page_state_output_unit()` (`:1628-1665`) then **overrides to `1`** all seven `WORKINGSET_*` keys, all four
  `PGDEMOTE_*`, all four `PGSTEAL_*`, all four `PGSCAN_*`, `PGREFILL`, and (under `CONFIG_NUMA_BALANCING`)
  `PGPROMOTE_SUCCESS`. The function’s own comment says why: *“Workingset state is actually in pages, but we export
  it to userspace as a scalar count of events”* (`:1631-1632`); *“Demotion and promotion activities are exported in
  pages”* (`:1634-1635`).
- The two aggregate lines `pgscan` and `pgsteal` are printed from `memcg_page_state()` with **no** unit
  multiplication (`:1728-1737`) — pages.
- The vm-event lines are raw counters (`:1739-1748`).

So `workingset_refault_anon`, `workingset_refault_file`, `workingset_activate_anon`, `workingset_activate_file`,
`workingset_restore_anon`, `workingset_restore_file`, `workingset_nodereclaim`, `pgdemote_*` (4), `pgsteal_*` (4),
`pgscan_*` (4), `pgrefill`, `pgpromote_success`, `pgscan`, `pgsteal`, and every event key (`pgfault`,
`pgmajfault`, `pswpin`, `pswpout`, …) are **pages or event counts, not bytes** — 21 table keys plus 2 aggregate
lines plus the event block — 43 of roughly 72 printed lines. The doc sentence the entry leans on is
“All memory amounts are in bytes” (`doc:1194-1196`, interface-file preamble; repeated at `doc:1397` for
`memory.stat`) — “amounts”, which the activity counters are not. No charge-amount key (`anon`, `file`, `kernel`,
`kernel_stack`, `pagetables`, `sec_pagetables`, `percpu`, `sock`, `vmalloc`, `shmem`, `slab*`, `inactive_*`,
`active_*`, `unevictable`) is affected; the defect is that the flat rule invites a 4096× unit error on the
activity keys.

### R2 “Read the block by key, not by position: the entries are ordered for humans and a newer kernel can insert a counter in the middle.”

**Verdict: supported on both halves.** `doc:1398-1400` (“The entries are ordered to be human readable, and new
entries can show up in the middle. Don’t rely on items remaining in a fixed position; use the keys…”); the code’s
own ordering rationale is at `memcontrol.c:1701-1703` (“This list is ordered following a combination of these
gradients: 1) generic big picture -> specifics and details 2) reflecting userspace activity -> reflecting kernel
heuristics”).

### R3 “The key set is also compile-time conditional — `zswap`, `zswapped`, `swapcached`, `anon_thp`, `file_thp`, `shmem_thp` and `hugetlb` are printed only under their CONFIG options, so a missing key is not a zero.”

**Verdict: every named key is correctly placed, but the list is presented as the conditional set and is not
complete, and one named key is also runtime-gated.**
`memcontrol.c:1557-1561` (`CONFIG_ZSWAP`: `zswap`, `zswapped`, **`zswap_incomp`**), `:1565-1567` (`CONFIG_SWAP`:
`swapcached`), `:1568-1572` (`CONFIG_TRANSPARENT_HUGEPAGE`: `anon_thp`, `file_thp`, `shmem_thp`),
`:1580-1582` (`CONFIG_HUGETLB_PAGE`: `hugetlb`). Missing from the sentence: `zswap_incomp` (`:1560`, same `#ifdef`
block) and `pgpromote_success` (`,:1606-1608`, `CONFIG_NUMA_BALANCING`), and the seven vm-event keys guarded at
`:1741-1748` (`CONFIG_SWAP`/`CONFIG_ZSWAP`/`CONFIG_TRANSPARENT_HUGEPAGE`/`CONFIG_NUMA_BALANCING`). Also, `hugetlb`
is not only compile-time: `memcg_stat_format()` skips it unless `memcg_accounts_hugetlb()` is true
(`:1713-1715`, reading `CGRP_ROOT_MEMORY_HUGETLB_ACCOUNTING` at `:1682-1685`), so with the config in and cgroup
hugetlb accounting off the key is absent. The conclusion (“a missing key is not a zero”) survives — it is in fact
reinforced.

### R4 “`anon` is anonymous mappings, `file` is page cache including tmpfs and shared memory, and `shmem` is the swap-backed subset inside `file` … Do not add `file` and `shmem`.”

**Verdict: supported by the doc; the subset mechanism is outside the frozen set.**
`doc:1406-1408` (anon), `doc:1411-1413` (“including tmpfs and shared memory”), `doc:1434-1436` (shmem is “cached
filesystem data that is swap-backed, such as tmpfs, shm segments, shared anonymous mmap()s”). In the frozen code
`file` is `NR_FILE_PAGES` and `shmem` is `NR_SHMEM` (`memcontrol.c:1548,1556`); that `NR_SHMEM` is inside
`NR_FILE_PAGES` is not shown by any frozen copy — upstream `mm/shmem.c:883-885` increments both for the same folio
(**outside the frozen set**). “Do not add `file` and `shmem`” is therefore correct but rests on a file the entry
does not cite.

### R5 “`kernel` already contains `kernel_stack`, `pagetables`, `percpu`, `vmalloc` and `slab`, which are also printed on their own lines; summing every key double counts kernel memory.”

**Verdict: doc-supported, code-contradicted. The entry states the document’s composition claim as code fact.**
The doc says exactly this (`doc:1415-1418`: “kernel (npn) Amount of total kernel memory, including (kernel_stack,
pagetables, percpu, vmalloc, slab) in addition to other kernel memory use cases.”). The frozen code does not
compose `kernel` that way: `{ "kernel", MEMCG_KMEM }` (`memcontrol.c:1549`) — `MEMCG_KMEM` is its own counter,
updated by `mod_memcg_state(memcg, MEMCG_KMEM, …)` from object-cgroup charging/releasing (`:175`, `:3047`,
`:3057`, `:3332`, `:5238`, NMI flush path `:4438`), while the five keys are separate per-node stats
(`kernel_stack` `NR_KERNEL_STACK_KB` `:1550`, `pagetables` `NR_PAGETABLE` `:1551`, `percpu` `MEMCG_PERCPU_B`
`:1553`, `vmalloc` `NR_VMALLOC` `:1555`, `slab_reclaimable`/`slab_unreclaimable` `:1578-1579` with the `slab`
aggregate at `:1720-1723`). Nothing in the frozen copies shows `MEMCG_KMEM` containing those five; the “do not
sum” conclusion is the document’s, not the code’s. An operator who subtracts the five from `kernel` to get
“other kernel memory” is doing arithmetic the frozen code does not license.

### R6 “The block is the cgroup’s charge, not the victim’s. … the cgroup over its limit and the victim’s own cgroup are two different labels on the `oom-kill:` line; the source’s NOTE … says they can differ when hierarchy is enabled.”

**Verdict: supported throughout, including the NOTE and the identity of the block’s cgroup.**
`dump_header()` calls `mem_cgroup_print_oom_meminfo(oc->memcg)` for a memcg OOM (`oom_kill.c:465-466`);
`oc->memcg` is `mem_over_limit`, the cgroup whose `page_counter_try_charge()` failed
(`memcontrol.c:2625-2627`, set into `oc` at `:1885-1893`), i.e. the limit holder, not the allocating task’s
cgroup. The block’s numbers are hierarchical: the printed state is the “Aggregated (CPU and subtree)” array
(`memcontrol.c:472-474`). The victim’s own counters are on the `Killed process` line
(`oom_kill.c:945-951`, `get_mm_counter_sum(mm, …)`). The two labels: `dump_oom_victim()` prints
`,oom_memcg=` then `,task_memcg=` (`oom_kill.c:444-454` → `memcontrol.c:1770-1780`), and the NOTE is verbatim at
`memcontrol.c:1767-1768` (“NOTE: @memcg and @p's mem_cgroup can be different when hierarchy is enabled”).

### R7 “A group kill announces itself with `Tasks in <path> are going to be killed due to memory.oom.group set` and then prints one victim line per killed mm; `oom_kill` counts processes while `oom_group_kill` counts group events.”

Three separate claims, one right, two wrong.

**(a) The string.** **Supported**: `mem_cgroup_print_oom_group()` at `memcontrol.c:1994-1999` prints
`"Tasks in "` + path + `" are going to be killed due to memory.oom.group set\n"`.

**(b) “and then prints one victim line …” — order inverted.** **Contradicted.** In `oom_kill_process()` the
selected victim is killed, counted and printed **before** the group announcement: `__oom_kill_process(victim,
message)` at `oom_kill.c:1042` (its `Killed process` at `:945`), then `if (oom_group) { … memcg_memory_event(…,
MEMCG_OOM_GROUP_KILL); mem_cgroup_print_oom_group(oom_group); mem_cgroup_scan_tasks(…) }` at `:1047-1051`. So the
first `Killed process` line of a group kill appears *above* the `Tasks in …` line, which inverts the reading rule
for anyone slicing a burst in log order.

**(c) “one victim line per killed mm” — not guaranteed, in both directions.** **Contradicted.** The line is
printed once per `__oom_kill_process()` call (`oom_kill.c:945`), and:
- every process that merely *shares the victim’s mm* in another thread group is SIGKILLed with **no line and no
  counter** (`oom_kill.c:954-985`; `count_vm_event(OOM_KILL)` happened once at `:935`), so lines < killed
  processes;
- the group scan iterates **processes**, not mms (`CSS_TASK_ITER_PROCS` at `memcontrol.c:1374`), and the selected
  victim lies inside the group’s subtree (`mem_cgroup_get_oom_group()` walks from the victim’s cgroup up to
  `oom_domain` and stops there, `memcontrol.c:1947-1989`; the group is therefore an ancestor-or-self of the
  victim’s cgroup), so the scan can revisit the already-killed victim — `oom_kill_memcg_member()` has no
  already-a-victim guard (`oom_kill.c:998-1005`) and only `find_lock_task_mm()` failing (`:918-924`, “already
  exiting. Skip killing the task”) prevents a second line. Two lines for one mm and duplicate `OOM_KILL`
  increments are therefore possible; one line per mm is not a rule the code guarantees.

**(d) `oom_kill` vs `oom_group_kill`.** **Doc-supported with a code caveat.** `doc:1378-1380` (“The number of
processes belonging to this cgroup killed by any kind of OOM killer”), `doc:1381` (“The number of times a group OOM
has occurred”). Code: `oom_kill` rises once per `__oom_kill_process()` call (`oom_kill.c:935-936`), i.e. per
victim record, not per process actually killed (see (c)); `oom_group_kill` rises once per group kill
(`oom_kill.c:1048`) into `memory.events` (`memcontrol.c:4883-4884`). Both events are charged up the hierarchy
(`__memcg_memory_event()` walks parents, `memcontrol.c:1854-1883`), and the doc says `memory.events` fields are
hierarchical (`doc:1350-1351`) — so “counts processes” is the doc’s wording for a *hierarchical, per-victim*
counter. The entry does not say either counter is hierarchical, which matters for attribution (a rising
`oom_kill` in a parent may come from a descendant).

---

## 2. Verdicts, sentence by sentence — `## Limits`

### L1 “Kernel v7.2 only, read from the frozen copies whose sha256 the counter pins; later kernels add or rename keys and can change the report path.”

**Verdict: first clause verified (§0); the tail is UNVERIFIED** — see §0.

### L2 “cgroup v2 only. On a v1 hierarchy the same function prints `memory+swap` and `kmem` lines and a real per-page failcnt, which cgroup v2 does not have; nothing here carries over to v1.”

**Verdict: the lines and the failcnt split are supported; “per-page” is not.**
`memcontrol.c:1800-1803` chooses `memory_events[MEMCG_MAX]` on v2 and `memcg->memory.failcnt` otherwise — this is
the “real … failcnt, which cgroup v2 does not have” claim, exactly. The v1-only lines are
`memcontrol.c:1813-1822` (`#ifdef CONFIG_MEMCG_V1`, printing `memory+swap:` at `:1815` and `kmem:` at `:1818`,
both kB, both with the page-counter `failcnt`). Two precisions the sentence loses: (i) those lines exist only when
`CONFIG_MEMCG_V1` is compiled; (ii) “per-page failcnt” is a unit characterization of `page_counter.failcnt` that
no frozen copy states — it is a count of failed charge attempts (the page-counter implementation is
**outside the frozen set**). What the copies show is only which field is printed.

### L3 “The summary is rate-limited (`if (__ratelimit(&oom_rs)) { dump_header(oc); dump_oom_victim(oc, victim); }`), but the victim line is printed outside that guard; a burst of kills can leave `Killed process` lines with no block at all, so a missing block is not evidence that the kill was global.”

**Verdict: correct, and this is the sentence I tried hardest to break.** The guard is exactly as quoted
(`oom_kill.c:1012-1013` for the state, `:1030-1032` for the guard). The `Killed process` line is in
`__oom_kill_process()` (`:945`), reached from `:1042` and from the group scan (`:999-1003`, via `:1050-1051`) —
both outside the guard. So a ratelimited interval can print victim lines with no `oom-kill:` context line, no
block and no `Tasks state` table (both are inside `dump_header()`/`dump_oom_victim()`), and the conclusion “a
missing block is not evidence that the kill was global” follows. **Two facts that strengthen it are missing from
the entry:** the `Tasks in …` group announcement is *also* outside the guard (`:1049`), and the `oom-kill:`
context line itself is *inside* it (`:1032`), so in a burst the reader loses the `oom_memcg`/`task_memcg` labels
before losing the victim lines.

### L4 “The block is formatted into a static `SEQ_BUF_SIZE` buffer under `oom_lock`, and an overflow only prints a warning, so a truncated block is possible at event time.”

**Verdict: supported.** `SEQ_BUF_SIZE` = `SZ_4K` (`memcontrol.c:127`); the buffer is `static char buf[SEQ_BUF_SIZE]`
with the comment “Use static buffer, for the caller is holding oom_lock” (`:1793-1794`), and the invariant is
asserted (`lockdep_assert_held(&oom_lock)`, `:1798`). The memcg OOM path holds it: `mem_cgroup_out_of_memory()`
takes `oom_lock` around `out_of_memory()` (`:1897-1910`). Formatting into the buffer at `:1827-1828`; the overflow
warning at `:1757-1758`; printing at `:1829`. Missing precision, not an error: an overflowed buffer is printed only
up to `s->len` (upstream `lib/seq_buf.c:115-133`, **outside the frozen set**), and `seq_buf_printf()` truncates the
string it is writing — so the last line of a truncated block can be a **partial value** of a key (e.g. a prefix of
a larger number), not just a missing key. A detector that parses a truncated block can accept a wrong number.

### L5 “No host block was read. … this entry states what the kernel prints, not what any past kill on this host printed.”

**Verdict: process claim, not checkable from the frozen copies; I did not read journal/MESSAGE text either**
(lane rule QUALITY 15). Nothing in the copies can support or contradict it; I record it as UNVERIFIED by source
and note only that the entry makes no host claim elsewhere in these two sections.

### L6 “A located quote proves the quoted words occur in the committed copy, not that the claim cell follows from them.”

**Verdict: correct as a meta-statement, and this review is an instance of it:** the unit quote for the table
(`doc:1194-1196`) is located but the prose built on it (R1d) is only true of memory *amounts*; the `kernel`
quote (`doc:1415-1418`) is located but the composed fact is not what `memcontrol.c:1549` implements (R5).

---

## 3. Cross-section consistency (inversion check)

The introduction says a stats block *means* the kill was charged to a scope; L3 says a *missing* block does not
mean the kill was global. Those are the two directions of one implication and they do not contradict: one-way
detection (`block ⇒ charged`) plus a stated non-converse. Checked against
`oom_kill.c:465-470` (memcg → `mem_cgroup_print_oom_meminfo`; global → `__show_mem`) and
`memcontrol.c:1772-1778` (`global_oom` only when `memcg == NULL`). No fix needed; recorded so the L1 does not
“repair” one half into disagreement with the other.

---

## 4. Draft corrections (fenced; the L1 integrates, I do not edit the entry)

Smallest safe edits, prose only, all facts traceable to the three copies:

```markdown
- Units are per line. The usage and swap lines print kB (`K()` shifts page counts), the `Killed process` fields
  print kB, the stats block prints bytes for memory amounts but **pages or event counts** for the `workingset_*`,
  `pgdemote_*`, `pgscan_*`, `pgsteal_*`, `pgrefill`, `pgpromote_success`, `pgscan`, `pgsteal` and vm-event lines,
  and the `Tasks state` table prints page counts except its `pgtables_bytes` (bytes) and `oom_score_adj` columns;
  convert before comparing a number from one line with a number from another.
```

```markdown
- Read the block by key, not by position: the entries are ordered for humans and a newer kernel can insert a
  counter in the middle. The key set is also conditional — `zswap`, `zswapped`, `zswap_incomp`, `swapcached`,
  `anon_thp`, `file_thp`, `shmem_thp`, `hugetlb` and `pgpromote_success` are printed only under their CONFIG
  options, `hugetlb` additionally only while cgroup hugetlb accounting is on, and the vm-event keys are gated the
  same way, so a missing key is not a zero.
```

```markdown
- The documentation states that `kernel` already contains `kernel_stack`, `pagetables`, `percpu`, `vmalloc` and
  `slab`, which are also printed on their own lines, so do not add them to `kernel` on the document's account.
  The v7.2 code prints `kernel` from its own counter (`MEMCG_KMEM`), not from those five, so the containment is
  the document's claim and not something the frozen code shows.
```

```markdown
- A group kill announces itself with `Tasks in <path> are going to be killed due to memory.oom.group set`, but the
  selected victim's `Killed process` line is printed *before* that announcement; the announcement then covers one
  line per process the scan reaches in the group's subtree. Processes that only share a killed mm are killed with
  no line, and a re-scanned victim can be printed twice, so count lines as records, not as kills. `oom_kill` rises
  once per victim record and `oom_group_kill` once per group kill; both are charged up the hierarchy.
```

```markdown
- cgroup v2 only. On a v1 hierarchy the same function prints `memory+swap` and `kmem` lines and the page counter's
  own `failcnt`, which cgroup v2 does not have; nothing here carries over to v1.
```

```markdown
- The block is formatted into a static `SEQ_BUF_SIZE` buffer under `oom_lock`, and an overflow only prints a
  warning: the block is printed up to what fit, so it can end mid-key or mid-number and a partial value at the end
  is not a measurement.
```

Optional (gap, not an error) — makes the block-vs-victim rule usable:

```markdown
- The block's numbers are subtree totals of the cgroup whose charge failed, not a per-process split; when the
  limit that failed belongs to an ancestor of the victim's cgroup, the `Tasks state` table (printed with the
  block, pages) is where the per-process rss split is, and the block's `anon` can exceed the victim line's
  `anon-rss` by the whole subtree. The `Tasks in <path>` group announcement can likewise name a descendant of the
  block's path.
```

---

## 5. Named limits of this review

- I attacked prose only. Rows of the claim table were not re-judged here (other seats hold that); where a row’s
  quote underpins a prose sentence I said so (R1d, R5, L6) but did not score the row.
- The counter checks none of these sentences, so a prose error (including a HIGH one) is invisible to
  `count-c2.py`; this report is the only carrier for it.
- Four mechanisms lie outside the frozen set (`K()` in `mm/internal.h:641`, the `NR_SHMEM`⊂`NR_FILE_PAGES`
  charging in `mm/shmem.c:883-885`, `seq_buf_do_printk`/`seq_buf_printf` truncation in `lib/seq_buf.c:115-133`,
  and `page_counter` failcnt semantics): I fetched the same tag to know the truth and marked every one. The entry
  may not rest on them, but the prose is not made false by them either.
- No host observation: I read no journal/MESSAGE text, triggered no OOM, changed no cgroup file.
- I did not test v1 behaviour, other kernels, or `CONFIG_MEMCG_V1=n` builds — there is no such kernel here.
- One degenerate case I could not settle in-copy: whether the selected victim is *always* re-visited in a group
  kill depends on signal-delivery timing (`find_lock_task_mm()` at `oom_kill.c:918`); I report it as possible, not
  as observed, and the “one line per mm” defect stands on the silent mm-sharers case regardless.

---

## 6. Scratch and hygiene

- `mkdir -p /fast/scratch/hyaku/mori-r50/Mo50bCritReadingRules/tmp`;
  `export TMPDIR=/fast/scratch/hyaku/mori-r50/Mo50bCritReadingRules/tmp` on every fetch. No clone was made, so no
  fixture repo and no commit identity existed.
- `scripts/hyaku/disk-guard.sh status` before any fetch: `/fast/scratch/hyaku 24% use, 614.1G free` — no ENOSPC.
- Nothing installed or upgraded (no pacman — host-wide pause respected; no uv/npx/binary install needed). Only
  `curl` fetches of the same v7.2 tag into scratch.
- Read-only on every repo: no git add/commit/stash/checkout/reset/pull/push, no jj command, no writes outside this
  report. `/home/vgpnk/Projects/shokuknow` was not touched.
- Scratch removed: `rm -rf -- /fast/scratch/hyaku/mori-r50/Mo50bCritReadingRules` (verified absent with
  `test -e … ; echo $?` → `1`). Everything I cite from scratch is quoted verbatim above.

---

## Findings

1. **MED — `corpus/knowledge/oom-memcg-stat-r50.md`, `## Reading rules` bullet 1 (“the stats block prints bytes”).**
   False for 21 table keys plus `pgscan`/`pgsteal` plus every vm-event line: `memcontrol.c:1628-1665` overrides the
   output unit to 1 for `workingset_*`, `pgdemote_*`, `pgsteal_*`, `pgscan_*`, `pgrefill`, `pgpromote_success`
   (comment at `:1631-1635` says they are pages/event counts), aggregates at `:1728-1737` are raw pages, events at
   `:1739-1748` are counts. No charge-amount key is affected; the rule must be split by key class (draft §4, first
   block).

2. **MED — same entry, `## Reading rules` bullet 4 (“`kernel` already contains … summing every key double counts”).**
   Doc-supported (`doc:1415-1418`) but contradicted as a code fact: `{ "kernel", MEMCG_KMEM }` at
   `memcontrol.c:1549`, an independent counter updated at `:175`, `:3047`, `:3057`, `:3332`, `:5238`, while the five
   named keys are separate stats at `:1550-1555`, `:1578-1579`. The entry presents the document’s composition claim
   as what the kernel computes.

3. **MED — same entry, `## Reading rules` bullet 6 (“one victim line per killed mm”).**
   `oom_kill.c:954-985` kills mm-sharing processes with no line and no counter (count once at `:935`); the group
   scan is per process (`memcontrol.c:1374`) and can revisit the selected victim because
   `oom_kill_memcg_member()` has no victim guard (`oom_kill.c:998-1005`) and the selected victim is inside the
   group’s subtree (`memcontrol.c:1947-1989`). Both arrows break the “per mm” rule.

4. **LOW — same bullet, ordering.** The selected victim’s `Killed process` line (`oom_kill.c:1042` → `:945`) is
   printed *before* the `Tasks in …` announcement (`:1047-1051`); the entry says the announcement comes first and
   the victim lines follow.

5. **LOW — same entry, `## Reading rules` bullet 1 (“the `Tasks state` table prints pages”).**
   The `pgtables_bytes` column is raw bytes (`oom_kill.c:404`; the file itself divides by `PAGE_SIZE` at
   `:228-229`) and `oom_score_adj` is unitless; the header at `:424` is the kernel’s own imprecision and the entry
   repeats it without qualification.

6. **LOW — same bullet, conditional-key list.** `zswap_incomp` (`memcontrol.c:1560`) and `pgpromote_success`
   (`:1606-1608`) are missing from the list, the vm-event keys are gated the same way (`:1741-1748`), and `hugetlb`
   is runtime-gated as well as compile-time (`:1713-1715`, `:1682-1685`) — “compile-time conditional” understates
   it. The “a missing key is not a zero” conclusion stands.

7. **LOW — same entry, `## Limits` bullet 2 (“a real per-page failcnt”).** What the frozen copies show is which
   field is printed (`memcontrol.c:1800-1803`, `:1817`, `:1820`), not that the failcnt is “per page”; page-counter
   failcnt semantics live outside the frozen set. Replace with “the page counter’s own `failcnt`”.

8. **LOW — same entry, `## Reading rules` bullet 1 (“`K()` converts from pages”).** `K()` is not defined in any
   frozen copy (`grep -n "define K("` → no match); the definition is upstream `mm/internal.h:641`, outside the
   entry’s evidence base. Fact correct, provenance unchecked by the counter.

9. **LOW — same entry, `## Limits` bullet 4 (truncation).** True as far as it goes, but a `SEQ_BUF_SIZE` overflow
   truncates mid-value (`seq_buf_printf`/`seq_buf_do_printk`, outside the frozen set), so the last key of a
   truncated block can carry a plausible partial number; the limit should say so.

10. **LOW — gaps the sections omit (not errors).** The block is a subtree aggregate (`memcontrol.c:472-474`) of the
    cgroup whose charge failed (`:2625-2627`), and the `Tasks in <path>` group path can be a descendant of the
    block’s path (`:1947-1989`); the entry states `oom_memcg`≠`task_memcg` but not this pair, and it omits that the
    `Tasks state` table is where the per-process split is.

11. **No defect (recorded so the L1 does not “fix” it).** `## Limits` bullet 3 (rate-limit sentence) is fully
    supported and I could not break it: guard at `oom_kill.c:1030-1032`, victim line at `:945` reached from `:1042`
    and `:1050-1051`, all summary/context/task lines inside the guard, `Tasks in …` (`:1049`) outside it. Also
    verified: provenance of the three copies (§0), bullets 2–3 of `## Reading rules` (`doc:1398-1400`,
    `memcontrol.c:1701-1703`; `doc:1406-1436`), and bullet 5 (`oom_kill.c:465-466`, `memcontrol.c:1767-1768`,
    `:1770-1780`, `:472-474`).
