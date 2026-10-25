# ScoutROMA — ROMA full text (doi 10.1109/TSC.2026.3698682): openability and the "such as" test

Scope: open the ROMA paper's full text by every route available, and answer one question —
does the sentence naming `mark_victim` / `start_task_reaping` / `finish_task_reaping` say
**"such as"** (non-exhaustive)? Everything below is observed output from this seat.

**Bottom line: the paper WAS opened (full 14-page VOR PDF, CC BY 4.0), and the sentence the
staged row S507 quotes says "such as".** The staged entry's "exactly three named tracepoints"
headline therefore rests on a non-exhaustive illustration, not on an exhaustive claim by the
paper. Details, plus a page-count error found in S507, below.

## 1. The route that worked

`aaron` could not open it (all three tiers fail — §3). The publisher's own deposited VOR
PDF, whose URL is carried in the Crossref record, opened on the second attempt once a browser
User-Agent was supplied.

Crossref record — `curl -sL -o cr.json 'https://api.crossref.org/works/10.1109/TSC.2026.3698682'`
(HTTP 200, 8160 B). Decoded fields:

```text
license: [{'content-version': 'vor', 'delay-in-days': 0,
           'URL': 'https://creativecommons.org/licenses/by/4.0/legalcode',
           'start': {'date-parts': [[2026, 7, 1]]}}]
link:    [{'URL': 'http://xplorestaging.ieee.org/ielx8/4629386/11644734/11540439.pdf?arnumber=11540439',
           'content-type': 'unspecified', 'content-version': 'vor',
           'intended-application': 'similarity-checking'}]
title:   ['ROMA: Enhancing Container OOM Resilience via Reinforced Isolation and Adaptive Shared Resource Reclamation']
page:    3015-3028   vol: 19   issue: 4
```

First fetch, **without** a User-Agent — blocked by IEEE's bot wall (HTTP 418, HTML body
titled `IEEE Xplore - Unable to Load Page`):

```text
$ curl -sL -w 'HTTP=%{http_code} SIZE=%{size_download} CT=%{content_type} ...' \
    -o roma-vor.pdf 'http://xplorestaging.ieee.org/ielx8/4629386/11644734/11540439.pdf?arnumber=11540439'
HTTP=418 SIZE=15410 CT=text/html
$ file roma-vor.pdf
roma-vor.pdf: HTML document, ASCII text, with very long lines (1361)
```

Second fetch, **with** a browser User-Agent — the PDF:

```text
$ curl -sL -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36' \
    -H 'Accept: application/pdf,*/*' \
    -w 'HTTP=%{http_code} SIZE=%{size_download} CT=%{content_type}\n' \
    -o roma-vor2.pdf 'http://xplorestaging.ieee.org/ielx8/4629386/11644734/11540439.pdf?arnumber=11540439'
HTTP=200 SIZE=2357114 CT=application/pdf
$ file roma-vor2.pdf
roma-vor2.pdf: PDF document, version 1.4, 4 page(s)
$ sha256sum roma-vor2.pdf
1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2  roma-vor2.pdf
```

The identical bytes are also served from the non-staging host, so the staging hostname is not
required:

```text
$ curl -sL -A 'Mozilla/5.0 (X11; Linux x86_64) Chrome/128.0' -o roma-ieee.pdf \
    'https://ieeexplore.ieee.org/ielx8/4629386/11644734/11540439.pdf'
$ sha256sum roma-ieee.pdf roma-vor2.pdf
1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2  roma-ieee.pdf
1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2  roma-vor2.pdf
$ cmp roma-ieee.pdf roma-vor2.pdf   # -> IDENTICAL
```

`pdfinfo` on the opened file:

```text
Title:          ROMA: Enhancing Container OOM Resilience via Reinforced Isolation and Adaptive Shared Resource Reclamation
Subject:        IEEE Transactions on Services Computing;2026;19;4;10.1109/TSC.2026.3698682
Creator:        LaTeX with hyperref package
Producer:       Acrobat Distiller 11.0 (Windows); modified using iText® Core 7.2.4
CreationDate:   Wed Jul 22 06:27:59 2026 -03
ModDate:        Thu Aug  6 22:24:42 2026 -03
Pages:          14
Page size:      594 x 792 pts
File size:      2357114 bytes
```

The licence statement is in the PDF's own first-page footer (`roma-vor2.txt` chunk 1 =
printed p. 3015, lines 98–99):

```text
© 2026 The Authors. This work is licensed under a Creative Commons Attribution 4.0 License. For more information, see
https://creativecommons.org/licenses/by/4.0/
```

## 2. The "such as" answer, with the quote

Text extraction: `pdftotext -enc UTF-8 roma-vor2.pdf roma-vor2.txt` → 1405 lines, 14
form-feed chunks (one per physical page). The extracted text is **byte-identical** to the
round-5 copy already in the knowledge tree
(`/home/vgpnk/Projects/shokuknow/lanes/mori/round5/.deepresearch/notes/roma.txt`), so the
prior round's reading reproduces exactly:

```text
$ cmp roma-vor2.txt /home/vgpnk/Projects/shokuknow/lanes/mori/round5/.deepresearch/notes/roma.txt
TEXT IDENTICAL to prior round roma.txt
5ce2d7ace3f3f385f005d620f456f969dfb5f1075325d91dd7a22845814c7f5b  roma-vor2.txt
5ce2d7ace3f3f385f005d620f456f969dfb5f1075325d91dd7a22845814c7f5b  .../round5/.deepresearch/notes/roma.txt
```

### The sentence the staged row quotes — it DOES say "such as"

**Quote (20 words), printed page 3016, §I. INTRODUCTION (the "To fill this gap, we propose
ROMA…" paragraph; physical PDF page 2 of 14; `roma-vor2.txt` lines 139–141):**

> "It leverages eBPF to hook into OOM-related kernel tracepoints **such as** mark_victim,
> start_task_reaping, and finish_task_reaping"

Full sentence with its tail (lines 139–141): `...It leverages eBPF to hook into OOM-related
kernel tracepoints such as mark_victim, start_task_reaping, and finish_task_reaping to record
OOM-triggering process metadata.`

**Answer: YES — the sentence says "such as".** The list is explicitly non-exhaustive: the
paper offers three examples of OOM-related kernel tracepoints an eBPF observer can hook, not
a closed enumeration of the kernel's OOM tracepoints. The paper nowhere states that the
kernel has three OOM tracepoints, and `grep -n 'exactly'` over the whole 14-page text yields
exactly one hit — `Each task belongs to exactly one cgroup` (line 403), about cgroups, not
tracepoints. `grep -n 'three'` yields seven hits, none about the set of OOM tracepoints
(comparison configurations, three metrics, three representative services).

### The second, design-section occurrence — an enumeration of ROMA's own attachments

The same three names appear once more, at printed page 3020, §IV.B "Container Monitoring
Module" → "2) OOM Context Capture and Correlation" (`roma-vor2.txt` lines 440–442):

> "ROMA attaches eBPF programs to the kernel tracepoints oom:mark_victim, oom:start_task_reaping, and oom:finish_task_reaping."

Here the wording is **not** "such as"; it is a closed list — but of *the tracepoints ROMA
attaches*, not of the kernel's OOM tracepoint inventory. Read with the surrounding clause
(lines 440–447: "At oom:mark_victim, ROMA acquires a reference to the victim's task_struct…
At oom:start_task_reaping, the entry is enriched… When oom:finish_task_reaping fires, ROMA
marks the OOM instance as completed…"), it describes ROMA's implementation.

Occurrence map over the whole text (`grep -n -o`):

```text
140:mark_victim          140:start_task_reaping   140:finish_task_reaping    (p. 3016, §I. INTRODUCTION)
441:mark_victim          441:start_task_reaping                                    (p. 3020, §IV.B)
442:finish_task_reaping  442:mark_victim
445:start_task_reaping
447:finish_task_reaping
```

So: `mark_victim` 3×, `start_task_reaping` 3×, `finish_task_reaping` 3×, and no other OOM
tracepoint name appears at all — `wake_reaper`, `skip_task_reaping`, `oom_score_adj_update`,
`reclaim_retry_zone`, `compact_retry` all score 0 occurrences.

### Why this matters for C2 (cross-reference, observed here)

The staged entry
`/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/oom-tracing-tracepoints-r42.md`
headline reads "The OOM lifecycle an observer can hook is three named tracepoints" and its
Claim body reads "**exactly three named tracepoints**". Its own quoted evidence is the p.3016
sentence — which says "such as". Its recheck pin is a string-occurrence count, not a
tracepoint count:

```text
recheck: 180d — `pdftotext -enc UTF-8 roma.pdf - | grep -c 'mark_victim'` -> 3 (ran 2026-10-23)
```

`grep -c` counts *lines* containing the token (3 lines here: 140, 441, 442), so the "3" is a
property of the paper's prose, not of the kernel's tracepoint set. Independently observed in
this seat: the lane's committed v7.2 copy
`corpus/evidence/sources-r47/include_trace_events_oom.h` defines **eight** `TRACE_EVENT`s —
`oom_score_adj_update`, `reclaim_retry_zone`, `mark_victim`, `wake_reaper`,
`start_task_reaping`, `finish_task_reaping`, `skip_task_reaping`, `compact_retry` — of which
the paper names three, and by "such as". The paper's five unnamed OOM tracepoints are
therefore not contradicted by the paper; they are outside what the paper chose to list.

## 3. Every route tried, and its result

| # | Route | Command / URL | Result |
|---|-------|---------------|--------|
| 1 | `aaron papers fetch -m auto` | `aaron papers fetch 10.1109/TSC.2026.3698682 -m auto` | **FAIL** exit 1: `{"error":"All tiers failed for DOI 10.1109/TSC.2026.3698682: [{"tier":"scihub","error":"scihub: no mirror resolved PDF URL"},{"tier":"arxiv","error":"arxiv: DOI not in arxiv"},{"tier":"s2","error":"s2: DOI not in Semantic Scholar"}]"}` |
| 2 | `aaron` s2 tier | `aaron papers fetch 10.1109/TSC.2026.3698682 -m s2` | **FAIL** exit 1: `{"error":"s2: DOI not in Semantic Scholar"}` |
| 3 | `aaron` arxiv tier | `aaron papers fetch 10.1109/TSC.2026.3698682 -m arxiv` | **FAIL** exit 1: `{"error":"arxiv: DOI not in arxiv"}` |
| 4 | `aaron` scihub tier | `aaron papers fetch 10.1109/TSC.2026.3698682 -m scihub` | **FAIL** exit 1: `{"error":"scihub: no mirror resolved PDF URL"}` |
| 5 | `aaron`, lower-case DOI | `aaron papers fetch 10.1109/tsc.2026.3698682 -m auto` | **FAIL** exit 1, same three tier errors |
| 6 | `aaron`, `DOI:` prefix | `aaron papers fetch DOI:10.1109/TSC.2026.3698682 -m s2` | **FAIL** exit 1: `{"error":"s2: DOI not in Semantic Scholar"}` |
| 7 | OpenAlex `best_oa_location` | `curl -sL 'https://api.openalex.org/works/doi:10.1109/TSC.2026.3698682'` | HTTP 200, 67270 B. `open_access.is_oa=true`, `oa_status=hybrid`, `license=cc-by`, `version=publishedVersion` — **but `best_oa_location.pdf_url` is `null`**; `landing_page_url` = the DOI. `locations[]` has 2 entries: publisher (`pdf_url=null`, landing = DOI) and Lancaster eprint (`is_oa=false`, `version=submittedVersion`, `pdf_url=null`). OpenAlex therefore yields **no direct PDF URL** |
| 8 | Semantic Scholar graph API | `curl -sL 'https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/TSC.2026.3698682?fields=title,openAccessPdf,externalIds,isOpenAccess,openAccessPdf'` | HTTP 200: `{"paperId":"2ab2ccce455572de03406c2b8f8aa399da76500a","externalIds":{"DBLP":"journals/tsc/LiWZLMGW26","DOI":"10.1109/TSC.2026.3698682","CorpusId":288883898},"isOpenAccess":true,"openAccessPdf":{"url":"https://doi.org/10.1109/tsc.2026.3698682","status":"HYBRID","license":"CCBY"}}` — the OA "pdf" URL is just the DOI, not a PDF. **Note the disagreement with #2: aaron's s2 tier reports "not in Semantic Scholar" for a DOI S2 itself resolves.** A second S2 call later returned HTTP 429 (rate limit), and a third (`fields=abstract,openAccessPdf,tldr,…`) returned HTTP 429 with no abstract |
| 9 | DOI resolver | `curl -sL 'https://doi.org/10.1109/TSC.2026.3698682'` | HTTP 202, CT text/html, **SIZE=0**, final URL `https://ieeexplore.ieee.org/document/11540439/` — IEEE's bot challenge, not a PDF |
| 10 | IEEE landing page | `curl -sL -A 'Mozilla/5.0 … Chrome/128.0' 'https://ieeexplore.ieee.org/document/11540439/'` | HTTP 202, CT text/html, SIZE=0 — same bot wall |
| 11 | IEEE stamp page | `curl -sL -A 'Mozilla/5.0 … Chrome/128.0' 'https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=11540439'` | HTTP 200 but CT text/html, 8039 B — no `pdfurl` in the body |
| 12 | IEEE ielx8 PDF, no UA | `curl -sL 'http://xplorestaging.ieee.org/ielx8/4629386/11644734/11540439.pdf?arnumber=11540439'` | **FAIL** HTTP 418, 15410 B of HTML (`IEEE Xplore - Unable to Load Page`) |
| 13 | IEEE ielx8 PDF, browser UA | as in §1 | **SUCCESS** HTTP 200, 2357114 B, `application/pdf` |
| 14 | IEEE ielx8 PDF, production host | `curl -sL -A 'Mozilla/5.0 … Chrome/128.0' 'https://ieeexplore.ieee.org/ielx8/4629386/11644734/11540439.pdf'` | **SUCCESS** HTTP 200, `application/pdf`, 2357114 B, byte-identical to #13 |
| 15 | Unpaywall | `curl -sL 'https://api.unpaywall.org/v2/10.1109/TSC.2026.3698682?email=…'` | HTTP 200. `is_oa=true`, `oa_status=hybrid`; one location only: publisher, `publishedVersion`, `license=cc-by`, **`url_for_pdf` = `None`**, `url` = the DOI → no direct PDF URL |
| 16 | CORE | `curl -sL 'https://api.core.ac.uk/v3/search/works?q=doi:%2210.1109/TSC.2026.3698682%22'` | HTTP 200, `{"totalHits":0,…,"results":[]}` — no record |
| 17 | OpenAIRE | `curl -sL 'https://api.openaire.eu/search/publications?doi=10.1109/TSC.2026.3698682'` | HTTP 200, 10116 B of XML — **no `.pdf` URL and no `<webresource>` in the payload** |
| 18 | Lancaster eprint (institutional repository) | `curl -sL -A 'Mozilla/5.0' 'https://eprints.lancs.ac.uk/id/eprint/237917/'` | HTTP 200, 25092 B of HTML — the only document link is `href="https://eprints.lancs.ac.uk/sword-app/servicedocument"` (a SWORD deposit service), **no `.pdf` href** |

**Reading of the route table:** the DOI is openly licensed (CC BY 4.0, `oa_status=hybrid`)
and the publisher's deposited VOR PDF is real and reachable, but **every generic discovery
API returns the DOI landing page rather than a PDF URL** — OpenAlex `pdf_url: null`,
Unpaywall `url_for_pdf: null`, Semantic Scholar `openAccessPdf.url` = the DOI. Only the
Crossref record's `link[]` array carries the publisher's own deposited PDF URL, and that URL
is served only to a client that presents a browser User-Agent. `aaron`'s s2 tier's
"not in Semantic Scholar" is contradicted by the S2 graph API itself (#8), so aaron's failure
here is a lookup-key/behaviour limitation of that tier, not evidence about the paper.

## 4. A defect found in the staged row S507

S507 (`/home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md` line 43, and the
round-5 proposal it came from) describes the deposited artefact as
"the VOR PDF deposited by the publisher (2 357 114 B, **4 pages**)". The byte count is
right; the page count is wrong. The PDF has **14** pages: `pdfinfo` reports `Pages: 14`,
the file contains 14 `/Type /Page` objects, `pdftotext` yields 14 form-feed chunks, and the
printed journal pagination runs 3015–3028 (14 pages) — which is exactly what the same
Crossref record's `page` field says (`3015-3028`). The "4" is what `file(1)` reports
(`PDF document, version 1.4, 4 page(s)`) because the linearized PDF's page tree carries a
nested `/Count 4` node ahead of the root `/Count 14`; `file` reads the first one it finds.
The prior round recorded `file`'s answer. Anyone copying "4 pages" into the new S475 row or
into the C2 knowledge entry would carry the error forward.

## 5. Tools

No tool was installed or upgraded by this seat. `aaron` was already present
(`/home/vgpnk/.local/bin/aaron`, 3245442 B, mtime 2026-10-23 17:22, Node ≥20 via fnm) and
`pdftotext` (`/usr/bin/pdftotext`) was already present. The operator's tooling directive was
read at `/home/vgpnk/.omp/agent/RULES.md`; **no pacman transaction was run** (pacman is paused
host-wide, and nothing here needed it).

## 6. Artefacts this seat produced

Under `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-ScoutROMA/` (scratch only —
no production file was touched; `/home/vgpnk/Projects/shokuknow` was read only):

- `roma-vor2.pdf` — the opened VOR PDF, 2357114 B, sha256 `1603404d…eadd2`
- `roma-vor2.txt` — `pdftotext -enc UTF-8` output, 1405 lines, sha256 `5ce2d7ac…c7f5b`
- `roma-ieee.pdf` — production-host copy, byte-identical
- `roma-vor.pdf` — the HTTP 418 HTML body (kept as the blocked-route evidence)
- `cr.json`, `openalex-roma.json`, `s2-roma.json`, `upw.json`, `core.json`, `oa.json`,
  `lancs.html`, `stamp.html`, `doc.html`, `s507-row.txt` — the raw route responses

## 7. Report for the L1 integrator

1. **The "such as" answer is settled: yes.** The p.3016 §I sentence says "such as"; the
   p.3020 §IV.B sentence is a closed list of ROMA's own attachments, with `oom:` prefixes.
   Any new S475 row or knowledge entry that cites the paper must not restate the paper as
   asserting an exhaustive three-tracepoint set — the paper asserts neither.
2. **S507's "4 pages" is wrong → 14 pages** (printed 3015–3028). It is a `file(1)`
   misreading, not a fact about the artefact.
3. **The paper's full text is reachable** at the Crossref-recorded VOR URL with a browser
   User-Agent; aaron cannot reach it, and no discovery API hands back a PDF URL.
4. The `grep -c 'mark_victim' -> 3` recheck pin in the staged r42 entry counts prose lines;
   it is not a tracepoint count and should not be cited as one.
