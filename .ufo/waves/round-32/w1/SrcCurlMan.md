# SrcCurlMan — S175, the curl(1) man page (grounds the C1 recheck fetch)

Seat `MoriR32A2.SrcCurlMan` (leaf, wave 1). Assignment: open candidate S175 for the C1 recheck method, locate the
passages for `--fail`/`-f` (exit 22), `-L` (follow redirects), `-m`/`--max-time` (exit 28) and the EXIT CODES entries
22 and 28, and draft the gate row, the SOURCES row and the README paragraph. All work stayed in this report and
`/fast/scratch/hyaku/mori-r32/MoriR32A2.SrcCurlMan/`.

## 1. Fetch record (only id: S175)

| field | value |
|---|---|
| url | https://curl.se/docs/manpage.html |
| accessed (UTC at fetch) | 2026-10-23T01:31:33Z |
| command | `curl -sSL --fail -m 60 https://curl.se/docs/manpage.html -o S175.src` (1 try, rc=0) |
| bytes | 465399 |
| sha256 | 9d2b36d00af7240f77480e911ce28346113419dd3eb5ebca1d8cc50284cfe5ca |
| type | HTML (`<!DOCTYPE html>`), ASCII; the counter's HTML branch applies |
| saved copy (unchanged) | `/fast/scratch/hyaku/mori-r32/MoriR32A2.SrcCurlMan/S175.src` |
| normalised text | `/fast/scratch/hyaku/mori-r32/MoriR32A2.SrcCurlMan/S175.txt` = `seat-check.py text` output (one line; 264661 bytes incl. `print` newline, `normalise()` gives 264660 chars) |

URL novelty: `grep -F -c 'curl.se' corpus/SOURCES.md` → 0; at base `641a6e86:corpus/SOURCES.md` → 0. Of the 231 URLs
in current SOURCES.md there is no prefix relation to this URL in either direction; corpus-wide grep for
`curl.se/docs/manpage` → 0 hits.

## 2. Gate row (ready to paste into `## Gate` of corpus/lessons/round-32.md)

```md
| S175 | https://curl.se/docs/manpage.html | 2026-10-23T01:31:33Z | `9d2b36d00af7240f77480e911ce28346113419dd3eb5ebca1d8cc50284cfe5ca` | Options > -f, --fail (24 words): "Fail with error code 22 and with no response body output at all for HTTP transfers returning HTTP response codes at 400 or greater."; Options > -L, --location (11 words): "this option makes curl redo the request to the new place."; Options > -m, --max-time (13 words): "Set the maximum time in seconds that you allow each transfer to take."; Exit codes > 28 (12 words): "Operation timeout. The specified time-out period was reached according to the conditions." | admit, A, mined |
```

The four `(N words)` labels were computed with the counter's own `len(q.split())` after `fold`: 24, 11, 13, 12.
The row has 6 cells; `count-c1.py:299` reads g[1]=url, g[3]=sha256, g[4]=quotes, g[-1]=decision.

## 3. SOURCES row (11 cells, column order of corpus/SOURCES.md:5)

```md
| S175 | curl(1) man page (curl.se) — https://curl.se/docs/manpage.html | docs | A | curl(1) option semantics used by the round-32 recheck fetch only: -f/--fail exit 22 on HTTP error replies, -L/--location following redirects, and -m/--max-time with Exit codes entry 28 for timeouts; not the full curl manual or its other options | Options > -f, --fail; -L, --location; -m, --max-time; Exit codes entries 22 and 28; page opened 2026-10-23, sha256 9d2b36d00af7240f; 465399 bytes | A recheck fetch distinguishes a timed-out or HTTP-error request from a fetched page by curl exit code: --fail returns 22 on HTTP error replies, --max-time caps each transfer and exit 28 marks a timeout, and --location follows redirects so the saved bytes are the final page. | mined | 2026-10-23 | on-release | corpus/evidence/recheck-r32/README.md |
```

## 4. README paragraph draft (corpus/evidence/recheck-r32/README.md)

```md
The recheck method's fetch step is the call `curl -sSL --fail -m 60 <url>` (up to three tries, as `count-c1.py` R3
replays it), and S175, the curl(1) man page (https://curl.se/docs/manpage.html, opened 2026-10-23T01:31:33Z, sha256
`9d2b36d00af7240f77480e911ce28346113419dd3eb5ebca1d8cc50284cfe5ca`), grounds each of its flags. The page's
`Options > -f, --fail` entry says the option fails with error code 22 and writes no response body for HTTP transfers
returning codes at 400 or greater, so a fetch that exits 22 is recorded as a failed attempt rather than quoted as
page text; `Options > -L, --location` says the option makes curl redo the request at the new place, so the saved
`<id>.src` bytes are the final page, not a 3XX body; and `Options > -m, --max-time` caps each transfer while
`Exit codes > 28` names the timeout signal (`Operation timeout`), which is how the transcript separates a timeout
from a page that was retrieved. Exit codes 22 and 28 are therefore the two failure signals the three-try loop keys on.
```

## 5. Quotes: the teaches-cell fact each bears on

1. `Options > -f, --fail` (24 words): "Fail with error code 22 and with no response body output at all for HTTP transfers returning HTTP response codes at 400 or greater."
   Bears on the teaches fact "--fail returns 22 on HTTP error replies": with `--fail`, a 4xx/5xx answer exits 22 and
   yields no body, so the recheck must log it as a failed attempt, not as page text. Verdict `admit` follows: the page
   states the exact failure condition the fetch step relies on.
2. `Options > -L, --location` (11 words): "this option makes curl redo the request to the new place."
   Bears on "--location follows redirects so the saved bytes are the final page". The page's full first sentence is 35
   words (above the 25-word cap); the quoted main clause is the option's action, and the locator names the option.
3. `Options > -m, --max-time` (13 words): "Set the maximum time in seconds that you allow each transfer to take."
   Bears on "--max-time caps each transfer" — the `-m 60` in the method's command line.
4. `Exit codes > 28` (12 words): "Operation timeout. The specified time-out period was reached according to the conditions."
   Bears on "exit 28 marks a timeout", the signal that separates a timeout from a page that was retrieved.

Located but not quoted in the row (kept the row at four quotes; no count cap exists in the gate check):
- `Exit codes > 22` (verbatim, 32 words): "HTTP page not retrieved. The requested URL was not found or returned another error with the HTTP error code being 400 or above. This return code only appears if --fail is used."
  The quoted `--fail` entry already carries "error code 22", so this entry is corroboration; it confirms exit 22
  "only appears if --fail is used".

## 6. Verification actually run

Fresh import of the frozen `count-c1.py` functions (read-only), on the final row strings:

- gate cells = 6; g[1] with backticks and angle brackets stripped equals the row url (True); g[3] with backticks
  stripped equals sha256 of the saved copy (True); g[-1] starts with `admit` (True).
- `quotes_of(g[4])` → 4 quotes, word counts `[24, 11, 13, 12]`, each 3–25 words and each `in normalise(copy)` True.
- SOURCES row: 11 cells; `c[7] == 'mined'`; first https token in `c[1]` = `https://curl.se/docs/manpage.html`; used-by cell exact.
- Shared content tokens between the four quotes and the drafted teaches+anchor+scope: `code, codes, curl, error, fail, http, option, request, time, timeout, transfer` (11; the gate check does not enforce overlap, `count-c1.py:307`).
- `sha256sum` of the saved copy re-run: `9d2b36d00af7240f77480e911ce28346113419dd3eb5ebca1d8cc50284cfe5ca`.
- `seat-check.py row S175 S175.src '<quotes>'` → `S175: not in population` (exit 2): S175 is not one of the 34 C1 rows;
  the new-source check at `count-c1.py:272-315` is the authority and has no quote-count cap.

## 7. Handoff for L1

- Copy `/fast/scratch/hyaku/mori-r32/MoriR32A2.SrcCurlMan/S175.src` byte-exact to
  `corpus/evidence/sources-r32/S175.src`; the counter hashes that committed copy (`count-c1.py:300`).
- Add the gate row under `## Gate` in `corpus/lessons/round-32.md` (the file did not exist at 01:31Z, so section and
  header are L1's to create; the gate table needs a header/separator before this body row).
- Append the SOURCES row; it carries `mined` and a URL absent at base (both checked above).
- Create `corpus/evidence/recheck-r32/README.md`; the counter only requires `S175` to appear in it
  (`count-c1.py:311`), but the paragraph is the round's sourced claim per contract.md:28-29.

## 8. Drift and unknowns

- No drift verdict applies here: S175 is a new source, not a recheck row.
- The URL is unpinned: the page tracks the current curl release (served 2026-10-23; local curl is 8.23.0), so the
  row's recheck stays `on-release`.
- The new-source check does not re-fetch S175 live; it hashes the committed copy and searches quotes in that copy
  (`count-c1.py:300,305-307`). [OBSERVED] Later drift of the URL is therefore not caught by this counter.
- [INFERENCE] A 4xx/5xx recheck fetch exits 22 with no bytes (`--fail` suppresses the body); the fetch transcript
  should record exit codes so a judge can tell an HTTP-error reply from a timeout (28) or a network failure.

## Tooling

No install or update was needed or run (no pacman, uv, npx or binary installs). Tools used: system `curl 8.23.0`
(Release-Date 2026-10-14) and `python3 3.14.8`.
