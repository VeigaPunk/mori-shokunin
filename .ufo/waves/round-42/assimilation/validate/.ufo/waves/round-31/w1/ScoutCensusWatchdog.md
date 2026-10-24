# ScoutCensusWatchdog — how the census and the fleet decide the watchdog is alive

Seat: `MoriR31.ScoutCensusWatchdog`. Scope: read-only map of `probe_watchdog` in the
lane census, the fleet launcher, the audit's D05/D06, and the driver actually running
today. No fleet script, unit, harness or MCP file was edited; nothing was installed;
no process was started beyond short-lived local fixtures and none survives.
Real pids are written `<pid>`.

## 0. Answer

The census asks one yes/no question: does `pgrep -af shokunin-watchdog` print at least
one line that also contains `shokunin-watchdog` and does not contain `pgrep`? If yes,
`pids>0` and the pid half is "ok"; if no, `WATCHDOG_ABSENT` (warn) and the watchdog
surface is `drift`. It never validates a returned pid. The launcher has **no pid
file**; its only kernel-backed singleton identity is an exclusive `flock` on
`.ufo/.watchdog.lock` (`scripts/shokunin-watchdog.sh:381-382`), which the census never
reads or tests. Today no daemon process and no lock file exist; the fleet is driven
in-session by `scripts/hyaku/inline.sh`, whose identity appears only in log text
(`driver=hyaku-inline`, `scripts/hyaku/inline.sh:103`). The pid criterion is therefore
structurally blind to the driver that is actually running the fleet.

## 1. The exact probe

- Function: `probe_watchdog()` at `tools/mori-census.sh:704-853`.
- Inputs: `WATCHDOG_LOG` default `$UFO/watchdog.log` (`:297`), `STATE_DIR` default
  `$UFO/state` (`:302`), `PGREP_BIN` default `pgrep` (`:315`),
  `WATCHDOG_STALE_S` default `900` (`:351`). `UFO` is the **fleet** root's `.ufo`
  (`:289-292`: a lane dir ending `-shokunin` derives ROOT from its parent), so the
  lane census reads `/home/vgpnk/Projects/shokunin/.ufo/...`.
- Disclosure string (`:706`): `cmd_bits="pgrep -af shokunin-watchdog; stat $WATCHDOG_LOG; ls $STATE_DIR"`.
- Availability gate (`:710`): `if have "$PGREP_BIN" || [ -x "$PGREP_BIN" ]`, where
  `have()` is `command -v` (`:559`).
- Actual call (`:711`): `cap "$PGREP_BIN" -af shokunin-watchdog`; `cap()` captures
  stdout+stderr and rc without tripping `set -e` (`:561-566`). Under bash the binary
  is procps-ng: `/usr/bin/pgrep --version` → `pgrep from procps-ng 4.0.7`, owned by
  `procps-ng 4.0.7-1`.
- Filters (`:713`): `pids=$(printf '%s\n' "$CAP_OUT" | grep -E 'shokunin-watchdog' | grep -vF 'pgrep' || true)`;
  count (`:715`): `pid_n=$(printf '%s\n' "$pids" | grep -c . || true)`.
  The first `grep` is a substring test, not a token test. The second drops every line
  containing the literal `pgrep` (the pattern is unanchored: `pgrep` matches inside
  any word).
- Alive := `pid_n > 0` (`:833-834`: `if [ "$pid_n" -eq 0 ] || [ "$stale" -eq 1 ]; then st=drift; fi`).
  No `kill -0`, no `/proc/<pid>` read, no environ tag, no exe path, no start time.

## 2. Verdict and emitted text

Output formats: findings are `FINDING <id> severity=<sev> obs=<text> ts=<utc> script_sha256=<sha>`
(`:424`); surfaces are `SURFACE <name>: <state> (<detail>)` (`:436`). Lines are buffered
and printed only at the end (`:2711-2712`), then `MORI_CENSUS: CLEAN|DRIFT ...`
(`:2714-2715`). Only `warn|crit` flips the roll (`:426-430`); `info` does not, but
`unavailable` surfaces increment `N_UNAVAIL` (`:437-439`).

| Observation | Emitted text / verdict | Source |
|---|---|---|
| `pgrep` absent / not executable | surface `watchdog: unavailable (cmd=...; pgrep=missing; ts=...)`; finding `WATCHDOG_PROBE_UNAVAILABLE severity=info obs=pgrep unavailable — daemon liveness UNKNOWN, not absent`; then `return 0`, so the log check is **never run** (the next finding, `:721`, is dead code) | `tools/mori-census.sh:718-721`; audit D05 `corpus/knowledge/audit-r11.md:200` |
| `pgrep` runs, zero surviving lines | `WATCHDOG_ABSENT severity=warn obs=no shokunin-watchdog process matched by pgrep -af`; surface `watchdog: drift (...; pids=0; log=...; age_s=...; stale_threshold_s=900; state_rounds=...; ts=...)`; roll DRIFT | `:829-831`, `:833-834`, `:852-853` |
| `pgrep` runs, ≥1 surviving line | `pids=N`; pid half "ok". Surface is `ok` only if the log is fresh; a stale log still yields `WATCHDOG_STALE severity=warn` and `drift` | `:736-737`, `:833-834`, `:852` |
| Log mtime age > 900 s | `WATCHDOG_STALE severity=warn obs=watchdog.log mtime_age_s=<age> threshold_s=900 path=<log>` | `:734-737` |
| Log absent / unreadable | `WATCHDOG_LOG_UNAVAILABLE severity=info` (`:727`, `:730`); drift only when `pids=0` too | `:829-831`, `:835-838` |
| `.round` value below last `launch <lane> round=N` in the ledger | `WATCHDOG_STATE_LAG severity=info` (`:818`), never flips the roll | `:660-670`, `:813-818` |
| `.round` value above ledger | `WATCHDOG_STATE_AHEAD severity=info` (`:821`) | `:820-821` |
| `.round` walk unreadable | `state_rounds=unavailable state_unreadable=1` in the detail | `:846-850` |

The strictest statement the probe supports is: "a process whose command line contains
`shokunin-watchdog` and not `pgrep` is visible in this pid namespace at this instant".

## 3. What a pid signal cannot establish (measured)

1. **D06 false positive, reproduced.** One `sleep` whose argv[0] was set to
   `shokunin-watchdog` (no daemon anywhere) measures, exactly as the probe measures
   it (`pgrep -af` captured first, then the two filters), `raw_lines=1
   filtered_count=1` with the surviving line `<pid> shokunin-watchdog 8`. A
   one-pipeline variant of the same fixture put its own `timeout` and `bash -c`
   wrapper lines into the raw snapshot (three raw lines for the one sleep), so
   wrapper argv inflates the count too; the probe's separate capture keeps its own
   filter processes out of the snapshot. `pids=1` for zero daemons; any editor or
   grep command that merely mentions the name counts the same way. Audit D06:
   `corpus/knowledge/audit-r11.md:201`.
2. **No identity check of a hit.** A recycled pid, a wrapper, a `less`/`nvim` argument,
   or this seat's own `grep -rn shokunin-watchdog` all satisfy `pid_n>0`. The fleet's
   own lane liveness is stricter (`scripts/shokunin-watchdog.sh:231-236`: `kill -0`
   plus `SHOKUNIN_LANE=<lane>` in `/proc/<pid>/environ`); the census applies no such
   test to the driver.
3. **The inline driver is invisible.** `scripts/hyaku/inline.sh:24` **sources**
   `scripts/shokunin-watchdog.sh`; sourcing does not put `shokunin-watchdog` in argv.
   The running command is `bash .../scripts/hyaku/inline.sh dispatch ...`. Driver
   identity exists only as log text: `log "launch ... driver=hyaku-inline attempt=$a"`
   (`inline.sh:103`), and `probe_watchdog` never parses `driver=`.
4. **Log freshness is shared.** `log()` writes the same `$UFO/watchdog.log` for the
   daemon (`shokunin-watchdog.sh:66,221,406`) and the inline driver (sourced `log`,
   `inline.sh:103`). Under the daemon, a `tick=...` line lands every 450 s
   (`shokunin-watchdog.sh:406`, `TICK_SECONDS=450` at `shokunin.conf:11`), so the log
   cannot age past 900 s while the daemon lives. Inline writes only launch, complete
   and failure lines (`inline.sh:103,130,136`), no fixed cadence, so a long round ages
   the log: measured at `2026-10-22T20:44:24-03:00`,
   `age_s=1024 > 900` on a live fleet; at `20:47:43` it was `age_s=12` after a
   `complete kake round=35` line. log age alone is not daemon liveness.
5. **The state walk reads daemon-shaped state.** `.ufo/state/<lane>.round` is written
   only by the daemon's `launch_lane` (`shokunin-watchdog.sh:219-220`); the inline
   driver keeps claims elsewhere (`inline.sh:19,91-96`) and never updates `.round`.
   Replaying the census comparison over the fleet log and all 21 `*.round` files:
   `compared=21 lag=15 ahead=0`; e.g. `mori state=2` vs last `launch mori round=31`,
   `tsukuroi state=1` vs `round=31`. These are info-only, but they show the surface is
   still modelled on the daemon.
6. **Unknown pid is not "absent" only on the missing-pgrep path.** `pgrep` missing is
   graded `unavailable`/UNKNOWN (`:718-719`), which is correct; a *working* pgrep that
   matches nothing is graded `WATCHDOG_ABSENT`/drift even when the inline driver is
   alive. The two readings invert the epistemics: the broken probe is honest, the
   working probe is overconfident about the wrong process shape.

## 4. Stronger identity that exists (inventory, no changes proposed)

- **Daemon lock (kernel-backed, unused by the census).** `main()` opens
  `$UFO/.watchdog.lock` and takes `flock -n`; a second instance dies
  (`scripts/shokunin-watchdog.sh:379-382`). The lock is held across the whole run, so
  a non-blocking `flock` test would distinguish "holder exists" from "none" without
  trusting argv. The file is currently **absent** (`ls .ufo/.watchdog.lock` → no such
  file), consistent with no daemon run since the file was created/removed.
- **No pid file** for the driver anywhere in the fleet root (`find . -maxdepth 3 -name
  '*watchdog*.service'` → empty; `ls scripts/*watchdog*` → only
  `scripts/shokunin-watchdog.sh`).
- **Lane identity pattern (not the driver).** `.ufo/state/<lane>.mission` stores the
  lane process-group leader (`shokunin-watchdog.sh:219`) and `mission_live` verifies
  `SHOKUNIN_LANE=<lane>` in `/proc/<pid>/environ` (`:231-236`). 21 `.mission` files
  exist, all from the daemon era.
- **Inline driver state (durable intent, not liveness).** Claims dir with
  `owner=inline`, `round`, `attempt`, `dispatched` (`inline.sh:91-96`); event log via
  `ev()` (`inline.sh:29`). No lock and no pid.
- **No supervisor unit found.** `systemctl list-unit-files | grep -i shokunin` → rc 1
  (no match); `systemctl --user list-unit-files` → rc 1; `systemctl --user list-units --all`
  → rc 1. Documented manual launch: `SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin bash
  <canonical>/scripts/shokunin-watchdog.sh` (`LOG.md:657`). A grep of `scripts/` and
  `README.md` finds no launcher wrapper: the only script reference is the sourcing at
  `scripts/hyaku/inline.sh:24`, and `grep -n watchdog README*` prints no line. The
  launcher starts
  `#!/usr/bin/env bash` (`scripts/shokunin-watchdog.sh:1`) with `set -u` (`:33`) and
  does not exec itself into a lane: `launch_lane` only runs `exec setsid bash -c ...`
  in a child (`:215`), so a running daemon's argv is `bash .../scripts/shokunin-watchdog.sh`
  and would match `pgrep -af`.

## 5. Current state: the fleet is inline-driven, not daemon-driven

- Daemon process: absent. Census-filter replay `pids=0`; `ps -eo args= | grep -cF
  'scripts/shokunin-watchdog.sh'` → `0`. (Observed `2026-10-22T23:48-23:49Z`.)
- Singleton lock: absent (above).
- `watchdog.log` (64021 B, mtime `20:47:30-03:00`): 208 `driver=hyaku-inline` lines,
  3 `driver=hyaku` lines (the older slot variant, `2026-10-19T23:10:53-03:00`, log
  lines 403-405). Last lines: `20:27:52 launch mori round=31 pgid=<pid>
  driver=hyaku-inline attempt=1` (line 780) and `20:47:30 complete kake round=35;
  hyaku-inline attempt=1` (line 781). No launch line without a `driver=` field exists
  in the recent tail; the daemon's own launch shape (`shokunin-watchdog.sh:221`) would
  have none.
- Inline claim for this round: `owner=inline`, `round=31`, `attempt=1`,
  `dispatched=2026-10-22T20:27:51-03:00` (claim dir defined at `inline.sh:19,91-96`); claim
  dirs exist for 11 lanes. `events.log` tail: `inline complete lane=kake round=35
  attempt=1`, `inline closure-launch lane=kake round=35`.
- Therefore: **the fleet does not run the watchdog daemon today**; `scripts/hyaku/inline.sh`
  is the driver, matching `AGENTS.md:14` ("In-session orchestrator (current mode)") and
  `AGENTS.md:19` ("Never run the watchdog and `inline.sh` together"). [INFERENCE] The
  inline driver's own liveness is only evidenced by its fresh claim/event writes, not
  by any kernel-held identity.
- Consequence for the census: on the same host the probe emits `WATCHDOG_ABSENT`
  (warn → DRIFT) because no argv contains the script name, and `WATCHDOG_STATE_LAG`
  for 15/21 lanes because `.round` froze when the daemon stopped. Neither is a dead
  fleet; both are the daemon-shaped criterion meeting an inline-driven fleet.

## 6. C1-ready observation rows (source column is `path:line`, ids to be attached)

| Observation | Reading | Verdict | Sources |
|---|---|---|---|
| pgrep binary missing | liveness UNKNOWN, not absent | unavailable, census may still be CLEAN | `tools/mori-census.sh:718-720` |
| pgrep returns 0 filtered lines | no matching argv visible | absent (warn) → drift; blind to inline driver | `tools/mori-census.sh:713-715,829-831` |
| pgrep returns ≥1 line, log fresh | some argv mentions the name | alive/ok, no identity proof | `tools/mori-census.sh:833-834,852-853` |
| argv mention only (editor/wrapper) | false positive | alive/ok is wrong | audit `corpus/knowledge/audit-r11.md:201`; fixture §3.1 |
| log mtime > 900 s with pids>0 | daemon ticks would prevent this; inline does not tick | warn/drift despite live driver | `shokunin-watchdog.sh:406`; `mori-census.sh:734-737` |
| `.ufo/.watchdog.lock` held | kernel-backed singleton exists | stronger than argv (not probed today) | `shokunin-watchdog.sh:381-382` |
| no process, no lock, inline claims fresh | daemon down, inline driving | fleet alive [INFERENCE], daemon absent | §5; `inline.sh:91-96,103` |
| `.round` below ledger launch round | state frozen at daemon era | info lag, not liveness | `shokunin-watchdog.sh:219-220`; `mori-census.sh:818` |

## 7. Confidence and remaining unknowns

- High confidence: probe mechanics, emitted strings, daemon absence (three independent
  signals: pgrep, ps, lock), inline activity (claims + events + 208 log lines), and
  the state-lag replay (21 files, 15 lag).
- Medium: a `pgrep -af shokunin-watchdog` line naming `pgrep` itself was observed once
  next to my shell command (`<pid> pgrep -af shokunin-watchdog`); it did not reproduce
  with a unique token, so I do not claim pgrep self-lists. The census's
  `grep -vF pgrep` would remove it regardless. The harness's interactive shell also
  exposes a `pgrep` builtin reporting `0.2.0`; the census runs under bash and resolves
  `/usr/bin/pgrep` (procps-ng 4.0.7), observed.
- Unknown: no full census receipt. A live run hit my 115 s bound (`rc=124`) and printed
  nothing, because surface/finding lines are buffered until the end
  (`tools/mori-census.sh:2711-2712`). All verdict text above is from code plus probe
  arithmetic replayed by hand, not from a completed census run.
- Not checked: whether an operator starts the daemon by hand outside a unit (no unit
  exists; process/lock evidence settles "running today"). No fleet-script changes are
  proposed here.
