# CensusNoHarmBaseline — before-baseline for the census surface (claim C2)

Seat: `MoriR24.CensusNoHarmBaseline` (read-only leaf, no subagent dispatch).
Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Surface: `tools/mori-census.sh` (the production census gate).
Purpose: establish the **before** state of the census so that claim C2
(`tools/mori-pressure.py`, a new separate tool) can be shown to leave the
census untouched. Nothing in the lane repo was modified by this seat except
this report file.

## 1. Setup (sandbox clone, outside the fleet tree)

```
mkdir -p /fast/scratch/hyaku/mori-r24-a2
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin \
    /fast/scratch/hyaku/mori-r24-a2/census-baseline
cd /fast/scratch/hyaku/mori-r24-a2/census-baseline
git checkout --detach 29c1bf45dde6af48fc9a07aef447bd7d7f822cc5
```

- clone HEAD: `29c1bf45dde6af48fc9a07aef447bd7d7f822cc5`
  (`round-24: declare claims and contract before implementation`).
- clone remote: `origin /home/vgpnk/Projects/shokunin/mori-shokunin` (fetch/push
  address unchanged; **no push, no fetch, no clone-side commit** — `git status
  --porcelain` in the clone is empty after both runs).
- scratch TMPDIR: `/fast/scratch/hyaku/mori-r24-a2/census-baseline-tmp` (created
  before both runs; it was **empty** afterwards — the selftest removed its own
  fixture tree).
- The C2 tool does not exist at this revision:
  `git cat-file -e 29c1bf45...:tools/mori-pressure.py` → `fatal: path
  'tools/mori-pressure.py' does not exist` (exit **128**). So every number below
  was produced by the census alone, before C2 exists.

## 2. Census bytes (the pinned no-harm digest)

`tools/mori-census.sh`, sha256:

| source | sha256 |
|---|---|
| clone worktree @ 29c1bf4 | `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28` |
| `git cat-file -p 29c1bf4:tools/mori-census.sh` | `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28` |
| `git cat-file -p 4059ffb:tools/mori-census.sh` (wave-1 ledger/spec commits) | `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28` |
| `git cat-file -p 11d8f71:tools/mori-census.sh` (lane tip observed at report time) | `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28` |
| lane repo worktree `tools/mori-census.sh` | `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28` |

The census is byte-identical across the before-commit, the wave-1 commits and
the current lane tip. The census also stamps this digest into its own
findings (`script_sha256=87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28`),
so the live run below is self-identifying.

## 3. Run A — selftest

```
cd /fast/scratch/hyaku/mori-r24-a2/census-baseline
TMPDIR=/fast/scratch/hyaku/mori-r24-a2/census-baseline-tmp \
    bash tools/mori-census.sh --selftest
```

- **exit code: 0**
- **summary line:** `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)`
- stdout: 135 lines (134 `PASS …` lines + the summary), sha256
  `a67a336bf02cb9d88453917a7ed53d1aec673a76e8c85f7016051d449554777f`
  (kept at `/fast/scratch/hyaku/mori-r24-a2/selftest.out`).
- stderr: 0 bytes. Wall time ≈ 14 s.
- The last case lines were, verbatim from the output file:
  `PASS drift: --pin writes a baseline (exit 0)` … `PASS cli: --pin without a path
  exits 2 (exit 0)` / `PASS cli: --help exit 0 (exit 0)`.

## 4. Run B — one live census run, as SKILL.md documents it

The documented invocation (`SKILL.md:164`, gate registry row *census*):
`bash tools/mori-census.sh` (`MORI_SHOKUNIN_ROOT=<fleet root>` outside the fleet
tree). Executed from the sandbox clone, which is outside the fleet tree, with
the fleet root given explicitly:

```
cd /fast/scratch/hyaku/mori-r24-a2/census-baseline
TMPDIR=/fast/scratch/hyaku/mori-r24-a2/census-baseline-tmp \
MORI_SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin \
    bash tools/mori-census.sh
```

- **exit code: 1** (DRIFT — the verdict map is 0 CLEAN / 1 DRIFT / 2 setup).
- **summary line:** `MORI_CENSUS: DRIFT (findings=30 drift=12 unavailable=1 surfaces=8)`
- header line: `mori-census census-r6 — ts=2026-10-22T08:16:37Z — mode=live — read-only`
- stderr: 0 bytes. Wall time ≈ 109 s.
- stdout: 63 lines, sha256 `9e8e331913112cf9acb7e3bef3dc6cb5b27a51eefb57f6a81e7cbfdb2ea8fbb4`
  (`/fast/scratch/hyaku/mori-r24-a2/live.out`). A timestamp-masked copy
  (`ts=<iso>` → `ts=<T>`, nothing else) is at
  `/fast/scratch/hyaku/mori-r24-a2/live.normalized.txt`, sha256
  `7a602716e0cc47f8f2a5237a48bccc4f15bf8779df83c3290f33130f0f6cb4a6`.

Surface states observed: `watchdog drift`, `waves drift`, `journal.user ok`,
`journal.system ok`, `cgroup ok`, `disk ok`, `silence drift`, `tmux unavailable`,
plus 23 per-lane rows.

Finding composition of the 30 findings (ids only, no record text):

| id | count | severity |
|---|---|---|
| `WATCHDOG_STATE_LAG` | 15 | info |
| `WAVE_UNSETTLED_AGE` | 10 | warn |
| `WATCHDOG_ABSENT` | 1 | warn |
| `LANE_SILENT` | 1 | warn (lane=kake) |
| `COREDUMP_NOTICE_JOURNAL_USER` | 1 | info |
| `JOURNAL_CLASSES_UNMEASURED` | 1 | info |
| `ROSTER_SET_MISMATCH` | 1 | info |

The 12 drift findings are host state that already exists at the before-commit
(no watchdog process matched, ten aged unsettled waves, one silent lane). They
are **not** a C2 effect and are not a regression: this run happened with
`tools/mori-pressure.py` absent (exit-128 proof above). The census's own
`script_sha256` on every finding equals the pinned digest, so the run is
attributable to exactly the bytes listed in §2.

## 5. No-harm reading

The before-baseline for C2 is therefore three pinned facts:

1. census bytes sha256 `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28`;
2. `bash tools/mori-census.sh --selftest` → exit **0**, `MORI_CENSUS_SELFTEST: PASS
   (134 cases, 134 passed, 0 failed)`;
3. one live run → exit **1**, `MORI_CENSUS: DRIFT (findings=30 drift=12
   unavailable=1 surfaces=8)`, stderr empty.

An after-run at the C2 landed tip must reproduce (1) byte-for-byte and (2)
exit 0 with the same 134/134 tally, and its live run must still be a census
run with the same finding id set and the same `script_sha256` stamp. A changed
digest or a changed selftest tally is the harm signal this baseline is for.
C2 adds a **separate** tool (`tools/mori-pressure.py`); nothing in the census
calls it, and the census is never edited (`SKILL.md:516` — "Never edit
`tools/mori-census.sh`").

## 6. Side effects and cleanliness

- The census live mode writes nothing (`SKILL.md:211`); the selftest wrote only
  under the given TMPDIR and removed its fixture tree (TMPDIR is empty after).
- The lane repo was not mutated by this seat: `git status --porcelain` in the
  lane shows only untracked files that belong to other seats
  (`.ufo/waves/round-24/w1/*.md` reports, `.scratch/`, `tools/__pycache__/`).
  No `git add/commit/stash/checkout/reset/pull` and no mutating `jj` command was
  run in the lane.
- All scratch artifacts live under `/fast/scratch/hyaku/mori-r24-a2/`
  (`census-baseline/`, `census-baseline-tmp/`, `selftest.out`, `selftest.err`,
  `live.out`, `live.err`, `live.normalized.txt`).

## 7. Tooling

No installs and no upgrades were performed; no package transaction was needed
(the census needs only bash plus the host's `journalctl`, `df`, `pgrep`, `tmux`
and coreutils, all already present). The operator's pacman guard was not
touched.

## 8. Risks and blockers

- The live DRIFT verdict is host state, not a C2 effect; an after-run will not
  be expected to be CLEAN unless the watchdog, the aged waves and lane `kake`
  change. The comparison must be on the census bytes, the selftest tally and
  the finding id set — not on the CLEAN/DRIFT roll.
- The live run takes ≈ 109 s wall time on this host, so an after-run must allow
  a comparable budget (the run above was launched with a 600 s deadline and
  finished inside it).
- No blockers.
