# ScribeQuarantine — hand-check of the three quarantine rows (mori r45 w1)

Lane tip read: `3ad8faaa637ae466c61f9427fea1c208bf49ea82` (`git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD`).
Slice: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/assimilation/quarantine-slice` (3 rows).
Register that the slice names: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (read-only; never edited).
Lane register: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` (read-only; never edited).
Scratch: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/ScribeQuarantine` (no `/tmp` use). No tool installed or upgraded.

**Headline.** Of the three rows classed `unreachable`: two are `quote-present` at a carrier the row itself names (S244 on the arXiv companion; S262 on the OpenAlex deposited abstract), and one remains `unverifiable` today (S268 — every IEEE carrier 418 / 202-0-byte, repository copy absent). **No row is fabrication-class.** Two of the three rows have **no row in `corpus/SOURCES.md` at all**; their row content exists only in the staging package (`SOURCES.append.md` as `S483`/`S507`). The one row that does exist in the lane register (S262) exists only at abstract scope — the quarantine row S268 is the *full-text* row for the same paper and was never appended.

## 0. What the three slice rows actually are (read before the table)

The slice file, verbatim (3 data rows; the id cells are malformed, see F2):

```
 S244`   the cited source could not be fetched, so no quote was checked
 S262`   the cited source could not be fetched, so no quote was checked
 S268`   the cited source could not be fetched, so no quote was checked
```

Source rows in the campaign register, verbatim (`grep -n '^| `mori` |'`, register lines 356-358):

```
| `mori` | round1 | S244` | the cited source could not be fetched, so no quote was checked | https://doi.org/10.1145/3643916.3644413 |
| `mori` | round4 | S262` | the cited source could not be fetched, so no quote was checked | https://doi.org/10.1109/TSC.2026.3698682 |
| `mori` | round5 | S268` | the cited source could not be fetched, so no quote was checked | https://doi.org/10.1109/TSC.2026.3698682 |
```

Identity of the rows, by document (not by id arithmetic): the census ids are round-local; the merged staging rows are `S483` (`merge/mori/SOURCES.append.md:19`), `S501` (`:37`) and `S507` (`:43`) — same three documents.

Lane-register receipts (`cwd=/home/vgpnk/Projects/shokunin/mori-shokunin`):

```
$ grep -nE '^\| S(244|268|483|501|507) \|' corpus/SOURCES.md ; echo "rc=$?"
rc=1                                # none of those ids is a row in SOURCES.md
$ grep -c '3643916.3644413' corpus/SOURCES.md   -> 0
$ grep -c '2403.18832'      corpus/SOURCES.md   -> 0
$ grep -c '3698682'         corpus/SOURCES.md   -> 1   (line 243, id S262)
$ grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md -> 245 rows
$ git log --all --oneline -S"S244" -- corpus/SOURCES.md  -> (no output)
$ git log --all --oneline -S"S268" -- corpus/SOURCES.md  -> (no output)
```

So: **S262 has a `SOURCES.md` row (line 243) and it is the same document, abstract scope. S244 and S268 have never had a `SOURCES.md` row** in any commit reachable here. For those two, "read the row in `corpus/SOURCES.md`" has nothing to return; I read the row in the staging append instead and say so per row.

## 1. Verdict table (3 rows)

Legend: `quote-present` = the span the row's own gate block quotes was located verbatim in a fetched document the row itself names; `quote-absent` = fabrication class (all named sources fetched cleanly and the span is in none); `unverifiable` = still cannot fetch — never called fabrication.

| id (slice) | row in `corpus/SOURCES.md` | cited URL — fetch receipt (2026-10-25) | quote to locate (from the row's own gate block) | located? | **verdict** | `used-by` |
|---|---|---|---|---|---|---|
| **S244** | **absent** (never committed; `rc=1`). Row content: staged `S483`, `merge/mori/SOURCES.append.md:19`. URL `https://doi.org/10.1145/3643916.3644413`; anchor "Abstract, as published on `https://arxiv.org/abs/2403.18832`"; teaches "98.9% of the dataset's commits carry rationale sentences"; used-by `corpus/knowledge/kernel-oom-line-attribution-r12.md` | `curl -fsSL` → **403**, 0 B, rc 22, final `https://dl.acm.org/doi/10.1145/3643916.3644413`. Diagnostic GET (no `-f`): **403**, **5471 B** `text/html`, sha256 `f42332689e6b…53806`, body is the Cloudflare "Just a moment..." page | 「We find that 98.9% of commits in our dataset contain sentences with rationale information」 (`lanes/mori/SOURCES-PROPOSED.md`, `## Gate — S483`) | **Yes.** Companion the row names: `https://arxiv.org/abs/2403.18832` → **200**, **41919 B** `text/html; charset=utf-8`, sha256 `2f302c3cb6c0…71bb4`. Quote verbatim at **line 121** (the `Abstract:` span); also in the fetched **arXiv PDF** (`https://arxiv.org/pdf/2403.18832` → **200**, **1420568 B**, 3 pages, sha256 `ab8ab19551fb…018e`) at `pdftotext` **lines 29-30** (line 29 `…We find that 98.9% of commits` / line 30 `in our dataset contain sentences with rationale information, and`), repeated at lines 630 and 1186 | **`quote-present`** | `kernel-oom-line-attribution-r12.md` **exists** (7262 B) but does **not** carry this row's teaching: `grep -n -iE` over that file for `98.9`, `rationale`, `ACM`, `3643916`, `2403.18832`, `S483`, `S244` → **no match (rc 1)**. Its `source:` line is S003/S004/S014 and its claim is kernel event-time attribution. So a real file is named, but the row's `used-by` is a mismatch |
| **S262** | **present**: `corpus/SOURCES.md:243`. URL `https://doi.org/10.1109/TSC.2026.3698682`; anchor "OpenAlex work record for doi 10.1109/tsc.2026.3698682, abstract inverted index … refetched 2026-10-24, copy `corpus/evidence/sources-r42/S262.oa.json`"; teaches "the kernel's default OOM victim selection has no container context … per the authors' abstract"; used-by `corpus/knowledge/oom-victim-context-r41.md` | `curl -fsSL` → **202**, **0 B**, rc 0, final `https://ieeexplore.ieee.org/document/11540439/` (reproduces the quarantine exactly) | 「Our study shows that Linux cgroups and the default Out-of-Memory (OOM) mechanism lack sufficient container context when selecting victim processes.」 (`lanes/mori/round4/SOURCES-PROPOSED.md`, `## Gate — S501`) | **Yes.** Anchor carrier: `https://api.openalex.org/works/https://doi.org/10.1109/tsc.2026.3698682` → **200**, **67270 B** `application/json`, sha256 `f757c4a673d3…4a09`; abstract reconstructed from `abstract_inverted_index` (1456 chars) contains the quote verbatim; identical abstract to the committed `corpus/evidence/sources-r42/S262.oa.json` (sha256 `2ad83a48366a…62cc`, 1456 chars; `abstracts identical: True`) | **`quote-present`** | `oom-victim-context-r41.md` **exists** (5812 B) and claims exactly this: quotes the sentence at **lines 16-17** attributed "(S262)", and records the abstract-only boundary at **lines 44-50** (`ieeexplore…document/11540439` returns 202/0-byte; full text paywalled). Consistent |
| **S268** | **absent** (never committed; `rc=1`). Row content: staged `S507`, `merge/mori/SOURCES.append.md:43`. Same DOI URL; scope "the paper's **full text** as deposited by the publisher"; anchor "the eBPF/LSM paragraph … the VOR PDF deposited by the publisher (2 357 114 B, 4 pages)"; teaches the three tracepoints and two LSM hooks; used-by `corpus/knowledge/oom-tracing-tracepoints-r42.md` | `curl -fsSL` → **202**, **0 B**, rc 0, final `https://ieeexplore.ieee.org/document/11540439/` | 「It leverages eBPF to hook into OOM-related kernel tracepoints such as mark_victim, start_task_reaping, and finish_task_reaping」 (`lanes/mori/round5/SOURCES-PROPOSED.md`, `## Gate — S507`) | **No — carrier not fetched.** `stampPDF/getPDF.jsp?tp=&arnumber=11540439` → **418**, `text/html`, body **15410 B** (diagnostic GET; two attempts, different sha256: `f4b4b59f…df77`, `f4133bf0…52fa` — a dynamic mitigation page, magic `<script> var MEMBER_PROFILE_CHANGE_USERNAMEPASS_LINK`). `ielx8/4629386/11644734/11540439.pdf` → **418**, 15410 B. `xplorestaging…/11540439.pdf` → **418**, 15410 B. `eprints.lancs.ac.uk/id/eprint/237917/` → **200**, 25092 B, page says "**Full text not available from this repository.**". OpenAlex abstract (200) contains **none** of `mark_victim`, `start_task_reaping`, `finish_task_reaping`, `92.6`, `82.4`, `lsm_oom_kill_check` | **`unverifiable`** — *not* fabrication | `oom-tracing-tracepoints-r42.md` **does not exist**: `ls` → "No such file or directory"; `git ls-files` filtered for `oom-tracing` → only `.ufo/waves/round-42/assimilation/refused-oom-tracing.md`. The entry was refused in round 42 and never landed; the staged row nevertheless records status `mined` |

### 1.1 S268 — what "unverifiable" means here, precisely

Today's failure is `202` with a 0-byte body from the DOI/`ieeexplore` landing and `418` with a 15 KB mitigation page from every PDF endpoint the row names; the institutional repository explicitly has no deposited file. That is an unavailable read, not evidence of absence, so the row is `unverifiable`, **never** `quote-absent`. Supporting `corpus/knowledge/oom-tracing-tracepoints-r42.md` is absent, so nothing in the lane currently restates the quote outside this staging row.

Corroboration I found but did **not** treat as a located quote: the staging repo holds a derived text note `/home/vgpnk/Projects/shokuknow/lanes/mori/round5/.deepresearch/notes/roma.txt` (81110 B, sha256 `5ce2d7ace3f3…f75b`) whose line 139-140 reads `as mark_victim, start_task_reaping, and finish_task_reaping to record OOM-triggering process`. That is a derived artifact from an earlier fetch, not the cited source; I did not re-fetch the PDF and did not re-verify the note against a fetched copy. The carrier is demonstrably intermittent (`round-42/w1/RevRefusal.md` records a `stampPDF` 200 / 2 363 161 B / 14-page PDF on 2026-10-24; round 43 re-probed 418; I re-probe 418 today) — every unreachable verdict must carry its date, and this one carries 2026-10-25.

## 2. What the register's stale header totals mean for a reader

The register header (`absent-defect-register.md:18-23`) prints "rows with at least one ABSENT quote: **194**" and "ABSENT quotes: **324**", and its class table lists exactly one counted class (`payload-absent`, 194 rows). I measured the file itself: `## Rows` has **194** data rows over **19** lanes; `## Rows whose quotes were NEVER CHECKED` has **109** data rows over **18** lanes — **303** flagged data rows in total — and `## By lane` lists 19 lanes summing to **194**. So the header's 194 is *one of the two tables*, `unreachable` has **no row total anywhere** in the file, `324` is a quote count and not a row count, and `## By lane` silently omits the second table, including `lore` (9) and `mori` (3) — the only lanes that appear there and not here. The prose in the section preamble is honest ("These are not fabrications and they are not confirmed"), but the numbers above it are not: a reader who trusts the header sees a 194-row fabrication-class register and zero `unreachable` rows, and a reader who trusts `## By lane` concludes that mori has no flagged row at all. Compounding it, all **109** id cells in that second table are malformed (`S244\`` — a stray backtick where the closing `|` should be), so a strict `S[0-9]+` cell match returns the empty set and any tool-driven reader sees no slice. Our three rows are exactly the class this hides: not fabrications, not confirmed, and reachable only by reading lane-by-lane rather than by id.

## 3. Findings (register and staging are read-only for this seat; nothing fixed)

- **F1 — slice ids are not registry ids.** S244/S268 have no `SOURCES.md` row in any commit here (`git log -S` empty); they exist only as staged `S483`/`S507`. S262 does exist (`SOURCES.md:243`) but at abstract scope; the full-text row for the same paper is S268, which never landed. Any instruction to "check the row in `SOURCES.md`" silently resolves for one row of three.
- **F2 — generator defect, 109/109.** Every id cell in the never-checked table has a trailing backtick in place of the cell delimiter, so the slice is empty under a strict parse (`S244\`` not `S244`).
- **F3 — a `mined` row with no used-by file.** Staged `S507` records status `mined` and `used-by corpus/knowledge/oom-tracing-tracepoints-r42.md`, which does not exist; the only related byte is the round-42 refusal record.
- **F4 — a `used-by` that does not use the row.** Staged `S483`'s used-by `kernel-oom-line-attribution-r12.md` exists but contains no reference to the paper, the 98.9% figure, the ACM DOI or the arXiv id; its own `source:` line is S003/S004/S014.
- **F5 — header totals understate by 109 rows and give no `unreachable` count** (paragraph above).
- **F6 — nit in the refusal record.** `refused-oom-tracing.md` states OpenAlex reports `any_repository_has_fulltext: False`; the key is **absent** from both the live (2026-10-25) and committed records (`.get()` → `None`), so the literal value cited is a derived default, not a field. Not load-bearing for the refusal.
- **F7 — carrier intermittency must be dated.** S268's PDF was fetched 200 on 2026-10-24 (`RevRefusal.md`) and is 418 on 2026-10-25; an `unreachable` verdict is a verdict about one attempt on one day, and the register as rendered has no date column to carry that.

## 4. Checks actually exercised

| check | command (compressed) | result |
|---|---|---|
| lane tip | `git rev-parse HEAD` | `3ad8faaa637ae466c61f9427fea1c208bf49ea82` |
| S244 cited DOI | `curl -fsSL --max-time 40` | 403, 0 B, rc 22; diag 403/5471 B |
| S244 carrier | `curl -fsSL … arxiv.org/abs/2403.18832` | 200, 41919 B, sha `2f302c3c…` |
| S244 PDF | `curl -fsSL … arxiv.org/pdf/2403.18832` + `pdftotext` | 200, 1420568 B, sha `ab8ab195…`; quote lines 29-30 |
| S262/S268 cited DOI | `curl -fsSL … doi.org/10.1109/TSC.2026.3698682` | 202, 0 B, final `/document/11540439/` |
| S262 anchor | `curl -fsSL … api.openalex.org/works/…` | 200, 67270 B, sha `f757c4a6…`; quote present; abstract == committed |
| S268 carriers | `curl` stampPDF / ielx8 / xplorestaging / lancs | 418/15410, 418/15410, 418/15410, 200/"Full text not available" |
| absence in registry | the row-id `grep -nE` pattern quoted in §0 | rc 1 (no rows) |
| used-by existence | `ls` / `git ls-files` | 2 of 3 exist; `oom-tracing-tracepoints-r42.md` absent |
| register totals | `python3` row count by section | 194 + 109 = 303 rows; `By lane` 19 lanes = 194; 109/109 malformed ids |

## 5. Touched surfaces

- **Written:** this report and files under `.ufo/waves/round-45/tmp/ScribeQuarantine/` only (`f-1dea8e74.bin`, `s244.pdf`, `s244.txt`, `acm403.html`, `openalex.json`, `stamp418.html`, `stamp418b.html`, `doi202.bin`, `xplore418.html`, `lancs.html`).
- **Read-only:** `corpus/SOURCES.md`, `corpus/knowledge/*.md`, `.ufo/waves/round-4[234]/…`, the campaign register, and `shokuknow/merge/mori/SOURCES.append.md` + `shokuknow/lanes/mori/…`.
- **Not done:** no register edit, no `SOURCES.md` edit, no verdict upgraded from a non-fetch, no git mutation, no tool install, no `/tmp` write.
