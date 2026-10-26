# Mo51CritEntail17 — ENTAILMENT votes, rows 17–21 (adversarial second vote)

Data commit: `87e0c374537557754bf71dd68036ded3ddc6699c`. Claim rows 17–21 of
`corpus/knowledge/memavailable-estimate-r51.md` judged against the committed source
copies under `corpus/evidence/sources-r51/`. Working tree of the entry and the source
copies byte-equal the data commit (`git diff --quiet 87e0c374… -- corpus/knowledge/memavailable-estimate-r51.md corpus/evidence/sources-r51/`, exit 0).

Hashes recomputed with the mandated one-liner (`sha256` of the claim with whitespace
collapsed, first 12 hex); all five match `evidence/c2-hashes-at-data.txt`. Quotes
located by whitespace-collapsed regex over the committed copy bytes; line numbers given
per row. Context read: the full docstring block around the S495 quote (lines 13–31)
and the full commit-message body for S496 (lines 6–27).

## Row-by-row

### Row 17 — d6001a798ea7 — entailed
Claim: "The LRU sorting helper returns zero for tmpfs folios, which places them on an anon LRU list instead of a file list." (S495)
Quote located at `mm_inline.h.v7.2` lines 25–26: `0 if @folio is a normal anonymous folio, a tmpfs folio or otherwise * ram or swap backed folio.`
Context (lines 13–31): the `folio_is_file_lru` docstring asks "Should the folio be on a file LRU or anon LRU?" and states the returned integer is "used to sort a folio onto the right LRU list". Return 0 covers normal anonymous, tmpfs and ram/swap-backed folios; therefore a tmpfs folio sorts to the anon LRU side, not the file side. The body confirms the split (`return !folio_test_swapbacked(folio);`); line 91 (`folio_is_file_lru(folio) ? LRU_INACTIVE_FILE : LRU_INACTIVE_ANON`) corroborates 0→anon, 65 lines past the quote. The second clause follows from the docstring frame alone; nothing added beyond the source.

### Row 18 — 8f6d04247472 — entailed
Quote located at `mm_inline.h.v7.2` lines 23–24: `1 if @folio is a regular filesystem backed page cache folio * or a lazily freed anonymous folio (e.g. via MADV_FREE).`
Same docstring context assigns return 1 to the file LRU side. The claim restates the 1-case as what the file LRU lists hold; no consequence, number or scope beyond the source.

### Row 19 — a07e4bd7a5ec — entailed
Quote located at `34e431b0.patch` lines 7–8: `They generally do this by adding up "free" and "cached", which was fine ten years ago,`
Context (lines 6–9): "Many load balancing and workload placing programs check /proc/meminfo to estimate how much free memory is available. They generally do this by adding up 'free' and 'cached', which was fine ten years ago, but is pretty much guaranteed to be wrong today." Patch header date is 2014-01-21, so "The 2014 commit" is exact. "Which it calls outdated" is a compression of "fine ten years ago, but … wrong today" — weaker than the source (outdated ⊂ wrong today), not an addition.

### Row 20 — 4d162ecf1409 — entailed
Quote located at `34e431b0.patch` lines 11–12: `It is wrong because Cached includes memory that is not freeable as page cache, for example shared memory segments, tmpfs, and ramfs,`
Context: "It is wrong" refers to the sum method just described (lines 6–9). "Pages that cannot be dropped like cache" restates "memory that is not freeable as page cache"; the enumerated kinds (shared memory segments, tmpfs, ramfs) match exactly. Entailed.

### Row 21 — 50f54829ae20 — entailed
Quote located at `34e431b0.patch` lines 21–23: `user space really should not be expected to know kernel internals to come up with an estimate for the amount of free memory.`
Context (lines 16–26): the current estimate requires MemFree, Active(file), Inactive(file), SReclaimable and zone low watermarks; "However, this may change in the future, and user space really should not be expected to know kernel internals…"; "It is more convenient to provide such an estimate in /proc/meminfo." The claim's "monitoring programs" are a subset of user space (the message itself names workload-placing programs as the user-space consumers), and the internals in question are reclaim internals. The causal reading — the estimate went into meminfo so user space need not model these internals — is the message's stated motivation. Entailed.

## Votes

ENTAIL d6001a798ea7 entailed
ENTAIL 8f6d04247472 entailed
ENTAIL a07e4bd7a5ec entailed
ENTAIL 4d162ecf1409 entailed
ENTAIL 50f54829ae20 entailed

## Findings
- [LOW] Row 17/18 (corpus/evidence/sources-r51/mm_inline.h.v7.2 lines 23–26): the quote alone does not spell out the 0→anon / 1→file mapping; entailment rests on the docstring frame ("file LRU or anon LRU", "used to sort a folio onto the right LRU list") within the ~20-line window. The code at line 91 corroborates, but is 65 lines past the quote.
- [LOW] Row 19 (corpus/evidence/sources-r51/34e431b0.patch lines 7–8): the word "outdated" is not in the source; the verdict treats it as a faithful, weaker compression of "fine ten years ago, but … wrong today", not as an added fact.
