# Mo53CritLedgerProse — attack on `corpus/knowledge/kernel-v7.3-recheck-r53.md` prose

Report: .ufo/waves/round-53/w1/Mo53CritLedgerProse.md
Scope: overclaims and misreadable prose in the C1 ledger at `2a4213bf8da72f7cd78189baa5bb9be825dca1df`
(working-tree bytes identical to the data commit: sha256 `a71a5b15470a2b534a6e4d79643294941e3c3ee3d00e0ab1fb1335d3e3558eee`
both ways). The counters, controls and kill rules are frozen; nothing below proposes touching them.
Scratch used: `/fast/scratch/hyaku/mori-r53/Mo53CritLedgerProse/` (reads only; removed on exit).

## What survived attack (verified, no defect)

- All 46 ledger rows parse; every `quote` cell occurs whitespace-collapsed in its named v7.3 copy
  (independent re-derivation, python3 + `re.sub(r'\s+',' ')`: `rows parsed: 46`, `missing quotes: []`,
  `Counter({('held','holds'): 44, ('absent','holds'): 2})`).
- The two `absent` rows' v7.2 quotes genuinely do not occur at v7.3 (`old q1 still in v7.3: False`,
  `old q2 still in v7.3: False`), and the ledger's v7.3 respellings do occur (`q1/q2 in v7.3: True`,
  `sources-r53/mmap.c.v7.3:563-571` — the pointer `mmap.c.v7.3:563-571` in the reading-rules row is exact).
- Diff-size column is accurate per the ledger's own stated method
  (`diff -u | grep -c '^[-+][^-+]'`): 3 / 22 / 49 / 64 / 14 / 190 all reproduced; the three
  byte-identical files are byte-identical (`cmp -s`: meminfo.c, overcommit-accounting.rst, mman.h).
- `si_mem_available` body is byte-identical v7.2→v7.3 (extracted `long si_mem_available(void)` … `\n}`
  and compared: `True`); `folio_is_file_lru` sits at `mm_inline.h.v7.3:28`, before the first diff hunk
  (566), so "untouched" is right.
- "46 of 49" confirmed: `memavailable-estimate-r51.md` claim table has 21 rows of which 3 cite S496
  (the 2014 patch; lines 42–44), `overcommit-commit-limit-r52.md` has 28; 18+28=46.
- Boundaries' named entries exist with the stated recheck fields: `oom-tracepoints-r47.md` has
  `recheck: on-release`, `oom-memcg-stat-r50.md` has `recheck: 90d`. Host runs `7.2.11-arch1-1`, so
  "the host runs 7.2.11" is right.
- `MAP_DROPPABLE` exists in both copies (not a v7.3 novelty); the reserve-initialiser quotes survive
  in the heavily-edited `mmap.c.v7.3` (`sysctl_user_reserve_kbytes`/`sysctl_admin_reserve_kbytes`: True/True).
- `mmap.c.v7.3` itself supplies weak internal evidence for the disposition equivalence: `do_mmap`
  accumulates flags via repeated `vma_flags_set(&vma_flags, …)` calls (lines 409, 471, 511, 537,
  543-544, 566, 570), so the helper behaves as a set-bits operation on an accumulator — "the two
  conditions are the same" is supported as far as the committed copies allow. Caveat recorded under F5.

## Findings

### F1 — MED — `mm/mmap.c` "where" cell understates a non-mechanical diff (line 32)

The cell reads "the `vm_flags_t` → `vma_flags_t` conversion, including the `MAP_NORESERVE` block" as
the whole character of the 190-line diff. The committed diff also contains: deletion of the whole
`__install_special_mapping` helper (v7.2 `mmap.c:1447+`, 44 lines) while its caller
`_install_special_mapping` still exists at `mmap.c.v7.3:1481` (the helper's new home is outside the
nine fetched files — none of the r53 copies defines it); renames
`mm_get_unmapped_area_vmflags`/`thp_get_unmapped_area_vmflags` → `*_vmaflags` with changed signatures;
a `check_brk_limits` refactor introducing `is_def_locked`; a `memfd_check_seals_mmap(file, &vm_flags)`
→ `(file, &vma_flags)` call-site API change; and the `MAP_DROPPABLE` case's restructure
(`VM_DROPPABLE == VM_NONE` → `vma_flags_empty(&droppable)` plus `vma_flags_set_mask`). An operator
reading "conversion" will believe every hunk was mechanical; at least the helper deletion and the
renames are not provable from the fetched copies alone.

Fenced replacement for line 32's "where" cell:

```
| `mm/mmap.c` | 190 changed lines | mostly the `vm_flags_t` → `vma_flags_t` conversion, including the `MAP_NORESERVE` block; also the removal of the `__install_special_mapping` helper (its caller `_install_special_mapping` remains — new home outside the fetched files), `*_unmapped_area_vmflags` → `*_vmaflags` renames, a `check_brk_limits` refactor and the `MAP_DROPPABLE` case's restructure |
```

### F2 — MED — `include/linux/mm_inline.h` "where" cell omits the second edit (line 29)

Cell: "removal of the uffd-wp pte helper; `folio_is_file_lru` untouched". True but incomplete: the diff
also changes `num_pages_contiguous` — `memdesc_section(cur_page->flags)` → `memdesc_section(&cur_page->flags)`
in two places (4 changed lines), i.e. the helper now takes a pointer. Presented as part of a "what
changed" table it reads as exhaustive.

Fenced replacement for line 29's "where" cell:

```
| `include/linux/mm_inline.h` | 49 changed lines | removal of the uffd-wp pte helper (45 lines) plus a `memdesc_section` signature change in `num_pages_contiguous` (now takes `&folio->flags`); `folio_is_file_lru` untouched |
```

### F3 — MED — `mm/util.c` "where" cell omits two hunks and mischaracterises one (line 31)

Cell credits only "`vm_mmap_pgoff` and the shadow-stack helper (`vm_flags_t` → `vma_flags_t`)". The
committed diff has four hunks: the `vm_mmap_pgoff` change is `0` → `EMPTY_VMA_FLAGS` (a flag *value*
change riding the conversion, not a type change at the call site), the shadow-stack hunk, and two more
hunks converting `vma->vm_pgoff` to `vma_start_pgoff(vma)` (`util.c` ~1188 and ~1379), an accessor
wrapper whose inlining is asserted, not shown, by the fetched copy.

Fenced replacement for line 31's "where" cell:

```
| `mm/util.c` | 14 changed lines | `vm_mmap_pgoff` (`0` → `EMPTY_VMA_FLAGS`), the shadow-stack helper (`vm_flags_t` → `vma_flags_t`), and two `vma->vm_pgoff` → `vma_start_pgoff(vma)` reads; `vm_commit_limit`, `__vm_enough_memory` untouched |
```

### F4 — LOW — `mm/show_mem.c` "where" cell: "printk units" bundles three change classes (line 28)

The 22 lines are: one include, three `const nodemask_t *` signatures, and printk *format-string* fixes —
of which only the `%luKB` → `%lukB` pair is a unit fix; the rest are signedness (`%ld`/`%lu` swaps for
`global_node_page_state` and `atomic_long_read`) and a `(unsigned long)` cast. All printk-visible,
nothing load-bearing, but "units" mislabels the class.

Fenced replacement for line 28's "where" cell:

```
| `mm/show_mem.c` | 22 changed lines | an include, `const nodemask_t *` parameters, and printk format fixes (`%luKB` → `%lukB` units, `%ld`/`%lu` signedness, one cast); `si_mem_available` untouched |
```

### F5 — MED — reading-rules row 2 overstates what the copies prove (line 100)

"`v7.3` writes the `MAP_NORESERVE` decision with `vma_flags_set(&vma_flags, VMA_NORESERVE_BIT)` instead
of `vm_flags |= VM_NORESERVE`; the two conditions are the same" — the two *if-conditions* are indeed
byte-identical in the copies, and the accumulator pattern elsewhere in `do_mmap` supports OR-semantics
for `vma_flags_set`. But `vma_flags_set`, `vma_flags_t` and `VMA_NORESERVE_BIT` are not defined in any
of the nine fetched files (verified: `grep` over `sources-r53/` finds only call sites). A critic reader
cannot check the equivalence claim from the provenance trio alone; the entry should say so rather than
imply the equivalence is established fact.

Fenced replacement for line 100's "answer at v7.3" cell:

```
| Why do two round-52 quotes no longer match? | v7.3 writes the `MAP_NORESERVE` decision with `vma_flags_set(&vma_flags, VMA_NORESERVE_BIT)` instead of `vm_flags \|= VM_NORESERVE`. The two *conditions* are byte-identical in the copies; `vma_flags_set`'s set-bits semantics are inferred from its accumulator use inside `do_mmap` (its definition lives outside the nine fetched files), so the equivalence is the lane's reading, which the two votes carry | `mmap.c.v7.3:563-571` |
```

### F6 — MED — reading-rules row 1 answers "yes" wider than the recheck reached (line 99)

"May a reader still use the round-51/52 entries on a v7.3 kernel? — yes, row by row, as far as each
row's disposition says `holds`". Three ways to misread it as stronger than it is: (a) the *entries*
include prose outside the claim tables — Boundaries says that prose was not rechecked; (b) "each row's
disposition" silently excludes the three S496 rows, which carry no disposition; (c) a `holds` row whose
status is `absent` still quotes v7.2 bytes in the old entries, and this row does not say where the
respelled quote lives. Nothing in the row bounds it to v7.3 specifically, so "safe on any kernel" is
a reachable misreading.

Fenced replacement for lines 99's "answer at v7.3" cell:

```
| May a reader still use the round-51/52 entries on a v7.3 kernel? | Only the 46 claim-table rows were rechecked, at v7.3 only: rows whose disposition is `holds` (all 46 — including the two `absent` rows, whose claim holds under the new spelling quoted in the ledger; the v7.2 quote in the old entry is stale bytes there). The three S496 rows and all prose outside the tables were not rechecked; nothing here speaks to v7.4 or later | the ledger above |
```

### F7 — LOW — "which no release changes" mislabels why the 3 patch rows are out of scope (line 20)

"the other three cite the 2014 commit patch, which no release changes" — the patch *bytes* don't change,
but what a release can change is whether the commit's stated motivation still describes the kernel. The
rows are out of scope because a tag-diff recheck cannot move them, not because nothing about them ages.

Fenced replacement for the clause in line 20:

```
is read again against the same path at v7.3. The other three cite the 2014 commit's own patch bytes, so no tag can move their quotes and they sit outside this recheck — their *relevance* (does the 2014 motivation still describe the kernel) is a claim question no release diff answers.
```

### F8 — LOW — `status`/`disposition` legend invites "absent = claim failed" (line 39-44 prose)

The legend defines `absent` mechanically ("the v7.2 quote does not occur") and `disposition` separately,
but a skim reader will still pair `absent` with `changed`. One clause makes it unmissable.

Fenced replacement for the second sentence of the legend paragraph:

```
`disposition` says whether the claim, read against the v7.3 file, still holds (`holds`) or not (`changed`) — note `absent` is about the quote's bytes, not the claim: an `absent` row can carry `holds` when the rule survives under new spelling (the two `mmap.c` rows below are exactly that). It is the L1's reading at the data commit and is decided by two RECHECK votes per row from seats that did not write the row (`.ufo/waves/round-53/w1/Mo53Fr01.md`–`Mo53Fr12.md`).
```

### F9 — LOW — provenance trio: `recheck:` line and Boundaries omit two limits the contract names (lines 13, 105-108)

The `recheck:` line tells the next rechecker to fetch "each path" and run "the same ledger shape" but
never says the scope is the 46 rows of *these two tables* (a future reader could read it as
re-deriving over all v7.x-pinned entries), and neither the header nor Boundaries repeats the contract's
named limit that the copies are the L1's cgit fetches, pinned by sha256, not independently verified
against the tag. `verified-at: 2026-10-26` matches house convention (the other entries use the same
field) — noted, no defect.

Fenced replacement for the `recheck:` header line:

```
recheck: on-release — `python3 .ufo/waves/round-53/count-c1.py <rev>` re-derives every status below from the committed v7.3 copies (fetched by the L1 from cgit, pinned by sha256 in SOURCES, not independently re-verified against the tag); at the next tag, fetch each of the nine paths with `curl -fsSL 'https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/<path>?h=<tag>'`, add the copies and rows, and re-run the ledger over the same scope: the claim-table rows of `memavailable-estimate-r51.md` and `overcommit-commit-limit-r52.md` that cite a kernel file
```

Fenced addition for Boundaries (append after the first bullet):

```
- The `*.v7.3` copies are the L1's fetches from git.kernel.org cgit on 2026-10-26, pinned by sha256 in
  SOURCES; they are evidence of what cgit served, not independent verification that cgit served tag v7.3.
```

### F10 — LOW — "3 changed lines" method silently excludes blank-line churn (line 34)

`grep -c '^[-+][^-+]'` counts only non-blank changed lines (blank `+`/`-` lines start the second
character with nothing to exclude — actually they are *excluded* since a bare `+`/`-` matches `^-+`
then requires a non-`+-` char: bare `+` is 1 char and fails `[^-+]`, correct). The vm.rst diff adds a
79-line section yet counts 64 because the section's added blank lines (and the removed `---`… fine) are
skipped. The method is disclosed verbatim, so this is honest — but "changed lines" will read to most
operators as "diffstat lines". A half-sentence keeps it truthful.

Fenced replacement for line 34:

```
Line counts: `diff -u <v7.2 copy> <v7.3 copy> | grep -c '^[-+][^-+]'` over the round-51/52 copies and
`corpus/evidence/sources-r53/` — i.e. non-blank changed lines only (added/removed blank lines are not counted).
```

## Routed items for round 54 (named limits, not counter fixes)

- The "where" column convention (F1–F4) rewards brevity over completeness; a future recheck entry should
  state "hunks beyond the conversion:" when a diff is not purely mechanical.
- `vma_flags_*` semantics sit outside the fetched set; a recheck that depends on helper semantics should
  open the defining header (`include/linux/mm_types.h` at the tag) as an eleventh source — recorded
  here, not actioned (frozen scope).
- Reading rule "the two conditions are the same" relies on votes to carry meaning; that is per contract,
  but the entry's own language should mark it as a reading (F5).

## Checks NOT performed (UNVERIFIED)

- Whether cgit actually served tag `v7.3` for the nine copies (contract assigns re-fetch to wave seats;
  I did not hit the network). The pins in `freeze-sha256.txt` only prove committed bytes.
- Whether `_install_special_mapping`'s callee `__install_special_mapping` exists elsewhere at v7.3 —
  outside the fetched set; if it does not, the file would not compile, which is impossible, so it moved
  (the strongest statement the copies support: "not defined in any fetched file").
- The `diff` behaviour on this host is GNU diffutils output rendered by the tooling layer in one run;
  line counts were re-derived with `/usr/bin/diff -u` and match the ledger's stated method.

## Findings (severity list)

- F1 MED — `kernel-v7.3-recheck-r53.md:32` — `mm/mmap.c` "where" cell: understates the diff (helper deletion, renames, DROPPABLE restructure).
- F2 MED — `kernel-v7.3-recheck-r53.md:29` — `mm_inline.h` "where" cell: omits the `memdesc_section(&…)` signature change.
- F3 MED — `kernel-v7.3-recheck-r53.md:31` — `util.c` "where" cell: omits `vma_start_pgoff` hunks; `vm_mmap_pgoff` change is `0 → EMPTY_VMA_FLAGS`, not a type change.
- F4 LOW — `kernel-v7.3-recheck-r53.md:28` — `show_mem.c` "where" cell: "printk units" mislabels signedness/cast fixes.
- F5 MED — `kernel-v7.3-recheck-r53.md:100` — "the two conditions are the same" asserts helper semantics not defined in the fetched set.
- F6 MED — `kernel-v7.3-recheck-r53.md:99` — reading-rule answer is wider than the recheck: covers only 46 table rows, at v7.3 only; reachable misreadings as "entries verified" / "safe on any kernel".
- F7 LOW — `kernel-v7.3-recheck-r53.md:20` — "no release changes" conflates immutable patch bytes with unaging claim relevance.
- F8 LOW — `kernel-v7.3-recheck-r53.md:39-44` — legend does not pre-empt the "absent = failed claim" misreading.
- F9 LOW — `kernel-v7.3-recheck-r53.md:13,105-108` — `recheck:` line omits the ledger's scope and the pins' provenance limit.
- F10 LOW — `kernel-v7.3-recheck-r53.md:34` — disclosed line-count method excludes blank-line churn without saying so.

No finding asserts a counter, control or kill-rule defect. The ledger's mechanical content (46/46
quotes located, statuses, byte-identity claims, diff counts, scope 46-of-49, boundary references)
verified clean; all findings are prose overclaim or misreading risk with fenced replacements above.
