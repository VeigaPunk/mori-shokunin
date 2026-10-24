measured 2026-10-23T08:58:29Z

# SrcDmStack — source for stacked diskstats double counting

Axes: the sentence must state both halves (underlying device also counted, so a sum double-counts); the URL must be a tag or commit; each quote is at most 25 contiguous words and contains no quotation mark or pipe; a partial sentence is not admitted as the whole claim.

Claim under test, from the assignment, not from S192: I/O to a stacked block device (device-mapper or md) is also accounted on its underlying devices in /proc/diskstats, so summing both double-counts. `SKILL.md:834` attributes that to S192. S192 is `block/holder.c` symlinks only (`corpus/SOURCES.md:198`; ReJudgeSkillR34 `.ufo/waves/round-34/wb/ReJudgeSkillR34.md:102-104`).

No file opened this round states that full sentence. No `DRAFT SOURCES S203` row.

## Candidates

Bytes under `/fast/scratch/hyaku/mori-r35/SrcDmStack/`. Fetched with `curl -fsSL` from the pinned tag URL. No tool installed (`/home/vgpnk/.omp/agent/RULES.md` read; pacman not used).

### iostats.rst — does not state it

URL `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/iostats.rst`, fetched 2026-10-23T08:53:42Z, 8592 bytes, 187 lines, sha256 `166bdc8fd4ee9e53bcb86804e0d22d50c89314dcfc1a248814b0069300034124`.

Nearest line, not the claim (`iostats.rst:39-40`, 17 words): if you want system-wide stats you'll have to find all the devices and sum them all up.

That tells the reader to sum every device. It does not name device-mapper, md, or a stacked device. A search of this file for `dm-`, `device-mapper`, `device mapper`, and `stacked` returned no hits. `underlying` at `:35` is counter overflow, not a lower block device.

VERDICT: reject

### drivers/md/dm.c — does not state it

URL `https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/md/dm.c`, same fetch window, 92806 bytes, 3848 lines, sha256 `b01ff2d6285efff17e52ee7a5ca1844e3fc002f59c9c53e45bc67a40bab8b02b` (same hash as the round-33 copy).

What it does state (`dm.c:1379-1380`, 16 words): Account io->origin_bio to DM dev on behalf of target that took ownership of IO with DM_MAPIO_SUBMITTED.

`dm_io_acct` then calls `bdev_start_io_acct` / `bdev_end_io_acct` on `io->orig_bio->bi_bdev` (`dm.c:508-517`). `dm_submit_bio_remap` follows the account call with `submit_bio_noacct(tgt_clone)` (`dm.c:1382-1386`). Those lines account the original bio to the device-mapper device and resubmit a clone. They do not say the clone is counted again in the underlying device's `/proc/diskstats` line, and they do not say a sum double-counts. Same limit round 33 recorded (`.ufo/waves/round-33/w1/SrcDmCore.md:35-36`).

VERDICT: reject

### block/blk-core.c — does not state it

URL `https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-core.c`, same fetch window, 36689 bytes, 1329 lines, sha256 `528501312dbd8da7649051006f12203fbef03f5180c4408ccc20856262c77827`.

Nearest line (`blk-core.c:812-813`, 24 words): This is a version of submit_bio() that shall only be used for I/O that is resubmitted to lower level drivers by stacking block drivers.

That is the resubmit rule for `submit_bio_noacct`. `submit_bio` itself only does task and VM event accounting, then calls `submit_bio_noacct` (`blk-core.c:954-962`). `bdev_end_io_acct` adds sectors to the `bdev` argument (`blk-core.c:1100-1110`); this file does not call it on a device-mapper bio and on that bio's underlying device. No sentence says summing both double-counts.

VERDICT: reject

### sysstat iostat docs — does not state it

Man source, which is the iostat manual at this tag: `https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/man/iostat.in`, fetched 2026-10-23T08:54:25Z, 18321 bytes, 485 lines, sha256 `b16edbf63faef52e5f8a1d36cf5d6b1ef8c579e988f80599bbe6ce6875f27c32`. `man/iostat.1` at this tag returned 404. The jsDelivr file index (2933 paths) lists `man/iostat.in` as the iostat manual.

Nearest line (`iostat.in:323-324`, 16 words): Display the registered device mapper names for any device mapper devices. Useful for viewing LVM2 statistics.

That is the `-N` display name. The manual also says statistics are shown for every device the kernel keeps stats for (`iostat.in:96-101`) and that `/proc/diskstats` contains disk statistics (`iostat.in:468`). It never says a device-mapper or md line repeats an underlying device, and never says not to add them.

Also opened at v12.8.0 and searched for the same claim (no stating sentence): `iostat.c` sha256 `f099229c0051be9538f220d63fe7953247ee947f112d367ff647d791953b9dce` (71360 bytes; `dm-` hits are name lookup for `-N`, `iostat.c:129-161`); `FAQ.md` sha256 `c4e21eb9d34452eb9b9d661f3d5588e7168cf63361ae3a401baab9f48de9e3a9` (36476 bytes; diskstats mentions are field 9 and where iostat reads); `README.md` sha256 `abf6b89d1109a2f592c85dbd3315213080ea99919891d25436ea7daac28bf180`; `man/sar.in` sha256 `62495e7259269e92641e560cc3439bb495be1cefa0395a3aa66b90db822937d7` (no `double`, `device mapper`, or `underlying`).

VERDICT: reject

### util-linux lsblk docs — does not state it

URL `https://raw.githubusercontent.com/util-linux/util-linux/v2.42.4/misc-utils/lsblk.8.adoc`, fetched 2026-10-23T08:56:18Z, 11860 bytes, 263 lines, sha256 `82f583f69e05bd4bca35281a7d8a964812767f98f25958c2947d42f094eca4a7`. `sys-utils/lsblk.8.adoc` and `lsblk-cmd/lsblk.8.adoc` returned 404. The path was taken from the kernel.org release tarball `https://cdn.kernel.org/pub/linux/utils/util-linux/v2.42/util-linux-2.42.4.tar.xz` (10729748 bytes, sha256 `fbd62a100ab7bb8746ba0661255c3c48185b1e9021507c624da01fbc696330ec`); the member `misc-utils/lsblk.8.adoc` hashes equal to the tag URL (`cmp` match).

Nearest line (`lsblk.8.adoc:53`, 7 words): Do not print holder devices or slaves.

That is `--nodeps` tree printing. `lsblk.c` at the same tag (sha256 `ca3e8d5c18020ab624373ed1f2eb4176e8a3610595ffdca4164ca68f36f9440a`, 78558 bytes) uses `stat` for uid, gid, and mode (`lsblk.c:741-886`), not `/proc/diskstats`. No sentence about accounting a stacked device on its slaves.

VERDICT: reject

## Sweep besides the five candidates

Opened, pinned, and none states the full sentence:

- `drivers/md/dm-linear.c` v7.2, sha256 `4b37a1dbf0c1881495660a14ca2456320e99b44b6c762feac7b70589808d6e83`, 5472 bytes. `linear_map` does `bio_set_dev(bio, lc->dev->bdev)` and returns `DM_MAPIO_REMAPPED` (`k-dm-linear.c:93-96`). That aims the bio at the underlying bdev. It does not mention diskstats.
- `Documentation/admin-guide/md.rst` v7.2, sha256 `9ecd6c92bb42a3a8dc1b213ac4f099a5e1ea498362afbcaed6310099f6d64b96`, 29609 bytes. No diskstats or double-count sentence (grep `double|diskstat|iostat|account`).
- `Documentation/admin-guide/device-mapper/statistics.rst` v7.2, sha256 `f6539e348a71099eb158edb9620a7e60bcaf1106de1345608b0239ae1954bb70`, 7753 bytes. This is the separate region-stats facility, same field layout as diskstats (`k-statistics.rst:14-16`). It does not say ordinary dm lines repeat underlying diskstats lines.
- `Documentation/ABI/testing/sysfs-block` at v7.2 returned 404.
- Round 33 already opened `drivers/md/md.c` v7.2 and reported it does not state member-device re-accounting (`.ufo/waves/round-33/w1/SrcLoopOrMd.md:64-65`). Not re-fetched this round; not treated as a new admit.

Queries that did not yield a kernel or sysstat sentence of the claim: device-mapper diskstats double count; iostat device mapper underlying do not sum; avoid double counting diskstats device mapper; submit_bio_noacct stacking accounting. Web hits that state the warning in prose were a secondary iostat tutorial and collectl (below), not the kernel tree, sysstat, or util-linux.

## Closest statement — not admitted for the full claim

collectl tag 4.3.20.3 (`166c9ba5f916727974444b1f4c680ce5ddf498ca`), file `docs/Disks.html`. URL `https://raw.githubusercontent.com/sharkcz/collectl/4.3.20.3/docs/Disks.html`, fetched 2026-10-23T08:57:44Z, 8940 bytes, 168 lines, sha256 `c84b28a24ad42b2b523a9b316d7cfb0368e47e2306ee762473c4c00d97681b8e`. The same bytes are at HEAD `c0d08ef39d3560da6327efbd23aea84f3e05a474`. The live `https://collectl.sourceforge.net/Disks.html` (5721 bytes, sha256 `15ced62046cbd44d24821868fca64d81e28c32c4dc1bcf7bf65ef8f2d07710c3`) still has the device-mapper bullet but is not the pinned text; quotes below are from the tag file.

`Disks.html:13-14` (19 words): disk summary data represents the total activity across all disks or to be more precise, those enumerated in /proc/diskstats

`Disks.html:24-25` (20 words; the file wraps NOT in an i element): Device mapper disks, while listed in the detail data are NOT included in the summary data to avoid double counting

That states a device-mapper exclusion from a `/proc/diskstats` summary, and gives double counting as the reason. It does not say the same I/O is accounted on the underlying device, and it does not mention md. The partition bullet on `:21` is the other mechanism (already S183), not stacked devices. The collectl program at this tag (`collectl`, 253219 bytes, sha256 `5fb55c7a4ec63dd9214dc53bfb5e8fc53d35c2bc845afe6cda0589e44cdbb29f`) and `man1/collectl.1` (sha256 `bd4c54073af455316fd9c4e0f74a46e6292cd83d3398b1de0c33c646b8a60d4c`) do not contain that sentence. `docs/WhySummary.html` (sha256 `7dd7cc6be4ecb267df15d4aa4e0d6c2afa737ace1b27cd3a379872a670b0892c`) has no double-count or diskstats hit.

[INFERENCE] Joining `dm-linear.c:93-96` (bio retargeted at the underlying bdev), `dm.c:1379-1386` (account the dm bio, then `submit_bio_noacct` of the clone), and `blk-core.c:812-813` (that call is how stacking drivers resubmit) still does not show the lower device's diskstats update inside these files. Not recorded as a source.

```
DRAFT SOURCES S203
none
```

VERDICT: fails
