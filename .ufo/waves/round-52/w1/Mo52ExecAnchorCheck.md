# Mo52ExecAnchorCheck — anchor cells of S497–S501 (round 52, w1)

Seat: executor (leaf). Lane: mori-shokunin. Measured revision `8524904adb25e44f24d9f25aac7eae909625c18c`
(round-52 data commit). Lane HEAD at run time `075436b1346ca659afb8be7a46f0e67e4170aa83`; `git diff --stat
8524904 HEAD -- corpus/SOURCES.md corpus/evidence/sources-r52` is empty, so the working tree bytes of my surface
are the measured ones — the proposals below are not stale.

Scope of this seat: the `anchor` cells of rows S497–S501 in `corpus/SOURCES.md`, checked against the copies in
`corpus/evidence/sources-r52/`; the 11-cell shape of each row; each row's `used-by` cell. Not my item: the entry
prose locators (`Mo52ExecProseLines`), the entry table quotes, and the host formula check (`Mo52ExecHostCommit`).

Method: read-only. `git -C <lane> show 8524904...:corpus/SOURCES.md` for the rows; the five copies read in place
from `corpus/evidence/sources-r52/`; `sha256sum` on the copies. No network fetch, no writes into the lane except
this report, no git/jj mutation. Scratch `/fast/scratch/hyaku/mori-r52/Mo52ExecAnchorCheck/` (created, used for
`TMPDIR`, removed before the end).

## 1. Shape checks (all five rows)

Command:

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r52 && sha256sum *.v7.2 && wc -l *.v7.2
d7bf787c910d9a7cbabee3a50c512ce3aad78d63659b0c968adca16b5916b058  mman.h.v7.2
449b858385c7ece0ff88a8b41893efadb70a437fb8585a296c4ef0461a4c1545  mmap.c.v7.2
767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f  overcommit-accounting.rst.v7.2
e702754c45bd7bd69e5da22a6505c9c1016eaafe6e883b746cc3cdbd413ebe7c  util.c.v7.2
bf8ca0265fefc019250697b6ee47a0679709b2ee45f4d1893b3dfd95c1f8c1ce  vm.rst.v7.2
   173 mman.h.v7.2
  1921 mmap.c.v7.2
    85 overcommit-accounting.rst.v7.2
  1608 util.c.v7.2
  1153 vm.rst.v7.2
exit=0
```

`split_cells` on the unescaped `|` (the counter's own rule, `count-c2.py:68-70`), rows selected with
`^ {0,3}\|\s*S(497|…|501)\s*\|`:

```
S497 cells= 11 status= mined opened= 2026-10-26 usedby= ['corpus/knowledge/overcommit-commit-limit-r52.md']
S498 cells= 11 status= mined opened= 2026-10-26 usedby= ['corpus/knowledge/overcommit-commit-limit-r52.md']
S499 cells= 11 status= mined opened= 2026-10-26 usedby= ['corpus/knowledge/overcommit-commit-limit-r52.md']
S500 cells= 11 status= mined opened= 2026-10-26 usedby= ['corpus/knowledge/overcommit-commit-limit-r52.md']
S501 cells= 11 status= mined opened= 2026-10-26 usedby= ['corpus/knowledge/overcommit-commit-limit-r52.md']
exit=0
```

- All five rows are `|`-delimited with 11 cells and 0 leading spaces (`corpus/SOURCES.md:276-280` at 8524904).
- All five name exactly one `used-by` path, `corpus/knowledge/overcommit-commit-limit-r52.md` — the entry the
  counter expects (`ENTRY`, `count-c2.py:43`).
- All five are `mined` / opened `2026-10-26`, which is what `row_ok` requires (`count-c2.py:226-228`).
- Each anchor cell carries `tag v7.2` and `copy … sha256 <digest>`; the five digests in the cells equal the
  `sha256sum` of the five copies above, and equal the frozen `COPIES` table (`count-c2.py:49-60`). Pins hold.
- Every named line range is in bounds: 85/1153/1608/173/1921-line files, highest cited line 1619 (S501), 1046
  (S498), 1006 (S499), 85 (S497), 84 (S500).

## 2. Range-by-range check (lines printed from the copies)

Boundary lines below are verbatim from the copies (`repr` of the line, trailing whitespace visible). "Holds"
means the printed lines carry what the row's `scope` and `teaches` cells say.

### S497 — `overcommit-accounting.rst:7-28,33-37,45,54-64,83-84` (85-line copy)

```
7-28  in-bounds
  first 7: '0'
  last  28: '\tallocations will be available in the future without having to'
33-37 in-bounds
  first 33: 'The overcommit amount can be set via ``vm.overcommit_ratio`` (percentage)'
  last  37: 'The current overcommit limit and amount committed are viewable in'
45    in-bounds
  first 45: 'largest size you think you will need. For typical stack usage this does'
54-64 in-bounds
  first 54: 'The overcommit is based on the following rules'
  last  64: ''
83-84 in-bounds
  first 83: 'To Do'
  last  84: '====='
```

Interior lines that decide the verdict:

```
 7: 0
 8: \tHeuristic overcommit handling. Obvious overcommits of address
11: \treduce swap usage. This is the default.
13: 1
14: \tAlways overcommit. Appropriate for some scientific
19: 2
20: \tDon't overcommit. The total address space commit for the
21: \tsystem is not permitted to exceed swap + a configurable amount
22: \t(default is 50%) of physical RAM.  Depending on the amount you
24: \tkilled while accessing pages but will receive errors on memory
25: \tallocation as appropriate.
29: \tinitialize every page.
31: The overcommit policy is set via the sysctl ``vm.overcommit_memory``.
34: or ``vm.overcommit_kbytes`` (absolute value). These only have an effect
35: when ``vm.overcommit_memory`` is set to 2.
38: ``/proc/meminfo`` as CommitLimit and Committed_AS respectively.
43: The C language stack growth does an implicit mremap. If you want absolute
44: guarantees and run close to the edge you MUST mmap your stack for the
46: not matter much but it's a corner case if you really really care
48: In mode 2 the MAP_NORESERVE flag is ignored.
56: For a file backed map
57: \t| SHARED or READ-only\t-\t0 cost (the file is the map not swap)
60: For an anonymous or ``/dev/zero`` map
63: \t| PRIVATE WRITABLE\t-\tsize of mapping per instance
85: *\tAccount ptrace pages (this is hard)
```

- `7-28` holds "the three overcommit modes" and "the mode-2 limit" (mode 0 at 7-11, mode 1 at 13-17, mode 2 at
  19-28 with "swap + a configurable amount (default is 50%) of physical RAM"), **but** it ends mid-sentence:
  28 ends "without having to", and the sentence closes at 29 ("initialize every page."). Truncated range end.
- `33-37` holds "the mode-2 limit" setting (`overcommit_ratio`/`overcommit_kbytes` "only have an effect when
  `vm.overcommit_memory` is set to 2", 34-35) but again ends mid-sentence: 37 ends "are viewable in" and 38 names
  `CommitLimit` and `Committed_AS` — the two lines the whole entry is about. Truncated range end.
- `45` **does not hold anything this row's scope or teaches names.** It is the middle of the stack-growth gotcha
  (43-46): `largest size you think you will need. For typical stack usage this does`. Neither cell mentions stack
  growth or `mremap`. The line that fits this row is 48, `In mode 2 the MAP_NORESERVE flag is ignored.` — a mode-2
  accounting rule, and the exact quote the entry uses for its S497 MAP_NORESERVE claim.
- `54-64` holds "the per-mapping accounting rules" (file-backed 56-58, anonymous/`/dev/zero` 60-63). 64 is a blank
  line; harmless.
- `83-84` **does not hold "the listed gaps".** 83 is `To Do`, 84 is the `=====` underline, and the only gap item is
  85: `*\tAccount ptrace pages (this is hard)`. A reader following `83-84` sees a heading and no content, and the
  entry's own ptrace claim quotes 83-85 ("To Do ===== * Account ptrace pages (this is hard)").
- `teaches` ("Only mode 2 caps the committed total (swap plus a share of RAM, default half) and fails allocations
  instead of killing; modes 0 and 1 overcommit") is held by 20-25 and 8-11/13-17. Verdict: teaches holds; scope
  holds for three of its four items, fails for "the listed gaps".

### S498 — `vm.rst:84-97,825-833,836-858,861-866,1029-1046` (1153-line copy)

```
84-97     first 84: 'admin_reserve_kbytes'
          last  97: 'root may not be able to log in to recover the system.'
825-833   first 825: 'overcommit_kbytes'
          last  833: 'then appears as 0 when read).'
836-858   first 836: 'overcommit_memory'
          last  858: 'mm/util.c::__vm_enough_memory() for more information.'
861-866   first 861: 'overcommit_ratio'
          last  866: 'of physical RAM.  See above.'
1029-1046 first 1029: 'user_reserve_kbytes'
          last  1046: 'Changing this takes effect whenever an application requests memory.'
```

Interior lines:

```
 84: admin_reserve_kbytes
 90: admin_reserve_kbytes defaults to min(3% of free pages, 8MB)
 92: That should provide enough for the admin to log in and kill a process,
 93: if necessary, under the default overcommit 'guess' mode.
 95: Systems running under overcommit 'never' should increase this to account
 97: root may not be able to log in to recover the system.
828: When overcommit_memory is set to 2, the committed address space is not
829: permitted to exceed swap plus this amount of physical RAM. See below.
831: Note: overcommit_kbytes is the counterpart of overcommit_ratio. Only one
832: of them may be specified at a time. Setting one disables the other (which
833: then appears as 0 when read).
841: When this flag is 0, the kernel compares the userspace memory request
842: size against total memory plus swap and rejects obvious overcommits.
844: When this flag is 1, the kernel pretends there is always enough
845: memory until it actually runs out.
847: When this flag is 2, the kernel uses a "never overcommit"
849: Note that user_reserve_kbytes affects this policy.
855: The default value is 0.
857: See Documentation/mm/overcommit-accounting.rst and
864: When overcommit_memory is set to 2, the committed address
865: space is not permitted to exceed swap plus this percentage
866: of physical RAM.  See above.
1032: When overcommit_memory is set to 2, "never overcommit" mode, reserve
1033: min(3% of current process size, user_reserve_kbytes) of free memory.
1037: This setting has no effect when overcommit_memory is set to 0 or 1.
1039: user_reserve_kbytes defaults to min(3% of the current process size, 128MB).
1046: Changing this takes effect whenever an application requests memory.
```

- Scope names five sysctls; each range is the whole section of one of them (heading through the last paragraph
  line), and each range ends on a complete sentence. `teaches` ("Mode 0 compares one request with RAM plus swap,
  mode 1 never refuses; ratio and kbytes are exclusive and act only in mode 2; two reserves") is held by 841-842,
  844-845, 831-833 + 828-829 + 864-866, and 84-97 + 1029-1046.
- Verdict: **holds, no drift.** Nothing to propose for S498.

### S499 — `mm/util.c:781-786,806-834,901-1006` (1608-line copy)

```
781-786  first 781: 'int sysctl_overcommit_memory __read_mostly = OVERCOMMIT_GUESS;'
         last  786: 'unsigned long sysctl_admin_reserve_kbytes __read_mostly = 1UL << 13; /* 8MB */'
806-834  first 806: 'static int overcommit_policy_handler(const struct ctl_table *table, int write,'
         last  834: '\t\tsysctl_overcommit_memory = new_policy;'
901-1006 first 901: '/*'
         last  1006: ' * get_cmdline() - copy the cmdline value to a buffer.'
```

Interior lines:

```
781: int sysctl_overcommit_memory __read_mostly = OVERCOMMIT_GUESS;
782: static int sysctl_overcommit_ratio __read_mostly = 50;
783: static unsigned long sysctl_overcommit_kbytes __read_mostly;
785: unsigned long sysctl_user_reserve_kbytes __read_mostly = 1UL << 17; /* 128MB */
786: unsigned long sysctl_admin_reserve_kbytes __read_mostly = 1UL << 13; /* 8MB */
806: static int overcommit_policy_handler(const struct ctl_table *table, int write,
813: \t * The deviation of sync_overcommit_as could be big with loose policy
814: \t * like OVERCOMMIT_ALWAYS/OVERCOMMIT_GUESS. When changing policy to
831: \t\tmm_compute_batch(new_policy);
832: \t\tif (new_policy == OVERCOMMIT_NEVER)
833: \t\t\tschedule_on_each_cpu(sync_overcommit_as);
834: \t\tsysctl_overcommit_memory = new_policy;
835: \t} else {
836: \t\tret = proc_dointvec_minmax(table, write, buffer, lenp, ppos);
837: \t}
839: \treturn ret;
840: }
901: /*
902:  * Committed memory limit enforced when OVERCOMMIT_NEVER policy is used
904: unsigned long vm_commit_limit(void)
908: \tif (sysctl_overcommit_kbytes)
909: \t\tallowed = sysctl_overcommit_kbytes >> (PAGE_SHIFT - 10);
911: \t\tallowed = ((totalram_pages() - hugetlb_total_pages())
912: \t\t\t   * sysctl_overcommit_ratio / 100);
913: \tallowed += total_swap_pages;
922: struct percpu_counter vm_committed_as ____cacheline_aligned_in_smp;
937: unsigned long vm_memory_committed(void)
939: \treturn percpu_counter_sum_positive(&vm_committed_as);
959: int __vm_enough_memory(const struct mm_struct *mm, long pages, int cap_sys_admin)
964: \tvm_acct_memory(pages);
969: \tif (sysctl_overcommit_memory == OVERCOMMIT_ALWAYS)
970: \t\treturn 0;
972: \tif (sysctl_overcommit_memory == OVERCOMMIT_GUESS) {
973: \t\tif (pages > totalram_pages() + total_swap_pages)
978: \tallowed = vm_commit_limit();
982: \tif (!cap_sys_admin)
983: \t\tallowed -= sysctl_admin_reserve_kbytes >> (PAGE_SHIFT - 10);
988: \tif (mm) {
991: \t\tallowed -= min_t(long, mm->total_vm / 32, reserve);
994: \tif (percpu_counter_read_positive(&vm_committed_as) < allowed)
998: \tpr_warn_ratelimited("%s: pid: %d, comm: %s, bytes: %lu not enough memory for the allocation\n",
1000: \tvm_unacct_memory(pages);
1002: \treturn -ENOMEM;
1003: }
1004:
1005: /**
1006:  * get_cmdline() - copy the cmdline value to a buffer.
```

- Scope names `vm_commit_limit()`, `vm_memory_committed()`, `__vm_enough_memory()` and the overcommit policy
  handler. The first three are wholly inside `901-1006`; the handler is `806-840`, and the cited `806-834` stops
  at `sysctl_overcommit_memory = new_policy;` — the `} else {` branch (835-837) and `return ret;` (839-840) are cut.
- `901-1006` **overruns the symbol**: `__vm_enough_memory` closes at 1003, 1004 is blank, and 1005-1006 are the
  opening of `get_cmdline()`'s kernel-doc. A reader following the anchor lands inside an unrelated function's
  documentation.
- `781-786` is the compiled-in sysctl defaults block (`ratio = 50`, the two reserves). It is **not one of the four
  items the scope cell names**, so the row cites lines its scope does not describe — while the entry does use it
  (its "compiled-in default for the ratio knob is fifty" claim quotes 782), so the lines are warranted and the
  *scope* is what is short.
- `teaches` ("CommitLimit is (RAM minus hugetlb) times ratio plus swap, or kbytes plus swap; every request is
  charged first; only mode 2 tests the total") is held: 908-913, 964 before any mode test, and the committed-total
  test only in the never path (978-994; mode 1 returns at 969-970, mode 0 compares the single request at 972-976).
  Verdict: teaches holds; scope holds; three range defects (truncated handler, overrun past 1003, unnamed 781-786).

### S500 — `include/linux/mman.h:61-84` (173-line copy)

```
61-84  first 61: 'extern int sysctl_overcommit_memory;'
       last  84: '}'
```

Interior lines:

```
61: extern int sysctl_overcommit_memory;
62: extern struct percpu_counter vm_committed_as;
65: extern s32 vm_committed_as_batch;
66: extern void mm_compute_batch(int overcommit_policy);
74: unsigned long vm_memory_committed(void);
76: static inline void vm_acct_memory(long pages)
78: \tpercpu_counter_add_batch(&vm_committed_as, pages, vm_committed_as_batch);
81: static inline void vm_unacct_memory(long pages)
83: \tvm_acct_memory(-pages);
84: }
```

- Scope ("`vm_acct_memory()` and `vm_unacct_memory()` … how the committed counter is charged and released") is held
  exactly: 76-79 charges, 81-84 releases through the same path, with the `percpu_counter`/batch declarations that
  make it a per-CPU counter.
- `teaches` first clause is held: "a per-CPU counter charged and released by batched adds" (62, 65, 78). The last
  clause, "so a cheap read of it is approximate", is **not stated in 61-84**: the approximation and the batch
  deviation are stated in `mm/util.c` (`/ * The deviation of sync_overcommit_as could be big with loose policy * /`,
  813-823) and the cheap read is `percpu_counter_read_positive()` at 994 — S499's anchor, not S500's.
- Verdict: anchor holds; teaches is one clause wider than its own anchor (the clause is true and supported by the
  copy set, just not by this row's range).

### S501 — `mm/mmap.c:546-558,1585-1619` (1921-line copy)

```
546-558   first 546: '\t/*'
          last  558: '\t}'
1585-1619 first 1585: ' *'
          last  1619: 'subsys_initcall(init_admin_reserve);'
```

Interior lines:

```
546: \t/*
547: \t * Set 'VM_NORESERVE' if we should not account for the
548: \t * memory use of this mapping.
550: \tif (flags & MAP_NORESERVE) {
551: \t\t/* We honor MAP_NORESERVE if allowed to overcommit */
552: \t\tif (sysctl_overcommit_memory != OVERCOMMIT_NEVER)
553: \t\t\tvm_flags |= VM_NORESERVE;
555: \t\t/* hugetlb applies strict overcommit unless MAP_NORESERVE */
556: \t\tif (file && is_file_hugepages(file))
557: \t\t\tvm_flags |= VM_NORESERVE;
1579: /*
1580:  * Initialise sysctl_user_reserve_kbytes.
1582:  * This is intended to prevent a user from starting a single memory hogging
1583:  * process, such that they cannot recover (kill the hog) in OVERCOMMIT_NEVER
1586:  * The default value is min(3% of free memory, 128MB)
1587:  * 128MB is enough to recover with sshd/login, bash, and top/kill.
1589: static int init_user_reserve(void)
1593: \tfree_kbytes = K(global_zone_page_state(NR_FREE_PAGES));
1595: \tsysctl_user_reserve_kbytes = min(free_kbytes / 32, SZ_128K);
1598: subsys_initcall(init_user_reserve);
1600: /*
1601:  * Initialise sysctl_admin_reserve_kbytes.
1606:  * Systems with more than 256MB will reserve 8MB, enough to recover
1610: static int init_admin_reserve(void)
1616: \tsysctl_admin_reserve_kbytes = min(free_kbytes / 32, SZ_8K);
1619: subsys_initcall(init_admin_reserve);
```

- `546-558` holds "MAP_NORESERVE handling in do_mmap()" completely (comment 546-549, block 550-558).
- `1585-1619` holds "the boot-time user and admin reserve initialisers" (1589-1597, 1610-1618 + their
  `subsys_initcall`s). It **starts inside** the `init_user_reserve` comment: 1585 is a bare ` *`, and the comment
  head that says what the reserve is for (1579-1584, "This is intended to prevent a user from starting a single
  memory hogging process … in OVERCOMMIT_NEVER mode") is outside the range. Cosmetic-but-real: the range's first
  line is a comment-continuation line with no opening.
- `teaches` ("MAP_NORESERVE is honoured outside mode 2, hugetlb files keep it in every mode, and the reserves start
  at min(free/32, 128 MiB or 8 MiB)") is held: 552-553, 556-557, 1595 and 1616. The unit reading is correct —
  `sysctl_*_reserve_kbytes` is in kilobytes (it is shifted by `PAGE_SHIFT - 10` before use, `mm/util.c:983,989`),
  so `SZ_128K` and `SZ_8K` stored into it are 128 MiB and 8 MiB, matching the "128MB"/"8MB" comments at
  1586-1587 and 1606. No overclaim. Verdict: teaches holds; scope holds; one cosmetic range-head defect.

## 3. Proposed exact replacement anchor cells

Only the listed-line numbers change (the `tag v7.2` and `copy … sha256 …` suffixes stay byte-identical). Proposals
are text for the L1 to apply if it agrees; I edited nothing. Each proposal is justified by the printed lines above.

S497 (`corpus/SOURCES.md:276`) — current line list `7-28,33-37,45,54-64,83-84`; proposed:

```
overcommit-accounting.rst:7-29,33-38,48,54-64,83-85; tag v7.2; copy corpus/evidence/sources-r52/overcommit-accounting.rst.v7.2 sha256 767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f
```

- `7-28` → `7-29` (mode 2's paragraph ends at 29, "initialize every page.").
- `33-37` → `33-38` (the sentence closes at 38, which names `CommitLimit` and `Committed_AS`).
- `45` → `48` (45 is the stack-growth gotcha; 48 is the mode-2 rule "In mode 2 the MAP_NORESERVE flag is ignored.").
- `83-84` → `83-85` (the only "listed gap" is line 85, "Account ptrace pages (this is hard)").

S498 (`corpus/SOURCES.md:277`) — **no change**; `vm.rst:84-97,825-833,836-858,861-866,1029-1046`.

S499 (`corpus/SOURCES.md:278`) — current `mm/util.c:781-786,806-834,901-1006`; proposed:

```
mm/util.c:781-786,806-840,901-1003; tag v7.2; copy corpus/evidence/sources-r52/util.c.v7.2 sha256 e702754c45bd7bd69e5da22a6505c9c1016eaafe6e883b746cc3cdbd413ebe7c
```

- `806-834` → `806-840` (whole `overcommit_policy_handler`, including `} else {` at 835 and `return ret;` at 839).
- `901-1006` → `901-1003` (ends at the closing brace of `__vm_enough_memory`; 1005-1006 belong to `get_cmdline()`).

With that anchor, the row's `scope` cell should also name the block it cites at 781-786. Proposed scope text:

```
vm_commit_limit(), vm_memory_committed(), __vm_enough_memory(), the overcommit policy handler and the compiled-in sysctl defaults at v7.2
```

S500 (`corpus/SOURCES.md:279`) — **no anchor change**; `include/linux/mman.h:61-84`. Optional `teaches` tightening so
every clause is held by this row's own range (the approximation sentence belongs to S499's `mm/util.c:813-823`
comment and `:994`):

```
The committed total is a per-CPU counter charged and released by batched adds against vm_committed_as_batch, so it is not one global variable and a read has to account for per-CPU batching.
```

S501 (`corpus/SOURCES.md:280`) — current `mm/mmap.c:546-558,1585-1619`; proposed:

```
mm/mmap.c:546-558,1579-1619; tag v7.2; copy corpus/evidence/sources-r52/mmap.c.v7.2 sha256 449b858385c7ece0ff88a8b41893efadb70a437fb8585a296c4ef0461a4c1545
```

- `1585` → `1579` (start at the `/*` that opens `init_user_reserve`'s comment; 1585 is a bare ` *`).

Optional, style only (not drift): S497 and S498 use bare basenames (`overcommit-accounting.rst:`, `vm.rst:`) while
S499-S501 use repo-relative paths (`mm/util.c:`, `include/linux/mman.h:`, `mm/mmap.c:`). No other row in the
registry is ambiguous because each row's URL fixes the path, so I do not propose it.

## 4. What this check does not establish (UNVERIFIED)

- Upstream equality. I did not fetch
  `https://raw.githubusercontent.com/torvalds/linux/v7.2/...`; I verified only that the five copies hash to the
  digests in the anchor cells and in the frozen `COPIES` table (`count-c2.py:49-60`) — internal consistency, not
  that the copies are the v7.2 bytes. The entry's own `recheck:` command is the network check.
- That the entry's claims are right. My seat reads scope/teaches against the cited ranges; the quotes themselves
  were located by the counter (`c2-at-data.txt`: `located=28 quote_missing=0`) and judged by the ENTAILMENT seats.
- Counter weakness (named here as a round-53 routing item, not a proposal): `count-c2.py` validates a sources row
  only through cells 1, 7, 8 and 10 plus `len(srow) == 11` (`count-c2.py:226-228`); **cell 5 (`anchor`) is never
  read**, so none of the four ranges I found defective can make this claim unmet. The same holds for the `scope`
  and `teaches` cells. An anchor that points a reader at the wrong lines is invisible to C2 as scored.
- No host read was needed for this item; nothing here depends on this host's sysctl values.

## 5. Receipts

```
$ mkdir -p /fast/scratch/hyaku/mori-r52/Mo52ExecAnchorCheck/tmp && export TMPDIR=$PWD/tmp        # exit 0
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 8524904...:corpus/SOURCES.md | sed -n '276,280p'
    # the five rows, 11 cells each (output in §1/§2)                                               # exit 0
$ cd corpus/evidence/sources-r52 && sha256sum *.v7.2 && wc -l *.v7.2                              # exit 0, §1
$ awk 'NR==45||NR==48 ...' overcommit-accounting.rst.v7.2 / util.c.v7.2 / mmap.c.v7.2             # exit 0, §2
$ git -C ... diff --stat 8524904adb25e44f24d9f25aac7eae909625c18c HEAD -- corpus/SOURCES.md corpus/evidence/sources-r52
    # empty: no later commit touched my surface                                                   # exit 0
$ rm -rf /fast/scratch/hyaku/mori-r52/Mo52ExecAnchorCheck                                          # exit 0
```

Tooling installed or upgraded: none (no pacman, no network). Lane writes: this report only. Lane git/jj state
untouched (`git show` / `git diff` / `git rev-parse` only).

## Findings

1. **MED — S497 anchor line `45` points at the stack-growth gotcha, not at anything the row claims.**
   `corpus/SOURCES.md:276` (anchor cell), copy `corpus/evidence/sources-r52/overcommit-accounting.rst.v7.2:45`:
   `largest size you think you will need. For typical stack usage this does`. Neither `scope` nor `teaches` mentions
   stack growth or `mremap`; the mode-2 rule the row needs is line 48, `In mode 2 the MAP_NORESERVE flag is ignored.`
   Proposed: `45` → `48`.

2. **MED — S497 anchor `83-84` omits the only listed gap, so "the listed gaps" in `scope` is not held.**
   `corpus/SOURCES.md:276`; copy lines `83: To Do`, `84: =====`, `85: * Account ptrace pages (this is hard)`. The
   entry's own ptrace claim quotes 83-85. Proposed: `83-84` → `83-85`.

3. **MED — S499 anchor `901-1006` overruns `__vm_enough_memory` into `get_cmdline()`'s kernel-doc.**
   `corpus/SOURCES.md:278`; copy `util.c.v7.2:1003` is the function's closing brace, 1004 is blank, and
   `1005-1006` are `/**` and ` * get_cmdline() - copy the cmdline value to a buffer.` Proposed: `901-1006` →
   `901-1003`.

4. **LOW — S499 anchor `806-834` truncates `overcommit_policy_handler` mid-branch.**
   `corpus/SOURCES.md:278`; the handler is 806-840, and 835-840 (`} else {`, `proc_dointvec_minmax`,
   `return ret;`, closing brace) are outside the range. Proposed: `806-834` → `806-840`.

5. **LOW — S499 cites `781-786` (compiled-in sysctl defaults) but its `scope` cell does not describe that block.**
   `corpus/SOURCES.md:278` scope cell vs lines `782: sysctl_overcommit_ratio … = 50`, `785-786: user/admin
   reserve defaults`. The lines are warranted (the entry quotes 782); the scope is short. Proposed scope text in
   §3.

6. **LOW — S497 ranges `7-28` and `33-37` end mid-sentence.** `corpus/SOURCES.md:276`; mode 2's paragraph closes
   at 29 ("initialize every page.") and the meminfo sentence closes at 38 (`CommitLimit` / `Committed_AS` — the
   entry's subject). Proposed: `7-29` and `33-38`.

7. **LOW — S501 anchor `1585-1619` starts on a bare ` *` inside `init_user_reserve`'s comment.**
   `corpus/SOURCES.md:280`; the comment opens at 1579-1580 ("Initialise sysctl_user_reserve_kbytes … intended to
   prevent a user from starting a single memory hogging process"). Proposed: `1585-1619` → `1579-1619`.

8. **LOW — S500 `teaches` last clause is not held by its own anchor.** `corpus/SOURCES.md:279` +
   `include/linux/mman.h:61-84`: the range gives the per-CPU counter and the batch variable, but "a cheap read of
   it is approximate" is stated in `mm/util.c:813-823` and performed by `percpu_counter_read_positive()` at
   `util.c:994` (S499's range). Optional `teaches` wording in §3.

9. **MED (routed to round 53, not a fix for this round) — the C2 counter never reads the `anchor` cell, so no
   anchor defect can register.** `.ufo/waves/round-52/count-c2.py:226-228`: `row_ok` tests `len(srow) == 11`, the
   URL in cell 1, `mined`, the opened date and the `used-by` cell only; `scope` (4), `anchor` (5) and `teaches` (6)
   are unread. All four anchor defects above (findings 1-4) are therefore invisible in
   `C2=met … source_rows=ok`. Named limit for the report; routing item for the successor freeze.

10. **LOW (no action taken) — rows S497-S501 are shape-clean.** `corpus/SOURCES.md:276-280` at 8524904: 11 cells
    each, 0 leading spaces, `mined`, opened `2026-10-26`, `used-by` exactly
    `corpus/knowledge/overcommit-commit-limit-r52.md`, `tag v7.2` plus a `copy … sha256` digest that matches the
    copy on disk and the frozen `COPIES` table. Recorded so the L1 can see the parts that need no change.
