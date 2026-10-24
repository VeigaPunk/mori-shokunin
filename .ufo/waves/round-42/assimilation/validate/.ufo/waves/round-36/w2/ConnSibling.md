# ConnSibling — sibling-overlap scan for the 16 new source rows (S205–S220)

Seat: `ConnSibling` (mori round 36, wave 2, attempt 2). Attack: **absorption/overlap** — URL and
scope comparison of the 16 rows landed at tip `bf0df77fee4b6ef54a90aea09335c7617f125151`
(`mori-shokunin/corpus/SOURCES.md:211-226`) against the sibling corpora (tsukuroi, kumitate,
chousa, kake, kotoba — all read-only), with a fleet-wide extension for context. Per kaika
practice, exact-URL sharing means a row is **not merged but noted** — this report is that note.

No tools installed or updated. Scratch: `/fast/scratch/hyaku/mori-r36/ConnSibling/`
(`sweep.py`, `sweep2.py`). The lane repo was only read; this report is the only lane file written.

## Method

1. Row bytes: `read mori-shokunin/corpus/SOURCES.md:211-226:raw` — S205 fleet CORPUS.md contract;
   S206 RFC 6585; S207 jj git-compatibility (`docs.jj-vcs.dev/latest/`); S208 NIST SP 800-122;
   S209 RFC 8785 (JCS); S210 git-rev-parse(1); S211 PMC Nosek mirror (rejected); S212–S219 Linux
   v7.2 block-accounting (stat.rst, iostats.rst, part_stat.h, blk-core.c, blk-mq.c, blk_types.h,
   commits b6866318/bdca3c87 .patch); S220 sysstat iostat.c v12.8.0. 17 distinct URLs.
2. Exact-URL intersection, all 20 sibling lanes' `corpus/SOURCES.md` (script
   `/fast/scratch/hyaku/mori-r36/ConnSibling/sweep2.py`; extracts every `https?://` URL from every
   `| SNNN |` row and intersects with the 17 target URLs):
   ```
   EXACT S211 <-> kaidoku-shokunin S068 @ kaidoku-shokunin/corpus/SOURCES.md:74 :: https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/
   EXACT S210 <-> kumitate-shokunin  S031 @ kumitate-shokunin/corpus/SOURCES.md:44  :: https://git-scm.com/docs/git-rev-parse
   EXACT S207 <-> souji-shokunin     S051 @ souji-shokunin/corpus/SOURCES.md:71     :: https://docs.jj-vcs.dev/latest/git-compatibility/
   EXACT S210 <-> souji-shokunin  S079/S091/S099 @ souji-shokunin/corpus/SOURCES.md:99,111,119 :: https://git-scm.com/docs/git-rev-parse
   EXACT S210 <-> tabi-shokunin   S052/S065 @ tabi-shokunin/corpus/SOURCES.md:66,79  :: https://git-scm.com/docs/git-rev-parse
   EXACT S207 <-> tameshi-shokunin S061/S076 @ tameshi-shokunin/corpus/SOURCES.md:70,85 :: https://docs.jj-vcs.dev/latest/git-compatibility/
   EXACT S210 <-> tameshi-shokunin S062 @ tameshi-shokunin/corpus/SOURCES.md:71     :: https://git-scm.com/docs/git-rev-parse
   exact_hits= 11
   ```
   Restricted to the five named corpora, the only exact hit is **S210 ↔ kumitate S031**.
3. Near-URL (same document, different URL form), same script plus targeted greps:
   ```
   NEAR[jj git-compat]  S207 <-> kumitate S066 @ kumitate-shokunin/corpus/SOURCES.md:79  :: raw.githubusercontent.com/jj-vcs/jj/v0.45.1/docs/git-compatibility.md
   NEAR[jj git-compat]  S207 <-> kaidoku  S036 @ kaidoku-shokunin/corpus/SOURCES.md:42  :: docs.jj-vcs.dev/v0.45.1/git-compatibility/ (+ raw tag URL)
   NEAR[jj git-compat]  S207 <-> tabi  S049/S055 @ tabi-shokunin/corpus/SOURCES.md:63,69 :: docs.jj-vcs.dev/v0.45.1/git-compatibility/
   NEAR[rev-parse doc]  S210 <-> tsukuroi S077/S082 @ tsukuroi-shokunin/corpus/SOURCES.md:83,88 :: https://git-scm.com/docs/git-rev-parse/2.56.0
   ```
4. Topic/scope greps over each sibling corpus dir (`torvalds/linux|sysstat|iostat|diskstats|blk-core|
   blk-mq|part_stat|blk_types|block/stat|8785|6585|rev-parse|jj-vcs|800-122|PMC5856500|Nosek|CORPUS\.md|
   canonicaliz`): chousa corpus → **No matches** for `8785|JSON Canonicalization|JCS|RFC 8785|rfc8785`;
   kake corpus → zero torvalds/linux/sysstat/iostat rows; kotoba corpus → zero hits in `SOURCES.md`.

## 1. Exact-URL sharing (noted, not merged — kaika practice, mori PROVINCE.md:90)

| mori row | URL | sibling rows carrying the same URL |
|---|---|---|
| S210 (`SOURCES.md:216`) | `https://git-scm.com/docs/git-rev-parse` | **kumitate S031** `kumitate-shokunin/corpus/SOURCES.md:44` (within the five named corpora); plus souji S079 `:99`, S091 `:111`, S099 `:119`; tabi S052 `:66`, S065 `:79`; tameshi S062 `:71` |
| S207 (`SOURCES.md:213`) | `https://docs.jj-vcs.dev/latest/git-compatibility/` | **souji S051** `souji-shokunin/corpus/SOURCES.md:71`; **tameshi S061** `:70`, S076 `:85` (outside the five named corpora) |
| S211 (`SOURCES.md:217`, rejected row) | `https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/` | **kaidoku S068** `kaidoku-shokunin/corpus/SOURCES.md:74` (Nosek et al. 2018, preregistration) — outside the five named corpora |

Scopes are distinct at every hit, so no merge is indicated: kumitate S031 uses `--verify` for its
PIN unverifiable-vs-mismatch split (`kumitate-shokunin/corpus/knowledge/pinned-evidence.md:18-20`);
mori S210 teaches C2 selector→existing-commit-object resolution with the lane rule "not remote
publication, source authenticity or input-tree equality". Souji S051 scopes colocated workspaces to
keep-ref lifetime/GC; tameshi S061/S076 to HEAD meaning for worktree checks; tabi S052/S065 to HEAD
resolution. Kaidoku S068 applies Nosek to freezing counting instruments; mori S211 **rejects** the
mirror as a duplicate of mori's own S056 — the sharing is disclosed inside the row itself
(`supersedes S179 — … duplicate URL already carried in S056's source cell`). This mirrors tsukuroi's
own disclosure convention (`tsukuroi-shokunin/corpus/lessons/round-21.md:25`: "Reopening an existing
URL for a distinct narrow scope is disclosed as a duplicate URL warning, not merged history").

## 2. Near-URL duplicates (same document, different URL form)

- **S207 ↔ kumitate S066** (`kumitate-shokunin/corpus/SOURCES.md:79`): same jj git-compatibility
  document; kumitate pins tag v0.45.1 raw bytes, mori cites the `/latest/` rendered page. Also
  kaidoku S036 (`:42`, v0.45.1 docs-site + raw) and tabi S049/S055 (`:63,69`, v0.45.1). Distinct
  scopes (colocation import/export vs detached-HEAD lane rule).
- **S210 ↔ tsukuroi S077/S082** (`tsukuroi-shokunin/corpus/SOURCES.md:83,88`): versioned
  `git-rev-parse/2.56.0` URL; mori S210 records the served page as 2.56.0
  ("page last updated 2.56.0, 2026-09-28"), so the bytes are the same document generation.
- No other near-duplicates: S205's fleet raw `CORPUS.md` URL appears in no sibling registry — the
  closest same-document reliances are kake S019's **own-work audit of the kimi-shokunin skills copy**
  of CORPUS.md (local path, `kake-shokunin/corpus/SOURCES.md:27`) and kumitate QUALITY Q35 quoting
  fleet `CORPUS.md:116-118` (`kumitate-shokunin/corpus/QUALITY.md:700-701`) — same normative
  contract family, different artifact/path, no lane owns it.

## 3. Scope-overlap checks against the dispatcher's two probe directions

- **iostats/disk accounting (S212–S220) vs kake/tsukuroi ground**: zero kake corpus rows touch
  torvalds/linux, sysstat, iostats or diskstats (kake PROVINCE scopes web properties & publishing,
  `kake-shokunin/PROVINCE.md:3-6`, crawl hygiene `:22-23`). Tsukuroi's kernel rows are
  memory/OOM/PSI/btrfs/taint surfaces (`tsukuroi-shokunin/corpus/SOURCES.md:115-165,184-191`), and
  its round-26 storage-integrity entry explicitly carves mori's surface out: "It does not cover
  disk-space runway (**mori's surface**)" (`tsukuroi-shokunin/corpus/knowledge/storage-health-r26.md:9`).
  Adjacent corroboration only: tsukuroi's host capture records `sysstat-12.8.0-1` installed
  (`tsukuroi-shokunin/corpus/knowledge/kill-event-deep-r8.md:368`) — the same 12.8.0 line mori S220
  pins; no tsukuroi registry row owns iostat semantics. **No overlap, no absorption.**
- **RFC 8785 (S209) vs chousa**: chousa corpus has **no** RFC 8785 / JCS / JSON-Canonicalization
  row or mention (grep over `chousa-shokunin/corpus`: "No matches found"); its "canonicalization"
  hits are filesystem path canonicalization in the research gate. Chousa owns question framing,
  source hierarchy, citation chaining (`chousa-shokunin/PROVINCE.md:5-8`) — mori S209 uses JCS for
  hashing in its own counters. **No overlap, no absorption.**
- Remaining rows: S206 (RFC 6585/429) — no sibling row anywhere; kotoba (prompt & skill craft,
  `kotoba-shokunin/PROVINCE.md:3-6`) is untouched by mori's 429 lane rule. S208 (NIST SP 800-122)
  — no sibling row anywhere (fleet-wide sweep).

## 4. PROVINCE adjacency confirmation (no sibling-owned scope absorbed)

Against mori's Adjacent table (`mori-shokunin/PROVINCE.md:61-69`) and each named sibling's own
declaration: kumitate owns OMP task/hub orchestration (`kumitate-shokunin/PROVINCE.md:3-6,15` — its
learning registry is its own); tsukuroi owns host OS/package/systemd/boot diagnosis
(`tsukuroi-shokunin/PROVINCE.md:8-14`); chousa `PROVINCE.md:5-8`; kake `PROVINCE.md:3-6`;
kotoba `PROVINCE.md:3-6` (its census row for mori: "fleet and host observability; no split with
kotoba", `kotoba-shokunin/PROVINCE.md:61`). None of S205–S220 asserts a claim inside any of these
provinces: the shared URLs (S207/S210/S211) are tool-behavior primaries re-scoped per lane —
established multi-lane practice (six sibling rows already carry the rev-parse URL) — and the block
accounting family supports mori's own disk census (`corpus/knowledge/disk-write-rate-r33.md`, S220
`used-by`), a surface tsukuroi explicitly disclaims.

## 5. Residual notes (for the L1, not defects)

- This overlap note exists only here: no round-36 lesson/w1/w2 record or PROVINCE line yet records
  the S207/S210/S211 sibling sharing (grep of `corpus/lessons/round-36.md` and `w2/` for
  sibling/overlap/kumitate/souji/tabi/tameshi/kaidoku: no URL-sharing note). Absorb this table if
  the round report needs the kaika-practice note in a durable record.
- Intra-lane duplicate URLs are separately disclosed by the lane census (13 W04 warnings at
  `evidence/census-start.txt`; S213's S033 counterpartship is stated in its own row) — intra-lane
  registry hygiene, outside this seat's sibling scope.
- S207's `/latest/` (unversioned) URL is the only one of the 16 whose pinned document identity is
  version-by-redirect rather than tag-pinned — relevant to the C1 drift probe's re-fetch semantics,
  already covered by sibling seats (RevSupS214S217 scope), restated here only as a URL-form
  asymmetry against kumitate/kaidoku/tabi's pinned variants.

VERDICT: PASS (no defect found — no sibling-owned scope absorbed; 3 exact-URL shares and 2
near-duplicate families exist and are hereby noted, not merged, per kaika practice)
Report: .ufo/waves/round-36/w2/ConnSibling.md
