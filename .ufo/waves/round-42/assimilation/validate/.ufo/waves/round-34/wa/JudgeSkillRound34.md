measured 2026-10-23T05:39:35Z

# JudgeSkillRound34 — four `Round34 rule:` lines in SKILL.md at 8d56809

Scope: judge the four `Round34 rule:` lines in `SKILL.md` (section `## Round34 — two-sample disk write rate tool`) at
8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3 against (a) the judged tool `tools/mori-disk-rate.py` at the same revision
(one offline witness per line, plus one live run) and (b) the sources each line cites (SOURCES rows S191–S195 and
copies `corpus/evidence/sources-r34/S191.src`–`S195.src`; `corpus/knowledge/disk-write-rate-r33.md` rows 3r, 4, 9,
13r). Verdicts use `supported` / `unsupported`.

Tool identity: `git hash-object tools/mori-disk-rate.py` = `git rev-parse 8d56809:tools/mori-disk-rate.py` =
`git rev-parse ba525e1a:tools/mori-disk-rate.py` = `c7ea8bdac9c98b8d350a489fb8aca3a4750bcfbf` (byte-identical at
landing commit and tip; judged object unchanged). No tools installed this run.

## Line 1 — CLI / two samples / never since-boot average
SKILL.md text: "for a current write rate run `python3 tools/mori-disk-rate.py --interval-ms N` (live: read, wait N ms,
read again) or add `--a FILE --b FILE` for two saved samples; never report the census's since-boot average as that rate
(corpus/knowledge/disk-write-rate-r33.md row 13r)".

- Offline witness: `python3 tools/mori-disk-rate.py --a w2/sampA --b w2/sampB --interval-ms 500 --sysfs w2/sysfs`
  → exit 0, JSON with `interval_ms=500`, per-device `class`/`state`/`write_Bps`, `host_basis`, `host_write_Bps`.
- `--a FILE` alone → `error: --a and --b must be given together, or neither`, exit 2; `--interval-ms 0` →
  `error: --interval-ms must be a positive number of milliseconds`, exit 2.
- Live witness: `python3 tools/mori-disk-rate.py --interval-ms 200` → exit 0; JSON classes match real `/sys/class/block`
  (`nvme0n1` disk, `nvme0n1p1/p2` partition, `dm-0` stacked). Tool code `read_live_samples` reads the first sample,
  `time.sleep(interval_ms/1000.0)`, reads again (`tools/mori-disk-rate.py` `read_live_samples`), so live = read, wait
  N ms, read again.
- No since-boot path: `grep -nE 'uptime|since_boot|since-boot|_BOOT|/proc/uptime' tools/mori-disk-rate.py` → no
  matches (rc 1); the only rate is the two-sample delta `(B - A) * 512 * 1000 // interval_ms`. Row 13r (r33
  `§Round-34 revision` table) supports the negative clause: the census value is a since-boot average, never the current
  rate.

VERDICT: supported

## Line 2 — device class order
SKILL.md text: "classify a device from `/sys/class/block/<name>` in this order: no directory → unknown; a `partition`
entry → partition (S191); a non-empty `slaves` directory → stacked (S192); a `device` entry → disk (S193); otherwise
virtual, as a zram disk registered without a parent (S194; sysstat also calls a device without a `device` link virtual,
S195)".

Offline witness (fixture sysfs; sample lines of 20 tokens): `p1` had BOTH `partition` and `device` entries →
`partition`; `st1` with non-empty `slaves/` → `stacked`; `dk1`/`dk2` with `device` → `disk`; `vr1` bare → `virtual`;
`abs1` sysfs-only → `virtual`/`absent`; `un1`, `extra` in samples but no sysfs dir → `unknown`. The tool's `classify`
(`tools/mori-disk-rate.py`) checks in exactly this order: `isdir` fail → unknown; `lexists(partition)` → partition;
non-empty `listdir(slaves)` → stacked; `lexists(device)` → disk; else virtual.

Sources (committed copies at 8d56809):
- S191.src (`block/partitions/core.c` v7.2): `part_partition_show`, `dev_attr_partition` in `part_attrs`,
  `part_attr_group` in `part_attr_groups` — supports the partition-only attribute.
- S192.src (`block/holder.c` v7.2): `bd_link_disk_holder` creates the slaves/holders symlinks (dm-0/sda example);
  `bd_unlink_disk_holder` removes them — supports non-empty `slaves` marking stacking.
- S193.src (`drivers/base/core.c` v7.2): `device` symlink created and removed only when `dev->parent &&
  device_is_not_partition(dev)` — supports `device` entry = whole disk with parent.
- S194.src (`drivers/block/zram/zram_drv.c` v7.2): `device_add_disk(NULL, zram->disk, …)` — zram registers with no
  parent, so (with S193) no `device` link → virtual.
- S195.src (`sysstat/common.c` v12.8.0): `is_device()` doc: "The device is assumed to be virtual if no
  /sys/block/<device>/device link exists" — supports the S195 clause.

VERDICT: supported

## Line 3 — state precedence and rate formula
SKILL.md text: "a device's state is bad-line, absent, gone, new, reset or ok, in that precedence; only an ok device has
a rate, `(B − A) × 512 × 1000 // interval_ms` bytes per second, and every other state reports null, never zero
(corpus/knowledge/disk-write-rate-r33.md rows 4 and 9)".

Offline witness (interval_ms=500), every device state as designed:
- `bad1` (13-token malformed line in A, valid in B) → `bad-line`, null — precedence over ok.
- `bad2` (valid in A, malformed in B) → `bad-line`, null.
- `gon1` (line in A only) → `gone`, null; `new1` (B only) → `new`, null.
- `rst1` (B sectors 50 < A 90) → `reset`, null; `abs1` (sysfs only) → `absent`, null; `ok1` (A 100 → B 200) →
  `ok`, `write_Bps=102400` = (200−100)×512×1000//500. All non-ok states printed JSON `null`, never 0.
- Tool `device_state` precedence matches the stated order (bad-line > absent > gone > new > reset > ok); rate formula
  matches. Row 4 (lower newer reading → mark interval unavailable, never negative/wrapped) and row 9 (no line → report
  unavailable, never zero) support the null-never-zero clauses.

VERDICT: supported

## Line 4 — host total
SKILL.md text: "the host total sums the disk class only and is null unless every disk is ok; partitions are already
inside their disk (row 3r) and a stacked device maps onto devices already counted (S192)".

Offline witness (fixture: disks `dk1`/`dk2`; partition `p1`, stacked `st1`, virtual `vr1`, unknown `extra`/`un1`, all
with large rates): `host_basis=["dk1","dk2"]` only; with `dk2` reset → `host_write_Bps:null`; in the second run with
`dk2` ok, host = 20480 = sum of the two disk rates, and `p1`/`st1`/`vr1` (each 10240) were excluded. Live witness
corroborates: `host_basis=["nvme0n1","nvme1n1","sda","sr0"]` and host 24043520 = nvme0n1 20111360 + nvme1n1 3932160
(dm-0 stacked, partitions excluded).

Sources: row 3r (`diskstats_show` counts a partition's contribution once; the disk's own line already holds its
partitions' sectors) supports "partitions are already inside their disk"; S192.src (holder.c) supports a stacked device
mapping onto already-counted devices. Tool `build_report` includes only class `disk` in `basis`, and `host` is null
unless every basis device is ok.

VERDICT: supported

## Findings
No defect found in scope: all four `Round34 rule:` lines match the tool's actual behavior and the sources they cite.
No contradictions between the SKILL.md text and the frozen C1 rules R1–R7 (contract.md §C1) or the tool implementation.

## Residual risk / verification gaps
- The live arm was exercised once (exit 0, classes match /sys); live-rate exactness is not claimed by these lines and
  was not re-derived ([INFERENCE]: live rates are bounded by the tool's own two reads; not independently measured).
- S192's doc example shows `/sys/block/...` paths while the tool reads `/sys/class/block/<name>/slaves`; the live
  fixture proves the class/block path yields the same stacked classification (dm-0), so no contradiction is observed on
  this host.
- Line 1's "never report the census's since-boot average" is verified structurally (no since-boot computation exists in
  the tool; grep-clean) and against row 13r, not by executing the census.
