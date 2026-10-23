# SrcUnicodedata — candidate S176 (Python `unicodedata`, NFKC) opened for the C1 recheck method

Seat `MoriR32A2.SrcUnicodedata` (wave 1). Question: does a new source ground the counter's quote
normalisation step (`fold`, NFKC) well enough to admit as S176? Answer: **admit, A, mined** — the page
defines `normalize()` and the NFKC form exactly, and it also grounds *why* the explicit typographic
fold map is needed after NFKC. No lane file was modified; this report is the seat's only write.

## 1. The fetch

| item | value |
|---|---|
| id | S176 |
| url | https://docs.python.org/3/library/unicodedata.html |
| accessed (UTC, at fetch) | 2026-10-23T01:31:32Z |
| http | `http=200 size=55620` (curl `-sSL --fail -m 60`, exit 0, one try) |
| bytes | 55620 |
| sha256 (unchanged fetched bytes) | d3d261bcde4906ce9685d8e362a7bbb0dc4b254b1fc12f70ec46a9db65e77375 |
| scratch copy | /fast/scratch/hyaku/mori-r32/MoriR32A2.SrcUnicodedata/S176.src |
| normalised text | /fast/scratch/hyaku/mori-r32/MoriR32A2.SrcUnicodedata/S176.txt |
| page identity | `<title>unicodedata — Unicode Database — Python 3.15.1 documentation`; "Last updated on Oct 23, 2026 (00:01 UTC)" |

Command: `curl -sSL --fail -m 60 https://docs.python.org/3/library/unicodedata.html -o S176.src`;
`date -u +%FT%TZ` printed `2026-10-23T01:31:32Z` before and after; `sha256sum S176.src` printed the
digest above; `wc -c` printed 55620. The bytes were not edited, decompressed or re-encoded.

URL uniqueness (both halves of the rule):
- `grep -F -c "https://docs.python.org/3/library/unicodedata.html" corpus/SOURCES.md` → `0`, exit 1.
- Existing `docs.python.org` URLs at base are hashlib.html, json.html, os.html, pathlib.html (command:
  `grep -oE 'https?://[^ |)]*docs\.python\.org[^ |)]*' corpus/SOURCES.md | sort -u`). None is a prefix of
  mine and mine is not a prefix of any of them (the paths differ at the module name), so no prefix
  collision.
- ids S175 and S176 are both absent from the lane SOURCES.md (`grep -cE '^\| S(175|176) \|'` → `0`, exit 1),
  so S176 is unclaimed.

Integration note for L1: commit the scratch copy unchanged as
`corpus/evidence/sources-r32/S176.src` (the frozen new-source check compares its sha256 with the gate
row). I did not write it — the seat is report-only.

## 2. Ready-to-paste rows

Gate row for `corpus/lessons/round-32.md` under `## Gate` (header
`| id | url | accessed | sha256 | quotes | decision |`):

```
| S176 | https://docs.python.org/3/library/unicodedata.html | 2026-10-23T01:31:32Z | d3d261bcde4906ce9685d8e362a7bbb0dc4b254b1fc12f70ec46a9db65e77375 | unicodedata.normalize entry, valid form values, S176.src:516-517 (10 words): "Valid values for form are 'NFC', 'NFKC', 'NFD', and 'NFKD'."; NFKC definition, S176.src:534-536 (15 words): "The normal form KC (NFKC) first applies the compatibility decomposition, followed by the canonical composition."; NFKD definition, S176.src:533-534 (19 words): "The normal form KD (NFKD) will apply the compatibility decomposition, that is, replace all compatibility characters with their equivalents." | admit, A, mined |
```

SOURCES row (11 columns, same order as `corpus/SOURCES.md:5`; append at the end of the registry table,
before `## Paths`):

```
| S176 | Python 3.15.1 unicodedata — the Unicode Database (normalize and the NFKC/NFKD forms) — https://docs.python.org/3/library/unicodedata.html | docs | A | the documented semantics of unicodedata.normalize and the NFKC/NFKD normal forms only; not any Python implementation detail, not the recomposition behaviour of any particular runtime | Normalization section: unicodedata.normalize ( form , unistr , / ); the NFKC/NFKD paragraphs; https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize; Python 3.15.1 page last updated 2026-10-23 00:01 UTC | unicodedata.normalize() returns a requested normal form; the NFKC form is the compatibility decomposition followed by the canonical composition, and NFKD replaces compatibility characters with their equivalents. | mined | 2026-10-23T01:31:32Z | on-release | corpus/evidence/recheck-r32/README.md |
```

`on-release` is the recheck cadence: this is a live `docs.python.org/3` page (3.x development branch,
3.15.1 at fetch), so its bytes can drift.

## 3. What each quote bears on

Row cells used for the topic test: teaches = "unicodedata.normalize() returns a requested normal form;
the NFKC form is the compatibility decomposition followed by the canonical composition, and NFKD replaces
compatibility characters with their equivalents"; anchor = the normalize entry and NFKC/NFKD paragraphs;
scope = the documented semantics only.

1. `"Valid values for form are 'NFC', 'NFKC', 'NFD', and 'NFKD'."` (10 words) — raw S176.src:516-517, in
   the normalize() entry opened at S176.src:513-514 (`<dt ... id="unicodedata.normalize">`). Bears on the
   teaches claim that `normalize()` returns a *requested* normal form: it enumerates the four valid values.
   Note the source uses typographic quotes (`‘NFC’`); after `fold` both copy and quote carry ASCII `'`,
   which is why the quote as written is found in the normalised copy (`in_copy=True`).
2. `"The normal form KC (NFKC) first applies the compatibility decomposition, followed by the canonical composition."`
   (15 words) — raw S176.src:534-536. This is the definition the assignment asked for, and it is the
   teaches claim verbatim: NFKC = compatibility decomposition, then canonical composition.
3. `"The normal form KD (NFKD) will apply the compatibility decomposition, that is, replace all compatibility characters with their equivalents."`
   (19 words) — raw S176.src:533-534. Bears on the teaches clause "NFKD replaces compatibility characters
   with their equivalents" and defines the "compatibility decomposition" term that quote 2 uses.

Verdict: `admit` — the page is exactly the normative statement of the mechanism the counter implements,
so quoting it cannot be a coincidental match on unrelated prose.

## 4. Checks run

`seat-check.py row S176 …` (the helper only knows the 34 recheck ids, so it refuses a new source):

```
S176: not in population
exit=2
```

Because that helper cannot score a gate row, I ran the counter's *own* new-source block — the code at
`.ufo/waves/round-32/count-c1.py:275-320` copied verbatim, with only `show()` redirected to the scratch
copies (base SOURCES without the row, tip SOURCES with the row, the Gate table, the README, and the
committed-copy path) and `quotes_of`/`normalise`/`cells`/`table`/`section`/`tokens` imported unchanged from
the frozen counter. Output:

```
gate header: ['id', 'url', 'accessed', 'sha256', 'quotes', 'decision'] gate rows: 1
cells: 11 status: mined url: https://docs.python.org/3/library/unicodedata.html
quotes: 3 words: [10, 15, 19] in_copy: [True, True, True]
shared_tokens: ['canonical', 'characters', 'compatibility', 'composition', 'decomposition', 'equivalents', 'followed', 'form', 'nfkc', 'nfkd', 'normal'] topic_ok: True
new_ok=1 new_failures=none
```

So every clause of the new-source check passes on paper: 11 cells, status `mined`, url absent at base,
one gate row whose url equals the SOURCES url, gate sha equal to the copy sha, three quotes of 10/15/19
words all inside the normalised copy, decision starting `admit`, and the id cited in the README. The
SOURCES cells also clear the R2-style topic test with 11 shared content tokens (11× the minimum of 2).
[INFERENCE] The real counter additionally reads these bytes from the lane at a rev; nothing else in the
block can differ, since I passed the same functions and the same file contents.

## 5. Drift details

None. This is a new-source admission, not a recheck row: the page was opened live once, at
2026-10-23T01:31:32Z, and supports every clause of the teaches cell. Residual risk is ordinary live-page
drift (3.15.1 dev docs), which the `on-release` recheck column records.

Second-order fact worth carrying into the method note: NFKC does **not** fold the typographic quotes and
dashes, so the `FOLD` map in `count-c1.py:77` is not redundant. Observed on this host
(`python3`, stdlib `unicodedata`, no install):

```
input : ['0x2018', '0x2019', '0x201c', '0x201d', '0x2013', '0x2014', '0xa0']
nfkc  : '‘’“”–— ' ['0x2018', '0x2019', '0x201c', '0x201d', '0x2013', '0x2014', '0x20']
nfkc alone already equals folded: False
```

U+00A0 → U+0020 is the only entry the NFKC step already performs; U+2018/2019/201C/201D/2013/2014 survive
NFKC unchanged, which is what the page itself warns about at S176.src:537-539 ("Even if two unicode
strings are normalized and look the same to a human reader … they may not compare equal").

## 6. Draft README paragraph for `corpus/evidence/recheck-r32/README.md`

> **Step 2, quote normalisation — S176.** The recheck method does not compare a quote with the served
> bytes directly: `count-c1.py` folds both the fetched copy and every quoted passage through
> `unicodedata.normalize('NFKC', s)`, then maps typographic quotes and dashes to ASCII and collapses
> whitespace runs (`fold`, `count-c1.py:80-84`, applied to copies by `normalise`, `:92-103`, and to quotes
> by `quotes_of`, `:107-109`). S176 (https://docs.python.org/3/library/unicodedata.html, Python 3.15.1,
> opened 2026-10-23, sha256 d3d261bcde4906ce9685d8e362a7bbb0dc4b254b1fc12f70ec46a9db65e77375) grounds that
> step: it defines `normalize(form, unistr, /)` as returning the normal form `form` for `unistr`, with
> `'NFC'`, `'NFKC'`, `'NFD'` and `'NFKD'` as the valid values, and defines NFKC as the compatibility
> decomposition followed by the canonical composition, while NFKD "will apply the compatibility
> decomposition, that is, replace all compatibility characters with their equivalents". S176 also shows
> the limit of the NFKC step alone: the page states that two normalized strings which look the same to a
> human reader may still not compare equal, and NFKC leaves U+2018, U+2019, U+201C, U+201D, U+2013 and
> U+2014 untouched (only U+00A0 becomes a space), so the explicit `FOLD` map after the NFKC call is what
> makes a quote copied from a rendered page match the served bytes. Both halves of the fold are therefore
> sourced, not invented: the normal form by S176, the typographic map by S176's own caveat plus the
> counter's observed behaviour.

## 7. Bounds and tooling

- Writes: this report only. All scratch work stayed under
  `/fast/scratch/hyaku/mori-r32/MoriR32A2.SrcUnicodedata/` (S176.src, S176.txt, row.txt, gate.txt, sim/).
- No git or jj write; no lane index or jj state touched. Lane reads: `grep`, `cat`, `sed -n`, `read`, and
  one `git -C … rev-parse/log` read-only pair (`8ab61affbd2fc59030040bf80cddc08f7c60ad82`,
  `8ab61af round-32: C0 control receipts …`).
- No installs or upgrades (pacman is paused host-wide and nothing was needed). No subagents, no background
  jobs; every command was wrapped in `timeout` (≤600 s).
- No bot challenge was met; the one fetch returned 200 on the first try.
