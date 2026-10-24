measured 2026-10-23T12:04:38Z

# SupS179 — round-35 routed defect 2

## Findings and behavior

- The routed finding is that S179's immutable scope and teaches cells changed in place at commit `5126891`, 44 seconds after first publication at `55c3ed5` (`.ufo/waves/round-35/w2/ScoutAppendDebt.md:31`). I read both requested revisions:

```text
timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 6bd57097:corpus/SOURCES.md | grep '^| S179 '
| S179 | PMC mirror of Nosek et al. 2018 (round-32 candidate, rejected) — https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/ | paper | A | rejected candidate: the full-text mirror S056's source cell already names | — | Rejected round 32: duplicate URL already carried in S056's source cell; a mirror row would not recheck S056's URL. | rejected | 2026-10-23 | 365d | — |

timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 55c3ed5:corpus/SOURCES.md | grep '^| S179 '
| S179 | PMC mirror of Nosek et al. 2018 (round-32 candidate, rejected) — https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/ | paper | A | rejected candidate: same work as S056 | — | Rejected round 32: same article as S056; a mirror row would not recheck S056's URL. | rejected | 2026-10-23 | 365d | — |
```

- I reopened the tip URL by ordinary curl, without a challenge: `timeout 120s sh -c 'mkdir -p /fast/scratch/hyaku/mori-r36/SupS179 && curl --location --silent --show-error --max-time 105 --output /fast/scratch/hyaku/mori-r36/SupS179/S179.src --write-out "HTTP_STATUS=%{http_code}\n" https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/ && sha256sum /fast/scratch/hyaku/mori-r36/SupS179/S179.src'` → `HTTP_STATUS=200`; SHA-256 `a4e104ec9d6da304cc642346112b6f450dd2e4ef45d1a8e43531949842f39511`. `timeout 120s stat -c 'bytes=%s' /fast/scratch/hyaku/mori-r36/SupS179/S179.src` → `bytes=196972`. The source is saved at `/fast/scratch/hyaku/mori-r36/SupS179/S179.src`.
- Tip anchor is `—`, so it names no anchor locator to test. The opened page identifies the work: quote at `S179.src:95`: `https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/`; quote at `S179.src:98`: `The preregistration revolution`; quote at `S179.src:112`: `10.1073/pnas.1708274114`. The article text at `S179.src:1448` says `In prediction, the problem of forking paths is avoided because the analytic pipeline is specified before observing the data` (19 words).
- The S056 tip source cell names this exact PMC full-text URL and the same PNAS article (command `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 6bd57097:corpus/SOURCES.md | grep -E '^\| S056 \||^\| S201 \|'`; S056 at `corpus/SOURCES.md:62`). Its S056 anchor also includes the same passage, so reopening the PMC URL did not recheck a distinct URL. The tip scope and teaches cells are supported; neither needs correction. The opened bytes support the article identity and the repeated passage; the duplicate-URL relation is confirmed by the registry, not asserted by the article itself.
- The requested row model S201 has a supersedes prefix (`corpus/SOURCES.md:207`); S073 has the same format (`corpus/SOURCES.md:79`). The required used-by path exists at tip: `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e 6bd57097:corpus/lessons/round-32.md && printf 'exists: corpus/lessons/round-32.md\n'` → `exists: corpus/lessons/round-32.md`.

## Drafts

DRAFT `corpus/SOURCES.md`:

```DRAFT corpus/SOURCES.md
| S2NN | PMC mirror of Nosek et al. 2018 (round-32 candidate, rejected) — https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/ | paper | A | rejected candidate: the full-text mirror S056's source cell already names | — | supersedes S179 — Rejected round 32: duplicate URL already carried in S056's source cell; a mirror row would not recheck S056's URL. | rejected | 2026-10-23 | 365d | corpus/lessons/round-32.md |
```

DRAFT `corpus/lessons/round-32.md` Gate row:

```DRAFT corpus/lessons/round-32.md § Gate
| S2NN | https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/ | 2026-10-23 | a4e104ec9d6da304cc642346112b6f450dd2e4ef45d1a8e43531949842f39511 | S179.src:95 canonical URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/; S179.src:98 title: The preregistration revolution; S179.src:112 DOI: 10.1073/pnas.1708274114; S179.src:1448 article text (19 words): In prediction, the problem of forking paths is avoided because the analytic pipeline is specified before observing the data | reject, duplicate URL: S056's source cell already names this mirror URL at corpus/SOURCES.md:62 |
```

VERDICT: supported

## Gates, surfaces, limits

- Gate decision remains `reject` because S056 already carries the PMC URL, while the opened page confirms the same article via its title and DOI (`corpus/SOURCES.md:62`; `S179.src:95,98,112`). Its quoted body passage is present at `S179.src:1448`.
- Touched surfaces: this report and `/fast/scratch/hyaku/mori-r36/SupS179/S179.src` only. No source row, lesson, contract, code, judge, index, or repository metadata was edited. No tools were installed.
- Out of scope: source admission or changing S179's rejected status; this assignment asks for a superseding rejected row. No tests or checks beyond the listed source read, URL fetch, digest, and tip-path check were run.
- Artifacts: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/w1/SupS179.md`; `/fast/scratch/hyaku/mori-r36/SupS179/S179.src` (SHA-256 above).
