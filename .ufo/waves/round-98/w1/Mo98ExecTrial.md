# Mo98ExecTrial — live trial of tools/mori-userns-runway.py (round 98, wave w1)

Date: 2026-11-05 (host local -03). Executor seat, read-only live trial; no sysctl written, no sudo, only unprivileged
`unshare -Ur` holders created by my own user. Scratch /fast/scratch/hyaku/mori-r98/Mo98ExecTrial (removed after trial).

## Bytes under trial and environment

- Tool: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-userns-runway.py`,
  sha256 `5ab134ee036f83851eb98a9027db699a5800130c5c13598cb37aeb2abe452db2`.
- Byte pin against landing: `git rev-parse 600deb7ed2695f54b289cf5b6c3931e0fa9c8bb3:tools/mori-userns-runway.py`
  → `89335d913ddb317f1b78e156444a91b68c958b90`; `git hash-object -- tools/mori-userns-runway.py` (worktree)
  → `89335d913ddb317f1b78e156444a91b68c958b90`. Equal: this trial ran exactly the landing-revision bytes
  (lane HEAD was 379a2f616c14… with 8 dirty files during the wave; the tool file itself matches landing).
- Host: kernel 7.2.11-arch1-1, user `vgpnk` (non-root), `/proc/sys/user/max_user_namespaces` = `122865`.
- Precheck: `unshare -Ur true` → exit 0 (`PRECHECK-OK rc=0`); `command -v unshare journalctl` → `/usr/bin/unshare`,
  `/usr/bin/journalctl`.

## Step 1 — baseline runway read

```
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-userns-runway.py
USERNS_RUNWAY limit=122865 used_lb=6 pids=3473 unreadable=3211 runway=122859 low=32 state=ok
rc=0
```

Matches knowledge-entry format and semantics (limit 122865 = restored value; state=ok, exit 0).

## Step 2 — three holders, delta, --low threshold, kill

Script: three `unshare -Ur sleep 90 &`, `sleep 2`, read, `--low 200000`, kill, `sleep 1`, read.

```
BEFORE_USED_LB=6
--- RUN during 3 holders ---
USERNS_RUNWAY limit=122865 used_lb=9 pids=3476 unreadable=3211 runway=122856 low=32 state=ok
rc=0
--- RUN --low 200000 during 3 holders ---
USERNS_RUNWAY limit=122865 used_lb=9 pids=3476 unreadable=3210 runway=122856 low=200000 state=low
rc=1
--- RUN after kill ---
USERNS_RUNWAY limit=122865 used_lb=6 pids=3473 unreadable=3210 runway=122859 low=32 state=ok
rc=0
```

used_lb rose 6 → 9 = exactly +3 with the three holders; `--low 200000` → `state=low` exit 1; after kill back to 6,
exit 0. All three behaviors as documented.

## Step 3 — nested namespaces, pure exec chain (`unshare -Ur unshare -Ur sleep 60 &`)

```
BEFORE_USED_LB=6
--- holder ns link ---
lrwxrwxrwx 1 vgpnk vgpnk 0 Nov  5 18:37 /proc/1313709/ns/user -> user:[4026533830]
ls_rc=0
user:[4026533830]
--- RUN during nested holder ---
USERNS_RUNWAY limit=122865 used_lb=7 pids=3479 unreadable=3210 runway=122858 low=32 state=ok
rc=0
--- RUN after kill ---
USERNS_RUNWAY limit=122865 used_lb=6 pids=3477 unreadable=3210 runway=122859 low=32 state=ok
rc=0
```

Two user namespaces were created, used_lb rose by 1 (6 → 7). The holder's single link is the INNERMOST namespace;
the outer namespace was passed through by exec (no fork), so no process link points to it. This is exactly the
documented `used_lb` lower-bound case (namespaces without a process link are invisible), not a miscount. The task
parenthetical said "(2 namespaces)" — observed: 2 created, 1 linkable/counted in this exec-chain form.

## Step 3b — contrast: forked nesting (`unshare -Ur --fork unshare -Ur sleep 45 &`)

```
BEFORE_USED_LB=6
--- process tree ns links ---
pid=1337138 user:[4026533834]
pid=1337136 user:[4026533830]
--- RUN during forked nested holder ---
USERNS_RUNWAY limit=122865 used_lb=8 pids=3490 unreadable=3222 runway=122857 low=32 state=ok
rc=0
--- RUN after kill ---
USERNS_RUNWAY limit=122865 used_lb=6 pids=3488 unreadable=3222 runway=122859 low=32 state=ok
rc=0
```

With `--fork` the outer namespace keeps a live process (pid 1337136), so both created namespaces are counted:
6 → 8 = +2. Confirms the counting is "distinct non-initial inodes on readable links", per docstring and knowledge
entry lower-bound rule.

## Step 4 — journal-live scan of the incident window

```
$ python3 tools/mori-userns-runway.py --journal-live --since '2026-11-05 00:00' --until now
SYSCTL_WRITE ts=2026-11-05T05:14:52-03:00 pid=1302030 key=user.max_user_namespaces value=0 via=sh-echo
SYSCTL_WRITE ts=2026-11-05T05:14:54-03:00 pid=1316549 key=user.max_user_namespaces value=10000 via=sysctl
SYSCTL_WRITE ts=2026-11-05T05:16:04-03:00 pid=1580806 key=user.max_user_namespaces value=15638 via=sysctl
SYSCTL_WRITE ts=2026-11-05T05:16:04-03:00 pid=1580838 key=user.max_user_namespaces value=15638 via=sh-echo
SYSCTL_WRITE ts=2026-11-05T05:22:02-03:00 pid=2322929 key=user.max_user_namespaces value=0 via=sh-echo
SYSCTL_WRITE ts=2026-11-05T05:42:18-03:00 pid=2548588 key=user.max_user_namespaces value=122865 via=sysctl
SYSCTL_WRITES n=6 keys=1 userns_zero=2
rc=1
```

Reproduces the knowledge entry's Observed line exactly: `SYSCTL_WRITES n=6 keys=1 userns_zero=2`, the writes at
05:14:52 (0), 05:14:54 (10000), 05:16:04 (15638 twice — one plain `sysctl` without `-w`, one `sh-echo`), 05:22:02
(0), 05:42:18 (122865 restore). Exit 1 = "at least one write" per docstring. No user names, PWDs or command text in
the output (redaction posture holds). `journalctl` was readable as vgpnk without sudo on this host.

## Step 5 — journal edge inputs

```
$ printf '' | python3 tools/mori-userns-runway.py --journal -
SYSCTL_WRITES n=0 keys=0 userns_zero=0
rc=0
$ python3 tools/mori-userns-runway.py --journal /fast/scratch/hyaku/mori-r98/Mo98ExecTrial/does-not-exist.log
SYSCTL_WRITES_SETUP FileNotFoundError
rc=2
```

Empty input → `n=0` exit 0 (no write); missing file → `SYSCTL_WRITES_SETUP FileNotFoundError` exit 2 (fail closed,
never read as "no writes" success). Both as documented.

## Step 6 — selftest

```
$ python3 tools/mori-userns-runway.py --selftest
case ok-distinct pass
case limit-zero pass
case full pass
case low pass
case missing-limit pass
case garbage-limit pass
case no-pids pass
case journal-incident pass
case journal-forms pass
case journal-empty pass
case redaction pass
MORI_USERNS_RUNWAY_SELFTEST: PASS (11 cases)
rc=0
```

Last line matches `MORI_USERNS_RUNWAY_SELFTEST: PASS (<n> cases)` (P1 conjunct (a) shape).

## Contradictions and notes

- No contradiction with `corpus/knowledge/userns-runway-r98.md` found. Every documented behavior (delta counting,
  low/exhausted thresholds, setup exits, incident counts/timestamps, redaction, lower-bound caveat) reproduced live.
- Knowledge entry "Observed" live line shows `used_lb=7 pids=3828 unreadable=3527` vs this trial's baseline
  `used_lb=6 pids=3473 unreadable=3211` — live host drift between observations, same limit, same state=ok; not a
  contradiction.
- Caveat worth carrying: a nested creation chain that execs through the intermediate namespace leaves that namespace
  without a process link, so 2 created namespaces can count as +1. The claim already covers this via the `used_lb`
  lower-bound wording; no amendment needed.
- Unrun checks: none within my task scope. Not exercised here: bwrap ENOSPC signature under a real limit-0 host
  state (never write sysctls), fd/bind-mount-only held namespaces (out of scope for a process-link tool).
