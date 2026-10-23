# ExecSecondUrls — routed round-32 defect 5 (population scope)

Seat: `MoriR33.ExecSecondUrls` (leaf executor). Assignment: build and run a small script that, for every
row of the round-32 C1 population, lists every URL in the row's source cell and classifies each
non-first URL as pinned or unpinned. No fetch, no lane write beyond this report.

## Artifacts

- Script: `/fast/scratch/hyaku/mori-r33/ExecSecondUrls/second-urls.py`
  - sha256 `997128c815e7153e213f3254ed70a5b12d772c04fac7ddf095c27dbc392962da` (3881 bytes)
- Command run: `cd /fast/scratch/hyaku/mori-r33/ExecSecondUrls && timeout 60 python3 second-urls.py`
  (exit=0; run at 2026-10-23T02:41Z UTC — the host's local clock read 2026-10-22T23:41; no network access, no writes)
- Saved committed copy used for inspection only:
  `/fast/scratch/hyaku/mori-r33/ExecSecondUrls/sources-7d382043.md`
  (sha256 `5cc930974e81fce78eb6d1abca5ec5d6b3173634f3fdaf6ebd92537109b66432`, 236 lines, from
  `git -C <lane> show 7d382043:corpus/SOURCES.md`; the script itself re-runs `git show` in-process)

## Method (as implemented, script lines refer to the file above)

- Population read from `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/c1-population.json`
  (`population`, 34 rows; `base` = 641a6e86ecc60634d215c0a47ab86c47661abf86) — script lines 60-61.
- Source text: `git -C <lane> show 7d382043:corpus/SOURCES.md`, subprocess with `GIT_DIR`,
  `GIT_WORK_TREE`, `GIT_INDEX_FILE` unset (lines 43-47, 63). Read-only; no lane mutation.
- Row parse: lines starting `| S`; cells split on `|`; cell 2 = source cell (lines 71-79).
- URL extraction: source cell split on ` ; ` then on whitespace; tokens matching `https?://` kept;
  a token is trimmed of trailing prose `;`/`,`/`.` only, and every trim is reported as a `# note` line
  (lines 85-93, 36-37).
- First token in cell order = the population URL; every later token is an "other URL" (lines 96-101).
- Pinned iff the URL contains a 40-hex commit id, or a `/vN(.N)*` path segment (`/v7.2/`, `/v262/`,
  `/v1.9.0/`), or `refs/tags` (lines 24-34).

## Full output (verbatim)

```
# population: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/c1-population.json (34 rows, base 641a6e86ecc60634d215c0a47ab86c47661abf86)
# sources: 7d382043:corpus/SOURCES.md blob=39813897608eeb272ba9e24ee2eab1a524d08ca5 sha256=5cc930974e81fce78eb6d1abca5ec5d6b3173634f3fdaf6ebd92537109b66432
# note S056: token 'https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/;' trimmed of prose ';'
S056	https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/	unpinned
S058	https://git-scm.com/docs/git-diff-tree	unpinned
S117	https://api.github.com/repos/rfjakob/earlyoom/releases	unpinned
S117	https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c	pinned
S117	https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c	pinned
S117	https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h	pinned
S117	https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/README.md	pinned
S117	https://raw.githubusercontent.com/rfjakob/earlyoom/v1.8/main.c	pinned
S117	https://raw.githubusercontent.com/rfjakob/earlyoom/v1.8/kill.c	pinned
S117	https://raw.githubusercontent.com/rfjakob/earlyoom/v1.7/main.c	pinned
S117	https://raw.githubusercontent.com/rfjakob/earlyoom/v1.7/kill.c	pinned
S128	https://man7.org/linux/man-pages/man5/proc_pid_oom_score.5.html	unpinned
S137	https://raw.githubusercontent.com/rfjakob/earlyoom/750a7c0d97bb01c1bdf126fd6bf5722da17e8998/main.c	pinned
S149	https://man7.org/linux/man-pages/man5/proc_pid_oom_score.5.html	unpinned
rows=34 multi_url_rows=6 other_urls=14 pinned=9 unpinned=5
```

Tabs separate the three fields on every data line (`id<TAB>url<TAB>class`).

## Findings (facts, each with its evidence)

1. All 34 population ids resolve to a source row at `7d382043:corpus/SOURCES.md`; the script emitted no
   `# MISSING` and no `# FIRST-MISMATCH` line, so the first URL token of each cell equals that row's
   population URL. Evidence: output above; `git show` text has 179 `| S` rows and no duplicate id
   (`# duplicate ids` absent).
2. 6 of 34 rows cite more than one URL in the source cell: S056, S058, S117, S128, S137, S149.
3. 14 other URLs exist in total; 9 are pinned (8 from S117: `v1.9.0` ×4, `v1.8` ×2, `v1.7` ×2; 1 from
   S137: the 40-hex `750a7c0d97bb01c1bdf126fd6bf5722da17e8998` raw file), 5 are unpinned
   (S056 PMC full text, S058 git-diff-tree(1), S117 releases API feed, S128 oom_score(5) page,
   S149 oom_score(5) page).
4. One other URL needs a reading decision, recorded rather than silently normalized: S056's second URL
   token is `https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/;` — the `;` is prose punctuation closing
   a parenthetical, not part of the URL (source cell verbatim, `sources-7d382043.md` line 62:
   `... (full text via https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/; pnas.org HTTP 403 on 2026-10-21)`).
   The script trims it and prints a `# note`; the classification (unpinned) is the same either way.
5. The unpinned other URLs are exactly the ones the population selector could not have excluded through
   the cited URL: S117's `api.github.com/.../releases` feed, S056's PMC mirror, S058's `git-diff-tree`,
   and the `oom_score.5.html` companion pages of S128/S149. Whether those companions are in scope for
   the population's own claims is the L1's call, not mine; the script only reports them.
6. Nothing was fetched: the script performs exactly one subprocess call pair (`git show`,
   `git rev-parse`) and no network call; verified by reading the script and by the `#` header lines it
   printed (blob id `39813897608eeb272ba9e24ee2eab1a524d08ca5`, text sha256
   `5cc93097...b66432`, matching my independent `git show`-to-file sha256).

## Risks / limits

- The script's pinned test is a URL-shape test, not a resolvability test: `/vN(.N)*/` would also mark a
  directory literally named `v1` as pinned, and a bare `refs/tags` mention anywhere in the URL counts.
  No other URL in this population hits either edge ([INFERENCE] from the 14 printed URLs).
- Classification reads the source cell only; `scope`, `anchor` and `teaches` cells mention further URLs
  (e.g. S149's `kernel/fork.c`), which are not "URLs in the source cell" and are deliberately not
  listed. If the L1 wants those, that is a different extraction rule.
- The evidence binds to commit `7d382043`; a later SOURCES.md revision may add or remove other URLs.
- No tool install or update was needed (nothing installed; no pacman/uv/npm/cargo call made).
- No blocker. Reproducible in one command from the script path above.
