# Mo85E01C1Arms — the two X1/X2 failing arms for the r84 counter (round 85, wave w1, attempt 1)

Seat: give `.ufo/waves/round-84/count-c1.py` the two failing selftest arms the round-85 C1
counter requires (contract P-C1, frozen at `ab2608655ea52ba6d151b3a31d69a3b18cd2b41e`). Judged
on operability. All scratch work under `/fast/scratch/hyaku/mori-r85/Mo85E01C1Arms/` (deleted
before yield). No tools installed or upgraded; no pacman transaction; no lane/OS/orchestration
state changed; only the assigned file and this report were written in the lane.

## 0. Collision finding (honest record)

I read the worktree counter as 15 arms (the entering-revision state, matching the measured
control `arms=15 ... missing=killed_mutant_with_coupling_not_equivalent,duplicate_coupling_not_equivalent`),
landed my two arms, and the edit result's own context lines showed a
`duplicate_coupling_not_equivalent` block I had not written at lines 299-301. Re-read confirmed
the file then carried FOUR new `cases.append` blocks for the two frozen labels: the L1 stand-in
had already landed the two arms while my seat was reading the stale bytes, and my append
duplicated them. The L1 messaged me to stop writing (the duplicated state's pristine selftest
read `pass=17 fail=2`), and restored the single-pair 17-arm version. Since that message this
seat has written nothing to the counter; everything below verifies the restored on-disk bytes.
Net effect of the collision: no byte damage survived (anchors still ×1, one arm per label),
one duplicated-edit window, no measurement was taken from the broken state.

## 1. What is on disk (restored state this seat verified, not authored)

`.ufo/waves/round-84/count-c1.py`, `selfcheck()` only, 17 arms, both new labels exactly once,
both before `target_split_ok`:

- `killed_mutant_with_coupling_not_equivalent` — fixture `tools/killed_coupled.py`: `GUARD = 1`
  (the anchor), the three M24d coupling markers each exactly once
  (`agreed == len(snapshot_tokens)`, `residual += duplicates`, `duplicates == 0`), and a
  `print('FAKE pass=%d fail=%d' ...)`/`raise SystemExit(...)` pair keyed on `GUARD == 1`.
  Grades `("tools/killed_coupled.py", "M24d_met_residual", "GUARD = 1", "GUARD = 0")`; asserts
  met, `equivalent=0` in tail, and a ` killed ` line.
- `duplicate_coupling_not_equivalent` — fixture `tools/dup_coupling.py`: same three markers with
  `agreed == len(snapshot_tokens)` twice, plain `print('FAKE pass=1 fail=0')` (mutation
  non-killing). Same grade tuple; asserts not met, a `coupling-absent` extra, `survivors=1`.

Why each arm kills its mutant: X1 (`if not k and coupling is not None:` → `if coupling is not
None:`) routes a killed-but-coupled mutant into the equivalence branch, so arm 1's fixture grades
`equivalent`/`equivalent=1` and the assertion `met and equivalent=0 and killed-line` fails. X2
(`== 1` → `>= 1`) makes the duplicated marker read coupled, so arm 2's fixture grades
`equivalent`/`met`/`survivors=0` and the assertion `not met and coupling-absent and survivors=1`
fails. No other arm reaches those code paths with a flipping input (checked by the X1/X2 runs:
exactly one FAIL line each).

Byte facts (grep): `if not k and coupling is not None:` ×1; `coupled = all(base.count(marker)
== 1 for marker in coupling)` ×1; `cases.append` ×17; each new fixture `write(d, ...)` ×1.

## 2. Acceptance evidence (commands quoted; run from my scratch, absolute paths)

Copy: `cp /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/count-c1.py
$S/c1-armed.py` (all runs `python3 -I`, `--scratch` under `$S`, cwd `$S`).

1. Pristine selftest — `python3 -I $S/c1-armed.py --selftest --scratch $S/st1`:
   `C1_COUNTER_SELFTEST pass=17 fail=0`, rc 0. No FAIL lines.
2. X1 mutant (`if not k and coupling is not None:` → `if coupling is not None:`, anchor count
   asserted 1 before replace) — `python3 -I $S/c1-x1.py --selftest --scratch $S/st2`:
   rc 1, `C1_COUNTER_SELFTEST pass=16 fail=1`, FAIL line
   `FAIL killed_mutant_with_coupling_not_equivalent mutants=1 killed=0 equivalent=1 survivors=0
   total=1 pristine=green | MUTANT killed_coupled.py M24d_met_residual equivalent rc=1`.
3. X2 mutant (`== 1` → `>= 1`, anchor count asserted 1) — `python3 -I $S/c1-x2.py --selftest
   --scratch $S/st3`: rc 1, `C1_COUNTER_SELFTEST pass=16 fail=1`, FAIL line
   `FAIL duplicate_coupling_not_equivalent mutants=1 killed=0 equivalent=1 survivors=0 total=1
   pristine=green`.
4. Diff scope — `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --numstat --
   .ufo/waves/round-84/count-c1.py` → `29  0  .ufo/waves/round-84/count-c1.py` (identical
   against HEAD `91f657f6` and against the freeze commit `ab260865`; additions only: the two arm
   blocks — fixtures, writes, grade calls, appends, comments — zero deletions; the arms are
   working-tree bytes, the L1 owns the commit).
5. r84 frozen target reachable — `python3 -I $S/c1-armed.py
   ab2608655ea52ba6d151b3a31d69a3b18cd2b41e --repo /home/vgpnk/Projects/shokunin/mori-shokunin
   --scratch $S/st4`: rc 0, `MUTANT count-c1.py M24a_killed_tally killed rc=1` / `M24b killed
   rc=1` / `count-c2.py M24c_met_unclassified equivalent rc=0` / `M24d_met_residual equivalent
   rc=0`, tail `C1=met mutants=4 killed=2 equivalent=2 survivors=0 total=4 pristine=green
   detector=green rev=ab2608655ea5`.
6. Full P-C1 target end-to-end — `git clone --shared` of the lane into `$S/clone` (toplevel
   asserted equal to the clone dir), armed counter copied in and committed with
   `-c user.name=t -c user.email=t@t` → clone rev `bf8d81240450c5c74a4d5a2b3b64a4447b095817`;
   then `python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-85/count-c1.py
   bf8d8124... --repo $S/clone --scratch $S/st5`: rc 0,
   `MUTANT count-c1.py X1_killed_rescued_as_equivalent killed rc=1`,
   `MUTANT count-c1.py X2_coupling_duplicate_passes killed rc=1`,
   `C1=met mutants=2 killed=2 survivors=0 total=2 arms=17 r84=met rev=bf8d81240450` — the exact
   frozen target sentence of P-C1, over graded bytes (not merely selftest-simulated).

## 3. Risks / notes for the L1

- The arms are uncommitted worktree bytes on top of `91f657f6`; the commit is yours. Until it
  lands, the round-85 counter run at the lane HEAD still reads the entering control
  (`arms=15`, survivors=2).
- Collision window (§0): if any other receipt quotes the transient 4-block or `fail=2` state,
  supersede it with this report's §1/§2 readings.
- The two arms grade through the counter's own `grade()` with synthetic fixtures; the r84
  counter's 4-mutant grade path and the r85 counter's full grade path were both re-run over the
  armed bytes here, so the target line is proven against bytes, not asserted.
