measured 2026-10-23T08:01:00Z

# ReJudgeSkillR34 — re-judge of the four `Round34 rule:` lines, SKILL.md:831-834 at 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3

Judged object: `tools/mori-disk-rate.py` at fd2521351c6cef47384aef30afbe1e4db7e6912e. Verified blob-identical:
`git rev-parse` gives `c7ea8bdac9c98b8d350a489fb8aca3a4750bcfbf` at 8d56809, ba525e1a and fd252135, and
`git hash-object tools/mori-disk-rate.py` in the working tree gives the same. Contents used below were extracted to
`/fast/scratch/hyaku/mori-r34/a3-ReJudgeSkillR34/mori-disk-rate.py`; all fixtures are files under
`/fast/scratch/hyaku/mori-r34/a3-ReJudgeSkillR34/` (14-token `/proc/diskstats`-style lines: `8 0 <name> <f4..f9> <wr_sec> <f11..f14>`).
Verdicts below were reached from the bytes before `.ufo/waves/round-34/wa/JudgeSkillRound34.md` was opened.

## Line 831 — CLI / two samples / never since-boot average (cites row 13r)

- Code: `main` requires `--interval-ms`; `--a` and `--b` "both or neither" (usage-error path); offline reads the two
  files, live `read_live_samples` = read → `time.sleep(interval_ms/1000)` → read (`mori-disk-rate.py` `read_live_samples`).
- Witness: `python3 mori-disk-rate.py --a w1_a.txt --b w1_b.txt --sysfs w1sys --interval-ms 1000` → `sda` reported
  `write_Bps=51200` from a 100-sector delta on a base of 1,000,000 sectors. A since-boot average would be a different,
  far larger number; the tool printed only the delta rate. `nvme0n1` (equal counters) → `ok`, `write_Bps=0`.
- `--a` alone → `error: --a and --b must be given together, or neither`, exit 2. `--interval-ms 0` →
  `error: --interval-ms must be a positive number of milliseconds`, exit 2.
- Live witness: `--interval-ms 60` → exit 0, JSON, `interval_ms=60`, host basis `["nvme0n1","nvme1n1","sda","sr0"]`.
- Source: row 13r (`corpus/knowledge/disk-write-rate-r33.md`, Round-34 revision table) states the census value is a
  since-boot average and must never be reported as the current write rate — matches the negative clause.

VERDICT: supported

## Line 832 — device class order (cites S191, S192, S193, S194, S195)

- Code `classify`: `isdir` fails → unknown; `lexists(partition)` → partition; non-empty `listdir(slaves)` → stacked;
  `lexists(device)` → disk; else virtual — exactly the stated order.
- Witness `w2` fixture (one offline run): `ghost` in samples only, no sysfs dir → `unknown`; `pslv` with BOTH
  `partition` and non-empty `slaves` → `partition` (precedence proven); `sdev` with BOTH non-empty `slaves` and
  `device` → `stacked` (precedence proven); `sda` with `device` only → `disk`; `zram0` bare dir → `virtual`;
  `sda1` partition entry → `partition`; `dm0` non-empty `slaves/` → `stacked`.
- Sources: S191.src:208,222,266-268 — `DEVICE_ATTR(partition)` sits in `part_attrs`, which is the `.groups` of
  `part_type` ("partition") only: the attribute is partition-only. S192.src:43-50,62-64,126,129-131 — `bd_link_disk_holder`
  creates `slaves/` and `holders/` symlinks between holder disk and claimed bdev; non-empty `slaves` marks stacking.
  S193.src:3508-3510,3542-3543,2430-2438 — the `device` symlink is created iff `dev->parent && device_is_not_partition(dev)`
  (parent exists and dev is not `part_type`). S194.src:3094 — `device_add_disk(NULL, zram->disk, …)`: zram registers a
  disk with no parent → no `device` link → virtual. S195.src:198-205,211-224 — sysstat `is_device()` states "The device
  is assumed to be virtual if no /sys/block/<device>/device link exists".

VERDICT: supported

## Line 833 — state precedence and rate formula (cites rows 4 and 9)

- Code `device_state`: bad-line > absent > gone > new > reset > ok; rate only for ok as
  `(B-A) * 512 * 1000 // interval_ms`; non-ok → `write_Bps` null (`build_report`).
- Witness `w3` fixture (`--interval-ms 500`): `baddev`/`badgone`/`badonly` → `bad-line` null (baddev malformed in A also
  beats the `new` it would otherwise be; `badgone` malformed in B beats `gone`; `badonly` malformed-only beats `absent` —
  precedence proven); `absdev`/`absbad` → `absent` null; `gonedev` → `gone` null; `newdev` → `new` null;
  `rstdev` (500→400) → `reset` null; `okdev` (100→200) → `ok`, `write_Bps=102400` = 100×512×1000//500; `eqdev` equal
  counters → `ok`, `write_Bps=0` (an ok device may legitimately report 0; the "never zero" clause covers non-ok states).
- Sources: row 4 (lower newer reading → mark unavailable, never a negative or wrapped rate) supports `reset` → null;
  row 9 (no line of its own → unavailable, never zero writes) supports `absent`-style null. Rows 4 and 9 cover the
  `reset`/`absent` halves of the null-never-zero claim; `bad-line`/`gone`/`new` follow the same never-zero convention
  ([INFERENCE] — the cited rows do not name those three states; the claim stands on the tool).

VERDICT: supported

## Line 834 — host total (cites row 3r and S192)

- Code `build_report`: `basis` = devices with class `disk`; `host_write_Bps` = sum of their rates iff `basis` non-empty
  AND every basis device `ok`, else null.
- Witness `w4`: A→B with `sda` ok (100→200) and `sdb` reset (200→150) → `host_basis=["sda","sdb"]`,
  `host_write_Bps=null`. Second run `sdb` ok (200→300) → `host=102400` = sda 51200 + sdb 51200 exactly; `sda1`
  partition (1024), `dm0` stacked (5120), `zram0` virtual (1024) all excluded from the sum.
- Sources: row 3r (`part_stat_add` adds a partition's amount again to `bdev_whole(part)` = disk `part0`; verdict "never
  add a disk's line to the lines of its own partitions") supports "partitions are already inside their disk". S192
  supports the stacked-device→slaves mapping (see residual note for "already counted").
- Precision gap, not a defect: SKILL says "null unless every disk is ok" but omits the non-empty-basis condition —
  `w4c` (only a `zram0` virtual) → `host_basis=[]`, `host_write_Bps=null`. The frozen R7 text in the tool docstring
  carries the non-empty condition, so SKILL.md is a subset statement; consistent, not contradictory.

VERDICT: supported

## Audit of .ufo/waves/round-34/wa/JudgeSkillRound34.md

Claims that a round would cite, vs my evidence:

1. Tool blob hash `c7ea8bda…cfbf` identical at 8d56809/ba525e1a/working tree — agree (`git rev-parse`/`hash-object` above).
2. Offline witness emits `interval_ms`, per-device `class`/`state`/`write_Bps`, `host_basis`, `host_write_Bps` — agree (W1 output).
3. `--a` alone → pairing error exit 2; `--interval-ms 0` → positivity error exit 2 — agree (my runs, both).
4. Live = read, wait N ms, read again per `read_live_samples` — agree (code path; live witness exit 0).
5. No uptime/since-boot computation; only rate is the delta formula — agree (full source read).
6. Row 13r supports the never-report-since-boot clause — agree (row text).
7. `classify` checks exactly the SKILL order — agree (code; W2 precedence fixtures).
8. `p1` with partition+device entries → partition — agree (`pslv` partition+slaves → partition; `part_type` attr group proves partition precedence).
9. Sysfs-only bare dir → `virtual`/`absent` — agree (`absdev`).
10. Sample-only name, no sysfs dir → `unknown` — agree (`ghost`).
11. S191: partition attribute in partition-type group only — agree (S191.src:208,222,266-268).
12. S192: `bd_link_disk_holder` creates and `bd_unlink` removes slaves/holders links — agree (S192.src:62-64,126,129-131).
13. S193: `device` link only when `dev->parent && device_is_not_partition(dev)` — agree (S193.src:3508-3510,2430-2438).
14. S194: `device_add_disk(NULL, …)` → zram parentless → virtual — agree (S194.src:3094).
15. S195: `is_device` doc assumes virtual when no `device` link — agree (S195.src:198-205,211-224).
16. Six-state witness incl. `ok1` 102400=(200−100)×512×1000//500, all non-ok null — agree (my `okdev`/`baddev`/`rstdev` match).
17. Rows 4 and 9 support the null-never-zero clauses — agree (row 4 reset→unavailable; row 9 missing line→never zero).
18. Host witness: disk-only basis; disk reset → host null; ok run sums disks only — agree (W4a/W4b reproduce).
19. Live `host_basis=[nvme0n1,nvme1n1,sda,sr0]` and host 24043520 = 20111360+3932160 — agree: basis corroborated by my
    live run (same four names) and the sum is arithmetically consistent; the per-device figures are historical sample
    data, unverifiable [INFERENCE that they are accurate — not disproved].
20. "S192 supports a stacked device mapping onto already-counted devices" — disagree: S192.src:43-50 proves the
    slaves/holders mapping only; the "already counted" half is unsourced — the knowledge file's own Host observation
    (`disk-write-rate-r33.md` §Host observation) calls stacked re-accounting "observed on this host, not sourced".
    Frozen R7 keeps the same wording, so this overreach does not change the verdict, only the claim's sourcing.
21. Verdict line 1 `supported` — agree (W1).
22. Verdict line 2 `supported` — agree (W2 + S191–S195).
23. Verdict line 3 `supported` — agree (W3).
24. Verdict line 4 `supported` — agree (W4).
25. Residual notes: S192 doc prints `/sys/block/...` while the tool reads `/sys/class/block/...` — agree; on this host
    both trees resolve to the same entries ([INFERENCE]: sysfs symlinks make them equivalent). Line-1 negative clause
    verified structurally, not by running the census — agree as stated.

AUDIT: agree 24 / disagree 1

## Residual risk / verification gaps

- Live rates divide by the requested N ms while the actual gap is N ms plus the first sample's read time; live rates
  therefore skew low by the read duration ([INFERENCE]; not independently timed). Not claimed by any line.
- SKILL.md line 834 elides the empty-basis null (observed `w4c`: `host_basis=[]` → null). Consistent with frozen R7.
- "Already counted" for stacked devices is host-observed, not source-proven; rows 4/9 do not name bad-line/gone/new —
  both are wording-level gaps, not defects.
- No tools installed this run (pacman paused; nothing needed). No installs to record.
- Witnesses were offline `--a/--b` runs plus one live run; counter `count-c1-a1.py` was not invoked (not in this seat's scope).
