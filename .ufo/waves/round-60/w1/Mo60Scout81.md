# Mo60Scout81 — instrument-surface recon

Pinned range: `ddfb12fb0838b4307c445194a844f0c4b1950195..b3c256138f00c704d5aa56eb0332d74506502ef2`.
Tip at read time: `b3c256138f00c704d5aa56eb0332d74506502ef2` (detached HEAD, no branch). Ancestor check: base is an ancestor of tip; parent of the first in-range commit `4d036fb07207dbc9aa400617e57117b9857114e9` is the entering revision. Six commits. Read-only. No lsp (path inventory, not a symbol).

## Verdict

**Not exactly the instrument set.** `git diff --stat` is `141 files changed, 4188 insertions(+), 2 deletions(-)`. Default `--name-status` is `138 A`, `3 M`, no `D`. `--find-renames --find-copies` does not reclassify any path (`138 A`, `3 M`). Tracked worktree at the tip was clean (`git status --porcelain --untracked-files=no` empty).

Of the 141 paths:

| bucket | count | status |
|---|---:|---|
| `tools/mori-entry-claims-check.py` | 1 | A (absent at base: `git cat-file -e ddfb12fb:tools/mori-entry-claims-check.py` → fatal, not in that revision) |
| counters `count-c1.py` `count-c2.py` `count-c3.py` | 3 | A |
| fixture trees `trees-c2h/` | 117 | A |
| fixture expect table `trees-c2h-expects.json` | 1 | A |
| fixture builder `build-fixtures-r60.py` | 1 | A |
| **flagged, not that set** | **18** | 13 A + 3 M |

123 paths are the verifier, the three counters, and the fixture package (13 hostile trees, the expect table, the builder). The other 18 are wave-control, evidence receipts, and production/corpus edits.

After amended freeze `ac496c7c` (the contract's pre-data amendment 2), **no commit touches** the verifier, the three counters, `build-fixtures-r60.py`, `trees-c2h/`, `trees-c2h-expects.json`, or `contract.md`. `git log ac496c7c..b3c25613 -- <those paths>` is empty.

## Command

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --stat \
  ddfb12fb0838b4307c445194a844f0c4b1950195..b3c256138f00c704d5aa56eb0332d74506502ef2
```

Summary line: `141 files changed, 4188 insertions(+), 2 deletions(-)`.

The only deletions in the range are the two SCORECARD row replacements (`numstat` `2 2` on `SCORECARD.md`). Every other changed path is insertion-only.

## In set

Verifier (added; 478 lines at tip vs base):

- `tools/mori-entry-claims-check.py`

Counters (all under `.ufo/waves/round-60/`):

- `count-c1.py` (307)
- `count-c2.py` (488)
- `count-c3.py` (314)

Fixtures. Thirteen trees, each with the same 9 relative paths (suffix count is 13 for every suffix; 13×9 = 117; no other path under `trees-c2h/`):

Trees: `h00-good-control` `h01-semantically-empty` `h02-malformed-claim` `h03-line-offset-alias` `h04-blank-quote` `h05-short-quotes` `h06-degenerate-text` `h07-single-row` `h08-row-not-mined` `h09-usedby-other` `h10-stale-pin` `h11-wrong-line` `h12-no-frontmatter`.

Per tree, all `A`:

- `corpus/SOURCES.md`
- `corpus/evidence/sources-r59/w1-results-r54.json`
- `corpus/evidence/sources-r59/w1-results-r55.json`
- `corpus/evidence/sources-r59/w1-results-r56.json`
- `corpus/evidence/sources-r59/w1-results-r57.json`
- `corpus/evidence/sources-r59/w1-results-r58.json`
- `corpus/evidence/sources-r59/w1-settlement-r58.json`
- `corpus/knowledge/wave-settlement-artifacts-r59.md`
- `expect.txt`

Full path shape: `.ufo/waves/round-60/trees-c2h/<tree>/<suffix>`.

Also counted in the fixture package, not inside a tree:

- `.ufo/waves/round-60/trees-c2h-expects.json` (40) — frozen expect table
- `.ufo/waves/round-60/build-fixtures-r60.py` (270) — builder, not a hostile tree and not a counter

`tools/` in this range is only `tools/mori-entry-claims-check.py`. `LOG.md` and `MANIFEST.json` are not in the diff.

## Flagged (18)

Wave control (4, all A):

- `.ufo/waves/round-60/contract.md` (163) — claim text, not an executable instrument
- `.ufo/waves/round-60/build-w1-spec.py` (144)
- `.ufo/waves/round-60/w1-spec.json` (327)
- `.ufo/waves/round-60/w1-dispatch.json` (747)

Evidence receipts (9, all A):

- `.ufo/waves/round-60/evidence/census-start.txt` (26)
- `.ufo/waves/round-60/evidence/control-c1-do-nothing.txt` (1)
- `.ufo/waves/round-60/evidence/control-c2-do-nothing.txt` (1)
- `.ufo/waves/round-60/evidence/control-c3-do-nothing.txt` (1)
- `.ufo/waves/round-60/evidence/c2-at-freeze.txt` (1)
- `.ufo/waves/round-60/evidence/c3-at-freeze.txt` (1)
- `.ufo/waves/round-60/evidence/r59-absent-set.md` (22)
- `.ufo/waves/round-60/evidence/r59-c1-met.txt` (1)
- `.ufo/waves/round-60/evidence/r59-c2-met.txt` (1)

Production / corpus (5). These are outside `.ufo/waves/round-60/` and outside `tools/`:

- `M SCORECARD.md` — hunk `@@ -2950,2 +2950,2 @@`. Lines 2950–2951 (the round-59 C1 and C2 table rows) replaced in place. Both new rows carry an `r60-correction:` dead-pointer note (`c1-entering.txt` → `control-c1-do-nothing.txt`, `c2-entering.txt` → `control-c2-do-nothing.txt`). `numstat` `2 2`. This is the range's only deletion.
- `M corpus/QUALITY.md` — hunk `@@ -1586,0 +1587,33 @@`. Inserts lines 1587–1619: `## Criteria added round 60` items 156 and 157. `numstat` `33 0`.
- `M corpus/SOURCES.md` — hunk `@@ -340,0 +341,4 @@`. Inserts lines 341–344: Registry rows S561, S562, S563, S564. `numstat` `4 0`.
- `A corpus/knowledge/entry-claims-hardening-r60.md` (43)
- `A corpus/lessons/round-60.md` (87)

## Commits (oldest first)

| rev | subject | what it touches beyond a pure add of the freeze set |
|---|---|---|
| `4d036fb0` | freeze counters + verifier + 13 trees + do-nothing controls | introduces verifier, three counters, builder, contract, expects json, all 117 tree files, `census-start.txt`, three `control-*-do-nothing.txt` |
| `772b2b4b` | freeze amendment 1 (pre-data) | `M` verifier, `count-c2.py`, `count-c3.py`, builder, `contract.md`, and `expect.txt` for h01–h12 (not h00) |
| `ac496c7c` | freeze amendment 2 (pre-data) | `M` `count-c3.py` only |
| `76904b21` | w1 dispatch + at-freeze C2/C3 receipts | `build-w1-spec.py`, `w1-spec.json`, `w1-dispatch.json`, `evidence/c2-at-freeze.txt`, `evidence/c3-at-freeze.txt` |
| `398d3225` | land C1 data | `evidence/r59-absent-set.md`, `r59-c1-met.txt`, `r59-c2-met.txt`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/knowledge/entry-claims-hardening-r60.md`, `corpus/lessons/round-60.md` |
| `b3c25613` | census E12: S561–S564 into the Registry table | `M` `corpus/SOURCES.md` only (net vs base is the single +4 hunk above) |

## Working tree, not in the range

Untracked files are not in `ddfb12fb..b3c25613`. Snapshot while tip was still `b3c25613` (`git status --porcelain=v1 -b --untracked-files=all`):

- `?? .ufo/waves/round-60/evidence/c1-at-data.txt`
- `?? .ufo/waves/round-60/w1.ready`
- `?? .ufo/waves/round-60/w1.ready.dispatched`
- `?? .ufo/waves/round-60/w1/Mo60Executor51.md`
- `?? .ufo/waves/round-60/w1/Mo60Executor53.md`
- `?? .ufo/waves/round-60/w1/Mo60Executor54.md`
- `?? .ufo/waves/round-60/w1/Mo60Executor56.md`
- `?? .ufo/waves/round-60/w1/Mo60Executor61.md`
- `?? .ufo/waves/round-60/w1/Mo60Reviewer14.md`
- `?? .ufo/waves/round-60/w1/swarm-registry.json`

An earlier status in the same seat also showed `w1.ready.partial` and did not yet show `w1.ready.dispatched` or several `w1/*.md` files. That set is live wave output, not a committed instrument surface. Do not treat it as part of the tip diff.

## Confidence

High on the 141-path inventory, the 123/18 split, the 13×9 tree product, the production hunks, and the empty post-`ac496c7c` instrument log. Those are `git diff` / `git log` / `git cat-file` against the named revisions.

Unresolved: whether a later commit after `b3c25613` lands more C1 data (the untracked `c1-at-data.txt` is the obvious candidate). This recon does not score that file.
