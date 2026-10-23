measured 2026-10-23T07:43:35Z

# GateS198 — independent re-attack of draft Gate row S198 and registry row (wave B)

Seat: MoriR34A3.GateS198 (leaf). Objects under attack:
- Gate row: `/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_lessons_round-34.md:23`
- Registry row: `/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_SOURCES.md:204`
  (diff vs tip `fd25213` in `/fast/scratch/hyaku/mori-r34/a3-L1/drafts/attempt2-tracked.diff:130,138`)

## 1. Live re-open (independent fetch)

- `curl https://raw.githubusercontent.com/torvalds/linux/v4.19/block/genhd.c` at
  2026-10-23T07:41:01Z → sha256 `4c55aeba02bfaecee8ef5a20514f834f2aa34a338f51a66a83bcc40d5a7588f1`,
  50211 bytes (scratch: `/fast/scratch/hyaku/mori-r34/a3-GateS198/S198.live`, fetch-ts.txt).
- Committed copy at `fd25213` (`git cat-file -p fd25213:corpus/evidence/sources-r34/S198.src`):
  same sha256 `4c55aeba…f1`; 2024 lines, 50211 bytes; blob `be5bab20b2abf278fd7d7370c1a082de0928b1ed`.
- Lesson row sha256 cell `4c55aeba…f1` matches my live fetch and the committed copy. Row's accessed
  timestamps (05:32:35Z L1, 05:38:48Z ReopenS198) precede my fetch — consistent.

## 2. Gate quote check (whitespace runs collapsed)

Row cites one quote: `S198.src:1354-1357` (9 words):
`part_stat_read(hd, ios[STAT_DISCARD]), part_stat_read(hd, merges[STAT_DISCARD]), part_stat_read(hd, sectors[STAT_DISCARD]), (unsigned int)part_stat_read_msecs(hd, STAT_DISCARD)`

- Lines 1354-1357 of the committed copy (verified against `git cat-file` output) are exactly the
  four trailing arguments of the `seq_printf`; collapsed, they equal the quote verbatim. Contiguous. ✓
- `wc -w` on collapsed 1354-1357 = 9 words; stated 9. ✓ 3 ≤ 9 ≤ 25. ✓
- `grep -c '["|]'` on the quote = 0: no `"`, no `|`. ✓

## 3. Registry row, cell by cell

| cell | value | check | result |
|---|---|---|---|
| id | S198 | — | ok |
| source | genhd.c at v4.19 + raw.githubusercontent URL | URL fetched live, matches copy | ok |
| kind | code | C source file | ok |
| tier | A | required tier | ok |
| scope | "the v4.19 /proc/diskstats line format" | anchor block is the diskstats seq_printf (fn `diskstats_show` at :1313, call :1336-1358, `.show = diskstats_show` :1369) | ok |
| anchor | `block/genhd.c:1336-1358; tag v4.19` | 1336 opens `seq_printf(seqf, "%4d %7d %s "`, 1358 closes `);` — exactly the call; URL pins tag v4.19 | ok |
| teaches | 18 conversions; arg list ends with four STAT_DISCARD values; `lane rule:` boundary | below | ok |
| status | `mined` | required | ok |
| opened | 2026-10-23 | consistent with Gate accessed cell | ok |
| recheck | `on-release` | consistent with sibling rows | ok |
| used-by | `corpus/knowledge/disk-write-rate-r33.md` | exists at `fd25213` (blob `e8e661f2`); its Row-8-correction section (:81-88) cites `S198.src:1336-1358` explicitly — real usage. Single path (M6-compliant); attempt-2 diff removes the `(Round-34 row 8 correction)` annotation that failed census | ok |

### Teaches clauses

- Clause A "has 18 conversions": arithmetic over the anchored block, not a literal sentence.
  Format string lines 1336-1340: `grep -o '%[0-9lu]*[a-z]'` → 18 conversions. Argument list
  lines 1341-1357: major, minor, name + 15 value arguments = 18. Supported by the copy.
  Located supporting text: `S198.src:1341-1357` is the complete argument list (slices verified:
  1341-1342 = 5 words `MAJOR(part_devt(hd)), MINOR(part_devt(hd)), disk_name(gp, hd->partno, buf),`;
  1351-1353 = 5 words `inflight[0], jiffies_to_msecs(part_stat_read(hd, io_ticks)), jiffies_to_msecs(part_stat_read(hd, time_in_queue)),`; 1354-1357 = 9 words, above). The format-string
  lines 1336-1340 cannot be quoted (contain `"`, excluded by quote rule) — arithmetic anchor stands.
- Clause B "ends with four STAT_DISCARD values (ios, merges, sectors, msecs)": stated by the copy —
  the :1354-1357 quote above is exactly ios/merges/sectors/msecs STAT_DISCARD, and :1357 is the last
  argument before `);` at 1358. Supported.
- Clause C `lane rule:` — exempt from copy-stated requirement; fact-checked anyway:
  `S197.src` (v4.18, sha256 `96b5638180eb…48f1` == committed copy at fd25213) has `seq_printf` at
  :1336 with argument list ending :1336-1351 and zero `STAT_DISCARD`/`DISCARD` occurrences
  (`grep -n DISCARD` → none). The boundary claim (first at v4.19, not v4.18) holds on the bytes.
- The earlier overclaim noted in the lesson ("the first release whose printer carries discard
  fields") is absent from the draft row — it is now correctly labelled `lane rule:`. ✓

## Audit of .ufo/waves/round-34/wa/ReopenS198.md

Independence: all §1-3 conclusions were reached from my own fetch and `git cat-file` reads before
opening the report. Factual claims the round would cite:

1. Row was `corpus/SOURCES.md:204` at `8d56809a` — **agree** (`git show 8d56809a:corpus/SOURCES.md`,
   row at :204).
2. Worktree copy byte-identical to 8d56809a — agree in substance: `git show 8d56809a:…/S198.src`
   sha256 = `4c55aeba…f1` == fd25213 copy; blob `be5bab20…81ed` confirmed at fd25213.
3. sha256 `4c55aeba…f1` on both fetches and the committed copy — **agree** (my independent fetch
   at 07:41:01Z yields the same).
4. Copy is 2024 lines / 50211 B — **agree** (wc -l 2024, wc -c 50211).
5. 18 format conversions (3+4+4+3+4) and 18 arguments — **agree** (my grep count = 18; argument
   list 1341-1357 = 18 args).
6. Five quoted slices, all 3-25 words, no `"`/`|` — **agree** (verified 1341-1342, 1351-1353,
   1354-1357 by wc; 1343-1346, 1347-1350 are the symmetric read/write 4-token groups at
   `S198.src:1343-1350`, each 9 words).
7. Clause-3 fact-check: v4.18 sha256 `96b56381…`, no STAT_DISCARD, 14-conversion call :1336-1351 —
   **agree** (my grep on committed S197.src: no DISCARD; hash matches).
8. Anchor 1336-1358 holds the cited code — **agree**.
9. "No defect found" findings (§4 items 1-3, incl. the "18 conversions is arithmetic" caveat) —
   **agree**.
10. §5 residuals (only v4.19 re-opened; rule rests on S197 copy; status/recheck/used-by unassessed)
    — **agree**; my checks above cover the cells they left open (all pass).

AUDIT: agree 10 / disagree 0

## Findings by severity

- None. No defect found in Gate row, quote, or any registry cell for S198.
- Residual: only tag v4.19 re-opened (as the row cites); the `lane rule:` claim additionally
  verified against S197's committed v4.18 copy. Attempt-2 diff cell for S198 changes only the
  used-by annotation removal — an improvement (M6 fix), not a defect.

VERDICT: admit
