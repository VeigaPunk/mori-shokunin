# Mo51RevEntail16 — entailment votes for claim rows 16–18 (mori round 51, wave w1)

Seat: Mo51RevEntail16 (reviewer, ENTAILMENT item). Judged at data commit
87e0c374537557754bf71dd68036ded3ddc6699c. Method per row: the claim and quote cells were parsed
programmatically from the committed entry `corpus/knowledge/memavailable-estimate-r51.md` (21 table rows
parsed, no manual transcription), the row hash was recomputed with the frozen one-liner (sha256 of the
whitespace-collapsed claim cell, first 12 hex) and checked against
`.ufo/waves/round-51/evidence/c2-hashes-at-data.txt`, the quote was located whitespace-collapsed in the
committed copy under `corpus/evidence/sources-r51/`, and about 20 lines of context around it were read
before judging. Scratch `/fast/scratch/hyaku/mori-r51/Mo51RevEntail16/` with `TMPDIR` inside it; disk-guard
status before start: `/fast/scratch/hyaku` 25 % used, 604.3 G free — no ENOSPC. Files were extracted with
`git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive 87e0c374537557754bf71dd68036ded3ddc6699c --
corpus/knowledge/memavailable-estimate-r51.md corpus/evidence/sources-r51 | tar -x` (rc 0). No tool
installs, no pacman, no repo or index mutation, no subagents.

Copy integrity: the sha256 of both copies judged here match the frozen list
`.ufo/waves/round-51/evidence/freeze-sha256.txt` — meminfo.c.v7.2 =
d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda, mm_inline.h.v7.2 =
2d4accbbc1ec139bfe11a356d4d17a55a2543769f3e10057a8a8584429c45ef6 (observed via `sha256sum`, rc 0).

## Row 16 — hash 357c747c23d2 (source S494)

- Claim cell: "MemFree prints the sysinfo free count while MemAvailable prints the separately computed
  estimate, as two adjacent lines."
- Recomputed hash 357c747c23d2 — matches the frozen row hash (row=16 in c2-hashes-at-data.txt).
- Quote located in `corpus/evidence/sources-r51/meminfo.c.v7.2` at line 61 (the collapsed span covers
  lines 61–62); exactly 1 occurrence in the copy.
- Context read: lines 41–81, plus the `show_val_kb` helper at lines 23–27 and the declarations at
  lines 31–35.
- What the context shows: `struct sysinfo i;` is declared (line 31) and filled by `si_meminfo(&i);`
  (line 44); `long available;` is a separate variable set by `available = si_mem_available();` (line 56),
  a dedicated computation distinct from the sysinfo fill; then `show_val_kb(m, "MemFree: ", i.freeram);`
  (line 61) and `show_val_kb(m, "MemAvailable: ", available);` (line 62) are consecutive calls, and
  `show_val_kb` emits one "… kB\n" line per call (lines 23–27), so the two output lines are adjacent.
- Judgment: every operative part of the claim is stated by the quote plus context — MemFree from
  `i.freeram`, the free field of the sysinfo struct; MemAvailable from `available`, computed separately by
  `si_mem_available()`; two adjacent output lines. Calling that value "the estimate" adds no consequence,
  number or scope: it is the entry's defined term for `si_mem_available()`'s return (established by the
  S493 rows of the same entry) and matches the function's role. No overclaim.

ENTAIL 357c747c23d2 entailed

## Row 17 — hash d6001a798ea7 (source S495)

- Claim cell: "The LRU sorting helper returns zero for tmpfs folios, which places them on an anon LRU list
  instead of a file list."
- Recomputed hash d6001a798ea7 — matches the frozen row hash (row=17).
- Quote located in `corpus/evidence/sources-r51/mm_inline.h.v7.2` at line 25 (span 25–26); exactly 1
  occurrence in the copy.
- Context read: lines 5–45 — the whole `folio_is_file_lru` doc block and body.
- What the context shows: the helper is `folio_is_file_lru`, documented as "Should the folio be on a file
  LRU or anon LRU?" (line 14), whose return is "used to sort a folio onto the right LRU list" (lines
  21–22); the quote itself is the 0-case: "0 if @folio is a normal anonymous folio, a tmpfs folio or
  otherwise ram or swap backed folio" (lines 25–26); the body is `return !folio_test_swapbacked(folio);`
  (line 30).
- Judgment: the helper's documented dichotomy is file-LRU-versus-anon-LRU and its return sorts the folio
  onto the right list; returning 0 for tmpfs folios therefore sorts them onto the anon LRU list, not the
  file list. "Places them on an anon LRU list" is the doc's own "sort onto the right LRU list" applied to
  the 0-case. No added consequence, number or scope. No overclaim.

ENTAIL d6001a798ea7 entailed

## Row 18 — hash 8f6d04247472 (source S495)

- Claim cell: "The file LRU lists hold regular filesystem page cache and also anonymous pages lazily freed
  through MADV_FREE."
- Recomputed hash 8f6d04247472 — matches the frozen row hash (row=18).
- Quote located in `corpus/evidence/sources-r51/mm_inline.h.v7.2` at line 23 (span 23–24); exactly 1
  occurrence in the copy.
- Context read: lines 3–43 — the same doc block, the 1-case and the complementary 0-case, plus the body.
- What the context shows: return 1 — "a regular filesystem backed page cache folio or a lazily freed
  anonymous folio (e.g. via MADV_FREE)" (lines 23–24) — is the file-LRU answer of `folio_is_file_lru`
  (function name, doc question at line 14, complementary 0-case at lines 25–26), and the return is "used
  to sort a folio onto the right LRU list" (lines 21–22).
- Judgment: both categories the claim names are the source's own 1-case, and being sorted onto the file
  LRU list is what "the file LRU lists hold" means here. The claim's "through MADV_FREE" names the
  source's own example ("e.g. via MADV_FREE"); it asserts a subset of the source's set (all lazily freed
  anonymous folios, of which MADV_FREE is the given instance) and asserts no exclusivity, so it adds no
  scope the source lacks. No overclaim.

ENTAIL 8f6d04247472 entailed

## Evidence commands

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive 87e0c374537557754bf71dd68036ded3ddc6699c --
  corpus/knowledge/memavailable-estimate-r51.md corpus/evidence/sources-r51 | tar -x` in the scratch dir →
  rc 0, six files extracted.
- Frozen one-liner hash recompute over the three claim cells as parsed from the committed table →
  357c747c23d2, d6001a798ea7, 8f6d04247472 — all three match rows 16–18 of
  `.ufo/waves/round-51/evidence/c2-hashes-at-data.txt`.
- Whitespace-collapsed quote search over the copies → row 16 unique at meminfo.c.v7.2:61 (span 61–62);
  row 17 unique at mm_inline.h.v7.2:25 (span 25–26); row 18 unique at mm_inline.h.v7.2:23 (span 23–24).
- `sha256sum` over the two copies → the two values above, both equal to the frozen entries in
  `.ufo/waves/round-51/evidence/freeze-sha256.txt`.

## Named limits of this judgment

- Per the frozen predicate, an entailed vote records this seat's judgment that the claim follows from the
  quote plus about 20 lines of context; it is a committed reviewer step, not outside verification (contract,
  C2 named limits).
- Row 16's word "estimate" is judged against the entry's defined term (its S493 rows), not against
  meminfo.c's own vocabulary; meminfo.c never uses the word.
- v7.2 bytes only; nothing here speaks about other kernels or hosts.

## Findings

- LOW — row 16 (`corpus/knowledge/memavailable-estimate-r51.md`, Claims row 16): the claim calls the
  MemAvailable value "the estimate", a word that does not occur in this row's own source
  (`corpus/evidence/sources-r51/meminfo.c.v7.2`); judged entailed because it adds no consequence, number
  or scope and is the entry's defined term for `si_mem_available()`'s return, but the term rests on the
  S492/S493 rows, not on this row's quote.
- LOW — row 18 (same file, Claims row 18): the claim narrows the source's "a lazily freed anonymous folio
  (e.g. via MADV_FREE)" to "through MADV_FREE"; judged entailed as a subset assertion with no exclusivity
  claimed, but a cell keeping the source's example scope ("lazily freed anonymous folios, e.g. via
  MADV_FREE") would match the source even more exactly.
- No HIGH or MED findings; no overclaim votes cast; no counter weakness observed within this seat's scope.
