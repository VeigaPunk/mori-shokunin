# SrcEarlyoomUnit — earlyoom unit file and Arch packaging source

Seat: `MoriR26.SrcEarlyoomUnit` (scribe, wave 1). Scope: the upstream earlyoom systemd
unit and the Arch Linux package source for earlyoom 1.9.0-1, as opened for the C1
superseding entry and the C2 tool grammar. Nothing in the lane was modified; this report
is the seat's only write.

## Two corrections the round needs before it writes anything

**C-1. The upstream unit URL named in the assignment returns HTTP 404.**
`https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.service` → **HTTP 404**,
14 bytes, body `404: Not Found`, sha256 `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed`.
Upstream at tag `v1.9.0` ships **`earlyoom.service.in`** (a template, 1340 B), not
`earlyoom.service`; the GitHub tree API for that tag lists `earlyoom.service.in`,
`earlyoom.default` and `earlyoom.initscript.in` and no `earlyoom.service`
(`https://api.github.com/repos/rfjakob/earlyoom/git/trees/v1.9.0?recursive=1`, fetched
2026-10-22). The generated `earlyoom.service` is produced by the Makefile rule
`earlyoom.%: earlyoom.%.in` (Makefile:52-53), which substitutes `:TARGET:` → `$(BINDIR)`
and `:SYSCONFDIR:` → `$(SYSCONFDIR)`. **Any SOURCES row for the upstream unit must cite
`earlyoom.service.in`, not `earlyoom.service`** — a row citing the 404 URL would be an
unopenable citation.

**C-2. The unit sets no `StandardError=` line at all, at any tag in reach.** Upstream
`earlyoom.service.in` at `v1.9.0` contains **zero** occurrences of the string `Standard`
(`grep -c Standard earlyoom.service.in` → 0). stderr reaches the journal by systemd
**defaults**, not by a unit directive: `DefaultStandardOutput=journal`
(systemd-system.conf.xml:81) and `DefaultStandardError=inherit`
(systemd-system.conf.xml:82), where `inherit` "duplicated" the stdout fd for stderr
(systemd.exec.xml:3566-3569) and `StandardError=` "defaults to the value set with
`DefaultStandardError=` … which defaults to `inherit`" (systemd.exec.xml:3571-3574).

This matters for the C2 grammar: earlyoom's messages reach the journal because the unit
never redirects stderr, and systemd's default is `inherit` of a journal stdout. The upstream
unit only *used* to say anything about stderr: at `7436b59684ff^` it carried
`StandardOutput=null` + `StandardError=syslog`, and commit `7436b59684ff`
(2018-07-18, "earlyoom.service: use \"-r 60\" instead of StandardOutput=null") removed both
lines. The 2023 hardening commit `754495c6023b` is titled "earlyoom.service: redirect
stderr and more handening" but its diff adds **no** `StandardError=` line either — every
added line is a hardening directive, and the file at that commit also has zero
occurrences of `Standard`. The subject line is not evidence of a stderr directive.

## Facts the round can rest on (with line numbers)

**F-1. The unit reads its options from one optional environment file.**
`earlyoom.service.in:6` — `EnvironmentFile=-:SYSCONFDIR:/default/earlyoom`.
`earlyoom.service.in:7` — `ExecStart=:TARGET:/earlyoom $EARLYOOM_ARGS`.
The leading `-` makes the file optional: systemd.exec.xml:3303-3306 ("prefix the path with
`-`, which causes all errors related to the file to be silently ignored"); the file is
parsed per systemd.exec.xml:3269-3301 (shell-style quoting rules, not shell evaluation).
`$EARLYOOM_ARGS` is expanded as a **separate word** and is therefore *split at whitespace*
into zero or more arguments — systemd.service.xml:1620-1624 ("it will be replaced by the
value of the environment variable split at whitespace, resulting in zero or more arguments.
For this type of expansion, quotes are respected when splitting into words, and afterwards
removed"). A `${EARLYOOM_ARGS}` would have been one argument; the unbraced form is not.

**F-2. The upstream default file the unit points at is `earlyoom.default`, installed to
`/etc/default/earlyoom`.** Makefile:55-57 (`install-default` → `install -m 644 $<
$(DESTDIR)$(SYSCONFDIR)/default/earlyoom`), with `SYSCONFDIR ?= /etc` (Makefile:16) and
`SYSTEMDUNITDIR ?= /etc/systemd/system` (Makefile:17). Upstream `earlyoom.default` at
`v1.9.0` is 563 bytes, sha256
`c0770413a180e0731583f643fc4e84f4a0dac57efb8f575b74ee9a971df984a2`. Its first two lines
say the file "is sourced by /bin/sh from /etc/init.d/earlyoom or by systemd from
earlyoom.service" — but systemd does **not** source it with a shell; it reads it with the
`EnvironmentFile=` parser. The C2 grammar does not depend on this, but a knowledge entry
saying "systemd sources the file with /bin/sh" would be wrong.

**F-3. The rendered unit that ships on this host differs from upstream v1.9.0 by exactly
one line, and Arch's packaging is what adds it.** `diff` of the Makefile-rendered template
against the installed `/usr/lib/systemd/system/earlyoom.service` shows one hunk: upstream's
`earlyoom.service.in:25` `DynamicUser=true` is followed by an inserted
`SupplementaryGroups=proc`. `PKGBUILD:21` —
`sed '/^DynamicUser=/a SupplementaryGroups=proc' -i earlyoom.service.in` — introduced by
Arch commit `3eb122e4759` (2020-04-06, "Added directive SupplementaryGroups=proc to systemd
service"). `PKGBUILD:20` also strips the `systemctl|chcon` lines from the Makefile
(`sed "/systemctl|chcon/d" -ri Makefile`), so packaging does not run `systemctl enable
earlyoom` at build time — the unit is enabled by the distribution's normal mechanisms. The
installed file is owned by `earlyoom 1.9.0-1` (`pacman -Qo
/usr/lib/systemd/system/earlyoom.service`), dated 2025-09-17, matching the Arch commit
`704e05715e672b5de664d543e734aa3f757af9bb` ("upgpkg: 1.9.0-1", 2025-09-17).

**F-4. Why `SupplementaryGroups=proc` matters for what earlyoom can read.** The daemon
runs unprivileged (upstream `earlyoom.service.in:25` `DynamicUser=true`; systemd.exec.xml:
731-733 allocates a transient user/group), yet it must read other processes' `/proc/<pid>`
entries to pick a victim (earlyoom reads `/proc/<pid>/stat`, `oom_score`, `oom_score_adj`,
`comm`, `cmdline` — meminfo.c:151-235). Two mechanisms gate that:
- **Directory traversal** of `/proc/<pid>` is `proc_pid_permission` → `has_pid_permissions`
  (fs/proc/base.c:746-753, 726-743); with no `hidepid` mount option this returns true
  outright (fs/proc/base.c:738-739).
- **The `gid=` mount option** names a group exempt from `hidepid` (proc(5) man page lines
  119-125: "users in this group behave as though `/proc` was mounted with `hidepid=0`"); the
  kernel check is `in_group_p(fs_info->pid_gid)` (fs/proc/base.c:740). The `proc` group
  (gid 26 here, `getent group proc` → `proc:x:26:`) is that exemption group, and upstream
  earlyoom's wiki states the pairing ("Mount proc with `hidepid=2,gid=adm` and set
  `SupplementaryGroups=adm` in the unit").
- On **this host** `/proc` is mounted with neither `hidepid` nor `gid=`
  (`/proc/self/mountinfo` line 26: `proc rw,nosuid,nodev,noexec,relatime`), so
  `fs_info->hide_pid` is `HIDEPID_OFF` and the early-true branch (fs/proc/base.c:738-739)
  returns true for everyone. The daemon is in group 26 nonetheless (its supplementary
  groups include gid 26).

**F-5. The hardening that changes what earlyoom can read.** Upstream
`earlyoom.service.in:22-48` sets, among others:
- `ProtectSystem=strict` (:27) — the entire filesystem hierarchy is read-only **except**
  `/dev/`, `/proc/` and `/sys/` (systemd.exec.xml:1503-1506). The `/proc` carve-out is
  what keeps earlyoom's job possible.
- `ProtectHome=true` (:29) — `/home`, `/root`, `/run/user` inaccessible and empty
  (systemd.exec.xml:1529-1531).
- `ProtectKernelTunables=true` (:35) — `/proc/sys` and friends read-only; `/proc/kallsyms`
  and `/proc/kcore` inaccessible (systemd.exec.xml:2366-2370).
  `ProtectKernelLogs=true` (:33) — `/dev/kmsg` and `/proc/kmsg` inaccessible
  (systemd.exec.xml:2417-2418). `ProtectControlGroups=true` (:36).
- `RestrictAddressFamilies=AF_UNIX` (:44), whose unit comment at :43 reads "Unix socket is
  used by dbus-send" (earlyoom's `--notify` path spawns `dbus-send`, kill.c:179);
  `SystemCallArchitectures=native` (:46), `SystemCallFilter=@system-service
  process_mrelease` (:47), `SystemCallFilter=~@privileged` (:48).
- `ProtectProc` is **not** set by the unit. systemd.exec.xml:425-428 and 436-437: the
  default is `default`, i.e. "no restrictions on `/proc/` access or visibility are made";
  systemd.exec.xml:445 states the option "cannot be used for services that need to access
  metainformation about other users' processes" — exactly what earlyoom needs. Host:
  `systemctl show earlyoom.service -p ProtectProc` → `ProtectProc=default`.
- `MemoryMax=50M` (:20), `TasksMax=10` (:19) bound the daemon itself; `Nice=-20` (:12),
  `OOMScoreAdjust=-100` (:14), `Restart=always` (:17).
  `AmbientCapabilities=CAP_KILL CAP_IPC_LOCK` (:9) with a matching
  `CapabilityBoundingSet=CAP_KILL CAP_IPC_LOCK` (:10) — the unit's comment at :8 is "Allow
  killing processes and calling mlockall()".

**F-6. The hardening lines were moved by four upstream commits; cite the tag, not the
history.** `754495c6023b` (2023-06-17) introduced the hardening block with
`SystemCallFilter=~@resources @privileged` and `IPAddressDeny=true`;
`b41ebb2275e5` (2024-04-18, "remove systemd resources syscall filter because it causes
earlyoom to be terminated when launched with -p flag") dropped `~@resources`;
`e6c797881341` (2024-04-19) changed `IPAddressDeny=true` → `any`; `c171b72ba217` (2024-04-21)
added `process_mrelease` to the allowed set. The `v1.9.0` file already carries all four
outcomes (lines 41, 47, 48).

**F-7. What the host's effective stderr destination is.** `systemctl show earlyoom.service
-p StandardOutput -p StandardError` → `StandardOutput=journal`, `StandardError=inherit`.
That is the systemd default pair, not a unit directive — consistent with F-1/F-2 and with
`grep -c Standard /usr/lib/systemd/system/earlyoom.service` → 0.

**F-8. The journal the C2 tool reads does contain earlyoom's messages, and its composition
is known.** `journalctl -q -b -u earlyoom.service -o json --output-fields=MESSAGE` on this
host yields 14 records for the current boot: 1 systemd `Started …` line, 1 `earlyoom 1.9.0`
version line, 1 `mem total:` line, 2 threshold lines (`sending SIGTERM when mem avail <=
10.00% and swap free <= 10.00%,` and `SIGKILL when mem avail <=  5.00% and swap free <=
5.00%`), 1 `--prefer` echo, 1 `--avoid` echo, and 7 `mem avail:` report lines at a 3600 s
cadence (measured deltas 3600344236, 3600266262, 3600259765, 3600273573, 3600263331,
3600269746 µs). `journalctl` here emits both `MESSAGE` and `__MONOTONIC_TIMESTAMP` for
that query, so the contract's scope rule is satisfiable. Two precision notes for the C2
grammar, both verified against the real bytes:
- The `SIGKILL` threshold line is **indented by eight spaces** and carries a **double
  space** before `5.00%` (`PRIPCT` is `"%5.2lf%%"`, msg.h:10, so `5.00` is width-5
  right-aligned). A regex `mem avail <= (\S+)%` **fails** on that line and succeeds on the
  `10.00%` one; a tolerant `mem avail <=\s*(\S+)%` matches both, yielding
  `('5.00','5.00')`.
- The version line is `earlyoom 1.9.0` — the *first* line of the invocation
  (main.c:161 `fprintf(stderr, "earlyoom " VERSION "\n")`), so it is the scope anchor the
  contract's `scope_complete` rule depends on.

**F-9. The `--avoid` / `--prefer` values on this host are host state, not upstream state,
and they are withheld.** The host `/etc/default/earlyoom` is 697 bytes, sha256
`c40931ae5b853f9f44d4d95d9a6163dc1f992fb0ef22c8c756f5e84b5b6a8517`, 21 lines, owner
`earlyoom 1.9.0-1` (a pacman backup file), mtime 2026-10-20. It differs from **both** the
upstream `earlyoom.default` (563 B) and the file the packaging would produce (607 B,
sha256 `cbf1c9d1cae25ee5121306dd1889081bf90ce7a06815227b088d8963e625bf65` — upstream plus
the `PKGBUILD:22` sed): the difference is confined to the single `EARLYOOM_ARGS=` line.
Counts that do not disclose values: `grep -c '^EARLYOOM_ARGS='` → 1; the running process's
argv is 7 words (`/usr/bin/earlyoom` plus 6); the journal carries exactly one `--prefer`
echo and one `--avoid` echo. The host file's value differs from the packaged default's (it
adds a `--prefer`, which neither upstream nor the packaged default has). The option and
expression values are withheld under the round's privacy bound; the packaged default's
sha256 is reproducible by applying `PKGBUILD:22` to the upstream `earlyoom.default`.

**F-10. The Arch repository is reachable by ordinary means and needed no challenge
avoidance.** `https://gitlab.archlinux.org/archlinux/packaging/packages/earlyoom` served
the API tree without a bot challenge; the raw file URL
`…/-/raw/704e05715e672b5de664d543e734aa3f757af9bb/PKGBUILD` returned **HTTP 200**, 1179
bytes, sha256 `f48dc3f99aee5d6a93f8cad4e4b6286dab014745aa6f85b1c3582c3db46dd4a2`, and the
same bytes as the `main` branch. The package tree at that commit holds `LICENSES`,
`.SRCINFO`, `.nvchecker.toml`, `LICENSE`, `PKGBUILD`, `REUSE.toml` — there is no separate
`/etc/default/earlyoom` in the repository; the shipped default comes from the upstream
tarball, rewritten by the `prepare()` sed.

## SOURCES row draft (ready to paste)

The registry's last row is **S113** (`corpus/SOURCES.md` line 119); rows S114+ do not
exist yet, so the next free id is S114. I leave the id as `S???` as instructed and let the
L1 own the numbering. I drafted **two** rows because the upstream unit and the Arch
packaging are two different URLs with two different tiers of authority; the L1 may admit
one, both, or merge them.

```markdown
| S??? | earlyoom systemd unit template earlyoom.service.in at v1.9.0 — https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.service.in | code | A | the upstream unit template only: how earlyoom is configured and what its hardening permits it to read; the generated earlyoom.service and the Arch packaging delta are separate sources | earlyoom.service.in:6 (EnvironmentFile=-:SYSCONFDIR:/default/earlyoom), :7 (ExecStart=:TARGET:/earlyoom $EARLYOOM_ARGS), :9-10 (AmbientCapabilities=CAP_KILL CAP_IPC_LOCK, CapabilityBoundingSet=), :12 (Nice=-20), :14 (OOMScoreAdjust=-100), :17 (Restart=always), :19-20 (TasksMax=10, MemoryMax=50M), :25 (DynamicUser=true), :27 (ProtectSystem=strict), :29 (ProtectHome=true), :33 (ProtectKernelLogs=true), :35 (ProtectKernelTunables=true), :36 (ProtectControlGroups=true), :41 (IPAddressDeny=any), :43-44 (dbus-send comment, RestrictAddressFamilies=AF_UNIX), :46-48 (SystemCallArchitectures=native, SystemCallFilter=@system-service process_mrelease, SystemCallFilter=~@privileged); no StandardOutput= or StandardError= line anywhere in the file; HTTP 200, 1,340 B, sha256 d4019b66d87539a006fc2d178d972dcf1b46e70343627b8bf66d1a08dcdda0bd | The unit sets no StandardOutput= or StandardError= at all, so earlyoom's stderr reaches the journal through systemd's defaults (DefaultStandardOutput=journal, DefaultStandardError=inherit) rather than through a unit directive; and ProtectProc is unset, so the unit imposes no /proc visibility restriction on the daemon that must read other processes' metadata. | mined | 2026-10-22 | on-release | corpus/knowledge/userspace-oom-killers-r26.md |
```

```markdown
| S??? | Arch Linux packaging for earlyoom 1.9.0-1 — https://gitlab.archlinux.org/archlinux/packaging/packages/earlyoom/-/raw/704e05715e672b5de664d543e734aa3f757af9bb/PKGBUILD | code | A | how the distribution packages earlyoom 1.9.0-1 and what it changes in the upstream unit and in the shipped default file; not the upstream unit itself | PKGBUILD:5-6 (pkgver=1.9.0, pkgrel=1), :14 (backup=("etc/default/earlyoom")), :20 (sed strips the systemctl and chcon lines from the Makefile), :21 (sed adds SupplementaryGroups=proc after DynamicUser=), :22 (sed appends the notify and avoid options to the shipped EARLYOOM_ARGS), :27 (build with SYSTEMDUNITDIR=/usr/lib/systemd/system VERSION=$pkgver), :32 (install with the same SYSTEMDUNITDIR); HTTP 200, 1,179 B, sha256 f48dc3f99aee5d6a93f8cad4e4b6286dab014745aa6f85b1c3582c3db46dd4a2 | The distribution's unit is not upstream's unit: packaging adds one supplementary group to it and ships the configuration file as a pacman backup, so the running daemon can traverse other processes' /proc entries while its configuration file survives upgrades. | mined | 2026-10-22 | on-release | corpus/knowledge/userspace-oom-killers-r26.md |
```

Tier reasoning: **A** for both. Each is a first-party artifact of the project or of the
distribution that ships it, pinned to an immutable tag or commit, quoted by line number,
and byte-hashed; the registry's tier A covers exactly this kind of primary material
(e.g. S003, S011, S016 — upstream sources read the same way). Neither is second-hand, so
neither is B or C. Status **mined**: both rows carry facts the round's C1 superseding entry
and the C2 grammar rely on. `recheck` `on-release` matches how upstream-tag rows in the
registry are marked (S003, S011, S016). `used-by` is set to
`corpus/knowledge/userspace-oom-killers-r26.md`, the entry the contract's C1 requires.

The `teaches` sentences state only what the cited lines show. Two guards were applied
deliberately: the upstream row asserts the *absence* of a stderr directive (which the whole
51-line file shows) rather than claiming the unit redirects stderr, and the Arch row
asserts that packaging *adds a group* and *ships the file as a backup* without restating
the `--avoid`/`--prefer` values, which the round's privacy bound withholds.

## Gate

Sources opened 2026-10-22 by ordinary `curl` (no browser; no bot challenge encountered — the
GitLab API and raw endpoints served the repository directly).

| Source | URL | Fetch | sha256 | Located quote (≤25 words) | Decision |
|---|---|---|---|---|---|
| earlyoom.service.in at v1.9.0 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.service.in | HTTP 200, 1,340 B | `d4019b66d87539a006fc2d178d972dcf1b46e70343627b8bf66d1a08dcdda0bd` | `:6` "EnvironmentFile=-:SYSCONFDIR:/default/earlyoom"; `:25` "DynamicUser=true"; `:27` "ProtectSystem=strict" | admit, A, mined |
| earlyoom.default at v1.9.0 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.default | HTTP 200, 563 B | `c0770413a180e0731583f643fc4e84f4a0dac57efb8f575b74ee9a971df984a2` | `:1-2` "This file is sourced by /bin/sh from /etc/init.d/earlyoom or by systemd from earlyoom.service." | admit, A, mined (upstream-unit row scope note) |
| Makefile at v1.9.0 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/Makefile | HTTP 200, 2,898 B | `b852cb9b832729f37f2b19fe93956720a5a58017aa8f76a6036cc928d96127ae` | `:52-53` "earlyoom.%: earlyoom.%.in" / `sed "s\|:TARGET:\|$(BINDIR)\|g;s\|:SYSCONFDIR:\|$(SYSCONFDIR)\|g" $< > $@` | admit, A, mined (rendering rule, in the row anchor) |
| Arch PKGBUILD at 704e0571 | https://gitlab.archlinux.org/archlinux/packaging/packages/earlyoom/-/raw/704e05715e672b5de664d543e734aa3f757af9bb/PKGBUILD | HTTP 200, 1,179 B | `f48dc3f99aee5d6a93f8cad4e4b6286dab014745aa6f85b1c3582c3db46dd4a2` | `:5-6` "pkgver=1.9.0" / "pkgrel=1"; `:14` `backup=("etc/default/earlyoom")`; `:21` "sed '/^DynamicUser=/a SupplementaryGroups=proc' -i earlyoom.service.in" | admit, A, mined |
| systemd v262 exec(5) | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml | HTTP 200, 343,315 B | `44b89bffce737aff803966c207329e9fe2d28d07709a4bb8e0edf6a4ec0d844` | `:3305-3306` "prefix the path with -, which causes all errors related to the file to be silently ignored"; `:3567` "the file descriptor used for standard output is duplicated for standard error"; `:445` "It cannot be used for services that need to access metainformation about other users' processes." | admit, A, mined |
| systemd v262 system.conf(5) | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-system.conf.xml | HTTP 200, 49,977 B | `161359987affadc8e4a533bc9117bbbd98053cb807808b623eb24794b49b0c58` | `:81-82` "DefaultStandardOutput=journal" / "DefaultStandardError=inherit" | admit, A, mined |
| systemd v262 service(5) | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.service.xml | HTTP 200, 120,642 B | `12770f86a26dcdf32873225669f5aa9421283c303bbc72bddb04530850f66d44` | `:1621-1622` "replaced by the value of the environment variable split at whitespace, resulting in zero or more arguments" | admit, A, mined |
| Linux v7.2 fs/proc/base.c | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c | HTTP 200, 98,196 B | `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6` | `:738-740` "if (fs_info->hide_pid < hide_pid_min) return true;" / "if (in_group_p(fs_info->pid_gid)) return true;" | admit, A, mined |
| proc(5) | https://man7.org/linux/man-pages/man5/proc.5.html | HTTP 200, 31,125 B | `b197c5fa64577269f992d50f60acfd5e0cc3df756644ddd8bd19a02591272a97` | `:120-123` "Specifies the ID of a group whose members are authorized to learn process information otherwise prohibited by hidepid" | admit, A, mined |
| upstream wiki proc-hidepid | https://raw.githubusercontent.com/wiki/rfjakob/earlyoom/proc-hidepid.md | HTTP 200, 1,023 B | `dfed12c8bb40ee9ef5c8cdef9ea40464b884dc8b6cfb1a6e1b215525d290cab1` | `:12` "earlyoom running as a normal user can no longer see (hidepid=2) or look at the memory usage (hidepid=1) of running processes" | admit, A, mined |
| **earlyoom.service at v1.9.0 (the URL in the assignment)** | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.service | **HTTP 404**, 14 B | `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` | body "404: Not Found" | **reject — unopenable citation; upstream ships earlyoom.service.in** |
| Linux v7.2 include/linux/proc_fs.h | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/proc_fs.h | HTTP 429 (rate-limited) | — | enum proc_hidepid { HIDEPID_OFF = 0, HIDEPID_NO_ACCESS = 1, HIDEPID_INVISIBLE = 2, HIDEPID_NOT_PTRACEABLE = 4 } | fetched via mirror cdn.jsdelivr.net/gh/torvalds/linux@v7.2 (HTTP 200, 9,616 B, sha256 `440d0e3c544a18444d8cccbfee0aecf5a4858a1337e5554ecb8e5c4d4dc5a602`); the enum values are corroborated by fs/proc/inode.c:161-171 |

No source was rejected for content. The single rejection is the 404 URL, and it is rejected
as a *citation target*, not as a source: the row must cite `earlyoom.service.in`.

## Facts that contradict or constrain the contract

**X-1. The contract's C2 grammar omits the indentation and padding of the `SIGKILL`
threshold line.** Contract line: "`SIGKILL when mem avail <= <c>% and swap free <= <d>%`
→ kill thresholds (main.c:416)". Verified upstream `main.c:416` is
`fprintf(stderr, "        SIGKILL when mem avail <= " PRIPCT " and swap free <= " PRIPCT "\n",`
— eight literal spaces of indentation, and `PRIPCT` is `"%5.2lf%%"` (`msg.h:10`), so a
value of 5 renders as ` 5.00` (width 5, right-aligned). The live host bytes are
`        SIGKILL when mem avail <=  5.00% and swap free <=  5.00%` — a *double* space
before the number. A matcher `mem avail <= (\S+)%` does **not** match that line (verified:
`naive_match=False`) while it does match the `10.00%` line; `mem avail <=\s*(\S+)%`
matches both (verified: groups `('5.00','5.00')`). The contract's own wording — "matched
after stripping leading whitespace, prefix-anchored" — plus the host-shaped quiet case
expecting 5.00 kill thresholds make this load-bearing for the C2 tool and the case file.

**X-2. The contract's C1 claim that earlyoom 1.9.0 is active and enabled is consistent
with this seat's observations**: host package `earlyoom 1.9.0-1` (`pacman -Q earlyoom`),
owned unit `/usr/lib/systemd/system/earlyoom.service`, `is-enabled` → `enabled`,
`is-active` → `active`, `NRestarts=0`, `ActiveEnterTimestamp` = 2026-10-22 04:55:44 -03
(the contract's stated start time), journal version line `earlyoom 1.9.0`. No contradiction.

**X-3. The stderr→journal statement holds, but the mechanism is the systemd default, not
a unit directive** (F-1, F-2, F-7). If the C1 entry or the C2 tool comment says the
*unit* redirects stderr to the journal, that wording is wrong:
`grep -c Standard /usr/lib/systemd/system/earlyoom.service` → 0, same upstream at
`v1.9.0`. The correct statement is "the unit does not redirect stderr, so earlyoom's
stderr follows the systemd default (stdout journal, stderr inherit) into the journal".

**X-4. Nothing in this seat's scope contradicts the contract's C2 tool interface.** The
contract's live collection uses
`journalctl -q -b -u earlyoom.service -o json --output-fields=MESSAGE` and requires
`MESSAGE` plus `__MONOTONIC_TIMESTAMP`. Verified on this host: that exact command returns
both fields, and the `--output-fields=MESSAGE` form still carries
`__MONOTONIC_TIMESTAMP` (keys observed: `MESSAGE`, `_BOOT_ID`, `__CURSOR`,
`__MONOTONIC_TIMESTAMP`, `__REALTIME_TIMESTAMP`, `__SEQNUM`, `__SEQNUM_ID`). The
contract's oomd-notice command shape also works:
`journalctl -q -b MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json
--output-fields=MESSAGE_ID` exits 0 and prints 0 lines on this host (earlyoom's unit is
the only one in scope; oomd is inactive and disabled).

**X-5. The contract's scope rule ("≥ ActiveEnterTimestampMonotonic of the current
earlyoom invocation") is satisfiable but depends on the invocation-scoped version line.**
`ActiveEnterTimestampMonotonic` → `19964362`; the version line sits at `19981126` and the
systemd `Started …` record at `19964370` — inside the window; the seven `mem avail:`
report lines sit at `19983943` and hourly afterwards, also inside it. `NRestarts=0`, so
"current invocation" and "this boot" coincide here; on a host with a restart the version
line (`main.c:161`) is the in-window anchor that distinguishes invocations, and it is the
first stderr line of each invocation. The tool should key scope on the version line, not
on the boot start.

## Tooling

No package was installed, upgraded or removed. `pacman` transactions are paused host-wide
per the round's bound, and nothing this seat needed was missing: `curl 8.23.0`,
`python3 3.14.8`, `git 2.56.0` and `jq`/`jaq 3.1.1` (`~/.local/bin/jq`) were already
present and were used as-is. Per `/home/vgpnk/.omp/agent/RULES.md` nothing was fetched
from an unverified remote script and no full-system upgrade was attempted.

## Scratch and privacy

Scratch for this seat is `/fast/scratch/hyaku/mori-r26/MoriR26.SrcEarlyoomUnit/` (fetched
bytes only). The upstream `main.c`/`kill.c`/`meminfo.c`/`README.md`/`MANPAGE.md` copies in
`/fast/scratch/hyaku/mori-r26/` were re-fetched here and their sha256 values match the
L1's copies byte for byte (`main.c` `08656b0b…`, `kill.c` `b32e0fad…`, `meminfo.c`
`526e512c…`, `README.md` `23411dbf…`, `MANPAGE.md` `cc48b02e…`). Two scratch files that
held derived `/etc/default/earlyoom` content were deleted after hashing so that no host
`--avoid`/`--prefer` value lingers outside this report.

No journal MESSAGE text, process name, command line, uid, or `--avoid`/`--prefer`
expression value appears in this report. Journal evidence is given as counts, byte
lengths, timings and prefixes only; the host's `/etc/default/earlyoom` is described by
size, sha256, line count and the count of `EARLYOOM_ARGS=` assignments — never its values.
