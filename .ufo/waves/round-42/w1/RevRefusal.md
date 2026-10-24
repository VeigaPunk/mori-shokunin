# RevRefusal — adjudication of `.ufo/waves/round-42/assimilation/refused-oom-tracing.md`

Reviewer seat, round-42 w1. Re-attempted the S268 fetch from this host on
2026-10-24 and judged the gate decision.

## Verdict

**The refusal was the correct gate decision on the evidence the L1 actually
gathered — and the recorded flip condition has now fired.** The VOR PDF is
fetchable from this host today via an alternate IEEE endpoint, and every quote
the refused entry carries verifies against it. The refusal record is honest and
accurately classified; the only gap is that the fetch attempt did not cover the
endpoint that serves bytes.

## Fetch re-attempt (run 2026-10-24 ~20:47 UTC, this host)

| channel | result |
|---|---|
| `curl -sIL https://doi.org/10.1109/TSC.2026.3698682` | 302 → `ieeexplore.ieee.org/document/11540439/` → **HTTP 202, 0-byte body** — reproduces the refusal's claim exactly |
| `GET ieeexplore.ieee.org/document/11540439` | **HTTP 202, size=0** — reproduces |
| `GET ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11540439` | HTTP 418, 15 KB HTML (mitigation page) |
| OpenAlex `works/doi:10.1109/tsc.2026.3698682` | `any_repository_has_fulltext: false`, `has_fulltext: false`; locations: IEEE (is_oa, cc-by, `pdf_url: null`) + Lancaster EPrints (`pdf_url: null`, is_oa: false) |
| `eprints.lancs.ac.uk/id/eprint/237917/` | 200 landing page; **"Full text not available from this repository"** |
| Semantic Scholar `paper/DOI:…` | 200; `openAccessPdf.url` is just the DOI (HYBRID, CCBY) — no independent copy |
| Unpaywall | `is_oa: true` (hybrid, publishedVersion); `best_oa_location.url_for_pdf: null` |
| **`GET ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber=11540439`** | **HTTP 200, `application/pdf`, 2 363 161 bytes, 14 pages** — the VOR PDF |

Extracted text (`pdftotext -enc UTF-8`) confirms IEEE TSC vol. 19 no. 4 pp.
3015–3028, © 2026 The Authors, CC BY 4.0 (text line 98–99), sha256
`d42b2fbfbd44d859f8f0af8f6a3e26d17ae290eff079e192af65d5190a9f49fc`. Byte size is
within ~0.3 % of the campaign row's recorded `2 357 114 B` (watermark/session
variance; same page count and license). The campaign's recheck
`grep -c 'mark_victim' -> 3` reproduces exactly (roma.txt lines 140, 441, 442).

## Quote re-location on the fetched copy

Every claim the refused entry `oom-tracing-tracepoints-r42.md` makes against
S268 is verifiable in the fetched VOR (line numbers in extracted text):

- `mark_victim`, `start_task_reaping`, `finish_task_reaping` — :139–141,
  :441–448 (`oom:` namespaced names confirmed).
- `lsm_oom_kill_check()` "intercepts victim selection and excludes
  system-critical or cross-container targets" — :142 verbatim.
- `lsm_oom_cleanup_container()` IPC/tmpfs/shared-memory reclamation — :143–145.
- "installed via standard LSM points and require no kernel patching or reboot"
  — :145–146 verbatim.
- "rely solely on per-process memory usage, lacking awareness of container
  context" + "heuristic scoring … core system daemons and normal workloads" —
  :78–81.
- "6.94% throughput overhead across eight workloads" — :26 (abstract) and :904,
  :1218.
- "benign throughput retention remains 92.6% with ROMA, compared with 82.4%"
  — :1049 verbatim.

By contrast the OpenAlex deposited abstract (the S262 basis) contains *none* of
the three tracepoint names, no `92.6`/`82.4`, and no hook names — so the entry
could not have been honestly re-scoped onto the abstract alone. Its
full-text-only load-bearing quotes genuinely required the PDF.

## Gate-decision judgment

- **Refuse (not admit) was correct.** Under QUALITY 60 a rejected row needs a
  located quote or an explicit unavailable limitation *with the access
  attempts*; the refusal records exactly that. Under the register's own class
  table (`unreachable` → "re-fetch, or mark the row unverifiable — do NOT call
  it a fabrication"), the quarantine-unverifiable class is right and the
  record correctly says unreachable-not-fabrication. Admitting the entry on
  the campaign's say-so would have installed unverified quotes — the
  fabrication class — and the precedent set (S262 adopted only after its
  abstract was located in a fetched OpenAlex copy) required the same located-
  quote bar for S268.
- **The refusal record is accurate.** Its two load-bearing fetch facts
  reproduce on this host today (202 + 0 bytes at doi.org and at
  `/document/`; `any_repository_has_fulltext: false`).
- **Residual risk it correctly names:** the row is quarantined, not deleted;
  the flip condition is concrete and checkable — and it has now fired.

## Recommendation (advisory, not a lane mutation)

1. **Flip condition met** — the `stampPDF/getPDF.jsp` endpoint is the
   operator-side/reachable fetch the record asked for. A future round should
   re-enter `oom-tracing-tracepoints-r42.md` at gating with the quotes
   re-located at the fetched copy (evidence above: sha256
   `d42b2fbf…f49fc`, all six quoted spans located verbatim).
2. **Fetch-policy gap (minor):** the L1 tried the landing path
   (`/document/`, `/stamp/stamp.jsp`) but not `stampPDF/getPDF.jsp`, which is
   the endpoint that serves bytes even while `/document/` returns the 202
   mitigation stub. Any "ieee unreachable" claim should cover that endpoint
   before it concludes unreachable; worth folding into the lane's
   source-fetch checklist alongside the existing huge_cap /
   redirect_private_refused policies.
3. **No erratum owed:** the refusal record asserts reachability *from this
   host on 2026-10-24 via the named channels*; those claims were true as
   written. The gap is completeness of the channel set, not accuracy.
4. Campaign-row nit (informational): staged S268 row records "2 357 114 B, 4
   pages"; fetched VOR is 14 pages / 2 363 161 B. The "4" likely records the
   DOI record's page-span count elsewhere; on flip the row's evidence cell
   should be updated with the observed copy's hash, size and 14-page count.

## Evidence files

Disposable sandbox `/tmp/revrefusal-s268/` (not committed):
`roma.pdf` (2 363 161 B), `roma.txt`, `abstract.txt`, `s268.oa.json`,
`unpaywall.json`, `s2.json`, `eprints.html`, `ieee-stamp.bin`, `s268-row.txt`.

## Tooling

No installs performed or needed (curl, pdftotext/poppler, python3 all
preinstalled). No secrets read; no production file edited; only this report
written.
