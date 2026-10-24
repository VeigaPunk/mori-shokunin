measured 2026-10-23T05:40:20Z

# Re-open S196 — util-linux lib/sysfs.c at v2.42.4 (seat MoriR34A2.ReopenS196)

Axes (godspeed): (1) byte fidelity — live fetch vs committed copy vs blob at rev 8d56809; (2) quote grounding — every teaches/anchor clause located in the copy; (3) anchor truth — cited line numbers hold the cited code; (4) verdict discipline — admit only if 1-3 hold.

## 1. Live re-open (twice)

Command shape (each curl wrapped in `timeout 70`, `-sSL --fail -m 60`, output to scratch):
`curl -sSL --fail -m 60 https://raw.githubusercontent.com/util-linux/util-linux/v2.42.4/lib/sysfs.c -o s196.liveN.c`

- Fetch 1: accessed 2026-10-23T05:40:20Z, sha256 `c19c802cc976c6be99c86db1e63ce4261ad7c9d4e5108cfa817526440cf9cbbf`
- Fetch 2: accessed 2026-10-23T05:40:20Z, sha256 `c19c802cc976c6be99c86db1e63ce4261ad7c9d4e5108cfa817526440cf9cbbf`
- `cmp` fetch1 vs fetch2 → LIVE1_EQ_LIVE2.
- Committed copy `corpus/evidence/sources-r34/S196.src` (1300 lines) sha256 `c19c802c…` → LIVE1_EQ_COMMITTED and LIVE2_EQ_COMMITTED.

At-revision pinning:
- `git show 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3:corpus/evidence/sources-r34/S196.src | sha256sum` → `c19c802c…` — equals live and working tree.
- `git show 8d56809…:corpus/SOURCES.md | sha256sum` → `78437f68ce7f54292f1b3df34456e5a80ded839e8902c1e4c2ce91c84ec0ab6d` = sha256 of working-tree `corpus/SOURCES.md` — the row read below is the row at the attack revision.
- Lane note: `git rev-parse HEAD` currently returns `fd2521351c6cef47384aef30afbe1e4db7e6912e` (tip has advanced past 8d56809), but both analyzed files are byte-identical at 8d56809 per the hashes above, so all findings are at-revision.

## 2. Row under judgment — corpus/SOURCES.md:202 (at 8d56809)

- id S196 | util-linux lib/sysfs.c at v2.42.4 (partition and slave helpers) | code | A
- scope: how util-linux 2.42.4 detects partitions and reads slaves
- anchor: `lib/sysfs.c:205-245,304-325,524-592; tag v2.42.4`
- teaches: "Regular partitions (BLKPG or kernel partition-table parser) have a /sys/.../partition file; partitions mapped by device-mapper do not; the partition file cannot be used on old sysfs; the slave helper returns a name only for exactly one slave."
- status mined, opened 2026-10-23, recheck on-release, used-by SKILL.md Round34.

## 3. Anchor check — line numbers hold the cited code (raw reads of the fetched copy, byte-identical to S196.src)

- `205-245` → exactly the whole `sysfs_blkdev_is_partition_dirent()` (definition at 205, closing brace at 245). Holds.
- `304-325` → `sysfs_blkdev_get_slave()`: doc comment 304-307, definition 308, body through `return name;` at 325. Holds.
- `524-592` → `get_dm_wholedisk()` 524-548 and `sysfs_blkdev_get_wholedisk()` from 554 through the DM-branch close at 592. Holds.
- `tag v2.42.4` → URL pins the tag; fetched bytes match the committed copy (§1). Holds.

## 4. Teaches clauses — none is labelled `lane rule:`; all four judged

1. supported — S196.src:569-570 (15 words): "All regular partitions (added by BLKPG ioctl or kernel PT parser) have the /sys/.../partition file."
   Code: S196.src:564 `is_part = ul_path_access(pc, F_OK, "partition") == 0;` (not quoted: line contains `"`).
2. supported — S196.src:570-571 (9 words): "The partitions mapped by DM don't have such file,"
   Corroboration — S196.src:567 (7 words): "Extra case for partitions mapped by device-mapper."
3. supported — S196.src:241 (9 words): "Cannot use /partition file, not supported on old sysfs"
   Code path: S196.src:242-244 falls back to `<name>/start` readability via `faccessat(..., R_OK, 0)`.
4. supported — S196.src:305 (9 words): "Returns slave name if there is only one slave"
   Enforcement: S196.src:318-321 — second dirent hits `goto err` → returns NULL; restated at S196.src:530-531 (15 words): "returns the first slave only; if there are more slaves, it returns NULL"

No clause unsupported; no quote used contains `"` or `|`.

## 5. Proposed Gate row

| S196 | https://raw.githubusercontent.com/util-linux/util-linux/v2.42.4/lib/sysfs.c | 2026-10-23T05:40:20Z | c19c802cc976c6be99c86db1e63ce4261ad7c9d4e5108cfa817526440cf9cbbf | S196.src:569-570 (15 words): "All regular partitions (added by BLKPG ioctl or kernel PT parser) have the /sys/.../partition file." S196.src:570-571 (9 words): "The partitions mapped by DM don't have such file," S196.src:241 (9 words): "Cannot use /partition file, not supported on old sysfs" S196.src:305 (9 words): "Returns slave name if there is only one slave" | admit, A, mined |

VERDICT: admit

## Residual risk / gaps

- raw.githubusercontent serves whatever the tag points at; GitHub tag immutability is assumed, not observed [INFERENCE]. Mitigated: two independent fetches today agree with the copy committed at 8d56809.
- Clause 4 phrasing "only for exactly one slave": the helper also returns NULL when `slaves` cannot be opened (S196.src:314-316); consistent with "only for", not contradicting it.
- Comment-marker `/* */` glyphs around lines 241/305/569-571 are outside the quoted word spans; quoted words are contiguous in their lines (raw reads §3/§4).
- Tooling directive: no tools installed — stock curl/sha256sum/git sufficed.
- Containment: writes limited to this report and `/fast/scratch/hyaku/mori-r34/a2-ReopenS196/` (two live copies); no git/jj writes, no write load, no leftover processes.
