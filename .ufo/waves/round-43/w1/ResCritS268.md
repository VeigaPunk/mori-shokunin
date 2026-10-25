# ResCritS268 — attack on the S268 refusal

Round-43 w1 residual critic, 2026-10-24 (local). Target: `.ufo/waves/round-43/assimilation/refused.md` § S268 ("Not re-admitted... The r42 refusal stands") and its underlying record `.ufo/waves/round-42/assimilation/refused-oom-tracing.md`. Source S268 = ROMA paper, DOI 10.1109/TSC.2026.3698682, IEEE Xplore arnumber 11540439.

## Axes attacked

1. **Method artifact** — r43 closed the flip on a `curl -sI` (HEAD) probe returning 418; r42's own review (`.ufo/waves/round-42/w1/RevRefusal.md`) recorded `GET stampPDF/getPDF.jsp` → 200 `application/pdf`, 2 363 161 B. If GET still serves bytes, the r43 flip-check is unsound and the refusal collapses.
2. **Wrong-endpoint artifact** — the 15 410-byte 418 body equals r42's `stamp/stamp.jsp` mitigation-page size; if the refusal probed the wrong stamp path, "no PDF" is unproven.
3. **Committed-copy escape** — a PDF for this source already committed under `corpus/evidence/` would make the refusal moot.

## Probes (all from this host, 2026-10-24 22:56 local; body to /tmp sandbox only)

1. HEAD, the stampPDF endpoint (assigned probe):
   - `$ curl -sI 'https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber=11540439'`
   - `HTTP/2 418`, `content-type: text/html`, `content-length: 15410` (plus no-store/cloudfront error headers). Reproduces refused.md exactly.
2. GET, same URL (method-artifact test):
   - `$ curl -s -o /tmp/rescrit-s268/get.pdf -w 'HTTP %{http_code} | content-type: %{content_type} | size: %{size_download}\n' 'https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber=11540439'`
   - `HTTP 418 | content-type: text/html | size: 15410`; `file get.pdf` → "HTML document"; body begins `<script> var MEMBER_PROFILE_...` (IEEE Xplore HTML, not `%PDF`); sha256 `eea70952e36f4e23a9aa13d4607acbc8420753bab6433bd47d6789a2466d8007`.
3. HEAD `https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11540439` → `HTTP/2 418`, `text/html`, 15410 — same mitigation page; no endpoint confusion helps.
4. `$ curl -sIL 'https://doi.org/10.1109/TSC.2026.3698682'` → `https://ieeexplore.ieee.org/document/11540439/ -> HTTP 202 | type=text/html; charset=UTF-8 | size=0` — reproduces the r42 refusal's primary claim.

## Counterexample result

The strongest counterexample available — "GET still serves the PDF that r42's RevRefusal fetched; the r43 flip-check used the wrong HTTP method" — is **falsified**. GET on `stampPDF/getPDF.jsp` now returns the identical 15 410-byte 418 HTML mitigation page as HEAD. The endpoint state that r42 recorded (200 `application/pdf`, 2 363 161 B) no longer reproduces from this host; the flip condition RevRefusal declared "fired" has since un-fired. Every load-bearing fetch fact in the r43 refusal (418 / text/html / 15410; doi.org → 202 + 0 bytes) reproduces exactly.

## Committed-evidence census

`git ls-files corpus/evidence/` shows exactly one committed PDF in the lane: `corpus/evidence/sources-r42/S235.pdf` — row S235 (r42 whitepaper), a different source. **No committed file under `corpus/evidence/` is a PDF for the S268/ROMA source.** Related committed files are not PDFs: `sources-r42/S262.oa.json` is the same DOI's OpenAlex abstract-level record keyed to row S262 (mined, abstract-class — consistent, not a duplicate authority), and `.ufo/waves/round-43/evidence/s268-headers.txt` (headers receipt) lives outside `corpus/evidence/`.

## Smallest safe correction (advisory; no lane file edited by this seat)

The r43 refusal is correct on today's evidence but cites only the `-I` probe. Since r42's own record proves this exact endpoint can serve GET while other channels stub, a HEAD-only probe cannot by itself distinguish "mitigation page" from "HEAD-rejected-but-GET-serves" in either direction. Fold into the source-fetch checklist: an unreachable/not-fetchable verdict must record a full-GET probe (status + content-type + first bytes / magic) for each candidate endpoint, not `-I` alone. The refusal itself stands and S268 correctly remains quarantined-unverifiable.

Verdict line below; scratch artifacts in `/tmp/rescrit-s268/` (not committed).

SURVIVED — $ curl -sI 'https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber=11540439'
HTTP/2 418
content-type: text/html
content-length: 15410
cache-control: no-store, must-revalidate, no-cache
pragma: no-cache
x-content-type-options: nosniff
x-frame-options: SAMEORIGIN
x-xss-protection: 1; mode=block
date: Sun, 25 Oct 2026 01:56:07 GMT
x-cache: Error from cloudfront
via: 1.1 7aaab53a596909564459a4a21007ab68.cloudfront.net (CloudFront)
x-amz-cf-pop: GIG52-P3
x-amz-cf-id: iIIttnC2NWuxlR0zC1671ripWNuTmIguy-BXR4f25tLnUjWOXdtBKw==
