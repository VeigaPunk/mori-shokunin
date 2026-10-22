# SupersedeS128 — S128 row: first-published cells, re-open of the man pages, the S149 superseding row, Gate line, QUALITY 77 sweep

seat: MoriR28.SupersedeS128 (leaf; no subagent dispatch; no background job)
lane: /home/vgpnk/Projects/shokunin/mori-shokunin (read-only for this seat)
entering tip examined: `6ebd518f` (round-27 verifier spot-check); lane HEAD at read time `079a47c`
scratch: /fast/scratch/hyaku/mori-r28/SupersedeS128/ (one `git clone --no-hardlinks` sandbox at
`/fast/scratch/hyaku/mori-r28/SupersedeS128/clone`; the only commit there is a scratch commit)
lane writes by this seat: this report file only

## 0. Summary

- **S128's row is byte-identical to its first publication.** The oldest commit carrying `| S128 |` is
  `126e192d1fa92675bbaabdcfa7fa1b389f01791c` (round-27, "SOURCES S127-S132"). The whole 11-cell row at
  `126e192d:corpus/SOURCES.md:134` and at `6ebd518f:corpus/SOURCES.md:134` is one identical 2,343-byte line
  (sha256 `3ff8a8eee7947e09e20f13a493f3793f2318a6cf5c3e1d89ac3971c2d0fe9a7b` for both). **No cell differs.**
  Unlike S096/S097/S101, S128 needs no restore: QUALITY 81's check at the tip already lists only
  `changed S096 cells=teaches`, `changed S097 cells=anchor,teaches`, `changed S101 cells=teaches`,
  `rows=144 changed=3 removed=0 bad=0` — S128 is not on that list. What S128 needs is a superseding row,
  because its `teaches` cell states a false contract.
- **The defect is real and re-verified against the bytes.** S128's `teaches` says the pages' inheritance and
  privilege sentences "belong to the legacy oom_adj file, **not to oom_score_adj**". The pages do place those
  sentences only inside the `oom_adj` paragraph (adj page `:134` heading, `:145-149` the sentences), so the
  *placement* half holds; the *contract* half is false. The kernel gives `oom_score_adj` its own privilege floor
  (`fs/proc/base.c:1131-1133`, `-EACCES` without `CAP_SYS_RESOURCE`), sets that floor only from a privileged
  writer (`:1156-1157`, `:1175-1176`), and copies `oom_score_adj` **and its floor** at fork
  (`kernel/fork.c:1768-1769` in `copy_signal`, `:1963-1964` in `copy_oom_score_adj`, called at `:2558`). The
  pages' silence is a documentation gap, not an absent kernel rule.
- **Ready-to-paste: one new row, S149** (section 4). It supersedes S128, keeps the old teaching's true parts,
  and corrects the false one. It is the row the contract's fixed id map requires (`MAP="… S149:S128 …"` in
  `.ufo/waves/round-28/count-c1.sh`).
- **One conflict for the L1, with measured outcomes (section 7).** The amended C1 counter (contract amendment A1)
  rejects a `used-by` path that does not itself cite the **new** id, so the task's literal instruction
  ("used-by = the files that cite S128 today") and the counter cannot both be satisfied as written. I measured
  four variants; section 7 gives the numbers and the recommendation. Also, a corrected `scope` (needed for the
  F3 comparator correction) adds one `W04` census warning; a verbatim scope does not. Both are measured.

## 1. First-published cells versus the tip

The oldest lane commit of `corpus/SOURCES.md` carrying `| S128 |`:

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --reverse --format='%H %ad %s' --date=iso -S'| S128 |' -- corpus/SOURCES.md
126e192d1fa92675bbaabdcfa7fa1b389f01791c 2026-10-22 12:50:10 -0300 round-27: C1 entry oom-victim-selection-r27, SOURCES S127-S132 and used-by anchors, SKILL Round27 table, capture evidence, wave-1 reports so far; round-26 late wave-2 reports (routed D1, uid redacted)
```

The row sits at line **134** at `126e192d` and at line **134** at `6ebd518f`. Cell split (11 cells + the two
separator pipes) at both revisions:

| # | cell | `126e192d` (first published) | `6ebd518f` (tip) | differs |
|---|---|---|---|---|
| 1 | id | S128 | S128 | no |
| 2 | source | `/proc/pid/oom_score_adj(5) and /proc/pid/oom_score(5) manual pages (the v7.2 code they describe is S127) — https://man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html ; https://man7.org/linux/man-pages/man5/proc_pid_oom_score.5.html` | same | no |
| 3 | kind | docs | docs | no |
| 4 | tier | A | A | no |
| 5 | scope | "the documented contract of the two proc files as served from man-pages 6.19, compared with the v7.2 kernel code that enforces it (that code is row S127): the -1000..+1000 range, the -1000 reading, the added-versus-scaled adjustment wording, the 3% root clause, the oom_adj legacy scaling, the owner-only write mode, and the fact that inheritance and the CAP_SYS_RESOURCE rule are documented only inside the oom_adj paragraph; not kill-time victim ordering, not OOM_SCORE_ADJ_MIN exclusion, not this host's oom_score_adj values, not earlyoom's own selection logic" | same | no |
| 6 | anchor | adj page `:72`, `:86-88`, `:102-103`, `:104-110`, `:122-127`, `:145-149`, `:175`; score page `:72-80`, `:97-98`, `:120`; compared with S127 base.c `:583-601`, `:586`, `:596-597`, `:591-594`, `:1089-1101`, `:1213-1231`, `:1131-1133`, `:1156-1157`, `:1175-1176`, `:1242-1256`, `:1275-1279`, `:3351-3353`; HTTP 200 on 2026-10-22T15:46:37Z–15:46:38Z, 11,680 B sha256 `769edf3b…`, 7,955 B sha256 `6169628d…`, base.c 98,196 B sha256 `cef1a2cf…`; Linux tag v7.2; man-pages 6.20 sources carry the same four statement blocks (adj 6.20:25-26,46-47,53,101-105) | same | no |
| 7 | **teaches** | "The two files are different contracts: oom_score_adj is the writable -1000..+1000 preference whose value the kernel scales by totalpages/1000, oom_score is a read-only [0, 2000] export folding that preference in, and the page's inheritance and privilege sentences belong to the legacy oom_adj file, **not to oom_score_adj**." | same | no |
| 8 | status | mined | mined | no |
| 9 | opened | 2026-10-22 | 2026-10-22 | no |
| 10 | recheck | on-release | on-release | no |
| 11 | used-by | corpus/knowledge/oom-victim-selection-r27.md | same | no |

**No cell differs.** Proof, not inference: the whole line was extracted at both revisions and compared byte for
byte — `cmp` reports no difference and both files hash to
`3ff8a8eee7947e09e20f13a493f3793f2318a6cf5c3e1d89ac3971c2d0fe9a7b` (2,343 bytes each; scratch
`first.txt` / `tip.txt`). `git log -S'| S128 |' -- corpus/SOURCES.md` returns **one** commit, so the id was
added once and never edited.

Consequence for the round: **S128 needs no restore.** The QUALITY 81 check at the tip does not list it:

```
python3 -I -B .ufo/waves/round-27/check-row-identity.py 6ebd518f
changed S096 cells=teaches
changed S097 cells=anchor,teaches
changed S101 cells=teaches
rows=144 changed=3 removed=0 bad=0      (exit 1; the three named rows belong to other seats)
```

S128's own row therefore needs exactly one thing: a superseding row that carries the corrected teaching.

Where the defect came from: `.ufo/waves/round-27/w1/SrcManProcOomScoreAdj.md` (the wave-1 seat that opened the
pages) drafted the row with the same false clause — its ready-to-paste line at `:115` carries "and the page's
inheritance and privilege sentences belong to the legacy oom_adj file, not to oom_score_adj" — while the same
report's own analysis at `:70-72` says the inheritance is true in v7.2 but unstated on the page: "This is a gap,
not a contradiction." The drafted row turned the gap into a contradiction.

## 2. The source re-opened today (ordinary curl; no bot challenge)

| URL | accessed (UTC) | HTTP / bytes | sha256 of the bytes fetched | matches the row? |
|---|---|---|---|---|
| https://man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html | 2026-10-22T17:59:01Z | 200 / 11,680 | `769edf3b9c054934db07f16173297fc5fd63c3a4c807682355f08fa45cde80a9` | yes — same as SOURCES:134 |
| https://man7.org/linux/man-pages/man5/proc_pid_oom_score.5.html | 2026-10-22T17:59:02Z | 200 / 7,955 | `6169628d8a2cdc512795cfda74f3598d5b7a25e5b71921d4088c0539cf71b2bc` | yes — same as SOURCES:134 |
| https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c | 2026-10-22T17:59:10Z | 200 / 98,196 | `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6` | yes — same as SOURCES:134 |
| https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/fork.c | 2026-10-22T17:59:11Z | 200 / 85,725 | `359882ea981b58f5289293e5644f7c0085a8350e4f1937f39dcb94ae1cd0dd1d` | yes — same as S127's anchor |
| https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c | 2026-10-22T17:59:54Z | 200 / 34,311 | `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` | yes — same as S003's anchor |
| https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_oom_score_adj.5?id=man-pages-6.20 | 2026-10-22T18:01:39Z | 200 / 4,212 | `16a0d4b50deca2828d840350262d936f70934272a276b96c750af050f31161f3` | yes — same as `.ufo/waves/round-27/w1/SrcManProcOomScoreAdj.md:95` |
| … the same path for `proc_pid_oom_score.5?id=man-pages-6.20` | 2026-10-22T18:01:39Z | 200 / 1,899 | `95c707bd3b4f2d8615085ac5a1bdacbeb5d975cfb94371dcfd4bf33e239f50ea` | yes — same as `SrcManProcOomScoreAdj.md:96` |
| https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/kernel/fork.c?h=v7.2 | 2026-10-22T18:02:32Z | 200 / 85,725 | `359882ea981b58f5289293e5644f7c0085a8350e4f1937f39dcb94ae1cd0dd1d` | **byte-identical** to the raw.githubusercontent fork.c (`cmp` ok) — the two hosts serve the same file |

Every anchor line number in the old row resolves on these bytes. Located quotes (verbatim, at most 25 words, with
line numbers in the fetched bytes):

- adj page `:145-146` (16 words): "The default value for this file is 0; a new process inherits its parent's oom_adj setting."
- adj page `:147` (11 words): "privileged (CAP_SYS_RESOURCE) to update this file, although"
- adj page `:104-105` (9 words): "Acceptable values range from -1000 (OOM_SCORE_ADJ_MIN) to +1000 (OOM_SCORE_ADJ_MAX)."
- adj page `:102-103` (20 words): "The value of oom_score_adj is added to the badness score before it is used to determine which task to kill."
- adj page `:86-88` (14 words): "There is an additional factor included in the badness score: root processes are given 3% extra memory over other tasks."
- adj page `:77-78` (20 words): "The badness heuristic assigns a value to each candidate task ranging from 0 (never kill) to 1000 (always kill)"
- score page `:97-98` (21 words): "The oom_score also reflects the adjustment specified by the oom_score_adj or oom_adj setting for the process."
- `fs/proc/base.c:1131-1133`: `if ((short)oom_adj < task->signal->oom_score_adj_min &&` / `!capable(CAP_SYS_RESOURCE)) {` / `err = -EACCES;`
- `kernel/fork.c:1768-1769`: `sig->oom_score_adj = current->signal->oom_score_adj;` / `sig->oom_score_adj_min = current->signal->oom_score_adj_min;`
- `mm/oom_kill.c:233-234`: `adj *= totalpages / 1000;` / `points += adj;`

## 3. Claim-by-claim verdicts against those bytes

| # | statement | bytes | verdict |
|---|---|---|---|
| 1 | scope: the pages document inheritance and the CAP_SYS_RESOURCE rule only inside the oom_adj paragraph | adj page `:134` is the `oom_adj` heading under HISTORY; the two sentences sit at `:146-147`; `grep -n -i 'inherit\|CAP_\|privileg'` on the adj page returns **only** `:146` and `:147`; on the score page only `:80`, which is the oom_score factor "whether the process is privileged (-)", not a write rule | holds |
| 2 | **old teaches: "the page's inheritance and privilege sentences belong to the legacy oom_adj file, not to oom_score_adj"** | base.c `:1131-1133` refuses an unprivileged write below `oom_score_adj_min` with `-EACCES`; `:1156-1157` and `:1175-1176` set the floor only for a `CAP_SYS_RESOURCE` writer; fork.c `:1768-1769` and `:1963-1964` copy the value **and the floor** at fork; fork.c `:1949-1966` is `copy_oom_score_adj`, called at `:2558` | **fails as a contract claim** (holds only as a placement claim about the pages) |
| 3 | teaches: oom_score_adj is the writable -1000..+1000 preference | adj `:104-105` (range), `:126-127` (writes reach both files); base.c `:3353` `REG("oom_score_adj", S_IRUGO\|S_IWUSR, …)` — owner-writable; base.c `:1275-1279` rejects out-of-range with `-EINVAL` | holds |
| 4 | teaches: the kernel scales that value by totalpages/1000 | oom_kill.c `:233` `adj *= totalpages / 1000;`, `:234` `points += adj;` | holds, but the old row had **no anchor** for it (the old anchor names base.c only; S003's own anchor cell does not register `mm/oom_kill.c:199-237`) — the anchor gap the wave-2 report called F2 |
| 5 | teaches: oom_score is a read-only [0, 2000] export | base.c `:3351` `ONE("oom_score", S_IRUGO, proc_oom_score)` — no write mode; `:591-595` the `[0, 2000]` comment; `:596-597` `points = (1000 + badness * 1000 / (long)totalpages) * 2 / 3;` | holds |
| 6 | scope/anchor: the 3% root clause has no v7.2 implementation | oom_kill.c is 1,257 lines; `grep -c -i 'root\|3%\|CAP_SYS_ADMIN'` → **0**; `grep -c 'capab'` → **0**; `grep -c 'capable'` → **0**; `oom_badness` is `:199-237` | holds, scoped to v7.2 `oom_badness` |
| 7 | scope: the oom_adj legacy scaling | adj `:122-124` "Its value is scaled linearly with oom_score_adj"; base.c `:1089-1101` (read) and `:1213-1231` (write) | holds |
| 8 | scope: the owner-only write mode | base.c `:3353` `S_IRUGO\|S_IWUSR`; `:3351` oom_score is `S_IRUGO` | holds (the pages are silent on modes; the row compares code to pages) |
| 9 | anchor: the 6.20 sources carry the same four statement blocks | 6.20 adj `:25-26` (3% clause), `:46-47` (range), `:53` (badness 0), `:101-105` (inherits / privileged / CAP_SYS_RESOURCE); 6.20 score `:28` "whether the process is privileged (\-)." | holds — and the old row named no URL or digest for it (wave-2 F4) |
| 10 | anchor: the page's own 0-to-1000 badness statement (old row omitted it) | adj `:77-78` | holds; the old anchor omitted it (wave-2 F5) |
| 11 | source: "(the v7.2 code they describe is S127)" | the pages describe the interface across releases ("since Linux 2.6.11", "since Linux 2.6.36") and never mention v7.2 — "describe" overstates | overstatement (wave-2 F6); S149 says "the v7.2 code that enforces them" |
| 12 | scope: the comparator for the 3% absence is S127 (old row) | S127's own scope excludes "the oom_badness body (mm/oom_kill.c, S003)"; the absence lives in `oom_badness` | **wrong comparator** (wave-2 F3); S149 names both S127 and S003 |

Not verified today (gaps, stated, not passes): the old row's fetch timestamps (2026-10-22T15:46:37Z–15:46:38Z)
cannot be re-observed; the man-pages tarball members were not re-extracted; the S127 uapi `oom.h` and the other S127
anchors were not re-read beyond what is quoted above.

## 4. Ready-to-paste row S149

Insert after the S144 row (`corpus/SOURCES.md:150` at the tip, the last row of the `## Registry` table, before
the blank line and `## Paths`). The block below is the complete row: one line, 11 cells, 3,962 bytes plus newline,
byte-identical to `/fast/scratch/hyaku/mori-r28/SupersedeS128/row-S149.txt` (sha256
`11f2a80cbe242302810b9a5026f55d5938485829b0a9969641fc7b8ea81e19b5`), which is the file that was tested in the
sandbox (section 6).

```
| S149 | /proc/pid/oom_score_adj(5) and /proc/pid/oom_score(5) manual pages (the v7.2 code that enforces them is S127; the oom_badness scaling and the absent 3% root term are S003) — https://man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html ; https://man7.org/linux/man-pages/man5/proc_pid_oom_score.5.html | docs | A | the documented contract of the two proc files as served from man-pages 6.19, compared with the v7.2 kernel code that enforces it (the /proc read and write path is fs/proc/base.c, row S127; the kill-time score and its totalpages scaling are in mm/oom_kill.c, row S003): the -1000..+1000 range, the -1000 reading, the added-versus-scaled adjustment wording, the 3% root clause, the oom_adj legacy scaling, the owner-only write mode, and the fact that the pages state inheritance and the CAP_SYS_RESOURCE rule only inside the oom_adj paragraph; not kill-time victim ordering, not OOM_SCORE_ADJ_MIN exclusion, not this host's oom_score_adj values, not earlyoom's own selection logic | adj page:72 (since 2.6.36), :77-78 (badness 0 to 1000), :86-88 (3% root), :102-103 (adjustment "added"), :104-110 (range and -1000), :122-127 (oom_adj scaling), :145-149 (oom_adj inheritance and privilege), :175 (footer "Linux man-pages 6.19 2026-02-08"); score page:72-80 (since 2.6.11, factors), :97-98 (reflects the adjustment), :120 (footer); compared with S127 base.c:583-602 (proc_oom_score, totalpages :586, formula :596-597, [0, 2000] comment :591-595), :1089-1101 and :1213-1231 (oom_adj scaling), :1131-1133 (CAP_SYS_RESOURCE floor gate, -EACCES), :1156-1157 (:1175-1176 shared-mm copy of oom_score_adj_min), :1242-1256 (oom_score_adj read), :1275-1279 (range check, -EINVAL), :3351-3353 (S_IRUGO / S_IRUGO plus S_IWUSR), and kernel/fork.c:1721-1775 (copy_signal), :1768-1769, :1949-1966 (copy_oom_score_adj), called at :2558; and with S003 mm/oom_kill.c:199-237 (oom_badness; OOM_SCORE_ADJ_MIN exclusion :216-222, adj scaling :232-234 `adj *= totalpages / 1000; points += adj;`, no capability term in the function); man-pages 6.20 carries the same four statement blocks (adj 6.20:25-26,46-47,53,101-105; score 6.20:28) at https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_oom_score_adj.5?id=man-pages-6.20 (4,212 B, sha256 16a0d4b50deca2828d840350262d936f70934272a276b96c750af050f31161f3) and the same path for proc_pid_oom_score.5?id=man-pages-6.20 (1,899 B, sha256 95c707bd3b4f2d8615085ac5a1bdacbeb5d975cfb94371dcfd4bf33e239f50ea); HTTP 200 on 2026-10-22T17:59:01Z-2026-10-22T18:02:32Z, adj 11,680 B sha256 769edf3b9c054934db07f16173297fc5fd63c3a4c807682355f08fa45cde80a9, score 7,955 B sha256 6169628d8a2cdc512795cfda74f3598d5b7a25e5b71921d4088c0539cf71b2bc, base.c 98,196 B sha256 cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6, fork.c 85,725 B sha256 359882ea981b58f5289293e5644f7c0085a8350e4f1937f39dcb94ae1cd0dd1d, oom_kill.c 34,311 B sha256 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e; Linux tag v7.2 | supersedes S128 — the old row said the pages' inheritance and privilege sentences belong to the legacy oom_adj file and not to oom_score_adj; the pages do place them only inside the oom_adj paragraph (adj:145-149), but that placement is a documentation gap, not an absent kernel rule, because the kernel still copies oom_score_adj and its floor at fork (kernel/fork.c:1768-1769,1949-1966) and refuses an unprivileged write below oom_score_adj_min (fs/proc/base.c:1131-1133). The two files are different contracts: oom_score_adj is the writable -1000..+1000 preference whose value the kernel scales by totalpages/1000 (mm/oom_kill.c:232-234), oom_score is a read-only [0, 2000] export folding that preference in (fs/proc/base.c:596-597), and the pages' 3% root clause (adj:86-88) has no implementation in v7.2 oom_badness (mm/oom_kill.c:199-237). | mined | 2026-10-22 | on-release | corpus/knowledge/oom-victim-selection-r27.md, corpus/lessons/round-28.md |
```

Cell check (all machine-checked, section 6): 11 cells, no `|` inside any cell; `teaches` opens exactly
`supersedes S128 — ` (em dash U+2014, then a space); `status` `mined`; `opened` `2026-10-22`; `recheck`
`on-release` (S128's own convention); `used-by` as listed in section 5.

**What changed against S128, cell by cell** (the old → new log the round lesson needs):

| cell | old | new |
|---|---|---|
| source | "…(the v7.2 code they describe is S127)…" | "…(the v7.2 code that enforces them is S127; the oom_badness scaling and the absent 3% root term are S003)…" — the pages describe the interface across releases, not v7.2 (F6) |
| scope | "…(that code is row S127): … the fact that inheritance and the CAP_SYS_RESOURCE rule are documented only inside the oom_adj paragraph…" | "…(the /proc read and write path is fs/proc/base.c, row S127; the kill-time score and its totalpages scaling are in mm/oom_kill.c, row S003): … the fact that the pages **state** inheritance and the CAP_SYS_RESOURCE rule only inside the oom_adj paragraph…" — the comparator for the 3% absence and the scaling is S003, not S127 (F3); "state" makes the placement claim about the pages, not a rule |
| anchor | adj `:72`, `:86-88`, `:102-103`, `:104-110`, `:122-127`, `:145-149`, `:175`; score `:72-80`, `:97-98`, `:120`; base.c `:583-601`, `:586`, `:596-597`, `:591-594`, `:1089-1101`, `:1213-1231`, `:1131-1133`, `:1156-1157`, `:1175-1176`, `:1242-1256`, `:1275-1279`, `:3351-3353`; HTTP 200 on 2026-10-22T15:46:37Z–15:46:38Z with three digests; Linux tag v7.2; "man-pages 6.20 sources carry the same four statement blocks" with no URL or digest | adds adj `:77-78` (the page's own 0-to-1000 badness range, F5); base.c `:583-602` and `:591-595`; kernel/fork.c `:1721-1775`, `:1768-1769`, `:1949-1966`, `:2558`; S003 mm/oom_kill.c `:199-237`, `:216-222`, `:232-234` (the scaling claim was unanchored, F2); the 6.20 statement blocks now carry both URLs and both digests (F4); access times and digests are today's |
| teaches | "…and the page's inheritance and privilege sentences belong to the legacy oom_adj file, not to oom_score_adj." | "supersedes S128 — the old row said …; the pages do place them only inside the oom_adj paragraph (adj:145-149), but that placement is a documentation gap, not an absent kernel rule, because the kernel still copies oom_score_adj and its floor at fork (kernel/fork.c:1768-1769,1949-1966) and refuses an unprivileged write below oom_score_adj_min (fs/proc/base.c:1131-1133). …" — the false contract is named and replaced; the two true contracts (writable preference, read-only export) and the 3% absence are kept, now anchored |
| used-by | corpus/knowledge/oom-victim-selection-r27.md | corpus/knowledge/oom-victim-selection-r27.md, corpus/lessons/round-28.md — see the conflict in section 7 |

`status`, `opened` and `recheck` are unchanged (all three are mutable in place, and S128's values are the right ones).

## 5. `used-by` for S149

Files that cite S128 today (`git -C <lane> grep -n 'S128' 6ebd518f -- corpus SKILL.md PROVINCE.md`):

- `corpus/SOURCES.md:134` — the registry itself; the registry is not a used-by path (S143/S144 precedent).
- `corpus/knowledge/oom-victim-selection-r27.md:1` (source header) and `:66` (the "documentation and the code
  disagree in one place" bullet) — a live reader, in the counter's `READERS` list.
- `corpus/lessons/round-27-verifier-spotcheck.md:132`, `:150` and `corpus/lessons/round-27.md:70`, `:126`, `:127`
  — history files. `corpus/lessons/round-27.md:70` is the round-27 Gate line for S128; `:126-127` are the
  round-27 lesson's "carried as named debt" lines that name S128 teaches F1.
- `SKILL.md` and `PROVINCE.md`: **no** S128 hit (`git grep -n 'S128' 6ebd518f -- SKILL.md PROVINCE.md` → nothing).

So the files that cite S128 today are the knowledge entry and the two round-27 lessons. **The round-28 counter
(amendment A1) will not accept that list as the row's `used-by`** — it requires every `used-by` path to cite the
**new** id S149 at the landed revision, and the two round-27 lesson files are frozen history that will keep saying
S128. S149 therefore carries `corpus/knowledge/oom-victim-selection-r27.md, corpus/lessons/round-28.md`: the
knowledge entry becomes an S149 reader when the L1 moves the reader (section 7), and the round-28 lesson carries
the S149 Gate line, so both cite S149. Measured outcomes in section 7.

## 6. Gate line

The counter's `gate_line` test (`count-c1.sh`, python block) requires a line in the round-28 lesson's `## Gate`
section that matches `\|\s*S149\s*\|` **and** contains an `https://` URL, a 64-hex sha256, and a quoted span.
This line satisfies all four (checked against the counter's own regexes):

| Row | URL | Accessed | Located quote | Decision |
|---|---|---|---|---|
| S149 | https://man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html ; https://man7.org/linux/man-pages/man5/proc_pid_oom_score.5.html (sha256 769edf3b9c054934db07f16173297fc5fd63c3a4c807682355f08fa45cde80a9 ; 6169628d8a2cdc512795cfda74f3598d5b7a25e5b71921d4088c0539cf71b2bc) | 2026-10-22T17:59:01Z | adj page `:145-146` "The default value for this file is 0; a new process inherits its parent's oom_adj setting." (16 words) | admit, A, mined (SupersedeS128) |

The quote is verbatim from the bytes fetched at 2026-10-22T17:59:01Z, 16 words (limit 25), located at adj page
`:145-146`.

## 7. Conflict for the L1 — the amended counter and the `used-by` list (measured)

Contract amendment A1 (`.ufo/waves/round-28/count-c1.sh`, `MAP="S145:S096 S146:S097 S147:S101 S148:S127
S149:S128 S150:S129 S151:S131 S152:S140"`) adds, per new row: the `supersedes S0NN — ` prefix, a **changed**
`teaches`, a non-empty `used-by` for a `mined` row, a Gate line, and — the part that bites here —
`bad = [p for p in paths if not exists_with_id(p, new)]`, i.e. **every `used-by` path must itself cite S149** at
the landed revision (`git grep -q -w -F S149 <rev> -- <path>`).

The task instruction ("used-by = the files that cite S128 today") and that check cannot both hold: the two
round-27 lesson files cite S128 today, are frozen history, and will never cite S149. I measured all four
combinations in the sandbox (clone at `763d346`, S149 inserted after S144, the knowledge entry's S128 → S149
reader move applied, the round-28 lesson with the Gate line of section 6 added):

| variant | scope | `used-by` | amended counter on S149 | census |
|---|---|---|---|---|
| **A (recommended)** | corrected | knowledge entry + `corpus/lessons/round-28.md` | **passes every per-row check**; `superseding=1/8 ids=S128` | exit 0, E=0, **7** W04 (one new for S149) |
| B | corrected | the three S128-citing files (task-literal) | **fails**: `fail S149 used_by_not_citing=corpus/lessons/round-27.md,corpus/lessons/round-27-verifier-spotcheck.md` → `superseding=0/8` | exit 0, E=0, 7 W04 |
| C | S128's scope verbatim | knowledge entry + `corpus/lessons/round-28.md` | passes; `superseding=1/8 ids=S128` | exit 0, E=0, **6** W04 (no new) |
| D | S128's scope verbatim | the three S128-citing files | fails the same way as B | exit 0, E=0, 6 W04 |

Recommendation and the two decisions behind it:

1. **`used-by` = `corpus/knowledge/oom-victim-selection-r27.md, corpus/lessons/round-28.md` (variant A).** This is
   the only list that satisfies the counter. It is also the lane's own convention for a *new* row: `used-by` is
   "repo-relative paths of the knowledge entries or lessons **citing the row**" (`CORPUS.md:107`), and after the
   reader move those are exactly the two files. The round-27 lessons stay in S128's own `used-by` cell, which is
   where they belong as its history. The alternative — adding the round-27 lessons to S149's `used-by` — fails
   the counter (variant B), so it is not available.
2. **Scope: corrected (variant A) rather than verbatim (variant C).** The corrected scope is what fixes F3 (the
   3% absence and the totalpages scaling live in `mm/oom_kill.c`, row S003; S127's own scope excludes "the
   oom_badness body"). The price is **one new `W04` census warning**: `file W04 S149 duplicate url
   man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html across scopes`. The census still exits **0** with
   `ok` and no `E`-code; `W04` is a warning the census script documents as "same URL across scopes (warnings do
   not affect clean lanes)" (`scripts/sources-census.sh:33`). The lane's six pre-existing W04s are S035, S037,
   S073, S074, S075, S076 — all unrelated rows. If the L1 prefers a clean W04 set over the F3 correction, variant
   C is the drop-in alternative: the same row with S128's `scope` cell byte for byte. **This is the L1's call; this
   seat did not write in the lane.**
3. **The reader move is owed to the L1, not to this seat.** The counter's `readers_left` term counts live-reader
   lines still citing any of the eight superseded ids. At `6ebd518f` there are **27** such lines across
   `SKILL.md`, `PROVINCE.md`, `corpus/README.md` and `corpus/knowledge`; **two** of them cite S128, both in
   `corpus/knowledge/oom-victim-selection-r27.md` (`:1` source header, `:66`). The other 25 belong to other seats'
   rows. To reach `readers_left=0` the L1 must, in the knowledge entry, replace the S128 citations with S149 (the
   sandbox did exactly this and the S149 per-row checks then passed) and, for the other seats' rows, move their
   readers too. This seat's row alone cannot clear `readers_left`.
4. **The lesson must exist before the row passes.** `count-c1.sh` reads `corpus/lessons/round-28.md` from the
   landed revision; the file does not exist at `6ebd518f` or `079a47c` (it exists only in the working tree). The
   Gate line of section 6 and the row's `used-by` both depend on it. In the sandbox the lesson was created with
   that Gate line, and the S149 checks passed.

## 8. QUALITY 77 sweep — every place in the lane whose prose states the defective wording

`corpus/QUALITY.md:349` (criterion 77): a correction sweeps every mention in place; the superseded wording is
removed, not shadowed. The defective wording is the `teaches` clause
**"the page's inheritance and privilege sentences belong to the legacy oom_adj file, not to oom_score_adj"**, and
the scope clause that reads the same claim ("inheritance and the CAP_SYS_RESOURCE rule are documented only inside
the oom_adj paragraph" as a rule statement rather than a placement statement). At `6ebd518f`, a whitespace-folded,
emphasis-stripped sweep over every tracked file (script in scratch, `sweep.py`) plus a literal
`git grep` finds exactly these places:

| path:line | what it says | kind |
|---|---|---|
| `corpus/SOURCES.md:134` | the S128 row's own `teaches` cell — "…belong to the legacy oom_adj file, not to oom_score_adj." | **the live defect**; corrected by S149 (§4) and left in place because QUALITY 81 freezes the row's first-published cells |
| `corpus/SOURCES.md:134` | the same row's `scope` cell — "…the fact that inheritance and the CAP_SYS_RESOURCE rule are documented only inside the oom_adj paragraph…" | the scope half of the claim; **frozen by QUALITY 81** (the row is byte-identical to its first publication), corrected in S149's scope (§4) |
| `.ufo/waves/round-27/w1/SrcManProcOomScoreAdj.md:115` | the wave-1 seat's ready-to-paste row line, carrying the same defective `teaches` clause | **live false claim in a seat report** |
| `.ufo/waves/round-27/w1/SrcManProcOomScoreAdj.md:10` | the same report's verdict line: "state inheritance and the `CAP_SYS_RESOURCE` write rule only inside the legacy `oom_adj` paragraph, never for `oom_score_adj`" | **live claim of the same defect** (the report's own analysis at `:70-72` contradicts it: "This is a gap, not a contradiction") |
| `.ufo/waves/round-27/w2/ReopenS128.md:11`, `:96`, `:107`, `:108`, `:114`, `:130`, `:131` | quotes the claim in order to name it F1 and gives the corrected text | falsification record — keep as it is |
| `corpus/lessons/round-27.md:70` | the round-27 Gate line for S128 | round-27 Gate history — keep as it is |
| `corpus/lessons/round-27.md:126`, `:127` | "S128 teaches F1 (ReopenS128)" under "Carried as named debt" | lesson history — keep as it is |
| `corpus/lessons/round-27-verifier-spotcheck.md:132`, `:150` | "row defects in S127, S128, …" and "S127 scope/teaches F1–F5, S128 F1, …" | outside-check history — keep as it is |

Places that already carry the **correct** wording and must stay (these are what S149 agrees with):
`corpus/knowledge/oom-victim-selection-r27.md:84-89` ("`fork` copies both the value and its floor (S127
`kernel/fork.c:1768-1769,1949-1966`)" and "only a writer with `CAP_SYS_RESOURCE` may go below that floor … (S127
`fs/proc/base.c:1131-1133, 1156-1157`)"), and `SKILL.md:742` ("it can lower down to `oom_score_adj_min` … only the
legacy `oom_adj` file ratchets").

**Recommended sweep for the L1 (decide, do not leave implicit):**

(a) Log the old → new cells in the round-28 lesson's "Row changes logged old → new" section, in the S124 form
(`corpus/lessons/round-27.md:92-100`); the table in §4 is the content.
(b) Add a dated correction block to the two live false claims in the round-27 wave-1 report
(`SrcManProcOomScoreAdj.md:10` and `:115`), or name them and their disposition in the round-28 lesson, following
the r26 D4 precedent (`corpus/lessons/round-27.md:109`). Whether those two lines are rewritten or logged as
history is the L1's call.
(c) Leave the wave-2 falsification record and the round-27 lessons and the outside check untouched: they quote
the claim in order to refute it.

Note on the QUALITY 81 / QUALITY 77 tension: S128's row keeps its first-published bytes (nothing to restore —
§1), so the false wording stays in `corpus/SOURCES.md:134` while S149 carries the correction. That is the same
shape as the lane's S124→S133, S090→S143 and S093→S144 precedent (corrected teaching in the new row, old → new
logged in the lesson), and the counter's design expects it: the amended counter accepts a superseding row whose
`teaches` differs from the old one, and the reader move (§7 item 3) is what stops the old id from being read as
current. The lane's own `readers_left` term is the mechanism that forces the readers off the defective wording.

## 9. Checks run (scratch only; the lane was not modified)

Sandbox: `git clone --no-hardlinks` of the lane into `/fast/scratch/hyaku/mori-r28/SupersedeS128/clone`, checked
out at `763d346`. Commits there are scratch commits only (the clone's HEAD moved to a scratch commit carrying
S149, the knowledge-entry reader move and the round-28 lesson with the Gate line).

1. **Row identity** — the lane's own `.ufo/waves/round-27/check-row-identity.py` with `LANE` repointed at the
   clone: before → `changed S096 cells=teaches`, `changed S097 cells=anchor,teaches`, `changed S101 cells=teaches`,
   `rows=144 changed=3 removed=0 bad=0`, exit 1; after S149 → `rows=145 changed=3 removed=0 bad=0`, exit 1 — S149
   is **not** listed as changed (it is a new row, so it has no first-published cells to differ from).
2. **Amended C1 counter** (`.ufo/waves/round-28/count-c1.sh` with `LANE` repointed at the clone and its frozen
   `check.py` replaced by the identically-patched script): with S149 + the knowledge-entry reader move + the
   round-28 lesson Gate line → `row_identity=rows=145 changed=3 removed=0 bad=0`, `superseding=1/8 ids=S128`, **no
   `fail S149` line**, `readers_left=26` (the other 26 lines belong to other seats' rows). Without the row →
   `superseding=0/8 ids=none`, `fail S149 row_absent`.
3. **Control** — the same counter with the `supersedes S128 — ` prefix removed from S149's `teaches` →
   `fail S149 prefix`. With the `used-by` set to the three S128-citing files → `fail S149
   used_by_not_citing=corpus/lessons/round-27.md,corpus/lessons/round-27-verifier-spotcheck.md`. Both controls
   fail as they should.
4. **Census** — `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <clone>/corpus/SOURCES.md`
   → exit **0**, no `E`-code, `ok`. With the corrected scope: 7 `W04` lines (the six pre-existing S035, S037,
   S073–S076 plus one new for S149). With S128's scope verbatim: the same six, no new line.
5. **Counter's Gate-line regex** — the section-6 line matches `\|\s*S149\s*\|`, contains `https://`, contains both
   64-hex digests, and contains a quoted span; the located quote is 16 words (limit 25) and is verbatim from the
   bytes fetched at 2026-10-22T17:59:01Z.
6. **Row bytes** — `row-S149.txt` is 3,962 bytes plus newline, sha256
   `11f2a80cbe242302810b9a5026f55d5938485829b0a9969641fc7b8ea81e19b5`; 11 cells; no `|` inside any cell; the
   `teaches` prefix is `supersedes S128 — ` (em dash).
7. **Read-only in the lane** — `bash .ufo/waves/round-28/count-c1.sh 6ebd518f` → `row_identity=rows=144 changed=3
   removed=0 bad=0`, `superseding=0/8 ids=none`, `C1=unmet`, exit 1 — the before state the contract declares. Only
   `git show`, `git log`, `git grep`, `git rev-parse`, `git ls-tree` and `git status --porcelain` were used there.
8. **Byte equality of the S128 row** — the extracted line at `126e192d` and at `6ebd518f` are identical
   (`cmp` ok, both sha256 `3ff8a8ee…`, 2,343 bytes).

## 10. Out of scope, gaps, limits

- This seat owns S128 only. S096, S097, S101, S127, S129, S131 and S140 are other rows of C1 and are untouched
  here; the `readers_left=26` lines counted in §7 item 3 are mostly theirs.
- The old row's fetch timestamps (2026-10-22T15:46:37Z–15:46:38Z) could not be re-observed; S149 carries today's
  access times and digests instead.
- The man-pages tarball members were not re-extracted; the 6.20 cross-check used the two git blobs, whose digests
  match the wave-1 report's recorded values.
- The S127 uapi `oom.h` and the other S127 anchors were not re-read beyond the lines quoted here.
- The "no 3% term" claim is scoped to v7.2 `oom_badness` (`mm/oom_kill.c:199-237`) and to the whole file (1,257
  lines, zero hits for `root`, `3%`, `CAP_SYS_ADMIN`, `capab`, `capable`); no other kernel file was searched.
- The counter's `readers_left` term cannot reach 0 from this row alone; it needs the other seven seats' rows and
  the L1's reader move.
- The lane working tree already carries uncommitted edits by other seats (`corpus/SOURCES.md`, `SKILL.md`,
  `PROVINCE.md`, `corpus/README.md` modified; `.ufo/waves/round-28/` untracked). These are concurrent sibling-seat
  and L1 edits, not committed bytes, and not this seat's work. At 18:0xZ no `S149` row exists in the lane's
  `corpus/SOURCES.md` (`grep -c '^| S149 '` → 0), so the row of §4 is still to be pasted.

## 11. Tooling and privacy

- No installs and no updates: every tool needed was already present. Versions used: bash 5.3.20, curl 8.23.0,
  git 2.56.0, Python 3.14.8, sha256sum 0.8.0, GNU Awk 5.4.1. The operator's agent rules file
  (`/home/vgpnk/.omp/agent/RULES.md`) was read and its tooling directive followed (nothing needed installing; all
  pacman transactions remain paused host-wide).
- Only read-only git was used in the lane; `git clone --no-hardlinks` and the scratch commits wrote only into
  `/fast/scratch/hyaku/mori-r28/SupersedeS128/`.
- This report carries commit ids, URLs, digests, line numbers, row cells, counts and states only. No uid, pid,
  session id, session-store path, unit name of this host's user session, settings value or command line. The
  operator's harness settings file is referred to by that description only, and no value from it is quoted.
- No lane file was written except this report. No git or jj mutation in the lane, no host write, no service or
  package change, no unit started or stopped, no process signalled.
