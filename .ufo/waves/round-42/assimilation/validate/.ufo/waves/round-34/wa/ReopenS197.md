measured 2026-10-23T05:39:38Z

# ReopenS197 — wave A verdict

Reviewer: MoriR34A2.ReopenS197 (leaf seat).
Target: SOURCES.md row S197 at rev 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3 (line 203).
Source URL: https://raw.githubusercontent.com/torvalds/linux/v4.18/block/genhd.c
Committed copy: corpus/evidence/sources-r34/S197.src.
Verdict words: rows supported/unsupported; code defect/no defect found; VERDICT line at end.

## 1. Live re-fetch (twice)

Commands (scratch /fast/scratch/hyaku/mori-r34/a2-ReopenS197/):
`curl -sSL --fail -m 60 -o S197.fetch1.txt <url>`, then same for S197.fetch2.txt; `date -u +%FT%TZ` after each; `sha256sum` each; `cmp` pair; sha256 + cmp against committed copy.

- date(1) = 2026-10-23T05:38:43Z; date(2) = 2026-10-23T05:38:43Z.
- sha256(fetch1) = 96b5638180eb70886195b46722681623301c328763b47c674a6543b27c3e748b
- sha256(fetch2) = 96b5638180eb70886195b46722681623301c328763b47c674a6543b27c3e748b
- cmp fetch1 vs fetch2: FETCHES_IDENTICAL (2017 lines each).
- sha256(committed S197.src) = 96b5638180eb70886195b46722681623301c328763b47c674a6543b27c3e748b (same as fetches); cmp committed vs fetch1: MATCHES_COMMITTED.
- git show 8d56809:corpus/evidence/sources-r34/S197.src | sha256sum = same 96b563... → committed copy is byte-identical at the reviewed rev and in the work tree.

Live source and committed copy are identical; two fetches are identical.

## 2. Tag v4.18 identity

- GitHub API `repos/torvalds/linux/git/refs/tags/v4.18`: ref exists, object type=tag, sha 85262cb1fbc5cc267b3c86bc162a02dedd219548.
- Independent mirror kernel.org cgit `plain/block/genhd.c?h=v4.18` → sha256 96b5638180eb70886195b46722681623301c328763b47c674a6543b27c3e748b; cmp: CGIT_MATCHES_FETCH.
- [INFERENCE] Kernel tags are immutable by convention; the tag resolves to the same bytes on two independent hosts. No deeper content-to-commit check was run (would require fetching the kernel repo).

## 3. Anchor cell: "block/genhd.c:1336-1351; tag v4.18"

- Function `diskstats_show` spans copy lines 1313–1356 (`static int diskstats_show(struct seq_file *seqf, void *v)` at 1313; closing `}` at 1356).
- The single `seq_printf` statement that prints the stats line covers exactly lines 1336–1351: format string 1336–1337, 14 arguments 1338–1350, closing `);` at 1351.
- Anchor lines hold the cited code. Supported.

## 4. Teaches cell — clause by clause

Teaches text: "The v4.18 diskstats_show format has 14 conversions (major, minor, name and 11 values) and its argument list ends with the in-flight, io_ticks and time_in_queue values; it prints no discard values." No `lane rule:` label present in this row.

C1 — "has 14 conversions (major, minor, name and 11 values)": SUPPORTED.
- Conversion specifiers, contiguous per line (no `"`/`|` in quotes):
  - S197.src:1336 (7 words): "%4d %7d %s %lu %lu %lu"
  - S197.src:1337 (8 words): "%u %lu %lu %lu %u %u %u %u"
  → 14 specifiers total: %4d %7d %s (major, minor, name) + 11 value specifiers.
- First three arguments: S197.src:1338-1339 (3 words): "MAJOR(part_devt(hd)), MINOR(part_devt(hd)), disk_name(gp, hd->partno, buf),"
- Remaining 11 value arguments occupy lines 1340–1350: ios[READ], merges[READ], sectors[READ], ticks[READ]→msecs, ios[WRITE], merges[WRITE], sectors[WRITE], ticks[WRITE]→msecs, inflight[0], io_ticks→msecs, time_in_queue→msecs.

C2 — "argument list ends with the in-flight, io_ticks and time_in_queue values": SUPPORTED.
- S197.src:1348-1350 (5 words): "inflight[0]," / "jiffies_to_msecs(part_stat_read(hd, io_ticks))," / "jiffies_to_msecs(part_stat_read(hd, time_in_queue))"
- These are the final three arguments before the closing paren at 1351.

C3 — "it prints no discard values": SUPPORTED (negative claim; verified by scan — absence cannot be quoted).
- Case-insensitive `grep -i discard` over the whole copy matches only lines 1121, 1127, 1137, 1159 — all sysfs device-attribute code (`disk_discard_alignment_show`, `dev_attr_discard_alignment`), outside `diskstats_show`.
- Printer lines 1336–1351 and function body 1313–1356 contain no discard/STAT_DISCARD token.

All teaches clauses supported.

## 5. Other cells

- kind=code, tier=A, scope "the v4.18 /proc/diskstats line format", status=mined, opened 2026-10-23, recheck=on-release: all internally consistent; no contradiction found.
- used-by corpus/knowledge/disk-write-rate-r33.md (Round-34 row 8 correction): not reviewed here (separate seat).

## 6. Tooling

- No tools installed or updated; no pacman transaction; nothing to record under the tooling directive.

## 7. Residual risk / verification gaps

- [INFERENCE] Tag v4.18 content ↔ release commit identity rests on tag immutability convention plus two-mirror agreement; a rewound tag would not be caught.
- No check of the downstream knowledge file that claims this row (out of scope).
- C3 is an absence claim; supported by whole-file scan, not by a quote.

## 8. Proposed Gate row

| S197 | https://raw.githubusercontent.com/torvalds/linux/v4.18/block/genhd.c | 2026-10-23T05:38:43Z | 96b5638180eb70886195b46722681623301c328763b47c674a6543b27c3e748b | %4d %7d %s %lu %lu %lu %u %lu %lu %lu %u %u %u %u | admit, A, mined |

VERDICT: admit
