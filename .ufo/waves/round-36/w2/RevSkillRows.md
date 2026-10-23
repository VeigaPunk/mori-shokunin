# RevSkillRows — round-36 wave-2 gate-registry review

Attacks: gate-registry integrity for the three new Round36 rows in `SKILL.md`
(source drift, SOURCES append-only, index clean).

Seat: `mori-r36-w2-RevSkillRows-13`. Lane repo read-only; no files in the lane
were modified. Scratch only under `/fast/scratch/hyaku/mori-r36/RevSkillRows/`.

## Ground truth used

- `PROTOCOL.md` §Gate standard (fleet root, /home/vgpnk/Projects/shokunin/PROTOCOL.md,
  lines 375–413): row fields = name, `gate|probe`, entry command, verdict map
  (code → class), self-test command and spelling, pinned-value path, write scope, owner.
- `SKILL.md` Round36 section (lines 856–874): prose guidance plus the registry
  table with header `| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |`.
- Measured revision: HEAD = `bf0df77fee4b6ef54a90aea09335c7617f125151`
  (the landed data tip). All three tools are committed at that tip
  (`git ls-tree bf0df77 tools/` → mori-source-drift.py 103965ac…, mori-sources-appendonly.py dfb5040b…, mori-index-clean.sh d171da39…).

## 1. Field presence (all three rows)

| row (SKILL.md line) | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|---|
| source drift (r36) — line 872 | probe | `python3 tools/mori-source-drift.py --root <repo>` | 0 `drifted=0` · 1 `drifted>0` · 2 could-not-evaluate | `--selftest` (offline 127.0.0.1 fixture) | newest copy `corpus/evidence/sources-r<N>/<id>.<ext>` per row; live URL bodies | none (read-only) | mori |
| SOURCES append-only (r36) — line 873 | gate | `python3 tools/mori-sources-appendonly.py <rev> [--repo DIR] [--round-base REV] [--path P]` | with `--round-base`: 0 `round_changed=[]` · 1 non-empty; without: 0 no `ids` and no `deleted` · 1 otherwise; 2 git or parse error | `--selftest` (8 sandbox histories through CLI) | git history of `corpus/SOURCES.md`; immutable = every column but status, recheck, used-by | none (read-only git) | mori |
| index clean (r36) — line 874 | gate | `bash tools/mori-index-clean.sh <repo>` | 0 `staged=0 intent_to_add=0` · 1 staged or intent-to-add (≤20 paths) · 2 usage/not-a-repo/git error/porcelain v1-v2 disagreement | `--selftest` (clean, `add -N`, `add`, not-a-repo) | the repo's git index | none (`--no-optional-locks`) | mori |

All eight gate-standard fields are present in each row; kinds are correctly
assigned (source drift is a probe per the C1 exploratory declaration; the other
two are gates). No missing field.

## 2. Entry commands run at bf0df77 with mapped exits

All commands run from `/home/vgpnk/Projects/shokunin/mori-shokunin` (worktree at
bf0df77), read-only.

### source drift (probe)
Command: `python3 tools/mori-source-drift.py --root .`

Observed output (tail; full 222-line output in scratch `drift-run.out`):
```
S219 fresh
S220 fresh
MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162
```
`echo $?` → `1`. Drifted ids: S156 S157 S158 S159 S160 S176 S177 S210 S211 —
identical set to the `evidence/c1-after.txt` receipt (fresh=49 drifted=9).
Map says 1 `drifted>0` → **mapped exit observed** (1).

### SOURCES append-only (gate), with `--round-base`
Command: `python3 tools/mori-sources-appendonly.py bf0df77fee4b6ef54a90aea09335c7617f125151 --round-base 6bd57097`

Observed output (tail):
```
changed S190 superseded_by=S220
changed S193 superseded_by=S202
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[]
```
`echo $?` → `0`. Map says with `--round-base`: 0 `round_changed=[]` → **mapped exit observed** (0). Matches L1's stated gate run.

### SOURCES append-only (gate), without `--round-base`
Command: `python3 tools/mori-sources-appendonly.py bf0df77fee4b6ef54a90aea09335c7617f125151`

Same output line with `round_changed=[]`; `echo $?` → `1`. Map says without:
0 no `ids` and no `deleted` · 1 otherwise; ids non-empty → **mapped exit observed** (1).

### index clean (gate)
Command: `bash tools/mori-index-clean.sh /home/vgpnk/Projects/shokunin/mori-shokunin`

Observed output:
```
MORI_INDEX_CLEAN staged=0 intent_to_add=0
```
`echo $?` → `0`. Map says 0 `staged=0 intent_to_add=0` → **mapped exit observed** (0).
(Untracked files and an unstaged worktree edit to dispatch-log.txt exist in the
worktree; per the tool's and row's semantics they are not index state and do not
count — consistent with QUALITY 103.)

## 3. Self-tests (as recorded in the rows)

| row | command | observed | tally per row |
|---|---|---|---|
| source drift | `python3 tools/mori-source-drift.py --selftest` | `MORI_SOURCE_DRIFT_SELFTEST: PASS (4 cases)` exit 0 | offline 127.0.0.1 fixture |
| SOURCES append-only | `python3 tools/mori-sources-appendonly.py --selftest` | `MORI_SOURCES_APPENDONLY_SELFTEST pass=8 fail=0` exit 0 | 8 sandbox histories through the CLI |
| index clean | `bash tools/mori-index-clean.sh --selftest` | `MORI_INDEX_CLEAN_SELFTEST pass=4 fail=0` exit 0 | clean, `add -N`, `add`, not-a-repo |

All pass with the claimed tallies and exit 0.

## Findings

No defects found. No missing field and no wrong exit map in any of the three
Round36 rows; each entry command runs at bf0df77 and exits per its documented map.

## Residual risk / verification gaps

- The source-drift probe is live-network; counts can vary day-to-day, but the
  observed run reproduced the receipt's classification exactly (fresh=49
  drifted=9, same drifted ids), and the exit followed the map.
- `evidence/c2-after.txt`'s real arm shows `round_changed=[S182,S193]` exit 1 —
  that run used the counter-internal round base (f10a320d), not the registry
  row's input contract; the row's verdict map was verified with the round base
  the assignment cites (6bd57097) and held. Counter-internal behavior is out of
  this seat's registry scope.

## VERDICT: PASS

(no defect found — all three gate-registry rows carry the gate-standard fields
and their entry commands run at bf0df77fee4b6ef54a90aea09335c7617f125151 with the
mapped exits)
