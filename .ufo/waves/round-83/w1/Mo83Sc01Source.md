# Mo83Sc01Source — round 83 w1 source pin (C1 mutation-adequacy rule)

Seat: scout, leaf member (no subagent dispatch, no subagents spawned). Lane root
`/home/vgpnk/Projects/shokunin/mori-shokunin`; all access 2026-11-04 (server date header
`Wed, 04 Nov 2026 08:21:53 GMT` on the first fetch). Detection and report only: no lane, OS,
unit, service, credential or orchestration state was changed. No git/jj mutation was run
anywhere (read-only `git status`, `git log`, `git show`, `git diff` only). No tool was installed
(only `curl`, `sha256sum`, `grep`, `awk`, `sed`, `wc`, `cmp`, `stat`, `python3` 3.x were used —
none needed installing, so the tooling-authorization clause has no entry to record).

**Verdict.** One row proposed for admission (**S598**), independently re-pinned and re-quoted;
one candidate rejected (`PIT — Mutation operators`, the mutators page). The pinned bytes are
byte-identical to the file the L1 had already fetched and to two fresh fetches of my own; the
located quote reproduces at `:114` with 14 words. One **precision defect** was found in another
seat's bytes: the "51 words" block is cited as raw lines `108-113` in two places, but it is raw
lines `106-114` (measured: 51 rendered words there, 31 at `108-113`) — see §9.

| disposition | id | carrier | what it grounds |
|---|---|---|---|
| ADMIT | **S598** | PIT (pitest.org) "What is mutation testing?" — `corpus/evidence/sources-r83/pitest-home.html` | the killed/lived mechanism and the metric: failing tests kill the mutation, passing tests let it live, and the killed percentage gauges test quality |
| REJECT | — (no id) | `https://pitest.org/quickstart/mutators/` ("Mutation operators") | it catalogues default mutators; it states no adequacy rule and never mentions killed/lived |
| NOT ADMITTED (adjacent, already held) | S595 | arXiv:2102.11378v2 abstract | mutation analysis's definition as an adequacy criterion from that abstract — a different document on the same concept; S598 supplies the gauge sentence S595's scope does not claim |

## 1. Files produced

| absolute path | sha256 | bytes | lines |
|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r83/pitest-home.html` | `b0c7e0505c51c95b596060ef27babbce08e72d5aaf4557eb002c2637d2bf10cc` | 12023 | 284 |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-83/w1/Mo83Sc01Source.md` | this report | — | — |

The pin was written **with curl**, not from memory or from another seat's copy:
`curl -sS -L --max-time 60 -o corpus/evidence/sources-r83/pitest-home.html https://pitest.org/`
(§2, fetch 3). `corpus/evidence/sources-r83/` already existed at entry (it held the L1's single
fetch, `12023` bytes, same sha256); my write replaced it with the same bytes, verified by `cmp`
against my own fetch 1. No other lane path was created or modified. `corpus/SOURCES.md` was **not
edited by this seat** (it carries an uncommitted S598 row drafted by another seat — §8/§9).

## 2. Fetch receipts

All fetches were run from `/fast/scratch/hyaku/mori-r83/Mo83Sc01Source` (my scratch; deleted
before yield). No redirect on any fetch: `%{url_effective}` equals the requested URL and
`num_redirects=0`.

**Fetch 1 — identity and headers** (`fetch1.html`, `headers1.txt`):

```
$ curl -sS -L --max-time 60 -o fetch1.html -D headers1.txt \
    -w 'final_url=%{url_effective}\nhttp_code=%{http_code}\ncontent_type=%{content_type}\nsize_download=%{size_download}\nnum_redirects=%{num_redirects}\ntime_total=%{time_total}\n' \
    https://pitest.org/
final_url=https://pitest.org/
http_code=200
content_type=text/html; charset=utf-8
size_download=12023
num_redirects=0
time_total=0.013788
```

```
$ cat headers1.txt
HTTP/2 200
server: GitHub.com
content-type: text/html; charset=utf-8
x-origin-cache: HIT
last-modified: Wed, 03 Jun 2026 08:45:38 GMT
access-control-allow-origin: *
etag: "6a1fe9b2-2ef7"
expires: Wed, 04 Nov 2026 08:24:49 GMT
cache-control: max-age=600
x-proxy-cache: MISS
x-github-request-id: 9F56:29C9AB:1B0AD8:1DA6B9:6AEAE978
x-github-edge-region: sea
accept-ranges: bytes
date: Wed, 04 Nov 2026 08:21:53 GMT
via: 1.1 varnish
age: 424
x-served-by: cache-gig2250056-GIG
x-cache: HIT
x-cache-hits: 1
x-timer: S1793780513.478342,VS0,VE1
vary: Accept-Encoding
x-fastly-request-id: 707bb8398748ea7b2f5c525b99b7a87f7876175a
content-length: 12023
```

**Fetch 2 — independent second fetch** (`fetch2.html`):

```
$ curl -sS -L --max-time 60 -o fetch2.html -w 'http_code=%{http_code} size=%{size_download}\n' https://pitest.org/
http_code=200 size=12023
$ sha256sum fetch2.html
b0c7e0505c51c95b596060ef27babbce08e72d5aaf4557eb002c2637d2bf10cc  fetch2.html
$ cmp fetch1.html fetch2.html
CMP: fetch1 == fetch2
```

**Fetch 3 — the pin itself**, then compared to fetch 1:

```
$ curl -sS -L --max-time 60 -D headers-pin.txt -o corpus/evidence/sources-r83/pitest-home.html \
    -w 'final_url=%{url_effective}\nhttp_code=%{http_code}\nsize=%{size_download}\n' https://pitest.org/
final_url=https://pitest.org/
http_code=200
size=12023

$ sha256sum corpus/evidence/sources-r83/pitest-home.html
b0c7e0505c51c95b596060ef27babbce08e72d5aaf4557eb002c2637d2bf10cc  corpus/evidence/sources-r83/pitest-home.html
$ wc -c < corpus/evidence/sources-r83/pitest-home.html
12023
$ wc -l < corpus/evidence/sources-r83/pitest-home.html
284
$ cmp /fast/scratch/hyaku/mori-r83/Mo83Sc01Source/fetch1.html corpus/evidence/sources-r83/pitest-home.html
CMP: pin == independent fresh fetch1
$ grep -i -E '^(last-modified|etag|content-length|date):' headers-pin.txt
last-modified: Wed, 03 Jun 2026 08:45:38 GMT
etag: "6a1fe9b2-2ef7"
date: Wed, 04 Nov 2026 08:23:27 GMT
content-length: 12023
$ stat -c '%n %s bytes mtime=%y' corpus/evidence/sources-r83/pitest-home.html
corpus/evidence/sources-r83/pitest-home.html 12023 bytes mtime=2026-11-04 05:23:27.695145069 -0300
```

Three independent 200 fetches (L1's original, my fetch 1, my fetch 2) plus the pin write all hash
to `b0c7e050…`; `cmp` is byte-identical each time.

**Strong validator revalidation** — the pinned ETag is live, not stale:

```
$ curl -sS -o /dev/null -w 'http_code=%{http_code}\n' -H 'If-None-Match: "6a1fe9b2-2ef7"' https://pitest.org/
http_code=304
```

The ETag's size suffix is a self-check: `0x2ef7` = `12023` decimal, equal to `content-length` and
to the pinned byte count.

Byte characteristics of the pin: `file` → `HTML document, Unicode text, UTF-8 text`; CR count `0`
(`grep -c $'\r'` → 0, i.e. LF-only); exactly 3 non-ASCII lines (`:227`, `:229`, `:231`, each a
`≈` in the coverage graphic markup); final byte `0a` (newline-terminated); 284 newline-terminated
lines.

Freshness: server `last-modified` `2026-06-03T08:45:38Z`, access `2026-11-04T08:21:53Z` →
**`13304175` seconds = 153 days 23 h** at access. The page carries no visible publication date,
author, version or copyright line (`grep -n -i -E 'generator|last.updated|&#169;|&copy;|<footer'`
matches only `<footer class="footer">` at `:221`), so the only date evidence is the server
header; `recheck 365d` as drafted is consistent with it.

## 3. Located quote (exact pinned bytes)

**Primary quote — the adequacy gauge, raw line 114, 14 words.**

```
$ grep -n 'The quality of your tests can be gauged from the percentage of mutations killed\.' \
    corpus/evidence/sources-r83/pitest-home.html
114:        <p class="marketing-info">The quality of your tests can be gauged from the percentage of mutations killed.</p>
$ grep -c 'The quality of your tests can be gauged from the percentage of mutations killed\.' \
    corpus/evidence/sources-r83/pitest-home.html
1
```

> "The quality of your tests can be gauged from the percentage of mutations killed."

Word count verified mechanically:
`printf '%s' 'The quality of your tests can be gauged from the percentage of mutations killed.' | wc -w`
→ `14`. Occurrence count in the pinned file: exactly 1 (the anchor is unique).

This is the sentence that grounds the second half of C1's rule — the killed percentage gauges
test adequacy. It is a complete sentence in the pinned bytes: no cut, no ellipsis, no paraphrase.

## 4. Supporting locations (each re-derivable)

**Kill/live mechanism, raw 110-112** — the sentence that makes a passing suite the definition of a
live mutant:

```
$ grep -n 'the mutation <strong>lived</strong>' corpus/evidence/sources-r83/pitest-home.html
112:          the mutation <strong>lived</strong>. </p>
```

Rendered text of raw 106-114 (tags stripped) is, verbatim:

> "Mutation testing is conceptually quite simple. Faults (or mutations) are automatically seeded
> into your code, then your tests are run. If your tests fail then the mutation is killed, if your
> tests pass then the mutation lived. The quality of your tests can be gauged from the percentage
> of mutations killed."

The rendered span is 31 words for the seeded/killed/lived sentence (raw 110-112) — over the
25-word cap, so it is quoted here only as supporting context, never as the located quote. Its
raw bytes carry the `<strong>` markup, which is why the raw span is not cited as a plain quote.

**The hedged predecessor of "the suite does not constrain the behaviour", raw 119-122:**

```
$ grep -n 'If a unit test does not fail in this situation' corpus/evidence/sources-r83/pitest-home.html
121:          cause the unit tests to fail. If a unit test does not fail in this situation, it may indicate an issue with
```

Note the hedge: "it **may** indicate an issue with the test suite". The page's own strongest
statement of the survivor→suite reading is weaker than the lane's rule sentence ("reveals a
behaviour the test suite does not constrain"); the lane's stronger phrasing is the lane's
reading, and the pin should not be cited as if PIT wrote it.

**Scope bound — Java/PIT, line 71 and line 144:**

```
71:        standard test coverage</strong> for Java and the jvm. It's fast, scalable and integrates with modern test and
144:        <p class="marketing-info">There are other mutation testing systems for Java, but they are not widely used.
```

**Comparison frame the page does state, line 138** (supporting context, not the adequacy rule):
"mutation testing is the **gold standard** against which all other types of coverage are measured."

## 5. The page's own "51 words" and the exact block extent

The page labels the block itself at raw `:102`: `<p class="marketing-byline" …>How it works in 51
words</p>`. The block's three `<p class="marketing-info">` paragraphs are at raw `:106-107`,
`:110-112` and `:114`. Stripping tags and counting whitespace tokens:

```
$ sed -n '106,114p' fetch1.html | sed -e 's/<[^>]*>//g' | tr -s '[:space:]' ' ' | wc -w
51
$ sed -n '108,113p' fetch1.html | sed -e 's/<[^>]*>//g' | tr -s '[:space:]' ' ' | wc -w
31
$ sed -n '106,112p' fetch1.html | sed -e 's/<[^>]*>//g' | tr -s '[:space:]' ' ' | wc -w
37
```

The page's own count (51) reconciles **exactly** with raw `106-114` and with nothing else. The
block therefore spans raw `106-114` (body text at `107`, `110-112`, `114`; `106` is the opening
tag of the first paragraph, `108-109` are an empty `<p>` and a blank line, `113` is a blank line).
The adequacy sentence at `:114` is **inside** the 51-word block.

## 6. What the page does NOT say (measured, re-runnable)

Counts are `grep -c -i` against the pinned file unless noted; `rc=1` on a zero count is grep's
"no match", recorded here rather than hidden:

| term | count | consequence |
|---|---|---|
| `exit` | 0 | no exit-status semantics; C1's "non-zero exit **or** `fail=<n>`" kill rule is the lane's own |
| `self-test`, `selftest` | 0 each | nothing about a tool testing its own detector; the `--selftest` arm is the lane's decision |
| `threshold` | 0 | no numeric adequacy bar (no "90 % is good"), only "gauged from the percentage" |
| `score` | 0 | the page never uses "mutation score" |
| `surviv` (case-insensitive) | 0 | the page's term is **lived**; "surviving mutant" is the lane's paraphrase, not PIT's word here |
| `mori`, `shokunin` | 0 each | nothing about this lane |
| `CI `, `continuous integration` | 0 each | no claim about gating a pipeline on the percentage |

Also absent: any statement that *all* survivors are bugs (the page says a live mutant means the
tests passed, not that the code is wrong), any operator catalogue (that is the rejected page), any
date/version/author (§2), and any claim about non-Java languages beyond the Java/PIT framing at
`:71` and `:144`. The quoted sentences sit in `<p class="marketing-info">` paragraphs of the
vendor's product page — the admitted text is the vendor's own definition of its own technique,
not a standard or a peer-reviewed result; the lane's stronger rule wording and its operational
consequences are the lane's, which the knowledge entry must keep separate.

## 7. Reject candidate — PIT "Mutation operators" (`/quickstart/mutators/`)

Screened, not persisted (no second copy is pinned; the flip condition below would require a new
pin if it ever qualifies).

```
$ curl -sS -L --max-time 60 -o mutators.html -D headers-mutators.txt \
    -w 'final_url=%{url_effective}\nhttp_code=%{http_code}\nsize=%{size_download}\n' https://pitest.org/quickstart/mutators/
final_url=https://pitest.org/quickstart/mutators/
http_code=200
size=67033
$ wc -l < mutators.html
1459
$ sha256sum mutators.html
a31331daf89f246f3e02c0da92578d4ad2163c53741c3700437e75b9a1602da2  mutators.html
$ grep -n -o '<title>[^<]*' mutators.html
5:<title>Mutation operators
$ grep -i -E '^(last-modified|etag):' headers-mutators.txt
last-modified: Wed, 03 Jun 2026 08:45:37 GMT
etag: "6a1fe9b1-105d9"
```

Absence evidence (each command re-runnable; zero counts print `0` and make grep exit 1):

```
$ printf 'killed=';   grep -c -i 'killed'   mutators.html     → killed=0
$ printf 'lived=';    grep -c -i 'lived'    mutators.html     → lived=0
$ printf 'adequacy='; grep -c -i 'adequacy' mutators.html     → adequacy=0
$ printf 'gauged=';   grep -c -i 'gauged'   mutators.html     → gauged=0
$ grep -n -i -E 'gauged|quality of your tests|percentage of mutations killed|test adequacy|surviv' mutators.html; echo "grep_rc=$?"
grep_rc=1
```

What it *is*: an operator catalogue — `<h1 id="available-mutators-and-groups">` at `:86`,
`<h1 id="default-mutators">Default Mutators</h1>` at `:310`, then one `<h2>` per operator
(`:313` `Conditionals Boundary Mutator (CONDITIONALS_BOUNDARY)`, `:364` `Increments Mutator`,
`:394` `Invert Negatives Mutator`, `:417` `Math Mutator`, …), 38 occurrences of `Mutator`.

**Refusal reason.** It defines operator semantics, never the significance of a survivor or the
adequacy metric; admitting it would ground "how PIT mutates", not C1's rule "a survivor reveals
an unconstrained behaviour, and the killed share gauges adequacy". The page also carries no
killed/lived definition at all, so even as corroboration it would add nothing to S598.

**Flip condition.** Admit a pinned copy of this page only if (a) a revision of it states what a
surviving mutant means for suite adequacy (or the killed-percentage gauge), or (b) at S598's
recheck the home page has lost/rewritten the `:106-114` block while this page carries the
definition — in either case the new bytes must be pinned and re-quoted (new row, new hash), never
back-filled into S598's anchor.

## 8. Duplicate sweep, adjacency, id state

```
$ grep -n 'pitest' corpus/SOURCES.md | cut -c1-140
379:| S598 | PIT mutation testing — “What is mutation testing?” — https://pitest.org/ | docs | A | mutation adequacy: a surviving mu
457:Round 83 bounded search — Question: what source grounds the rule that a surviving mutant is a coverage finding about the suite rather
$ grep -c 'https://pitest.org' corpus/SOURCES.md
1                    # the S598 row itself; no earlier row on this base URL
$ grep -c '^| S598 ' corpus/SOURCES.md
1
$ grep -n -i 'mutation' corpus/SOURCES.md | cut -c1-150 | tail -3
376:| S595 | Practical Mutation Testing at Scale — arXiv:2102.11378v2 — https://arxiv.org/abs/2102.11378v2 | paper | A | mutation analysis's own d…
379:| S598 | PIT mutation testing — “What is mutation testing?” — https://pitest.org/ | docs | A | mutation adequacy: a surviving mutant shows…
457:Round 83 bounded search — Question: what source grounds the rule that a surviving mutant is a coverage finding about the suite rather th…
$ grep -oE '^\| S[0-9]{3,4} ' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -V | tail -4
S595
S596
S597
S598
```

- **No prior row on `https://pitest.org`** — the only base-URL match is the S598 row itself. No
  duplicate-base-URL shape (the S178 reject class) is created.
- **Adjacency: S595** (`corpus/SOURCES.md:376`) is the *other* mutation-adequacy source. It is a
  different document (arXiv:2102.11378v2, `paper`, scope "mutation analysis's own definition as a
  test-adequacy criterion, limited to what the abstract states"). S598 adds the killed/lived
  mechanism and the gauge sentence; the two rows do not restate each other's scope and neither
  quote is in the other's bytes. Adjacent concept, distinct carrier — the same shape the registry
  already holds for S594/S578-style splits.
- **Id state.** At HEAD (`466d28bc229f13106e9fa1d3d65221b19a58e120`) the registry's max is S597
  (`git show HEAD:corpus/SOURCES.md | grep -c '^| S59[78] '` → `1`, the S597 row). In the working
  tree another seat has already drafted **S598** (plus a round-83 search-log paragraph) as an
  uncommitted change: `git diff --stat corpus/SOURCES.md` → `1 file changed, 3 insertions(+)`
  (`@@ -378,0 +379 @@` row, `@@ -454,0 +456,2 @@` search paragraph). Per the seat spec I did
  **not** edit `corpus/SOURCES.md`; the L1 owns the append. My independent pin **confirms** the
  row's immutable facts — sha256 `b0c7e050…`, 12023 bytes, 284 lines, quote at `:114`, 14 words,
  the no-redirect 200 and the `2026-06-03` last-modified all reproduce — and contradicts one
  anchor detail (§9).

## 9. Defects found in another seat's bytes

**D83-SC1 (anchor precision, status-neutral) — the 51-word block range.**
`corpus/SOURCES.md:379` (working-tree S598 row) states the block is at "raw lines 108-113", and
`corpus/knowledge/counter-mutation-adequacy-r83.md:17` repeats "pinned lines 108-113, defines
killed and lived". Measured against the pinned bytes (sha256 matches the row, so this is the same
file): raw `108-113` renders to **31** words and contains only the middle paragraph; the block
that the page itself labels "51 words" (`:102`) occupies raw **`106-114`** (body `107`, `110-112`,
`114`) and renders to exactly **51** words. Two consequences: the cited range omits `:114`, which
is the very sentence (the adequacy gauge) the row's anchor column leads with; and it includes
`108-109`, which are an empty `<p>` and a blank line. Fix: replace `raw lines 108-113` with
`raw lines 106-114 (body 107, 110-112, 114; 51 rendered words)` in both places. Nothing else in
the row or the knowledge entry conflicts with my independent measurements (sha256, size, line
count, `:114`, 14-word quote, ETag, last-modified, the mutators-page exclusion, the "identified 2 /
included 1" search accounting all check out).

**Observation, not a defect.** `corpus/evidence/sources-r83/pitest-home.html` was already present
at entry with the same bytes; I re-fetched and re-wrote it so the pin's provenance is a curl
write in this seat's own receipt, not an inherited file. The uncommitted S598 row and the
round-83 search paragraph (`corpus/SOURCES.md:457`) were not written by me and I did not touch
them; my §2/§3/§6 receipts independently reproduce every number in that paragraph
(`12023` bytes, `284` lines, sha256 prefix `b0c7e050…`, ETag `6a1fe9b2-2ef7`, last-modified
`2026-06-03`, `:114`, 14 words, second fetch byte-identical, mutators page excluded).

## 10. Verification ledger

**Verified by execution in this seat** (every command above was run; outputs are pasted, not
recalled): final URL and `http_code=200` with `num_redirects=0`; `last-modified`, `ETag`,
`content-length`, `date` headers; sha256 of three fetches and the pin (one value); `cmp` identity
three ways (fetch1↔fetch2, fetch1↔pin, plus the L1's original by hash); byte count 12023 and line
count 284; LF-only, UTF-8, newline-terminated; ETag size suffix `0x2ef7` = 12023; conditional GET
`304`; quote at `:114` with occurrence count 1 and 14 words; the 51/31/37-word arithmetic for
`106-114` / `108-113` / `106-112`; the absence counts in §6; the mutators page's identity
(67033 bytes, 1459 lines, sha256 `a31331da…`, 200, no redirect) and its absence counts; the
registry duplicate sweep and id state.

**Not verified / limits.** (a) The page's true publication or revision date: no visible date,
author, version or copyright in the bytes; only the server `last-modified`, and the response came
from a Fastly edge (`x-cache: HIT`, `x-origin-cache: HIT`), so the header is the edge's copy of
the origin's stamp, not a first-hand origin read. (b) That another edge or another
`Accept-Encoding` (`vary: Accept-Encoding`) yields the same decoded bytes — I fetched only from
this host/edge, identity-encoded; the two-fetch identity and the ETag 304 bound the risk but do
not exclude a differently-encoded variant being served elsewhere. (c) That the page's own "51
words" counting convention equals `wc -w` in general — my `wc -w` lands exactly on 51 for
`106-114` and on 31/37 for the other ranges, which is consistent but is a coincidence check, not
PIT's stated method. (d) The registry's tier contract: `corpus/SOURCES.md` carries the tier column
and precedents but no written tier table that I could find (`grep -n '^#\{1,3\} '` → sections
`Registry`, `Paths`, `Search log`, `Leads (unopened)`), so I neither confirm nor contest the
drafted `docs | A`; the Gate owns that call. (e) Nothing about PIT's software behaviour was
executed or tested — the pin grounds a definition only.

**Recipe to reproduce the whole pin** (throwaway dir, no lane writes):

```
$ S=$(mktemp -d); cd "$S"
$ curl -sSL -o a.html -w 'code=%{http_code} final=%{url_effective}\n' https://pitest.org/
$ curl -sSL -o b.html https://pitest.org/
$ cmp a.html b.html && sha256sum a.html
b0c7e0505c51c95b596060ef27babbce08e72d5aaf4557eb002c2637d2bf10cc  a.html
$ wc -c < a.html; wc -l < a.html          # 12023 / 284
$ grep -n 'The quality of your tests can be gauged' a.html   # 114
$ sed -n '106,114p' a.html | sed 's/<[^>]*>//g' | wc -w      # 51
$ cd /; rm -rf "$S"
```

## 11. Scope statement

Exactly two lane paths were written by this seat: the pin
`/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r83/pitest-home.html`
(overwritten with identical curl bytes) and this report. Scratch lived at
`/fast/scratch/hyaku/mori-r83/Mo83Sc01Source` and is removed before yield. No file outside
`/home/vgpnk/Projects/shokunin/mori-shokunin` was written; no `corpus/SOURCES.md`,
`.ufo/state/`, `MANIFEST.json`, `.ufo/watchdog.log` or `.scratch/` write; no commit, push, add,
checkout, reset, stash or jj command; no subagent.
