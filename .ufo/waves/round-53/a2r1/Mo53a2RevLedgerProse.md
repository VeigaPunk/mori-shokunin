# Mo53a2RevLedgerProse — review of 34d97cd3eaea8c13b0f065afc52aac1e5cf518a5

Review scope: intro, `## What changed` table, line-count paragraph, `## Reading rules`, and `## Boundaries` of `corpus/knowledge/kernel-v7.3-recheck-r53.md`; ledger rows excluded except where needed to verify row numbering and enclosing functions/sections.

Evidence used: read the target from `git archive 34d97cd3eaea8c13b0f065afc52aac1e5cf518a5` into this seat's scratch; archive resolved to that commit. `uname -r` returned `7.2.11-arch1-1`. `evidence/sweeps.txt` line 19 records `c03c1a14507dfaf8b856c2608f9ac216021fc222 refs/tags/v7.3^{}`; the prose's `c03c1a14507d` prefix is correct. The two prior entries contain 21 (round 51) and 28 (round 52) claim rows, 49 total; round-51 rows 19–21 cite S496, the 2014 commit patch. The frozen scope file reports `scope=46`, and its ordered hashes match the ledger's 46 rows. Ledger rows 34 and 37 are the two `absent` rows.

Commands and observed results:

- For each corresponding v7.2/v7.3 copy, ran `diff -u <v7.2> <v7.3> | grep -c '^[-+][^-+]'` and `git diff --no-index --numstat <v7.2> <v7.3>`. Results: `proc.rst 3; 2/1`, `show_mem.c 22; 13/9`, `mm_inline.h 49; 2/55`, `vm.rst 64; 80/3`, `util.c 14; 7/7`, `mmap.c 190; 92/113`; `meminfo.c`, `overcommit-accounting.rst`, and `mman.h` each had diff count 0 and matching SHA-256 pairs. These agree with all listed counts (the line-count regex skips changed blank lines).
- Compared enclosing v7.2 functions/sections with v7.3 and diff hunk ranges. For the 46 rows, only rows 34 and 37 have quotes in a changed enclosing function/section: both are in `do_mmap`'s MAP_NORESERVE block. Rows 35–36 are in unchanged `init_user_reserve` and `init_admin_reserve`; the other mapped code functions and documentation sections are unchanged. Row 43 is a file-scope variable, not enclosed by a function/section. `si_mem_available`, `folio_is_file_lru`, `vm_commit_limit`, and `__vm_enough_memory` bodies compare identical across copies.
- The proc.rst hunks are in `1.1 Process-Specific Subdirectories`, not the `meminfo` section. vm.rst changes are in the introductory `/proc/sys/vm/` section and the new panic section; the cited overcommit/user/admin-reserve sections are unchanged.
- The table descriptions otherwise match the diffs: `proc.rst` typo correction and userfaultfd flag index; `show_mem.c` include, const nodemask parameters, two `%luKB`→`%lukB` format changes, `%ld`/`%lu` flips and cast; removal of `pte_install_uffd_wp_if_needed` and pointer-argument changes in both `memdesc_section` calls; vm.rst's new section/index and removed `mm/swap.c` sentence; util.c's named conversions; and mmap.c's vma-flags conversion, renamed function, and 38-line removal of `__install_special_mapping`. The `mmap.c.v7.3:563-571` pointer covers the MAP_NORESERVE block, and both condition expressions are unchanged from v7.2.

No tools were installed or updated. Scratch was removed before completion.

Report: `.ufo/waves/round-53/a2r1/Mo53a2RevLedgerProse.md`

## Findings

- **LOW — `corpus/knowledge/kernel-v7.3-recheck-r53.md:28`.** The `show_mem.c` description omits a third printk unit-format change: `local_pcp:%ukB` became `local_pcp:%lukB` (in addition to the two `%luKB`→`%lukB` changes). Replace the cell text `printk units (`%luKB` → `%lukB`)` with `printk units (`%luKB`/`%ukB` → `%lukB`)`.
- **LOW — `corpus/knowledge/kernel-v7.3-recheck-r53.md:29`.** “removal of the uffd-wp pte helper and two `memdesc_section(&cur_page->flags)` call sites” can state that the call sites were removed, but they remain and were rewritten to take `&cur_page->flags`. Replace with `removal of the uffd-wp pte helper and two call sites rewritten to `memdesc_section(&cur_page->flags)``.
