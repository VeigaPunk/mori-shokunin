# Mo56ExecDriverSelftest — round 56, wave w1

Seat scope: the driver-liveness probe's own 13-case selftest
(`tools/mori-driver-liveness.py --selftest`) at the freeze tip
`8be2717b0809281d07dffe83dad424a4859e0747`, plus a falsification battery
against the frozen C1 predicate. Detection and report only; nothing in the
lane, the fleet root, the jj/git state or the watchdog log was mutated.

- Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`
- Freeze tip examined: `8be2717b0809281d07dffe83dad424a4859e0747`
- Tool pin asserted by the frozen counter:
  `6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997`
- Scratch: `/fast/scratch/hyaku/mori-r56/Mo56ExecDriverSelftest/` (removed on exit)
- Interpreter observed: `Python 3.14.8 (main, Oct 2, 2026, 10:23:31) [GCC 16.2.1]`

## 1. Method

One archive extraction of the freeze tip into scratch (no clone, no mirror):

```
S=/fast/scratch/hyaku/mori-r56/Mo56ExecDriverSelftest
mkdir -p "$S/tmp" "$S/final/tmp" "$S/final/home"
git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive \
    8be2717b0809281d07dffe83dad424a4859e0747 | tar -x -C "$S/final"
```

Byte identity of the extracted tool against the frozen pin:

```
$ sha256sum tools/mori-driver-liveness.py
6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997  tools/mori-driver-liveness.py
```

Matches `freeze-sha256.txt` (`tools/mori-driver-liveness.py@6ced9da9`) and the
`PIN =` line in `.ufo/waves/round-56/count-c1.py`. The lane worktree copy has
the same sha (no drift between the frozen commit and the working tree).

The frozen fixture tree in the archive is byte-identical to the lane worktree
copy: recursive `diff` over `.ufo/waves/round-56/fixtures/driver` reported no
difference, and per-file `sha256sum` manifests were equal. The
`state-shapes/state/kake.round -> mori.round` symlink survives `git archive`
and is re-materialized as a symlink by the counter's own fixture
materializer (verified: `lrwxrwxrwx ... kake.round -> mori.round` inside the
counter's `TMPDIR/mori-r56-c1-*/tool/...` tree).

## 2. The three required runs

Environment: `PWD=$S/final`, `TMPDIR=$S/final/tmp`, `HOME=$S/final/home`
(both redirected into scratch), command
`python3 tools/mori-driver-liveness.py --selftest`.

```
--- run 1 ---
DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0
exit=0
--- run 2 ---
DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0
exit=0
--- run 3 ---
DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0
exit=0
```

All three runs: stdout only, empty stderr, exit 0, identical bytes. Twenty
consecutive runs in one shell collapsed to a single distinct output line
(`20 DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0`) — the selftest is
deterministic, no flakiness observed.

The same line is produced with the environment varied (each exit 0 except the
one noted in §5):

| variation | result |
|---|---|
| `HOME` unset | pass=13 fail=0 skipped=0, exit 0 |
| `HOME=/nonexistent` | pass=13 fail=0 skipped=0, exit 0 |
| `HOME=/` | pass=13 fail=0 skipped=0, exit 0 |
| `TMPDIR` unset (falls back to `/tmp`) | pass=13 fail=0 skipped=0, exit 0, no `/tmp/mori-driver-liveness-*` leftover |
| `PYTHONHASHSEED=0 LC_ALL=C` | pass=13 fail=0 skipped=0, exit 0 |
| `python3 -B -E` | pass=13 fail=0 skipped=0, exit 0 |
| `TZ=Pacific/Kiritimati` / `TZ=Etc/GMT+12` | pass=13 fail=0 skipped=0, exit 0 |
| cwd = scratch root | pass=13 fail=0 skipped=0, exit 0 |
| cwd = `/`, absolute tool path | pass=13 fail=0 skipped=0, exit 0 |
| cwd = `$S/tmp2`, relative tool path | pass=13 fail=0 skipped=0, exit 0 |

The tool reads no `HOME`/user-config path at all; the only environment
dependency is `TMPDIR` (one case, `t_empty_log`, materialises an empty log in
`tempfile.mkdtemp(dir=os.environ.get("TMPDIR") or None)` and removes it again).
After a selftest run the redirected `TMPDIR` is empty — the tool leaves no
temp residue. The counter, by contrast, does leave its materialization tree
behind (see §5, LOW-3).

## 3. Comparison with the frozen evidence directory

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/evidence/`
holds ten files. Relevant ones:

- `c1-at-freeze.txt` → `C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=3f494b49cde612d929e82887a48e1660c022c359`, exit 0
- `selftest-c1-counter.txt` → `C1_COUNTER_SELFTEST pass=1 fail=0`, exit 0
- `controls.txt` → `do-nothing-c1 PASS C1=unmet … failed=tool_absent rev=5b295eee…`
- `driver-liveness-live.txt` → the live JSON receipt
- `selftest-vote-bind.txt` → `VOTE_BIND_SELFTEST pass=16 fail=0` (the C2 tool)

**The driver's own selftest is NOT separately receipted.** The literal string
`DRIVER_LIVENESS_SELFTEST` appears nowhere under
`.ufo/waves/round-56/evidence/` — grep across the whole round-56 directory
finds it only inside `count-c1.py` (the expected-value constant and the
docstring) and inside the dispatch artifacts (`w1-spec.json`,
`w1-dispatch.json`, `build-w1-spec.py`). The string `pass=13` likewise appears
in no evidence file. The C1 arm is attested only indirectly, through the
counter's own aggregate verdict line `selftest=ok` in `c1-at-freeze.txt`.

This is an asymmetry with C2, which does have a standalone tool-selftest
receipt (`selftest-vote-bind.txt` → `VOTE_BIND_SELFTEST pass=16 fail=0`).
Recorded as a named limit below (LOW-1); I did not modify any evidence file.

Re-running the frozen counter reproduces the frozen verdicts exactly:

```
$ python3 .ufo/waves/round-56/count-c1.py 8be2717b0809281d07dffe83dad424a4859e0747 \
      --repo /home/vgpnk/Projects/shokunin/mori-shokunin
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
exit=0

$ python3 .ufo/waves/round-56/count-c1.py 3f494b49cde612d929e82887a48e1660c022c359 \
      --repo /home/vgpnk/Projects/shokunin/mori-shokunin
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=3f494b49cde612d929e82887a48e1660c022c359
exit=0

$ python3 .ufo/waves/round-56/count-c1.py 5b295eeebd87ebd610d8d39bfe2035742f740cfa \
      --repo /home/vgpnk/Projects/shokunin/mori-shokunin
C1=unmet selftest=bad fixtures=bad entry=bad row=bad norem=bad failed=tool_absent rev=5b295eeebd87ebd610d8d39bfe2035742f740cfa
exit=1
```

The last line reproduces the frozen do-nothing control in `controls.txt`
byte-for-byte in substance (`failed=tool_absent`, exit 1). The freeze
commit's own counter also reports `C1=met` at `3f494b49`, so the freeze
commit and the controls/receipts commit agree.

Per-fixture re-run against the frozen `EXPECT_FIX` table (all nine):

```
attempt-rollover   want_malformed=0 got=0 verdict=DRIVER_LIVENESS_OK rc=0 OK
fails-and-dead     want_malformed=0 got=0 verdict=DRIVER_LIVENESS_OK rc=0 OK
hyaku-pairing      want_malformed=0 got=0 verdict=DRIVER_LIVENESS_OK rc=0 OK
in-flight          want_malformed=0 got=0 verdict=DRIVER_LIVENESS_OK rc=0 OK
legacy-grammar     want_malformed=0 got=0 verdict=DRIVER_LIVENESS_OK rc=0 OK
malformed          want_malformed=5 got=5 verdict=DRIVER_LIVENESS_OK rc=0 OK
state-shapes       want_malformed=0 got=0 verdict=DRIVER_LIVENESS_OK rc=0 OK
two-lanes          want_malformed=0 got=0 verdict=DRIVER_LIVENESS_OK rc=0 OK
variants           want_malformed=0 got=0 verdict=DRIVER_LIVENESS_OK rc=0 OK
```

Nine fixture directories, nine `EXPECT_FIX` entries — no fixture outside the
frozen table.

## 4. Falsification battery (the load-bearing part)

Two harnesses, both in scratch, both against copies of the tool (the lane's
tool file was never edited).

### 4.1 Mutation sweep against the tool's own 13-case selftest

One output-field computation replaced at a time; "SURVIVED" means the frozen
selftest still printed `pass=13 fail=0 skipped=0` and exited 0, i.e. the field
is asserted nowhere.

```
[lanes_launches      ] KILLED   exit=1 :: pass=6 fail=7  failed=t_hyaku_pairing,t_attempt_rollover,t_legacy_grammar,t_malformed_refusal,t_two_lanes,t_variants,t_other_lines_not_malformed
[lanes_completes     ] KILLED   exit=1 :: pass=9 fail=4  failed=t_hyaku_pairing,t_attempt_rollover,t_legacy_grammar,t_variants
[lanes_deads         ] KILLED   exit=1 :: pass=10 fail=3 failed=t_attempt_rollover,t_launch_fail_and_dead_legacy,t_variants
[lanes_launch_fails  ] KILLED   exit=1 :: pass=12 fail=1 failed=t_launch_fail_and_dead_legacy
[lanes_wraps         ] KILLED   exit=1 :: pass=12 fail=1 failed=t_variants
[lanes_rounds_seen   ] SURVIVED exit=0 :: pass=13 fail=0 skipped=0
[lanes_unclosed      ] KILLED   exit=1 :: pass=11 fail=2 failed=t_in_flight,t_variants
[lanes_in_flight     ] KILLED   exit=1 :: pass=10 fail=3 failed=t_in_flight,t_two_lanes,t_variants
[lanes_last_launch_ts] SURVIVED exit=0 :: pass=13 fail=0 skipped=0
[log_lines           ] SURVIVED exit=0 :: pass=13 fail=0 skipped=0
[log_malformed       ] KILLED   exit=1 :: pass=11 fail=2 failed=t_malformed_refusal,t_other_lines_not_malformed
[log_other_lines     ] KILLED   exit=1 :: pass=11 fail=2 failed=t_variants,t_other_lines_not_malformed
[log_newest_ts       ] SURVIVED exit=0 :: pass=13 fail=0 skipped=0
[log_examples_cap    ] SURVIVED exit=0 :: pass=13 fail=0 skipped=0
[log_mtime_age       ] SURVIVED exit=0 :: pass=13 fail=0 skipped=0
[state_regular       ] KILLED   exit=1 :: pass=12 fail=1 failed=t_state_shapes
[state_symlink       ] KILLED   exit=1 :: pass=12 fail=1 failed=t_state_shapes
[state_dir           ] KILLED   exit=1 :: pass=12 fail=1 failed=t_state_shapes
[state_other         ] SURVIVED exit=0 :: pass=13 fail=0 skipped=0
[notes_dropped       ] SURVIVED exit=0 :: pass=13 fail=0 skipped=0
[schema_changed      ] SURVIVED exit=0 :: pass=13 fail=0 skipped=0
[dead_clears_round   ] KILLED   exit=1 :: pass=12 fail=1 failed=t_attempt_rollover
[attempt_key_ignored ] SURVIVED exit=0 :: pass=13 fail=0 skipped=0
```

The selftest is genuinely load-bearing for the nine counters it does assert
(launches, completes, deads, launch_fails, wraps, unclosed, in_flight,
malformed, other_lines, and the state-dir regular/symlink/dir shapes, and the
"dead clears the round" rule). Ten mutated fields pass it untouched.

### 4.2 The same sweep through the frozen C1 counter

Each mutant was committed in a scratch fixture repo (created with
`git init -q` inside scratch; `git rev-parse --show-toplevel` asserted equal
to the fixture dir before the first commit; throwaway identity
`fixture <fixture@example.invalid>`; never committed anywhere else), the
counter's `PIN` re-pinned to the mutant's sha, and the frozen counter run at
that rev.

```
[launches_zero]        exit=1 :: C1=unmet … failed=selftest
[completes_zero]       exit=1 :: C1=unmet … failed=selftest
[malformed_zero]       exit=1 :: C1=unmet … failed=selftest,fixtures
[in_flight_false]      exit=1 :: C1=unmet … failed=selftest
[rounds_seen_zero]     exit=0 :: C1=met  selftest=ok fixtures=ok entry=ok row=ok norem=ok
[examples_cap_off]     exit=0 :: C1=met  selftest=ok fixtures=ok entry=ok row=ok norem=ok
[symlink_zero]         exit=1 :: C1=unmet … failed=selftest
[event_kw_narrow]      exit=1 :: C1=unmet … failed=selftest,fixtures
[deads_zero]           exit=1 :: C1=unmet … failed=selftest
[wraps_zero]           exit=1 :: C1=unmet … failed=selftest
[unclosed_zero]        exit=1 :: C1=unmet … failed=selftest
[health_word_inject]   exit=1 :: C1=unmet … failed=selftest,norem
```

Ten of the ten surviving fields also survive the whole frozen predicate once
the pin is re-pinned:

```
[rounds_seen_zero]      exit=0 :: C1=met …
[last_launch_ts_zero]   exit=0 :: C1=met …
[log_lines_zero]        exit=0 :: C1=met …
[examples_cap_off]      exit=0 :: C1=met …
[mtime_age_none]        exit=0 :: C1=met …
[state_other_zero]      exit=0 :: C1=met …
[notes_dropped]         exit=0 :: C1=met …
[schema_changed]        exit=0 :: C1=met …
[attempt_key_ignored]   exit=0 :: C1=met …
[newest_ts_min]         exit=0 :: C1=met …
```

### 4.3 What actually holds C1 up today: the pin

With the frozen `PIN` left in place, every one of the mutants above is
killed by the pin arm alone:

```
tautological mutant, frozen PIN  -> C1=unmet … failed=pins   exit=1
rounds_seen mutant, frozen PIN   -> C1=unmet … failed=pins   exit=1
```

So the current `C1=met` rests on the sha256 pin, with the selftest and the
fixture arm as the semantic checks behind it.

### 4.4 The selftest arm is a substring assertion on self-reported stdout

`count-c1.py` checks `EXPECT_SELFTEST not in (out or "")` — a substring test
against the tool's own printed line — plus `rc != 0`. A mutant that
hardcodes the printed line and forces `return 0` satisfies it:

```
tautological mutant (print hardcoded line + return 0 + unclosed broken), PIN re-pinned
  -> C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok   exit=0
  -> its own stdout: DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0 failed=t_in_flight,t_variants
```

Note the printed line still lists `failed=t_in_flight,t_variants` while
claiming `pass=13 fail=0` — the substring match accepts it. This mutant is
invisible to the selftest arm, to the fixture arm (the fixture arm asserts
only `verdict` and `log.malformed`) and to the norem arm; only the pin
catches it. Reachable only after a re-pin, which the contract permits the L1
to do when correcting tool data.

### 4.5 The norem arm scans only the pre-`# selftest` prefix

`count-c1.py` computes `low = tool_src.split("# selftest", 1)[0].lower()` and
looks for `healthy / unhealthy / failed lane / is stuck / wedged` in that
prefix. The marker sits at line 248; `main()` (line 451) and the whole
selftest region are after it. Injecting a verdict string into `main()`:

```
health verdict in main() (post-marker), PIN re-pinned
  -> C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok   exit=0
  -> the mutant really prints it:  lane is wedged and unhealthy
```

A comment carrying the same words after the marker likewise yields `norem=ok`.
So the "no health-verdict string" guarantee holds only for the pre-marker
prefix; the tool's own production entry point is outside the scan. The
pre-marker text is clean today (the three health words occur only inside the
`# selftest` region, in the `t_no_health_verdict` case's own assertion
strings, and the `notes` string in `run()` says "not health verdicts").

### 4.6 Attempt-pairing semantics are asserted nowhere

`parse_log` keys an open launch by `(round, attempt)` and a `complete` by its
own `attempt=`, so a `complete` for a different attempt does not close the
launch. No frozen fixture contains a mismatched attempt pair (all `attempt=`
occurrences in the nine fixtures pair 1↔1 or 2↔2), and the `attempt_key_ignored`
mutant (`key = (int(round_s), None)`) is not detected by anything. Demonstrated
on a scratch fixture `launch … attempt=1` + `complete … attempt=2`:

```
ORIGINAL  -> unclosed=1
MUTANT    -> unclosed=0
mutant's own selftest: DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0  (exit 0)
```

The tool's own docstring advertises "unclosed = launches with no
same-(lane,round,attempt) complete", so this is the documented pairing
semantics with zero frozen coverage.

### 4.7 Live receipt reproduces, with one expected drift

Re-running the probe read-only against the live fleet log
(`/home/vgpnk/Projects/shokunin/.ufo/watchdog.log`, no writes) and comparing
to `evidence/driver-liveness-live.txt`: identical `verdict`
(`DRIVER_LIVENESS_OK`), identical lane set (23 lanes), identical
`malformed=0`, `other_lines=121`, identical `state_dir` shape
(`regular=21, symlink=0, dir=0, other=0`), identical `notes` and `schema`.
Two drift deltas, both explained by the log growing between the receipt
(10:18) and now (10:56+): `log.lines` 1728 → 1729, and lane `kake` gained
one `complete` (`completes` 50 → 51, `unclosed` 13 → 12, `in_flight`
true → false). `mtime_age_s` moved from 1445.9 to 319.0. Not a defect; noted
so the receipt is not read as a live invariant.

## 5. Other observations

- **Skips are not failures.** With the fixture tree renamed away, the tool
  prints `pass=2 fail=0 skipped=11` and exits **0**. The counter still catches
  it (the exact expected line is absent → `selftest` arm fails), so the
  predicate is safe, but the tool's own exit code is 0 on a degraded run.
- **Counter temp leak.** `count-c1.py` creates `tempfile.mkdtemp(prefix=
  "mori-r56-c1-", …)` and never removes it; one such tree per run remains in
  `TMPDIR`. Observed directly. Harmless but untidy, and it makes `TMPDIR`
  growth proportional to counter invocations.
- **Counter selftest is near-tautological.** `count-c1.py --selftest` asserts
  only `len(EXPECT_FIX) == 9` and `EXPECT_SELFTEST.startswith("DRIVER_…")`
  → `C1_COUNTER_SELFTEST pass=1 fail=0`. It executes none of the counter's
  own arms.
- **Fixture materialization by the counter is faithful**, including the
  symlink, and the tool resolves its fixture directory from its own
  `dirname(dirname(__file__))`, so the `cwd/tool/tools/` + `cwd/tool/.ufo/`
  nesting in `run_tool` is correct.
- **No host mutation.** The tool opens its inputs read-only and writes
  nothing outside `TMPDIR` (one temp file, removed). I never wrote
  `.ufo/watchdog.log` or `.ufo/state`, never ran `systemctl`, never touched a
  cgroup or sysctl, never killed or signalled a process. `git` was used
  read-only against the lane repo (`rev-parse`, `status`, `archive`); all
  commits were confined to the scratch fixture repo.
- The lane worktree showed `M LOG.md`, `M SCORECARD.md`, `M SHONEN.md`,
  `?? .ufo/waves/round-56/w1/` and `?? corpus/lessons/round-56.md` — these
  are other seats' and the L1's edits, present before and after my work; I
  touched none of them.
- No tool was installed or upgraded for this seat; none was needed
  (`python3`, `git`, `tar`, `diff`, `sha256sum` were sufficient). The
  operator's tooling directive was therefore not exercised.

## 6. Verdict on the assigned claim

**Confirmed, at the freeze tip, with the frozen bytes.** Three consecutive
runs of `python3 tools/mori-driver-liveness.py --selftest` from an archive of
`8be2717b0809281d07dffe83dad424a4859e0747`, with `TMPDIR` and `HOME`
redirected into scratch, each printed
`DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0` with empty stderr and
exit 0; the result is deterministic across twenty runs and across HOME/TMPDIR/
TZ/locale/hash-seed/cwd variations. The frozen C1 counter reproduces
`C1=met …` at both the freeze commit and the controls commit, and reproduces
the `failed=tool_absent` do-nothing control at the entering tip.

**Not falsified.** No mutation of the shipped tool at the frozen pin escapes
the frozen predicate: eleven of the twenty-five mutated output fields and
every counter-critical field are killed by the selftest or fixture arms, and
the pin kills the rest.

**Falsified only in the counter's future-facing structure** (§4.4, §4.5,
§4.6): the predicate's semantic strength is the pin plus nine asserted
fields; the selftest arm is a substring match on self-reported stdout, the
norem arm scans only a text prefix, and ten output fields plus the documented
attempt-pairing rule have no assertion anywhere. These are counter/selftest
design limits, not defects in the shipped tool's data — the tool's bytes at
the frozen pin are correct as far as this seat can measure, and the tool
emits no health verdict in its normal output.

## 7. Files changed

Only this report:
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/w1/Mo56ExecDriverSelftest.md`

No lane source, counter, contract, evidence file, corpus file or tool was
modified. All fixtures, clones, mutants and temp trees lived under
`/fast/scratch/hyaku/mori-r56/Mo56ExecDriverSelftest/` and were removed on
exit.

## Findings

- **MED — selftest arm is a substring assertion on self-reported stdout.**
  `count-c1.py:131` (`elif rc != 0 or EXPECT_SELFTEST not in (out or "")`)
  accepts a tool that prints the expected line verbatim and exits 0, even
  while its own output lists `failed=t_in_flight,t_variants`. Demonstrated
  end-to-end: such a mutant, with a broken `unclosed` computation and a
  re-pinned `PIN`, yields `C1=met selftest=ok … exit=0`. Today only the sha256
  pin stops it; the arm is not independently falsifying. Routed item for
  round 57: the selftest arm should assert the exit code plus the absence of
  a `failed=` clause, or the counter should execute the case list itself.
  (Lives in `.ufo/waves/round-56/count-c1.py:128-132` and `:39`.)

- **MED — norem arm scans only the text before the `# selftest` marker.**
  `count-c1.py:162` computes `tool_src.split("# selftest", 1)[0]`; the marker
  is at `tools/mori-driver-liveness.py:248` and the tool's production entry
  point `main()` is at `:451`, outside the scanned prefix. A verdict string
  injected into `main()` prints (`lane is wedged and unhealthy`) and the
  counter still reports `norem=ok` / `C1=met`. The no-health-verdict
  guarantee therefore does not currently extend to the whole tool file.
  Routed item for round 57: scan the whole file, or scan the region that
  excludes only the assertion strings of `t_no_health_verdict`.
  (`.ufo/waves/round-56/count-c1.py:161-164`, `tools/mori-driver-liveness.py:248,451`.)

- **MED — ten output fields and the attempt-pairing rule have no assertion.**
  Surviving the tool's 13-case selftest *and* the whole frozen predicate
  (with a re-pinned pin): `lanes.rounds_seen`, `lanes.last_launch_ts`,
  `log.lines`, `log.newest_ts`, `log.examples` cap, `log.mtime_age_s`,
  `state_dir.other`, `notes`, `schema`, and the `(round, attempt)` pairing
  key. The last is documented behaviour ("unclosed = launches with no
  same-(lane,round,attempt) complete", `tools/mori-driver-liveness.py:34`)
  and is observable — a mismatched attempt pair gives `unclosed=1` on the
  shipped tool and `unclosed=0` on the attempt-key mutant — but no frozen
  fixture contains such a pair. Routed item for round 57: add a fixture with
  a mismatched attempt pair and assert `rounds_seen`, `last_launch_ts` and
  `log.lines`.
  (`tools/mori-driver-liveness.py:34,113-118,169-176`; fixtures under
  `.ufo/waves/round-56/fixtures/driver/`.)

- **MED — the driver's own selftest is not separately receipted.** The string
  `DRIVER_LIVENESS_SELFTEST` appears in no file under
  `.ufo/waves/round-56/evidence/`; the C1 arm is attested only by the
  counter's aggregate `selftest=ok` in `c1-at-freeze.txt`. The C2 tool has a
  standalone receipt (`selftest-vote-bind.txt`), so the asymmetry is a
  round-56 packaging gap rather than a policy. Routed item for round 57: land
  a `selftest-driver-liveness.txt` receipt beside the C2 one.
  (`.ufo/waves/round-56/evidence/` — absent file.)

- **LOW — skipped cases do not fail the tool.** With the fixture tree
  absent, `tools/mori-driver-liveness.py --selftest` prints
  `pass=2 fail=0 skipped=11` and exits 0; `selftest()` returns
  `0 if failed == 0 else 1` and ignores `skipped`. The frozen counter still
  catches the degraded run through its exact-line check, so C1 is not
  endangered, but the tool's own exit code is not a sufficient gate.
  (`tools/mori-driver-liveness.py:426-448`.)

- **LOW — the counter leaks its materialization tree.** `count-c1.py:126`
  creates `tempfile.mkdtemp(prefix="mori-r56-c1-", …)` and never removes it;
  one tree per invocation stays in `TMPDIR` (observed: `tmp/mori-r56-c1-*`
  after a single run).
  (`.ufo/waves/round-56/count-c1.py:126`.)

- **LOW — the counter's own selftest asserts almost nothing.**
  `count-c1.py:169-172` checks only `len(EXPECT_FIX) == 9` and a string
  prefix, then prints `C1_COUNTER_SELFTEST pass=1 fail=0`; none of the
  counter's arms are exercised.
  (`.ufo/waves/round-56/count-c1.py:169-172`.)

- **LOW — the live receipt drifts with the log.** `evidence/driver-liveness-
  live.txt` (`log.lines` 1728, lane `kake` `completes` 50) does not equal a
  fresh read of the same live log (1729, `completes` 51), because the log
  gained one `complete` between 10:18 and 10:56. Everything else matches
  exactly. The receipt is a point-in-time snapshot and should not be read as
  an invariant.
  (`.ufo/waves/round-56/evidence/driver-liveness-live.txt`.)

- **LOW — the selftest requires a writable `TMPDIR`.** `t_empty_log`
  materialises its empty log under `TMPDIR`; with a read-only `TMPDIR` the
  case raises and the selftest reports `pass=12 fail=1
  failed=t_empty_log:EXC:[Errno 13] Permission denied`, exit 1. Fail-closed
  and correct, but the precondition is undocumented in the tool's usage
  text. (`tools/mori-driver-liveness.py:350-360`.)
