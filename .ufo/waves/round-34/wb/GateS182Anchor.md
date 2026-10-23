measured 2026-10-23T07:43:59Z

# Gate S182 anchor — round 34 wave B (seat MoriR34A3.GateS182Anchor)

Attacks: the attempt-2 change to existing row S182 in `corpus/SOURCES.md`. Independent verdict from bytes
first; audit of `wa/ReopenS182Anchor.md` at the end.

## Which cells changed

Committed ancestry (read-only `git log`/`diff` in lane, lane tip `fd2521351c6cef47384aef30afbe1e4db7e6912e`):

- `git show f10a320d:corpus/SOURCES.md` S182 row, cell 6 (anchor):
  `block/genhd.c:1353,1371-1374,1395,1403,1418-1425 (diskstats_show, diskstats_op, proc_create_seq); tag v7.2`;
  cell 11 (used-by): `corpus/knowledge/disk-write-rate-r33.md`.
- `git show 8d56809a:corpus/SOURCES.md` S182 row — the only S182-changing commit between f10a320d and tip
  (`git log f10a320d..fd2521351c -- corpus/SOURCES.md` lists only `8d56809`): cell 6 gained
  `; 485-486,512-518,620-623 (__add_disk parent, holders and slaves directories, device_add_disk)`; cell 11 became
  `corpus/knowledge/disk-write-rate-r33.md; tools/mori-disk-rate.py`. All other cells byte-identical (full-row
  `diff` of the three extractions).
- `git show fd2521351c:corpus/SOURCES.md` S182 row = 8d56809a row byte-for-byte (`diff` exit 0).
- Draft registry (first hunk of `/fast/scratch/hyaku/mori-r34/a3-L1/drafts/attempt2-tracked.diff` for
  `corpus/SOURCES.md`, `@@ -185,7 +185,7 @@`): the `-` line is byte-identical to the committed fd2521 row
  (`cmp` exit 0); the `+` line differs in **cell 11 only**: `corpus/knowledge/disk-write-rate-r33.md`
  (single path). The anchor cell is untouched by the draft — the anchor change is already committed at 8d56809a.

So: round-level old→new across f10a320d→draft touches **two** cells (anchor at commit 8d56809a; used-by widened at
8d56809a then restored to single-path in the uncommitted draft). The attempt-2 diff itself changes only used-by.

## Live re-open of the source

- `date -u` 2026-10-23T07:42:21Z; `curl -fsSL --max-time 60
  https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c` → 1588 lines, sha256
  `8c2faa1564190e9a8e4cf3ebac5e2561b96818e38560cdcf44fea1761c8d39a5`.
- `sha256sum corpus/evidence/sources-r33/S182.src` → identical sha256, identical line count. Live file and
  stored copy are the same bytes.

## New anchor lines vs the parenthesis

In the live file (`/tmp` copy, line numbers checked with `sed -n`):
- `__add_disk parent`: `__add_disk` opens at line 427 (`static int __add_disk(struct device *parent, ...)`);
  line 485 `ddev->parent = parent;` and 486 `ddev->groups = groups;` sit inside it. Holds.
- `holders and slaves directories`: 512-513 `disk->part0->bd_holder_dir = kobject_create_and_add("holders",
  &ddev->kobj);`, 517-518 `disk->slave_dir = kobject_create_and_add("slaves", &ddev->kobj);`; the span 512-518
  covers both creates plus the intervening `-ENOMEM`/`goto out_del_block_link` error path (514-516). Holds.
- `device_add_disk`: 620-623 `int __must_check device_add_disk(struct device *parent, struct gendisk *disk,
  const struct attribute_group **groups) { return add_disk_fwnode(parent, disk, groups, NULL); }` — the
  signature with `parent` first, matching S194's "(the parent argument per S182's device_add_disk signature)".
  Holds.
- Pre-existing part still accurate: 1353 `static int diskstats_show(...)`; 1371-1372 the zero-sector partition
  skip; 1374 `inflight = bdev_count_inflight(hd)`; 1395 `jiffies_to_msecs(stat.io_ticks)`; 1403
  `stat.sectors[STAT_DISCARD]`; 1416-1421 `diskstats_op`; 1425 `proc_create_seq("diskstats", ...)`.

## Lesson old→new byte check (`drafts/corpus_lessons_round-34.md:35-41`)

- Anchor: old literal `block/genhd.c:1353,1371-1374,1395,1403,1418-1425 (diskstats_show, diskstats_op,
  proc_create_seq); tag v7.2` = byte-exact f10a320d cell 6. New literal `… ; 485-486,512-518,620-623
  (__add_disk parent, holders and slaves directories, device_add_disk); tag v7.2` = byte-exact tail of the new
  cell; the `…` stands for the unchanged prefix, and the lesson's `… ;` writes one cosmetic space the cell does
  not have (cell has `); 485`). Elision convention, content exact.
- Used-by: `corpus/knowledge/disk-write-rate-r33.md` → `...; tools/mori-disk-rate.py` "landed at 8d56809a"
  matches the committed diff exactly; "restored to the single path" matches the draft `+` cell; "RevAppendOnly
  missed it" is the seat's annotation, consistent with the cell having been widened without the appendix-style
  marker. "No status or recheck cell of an existing row changed" — verified: cells 8-10 identical in all three
  revisions and the draft.

## Audit of .ufo/waves/round-34/wa/ReopenS182Anchor.md

- "The one changed cell of row S182 ... anchor gained `485-486,...device_add_disk` between f10a320d and
  8d56809a" — **agree** for the anchor half (`git diff f10a320d 8d56809a` S182 hunk shows exactly that cell-6
  change), but the seat's premise "the one changed cell" is incomplete: the same commit also changed cell 11
  (used-by → two paths). Within the seat's stated scope (anchor only) the claim it makes is accurate; flagged
  as a scope note, not an error.
- OLD/NEW anchor literals (lines 12-13 of that report) — **agree**: byte-exact vs my cell extractions.
- "All other S182 cells unchanged in this diff" (line 14) — **disagree**: `git diff f10a320d 8d56809a --
  corpus/SOURCES.md` shows cell 11 also changed (`corpus/knowledge/disk-write-rate-r33.md` →
  `corpus/knowledge/disk-write-rate-r33.md; tools/mori-disk-rate.py`). One literal error.
- Live fetch: two pulls 1588 lines, sha256 `8c2faa15...39a5`, identical to S182.src — **agree**: my pull at
  07:42:21Z produced the same hash and the same `diff -q`-equivalent result.
- Line claims (report lines 29-34): 427 `__add_disk` signature, 485-486 parent/groups, 512-513 holders,
  518 slaves, 620-623 device_add_disk — **agree** on every line, verified in the live bytes (minor: the report
  attributes line 518 to the slaves create; `sed -n` shows the create at 517 with `&ddev->kobj);` on 518 —
  the two-line statement spans 517-518, so the range claim still holds).
- "512-518 also covers the -ENOMEM error paths 514-517" — **agree** (514-516 are the holder-dir check; the
  slaves create begins 517).
- Pre-existing anchor sanity list (line 38) — **agree** on all cited lines.
- S194 cross-check (line 35): S194's text relies on `parent` first in device_add_disk — **agree**; signature
  confirms parent is parameter 1.
- Residual-risk lines — **agree** (no counter claims made; honest scope note).

AUDIT: agree 8 / disagree 1

## Verdicts

VERDICT: supported — anchor cell (new lines 485-486, 512-518, 620-623 hold what the parenthesis claims,
verified live 2026-10-23T07:42:21Z, sha256 8c2faa15...39a5 = stored S182.src)
VERDICT: supported — used-by cell (draft restores the single path `corpus/knowledge/disk-write-rate-r33.md`,
exactly reversing the two-path cell committed at 8d56809a; only cell 11 changes in the attempt-2 diff)
VERDICT: supported — old→new log (lesson lines 36-40 reproduce both cell texts byte-accurately modulo one
elision ellipsis; the one cosmetic space in `… ;` does not alter a byte of the cell)

## Residual risk / gaps

- The wa report's "all other S182 cells unchanged" error is a scope artifact (it audited the anchor only);
  the used-by widening it missed is exactly what the draft now reverts — consistent, not contradicting.
- Anchor span 512-518 includes the error path between the two kobject creates; the parenthesis's label covers
  it adequately.
- v7.2 tag drift: single live pull here; identical to the r33-stored copy and to the wa seat's two pulls, so
  no drift observed across ~2 h.
- Tooling: nothing installed or updated (curl, git, sha256sum, sed, date already present); pacman untouched.
- Lane writes: none. Scratch reads only under `/tmp` and the named drafts dir.
