# Mo50bMutCollisionGuard — mutation test of the assimilation collision guard (a2w1)

Seat: Mo50bMutCollisionGuard (mori-shokunin, round 50 attempt 2, wave a2w1). Date: 2026-10-26.
MACHINE_ID: `432d02b544a5459ebbff9c42ec68334d`. Lane pin under test: `487941b9395e89678af0053cc443cdb49cdee6e3` (verified `git rev-parse --verify 487941b…^{commit}`; live worktree `corpus/SOURCES.md` byte-identical to the pinned blob — `cmp` rc 0, so all pin numbers below also describe the worktree).
Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bMutCollisionGuard/` (TMPDIR under it; removed before yield). Tooling installed: none. No subagents. Repo bytes never written: all runs used scratch copies; repo fixture hashes before (copies) and after are equal (§7).

Claim under test (contract.md, "Frontier step, assimilation"): the guard pattern `^ {0,3}\|[[:space:]]*S[0-9]{3,}` catches indented registry rows, and the wave's `assimilation/{reg-ids,staged-ids,collisions}` artifact is reproducible with it.

## 1. Detector under test

The quarantine-scout collision pipeline, verbatim (guard taken from a pattern file so the mutant is a byte-level change to the behavior-bearing point only):

```sh
grep -oE "$GUARD" REGISTRY | grep -oE 'S[0-9]+' | sort > reg-ids
grep -oE "$GUARD" STAGED   | grep -oE 'S[0-9]+' | sort > staged-ids
comm -12 reg-ids staged-ids > collisions
```

Inputs (scratch copies; sha256):
- fixture registry `guard-proof/registry.md` `e54d759bf78be36200da999c7d0e060ce6eab7ddcd54272deb91c304dbd793ba`; fixture staged `staged.md` `4cfbdd889f070d417f1668712dfc673cc7361c2a1bab816dd53cf29a20a6eb8b`; expected outputs `reg-ids` `b2292f43…`, `staged-ids` `3149d417…`, `collisions` `69c3b272…`.
- real registry `git show 487941b…:corpus/SOURCES.md` → `33f294439e479f3891fbc5b71b5ceb0a623871cad6980285dcbc696be04fc185` (331 lines).
- real staged `/home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md` (read-only copy) → `4f69b2df7644441174ab7db152dab3316be7e46cae666e308097afb3d7bfe1cc` (142 lines).

Kill rule (per tasking): a mutant is **killed iff the collision set changes** vs the pristine run; run on the fixture pair and the real pair.

## 2. Baseline (pristine) — passes, verdicts conclusive

```text
GUARD = ^ {0,3}\|[[:space:]]*S[0-9]{3,}          (pristine.pat sha256 0e77845e…)
fixture: reg-ids 3 (S533,S534,S900)  staged-ids 3 (S533,S534,S539)  collisions 2 (S533,S534)
diff vs guard-proof/{reg-ids,staged-ids,collisions}: IDENTICAL, rc 0 — byte-for-byte
real:    reg-ids 264   staged-ids 136   collisions 21 (S471…S491)
```

Answer to "does it still report the indented collisions and the 18 real ones": **yes, with a drift on the real side.** The indented fixture collisions S533/S534 are reported; on the real pair the pinned-rev run reports **21** collisions, whose **first 18 are exactly the frozen artifact's 18** (`diff assimilation/collisions <(head -18 pristine-collisions)` → rc 0, S471–S488); the extra S489/S490/S491 exist because round 50 itself landed those ids into the registry while the staged package also carries same-numbered rows — the same 18→21 drift Mo50bScoutQuarantine.md finding 3 already reported (frozen `assimilation/{reg-ids,collisions}` = 261/18). Not a guard fault; baseline for kill verdicts is the pristine run at the same rev.

## 3. Mutants and verdicts

| mutant | guard (mutated bytes, sha256 prefix) | fixture collisions | real collisions | verdict |
|---|---|---|---|---|
| M1 column-0 only | `^\|[[:space:]]*S[0-9]{3,}` `822615ae` | {S533,S534} → ∅ | 21 → 21 unchanged | **KILLED** (fixture) |
| M2 `{0,1}` | `^ {0,1}\|[[:space:]]*S[0-9]{3,}` `a8e9e5a7` | {S533,S534} → ∅ | unchanged | **KILLED** (fixture) |
| M3 `{0,4}` | `^ {0,4}\|[[:space:]]*S[0-9]{3,}` `87fc3a61` | {S533,S534} → {S533,S534,**S539**} | unchanged | **KILLED** (fixture) |
| M4 `S[0-9]{2,}` | `^ {0,3}\|[[:space:]]*S[0-9]{2,}` `06fe4fbb` | unchanged | unchanged | **SURVIVED** |
| M5 no `[[:space:]]*` | `^ {0,3}\|S[0-9]{3,}` `630667fe` | → ∅ | 21 → **∅** | **KILLED** (both) |

Observed outputs (abridged from the run log):

```text
m1-col0/fixture diff vs pristine:  @@ -1,2 +0,0 @@  -S533 -S534          (indented collisions lost)
m2-q1/fixture  diff vs pristine:  @@ -1,2 +0,0 @@  -S533 -S534
m3-q4/fixture  diff vs pristine:  @@ -1,2 +1,3 @@  +S539                 (4-space code-indented row now a false registry row)
m4-s2          fixture and real:  collisions IDENTICAL
m5-nospace/real diff vs pristine: @@ -1,21 +0,0 @@  -S471 … -S491         (every real row is "| S…" with a space)
```

Interpretation: the two fixture behaviors the contract claims — indented rows caught, "a column-0-only pattern catches neither" — are both real: M1/M2 lose the indented collisions, M3 over-matches the 4-space code-fence row S539, M5 loses everything because all real rows carry a space after the pipe. M4 changes nothing anywhere (see §4).

## 4. Extra question: does any row in the real registry start with 1-3 spaces?

No. Probes on the pinned registry and on the staged append (`grep -cE`, counts):

```text
SOURCES.md          rows starting 1-3 spaces + '|': 0   4+ spaces + '|': 0
                    guard hits 264, of which at column 0: 264
                    row-start S-ids with 1-2 digits: 0   row-start '|S' (no space): 0
SOURCES.append.md   rows starting 1-3 spaces + '|': 0   4+ spaces + '|': 0
                    guard hits 136, of which at column 0: 136
                    row-start S-ids with 1-2 digits: 0   row-start '|S' (no space): 0
```

So on today's real data the `{0,3}` upper bound and the `[[:space:]]*` element are exercised only by the fixture; M4's widened `{2,}` has zero blast radius because no row in either file starts with a 1-2-digit id.

## 5. Named limits

- M1/M2/M3 are killed **only by the fixture detector**; on the real pair alone their collision sets are unchanged (registry and append are 100 % column-0 rows). The kill evidence rests on `guard-proof/`, which is exactly what that fixture was built to carry.
- M4's survival is a fixture coverage gap (no short-id negative case), not evidence that the guard is wrong: no real row can distinguish `{2,}` from `{3,}` today. [INFERENCE] The id shape is additionally enforced downstream for C2 claims by `count-c2.py:154` (`re.fullmatch(r"S[0-9]{3,}", sid)` → counted bad), an independent carrier of the `{3,}` convention; no counter change proposed.
- The dispatcher's expected "18 real ones" corresponds to the frozen pre-landing artifact (`reg-ids`=261); at the pinned rev the same pristine pipeline yields 21. Recorded as observed drift, not compensated.

## 6. Restoration evidence

- Mutated bytes lived only in `$S/mutants/*.pat` + `$S/pipeline.sh` + `$S/run-all.sh` (scratch, disposable per operator directive 2026-10-25); the six pattern-file sha256s are recorded in §3. No repo path was ever a write target.
- Repo fixture hashes after the sweep equal the before-copies: registry.md `e54d759b…`, staged.md `4cfbdd88…`, reg-ids `b2292f43…`, staged-ids `3149d417…`, collisions `69c3b272…` — UNCHANGED.
- Post-sweep pristine re-run: fixture outputs `diff -r` vs pre-mutant pristine → IDENTICAL rc 0 (reg=3 staged=3 coll=2); real outputs IDENTICAL rc 0 (reg=264 staged=136 coll=21).
- Scratch removed at the end of this seat (`rm -rf /fast/scratch/hyaku/mori-r50/Mo50bMutCollisionGuard`), TMPDIR included.

## Findings

- LOW — coverage gap: mutant M4 `^ {0,3}\|[[:space:]]*S[0-9]{2,}` **survives** on both fixture and real pairs (collision sets byte-identical to pristine). The fixture `.ufo/waves/round-50/assimilation/guard-proof/registry.md` has no 1-2-digit-id negative row, and no row of `corpus/SOURCES.md` @487941b or `SOURCES.append.md` starts with a 1-2-digit id (probe count 0/0), so the guard's `{3,}` lower bound is currently untested and unexercised. Guard not weakened on today's data; a fixture row like `  | S47 |` would kill it.
- LOW — fixture-dependence: mutants M1 (`^\|`), M2 (`{0,1}`), M3 (`{0,4}`) are killed only on the fixture detector; on the real pair (`.ufo/waves/round-50/assimilation/{reg-ids,collisions}` inputs `corpus/SOURCES.md` @487941b, `SOURCES.append.md`) their collision sets are unchanged because every one of the 264+136 real rows is column-0 with `| S…` spacing. The guard-proof fixture is the sole evidence carrier for the `{0,3}`/`[[:space:]]*` invariants; it should stay with the round artifacts.
- LOW — stale frozen counts (already reported by Mo50bScoutQuarantine.md): the tasking's "18 real ones" (S471–S488) is the pre-landing snapshot (`assimilation/reg-ids`=261, `collisions`=18); the pristine pipeline at the pinned rev `487941b` reports 264 registry ids and 21 collisions, the frozen 18 being exactly its first 18 plus landed-and-staged S489–S491. No guard or counter defect; L1 should quote 21 (or 18 with "as of the freeze") if it cites the collision counts.

Guard verdict: invariant **holds** — 4/5 mutants killed; the one survivor is a fixture coverage gap, not a counter or data fault. Per seat bounds, no change to any counter, predicate, fixture or corpus file is proposed.
