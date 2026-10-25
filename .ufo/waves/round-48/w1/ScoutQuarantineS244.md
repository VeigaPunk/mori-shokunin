PRESENT — the staged S244 source is the same document currently staged as S483, and its abstract grounds the 98.9% rationale claim.

## Evidence

- Register: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`, line 356, records `mori / round1 / S244` and DOI `https://doi.org/10.1145/3643916.3644413` as not fetched. `quote-lint-full-v5.json` finding for that lane/round/id is `verdict: fetch-failed` with the DOI as detail.
- Staged append: `/home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md` has no row numbered S244. Its row S483 (line 19) names the identical DOI and the arXiv preprint, and teaches that 98.9% of dataset commits carry rationale sentences. Upstream history confirms the renumbering: `git show 9e91e504:lanes/mori/SOURCES-PROPOSED.md` shows this DOI at S244; current staging identifies it as S483. These are the same paper/document, with an ID change.
- Lane registry: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` has no S244 row (S244 is a gap); it also has no row for this DOI. Thus there is no current lane S244 row to compare. IDs are not transferable between this registry and the staged package.
- Fetch: `read https://arxiv.org/abs/2403.18832` returned the paper abstract, including: “We find that 98.9% of commits in our dataset contain sentences with rationale information.” This directly grounds the quantitative part of the staged teaches statement. `read https://doi.org/10.1145/3643916.3644413` resolved through Crossref to the same title, authors, publisher, and DOI; Crossref response says no abstract available. The successful arXiv fetch resolves the prior fetch failure; no fabrication finding is supported.

## Commands / outputs

- `grep -n 'S244' /home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md` — no match (exit 1).
- `grep -c 'S244' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` — `0` (exit 1).
- `git show 9e91e504:lanes/mori/SOURCES-PROPOSED.md | grep -n '3643916'` (in `/home/vgpnk/Projects/shokuknow`) — line 52 identifies the paper at S244 (exit 0).
- `read` of arXiv and DOI URLs — successful; responses above (the reader device does not expose a shell exit code).
