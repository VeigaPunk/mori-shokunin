author: mori-shokunin L1 MoriR33 (round 33, attempt 1)

# mori round 33 — lesson

## Gate (rows opened 2026-10-23 in round 33)

Eleven sources admitted for C1 (FR6). Ten were opened by wave-1 seats and S187 by the L1. Each copy is committed
unchanged at `corpus/evidence/sources-r33/S###.src`; every seat fetched twice and both sha256 values matched. Quotes
and locators were re-located by the L1 in the committed copies (`/fast/scratch/hyaku/mori-r33/L1/build_sources.py`);
a seat-drafted quote that was not contiguous in its copy (SrcSectorSize "512 = 2**9 bytes.", split by a ` * ` comment
prefix) was replaced by a contiguous one.

| id | url | accessed | sha256 | quotes | decision |
|---|---|---|---|---|---|
| S180 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/block/stat.rst | 2026-10-23T02:39:46Z | `4c35b795a518ceefea985f11e53b51f71d58fc99bf5a0920ca3738f13c90cb2e` | `S180.src:21-22` (17 words): "The stat file consists of a single line of text containing 17 decimal values separated by whitespace."; `S180.src:71-73` (13 words): "are the standard UNIX 512-byte sectors, not any device- or filesystem-specific block size."; `S180.src:73` (8 words): "The counters are incremented when the I/O completes."; `S180.src:79-80` (17 words): "If there are multiple I/O requests waiting, these values will increase at a rate greater than 1000/second" | admit, A, mined |
| S181 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/iostats.rst | 2026-10-23T02:40:16Z | `166bdc8fd4ee9e53bcb86804e0d22d50c89314dcfc1a248814b0069300034124` | `S181.src:33-34` (17 words): "All fields are cumulative, monotonic counters, except for field 9, which resets to zero as I/Os complete."; `S181.src:34-36` (17 words): "The remaining fields reset at boot, on device reattachment or reinitialization, or when the underlying counter overflows."; `S181.src:76` (10 words): "This field increases so long as field 9 is nonzero."; `S181.src:22` (7 words): "Both files contain the same 17 statistics." | admit, A, mined |
| S182 | https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c | 2026-10-23T02:39:43Z | `8c2faa1564190e9a8e4cf3ebac5e2561b96818e38560cdcf44fea1761c8d39a5` | `S182.src:1371-1374` (8 words): "if (bdev_is_partition(hd) && !bdev_nr_sectors(hd)) continue; inflight = bdev_count_inflight(hd);"; `S182.src:1425` (4 words): "proc_create_seq(\"diskstats\", 0, NULL, &diskstats_op);"; `S182.src:1395` (4 words): "seq_put_decimal_ull(seqf, \" \", jiffies_to_msecs(stat.io_ticks));"; `S182.src:1403` (4 words): "seq_put_decimal_ull(seqf, \" \", stat.sectors[STAT_DISCARD]);" | admit, A, mined |
| S183 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/part_stat.h | 2026-10-23T02:39:48Z | `2e22ee58e88396108d9962b122082d899fd517e3c67195e9dee580db63d55a9a` | `S183.src:60-63` (17 words): "#define part_stat_add(part, field, addnd) do { \\ __part_stat_add((part), field, addnd); \\ if (bdev_is_partition(part)) \\ __part_stat_add(bdev_whole(part), field, addnd);"; `S183.src:10` (3 words): "unsigned long sectors[NR_STAT_GROUPS];" | admit, A, mined |
| S184 | https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-core.c | 2026-10-23T02:39:49Z | `528501312dbd8da7649051006f12203fbef03f5180c4408ccc20856262c77827` | `S184.src:1100` (7 words): "void bdev_end_io_acct(struct block_device *bdev, enum req_op op,"; `S184.src:1108-1110` (8 words): "update_io_ticks(bdev, now, true); part_stat_inc(bdev, ios[sgrp]); part_stat_add(bdev, sectors[sgrp], sectors);"; `S184.src:1067-1068` (8 words): "(end \|\| bdev_count_inflight(part))) __part_stat_add(part, io_ticks, now - stamp);" | admit, A, mined |
| S185 | https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-mq.c | 2026-10-23T02:39:58Z | `7483f1738ad1a00372f5fca0e553023ff4a683e4e2a73c01b3da31302bba8c11` | `S185.src:856` (8 words): "static void blk_account_io_completion(struct request *req, unsigned int bytes)"; `S185.src:858` (5 words): "if (req->rq_flags & RQF_IO_STAT) {"; `S185.src:862` (5 words): "part_stat_add(req->part, sectors[sgrp], bytes >> 9);" | admit, A, mined |
| S186 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/blk_types.h | 2026-10-23T02:39:40Z | `adff86f6d9433c496dc5ddf32d0e353a24969af7ed90191dffc562f1998b2e6e` | `S186.src:25` (9 words): "The basic unit of block I/O is a sector."; `S186.src:26` (9 words): "The size of one sector is 512 = 2**9"; `S186.src:31` (3 words): "#define SECTOR_SHIFT 9"; `S186.src:84-85` (4 words): "#define bdev_whole(_bdev) \\ ((_bdev)->bd_disk->part0)" | admit, A, mined |
| S187 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/ABI/testing/procfs-diskstats | 2026-10-23T02:46:06Z | `0f2ffdc724e0a666c54aa3b1f1e94f93ce6b76745827d301dd164d789bbdd3b7` | `S187.src:6-7` (7 words): "Each line contains the following 14 fields:"; `S187.src:19-21` (13 words): "10 sectors written 11 time spent writing (ms) 12 I/Os currently in progress"; `S187.src:26-27` (14 words): "Kernel 4.18+ appends four more fields for discard tracking putting the total at 18:"; `S187.src:36` (9 words): "Kernel 5.5+ appends two more fields for flush requests:" | admit, A, mined |
| S188 | https://github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch | 2026-10-23T02:40:15Z | `a844836a15c04bfb15f44f7398851074d901afff5206509ea9be661ac5758d89` | `S188.src:9` (10 words): "Block layer has sophisticated engine for combining several flush requests"; `S188.src:11` (10 words): "Requests which trigger flushes usually are barriers - zero-size writes."; `S188.src:72` (11 words): "This counts flush requests executed by disk. Not tracked for partitions."; `S188.src:71` (13 words): "Block layer combines flush requests and executes at most one at a time." | admit, A, mined |
| S189 | https://github.com/torvalds/linux/commit/bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c.patch | 2026-10-23T02:40:27Z | `f265ef76e862e4e48cdbdae1b4702cbe47b356501d5d6cbfe9abeaaacd4cf318` | `S189.src:9-10` (12 words): "These are tracked with the same four stats as reads and writes:"; `S189.src:12-15` (20 words): "Number of discard ios completed. Number of discard ios merged Number of discard sectors completed Milliseconds spent on discard requests" | admit, A, mined |
| S190 | https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c | 2026-10-23T02:40:11Z | `f099229c0051be9538f220d63fe7953247ee947f112d367ff647d791953b9dce` | `S190.src:1462` (9 words): "void write_ext_stat(unsigned long long itv, int fctr, int hpart,"; `S190.src:1151` (4 words): "@ioi Current sample statistics."; `S190.src:1152` (4 words): "@ioj Previous sample statistics."; `S190.src:1516-1517` (11 words): "xios.wsectors = ioi->wr_sectors < ioj->wr_sectors ? 0.0 : S_VALUE(ioj->wr_sectors, ioi->wr_sectors, itv);" | admit, A, mined |

Opened but not registered (no table row rests on them; reports committed): `drivers/md/dm.c` at v7.2 (SrcDmCore,
sha256 `b01ff2d6…`: dm accounts the original bio on the dm device; it does not state that the backing device counts the
same write again, so the host-observed dm double count stays unsourced), `drivers/block/loop.c` and `drivers/md/md.c`
at v7.2 (SrcLoopOrMd: no member-side double count stated), `Documentation/ABI/stable/sysfs-block` at v7.2
(SrcSysfsBlockAbi: the stat entry and queue block sizes; it does not compare the stat sector unit with the block
size). The docs.kernel.org iostats page is already S033 (`queued`); S181 is its tag-pinned source file, a different URL
whose bytes are stable.

Status changes this round: no status, recheck or used-by cell changed. Six teaches or scope cells changed (routed
defect 3, below). New rows S180–S190 are `mined`, used by `corpus/knowledge/disk-write-rate-r33.md`.

## Round-32 repair (routed by `corpus/lessons/round-32-verifier-spotcheck.md` §8)

Rule R-R (frozen in `.ufo/waves/round-33/contract.md` before any seat ran; quoted word for word in every repair seat's
dispatch and in the repair judge's dispatch and receipt): "A teaches-cell clause is supported only when a quote located
in the committed copy of a page that the row's own source cell names states it; a row is current under the round-32
definition only when its population page alone supports every clause of its teaches cell; a clause the judge would
accept only with a caveat, through absence of contradiction, or through a page the row's source cell does not name is
unsupported."

### 1. Five `current` rows that their population page does not carry (correction, append-only)

Round 32's `## Recheck` rows for S058, S117, S128, S149 and S137 stay as written in `corpus/lessons/round-32.md`.
Under the round-32 frozen definition none of the five is `current`: its population page alone does not support every
clause of its teaches cell. Round 32's C1 stays a miss. The clauses were re-checked on the pages each row's own source
cell names; copies are committed at `corpus/evidence/recheck-r33/` (sha256 in `corpus/evidence/recheck-r33/SHA256SUMS`) and, for the population
pages, at `corpus/evidence/recheck-r32/`. Clause tables with every located quote: `.ufo/waves/round-33/w1/RepairS058.md`,
`RepairS117.md`, `RepairS128.md`, `RepairS149.md`, `RepairS137.md`.

| row | round-32 verdict → corrected | clauses the population page does not carry | supported on another page the row names (committed copy:line) | unsupported on every page the row names |
|---|---|---|---|---|
| S058 | current → not current (population page alone) | the whole diff-tree half | `-r` "Recurse into sub-trees." `S058-difftree-r33.src:4377`; two trees compared first-to-second `:4402`; `--stdin` hides merge diffs by default `:4420-4422`; `--root` creation event `:4385-4386`; `--name-status` `:3663-3664` | a merge *requires* the explicit first-parent form `<commit>^1 <commit>`; a root commit *needs* `--root` (both lane procedure, undeclared) |
| S117 | current → not current | every factual clause (the population page is the tags JSON) | release-local literals only: v1.8 and v1.9.0 `mem avail <=` (`S117-main-v1.8.src:382-383`, `S117-main-v1.9.0.src:414-415`); v1.7 `mem <=` (`S117-main-v1.7.src:326-327`); per-tag action and escalation literals (`S117-kill-v1.7.src:167,377`, `S117-kill-v1.8.src:230,539`, `S117-kill-v1.9.0.src:318,627`); `PRIPCT "%5.2lf%%"` (`S117-msg-v1.9.0.src:9-10`); a padded single-digit example line `mem avail <=  5.00%` (`S117-README-v1.9.0.src:146`) | every cross-release clause: "since v1.8", "unchanged in v1.9.0", "never prints" in v1.7, "stable prefixes", "trailing fields change", "the version line identifies the grammar". Nine of the row's ten pages have committed copies; the releases feed (`api.github.com/…/releases`) was not committed, so these clauses are unsupported on the nine committed pages and unchecked on the tenth |
| S128 | current → not current | `totalpages/1000` scaling; read-only `oom_score` `[0,2000]` export | `oom_score` displays the kernel's current score and reflects `oom_score_adj` (`S128-S149-oom_score.src:73-75,97-98`, the row's own second URL) | `totalpages/1000` scaling; read-only access; the `[0,2000]` range (these rest on S127 kernel code, a different row); "the two files are different contracts" (lane assessment; wave-2 AttackRepairS128) |
| S149 | current → not current | fork copy and floor; unprivileged-write floor; kernel scaling; `[0,2000]` export; root allowance absent in v7.2 | the score reflects the adjustment (`S128-S149-oom_score.src:97-98`) | on the two man pages the source cell gives as URLs: fork copy and floor; unprivileged-write floor; `totalpages/1000`; read-only `[0,2000]`; absence of the 3% root term in v7.2; the "supersedes S128" history and the "only there" / "documentation gap" assessments (lane inference). The source cell also refers to rows S127 and S003 by id; wave-2 AttackRepairS149 found the lane-root copies `base.c` and `oom_kill.c` state the scaling, the read-only export and the write floor, but those are other rows' pages, not pages this row names, so under R-R they do not make S149 current |
| S137 | current → not current | v1.2 removal; v1.9.0 ignored-option output; `--kernel-oom` spelling | "Option -k is ignored since earlyoom v1.2" and the `kernel-oom` long option, at the commit-pinned `main.c` (`S137-main-750a.src:260`, `:201`, `:352`) | that a v1.9.0 binary prints that output (the page is commit `750a7c0d`, not v1.9.0); "delegation claims must name the build" (lane rule, undeclared) |

The judge JudgeRecheck's five `agree` lines for these rows conceded the unsupported part and accepted the row through
companion sources or absence of contradiction (`.ufo/waves/round-32/judge/JudgeRecheck.md:63,73-76`); under R-R those
are `unsupported`.

### 2. Judge rule drift and the citation to a nonexistent finding

`corpus/lessons/round-32.md:113-116` cites "`JudgeRecheck` finding 1". The receipt has no numbered findings
(`grep -n -i finding .ufo/waves/round-32/judge/JudgeRecheck.md` → no match, wave-1 DraftJudgeRuleQuality); the loose
reading is in its per-row reasons at `JudgeRecheck.md:63,73-76`, and the S058 shape was ReviewMultiSource Finding 1
(`.ufo/waves/round-32/r1/ReviewMultiSource.md:22`). An append-only correction is added to `corpus/lessons/round-32.md`.
QUALITY 97 (new) requires the frozen rule word for word in every judge dispatch and receipt; this round's counter checks
it (`count-c1-a1.py`, R-J), and the repair judge's receipt quotes R-R.

### 3. Six rows with undeclared lane-inference clauses (critic CriticScopingRows, not adjudicated by the closure)

Each lane-application clause is now declared with `lane rule:`; no other word changed (wave-1 ScopeS041, ScopeS044,
ScopeS051, ScopeS062, ScopeS064, ScopeS069). Old → new, teaches cell unless noted:

- S041: "…in a time window; it does not identify…" → "…in a time window; lane rule: it does not identify…".
- S044: "…detached HEAD state; a commit-id read is not…" → "…detached HEAD state; lane rule: a commit-id read is not…".
- S051: "…under schedules. A class-hit gate…" → "…under schedules. lane rule: A class-hit gate…".
- S062: "…no whitespace, error on NaN/Infinity, no duplicate names; -0 is a parser SHOULD-error per the verified errata;
  a Python json.dumps identity…" → "…no whitespace between JSON tokens, error on NaN/Infinity, no duplicate names; lane
  rule: -0 is a parser SHOULD-error per the verified errata; lane rule: a Python json.dumps identity…" ("between JSON
  tokens" added after wave-2 AttackScopeEdits: the RFC forbids whitespace between tokens, not inside strings).
- S064 scope: "…existing commit object; not remote publication…" → "…existing commit object; lane rule: not remote
  publication…"; teaches: "Resolve a selector once with --verify --end-of-options and commit peeling, retain the full
  object id, then separately bind…" → "Resolve a selector with --verify --end-of-options and commit peeling; lane rule:
  do it once, retain the full object id, then separately bind…" (wave-2 AttackScopeEdits: "once" and "retain" are
  lane procedure, not page text; the page-stated flags stay outside the label).
- S069: "…cannot see symlinks: reject absolute…" → "…cannot see symlinks: lane rule: reject absolute…".

Judge-reason misstatements recorded (round-32 receipt unchanged): S062's reason says other rows attribute the
`json.dumps` clause, but no row's cell does (S063 is a rejected parameter-contract row; ScopeS062); S069's reason imports
S073's own-rule disclaimer, which S069's frozen cell lacked (ScopeS069).

### 4. Cut quotes S128 Q3 and S149 Q2

Both stop before ", although a process can always increase its own oom_adj setting". The whole sentence in the
committed copies (`corpus/evidence/recheck-r32/S128.src`, `S149.src`; wave-1 RepairS128, RepairS149; 23 words after tag
stripping): "A process must be privileged (CAP_SYS_RESOURCE) to update this file, although a process can always increase its
own oom_adj setting (since Linux 2.6.20)." The round-32 rows are not rewritten; this is the whole-sentence quote a later
recheck uses. (Corrected after wave-2 AttackRepairS128: a draft dropped "(since Linux 2.6.20)".)

### 5. Second URLs outside the round-32 population

`python3 /fast/scratch/hyaku/mori-r33/ExecSecondUrls/second-urls.py` (sha256 `997128c8…`, copy and output committed at
`.ufo/waves/round-33/evidence/second-urls.py`, `second-urls.txt`) reads the source cell only:
`rows=34 multi_url_rows=6 other_urls=14 pinned=9 unpinned=5`. The five unpinned ones are S056 PMC mirror, S058
git-diff-tree, S117 releases feed, S128 and S149 `oom_score.5`; S058's diff-tree and the `oom_score.5` page were
re-opened this round (§1). Wave-2 ReviewSecondUrls scanned every cell of the 34 rows and found two more URLs outside
the source cell: S051's anchor names the landing page `https://csrc.nist.gov/pubs/sp/800/122/final` (unpinned), and
S149's anchor names a `git.kernel.org` man-page URL pinned by `?id=man-pages-6.20` (a pin shape the script does not
recognise). Counted over all cells: 16 other URLs, 8 rows, 6 unpinned. A future freshness claim counts all 16. The
S060 in-toto `blob/main` files are not in the 34-row population (wave-1 ScoutRoutedLedger G5); they stay named here
as a further unpinned set.

### 6. Carried a third time: round-30 detector false positives/negatives and the FR5 census probe — retired explicitly

- Detectors (`writer-tool-source-citation`, `writer-tool-run-output` in `tools/mori-blind-check.sh`): the concrete cases
  are F1–F6 in `.ufo/waves/round-31/w1/ReviewGateR30Lines.md`; wave-1 ExecItem6 rebuilt them as B1–B8 and measured the
  committed tool: 4 false-positive lines (B1, B2, B3, B4) and B5–B8 silent. A five-line candidate fix (F2, F3, F4, F6)
  was measured in scratch only (selftest PASS; frozen `count-c2.py` still `exact=16/16`); F1 and F5 trade one error for
  another and need a rule decision, not a regex. Retired from the routed carry and registered as operability debt for a
  later claim: the defects are now enumerated with fixtures and a measured fix, and a tool change belongs in a claim
  whose counter scores those fixtures. (Correction after wave-2 CriticItem6Retire: an earlier draft said a tool change
  would move the round-32 frozen run; it would not — `verify.sh` runs its own pinned copy at
  `.ufo/waves/round-32/frozen/blind-check/tool/`.)
- FR5 census probe: under the hyaku inline driver the census finds no `shokunin-watchdog` pid (`pids=0`) and prints
  `FINDING WATCHDOG_ABSENT severity=warn` every round (ExecItem6 full census run, 104.45 s, `MORI_CENSUS: DRIFT
  (findings=30 drift=11 unavailable=1 surfaces=8)`). The finding reports exactly that observation; it does not show
  that the fleet is unwatched, because the inline driver writes `launch`/`complete` lines to `.ufo/watchdog.log`
  without a daemon. Retired from the routed carry: reading the inline driver's log as a second liveness source is a
  coverage change, now named in FR5's boundary (`corpus/README.md` Frontier), not a defect of the probe.

## Mistakes

- **M1 — a judge applied a looser rule than its dispatch and the receipt let it pass (class: judge rule drift /
  caveated agreement; round 32).** Evidence: `.ufo/waves/round-32/r1-dispatch.json` carries "Reject (disagree) a row
  when … a `current` verdict claims support for teaches-cell facts the quoted page does not carry"; the receipt
  `.ufo/waves/round-32/judge/JudgeRecheck.md` does not contain that sentence and records `agree` for S058, S117, S128,
  S149 and S137 while its reasons concede the unsupported part (`:63,73-76`); closure ruling
  `corpus/lessons/round-32-verifier-spotcheck.md:34-56`. Captured-by: none — round 32's R4 checked only for an `agree`
  line and the judged-bytes sha (QUALITY 95), not the rule applied. Fix: QUALITY 97; this round's counter requires the
  frozen R-J sentence in both the judge dispatch and receipt (`count-c1-a1.py`), and R-R is quoted in the repair
  judge's. Shown able to fail: the round-32 receipt fails QUALITY 97's check (`grep -F` count 0 against 1 in the
  dispatch); C0 control CtlJudgeShapes "R-J removed from the receipt" prints `C1=unmet` (`judge`).
- **M2 — the frozen counter was looser than its own predicate sentence (class: code weaker than the sentence it
  claims to implement; round 33, caught before data).** Evidence: P-C1 requires every supported row to carry a valid
  span, but `count-c1.py` dropped bad-span rows from the count, so a 5-word span and a span from an uncited copy still
  printed `C1=met` (C0 CtlJudgeShapes `24aea096`, `c126ffcd`); readings copied from Gate quotes and rows distinct only
  by punctuation also met it (CtlShortcutIds `fad276ef`, `76d5c229`). Captured-by: the pre-freeze adversarial control
  wave (orchestrator ruling 01:05Z). Fix: Amendment A1 (`count-c1-a1.py`, committed `fdf4371f` before wave 1). Shown
  able to fail: the same four commits print `C1=met` under `count-c1.py` and `C1=unmet` under `count-c1-a1.py`
  (`.ufo/waves/round-33/evidence/c1-controls.txt`).
- **M3 — a seat-drafted Gate quote was not contiguous in its own copy (class: quote not located; round 33, caught at
  integration).** Evidence: wave-1 SrcSectorSize drafted "The size of one sector is 512 = 2**9 bytes." but the copy
  breaks the sentence with a ` * ` comment prefix (`corpus/evidence/sources-r33/S186.src:26-27`); the L1's builder
  asserts every quote is a substring of the whitespace-collapsed copy and stopped on it. Captured-by: the counter's copy
  check (P-C1, "contains every quote") and the builder's assertion. Fix: quotes are re-located by script from the
  committed copy and their locators computed, not typed (`/fast/scratch/hyaku/mori-r33/L1/build_sources.py`, quoted in
  the Gate note). Shown able to fail: the seat's quote is not a substring of the collapsed copy (`norm(q) in norm(copy)`
  is False).

## Attacks on the data and how they were settled (wave 2, 42 seats, before the judges)

Fixed before the judge read the entry (data revision `ab8f4cfe`): row 2 gained the `RQF_IO_STAT` guard and its quote
(AttackRow02, AttackSrc185); row 3's verdict narrowed to "never add a disk's line to its own partitions" and cites
`bdev_whole` = `part0` (AttackRow03, AttackSrc183, CriticAxisNoHarm); row 4 limited to sectors written (AttackRow04);
row 5 drops "queue depth" and the per-read link is quoted through `proc_create_seq("diskstats", …)` (AttackRow05,
AttackSrc182); row 6 drops the field-10 identity and calls the busy share approximate (AttackRow06, AttackSrc181,
CriticAxisNoHarm); row 7 "can climb", no "tick" wording (AttackRow07, AttackSrc180); row 8 no "whitespace-separated",
20 made explicit (AttackSrc187); row 11 separates request count from duration and quotes the combine sentence
(AttackRow11, AttackSrc188); row 13 no longer equates uptime with counter lifetime (AttackRow13, CriticEntryProse);
row 14 narrowed to iostat's extended-statistics display — the default report computes its rate unclamped
(AttackSrc190 blocker, AttackRow14); entry prose corrected (CriticEntryProse); SKILL rules carry every verdict
(ReviewSkillRound33); S184/S189 quotes widened, S181/S186/S188/S190 cells and anchors tightened (AttackSrc18x).

Recorded, not fixed (open findings for the closure):
- AttackRow08: the ABI file's "Kernel 4.18+" discard boundary is contradicted by v4.18 code (v4.19 first emits 18); row
  8 now attributes the boundary to the ABI file and its verdict does not depend on it.
- CtlGlossaryA1: an 11-row definition-only glossary with honest self-judgments prints `C1=met` under P-C1-A1
  (sandbox `04c02ae`). The predicate certifies sourced rows and a judge, not that each row carries a write-rate
  decision; every real row carries one (the same report, row by row). Reported against the claim's discrimination.
- CtlLocatorStale: a false `file:L` locator survives the counter (exit 0); a stale copy and an uncited span are caught.
- ReviewCounterData: at `62db24c0` every condition but `judge` was met; rows 9 and 14 meet the overlap check with
  generic words only.
- Repair rows: S117's releases feed was never committed (unchecked on that page); S128 gained the omitted "different
  contracts" clause; S149's row now separates its two named pages from rows S127/S003; S137's `-k` vs `--kernel-oom`
  identity (AttackRepairS137 F1) stays as a note. MutQuality97: criterion 97's concession half needs a human reader.
- No-harm: retention metric 4 at `62db24c0` = 4 at base (ExecRetentionData); census validate `mori ok`, no new W04
  (ScoutCensusMisroot); fleet-root sweep found no mori round-33 file (two seats briefly wrote reports at the fleet root
  by a relative path and moved them into the lane themselves: AttackSrc180, AttackSrc184).

## Judges (residual call J, 2 reviewer seats, dispatch committed `7a0234c2` before they ran)

- JudgeC1Rows (entry sha `eaeb1100…c764` at `ab8f4cfe`, R-J quoted): 10 supported, 4 unsupported — row 3 (the
  disk line printing `part0` is in S182, not cited), row 6 ("approximate" needs S181:78-80, not cited), row 7 (the
  procfs/sysfs identity is S181:22, not cited), row 13 (the census formula is a tool fact, not a source fact). The entry
  is left as judged: an edit would change the judged bytes. The four rows stand marked unsupported in the receipt and
  are the next round's repair (cite S182/S181 or narrow the cells).
- JudgeRepairR32 (lesson sha `470b6e3b…` at `ab8f4cfe`, R-R quoted): not-current 5/5 agree; support pointers 13
  agree, 1 disagree (S137: `main.c:260` does not tie `-k` to the kernel-OOM option, so "v1.2 removal" is unsupported on
  S137's own pages); unsupported clauses 23/23 agree; omitted clauses: S137 "returned on master in February 2026",
  "current master", "(S016 documents it…)"; S149 "the two files are different contracts"; S058 the combined "--reverse
  --topo-order lists ancestors first" (inference from two quotes). Correction (append-only, per the judge): those six
  clauses are unsupported under R-R and belong in the last column of §1; S137's first pointer moves there too. The
  judge's residual reading (a row id in a source cell does not name that row's pages) is stated in its receipt.


## Round-34 corrections (routed by `round-33-verifier-spotcheck.md` §8 items 5–8; append-only, L1 MoriR34 / MoriR34A2)

Drafted by round-34 attempt-1 wave-1 seats RepairLessonSec1, RepairWordEdits, RepairTimeLabels and RepairLocatorS117
(those seats died with the attempt-1 orchestrator; their drafts were never committed), integrated by the L1, and
judged item by item by non-author seats of round-34 wave A (`.ufo/waves/round-34/wa/`). Nothing above this heading is changed; each block below supersedes
only the cells or sentences it names. The fleet report `.ufo/reports/round-33/mori.md` is landed and is not edited; its
`:52-53` summary is corrected here.

### Item 5 — §1 last column vs `## Judges`

#### Correction to §1's last column

| row | corrected unsupported on every page the row names |
|---|---|
| S058 | A merge *requires* the explicit first-parent form `<commit>^1 <commit>`; a root commit *needs* `--root` (both lane procedure, undeclared); the combined `--reverse --topo-order lists ancestors first` conclusion is a two-quote inference and unsupported under R-R. See “Count and pointer correction” below. |
| S149 | On the two man pages the source cell gives as URLs: fork copy and floor; unprivileged-write floor; `totalpages/1000`; read-only `[0,2000]`; absence of the 3% root term in v7.2; the “supersedes S128” history; the “only there” / “documentation gap” assessments; and “the two files are different contracts” (lane assessment). The source cell also refers to S127 and S003 by id; wave-2 AttackRepairS149 found lane-root copies `base.c` and `oom_kill.c` state the scaling, read-only export and write floor, but they are other rows' pages, so under R-R they do not make S149 current. See “Count and pointer correction” below. |
| S137 | That a v1.9.0 binary prints that output (the page is commit `750a7c0d`, not v1.9.0); the `S137-main-750a.src:260` pointer is misfiled as support for “v1.2 removal” because it does not tie `-k` to `--kernel-oom`; “returned on master in February 2026”; “current master”; “(S016 documents it…)”; “delegation claims must name the build” (lane rule, undeclared). The `:260` pointer belongs in this unsupported column, not the supported column. See “Count and pointer correction” below. |

#### Count and pointer correction

The `## Judges` phrase “those six clauses” counts six defects, not six omitted clauses: five omitted teaches-cell clauses (S137 ×3, S149 ×1, S058 ×1) plus one misfiled S137 support pointer (`.ufo/waves/round-33/judge/JudgeRepairR32.md:76-77`). The `S137-main-750a.src:260` pointer is not support for the kernel-OOM option identity; the spotcheck describes the bare `case 'k'` and the separate option (`corpus/lessons/round-33-verifier-spotcheck.md:152-155`). This corrects the count and pointer placement stated at `corpus/lessons/round-33.md:209-210` without changing the five not-current verdicts (`corpus/lessons/round-33.md:56-64`).

### Item 6 — the six-cell summary at :79 (and report :52-53)

#### Correction to §3's six-row change summary (append-only)

The sentence at §3 line 79, “no other word changed”, is incorrect. All six rows gained `lane rule:` labels, but S062 and S064 also changed wording or attribution. S062 changed “no whitespace” to “no whitespace between JSON tokens” (as already noted at :85-88). S064 changed its teaches wording from “Resolve a selector once … retain the full object id …” to “Resolve a selector …; lane rule: do it once, retain the full object id …”, moving “once” and the procedure into the lane-rule clause; its scope likewise labels “not remote publication …” as a lane rule (:89-93). S041, S044, S051 and S069 only gained the label in the clauses shown at :82-84 and :94. The diff `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 7d382043 89791013 -- corpus/SOURCES.md` confirms the S062 and S064 edits (SOURCES.md lines 68 and 70). The fleet report's :52-53 summary is abbreviated: it records the label additions and unchanged status/recheck/used-by fields but does not enumerate these two text edits.

### Item 7 — receipt time labels

#### Receipt-time correction (append-only)

§8 item 7 correctly flags two inaccurate receipt labels. The header of `evidence/c1-controls.txt:1` says the C0 dispatch was `2026-10-23T02:38Z`; the closure records the actual dispatch as `2026-10-23T02:30:05.953Z` (`round-33-verifier-spotcheck.md` §2, lines 50-53). The receipt is carried by commit `fdf4371f`, whose committer time is `2026-10-23T02:39:02Z`; that commit time is not the dispatch time.

The header of `evidence/parity-freeze.txt:1` says `2026-10-23T02:3xZ`; the closure identifies the actual run as `2026-10-23T02:28:27Z` (`round-33-verifier-spotcheck.md` §1, lines 41-43). Commit `27969134` carries the original receipt at committer time `2026-10-23T02:28:27Z`, matching the closure's run time; the closure also records that the content landed at that committer time (`round-33-verifier-spotcheck.md` §2, lines 37-39). Commit time is corroboration, not a substitute for an execution timestamp. Preserve both receipt files unchanged; document the corrections here.

Round 34 carries the fix forward: every round-34 receipt's first line is `date -u` output taken when it was measured
or written (`.ufo/waves/round-34/evidence/*.txt`, `.ufo/waves/round-34/c0/*.md`, and the wave-A seat reports).

### Item 8 — CtlLocatorStale and the S117 preamble

#### Locator-address control (append-only)

`CtlLocatorStale` found that the round-33 counter does not validate the line address in a Gate locator. In its synthetic M1 control, `S180.src:21-22` was changed to `S180.src:999999`; the quote remained in the committed copy, and the counter still returned `C1=met` (exit 0). The counter checks quote presence in the whole copy, not within the located line range (`count-c1-a1.py:59,239-242`; `.ufo/waves/round-33/w2/CtlLocatorStale.md:55-82`). Thus a passing counter does not establish that a `file:L` locator addresses the quote. This is a counter residual demonstrated with synthetic data, not evidence that a live lane locator is false.

#### S117 recheck-scope clarification (append-only)

Clarification to the §1 preamble at lines 50-53: it must not be read to say that every page named by every repaired row was committed and checked. For S117, the committed `corpus/evidence/recheck-r33/` tree at `89791013` contains copies of nine of the row's ten pages, but no copy of the GitHub releases feed/API page. The release-local literals listed in the S117 table were checked against the committed copies; the cross-release clauses remain unsupported on those copies and unchecked against the missing feed (`round-33.md:59`). S117 remains `not current`.
