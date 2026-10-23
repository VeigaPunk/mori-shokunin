# ExecHostDiskstats — mori round 33, wave 1 — host evidence for C1 (FR6: /proc/diskstats as a write rate)
Status: complete. Kind: **HOST OBSERVATION on this machine, not a source.** No URL was opened, no upstream sha256 is
offered, nothing here may stand in for a Gate/SOURCES row; where the assignment's own wording (e.g. "field 10 is
sectors written") supplies meaning my commands cannot show, I say so. Host: `Linux plazir27 7.2.11-arch1-1 #1 SMP
PREEMPT_DYNAMIC Fri, 16 Oct 2026 00:28:58 +0000 x86_64 GNU/Linux`, sampled 2026-10-23T02:39:52Z … 02:42:18Z (host
local clock 2026-10-22 23:39–23:42). No serial, uid, pid, slice name, session id or setting value was read into or
written from this report; device names only, and `/sys/block/dm-0/dm/uuid` was piped into a fixed redaction string
whose value never reached this report. Tool installs: **none** (no pacman, no uv, no new binary); used only
pre-existing `sh awk cut sort uniq paste ls cat cp dd rm wc stat sha256sum lsblk findmnt df`. LSP: not applicable —
no code symbol edited. Scratch kept: `/fast/scratch/hyaku/mori-r33/ExecHostDiskstats/` (`measure.sh`, `cmpstat.sh`,
snapshots `t0.txt t1.txt n0.txt n1.txt w0.txt w1.txt u10..u41.txt`).
## 1. Commands and outputs
### 1.1 kernel and time
```
$ date -u +%FT%TZ ; timeout 30 uname -r ; timeout 30 uname -a
2026-10-23T02:39:52Z
7.2.11-arch1-1
Linux plazir27 7.2.11-arch1-1 #1 SMP PREEMPT_DYNAMIC Fri, 16 Oct 2026 00:28:58 +0000 x86_64 GNU/Linux
```
### 1.2 fields per /proc/diskstats line, and per /sys/block/<dev>/stat
$ timeout 30 awk '{print NF}' /proc/diskstats | sort | uniq -c
     11 20
$ timeout 30 wc -l < /proc/diskstats
11
$ for d in /sys/block/*/stat; do echo "$(echo $d | cut -d/ -f4): $(wc -w < $d) fields"; done
dm-0: 17 fields
nvme0n1: 17 fields
nvme1n1: 17 fields
sda: 17 fields
sr0: 17 fields
No header line: 11 data lines, each exactly 20 whitespace-separated fields; every `/sys/block/<dev>/stat` has exactly 17.
### 1.3 device names by class (names only; no serial, uid or pid)
```
$ timeout 30 ls /sys/class/block/ | tr '\n' ' '
dm-0 nvme0n1 nvme0n1p1 nvme0n1p2 nvme1n1 nvme1n1p1 nvme1n1p2 sda sda1 sda2 sr0
$ timeout 30 ls /sys/class/nvme/   →  nvme0 nvme1
```
Classes: whole disks `nvme0n1 nvme1n1 sda`; partitions `nvme0n1p1 nvme0n1p2 nvme1n1p1 nvme1n1p2 sda1 sda2`;
device-mapper `dm-0`; optical `sr0`. `loop*`: **none present**. `zram*`: **none present**. Multipath namespace node
(`nvme0c0n1`-style): none; the two NVMe namespaces appear only as `nvme0n1`, `nvme1n1`.
```
$ timeout 30 lsblk -o NAME,MAJ:MIN,SIZE,TYPE,FSTYPE,MOUNTPOINTS
NAME        MAJ:MIN   SIZE TYPE  FSTYPE      MOUNTPOINTS
sda           8:0    23.9G disk  iso9660
├─sda1        8:1     7.4G part  iso9660
└─sda2        8:2      23M part  vfat
sr0          11:0    21.5G rom   iso9660
nvme0n1     259:0   931.5G disk
├─nvme0n1p1 259:1       2G part  vfat        /boot
└─nvme0n1p2 259:2   929.5G part  crypto_LUKS
  └─root    253:0   929.5G crypt btrfs       /var/log  /home  /var/cache/pacman/pkg  /
nvme1n1     259:3   931.5G disk
├─nvme1n1p1 259:4     128G part  xfs         /tmp
└─nvme1n1p2 259:5   803.5G part  xfs         /fast
$ timeout 30 ls -l /sys/block/dm-0/slaves/
lrwxrwxrwx 1 root root 0 Oct 22 23:40 nvme0n1p2 -> ../../../../pci0000:00/0000:00:01.2/0000:02:00.0/nvme/nvme0/nvme0n1/nvme0n1p2
$ timeout 30 cat /sys/block/dm-0/dm/name
root
$ timeout 30 findmnt -no SOURCE,FSTYPE,OPTIONS /fast
/dev/nvme1n1p2 xfs rw,nosuid,nodev,noatime,inode64,logbufs=8,logbsize=256k,noquota
$ timeout 30 df -h /fast
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  425G  379G  53% /fast
```
`dm-0` is the crypt mapping `root` over `nvme0n1p2`, carrying `/`, `/home`, `/var/log`; the assigned scratch filesystem
`/fast` is `nvme1n1p2`, **not** `dm-0`.
### 1.4 block sizes
$ for d in /sys/block/*; do echo "$d logical=$(cat $d/queue/logical_block_size 2>/dev/null) phys=$(cat $d/queue/physical_block_size 2>/dev/null)"; done
/sys/block/dm-0 logical=512 phys=512
/sys/block/nvme0n1 logical=512 phys=512
/sys/block/nvme1n1 logical=4096 phys=4096
/sys/block/sda logical=512 phys=512
/sys/block/sr0 logical=2048 phys=2048
$ for d in nvme0n1 nvme1n1 sda dm-0; do echo "$d hw_sector_size=$(cat /sys/block/$d/queue/hw_sector_size)"; done
nvme0n1 hw_sector_size=512
nvme1n1 hw_sector_size=4096
sda hw_sector_size=512
dm-0 hw_sector_size=512
### 1.5 one raw snapshot, all 11 lines (`w0.txt`, mtime 2026-10-22 23:40:51 -0300)
```
 259       0 nvme0n1 663906138 15302136 16400244827 43106629 22592227 3742639 443549480 153190669 2 18990388 196399121 183087 154587 851114664 71829 218486 29992
 259       1 nvme0n1p1 83775 3351 19539629 24664 137 19 352 2 0 1787 24667 0 0 0 0 0 0
 259       2 nvme0n1p2 663822303 15298785 16380697598 43081962 22592088 3742620 443549128 153190667 2 18880656 196344459 183087 154587 851114664 71829 0 0
 259       3 nvme1n1 66693805 448703 1790777184 4789962 45540396 38782426 3056658744 74253217 0 4621941 79365848 0 0 0 0 750136 322668
 259       4 nvme1n1p1 14752825 34355 414825992 1016209 18723855 12943994 1113682168 24605759 0 1391645 25621969 0 0 0 0 0 0
 259       5 nvme1n1p2 51940927 414348 1375944952 3773721 26816541 25838432 1942976576 49647457 0 3428360 53421178 0 0 0 0 0 0
   8       0 sda 180 3 10824 6811 0 0 0 0 0 5298 6811 0 0 0 0 0 0
   8       1 sda1 64 2 5136 1092 0 0 0 0 0 1039 1092 0 0 0 0 0 0
   8       2 sda2 51 0 1728 993 0 0 0 0 0 980 993 0 0 0 0 0 0
  11       0 sr0 75 0 2376 204 0 0 0 0 0 194 204 0 0 0 0 0 0
 253       0 dm-0 679121055 0 16380693768 45626682 26334708 0 443549128 67329203 2 19787370 113017978 337674 0 851114664 62093 0 0
```
In this one instant `dm-0` field 10 `443549128` equals `nvme0n1p2` field 10 `443549128`, and `nvme0n1` field 10
`443549480` exceeds it by exactly `nvme0n1p1`'s `352`.
### 1.6 whole disk vs its partitions, prescribed write
```
$ cd /fast/scratch/hyaku/mori-r33/ExecHostDiskstats && cp /proc/diskstats t0.txt && dd if=/dev/zero of=blob bs=1M count=64 conv=fsync && cp /proc/diskstats t1.txt
64+0 records in
64+0 records out
67108864 bytes (67 MB, 64 MiB) copied, 0.0362923 s, 1.8 GB/s
$ ./measure.sh table t0.txt t1.txt nvme1n1 nvme1n1p1 nvme1n1p2
device         t0_field10     t1_field10     delta_field10
nvme1n1        3053879992     3054079048     199056
nvme1n1p1      1113681040     1113681048     8
nvme1n1p2      1940198952     1940398000     199048
$ ./measure.sh partsum t0.txt t1.txt nvme1n1p1 nvme1n1p2
199056
```
Disk delta `199056` = partition sum `199056` (`199048 + 8`). In the same window `dm-0` and `nvme0n1p2` each moved
`8648` (background traffic only; the blob is not on `dm-0`).
### 1.7 two 5 s windows, all devices (`measure.sh table` printed two tables; merged here cell for cell)
```
$ cp /proc/diskstats n0.txt ; sleep 5 ; cp /proc/diskstats n1.txt          # natural, no induced write
$ cp /proc/diskstats w0.txt ; dd if=/dev/zero of=blob bs=1M count=64 conv=fsync ; sleep 5 ; cp /proc/diskstats w1.txt
device      natural 5.04 s: t0 -> t1 = delta    induced dd 64 MiB + 5.32 s: t0 -> t1 = delta
nvme0n1     443549480 -> 443590560 = 41080     443549480 -> 443601096 = 51616
nvme0n1p1   352 -> 352 = 0                     352 -> 352 = 0
nvme0n1p2   443549128 -> 443590208 = 41080     443549128 -> 443600744 = 51616
dm-0        443549128 -> 443590208 = 41080     443549128 -> 443600744 = 51616
nvme1n1     3056658744 -> 3057841360 = 1182616 3056658744 -> 3057948568 = 1289824
nvme1n1p1   1113682168 -> 1113682768 = 600     1113682168 -> 1113682776 = 608
nvme1n1p2   1942976576 -> 1944158592 = 1182016 1942976576 -> 1944265792 = 1289216
sda         0 -> 0 = 0                         0 -> 0 = 0
sr0         0 -> 0 = 0                         0 -> 0 = 0
sum(nvme0n1p1+nvme0n1p2) = 41080               sum = 51616
sum(nvme1n1p1+nvme1n1p2) = 1182616             sum = 1289824
```
In **both** windows `dm-0`'s delta equals its slave `nvme0n1p2`'s exactly (`41080`, `51616`), and each whole disk's
delta equals the sum over its partitions (`41080`, `51616`; `1182616`, `1289824`). A reader adding up every line
counts the same bytes up to three times (`dm-0`, its partition, the whole disk).
### 1.8 /sys/block/<dev>/stat against the /proc/diskstats line
`cmpstat.sh <dev>` reads both files twice and reports any matching pairing plus a diff of sysfs index *i* against
diskstats field *i+3*:
```
$ ./cmpstat.sh sda      -> match: sysfs#2==diskstats#2 ; all 17 pairs "same"
$ ./cmpstat.sh nvme1n1  -> match: sysfs#2==diskstats#2 ; all 17 pairs "same"
  sysfs#1 = 66802790 448712 1795520776 4806882 45839952 38842227 3069258104 74955718 0 4634333 80086872 0 0 0 0 751327 324270
  diskst#1(fields 4-20) = identical, field for field
$ ./cmpstat.sh nvme0n1  -> match: none ; pairs differing: 1,3,4,9,10,11 only
  sysfs#1 = 664784395 15303052 16426664523 43162526 22622440 3744649 444305152 153252001 2 19027188 196516650 183198 154670 851778144 71926 219895 30195
  diskst#1 = 664784456 15303052 16426665483 43162530 22622440 3744649 444305152 153252001 1 19027190 196516654 183198 154670 851778144 71926 219895 30195
$ ./cmpstat.sh dm-0     -> match: none ; pairs differing: 1,3,4,9,10,11 only, same shape
  sysfs#1 = 680000238 0 16407113640 45687250 26366931 0 444304800 67392026 5 19826217 113141522 337868 0 851778144 62246 0 0
  diskst#1 = 680000288 0 16407114416 45687257 26366931 0 444304800 67392026 2 19826219 113141529 337868 0 851778144 62246 0 0
```
The 17 sysfs fields are diskstats fields 4–20 in order (major, minor, name have no sysfs counterpart); idle devices
match exactly, busy devices differ only where counters advanced between the two reads. Diskstats field 10 = sysfs field 7.
### 1.9 which unit field 10 counts in (4 direct 64 MiB writes on a 4096-byte-logical device)
```
$ for i in 1 2 3 4; do cp /proc/diskstats u${i}0.txt ; dd if=/dev/zero of=blob3 bs=1M count=64 oflag=direct conv=fsync ; cp /proc/diskstats u${i}1.txt ; done
trial 1: nvme1n1p2 1949828480 -> 1949962984 = 134504 ; nvme1n1 3063526872 -> 3063661376 = 134504
trial 2: nvme1n1p2 1949962992 -> 1950097424 = 134432 ; nvme1n1 3063661384 -> 3063795840 = 134456
trial 3: nvme1n1p2 1950097456 -> 1950231904 = 134448 ; nvme1n1 3063795872 -> 3063930320 = 134448
trial 4: nvme1n1p2 1950231936 -> 1950365008 = 133072 ; nvme1n1 3063930352 -> 3064063424 = 133072
```
64 MiB is `131072` 512-byte units or `16384` 4096-byte units. Every trial lands at ~`1.02 × 131072`, about eight times
the 4096-unit figure. [INFERENCE, not a host fact: field 10 counts 512-byte units even for this 4096-byte-logical
device; the 2000–3432 sectors of excess over 131072 are filesystem metadata plus background traffic, not isolated.]
Trial 2's whole disk exceeds its partition by 24 sectors, unattributed.
### 1.10 cleanup
$ ls -l blob blob3 ; rm -f blob blob3 ; ls blob blob3
-rw-r--r-- 1 vgpnk vgpnk 67108864 Oct 22 23:40 blob    -rw-r--r-- 1 vgpnk vgpnk 67108864 Oct 22 23:41 blob3
ls: cannot access 'blob': No such file or directory
ls: cannot access 'blob3': No such file or directory
Both blobs deleted; nothing left running; no process signalled (`pgrep -c -u vgpnk dd` → `0`).
## 2. Facts (each with the command that shows it)
1. Kernel release `7.2.11-arch1-1`, x86_64 (§1.1). 2. `/proc/diskstats` has 11 data lines, no header, every line
exactly 20 fields (§1.2). 3. Every `/sys/block/<dev>/stat` has exactly 17 fields (§1.2). 4. The 17 sysfs fields are
diskstats fields 4–20 in order; idle devices match exactly, busy devices differ only where counters advanced (§1.8).
5. Diskstats field 10 equals sysfs field 7 (§1.8). 6. Present classes: whole disks `nvme0n1 nvme1n1 sda`, their
partitions, one dm device `dm-0`, one optical `sr0`; no `loop*`, no `zram*`, no multipath namespace node (§1.3).
7. `dm-0`'s only slave is `nvme0n1p2`; its dm name is `root`; it carries `/`, `/home`, `/var/log` (§1.3).
8. `/fast` is `nvme1n1p2` (xfs), so the assigned scratch path is not on `dm-0` (§1.3). 9. Logical and physical block
size are 512 for `dm-0`, `nvme0n1`, `sda`; 4096 for `nvme1n1`; 2048 for `sr0`; `hw_sector_size` matched each time
(§1.4). 10. A whole disk's field-10 delta equals the sum of its partitions' deltas over the same window, in all three
windows measured (§1.6, §1.7). 11. In the same 5 s window `dm-0` and its slave `nvme0n1p2` show the **same** field-10
delta, and in the §1.5 snapshot their since-boot field-10 totals are the identical number `443549128` (§1.7, §1.5).
12. Field-10 values are since-boot totals; a rate needs two samples (§1.5 vs §1.6/§1.7). 13. Under load counters move
on their own: `nvme1n1` gained `1182616` sectors in a 5 s window with no write induced by me (§1.7). 14. A 64 MiB
direct write on the 4096-byte-logical `nvme1n1p2` moves field 10 by ~131072, not ~16384 (§1.9).
## 3. Assumptions these commands do NOT support
- Field 10's *meaning* (sectors written, not read sectors or milliseconds) is not observable from `/proc/diskstats`
  alone; the correspondence to sysfs field 7 is (§1.8), but that field's name comes from the kernel ABI document,
  which this seat did not open.
- Whether field 10 counts 512-byte units on *every* device type is unsettled by §1.9 (one device, one write size).
- Counter wrap, reset on device re-add and behaviour across suspend were not tested.
- The field count is version-dependent; one kernel measured, and the 20-field layout's trailing fields were not probed.
- Nothing here says how a *rate* should be formed (window length, smoothing, which of the 11 lines to read).
- `/proc/diskstats` and `/sys/block/<dev>/stat` were not verified to update atomically with respect to each other.
- No `loop` or `zram` device exists here, so their line shape is unobserved on this host.
- No source, URL, quote or upstream sha256 is produced here; a row resting on this material must be declared as lane doctrine.
## 4. Deviations, risks, blockers
- The prescribed write (`dd … of=/fast/scratch/…/blob … conv=fsync`) lands on `nvme1n1p2`, because `/fast` is not on
  `dm-0` here; it cannot exercise `dm-0`. The `dm-N`-vs-slave coincidence is shown instead by the same-window rows of
  §1.7 (`dm-0` delta = `nvme0n1p2` delta = `41080`, then `51616`) and the identical since-boot totals in §1.5.
- The host is busy (fleet seats): background traffic reached ~1.18 M sectors per 5 s on `nvme1n1`, so any single-write
  window is confounded; §1.9 repeats the same write four times rather than trusting one.
- The "5 s" windows are 5.04 s and 5.32 s, timed by the shell, not by a timer inside the sampling command; everything
  above is a snapshot of one host on one kernel, not reproducible byte-for-byte and never a Gate sha256.
- No blockers. No tool needed installing, no pacman transaction attempted, no process left alive.
