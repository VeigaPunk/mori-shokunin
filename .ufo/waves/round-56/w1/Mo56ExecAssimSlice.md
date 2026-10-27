# Mo56ExecAssimSlice — independent re-derivation of the mori absent-defect register slice

Seat: executor (leaf, no subagents dispatched). Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`;
scratch `/fast/scratch/hyaku/mori-r56/Mo56ExecAssimSlice/` (removed before yield). The campaign repo
`/home/vgpnk/Projects/shokuknow` was **read only** — no byte written there, no campaign tool run.
No tool was installed or upgraded (nothing in this item needed one). No git mutation anywhere; only
read-only `git log`/`grep`/`show`-style queries were used.

Claim under test (round-56 contract, "Assimilation: none unless package material is located and
opened this round; quarantine slice re-derived"): the mori slice of the campaign's absent-defect
register, re-derived independently of the sibling `Mo56ExecQuarantine` seat, and checked against the
2026-10-24 census note and the prior rounds' verdict files.

## 1. Slice re-derivation (the same awk, run fresh)

Register (read-only, unchanged since the round-50 pin):

```
$ sha256sum /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833
```

That digest is byte-identical to the digest pinned in
`.ufo/waves/round-50/a2w1/Mo50bScoutQuarantine.md:7`, so the register has not moved since round 50.

```
$ awk -F'|' -v l='mori' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
    /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
 S244`   the cited source could not be fetched, so no quote was checked
 S262`   the cited source could not be fetched, so no quote was checked
 S268`   the cited source could not be fetched, so no quote was checked
```

Exit code 0. **Row count: 3.** Ids: **S244, S262, S268** (all in the second table,
`## Rows whose quotes were NEVER CHECKED`). The printed id carries the register's own malformed
cell (`S244\`` — a trailing backtick where the closing `|` should be), which is why the shape of the
output looks odd; that malformation is the register's, not the awk's.

Independent cross-check with a different tool (not the awk):

```
$ grep -c '^| `mori` |' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
3
$ grep -in 'mori' <same file>   # the literal lane name occurs exactly 3 times in the whole file
3
```

Raw rows (register lines 356-358), with the two cited DOIs:

```
356:| `mori` | round1 | S244` | the cited source could not be fetched, so no quote was checked | https://doi.org/10.1145/3643916.3644413
357:| `mori` | round4 | S262` | the cited source could not be fetched, so no quote was checked | https://doi.org/10.1109/TSC.2026.3698682
358:| `mori` | round5 | S268` | the cited source could not be fetched, so no quote was checked | https://doi.org/10.1109/TSC.2026.3698682
```

Byte-identity against the prior rounds' frozen slice files (all three sha256 `8494dc0b…7349`):

```
$ sha256sum mori-slice.txt \
    mori-shokunin/.ufo/waves/round-50/assimilation/quarantine-slice \
    mori-shokunin/.ufo/waves/round-54/assimilation/quarantine-slice \
    mori-shokunin/.ufo/waves/round-55/assimilation/quarantine-slice
8494dc0b4942527cdcc724cf1550653b98be679bd811b74d20e43ce5a6207349   (x4, all identical)
$ cmp mori-slice.txt mori-shokunin/.ufo/waves/round-55/assimilation/quarantine-slice
IDENTICAL
```

So the slice is **stable across rounds 50, 54, 55 and now 56**: 3 rows, same ids, same bytes.

### Register shape facts I measured (context for the row count)

| fact | value |
|---|---|
| `## Rows` (payload-absent) data rows | 194 |
| `## Rows whose quotes were NEVER CHECKED` data rows | 109 (file prints `rows: **109**` at line 263) |
| flagged data rows in the file | 194 + 109 = 303 |
| `## By lane` rows | 19 lanes, values sum to 194 |
| lanes in `## By lane` | tabi revenger chousa kotodama tameshi game-dev-2d kake audio kagi kama kotoba souji mado kumitate game-dev-3d kasegi kengaku tsukuroi kaidoku — **mori and lore are absent** |
| mori rows in the payload table | **0** (mori appears only in the never-checked table) |
| never-checked reason cells | 78 × "the cited source could not be fetched", 31 × "the gate block named no locator" |
| id cells malformed (trailing backtick) | **109 of 109** in the never-checked table; 0 of 194 in the payload table |

## 2. Comparison with the 2026-10-24 census note (mori slice)

No file literally named "census note" dated 2026-10-24 exists in either repo (`find`/`grep` over
`shokuknow/.ufo/waves/corpus-expansion-1`, `shokunin/mori-shokunin/corpus`,
`shokunin/mori-shokunin/.ufo/waves/round-*` — no match). Three candidate referents exist and I
measured all of them; the note that actually describes the mori slice is the **round-45 lesson's
census paragraph** (`corpus/lessons/round-45.md:118-127`), which interprets the **2026-10-24 census
artifacts** that the register was generated from.

Pins for the 2026-10-24 census artifacts (mtimes are the 2026-10-24 census run):

| artifact | mtime | sha256 | size |
|---|---|---|---|
| `quote-lint-full.json` (v1) | 2026-10-24 03:32 | — | 673,939 |
| `quote-lint-full-v4.json` | 2026-10-24 06:29 | — | 776,927 |
| `quote-lint-full-v5.json` | 2026-10-24 08:05 | `403769e369393d6f5f4e1f461f54a9555f8c15c053ccc700071c46f7b368f0b3` | 863,811 |
| `absent-defect-register.md` (generated from v5) | 2026-10-24 08:37 | `5afe1810…bad833` | 83,621 |
| `census-adjudication.json` (source: quote-lint-full.json, i.e. v1) | 2026-10-24 01:25 | `1c320e5b6210bfa7c17f4f600ccf82f78ff50acf54f7e8603afb2817098a26a2` | 186,924 |

What the census says about the mori slice (measured from `quote-lint-full-v5.json`, the census the
register was built from):

```
mori findings total            : 231   (over 66 distinct ids)
mori verdict histogram         : folded 135, sweep-found 93, fetch-failed 3
mori fetch-failed ids          : [('S244','round1'), ('S262','round4'), ('S268','round5')]
mori findings carrying a 'quote' key for those 3 ids : False
mori ABSENT verdicts           : []   (mori contributes 0 rows to the payload-absent table)
census totals                  : rows 1901, quotes 4152, absent 324, fetch_failed 78
```

This **agrees exactly** with the round-45 lesson's census note, which says the census counted
"1901 rows, 4152 quotes, 78 `fetch_failed`" and that "its three mori findings are `fetch-failed`
with no `quote` key", and that the slice is "3 of the 109 never-checked rows, not 3 of the 194
absent ones". My measurements reproduce every number in that note:

| lesson claim (round-45.md:120-127) | my measurement | agree |
|---|---|---|
| census = 1901 rows | 1901 | yes |
| census = 4152 quotes | 4152 | yes |
| census = 78 `fetch_failed` | 78 | yes |
| the three mori findings are `fetch-failed`, no `quote` key | exactly S244/S262/S268, no `quote` key | yes |
| slice is 3 of the 109 never-checked rows | 3 of 109 | yes |
| slice is not 3 of the 194 absent ones | mori payload rows = 0 | yes |
| register header prints 194 absent-quote rows and 324 absent quotes | 194 / 324 (324 is a quote count, matches census `absent 324`) | yes |
| `## By lane` sums to 194 and omits the never-checked table | sum 194; mori and lore missing | yes |
| "303 flagged data rows over 19 lanes" | 303 rows ✓, but the **lane count is 21, not 19** | **no** — see finding F1 |

`census-adjudication.json` is derived from the *earlier* v1 census and its `unreadable` list holds
three rows — none of them mori (`kotodama S732`, `revenger S069` ×2). It contains no mori row at
all, so it neither supports nor contradicts the mori slice.

## 3. Prior rounds' verdict files — are the prior verdicts consistent with the register text?

Prior verdict files found (read-only):

* `mori-shokunin/.ufo/waves/round-54/assimilation/quarantine-verdicts.txt` — S244 UNVERIFIABLE,
  S262 PRESENT, S268 PRESENT.
* `mori-shokunin/.ufo/waves/round-55/assimilation/quarantine-verdicts.txt` — same three verdicts plus
  an append-only **"Correction 2026-10-27 (Mo55Scribe04 F2/F6) — S244 flip"**: S244 is PRESENT at
  the row's arXiv companion, publisher path still 403.
* `mori-shokunin/.ufo/waves/round-54/assimilation/quarantine-slice` and
  `…/round-55/assimilation/quarantine-slice` — the 3-row slice files (byte-identical to mine).
* `mori-shokunin/.ufo/waves/round-50/assimilation/quarantine-slice` — same 3 rows, same bytes
  (round 50 has no verdicts file).

**Consistency with the register text.** The register's three rows carry the prose class "the cited
source could not be fetched, so no quote was checked" and no quote cell at all (the never-checked
table has only five columns: lane, round, id, why-not-checked, cited source). So the register makes
**no absence claim** on these rows and the prior verdicts contradict nothing in it: `unreachable` is
"never checked", not "fabrication". The register's own header states this explicitly ("These are
not fabrications and they are not confirmed"). The prior verdicts are strictly *additional*
adjudications against carriers the register rows do not name.

**Independent re-verification of each verdict today (2026-10-27).** Every fetch below was run from
my scratch dir with `TMPDIR` set there; all network reads were full GETs.

S244 — the flip the round-55 file records:

```
$ curl -fsSL --max-time 40 -o s244_abs.html \
    -w 'http=%{http_code} bytes=%{size_download}\n' 'https://arxiv.org/abs/2403.18832'
http=200 bytes=41919
$ sha256sum s244_abs.html
2f302c3cb6c055452cd81d708e1e071b9fc9264681e550724e5a5d90cb771bb4
$ grep -o 'citation_doi" content="[^"]*"' s244_abs.html
citation_doi" content="10.1145/3643916.3644413"
```

Byte count and sha256 reproduce the round-55 verdict file's figures exactly, and the `citation_doi`
matches the register's cited DOI. The gate quote is present verbatim in the abstract block:
"We find that 98.9% of commits in our dataset contain sentences with rationale information" → **True**.

Publisher path for the same document, three variants:

```
$ curl -sS    -o acm_plain.html -w 'http=%{http_code} bytes=%{size_download}\n' 'https://dl.acm.org/doi/10.1145/3643916.3644413'
http=403 bytes=5471
$ curl -sSL -A '<browser UA>' -o acm_ua2.html -w 'http=%{http_code} bytes=%{size_download}\n' 'https://dl.acm.org/doi/10.1145/3643916.3644413'
http=403 bytes=5684
$ curl -sS -I -o acm_head.txt -w 'http=%{http_code} bytes=%{size_download}\n' 'https://dl.acm.org/doi/10.1145/3643916.3644413'
http=403 bytes=0
```

Body is the Cloudflare "Just a moment…" interstitial. This reproduces the round-55 correction
exactly (5,471 / 5,684 / 0 B) and confirms that the earlier "5,620-byte denial response" still does
**not** reproduce. So the S244 flip (PRESENT at the companion, publisher path unverifiable) is
**consistent** with the register row and with the round-55 verdict file.

S262 / S268 — the PRESENT verdicts, on the publisher-deposited PDF:

```
$ curl -fsSL --max-time 90 -A '<browser UA>' -o roma.pdf \
    -w 'http=%{http_code} bytes=%{size_download} type=%{content_type}\n' \
    'https://ieeexplore.ieee.org/ielx8/4629386/11644734/11540439.pdf'
http=200 bytes=2357114 type=application/pdf
$ sha256sum roma.pdf
1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2
```

Byte-identical to the digest the round-54 and round-55 verdict files pin. Both quotes are present:
S262's "Our study shows that Linux cgroups and the default Out-of-Memory (OOM) mechanism lack
sufficient container context when selecting victim processes." and S268's "It leverages eBPF to hook
into OOM-related kernel tracepoints such as mark_victim, start_task_reaping, and finish_task_reaping
to record OOM-triggering process metadata." → both **PRESENT** after de-hyphenation (and verbatim in
the plain, non-layout text extraction: S262 at line 15, S268 at lines 139-141 of a 1,405-line file —
exactly the line numbers round-48 recorded). The S262 quote also reproduces from the lane's own
committed OpenAlex copy `corpus/evidence/sources-r42/S262.oa.json` (reconstructed abstract contains
the sentence → **True**), which is the carrier the lane's S262 row declares.

The user-agent really is load-bearing, exactly as the prior rounds recorded:

```
$ curl -sSL --max-time 60 -o ielx8_noua.pdf -w 'http=%{http_code} bytes=%{size_download} type=%{content_type}\n' \
    'https://ieeexplore.ieee.org/ielx8/4629386/11644734/11540439.pdf'      # no UA
http=418 bytes=15410 type=text/html
$ curl -sSL --max-time 60 -o stamp_noua.pdf -w 'http=%{http_code} bytes=%{size_download} type=%{content_type}\n' \
    'https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber=11540439'  # no UA
http=418 bytes=15410 type=text/html
$ curl -sSL --max-time 40 -o s262_doi.html -w 'http=%{http_code} bytes=%{size_download}\n' \
    'https://doi.org/10.1109/TSC.2026.3698682'
http=202 bytes=0   (final URL https://ieeexplore.ieee.org/document/11540439/)
```

So the register's "could not be fetched" prose is still literally true of the **cited URL** today
(the DOI landing serves 202 / 0 bytes), while the quotes themselves are present in the carrier. That
is exactly the asymmetry the prior rounds recorded, and it is the reason the register's class must
not be read as a fabrication verdict.

### Second byte variant (new observation, resolves the old byte-size discrepancy)

The same document is served by two endpoints with **different bytes**, both reproducing today:

| endpoint | bytes | sha256 | `pdfinfo` pages |
|---|---|---|---|
| `…/ielx8/4629386/11644734/11540439.pdf` (browser UA) | 2,357,114 | `1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2` | 14 |
| `…/stampPDF/getPDF.jsp?tp=&arnumber=11540439` (browser UA) | 2,363,161 | `d42b2fbfbd44d859f8f0af8f6a3e26d17ae290eff079e192af65d5190a9f49fc` | 14 |

Both carry both quotes (checked: S262 and S268 sentences **True** in each variant). Round 42 pinned
the stampPDF digest, rounds 48/54/55 pinned the ielx8 digest; the 6,047-byte difference the round-42
record called "watermark/session variance" is in fact two distinct artifacts, both stable and both
reproducible today.

### Registry facts behind the slice (read-only git)

```
$ grep -c '^| S244 |' corpus/SOURCES.md   -> 0
$ grep -c '^| S268 |' corpus/SOURCES.md   -> 0
$ grep -n '^| S262 |' corpus/SOURCES.md   -> line 243 (ROMA, abstract scope)
$ git log --all --oneline -S'S244' -- corpus/SOURCES.md | wc -l -> 0
$ git log --all --oneline -S'S268' -- corpus/SOURCES.md | wc -l -> 0
$ git log --all --oneline -S'S262' -- corpus/SOURCES.md | wc -l -> 14
```

So S244 and S268 have never had a lane registry row (their content is staged as `S483` / `S507` in
`shokuknow/merge/mori/SOURCES.append.md:19,43`); S262 does have one; the lane's ROMA **full-text**
row is `S478` (`corpus/SOURCES.md:257`, 2,357,114 B, sha `1603404d…`). This matches the prior
rounds' verdicts and does not contradict them.

## 4. Answer to the seat's three questions

1. **Row count:** 3 (never-checked table; mori contributes 0 rows to the payload-absent table).
2. **Ids:** S244 (round1), S262 (round4), S268 (round5) — printed with the register's trailing
   backtick. The re-derived slice is byte-identical (sha256 `8494dc0b…7349`) to the round-50,
   round-54 and round-55 slice files, and the register itself is byte-identical to its round-50 pin.
3. **Are the prior verdicts consistent with the register text?** **Yes.** The register asserts only
   "not checked" for these three rows and carries no quote, so it is silent where the verdicts speak;
   the verdicts' PRESENT findings come from carriers the register rows do not name (arXiv companion
   for S244; publisher-deposited PDF for S262/S268). Independently re-measured today: S244 PRESENT at
   `arxiv.org/abs/2403.18832` (HTTP 200, 41,919 B, sha `2f302c3c…`, quote verbatim, `citation_doi`
   matches), publisher path still 403 (5,471 / 5,684 / 0 B, so the old 5,620-byte figure still does
   not reproduce); S262 and S268 PRESENT in the publisher PDF (2,357,114 B, sha `1603404d…`, quotes
   located on the named printed pages 3015 and 3016). No row in the slice is fabrication-class.

**Round-56 consequence:** the re-derivation is complete and stable; the L1 can land the
round-56 `assimilation/quarantine-slice` file by copying the frozen bytes (sha256 `8494dc0b…7349`,
3 rows). `.ufo/waves/round-56/assimilation/` does not exist yet, so the file is not there to be
compared against — the comparison above is against rounds 50/54/55.

## Findings

| # | severity | file / line | finding |
|---|---|---|---|
| F1 | MED | `mori-shokunin/corpus/lessons/round-45.md:122-123` | Lane-count misstatement in a committed corpus lesson: "its two tables hold **194 + 109 = 303** flagged data rows over 19 lanes". The row total (303) is right; the lane count is not — the union of lanes across the two tables is **21** (payload table 19 lanes, never-checked table 18, shared 16; `mori` and `lore` appear only in the never-checked table, `kama`/`kagi`/`kengaku` only in the payload table). "19" is the `## By lane` table's lane count, not the union. This is exactly the row-count-misstatement class the round-56 contract mines (routed defect 1). Route to round 57 as a named limit + lesson fix; do not edit the frozen counter/predicate (none involved). |
| F2 | LOW | `mori-shokunin/.ufo/waves/round-5{4,5}/assimilation/quarantine-verdicts.txt` (S262/S268 line citations) | The "quote present" reproduction is method-dependent and the cited line numbers disagree across rounds for the same artifact and quote: round-48 cites 139-141 (plain `pdftotext`, 1,405 lines), round-54 cites 121-126 and round-55 cites 123-126 (both `-layout`, 955 lines). Measured today: `-layout` puts the S268 sentence at **122-126** and the S262 sentence at **17-22**; the raw `-layout` text does **not** contain either quote as a contiguous substring (hyphenation and the two-column layout split them) — a literal `grep -F` against the layout text returns a false "absent". The quotes are contiguous in the plain (non-layout) extraction and after de-hyphenation. Any re-checker must normalize, or will mis-verify. |
| F3 | LOW | `shokuknow/merge/mori/SOURCES.append.md:43` (staged row `S507`, anchor cell) | The staged row's "2 357 114 B, **4 pages**" is not a typo: `file` on that exact artifact prints `PDF document, version 1.4, 4 page(s)` because its linearized page tree exposes `/Count 4` first, while `pdfinfo` reports **14 pages**. Root cause identified; both byte variants are 14 pages by `pdfinfo`. (The round-55 file already flagged the page count as wrong; the `file`-vs-`pdfinfo` explanation was not on record.) |
| F4 | LOW | `mori-shokunin/.ufo/waves/round-5{4,5}/assimilation/quarantine-verdicts.txt`, `mori-shokunin/corpus/SOURCES.md:257` | The pinned ROMA digest is endpoint-specific: two stable, byte-different artifacts serve the same 14-page document (ielx8 = 2,357,114 B / `1603404d…`; stampPDF = 2,363,161 B / `d42b2fbf…`), both carrying both quotes. A re-pin must name the endpoint and the digest together, otherwise a reader re-fetching the other endpoint sees a "wrong" hash. Both digests reproduce today. |
| F5 | LOW | `shokuknow/.ufo/waves/corpus-expansion-1/quote-lint-full.json` (2026-10-24 03:32) vs `quote-lint-full-v4.json` (06:29) / `-v5.json` (08:05) | The mori slice's ids moved inside the same 2026-10-24 census day: the same three documents are `fetch-failed` under **S239/S257/S263** in the v1 census and under **S244/S262/S268** in v4/v5 (the register was built from v5). Re-deriving the slice against the earlier census file yields different ids for the same rows; an id-based cross-check between census generations will look like a mismatch when nothing changed. |
| F6 | LOW | `shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (header lines 16-26; `## By lane` lines 234-255; never-checked table from line 256) | Register-header defects, re-measured unchanged (known since round 44/45, still true): the header's 194/324 describe only the first table (the file holds 303 flagged rows); the class table counts only `payload-absent`; `## By lane` omits `mori` (3) and `lore` (9), the two lanes that appear only in the never-checked table; 109 of 109 never-checked id cells are malformed (`S244\``), so a strict cell parse returns an empty slice; the "324" is a quote count (census `absent 324`), not a row count. Register is read-only for the lane — no fix attempted. |
| F7 | LOW | `mori-shokunin/.ufo/waves/round-56/` (no `assimilation/` directory) | The round-56 contract requires the quarantine slice to be re-derived; `.ufo/waves/round-56/assimilation/quarantine-slice` does not exist yet. The bytes are settled and stable (sha256 `8494dc0b…7349`, 3 rows) and can be landed by the L1 by copy; nothing was written by this seat outside its own report. |
| F8 | INFO | `mori-shokunin/corpus/SOURCES.md` (rows for S244/S262/S268) | Registry-side fact behind the slice, consistent with the prior verdicts: S244 and S268 have no `SOURCES.md` row in any commit reachable here (`git log -S` → 0 each; their content is staged as S483/S507 in `shokuknow/merge/mori/SOURCES.append.md`), S262 does (`corpus/SOURCES.md:243`), and the lane's ROMA full-text row is S478 (`corpus/SOURCES.md:257`). The register's slice ids are therefore partly *staging* ids and should not be read as lane registry rows. |

No fabrication-class row exists in the mori slice; nothing in this seat's evidence changes any
frozen counter, predicate, control or kill rule, and no corpus, tool, registry or campaign byte was
modified.
