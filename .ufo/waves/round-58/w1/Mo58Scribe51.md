# Mo58Scribe51 — round-58 absent-defect-register slice: re-derivation and hand-check

**Result: the mori slice is still exactly 3 rows (S244, S262, S268); 0 of 3 is
`payload-absent` and none is a fabrication, and today 0 of 3 is *unreachable* —
all three works are readable through a DOI-linked carrier. Two were verified
byte-identically against the publisher's deposited PDF; the third is verified
against the DOI-declared arXiv preprint while the ACM version-of-record stays
behind a 403.** No corpus, registry, SCORECARD, LOG or VCS write was made.

Scope: re-derive the slice from the external campaign register, then hand-check
(a) whether the *cited source* is reachable from this host today and (b) whether
a located quote from each work exists verbatim. Distinguish `absent` (source
contains no such text) from `unreachable` (checker could not reach the source).
Draft/review note only — the lesson §Quarantine slice text is below, uncommitted.

## 1. Slice identity (re-derived, read-only)

Register: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`,
sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`
(unchanged from the round-50/round-56 records). The slice lives in
**`## Rows whose quotes were NEVER CHECKED`**, data lines 356–358:

```
356 | `mori` | round1 | S244` | the cited source could not be fetched, so no quote was checked | https://doi.org/10.1145/3643916.3644413
357 | `mori` | round4 | S262` | the cited source could not be fetched, so no quote was checked | https://doi.org/10.1109/TSC.2026.3698682
358 | `mori` | round5 | S268` | the cited source could not be fetched, so no quote was checked | https://doi.org/10.1109/TSC.2026.3698682
```

`mori_rows=3`; the same `awk` slice prints 3 rows today. The section preamble
itself says: *"These are not fabrications and they are not confirmed. The
checker could not reach the source, so it never attempted a match"* — and the
table has **no quote column**. This matters for the wording of any lesson text
(see §4, F3).

## 2. Verdicts after reopening the sources (2026-10-27, this host, this seat)

| row | cited endpoint today | carrier actually read | located quote (hand-checked) | verdict |
|---|---|---|---|---|
| S244 | `https://doi.org/10.1145/3643916.3644413` → `dl.acm.org` **403** (Cloudflare) | arXiv `2403.18832v1` full text, 1,420,568 B, sha256 `ab8ab195…b6018e`, 11 pp.; arXiv metadata declares `<arxiv:doi>10.1145/3643916.3644413`; OpenAlex work record for the DOI carries the same abstract | `We find that 98.9% of commits in our dataset contain sentences with rationale information` — p. 1 abstract, extraction line 29 (1437-line dump) | **PRESENT via DOI-matched preprint; version-of-record UNREACHABLE** (not absent, not fabrication) |
| S262 | `https://doi.org/10.1109/TSC.2026.3698682` → `ieeexplore.ieee.org/document/11540439` **202, 0 bytes** | publisher-deposited PDF `ielx8/4629386/11644734/11540439.pdf`, **HTTP 200**, 2,357,114 B, sha256 `1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2` — byte-identical to the sha256 in `SOURCES.md:257` (S478) | `Our study shows that Linux cgroups and the default Out-of-Memory (OOM) mechanism lack sufficient container context when selecting victim processes.` — printed p. 3015 = PDF p. 1, Abstract, default-mode lines 14–15; also verbatim in the lane-held `corpus/evidence/sources-r42/S262.oa.json` abstract | **PRESENT (full text, byte-identical copy)** |
| S268 | same DOI as S262; same 202/0-byte reader endpoint | same pins: 2,357,114 B, sha256 `1603404d…` | `It leverages eBPF to hook into OOM-related kernel tracepoints such as mark_victim, start_task_reaping, and finish_task_reaping` — printed p. 3016 = PDF p. 2, §I Introduction, lines 139–141 | **PRESENT (full text, byte-identical copy)** |

Byte-level identity, not "both fetched": the sha256 recomputed today for the
ROMA PDF equals the sha256 recorded in S478's locator cell (fetched 2026-10-25)
and in the round-54 verdict file. The arXiv PDF sha256 likewise equals the
round-56 record.

## 3. Absent vs unreachable — the distinction this seat exists to keep

- **Unreachable.** True of the *cited endpoint* in all three cases (ACM 403;
  IEEE document reader 202/0 bytes). This is the only thing the register
  asserts, and it is a host/access fact.
- **Reachable through a DOI-linked carrier.** True of all three works today:
  two through the publisher-deposited CC-BY PDF (`ielx8/…`, 200), one through
  the arXiv preprint whose own metadata declares the cited ACM DOI.
- **Absent.** Would require a quote test against a matched carrier returning no
  span. That was never performed and is not the disposition of any of the three
  rows: all three located spans match verbatim. **No row in this slice is
  `payload-absent`, and no fabrication finding is supported.**
- **Still genuinely unverified:** S244's *version of record* (ACM ICPC 2024,
  pp. 415–425). Only the arXiv v1 (2024-02-06) was readable; whether the
  proceedings version reproduces the same sentence is untested. Label it
  "present via DOI-matched preprint", not "present in the VOR".

## 4. Findings for the lesson (each is a measured statement)

- **F1 — the lane's two line locators for the same sentences use different
  `pdftotext` modes, and only one of them is byte-faithful.**
  `round-54/assimilation/quarantine-verdicts.txt` cites "extracted lines 17–22"
  (S262) and "121–126" (S268); those are **`-layout`** line numbers and they
  reproduce exactly in `-layout` mode. `SOURCES.md:257` (S478) cites "pdftotext
  lines 139–141"; those are **default-mode** line numbers and reproduce exactly
  in default mode (S262 begins at default line 14, S268 at 139). Crucially,
  `-layout` mode splits both sentences with end-of-line hyphenation
  (`…(OOM) mech-` / `anism`, `…fin-` / `ish_task_reaping`), so a literal
  substring test against `-layout` text returns **False for both quotes**;
  default mode rejoins the words and returns **True for both**:
  `default {'S262': True, 'S268': True}` / `layout {'S262': False, 'S268': False}`.
  Round-54's *content* verdicts are right; its locators are mode-bound and its
  mode cannot support byte-faithful binding. Lesson text must name the mode
  (default), and anchor on printed page + section.
- **F2 — stale boundary phrase on S262, contradicted by the lane's own S478.**
  `SOURCES.md:243` scopes its evidence cell as "not the full text (paywalled
  from this host)". The same work's deposited full text at the `ielx8` PDF URL is
  HTTP 200 and open access (S478's row marks it CC BY 4.0), and it is
  byte-identical to S478's recorded pin. The 202-with-0-bytes behaviour belongs
  to the *document reader* endpoint (`/document/11540439`), not to the PDF.
  `corpus/SOURCES.md` is append-only, so this is reported, not edited.
- **F3 — the register's class string is an access verdict, not a content
  verdict.** All three rows sit under "Rows whose quotes were NEVER CHECKED",
  whose text disclaims fabrication and confirmation, and whose table has no
  quote column. Lesson wording must say "unreachable at check time; re-derivable
  today", never "absent" or "the quote is not in the source".
- **F4 — malformed id cells persist.** 3/3 slice id cells render as ``S244` ``,
  ``S262` ``, ``S268` `` (trailing backtick), so a strict `^\| S\d+ \|` parse of
  that table yields an empty slice; a backtick-tolerant parse yields exactly the
  3 expected rows. Known since round 45; still true today.
- **F5 — campaign IDs are not lane IDs; two of the three contents are already
  committed under other IDs.** `corpus/SOURCES.md` today has **no** S244 row and
  **no** S268 row; the same works are `S262` (line 243, abstract-tier) and `S478`
  (line 257, full-text-tier — the row that already carries the S268 tracepoint
  quote). Upstream staging renumbers them S244→`S483`, S262→`S501`,
  S268→`S507` (`/home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md:19,37,43`).
  Therefore this round must **not** append rows for S244/S268; the slice is a
  verdict exercise only.
- **F6 — S244 supports two independent carriers.** OpenAlex's abstract for the
  cited DOI *and* the arXiv v1 abstract both contain the 98.9 % sentence, so the
  preprint route is not a single-source coincidence.

## 5. Draft text for `corpus/lessons/round-58.md` — `### Quarantine slice` (uncommitted)

> The round-58 absent-defect-register slice is S244, S262 and S268 (register
> sha256 `5afe1810…bad833`, data lines 356–358, section "Rows whose quotes were
> NEVER CHECKED" — an access class, not a content class). All three were
> re-opened on 2026-10-27. None is absent and none is a fabrication:
> S262 and S268 are **present** in the publisher-deposited ROMA PDF
> (`ielx8/4629386/11644734/11540439.pdf`, HTTP 200, 2,357,114 bytes, sha256
> `1603404d…6add2`, byte-identical to the pin in `SOURCES.md:257`), S262's
> abstract sentence at printed p. 3015 and S268's tracepoint sentence at printed
> p. 3016; S244 is **present via its DOI-matched arXiv preprint**
> (`2403.18832v1`, 1,420,568 bytes, sha256 `ab8ab195…b6018e`, arXiv metadata
> declares `10.1145/3643916.3644413`) while the ACM version of record still
> answers 403 from this host, so the VOR sentence remains untested. The cited
> endpoints themselves remain unreachable to an automated client (ACM 403; IEEE
> document reader 202 with 0 bytes). No campaign file was edited; no lane row
> was added (S244/S268 are gaps in `corpus/SOURCES.md`; their content is already
> carried by S262 and S478).

Access/share line for the wave report: Attack share unaffected; this seat is a
scribe (non-attack), producing no votes.

## 6. Limits

- Fetch results are host- and UA-specific; the `read`-tool route was not used as
  the only witness — every claim above comes from a shell `curl` with an
  explicit `%{http_code}`/`%{size_download}` receipt.
- No network egress check beyond the four endpoints named; no proxy variation
  attempted.
- The ROMA PDF was not committed anywhere; identity rests on the recomputed
  sha256 versus the cell recorded in S478. The arXiv PDF is likewise scratch-only.
- Nothing here scores C1 or C2; neither counter reads the quarantine slice.
- No tool installation or upgrade occurred; `pdftotext`/`pdfinfo` were already
  present (poppler 26.08.0). Pacman was not invoked.

## 7. Reproduction

Commands, byte counts, shas and line anchors are in
`.ufo/waves/round-58/w1/Mo58Scribe51-receipts.txt` (copied out of scratch before
cleanup). Scratch root `/fast/scratch/hyaku/mori-r58/Mo58Scribe51` was created
explicitly, `TMPDIR` set to it, disk-guard green at start (32 % used, 552.8 G
free), and the scratch directory removed after the receipts were copied.
