# Mo84Sc01Source — round 84 w1 source pin (C1 equivalence adjudication)

Seat: scout, leaf member (no subagent dispatch; none spawned). Lane root
`/home/vgpnk/Projects/shokunin/mori-shokunin`; all access 2026-11-04 (server `date` header on the
pin fetch: `Wed, 04 Nov 2026 09:40:11 GMT`). Detection and report only: no lane, OS, unit,
service, credential, harness or orchestration state was changed. No git/jj mutation was run
anywhere (the only git calls were read-only: `git status --porcelain`, `git log --oneline`,
`git rev-parse`, `git merge-base --is-ancestor`). No tool was installed: only `curl`,
`sha256sum`, `cmp`, `grep`, `awk`, `sed`, `wc`, `file`, `xxd`, `cut`, `tail`, `sort` and
`python3` (stdlib only) were used, all preinstalled — the tooling-authorization clause has no
install to record. Scratch `/fast/scratch/hyaku/mori-r84/Mo84Sc01Source` (deleted before yield).

Lane revision at write time (read-only observation, no judgment): `HEAD = dbdb1aaa4d5b293d678a18b15c50a4a55bc90759`
("round-84: pre-data amendment A1 (fixture finding line numbers; no predicate change)");
`git merge-base --is-ancestor` confirms both the freeze commit
`daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4` and the entering revision
`5adf4337b6510dd246b247092c11cbaa97c930d3` are ancestors of `HEAD`.

**Verdict.** **ADMIT** one source as **S599**: `https://arxiv.org/abs/2408.01760`
(arXiv:2408.01760v1, "Large Language Models for Equivalent Mutant Detection: How Far Are We?",
ISSTA'24). **REFUSE** the second candidate `https://arxiv.org/abs/2404.09241`: it grounds a
syntax-not-semantics *definition* and a weaker "hamper this process" cost claim about
**manually created** mutants in a game study, and never states the rule's *bias* half; flip
condition in §6. `corpus/SOURCES.md` carries **no write of mine**: at entry and through my
measurements it was clean and had no S599 row (`git status --porcelain -- corpus/SOURCES.md`
printed nothing; `grep -c '| S599 |'` → `0`, rc 1), but at my final re-check a **concurrent seat**
had appended an S599 row and a round-84 bounded-search paragraph (file mtime `2026-11-04
06:43:49`, `git status` now `M corpus/SOURCES.md`, `grep -c '| S599 |'` → `1`). That row is not my
write and it was drafted from this report while I was revising; §7 compares it with the row I
propose, and §8c records the precision defects found in that drafting.

| disposition | id | carrier | what it grounds |
|---|---|---|---|
| ADMIT | **S599** | arXiv:2408.01760 abs page — pinned at `corpus/evidence/sources-r84/arXiv-2408.01760-abs.html` | the presence of equivalent mutants introduces redundant cost and bias issues and hinders mutation testing's effectiveness — the rule's known-cost-and-bias half |
| REFUSE (screened, not pinned) | — | `https://arxiv.org/abs/2404.09241` | a definition of equivalence plus a `hamper this process` cost line over human-created mutants; no bias statement, different population, no procedure |

## 1. Files produced

| absolute path | sha256 | bytes | newlines | records |
|---|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r84/arXiv-2408.01760-abs.html` | `688224106999973f3b5c318af871b77923df2c36d0e3e2d799424e2c697cff49` | 42566 | 597 | 598 |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/w1/Mo84Sc01Source.md` | this report | — | — | — |

The pin was written **with curl** directly to the lane path (§2, fetch 2) — never from memory and
never copied from another seat. `corpus/evidence/sources-r84/` did not exist at entry:

```
$ ls -la /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r84/
ls: cannot access '/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r84/': No such file or directory
```

It now holds exactly one file (`ls -la` → `arXiv-2408.01760-abs.html`, 42566 bytes). `git status --porcelain -- corpus/evidence/sources-r84 .ufo/waves/round-84/w1` →
`?? corpus/evidence/sources-r84/` and `?? .ufo/waves/round-84/w1/` (both untracked; the w1
directory is the wave's, not mine alone — it already held `swarm-registry.json`).

Byte geometry (`file`, `grep -c $'\r'`, `awk 'END{print NR}'`, `wc -l`, `tail -c 1 | xxd -p`):
`HTML document, ASCII text, with very long lines (2532)`; CR count `0` (LF-only); `awk NR=598`;
`wc -l` `597` (the last record is **not** newline-terminated — last byte `3e`, i.e. `>`); zero
non-ASCII lines (`grep -c -P '[^\x00-\x7F]'` → `0`, rc 1).

## 2. Fetch receipts

All fetches ran from `/fast/scratch/hyaku/mori-r84/Mo84Sc01Source`. No redirect on any fetch:
`%{url_effective}` equals the requested URL and no `location:` header appears in either response.

**Fetch 1 — identity and headers** (`abs-2408.html`, `headers-2408.txt`):

```
$ curl -sS -D headers-2408.txt -o abs-2408.html \
    -w 'http_code=%{http_code}\nurl_effective=%{url_effective}\ncontent_type=%{content_type}\nsize_download=%{size_download}\n' \
    'https://arxiv.org/abs/2408.01760'
http_code=200
url_effective=https://arxiv.org/abs/2408.01760
content_type=text/html; charset=utf-8
size_download=42566
```

```
$ cat headers-2408.txt
HTTP/2 200
last-modified: Mon, 24 Aug 2026 20:41:50 GMT
content-security-policy: frame-ancestors 'none'
x-frame-options: SAMEORIGIN
server: Google Frontend
cache-control: max-age=3600
via: 1.1 google, 1.1 varnish, 1.1 varnish, 1.1 varnish
x-cloud-trace-context: bd886bb23fc0080cae1b4653bcc7280a
content-type: text/html; charset=utf-8
accept-ranges: bytes
age: 88221
date: Wed, 04 Nov 2026 09:39:47 GMT
x-served-by: cache-lga-kjfk8660022-LGA, cache-lga-kjfk8660022-LGA, cache-lga-kjfk8660059-LGA, cache-gig2250087-GIG
x-cache: MISS, HIT, HIT
x-timer: S1793785188.959736,VS0,VE1
content-length: 42566
```

**Fetch 2 — the pin itself** (`headers-pin.txt`, written straight to the lane path):

```
$ curl -sS -D headers-pin.txt \
    -o /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r84/arXiv-2408.01760-abs.html \
    -w 'http_code=%{http_code}\nurl_effective=%{url_effective}\nsize_download=%{size_download}\ntime_total=%{time_total}\n' \
    'https://arxiv.org/abs/2408.01760'
http_code=200
url_effective=https://arxiv.org/abs/2408.01760
size_download=42566
time_total=0.016492
```

Header subset of the pin response. The full listing differs from fetch 1 in exactly four headers —
`date`, `age`, `x-served-by`, `x-timer` (verified: `diff <(sort headers-2408.txt) <(sort
headers-pin.txt)` reports only those four lines; every semantic header is identical):

```
$ grep -i -E '^(HTTP|last-modified|etag|content-length|location)' headers-pin.txt
HTTP/2 200
last-modified: Mon, 24 Aug 2026 20:41:50 GMT
content-length: 42566
```

`ETag`: **absent** (no `etag:` line in either response; a HEAD confirms — §below). `location`:
absent. Status: **200** on every fetch.

**Fetch 3 — independent second fetch + byte comparison** (`refetch-2408.html`):

```
$ curl -sS -o refetch-2408.html -w 'second_fetch http_code=%{http_code} size=%{size_download}\n' \
    'https://arxiv.org/abs/2408.01760'
second_fetch http_code=200 size=42566
$ sha256sum corpus/evidence/sources-r84/arXiv-2408.01760-abs.html refetch-2408.html abs-2408.html
688224106999973f3b5c318af871b77923df2c36d0e3e2d799424e2c697cff49  corpus/evidence/sources-r84/arXiv-2408.01760-abs.html
688224106999973f3b5c318af871b77923df2c36d0e3e2d799424e2c697cff49  refetch-2408.html
688224106999973f3b5c318af871b77923df2c36d0e3e2d799424e2c697cff49  abs-2408.html
$ wc -c -l corpus/evidence/sources-r84/arXiv-2408.01760-abs.html refetch-2408.html
  597 42566 corpus/evidence/sources-r84/arXiv-2408.01760-abs.html
  597 42566 refetch-2408.html
$ cmp corpus/evidence/sources-r84/arXiv-2408.01760-abs.html refetch-2408.html && echo "cmp: byte-identical (rc=$?)"
cmp: byte-identical (rc=0)
$ cmp corpus/evidence/sources-r84/arXiv-2408.01760-abs.html abs-2408.html && echo "cmp2: byte-identical (rc=$?)"
cmp2: byte-identical (rc=0)
```

Three 200 fetches (two of mine plus the pin write) hash to `68822410…` and `cmp` byte-identical.

A **fourth, independent copy** exists that I did not create: `/fast/scratch/hyaku/mori-r84/emd-abs.html`
(another seat's fetch of the same URL, mtime `06:29`). It matches the pin exactly:

```
$ sha256sum /fast/scratch/hyaku/mori-r84/emd-abs.html
688224106999973f3b5c318af871b77923df2c36d0e3e2d799424e2c697cff49  /fast/scratch/hyaku/mori-r84/emd-abs.html
$ cmp /fast/scratch/hyaku/mori-r84/emd-abs.html /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r84/arXiv-2408.01760-abs.html && echo "cmp: peer copy == pin (byte-identical)"
cmp: peer copy == pin (byte-identical)
```

**Validator revalidation and HEAD** (freshness of the served bytes, not just of my copy):

```
$ curl -sS -o /dev/null -w 'http_code=%{http_code}\n' \
    -H 'If-Modified-Since: Mon, 24 Aug 2026 20:41:50 GMT' 'https://arxiv.org/abs/2408.01760'
http_code=304
$ curl -sSI 'https://arxiv.org/abs/2408.01760' | grep -i -E '^(HTTP|etag|last-modified|content-length|content-type)'
HTTP/2 200
last-modified: Mon, 24 Aug 2026 20:41:50 GMT
content-type: text/html; charset=utf-8
content-length: 42566
```

The `304` establishes that the `last-modified` value I record is the server's current validator
for these bytes; there is no `ETag` to revalidate against.

## 3. Located quote (exact pinned bytes, 24 words)

**The rule-grounding sentence — the abstract's second sentence, raw line 121, 24 words.**

```
$ grep -n 'However, the presence of equivalent mutants is known to introduce redundant cost and bias issues, hindering the effectiveness of mutation testing in practical use\.' \
    /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r84/arXiv-2408.01760-abs.html | cut -c1-60
28:<meta property="og:description" content="Mutation testing
39:  <script src="/static/browse/0.3.4/js/cite.js" type="tex
121:            <span class="descriptor">Abstract:</span>Mut
```

Occurrence count is three (the abstract body at `:121` plus the `og:description` and
`citation_abstract` metadata copies at `:28` and `:39`). The `twitter:description` copy at `:32`
holds only a truncated prefix — it stops at `, hindering the effectiveness of mutation...` (three
literal periods in the bytes) — which is why it does not match this sentence:

```
$ awk '/the presence of equivalent mutants is known to introduce redundant cost and bias issues, hindering the effectiveness of mutation testing/{print NR": match"}' \
    /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r84/arXiv-2408.01760-abs.html
28: match
39: match
121: match
$ sed -n '32p' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r84/arXiv-2408.01760-abs.html | tail -c 400
<meta name="twitter:description" content="Mutation testing is vital for ensuring software quality. However, the presence of equivalent mutants is known to introduce redundant cost and bias issues, hindering the effectiveness of mutation..."/>
```

The located quote, verbatim:

> "However, the presence of equivalent mutants is known to introduce redundant cost and bias issues, hindering the effectiveness of mutation testing in practical use."

Mechanical checks:

```
$ grep -o 'However, the presence of equivalent mutants is known to introduce redundant cost and bias issues, hindering the effectiveness of mutation testing in practical use\.' \
    /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r84/arXiv-2408.01760-abs.html | sort -u
However, the presence of equivalent mutants is known to introduce redundant cost and bias issues, hindering the effectiveness of mutation testing in practical use.
$ printf '%s' 'However, the presence of equivalent mutants is known to introduce redundant cost and bias issues, hindering the effectiveness of mutation testing in practical use.' | wc -w
24
```

24 words ≤ the 25-word cap; the sentence is complete in the pinned bytes (no ellipsis, no cut, no
paraphrase). Shortest core span, if a narrower anchor is wanted, is
`the presence of equivalent mutants is known to introduce redundant cost and bias issues`
(14 words; `grep -c` → `4`, i.e. lines `:28`, `:32`, `:39`, `:121`).

**What the sentence grounds, and what it does not.** It grounds the *premise* of C1's
adjudication — equivalent mutants are a **known** cost and a **bias** in mutation testing, so an
unkillable mutant is an expected artefact of the technique rather than an anomaly. It does **not**
state the rule's second clause, "not evidence of a missing test": that is the lane's adjudication
consequence (if semantics are identical, no test can distinguish the mutant), and the abstract
never uses kill/survivor vocabulary at all (§5). The lane must keep its own sentence separate from
this quote — the source supplies cost+bias and effectiveness harm, nothing about counters,
selftests, exit statuses or how to adjudicate.

## 4. Identity and supporting locations

Identity (all from the pinned bytes):

```
$ P=/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r84/arXiv-2408.01760-abs.html
$ grep -o 'citation_title" content="[^"]*"' "$P"
citation_title" content="Large Language Models for Equivalent Mutant Detection: How Far Are We?"
$ grep -o 'citation_date" content="[^"]*"' "$P"
citation_date" content="2024/08/03"
$ grep -o 'citation_online_date" content="[^"]*"' "$P"
citation_online_date" content="2024/08/03"
$ grep -o 'citation_author" content="[^"]*"' "$P"
citation_author" content="Tian, Zhao"
citation_author" content="Shu, Honglin"
citation_author" content="Wang, Dong"
citation_author" content="Cao, Xuejie"
citation_author" content="Kamei, Yasutaka"
citation_author" content="Chen, Junjie"
$ grep -o '\[v[0-9]\]' "$P" | sort | uniq -c
      1 [v1]
$ sed -n '160,172p' "$P" | sed -e 's/<[^>]*>//g' | sed '/^ *$/d'
      Submission history From: Zhao Tian [view email]          [v1]
        Sat, 3 Aug 2024 11:58:16 UTC (2,614 KB)
      Full-text links:
      Access Paper:
View a PDF of the paper titled Large Language Models for Equivalent Mutant Detection: How Far Are We?, by Zhao Tian and 5 other authorsView PDFHTML (experimental)TeX Source
$ sed -n '126,140p' "$P" | cut -c1-220
      <table summary="Additional metadata">        <tr>
          <td class="tablecell label">Comments:</td>
          <td class="tablecell comments mathjax">This paper has been accepted by ISSTA&#39;2024</td>
        </tr>
<tr>
          <td class="tablecell label">Subjects:</td>
          <td class="tablecell subjects">
            <span class="primary-subject">Software Engineering (cs.SE)</span></td>
        </tr><tr>
          <td class="tablecell label">Cite as:</td>
          <td class="tablecell arxivid"><span class="arxivid"><a href="https://arxiv.org/abs/2408.01760">arXiv:2408.01760</a> [cs.SE]</span></td>
        </tr>
        <tr>
          <td class="tablecell label">&nbsp;</td>
          <td class="tablecell arxividv">(or <span class="arxivid">
```

One version only: `[v1]` at `:161` (`grep -n '\[v1\]' "$P"` → `161:      <h2>Submission history</h2> From: Zhao Tian [<a href="/show-email/43e9…`; the
`:160-172` rendering above shows the same block). Authors per `citation_author`:
Zhao Tian, Honglin Shu, Dong Wang, Xuejie Cao, Yasutaka Kamei, Junjie Chen. `Comments:` row at
`:127-128` = "This paper has been accepted by ISSTA'2024"; `Subjects:` row `:131-133` = "Software
Engineering (cs.SE)"; `Cite as:` row `:135` = `arXiv:2408.01760` (inside an `<a>` element's link
text) followed by `[cs.SE]` — which is why a plain-text grep for the joined string
`arXiv:2408.01760 [cs.SE]` finds nothing in the raw bytes:

```
$ grep -c 'arXiv:2408.01760 \[cs\.SE\]' "$P"
0
```

**Scope bound — the Java/method-level study, raw line 121, 11 words:**

```
$ grep -n 'we conduct an empirical study on 3,302 method-level Java mutant pairs' "$P" | cut -c1-60
28:<meta property="og:description" content="Mutation testing
39:  <script src="/static/browse/0.3.4/js/cite.js" type="tex
121:            <span class="descriptor">Abstract:</span>Mut
$ grep -o 'we conduct an empirical study on 3,302 method-level Java mutant pairs' "$P" | sort -u | wc -w
11
```

This is the sentence that fixes the empirical study's population: 3,302 **method-level Java**
mutant pairs. The paper's own results are LLM detection performance — its abstract's
`average improvement of 35.69% in terms of F1-score` (8 words, `:28`, `:39`, `:121`) for
LLM-based techniques over existing EMD techniques — i.e. a *detection-method* study, not a
statement about any lane.

## 5. What the page does NOT say (measured, re-runnable)

Counts are `grep -c -i` against the pinned file (`P` is the path set in §4); grep exits 1 on a
zero count, recorded here rather than hidden:

| term | count | consequence |
|---|---|---|
| `exit status`, `exit code` | 0 each | no exit-status semantics; C1's rc/fail-token kill rule is the lane's own |
| `surviv` | 0 | the page never says "survivor"/"surviving mutant"; that vocabulary is PIT's (S598), not this paper's |
| `kill` | 1 | the single hit is `madskills.com` in the RSS namespace at `:91` — **no mutation-kill usage anywhere** |
| `counter` | 0 | nothing about counters, tallies or counting instruments |
| `adjudicat` | 0 | no adjudication procedure, no equivalence *proof* method |
| `selftest` | 0 | nothing about a tool testing its own detector |
| `python` | 0 | no implementation of the study in this language; no claim about any Python tool |
| `mori`, `shokunin` | 0 each | nothing about this lane |
| `threshold`, `mutation score` | 0 each | no numeric bar and no named score |
| `differ only in syntax` | 0 | **the page never defines equivalence** — the definition is absent here (see §6) |
| `equivalent mutant` | 14 | the topic is present; only the cost/bias sentence and the detection-performance framing are claimed |

The single `kill` hit, shown in full so the "1" is not taken on trust:

```
$ grep -n -i 'kill' "$P"
91:         xmlns:trackback="http://madskills.com/public/xml/rss/module/trackback/">
```

Positive hits that bound the reading: `bias` 4 and `cost` 4 — all four occurrences are the same
abstract sentence (metadata copies at `:28`, `:32`, `:39` and body `:121`); there is no second,
independent cost/bias statement on the page.

Also absent: any claim that an equivalent mutant should be *excluded* from a kill tally (the page
argues for detecting them, not for how a count is reported), any statement about a lane's counters
or about non-Java code beyond the Java framing at `:121`, and any procedure for proving two
programs semantically identical. The admitted text is a **preprint abstract**; the ISSTA'24
proceedings version was not opened.

## 6. Second candidate — screened and refused

**Fetched** (`abs-2404.html`, `headers-2404.txt`, scratch only; **not pinned**):

```
$ curl -sS -D headers-2404.txt -o abs-2404.html \
    -w 'http_code=%{http_code}\nurl_effective=%{url_effective}\nsize_download=%{size_download}\n' \
    'https://arxiv.org/abs/2404.09241'
http_code=200
url_effective=https://arxiv.org/abs/2404.09241
size_download=40386
$ grep -i -E '^(last-modified|etag|content-length)' headers-2404.txt
last-modified: Mon, 24 Aug 2026 20:46:14 GMT
content-length: 40386
$ sha256sum abs-2404.html
4bcb20b23ad5046657a65a29595517da973128a289ff75ba13ad8926c5511a80  abs-2404.html
$ wc -c -l abs-2404.html        → 596 40386      (awk NR=597; last byte 3e; CR count 0)
$ grep -n -o '<title>[^<]*' abs-2404.html
4:<title>[2404.09241] An Empirical Evaluation of Manually Created Equivalent Mutants
$ grep -o 'citation_date" content="[^"]*"' abs-2404.html
citation_date" content="2024/04/14"
```

No redirect, no `ETag`, HTTP 200. Authors per metadata: Philipp Straubinger, Alexander Degenhart,
Gordon Fraser.

**What it states** (verbatim spans located in the screening copy, which is not persisted — a flip
would require a fresh pin):

| span | lines | words |
|---|---|---|
| `mutants that differ only in syntax but not semantics` | `:28`, `:39`, `:121` | 9 |
| `equivalent mutants, i.e., mutants that differ only in syntax but not semantics, hamper this process` | `:28`, `:39`, `:121` | 15 |
| `less than 10 % of manually created mutants are equivalent` | `:28`, `:39`, `:121` | 10 |
| `a significant portion of developers struggle to accurately identify equivalent mutants` | `:28`, `:39`, `:121` | 11 |

Each row's line list is `grep -n -o '<span>' abs-2404.html | cut -c1-30` on the screening copy;
the `twitter:description` copy at `:32` is truncated before all four spans, as on the pin.

Absence checks on the screening copy: `bias` **0**, `redundant` **0**, `exit status` **0**,
`counter` **0**, `adjudicat` **0**.

**Refusal reason (three parts, all measured).**

1. It never says the rule's word: `bias` and `redundant` are both **0** in its bytes; its only cost
   statement is the generic `hamper this process`. The first candidate states "known to introduce
   redundant cost and bias issues" — the rule's own phrase — and is therefore the tighter ground.
2. Its population is **manually created** mutants produced by human players of Code Defenders, and
   its claims are about human production and human identification accuracy. The lane's M24c/M24d
   are tool-generated mutants of its own Python counter; the source's unit of analysis does not
   reach them.
3. It supplies no adjudication procedure either (`adjudicat` 0), so admitting it would not reduce
   any open C1 unknown beyond what S599 already covers.

**Does it ground the rule better? No.** It does, however, state something S599 lacks: a
definition of equivalence ("differ only in syntax but not semantics", 9 words), which the pin
nowhere defines (`differ only in syntax` → 0 in the pin). That is recorded as a **limit of S599**,
not as grounds for admission here: the C1 rule is about *cost and bias*, not about the definition,
and the contract's coupling proofs are the lane's own construction.

**Flip condition.** Admit a **freshly pinned** copy of `https://arxiv.org/abs/2404.09241` (new
hash, new row, never back-filled into S599) only if the graded question changes from "is an
unkillable mutant a known cost and bias of the technique" to "is a human adjudicator's equivalence
verdict itself reliable" — i.e. if a round asks whether manual inspection can stand in for a
coupling proof. In that case the locating span would be
`a significant portion of developers struggle to accurately identify equivalent mutants`
(`:121`, 11 words) on the then-current bytes. Should the lane instead need a *definition* anchor,
neither row is the right carrier by itself and a new candidate must be screened.

## 7. Registry row — what landed (not my write) and what I would have proposed

`corpus/SOURCES.md` now carries an S599 row and a round-84 bounded-search paragraph written by a
**concurrent seat** at `06:43:49` (I hold no write there; the file was clean when I started —
§Verdict). For the record, my proposed row was:

```
| S599 | Large Language Models for Equivalent Mutant Detection: How Far Are We? — arXiv:2408.01760v1 — https://arxiv.org/abs/2408.01760 | paper | A | equivalent mutants as a known cost and bias in mutation testing, limited to what this abstract states (Java method-level mutants, 3,302 pairs; no adjudication procedure) | abstract body line 121 (`grep -n 'However, the presence of equivalent mutants is known' corpus/evidence/sources-r84/arXiv-2408.01760-abs.html`; metadata copies at :28 and :39, :32 truncates); 24-word sentence at :121; sha256 688224106999973f3b5c318af871b77923df2c36d0e3e2d799424e2c697cff49; copy corpus/evidence/sources-r84/arXiv-2408.01760-abs.html; 42566 bytes, 597 newlines (598 records, no trailing newline); last-modified 2026-08-24T20:41:50Z, no ETag | The presence of equivalent mutants introduces redundant cost and bias issues and hinders mutation testing's effectiveness, so an unkillable mutant is a known cost of the technique rather than evidence of a missing test. | queued | 2026-11-04 | 365d | — |
```

The landed row matches on id, carrier, hash, byte count, pin path, sentence location and
`recheck 365d`; it adds `status mined` and `used-by corpus/knowledge/equivalent-mutant-adjudication-r84.md`
(that file exists, 4288 bytes, mtime `06:43`). Two precision defects — one in the landed row, one
in the knowledge entry — and one observation are recorded in §8c; all are the D83-3 class
(locator/numeric precision), and both defects concern the same `:32` line.

## 8. Freshness and what remains unverified

Freshness: server `last-modified` `2026-08-24T20:41:50Z`, access `2026-11-04T09:40:11Z` →
`6181101` seconds = **71 days** at access (`python3 -c` arithmetic, command and output above).
The `If-Modified-Since` revalidation returns `304`, so the served representation has not changed
since that date. The page is a single-version preprint abstract (`[v1]`, 2024-08-03); `recheck
365d` is proposed for the row, consistent with the lane's paper-row convention.

Not verified, stated plainly: the PDF/HTML full text was not opened (this row claims abstract-level
ground only); the ISSTA'24 proceedings version was not compared to the preprint; the paper's
reported numbers (35.69% F1 improvement) are the preprint abstract's and were not reproduced; the
second candidate's full text was not opened, so its refusal rests on its abstract bytes alone.

## 8c. Defects found in another seat's bytes

Three, all of the D83-3 locator-precision class, all reproducible from the commands in §3/§5. They
are reported, not fixed: `corpus/SOURCES.md` and `corpus/knowledge/` are not my write scope.

1. **`corpus/SOURCES.md:380` (S599 row), anchor column** — "the 24-word sentence, also copied at
   metadata lines 28/32/39". The `:32` copy is a **truncated prefix**: it ends
   `…hindering the effectiveness of mutation...` and does not contain the sentence. Measured:

   ```
   $ awk '/the presence of equivalent mutants is known to introduce redundant cost and bias issues, hindering the effectiveness of mutation testing/{print NR": match"}' \
       /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r84/arXiv-2408.01760-abs.html
   28: match
   39: match
   121: match
   $ sed -n '32p' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r84/arXiv-2408.01760-abs.html | tail -c 120
    equivalent mutants is known to introduce redundant cost and bias issues, hindering the effectiveness of mutation..."/>
   ```

   Correction: `:28`, `:39`, `:121` carry the sentence; `:32` carries a prefix. The row also
   contradicts itself — a 24-word sentence cannot be "copied" at a line that stops after 15 of
   its words.

2. **`corpus/knowledge/equivalent-mutant-adjudication-r84.md` K1, first paragraph** — "The
   abstract's second sentence (pinned body line 121, 14 words) reads: 'the presence of equivalent
   mutants is known to introduce redundant cost and bias issues'." The second sentence is **24
   words** (§3, `printf … | wc -w` → `24`); the quoted 14 words are its prefix, and the sentence
   continues `, hindering the effectiveness of mutation testing in practical use.` A 14-word quote
   presented as the sentence is a truncation without an ellipsis. Same file: "The same sentence is
   repeated in page metadata at lines 28, 32 and 39" carries defect 1's `:32` error.

3. **Observation, not a defect — `corpus/knowledge/equivalent-mutant-adjudication-r84.md` K4**
   restates the r83 sweep's `M24a` as `killed_n = total - survivors` → `killed_n = total` (which is
   verbatim `.ufo/waves/round-83/w1/Mo83R01C1.md` §6), while the r84 contract's table anchors
   `killed_n = total - survivors - equivalent` → `killed_n = total - equivalent`. The contract is
   the one that matches the frozen bytes:

   ```
   $ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4:.ufo/waves/round-83/count-c1.py | grep -n 'killed_n = total'
   191:    killed_n = total - survivors - equivalent
   $ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4:.ufo/waves/round-83/count-c1.py | grep -c 'killed_n = total - survivors - equivalent'
   1
   ```

   The K4 sentence remains a faithful citation of §6 (which measured `c4845c83`, a different
   revision); it just is not the anchor the frozen r84 table uses, so a reader who takes it as the
   graded anchor will grep a string that no longer exists at the freeze. No action is mine to take.

No other defect: `.ufo/waves/round-83/w1/Mo83Sc01Source.md` and
`corpus/lessons/round-83-verifier-spotcheck.md` were read only for format and anti-pattern, and no
claim in them is contradicted by my measurements; I found no defect in the round-84 counters,
contract or evidence files I read.
