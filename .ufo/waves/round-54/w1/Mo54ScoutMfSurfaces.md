# Mo54ScoutMfSurfaces — memory-error boundary reconnaissance

## Scope and evidence

Detection/report only. No host settings, sysctls, memory, or trace state were changed. Linux v7.3 source copies were fetched from `git.kernel.org` into the seat scratch directory. Relevant source URLs and cited source paths are below. The local host runs `7.2.11-arch1-1`.

## Observed facts

- **MCE-to-memory-failure handoff (v7.3):** `arch/x86/kernel/cpu/mce/core.c` calls `trace_mce_record(err)` in `mce_early_notifier`; the `mce:mce_record` trace event (`include/trace/events/mce.h`) carries structured MCE fields including status, address, CPU, bank, time, socket and vendor. For usable-address AO/deferred severity, `uc_decode_notifier` calls `memory_failure(pfn, 0)`. For user-mode action-required faults, `do_machine_check` queues `kill_me_maybe`; that calls `memory_failure(pfn, MF_ACTION_REQUIRED)`. `kill_me_maybe` emits an `pr_err` line before the handler; MCE decoding also logs `[Hardware Error]: Machine Check...` records via `print_mce`. The MCE record/trace and the printk are not proof that a process was killed.
- **Prefix distinction:** `include/linux/printk.h` defines `HW_ERR` as `[Hardware Error]: `. `arch/x86/kernel/cpu/mce/internal.h` sets `pr_fmt(fmt)` to `mce: `, so ordinary `pr_err` calls in MCE core (including `kill_me_maybe`) have the `mce:` prefix. The later `memory_failure()` handler has its own `Memory failure:` prefix. These are text logs, not a structured count; do not count matching log lines as events.
- **Other MCE and EDAC structured paths:** `include/ras/ras_event.h` defines `ras:mc_event`, with structured error type/count, memory-controller index, location, address, syndrome, label and driver detail; `include/trace/events/mce.h` defines `mce:mce_record`. EDAC ABI `Documentation/ABI/testing/sysfs-devices-edac` describes cumulative per-controller `ue_count`/`ce_count` and per-DIMM counts. These are candidate structured surfaces for hardware-error detection, not memory-failure kill counts. `Documentation/ABI/testing/sysfs-mce` describes `machinecheckX/trigger` as a program-to-run control, not an event counter. `rasdaemon` is a userspace consumer/recorder candidate, not an admitted source here.
- **GHES route:** v7.3 `drivers/acpi/apei/ghes.c` has `ghes_do_memory_failure`, which can queue `memory_failure`; its task-work fallback logs and calls `force_sig(SIGBUS)`. This is another firmware-first route into the class and not an MCE-only phenomenon.
- **Userspace signal code:** v7.3 `include/uapi/asm-generic/siginfo.h` assigns `BUS_MCEERR_AR=4` and `BUS_MCEERR_AO=5`. `memory-failure.c` passes AR to `force_sig_mceerr` for the current action-required task, AO to `send_sig_mceerr` for another eligible mapper. The code is available to a userspace `SA_SIGINFO` handler via `siginfo_t.si_code`; a receiver can classify it while handling the signal. Plain `force_sig(SIGBUS)` paths, including the GHES fallback, are not evidence of those BUS_MCEERR codes. Exact `si_code` for plain-force paths was not independently traced here.
- **systemd-coredump:** host systemd is 262. The active `core_pattern` passes `%s` (signal number), and local `systemd-coredump` strings plus an actual journal JSON record show `COREDUMP_SIGNAL` and `COREDUMP_SIGNAL_NAME`; the inspected record has no `SI_CODE`/`COREDUMP_SI_CODE` field. `man 5 core` documents `%s` as the signal number and provides no `si_code` specifier. Thus journal/coredump metadata can count SIGBUS deaths as SIGBUS, but cannot distinguish `BUS_MCEERR_AR/AO` from other SIGBUS causes on observed systemd.
- **Host observations:** `coredumpctl list` showed SIGBUS entries; `journalctl` filtered by systemd's coredump `MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1` and `COREDUMP_SIGNAL=7` returned 5 matching messages in the current boot and 12 across retained journal. These are SIGBUS coredumps, not attributed to hardware poison. Kernel journal searches for `Hardware Error` and `Memory failure` returned no entries; EDAC search found only `EDAC MC: Ver: 3.0.0`. `/proc/interrupts` showed MCE counts zero and MCP polling counts 152 on each listed CPU. `/sys/devices/system/edac/mc/` had no `mc*` controller directories. No `/var/lib/rasdaemon`, `rasdaemon`, `ras-mc-ctl`, `mcelog`, `trace-cmd` or `perf` executable was found. ACPI table listing had no HEST/BERT/EINJ. Tracefs is mounted but reading its event paths was denied, so host tracepoint presence/format is UNVERIFIED.

## Structured-count answer

The clearest **non-text structured signals** are the kernel tracepoints (`mce:mce_record`, `ras:mc_event`, and the entry's `ras:memory_failure_event`) and cumulative EDAC/sysfs counters. A resident tracing consumer can count trace events; a configured `rasdaemon` can persist RAS records. Those count MCE/EDAC/memory-failure events, not necessarily process deaths. `siginfo_t.si_code` is structured and distinguishes action-required/optional hardware SIGBUS for a handler that receives the signal, but it is not exposed as a countable systemd journal field on the inspected system. `COREDUMP_SIGNAL=7` is structured but only counts SIGBUS coredumps, not hardware-origin SIGBUS specifically. None of the observed host SIGBUS coredumps can be attributed to memory failure from those fields alone.

## Proposed lead rows (not admitted claims)

| URL / source | What it would teach |
|---|---|
| `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/arch/x86/kernel/cpu/mce/core.c?h=v7.3` | MCE print path, trace emission, `memory_failure` handoff, and task-work SIGBUS routes. |
| `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/trace/events/mce.h?h=v7.3` | Structured fields and identity of `mce:mce_record`. |
| `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/ras/ras_event.h?h=v7.3` | `ras:mc_event` structured EDAC event fields; separate corrected/uncorrected hardware-error accounting from kill counts. |
| `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/ABI/testing/sysfs-devices-edac?h=v7.3` | Meaning and scope of EDAC UE/CE cumulative counters, where controllers expose them. |
| `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/ABI/testing/sysfs-mce?h=v7.3` | MCE sysfs controls and why `trigger` is not a counter. |
| `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/drivers/acpi/apei/ghes.c?h=v7.3` | Firmware-first GHES path can call memory failure and signal independently of x86 MCE path. |
| `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/uapi/asm-generic/siginfo.h?h=v7.3` | Numeric BUS_MCEERR_AR/AO `si_code` values exposed to signal recipients. |
| `https://github.com/mchehab/rasdaemon` | Userspace RAS collector/recording and operational prerequisites; contents/schema need independent source review before any claim. |
| `https://www.freedesktop.org/software/systemd/man/latest/systemd-coredump.html` and local `man 5 core` | Coredump journal fields/metadata boundary: signal number is present; no `si_code` field or `%` specifier established here. |

## Evidence commands / limits

- `uname -r` → `7.2.11-arch1-1` (exit 0).
- `cat /proc/sys/kernel/core_pattern` → `|/usr/lib/systemd/systemd-coredump %P %u %g %s %t %c %h %d %F %I` (exit 0).
- `coredumpctl list --no-pager` → SIGBUS entries present (exit 0).
- `journalctl MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1 COREDUMP_SIGNAL=7 ... -o json` → fields include `COREDUMP_SIGNAL`, `COREDUMP_SIGNAL_NAME`; no `SI_CODE`/`COREDUMP_SI_CODE` (exit 0).
- `journalctl -k -g 'Hardware Error' ...` and `-g 'Memory failure'` → `-- No entries --` (exit 1 for no match).
- `ls /sys/devices/system/edac/mc/` → only no controller child directories (exit 0); `ls /var/lib/rasdaemon` → absent (exit 2).
- `ls /sys/kernel/tracing/events/ras/` → Permission denied (exit 2); trace formats UNVERIFIED.
- No tools installed/updated.
- Scratch sources and temporary files were under `/fast/scratch/hyaku/mori-r54/Mo54ScoutMfSurfaces`; cleaned before completion.

## Findings

- **MED — `corpus/knowledge/memory-failure-kills-r54.md`, boundaries at lines 81–82:** useful adjacent class, but MCE/EDAC corrected-error logging and counters, rasdaemon persistence, and the upstream MCE/GHES handoff are intentionally outside the current entry. Consider separate hardware-health/detection leads; do not treat these as additional kill counters without defining their event semantics.
- **MED — `corpus/knowledge/memory-failure-kills-r54.md`, lines 55–57:** SIGBUS/SIGKILL printk attribution remains text; structured coredump signal number does not carry `si_code`. The wave's caution against text tally remains necessary.
- **LOW — host observability:** no EDAC memory-controller instance or rasdaemon store was observed; tracefs formats were inaccessible. Live structured event availability/counting on this host is therefore UNVERIFIED.
