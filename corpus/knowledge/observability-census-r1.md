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
