# The successor measurement's run() accepts cwd

source: S348 — https://docs.python.org/3/library/subprocess.html#subprocess.run — docs, tier A, Python subprocess.run signature, opened 2026-10-24
verified-at: 2026-10-24
recheck: 90d

The frozen round-42 counter's `run()` takes `argv, timeout` and not `cwd`.
Its no-harm check calls `run(..., cwd=clone)` and raises
`TypeError: run() got an unexpected keyword argument 'cwd'` before any
`C1=` line. That counter is not amended.

`subprocess.run`'s documented signature includes `cwd=None`. The round-43
successor `.ufo/waves/round-43/count-c1s.py` passes `cwd` through to
`subprocess.run` and scores `C1S=met` only when that call completes, the
append-only gate selftest in the sandbox clone records `pass=22 fail=0`,
and the frozen counter at the same revision still crashes with no `C1=`
line. A revision that does not contain this counter byte-identical prints
`C1S=unmet`.

This does not restart a service, change a limit, or remediate a kill.
