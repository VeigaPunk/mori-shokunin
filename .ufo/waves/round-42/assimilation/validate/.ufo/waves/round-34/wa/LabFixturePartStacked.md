measured 2026-10-23T05:46:29Z

# Lab — partition/stacked fixture classes (seat MoriR34A2.LabFixturePartStacked)

Attacks: the hypothesis that `tools/mori-disk-rate.py` classes a fake sysfs tree correctly per contract
R3 for (1) a disk with two partitions, (2) a dm device on a partition, (3) an md raid1 over two
partitions, (4) a dm device over an md device, (5) a partition whose dir also has non-empty slaves,
(6) a disk with an empty slaves dir — and reports `host_basis`/`host_write_Bps` per R7.

Object: `git cat-file -p 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3:tools/mori-disk-rate.py`
sha256 `370932deb525b95135f0c30e4caaf2666b95c6feeffe76b70f06b48c09caa74b`; identical to the
lane working-tree file (same sha256). Run from a scratch copy, offline arm only.

## Method

Trees under `/fast/scratch/hyaku/mori-r34/a2-LabFixturePartStacked/`, built as the kernel lays them
out — measured on the live host first:

- `ls -la /sys/class/block/sda` → `device -> ../../../12:0:0:1`, `slaves/` (empty), `holders/`, no `partition`.
- `ls -la /sys/class/block/sda1` → `partition` file, `holders/`, **no** `device`, **no** `slaves/`.
- `readlink /sys/class/block/dm-0/device` → empty (no link); `/sys/class/block/dm-0/slaves/nvme0n1p2 -> ...`
- `class/block/<name>` is a symlink into `devices/...`; a partition lives under `<disk>/<part>`.

Exact shapes built (paths relative to `<fixture>/sys`): `class/block/<n>` → `../../devices/...`
symlink; a whole disk dir e.g. `devices/pci.../block/sda` with `device -> ../../` (the parent device
dir), empty `slaves/`, `holders/`; a partition dir nested under its disk, `.../block/sda/sda1`, with a
`partition` file and `holders/md0`, **no** `device`, **no** `slaves/`; dm/md at
`devices/virtual/block/<n>` with `holders/` and `slaves/<slave>` relative symlinks, no `device`.
Two 14-token diskstats samples, interval 1000 ms; rate = (B−A)·512·1000/1000 B/s. Verified by hand and
cross-checked against the frozen oracle (`count-c1-a1.py`, imported read-only).

Measured tree evidence (fixture B): `class/block/dm-0 -> ../../devices/virtual/block/dm-0`;
`class/block/nvme0n1p2 -> ../../devices/.../nvme0n1/nvme0n1p2`; `.../nvme0n1/device -> ../../`;
`.../dm-0/slaves/nvme0n1p2 -> ../../../../pci0000:00/...`; `ls -a .../nvme0n1p2` → `holders partition`;
`ls -a .../dm-0` → `holders slaves`; `ls -a .../nvme0n1` → `device holders nvme0n1p2 slaves`.

Command per fixture:
`python3 mori-disk-rate.py --a a.diskstats --b b.diskstats --sysfs <fx>/sys --interval-ms 1000` (rc 0).

## Results (measured; "✓" = equals hand value and frozen oracle)

### A — disk with two partitions
sda A=1000 B=1100 → 100·512 = 51200; sda1 500→520 → 10240; sda2 700→705 → 2560.
classes sda disk, sda1/sda2 partition; `host_basis ["sda"]`; `host_write_Bps 51200` (partition writes
already inside the whole-disk counter, S183). ✓
VERDICT: no defect found

### B — dm device on a partition
nvme0n1 2000→2200 → 102400; nvme0n1p2 900→950 → 25600; dm-0 300→350 → 25600.
classes nvme0n1 disk, nvme0n1p2 partition, dm-0 stacked; basis `["nvme0n1"]`; host 102400. ✓
VERDICT: no defect found

### C — md raid1 over two partitions
sda 1000→1100 → 51200; sdb 2000→2100 → 51200; sda1 500→560 → 30720; sdb1 500→560 → 30720; md0 1000→1120 → 61440.
classes sda/sdb disk, sda1/sdb1 partition, md0 stacked; basis `["sda","sdb"]`; host 102400. ✓
VERDICT: no defect found

### D — dm over md over the two partitions
dm-0 2000→2120 → 61440, md0 1000→1120 → 61440 (both stacked, excluded); sda/sdb as in C.
basis `["sda","sdb"]`; host 102400 — no double count through the two stacking layers. ✓
VERDICT: no defect found

### E — partition whose dir also has non-empty slaves
sda1 carries a `partition` file *and* `slaves/sda2`. Measured class `partition` (R3 checks the partition
entry before slaves), rate 10240; basis `["sda"]`; host 51200. ✓ (matches R3's stated order)
The kernel does not produce this shape (verified: partitions get `holders/`, never `slaves/`).
VERDICT: no defect found

### F — disk with an empty slaves dir
sda has `device` + empty `slaves/` → `disk`, 100·512 = 51200; loop0 (no device link, empty slaves) → `virtual`,
delta 0 → 0 (state ok). basis `["sda"]`; host 51200. ✓ Empty slaves is correctly not stacking.
VERDICT: no defect found

### G (extra) — disk in sample A only
sda state `gone`, rate null; basis `["sda"]` non-empty but not all ok → `host_write_Bps null`. ✓
VERDICT: no defect found

### H (extra) — dm-mapped partition (BLKPG), no `partition` file per S196
dm-0p1 (dir under the dm device, `holders/`, no `partition` file) measured class `virtual`, rate 20480;
dm-0 stacked 25600; basis `["nvme0n1"]`; host 102400. ✓ as R3 is written.
VERDICT: no defect found

### J (extra) — disk present only in sysfs
sda state `absent`, rate null; basis `["sda"]` → `host_write_Bps null`. sda1 ok 10240. ✓
VERDICT: no defect found

## Cross-checks

- Tool JSON == frozen oracle on all 10 fixture runs (`crosscheck.json`, field `tool_equals_oracle: true`
  for A–J) and tool == hand values for classes, basis and host in all 10.
- Real `/sys` pass (two `/proc/diskstats` reads 1.2 s apart, `--sysfs /sys`): rc 0, classes
  dm-0 stacked, nvme0n1/nvme1n1/sda/sr0 disk, all partitions partition; `class_mismatches {}` against the
  oracle's `classify`; basis `["nvme0n1","nvme1n1","sda","sr0"]` equals the oracle's.
- R3's `device`-link rationale verified in the cited source copy: `S193.src`
  `device_add_class_symlinks()` has `if (dev->parent && device_is_not_partition(dev))` before creating
  the `device` link — matches R3 and the live host (partitions have no `device` link).

## Observations for the L1 (none is a defect of the tool)

1. The counter's scenario generator never exercises the real layout: `count-c1-a1.py:171-172` creates
   `slaves/` only for non-partitions and the file has no `os.symlink` at all (`grep -n os.symlink` →
   no match), so class entries are real dirs and `device`/`partition`/slaves members are regular files.
   The 12 fixed + 300 drawn scenarios therefore never test symlinked class entries, a partition with
   slaves, `holders/`, or a dm-mapped partition. The tool passes all of those shapes here; this is a
   coverage note about P-C1-A1, not about the tool bytes.
2. Rule-scope limitation (H): R3 detects a partition only by the `partition` file, which S196 says
   dm-mapped partitions lack, so a real dm partition is classed `virtual`. Harmless for R7 (either way it
   is not in `host_basis`), but the per-device class is wrong by the kernel's own terminology. R3's
   sources do not claim completeness, so this is a limitation, not a contradicted rule.
3. Undefined-input robustness: an unreadable `slaves/` dir (`chmod 000`) makes `classify` raise
   `PermissionError`, rc 1, no JSON (probe 1). R3 defines no such case and real sysfs dirs are 0755, so
   P-C1-A1 never reaches it; noted only because the CLI docstring promises JSON on rc 0.
4. Latent tool/oracle divergence, unreachable from `/proc/diskstats`: `parse_sample` marks a name
   `bad-line` if any of its lines is malformed while the oracle's `parse` keeps the last line's status.
   Duplicate lines per device are impossible in `/proc/diskstats` and in the generator.
5. A dangling `class/block` symlink yields `unknown` with its diskstats rate still computed (probe 2) —
   matches R3/R4 as written.

## Containment / tooling

- Report written only at `.ufo/waves/round-34/wa/LabFixturePartStacked.md`; all other bytes are under
  `/fast/scratch/hyaku/mori-r34/a2-LabFixturePartStacked/` (188 KB, receipts `crosscheck.json`,
  `tool_output.json`, fixture trees, builder scripts).
- Lane touched read-only (`git cat-file`, `ls`, `grep`, file reads). No git/jj writes, no lane-index
  change, no writes to `/sys`, `/proc`, devices or the fleet repo.
- No tools installed or updated; no package manager run. No background jobs; short-lived processes only
  (all finished). No load written.

## Risks / blockers

None blocking. Residual: fixtures are hand-built, so they prove R3 conformance on these shapes, not on a
kernel that misreports a link; R3 has no rule for that case.
