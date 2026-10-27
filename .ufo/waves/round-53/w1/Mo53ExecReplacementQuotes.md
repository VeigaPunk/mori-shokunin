# Mo53ExecReplacementQuotes — the two `absent` rows carry their replacement quotes (w1, round 53)

Assignment: for hashes `0fbd62f51ce8` (ledger row 34) and `d7a1dc88dcb3` (row 37) verify that the replacement quote in
`corpus/knowledge/kernel-v7.3-recheck-r53.md` (a) occurs, whitespace-collapsed, in
`corpus/evidence/sources-r53/mmap.c.v7.3` (with lines), (b) is 6–25 words under the frozen counter rule, (c) states the
same condition as the v7.2 quote in `corpus/evidence/sources-r52/mmap.c.v7.2`, and explain
`vma_flags_set(&vma_flags, VMA_NORESERVE_BIT)` vs `vm_flags |= VM_NORESERVE` from the v7.3 definitions. Verdict per row.
This seat is an executor, not a voter: it writes no verdict line for the C1 vote tally.

All reads were absolute and read-only. Scratch: `/fast/scratch/hyaku/mori-r53/Mo53ExecReplacementQuotes/` (removed at the
end, §Scratch). No file outside this report and that scratch tree was written; no git/jj mutation was run anywhere.

## Independent byte provenance (re-fetched, not trusted)

Every byte I judged was re-fetched this seat, then compared with the lane's committed copy.

| file | URL | sha256 | vs lane copy |
|---|---|---|---|
| `mm/mmap.c` @ v7.3 | `…/plain/mm/mmap.c?h=v7.3` | `8e51fb1c10fee6943c9edc26b72952137b4098b00cc050ea1e6ade6e27197feb` | identical to `corpus/evidence/sources-r53/mmap.c.v7.3` (`diff` empty) |
| `mm/mmap.c` @ tag commit `c03c1a14507dfaf8b856c2608f9ac216021fc222` | `…/plain/mm/mmap.c?h=c03c1a14507d…` | `8e51fb1c10fe…` | identical to the `?h=v7.3` bytes |
| `mm/mmap.c` @ v7.2 | `…/plain/mm/mmap.c?h=v7.2` | `449b858385c7ece0ff88a8b41893efadb70a437fb8585a296c4ef0461a4c1545` | identical to `corpus/evidence/sources-r52/mmap.c.v7.2` |
| `include/linux/mm.h` @ v7.3 | `…/plain/include/linux/mm.h?h=v7.3` | `c294397b9973040f9431604ad4088c957ac7101c777a8e4be91d0ea3f2a37e80` | not in lane (fetched) |
| `include/linux/mm.h` @ tag commit | `…?h=c03c1a14507d…` | `c294397b9973…` | same as `?h=v7.3` |
| `include/linux/mm_types.h` @ v7.3 | `…/plain/include/linux/mm_types.h?h=v7.3` | `3f3687985aff94dfa0301edc45158905d13944bed310f3697e65ed61848f0e99` | not in lane (fetched) |
| `mm/vma.c` @ v7.3 / v7.2 | `…/plain/mm/vma.c?h=v7.3` / `?h=v7.2` | `1593befef4ef3392c2f818321489dabc610e930958d121659694fbbcc6ff99ab` / `9512e40a6f73d71a14aa49828c99b37808074f60cdc59dbad05e6df652e46a55` | not in lane (fetched) |
| `mm/hugetlb.c` @ v7.3 / v7.2 | `…/plain/mm/hugetlb.c?h=v7.3` / `?h=v7.2` | `3e7bdb3182a0b699f10f9c19be338c967dffffc15fe1f57eeddc1bad776ce6a4` / `7f895f6440a83fdaad2a98a519071c9d401a2a5f0a1d936fd135a5ab3484a384` | not in lane (fetched) |

Tag identity: `git ls-remote … 'refs/tags/v7.3*'` → `refs/tags/v7.3 091b06388b117fefdcb63336ac09956a4914b961`, `refs/tags/v7.3^{} c03c1a14507dfaf8b856c2608f9ac216021fc222`; cgit served the same `mm/mmap.c` bytes for `?h=v7.3` and for that commit sha. The pin in the counter
(`V73["mm/mmap.c"] = 8e51fb1c10fe…`) and in SOURCES row S510 agree with my independent fetch.

## Side by side: hash `0fbd62f51ce8`, ledger row 34

Claim text (`.ufo/waves/round-53/evidence/c1-claims.txt`, row 34): *"For ordinary mappings MAP_NORESERVE drops commit
charging only when the mode is something other than never-overcommit."*

`corpus/evidence/sources-r52/mmap.c.v7.2:546-558` (quote lines 551-553):

```
	/*
	 * Set 'VM_NORESERVE' if we should not account for the
	 * memory use of this mapping.
	 */
	if (flags & MAP_NORESERVE) {
		/* We honor MAP_NORESERVE if allowed to overcommit */
		if (sysctl_overcommit_memory != OVERCOMMIT_NEVER)
			vm_flags |= VM_NORESERVE;

		/* hugetlb applies strict overcommit unless MAP_NORESERVE */
		if (file && is_file_hugepages(file))
			vm_flags |= VM_NORESERVE;
	}
```

`corpus/evidence/sources-r53/mmap.c.v7.3:559-571` (quote lines 564-566; same bytes as `?h=v7.3`):

```
	/*
	 * Set VMA_NORESERVE_BIT if we should not account for the memory use
	 * of this mapping.
	 */
	if (flags & MAP_NORESERVE) {
		/* We honor MAP_NORESERVE if allowed to overcommit */
		if (sysctl_overcommit_memory != OVERCOMMIT_NEVER)
			vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);

		/* hugetlb applies strict overcommit unless MAP_NORESERVE */
		if (file && is_file_hugepages(file))
			vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);
	}
```

Ledger quote cell: `We honor MAP_NORESERVE if allowed to overcommit */ if (sysctl_overcommit_memory != OVERCOMMIT_NEVER) vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);`
- occurs whitespace-collapsed in `mmap.c.v7.3`: **yes**, exactly once, spanning lines **564-566** (collapsed span
  `/* We honor MAP_NORESERVE if allowed to overcommit */ if (sysctl_overcommit_memory != OVERCOMMIT_NEVER) vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);` — the cell drops the leading `/* `).
- word count: **14** tokens (counter rule `MIN_WORDS..MAX_WORDS = 6..25`), i.e. inside the bound.
- the v7.2 quote is **not** in the v7.3 copy (0 occurrences of `vm_flags |= VM_NORESERVE` in `mmap.c.v7.3`) — the
  counter's derived `absent` is correct.
- same condition: outer guard `if (flags & MAP_NORESERVE)` (v7.2:550 / v7.3:563), inner guard
  `if (sysctl_overcommit_memory != OVERCOMMIT_NEVER)` (v7.2:552 / v7.3:565) — byte-identical text; only the flag-write
  statement changed.

## Side by side: hash `d7a1dc88dcb3`, ledger row 37

Claim text (same file, row 37): *"Hugetlb file mappings are charged strictly unless the caller passes MAP_NORESERVE, a
carve-out the mode-2 rule does not mention."*

`corpus/evidence/sources-r52/mmap.c.v7.2:555-557`:

```
		/* hugetlb applies strict overcommit unless MAP_NORESERVE */
		if (file && is_file_hugepages(file))
			vm_flags |= VM_NORESERVE;
```

`corpus/evidence/sources-r53/mmap.c.v7.3:568-570`:

```
		/* hugetlb applies strict overcommit unless MAP_NORESERVE */
		if (file && is_file_hugepages(file))
			vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);
```

Ledger quote cell: `hugetlb applies strict overcommit unless MAP_NORESERVE */ if (file && is_file_hugepages(file)) vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);`
- occurs whitespace-collapsed in `mmap.c.v7.3`: **yes**, exactly once, spanning lines **568-570**.
- word count: **13** tokens → inside 6..25.
- v7.2 quote absent from the v7.3 copy: **yes** (`vm_flags |= VM_NORESERVE` has 0 hits there).
- same condition: outer guard `if (flags & MAP_NORESERVE)` and inner guard `if (file && is_file_hugepages(file))`
  (v7.2:556 / v7.3:569) — identical text; only the flag-write changed. This block is nested inside the
  `if (flags & MAP_NORESERVE)` block in both versions, so the carve-out still applies only when the caller passes
  MAP_NORESERVE.

## Why the two spellings are the same bit (v7.3 definitions)

v7.2 wrote the legacy word; v7.3 writes the vma-flags bitmap. They are the same bit 21 of the same first word.

1. Bit number: `include/linux/mm.h` v7.3:323 `DECLARE_VMA_BIT(NORESERVE, 21), /* should the VM suppress accounting */`
   — identical line in v7.2 (`mm.h.v7.2:322`). No renumbering between releases.
2. Legacy name: v7.3 `mm.h:400` `#define INIT_VM_FLAG(name) BIT((__force int) VMA_ ## name ## _BIT)`; `mm.h:427`
   `#define VM_NORESERVE INIT_VM_FLAG(NORESERVE)` ⇒ legacy `VM_NORESERVE == BIT(21)`. So v7.2's
   `vm_flags |= VM_NORESERVE` set bit 21 of the legacy `vm_flags_t` word.
3. New name path: v7.3 `mm.h:1276-1277` `#define vma_flags_set(flags, ...) vma_flags_set_mask(flags, mk_vma_flags(__VA_ARGS__))`
   → `mm.h:1145-1146` `mk_vma_flags` → `mm.h:1117-1122` `vma_flags_set_flag()` → `__set_bit((__force int)bit, bitmap)`.
   With `VMA_NORESERVE_BIT = 21` and `vma_flags_t` a single-word bitmap
   (`mm_types.h` v7.3:868-870, `NUM_VMA_FLAG_BITS BITS_PER_LONG`), this sets bit 21 of `__vma_flags[0]`.
4. Same storage: v7.3 `mm_types.h:1093-1096` `vma_flags_to_legacy(flags) { return (vm_flags_t)flags.__vma_flags[0]; }`
   and `mm_types.h:948-951` `union { const vm_flags_t vm_flags; vma_flags_t flags; }` in `struct vm_area_struct`. A bit
   written through `vma_flags_set()` is visible as legacy `VM_NORESERVE` and vice versa, for any bit `< BITS_PER_LONG`
   (bit 21 qualifies on 32- and 64-bit builds).
5. Same producer plumbing: v7.2 `do_mmap(..., vm_flags_t vm_flags, ...)` (mmap.c v7.2:336-338) ORs
   `calc_vm_prot_bits()|calc_vm_flag_bits()` into the legacy word (v7.2:402); v7.3 `do_mmap(..., vma_flags_t vma_flags, ...)`
   (mmap.c v7.3:338-340) ORs `legacy_to_vma_flags(calc_vm_prot_bits(...))` / `legacy_to_vma_flags(calc_vm_flag_bits(...))`
   into the bitmap (v7.3:404-408), and `legacy_to_vma_flags()` copies the legacy word into word 0 verbatim
   (`mm_types.h` v7.3:1118-1123). `vm_mmap_pgoff()` passes `0` (v7.2 `util.c.v7.2:581`) vs `EMPTY_VMA_FLAGS`
   (v7.3 `util.c.v7.3:581`) — the same empty starting set.
6. Same consumer: `accountable_mapping()` in `mm/vma.c` is textually identical at v7.2:2341-2354 and v7.3:2463-2476 and
   tests the bit through the new API (`!vma_flags_test_any(&map->vma_flags, VMA_NORESERVE_BIT, VMA_SHARED_BIT)`); the
   hugetlb carve-out consumer `hugetlb_reserve_pages()` is likewise identical (`mm/hugetlb.c` v7.2:6574 / v7.3:6703
   `if (vma_flags_test(&vma_flags, VMA_NORESERVE_BIT)) return 0;`). So at v7.2 the producer's legacy-word write already
   had to land on bit 21 for the consumer to see it (that is exactly the aliasing in 4); v7.3 spells the same write with
   the consumer's own API. No behaviour change, only the representation of the write.

## Verdicts

| h | ledger row | occurrence (whitespace-collapsed) | words | same condition as v7.2 quote | derived status | verdict |
|---|---|---|---|---|---|---|
| `0fbd62f51ce8` | 34 | one occurrence, `mmap.c.v7.3:564-566` | 14 (bound 6–25) | yes — identical guards, flag write respelled | `absent` (correct) | **PASS** |
| `d7a1dc88dcb3` | 37 | one occurrence, `mmap.c.v7.3:568-570` | 13 (bound 6–25) | yes — identical guards, flag write respelled | `absent` (correct) | **PASS** |

Frozen counter re-run at the data commit (read-only, cwd `/home/vgpnk/Projects/shokunin/mori-shokunin`):

```
$ python3 .ufo/waves/round-53/count-c1.py 2a4213bf8da72f7cd78189baa5bb9be825dca1df
C1=unmet scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=0 dissent=0 rev=2a4213bf… failed=votes
```

`quote_ok=46` and `absent=2` match my independent reading of these two rows; `failed=votes` is the expected data-commit
state (no RECHECK reports yet at that revision), not a data defect. I did not change any byte of the counter, the
predicates, the ledger, the copies or the tool.

## Retained evidence (commands, exit codes)

```
$ mkdir -p /fast/scratch/hyaku/mori-r53/Mo53ExecReplacementQuotes/tmp            # rc 0
$ curl -fsSL -o mmap.c.v7.3.fetch 'https://git.kernel.org/…/plain/mm/mmap.c?h=v7.3'    # rc 0
$ curl -fsSL -o mm.h.v7.3.fetch   'https://git.kernel.org/…/plain/include/linux/mm.h?h=v7.3'  # rc 0
$ sha256sum mmap.c.v7.3.fetch …/corpus/evidence/sources-r53/mmap.c.v7.3
  8e51fb1c…feb  both                                                            # rc 0, identical
$ diff -u mmap.c.v7.3.fetch …/sources-r53/mmap.c.v7.3 && echo IDENTICAL         # rc 0, IDENTICAL
$ curl -fsSL -o mmap.c.attag.fetch 'https://git.kernel.org/…/plain/mm/mmap.c?h=c03c1a14507dfaf8b856c2608f9ac216021fc222'  # rc 0
$ sha256sum mmap.c.attag.fetch → 8e51fb1c…feb                                     # same as ?h=v7.3
$ git ls-remote https://git.kernel.org/…/linux.git 'refs/tags/v7.3*'
  091b06388b117fefdcb63336ac09956a4914b961  refs/tags/v7.3
  c03c1a14507dfaf8b856c2608f9ac216021fc222  refs/tags/v7.3^{}                  # rc 0
$ curl -fsSL -o mmap.c.v7.2.fetch 'https://git.kernel.org/…/plain/mm/mmap.c?h=v7.2'   # rc 0
$ sha256sum mmap.c.v7.2.fetch …/sources-r52/mmap.c.v7.2 → 449b8583…545            # identical
$ python3 verify.py   # independent occurrence/word/ledger-cell check, outputs below       # rc 0
  hash 0fbd62f51ce8 v7.2 quote in v7.3 collapsed: False | v7.3 quote in v7.3 collapsed: True
  v7.3 quote raw-file line spans: (564,566) | quote words 14 | ledger cell == replacement: True
  hash d7a1dc88dcb3 v7.2 quote in v7.3 collapsed: False | v7.3 quote in v7.3 collapsed: True
  v7.3 quote raw-file line spans: (568,570) | quote words 13 | ledger cell == replacement: True
$ python3 - <<'PY' … n.count(q) … PY   # whitespace-collapsed occurrence counts in mmap.c.v7.3
  1  'We honor MAP_NORESERVE if allowed to overcommit */ if (sysct…'
  1  'hugetlb applies strict overcommit unless MAP_NORESERVE */ if'
  0  'vm_flags |= VM_NORESERVE'
$ grep -n 'DECLARE_VMA_BIT(NORESERVE' mm.h.v7.2.fetch mm.h.v7.3.fetch
  mm.h.v7.2.fetch:322 … mm.h.v7.3.fetch:323   (both "NORESERVE, 21")
$ grep -n 'NORESERVE' vma.c.v7.2.fetch vma.c.v7.3.fetch
  v7.2:2353 / v7.3:2475  !vma_flags_test_any(&map->vma_flags, VMA_NORESERVE_BIT, VMA_SHARED_BIT)
$ grep -n 'NORESERVE' hugetlb.c.v7.2.fetch hugetlb.c.v7.3.fetch
  v7.2:6574 / v7.3:6703  if (vma_flags_test(&vma_flags, VMA_NORESERVE_BIT)) return 0;
```

Cited excerpts are reproduced in this report (§Side by side and §Why the two spellings are the same bit); the scratch
tree itself is deleted, nothing cited depends on it.

## Risks and limits (this seat)

- The `holds` disposition is a reading, and I am not a voter: these two rows still need two RECHECK seats' final
  unfenced line each (the counter's `voted=0 failed=votes` at the data commit shows that state).
- `absent` is derived from the v7.2 *quote string* not occurring in the v7.3 file. It does not by itself prove the
  `MAP_NORESERVE` rule changed meaning; that is why the replacement quote and its disposition exist. Verified here: the
  new quote and the old quote describe the same guard, and both consumers read the same bit.
- My equivalence argument rests on files the lane does not pin (`include/linux/mm.h`, `include/linux/mm_types.h`,
  `mm/vma.c`, `mm/hugetlb.c` at v7.3). I fetched them from cgit this seat and record sha256 above; they are not in
  `corpus/evidence/sources-r53/`, so a reader of the lane alone cannot re-derive §Why the two spellings are the same bit.
- Word counts are token counts under the counter's own rule (`len(q.split(" "))` after whitespace collapse), not prose
  words: `*/`, `!=` and `(file` count as tokens.

## Scratch

`/fast/scratch/hyaku/mori-r53/Mo53ExecReplacementQuotes/` held only the fetched copies, two small check scripts and an
empty `tmp/`; it is removed (`rm -rf`) at the end of this seat. No clone was made; no git/jj command mutated the fleet
repo, the lane or the index (only `git ls-remote` and read-only `git show` via the lane's counter were used).

## Findings

- **LOW** — Both replacement quote cells begin mid-comment: they drop the comment opener (`/* `) and start at
  `We honor…` / `hugetlb applies…`, then carry the closing `*/`. Same shape as the v7.2 quotes they replace, so the
  frozen `quote_ok` rule accepts them, but a reader cannot see where the comment begins. Files:
  `corpus/knowledge/kernel-v7.3-recheck-r53.md` (rows `0fbd62f51ce8`, `d7a1dc88dcb3`); inherited shape from
  `corpus/evidence/sources-r52/mmap.c.v7.2:551,555`. Advisory only.
- **LOW** — The frozen word bound counts C tokens, not words: the two replacements are 14 and 13 tokens but roughly 7
  and 6 prose words, so the "6–25 words" rule is effectively a 6–25 *token* rule for code quotes. Named limit of
  `.ufo/waves/round-53/count-c1.py` (`MIN_WORDS, MAX_WORDS = 6, 25`); both rows pass either way. Not a change request.
- **LOW** — The equivalence "legacy `vm_flags |= VM_NORESERVE` ≡ `vma_flags_set(&vma_flags, VMA_NORESERVE_BIT)`"
  cannot be checked from in-lane bytes: `include/linux/mm.h`, `include/linux/mm_types.h`, `mm/vma.c` and
  `mm/hugetlb.c` at v7.3 are not among the twelve pinned copies in `corpus/evidence/sources-r53/` (rows S502–S513).
  Route for round 54: if the ledger's "the two conditions are the same" claim is to be reader-checkable in-lane, pin
  those headers/consumers too. Files: `corpus/evidence/sources-r53/` (pin set),
  `corpus/knowledge/kernel-v7.3-recheck-r53.md` §Reading rules (pointer `mmap.c.v7.3:563-571`, which I verified is
  the correct block range).
- **LOW (informational, no defect)** — Verified accurate and worth recording: `kernel-v7.3-recheck-r53.md`
  §Reading rules points at `mmap.c.v7.3:563-571`; the block is exactly 563–571, and the two replacement quotes sit at
  564–566 and 568–570. File: `corpus/knowledge/kernel-v7.3-recheck-r53.md`.
