# HistoryCleanup — round 21

**Scope:** Offline read-only review of the souji receipts cited by `mori-shokunin/PROVINCE.md:89`, and the round-21 correction at `:183-190`. No census, source edit, or sibling write was performed.

## Finding

**C1 freshness:** the two baseline identities `aggregator-r10` and `aggregator-r10-resume` have per-path removal receipts for 18 artifacts. The evidence supports recording those exact artifacts as swept with a `pushed` receipt; it does **not** support either wave's settlement or an independent cleanup disposition. Keep both wave observations unresolved and the pin BLOCKED while disposition is unknown.

**C2 calibration:** this is the `loss-cleanup-only` case, not independent disposition: the cleaner, deletion author, original-approval-list author, and later sweep-receipt author all resolve to `souji-shokunin`. A `pushed` receipt is evidence about safe removal/recoverability, not a wave lifecycle decision.

## Receipt chain and attribution

- `mori-shokunin/PROVINCE.md:89` describes the exact scope correctly: hashed `aggregator-r10*` artifacts in the approval list, with those exact paths marked `pushed` by the later sweep. Its round-21 erratum (`:183-190`) narrows the meaning: the pushed receipt establishes removal-safety/recoverability only; the old artifacts and the later empty-at-inspection observation do not establish independent lifecycle closure.
- Current souji scope is `souji-shokunin/PROVINCE.md:7-17,50-52` (hygiene/removal-list proposals; liveness/resource findings route to mori). The adjacency quote still present at `mori-shokunin/PROVINCE.md:69` is historical/stale relative to those current lines. Souji `SKILL.md:35,49` defines `pushed` as a safe-to-remove receipt: the path existed for the check, its introducing commit was an ancestor of the resolved default remote ref, and no unpushed commit touched it; `SAFE(pushed)` is removable after quarantine. Neither definition says the wave was settled, reported, or accepted.
- `souji-shokunin/census/round-3/operator-approval-list.tsv:56-73` is in commit `36746332cab0617c1ef23a63fee727c8869bd25e`, authored and committed by `souji-shokunin <souji@shokunin.local>` at `2026-10-18T13:49:06-03:00`. Its 18 rows record paths, byte sizes, SHA-256 values, and the introducing commit prefix `b2f2efae7549` with `origin/master ... ancestor=yes`.
- The fleet-root deletion is commit `e20f4fa3fd3fc9550641af38da3eddcf3d35f528`, authored and committed by the same souji identity at `2026-10-18T23:58:39-03:00`. `git show --name-status` for the two wave directories reports exactly 18 `D` entries, matching the receipt paths below: 10 under `aggregator-r10-resume`, 8 under `aggregator-r10`.
- The later per-path `pushed` list (`souji-shokunin/census/operator-sweep-20261018/approval-list.tsv:56-73`) and corresponding verdicts (`.../resume-verdicts.tsv:52-69`, each `SAFE pushed`, `snapshot=equal clean=yes`) are in commit `2f303dc6e30d7650e1e513e3cbad75412efdc353`, again authored and committed by `souji-shokunin <souji@shokunin.local>`, at `2026-10-19T00:02:43-03:00`—4m04s after the deletion commit. This proves post-deletion publication of those later per-path records, not by itself when their checks ran. Separately, the deletion commit message claims 96/96 SAFE were re-derived at decision time and the second check passed. Both records remain souji-authored; neither is a non-souji wave disposition.
- The retained `removal-metadata.txt` is a mori evidence copy of the deletion commit metadata. The underlying souji-authored commit message claims “operator approval” via the original approval list and an operator directive, but it does not identify an independent operator-authored per-wave disposition. Whether a separate operator record exists outside the public lane artifacts remains **unknown**. No private session material was inspected.

## Exact per-path records

The SHA-256 values below are those **recorded by the original souji approval list** (not re-hashed from the deleted live paths). Every listed path is `pushed` in the later sweep approval list and has a `SAFE pushed` verdict with `snapshot=equal clean=yes` in the verdict file.

| Fleet-root path | Recorded SHA-256 |
|---|---|
| `.ufo/waves/aggregator-r10-resume/before.json` | `671514a0cb0c478e2ce3872324c59a5c93f4b29e7f81adade5bf2e9c9204f749` |
| `.ufo/waves/aggregator-r10-resume/CONTEXT.md` | `5be992e7b2ee4ed500bd411c251b6a371df36ca25285945365f6113b66c52b` |
| `.ufo/waves/aggregator-r10-resume/critic.md` | `d0ff266dfae1b34fb473d10485dc8e3232a2442c3447ae0291b6c670ca573cfa` |
| `.ufo/waves/aggregator-r10-resume/dispatch.json` | `76de24c48661c643b5fb12e1a724ee27a152f8e15d38b9c750600a8d8788d6cb` |
| `.ufo/waves/aggregator-r10-resume/evidence.md` | `5e606a9e5c5b6a7be2e724cf4c641925bb903f94200f14ff96659247a54a60f1` |
| `.ufo/waves/aggregator-r10-resume/measure-corpus.mjs` | `fefbf2ff9f0aa29c25daa16696a269182c0491572aac6276ced42325bd7bbf9c` |
| `.ufo/waves/aggregator-r10-resume/plan.md` | `6d119a4361e024c6dbbb5d36c7a4195e8a551e7e7fbf24e4e4cf255e696b8147` |
| `.ufo/waves/aggregator-r10-resume/preservation-pins.json` | `5463a068998ee64979f9be9cc96bb794c99c95d6383e13876b6d9e0abc88d0d5` |
| `.ufo/waves/aggregator-r10-resume/selection.md` | `7a81e775e3368c1c819cf925b83a39bcd002108f548776dff79181c685953f29` |
| `.ufo/waves/aggregator-r10-resume/surfaces.md` | `35b86024b2ba36197803985bb5da9de7a65f84a4b3262e7eea3092acd6779225` |
| `.ufo/waves/aggregator-r10/before.json` | `afecb2fda4e1f78e01b5e3863480c75de4588228cc781278148eb8b7753f57ae` |
| `.ufo/waves/aggregator-r10/before-summaries.log` | `67bcad7f0f5b3e8bb89f2f0192beb80aaea27e6b351425520e6f9cceabcd7241` |
| `.ufo/waves/aggregator-r10/count-before.log` | `3ae886073ed84a576ee079961317607912cb5c1488b2a91762bdaab6a9fdf3e3` |
| `.ufo/waves/aggregator-r10/dispatch.json` | `b95403311981fb91d5a17c7bd07d99e5a3a4acbfb1aa2ba20fb64bb8f9943de1` |
| `.ufo/waves/aggregator-r10/seats/critic.md` | `6ce3f3a0d62783068d19d14825fec8fbb1fad729788aee0a9d5fcebe4b0838e1` |
| `.ufo/waves/aggregator-r10/seats/plan.md` | `e55d23b5b3e8766ab40e9f971b63d18cc37622af0310a43486f1efb64ba82f49` |
| `.ufo/waves/aggregator-r10/seats/scout.md` | `da3dfd1d46efede947414ed747cebc64d268f930ba678c96270397da8f115b99` |
| `.ufo/waves/aggregator-r10/seats/scribe.md` | `b102bf65e0b534c6dd20e776d82ad5c53e962b74b69bca06ad57f33e2277e245` |

## Exact accounting provenance and remaining unknown

Round-21 `contract.md:13-14` requires `baseline`, `deletion`, and `cleanup` provenance as `{path, revision, sha256}` for retained rows; `disposed` additionally requires independent evidence, `independent:true`, an actor distinct from cleanup, an explicit wave ID, and disposition `settlement` or `cleanup-accounted`. The following own-lane committed copies are available for retained accounting:

| Provenance | Own-lane evidence-copy path | Copy revision | Copy SHA-256 | Source identity recorded in copy |
|---|---|---|---|---|
| baseline | `corpus/evidence/baseline-r10-20261015T2231Z.json` | `e9f340ce986f82a60baad1b8e5ead655ab818a1c` | `0993b23505deab2aeb05b2309bdf7dd6eaad2b82f27852491352511aa9670478` | r10 baseline |
| deletion | `.ufo/waves/round-21/evidence/removal-metadata.txt` | `a8442a018aa9c51b21b92c3ce3b17736317375b1` | `4276625be64ab1943bb5781dab7a3d9e8c912bdb48ea562870f20b70b753263e` | fleet deletion `e20f4fa3fd3fc9550641af38da3eddcf3d35f528`; actor souji |
| cleanup | `.ufo/waves/round-21/evidence/cleanup-receipts.tsv` | `a8442a018aa9c51b21b92c3ce3b17736317375b1` | `46f84c3a60ac701ec7d0c16523e5bbfa999be3999cb61029be8fba50785970a7` | souji source `census/operator-sweep-20261018/approval-list.tsv`, revision `2f303dc6e30d7650e1e513e3cbad75412efdc353`, source SHA-256 `550da61f5da587b4d09b826259f49978c826f3cbe2ed8440b86c413251d45715`; 18-row projection |

Supporting souji source digests: original `census/round-3/operator-approval-list.tsv` at revision `36746332cab0617c1ef23a63fee727c8869bd25e` = `0a33e223ecf8439a823324e6775bd0f3b6a6c17b5e1eb98d05ee55a283e107f8`; later `census/operator-sweep-20261018/resume-verdicts.tsv` at revision `2f303dc6e30d7650e1e513e3cbad75412efdc353` = `47f90aea6f0e01b548f52469a9cd8916452ed9a8d9ceee882e3f966be299444f`. `historical-provenance.json` (own-lane revision `a8442a018aa9c51b21b92c3ce3b17736317375b1`) has SHA-256 `0f398d0033ad2c3a8c2f1786ab5cd81a05094ec67d5690fbea0154a46d61098b`; it records `independent_wave_disposition: null` and `settlement: unknown`.

**Disposition gap:** there is no independent per-wave disposition path or digest in the reviewed receipts. To change either row from unresolved, a separate committed evidence object must explicitly identify that wave and disposition and be authored by the operator or an appropriate non-author wave/lifecycle owner, distinct from souji's cleanup actor. Until then, both rows remain unresolved; cleanup-only maps to frozen case `loss-cleanup-only` (`true,false,false` → `census-regression`, pin false).

## Method and confidence

- **Observed:** the quoted receipt rows, recorded per-file digests, source/own-lane file hashes, and commit author/timestamps above; exact deletion paths checked from the read-only Git name-status output.
- **Inference:** same-identity cleanup records cannot establish independent disposition; this follows the round-21 contract and province erratum, not merely the timing.
- **Unknown:** any separate operator/lifecycle disposition outside the public artifacts reviewed; the current outcome of either wave beyond its documented loss.
- **Confidence:** high for what the named receipts cover and their author/timing; no conclusion of settlement is made.
- **LSP:** no `lsp` tool is mounted (`xd://lsp` returned “No such tool”); searches were used only to locate source lines, then relevant files/sections and receipts were read directly.
