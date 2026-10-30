# Mo61Critic27 — assimilation ruling sanity (read-only)

Seat: Mo61Critic27 (critic, leaf). Scope: verify the 94-collision extraction and count, the
0–3-space-tolerant pattern, and the "mass id drift → L0 question + adopt nothing" ruling.
No counter, contract, registry, or VCS state was written. Scratch used and removed:
`/fast/scratch/hyaku/mori-r61/Mo61Critic27/` (plus one `/tmp/lc.err`, deleted).

## Verdict

- **Count: correct.** 94 recomputed byte-identically from the lane registry and the staged package.
- **Pattern: correct and matches the CORPUS census clause.** The 0–3-space tolerance is the right
  choice. It is non-discriminating on today's inputs (no indented id rows exist in either file), so
  the r50 guard-proof is what carries the proof, and it replays exactly.
- **Ruling: consistent with the lane-addendum clause, but mis-cited.** The rule is not in
  `CORPUS.md §10` (that section does not exist). It is `scripts/hyaku/lane-addendum.md` §6 item 10,
  lines 457–466. The frozen contract and `build-w1-spec.py:341` repeat the wrong section number.
- **Provenance gap:** the 94 is computed from an uncommitted working-tree file in the shokuknow repo.
  No sha of that input is pinned anywhere in the r61 wave.

## Evidence

### 1. Recomputation (exact commands, all read-only)

```
LANE=/home/vgpnk/Projects/shokunin/mori-shokunin
S=/home/vgpnk/Projects/shokuknow
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' $LANE/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > reg-ids.re
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' $S/merge/mori/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > staged-ids.re
comm -12 reg-ids.re staged-ids.re > collisions.re
```

- `reg-ids`: 337 lines, 337 unique. `diff` against `.ufo/waves/round-61/assimilation/reg-ids` → identical.
- `staged-ids`: 136 lines, 136 unique (S471..S606). `diff` → identical.
- `collisions`: 94 lines, S471..S564, contiguous. `diff` → identical.
- Re-derived from committed lane bytes only (`comm -12 assimilation/reg-ids assimilation/staged-ids`): 94, identical.
- Locale check: `LC_ALL` = C, en_US.UTF-8, C.UTF-8, POSIX all give 94, no sort warnings.
- Manual census row count (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`) = 337, matching CORPUS.md's own census.
- Registry worktree is clean; `HEAD:corpus/SOURCES.md` = `c3a91a39…` = `git hash-object` of the worktree file.

### 2. Pattern discrimination

- `^ {0,3}\|` and `^\|` give identical output on both current inputs: 337 / 136 / 94. Identical to committed bytes. The tolerance is therefore not exercised by today's data.
- Fixture `  | S002 |` (2 leading spaces): tolerant pattern → 1 collision; column-zero pattern → 0. The tolerant pattern is the one that catches it.
- r50 guard-proof (`.ufo/waves/round-50/assimilation/guard-proof/`) replayed: tolerant collisions = `S533 S534`, identical to its `collisions` file. Column-zero would give 0.
- Census CLI row scanner (`scripts/sources-census.sh:615-616`, `sub(/^ {0,3}/,…)`) agrees with the extractor's 0–3 rule. Rows with 4+ spaces are ignored by both.

### 3. What a false-green would have looked like (each tested)

| construction | result | why it is a false green |
|---|---|---|
| column-zero-only pattern (`^\|`) | 0 on indented fixture | misses indented collisions. Not the case today (0 indented rows in both files), but the guard would be silently dead. |
| census-section-gated staged extraction | **0 collisions** (staged census-semantics rows = 0) | the staged file has **no `## Registry` heading**, so census finds no rows and the collision set is empty. Census run on it: `rc=1`, 136× `E12 row outside Registry section`. |
| unanchored `S[0-9]{3,}` over whole staged file | 170 ids, 101 "collisions" | prose tokens inflate the set. Wrong-direction false alarm. |
| committed staged blob `6338c2b1` instead of the live file | 92 staged ids, **6 collisions** | `git diff --stat` in shokuknow: live file is 136+/92−, uncommitted. Using the committed blob turns 94 into 6. |
| census CLI `validate --file <staged>` exit code read through a pipe | `rc=0` if read through `| head` | the first run printed `rc=0` only because it captured `head`'s status. Direct run: `rc=1`. Do not cite the pipe form. |

### 4. Provenance gaps (the input is not pinned)

- Staged input `/home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md`, sha256
  `4f69b2df7644441174ab7db152dab3316be7e46cae666e308097afb3d7bfe1cc`. Committed blob at
  `ba6779f0`…: `6338c2b1…`. The live file differs from the committed blob (`git diff --stat`:
  136 insertions, 92 deletions). The round-61 wave records no sha of this input.
- `merge/mori/` has no `## Registry` section. Census reports the file as E12 on all 136 rows.
  This is a shokuknow-side defect, not a lane defect.
- The 94 collisions are the entire S471–S564 block (94 consecutive registry ids). The lane's
  own rounds 44–60 grew into the staged space. The package was built against registry max S470.
  This supports the "mass drift" reading.

### 5. Ruling sanity

- The clause at `lane-addendum.md:464` is: "Drift a read-only check cannot fix (mass id drift,
  reshuffled register) → append an L0 question and adopt nothing this round." The L0 is filed at
  fleet commit `1aea7343` (`.ufo/l0-questions.md`, line 210). It says "adoption closed this round"
  and cites the 0–3-space extraction and the collisions file. Accurate.
- The rule is conditional: "a read-only check cannot fix." The lane has done this before.
  Round-45 `renumber-map.tsv` and round-50 "renumber by document" (contract:133-139, adopted
  S533→S489) show a document-keyed map is producible read-only. On the current data, 39 of 94
  colliding staged rows point at a document the lane already holds under another id (e.g.
  S471→S232), and 55 do not. So whether this is "a drift a read-only check cannot fix" is a judgment,
  not a mechanical fact. The ruling is defensible: 94/94 of the block drifted, and the frozen
  contract says adopt nothing. The L0 should say that the document-keyed map is possible but
  was not built, not that it is impossible.
- Mis-citation: `build-w1-spec.py:341` says "CORPUS.md §10". `CORPUS.md` has no §10. The clause
  lives in `scripts/hyaku/lane-addendum.md` §6 item 10. The contract line 140 gives no section, so it
  is correct. Report only; do not amend.
- Contract typo: `contract.md:137` says "rows S565–S070". It should read S565–S570. The data
  phase would add those ids, which would raise the collision count to 100 (computed: S565–S570 are
  all in the staged set, 6 more collisions). The next round's guard will see 100, not 94, unless the
  L0 is answered first.

## Findings (routed; no edits)

1. **Mis-citation (low):** `build-w1-spec.py:341` cites `CORPUS.md §10`. Correct: `scripts/hyaku/lane-addendum.md` §6 item 10 (lines 457–466). Frozen contract wording is fine.
2. **Unpinned input (medium):** the staged file's sha256 (`4f69b2df…`) and the committed blob (`6338c2b1…`) are not recorded in the r61 wave. Anyone reproducing the 94 from the committed blob gets 6. Recommend the L1 record the live sha in the L0 or the report.
3. **Contract typo (low):** `contract.md:137` "S565–S070" → S565–S570. Report only.
4. **Next-round consequence (informational):** after the data phase lands S565–S570, the next collision run reads 100, not 94. The L0 should record the expected count so the next guard does not look like a regression.
5. **Staged file defect (shokuknow, out of lane):** `merge/mori/SOURCES.append.md` has no `## Registry` heading, so the census validator reports 136 E12 on it.

## Receipts (small, copy-paste)

```
reg-ids 337 / staged-ids 136 / collisions 94   (re-derived; identical to committed)
committed-blob staged-ids 92 / collisions 6    (false green if the blob is used)
section-gated staged extraction 0               (false green: no Registry heading)
census validate --file <staged> -> rc=1, 136x E12
r50 guard-proof replay: S533 S534 (identical)
data-phase projection: S565–S570 -> 100 collisions
```

No commits, no VCS mutation, no fleet or sibling writes. Scratch removed in the final step.

## Tooling

No installs. Only coreutils (`grep`, `comm`, `sort`, `diff`, `awk`, `git` read-only), `python3`, and the census CLI in read-only mode.
