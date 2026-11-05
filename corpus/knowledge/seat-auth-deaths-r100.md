# Seat deaths on credential or entitlement refusal (dead_auth)

source: S637 — https://connectrpc.com/docs/protocol/ — spec, tier A, Connect protocol reference (Error Codes table, the code-choice rule, HTTP-to-Connect code mapping), committed copy `corpus/evidence/sources-r100/S637-connect-protocol.html`, opened 2026-11-05
source: S638 — https://grpc.github.io/grpc/core/md_doc_statuscodes.html — spec, tier A, gRPC status codes (PERMISSION_DENIED, UNAUTHENTICATED, RESOURCE_EXHAUSTED), committed copy `corpus/evidence/sources-r100/S638-grpc-statuscodes.html`, opened 2026-11-05
source: S639 — https://www.rfc-editor.org/rfc/rfc9110.txt — spec, tier A, RFC 9110 §15.5.2 401 Unauthorized and §15.5.4 403 Forbidden (S221 holds the same URL scoped to §15.4), opened 2026-11-05, committed copy `corpus/evidence/sources-r100/S221-rfc9110-r100.txt`
verified-at: 2026-11-05
recheck: 180d — `python3 tools/mori-seat-terminal.py --selftest` (cases `auth-*`); re-open S637/S638 and diff the code tables when a provider in the fleet changes transport
coverage-map: kill and death events — seat terminal status (round 17), the auth/entitlement class, round 100

The seat terminal census (`tools/mori-seat-terminal.py`, round 17) sorted a seat whose last record is an aged
assistant error into `dead_quota`, `dead_rate_limit` or `dead_error_other`. On 2026-11-04/05 the fleet's
provider failures were mostly refusals of a credential or of an entitlement: `401 Invalid 'Authorization' header`
(commandcode), `403 ... permission_error ... subscription does not have access`, and Devin's
`stream error permission_denied: This model is no longer available for your account`. None carries a quota or
rate token, so the census put them in `dead_error_other`, next to real unknowns. In the fleet's own transcripts of
the two days before the round, 187 of the 190 terminal errors the round-99 rules would call `dead_error_other`
carry a 401/403 status or an auth code spelling (`.ufo/waves/round-100/evidence/live-errors-prefreeze.txt`,
counts only). An auth refusal does not clear by waiting, unlike a rate limit, and a quota refusal clears at a
reset; the operator needs the three apart to decide between re-login, re-routing and waiting.

## Claims

| claim | source | quote |
|---|---|---|
| HTTP 401 means the request lacks valid authentication credentials for the resource. | S639 | `the request has not been applied because it lacks valid authentication credentials for the target resource.` (rfc9110.txt:7550-7552, §15.5.2) |
| HTTP 403 means the server understood the request but refuses to fulfill it. | S639 | `the request but refuses to fulfill it.` (rfc9110.txt:7572, §15.5.4) |
| HTTP 402 is only reserved; a provider's 402 "insufficient balance" meaning is its own, which is why the tool reads `402` as quota text, not as a status class. | S639 | `The 402 (Payment Required) status code is reserved for future use.` (rfc9110.txt:7567) |
| Connect error codes are lowercase snake spellings; `permission_denied` and `unauthenticated` are auth codes, and a per-user quota is `resource_exhausted`, not an auth code. | S637 | `use unauthenticated if the user can’t be identified or presents invalid credentials. Use resource_exhausted if a per-user quota` (raw lines 646-647) |
| A Connect client infers `unauthenticated` from HTTP 401 and `permission_denied` from HTTP 403. | S637 | `401 Unauthorized unauthenticated 403 Forbidden permission_denied` (raw line 711, tags stripped) |
| gRPC forbids PERMISSION_DENIED for resource exhaustion, so explicit quota evidence must win over an auth spelling. | S638 | `PERMISSION_DENIED must not be used for rejections caused by exhausting some resource` (raw line 88) |
| gRPC UNAUTHENTICATED means the request has no valid authentication credentials. | S638 | `The request does not have valid authentication credentials for the operation.` (raw line 106) |

## Rule (as landed)

1. Z.AI business codes keep their round-17 meaning (`1113`/`1308` quota, `1302` rate) when the provider is `zai`.
2. Quota evidence (`quota`, `Quota`, `QUOTA`, `usage limit`, `402`, `credits`) → `dead_quota`. The two capitalised
   spellings were added after the landing measurement: without them `403 Quota exceeded for project …` and
   `403 QUOTA_EXCEEDED` became `dead_auth` (`.ufo/waves/round-100/w1/Mo100CritC1.md` H03/H04).
3. Rate evidence (HTTP 429 or a rate spelling) → `dead_rate_limit`.
4. Auth evidence → `dead_auth`: HTTP 401 or 403, or one of the spellings `permission_denied`,
   `PERMISSION_DENIED`, `unauthenticated`, `UNAUTHENTICATED`, `authentication_error`, `permission_error`.
5. Anything else → `dead_error_other`.

Steps 2–3 come first because some providers answer quota exhaustion with 403 and gRPC reserves exhaustion for
RESOURCE_EXHAUSTED (S638). So `dead_auth` only ever takes seats the round-99 rules put in `dead_error_other`;
no seat moves between the other classes.

## Limits

- The class says the provider refused a credential or an entitlement. It does not say which credential, account
  or model, and it is not proof the route is dead for other seats; the transcript text is never emitted.
- Spellings outside the list are not read: CamelCase identifiers such as `PermissionDenied` / `Unauthenticated`
  (the Go constant names of the same codes) and a bare `401 Unauthorized` text without an `errorStatus` stay
  `dead_error_other`.
- The plain words `permission denied` (with a space) are not auth evidence: a file-system error says the same.
- The numeric quota and rate spellings (`402`, `429`) match as substrings, a round-17 rule this round keeps: a
  request id or trace number holding `429` turns an auth death into `dead_rate_limit` (found by the round-100
  counter's own random tails, `.ufo/waves/round-100/w1/Mo100ExecReplay.md`; routed to the next round).
- Devin's `failed_precondition: Your weekly usage quota has been exhausted` is a quota death by its text, not auth.
- The output schema name stays `mori-seat-terminal-v1`; the class list and `totals` keys gain `dead_auth`, so a
  consumer that checks the exact key set (the round-17 fixture gate did) must add it.

## Boundaries

Detection and report only. Re-login, key rotation and routing are the operator's (harness configuration); mori
names the class and the count.
