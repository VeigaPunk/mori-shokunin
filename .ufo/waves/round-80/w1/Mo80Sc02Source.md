# Mo80Sc02Source — S595 source pin (C2 grounding, round 80 w1)

Seat: scout, leaf (no subagent dispatch). Lane root `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Candidate: arXiv `2102.11378v2` "Practical Mutation Testing at Scale", abstract page.
Result: **pinned, quote located on the abstract body line, anchor-checked PASS. No duplicate held.**
Scratch: `/fast/scratch/hyaku/mori-r80/Mo80Sc02Source/` (created, used, removed at end — see §7).

## 1. Duplicate sweep BEFORE the fetch (r69 rule)

Run from the lane root, before any network call (first tool batch, 2026-11-04):

```
$ grep -n 'arxiv.org/abs/2102.11378' corpus/SOURCES.md ; echo rc=$?
rc=1
$ grep -n '2102\.11378' corpus/SOURCES.md ; echo rc=$?
rc=1
$ grep -in 'mutation test' corpus/SOURCES.md ; echo rc=$?
rc=1
$ grep -in 'mutation' corpus/SOURCES.md
247:| S350 | systemd.scope(5) — ... (row continues)
369:| S588 | Troubleshoot unexpected reboots using system event logs — ... (row continues)
$ sed -n '247p' corpus/SOURCES.md | grep -o -i '.\{0,50\}mutation.\{0,50\}'
... a host mutation outside mori's detection-and-report province; flip: ...
$ sed -n '369p' corpus/SOURCES.md | grep -o -i '.\{0,50\}mutation.\{0,50\}'
... PASS items=2, able-to-fail label-mutation arm FAIL rc 1 in the same receipt); ...
```

(Those two `sed` lines are elided with `...` at the edges only; the matched substring is verbatim.)

Named nearest held rows at sweep time:

- **id-adjacent (last registry rows):** `S594` (line 375, HTTP Caching RFC 9111 §4.1), `S593` (line 374, Memory Performance Information), `S592`, `S591`.
- **topical neighbours:** **none on mutation testing.** The two `mutation` hits are `S350` (line 247: a *host* mutation — the refused `systemctl reset-failed` action) and `S588` (line 369: the quoted phrase `label-mutation arm` from the r59 critic receipt, inside a Windows-reboot row). A wider sweep `grep -in 'adequacy\|test suite\|mutant'` returns line 60 (`S054`, "over-redaction fails adequacy as well"), line 343 (`S563`, "§Decisive mutants table"), and post-fetch line 376 (`S595` itself); none is a mutation-testing source and none defines mutation analysis.
- `grep -n '^| S595 '` → rc 1 at sweep time: the id was free, so the contract's planned S595 id is available.

No duplicate URL, no duplicate work, no `REJECTED` row to reopen. A later sibling write (`Mo80S01Row`) added `S595` at `corpus/SOURCES.md:376`; that row's anchor cell cites `:121`, the sha256 and the byte/line counts below, and its `used-by` is `corpus/knowledge/mutation-adequacy-r80.md` (not yet present at my last check — not my file).

## 2. Fetch (two independent copies, byte-identical)

```
$ S=/fast/scratch/hyaku/mori-r80/Mo80Sc02Source; mkdir -p "$S"; cd "$S"; export TMPDIR="$S"
$ curl -sS -L --max-time 90 -w 'HTTP=%{http_code} bytes=%{size_download} url=%{url_effective}\n' \
    -A 'mori-source-pin/1.0 (detection-and-report lane; contact: local)' \
    -o abs-fetch1.html 'https://arxiv.org/abs/2102.11378v2'
HTTP=200 bytes=43884 url=https://arxiv.org/abs/2102.11378v2
curl1_rc=0
$ curl ... -o abs-fetch2.html 'https://arxiv.org/abs/2102.11378v2'
HTTP=200 bytes=43884 url=https://arxiv.org/abs/2102.11378v2
curl2_rc=0
$ sha256sum abs-fetch1.html abs-fetch2.html
28ea1f163860348979a3aa9e9ef8e00fc8eb3ecec2762782d639783003f1b884  abs-fetch1.html
28ea1f163860348979a3aa9e9ef8e00fc8eb3ecec2762782d639783003f1b884  abs-fetch2.html
$ wc -lc abs-fetch1.html abs-fetch2.html
  613 43884 abs-fetch1.html
  613 43884 abs-fetch2.html
 1226 87768 total
$ cmp abs-fetch1.html abs-fetch2.html && echo IDENTICAL
IDENTICAL
```

**Both copies: sha256 `28ea1f163860348979a3aa9e9ef8e00fc8eb3ecec2762782d639783003f1b884`, 613 lines, 43884 bytes.** No substitution, no fallback host, no `--compressed` variance risk (no compression negotiated with the default header set).

## 3. Quote location

The visible abstract paragraph is one HTML line, **line 121** of the pin:

```
$ sed -n '121p' abs-fetch1.html | wc -lc
   1 1959
$ sed -n '121p' abs-fetch1.html | cut -c1-260
            <span class="descriptor">Abstract:</span>Mutation analysis assesses a test suite&#39;s adequacy by measuring its ability to detect small artificial faults, systematically seeded into the tested program. Mutation analysis is considered one of the strongest test-adequacy criteria. ...
```

First sentence, exact contiguous span as committed (apostrophe is the HTML entity `&#39;` in the pinned bytes; rendered text reads `suite's`):

```
Mutation analysis assesses a test suite&#39;s adequacy by measuring its ability to detect small artificial faults, systematically seeded into the tested program.
```

**Shortest span that still supports "mutation analysis assesses a test suite's adequacy by measuring its ability to detect small artificial faults"** (keeps the named subject, the object and the mechanism; drops only the participial tail that says *how* the faults are seeded):

```
Mutation analysis assesses a test suite&#39;s adequacy by measuring its ability to detect small artificial faults
```

Word counts (`wc -w` over the exact text):

```
$ printf '%s\n' '<full first sentence>' | wc -w
22
$ printf '%s\n' '<short span>' | wc -w
16
```

Both ≤ 25 words. Dropping `its ability to` would be an ellipsis, not a contiguous span, so 16 is the floor for a verbatim quotation.

**Duplicate-line caveat (measured, not guessed):** the same sentence is also embedded in page metadata before the abstract body, so `grep -n` returns four lines, not one:

```
$ grep -n 'Mutation analysis assesses a test suite&#39;s adequacy by measuring its ability' abs-fetch1.html | cut -d: -f1
28      # og:description
32      # twitter:description
39      # citation_abstract (schema.org meta)
121     # the abstract body — the only visible occurrence
$ awk 'NR==121' abs-fetch1.html | grep -c 'Mutation analysis assesses'
1
```

The anchor therefore records `:121` — the abstract body — and not 28/32/39, which are machine-readable copies of the same string and would make a "located" verdict true but the location misleading.

## 4. Lane checker verdict (it applies)

`tools/mori-anchor-check.py` is HTML-agnostic by design: it reads the pin as UTF-8, splits lines and counts exact substring occurrences on the recorded span; its own selftest fixture is `fixture.html`. Run verbatim against the installed pin, with the entity exactly as pinned:

```
$ python3 -I tools/mori-anchor-check.py \
    --pin corpus/evidence/sources-r80/arXiv-2102.11378v2-abs.html \
    --check 's595a|121|16|Mutation analysis assesses a test suite&#39;s adequacy by measuring its ability to detect small artificial faults' \
    --check 's595b|121|22|Mutation analysis assesses a test suite&#39;s adequacy by measuring its ability to detect small artificial faults, systematically seeded into the tested program.'
anchor item=s595a span=121 verdict=ok located_on=121 occurrences=1 words_counted=16 words_recorded=16
anchor item=s595b span=121 verdict=ok located_on=121 occurrences=1 words_counted=22 words_recorded=22
ANCHOR_CHECK: PASS items=2 ok=2 pin_sha256=28ea1f163860348979a3aa9e9ef8e00fc8eb3ecec2762782d639783003f1b884 pin_bytes=43884
anchor_rc=0
```

Verdict `PASS` on the same sha256 the pin carries; the tool re-derived the pin digest from the file it read, so the anchor and the pin are bound in one receipt.

Negative arm (the check can fail, and says why): the same span with the *rendered* apostrophe instead of the pinned entity does **not** locate, because the pin stores `&#39;`:

```
$ python3 -I tools/mori-anchor-check.py --pin corpus/evidence/sources-r80/arXiv-2102.11378v2-abs.html \
    --check "s595c|121|16|Mutation analysis assesses a test suite's adequacy by measuring its ability to detect small artificial faults"
anchor item=s595c span=121 verdict=mislocated located_on=- occurrences=0 words_counted=- words_recorded=16
ANCHOR_CHECK: FAIL items=1 ok=0 mislocated=1 wordcount_mismatch=0 pin_sha256=28ea1f... pin_bytes=43884
rendered_rc=1
```

So the prose may quote `suite's`, but any `--check` spec or SOURCES anchor cell that carries an exact-quote check must carry `&#39;` as the pinned bytes do. [INFERENCE] The row at `corpus/SOURCES.md:376` currently names only the line and the digest; if a later seat adds an exact-quote spec there, it must use the entity or it will score `mislocated` against this pin.

## 5. Committed pin and README

```
$ cp -p abs-fetch1.html corpus/evidence/sources-r80/arXiv-2102.11378v2-abs.html
$ sha256sum corpus/evidence/sources-r80/arXiv-2102.11378v2-abs.html
28ea1f163860348979a3aa9e9ef8e00fc8eb3ecec2762782d639783003f1b884  corpus/evidence/sources-r80/arXiv-2102.11378v2-abs.html
$ wc -lc corpus/evidence/sources-r80/arXiv-2102.11378v2-abs.html
  613 43884 corpus/evidence/sources-r80/arXiv-2102.11378v2-abs.html
$ cmp abs-fetch1.html corpus/evidence/sources-r80/arXiv-2102.11378v2-abs.html && echo COPY_IDENTICAL
COPY_IDENTICAL
```

`corpus/evidence/sources-r80/README.md` written (557 bytes): one paragraph naming the document, the two-curl identity, sha256, 613 lines / 43884 bytes, fetch date 2026-11-04, and that the bytes are public-document bytes only. Fetch date recorded also by file mtime `2026-11-04 03:08:51 -0300` and by `date -u` `2026-11-04T06:10:03Z` at report time.

## 6. What the abstract does NOT support (for the entry's Limits)

Counts are `grep -ic` over the pin; the abstract body column is `sed -n '121p' | grep -ic`:

| Term | whole pin | abstract body (line 121) |
|---|---|---|
| `equivalent` | 0 | 0 |
| `surviving` | 0 | 0 |
| `survivor` | 0 | 0 |
| `Python` | 0 | 0 |
| `selftest` / `self-test` | 0 / 0 | 0 / 0 |
| `green` | 0 | 0 |
| `passing` | 0 | 0 |
| `mutation score` | 0 | 0 |

The eight `javascript` hits in the whole pin are site chrome (`<script>` blocks), zero in the abstract body.

Not supported, therefore:

1. **No claim about equivalent mutants** — the word does not occur; the abstract speaks only of "mutants that are likely to be irrelevant to developers" and of filtering/selection, which is not the equivalence relation.
2. **No surviving-mutant metric** — neither `surviving` nor `survivor` occurs, and no mutation-score definition is given; the abstract's evaluation reports "orders of magnitude fewer mutants" and improved "mutant quality and actionability", not a survivor count.
3. **No claim about any Python tool** — `Python` occurs zero times; the setting is Google's code-review pipeline (two billion lines, 500,000,000 tests/day, 24,000+ developers, 1,000+ projects), not a language or a tool the lane runs.
4. **No claim that a green selftest is adequate** — `green`, `passing` and `selftest` are absent; the abstract defines what mutation analysis measures and calls it "one of the strongest test-adequacy criteria", which is a statement about the criterion, not about any particular passing check.
5. **No claim that a green unmutated run is inadequate** — the abstract never mentions an unmutated or green run at all; that contrast is the lane's inference (round-80 S595 row's `teaches` cell states it), not a sentence of the abstract.
6. **No universal or industrial-completeness claim for mori** — the paper's scale result is its own industrial setting; nothing in the abstract transfers to a six-mutant fixture or to any local harness.

Routed observation (detection and report only, not edited — `corpus/SOURCES.md` belongs to `Mo80S01Row`): the landed S595 `teaches` cell at line 376 reads "a green unmutated run alone does not measure" adequacy. Per item 5 that sentence is stronger than the pinned abstract, which nowhere mentions a green or unmutated run. It is a fair inference from the definition plus "strongest test-adequacy criteria", but if the entry's Gate quotes the abstract for it, the quote does not carry the word "green". The safe cell wording is the definition itself (16-word span above); the contrast belongs in the entry's reasoning, labelled as inference.

## 7. Scratch cleanup

```
$ rm -rf -- /fast/scratch/hyaku/mori-r80/Mo80Sc02Source
$ ls -d /fast/scratch/hyaku/mori-r80/Mo80Sc02Source 2>&1
ls: cannot access '/fast/scratch/hyaku/mori-r80/Mo80Sc02Source': No such file or directory
ls_rc=2
$ ls /fast/scratch/hyaku/mori-r80/
Mo80E02Correct  Mo80L01Probe  Mo80M01Mutant  Mo80R01Counter  Mo80Sc01Recon  abs2102.html  ax.xml  ax2.xml  census-start.txt  probe
```

My seat tree is gone. The shared root holds other seats' entries (`Mo80*` directories) plus loose files (`abs2102.html`, `ax.xml`, `ax2.xml`, `census-start.txt`, `probe`) that this seat did not create and does not touch; `abs2102.html` is not mine and is not a committed artifact — I did not read, write or delete it. Nothing of mine under `/tmp`. No mutating git/jj command: only `git -C <lane> status --porcelain` (read-only) was used, once, to confirm which paths the wave has touched.

## 8. Own defects (what I got wrong, and how I caught it)

1. **First sweep lacked exit-code evidence.** My first pass used the `grep` tool with one combined regex (`2102\.11378|arxiv\.org/abs/2102\.11378|mutation test`), which returned "No matches found" but no rc. The spec asks for `grep -n` per pattern, so I re-ran three separate `grep -n` commands; all rc 1. Caught by re-reading my own step list before fetching — the fetch had not yet happened, so the ordering rule was preserved.
2. **I assumed one located line.** I expected `grep -n <first sentence>` to return only the abstract line; it returned 28, 32, 39 and 121. The sentence is duplicated into `og:description`, `twitter:description` and `citation_abstract`. Caught by reading the full grep output instead of the first hit; recorded so the anchor pins the abstract *body* line, and so the checker's `occurrences=1` (per-line) is not over-read as "occurs once in the file".
3. **Two commands were backgrounded mid-flight** by incoming peer messages, so their outputs arrived asynchronously; no result was lost, but the report's numbering reflects the re-run that produced the recorded receipts, not the interrupted invocation.
4. **I did not write the knowledge entry** (`corpus/knowledge/mutation-adequacy-r80.md`) — it is outside this seat's file ownership and did not exist at my last check; the S595 row's `used-by` cell already points at it, so the entry's author must use the 16-word span and the Limits list in §6.
