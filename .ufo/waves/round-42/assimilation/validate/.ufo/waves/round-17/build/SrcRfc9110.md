# SrcRfc9110: RFC 9110 §10.2.3 Retry-After (S042 draft)

Seat: `MoriR17.SrcRfc9110-5` (scribe, leaf, no subagent dispatch). Access date: 2026-10-20.
Tools: no installs or updates. Network: one read of the RFC Editor page. No pacman, journal,
or VCS write. No lane file edited; this report is the only write.

## Source access

- URL: https://www.rfc-editor.org/rfc/rfc9110#section-10.2.3
- Accessed: 2026-10-20 via the `read` tool (reader rendering of the full RFC 9110 text,
  June 2022, Standards Track, STD 97, Obsoletes 7230/7231/7232/7233/7235). The section
  appears at reader lines 4799-4853 (heading `10.2.3. Retry-After` at line 4825 of the
  rendered text). No SHA-256 was computed for the page.
- Located quote (21 words, ≤25), verbatim from §10.2.3:
  “Servers send the "Retry-After" header field to indicate how long the user agent ought to wait before making a follow-up request.”

## Draft SOURCES row (S042, provisional; column format of `corpus/SOURCES.md`)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S042 | RFC 9110 HTTP Semantics, §10.2.3 Retry-After — https://www.rfc-editor.org/rfc/rfc9110#section-10.2.3 | spec | A | Retry-After response-header semantics: server hint on how long a client ought to wait before a follow-up request | §10.2.3 Retry-After (reader lines 4825-4843); RFC 9110 June 2022, Standards Track; opened 2026-10-20 | Retry-After is a server wait hint given as HTTP-date or delay-seconds; §10.2.3 names 503 and 3xx as its contexts and does not define its use with 429. | queued | 2026-10-20 | 365d | — |

Column note: `recheck` 365d is proposed because RFC 9110 is a published standard; the row
is not expected to change unless an erratum or successor RFC lands. Errata index at
https://www.rfc-editor.org/errata/rfc9110 (listed in the reader metadata; not opened).

## Gate line (for the lesson `## Gate` table)

| row | URL | accessed | located quote (≤25 words) | location |
|---|---|---|---|---|
| S042 | https://www.rfc-editor.org/rfc/rfc9110#section-10.2.3 | 2026-10-20 | “Servers send the "Retry-After" header field to indicate how long the user agent ought to wait before making a follow-up request.” | §10.2.3 Retry-After |

## Observed facts supporting the row (from the same opened text)

- §10.2.3 scope: "When sent with a 503 (Service Unavailable) response, Retry-After indicates
  how long the service is expected to be unavailable to the client. When sent with any 3xx
  (Redirection) response, Retry-After indicates the minimum time..." (reader lines 4827-4831).
- Value grammar: `Retry-After = HTTP-date / delay-seconds` (line 4836); `delay-seconds = 1*DIGIT`
  (line ~4842); "A delay-seconds value is a non-negative decimal integer, representing time in seconds."
- Keyword rule, §2.2 (reader lines 571-575): the key words "MUST", "SHOULD", "MAY", etc. are
  interpreted as BCP 14 "when, and only when, they appear in all capitals". §10.2.3 uses
  lowercase "ought to wait", so that sentence is not a BCP 14 requirement.
- Search of the full opened text for `429`, `Too Many Requests`, `ought`, `normative`:
  zero hits for 429 or "Too Many Requests" in RFC 9110. The 429 status is defined by RFC 6585
  (candidate S041, not opened in this seat).

## Teaching: is a 429 seat death without honoring Retry-After consistent with RFC 9110?

Teaching, not judgment. [INFERENCE] from the observed text:

1. No requirement is breached. RFC 9110 defines Retry-After only for 503 and 3xx in §10.2.3,
   says nothing about 429, and its only deontic phrase is lowercase "ought to", outside §2.2's
   BCP 14 scope. A server that omits Retry-After on a 429 does not violate §10.2.3, and a client
   that ignores it does not violate a MUST.
2. The RFC defines no client give-up behavior. Retry budgets ("Retry budget exhausted after 10
   retries") and the terminal state of a seat are outside RFC 9110; the RFC neither requires
   retrying nor forbids abandoning.
3. The header's stated purpose is a wait hint: it tells the user agent how long to wait before
   a follow-up request. A client that issues follow-up requests immediately, without honoring a
   delay it received, acts against that stated purpose even though the RFC does not enforce it.
   Whether a given 429 carried Retry-After at all is not observable from the transcript field
   set fixed by `contract.md` (`error_status`, `error_code`, `retries`, `retry_exhausted`);
   the classifier cannot tell "ignored" from "absent". Teaching point for C1: a
   `dead_rate_limit` class records the terminal state, not the header's presence or the client's
   honoring of it.
4. The `(type=1302)` provider code and the "Retry budget exhausted" wording are provider- and
   client-specific; RFC 9110 does not define them. Mapping them to RFC semantics would be an
   extension, not a citation. The Z.AI row (S043) is the place for that claim, not this row.

Conclusion for the row: the RFC is consistent with a 429 seat death whether or not Retry-After
was honored, because it imposes no MUST on that path; the RFC's advisory wait semantics argue
against ignoring a received Retry-After, and this cannot be checked from the seat transcript
fields.

## Limits

- Opened once via the reader rendering; not compared with the IETF datatracker text or the
  errata page (not opened). No byte-level digest; the lane's current convention (round 13-16
  gates) records URL, access date and quote only.
- S042 status is `queued`: no knowledge entry cites it yet. Its `used-by` is empty until a
  lesson or knowledge entry does so.
- Row S041 (RFC 6585 §4, 429) and S043 (Z.AI error codes) are other seats' drafts; the numbers
  are provisional and this seat did not verify them.

## Commands run

- `read https://www.rfc-editor.org/rfc/rfc9110#section-10.2.3` → exit success (reader rendering).
- `grep` on the opened text for `Retry-After`, `429`, `Too Many Requests`, `ought`, `Requirements Notation`
  → used only to locate lines above; no file writes.
- No shell, no network beyond the single read, no journal query, no VCS command.
