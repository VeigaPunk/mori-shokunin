measured 2026-10-23T07:57:17Z

# Gate attack — S196 (seat MoriR34A3.GateS196, attempt 3 wave B)

Attacks: Gate row `/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_lessons_round-34.md:21` and registry row
`/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_SOURCES.md:202` (diff vs tip:
`/fast/scratch/hyaku/mori-r34/a3-L1/drafts/attempt2-tracked.diff` hunk at lines 128/136).
Copy under judgment: `corpus/evidence/sources-r34/S196.src` at fd2521351c6cef47384aef30afbe1e4db7e6912e
(28011 bytes, 1300 lines). Scratch: `/fast/scratch/hyaku/mori-r34/a3-GateS196/` (committed copy, live fetch,
check_quotes.py).

## 1. Live fetch vs committed copy

`curl -fsSL --max-time 60 https://raw.githubusercontent.com/util-linux/util-linux/v2.42.4/lib/sysfs.c`
- FETCH_START 2026-10-23T07:41:27Z, FETCH_END 2026-10-23T07:41:28Z.
- live sha256 `c19c802cc976c6be99c86db1e63ce4261ad7c9d4e5108cfa817526440cf9cbbf`, 28011 bytes.
- committed copy sha256 identical; `cmp` → IDENTICAL. Also identical at 8d56809af
  (`git show 8d56809…:corpus/evidence/sources-r34/S196.src | sha256sum` → same hash).
- Gate row's sha256 cell and URL cell match. Accessed cell cites 05:32:35Z (L1) + 05:40:20Z (ReopenS196);
  my fetch is a third independent open with the same hash.

## 2. Gate quotes — all four PASS byte-exactly

Check: each quote contiguous within its locator line after whitespace-run collapse
(`re.sub(r"\s+"," ",s).strip()`; script check_quotes.py), 3–25 words, count right, no `"` or `|`.

| locator | collapsed line (verbatim) | quote | words (claimed) | chars |
|---|---|---|---|---|
| S196.src:570 | `* parser) have the /sys/.../partition file. The partitions` | `parser) have the /sys/.../partition file. The partitions` | 7 (7) | none |
| S196.src:571 | `* mapped by DM don't have such file, but they have "part"` | `mapped by DM don't have such file,` | 7 (7) | none — quote ends before `"` |
| S196.src:241 | `/* Cannot use /partition file, not supported on old sysfs */` | `Cannot use /partition file, not supported on old sysfs` | 9 (9) | none |
| S196.src:305 | `* Returns slave name if there is only one slave, otherwise returns NULL.` | `Returns slave name if there is only one slave` | 9 (9) | none |

Each quote is a strict substring of its collapsed locator line (the `*`/`/*` comment glyphs sit outside the
quoted span, so no ` * `-spanning defect like the rejected seat proposals). Decision cell `admit, A, mined` ✓.

## 3. Registry row cell by cell

Row: `| S196 | util-linux lib/sysfs.c at v2.42.4 (partition and slave helpers) — <url> | code | A | … | lib/sysfs.c:205-245,304-325,524-592; tag v2.42.4 | <teaches> | mined | 2026-10-23 | on-release | SKILL.md |`

- id/name/URL ✓ — URL matches Gate row and fetched artifact; title accurate; `tag v2.42.4` pinned by URL.
- type `code`, tier `A`, status `mined`, opened `2026-10-23`, recheck `on-release` ✓.
- anchors hold the cited code: `205-245` = whole `sysfs_blkdev_is_partition_dirent()` (def 205, `}` 245),
  including the `/partition`-fallback comment at 241. `304-325` = doc comment `/*` 304..`*/` 307 +
  `sysfs_blkdev_get_slave()` def 308 through `return name;` 325 (err cleanup runs 326-330, just past the range).
  `524-592` = whole `get_dm_wholedisk()` (def 524, `}` 548) + `sysfs_blkdev_get_wholedisk()` def 554 through
  `}` 592 closing the DM-partition branch. Every teaches-relevant statement is inside the ranges; the two
  ranges that end mid-function stop after the cited logic — cosmetic, not a miss.
- teaches clauses (none labelled `lane rule:`; all four stated by the copy):
  1. "Regular partitions (BLKPG or kernel partition-table parser) have a /sys/.../partition file" —
     supported by comment S196.src:569-570 and code S196.src:564 `is_part = ul_path_access(pc, F_OK, "partition") == 0;`
  2. "partitions mapped by device-mapper do not" — comment S196.src:567 ("Extra case for partitions mapped
     by device-mapper.") and 570-571; DM `part` UUID fallback at 575-580.
  3. "the partition file cannot be used on old sysfs" — comment S196.src:241; fallback to `<name>/start`
     readability at 242-244.
  4. "the slave helper returns a name only for exactly one slave" — doc comment 305; enforcement: zero
     slaves → name NULL → `return name` (325) yields NULL, ≥2 slaves → `goto err` (319-320) → NULL; restated
     530-531 ("returns the first slave only; if there are more slaves, it returns NULL").
- used-by `SKILL.md` — file exists at fd25213 (`git ls-tree` → `SKILL.md`; `## Round34` section at
  SKILL.md:826). Residual: the Round34 rules cite S191–S195 (SKILL.md:832) but name no S196; the used-by
  link is semantic only. Cell itself satisfies the existence check.
- diff vs tip (attempt2-tracked.diff:128 vs :136): only the used-by cell changes, `SKILL.md Round34` →
  `SKILL.md` — the committed row at fd25213 corpus/SOURCES.md:202 otherwise equals the draft row;
  consistent with the M6 single-path census narrative.

## 4. Audit of /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/wa/ReopenS196.md

Independence: my §1–§3 verdicts were reached from the bytes before opening this report.

1. agree — two live fetches hashed `c19c802c…`: the seat's artifacts `/fast/scratch/hyaku/mori-r34/a2-ReopenS196/s196.live{1,2}.c` both hash `c19c802c…` today; my independent fetch agrees. (Accessed timestamps unverifiable now; hash equivalence is the citable fact.)
2. agree — committed copy 1300 lines, same hash; verified at fd25213 (28011 B).
3. agree — S196.src at 8d56809 hashes `c19c802c…` (verified by `git show` above).
4. agree — `corpus/SOURCES.md` at 8d56809 hashes `78437f68ce7f54292f1b3df34456e5a80ded839e8902c1e4c2ce91c84ec0ab6d` (verified); row S196 sits at :202 there and at fd25213.
5. agree — row transcription (report §2) matches committed row and draft row verbatim, modulo the used-by cell it records as `SKILL.md Round34` (the pre-M6 value; draft now `SKILL.md`).
6. agree — anchor `205-245` is exactly `sysfs_blkdev_is_partition_dirent()` (def 205, `}` 245).
7. agree — `304-325` = doc comment + `sysfs_blkdev_get_slave()` through `return name;` at 325.
8. agree — `524-592` = `get_dm_wholedisk()` 524-548 + `sysfs_blkdev_get_wholedisk()` from 554 through the DM-branch `}` at 592.
9. agree — clause 1 supported; text at 569-570 verbatim; code cite 564 verbatim. (Its "15 words" count is right, but see disagree-2: it cannot serve as a Gate quote.)
10. agree — clause 2 supported; 570-571 quote is 9 words verbatim; corroboration 567 is 7 words verbatim.
11. agree — clause 3 supported; quote at 241 verbatim 9 words; fallback `faccessat(..., R_OK, 0)` at 242-244 verbatim.
12. agree — clause 4 supported; quote at 305 verbatim 9 words; enforcement lines 318-321 verified (`if (name) goto err` → NULL).
13. disagree — the report counts the 530-531 restatement as "15 words"; the verbatim text "returns the first slave only; if there are more slaves, it returns NULL" is 13 words.
14. disagree (with §5/§60's implication that the seat's proposals were valid Gate quotes): its proposed quotes `569-570` and `570-571` span a ` * ` comment prefix — under whitespace-run collapse "PT * parser)" ≠ "PT parser)", so they are not contiguous; the lessons file records the L1 rejected exactly these and landed single-line quotes instead. The report's located-quote evidence for the clauses is still sound.
15. agree — residual claim (report:59): helper also returns NULL when `slaves` cannot be opened (314-316 verified); consistent with "only for exactly one slave".
16. agree — `VERDICT: admit` on the row: all clauses supported, anchors hold, status/tier correct.

AUDIT: agree 14 / disagree 2

## Verdict

The draft Gate row (lessons :21) and registry row (SOURCES :202) survive every attack: live bytes equal the
committed copy, all four landed quotes verify, every cell checks. No cell changes.

VERDICT: admit

## Residual risk / verification gaps

- Tag `v2.42.4` mutability assumed, not observed (three independent opens — L1, seat, mine — agree) [INFERENCE].
- `used-by SKILL.md`: exists but names no S196 row/section at fd25213; link is semantic.
- Anchors `304-325` and `524-592` end mid-function (err cleanup; wholedisk tail) — cited logic fully inside.
- Tooling: none installed; stock curl 8.x/sha256sum/python3/git sufficed (pacman paused).
- Containment: writes only this report and `/fast/scratch/hyaku/mori-r34/a3-GateS196/` (~84 KB); read-only
  git; no processes left running; only message target agent://MoriR34A3.
