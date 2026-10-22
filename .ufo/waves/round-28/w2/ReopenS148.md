# ReopenS148 — re-attack row S148 (supersedes S127) at f2de0eedcd60d2e354da75265ea6122bc3896073

**Verdict: holds.** S148 was re-opened against live bytes now, every cell re-verified, every named defect confirmed
fixed (not copied), every used-by path cites S148, and no live reader retains S127 or the defective wording.
seat: MoriR28.ReopenS148 (leaf; no subagents, no background jobs). L1: MoriR28. No lane file other than this report
was written. Scratch: `/fast/scratch/hyaku/mori-r28-w2/ReopenS148/` (downloads only; no clone needed).

## 1. Re-open of S148's sources (fetch evidence)

All fetches by plain `curl`, bytes hashed with `sha256sum`. Row source cell (`SOURCES.md:153` at the attack rev)
names three URLs; the anchor cell also pins two cross-row files, fetched too.

| URL | Accessed (UTC) | HTTP | Bytes | sha256 | Verdict |
|---|---|---|---|---|---|
| raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c | 2026-10-22T18:53:37Z | 200 | 98,196 | `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6` | equals Gate + anchor hash |
| git.kernel.org/…/plain/include/uapi/linux/oom.h?h=v7.2 | 2026-10-22T18:53:37Z | 200 | 526 | `6b00b4d0648bcdc9d6be7ea8a33b8e6b842c063e7b2b71bdabd757de773896ae` | equals anchor hash |
| git.kernel.org/…/plain/kernel/fork.c?h=v7.2 | 2026-10-22T18:53:37Z | 200 | 85,725 | `359882ea981b58f5289293e5644f7c0085a8350e4f1937f39dcb94ae1cd0dd1d` | equals anchor hash |
| torvalds/linux/v7.2/mm/oom_kill.c (cross-row, S003's file) | 2026-10-22T18:54:23Z | 200 | 34,311 | `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` | equals anchor hash |
| torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst (S092's file) | 2026-10-22T18:54:23Z | 200 | 133,236 | `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad` | equals anchor hash |

Note: GitHub raw returned HTTP 429 (199 B) twice for the two cross-row files at 18:53:37Z and 18:54:06Z; both were
then fetched from `git.kernel.org/…/plain/…?h=v7.2`, HTTP 200, and their sha256s equal the values the anchor cell
declares — the drift is the transport, not the bytes. The 199-byte 429 bodies are not evidence. All three row URLs
returned 200 directly. No drift in any declared hash.

## 2. Gate line (`corpus/lessons/round-28.md:67` at the attack rev)

Line 67: `| S148 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c (with …) | 2026-10-22T17:58:57Z | cef1a2cf…915c6 | `base.c:1147` "if (mm_flags_test(MMF_MULTIPROCESS, p->mm)) {" | admit, A, mined; sha256 cef1a2cf… |`

- https URL present; access time present; 64-hex sha256 equals my own 18:53:37Z fetch of that URL — **holds**.
- Located quote: `base.c:1147` reads exactly `			if (mm_flags_test(MMF_MULTIPROCESS, p->mm)) {` — 8 words, ≤25, verbatim — **holds**.
- Minor observation (not a defect): the decision cell repeats the sha256 already in the sha256 column; redundant,
  satisfies rather than violates the counter's requirements.

## 3. S148 row cells vs bytes (`SOURCES.md:153`, 13 `|`-fields, no `|` inside a cell — NF=13, same as header/S127)

- **source/kind/tier**: three URLs match the fetched bytes above; `code`, `A` — holds.
- **scope** (cell 6): "that -1000 reads 0 (the LONG_MIN return is in S003's mm/oom_kill.c:204-221 …, cited here, not
  restated)" — `oom_kill.c:204-221` holds the LONG_MIN returns; "set only for a CLONE_VM clone" — `fork.c:1956-1961`;
  "cgroup memory.oom.group … in the file row S092 opens, cgroup-v2.rst:1450-1466" — `cgroup-v2.rst:1450` is
  `  memory.oom.group`, block runs to `:1466`; "S002 covers memory events and memory.peak, not it" — S002's row
  (`SOURCES.md:8`) names memory.events/memory.peak/hierarchy only. All hold.
- **anchor** (cell 7): verified line-by-line on fetched bytes — `base.c:583-602` (`proc_oom_score` opens at 583,
  closes at 602), `:586` totalpages=RAM+swap, `:590` oom_badness call, `:592-597` LONG_MIN skip + formula +
  comment's "[0, 2000]", `:1106` `__set_oom_adj`, `:1118-1122` legacy/current EACCES, `:1131-1135` adj_min floor,
  `:1143-1150` mm grab gated on `!task->vfork_done` and `MMF_MULTIPROCESS` (the flag test is `:1147`), `:1155-1158`
  assignment/min/tracepoint, `:1164-1177` propagation loop skipping same thread group, PF_KTHREAD, global init,
  vfork/different-mm tasks, `:1242-1256` `oom_score_adj_read` (value at `:1252`), `:1275-1279` -EINVAL range check,
  `:3351-3353`/`:3706-3708` modes S_IRUGO for oom_score and S_IRUGO|S_IWUSR for oom_score_adj (also `oom_adj`, but
  the cell's claim is about the two named files — holds); `oom.h:9-10` `-1000`/`1000`; `fork.c:1728` zalloc,
  `:1768-1769` both copies inside `copy_signal` (opens `fork.c:1721`), `:1949-1966` `copy_oom_score_adj` with the
  `(CLONE_VM|CLONE_THREAD|CLONE_VFORK) != CLONE_VM` return at `:1956` and `mm_flags_set` at `:1961`; cross-row
  `oom_kill.c:204-221` + `:233-234` inside `oom_badness` (opens `:199`, closes `:237`), `cgroup-v2.rst:1450-1466`.
  Embedded sha256s all equal my fetches; byte counts 98,196 / 526 / 85,725 match. Holds.
- **teaches** (cell 8): opens `supersedes S127 — ` with real em dash (bytes `e2 80 94`, xxd-confirmed) then corrected
  teaching; differs from S127's teaches — holds (the counter's teaches-changed rule).
- **status `mined`, opened `2026-10-22`, recheck `on-release`** — S127 is `mined`, so `mined` is the required
  status — holds.
- **used-by** (cell 12): five paths; all cite S148 as a word — §5.

## 4. Named defects (SupersedeS127 report F1–F4; F5 routed to S149) — fixed, not copied

S127's defective text re-verified verbatim at the attack rev (`SOURCES.md:133`): scope says "the two facts they
depend on … why -1000 reads 0 … not cgroup memory.oom.group (S002)"; teaches says "0 when the task is unkillable or
oom_score_adj is -1000 … with the write copied to every non-thread process sharing the mm."

- **F1** (memory.oom.group pointed at S002): S148 scope says it is in S092's cgroup-v2.rst:1450-1466 and that S002
  covers events/peak — confirmed against `cgroup-v2.rst:1450-1466` and `SOURCES.md:8`. **Fixed.**
- **F2** ("every non-thread process sharing the mm" over-broad): S148 now states the mm is grabbed only when the
  writer is not in vfork and the mm carries MMF_MULTIPROCESS (`base.c:1143-1150`), the loop skips own thread group /
  kernel threads / global init / vfork holders (`:1164-1177`), and the flag is set only for a CLONE_VM-only clone
  (`fork.c:1956-1961`). All verified on bytes. **Fixed.**
- **F3** (two reasons for a 0 reading): S148 states five cases — init or kernel thread, no mm, adj -1000,
  MMF_OOM_SKIP, in vfork — matching `oom_kill.c:204-221` (`oom_unkillable_task` covering the first pair at `:160-167`)
  plus `base.c:592-597` (0 whenever badness is LONG_MIN). **Fixed.**
- **F4** ("-1000 reads 0" reason placed in this row's scope): S148 cites S003's file explicitly ("cited here, not
  restated"). **Fixed.**
- **F5** (S128's mis-pointed totalpages/1000 clause): S148 carries the attribution S149 needs ("scaled by
  totalpages/1000 inside oom_badness (S003's mm/oom_kill.c:233-234), not in this row's files") — verified
  `oom_kill.c:233-234` is inside `oom_badness` (`:199-237`). Not this row's defect; no defect found in S148's part.

## 5. Used-by citations and QUALITY 77 sweep (at the attack rev)

- used-by paths cite S148 as a word: `corpus/knowledge/oom-victim-selection-r27.md` (lines 1, 37, 55, 63, 72, 84,
  89), `SKILL.md:722`, `PROVINCE.md:377`, `corpus/README.md:36` ("S148, S149, S150, S130, S151, S132, S142"), and
  `corpus/lessons/round-28.md:67`. All five — **hold**.
- `grep -w 'S127'` over SKILL.md PROVINCE.md corpus/README.md corpus/knowledge/*: exactly one hit,
  `oom-victim-selection-r27.md:203`, which names the **tsukuroi** registry's S127 (different lane, different row) —
  correctly excluded by the counter's `grep -v tsukuroi`; moving it would be a factual error.
- Defective-wording sweep (`every non-thread process`, `unkillable or oom_score_adj`, `why -1000 reads 0`,
  S002↔memory.oom.group, `two reasons`): zero hits in live readers. The entry's own restatements are correct:
  `:63` "0 for an excluded task (S148 `fs/proc/base.c:583-599`)" (inside the verified span) and `:60-61`
  victim-selection exclusions match `oom_kill.c:160-167,216-222`.
- Canonical counter, `count-c1.sh f2de0eed`: `readers_left=0`, `superseding=7/8` including S127, and **no
  `fail S148` line** — S148 passes every per-row gate. `C1=unmet` at this rev solely from `fail S147 row_absent`
  (a sibling seat's row, outside this seat's scope); my report records, not adjudicates, that gap.

## 6. Tool record

Read `/home/vgpnk/.omp/agent/RULES.md`. **No tool installed or upgraded** (pacman paused host-wide; git 2.56.0,
curl 8.23.0, sha256sum, awk, grep already present sufficed). Lane accessed read-only (`git show`, `ls-tree`); no
mutation of lane, fleet root, jj state, or index. No unit touched, no process signalled, no settings values copied.

## 7. Residual risk

- `base.c` tag v7.2 is a release tag; bytes were identical across my fetch and the seat's 17:58:57Z fetch — no drift.
- The two cross-row files were fetched via kernel.org after GitHub 429s; equality is proven by sha256 match to the
  anchor cell, so transport difference is not a correctness risk.
- Nothing found that S148 states which the bytes contradict; nothing found that S127 said which any live reader
  still repeats.
