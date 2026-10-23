# ReviewSecondUrls — wave-2 falsification of routed item 5 (§5 "Second URLs outside the round-32 population")

Scope: re-derive `.ufo/waves/round-33/evidence/second-urls.py`, compare with `second-urls.txt`, independently
check all cells of the 34 population rows in `SOURCES.md@7d382043` for missed URLs (incl. `...` abbreviations
like S060's), verify pinned/unpinned calls, confirm/refute lesson §5 (`corpus/lessons/round-33.md:105-112`).

Verdict: **§5 refuted in part.** The script reproduces byte-identically and all 14 listed classifications are
correct, but the census misses **two URLs inside the 34-row population** — both in `anchor` cells, which the
script never reads — so `other_urls=14`, `unpinned=5`, `multi_url_rows=6` and §5's "five unpinned ones"
enumeration are all wrong row-wide. Row S051 is genuinely unpinned and silently extends the must-count set.

## Findings

### F1 (major) — S051's anchor-cell URL missed; genuinely unpinned; §5's "five unpinned" is six

- Attacks: `corpus/lessons/round-33.md:108-110` ("`other_urls=14 … unpinned=5`. The five unpinned ones … are
  what a future freshness claim must count").
- Evidence: `SOURCES.md@7d382043:57`, row S051, `anchor` cell (column 6): "…April 2010 final, document
  history 04/06/10; landing page `https://csrc.nist.gov/pubs/sp/800/122/final` opened 2026-10-21". This URL
  names a fetched page ("opened 2026-10-21") yet is absent from `second-urls.txt` because `second-urls.py:69`
  keeps only `parts[1]` (the `source` column).
- Classification check: under the script's own rules (`second-urls.py:34-41`: 40-hex, `/vN/` path, `refs/tags`)
  it is **unpinned** — `/final` is a prose path segment, not `/vN/`. Verified by replaying `pinned()`. So the
  row-wide truth is `other_urls≥15`, `unpinned≥6`, and S051 joins the freshness must-count set. `multi_url_rows`
  is 8 row-wide (S051 and S149 each have a second named page outside cell 1), not 6.

### F2 (major) — S149's anchor-cell gitweb URL missed; classifier lacks a query-param pin rule

- Attacks: same §5 census (`round-33.md:108`) and `second-urls.txt` completeness.
- Evidence: `SOURCES.md@7d382043:155`, row S149, `anchor` cell: "…man-pages 6.20 carries the same four
  statement blocks … at
  `https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_oom_score_adj.5?id=man-pages-6.20`
  (4,212 B, sha256 16a0d4b50deca2828d840350262d936f70934272a276b96c750af…)". Absent from `second-urls.txt`.
- Two defects in one: (a) the URL is a named page whose bytes are sha256-recorded in the cell — exactly the
  freshness surface item 5 wants counted, yet uncounted; (b) had the script seen it, `pinned()` would call it
  **unpinned** (replay: no 40-hex, no `/vN/`, no `refs/tags`), but `?id=man-pages-6.20` is a tag reference —
  semantically pinned. The classifier has no rule for gitweb `?id=<tag>` pins, so any future inclusion of this
  URL via the same rules would miscount the unpinned set a second way.

### F3 (minor) — §5 presents source-cell output as a row census without stating the column scope

- `second-urls.py:4-7` docstring honestly says it reads "the row's source cell (cell 2)"; the lesson text
  (`round-33.md:105-112`) never restates that restriction, so a later reader takes `other_urls=14` as
  "all URLs the 34 rows name". F1/F2 show that reading is false. One-word fix existed ("…in the source
  cell…"). Also note `?id=` and S051's landing page live in `anchor`, a column R-R's support rule does not
  use — so this is a *freshness* (item-5) gap, not an R-R support gap.

### Confirmed correct (no defect)

- **Reproducibility**: `timeout 60 python3 .ufo/waves/round-33/evidence/second-urls.py` output `diff -u`
  against `second-urls.txt` → identical, byte for byte (incl. all `#` diagnostics). Script sha256
  `997128c815e7153e213f3254ed70a5b12d772c04fac7ddf095c27dbc392962da` matches §5's `997128c8…`.
- **All 14 listed classifications correct** under the stated rules: 9 pinned (S137's 40-hex `750a7c0d…`,
  S117's `/v1.9.0/`, `/v1.8/`, `/v1.7/` paths — `TAGPATH_RE` requires trailing `/` or EOS, correct for all
  nine), 5 unpinned (S056 PMC mirror, S058 git-diff-tree, S117 releases feed, S128/S149 `oom_score.5`).
- **No missed URLs inside source cells**: exhaustive re-scan of all 11 columns of all 34 rows found zero
  `...`-abbreviations (S060-style), zero `www.`/schemaless URLs, zero embedded `;https`/`(https` tokens, zero
  markdown-wrapped URLs, no duplicate ids, no missing rows, and every row's first source-cell URL equals its
  population `url` (no `# FIRST-MISMATCH`/`# MISSING` diagnostics — verified). S117 anchor has abbreviated
  *commit hashes* (`08656b0b…f9d0e4`), not URLs.
- **S060**: absent from the 34-id population (`c1-population.json` lists S058, S117, S128, S137, S149;
  S060 not among them) — §5's S060 paragraph is accurate and consistent with wave-1 ScoutRoutedLedger G5;
  its `blob/main` in-toto URLs are correctly named there as unpinned.
- **§5 "re-opened this round (§1)"**: `corpus/evidence/recheck-r33/` contains `S058-difftree-r33.src` and
  `S128-S149-oom_score.src`, and §1 rows S058/S128/S149 (`round-33.md:58,60-61`) cite them — claim holds.
- **§5 script path honest**: cites the scratch path plus committed output — both verified above.

## Checks run

1. Rerun + `diff -u` vs committed txt → identical.
2. Independent parse: `git show 7d382043:corpus/SOURCES.md`, split all 34 rows to 11 cells each, regex-scan
   every cell for `https?://`, `www.`, bare domains, `...`/`…` tokens → only F1/F2 URLs outside cell 1.
3. Replayed `pinned()` on both missed URLs; reviewed `TAGPATH_RE`/`SHA40_RE` semantics.
4. Verified population membership, first-URL equality, recheck-r33 copies, script sha256.

## Residual risk / gaps

- If the lane's freshness convention is later defined as "source cell only", F1/F2 degrade to the wording
  nit in F3; the routed item's wording ("the other unpinned URLs … a freshness claim must name and count")
  does not state that restriction, and S051's anchor explicitly records an open date for its landing page.
- S149's scope cell says the contract is "as served from man-pages 6.19" while the anchor cites the 6.20
  gitweb copy with a recorded sha256 — internally consistent (6.19 is the served page, 6.20 a comparison),
  but worth a note if a freshness claim ever re-opens the anchor URL.
- Tooling: none installed; stock python3/git sufficient (RULES.md read).
