# SrcZaiErrorCodes — round 17 S043 (Z.AI business error code 1302 / HTTP 429)

Seat: MoriR17.SrcZaiErrorCodes-5. Lane: /home/vgpnk/Projects/shokunin/mori-shokunin (entering tip 24526ea). Access date: 2026-10-20.
Installs/updates: none. Tools used: `read` (Mintlify markdown alternate), `curl` (stdout only, no file written), no writes outside this report.

## Outcome

Found, opened, and reachable. Code 1302 is present and mapped to HTTP 429. S043 is drafted as an accepted row (not rejected).

## Evidence observed

- Source page: https://docs.z.ai/api-reference/api-code (rendered); markdown alternate https://docs.z.ai/api-reference/api-code.md.
- `curl -sS -L -o /dev/null -w 'status=%{http_code}'` on the .md URL → `status=200`, 5208 bytes, no redirect (final URL equal to request). Command exit 0.
- `curl -sS -L <md> | grep -n '1302\|1113\|1308\|^# \|Rate limit'` (exit 0) on the markdown alternate:
  - line 5: `# Errors`
  - line 16: `| 1113 | 429 | Insufficient balance or no resource package. Please recharge. |`
  - line 31: `| 1302 | 429 | Rate limit reached for requests |`
  - line 33: `| 1308 | 429 | Usage limit reached for ... |`
- The markdown body is 82 lines (`grep -c ''`).
- Error Shapes section: errors are JSON with a top-level `error` object containing `code` (string) and `message`; the example uses `"code":"1214"`.
- Page note: for SSE streams, abnormal termination is reported via `finish_reason` rather than these codes.

## Gate verbatim quote (<=25 words)

Quote: "Rate limit reached for requests" (cell text for code 1302, HTTP status 429; api-code.md line 31; accessed 2026-10-20). 5 words.

## SOURCES row draft (column format of corpus/SOURCES.md)

| S043 | Z.AI API error codes — https://docs.z.ai/api-reference/api-code (markdown alternate https://docs.z.ai/api-reference/api-code.md) | docs | A | Z.AI business error codes in the response body, with HTTP status mapping for 1302 (rate limit) and 1113 / 1308 (usage and balance) | Errors table: api-code.md:16 (1113, HTTP 429), api-code.md:31 (1302, HTTP 429), api-code.md:33 (1308, HTTP 429); Error Shapes section; Mintlify page served HTTP 200, accessed 2026-10-20 | Z.AI code 1302 is returned with HTTP 429 and the message "Rate limit reached for requests"; a 429 HTTP status alone does not identify the business cause, since 1113 and 1308 also use 429. | mined | 2026-10-20 | on-release | pending: C1 knowledge entry corpus/knowledge/seat-terminal-status-r17.md (not drafted by this seat) |

Gate line: S043 gate — verbatim quote "Rate limit reached for requests" (1302 | HTTP 429), api-code.md:31, accessed 2026-10-20, <=25 words, matches the page text observed in both the rendered page and the markdown alternate.

## Scope limits and [INFERENCE]

- The doc maps the business code to HTTP status and message. It does not document the `(type=NNNN)` token form that the C1 parser (`error_code` in contract.md) reads from seat transcripts. Linking a transcript `(type=1302)` to this table is [INFERENCE], not observed here. No transcript was read by this seat (the seat-transcript read rule was respected).
- The docs do not state retry behavior, retry-after semantics, or whether 1302 is transient. Those are not claimed in S043.
- 1113 (insufficient balance) and 1308/1310/1316-1321 (usage or quota) are also HTTP 429 in this table. C1's `dead_rate_limit` vs `dead_quota` split (contract.md: rate-limit test before quota) cannot be decided from HTTP 429 alone; the business code is the discriminator if it is present. [INFERENCE] for the classifier design; not a claim about any transcript.
- Rendered page and markdown alternate were both sourced from the same Mintlify deployment; the page text observed is identical for the cited lines (line numbers refer to the .md alternate as fetched on 2026-10-20).
- Lines in this table are a snapshot; `on-release` recheck applies.

## Out of scope / not done

- No S041, S042, S044-S048 rows drafted (other seats).
- No corpus file, SOURCES.md, or knowledge entry was written; the row is a draft for the integration owner (MoriR17) to append.
- No selftest or gate run (not assigned to this seat).

## Verdict

S043 accepted as drafted: 1302 is present in the official Z.AI table and mapped to HTTP 429 with the quoted message.
