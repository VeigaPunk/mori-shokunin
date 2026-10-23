author: mori-shokunin L1 MoriR31 (round 31, attempt 1)

# mori round 31 — lesson

## What the round learned

- A pid probe cannot identify the fleet watchdog by name: its `#!/usr/bin/env bash` shebang makes the task name `bash`
  (measured, wave-1 LiveCommProbe), `-f` matches any command line that mentions the name (LiveArgvProbe), and the one
  read-only identity anchor the watchdog itself creates is its `flock` on `.ufo/.watchdog.lock`, visible in
  `/proc/locks` (S174). Entry `corpus/knowledge/watchdog-identity-r31.md`.
- A counter frozen with two controls can still be met by a third, cheaper shortcut. Both round-31 counters were: junk
  readings over real upstream copies met C1, and answer-key lookups met C2 (M3). Amendment A1 tightened both before any
  entry or tool was scored.
- The round-30 blindness gate's parser defect (D1) is fixed in a lane tool, `tools/mori-blind-check.sh`, scored on 27
  fixtures under bwrap isolation.

## Mistakes

- **M1 — a declared before-value the counter cannot print (class: declaration not reconciled with its receipt).**
  Evidence: the round-31 SCORECARD declaration (`2124cbcd`) says `count-c2.py a12c68ae` → `tool=absent`, `C2=unmet`,
  exit 1; the receipt committed at `8baccf4a` (`.ufo/waves/round-31/evidence/c2-before-base.txt`) prints `fixtures absent
  at revision`, `C2=error`, exit 2, because the counter reads the fixtures (frozen in the same commit) before the tool.
  Captured-by: none fired; QUALITY 25 (state the scope measured) is the nearest, and wave-1 CriticSizing and
  CriticC2Counter caught it. Fix: an appended SCORECARD correction (amendment A1 paragraph) names the real before
  state at `2124cbcd`; rule for later rounds — paste the before receipt's last three lines into the declaration cell
  only after running it. Shown able to fail: the receipt above differs from the declared cell.
- **M2 — A1 silently weakened C1's frozen case-uniqueness predicate (class: undisclosed-contract-relaxation).** Evidence: the frozen contract requires each row's case id to exist in exactly one eligible fixture file (`a66751b1:.ufo/waves/round-30/contract.md:32-36`; the original contract is identified at `round-30-verifier-spotcheck.md:38-39`). Amendment A1's preamble says "nothing is narrowed" (`05db57ed:.ufo/waves/round-30/contract.md:124`), but its added 3a text permits a case id in more than one eligible file when copies' `inputs` and `expect` are identical (`05db57ed:.ufo/waves/round-30/contract.md:136-137`). This relaxes the exactly-one predicate. Captured-by: QUALITY 25 says narrowing must be an explicit correction, not a silent edit (`corpus/QUALITY.md:50`). It did not catch this at amendment time: the round-30 spotcheck records both the relaxation and the absence of a `## Mistakes` row (`round-30-verifier-spotcheck.md:34-37,179-181`). [INFERENCE] The criterion was not operationalized as an amendment-versus-frozen-predicate check; A1's broad preamble was not tested against its condition-level change. Fix: before accepting an amendment, compare every amended condition against the frozen predicate, list each removed or loosened obligation, and fail if an undisclosed relaxation remains. Show that the check can fail by applying it to A1 and requiring a red result that names condition 3a's `exactly one` → `more than one when identical` change despite the preamble; retain that failing receipt (and an unchanged-predicate control). A3 (`55f9a694`) is no precedent: its contract labels it AFTER the L1 ran the A2 gate and describes a gate-allowlist counter change after data (`.ufo/waves/round-30/contract.md:207-218`); the spotcheck explicitly says not to use A3 as precedent (`round-30-verifier-spotcheck.md:180-181`).
  A3 (`55f9a694`, a gate change made after its output was seen) is not a precedent for any later amendment.
- **M3 — controls chosen by the author missed the cheapest shortcut (class: counter met by a do-nothing-grade
  shortcut).** Evidence: `count-c1.py` printed `C1=met` on a junk table citing real upstream copies (CriticSizing
  sandbox `1f5710a8`) and on an HTML-commented, renumbered falsifier (CriticC1Counter sandbox `9140d11c`);
  `count-c2.py` printed `C2=met` for content-hash, creation-order and answer-key lookups (CriticC2Counter,
  CriticSizing). The committed controls (`evidence/c1-controls.txt`, `c2-controls.txt`) had tried only a sourceless
  table, fabricated copies, a do-nothing port, a grep shortcut and id-keyed canned output. Captured-by: addendum §9
  ("build the cheapest control … if it meets the target, the counter … is wrong — fix it before data"); it fired only
  because wave-1 critics attacked the counters before any entry or tool existed. Fix: amendment A1 (`7973034b`), receipts
  `evidence/c1-a1-controls.txt` and `c2-a1-controls.txt` (`3b92ccbb`): all eleven C2 and five C1 controls unmet.
  Shown able to fail: the same controls print `C1=met` / `C2=met` under the original counters (same receipts).
- **M4 — pre-assigned source ids pointed at already-registered URLs (class: renumbered source).** Evidence: S166
  (`fs/proc/base.c`, already S127/S148) and S168 (`proc.rst`, already S082) were pre-assigned in the wave-1 context;
  seats SrcProcBaseCmdline and SrcProcDocs rejected both (Gate below). Captured-by: the round-30 reject precedent
  (`corpus/lessons/round-30.md:134`); A1 now also requires a new id's URL to be absent at the entering tip. Fix shown
  able to fail: `count-c1-a1.py` on CriticC1Counter's renumbered falsifier reports `url_registered_at_entering_tip`.

- **M5 — amendment A1 said nothing was loosened, but its C2 nonce line removed the end-of-file shape (class:
  undisclosed relaxation inside a tightening; the round-30 D2 class repeated).** Evidence: `count-c2-a1.py:55` appends
  `<!-- nonce … -->` after every brief, so no block reaches end of file; ten of the 16 frozen fixtures end on a list
  entry. Residual CriticAmendmentA1 built a copy of the tip tool that drops a file's last line: `count-c2.py` → `7/16`,
  `C2=unmet`; `count-c2-a1.py` → `27/27`, `C2=met` (`.ufo/waves/round-31/r1/CriticAmendmentA1.md`). The contract's A1
  text ("A1 only adds conditions; nothing in P-C1 or P-C2 is removed or loosened") is therefore wrong for C2. Unlike
  P-C1-A1, P-C2-A1 does not include "P-C2 holds". Captured-by: QUALITY 25 and this lesson's M2 rule; the A1 author
  checked the nonce against expected hits only, not against tool failure modes it could hide. Effect on the verdict:
  none — both counters print `C2=met` at the measured tip (`evidence/c2-after.txt`), and the report states C2 under
  both. Fix: an amendment that perturbs inputs must state, per perturbation, which failure mode it can mask, and
  must keep the original predicate as a conjunct; shown able to fail by the last-line-drop copy above.
- **M3 addendum — thresholds set with candidate data in view.** When A1 was written, the wave-1 source drafts and the
  entry draft existed in seat reports (none committed, none scored). A1's C1 conditions loosen nothing, but they were not
  set blind to that data (residual CriticAmendmentA1 §1).

## Gate (rows opened 2026-10-22 in round 31)

Fourteen candidates opened; twelve admitted, two rejected (duplicate URLs). Every admit row's bytes are committed
unchanged at `corpus/evidence/sources-r31/S###.src` and re-fetched by `count-c1.py` / `count-c1-a1.py` at measurement.
S161–S173 were opened by wave-1 seats (seat report `.ufo/waves/round-31/w1/<seat>.md`); S174 by the L1. The L1 dropped two located quotes shorter than 3 words from the seat drafts of S163
(`sched.h:1181`, 2 words) and S164 (`fs/exec.c:1253`, 1 word) to meet A1; the remaining quotes are the seats' own. The S174
label `proc_locks.5:46-48` read `(12 words)` at `5b728304`; the quote has 13 words (residual ReviewGateSpot); corrected
in place under QUALITY 90. Residual JudgeC1Rows reported two locators one line off (S172 `:34-35`, S173 `:1092-1093`); rejected after
checking: `sed -n 34,35p` of `S172.src` and `sed -n 1092,1093p` of `S173.src` print the quoted lines, so both stand.

| id | url | accessed | sha256 | located quotes | decision |
|---|---|---|---|---|---|
| S161 | https://gitlab.com/procps-ng/procps/-/raw/v4.0.7/man/pgrep.1 | 2026-10-22T23:43:06Z | `c2024c384dd88df2a4d5093d4726e57f38c5fee378dc7ed4c99c70c2f6341e35` | `man/pgrep.1:105-108` (21 words): ".I pattern is normally only matched against the process name.  When .B \-f is set, the full command line is used."; `man/pgrep.1:305` (10 words): "No processes matched or none of them could be signalled."; `man/pgrep.1:318-324` (19 words): "The running .BR pgrep , .BR pkill , or .B pidwait process will never report itself as a match." | admit, A, mined |
| S162 | https://gitlab.com/procps-ng/procps/-/raw/v4.0.7/src/pgrep.c | 2026-10-22T23:43:06Z | `af711983209fa083eef970f045104397b0d1406b9aacad2be0747e966e584e16` | `src/pgrep.c:909-912` (13 words): "if (opt_full) strncpy (cmdsearch, task_cmdline, cmdlen -1); else strncpy (cmdsearch, PIDS_GETSTR(CMD), cmdlen -1);"; `src/pgrep.c:851-852` (5 words): "if (PIDS_GETINT(PID) == myself) continue;"; `src/pgrep.c:962-963` (21 words): "if ((!matches) && (!opt_full) && is_long_match(opt_pattern)) warnx(_(\"pattern that searches for process name longer than 15 characters will result in zero matches\n\"" | admit, A, mined |
| S163 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/sched.h | 2026-10-22T23:43:05Z | `a31c63e692cb8ab036d01c0092fcdf4dfb75ec1f17dfda9056b12abecdb3dedf` | `sched.h:325` (3 words): "TASK_COMM_LEN = 16,"; `sched.h:1177-1179` (19 words): "normally initialized by begin_new_exec() * - set it with set_task_comm() to ensure it is always * NUL-terminated and zero-padded" | admit, A, mined |
| S164 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/exec.c | 2026-10-22T23:43:07Z | `44e4185bf9332d86a2fd6bbe33c22cdd0b5129521499b703058813d2106572c7` | `fs/exec.c:1096` (7 words): "size_t len = strnlen(buf, sizeof(tsk->comm) - 1);"; `fs/exec.c:1257` (3 words): "__set_task_comm(me, kbasename(bprm->filename), true);" | admit, A, mined |
| S165 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/binfmt_script.c | 2026-10-22T23:43:06Z | `81b0293a89908d56575f2b00b3550f927eb80714ef540f9634272bce56f9c656` | `binfmt_script.c:99-101` (22 words): "Splice in (1) the interpreter's name for argv[0] * (2) (optional) argument to interpreter * (3) filename of shell script (replace argv[0])"; `binfmt_script.c:125` (4 words): "retval = bprm_change_interp(i_name, bprm);"; `binfmt_script.c:136` (3 words): "bprm->interpreter = file;" | admit, A, mined |
| S166 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c | 2026-10-22T23:43:05Z | `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6` | `base.c:376-378` (7 words): "mm = get_task_mm(tsk); if (!mm) return 0;"; `base.c:323-324` (20 words): "* Magical special case: if the argv[] end byte is not * zero, the user has overwritten it with setproctitle(3)."; `base.c:1766-1773` (17 words): "exe_file = get_task_exe_file(task); if (exe_file) { *exe_path = exe_file->f_path; path_get(&exe_file->f_path); fput(exe_file); return 0; } else return -ENOENT;" | reject, duplicate URL already carried by S127 (corpus/SOURCES.md:133) and S148 (corpus/SOURCES.md:154); round-30 precedent corpus/lessons/round-30.md:134 rejects a URL already shown inside a SOURCES row |
| S167 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/array.c | 2026-10-22T23:43:06Z | `a3eb1567e6125bd9c3136efacf1e6ee7526deb4212a895f3c3156d2410985828` | `fs/proc/array.c:584-586` (15 words): "/* apply timens offset for boottime and convert nsec -> ticks */ start_time = nsec_to_clock_t(timens_add_boottime_ns(task->start_boottime));"; `fs/proc/array.c:588-592` (15 words): "seq_put_decimal_ull(m, \"\", pid_nr_ns(pid, ns)); seq_puts(m, \" (\"); proc_task_name(m, task, false); seq_puts(m, \") \"); seq_putc(m, state);"; `fs/proc/array.c:136` (5 words): "\"Z (zombie)\", /* 0x20 */"; `fs/proc/array.c:610-611` (8 words): "seq_put_decimal_ull(m, \" \", 0); seq_put_decimal_ull(m, \" \", start_time);" | admit, A, mined |
| S168 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst | 2026-10-22T23:43:07Z | `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126` | `proc.rst:347` (8 words): "start_time time the process started after system boot"; `proc.rst:2009-2011` (21 words): "writing anything longer then the kernel's TASK_COMM_LEN (currently 16 chars, including the NUL terminator) will result in a truncated comm value."; `proc.rst:135` (4 words): "cmdline Command line arguments" | reject, exact URL already a row: S082 at corpus/SOURCES.md:88 carries this same URL at tag v7.2 with the same sha256 prefix e760f716f8278dee, so the bytes are already admitted; extend S082's scope and anchor instead of opening a second id for them |
| S169 | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_comm.5?h=man-pages-6.20 | 2026-10-22T23:43:06Z | `31aee9e50c23579e7983e26edee83bee9ab7a8ba4c7be46027db2cac5ee23c08` | `man/man5/proc_pid_comm.5:30-32` (15 words): "Strings longer than .B TASK_COMM_LEN (16) characters (including the terminating null byte) are silently truncated."; `man/man5/proc_pid_comm.5:21-23` (21 words): "A thread may modify its .I comm value, or that of any of other thread in the same thread group (see"; `man/man5/proc_pid_comm.5:17-20` (21 words): "Different threads in the same process may have different .I comm values, accessible via .IR /proc/ pid /task/ tid /comm ." | admit, A, mined |
| S170 | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_cmdline.5?h=man-pages-6.20 | 2026-10-22T23:43:06Z | `a9f3b83b1b0442319d0a8a5be23787c8024bc485dd54a062da9c37d57733f111` | `proc_pid_cmdline.5:13-14` (17 words): "This read-only file holds the complete command line for the process, unless the process is a zombie."; `proc_pid_cmdline.5:16-17` (21 words): "In the latter case, there is nothing in this file: that is, a read on this file will return 0 characters."; `proc_pid_cmdline.5:33-37` (19 words): "If, after an .BR execve (2), the process modifies its .I argv strings, those changes will show up here." | admit, A, mined |
| S171 | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_stat.5?h=man-pages-6.20 | 2026-10-22T23:43:07Z | `cba82e47c8c7917ec4f7c24d9c8779c53ecf478fdefe5c7835690989bb060bcd` | `man5/proc_pid_stat.5:43` (8 words): "One of the following characters, indicating process state:"; `man5/proc_pid_stat.5:228-229` (17 words): "The time the process started after system boot. Before Linux 2.6, this value was expressed in jiffies."; `man5/proc_pid_stat.5:39` (10 words): "(16) characters (including the terminating null byte) are silently truncated." | admit, A, mined |
| S172 | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man2const/PR_SET_NAME.2const?h=man-pages-6.20 | 2026-10-22T23:43:03Z | `f2ac57cc826943dcd5bc71feea9859099014bc59767b21eafad44a7325be558a` | `PR_SET_NAME.2const:26-29` (21 words): ".B PR_SET_NAME Set the name of the calling thread, using the value in the location pointed to by .IR name ."; `PR_SET_NAME.2const:34-35` (19 words): "If the length of the string, including the terminating null byte, exceeds 16 bytes, the string is silently truncated."; `PR_SET_NAME.2const:53-57` (11 words): ".SH ERRORS .TP .B EFAULT .I name is an invalid address." | admit, A, mined |
| S173 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/sysctl/kernel.rst | 2026-10-22T23:43:06Z | `e9baf759b3eac6b58d893638280e9924fec46a8814169b224bbf9ae7f7fd4a32` | `kernel.rst:1084-1085` (21 words): "PID allocation wrap value.  When the kernel's next PID value reaches this value, it wraps back to a minimum PID value."; `kernel.rst:1086` (9 words): "PIDs of value ``pid_max`` or larger are not allocated."; `kernel.rst:1092-1093` (17 words): "The last pid allocated in the current (the one task using this sysctl lives in) pid namespace." | admit, A, mined |
| S174 | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_locks.5?h=man-pages-6.20 | 2026-10-22T23:48:04Z | `509fd95031ba3c9fb62c8d34b8e0c9f233ccf44d0d33d4b48b260a91de2d4905` | `proc_locks.5:46-48` (13 words): ".B FLOCK This is a BSD file lock created using .BR flock (2)."; `proc_locks.5:80` (9 words): "The PID of the process that owns the lock."; `proc_locks.5:93` (9 words): "followed by the inode number of the locked file." | admit, A, mined |

Status changes this round: none to existing rows. New rows S161–S174 (S166, S168 `rejected`).

## Routed defects (round-30 closure §7) — disposition

| Defect | Disposition | Evidence |
|---|---|---|
| D1 blindness gate parser | fixed as C2: `tools/mori-blind-check.sh`, round-30 gate bytes untouched; its self-test carries no `CaseA210c` missing-list expectation | C2 receipts below |
| D2 A1 silent loosening | M2 above, citing QUALITY 25; A3 named as no precedent | this lesson |
| D3 QUALITY 93 cannot fail | QUALITY 94 supersedes it by name; QUALITY 92 recorded unmet at the round-30 tip | `corpus/QUALITY.md` 94 (`1d94055d`); wave-1 ScoutQuality92 re-ran 92's check: `pinned=8 limit_stated=no frozen=yes`, rc 1 |
| D4 entry "reports its version"; S159/S120 | corrected in place at both mentions and recorded in an appended section | `corpus/knowledge/earlyoom-invocation-scope-r30.md` (`1d94055d`) |
| D5 coverage-map row | added | `corpus/README.md:44` (`1d94055d`) |
| D6 X1/X2 dry-run flips | pinned as two cases in a new file; tip tool `PASS 2/2`, round-30 base tool `FAIL 0/2` | `tools/fixtures/mori-oom-killers/cases-r31-dryrun-flips.json`, `.ufo/waves/round-31/evidence/d6-dryrun-flips.txt` |
| D7 LOG for `713be294` | appended | `LOG.md` (`1d94055d`) |
| D8 stale SCORECARD counts | appended correction | `SCORECARD.md` (`1d94055d`) |
| D9 redacted tokens in history | noted; no history rewrite (operator-owned) | — |

## Carried (named, not repaired this round)

- C2 rule ambiguities found by wave-1 RealBriefsR29: a heading with words between `files` and `opened`, lead-in prose
  before the first entry, and a sub-heading inside a block are read literally by rule clauses 1 and 3; on the round-29
  briefs the literal reading yields missing-list hits a looser reading would not. No fixture pins those shapes.
- `tools/mori-blind-check.sh` edge cases outside the 27 fixtures (residual CriticC2Tip): setext and indented headings,
  CRLF line endings, a tab after `-`, and `../` through an allow glob; a fenced `# files opened` line opens a block (residual
  ReviewC2Tool F1); named in SKILL, not fixed under C2.
- The two kept round-30 detectors have false positives and negatives (wave-1 ReviewGateR30Lines F1–F6); rule clause 6
  keeps them unchanged.
- MutFixturePower: three mutants survive the 16 original fixtures (reverse opener, `+ ` marker, prose not closing);
  the A1 fixtures A01, A03/A04 and A07 target those shapes.
- The census probe itself is unchanged (FR5 stays frontier); under the inline driver it reports `WATCHDOG_ABSENT`.
- Unrouted round-30 carries named by ScoutCarriedDebt: the uncounted last-invocation send, retention blindness to
  unit/pid/cmdline shapes, the stale `fleet-ledger` pointer at `corpus/README.md:337`, QUALITY 89 vacuous on an
  absence-free lesson.

## Census and sweep

- Round start (23:41Z, `8baccf4a`): ten W04, `mori ok`, exit 0 (`.ufo/waves/round-31/evidence/census-start.txt`).
- Round end (`.ufo/waves/round-31/evidence/census-end.txt`): twelve W04 — the ten pre-existing plus S166 and S168, both
  `rejected` rows naming the rows that already carry their URLs — `mori ok`, exit 0.
- Fleet-root misroot sweep (`git -C /home/vgpnk/Projects/shokunin status --porcelain`): untracked `AGENTS.md`,
  `bm.json`, `live_s228.html`, `nama.html`, `s395.txt`, `tf_bavelas.html`, `wb2.html`, `write`; none names mori round
  31 and all predate the wave-1 dispatch, so none was moved.
