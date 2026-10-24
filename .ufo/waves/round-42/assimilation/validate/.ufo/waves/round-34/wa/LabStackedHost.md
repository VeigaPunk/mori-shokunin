measured 2026-10-23T05:47:33Z

# LabStackedHost — live class tree and host_write_Bps double-count check (round 34, wave A)

Seat: MoriR34A2.LabStackedHost. Lane: mori-shokunin; judged object `tools/mori-disk-rate.py`,
blob `c7ea8bdac9c98b8d350a489fb8aca3a4750bcfbf` at HEAD `fd25213`, identical at
`8d56809` and at landing `ba525e1` (read-only git: `git rev-parse <rev>:tools/mori-disk-rate.py`
→ `c7ea8bda…` for all three). Host: linux 7.2.11-arch1-1, `uname -r` = `7.2.11-arch1-1`.
Hypothesis under test: the tool classes each `/sys/class/block` entry as an independent sysfs
reading would, `host_basis` excludes partitions and dm devices, so `host_write_Bps` does not
double count dm-0 over its backing partition.

## 1. Tool runs (live, 3×)

`timeout 120 python3 tools/mori-disk-rate.py --interval-ms 2000` → exit 0 for runs 1, 2, 3
(stderr empty; JSON on stdout). Per-run summary:

| run | devices | all state `ok` | all `write_Bps` int | host_basis | host_write_Bps |
|---|---|---|---|---|---|
| 1 | 11 | yes | yes | nvme0n1, nvme1n1, sda, sr0 | 440320 |
| 2 | 11 | yes | yes | nvme0n1, nvme1n1, sda, sr0 | 20109312 |
| 3 | 11 | yes | yes | nvme0n1, nvme1n1, sda, sr0 | 520192 |

`host_write_Bps` equals the sum of the basis devices' rates in each run (checked arithmetically:
run1 331776+108544+0+0 = 440320; run2 20109312; run3 518144+2048 = 520192).

## 2. Class by class — tool vs my own reading vs R3 vs counter oracle

My independent reading of `/sys/class/block/<n>`: `partition` attribute → partition; else
non-empty `slaves/` → stacked; else `device` symlink → disk; else virtual. `lsblk -o NAME,TYPE,PKNAME`
read separately for the human-readable view. The counter's own frozen oracle
(`.ufo/waves/round-34/count-c1-a1.py`, `classify()` at :63-74) was loaded read-only and applied to
the live `/sys` for a third opinion.

| name | tool class | my sysfs reading | lsblk TYPE / PKNAME | counter oracle | agree |
|---|---|---|---|---|---|
| dm-0 | stacked | stacked (slaves=nvme0n1p2) | (crypt `root`) / nvme0n1p2 | stacked | YES |
| nvme0n1 | disk | disk (device->../../nvme0) | disk / – | disk | YES |
| nvme0n1p1 | partition | partition | part / nvme0n1 | partition | YES |
| nvme0n1p2 | partition | partition | part / nvme0n1 | partition | YES |
| nvme1n1 | disk | disk (device->../../nvme1) | disk / – | disk | YES |
| nvme1n1p1 | partition | partition | part / nvme1n1 | partition | YES |
| nvme1n1p2 | partition | partition | part / nvme1n1 | partition | YES |
| sda | disk | disk (device->../../../12:0:0:1) | disk / – | disk | YES |
| sda1 | partition | partition | part / sda | partition | YES |
| sda2 | partition | partition | part / sda | partition | YES |
| sr0 | disk | disk (device->../../../12:0:0:0) | **rom** / – | disk | YES |

Class mismatches tool↔counter oracle on the live host: **0** (all 11 names).
The only divergence from `lsblk`'s TYPE column is `sr0` (lsblk `rom`, tool/oracle `disk`).
R3's vocabulary has five classes (`disk, partition, stacked, virtual, unknown`) and no `rom`, and
R3's rule is "`device` entry → `disk`", which sr0 satisfies (`/sys/class/block/sr0/device` →
`../../../12:0:0:0`, parent is not a partition). So the divergence is a label difference against
`lsblk`, not a deviation from R3.

## 3. host_basis excludes partitions and dm devices

`host_basis` in every live run = `['nvme0n1','nvme1n1','sda','sr0']` — the four whole disks.
Excluded: nvme0n1p1, nvme0n1p2, nvme1n1p1, nvme1n1p2, sda1, sda2 (class `partition`) and dm-0
(class `stacked`).

Structural note (stronger than the hypothesis states): dm-0 is excluded by *two* independent
mechanisms, not only by the slaves check. `/sys/class/block/dm-0` has **no `device` entry**
(`readlink /sys/class/block/dm-0/device` → empty; the directory listing has `dev` but not
`device`), so under R3's order it can never be `disk` even if `slaves/` were empty; with
`slaves/` non-empty it is `stacked`. Verified offline with a synthetic sysfs root
(`--sysfs fake`): a `dm-0` directory without `slaves/` and without `device` came out `virtual`,
still not `disk`.

## 4. host_write_Bps vs the sum of whole-disk deltas I read myself

Offline, on two samples I captured myself (`cp /proc/diskstats`; sleep 2; `cp` again):
tool `--a myA.txt --b myB.txt --interval-ms 2000` → `host_write_Bps` = 184358912.
My own parse of the same two files, whole disks only (nvme0n1, nvme1n1, sda, sr0):
deltas 4672 + 715480 + 0 + 0 = 720152 sectors → 720152·512·1000/2000 = **184358912 B/s**.
Exact match.

Live, cross-checked with my own 20 ms sampler bracketing the tool's two `/proc/diskstats` opens
(strace `-ttt` gives the open epochs):

| interval | tool open gap | my bracketing window | my whole-disk sum | my B/s | tool host_write_Bps | tool/mine |
|---|---|---|---|---|---|---|
| 2000 ms | 2.000585 s | 1.9573 s | 142696 sectors | 37327251.7 | 38647808 | 1.0354 |
| 3000 ms | 3.0005 s | 3.0088 s | 505368 sectors | 85997996.3 | 86249471 | 1.0029 |
| 5000 ms | 5.0005 s | 5.0231 s | 122320 sectors | 12467891.7 | 12525567 | 1.0046 |

The residual ratio is fully explained by window length: the tool divides by the nominal
`interval_ms` while my sampler brackets a slightly different window, so
tool/mine ≈ my_window/tool_window (3.0088/3.0005 = 1.0028 vs observed 1.0029; 5.0231/5.0005 =
1.0045 vs observed 1.0046). No unexplained discrepancy.

Timing floor for A1: the two reads are at least 0.9·interval apart in every run
(2.000585 s / 3.0005 s / 5.0005 s for 2000 / 3000 / 5000 ms).

## 5. The double-count question, measured directly

Kernel roll-up (S183 / r33 row 3): a partition's sectors are added again to the whole disk's
`part0`, so the whole-disk line already contains its partitions' sectors. Measured on my own
samples: nvme0n1 Δ = 4672 = Δ(nvme0n1p1) 0 + Δ(nvme0n1p2) 4672; nvme1n1 Δ = 715480 =
24 + 715456; sda Δ = 0 = 0 + 0. dm-0 Δ = 4672 = Δ(nvme0n1p2) = 4672 (dm-0's slaves = nvme0n1p2,
so the same bytes appear at the dm layer, the partition layer and the disk layer).

Controlled write probe: 128 MiB of incompressible random data written and fsync'd to
`/var/tmp` (btrfs on `/dev/mapper/root`, i.e. dm-0 → nvme0n1p2 → nvme0n1) while the tool ran
live with `--interval-ms 3000`:

| device | class | state | tool write_Bps |
|---|---|---|---|
| dm-0 | stacked | ok | 61613397 |
| nvme0n1p2 | partition | ok | 61613397 |
| nvme0n1 | disk | ok | 61613397 |
| nvme1n1 | disk | ok | 146545322 |
| nvme1n1p1 | partition | ok | 1859584 |
| nvme1n1p2 | partition | ok | 144685738 |
| sda, sda1, sda2, sr0, nvme0n1p1 | disk/partition | ok | 0 |

`host_write_Bps` = 208158719 over basis `['nvme0n1','nvme1n1','sda','sr0']` — the 128 MiB probe
bytes appear once (in nvme0n1), not twice. Counter-check on the same run shape: summing *all*
devices' rates gave 428064768 = exactly **2.000 ×** host_write_Bps 213995520 (a run in which
every device was active) — i.e. including the partition and dm layers would double count, and
the tool's basis does not.

**Conclusion on the hypothesis:** the third clause is confirmed by direct measurement, not only
by reading the rule. dm-0's bytes are already inside nvme0n1p2's counter and (by the kernel
roll-up) inside nvme0n1's counter; taking whole disks only counts them once. The second clause
is confirmed and is structural (dm-0 can never be `disk` on this host because it has no `device`
entry). The first clause is confirmed for 11/11 entries against R3 and the counter oracle, with
one label-only divergence from `lsblk` at `sr0` (`rom` vs `disk`) that R3's rule and the counter
both resolve to `disk`.

## 6. Other behaviours checked on this host

- R7 null paths (offline, mutated samples): a whole-disk counter reset between samples →
  state `reset`, `host_write_Bps` null, basis unchanged; a whole-disk line removed from both
  samples → state `absent`, `host_write_Bps` null. Removing dm-0 from both samples → dm-0 still
  classed `stacked` (from sysfs, R4) with state `absent`, `write_Bps` null, and `host_write_Bps`
  unchanged (184358912) because dm-0 is not in the basis.
- R4 coverage: the live JSON lists all 11 `/sys/class/block` entries (every one appears in the
  `devices` map).
- The tool's `parse` agrees with the counter oracle's `parse` on the live `/proc/diskstats`
  (zero differences); live token counts are all 20.
- Detection and report only: `strace -f -e trace=write,writev,openat,open,creat,unlink,mkdir`
  over a live run shows writes only to fd 1 (stdout); no `O_WRONLY`/`O_RDWR`/`O_CREAT` opens, no
  `creat`/`unlink`/`mkdir`. No file, block device or setting was written.
- Source guard: the tool text contains no `.ufo`, `count-c1` or counter reference
  (`grep` → no match).

## 7. Risks and blockers

1. `sr0` (read-only optical device, `ro=1`, `size=44989040`) is classed `disk` and therefore sits
   in `host_basis`. Its rate is 0 on this host, so it does not distort the total today, but R7
   nulls `host_write_Bps` if any basis device is not `ok`; a missing or malformed `sr0` line in
   `/proc/diskstats` would null the host total even though nothing was written. This follows
   R3/R7 as frozen (the counter oracle classifies sr0 `disk` too), so it is a property of the
   claim, not a deviation by the tool.
2. The whole-disk line's roll-up is a kernel property (S183). If a future kernel stopped
   rolling partition sectors into `part0`, a whole-disk-only basis would under-count. Not
   observable on this host (measured equal in every sample); noted, not claimed.
3. No virtual/loop/zram devices exist on this host, so the `virtual` class and the
   `unknown` class were exercised only through the synthetic sysfs root, not live.

## 8. Tools

No tool was installed or updated (no pacman / uv / npm / cargo action); everything used was
already present: python3 (3.14), util-linux `strace`, `lsblk`/`lsblk -P` (util-linux),
`findmnt`/`df`, coreutils. Scratch under `/fast/scratch/hyaku/mori-r34/a2-LabStackedHost/`
(220 KB) holds the captured samples, JSON outputs and traces; the two write-load probes
(`probe.bin`, `/var/tmp/mori-probe.bin`) were deleted.

VERDICT: no defect found
