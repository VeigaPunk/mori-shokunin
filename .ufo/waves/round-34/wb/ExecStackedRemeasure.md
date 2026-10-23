measured 2026-10-23T07:48:33Z

# ExecStackedRemeasure — dm-0 stacked-device write multiplicity, re-measured live

Seat: MoriR34A3.ExecStackedRemeasure. Lane: mori-shokunin. Judged object unchanged and not
touched: `tools/mori-disk-rate.py`, blob `c7ea8bdac9c98b8d350a489fb8aca3a4750bcfbf`
(`git rev-parse fd25213:tools/mori-disk-rate.py`, also at `8d56809`, `ba525e1`, and at current
HEAD `5216d78`). Host: `uname -r` = `7.2.11-arch1-1`. Claim under test, verbatim from
`/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_README.md:552-554`:

> Round 34 observed it again on this host (dm-0's delta equals its slave's; a write through dm-0
> appears once in the whole-disk total and twice in a sum over every line, …

## 1. Does a stacked device exist? Which, and is my scratch on it?

Every `/sys/class/block` entry was checked for a non-empty `slaves/`; exactly one has one:

| device | slaves | dm name | dm uuid | class marker |
|---|---|---|---|---|
| `dm-0` | `nvme0n1p2` | `root` | `CRYPT-LUKS2-75698eb388634f9584465d52efe0fc8d-root` | no `device` entry |

`lsblk -s` shows the chain `root (crypt) → nvme0n1p2 (part) → nvme0n1 (disk)`; `dm-0` size
1949292544 sectors vs slave 1949325312 — exactly 32768 sectors (16 MiB) smaller, the LUKS2 header.
All ten other entries have empty `slaves/`. There is no md, LVM, loop or zram device.

**My scratch is not on the stacked device, so I wrote nothing.** `findmnt -T
/fast/scratch/hyaku/mori-r34/a3-ExecStackedRemeasure` → `/fast /dev/nvme1n1p2 xfs`, and
`lsblk -s` shows `nvme1n1p2 → nvme1n1` with no mapper above it. Per the item's gate, the 512 MiB
`dd` was **not run**; all load observed below is ambient system I/O on `/dev/mapper/root`, which
is the same substrate the attempt-2 report probed (`findmnt -T /var/tmp` →
`/dev/mapper/root[/@]` btrfs — confirms their probe traversed dm-0).

## 2. Measurement

One timed pair, 30 s window, midpoint interval exactly 30000 ms, samples kept at
`/fast/scratch/hyaku/mori-r34/a3-ExecStackedRemeasure/{A,B}.diskstats`. Per-device sector deltas
(field 10, sectors written):

| device | Δ reads-sectors | Δ writes(count) | Δ write-sectors | MB |
|---|---|---|---|---|
| **dm-0** (stacked) | 27713856 | 12426 | **219728** | 112.501 |
| **nvme0n1p2** (slave, partition) | 27713864 | 9758 | **219728** | 112.501 |
| **nvme0n1** (whole disk) | 27713848 | 9758 | **219728** | 112.501 |
| nvme0n1p1 | 0 | 0 | 0 | 0 |
| nvme1n1 | 1450504 | 2246 | 254896 | 130.507 |
| nvme1n1p1 / nvme1n1p2 | 670896 / 779608 | 63 / 2183 | 3800 / 251096 | 1.946 / 128.561 |
| sda, sda1, sda2, sr0 | 0 | 0 | 0 | 0 |

- `Δ(dm-0) == Δ(nvme0n1p2) == Δ(nvme0n1) == 219728` sectors, bit-exact. The three identical
  values also hold absolutely at sample B: `dm-0.wsec = nvme0n1p2.wsec = 732087680`.
- Sector counts mirror; **write counts do not** (12426 vs 9758) — dm-crypt sees the small writes
  the lower layer merges. Any claim resting on I/O *counts* would not reproduce; the sector
  equality is the invariant.
- Read sectors are *not* exactly equal (dm-0 27713856 vs slave 27713864, 8 sectors; cumulative
  gap 3830 sectors), so the mirroring is a write-counter property, not a whole-line property.
- Kernel roll-up confirmed: at sample B, `nvme0n1.wsec 732088118 = p1 438 + p2 732087680`, exactly.

Tool run once on that pair, `--interval-ms 30000` (exit 0):

- `host_basis` = `['nvme0n1','nvme1n1','sda','sr0']` (the four class-`disk` devices).
- `host_write_Bps` = **8100249**; recomputed from the per-device rates as
  3750024 + 4350225 + 0 + 0 = 8100249, exact.
- Per-device: `dm-0` class `stacked` 3750024; `nvme0n1p2` class `partition` 3750024;
  `nvme0n1` class `disk` 3750024. **Three identical rates.**
- A write through dm-0 therefore appears **once** in `host_write_Bps` (via `nvme0n1`; `dm-0` is
  excluded as `stacked`) — reproduced exactly — and **three times** in a naive sum over every
  reported line: naive 19950521 B/s vs host 8100249 B/s (2.462952×), with `dm-0`'s 3750024
  counted three times (`dm-0`, `nvme0n1p2`, `nvme0n1`).

**The observation reproduces; the numeral "twice" does not.** A dm-crypt device stacked on a
*partition* is written to three diskstats lines (mapper, partition, whole disk). "Twice" is
correct only for a mapper stacked directly on a whole disk, or for a sum that excludes
`partition`-class lines — excluding them here gives 3750024×2 = 7500048, and `dm-0` is then
counted exactly twice. The frontier note's sentence is therefore accurate in mechanism and wrong
in its count for this host's topology; it should read "three times" (or "twice, excluding
partition lines").

VERDICT: observation reproduced

## Audit of .ufo/waves/round-34/wa/LabStackedHost.md

Independence: the measurement and the verdict above were taken from the bytes before this file
was opened.

VERDICT: agree — Tool blob `c7ea8bda…` identical at `fd25213`, `8d56809`, `ba525e1`. `git rev-parse <rev>:tools/mori-disk-rate.py` returns that hash for all three, and for current HEAD `5216d78`.
VERDICT: agree — Host `7.2.11-arch1-1`. `uname -r`.
VERDICT: agree — `host_basis` = `['nvme0n1','nvme1n1','sda','sr0']` and `host_write_Bps` is the arithmetic sum of those rates. My run: same basis, 3750024+4350225+0+0 = 8100249 = reported host total.
VERDICT: agree — 11 devices, all state `ok`, all `write_Bps` integers. My run enumerates the same 11 and every state is `ok`.
VERDICT: agree — Class table. Independent sysfs read: `dm-0` has `slaves/` = `nvme0n1p2` → stacked; `nvme0n1p1/p2`, `nvme1n1p1/p2`, `sda1/sda2` carry a `partition` entry; `nvme0n1`, `nvme1n1`, `sda`, `sr0` have a `device` entry and no `partition` entry.
VERDICT: agree — `sr0` is `disk` under R3 and diverges from `lsblk`'s `rom`; size 44989040. `/sys/class/block/sr0/device` exists, `/sys/class/block/sr0/partition` does not, `size` = 44989040.
VERDICT: agree — `dm-0` has no `device` entry, so R3 can never call it `disk`; a synthetic sysfs root with `class/block/dm-0` (no `slaves/`, no `device`) yields `virtual`. `[ -e /sys/class/block/dm-0/device ]` → NO; my `--sysfs fake` run returned `{'class': 'virtual', ...}`.
VERDICT: agree — Kernel roll-up: whole-disk Δ = Σ partition Δ. Sample B: `nvme0n1.wsec 732088118 = 438 + 732087680`, and the 30 s Δ 219728 = p1 0 + p2 219728.
VERDICT: agree — `Δ(dm-0) = Δ(nvme0n1p2)` and the same bytes appear at dm, partition and disk layers. 219728 on all three lines, absolute counters equal, three identical rates.
VERDICT: agree — 128 MiB probe through `/var/tmp` (btrfs on `/dev/mapper/root`) gives `dm-0 = nvme0n1p2 = nvme0n1 = 61613397` and the bytes appear once in `host_write_Bps`. I did not rerun the probe (my scratch is not on the stacked device, §1); ambient load reproduces the identical-triple pattern and the once-only host count. The stated B/s value itself is [INFERENCE] from their run, unrerun.
VERDICT: disagree — "summing all devices' rates gave 428064768 = exactly 2.000 × host_write_Bps 213995520". 2 × 213995520 = 427991040, so the stated sum is 2.000345×, not exactly 2.000; and 2.000 is not a property of the shape: my run gives naive/host = 19950521/8100249 = 2.462952×, with dm-0's bytes counted three times.
VERDICT: agree — §4 rows 3000/5000: residual equals the window ratio. Recomputed 3.0088/3.0005 = 1.00277 vs stated 1.0029, and 5.0231/5.0005 = 1.00452 vs stated 1.0046; implied tool sectors equal the sampler's (505368, 122320), so the residual is window-only.
VERDICT: disagree — §4 row 2000 claims a 1.9573 s "bracketing" window around a 2.000585 s open gap and "no unexplained discrepancy". A 1.9573 s window cannot bracket two opens 2.000585 s apart; and that row's own numbers imply tool sectors 150968 vs sampler 142696 (ratio 1.0580) where containment predicts 1.0221, while the window-only prediction for tool/mine is 0.9784 against the observed 1.0354. The 2000 ms row carries ~3.5 % unexplained, so the blanket "fully explained" sentence is false for it.
VERDICT: agree — Offline `host_write_Bps` 184358912 = 720152 sectors × 512 × 1000 / 2000. Recomputed exactly 184358912.0.
VERDICT: agree — R7 null paths: removing `dm-0` from both samples leaves it `stacked` (from sysfs), state `absent`, `write_Bps` null, and `host_write_Bps` unchanged. My stripped-sample run: `{'class': 'stacked', 'state': 'absent', 'write_Bps': None}`, host total still 8100249.
VERDICT: agree — Live `/proc/diskstats` token counts are all 20. `awk '{print NF}' /proc/diskstats | sort -u` → single value `20`.
VERDICT: agree — Detection and report only: no `O_WRONLY`/`O_RDWR`/`O_CREAT` opens, no `creat`/`unlink`/`mkdir`. My own `strace -f -e trace=openat,open,creat,unlink,mkdir` over an offline run: 0 matches, 2 `/proc/diskstats` opens, 154 trace lines.
VERDICT: agree — Source guard: tool text contains no `.ufo` or `count-c1`. `grep -c '\.ufo\|count-c1' tools/mori-disk-rate.py` → 0.
VERDICT: agree — Both write-probe files were deleted. `/var/tmp/mori-probe.bin` and `/fast/scratch/hyaku/mori-r34/a2-LabStackedHost/probe.bin` both absent.
VERDICT: agree — First line `measured 2026-10-23T05:47:33Z` is consistent with the file's mtime. `stat` → `2026-10-23 02:48:19 -0300` = 05:48:19Z, 46 s later.

AUDIT: agree 18 / disagree 2

## Risks and blockers

1. The frontier note's "twice" must be corrected to "three times" (or "twice, excluding partition
   lines") before it lands; the report it cites describes three layers even while its §5
   counter-check says 2.000×.
2. `sr0` (class `disk`, rate 0) sits in `host_basis`, so a missing `sr0` line would null the host
   total although nothing was written. That is R3/R7 as frozen, not a tool defect; unchanged by
   this wave.
3. The 512 MiB write probe was not run: no scratch path of mine lies on `dm-0`. The reproduction
   rests on ambient I/O over the same mapper, which was sufficient because the three counters
   moved by the identical 219728 sectors.
4. No tool was installed or updated (no pacman / uv / npm / cargo action; pacman transactions are
   paused host-wide and none was attempted). Scratch evidence, 44 KB total, under
   `/fast/scratch/hyaku/mori-r34/a3-ExecStackedRemeasure/` (`A.diskstats`, `B.diskstats`,
   `A2/B2` stripped, `tool.json`, `strace.out`, `sample.py`, `interval.txt`); no load file was
   created and nothing is left running.

Files changed: `.ufo/waves/round-34/wb/ExecStackedRemeasure.md` (this report) only.
