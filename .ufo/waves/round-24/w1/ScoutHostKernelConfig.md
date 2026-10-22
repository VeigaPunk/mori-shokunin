# ScoutHostKernelConfig — host kernel PSI configuration (C2 / frontier FR12)

Seat: read-only scout `MoriR24.ScoutHostKernelConfig`. Host: `7.2.11-arch1-1`.
Read-only throughout: no writes to /proc, /sys or cgroup files, no PSI trigger registration,
no service/package change, no tool install or upgrade (nothing installed; nothing to record).
Only file created: this report.

## 1. Answer

| Question | Observed value | Where read |
|---|---|---|
| `CONFIG_PSI` | `=y` | `/proc/config.gz` (config embedded in the **running** kernel) |
| `CONFIG_PSI_DEFAULT_DISABLED` | `# CONFIG_PSI_DEFAULT_DISABLED is not set` | `/proc/config.gz` |
| `CONFIG_IRQ_TIME_ACCOUNTING` | `=y` | `/proc/config.gz` |
| `psi=` in `/proc/cmdline` | **absent** (0 matches) | `/proc/cmdline` (and the bootloader's configured cmdlines) |
| `/proc/pressure/{cpu,memory,io,irq}` | **all four exist**, mode `0666`, all readable | `ls -l /proc/pressure/` |

Net: PSI is compiled in, enabled at boot without any boot parameter, and IRQ-time accounting is
compiled in, so this host presents the full four-file `/proc/pressure` set. The `--selftest`
fixtures and the live host run of `tools/mori-pressure.py` both land on a host whose system PSI
surface is fully present (no `absent` / `unsupported` path is exercised by the live run).

## 2. Evidence — commands and outputs

### E1 running kernel's own config (`IKCONFIG_PROC=y`, so this is the booted kernel's config)

```
$ zcat /proc/config.gz | grep -E 'CONFIG_PSI|CONFIG_IRQ_TIME_ACCOUNTING|CONFIG_IKCONFIG|CONFIG_TASK_DELAY_ACCT|CONFIG_SCHED_INFO|CONFIG_CGROUP_SCHED'
CONFIG_IRQ_TIME_ACCOUNTING=y
CONFIG_TASK_DELAY_ACCT=y
CONFIG_PSI=y
# CONFIG_PSI_DEFAULT_DISABLED is not set
CONFIG_IKCONFIG=y
CONFIG_IKCONFIG_PROC=y
CONFIG_CGROUP_SCHED=y
CONFIG_SCHED_INFO=y
$ zcat /proc/config.gz | grep -E 'CONFIG_PREEMPT_RT|CONFIG_PREEMPT|CONFIG_HZ=|CONFIG_VIRT_CPU_ACCOUNTING'
CONFIG_PREEMPT_BUILD=y
CONFIG_PREEMPT=y
# CONFIG_PREEMPT_LAZY is not set
CONFIG_PREEMPT_COUNT=y
CONFIG_PREEMPTION=y
CONFIG_PREEMPT_DYNAMIC=y
CONFIG_VIRT_CPU_ACCOUNTING=y
CONFIG_VIRT_CPU_ACCOUNTING_GEN=y
CONFIG_IRQ_TIME_ACCOUNTING=y
CONFIG_PREEMPT_RCU=y
CONFIG_HZ=1000
```

### E2 three on-disk config copies, byte-identical to the running config

```
$ md5sum /usr/lib/modules/7.2.11-arch1-1/build/.config; zcat /proc/config.gz | md5sum
6e57d8197b25e8885ab23d4ea0201fbc  /usr/lib/modules/7.2.11-arch1-1/build/.config
6e57d8197b25e8885ab23d4ea0201fbc  -
$ md5sum /usr/src/linux/.config
6e57d8197b25e8885ab23d4ea0201fbc  /usr/src/linux/.config
$ grep -nE 'CONFIG_PSI|CONFIG_IRQ_TIME_ACCOUNTING|CONFIG_IKCONFIG' /usr/lib/modules/7.2.11-arch1-1/build/.config
161:CONFIG_IRQ_TIME_ACCOUNTING=y
169:CONFIG_PSI=y
170:# CONFIG_PSI_DEFAULT_DISABLED is not set
207:CONFIG_IKCONFIG=y
208:CONFIG_IKCONFIG_PROC=y
$ grep -E 'CONFIG_(PSI|IRQ_TIME_ACCOUNTING|IKCONFIG|VIRT_CPU_ACCOUNTING)' /usr/src/linux/include/generated/autoconf.h
#define CONFIG_IKCONFIG 1
#define CONFIG_VIRT_CPU_ACCOUNTING 1
#define CONFIG_PSI 1
#define CONFIG_IKCONFIG_PROC 1
#define CONFIG_IRQ_TIME_ACCOUNTING 1
#define CONFIG_VIRT_CPU_ACCOUNTING_GEN 1
```

The Arch `linux` package ships no `config-*` file (`pacman -Ql linux | grep -i config` lists only
`.ko` files plus `pkgbase`/`vmlinuz`), and `/boot` holds no `config-7.2.11-arch1-1`
(`sudo -n ls -la /boot` → `amd-ucode.img`, `EFI/`, `limine.conf`, `limine.conf.old`, `loader/`,
`432d02b544a5459ebbff9c42ec68334d/limine_history`, nothing else). The four config sources above
(`/proc/config.gz`, `linux-headers` `.config`, `/usr/src/linux/.config`, generated
`autoconf.h`/`auto.conf`) are the available ones, and they agree.

### E3 boot parameters

```
$ uname -r
7.2.11-arch1-1
$ cat /proc/cmdline
resume=/dev/mapper/root resume_offset=3795013 quiet splash loglevel=0 systemd.show_status=false rd.udev.log_level=0 vt.global_cursor_default=0 cryptdevice=PARTUUID=cf3d875f-72a4-4468-9795-015c9e953618:root:allow-discards,no-read-workqueue,no-write-workqueue root=/dev/mapper/root zswap.enabled=1 zswap.max_pool_percent=25 rootflags=subvol=@ rw rootfstype=btrfs
$ grep -c 'psi=' /proc/cmdline
0
$ md5sum /proc/cmdline
ecace254fc5680e70712d46226bf7aca  /proc/cmdline
```

The parameter is not merely dropped: all five configured cmdlines in `/boot/limine.conf`
(lines 31, 39, 51, 57, 65, read via `sudo -n grep`) are the same string and none contains `psi=`,
and the running kernel does accept the parameter (`strings -a /usr/src/linux/vmlinux | grep -n -F 'psi='`
finds it once, at index 554487, between `nohz_full=` and `relax_domain_level=` — i.e. it is
registered in the sched boot-parameter table).

### E4 the runtime surface

```
$ ls -la /proc/pressure/
total 0
dr-xr-xr-x    2 root root 0 Oct 22 04:55 .
dr-xr-xr-x 1729 root root 0 Oct 22 04:55 ..
-rw-rw-rw-    1 root root 0 Oct 22 04:55 cpu
-rw-rw-rw-    1 root root 0 Oct 22 04:55 io
-rw-rw-rw-    1 root root 0 Oct 22 05:15 irq
-rw-rw-rw-    1 root root 0 Oct 22 04:55 memory
$ for f in cpu memory io irq; do echo "== /proc/pressure/$f"; cat /proc/pressure/$f; done
== /proc/pressure/cpu
some avg10=0.00 avg60=0.00 avg300=0.00 total=1220326
full avg10=0.00 avg60=0.00 avg300=0.00 total=0
== /proc/pressure/memory
some avg10=0.10 avg60=0.20 avg300=0.10 total=1530827
full avg10=0.10 avg60=0.20 avg300=0.10 total=1513266
== /proc/pressure/io
some avg10=4.33 avg60=4.39 avg300=3.34 total=24847374
full avg10=4.28 avg60=4.32 avg300=3.27 total=24541577
== /proc/pressure/irq
full avg10=0.01 avg60=0.02 avg300=0.02 total=5373007
```

Three observations that matter to the C2 tool's grammar and to the frozen cases:

* `/proc/pressure/irq` emits **only** the `full` line — the contract's "irq needs `full` only,
  `some: null`, never malformed" (case P03) matches the real host.
* `/proc/pressure/cpu` emits both lines, and `full total=0` while `some total=1220326`: the
  system-wide CPU `full` line exists but carries no accumulated stall, consistent with the
  contract's `full_system_undefined: true` labelling of system `cpu` `full` (case P02 injects the
  nonzero variant, which the host does not currently produce).
* All four files are mode `0666` and size 0: any user may open them for write, which is the
  trigger-registration path the lane's "never register PSI triggers" bound exists to prevent.

### E5 PSI code is in the running kernel image, including the irq resource

```
$ grep -aE '\b(psi_[a-zA-Z0-9_]+|irqtime_account_irq|irqtime_account_process_tick)\b' /proc/kallsyms | sort -u -k3
... psi_proc_init t ... psi_cpu_proc_ops d ... psi_memory_proc_ops d ... psi_io_proc_ops d ...
    psi_irq_proc_ops d ... psi_irq_open t ... psi_irq_show t ... psi_irq_write t ...
    psi_disabled B ... psi_cgroups_enabled t ... psi_account_irqtime T ... irqtime_account_irq T ...
$ strings -a /usr/src/linux/vmlinux | grep -c -F 'pressure/irq'   # 1  (also pressure/cpu, memory, io: 1 each)
```

(kptr_restrict is 0 but addresses print as zero for this unprivileged reader; only the names are
used here.) `/usr/src/linux/vmlinux` is `not stripped`, built `7.2.11-arch1-1 ... gcc (GCC) 16.2.1
20260810 ... #1 SMP PREEMPT_DYNAMIC Fri, 16 Oct 2026 00:28:58 +0000` — the same build stamp as
`/proc/version`, and its `.config` hashes equal to the running config (E2).

### E6 the compile-time gate for the irq resource, from this host's own headers

`/usr/src/linux/include/linux/psi_types.h:40-48`:

```c
enum psi_res {
	PSI_IO,
	PSI_MEM,
	PSI_CPU,
#ifdef CONFIG_IRQ_TIME_ACCOUNTING
	PSI_IRQ,
#endif
	NR_PSI_RESOURCES,
};
```

and `psi_types.h:63-66` gates the matching state:

```c
	PSI_CPU_FULL,
#ifdef CONFIG_IRQ_TIME_ACCOUNTING
	PSI_IRQ_FULL,
#endif
```

`/usr/src/linux/include/linux/psi.h:17` declares the runtime gate:
`extern struct static_key_false psi_disabled;` (the `psi_disabled` BSS symbol in E5).

## 3. What each value implies for which /proc/pressure files exist

* `CONFIG_PSI=y` — the subsystem is compiled in, and its proc init creates the directory. Local
  Kconfig help text, `/usr/src/linux/init/Kconfig:735-742`: "If you say Y here, the kernel will
  create /proc/pressure/ with the pressure statistics files cpu, memory, and io. … In kernels with
  cgroup support, cgroups (cgroup2 only) will have cpu.pressure, memory.pressure, and io.pressure
  files". `CONFIG_PSI=n` ⇒ no `/proc/pressure` directory at all ⇒ all four reads `ENOENT`, i.e.
  state `absent` for every resource (the tool's `PRESSURE_UNAVAILABLE`, exit 2).
* `CONFIG_PSI_DEFAULT_DISABLED` — `default n` (`init/Kconfig:748-751`). It is **not set** here, so
  PSI is on at boot with no parameter. Its help text (`init/Kconfig:753-755`): "If set, pressure
  stall information tracking will be disabled per default but can be enabled through passing psi=1
  on the kernel commandline during boot." Had it been set with this cmdline, `/proc/pressure`
  would not be created at all — again all four `ENOENT`/`absent`, indistinguishable at runtime from
  `CONFIG_PSI=n`. This is why the config read is the only way to tell "compiled out" from
  "compiled in but disabled".
* `psi=` on the cmdline — **absent**, so the default (enabled) applies. `psi=0` would disable PSI
  at boot; `psi=1` is the enable switch needed only when `CONFIG_PSI_DEFAULT_DISABLED=y`. The
  running kernel does parse it (E3), so absence is a deliberate host configuration, not a
  parameter the kernel would ignore.
* `CONFIG_IRQ_TIME_ACCOUNTING=y` — `PSI_IRQ` / `PSI_IRQ_FULL` exist in this build (E6) and the irq
  proc ops are in the running image (E5), which is why `/proc/pressure/irq` is present and carries
  only the `full` line (there is no `some` state for IRQ by construction — E6 shows `PSI_IRQ_FULL`
  and no `PSI_IRQ_SOME`). With this option off, the IRQ resource does not exist at compile time, so
  `cpu`/`memory`/`io` would still be present while `/proc/pressure/irq` would not be created — the
  `PRESSURE_PARTIAL` shape of frozen case P04 (irq absent, exit 0).
  *[INFERENCE — the exact `#ifdef CONFIG_IRQ_TIME_ACCOUNTING` wrapping the `proc_create("pressure/irq", …)`
  call lives in `kernel/sched/psi.c`, which is not on this host (E7); the compile-time non-existence
  of the resource is observed directly in the local header, and the file's presence on this host is
  observed directly.]*
* Per-resource summary for this host: `cpu` — exists, both kinds, `full` undefined system-wide;
  `memory` — exists, both kinds; `io` — exists, both kinds; `irq` — exists, `full` only.

## 4. Adjacent observations (cgroup2, not part of the C2 tool's scope)

```
$ ls -l /sys/fs/cgroup/user.slice/ | grep pressure
-rw-r--r--  cgroup.pressure
-rw-r--r--  cpu.pressure
-rw-r--r--  io.pressure
-rw-r--r--  irq.pressure
-rw-r--r--  memory.pressure
$ cat /sys/fs/cgroup/user.slice/irq.pressure
full avg10=0.00 avg60=0.00 avg300=0.00 total=5355460
$ cat /sys/fs/cgroup/user.slice/cgroup.pressure
1
```

* This host exposes a per-cgroup `irq.pressure` (and `cgroup.pressure`, `cpu.pressure`,
  `io.pressure`, `memory.pressure`) at `/sys/fs/cgroup` and in `user.slice`; all 47 scanned
  `cgroup.pressure` files under `/sys/fs/cgroup` (depth ≤ 3) read `1`, i.e. per-cgroup PSI is
  enabled everywhere I looked. Cgroup files are mode `0644` root-owned, in contrast to the
  world-writable `0666` `/proc/pressure/*`.
* Consequence for the frozen fixtures: no `EOPNOTSUPP` (state `unsupported`) can be observed on
  this host without writing (either a `cgroup.pressure=0` cgroup or a `psi=0` reboot), so the
  `unsupported` branch is exercised only by the selftest's in-process open hook (cases P05).
  I did not create such a cgroup — that would be a host write.

## 5. Not run / unresolved

* No live run of `tools/mori-pressure.py` (executor's seat) and no trigger registration, no
  /proc, /sys or cgroup write of any kind.
* `/sys/kernel/notes` is not ELF (`readelf: Error: Not an ELF file - it has the wrong magic bytes`),
  so the running image's GNU build-id could not be compared with `vmlinux`'s
  `1e38049adb503fbd3a6552a982bd2d91fe8786ca`. Running-kernel identity rests instead on
  `/proc/config.gz` (embedded in the booted kernel by `CONFIG_IKCONFIG_PROC=y`) plus the identical
  version/build stamp in `/proc/version` and `/usr/src/linux/vmlinux`.
* `kernel/sched/psi.c`, `Documentation/accounting/psi.rst` and
  `Documentation/admin-guide/kernel-parameters.txt` are **not present** on this host:
  `/usr/src/linux` is a pruned artifact tree (it has `vmlinux`, `System.map`, `Module.symvers`,
  `.config`, headers and Kconfig files, but `kernel/` holds only `Kconfig.*` files and no `sched/`).
  Source-level quotation of the `psi=` parameter and of the `pressure/irq` creation site is
  therefore out of reach locally and is left to the seats that cite `SOURCES.md` rows.
* No package installed or upgraded, so nothing to record under the tooling directive.
