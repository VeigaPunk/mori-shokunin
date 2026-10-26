# Mo50bRevRowsCgroupA — entailment review: claims-table rows 1–4 (S489), `corpus/knowledge/oom-memcg-stat-r50.md`

Reviewed at: `487941b9395e89678af0053cc443cdb49cdee6e3` (L1 landed data). Rows 1–4 are entry lines 18–21 in
`git show 487941b9395e89678af0053cc443cdb49cdee6e3:corpus/knowledge/oom-memcg-stat-r50.md`.
Source copy: `corpus/evidence/sources-r50/cgroup-v2.7.2.html` (S489, `corpus/SOURCES.md:268`).

## Inputs and copy identity

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse 487941b…:corpus/evidence/sources-r50/cgroup-v2.7.2.html HEAD:corpus/evidence/sources-r50/cgroup-v2.7.2.html` → `2378ff30758ba6975e94c2d3795e899e9db0fae0` / `2378ff30758ba6975e94c2d3795e899e9db0fae0`; `git status --porcelain corpus/evidence/sources-r50/` → empty (exit 0, no output). The bytes I read are the bytes the counter scored.
- `python3 .ufo/waves/round-50/count-c2.py 487941b9395e89678af0053cc443cdb49cdee6e3` → `C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=487941b9395e89678af0053cc443cdb49cdee6e3` (exit 0). The counter proves each quote occurs in the copy; per the frozen named limit, location is not entailment — the judgments below are mine.
- S489 row read at `corpus/SOURCES.md:268`: names `https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html`, `mined`, `2026-10-26`, copy sha256 `2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34` — same digest the entry's `recheck:` line pins. (`used-by` cell not eyeballed beyond the 768-byte read window; covered by the counter's `source_rows=ok`.)

## Row 1 — byte counts and write rounding

Claim cell: `Every memory amount the block prints is a byte count, and an unaligned write may be rounded up to a page when read back.`

Quote location: `cgroup-v2.7.2.html` lines 1194–1196, section `Memory Interface Files` (`<section id="memory-interface-files">` line 1192). 15-line context read: lines 1177–1215.

```
1194  <p>All memory amounts are in bytes.  If a value which is not aligned to
1195  PAGE_SIZE is written, the value may be rounded up to the closest
1196  PAGE_SIZE multiple when read back.</p>
```

Judgment: **OVERCLAIM** (second half only).

- "Every memory amount the block prints is a byte count" — supported. The `memory.stat` entry itself says `All memory amounts are in bytes.` (line 1397, inside the `<dt>memory.stat</dt>` dd starting at 1393), and the quoted interface-files preamble (1194) states it for the memory interface files generally.
- "an unaligned write may be rounded up to a page when read back" — the source says `may be rounded up to the closest PAGE_SIZE multiple` (1195–1196). "Rounded up to a page" literally reads as rounding up to one page; for a value larger than one page (e.g. 1.5 pages) the source's rule gives the closest multiple (2 pages), not "a page". The claim replaces the source's precise rule with a shorter phrase that does not follow from it.

Exact words to cut: `a page` → `a PAGE_SIZE multiple` (the source's own words, lines 1195–1196).

Replacement claim cell (floors held by manual token count: 21 words; words of 3+ letters absent from the quote include `every, block, prints, count, unaligned, rounded, multiple, when, read, back` — the quote's words are all/memory/amounts/are/in/bytes/if/value/which/not/aligned/page_size/is/written; cell text remains unique in the table):

```
| Every memory amount the block prints is a byte count, and an unaligned write may be rounded up to a PAGE_SIZE multiple when read back. | S489 | `All memory amounts are in bytes. If a value which is not aligned to PAGE_SIZE is written,` |
```

Severity: LOW. The rounding half concerns write-side behavior this lane never performs (Boundaries: setting `memory.max` is tsukuroi's work); no detection rule in the entry depends on it.

## Row 2 — the anon key

Claim cell: `The anon key counts anonymous mappings such as brk and MAP_ANONYMOUS, so it carries a process heap rather than page cache.`

Quote location: lines 1406–1410, `<dt>anon</dt>` dd inside the `memory.stat` dl (dt at 1393). 15-line context read: lines 1389–1463 (covers rows 2–4).

```
1406  <dt>anon</dt><dd><p>Amount of memory used in anonymous mappings such as
1407  <code ...><span class="pre">brk()</span></code>, <code ...><span class="pre">sbrk()</span></code>, and mmap(MAP_ANONYMOUS). Note that
1408  some kernel configurations might account complete larger
1409  allocations (e.g., THP) if only some, but not all the
1410  memory of such an allocation is mapped anymore.</p>
```

Judgment: **SUPPORTED**.

- "counts anonymous mappings such as brk and MAP_ANONYMOUS" — direct restatement of 1406–1407.
- "carries a process heap rather than page cache" — entailed by the source's own taxonomy: the controller tracks "Userland memory - page cache and anonymous memory" (line 1186, in the row-1 context window), and the `file` key (1412–1413, ~6 lines below the quote) is "memory used to cache filesystem data" — the page-cache side. brk()/sbrk() are the heap-growing calls the source itself names as anon contents, so "carries a process heap" is a fair reading.
- The THP caveat (1408–1410) qualifies completeness of per-allocation accounting, not the anon-vs-page-cache split; it does not contradict the claim.

## Row 3 — the file key

Claim cell: `The file key includes tmpfs and shared memory, so a filesystem cache total also carries tmpfs pages.`

Quote location: lines 1412–1413, `<dt>file</dt>` dd. Same context window as row 2.

```
1412  <dt>file</dt><dd><p>Amount of memory used to cache filesystem data,
1413  including tmpfs and shared memory.</p>
```

Judgment: **SUPPORTED**. "Includes tmpfs and shared memory" restates "including tmpfs and shared memory" (1413); the inference — a filesystem-cache total therefore carries tmpfs pages — follows directly.

## Row 4 — the shmem key

Claim cell: `The shmem key is the swap-backed part of that cached data, covering tmpfs, shm segments and shared anonymous mmap.`

Quote location: lines 1434–1435, `<dt>shmem</dt>` dd. Same context window as rows 2–3.

```
1434  <dt>shmem</dt><dd><p>Amount of cached filesystem data that is swap-backed,
1435  such as tmpfs, shm segments, shared anonymous mmap()s</p>
```

Judgment: **SUPPORTED** (one nuance, no change required).

- "the swap-backed part of that cached data" — "cached filesystem data that is swap-backed" (1434) is a subset description over the same head noun as `file` ("cache filesystem data", 1412); consistent with the entry's own reading rule that `shmem` sits inside `file` and the two must not be added.
- "covering tmpfs, shm segments and shared anonymous mmap" — the source marks the list non-exhaustive ("such as", 1435). The claim's "covering" asserts the three named items are included, which the source entails; it does not assert exclusivity. LOW observation only: the non-exhaustive marker is dropped, so a reader could wrongly infer the list is complete. The entry's Limits ("later kernels add or rename keys") and Reading rules already cover the general point; I propose no replacement under "only where needed".

## Findings

- LOW — entry claims-table row 1 (`corpus/knowledge/oom-memcg-stat-r50.md`, entry lines 18 at `487941b`), claim cell: "rounded up to a page" vs source "rounded up to the closest PAGE_SIZE multiple when read back" (`cgroup-v2.7.2.html:1194-1196`). Replacement cell proposed above (quote and source cells unchanged).
- LOW — entry claims-table row 4 (entry line 21), claim cell: "covering" drops the source's non-exhaustive "such as" (`cgroup-v2.7.2.html:1434-1435`); inclusion of the three named items is still entailed, so no replacement proposed.

Rows 2 and 3: SUPPORTED, no defects, no replacement cells.

## Residual risk and verification gaps

- The row-1 replacement cell was not run through the frozen counter (integrating it means editing the entry, which only the L1 may do; the counter is scored at a landed rev). Floors were checked by manual token analysis only. The L1 should re-run `count-c2.py` after integration; the kill rule is unaffected either way since the counter's quote-location test does not read the claim cell's wording beyond the word floor.
- Quote occurrence was not re-implemented (no tag-stripping/entity-decoding harness); I verified word-level presence of each quote at the cited lines via fragment grep, and the frozen counter reports `located=22 quote_missing=0` at the pinned rev.
- Judgments are scoped to rows 1–4 against the v7.2 copy; the 15-line windows plus the row-1 window (1177–1215) are the only HTML ranges read beyond anchor greps.

## Tooling

No tools installed or upgraded; no pacman use. Scratch `/fast/scratch/hyaku/mori-r50/Mo50bRevRowsCgroupA/` (TMPDIR under it) holds only a read-only `git show` extract of the entry and is removed after this report is written; everything cited is inlined above. Fleet repo untouched (read-only git only).
