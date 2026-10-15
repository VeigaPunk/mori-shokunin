# Fleet & host observability census — round 1 (live receipt)

source: `tools/mori-census.sh` (read-only) at `mori-shokunin/tools/mori-census.sh`
verified-at: 2026-10-15T00:35:18Z (live run, exit 1 DRIFT — a red census is a
finding, not a failure)
recheck: `bash tools/mori-census.sh` (live) · `bash tools/mori-census.sh --selftest` (14 cases)

## Surfaces

| Surface | What it reads | Read-only probe |
|---|---|---|
| watchdog | driver pid, `.ufo/watchdog.log` mtime, `.ufo/state/*.round` | `pgrep -af shokunin-watchdog`, `stat`, `ls` |
| waves | `.ufo/waves/*` settlement shape and age | `find` + file presence |
| journal | kill/OOM/segfault/unit-failure classes this boot | `journalctl --user -b` |
| cgroup | user-slice `memory.events` / `memory.current` | `cat` |
| disk | runway on the fleet root and `/tmp` | `df -P` |
| silence | lane silent / progressing / progressing-weak | `git log -1 --format=%ct`, `find -newermt` |

## Live receipt (verbatim)

```
mori-census census-r1 — ts=2026-10-15T00:35:31Z — mode=live — read-only
SURFACE watchdog: drift (cmd=pgrep -af shokunin-watchdog; stat /home/vgpnk/Projects/shokunin/.ufo/watchdog.log; ls /home/vgpnk/Projects/shokunin/.ufo/state; pids=0; log=ok; age_s=103843; stale_threshold_s=900; state_rounds=9; ts=2026-10-15T00:35:31Z)
SURFACE waves: drift (cmd=find /home/vgpnk/Projects/shokunin/.ufo/waves -maxdepth 1 -mindepth 1 -type d; total=33 settled=7 unsettled=10 aged_unsettled=5 empty=16 threshold_s=7200; ts=2026-10-15T00:35:31Z)
SURFACE journal: drift (cmd=journalctl --user -b --no-pager; oom_kill=1 kill_signal=0 segfault=0 unit_failure=2 rc=0; ts=2026-10-15T00:35:31Z)
SURFACE cgroup: drift (cmd=cat /sys/fs/cgroup/user.slice/user-1000.slice/memory.events; cat /sys/fs/cgroup/user.slice/user-1000.slice/memory.current; oom_kill=1 oom=0 high=0 max=0 current=24685088768; ts=2026-10-15T00:35:31Z)
SURFACE disk: ok (cmd=df -P; targets=/home/vgpnk/Projects/shokunin /tmp; warn_pct=85 crit_pct=95; ts=2026-10-15T00:35:31Z)
SURFACE silence: ok (cmd=git -C <repo> log -1 --format=%ct; find <repo> -newermt @window; silent=0 progressing=9 progressing_weak=0 skipped=0 window_s=7200; ts=2026-10-15T00:35:31Z)
SURFACE tmux: ok (cmd=tmux ls; sessions=1; ts=2026-10-15T00:35:31Z)
FINDING WATCHDOG_STALE severity=warn obs=watchdog.log mtime_age_s=103843 threshold_s=900 path=/home/vgpnk/Projects/shokunin/.ufo/watchdog.log
FINDING WATCHDOG_ABSENT severity=warn obs=no shokunin-watchdog process matched by pgrep -af
FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave=shokunin-train-20261013 age_s=95458 threshold_s=7200 reg=1 disp=1 run=0 settle=0
FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave=shokunin-train-20261013-w2 age_s=89679 threshold_s=7200 reg=1 disp=1 run=0 settle=0
FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave=shokunin-train-20261013-w3 age_s=84509 threshold_s=7200 reg=1 disp=1 run=0 settle=0
FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave=shokunin-train-20261013-w4 age_s=81647 threshold_s=7200 reg=1 disp=1 run=0 settle=0
FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave=shokunin-train-20261013-w5 age_s=70601 threshold_s=7200 reg=1 disp=1 run=0 settle=0
FINDING OOM_KILL_JOURNAL severity=crit obs=class=oom_kill count=1 boot=current scope=user
FINDING UNIT_FAILURE_JOURNAL severity=info obs=class=unit_failure count=2 boot=current scope=user
FINDING CGROUP_OOM_KILL severity=crit obs=oom_kill=1 oom=0 high=0 max=0 current=24685088768 path=/sys/fs/cgroup/user.slice/user-1000.slice/memory.events
MORI_CENSUS: DRIFT (findings=10 drift=9 unavailable=0 surfaces=7)
```

## What the census says right now (observation, not inference)

- **The fleet watchdog is not running and its log is ~29 h stale**
  (`WATCHDOG_ABSENT`, `WATCHDOG_STALE age_s=103830`). This is the exact class the
  operator described when demanding this lane: the fleet can stop without anyone
  noticing.
- **A real OOM kill occurred on this boot** (`OOM_KILL_JOURNAL count=1`,
  `CGROUP_OOM_KILL oom_kill=1`), with 2 unit failures. Recorded as fleet evidence;
  remediation is the operator's.
- **Five waves are unsettled past the window** (`WAVE_UNSETTLED_AGE`, oldest
  `age_s=95445` ≈ 26.5 h): dispatched, never settled, invisible until now.
- Disk and lane silence are clean; all nine rostered lanes show in-window activity.

## Boundary

Detection and report only: the gate writes nothing in live mode, restarts
nothing, and refuses dispatch (kumitate) and OS-package state (tsukuroi). Its
`--selftest` writes only under its own temp dir and asserts the fixture tree is
unchanged after every case.

## Erratum (appended 2026-10-15) — journal scope limit, and the watchdog's halt is old

**Scope limit, measured.** The `journal` probe reads `journalctl --user -b` only.
The independent `LiveReceipt` seat reported 588 segfault lines; re-measured here:

| Scope | `grep -ciE 'segfault|general protection fault'` |
|---|---|
| `journalctl --user -b` (this gate's scope) | **0** |
| `journalctl -b` (system journal) | **626** |

`coredumpctl list` → **1228** entries. So the gate is correct for its declared
scope and **blind to host-level segfaults**, which are fleet-relevant (a crashed
process can be a fleet process). Named coverage gap; unblock: add a system-journal
probe with its own finding id (`SEGFAULT_SYSTEM`), keeping the user scope as the
primary. 626 segfaults + 1228 core dumps on this boot is itself an operator-facing
observation that this round did not previously surface.

**The watchdog's halt is old, not fresh.** `WATCHDOG_ABSENT` + `WATCHDOG_STALE`
are correct as observations, but the cause is not a recent death: the log's last
lines are `2026-09-28T23:55:00-03:00 wrap kagi round=16 complete; NOT respawning
(fleet-wrap)` — the driver was deliberately halted on **2026-09-28** and no
`fleet-wrap` file exists now, so it simply has not been restarted. Recorded so the
finding is not read as an undetected crash.

## Erratum 2 (appended 2026-10-15) — two probe scopes corrected after cross-domain audit

**`CGROUP_OOM_KILL` was firing on a cumulative, non-fleet counter.** Cgroup v2
`memory.events` counters are monotonic across the boot. Measured: parent
`user-1000.slice` reads `oom_kill 1` while `user@1000.service` — the scope that
actually contains fleet processes — reads `0`, and the event was a desktop
terminal `python3` killed on **2026-10-13 23:44:30**
(`app-Hyprland-xdg-terminal-exec-dd9e67bd.scope: Failed with result 'oom-kill'`).
Firing `crit` on the parent counter forced a permanent false DRIFT on every run
and absorbed tsukuroi's OS triage into mori. The probe now fires `crit` only on
the session-service counter and reports the parent counter as
`CGROUP_OOM_KILL_CUMULATIVE` (info). **The round-1 receipt's headline "a real OOM
kill occurred on this boot" was wrong as characterized** — the kill was ~25 h old
and not a fleet process.

**`UNIT_FAILURE_JOURNAL` was scraping desktop units.** The unscoped grep matched
`pipewire-pulse.service: Failed with result 'core-dump'` — OS triage, tsukuroi's
domain. Fleet-relevant units now fire `UNIT_FAILURE_JOURNAL`; everything else is
`UNIT_FAILURE_OUT_OF_SCOPE` (info) with the owner named.

**Wave settlement is a typed token, not a filename.** `w5`–`w11` close out with
`closeout.md` and/or a registry carrying `"closed": true`, which a results-file
test cannot see; five settled train waves were aged into false
`WAVE_UNSETTLED_AGE`. The probe now accepts those tokens. **Still provisional:**
`w1`–`w4` have registry+dispatch and no closeout token while their lane reports
landed elsewhere, so "age" remains the wrong clock for them — the independent
`WaveAgeMath` critique is carried as debt, and a wave reported here as
`WAVE_UNSETTLED_AGE` may be surface silence rather than an unsettled wave.

## Finding → owner routing (appended 2026-10-15)

Two tiers, because a single-tier map deadlocks: `tsukuroi` and `kama` refuse to
act by their own provinces, so a finding routed to them for remediation stalls.
**Tier 1 (triage, read-only):** tsukuroi / kama / kumitate / mori each re-probe and
diagnose in their own domain. **Tier 2 (actuation):** `kumitate` for automated
orchestration actions, the **operator** for host mutations. Never collapse
everything onto the operator — that is the drowning trap. Payloads must be typed
(`pid`, `comm`, `cgroup`, `mount`, `use_pct`, `wave_dir`, `newest_file_age_s`) so
Tier 1 can diagnose without re-probing. An `WAVE_UNSETTLED_AGE` finding must not
auto-settle a wave that is still being written to.

## Erratum 3 (appended 2026-10-15) — the cgroup discriminator, and what that kill was NOT

A cgroup walk of **101 cgroups** found **no live cgroup with local `oom_kill > 0`**;
the parent slice's `1` is a propagated count, and `memory.events.local` reads `0`.
The probe now prefers `memory.events.local`, which is immune to both traps the
ancestor/service reads hit: propagation (a parent counts a descendant's kill) and
restart (`user@1000.service` started `2026-10-14 13:11:07`, *after* the
`2026-10-13 23:44:30` kill, so a service-only read misses an ancestor event
entirely).

**The killed process was not the webbridge daemon.** Journal: pid `1732581`
(`python3`) in `app-Hyprland-xdg-terminal-exec-dd9e67bd.scope`, argv unknown, cgroup
path now `ENOENT`. The mint's demand instance is the operator's separate account of
a webbridge OOM-death; this boot's kill is an unrelated desktop event and must not
be cited as that demand's evidence.
