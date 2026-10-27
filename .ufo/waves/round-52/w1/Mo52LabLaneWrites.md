Report: .ufo/waves/round-52/w1/Mo52LabLaneWrites.md

# Mo52LabLaneWrites — attack: is C1's `lane_writes` guard falsifiable?

Seat: `Mo52LabLaneWrites` (leaf; no subagents spawned). Lane: `mori-shokunin`. Wave: round 52 / `w1`.
Instrument measured: `.ufo/waves/round-52/count-c1.py`, sha256 `e864922790451b4026be784d5344d9a06827b251ed3c81bfe26b1c559ee3c300`
(identical to `evidence/freeze-sha256.txt:2`), run unmodified.
Subject: data commit `8524904adb25e44f24d9f25aac7eae909625c18c` in a `--no-local` clone under
`/fast/scratch/hyaku/mori-r52/Mo52LabLaneWrites/clone`; the frozen counters and predicates are untouched by this seat.

**Verdict (one line).** The hypothesis "C1's `lane_writes` guard catches a pinned command that writes into the measured
repo" is **falsified for (a)–(d) and narrowed for the rest**: `run()` executes every pinned command with
`cwd` = an archive extraction under `--scratch` (`count-c1.py:534-548`), so a *relative* write can never reach the
repo at all; the guard fires only on an absolute-path write to a **new, non-ignored** path **in `--repo`** (one of
seven fixtures: case e). Three write classes into the measured repo were measured invisible (g, h) and one into the
lane-from-a-clone (f).

## 1. Hypothesis under test

Stated by the wave: "C1's `lane_writes` guard catches a pinned command that writes into the measured repo."
Falsification design: one pinned fixture probe per write class, each writing exactly one target and then printing a
tally so the pin is enumerated and executed; results read off `lane_writes=` in the counter line.

## 2. Setup (literal commands)

```
S=/fast/scratch/hyaku/mori-r52/Mo52LabLaneWrites; export TMPDIR=$S/tmp
git clone --no-local --quiet /home/vgpnk/Projects/shokunin/mori-shokunin $S/clone
git -C $S/clone checkout -q --detach 8524904adb25e44f24d9f25aac7eae909625c18c
git -C $S/clone rev-parse --show-toplevel
  -> /fast/scratch/hyaku/mori-r52/Mo52LabLaneWrites/clone
git -C $S/clone rev-parse HEAD
  -> 8524904adb25e44f24d9f25aac7eae909625c18c
git -C $S/clone config user.name Mo52LabLaneWrites
git -C $S/clone config user.email fixtlab@example.invalid
```

Each case is one commit in the clone (fixture identity, toplevel asserted before the first commit) adding
`fixture/probe_<case>.py` plus one appended SHONEN bullet:

```
- [~] fixture probe <case>: `python3 fixture/probe_<case>.py --selftest` → `PROBE_SELFTEST pass=0 fail=0`
```

Probe body (identical for all cases except `TARGET`):

```python
#!/usr/bin/env python3
"""Round-52 lane_writes falsification fixture: writes <desc>."""
import os

TARGET = <target>


def main():
    d = os.path.dirname(TARGET)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(TARGET, "w", encoding="utf-8") as f:
        f.write("probe\n")
    print("PROBE_CWD " + os.getcwd())
    print("PROBE_SELFTEST pass=0 fail=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Counter invocation per case (~70-73 s each):

```
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/count-c1.py <clone-commit> \
  --repo $S/clone --fleet-repo /home/vgpnk/Projects/shokunin --scratch $S/c1-<clone-commit>
```

`--fleet-repo` is needed because the counter defaults the fleet repo to `dirname(--repo)`, which is scratch.
The 8.4 GiB-free `/fast/scratch` was checked first (`scripts/hyaku/disk-guard.sh status`: use% 24, 615.0G free).

## 3. Results

| case | written target | path form | `lane_writes` | did the write reach the measured repo? | caught |
|---|---|---|---|---|---|
| a | `probe-root-untracked.txt` | relative | 0 | no — archive tree | no |
| b | `__pycache__/probe_bytecode.pyc` (ignored) | relative | 0 | no — archive tree | no |
| c | `.git/probe-into-git.txt` | relative | 0 | no — archive tree (no `.git` there; the probe created one) | no |
| d | `.ufo/waves/round-38/scratch/probe.txt` | relative | 0 | no — archive tree | no |
| e | `<clone>/probe-absolute-untracked.txt` | absolute | **1** | **yes** | **yes** |
| f | `<other fixture repo>/probe-other-repo.txt` | absolute | 0 | yes, into a *different* repo | no |
| g | `<clone>/probe-pre-existing.txt` (already untracked before the run) | absolute | 0 | **yes** (content `preexisting` → `probe`) | no |
| h | `<clone>/.git/probe-into-git-abs.txt` | absolute | 0 | **yes** (6-byte file present after the run) | no |

Verbatim counter lines (rev shortened in the table only; full sha in the receipts column below):

```
a 261b2415cadc66cbffd041f5586bf57933693fb0  C1=unmet items=43 axes=6 pins=3 boxes=5 living=7 superseded=4 locators=27 mismatches=1 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400 rev=261b2415cadc66cbffd041f5586bf57933693fb0 failed=mismatch   exit=1
b d3a64156abb7c6c3f4e8e82a6401d38d661157fe  C1=unmet items=44 axes=6 pins=4 boxes=6 living=7 superseded=4 locators=27 mismatches=2 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400 rev=d3a64156abb7c6c3f4e8e82a6401d38d661157fe failed=mismatch   exit=1
c dfd5f3f4639b4b4a1096879a36cf071884d7a7c2  C1=unmet items=45 axes=6 pins=5 boxes=7 living=7 superseded=4 locators=27 mismatches=3 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400 rev=dfd5f3f4639b4b4a1096879a36cf071884d7a7c2 failed=mismatch   exit=1
d 1132c7a57025d4e7211ad95fa2c0d592168b2aff  C1=unmet items=46 axes=6 pins=6 boxes=8 living=7 superseded=4 locators=27 mismatches=4 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400 rev=1132c7a57025d4e7211ad95fa2c0d592168b2aff failed=mismatch   exit=1
e c3a928e16e01346c4872fd50c2b49ae3bc20371b  C1=unmet items=47 axes=6 pins=7 boxes=9 living=7 superseded=4 locators=27 mismatches=5 errors=1 hidden=0 lane_writes=1 manifest=6209bdb8e400 rev=c3a928e16e01346c4872fd50c2b49ae3bc20371b failed=errors,lane_writes,mismatch   exit=1
f 7afc3769264b85371a5c112d37524e96ffc30b24  C1=unmet items=48 axes=6 pins=8 boxes=10 living=7 superseded=4 locators=27 mismatches=6 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400 rev=7afc3769264b85371a5c112d37524e96ffc30b24 failed=mismatch   exit=1
g 292e6b40e6e4c035e413b810b28edb39624bf05f  C1=unmet items=49 axes=6 pins=9 boxes=11 living=7 superseded=4 locators=27 mismatches=7 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400 rev=292e6b40e6e4c035e413b810b28edb39624bf05f failed=mismatch   exit=1
h a35c3dbd06dbcd790c19df79730c2a9cded4a4b6  C1=unmet items=50 axes=6 pins=10 boxes=12 living=7 superseded=4 locators=27 mismatches=8 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400 rev=a35c3dbd06dbcd790c19df79730c2a9cded4a4b6 failed=mismatch   exit=1
```

Every fixture pin really executed (so the runs are not vacuous), e.g. from case g:

```
item pin python3_fixture/probe_g.py_--selftest expect=PROBE_SELFTEST_pass=0_fail=0 got=PROBE_SELFTEST_pass=0_fail=0_receipt_missing state=mismatch
```

The `mismatches=` growth and exit=1 are the fixture pins' `receipt_missing` (no round-52 receipt exists for a
fixture stem) plus the extra SHONEN boxes; they are constant fixture noise, not a reading of the guard. The only
value that changes with the write class is `lane_writes` (and, in case e, `errors`).

Case e's guard output, verbatim (it prints each new status line):

```
lane_write ?? probe-absolute-untracked.txt
```

Case g's proof that the write landed while the guard stayed silent — the pinned probe rewrote an
already-untracked file, and `git status` line is byte-identical before and after:

```
before: ?? probe-pre-existing.txt      content "preexisting"
after : ?? probe-pre-existing.txt      content "probe"
lane_writes=0
```

Case h's proof that a `.git/` write is invisible even by absolute path:

```
$ ls -l $S/clone/.git/probe-into-git-abs.txt
-rw-r--r-- 1 vgpnk vgpnk 6 Oct 26 21:21 .../clone/.git/probe-into-git-abs.txt
$ cat $S/clone/.git/probe-into-git-abs.txt
probe
$ git -C $S/clone status --porcelain --ignored --untracked-files=all
?? probe-absolute-untracked.txt
?? probe-pre-existing.txt
lane_writes=0
```

Case f's proof that the guard is scoped to `--repo`, not to the lane: the pinned command wrote into a second
throwaway fixture repo, and that repo shows the write while the measured clone reports nothing.

```
$ cat $S/run-7afc3769264b85371a5c112d37524e96ffc30b24.txt | grep '^C1='
C1=unmet ... lane_writes=0 manifest=6209bdb8e400 rev=7afc3769264b85371a5c112d37524e96ffc30b24 failed=mismatch
$ git -C <other fixture repo> status --porcelain --ignored --untracked-files=all
?? probe-other-repo.txt
```

## 4. Why: the mechanism in the frozen counter

- `def run(argv)` (`count-c1.py:534`) extracts `git archive rev` into `os.path.join(base, "tree")` once
  (`:535-544`) and runs the pinned command with `cwd=state["tree"]` and
  `env=dict(os.environ, TMPDIR=<base>/tmp, PYTHONDONTWRITEBYTECODE="1")` (`:545-548`).
  Therefore relative writes land in the scratch archive, and bytecode is off — (a), (b), (c) and (d) cannot reach
  the repo at all. `--scratch` is additionally refused if it lies inside `--repo` (`main`, the `commonpath` check).
- `def status()` (`:527`) reads `git -C repo status --porcelain --ignored --untracked-files=all`; `before = status()`
  is snapshotted once (`:531`) and `lane_writes()` (`:562`) returns `len((status() - before) - {""})`, printing each
  new line as `lane_write ...`. So the guard is a **set difference of status lines of `--repo`**, and nothing else:
  - a path that was already dirty contributes the same line before and after → invisible (case g);
  - a path git never lists (anything under `.git/`) never enters the set → invisible (case h);
  - a write into any other repo is not in the set at all (case f, and by construction: only `--repo` is read).
- Nonzero `writes` is folded into `errs` and `failed.append("lane_writes")` (`:429-438`), and the printed line
  carries `lane_writes=W`; so the *reporting* is correct — only the *coverage* is narrower than the docstring's
  "any nonzero value is an error (a pinned command wrote into the repo it measures)" (`:44`).
- The docstring of `run()` says the pinned commands run "at R (git archive of R under the scratch dir)"; the
  predicate's own lane_writes sentence says "the lane repo". With `--repo` = a clone these are different repos, and
  the frozen text reports on the clone under the name of the lane.

Manual reproduction of the cwd claim, independent of the counter (probes a–d run by hand in a fresh extraction):

```
$ git -C $S/clone archive 1132c7a5 | tar -x -C $S/manual-tree      # archive_files=12614 archive_has_git_dir=no
probe_a -> PROBE_CWD /fast/scratch/hyaku/mori-r52/Mo52LabLaneWrites/manual-tree PROBE_SELFTEST pass=0 fail=0
probe_b -> PROBE_CWD /fast/scratch/hyaku/mori-r52/Mo52LabLaneWrites/manual-tree PROBE_SELFTEST pass=0 fail=0
probe_c -> PROBE_CWD /fast/scratch/hyaku/mori-r52/Mo52LabLaneWrites/manual-tree PROBE_SELFTEST pass=0 fail=0
probe_d -> PROBE_CWD /fast/scratch/hyaku/mori-r52/Mo52LabLaneWrites/manual-tree PROBE_SELFTEST pass=0 fail=0
LANDED_IN_ARCHIVE probe-root-untracked.txt      absent_in_clone probe-root-untracked.txt
LANDED_IN_ARCHIVE __pycache__/probe_bytecode.pyc    absent_in_clone __pycache__/probe_bytecode.pyc
LANDED_IN_ARCHIVE .git/probe-into-git.txt       absent_in_clone .git/probe-into-git.txt
LANDED_IN_ARCHIVE .ufo/waves/round-38/scratch/probe.txt  absent_in_clone .ufo/waves/round-38/scratch/probe.txt
$ git -C $S/clone status --porcelain --ignored --untracked-files=all      # (empty)
```

## 5. A live instance of the escape (not a fixture)

The counter executes the living pin of `corpus/README.md` that runs `python3 .ufo/waves/round-39/conform.py <rev>
--selftest` (receipt line: `item living corpus/README.md:728 ... got=CONFORM_SELFTEST_pass=9_fail=0_rc=0 state=ok`).
That script hardcodes the lane:

```
.ufo/waves/round-39/conform.py:53   LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
.ufo/waves/round-39/conform.py:54   SCRATCH_ROOT = os.path.join(LANE, ".ufo", "waves", "round-39", "scratch")
.ufo/waves/round-39/conform.py:491  os.makedirs(SCRATCH_ROOT, exist_ok=True)
.ufo/waves/round-39/conform.py:492  work = tempfile.mkdtemp(prefix="mori-conform-selftest-", dir=SCRATCH_ROOT)
.ufo/waves/round-39/conform.py:501  with open(path, "w", encoding="utf-8") as handle:
.ufo/waves/round-39/conform.py:511-512  finally: shutil.rmtree(work, ignore_errors=True)
```

so every `count-c1.py` run writes nine mutation copies into the **real lane** regardless of cwd and regardless of
`--repo`. In my eight clone-scoped runs the real lane gained such directories and no run reported them:

```
$ ls -d /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/scratch/*/
... mori-conform-selftest-0kscwtiu  2buyokr3  5jy7nf1u  8zi6dg28  cz4gkmg0  h2x9yh9i   (6 dirs, mtime 21:23)
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain --ignored --untracked-files=all | grep -c 'round-39/scratch'
27
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain --ignored --untracked-files=all | wc -l
10423
```

Attribution is deliberately weak: mtimes (21:23) fall inside my case-h run window, but sibling seats run the same
counter concurrently and the script deletes its own `work` dir in a `finally`, so surviving dirs indicate runs that
were killed before cleanup — **not** established as mine. What is established by code reading plus case f is that the
write happens on every run and that a clone-scoped guard cannot see it. Files I may have caused inside the lane are
disclosed in §7 as required; I removed nothing there (removal would itself be a lane mutation).

Also note the same shape is self-erasing: because `conform.py` removes `work` in a `finally`, even a run with
`--repo` = the lane ends with the pre-run status set and reads `lane_writes=0` — a self-cleaning write is invisible
to a before/after set difference by construction.

`.ufo/waves/round-38/conform.py:37-38` carries the same hardcoded shape
(`LANE = ...`, `SCRATCH_ROOT = <LANE>/.ufo/waves/round-38/scratch`, writes at `:238-248`); its living pin at
`corpus/QUALITY.md:885` is superseded today, so the counter does not execute it (receipt:
`item living corpus/QUALITY.md:885 ... got=superseded state=ok`).

## 6. Does this falsify P-C1 as landed?

No, not by itself, and this seat does not re-score anything. The measured line at the data commit is
`C1=met ... lane_writes=0` with the counter's default `--repo` = the lane, so the claim's own receipt is honest about
what it measured. What the attack shows is that `lane_writes` is a **one-class detector**:
absolute-path, new-path, non-ignored, inside `--repo`, surviving to the end of the run. It cannot be "unmet" by
(a)–(d) at all, and it is silent for g, h and f. Every control the round built (`controls/c1-controls.py` commits in a
throwaway `--no-local` clone) and every wave seat re-running the counter on a clone measures a clone, so for those
runs the printed `lane_writes=0` says nothing about the lane.

## 7. Files this seat created or may have created inside the lane (required disclosure)

- None written by this seat by design: every command ran from `/fast/scratch/hyaku/mori-r52/Mo52LabLaneWrites`, and
  the only byte written under the lane tree is whatever the *pinned* commands write (see §5).
- Disclosed as possibly mine, not attributable: `.ufo/waves/round-39/scratch/mori-conform-selftest-*/` (6 dirs,
  mtime 2026-10-26 21:23, 27 untracked status lines), created by the pinned `round-39/conform.py --selftest` during
  my mandated counter runs and/or by sibling seats running the same counter. Not removed by me.
- Nothing in `~/.local/bin` or any PATH directory; nothing installed, so no tool record is owed. No pacman command
  was run (host-wide pause respected).

## 8. Named limits (frozen; routed to round 53, not proposed as a fix for this round)

1. **Scope.** `lane_writes` reads `--repo` only (case f). Under the wave's mandated clone-scoped re-execution the
   value certifies the clone, not the lane, while the docstring's sentence (`:44`) names "the lane repo".
2. **Reachability.** Pinned commands run with `cwd` = the scratch archive (`:548`), so relative writes cannot enter
   the repo (a)–(d); only absolute paths (or a tracked symlink inside the archive resolving to an absolute target)
   reach it. The contract's named limit "the counter runs the pinned commands unsandboxed in an archive of R" states
   the archive; it does not state that *relative* writes are therefore inert, which is why the guard reads 0 in (a)–(d).
3. **Net difference.** A write to a path already listed by `git status --porcelain --ignored` is invisible (case g).
   The lane carries 10423 status lines today, so this class has wide surface.
4. **`.git/`.** Confirmed invisible even by absolute path (case h); the contract already names this.
5. **Self-erasing writes.** A pinned instrument that creates and `rmtree`s its scratch (the shape of both round-38
   and round-39 `conform.py`) leaves the set unchanged and reads 0 even with `--repo` = the lane (§5).
6. **Selftest arm is a stub.** `C1_SELFTEST pass=42 fail=0` includes one `lane_writes` check, but it injects the
   value (`count-c1.py:752`: `run_eval(files(), writes=3)`; `run_eval` passes `lane_writes=lambda: writes`), so no
   selftest case exercises `status()`, the set difference, or the archive cwd. The detector's discovery path is
   untested by `--selftest`; my eight fixture runs are the first executed exercise of it.
7. **Pinned absolute-path writers exist in the corpus** (round-38/39 `conform.py` above; 399 tracked `*.py`/`*.sh`
   files contain the absolute lane path at R), so the escape in §5 is a class, not one file. Round 51's closure item 8
   (in-lane writers inventoried, fix routed with a successor-freeze design) is where this belongs.

Nothing here is offered as a counter change for this round: both counters, the predicates and the kill rules are
frozen, and the data this seat inspected was not shown wrong.

## 9. Retention

All receipts lived in `/fast/scratch/hyaku/mori-r52/Mo52LabLaneWrites/` (`run-<commit>.txt` ×8, `fixture-commits.txt`,
the two probe builders, `manual-tree/`, `clone/`, `other-rbnH/`) and were removed after the verbatim counter lines
and outputs above were copied into this report. The fixture commits
(`261b2415`, `d3a64156`, `dfd5f3f4`, `1132c7a5`, `c3a928e1`, `7afc3769`, `292e6b40`, `a35c3dbd`) live only in that
removed clone and are unreachable from the lane; they are reproducible from §2.

## Findings

1. **HIGH** — `lane_writes` measures `--repo`, not the lane: in a clone-scoped run (the pattern this wave mandates and
   every control uses) a pinned command can write into the real lane and the counter still prints `lane_writes=0`;
   measured in case f and observed live via the pinned `round-39/conform.py --selftest`. Concerns
   `.ufo/waves/round-52/count-c1.py:562` (with `:527-531`) and its docstring sentence at `:44`.
2. **MED** — arms (a)–(d) of the attack cannot reach the repo at all: `run()` executes pinned commands with
   `cwd` = the scratch archive, so relative writes always land there (`count-c1.py:534-548`); the guard's only
   reachable class is an absolute path. Fixture cases a, b, c, d all read `lane_writes=0`; manual repro shows the
   files inside the archive only.
3. **MED** — a write to an already-dirty path is invisible (set difference of status lines, `count-c1.py:562`);
   case g rewrote an untracked file's content (`preexisting` → `probe`) and read `lane_writes=0`, with 10423 status
   lines in the lane today.
4. **MED** — an absolute write under the measured repo's `.git/` is invisible (`git status` never lists it); case h
   left a 6-byte file in the clone's `.git/` and read `lane_writes=0`. Already a named limit in `contract.md`; now
   demonstrated with a receipt.
5. **MED** — the live escape: `python3 .ufo/waves/round-39/conform.py <rev> --selftest`, executed by the counter via
   the `corpus/README.md:728` pin, writes `mori-conform-selftest-*` copies into
   `<lane>/.ufo/waves/round-39/scratch/` through a hardcoded `LANE` (`conform.py:53-54`, `:491-501`); 6 such dirs and
   27 untracked status lines are present in the lane working tree after this wave's runs. Same shape at
   `.ufo/waves/round-38/conform.py:37-38` (pin superseded, so not executed).
6. **LOW** — the `--selftest` arm for `lane_writes` is a stub (`count-c1.py:752` injects `writes=3`), so
   `C1_SELFTEST pass=42 fail=0` does not demonstrate that the detector fires on a real write.
7. **LOW** — a self-cleaning pinned instrument (mkdtemp + `rmtree` in `finally`, both `conform.py` variants) is
   net-zero against a before/after status snapshot, so even `--repo` = lane reads 0 for that write class.
