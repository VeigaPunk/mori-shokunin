# MutRoutedTiming — wave 2 mutation probe (C1, R4 timing comparison)

Seat: `MoriR24.MutRoutedTiming` (leaf; no subagents, no lane mutation).
Date: 2026-10-22. Wave: round-24 wave-2 falsify.
Probe: mutate the R4 timing comparison in `tools/mori-routed-check.py` (inverted, then
removed); ask whether `--round 23` at `c725aa37` still goes red and whether the round-24
tip stays held; report whether the mutant is killed by an existing control.

## Rules followed

- Scratch clone only: `/fast/scratch/hyaku/mori-r24-a2/w2/MutRoutedTiming/repo`, created
  with `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin <dir>`, checked
  out detached at `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc` (measured lane tip for this
  wave). Committed tamper commits were created in this clone only; nothing was pushed.
- Fleet repo/lane state untouched: no git add/commit/stash/checkout/reset/pull/push or jj
  mutation in `/home/vgpnk/Projects/shokunin/mori-shokunin`; only the report file below is
  created there. `git status --porcelain` in the clone is empty at the end (restored).
- No host writes, no PSI/cgroup/proc writes, no service restarts.
- Tooling installs: none (Python 3.14.8 at `/usr/bin/python3` already present; no package
  installed, so pacman guard is not exercised).

## Claims under test (contract)

- C1 declared before: `--rev c725aa37 --round 23` → `held: 3` (R4 red), exit 1
  (contract.md:42-43, 150-152, A4).
- C1 declared after: `--rev <landed tip> --round 24` → `held: 4`, exit 0
  (contract.md:44-45).
- R4 able-to-fail demon (A1, contract.md:47-48): a ledger row whose `at` precedes its
  dispatch commit turns R4 red. R4 predicate (A4, contract.md:143-149): every
  `.ufo/waves/round-N/*-attempts.json` and `*-ledger.json` verifies clean with
  `tools/mori-dispatch-ledger.py verify` at REV, and for every row the committer time of the
  commit that last changed its `dispatch_path` is at or before the row's `at`; every wave
  spec has a ledger whose last row is `started`/`partial`.

## Tool identity and hashes

Pristine `tools/mori-routed-check.py` at a730ecfe (and restored copy):
`64921a0c30aed1d9a2a7a03c377825add37ebecd7aded8fbfe8f30c02dafbd14`.
- Mutant A (inverted comparison), line 612: `elif changed_epoch > int(at.timestamp()):` →
  `elif changed_epoch <= int(at.timestamp()):`. Hash: `b6e13756ba33995b6d50354d1b731601dbc84cb77f4b7fde39cc744a3edf9002`.
- Mutant B (comparison removed): the entire `elif ... dispatch_committed_after_dispatch`
  branch (lines 612-614) deleted; `else: bound_before_call` becomes unconditional. Hash:
  `0adebf9cfe7a817111d1e2a99589602eecb1c6fffe8c7b25d9881097a884e9a1`.

All runs: `python3 -I tools/mori-routed-check.py --repo <clone> --rev <rev> --round N`
from inside the clone (working-tree tool bytes; repo reads are git-object-only).
Raw outputs: `/fast/scratch/hyaku/mori-r24-a2/w2/MutRoutedTiming/out/`.

## Baseline (pristine) runs

| # | Command | Observed | Expected |
|---|---|---|---|
| B1 | `--rev c725aa37 --round 23` | exit 1, `held: 3`, status failed | red (declared before) |
| B2 | `--rev a730ecfe --round 24` | exit 0, `held: 4`, status held | green (declared after) |
| B3 | `--rev c725aa37 --round 24` | exit 1, `held: 3`, R4 `no_round_ledger` | red (contract.md:152) |
| B4 | `--rev a730ecfe --round 23` | exit 1, `held: 3` | red (same defect as B1) |

At B1/B4 R4 is red for two independent reasons (out/baseline-c725aa37-r23.json rows[3],
out/baseline-a730ecfe-r23.json rows[3]):
1. `wave1-attempts.json` fails `verify` (`attempt_ledger_not_clean` + findings
   `AT_INVALID`, `LEGACY_ROW_UNBOUND`, `STARTED_MISSING`; 8 rows `no_dispatch_path`).
2. `wave1-ledger.json` rows 1-8: `dispatch_committed_after_dispatch` — `at` 17:03Z–17:24Z
   (`at_epoch` 1792602191–1792603454) with `dispatch_last_changed_epoch` 1792606259 (commit
   `22772c1`, 18:10:59Z), exactly the contract's described defect. `wave2-ledger.json` is
   clean and `bound_before_call`.

At B2 R4 is green: the single `wave1-attempts.json` row is `bound_before_call`
(`dispatch_last_changed_epoch` 1792656837 ≤ `at_epoch` 1792656853), verify clean, spec
started.

## Tamper commit (synthetic R4 able-to-fail demon)

In the clone, commit `2033142233d08646f7b277df401873053dfc4572` (parent a730ecfe,
committer 2026-10-22T07:00:00+00:00, epoch 1792652400) adds:
- `.ufo/waves/round-24/tamper-dispatch.json` — small dispatch payload (3 tasks);
- `.ufo/waves/round-24/tamper-attempts.json` — one clean row: `at`
  2026-10-22T00:00:00+00:00 (epoch 1792627200, i.e. 7 h before the dispatch commit),
  `dispatch_path` = the tamper dispatch, `result: started`, `started_ids: 3`, bound
  payload fields matching `tamper-dispatch.json`.

`tools/mori-dispatch-ledger.py verify --repo <clone> --rev 20331422 --ledger
.ufo/waves/round-24/tamper-attempts.json` → exit 0, `status: clean` (`LEDGER_CLEAN`,
rows: 1, bound: 1). The tamper is therefore a *clean* ledger whose only defect is the
timing order — the contract's R4 demon in isolation.

Pristine tool on the tamper: exit 1, `held: 3`, R4 reasons exactly
`["dispatch_committed_after_dispatch"]` (out/tamper-orig-r24.json).

## Mutant A — comparison inverted (`>` → `<=`)

| Command | Original | Mutant A | Detection |
|---|---|---|---|
| `--rev c725aa37 --round 23` | exit 1, held 3 | exit 1, held 3 (R4 reasons unchanged: attempts-ledger findings only; the 8 timing reasons disappear) | not observable |
| `--rev a730ecfe --round 24` | exit 0, held 4 | exit 1, held 3; row 1 now `dispatch_committed_after_dispatch` (`at_epoch` 1792656853, `dispatch_last_changed_epoch` 1792656837) | **KILLED** |
| `--rev a730ecfe --round 23` | exit 1, held 3 | exit 1, held 3 | not observable |
| `--rev 20331422 --round 24` (tamper) | exit 1, held 3 | exit 1, held 3 (wave1 row now flagged; tamper row now passes inverted predicate) | not observable |

Verdict: **killed by an existing control** — the declared after-value run (`--rev
a730ecfe --round 24` → held 4, exit 0) goes red under the inversion. A future regression
that flips the comparison direction would be caught by the claim's own after-value.

## Mutant B — comparison removed

| Command | Original | Mutant B | Detection |
|---|---|---|---|
| `--rev c725aa37 --round 23` | exit 1, held 3 | exit 1, held 3 (R4 reasons now only the attempts-ledger findings; the 8 `dispatch_committed_after_dispatch` reasons are gone but do not change held) | not observable |
| `--rev a730ecfe --round 24` | exit 0, held 4 | exit 0, held 4 | not observable |
| `--rev a730ecfe --round 23` | exit 1, held 3 | exit 1, held 3 | not observable |
| `--rev 20331422 --round 24` (tamper) | exit 1, held 3 | exit 0, held 4 (R4 reasons `[]`) | only the synthetic tamper catches it |

Verdict: **survives every existing committed-state control.** All four declared/real runs
are behaviorally identical between original and mutant. The only input that distinguishes
it is the tamper commit I created (a clean ledger with `at` before its dispatch commit),
which the original flags and the mutant misses.

## Coverage finding

The R4 timing predicate is not exercised in isolation by any already-committed state:
- The declared before-value (`c725aa37 --round 23`) is red even with the timing check
  removed, because the legacy `wave1-attempts.json` fails `verify` (AT_INVALID /
  LEGACY_ROW_UNBOUND / STARTED_MISSING). The real round-23 timing violation
  (`wave1-ledger.json` rows vs commit `22772c1`) is masked by that unrelated failure — the
  before-value control alone cannot detect a regression that silently deletes the timing
  comparison, and its "red" reason mix changes without changing `held`.
- The declared after-value (`a730ecfe --round 24`) contains no timing violation, so a
  removed comparison is invisible there (it only catches the *direction* flip, mutant A).
- Therefore the only committed predicate that can prove R4 timing still runs is the
  contract's able-to-fail demon shape (A1, contract.md:47-48): a clean ledger whose row
  `at` precedes its dispatch commit. None exists in committed history; the real round-23
  instances coexist with a non-clean attempts ledger. Per campaign rule, a surviving mutant
  is a coverage finding, not permission to change the contract.

## Restoration evidence

- Before any mutation: pristine hash `64921a0c…` (out/hashes-pristine.txt).
- After mutant A: mutated hash `b6e13756…` (out/hashes-mutant-invert.txt); restored via
  `cp pristine-mori-routed-check.py repo/tools/mori-routed-check.py`; `sha256sum` matches
  `64921a0c…`; `cmp -s` reports identical.
- After mutant B: mutated hash `0adebf9c…` (out/hashes-mutant-remove.txt); restored again;
  hash matches `64921a0c…`, `cmp -s` identical; clone `git status --porcelain` empty;
  clone HEAD = tamper `20331422` on top of a730ecfe.

## Files

- Scratch outputs: `/fast/scratch/hyaku/mori-r24-a2/w2/MutRoutedTiming/out/`
  (baseline-*.json, tamper-orig-r24.json, mutant-invert-*.json, mutant-remove-*.json,
  hashes-*.txt).
- Pristine copy: `/fast/scratch/hyaku/mori-r24-a2/w2/MutRoutedTiming/pristine-mori-routed-check.py`.
- This report: `.ufo/waves/round-24/w2/MutRoutedTiming.md` (only file created in the lane repo).
