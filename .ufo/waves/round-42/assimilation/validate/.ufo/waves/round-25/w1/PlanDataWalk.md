# Round 25 wave 1 — planner data walk (C1 before-state, C2 before)

Seat: MoriR25.PlanDataWalk. Date 2026-10-22. Read-only measurement; this file is the only write.

## Method

All facts come from committed bytes via read-only git (`cat-file`, `show`, `rev-parse`, `ls-tree`,
`archive`, `log`), plus `python3 -I -B` selftest runs from temporary `git archive` extracts under `/tmp`.
No jj, no git write, no `omp` invocation, no settings touched, no tool installed.
Environment: Python 3.14.8, git 2.56.0.

Lane state at walk time (read-only `git status --porcelain`): HEAD
`129832e3e8a710d47ecd0425efb9fc67ecf59697`, two commits past `7634be75`; uncommitted ` M .gitignore`
and untracked `.scratch/`, `.ufo/waves/round-25/w1/QualityCriteriaDraft.md` were already present and
were not touched.

## D1 — stale gate evidence

**Existence of the round-25 evidence file.**

| Command | Output |
|---|---|
| `git cat-file -e 28b79d3d:.ufo/waves/round-25/evidence/pressure-selftest.txt` | `fatal: path '.ufo/waves/round-25/evidence/pressure-selftest.txt' does not exist in '28b79d3d'`; exit 128 |
| `git cat-file -e 7634be75:.ufo/waves/round-25/evidence/pressure-selftest.txt` | same fatal; exit 128 |
| `git ls-tree -r --name-only 7634be75 .ufo/waves/round-25` | `.ufo/waves/round-25/contract.md` (only file; no `evidence/`) |

**Round-24 capture vs the tool's actual stdout.**

| Command | Output |
|---|---|
| `git show 28b79d3d:.ufo/waves/round-24/evidence/c2-selftest-after.txt \| cat -A` | `MORI_PRESSURE_SELFTEST: PASS 12/12$` — 35 bytes, blob `4618daf95d9a612f8f18a04e29520cb599e92862`; no `revision:`, no `exit:`, no `MATCHER` line |
| `T=$(mktemp -d); git archive 7634be75 tools \| tar -x -C "$T"; cd "$T"; python3 -I -B tools/mori-pressure.py --selftest` | exit 0; stdout 82 bytes, sha256 `d767d1b6fd53e45caaeae8ca430f54f91badc08f89676a4d606bd1e2ac0be16f`: <br>`MORI_PRESSURE_SELFTEST: PASS 12/12`<br>`MATCHER: rejected 48/48 corrupted expectations`<br>stderr 0 bytes |
| same from `28b79d3d` extract | exit 0; identical stdout sha256 `d767d1b6…` (tool blob `5785c5b23233a5ed1d2116ab610f9aa0cf3b12ec` and fixtures tree `060f60f6e336da814ec4f0d33c47b18eb582089b` are identical at `28b79d3d`, `7634be75` and HEAD) |
| `git log --diff-filter=A --format='%h %ad %s' -- .ufo/waves/round-24/evidence/c2-selftest-after.txt` | `89849a7 … pressure selftest gains matcher negative controls and a co-evolved supplementary case file` |
| `git log -S 'MATCHER: rejected' -- tools/mori-pressure.py` | `89849a7` — the MATCHER line entered the tool in the same commit that added the capture, yet the capture holds only the first line |

Verdict: the file does not exist at either rev → **D1 unheld at both revs**. The round-24 file is exactly
line 1 of its own commit's stdout (same-commit stale capture), and the current tool prints two lines.

## D2 — knowledge entry wording

Blob `corpus/knowledge/system-pressure-r24.md` = `d4ccce4262d8224e362da65eb5ba4b851ad0fea2` at
`28b79d3d`, `7634be75` and HEAD (identical bytes).

One Corrections section: heading at line 8 `## Corrections after wave-2 falsification (round 24, before
closure)`, body lines 8–42.

Line breaks folded to single spaces, matches outside that section:

| Phrase | Matches | Source span |
|---|---|---|
| `refreshed on each read` | 1 | lines 94–95 |
| `a shorter spike between two reads can be invisible` | 1 | line 170 |
| `` `null` means *undefined* `` | 1 | line 171 |

`(K4)` occurrences in the whole file: **0** (so no `## Corrections` section contains it).

Verdict: **D2 unheld at both revs** (3 body hits outside Corrections, no K4 row).
Line numbers match the spot-check's `4f05dd5a` cites (94–95, 170, 171).

## D3 — lesson count drift

| Command | Output |
|---|---|
| `git show 4f05dd5a:tools/fixtures/mori-pressure/supplementary-cases.json` (parsed `cases`) | 7 cases, ids `S01…S07` → n = 7 |
| `git show 28b79d3d:corpus/lessons/round-24.md \| grep -n 'PASS'` | one hit, line 80: ``… (`PASS 6/6`). Non-UTF-8 content is now `malformed`…``; lines 79–80 name `S01–S06` |
| lesson blob | `779a07952ca57de06b9d7c33d812c510c3dd028f`, identical at `28b79d3d`, `7634be75`, HEAD |

Zero lines contain capital `Correction`, so no line contains both `Correction` and `PASS n/n`; the only
`PASS n/n` on disk is `PASS 6/6` (≠ `PASS 7/7`).
Verdict: **D3 unheld at both revs**.

## D4 — `__pycache__` hygiene

`.gitignore` blob `32e57724a32b990da249692836336b9f370eece5`, identical at `28b79d3d`, `7634be75`, HEAD:

```
1  .ufo/interactive-sessions/
2  .ufo/worktrees/
```

No line equals any of `__pycache__/`, `__pycache__`, `**/__pycache__/`, `tools/__pycache__/`, `*.pyc`,
`*.py[cod]`. Verdict: **D4 unheld at both revs**.

Related working-tree fact (not mine, not touched): `git status --porcelain .gitignore` → ` M .gitignore`;
worktree line 3 is `__pycache__/`, and `git check-ignore -v tools/__pycache__` →
`.gitignore:3:__pycache__/` (one file inside `tools/__pycache__/`). The held predicate reads the
`.gitignore` blob at REV, so this uncommitted edit does not count until committed.

## C1 before aggregate

| Rev | D1 | D2 | D3 | D4 | held | mismatches |
|---|---|---|---|---|---|---|
| `28b79d3d1b76824f0c825aabe6cb6c5dc49961bf` | unheld | unheld | unheld | unheld | 0 | 4 |
| `7634be75c74891b5cd2815d0bd5374f89abd7087` | unheld | unheld | unheld | unheld | 0 | 4 |

`tools/mori-routed-r24.py` does not exist at either rev (`git cat-file -e` exit 128 at both), so
`mismatches: 4` is the contract's arithmetic over the four measured items, not a tool output. It matches
the contract's declared before (`mismatches: 4` at `28b79d3d`).

## C2 before

| Command | Output |
|---|---|
| `git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e 28b79d3d:tools/mori-job-runway.py` | `fatal: path 'tools/mori-job-runway.py' does not exist in '28b79d3d'`; **exit 128** |
| same at `7634be75`, HEAD | exit 128, exit 128 |
| `git show 7634be75:tools/fixtures/mori-job-runway/cases.json` | 21 cases, ids `J01…J21` (frozen before any tool, as committed at `7634be75`) |
| `git cat-file -e 28b79d3d:tools/fixtures/mori-job-runway/cases.json` | exit 128 |

C2 before confirmed: the tool is absent.

## Current tip (context, not part of the before measurement)

HEAD `129832e3…` is 2 commits past `7634be75`; `0099a39` and `129832e` add round-25 SCORECARD/LOG/
contract-metadata files only. At HEAD: no `pressure-selftest.txt` (128), no `tools/mori-routed-r24.py`
(128), no `tools/mori-job-runway.py` (128); `.gitignore`, knowledge entry and lesson blobs are still the
`28b79d3d` blobs. Both after-values remain unlanded as of this walk.

## Confidence and remaining unknowns

- Observed (high confidence): every row above is a direct object read or a recorded exit code; selftest
  runs reproduced byte-identically from two revs.
- Unknown: the round-24 capture names no revision, so its capture time cannot be recovered from
  committed bytes; its staleness is established only by output comparison with its own commit `89849a7`.
  Nothing else material to the assigned before-state.
