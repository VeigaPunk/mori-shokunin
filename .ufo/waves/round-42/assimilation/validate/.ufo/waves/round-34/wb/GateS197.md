measured 2026-10-23T07:43:00Z

# GateS197 — wave B verdict

Reviewer: MoriR34A3.GateS197 (leaf seat, wave B).
Targets: Gate row S197 (`/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_lessons_round-34.md:22`) and the
S197 registry row (`/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_SOURCES.md:203`; committed counterpart
`corpus/SOURCES.md` line 203 at fd2521351c6cef47384aef30afbe1e4db7e6912e, diff in
`/fast/scratch/hyaku/mori-r34/a3-L1/drafts/attempt2-tracked.diff:129,137`).
Copy under test: `corpus/evidence/sources-r34/S197.src` (2017 lines) extracted read-only from the lane at tip.

## 1. Live fetch vs committed copy

- `date -u` at fetch: 2026-10-23T07:41:15Z.
- `curl -sSL https://raw.githubusercontent.com/torvalds/linux/v4.18/block/genhd.c` →
  sha256 `96b5638180eb70886195b46722681623301c328763b47c674a6543b27c3e748b` (2017 lines).
- `git cat-file -p fd252135:corpus/evidence/sources-r34/S197.src` → identical sha256 and line count.
- Also byte-identical at rev 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3 (`git cat-file` → same sha256).
- Independent mirror: `git.kernel.org .../plain/block/genhd.c?h=v4.18` fetched 07:42Z → same sha256.
- Row sha256 cell matches all of the above. Fetch equality holds.

## 2. Gate quotes re-located in the copy (whitespace runs collapsed)

- `S197.src:1338-1339` → `MAJOR(part_devt(hd)), MINOR(part_devt(hd)), disk_name(gp, hd->partno, buf),`
  contiguous at locator; 5 words (row says 5); no `"`, no `|`. PASS.
- `S197.src:1348-1350` → `inflight[0], jiffies_to_msecs(part_stat_read(hd, io_ticks)), jiffies_to_msecs(part_stat_read(hd, time_in_queue))`
  contiguous at locator; 5 words (row says 5); no `"`, no `|`. PASS.
- Lesson line 31-32 claim that a format quote at `:1336-1337` was rejected for containing `"`: lines 1336-1337
  do contain `"` (format string literals); consistent.

## 3. Draft registry row, cell by cell

| cell | value | check |
|---|---|---|
| id, title/URL | S197, `…/torvalds/linux/v4.18/block/genhd.c` | fetchable, correct file/tag; PASS |
| kind / tier | `code` / `A` | C source at a release tag; PASS |
| scope | `the v4.18 /proc/diskstats line format` | `proc_create_seq("diskstats", …)` at S197.src:1367 wired to `diskstats_show` (1313–1356); PASS |
| anchor | `block/genhd.c:1336-1351; tag v4.18` | the single `seq_printf` that prints the stats line: format 1336–1337, args 1338–1350, `);` at 1351; PASS |
| teaches | see below | every clause supported |
| status / opened / recheck | `mined` / `2026-10-23` / `on-release` | PASS |
| used-by | `corpus/knowledge/disk-write-rate-r33.md` | exists at fd252135 (`git cat-file -e` OK) and cites S197 (file lines 83–87); single path, M6-conformant |

Teaches clauses (no `lane rule:` label in this row):
- "14 conversions (major, minor, name and 11 values)": format `"%4d %7d %s %lu %lu %lu %u %lu %lu %lu %u %u %u %u\n"`
  = 14 specifiers, 14 args (1338–1350). Located: S197.src:1336-1337 (format), 1338-1339 (major/minor/name), 1340-1350 (11 values).
- "argument list ends with the in-flight, io_ticks and time_in_queue values": S197.src:1348-1350 (quoted above).
- "prints no discard values": `diskstats_show` body 1313–1356 contains no discard token; whole-file `discard` matches
  are only sysfs attr code at 1121/1127/1137/1159, outside the printer. SUPPORTED.

Draft vs committed row: the only change (attempt2-tracked.diff:129→137) drops the used-by annotation
`(Round-34 row 8 correction)` → single path; all other cells unchanged. Both rows verify clean under this audit.

## Audit of /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/wa/ReopenS197.md

- sha256 of both fetches and committed copy = `96b563…748b`, 2017 lines: agree (my fetch 07:41:15Z, git cat-file at fd252135 and 8d56809a).
- kernel.org cgit mirror sha256 matches: agree (re-fetched now, same hash).
- GitHub API tag ref sha `85262cb1…219548`: not verified — GitHub API rate-limited me now; tag content is corroborated by two-host byte agreement. [INFERENCE] plausible, not counted either way.
- "`diskstats_show` spans 1313–1356": agree (S197.src:1313 `static int`, closing `}` at 1356).
- "`seq_printf` covers exactly 1336–1351, format 1336–1337, 14 arguments 1338–1350, `);` at 1351": agree (I count 14 args).
- "14 conversion specifiers" from 1336–1337: agree (`%4d %7d %s` + 11 value specifiers).
- Annotation "(3 words)" on the 1338–1339 argument quote: disagree — the joined text has 5 whitespace-separated words
  (`MAJOR(part_devt(hd)),` `MINOR(part_devt(hd)),` `disk_name(gp,` `hd->partno,` `buf),`); the underlying locator/content claim is right.
- "remaining 11 value arguments occupy 1340–1350" (ios/merges/sectors/ticks R+W, inflight, io_ticks, time_in_queue): agree.
- "discard matches only 1121/1127/1137/1159, all outside `diskstats_show`": agree (my grep; no DISCARD token at all in v4.18 file).
- "kind/tier/scope/status/opened/recheck consistent": agree.

AUDIT: agree 9 / disagree 1

## Tooling

- No tools installed or updated; pacman untouched (host-wide pause). curl, git, coreutils only.

## Residual risk / gaps

- GitHub tag-ref sha not independently verified (API rate limit); two-mirror byte agreement stands in.
- Word-count slip in ReopenS197 §4 is cosmetic; the Gate row's own "(5 words)" counts are correct.
- No defects found in row cells, quotes, or fetch chain.

VERDICT: admit — no row cells need changing; every cell of the draft S197 row verifies against the bytes.
