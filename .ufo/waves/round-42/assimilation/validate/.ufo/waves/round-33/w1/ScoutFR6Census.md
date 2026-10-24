# ScoutFR6Census — FR6 recon: what the lane already says and does about disk write rates

Read-only recon. Lane files read at the working copy (2026-10-23); no lane write except this
report; no fetch, no install/update, no counter run. Line numbers are the working copy's.

## 1. The exact current computation (path:line)

| Step | What the code does | Where |
|---|---|---|
| counter file | `MORI_DISKSTATS` default `/proc/diskstats` | `tools/mori-census.sh:311` |
| divisor file | `MORI_UPTIME` default `/proc/uptime` | `tools/mori-census.sh:312` |
| divisor parse | whole file read, first token, fractional part stripped ⇒ **integer seconds**, must be >0 | `tools/mori-census.sh:1907-1908` |
| target → fs | `df -P <target>`, second line, column 1 = filesystem source | `tools/mori-census.sh:1922,1927` |
| device resolution | `dev_of`: only `/dev/*` sources; `readlink -f` follows the symlink; literal `/dev/` stripped ⇒ device basename (`/dev/mapper/root`→`dm-0`) | `tools/mori-census.sh:1872-1877,1946` |
| line selection | `awk 'NF >= 10 && $3 == d { print; exit }'` — **first** line whose raw whitespace field 3 equals that basename and that has ≥10 fields | `tools/mori-census.sh:1883` |
| field used | raw **$10** (no other field read) | `tools/mori-census.sh:1892` |
| unit conversion | `sectors * 512 / up_s` — 512 B/sector, **integer division truncation**, per device | `tools/mori-census.sh:1894` |
| row | `io_basis=since-boot io_avg_since_boot=<dev>:<rate>Bps/<up>s io_avg_unavailable=<dev>:<reason>`; `DISK_IO_UNMEASURED` info when nothing measurable; warn/crit 85/95 untouched | `tools/mori-census.sh:1958,1967-1969,1974` |
| reasons | `no-uptime`, `no-diskstats`, `diskstats-rc<N>`, `device-not-in-diskstats`, `counter-parse`, `not-a-block-device` | `tools/mori-census.sh:1881-1893,1948` |

- Partition vs disk: there is **no choice** — the probe reads whatever the df source resolves
  to. If a partition is mounted directly it reads the partition line; if a mapper device is
  mounted it reads the `dm-*` line. No aggregation, no summing, one line per target.
- dm resolution is `readlink -f` only (`:1876`); no `/sys/dev/block`, no major:minor lookup,
  no sysfs read anywhere in the lane (`grep -n 'sys/block\|block/stat' tools/*.sh tools/*.py
  SKILL.md PROTOCOL.md` → no match, 2026-10-23).
- Live reproduction, 2026-10-23T02:45:11Z (read-only reads of `df -P / /tmp`, `readlink -f`,
  `/proc/uptime`, `/proc/diskstats`): `/` → `/dev/mapper/root` → `dm-0`; `/tmp` →
  `/dev/nvme1n1p1`; uptime 67795 s; `dm-0` $10 = 445960832 ⇒ 3368315 Bps;
  `nvme1n1p1` $10 = 1115329696 ⇒ 8423420 Bps (same integer-division arithmetic as `:1894`).
- I attempted one live gate run; it printed no disk row within a 120 s `timeout` under current
  load (live mode writes nothing), so the arithmetic above was reproduced from `/proc` directly.
  The documented live rows remain `corpus/knowledge/surfaces-r7.md:127-128` and
  `surfaces-r8.md:76-78` (`dm-0:9374197Bps/13983s`).

## 2. Stated limits (as written in the lane)

- `corpus/knowledge/surfaces-r7.md:153-157`: not fleet-attributable (counts every write to the
  device since boot, OS/desktop included); nothing per-process or per-lane; cannot detect a
  burst; `/tmp` is tmpfs on the r7 host so structurally no rate.
- `corpus/knowledge/surfaces-r7.md:140-151` + `surfaces-r8.md:41,47-48,75-89`: instantaneous
  two-sample rate deferred; 0.2 s variant minimum 208 ms vs a 50 ms bar; noisy on this host
  (0 sectors in 3 of 5 reps); no threshold moved.
- `SKILL.md:43,399-406`: since-boot average only; 85/95 carry no write-rate evidence; a
  writer-less FIFO pinned for `MORI_DISKSTATS`/`MORI_UPTIME` is a named open hang
  (`corpus/knowledge/audit-r11.md:90-96`, exit 124).
- `corpus/knowledge/observability-surfaces-r2.md:271-283`; `corpus/README.md:151,161,176,340`.
- **Not stated anywhere in the lane:** counter reset/overflow handling; that the reported
  device is whatever df resolved (partition or dm); stacked dm/loop double counting;
  field-count versions; the integer-second divisor truncation; that the 512-byte unit has no
  SOURCES row. `grep -n -i reset` over `surfaces-r7.md`, `surfaces-r8.md`,
  `observability-surfaces-r2.md`, `SKILL.md` returns one unrelated hit
  (`observability-surfaces-r2.md:160`, an mtime-reset sentence).

## 3. Every place the lane asserts a diskstats fact, and its backing

1. `tools/mori-census.sh:1887-1889` — "field 10 of a diskstats line = sectors written
   (field 8 is writes completed); 512 bytes per sector is the counter's unit". **No SOURCES row
   cited.** S033 (queued, `SOURCES.md:39`) states Field 7 = sectors written in doc numbering,
   which is consistent, but nothing in the registry states 512.
2. `tools/mori-census.sh:1866-1870` — "per-boot counters ⇒ the only rate derivable without a
   sampling interval is the average since boot". Assertion; no source.
3. `corpus/knowledge/surfaces-r7.md:124-129` — impl description (field 10, `readlink -f` →
   `dm-0`, 512 arithmetic); cites code lines, not a source.
4. `corpus/knowledge/observability-surfaces-r2.md:271-283` — same, r7 update paragraph.
5. `corpus/knowledge/surfaces-r8.md:41,75-89` — own measurements (dwell cost, noise).
6. `SKILL.md:43,401-403` — "sectors written × 512 ÷ uptime"; since-boot only.
7. `corpus/lessons/2026-10-15-free-lunch-measurements-counter-baselines.md:35-36,102-108` —
   own-work: diskstats holds only since-boot sector totals; measured pair 200924364 → 200929868
   (5504 sectors over 3 s).
8. `corpus/lessons/round-12.md:159` — Gate-style row for S033 with quote
   "This is the total number of sectors written successfully." and sha
   `aeef40c141be7bb8…`; its SOURCES row is `queued`, not `mined`.
9. `corpus/evidence/README.md:488` — `diskrate.log` receipt (own-work; live row + manual check).
10. Selftest fixtures `tools/mori-census.sh:3202` (16-field line) and `:4466` (14-field line);
    `audit-r11.md:344` uses an 11-field line — all pass the `NF >= 10` gate.

## 4. The 11 named candidate rows: what each must add to be depth, not repetition

| candidate row | lane today | what a source-backed row must state | dispatched seat |
|---|---|---|---|
| sector unit | code comment says 512 (`:1888-1889`), unsourced; S033's page has **zero** "512" and zero "bytes" occurrences | sector = 512 = 2**9 bytes, `SECTOR_SHIFT`/`SECTOR_SIZE`; keep distinct from device logical/physical block size | SrcSectorSize (draft: `blk_types.h` v7.2, sha `adff86f6…`, quotes at :26,:27-28,:31,:34); SrcSysfsBlockAbi for the block-size contrast |
| completion-time accounting | nothing | Field 7 counts sectors written **successfully** (completed); Field 8 = ms writing (blk_mq_alloc_request→__blk_mq_end_request); Field 11 = weighted, in-flight × ms (completion time + backlog); 4.19 ns→ms truncation ⇒ the rate is a completion-byte rate, not busy time or latency | SrcIostatsRst (field text), SrcBlkCore |
| wrap / reset | nothing; no finding id exists for a reset | counters cumulative/monotonic except Field 9; remaining fields reset at boot, device reattachment/reinitialization, or overflow; readers should detect and handle resets when comparing snapshots ⇒ a since-boot divisor silently assumes no reset | SrcIostatsRst |
| partition+disk double count | probe reads exactly one resolved line, so it cannot double count today | each set applies only to the indicated device; system-wide needs summing all devices; a merged operation is attributed to the partition holding the first sector; 2.6.25 made disk/partition sets consistent again ⇒ rule: never add a partition line to its disk line. Hazard: the page's older sentence "There are only four fields available for partitions on 2.6+ machines" is historical — citing it as current is a caveat ⇒ unsupported under R-J | SrcIostatsRst, SrcGenhd, SrcPartStat |
| stacked dm/loop double count | nothing; live 02:45:11Z shows `dm-0` $10 = `nvme0n1p2` $10 = 445960832, and `nvme0n1p1`+`nvme0n1p2` = `nvme0n1` exactly (352 + 445960832 = 445961184) | the same write bytes are visible on the dm device, its backing partition, and the whole disk ⇒ rule: report the resolved device only, never a sum | SrcDmCore, SrcLoopOrMd, SrcGenhd |
| 14/18/20 field counts | `NF >= 10` only; fixtures 11/14/16 fields; live host: all 11 diskstats lines have 20 raw fields | the doc field list runs Field 1–17 (discard 12–15, flush 16–17) and grew by version ⇒ raw index $10 = doc Field 7 because genhd prints major/minor/name first; pinned commits for the additions | SrcDiscardCommit (4.18/4.19), SrcFlushCommit (5.5), SrcGenhd |
| in-flight gauge | never read | Field 9 is the one field that should go to zero, incremented as requests are queued and decremented as they finish ⇒ a gauge, no rate derivable; live raw field 12 = 1 on `dm-0`/`nvme0n1p2`/`nvme0n1`, 0 on partitions | SrcIostatsRst |
| io_ticks / %util | never read; no %util computed | Field 10 = ms doing I/Os, increases while Field 9 nonzero; since 5.0 counts jiffies when a request started or completed, and >2-jiffy requests may not be fully accounted under concurrency ⇒ %util from these fields is approximate; the formula belongs to sysstat | SrcIostatsRst, SrcSysstatIostat |
| since-boot average vs two-sample rate | the average is restated in ≥6 places (SKILL, r7, r8, r2 note, README, lesson) — highest repetition risk | counters are cumulative ⇒ a rate needs two samples and a dwell; the reset-at-boot statement bounds the average's basis ⇒ rule: label the since-boot average as such, never as instantaneous. The lane's own 208 ms/50 ms numbers must stay out of observation/reading cells (R-J) | SrcIostatsRst |
| extra, high-depth | nothing in the lane | sysfs `/sys/block/<dev>/stat` equivalence: same 17 statistics, no major/minor prefix, first value equal, per-partition subdirectories; discard/flush sectors are separate counters (Field 12–17, flush "Not tracked for partitions") and must not enter a write rate; Field 2/6 merging makes writes-completed ≠ requests; the no-lock/per-CPU summation paragraph (minor inaccuracies, possible overflow when summing) | SrcStatRst, SrcSysfsBlockAbi, SrcGenhd, SrcBlkMq |

## 5. Source-opening facts for the L1

- `SOURCES.md:39` S033 = `https://docs.kernel.org/admin-guide/iostats.html`, status **queued**
  (not `mined`) and its URL is already in SOURCES.md ⇒ unusable as a new id on both counts.
- The same document as a byte-stable file (`https://raw.githubusercontent.com/torvalds/linux/
  <tag>/Documentation/admin-guide/iostats.rst`) is **absent** from SOURCES.md at the tip
  (grep, 2026-10-23), so it passes the literal URL-new test — but it is the same document as
  S033. The C0 seat already fetched the v6.12 copy
  (`.ufo/waves/round-33/c0/CtlShortcutIds.md:68`, sha `f76d7ea58954ae30cc7877bd48c71c9c3265726caebca54aafbc5d6fa5086923`).
  The lane's other kernel sources are pinned at `v7.2`; a v7.2 `iostats.rst` must be opened by
  the source seat (this recon did not fetch it).
- Verified on the C0 seat's scratch copy of the docs.kernel.org page
  (`/fast/scratch/hyaku/mori-r33/CtlShortcutIds/S033.src`, 21784 bytes, sha256
  `aeef40c141be7bb8e9e94c3fa94d7088b15c564112c61e8e93191883b09346de`): `grep -c 512` = 0,
  `grep -c -i bytes` = 0. It states the field list (`:216-260`), the reset paragraph
  (`:201-205`: "All fields are cumulative, monotonic counters, except for field 9, which
  resets to zero as I/Os complete. The remaining fields reset at boot, on device reattachment
  or reinitialization, or when the underlying counter overflows."), the sysfs equivalence
  example ("Both files contain the same 17 statistics", "the first stat value for nvme0n1 is
  255999 in both files"), and the Disks-vs-Partitions section (`:285-312`, incl. "an operation
  is attributed to the partition which contains the first sector of the request after the
  eventual merges"). This copy is scratch, not a committed copy — a new id needs
  `corpus/evidence/sources-r33/S###.src` with the Gate sha256.

## 6. Row-design constraints from the frozen text (for the drafters)

- Amendment A1 (`count-c1-a1.py:8-11`): a reading cell fails if it contains a run of 6
  consecutive words that also occurs in a Gate quote of a cited new id ⇒ paraphrase; give the
  quote separately.
- The anti-shortcut condition requires every row citing a new id to share ≥2 distinct 4+ letter
  words with that id's Gate quotes (contract P-C1 sentence) — so pure paraphrase with no shared
  vocabulary also fails; name the field/mechanism in the row's own words.
- R-J: every fact in observation and reading must be stated by the located quotes, and the
  verdict must follow with no further fact. Lane measurements (208 ms dwell, 50 ms budget, the
  0.2 s arm) cannot be asserted in observation/reading cells; the verdict cell must be a
  reporting rule that follows from the reading alone (detection and report only).
- Volume: the named 11 plus the four extra candidates in §4 give ≥15 pairwise-distinct rows;
  C1 needs ≥10 with ≥8 citing new ids (≥5 distinct ids).

## 7. Unknowns / inference

- Whether the raw `iostats.rst` URL is acceptable as URL-new given it duplicates S033's
  document is the L1's call; the literal P-C1 test only looks for the URL string.
- I did not open the v7.2 `iostats.rst`; whether its field text matches the 2026-10-19
  docs.kernel.org snapshot is unverified here.
- Whether SrcStatRst/SrcGenhd drafts state the raw-index-vs-doc-field-order fact (needed for
  the field-count row) was unverified at read time (peer drafts still landing).
- No finding id exists for a counter reset, so the reset row's "the census cannot detect it"
  is a lane-doctrine statement to be declared as such, not a sourced fact.
- [INFERENCE] No double counting happens in the current census because each df target resolves
  to exactly one line and no summing code exists; the hazard is in the reading rules an entry
  states and in any future multi-target sum.
