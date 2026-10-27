# Mo54ExecRefetchDocs — rendered cgroup-v2 re-fetch (S520, S489) and the seven S489-derived quote rows

seat: Mo54ExecRefetchDocs (wave w1, mori round 54)
scope: independent re-fetch of the rendered page `https://docs.kernel.org/7.3/admin-guide/cgroup-v2.html` (S520) twice at
least a minute apart and compare its sha256 with the pin in `.ufo/waves/round-54/count-c1.py` and the committed copy
`corpus/evidence/sources-r54/cgroup-v2.7.3.html`; re-fetch `https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html` and
compare with `corpus/evidence/sources-r50/cgroup-v2.7.2.html` (S489); fetch the raw rst at cgit `?h=v7.3`
(`Documentation/admin-guide/cgroup-v2.rst`) and check that each of the seven S489-derived quotes of
`corpus/knowledge/kernel-v7.3-recheck-r54.md` rows 9–15 occurs in it; answer whether the rendered page is tag-pinned.
scratch: `/fast/scratch/hyaku/mori-r54/Mo54ExecRefetchDocs` (created with `mkdir -p`, `TMPDIR` set under it, removed at end of seat)
tooling: nothing installed, nothing upgraded, no pacman invocation. Writes: this report only. No file under
`corpus/`, `tools/`, `considerthese/` or the round-54 wave dir other than this report was touched.
I am not a RECHECK or ENTAILMENT seat: this report casts no vote and its lines are not counter input.

## 1. Fetch 1 — rendered 7.3 page (2026-10-27T04:39:40Z)

```
$ cd /fast/scratch/hyaku/mori-r54/Mo54ExecRefetchDocs
$ curl -sS --max-time 120 -o bad59863.body -w 'http=%{http_code} bytes=%{size_download} time=%{time_total}\n' \
    https://docs.kernel.org/7.3/admin-guide/cgroup-v2.html
http=200 bytes=172967 time=0.264878
curl_exit=0
$ sha256sum bad59863.body
b478c1bae99899df476d6b4989cbb516f7ca93c5f009cdff64b802bbc24f3d4b  bad59863.body
```

Pin in the C1 counter (`count-c1.py` `_COPIES`, key `docs:admin-guide/cgroup-v2.html`) and the committed copy:

```
$ sha256sum corpus/evidence/sources-r54/cgroup-v2.7.3.html
b478c1bae99899df476d6b4989cbb516f7ca93c5f009cdff64b802bbc24f3d4b  corpus/evidence/sources-r54/cgroup-v2.7.3.html
$ wc -l corpus/evidence/sources-r54/cgroup-v2.7.3.html
3314 corpus/evidence/sources-r54/cgroup-v2.7.3.html
```

Byte identity was also checked directly, not only by hash: `pin==fetch73: True` (Python string comparison of the two
decoded files). So the freeze-time fetch of S520 reproduces from upstream today, byte for byte.

## 2. Fetch 2 — same URL, 67.3 s later (2026-10-27T04:40:47Z)

```
$ date -u +%FT%T.%NZ   # before fetch 1 body: 2026-10-27T04:39:40.036589351Z
first-fetch mtime UTC: 2026-10-27T04:39:40.305209Z elapsed_now_s=67.3
$ curl -sS --max-time 120 -o cg73-b.html -D cg73-b.hdr -w 'http=%{http_code} bytes=%{size_download} time=%{time_total}\n' \
    https://docs.kernel.org/7.3/admin-guide/cgroup-v2.html
http=200 bytes=172967 time=0.061303
curl_exit=0
$ sha256sum cg73-b.html bad59863.body corpus/evidence/sources-r54/cgroup-v2.7.3.html
b478c1bae99899df476d6b4989cbb516f7ca93c5f009cdff64b802bbc24f3d4b  cg73-b.html
b478c1bae99899df476d6b4989cbb516f7ca93c5f009cdff64b802bbc24f3d4b  bad59863.body
b478c1bae99899df476d6b4989cbb516f7ca93c5f009cdff64b802bbc24f3d4b  corpus/evidence/sources-r54/cgroup-v2.7.3.html
```

Response headers of fetch 2 (the ones that bear on determinism):

```
server: nginx
last-modified: Sun, 18 Oct 2026 23:26:39 GMT
date: Tue, 27 Oct 2026 04:40:47 GMT
age: 1129
x-cache: HIT
x-cache-hits: 1
content-length: 172967
```

No `etag` header is served. Both fetches were answered from the same CDN object (`x-cache: HIT`, `age: 1129` at
04:40:47 s means the cached object was 1129 s old at fetch 2, i.e. it was already cached before fetch 1). The
determinism statement this supports is therefore "the same cached object over 67 s", not "independent origin builds";
see the limit in §6.

## 3. Rendered 7.2 page vs S489 (2026-10-27T04:41:13Z)

```
$ curl -sS --max-time 120 -o d37835ef.body -w 'http=%{http_code} bytes=%{size_download} time=%{time_total}\n' \
    https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html
http=200 bytes=168438 time=0.604125          # first fetch, 04:39:40Z
$ curl ... -o cg72-b.html ...                 # second fetch, 04:41:13Z
http=200 bytes=168438 time=0.066715
curl_exit=0
$ sha256sum cg72-b.html corpus/evidence/sources-r50/cgroup-v2.7.2.html
2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34  cg72-b.html
2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34  corpus/evidence/sources-r50/cgroup-v2.7.2.html
$ wc -l corpus/evidence/sources-r50/cgroup-v2.7.2.html
3257 corpus/evidence/sources-r50/cgroup-v2.7.2.html
```

Headers of the 7.2 fetch: `last-modified: Sun, 16 Aug 2026 22:59:28 GMT`, `age: 93`, `x-cache: HIT`,
`content-length: 168438`. The hash is the one S489's own row records (`corpus/SOURCES.md:268`, "sha256
2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34") and the one in
`.ufo/waves/round-50/evidence/freeze-sha256.txt:1` and `corpus/knowledge/oom-memcg-stat-r50.md:7` (the round-50
`recheck: 90d` line). So S489 reproduces too.

## 4. Raw rst at cgit `?h=v7.3`, and what the rendered page was built from

```
$ curl -sS --max-time 120 -o acabd24b.body -w 'http=%{http_code} bytes=%{size_download} time=%{time_total}\n' \
    'https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/cgroup-v2.rst?h=v7.3'
http=200 bytes=135851 time=0.709502
curl_exit=0
$ sha256sum acabd24b.body
2750c11a6324e18f4d3a9bb63032b55f3268bd7077b80897af2f15a712611b68  acabd24b.body
$ wc -l acabd24b.body
3581        # newline-terminated; Python count("\n")+1 = 3582 counts the empty tail, as expected
```

The page's own source link is `<a href="../_sources/admin-guide/cgroup-v2.rst.txt" rel="nofollow">Page source</a>`
(page footer). Fetching that URL from the same release path:

```
$ curl -sS --max-time 120 -o cg73-src.rst.txt -w 'src http=%{http_code} bytes=%{size_download}\n' \
    https://docs.kernel.org/7.3/_sources/admin-guide/cgroup-v2.rst.txt
src http=200 bytes=135851
$ sha256sum cg73-src.rst.txt acabd24b.body
2750c11a6324e18f4d3a9bb63032b55f3268bd7077b80897af2f15a712611b68  cg73-src.rst.txt
2750c11a6324e18f4d3a9bb63032b55f3268bd7077b80897af2f15a712611b68  acabd24b.body
```

The rst that the `/7.3/` page was built from is byte-identical to the rst the `v7.3` tag resolves to. Tag identity
(read-only `git ls-remote`, no clone, no fetch into the lane):

```
$ timeout 90 git ls-remote https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git 'refs/tags/v7.3' 'refs/tags/v7.3^{}' 'refs/tags/v7.2' 'refs/tags/v7.2^{}'
237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63  refs/tags/v7.2
8d3ae59288f1e7d58d76558a6ee96d533bc5019f  refs/tags/v7.2^{}
091b06388b117fefdcb63336ac09956a4914b961  refs/tags/v7.3
c03c1a14507dfaf8b856c2608f9ac216021fc222  refs/tags/v7.3^{}
exit=0
```

`v7.3` is an annotated tag object `091b06388b117fefdcb63336ac09956a4914b961` dereferencing to commit
`c03c1a14507dfaf8b856c2608f9ac216021fc222`; `v7.2` is `237a1c39…` → commit `8d3ae592…`.

## 5. The seven S489-derived quotes (ledger rows 9–15) in the 7.3 copy and in the tag's rst

Method: HTML read with the counter's own normalisation semantics, independently re-implemented here — script/style
blocks, comments and tags become one space, entities are decoded, runs of whitespace collapse to one space, offsets
keep their position in the raw file so a matched character can be mapped back to a line number (`count-c1.py`
`norm_map`/`lines_of`). The rst was compared two ways: (a) after removing rst inline markup (`` ``lit`` ``,
``` `ref`_ ```, `**bold**`, `*em*`) and collapsing whitespace — the strict arm; (b) as a word-token run
(`[A-Za-z0-9_()]+`, curly apostrophe folded to `'`) — the wording arm.

| h (ledger row) | ledger line (7.3) | match at that line in fetched 7.3 page | match in committed 7.3 copy | rst strict | rst word-run lines | ledger v7.2 line → fetched 7.2 page |
|---|---|---|---|---|---|---|
| 07524a78c749 (9) | 1225 | yes, line 1225 | yes | yes | 1320–1321 | 1194 → 1194–1195 |
| 202158f50bb3 (10) | 1437 | yes, line 1437 | yes | **no** (see below) | 1566–1568 | 1406 → 1406–1407 |
| 41496ae6cbe1 (11) | 1409 | yes, line 1409 | yes | yes | 1534–1535 | 1378 → 1378–1379 |
| 460b0cafc999 (12) | 1430 | yes, lines 1430 and 1636 | yes | **no** (curly apostrophe) | 1559–1560 | 1399,1605 → 1399–1400 and 1605–1606 |
| 51390e34b4d7 (13) | 1465 | yes, line 1465 | yes | yes | 1603–1605 | 1434 → 1434–1435 |
| ed03d041e844 (14) | 1446 | yes, line 1446 | yes | yes | 1577–1580 | 1415 → 1415–1417 |
| fd3728bdc6d6 (15) | 1443 | yes, line 1443 | yes | yes | 1573–1575 | 1412 → 1412–1413 |

Aggregates printed by the checking script: `quotes matched in grabbed 7.3 html AND pin: 7 /7 ; in raw rst: 5 /7`
under the strict arm, and 7/7 under the word-run arm. Every ledger `line` value is reproduced exactly, and the
ledger's "+31" move for all seven rendered-page rows is confirmed (1194→1225, 1406→1437, 1378→1409, 1399/1605→
1430/1636, 1434→1465, 1415→1446, 1412→1443).

The two rst-strict misses, with the exact bytes:

```
$ sed -n '1435,1438p' bad59863.body        # 7.3 page, row 10
<div><dl>
<dt>anon</dt><dd><p>Amount of memory used in anonymous mappings such as
<code class="xref c c-func broken_xref docutils literal notranslate"><span class="pre">brk()</span></code>, <code ...><span class="pre">sbrk()</span></code>, and mmap(MAP_ANONYMOUS). Note that
$ sed -n '1430p' bad59863.body              # 7.3 page, row 12
can show up in the middle. Don’t rely on items remaining in a
$ sed -n '1566,1568p' acabd24b.body | cat -A | cut -c1-200     # tag rst
^I  anon$
^I^IAmount of memory used in anonymous mappings such as$
^I^Ibrk(), sbrk(), and mmap(MAP_ANONYMOUS). Note that
$ sed -n '1559,1560p' acabd24b.body | cat -A                    # tag rst, row 12
^Ican show up in the middle. Don't rely on items remaining in a$
^Ifixed position; use the keys to look up specific values!$
```

Row 10: the rendered page's normalised text carries `brk() ,` / `sbrk() ,` because the `</code>` boundary becomes a
space before the comma; the tag's rst has `brk(), sbrk(),`. Row 12: the rendered page has U+2019 (`Don’t`), the rst has
ASCII `'` (`Don't`). Both ledger quotes are faithful to the copy the counter reads (the HTML page); the divergence is
rendering, not content. The consequence is only this: a recheck that matched these ledger quote strings against rst
bytes verbatim would call rows 10 and 12 absent.

## 6. Is the rendered page tag-pinned?

What the page actually carries (fetched copy, 172967 bytes, 3314 lines):

```
$ grep -c "7\.3\.0" cg73-b.html
1
$ grep -n "blurb" cg73-b.html
42:<p class="blurb">7.3.0</p>
$ grep -o "v7\.3[0-9.a-z-]*" cg73-b.html | sort -u    # (empty: no version string other than the blurb)
$ grep -c "git.kernel.org" cg73-b.html
0
$ tail -12 cg73-b.html    # the footer div
    <div class="footer">
      &#169;The kernel development community.
      |
      Powered by <a href="https://www.sphinx-doc.org/">Sphinx 5.3.0</a>
      &amp; <a href="https://alabaster.readthedocs.io">Alabaster 0.7.16</a>
      |
      <a href="../_sources/admin-guide/cgroup-v2.rst.txt" rel="nofollow">Page source</a>
    </div>
```

- The release marker `7.3.0` exists and occurs exactly once, as `<p class="blurb">7.3.0</p>` inside
  `<div class="sphinxsidebar" role="navigation">` (document line 42) — a **sidebar blurb**, not the footer. The footer
  (last lines of the document) carries only the copyright, `Sphinx 5.3.0`, `Alabaster 0.7.16` and the relative
  "Page source" link.
- The page carries no git tag name, no commit sha and no absolute source URL; a reader cannot recover the tag from the
  bytes. The pin is the URL path `/7.3/` plus that blurb, and it is corroborated *outside* the page: its
  `_sources/admin-guide/cgroup-v2.rst.txt` is byte-identical (sha256 `2750c11a…`) to cgit `?h=v7.3`, and `v7.3` is the
  annotated tag `091b0638…` → commit `c03c1a14…` (§4).
- The path is a per-release path, not a moving series: `https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html` still
  says `7.2.0` at the same document line 42 (`grep -n blurb` → `42:<p class="blurb">7.2.0</p>`, count of `7.2.0` = 1)
  with `last-modified: Sun, 16 Aug 2026 22:59:28 GMT`, although the host runs 7.2.11.

Answer: yes — the fetched page identifies itself as the 7.3.0 release documentation build (and stays 7.3.0-labelled on
a re-fetch 67 s later), and its build source is the tag's rst byte for byte. But the marker sits in the sidebar blurb,
not the footer; S520's SOURCES row says "rendered page footer 7.3.0", which is a wrong location for a right fact
(finding F1).

## 7. Limits of this re-fetch (named, not fixed here)

- L1: determinism across 67 s was measured through a CDN cache (`x-cache: HIT` on both 7.3 fetches, `age: 1129` at the
  second, no `etag`). It shows the same cached object was served twice, not that an independent origin build is
  byte-stable. What would catch origin drift is the sha256 pin (`pins=bad`) and the `_sources` ↔ cgit identity in §4.
- L2: if docs.kernel.org rebuilds the `/7.3/` path (for example for a 7.3.y stable release), the bytes change at an
  unchanged URL. The counter's pin then reads `pins=bad`, which is the designed detection, but the ledger, the seven
  quote lines and the `moved +31` column would all need a re-fetch and a new hash. Round-55 note, not a round-54 fix.
- L3: the ledger's rendered-page quotes are HTML-normalised text (TAG→space, entity decode); two of the seven cannot
  be matched against the tag's rst without folding the `</code>`-boundary space and U+2019 (§5). Any future
  rst-based verification of these rows must fold, or it will report absent for row 10 and row 12.
- L4: I re-derived the pin comparison only; I did not run `count-c1.py` and make no statement about the claim's
  vote arms, dispositions or the other 24 rows. Reading the page as it renders says nothing about the code around the
  quoted lines.

## Findings

- **F1 (MED)** `corpus/SOURCES.md:299` (row S520) — the used-by cell says "rendered page footer 7.3.0". The marker is
  `<p class="blurb">7.3.0</p>` inside the Sphinx sidebar at document line 42 of the fetched page; the footer holds only
  the copyright, Sphinx 5.3.0, Alabaster 0.7.16 and the relative "Page source" link. The fact is right, the location
  is wrong, and a reader told to look in the footer will not find it. Data (SOURCES prose) correction for the L1.
- **F2 (LOW)** `corpus/knowledge/kernel-v7.3-recheck-r54.md` rows 10 and 12 (hashes `202158f50bb3`, `460b0cafc999`) —
  the ledger quotes carry the rendered page's normalised text (`brk() ,` and U+2019 `Don’t`); the tag's rst
  (`Documentation/admin-guide/cgroup-v2.rst@v7.3`, sha256 `2750c11a…`) reads `brk(),` and `Don't`. Both are correct
  for the HTML copy the counter reads; the rows are not wrong. Recorded so a later rst-based recheck of these rows
  does not misread the divergence as a content change.
- **F3 (LOW)** S520 determinism evidence — both 7.3 fetches were CDN cache hits on the same object (`age: 1129`, no
  ETag). `corpus/evidence/sources-r54/cgroup-v2.7.3.html` reproduced byte-identically (sha256
  `b478c1bae99899df476d6b4989cbb516f7ca93c5f009cdff64b802bbc24f3d4b`, 172967 bytes) and the tag-level source check in
  §4 is what actually ties `/7.3/` to `v7.3`; the two-fetch arm alone is weaker than it looks. Named limit for the
  round-54 report; no change to the counter.
- **F4 (LOW)** `.ufo/waves/round-54/count-c1.py` pin table — the pin has no version string beside the rendered page's
  hash, so a 7.3.y rebuild at the same URL would surface only as `pins=bad` with no in-file hint that the release
  build (not the content) moved. Observation for round 55 only; the pin bytes are frozen and I propose no change.
