# SrcSystemdUserService — systemd v262 `user@.service.in` and the user-slice units: OOM placement

Question: what `OOMScoreAdjust=` does the per-user service manager carry at systemd v262, what comment or
commit explains it, does any user-slice unit in `units/` set `OOMScoreAdjust=` or `ManagedOOM*`, and what
SOURCES row or anchor this needs for C1.

Bottom line: `OOMScoreAdjust=100` at `units/user@.service.in:35`, explained by commit
`ce7de0ba8ef355c5119e7dffc46e075b257dc90d` ("units: run user service managers at OOM score adjustment 100");
there is **no in-file comment** for the line. No slice unit at v262 sets `OOMScoreAdjust=` or any
`ManagedOOM*` key. The file is **unowned** by `corpus/SOURCES.md` (`grep -i 'user@\.service'` → 0 rows,
`grep -i 'units/user'` → 0 rows, `grep -i 'systemd-system\.conf'` → 0 rows), so this is a **new S127+ row**,
not an anchor.

## Gate block

Access: 2026-10-22, 15:46Z–15:50Z, ordinary `curl` only (no browser, no challenge handled). HTTP 200 on every
URL below.

| URL | bytes | sha256 |
|---|---|---|
| https://raw.githubusercontent.com/systemd/systemd/v262/units/user@.service.in | 1,315 | `72c2f40dcfced1d85bcc17583715966fc8a552b68af44404c213de2ea320504c` |
| https://raw.githubusercontent.com/systemd/systemd/8cc40e0c5e9234bf45084751ac53b1fbfe70b492/units/user@.service.in (tag commit) | 1,315 | same, `cmp` identical |
| https://raw.githubusercontent.com/systemd/systemd/v262/units/user.slice | 440 | `502efa90338cff5781e7d63195906700a868094154864add8f38d252feed2715` |
| https://raw.githubusercontent.com/systemd/systemd/v262/units/user-.slice.d/10-defaults.conf | 458 | `f8779864a6741f9a80eb803a651c38914a002330dcc17f048716f1d6f0cab983` |
| https://raw.githubusercontent.com/systemd/systemd/v262/units/machine.slice | 453 | `0fe5e4c04a07de5e4421f00e35057f00cc17a0d39da004693f565f31c5c156b4` |
| https://raw.githubusercontent.com/systemd/systemd/v262/units/capsule.slice | 431 | `0651c97c08210cd7b411ecb6e1112c5bc74546b1881d000942748e3ff75c4bd2` |
| https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-system.conf.xml | 49,977 | `161359987affadc8e4a533bc9117bbbd98053cb807808b623eb24794b49b0c58` |
| https://github.com/systemd/systemd/commit/ce7de0ba8ef355c5119e7dffc46e075b257dc90d.patch | 1,355 | `3bd6862e608264559021239ce2511485aab6929effc0f2b32d99358f047c62fc` |
| https://api.github.com/repos/systemd/systemd/commits?path=units/user@.service.in&sha=v262&per_page=100 | 191,760 | `aff7712ceefae9001d5a5c2a5135d65ac0f2048c2e3cce60faf567338bf91bb8` |
| https://api.github.com/repos/systemd/systemd/commits/ce7de0ba8ef3 | 5,437 | `88d0a8a8b3cfbe4c8deed0a0abe9982f459bef0542763c21e6d2980c5536b7e9` |
| https://codeload.github.com/systemd/systemd/tar.gz/refs/tags/v262 (units-wide sweep) | 19,038,647 | `6aa77506c0644aa67f940a48e3d3a7368601f787e4f249139516d353f107bcab` |
| https://raw.githubusercontent.com/systemd/systemd/v262/man/user@.service.xml | 10,491 | `a3015b9c7168958b8e1a3f71ff1fc67e32cee3d7c62e94e735409052bdb57276` |

Tag resolution: `refs/tags/v262` is an annotated tag object `1f7dffaf714cc4488159c498b7a17cf34c5a96d5`
(tagger 2026-09-22T13:12:43Z) pointing at commit `8cc40e0c5e9234bf45084751ac53b1fbfe70b492` — the same commit
S121 records, so the v262 pin is stable.

Located quotes (verbatim, ≤25 words each):

| # | source:lines | quote |
|---|---|---|
| Q1 | `units/user@.service.in:35` | `OOMScoreAdjust=100` |
| Q2 | `ce7de0ba…patch:4` | "units: run user service managers at OOM score adjustment 100" |
| Q3 | `ce7de0ba…patch:6-7` | "Let's make it slightly more likely that a per-user service manager is killed than any system service." |
| Q4 | `man/systemd-system.conf.xml:305-306` | "except if the service manager is run for an unprivileged user, in which case this defaults to the service manager's OOM adjustment value plus 100" |
| Q5 | `units/user-.slice.d/10-defaults.conf:16` | `TasksMax=33%` |

## The setting and what explains it

`units/user@.service.in` is 36 lines: `[Unit]` at :10, `[Service]` at :19, `OOMScoreAdjust=100` at :35,
`MemoryPressureWatch=skip` at :36. The only comment blocks in the file are the licence header (:1-8), a TPM2
ordering note (:14-15) and a `ReloadSignal=` note (:25-27). **No comment states why the OOM score is 100** —
observed by `grep -n '^#'`, whose full output is those three blocks.

Commit `ce7de0ba8ef355c5119e7dffc46e075b257dc90d` (2021-09-30 author, 2021-10-04 committer, parent
`d4a402e4f6935cd7fa9ae8ea01b30944d9fcb3d0`) adds exactly one line to one file (`1 file changed, 1 insertion`,
patch line 23-24: `+OOMScoreAdjust=100`). Its message is the explanation:

- :6-8 "Let's make it slightly more likely that a per-user service manager is killed than any system service.
  We use a conservative 100 (from a range that goes all the way to 1000)."
- :12-15 "system manager and system services are placed at OOM score adjustment 0 … User service manager (both
  for root and non-root) are placed at 100. User services for non-root are placed at 200, those for root
  inherit 100."
- :18-21 "processes forked off the user *sessions* (i.e. not forked off the per-user service manager) remain at
  0 (e.g. the shell process created by a tty or ssh login)."

The per-user manager's children get their default from the parent commit `d4a402e4` ("core: add a new setting
DefaultOOMScoreAdjust= and set it to 100 above service manager's by default"), now documented at
`man/systemd-system.conf.xml:303-309`: unset means children inherit the manager's value, "except … an
unprivileged user, in which case this defaults to the service manager's OOM adjustment value plus 100".

History check: `units/user@.service.in` has 44 commits; only two mention OOM — `ce7de0ba…` (the value) and
`cafd2c0be404` (2023-03-18, "units: Order user@.service after systemd-oomd.service", which added the
`systemd-oomd.service` term to the `After=` line at :16). No later commit changed the `OOMScoreAdjust=` value,
and the tag-commit bytes are identical to the `v262` ref bytes.

## Slice units at v262: no OOM policy

`units/` at v262 is a flat directory of 340 entries; the slice files it contains are `capsule.slice`,
`machine.slice`, `slices.target`, `system-systemd-cryptsetup.slice`, `system-systemd-mute-console.slice`,
`system-systemd-veritysetup.slice`, `user.slice` and the `user-.slice.d` directory (there is no `system.slice`
file at all).

- `units/user.slice` is 13 lines: `[Unit]` at :10, `Description=User and Session Slice`, `Documentation=`,
  `Before=slices.target`. No `[Slice]` section, no resource-control key.
- `units/user-.slice.d/10-defaults.conf` has a `[Slice]` section whose only key is `TasksMax=33%` (:16).
- `machine.slice` and `capsule.slice` are the same 13-line shape as `user.slice`.
- Units-wide `grep -r 'ManagedOOM' units/` returns one hit only: `systemd-oomd.socket:22`
  `ListenStream=/run/systemd/oom/io.systemd.ManagedOOM`, a varlink socket path, not a unit setting. No unit sets
  `ManagedOOMSwap=` or `ManagedOOMMemoryPressure=` — the upstream default is therefore whatever the
  resource-control default is, which is S124's ground and is deliberately out of this row's scope.
- Units-wide `grep -r 'OOMScoreAdjust' units/` returns seven files, none of them a slice:
  `capsule@.service.in:36` (100), `systemd-coredump@.service.in:26` (500),
  `systemd-coredumpd.service.in:37` (−1000), `systemd-journald.service.in:42` (−250),
  `systemd-oomd.service.in:38` (−900), `systemd-udevd.service.in:41` (−1000), `user@.service.in:35` (100).
  `capsule@.service.in` is the container-side twin of the user manager (same trailing block, :36-37).

Consequence for C1 [INFERENCE, chain stated]: a process running as a unit of an unprivileged user's manager
carries adjustment 200 (100 from the unit plus the +100 default), while a process forked off a login session
carries the session's inherited value (0 in the upstream design). Which of the two the fleet's own runtimes sit
in is a runtime measurement and belongs to the seat that samples `oom_score_adj`, not to this source.

## Host cross-check (presence and key names only, no operator values copied)

- Host: `systemctl --version` → `systemd 262 (262-1-arch)`; `pacman -Q systemd earlyoom` → `systemd 262-1`,
  `earlyoom 1.9.0-1`. The v262 pin matches the running systemd.
- `/usr/lib/systemd/system/user@.service` carries the same lines at the same numbers (:24 `Slice=`,
  :30 `Delegate=`, :35 `OOMScoreAdjust=100`, :36 `MemoryPressureWatch=skip`), so the Arch package does not
  touch the OOM line [observed by grep of the installed unit].
- Two drop-ins exist for the template: `/usr/lib/systemd/system/user@.service.d/10-login-barrier.conf` whose only
  key is `After=`, and `/etc/systemd/system/user@.service.d/faster-shutdown.conf` whose only key is
  `TimeoutStopSec=`. Neither sets `OOMScoreAdjust`, so the effective manager value on this host is the upstream
  100 [observed key names; `grep -o -E '^[A-Za-z]+='`].
- `/etc/systemd/user.conf` and `/etc/systemd/system.conf` each have 0 `DefaultOOMScoreAdjust=` lines, and
  `/etc/systemd/user.conf.d`, `/etc/systemd/system.conf.d` contain 0 files naming the key (the `user.conf.d`
  directory exists; `system.conf.d` exists). The unprivileged manager therefore keeps its built-in +100 default
  → user services at 200 [INFERENCE from Q4 plus those zero counts; no host value was read or copied].
- `/etc/systemd/system/user@.service.d` is an operator directory and its file name is cited only as a key-name
  observation; no value from it is reproduced here.

## Ready-to-paste SOURCES row

`S???` is this seat's placeholder as instructed; the next free id at writing time is **S127** (last registry row
is S126 at `corpus/SOURCES.md:132`, and `grep -c -E '^\| S12[7-9]'` → 0). The counter needs an id ≥ S127
(`.ufo/waves/round-27/count-c1.sh:11`), so substitute S127 unless the planner has already spent it. Eleven
columns, status `mined`, no `|` inside cells.

```markdown
| S??? | systemd v262 per-user service manager unit and the OOM score default for its children — https://raw.githubusercontent.com/systemd/systemd/v262/units/user@.service.in ; https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-system.conf.xml ; https://github.com/systemd/systemd/commit/ce7de0ba8ef355c5119e7dffc46e075b257dc90d.patch | code | A | the per-user service manager's OOM placement at the v262 release tag and what its children inherit: the `OOMScoreAdjust=` line in `units/user@.service.in`, the `DefaultOOMScoreAdjust=` default sentence in `systemd-system.conf(5)`, and a `units/`-wide sweep for `OOMScoreAdjust=` and `ManagedOOM*`; not this host's live per-process `oom_score_adj` values, not earlyoom's victim selection, not the kernel badness function, not the meaning of the `ManagedOOM*` keys (S124) | units/user@.service.in:35 (`OOMScoreAdjust=100`), :24 (`Slice=user-%i.slice`), :36 (`MemoryPressureWatch=skip`), :19 (`[Service]`); no comment in the file explains :35 (comment blocks are :1-8, :14-15, :25-27); units/ sweep at v262 (tarball sha256 6aa77506c0644aa67f940a48e3d3a7368601f787e4f249139516d353f107bcab): `OOMScoreAdjust=` only in capsule@.service.in:36 (100), systemd-coredump@.service.in:26 (500), systemd-coredumpd.service.in:37 (-1000), systemd-journald.service.in:42 (-250), systemd-oomd.service.in:38 (-900), systemd-udevd.service.in:41 (-1000), user@.service.in:35 (100); no slice file sets it; `ManagedOOM` only at systemd-oomd.socket:22 (varlink path); units/user.slice:10-13 (`[Unit]` only); units/user-.slice.d/10-defaults.conf:16 (`TasksMax=33%`); man/systemd-system.conf.xml:303-309 (an unprivileged manager's children default to the manager's value plus 100); commit ce7de0ba8ef355c5119e7dffc46e075b257dc90d (parent d4a402e4f6935cd7fa9ae8ea01b30944d9fcb3d0), patch :4 subject, :6-8 rationale, :12-15 the 0/100/200 placement, :18-21 session-forked processes left at 0; tag v262 = annotated tag 1f7dffaf714cc4488159c498b7a17cf34c5a96d5 → commit 8cc40e0c5e9234bf45084751ac53b1fbfe70b492; unit file 1,315 B sha256 72c2f40dcfced1d85bcc17583715966fc8a552b68af44404c213de2ea320504c, byte-identical at the tag commit | A per-user service manager runs at OOM score adjustment 100 and its unprivileged user's service processes default to that value plus 100, while the user slice unit adds no OOM policy of its own. | mined | 2026-10-22 | on-release | corpus/knowledge/oom-victim-selection-r27.md |
```

## Privacy and tooling

- Nothing here copies a command line, uid, pid list, journal `MESSAGE` text, harness setting key or value,
  session-store path, `/etc/default/earlyoom` value, or any `--prefer`/`--avoid`/`--ignore` expression. Host
  reads were limited to `systemctl --version`, `pacman -Q`, and key-name-only greps of installed unit and
  drop-in files; no unit was started, stopped, enabled or restarted; no `oom_score_adj` was written; no signal
  was sent; no omp process was run.
- Tooling: no install or upgrade (the paused pacman rule was not touched). Stock `curl`, `tar`, `grep`,
  `sha256sum`, `cmp`, the read/write tools, and the `eval`-free shell. Scratch (including the 19 MB tarball) is
  under `/fast/scratch/hyaku/mori-r27/SrcSystemdUserService/`.
- No jj command was run at any root; no git write command was run in the lane.

## Unresolved gaps

- `systemd.exec(5)`'s `OOMScoreAdjust=` range and `-1000` semantics are not this row's and were not fetched;
  the kernel-side range sits in proc.rst (S082) and the units here only show the chosen values.
- Whether the fleet's processes actually carry 0 or 200 depends on whether they are children of a login
  session or units of the user manager; only a runtime sample can settle it, and that sample belongs to the
  `oom_score_adj` seat.
- `system.slice` has no file in `units/` at v262, so its OOM placement (0, inherited) is a pid1 runtime fact,
  not a unit-file fact; nothing here should be cited as a file anchor for it.
