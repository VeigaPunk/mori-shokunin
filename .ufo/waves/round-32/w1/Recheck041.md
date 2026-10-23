# Recheck041 — S041 (wave 1, round 32 C1)

Seat: `MoriR32A2.Recheck041` (scout, leaf). Assigned id: **S041**. Verdict: **current**.
No tool installs or updates were needed (nothing beyond curl, python3, coreutils):

```
$ curl --version | head -1   # curl 8.x, distro package, already present
$ timeout 120 python3 --version  # Python 3.x, already present
```

## 1. Fetch

| item | value |
|---|---|
| population url | `https://www.rfc-editor.org/rfc/rfc6585` |
| fetch command | `curl -sSL --fail -m 60 https://www.rfc-editor.org/rfc/rfc6585 -o S041.src` (1 try, exit 0) |
| redirect | `HTTP/2 301` → `location: https://www.rfc-editor.org/info/rfc6585/` (the url cell stays the population url; the bytes are the /info/ rendering of RFC 6585) |
| effective url | `https://www.rfc-editor.org/info/rfc6585/` |
| curl write-out | `HTTP=200 SIZE=171484 URL=https://www.rfc-editor.org/info/rfc6585/` |
| accessed (UTC, at fetch) | `2026-10-23T01:31:23Z` |
| byte size | 171484 |
| sha256 | `3924746f977d3bd8b086fe275ccd67dc344271753e355cc9eaa9d7e698f0886b` |
| scratch copy | `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck041/S041.src` (bytes unchanged; ends with `</script></body></html>`, no zero-width chars, no BOM) |
| normalised text | `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck041/S041.txt` (16191 bytes, from `seat-check.py text`) |

Commit instruction for L1: copy `S041.src` byte-for-byte to `corpus/evidence/recheck-r32/S041.src`; the
row sha above is that file's sha256, so an unchanged copy satisfies the counter's `copy_sha` check.

## 2. Ready-to-paste row (`## Recheck` table)

```markdown
| S041 | https://www.rfc-editor.org/rfc/rfc6585 | 2026-10-23T01:31:23Z | 3924746f977d3bd8b086fe275ccd67dc344271753e355cc9eaa9d7e698f0886b | "The 429 status code indicates that the user has sent too many requests in a given amount of time"; "Note that this specification does not define how the origin server identifies the user, nor how it counts requests"; "MAY include a Retry-After header indicating how long to wait before making a new request" | current |
```

Parsed with the counter's own `cells()`: 6 cells, `quotes_of()` → 3 quotes with word counts `[19, 19, 15]`.

## 3. Quotes vs the teaches cell

Teaches cell: *HTTP 429 denotes too many requests in a time window; it does not identify a vendor business
error or establish permanent seat death.*

- Q1 `The 429 status code indicates that the user has sent too many requests in a given amount of time`
  — RFC 6585 §4, first sentence. Bears on clause 1 verbatim: 429 is defined as the user sending too many
  requests "in a given amount of time", i.e. a time window. This is the whole normative definition of the
  code on the page; nothing wider is asserted.
- Q2 `Note that this specification does not define how the origin server identifies the user, nor how it counts requests`
  — RFC 6585 §4, second paragraph. Bears on clause 2: the status carries only a rate-limit meaning whose
  identification and counting are left undefined by the spec, so a 429 by itself cannot name a vendor
  business cause or error class. Cross-check: the used-by file itself states this —
  `corpus/knowledge/seat-terminal-status-r17.md:27-28` ("RFC 6585 grounds the generic status meaning, not
  the vendor business cause or OMP recovery").
- Q3 `MAY include a Retry-After header indicating how long to wait before making a new request`
  — RFC 6585 §4. Bears on clause 3: the defined recovery signal is a bounded wait followed by a new
  request, i.e. a transient condition, not permanent seat death.

Verdict `current`: the live page still states the rate-limit-in-a-time-window meaning (§4), still leaves
counting/identification undefined, and still offers Retry-After as the wait signal. The anchor also
holds: the page header reads `Category: Standards Track` / `April 2012` (normalised text, §4 at
"4 . 429 Too Many Requests"). No wording contradicts the teaches cell, so no `Round32` correction is
needed in `corpus/knowledge/seat-terminal-status-r17.md`.

## 4. Seat-check output

```
$ timeout 300 python3 .ufo/waves/round-32/seat-check.py row S041 /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck041/S041.src '"The 429 status code indicates that the user has sent too many requests in a given amount of time"; "Note that this specification does not define how the origin server identifies the user, nor how it counts requests"; "MAY include a Retry-After header indicating how long to wait before making a new request"'
sha256=3924746f977d3bd8b086fe275ccd67dc344271753e355cc9eaa9d7e698f0886b
quotes=3 words=[19, 19, 15] in_copy=[True, True, True]
shared_tokens=['many', 'requests', 'status', 'time'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
```

## 5. Drift details

None. No redirect to a changed document: the 301 is RFC Editor's canonical `/rfc/<n>` → `/info/rfc<n>/`
hop; the body is still RFC 6585 as published April 2012 and the §4 wording is unchanged. No correction
drafted (verdict is not `drifted`).

Remaining unknown: `ROW_CHECK` does not cover R4 (judge receipt) — that needs the reviewer seat named in a
round-32 dispatch file, per `count-c1.py:161-280`. Nothing else outstanding for S041.
