# LossUnknown — r21 loss-accounting unresolved dispositions (metadata only)

Seat: MoriR22.LossUnknown (scout, read-only). Scope: `corpus/evidence/loss-accounting-r21.json` plus the three artifacts it references directly. No matched text, no transcript/session/config reads, no tests/builds. Installs: none.

## Verdict

CONFIRMED: exactly two observations, both unresolved, and neither has an independent disposition. Baseline acceptance stays blocked.

| id | state | independent_disposition |
|---|---|---|
| `aggregator-r10` | `unresolved` | `null` |
| `aggregator-r10-resume` | `unresolved` | `null` |

Schema `mori-loss-accounting-v1`; `observations` length 2; no other observation states are present.

## File identity (observed)

- `corpus/evidence/loss-accounting-r21.json`: worktree sha256 `e650c7ff04bcff61d17150ba5bbcfdad4fe5130817b307e9ec9f7764fa5b2736`; HEAD (`306e06ecd02e0ea8e544fbd30d1ff7e7359c581e`) blob `c055b634d8ceff3789e0c7a015280c0254e3ac6d`; `git status --porcelain` is clean.
- Introduced by `8fed329636f53455ae2f53930c171c6186aff1fd` (2026-10-21T09:44:23-03:00), which is an ancestor of the round-22 entering commit `77a5bbe8a0b41dfbfd2546d024d36e294b814bd0`, which is in turn an ancestor of HEAD.

## Referenced evidence bindings (identical for both observations; all verified)

| role | path | revision | sha256 | worktree | git blob at revision |
|---|---|---|---|---|---|
| baseline | `corpus/evidence/baseline-r10-20261015T2231Z.json` | `e9f340ce986f82a60baad1b8e5ead655ab818a1c` | `0993b23505deab2aeb05b2309bdf7dd6eaad2b82f27852491352511aa9670478` | match | match |
| deletion | `.ufo/waves/round-21/evidence/removal-metadata.txt` | `a8442a018aa9c51b21b92c3ce3b17736317375b1` | `4276625be64ab1943bb5781dab7a3d9e8c912bdb48ea562870f20b70b753263e` | match | match |
| cleanup | `.ufo/waves/round-21/evidence/cleanup-receipts.tsv` | `a8442a018aa9c51b21b92c3ce3b17736317375b1` | `46f84c3a60ac701ec7d0c16523e5bbfa999be3999cb61029be8fba50785970a7` | match | match |

- Both revisions are commit objects and ancestors of HEAD.
- Cleanup actor recorded: `souji-shokunin <souji@shokunin.local>`. This is the cleanup executor, not an independent disposer.
- Reference counts (counts only, no text): `removal-metadata.txt` has 36 lines, 18 of which mention `aggregator-r10` (10 of them `-resume`). `cleanup-receipts.tsv` has 18 lines with the same 18/10 split. The baseline JSON has 2 lines (1 of them `-resume`). The token `disposition` appears 0 times in all three files, so no referenced artifact supplies an independent disposition.

## Preservation criterion

The unknown is preserved only if all of the following hold:

1. `corpus/evidence/loss-accounting-r21.json` stays byte-unchanged: sha256 `e650c7ff04bcff61d17150ba5bbcfdad4fe5130817b307e9ec9f7764fa5b2736`, blob `c055b634d8ceff3789e0c7a015280c0254e3ac6d`.
2. Both observations keep `state: "unresolved"` and `independent_disposition: null`. No round-22 artifact may assert either disappearance as resolved, accepted, benign, or attributed.
3. All six (path, revision, sha256) bindings above keep verifying, both in the worktree and as Git blobs at their recorded revisions. The referenced evidence also stays byte-unchanged.
4. Baseline acceptance stays blocked while either disposition is null. A cleanup receipt or deletion metadata, including souji's, does not count as an independent disposition. A source hash is not authentication or secrecy.
5. Any future resolution has to arrive as new, append-only evidence from an actor independent of the cleanup actor, and it must reference this file's sha256. It must never come from editing this file in place.

## Remaining unknowns

- The actual fate of the two historical waves (`aggregator-r10`, `aggregator-r10-resume`) is unknown. No evidence in scope resolves it.
- I did not determine whether an independent disposer exists anywhere outside the named files; that would need a search outside this scope.

## Checks actually run

`sha256sum` on the 4 files; `git cat-file -t` and `cat-file blob | sha256sum` for the 3 bindings; `git log`, `ls-tree`, `status --porcelain`, `rev-parse HEAD`; `merge-base --is-ancestor` ×4; `rg -c` counts on the 3 referenced files. No tests, builds, or linters.
