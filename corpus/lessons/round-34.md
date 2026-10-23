author: mori-shokunin L1 MoriR34A3 (round 34, attempt 3). Attempt 1 (L1 MoriR34) died with the orchestrator at
05:25:25Z; attempt 2 (L1 MoriR34A2) died with it (omp SIGSEGV) at 06:19:06Z (`/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:847,867`,
`.ufo/waves/round-34/wb/ScoutAccounting.md`). This lesson is written in attempt 3. Every attempt-1/2 file that was not
committed is untrusted: attempt 3 cites it only where a wave-B seat audited it (each audit is named), and moved the
rest out of the lane (`/fast/scratch/hyaku/mori-r34/a3-L1/removed-untrusted/`, below).

# mori round 34 — lesson

## Gate (rows opened 2026-10-23 in round 34)

Eight sources admitted, all tier A, status `mined`. Attempt 2 fetched them at 05:32:35Z and landed the copies at
`8d56809a`. Attempt 3 re-opened every URL live: the L1 at 06:48:19-21Z (`.ufo/waves/round-34/evidence/sources-refetch-a3.txt`,
sha256 equal to the committed copy for all eight and for S182), and one fresh wave-B reviewer per row at 07:40-07:42Z
(`.ufo/waves/round-34/wb/GateS191.md` … `GateS198.md`), who also re-located every quote below and judged the registry
row cell by cell. The L1 re-checked all 20 quotes in the committed copies (whitespace runs collapsed): each contiguous at
its locator, word count as stated, 3–25 words, no `"` or `|`.

| id | url | accessed | sha256 | quotes | decision |
|---|---|---|---|---|---|
| S191 | https://raw.githubusercontent.com/torvalds/linux/v7.2/block/partitions/core.c | 2026-10-23T05:32:35Z (L1); 2026-10-23T05:38:41Z (ReopenS191) | `add355b5a35d09f77daa435e6f281ab6a3ba801d1b19980c8d5e471f05ed5d17` | `S191.src:208` (5 words): "static DEVICE_ATTR(partition, 0444, part_partition_show, NULL);"; `S191.src:221-222` (7 words): "static struct attribute *part_attrs[] = { &dev_attr_partition.attr,"; `S191.src:266-268` (6 words): "const struct device_type part_type = {" | admit, A, mined |
| S192 | https://raw.githubusercontent.com/torvalds/linux/v7.2/block/holder.c | 2026-10-23T05:32:35Z (L1); 2026-10-23T05:38:46Z (ReopenS192) | `1e41cc5cde74b89d10269351383426aef2d22dd7018fbc89ad63952562153a91` | `S192.src:41` (7 words): "This functions creates the following sysfs symlinks."; `S192.src:46` (7 words): "For example, if /dev/dm-0 maps to /dev/sda"; `S192.src:49-50` (3 words): "/sys/block/dm-0/slaves/sda --> /sys/block/sda"; `S192.src:147` (7 words): "if (!WARN_ON_ONCE(holder == NULL) && !--holder->refcnt) {" | admit, A, mined |
| S193 | https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/base/core.c | 2026-10-23T05:32:35Z (L1); 2026-10-23T05:38:54Z (ReopenS193) | `fa223c8f9f1bb40ca52c73f156439d311065e9be04efa2c6cf57039940e1c9fa` | `S193.src:3508-3509` (9 words): "if (dev->parent && device_is_not_partition(dev)) { error = sysfs_create_link(&dev->kobj, &dev->parent->kobj,"; `S193.src:3542` (4 words): "if (dev->parent && device_is_not_partition(dev))" | admit, A, mined |
| S194 | https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/block/zram/zram_drv.c | 2026-10-23T05:32:35Z (L1); 2026-10-23T05:38:39Z (ReopenS194) | `d5d4933a2aed57d667edbb8c8904be3d9569a61cc5a428a2cd8b044aeab00f25` | `S194.src:3094` (5 words): "ret = device_add_disk(NULL, zram->disk, zram_disk_groups);" | admit, A, mined |
| S195 | https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/common.c | 2026-10-23T05:32:35Z (L1); 2026-10-23T05:38:42Z (ReopenS195) | `4aa91c92577ac27970c55b3778e0718a575a17cf86b40d3bbb9ed8d4412eac21` | `S195.src:204` (9 words): "The device is assumed to be virtual if no"; `S195.src:205` (3 words): "/sys/block/<device>/device link exists."; `S195.src:208` (12 words): "TRUE if @name is a device, and FALSE if it's a partition." | admit, A, mined |
| S196 | https://raw.githubusercontent.com/util-linux/util-linux/v2.42.4/lib/sysfs.c | 2026-10-23T05:32:35Z (L1); 2026-10-23T05:40:20Z (ReopenS196) | `c19c802cc976c6be99c86db1e63ce4261ad7c9d4e5108cfa817526440cf9cbbf` | `S196.src:570` (7 words): "parser) have the /sys/.../partition file. The partitions"; `S196.src:571` (7 words): "mapped by DM don't have such file,"; `S196.src:241` (9 words): "Cannot use /partition file, not supported on old sysfs"; `S196.src:305` (9 words): "Returns slave name if there is only one slave" | admit, A, mined |
| S197 | https://raw.githubusercontent.com/torvalds/linux/v4.18/block/genhd.c | 2026-10-23T05:32:35Z (L1); 2026-10-23T05:38:43Z (ReopenS197) | `96b5638180eb70886195b46722681623301c328763b47c674a6543b27c3e748b` | `S197.src:1338-1339` (5 words): "MAJOR(part_devt(hd)), MINOR(part_devt(hd)), disk_name(gp, hd->partno, buf),"; `S197.src:1348-1350` (5 words): "inflight[0], jiffies_to_msecs(part_stat_read(hd, io_ticks)), jiffies_to_msecs(part_stat_read(hd, time_in_queue))" | admit, A, mined |
| S198 | https://raw.githubusercontent.com/torvalds/linux/v4.19/block/genhd.c | 2026-10-23T05:32:35Z (L1); 2026-10-23T05:38:48Z (ReopenS198) | `4c55aeba02bfaecee8ef5a20514f834f2aa34a338f51a66a83bcc40d5a7588f1` | `S198.src:1354-1357` (9 words): "part_stat_read(hd, ios[STAT_DISCARD]), part_stat_read(hd, merges[STAT_DISCARD]), part_stat_read(hd, sectors[STAT_DISCARD]), (unsigned int)part_stat_read_msecs(hd, STAT_DISCARD)" | admit, A, mined |

Rejected at the gate this round (real rejects, with reasons):
- **S193's first teaches cell** ("The `device` symlink is created, and removed, only when the device has a parent and is
  not a partition", landed at `8d56809a`): rejected by GateS193 — `device_move_class_links` (`S193.src:4647-4658`, called
  by `device_move` at `:4667`, `:4706`) removes and creates the link on a reparent with no partition check
  (`S193.src:4653-4657`). The cell was rewritten (old→new below) and re-judged by ReGateS193 (residual call).
- **The attempt-1 tool draft** (dead seat MoriR34.ExecDiskRateTool, never committed): rejected as the C1 deliverable;
  the frozen counter scored it `live=fed-no-interval C1=unmet` (`.ufo/waves/round-34/evidence/c1-tool-provenance.txt`,
  committed at `ba525e1a`). Only the L1-changed version landed.
- **Seat-proposed quotes** (attempt 2) for S195 (`:204-205`) and S196 (`:569-570`, `:570-571`): not contiguous, each spans a
  ` * ` comment prefix; replaced by single-line quotes (GateS195 re-verified the S195 reject). S192 `:148-149` (2 words)
  under 3 words; S193 `:3542-3543` and S197 `:1336-1337` contain `"`.

Row changes logged old→new:
- S182 (existing row): at `8d56809a` the anchor gained `; 485-486,512-518,620-623 (__add_disk parent, holders and slaves
  directories, device_add_disk)` and used-by changed `corpus/knowledge/disk-write-rate-r33.md` →
  `corpus/knowledge/disk-write-rate-r33.md; tools/mori-disk-rate.py`. The used-by cell is restored to
  `corpus/knowledge/disk-write-rate-r33.md` at `ff334073` (census E11, M6). GateS182Anchor: anchor, used-by and this log
  supported. No status or recheck cell of an existing row changed.
- S191–S198 added at `8d56809a` (`mined`, opened 2026-10-23, `on-release`). used-by cells at `8d56809a` were
  `tools/mori-disk-rate.py; SKILL.md Round34` (S191–S193), `SKILL.md Round34` (S194–S196) and
  `corpus/knowledge/disk-write-rate-r33.md (Round-34 row 8 correction)` (S197–S198); at `ff334073` they are the single
  paths `tools/mori-disk-rate.py`, `SKILL.md` and `corpus/knowledge/disk-write-rate-r33.md`.
- S193 anchor `drivers/base/core.c:3508-3510,3542-3543; tag v7.2` → `drivers/base/core.c:3508-3510,3542-3543,4653-4657;
  tag v7.2`; teaches "The `device` symlink is created, and removed, only when the device has a parent and is not a
  partition." → "On add and on delete, the `device` symlink is created and removed only when the device has a parent and
  is not a partition; on a reparent (`device_move`) the link follows the new parent with no partition check." (lane-rule
  clause unchanged).

Census: `corpus/SOURCES.md` rows 190 → 198 (`grep -c '^| S[0-9]' corpus/SOURCES.md`). Start: `evidence/census-start.txt`
(attempt 1, `mori ok`, exit 0) and `evidence/census-a3-start.txt` (attempt 3, working tree, exit 0). The registry
committed at `8d56809a` fails the census with nine `E11` lines (ExecCensusE11); `ff334073` fixes it. End:
`evidence/census-a3-end.txt`.

## Claims and verdicts (L1 view; the closure rules)

- **C1 coverage — `tools/mori-disk-rate.py`, judged by P-C1-A1: not verified (honest stop under addendum §9).** The
  frozen counter reports `C1=met` at the tip (L1, `evidence/c1-tip-a3.txt`, 06:47:48Z, fresh seed) and in four clone
  runs (ExecCloneRerun: two fresh seeds and `--seed 1` at `fd252135`, one fresh at `5216d78d`). But a program that skips
  the claimed operation also meets it: probe `ef936fb4` (built after data by attempt-2 critic CritPostDataShortcut)
  reads the real `/proc/diskstats` once and reports every rate 0, reads twice only when the file is a FIFO, and classes
  devices from name patterns without opening `partition`, `slaves` or `device`. The L1 re-scored it at 06:48:06Z
  (`evidence/ctl-postdata-shortcut/rescore-a3.txt`: `C1=met`, probe bytes sha256 `cd5389b9…` = the committed copy) and
  critic CritShortcutRescore re-scored it twice more and read its code (`wb/CritShortcutRescore.md`). CritQ99Gap built two
  more skip programs that meet it (`wb/CritQ99Gap.md`). The counter, rules and target are not amended.
- **C2 calibration (exploratory) — QUALITY 98: `unprovable-but-better`** by named non-author reviewer ReviewC2Judge3
  (`.ufo/waves/round-34/wb/ReviewC2Judge3.md`, reached before it opened the attempt-2 judge): 98's check (a) fails round
  33's contract at `fdf4371f` and passes round 34's at `b9fb029e`; it forced a pre-data re-design this round (the C0
  controls that met the first counter, Amendment A1); it goes beyond QUALITY 95-97 and §9 by moving the shortcut test
  before data with discharge rules and an ancestry check. Against it, on record: it does not answer §8 item 1's second
  clause (verdict cells naming a reader action); its own table discharges the echo shape by a guard trip, which its
  discharge sentence forbids (D2); "maps each shape" overstates (no row for a rule changed after data; D1); the contract
  says three controls met P-C1 where four runs met (D4); and after data the shortcut `ef936fb4` met the counter although
  98's battery passed (M2), which bounds 98 to pre-data discipline. The axis score does not change.

## Mistakes

- **M1 — a no-decision glossary met round 33's frozen counter because the pre-data controls had no no-decision case.**
  Class: pre-data control gap (counter discrimination). Evidence: `corpus/lessons/round-33-verifier-spotcheck.md` §3.2
  item 4. Captured-by: none before round 34. Fix: QUALITY 98. Shown able to fail: 98's check (a) fails on round 33's
  control list (`.ufo/waves/round-33/contract.md` at `fdf4371f`); MutQ98R34 kills a round-34 contract with the no-decision
  row deleted (`wb/MutQ98R34.md`, variant 1).
- **M2 — round 34's own pre-data battery (16 controls, 98-shaped) missed a label-keyed, harness-keyed shortcut, which
  met P-C1-A1 after data.** Class: counter discrimination (shortcut not built before data). Evidence:
  `evidence/ctl-postdata-shortcut/receipt.txt`, `rescore-a3.txt`; `wb/CritShortcutRescore.md`;
  `.ufo/waves/round-34/count-c1-a1.py:277-278` (live bound upper-only, so rate 0 passes) and `:145-166` (each class drawn
  from its own name family). Captured-by: QUALITY 98 maps the label-keyed shape, but C-labelkey keyed only on the 12
  fixed-seed input bytes, so 98 passed the table: none caught it. Fix: QUALITY 99. Shown able to fail: 99's (a) fails on
  round 34's table at `b9fb029e` (no harness-keyed control; label key on input bytes only) and its (c) fails on the
  upper-only bound; the first 99 draft let both through (MutQ99 variants 3 and 4 survived) and was revised before landing.
- **M3 — the frozen counter is blind to rule order and to rule parts its generator never draws, and that was never
  measured before data.** Class: counter coverage. Evidence: ExecM3Mutants (`wb/ExecM3Mutants.md`): mutants swapping R3
  partition↔stacked, R3 stacked↔disk and R5 bad-line↔absent survive (`C1=met` at `--seed 1` and a fresh seed), each with
  a direct witness on which mutant and tool outputs differ; accepting bare hex or a two-token line also survives, while
  accepting `0x` hex or a 10-13-token line is killed by the random arm (so attempt 2's "short-line handling and bare-hex"
  wording was too broad: only the spellings the generator cannot draw survive). AuditM3Reports re-derived the measured-time
  and mountinfo-path live mutants (both `C1=met`) and confirmed from the counter source that the generator never draws
  overlapping class markers, symlinked entries or a partition with slaves (`count-c1-a1.py:152-178`). CritQ99Gap adds two
  rule-part skips that meet the counter (R4 sysfs-only devices; decimal validation replaced by the generator's corruption
  characters). Captured-by: none. Fix: the next counter freezes one witness per ordered rule pair and per generator
  vocabulary gap; shown able to fail by the surviving mutants above.
- **M4 — two L1-integrated round-33 corrections carry wrong details.** Item 7 cites "spot-check §2, lines 37-39"; those
  lines are in §1 (ReJudgeLesson7, `not repaired` for that one detail). Item 8 says the `recheck-r33/` tree holds nine of
  S117's ten page copies; it holds eight, and the ninth (the tags JSON) is `corpus/evidence/recheck-r32/S117.src`
  (ReJudgeLesson8, `repaired — with one wrong detail`).
  Class: integration without re-count. Captured-by: the per-item judges. Fix: the corrections below.
- **M5 — the provenance receipt overstates, and attempt 2's correction of it overstated again.**
  `evidence/c1-tool-provenance.txt` (committed at `ba525e1a`) says the draft seat was "not given" the counter; critic
  CritM5Audit found the counter byte-present in that seat's clone (`/fast/scratch/hyaku/mori-r34/ExecDiskRateTool/clone`,
  counter sha256 `c14c3494…` = the lane's; draft sha256 `583cc423…` = the receipt's), though actual consultation is not
  shown. The L1's change (draft → `ba525e1a`) removes the FIFO branch and changes nothing in the regular-file
  read/sleep/read path: it is a conformance fix to the counter's reader-close protocol, not an arithmetic fix. Attempt 2
  argued the tool "is no copy" because it diverges from the oracle on a duplicate-name sample; CritM5Audit built an
  explicitly oracle-derived program that diverges the same way, so divergence does not prove independent authorship:
  residual (a) of the contract stays a residual. The docstring of `read_live_samples` (`tools/mori-disk-rate.py:178-180`)
  says the divisor is the time between the readings; it is the nominal interval, and all ten fresh read-start gaps were
  longer (+0.12% to +0.19% at 200 ms, +0.02% to +0.03% at 1000 ms; `wb/CritM5Audit.md`). Attempt 2's "+0.07% to +6.4%
  under load" range was not re-established and is not carried. Class: provenance wording. Captured-by: none. Fix: this
  entry; the tool is the judged object and is not edited. Shown able to fail: CritM5Audit's derived-oracle witness.
- **M6 — multi-path used-by cells failed the census, and the failing registry was committed.** The census reads a
  used-by cell as a comma list of paths and checks each with `[ -e ]` (`scripts/sources-census.sh:562-567`); attempt 1's
  integration wrote `a; b` and annotated cells, and attempt 2 committed them at `8d56809a`, where the census prints nine
  `E11` lines and exits 1 (ExecCensusE11 reproduced all nine from the committed blob, and E11 on a `;` cell and an
  annotated cell in a sandbox). Attempt 2 fixed the working tree but never committed the fix, and its
  `census-end.txt` said "committed". Class: registry format; claim of a commit not made. Captured-by:
  `scripts/sources-census.sh` E11. Fix: single paths, committed at `ff334073`; end census over committed bytes. Shown able
  to fail: the census on `8d56809a`'s registry.
- **M7 — attempt 2 produced its integration after its last lane commit and left it uncommitted for about 40 minutes,
  so the orchestrator's death made it untrusted.** Class: integration durability. Evidence: attempt 2's last lane commit
  `fd252135` is 02:37:39-03:00 (05:37:39Z); its seat reports, lesson, SCORECARD/LOG/QUALITY/README edits and the census
  fix carry later mtimes (up to 06:17Z) and were uncommitted at 06:19:06Z (`wb/ScribeMistakeM7.md`; snapshot hashes in
  `/fast/scratch/hyaku/mori-r34/a3-L1/drafts/`). Captured-by: none (attempt 3's re-derivation rule). Fix: land each
  verified integration as soon as it is judged, and check before filing that the final lane commit is later than every
  wave report's mtime and its tree holds them. Shown able to fail: `wa/ReopenS191.md` (05:38:58Z) is newer than
  `fd252135`. Attempt 3 landed the SOURCES fix at `ff334073` as soon as eight gate seats had judged it.

## Corrections (append-only) to `corpus/lessons/round-33.md` § Round-34 corrections

- Item 7: read "(`round-33-verifier-spotcheck.md` §2, lines 37-39)" as "§1, lines 37-39" (ReJudgeLesson7).
- Item 8, S117 clarification: read "contains copies of nine of the row's ten pages" as "contains copies of eight of the
  row's ten pages; a ninth, the tags JSON, is `corpus/evidence/recheck-r32/S117.src`" (ReJudgeLesson8).
- The tool docstring's R2 → S180 and R6 → S187 attributions are unsupported: S180 describes the sysfs stat file, not a
  `/proc/diskstats` line, and S187 states no byte unit; S187 carries R2 (`S187.src:6-7,12,19,26-27`) and S186 carries R6's
  512-byte sector (`S186.src:25-28`). The same R6 label sits in the code comment at `tools/mori-disk-rate.py:86`
  (AuditToolDocstring). The labels copy the frozen contract's (`contract.md:36,46`). The tool is the judged object and is
  not edited.
- QUALITY 98's last sentence cites "round-34 Mistakes M1" for the rule-order gap; it is M3 (noted in QUALITY 99's section).

## Round-33 routed defects (closure §8) — outcome (attempt-3 judges; each also audited the attempt-2 judge)

| item | landed at | attempt-3 judge | verdict |
|---|---|---|---|
| 1 counter discrimination | QUALITY 98 (C2), 99 | ReviewC2Judge3, MutQ98R34, ReviewQ99, MutQ99, CritQ99Revised | first clause answered (98 `unprovable-but-better`; 99 admitted with fixes, applied, not re-judged); second clause (reader-action check) open |
| 2 row 3 | 3r at `8d56809a`; 3r2 at `5c3e2dde` | ReJudgeRow3r: 3r **unsupported** (four facts not stated by the cited lines); JudgeRow3r2 (residual) | 3r2 supported |
| 2 rows 6, 7, 13 | 6r, 7r, 13r at `8d56809a` | ReJudgeRow6r, ReJudgeRow7r, ReJudgeRow13r | 3/3 supported |
| 3 row 8 "4.18" | Row 8 correction at `8d56809a` | ReJudgeRow8 | 8/8 sentences supported; its Gate pointer resolves once this lesson is committed |
| 4 SKILL :820 | SKILL Round34 correction | ReJudgeSkillCorr | supported (also: append-only, rules :816-818 hold) |
| 5 §1 vs Judges | round-33 lesson Item 5 | ReJudgeLesson5 | repaired |
| 6 word edits | round-33 lesson Item 6 | ReJudgeLesson6 | repaired |
| 7 time labels | round-33 lesson Item 7 | ReJudgeLesson7 | not repaired as landed (one wrong section label), corrected above |
| 8 CtlLocatorStale, S117 | round-33 lesson Item 8 | ReJudgeLesson8 | repaired with one wrong count, corrected above |

Disagreement on record: ReJudgeSkillCorr holds SKILL.md:817 under 3r, while ReJudgeRow3r judges 3r unsupported under the
letter of R-J; ReJudgeRow3r also says SKILL.md:817 holds in substance. The L1 follows the stricter judge and lands 3r2.

## Judges

Wave B (attempt 3; validated 41-seat v1 wave `wb-spec.json`, dispatched in four chunks, `wb-dispatch-log.txt`) and one
residual call (3 seats, `wb-residual-dispatch.json`). Every seat reached its verdict from the bytes before auditing the
attempt-2 report named in its item; the audited attempt-2 reports are committed under `.ufo/waves/round-34/wa/` as audit
objects, not evidence.

| seat | object | verdict | audit of attempt-2 report |
|---|---|---|---|
| GateS191–S198 | Gate rows and registry rows S191–S198 | 7 admit; S193 reject (teaches cell) | agree 15/0, 11/3, 13/4, 16/1, 11/0, 14/2, 9/1, 10/0 |
| GateS182Anchor | S182 anchor, used-by, old→new log | supported ×3 | 8/1 |
| ReGateS193 (residual) | revised S193 row | admit | — |
| ReJudgeRow3r / 6r / 7r / 13r | entry rows | unsupported / supported / supported / supported | 8/7, 12/0, 12/1, 14/0 |
| JudgeRow3r2 (residual) | row 3r2 | supported | — |
| ReJudgeRow8 | Row 8 correction | 8/8 sentences supported | 10/0 |
| ReJudgeSkillCorr | SKILL Round34 correction | supported (3 items) | 20/0 |
| ReJudgeSkillR34 | four `Round34 rule:` lines | 4/4 supported; :834's "already counted (S192)" is observed, not sourced | 24/1 |
| ReJudgeLesson5 / 6 / 7 / 8 | round-33 lesson Items 5–8 | repaired / repaired / one wrong label / one wrong count | 10/0, 15/0, 12/1, 10/0 |
| CritShortcutRescore | probe `ef936fb4` | meets P-C1-A1 (2 fresh runs); real tool also meets | 16/14 |
| CritQ99Gap | QUALITY 99 draft | gap found (2 more skip programs meet P-C1-A1) | — |
| ReviewC2Judge3 | QUALITY 98 (C2) | unprovable-but-better | 15/2 (ReviewC2Judge), 11/0 (MutQ98) |
| MutQ98R34 | 98's check on round 34's contract | variants 1, 2, 4 killed; 3 (reasoned inapplicability) survived | — |
| ReviewQ99 / MutQ99 / CritQ99Revised | QUALITY 99 | admit with fixes / variants 3, 4 survived the first draft / revised check rejects both, fixes listed | — |
| ExecCloneRerun | C1 at `fd252135`, `5216d78d` | `C1=met` ×4 | — |
| ExecM3Mutants / AuditM3Reports | M3 | 5 survivors with witnesses, 3 killed / 4 claims agree | — (MutLiveArm, CritGeneratorCoverage, LabFixturePartStacked agreed) |
| CritM5Audit | M5 | 4 claims agree, 2 disagree (see M5) | 11/5 (CritResidualA), 7/7 (LabIntervalError) |
| ExecCensusE11 | M6 | reproduced; registry at `8d56809a` fails (9 E11) | — |
| AuditLessonDraft / AuditScorecardLog | attempt-2 lesson, SCORECARD and LOG drafts | 12 untracked citations, 2 dangling paths, one bad sum | — (drafts rewritten in attempt 3) |
| AuditFrontierNote / ExecLatencyRemeasure / ExecStackedRemeasure | FR6 frontier note | 8/9 sentences agree; "twice" is three times; "fitting intervals read zero" unsupported | 16/1 (ExecLatencyBudget), 18/2 (LabStackedHost) |
| AuditToolDocstring | docstring attribution correction | both attributions unsupported, as the correction says | 21/0 (RevToolDocstring) |
| ConnectorSiblings | sibling overlap | 10 overlaps (control method: chousa r29/r31, kake r39; attempt-death quarantine: nine lanes) | — |
| ScoutAccounting | seat accounting | complete | — |
| ScribeMistakeM7 | M7 | supported | — |
| SentinelPrivacy | bytes to commit | 5 findings: four pids in `wa/ExecRerunLane.md` (not committed) and one OMP setting value at `LOG.md:1801` (committed in an earlier round; operator decision) | — |

Disagreements the L1 did not resolve this round: SKILL.md:834 cites S192 for "maps onto devices already counted",
which S192 does not state (ReJudgeSkillR34); the entry's round-34 revision header (`8d56809a`) names `.ufo/waves/round-34/w1/`,
which was never committed and was moved out of the lane in attempt 3.

## Untrusted attempt-1/2 files (moved out of the lane, not cited)

To `/fast/scratch/hyaku/mori-r34/a3-L1/removed-untrusted/`: attempt 1's `w1/` (30 seat reports) and `wave1-*.json`;
attempt 2's `evidence/c1-after.txt`, `evidence/census-end.txt`, `wa-run.err` and the 20 wave-A reports no wave-B seat
audited (including `ExecRerunLane.md`, which holds pids). Attempt 2's working-tree edits were snapshotted at
`/fast/scratch/hyaku/mori-r34/a3-L1/drafts/` and either re-derived (SOURCES used-by cells, QUALITY 99, frontier note) or
rewritten (this lesson, SCORECARD, LOG).
