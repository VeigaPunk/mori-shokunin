# ReopenS128: re-open of SOURCES row S128 at tip 5f00fd045c137b7e3835506d69946cfd9d010eb5

Seat: MoriR27.ReopenS128 (leaf; no subagents, no background jobs). Lane: /home/vgpnk/Projects/shokunin/mori-shokunin (branch master). Tip checked: 5f00fd04. Entering tip: fc09f96c. Scratch bytes: /fast/scratch/hyaku/mori-r27/ReopenS128/.

Notation: `adj:N` is line N of the man7 proc_pid_oom_score_adj(5) HTML (sha256 769edf3b…); `score:N` is line N of the man7 proc_pid_oom_score(5) HTML (sha256 6169628d…); `base.c:N` is fs/proc/base.c at v7.2 (sha256 cef1a2cf…); `oom_kill.c:N` is mm/oom_kill.c at v7.2 (sha256 452f1348…); `fork.c:N` is kernel/fork.c at v7.2; `SOURCES:N` is corpus/SOURCES.md at the tip; `knowledge:N` is corpus/knowledge/oom-victim-selection-r27.md; `lesson:N` is corpus/lessons/round-27.md. Every line number below was checked with `grep -n` or a line-numbered read on the fetched bytes.

## 0. Summary

- The bytes reproduce the row. The man7 adj page (11,680 B), the man7 score page (7,955 B) and S127 base.c (98,196 B) return HTTP 200 and match the sha256 values in SOURCES:134. Every anchor line number and every quoted phrase resolves on those bytes (section 3).
- S128 is a new id at the tip (absent at the entering tip). No older row cites either man page. The row-identity check does not list S128 (section 2).
- One HIGH defect. The `teaches` cell says the inheritance and privilege sentences "belong to the legacy oom_adj file, not to oom_score_adj". The kernel gives oom_score_adj its own privilege floor and copies it at fork (F1).
- Three MEDIUM defects. The totalpages scaling and the 3% absence rest on mm/oom_kill.c, which the row does not anchor or name in its scope (F2, F3). The 6.20 claim has no URL or hash (F4).
- Eight lane statements cite S128 by id (section 6). One is wrong (the row's `teaches`). Two hold but have citation gaps (knowledge:72, lesson:71). Three hold outright (knowledge:1, knowledge:70, CriticC1Counter:125). Two are fixture descriptions with no landed-bytes claim (CriticC1Counter:55, :59).

## 1. Fetched bytes, hashes and sizes

| Object | Access (UTC, this seat) | HTTP / bytes | sha256 (computed here) | Row or Gate records | Result |
|---|---|---|---|---|---|
| man7 proc_pid_oom_score_adj(5) | 2026-10-22T17:09:45Z | 200 / 11,680 | 769edf3b9c054934db07f16173297fc5fd63c3a4c807682355f08fa45cde80a9 | SOURCES:134 same value | match |
| man7 proc_pid_oom_score(5) | 2026-10-22T17:09:46Z | 200 / 7,955 | 6169628d8a2cdc512795cfda74f3598d5b7a25e5b71921d4088c0539cf71b2bc | SOURCES:134 same value | match |
| S127 fs/proc/base.c at v7.2 | 2026-10-22T17:10:01Z | 200 / 98,196 | cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6 | SOURCES:134 same value | match |
| mm/oom_kill.c at v7.2 (for the S003 lines the knowledge entry cites) | 2026-10-22T17:11:07Z | 200 / 34,311 | 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e | knowledge:1 (S003 sha256) same value | match |
| man-pages 6.20 proc_pid_oom_score_adj.5, git blob at tag man-pages-6.20 (not named in the row) | 2026-10-22T17:16:21Z | 200 / 4,212 | 16a0d4b50deca2828d840350262d936f70934272a276b96c750af050f31161f3 | w1 report SrcManProcOomScoreAdj.md:94-96 same value | match |
| man-pages 6.20 proc_pid_oom_score.5, git blob (not named in the row) | 2026-10-22T17:16:21Z | 200 / 1,899 | 95c707bd3b4f2d8615085ac5a1bdacbeb5d975cfb94371dcfd4bf33e239f50ea | SrcManProcOomScoreAdj.md:94-96 same value | match |
| man-pages-6.20.tar.gz (not named in the row) | 2026-10-22T17:12:05Z | 200 / 2,805,991 | 46f325713f2fd75c8d1f4fa42748153526a44846806d37028fab85cd0143de46 | none | recorded here |
| man-pages-6.19.tar.gz (the man7 HTML colophon names it, adj:165) | 2026-10-22T17:12:07Z | 200 / 2,797,527 | fc0c620f…5572 (full value in the scratch directory) | adj:165 names the tarball | recorded here |

- Tarball members, byte for byte: man/man5/proc_pid_oom_score_adj.5 is 4,216 B with sha256 a8e996dd3717e373419906742326cce8606638b50fa778c01efc35db7c52755a in both the 6.19 and 6.20 tarballs. man/man5/proc_pid_oom_score.5 is 1,903 B with sha256 b29c3242c23d49eb47dbd0fc847e90e1619aa851879381b8a2dd57951dfdefcf in both. So the 6.19 rendering is not behind 6.20 for these two pages.
- The git.kernel.org 6.20 blobs differ from the tarball members only in the `.TH` date. The blob has `(date)` at line 7 and the tarball has `2026-02-08`. Line numbers are identical.
- The Gate entry (lesson:71) records no hash. Lesson:65 defers the hashes to the wave-1 seat report. That report records the three man7 and base.c hashes at SrcManProcOomScoreAdj.md:23, and the 6.20 hashes at :94-96. All of them match the values above.
- Timestamps. The row (SOURCES:134) and the Gate (lesson:71) say 2026-10-22T15:46:37Z. I could not reproduce that time. The bytes and hashes are identical at 17:09Z, so the content is stable across the two fetches.

## 2. Row identity and duplicates

- At the entering tip, SOURCES.md ends at S126. `git show fc09f96c:corpus/SOURCES.md | grep -n '^| S12[5-9] \|^| S13[0-3] '` shows only S125 and S126. `git log -S'| S128 |' -- corpus/SOURCES.md` returns one commit, 126e192 (subject "SOURCES S127-S132"), so S128 was added once and is not a reused id.
- `git grep -n 'man5\|proc_pid\|oom_score' fc09f96c -- corpus/SOURCES.md` returns S005 (a tracepoint field list) and S097 (proc_pressure(5), HTTP 404). No older row names either proc oom man page. The man7 URLs in SOURCES:134 are unique in the registry.
- `python3 -I -B .ufo/waves/round-27/check-row-identity.py 5f00fd045c137b7e3835506d69946cfd9d010eb5` prints `rows=141 changed=5 removed=0 bad=0` and names S090, S093, S096, S097 and S101. S128 is not listed, so its non-mutable cells equal its first-published cells.
- proc.rst (row S082) is a different file. Its sha256 prefix e760f716 matches S082, and S082's scope is mountinfo only. Not a duplicate.
- Verdict: the row is not a duplicate of an older row's file.

## 3. Anchor verdicts (SOURCES:134, `anchor` cell)

man7 adj page (`adj:N`):

| Anchor in row | Bytes | Verdict |
|---|---|---|
| :72 "(since Linux 2.6.36)" | adj:72 `/proc/pid/oom_score_adj (since Linux 2.6.36)` | holds |
| :86-88 3% root clause | adj:86 "There is an additional factor included in the badness", adj:87 "score: root processes are given 3% extra memory over other", adj:88 "tasks." | holds |
| :102-103 adjustment "added" | adj:102 "The value of oom_score_adj is added to the badness score", adj:103 "before it is used to determine which task to kill." | holds |
| :104-110 range and -1000 | adj:104-105 "Acceptable values range from -1000 … +1000"; adj:108-110 "The lowest possible value, -1000, is … since it will always report a badness score of 0." | holds |
| :122-127 oom_adj scaling | adj:122-124 "Its value is scaled linearly with oom_score_adj"; adj:126-127 write-through | holds |
| :145-149 inheritance and privilege | adj:146 "inherits its parent's oom_adj setting"; adj:147 "privileged (CAP_SYS_RESOURCE)"; adj:148-149 "always increase its own oom_adj setting" | holds. All three sit under the oom_adj heading at adj:134 |
| :175 footer | adj:175 footer, "Linux man-pages 6.19" and "2026-02-08" (the bytes use runs of spaces) | holds |
| not anchored: badness 0 to 1000 | adj:77-78 "…assigns a value to each candidate / task ranging from 0 (never kill) to 1000 (always kill)" | omission (F5) |

man7 score page (`score:N`):

| Anchor in row | Bytes | Verdict |
|---|---|---|
| :72-80 since 2.6.11, factors | score:72 "(since Linux 2.6.11)"; score:78 factor list; score:80 "whether the process is privileged (-)." | holds. Line 80 is an oom_score factor, not the CAP_SYS_RESOURCE write rule |
| :97-98 reflects the adjustment | score:97-98 "The oom_score also reflects the adjustment specified by the oom_score_adj or oom_adj setting" | holds |
| :120 footer | score:120 footer | holds |

S127 fs/proc/base.c at v7.2 (`base.c:N`):

| Anchor in row | Bytes | Verdict |
|---|---|---|
| 583-601 proc_oom_score | 583 signature; 586 `totalpages = totalram_pages() + total_swap_pages`; 590 `badness = oom_badness(task, totalpages);`; 591-595 comment; 596-597 `if (badness != LONG_MIN)` and the formula | holds |
| :586 totalpages | base.c:586 | holds |
| :596-597 formula | base.c:597 `points = (1000 + badness * 1000 / (long)totalpages) * 2 / 3;` | holds |
| :591-594 [0, 2000] comment | the words "[0, 2000] range" are at base.c:593 | holds |
| 1089-1101 oom_adj read scaling | base.c:1097-1098 `oom_adj = (task->signal->oom_score_adj * -OOM_DISABLE) / OOM_SCORE_ADJ_MAX;` | holds |
| 1213-1231 oom_adj write scaling | base.c:1226-1229 mapping; base.c:1231 `__set_oom_adj(file, oom_adj, true)` | holds |
| 1131-1133 CAP_SYS_RESOURCE floor gate, -EACCES | base.c:1131 `if ((short)oom_adj < task->signal->oom_score_adj_min &&`; 1132 `!capable(CAP_SYS_RESOURCE)) {`; 1133 `err = -EACCES;` | holds |
| 1156-1157 floor set by a privileged writer | base.c:1156 `if (!legacy && has_capability_noaudit(current, CAP_SYS_RESOURCE))`; base.c:1157 `task->signal->oom_score_adj_min = (short)oom_adj;` | holds |
| 1175-1176 shared-mm copy | base.c:1174 `p->signal->oom_score_adj = oom_adj;`; base.c:1175-1176 the same floor condition and copy | holds |
| 1242-1256 oom_score_adj read | base.c:1247 `short oom_score_adj = OOM_SCORE_ADJ_MIN;`; base.c:1256 closing brace | holds |
| 1275-1279 range check, -EINVAL | base.c:1275-1277 range condition with `err = -EINVAL;` at 1277; base.c:1278-1279 jump and brace | holds |
| 3351-3353 file modes | base.c:3351 `ONE("oom_score", S_IRUGO, proc_oom_score)`; base.c:3352 oom_adj `S_IRUGO|S_IWUSR`; base.c:3353 oom_score_adj `S_IRUGO|S_IWUSR` | holds (the tid table at base.c:3706-3708 repeats the modes) |

6.20 statement blocks (row: "adj 6.20:25-26,46-47,53,101-105"; troff members of the tarball and the git blob, identical line numbers):

| Lines | Bytes | Verdict |
|---|---|---|
| 25-26 | "There is an additional factor included in the badness score: root / processes are given 3% extra memory over other tasks." | holds, but no URL or hash in the row (F4) |
| 46-47 | "Acceptable values range from \-1000 / (OOM_SCORE_ADJ_MIN) to +1000 (OOM_SCORE_ADJ_MAX)." | holds (same F4 caveat) |
| 53 | "since it will always report a badness score of 0." | holds (same F4 caveat) |
| 101-105 | 101 "a new process inherits its parent's", 104 "A process must be privileged", 105 ".RB ( CAP_SYS_RESOURCE )" | holds (same F4 caveat) |

Quotes in the Gate entry (lesson:71): "root processes are given 3% extra memory" is verbatim at adj:87. The range sentence is at adj:104-105. Both hold.

## 4. Scope verdicts (SOURCES:134, `scope` cell)

- "-1000..+1000 range", "-1000 reading", "added-versus-scaled adjustment wording", "oom_adj legacy scaling", "owner-only write mode": hold (adj:102-110, adj:122-127, base.c:1275-1279, base.c:596, base.c:3353). The page is silent on the file mode, and the row says it compares against the code, so that is correct.
- "the 3% root clause": the page text holds (adj:86-88). The absence of a 3% term is shown only in mm/oom_kill.c. The row's stated comparator is S127 alone (see F3).
- "inheritance and the CAP_SYS_RESOURCE rule are documented only inside the oom_adj paragraph": holds. `grep -n -i 'inherit\|CAP_\|privileg'` on the adj page returns adj:146-147 only. On the score page it returns score:80 only, and that is an oom_score factor.
- Exclusions ("not kill-time victim ordering", "not OOM_SCORE_ADJ_MIN exclusion", "not this host's values", "not earlyoom's selection logic"): no statement depends on them.
- "(the v7.2 code they describe is S127)": overstated. The pages describe the interface across releases (since 2.6.11 and 2.6.36) and do not mention v7.2 (F6).
- Scope against teaches: the `teaches` cell uses oom_badness (the kill-time score, mm/oom_kill.c:232-234), which the scope does not name (F2, F3).

## 5. Teaches cell, clause by clause (SOURCES:134, `teaches` cell)

1. "oom_score_adj is the writable -1000..+1000 preference": holds (adj:73-74 "This file can be used to adjust the badness heuristic"; adj:104-105; base.c:3353 `S_IWUSR`).
2. "whose value the kernel scales by totalpages/1000": holds on the bytes (oom_kill.c:233 `adj *= totalpages / 1000;`). Not anchored in S128 or S127, and S127 excludes the oom_badness body (SOURCES:133 "not the oom_badness body"). Unsupported as written (F2).
3. "oom_score is a read-only [0, 2000] export": holds (base.c:3351 `S_IRUGO`; base.c:593 comment).
4. "folding that preference in": holds (base.c:590 calls oom_badness; oom_kill.c:234 `points += adj;`; score:97-98). Same anchor gap as clause 2.
5. "the page's inheritance and privilege sentences belong to the legacy oom_adj file": holds as a statement about placement (adj:134 heading; adj:145-149).
6. "…not to oom_score_adj": wrong as a statement about the contract. The kernel gives oom_score_adj a privilege floor (base.c:1131-1133; the floor is set by a privileged writer at base.c:1156-1157 and base.c:1175-1176; the write path is base.c:1281). The kernel copies oom_score_adj and its floor at fork (fork.c:1768-1769 in `copy_signal`; fork.c:1963-1964 in `copy_oom_score_adj`, called at fork.c:2558). The page's silence is a documentation gap, not an absent rule (F1).

## 6. The eight lane statements that cite S128 (`git grep -n S128 5f00fd04`)

| # | Location | Statement (short form) | Verdict |
|---|---|---|---|
| 1 | SOURCES:134 (the row) | `teaches` clause 6, "not to oom_score_adj" | WRONG (F1) |
| 2 | SOURCES:134 (the row) | anchors, hashes, sizes, scope items | holds, except F2 to F6 |
| 3 | knowledge:1 (source header) | "S128 (man-pages 6.19 proc_pid_oom_score_adj(5) and proc_pid_oom_score(5) — the documented contract and where it differs from the code)" | holds |
| 4 | knowledge:70 | "the man page says the adjustment is 'added' (S128 …, adj page :102-103) while the code scales it by memory size" | holds (adj:102-103; oom_kill.c:233) |
| 5 | knowledge:72-73 | "the man page's 'root processes are given 3% extra memory' has no implementation in v7.2 oom_badness (S128 adj page :86-88 against S003 mm/oom_kill.c:226-235)" | holds on the bytes. The quote is verbatim (adj:87). The absence is true: a grep of the whole v7.2 oom_kill.c (1257 lines) finds no `root`, `3%`, `CAP_SYS_ADMIN` or `/ 100`, and oom_badness at oom_kill.c:199-237 has no privilege term. Citation gap: S003's anchor cell (SOURCES:9) lists none of 199-237 (F2) |
| 6 | lesson:71 (Gate row) | "adj page `:104-105` the range -1000 to +1000; `:86-88` 'root processes are given 3% extra memory' (no v7.2 implementation)" | holds. The line numbers and quote are right. The parenthesis rests on mm/oom_kill.c, which the Gate does not cite (F7). The Gate records no hash (section 1) |
| 7 | .ufo/waves/round-27/w1/CriticC1Counter.md:55 (G1) | "entry is the single line `source: S127 S128 S129`" | Not a landed-bytes claim. G1 is a fixture commit in the counter's test table, "what the commit holds". No finding |
| 8 | .ufo/waves/round-27/w1/CriticC1Counter.md:59 (G5) | "existing rows S114, S115 and S118 are renumbered to S127, S128 and S129" | Not a landed-bytes claim. G5 is a fixture commit. The tip does not renumber: S114, S115 and S118 keep their ids at SOURCES:120, :121 and :124. No finding |
| 9 | .ufo/waves/round-27/w1/CriticC1Counter.md:125 | landing form: entry line 1 writes "S127 (…), S128 (…), S129 (…)" individually | Guidance, and it holds. knowledge:1 writes S127, S128 and S129 individually, with no range |

(The grep returned eight lines. Row 2 is the same line as row 1, so the table lists nine verdicts for eight hits.)

## 7. Findings with exact old and new text

**F1 (HIGH). The `teaches` cell gives a false contract for oom_score_adj.**
Evidence: base.c:1131-1133, base.c:1156-1157, base.c:1175-1176, base.c:1281, fork.c:1768-1769, fork.c:1963-1964. The lane's own knowledge entry states the same rule correctly (knowledge:92-97: "only a writer with `CAP_SYS_RESOURCE` may go below that floor", and "`fork` copies both the value and its floor"). SKILL.md:741 also states it correctly. The w1 analysis (SrcManProcOomScoreAdj.md, sections "Inheritance across fork and execve" and "Privilege rule") called this "a gap, not a contradiction". The landed `teaches` cell is identical to that draft's `teaches` cell, and it turned the gap into a contradiction.
- Old (SOURCES:134, `teaches`): "and the page's inheritance and privilege sentences belong to the legacy oom_adj file, not to oom_score_adj."
- New: "and the page states inheritance and the CAP_SYS_RESOURCE rule only in its legacy oom_adj section (adj:145-149); the kernel still copies oom_score_adj and its floor at fork (kernel/fork.c:1768-1769, 1963-1964) and refuses an unprivileged write below the floor (fs/proc/base.c:1131-1133), so the page's silence is a documentation gap, not an absent rule."

**F2 (MEDIUM). The scaling and folding claims in `teaches` have no anchor in the row.**
Evidence: oom_kill.c:228-229 (rss, swap, page tables), oom_kill.c:232-234 (`adj *= totalpages / 1000;` at 233, `points += adj;` at 234), oom_kill.c:199-237 (the function). The S127 scope excludes "the oom_badness body" (SOURCES:133). The S003 anchor cell (SOURCES:9) reads "mm/oom_kill.c:447,935-936,945; tag v7.2". The companion anchor that the w1 report proposed (SrcManProcOomScoreAdj.md:123) did not land. Note that its range "191-237" starts at the kerneldoc (oom_kill.c:190-198); the function is 199-237.
- Old (SOURCES:9, S003 `anchor` cell): "mm/oom_kill.c:447,935-936,945; tag v7.2"
- New: "mm/oom_kill.c:447,935-936,945; oom_badness mm/oom_kill.c:199-237 (rss sum :228-229; OOM_SCORE_ADJ_MIN exclusion :217-222; adj scaling :232-234 `adj *= totalpages / 1000; points += adj;`); select_bad_process compare :339-340; tag v7.2; sha256 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e"
- Also in SOURCES:134 `teaches`, after "scales by totalpages/1000": add "(mm/oom_kill.c:232-234, row S003)".

**F3 (MEDIUM). The 3% comparison names the wrong comparator.**
Evidence: the scope says "compared with the v7.2 kernel code that enforces it (that code is row S127)". The absence of a 3% term is in oom_kill.c, not in base.c. knowledge:72-73 cites S003 for it, and SOURCES:9 does not register those lines (F2).
- Old (SOURCES:134, `scope`): "compared with the v7.2 kernel code that enforces it (that code is row S127)"
- New: "compared with the v7.2 kernel code that enforces it (fs/proc code: row S127; oom_badness in mm/oom_kill.c, which holds the totalpages scaling and has no 3% term: row S003, mm/oom_kill.c:199-237)"

**F4 (MEDIUM). The 6.20 claim has no source in the row.**
Evidence: the bytes in section 1 (the git blobs and the tarball members). The row names no URL and no hash for 6.20.
- Old (SOURCES:134, `anchor` cell): "man-pages 6.20 sources carry the same four statement blocks (adj 6.20:25-26,46-47,53,101-105)"
- New: "man-pages 6.20 carries the same four statement blocks (adj 6.20:25-26,46-47,53,101-105; score 6.20:28): https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_oom_score_adj.5?id=man-pages-6.20 (4,212 B, sha256 16a0d4b50deca2828d840350262d936f70934272a276b96c750af050f31161f3) and …/plain/man/man5/proc_pid_oom_score.5?id=man-pages-6.20 (1,899 B, sha256 95c707bd3b4f2d8615085ac5a1bdacbeb5d975cfb94371dcfd4bf33e239f50ea); the tarball https://mirrors.edge.kernel.org/pub/linux/docs/man-pages/man-pages-6.20.tar.gz (sha256 46f325713f2fd75c8d1f4fa42748153526a44846806d37028fab85cd0143de46) has members byte-identical to the 6.19 tarball (sha256 a8e996dd… and b29c3242…)."

**F5 (LOW). The row omits the man page's own 0-to-1000 badness statement.**
Evidence: adj:77-78. knowledge:69-70 attributes the 0-to-1000 reading only to proc.rst.
- Old (SOURCES:134, `anchor` cell): "adj page:72 (since 2.6.36), :86-88 (3% root)"
- New: "adj page:72 (since 2.6.36), :77-78 (badness 0 to 1000), :86-88 (3% root)"

**F6 (LOW). The source cell overstates the code link.**
- Old (SOURCES:134, `source` cell): "(the v7.2 code they describe is S127)"
- New: "(the v7.2 code that enforces them is S127)"

**F7 (LOW). The Gate entry rests a claim on the wrong row.**
- Old (lesson:71): "(no v7.2 implementation)"
- New: "(no v7.2 implementation: mm/oom_kill.c:199-237, S003)"
- Optional: copy the three man7 and base.c sha256 values into the Gate row from SrcManProcOomScoreAdj.md:23, so the Gate carries its own hashes.

## 8. Adjacent observations (outside S128; for the owners of the other rows)

- A1. The lane's identity check exits 1 at the tip: `rows=141 changed=5 removed=0 bad=0`, changed S090 (anchor, teaches), S093 (anchor), S096 (teaches), S097 (anchor, teaches), S101 (teaches). Not S128.
- A2. knowledge:70 cites proc.rst:1761-1763 for the 0-to-1000 reading. The bytes hold: proc.rst:1761-1762 reads "ranging from 0 / (never kill) to 1000 (always kill)". The S082 row (SOURCES:88) does not list these lines; it lists section 3.5 and the field table.
- A3. The S003 anchor cell (SOURCES:9) lists no oom_kill.c line that the knowledge entry cites. Examples: knowledge:61-64 (228-229, 232-234, 160-167, 216-222, 340), knowledge:73 (226-235) and knowledge:75 (998-1006, 1040-1053). F2 is the fix for the oom_badness lines.
- A4. SKILL.md:722 lists the grounding sources for the Round27 section and omits S128. SKILL.md:740 relies on knowledge Fact 2, which cites S128.
- A5. lesson:13 says "proc.rst and the man page disagree with the code in three places (Fact 2)". The three items match knowledge:69-73. Holds.

## 9. Verification gaps and residual risk

- I could not reproduce the fetch times 15:46:37Z to 15:46:38Z in the row and Gate. The bytes and hashes did reproduce at 17:09Z to 17:16Z.
- I did not re-fetch the refs/tags listing (86,480 B) that the w1 report cites.
- For the kernel-side claims I read base.c, fork.c, oom_kill.c and proc.rst. I did not check the S127 uapi oom.h or the other S127 anchors beyond those listed in section 3.
- The "no 3% term" claim is a grep over all 1,257 lines of v7.2 oom_kill.c plus a read of oom_badness. I did not search other kernel files. The claim is scoped to oom_badness, so that is enough for the text.
- The CriticC1Counter G1 and G5 fixtures were not reproduced. They describe test commits, not the landed bytes.
- Residual risk. F1 stays in the registry until SOURCES:134 changes. The knowledge entry and SKILL.md already state the correct floor and inheritance rules, so the lane's guidance is right and only the registry row is wrong.

## 10. Tooling, writes and bounds

- Installs or upgrades: none. Tools used: curl, tar, sha256sum, cmp, diff, grep, sed (print only), git (read-only: show, grep, log, rev-parse) and python3 -I -B for the frozen identity check (read-only). No pacman, uv or npm.
- Writes: this report, and scratch files under /fast/scratch/hyaku/mori-r27/ReopenS128/.
- No lane edits, no git writes, no jj, no units touched, no signals sent, no omp runs, no settings or MCP files read or written.
