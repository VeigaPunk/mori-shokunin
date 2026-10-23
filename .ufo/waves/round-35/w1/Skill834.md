measured 2026-10-23T08:54:04Z

# Skill834 — attack of SKILL.md:834 stacked-device attribution to S192

Seat: MoriR35.Skill834 (leaf, wave 1). Lane: mori-shokunin. Attacked claim, verbatim
`SKILL.md:834`: the host-total rule ends `partitions are already inside their disk (row 3r) and a
stacked device maps onto devices already counted (S192)`.

## 1. What S192 actually is

Row `corpus/SOURCES.md:198`: S192 is Linux `block/holder.c` at v7.2, class A, purpose `the v7.2
holder/slave sysfs symlinks between a stacking disk and the device it claims`, note cell
(pipes stripped, contiguous): `bd_link_disk_holder creates sysfs symlinks; for dm-0 mapping sda,
/sys/block/dm-0/slaves/sda and /sys/block/sda/holders/dm-0`, followed in the same cell by
`lane rule: a non-empty `slaves` directory marks a stacked device (tool rule R3)`. Committed copy
`corpus/evidence/sources-r34/S192.src` (81 lines) is the unannotated holder.c text: it creates and
removes the two symlinks and nothing else — no write-counter, accounting or host-total statement
anywhere in the file.

S192 is a *classification* source. SKILL.md already cites it correctly for exactly that at
`SKILL.md:832` (a non-empty `slaves` directory → stacked). Line 834 re-uses the citation for a
*different* claim — that the stacked device's writes are already counted on devices the host total
includes. That claim is nowhere in the row or its source.

## 2. Sweep — does any committed row S180–S198 state the counted-mapping claim?

Method: full untruncated text of `corpus/SOURCES.md:186-204` (all 19 rows); committed copies
`corpus/evidence/sources-r33/S180-S190.src` (11 files) and `corpus/evidence/sources-r34/S191-S198.src`
(8 files, raw kernel/sysstat/util-linux text, no lane annotations); regex sweep over both copy
directories for already-counted / counted-twice / duplicate / double-count / maps-onto /
device-mapper / stacked / backing-device / bdev_whole / whole-disk statements.

Per-row result (row → what it states → states the claim?):

- S180 stat.rst: 17-value stat line, 512-byte sectors, tick fields — no.
- S181 iostats.rst: cumulative counters, resets, field-10 growth, procfs/sysfs equivalence — no.
- S182 genhd.c v7.2: diskstats_show printing, zero-size partitions skipped, in-flight at read,
  io_ticks jiffies; also documents that slaves/holders *directories* exist — directory existence,
  not counter duplication — no.
- S183 part_stat.h: partition adds also land on `bdev_whole(part)` — the *partition* roll-up
  (knowledge row 3r/3r2), not stacked devices — no.
- S184 blk-core.c: bdev_end_io_acct / update_io_ticks accounting paths — no.
- S185 blk-mq.c: request completion sector adds — no (its only stacked mention is queue-limit
  recompute across stacked queues, `S185.src:3264`, not counting).
- S186 blk_types.h: 512-byte sector unit, bdev_whole macro — no.
- S187 procfs-diskstats ABI: field numbering by kernel version — no.
- S188 flush-counter commit: flush request counting, not per-partition — no.
- S189 discard-counter commit: discard statistics — no.
- S190 iostat.c: extended-statistics 0.0 display quirk; dm name resolution only — no.
- S191 partitions/core.c: `partition` sysfs attribute (classification, tool rule R3) — no.
- S192 holder.c: slaves/holders symlinks (classification, tool rule R3) — no.
- S193 core.c: `device` symlink creation rules (classification) — no.
- S194 zram_drv.c: device_add_disk with NULL parent (classification) — no.
- S195 sysstat common.c is_device: virtual when no `device` link (classification) — no.
- S196 util-linux sysfs.c: partition file detection, slave helper returns a name only for exactly
  one slave — reading sysfs, not counting — no.
- S197 genhd.c v4.18 / S198 genhd.c v4.19: historical line formats — no.

VERDICT: unsupported — no committed row S180–S198 states that a stacked device maps onto devices already counted; the claim's only in-lane basis is host observation.

## 3. The lane already records the true status

`corpus/knowledge/disk-write-rate-r33.md` Host observation (round 33; evidence, not a source),
lines 41-45: dm-0 moved by the same field-10 delta as its slave, and line 42-45 states in so many
words: `That stacked-device equality is observed on this host, not sourced: no admitted` /
`source states that a device-mapper write is accounted again on the backing device` — citing
wave-1 SrcDmCore's dm.c reading — and keeps the clause frontier (FR6) until a source carries it.
Round-34 remeasure `.ufo/waves/round-34/wb/ExecStackedRemeasure.md` reproduced the equality
(Δ 219728 sectors identical on dm-0, nvme0n1p2, nvme0n1; tool host_basis excludes dm-0) and
corrected the multiplicity: a write through dm-0 lands on three lines for this host's topology
(mapper, partition, disk), so the earlier `twice` numeral in the round-34 frontier note is wrong
in count while right in mechanism.

So SKILL.md:834 attributes to S192 a claim the lane's own evidence trail classifies as
observed-on-this-host and explicitly unsourced — a citation defect, not a rule defect (the host
total itself still sums the disk class only and is unaffected).

VERDICT: unsupported — SKILL.md:834's citation of S192 for the counted-mapping clause fails; form (a) has no eligible row today.

## 4. Drafts for L1 (append-only, matching SKILL.md's correction idiom)

Form (a) — re-cited to a named row. Eligibility check ran in §2: no row S180–S198 states it, so
form (a) is not available today; the draft is the sentence L1 should land the moment such a row is
admitted (fill `Sxxx`).

```DRAFT SKILL 834-correction (form a — re-cited to a named row; not applicable until one exists)
Round34 correction to the Round34 section above (append-only): the host-total clause a stacked
device maps onto devices already counted was miscited to S192, which supplies only the slaves
directory classification (tool rule R3); it is re-cited to Sxxx, whose admitted row states that a
device-mapper write is accounted again on its backing device.
```

Form (b) — observed on this host, not sourced, with the lane's observation pointer. This is the
form the current evidence supports; L1 should land this one.

```DRAFT SKILL 834-correction (form b — observed on this host, not sourced)
Round34 correction to the Round34 section above (append-only): the host-total clause a stacked
device maps onto devices already counted is observed on this host, not sourced — no admitted source
row S180–S198 states that a device-mapper write is accounted again on its backing device, S192
supplies only the slaves-directory classification (SKILL.md line 832), the observation pointer is
.ufo/waves/round-34/wb/ExecStackedRemeasure.md (dm-0 write-sector delta equal to its slave and its
disk, 219728 sectors over 30 s, a write landing on three lines for a mapper over a partition), and
the clause stays frontier (FR6) until a source carries it (corpus/knowledge/disk-write-rate-r33.md
host observation).
```

## 5. Residual risk and verification gaps

- Copy directories hold the sources only (r33: S180-S190.src; r34: S191-S198.src); no sidecar
  annotation files exist there, so a claim cannot hide outside SOURCES.md rows plus .src text —
  both swept. `lsblk`-style tooling aside, no row was read through any channel other than the
  committed files.
- The counted-mapping claim itself may be *true* as kernel behavior (SrcDmCore's dm.c reading
  suggests the mechanism); this report judges only the citation. A future source row could make
  form (a) live — that admission is not my scope.
- Form (b) inherits ExecStackedRemeasure's topology caveat (three lines for a mapper over a
  partition); the draft sentence deliberately states the mechanism without freezing the numeral.
- No tools installed or updated (pacman transactions are paused host-wide; none attempted).
- Containment: this file and nothing else written in the lane; no git/jj writes; no processes left.
