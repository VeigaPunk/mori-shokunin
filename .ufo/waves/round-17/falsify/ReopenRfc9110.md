# S042 — RFC 9110 §10.2.3 fresh read-only reopen

## Scope and verdict

Attacked scope: source row S042 in `corpus/SOURCES.md:48` (immutable source/scope/anchor/
teaches/tier, status, used-by) and the ≤25-word quote in the round-17 Gate table
(`corpus/lessons/round-17.md:48`), checked against the live RFC Editor page opened
2026-10-20. This is a source/quote witness, not an admission decision.

Verdict: **agree** with all five immutable cells, with `queued`/`—`, and with the factual
content of the quote. One located defect: the committed lesson quote carries two literal
U+005C backslash bytes before the inner double quotes (`\"Retry-After\"`), which the RFC text
and the seat's own receipt (`build/SrcRfc9110.md:31`) do not contain. After removing exactly
those two bytes the lesson quote is identical to the receipt quote and to the RFC text; word
count is 21 in every version. The defect is a rendering/serialization artifact in the lesson
table, not a misquotation, and it is shared by sibling rows S041 and S044. No source registry
edit was made.

## Source access and located quote

- URL: https://www.rfc-editor.org/rfc/rfc9110#section-10.2.3
- Accessed: 2026-10-20 (system clock `2026-10-20T16:49:07-03:00`), read-only.
- Located quote, plain text of the page:

  “Servers send the "Retry-After" header field to indicate how long the user agent ought to
  wait before making a follow-up request.”

  Plain-text rendering lines 4825–4826; §10.2.3 heading at line 4823; the 503/3xx context
  follows at 4827–4831, the value grammar (`Retry-After = HTTP-date / delay-seconds`) at 4836,
  `delay-seconds = 1*DIGIT` at 4841.

- Verification, both RFC Editor renderings, in-memory (`curl … | python3 -c`, no files written):

  - HTML (`rfc9110.html`), section 10.2.3 extracted and text-normalized:
    `QUOTE_IN_HTML True`, `QUOTE_WORDS 21`.
  - Plain text (`rfc9110.txt`), section sliced from the body occurrence to `10.2.4.`:
    `QUOTE_IN_TXT True`, `QUOTE_WORDS 21`, normalized section SHA-256
    `5c808da916edb56362b9fc4936e500cd0c3e8ef8b02f1109cb0c9f7feed61589` (854 chars).
  - Anchor: `id="section-10.2.3"` exists in the HTML, plus sub-ids `-1` … `-8`; the cited
    fragment therefore resolves.
  - Quote SHA-256 (plain form, from the seat receipt): `f03abb7d983c4b33a1975d49589cd605a35dc812afc4c28ae978129646a777e1`.

- Errata/freshness: https://www.rfc-editor.org/errata/rfc9110 lists 6 verified, 2 reported and
  6 rejected errata. A full-text grep of the rendered page for `10.2.3` and `Retry-After`
  returned no matches, so no erratum changes this section or the quote.
- Publication metadata: June 2022, Category Standards Track, STD 97; the info page
  (https://www.rfc-editor.org/info/rfc9110) renders the current status as “Internet Standard”.

## Immutable cells

| Cell | Observed against the page | Verdict |
|---|---|---|
| `source` | RFC 9110 title is “HTTP Semantics”; the URL resolves and the `#section-10.2.3` fragment is a real HTML id. | Agree. |
| `scope` | “Retry-After response-header semantics” matches §10.2.3: wait-hint semantics for 503 and 3xx, plus HTTP-date/delay-seconds grammar. The cell is a summary, not an exhaustive transcription. | Agree. |
| `anchor` | `10.2.3.  Retry-After`; June 2022; opened 2026-10-20. “Standards Track” is the document's own Category line (and the S041 convention); the current maturity label on the info page is “Internet Standard” (STD 97), which the anchor does not state. | Agree; maturity-label omission is precision, not falsity. |
| `teaches` | “Retry-After indicates how long a user agent ought to wait before a follow-up request; this section is not proof of a client retry implementation.” The first clause paraphrases the located quote; the second is true of §10.2.3, which defines no client retry behavior. | Agree. |
| `tier` | Primary IETF standards-track/Internet Standard reference; same tier assigned to S041 (RFC 6585) under the registry's convention. | Agree. |

Cross-source boundary noted, not a defect in this row: RFC 6585 §4 (S041, same registry)
states that a 429 response “MAY include a Retry-After header”. RFC 9110 §10.2.3 never mentions
429, so its silence must not be read as exclusivity. The S042 cells avoid the “only 503/3xx”
phrasing; the seat report's teaching sentence “defines Retry-After only for 503 and 3xx”
(`build/SrcRfc9110.md:51`) is where that overread could re-enter if copied forward.
[INFERENCE] That sentence is true of RFC 9110 alone but incomplete about HTTP; S042's
immutable cells do not inherit it.

## Quote defect (located)

The pinned measured commit is `273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7`; the observed branch
tip is `5c1dfb8d0530c74eb0e1630c2b522b735b486274`. The S042 row and the lesson line 48 bytes
are identical at both revisions (`od -c` at each); the only lesson/SOURCES diff between them
is 64 added lesson lines elsewhere. Raw bytes of the committed lesson quote (`od -c`, measured commit):

```text
... : 342 200 234   S e r v e r s   s e n d   t h e   \
" R e t r y - A f t e r \ "   h e a d e r   f i e l d ...
```

A Python comparison of the committed line against `build/SrcRfc9110.md:31` (measured commit):

```text
lesson_quote_repr:   'Servers send the \\"Retry-After\\" header field to indicate how long the user agent ought to wait before making a follow-up request.'
receipt_quote_repr:  'Servers send the "Retry-After" header field to indicate how long the user agent ought to wait before making a follow-up request.'
words_lesson 21 words_receipt 21
equal_after_strip_backslash: True
backslash_count_lesson_quote 2
spurious_backslash_positions [17, 30]
lesson_quote_sha256 d30cbe37ddb6490ffec840162545e152c3ebf419e9f65f59d0931d94cbd46974
receipt_quote_sha256 f03abb7d983c4b33a1975d49589cd605a35dc812afc4c28ae978129646a777e1
```

So the committed Gate quote is not byte-verbatim: two U+005C characters that are absent from
the RFC text and from the seat receipt were introduced at integration. The words, punctuation
and the ≤25 limit are unaffected, and Markdown renders `\"` back to `"`. The same artifact
affects `corpus/lessons/round-17.md:47` (S041) and `:50` (S044); rounds 12–14 Gate quotes
contain no such escapes. The source receipt and the SOURCES.md row itself are clean.

Minor receipt imprecision: `build/SrcRfc9110.md:12` says the heading is at reader line 4825;
in the same rendering the heading is at 4823 and the quote starts at 4825. The in-section
references (4827–4831, 4836, ~4842) match. The integrated anchor omits line numbers, so this
does not reach SOURCES.md.

## used-by / status dependency

- `corpus/SOURCES.md:48` records `queued` and `used-by —`.
- `corpus/knowledge/seat-terminal-status-r17.md` cites S041 and S043 only (its `source:`
  header and body); S042 appears nowhere under `corpus/knowledge/` and nowhere in `tools/`
  (case-insensitive grep for `Retry-After|retry_after|retry.after` returned no matches). The
  C1 tool cannot observe a header: its fields are status/code/retry counters, and the
  knowledge entry explicitly classes results as terminal observations, not incidents.
- The round-17 lesson's own prose assigns causation only to S043 and S046 (“These are sourced
  claims, not decorative citations”, `corpus/lessons/round-17.md:59-60`); S042 is listed as
  entering `queued`.
- Convention precedent: S008, S017 and S033 each have a round-12 Gate row
  (`corpus/lessons/round-12.md:134,143,159`) yet remain `queued`/`—` in `corpus/SOURCES.md`.
  A Gate-table listing is a source-opening receipt, not `used-by`.
- Count consistency: `evidence/source-count.json` reproduces mined 19→25 (+6: S041, S043,
  S044, S045, S046, S047) and queued 20→22 (+2: S042, S048).

Verdict: S042 is honestly queued and unused; no knowledge entry depends on it, so it is not
decorative support. Any future use is limited to “Retry-After is a wait hint”; it cannot
support “the client ignored/was sent Retry-After”, because no cited field set includes the
header, and RFC 6585 §4 (not RFC 9110) is the row that even permits the header on 429.

## Limits, blockers, changes

- One page access per rendering (HTML and plain text) plus the errata and info pages; no
  IETF datatracker comparison. No byte digest of the full page; the normalized section digest
  above is recorded instead.
- No gate, selftest, build or lint was run; no live probe was repeated. No tool install or
  update occurred. No source registry, knowledge note, tool or sibling file was edited; the
  only write is this report.
- No blocker: the assigned question is answered. The escaped-quote defect is reported, not
  repaired, per the no-registry-edit bound and the integration-owner rule.
