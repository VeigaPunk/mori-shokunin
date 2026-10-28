# Mo59Reviewer17 — C2 ARTIFACTS binding (copy name → committed `.ufo` artifact, sha256-equality)

Seat: reviewer (read-only). Scope: every `(copy → artifact)` pair in the frozen
`count-c2.py` `ARTIFACTS` dict — (a) each `.ufo` value resolves to a real
committed blob at freeze revision `60b3a76ad0524c8978cc51922940be1c8c388915`,
(b) copy↔artifact sha256-equality holds for files that exist (`.ufo` side
mandatory; copy side checked where it exists), (c) name mapping is unambiguous.

**Verdict: NO COUNTEREXAMPLE.** Binding is sound; no mismatches. One
informational observation (out-of-scope extra copy file) noted at bottom.

## Verified facts

### 1. All 6 `.ufo` anchors are committed blobs at freeze (artifact_absent = impossible at freeze)

`git -C $REPO ls-tree $R -- <path>` for each ARTIFACTS value:

| artifact @60b3a76 | mode/type | blob id | sha256(content) |
|---|---|---|---|
| `.ufo/waves/round-54/w1-results.json` | 100644 blob | `52461ffd…97324` | `ea48a0cc…335f` |
| `.ufo/waves/round-55/w1-results.json` | 100644 blob | `39562ece…14bf7` | `2e5b0a0f…763b` |
| `.ufo/waves/round-56/w1-results.json` | 100644 blob | `12053ae4…307f` | `19536201…761` |
| `.ufo/waves/round-57/w1-results.json` | 100644 blob | `9507020f…22eb6` | `29e7a35d…beb1` |
| `.ufo/waves/round-58/w1-results.json` | 100644 blob | `9064e531…2083` | `a57b660d…61fc` |
| `.ufo/waves/round-58/evidence/w1-settlement.json` | 100644 blob | `39949e14…2b8e` | `b259e73c…5588` |

All are mode `100644` regular blobs — no symlink/gitlink/directory tricks that
`git_show` could misresolve (`git show` on a tree returns listing bytes, not the
artifact, so sha equality would fail loudly anyway).

### 2. Anchors are byte-stable freeze→HEAD (no post-freeze artifact rewrite)

`git rev-parse $R:<a>` vs `HEAD:<a>` — all 6 SAME blob ids (plus DRIFT anchor
`.ufo/waves/round-53/w1-results.json` = `eb3aa50e…b7ad3`, also SAME). So the
counter's `tree` arm (`count-c2.py:266-278`, compares copy@R vs artifact@R at
measured R) cannot be evaded by artifact drift: any binding failure at a landed
R must be a wrong copy, never a moved anchor.

### 3. Name mapping is unambiguous — each copy name maps to exactly one artifact

Full `ls-tree -r` of `.ufo/waves/round-53..58` at freeze: exactly one
`w1-results.json` per round 54–58 and exactly one `w1-settlement.json`
(`.ufo/waves/round-58/evidence/`). Only other results file is
`.ufo/waves/round-53/{a2r1-results.json,w1-results.json}` — r53 is the frozen
DRIFT anchor, correctly NOT in ARTIFACTS (a copy name `w1-results-r53.json`
could not cite-claim anyway: `files:outside` rejects it). Copy basenames'
`-rNN` tags agree with the round in the mapped path for all 6 pairs; keys and
values are both unique (no two copies share an anchor).

### 4. Copy side at freeze: all absent (do-nothing control intact)

`git cat-file -e $R:<copy>` → ABSENT for all 6 `corpus/evidence/sources-r59/*`
paths; also absent at entering `2b9f0397`. The tree arm therefore correctly
yields `copy_absent:*` → UNMET at entering.

### 5. Worktree copies (untracked, wave in-flight) are byte-equal to their freeze anchors

`sha256sum` worktree file vs `git show $R:<artifact> | sha256sum`:

- w1-results-r54 `ea48a0cc…` MATCH; r55 `2e5b0a0f…` MATCH; r56 `19536201…`
  MATCH; r57 `29e7a35d…` MATCH; r58 `a57b660d…` MATCH;
  w1-settlement-r58 `b259e73c…` MATCH — all 6/6 byte-exact.

### 6. Counter binding semantics checked (frozen bytes)

`measure()` tree arm (lines 265-281): per pair, `copy_absent` / `artifact_absent`
/ `tree:<copy>` cover all three failure modes; `sha256(cb) != sha256(ab)` is
byte-exact on raw blob stdout. `eval_entry` pins bind claim→copy content
(`pin:<kid>`), tree arm binds copy→artifact name — composition is complete; no
path for a claim to pin non-artifact bytes while tree passes. Frozen bytes
verified: `count-c2.py`, `count-c1.py`, `contract.md` worktree sha256 ==
freeze-rev sha256 (`2df3ae84…` / `2be6fda8…` / `427fca0b…`); all absent at
entering rev.

## Observations (not mismatches)

- Untracked `corpus/evidence/sources-r59/w1-results-r53.json` exists in the
  worktree (byte-equal to the DRIFT anchor `.ufo/waves/round-53/w1-results.json`,
  `0d644e0f…4260`). It is NOT an ARTIFACTS key: the tree arm ignores it and
  `files:outside` makes it unclaimable, so it cannot pollute claims/files
  counts. It would still cost an S-row slot if opened per "one per cited
  artifact copy" — informational only.
- Hostile trees each ship their own 3 copies under
  `trees-c2/tNN-*/corpus/evidence/sources-r59/` — evaluated in-tree by
  `eval_entry(tr)`; they cannot shadow the real copy dir.

## Method / bounds

Commands run read-only from fleet root against the lane repo: `git ls-tree`,
`git cat-file -e`, `git show`, `git rev-parse`, `git diff --stat`,
`git status --porcelain`, `sha256sum`. Bounded: I verified the `.ufo` side at
freeze (plus HEAD blob-identity) and the copy side where bytes exist on disk;
the counter's R-relative check remains authoritative for the landed commit.
Pins inside the not-yet-committed entry are out of scope (covered by other
seats). No production edits, no commits, no fixture repos created; scratch dir
`/fast/scratch/hyaku/mori-r59/Mo59Reviewer17` created empty, unused, removed.
