measured 2026-10-23T12:11:37Z

# ReviewDebtList — re-derive the SOURCES append-only debt at 6bd57097 (routed defect 2, round-35 spotcheck §6 item 2)

Reviewed: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-35-verifier-spotcheck.md:172-174` —
"15 ids changed in place before round 34, not superseded (`w2/ScoutAppendDebt.md`), plus S069."
Method: sandbox clone, the round-35 checker at the pinned rev, plus an independent parser (not the checker)
and literal `git log -p` walks for 3 sampled ids. No lane writes; no installs (python3/git already present).

## Run

Clone (per containment rules):
`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r36/ReviewDebtList/clone` → HEAD c1a026cb; `6bd57097^{commit}` = 6bd57097f7ab2b471b4593ed2019c980b1368c68, an ancestor of the clone HEAD.

Checker (identical at both revs — `git diff --stat 6bd57097 HEAD -- .ufo/waves/round-35/check-sources-appendonly.py` is empty):

```
$ cd /fast/scratch/hyaku/mori-r36/ReviewDebtList/clone
$ timeout 120 python3 .ufo/waves/round-35/check-sources-appendonly.py 6bd57097 --repo .
rev=6bd57097f7ab2b471b4593ed2019c980b1368c68 rows=204 commits=47
CHANGED id=S041 origin=273aa74a changed_at=62db24c0 cols=teaches superseded_by=-
CHANGED id=S044 origin=273aa74a changed_at=62db24c0 cols=teaches superseded_by=-
CHANGED id=S051 origin=daceeec8 changed_at=62db24c0 cols=teaches superseded_by=-
CHANGED id=S062 origin=daceeec8 changed_at=62db24c0,ab8f4cf cols=teaches superseded_by=-
CHANGED id=S064 origin=367927c5 changed_at=62db24c0,ab8f4cf cols=scope,teaches superseded_by=-
CHANGED id=S069 origin=8f8c58ee changed_at=62db24c0 cols=teaches superseded_by=S073
CHANGED id=S179 origin=55c3ed5e changed_at=5126891 cols=scope,teaches superseded_by=-
CHANGED id=S180 origin=62db24c0 changed_at=ab8f4cf cols=anchor,teaches superseded_by=-
CHANGED id=S181 origin=62db24c0 changed_at=ab8f4cf cols=source,scope,anchor superseded_by=-
CHANGED id=S182 origin=62db24c0 changed_at=ab8f4cf,8d56809 cols=anchor superseded_by=S201
CHANGED id=S183 origin=62db24c0 changed_at=ab8f4cf cols=anchor,teaches superseded_by=-
CHANGED id=S184 origin=62db24c0 changed_at=ab8f4cf cols=anchor superseded_by=-
CHANGED id=S185 origin=62db24c0 changed_at=ab8f4cf cols=anchor,teaches superseded_by=-
CHANGED id=S186 origin=62db24c0 changed_at=ab8f4cf cols=scope,anchor,teaches superseded_by=-
CHANGED id=S188 origin=62db24c0 changed_at=ab8f4cf cols=scope,anchor,teaches superseded_by=-
CHANGED id=S189 origin=62db24c0 changed_at=ab8f4cf cols=anchor superseded_by=-
CHANGED id=S190 origin=62db24c0 changed_at=ab8f4cf cols=scope,anchor,teaches superseded_by=-
CHANGED id=S193 origin=8d56809a changed_at=406d91a4 cols=anchor,teaches superseded_by=S202
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] superseded=[S069,S182,S193]
EXIT=1
```

(origin/changed_at shas abbreviated here; full shas in the raw output and in my re-derivation below.)

## Independent re-derivation (own parser)

`/fast/scratch/hyaku/mori-r36/ReviewDebtList/rederive.py` (sha256 11558e9eaa87075031064acb611b119f005de4799a1faf75f31cfb751b1f3718)
re-walks all 47 content snapshots of `corpus/SOURCES.md` in 6bd57097's ancestry, applies the same 11-cell
row rule and the same 8 compared cells, and recomputes first-held, changes and supersessions without importing
checker code. Result: identical 18 ids, identical origin commits, identical changed_at lists, identical
superseded_by. `ids_ever=204 ids_at_tip=204`.

## `git log -p` sampling (3 ids, first-held cells)

`git log -p --reverse --format='COMMIT %h %s' -- corpus/SOURCES.md | awk` first-added row per id:

- **S041** first added at `273aa74a` "round-17: terminal observation, branch provenance and blind-sweep calibration". First-held teaches: "HTTP 429 denotes too many requests in a time window; it does not identify a vendor business error or establish permanent seat death." Tip row inserts `lane rule: ` before "it does not identify" — teaches-only in-place edit. Matches checker (origin=273aa74a, cols=teaches).
- **S184** first added at `62db24c0` "round-33: C1 FR6 entry, sources S180-S190 …". First-held anchor: `block/blk-core.c:1067-1068,1100,1110; tag v7.2`; tip: `:1067-1068,1100,1108-1110`. Teaches byte-identical; anchor-only in-place edit. Matches checker (origin=62db24c0, cols=anchor).
- **S069** first added at `8f8c58ee` "round-20: C1 classified register and re-pin (baseline-r20) …". First-held teaches: "String-only containment cannot see symlinks: reject absolute and .. lexically …"; tip inserts `lane rule: ` after the colon. Teaches-only in-place edit. Matches checker (origin=8f8c58ee, superseded_by=S073).

## Superseded ids and the exact decomposition

- S069 superseded by S073 — `corpus/SOURCES.md:79` teaches opens `supersedes S069 — string-only containment …`.
- S182 superseded by S201 (`corpus/SOURCES.md:207`), S193 superseded by S202 (`corpus/SOURCES.md:208`); both landed in round-35 (`cedb0ec` subject: "S201/S202 supersede S182/S193"; spotcheck `:81`).
- Not superseded (15): S041, S044, S051, S062, S064, S179, S180, S181, S183, S184, S185, S186, S188, S189, S190 — exactly `w2/ScoutAppendDebt.md`'s list.

"Before round 34": the 16 routed ids' changed_at commits are `5126891` (round-32, 2026-10-22T23:05:39-03),
`62db24c0` (round-33, 23:55:24), `ab8f4cf` (round-33 wave-2, 2026-10-23T00:08:53) — all earlier than the
first round-34-labelled commit `2460318` 2026-10-23T01:53:22-03 ("round-34: freeze C1/C2 contract …").
S182's second change (`8d56809`, round-34 02:34:40) and S193's (`406d91a4`, round-34 05:00:15) are round-34
events, correctly outside the routed claim and already discharged by S201/S202. Checker total 18 = routed 16
(15 + S069) + S182 + S193. (QUALITY 102's "all changed in place before round 35", `corpus/QUALITY.md:809-810`, also holds: last in-place edit 05:00:15, round-35 begins with `cedb0ec` 06:06:42.)

## Deleted rows

None, in the whole lane history through 6bd57097. Evidence:

- 204 ids ever held = 204 ids at tip; zero ids present earlier and absent at 6bd57097.
- Zero deletion events across the 47 consecutive content snapshots (id present in snapshot k, absent in k+1).
- Merge audit: only 2 merges in ancestry. `6531ac6` is TREESAME to parent bf7cdc4 for SOURCES and the diff vs parent b2e1ca2 is `new file` (that side never had the file). `343077f` predates the file (absent at both parents). No hidden side-branch content: `git rev-list --full-history 6bd57097 -- corpus/SOURCES.md` = 48 = 47 + the creation merge.
- No rename history: `git log --follow --format=%h -- corpus/SOURCES.md` = 47, same as without `--follow`.
- SOURCES.md is byte-identical from 6bd57097 to clone HEAD c1a026cb and to the live lane HEAD 5842dc04 (`git diff --stat` empty at both), so the list is current at the tip as of measurement.

So QUALITY 102's declared gap "Not covered: deleted rows" (`corpus/QUALITY.md:810`) has zero instances in
lane history; the gap is real as a checker capability but empty as a debt.

## Findings

1. The routed claim's id list re-derives exactly: 15 pre-round-34 in-place ids, none superseded, plus S069
   (in-place edited in round 33 after S073 had already superseded it in round 20; the round-35 checker
   revision correctly keeps it listed with superseded_by=S073). The spotcheck's exclusion of S182/S193 is
   right: their in-place edits are round-34 events, and S201/S202 supersede them.
2. First-held cells for the 3 sampled ids confirmed by literal `git log -p` walk, independently of the checker.
3. No row was ever deleted from the registry through 6bd57097 (census above).
4. The checker and my parser agree id-for-id; the checker's blind spots (merge simplification) were audited
   and found empty for this history.

VERDICT: agree

## Residual risk and verification gaps

- Net-cell semantics: origin-vs-tip comparison; per-commit intermediate cells are reflected only in the
  changed_at lists (full for every flagged id). Full first/tip rows were printed for the 3 samples only.
- The deletion census covers 6bd57097's ancestry (the lane history the checker defines); refs outside that
  ancestry are out of scope by construction.
- Whether round-33's partial old-to-new logging (S041, S044, S051, S062, S064) satisfies the log half of
  rule 2 while violating the supersede half is a judgment for the L1; this seat only confirms the in-place
  fact and the absence of supersede rows for the 15.
- The lane moved during measurement (6bd57097 → c1a026cb → 5842dc04); SOURCES.md verified unchanged across
  all three, but later commits after 5842dc04 are not covered.
- No counter, gate or lane tool other than the named checker was executed; the checker ran read-only in a
  sandbox clone. [INFERENCE] none: all numbers above are command outputs.

## Artifacts and containment

- Scratch: `/fast/scratch/hyaku/mori-r36/ReviewDebtList/` — `clone/` (sandbox, read-only use), `rederive.py`
  (sha256 11558e9eaa87075031064acb611b119f005de4799a1faf75f31cfb751b1f3718). No other writes; no lane file
  besides this report. No processes left running; no tool installs (existing python3/git sufficient).
