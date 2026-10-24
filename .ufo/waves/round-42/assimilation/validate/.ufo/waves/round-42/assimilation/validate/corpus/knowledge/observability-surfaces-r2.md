# Fleet & host observability surfaces — round 2 (one note per surface family)

source: `tools/mori-census.sh` (`census-r1`, sha256
`e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2`); surfaces declared at
`tools/mori-census.sh:10-17`, probes at `:182` (watchdog), `:247` (waves), `:311`
(journal), `:372` (cgroup), `:432` (disk), `:497` (silence), `:546` (tmux), dispatched
in `run_census` `:568-574`.
verified-at: 2026-10-15T15:27:57Z live census (receipt below) + `--selftest`
`PASS (14 cases, 14 passed, 0 failed)` exit 0 in the same window.
recheck: `bash tools/mori-census.sh` (live, writes nothing; exit 0 CLEAN | 1 DRIFT | 2
setup) · `bash tools/mori-census.sh --selftest` (hermetic, `/tmp` only).
scope: detection and report only (`PROVINCE.md:16-18`); nothing here remediates.
driver-citation scope: `mori-silence-cases.sh` line refs in the silence sections name the
pre-wave candidate `61db3df3`; shipped is `505a7504` (fixture report-path block now `:576-624`,
case bodies near `:650-657`). Case ids unchanged.

Seven surfaces — not six. Round 1's consolidated note documented six
(`corpus/knowledge/observability-census-r1.md:10-17`) and `corpus/README.md:7` says
"the six census surfaces", but the executed set is seven (`:568-574`, header `:10-17`).
The seventh, `tmux`, is landed in this note; the round-1 files are the parent's to
correct.

## Receipt pointers (all read-only)

| Receipt | Where | What it shows |
|---|---|---|
| r2 live watch receipt | §"r2 live receipt" below (ts 2026-10-15T15:27:57Z) | all 7 surface rows, 23 findings, exit 1 |
| r1 consolidated receipt + 7 errata | `corpus/knowledge/observability-census-r1.md:19-41` (receipt), `:63-221` (errata) | first dated receipt; scope corrections this note relies on |
| r1 pre-cutover baseline | `corpus/evidence/round-2/live-before.txt:7-30` | 17-lane roster, window 900, `silent=2` |
| scenario fixture receipt | `corpus/evidence/round-2/completed-before.txt` | r1 grader on a completed mission: `LANE_SILENT … head_epoch=0` (`:15`) — the named unavailable hole, live |
| mori-only admission check | `.ufo/round-2/interactive-cutover/checks/live-census.json` | same script bytes, roster=mori, window 900, exit 1 |
| selftest check | `.ufo/round-2/interactive-cutover/checks/selftest.json` (+ `summary.json`) | 14/14 PASS; `localAcceptance`: "proposed round-two behavior not admitted" |

## Status vocabulary

- `MORI_CENSUS: CLEAN|DRIFT (findings=N drift=M unavailable=U surfaces=7)`; exit
  0/1/2 (`:7-8`, `:580-587`).
- `unavailable` is a state, not a fault: it never flips the roll by itself
  (`emit_surface` `:146-153`; proved by selftest case "clean: CGROUP_UNAVAILABLE is
  not DRIFT" `:859-864`).
- Every `FINDING` carries `ts=` and `script_sha256=` (`:133-143`). The stable compare
  contract is the finding ids/severities/subjects; drop `ts=`, `age_s` and `current=`
  before diffing two runs (r1 note `:160-164`).
- All numbers below are mutable live observations pinned to one clock; the gate is
  the receipt, not a baseline.

## r2 live receipt (verbatim, `bash tools/mori-census.sh`, exit 1)

```
mori-census census-r1 — ts=2026-10-15T15:27:57Z — mode=live — read-only
SURFACE watchdog: drift (cmd=pgrep -af shokunin-watchdog; stat /home/vgpnk/Projects/shokunin/.ufo/watchdog.log; ls /home/vgpnk/Projects/shokunin/.ufo/state; pids=0; log=ok; age_s=37770; stale_threshold_s=900; state_rounds=21; ts=2026-10-15T15:27:57Z)
SURFACE waves: drift (cmd=find /home/vgpnk/Projects/shokunin/.ufo/waves -maxdepth 1 -mindepth 1 -type d; total=37 settled=13 unsettled=11 aged_unsettled=11 empty=13 threshold_s=7200; ts=2026-10-15T15:27:57Z)
SURFACE journal: drift (cmd=journalctl --user -b --no-pager; oom_kill=1 kill_signal=0 segfault=718 unit_failure=63 rc=0; ts=2026-10-15T15:27:57Z)
SURFACE cgroup: ok (cmd=cat /sys/fs/cgroup/user.slice/user-1000.slice/memory.events; cat /sys/fs/cgroup/user.slice/user-1000.slice/memory.current; oom_kill=1 oom=0 high=0 max=0 current=20467998720; ts=2026-10-15T15:27:57Z)
SURFACE disk: ok (cmd=df -P; targets=/home/vgpnk/Projects/shokunin /tmp; warn_pct=85 crit_pct=95; ts=2026-10-15T15:27:57Z)
SURFACE silence: drift (cmd=git -C <repo> log -1 --format=%ct; find <repo> -newermt @window; silent=6 progressing=3 progressing_weak=0 skipped=0 window_s=7200; ts=2026-10-15T15:27:57Z)
SURFACE tmux: ok (cmd=tmux ls; sessions=1; ts=2026-10-15T15:27:57Z)
FINDING WATCHDOG_STALE severity=warn obs=watchdog.log mtime_age_s=37770 threshold_s=900 path=/home/vgpnk/Projects/shokunin/.ufo/watchdog.log ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING WATCHDOG_ABSENT severity=warn obs=no shokunin-watchdog process matched by pgrep -af ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave=aggregator-r10 age_s=38243 threshold_s=7200 reg=0 disp=1 run=0 settle=0 ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave=aggregator-r10-resume age_s=37514 threshold_s=7200 reg=0 disp=1 run=0 settle=0 ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave=shokunin12h-20261014-p1-audit age_s=53420 threshold_s=7200 reg=0 disp=0 run=1 settle=0 ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave=shokunin12h-20261014-p2-kumitate age_s=53100 threshold_s=7200 reg=0 disp=0 run=1 settle=0 ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave=shokunin12h-20261014-p3-kengaku age_s=54681 threshold_s=7200 reg=0 disp=0 run=1 settle=0 ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave=shokunin12h-20261014-p4-mori-r1 age_s=52315 threshold_s=7200 reg=0 disp=0 run=1 settle=0 ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave=shokunin12h-20261014-p5-chousa-r1 age_s=51402 threshold_s=7200 reg=0 disp=0 run=1 settle=0 ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave=shokunin-train-20261013 age_s=149004 threshold_s=7200 reg=1 disp=1 run=0 settle=0 ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave=shokunin-train-20261013-w2 age_s=143225 threshold_s=7200 reg=1 disp=1 run=0 settle=0 ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave=shokunin-train-20261013-w3 age_s=138055 threshold_s=7200 reg=1 disp=1 run=0 settle=0 ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave=shokunin-train-20261013-w4 age_s=135193 threshold_s=7200 reg=1 disp=1 run=0 settle=0 ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING OOM_KILL_JOURNAL severity=crit obs=class=oom_kill count=1 boot=current scope=user ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING SEGFAULT_JOURNAL severity=info obs=class=segfault count=718 boot=current scope=user ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING UNIT_FAILURE_OUT_OF_SCOPE severity=info obs=class=unit_failure count=63 note=non-fleet units (desktop/OS) — tsukuroi owns these ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING CGROUP_OOM_KILL_CUMULATIVE severity=info obs=parent_slice_oom_kill=1 service_scope_oom_kill=0 note=cumulative boot counter; attribute the event before treating it as fleet evidence ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING LANE_SILENT severity=warn obs=lane=kasegi head_epoch=1792041688 newest_epoch=1792043037 window_s=7200 ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING LANE_SILENT severity=warn obs=lane=kake head_epoch=1792041665 newest_epoch=1792043037 window_s=7200 ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING LANE_SILENT severity=warn obs=lane=kumitate head_epoch=1792041397 newest_epoch=1792043037 window_s=7200 ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING LANE_SILENT severity=warn obs=lane=kotoba head_epoch=1792041275 newest_epoch=1792043037 window_s=7200 ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING LANE_SILENT severity=warn obs=lane=kagi head_epoch=1792041744 newest_epoch=1792043037 window_s=7200 ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING LANE_SILENT severity=warn obs=lane=kama head_epoch=1792041384 newest_epoch=1792043037 window_s=7200 ts=2026-10-15T15:27:57Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
MORI_CENSUS: DRIFT (findings=23 drift=20 unavailable=0 surfaces=7)
```

Same-day selftest receipt: `MORI_CENSUS_SELFTEST: PASS (14 cases, 14 passed, 0
failed)`, exit 0 (matches `.ufo/round-2/interactive-cutover/checks/selftest.json`).

## 1. watchdog — driver liveness

**Measures.** `pgrep -af shokunin-watchdog` filtered to lines containing
`shokunin-watchdog` and not containing the literal `pgrep` (`:188-194`); the age of
`.ufo/watchdog.log` mtime against `MORI_WATCHDOG_STALE_S` (default 900 = two driver
ticks, `:86`, `:211-215`); a count of `.ufo/state/*.round` files (`:218-221`).
Findings: `WATCHDOG_STALE` warn (`:214`), `WATCHDOG_ABSENT` warn (`:224`),
`WATCHDOG_LOG_UNAVAILABLE` info (`:205`, `:208`), `WATCHDOG_PROBE_UNAVAILABLE` info
when pgrep is missing (`:197`). Surface state is drift if `pids=0` or log stale
(`:227-232`).

**Status (r2 receipt).** drift — `pids=0; log=ok; age_s=37770; state_rounds=21`;
findings `WATCHDOG_STALE` + `WATCHDOG_ABSENT`. This is a window observation, not a
permanent property: the same probe read `pids=19; age_s=171` at 04:53Z
(`corpus/evidence/round-2/live-before.txt:8`). R1's audit concluded the Sep-28 stop
was a deliberate `fleet-wrap`, not an undetected crash (r1 note `:80-85`) — the gate
observed correctly and still cannot say which.

**Gaps.** Deliberate halt vs death is not distinguishable by the probe (no stop/fleet-
wrap marker; learned by hand in r1, `:80-85`). `state_rounds` counts files, never
values (`:220`), so a frozen round counter is invisible. Match precision is
unmeasured-in-production but demonstrated under control: any argv containing the
string — e.g. an editor opening `scripts/shokunin-watchdog.sh` — counts, because the
filter only drops lines containing `pgrep` (measured below). In the pgrep-missing arm
the code dead-ends: `tools/mori-census.sh:198-200` emits, then `return 0`s before the
log checks, leaving `emit_finding WATCHDOG_LOG_UNAVAILABLE` unreachable and the
comment "still try log" false (r1 `:176-182` already names the arm latent; the selftest
never removes the pgrep stub, `:706-709`). Selftest proves absent and stale arms
(`:772-789`) but not the probe-unavailable arm.

**r7 update (2026-10-15) — the `state_rounds` count-only clause: closed.** At census
`c7c3569b…` (`VERSION=census-r4`, 2004 lines) the walk reads every `.ufo/state/*.round`
value, the row adds `state_rounds_max= state_lag= state_ahead= state_cmp=
state_val_unreadable=` (`tools/mori-census.sh:445`), and each value is compared with the
lane's last `launch <lane> round=N` ledger line — below → `WATCHDOG_STATE_LAG` info
(`:421`), above → `WATCHDOG_STATE_AHEAD` info (`:424`), neither flipping the roll. Live
19:54:10Z row: `state_rounds=21 state_rounds_max=18 state_lag=0 state_ahead=0
state_cmp=21 state_val_unreadable=0`; four selftest cases (`:1951`, `:1959`, `:1967`,
`:1973`; receipt `corpus/evidence/surfaces-r7-20261015T1948Z-staterounds.log`). The
halt-vs-death, match-precision and pgrep-missing-arm clauses above are
outside the r7 move and remain as written. Pointer: `corpus/knowledge/surfaces-r7.md:159-189`
(§4).

Controlled false-positive demonstration (not fleet state): with a synthetic
`bash -c 'sleep 9; echo shokunin-watchdog >/dev/null'` alive,

```
SURFACE watchdog: drift (… pids=1; log=ok; age_s=37891; …; ts=2026-10-15T15:29:58Z)
FINDING WATCHDOG_STALE severity=warn … (no WATCHDOG_ABSENT)
```

versus `pids=0` + `WATCHDOG_ABSENT` at 15:27:57Z — the synthetic non-daemon suppressed
the absence finding.

## 2. waves — settlement and age

**Measures.** Directories under `.ufo/waves` (`:258-261`; `round-*` and dot dirs
excluded). Settlement is a typed token: `results.json` | `closeout.json` |
`mission-result.json` | `closeout.md`, or a registry/dispatch/run/spec declaring
`"closed": true` / `"settled": true` / `"status": "closed"` (`:272-281`). Age = NOW −
newest file mtime in the dir (`:283-285`); unsettled with age >
`MORI_WAVE_UNSETTLED_S` (default 7200, `:87`) fires `WAVE_UNSETTLED_AGE` warn
(`:291-295`). Unsettled is never called "failed" (`:246`).

**Status (r2 receipt).** drift — `total=37 settled=13 unsettled=11 aged_unsettled=11
empty=13`; 11 `WAVE_UNSETTLED_AGE` findings (2 `aggregator-r10*` with `disp=1`, 5
`shokunin12h-20261014-*` with `run=1`, 4 `shokunin-train-20261013*` with `reg=1
disp=1`).

**Gaps.** The age clock is carried debt: `w1`–`w4` have registry+dispatch and no
closeout token while their lane reports landed elsewhere, so "age" is the wrong clock
for them and a reported `WAVE_UNSETTLED_AGE` may be surface silence rather than an
unsettled wave (r1 `:107-118`, the `WaveAgeMath` critique). Because age anchors on the
newest mtime (`:283-285`), any writer touching the directory resets it — an
actively-written but stuck wave never ages. Empty wave dirs (13 here) are counted but
neither classified nor explained (`:296-298`). Selftest proves aged-unsettled vs
young-unsettled (`:791-814`) but no fixture drives the typed-token branches
(`closeout.md`, `"closed": true`), so the settlement form fixed in r1 `:107-114` is
unproved by the hermetic suite.

## 3. journal — kill/OOM/segfault/unit classes

**Measures.** `journalctl --user -b --no-pager` (`:312`, `:322`); rc > 1 →
unavailable (`:326-329`). OOM text class `Out of memory|oom-kill|oom_reaper|Killed
process` (`:331`) → `OOM_KILL_JOURNAL` crit (`:350-353`); kill-signal class
`status=9/KILL|Failed with result .signal|SIGKILL` (`:332`) → `KILL_SIGNAL_JOURNAL`
warn (`:354-357`); segfault text (`:338`) plus a live-host-only JSON
`COREDUMP_SIGNAL=11` additional count (`:339-343`) → `SEGFAULT_JOURNAL` info
(`:358-360`); unit failures (`:347-348`) → `UNIT_FAILURE_JOURNAL` info only for units
whose name matches `shokunin|ufo-sighting|tmux-spawn|the-tick|fleet`, everything else
`UNIT_FAILURE_OUT_OF_SCOPE` info (`:361-366`).

**Status (r2 receipt).** drift — `oom_kill=1` (crit `OOM_KILL_JOURNAL`),
`kill_signal=0`, `segfault=718` (info), `unit_failure=63` all out-of-scope (0 fleet
units; info), rc=0.

**Gaps.** Scope is the user journal only: system-journal segfaults are invisible
(measured 626 system vs 0 user in text form, r1 `:63-78`; unblock `SEGFAULT_SYSTEM`
named at `corpus/README.md:16-18`). The OOM class is a cumulative boot-scope text
count with no age or process identity — it read `count=1` in every receipt measured
today (r1 `:37`; live-before `:10`; `checks/live-census.json`; this receipt), matching
r1's attribution of the boot's single event to a 2026-10-13 desktop terminal python3
(r1 `:132-146`), yet it re-fires crit until the boot ends. The fleet-unit allowance is
a name-substring list (`:344-348`): a fleet unit whose name lacks those tokens is
classified out of scope (0 fleet / 63 out-of-scope in this receipt). The coredump
filter must stay signal-specific — all-core-dump entries measured 1051 vs 656 for
signal 11, and signal-5 SIGTRAP lines share a MESSAGE_ID (r1 `:186-199`). Threat-model
carry-overs: xtrace stays disabled because journal text can carry token-shaped lines
(`:52-56`; r1 `:203-210`); the published `cmd=` re-run prints `MESSAGE` by design;
live-mode `MORI_*_BIN` overrides are accepted and a live-mode refusal is the named
unblock (r1 `:216-219`); a future probe must not adopt `/proc/<pid>/environ`
(r1 `:220-221`). The JSON segfault path is live-only (`MORI_FIXTURE` disables it, `:339`), so
the hermetic suite never exercises it.

## 4. cgroup — user-slice memory

**Measures.** `memory.events` fields `oom_kill`/`oom`/`high`/`max` (`:382`,
`:405-407`) and the first line of `memory.current`, refused unless the resolved path
is under `/sys/fs/cgroup` (`:409-417`). Local discriminator preferred:
`memory.events.local`, else `user@<uid>.service/memory.events` (`:397-404`).
`CGROUP_OOM_KILL` crit only on the local/service counter > 0 (`:421-423`); the parent
slice's cumulative counter > 0 becomes `CGROUP_OOM_KILL_CUMULATIVE` info (`:424-426`);
unreadable parent events → surface unavailable + `CGROUP_UNAVAILABLE` info (`:376-379`).

**Status (r2 receipt).** ok — `oom_kill=1 oom=0 high=0 max=0 current=20467998720`;
finding `CGROUP_OOM_KILL_CUMULATIVE` info (`parent_slice_oom_kill=1
service_scope_oom_kill=0`). The `oom_kill=1` in the surface row is the *parent
cumulative* counter (`:382`, `:418`, `:428`), not a local kill.

**Gaps.** The row prints the parent counter under the bare name `oom_kill=`, with the
local/service reading visible only inside finding text — the exact
propagation trap r1 `:88-100` and `:132-140` had to correct at finding level. If both
`.events.local` and the session-service file are unreadable, no `unavailable` is
emitted and the row is unchanged (`:399-404`, `:421-428`): a genuine service-scope
kill degrades to the info cumulative finding at best, and the degraded read is not
disclosed. Memory pressure is owned (`PROVINCE.md:9-10`) but ungraded: `high`, `max`,
`oom`, `current` are printed only; no threshold exists and none is measured here
(unmeasured — no number is proposed). Selftest proves crit-on-counter (`:822-825`)
and unavailable-not-drift (`:859-864`); it does not drive parent>0/service=0, so the
cumulative-info branch and the local-vs-service discrimination are unproved by
fixture.

**r7 update (2026-10-15) — the memory-pressure clause: closed with labeled-local
numbers.** At census `c7c3569b…` the cgroup probe reads `memory.pressure` (PSI) and
grades `some avg10` ≥ `MORI_MEM_PSI_WARN_AVG10` (default 10, `threshold_label=local`) →
`MEM_PRESSURE_HIGH` warn (`tools/mori-census.sh:680`); fill pressure is `current/max`
against `MORI_MEM_FILL_WARN_PCT` (default 85) → `MEM_FILL_HIGH` warn (`:727`) when
`memory.max` is numeric, else the host `MemAvailable/MemTotal` floor against
`MORI_MEM_AVAIL_MIN_PCT` (default 10) → `MEM_AVAIL_LOW` warn (`:717`) with the scope
named on the row (`mem_fill_scope=`). Live 19:54:10Z row: `local_oom_kill=0
psi_some_avg10=0.00 psi_full_avg10=0.00 psi_source=ok psi_warn_avg10=10
mem_fill_pct=unavailable mem_fill_scope=host-ram host_mem_avail_pct=69` (receipt
`corpus/evidence/surfaces-r7-20261015T1948Z-memory.log`); this host's `memory.max` is
`max`, so only the host-ram arm is live-observable. Five selftest cases (`:1888`,
`:1895`, `:1903`, `:1910`, `:1917`); all three r7 memory findings are `warn` and do
flip the roll — the numbers are local placeholders, deliberately not derived from a
measurement of this host (`surfaces-r7.md:110-118`). The same row also closes the
defect-3 disclosure with `local_oom_kill=` (`surfaces-r7.md:88-90`). Pointer:
`corpus/knowledge/surfaces-r7.md:72-118` (§2).

## 5. disk — runway

**Measures.** `df -P` on each path in `MORI_DISK_TARGETS` (default `$ROOT /tmp`, `:85`);
column 5 percent parsed (`:458-467`); `DISK_CRITICAL` crit at ≥95%, `DISK_LOW` warn at
≥85% (`:468-474`); absent target / df failure / parse failure → `DISK_UNAVAILABLE`
info (`:443-449`, `:464-466`); no target present → surface unavailable (`:477-479`).

**Status (r2 receipt).** ok — `targets=/home/vgpnk/Projects/shokunin /tmp;
warn_pct=85 crit_pct=95`; no findings.

**Gaps.** 85/95 are explicitly PROPOSALS, not measurements: no write-rate evidence
exists, and the fleet's own reported disk failures were EDQUOT quota events that a
capacity-% probe cannot see (`:88-94`) — do not install a "better" number
without a measured write rate. The scratch root is owned (`PROVINCE.md:9`) but not in
the defaults, and `/scratch/tmp` re-measured absent on this host (`ls -d /scratch/tmp`
→ `No such file or directory`, rc 2, 2026-10-15T15:29Z), so `unavailable=0` does not
classify it; coverage exists only when an operator pins `MORI_DISK_TARGETS` (r1
`:182-184`). Do not OR a byte floor against `df -P`'s 1024-block Available column
(`:91-92`). Selftest proves crit vs under-warn (`:827-835`); the target-absent /
df-failed arms have no case.

**r7 update (2026-10-15) — the no-write-rate clause: a since-boot average is now
measured; the instantaneous rate is a bounded deferral.** At census `c7c3569b…` the
disk probe maps each `df` source to its device and reports `io_basis=since-boot
io_avg_since_boot=<dev>:<rate>Bps/<up_s>s` from `/proc/diskstats` sectors-written
(`tools/mori-census.sh:764-787`, row `:866`), with every unmeasurable target named in
`io_avg_unavailable=` (e.g. `tmpfs:not-a-block-device`) and `DISK_IO_UNMEASURED` info
(`:860`) when nothing is measurable. Live 19:54:10Z row:
`io_avg_since_boot=dm-0:9547707Bps/11784s`. This is the "measured write rate" the
clause above demanded — and no threshold moved: `warn_pct=85 crit_pct=95` unchanged.
Not implemented, as an explicit bounded deferral: the **instantaneous** two-sample
rate; the precondition to lift it — *measure the wall-time a second sample adds and
record it in the round note* (impl header `tools/mori-census.sh:48-52`) — is now met
as a datum: the r7 diskrate receipt measures a 10 s two-sample pair on dm-0 (13984
sectors → 715980 Bps), whole-gate wall time 3436 ms, and tiny/zero idle-window deltas
(`corpus/evidence/surfaces-r7-20261015T1948Z-diskrate.log:16-18`), so the in-census
probe stays deferred on measured grounds (`surfaces-r7.md:140-151`). Three selftest
cases (`:1927`, `:1933`, `:1940`); the average is not fleet-attributable and cannot
detect a burst (`surfaces-r7.md:153-157`). Pointer:
`corpus/knowledge/surfaces-r7.md:120-157` (§3).

## 6. silence — lane silent / progressing / progressing-weak

**Measures.** For each lane in `MORI_ROSTER_LANES` (default 9 lanes, `:96`; `protocol`
and `aggregator` map to the fleet root, `:490-495`): the HEAD commit epoch
(`git log -1 --format=%ct`, `:509-515`) and the newest non-`.git` file mtime (`:517`).
Window = NOW − `MORI_LANE_SILENCE_S` (default 7200, `:95`). In-window newest file →
`progressing`; in-window HEAD only → `progressing-weak`; neither → `LANE_SILENT` warn
(`:521-539`). A missing lane repo is counted `skipped` and produces no finding
(`:504-507`).

**Status (r2 receipt).** drift — `silent=6 progressing=3 progressing_weak=0 skipped=0
window_s=7200`; `LANE_SILENT` for kasegi, kake, kumitate, kotoba, kagi, kama. Numbers
are a pure function of `MORI_ROSTER_LANES` and `MORI_LANE_SILENCE_S` (17 lanes/window
900 read `silent=2` at 04:53Z, live-before `:13`), so any comparison must pin both.

**Gaps.** Rolling window, not launch-aware; no author check, so sibling commits count
as `progressing` and `progressing-weak` stays declared-deferred (`:524-534`;
`corpus/README.md:13-14`). No `unavailable` state: an unread HEAD (`head_t=0`) or
missing data can surface as `LANE_SILENT` (r1 `:182-184`), visible live in
`corpus/evidence/round-2/completed-before.txt:15` (`head_epoch=0`). `skipped` lanes
stay invisible except as a counter (`:504-507`; `corpus/knowledge/lane-silence-r2.md:181-184`).
The rule divergence against `PROTOCOL.md:155-168` is recorded at `LOG.md:73-80` /
`SKILL.md:111-129`. The launch-aware authorship rewrite is an uncommitted candidate
(`corpus/knowledge/lane-silence-r2.md`; driver `tools/mori-silence-cases.sh` sha256
`61db3df336fcd0facfaa9de6a5f0b5753047a450bbe85f685bc2d2a051b7011f` at 15:31Z), not
admitted as r2 grader behavior — and at that revision it exits 1 in fixture setup
before any case (no `MORI_SILENCE_CASES` line; SCORECARD.md `:68-69` records the same
pre-repair state). This note makes no claim about a repaired revision. Selftest proves
`LANE_SILENT` at a real threshold (`:837-857`); nothing proves authorship grading.

## 7. tmux — optional session list

**Measures.** `tmux ls` (`:547`); missing binary or rc ≠ 0 → unavailable, explicitly
not DRIFT (`:16-17`, `:548-556`); otherwise a count of non-empty output lines →
`SURFACE tmux: ok (sessions=N)` (`:558-560`).

**Status (r2 receipt).** ok — `sessions=1` (this wave's own server context; the
surface cannot say which sessions those are).

**Gaps.** The surface is count-only: no session names, no per-session freshness, no
fleet-relevance test (`:558-560`); `sessions=1` cannot distinguish a fleet session
from any other tmux server on a sibling socket. Correlation between sessions and
wave/lane activity is unmeasured and not claimed here. The unavailable arm (missing
tmux, rc ≠ 0) is declared in the header but never fixture-proved — no tmux case exists
among the selftest cases (`:762-872`). Round 1's note omitted this surface entirely
(r1 `:10-17`).

**r7 update (2026-10-15) — the relevance-test clause: closed; live proof still
absent.** At census `c7c3569b…` `probe_tmux` (`tools/mori-census.sh:1242-1302`) keeps
the `tmux ls` count and adds `tmux list-panes -a` pane current paths: a session is
`fleet` iff a pane sits at/under `$TMUX_SCOPE_ROOT` (default `$ROOT`, `:156`), else
`foreign` (`TMUX_FOREIGN_SESSION` info names it, `:1286`); the row carries
`sessions=N relevant=F foreign=X unclassified=U rule=pane_cwd_under_fleet_root`
(`:1301`), or `relevance=unavailable reason=…` with `TMUX_RELEVANCE_UNAVAILABLE` info
(`:1298`). The unavailable arm is fixture-proved now — three selftest cases (`:1861`,
`:1871`, `:1880`; previously none). Live proof is still absent: this host had no tmux
server at the r7 clocks (`tmux ls` rc 1 → the old `unavailable` row shape; receipt
`corpus/evidence/surfaces-r7-20261015T1948Z-tmux.log`), so relevance classification is
fixture-proved only, and per-session freshness remains unmeasured
(`surfaces-r7.md:65-70`). Pointer: `corpus/knowledge/surfaces-r7.md:38-70` (§1).

## Cross-surface constraints

- **Compare key.** Two runs differ by `ts=`, every `age_s`, and `current=`. Finding
  ids, severities and subjects are the contract; clock fields are not (r1 `:160-164`).
- **Unavailable is not unhealthy.** `unavailable` never flips the roll
  (`:146-153`); the selftest holds that invariant (`:859-864`).
- **Read-only guarantee.** Live mode writes nothing; `--selftest` writes only under
  its own `/tmp` dir and asserts the fixture tree hash is unchanged per case
  (`:19-20`, `:635-640`). The driver contract test for this lives in the silence-case
  candidate's `readonly-no-mutation` case (`tools/mori-silence-cases.sh:592-606`).
- **Threat-model carry-overs** (r1 `:200-221`): xtrace disabled; cgroup path resolved
  before the `/sys/fs/cgroup` prefix check; live-mode `MORI_*_BIN` overrides remain an
  accepted operator surface with a named unblock; `/proc/<pid>/environ` is forbidden
  for future probes even though readable on this host.

## Defects measured in this round (parent's files)

1. `tools/mori-census.sh:198-200` — unreachable `WATCHDOG_LOG_UNAVAILABLE` emission
   after `return 0` plus a false "still try log" comment; the log is not assessed in
   the pgrep-missing arm.
2. `tools/mori-census.sh:190-194` — measured false positive: a synthetic
   non-watchdog argv was counted as `pids=1` and suppressed `WATCHDOG_ABSENT`
   (15:29:58Z receipt above). Any process whose argv contains the literal string
   counts.
3. `tools/mori-census.sh:399-404` + `:421-428` — local/service cgroup counter
   unavailability is invisible when the parent file is readable; the row prints the
   parent cumulative counter under the bare `oom_kill=`.
4. `tools/mori-census.sh:220` — `state_rounds` is a file count; round values are never
   read.
5. Coverage framing: `corpus/knowledge/observability-census-r1.md:10-17` and
   `corpus/README.md:7` say six surfaces; the executed set is seven (`:568-574`).
   Fixed by this note; the two round-1 files remain the parent's to update.
6. `tools/mori-silence-cases.sh:188-217` (`gc`) — shell grouping `A || B && C` parses
   as `(A || B) && C`. The first commit `--allow-empty -am` (`:201`) succeeds as an
   empty commit and never stages the new file, so the `git add` fallback (`:208`) is
   skipped, and the trailing plain `git commit` (`:209-215`) then runs on an
   untracked-only tree and fails — exactly the observed
   `nothing added to commit but untracked files present`, exit 1, before any case.
   Line `:214` also carries `-c core.autcrlf=false` (typo for `core.autocrlf`; `:200`
   is correct), so the fallback would not pin autocrlf either. Reported, not patched
   here (driver seat owns it).

## What this note does not claim

No remediation, no kill/restart, no host config change, no fabricated numbers. Every
status above is the 15:27:57Z receipt or a cited prior receipt; every gap is either
code-cited, receipt-cited, or explicitly marked unmeasured. The seven surface rows are
current as of one mutable observation and will drift with the host.