# Round 28 — lesson (mori, L1 MoriR28)

author: MoriR28 (L1), from the wave-1 seat reports under `.ufo/waves/round-28/w1/` and the round-27 outside check
`corpus/lessons/round-27-verifier-spotcheck.md`.
Contract: `.ufo/waves/round-28/contract.md` (declared at `079a47c6`; amendments A1 and A2 before any data).

## What the round learned

- **A restore without a reader move puts readers back on wrong wording.** QUALITY 81 freezes a row's first-published
  cells, so restoring S096, S097 and S101 brings back the wording that was corrected in place. The corrected text
  lives on only in the superseding rows S145–S147, and only if every live reader cites those (wave-1 CriticC1Design
  finding 2). Round 27's S143 and S144 broke this: no live file cites either. The C1 counter now counts
  `readers_left`.
- **A shape counter can be met by bookkeeping.** Eight rows that copy the old wording behind a `supersedes` prefix
  made the declared C1 counter print `C1=met` in a sandbox (CriticC1Design finding 1). Amendment A1 hardened it before
  any row existed.
- **jj author time is not write time.** In this jj-colocated lane a commit's author time is when its empty change was
  opened (CriticRoutingCoverage gap 1); only the committer time bounds when content existed.
- **The round-26 tool diverges from two A2 rules in shapes no frozen case covered** (A2-07 in-scope dry-run split;
  A2-10 stamp-less records outside the bounded branch; wave-1 ReviewA2SpecVsTool, tool read at `6ebd518f`). The
  blind cases decide whether those shapes are pinned.

## Mistakes

- **M1 — a typed heading time (class: future-dated evidence).** Evidence: round-27 amendment W1 heading
  `2026-10-22T15:55Z` vs its shipping commit `dd4dbb20`, committed 15:50:10Z (`round-27-verifier-spotcheck.md:34-37`).
  Round 28's first correction then bounded it by author time, which jj sets when the change is opened (wave-1
  CriticRoutingCoverage). Captured-by: none (PROTOCOL §Evidence standard states the rule; no check enforced it).
  Fix: QUALITY 83 (below), whose check compares a dated heading with the committer time of the commit that adds it;
  shown able to fail on W1 at `df886be1`.
- **M2 — seat fetches misrooted at the fleet root, invisible to the lane's misroot sweep (class: write outside the
  lane; detection blind spot).** Evidence: seven upstream files (`base.c`, `oom_kill.c`, `MANPAGE.md`, `main.c`,
  `meminfo.c`, `sd-main.c`, `user@.service.in`) written at the fleet root during round 27 (mtime 14:08:55-03:00); each
  sha256 prefix is cited by a mori round-27 w1 report, and no other lane claims them (wave-1 MisrootProvenance;
  tsukuroi `RevSeatScope.md:13` disowns them). `tools/mori-misroot-sweep.py --lane mori --round 27` read
  `MORI_MISROOT_CLEAN` on them: upstream bytes name neither the lane nor the round. Captured-by: the addendum's misroot
  sweep (manual), not the lane tool. Fix: `.ufo/waves/round-28/misroot-hash-check.sh <round>` matches untracked
  fleet-root files by content hash against the round's committed wave reports; it printed `misroot_hits=7`, exit 1
  before the sweep (`evidence/misroot-before.txt`) and `misroot_hits=0`, exit 0 after (`evidence/misroot-after.txt`).
  Disposition: copied byte-exact to the lane root (`cmp` ok) and the fleet copies deleted at 18:01Z, landed in
  `763d3469`.
- **M3 — a withdrawn claim shrinks the admission set (class: claim declared beyond what one round can land).**
  Evidence: round-27 C2 withdrawn by W1 after its case writer died at spawn; the closure ruled a withdrawn claim not
  verified (`round-27-verifier-spotcheck.md:71-79`). Captured-by: the closure (outside). Fix: this round's contract
  states "a declared claim is never withdrawn; a miss is reported as a miss" (`contract.md:5-6`), and C2 is
  re-declared with ten independent blind writers instead of one.
- **M4 — superseding rows that no reader cites (class: false provenance).** Evidence: S143, S144 (round 27) list
  `used-by` files that cite neither id (wave-1 CriticC1Design finding 2: `grep -c '\bS14[34]\b'` → 0 in all six
  pairs). Captured-by: none. Fix: the amended C1 counter fails a mined superseding row whose `used-by` paths do not
  cite it and counts `readers_left`; it printed `readers_left=27`, `C1=unmet` at `6ebd518f`
  (`evidence/c1-before-a1.txt`). S143/S144 themselves are carried (not in this round's eight).
- **M5 — no receipt at the landed tip (class: evidence measured before the last batches).** Evidence: round 27's
  last committed C1 receipt and retention scan name `0becc421` and `5f00fd04`, seven commits before the landed tip
  `df886be1` (`round-27-verifier-spotcheck.md:88-89,146-147`). Captured-by: none. Fix: QUALITY 84 and its check
  `.ufo/waves/round-28/check-tip-receipts.sh`, which fails on round 27 at `df886be1` (exit 1; wave-1
  DraftQualityCriteria); the round-27 tip receipts now exist (`evidence/r27-tip-c1.txt` `C1=met` exit 0,
  `evidence/r27-tip-retention.txt` metric 4; wave-1 TipReceiptsR27), and round 28's last batch carries its own.

## Gate (superseding rows, opened 2026-10-22 in round 28)

Each line is copied from the drafting seat's report (`.ufo/waves/round-28/w1/Supersede<old id>.md`); the sha256 cell is that seat's digest of the fetched bytes at the URL named first.

| id | source | access time | sha256 | located quote | decision |
|---|---|---|---|---|---|
| S145 | https://github.com/torvalds/linux/commit/52b1364ba0b105122d6de0e719b36db705011ac1.patch | 2026-10-22T17:59:57Z | `a255f4471b9388ba3d5bfdf64a093dec35a66cd8080473fb4bd2d4b49dce7cd6` | patch `:15-17` (25 words): "IRQ/SOFTIRQ always happen in the current task on the CPU, make nothing productive could run even if it were runnable, so we only use PSI_IRQ_FULL." | admit, A, mined |
| S146 | https://www.kernel.org/pub/linux/docs/man-pages/man-pages-6.20.tar.xz (with https://man7.org/linux/man-pages/man5/proc_pressure.5.html, https://man7.org/linux/man-pages/dir_section_5.html, https://man7.org/linux/man-pages/man5/proc.5.html) | 2026-10-22T18:00:50Z | `180f0d16a2142dd9671760ac0afeadcc25e861f695eb420293e1206a87ca083f` | 404 body line 6 (man7 candidate page): "The requested URL was not found on this server." (9 words) | admit, A, mined |
| S147 | https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md | 2026-10-22T17:59:03Z | `0b2e1457021fa526f2c35015672f1d7ccbac95e7b9f217528ab8022c55ed5883` | `:623` "`async.maxJobs` \| number \| `100` \| Running background-job cap, floored to at least 1" (11 words) | admit, A, mined (SupersedeS101; duplicated sha256 cell removed after wave-2 ReopenS147) |
| S148 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c (with `include/uapi/linux/oom.h` and `kernel/fork.c` at v7.2) | 2026-10-22T17:58:57Z | `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6` | `base.c:1147` "if (mm_flags_test(MMF_MULTIPROCESS, p->mm)) {" | admit, A, mined; sha256 cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6 |
| S149 | https://man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html ; https://man7.org/linux/man-pages/man5/proc_pid_oom_score.5.html (sha256 769edf3b9c054934db07f16173297fc5fd63c3a4c807682355f08fa45cde80a9 ; 6169628d8a2cdc512795cfda74f3598d5b7a25e5b71921d4088c0539cf71b2bc) | 2026-10-22T17:59:01Z | `769edf3b9c054934db07f16173297fc5fd63c3a4c807682355f08fa45cde80a9` | adj page `:145-146` "The default value for this file is 0; a new process inherits its parent's oom_adj setting." (16 words) | admit, A, mined (SupersedeS128) |
| S150 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml (with https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-system.conf.xml) | 2026-10-22T17:58:56Z | `44b89bffce737aff803966c207329e9fe2d28ad07709a4bb8e0edf6a4ec0d844` | `systemd.exec.xml:1299-1300` "If not specified, defaults to the OOM score adjustment level of the service manager itself, which is normally at 0." (20 words) | admit, A, mined (MoriR28.SupersedeS129) |
| S151 | https://api.github.com/repos/rfjakob/earlyoom/git/trees/v1.9.0?recursive=1 ; https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.default (listing sha256 8b3c95cf88d0b8c58bbe973c1b6846c34063a258b7edfaeb57320f5dfbf3c145) | 2026-10-22T17:59:24Z | `8b3c95cf88d0b8c58bbe973c1b6846c34063a258b7edfaeb57320f5dfbf3c145` | `:535` `"truncated": false`; `:5` `EARLYOOM_ARGS="-r 3600"` | admit, A, mined (SupersedeS131) |
| S152 | https://raw.githubusercontent.com/can1357/oh-my-pi/6962d5cd2ef157ebf9f415acd58b8744f66400d8/packages/coding-agent/src/async/job-manager.ts | 2026-10-22T17:59:30Z | `f8851470a8bd953f25ab659c0d0aac2ea8c34df9a433e154ec4127c7683b70bd` | `job-manager.ts:305` "return Math.max(1, Math.floor(value ?? DEFAULT_MAX_RUNNING_JOBS));" (5 words) | admit, A, mined (sha256 `f8851470a8bd953f25ab659c0d0aac2ea8c34df9a433e154ec4127c7683b70bd`) |

### Row changes logged old → new (CORPUS Rules 2)

- **S096 `teaches`, restored in place (QUALITY 81):** old (in-place edit `7c77fba`) "…so an absent irq file is never a
  zero reading; it is consistent with no IRQ time accounting at build, PSI disabled at boot (the commit gates the file
  under psi_enable), or a kernel older than 6.1." → new = first-published (`df4db54`) "…so an absent irq file is a
  build-configuration fact and never a zero reading." The first-published wording is false; S145 carries the correction
  and every live reader now cites S145.
- **S097 `anchor` and `teaches`, restored in place:** old digest `80c3fe2ae1062abf` and flip "(S090, …; S001 is the
  rendered page)" → new = first-published (`df4db54`) digest `80c3fe2ae1062abf5` and flip "(S001; …)". S146 carries the
  correction (its source is the man-pages 6.20 tarball, re-opened this round; the 404 page is unchanged: wave-1
  SupersedeS097).
- **S101 `teaches`, restored in place:** old (in-place edit `d3b7af2`) "…states no maximum, so a reader of this page alone
  would expect… The page omits the maximum; it does not contradict it." → new = first-published (`90ed9b7`) "…states no
  upper bound… so docs and code disagree for values above 100." False; S147 carries the correction.
- **New rows S145–S152** (`status` mined; `used-by` = the live readers that cite each new id plus this lesson). No
  `status`, `recheck` or `used-by` cell of an older row changed this round; the old rows' `used-by` still name their
  readers of record (carried: move them to history-only lessons, wave-1 CriticC1Design finding 2 step 3).
- **Live readers repointed** (QUALITY 77; amendment A1): `SKILL.md:619,722`, `PROVINCE.md:257-258,377-378`,
  `corpus/README.md:36`, `corpus/knowledge/system-pressure-r24.md:1,30,41,61,110,177,224`,
  `corpus/knowledge/harness-job-capacity-r25.md:1,47,277,330`, `corpus/knowledge/oom-victim-selection-r27.md:1,37,48,55,63,66,72,78,84,89`.
  `oom-victim-selection-r27.md:203` keeps `S127` because it names tsukuroi's row (wave-1 SupersedeS127).

### Census (round start → round end)

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`:
start (18:00:45Z, working tree before any round-28 row) six W04 (S035, S037, S073–S076), `mori ok`, exit 0; end
(after `6b695b02`) nine W04 — the six plus S148, S149, S150 ("duplicate url … across scopes": each superseding row
keeps its old row's URL with a corrected scope) — `mori ok`, exit 0. Rows 144 → 152 (+8, all tier A, all mined).

### Routed defects (round-27 closure) — disposition

| Routed | Disposition | Evidence |
|---|---|---|
| 1 W1 future-dated | dated correction appended (committer-time bound); QUALITY 83 + check | `.ufo/waves/round-27/contract.md` tail; M1 |
| 2 tip receipts | r27 tip receipts committed; QUALITY 84 + check; round-28 last batch carries its own | `evidence/r27-tip-*.txt`; M5 |
| 3 QUALITY 81 at tip | S096, S097, S101 restored; `changed=0` | C1 counter, `row_identity=rows=152 changed=0` |
| 4 carried row defects | S145–S152 superseding rows, readers repointed | C1 `superseding=8/8 readers_left=0` |
| 5 C2 / r26 D7 | re-declared and frozen with ten blind writers; `PASS 30/30` | C2 counter at the freeze `d21b8bd3` |
| 6 r25 R1, R5 | carried: wave-1 FixR1Runway and FixR5RoutedSelftest drafts exist in scratch only; no non-author check of a landed change fits the time box, so no tool change landed | wave-2 ReviewR1Patch, ReviewR5Patch |
| operator: seven fleet-root files | mori r27 seat fetches; swept into the lane | M2 |

### Seat notes

- Wave-1 CaseA2r01 read part of `CriticC2Design.md` (which holds tool outputs) after finalising its cases, and says so;
  its cases were already fixed in its scratch file. Disclosed for the C2 blindness judgment.
- Wave-1 SupersedeS140 ended its first run before writing its report; the same identity was resumed by message
  and wrote it (no replacement seat).
- Wave-1 seats CriticC2Design and ReviewA2SpecVsTool read the tool; neither wrote cases.
- Round-27 wave-2 reports not named in `round-27.md` (wave-1 ReviewQ80AtR27Tip: CriticC1Admission, ReopenS133–S137,
  ReviewEntryFact1, ReviewHygieneD2, ReviewHygieneR7, ScoutMisroot): committed in round 27, their open findings are
  carried as named debt for round 29 (not routed to this round's claims).
- Inherited, untouched: `.scratch/` (dated 2026-10-21, pre-round, not round work).
- C2 blindness, qualified (wave-2 CriticC2Admission): CaseA2r03 read lines 1-45 of `w1/CriticC2Design.md` before
  writing its cases; CaseA2r07 read the round-27 counter; CaseA2r04–r07 read the round-28 contract (A1 carries the
  tool-derived A2-07 field fact). The freeze hash was missing from the freeze batch's LOG line; it is `d21b8bd3`,
  case file sha256 `ec04a74a3eb65f856dedb3f0509122ee07fdfba7f49e90781d86ab2a393ea6aa`. The A2-07 and A2-10 breach shapes of wave-1 ReviewA2SpecVsTool are not covered by any
  frozen case and stay open (round-29 candidate). Lesson: a writer-blind wave needs its critic's tool-reading report
  kept out of the shared report directory until the freeze.

### Wave-2 corrections to `## Mistakes` (CriticLessonMistakes, ReviewMisrootSweep; appended, the entries above stand as written)

- **M1, M5 captured-by:** "none" is wrong for both; the round-27 closure caught them
  (`round-27-verifier-spotcheck.md:34-37,144-147`). The checks (QUALITY 83, 84) are the first in-lane capture.
- **M2:** the claim that `tools/mori-misroot-sweep.py --lane mori --round 27` read `MORI_MISROOT_CLEAN` rests on an
  L1 run at about 18:00Z whose output was not saved; it is not committed evidence. The hash check is defeated by a
  one-byte change to a fetched file and credits its own receipt when run against round 28 (CriticLessonMistakes).
- **M3:** class corrected to *single point of failure in a declared claim* (one writer per rule); the fix is a contract
  sentence and cannot fail, so it does not count as a fix shown able to fail.
- **M4:** the counter's fixed map never examines S143/S144; that debt stays carried.
- **M6 (new) — writer blindness broken by a shared report directory (class: independence leak).** Evidence: CaseA2r03
  read lines 1-45 of `w1/CriticC2Design.md` before writing; disclosure above under "Seat notes" and in `LOG.md`.
  Captured-by: wave-2 CriticC2Admission. Fix (not yet shown able to fail): a blind wave's critic reports that quote tool
  output are written outside the writers' readable paths until the freeze.
- **M7 (new) — a reader cited a row before the row existed (class: dangling citation).** Evidence:
  `harness-job-capacity-r25.md:47` cited S147 from `1c4c186e` until S147 landed in `6b695b02`; the counter's
  `readers_left` only looks for old ids. Captured-by: wave-2 CriticC1Admission F3. Fix: carried (a dangling-id check).
- **Late seats:** SupersedeS101 delivered last (S147 landed in `6b695b02`, after the wave-2 attack revision
  `f2de0eed`, so wave-2 re-runs at `f2de0eed` print `superseding=7/8`); SupersedeS140 was resumed once by message.
  BuildCountC2's report landed in `84abe93e`, after its counter (`7b75f45a`). The case writers' brief allowed upstream
  earlyoom sources beyond the contract's read list; no amendment recorded it.
- **Withheld seat report:** wave-1 `FixR1Runway.md` (written after the scope freeze) quotes the live harness settings
  value in two before/after lines, so it is not committed (privacy rule; QUALITY 80 disposition: withheld). Its patch
  stays in scratch; r25 R1 and R5 are carried (wave-2 ReviewR1Patch: F1–F3 reproduced open; ReviewR5Patch: forged PASS
  survives `--rerun`, missing baseline exits 1, sub-directory `--repo` flips the result). FixR5RoutedSelftest had not
  returned at the round's last commit.
