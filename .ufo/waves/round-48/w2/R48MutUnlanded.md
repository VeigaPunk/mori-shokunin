# R48MutUnlanded — mori round 48 w2 (falsify)

**Attacked:** the kill-power of `--selftest` in `tools/mori-unlanded-check.py` @ e4dfff32d4f97c7ef250e9a7538fa75d4f284492 — 8 single-point mutations of a scratch copy, detector = `--selftest` (13 arms), pristine → mutated → restored per cycle.

**Verdict: BREAKS (coverage gap).** 6/8 mutants killed; **2 survived** — the selftest has no arm that (a) creates a git rename (`-z` rename-source skip is dead code to the suite) and (b) never exceeds the 50-path list cap. Both survivors were proven behavior-breaking by supplementary scratch probes.

Pristine baseline: `UNLANDED_SELFTEST pass=13 fail=0`, rc=0.

## Mutants

All edits were made to the scratch copy `.scratch/r48w2-R48MutUnlanded/work.py` only; the tracked tool was never opened by an edit tool.

| # | Point | Single-point mutation (scratch copy) | selftest result | Verdict |
|---|-------|--------------------------------------|-----------------|---------|
| M1 | top-level guard | deleted `if os.path.realpath(top) != os.path.realpath(repo): raise Setup(...)` in `check()` | pass=11 fail=2 — FAIL `subdirectory_is_setup_error` (no error), FAIL `cli_setup_rc2` (rc=1) | **killed** |
| M2 | `-z` rename handling | deleted `if xy[0] in "RC": i += 1` in `check()` | pass=13 fail=0, rc=0 | **SURVIVED** |
| M3 | scope prefix | dropped `or path.startswith("tools/")` in `in_scope()` | pass=12 fail=1 — FAIL `lessons_and_space_in_path_listed` (`tools/new tool.py` no longer listed, paths=1) | **killed** |
| M4 | `.scratch` exclusion | added `or path.startswith(".scratch/")` disjunct in `in_scope()` (see note) | pass=11 fail=2 — FAIL `outside_scope_and_scratch_not_listed` (`unlanded ?? .scratch/seat/out.txt`), FAIL `other_round_not_listed` | **killed** |
| M5 | staged records | `if in_scope(...)` → `if in_scope(...) and xy[1] != " "` (index-only `A `/`M ` records dropped) | pass=11 fail=2 — FAIL `staged_but_uncommitted_listed` (rc=0), FAIL `cli_dirty_rc1` (rc=0) | **killed** |
| M6 | round filter | `".ufo/waves/round-%d/" % round_number` → `".ufo/waves/round-"` | pass=12 fail=1 — FAIL `other_round_not_listed` (`unlanded ?? .ufo/waves/round-7/w1/Old.md` under round 8) | **killed** |
| M7 | exit codes | `return 1, lines` → `return 0, lines` in `run()` dirty path | pass=7 fail=6 — FAIL `untracked_late_result_exit1_names_it`, `modified_tracked_report_exit1`, `other_round_listed_for_that_round`, `lessons_and_space_in_path_listed`, `staged_but_uncommitted_listed`, `cli_dirty_rc1` | **killed** |
| M8 | list cap | `found[:LIST_CAP]` → `found` in `run()` (cap no longer applied) | pass=13 fail=0, rc=0 | **SURVIVED** |

Note on M4: the tool has **no explicit `.scratch` exclusion statement** — exclusion is emergent from the prefix whitelist in `in_scope()` (docstring: "`.scratch/` … outside the scope on purpose"). The minimal behavior-bearing point is therefore the whitelist itself; the mutant admits `.scratch/` to it. The dedicated arm `outside_scope_and_scratch_not_listed` kills it. Related single-token mutant (drop `"/" not in path`, the top-level-only `.md` guard) was **not** separately run; by arm analysis it would survive (`outside_scope_and_scratch_not_listed` writes `.scratch/seat/out.txt`, not a nested `.md`, and no arm writes a nested `.md`) — UNVERIFIED, left as a follow-up probe suggestion.

## Survivors — coverage findings (arm text that would kill them)

- **M2 (rename-source skip).** No selftest arm performs a rename, so the deleted branch is never observed. Probe (scratch sandbox `$D` = `.scratch/r48w2-R48MutUnlanded/probe-rename`: init, commit top-level `NOTE.md`, `git mv NOTE.md docs/NOTE.md`, run `--repo $D --round 8`):
  - pristine: `UNLANDED=clean round=8`, rc=0
  - mutant: `UNLANDED=dirty round=8 paths=1` / `unlanded NO E.md`, rc=1 — the rename source `NOTE.md` is consumed as a status record and re-sliced into a fictitious top-level `.md` (`E.md`), fabricating an unlanded path on a clean tree.
  - Killing arm text: sandbox arm that `git mv`s a top-level `NOTE.md` to `docs/NOTE.md` and asserts rc=0 / output == `['UNLANDED=clean round=8']` (and, for an in-scope rename, that exactly one `unlanded R. <dest>` line with the destination appears).
- **M8 (list cap).** Every selftest sandbox holds ≤3 in-scope paths, so `found[:LIST_CAP]` never truncates. Probe (`.scratch/r48w2-R48MutUnlanded/probe-cap`: 60 untracked files `.ufo/waves/round-8/w2/F00..F59.md`, run `--round 8`):
  - pristine: header `UNLANDED=dirty round=8 paths=60`, **50** `unlanded` lines
  - mutant: header `UNLANDED=dirty round=8 paths=60`, **60** `unlanded` lines — output exceeds the documented "at most 50" contract.
  - Killing arm text: sandbox arm with >50 in-scope paths asserting `len(out) == 51` and `out[-1]` is the 50th sorted path.

## Restoration evidence

- Mutants lived only in `.scratch/r48w2-R48MutUnlanded/work.py`; after every cycle it was overwritten from `pristine.py` and hashed.
- sha256 before and after all cycles, identical across tracked file, work copy, and pristine reference:
  `e6695e04026b3da93e0c6406737602a31265970cd5bdfa1ac1d44835ad6a2b85  tools/mori-unlanded-check.py`
  (same digest for `.scratch/r48w2-R48MutUnlanded/work.py` and `pristine.py`)
- Post-restore behavior: `--selftest` → `UNLANDED_SELFTEST pass=13 fail=0`, rc=0.
- `git status --porcelain=v1 -- tools/` → empty (0 lines); lane HEAD unchanged at `e4dfff32d4f97c7ef250e9a7538fa75d4f284492`. No git state was mutated; no sibling files touched.

## Scope / method

- Scratch root: `.scratch/r48w2-R48MutUnlanded/` (work.py, pristine.py, probe-rename/, probe-cap/); all tool runs used `TMPDIR` pointed at that scratch root. Probes ran `git init` in scratch-only repos.
- No tools installed (none needed); no credential material.
- Seat bounds respected: leaf, no subagents; detector is `--selftest` only — claims C1/C2 counters were not exercised (out of seat scope).
- This is a coverage finding against the selftest's kill-power, not a defect report against the tool: pristine behavior on both probes is the documented contract.

Report: .ufo/waves/round-48/w2/R48MutUnlanded.md
