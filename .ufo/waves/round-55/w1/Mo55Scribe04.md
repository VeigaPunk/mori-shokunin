# Mo55Scribe04 — quarantine verdicts vs capture and source (mori r55 w1)

Seat: report-only scribe. Scope: the three quarantine verdicts in
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-55/assimilation/quarantine-verdicts.txt`
(committed at data rev `b8b7064c2b54c8b6b22c288232a96c43fae1af47`), checked against the slice capture,
the campaign register rows, the referenced lane tutorials/knowledge files, and the live carriers.
No production file was edited; no campaign file, register row, source row or lesson was changed.
No tool installed or upgraded. This seat is **not** a C1/C2 voter: no `RECHECK`, `ENTAIL`, `REPLACE`
or quote-bound vote line appears anywhere in this report or its output.

Context read: lane HEAD `b8a70adf93ebd9d1e4e95bef8627a220f2fa816b`; frozen contract
`.ufo/waves/round-55/contract.md` (lines 7-19 for the quarantine clause: "quarantine slice is re-derived");
frozen inputs `c9b908f0bb89974f30b927776ce2450ae4198b10`; data `b8b7064c`. Disk guard before work:
`/tmp` 3 %, `/var/tmp` 34 %, `/fast/scratch/hyaku` 26 % (595 G free) — no pressure, work proceeded.

## Headline

**Three rows, zero fabrication-class rows.** Under the register's own class table the slice is the
`unreachable` class by construction (register:15-16: `unreachable` = "the source could not be fetched, so the
quote was never checked … re-fetch, or mark the row unverifiable — do NOT call it a fabrication"), and mori
contributes **no** row to the `payload-absent` (fabrication) table: `grep -c '^| \`mori\` |'` on the register
= **3**, all three on lines 356-358 inside `## Rows whose quotes were NEVER CHECKED` (register:256).

Of the three verdicts:

- **S262 PRESENT and S268 PRESENT reproduce exactly.** I re-fetched the carrier today and got byte-identical
  content: HTTP 200, **2 357 114 B**, sha256 **1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2**
  (verdict:11,13 claim the same). Both quoted sentences are in that PDF at the stated printed pages and
  extracted line ranges. These are the strongest form of "verified against capture": the evidence is
  content-addressed, so it is re-derivable by anyone.
- **S244 UNVERIFIABLE is correct for the ACM publisher path and correct in refusing to call it fabrication —
  but it is narrower than the evidence in hand.** The row's own staged gate names an arXiv companion
  (`https://arxiv.org/abs/2403.18832`), which today returns **HTTP 200, 41 919 B, sha256
  `2f302c3cb6c055452cd81d708e1e071b9fc9264681e550724e5a5d90cb771bb4`** and carries the gate quote verbatim
  ("We find that 98.9% of commits in our dataset contain sentences with rationale information"). Round 45
  had already recorded that row as `quote-present` on the same companion with the same hash prefix
  (`.ufo/waves/round-45/w1/ScribeQuarantine.md:52`). The r55 file does not mention the companion, round 45's
  finding, or why that finding is no longer accepted.
- **The one number that does not reproduce is S244's "5,620-byte denial response"** (verdict:9). Today the
  ACM challenge body is 5 471 B with curl/no User-Agent and 5 684 B with a browser User-Agent; the same 403
  and the same Cloudflare "Just a moment..." body reproduce. No raw copy of that response exists in the data
  commit, so the byte count is the only quarantine claim that cannot be re-derived from a stored or
  content-addressed artifact.

Net: the file distinguishes unverifiable from fabrication correctly and never upgrades an unreachable row to
a fabrication judgement; its defects are the opposite direction (one verifiable row left unverifiable) plus
one unpinnable byte count.

## 0. Slice re-derivation (exact command, exact bytes)

Command as written in `assimilation/quarantine-verdicts.txt:3`, run with cwd
`/home/vgpnk/Projects/shokunin/mori-shokunin`:

```
awk -F'|' -v l='mori' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
```

Result (rc 0, three lines, leading and trailing space per line preserved):

```
 S244`   the cited source could not be fetched, so no quote was checked
 S262`   the cited source could not be fetched, so no quote was checked
 S268`   the cited source could not be fetched, so no quote was checked
```

- `assimilation/quarantine-slice` is **byte-exact** equal to that awk output plus a final newline
  (`od -c` shows the leading space; Python equality check returned `True`).
- The three register rows, read raw:
  `356:| \`mori\` | round1 | S244\` | … | https://doi.org/10.1145/3643916.3644413 |`,
  `357:| round4 | S262\` | … | https://doi.org/10.1109/TSC.2026.3698682 |`,
  `358:| round5 | S268\` | … | (same DOI) |`. The id cell carries the trailing backtick in the register
  itself, and the slice reproduces it rather than normalising it.
- The selector is complete for mori and does not leak the other table: mori has 3 register rows in total,
  none of them in `## Rows` (`payload-absent`), so the re-derived slice is exactly "mori's never-checked
  rows" — all `unreachable`.

## 1. Per-row check against capture and source

| row | verdict in file | capture re-run today | source check | class holds? |
|---|---|---|---|---|
| S244 | UNVERIFIABLE, not fabrication (verdict:9) | `curl -sS -L https://doi.org/10.1145/3643916.3644413` → **403**, 5 471 B, final `https://dl.acm.org/doi/10.1145/3643916.3644413`, `<title>Just a moment...</title>`; direct `dl.acm.org` request → same 403 / 5 471 B; browser User-Agent → **403 / 5 684 B**, sha256 `03d1a2b6…`; `curl -I -L` → 403 / 0 B. Zero occurrences of `98.9` or `rationale` in any denial body. **5 620 B is not reproduced by any of the four variants.** | register row has no quote column value; the same document's staged gate (§below) names the arXiv anchor | **partly** — unverifiable at the publisher is true; "no quote to compare" is false at document level |
| S262 | PRESENT (verdict:11) | `curl -sS -L -A '<browser UA>' https://ieeexplore.ieee.org/ielx8/4629386/11644734/11540439.pdf` → **200**, **2 357 114 B**, sha256 **1603404d…6add2** — identical to the claimed hash; without a browser UA the same URL returns **418 / 15 410 B**, reproducing why the UA is load-bearing | `pdfinfo`: 14 pages, Subject `10.1109/TSC.2026.3698682`. Sentence is the abstract's second sentence on printed page **3015** (page 1); `pdftotext -layout` lines **17-22** as claimed | **yes** |
| S268 | PRESENT, same PDF (verdict:13) | same 200 / 2 357 114 B / `1603404d…6add2` | printed page **3016** (page 2); `pdftotext -layout` lines **123-126** reproduce the claim, and the sentence is contiguous after dehyphenation: "It leverages eBPF to hook into OOM-related kernel tracepoints such as mark_victim, start_task_reaping, and finish_task_reaping to record OOM-triggering process metadata." | **yes** |

### 1.1 Why the two locator schemes do not conflict

The same sentence sits at different line numbers under different `pdftotext` modes of the same bytes:

| mode | S262 abstract sentence | S268 eBPF sentence |
|---|---|---|
| `pdftotext -layout` (mode the verdict declares) | line 19 hit, sentence 17-22 | lines 123-126 |
| `pdftotext` default, `-enc UTF-8` | line 15 hit | line **139** (sentence 139-141) |
| `pdftotext -raw` | line 12 hit | line 148 |

`corpus/SOURCES.md:257` (row **S478**, same DOI, same sha256 `1603404d…`, "printed page 3016, section I
Introduction … pdftotext lines 139-141") is the **default-mode** numbering, so S478 and the r55 verdict agree
on the page and differ only by extraction mode. Both resolve.

### 1.2 The extraction chain is reproducible byte-for-byte

`pdftotext -enc UTF-8 s262.pdf` yields 81 110 B / 1 405 lines / sha256
`5ce2d7ace3f3f385f005d620f456f969dfb5f1075325d91dd7a22845814c7f5b`, which is **byte-identical**
(`cmp` → identical) to the round-5 derived note
`/home/vgpnk/Projects/shokuknow/lanes/mori/round5/.deepresearch/notes/roma.txt` (same size, same hash). The
staged round-5 row's "1 405 lines of extracted text" is therefore also reproduced, and the r55 "PRESENT"
verdicts rest on the same artifact the round-5 row was written from — not on a re-made text.

### 1.3 S244 at document level: the companion the staged row itself names still serves the quote

- Staged row for the same document (`.ufo/waves/round-55/quarantine-slice` id `S244`; staging row
  `/home/vgpnk/Projects/shokuknow/lanes/mori/SOURCES-PROPOSED.md:160-166`, `## Gate — S483`):
  URL `https://arxiv.org/abs/2403.18832`, "Abstract.", quote
  "We find that 98.9% of commits in our dataset contain sentences with rationale information",
  opened 2026-10-23, and the note that `citation_doi` = `10.1145/3643916.3644413` is how the row bound the
  preprint to the ACM DOI.
- Identity is machine-checkable, not arithmetic: the live arXiv page carries
  `<meta name="citation_doi" content="10.1145/3643916.3644413"` — the exact DOI in the register row.
- Today's fetch: 200, 41 919 B, sha256 `2f302c3c…1bb4`; the abstract text contains the staged quote
  verbatim (`staged_S483_quote_in_abstract=True`), and the full sentence reads "We find that 98.9% of commits
  in our dataset contain sentences with rationale information, and that experienced developers report
  rationale in about 60% of the sentences in their commits."
- Round 45 recorded the same result on the same companion with hash prefix `2f302c3c…`
  (`.ufo/waves/round-45/w1/ScribeQuarantine.md:52`), verdict `quote-present`.

So the honest classification for S244 is: **publisher DOI 403 (unverifiable there) / quote present at the
anchor the row's own gate names**. "UNVERIFIABLE" as written drops the second half, and its flip condition
("when the publisher record/full text can be opened") is stricter than the row's own abstract-anchor scope.
Nothing about this makes the row a fabrication candidate, and the file does not call it one.

### 1.4 The fabrication boundary, stated for the record

The register's fabrication class requires "every relevant source fetched cleanly and the quote is in none of
them" (register:15). For these three rows that test was never satisfiable in this round's evidence:

- S262/S268: the carriers were fetched cleanly and the quotes **are** present → not fabrication, and not
  unverifiable either; PRESENT is the correct class.
- S244: the publisher carrier did **not** fetch cleanly (403 challenge page, body contains no article text);
  the companion fetched cleanly and holds the quote. Neither branch is a fabrication branch.

No row in this slice meets the fabrication test, and none is reported as one.

## 2. Findings

**F1 — medium — the only unpinnable number in the quarantine file.** `quarantine-verdicts.txt:9` records the
ACM denial as a "5,620-byte denial response"; today's re-fetch gives 5 471 B (curl/no UA) and 5 684 B
(browser UA), and the same 403 challenge body. Challenge pages vary per request, and the data commit retains
no raw copy of that response (`git show --stat b8b7064c` → only the 15-line text file), so the count is
asserted rather than captured. Evidence: `.ufo/waves/round-55/assimilation/quarantine-verdicts.txt:9`;
capture absent from `.ufo/waves/round-55/evidence/`.

**F2 — medium — a verifiable row is left unverifiable, with lane history unacknowledged.**
`quarantine-verdicts.txt:9` says the register row "supplies no locator or quote to compare, and no publisher
full text was available" and sets the flip condition on the publisher record. The row's own staged gate names
the arXiv companion, which serves the quote today (200, 41 919 B, `2f302c3c…`), and round 45 already
adjudicated it `quote-present` on that companion. Evidence:
`/home/vgpnk/Projects/shokuknow/lanes/mori/SOURCES-PROPOSED.md:160-166`,
`.ufo/waves/round-45/w1/ScribeQuarantine.md:52`, and the live `citation_doi` match to the register DOI.

**F3 — low — the transcribed capture in the verdict file is not byte-exact, though the capture file is.**
Lines 5-7 of `quarantine-verdicts.txt` drop the per-line leading and trailing space that `awk` emits;
`assimilation/quarantine-slice` reproduces it exactly (`slice == awk output + newline` → `True`,
`od -c` shows the leading space). The round-54 D1 lesson ("capture, not type") is satisfied by the slice file
and only imperfectly by the copy embedded in the verdict file.

**F4 — low — pre-existing source-row drift, surfaced by the PRESENT verdicts.** The staged round-5 row calls
the deposited VOR PDF "2 357 114 B, 4 pages" (`/home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md:43`);
the artifact with that exact size and hash has **14 pages** (`pdfinfo`). Byte count and the "1 405 lines of
extracted text" are correct; only the page count is wrong. This does not weaken S268's PRESENT verdict
(located on a named printed page), but a reader who sanity-checks page count against bytes will hit it.

**F5 — info — the two PRESENT verdicts judge quotes the slice rows do not carry.** The register rows for
S262/S268 have no quote cell value, so the verdicts necessarily compare against quotes drawn from lane
knowledge: `corpus/knowledge/oom-victim-context-r41.md:15-17` (verified: line 15 begins "The paper's own study
finding: 「Our study shows that Linux cgroups and the …", abstract-level, matching PDF page 3015) and
`corpus/knowledge/oom-tracepoints-r47.md:63-64` (verified: "leverages eBPF to hook into OOM-related kernel
tracepoints such as mark_victim, start_task_reaping, and finish_task_reaping", cited to S478 p. 3016). The
file states this provenance only implicitly, and states the "no quote in the row" fact only for S244.

**F6 — info — the classification asymmetry is defensible today, not proven permanent.** The same file treats
a 403 as terminal for S244 while using a browser User-Agent to unlock the IEEE PDF. I closed that gap from
this seat: with a browser User-Agent the ACM DOI still returns 403 / 5 684 B, so no browser-UA route exists
for that item today, and the register's own remedy ("re-fetch, or mark the row unverifiable") is followed.
Recorded so the asymmetry is not read as an untried route.

## 3. Commands actually exercised (all read-only)

| check | command (compressed) | result |
|---|---|---|
| disk guard | `scripts/hyaku/disk-guard.sh status` | 3 % / 34 % / 26 %; 595 G free |
| slice | the `awk` in §0 against the campaign register | rc 0, 3 rows; equals `quarantine-slice` byte-for-byte |
| mori rows | `grep -c '^| \`mori\` |' register` → 3; `grep -n` → 356-358 | no mori row in the `payload-absent` table |
| data commit contents | `git show --stat b8b7064c` | slice + verdicts + 8 evidence files + `disk-runway-enospc-r55.md` |
| S244 DOI | `curl -sS -L` (no UA / browser UA / curl UA), `curl -I -L` | 403, 5 471 B / 403, 5 684 B / 403, 5 471 B / 403, 0 B |
| S244 companion | `curl -sS -L arxiv.org/abs/2403.18832` | 200, 41 919 B, sha256 `2f302c3c…1bb4`; quote present verbatim |
| S244 identity | `<meta name="citation_doi">` on that page | `10.1145/3643916.3644413` = register DOI |
| S262/S268 PDF | `curl -sS -L -A '<browser UA>' …/ielx8/4629386/11644734/11540439.pdf` | 200, 2 357 114 B, sha256 `1603404dd25b…6add2` |
| same PDF without UA | `curl -sS -L -o /dev/null -w '%{http_code} %{size_download}'` | 418, 15 410 B (UA is load-bearing) |
| PDF facts | `pdfinfo` | 14 pages; Subject `…10.1109/TSC.2026.3698682` |
| quote location | `pdftotext -layout` / default / `-raw` | p. 3015 lines 17-22 (layout) / p. 3016 lines 123-126 (layout), 139-141 (default) |
| extraction identity | `pdftotext -enc UTF-8` + `cmp` vs r5 note | byte-identical, 81 110 B, `5ce2d7ac…4c7f5b` |
| abstract consistency | rebuild OpenAlex inverted index from `corpus/evidence/sources-r42/S262.oa.json` | contains "lack sufficient container context"; PDF abstract matches |
| S244 in lane register | `grep -nE '^\| *S(244|268) ' corpus/SOURCES.md` | rc 1 (absent); ACM DOI count in `SOURCES.md` = 0 |
| using file | `grep -c '98\.9\|3643916\|2403\.18832' corpus/knowledge/kernel-oom-line-attribution-r12.md` | 0 (no reference to the paper; unchanged since r45 F4) |
| knowledge quote anchors | `sed -n '15,17p' oom-victim-context-r41.md`; `grep -n mark_victim oom-tracepoints-r47.md` | both quotes present at the cited places |

## 4. Touched surfaces and limits

- **Written:** this report only. Scratch `/fast/scratch/hyaku/mori-r55/Mo55Scribe04/` was created, used and
  removed before yield (`rm -rf`); nothing under `/tmp` was used.
- **Read-only:** `.ufo/waves/round-55/{contract.md,assimilation/*,evidence/freeze-sha256.txt}`,
  `corpus/SOURCES.md`, `corpus/knowledge/{oom-victim-context-r41,oom-tracepoints-r47,kernel-oom-line-attribution-r12}.md`,
  `corpus/lessons/round-55.md`, `.ufo/waves/round-45/w1/ScribeQuarantine.md`,
  `corpus/evidence/sources-r42/S262.oa.json`, and the `shokuknow` staging/register files.
- **Not done:** no register, SOURCES, lesson or verdict file edited; no git/jj mutation; no commit or push;
  no browser-based Cloudflare bypass attempted; the 109-row never-checked table was not audited beyond
  mori's three rows.
- **Unverified by this seat:** round 45's verdicts for rows outside mori; anything behind the ACM challenge.
  Everything reported above was re-run here unless it is explicitly attributed to a cited file.
