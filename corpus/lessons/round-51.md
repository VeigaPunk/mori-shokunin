# Round 51 lesson

Entering tip `aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd` (round-50 closure); freeze
`4677910eae6df3dabd38fe9a0daf1945146a1110` (contract `.ufo/waves/round-51/contract.md`, both counters, the C1 controls
and witness bytes, receipts, the five source copies); data `87e0c374537557754bf71dd68036ded3ddc6699c`; wave spec
`b504cb1701568a0038aab9d98ec13d28eff801da`. L1 MoriR51, attempt 1. Claims: C1 operability — pin re-execution is
hermetic and says why a pin failed (`tools/mori-pin-check.py` v5, `.ufo/waves/round-40/conform.py`;
`count-c1.py`); C2 depth — what MemAvailable is at kernel v7.2 (`corpus/knowledge/memavailable-estimate-r51.md`,
S492–S496; `count-c2.py`, whose new entailment arm needs a non-L1 wave vote per claim row). One v2 wave `w1`
(68 seats) ran after the data commit, as the contract froze.

## Gate

### New SOURCES rows (each opened this round; rule 1)

Five rows, all opened 2026-10-26, appended after S491 (`corpus/SOURCES.md:271-275`), 11 cells each, status `mined`,
recheck `on-release`, `used-by corpus/knowledge/memavailable-estimate-r51.md`. The five documents were copied into
`corpus/evidence/sources-r51/` and pinned by sha256 in `evidence/freeze-sha256.txt` (21 lines, 5 of them
`sources-r51`); at the data commit `87e0c374` the five committed blobs hash to exactly the values in the row cells
and in that list (`git cat-file -p 87e0c374:corpus/evidence/sources-r51/<file> | sha256sum`, 5/5 equal), and the
worktree bytes match too. `corpus/SOURCES.md` gains five lines and loses none between the entering tip `aa3af1ec`
and `87e0c374` (`git diff --numstat` → `5	0`), so no earlier row was edited this round. Changed in place after the wave (rule 2, in-round rows only, old → new):
S492 scope "S168 was the rejected same-scope duplicate" → "S168 was the rejected same-URL candidate (a duplicate of
S082)" (`w1/Mo51RevSourcesRows.md` LOW 1); S493 anchor is unchanged (`32-73` covers the function and its export).

| id | URL / locator | accessed | ≤25-word located quote | decision |
|---|---|---|---|---|
| S492 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst — copy `proc.rst.v7.2` (sha256 `e760f716…40d126`) | 2026-10-26 | "Calculated from MemFree, SReclaimable, the size of the file LRU lists, and the low watermarks in each zone." (18 words) — `MemAvailable` entry, copy lines 1128-1130 (the quote is also the entry's row-2 quote); the `Cached` sentence the entry's tmpfs claim uses, "In-memory cache for files read from the disk (the pagecache) as well as tmpfs & shmem." (16 words), is at 1139-1140 inside the row's `1138-1141` anchor | admit, mined, kind docs, tier A, recheck `on-release`; scope is the `/proc/meminfo` field text at v7.2 (MemFree, MemAvailable, Cached, Shmem, KReclaimable, SReclaimable definitions), not S082's mountinfo layout (`corpus/SOURCES.md:88`) and not the code that computes the value (S493-S495); same URL and bytes as S082 and the rejected same-scope row S168 (`:174`), so this row is a **W04** warning — informational, separate scope; S082 pins only a 16-hex prefix, so "same bytes" rests on this row's full hash |
| S493 | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/show_mem.c — copy `show_mem.c.v7.2` (sha256 `dba76b26…b02f5`) | 2026-10-26 | "pagecache = global_node_page_state(NR_ACTIVE_FILE) + global_node_page_state(NR_INACTIVE_FILE); pagecache -= min(pagecache / 2, wmark_low);" (11 words) — `si_mem_available()`, copy lines 54-56 | admit, mined, kind code, tier A, recheck `on-release`; scope is `si_mem_available()` at tag v7.2 — free pages minus `totalreserve_pages` (47), plus the active+inactive file LRU pages less `min(half, wmark_low)` (54-57), plus reclaimable slab and other reclaimable kernel pages less the same holdback (64-67), clamped at zero (69-70), with `wmark_low` summed over zones (40-41) — and not the global OOM report `__show_mem()` that shares the file; the quote is the file-cache term and its holdback, the reason the term is not the whole page cache |
| S494 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/meminfo.c — copy `meminfo.c.v7.2` (sha256 `d6c58074…3deda`) | 2026-10-26 | "cached = global_node_page_state(NR_FILE_PAGES) - total_swapcache_pages() - i.bufferram;" (7 words) — copy lines 48-49 | admit, mined, kind code, tier A, recheck `on-release`; scope is the print path: `show_val_kb()` shifting pages by `PAGE_SHIFT - 10` and writing ` kB` (28-32), the `Cached` derivation (48-51, the different base the entry contrasts with the two file LRU lists), and the adjacent `MemFree:`/`MemAvailable:` lines (61-62) where `MemAvailable` prints the value `si_mem_available()` returned at 56; the estimate's arithmetic itself is S493's scope, not this row's |
| S495 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/mm_inline.h — copy `mm_inline.h.v7.2` (sha256 `2d4accbb…c45ef6`) | 2026-10-26 | "0 if @folio is a normal anonymous folio, a tmpfs folio or otherwise * ram or swap backed folio." (19 words) — `folio_is_file_lru()` doc comment, copy lines 25-26; the `*` is the comment's continuation marker at the line break and is part of the located text | admit, mined, kind code, tier A, recheck `on-release`; scope is `folio_is_file_lru()`'s return contract and its one-line body `return !folio_test_swapbacked(folio);` (28-31): file LRU for page-cache folios and MADV_FREE'd anon folios, anon LRU for normal anonymous, tmpfs and swap-backed folios — why the estimate's file-LRU term cannot include tmpfs; the entry's two claims both draw on this block (23-26) |
| S496 | https://github.com/torvalds/linux/commit/34e431b0ae398fc54ea69ff85ec700722c9da773.patch — copy `34e431b0.patch` (sha256 `9f571a04…563d0`) | 2026-10-26 | "It is wrong because Cached includes memory that is not freeable as page cache, for example shared memory segments, tmpfs, and ramfs" (22 words) — commit message, copy lines 11-12 | admit, mined, kind code, tier A, recheck `on-release`; scope is the commit's stated motivation (free plus cached overstates startable memory: Cached holds non-freeable shared memory, tmpfs and ramfs, and omits reclaimable slab, lines 6-14) and its original 2014 formula hunk for `fs/proc/meminfo.c`, not v7.2 behaviour; this is the first row to carry the URL (no W04); the bytes are GitHub's `.patch` rendering (mbox header at line 1), so an `on-release` recheck compares a rendered patch, not a raw blob |

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

## Mistakes

| id | class | evidence | captured-by | fix | shown able to fail |
|---|---|---|---|---|---|
| M1 | hidden location dependence | `tools/mori-pin-check.py` at the entering tip `aa3af1ec` exported the measured tree with `git archive` to `<repo>/.scratch/pin-check-*/tree` (`:884` `scratch_parent = os.path.join(repo, ".scratch")`; export `:844-862`), so a pin that ran `git -C <tree> …` resolved against whichever repository enclosed the export. Three pins do that. `.ufo/waves/round-49/count-c1.py:52-53` sets `LANE` from `__file__` and `:353` runs `git -C LANE rev-parse --verify master^{commit}` (`--rev` defaults to `master`, `:313`), so inside the repo it read the lane tip and the arm passed for the wrong reason. `tools/mori-round19-regressions.py:844` takes `repo = resolved.parents[4]` and `:854` runs `git -C repo show ORACLE_REVISION:…`, which raises `pinned-oracle-unavailable` when that tree has no repository. `.ufo/waves/round-40/conform.py:69` at that tip hardcoded `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"` (scratch under the lane at `:70`) and `:522` runs `git -C repo rev-parse HEAD` with `repo` defaulting to it, so it measured the host lane wherever it ran. Fixture: `git -C <D>/.scratch/exp/tree rev-parse --show-toplevel` printed `<D>` rc 0; the same tree with no enclosing repository printed `fatal: not a git repository` rc 128. Receipt `evidence/control-c1-scratch-only.txt`: `C1=unmet kill_residue=0 relocated=unmet reloc_mismatch=3 classified=bad selftest=pass=114,fail=0`, exit 1 — moving the export out alone turned three pins red. The receipt carries the count only (`count-c1.py:144` writes the per-pin lines to `<scratch>/relocated.out`, removed with the scratch), so "which three" rests on `contract.md` C1 and this code reading, not on a committed per-pin line. | none. Nearest is QUALITY 78 (`corpus/QUALITY.md:357-360`): it binds a counting command to committed bytes and forbids reading a list or fixture from the working directory, and names no check; it never constrains a pin instrument's repository discovery. QUALITY 127 (`corpus/QUALITY.md:1070-1077`) checks only that an instrument carries no absolute host path — its check greps the literal `/home/vgpnk` over `tools/` at a rev, so `.ufo/waves/round-49/count-c1.py` is outside its pathspec, and a file with no absolute path that reaches the lane through `git -C <tree>` is invisible to it. | C1's arms A and B in `tools/mori-pin-check.py` v5 (`87e0c374`). Arm B (relocated): `export_rev` (`:870-887`) measures a `git clone --shared --no-checkout` of the source repo checked out detached at R (`:880-883`) under `--scratch`/TMPDIR (`:912`), so `git -C <tree>` finds the clone's own repository and its `master` — the frozen counter's comment (`.ufo/waves/round-51/count-c1.py:77-78`) says those pins "read `master` from the repository they run in". Arm A (kill residue): the same move takes the export off the measured repo. The lane's `conform.py` now derives `LANE` from `os.path.abspath(__file__)` and puts `SCRATCH_ROOT` at `tempfile.gettempdir()` (`.ufo/waves/round-40/conform.py:71-73`). | Arm B: `evidence/control-c1-do-nothing.txt` (`relocated=unmet reloc_mismatch=1`) and `evidence/control-c1-scratch-only.txt` (`reloc_mismatch=3`) exit 1; `evidence/c1-at-data.txt` reads `relocated=met reloc_mismatch=0` exit 0. Arm A: `control-c1-do-nothing.txt` `kill_residue=12547` (first path `!! .scratch/pin-check-uphozg94/tree/.gitignore`) and `control-c1-conform-only.txt` `kill_residue=12478`; `c1-at-data.txt` `kill_residue=0`. Floor of arm A: `control-c1-class-only.txt` shows `kill_residue=1` is still unmet. |
| M2 | residue producer (round-50 D-d) | The round-50 spot-check named the two producers and routed them: D-d (`corpus/lessons/round-50-verifier-spotcheck.md:45-49`) and routed defect 1 (`:173-174`, `tools/mori-pin-check.py:884-887` and `.ufo/waves/round-40/conform.py:69`). At the entering tip the residue is measured: `evidence/control-c1-do-nothing.txt` carries `kill_residue_first: !! .scratch/pin-check-uphozg94/tree/.gitignore` and `C1=unmet kill_residue=12547 …`, exit 1 — a SIGKILLed `--rev` run left 12547 untracked/ignored paths in the repo it reads, because the export sat at `<repo>/.scratch` (`:884`). `conform.py:70` at that tip put its selftest scratch at `<lane>/.ufo/waves/round-40/scratch` (`:746`, `mkdtemp(prefix="mori-conform-selftest-", dir=SCRATCH_ROOT)`), the untracked debris round-49 M6 recorded; the same in-lane scratch is why a re-execution diverged before rerun (D-d: `conform.py` exited 2 under load). | none, and round 49's fix hid the class. `.gitignore:5` is `.scratch/`; `tools/mori-unlanded-check.py:14` says `.scratch/` and ignored paths are outside its scope "on purpose"; QUALITY 80 (`corpus/QUALITY.md:368-372`) reads `git status --porcelain --untracked-files=all -- .ufo/waves/round-<N>/` only. A transient full tree under `.scratch/` is invisible to every committed check while it exists and gone after the run's own cleanup, and the round-40 selftest scratch would reach QUALITY 80's pathspec only if it outlived the run. | Arms A and B of the frozen P-C1, not a new counter. Arm A (residue): v5's export and its temp dirs live in `--scratch`/TMPDIR (`tools/mori-pin-check.py:911-916`), so a SIGKILL leaves the measured clone's `git status --porcelain --ignored --untracked-files=all` empty. Arm B (relocation): `conform.py`'s `__file__`-derived `LANE` (`:71-72`) and `SCRATCH_ROOT = tempfile.gettempdir()` (`:73`, used at `:746`) move both its measurement and its selftest scratch off the lane. Both arms are frozen in `count-c1.py`'s docstring (`:7-11` arm A, `:12-15` arm B). | Arm A: `control-c1-do-nothing.txt` `kill_residue=12547` and `control-c1-conform-only.txt` `kill_residue=12478` exit 1, `c1-at-data.txt` `kill_residue=0` exit 0, `control-c1-class-only.txt` `kill_residue=1` (any nonzero is unmet, per the contract). Arm B: `control-c1-do-nothing.txt` `reloc_mismatch=1`, `control-c1-class-only.txt` `reloc_mismatch=2`, `control-c1-always-env.txt` `reloc_mismatch=1`, `control-c1-scratch-only.txt` `reloc_mismatch=3`, `c1-at-data.txt` `relocated=met reloc_mismatch=0`. |
| M3 | seat report misrooted to the fleet root | Two wave seats (`Mo51CritEntail12`, `Mo51ConnSiblings`) wrote their reports to `/home/vgpnk/Projects/shokunin/.ufo/waves/round-51/w1/` — the `Report:` trailer is lane-relative and the seat cwd is the fleet root. The orchestrator moved both, bytes unchanged, into the lane at 19:52 -03 and told the L1 (sha256 `351684a6…`, `c85e3277…`); `w1/Mo51ExecMisrootSweep.md` HIGH saw the same window. Until the move, `Mo51ExecEntailHashTool` read "row 12 no vote". | the wave context's absolute-path rule ("every `Report:` trailer path is relative to {lane} — write it at {lane}/<that path>") — present in this wave's context and not followed by two of 68 seats; QUALITY has no criterion | none in the lane: the trailer is rendered by the fleet validator. The L1 checks the fleet root after every wave (`git -C <fleet> status --porcelain`) before integrating, and the report records each move | not yet shown |

## Round-50 routed defects (spot-check §5) — dispositions

The round-50 closure routed six defects (`corpus/lessons/round-50-verifier-spotcheck.md:171-188`). Item by item:
what this round did, where the bytes are, and what stays open.

1. **`.scratch` producers → C1** (`round-50-verifier-spotcheck.md:173-175`). This is exactly this round's C1
   surface, and its predicate is the counter's docstring. At `87e0c374537557754bf71dd68036ded3ddc6699c` the counter
   prints `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0` exit 0
   (`evidence/c1-at-data.txt`), against `C1=unmet kill_residue=12547 relocated=unmet reloc_mismatch=1
   classified=bad selftest=pass=114,fail=0` exit 1 at the entering tip (`evidence/control-c1-do-nothing.txt`, whose
   residue line is `kill_residue_first: !! .scratch/pin-check-uphozg94/tree/.gitignore`). Both producers the
   closure named are changed:
   - `tools/mori-pin-check.py` — entering `:884` read `scratch_parent = os.path.join(repo, ".scratch")`; v5 makes
     the `--rev` export a `git clone -q --shared --no-checkout` plus `checkout -q --detach` under `--scratch DIR`,
     defaulting to the TMPDIR temp dir and "never `<repo>/.scratch`" (`tools/mori-pin-check.py:880-886,901,136-142`),
     and gives every mismatch line `class=env` or `class=stale` with the summary ending `env=N stale=N`, `env=2`
     `stale=2` over the frozen five-row fixture (`:136-142`).
   - `.ufo/waves/round-40/conform.py` — entering `:69-70` hardcoded `LANE = "/home/vgpnk/Projects/shokunin/
     mori-shokunin"` and `SCRATCH_ROOT = os.path.join(LANE, ".ufo", "waves", "round-40", "scratch")`; at the data
     commit `LANE` is four `dirname`s of `__file__` and `SCRATCH_ROOT = tempfile.gettempdir()`.
   What the claim does not cover, named before data: arm A kills at one moment only (3 s after the first write) and
   proves nothing about a kill at another moment; arm B hides one path (the lane) and does not prove portability to
   another host, user or kernel; arm C's fixture is five rows and its rule is "no tally line ⇒ env", so a tool that
   prints a tally and then fails environmentally is classed `stale`; and `--root` mode still writes
   `<root>/.scratch` (`tools/mori-pin-check.py:542`), so a closure that re-executes with `--root` against the lane
   refills it. The producer is closed on the `--rev` and `conform.py` paths the closure named, not on every path;
   the `--root` residue stays a named limit of the claim.

2. **Round shape → one v2 wave after the data, as frozen** (`round-50-verifier-spotcheck.md:176-178`). Measured
   against the contract (`contract.md:121-122,127-133`): wave `w1`, `counts={"spawn":68,…,"total":68}`, against the
   v2 policy band `waveMinLanes 64` / `waveMaxLanes 128`; registry created 19:42:41 and the wave stamped
   dispatched 19:48:42, both after the data commit `87e0c37…` (author 19:37:01, committer 19:37:45); one wave and no
   second; 68 is under the closure's 100-seat ceiling and under the contract's 128 cap; attack share is 29/68 = 43 %
   (reviewer 14, critic 12, mutation-tester 3) against the 25 % floor. The contract states two seat bands that part
   company above 100 (`:121-122` "w1 (64–100 seats)" versus `:129` "band 64–128"); 68 is inside both, and the
   disagreement can only bite on a residual call, where `LOG.md` must say which ceiling was used.

   **The 35 attempt-1 seats: outcome unknown, not dead.** The round-50 lesson already says "unknown (not dead, not
   complete)"; this round closes it with what the record actually holds. Knowable:
   - the wave ramped rather than spawning at once. `.ufo/state/inline-dispatcher.log:1569-1603` shows 21 spawned at
     05:50:20 and three seats deferred by the host job cap before the wave completed —
     `Mo50CritC2Counter` (05:52:27-05:54:27), `Mo50CritStagedClaims` (05:55:28-05:56:28) and
     `Mo50ConnConsiderthese` (05:57:49) — reaching `spawned mori 50 w1 40` at 05:58:49. So the
     `w1.ready.dispatched` stamp (05:58:49) is when the wave finished spawning, not when it started: the first
     landed report, `Mo50ScoutCoverageFR1.md`, was written 05:51:24, 7m25s earlier. `corpus/lessons/round-50.md:196`
     and `:252` read "dispatched … at 2026-10-26T05:58:49"; that is the stamp, and the wave ramped.
   - five reports exist, mtimes 05:51:24-06:08:03, all committed by the orchestrator salvage `9b8562a3`
     (`git log --diff-filter=A` per file → one commit).
   - the same log's live count for the wave falls 39/40 (05:59:19) → 38/40 (06:05:05) → 37/40 (06:09:06) and holds at
     37/40 through its last tick 06:22:15; it records no tick until 08:29:36, where the restarted dispatcher
     `adopted` the wave file and recorded no further spawn for it.
   - the L1 died in the host crash: `.ufo/watchdog.log:1518` `lane-dead-no-report mori round=50 … attempt 1 L1 died in
     the orchestrator host crash 2026-10-26 ~08:50 -03`, and `.scratch/goal-20261026-hyaku-run8.md:85` says the omp
     exit "ended every live agent: L1s SoujiR32, TabiR31, TameshiR48 and MoriR50, plus their seats".
   - settlement is filesystem shape only. `tools/mori-wave-settlement.py scan --lane-root <lane>` on the committed
     tree: `.ufo/waves/round-50/w1-dispatch.json members 40 … present 5, missing 35, stub 0, misrooted 0, unsafe 0,
     unparsed 0`; the tool's docstring says outright "A missing report is not a dead seat; this tool reports
     filesystem shape only" (`tools/mori-wave-settlement.py:18`).
   - no per-seat identity was recorded: `w1/swarm-registry.json` has `agentId: null` for all 40 members, and no
     `.ufo/waves/round-50/w1-results.json` exists; `a2w1-results.json` is attempt 2's, 64 seats and 64 results,
     written 10:50:12 — after the critic that reported it missing at 09:56, so that critic sentence was true when
     written and is stale now.
   - no per-seat remnant survives: all five landed reports name scratch under
     `/fast/scratch/hyaku/mori-r50/<seat>/`, and that root is gone today (`ls /fast/scratch/hyaku | grep mori` →
     `mori-r51` only). Attempt-2 seats removed their own scratch by design (`a2w1/Mo50bConnSalvage.md:11`), so
     absence today is not evidence that the root was never used.
   Not knowable, and not to be asserted: whether a named seat started, took a turn, wrote and lost a draft, or
   finished with nothing to show. The record keeps counts, not names; "unknown" is the finding, and "dead" would be
   an invention.
   The work itself was mostly re-attempted: 25 of the 35 items carry the same item name in `a2w1`, 8 more were
   re-tasked under a different name for the same intent (three quote inventories → six `RevRows*` reviewers;
   `ScribeRowCgroup`, `ScribeAxesCells`, `ScribeShonen` → the landed data plus `RevRowsCgroup*`, `RevAxesCells`,
   `RevShonen`; `ExecHostPaths` → `SentHostPaths`/`ExecMisrootSweep`; `ConnConsiderthese` → the considerthese lines
   in `ScribeLessonGate`/`RevPromptConformance`), and 2 were never re-attempted and left nothing:
   `Mo50ExecSelfassessTool` (a candidate standing C1 tool) and `Mo50ExecCensusMirror` (the scratch
   mirror-validation harness) — no `mori-selfassess-check.py` and no `mirror-validate.sh` anywhere in the tree at
   `87e0c37…`. Those two are dropped, not deferred, and the round-51 record says so.

3. **Successor C1 counter and K4 beyond SHONEN → not done this round; routed to round 52**
   (`round-50-verifier-spotcheck.md:179-181`). The contract routes it in as many words: "3 successor calibration
   counter and K4 beyond SHONEN → not claimed this round (stays routed to round 52, named in `LOG.md`)"
   (`contract.md:122-123`). The reason is the freeze rule itself — "A predicate, counter, floor or kill rule changed
   after any seat has scored is not the claim's rule" (`contract.md:6-7`) — and the round's two claims are
   operability (C1) and depth (C2); a successor calibration counter would be a calibration-axis instrument, and
   this round's C1 instrument reads no `SCORECARD.md`, no `## Axes` row, no Score cell and no `QUALITY.md`/`LOG.md`
   pin (`grep -c 'SCORECARD\|Axes' .ufo/waves/round-51/count-c1.py` → 0), so nothing here re-tests the five
   survivors the closure named or closes K4 outside `SHONEN.md` (round 50 closed K4 for `SHONEN.md` only,
   `corpus/lessons/round-50.md:230-235`). Both stay open; this sentence is the deviation `LOG.md` must carry under
   item 5.

4. **C2 entailment → the entailment arm of P-C2** (`round-50-verifier-spotcheck.md:182-183`). Implemented inside the
   frozen predicate: for every row of `corpus/knowledge/memavailable-estimate-r51.md`, the wave report files at R
   under `.ufo/waves/round-51/w1/` whose names do not start `MoriR51` must carry at least one vote line of the form
   `ENTAIL <h> entailed` and no dissent line `ENTAIL <h> overclaim`, where `<h>` is the first 12 hex of the sha256 of
   the row's claim cell with whitespace collapsed and ends stripped (`count-c2.py:14-18`, reader at `:117-130`, hash
   at `:113-114`). The votes are in flight as this is written: at the data commit the entry reads
   `claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0
   dissent=0` with `failed=entailment`, exit 1 (`evidence/c2-at-data.txt`) — located quotes with no recorded
   judgment do not meet P-C2. The wave pairs every row with two seats of different roles: seven reviewers
   `Mo51RevEntail01…19` (rows 1-3 each, 21/21) and four critics `Mo51CritEntail01…17` (rows 1-6, 7-11, 12-16, 17-21,
   21/21), a design seat `Mo51CritEntailArm`, and a hash-recomputation seat `Mo51ExecEntailHashTool`. The counter
   accepts one vote and no dissent, so "at least two seats of different roles" (`contract.md:131`) is a round-shape
   rule the predicate does not check — that gap is a named limit of P-C2, not something the L1 may close by editing
   a frozen counter. An `overclaim` blocks the row until the L1 replaces the claim text with text a
   non-L1 seat voted `entailed`; the old hash then matches no row and no vote line is ever deleted from a report.

5. **Contract deviations named in the record** (`round-50-verifier-spotcheck.md:184-185`). Rule for this round: a
   deviation from `contract.md` is named in `LOG.md` and in this lesson, in the same breath as the item it deviates
   from — not only in the lesson, which is the defect round 50 hit. The deviation the contract already commits to is
   item 3 above (a routed defect not worked). The carrier for the rest is `LOG.md`'s `## Round 51` entry; at
   drafting, `LOG.md` has no `## Round 51` heading (`grep -c '^## Round 51' LOG.md` → 0; its last entry is
   `## Round 50` at `:2732`), and the entry is being drafted by `Mo51ScribeLogScorecard`. Two candidate deviations
   the entry must state if they stand at filing: item 3 above, and the contract's own two seat bands (item 2) if a
   residual call takes the round past 100 seats.

6. **Fleet-owned author date → the operator's** (`round-50-verifier-spotcheck.md:186-188`). The mechanism is
   unchanged and is fleet code: `scripts/hyaku/fleet-commit.sh:84-85` stamps the author before committing —
   "`jj commit <paths>` keeps @'s author: stamp it first so author == committer", `jj metaedit --update-author` —
   and the stamp is the working-copy change's creation time, so a filing commit can be authored before the lane tip
   it cites. Round 50 shows both sides in one round: the first filing `4a20abb1` is authored 10:15:47 against a tip
   committed 10:54:21 (the defect), and the second filing `e9833c0f` is authored 10:54:42, after the tip. The lane
   cannot fix this, and this round claims nothing about it: the report records both values (its own author date and
   the cited lane tip's committer date) as the surface, the way round 50 did. Routed to the operator, unchanged.

Status of the six: 1 → the C1 claim; 2 → done as frozen, with the 35 attempt-1 seats closed as "outcome unknown,
not dead"; 3 → not done, routed to round 52 and named; 4 → the C2 claim's entailment arm; 5 → the rule plus this
entry's copy; 6 → operator's, unchanged.

## Wave w1 — integrated findings

Taken into the data after the wave (the counters, predicates, controls and kill rules stay frozen):

- C2 entry: four claim rows replaced by the text the voting seat proposed and voted `entailed` — row 6
  (`Mo51CritEntail01`: "the pages the kernel holds back from userspace allocations" is not in `show_mem.c`), row 12
  (`Mo51RevEntail10`: "the line reads zero" is S494's fact, not S493's), row 14 (`Mo51RevEntail13`, also
  `Mo51CritEntail12`: not every meminfo value goes through `show_val_kb`), row 15 (`Mo51RevEntail13`: the "two file
  LRU lists" comparison is not in S494). For row 14 two seats proposed replacements; `Mo51RevEntail13`'s
  (`6c2327e19df1`) landed, `Mo51CritEntail12`'s (`56b7a3309d66`) did not. Their dissent lines stay in their reports;
  they no longer match a row.
- C2 prose: the intro's "pressure probes print MemAvailable/MemTotal" was false — only the census fill arm does
  (`Mo51SentEntryScope` MED 1); the dispatcher sentence now names the fleet-owned files (`Mo51SentEntryScope` MED 2,
  `Mo51ScoutPriorMentions`); "Units are kB on every meminfo line" was false (`Mo51CritReadingRules` HIGH); the
  unsourced free-swap sentence was cut (LOW); "same shape since 2014" was replaced by the dated input changes
  (`Mo51ExecPatchVsV72` MED, `Mo51CritReadingRules` MED); the `totalreserve_pages` sentence now says what a
  host recomputation needs, after `Mo51ExecHostMeminfo` reproduced `MemAvailable` to the page at four of five
  samples with `/proc/zoneinfo`; `watermark_boost` and the non-atomic read are named; the tsukuroi boundary now
  matches its PROVINCE (`Mo51SentEntryScope` LOW 3); a `## What this changes for mori` section
  (`Mo51ScribeWhatChanges`, `Mo51ScoutPriorMentions`).
- S492 scope wording (`Mo51RevSourcesRows` LOW 1).
- C1 tool, v5 → v5.1: the default scratch was `tempfile.gettempdir()`, so a bare `--rev` run put a ~330 MB tree
  in `/tmp` against the 2026-10-25 directive (`Mo51SentKillSafety` HIGH 1, `Mo51RevPinCheckDiff` MED,
  `Mo51RevenScratchProducers` MED 3) — now `--scratch`, else a TMPDIR outside the repo, else `/var/tmp`, and a
  `--scratch` inside the repo exits 2 (`Mo51RevenScratchProducers` HIGH 1); the measured tree's `master` was the
  source's live branch, so a pin reading `master` measured something other than R (`Mo51CritExportClone` MED,
  `Mo51ExecPinCheckLaneRev` MED) — now `master` is R; classes: an absent instrument file, disagreeing tally lines
  and a different tally printed before a timeout are `stale`, the pinned tally then a timeout is `env`
  (`Mo51CritClassRule` HIGH ×2, MED ×2); the stale `git archive` sentence in the Modes paragraph
  (`Mo51ExecPinCheckLaneRev` LOW). Six selftest arms added (119 → 125), two of which kill the mutants that
  survived the v5 selftest (`Mo51MutPinCheckV5` F1 default-scratch revert; the master arm).

Named limits, not repaired (frozen counters; a weakness found after scoring is a limit):

- `count-c1.py`: arm A measures residue at one moment, so a tool that delays its in-repo write past 3 s scores 0
  (`Mo51CritC1Counter` HIGH); arm A runs the revision's code unsandboxed and checks only the clone
  (`Mo51SentBwrap` HIGH 1); arm B checks exit code and the last line, so a stub or a lane-path short-circuit passes
  (`Mo51CritC1Counter` HIGH); arm D parses the printed tally (a selftest that prints without running passes);
  arm C's five prefixes can be hardcoded; bwrap is a one-path mask with the caller's environment and network
  (`Mo51SentBwrap` MED 2); the controls cannot be replayed from a copy outside the lane (`Mo51ExecC1Controls`
  MED); `--root` mode and other lane writers (round-39 `conform.py`, round-48/49 `count-c1.py` scratch under
  `<repo>/.scratch`) are outside C1 (`Mo51RevenScratchProducers` MED 4-6, `Mo51RevPromptConformance` F1).
- `count-c2.py`: any `.md` under `w1/` not named `MoriR51*` can vote, lines inside fences count, and one vote meets
  the arm (`Mo51CritC2Counter` HIGH ×2, `Mo51CritEntailArm` F1); nothing binds committed reports to what seats
  wrote except the commit itself and the wave results file (`Mo51CritEntailArm` F2). The L1 receipt
  `evidence/entail-voters.txt` lists every vote line with its file and checks that only the eleven ENTAILMENT
  seats wrote vote lines; the closure can compare the committed reports with `w1-results.json`.
- v5.1 class rule: a tally printed before a crash on a missing host path is still `stale`; an ImportError of a
  repo-local module is `env` (`Mo51CritClassRule`).
- Fleet-owned, routed to the operator (mori never edits them): `scripts/hyaku/inline-dispatcher.py:133` fails open
  on an unreadable `/proc/meminfo`, its `MEM_MIN_GB` is GiB, and the two hyaku gates hold different floors (4 GiB
  vs 6144 MiB) on the same line (`Mo51ExecDispatcherGate` MED 1-3).
- Sibling: tsukuroi's `kill-oom-boundary-r33.md:30` grounds an exclusivity cell on "Shmem not named" by mori; this
  entry now names Shmem — adjoins, no conflict; tsukuroi's next adjacency pass should re-read it
  (`Mo51ConnSiblings` HIGH).

## Round shape

One v2 wave `w1` (policy v2, validated rc 0): 68 seats — executor 18, reviewer 14, critic 12, scribe 9, sentinel 4,
mutation-tester 3, connector 3, scout 2, simplifier 2, revenger 1; m_flash roles 34/68, attack roles 29/68. No
residual call. The L1 held the planner seat (the validator rejects `planner`). Seat outcomes are in the round report.
