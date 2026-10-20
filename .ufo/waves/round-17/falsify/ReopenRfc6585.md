# ReopenRfc6585 — fresh attack on SOURCES row S041 (RFC 6585 §4)

Seat: `MoriR17.ReopenRfc6585-4`, wave 2, leaf scout. Assigned row: **S041** only.
Producer this attack is subject to: L1 `MoriR17` (planner and sole integrator); no admission verdict is claimed here.

- URL attacked: https://www.rfc-editor.org/rfc/rfc6585 (row `source`), plain-text
  serialization checked separately: https://www.rfc-editor.org/rfc/rfc6585.txt
- Access date: **2026-10-20** (fresh fetch by this seat, not replayed from the wave-1 receipt)
- Registry row attacked: `corpus/SOURCES.md:47`; lesson gate row: `corpus/lessons/round-17.md:47`;
  knowledge consumer: `corpus/knowledge/seat-terminal-status-r17.md:1,21,26-28`
- Opening receipt re-read (not trusted as evidence): `.ufo/waves/round-17/build/SrcRfc6585.md:9,15-21`

## 1. Fresh fetch, located quote

Commands (lane root, this seat, rc as shown):

```
curl -fsSL https://www.rfc-editor.org/rfc/rfc6585 -o /dev/null -w '%{http_code} %{size_download}\n'   # rc0, 200 172391
curl -fsSL https://www.rfc-editor.org/rfc/rfc6585.txt | nl -ba | sed -n '125,170p'                     # rc0
curl -fsSL https://www.rfc-editor.org/rfc/rfc6585 | python3 -c '... strip tags, check sentence ...'    # HTML_TEXT_HAS_QUOTE: True
```

Observed plain-text anchors (immutable RFC serialization):

- `rfc6585.txt:132` `4.  429 Too Many Requests` (section heading)
- `rfc6585.txt:134-135` `The 429 status code indicates that the user has sent too many` / `requests in a given amount of time ("rate limiting").`
- `rfc6585.txt:158-163` `Note that this specification does not define how the origin server identifies the user, nor how it counts requests.`
- `rfc6585.txt:165` `Responses with the 429 status code MUST NOT be stored by a cache.`

The lesson quote at `corpus/lessons/round-17.md:47` is the sentence at :134-135 with the line
wrap joined by one space. Word count (whitespace split, either quote form): **21**, so the
`<=25`-word rule holds. The cited HTML page contains the same sentence with straight ASCII
quotes (`HTML_TEXT_HAS_QUOTE: True`), so the source itself is not the problem — see D1.

## 2. Immutable source, status links

- Datatracker API (`doc/document/rfc6585`): `obsoleted_by: null`, `updated_by: null`,
  `std_level: ps`, `stream: ietf`, `time: 2026-05-20`. The RFC is **not** obsoleted or
  updated; the anchored §4 text is the live definition.
- RFC 9110 does not define 429; it points at 6585 as the extension
  (`rfc9110.txt:8629` `limits have been defined by extensions to HTTP [RFC6585]`,
  reference entry `:9644-9646`). So S041 is still the correct primary for the status
  meaning, and the S042 row does not silently supersede it.
- Errata (`https://www.rfc-editor.org/errata/rfc6585`): exactly one, **erratum 8181**,
  status **Reported** (not Verified), type Technical, "Throughout the document",
  `Updates: 2616` → `Updates: 9110`. It touches the header metadata only; it does **not**
  touch §4 or the quoted sentence. No correction is owed to the row. (The opening receipt's
  metadata note "Updates RFC2616" at `build/SrcRfc6585.md:19` is the disputed header field,
  but the row does not carry that field.)
- `RFC 6585` is an IETF Standards Track RFC, Category "Standards Track", April 2012, DOI
  10.17487/RFC6585. Datatracker's `ps` level is the usual Proposed-Standard form; the row
  writes "Standards Track", not "Internet Standard", so the level is not inflated.

## 3. Field-by-field verdict on `corpus/SOURCES.md:47`

| Field | Row value | Verdict |
|---|---|---|
| id/source | `S041` / `RFC 6585 Additional HTTP Status Codes — https://www.rfc-editor.org/rfc/rfc6585` | **agree.** Next unused id after S040 (`SOURCES.md:46`); canonical RFC Editor URL, resolves 200. |
| kind | `spec` | **agree.** Enumerated kind, primary IETF specification. |
| tier | `A` | **agree.** Contract v1 (`CORPUS.md` §SOURCES, `tier`) makes a spec primary for its scope; scope is exactly the status meaning. |
| scope | `HTTP 429 Too Many Requests status meaning` | **agree, and properly narrow.** It does not claim Retry-After (S042), client behavior, or permanence. |
| anchor | `§4, plain-text lines 132–135; Standards Track, April 2012; opened 2026-10-20` | **agree for content, D4 for representation.** :132 is the heading, :134-135 the quote, publication date matches, date is today. |
| teaches | `HTTP 429 denotes too many requests in a time window; it does not identify a vendor business error or establish permanent seat death.` | **agree.** First clause is :134-135. The negative clauses are supported by the spec's own non-definition (`:158-163`, §7.2 "servers are not required to use 429") and are corroborated by S043, which documents usage/balance causes under HTTP 429. |
| quote (lesson `:47`) | 21 words, location "§4, plain text lines 134–135" | **words agree, bytes disagree — D1.** |
| status | `mined` | **agree under contract v1.** `mined` = "cited by ≥1 path in `used-by`"; the cited note exists and cites S041 at `corpus/knowledge/seat-terminal-status-r17.md:1`. |
| opened / recheck | `2026-10-20` / `365d` | **agree.** Immutable text; 365d is adequate. An open unverified erratum does not change the anchored text. |
| used-by | `corpus/knowledge/seat-terminal-status-r17.md` | **agree, with D3.** Path exists and cites S041. The round lesson also cites it and is not listed; see D3. |

## 4. Does the knowledge entry actually depend on S041?

Observed dependence points:

- `corpus/knowledge/seat-terminal-status-r17.md:21` decision row: "older error, type 1302 or
  rate-limit/429 token → `dead_rate_limit`".
- `tools/mori-seat-terminal.py:269` `if view["error_status"] == 429 or any(token in error_message for token in RATE_TOKENS): return "dead_rate_limit"` — the status-only branch exists and is reachable when no quota token/code is present.
- `corpus/knowledge/seat-terminal-status-r17.md:26-28` states the dependence exactly:
  "S043 is operational, not decorative ... RFC 6585 grounds the generic status meaning, not
  the vendor business cause or OMP recovery."

Verdict: **not decorative at the definitional level, and not evidence of any observation.**
The proposition "429 means rate limiting" is exactly what the row teaches, it is the only
source in the registry for that status meaning (S043 maps *vendor codes* onto 429 and
presupposes the status meaning), and the entry's decision table plus the tool's status branch
use it. The wave-1 "decorative" verdict (`build/CriticFrontier.md:123-128`) was aimed at the
earlier draft sentence "The tool is unaffected" (`build/KnowledgeSeatTerminal.md:67`); the
admitted entry replaced that with the narrower, accurate sentence above, so the charge no
longer lands as stated. What remains true from that critique: S041 supplies **no** evidence
that any OMP seat emitted 429, and no branch's *code* would change if the row were rejected —
the dependence is semantic grounding, not a behavioural delta. It should not be described as
more than that.

Consequence for L1: C1's `2b.4` "at least one sourced claim" does **not** hinge on S041.
S043 is operational — `tools/mori-seat-terminal.py:87-88` (`QUOTA_CODES = frozenset(("1113","1308"))`,
`RATE_CODES = frozenset(("1302",))`) and the code/quota-before-token order at `:263-269` implement A1.10
from S043. So even a rejection of S041 would leave C1 sourced.

## 5. Defects found

**D1 (reference-drift, transcription; low).** The lesson's "verbatim" quote contains two
backslash-escaped double quotes that are not in the source:
`corpus/lessons/round-17.md:47` bytes are `time (\"rate limiting\")`; `rfc6585.txt:135` has
`time ("rate limiting")`. Falsifier executed:

```
grep -cF 'time (\"rate limiting\")'  rfc6585.txt   -> 0
grep -cF 'time ("rate limiting")'    rfc6585.txt   -> 1
```

Consequence: a verifier who `grep -F`s the committed quote fails against the source. Words,
order and meaning are exact, so the teaching is unaffected; the "copied verbatim" claim in the
lesson's own column header (`corpus/lessons/round-17.md:45`) is false as bytes. Same class in
sibling rows `:48` (S042) and `:50` (S044) — noted for L1, not claimed as my scope.
Fix: delete the two backslashes (markdown renders `"` in a table without escaping).

**D2 (provenance/freshness; low).** The consumer's `recheck:` line does not exercise S041 at
all: `corpus/knowledge/seat-terminal-status-r17.md:3` runs only the tool selftest and the
fixture gate. A wrong or withdrawn quote/URL would not be caught by the declared recheck.
Lane precedent for an external source is an executable source grep, e.g.
`corpus/knowledge/journal-cursor-window-r16.md:3` (`curl … | grep -oF '<quote>'`). The row's
own `365d` cadence implies re-opening the source, but no command in the entry does so.
Fix (one line, no registry edit): append
`curl -fsSL https://www.rfc-editor.org/rfc/rfc6585.txt | grep -cF 'The 429 status code indicates that the user has sent too many'`.

**D3 (used-by completeness; informational).** Contract v1 defines `used-by` as "knowledge
entries **or lessons** citing the row", and `corpus/lessons/round-17.md:47,56` cites S041, yet
only the knowledge path is listed. Status `mined` is unaffected (≥1 path) and the omission
matches the recent-row convention (S035–S040 list knowledge files only; S001 does list a
lesson). No change recommended unless L1 wants the strict reading.

**D4 (anchor representation; informational).** The registry anchor is expressed in
`rfc6585.txt` line numbers while `source` points at the HTML rendering, which exposes no line
numbers. The anchor is still exact and immutable (the .txt is the RFC's canonical artifact),
but a reader following only the row's URL cannot confirm 132–135. Suggest (not performed) the
parenthetical `(rfc6585.txt)`. Also note the registry anchor spans 132–135 while the lesson
gate says 134–135; both are true — the heading plus the sentence — and not a contradiction.

## 6. Attacked and found sound (no blanket pass)

- URL resolution and content: 200, 172391 bytes, quote present in both HTML and .txt.
- Quote location: exactly `rfc6585.txt:134-135`; 21 words; ASCII quotes; line wrap correctly joined.
- Section number and title (`4. 429 Too Many Requests`; TOC entry at `rfc6585.txt:68`, heading at `:132`; §7.2 security subsection at `:294`).
- Immutability: no obsoletion, no update, no verified erratum touching §4.
- Tier A / kind `spec` / scope narrowness / status `mined` / used-by path existence.
- `teaches` does not overclaim identity, counting, or permanence.

## 7. Remaining unknowns

- [UNKNOWN] Whether an independent non-author verifier has re-opened this URL outside an
  L1-dispatched seat. This seat is wave-2 fresh and non-author to the row, but it is still
  L1-dispatched; it is not outside closure by itself.
- [UNKNOWN] Whether the lane's census or any gate rejects escape-mangled quotes; no such
  check was observed in the frozen v1 census commands (`CORPUS.md` §SOURCES, Census block).
- [UNKNOWN] Whether erratum 8181 will ever be verified. It would change only the `Updates:`
  header, not §4, so the row would remain correct either way.

## 8. Procedure / tooling

- No install or update performed; existing `curl`, `grep`, `python3`, `nl` only.
- No VCS mutation, no background job, no journal query, no credential/transcript read.
- One transient file `.ufo/waves/round-17/.rfc6585.check.txt` was created for the two
  `grep -F` counts and deleted in the same command; no artifact retained. Disclosed because
  the seat rules discourage scratch writes even outside `/tmp`.
- Only this report was written; no source-registry or knowledge edit.
