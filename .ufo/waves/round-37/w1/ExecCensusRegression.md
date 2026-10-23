# ExecCensusRegression — r37 w1

Item attacked: **the main census regression battery** — that the census's own hermetic proof
(`mori-census.sh --selftest`) and the lane's frozen behavioral oracle (`mori-silence-cases.sh`,
the "oracle 28/28" of r36) are *fully green at the scored-tip bytes*, and that green is not
vacuous (each side detects a deliberate mutation).

Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only for this seat). Scratch:
`/fast/scratch/hyaku/mori-r37/ExecCensusRegression/`. No lane file was edited; no new lanes,
configs, installs (nothing installed this wave).

## 1. Byte pin — the battery ran the scored tip, not a drifting worktree

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && sha256sum tools/mori-census.sh tools/mori-silence-cases.sh
87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28  tools/mori-census.sh
34cd5770889ec6e7521b477aa9976cece7a64e07b83774c12ce2aea73161abfa  tools/mori-silence-cases.sh

$ for r in e57c58b57c025364e79d130fbdf764d2674d83d6 842a32074b5c7972e9728f3f629d83eb92f127c2; do
    echo "== $r"; git show $r:tools/mori-census.sh | sha256sum; git show $r:tools/mori-silence-cases.sh | sha256sum; done
== e57c58b57c025364e79d130fbdf764d2674d83d6
87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28  -
34cd5770889ec6e7521b477aa9976cece7a64e07b83774c12ce2aea73161abfa  -
== 842a32074b5c7972e9728f3f629d83eb92f127c2
87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28  -
34cd5770889ec6e7521b477aa9976cece7a64e07b83774c12ce2aea73161abfa  -
```

Worktree bytes == scored tip `e57c58b` == entering tip `842a320` for **both** artifacts, so the
tallies below describe the graded revision exactly. (`git rev-parse HEAD` moved under me during
the wave: `c31076ed` → `0a05f7e6` — other seats are landing; neither pinned hash changed, and
`git status --porcelain tools/` stayed empty.)

## 2. Selftest tally

```
$ TMPDIR=/fast/scratch/hyaku/mori-r37/ExecCensusRegression/tmp bash tools/mori-census.sh --selftest
EXIT=0
PASS cli: unknown arg exit 2 (exit 2)
PASS cli: --help exit 0 (exit 0)
PASS cli: --pin without a path exits 2 (exit 2)
PASS cli: --drift without a path exits 2 (exit 2)
MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)
Wall time: 18.31 seconds
```

Second run, distinct TMPDIR, same tally:

```
$ TMPDIR=…/tmp2 bash tools/mori-census.sh --selftest
EXIT=0
MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)
Wall time: 20.07 seconds
```

Receipts are **byte-identical** across the two runs:

```
$ sha256sum selftest.log selftest-2.log
a67a336bf02cb9d88453917a7ed53d1aec673a76e8c85f7016051d449554777f  selftest.log
a67a336bf02cb9d88453917a7ed53d1aec673a76e8c85f7016051d449554777f  selftest-2.log
```

Line accounting: `grep -cE '^PASS '` → `134`, `grep -cE '^FAIL '` → `0`, and the 134 PASS lines
are 134 distinct case descriptions (13 carry no `(exit …)` suffix — the canary/negative cases
`roster: config was not sourced (canary absent)`, `jj: sibling-lane author was not flagged`,
`git env: trace canary absent — GIT_TRACE* scrubbed`, …; none repeats). No `SKIP`/`WARN` lines
(`grep -ciE '^(SKIP|WARN|TODO)'` → `0`). Sorted case-label sets of run 1 and run 2: `IDENTICAL`.

## 3. Oracle tally

The census usage block documents **no** oracle mode; the lane's oracle is the frozen behavioral
matcher, which takes the census path as an argument (`tools/mori-silence-cases.sh [path-to-census]`,
`34cd5770…`). Two runs, different shuffle seeds:

```
$ bash tools/mori-silence-cases.sh
EXIT=0
SHUFFLE_SEED=3834436211
RUN_NONCE=2682988930
MORI_SILENCE_CASES: matched=28 total=28          (5.14 s)

$ TMPDIR=…/tmp3 bash tools/mori-silence-cases.sh
EXIT=0
SHUFFLE_SEED=724844120
MORI_SILENCE_CASES: matched=28 total=28          (5.71 s)
```

Case set: 28 distinct case ids, and the sorted id sets of the two runs are `ORACLE_SETS_IDENTICAL`
(the differing `CASE_ORDER=` lines are the intended shuffle; zero `FAIL` lines in either log).
This matches the r36 baseline verbatim — `.ufo/waves/round-36/w2/ExecCensusRegression.md:14-15`
(`PASS (134 cases, 134 passed, 0 failed)`, `matched=28 total=28`), so no case was silently lost
or added between rounds.

Acting on "the oracle mode if the usage documents it": it does not, and the CLI says so —

```
$ bash tools/mori-census.sh --oracle
mori-census: unknown argument: --oracle
usage: mori-census.sh [--selftest] [--pin <path>] [--drift <path>] [--help]
   (17-line usage on stderr; process rc observed as exit 2 by the caller)
```

so `--oracle` is *not* the oracle, and the frozen matcher above is what carries the 28/28 claim.

## 4. Non-vacuity controls (scratch copies only, lane files untouched)

Control A — oracle vs a census whose silence row-D state was changed
(`GL_STATE=silent` → `progressing`, copy at
`/fast/scratch/hyaku/mori-r37/ExecCensusRegression/mut/census-mut-silent.sh`, line 2503):

```
$ bash tools/mori-silence-cases.sh …/mut/census-mut-silent.sh
FAIL legacy-steer-open-silent: state want [silent] got [progressing] via lane finding want=1 got=0 rc want=1 got=0
FAIL silent-open: state want [silent] got [progressing] via lane finding want=1 got=0 rc want=1 got=0
FAIL old-report-before-relaunch-silent: state want [silent] got [progressing] …
FAIL report-future-no-close: state want [progressing-weak|silent] got [progressing] …
MORI_SILENCE_CASES: matched=21 total=28
mori-silence-cases: failed: main-repo-noise-silent report-eq-launch-no-close same-round-relaunch-silent
 legacy-steer-open-silent silent-open old-report-before-relaunch-silent report-future-no-close
EXIT=1
```

Control B — selftest vs a census whose usage-error exit was changed (`exit 2` → `exit 3`,
`mut/census-mut-cli.sh`, line 416):

```
$ bash …/mut/census-mut-cli.sh --selftest
FAIL cli: unknown arg exit 2: exit 3 want 2
FAIL cli: --pin without a path exits 2: exit 3 want 2
FAIL cli: --drift without a path exits 2: exit 3 want 2
MORI_CENSUS_SELFTEST: FAIL (134 cases, 131 passed, 3 failed)
EXIT=1
```

Both mutants were detected, with exactly the assertions the mutation targets; the green in §2/§3
is load-bearing, not a matcher that cannot fail.

## 5. Supplementary observations (detection only, outside acceptance)

- **Live mode runs and terminates**: `bash tools/mori-census.sh` → `EXIT=1`,
  `MORI_CENSUS: DRIFT (findings=32 drift=12 unavailable=1 surfaces=8)`, wall `141.47 s` on this
  saturated host (100 background-job cap reached, ~700 live peers). The DRIFT roll is *host
  state* (`findings=`/`unavailable=` surfaces), not a battery failure, and this seat remediates
  nothing. A 45 s-bounded rerun (`timeout 45`) was still running at the cutoff (`rc=124`), so
  live-mode wall time is load-sensitive; the hermetic battery is not (cf. the identical selftest
  receipts in §2).
- **Setup-error path**: `TMPDIR=/nonexistent-census-probe bash tools/mori-census.sh --selftest`
  emits only `mktemp: failed to create directory via template
  '/nonexistent-census-probe/mori-census-selftest.XXXXXX': No such file or directory` and no
  tally. The census process rc for this path was **not captured** (the harness dropped that
  shell's output); do not read an exit code into this line — the usage contract claims 2, unverified
  here. [INFERENCE] the selftest cannot proceed without a usable TMPDIR; it does not fall back
  into the lane or the repo.
- No residue: after every run `${TMPDIR}/mori-census-selftest.*` was gone (fixtures removed), and
  the only untracked entries in the lane were other seats' reports/scratch, never census output.

## 6. Risks / limits of this item

- The battery proves *census-internal* behavior and the 28 silence cases; it does **not** touch
  the round's C1 (calibration/counter) or C2 (source-drift) claims, which have their own seats.
- The tallies are identical to r36, so this battery covers no *new* round-37 behavior; the routed
  debts (d–h in the contract) live in `mori-round17-jj-regressions.py` and the drift tool, not here.
- Oracle fidelity depends on the real `git`/`tmux` stubs of this host; both runs agreeing across
  different shuffle seeds and nonces is the strongest evidence available read-only.

## VERDICT: PASS

- `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)` exit 0, twice, byte-identical receipts.
- `MORI_SILENCE_CASES: matched=28 total=28` exit 0, twice, two shuffle seeds, identical case sets.
- Both scripts hash-pinned to scored tip `e57c58b` and entering tip `842a320`;
  two independent mutants each produce the expected red (21/28 and 131/134). No defect found.
