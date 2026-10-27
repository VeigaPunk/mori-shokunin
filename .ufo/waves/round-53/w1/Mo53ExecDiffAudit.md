# Mo53ExecDiffAudit — per-row enclosing-function/section diff, v7.2 copy vs v7.3 copy

Seat: `Mo53ExecDiffAudit` (executor, leaf). Round-53 wave `w1`. Data under audit:
`2a4213bf8da72f7cd78189baa5bb9be825dca1df` (`round-53: data — v7.3 recheck ledger (C1), …`).
Entering tip `20edafa59b38dac1ca358893f0259b1f436372d3`. Lane HEAD when this seat ran:
`95cf78eef71979f9b740ef6bc3c5299b6beff86e`.

**This is input for the RECHECK voters' attackers, not a vote.** No line in this report is a
vote; the twelve RECHECK seats decide the dispositions. Nothing here was written into the lane
except this file.

## What was measured

Assignment: for each of the 46 ledger rows, locate the v7.2 quote's line in the v7.2 copy and the
enclosing function/section; `diff -u` that unit between the v7.2 copy and the v7.3 copy; list the
rows whose enclosing unit changed, with the hunk.

Method (all read-only; scripts in `/fast/scratch/hyaku/mori-r53/Mo53ExecDiffAudit/`):

1. **Quote location.** Each row's *v7.2* quote (from `evidence/c1-claims.txt`, the v7.2 text even
   for the two `absent` rows) is searched in the committed v7.2 copy with whitespace collapsed
   exactly as the counter does, but through a character→line map, giving the quote's exact line
   span. **Every one of the 46 quotes occurs exactly once** in its v7.2 copy (`occ72=1` for all
   46), so there is no locator ambiguity to resolve.
2. **Enclosing unit.** For `*.c`/`*.h`, top-level blocks found from a comment- and string-aware
   brace-depth scan (kernel multi-line headers handled: the declaration start is walked back over
   signature continuation lines), and the unit is the function whose body contains the quote; a
   kernel-doc comment directly above the function is included in the unit. A quote that straddles
   a comment's closing `*/` and the code after it is assigned to the **function**, not the comment
   (overlap-maximal choice, function preferred on ties). For `*.rst`, the unit is the reST section
   (heading + underline, extent to the next heading of the same or higher level).
3. **Counterpart in v7.3.** Same function name / section title / global identifier in the v7.3
   copy — not a line-number guess, because line numbers move: `user_reserve_kbytes` shifts
   +77 lines (1029 → 1106), `init_user_reserve` −23 (1579 → 1556), the `overcommit_*` sections
   −2, `meminfo` and `si_mem_available` +1.
4. **Diff.** `diff -u` of the two unit bodies (GNU diffutils 3.12 via `/usr/bin/diff`; note that
   `diff` is a *shell builtin* in this shell that emits a git-style diff — `/usr/bin/diff` was
   used explicitly for every comparison, and both give identical changed-line counts).

Two independent cross-checks were run and both agree with the unit-diff on all 46 rows:

- **Containment**: whole-file `diff -u` changed-line sets intersected with each row's unit range
  (`agree=46 disagree=0`).
- **Re-derivation on independently fetched bytes**: all nine v7.2 and all nine v7.3 files were
  re-fetched from `git.kernel.org` cgit `?h=v7.2` / `?h=v7.3` and every one is **byte-identical**
  (sha256) to the committed copies; the whole audit was then re-run against the re-fetched bytes
  and produced the identical per-row answer.

## Result: 2 of 46 rows have a changed enclosing unit

Only **rows 34 and 37** (`0fbd62f51ce8`, `d7a1dc88dcb3`, `mm/mmap.c`, unit `do_mmap`) sit in a
function whose text differs at all between v7.2 and v7.3. The other **44 rows' enclosing function
or section is byte-identical** between the two tags.

### Row 34 `0fbd62f51ce8` — `mm/mmap.c`, unit `do_mmap` (v7.2 lines 279–566 → v7.3 lines 280–579)

Quote (v7.2 lines 551–553): `We honor MAP_NORESERVE if allowed to overcommit */ if
(sysctl_overcommit_memory != OVERCOMMIT_NEVER) vm_flags |= VM_NORESERVE;`

The unit diff is large (34 whole-file hunks, 190 changed lines in this file). The hunk that
contains the quote:

```diff
@@ -266,22 +278,22 @@
 	/*
-	 * Set 'VM_NORESERVE' if we should not account for the
-	 * memory use of this mapping.
+	 * Set VMA_NORESERVE_BIT if we should not account for the memory use
+	 * of this mapping.
 	 */
 	if (flags & MAP_NORESERVE) {
 		/* We honor MAP_NORESERVE if allowed to overcommit */
 		if (sysctl_overcommit_memory != OVERCOMMIT_NEVER)
-			vm_flags |= VM_NORESERVE;
+			vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);
 
 		/* hugetlb applies strict overcommit unless MAP_NORESERVE */
 		if (file && is_file_hugepages(file))
-			vm_flags |= VM_NORESERVE;
+			vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);
 	}
 
-	addr = mmap_region(file, addr, len, vm_flags, pgoff, uf);
+	addr = mmap_region(file, addr, len, vma_flags, pgoff, uf);
```

The rest of the `do_mmap` diff is the `vm_flags_t` → `vma_flags_t` conversion: the parameter
becomes `vma_flags_t vma_flags`, `vm_flags |=` / `vm_flags &= ~` become
`vma_flags_set(...)` / `vma_flags_clear(...)`, `vm_flags & X` becomes `vma_flags_test(&vma_flags,
X_BIT)`, the `MAP_DROPPABLE` case gains a `vma_flags_t droppable = VMA_DROPPABLE;` local so
`VM_DROPPABLE == VM_NONE` can be spelled `vma_flags_empty(&droppable)`, and the kernel-doc
`@vm_flags` parameter is respelled `@vma_flags` (default now `EMPTY_VMA_FLAGS`). Nine of the
file's 34 hunks fall inside `do_mmap`; the other 25 touch functions whose bodies also changed —
`__get_unmapped_area`, `arch_get_unmapped_area`, `arch_get_unmapped_area_topdown`,
`generic_get_unmapped_area`, `generic_get_unmapped_area_topdown`, `mm_get_unmapped_area`,
`mm_get_unmapped_area_vmflags`, `__install_special_mapping`, `vm_brk_flags`, `dup_mmap`,
`tear_down_vmas`, `special_mapping_split`, `stack_guard_placement`, `vma_set_page_prot`,
`check_brk_limits`, `find_extend_vma_locked`, `mmap_read_lock_maybe_expand`,
`SYSCALL_DEFINE1`, `SYSCALL_DEFINE5`. `mmap_region` is *called* from `do_mmap` but not defined
in `mm/mmap.c`, so its own body is outside this comparison.

### Row 37 `d7a1dc88dcb3` — `mm/mmap.c`, unit `do_mmap` (same unit, different quote lines)

Quote (v7.2 lines 555–557): `hugetlb applies strict overcommit unless MAP_NORESERVE */ if (file &&
is_file_hugepages(file)) vm_flags |= VM_NORESERVE;`

Same unit and the same hunk as row 34 (the two quotes are 4 lines apart inside the same
`if (flags & MAP_NORESERVE)` block); the hugetlb condition `if (file && is_file_hugepages(file))`
is unchanged, and its body becomes `vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);`. The two rows
share one diff; no separate hunk exists.

**Both rows are exactly the two rows the ledger already records as `status=absent`.** The
*enclosing unit changed* and the *quote no longer occurs* are the same fact here: the respelling
`vm_flags |= VM_NORESERVE` → `vma_flags_set(&vma_flags, VMA_NORESERVE_BIT)` is the change.

## The other 44 rows: enclosing unit byte-identical

Grouped by file, with the unit and the v7.2/v7.3 line ranges that were compared:

| rows | path | unit | unit lines v7.2 → v7.3 | changed |
|---|---|---|---|---|
| 1, 2, 3, 4, 5 | `Documentation/filesystems/proc.rst` | section `meminfo` | 1042–1302 → 1043–1303 | no |
| 6, 8 | `fs/proc/meminfo.c` | `meminfo_proc_show` | 33–178 → 33–178 | no |
| 7 | `fs/proc/meminfo.c` | `show_val_kb` | 27–32 → 27–32 | no |
| 9, 10 | `include/linux/mm_inline.h` | `folio_is_file_lru` + its kernel-doc | 13–31 → 13–31 | no |
| 11–18 | `mm/show_mem.c` | `si_mem_available` | 31–72 → 32–73 | no |
| 19 | `Documentation/admin-guide/sysctl/vm.rst` | section `user_reserve_kbytes` | 1029–1048 → 1106–1125 | no |
| 20, 21 | `…/sysctl/vm.rst` | section `overcommit_memory` | 836–860 → 834–858 | no |
| 22 | `…/sysctl/vm.rst` | section `overcommit_kbytes` | 825–835 → 823–833 | no |
| 23 | `…/sysctl/vm.rst` | section `admin_reserve_kbytes` | 84–112 → 82–110 | no |
| 24 | `…/sysctl/vm.rst` | section `overcommit_ratio` | 861–868 → 859–866 | no |
| 25, 26, 27, 30 | `Documentation/mm/overcommit-accounting.rst` | section `Overcommit Accounting` | 2–39 → 2–39 | no |
| 28 | `…/overcommit-accounting.rst` | section `To Do` | 83–86 → 83–86 | no |
| 29 | `…/overcommit-accounting.rst` | section `Gotchas` | 40–50 → 40–50 | no |
| 31 | `…/overcommit-accounting.rst` | section `How It Works` | 51–68 → 51–68 | no |
| 32 | `include/linux/mman.h` | `vm_acct_memory` | 75–79 → 75–79 | no |
| 33 | `include/linux/mman.h` | `vm_unacct_memory` | 80–84 → 80–84 | no |
| 35 | `mm/mmap.c` | `init_user_reserve` | 1579–1597 → 1556–1574 | no |
| 36 | `mm/mmap.c` | `init_admin_reserve` | 1600–1618 → 1577–1595 | no |
| 38, 44 | `mm/util.c` | `vm_commit_limit` | 901–916 → 901–916 | no |
| 39 | `mm/util.c` | `overcommit_policy_handler` | 805–840 → 805–840 | no |
| 40, 41, 42, 45, 46 | `mm/util.c` | `__vm_enough_memory` | 943–1003 → 943–1003 | no |
| 43 | `mm/util.c` | file-scope decl `sysctl_overcommit_ratio` | 782 → 782 | no |

Note on ranges: the *line numbers* move (`vm.rst` inserts 79 lines for the new
`panic_on_unrecoverable_memory_failure` section but also drops 3 and adds 1 in the preamble, so
`user_reserve_kbytes` lands at +77; `mmap.c` `init_*_reserve` shift by −23; `show_mem.c`
`si_mem_available` by +1) but the *unit text* is identical. A line-number-based reader would see
"changed" where the text is the same; this audit matches by unit name.

## Stronger-than-`held` result (for the attackers)

The counter's named limit says `held` proves the words still occur *somewhere* in the v7.3 file,
not at the same place. Measured directly:

- **44 of 46 rows**: the v7.2 quote still occurs **inside the row's own enclosing unit** in v7.3
  (`within_unit=True`). This is a strictly stronger property than the counter's `held`.
- **2 of 46 rows** (34, 37): the v7.2 quote does not occur anywhere in the v7.3 copy — those are
  the counter's two `absent` rows. The ledger's substitute v7.3 quote for each does occur exactly
  once in the v7.3 copy (asserted separately).

## Independent re-derivation of the ledger's `status` column

Parsing the ledger table and re-deriving `held`/`absent` from the committed copies independently
of `count-c1.py`: **46/46 reproduce the ledger's status** (`status_ok=46`, `status_bad=0`). No
quote has a locator ambiguity (each v7.2 quote occurs once in v7.2). The two `absent` rows are
exactly the two whose enclosing unit changed.

## The ledger's per-file change table — reproduced

The ledger's "What changed between v7.2 and v7.3" line counts were re-measured with the entry's
own stated formula (`diff -u <v7.2 copy> <v7.3 copy> | grep -c '^[-+][^-+]'`):

| path | ledger | measured | verdict |
|---|---|---|---|
| `Documentation/filesystems/proc.rst` | 3 | 3 (1 del / 2 add) | matches |
| `mm/show_mem.c` | 22 | 22 (9 / 13) | matches |
| `include/linux/mm_inline.h` | 49 | 49 (47 / 2) | matches |
| `Documentation/admin-guide/sysctl/vm.rst` | 64 | 64 (2 / 64) | matches |
| `mm/util.c` | 14 | 14 (7 / 7) | matches |
| `mm/mmap.c` | 190 | 190 (103 / 87) | matches |
| `Documentation/mm/overcommit-accounting.rst` | byte-identical | 0 changed lines, same sha256 | matches |
| `fs/proc/meminfo.c` | byte-identical | 0 changed lines, same sha256 | matches |
| `include/linux/mman.h` | byte-identical | 0 changed lines, same sha256 | matches |

The ledger's "six of the nine files changed" is correct, and so are the three it calls
byte-identical.

The ledger's *qualitative* descriptions of where those changes are also hold, verified per hunk:

- `proc.rst`: the 3 lines are at v7.2 513 (a duplicated word "page page" → "page" in the
  `/proc/pid/smaps` "shared"/"private" paragraph) and 608 (a new `ur` userfaultfd
  read-write-protect flag row in the `smaps` VmFlags legend table) — both **outside** the
  `meminfo` section (1042–1302), as the ledger says.
- `show_mem.c`: an added `#include "page_alloc.h"` in the include block (hunk at v7.2 line 16),
  `const nodemask_t *` on
  `show_mem_node_skip` / `show_free_areas` / `__show_mem`, and printk unit fixes
  (`%luKB`→`%lukB`, `%ukB`→`%lukB`, a `(unsigned long)` cast, `%ld`→`%lu`). `si_mem_available`
  and `si_meminfo` are byte-identical, as the ledger says.
- `mm_inline.h`: removes the uffd-wp helper `pte_install_uffd_wp_if_needed` (53 lines) and
  changes `memdesc_section(cur_page->flags)` → `memdesc_section(&cur_page->flags)` in
  `num_pages_contiguous`. `folio_is_file_lru` and its kernel-doc are byte-identical.
- `vm.rst`: drops the `mm/swap.c` pointer sentence from the preamble, adds
  `panic_on_unrecoverable_memory_failure` to the index list, and adds that section (79 lines)
  between `panic_on_oom` and `percpu_pagelist_high_fraction`. **No `overcommit_*`,
  `admin_reserve_kbytes` or `user_reserve_kbytes` section text changed.**
- `util.c`: `vm_mmap_pgoff` (the `do_mmap(..., 0, ...)` argument → `EMPTY_VMA_FLAGS`),
  `vm_mmap_shadow_stack` (`vm_flags_t`→`vma_flags_t`), and `compat_set_desc_from_vma` /
  `call_vma_mapped` (`vma->vm_pgoff` → `vma_start_pgoff(vma)`). `vm_commit_limit`,
  `__vm_enough_memory`, `overcommit_policy_handler` and the `sysctl_overcommit_*` globals are
  byte-identical.
- `mmap.c`: the `vm_flags_t` → `vma_flags_t` conversion across 34 hunks, including the
  `MAP_NORESERVE` block (rows 34, 37).

The ledger's `Reading rules` pointer `mmap.c.v7.3:563-571` is **correct**: lines 563–571 of the
v7.3 copy are exactly the `if (flags & MAP_NORESERVE) { … }` block with both
`vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);` writes and the same two guard conditions.

## Indirect-dependency check (does "unit unchanged" hide a behaviour change?)

Two further checks beyond the unit text, both negative:

- **Same-file call graph**: for each of the nine files, the set of functions whose body changed
  was computed. **Zero** of the 44 unchanged-unit rows call, from inside its own unit, a function
  whose body changed in the same file. Changed bodies, exhaustively: `mm/mmap.c` —
  `SYSCALL_DEFINE1`, `SYSCALL_DEFINE5`, `__get_unmapped_area`, `__install_special_mapping`,
  `arch_get_unmapped_area`, `arch_get_unmapped_area_topdown`, `check_brk_limits`, `do_mmap`,
  `dup_mmap`, `find_extend_vma_locked`, `generic_get_unmapped_area`,
  `generic_get_unmapped_area_topdown`, `mm_get_unmapped_area`, `mm_get_unmapped_area_vmflags`,
  `mmap_read_lock_maybe_expand`, `special_mapping_split`, `stack_guard_placement`,
  `tear_down_vmas`, `vm_brk_flags`, `vma_set_page_prot`; `mm/util.c` — `vm_mmap_pgoff`,
  `vm_mmap_shadow_stack`, `compat_set_desc_from_vma`, `call_vma_mapped`; `mm/show_mem.c` —
  `__show_mem`, `show_free_areas`, `show_mem_node_skip`; `include/linux/mm_inline.h` —
  `pte_install_uffd_wp_if_needed` (removed), `num_pages_contiguous`; `fs/proc/meminfo.c` and
  `include/linux/mman.h` — none. `mmap_region` is not defined in `mm/mmap.c`, so it cannot appear
  in this set; only its call site inside `do_mmap` changed.
- **Cross-file call graph**: **zero** rows call a function whose body changed in a *different*
  one of the nine files. The 25 rows that call any nine-file function call only unchanged ones —
  e.g. `__vm_enough_memory` calls `vm_acct_memory`, `vm_unacct_memory` and `vm_commit_limit`,
  each byte-identical between the two copies; `meminfo_proc_show` calls `si_meminfo`,
  `si_mem_available`, `show_val_kb`, `vm_commit_limit` and `vm_memory_committed`, each
  byte-identical.

So nothing in the nine re-opened files contradicts a `holds` disposition for rows other than
34/37 through an indirect call either. This is *not* a semantic vote: it says the code the quotes
call did not change; it does not say the words still mean what the claim says.

## Not checked / limits of this seat

- The nine files are the whole corpus this seat was given. A callee defined **outside** the nine
  (e.g. `global_node_page_state` in `mm/vmstat.c`, `percpu_counter_add_batch` in
  `lib/percpu_counter.c`, `low_wmark_pages`, `totalram_pages`) was not re-opened at v7.3 and its
  stability is **UNVERIFIED** here. The two `mm_inline.h` rows (9, 10) and the two `mman.h` rows
  (32, 33) rest on header text whose *definitions* are outside the nine.
- The unit is the *enclosing* function/section. A change in a sibling function, a global, a
  header enum or a `#define` used by an unchanged unit would not appear in the unit diff; the two
  call-graph checks above test only direct calls by name inside the unit.
- I did not fetch `v7.3` for the three files outside the nine that the ledger cites for C2
  (rows S511–S513) — not in this seat's scope.
- Semantic equivalence of `vm_flags |= VM_NORESERVE` and
  `vma_flags_set(&vma_flags, VMA_NORESERVE_BIT)` is **for the voters to judge**; this seat only
  reports that the enclosing text changed and where.

## Scratch and housekeeping

Scratch: `/fast/scratch/hyaku/mori-r53/Mo53ExecDiffAudit/` (scripts `audit3.py`,
`crosscheck.py`, `statuscheck.py`, `withinunit.py`, `callgraph.py`, `xfile.py`, `depcheck.py`;
outputs `results.json`, `crosscheck.json`, `statuscheck.json`, `withinunit.json`; 18 re-fetched
source files under `refetch/`). `disk-guard.sh status` was checked before the run (rc 0;
`/fast/scratch/hyaku` 24 % used, 615.2 GB free). Bounded fetches only: 18 single-file cgit
`plain/` requests, no clones, no mirrors. Nothing written under `/tmp`, nothing written to
`~/.local/bin` or any PATH directory, no `pacman`, no git/jj mutation, no file created inside
the lane outside this report. Scratch directory removed at the end of the run.

Tools installed or upgraded: none.

## Findings

- **Note (no severity — positive result, the assignment's headline)** — `corpus/knowledge/kernel-v7.3-recheck-r53.md`,
  ledger rows 1–46: the enclosing function/section changed for exactly **two rows, 34
  (`0fbd62f51ce8`) and 37 (`d7a1dc88dcb3`)**, both `mm/mmap.c` unit `do_mmap`; the other 44
  rows' enclosing unit is byte-identical between the v7.2 and v7.3 committed copies. The two
  changed rows are exactly the ledger's two `status=absent` rows.
- **LOW** — `corpus/knowledge/kernel-v7.3-recheck-r53.md`, "What changed between v7.2 and v7.3"
  table, `mm/util.c` row: the "where" cell names only `vm_mmap_pgoff` and the shadow-stack
  helper, but `mm/util.c` has four changed regions — the other two convert `vma->vm_pgoff` to
  `vma_start_pgoff(vma)` in `compat_set_desc_from_vma` (v7.2 line 1188) and `call_vma_mapped`
  (v7.2 line 1379). The 14-line count is correct; only the prose is incomplete. No ledger row's
  enclosing unit is affected (all `util.c` row units are byte-identical), so this is a wording
  gap, not a claim defect.
- **LOW** — `corpus/knowledge/kernel-v7.3-recheck-r53.md`, "What changed" table: the `mmap.c`
  cell says the change is "the `vm_flags_t` → `vma_flags_t` conversion, including the
  `MAP_NORESERVE` block". True but under-stated for the attackers' purpose: 20 named functions
  in `mm/mmap.c` changed body, 34 hunks, 190 changed lines (103 removed / 87 added), including
  the `MAP_DROPPABLE` case gaining a `vma_flags_empty(&droppable)` guard. A reader taking the
  cell as a complete inventory would under-estimate the surface around rows 34/37.
- **LOW (named limit for the report, not correctable data)** — `count-c1.py` `held`: `held` is
  "the words occur somewhere in the v7.3 file". Measured stronger: for 44/46 rows the v7.2 quote
  still occurs **inside the row's own enclosing unit**; for rows 34 and 37 it occurs nowhere.
  The counter cannot express this stronger property, so a quote that drifted into a different
  function would still read `held`. Routed to round 54 as a counter gap (frozen this round).
- **LOW (limit of this evidence, for the L1 to carry)** — the call-graph results
  ("no row's unchanged unit calls a function whose body changed") hold only within the nine
  files in `corpus/evidence/sources-r53/`. Callees defined outside them
  (`global_node_page_state`, `percpu_counter_add_batch`, `low_wmark_pages`, `totalram_pages`,
  the `VMA_*_BIT` / `VM_*` macros of `include/linux/mm.h`) were not re-opened at v7.3; the two
  `mm_inline.h` rows (9, 10) and the two `mman.h` rows (32, 33) are the ones most exposed to
  that gap.
- **Note (method hazard, no severity)** — `diff` is a *shell builtin* in this environment that
  emits a git-style diff; `grep -c '^[-+][^-+]'` over its output still gives the same counts here
  (verified against `/usr/bin/diff` for all nine files), but a future instrument that parses
  hunk headers (`^@@`) from the builtin's output would read nothing. `count-c1.py`/`count-c2.py`
  do not shell out to `diff`, so no counter is affected this round.

Report: .ufo/waves/round-53/w1/Mo53ExecDiffAudit.md
