# Mo50bExecPinCheckTip — round 50 (attempt 2), wave a2w1: pin-check at both revisions + unlanded-check

Seat: executor (leaf). Lane `mori-shokunin`, repo `/home/vgpnk/Projects/shokunin/mori-shokunin`, fleet root
`/home/vgpnk/Projects/shokunin`. Contract read first: `.ufo/waves/round-50/contract.md` (frozen at
`950e99be6757a52b00e9eb70ae1a1a7bbe2ea379`). Measured revisions: entering tip
`7197160b927f04db294c9553fb48fadcc7a3f4e3` and landed data
`487941b9395e89678af0053cc443cdb49cdee6e3`. Lane HEAD while running:
`4548a34dc8b4072abaa4335c1f54a9efcfcc314a`. Environment: `Python 3.14.8`, `git version 2.56.0`.

Scope: operability / no-harm measurement only — did round 50 add a pin mismatch, and what does the unlanded
check report on the live lane. No judgement of C1 or C2, no edit to any lane file, no counter, predicate,
control or kill-rule change proposed, no host state touched.

## Verdict (answers first)

**No mismatch at either revision. The round added none.** Both runs print `PIN_CHECK=met … mismatches=0 …`
with exit 0, and the two outputs differ only in the revision substituted into the two rev-bound argv lines
(911 `round-40/conform.py <rev>` and 912 `mori-sources-appendonly.py <rev>`). 43 pin lines at each revision,
all `state=match`; the finding buckets that would carry a mismatch
(`mismatch`, `unparsed`, `no_command`, `dropped`, `rebound`, `duplicate`, `hidden`, `misattributed`,
`env_unexpanded`) are all 0 at both revisions, so the classification requested by the assignment
(environmental vs stale) has an **empty set — nothing to classify**, and I show below that the classifier is
not vacuous.

`mori-unlanded-check.py` on the live lane is `UNLANDED=dirty round=50` at measurement time (exit 1): see
"Unlanded readings" — 2 paths at 09:38, 5 paths at 09:40, all round-50 wave bookkeeping and seat reports,
i.e. the wave is mid-flight, not a landed defect. Controls: the same check is `UNLANDED=clean round=50`
(exit 0) on a clean clone of lane HEAD, and `UNLANDED=clean round=49` (exit 0) on the live lane.

## Method (exact, reproducible)

Scratch `S = /fast/scratch/hyaku/mori-r50/Mo50bExecPinCheckTip`, `export TMPDIR=$S/tmp`. Nothing installed
(no pacman — host-wide pause respected —, no uv, no npx, no `~/.local/bin` addition): stock `python3` and `git`
sufficed, so there is no tool/version/channel line to record beyond those two.

Tool usage read first (`--help`/docstring): `tools/mori-pin-check.py:113-132` documents
`--rev REV [--repo DIR]` and states that with `--rev` it *writes only its own export under `<repo>/.scratch`
(removed on exit)*, and `tools/mori-pin-unlanded-check.py` docstring states `--repo DIR --round N` plus
`--selftest`, scope, and that `--repo` must be the repository's own top level.

To keep every byte the tools write inside scratch, `--repo` points at a **`git clone --shared` of the lane in
scratch** (one clone for this seat, no mirror). The instrument is the version landed at `487941b9`, extracted
with `git archive` as assigned (`tree-4879`), so the measured tool is the landed tool.

```bash
S=/fast/scratch/hyaku/mori-r50/Mo50bExecPinCheckTip
mkdir -p "$S/tmp" "$S/tree-4879"; export TMPDIR="$S/tmp"
git clone --shared -q /home/vgpnk/Projects/shokunin/mori-shokunin "$S/clone"          # rc=0
git -C "$S/clone" rev-parse --show-toplevel        # $S/clone  (fixture top level confirmed)
git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive 487941b9395e89678af0053cc443cdb49cdee6e3 \
  | tar -x -C "$S/tree-4879"                                                            # rc=0
cd "$S/tree-4879"
python3 tools/mori-pin-check.py --rev 487941b9395e89678af0053cc443cdb49cdee6e3 --repo "$S/clone"   # rc=0, 82s
python3 tools/mori-pin-check.py --rev 7197160b927f04db294c9553fb48fadcc7a3f4e3 --repo "$S/clone"   # rc=0, 81s
python3 tools/mori-unlanded-check.py --repo /home/vgpnk/Projects/shokunin/mori-shokunin --round 50   # rc=1
```

Disk guard checked before the heavy runs (`scripts/hyaku/disk-guard.sh status`): `/fast/scratch/hyaku 24%,
613.7G free`, `/tmp 2%` — no ENOSPC risk, no partial state. After the two pin runs the clone's `.scratch`
holds only the 225 **tracked** legacy `.scratch` files that came with the checkout (0 `pin-check-*`
residue), and the lane's own `.scratch` was never written by this seat (`mtime Oct 25 23:35`, unchanged
because no run used the lane as `--repo`).

Frozen-provenance check: the pinned text and the instrument are byte-identical at both revisions and at the
live worktree, which is *why* the two outputs must agree whatever the data commit changed:

```
blob SKILL.md@4879 = 5c639d2cfcbd39e75309573d13388ffea7b5c32c2dc35df736f1578f1311da4c
blob SKILL.md@7197 = 5c639d2cfcbd39e75309573d13388ffea7b5c32c2dc35df736f1578f1311da4c   (worktree: same)
blob mori-pin-check.py@4879 = 697ab2cc6ca6702a5abcf361f48bee31570b4c58ddcc386f41c84c84b5c08e39
blob mori-pin-check.py@7197 = 697ab2cc6ca6702a5abcf361f48bee31570b4c58ddcc386f41c84c84b5c08e39
blob mori-unlanded-check.py@4879 = 612d50c1590d5a30a1beae19a8e43da3acba18ddd30d47a6b51c2cdeada76109
blob mori-unlanded-check.py@7197 = 612d50c1590d5a30a1beae19a8e43da3acba18ddd30d47a6b51c2cdeada76109
git diff 7197160b… 487941b9… -- SKILL.md   → empty (no registry row added, edited or deleted this round)
```

## Observed pin-check output

Summary lines, verbatim (each run's own `.out` under `$S`, 7028 bytes at each revision):

```
PIN_CHECK=met tally_pins=33 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 \
  duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 \
  rev=487941b9395e89678af0053cc443cdb49cdee6e3 baseline=no                     # rc=0
PIN_CHECK=met tally_pins=33 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 \
  duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 \
  rev=7197160b927f04db294c9553fb48fadcc7a3f4e3 baseline=no                     # rc=0
```

Pin-line census (identical at both revisions): 43 lines = 33 `kind=tally` + 8 `kind=digest` + 2 `kind=lines`;
all 43 `state=match`. Child exit codes: 31 pins `rc=0`, 2 pins `rc=1` — the two intended mutants
(`.ufo/waves/round-45/fixtures/mutants/count-c1.py` pinned `pass=15 fail=1`, and
`…/mutants/count-c3.py` pinned `pass=17 fail=2`), i.e. the nonzero exits are the declared ones, not failures.

Full `diff` of the two pin-line sets (the only difference between the revisions):

```
35,36c35,36
< pin line=911 kind=tally prefix=CONFORM_SELFTEST state=match pinned='pass=11 fail=0' observed='pass=11 fail=0' rc=0 cmd='python3 .ufo/waves/round-40/conform.py 487941b9395e89678af0053cc443cdb49cdee6e3 --selftest'
< pin line=912 kind=tally prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=match pinned='pass=22 fail=0' observed='pass=22 fail=0' rc=0 cmd='python3 tools/mori-sources-appendonly.py 487941b9395e89678af0053cc443cdb49cdee6e3 --selftest'
---
> pin line=911 kind=tally prefix=CONFORM_SELFTEST state=match pinned='pass=11 fail=0' observed='pass=11 fail=0' rc=0 cmd='python3 .ufo/waves/round-40/conform.py 7197160b927f04db294c9553fb48fadcc7a3f4e3 --selftest'
> pin line=912 kind=tally prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=match pinned='pass=22 fail=0' observed='pass=22 fail=0' rc=0 cmd='python3 tools/mori-sources-appendonly.py 7197160b927f04db294c9553fb48fadcc7a3f4e3 --selftest'
```

Per-line evidence for the two round-50-relevant rows, both revisions (`state=match`, so neither is stale and
neither is unset-up):

```
pin line=938 kind=tally prefix=PIN_CHECK_SELFTEST state=match pinned='pass=114 fail=0' observed='pass=114 fail=0' rc=0 cmd='python3 tools/mori-pin-check.py --selftest'
pin line=973 kind=tally prefix=UNLANDED_SELFTEST state=match pinned='pass=17 fail=0' observed='pass=17 fail=0' rc=0 cmd='python3 tools/mori-unlanded-check.py --selftest'
```

## Classification of mismatches: empty set, classifier shown non-vacuous

Rule applied per the assignment: a mismatch is **environmental** when the pinned command cannot set itself up
(exit 2 / absent path / absolute host path / unresolvable revision) and **stale** when the command runs and
prints a tally different from the pinned text. There are zero `state=match`-excluded lines at either revision,
so no line falls in either class.

The classifier was exercised on both classes so the empty set is not an artifact of never looking:

- **Environmental, demonstrated live:** running the same instrument from the extracted archive *without*
  `--repo` (i.e. the literal "from a `git archive`" reading) cannot resolve a revision, because the extracted
  tree is not a git repository — this is exactly the environmental class the assignment names:

  ```
  $ cd "$S/tree-4879" && python3 tools/mori-pin-check.py --rev 487941b9395e89678af0053cc443cdb49cdee6e3
  PIN_CHECK_SETUP unresolvable revision 487941b9395e89678af0053cc443cdb49cdee6e3      # rc=2, stderr
  ```

  Hence every measured run above passes `--repo "$S/clone"`; the pin verdicts are unaffected (same instrument
  bytes, same object store through `--shared` alternates), and no write reaches the lane.
- **Environmental, second instance:** the unlanded check refuses a non-repository `--repo` —
  `python3 tools/mori-unlanded-check.py --repo "$S/tree-4879" --round 50` →
  `UNLANDED_SETUP fatal: not a git repository (or any parent up to mount point /) …`, `rc=2`.
- **Stale, not observed:** no bound argv produces a tally different from its pin. As a structural argument
  beyond the one run, none of the 43 bound argv paths is absolute or host-dependent — 0 hits for
  `cmd='(python3|bash|sh|python) (-[IB] )?/`; the unique path tokens are all lane-relative (`tools/…` ×15,
  `.ufo/waves/round-N/…` ×14, including the two `fixtures/mutants/` paths), so a pin can only go stale by a
  tool's answer changing, and none did at either revision.

## Unlanded readings (live lane, read-only)

`--repo` = the lane itself: the tool uses only `git rev-parse` and `git status --no-optional-locks`
(docstring), so this is read-only and touches neither the index nor the fleet repo.

```
09:38  UNLANDED=dirty round=50 paths=2   rc=1
       unlanded ?? .ufo/waves/round-50/a2w1.ready
       unlanded ?? .ufo/waves/round-50/a2w1/swarm-registry.json

09:40:49  UNLANDED=dirty round=50 paths=5   rc=1     (lane HEAD 4548a34d)
       unlanded ?? .ufo/waves/round-50/a2w1.ready
       unlanded ?? .ufo/waves/round-50/a2w1/Mo50bExecC1Controls.md
       unlanded ?? .ufo/waves/round-50/a2w1/Mo50bExecLiveRecheck.md
       unlanded ?? .ufo/waves/round-50/a2w1/Mo50bExecManifestAudit.md
       unlanded ?? .ufo/waves/round-50/a2w1/swarm-registry.json

09:42:17  UNLANDED=dirty round=50 paths=7   rc=1     (after this report was written; same instrument bytes,
       sha256 612d50c1590d5a30a1beae19a8e43da3acba18ddd30d47a6b51c2cdeada76109, run from the lane worktree
       because the scratch tree had already been removed)
       unlanded ?? .ufo/waves/round-50/a2w1.ready
       unlanded ?? .ufo/waves/round-50/a2w1/Mo50bExecC1Controls.md
       unlanded ?? .ufo/waves/round-50/a2w1/Mo50bExecC1Rerun.md
       unlanded ?? .ufo/waves/round-50/a2w1/Mo50bExecLiveRecheck.md
       unlanded ?? .ufo/waves/round-50/a2w1/Mo50bExecManifestAudit.md
       unlanded ?? .ufo/waves/round-50/a2w1/Mo50bExecPinCheckTip.md      ← this report
       unlanded ?? .ufo/waves/round-50/a2w1/swarm-registry.json
```

Controls (same instrument, same scratch TMPDIR):

```
UNLANDED=clean round=50     --repo "$S/clone"        rc=0   (clean checkout of lane HEAD 4548a34d)
UNLANDED=clean round=49     --repo <lane>            rc=0   (no corpus/, tools/ or top-level *.md path is
                                                            unlanded, so the round-50 dirt is exactly the
                                                            wave's own bookkeeping + seat reports)
```

Reading: the scope of the check includes `corpus/`, `tools/`, top-level `*.md` **in addition to**
`.ufo/waves/round-N/`, so the round-49-scope clean result also proves the data landing at `487941b9` left no
uncommitted `corpus/` or `.md` edit behind — the only unlanded bytes are files the wave itself is creating.
`a2w1.ready` and `a2w1/swarm-registry.json` are the same two artifacts the frozen wave w1 landed
(`w1.ready`, `w1/swarm-registry.json` are tracked at `487941b9`), so they are expected to be committed with
the wave; the seat reports are seats still writing. The 09:42:17 reading, taken after this report was written,
shows this report as the sixth unlanded file plus one more sibling (`Mo50bExecC1Rerun.md`) — the count tracks
the live wave, not a defect.

## Named limits

- `PIN_CHECK=met` certifies that each pinned text equals what its instrument prints at R; it does not certify
  that the arms are good, and this seat did not re-read the arms. `--min-tally-pins` was left at its default 1
  (the assignment did not ask for the floor), and `--baseline-rev` was not passed: the basis for "no pin was
  dropped or rebound" here is the stronger byte-identity of `SKILL.md` at both revisions, not a baseline run.
- The userland-host dimension (pinned commands touching the host, e.g. `mori-pressure.py`, `mori-oom-killers.py`,
  `mori-job-runway.py`) is exercised only through each tool's `--selftest`, which their docs describe as
  fixture-based; this seat did not audit whether any arm reads live host state.
- `--shared` clone: object identity is by alternates into the lane repo (read-only), not by copy; a lane object
  store corruption would have been inherited. No such condition was observed (`git archive`, `cat-file` and
  both runs exit 0).
- The unlanded readings are a moving target while the wave runs; only the 09:40:49 list is exact for its
  timestamp, and a later reader will see more paths (my own report) until integration.
- No `/tmp` path is cited as evidence; all evidence paths are the frozen repo bytes or `$S` (removed after
  the report was written).

## Findings

- **F1 — LOW (no defect; the measured claim)** — `SKILL.md` registry pins: 0 mismatches at both
  `7197160b927f04db294c9553fb48fadcc7a3f4e3` and `487941b9395e89678af0053cc443cdb49cdee6e3`
  (`PIN_CHECK=met … mismatches=0` exit 0 each; 43 pins, all `state=match`; only lines 911/912 differ, by the
  substituted revision). Round 50 added no pin mismatch and broke no pin's ability to set itself up;
  `SKILL.md` is byte-identical across the round (`5c639d2c…`).
- **F2 — LOW (usage hazard, environmental class)** — `tools/mori-pin-check.py:113-132, 886-889`: `--rev` mode
  resolves revisions through `--repo` (default: the tool's grandparent directory) and materialises its export
  under `<repo>/.scratch`. Run literally "from a `git archive` extraction" it exits 2
  (`PIN_CHECK_SETUP unresolvable revision`, observed), and run with `--repo` pointed at the lane it would write
  into the lane's gitignored `.scratch`. The wave-2/round-51 brief should say `--repo <scratch clone>` (or keep
  a note), so a later seat does not read the exit 2 as a pin mismatch.
- **F3 — LOW (landing obligation, not a current defect)** — `.ufo/waves/round-50/a2w1*`: at 09:40:49 the live
  lane is `UNLANDED=dirty round=50 paths=5` (a2w1.ready, a2w1/swarm-registry.json, plus three seat reports),
  i.e. the round-47 M1 class ("work on disk, report filed before it is committed"). Nothing to fix mid-wave;
  the L1's integration commit must land the whole `a2w1/` directory, and a final `UNLANDED=clean round=50`
  (or an accounted list) before the round report is the operability receipt that it did.
- **F4 — LOW (corroboration, not a finding against the contract)** — `evidence/selftests/mori-pin-check.txt`
  carries 114 `PASS` / 0 `FAIL` arm lines and a final `PIN_CHECK_SELFTEST pass=114 fail=0` exit=0 line;
  `…/mori-unlanded-check.txt` carries 17 `PASS` / 0 `FAIL` and `UNLANDED_SELFTEST pass=17 fail=0` exit=0. This
  seat's independent runs at `487941b9` printed exactly `pass=114 fail=0` and `pass=17 fail=0` for those
  commands, matching the receipts and the SHONEN pins. Evidence only; the C1 verdict remains the L1's.

## Verification status

All statements above are observed command output from this seat's runs (command + output + exit code quoted);
no lane, fleet, jj or index state was mutated; no pacman transaction; no host log MESSAGE read; no credential
material read. `UNVERIFIED`: whether any pinned `--selftest` arm touches live host state (see named limits);
nothing else claimed beyond the measurements.
