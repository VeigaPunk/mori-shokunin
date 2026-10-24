# LivePressureCapture — this host's live pressure interface (claim C2 surface)

Seat: `MoriR24.LivePressureCapture` (read-only executor leaf). Claim C2, surface arm
only: what this host actually exposes at the PSI interface, captured as bytes with
timestamps, plus a live run of the C2 tool once it landed.

Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Lane HEAD at capture start: `f7eb430` — *"round-24: contract amendment A1 (R2 scan
scope) before the C1 tool lands"*.
Lane HEAD at capture end: `06a7686` — *"round-24: freeze-order measurement register
copy for C2"*; the C2 tool is commit `6ee6248`, the frozen cases are commit
`f6a2970`, both verified ancestors of that HEAD with
`git merge-base --is-ancestor`.
Host: `plazir27`, kernel `7.2.11-arch1-1`, x86_64, btrfs root.
Capture window (UTC): **2026-10-22T08:16:37.723144Z → 2026-10-22T08:37:33.013335Z**.

Writes made by this seat: **this report only**, plus scratch under
`/fast/scratch/hyaku/mori-r24-a2/livepressure/`. Nothing under `/proc`, `/sys`, any
cgroup, any service, or any package manager was written. No PSI trigger was
registered. No file in the lane repo other than this report was created or modified
(no `git add`/`commit`/`stash`/`checkout`/`reset`/`pull`/`push`, no mutating `jj`).
The C2 tool was run read-only against the host; it writes nothing.

Tooling: **none installed or upgraded**. The capture used only pre-existing
coreutils (`cat`, `od`, `stat`, `ls`, `grep`, `uname`, `zcat`) and the pre-existing
`/usr/bin/python3` (3.14). The pacman guard was not touched: no pacman transaction
of any kind was attempted, so no install/upgrade record is owed.

## 1. Answer in one line

This host has **full system PSI enabled and healthy**: all four
`/proc/pressure/{cpu,io,irq,memory}` files exist, parse cleanly under the contract's
grammar, expose the expected kinds (`irq` carries `full` only, no `some`), and
`/sys/fs/cgroup/*.pressure` at the cgroup root reads **byte-identical to the system
files** for the same resource when both are read in the same process;
`CONFIG_PSI=y`, `CONFIG_PSI_DEFAULT_DISABLED` is not set,
`CONFIG_IRQ_TIME_ACCOUNTING=y`, and there is **no `psi=` token on
`/proc/cmdline`** — so PSI is on by default, not by an explicit boot switch. The
landed C2 tool reproduces all of this: `--selftest` prints
`MORI_PRESSURE_SELFTEST: PASS 12/12` (exit 0) and a live run prints
`"verdict": "PRESSURE_OK"` with `irq.some = null` and `cpu.full_system_undefined =
true` (exit 0).

## 2. Kernel and PSI enablement

| item | value | source |
|---|---|---|
| `uname -r` | `7.2.11-arch1-1` | record 1 |
| `uname -a` | `Linux plazir27 7.2.11-arch1-1 #1 SMP PREEMPT_DYNAMIC Fri, 16 Oct 2026 00:28:58 +0000 x86_64 GNU/Linux` | record 2 |
| `CONFIG_PSI` | `=y` (config line 169) | records 19, 20, 22 |
| `CONFIG_PSI_DEFAULT_DISABLED` | `# CONFIG_PSI_DEFAULT_DISABLED is not set` (line 170) | records 22, 23 |
| `CONFIG_IRQ_TIME_ACCOUNTING` | `=y` (line 161) | records 19, 20, 22 |
| `CONFIG_HAVE_IRQ_TIME_ACCOUNTING` | `=y` (line 980) | record 22 |
| `psi=` on `/proc/cmdline` | **absent** — `grep -c 'psi='` printed `0` and exited 1 | records 24, 57, 58 |

Consequences that bear directly on the contract's mapping (`contract.md` C2):

- `/proc/config.gz` is present and readable (69 954 bytes, record 14;
  `CONFIG_IKCONFIG_PROC`), so the "compiled out" vs "disabled at boot" distinction
  is decidable from bytes on this host without guessing. The
  installed-kernel-config fallback is **not** available here:
  `/usr/lib/modules/7.2.11-arch1-1/config` does not exist (record 16, exit 2), so
  `/proc/config.gz` is the only in-host kernel-config source for this release.
- `CONFIG_PSI_DEFAULT_DISABLED` **not set** ⇒ the kernel default is *enabled*; the
  absence of `psi=` on the cmdline is therefore not a gap, it is the expected
  "default on" state. Had the symbol been set, PSI would be off unless `psi=1` were
  passed, and every `/proc/pressure/*` read would have been `ENOENT`.
- `CONFIG_IRQ_TIME_ACCOUNTING=y` is the prerequisite for the `irq` resource; its
  presence is consistent with `/proc/pressure/irq` existing and carrying a `full`
  line.

`/proc/cmdline` verbatim (records 12, 56):

```
resume=/dev/mapper/root resume_offset=3795013 quiet splash loglevel=0 systemd.show_status=false rd.udev.log_level=0 vt.global_cursor_default=0 cryptdevice=PARTUUID:...:root:allow-discards,no-read-workqueue,no-write-workqueue root=/dev/mapper/root zswap.enabled=1 zswap.max_pool_percent=25 rootflags=subvol=@ rw rootfstype=btrfs
```

Token inventory extracted from that line (record 25): `cryptdevice loglevel resume
resume_offset root rootflags rootfstype` — **no `psi=`** among them. `grep -o
'psi=[^ ]*'` found nothing (record 57, exit 1) and `grep -c 'psi='` printed `0`
(record 58, exit 1).

## 3. The four system PSI files (records 3–6)

Read at 2026-10-22T08:16:37.723981Z – .724888Z:

```
/proc/pressure/cpu
some avg10=0.18 avg60=0.03 avg300=0.00 total=1455783
full avg10=0.00 avg60=0.00 avg300=0.00 total=0

/proc/pressure/io
some avg10=1.07 avg60=3.90 avg300=3.68 total=29471300
full avg10=1.01 avg60=3.77 avg300=3.60 total=29076706

/proc/pressure/irq
full avg10=0.00 avg60=0.00 avg300=0.00 total=5908314

/proc/pressure/memory
some avg10=0.00 avg60=0.14 avg300=0.12 total=2035146
full avg10=0.00 avg60=0.12 avg300=0.11 total=2011665
```

Observations that constrain the implementation:

1. **`irq` has `full` and no `some`** — exactly the shape the contract says must be
   reported as `some: null`, *not* `malformed`. This host is the live instance of
   contract case **P03**. The `irq` file is a single line (53 bytes = `0o65`,
   `od -c` offset in record 34), so the missing `some` is a kernel property, not a
   truncation.
2. **`cpu.full` exists but its `total` is `0` and every average is `0.00`.** This is
   the kernel's documented behaviour for the *system* CPU `full` line: "full" means
   *all* non-idle tasks were stalled simultaneously, which at system scope is
   effectively never true, so the counter stays at zero. It is **not** evidence of
   health. The contract's rule — report it, label it `full_system_undefined: true`,
   never use it for a threshold, never read it as evidence of no stall — is exactly
   what this host requires. A tool that treated `cpu.full total=0` as "no CPU
   pressure" would be wrong here; a tool that treated it as a stall signal would
   also be wrong.
3. Every line matches the contract's grammar
   `^(some|full) avg10=D avg60=D avg300=D total=N$` with `D` decimal and `N` a
   non-negative integer. `od -c` (records 32–35) confirms the byte-exact shape: two
   space-separated tokens per line, single `\n` line terminators, no trailing
   whitespace, no extra fields, no CR.
4. **File modes are `0666`** (`-rw-rw-rw-`, uid 0 gid 0, size 0 — record 26). This
   matters for the contract's error mapping: `/proc/pressure/*` is world-writable on
   this kernel, so `EACCES` is *not* reachable for an unprivileged reader of these
   four paths — an `EACCES` result would indicate something other than the file's
   own mode. `/sys/fs/cgroup/cgroup.pressure` is `0444` (record 26).

## 4. The cgroup-v2 pressure files (records 7–11)

```
/sys/fs/cgroup/cpu.pressure
some avg10=0.18 avg60=0.03 avg300=0.00 total=1455783
full avg10=0.00 avg60=0.00 avg300=0.00 total=0

/sys/fs/cgroup/io.pressure
some avg10=1.07 avg60=3.90 avg300=3.68 total=29471300
full avg10=1.01 avg60=3.77 avg300=3.60 total=29076706

/sys/fs/cgroup/irq.pressure
full avg10=0.00 avg60=0.00 avg300=0.00 total=5908314

/sys/fs/cgroup/memory.pressure
some avg10=0.00 avg60=0.14 avg300=0.12 total=2035146
full avg10=0.00 avg60=0.12 avg300=0.11 total=2011665

/sys/fs/cgroup/cgroup.pressure
1
```

- **`cgroup.pressure` is a single byte `1\n`** (record 36, `od -c` → `1 \n`, 2
  bytes; the plain `cat` is record 11). It is *not* a `some`/`full` PSI line and
  does not parse under the contract's grammar. It is the cgroup-v2 "pressure
  accounting enabled" flag for that cgroup. Any parser that treats
  `cgroup.pressure` as a PSI resource line is wrong; it must be read as a flag.
- The **root** cgroup's `*.pressure` files are **byte-identical to the corresponding
  `/proc/pressure/*` files**. Measured, not assumed: a single-process read of both
  sides back-to-back (record 53) reports `identical: true` for all four resources,
  with matching `avg10`/`avg60`/`avg300`/`total` on every line — e.g. `cpu` both
  sides `some avg10=0.70 avg60=0.48 avg300=0.14 total=3132563`, `irq` both sides
  `full avg10=0.99 avg60=0.84 avg300=0.34 total=8987071`. This is expected: the
  cgroup root contains the whole system. It means the *system* surface and the
  *root-cgroup* surface are two views of one counter set on this host — a tool that
  summed them would double-count.
- The equality is a *same-instant* equality, and the measurement method matters.
  Two further observations bound the claim:
  - In the first capture the two sets were also byte-identical even though each
    `cat` was its own process (records 3–6 vs 7–10, e.g. `cpu` `total=1455783`
    on both sides, `io` `total=29471300` on both sides) — the counters did not
    move in the microseconds between the two reads.
  - Later, under heavier load, the same cross-process comparison showed the two
    surfaces drifting apart by 1–90 µs *between* the two reads (records 44–51:
    `cpu` `total=2783690` vs `2783691`, `io` `46904948` vs `46905013`,
    `memory` `4864688` vs `4864778`), and record 52's automated comparison
    correctly reported `{'cpu': False, 'io': False, 'irq': False, 'memory': False}`.
    So the surfaces track one counter set but are **not guaranteed to be
    byte-equal across two separate reads**; a tool that compares the two surfaces
    for equality must read them in the same process, and one that requires
    byte-equality across separate reads would false-alarm under load.
- Per-cgroup values are genuinely distinct from the root: `/sys/fs/cgroup/system.slice/`
  has its own `cpu.pressure` (`some avg10=0.00 … total=10430`, `full … total=3447`),
  `memory.pressure` (`total=757`), `irq.pressure` (`full … total=29847`),
  `io.pressure` (`some … total=315615`, `full … total=313678`) and its own
  `cgroup.pressure` = `1` (records 37–38, 55). `system.slice` is a real subset, so
  cgroup-scoped reading is a different measurement, not a duplicate.

## 5. Two samples one second apart — per-kind total deltas

Sample 1 at **2026-10-22T08:16:37.731933Z** (record 17), sample 2 at
**2026-10-22T08:16:38.732044Z** (record 18) — one second of wall clock between the
reads. Raw sample texts are records 17–18; the computed delta table is record 21.

| resource | kind | total (sample 1) | total (sample 2) | `total_delta_us` | `stall_ratio` |
|---|---|---|---|---|---|
| cpu | some | 1455803 | 1457433 | **1630** | 0.001630 |
| cpu | full | 0 | 0 | **0** | 0.000000 |
| io | some | 29471522 | 29479051 | **7529** | 0.007529 |
| io | full | 29076910 | 29084039 | **7129** | 0.007129 |
| irq | full | 5908337 | 5911257 | **2920** | 0.002920 |
| memory | some | 2035146 | 2035155 | **9** | 0.000009 |
| memory | full | 2011665 | 2011672 | **7** | 0.000007 |

`stall_ratio = total_delta_us / (S * 1e6)` with `S = 1`.

Readings that matter for the tool:

- **Every delta is non-negative**; no counter regressed on this host in this window.
  `cpu.full` delta is `0` because its counter is pinned at `0` (§3.2) — a
  `counter_regressed` detection must key on a *decrease*, not on a zero delta, or
  `cpu.full` would false-positive here.
- `memory` deltas are tiny but non-zero (9 µs and 7 µs over one second). A
  "no movement ⇒ absent" shortcut would misreport `memory` as unavailable.
- `avg10` values are identical across the two samples for every kind (e.g. `cpu.some`
  `0.18` → `0.18`, `io.some` `1.07` → `1.07`) because the averaging window is
  10 s and the elapsed interval is 1 s. An implementation that samples the averages
  twice and compares them for change would see nothing.

### Independent corroboration — four samples, 2 s apart (records 42–43)

To confirm the delta method rather than rely on a single pair, the same computation
was run over four samples spaced 2 s:

```
2026-10-22T08:18:24.790154Z cpu.some    total=1666143   cpu.full    total=0
2026-10-22T08:18:26.790261Z cpu.some    total=1669269  Δ=3126      cpu.full  total=0  Δ=0
2026-10-22T08:18:28.790422Z cpu.some    total=1671830  Δ=2561      cpu.full  total=0  Δ=0
2026-10-22T08:18:30.790606Z cpu.some    total=1673767  Δ=1937      cpu.full  total=0  Δ=0
2026-10-22T08:18:26.790261Z io.some     total=32695353 Δ=30910     io.full   total=32224714 Δ=29737
2026-10-22T08:18:28.790422Z io.some     total=32720881 Δ=25528     io.full   total=32249283 Δ=24569
2026-10-22T08:18:30.790606Z io.some     total=32758236 Δ=37355     io.full   total=32286198 Δ=36915
2026-10-22T08:18:26.790261Z irq.full    total=6438580  Δ=7807
2026-10-22T08:18:28.790422Z irq.full    total=6446181  Δ=7601
2026-10-22T08:18:30.790606Z irq.full    total=6454841  Δ=8660
2026-10-22T08:18:26.790261Z memory.some  total=2370371  Δ=3234      memory.full total=2341346 Δ=3226
2026-10-22T08:18:28.790422Z memory.some  total=2370371  Δ=0         memory.full total=2341346 Δ=0
2026-10-22T08:18:30.790606Z memory.some  total=2370371  Δ=0         memory.full total=2341346 Δ=0
```

Two behaviours a live tool must survive, both observed here:

- **`memory` legitimately stops advancing** (Δ=0 for the last two 2-second windows
  while `io` and `cpu` keep moving). A zero delta is normal, not a stall and not a
  regression.
- The host's `io` pressure was materially busier during the capture than the first
  pair suggested — `io.some avg10` moved from `1.07` (record 4) to `5.41`
  (record 33) to `9.57` (record 53) and, at 08:22:34Z, to **`10.57`** (records
  46–47). **A live run of the tool on this host is therefore not guaranteed to
  produce `PRESSURE_OK`**: with the contract's default `--warn-avg10 10.0`, this
  host's `io.some` **did cross the threshold during the capture window**
  (`avg10=10.57` at 2026-10-22T08:22:34Z, with `io.full avg10=9.09` just
  under). A retained "live host run" must record the value it saw, not assert a
  verdict it did not observe — on this host `PRESSURE_HIGH` is a reachable live
  outcome, and the sibling seats' own capture activity (this fleet is running 33
  concurrent agents) is a plausible cause of the `io` load.

  Note for the threshold rule: the contract flags `avg10 ≥ X` on `some` of
  cpu/io/memory or `full` of memory/io/irq. On this host, `io.some` is the line
  that fires first, and `io.full` trails it by roughly one point — so a
  `--warn-avg10 10.0` run sees `PRESSURE_HIGH` on `some` before it ever sees it
  on `full`. The `full`/`some` distinction is therefore load-bearing for the
  finding's `resource` field, not cosmetic.

## 6. Absent-resource behaviour on this host

`open("/proc/pressure/nonexistent")` raised `OSError: No such file or directory
(errno=2)` (record 59) and `cat /proc/pressure/missing-file-test` exited 1 with
`No such file or directory` (record 27). So the contract's ENOENT → `absent`
mapping is reachable and observable on this host; `EOPNOTSUPP` (PSI compiled out
or `psi=0`) and `EACCES`/`EPERM` are **not** reachable here and were not observed
— the config read is what explains why.

## 7. The C2 tool landed mid-capture, and its live run agrees

The C2 tool did **not** exist when the capture began. Measured absences, all
recorded:

- `ls .../tools/fixtures/` → *No such file or directory* (exit 2, record 40).
- `find .../tools -maxdepth 2 -name 'mori-pressure*'` → no output (record 31).
- `ls .../tools/ | grep -i pressure` → no match, exit 1 (record 30).
- `find ... -maxdepth 3 -name 'mori-pressure*'` → no output (record 41).

While the capture was in flight the tool and the frozen cases were committed by
their own seats:

- `f6a2970` — *"round-24: freeze the 12 C2 pressure cases and register before the
  tool"*
- `6ee6248` — *"round-24: land tools/mori-pressure.py (C2) after the frozen cases"*

Both are verified ancestors of the capture-end HEAD `06a7686` via
`git merge-base --is-ancestor`. `git status --porcelain tools/mori-pressure.py
tools/fixtures/mori-pressure/cases.json` is **empty** — both are committed and
clean, not working-tree edits (record 66).

Live runs of the landed tool, all read-only, all in the evidence block:

| command | exit | observed |
|---|---|---|
| `python3 -I tools/mori-pressure.py --selftest` | 0 | `MORI_PRESSURE_SELFTEST: PASS 12/12` (record 67) |
| `python3 -I tools/mori-pressure.py` | 0 | `"verdict": "PRESSURE_OK"`, `"findings": []`, `"schema": "mori-pressure-v1"` (record 68) |
| `python3 -I tools/mori-pressure.py --interval 1` | 0 | `"verdict": "PRESSURE_OK"`, per-kind `total_delta_us` and `stall_ratio` (record 69) |
| `python3 -I tools/mori-pressure.py --warn-avg10 0.01` | **1** | `"verdict": "PRESSURE_HIGH"`, two `PRESSURE_HIGH` findings (`memory` some, `io` some) (record 70) |

The tool's live output reproduces every host fact this seat measured independently:

- `irq` → `"some": null`, `"state": "ok"` — never `malformed` (matches §3.1).
- `cpu` → `"full": {"avg10": 0.0, "avg60": 0.0, "avg300": 0.0, "total": 0}` with
  `"full_system_undefined": true` and the note *"system cpu 'full' is undefined by
  the kernel: reported, never used for a threshold"* (matches §3.2).
- `--interval 1` produced `"cpu.some.total_delta_us": 2277` /
  `"stall_ratio": 0.002277` and `"memory.*.total_delta_us": 0` with
  `"stall_ratio": 0.0` — the tool correctly treats a zero delta as normal, not
  `counter_regressed` (matches §5).
- `--interval 1` also reports `"elapsed_us": 1000275` — the implementation measures
  the real elapsed time rather than assuming exactly 1 s.
- The `--warn-avg10 0.01` run fired on `some` for `memory` and `io` and **not** on
  `cpu.full` (whose `avg10` is `0.0`), which is the contract's
  "system cpu full is never used for a threshold" rule doing its job.
- `--warn-avg10 0.01` exits **1** on `PRESSURE_HIGH` and the plain run exits **0**
  on `PRESSURE_OK`, matching the contract's exit map.

The tool's own live numbers also confirm the volatility noted in §5: the plain run
at 08:37:31Z saw `io.some avg10 = 0.2`, whereas the raw read at 08:22:34Z saw
`10.57`. **A retained live host run must report what it saw, not assert a
verdict.** The run in this report happened to see `PRESSURE_OK`; the same host
minutes earlier crossed the default threshold. The L1 should retain the output
verbatim and not present `PRESSURE_OK` as a stable property of this host.

## 8. What this seat did not do, and what it did not run

- The C2 tool did not exist for the first ~20 minutes of the capture; the
  before-state absences are recorded above (§7) and the tool's own after-state runs
  are recorded too.
- No `--warn-avg10` sweep beyond the two values actually run (default `10.0` and
  `0.01`) was performed; no other threshold was exercised.
- No cgroup was created, no `cgroup.pressure` value was written, no PSI trigger was
  registered, no service was restarted, no package was installed or upgraded.
- The tool was invoked only in its read-only modes (`--selftest`, default,
  `--interval`, `--warn-avg10`); no mode that writes was invoked.
- Not run: nothing else. Every number quoted above comes from a command in the
  JSON block below.

## 9. Facts handed to the tool-building seat and to the L1

1. `irq` ⇒ `some: null`, `state: ok` (never `malformed`) — live host proves it, and
   the landed tool reports it.
2. `cpu.full` ⇒ `total` is `0` and all averages `0.00`; report it, label
   `full_system_undefined: true`, exclude it from every threshold, and do not read
   it as "no stall". A `total_delta_us` of `0` there is normal, not
   `counter_regressed`.
3. A zero `total_delta_us` is normal for a healthy resource (`memory` on this
   host, and `cpu.full` always). Regression detection must compare the new total
   against the old one, not against zero.
4. `/proc/pressure/*` are mode `0666`; `EACCES` is not reachable for these four
   paths on this host.
5. `/sys/fs/cgroup/cgroup.pressure` is the flag `1`, not a PSI line; the root
   cgroup's `*.pressure` files are the same counter set as the system files
   (byte-identical when read in one process, drifting by 1–90 µs across two
   separate reads under load), so the two surfaces must not be summed or treated
   as independent evidence.
6. `avg10` does not change over a 1-second sampling interval; a two-sample avg
   comparison is vacuous here.
7. `io` pressure on this host is volatile and **did cross the contract's default
   `--warn-avg10 10.0` threshold during the capture** (`io.some avg10` 1.07 → 5.41
   → 9.57 → **10.57**). A retained live run must report what it saw;
   `PRESSURE_HIGH` is a reachable live outcome on this host, so it must not be
   written up as `PRESSURE_OK` by assumption. The run retained in §7 saw
   `PRESSURE_OK` at 08:37:31Z; that is a reading, not a host invariant.

## 10. Evidence block (every command, exit code, output, UTC timestamp)

Machine-readable; `records[]` is in execution order, each with `timestamp_utc`,
`command`, `exit_code`, `stdout`, `stderr`.

```json
{
  "schema": "mori-live-pressure-capture-v1",
  "seat": "MoriR24.LivePressureCapture",
  "claim": "C2",
  "lane_repo": "/home/vgpnk/Projects/shokunin/mori-shokunin",
  "lane_head_at_capture_start": "f7eb430 round-24: contract amendment A1 (R2 scan scope) before the C1 tool lands",
  "lane_head_at_capture_end": "06a7686 round-24: freeze-order measurement register copy for C2",
  "tool_commit": "6ee6248 round-24: land tools/mori-pressure.py (C2) after the frozen cases",
  "cases_commit": "f6a2970 round-24: freeze the 12 C2 pressure cases and register before the tool",
  "host": "plazir27",
  "kernel_release": "7.2.11-arch1-1",
  "captured_utc_window": [
    "2026-10-22T08:16:37.723144Z",
    "2026-10-22T08:37:33.013335Z"
  ],
  "mode": "read-only; no writes to /proc, /sys or cgroup files; no PSI trigger registration; no service or package changes; no lane-repo file other than this report",
  "records": [
    {
      "timestamp_utc": "2026-10-22T08:16:37.723144Z",
      "command": "uname -r",
      "exit_code": 0,
      "stdout": "7.2.11-arch1-1\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:16:37.723581Z",
      "command": "uname -a",
      "exit_code": 0,
      "stdout": "Linux plazir27 7.2.11-arch1-1 #1 SMP PREEMPT_DYNAMIC Fri, 16 Oct 2026 00:28:58 +0000 x86_64 GNU/Linux\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:16:37.723981Z",
      "command": "cat /proc/pressure/cpu",
      "exit_code": 0,
      "stdout": "some avg10=0.18 avg60=0.03 avg300=0.00 total=1455783\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:16:37.724314Z",
      "command": "cat /proc/pressure/io",
      "exit_code": 0,
      "stdout": "some avg10=1.07 avg60=3.90 avg300=3.68 total=29471300\nfull avg10=1.01 avg60=3.77 avg300=3.60 total=29076706\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:16:37.724574Z",
      "command": "cat /proc/pressure/irq",
      "exit_code": 0,
      "stdout": "full avg10=0.00 avg60=0.00 avg300=0.00 total=5908314\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:16:37.724888Z",
      "command": "cat /proc/pressure/memory",
      "exit_code": 0,
      "stdout": "some avg10=0.00 avg60=0.14 avg300=0.12 total=2035146\nfull avg10=0.00 avg60=0.12 avg300=0.11 total=2011665\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:16:37.725156Z",
      "command": "cat /sys/fs/cgroup/cpu.pressure",
      "exit_code": 0,
      "stdout": "some avg10=0.18 avg60=0.03 avg300=0.00 total=1455783\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:16:37.725466Z",
      "command": "cat /sys/fs/cgroup/io.pressure",
      "exit_code": 0,
      "stdout": "some avg10=1.07 avg60=3.90 avg300=3.68 total=29471300\nfull avg10=1.01 avg60=3.77 avg300=3.60 total=29076706\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:16:37.725704Z",
      "command": "cat /sys/fs/cgroup/irq.pressure",
      "exit_code": 0,
      "stdout": "full avg10=0.00 avg60=0.00 avg300=0.00 total=5908314\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:16:37.725952Z",
      "command": "cat /sys/fs/cgroup/memory.pressure",
      "exit_code": 0,
      "stdout": "some avg10=0.00 avg60=0.14 avg300=0.12 total=2035146\nfull avg10=0.00 avg60=0.12 avg300=0.11 total=2011665\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:16:37.726203Z",
      "command": "cat /sys/fs/cgroup/cgroup.pressure",
      "exit_code": 0,
      "stdout": "1\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:16:37.726459Z",
      "command": "cat /proc/cmdline",
      "exit_code": 0,
      "stdout": "resume=/dev/mapper/root resume_offset=3795013 quiet splash loglevel=0 systemd.show_status=false rd.udev.log_level=0 vt.global_cursor_default=0 cryptdevice=PARTUUID=cf3d875f-72a4-4468-9795-015c9e953618:root:allow-discards,no-read-workqueue,no-write-workqueue root=/dev/mapper/root zswap.enabled=1 zswap.max_pool_percent=25 rootflags=subvol=@ rw rootfstype=btrfs\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:16:37.726923Z",
      "command": "sh -c zcat /proc/config.gz | wc -c",
      "exit_code": 0,
      "stdout": "293587\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:16:37.729896Z",
      "command": "ls -la /proc/config.gz",
      "exit_code": 0,
      "stdout": "-r--r--r-- 1 root root 69954 Oct 22 05:15 /proc/config.gz\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:16:37.730983Z",
      "command": "ls -la /usr/lib/modules/7.2.11-arch1-1/",
      "exit_code": 0,
      "stdout": "total 24660\ndrwxr-xr-x 1 root root      532 Oct 20 09:18 .\ndrwxr-xr-x 1 root root       62 Oct 20 09:57 ..\ndrwxr-xr-x 1 root root      466 Oct 20 09:16 build\ndrwxr-xr-x 1 root root      100 Oct 20 09:16 kernel\n-rw-r--r-- 1 root root  1782422 Oct 20 09:18 modules.alias\n-rw-r--r-- 1 root root  1731669 Oct 20 09:18 modules.alias.bin\n-rw-r--r-- 1 root root     8515 Oct 15 21:28 modules.builtin\n-rw-r--r-- 1 root root    69360 Oct 20 09:18 modules.builtin.alias.bin\n-rw-r--r-- 1 root root    10517 Oct 20 09:18 modules.builtin.bin\n-rw-r--r-- 1 root root   144039 Oct 15 21:28 modules.builtin.modinfo\n-rw-r--r-- 1 root root   950216 Oct 20 09:18 modules.dep\n-rw-r--r-- 1 root root  1230557 Oct 20 09:18 modules.dep.bin\n-rw-r--r-- 1 root root      409 Oct 20 09:18 modules.devname\n-rw-r--r-- 1 root root   266445 Oct 15 21:28 modules.order\n-rw-r--r-- 1 root root     2273 Oct 20 09:18 modules.softdep\n-rw-r--r-- 1 root root   798915 Oct 20 09:18 modules.symbols\n-rw-r--r-- 1 root root   968187 Oct 20 09:18 modules.symbols.bin\n-rw-r--r-- 1 root root       55 Oct 20 09:18 modules.weakdep\n-rw-r--r-- 1 root root        6 Oct 15 21:28 pkgbase\ndrwxr-xr-x 1 root root        8 Oct 20 09:17 updates\ndrwxr-xr-x 1 root root       56 Oct 20 09:16 vdso\n-rw-r--r-- 1 root root 17244672 Oct 15 21:28 vmlinuz\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:16:37.731616Z",
      "command": "ls -la /usr/lib/modules/7.2.11-arch1-1/config",
      "exit_code": 2,
      "stdout": "",
      "stderr": "ls: cannot access '/usr/lib/modules/7.2.11-arch1-1/config': No such file or directory\n"
    },
    {
      "timestamp_utc": "2026-10-22T08:16:37.731933Z",
      "command": "cat /proc/pressure/{cpu,io,irq,memory}   # sample 1",
      "exit_code": 0,
      "stdout": "{\n  \"cpu\": \"some avg10=0.18 avg60=0.03 avg300=0.00 total=1455803\\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\\n\",\n  \"io\": \"some avg10=1.07 avg60=3.90 avg300=3.68 total=29471522\\nfull avg10=1.01 avg60=3.77 avg300=3.60 total=29076910\\n\",\n  \"irq\": \"full avg10=0.00 avg60=0.00 avg300=0.00 total=5908337\\n\",\n  \"memory\": \"some avg10=0.00 avg60=0.14 avg300=0.12 total=2035146\\nfull avg10=0.00 avg60=0.12 avg300=0.11 total=2011665\\n\"\n}",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:16:38.732044Z",
      "command": "sleep 1; cat /proc/pressure/{cpu,io,irq,memory}   # sample 2",
      "exit_code": 0,
      "stdout": "{\n  \"cpu\": \"some avg10=0.18 avg60=0.03 avg300=0.00 total=1457433\\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\\n\",\n  \"io\": \"some avg10=1.07 avg60=3.90 avg300=3.68 total=29479051\\nfull avg10=1.01 avg60=3.77 avg300=3.60 total=29084039\\n\",\n  \"irq\": \"full avg10=0.00 avg60=0.00 avg300=0.00 total=5911257\\n\",\n  \"memory\": \"some avg10=0.00 avg60=0.14 avg300=0.12 total=2035155\\nfull avg10=0.00 avg60=0.12 avg300=0.11 total=2011672\\n\"\n}",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:16:38.733062Z",
      "command": "sh -c zcat /proc/config.gz | grep -E '^CONFIG_(PSI|PSI_DEFAULT_DISABLED|IRQ_TIME_ACCOUNTING)='",
      "exit_code": 0,
      "stdout": "CONFIG_IRQ_TIME_ACCOUNTING=y\nCONFIG_PSI=y\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:16:38.738324Z",
      "command": "zcat /proc/config.gz | grep -E '^CONFIG_(PSI|PSI_DEFAULT_DISABLED|IRQ_TIME_ACCOUNTING)='",
      "exit_code": 0,
      "stdout": "CONFIG_IRQ_TIME_ACCOUNTING=y\nCONFIG_PSI=y",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:16:38.738490Z",
      "command": "computed: total_delta_us = total(sample2) - total(sample1); stall_ratio = total_delta_us / (1 * 1e6)",
      "exit_code": 0,
      "stdout": "{\n  \"cpu\": {\n    \"some\": {\n      \"total_sample1\": 1455803,\n      \"total_sample2\": 1457433,\n      \"total_delta_us\": 1630,\n      \"stall_ratio\": 0.00163,\n      \"avg10_sample1\": 0.18,\n      \"avg10_sample2\": 0.18\n    },\n    \"full\": {\n      \"total_sample1\": 0,\n      \"total_sample2\": 0,\n      \"total_delta_us\": 0,\n      \"stall_ratio\": 0.0,\n      \"avg10_sample1\": 0.0,\n      \"avg10_sample2\": 0.0\n    }\n  },\n  \"io\": {\n    \"some\": {\n      \"total_sample1\": 29471522,\n      \"total_sample2\": 29479051,\n      \"total_delta_us\": 7529,\n      \"stall_ratio\": 0.007529,\n      \"avg10_sample1\": 1.07,\n      \"avg10_sample2\": 1.07\n    },\n    \"full\": {\n      \"total_sample1\": 29076910,\n      \"total_sample2\": 29084039,\n      \"total_delta_us\": 7129,\n      \"stall_ratio\": 0.007129,\n      \"avg10_sample1\": 1.01,\n      \"avg10_sample2\": 1.01\n    }\n  },\n  \"irq\": {\n    \"full\": {\n      \"total_sample1\": 5908337,\n      \"total_sample2\": 5911257,\n      \"total_delta_us\": 2920,\n      \"stall_ratio\": 0.00292,\n      \"avg10_sample1\": 0.0,\n      \"avg10_sample2\": 0.0\n    }\n  },\n  \"memory\": {\n    \"some\": {\n      \"total_sample1\": 2035146,\n      \"total_sample2\": 2035155,\n      \"total_delta_us\": 9,\n      \"stall_ratio\": 9e-06,\n      \"avg10_sample1\": 0.0,\n      \"avg10_sample2\": 0.0\n    },\n    \"full\": {\n      \"total_sample1\": 2011665,\n      \"total_sample2\": 2011672,\n      \"total_delta_us\": 7,\n      \"stall_ratio\": 7e-06,\n      \"avg10_sample1\": 0.0,\n      \"avg10_sample2\": 0.0\n    }\n  }\n}",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:17:10.691454Z",
      "command": "zcat /proc/config.gz | grep -nE 'PSI|IRQ_TIME_ACCOUNTING'",
      "exit_code": 0,
      "stdout": "161:CONFIG_IRQ_TIME_ACCOUNTING=y\n169:CONFIG_PSI=y\n170:# CONFIG_PSI_DEFAULT_DISABLED is not set\n980:CONFIG_HAVE_IRQ_TIME_ACCOUNTING=y\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:17:10.693985Z",
      "command": "zcat /proc/config.gz | grep -c '^CONFIG_PSI_DEFAULT_DISABLED='",
      "exit_code": 1,
      "stdout": "0\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:17:10.695135Z",
      "command": "grep -c 'psi=' /proc/cmdline; echo \"grep_exit=$?\"",
      "exit_code": 0,
      "stdout": "0\ngrep_exit=1\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:17:10.696613Z",
      "command": "grep -oE '(^| )[a-z_]+=' /proc/cmdline | tr -d ' =' | sort | tr '\\n' ' '; echo",
      "exit_code": 0,
      "stdout": "cryptdevice loglevel resume resume_offset root rootflags rootfstype \n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:17:10.697562Z",
      "command": "stat -c '%n mode=%A size=%s uid=%u gid=%g' /proc/pressure/cpu /proc/pressure/io /proc/pressure/irq /proc/pressure/memory /sys/fs/cgroup/cgroup.pressure",
      "exit_code": 0,
      "stdout": "/proc/pressure/cpu mode=-rw-rw-rw- size=0 uid=0 gid=0\n/proc/pressure/io mode=-rw-rw-rw- size=0 uid=0 gid=0\n/proc/pressure/irq mode=-rw-rw-rw- size=0 uid=0 gid=0\n/proc/pressure/memory mode=-rw-rw-rw- size=0 uid=0 gid=0\n/sys/fs/cgroup/cgroup.pressure mode=-rw-r--r-- size=0 uid=0 gid=0\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:17:10.698524Z",
      "command": "cat /proc/pressure/missing-file-test; echo exit=$?",
      "exit_code": 0,
      "stdout": "exit=1\n",
      "stderr": "cat: /proc/pressure/missing-file-test: No such file or directory\n"
    },
    {
      "timestamp_utc": "2026-10-22T08:17:10.699589Z",
      "command": "ls /sys/fs/cgroup/system.slice/ | grep -i pressure",
      "exit_code": 0,
      "stdout": "cgroup.pressure\ncpu.pressure\nio.pressure\nirq.pressure\nmemory.pressure\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:17:10.700769Z",
      "command": "cat /sys/fs/cgroup/cgroup.controllers; echo; cat /sys/fs/cgroup/cgroup.subtree_control",
      "exit_code": 0,
      "stdout": "cpuset cpu io memory hugetlb pids rdma misc dmem\n\ncpuset cpu io memory pids\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:17:10.702448Z",
      "command": "ls -la /home/vgpnk/Projects/shokunin/mori-shokunin/tools/ | grep -i pressure; echo 'exit='$?",
      "exit_code": 0,
      "stdout": "exit=1\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:17:10.703698Z",
      "command": "find /home/vgpnk/Projects/shokunin/mori-shokunin/tools -maxdepth 2 -name 'mori-pressure*' 2>/dev/null; echo done",
      "exit_code": 0,
      "stdout": "done\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:18:07.520090Z",
      "command": "od -c /proc/pressure/cpu",
      "exit_code": 0,
      "stdout": "0000000   s   o   m   e       a   v   g   1   0   =   0   .   0   0    \n0000020   a   v   g   6   0   =   0   .   0   0       a   v   g   3   0\n0000040   0   =   0   .   0   0       t   o   t   a   l   =   1   6   3\n0000060   9   0   0   6  \\n   f   u   l   l       a   v   g   1   0   =\n0000100   0   .   0   0       a   v   g   6   0   =   0   .   0   0    \n0000120   a   v   g   3   0   0   =   0   .   0   0       t   o   t   a\n0000140   l   =   0  \\n\n0000144\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:18:07.521150Z",
      "command": "od -c /proc/pressure/io",
      "exit_code": 0,
      "stdout": "0000000   s   o   m   e       a   v   g   1   0   =   5   .   4   1    \n0000020   a   v   g   6   0   =   3   .   4   1       a   v   g   3   0\n0000040   0   =   3   .   4   1       t   o   t   a   l   =   3   2   2\n0000060   2   7   2   3   1  \\n   f   u   l   l       a   v   g   1   0\n0000100   =   5   .   4   1       a   v   g   6   0   =   3   .   3   6\n0000120       a   v   g   3   0   0   =   3   .   3   3       t   o   t\n0000140   a   l   =   3   1   7   7   1   0   3   1  \\n\n0000154\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:18:07.522135Z",
      "command": "od -c /proc/pressure/irq",
      "exit_code": 0,
      "stdout": "0000000   f   u   l   l       a   v   g   1   0   =   0   .   0   9    \n0000020   a   v   g   6   0   =   0   .   0   2       a   v   g   3   0\n0000040   0   =   0   .   0   0       t   o   t   a   l   =   6   3   5\n0000060   9   5   2   0  \\n\n0000065\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:18:07.523102Z",
      "command": "od -c /proc/pressure/memory",
      "exit_code": 0,
      "stdout": "0000000   s   o   m   e       a   v   g   1   0   =   0   .   5   5    \n0000020   a   v   g   6   0   =   0   .   1   5       a   v   g   3   0\n0000040   0   =   0   .   1   0       t   o   t   a   l   =   2   2   9\n0000060   7   1   5   6  \\n   f   u   l   l       a   v   g   1   0   =\n0000100   0   .   5   5       a   v   g   6   0   =   0   .   1   4    \n0000120   a   v   g   3   0   0   =   0   .   0   9       t   o   t   a\n0000140   l   =   2   2   6   9   0   0   4  \\n\n0000152\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:18:07.524077Z",
      "command": "od -c /sys/fs/cgroup/cgroup.pressure",
      "exit_code": 0,
      "stdout": "0000000   1  \\n\n0000002\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:18:07.525334Z",
      "command": "cat /sys/fs/cgroup/system.slice/cpu.pressure; echo '---'; cat /sys/fs/cgroup/system.slice/memory.pressure",
      "exit_code": 0,
      "stdout": "some avg10=0.00 avg60=0.00 avg300=0.00 total=10430\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=3447\n---\nsome avg10=0.00 avg60=0.00 avg300=0.00 total=757\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=757\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:18:07.526735Z",
      "command": "cat /sys/fs/cgroup/system.slice/irq.pressure; echo '---'; cat /sys/fs/cgroup/system.slice/io.pressure; echo '---'; cat /sys/fs/cgroup/system.slice/cgroup.pressure",
      "exit_code": 0,
      "stdout": "full avg10=0.00 avg60=0.00 avg300=0.00 total=29847\n---\nsome avg10=0.00 avg60=0.00 avg300=0.00 total=315615\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=313678\n---\n1\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:18:07.528579Z",
      "command": "git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --oneline -1",
      "exit_code": 0,
      "stdout": "f7eb430 round-24: contract amendment A1 (R2 scan scope) before the C1 tool lands\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:18:07.529820Z",
      "command": "ls /home/vgpnk/Projects/shokunin/mori-shokunin/tools/fixtures/ 2>&1",
      "exit_code": 2,
      "stdout": "ls: cannot access '/home/vgpnk/Projects/shokunin/mori-shokunin/tools/fixtures/': No such file or directory\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:18:07.531389Z",
      "command": "find /home/vgpnk/Projects/shokunin/mori-shokunin -maxdepth 3 -name 'mori-pressure*' 2>/dev/null; echo end",
      "exit_code": 0,
      "stdout": "end\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:18:30.791671Z",
      "command": "echo 'multi-sample: 4 samples, 2s apart, of /proc/pressure/{cpu,io,irq,memory}'",
      "exit_code": 0,
      "stdout": "multi-sample: 4 samples, 2s apart, of /proc/pressure/{cpu,io,irq,memory}\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:18:30.798724Z",
      "command": "python3 -c \"print(chr(10).join(['2026-10-22T08:18:24.790154Z cpu.some total=1666143 delta=None', '2026-10-22T08:18:24.790154Z cpu.full total=0 delta=None', '2026-10-22T08:18:24.790154Z io.some total=32664443 delta=None', '2026-10-22T08:18:24.790154Z io.full total=32194977 delta=None', '2026-10-22T08:18:24.790154Z irq.full total=6430773 delta=None', '2026-10-22T08:18:24.790154Z memory.some total=2367137 delta=None', '2026-10-22T08:18:24.790154Z memory.full total=2338120 delta=None', '2026-10-22T08:18:26.790261Z cpu.some total=1669269 delta=3126', '2026-10-22T08:18:26.790261Z cpu.full total=0 delta=0', '2026-10-22T08:18:26.790261Z io.some total=32695353 delta=30910', '2026-10-22T08:18:26.790261Z io.full total=32224714 delta=29737', '2026-10-22T08:18:26.790261Z irq.full total=6438580 delta=7807', '2026-10-22T08:18:26.790261Z memory.some total=2370371 delta=3234', '2026-10-22T08:18:26.790261Z memory.full total=2341346 delta=3226', '2026-10-22T08:18:28.790422Z cpu.some total=1671830 delta=2561', '2026-10-22T08:18:28.790422Z cpu.full total=0 delta=0', '2026-10-22T08:18:28.790422Z io.some total=32720881 delta=25528', '2026-10-22T08:18:28.790422Z io.full total=32249283 delta=24569', '2026-10-22T08:18:28.790422Z irq.full total=6446181 delta=7601', '2026-10-22T08:18:28.790422Z memory.some total=2370371 delta=0', '2026-10-22T08:18:28.790422Z memory.full total=2341346 delta=0', '2026-10-22T08:18:30.790606Z cpu.some total=1673767 delta=1937', '2026-10-22T08:18:30.790606Z cpu.full total=0 delta=0', '2026-10-22T08:18:30.790606Z io.some total=32758236 delta=37355', '2026-10-22T08:18:30.790606Z io.full total=32286198 delta=36915', '2026-10-22T08:18:30.790606Z irq.full total=6454841 delta=8660', '2026-10-22T08:18:30.790606Z memory.some total=2370371 delta=0', '2026-10-22T08:18:30.790606Z memory.full total=2341346 delta=0']))\" ",
      "exit_code": 0,
      "stdout": "2026-10-22T08:18:24.790154Z cpu.some total=1666143 delta=None\n2026-10-22T08:18:24.790154Z cpu.full total=0 delta=None\n2026-10-22T08:18:24.790154Z io.some total=32664443 delta=None\n2026-10-22T08:18:24.790154Z io.full total=32194977 delta=None\n2026-10-22T08:18:24.790154Z irq.full total=6430773 delta=None\n2026-10-22T08:18:24.790154Z memory.some total=2367137 delta=None\n2026-10-22T08:18:24.790154Z memory.full total=2338120 delta=None\n2026-10-22T08:18:26.790261Z cpu.some total=1669269 delta=3126\n2026-10-22T08:18:26.790261Z cpu.full total=0 delta=0\n2026-10-22T08:18:26.790261Z io.some total=32695353 delta=30910\n2026-10-22T08:18:26.790261Z io.full total=32224714 delta=29737\n2026-10-22T08:18:26.790261Z irq.full total=6438580 delta=7807\n2026-10-22T08:18:26.790261Z memory.some total=2370371 delta=3234\n2026-10-22T08:18:26.790261Z memory.full total=2341346 delta=3226\n2026-10-22T08:18:28.790422Z cpu.some total=1671830 delta=2561\n2026-10-22T08:18:28.790422Z cpu.full total=0 delta=0\n2026-10-22T08:18:28.790422Z io.some total=32720881 delta=25528\n2026-10-22T08:18:28.790422Z io.full total=32249283 delta=24569\n2026-10-22T08:18:28.790422Z irq.full total=6446181 delta=7601\n2026-10-22T08:18:28.790422Z memory.some total=2370371 delta=0\n2026-10-22T08:18:28.790422Z memory.full total=2341346 delta=0\n2026-10-22T08:18:30.790606Z cpu.some total=1673767 delta=1937\n2026-10-22T08:18:30.790606Z cpu.full total=0 delta=0\n2026-10-22T08:18:30.790606Z io.some total=32758236 delta=37355\n2026-10-22T08:18:30.790606Z io.full total=32286198 delta=36915\n2026-10-22T08:18:30.790606Z irq.full total=6454841 delta=8660\n2026-10-22T08:18:30.790606Z memory.some total=2370371 delta=0\n2026-10-22T08:18:30.790606Z memory.full total=2341346 delta=0\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:22:34.271026Z",
      "command": "cat /proc/pressure/cpu",
      "exit_code": 0,
      "stdout": "some avg10=0.82 avg60=0.31 avg300=0.07 total=2783690\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:22:34.272266Z",
      "command": "cat /sys/fs/cgroup/cpu.pressure",
      "exit_code": 0,
      "stdout": "some avg10=0.82 avg60=0.31 avg300=0.07 total=2783691\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:22:34.273388Z",
      "command": "cat /proc/pressure/io",
      "exit_code": 0,
      "stdout": "some avg10=10.57 avg60=7.05 avg300=4.69 total=46904948\nfull avg10=9.09 avg60=6.40 avg300=4.45 total=45571531\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:22:34.274515Z",
      "command": "cat /sys/fs/cgroup/io.pressure",
      "exit_code": 0,
      "stdout": "some avg10=10.57 avg60=7.05 avg300=4.69 total=46905013\nfull avg10=9.09 avg60=6.40 avg300=4.45 total=45571595\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:22:34.275561Z",
      "command": "cat /proc/pressure/irq",
      "exit_code": 0,
      "stdout": "full avg10=0.96 avg60=0.74 avg300=0.28 total=8544328\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:22:34.276669Z",
      "command": "cat /sys/fs/cgroup/irq.pressure",
      "exit_code": 0,
      "stdout": "full avg10=0.96 avg60=0.74 avg300=0.28 total=8544335\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:22:34.277662Z",
      "command": "cat /proc/pressure/memory",
      "exit_code": 0,
      "stdout": "some avg10=1.01 avg60=0.92 avg300=0.45 total=4864688\nfull avg10=0.94 avg60=0.86 avg300=0.43 total=4808892\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:22:34.278743Z",
      "command": "cat /sys/fs/cgroup/memory.pressure",
      "exit_code": 0,
      "stdout": "some avg10=1.01 avg60=0.92 avg300=0.45 total=4864778\nfull avg10=0.94 avg60=0.86 avg300=0.43 total=4808982\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:22:34.286557Z",
      "command": "python3 -c \"print({'cpu': False, 'io': False, 'irq': False, 'memory': False})\"",
      "exit_code": 0,
      "stdout": "{'cpu': False, 'io': False, 'irq': False, 'memory': False}\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:23:03.107746Z",
      "command": "python3 -c \"open('/proc/pressure/R'); open('/sys/fs/cgroup/R.pressure')\" for R in cpu,io,irq,memory (single process, back-to-back)",
      "exit_code": 0,
      "stdout": "{\n  \"cpu\": {\n    \"proc\": \"some avg10=0.70 avg60=0.48 avg300=0.14 total=3132563\\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\",\n    \"cgroup_root\": \"some avg10=0.70 avg60=0.48 avg300=0.14 total=3132563\\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\",\n    \"identical\": true\n  },\n  \"io\": {\n    \"proc\": \"some avg10=9.57 avg60=8.25 avg300=5.22 total=50018186\\nfull avg10=8.53 avg60=7.34 avg300=4.87 total=48317840\",\n    \"cgroup_root\": \"some avg10=9.57 avg60=8.25 avg300=5.22 total=50018186\\nfull avg10=8.53 avg60=7.34 avg300=4.87 total=48317840\",\n    \"identical\": true\n  },\n  \"irq\": {\n    \"proc\": \"full avg10=0.99 avg60=0.84 avg300=0.34 total=8987071\",\n    \"cgroup_root\": \"full avg10=0.99 avg60=0.84 avg300=0.34 total=8987071\",\n    \"identical\": true\n  },\n  \"memory\": {\n    \"proc\": \"some avg10=0.72 avg60=0.86 avg300=0.48 total=5249228\\nfull avg10=0.67 avg60=0.80 avg300=0.45 total=5189048\",\n    \"cgroup_root\": \"some avg10=0.72 avg60=0.86 avg300=0.48 total=5249228\\nfull avg10=0.67 avg60=0.80 avg300=0.45 total=5189048\",\n    \"identical\": true\n  }\n}",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:23:03.107783Z",
      "command": "cat /sys/fs/cgroup/cgroup.pressure",
      "exit_code": 0,
      "stdout": "1\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:23:03.107799Z",
      "command": "cat /sys/fs/cgroup/system.slice/cgroup.pressure",
      "exit_code": 0,
      "stdout": "1\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:23:03.107813Z",
      "command": "cat /proc/cmdline",
      "exit_code": 0,
      "stdout": "resume=/dev/mapper/root resume_offset=3795013 quiet splash loglevel=0 systemd.show_status=false rd.udev.log_level=0 vt.global_cursor_default=0 cryptdevice=PARTUUID=cf3d875f-72a4-4468-9795-015c9e953618:root:allow-discards,no-read-workqueue,no-write-workqueue root=/dev/mapper/root zswap.enabled=1 zswap.max_pool_percent=25 rootflags=subvol=@ rw rootfstype=btrfs\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:23:03.107816Z",
      "command": "grep -o 'psi=[^ ]*' /proc/cmdline; echo rc=$?",
      "exit_code": 1,
      "stdout": "",
      "stderr": "grep found no 'psi=' token in /proc/cmdline (exit 1)"
    },
    {
      "timestamp_utc": "2026-10-22T08:23:03.107818Z",
      "command": "grep -c 'psi=' /proc/cmdline",
      "exit_code": 1,
      "stdout": "0\n",
      "stderr": "grep -c printed 0 and exited 1 (no match)"
    },
    {
      "timestamp_utc": "2026-10-22T08:23:03.107829Z",
      "command": "open('/proc/pressure/nonexistent')",
      "exit_code": 1,
      "stdout": "",
      "stderr": "OSError: No such file or directory (errno=2)"
    },
    {
      "timestamp_utc": "2026-10-22T08:36:39.193636Z",
      "command": "ls -la /home/vgpnk/Projects/shokunin/mori-shokunin/tools/",
      "exit_code": 0,
      "stdout": "total 1452\ndrwxr-xr-x 1 vgpnk vgpnk   1094 Oct 22 05:25 .\ndrwxr-xr-x 1 vgpnk vgpnk    248 Oct 21 06:18 ..\ndrwxr-xr-x 1 vgpnk vgpnk     26 Oct 22 05:22 fixtures\n-rwxr-xr-x 1 vgpnk vgpnk 254328 Oct 20 17:39 mori-census.sh\n-rwxr-xr-x 1 vgpnk vgpnk  19406 Oct 21 05:54 mori-content-review.py\n-rwxr-xr-x 1 vgpnk vgpnk  23729 Oct 21 03:52 mori-dispatch-ledger.py\n-rwxr-xr-x 1 vgpnk vgpnk  56185 Oct 21 10:26 mori-evidence-loss.py\n-rwxr-xr-x 1 vgpnk vgpnk  27336 Oct 21 06:19 mori-freeze-order.py\n-rwxr-xr-x 1 vgpnk vgpnk  29352 Oct 20 06:00 mori-journal-window.py\n-rwxr-xr-x 1 vgpnk vgpnk  36080 Oct 20 17:21 mori-misroot-sweep.py\n-rwxr-xr-x 1 vgpnk vgpnk  22515 Oct 22 05:25 mori-pressure.py\n-rwxr-xr-x 1 vgpnk vgpnk  33923 Oct 21 03:49 mori-retention-gate.py\n-rwxr-xr-x 1 vgpnk vgpnk  18191 Oct 21 15:12 mori-retention-reconcile.py\n-rwxr-xr-x 1 vgpnk vgpnk 138699 Oct 20 04:41 mori-round13-regressions.py\n-rwxr-xr-x 1 vgpnk vgpnk 112205 Oct 20 04:40 mori-round14-regressions.py\n-rwxr-xr-x 1 vgpnk vgpnk  92669 Oct 20 05:27 mori-round15-regressions.py\n-rwxr-xr-x 1 vgpnk vgpnk  18460 Oct 20 05:56 mori-round16-context-check.py\n-rwxr-xr-x 1 vgpnk vgpnk  69219 Oct 20 06:10 mori-round16-regressions.py\n-rwxr-xr-x 1 vgpnk vgpnk  33900 Oct 20 17:21 mori-round17-context-check.py\n-rwxr-xr-x 1 vgpnk vgpnk  86018 Oct 20 17:32 mori-round17-jj-regressions.py\n-rwxr-xr-x 1 vgpnk vgpnk 131530 Oct 20 17:21 mori-round17-seat-regressions.py\n-rwxr-xr-x 1 vgpnk vgpnk  46933 Oct 21 06:30 mori-round19-regressions.py\n-rwxr-xr-x 1 vgpnk vgpnk 101752 Oct 20 17:47 mori-seat-terminal.py\n-rwxr-xr-x 1 vgpnk vgpnk  61159 Oct 20 01:19 mori-silence-cases.sh\n-rwxr-xr-x 1 vgpnk vgpnk  30451 Oct 21 08:17 mori-wave-settlement.py\ndrwxr-xr-x 1 vgpnk vgpnk     72 Oct 22 05:19 __pycache__\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:36:39.195276Z",
      "command": "ls -la /home/vgpnk/Projects/shokunin/mori-shokunin/tools/fixtures/ 2>&1",
      "exit_code": 0,
      "stdout": "total 0\ndrwxr-xr-x 1 vgpnk vgpnk   26 Oct 22 05:22 .\ndrwxr-xr-x 1 vgpnk vgpnk 1094 Oct 22 05:25 ..\ndrwxr-xr-x 1 vgpnk vgpnk   20 Oct 22 05:22 mori-pressure\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:36:39.196517Z",
      "command": "find /home/vgpnk/Projects/shokunin/mori-shokunin/tools -maxdepth 3 -name 'mori-pressure*' 2>/dev/null; echo 'find_rc='$?",
      "exit_code": 0,
      "stdout": "/home/vgpnk/Projects/shokunin/mori-shokunin/tools/fixtures/mori-pressure\n/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pressure.py\nfind_rc=0\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:36:39.204936Z",
      "command": "git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain -- tools/ ; echo 'git_status_rc='$?",
      "exit_code": 0,
      "stdout": "?? tools/__pycache__/\ngit_status_rc=0\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:36:39.206074Z",
      "command": "git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --oneline -1",
      "exit_code": 0,
      "stdout": "06a7686 round-24: freeze-order measurement register copy for C2\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:37:31.885561Z",
      "command": "git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --oneline -1",
      "exit_code": 0,
      "stdout": "06a7686 round-24: freeze-order measurement register copy for C2\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:37:31.895597Z",
      "command": "git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain tools/mori-pressure.py tools/fixtures/mori-pressure/cases.json; echo 'clean_if_empty_rc='$?",
      "exit_code": 0,
      "stdout": "clean_if_empty_rc=0\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:37:31.924521Z",
      "command": "python3 -I tools/mori-pressure.py --selftest",
      "exit_code": 0,
      "stdout": "MORI_PRESSURE_SELFTEST: PASS 12/12\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:37:31.954563Z",
      "command": "python3 -I tools/mori-pressure.py",
      "exit_code": 0,
      "stdout": "{\n  \"findings\": [],\n  \"resources\": {\n    \"cpu\": {\n      \"full\": {\n        \"avg10\": 0.0,\n        \"avg300\": 0.0,\n        \"avg60\": 0.0,\n        \"total\": 0\n      },\n      \"full_system_undefined\": true,\n      \"notes\": [\n        \"parsed from the kernel PSI line grammar\",\n        \"system cpu 'full' is undefined by the kernel: reported, never used for a threshold\"\n      ],\n      \"some\": {\n        \"avg10\": 0.0,\n        \"avg300\": 0.0,\n        \"avg60\": 0.0,\n        \"total\": 7715253\n      },\n      \"state\": \"ok\"\n    },\n    \"io\": {\n      \"full\": {\n        \"avg10\": 0.2,\n        \"avg300\": 0.82,\n        \"avg60\": 0.25,\n        \"total\": 66522163\n      },\n      \"notes\": [\n        \"parsed from the kernel PSI line grammar\"\n      ],\n      \"some\": {\n        \"avg10\": 0.2,\n        \"avg300\": 0.9,\n        \"avg60\": 0.26,\n        \"total\": 70099059\n      },\n      \"state\": \"ok\"\n    },\n    \"irq\": {\n      \"full\": {\n        \"avg10\": 0.0,\n        \"avg300\": 0.03,\n        \"avg60\": 0.0,\n        \"total\": 14540353\n      },\n      \"notes\": [\n        \"parsed from the kernel PSI line grammar\"\n      ],\n      \"some\": null,\n      \"state\": \"ok\"\n    },\n    \"memory\": {\n      \"full\": {\n        \"avg10\": 0.2,\n        \"avg300\": 0.08,\n        \"avg60\": 0.12,\n        \"total\": 9284409\n      },\n      \"notes\": [\n        \"parsed from the kernel PSI line grammar\"\n      ],\n      \"some\": {\n        \"avg10\": 0.2,\n        \"avg300\": 0.09,\n        \"avg60\": 0.12,\n        \"total\": 9382000\n      },\n      \"state\": \"ok\"\n    }\n  },\n  \"root\": \"/proc/pressure\",\n  \"schema\": \"mori-pressure-v1\",\n  \"threshold\": {\n    \"label\": \"local (not calibrated)\",\n    \"metric\": \"avg10\",\n    \"value\": 10.0\n  },\n  \"verdict\": \"PRESSURE_OK\"\n}\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:37:32.984854Z",
      "command": "python3 -I tools/mori-pressure.py --interval 1",
      "exit_code": 0,
      "stdout": "{\n  \"elapsed_us\": 1000275,\n  \"findings\": [],\n  \"interval_s\": 1.0,\n  \"resources\": {\n    \"cpu\": {\n      \"full\": {\n        \"avg10\": 0.0,\n        \"avg300\": 0.0,\n        \"avg60\": 0.0,\n        \"stall_ratio\": null,\n        \"total\": 0,\n        \"total_delta_us\": null\n      },\n      \"full_system_undefined\": true,\n      \"notes\": [\n        \"parsed from the kernel PSI line grammar\",\n        \"system cpu 'full' is undefined by the kernel: reported, never used for a threshold\"\n      ],\n      \"some\": {\n        \"avg10\": 0.0,\n        \"avg300\": 0.0,\n        \"avg60\": 0.0,\n        \"stall_ratio\": 0.002277,\n        \"total\": 7717776,\n        \"total_delta_us\": 2277\n      },\n      \"state\": \"ok\"\n    },\n    \"io\": {\n      \"full\": {\n        \"avg10\": 0.2,\n        \"avg300\": 0.82,\n        \"avg60\": 0.25,\n        \"stall_ratio\": 0.000621,\n        \"total\": 66522790,\n        \"total_delta_us\": 621\n      },\n      \"notes\": [\n        \"parsed from the kernel PSI line grammar\"\n      ],\n      \"some\": {\n        \"avg10\": 0.2,\n        \"avg300\": 0.9,\n        \"avg60\": 0.26,\n        \"stall_ratio\": 0.000813,\n        \"total\": 70099878,\n        \"total_delta_us\": 813\n      },\n      \"state\": \"ok\"\n    },\n    \"irq\": {\n      \"full\": {\n        \"avg10\": 0.0,\n        \"avg300\": 0.03,\n        \"avg60\": 0.0,\n        \"stall_ratio\": 0.002597,\n        \"total\": 14543064,\n        \"total_delta_us\": 2597\n      },\n      \"notes\": [\n        \"parsed from the kernel PSI line grammar\"\n      ],\n      \"some\": null,\n      \"state\": \"ok\"\n    },\n    \"memory\": {\n      \"full\": {\n        \"avg10\": 0.2,\n        \"avg300\": 0.08,\n        \"avg60\": 0.12,\n        \"stall_ratio\": 0.0,\n        \"total\": 9284409,\n        \"total_delta_us\": 0\n      },\n      \"notes\": [\n        \"parsed from the kernel PSI line grammar\"\n      ],\n      \"some\": {\n        \"avg10\": 0.2,\n        \"avg300\": 0.09,\n        \"avg60\": 0.12,\n        \"stall_ratio\": 0.0,\n        \"total\": 9382000,\n        \"total_delta_us\": 0\n      },\n      \"state\": \"ok\"\n    }\n  },\n  \"root\": \"/proc/pressure\",\n  \"schema\": \"mori-pressure-v1\",\n  \"threshold\": {\n    \"label\": \"local (not calibrated)\",\n    \"metric\": \"avg10\",\n    \"value\": 10.0\n  },\n  \"verdict\": \"PRESSURE_OK\"\n}\n",
      "stderr": ""
    },
    {
      "timestamp_utc": "2026-10-22T08:37:33.013335Z",
      "command": "python3 -I tools/mori-pressure.py --warn-avg10 0.01",
      "exit_code": 1,
      "stdout": "{\n  \"findings\": [\n    {\n      \"avg10\": 0.2,\n      \"detail\": \"memory some avg10 0.20 is at or above the local (not calibrated) threshold 0.01\",\n      \"id\": \"PRESSURE_HIGH\",\n      \"kind\": \"some\",\n      \"resource\": \"memory\",\n      \"threshold_avg10\": 0.01\n    },\n    {\n      \"avg10\": 0.2,\n      \"detail\": \"io some avg10 0.20 is at or above the local (not calibrated) threshold 0.01\",\n      \"id\": \"PRESSURE_HIGH\",\n      \"kind\": \"some\",\n      \"resource\": \"io\",\n      \"threshold_avg10\": 0.01\n    }\n  ],\n  \"resources\": {\n    \"cpu\": {\n      \"full\": {\n        \"avg10\": 0.0,\n        \"avg300\": 0.0,\n        \"avg60\": 0.0,\n        \"total\": 0\n      },\n      \"full_system_undefined\": true,\n      \"notes\": [\n        \"parsed from the kernel PSI line grammar\",\n        \"system cpu 'full' is undefined by the kernel: reported, never used for a threshold\"\n      ],\n      \"some\": {\n        \"avg10\": 0.0,\n        \"avg300\": 0.0,\n        \"avg60\": 0.0,\n        \"total\": 7717793\n      },\n      \"state\": \"ok\"\n    },\n    \"io\": {\n      \"full\": {\n        \"avg10\": 0.2,\n        \"avg300\": 0.82,\n        \"avg60\": 0.25,\n        \"total\": 66522790\n      },\n      \"notes\": [\n        \"parsed from the kernel PSI line grammar\"\n      ],\n      \"some\": {\n        \"avg10\": 0.2,\n        \"avg300\": 0.9,\n        \"avg60\": 0.26,\n        \"total\": 70099878\n      },\n      \"state\": \"ok\"\n    },\n    \"irq\": {\n      \"full\": {\n        \"avg10\": 0.0,\n        \"avg300\": 0.03,\n        \"avg60\": 0.0,\n        \"total\": 14543131\n      },\n      \"notes\": [\n        \"parsed from the kernel PSI line grammar\"\n      ],\n      \"some\": null,\n      \"state\": \"ok\"\n    },\n    \"memory\": {\n      \"full\": {\n        \"avg10\": 0.2,\n        \"avg300\": 0.08,\n        \"avg60\": 0.12,\n        \"total\": 9284409\n      },\n      \"notes\": [\n        \"parsed from the kernel PSI line grammar\"\n      ],\n      \"some\": {\n        \"avg10\": 0.2,\n        \"avg300\": 0.09,\n        \"avg60\": 0.12,\n        \"total\": 9382000\n      },\n      \"state\": \"ok\"\n    }\n  },\n  \"root\": \"/proc/pressure\",\n  \"schema\": \"mori-pressure-v1\",\n  \"threshold\": {\n    \"label\": \"local (not calibrated)\",\n    \"metric\": \"avg10\",\n    \"value\": 0.01\n  },\n  \"verdict\": \"PRESSURE_HIGH\"\n}\n",
      "stderr": ""
    }
  ]
}
```

## 11. Provenance

- Capture harness (not committed, scratch only):
  `/fast/scratch/hyaku/mori-r24-a2/livepressure/capture.sh` plus the per-phase
  scripts that produced `capture.json` and `supp.json` … `supp7.json`. The
  assembled block above is the concatenation of those phases in execution order.
- Lane repo state was **not** modified by this seat. The only file it created in
  the lane repo is this report. `git log --oneline -1` (records 39, 64 and 65) moved
  from `f7eb430` to `06a7686` purely because *other* seats committed the C2 tool
  and the frozen cases while this capture was in flight; this seat ran no
  `git add`/`commit`/`stash`/`checkout`/`reset`/`pull`/`push` and no mutating `jj`
  command.
- Sibling overlap: `ScoutHostKernelConfig.md` (same wave) independently reads
  `/proc/config.gz` and `/proc/cmdline` and reaches the same three config values
  and the same "no `psi=` token" result. This seat's §2 is the independent second
  measurement of those bytes; the two agree. Nothing here contradicts that report;
  the distinct contribution of this seat is §3–§7 (the live `/proc/pressure/*`
  and `/sys/fs/cgroup/*` contents, the timed deltas, and the live run of the
  landed tool), which no other seat in this wave captured.

Confidence: **high** on the file contents, the enablement state, the identity of
the root-cgroup and system surfaces, the delta arithmetic, and the tool's live
output — all are direct byte observations with recorded exit codes. **Medium** on
the claim that the `/proc/pressure/*` → `EACCES` path is unreachable: it is
inferred from the observed `0666` mode plus the `CONFIG_PSI=y` / no-`psi=` state,
not from an attempted read as an unprivileged user (the seat ran with its normal
privileges, so no `EACCES` was provoked).
