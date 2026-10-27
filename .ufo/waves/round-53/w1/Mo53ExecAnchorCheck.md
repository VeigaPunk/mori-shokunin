# Mo53ExecAnchorCheck — SOURCES.md anchor cells S502–S513 at 2a4213bf

Seat: Mo53ExecAnchorCheck (executor, round-53 wave w1). Scope: for every line range named in the
`anchor` cells of rows S502–S513 of `corpus/SOURCES.md` at `2a4213bf8da72f7cd78189baa5bb9be825dca1df`,
print those lines from the copy in `corpus/evidence/sources-r53/` and say whether they hold what the row's
`scope` and `teaches` cells say; check the `byte-identical to v7.2` claims (S504, S506, S509) by sha256
against the round-51/52 copies; check the change summaries (S503, S505, S507, S508, S510) against
`diff -u` of the copies; propose exact replacement text for any drift.

No counter, predicate, control or kill rule is proposed for change. Every finding below is in the anchors /
teaches text / ledger wording, i.e. data the L1 may correct. The C1 counter never reads the `anchor`
cell (it reads only the row's URL, `mined`, `opened` and `used-by`), so none of these findings can change a
C1 reading; they are traceability defects in the row text.

Scratch: `/fast/scratch/hyaku/mori-r53/Mo53ExecAnchorCheck/` (created, used, removed). No tool installed or
upgraded. Disk guard checked (`scripts/hyaku/disk-guard.sh status`, rc 0). Network used only against
git.kernel.org cgit: the nine v7.3 paths of S502–S510, `mm/mm_init.c` at v7.3 and the three v7.2 paths of
S511–S513 (13 fetches, all in the scratch dir).

Lane state while this seat ran: HEAD moved from the data commit `2a4213bf` to `fd86307a` ("data corrections
from w1"). Rows S502–S513 of `corpus/SOURCES.md` and `corpus/knowledge/kernel-v7.3-recheck-r53.md` are
byte-identical between the two (`diff` of the S502–S513 rows prints nothing; the ledger has no diff), so every
finding below still stands against HEAD. One finding was closed by that commit: `fd86307a` adds row S514
(`mm/mm_init.c` at v7.3, `mm_compute_batch` 195-214, sha256 678410005f88, copy
`corpus/evidence/sources-r53/mm_init.c.v7.3`) and rewrites the C2 boundary to cite it — exactly what §4.10
proposed. I had fetched that path independently before the commit landed and my fetch is byte-identical to the
committed copy (`sha256 678410005f881a64ae94d180c82174dc4474679b056ace69b6bc3d23978f976c`, `cmp` silent), and
S514's 195-214 is exactly the function, so that fix is correct. Finding 9 is therefore closed; finding 11 (the
host-kernel wording) survives in both S511's `scope` cell and the C2 boundary.

## 1. Evidence base and independent provenance

The lane's twelve copies were hashed, then the same paths were fetched again from cgit at the named tags into
scratch and compared byte for byte:

```
$ sha256sum corpus/evidence/sources-r53/*
d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda  meminfo.c.v7.3
ed691b24afbc0dc45090e149d115d707af0c5f7369a10b7722d491075f26a754  mm_init.c.v7.2
277e99e23ecc1b5babfdf041e7e7e3f9d280113b3b0a9f7e8340c0e13d7b391b  mm_inline.h.v7.3
d7bf787c910d9a7cbabee3a50c512ce3aad78d63659b0c968adca16b5916b058  mman.h.v7.3
8e51fb1c10fee6943c9edc26b72952137b4098b00cc050ea1e6ade6e27197feb  mmap.c.v7.3
767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f  overcommit-accounting.rst.v7.3
2c26e67751f939dfb21ff6221884280ae84a2a94a54de4468fb9dc8746130d6d  percpu_counter.c.v7.2
4a107bc381b3b5425b8ff441f7487d97ba6883dc6f5b426c4bd361ad7cbef896  percpu_counter.h.v7.2
bc178ff511e05c1b5e0c2413feb18223edcaeb2797ce499b714b98120cabf3c8  proc.rst.v7.3
c50205bc19974566d7bfe1c161f253cf71321c06ecc1327abb2a775be8a0de71  show_mem.c.v7.3
4dfcce2b8fa8f18c350565950a10248b3590e3d3c0c9335fef6d47daa7a9e1f2  util.c.v7.3
f81feb3dfca5f054cf8b76c71d7a4525a88d629d3ea8239743996b9d87bb391b  vm.rst.v7.3

$ curl -fsSL 'https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/<path>?h=v7.3'
277e99e23ecc  include/linux/mm_inline.h      d6c5807421a6  fs/proc/meminfo.c
c50205bc1997  mm/show_mem.c                  767ab88153c4  Documentation/mm/overcommit-accounting.rst
d7bf787c910d  include/linux/mman.h           bc178ff511e0  Documentation/filesystems/proc.rst
f81feb3dfca5  Documentation/admin-guide/sysctl/vm.rst   4dfcce2b8fa8  mm/util.c
8e51fb1c10fe  mm/mmap.c
$ curl ... '?h=v7.2'
ed691b24afbc  mm/mm_init.c     2c26e67751f9  lib/percpu_counter.c     4a107bc381b3  include/linux/percpu_counter.h
$ cmp <fetched> corpus/evidence/sources-r53/<copy>   -> IDENTICAL for all 12
```

So every `sha256` prefix in the anchor cells (bc178ff511e0, c50205bc1997, d6c5807421a6, 277e99e23ecc,
767ab88153c4, f81feb3dfca5, 4dfcce2b8fa8, d7bf787c910d, 8e51fb1c10fe, ed691b24afbc, 2c26e67751f9,
4a107bc381b3) matches both the committed copy and the independently fetched tag bytes. The tag ids are also
right: the sweep receipt (`evidence/sweeps.txt`) prints `refs/tags/v7.3` = 091b06388b11… and
`refs/tags/v7.3^{}` = c03c1a14507d…, `refs/tags/v7.2` = 237a1c39e8df… — matching the anchor cells.

## 2. Anchor verification, S502–S513

Format: the anchor cell's named locator, the lines printed from the `sources-r53/` copy, and the verdict
against the row's `scope`/`teaches` cells. Printed lines are quoted verbatim (leading indentation trimmed).

### S502 — `Documentation/filesystems/proc.rst` v7.3
Anchor names: meminfo section lines 1043-1240 (MemAvailable 1127, CommitLimit 1221, Committed_AS 1239).

```
1043: meminfo
1044: ~~~~~~~
1127: MemAvailable
1221: CommitLimit
1239: Committed_AS
1240:               The amount of memory presently allocated on the system.
```
All three named field lines and the section title are exact. `sed -n '1043,1240p'` prints the meminfo heading,
MemAvailable (1127) through "impact of those factors will vary from system to system.", Cached (1140),
Shmem (1194) and the CommitLimit block (1221-1238) — i.e. it holds "the /proc/meminfo field definitions" the
scope cell claims, and all five C1 ledger quotes sourced to S502 (lines 1128-1129, 1129-1131, 1134-1135,
1140-1141, 1194) sit inside it. Two imprecisions in the range, not in the fields:
- the meminfo section actually runs 1043–1302 (heading `vmallocinfo` at 1304), so "meminfo section lines
  1043-1240" is not the section;
- end 1240 falls one line into the Committed_AS description, which runs 1239-1251.
teaches ("v7.2 to v7.3 changes 3 lines, none in the meminfo definitions"): holds. `diff -u` gives exactly 3
changed lines — the typo fix `page is accounted as "shared" if any page page` → `…any page of` (v7.3:516) and
the added `ur    userfaultfd read-write-protect tracking` (v7.3:611) — both far above 1043. Consequence of the
added line: every line after 611 shifts +1, which is why the anchor's v7.3 numbers are 1127/1221/1239 where the
v7.2 row S492 has 1126/1220/1238. Consistent.

### S503 — `mm/show_mem.c` v7.3
Anchor names: si_mem_available lines 33-73.

```
33: long si_mem_available(void)
34: {
...
72: 	return available;
73: }
74: EXPORT_SYMBOL_GPL(si_mem_available);
```
Exact: 33-73 is the whole function including the closing brace. Body byte-identical to v7.2 (v7.2 32-72,
shifted +1 by the added `#include "page_alloc.h"` at v7.3:19): `cmp` of the two ranges prints nothing.
teaches ("the MemAvailable estimate body unchanged at v7.3"): holds. teaches ("the release's edits there are
an include, const nodemask parameters and printk units"): incomplete — see §4.1.

### S504 — `fs/proc/meminfo.c` v7.3
Anchor names: meminfo_proc_show from line 34 (CommitLimit and Committed_AS at 125-126).

```
28: static void show_val_kb(struct seq_file *m, const char *s, unsigned long num)
30: 	seq_put_decimal_ull_width(m, s, num << (PAGE_SHIFT - 10), 8);
31: 	seq_write(m, " kB\n", 4);
34: static int meminfo_proc_show(struct seq_file *m, void *v)
48: 	cached = global_node_page_state(NR_FILE_PAGES) -
61: 	show_val_kb(m, "MemFree:        ", i.freeram);
62: 	show_val_kb(m, "MemAvailable:   ", available);
125: 	show_val_kb(m, "CommitLimit:    ", vm_commit_limit());
126: 	show_val_kb(m, "Committed_AS:   ", committed);
```
34, 125, 126 are exact, and the file is byte-identical to the round-51 copy (d6c5807421a6 both), so the
"byte-identical to v7.2" claim holds. But the anchor starts at 34 and one of the three quotes the C1 ledger
attributes to S504 comes from the helper above it: 6c2327e19df1 (`seq_put_decimal_ull_width(…); seq_write(m,
" kB\n", 4);`) is at lines 30-31 in `show_val_kb` (28-32). The v7.2 predecessor row S494 anchored
`fs/proc/meminfo.c:27-31,48-51,56,61-64,105`, i.e. it named the helper. See §4.2.

### S505 — `include/linux/mm_inline.h` v7.3
Anchor names: folio_is_file_lru at line 28.

```
13: /**
14:  * folio_is_file_lru - Should the folio be on a file LRU or anon LRU?
...
23:  * 1 if @folio is a regular filesystem backed page cache folio
24:  * or a lazily freed anonymous folio (e.g. via MADV_FREE).
25:  * 0 if @folio is a normal anonymous folio, a tmpfs folio or otherwise
26:  * ram or swap backed folio.
27:  */
28: static inline int folio_is_file_lru(const struct folio *folio)
29: {
30: 	return !folio_test_swapbacked(folio);
31: }
```
28 is exact and the function is untouched by the release (the diff hunks start at 566). But both C1 ledger
quotes attributed to S505 (8f6d04247472, d6001a798ea7) are the kernel-doc lines 23-24 and 25-26, above the
named line. The v7.2 predecessor S495 anchored `include/linux/mm_inline.h:13-31`. See §4.3.

### S506 — `Documentation/mm/overcommit-accounting.rst` v7.3
Anchor names: whole file lines 1-85.

```
1:  =====================
2:  Overcommit Accounting
7:  0
8:  	Heuristic overcommit handling. Obvious overcommits of address
19: 2
20: 	Don't overcommit. The total address space commit for the
48: In mode 2 the MAP_NORESERVE flag is ignored.
57: 	| SHARED or READ-only	-	0 cost (the file is the map not swap)
83: To Do
84: =====
85: *	Account ptrace pages (this is hard)
```
`wc -l` = 85, so the whole-file anchor is exact, and the file is byte-identical to the round-52 copy
(767ab88153c4 both). The three-mode text (lines 7-29) and the mode-2 limit are where the scope cell says.
All seven C1 ledger quotes sourced to S506 are inside 1-85. Holds.

### S507 — `Documentation/admin-guide/sysctl/vm.rst` v7.3
Anchor names: admin_reserve_kbytes 82-109, overcommit_kbytes 823, overcommit_memory 834, overcommit_ratio 859,
user_reserve_kbytes 1106-1116.

```
82: admin_reserve_kbytes
83: ====================
823: overcommit_kbytes
824: =================
834: overcommit_memory
835: =================
859: overcommit_ratio
860: ================
1106: user_reserve_kbytes
1107: ===================
```
All five title lines are exact. Section bodies (computed from the title/underline pairs) are 82-108, 823-831,
834-856, 859-886 and 1106-1123. The anchor gives ranges for the two reserves but bare title lines for
overcommit_kbytes / overcommit_memory / overcommit_ratio, and four of the six C1 ledger quotes sourced to S507
sit 3-30 lines below those bare numbers (829-831, 839-840, 842-843, 862-864) — inside the sections, outside
the literal anchors. The v7.2 predecessor S498 gave ranges (`vm.rst:84-97,825-833,836-858,861-866,1029-1046`).
See §4.4.

teaches ("v7.3 adds panic_on_unrecoverable_memory_failure and drops a mm/swap.c pointer"): holds. The diff
removes the three-line "Default values and initialization routines … can be found in mm/swap.c." paragraph
(v7.2 19-21), adds the index bullet at `- panic_on_unrecoverable_memory_failure` (v7.3:67) and the new section
at v7.3:926-1002 (79 added lines in the hunk `@@ -925,6 +923,85 @@`; the next section starts at 1005).

### S508 — `mm/util.c` v7.3
Anchor names: overcommit_policy_handler 806, vm_commit_limit 904-916, __vm_enough_memory 959-1003.

```
781: int sysctl_overcommit_memory __read_mostly = OVERCOMMIT_GUESS;
782: static int sysctl_overcommit_ratio __read_mostly = 50;
783: static unsigned long sysctl_overcommit_kbytes __read_mostly;
806: static int overcommit_policy_handler(const struct ctl_table *table, int write,
814: 	 * The deviation of sync_overcommit_as could be big with loose policy
904: unsigned long vm_commit_limit(void)
916: }
959: int __vm_enough_memory(const struct mm_struct *mm, long pages, int cap_sys_admin)
1003: }
```
806, 904-916, 959-1003 are exact (the two ranges end precisely on the closing braces). `vm_commit_limit` and
`__vm_enough_memory` are untouched by the release, as the teaches cell says. But one C1 ledger quote attributed
to S508 — 9cb0e908f997, `static int sysctl_overcommit_ratio __read_mostly = 50;` — is at line 782, outside all
three named ranges; and 2d64007fa0dc (814-815) is inside the handler body whose start line 806 is what the
anchor names. The v7.2 predecessor S499 anchored `mm/util.c:781-786,806-840,901-1003`, i.e. it named the sysctl
defaults. See §4.5.

teaches ("the release's util.c edits sit in vm_mmap_pgoff and the shadow-stack helper"): incomplete — the diff
has four hunks; two of them are elsewhere. See §4.1.

### S509 — `include/linux/mman.h` v7.3
Anchor names: vm_acct_memory 76, vm_unacct_memory 81.

```
76: static inline void vm_acct_memory(long pages)
81: static inline void vm_unacct_memory(long pages)
```
Exact, and byte-identical to the round-52 copy (d7bf787c910d both, and the same digest the round-52 row S500
records). Both C1 ledger quotes (lines 76-79, 81-84) start at the named lines. Holds.

### S510 — `mm/mmap.c` v7.3
Anchor names: MAP_NORESERVE block 563-571, init_user_reserve 1566, init_admin_reserve 1587.

```
563: 	if (flags & MAP_NORESERVE) {
564: 		/* We honor MAP_NORESERVE if allowed to overcommit */
565: 		if (sysctl_overcommit_memory != OVERCOMMIT_NEVER)
566: 			vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);
568: 		/* hugetlb applies strict overcommit unless MAP_NORESERVE */
569: 		if (file && is_file_hugepages(file))
570: 			vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);
571: 	}
1566: static int init_user_reserve(void)
1587: static int init_admin_reserve(void)
```
563-571 is exactly the block, and both reserve initialisers start on the named lines. teaches ("the
MAP_NORESERVE rule kept under the v7.3 vma_flags_set spelling, which is why two round-52 quotes no longer match
byte for byte"): holds — `vm_flags |= VM_NORESERVE;` occurs in v7.2 and not in v7.3, `vma_flags_set(&vma_flags,
VMA_NORESERVE_BIT);` occurs in v7.3 and not in v7.2 (both checked in the copies). The two absent rows carry the
v7.3 spelling, which is what the predicate asks for. The two reserve quotes (1572, 1593) are inside the named
functions but below the named start lines — same title-line style as S507, LOW.

### S511 — `mm/mm_init.c` v7.2
Anchor names: mm_compute_batch lines 191-210, mm_compute_batch_init 226-233.

```
191: void mm_compute_batch(int overcommit_policy)
192: {
204: 	if (overcommit_policy == OVERCOMMIT_NEVER)
205: 		memsized_batch = min_t(u64, ram_pages/nr/256, INT_MAX);
210: }
226: static int __init mm_compute_batch_init(void)
231: }
233: __initcall(mm_compute_batch_init);
```
191-210 is exactly the function; 226-233 spans the initialiser plus its `__initcall` line (the function body
is 226-231). teaches ("the mode-2 batch rule (0.4 percent of RAM per CPU, floor max(2 x CPUs, 32))"): holds —
`min_t(u64, ram_pages/nr/256, INT_MAX)` for `OVERCOMMIT_NEVER` (1/256 = 0.39 %), `batch = max_t(s32, nr*2, 32)`,
and `vm_committed_as_batch = max_t(s32, memsized_batch, batch)`. The three C2-entry quotes (196-197, 199-202,
204-205) are all inside 191-210. Scope wording "(the host kernel line)" is imprecise — see §4.6.

### S512 — `lib/percpu_counter.c` v7.2
Anchor names: percpu_counter_add_batch lines 93-113 (SMP path).

```
87: #ifdef CONFIG_HAVE_CMPXCHG_LOCAL
93: void percpu_counter_add_batch(struct percpu_counter *fbc, s64 amount, s32 batch)
94: {
100: 		if (unlikely(abs(count + amount) >= batch)) {
101: 			raw_spin_lock_irqsave(&fbc->lock, flags);
113: }
114: #else
120: void percpu_counter_add_batch(struct percpu_counter *fbc, s64 amount, s32 batch)
```
93-113 is exactly the first `percpu_counter_add_batch` (the C2 quote at 100-101 is inside it), and teaches
("each CPU folds its local delta into the global count once it reaches the batch") holds for that body. But the
parenthetical is wrong: the in-file conditional that selects these lines is `#ifdef CONFIG_HAVE_CMPXCHG_LOCAL`
(87), with the alternative body at 114-137 under `#else`; the file contains no `CONFIG_SMP` at all
(`grep -c CONFIG_SMP lib/percpu_counter.c` → 0 on the re-fetched v7.2 bytes). See §4.7.

### S513 — `include/linux/percpu_counter.h` v7.2
Anchor names: percpu_counter_read_positive lines 118-126 (SMP).

```
20: #ifdef CONFIG_SMP
118: static inline s64 percpu_counter_read_positive(struct percpu_counter *fbc)
119: {
120: 	/* Prevent reloads of fbc->count */
121: 	s64 ret = READ_ONCE(fbc->count);
123: 	if (ret >= 0)
124: 		return ret;
125: 	return 0;
126: }
133: #else /* !CONFIG_SMP */
```
118-126 is exactly the function and the "(SMP)" label is correct here: the header's `#else /* !CONFIG_SMP */`
is at 133, so 118-126 sits inside the `CONFIG_SMP` branch opened at 20. teaches ("the mode-2 test reads only the
global count, never the per-CPU deltas"): holds. The C2 quote (120-123) is inside. Contrast this with S512:
the same "(SMP)" label is accurate in the header and inaccurate in the `.c`.

## 3. `byte-identical to v7.2` claims (S504, S506, S509)

```
$ cmp corpus/evidence/sources-r51/meminfo.c.v7.2 corpus/evidence/sources-r53/meminfo.c.v7.3 && echo IDENTICAL
IDENTICAL
$ cmp corpus/evidence/sources-r52/overcommit-accounting.rst.v7.2 corpus/evidence/sources-r53/overcommit-accounting.rst.v7.3 && echo IDENTICAL
IDENTICAL
$ cmp corpus/evidence/sources-r52/mman.h.v7.2 corpus/evidence/sources-r53/mman.h.v7.3 && echo IDENTICAL
IDENTICAL
```
sha256 equal in each pair (d6c5807421a6…, 767ab88153c4…, d7bf787c910d…), and `diff -u` yields 0 changed lines
for all three. All three claims hold. They carry ten C1 ledger rows between them: S504 backs three
(357c747c23d2, 6c2327e19df1, 7e14f1771092) and S506 seven, which is exactly what "carries over word for word"
means.

## 4. Drift and exact replacement text

Severity is in §7. Each proposal is the exact text to paste into the cell.

### 4.1 Change summaries that are incomplete (S503, S505, S508)

The ledger's own `What changed` table repeats the same summaries; fix both places.

S503 teaches (SOURCES) — now: "shows the MemAvailable estimate body unchanged at v7.3; the release's edits
there are an include, const nodemask parameters and printk units". The 22 changed lines of show_mem.c are:
`+#include "page_alloc.h"`; three `const nodemask_t *` signatures (`show_mem_node_skip`, `show_free_areas`,
`__show_mem`); printk unit fixes `" reserved_highatomic:%luKB"`→`%lukB`, `" free_highatomic:%luKB"`→`%lukB`,
`" local_pcp:%ukB"`→`%lukB`; `K(this_cpu_read(...))`→`K((unsigned long)this_cpu_read(...))`; and two printk
format-specifier flips `"%ld total pagecache pages"`→`"%lu"` and `"%lu pages hwpoisoned"`→`"%ld"`. The cell
names three of those five kinds. Replacement:

```
shows the MemAvailable estimate body unchanged at v7.3; the release's edits there are an include (`page_alloc.h`), three `const nodemask_t *` signatures, printk unit fixes (`%luKB` -> `%lukB`, `%ukB` -> `%lukB`), two printk format-specifier flips (`%ld` -> `%lu` on the pagecache line, `%lu` -> `%ld` on the hwpoisoned line) and one added `(unsigned long)` cast
```

S505 teaches (SOURCES) — now: "re-checks the file-LRU membership rule the MemAvailable estimate relies on;
the v7.3 edit removes an unrelated uffd-wp helper". mm_inline.h has exactly three hunks: the 53-line removal of
`pte_install_uffd_wp_if_needed` (a uffd-wp pte helper) and two changed lines in `num_pages_contiguous` where
`memdesc_section(cur_page->flags)` becomes `memdesc_section(&cur_page->flags)` (v7.3:600 and 610). Replacement:

```
re-checks the file-LRU membership rule the MemAvailable estimate relies on; the v7.3 edits remove the unrelated uffd-wp pte helper and pass `&cur_page->flags` to `memdesc_section()` at two call sites (v7.3:600, 610)
```

S508 teaches (SOURCES) — now: "shows the commit limit and the mode-2 test unchanged at v7.3; the release's
util.c edits sit in vm_mmap_pgoff and the shadow-stack helper". util.c has four hunks: (1) `vm_mmap_pgoff`,
`do_mmap(..., 0, pgoff, ...)` → `do_mmap(..., EMPTY_VMA_FLAGS, pgoff, ...)`; (2) `vm_mmap_shadow_stack`,
`vm_flags_t`/`VM_SHADOW_STACK` → `vma_flags_t`/`VMA_SHADOW_STACK`; (3) `compat_set_desc_from_vma`,
`desc->pgoff = vma->vm_pgoff` → `vma_start_pgoff(vma)`; (4) `call_vma_mapped`, `vm_ops->mapped(..., vma->vm_pgoff,
...)` → `vma_start_pgoff(vma)`. Hunks 3 and 4 are in neither named place. Replacement:

```
shows the commit limit and the mode-2 test unchanged at v7.3; the release's util.c edits sit in `vm_mmap_pgoff` (`EMPTY_VMA_FLAGS`), the shadow-stack helper (`vma_flags_t`), and two `vma->vm_pgoff` -> `vma_start_pgoff(vma)` conversions in `compat_set_desc_from_vma` and `call_vma_mapped`
```

S507 and S510 change summaries hold as written (verified in §2) and need no change.

### 4.2 S504 anchor — helper outside the named range

Now: "tag v7.3 (091b06388b11, commit c03c1a14507d); meminfo_proc_show from line 34 (CommitLimit and
Committed_AS at 125-126); sha256 d6c5807421a6, byte-identical to v7.2; copy
corpus/evidence/sources-r53/meminfo.c.v7.3". Replacement (adds the `show_val_kb` helper at 28-32, which is
where the kB-format quote the ledger attributes to this row lives):

```
tag v7.3 (091b06388b11, commit c03c1a14507d); show_val_kb helper 28-32, meminfo_proc_show from line 34 (CommitLimit and Committed_AS at 125-126); sha256 d6c5807421a6, byte-identical to v7.2; copy corpus/evidence/sources-r53/meminfo.c.v7.3
```

### 4.3 S505 anchor — doc comment outside the named line

Now: "…; folio_is_file_lru at line 28; …". Both ledger quotes for this row are the kernel-doc text at 23-26.
Replacement (mirrors the v7.2 row S495's 13-31):

```
tag v7.3 (091b06388b11, commit c03c1a14507d); folio_is_file_lru kernel-doc and definition 13-31 (function at 28); sha256 277e99e23ecc; copy corpus/evidence/sources-r53/mm_inline.h.v7.3
```

### 4.4 S507 anchor — bare title lines instead of section ranges

Now: "…; admin_reserve_kbytes 82-109, overcommit_kbytes 823, overcommit_memory 834, overcommit_ratio 859,
user_reserve_kbytes 1106-1116; …". Replacement (section bodies computed from the title/underline pairs; drops
the trailing blank at 109, covers the bodies where the quotes are, and keeps the full user_reserve_kbytes
section):

```
tag v7.3 (091b06388b11, commit c03c1a14507d); admin_reserve_kbytes 82-108, overcommit_kbytes 823-831, overcommit_memory 834-856, overcommit_ratio 859-886, user_reserve_kbytes 1106-1123; sha256 f81feb3dfca5; copy corpus/evidence/sources-r53/vm.rst.v7.3
```

### 4.5 S508 anchor — sysctl defaults dropped

Now: "…; overcommit_policy_handler 806, vm_commit_limit 904-916, __vm_enough_memory 959-1003; …". One ledger
row quotes util.c:782, so the defaults block must be named. Replacement:

```
tag v7.3 (091b06388b11, commit c03c1a14507d); sysctl_overcommit_memory/ratio/kbytes defaults 781-783, overcommit_policy_handler 806-840, vm_commit_limit 904-916, __vm_enough_memory 959-1003; sha256 4dfcce2b8fa8; copy corpus/evidence/sources-r53/util.c.v7.3
```

### 4.6 S511 scope — "the host kernel line"

The copy is the upstream torvalds v7.2 tag (237a1c39e8df). The host runs 7.2.11-arch1-1 (`uname -r`,
2026-10-26) and its own `mm_init.c` is neither in the lane nor on this machine
(`/usr/lib/modules/7.2.11-arch1-1/build/mm/` contains only Kconfig/Kconfig.debug/damon), so the identification
of the copied bytes with the host's kernel is unverified. Replacement scope cell:

```
the vm_committed_as batch size by overcommit policy at v7.2 (the copy is the upstream v7.2 tag 237a1c39e8df; the host runs the 7.2 line, 7.2.11-arch1-1, whose own bytes are not in evidence)
```

### 4.7 S512 anchor — "(SMP path)" names a macro that is not there

Now: "…; percpu_counter_add_batch lines 93-113 (SMP path); …". Replacement:

```
tag v7.2 (237a1c39e8df); percpu_counter_add_batch lines 93-113 (the CONFIG_HAVE_CMPXCHG_LOCAL branch, guarded at line 87; the alternative body at 114-137 under #else); sha256 2c26e67751f9; copy corpus/evidence/sources-r53/percpu_counter.c.v7.2
```

### 4.8 S502 anchor — range end is not the section end

Now: "…; meminfo section lines 1043-1240 (MemAvailable 1127, CommitLimit 1221, Committed_AS 1239); …".
Replacement:

```
tag v7.3 (091b06388b11, commit c03c1a14507d); meminfo section lines 1043-1302 (MemAvailable 1127, CommitLimit 1221, Committed_AS 1239-1251); sha256 bc178ff511e0; copy corpus/evidence/sources-r53/proc.rst.v7.3
```

### 4.9 Ledger `What changed` table (corpus/knowledge/kernel-v7.3-recheck-r53.md)

The table's stated method is `diff -u <v7.2 copy> <v7.3 copy> | grep -c '^[-+][^-+]'`, which does not match a
bare `-` or `+` line and therefore drops every blank added/removed line. Reproduced exactly (proc.rst 3,
show_mem.c 22, mm_inline.h 49, vm.rst 64, util.c 14, mmap.c 190) — so the numbers are honest under the stated
method, but they understate the real change, which `git diff --no-index --numstat` gives as 3, 22, 57, 83, 14,
205. Proposal: keep the method note and add the split, e.g. replace the sentence

```
Line counts: `diff -u <v7.2 copy> <v7.3 copy> | grep -c '^[-+][^-+]'` over the round-51/52 copies and
`corpus/evidence/sources-r53/`.
```
with
```
Line counts: `diff -u <v7.2 copy> <v7.3 copy> | grep -c '^[-+][^-+]'` over the round-51/52 copies and
`corpus/evidence/sources-r53/` (this pattern skips changed blank lines). Added+removed lines by
`git diff --no-index --numstat`: proc.rst 3, show_mem.c 22, mm_inline.h 57 (2/55), vm.rst 83 (80/3),
util.c 14, mmap.c 205 (92/113).
```
and correct the three affected `where` cells:
- `include/linux/mm_inline.h` row: "49 changed lines | removal of the uffd-wp pte helper; `folio_is_file_lru`
  untouched" → "49 changed lines (57 added+removed) | removal of the uffd-wp pte helper and two
  `memdesc_section(&cur_page->flags)` call sites; `folio_is_file_lru` untouched".
- `Documentation/admin-guide/sysctl/vm.rst` row: "64 changed lines" → "64 changed lines (83 added+removed)"
  (the rest of the row is accurate).
- `mm/util.c` row: "14 changed lines | `vm_mmap_pgoff` and the shadow-stack helper (`vm_flags_t` →
  `vma_flags_t`); `vm_commit_limit`, `__vm_enough_memory` untouched" → "14 changed lines | `vm_mmap_pgoff`
  (`EMPTY_VMA_FLAGS`), the shadow-stack helper (`vm_flags_t` → `vma_flags_t`), and two `vma->vm_pgoff` →
  `vma_start_pgoff(vma)` conversions (`compat_set_desc_from_vma`, `call_vma_mapped`); `vm_commit_limit`,
  `__vm_enough_memory` untouched".
- `mm/mmap.c` row: "190 changed lines | the `vm_flags_t` → `vma_flags_t` conversion, including the
  `MAP_NORESERVE` block" → "190 changed lines (205 added+removed) | the `vm_flags_t` → `vma_flags_t`
  conversion including the `MAP_NORESERVE` block, the `mm_get_unmapped_area_vmflags` →
  `mm_get_unmapped_area_vmaflags` rename, and the removal of `__install_special_mapping` from this file
  (38 lines deleted, v7.2 hunk `@@ -1447,44 +1462,6 @@`, the helper itself at v7.2:1450-1486; the call at
  v7.3:1486 now reaches a definition held elsewhere)".
- `mm/show_mem.c` row: "22 changed lines | an include, `const nodemask_t *` parameters, printk units
  (`%luKB` → `%lukB`); `si_mem_available` untouched" → add "two printk format-specifier flips (`%ld`/`%lu`) and
  one `(unsigned long)` cast" before "; `si_mem_available` untouched".

### 4.10 C2 entry boundary cites a copy the lane does not hold — closed at `fd86307a`

At the data commit, `corpus/knowledge/commit-runway-read-r53.md` Boundaries, line 51-52 read: "the batch rule is
unchanged at v7.3 (`mm_compute_batch` in the v7.3 copy differs only by its line number)". The claim is true — I
fetched `mm/mm_init.c?h=v7.3` independently (sha256
678410005f881a64ae94d180c82174dc4474679b056ace69b6bc3d23978f976c, 2693 lines): `mm_compute_batch` sits at
195-214 and `cmp` of 195-214 against the v7.2 copy's 191-210 is empty (only the line number moves, 191→195). But
at that commit the lane pinned no v7.3 `mm_init.c`, so the sentence could not be checked from the repo.
`fd86307a` closed this by adding S514 and citing `corpus/evidence/sources-r53/mm_init.c.v7.3:195-214`; the
committed copy is byte-identical to my fetch. Text proposed at the time (kept for the record):

```
- v7.2 bytes, the host's kernel line (7.2.11); the batch rule is unchanged at v7.3 (`mm_compute_batch` at
  mm/mm_init.c v7.3:195-214 is byte-identical to the v7.2 copy at 191-210; verified 2026-10-26 by fetching
  mm/mm_init.c?h=v7.3, sha256 678410005f881a64ae94d180c82174dc4474679b056ace69b6bc3d23978f976c, not pinned in
  this lane).
```

Related wording: "the host's kernel line (7.2.11)" has the same unverified identification as §4.6.

## 5. Cross-checks that held

- Ledger vs frozen scope D: reusing the counter's own `scope()` reader over the entering tip gives 46 hashes;
  the ledger has exactly 46 rows, every hash is in D, every `entry` cell matches D's entry, every `held` row's
  quote is whitespace-equal to D's v7.2 quote, and both `absent` rows carry a quote that is not the v7.2 quote.
  0 problems (script run against the frozen module, read-only; no counter change proposed).
- The two `absent` rows are exactly the two MAP_NORESERVE rows: `vm_flags |= VM_NORESERVE;` is in the v7.2
  copy and not in the v7.3 copy; `vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);` is in the v7.3 copy and not in
  the v7.2 copy.
- Each of the nine frozen v7.3 URLs (`count-c1.py` V73 map) is the URL in exactly one SOURCES row, and each of
  those rows is `mined`, opened 2026-10-26, and lists `corpus/knowledge/kernel-v7.3-recheck-r53.md` in used-by;
  S511-S513 are `mined`, opened 2026-10-26, used-by `corpus/knowledge/commit-runway-read-r53.md`, which lists
  them as its sources.
- C2 entry quotes: all 8 claim-table quotes occur (whitespace-collapsed) in the copies their source cell names
  (S511 ×3, S512, S513, S499 ×3).
- `uname -r` = 7.2.11-arch1-1, matching the C1 entry's "the host runs 7.2.11" boundary and the S511/C2 phrase
  under discussion.
- Incidental check of the row `fd86307a` added (S514, outside my assigned S502–S513 range): its URL
  `mm/mm_init.c?h=v7.3`, copy `corpus/evidence/sources-r53/mm_init.c.v7.3` (sha256 678410005f88…, identical to
  my independent cgit fetch), anchor `mm_compute_batch lines 195-214` (195 = signature, 214 = closing brace) and
  teaches ("byte-identical to v7.2 apart from its position") all hold; its `used-by` names the C2 entry, which
  lists it as a source. It is not one of the nine paths in the C1 counter's frozen V73 map (the nine frozen URLs
  still each appear in exactly one SOURCES row), so it cannot affect C1's `source_rows` or `pins` legs.

## 6. Named limits of this check

- Anchor coverage was tested with a whitespace-collapsed locator (the same normalisation the counter uses for
  quotes). That is the right test for "is the quoted text at the named place", but it cannot tell whether a
  quote's meaning survives the move; that is the disposition's job, not mine.
- The v7.3 comparisons use the round-51/52 copies as the v7.2 side (they are the lane's pinned v7.2 bytes);
  I did not re-fetch v7.2 for the nine v7.3 paths, only for S511-S513.
- The host's own kernel source is not available, so "the host kernel line" cannot be checked (§4.6, §4.10).
- The v7.3 `mm_init.c` fetch is scratch-only and is not evidence in the repo; it is cited by command and
  sha256 in §4.10 and disappears with the scratch dir.

## Findings

1. **MED — S504 anchor does not cover one of its own quotes.** `corpus/SOURCES.md` row S504, `anchor` cell:
   "meminfo_proc_show from line 34" leaves out `show_val_kb` (v7.3:28-32), where ledger quote 6c2327e19df1
   lives (lines 30-31). Replacement in §4.2. (The v7.2 predecessor S494 named 27-31.)
2. **MED — S505 anchor does not cover either of its own quotes.** Row S505, `anchor` cell: "folio_is_file_lru at
   line 28" leaves out the kernel-doc comment at 13-27, where quotes 8f6d04247472 (23-24) and d6001a798ea7
   (25-26) live. Replacement in §4.3.
3. **MED — S505 `teaches` cell understates the v7.3 edit.** Row S505, `teaches`: says only that the release
   "removes an unrelated uffd-wp helper"; the diff also changes `memdesc_section(cur_page->flags)` →
   `memdesc_section(&cur_page->flags)` at v7.3:600 and 610. Replacement in §4.1.
4. **MED — S508 anchor does not cover one of its own quotes.** Row S508, `anchor` cell: none of 806 / 904-916 /
   959-1003 contains util.c:782, the `sysctl_overcommit_ratio … = 50;` line quoted by ledger row 9cb0e908f997.
   Replacement in §4.5.
5. **MED — S508 `teaches` cell understates the v7.3 edit.** Row S508, `teaches`: names two of four edit sites;
   the `vma->vm_pgoff` → `vma_start_pgoff(vma)` hunks in `compat_set_desc_from_vma` (v7.3:1191) and
   `call_vma_mapped` (v7.3:1382) are omitted. Replacement in §4.1.
6. **MED — S507 anchors name title lines where the quotes are 3-30 lines below.** Row S507, `anchor` cell:
   overcommit_kbytes 823, overcommit_memory 834, overcommit_ratio 859 are bare titles; four ledger quotes
   (5c40f6fa5c62 at 829-831, 43cf2a78acdd at 839-840, 35d642f1d0d9 at 842-843, fcd0e7a78872 at 862-864) fall
   outside the literal anchors though inside the sections. Replacement ranges in §4.4.
7. **MED — S503 `teaches` cell understates the v7.3 edit.** Row S503, `teaches`: "an include, const nodemask
   parameters and printk units" omits the added `(unsigned long)` cast (v7.3:353) and the two printk
   format-specifier flips (v7.3:403 `%ld`→`%lu`, v7.3:433 `%lu`→`%ld`). Replacement in §4.1.
8. **MED — S512 anchor's "(SMP path)" names a macro absent from the file.** Row S512, `anchor` cell: lines
   93-113 are the `CONFIG_HAVE_CMPXCHG_LOCAL` branch (`#ifdef` at 87, `#else` at 114); `grep -c CONFIG_SMP` on
   the re-fetched v7.2 bytes is 0. S513's "(SMP)" by contrast is correct (inside `#ifdef CONFIG_SMP` at 20..132).
   Replacement in §4.7.
9. **MED — CLOSED at `fd86307a` — C2 entry cited a v7.3 copy the lane did not pin.**
   `corpus/knowledge/commit-runway-read-r53.md:51-52` at `2a4213bf` ("`mm_compute_batch` in the v7.3 copy
   differs only by its line number"): the claim was true against an independent cgit fetch (sha256
   678410005f88…, function at 195-214, body identical to 191-210) but no v7.3 `mm_init.c` existed under
   `corpus/evidence/`, so the sentence was unreproducible from the repo. `fd86307a` adds S514 pinning exactly
   that file and rewrites the boundary to cite it; my independent fetch is byte-identical to the new copy and
   `cmp` of v7.3:195-214 against v7.2:191-210 is silent, so the fix is correct. Recorded here only as evidence
   that the finding was real at the data commit; no further action. §4.10 is the text that was proposed.
10. **LOW — S502 anchor's range end is not the section end and truncates Committed_AS.** Row S502, `anchor`
    cell: "meminfo section lines 1043-1240"; the section runs 1043-1302 (vmallocinfo at 1304) and the
    Committed_AS description runs 1239-1251. All five S502 quotes are inside, and the three named field lines
    (1127/1221/1239) are exact, so only the range text is wrong. Replacement in §4.8.
11. **LOW — S511 `scope` cell's "(the host kernel line)" over-identifies the copy with the host kernel.** Row
    S511, `scope`: the copy is upstream tag v7.2 (237a1c39e8df); the host runs 7.2.11-arch1-1 and its own
    `mm_init.c` is not in evidence (no source under `/usr/lib/modules/7.2.11-arch1-1/build/mm/`).
    UNVERIFIED for the host's bytes. Replacement in §4.6.
12. **LOW — the ledger's "changed lines" numbers understate because of the stated counting method.**
    `corpus/knowledge/kernel-v7.3-recheck-r53.md`, the `What changed` table: `grep -c '^[-+][^-+]'` drops changed
    blank lines, giving 49 vs 57 (mm_inline.h), 64 vs 83 (vm.rst) and 190 vs 205 (mmap.c); the `where` cell for
    mmap.c also calls a 205-line diff "the `vm_flags_t` → `vma_flags_t` conversion" although it deletes the
    38-line `__install_special_mapping` helper and renames `mm_get_unmapped_area_vmflags`. Replacements in §4.9.
13. **LOW — S507/S510 name function start lines where the quotes are inside the function bodies.** Rows S507
    (`user_reserve_kbytes 1106-1116`) and S510 (`init_user_reserve 1566`, `init_admin_reserve 1587`): quotes at
    1572 and 1593 sit inside the functions but outside the literal named line, and S507's 1106-1116 stops 7
    lines before the section ends (1123). Same class as finding 6; folded into §4.4. No claim is wrong.
14. **LOW — no drift found in S502, S503, S506, S509, S510, S511, S513 line numbers or in the three
    byte-identity claims.** Recorded so the L1 knows these were checked and need no change: S502's 1043/1127/
    1221/1239, S503's 33-73 (body byte-identical to v7.2), S506's 1-85 and byte-identity, S509's 76/81 and
    byte-identity, S510's 563-571/1566/1587, S511's 191-210/226-233, S513's 118-126 and its "(SMP)" label.
