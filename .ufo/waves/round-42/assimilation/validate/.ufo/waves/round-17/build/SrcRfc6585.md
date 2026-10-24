# SrcRfc6585 — S041 draft (RFC 6585 §4, 429 Too Many Requests)

Scope: draft one SOURCES row and one Gate line. SOURCES.md was NOT edited (draft only, lane write scope).

## Draft row (exact column order of corpus/SOURCES.md)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S041 (provisional) | RFC 6585, Additional HTTP Status Codes — https://www.rfc-editor.org/rfc/rfc6585 | spec | A | HTTP 429 Too Many Requests semantics (rate limiting), section 4 | §4 "4. 429 Too Many Requests" (plain text lines 132-135, 165; RFC Standards Track, April 2012) | A 429 response signals that the user sent too many requests in a time window; the origin chooses what counts and who is counted, responses SHOULD explain and MAY carry Retry-After, and 429 responses MUST NOT be stored by a cache. | queued | 2026-10-20 | 365d | — |

## Gate

- URL: https://www.rfc-editor.org/rfc/rfc6585 (plain text: https://www.rfc-editor.org/rfc/rfc6585.txt)
- Access date: 2026-10-20 (UTC)
- Located quote (section 4, verbatim, 21 words; the RFC's line wrap is joined with one space):
  > The 429 status code indicates that the user has sent too many requests in a given amount of time ("rate limiting").

## Verification trail

- `curl -sSfL https://www.rfc-editor.org/rfc/rfc6585.txt` → rc=0; `grep -n` located "4.  429 Too Many Requests" at line 132, the quoted sentence at lines 134-135, and "Responses with the 429 status code MUST NOT be stored by a cache." at line 165. `sed -n '132,136p;165,166p'` with `cat -A` confirmed the quoted text and its wrap.
- The rendered reader page (rfc-editor.org/rfc/rfc6585) gave the same section 4 text; its metadata reports Standards Track, Published April 2012, Updates RFC2616.
- Also in section 4 (not used in the row's quote): "The response representations SHOULD include details explaining the condition, and MAY include a Retry-After header" (plain text lines 137-138).

## Notes

- Tier A: IETF Standards Track, primary source.
- Scope limit for mori: section 4 does not define how a server identifies users or counts requests (verbatim: "this specification does not define how the origin server identifies the user, nor how it counts requests"). The row's teaches column must not claim a counting rule.
- Section 7.2 adds that servers are not required to use 429 under attack; a consumer should not read 429 as a universal response behavior.
- Row kept as `queued`: no lesson mines S041 yet; used-by is `—`.

## Tooling

- No install or update performed. Used the existing `curl` binary (no version change) and the existing `read` tool.
- No writes outside this report file. No VCS commands. No /tmp use.
