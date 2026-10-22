# Round 27 wave 2 — Fact 1 review of `corpus/knowledge/oom-victim-selection-r27.md` at tip 5f00fd04

Seat: MoriR27.ReviewEntryFact1 (leaf reviewer, no subagents, no background jobs).
Lane: /home/vgpnk/Projects/shokunin/mori-shokunin. Read-only use only (`git show`, `git cat-file`, `git hash-object` without `-w`). Scratch: /fast/scratch/hyaku/mori-r27/ReviewEntryFact1/.

Scope: Fact 1 only, entry lines 23-56 of the tip blob (`git show 5f00fd04:corpus/knowledge/oom-victim-selection-r27.md`). Checked against earlyoom v1.9.0 `kill.c`, `main.c`, `MANPAGE.md`, `earlyoom.default`, `earlyoom.service.in`, plus the helper sources that Fact 1's reads depend on (`meminfo.c`, `meminfo.h`, `globals.h`, `kill.h`, `msg.h`) and the two kernel lines Fact 1 cites (`fs/proc/base.c:597`, `mm/oom_kill.c:217`). Line numbers come from `awk NR` on the downloaded bytes (same as `grep -n`). `E##` means a line of the tip blob.

## 1. Findings by severity

**High:** none.

**Medium**
- M1 (V22, E55): "`-p` would do the same from inside" conflicts with the manual the entry cites: `MANPAGE.md:114` says the `-p` switch "doesn't work" through the default service. Verdict: UNSUPPORTED as written.
- M2 (V4, E28-29): the quoted words "the process with the highest oom_score" are not in `MANPAGE.md`. Verdict: WRONG quote. The verbatim text is at `MANPAGE.md:20-21`.
- M3 (V12, E41-43): the send-line `oom_score` carries the ±300 only without `--sort-by-rss`. Verdict: WRONG for `--sort-by-rss`; "not the kernel's" overstates.
- M4 (V6, E30-31): the `--sort-by-rss` zero-RSS fallback runs after the ±3 GiB `--prefer`/`--avoid` change. Verdict: INCOMPLETE.
- M5 (V13, E44-45): the "What it skips" list omits three other unreadable-value exits (`oom_score_adj`, `comm`, uid). Verdict: INCOMPLETE.
- R1, R2, R3 (Section 5): rows S115, S118 and S119 do not record most lines Fact 1 cites. The S115 and S118 scopes do not cover the victim options or the victim-selection code.

**Low:** cite additions and wording (V2, V5, V7, V11, V15, V16, V17, V20, V23, header E23). Section 4.

**Holds:** 18 of 23 sentence-level verdicts hold; several need a cite addition.

**Line numbers:** 29 cite groups checked against the bytes. All point at the stated content except two: V4 (the sentence sits at `MANPAGE.md:20-21`; the cite says 19-21) and V15 (the sleep is at `kill.c:613`, outside the cited `:587-592`).

**Upstream bytes are genuine.** All five upstream files match the git blob IDs of the v1.9.0 tree, and the tag resolves to commit 202d4db0 as the entry says (Section 2).

## 2. Upstream record (accessed 2026-10-22, ordinary HTTPS via curl, no browser)

| File at tag v1.9.0 | URL (raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/…) | Access (UTC) | Lines | Bytes | sha256 | git blob = tree |
|---|---|---|---|---|---|---|
| kill.c | …/kill.c | 17:10:02Z | 666 | 21,169 | b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3 | yes (10ad47dc) |
| main.c | …/main.c | 17:10:02Z | 552 | 21,053 | 08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4 | yes (e695f375) |
| MANPAGE.md | …/MANPAGE.md | 17:10:02Z | 288 | 10,114 | cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda | yes (456ee62c) |
| earlyoom.default | …/earlyoom.default | 17:10:02Z | 21 | 563 | c0770413a180e0731583f643fc4e84f4a0dac57efb8f575b74ee9a971df984a2 | yes (ba4f5c9f) |
| earlyoom.service.in | …/earlyoom.service.in | 17:10:02Z | 51 | 1,340 | d4019b66d87539a006fc2d178d972dcf1b46e70343627b8bf66d1a08dcdda0bd | yes (091b041e) |

- Tag: `refs/tags/v1.9.0` → annotated tag object 66d78843fd675859a09a52d3f17b1c408a827a34 → commit 202d4db0d308ca6478f68de68b46cae34896ddaf (api.github.com `git/tags/…`, 17:10:16Z; tagger 2025-09-16T19:09:33Z). Tree listing (recursive): 67 entries, 60 blobs, `truncated: false`, sha256 8b3c95cf88d0b8c58bbe973c1b6846c34063a258b7edfaeb57320f5dfbf3c145 (19,112 B). The S131 row records the same hash.
- Helpers, same tag, all blob-matched: `meminfo.c` 25936e19 (286 lines, sha256 526e512c89c58cb0b1db2ae98ea62d287cdc1516846be80c9173bdc4bf0edfeb); `meminfo.h` 8ea36568; `globals.h` 807c8604; `kill.h` 0d96d3ea; `msg.h` 4b1fc2bd (sha256 e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c). Fetched about 17:11Z.
- Kernel, torvalds/linux tag v7.2, raw.githubusercontent.com, about 17:13Z: `fs/proc/base.c` 3,990 lines, sha256 cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6 (equals the S127 row's recorded hash); `mm/oom_kill.c` 1,257 lines, sha256 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e (equals the S003 row's hash); `kernel/sys.c` 3,074 lines, sha256 c813a332202cd44d7ddb95ced675d1f3f87691678a2973b959c687e28806a251 (fetched about 17:15Z; the first try returned HTTP 429, the retry after 15 s returned 200). `kernel/sys.c` appears in no SOURCES row.
- Upstream quotes (verbatim, line numbers from the downloaded bytes):
  - `MANPAGE.md:20-21`: "it will kill the largest process (highest `oom_score`)."
  - `MANPAGE.md:114`: "the `-p` switch doesn't work"
  - `MANPAGE.md:180-181`: "It is the first 15 bytes of the process name."
  - `kill.c:627`: "sending %s to process %d uid %d" (format string; quotes escaped in source)

## 3. Verdicts, sentence by sentence

Each entry gives the tip line range (E##), the claim, the verdict, the evidence (upstream path:line), and the correction where one is needed. "Holds" with a cite addition means the sentence is true and the cite is incomplete.

**V1 · E25-26 · "One pass … keeps the best candidate through `is_larger` (`kill.c:525-527,551-578`)" · HOLDS.** `kill.c:551` `while (1) {` to `:578`; `:562-563` skip non-numeric names; `:568` calls `is_larger`; `:572-574` replace the victim. Lines 525-527 are the doc comment and the signature.

**V2 · E26-27 · "key is `/proc/<pid>/oom_score`, read as the kernel exports it (`kill.c:396-401`)" · HOLDS.** `kill.c:396` calls `get_oom_score`. The reader is `meminfo.c:175-183`, which reads `oom_score` at `:178`. Add `meminfo.c:172-183` to the cite.

**V3 · E27-28 · "an exact tie goes to the larger resident set (`kill.c:457-465`)" · HOLDS.** `kill.c:462` replaces only when `VmRSSkiB` is strictly larger on an equal score. On a full tie the earlier-scanned process stays.

**V4 · E28-29 · "The manual says the same: kill "the process with the highest oom_score" (S115 `MANPAGE.md:19-21`)" · WRONG (M2, medium).** The quoted words are not in `MANPAGE.md` (grep: absent). The verbatim sentence is at `MANPAGE.md:20-21`: "it will kill the largest process (highest `oom_score`)."
- Old: ``The manual says the same: kill "the process with the highest oom_score" (S115 `MANPAGE.md:19-21`).``
- New: ``The manual says the same, in its parenthetical: it "will kill the largest process (highest `oom_score`)" (S115 `MANPAGE.md:20-21`).``

**V5 · E30-31 · "`--sort-by-rss` makes the resident set the primary key with `oom_score` as the tie-break" · HOLDS (code).** `kill.c:433-440` compares RSS first, then `oom_score` on an RSS tie. The manual (`MANPAGE.md:202-203`) documents only "find process with the largest rss (default oom_score)". Say so in the cite. The fallback part is V6.

**V6 · E30-31 · "falls back to `oom_score` when either side reads a resident set of 0 (S118 `kill.c:429-455`; S115 `MANPAGE.md:202-203`)" · INCOMPLETE (M4, medium).** The test runs on the RSS after the `--prefer`/`--avoid` change. `kill.c:411-412` adds `VMRSS_PREFER` and `:418-419` adds `VMRSS_AVOID` to `VmRSSkiB` before the sort-by-rss block starts at `:430`. Consequences, from code reading (not run):
- A zero-RSS process matching `--prefer` counts as 3 GiB (3,145,728 KiB), so the RSS test (case 1, `:433-440`) applies to it whenever the other side is also above 0, instead of the fallback.
- A process under 3 GiB matching `--avoid` goes negative. The test at `:433` needs both sides above 0, so the comparison falls to `oom_score` (`:441-455`).
- Old: ``falls back to `oom_score` when either side reads a resident set of 0 (S118 `kill.c:429-455`; S115 `MANPAGE.md:202-203`).``
- New: ``falls back to `oom_score` when either side's resident set is not above 0 after the `--prefer`/`--avoid` change (`kill.c:411-412,418-419,433,441-455`), so a `--prefer` match counts a zero-RSS process as 3 GiB and an `--avoid` match makes a process under 3 GiB negative and compares it by `oom_score` (S118 `kill.c:429-455`; the manual documents only the primary key, S115 `MANPAGE.md:202-203`).``

**V7 · E32-33 · "`--prefer`/`--avoid`/`--ignore` match the process name only (`/proc/<pid>/comm`, at most 15 bytes), never the command line" · HOLDS.** `kill.c:405` reads the name into `cur->name`; `:410`, `:417`, `:424` match only that name. The command line is read only for printing (`kill.c:493`, reached from `:514` and `:596`). The 15-byte figure is the manual's (`MANPAGE.md:180-181`). `meminfo.c:207` and `:221` read up to 255 bytes and drop the trailing newline, so the limit comes from the kernel's comm. Add `MANPAGE.md:180-181` to the cite.

**V8 · E34-35 · "`--prefer` adds 300, `--avoid` subtracts 300 (`kill.c:24-27,410-421`); under `--sort-by-rss` ±3,145,728 KiB (`kill.c:29-32`)" · HOLDS.** `kill.c:25`, `:27`, `:30`, `:32` are the defines; `:414` and `:421` add to `oom_score`; `:412` and `:419` add to `VmRSSkiB` under sort-by-rss.

**V9 · E35-36 · "`--ignore` removes the candidate (`kill.c:424-426`)" · HOLDS.** `:425` returns false before the comparison.

**V10 · E36-37 · "Each option takes one regular expression; a repeated flag overwrites the earlier one (`main.c:289,292,302`)" · HOLDS.** `main.c:289`, `:292`, `:302` assign `optarg`, so the last one wins. `regcomp` runs at `:376`, `:383`, `:390`.

**V11 · E38-40 · "+300 weighs like an `oom_score_adj` of about +450 [INFERENCE: base.c:597, kill.c:24-25]" · HOLDS (label correct).** `fs/proc/base.c:597` is `points = (1000 + badness * 1000 / (long)totalpages) * 2 / 3;`. An adjustment A adds A to the inner term through `mm/oom_kill.c:233-234` (`adj *= totalpages / 1000; points += adj;`), so the exported value moves by 2A/3. For +300, A = 450. Add `mm/oom_kill.c:232-234` to the cite.

**V12 · E41-43 · "The score in a send line is earlyoom's score, not the kernel's. The send line prints the candidate's `oom_score` after the prefer/avoid adjustment (S118 `kill.c:627`, format …)" · WRONG for `--sort-by-rss` (M3, medium).** The format string at `kill.c:627` matches the quoted one after unescaping. The printed value is `victim->oom_score` (`:627-628`). It carries the ±300 only without `--sort-by-rss` (`:414`, `:421`). With `--sort-by-rss` the ±3,145,728 KiB goes into `VmRSSkiB` (`:412`, `:419`), which is printed in MiB (`:628`, `victim->VmRSSkiB / 1024`), and the printed `oom_score` is the unadjusted exported value. "Not the kernel's" overstates: the printed value is the kernel's exported value plus the adjustment.
- Old (heading and first sentence): ``**The score in a send line is earlyoom's score, not the kernel's.** The send line prints the candidate's `oom_score` after the prefer/avoid adjustment``
- New (heading and first sentence): ``**The score in a send line is the kernel's exported score plus earlyoom's adjustment.** The send line prints `victim->oom_score``
- Cite: `(S118 kill.c:627-628, format …)` unchanged in form. Add after the format sentence: "Without `--sort-by-rss` that value includes the ±300 (`kill.c:414,421`); with `--sort-by-rss` the ±3,145,728 KiB goes into the printed VmRSS instead (`kill.c:412,419,628`), and the printed `oom_score` is the unadjusted exported value."

**V13 · E44-45 · "What it skips: … processes whose `stat` or `oom_score` it cannot read (`:377-381,396-401`)" · INCOMPLETE (M5, medium).** Other unreadable-value exits in `is_larger`: `oom_score_adj` (`kill.c:470-474`, `return false` at `:473`); `comm` when a prefer/avoid/ignore option is set (`:405-409`, `return false` at `:408`); uid under `--ignore-root-user` (`:364-368`, `return false` at `:367`).
- Old: ``processes whose `stat` or `oom_score` it cannot read (`:377-381,396-401`)``
- New: ``any process whose `stat` (`:377-381`), `oom_score` (`:396-401`) or `oom_score_adj` (`:470-474`) cannot be read; one whose `comm` cannot be read while a prefer/avoid/ignore option is set (`:405-409`); one whose uid cannot be read under `--ignore-root-user` (`:364-368`)``

**V14 · E44-46 · "pid ≤ 2 (`kill.c:357-359`); kernel threads (`ppid == 2`, `:391-393`); root-owned processes under `--ignore-root-user` (`:363-374`); `oom_score_adj == -1000`, checked after the comparison (`:467-478`)" · HOLDS.** `kill.c:357` tests `cur->pid <= 2`; `:391` tests `cur->stat.ppid == 2`; `:371` tests root ownership (`cur->uid == 0`) inside `:363-374`; `:475` tests -1000 after the comparison at `:429-465`.

**V15 · E46-47 · "It does not skip itself during the scan; it notices only after choosing itself and then sleeps (`:587-592`)" · HOLDS, cite gap (low).** `kill.c:587` is the only `getpid()` in the file (checked); `is_larger` (`:355-480`) has no self test. The victim is zeroed at `:591`. The sleep is in `kill_process`: `:608-614`, with `sleep(1)` at `:613`. Add `:608-614` to the cite.

**V16 · E48-49 · "A victim that vanishes before the signal produces one `kill failed:` line and no re-selection; the next attempt is the next poll (`kill.c:640-657`)" · HOLDS, cite gap (low).** `kill.c:640` calls `kill_wait`; `:653-654` print `kill failed:`; `kill_process` does not re-select. For a process already gone, `kill_wait` first prints its pidfd warning at `kill.c:287-290` (`pidfd_open` fails, then `kill` returns ESRCH). The next attempt is the next loop pass in `main.c:514-551` (`find_largest_process` at `:527`, sleep at `:545-549`). Add both cites.

**V17 · E50 · "No prefer, avoid or ignore expression exists by default (S115 has none …)" · HOLDS.** `main.c:147-149` start as `NULL`; `main.c:374-394` act only when the option is given. Add these cites.

**V18 · E51 · "the shipped `earlyoom.default` sets only `EARLYOOM_ARGS="-r 3600"`, S131 `earlyoom.default:5`" · HOLDS.** `earlyoom.default:5` is the only active assignment. `:10`, `:13`, `:16`, `:19` are commented examples (`:19` is a commented `--avoid` example, not active).

**V19 · E51-52 · "`-i` has been a no-op since v1.7 (S115 `MANPAGE.md:89-90`)" · HOLDS.** `MANPAGE.md:89-90` reads "removed in earlyoom v1.7, ignored for compatibility". `main.c:248-250` print "Option -i is ignored since earlyoom v1.7" and do nothing else.

**V20 · E52-53 · "`--ignore-root-user` still works and is missing from the 1.9.0 manual (S119 `main.c:185,281`)" · HOLDS.** `main.c:185` is the long-option entry; `:281` sets `ignore_root_user`. `MANPAGE.md` has no "ignore-root" string (grep: absent). Add `main.c:327`: the `--help` text documents the option, so the accurate claim is "missing from the manual, present in `--help`".

**V21 · E54-55 · "the upstream unit sets `OOMScoreAdjust=-100` and `Nice=-20` (S120 `earlyoom.service.in:12,14`)" · HOLDS.** `earlyoom.service.in:12` is `Nice=-20`; `:14` is `OOMScoreAdjust=-100`. The entry lists them in reverse order; harmless.

**V22 · E55 · "`-p` would do the same from inside (S119 `main.c:397,401`)" · UNSUPPORTED as written (M1, medium).** The code does request the same two values: `main.c:397` calls `setpriority(PRIO_PROCESS, 0, -20)` and `:401` calls `set_oom_score_adj(-100)`. Failures print "Continuing anyway" (`:398`, `:403`). The cited manual says the opposite for the default unit: `MANPAGE.md:114` "When earlyoom is run through its default systemd service, the `-p` switch doesn't work", and `:116-118` give the two unit lines instead. The unit's `CapabilityBoundingSet=CAP_KILL CAP_IPC_LOCK` (`earlyoom.service.in:10`) omits CAP_SYS_NICE and CAP_SYS_RESOURCE. Not run.
- [INFERENCE, not run] The unit already sets both values, so the in-process calls would be same-value writes. `kernel/sys.c:243` refuses only a lowering nice, and the same-uid permission at `:219-229` passes for self. `fs/proc/base.c:1131-1133` refuses only a value below the floor, and the floor is set by a privileged write (`base.c:1155-1157`). If the floor is -100 (set by systemd's privileged write, not read here), writing -100 is accepted. The manual's "doesn't work" may describe an older unit. Either way the sentence must carry the manual's caveat.
- Old: ``; `-p` would do the same from inside (S119 `main.c:397,401`). -100 lowers its score; only -1000 would exclude it.``
- New: ``; `-p` requests the same two values from inside (S119 `main.c:397,401`), but the manual says the `-p` switch "doesn't work" through the default service and gives the two unit lines instead (S115 `MANPAGE.md:114-118`). Not run here. -100 lowers its score; only -1000 would exclude it (kernel `mm/oom_kill.c:217`; earlyoom's own skip `kill.c:475-477`).``
- Dependency: `kernel/sys.c` is in no SOURCES row. Add a row before citing it.

**V23 · E55-56 · "-100 lowers its score; only -1000 would exclude it" · HOLDS, uncited (low).** `mm/oom_kill.c:217` returns `LONG_MIN` for `adj == OOM_SCORE_ADJ_MIN`; `fs/proc/base.c:596-597` leaves the exported score at 0 in that case. The -100 effect is `oom_kill.c:233-234` (2/3 of 100 on the exported scale, about 67 points). Nuance: vfork and already-reaped tasks are also excluded transiently (`oom_kill.c:218-219`). earlyoom's own skip is `kill.c:475-477`. Add these cites.

**Header E23 · "(S118, S115, S119)" · LOW.** Fact 1 also cites S120, S131 and S127. Add them.

## 4. Low-severity cite fixes (exact)

- V2 (E26-27): add `(reader meminfo.c:172-183)` after `kill.c:396-401`.
- V5 (E30-31): after "tie-break" add "(the manual gives only the primary key, `MANPAGE.md:202-203`)".
- V7 (E32-33): add `MANPAGE.md:180-181` for the 15-byte figure.
- V11 (E38-40): add `mm/oom_kill.c:232-234` for the adjustment scaling.
- V15 (E46-47): `(:587-592; the sleep is kill_process's sleep(1) at :608-614)`.
- V16 (E48-49): add `kill.c:287-290` (pidfd warning for a gone process) and `main.c:514-551` (the next poll).
- V17 (E50): add `main.c:147-149` and `main.c:374-394`.
- V20 (E52-53): add `main.c:327` (the `--help` text documents it).
- V23 (E55-56): add `mm/oom_kill.c:217` and `kill.c:475-477`.

## 5. Row-scope gaps (R1-R3, medium)

Each row's recorded line list in SOURCES.md does not cover the lines Fact 1 relies on. Row text is quoted from the tip.

- **R1, S115 (SOURCES.md:121).** Recorded lines: `:30-35`, `:41-45,55-57`, `:65-84`, `:98-109`, `:205-206`, `:208-217`, `:222-250`, `:270-273`. Scope: "the documented command-line contract … `-m`/`-s`, `-M`/`-S`, `-r`, `--dryrun`, `--syslog`, EXIT STATUS". Fact 1 cites `MANPAGE.md:19-21`, `:89-90`, `:177-200`, `:202-203`: none recorded, and the victim options and `-i` fall outside the stated scope. Fix: record those ranges and widen the scope, or cite a row whose scope covers them.
- **R2, S118 (SOURCES.md:124).** Recorded lines: `kill.c:272,282,318,329,338,609,617-627,654`. Scope: "kill-path log literals and the warn() output route". Fact 1 cites 19 kill.c ranges: `24-25`, `24-27`, `29-32`, `357-359`, `363-374`, `377-381`, `391-393`, `396-401`, `404-427`, `410-421`, `424-426`, `429-455`, `457-465`, `467-478`, `525-527`, `551-578`, `587-592`, `627`, `640-657`. Only `:627` lies inside a recorded range; `:654` is recorded, `640-657` is not. The selection code (`kill.c:355-480` and `:525-578`) is outside the row's stated scope, yet it is the basis of V1-V9 and V13-V15. Fix: record those ranges and widen the scope to victim-selection code, or add a row for it.
- **R3, S119 (SOURCES.md:125).** Recorded lines: `main.c:161`, `:295`, `:346-372`, `:414-417`, `:498-504`, `:507-552`, `:519`, `:523`. Scope: "startup and poll-loop emission only". Fact 1 cites `main.c:185`, `:281`, `:289`, `:292`, `:302`, `:397`, `:401`: none recorded; option parsing and `-p` are outside the scope. Fix: record and widen, or add a row.
- **Rows that do cover their cites:** S120 (`earlyoom.service.in:12` and `:14`, SOURCES.md:126); S131 (`earlyoom.default:5`, SOURCES.md:137); S127 (`base.c:592-597`, SOURCES.md:133).
- **Recorded hashes checked against my downloads:** S118 kill.c (21,169 B, b32e0fad) matches; S115 MANPAGE.md (10,114 B, 288 lines, cc48b02e) matches; S119 main.c (08656b0b) matches; S120 service.in (1,340 B, d4019b66) matches; S131 earlyoom.default (563 B, 21 lines, c0770413) and tree listing (8b3c95cf) match; S127 base.c (cef1a2cf) matches; S003 oom_kill.c (452f1348) matches.

## 6. Outside Fact 1 (dependency note; not reviewed beyond the above)

- E135 (Section 5): "Only earlyoom's +300 `--prefer` adjustment can produce that (Fact 1)" holds only for sends printed without `--sort-by-rss` (V12). [INFERENCE] The 8 above-ceiling sends themselves show that the default mode applied to them: only the default mode writes ±300 into the printed score, and the exported score is bounded by `(2000 + adj) * 2 / 3` (`base.c:597`). The sentence should say so.
- Facts 2-6 and their cites were not reviewed, except `base.c:597` and `oom_kill.c:217, :232-234`, which Fact 1 uses.

## 7. Residual risk and verification gaps

- Not run: no earlyoom process, no `-p` call, no `--sort-by-rss` run. V6, V12 and V22 rest on code reading; the `-p` mechanics are labelled [INFERENCE].
- The floor of -100 under the unit depends on systemd's privileged write (not read here; S129 and S130 are outside this review).
- Upstream and kernel lines were read from the downloaded bytes, not from the read tool's URL windows.
- No host data read. No host process, unit, journal or settings value appears in this report.

## 8. Tools, access and privacy

- Installs or updates: none. Tools used as found: curl 8.23.0 (ordinary HTTPS, no browser, no bypass), Python 3.14.8 (stdlib, `-I -B`, blob hashes), git 2.56.0 (read-only `show`; `hash-object` without `-w`), sha256sum 0.8.0, GNU Awk 5.4.1. No pacman transaction.
- Privacy: no uid number, pid, command line, journal `MESSAGE` text, `/etc/default/earlyoom` value, or `--prefer`/`--avoid`/`--ignore` expression was read or written. Upstream code tests are cited by path and line only.
- Retention: the operator's harness settings file was not touched and is not named here.
- Writes: this report only. Scratch files are under /fast/scratch/hyaku/mori-r27/ReviewEntryFact1/.
