measured 2026-10-23T09:32:54Z
# Residual re-judge — QUALITY 102 (ResQ102Check)

Scope: revised checker `.ufo/waves/round-35/check-sources-appendonly.py` (tip `6d3d94b3`, working-tree
blob diffed byte-identical to `6d3d94b3:.ufo/...`, diff_rc=0; scratch copy at
`/fast/scratch/hyaku/mori-r35/MoriR35.ResQ102Check/`). Ran from scratch with `--repo
/home/vgpnk/Projects/shokunin/mori-shokunin`, timeout ≤110 s, read-only git only.

## Run 1: `dd76eb79 --round-base f10a320d` (round 34 window; f10a320d = round-33 tip, dd76eb79 = round-34 tip)

stdout: `rev=dd76eb79... rows=198 commits=46`; 18 `CHANGED id=` lines (S041,S044,S051,S062,S064,S069,
S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193), each with `origin=`, `changed_at=`, `cols=`,
`superseded_by=` (only S069 has `superseded_by=S073`); then
`appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] superseded=[S069]`
and `round_changed=[S182,S193]`. EXIT=1.

VERDICT: supported — criterion states `round_changed=[S182,S193]`, exit 1; observed exactly.

## Run 2: `6d3d94b3 --round-base dd76eb79` (round 35 tip window)

rows=204 commits=47; same 18 CHANGED ids; `superseded_by=S201` on S182, `S202` on S193, `S073` on S069;
`appendonly_violations=18 ids=[same 18] superseded=[S069,S182,S193]`; `round_changed=[]`. EXIT=0.

VERDICT: supported — `round_changed=[]` exit 0; 18 ids stay listed; exactly S069/S182/S193 superseded,
the other 15 not; all 18 changed in place before round 35 (every `changed_at` is an ancestor of
dd76eb79 — verified via round-34-window membership for S182/S193 and `merge-base --is-ancestor` checks
for 62db24c0/ab8f4cfe/5126891f vs f10a320d for the rest).

## Run 3: `cedb0ec4 --round-base dd76eb79`

Output byte-for-byte identical to run 2 (rows=204, 18 ids, superseded=[S069,S182,S193],
`round_changed=[]`). EXIT=0.

VERDICT: supported — consistent with `git diff cedb0ec4..6d3d94b3 -- corpus/SOURCES.md` being empty
(tip commit changed no SOURCES rows); same verdict as tip.

## Exit-2 error path

`deadbeef --round-base f10a320d` → stderr `error: git rev-parse --verify deadbeef^{commit} failed: ...`,
EXIT=2. Matches "exit 2 is an error".

VERDICT: supported.

## Lesson M2 row (corpus/lessons/round-35.md:66 at 6d3d94b3)

States: `dd76eb79 --round-base f10a320d` → `round_changed=[S182,S193]`, exit 1 — supported (run 1).
States: at tip `--round-base dd76eb79` → `round_changed=[]`, exit 0 — supported (run 2).
States: `18 ids stay listed (S069, S182, S193 superseded; 15 routed debt)` — supported (run 2:
18 ids, 3 superseded, 15 not).

VERDICT: supported for each stated number above.

## Finding (low): stale middle-cell count in M2 row

M2's middle cell also says `the check also finds 15 ids edited in place before round 34`. Under the
revised checker this is off by one. Derivation: 18 violations minus the 2 whose in-place edits occurred
inside the round-34 window (S182 at `8d56809a`, S193 at `406d91a4`) = 16 ids edited only before
round 34 — and 17 counting S182, whose earlier edit `ab8f4cfe` is also pre-round-34
(`git merge-base --is-ancestor ab8f4cfe f10a320d` true). The old count 15 was correct only under the
pre-revision checker, where S069 was discharged by `supersedes S073` (MutQ102 historical receipt:
`appendonly_violations=17` without S069; 17−2=15). The revision that retains S069 invalidated the
middle-cell figure while the tail cell was correctly updated to 18. Fix: `15` → `16` (or rephrase).

VERDICT: defect — M2 row middle cell ("15 ids edited in place before round 34") fails under the revised
checker; observed 16 (strict) or 17 (any pre-round-34 edit incl. S182's `ab8f4cfe`).

## Residual risk / verification gaps

- Not re-audited: whether the 18 CHANGED ids' `origin=`/`changed_at=` values are individually correct
  (spot-checked ancestry only). Not in scope of the stated numbers.
- `supersedes` disposition is prefix-matched on the teaches cell of tip rows; S201/S202 supersede
  claims were taken from the checker output, not re-verified against the SOURCES table bytes (the
  lessons table at lines 20-21 does show `supersedes S182`/`supersedes S193` teaches prefixes).
- Error path covered only for unresolvable rev; timeout/malformed-row die() paths not exercised.

No installs; no lane/git writes; scratch only under /fast/scratch/hyaku/mori-r35/MoriR35.ResQ102Check/.
