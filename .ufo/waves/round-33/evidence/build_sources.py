#!/usr/bin/env python3
"""L1 integration helper (round 33): copy source bytes into the lane, locate quotes, emit SOURCES and Gate rows."""
import hashlib, json, os, re, shutil, sys

SCR = '/fast/scratch/hyaku/mori-r33'
LANE = '/home/vgpnk/Projects/shokunin/mori-shokunin'
OUT = f'{LANE}/corpus/evidence/sources-r33'
ENTRY = 'corpus/knowledge/disk-write-rate-r33.md'

S = [
 dict(id='S180', copy='MoriR33.SrcStatRst/stat.rst.src', seat='SrcStatRst', acc='2026-10-23T02:39:46Z', kind='docs',
      url='https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/block/stat.rst',
      title='Linux block-device stat file documentation v7.2',
      scope='the v7.2 /sys/block/<dev>/stat format: the 17-value line, the 512-byte sector unit, completion-time counting and the tick fields',
      anchor='Documentation/block/stat.rst:2-5,21-22,71-73,75-80; tag v7.2',
      teaches='The stat file is one line of 17 decimal values; its sector counts use the standard 512-byte sector, not a device or filesystem block size, and grow when an I/O completes; the millisecond wait values can rise faster than 1000 per second when several requests wait.',
      quotes=['The stat file consists of a single line of text containing 17 decimal values separated by whitespace.',
              'are the standard UNIX 512-byte sectors, not any device- or filesystem-specific block size.',
              'The counters are incremented when the I/O completes.',
              'If there are multiple I/O requests waiting, these values will increase at a rate greater than 1000/second']),
 dict(id='S181', copy='SrcIostatsRst/iostats.rst.first.src', seat='SrcIostatsRst', acc='2026-10-23T02:40:16Z', kind='docs',
      url='https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/iostats.rst',
      title='Linux I/O statistics fields documentation v7.2 (tag-pinned counterpart of the docs.kernel.org page in S033)',
      scope='the v7.2 iostats field semantics: which fields are cumulative, when they reset, how field 10 grows, and the sysfs/procfs equivalence',
      anchor='Documentation/admin-guide/iostats.rst:22,33-36,75-76; tag v7.2',
      teaches='All fields except field 9 are cumulative monotonic counters; they reset at boot, on device reattachment or reinitialisation, or on counter overflow; field 10 grows while field 9 is nonzero; /proc/diskstats and /sys/block/<dev>/stat carry the same 17 statistics.',
      quotes=['All fields are cumulative, monotonic counters, except for field 9, which resets to zero as I/Os complete.',
              'The remaining fields reset at boot, on device reattachment or reinitialization, or when the underlying counter overflows.',
              'This field increases so long as field 9 is nonzero.',
              'Both files contain the same 17 statistics.']),
 dict(id='S182', copy='SrcGenhd/genhd-1.src', seat='SrcGenhd', acc='2026-10-23T02:39:43Z', kind='code',
      url='https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c',
      title='Linux block/genhd.c at v7.2 (diskstats_show)',
      scope='how v7.2 prints /proc/diskstats: zero-size partitions skipped, in-flight computed at read time, io_ticks converted from jiffies, discard sectors printed from their own counter',
      anchor='block/genhd.c:1353,1371-1374,1395,1403,1418-1425 (diskstats_show, diskstats_op, proc_create_seq); tag v7.2',
      teaches='diskstats_show skips a partition with zero sectors, computes the in-flight count when the file is read, prints io_ticks through jiffies_to_msecs and prints discard sectors from the separate STAT_DISCARD counter.',
      quotes=['if (bdev_is_partition(hd) && !bdev_nr_sectors(hd)) continue; inflight = bdev_count_inflight(hd);',
              'proc_create_seq("diskstats", 0, NULL, &diskstats_op);',
              'seq_put_decimal_ull(seqf, " ", jiffies_to_msecs(stat.io_ticks));',
              'seq_put_decimal_ull(seqf, " ", stat.sectors[STAT_DISCARD]);']),
 dict(id='S183', copy='SrcPartStat/part_stat-1.src', seat='SrcPartStat', acc='2026-10-23T02:39:48Z', kind='code',
      url='https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/part_stat.h',
      title='Linux include/linux/part_stat.h at v7.2',
      scope='the v7.2 per-device statistics macros: part_stat_add on a partition also adds to the whole disk; sector counters are unsigned long',
      anchor='include/linux/part_stat.h:10,60-63; tag v7.2',
      teaches='part_stat_add applies an add made to a partition a second time to bdev_whole(part); the sectors array is unsigned long.',
      quotes=['#define part_stat_add(part, field, addnd) do { \\ __part_stat_add((part), field, addnd); \\ if (bdev_is_partition(part)) \\ __part_stat_add(bdev_whole(part), field, addnd);',
              'unsigned long sectors[NR_STAT_GROUPS];']),
 dict(id='S184', copy='SrcBlkCore/blk-core.src', seat='SrcBlkCore', acc='2026-10-23T02:39:49Z', kind='code',
      url='https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-core.c',
      title='Linux block/blk-core.c at v7.2 (bio accounting and update_io_ticks)',
      scope='v7.2 bio-based accounting: sectors added in bdev_end_io_acct through part_stat_add; io_ticks advanced by elapsed time when I/O is in flight or ending',
      anchor='block/blk-core.c:1067-1068,1100,1108-1110; tag v7.2',
      teaches='bdev_end_io_acct adds the completed sectors with part_stat_add; update_io_ticks adds the elapsed time to io_ticks only when an I/O ends or one is in flight.',
      quotes=['void bdev_end_io_acct(struct block_device *bdev, enum req_op op,',
              'update_io_ticks(bdev, now, true); part_stat_inc(bdev, ios[sgrp]); part_stat_add(bdev, sectors[sgrp], sectors);',
              '(end || bdev_count_inflight(part))) __part_stat_add(part, io_ticks, now - stamp);']),
 dict(id='S185', copy='MoriR33.SrcBlkMq/blk-mq-1.src', seat='SrcBlkMq', acc='2026-10-23T02:39:58Z', kind='code',
      url='https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-mq.c',
      title='Linux block/blk-mq.c at v7.2 (request completion accounting)',
      scope='v7.2 request-based accounting: sectors added from completed bytes in blk_account_io_completion',
      anchor='block/blk-mq.c:856,858,862; tag v7.2',
      teaches='For a request flagged RQF_IO_STAT, blk_account_io_completion adds completed bytes shifted right by 9 to the sector counter.',
      quotes=['static void blk_account_io_completion(struct request *req, unsigned int bytes)',
              'if (req->rq_flags & RQF_IO_STAT) {', 'part_stat_add(req->part, sectors[sgrp], bytes >> 9);']),
 dict(id='S186', copy='SrcSectorSize/blk_types.src', seat='SrcSectorSize', acc='2026-10-23T02:39:40Z', kind='code',
      url='https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/blk_types.h',
      title='Linux include/linux/blk_types.h at v7.2 (sector unit)',
      scope='the v7.2 kernel sector unit (512 bytes, SECTOR_SHIFT 9) and the bdev_whole macro',
      anchor='include/linux/blk_types.h:25-28,31,84-85; tag v7.2',
      teaches='The sector is the basic unit of block I/O; one sector is 512 = 2**9 (bytes, per the same comment) and SECTOR_SHIFT is 9; bdev_whole(bdev) is bd_disk->part0.',
      quotes=['The basic unit of block I/O is a sector.', 'The size of one sector is 512 = 2**9', '#define SECTOR_SHIFT 9', '#define bdev_whole(_bdev) \\ ((_bdev)->bd_disk->part0)']),
 dict(id='S187', copy='L1/src/procfs-diskstats.src', seat='L1 MoriR33', acc='2026-10-23T02:46:06Z', kind='docs',
      url='https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/ABI/testing/procfs-diskstats',
      title='Linux /proc/diskstats ABI description v7.2',
      scope='the v7.2 /proc/diskstats field numbering and the field counts by kernel version',
      anchor='Documentation/ABI/testing/procfs-diskstats:6-7,19-21,26-27,36; tag v7.2',
      teaches='A line has 14 fields (field 10 sectors written, 11 time spent writing in ms, 12 I/Os currently in progress); 4.18+ appends four discard fields for 18; 5.5+ appends two flush fields.',
      quotes=['Each line contains the following 14 fields:', '10 sectors written 11 time spent writing (ms) 12 I/Os currently in progress',
              'Kernel 4.18+ appends four more fields for discard tracking putting the total at 18:',
              'Kernel 5.5+ appends two more fields for flush requests:']),
 dict(id='S188', copy='SrcFlushCommit/flush-commit-1.src', seat='SrcFlushCommit', acc='2026-10-23T02:40:15Z', kind='code',
      url='https://github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch',
      title='Linux commit b6866318 "block: add iostat counters for flush requests" (patch view)',
      scope='what the flush counters count: flush requests executed by the disk, which the block layer combines; not tracked for partitions; triggered by requests that are usually zero-size writes',
      anchor='patch lines 9,11 (commit message) and 71-72 (iostats.rst hunk)',
      teaches='The flush counters (fields 16-17 in iostats numbering) count flush requests executed by the disk; the block layer combines flush requests and executes at most one at a time; they are not tracked for partitions; requests that trigger flushes are usually barriers, zero-size writes.',
      quotes=['Block layer has sophisticated engine for combining several flush requests',
              'Requests which trigger flushes usually are barriers - zero-size writes.',
              'This counts flush requests executed by disk. Not tracked for partitions.',
              'Block layer combines flush requests and executes at most one at a time.']),
 dict(id='S189', copy='MoriR33.SrcDiscardCommit/discard-first.src', seat='SrcDiscardCommit', acc='2026-10-23T02:40:27Z', kind='code',
      url='https://github.com/torvalds/linux/commit/bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c.patch',
      title='Linux commit bdca3c87 "block: Track DISCARD statistics and output them in stat and diskstat" (patch view)',
      scope='discard accounting: its own four statistics, appended to the stat files and /proc/diskstats',
      anchor='patch lines 7-17 (commit message)',
      teaches='Discard I/O is tracked with its own four statistics of the kinds kept for reads and writes, including discard sectors completed.',
      quotes=['These are tracked with the same four stats as reads and writes:', 'Number of discard ios completed. Number of discard ios merged Number of discard sectors completed Milliseconds spent on discard requests']),
 dict(id='S190', copy='SrcSysstatIostat/iostat-v12.8.0-1.src', seat='SrcSysstatIostat', acc='2026-10-23T02:40:11Z', kind='code',
      url='https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c',
      title='sysstat iostat.c at v12.8.0',
      scope='the extended-statistics display of iostat 12.8.0 (write_ext_stat) only: the current and previous samples and the write-sector value when the current count is lower; not the default report',
      anchor='iostat.c:1444-1464,1516-1517 (write_ext_stat); tag v12.8.0',
      teaches='In the extended-statistics display iostat takes ioi as the current and ioj as the previous sample and sets the write-sector value to 0.0 when the current sectors-written count is below the previous one; the default report computes its rate elsewhere and is not covered by this row.',
      quotes=['void write_ext_stat(unsigned long long itv, int fctr, int hpart,', '@ioi Current sample statistics.', '@ioj Previous sample statistics.',
              'xios.wsectors = ioi->wr_sectors < ioj->wr_sectors ? 0.0 : S_VALUE(ioj->wr_sectors, ioi->wr_sectors, itv);']),
]


def norm(t):
    return ' '.join(t.split())


def esc(q):
    return q.replace('\\', '\\\\').replace('"', '\\"').replace('|', '\\|')


def locate(lines, q):
    nq = norm(q)
    for j in range(len(lines)):
        for i in range(j, max(-1, j - 9), -1):
            if nq in norm(' '.join(lines[i:j + 1])):
                return i + 1, j + 1
    return None


def main():
    os.makedirs(OUT, exist_ok=True)
    src_rows, gate_rows, report = [], [], []
    for s in S:
        p = f'{SCR}/{s["copy"]}'
        b = open(p, 'rb').read()
        sha = hashlib.sha256(b).hexdigest()
        text = b.decode(errors='replace')
        lines = text.splitlines()
        qs = []
        for q in s['quotes']:
            loc = locate(lines, q)
            assert loc, (s['id'], q)
            assert norm(q) in norm(text)
            n = len(q.split())
            assert 3 <= n <= 25, (s['id'], q, n)
            L = f'{loc[0]}' if loc[0] == loc[1] else f'{loc[0]}-{loc[1]}'
            qs.append(f'`{s["id"]}.src:{L}` ({n} words): "{esc(q)}"')
        shutil.copyfile(p, f'{OUT}/{s["id"]}.src')
        gate_rows.append(f'| {s["id"]} | {s["url"]} | {s["acc"]} | `{sha}` | {"; ".join(qs)} | admit, A, mined |')
        src_rows.append(f'| {s["id"]} | {s["title"]} — {s["url"]} | {s["kind"]} | A | {s["scope"]} | {s["anchor"]} | '
                        f'{s["teaches"]} | mined | 2026-10-23 | on-release | {ENTRY} |')
        report.append(f'{s["id"]} {sha} {len(b)}B opened-by={s["seat"]} copy={s["copy"]}')
    open(f'{SCR}/L1/gate-rows.md', 'w').write('\n'.join(gate_rows) + '\n')
    open(f'{SCR}/L1/source-rows.md', 'w').write('\n'.join(src_rows) + '\n')
    print('\n'.join(report))


main()
