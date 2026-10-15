# Lesson — the free measurements of a one-shot read-only gate are the source's own aggregates; rates the source does not maintain cost a dwell, and no counter may be read without its baseline

date: 2026-10-15 · lane: mori-shokunin · round: 7 · source seat: lessons-distiller (flash wave)

Measured on host kernel `7.2.3-arch1-3`, boot 0 begun 2026-10-15T16:37:48Z,
against `tools/mori-census.sh` sha256
`af2d4e79e69b70bb0b5aecd6acc9608fc7c16b0716766d4a60310e0689d350d7`
(`VERSION=census-r3`) and the frozen oracle `tools/mori-silence-cases.sh` sha256
`3307761a04a1eab8f33859a69d2eb63fb6312afb8f8041f7b09da4544be174b9`.
Every measurement below is read-only; the only files written are
`/tmp/mori-r7-lessons*` and this note. Detection/report only — nothing here
remediates.

Context: round 7's axis is coverage, and its registered claim is the four
surface gaps of `corpus/knowledge/observability-surfaces-r2.md` (Gaps
sections: tmux relevance, memory-pressure threshold, disk write-rate,
`state_rounds` count-only). This note distils the general measurement-cost rule
those four gaps instantiate; it is not the verdict on their closure.

## The lesson

In a one-shot, read-only, stateless gate — one process, no resident sampler, no
state file, "live mode writes nothing" (`tools/mori-census.sh:21`) — whether a
measurement is affordable is decided by one question: **does the source already
maintain the aggregate?**

1. **Free (one read).** Cumulative counters the source keeps for you —
   `memory.events` fields, journal event counts, `/proc/diskstats` sector
   totals, PSI `total=`; windowed averages the kernel keeps for you — PSI
   `avg10/avg60/avg300` and per-cgroup `memory.pressure`; high-watermarks —
   `memory.peak`; and the contents of files the gate already lists
   (`.ufo/state/*.round` values; the session names `tmux ls -F` returns in the
   same invocation). Marginal cost: the read you were already making.
2. **Not free (a dwell or state).** Rates the source does not aggregate. Disk
   write throughput exists in no kernel file on this host: `/proc/diskstats`
   holds only since-boot sector totals, so bytes/s requires two reads separated
   by a dwell (added gate latency) or persisted state between runs (forbidden by
   the read-only contract). Measured below: 3 s of dwell to say ≈0.9 MiB/s,
   against a 2.6 s whole-gate budget.
3. **The billing condition.** Every cumulative counter answers "ever since X",
   and X is not printed in the number. The same field name can read different
   numbers for a legitimate reason — a boot, a cgroup re-creation, a service
   restart — and `boot=current` (`tools/mori-census.sh:389`) names the policy,
   not the instance. Printing the baseline is itself free
   (`/proc/sys/kernel/random/boot_id`, the cgroup directory ctime, the lane's
   launch epoch), and without it a cross-run comparison of the same counter is
   unsound.

The refinement over the intuitive form ("since-boot counters are the honest
free lunch") is point 3, forced by measurement: the counters are free, but a
receipt pair spanning the boot seam is not comparable, and the seam is
invisible unless the baseline is printed. The reboot measured below flipped
four census rows at byte-identical script SHA.

## What was measured (2026-10-15T19:24–19:27Z, all read-only)

### 1. PSI exists and maintains its own windows — the free rate

```
$ ls -l /proc/pressure/
total 0
-rw-rw-rw- 1 root root 0 Oct 15 16:04 cpu
-rw-rw-rw- 1 root root 0 Oct 15 16:23 io
-rw-rw-rw- 1 root root 0 Oct 15 16:23 irq
-rw-rw-rw- 1 root root 0 Oct 15 16:23 memory
$ uname -r
7.2.3-arch1-3
```

The [kernel PSI documentation](https://docs.kernel.org/accounting/psi.html)
defines the ratios as "recent trends over ten, sixty, and three hundred second
windows" and `total=` as absolute stall time (µs); the same file format exists
per cgroup (`memory.pressure`), confirmed live below.

Two reads three seconds apart, no deliberate load, nothing sampled in between —
the average moved anyway, because the kernel samples continuously:

```
T0 2026-10-15T19:24:07Z
/proc/pressure/io:     some avg10=0.00 avg60=0.07 avg300=0.03 total=15948128
/proc/pressure/memory: some avg10=0.01 avg60=0.05 avg300=0.04 total=10215486
T1 (sleep 3)
/proc/pressure/io:     some avg10=0.00 avg60=0.07 avg300=0.03 total=15956427
/proc/pressure/memory: some avg10=0.19 avg60=0.08 avg300=0.05 total=10252446
```

`memory some avg10` moved 0.01 → 0.19 and `total` advanced 36,960 µs while the
reader did nothing but read. The per-cgroup arm is equally free:

```
$ cat /sys/fs/cgroup/user.slice/user-1000.slice/memory.pressure
some avg10=0.00 avg60=0.00 avg300=0.00 total=5623670
full avg10=0.00 avg60=0.00 avg300=0.00 total=5031228
```

At `af2d4e79` the census reads no PSI file at all:
`grep -nE 'diskstats|pressure|\.peak' tools/mori-census.sh` → no match.

### 2. A rate the source does not maintain costs a dwell

```
$ awk '/ nvme0n1 /{print "sectors_written="$10}' /proc/diskstats   # T0 19:24:10Z
sectors_written=200924364
# sleep 3
sectors_written=200929868                                          # T1 19:24:13Z
```

5,504 sectors × 512 B = 2,818,048 B ≈ 2.69 MiB over 3 s ≈ **0.90 MiB/s** — and
that number exists only because the measurement slept. Against the gate's own
budget, measured live at byte-identical SHA:

```
$ time bash tools/mori-census.sh                       # 19:24:36Z
real 0m2.615s   … MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)   rc=1
$ time bash tools/mori-census.sh --selftest
real 0m2.269s   … MORI_CENSUS_SELFTEST: PASS (30 cases, 30 passed, 0 failed)   rc=0
```

A write-rate probe with a 60-second window would multiply the whole gate by
~24×; with a 3-second window it would double it. There is no local sampler to
borrow either: `which iostat` → none; `vmstat` exists.

### 3. The baseline seam, measured across a reboot

Boot 0 began **2026-10-15T16:37:48Z** (`uptime -s`); `journalctl --list-boots`
shows boot −1 ending 16:31:29Z and boot 0 from 16:38:07Z; the user cgroups were
(re)created at 16:38:09–16:38:10Z (`stat -c %z` on `user.slice`,
`user-1000.slice`, `user@1000.service`). The r2 receipt
(`observability-surfaces-r2.md:47-82`, 15:27:57Z, **previous boot**) and the
live run (19:24:36Z, **this boot**) are the same bytes on the same host:

| frozen census row | r2 receipt (boot −1) | live now (boot 0) |
|---|---|---|
| `SURFACE journal` | `oom_kill=1 kill_signal=0 segfault=718` | `oom_kill=0 kill_signal=1 segfault=45` |
| `SURFACE cgroup` | `oom_kill=1 … current=20467998720` | `oom_kill=0 … current=23859130368` |
| `SURFACE tmux` | `ok (… sessions=1)` | `unavailable (cmd=tmux ls; rc=1)` |
| `SURFACE watchdog` | `state_rounds=21` | `state_rounds=21` (persists — files, not counters) |

The cgroup reset is the cgroup instance's lifetime, not the boot per se:
`memory.events` is cumulative per cgroup instance, and the instance is
recreated at boot/restart. The census already documents the attribution trap
this caused (`tools/mori-census.sh:421-434`: a desktop OOM event re-fired `crit`
every run of the previous boot); after the reboot the same field reads 0.
`boot=current` labels the scope; only
`/proc/sys/kernel/random/boot_id` (`a8389953-f5b9-48b5-9107-74f1162db9ae`,
free to read) or the cgroup ctime pins the instance.

### 4. Free data the gate already walks past

`.ufo/state` holds 21 `*.round` files with 1–3-byte values, and the watchdog row
(`tools/mori-census.sh:233-256`) walks every one of them to print
`state_rounds=21` — count only. The values, free in the same walk:

```
aggregator=10 audio=1 chousa=1 game-dev-2d=1 game-dev-3d=1 kagi=16 kaidoku=1
kake=16 kama=1 kasegi=17 kengaku=13 kotoba=16 kumitate=18 lore=1 mado=1 mori=2
protocol=14 revenger=1 tabi=1 tameshi=1 tsukuroi=1
```

Twelve of the 21 lane ids are outside the 9-lane roster
(`protocol aggregator kasegi kengaku kake kumitate kotoba kagi kama`) — visible
here, invisible in the count. The silence probe shows the intended pattern in
the same file: it reads exactly one lane's value for its row-7 test
(`read_file "$STATE_DIR/$lane.round"`, `tools/mori-census.sh:749`).

Same for tmux: `probe_tmux` (`tools/mori-census.sh:883-898`) counts output lines
of `tmux ls`. The identity of the sessions — name, created/activity timestamps,
window count, attached — is in
`tmux ls -F '#{session_name}|#{session_created}|#{session_activity}|…'`, the
*same single invocation*; the surface is count-only by choice, not by cost.
The r2 receipt's `sessions=1` and today's `unavailable` are the same
instantaneous resource present then, absent now.

### 5. Free signals vs caps: memory pressure on this host

```
$ cat /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/memory.peak
28801970176
$ cat /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/memory.max
max
```

`memory.max` is unlimited on both the slice and the service scope, so a
percent-of-cap pressure threshold is not constructible here without inventing a
value. The honest free signals are PSI (stall share, baseline-free windows) and
`memory.peak` (high-watermark, baseline = cgroup instance creation). Any
threshold installed on them is local to this host and must be labeled so — this
note proposes no number.

### 6. The tmux row has no selftest case

`grep -n 'SURFACE tmux' tools/mori-census.sh` → no match at `af2d4e79`. The
fixture defines a tmux stub (`:1026`, `fx_session: 1 windows`) but no case
asserts the row, its count, or its unavailable arm — the header's `unavailable`
promise is fixture-unproved, and the 30-case suite is silent on this surface.

## Round-7 gap map — what each registered gap costs (as of the frozen SHAs)

| gap (`observability-surfaces-r2.md` §) | quantity class | honest cost |
|---|---|---|
| tmux session relevance (§7) | instantaneous resource + identity | free: names/timestamps in the same `tmux ls` call; relevance is a declared match rule, not a measurement; absent server = `unavailable`, not DRIFT (`:890-893`) |
| memory-pressure threshold (§4) | pressure (source aggregates) | free: PSI `avg10/60/300` (host + per cgroup), `memory.peak` with instance baseline; caps absent here (`max`), thresholds labeled local |
| disk write-rate (§5) | throughput (source does not aggregate) | not free: dwell ≥ window or state across runs; free substitutes answer different questions — PSI `io` (stall, not bytes), `diskstats` sectors (magnitude, not rate); else an explicit deferral with the precondition named |
| `state_rounds` count-only (§1) | file contents already walked | free: same walk, read the values; no rate, no window |

Status at the pre-round SHAs (`af2d4e79…`): none of the four was closed — the
census had no PSI, no `diskstats`, no `memory.peak`, no state values, and a
count-only tmux row (citations above).

### Round-7 landing addendum — verified 2026-10-15T19:41Z

At `tools/mori-census.sh` sha256
`75dd142d6a597ffb7b6da0868bc1193f99490de81be3a4023f19de2b31f71bd2`
(`census-r4`; verified 19:41Z, stable ≥100 s before the battery and unchanged
through it), and again at
`c7c3569b842ab3911cbfdf415eb7023766c950c60f354af95f6a4f020b5671af` (19:44Z,
stable ≥80 s), with the rebased oracle
`97035decd1606247924fee13367412fb8fa2ae06e5987f9b7cf37baa2c794a1a` at both
runs. The census iterated through 20+ observed revisions in this seat's window
(19:27–19:44Z) and the oracle moved once more as this note closed
(`448f7723…` by 19:44:30Z): both implementing seats were still iterating, so
treat these as verified snapshots, not final round bytes. All four gaps landed
as measured probes, each choosing the free or explicitly-labeled measurement
this note's taxonomy predicts (row fragments verbatim from the 19:41Z run):

- **tmux relevance** — sessions classified by pane cwd under the fleet root
  (`rule=pane_cwd_under_fleet_root`); foreign sessions reported
  (`TMUX_FOREIGN_SESSION`), unreadable pane data disclosed as
  `relevance=unavailable`, never guessed. Live row at measurement time:
  `SURFACE tmux: unavailable (cmd=tmux ls; rc=1)` — no server was running.
- **memory pressure** — `psi_some_avg10=0.00 psi_full_avg10=0.00 psi_source=ok
  psi_warn_avg10=10` (PSI window, threshold labeled local); fill pressure with
  the slice limit `max` falls back to host scope and says so
  (`mem_fill_pct=unavailable mem_fill_scope=host-ram host_mem_avail_pct=53`).
- **disk write-rate** — the dwell was declined; the row carries the since-boot
  average *and its divisor*: `io_basis=since-boot
  io_avg_since_boot=dm-0:9745912Bps/11040s
  io_avg_unavailable=tmpfs:not-a-block-device` — a baseline-named average, never
  an instantaneous rate.
- **state values** — read in the same walk: `state_rounds=21
  state_rounds_max=18 state_lag=0 state_ahead=0 state_cmp=21
  state_val_unreadable=0`, values compared against each lane's last launch
  round, unreadable values counted rather than zeroed.

Verdict machine green at these bytes, and identically at `c7c3569b…` (19:44Z):
`--selftest` →
`MORI_CENSUS_SELFTEST: PASS (45 cases, 45 passed, 0 failed)` exit 0; live →
`MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` exit 1;
oracle → `MORI_SILENCE_CASES: matched=28 total=28` exit 0. The oracle rebase is
8 added lines pinning `MORI_UPTIME`/`MORI_DISKSTATS` fixtures
(`git diff --stat tools/mori-silence-cases.sh` → `8 +`, no graded expectation
changed) — additive, matching the round's re-baseline rule.

What the landing validates here: a since-boot counter divided by boot uptime
yields a free, baseline-named average — the honest substitute for a rate the
source does not maintain — and it travels with its divisor (`…/11040s`); and
every threshold that can fire on this host carries `threshold_label=local`
rather than an invented constant.

## Applying it (any lane)

- Classify before adding: (a) source-aggregated — counter/average/peak/object
  contents already walked — costs one read; (b) a rate the source does not
  maintain costs a dwell or persisted state; a read-only gate must not persist,
  so name the precondition and defer rather than smuggling a sleep into a probe.
- Print the baseline next to every cumulative counter: boot id, cgroup/instance
  creation time, process start, or the window anchor. A number without its
  baseline is comparable only within one instance.
- Re-run counter-based gates across a reboot/restart boundary as a regression:
  finding ids can stay identical while every cumulative number resets
  (measured: four rows above).
- Read what you already walk: count-only file and session enumerations are
  foregone free data, not savings.
- Prefer the kernel's maintained window to a hand-rolled sampler; the
  hand-rolled one pays a dwell the kernel has already paid.

## Limits

- One host, one kernel (`7.2.3-arch1-3`), PSI enabled; the cgroup paths are this
  host's user-slice layout. PSI availability is a kernel-config question, not a
  universal.
- The reboot evidence pairs the r2 note's receipt (15:27Z, previous boot) with
  the live run (19:24Z); the boot boundaries come from `uptime -s`,
  `journalctl --list-boots`, and cgroup ctimes — three independent reads, all
  quoted above. The r2 receipt remains the canonical record of the previous
  boot's numbers; this note only reads it.
- "Free" here means zero added latency or state for the gate; it says nothing
  about the kernel's own accounting cost.
- All numbers are mutable live observations pinned to the clocks quoted. No
  threshold value is proposed; a threshold an implementer installs later is
  local and needs its own labeling.