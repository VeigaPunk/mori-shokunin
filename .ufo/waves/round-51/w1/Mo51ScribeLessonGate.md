# Mo51ScribeLessonGate — draft `## Gate` for `corpus/lessons/round-51.md`

Seat: scribe. Assignments: draft the `## Gate` section of the round-51 lesson (content below, fenced, house shape
of `corpus/lessons/round-50.md`); the five new SOURCES rows S492–S496 with quote cells left to the quote seat;
assimilation none; considerthese suggestion 1 as implemented inside C1; census start; a spot-check offering
admit and reject decisions. I edited no file but this report.

## What I ran and saw (read-only)

All commands from `/home/vgpnk/Projects/shokunin/mori-shokunin` unless the `cwd` is named; scratch was
`/fast/scratch/hyaku/mori-r51/Mo51ScribeLessonGate/` with `TMPDIR=/fast/scratch/hyaku/mori-r51/Mo51ScribeLessonGate/tmp`.

| # | command | outcome |
|---|---|---|
| 1 | `scripts/hyaku/disk-guard.sh status` | rc 0; `/fast/scratch/hyaku` 27 % used, 587.9 G free. No heavy run, no ENOSPC. |
| 2 | `git -C mori-shokunin rev-parse HEAD` | `b504cb1701568a0038aab9d98ec13d28eff801da` (wave tip; `87e0c374` is an ancestor) |
| 3 | `git show 87e0c374:corpus/SOURCES.md > $S/SOURCES-at-data.md`; `grep -nE '^ {0,3}\|[[:space:]]*S(082\|168\|492\|493\|494\|495\|496)[[:space:]]*\|'` | S082 at line 88, S168 at 174, S492–S496 at 271–275 (five rows, 336-line registry) |
| 4 | `git diff --numstat aa3af1ec 87e0c374 -- corpus/SOURCES.md` | `5	0	corpus/SOURCES.md` — five lines added, none removed, so no earlier row was edited this round |
| 5 | `for f in 34e431b0.patch meminfo.c.v7.2 mm_inline.h.v7.2 proc.rst.v7.2 show_mem.c.v7.2; do git cat-file -p 87e0c374:corpus/evidence/sources-r51/$f \| sha256sum; done` | 5/5 equal to the `sha256` cells of S492–S496 and to the five `sources-r51` lines of `evidence/freeze-sha256.txt` (21 lines total, `grep -c sources-r51` → 5) |
| 6 | worktree `sha256sum corpus/evidence/sources-r51/*` | same five hashes; `git status --porcelain corpus/SOURCES.md` empty and `git diff 87e0c374 -- corpus/SOURCES.md` empty; `git cat-file -p 87e0c374:corpus/knowledge/memavailable-estimate-r51.md \| sha256sum` = worktree `b04f030d…d4803` (entry is the data commit's bytes) |
| 7 | sweep re-run, read-only: `for p in MemAvailable si_mem_available totalreserve wmark_low folio_is_file_lru 34e431b0 show_mem.c; do git grep -c -F "$p" aa3af1ec -- corpus/SOURCES.md corpus/knowledge SKILL.md; done` | `MemAvailable`: 7 files (`corpus/SOURCES.md:1`, `audit-r11.md:1`, `harness-job-capacity-r25.md:1`, `observability-surfaces-r2.md:1`, `surfaces-r7.md:1`, `surfaces-r8.md:1`, `userspace-oom-killers-r26.md:1`), rc 0; `si_mem_available`, `totalreserve`, `wmark_low`, `folio_is_file_lru`, `34e431b0`, `show_mem.c`: no output, rc 1 each. Identical to `evidence/sweep-memavailable.txt`. |
| 8 | `grep -rl -i "MemAvailable\|si_mem_available" /home/vgpnk/Projects/shokuknow/merge/mori` | no output, rc 1 — the assimilation package holds no entry and no row on MemAvailable |
| 9 | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` (cwd = scratch) | rc 0; **23 `W04`**, 1 `file ok /…/corpus/SOURCES.md`, no `E` code. Diff against `evidence/census-start.txt` (22 `W04`): exactly one line added, `mori W04 S492 duplicate url …/Documentation/filesystems/proc.rst across scopes`; S168's existing `W04` for the same URL stays. |
| 10 | `git cat-file -p 87e0c374:.ufo/waves/round-51/evidence/census-start.txt \| sha256sum` vs worktree | `9209acb3…9cf24` both — the seed receipt is the frozen blob |
| 11 | `git grep -n 'class=env\|class=stale' 87e0c374 -- tools/mori-pin-check.py`; `git cat-file -p 87e0c374:.ufo/waves/round-51/evidence/c1-at-data.txt` | docstring `tools/mori-pin-check.py:136-143` names v5 and the class rule; the receipt prints one `classified: … class=env`/`class=stale` line per fixture, summary `env=2 stale=2`, and `C1=met … classified=ok … exit=0` |
| 12 | `git grep -n 'TMPDIR\|LANE' 87e0c374 -- .ufo/waves/round-40/conform.py` | `:71-72` comment + `LANE = os.path.dirname(…abspath(__file__))` — the lane path is derived from the file's own location |
| 13 | read `corpus/evidence/sources-r51/show_mem.c.v7.2:19-83`; `grep -n` on it | `23:unsigned long totalreserve_pages __read_mostly;`, `32:long si_mem_available(void)`, `47:` free minus reserve, `62:` `pagecache -= min(pagecache / 2, wmark_low);`, `73:EXPORT_SYMBOL_GPL(si_mem_available);` — the row anchor `23,32-73` names what the row's scope says |
| 14 | `sed -n '1120,1145p;1190,1205p' corpus/evidence/sources-r51/proc.rst.v7.2` | line 1124 `MemFree`, 1126–1134 the `MemAvailable` definition, 1138–1141 `Cached` "as well as tmpfs & shmem"; 1192–1201 `Shmem`, `KReclaimable`, `Slab`, `SReclaimable` — anchor `1124-1135,1138-1141,1192-1201` matches |
| 15 | count of the entry's table | `grep -cE '^\|' corpus/knowledge/memavailable-estimate-r51.md` → 23 (header + rule + **21** claim rows); source cells `grep -oE '\| S49[2-6] '` → S492 5, S493 8, S494 3, S495 2, S496 3 = 21; five `source:` lines at 3–7, `verified-at:` 8, `recheck:` 9 |
| 16 | open `https://blog.famzah.net/2014/09/22/know-your-linux-memory-usage/`; `grep -E '[Mm]em[Aa]vailable'` over the fetched text | page opened (2014-09-22, 649 hosts on kernel 3.2.59); one occurrence, a reader's 2017 comment linking `github.com/famzah/linux-memavailable-procfs`; the body never defines `MemAvailable`. `https://blogs.oracle.com/linux/memavailable-less-than-memfree` → HTTP 403, not read. |

No tool installed or upgraded (no pacman transaction; nothing written to a PATH directory). No counter, control,
tool or corpus file was modified; no git/jj mutation in the lane or the fleet repo (only `rev-parse`, `show`,
`cat-file`, `diff`, `numstat`, `status`, `grep`, `archive`-free reads). This seat is not an entailment seat and
wrote no vote-form line; it also did not run `count-c1.py`, `count-c2.py` or either control.

## Draft — `## Gate` of `corpus/lessons/round-51.md`

````markdown
## Gate

### New SOURCES rows (each opened this round; rule 1)

Five rows, all opened 2026-10-26, appended after S491 (`corpus/SOURCES.md:271-275`), 11 cells each, status `mined`,
recheck `on-release`, `used-by corpus/knowledge/memavailable-estimate-r51.md`. The five documents were copied into
`corpus/evidence/sources-r51/` and pinned by sha256 in `evidence/freeze-sha256.txt` (21 lines, 5 of them
`sources-r51`); at the data commit `87e0c374` the five committed blobs hash to exactly the values in the row cells
and in that list (`git cat-file -p 87e0c374:corpus/evidence/sources-r51/<file> | sha256sum`, 5/5 equal), and the
worktree bytes match too. `corpus/SOURCES.md` gains five lines and loses none between the entering tip `aa3af1ec`
and `87e0c374` (`git diff --numstat` → `5	0`), so no earlier row was edited this round and the rule-2
"changed in place" table is empty.

| id | URL / locator | accessed | ≤25-word located quote | decision |
|---|---|---|---|---|
| S492 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst — copy `proc.rst.v7.2` (sha256 `e760f716…af40d126`) | 2026-10-26 | [from ScribeGateQuotes] — the `/proc/meminfo` field block, copy lines 1124-1141 | admit, mined, kind docs, tier A, recheck `on-release`; scope is the `/proc/meminfo` field definitions at v7.2 (MemFree, MemAvailable, Cached, Shmem, KReclaimable, SReclaimable) with anchor `proc.rst:1124-1135,1138-1141,1192-1201`, and explicitly not S082's textual mountinfo layout; the URL and bytes are S082's (`corpus/SOURCES.md:88`, sha256 prefix `e760f716f8278dee`) and the rejected S168's (`:174`), so the row is a **W04** warning, not an error |
| S493 | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/show_mem.c — copy `show_mem.c.v7.2` (sha256 `dba76b26…cb5b02f5`) | 2026-10-26 | [from ScribeGateQuotes] — inside `si_mem_available()`, copy lines 32-73 | admit, mined, kind code, tier A, recheck `on-release`; scope is `si_mem_available()` at v7.2 — the free-minus-`totalreserve_pages` base, the file-LRU pagecache term and the reclaimable-kernel term, each less `min(half, summed low watermarks)`, clamped at zero — with anchor `mm/show_mem.c:23,32-73` (`:23` the reserve variable, `:32` the function, `:73` its `EXPORT_SYMBOL_GPL`), and explicitly not the global OOM report (`__show_mem`) that shares the file |
| S494 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/meminfo.c — copy `meminfo.c.v7.2` (sha256 `d6c58074…46e3deda`) | 2026-10-26 | [from ScribeGateQuotes] — the `show_val_kb`/`meminfo` print path, copy lines 27-31,48-51,56,61-64,105 | admit, mined, kind code, tier A, recheck `on-release`; scope is how `/proc/meminfo` prints its lines at v7.2 — the kB helper, the Cached derivation (file pages minus swap cache and buffers), the MemFree and MemAvailable lines — and explicitly not the estimate's formula (S493) |
| S495 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/mm_inline.h — copy `mm_inline.h.v7.2` (sha256 `2d4accbb…9c45ef6`) | 2026-10-26 | [from ScribeGateQuotes] — `folio_is_file_lru()`, copy lines 13-31 | admit, mined, kind code, tier A, recheck `on-release`; scope is `folio_is_file_lru()` at v7.2 — which folios sit on the file LRU lists and which (anonymous, tmpfs, swap-backed) on the anon lists — which is the page classification the estimate's file-LRU term depends on |
| S496 | https://github.com/torvalds/linux/commit/34e431b0ae398fc54ea69ff85ec700722c9da773.patch — copy `34e431b0.patch` (sha256 `9f571a04…b42563d0`) | 2026-10-26 | [from ScribeGateQuotes] — the commit message, lines 6-27 | admit, mined, kind code, tier A, recheck `on-release`; scope is the 2014 commit that added MemAvailable — its stated motivation (free plus cached overstates startable memory, because Cached holds non-freeable shared memory and tmpfs) and its original formula in the `fs/proc/meminfo.c` hunks; the locator is a commit hash, so the recheck is a byte check, not a moving page |

The claim table these rows feed holds 21 rows, each naming exactly one of the five ids (`grep -cE '^\|'` → 23 =
header + rule + 21; source cells S492 5, S493 8, S494 3, S495 2, S496 3), so all five sources are drawn on and no
row cites an id this Gate does not carry.

### Assimilation (addendum §10) — none this round

Package `/home/vgpnk/Projects/shokunin/shokuknow/merge/mori/` read only; no campaign tool run; nothing written
there. It holds no staged entry and no staged row on MemAvailable — the sweep's tail, re-run read-only during the
wave, is the receipt:

```
$ grep -rl -i "MemAvailable|si_mem_available" /home/vgpnk/Projects/shokuknow/merge/mori
rc=1 (1 = no file)
```

So there is no entry to rewrite, no staged id to renumber or reject, and no §10 1–3-entry cap to spend. The
pre-data sweep over the lane (`evidence/sweep-memavailable.txt`, at `aa3af1ec` over `corpus/SOURCES.md
corpus/knowledge SKILL.md`) reads: `MemAvailable` occurs in seven files, always as a value the lane reads, never as
a definition; `si_mem_available`, `totalreserve`, `wmark_low`, `folio_is_file_lru`, `34e431b0` and `show_mem.c`
occur 0 times; re-run read-only, the same lines and the same per-pattern exit codes (rc 0 for `MemAvailable`, rc 1
for each of the other six). The round's frontier ground is therefore chosen on the lowest axis (depth), not by
assimilation.

- **considerthese:** `considerthese/2026-10-26.md` suggestion 1 ("split pin-check mismatches into 'can't run here'
  and 'stale'") is implemented inside C1. `tools/mori-pin-check.py` v5's docstring carries it (`:136-143`: `env` =
  the pinned command printed no tally for its prefix; `stale` = it ran and printed a different tally, or a tally
  whose exit code contradicts it, or a digest/line-count pin differs; the summary ends `env=N stale=N`), and the
  receipt `evidence/c1-at-data.txt` shows one `classified: … class=env` / `class=stale` line per fixture row
  (2 env, 2 stale, 1 match with no class), summary `env=2 stale=2`, and `C1=met … classified=ok … exit=0`. The
  same diff also removes the residue the suggestion's diagnosis named: `--rev` exports a `git clone --shared` under
  `--scratch`/TMPDIR (`tools/mori-pin-check.py:130-135`) and `.ufo/waves/round-40/conform.py:71-72` derives `LANE`
  from its own path instead of hardcoding it. Suggestions 2–4 of that file have no carrier in the round-51 contract
  and no cell in the data diff (six files: the tool, `conform.py`, `SKILL.md`, `SHONEN.md`, `corpus/SOURCES.md`,
  the entry), so they are not claimed.
- **Census at R:** `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` at the tip whose
  `corpus/SOURCES.md` is `87e0c374`'s bytes → **23 `W04`**, one `file ok …/corpus/SOURCES.md`, **rc 0**, no `E`
  code. The entering census (`evidence/census-start.txt`, blob sha256 `9209acb3…9cf24`, identical at `87e0c374`)
  read **22 `W04`** and `census-rc=0`; the diff between the two lists is exactly one added line, S492's same-URL
  warning (S168's warning for that URL stays). So the round adds exactly one warning and no error: `E04` does not
  fire because the scope differs from S082's.

### Spot-check

The round-51 Gate decisions go to the round-51 non-author closure (`LEARNING.md`), as round 50's did. Sample
offered, three decisions:

- **admit, re-open one:** S493 — open `corpus/evidence/sources-r51/show_mem.c.v7.2` and confirm the anchor names
  what the scope cell says: `:23` `unsigned long totalreserve_pages __read_mostly;`, `:32` `long
  si_mem_available(void)`, `:47` `available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;`,
  `:55-57` `pagecache = … NR_ACTIVE_FILE + … NR_INACTIVE_FILE`, `:62` `pagecache -= min(pagecache / 2,
  wmark_low);`, `:67-69` the reclaimable slab/misc terms under the same `min(… / 2, wmark_low)` cap, `:71-72`
  `if (available < 0) available = 0;`, `:73` `EXPORT_SYMBOL_GPL(si_mem_available);`. Every clause of the teaches
  cell is a reading of those lines, and the scope's negative clause is a boundary inside the same file, so the row
  is admitted on its own range.
- **reject, do not widen:** S082 — its scope cell is "textual mountinfo field layout only"
  (`corpus/SOURCES.md:88`) with anchor `section3.5:1965-2002, field table:1973-1983`, and its `used-by` names two
  admitted closures (`corpus/lessons/round-23.md`, `corpus/knowledge/oom-victim-selection-r27.md`). Widening that
  row to the meminfo block would hand two closures a scope their byte check never covered; the lane instead adds
  S492 for the same URL at the other scope and accepts the W04. `git diff --numstat … corpus/SOURCES.md` → `5	0`
  is the evidence that S082's cells were not touched.
- **reject, a source opened and refused:** `https://blog.famzah.net/2014/09/22/know-your-linux-memory-usage/`,
  opened 2026-10-26. It is a 2014 practitioner write-up over 649 hosts on kernel 3.2.59: it establishes that tmpfs
  is counted in `Cached` and offers a `Total free` formula, but it predates the 3.14 feature and never defines
  `MemAvailable` — the only occurrence of the string on the page is a reader's 2017 comment linking a helper
  repository. Refused: non-primary, no sentence about the estimate to quote, and article and comment text are
  interleaved on the page. A vendor-blog candidate,
  `https://blogs.oracle.com/linux/memavailable-less-than-memfree`, answered HTTP 403 on 2026-10-26; it was not
  read, so it is neither admitted nor refused on content.
````

## Findings

1. **LOW — `evidence/sweep-memavailable.txt` has no per-pattern exit codes.** The receipt
   (`.ufo/waves/round-51/evidence/sweep-memavailable.txt:2-9`) records the `git grep -c` output for seven patterns
   but not each call's rc, so a reader cannot tell "0 occurrences" from "git grep itself failed" for the six empty
   patterns. My read-only re-run gives rc 1 (no match, not an error) for the six and rc 0 for `MemAvailable`, so the
   receipt's reading stands; the missing rcs are a recording gap, not a wrong result.
2. **LOW — `corpus/SOURCES.md:271` (S492) adds a 23rd `W04` warning by design.** The census at the tip whose
   `SOURCES.md` is `87e0c374`'s bytes prints 23 `W04`, one `file ok`, rc 0, and the only line it adds to
   `evidence/census-start.txt`'s 22 is S492's same-URL warning. The lesson must keep the "other scope, W04 warning,
   not an error" wording or a later reader will take it for a defect; S168's warning for the same URL
   (`corpus/SOURCES.md:174`) is unchanged.
3. **LOW — the entry's `recheck:` line is positional.** `corpus/knowledge/memavailable-estimate-r51.md:9` lists five
   URLs then five hashes in the order docs → `show_mem.c` → `meminfo.c` → `mm_inline.h` → the commit patch; the two
   lists match the five `source:` lines and the five `sources-r51` values in `evidence/freeze-sha256.txt` today, but
   a sixth source added to the entry without editing that line (or a reordered hash) would make the recheck print a
   wrong verdict with no counter noticing.
4. **LOW — the entry's body and the row anchor differ by one line on `show_mem.c`.** The prose cites
   `show_mem.c.v7.2:32-72` (`corpus/knowledge/memavailable-estimate-r51.md:15`) while S493's anchor is
   `mm/show_mem.c:23,32-73`; `:73` is the closing `EXPORT_SYMBOL_GPL`, so the anchor covers the function either
   way and no edit is needed — the lesson should quote `32-73` as the anchor, not `32-72`.
