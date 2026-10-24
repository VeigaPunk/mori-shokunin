# RevGateTimingE37 — gate `supersede_timing` at `e37dcc6` (C3 falsification)

Verdict: **PASS** — claim C3 verified. S069 is stale at `e37dcc6`, S073 cannot dispose
the `62db24c` in-place edit, and no other id is silently classified `as_of`.

## 1. Timing line at `e37dcc6` (re-derived, not read from a report)

Command run in lane `/home/vgpnk/Projects/shokunin/mori-shokunin`:

```
python3 tools/mori-sources-appendonly.py e37dcc6 --round-base f10a320d
```

Output tail (full 20 lines reproduced):

```
changed S041 superseded_by=S206
changed S044 superseded_by=S207
changed S051 superseded_by=S208
changed S062 superseded_by=S209
changed S064 superseded_by=S210
changed S069 superseded_by=S073
changed S179 superseded_by=S211
changed S180 superseded_by=S212
changed S181 superseded_by=S213
changed S182 superseded_by=S201
changed S183 superseded_by=S214
changed S184 superseded_by=S215
changed S185 superseded_by=S216
changed S186 superseded_by=S217
changed S188 superseded_by=S218
changed S189 superseded_by=S219
changed S190 superseded_by=S220
changed S193 superseded_by=S202
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[S182,S193]
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] stale_supersede=[S069]
exit=1
```

`stale_supersede=[S069]` — matches the claim and the frozen receipt
`.ufo/waves/round-38/evidence/gate-after-e37dcc6.txt` (that file stores only
`command:` / the timing line / `EXIT=1`; both match byte-for-byte).

Tip contrast, same command at `f725f30`: `stale_supersede=[]` with
`changed S069 superseded_by=S226` — S226's declaration at `daa1d4d` (index 51 of the
tip's 52-commit path history) lands strictly after S069's last edit (index 41),
so `landing > last_edit` → `superseded_as_of`.

## 2. Why S073 cannot dispose S069's in-place edit at `62db24c`

Gate rule (`tools/mori-sources-appendonly.py:282-289`): an id is `superseded_as_of`
only when its *latest* supersede declaration's first-appearance index is strictly
greater than the id's last immutable-cell edit index; otherwise `stale_supersede`.
Immutable cells = all columns except `status`/`recheck`/`used-by`
(`tools/mori-sources-appendonly.py:66`).

S069's row history on the path to `e37dcc6` (51 commits, `--reverse` order):

- idx 2 (`8f8c58e`, round-20): row created — teaches already ends
  "…reject absolute and .. lexically before any filesystem call, and test symlinks separately."
- idx 10 (`71abd41f`, round-20 "S073-S076 corrections"): **S073's row created** —
  teaches opens `supersedes S069 —` (verified: `git log -S "supersedes S069"` first
  hit is `71abd41f`; `git log -S "| S073 |"` shows idx 10 is the only commit ever
  touching the S073 row — created and never edited again).
- idx 41 (`62db24c`, round-33): **S069's immutable teaches cell edited in place** —
  `git show 62db24c -- corpus/SOURCES.md` inserts `lane rule:` into the teaches cell:
  `String-only containment cannot see symlinks:` → `…cannot see symlinks: lane rule: …`.
  This is S069's last edit (`last_edit[S069] = 41`).

Order on the commit axis: `decl(S069←S073) @ idx10` ≺ `last_edit(S069) @ idx41`
(`71abd41f` ≺ `62db24c`; `git merge-base --is-ancestor` confirms both ancestors of
`e37dcc6`, and S073's row was never touched after idx 10).

So S073's teaches text was written against S069's **pre-edit** content. The
round-33 edit later rewrote the row's semantics (inserting the "lane rule:"
attribution) *in place* — no new row — leaving S073 superseding a version of S069
that no longer exists. Under the lane's own contract (S205 row:
"corrections are new rows whose teaches opens `supersedes S0NN`"; CORPUS.md rule 2),
disposition requires a superseding row that postdates the last in-place edit.
S073 predates it; its declaration index (10) is not `> 41` → `stale_supersede`.
S226 (`daa1d4d`, idx 51) is the first row to supersede S069 *after* the edit, which
is why the tip correctly flips S069 to `superseded_as_of` — one canonical runtime,
same-identity rerouting confirmed (`changed S069 superseded_by=S073` → `=S226`).

## 3. Missed-stale sweep at `e37dcc6` — none found

Independent recomputation
(`scratch/RevGateTimingE37/verify-timing.py`, re-walks all 51 path commits with an
independently written parser — same column model, anchored `^supersedes S\d{3}`):

- `changed` ids: the same 18 — matches gate `ids=[…]` exactly.
- Expected partition: `as_of` = the 17 non-S069 ids, `stale` = `{S069}` — matches
  the gate line exactly (recompute in `scratch/RevGateTimingE37/recompute.txt`).
- Per-id triple check: every `as_of` id has `decl_idx > last_edit` and also
  `row_landing_idx > last_edit` (17/17; e.g. S041 decl@47>edit@41, S193 decl@46>edit@45).
  No id where the declaration is stale but a coincidental row-landing masks it.
- `deleted=[]`; no changed id lacks a supersede declaration; no superseded id is
  absent from `changed`.
- Mid-cell `supersedes S\d{3}` occurrences the anchored regex misses: **zero** inside
  table rows (all 37 anchored decls accounted for; the S067/S070/S071 ×2 counts are
  prose hits in `Bounded search 11/15` paragraphs, which `parse_registry` never
  reads as rows, and S205's literal "supersedes S0NN" is a non-digit placeholder).
  No hidden declaration could silently flip a classification.
- Edge direction: `landing == last_edit` (same-commit edit+supersede) → `not >` →
  stale; conservative and unreachable here (no same-index pairs in the data).

No other id is stale at `e37dcc6`, and none is silently classified `as_of`.

## 4. Residual risk / notes (not defects in this claim)

- The gate's landing index is the *first* appearance of a `(target, by)` pair
  (`supersede_rows.setdefault`, line 254), not the superseder row's last edit. A
  superseder whose teaches is later edited still counts from first appearance —
  conservative (can only add staleness, never hide it). Verified no such case exists
  in this history.
- `supersede_landing` keeps the *latest-declaring* superseder (line 272-275): an
  early stale decl plus a late fresh decl → `as_of` — correct per the stated rule.
- Exit code 1 at `e37dcc6` is the append-only violations themselves (18 in-place
  edits), orthogonal to `supersede_timing`; contract only claims the timing line.

## Tooling

No installs needed (pacman paused; nothing required beyond stock python3/git).

Report: .ufo/waves/round-38/w2/RevGateTimingE37.md
