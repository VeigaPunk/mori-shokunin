# Mo84E01C1Arms — round 84 w1: the two failing selftest arms for M24a/M24b

Seat: Mo84E01C1Arms (executor, leaf — no subagents, no labrat needed). Date: 2026-11-04.
Scope held: the only lane file written is
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-83/count-c1.py`, `selfcheck()`
only, plus this report. Scratch `/fast/scratch/hyaku/mori-r84/Mo84E01C1Arms/` (deleted before
yield; `ls` of the parent confirms absence). No tools installed; no pacman transaction; no lane,
OS or orchestration state changed. Only read-only git ran against the lane repo (`log`, `status`,
`rev-parse`, `cat-file`, `clone --shared`); the one `commit` ran inside the scratch fixture clone
with `-c user.name=t -c user.email=t@t` after asserting `rev-parse --show-toplevel` equalled the
clone dir. `HYAKU_SCRATCH` is unset in this environment, so every counter invocation below pins
`HYAKU_SCRATCH` (and `--scratch`) under the seat scratch dir to honour the never-/tmp rule; each
counter also cleans its own scratch in its `finally`.

## Change (one file)

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-83/count-c1.py` — in `selfcheck()`,
appended two detector arms between the `non_equivalent_still_survives` case and the
`ok = sum(...)` summary; every existing arm, `grade()`, `green()`, `killed()`, `MUTANTS`,
`EQUIVALENT`, `main()` and the `C1_COUNTER_SELFTEST pass=%d fail=%d` summary are byte-untouched.

1. `blind_case_tally` — fixture `combo.py` (pristine selftest: `pass=1 fail=0` rc 0) graded with
   two mutants: `combo_sensitive` (`GUARD = 1` → `GUARD = 0`, prints `fail=1` rc 1 → killed) and
   `combo_blind` (`NOOP = 1` → `NOOP = 2`, output unchanged → survives). Asserts `not met` and
   tail `killed=1 survivors=1 total=2` (the A4-operative assertion, not `killed=0`). Under M24a
   (`killed_n = total - equivalent`) the same fixture prints `killed=2`, so the arm fails and the
   mutant is killed.
2. `green_requires_fail_zero` — fixture `skip.py` whose pristine selftest exits 0 printing exactly
   `SELFTEST skipped` (no `fail=0` token), graded with one blind mutant `skip_blind`
   (`SKIP = 1` → `SKIP = 2`). Asserts `not met`, `pristine=red` in the tail and `survivors=1`.
   Under M24b (`green()` drops the `"fail=0"` requirement) the pristine reads green, so the arm
   fails and the mutant is killed.

Both arm labels are the literal strings the frozen counter checks (A5). The two protected lines
still occur exactly once (measured below): `killed_n = total - survivors - equivalent` and the
four-space-indented `    return rc == 0 and "fail=0" in out and not FAIL.search(out)`.

## Commands and outputs (all run by this seat)

```text
$ echo "HYAKU_SCRATCH=${HYAKU_SCRATCH:-unset}"
HYAKU_SCRATCH=unset

$ HYAKU_SCRATCH=$S/st python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-83/count-c1.py --selftest
PASS sensitive_killed mutants=1 killed=1 equivalent=0 survivors=0 total=1 pristine=green | MUTANT sensitive.py trip_guard killed rc=1
PASS blind_survives mutants=1 killed=0 equivalent=0 survivors=1 total=1 pristine=green
PASS duplicate_anchor_excluded mutants=0 killed=0 equivalent=0 survivors=0 total=0 pristine=green
PASS red_pristine_reported mutants=0 killed=0 equivalent=0 survivors=0 total=0 pristine=red
PASS equivalent_excluded_when_coupled mutants=1 killed=0 equivalent=1 survivors=0 total=1 pristine=green
PASS non_equivalent_still_survives mutants=1 killed=0 equivalent=0 survivors=1 total=1 pristine=green
PASS blind_case_tally mutants=2 killed=1 equivalent=0 survivors=1 total=2 pristine=green | MUTANT combo.py combo_sensitive killed rc=1;MUTANT combo.py combo_blind survived rc=0
PASS green_requires_fail_zero mutants=1 killed=0 equivalent=0 survivors=1 total=1 pristine=red
C1_COUNTER_SELFTEST pass=8 fail=0
selftest-rc=0

$ python3 -c "…s.count(anchor) for the two M24 old anchors + both arm labels…"
1 'killed_n = total - survivors - equivalent'
1 '    return rc == 0 and "fail=0" in out and not FAIL.search(o'   # truncated repr, count of full string
1 'blind_case_tally'
1 'green_requires_fail_zero'

# probe: shared clone + my edited file committed as fixture
$ git clone --quiet --shared /home/vgpnk/Projects/shokunin/mori-shokunin $S/probe/lane
$ git -C $S/probe/lane rev-parse --show-toplevel     # asserted == $S/probe/lane
toplevel-ok=/fast/scratch/hyaku/mori-r84/Mo84E01C1Arms/probe/lane
$ cp <edited file> $S/probe/lane/.ufo/waves/round-83/count-c1.py
$ git -C $S/probe/lane -c user.name=t -c user.email=t@t commit -aqm probe
probe-rev=c727429eba7ddc226f6743834e1878fbb7f2a0d0   # = 39190f8a (A2 HEAD) + this file

$ HYAKU_SCRATCH=$S/probe python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/count-c1.py c727429eba7ddc226f6743834e1878fbb7f2a0d0 --repo $S/probe/lane --scratch $S/probe/w
MUTANT count-c1.py M24a_killed_tally killed rc=1
MUTANT count-c1.py M24b_green_fail_token killed rc=1
MUTANT count-c2.py M24c_met_unclassified equivalent rc=0
MUTANT count-c2.py M24d_met_residual equivalent rc=0
C1=met mutants=4 killed=2 equivalent=2 survivors=0 total=4 pristine=green detector=green rev=c727429eba7d
probe-rc=0

# per-kill arm attribution: each mutant copy's own --selftest
$ python3 -c "…apply M24a / M24b to the edited bytes, run --selftest on each copy…"
M24a rc=1 ['FAIL blind_case_tally mutants=2 killed=2 equivalent=0 survivors=1 total=2 pristine=green | MUTANT combo.py combo_sensitive killed rc=1;MUTANT combo.py combo_blind survived rc=0'] ['C1_COUNTER_SELFTEST pass=7 fail=1']
M24b rc=1 ['FAIL green_requires_fail_zero mutants=1 killed=0 equivalent=0 survivors=1 total=1 pristine=green'] ['C1_COUNTER_SELFTEST pass=7 fail=1']

# causality control: same command at the freeze revision (arms absent there)
$ git -C $S/freeze/lane cat-file -e daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4
$ HYAKU_SCRATCH=$S/freeze python3 -I <round-84 counter> daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4 --repo $S/freeze/lane --scratch $S/freeze/w
MUTANT count-c1.py M24a_killed_tally survived rc=0
MUTANT count-c1.py M24b_green_fail_token survived rc=0
MUTANT count-c2.py M24c_met_unclassified equivalent rc=0
MUTANT count-c2.py M24d_met_residual equivalent rc=0
C1=unmet mutants=4 killed=0 equivalent=2 survivors=2 total=4 pristine=green detector=green rev=daa77bd5684c
freeze-rc=1

# the frozen counter's own detector selftest, worktree bytes
$ HYAKU_SCRATCH=$S/det python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/count-c1.py --selftest
PASS sensitive_killed … PASS blind_case_tally mutants=2 killed=1 … PASS green_requires_fail_zero mutants=1 … pristine=red
PASS green_direct green() boundary / PASS killed_direct killed() boundary / PASS target_split_ok 2/2/4
C1_COUNTER_SELFTEST pass=15 fail=0
r84-selftest-rc=0
```

## Verified

- `python3 -I .ufo/waves/round-83/count-c1.py --selftest` → `C1_COUNTER_SELFTEST pass=8 fail=0`,
  rc 0; the six pre-existing arms pass byte-identically (labels and PASS lines unchanged) plus the
  two new arms with the exact required tails (`killed=1 survivors=1 total=2`; `pristine=red`).
- Probe at `c727429eba7ddc226f6743834e1878fbb7f2a0d0` (lane HEAD `39190f8a` + only this file):
  `C1=met mutants=4 killed=2 equivalent=2 survivors=0 total=4 pristine=green detector=green` rc 0 —
  the frozen target string, with M24c/M24d reading `equivalent` off the committed `count-c2.py`
  couplings.
- Kills attribute honestly: the M24a-mutated counter's selftest fails exactly `blind_case_tally`
  (`killed=2`), the M24b-mutated counter's fails exactly `green_requires_fail_zero`
  (`pristine=green`); each is `pass=7 fail=1` rc 1. No other arm moves under either mutant.
- Causality: at the freeze commit `daa77bd5` (arms absent) the same command reads
  `C1=unmet mutants=4 killed=0 equivalent=2 survivors=2` rc 1 — the two arms are the whole delta.
- Anchor integrity at the after bytes: both M24 `old` anchors and both arm labels occur exactly
  once; `grade()`/`green()`/`killed()` bodies and the protected lines are untouched.

## Not verified

- The integration revision's grade (L1's post-wave gate); my probe binds to
  `c727429eba7ddc226f6743834e1878fbb7f2a0d0` = `39190f8a` + this file only.
- Sibling worktree edits: `.ufo/waves/round-83/count-c2.py` was modified-but-uncommitted in the
  lane worktree during this seat (C3's in-flight bytes); my `equivalent=2` readings grade the
  committed bytes at the probe/freeze revisions, not those worktree bytes.
- The r84 counter's `<rev>` mode prints only `detector=green`; its internal `pass=15 fail=0` was
  observed via the separate `--selftest` invocation above, not inside the probe run.

## Defects in other seats' bytes

None found. (Pre-existing observation, unchanged by this seat and already recorded in
`.ufo/waves/round-83/w1/Mo83R01C1.md` §7.1: the counter's `lane=unresolvable` fallback hard-codes
`~/Projects/shokunin/mori-shokunin` — fine on this host/user, portable only by named limit.)

## Tooling record

No tool installed or upgraded (python3 + system git only); no pacman transaction of any kind.
