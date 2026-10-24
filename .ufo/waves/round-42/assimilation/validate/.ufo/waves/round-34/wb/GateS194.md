measured 2026-10-23T07:46:07Z
# GateS194 — wave B re-derivation of S194 (zram_drv.c v7.2, gendisk registration)

Seat: MoriR34A3.GateS194. Objects:
- Gate row: /fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_lessons_round-34.md:19
- Registry row: /fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_SOURCES.md:200 (diff hunk /fast/scratch/hyaku/mori-r34/a3-L1/drafts/attempt2-tracked.diff:134; old line :126)
- Committed copy: corpus/evidence/sources-r34/S194.src at fd2521351c6cef47384aef30afbe1e4db7e6912e
- Audit lead: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/wa/ReopenS194.md

No tools installed (curl, sha256sum, git, awk already present). Scratch: /fast/scratch/hyaku/mori-r34/a3-GateS194/{S194.live.src,S194.committed.src,S182.committed.src,fetch-time.txt}. Lane git used read-only (show, ls-tree, log).

## Live fetch vs committed copy

- Live fetch: `curl -sS --max-time 60` of https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/block/zram/zram_drv.c at 2026-10-23T07:41:56Z → HTTP 200, 78168 bytes, sha256 `d5d4933a2aed57d667edbb8c8904be3d9569a61cc5a428a2cd8b044aeab00f25`.
- Committed copy `git show fd25213:corpus/evidence/sources-r34/S194.src` → sha256 `d5d4933a…ab00f25`, 3301 lines / 78168 bytes (`wc -l -c`). Live == committed byte-for-byte (`diff` of the two sha256 outputs identical).
- Gate-row sha256 cell `d5d4933a…ab00f25` matches both. Accessed cells `2026-10-23T05:32:35Z (L1); 2026-10-23T05:38:39Z (ReopenS194)` are consistent with commit 8d56809a's message ("copies re-fetched 05:32Z, sha match") and the wave-A report's Fetch-1 start 05:38:39Z.

## Gate quote re-location (whitespace runs collapsed)

- `S194.src:3094` holds `	ret = device_add_disk(NULL, zram->disk, zram_disk_groups);` — contiguous single line, matches the quoted text verbatim.
- Word count: `awk '{print NF}'` → 5 words; claim "(5 words)" correct; within 3-25.
- Forbidden chars: no `"`, no `|` (shell case-match: none).

## Registry row, cell by cell (draft corpus_SOURCES.md:200)

- name/url: "Linux drivers/block/zram/zram_drv.c at v7.2 (gendisk registration)" + raw.githubusercontent.com …/v7.2/… — serves the v7.2 tag file (fetch above).
- type `code`, tier `A` — correct for a C source row.
- scope: "how v7.2 zram registers its gendisk" — accurate; the call sits in the registration path (`S194.src:3074` blk_alloc_disk, `:3093` set_capacity, `:3094` device_add_disk).
- anchor `drivers/block/zram/zram_drv.c:3094; tag v7.2` — line 3094 holds the cited code (above). `grep -n device_add_disk S194.src` returns only :3094 — sole call site.
- teaches clause 1 (not `lane rule:`): "zram calls device_add_disk with NULL as its first argument (the parent argument per S182's device_add_disk signature)."
  - Located quote supporting it: `S194.src:3094` "ret = device_add_disk(NULL, zram->disk, zram_disk_groups);" — NULL is the first argument.
  - S182 cross-reference verified at tip: `corpus/evidence/sources-r33/S182.src:620-621` "int __must_check device_add_disk(struct device *parent, struct gendisk *disk, / const struct attribute_group **groups)" — first parameter is `parent`. Supported.
- teaches clause 2: `lane rule:`-labelled — exempt from copy support per the reopen rule.
- status `mined` — matches Gate decision cell "admit, A, mined".
- opened `2026-10-23`, recheck `on-release` — consistent with the round.
- used-by `SKILL.md` — exists at fd25213 (`git ls-tree` lists SKILL.md) and genuinely uses the source: SKILL.md:832 "otherwise virtual, as a zram disk registered without a parent (S194; sysstat also calls a device without a `device` link virtual, S195)". The diff changes only this cell vs 8d56809a (`SKILL.md Round34` → `SKILL.md`), matching the lesson's E11/M6 single-path narrative (corpus_lessons_round-34.md:44-45).

No defective cell found; I would change nothing.

## Audit of /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/wa/ReopenS194.md

- L4 "SOURCES.md row S194 at lane tip 8d56809a…25f5f3": DISAGREE. The row exists at 8d56809a (verified: `git show 8d56809a:corpus/SOURCES.md`, used-by `SKILL.md Round34`), but at the report's measured time 05:38:55Z the lane tip was fd25213 — committed 05:37:39Z, child of 8d56809a (`git log --format='%h parent=%p'`), while 8d56809a is 05:34:40Z. Harmless: the row bytes are identical at both commits.
- L9 Fetch 1 start 05:38:39Z, sha256 d5d4933a…, 3301 lines / 78168 bytes: AGREE. Same sha/bytes on my fetch; the cited scratch file exists and hashes to the same sha (`sha256sum /fast/scratch/hyaku/mori-r34/a2-ReopenS194/S194.live1.c` → d5d4933a…).
- L10 Fetch 2 start 05:38:43Z, same sha/size: AGREE. `S194.live2.c` hashes to the same sha.
- L11 committed copy sha/size: AGREE — my own measurement of `git show fd25213:…S194.src`.
- L12 live1 == live2 == committed, byte-identical: AGREE — all four hashes identical.
- L13 pinned URL serves v7.2 tag content: AGREE — bytes fetched at my re-verification match the committed copy.
- L17 anchor cell text `drivers/block/zram/zram_drv.c:3094; tag v7.2`: AGREE — draft row cell verbatim.
- L18 line 3094 holds the cited code: AGREE — re-located above.
- L19 sole device_add_disk call in file: AGREE — `grep -n` on committed copy returns only :3094.
- L20 registration-path context (3074 blk_alloc_disk, 3093 set_capacity, 3094 call) and scope accuracy: AGREE — lines shown above.
- L24-25 clause 1 supported, located quote :3094 (5 words): AGREE.
- L26 parenthetical = first-argument-is-parent per S182 signature: AGREE — verified independently at S182.src:620-621 (the report said "not re-verified against genhd.c"; its inference is correct).
- L28-29, 31 clause 2 is an exempt `lane rule:`; no clause lacks an anchor: AGREE — same reading I applied.
- L35 proposed Gate row matches the landed Gate row (accessed-date format aside): AGREE.
- L37 `VERDICT: admit`: AGREE with my own independent verdict.
- L41 "No tools installed": AGREE — consistent with the needed toolset (curl present). [INFERENCE] I did not audit its system.
- L42 scratch files exist (~156 KB): AGREE — S194.live1.c + S194.live2.c = 156336 bytes total, both hash to the claimed sha.

AUDIT: agree 16 / disagree 1

## Verdict

The draft registry row is accurate in every cell; the Gate row's quote, sha256, and decision all re-derive cleanly from the live URL and the committed copy. The single flaw found is in the wave-A audit lead's provenance line (stale tip), which changes nothing about the row.

VERDICT: admit
