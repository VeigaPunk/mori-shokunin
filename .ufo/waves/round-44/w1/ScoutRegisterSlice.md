# ScoutRegisterSlice — mori's quarantine slice of the campaign absent-defect register

Scope: read-only. The register
(`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`)
was read, never edited; no campaign tool was run in `/home/vgpnk/Projects/shokuknow`;
the lane repo was read with read-only `git grep` / `git log -S`. Scratch fetches ran
in `/tmp/tmp.HKMUfGZVks`. No tool was installed or upgraded for this item.

The "§10" pointer resolves to the round prompt's assimilation item (the register is
the quarantine gate on the append), not to a section of the frozen
`.ufo/waves/round-44/contract.md`, which has only `P-C1`, `P-C2`, `P-C3`, `Freeze`.

## 1. Derivation (header and `## By lane` totals not trusted)

Rule applied: data rows only (lines beginning `| \``), lane cell `mori`, round cell
matching `round[0-9]+`, id cell matching `S[0-9]+`. The register has two data tables:

```
$ python3 -  # counts by section
payload rows 194
never rows 109
mori payload 0
mori never 3
never-section reason cells: 78 "the cited source could not be fetched", 31 "the gate block named no locator"
id cells not fullmatching " S[0-9]+ ": 109 of 109
sample id cells: [' S039` ', ' S041` ', ' S100` ']
```

Two consequences a reader must know:

1. **The slice is in the second table only** (`## Rows whose quotes were NEVER
   CHECKED`), which has no `class` column at all: its fourth cell is a prose
   "why it was not checked" sentence. The register's class vocabulary for it is
   `unreachable` ("the source could not be fetched, so the quote was never
   checked"), defined in the header table; that table's `unreachable` row is not
   used by any data row.
2. **Every id cell in that table is malformed** — `S244\`` instead of `S244` (a
   stray backtick where the closing `|` should be), 109 of 109. Under a strict
   full-match rule the slice is *empty*; under a match rule it is the 3 rows below.
   The lane's own round-43 lesson independently names the same three ids
   (`corpus/lessons/round-43.md:92-94`), which is why I treat the 3-row slice as
   the intended one and report the malformation rather than the empty set.

The header/totals are stale exactly as warned:

- header: "rows with at least one ABSENT quote: **194**" — 194 is the *first*
  table only; the file carries 303 flagged data rows (194 + 109).
- `## By lane` sums to 194 and lists the 19 lanes of table 1; the file also has
  `lore` (9) and `mori` (3) in table 2, and neither lane appears in that table.
- "ABSENT quotes: **324**" is a *quote* count from the census
  (`quote-lint-full-v5.json` totals: `quotes 4152, exact 2532, folded 1296,
  absent 324, fetch_failed 78, no_url 31`), not a row count.

Command and output for the slice itself:

```
$ grep -n '^| `mori` |' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
356:| `mori` | round1 | S244` | the cited source could not be fetched, so no quote was checked | https://doi.org/10.1145/3643916.3644413 |
357:| `mori` | round4 | S262` | the cited source could not be fetched, so no quote was checked | https://doi.org/10.1109/TSC.2026.3698682 |
358:| `mori` | round5 | S268` | the cited source could not be fetched, so no quote was checked | https://doi.org/10.1109/TSC.2026.3698682 |
```

## 2. Raw slice (verbatim, 3 data rows)

```
| `mori` | round1 | S244` | the cited source could not be fetched, so no quote was checked | https://doi.org/10.1145/3643916.3644413 |
| `mori` | round4 | S262` | the cited source could not be fetched, so no quote was checked | https://doi.org/10.1109/TSC.2026.3698682 |
| `mori` | round5 | S268` | the cited source could not be fetched, so no quote was checked | https://doi.org/10.1109/TSC.2026.3698682 |
```

Row count: **3**. (`mori` appears nowhere in the payload-absent table.)

## 3. Verdicts

The verdict vocabulary used here follows the register's own header: `payload-absent`
(fabrication class) requires that *every relevant source fetched cleanly and the
quote is in none of them*; a source that could not be fetched is `unreachable` =
**unverifiable, not fabrication**.

| id | round | class cell (verbatim) | verdict | basis |
|---|---|---|---|---|
| S244 | round1 | `the cited source could not be fetched, so no quote was checked` | **clean** — quote located in a fetchable source the row itself names | the register's cited URL (ACM DOI) is 403, but the row's own gate block cites `https://arxiv.org/abs/2403.18832`; quote present verbatim there and in the arXiv PDF |
| S262 | round4 | `the cited source could not be fetched, so no quote was checked` | **clean** — quote located in the fetchable deposited abstract | the DOI landing is 202/0 bytes, but the row's own `anchor` is the OpenAlex deposited abstract, live-fetchable (HTTP 200) and committed at `corpus/evidence/sources-r42/S262.oa.json`; quote present verbatim |
| S268 | round5 | `the cited source could not be fetched, so no quote was checked` | **unverifiable** (not fabrication) | every endpoint for the claimed carrier is unreachable (202/0 bytes; VOR and stampPDF 418 HTML; repository record has no deposited file); the quoted sentence is not in the abstract; no committed PDF exists |

No row in the slice is fabrication-class. None of the three was ever a
"quote in none of the sources" case: the census never attempted a match on them.

### 3.1 What each row is in the current staging

Identified **by document identity**, not id arithmetic (the staged ids were
renumbered twice; `ID-REMAP.md:25` maps round1's last pre-merge id `S360`→`S483`,
`:111` maps round4 `S378`→`S501`, `:117` maps round5 `S384`→`S507`; the census's
round1 is 13 rows `S232`–`S244`, round4 `S262`–`S267`, round5 `S268`–`S272`).

| register id | staged row in the merge package | document |
|---|---|---|
| S244 | `S483` (`merge/mori/SOURCES.append.md:19`) | ACM DOI 10.1145/3643916.3644413 + arXiv:2403.18832 |
| S262 | `S501` (`merge/mori/SOURCES.append.md:37`) | IEEE TSC ROMA, abstract scope |
| S268 | `S507` (`merge/mori/SOURCES.append.md:43`) | IEEE TSC ROMA, full-text scope |

## 4. Fetch receipts

Every probe is a full GET (`-L`, body written to a file), per QUALITY 116 — no
HEAD-only verdicts.

```
https://doi.org/10.1145/3643916.3644413
  -> 403  text/html; charset=UTF-8  5471  https://dl.acm.org/doi/10.1145/3643916.3644413
  magic=<!DOCTYPE html><html lang="en-US"><head><title>Just a moment
https://dl.acm.org/doi/10.1145/3643916.3644413
  -> 403  text/html; charset=UTF-8  5471  https://dl.acm.org/doi/10.1145/3643916.3644413
https://doi.org/10.1109/TSC.2026.3698682
  -> 202  text/html; charset=UTF-8  0  https://ieeexplore.ieee.org/document/11540439/
https://ieeexplore.ieee.org/document/11540439
  -> 202  text/html; charset=UTF-8  0  https://ieeexplore.ieee.org/document/11540439/
https://arxiv.org/abs/2403.18832
  -> 200  text/html; charset=utf-8  41919
https://arxiv.org/pdf/2403.18832
  -> 200  application/pdf  1420568  (file: PDF document, version 1.5, 3 page(s))
https://api.openalex.org/works/https://doi.org/10.1145/3643916.3644413
  -> 200  15977  has_fulltext=True  best_oa_location pdf=https://arxiv.org/pdf/2403.18832
https://api.openalex.org/works/https://doi.org/10.1109/TSC.2026.3698682
  -> 200  67270  has_fulltext=False  oa_status=hybrid  any_repository_has_fulltext=False
      locations: DOI landing (is_oa=True, pdf_url=None); Lancaster EPrints (is_oa=False, pdf_url=None)
https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber=11540439
  -> 418  text/html  15410  (HTML, starts `<script> var MEMBER_PROFILE_CHANGE_USERNAMEPASS_LINK = …`)
https://xplorestaging.ieee.org/ielx8/4629386/11644734/11540439.pdf?arnumber=11540439
  -> 418  text/html  15410
https://eprints.lancs.ac.uk/id/eprint/237917/
  -> 200  text/html; charset=utf-8  25092  (title: ROMA : Enhancing Container OOM Resilience …)
      JSON export has no `documents` key -> metadata-only record, no deposited file
https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/TSC.2026.3698682?fields=title,openAccessPdf,…
  -> 429  Too Many Requests   (recorded as a probe that did not answer, not as absence)
```

### 4.1 S244 — quote located

The row's gate block (`lanes/mori/SOURCES-PROPOSED.md`, `## Gate — S483`) names
`https://arxiv.org/abs/2403.18832` and quotes:

> We find that 98.9% of commits in our dataset contain sentences with rationale information

Located verbatim in the fetchable arXiv abstract page and in the arXiv PDF:

```
$ python3 -   # joined text of the fetched HTML / pdftotext output
S483 QUOTE IN arXiv ABS PAGE: True
'…such as presence, temporal evolution, and structure. We find that 98.9% of commits in our dataset contain sentences with rationale information, and that experienced developers report rationale in about 60% of the …'
S483 QUOTE PRESENT IN arXiv PDF: True
$ sed -n '27,33p' s244.txt
… We find that 98.9% of commits
in our dataset contain sentences with rationale information, and
that experienced developers report rationale in about 60% of the
sentences in their commits.
```

So the register's prose class is true of the *canonical ACM landing* only (403
Cloudflare interstitial, 5471 bytes). The quote is checkable and present at the
companion the row itself cites. Verdict `clean` at the row's own scope.

### 4.2 S262 — quote located

The lane's registry row (`corpus/SOURCES.md:243`) declares the OpenAlex deposited
abstract as its anchor. Reconstructed from the live OpenAlex record (HTTP 200) and
from the committed `corpus/evidence/sources-r42/S262.oa.json`, the gate block's
quote is present verbatim:

> Our study shows that Linux cgroups and the default Out-of-Memory (OOM) mechanism lack sufficient container context when selecting victim processes.

```
QUOTE PRESENT: True
'Our study shows that Linux cgroups and the default Out-of-Memory (OOM) mechanism lack sufficient container context when selecting victim processes. As a result, a malicious container may disrupt critical co-located servi…'
```

Scope caveat stands: abstract-level only. The DOI landing page is still 202 with
0 bytes and the full text is not obtainable here (`has_fulltext=False`).

### 4.3 S268 — nothing located

The gate block claims the sentence sits in the publisher's deposited VOR PDF
(2,357,114 B) and quotes:

> It leverages eBPF to hook into OOM-related kernel tracepoints such as mark_victim, start_task_reaping, and finish_task_reaping

Every claimed carrier failed: VOR link 418 (HTML, 15410 B), stampPDF 418 (HTML),
ieeexplore 202/0 bytes, OpenAlex `pdf_url=None` and `any_repository_has_fulltext=False`,
the Lancaster EPrints record metadata-only, and no committed PDF in the lane
(`find . -name '*.pdf' -newermt 2026-10-20` → only `corpus/evidence/sources-r42/S235.pdf`).
The sentence is not in the abstract either:

```
eBPF in abstract: True
mark_victim in abstract: False
start_task_reaping in abstract: False
```

Verdict **unverifiable**, not fabrication: the carrier was never read, so "the quote
is in none of them" cannot be asserted. This agrees with the lane's own standing
refusal (`corpus/lessons/round-42.md:16`, `round-42-verifier-spotcheck.md:113`,
`round-43.md:61`, `round-43.md:144`).

## 5. Constraint on the C3 assimilation set

- **Intersection with C3's own rows: zero.** C3's entry cites `S471`/`S472`; the
  quarantine slice is `S244`/`S262`/`S268` = staged `S483`/`S501`/`S507`. None of
  the three quarantine rows is a C3 source, so the slice does not gate the C3
  entry's two pages.
- **Intersection with the item-10 append: all three rows are in it**
  (`merge/mori/SOURCES.append.md:19,37,43`; `MERGE-REPORT.md` records
  "proposed rows refused: **0**"). On this evidence:
  - `S483` and `S501` may be appended as verified at the scope their rows declare
    (arXiv preprint abstract; OpenAlex deposited abstract) — quotes located.
  - `S507` must not be appended as a verified full-text row: its load-bearing
    sentences (`mark_victim`, `start_task_reaping`, `finish_task_reaping`, the two
    LSM hooks) rest on a document this host cannot fetch and no committed copy
    holds. The corresponding entry was already refused in round 42 and not
    re-admitted in round 43; re-introducing it through the append would reinstate
    a refused source. Flip condition: any fetchable copy of the VOR PDF that
    yields the quoted sentence (a full GET, per QUALITY 116) — not a metadata
    record.
- Nothing in the slice is fabrication-class, so the quarantine does not force a
  refusal of the C3 entry itself.

## 6. Register defects observed (reported, not fixed — register is read-only)

1. **All 109 id cells in `## Rows whose quotes were NEVER CHECKED` are malformed**
   (`S244\`` instead of `S244`), so a strict cell match returns an empty slice.
   This is a generator defect, not a lane defect.
2. **The header and `## By lane` describe only the first table.** The file carries
   303 flagged data rows (194 `payload-absent` + 109 never-checked); `By lane`
   omits `lore` (9) and `mori` (3), the only two lanes with rows in the second table.
3. **`fetch-failed` is a one-endpoint verdict.** `quote-lint.py`'s `block_url()`
   picks a single URL (gate-block URL line, else the row's first URL) and marks the
   row failed when that one document is empty, without trying the row's other URLs.
   That is exactly why S244 is listed as unfetchable while the same row's companion
   URL (arXiv) serves the quote: the class is honest about the endpoint, not about
   the row.

## 7. Remaining unknowns

- Whether the ACM landing page serves the text to a non-blocked client (403 is a
  Cloudflare interstitial here; the work's identity is confirmed by OpenAlex and
  the arXiv record).
- Whether a full text of 10.1109/TSC.2026.3698682 is obtainable from any endpoint
  this host can reach; the Semantic Scholar probe was rate-limited (429) and is
  therefore neither a yes nor a no.
