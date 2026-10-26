# Mo51RevEntail04 — entailment votes on claim rows 4–6, `memavailable-estimate-r51.md`

Scope: rows 4–6 of the `## Claims` table of `corpus/knowledge/memavailable-estimate-r51.md` at commit
`87e0c374537557754bf71dd68036ded3ddc6699c`. Seat role: reviewer (non-L1), entailment item. No tools were
installed or upgraded for this work (nothing needed); no pacman run.

## Method and verification performed

1. Read the frozen contract (`.ufo/waves/round-51/contract.md`) first.
2. Extracted the three committed source copies I needed at the data commit with
   `git show 87e0c374537557754bf71dd68036ded3ddc6699c:<path>` into scratch
   `/fast/scratch/hyaku/mori-r51/Mo51RevEntail04/` (TMPDIR set there; removed after the report was written).
   `scripts/hyaku/disk-guard.sh status` was run before work: no ENOSPC condition reported.
3. Hash check — recomputed each claim hash with the prescribed one-liner
   (`python3 -c 'import hashlib,re,sys;print(hashlib.sha256(re.sub(r"\s+"," ",sys.argv[1]).strip().encode()).hexdigest()[:12])' "<claim text>"`):
   all three match `.ufo/waves/round-51/evidence/c2-hashes-at-data.txt`:
   - row 4 → `72cdbee44353`
   - row 5 → `a9cf30c5ed71`
   - row 6 → `5d06a2ae70cf`
4. Copy integrity — sha256 of the two copies I judged against the freeze manifest
   (`.ufo/waves/round-51/evidence/freeze-sha256.txt` at the data commit):
   - `proc.rst.v7.2` = `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126` — matches
   - `show_mem.c.v7.2` = `dba76b263bbdf93323a277a29c9281a892ff3fb35ddd6f0ddaf9ba1acb5b02f5` — matches
   (both also equal the hashes the entry's own `recheck:` line records).
5. Quote location — each quote located in the frozen copy after whitespace collapsing (python check, all `located`).

## Row 4 — hash `72cdbee44353` — source S492

Claim: “The Cached line of /proc/meminfo counts tmpfs and shmem pages together with ordinary file page cache.”

Quote located at `proc.rst.v7.2:1139-1140`, under the `Cached` field header (line 1138), in the /proc/meminfo
field list. Context as read (lines 1134-1141):

```
Buffers
              Relatively temporary storage for raw disk blocks
              shouldn't get tremendously large (20MB or so)
Cached
              In-memory cache for files read from the disk (the
              pagecache) as well as tmpfs & shmem.
              Doesn't include SwapCached.
```

Judgment: the doc defines the `Cached` figure as in-memory cache for files read from the disk (the pagecache)
as well as tmpfs & shmem. “Counts … together with” restates the field definition (a meminfo field definition is
exactly what the line's value is); “ordinary file page cache” restates “cache for files read from the disk (the
pagecache)”. No consequence, number, or scope is added beyond the definition; the claim does not assert
completeness beyond the doc's own wording. Note the doc's “Doesn't include SwapCached.” (line 1141) does not
contradict the claim.

Verdict: follows from quote + context.

ENTAIL 72cdbee44353 entailed

## Row 5 — hash `a9cf30c5ed71` — source S492

Claim: “The Shmem line reports the memory held by shared memory segments and tmpfs files as one figure.”

Quote located at `proc.rst.v7.2:1193`, the single description line under the `Shmem` field header (line 1192),
immediately before `KReclaimable` (line 1194). Context as read (lines 1191-1194):

```
Mapped
              files which have been mmapped, such as libraries. ...
Shmem
              Total memory used by shared memory (shmem) and tmpfs
KReclaimable
```

Judgment: “Total memory used by shared memory (shmem) and tmpfs” states one total covering both named users;
“as one figure” restates “Total”. “Shared memory segments” and “tmpfs files” expand the doc's noun phrases
“shared memory (shmem)” and “tmpfs” without narrowing or extending the covered set — the same document uses
“shared memory segments” for this facility elsewhere (`proc.rst.v7.2:1953`, coredump_filter section). No
consequence or number is added, and the scope (shmem + tmpfs) is unchanged.

Verdict: follows from quote + context.

ENTAIL a9cf30c5ed71 entailed

## Row 6 — hash `5d06a2ae70cf` — source S493

Claim: “The estimate starts from the free page count minus totalreserve_pages, the pages the kernel holds back
from userspace allocations.”

Quote located at `show_mem.c.v7.2:45-47`, inside `si_mem_available()`. Context as read (lines 40-57, 69-71):

```
	for_each_zone(zone)
		wmark_low += low_wmark_pages(zone);

	/*
	 * Estimate the amount of memory available for userspace allocations,
	 * without causing swapping or OOM.
	 */
	available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;

	/*
	 * Not all the page cache can be freed, otherwise the system will
	 * start swapping or thrashing. Assume at least half of the page
	 * cache, or the low watermark worth of cache, needs to stay.
	 */
	pagecache = global_node_page_state(NR_ACTIVE_FILE) +
		global_node_page_state(NR_INACTIVE_FILE);
	pagecache -= min(pagecache / 2, wmark_low);
	available += pagecache;
	...
	if (available < 0)
		available = 0;
	return available;
```

Judgment: (a) the first assignment of `available` (line 47) is the free-page counter (`NR_FREE_PAGES`) minus
`totalreserve_pages`, and later terms are added onto it (lines 54-57, 64-67), so “the estimate starts from the
free page count minus totalreserve_pages” matches the code's shape. (b) The parenthetical gloss rests on the
function's own comment (lines 43-46): the quantity being computed is “the amount of memory available for
userspace allocations, without causing swapping or OOM”; subtracting `totalreserve_pages` in that computation
is the reserves being excluded from userspace-allocatable memory. No number is added; no scope beyond the
function's own stated purpose. (The file also declares `unsigned long totalreserve_pages __read_mostly;` at
`show_mem.c.v7.2:23`; the detailed definition of the reserve lives outside this copy, but the claim's gloss does
not need it — it restates what the subtraction does given the comment.)

Verdict: follows from quote + context.

ENTAIL 5d06a2ae70cf entailed

## Verdict summary

This file carries exactly one verdict line per assigned row (4, 5, 6), one each in the row sections above;
no overclaim votes were cast, so no replacement claims are proposed. Rows 1-3 and 7-21 were not assigned to
this seat; no verdict is recorded for them here.

UNVERIFIED items: none material — the two copies judged were hash-checked against the freeze manifest, the
quotes were located, and the context lines quoted above are verbatim from those copies. I did not re-run
`count-c2.py` itself (counter reruns are other seats' items) and did not independently fetch the upstream URLs
(recheck is the entry's own `recheck:` arm).

## Findings

- LOW — `corpus/knowledge/memavailable-estimate-r51.md` row 5: the claim's nouns “segments” and “files” do not
  appear in the S492 quote itself; judged entailed because the covered set is unchanged and the same document
  says “shared memory segments” at `proc.rst.v7.2:1953`. A future strictness pass keyed to verbatim nouns only
  could flag this row; wording “shared memory (shmem) and tmpfs” would be beyond doubt.
- LOW — `corpus/knowledge/memavailable-estimate-r51.md` row 6: the gloss “the pages the kernel holds back from
  userspace allocations” is a contextual reading of the `si_mem_available()` comment plus the subtraction, not
  words from the quote; judged entailed on quote + context. The reserve's precise composition
  (`show_mem.c.v7.2:23`) is defined outside the frozen copy.
- No HIGH or MED findings on rows 4–6; all three claims are judged entailed by this seat, so no row needs the
  L1 to replace claim text.
