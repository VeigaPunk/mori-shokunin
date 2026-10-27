# Round 53 lesson

Entering tip `20edafa59b38dac1ca358893f0259b1f436372d3` (round-52 closure, admitted); freeze
`f4da3fd400fa88a6db8ea544a4f7045c15d2410e` (contract `.ufo/waves/round-53/contract.md`, both counters with selftests,
`controls/` and ten control receipts, census-start, sweeps, twelve source copies); data
`2a4213bf8da72f7cd78189baa5bb9be825dca1df`; wave spec `95cf78eef71979f9b740ef6bc3c5299b6beff86e`; data corrections
after the wave `fd86307ad54c13edb8b6dd13182a2ad196f42fcd`. L1 MoriR53, attempt 1. Claims: C1 freshness — the 46
v7.2-pinned claim rows of the round-51 and round-52 entries re-verified at Linux v7.3 (ledger
`corpus/knowledge/kernel-v7.3-recheck-r53.md`, S502–S510, `count-c1.py` with a two-voter RECHECK arm); C2 coverage —
the commit ledger as a runway surface read by `tools/mori-commit-runway.py`, by overcommit mode and, under mode 2,
against the per-CPU error band (`count-c2.py`: 16 frozen and 64 seeded fixtures against a reference reading, the
tool's selftest, a SKILL registry row and a live leg; entry `corpus/knowledge/commit-runway-read-r53.md`,
S511–S514). One v2 wave `w1` (67 seats) ran after the data commit, as the contract froze.

## Gate

### New SOURCES rows (each opened this round; rule 1)

Thirteen rows, all opened 2026-10-26, appended after S501, 11 cells each, status `mined`, recheck `on-release`.
S502–S510 (`used-by corpus/knowledge/kernel-v7.3-recheck-r53.md`) are the nine paths the round-51/52 claim rows cite,
at tag v7.3 from git.kernel.org cgit; S511–S514 (`used-by corpus/knowledge/commit-runway-read-r53.md`) are the band
sources. Copies under `corpus/evidence/sources-r53/`, pinned in `count-c1.py` (V73) and
`.ufo/waves/round-53/evidence/freeze-sha256.txt` (S514's copy came after the freeze; its sha256 is in its row).
Quotes located by `w1/Mo53ScribeGate.md` with a substring test that joins comment-decorated line breaks (12/12
found); S514's quote by the L1 (`mm_init.c.v7.3:198-199`).

| id | URL / locator | accessed | copy sha256 (full) | ≤25-word located quote | decision |
|---|---|---|---|---|---|
| S502 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/filesystems/proc.rst?h=v7.3 — copy `proc.rst.v7.3` | 2026-10-26 | `bc178ff511e05c1b5e0c2413feb18223edcaeb2797ce499b714b98120cabf3c8` | "An estimate of how much memory is available for starting new applications, without swapping." (14 words, `:1128-1129`) | admit, mined, tier A docs |
| S503 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/show_mem.c?h=v7.3 — copy `show_mem.c.v7.3` | 2026-10-26 | `c50205bc19974566d7bfe1c161f253cf71321c06ecc1327abb2a775be8a0de71` | "Estimate the amount of memory available for userspace allocations, without causing swapping or OOM." (14 words, `:45-46`) | admit, mined, tier A code |
| S504 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/proc/meminfo.c?h=v7.3 — copy `meminfo.c.v7.3` | 2026-10-26 | `d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda` | `show_val_kb(m, "Committed_AS:   ", committed);` (4 words, `:126`; CommitLimit one line above at `:125`) | admit, mined, tier A code |
| S505 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/mm_inline.h?h=v7.3 — copy `mm_inline.h.v7.3` | 2026-10-26 | `277e99e23ecc1b5babfdf041e7e7e3f9d280113b3b0a9f7e8340c0e13d7b391b` | "0 if @folio is a normal anonymous folio, a tmpfs folio or otherwise ram or swap backed folio." (18 words, `:25-26`) | admit, mined, tier A code |
| S506 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/mm/overcommit-accounting.rst?h=v7.3 — copy `overcommit-accounting.rst.v7.3` | 2026-10-26 | `767ab88153c4494e54fcf2db4e5bd01921d6bd8350f1596ada508cb5e4b4927f` | "The total address space commit for the system is not permitted to exceed swap + a configurable amount (default is 50%) of physical RAM." (24 words, `:20-22`) | admit, mined, tier A docs |
| S507 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/sysctl/vm.rst?h=v7.3 — copy `vm.rst.v7.3` | 2026-10-26 | `f81feb3dfca5f054cf8b76c71d7a4525a88d629d3ea8239743996b9d87bb391b` | "When this flag is 0, the kernel compares the userspace memory request size against total memory plus swap and rejects obvious overcommits." (22 words, `:839-840`) | admit, mined, tier A docs |
| S508 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/util.c?h=v7.3 — copy `util.c.v7.3` | 2026-10-26 | `4dfcce2b8fa8f18c350565950a10248b3590e3d3c0c9335fef6d47daa7a9e1f2` | `if (percpu_counter_read_positive(&vm_committed_as) < allowed) return 0;` (6 words, `:994-995`) | admit, mined, tier A code |
| S509 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/mman.h?h=v7.3 — copy `mman.h.v7.3` | 2026-10-26 | `d7bf787c910d9a7cbabee3a50c512ce3aad78d63659b0c968adca16b5916b058` | "static inline void vm_acct_memory(long pages) { percpu_counter_add_batch(&vm_committed_as, pages, vm_committed_as_batch); }" (10 words, `:76-79`) | admit, mined, tier A code |
| S510 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/mmap.c?h=v7.3 — copy `mmap.c.v7.3` | 2026-10-26 | `8e51fb1c10fee6943c9edc26b72952137b4098b00cc050ea1e6ade6e27197feb` | "if (flags & MAP_NORESERVE) { /* We honor MAP_NORESERVE if allowed to overcommit */ if (sysctl_overcommit_memory != OVERCOMMIT_NEVER) vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);" (20 words, `:563-566`) | admit, mined, tier A code |
| S511 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/mm_init.c?h=v7.2 — copy `mm_init.c.v7.2` | 2026-10-26 | `ed691b24afbc0dc45090e149d115d707af0c5f7369a10b7722d491075f26a754` | "For policy OVERCOMMIT_NEVER, set batch size to 0.4% of (total memory/#cpus), and lift it to 25% for other policies" (19 words, `:199-200`) | admit, mined, tier A code |
| S512 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/lib/percpu_counter.c?h=v7.2 — copy `percpu_counter.c.v7.2` | 2026-10-26 | `2c26e67751f939dfb21ff6221884280ae84a2a94a54de4468fb9dc8746130d6d` | `if (unlikely(abs(count + amount) >= batch)) {` (7 words, `:100`) | admit, mined, tier A code |
| S513 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/percpu_counter.h?h=v7.2 — copy `percpu_counter.h.v7.2` | 2026-10-26 | `4a107bc381b3b5425b8ff441f7487d97ba6883dc6f5b426c4bd361ad7cbef896` | `static inline s64 percpu_counter_read_positive(struct percpu_counter *fbc)` (6 words, `:118`) | admit, mined, tier A code |
| S514 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/mm_init.c?h=v7.3 — copy `mm_init.c.v7.3` | 2026-10-26 | `678410005f881a64ae94d180c82174dc4474679b056ace69b6bc3d23978f976c` | `s32 nr = num_present_cpus(); s32 batch = max_t(s32, nr*2, 32);` (10 words, `:198-199`) | admit, mined, tier A code (opened at integration after the wave found the band entry naming an unpinned v7.3 copy) |
| — | https://raw.githubusercontent.com/torvalds/linux/v7.3/… (the same nine v7.3 paths) | 2026-10-26 | `mm/util.c` returned 43965 bytes, sha256 `4dfcce2b…9e1f2` (byte-identical to the S508 copy); `include/linux/mman.h` returned HTTP 429 in the same session | — | **reject**: the host throttles per path (three 200s and one 429 in one sitting, and the L1's opening fetches got 429), so a row opened there cannot claim a stable locator for the bytes it quotes; the cgit `plain/<path>?h=v7.3` endpoint serves the same bytes and answered for all nine. Flip: every cited v7.3 path answers 200 with sha256 equal to the frozen cgit copy on the day it is opened — then raw is admissible as a second locator for these rows, never as a new row |
| — | https://www.kernel.org/doc/html/latest/admin-guide/sysctl/vm.html (rendered docs, `latest`) | 2026-10-26 | HTTP 200, 69002 bytes, sha256 `423d0434…42efa`; the page renders `<p class="blurb">7.3.0</p>` | the page carries the S507 sentence today ("rejects obvious overcommits") | **reject**: `latest` moves with each release (it renders 7.3.0 today, not the v7.3 bytes the rows pin tomorrow after v7.4), so a quote located there proves nothing pinned; S507's raw tag copy carries the same text. Flip: a release-pinned rendered URL (`/doc/html/v7.3/…`) would be admissible as a second locator for S507, not as a new row |

Independent channels: `w1/Mo53ExecRefetchGit.md` fetched the nine v7.3 paths from github (blob-filtered `git fetch`
of `refs/tags/v7.3`) — all byte-identical to the cgit copies; `w1/Mo53ExecRefetchCgit.md` re-fetched all twelve from
cgit — all equal to the pins; `w1/Mo53ExecTagCommit.md` confirmed tag `091b0638…` → commit `c03c1a14…`, `Linux 7.3`,
tagged 2026-10-18 13:14:58 -1000. This closes the contract's named limit "the pins prove the bytes are what the L1
fetched from cgit, not that cgit served the tag" for the nine v7.3 paths.

### Rows touched old→new (rule 2: status, recheck, used-by in place; in-round anchor corrections logged)

- S499 `used-by`: `corpus/knowledge/overcommit-commit-limit-r52.md` → `corpus/knowledge/overcommit-commit-limit-r52.md,
  corpus/knowledge/commit-runway-read-r53.md` (the band entry cites `util.c.v7.2`).
- In-round corrections to rows opened this round (the round-52 precedent, `corpus/lessons/round-52.md` Gate), each
  from `w1/Mo53ExecAnchorCheck.md` §4 and checked against the copy: S502 anchor `meminfo section lines 1043-1240 (…,
  Committed_AS 1239)` → `1043-1302 (…, Committed_AS 1239-1251)`; S503 teaches gains the two printk format flips and
  the `(unsigned long)` cast; S504 anchor gains `show_val_kb helper 28-32`; S505 anchor `folio_is_file_lru at line 28`
  → `folio_is_file_lru kernel-doc and definition 13-31 (function at 28)` and teaches gains the two
  `memdesc_section(&cur_page->flags)` call sites; S507 anchor title lines → section ranges `82-108, 823-831, 834-856,
  859-886, 1106-1123`; S508 anchor gains `sysctl_overcommit_memory/ratio/kbytes defaults 781-783` and
  `overcommit_policy_handler 806-840`, teaches gains the two `vma_start_pgoff(vma)` conversions; S511 scope `(the host
  kernel line)` → `(the copy is the upstream v7.2 tag 237a1c39e8df; the host runs the 7.2 line, 7.2.11-arch1-1, whose
  own bytes are not in evidence)`; S512 anchor `(SMP path)` → `(the CONFIG_HAVE_CMPXCHG_LOCAL branch, guarded at line
  87; the alternative body at 114-137 under #else)`. Pre-correction bytes: `git show 2a4213bf:corpus/SOURCES.md`.

### Assimilation (addendum §10) — none this round

`grep -rilE 'overcommit|CommitLimit|Committed_AS|percpu_counter|v7\.3' /home/vgpnk/Projects/shokuknow/merge/mori | wc -l`
→ 0 (`.ufo/waves/round-53/evidence/sweeps.txt`): the package stages nothing on either claim's ground.

### Spot-check

Pending the non-author closure (LEARNING.md: a seat this lane dispatched is still the lane). Candidates: admit S510
(the respelled MAP_NORESERVE block) and reject the raw.githubusercontent.com v7.3 locator.

## Mistakes

- M1: number-drift — a claim row's tally was transcribed from the *earlier* receipt and then the cell was pointed at
  the *later* one. `SCORECARD.md:2746` (round-52 C1 row) After cell reads `C1=met items=42 … locators=27`, rc 0 —
  `evidence/c1-at-landed.txt`; the receipt at that path prints `C1=met items=43 … locators=28 …
  rev=e7e056b8a17e54516a3c17798221c30e9902c250` (`.ufo/waves/round-52/evidence/c1-at-landed.txt:45`), while 42/27 is
  verbatim the at-data receipt (`evidence/c1-at-data.txt:44`, `rev=8524904a…`) written before the row. Evidence:
  the two receipts and the row above; `corpus/lessons/round-52-verifier-spotcheck.md` D2 for attribution (the row was
  written at integration `2f245af7`, before `c1-at-landed.txt` existed). Captured-by: none — no instrument compares a
  claim-table row with the receipt its own cell names: `count-c1.py` reads no `SCORECARD.md` byte (grep for
  `SCORECARD` in both round-53 counters → 0 hits), QUALITY 141 scopes living pins to `corpus/QUALITY.md` and
  `corpus/README.md`, QUALITY 142 scopes pointers to `## Axes` and the SHONEN boxes, and the SCORECARD-reading tools
  (`tools/mori-routed-check.py`, `tools/mori-round41-calibration.py`, `tools/mori-census.sh`) read other cells. The
  non-author closure found it by reading. Fix (proposed, routed to round 54 — no frozen counter changes this round): a
  row-vs-citation arm that parses each After cell's `C1=…` span and the verdict line of the file the same cell names,
  and requires every `k=v` of the row to occur in that receipt with the same `v`. Shown able to fail by a seat probe
  over the two neighbouring rows: round-51's row (`SCORECARD.md:2716`, `kill_residue=0 relocated=met reloc_mismatch=0
  classified=ok selftest=pass=125,fail=0`) reads `MISMATCH 0` against `.ufo/waves/round-51/evidence/c1-at-landed.txt`,
  round-52's row reads `MISMATCH 2: {'items': ('42','43'), 'locators': ('27','28')}`. The appended correction line of
  routed defect 1 is not in the tree at the data commit `2a4213bf` or at lane HEAD `95cf78ee` (grep for `items=42`,
  `42/27`, `43/28` finds only the row itself; `corpus/README.md` `## Round-52 corrections` covers living pins only).

- M2: landing — `[FILL]` left where the report's own commit hash belongs, and the placeholder row duplicated a real
  one. Fleet report `.ufo/reports/round-52/mori.md:5` ends ``Report commit `[FILL]`.``; `:46` is the table row
  `` | `[FILL]` | receipts at landed tip: `c1-at-landed.txt`, `c2-at-landed.txt`, `census-end.txt` | Round 52 | ``,
  identical in description to `:45`'s `37af57f2` row. The hash that exists is
  `aacd7a83027cdee8e950a2c39d490feaed3be13c` (`mori-shokunin <mori@shokunin.local> 2026-10-26T21:56:32-03:00`,
  `git log --format=%H -- .ufo/reports/round-52/mori.md` on the fleet repo). Evidence: those two lines; closure D1.
  Captured-by: none — QUALITY 9 states the obligation ("a report names the commit that carries its work") and no
  instrument reads report bytes; the closure found it. Fix: the round-53 convention, landed as a convention and not
  as an instrument — the report names its own commit by command, never by placeholder:
  `git log --format=%H -- .ufo/reports/round-53/mori.md` on the fleet repo, run after the report's commit (contract
  §Round-52 closure routed defects 2). Shown able to fail by a placeholder arm: `grep -rl '\[FILL\]'
  .ufo/reports --include='mori.md'` exits 0 on the round-52 report (2 hits) and finds 0 hits in the other 41 of 42
  mori reports, so the check fails exactly where the convention was broken and passes everywhere else. Not covered:
  the arm reads the placeholder token only; a report that names no commit at all passes it.

- M3: stale premise — an `on-release` recheck was authored *after* its release had been tagged, and the trigger sat
  unanswered for two rounds. `corpus/knowledge/memavailable-estimate-r51.md:9` and
  `corpus/knowledge/overcommit-commit-limit-r52.md:9` carry `recheck: on-release` over v7.2 URLs and both are
  `verified-at: 2026-10-26`; the release is older: cgit `tag/?h=v7.3` prints `tag date 2026-10-18 13:14:58 -1000`,
  `tag name v7.3 (091b06388b117fefdcb63336ac09956a4914b961)`, `tagged object commit c03c1a1450…`, message
  `Linux 7.3` — eight days before both entries. The lane's own bytes carried the sign twice and neither was followed:
  `LOG.md:2054` (round 32) records `docs.kernel.org renders 7.3.0`, and the round-52 wave seat wrote the banner
  difference into its rejection of the `latest` locator (`.ufo/waves/round-52/w1/Mo52ScribeGate.md:139-148`:
  `latest-overcommit-accounting.html:7.3.0`; `:202`: "the banner has already done (7.2.0 → 7.3.0) while the row's
  claim stayed at v7.2") without turning it into a recheck of its own v7.2 pins. The entering tip holds no recheck:
  `git grep -c -E 'v7\.3|7\.3\.0' 20edafa5 -- corpus/knowledge corpus/SOURCES.md SKILL.md` → exit 1, no match
  (`evidence/sweeps.txt:7-8`). Evidence: the two `recheck:` lines, the tag page, the two in-lane sightings, the sweep.
  Captured-by: none before round 53 — the `recheck:` line is prose and no instrument reads a kernel tag
  (`count-c1.py:6` asserts "that trigger has fired" as a premise, nothing on disk derived it). Fix: the round-53
  ledger `corpus/knowledge/kernel-v7.3-recheck-r53.md` (46 rows over S502–S510 with pinned v7.3 copies) and the C1
  ledger arm. Shown able to fail by `python3 .ufo/waves/round-53/count-c1.py <rev>`: at the entering tip
  `20edafa5` it reads `C1=unmet scope=46 rows=0 … source_rows=bad pins=bad provenance=bad … failed=ledger_absent,pins`,
  exit 1 (`.ufo/waves/round-53/evidence/control-c1-do-nothing.txt:3`), and at the data commit `2a4213bf` it reads
  `C1=unmet scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44
  absent=2 holds=46 changed=0 voted=0 dissent=0 … failed=votes` (`.ufo/waves/round-53/evidence/c1-at-data.txt:2`) —
  the omission fails, the recheck passes every arm the votes do not carry. Not covered: the fix reads no remote tag,
  so the trigger stays prose; the next tag still has to be noticed by a seat. Routed to round 54.

- M4: scope — two lane-tree writes by wave seats during w1. (a) `r53-data.tar` (51200 B, the `git archive` of
  `2a4213bf` over the two C2 data paths) appeared at the lane root at 23:19 -03: `git -C <lane> archive -o
  <relative-name>` writes into the repository root, not the cwd (`w1/Mo53ExecMisrootSweep.md` §5.3, finding 7);
  author unverified. (b) The working-tree `tools/fixtures/mori-commit-runway/cases.json` was rewritten to the
  data-commit bytes (23 cases) at 23:17:32 -03, after the L1 had added three cases (`w1/Mo53ExecSelftestReceipts.md`
  finding 2 saw `SKILL.md` pin `PASS 31/31` against a tool printing `28/28`); author unverified — no seat report
  names the write. Evidence: those reports, `w1/Mo53MutC2Tool.md` §Restoration (the seat saw the 26-case bytes,
  sha256 `3a1aef20…`, at 23:14:25). Captured-by: the wave context's rule "write ONLY your own report file" (not
  enforced) and the misroot sweep, which reads the fleet root only. Fix: the L1 removed the tarball, re-applied the
  three cases (sha256 `3a1aef20…`, the same bytes the seat observed) and landed them at `fd86307a`; shown able to
  fail: before the re-application `python3 -I -B tools/mori-commit-runway.py --selftest` printed `PASS 28/28`
  against the registry pin `PASS 31/31` (`mori-pin-check.py` read `state=mismatch class=stale`, seat
  `Mo53ExecPinCheckNoHarm`). Routed: the round-54 wave context names archive outputs absolutely under the seat
  scratch and adds a lane-tree check before integration (`git status --porcelain` outside `.ufo/waves/round-54/`).
- M5: vacuous direction — the band entry, SKILL row and tool docstring first said the per-CPU error makes refusal
  arrive early ("a non-root allocation may already be refused although the printed numbers still show room"); the
  local deltas are signed, so the enforced read sits above or below the exact sum and the dominant case is
  over-admission (`w1/Mo53RevC2Counter.md` finding 1, `w1/Mo53ScribeSkill.md`, `w1/Mo53ExecBandDerivation.md`
  finding 3). Captured-by: wave reviewers, not an instrument (`count-c2.py` compares the tool with REF, and both
  carry the same rule; the rule is direction-neutral, only the reading was wrong). Fix: the entry, SKILL row and
  docstring now state the band two-sided (`fd86307a`); QUALITY 145's rationale carries the corrected reading.
  Shown able to fail: none mechanical — a prose reading has no counter; the lesson records it as such.
- M6: landing latency — attempt 1 left its integration drafts uncommitted while the wave closed. The data
  corrections landed at `fd86307a` (22:41 -03), then `LOG.md`, `PROVINCE.md`, `SHONEN.md`, `corpus/QUALITY.md`,
  `corpus/README.md`, `corpus/SOURCES.md`, the ledger prose, this lesson, all 66 seat reports and the wave record sat
  in the working tree until the orchestrator session exited at 23:57:36 -03 (SIGHUP during an operator `omp update`)
  and killed the L1; the orchestrator had to commit them as salvage `0df80303`, which no L1 had reviewed. Evidence:
  `git show --stat 0df80303` (81 files, +16994/−19), `.ufo/watchdog.log` lane-dead line, the attempt-2 resume note.
  Captured-by: none — the commit order (§4) requires landing before the report, not landing in slices while seats
  settle. Fix (attempt 2, convention): seat reports and integration drafts land in one helper commit as soon as each
  integration pass ends, before the next pass starts; the checkable form is `jj-lane.sh state <lane>` printing
  `tracked=0 untracked=0` at each pass boundary. Shown able to fail: at the salvage-equivalent moment the same
  command would have printed nonzero counts (the 81 files were uncommitted); not shown on a live run — routed as a
  check for the round-54 L1, not counted as a fix.

## Round-52 closure routed defects — dispositions

1. SCORECARD correction → an appended `Round-52 correction` line after the round-52 section names the superseded
   `items=42 … locators=27` and the receipt's `items=43 … locators=28` (QUALITY 146 carries the check).
2. Report self-citation → convention: the round-53 report names its own commit by the command
   `git log --format=%H -- .ufo/reports/round-53/mori.md` on the fleet repo, never a placeholder (QUALITY 147); the
   round-52 report's own hash `aacd7a83027cdee8e950a2c39d490feaed3be13c` is recorded as an erratum in the round-53
   report (a filed report is corrected in the correcting round's report, PROTOCOL).
3. Standing limits (locator arm scope, pure-text receipts, arm-A `admitted` pin) → `Planned (round 54)` in
   SCORECARD, which now exists (it did not when the contract named it: `w1/Mo53ExecConsiderthese.md` finding 4).

## Wave w1 — integrated findings

Data corrected after the wave (landed `fd86307a` and the integration commit): the tool's reads are bounded and
non-blocking, numbers are 1-20 ASCII digits, CPU lists ascending and disjoint and at most 65536, `--page-kb` at most
1024 and ASCII, `--cases` ids one safe path component (`w1/Mo53SentC2ReadOnly.md` HIGH unbounded read and MED FIFO
block / traceback / case-id traversal; `w1/Mo53SentC2Hostile.md` F1–F7); three UNKNOWN cases and five built-in
hostile checks (`PASS 31/31`); the band reading two-sided (M5); the CPU-hotplug limit (the batch is recomputed on
memory hotplug and sysctl writes only — `w1/Mo53ScribeSkill.md`, `w1/Mo53ExecBandDerivation.md` finding 1); S514
pins `mm_init.c` at v7.3; the host sentence dated (`w1/Mo53ScoutRunwayTools.md`, `w1/Mo53ExecHostLive.md`); the
ledger's change table completed (`w1/Mo53ExecAnchorCheck.md` §4.9, `w1/Mo53ExecDiffAudit.md`); row cells corrected
(Gate above); PROVINCE gains the commit-ledger Core note (`w1/Mo53CritCapability.md` F1, `w1/Mo53ScribeProvince.md`).

Verified, no change: all 46 RECHECK rows `holds` by two or three voters, none dissenting (12 voter reports); the
enclosing unit changed for exactly the two `absent` rows (`w1/Mo53ExecDiffAudit.md`); both replacement quotes state
the same condition (`w1/Mo53ExecReplacementQuotes.md`); the 16 frozen and 64 seeded fixtures agree with two
independent kernel-derived oracles (`w1/Mo53ExecFixtureOracleA.md` 16/16, `Mo53ExecFixtureOracleB.md`); the live
read recomputes CommitLimit exactly (`w1/Mo53ExecHostLive.md`); the frozen bytes hash clean after the corrections
(`w1/Mo53ExecMisrootSweep.md` finding 6: 32/32 OK); no mori round-53 misroot at the fleet root.

Named limits of the frozen counters (found by the wave; routed to round 54, never re-scored this round):
- `count-c1.py`: voter identity is the report filename (`w1/Mo53CritC1Junk.md` HIGH); a disposition is never
  checked against the file, only against votes (HIGH, by design — the votes carry it); an `absent` row's quote may be
  any located 6-25-token span (MED); the QUOTE self-vote guard is exact-match (MED); the 25-token upper bound, the
  per-row URL and the scope revision have no selftest arm (`w1/Mo53MutC1.md` M-findings 1-3); the bound counts C
  tokens, not words (`w1/Mo53ExecReplacementQuotes.md`).
- `count-c2.py`: the exit-code comparison has no selftest arm (`w1/Mo53MutC2Counter.md` HIGH — a tool printing the
  right JSON with exit 0 always passes the mutant); the counter is tracked in the lane, so a tool may import REF from
  the archive (`w1/Mo53CritC2Junk.md` HIGH; the witness control is exactly that); the registry and selftest arms are
  textual (MED); `findings`/`notes` are unchecked (`w1/Mo53ExecFixtureOracleB.md`); the batch floor, INT_MAX cap and
  some input classes are never generated (`w1/Mo53MutC2Tool.md`, `w1/Mo53MutC2Counter.md`); the archive is buffered
  in memory (`w1/Mo53RevC2Counter.md` finding 2); the control receipts' agree counts are specific to the control
  commits because the seed is the commit id (`w1/Mo53ExecControlsReplay.md`, `w1/Mo53SentReceipts.md`).
- Scope: four release-triggered v7.2-pinned entries stay unrechecked (`oom-tracepoints-r47.md`,
  `oom-victim-selection-r27.md`, `disk-write-rate-r33.md`, `watchdog-identity-r31.md`; `w1/Mo53CritC1Scope.md`), and
  `w1/Mo53ExecOtherEntriesV73.md` measured r47/r50 drift at v7.3 (page_alloc.c and memcontrol.c citations); S511–S513
  are new v7.2 rows already exposed to the v7.3 trigger (`w1/Mo53ExecCensusCounts.md`) — S514 answers it for
  `mm_init.c`, `w1/Mo53ExecBandDerivation.md` finding 4 found `percpu_counter.c/.h` byte-identical at v7.3 by fetch
  (not pinned).

## Wave w1 — considerthese item: round-52 critic flags carried forward

Source: `considerthese/2026-10-26.md` suggestion 2; seat `w1/Mo53ExecConsiderthese.md`; reference tip
`20edafa5` (round-52 closure), window `4f266ef2..20edafa5`.

Inventory: 34 of 68 round-52 w1 reports carry HIGH/MED lines — 102 lines (97 bullets + 5 table rows), 98
genuine entries after removing four "no defect"/"none" lines — which collapse to 61 distinct flags.

Disposition at `20edafa5`: **13 fixed** by the round-52 landing (S497/S499/S501 anchors, entry rows 3/27/28
and the Boundaries/reading-rules prose, QUALITY 141/142/143, the round-51 erratum, the two stale living pins,
SHONEN pin paths, the at-data instrument commit, the README:728 hermetic wrapper); **18 routed** (five
`Planned (round 53)` items, lesson M4/§5, closure §Routed 1–3); **30 dropped**, of which 8 were recorded somewhere
with no owner and 22 were silent — including the SOURCES S490–S492 in-place rewrite (HIGH)
and the `mori-pin-check.py hidden_rows` blindness (MED).

Three route defects: the r53 contract routes three standing limits to a `Planned (round 54)` line that does not
exist in `SCORECARD.md`; `Planned (round 53)`'s successor-freeze list omits round-40 `conform.py`, the one the
wave proved divergent; and two seats' "route to round 53" sentences (the pin-check `hidden_rows` clause and the C2 docstring clause) have no lane artifact behind them.

Two dropped flags repeated in round 53 and can be checked: the at-data receipt is again outside the data commit
(`c1-at-data.txt` only at the wave-spec commit `95cf78ee`), and the new controls builder again writes receipts
into the lane's own `evidence/` with no `--out` (`round-53/controls/controls.py:78`). Two old counter
weaknesses were inherited verbatim by the new C1 counter (filename-keyed voter identity; `^\s*` vote lines with
a bare three-backtick/tilde fence toggle).

Lesson: a flag that is neither fixed nor named in a planned line is not "known" — it is unscheduled. Before a
wave closes, the L1 should reconcile the wave's HIGH/MED list against the next round's `Planned` paragraph and
either route each flag or record a "won't fix" with a reason; carry a count (`flagged / fixed / routed /
dropped`) in the round section so the drop rate is visible.

## Round shape

One v2 wave `w1`, 67 seats (policy v2, validated rc 0 at the first attempt): reviewer 12, critic 12, executor 20,
mutation-tester 3, sentinel 4, scout 2, connector 2, scribe 10, revenger 1, simplifier 1 (attack share 27/67;
flash-eligible 36/67 at spawn). Twelve RECHECK voters (`Mo53Fr01`–`Mo53Fr12`, three per block of 11-12 rows). The
L1 held the planner seat. The operator changed the role routing mid-round (executor → `@m_mim`, critic/connector →
`@m_kfc`, then connector → `@m_antigravity`, scout → `@m_kfc`); a seat keeps the model it was spawned with.
Residual calls: 0. Round total: 67.

## Attempt 2 (L1 MoriR53a2) — salvage re-verification

Attempt 1 (L1 MoriR53) and every seat of its orchestrator session were killed at 2026-10-26 23:57:36 -03 (session
exit, SIGHUP during an operator `omp update`; not a lane defect). The orchestrator committed the uncommitted tree as
salvage `0df803033fba2386b10f5dcc6aa96bdef65cba15` (parent `fd86307a`). Attempt 2 cites nothing from it before
re-verifying it:

- Frozen bytes: `sha256sum -c` over `.ufo/waves/round-53/evidence/freeze-sha256.txt` → rc 0 at `0df80303`.
- Both counters at `0df80303`: `C1=met … voted=46 dissent=0`, rc 0 (`evidence/c1-at-salvage.txt`); `C2=met … n=31
  fixtures=80 agree=80 disagree=0 registry=ok live=ok`, rc 0 (`evidence/c2-at-salvage.txt`); census `validate --root
  … mori` rc 0.
- Votes against unchanged rows: `git diff 2a4213bf 0df80303 -- corpus/knowledge/kernel-v7.3-recheck-r53.md` touches 0
  `| <12 hex> |` ledger rows; the salvage changes only the change-table prose and the reading-rules sentence.
- Wave record: `w1-results.json` 67 seats, 66 outputs recovered; `Mo53RevLedgerProse` (reviewer) died with no output
  and no report — stays dead in the evidence; its item is re-dispatched in the attempt-2 residual call.
- What the salvage carries that no seat attacked: the tool's post-wave corrections (`git diff 2a4213bf fd86307a --
  tools/` 181 lines), the band entry's two-sided rewrite, the SOURCES anchor corrections, QUALITY 144–147, the
  README/PROVINCE/SHONEN/LOG drafts and this lesson. Those are the residual call's items.
- Attempt 2 adds: the SCORECARD round-52 correction line and the round-53 section (Mo53ScribeScorecard's drafts,
  After cells from the at-salvage receipts so that each row's numbers are those of the receipt it cites — QUALITY
  146), M6 above, this section.
