# Host unit / OOM score-adjust recon — round 27, wave 1

Seat `MoriR27.HostUnitOomAdjust`. Read-only recon, run 2026-10-22 against the live host.
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`. No unit, sysctl, cgroup, systemd drop-in or
`/etc` file was written, enabled, started, stopped or reloaded; no signal was sent to any process;
no `pacman` transaction was run (nothing installed or upgraded, so the tooling directive has nothing
to record). Only this report file was written.

Host identity (observed): kernel `7.2.11-arch1-1` (`uname -r`), `systemd 262 (262-1-arch)`
(`systemctl --version`, line 1), `earlyoom 1.9.0-1` (`pacman -Q earlyoom`), Arch Linux
(`/etc/os-release` `NAME`).

## 1. `earlyoom.service`

Command: `systemctl show earlyoom.service -p OOMScoreAdjust -p ExecStart -p MemoryLow -p ManagedOOMMemoryPressure`

| Property | Value | Where it comes from |
|---|---|---|
| `ActiveState` / `SubState` | `active` / `running` | command output |
| `OOMScoreAdjust` | `-100` | `/usr/lib/systemd/system/earlyoom.service:14` — `OOMScoreAdjust=-100` |
| `ExecStart` binary | `/usr/bin/earlyoom` | unit `:7` — `ExecStart=/usr/bin/earlyoom $EARLYOOM_ARGS`; `systemctl show` prints `path=/usr/bin/earlyoom` |
| `ExecStart` flags | **none literal** — the argv is the binary plus the environment expansion `$EARLYOOM_ARGS`, fed by `EnvironmentFile=-/etc/default/earlyoom` (unit `:6`, `ignore_errors=yes`) | unit `:6-7` |
| `MemoryLow` | `0` | command output |
| `ManagedOOMMemoryPressure` | `auto` (inherit) | command output |

`DropInPaths=` is empty and `/etc/systemd/system/earlyoom.service.d/` does not exist, so no drop-in
overrides any of the above. `FragmentPath=/usr/lib/systemd/system/earlyoom.service`
(sha256 `8758ddb55bde2177239b26ab193db4a6ab07f7570a1742826d2b0765d346dbd2`).

Supporting unit lines (all `/usr/lib/systemd/system/earlyoom.service`): `:12` `Nice=-20`,
`:17` `Restart=always`, `:19` `TasksMax=10`, `:20` `MemoryMax=50M`, `:22` `DynamicUser=true`.

Effective runtime values (sampled once from the live main process):

- `oom_score_adj` = `-100` (matches the unit; still above the `-1000` floor, so the kernel can still
  pick earlyoom under extreme pressure).
- `oom_score` = `600`.
- `Nice` = `-20` (`systemctl show -p Nice`).

### Flags actually in effect (presence only; no values copied)

Live argv was masked before display — each non-flag token was replaced by a placeholder, so no
`/etc/default/earlyoom` value and no `--prefer` / `--avoid` expression entered this report. The
process carries exactly three option pairs, in argv order:

| Flag | Present | Meaning in earlyoom v1.9.0 |
|---|---|---|
| `--prefer` | **yes** (long form only) | `main.c:329` "prefer to kill processes matching REGEX" |
| `--avoid` | **yes** (long form only) | `main.c:330` "avoid killing processes matching REGEX" |
| `--ignore` | **no** | — |
| `--sort-by-rss` | **no** | — |
| `-r` | **yes** | `main.c:270-275` — memory *report interval* in seconds, `main.c:323` "memory report interval in seconds (default 1), set" |
| `-p` | **no** | `main.c:277-278` sets the self-priority flag; `main.c:325` "set niceness of earlyoom to -20 and oom_score_adj to" and `main.c:401` `int ret = set_oom_score_adj(-100);` |

Also tested and absent (15 further flag tokens): `--dryrun`, `--syslog`, `--ignore-root-user`,
`-d`, `-g`, `-n`, `-k`, `-i`, `-v`, `-m`, `-s`, `-M`, `-S`, `-N`, `-P`.

Correction for the wave: `-r` and `-p` are **not** short spellings of prefer/avoid in earlyoom 1.9.0.
The option table at `main.c:181-186` gives long-only `prefer` / `avoid` / `ignore` / `sort-by-rss`,
and `short_opt` at `main.c:179` is `const char* short_opt = "m:s:M:S:kingN:P:dvr:ph";`. So `-p` is
earlyoom raising its own priority (here redundant: the unit already forces `OOMScoreAdjust=-100`
and `Nice=-20`), and `-r` only sets the report cadence.

Net effect on victim choice (host state, not inference): two regex policies are armed (one prefer,
one avoid), none to ignore, default oom_score sorting (RSS sorting off), no dry-run.

## 2. `user@$(id -u).service` — the session user manager

Command: `systemctl show user@$(id -u).service -p OOMScoreAdjust -p ManagedOOMMemoryPressure`

| Property | Value | Where it comes from |
|---|---|---|
| `ActiveState` / `SubState` | `active` / `running` | command output |
| `OOMScoreAdjust` | `100` | `/usr/lib/systemd/system/user@.service:35` — `OOMScoreAdjust=100` |
| `ManagedOOMMemoryPressure` | `auto` | command output |

`FragmentPath=/usr/lib/systemd/system/user@.service`
(sha256 `96e528b5e7d593dc7e48657b9127a4ad27ffe863d0319956314cb6b954159cfb`).
`DropInPaths` lists two drop-ins that do not touch OOM: `/usr/lib/systemd/system/user@.service.d/10-login-barrier.conf`
and `/etc/systemd/system/user@.service.d/faster-shutdown.conf` (the latter contains only `TimeoutStopSec=5s`).
`grep -rn 'OOMScoreAdjust\|ManagedOOMMemoryPressure' /etc/systemd/system/` returns no hits, so nothing
under `/etc` overrides either value.

Effective runtime values:

- user manager main process: `oom_score_adj=100`, `oom_score=733`.
- its `init.scope`: `oom_score_adj=100`.
- a terminal-launched scope under it (mine): `oom_score_adj=200`, `oom_score=847`.

Why 200 rather than 100 — systemd v262 makes a non-root manager raise the default adjustment of its
children by 100 over itself. `src/core/main.c:3048` (comment): "Run our services at slightly higher
OOM score than ourselves."; `:3055` `if (getuid() == 0)` → `:3056` `return;` (root managers skip the
bump); `:3063` `b = saturate_add(a, 100, OOM_SCORE_ADJ_MAX);`. Live confirmation:
`systemctl show -p DefaultOOMScoreAdjust --value` → `0` for the system manager (root, no bump) and
`200` for the user manager (`systemctl --user show -p DefaultOOMScoreAdjust --value`), with no config
file setting `DefaultOOMScoreAdjust` (`grep -n DefaultOOMScoreAdjust` in `/etc/systemd/{system,user}.conf`
and the conf.d directories: no hits). `exec_context_get_oom_score_adjust()` at `src/core/execute.c:1888-1889`
confirms a unit that leaves the key unset inherits that manager default: "if (c->oom_score_adjust_set)
return c->oom_score_adjust;".

Consequence for C1 [observed + cited code, the fleet-wide survey itself is a sibling seat's job]:
every process in this user session that does not override the key runs at `oom_score_adj=200`,
i.e. 300 points of badness above earlyoom's `-100` and 200 above a default system service (`0`).
Earlyoom's own `--avoid` regexes are the only counterweight the fleet has on this host.

## 3. `vm` sysctls

`cat /proc/sys/vm/oom_kill_allocating_task /proc/sys/vm/panic_on_oom /proc/sys/vm/overcommit_memory`

| sysctl | value | meaning |
|---|---|---|
| `vm.oom_kill_allocating_task` | `0` | kernel scans for a victim by badness; it does not kill the task that triggered OOM |
| `vm.panic_on_oom` | `0` | a kernel OOM kill does not panic the host |
| `vm.overcommit_memory` | `0` | heuristic overcommit; no hard cap, so enforcement is earlyoom + the kernel OOM killer |

`systemd-oomd.service` is `inactive` and `disabled`, so userspace OOM handling on this host is
earlyoom alone (`systemctl is-active` / `is-enabled`).

## 4. `memory.oom.group` along my own shell's cgroup path

`cat /proc/self/cgroup` → `0::/user.slice/user-UID.slice/user@UID.service/app.slice/app-graphical.slice/app-Hyprland-…-exec-<suffix>.scope`
(the final segment is a transient per-terminal scope; its random unit-name suffix is elided here, and
the `\x2d` escapes are systemd's escaping of `-` in the unit name).

| cgroup | unit | `memory.oom.group` |
|---|---|---|
| root cgroup | `/sys/fs/cgroup/memory.oom.group` | file absent |
| `/user.slice` | `user.slice` | `0` |
| `/user.slice/user-UID.slice` | `user-UID.slice` | `0` |
| `/user.slice/user-UID.slice/user@UID.service` | `user@UID.service` | `0` |
| `…/app.slice` | `app.slice` | `0` |
| `…/app-graphical.slice` | `app-graphical.slice` | `0` |
| `…/app-Hyprland-…-exec-<suffix>.scope` | my shell's terminal scope | `0` |
| `/system.slice` | `system.slice` | `0` |
| `/system.slice/earlyoom.service` | `earlyoom.service` | `0` |

Every level where the file exists reads `0`, so group kill is off along this whole chain: a kernel
OOM kill inside these cgroups takes one process, not the cgroup. `ManagedOOMMemoryPressure` is `auto`
on `system.slice`, `user.slice`, `earlyoom.service` and `user@UID.service` (inherited default), and
`MemoryLow=0` on both slices.

## 5. `/etc/default/earlyoom` versus the packaged file

`pacman -Qkk earlyoom` (read-only) output, verbatim except the repeated unit prefix:

```
backup file: earlyoom: /etc/default/earlyoom (Modification time mismatch)
backup file: earlyoom: /etc/default/earlyoom (Size mismatch)
backup file: earlyoom: /etc/default/earlyoom (SHA256 checksum mismatch)
earlyoom: 17 total files, 0 altered files
```

**Result: the host file differs from the packaged one** on all three tests (mtime, size, SHA256).
It is registered as a pacman backup file, which is why the file tally still reads `0 altered files`
(backup files are excluded from that count by design). `sha256sum /etc/default/earlyoom` was run and
returns a well-formed 64-hex digest; neither that digest nor any file content is reproduced here.
Metadata only: `-rw-r--r-- root root`, 697 bytes. The package archive is not in the pacman cache
(`/var/cache/pacman/pkg/` has no `earlyoom-1.9.0-1-*.pkg.tar.*`), so `pacman -Qkk` against the local
DB is the comparison path used.

Meaning: the live flags in §1 are the host's local configuration, not Arch's shipped defaults.
[INFERENCE] A default Arch `/etc/default/earlyoom` would not necessarily arm `--prefer`/`--avoid`,
so the fleet's exposure to those regexes is a local choice, not an upstream one.

## 6. Source anchors (for the C1 owner)

Opened 2026-10-22 by plain `curl` of the public raw URL, no browser, no access control bypassed.

| URL | sha256 | SOURCES row |
|---|---|---|
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c` | `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` | same file as existing **S119** — this re-open **adds an anchor to S119, not a new row** |
| `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/main.c` | `5ecdca43a8e0ed088758b228b54c72df311c0b9dc3855721ed02c5b169d3aae3` | **new** — candidate row (systemd core main, `DefaultOOMScoreAdjust` computation) |
| `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/execute.c` | `30f8c6b60858f0722637f99f55e86f3babe9c933dce67a6023c06fc8a863dc8d` | **new** — candidate row (`exec_context_get_oom_score_adjust`) |

Verbatim quotes used above, each well under 25 words, with line numbers:

- `main.c:179` — `const char* short_opt = "m:s:M:S:kingN:P:dvr:ph";`
- `main.c:270` / `main.c:275` — `case 'r':` … `args.report_interval_ms = (int)(report_interval_f * 1000);`
- `main.c:277-278` — `case 'p':` / `set_my_priority = 1;`
- `main.c:323` — `memory report interval in seconds (default 1), set`
- `main.c:325` — `set niceness of earlyoom to -20 and oom_score_adj to`
- `main.c:329-330` — `prefer to kill processes matching REGEX` / `avoid killing processes matching REGEX`
- `main.c:401` — `int ret = set_oom_score_adj(-100);`
- systemd `src/core/main.c:3048` — `Run our services at slightly higher OOM score than ourselves.`
- systemd `src/core/main.c:3055` — `if (getuid() == 0)`
- systemd `src/core/main.c:3063` — `b = saturate_add(a, 100, OOM_SCORE_ADJ_MAX);`
- systemd `src/core/execute.c:1888` — `if (c->oom_score_adjust_set)`

Local unit files (hashes quoted in §1/§2) are `/usr/lib/systemd/system/earlyoom.service` and
`/usr/lib/systemd/system/user@.service`; line numbers above are from those on-disk files.

## 7. Not done here, and gaps

- Not done by this seat: journal scans, send counts, victim classes, boot -1 attribution — those are
  the other C1 seats' slices. This seat did not read any journal.
- Not surveyed: `oom_score_adj` of individual fleet runtimes (`omp`, `bun`, `node`, `python`); only
  the manager-level default (+200) and two sample processes were taken here.
- [INFERENCE] With `vm.oom_kill_allocating_task=0`, `vm.panic_on_oom=0` and every `memory.oom.group=0`
  in the session's chain, a kernel OOM kill here is a single-process, badness-ordered choice, and the
  fleet's +200 default puts those processes ahead of unadjusted system services.
- Unresolved: which component makes earlyoom's argv put `-r` before the two regex options (argv order
  is not unit-authored since `ExecStart` only expands `$EARLYOOM_ARGS`); not needed for C1, not chased.
