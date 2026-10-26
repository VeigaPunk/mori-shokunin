# Mo51ExecKillTimings — C1 arm A: kill-timing sweep of `mori-pin-check.py --rev` (both tools)

Seat: executor, leaf (no subagent dispatched). Item: extend C1 arm A's named limit by killing the `--rev` run
at five moments and counting repo and scratch residue for the landed tool and the entering tool.
Contract read: `.ufo/waves/round-51/contract.md` (freeze `4677910e`, entering tip `aa3af1ec`, data `87e0c374`).
Counters, predicates, controls and kill rules untouched; nothing below proposes a change to them. No tool was
installed or upgraded (no pacman, no uv, no npx — the pacman pause was respected and was not needed).
Lane repo was only read (`git show`, `git archive`, `git ls-tree`, `git log`); no add/commit/stash/checkout/reset/
pull/push, no jj command, no write outside `/fast/scratch/hyaku/mori-r51/Mo51ExecKillTimings/` and this report.

## 1. Method

Rev under test: `87e0c374537557754bf71dd68036ded3ddc6699c` (data). One clone for the seat, built the way the frozen
counter builds arm A's C0 (`count-c1.py:73-82` `fresh_clone`): `git clone --no-local --no-checkout <lane> clone`
then `git -C clone checkout -q -B master 87e0c374…`, so the clone's `master` **is** R and R is checked out. Verified
`git -C clone rev-parse --show-toplevel` = the clone dir and `git status --porcelain --ignored --untracked-files=all`
= 0 lines before every trial.

Tools (bytes):

| tool | source | sha256 |
|---|---|---|
| v5 (landed) | `clone/tools/mori-pin-check.py` (R) | `35c69d9115b5e45f91a4b0311ce95c03b3b2b929250e2afb31b571a49687b3bf` |
| entering | `git show aa3af1ec…:tools/mori-pin-check.py` saved to `entering/mori-pin-check.py` | `697ab2cc6ca6702a5abcf361f48bee31570b4c58ddcc386f41c84c84b5c08e39` (1425 lines) |

Trial driver (scratch, `driver.py`): cleans the clone (`git clean -xdffq`), asserts 0 status lines, `mkdir` of the
run's designated scratch and TMPDIR, then
`Popen([python3, <tool>, "--rev", <rev>, "--repo", <clone>] (+ "--scratch <run>/scratch" for v5 only),
cwd=<scratch seat dir>, env{TMPDIR=<run>/tmp, PYTHONDONTWRITEBYTECODE=1}, start_new_session=True)`, kills with
`os.killpg(pgid, SIGKILL)` at the wall time, then counts
`git -C clone status --porcelain --ignored --untracked-files=all` lines, recursive path count + `st_blocks` size of
`<clone>/.scratch` and of the designated scratch dir, and records the first 4 residue lines.

Commands (representative, exactly as run):

- v5: `python3 driver.py --label v5-kill-2 --tool clone/tools/mori-pin-check.py --rev 87e0c374… --clone clone --scratch runs/v5-kill-2/scratch --tmp runs/v5-kill-2/tmp --kill 2 --extra "--scratch runs/v5-kill-2/scratch" …`
- entering: same with `--tool entering/mori-pin-check.py --rev aa3af1ec… --kill 2 --extra ""`.

Baselines (no kill) are part of the same series: each tool's run to completion, to know where the 60 s sample sits.

Host: `git 2.56.0`, `Python 3.14.8`, clone and scratch on `/fast` (NVMe). Disk guard before the heavy runs:
`/fast/scratch/hyaku` 25 % used, 604.2 GB free; after the series 603 GB free, no ENOSPC.

## 2. Measured table

`repo residue` = lines from `git status --porcelain --ignored --untracked-files=all` in the clone;
`clone/.scratch` = paths under `<clone>/.scratch` (239 paths / 29,540 KB are **tracked baseline**, present at R even
with a clean tree); `scratch residue` = paths / `st_blocks` size under the run's `--scratch` (v5) or designated
scratch dir (entering; the entering tool has no `--scratch`, so this column is its *designated* scratch, which it
never touches). All kills landed while the process was alive (`rc=-9`).

### v5 (landed, `35c69d91…`) — full run baseline: exit 0 at 82.3 s, `PIN_CHECK=met`, repo 0 / scratch 0

| kill (s) | killed at (s) | repo status lines | clone/.scratch paths | clone/.scratch KB | scratch residue paths | scratch residue KB |
|---|---|---|---|---|---|---|
| 0.5 | 0.513 | 0 | 239 (baseline) | 29,540 | 14,191 | 337,844 |
| 2 | 2.019 | 0 | 239 | 29,540 | 14,287 | 338,148 |
| 10 | 10.027 | 0 | 239 | 29,540 | 14,207 | 337,884 |
| 30 | 30.016 | 0 | 239 | 29,540 | 14,199 | 337,988 |
| 60 | 60.023 | 0 | 239 | 29,540 | 14,202 | 338,060 |

Shape of the residue at every timing: `<run>/scratch/pin-check-<rand>/tree` — a complete shared-clone checkout of R
(12,498 files; ~330 MB); `<run>/tmp` stayed empty (0 paths). First appearance of the export dir: 0.040 s after start
at the earliest, i.e. the export is fully materialised well inside the 0.5 s sample. Nothing was reaped between
trials: each kill leaves its own `pin-check-<rand>/` under the caller-chosen scratch dir.

### entering (`697ab2cc…`, `--rev aa3af1ec…`) — full run baseline: exit 0 at 81.4 s, `PIN_CHECK=met`, repo 0 / designated scratch 0

| kill (s) | killed at (s) | repo status lines | clone/.scratch paths | clone/.scratch KB | designated scratch paths |
|---|---|---|---|---|---|
| 0.5 | 0.541 | 1 | 241 | 31,588 | 0 |
| 2 | 2.088 | 12,228 | 14,096 | 670,800 | 0 |
| 10 | 10.067 | 12,483 | 14,373 | 365,136 | 0 |
| 30 | 30.090 | 12,473 | 14,358 | 365,096 | 0 |
| 60 | 60.171 | 12,473 | 14,358 | 365,096 | 0 |

Residue lines (all `!!`, ignored, because `.scratch/` is gitignored):

- 0.5 s: `!! .scratch/pin-check-qzuyx5v6/tree.tar` (one file, ~2 MB written of the 329,134,080-byte archive at
  `aa3af1ec`; 12,473 files in that tree).
- 2 s: `!! .scratch/pin-check-szycxiw3/tree.tar` + `tree/…` — extraction in flight (12,228 of 12,473 files),
  tar still present → 670,800 KB, i.e. 655 MB = tar (314 MiB) + tree, twice the tree's size, **inside the repo**.
- 10 s: 12,483 lines (`tree/…`, tar unlinked after extraction) — 10 extra lines are pins' temp files.
- 30 s and 60 s: 12,473 lines, 365,096 KB — the plain extracted tree; the do-nothing control's 12,547 (3 s after
  first write, `evidence/control-c1-do-nothing.txt`) sits in this post-extraction regime.

## 3. Reading

1. **For v5 the repo-side result is flat across the whole kill window.** 0 lines at 0.5 s, 2 s, 10 s, 30 s and 60 s;
   the whole export is in scratch from 0.04 s onward. Arm A's single moment (3 s after the first write) is not a
   lucky sample of a monotone curve — it sits on a plateau. This *strengthens* arm A on the repo side on this host.
2. **The residue is rehomed, not removed.** Every kill, at every timing, leaves ~14,190 paths / ~330 MB under
   `--scratch` (or `TMPDIR`, which is the default parent: `tools/mori-pin-check.py:912`). The `finally:
   shutil.rmtree(scratch)` at `:948` cannot run after SIGKILL and nothing else scans the parent, so repeated kills
   accumulate: 5 kills = ~1.65 GB. On a host whose TMPDIR is `/tmp` (the counter's arm A sets TMPDIR inside its own
   scratch, `count-c1.py:98-130`, but a lane closure run need not) that is a ~330 MB `/tmp` directory per kill —
   and the operator directive treats `/tmp` paths as non-evidence.
3. **Neither tool was ever caught mid-export by a kill.** v5's first scratch entry is 0.040 s and the tree is
   complete (14,191 paths) by 0.513 s; the entering tool's single 0.5 s file is already a partial tar, i.e. `git
   archive` had finished and only the tar write was in flight. So none of the five timings measures a kill *during*
   object transfer; on a slower object store (network clone, cold cache) that window would open.
4. **The entering tool's repo residue is a step function of kill time** (1 → 12,228 → 12,473 lines) and its peak
   footprint inside the measured repo is ~655 MB at the 2 s sample, because `export_rev` writes the whole tar into
   `<repo>/.scratch/pin-check-*/` and then extracts beside it (`aa3af1ec:tools/mori-pin-check.py:844-862`, tar write
   at `:854-856`, extraction at `:857-861`). v5's fixed ~330 MB in scratch is the same order of magnitude but on the
   caller-chosen filesystem and never twice the tree.
5. **`.scratch` is tracked at R** (225 files / 239 paths / 29,540 KB), so "0 lines" is measured against a repo that
   already carries a `.scratch`; all residue in both tools is `!!` (ignored) — the count is only non-zero because
   `status_lines` passes `--ignored` (`count-c1.py:84-86`). Without `--ignored` the entering tool would score 0 at
   every timing, which is worth knowing before anyone "simplifies" the arm.

## 4. Side measurement (same R, different caller ref state) — evidence that `--rev` is not ref-hermetic

While validating the baselines I hit a v5 run at R that reported `unmet`. Same clone, same R, same tool bytes; the
only difference was the clone's ref state. Exact lines (saved `stdout-v5-full.txt` / `stdout-v5-full-master.txt`):

```
# caller HEAD detached at R, master = b504cb1 (lane master at clone time)
pin line=1009 kind=tally prefix=C1_SELFTEST state=mismatch pinned='pass=44 fail=0' observed='pass=0 fail=1' rc=1 cmd='python3 .ufo/waves/round-49/count-c1.py --selftest' class=stale
PIN_CHECK=unmet tally_pins=35 digest_pins=8 mismatches=1 … env=0 stale=1            (exit 1, 83.5 s)
# caller checked out on master = R
PIN_CHECK=met tally_pins=35 digest_pins=8 mismatches=0 … env=0 stale=0              (exit 0, 82.3 s)
```

Isolation (each export built exactly as v5 does, `git clone -q --shared --no-checkout <clone> tree` +
`checkout --detach R`, then the instrument run inside the tree with TMPDIR in the tree's `.scratch`):

| caller state | export `show-ref` | instrument |
|---|---|---|
| HEAD detached at R, `master`=b504cb1 | `refs/remotes/origin/master` only — **no `refs/heads/master`**, `HEAD`=detached | `C1_SELFTEST pass=0 fail=1` rc 1 |
| HEAD detached at R, `master`=R | `refs/heads/master` + `origin/*`, `HEAD`=`ref: refs/heads/master` | `C1_SELFTEST pass=44 fail=0` rc 0 |
| HEAD on `master`=R | `refs/heads/master` + `origin/*` | `C1_SELFTEST pass=44 fail=0` rc 0 |

Mechanism: `export_rev` (`tools/mori-pin-check.py:870-886`) gives the measured tree a repository whose **refs are
copied from the caller**, and `.ufo/waves/round-49/count-c1.py:353-357` reads `master` from *the tree it runs in*
(`LANE` is derived from its own path) and bails with `C1_SELFTEST pass=0 fail=1` when `master` is unreadable. So the
verdict of `--rev R` depends on the caller's HEAD/master, not only on R. The frozen counter is self-consistent here
— `fresh_clone` does `checkout -B master R` (`count-c1.py:73-82`) — and the frozen class rule labels this `stale`;
I am not proposing a counter change.

## 5. Draft: the named-limit extension (for the lesson text; no counter change)

```text
Arm A kills at one moment (3 s after the first write) and proves nothing about a kill at another moment.
Measured on 2026-10-26 (MACHINE_ID host, git 2.56.0, shared-clone export on NVMe) at 0.5/2/10/30/60 s with a caller
clone whose master was R: the repo-side count is 0 at every timing and the export is fully materialised by 0.5 s
(first scratch entry 0.040 s), so the arm sits on a plateau rather than a lucky point — but the residue is rehomed,
not removed: every kill leaves ~14,190 paths / ~330 MB under --scratch (or TMPDIR by default), unreaped, because the
rmtree lives in a finally that SIGKILL skips. A closure host with TMPDIR=/tmp therefore collects ~330 MB per killed
run. The entering tool instead leaves a repo-side step function (1 ignored line / 2 MB partial tar at 0.5 s, 12,228
at 2 s, 12,473 at 10 s and after) with a ~655 MB peak at 2 s (tar + tree inside the measured repo). No timing sampled
a kill during object transfer, so a slow object store is still untested; and the count is only non-zero because
--ignored is passed and because .scratch is tracked at R (225 files / 29,540 KB).
```

## 6. Limits of this measurement

- One host, one kernel, local NVMe clone, `--shared` export: the 0.5 s sample is host-specific; on a network or cold
  clone the export would not be complete at 0.5 s and the residue would be a partial clone (shape untested here).
- The clone is on `/fast`, so both the v5 scratch residue and the entering tool's repo residue landed on `/fast`. In
  the lane the entering tool's residue lands on the lane's filesystem (`/home`); the byte figures are unchanged but
  the filesystem differs.
- The entering tool's "first residue" instant is not measurable with my marker (its destination `<clone>/.scratch`
  pre-exists at R with 239 tracked paths); only the state at 0.5 s is evidence.
- `killpg` kills the whole session; no orphan of mine survived (a `pgrep -af mori-pin-check` after the series listed
  only *other seats'* live processes, none from this seat's runs).
- Repo-side counts are sensitive to `.scratch` being tracked (see §3.5); a repo without it would show the export
  directory itself as one untracked line instead of one ignored line.
- Every number above is for the committed bytes at R (`tools/mori-pin-check.py` sha `35c69d91…`), measured from a
  clone checked out at R. While this seat ran, the lane **working tree** gained an in-progress v5.1
  (`tools/mori-pin-check.py`, `SKILL.md`, `SHONEN.md`, `corpus/knowledge/memavailable-estimate-r51.md`, mtimes
  19:56–19:57 on 2026-10-26, 145 insertions / 33 deletions over four files) that, among other things, sets the
  measured tree's `master` to the measured revision and moves the default scratch parent to `$TMPDIR`, else
  `/var/tmp`. Those edits are not mine and do not touch this measurement — R's bytes come from git, not the
  worktree — but a seat that runs the tool *from the worktree* would be measuring v5.1 rather than R. The wave's
  own counters are unaffected: they copy R's bytes out of git (`count-c1.py` clones the repo, `--rev` reads
  committed objects).

## 7. Retained evidence

Scratch directory `/fast/scratch/hyaku/mori-r51/Mo51ExecKillTimings/` held `results.jsonl` (13 records, one per
trial, every field quoted above), `driver.py`, `entering/mori-pin-check.py`, per-trial `stdout-*.txt` and the
`r49-selftest-master-R.out` / `r49-selftest-master-W.out` A/B outputs. Every number in §2 and §4 is copied above;
the directory is removed at the end of the seat as the operator directive requires, so this report is the record.

## Findings

- **MED** — `tools/mori-pin-check.py:870-886` (`export_rev`) hands the measured tree a repository whose refs come
  from the caller, so `--rev R` is not hermetic with respect to the caller's HEAD/`master`: same R, `PIN_CHECK=met`
  from a caller on `master`=R and `PIN_CHECK=unmet … stale=1` from a caller detached at R with `master` elsewhere;
  the deciding pin is `.ufo/waves/round-49/count-c1.py:353-357`, which reads `master` from the tree it runs in.
  C1's claim wording ("hermetic") covers the lane path and the export location, not the caller's refs. The frozen
  counter is self-consistent because `count-c1.py:73-82` sets `master`=R in its own clones.
- **MED** — arm A's residue is rehomed, not removed: every kill from 0.5 s to 60 s leaves ~14,190 paths / ~330 MB
  under `--scratch`/`TMPDIR` (`tools/mori-pin-check.py:912-948`; `finally` rmtree is skipped by SIGKILL, and nothing
  scans the parent), so repeated kills accumulate ~330 MB each and a host with `TMPDIR=/tmp` would fill `/tmp`.
  `count-c1.py:7-10` counts only the repo.
- **LOW** — arm A's single kill moment is inside a plateau rather than a hazard window: repo count 0 at all five
  timings and the export complete by 0.5 s (first scratch entry 0.040 s; `count-c1.py:7-10`). A kill during object
  transfer was never sampled, so a slow object store remains untested — this is the sentence the named limit needs.
- **LOW** — the entering tool's repo residue is a step function of kill time (1 line at 0.5 s, 12,228 at 2 s, 12,473
  at 10 s+) with a ~655 MB peak at 2 s (tar + extracted tree inside the measured repo):
  `aa3af1ec:tools/mori-pin-check.py:844-862`; and the entering tool has no `--scratch`, so a harness that passes a
  scratch dir sees 0 there while 14k paths land in the measured repo (`aa3af1ec:tools/mori-pin-check.py:884-887`).
- **LOW** — both tools' residue lines are all `!!` (ignored) and `.scratch` is tracked at R (225 files / 239 paths /
  29,540 KB), so arm A's count depends on `--ignored` (`count-c1.py:84-86`); dropping `--ignored` would score the
  entering tool 0 at every timing.
- **LOW** — full-run time at R is ~82 s on this host (v5 82.3 s, entering 81.4 s), so 60 s is the largest kill time
  that is still mid-run; any later sample would be a no-op kill (bound for the report, not a defect).

Blockers: none. No tool installs, no pacman, no writes to `~/.local/bin`, no lane or fleet-root mutation.
