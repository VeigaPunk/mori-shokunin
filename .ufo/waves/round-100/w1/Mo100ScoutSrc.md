# Mo100ScoutSrc — round 100 attempt 1, wave w1 — C1 cited-source re-open

Seat: Mo100ScoutSrc (role scout). Scope: re-open S637, S638, S221 cited by C1; check SOURCES.md rows S637/S638
and each claim row of `corpus/knowledge/seat-auth-deaths-r100.md`. Read-only. No edits to lane files.
Live fetches run 2026-11-05 (UTC) from the cwd `/home/vgpnk/Projects/shokunin`, outputs in a scratch dir that is removed.

## 1. Live re-open versus pinned copies

| id | URL | UTC access | HTTP | bytes live / pinned | sha256 live | sha256 pinned | live == pinned |
|---|---|---|---|---|---|---|---|
| S637 | https://connectrpc.com/docs/protocol/ | 2026-11-05T23:22:21Z | 200 | 148033 / 148033 | 55d644c62a7d094ec836dbc4f9fbcb1f5b0cca27b675ba68902568fef9ca2578 | 55d644c62a7d094ec836dbc4f9fbcb1f5b0cca27b675ba68902568fef9ca2578 | yes |
| S638 | https://grpc.github.io/grpc/core/md_doc_statuscodes.html | 2026-11-05T23:22:21Z | 200 | 18133 / 18133 | 95459b760813d4cde87ad3c449753ff55bbd138cdf6c5bfdfacf6566b763e3c4 | 95459b760813d4cde87ad3c449753ff55bbd138cdf6c5bfdfacf6566b763e3c4 | yes |
| S221 | https://www.rfc-editor.org/rfc/rfc9110.txt | 2026-11-05T23:22:21Z | 200 | 502941 / 502941 | 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a | 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a | yes |

SOURCES.md rows record the same hashes for S637 (fetched 2026-11-05T23:00:13Z) and S638 (same time), matching live bytes.
Pinned line counts: S637 787 lines, S638 177 lines, S221 10785 lines.

## 2. Quote checks (tags stripped for HTML; whitespace word count)

| row / claim | source line | quote located | words | <=25 | source supports claim |
|---|---|---|---|---|---|
| S221 — 401 means lacks valid credentials for the resource | rfc9110.txt:7551 (§15.5.2 heading at 7548) | yes, verbatim in raw line | 9 | yes | yes |
| S221 — 403 means server understood request but refuses | rfc9110.txt:7572 (§15.5.4 heading at 7569) | yes, verbatim in raw line | 7 | yes | yes |
| S637 — code-choice rule (unauthenticated / resource_exhausted) | raw 646–647 (span crosses the line break) | yes, after tag strip | 18 (knowledge entry quote); SOURCES row quote 12 | yes | yes |
| S637 — HTTP 401→unauthenticated, 403→permission_denied | raw 711 (table "HTTP Status / Inferred Code") | yes, after tag strip | 6 | yes | yes |
| S638 — PERMISSION_DENIED must not be used for exhaustion | raw 88 | yes, verbatim in raw line after tag strip | 12 | yes | yes |
| S638 — UNAUTHENTICATED means no valid credentials | raw 106 | yes, verbatim in raw line | 11 | yes | yes |

Receipts (script output, trimmed):
```
S637 645: ' When choosing between unauthenticated , permission_denied , resource_exhausted , and'
S637 646: ' not_found , use unauthenticated if the user can’t be identified or presents'
S637 647: 'invalid credentials. Use resource_exhausted if a per-user quota (for example, a'
S637 711: ' ... 401 Unauthorized unauthenticated 403 Forbidden permission_denied 404 Not Found unimplemented ...'
S638 88:  ' PERMISSION_DENIED 7 The caller does not have permission to execute the specified operation. PERMISSION_DENIED must not be used for rejections caused by exhausting some resource (use RESOURCE_EXHAUSTED instead for those errors). ...'
S638 106: ' UNAUTHENTICATED 16 The request does not have valid authentication credentials for the operation. '
S221 7548: 15.5.2.  401 Unauthorized     S221 7569: 15.5.4.  403 Forbidden
```

Notes on the claim sentences:
- "Connect error codes are lowercase snake spellings ... a per-user quota is resource_exhausted, not an auth code": supported by the S637 code-choice paragraph (lines 645–650) and by the lowercase code names in the Error Codes table.
- "gRPC forbids PERMISSION_DENIED for resource exhaustion, so explicit quota evidence must win over an auth spelling": the first clause is the S638 text; "must win" is the design consequence, not a source statement (inference, labelled as such in the entry's rule section).

## 3. CamelCase spelling check (`PermissionDenied` / `Unauthenticated`)

Fetched live 2026-11-05 (UTC 23:28): pkg.go.dev/google.golang.org/grpc/codes (HTTP 200, 63005 bytes),
pkg.go.dev/connectrpc.com/connect (HTTP 200, 380920 bytes), pkg.go.dev/google.golang.org/grpc/status (HTTP 200, 61957 bytes).
- grpc/codes documents the Go identifiers `PermissionDenied = 7` and `Unauthenticated = 16` (doc comments use the same CamelCase names).
- connectrpc.com/connect documents `CodePermissionDenied Code = 7` and `CodeUnauthenticated Code = 16`.
- The printed form `code = PermissionDenied` (the entry's example in Limits) appears on none of the three pages (0 hits for `code = `). The grpc/status page has 0 hits for either spelling.
- The S637 and S638 pinned copies contain 0 CamelCase hits.

So the identifier spelling is documented by gRPC-Go and Connect-Go; the `code = X` printed form the entry names is not documented by any page the entry cites, and no page is cited for it.

## 4. Registry scope for S221

SOURCES.md row S221 (line 227) reads "HTTP Semantics (RFC 9110) §15.4 Redirection 3xx", claim "the 3xx redirection class and the Location-header redirect ...", fetched 2026-10-23, `used by` includes `corpus/knowledge/seat-auth-deaths-r100.md`. The entry cites S221 for §15.5.2 and §15.5.4 (401/403), which the row does not cover; the row still says §15.4:7230-7252 and the 2026-10-23 fetch. The 401/403 quotes do exist in the live and pinned text (see section 2).

## 5. Frozen C1 sourced predicate

The frozen `sourced` conjunct (contract) requires the knowledge entry to cite S637 and S638 in `source:` lines and both rows `mined`. Observed: entry has `source:` lines for S637, S638 and S221; SOURCES.md rows S637 and S638 both read `mined` (lines 418–419). That conjunct is met as written; the findings above concern registry quality, not that predicate.

## Findings

1. S221 registry row is scoped to §15.4 (3xx), while the entry uses it for §15.5.2/§15.5.4 (401/403) with a 2026-11-05 "re-opened" note. Row needs a 401/403 scope or a new row.
2. The entry's Limits bullet names gRPC-Go `code = PermissionDenied` / `code = Unauthenticated`. Only the Go identifiers are documented (grpc/codes, connect); the `code = X` printed form is on none of the fetched pages, and no Go page is cited in the entry.

## Verdict

VERDICT C1-sources needs-amend: quotes and line numbers for S637, S638, S221 all verify verbatim within 25 words and support their claim sentences, and live bytes equal the pinned copies; but the S221 registry row covers §15.4 (3xx) rather than the 401/403 sections cited, and the entry's gRPC-Go `code = PermissionDenied` limit is cited to no page (the CamelCase identifiers are documented on pkg.go.dev, the printed `code =` form is not).

Unrun checks (not run by this seat): `count-c1.py`, `count-c2.py` battery, `--selftest`, round-17 gate, controls runner. Pertinent C2 counter was run once incidentally on the lane tree (read-only, no --work), output `C2=met stated=60 mismatches=7 uncorrected=0 spurious=0 altered=0 census=ok checks_failed=- base=d1bd1b33`; not a C2 verdict from this seat.

Tooling: no tools installed. Used curl and python3 (already present) and the existing web_search/_read tools. No sudo, no pacman, no writes outside this report and scratch.
