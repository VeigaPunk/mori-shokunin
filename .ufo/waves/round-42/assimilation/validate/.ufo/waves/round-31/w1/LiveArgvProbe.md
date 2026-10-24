# LiveArgvProbe — FP/FN classes of the census watchdog probe (mori round 31, wave 1)

Seat MoriR31.LiveArgvProbe, 2026-10-22. Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Scratch `/fast/scratch/hyaku/mori-r31/LiveArgvProbe/` — scripts `exp-a.sh`…`exp-d.sh` kept as run evidence.
Leaf measurement with throwaway processes only: every process capped with `timeout`, killed by recorded pid,
kill confirmed by `kill -0` failure inside each script. No process I did not start was signalled.
All pids in this file are written `<pid>`. No uid, slice, session id or OMP setting value appears here.

## Probe under test

`tools/mori-census.sh:704-730` (`probe_watchdog()`; banner comment at :703); operative lines (grep-verified): 

- `mori-census.sh:711`: `cap "$PGREP_BIN" -af shokunin-watchdog`
- `mori-census.sh:713`: `pids=$(printf '%s\n' "$CAP_OUT" | grep -E 'shokunin-watchdog' | grep -vF 'pgrep' || true)`
- `mori-census.sh:715`: `pid_n=$(printf '%s\n' "$pids" | grep -c . || true)`

So the pipeline is `pgrep -af shokunin-watchdog | grep -E 'shokunin-watchdog' | grep -vF 'pgrep'` and
`pid_n` counts surviving **lines**. `PGREP_BIN` defaults to PATH `pgrep` (`mori-census.sh:315`); all tests
below call `/usr/bin/pgrep` explicitly.

## Environment (this host)

- `/usr/bin/pgrep --version` → `pgrep from procps-ng 4.0.7`
- kernel `7.2.11-arch1-1`; bash `5.3.20(1)`; Python `3.14.8`; `getconf CLK_TCK` = `100`
- `PR_SET_NAME = 15`: `/usr/include/linux/prctl.h:56` `#define PR_SET_NAME    15`
- Tooling directive: **no installs performed** — host tools sufficient (procps-ng 4.0.7 already present).

## (a) argv-mention-only decoy → FALSE POSITIVE

Command: `timeout 60 bash -c 'exec -a "less shokunin-watchdog.sh" sleep 50'` (script `exp-a.sh`).

```
-- decoy /proc/<pid>/comm:
sleep
-- decoy /proc/<pid>/cmdline (NULs rendered as spaces):
less shokunin-watchdog.sh 50
-- stage 3 census probe: ... | grep -vF 'pgrep' (pids masked):
<pid>  timeout 60 bash -c exec -a "less shokunin-watchdog.sh" sleep 50
<pid>  less shokunin-watchdog.sh 50
<pid>  grep -E shokunin-watchdog
-- census probe line count (= what census pid_n becomes):
3
-- decoy-only line count within census probe output:
1
decoy reaped
wrapper reaped
```

Reading: the process is `sleep` (comm `sleep`), its argv[0] was rewritten to merely *mention* the name.
`pgrep -f` matches the needle anywhere in the full command line, so the decoy passes all three stages and
`pid_n` becomes 3 while the watchdog is absent. The two extra counted lines are both mine and both
not-the-watchdog: the `timeout` wrapper of the same launch (line-vs-process inflation, since `mori-census.sh:715`
counts lines) and the census pipeline's own `grep -E shokunin-watchdog` stage, caught live by the snapshot —
the `grep -vF 'pgrep'` filter does **not** remove that stage's line (it contains no "pgrep" substring).

Row supported (my label, for the C1 table): **R-FP-argv** — observation "full command line merely mentions
shokunin-watchdog"; reading "`pgrep -f` matches the full cmdline, comm stays `sleep`"; verdict FALSE POSITIVE.
Sources: S161 (`pgrep.1` `-f` full-cmdline match), S162 (`pgrep.c`), S170 (`proc_pid_cmdline`); contrast S169 (comm).

## (b) candidate with "pgrep" in its argv → FALSE NEGATIVE

Command: `timeout 60 bash -c 'exec -a "shokunin-watchdog --pgrep-mode" sleep 50'` (script `exp-b.sh`).

```
-- decoy /proc/<pid>/comm:
sleep
-- decoy /proc/<pid>/cmdline (NULs rendered as spaces):
shokunin-watchdog --pgrep-mode 50
-- stage 3 census probe: ... | grep -vF 'pgrep' (pids masked):
<pid>  grep -E shokunin-watchdog
-- decoy line count after stage 2 (expect 1):
1
-- decoy line count after stage 3 census probe (expect 0):
0
decoy reaped
wrapper reaped
```

Reading: stage 1 listed the decoy and stage 2 kept it (count 1); the census `grep -vF 'pgrep'` stage then
deleted the line (count 0). The filter is line-based over the full cmdline, so it drops **any** candidate whose
argv contains the substring "pgrep" — including a watchdog-argv lookalike (or a real watchdog started with a
pgrep-mentioning flag). The filter's intended target (the pgrep process itself) never needs it: pgrep excludes
itself. The only surviving line in stage 3 is again the census pipeline's own `grep -E` stage.

Row supported: **R-FN-pgrep-substring** — observation "candidate cmdline contains substring pgrep"; reading
"`grep -vF 'pgrep'` deletes the whole line after listing"; verdict FALSE NEGATIVE.
Sources: S161, S162, S170.

## (c) comm forged via PR_SET_NAME → `pgrep -x` FP (and census `-af` FN)

Command (script `exp-c.sh`): `timeout 60 python3 -c '…libc.prctl(15, b"shokunin-watchd", 0, 0, 0)…; time.sleep(45)'`
with `PR_SET_NAME=15` grounded at `/usr/include/linux/prctl.h:56`.

```
prctl(PR_SET_NAME=15) rc: 0
-- decoy /proc/<pid>/comm after PR_SET_NAME:
shokunin-watchd
-- decoy /proc/<pid>/cmdline first 60 bytes (still python3):
python3 -c import ctypes,time; libc=ctypes.CDLL("libc.so.6",
-- /usr/bin/pgrep -x shokunin-watchd (pids masked):
<pid>
-- pgrep -x shokunin-watchd match count:
1
-- census probe pipeline lines naming python3 (expect 0):
0
decoy reaped
wrapper reaped
```

Reading: prctl returned 0 and `/proc/<pid>/comm` became `shokunin-watchd` — exactly 15 chars, the truncation of
`shokunin-watchdog` at TASK_COMM_LEN 16 incl. NUL — while the cmdline stayed `python3 -c …`. `pgrep -x` matches
the comm exactly and returned this process (count 1) although it is not the watchdog; note the real bash watchdog's
own comm truncates to the same 15 chars, so `-x shokunin-watchd` cannot separate real from forged. Conversely the
census cmdline pipeline listed it **0** times: a comm-only forgery is invisible to `pgrep -af`.

Row supported: **R-FP-comm** — observation "process sets comm via prctl(PR_SET_NAME) to the truncated watchdog
name"; reading "`pgrep -x` matches comm exactly; comm is user-writable; cmdline unchanged"; verdict: an `-x` match
is not identity (FALSE POSITIVE for comm-based checks) and the census `-af` pipeline misses it entirely.
Sources: S166 (`fs/proc/base.c`), S167 (`fs/proc/array.c`), S169 (`proc_pid_comm.5`), S172 (PR_SET_NAME).

## (d) pid reuse is not identity (`/proc/<pid>/stat` field 22)

Two consecutive runs of the identical command line `timeout 20 sleep 3` (script `exp-d.sh`).

```
run 1: command line 'timeout 20 sleep 3' (child cmdline: sleep 3 )
  wrapper=<pid> decoy=<pid> (masked); /proc/<pid>/stat field22 starttime = 5741473
run 2: command line 'timeout 20 sleep 3' (child cmdline: sleep 3 )
  wrapper=<pid> decoy=<pid> (masked); /proc/<pid>/stat field22 starttime = 5741569
  decoy pid DIFFERENT from previous run (both shown as <pid> in report)
getconf CLK_TCK = 100
field22 starttime DIFFERS across the two identical command lines: run1=5741473 run2=5741569 (clock ticks since boot)
```

Reading: identical command line, different pid and different field 22 (starttime; 5741569 − 5741473 = 96 ticks ≈
0.96 s at CLK_TCK=100). A pid observed earlier cannot certify the same daemon incarnation now: identity needs the
(pid, starttime) pair, otherwise a reused pid reads as "still alive".

Row supported: **R-ID-starttime** — observation "two consecutive runs of one identical command line"; reading
"`/proc/<pid>/stat` field 22 (starttime) and pid both differ"; verdict: pid or cmdline alone is not identity; pair
pid with field 22. Sources: S167 (`fs/proc/array.c`), S171 (`proc_pid_stat.5` field 22).

## Bonus artifacts observed while measuring (both FALSE POSITIVE classes)

- **R-FP-selfstage**: the census pipeline's own `grep -E shokunin-watchdog` stage survives `grep -vF 'pgrep'`
  (no "pgrep" in its argv) and was counted in (a) and (b) stage 3. `pid_n` can count the probe's own pipeline.
  Sources: S161, S162.
- **R-FP-linecount**: `mori-census.sh:715` counts lines, not processes — one decoy launch produced two counted
  lines (timeout wrapper + decoy) in (a). Sources: S161.

## Live unrelated process (observed, untouched)

Final sweep found one live process I did not start: cmdline `shokunin-watchdog 8` (pid masked here). It is not
mine, I did not signal it, and it is excluded from all counts above. It illustrates the entry's thesis live: the
probe sees the cmdline text but cannot attribute watchdog identity from it.

## Hygiene

- Every decoy killed by recorded pid; each script printed `decoy reaped` and `wrapper reaped` (10 processes over
  (a)–(d): 2+2+2+4; an earlier aborted round's decoys self-expired under their `timeout 60` caps).
- Final sweep: all my markers `none` (`less shokunin-watchdo[g]`, `--pgrep-mod[e]`, `PR_SET_NAM[E]`,
  `exp-[abcd]\.s[h]`, `pgrep -x shokunin-watchd` → none).
- One aborted first round leaked `/proc/cmdline` (kernel boot args) into transient tool output only; not
  reproduced or retained anywhere.
- No tools installed (nothing needed); no git/jj writes; no files written outside my report and scratch dir.
