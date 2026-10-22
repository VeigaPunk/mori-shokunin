# ReviewLateMutHeadingCheck — re-verify late r28-w2 `MutHeadingCheck.md` at `7118f320`

Seat: MoriR29.ReviewLateMutHeadingCheck (reviewer, leaf). Assignment: re-verify every finding of the inherited
untracked file `.ufo/waves/round-28/w2/MutHeadingCheck.md` against the committed lane at
`7118f320a5ef18d20c1e361eff77db0e1a97b2d6` in a sandbox clone; re-run its mutations/scenarios; judge impact on
round 28's admitted C1/C2 and QUALITY 83/84; privacy-check the file; recommend commit or dispose.

## Basis of comparison (all observed this run)

- Target bytes unchanged across the whole interval:
  `git show <r>:.ufo/waves/round-28/check-heading-time.py | sha256sum` for r in
  `f2de0eedcd60d2e354da75265ea6122bc3896073`, `7118f320a5ef18d20c1e361eff77db0e1a97b2d6`,
  `8a45cefe84af0557b457308e4e0f679ca490f9e9` (lane HEAD, contract landed), HEAD — all print
  `2ef80ed1fc546364c30fbc4ccc8de8375dba542cae45ec5126770795f0eeb040`, the pristine sha256 the file claims.
- `git log --oneline 7118f320..HEAD -- .ufo/waves/round-28/check-heading-time.py` prints nothing: **no later
  commit touches the script**, so nothing below is "closed by a later commit".
- `git merge-base --is-ancestor f2de0e 7118f320` → true.
- Working tree: `git status --porcelain` lists `check-heading-time.py` neither modified nor untracked →
  worktree bytes equal committed bytes.
- Harness-adapted pristine: I applied the file's own one-line adaptation (`import os` +
  `LANE = os.environ.get("MORI_LANE", ...)`) to the 7118f320 bytes → sha256
  `db5cb98e47da6ae42548f72a93ac84d6013073f89776cdb6230b2c1638d15706` — **byte-identical** to the hash the
  file records, so my variant generation reproduced theirs exactly.
- Sandbox: `git clone --no-hardlinks` lane → `/fast/scratch/hyaku/mori-r29/MoriR29.ReviewLateMutHeadingCheck/lane`
  (all git writes `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE`); fixture repo
  `…/fixture` (`git init`, commits A0–A12 with invented `GIT_*_DATE`s and `t@example.invalid`); variants under
  `…/variants/`; recorded outputs `results_host.txt`, `results_py310.txt` under the same scratch dir.
- Premise re-confirmed on this host (git 2.56.0): UTC commit `1b7d811f` logs
  `aI=2026-10-30T10:00:00Z cI=2026-10-30T10:00:00Z` — git really does emit `Z`.

## Findings re-verified

| id | claim (their words, compressed) | re-run (all runs: adapted bytes, `MORI_LANE=<fixture>` unless noted) | observed | status |
|---|---|---|---|---|
| F1 | renamed file rebinds heading to rename commit → future-dated heading passes | `pristine.py A8 mut/move-dst.md` | `added_by=b8df6962a333 … bound=2026-10-21T09:00:00-03:00 delta_s=68400 verdict=ok`, `headings=1 future_dated=0`, exit 0 | **reproduced open** |
| F2 | M17 (`Z` rewrite deleted, :44-45) equivalent on 3.11+, fatal ≤3.10 | `uv run --python 3.10 --no-project python -I -B {pristine,M17}.py A9 mut/utc.md` | pristine `verdict=FUTURE-DATED` rc 1; M17 `ValueError: Invalid isoformat string: '2026-10-30T10:00:00Z'` rc 1 | **reproduced open** |
| named-1 | r27 contract must fail @f2de0e | `check_heading_time_7118f320.py f2de0e .ufo/waves/round-27/contract.md` | `stated=2026-10-22T15:55Z … cI=2026-10-22T12:50:10-03:00 verdict=FUTURE-DATED`, second heading day/ok, `headings=2 future_dated=1`, exit 1 | reproduced open (checker correct here) |
| named-1b | same @df886be1 | same, rev `df886be1` | `headings=1 future_dated=1`, exit 1 | reproduced open |
| named-2 | r28 contract must pass @f2de0e | `… f2de0e .ufo/waves/round-28/contract.md` | `headings=1 future_dated=0`, exit 0 (heading :73 day granularity) | reproduced open |
| M10 | level-1 dated headings unchecked (`#{2,6}`, :34); lane r17 contract :1 not checked | fixture `mut/level1.md@A12`; lane `round-17/contract.md@f2de0e` | fixture pristine `headings=1` vs M10 `headings=2`; lane pristine `headings=2` vs M10 `headings=3` (line :1 `# mori round 17 … (L1-authored, 2026-10-20)` counted only by mutant) | reproduced open |
| M12 | bad rev should exit 2; mutant exits 0 | `… deadbeefdeadbeef mut/base.md` | pristine `bad_rev` rc 2; M12 `bad_rev` rc 0 | reproduced open (coverage gap) |
| M13 | missing file should exit 2 | `… HEAD mut/nope.md` | pristine `missing_file` rc 2; M13 `missing_file` rc 0 | reproduced open (coverage gap) |
| M21 | usage error should exit 2 | `…` (no args) | pristine usage rc 2; M21 usage rc 0 | reproduced open (coverage gap) |
| M22 | bad arg should exit 2 | `… HEAD mut/base.md --nope` | pristine `bad_arg --nope` rc 2; M22 `bad_arg --nope` rc 0 | reproduced open (coverage gap) |
| M14 | `--bound aI` ignored (documented flag :99-103) | `… A10 mut/bound.md --bound aI` (aI 10-19 < heading 10-21 < cI 10-23) | pristine `bound=2026-10-19T00:00:00+00:00 verdict=FUTURE-DATED` rc 1; M14 `verdict=ok` rc 0 | reproduced open (coverage gap) |
| M15 | `--heading` filter ignored | `… A11 mut/two.md --heading Past` | pristine `headings=1` rc 0; M15 `headings=2 future_dated=1` rc 1 | reproduced open (coverage gap) |
| M17 | (see F2) host python3 3.14.8 | `… A9 mut/utc.md` | pristine and M17 identical: `FUTURE-DATED` rc 1 | reproduced (equivalent ≥3.11) |

"Reproduced open" = behavior re-observed at 7118f320 bytes with no fix commit. For the exit-code/flag items the
finding is a *coverage gap in the assigned detector*, not a checker bug: each differential above shows the mutant
is killed only by a scenario outside the task-named families (all runs above satisfy baseline: pristine behaves
per criterion 83 on the same input). Tier-A survival itself follows structurally from the file's own named-family
list (date-only / zone-less / instant / moved-line / merge / the two lane must-fail/must-pass runs) containing no
level-1-heading, exit-code or CLI-flag case — [INFERENCE] from that list, not re-run of the full matrix.

### F1 mechanics re-observed (fixture A7 `39434eaa` authors the line, A8 `b8df696` is `R100` rename)

```
git -C fixture log --format='%H %aI %cI' -S'## Moved (2026-10-20 ~14:00)' A8 -- mut/move-dst.md
→ b8df6962a33346ebcd4c1b59e37fd9f1c9f2cc24  (the rename — what the checker binds)
git -C fixture log --format='%H %aI %cI' -S'## Moved (2026-10-20 ~14:00)' A8   (no path filter)
→ 39434eaaeeed217e6c6827a70d42fd8bc8373dbf  (the true adding commit A7)
pristine at A7 on mut/move-src.md: verdict=FUTURE-DATED  delta_s=-18000  exit 1   (heading catches correctly)
pristine at A8 on mut/move-dst.md: verdict=ok            delta_s=+68400  exit 0   (fail-open)
```

Erratum in the inherited file, marked for the lesson: its parenthetical "`git log --follow` does not help (`-S` +
`--follow` returns nothing)" is **not reproduced** — on git 2.56.0
`git -C fixture log --follow --format='%H' -S'## Moved (2026-10-20 ~14:00)' A8 -- mut/move-dst.md` returns
`39434eaaeeed` (A7), i.e. `--follow` recovers the true author in this minimal shape. F1 itself stands; only that
secondary claim about the fix space is overstated, and whether `--follow` suffices on real rename histories is
not proven either way here.

## Impact on round 28's admitted verdicts

- **C1/C2: unchanged.** Round-28's counters are `count-c1.sh` / `count-c2.sh`; `check-heading-time.py` is the
  QUALITY-83 instrument, not an input to either counter. No evidence path from the checker to the admitted counts.
- **QUALITY 83: unchanged for every past check.** The defect is fail-*open* (misses future-dated headings, never
  invents them) and triggers only after a rename. Lane rename census at 7118f320:
  `git log --name-status --diff-filter=R 7118f320 -- .ufo` prints **zero** R-status entries — no `.ufo` file was
  ever renamed, so every criterion-83 verdict ever taken bound to the correct commit. The named runs re-observed
  above (r27 fails, r28 passes at day granularity) are the honest outcomes criterion 83 prescribes.
- **QUALITY 84: untouched.** That criterion is exercised by `check-tip-receipts.sh`, not this script.
- **Forward risk (recorded, not a score change):** any future contract-file rename + a heading later-dated than
  its authoring commit will pass silently; the single level-1 dated heading in the lane
  (`.ufo/waves/round-17/contract.md:1`) is unchecked; `fromisoformat` `Z` handling is the only guard between a
  UTC commit and a crash on Python ≤3.10 (criterion 83 invokes bare `python3`, no pinned interpreter — host
  python3 is 3.14.8, so no live defect here).

## Privacy / commit-safety review of `MutHeadingCheck.md`

- `grep -nE 'user-[0-9]{3,}\.slice|user@[0-9]{3,}\.service|\bpid[ =:]*[0-9]{3,}|\buid[ =:]+[0-9]{3,}|/etc/default|prefer|avoid|ignore=|\.omp/|session|oom'` → **no hits**. No harness settings values, uids, pids, user-session unit names, host command lines, or `/etc/default/earlyoom` contents. Paths shown are repo/scratch paths only (`/home/vgpnk/…`, `/fast/scratch/…`); the elided `LANE = "/home/vgpnk/..."` quotes no new value.
- Blindness: the file contains no `mori-oom-killers` source lines, tool output or `MORI_OOM_KILLERS_SELFTEST` markers; it never reads the oom-killers tool.
- Fixture values in it are invented (A7/A8 dates); git shas are lane objects.

## Recommendation

**Commit as evidence.** The file documents a true, re-verified fail-open (F1) and a real portability finding
(F2), plus eight detector coverage gaps; its main claims reproduce byte-for-byte. One secondary claim (the
`--follow` parenthetical) is inaccurate on git 2.56.0 — worth one line in the round-29 lesson under carried
debt, not a reason to dispose. It is privacy-clean and in-scope (targets only `check-heading-time.py`).

## Tools and bounds

- Tools: host python3 3.14.8; `uv` 0.13.0 at `~/.local/bin/uv` reusing pre-existing cpython 3.10.22; git 2.56.0.
  **Nothing installed or upgraded**; `RULES.md` obligation noted, pacman untouched.
- Wrote only this report and files under `/fast/scratch/hyaku/mori-r29/MoriR29.ReviewLateMutHeadingCheck/`;
  all lane git read-only; no subagents, no background jobs; never opened `tools/mori-oom-killers.py` or any
  round-26/27/28 report other than the assigned file.
- Limits: the 15 killed mutants were not re-run individually (the file makes no *finding* about them beyond the
  tabulated kills); the `--follow` fix-space question for multi-hop rename chains is noted but not settled.

Report: .ufo/waves/round-29/w1/ReviewLateMutHeadingCheck.md
