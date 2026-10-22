# ReopenS127: wave-2 re-open of SOURCES row S127

Seat: MoriR27.ReopenS127 (leaf; no subagents, no background jobs). L1: MoriR27.
Lane: /home/vgpnk/Projects/shokunin/mori-shokunin. Checked tip: 5f00fd045c137b7e3835506d69946cfd9d010eb5 (master). Entering tip: fc09f96c. All fetches dated 2026-10-22 (UTC).

## 1. Summary

- Source URLs, byte counts and sha256 for the three named files: all hold (3 of 3). Mirror cross-check: holds (2 of 2).
- Anchors: all hold (23 of 23). Two range nits, no wrong line number.
- Gate quote (round-27.md:70, base.c:597): holds, verbatim.
- Duplicate-file and identity checks: hold. S127 is absent at fc09f96c and first appears in commit 126e192.
- teaches cell: two clauses need correction (F2 medium, F3 low-medium).
- scope cell: one wrong pointer (F1 medium) and one reason that lives in S003 (F4 low).
- Lane statements citing S127 (23 checked, section 7): 14 hold as written; 5 need correction (C1-C5); 4 hold with a qualifier, are unverified, or need evidence hygiene (C11, C17, C22, C23).
- No high-severity finding.

## 2. Method and tool record

- Tip text was read with read-only git only (`git show`, `git grep -n`, `git ls-tree`, `git log -S`, `git cat-file`). No jj command. No git write. No lane file edited; this report is the only write.
- Three citing files differ between the working copy and the tip (section 9). Verdicts are for tip bytes. I compared with `cmp` and `diff` against `git show` output.
- Fetches used ordinary curl 8.23.0. curl was already installed on the host; this seat installed or upgraded nothing. Every request returned HTTP 200 with no redirect. No challenge page appeared; no browser was used.
- Hashes: sha256sum. Line checks: `grep -n -F` on the downloaded bytes for quoted lines, and read-tool ranges for anchored blocks.
- Scratch: /fast/scratch/hyaku/mori-r27/ReopenS127/ (fetched bytes, tip copies, command outputs).

### 2.1 Fetched bytes

| Source | Access (UTC) | HTTP | Bytes | sha256 | Equal to row? | Equal to wave-1 report? |
|---|---|---|---|---|---|---|
| raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c | 2026-10-22T17:09:49Z | 200 | 98,196 | cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6 | yes | yes (SrcProcBaseOomScore.md:30) |
| git.kernel.org .../plain/include/uapi/linux/oom.h?h=v7.2 | 2026-10-22T17:09:49Z | 200 | 526 | 6b00b4d0648bcdc9d6be7ea8a33b8e6b842c063e7b2b71bdabd757de773896ae | yes | yes (:31) |
| git.kernel.org .../plain/kernel/fork.c?h=v7.2 | 2026-10-22T17:09:49Z | 200 | 85,725 | 359882ea981b58f5289293e5644f7c0085a8350e4f1937f39dcb94ae1cd0dd1d | yes | yes (:32) |

Cross-checks (URLs the row does not name):
- raw.githubusercontent.com v7.2 include/uapi/linux/oom.h and kernel/fork.c: same sha256 as the git.kernel.org copies. This settles the wave-1 "[INFERENCE]" about fork.c (SrcProcBaseOomScore.md:126).
- api.github.com git/ref/tags/v7.2: HTTP 200, annotated tag object 237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63.
- raw mm/oom_kill.c at v7.2 (the S003 file): 34,311 B, sha256 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e. Equal to knowledge entry line 1 and wave-1 report line 33.
- raw Documentation/admin-guide/cgroup-v2.rst at v7.2 (the S092 file): 133,236 B, sha256 a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad. Equal to the S092 row's sha prefix (SOURCES.md:98).
- docs.kernel.org admin-guide/cgroup-v2.html (the S002 URL): 172,967 B, sha256 b478c1bae99899df476d6b4989cbb516f7ca93c5f009cdff64b802bbc24f3d4b, accessed 17:14:13Z. Used only for C1 in section 7.

Hash record in the Gate: round-27.md:70 records no sha256. Its header (round-27.md:65-66) says the full Gate blocks, with hashes, are in the wave-1 report. SrcProcBaseOomScore.md:30-33 records four hashes. All four equal the fetched bytes.

## 3. Row S127 fields (SOURCES.md:133)

- id S127: holds. `grep -c '^| S127 |'` is 0 at fc09f96c (last row S126, line 132 of that revision) and 1 at tip. First added by commit 126e192 (`git log -S`).
- kind code, tier A, status mined: consistent with other code rows (S003 uses the same values). Holds.
- opened 2026-10-22: holds (my access 17:09:49Z; wave-1 access 15:46:35Z for base.c).
- recheck on-release: consistent with S003. Holds.
- used-by lists corpus/knowledge/oom-victim-selection-r27.md. That file does cite S127. It omits corpus/lessons/round-27.md (line 70) and SKILL.md (line 722), which also cite S127 by id. See F9.
- Duplicate-file check: `git grep -n` at tip for fs/proc/base, uapi/linux/oom, kernel/fork, proc_oom and oom_score finds no other row naming these files. Other rows name different files: S003 mm/oom_kill.c, S005 include/trace/events/oom.h, S082 Documentation/filesystems/proc.rst, S128 man pages. Holds.

## 4. Row S127 anchors (anchor cell, SOURCES.md:133)

Each line is one claim from the anchor cell. "Holds" means the cited bytes say what the cell says.

| # | Anchor as written | What the bytes say | Verdict |
|---|---|---|---|
| A1 | base.c:583-599 proc_oom_score | function runs 583-602; the cited span ends at the seq_printf line (599) | holds (span omits the return) |
| A2 | :586 totalpages = totalram_pages() + total_swap_pages | line 586 | holds |
| A3 | :590 oom_badness call | line 590 | holds |
| A4 | :592-597 LONG_MIN skip, formula, exported [0, 2000] | comment 592-595 with "[0, 2000]" at 593; `if (badness != LONG_MIN)` at 596 (grep -n); formula at 597 (grep -n) | holds |
| A5 | :1106-1186 __set_oom_adj | function runs 1106-1187; 1186 is `return err;` | holds (span one line short) |
| A6 | :1118-1122 legacy path vs current value | 1118-1119 compare against task->signal->oom_score_adj with !capable; 1120 -EACCES | holds |
| A7 | :1131-1135 oom_score_adj_min floor, -EACCES | 1131-1133 check (grep -n at 1131); 1133 -EACCES | holds |
| A8 | :1143-1153 MMF_MULTIPROCESS mm grab | 1143 `if (!task->vfork_done)`; 1147 MMF test (grep -n); 1149 mmgrab | holds |
| A9 | :1155-1158 assignment, min update, tracepoint | 1155 assignment; 1156-1157 min update under CAP_SYS_RESOURCE; 1158 tracepoint | holds |
| A10 | :1164-1177 mm-sharer propagation, kernel-thread and global-init skip | 1164 loop; 1165-1166 same_thread_group skip; 1168-1170 kernel-thread and global-init skip; 1173 `!p->vfork_done && process_shares_mm`; 1174-1176 copy | holds |
| A11 | :1242-1254 read | function 1242-1256; 1252 reads task->signal->oom_score_adj | holds |
| A12 | :1275-1279 range check, -EINVAL | 1275-1276 range test (grep -n at 1275); 1277 -EINVAL | holds |
| A13 | :3351-3353 pid entries | 3351-3353 inside tgid_base_stuff (3282-3394) | holds |
| A14 | :3706-3708 task/tid entries | 3706-3708 inside tid_base_stuff (3641-3739) | holds |
| A15 | modes S_IRUGO; S_IRUGO plus S_IWUSR | 3351 oom_score S_IRUGO; 3352-3353 oom_adj and oom_score_adj S_IRUGO\|S_IWUSR | holds |
| A16 | oom.h:9-10 OOM_SCORE_ADJ_MIN (-1000), OOM_SCORE_ADJ_MAX 1000 | 9 `#define OOM_SCORE_ADJ_MIN	(-1000)`; 10 `#define OOM_SCORE_ADJ_MAX	1000` (grep -n) | holds |
| A17 | fork.c:1728 zalloc signal struct | 1728 `sig = kmem_cache_zalloc(signal_cachep, GFP_KERNEL);` | holds |
| A18 | fork.c:1768-1769 inheritance in copy_signal | 1768 `sig->oom_score_adj = ...`; 1769 `sig->oom_score_adj_min = ...` (grep -n); CLONE_THREAD early return at 1725-1726 | holds |
| A19 | fork.c:1949-1966 copy_oom_score_adj sets MMF_MULTIPROCESS, copies both | 1952 kernel-thread skip; 1956 CLONE_VM-only test; 1961 `mm_flags_set(MMF_MULTIPROCESS, tsk->mm)` (grep -n); 1963-1964 copies | holds; the MMF set is conditional (CLONE_VM, not CLONE_THREAD, not CLONE_VFORK) |
| A20 | tag v7.2 | refs/tags/v7.2 exists (section 2.1) | holds |
| A21 | base.c 98,196 B, sha cef1a2cf... | section 2.1 | holds |
| A22 | oom.h 526 B, sha 6b00b4d0... | section 2.1 | holds |
| A23 | fork.c 85,725 B, sha 359882ea... | section 2.1 | holds |

Gate quote (round-27.md:70, "base.c:596-597"): `points = (1000 + badness * 1000 / (long)totalpages) * 2 / 3;` equals base.c:597 exactly (`grep -c -F` = 1). It is under 25 words. Holds.

## 5. Row S127 teaches and scope (cells 5 and 7)

Teaches, clause by clause:
- "A task's oom_score is (1000 + badness*1000/totalpages)*2/3": holds (base.c:597).
- "0 when the task is unkillable or oom_score_adj is -1000": incomplete, and the full list lives outside S127. The 0 comes from `badness != LONG_MIN` (base.c:596). oom_badness (mm/oom_kill.c, S003) returns LONG_MIN in five cases: init or kernel thread (oom_unkillable_task at S003:160-167, returned at 204-205); no mm after find_lock_task_mm (207-209); oom_score_adj == -1000 (216-221); MMF_OOM_SKIP (217-218); in_vfork (219). The clause names two of the five. [F3]
- "a writer may set oom_score_adj only within -1000..1000": holds (base.c:1275-1279; the /proc write path only).
- "below oom_score_adj_min only with CAP_SYS_RESOURCE": holds (base.c:1131-1133).
- "with the write copied to every non-thread process sharing the mm": over-broad. The copy happens only when the writer's mm carries MMF_MULTIPROCESS (base.c:1143-1150). It skips kernel threads and global init (1168-1170) and processes still in vfork (1173). MMF_MULTIPROCESS is set at fork only for a clone with CLONE_VM that is neither a thread nor a vfork (fork.c:1956-1961). The sentence holds for an ordinary clone(CLONE_VM) child. It does not hold as written. [F2]

Scope, clause by clause:
- "how oom_score is rescaled from oom_badness and why -1000 reads 0": the "why" is S003:216-221. The same cell excludes the oom_badness body. [F4]
- "not cgroup memory.oom.group (S002)": wrong pointer. S002's row (SOURCES.md:8) covers memory events, memory.peak and hierarchy. Its anchors and teaches never name memory.oom.group. The v7.2 text is cgroup-v2.rst:1450-1466 (1450 "memory.oom.group"; 1466 "memory.oom.group values of ancestor cgroups."), in the S092 file. [F1]
- "the -1000..1000 write range", "the file modes", "the oom_score_adj_min floor with CAP_SYS_RESOURCE", and "how a write reaches other processes that share the mm (fork copy, MMF_MULTIPROCESS)": hold, and match the bytes.

## 6. Row verdict

The row's sources, hashes and anchors are accurate. Its teaches cell over-states the propagation rule and its 0-rule list is incomplete. Its scope cell has one wrong pointer. None of this changes a sourced number. Any correction to a first-published cell needs a superseding row (corpus/QUALITY.md:373-374 allows only status, recheck and used-by to change in place).

## 7. Lane statements that cite S127 (tip bytes)

| # | Location (tip) | Statement, short form | Verdict | Note |
|---|---|---|---|---|
| C1 | SOURCES.md:133 (S127 scope) | "not cgroup memory.oom.group (S002)" | wrong | F1 |
| C2 | SOURCES.md:133 (S127 teaches) | "0 when the task is unkillable or oom_score_adj is -1000" | incomplete; list is in S003 | F3 |
| C3 | SOURCES.md:133 (S127 teaches) | "copied to every non-thread process sharing the mm" | over-broad | F2 |
| C4 | SOURCES.md:133 (S127 scope) | "why -1000 reads 0" | the "why" is S003:216-221 | F4 |
| C5 | SOURCES.md:134 (S128 row) | "compared with the v7.2 kernel code that enforces it (that code is row S127)" | all 12 S127 pointers in S128's anchor cell hold (base.c :583-601, :586, :596-597, :591-594, :1089-1101, :1213-1231, :1131-1133, :1156-1157, :1175-1176, :1242-1256, :1275-1279, :3351-3353). But the 3% root clause and the totalpages/1000 scaling are not in S127; they are in S003:199-237 and :233-234 | incomplete pointer | F5 |
| C6 | knowledge entry line 1 | S127 described as "how /proc/<pid>/oom_score is derived, the oom_score_adj write rules and fork inheritance" | holds | |
| C7 | knowledge entry line 39 | "+300 on the exported value weighs like an oom_score_adj of about +450" (labelled INFERENCE) | holds: 2/3 x 450 = 300 | |
| C8 | knowledge entry lines 65-68 | formula; totalpages = RAM + swap; 0 for an excluded task; range 0 to 2000; 666 at adjustment 0; 800 at 200; about 6.7 per percent | holds. Range 0-2000 needs S003:233-236 (`points += adj;` then `return points;`, no clamp), so negative badness is possible. The host's 600 reading for earlyoom at -100 fits this; with a clamp it would read 666. The exclusion list is S003 (see C2) | |
| C9 | knowledge entry line 92 | "fork copies both the value and its floor" (fork.c:1768-1769, 1949-1966) | holds | |
| C10 | knowledge entry lines 96-98 | floor; going below it and moving it need CAP_SYS_RESOURCE (base.c:1131-1133, 1156-1157); range -1000 to 1000 (1275-1279) | holds | |
| C11 | knowledge entry lines 98-99 | "Here the floor is 100, because PID 1 wrote the user manager's 100 with privilege" | writer identity not verified (systemd code is outside S127). The mechanism holds: a CAP_SYS_RESOURCE writer sets the floor (base.c:1156-1157) | F6, unverified |
| C12 | knowledge entry line 190 | "tsukuroi's S119 and S127 are not mori's" | holds (tsukuroi SOURCES.md:133 at 157ee255 is a row about a mori file) | |
| C13 | knowledge entry lines 134-135 | ceiling 1466 at adjustment 200 assumes rss, swap and page tables stay within RAM plus swap | holds; labelled INFERENCE | |
| C14 | round-27.md:70 (Gate) | S127: URL; accessed 15:46:35Z; quote base.c:596-597; admit, A, mined | holds (quote exact; access time equals wave-1 report:30) | |
| C15 | round-27.md:89-90 | oom.h "folded into S127" | holds (oom.h is in the S127 source cell) | |
| C16 | SKILL.md:722 | grounding list includes S127 | holds | |
| C17 | SKILL.md:727-728 | ceiling (2000 + oom_score_adj) * 2 / 3 (1466 at adjustment 200), so a --prefer match added 300 | holds arithmetically. The premise is INFERENCE in the entry (line 135) but unlabelled in the SKILL row | F7 |
| C18 | SKILL.md:740 | "range 0-2000, and v7.2 has no root bonus" | holds (base.c:597; S003:199-237 has no root term) | |
| C19 | SKILL.md:741 | "only the legacy oom_adj file ratchets" | holds (base.c:1118-1122 refuses lowering below the current value; the non-legacy path checks the floor at 1131-1135) | |
| C20 | SCORECARD.md:1726 | counter statement: C1 met at the tip, unmet at fc09f96c | holds as a counter statement. `count-c1.sh 5f00fd04` prints `entry=present new_rows_cited=6 skill_rows=10`, C1=met, rc 0. `count-c1.sh fc09f96c` prints `entry=absent new_rows_cited=0 skill_rows=0`, C1=unmet, rc 1. The evidence file matches. Substance not assessed (W1 scope) | |
| C21 | .ufo/waves/round-27/contract.md:24; count-c1.sh:9 | S127 and above did not exist at the entering tip | holds (section 3) | |
| C22 | .ufo/waves/round-27/w1/SrcProcBaseOomScore.md:30-33 | hashes, byte counts and HTTP codes | hold (4 of 4 hashes equal the fetched bytes). Access times for oom.h, fork.c and mm/oom_kill.c read "15:47:2xZ", "15:48:0xZ", "15:47:5xZ", which are unfinished | F8 |
| C23 | SrcProcBaseOomScore.md:40-41 | quotes Q3 and Q4 | each line exists as cited (base.c:1131-1133; 1173-1174), but each quotation joins two or three source lines into one string | F8 |

Count: 14 hold as written (C6-C10, C12-C16, C18-C21); 5 need correction (C1-C5); 4 hold with a qualifier, are unverified, or need evidence hygiene (C11, C17, C22, C23).

## 8. Findings by severity

Corrections to first-published cells (F1-F5) cannot be made in place. QUALITY 81 (corpus/QUALITY.md:373-374) says a correction is a new row whose teaches opens `supersedes S0NN —`, with the old and new text logged in the lesson. The next free id is the one to use.

F1 (medium). Wrong pointer in the S127 scope cell (SOURCES.md:133).
- Old: `not cgroup memory.oom.group (S002)`
- New: `not cgroup memory.oom.group (S092: cgroup-v2.rst:1450-1466 at v7.2)`
- Evidence: rst v7.2 lines 1450 and 1466 (grep -n); S002 row text at SOURCES.md:8 has no memory.oom.group. The entry (lines 74-75) cites S092 for this text, and SKILL.md:732 cites the same rst file by URL. S092's anchor cell does not list 1450-1466, so the entry's body citation is the only place it appears. Decide whether to add it through a superseding row.

F2 (medium). The S127 teaches over-states the copy to mm sharers (SOURCES.md:133).
- Old: `below oom_score_adj_min only with CAP_SYS_RESOURCE, with the write copied to every non-thread process sharing the mm.`
- New: `below oom_score_adj_min only with CAP_SYS_RESOURCE; for a clone(CLONE_VM) child that is neither a thread nor a vfork, the write is copied to each non-thread process sharing that mm, except kernel threads, global init and processes still in vfork.`
- Evidence: base.c:1143-1150, 1164-1177; fork.c:1956-1961.

F3 (low-medium). The "0 when ..." clause is incomplete and cross-row (SOURCES.md:133 teaches; scope "why -1000 reads 0").
- Old: `0 when the task is unkillable or oom_score_adj is -1000`
- New: `0 when oom_badness returns LONG_MIN (S003 mm/oom_kill.c:204-221: init or kernel thread; no mm; oom_score_adj -1000; MMF_OOM_SKIP; in_vfork)`
- Evidence: S003 bytes at 160-167 and 204-222 (the S003 file at v7.2, sha256 452f1348...).

F4 (low). The "why -1000 reads 0" scope clause depends on S003, which the scope excludes (SOURCES.md:133 scope).
- Old: `how oom_score is rescaled from oom_badness and why -1000 reads 0`
- New: `how oom_score is rescaled from oom_badness and that -1000 reads 0 (the LONG_MIN return is S003:216-221, cited here, not restated)`

F5 (low-medium). S128 names S127 as the code for facts that S127 does not contain (SOURCES.md:134).
- Old teaches clause: `whose value the kernel scales by totalpages/1000`
- New: `whose value oom_badness scales by totalpages/1000 (S003 mm/oom_kill.c:233-234)`
- Old pointer: `the v7.2 kernel code that enforces it (that code is row S127)`
- New: add `the 3% root clause (absent from oom_badness, S003:199-237) is in S003, not S127`.

F6 (low, unverified). The "PID 1 wrote the user manager's 100" clause (knowledge entry lines 98-99).
- Old: `because PID 1 wrote the user manager's 100 with privilege`
- New: `because the writer that set the user manager's 100 held CAP_SYS_RESOURCE (writer identity not checked here)`
- The mechanism holds (base.c:1156-1157). The writer identity sits in systemd's exec path, which this seat did not read.

F7 (low). The ceiling rule lacks its INFERENCE label (SKILL.md:727-728).
- Add after "(1466 at adjustment 200)": `[INFERENCE: assumes a process's rss, swap entries and page tables stay within RAM plus swap; entry lines 134-135]`

F8 (low). Evidence hygiene in the wave-1 report (.ufo/waves/round-27/w1/SrcProcBaseOomScore.md).
- Lines 31-33: the access times "2026-10-22T15:47:2xZ", "2026-10-22T15:48:0xZ" and "2026-10-22T15:47:5xZ" are unfinished. Replace with the real times, or "time not recorded".
- Lines 40-41: quotes Q3 and Q4 join two or three source lines into one string. Show the lines separately, or mark the quote "joined".

F9 (low, observation). S127's used-by lists only the knowledge entry (SOURCES.md:133). Lesson round-27.md:70 and SKILL.md:722 also cite S127 by id. No written rule in corpus/README.md or corpus/QUALITY.md requires them. S082 lists a lesson in its used-by, so the convention varies. Decision for the lane owner.

F10 (low, observation). Dangling rule citation. The lesson cites "CORPUS.md Rules 2" at round-27.md:37 and :87. No CORPUS.md exists in the tip tree: `git ls-tree -r` finds no such path, and the root and corpus/ listings have none. Name the file that holds the rule, or quote the rule text.

## 9. Working copy and non-live mentions

- Working copy versus tip (`diff` against `git show` output): corpus/knowledge/oom-victim-selection-r27.md differs at tip lines 151-157 and 180-181 (decision-table text). SKILL.md has one row inserted after tip line 726 and changes text in the row at tip line 731. SCORECARD.md adds an uncommitted block at working lines 1736-1745 ("Round 27 measured outcome ... measured at 0becc421") that cites S127–S132. None of the S127-citing lines differs from tip text (knowledge lines 1, 39, 58, 66, 79, 92, 97, 190; SKILL.md 722, 727-728, 732, 740-741). The SCORECARD block is not at tip and is not verified here.
- Round-26 wave files that say the registry stops at S113 or S126 (for example .ufo/waves/round-26/w1/SrcEarlyoomTagHistory.md:226-227) were true when written. Not checked further.
- Round-27 wave-1 drafts that proposed "S127" for other sources (SrcManProcOomScoreAdj.md:115; SrcSystemdExecOomScoreAdjust.md:94; SrcSystemdUserService.md:123-125; SrcOmpBunOomAdj.md:187; ReviewS124Supersede.md:93; ReviewS117.md:180) were superseded by other rows (S128, S129, S130, S132, S133, S137). They are stale drafts, not registry claims.
- Tsukuroi's own S127 (tsukuroi SOURCES.md:133 at 157ee255) is a row in a different registry, about a mori file. This matches C12.

## 10. Incidental observations outside S127

- QUALITY 81 at tip: `python3 -I -B .ufo/waves/round-27/check-row-identity.py 5f00fd045c137b7e3835506d69946cfd9d010eb5` prints `rows=141 changed=5` and exits 1 (S090, S093, S096, S097, S101). QUALITY 81 says it must print changed=0, exit 0. Lesson M2 routes these five rows to wave 2 (round-27.md:40-42). S127 is not among them.
- S002 anchors do not match the bytes at the URL the row names. On 2026-10-22 the docs.kernel.org page has memory.peak at line 1356 and memory.events at line 1377; the row says 1418-1426 and 1448-1509. The v7.2 rst has memory.peak at 1440 and memory.events at 1468. S002 needs its own reopen.

## 11. Residual risk and verification gaps

- Not verified: systemd's exec path (F6); the fs/exec.c "writes neither field" claim (knowledge entry line 93, labelled INFERENCE, not an S127 claim); the host values and probe results in the entry (wave-1 evidence); S003 lines beyond those cited here; the uncommitted SCORECARD block.
- The wave-1 access times (15:46-15:48Z) and this seat's (17:09-17:15Z) differ. Equal sha256 values show the bytes did not change between the two access times.
- Host state: none read beyond lane files and public bytes. No oom_score_adj read or written. No process signalled. No unit touched.
- Checks for the integrator after any superseding row: `python3 -I -B .ufo/waves/round-27/check-row-identity.py <rev>` (S127 must not appear in the changed list) and `bash .ufo/waves/round-27/count-c1.sh <rev>` (C1 must stay met).
