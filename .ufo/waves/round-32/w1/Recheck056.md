# Recheck056 — S056 (C1, round 32 attempt 2)

Seat: MoriR32A2.Recheck056. Scope: one population id, S056. Verdict: **unreachable**.
No tools installed or updated this seat (nothing needed; curl/python3/git already present).

## 1. Fetch

| field | value |
|---|---|
| id | S056 |
| population url | `https://www.pnas.org/doi/10.1073/pnas.1708274114` |
| accessed (UTC, at first fetch) | `2026-10-23T01:31:22Z` |
| HTTP | `403` on every try, `final=https://www.pnas.org/doi/10.1073/pnas.1708274114` (no redirect, `num_redirects=0`) |
| tries | 6 of 6 failed (two batches of 3; exit=22 each) |
| byte size | 0 (curl `--fail` discards the challenge body) |
| sha256 | none — no copy exists; row cell is `-` |
| fetch transcript (for commit at `corpus/evidence/recheck-r32/S056.fetch.txt`) | `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck056/S056.fetch.txt`, 1003 bytes, sha256 `ad4f4255276862dbb98fc26ba012097fb52824c5764e77fcf387adf824c4621f` |
| scratch copies | no `.src` (nothing was fetched); `S056.err` holds the raw curl stderr |

Fetches, each `curl -sSL --fail -m 60 https://www.pnas.org/doi/10.1073/pnas.1708274114 -o S056.src`:

```
2026-10-23T01:31:22Z  exit=22  HTTP=403  bytes=0
2026-10-23T01:31:25Z  exit=22  HTTP=403  bytes=0
2026-10-23T01:31:28Z  exit=22  HTTP=403  bytes=0
2026-10-23T01:31:52Z  exit=22  HTTP=403  bytes=0   (fresh shell, batch 2 x3)
stderr every try: curl: (22) The requested URL returned error: 403
```

Response headers for the same URL without `--fail` show a bot gate, not a moved page:

```
HTTP/2 403
server: cloudflare
cf-mitigated: challenge
content-type: text/html; charset=UTF-8
content-length: 5473
```

No `location:` header. Bare host `https://pnas.org/doi/10.1073/pnas.1708274114` and `https://pnas.org/doi/full/10.1073/pnas.1708274114`
return the same `403` / `cf-mitigated: challenge` (checked 01:32Z). The challenge was not attempted (contract).

The frozen counter's own fetcher reaches the same wall: calling `count-c1.fetch('https://www.pnas.org/doi/10.1073/pnas.1708274114')`
directly (import of `.ufo/waves/round-32/count-c1.py`, 01:34Z) yields `counter_fetch_yields= 0`, i.e. R3's unreachable branch
(`count-c1.py:261-265`) is the branch this row takes. C0 already recorded the same fact: `.ufo/waves/round-32/c0/CtlDoNothingJunk.md:158`
— "all-unreachable: 33 report counter_fetch_ok,judge; S056 reports only judge".

DOI resolution, for the record (not the population url): `https://doi.org/10.1073/pnas.1708274114` answers `HTTP/2 302` with
`location: https://pnas.org/doi/full/10.1073/pnas.1708274114` (01:32Z). That is PNAS's own canonical-link scheme, not a
redirect this row's url made.

## 2. Ready-to-paste row

```markdown
| S056 | https://www.pnas.org/doi/10.1073/pnas.1708274114 | 2026-10-23T01:31:22Z | - | - | unreachable |
```

Cell rationale: `sha256` and `quotes` are `-` because no bytes were obtained; R2 and the quote checks apply only to
`current`/`drifted` rows (`count-c1.py` docstring R2/R3, code `count-c1.py:239-262`), while an `unreachable` row needs the
committed transcript and three failed counter fetches. Nothing else is invented.

**Integrator action:** commit the transcript content at `corpus/evidence/recheck-r32/S056.fetch.txt` exactly as the scratch
copy (sha256 `ad4f4255276862dbb98fc26ba012097fb52824c5764e77fcf387adf824c4621f`), and paste the row above into the
`## Recheck` table of `corpus/lessons/round-32.md`. My scratch copy of that transcript:

```text
id: S056
url: https://www.pnas.org/doi/10.1073/pnas.1708274114
fetch_at: 2026-10-23T01:31:22Z (first), 2026-10-23T01:31:52Z (last)
command: curl -sSL --fail -m 60 https://www.pnas.org/doi/10.1073/pnas.1708274114 -o S056.src

batch 1:
  2026-10-23T01:31:22Z exit=22 http=403 bytes=0
  2026-10-23T01:31:25Z exit=22 http=403 bytes=0
  2026-10-23T01:31:28Z exit=22 http=403 bytes=0
batch 2 (fresh shell):
  2026-10-23T01:31:52Z exit=22 http=403 bytes=0
  2026-10-23T01:31:52Z exit=22 http=403 bytes=0
  2026-10-23T01:31:52Z exit=22 http=403 bytes=0

stderr (identical each try):
  curl: (22) The requested URL returned error: 403

response status line and headers (same URL, without --fail):
  HTTP/2 403
  server: cloudflare
  cf-mitigated: challenge
  content-type: text/html; charset=UTF-8
  content-length: 5473

no redirect: num_redirects=0, url_effective == requested url.
bot challenge not attempted (round-32 contract).
counter cross-check: count-c1.fetch(url) yielded 0 bodies (2026-10-23T01:34Z).
```

## 3. Quotes → teaches cell

None: no bytes were served, so there is nothing honest to quote from the population url, and the row is `unreachable`.

Supplementary content check (NOT the population url, NOT used in the row): the same article is open at the NCBI mirror
`https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/` (`HTTP 200`, 196972 bytes, sha256
`ccc65da58d4f56b6c91fa13a87dc9a2f34af7eab9c0cee6be83a3d3aa166201b`; normalised by the counter's own `normalise()`:
61098 bytes). In that mirror the article is still `Proc Natl Acad Sci U S A . 2018 Mar 13;115(11):2600-2606. doi:
10.1073/pnas.1708274114`, `The preregistration revolution`, Brian A Nosek — matching the row's anchor (journal, volume,
issue, pages, date). The teaches-cell claims are still present verbatim there:
`In prediction, the problem of forking paths is avoided because the analytic pipeline is specified before observing the data`;
`there is not yet sufficient experimental evidence establishing its superiority for reproducibility`;
`Challenge 1: Changes to Procedure During Study Administration`; `Standard Tools of Statistical Inference Assume Prediction`.
So no contradiction with the teaches cell was found in the article's own archival copy — the obstruction is the Cloudflare
gate on `www.pnas.org`, not a changed article. That is why the verdict is `unreachable` and not `drifted`; a `current`
verdict is impossible because R3 would need the live PNAS bytes, and fabricating a copy was not considered.

## 4. Self-check output

`seat-check.py row` (the contract requires `ROW_CHECK=pass` only for current/drifted; recorded for the check that this
unreachable shape is what I claim):

```
$ timeout 300 python3 .ufo/waves/round-32/seat-check.py row S056 S056.fetch.txt '-'
sha256=ad4f4255276862dbb98fc26ba012097fb52824c5764e77fcf387adf824c4621f
quotes=0 words=[] in_copy=[]
shared_tokens=[] topic_ok=False
live_quotes_ok=False
ROW_CHECK=fail (judge R4 and R5 not checked here)
seat_check_exit=1
```

Frozen counter, run live-mode against a throwaway `git init` repo in my scratch
(`/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck056/mini`, commit `a08e3613c8efab6feea2663b46a72c357637ddf3`) holding only
this row and the transcript:

```
$ timeout --kill-after=5 300 prlimit --as=2147483648 -- python3 .ufo/waves/round-32/count-c1.py \
    a08e3613c8efab6feea2663b46a72c357637ddf3 --repo /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck056/mini
revision=a08e3613c8efab6feea2663b46a72c357637ddf3 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=1 header_ok=True section_sha256=a71ea0d78139126c judge_ok=False judge_seat_ok=False judge_agree=0
rows_ok=0/34 verdicts={'unreachable': 1}
row_failures=... S056:judge ...
new_ok=0 new_failures=none
C1=unmet exit=1
```

`S056:judge` only: R1 (url, accessed, verdict, six cells, header), the transcript-existence half of R3 and the
"counter fetch succeeded" half of R3 all pass; only R4 (the reviewer receipt, not mine to write) is missing — the same
signature C0 saw for this id (`c0/CtlDoNothingJunk.md:158`). The other 33 ids report `rows=0` because the scratch repo
holds only this row.

## 5. Drift

No drift found, no `Round32` correction drafted: the article's archival copy still states every teaches-cell claim, and the
population url served no bytes that could differ. Remaining unknowns:

- Whether `www.pnas.org/doi/10.1073/pnas.1708274114` would still 200 for a browser: unobservable from this host without
  passing the Cloudflare challenge, which the contract forbids. The 403 carries `cf-mitigated: challenge`, so the page is
  gated rather than confirmed moved. [INFERENCE] PNAS canonicalises new links to `/doi/full/...` (seen in the doi.org 302),
  so the older `/doi/...` form might redirect for a browser; curl never got a `location:` header to confirm it.
- If a later round needs S056 quoted rather than transcribed, the PMC5856500 mirror is open and holds the same text, but the
  url cell must stay the population url, so its quotes cannot satisfy R3.

Bounds respected: writes only to this report and `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck056/`; no lane git or jj
writes (the only git commands ran in the scratch `mini` repo, with `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset);
every command bounded by `timeout`; no processes left running; no pacman, no host services touched.
