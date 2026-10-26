# Mo51ScribeGateQuotes — Gate lines for S492–S496 (round 51, wave w1)

Seat: scribe (leaf, no subagents). Assignment: write the lesson `## Gate` lines for the five C2 sources — URL,
access date 2026-10-26, a located verbatim quote ≤ 25 words with its line numbers in the committed copy under
`corpus/evidence/sources-r51/`, and the live sha256 fetched today and compared with the copy. Draft is in
§Draft below; nothing outside this report was written.

State read (read-only): lane tip `b504cb1701568a0038aab9d98ec13d28eff801da`, freeze
`4677910eae6df3dabd38fe9a0daf1945146a1110` (2026-10-26T19:37:01-03:00), data
`87e0c374537557754bf71dd68036ded3ddc6699c` (2026-10-26T19:37:45-03:00).

## Behavior

1. Fetched each of the five source URLs live with `curl` into scratch (`/fast/scratch/hyaku/mori-r51/
   Mo51ScribeGateQuotes/`), all HTTP 200, and hashed the fetched bytes.
2. Hashed the committed copies under `corpus/evidence/sources-r51/`; compared byte-for-byte with the fetch
   (`sha256` equal **and** `bytes` equal for all five).
3. Chose one ≤ 25-word quote per source, located it in the committed copy after whitespace collapse
   (`re.sub(r'\s+', ' ')`), reported the copy line span, and confirmed one occurrence per copy.
4. Checked the frozen copy list (`sha256sum -c .ufo/waves/round-51/evidence/freeze-sha256.txt`) and the registry
   placement of the five rows (appended after S491 at `corpus/SOURCES.md:271-275`, 11 cells each).
5. Removed scratch before finishing (output below). No clone, no fixture repo, no pacman, no tool install,
   no mutation of the lane, the fleet repo, `~/.local/bin` or `PATH`. Host reads only.

## Receipts

### Scratch and disk guard

```
$ mkdir -p /fast/scratch/hyaku/mori-r51/Mo51ScribeGateQuotes/{tmp,fetch}
$ scripts/hyaku/disk-guard.sh status
rc=0            (free /fast 589G at start)
$ df -h /fast | tail -1
/dev/nvme1n1p2  804G  215G  589G  27% /fast
```

### Live fetch (scratch/fetch, 2026-10-26T19:46:37-03:00)

Command shape: `curl -sS -L -o <name> -w '%{http_code}' --max-time 60 --max-filesize 50000000 <url>`
(`set -o pipefail`; `cd` into the scratch fetch dir first).

```
proc.rst.v7.2    http=200 bytes=107560 sha256=e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126
show_mem.c.v7.2  http=200 bytes=13204  sha256=dba76b263bbdf93323a277a29c9281a892ff3fb35ddd6f0ddaf9ba1acb5b02f5
meminfo.c.v7.2   http=200 bytes=6046   sha256=d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda
mm_inline.h.v7.2 http=200 bytes=19417  sha256=2d4accbbc1ec139bfe11a356d4d17a55a2543769f3e10057a8a8584429c45ef6
34e431b0.patch   http=200 bytes=5199   sha256=9f571a04fc365858d8c82d31b309217a5e40f37877732da70416b0b1b42563d0
```

### Committed copies vs live bytes

```
proc.rst.v7.2    e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126
show_mem.c.v7.2  dba76b263bbdf93323a277a29c9281a892ff3fb35ddd6f0ddaf9ba1acb5b02f5
meminfo.c.v7.2   d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda
mm_inline.h.v7.2 2d4accbbc1ec139bfe11a356d4d17a55a2543769f3e10057a8a8584429c45ef6
34e431b0.patch   9f571a04fc365858d8c82d31b309217a5e40f37877732da70416b0b1b42563d0
```

All five copy hashes equal their live hash and the script printed `same_bytes=yes` for each (it compared the raw
byte strings as well as the digests).

### Located quotes (whitespace-collapsed substring test)

Script (run from scratch; exit code recorded):

```python
def collapse(text):            # single space for any whitespace run, offset -> line map kept
    ...
coll, lm = collapse(open(path).read()); s, _ = collapse(quote)
idx = coll.find(s); ok = idx >= 0 and len(quote.split()) <= 25
```

Output:

```
S492  proc.rst.v7.2     words=18 (<=25: yes) located=PASS lines=1128-1130
S492b proc.rst.v7.2     words=16 (<=25: yes) located=PASS lines=1139-1140
S493  show_mem.c.v7.2   words=11 (<=25: yes) located=PASS lines=54-56
S494  meminfo.c.v7.2    words=7  (<=25: yes) located=PASS lines=48-49
S494b meminfo.c.v7.2    words=4  (<=25: yes) located=PASS lines=62
S495  mm_inline.h.v7.2  words=19 (<=25: yes) located=PASS lines=25-26
S496  34e431b0.patch    words=22 (<=25: yes) located=PASS lines=11-12
ALL_PASS=yes
exit=0
```

The first run of the same test reported `S495 … located=FAIL` because the quote I had drafted dropped the doc
comment's ` * ` continuation marker at the 25→26 line break; the corrected quote keeps it verbatim and passes.

Occurrence count per copy (same collapse): `S492=1, S492b=1, S493=1, S494=1, S495=1, S496=1` — each quote occurs
exactly once in its copy.

Quoted regions of the committed copies (line numbers as used in the draft; the copies are the live bytes):

```
## proc.rst.v7.2:1128-1130
1128	              applications, without swapping. Calculated from MemFree,
1129	              SReclaimable, the size of the file LRU lists, and the low
1130	              watermarks in each zone.
## show_mem.c.v7.2:54-56
54		pagecache = global_node_page_state(NR_ACTIVE_FILE) +
55			global_node_page_state(NR_INACTIVE_FILE);
56		pagecache -= min(pagecache / 2, wmark_low);
## meminfo.c.v7.2:48-49
48		cached = global_node_page_state(NR_FILE_PAGES) -
49				total_swapcache_pages() - i.bufferram;
## mm_inline.h.v7.2:25-26
25	 * 0 if @folio is a normal anonymous folio, a tmpfs folio or otherwise
26	 * ram or swap backed folio.
## 34e431b0.patch:11-12
11	It is wrong because Cached includes memory that is not freeable as page
12	cache, for example shared memory segments, tmpfs, and ramfs, and it does
```

### Frozen bytes and registry placement

```
$ sha256sum -c .ufo/waves/round-51/evidence/freeze-sha256.txt
corpus/evidence/sources-r51/34e431b0.patch: OK
corpus/evidence/sources-r51/meminfo.c.v7.2: OK
corpus/evidence/sources-r51/mm_inline.h.v7.2: OK
corpus/evidence/sources-r51/proc.rst.v7.2: OK
corpus/evidence/sources-r51/show_mem.c.v7.2: OK
… (.ufo/waves/round-51/contract.md, controls/, counters, evidence receipts) …
21 OK lines, 0 failures; exit 0
$ git log -1 --format='%H %cI' -- corpus/evidence/sources-r51/
4677910eae6df3dabd38fe9a0daf1945146a1110 2026-10-26T19:37:01-03:00
  ("round-51: freeze — contract, C1/C2 counters, controls and receipts, five source copies (before any seat)")
$ awk 'NR>=271 && NR<=275 { … }' corpus/SOURCES.md   # pipes per row
271..275 pipes=12 (= 11 cells each)
$ awk 'NR>=268 && NR<=271' corpus/SOURCES.md         # rows S489, S490, S491 then S492 at :271
```

### Duplicate-URL check (W04)

```
$ grep -o -n "https://[^ |]*<path>" corpus/SOURCES.md
Documentation/filesystems/proc.rst  -> lines 88 (S082, mined), 174 (S168, rejected), 271 (S492, mined)
mm/show_mem.c                       -> line 272 only
fs/proc/meminfo.c                   -> line 273 only
include/linux/mm_inline.h           -> line 274 only
34e431b0ae39                        -> line 275 only
```

S082 (`corpus/SOURCES.md:88`) records the same URL and sha256 prefix `e760f716f8278dee` (16 hex chars); S168
(`:174`) is the rejected same-scope duplicate. Both match what row S492 states.

### Cleanup

```
$ du -sh /fast/scratch/hyaku/mori-r51/Mo51ScribeGateQuotes     164K
$ rm -rf -- /fast/scratch/hyaku/mori-r51/Mo51ScribeGateQuotes
rm_rc=0
SCRATCH_GONE
$ df -h /fast | tail -1
/dev/nvme1n1p2  804G  202G  602G  26% /fast
```

Tooling: nothing installed or upgraded (no pacman transaction — paused host-wide; none attempted).

## Draft — `corpus/lessons/round-51.md`, `## Gate` (new rows only)

```markdown
## Gate

### New SOURCES rows (each opened this round; rule 1)

Five rows, all opened 2026-10-26, appended after S491 (`corpus/SOURCES.md:271-275`), 11 cells each, status
`mined`, recheck `on-release`, `used-by corpus/knowledge/memavailable-estimate-r51.md`. The five documents were
copied into `corpus/evidence/sources-r51/` at the freeze `4677910e` and pinned by sha256 in
`evidence/freeze-sha256.txt` (`sha256sum -c` → 21/21 `OK`, rc 0); the live bytes re-fetched on
2026-10-26T19:46:37-03:00 (HTTP 200 each) matched all five in digest and in bytes
(`w1/Mo51ScribeGateQuotes.md`), so each row is grounded in bytes this lane holds and the page it names still
serves them. Every quote below was located by this wave's quote seat in the committed copy (whitespace-collapsed
substring, one occurrence per copy) and re-checked at ≤ 25 words; the line numbers are the committed copy's, which
are the live bytes today.

| id | URL / locator | accessed | ≤25-word located quote | decision |
|---|---|---|---|---|
| S492 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst — copy `proc.rst.v7.2` (sha256 `e760f716…40d126`) | 2026-10-26 | "Calculated from MemFree, SReclaimable, the size of the file LRU lists, and the low watermarks in each zone." (18 words) — `MemAvailable` entry, copy lines 1128-1130 (the quote is also the entry's row-2 quote); the `Cached` sentence the entry's tmpfs claim uses, "In-memory cache for files read from the disk (the pagecache) as well as tmpfs & shmem." (16 words), is at 1139-1140 inside the row's `1138-1141` anchor | admit, mined, kind docs, tier A, recheck `on-release`; scope is the `/proc/meminfo` field text at v7.2 (MemFree, MemAvailable, Cached, Shmem, KReclaimable, SReclaimable definitions), not S082's mountinfo layout (`corpus/SOURCES.md:88`) and not the code that computes the value (S493-S495); same URL and bytes as S082 and the rejected same-scope row S168 (`:174`), so this row is a **W04** warning — informational, separate scope; S082 pins only a 16-hex prefix, so "same bytes" rests on this row's full hash |
| S493 | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/show_mem.c — copy `show_mem.c.v7.2` (sha256 `dba76b26…b02f5`) | 2026-10-26 | "pagecache = global_node_page_state(NR_ACTIVE_FILE) + global_node_page_state(NR_INACTIVE_FILE); pagecache -= min(pagecache / 2, wmark_low);" (11 words) — `si_mem_available()`, copy lines 54-56 | admit, mined, kind code, tier A, recheck `on-release`; scope is `si_mem_available()` at tag v7.2 — free pages minus `totalreserve_pages` (47), plus the active+inactive file LRU pages less `min(half, wmark_low)` (54-57), plus reclaimable slab and other reclaimable kernel pages less the same holdback (64-67), clamped at zero (69-70), with `wmark_low` summed over zones (40-41) — and not the global OOM report `__show_mem()` that shares the file; the quote is the file-cache term and its holdback, the reason the term is not the whole page cache |
| S494 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/meminfo.c — copy `meminfo.c.v7.2` (sha256 `d6c58074…3deda`) | 2026-10-26 | "cached = global_node_page_state(NR_FILE_PAGES) - total_swapcache_pages() - i.bufferram;" (7 words) — copy lines 48-49 | admit, mined, kind code, tier A, recheck `on-release`; scope is the print path: `show_val_kb()` shifting pages by `PAGE_SHIFT - 10` and writing ` kB` (28-32), the `Cached` derivation (48-51, the different base the entry contrasts with the two file LRU lists), and the adjacent `MemFree:`/`MemAvailable:` lines (61-62) where `MemAvailable` prints the value `si_mem_available()` returned at 56; the estimate's arithmetic itself is S493's scope, not this row's |
| S495 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/mm_inline.h — copy `mm_inline.h.v7.2` (sha256 `2d4accbb…c45ef6`) | 2026-10-26 | "0 if @folio is a normal anonymous folio, a tmpfs folio or otherwise * ram or swap backed folio." (19 words) — `folio_is_file_lru()` doc comment, copy lines 25-26; the `*` is the comment's continuation marker at the line break and is part of the located text | admit, mined, kind code, tier A, recheck `on-release`; scope is `folio_is_file_lru()`'s return contract and its one-line body `return !folio_test_swapbacked(folio);` (28-31): file LRU for page-cache folios and MADV_FREE'd anon folios, anon LRU for normal anonymous, tmpfs and swap-backed folios — why the estimate's file-LRU term cannot include tmpfs; the entry's two claims both draw on this block (23-26) |
| S496 | https://github.com/torvalds/linux/commit/34e431b0ae398fc54ea69ff85ec700722c9da773.patch — copy `34e431b0.patch` (sha256 `9f571a04…563d0`) | 2026-10-26 | "It is wrong because Cached includes memory that is not freeable as page cache, for example shared memory segments, tmpfs, and ramfs" (22 words) — commit message, copy lines 11-12 | admit, mined, kind code, tier A, recheck `on-release`; scope is the commit's stated motivation (free plus cached overstates startable memory: Cached holds non-freeable shared memory, tmpfs and ramfs, and omits reclaimable slab, lines 6-14) and its original 2014 formula hunk for `fs/proc/meminfo.c`, not v7.2 behaviour; this is the first row to carry the URL (no W04); the bytes are GitHub's `.patch` rendering (mbox header at line 1), so an `on-release` recheck compares a rendered patch, not a raw blob |
```

## Limits (named)

- A located quote proves the words occur in the committed copy and that today's fetched bytes hash to the same
  digest; it proves nothing about whether the row's scope text is the best reading of them — that is the
  entailment seats' judgment, not this seat's (this report carries no entailment vote).
- The live comparison is one fetch per URL at 2026-10-26T19:46:37-03:00. It does not prove the tag `v7.2` is
  immutable upstream; a future re-tag would change the bytes and the `on-release` recheck would show it.
- `curl -L` was used for all five, so each digest is of the body after any redirect. I recorded one redirect
  check only: a header request to the `show_mem.c` URL answered `HTTP/2 200`, `content-length: 13204`, `etag
  "d5681828c3170c5c99b484cb748571c2ceb1a95bf89268e1acf86bd5c54ce2db"`; redirect chains for the other four were
  not inspected. For the `.patch` URL the body is GitHub's rendered patch. The digest therefore pins the served
  body, not an upstream git object id.
- Line numbers are the committed copies' line numbers (which equal today's live bytes). A copy reformatted by
  whitespace changes could shift them without changing the words; the collapse test still locates the quote.
- The word count used is whitespace tokens, the convention round 50's Gate used for code quotes (its `pr_err(`
  line is 12 such tokens). S493 and S494 are code quotes, so their counts are token counts, not prose word counts.

## Out of scope / not done

- No edit to `SKILL.md`, `SHONEN.md`, `SCORECARD.md`, `LOG.md`, `corpus/`, `tools/`, `considerthese/`, or any
  other file under `.ufo/waves/round-51` — only this report was written. The L1 integrates.
- `sources-census.sh validate`, both counters and the C1 controls were not run by this seat (other seats own
  those); nothing here is a claim about C1 or about C2's counter readings.
- No OOM trigger, no cgroup/sysctl/swap/watermark change, no kernel log text read, no journal action.

## Findings

| # | severity | finding | file / line |
|---|---|---|---|
| 1 | LOW | A quote from the `folio_is_file_lru()` doc comment only locates under whitespace collapse if it keeps the ` * ` continuation marker at the 25→26 line break; a natural-punctuation re-quote of the same sentence fails the locate test (my first draft did, and the entry's own two quotes carry the marker for this reason). Anyone re-quoting this block must keep the marker. | `corpus/evidence/sources-r51/mm_inline.h.v7.2:25-26` (copied into the S495 draft row) |
| 2 | LOW | S496's provenance is a GitHub-rendered `.patch` (mbox `From … Mon Sep 17 00:00:00 2001` header, author/date/`Signed-off-by` block, `index` lines), not a raw blob or a git object id: the pinned sha256 tracks that rendering, so a change in GitHub's patch rendering would appear as source drift on the `on-release` recheck even with the commit unchanged. The row's scope is the commit's motivation plus its 2014 formula hunk, which the rendering carries. | `corpus/SOURCES.md:275`, `corpus/evidence/sources-r51/34e431b0.patch:1,38-40` |
| 3 | LOW | S492 carries the same URL and bytes as S082 (W04, informational): live fetch today is `e760f716…40d126`, matching S082's recorded prefix `e760f716f8278dee` and confirming the row's own note; S082 pins only 16 hex characters, so the "same bytes" statement rests on S492's full hash rather than on S082's cell. No action needed for this round; a future registry pass could lengthen S082's pin. | `corpus/SOURCES.md:88` (S082), `:174` (S168 rejected), `:271` (S492) |
| 4 | LOW | The five rows' `used-by` cells name `corpus/knowledge/memavailable-estimate-r51.md`, but no row names the lesson that carries these Gate lines; the round-50 pattern cites the quote seat report inside the Gate decision column, not via `used-by` — noting it so the L1 can decide whether the lesson belongs in `used-by` for S492-S496. | `corpus/SOURCES.md:271-275` |
