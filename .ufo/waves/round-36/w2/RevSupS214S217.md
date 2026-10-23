# RevSupS214S217 — re-open S214–S217 (rows + copies)

measured 2026-10-23; non-author review (w2). Commit pinned: `bf0df77fee4b6ef54a90aea09335c7617f125151`
(assignment tip). Mid-review the L1 landed settlement commits `9ca8f2e` and `6827d6e` (HEAD at last check
`6827d6e322e87a0b5857bdd25ceb45970732fcd1`); `git diff bf0df77 6827d6e -- corpus/SOURCES.md` changes only row
S205's `used-by`, so every S214–S217 cell and copy measured below is identical at both commits. Nothing in this
item touches or infers a C1 freshness verdict (C1 lands `unprovable` per the contract; my findings do not change that).

Item attacked: the round-36 discharge rows S214→S183 (`include/linux/part_stat.h`), S215→S184 (`block/blk-core.c`),
S216→S185 (`block/blk-mq.c`), S217→S186 (`include/linux/blk_types.h`), all tag-pinned v7.2, and their committed
copies `corpus/evidence/sources-r36/S21{4,5,6,7}.src`.

Axes: (1) copy fidelity (sha256 vs live fetch), (2) anchor/quote fidelity (contiguity at anchor, ≤25 words,
word-count labels), (3) rule-2 form (append-only, `supersedes S0NN —` form, gate `round_changed`), (4) registry
cell truthfulness (status/used-by citation pairing).

## 1. Copies — sha256-equal (PASS)

Fetched all four pinned files fresh (scratch `/fast/scratch/hyaku/mori-r36/RevSupS214S217-23/`):

```
curl -sSL https://raw.githubusercontent.com/torvalds/linux/v7.2/{include/linux/part_stat.h,block/blk-core.c,block/blk-mq.c,include/linux/blk_types.h}
sha256sum →
2e22ee58e88396108d9962b122082d899fd517e3c67195e9dee580db63d55a9a  include_linux_part_stat.h
528501312dbd8da7649051006f12203fbef03f5180c4408ccc20856262c77827  block_blk-core.c
7483f1738ad1a00372f5fca0e553023ff4a683e4e2a73c01b3da31302bba8c11  block_blk-mq.c
adff86f6d9433c496dc5ddf32d0e353a24969af7ed90191dffc562f1998b2e6e  include_linux_blk_types.h
```

- `diff` fetched vs `corpus/evidence/sources-r36/S214.src–S217.src`: **S214-IDENTICAL … S217-IDENTICAL** (byte-equal, hence sha256-equal).
- Also byte-identical to the round-33 copies they restate: `cmp sources-r33/S18{3,4,5,6}.src sources-r36/S21{4,5,6,7}.src` → all IDENTICAL; no older/decoy copy exists for S214–S217 (only `sources-r36/` holds these ids).
- Round-33 Gate recorded digests (`corpus/lessons/round-33.md:18-21`) match these same four hashes.
- Landed drift receipt agrees (`evidence/drift-live-r36.txt:214-217`: `S214 fresh … S217 fresh`); my independent hash makes that classification correct, not just consistent.

## 2. Anchors and teaches — contiguous at anchor (PASS)

Every anchor window was read from the fetched v7.2 bytes and supports the teaches claim, with the quoted code contiguous in the window:

| row | anchor | verified in fetched bytes |
|---|---|---|
| S214 (`:10,60-63`) | line 10 `unsigned long sectors[NR_STAT_GROUPS];`; lines 60-63 `#define part_stat_add… do { \ __part_stat_add((part), field, addnd); \ if (bdev_is_partition(part)) \ __part_stat_add(bdev_whole(part), field, addnd);` | the add is applied a second time to `bdev_whole(part)` exactly as taught; sectors array is `unsigned long` |
| S215 (`:1067-1068,1100,1108-1110`) | 1067-1068 `(end \|\| bdev_count_inflight(part))) __part_stat_add(part, io_ticks, now - stamp);`; 1100 `void bdev_end_io_acct(…`; 1108-1110 `update_io_ticks(bdev, now, true); part_stat_inc(bdev, ios[sgrp]); part_stat_add(bdev, sectors[sgrp], sectors);` | completed sectors added with `part_stat_add`; io_ticks gets elapsed time only when ending or in flight |
| S216 (`:856,858,862`) | 856 `static void blk_account_io_completion(…`; 858 `if (req->rq_flags & RQF_IO_STAT) {`; 862 `part_stat_add(req->part, sectors[sgrp], bytes >> 9);` | completed bytes shifted right by 9, under the RQF_IO_STAT flag, exactly at the three anchored lines |
| S217 (`:25-28,31,84-85`) | 25-28 sector-unit comment (`512 = 2**9`); 31 `#define SECTOR_SHIFT 9`; 84-85 `#define bdev_whole(_bdev) \ ((_bdev)->bd_disk->part0)` | all three claims grounded, `bdev_whole` is `bd_disk->part0` |

## 3. ≤25-word quotes (PASS on the rule-backed reading; measurement recorded)

The ≤25-word rule is rule 1's Gate-quote rule (`CORPUS.md:113-114`, fleet repo): the Gate records "a ≤25-word
quote with its location grounding `teaches`". The quotes grounding these four teaches cells are the round-33 Gate
quotes the new cells restate. I re-verified all 12 mechanically (contiguity after whitespace-normalization in the
fetched bytes; `wc -w`-equivalent token count vs the recorded label):

```
S214 :60-63 (17 words) OK;  :10 (3) OK
S215 :1100 (7) OK; :1108-1110 (8) OK; :1067-1068 (8) OK
S216 :856 (8) OK; :858 (5) OK; :862 (5) OK
S217 :25 (9) OK; :26 (9) OK; :31 (3) OK; :84-85 (4) OK   — all contiguous, all labels correct, all ≤25
```

Teaches-cell token counts (after the `supersedes S0NN — ` prefix), measured: S214=19, S215=24, S216=17,
**S217=27**. No rule bounds the `teaches` cell ("one grounded learner benefit", `CORPUS.md:100-101`); the same
27-token sentence is S186's first-published, already-admitted teaches, and rows such as S220 far exceed it. Under
the assignment's literal "<=25 words" applied to the teaches cell, S217 measures 27 — reported, not ruled a
defect; the rule-backed reading (Gate quotes) passes 12/12.

## 4. Rule-2 form (PASS)

- Each teaches opens `supersedes S183/S184/S185/S186 —` with the em-dash (`corpus/SOURCES.md:220-223`).
- Ids are new at this round: `git log -S'S214' --oneline -- corpus/SOURCES.md` → `bf0df77` only (same for S215-S217); rows appended in id order after S204; superseded ids S183-S186 still present (never deleted).
- The historical in-place edits of S183-S186 (round-33 w2 commit `ab8f4cf`: anchor/teaches/scope changes, unlogged) are the routed debt; the discharge matches QUALITY 102's design ("a later row whose teaches opens `supersedes S###` is the correction's disposition; it does not erase the in-place change, which stays listed").
- Frozen gate re-run by me, read-only: `python3 tools/mori-sources-appendonly.py bf0df77 --round-base 6bd57097` → `appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] … round_changed=[]`, **exit 0**, with `changed S183 superseded_by=S214` … `changed S186 superseded_by=S217` — matches the L1 receipt and QUALITY 102's "the round passes only with `round_changed=[]`" while the 18 stay listed with dispositions.
- Census (lane's own awk, `CORPUS.md` §SOURCES): malformed rows 0; duplicate ids none.

## 5. Findings

### F1 — defect (minor, rows): `mined` + `used-by` pairing is unearned for S214–S217

`corpus/SOURCES.md:220-223` carry `status=mined`, `used-by=corpus/knowledge/disk-write-rate-r33.md`. The
registry defines `mined` as "cited by ≥1 path in `used-by`" (fleet `CORPUS.md:103`). Measured at `bf0df77` and
unchanged at `6827d6e`:

```
grep -rlE 'S21[4-7]' corpus SKILL.md SCORECARD.md README.md  →  corpus/SOURCES.md   (only the registry itself)
S214: citing_files=0  S215: 0  S216: 0  S217: 0
```

`disk-write-rate-r33.md` cites **S183, S184, S185, S186** (`:20-22,25,76-77,98`) — never S214-S217. The
round-36 lesson itself landed the governing rule and applied it to S205: "mined used-by must cite the entry that
cites the row; w2/RevKnowledgeDrift F2" (`corpus/lessons/round-36.md:18-19`, S205 `used-by` repointed to the
citing note). The same-family precedent honors it for discharge rows too: S201/S202 are `mined` with
`used-by=SKILL.md`, and SKILL.md cited S201/S202 already at `cedb0ec` when those rows landed
(`git show cedb0ec:SKILL.md | grep -c` → 1 each). Nothing cites S214-S217 anywhere in the lane (the pending-but-now-landed
round-36 lesson does not mention them either), so the four rows' status/used-by pairing contradicts the cell
definition and the round's own just-landed rule. Blast radius (measured, for routing only): S206-S209, S212-S213,
S218-S219 share the gap; S205/S210/S211/S220 are cited.

Impact: none on the measured claims — the C2 predicate ignores status cells, and the drift probe ignores them
too; anchors/teaches/copies of S214-S217 all verify (§1-§4). This is a registry-truthfulness defect in the
re-opened rows, exactly this seat's surface.

### F2 — deviation (minor, process): rule-1 Gate letter not met for S214–S217

Rule 1: the round lesson's `## Gate` records, for every new row, the URL, the access date and a ≤25-word quote
with location (`CORPUS.md:113-114`). `corpus/lessons/round-36.md:11` admits S205-S220 as one batch row
("located quotes verified … by w1 SupS* and w2 RevSupS* seats") and records no per-row URL, access date or quote
for S214-S217; round-35 recorded per-row Gate lines (`corpus/lessons/round-35.md:18-23`). The quotes do exist and
verify in the wave reports (my §3 re-check passes 12/12), so the substance is present — but the lesson itself
carries none of the three required artifacts for these four rows.

### F3 — evidence hazard (not landed): wrong word-count labels in the SupS183 draft Gate line

`.ufo/waves/round-36/w1/SupS183.md:29` labels `unsigned long sectors[NR_STAT_GROUPS];` "(5 words)" (actual 3),
`if (bdev_is_partition(part))` "(1)" (actual 2), `__part_stat_add(bwhOle…addnd);` "(1)" (actual 4). Measured by
token count against the fetched bytes; the landed round-33 labels for the same content are correct (17/3). The
landed lesson carries no labels for these rows, so nothing landed is wrong — but since `round-36.md:11`
delegates quote verification to these seat reports, a future transcription must not copy the SupS183 draft line.
This is the exact defect class corrected in round 29 (`SOURCES.md` search-log correction entry) and repeated in
round-35 M5.

## Verification gaps and residual risk

- Word-count convention: I used whitespace tokenization (`wc -w`-equivalent), the convention of round-29/35 labels.
- The live v7.2 files were fetched once per seat run (2026-10-23); raw.githubusercontent tag views are stable, but I
  cannot exclude a fetch-window discrepancy with the w1 seats' 12:03-12:05Z fetches — mitigated: hashes equal the
  round-33 recorded digests and both copy generations.
- I did not re-judge S206-S209/S212-213/S218-S219 (sibling seats' scope); F1's blast radius there is measured, not adjudicated.
- No tools were installed or updated (none needed). Scratch: `/fast/scratch/hyaku/mori-r36/RevSupS214S217-23/`.
  This report is the only lane file I wrote; the lane repo was only read (git read-only commands, the lane's own read-only gate tool).

## VERDICT: FAIL

The four assigned checks pass — copies sha256-equal (4/4), teaches quotes contiguous at their anchors, all 12
grounding quotes ≤25 words with correct landed labels, rule-2 form clean (`round_changed=[]`, exit 0, 18
dispositions). The FAIL rides on F1: at the carrying commits `bf0df77`/`6827d6e`, S214-S217 claim `mined` via a
`used-by` entry that does not cite them and nothing else in the lane does (`corpus/SOURCES.md:220-223` vs
`corpus/knowledge/disk-write-rate-r33.md:20-22`, against fleet `CORPUS.md:103` and the round's own rule at
`corpus/lessons/round-36.md:18-19`) — a concrete row-cell mismatch with path:line evidence above. F2/F3 are
recorded as process/evidence hazards.
