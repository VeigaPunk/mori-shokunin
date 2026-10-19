source: S002 — https://docs.kernel.org/admin-guide/cgroup-v2.html — current cgroup-v2 docs, `memory.events`/`memory.events.local` OOM fields (opened 2026-10-19); S003 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c — v7.2 kernel OOM counter site lines 935–936; S007 — https://www.freedesktop.org/software/systemd/man/latest/systemd-oomd.service.html — systemd 262 Description; S011 — https://raw.githubusercontent.com/systemd/systemd/v261/src/oom/oomd-util.c — v261 `oomd_cgroup_kill` lines 269–316; S012 — https://github.com/systemd/systemd/security/advisories/GHSA-652q-wxr6-h5j6 — advisory published 2026-08-10, patch section; S013 — https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in — catalog at commit cf8ebfc6 `d989611b…` line 884; S016 — https://raw.githubusercontent.com/rfjakob/earlyoom/8477c902fce09be26e5668acba05df216871e7ae/README.md — README at commit 8477c902 signal/logging and `--kernel-oom` sections
verified-at: 2026-10-19 (lane base 20e2255; host kernel 7.2.3-arch1-3, systemd 261 (261.2-1-arch))
recheck: curl -fsSL https://raw.githubusercontent.com/systemd/systemd/v261/src/oom/oomd-util.c | grep -nE '"user\.oomd_(ooms|kill)"'; curl -fsSL https://raw.githubusercontent.com/rfjakob/earlyoom/8477c902fce09be26e5668acba05df216871e7ae/README.md | grep -cF 'kernel-oom'; curl -fsSL https://raw.githubusercontent.com/rfjakob/earlyoom/8477c902fce09be26e5668acba05df216871e7ae/README.md | grep -cF 'sending SIG'; systemctl is-active systemd-oomd.service; systemctl is-active earlyoom.service; journalctl --system -q MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json --output-fields=_BOOT_ID | wc -l; journalctl --user -q MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json --output-fields=_BOOT_ID | wc -l → 269: user.oomd_ooms; 306: user.oomd_kill; 1; 2; inactive; inactive; 0; 0

## Claim
systemd-oomd v261 records its cgroup kills in `user.oomd_ooms` (one per oomd kill attempt) and `user.oomd_kill` (number of PIDs killed), emits D-Bus `Killed(path, reason)`, and has the catalog notice `d989611b…`. These userspace kill paths do not increment the kernel OOM counters. earlyoom normally sends SIGTERM and then SIGKILL and logs its own actions; only `--kernel-oom` delegates to the kernel OOM killer. On this host both services are inactive, so a probe must render `unavailable (inactive)`, never a zero-kill result.

Adjacent: `tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md:344–346,353–367` owns host/service-state diagnosis and documents read-only detection surfaces. The `systemctl` readings here are a 2026-10-19 availability snapshot only; mori's claim is the fleet-facing rule `unavailable (inactive)`, not an OS/unit diagnosis.

## Evidence
- S011, v261 `oomd-util.c:269`: `increment_oomd_xattr(ctx->path, "user.oomd_ooms", 1)`; `:274–280` uses the cgroup kill helper and fallback; `:306` adds killed PIDs to `user.oomd_kill`; `:316–319` emits D-Bus `Killed(path, reason)`.
- S007, systemd 262 Description, says systemd-oomd “send[s] `SIGKILL` to all processes” in the selected cgroup. S013 `catalog/systemd.catalog.in:884–885` identifies `d989611b15e44c9dbf31e3c81256e4ed` as a unit notice for one or more oomd-killed processes.
- S016, README master:55–56 and `:148–149` documents ordinary SIGTERM/SIGKILL stages; `:157` says each action is logged to stderr; `:68–69` documents the `--kernel-oom` delegation exception.
- Host state: `systemctl is-active systemd-oomd.service` → `inactive`; `systemctl is-enabled systemd-oomd.service` → `disabled`; `systemctl is-active earlyoom.service` → `inactive`; `systemctl is-enabled earlyoom.service` → `not-found`.
- OOMD notice counts: `journalctl --system -q MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json --output-fields=_BOOT_ID | wc -l` → `0`; `journalctl --user -q MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json --output-fields=_BOOT_ID | wc -l` → `0`. These field-limited, count-only queries never emit journal `MESSAGE` text.

## Observed
The v261 source writes the two cgroup xattrs around oomd's kill operation and emits the D-Bus signal. Both service units are inactive; oomd is disabled and earlyoom's service unit is not found. The host has zero retained d989611b notices in each queried journal scope; that is not a historical-kill conclusion.

## [INFERENCE]
Because oomd acts through cgroup kill/signal paths instead of `__oom_kill_process`, its actions do not increment the kernel OOM counters described in `oom-kill-counter-kernel-only-r12.md`. A detector that cannot observe an inactive killer must report unavailable, not a healthy zero. The xattrs are attached to the target cgroup path and may cease to be available after cgroup removal; that lifetime behavior was not measured here.

## [UNKNOWN]
No oomd xattrs were read and no D-Bus listener was run. Whether an oomd D-Bus signal is observed depends on a resident listener; earlyoom's human-readable action lines are not a stable `MESSAGE_ID` class. Historical activity while either service was inactive is not inferred. GHSA-652q-wxr6-h5j6 is adjacency only: patch-state assessment belongs to tsukuroi and is not absorbed by this entry.

## What it changes for mori
For the SKILL.md `Did something get killed?` decision row (`:17`), use distinct oomd/earlyoom evidence, not `oom_kill`. For the `CGROUP_OOM_KILL` error-pattern row (`:28`) and `unavailable ≠ unhealthy` rule (`:54`; `:51` at base `20e2255`), keep inactive service state as `unavailable (inactive)`, never `0` kills. Round 12 folded this into SKILL.md as the `oom_kill=0` error-pattern row (`:29`).

## Delivery paths this cannot see
The oomd xattrs are cgroup-scoped and not a durable event log; D-Bus requires a listening consumer; the d989611b journal notice is limited by journal scope, retention, and access. earlyoom exposes its own action log (stderr / its unit journal when run under a service), not oomd xattrs or kernel OOM counters. These surfaces do not observe other userspace killers or arbitrary process termination.

## Fills (coverage-map ground; Frontier row)
Coverage-map ground: userspace-killer accounting and its unavailable state. Frontier F1: systemd-oomd xattrs / D-Bus / catalog notice and earlyoom action records; GHSA patch-state adjacency remains with tsukuroi.
