# Driver-liveness reading of .ufo/watchdog.log (round 56)

source: S544 (the driver scripts that write the log — grammar authority)
verified-at: 2026-10-27 (extract `corpus/evidence/sources-r56/watchdog-log-grammar.txt`, sha256 `38ba3e6b…`)
recheck: on-release
coverage-map: FR5 advance — the launch/complete liveness source named open ground in `corpus/README.md` (FR5 boundary, round-33 note)

## Why this probe exists

Under the hyaku inline driver no `shokunin-watchdog` daemon runs, so the
census watchdog surface fires `WATCHDOG_ABSENT` every round. FR5 names the
open coverage ground: reading the driver's own `launch`/`complete` lines in
`.ufo/watchdog.log` as a second liveness source. `tools/mori-driver-liveness.py`
moves that ground to Core, bounded: it reads the log and reports per-lane
driver-activity **facts** — launches, completes, deads, launch-fails, wraps,
last-launch age, `in_flight` (last event is a launch), `unclosed` (launches
with no same-round close) — and log shape (line count, malformed count,
`other_lines` for ts-first driver prose such as `steer`/`watchdog tick`).
Every field is a shape fact; the probe makes no health verdict and never
remediates.

## The frozen grammar (S544)

Two writers share one log; the probe grammar is frozen from the writer source
and every variant observed in the committed live log 2026-09-28..2026-10-27:

* `launch` — `pgid=` with optional `driver=… attempt=…`, optional `slot=…`,
  optional `mission=`; or bare `pid=`; or `mission=` alone; or `runId=`; or no
  rest at all (S544 `inline.sh:149`, `shokunin-watchdog.sh:266`, plus the
  steered/ufo-fsd variants present in the log).
* `complete` — `; hyaku-inline attempt=a` (S544 `inline.sh:176`),
  `; advancing to round=n+1` (S544 `shokunin-watchdog.sh:405`), or
  `; respawning` (legacy daemon respawn).
* `lane-dead-no-report` — `; retry same round` with a free optional parenthesis
  (S544 `inline.sh:182`, `shokunin-watchdog.sh:448`); the inner text varies
  (`hyaku-inline attempt=a: reason`, `hyaku: headless attempt ended …`) and is
  never parsed beyond the wrapper.
* `launch-fail` — ` :: reason` (S544 `shokunin-watchdog.sh:241-249`).
* `wrap` — ` landed` or ` complete`, optional `; NOT respawning (fleet-wrap)`
  (S544 `shokunin-watchdog.sh:398`); a wrap closes the round like a complete.
* A ts-first line matching none of these is an `other_line` (driver prose),
  counted but never a lane event and never malformed; a line whose first token
  is not ISO-8601, or an event line with an unrecognized rest, is malformed —
  counted with capped examples, never silent.

## Measured on this host (2026-10-27)

`python3 tools/mori-driver-liveness.py` against the live fleet log:
`DRIVER_LIVENESS_OK`, 1728 lines, **0 malformed**, 121 other_lines, 23 lanes;
mori: 66 launches / 39 completes / 17 deads / in_flight / unclosed 10
(receipt `evidence/driver-liveness-live.txt`). The full receipt is committed;
re-running the command reproduces it modulo ages.

## Limits (named before data)

* `in_flight`/`unclosed` are pairing facts over log lines, not health verdicts;
  a lane with an unclosed launch is *in flight by the log*, not "stuck".
* The probe reads log lines and `*.round` entry *shapes* only; it never reads
  state values and never follows symlinks (the census owns value semantics).
* Log lines are driver-authored shape, not authenticated events; a rewritten
  log would rewrite the reading. This is the same trust level as the census
  log-freshness arm it complements.
* Aged launches measure from the log timestamp; clock moves between driver and
  probe shift `last_launch_age_s` without changing the event counts.
