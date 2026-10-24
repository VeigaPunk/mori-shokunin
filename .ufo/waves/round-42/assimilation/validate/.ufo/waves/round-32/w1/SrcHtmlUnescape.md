# SrcHtmlUnescape — candidate S177 (new-source gate, C1 method support)

Seat: MoriR32A2.SrcHtmlUnescape. Decision: **admit, A, mined**.
Scratch: `/fast/scratch/hyaku/mori-r32/MoriR32A2.SrcHtmlUnescape/`

## 1. Fetch

- id: S177
- url: https://docs.python.org/3/library/html.html
- accessed: `2026-10-23T01:31:26Z` (`date -u +%FT%TZ` immediately before and after the fetch)
- command: `curl -sSL --fail -m 60 https://docs.python.org/3/library/html.html -o S177.src`; curl exit 0, one try
- redirect: none — a probe printed `final_url=https://docs.python.org/3/library/html.html code=200 bytes=20100`
- bytes saved unchanged: 20100; `<title>html — HyperText Markup Language support — Python 3.15.1 documentation</title>` (S177.src)
- sha256: `650c53ac7695b816427335a6fbdf3852c41c01d7458f3b502c2af4e916441bb0`
- copy: `/fast/scratch/hyaku/mori-r32/MoriR32A2.SrcHtmlUnescape/S177.src`
- normalised text (from `seat-check.py text`, 2365 chars / 2378 bytes): `S177.norm.txt`

URL-newness check (binding): tip `grep -cF 'https://docs.python.org/3/library/html.html' corpus/SOURCES.md` → `0`;
base `git show 641a6e86ec…:corpus/SOURCES.md | grep -cF <same>` → `0`; id free at tip (`grep -cF '| S177 |'` → `0`).
No existing row carries this URL, so no prefix collision.

Grounding: `count-c1.py:99-103` (HTML branch drops tags then `text = html.unescape(text)`) and `count-c1.py:107-109`
(`quotes_of` applies `fold(html.unescape(q…))` to every quote). The page documents exactly that function.

## 2. Ready-to-paste rows

Gate row for `## Gate` in `corpus/lessons/round-32.md` (header `| id | url | accessed | sha256 | located quotes | decision |`, as in `corpus/lessons/round-31.md:70-71`):

```markdown
| S177 | https://docs.python.org/3/library/html.html | 2026-10-23T01:31:26Z | 650c53ac7695b816427335a6fbdf3852c41c01d7458f3b502c2af4e916441bb0 | html.unescape(s) entry, first sentence (7 words): "Convert all named and numeric character references"; html.unescape(s) entry, first sentence (9 words): "in the string s to the corresponding Unicode characters"; html.unescape(s) entry, second sentence (18 words): "This function uses the rules defined by the HTML 5 standard for both valid and invalid character references" | admit, A, mined |
```

SOURCES row for the Registry table (`corpus/SOURCES.md:5` column order):

```markdown
| S177 | Python html module documentation — https://docs.python.org/3/library/html.html | docs | A | the documented contract of html.unescape only: all named and numeric character references (named, decimal and hex) converted to the corresponding Unicode characters under the HTML5 rules for both valid and invalid references; not the CPython implementation, not the counter's whitespace folding or quote extraction | `html.unescape(s)` entry in the html module page; Python 3.15.1 documentation opened 2026-10-23; sha256 650c53ac7695b816; 20 100 bytes | html.unescape converts all named and numeric character references to the corresponding Unicode characters using the HTML5 rules for valid and invalid references; the recheck method matches quotes against entity-unescaped text, so a quote must be copied from the normalised output — a literal entity spelling in the quote cell is unescaped a second time and will not match. | mined | 2026-10-23 | on-release | corpus/evidence/recheck-r32/README.md |
```

Integration: commit the saved bytes unchanged at `corpus/evidence/sources-r32/S177.src` (counter `NEWCOPIES`).
Copy path above; its sha256 must stay `650c53ac7695b816…`.

## 3. Quote → teaches-cell bearing

The page's `html.unescape(s)` entry in normalised text: `html. unescape ( s ) ¶ Convert all named and numeric
character references (e.g. &gt; , &#62; , &#x3e; ) in the string s to the corresponding Unicode characters. This
function uses the rules defined by the HTML 5 standard for both valid and invalid character references …`

1. `"Convert all named and numeric character references"` (7 words) — the head of the first sentence: the input set
   the function converts. Bears on teaches "all named and numeric character references".
2. `"in the string s to the corresponding Unicode characters"` (9 words) — the tail of the same sentence (the entity
   examples between are skipped, they contain `&` and are deliberately not quoted): the conversion target is
   Unicode. Bears on "converted to the corresponding Unicode characters".
3. `"This function uses the rules defined by the HTML 5 standard for both valid and invalid character references"`
   (18 words) — the second sentence: the HTML5 rule set, valid and invalid references. Bears on "using the HTML5
   rules for valid and invalid references".

Together they are the documented contract of `html.unescape`; the counter applies that same function to the page
(`normalise`) and to each drafted quote (`quotes_of`), which is why the method quotes the normalised text. Verdict
follows: the live page says exactly this, so the row is admitted; no drift.

## 4. Checks run

`seat-check.py row` covers only the 34 frozen population ids, so for a new id it prints `S177: not in population`
(exit 2). I therefore replicated the frozen new-source check's own expressions (`count-c1.py:272-317`) in
`gate_check.py`, using the counter's imported `cells`, `quotes_of`, `normalise`, `tokens`:

```
gate_cells 6 src_cells 11
url https://docs.python.org/3/library/html.html
status 'mined' status_ok True len_ge_11 True
gate_url_eq True https True
sha_eq True
quotes 3 words [7, 9, 18] in_copy [True, True, True]
decision 'admit, A, mined' ok True
shared ['both', 'character', 'characters', 'corresponding', 'html', 'invalid', 'named', 'numeric', 'references', 'rules', 'unicode', 'valid']
GATE_SIM=pass
```

Transcript: `S177.transcript.txt` (sha256sum, wc, tip/base absence, sim). Word counts 7/9/18 are inside 3-25; every
quote is verbatim in `S177.norm.txt`, has no `&`, pipe, backslash or typographic character, and starts/ends on a
whole word.

The gate row also survives the counter's own `section()` / `table()` parsing (synthetic `## Gate` section with the
round-31 header, `lesson_sim.py`):

```
section_starts '## Gate'
hdr ['id', 'url', 'accessed', 'sha256', 'located quotes', 'decision']
gate_rows_for_S177 1 cells 6
decision 'admit, A, mined'
TABLE_SIM=pass
```

## 5. README paragraph draft — `corpus/evidence/recheck-r32/README.md`

```markdown
### Entity handling in the normalise step (S177)

The recheck method's quote-copying step rests on the documented behaviour of `html.unescape`. The counter normalises
each fetched page by dropping tags and then unescaping entities (`count-c1.py:99-103`), and it applies the same
unescape to every drafted quote (`count-c1.py:107-109`). Python's `html` module documentation (S177,
https://docs.python.org/3/library/html.html) states that `html.unescape(s)` converts all named and numeric character
references to the corresponding Unicode characters and follows the HTML5 rules for both valid and invalid references.
Because both sides of the check are unescaped once, a quote must be copied from the normalised text printed by
`seat-check.py text` — not from the raw page source, where a displayed entity is double-escaped, and not with its own
literal entity spellings, which the quote parser would unescape a second time so that the quote no longer matches the
copy. Every row in the `## Recheck` table follows that rule, per S177.
```

## 6. Drift / unknowns

No drift (new source, verdict admit). Unknowns: the URL is the unversioned `/3/` current-docs path and the page now
reads "Python 3.15.1 documentation", so the bytes may move at a Python release; the row's `on-release` recheck
interval covers that. The quoted contract sentence has been stable across Python 3, but that is [INFERENCE] from this
single fetch, not verified history.

## Tooling

No installs or updates were made for this seat.
