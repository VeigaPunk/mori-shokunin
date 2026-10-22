# Re-open S120 + S126 — wave 2, seat MoriR26.ReopenS120S126

Rev under attack: 16935e24c93fa7e7567413d7ec091339a5df1474 (read via `git show`, working tree never trusted).
Rows read from `git show 16935e24…:corpus/SOURCES.md` lines 126 (S120) and 132 (S126); columns per registry header (SOURCES.md:4): id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by.
Fetches by ordinary means (curl); scratch under /fast/scratch/hyaku/mori-r26/MoriR26.ReopenS120S126/.
No tools installed; no pacman transactions run.

## S120 — earlyoom.service.in at v1.9.0 (SOURCES.md:126)

URL: https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.service.in

- HTTP 200; downloaded 1,340 B — row says 1,340 B. MATCH.
- sha256 d4019b66d87539a006fc2d178d972dcf1b46e70343627b8bf66d1a08dcdda0bd — row: same. MATCH.
- Anchor line numbers, all verified against fetched bytes (`grep -n` on earlyoom.service.in):
  :6 EnvironmentFile=-:SYSCONFDIR:/default/earlyoom ✓; :7 ExecStart=:TARGET:/earlyoom $EARLYOOM_ARGS ✓; :9 AmbientCapabilities=CAP_KILL CAP_IPC_LOCK ✓; :10 CapabilityBoundingSet=CAP_KILL CAP_IPC_LOCK ✓ (see minor note); :12 Nice=-20 ✓; :14 OOMScoreAdjust=-100 ✓; :17 Restart=always ✓; :19 TasksMax=10 ✓; :20 MemoryMax=50M ✓; :25 DynamicUser=true ✓; :27 ProtectSystem=strict ✓; :29 ProtectHome=true ✓; :33 ProtectKernelLogs=true ✓; :35 ProtectKernelTunables=true ✓; :36 ProtectControlGroups=true ✓; :41 IPAddressDeny=any ✓; :43 dbus-send comment ✓ / :44 RestrictAddressFamilies=AF_UNIX ✓; :46 SystemCallArchitectures=native ✓; :47 SystemCallFilter=@system-service process_mrelease ✓; :48 SystemCallFilter=~@privileged ✓.
- Negative anchor "no StandardOutput= or StandardError= line anywhere in the file": `grep -cE 'Standard(Out|Err)='` = 0. HOLDS.
- Gate quote (corpus/lessons/round-26.md:73): `:7 "ExecStart=:TARGET:/earlyoom $EARLYOOM_ARGS"` — byte-exact line 7 of fetched file (`grep -Fxc` = 1); located; 2 words ≤ 25. HOLDS.
- Tier: row kind=code, tier=A; Gate row says A (round-26.md:73). MATCH.
- Status: mined; opened 2026-10-22; recheck on-release. As claimed.
- Used-by: corpus/knowledge/userspace-oom-killers-r26.md cites S120 in its source line (file line 1), naming the same URL. HOLDS.

Minor note (not a defect): the anchor note renders line 10 as "CapabilityBoundingSet=" with the value omitted; the actual line is `CapabilityBoundingSet=CAP_KILL CAP_IPC_LOCK`. Line number and directive correct; note under-specifies the value.

**Verdict S120: holds.**

## S126 — Arch PKGBUILD, commit 704e057 (SOURCES.md:132)

URL: https://gitlab.archlinux.org/archlinux/packaging/packages/earlyoom/-/raw/704e05715e672b5de664d543e734aa3f757af9bb/PKGBUILD

- HTTP 200; downloaded 1,179 B — row says 1,179 B. MATCH.
- sha256 f48dc3f99aee5d6a93f8cad4e4b6286dab014745aa6f85b1c3582c3db46dd4a2 — row: same. MATCH.
- Anchor line numbers, all verified against fetched bytes:
  :5 pkgver=1.9.0 ✓; :6 pkgrel=1 ✓; :14 backup=("etc/default/earlyoom") ✓; :20 `sed "/systemctl|chcon/d" -ri Makefile` (strips systemctl/chcon lines) ✓; :21 `sed '/^DynamicUser=/a SupplementaryGroups=proc' -i earlyoom.service.in` (adds group after DynamicUser=) ✓; :22 sed appends `-n --avoid '(^|/)(init|systemd|Xorg|sshd)$'` to EARLYOOM_ARGS in earlyoom.default ✓; :27 build `make … SYSTEMDUNITDIR=/usr/lib/systemd/system VERSION=$pkgver` ✓; :32 install with same SYSTEMDUNITDIR ✓.
- Gate quote (corpus/lessons/round-26.md:79): `:5-6 "pkgver=1.9.0" / "pkgrel=1"` — both strings byte-exact at lines 5 and 6 of fetched file (`grep -Fxq`); located; 2 words ≤ 25. HOLDS.
- Tier: row kind=code, tier=A; Gate row says A (round-26.md:79). MATCH.
- Status: mined; opened 2026-10-22; recheck on-release. As claimed.
- Used-by: corpus/knowledge/userspace-oom-killers-r26.md cites S126 in its source line (file line 1). HOLDS.

Minor note (not a defect): the used-by citation describes the source via the GitLab repo root rather than the pinned raw-commit URL the row registers; the row id S126 is cited and the row itself carries the pin, so no contract check fails.

**Verdict S126: holds.**

## Residual risk / not run

- Both fetches were live-web re-openings on 2026-10-22; upstream could change after this fetch (raw tag URL and pinned-commit URL both currently return the registered bytes).
- Tag-to-commit pin for v1.9.0 = 202d4db0d308ca6478f68de68b46cae34896ddaf (round-26.md:60-61) not independently re-resolved; the row URL fetches via the tag.
- Gate table's other columns (seat names, admit decisions) not re-audited — outside this seat's scope.
