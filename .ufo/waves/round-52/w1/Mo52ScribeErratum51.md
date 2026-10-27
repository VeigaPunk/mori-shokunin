# Mo52ScribeErratum51 — round-51 erratum draft (closure D-c, D-d)

Seat: Mo52ScribeErratum51 (scribe, round 52 wave w1). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`
(entering tip for this round `4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d`; data `8524904adb25e44f24d9f25aac7eae909625c18c`).
Assignment: draft the append-only erratum `corpus/lessons/round-51-erratum.md` for the round-51 closure's D-c
(locator drift) and D-d (famzah attribution), re-deriving every S493 locator from the committed copy and
re-fetching the refused famzah page. No lane file edited; the draft is fenced in §4 and the L1 integrates.

Scratch: `/fast/scratch/hyaku/mori-r52/Mo52ScribeErratum51/` (removed at the end; every cited byte is pasted here
first).

## 1. D-c — S493 locators re-derived from the committed copy

Source of truth: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r51/show_mem.c.v7.2`,
sha256 `dba76b263bbdf93323a277a29c9281a892ff3fb35ddd6f0ddaf9ba1acb5b02f5`, 464 lines. That digest equals both the
S493 row cell (`corpus/SOURCES.md:272`, `dba76b263b…b02f5`) and the round-51 freeze pin
(`.ufo/waves/round-51/evidence/freeze-sha256.txt:5`).

Live-source control (so the drift is prose, not a stale copy): fetched
`https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/show_mem.c` on 2026-10-26 into scratch,
`http=200 bytes=13204`, sha256 `dba76b263bbdf93323a277a29c9281a892ff3fb35ddd6f0ddaf9ba1acb5b02f5`, and
`cmp` against the committed copy printed nothing and exited 0 (`CMP_IDENTICAL`).

Literal commands and outputs (`F=/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r51/show_mem.c.v7.2`):

```
$ grep -nF 'unsigned long totalreserve_pages __read_mostly;' "$F"
23:unsigned long totalreserve_pages __read_mostly;
$ grep -nF 'long si_mem_available(void)' "$F"
32:long si_mem_available(void)
$ grep -nF 'available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;' "$F"
47:	available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;
$ grep -nF 'pagecache = global_node_page_state(NR_ACTIVE_FILE) +' "$F"
54:	pagecache = global_node_page_state(NR_ACTIVE_FILE) +
$ grep -nF 'global_node_page_state(NR_INACTIVE_FILE);' "$F"
55:		global_node_page_state(NR_INACTIVE_FILE);
$ grep -nF 'pagecache -= min(pagecache / 2, wmark_low);' "$F"
56:	pagecache -= min(pagecache / 2, wmark_low);
$ grep -nF 'available += pagecache;' "$F"
57:	available += pagecache;
$ grep -nF 'reclaimable = global_node_page_state_pages(NR_SLAB_RECLAIMABLE_B) +' "$F"
64:	reclaimable = global_node_page_state_pages(NR_SLAB_RECLAIMABLE_B) +
$ grep -nF 'global_node_page_state(NR_KERNEL_MISC_RECLAIMABLE);' "$F"
65:		global_node_page_state(NR_KERNEL_MISC_RECLAIMABLE);
$ grep -nF 'reclaimable -= min(reclaimable / 2, wmark_low);' "$F"
66:	reclaimable -= min(reclaimable / 2, wmark_low);
$ grep -nF 'available += reclaimable;' "$F"
67:	available += reclaimable;
$ grep -nF 'if (available < 0)' "$F"
69:	if (available < 0)
$ grep -nF 'available = 0;' "$F"
70:		available = 0;
$ grep -nF 'EXPORT_SYMBOL_GPL(si_mem_available);' "$F"
73:EXPORT_SYMBOL_GPL(si_mem_available);
$ grep -nF 'wmark_low += low_wmark_pages(zone);' "$F"
41:		wmark_low += low_wmark_pages(zone);
```

All fifteen greps exited 0. Old → new, against the `### Spot-check` bullet at
`corpus/lessons/round-51.md:83-84` (each cited locator is quoted there verbatim):

| cited in round-51.md:83-84 | quoted words / object | observed now | old → new |
|---|---|---|---|
| `:23` | `unsigned long totalreserve_pages __read_mostly;` | 23 | 23 → 23 (correct) |
| `:32` | `long si_mem_available(void)` | 32 | 32 → 32 (correct) |
| `:47` | `available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;` | 47 | 47 → 47 (correct) |
| `:55-57` | `pagecache = … NR_ACTIVE_FILE + … NR_INACTIVE_FILE` | 54-55 (the pagecache block is 54-57, `available += pagecache;` at 57) | 55-57 → **54-55** |
| `:62` | `pagecache -= min(pagecache / 2, wmark_low);` | 56 | 62 → **56** |
| `:67-69` | reclaimable slab/misc terms under the same `min(… / 2, wmark_low)` cap | 64-66 (terms 64-65, cap 66; `available += reclaimable;` at 67) | 67-69 → **64-66** |
| `:71-72` | `if (available < 0) available = 0;` | 69-70 | 71-72 → **69-70** |
| `:73` | `EXPORT_SYMBOL_GPL(si_mem_available);` | 73 | 73 → 73 (correct) |

This reproduces the closure's mapping exactly (`corpus/lessons/round-51-verifier-spotcheck.md:35-37`: "cites
`:55-57`, `:62`, `:67-69`, `:71-72`; `grep -n` … gives 54-55, 56, 64-66, 69-70").

Scope of the drift, checked so the erratum does not overstate it:

- the lesson's own S493 decision row (`corpus/lessons/round-51.md:29`) is correct — quote "copy lines 54-56",
  scope "(47)", "(54-57)", "(64-67)", "(69-70)", "(40-41)";
- the registry anchor cell (`corpus/SOURCES.md:272`) is correct — `mm/show_mem.c:23,32-73`;
- the freeze pin is correct — `.ufo/waves/round-51/evidence/freeze-sha256.txt:5` carries `dba76b26…b02f5` for
  `corpus/evidence/sources-r51/show_mem.c.v7.2`;
- therefore only the `### Spot-check` prose drifts; the admit decision reads off the same lines and is unaffected.

## 2. D-d — famzah page re-fetched and attribution checked

```
$ curl -sS -L -o famzah.html -w 'http=%{http_code} bytes=%{size_download}\n' \
    https://blog.famzah.net/2014/09/22/know-your-linux-memory-usage/
http=200 bytes=134432
$ sha256sum famzah.html
07abeb2d3d88a807e4e515c26695248d403ceb7109b3fefe8a2d0cfcfd7bc8e5  famzah.html
$ grep -c 'MemAvailable' famzah.html
0
$ echo "rc=$?"
rc=1
$ grep -o -i 'memavailable' famzah.html | wc -l
3
$ awk '{n=gsub(/[Mm]em[Aa]vailable/,"&"); if(n) print NR": "n}' famzah.html
574: 2
779: 1
$ grep -o 'https://github.com/famzah/linux-memavailable-procfs' famzah.html | wc -l
2
```

Second fetch, same seat, minutes later (the page is not byte-stable):

```
$ curl -sS -L -o famzah.html -w 'http=%{http_code} bytes=%{size_download}\n' \
    https://blog.famzah.net/2014/09/22/know-your-linux-memory-usage/
http=200 bytes=134475
$ sha256sum famzah.html
0de988789c371c2c800a2b5fc320389d307efa390c11fb55dfc7061070ada6bb  famzah.html
$ grep -c 'MemAvailable' famzah.html; echo "rc=$?"
0
rc=1
$ grep -o -i 'memavailable' famzah.html | wc -l
3
$ awk '{n=gsub(/[Mm]em[Aa]vailable/,"&"); if(n) print NR": "n}' famzah.html
574: 2
779: 1
```

The counted facts agree across both fetches; the bytes do not (134432 vs 134475, different sha256). The page embeds
per-request nonces and rotating chrome — the nav-previous target differed between the two fetches
(`/2014/09/24/authentication-for-google-sites-liberation/` vs `/2014/08/06/authentication-for-google-sites-liberation/`).
So no page digest is a reproducible pin, and the line numbers below are as observed in both fetches.

The three case-insensitive occurrences are the lowercase helper-repository name `linux-memavailable-procfs`:
twice at HTML line 574 (link `href` and link text) and once at line 779 (the next-post navigation URL
`…/2014/09/24/memavailable-metric-for-linux-kernels-before-3-14-in-procmeminfo/`).

Attribution. The comment block containing line 574 opens at line 564 with
`class="comment byuser comment-author-famzah bypostauthor even depth-2"`; its stripped text is:

```
Ivan Zahariev
May 13, 2017 at 10:32 am
Take a look at the following project which is a working example on how to calculate the Total available
(free) memory: https://github.com/famzah/linux-memavailable-procfs
If your Linux is using a modern “ps” and/or kernel, this info is already available there.
AFAIK, AnonPages is memory mapped by applications.
Please note that tracking free memory down to MBytes is error-prone, I think. I’m not sure if all counters
which are exported are an atomic snapshot of the system.
```

`bypostauthor` plus the byline `September 22, 2014 by Ivan Zahariev`
(`article:published_time` `2014-09-22T08:37:25+00:00`) make the 2017 comment the blog author's own reply, not "a
reader's 2017 comment" (`corpus/lessons/round-51.md:96-98`). Also, "the only occurrence of the string on the page"
holds only case-sensitively; case-insensitively there are three, one of which is not comment text at all. The
refusal stands on the lesson's substantive reasons (non-primary, no sentence defining the estimate, article and
comment text interleaved).

## 3. Draft — `corpus/lessons/round-51-erratum.md` (fenced, append-only; target absent before this draft)

House shape copied from `corpus/lessons/round-39-erratum.md`: title line `# Round-N erratum — append-only
corrections to round-N records`, then prose paragraphs naming what the filed record said, what the bytes show, and
what is superseded, with no in-place edit of the filed lesson.

```markdown
# Round-51 erratum — append-only corrections to round-51 records

The round-51 lesson's `### Spot-check` S493 bullet (`corpus/lessons/round-51.md:83-84`) cites four locators that
drift from the committed copy `corpus/evidence/sources-r51/show_mem.c.v7.2` (sha256
`dba76b263bbdf93323a277a29c9281a892ff3fb35ddd6f0ddaf9ba1acb5b02f5`, byte-identical to the live
`https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/show_mem.c` fetched 2026-10-26, `cmp` equal). Re-derived
with `grep -nF` on the copy: cited `:55-57` for the words `pagecache = … NR_ACTIVE_FILE + … NR_INACTIVE_FILE` is
`:54-55` (the pagecache block runs 54-57, ending `available += pagecache;` at 57); cited `:62` for
`pagecache -= min(pagecache / 2, wmark_low);` is `:56`; cited `:67-69` for the reclaimable slab/misc terms under
the same `min(… / 2, wmark_low)` cap is `:64-66` (terms 64-65, cap 66; `available += reclaimable;` at 67); cited
`:71-72` for `if (available < 0) available = 0;` is `:69-70`. The bullet's `:23`, `:32`, `:47` and `:73` locators
are correct. The lesson's own S493 row (`corpus/lessons/round-51.md:29`: quote lines 54-56; scope 47, 54-57,
64-67, 69-70, 40-41), the registry anchor cell (`corpus/SOURCES.md:272`, `mm/show_mem.c:23,32-73`) and the freeze
pin (`.ufo/waves/round-51/evidence/freeze-sha256.txt:5`) all carry the correct numbers, so the drift is confined to
the spot-check prose and the admit decision is unaffected (round-51 closure §1 D-c, §5 item 5). The filed lesson
is not rewritten; this erratum is the correction.

The same lesson's third spot-check decision (`corpus/lessons/round-51.md:96-98`) calls the only occurrence of the
string on the refused famzah page "a reader's 2017 comment". Re-fetched twice on 2026-10-26 (HTTP 200 both times;
the page's bytes vary per request, so no digest is pinned): the exact string `MemAvailable` occurs 0 times
(case-sensitive `grep -c` → 0, exit 1). The three case-insensitive `memavailable` occurrences are the
lowercase repository name `linux-memavailable-procfs` — twice inside the comment whose HTML class is
`comment byuser comment-author-famzah bypostauthor` (the post author's own reply, Ivan Zahariev, May 13, 2017 at
10:32 am) and once in the next-post navigation URL. So the hit is the blog author's reply, not a reader's comment,
and "the only occurrence" holds only case-sensitively. The refusal stands on the lesson's stated reasons
(non-primary, no sentence defining the estimate); only the attribution and the occurrence count are corrected here
(round-51 closure §1 D-d, §5 item 5).
```

## 4. Checks run and not run

Run (all read-only): `read` of contract / closure / lessons / SOURCES; `grep -nF` ×15 on the committed copy;
`sha256sum` on copy and live fetch; `cmp` copy vs live; two `curl` fetches of the famzah page into scratch; `grep -c`,
`grep -o -i`, `awk` occurrence counts; `sed`/`awk` comment-block extraction; `mkdir -p` of the seat scratch and
`rm -rf` of it; `scripts/hyaku/disk-guard.sh status` (free `/fast/scratch/hyaku` 608.1G, use 25%; no ENOSPC).
No `pacman`, no tool install, no network write, no kernel/sysctl/cgroup write, no journal/systemctl call, no
kernel log message grep.

Not run: `count-c1.py`, `count-c2.py`, any lane gate, any control fixture, any git mutation, any `git status` in
the lane. No claim is scored here; this seat is a scribe.

## 5. Touched surfaces

- written: this report only, `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/w1/Mo52ScribeErratum51.md`;
- scratch `/fast/scratch/hyaku/mori-r52/Mo52ScribeErratum51/` created and removed;
- not touched: `corpus/lessons/round-51.md` (filed bytes stay frozen), `corpus/lessons/round-51-erratum.md` (does
  not exist yet — integration is the L1's), `corpus/SOURCES.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`, `tools/`,
  `considerthese/`, every other round-52 path.

## 6. Out of scope

- No evaluation of the C1/C2 counters, controls, predicates or kill rules; no votes (this seat is not an
  ENTAILMENT seat and emits no vote line).
- No check of the round-51 lesson's other S492/S494/S495/S496 prose, its Mistakes table, or the round-51 SOURCES
  cells beyond the S493 anchor cell needed to bound the drift.
- No judgment on whether the round-51 closure's D-c mapping or the lesson's admit decision should change: the
  decision reads off the same lines and is unaffected.

## Findings

- **MED** — `corpus/lessons/round-51.md:83-84`: the `### Spot-check` S493 locators drift (`:55-57`, `:62`,
  `:67-69`, `:71-72` vs `54-55`, `56`, `64-66`, `69-70`); corrected by the §3 erratum draft; the lesson's own
  S493 row at `:29`, `corpus/SOURCES.md:272` and the freeze pin are correct.
- **MED** — `corpus/lessons/round-51.md:96-98`: the famzah paragraph attributes the 2017 `bypostauthor` reply
  (Ivan Zahariev, May 13, 2017) to "a reader" and says the string occurs once; exact `MemAvailable` occurs 0
  times and the three case-insensitive hits are the lowercase repo name and a nav URL. Corrected by the same
  erratum; the refusal stands.
- **LOW** — the famzah page is not byte-stable: two fetches minutes apart returned 134432 and 134475 bytes with
  different sha256, and the nav-previous target changed between them; a future re-check must count occurrences and
  re-read the comment's `bypostauthor` class, never compare a page digest (this is why the erratum pins none).
- **LOW** — the same paragraph's "article and comment text are interleaved on the page" is not what the single
  cited occurrence demonstrates (one hit is navigation chrome); the refusal's substantive reasons (non-primary,
  no quotable sentence defining the estimate) are independently observed and unaffected.
- **LOW** — `.ufo/waves/round-52/evidence/freeze-sha256.txt` pins no round-51 source copy (it lists round-52
  material only), so the erratum's pin check had to use `.ufo/waves/round-51/evidence/freeze-sha256.txt:5`; the
  two digest values agree, but a reader of round 52 alone cannot re-derive the pin from the round-52 freeze list.

## Artifact paths

- draft target: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-51-erratum.md` (not written;
  fenced in §3)
- source copy: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r51/show_mem.c.v7.2`
- registry row: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md:272`
- filed lesson: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-51.md:29,83-84,96-98`
- closure: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-51-verifier-spotcheck.md:35-40,173-174`
- house shape: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-39-erratum.md`
- receipt: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/w1/Mo52ScribeErratum51.md` (this file)
