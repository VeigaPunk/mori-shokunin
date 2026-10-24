# ExeSelftestTiming

Axes: C1 selftest correctness and dispatch wall time versus the 1,800-second `mechanicalMs` budget.

## Results

Each requested selftest ran once and returned successfully (exit 0). The command output and shell `time` measurements were:

```text
TIMEFORMAT='WALL_SECONDS=%3R'; time python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --selftest
PASS predicate          predicate token changed -> only predicate failed
PASS head_pin           pin label renamed -> only head_pin failed
PASS tool_resolve       relative resolution removed -> only tool_resolve failed
PASS bounded_reads      git helper run timeout removed -> only bounded_reads failed
PASS timeout_scope      timeout value replaced with None -> only timeout_scope failed
PASS timeout_scope_shadow function-local None shadow inserted -> only timeout_scope failed
PASS drain_bind         communicate drains replaced by wait+read -> only drain_bind failed
PASS drain_bind_decoy   decoy used communicate beside a wait+read drain -> only drain_bind failed
PASS timeout_state      budget flag ignored -> only timeout_state failed
PASS scratch            scratch parent moved off-lane -> only scratch failed
PASS selftest_conjunct  communicate timeout keyword stripped -> only selftest_conjunct failed
CONFORM_SELFTEST pass=11 fail=0
real 0m57.383s
user 1m56.344s
sys 0m51.804s
```

```text
TIMEFORMAT='WALL_SECONDS=%3R'; time python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-sources-appendonly.py --selftest
MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0
real 0m0.939s
user 0m2.441s
sys 0m1.555s
```

Both wall times are inside 1,800 seconds. Conform took 57.383 seconds (1,742.617 seconds below budget); the gate took 0.939 seconds (1,799.061 seconds below budget). Measured lane-timeout risk is low; dispatch/queue overhead was not measured.

## Scored-tip byte provenance and caveat

The read-only command `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD` returned `ede486b7a09afbacfb380d5871c46a8051a6dc2e`, not scored tip `265a955cc67be4eae97d2dc5a9338a25f31eb29b`. I verified the selftest source and conform inputs against that scored commit using `git show <scored-tip>:<path> | sha256sum`; their hashes match the working-copy `sha256sum` values:

- `.ufo/waves/round-40/conform.py`: `5025b9664632d01063c11b4f5dadd4f9a063db66d73315d7ed25db8d90b83aaf`
- `tools/mori-sources-appendonly.py`: `bde5a9a34c7eb3bcbee39d669b8d187caeb51807ad1bdcd85a05c1bcd06777ec`
- `.ufo/waves/round-40/count-c8.py`: `4e4d50eb1e96d947f0e9d2ab25a13b2b8c33963f216f3be43060a3348702f6da`
- `.ufo/waves/round-39/contract.md`: `fc36841bff00e46bf3d2ba662c9e4e13e36577da1d1f2fec41d0bea91f8ebcd3`
- `.ufo/waves/round-39/fixtures/witness-summary-only-live.txt`: `8ac9e82bae369a2e41f4a4377016c3e82d58c8c6de484722f1d85b0bbf7cb4af`
- `.ufo/waves/round-39/fixtures/hang-after-flush.py`: `647410536bcc6b9ead5456af96056617b78b7945aaacc2c5d3635b1b017a87ca`

Thus the instrument and conform data bytes tested match the scored-tip blobs. The checkout itself was not at the scored revision: conform's internal `head_pin` selftest compared against the checked-out `HEAD` (`ede486…`), rather than a repository whose `HEAD` was `265a955…`. This is the scope caveat on the scored-tip measurement.

Timing note: the initial `/usr/bin/time -f 'WALL_SECONDS=%e' ...` attempts failed before Python ran because `/usr/bin/time` was unavailable (exit 127). The two successful one-run measurements above used the shell `time` keyword.