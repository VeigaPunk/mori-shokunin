measured 2026-10-23T09:11:25Z

# ReviewAxesFix — round 35 wave 2

Seat: MoriR35.ReviewAxesFix (reviewer, leaf). Scope: SCORECARD.md lines 11-12
(`## Axes` operability and depth rows) at `cedb0ec4f3a4f672804deac388b7191258f01fcd`
vs `dd76eb79`; the new "Last change" cells and appended evidence text against fleet
`MANIFEST.json@37b51a24` and `corpus/lessons/round-31-verifier-spotcheck.md:154-155`;
plus whether `tools/mori-routed-r24.py`'s D5 check still passes on the new table.

## What changed (git diff dd76eb79..cedb0ec SCORECARD.md, hunk @@ -8,8)

- Operability row: evidence cell gains a round-28 back-reference and a
  "latest admitted closure grades operability improved (blind-writer gate
  `tools/mori-blind-check.sh`, C2 verified) and states the score stays 7
  (`corpus/lessons/round-31-verifier-spotcheck.md:155`)" clause plus a
  round-35 correction note; Last change `round 28 (improved, score held)` ->
  `round 31 (improved, score held)`.
- Depth row: evidence cell gains "latest admitted closure grades depth improved
  (watchdog identity decision table, C1 re-measured) and states the score stays 5
  (`corpus/lessons/round-31-verifier-spotcheck.md:154`)" plus a round-35
  correction note; Last change `round 12 (4 → 5)` -> `round 31 (improved, score held)`.

## Verdicts

VERDICT: supported — operability "Last change = round 31 (improved, score held)".
Fleet `MANIFEST.json@37b51a24` rounds[495] records mori round 31 `admitted`,
`verdicts.operability: improved`, spotcheck
`mori-shokunin/corpus/lessons/round-31-verifier-spotcheck.md@641a6e86`; the cited
lesson `round-31-verifier-spotcheck.md:155` reads "operability | improved | C2
verified (§3); the score stays 7". No later closure is admitted: rounds 32, 33, 34
(MANIFEST rounds[498],[504],[524]) are all `rejected-honest-stop` with operability
`unchanged`, so round 31 is correctly the latest admitted closure for the cell.

VERDICT: supported — operability evidence clause names and cites the right claim.
Lesson §C2 header `round-31-verifier-spotcheck.md:109` is "C2 — operability:
`tools/mori-blind-check.sh` — verified (evidence-verified)", matching the cell's
"(blind-writer gate `tools/mori-blind-check.sh`, C2 verified)". The retained
round-28 clause also checks out: MANIFEST rounds[476] round 28 `admitted`,
`verdicts.operability: improved`.

VERDICT: supported — depth "Last change = round 31 (improved, score held)".
MANIFEST rounds[495] `verdicts.depth: improved` (admitted); the cited lesson
`round-31-verifier-spotcheck.md:154` reads "depth | improved | C1 verified (§3);
score stays 5 unless a closure states the move. This closure states none" — the
score is held at 5, matching the row's `| 5 |`. Round 30 also graded depth
improved but closed `rejected-honest-stop` (rounds[489]), and rounds 32-34 show
depth `unchanged`/`unprovable`, so 31 is the correct latest admitted cell value.

VERDICT: supported — depth evidence clause matches C1's subject. Lesson
`round-31-verifier-spotcheck.md:81` heads "C1 — depth: watchdog identity decision
table — verified (re-measured)", matching the cell's "(watchdog identity decision
table, C1 re-measured)". The pre-existing "round 27's depth improvement was
verified under a rejected-honest-stop closure and is not counted" is corroborated
by MANIFEST rounds[468] (round 27 `rejected-honest-stop`, depth `improved`).

VERDICT: supported — both appended "round-35 correction" disclosures are accurate.
The old cells at dd76eb79 really did say `round 28` (operability) and
`round 12 (4 → 5)` (depth) in Last change; the correction text states exactly that.

VERDICT: holds — `tools/mori-routed-r24.py` D5 check still passes on the new table.
The tool has a CLI (`--repo`, `--rev`, optional `--rerun`; main at
`tools/mori-routed-r24.py:891`; reads committed objects only, writes nothing —
docstring lines 10-12, `_git_env` uses `GIT_OPTIONAL_LOCKS=0`). Run from a scratch
copy (lane bytes untouched, `-B` so no `__pycache__`):
`timeout 120 python3 -I -B /fast/scratch/hyaku/mori-r35/ReviewAxesFix/mori-routed-r24.py
--repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev cedb0ec4...` →
`"status":"held","items":4,"held":4,"mismatches":0`, D5 row `"held":true`,
`"reasons":[]`, exit 0. Mechanism: D5 (`_check_d5`, `tools/mori-routed-r24.py:691`)
requires one row per axis, each score equal to the pinned `28b79d3d` lines
1499-1506 parse `{coverage 6, operability 7, depth 5, freshness 5, calibration 5,
adjacency 6}` — verified identical at `:1499-1506` above — and no moved-score row
with `round 1` (regex `\bround\s+1\b`, `:165`) in Last change. The new cells say
`round 31`, which cannot match `\bround 1\b` (the `2` in `12` and `3` in `31`
prevent a word boundary after `1`); coverage/depth evidence text containing
"round 12" sits in the third cell, not the parsed last cell. No stale-round-1
reason is emitted because scores 6/7/5 differ from round-1 5/6/4 only where the
Last change correctly says 26/31/31.

## Residual risk / gaps

- [INFERENCE] The correction phrase "the last score move" for depth's old
  `round 12 (4 → 5)` cell is consistent with the cell text and with
  `round-12-verifier-spotcheck.md:17` being cited as stating the move; I did not
  re-derive the round-12 table cell itself.
- D5's pinned-state parse is over `SCORECARD.md:1499-1506` at `28b79d3d`; those
  lines are a claim table plus a "Held and observed" sentence, parsed by regex —
  it yields all six axes today but is brittle to any future rewording at the base
  rev (impossible: base rev is committed bytes, so this is stable by construction).
- The MANIFEST round-31 record itself was not re-verified against fleet wave
  logs beyond the JSON fields shown; the spotcheck pin `641a6e86` is recorded but
  I checked the lesson at lane tip `cedb0ec`, not at that pin. [INFERENCE] The
  lesson file is append-only per lane convention and lines 154-155 sit in its
  core verdict table, so content at the pin should match, but this is unchecked.

## Tooling

No installs or updates performed; no tool was needed beyond system git/python3.

## Methods

`git show <rev>:<path>` and `git diff dd76eb79..cedb0ec -- SCORECARD.md` in the
lane (read-only); `git show 37b51a24:MANIFEST.json` parsed with python3 in the
fleet repo (read-only); routed tool copied to
`/fast/scratch/hyaku/mori-r35/ReviewAxesFix/` before execution so nothing ran
from the lane directory.
