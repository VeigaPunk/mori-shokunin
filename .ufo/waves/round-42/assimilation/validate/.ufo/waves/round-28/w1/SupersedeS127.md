# SupersedeS127 — S148 row draft, S127 re-open, QUALITY-77 sweep

seat: MoriR28.SupersedeS127 (leaf; no subagents, no background jobs). L1: MoriR28.
lane: /home/vgpnk/Projects/shokunin/mori-shokunin. Named tip: `6ebd518f` (round-27 verifier spot-check, the entering
tip of round 28). Lane master at read time: `079a47c` (round-28 declaration) → later `763d346` (amendment A1).
No lane file was written. Scratch: `/fast/scratch/hyaku/mori-r28/SupersedeS127/`.

## 0. Summary

- S127's row is **byte-identical** at first publication (`126e192d`) and at the tip (`6ebd518f`): the same 2532-byte
  line, sha256 `94e74936b9d894ff2328145f99784fe3ed78f67483dc4af3ce6bbb87c9a48244` both times. **No cell differs.**
  S127 is therefore *not* an in-place-edit defect like S096/S097/S101; it is a first-published-content defect, and
  QUALITY 81 (`corpus/QUALITY.md:373-375`) allows the fix only as a new row whose `teaches` opens `supersedes S127 — `.
- All five carried findings F1–F5 from `.ufo/waves/round-27/w2/ReopenS127.md:134-158` are **re-verified against
  fresh bytes** below. F1–F4 are S127 defects; **F5 (S128's mis-pointed `totalpages/1000` clause) is an S128 defect**
  and lands in the S149 seat, not S148 — see §6.
- One ready-to-paste row (S148) is drafted in §4 and **verified end-to-end in a sandbox clone**: 13 cells, no `|` inside
  any cell, `supersedes S127 — ` prefix with an em dash (U+2014), census `validate` exit 0 (one expected W04, same
  class as the six pre-existing ones), and the round-28 C1 counter reports **no `fail S148` line** — i.e. S148 passes
  every per-row gate in `count-c1.sh`.
- The QUALITY 77 sweep (§5) finds **7 reader lines** in the lane that state S127 by id. Six are live-reader prose and
  must move to S148; one (`corpus/knowledge/oom-victim-selection-r27.md:203`) is a **tsukuroi-registry** mention and
  must **stay**.
- The reader sweep for S127 is **not separable** from the other seven ids: `PROVINCE.md:377` and
  `corpus/README.md:36` write the range `S127–S132`, and `git grep -w` matches every id inside an en-dash range.
  See §7 (a routing hazard for the L1).

## 1. Method and tool record

- Lane reads: read-only `git` only (`show`, `log`, `grep`, `ls-tree`, `rev-parse`, `cat-file`, `status`,
  `diff`). No `jj` command anywhere. No `git add/commit/stash/checkout/switch/reset/pull/push` in the lane.
- Sandbox clones only, under my scratch dir, via `git clone --no-hardlinks`. Commits exist only in those clones.
- Fetches: ordinary `curl` (8.23.0) against the public raw URLs. Every request returned HTTP 200 with no redirect and
  no bot challenge; no browser was used. One retry: `cgroup-v2.rst` first returned **HTTP 429** with a 199-byte body at
  17:58:57Z; re-fetched at **2026-10-22T17:59:10Z** with HTTP 200 and 133,236 B. The 429 body is not evidence.
- Hashes: `sha256sum` (0.8.0). Line checks: `grep -n -F` on the downloaded bytes plus numbered reads.
- Versions observed: GNU bash 5.3.20(1), git 2.56.0, Python 3.14.8, curl 8.23.0, GNU Awk 5.4.1, sha256sum 0.8.0.
- **No tool was installed or upgraded by this seat.** The operator's tooling directive
  (`/home/vgpnk/.omp/agent/RULES.md`) was read; pacman transactions are PAUSED host-wide, so no host package was touched.
- No host state read beyond lane files and public bytes. No `oom_score_adj` read or written, no process signalled, no
  unit touched. No uid, pid, `user-<digits>.slice`, `user@<digits>.service` or unit name of this host's user session
  appears in this report.

### 1.1 Fetched bytes (2026-10-22)

| Source | Accessed (UTC) | HTTP | Bytes | sha256 | Equals the row's own hash? |
|---|---|---|---|---|---|
| `raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c` | 2026-10-22T17:58:57Z | 200 | 98,196 | `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6` | yes (S127 anchor) |
| `git.kernel.org/…/plain/include/uapi/linux/oom.h?h=v7.2` | 2026-10-22T17:58:57Z | 200 | 526 | `6b00b4d0648bcdc9d6be7ea8a33b8e6b842c063e7b2b71bdabd757de773896ae` | yes (S127 anchor) |
| `git.kernel.org/…/plain/kernel/fork.c?h=v7.2` | 2026-10-22T17:58:57Z | 200 | 85,725 | `359882ea981b58f5289293e5644f7c0085a8350e4f1937f39dcb94ae1cd0dd1d` | yes (S127 anchor) |
| `raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c` (S003's file, cross-row) | 2026-10-22T17:58:57Z | 200 | 34,311 | `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` | yes (S003/entry) |
| `raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst` (S092's file, cross-row) | 2026-10-22T17:59:10Z | 200 | 133,236 | `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad` | yes (S092 anchor) |

All three S127 hashes reproduce the values already in the S127 anchor cell, so the row's bytes did not change between
round 27 and now.

## 2. First-published cells (step 1)

`git log --reverse --format=%H -S'| S127 |' -- corpus/SOURCES.md | head -1` → **`126e192d1fa92675bbaabdcfa7fa1b389f01791c`**
("round-27: C1 entry oom-victim-selection-r27, SOURCES S127-S132 and used-by anchors …", 2026-10-22 12:50:10 -0300).
The row is at line 133 of `corpus/SOURCES.md` in that commit and at line 133 at `6ebd518f`.

```
| S127 | Linux fs/proc/base.c, include/uapi/linux/oom.h and kernel/fork.c at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c ; https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/uapi/linux/oom.h?h=v7.2 ; https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/kernel/fork.c?h=v7.2 | code | A | the /proc/<pid>/oom_score and /proc/<pid>/oom_score_adj files at the v7.2 tag and the two facts they depend on: how oom_score is rescaled from oom_badness and why -1000 reads 0, the -1000..1000 write range and the file modes, the oom_score_adj_min floor with CAP_SYS_RESOURCE, and how a write reaches other processes that share the mm (fork copy, MMF_MULTIPROCESS); not the oom_badness body or the kill loop (mm/oom_kill.c, S003), not cgroup memory.oom.group (S002), not this host's per-process values or earlyoom's use of them | fs/proc/base.c:583-599 (proc_oom_score), :586 (totalram_pages() + total_swap_pages), :590 (oom_badness call), :592-597 (LONG_MIN skip, (1000 + badness*1000/totalpages)*2/3, exported [0, 2000]), :1106-1186 (__set_oom_adj), :1118-1122 (legacy path vs current value), :1131-1135 (oom_score_adj_min floor, -EACCES without CAP_SYS_RESOURCE), :1143-1153 (MMF_MULTIPROCESS mm grab), :1155-1158 (assignment, min update, tracepoint), :1164-1177 (mm-sharer propagation, kernel-thread and global-init skip), :1242-1254 (read), :1275-1279 (range check, -EINVAL), :3351-3353 (pid entries) and :3706-3708 (task/tid entries), modes S_IRUGO (read-only oom_score) and S_IRUGO plus S_IWUSR (owner-writable oom_score_adj); include/uapi/linux/oom.h:9-10 (OOM_SCORE_ADJ_MIN (-1000), OOM_SCORE_ADJ_MAX 1000); kernel/fork.c:1728 (zalloc signal struct), :1768-1769 (inheritance in copy_signal), :1949-1966 (copy_oom_score_adj sets MMF_MULTIPROCESS, copies both values); tag v7.2; base.c HTTP 200, 98,196 B, sha256 cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6; oom.h HTTP 200, 526 B, sha256 6b00b4d0648bcdc9d6be7ea8a33b8e6b842c063e7b2b71bdabd757de773896ae; fork.c HTTP 200, 85,725 B, sha256 359882ea981b58f5289293e5644f7c0085a8350e4f1937f39dcb94ae1cd0dd1d | A task's oom_score is (1000 + badness*1000/totalpages)*2/3, 0 when the task is unkillable or oom_score_adj is -1000, and a writer may set oom_score_adj only within -1000..1000, below oom_score_adj_min only with CAP_SYS_RESOURCE, with the write copied to every non-thread process sharing the mm. | mined | 2026-10-22 | on-release | corpus/knowledge/oom-victim-selection-r27.md |
```

**Differing cells: none.** Verified two ways: (a) splitting both lines on `|` gives identical 13 cells; (b) the sha256 of
the raw `| S127 |` line is `94e74936b9d894ff2328145f99784fe3ed78f67483dc4af3ce6bbb87c9a48244` at both `126e192d` and
`6ebd518f`.

Consequence for the L1: S127 needs **no restoration**. It needs only a superseding row, and its cells must stay
byte-identical. `python3 -I -B .ufo/waves/round-27/check-row-identity.py 6ebd518f` prints `rows=144 changed=3` — the
three changed rows are S096, S097 and S101, **not S127**.

## 3. Re-open of S127's sources (step 2), with line numbers

Every statement the corrected row makes, checked against the fetched bytes.

| Claim | Bytes | Verdict |
|---|---|---|
| `oom_score` = `(1000 + badness*1000/totalpages)*2/3` | `base.c:597` `points = (1000 + badness * 1000 / (long)totalpages) * 2 / 3;` (13 words) | holds |
| the value is 0 when `badness == LONG_MIN` | `base.c:596` `if (badness != LONG_MIN)` guards the formula; `points` is initialised 0 at `:587` | holds |
| `totalpages` = RAM + swap | `base.c:586` `unsigned long totalpages = totalram_pages() + total_swap_pages();` | holds |
| the write range is -1000..1000 | `base.c:1275-1279` rejects `< OOM_SCORE_ADJ_MIN` / `> OOM_SCORE_ADJ_MAX` with `-EINVAL`; `oom.h:9-10` `#define OOM_SCORE_ADJ_MIN (-1000)` / `#define OOM_SCORE_ADJ_MAX 1000` | holds |
| below `oom_score_adj_min` needs `CAP_SYS_RESOURCE` | `base.c:1131-1135` `-EACCES` when `(short)oom_adj < task->signal->oom_score_adj_min` and `!capable(CAP_SYS_RESOURCE)`; `:1156-1157` raises the floor only with the capability | holds |
| the write is copied to the other processes of the mm **only through the MMF_MULTIPROCESS path** | `base.c:1143-1150`: the mm is grabbed only when `!task->vfork_done` **and** `mm_flags_test(MMF_MULTIPROCESS, p->mm)`; `:1164-1177`: the loop skips `same_thread_group(task, p)` (`:1165`), kernel threads and global init (`:1169`), and tasks with `p->vfork_done` or a different mm (`:1173`) | holds — **this is F2's correction** |
| `MMF_MULTIPROCESS` is set only for a `CLONE_VM`-only clone | `fork.c:1956` `if ((clone_flags & (CLONE_VM | CLONE_THREAD | CLONE_VFORK)) != CLONE_VM)` returns; `:1961` `mm_flags_set(MMF_MULTIPROCESS, tsk->mm);` | holds (10-word quote) |
| `oom_score_adj` is inherited | `fork.c:1768-1769` copies the value and the floor in `copy_signal`; `:1728` allocates the signal struct | holds |
| the read path | `base.c:1242-1256` `oom_score_adj_read`, value at `:1252` | holds |
| file modes | `base.c:3351` `ONE("oom_score", S_IRUGO, …)`, `:3353` `REG("oom_score_adj", S_IRUGO|S_IWUSR, …)`; same at `:3706` / `:3708` | holds |
| **0 reasons: five, not two** | `mm/oom_kill.c:204-205` (unkillable task) `return LONG_MIN;`; `:207-209` (no mm) `return LONG_MIN;`; `:216-221` `if (adj == OOM_SCORE_ADJ_MIN || mm_flags_test(MMF_OOM_SKIP, p->mm) || in_vfork(p)) { … return LONG_MIN; }`; `oom_unkillable_task` at `:160-167` covers init (`:162`) and kernel threads (`:164`) | holds — **F3's correction** |
| the adjustment is scaled by `totalpages/1000` **inside `oom_badness`** | `mm/oom_kill.c:233` `adj *= totalpages / 1000;`, `:234` `points += adj;` | holds — this is the fact S128 mis-attributed to S127 (F5) |
| `memory.oom.group` lives in **S092's** file, not S002's | `cgroup-v2.rst:1450` `  memory.oom.group`; `:1466` `memory.oom.group values of ancestor cgroups.`; S002's row (`SOURCES.md:8`) names `memory.events` / `memory.peak` / hierarchy only and never `memory.oom.group` | holds — **F1's correction** |

Anchor spans the corrected row tightens (all verified on the fetched bytes): `base.c:583-602` (the function ends at
`:602`, the old row said `:583-599`), `:1106-1187` (ends `:1187`, old `:1106-1186`), `:1242-1256` with the value read at
`:1252` (old `:1242-1254`), and `:1143-1150` for the mm grab (old `:1143-1153`).

## 4. The ready-to-paste row (step 3)

Paste as one line after the S144 row (currently `corpus/SOURCES.md:150`); the registry then ends at line 151.

```
| S148 | Linux fs/proc/base.c, include/uapi/linux/oom.h and kernel/fork.c at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c ; https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/uapi/linux/oom.h?h=v7.2 ; https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/kernel/fork.c?h=v7.2 | code | A | the /proc/<pid>/oom_score and /proc/<pid>/oom_score_adj files at the v7.2 tag and the facts they depend on: how oom_score is rescaled from oom_badness and that -1000 reads 0 (the LONG_MIN return is in S003's mm/oom_kill.c:204-221 at v7.2, cited here, not restated), the -1000..1000 write range and the file modes, the oom_score_adj_min floor with CAP_SYS_RESOURCE, and how a write reaches other processes that share the mm (fork copy, MMF_MULTIPROCESS, set only for a CLONE_VM clone); not the oom_badness body beyond those LONG_MIN returns, nor the kill loop (mm/oom_kill.c, S003), not cgroup memory.oom.group (that text is in the file row S092 opens, cgroup-v2.rst:1450-1466 at v7.2; S002 covers memory events and memory.peak, not it), not this host's per-process values or earlyoom's use of them | fs/proc/base.c:583-602 (proc_oom_score), :586 (totalram_pages() + total_swap_pages), :590 (oom_badness call), :592-597 (LONG_MIN skip, (1000 + badness*1000/totalpages)*2/3, exported [0, 2000]), :1106-1187 (__set_oom_adj), :1118-1122 (legacy path vs current value), :1131-1135 (oom_score_adj_min floor, -EACCES without CAP_SYS_RESOURCE), :1143-1150 (mm grab: not vfork_done, MMF_MULTIPROCESS only), :1155-1158 (assignment, min update, tracepoint), :1164-1177 (mm-sharer propagation; skips the writer's thread group, kernel threads, global init and vfork holders), :1242-1256 (read; the value read at :1252), :1275-1279 (range check, -EINVAL), :3351-3353 (pid entries) and :3706-3708 (task/tid entries), modes S_IRUGO (read-only oom_score) and S_IRUGO plus S_IWUSR (owner-writable oom_score_adj); include/uapi/linux/oom.h:9-10 (OOM_SCORE_ADJ_MIN (-1000), OOM_SCORE_ADJ_MAX 1000); kernel/fork.c:1728 (zalloc signal struct), :1768-1769 (inheritance in copy_signal), :1949-1966 (copy_oom_score_adj sets MMF_MULTIPROCESS and copies both values), :1956-1961 (the CLONE_VM-only test and the MMF_MULTIPROCESS set); cross-row anchors, in S003's file mm/oom_kill.c:204-221 (LONG_MIN returns: unkillable task, no mm, oom_score_adj -1000, MMF_OOM_SKIP, in vfork), :233-234 (adj scaled by totalpages/1000), sha256 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e, and in S092's file cgroup-v2.rst:1450-1466 (memory.oom.group), sha256 a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad, both at v7.2; tag v7.2; base.c HTTP 200, 98,196 B, sha256 cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6; oom.h HTTP 200, 526 B, sha256 6b00b4d0648bcdc9d6be7ea8a33b8e6b842c063e7b2b71bdabd757de773896ae; fork.c HTTP 200, 85,725 B, sha256 359882ea981b58f5289293e5644f7c0085a8350e4f1937f39dcb94ae1cd0dd1d | supersedes S127 — the old row overstated the copy rule and mis-pointed two neighbours. It said the write is copied to every non-thread process sharing the mm; in v7.2 the writer's mm is grabbed only when the writer is not in vfork and its mm carries MMF_MULTIPROCESS (base.c:1143-1150), and the copy loop then skips the writer's own thread group, kernel threads, global init and tasks still in vfork (base.c:1164-1177), while MMF_MULTIPROCESS itself is set only for a clone with CLONE_VM and neither CLONE_THREAD nor CLONE_VFORK (fork.c:1956-1961). It named two reasons for a 0 reading; oom_score reads 0 whenever oom_badness returns LONG_MIN, which covers five cases in S003's file (mm/oom_kill.c:204-221): init or kernel thread, no mm, oom_score_adj -1000, MMF_OOM_SKIP and a task in vfork. It put the -1000 reason in its own scope although that reason is S003's, and it pointed at S002 for memory.oom.group although that text is in S092's cgroup-v2.rst at 1450-1466. Corrected: a task's oom_score is (1000 + badness*1000/totalpages)*2/3 (base.c:597) and reads 0 whenever oom_badness returns LONG_MIN; a writer may set oom_score_adj only within -1000..1000 (base.c:1275-1279; oom.h:9-10) and below oom_score_adj_min only with CAP_SYS_RESOURCE (base.c:1131-1133,1156-1157); and the write reaches the other processes of the mm only through that MMF_MULTIPROCESS path. The adjustment itself is scaled by totalpages/1000 inside oom_badness (S003's mm/oom_kill.c:233-234), not in this row's files. | mined | 2026-10-22 | on-release | corpus/knowledge/oom-victim-selection-r27.md, corpus/lessons/round-28.md, SKILL.md, PROVINCE.md, corpus/README.md |
```

Cell notes for the L1:

- **source / kind / tier** are the verified S127 values (same three URLs, `code`, `A`).
- **scope** keeps S127's subject and adds the two corrected pointers (S003 owns the LONG_MIN return; S092's file owns
  `memory.oom.group`), and drops the two wrong ones.
- **anchor** keeps S127's anchors, tightens three spans, and adds the cross-row anchors the corrected teaching needs
  (S003's `mm/oom_kill.c:204-221` and `:233-234`; S092's `cgroup-v2.rst:1450-1466`) with their sha256.
- **teaches** opens exactly `supersedes S127 — ` (em dash U+2014 + space), then what the old row got wrong, then the
  corrected teaching.
- **status `mined`, opened `2026-10-22`, recheck `on-release`** — the old row's convention.
- **used-by** = the files that cite S127 today and that the QUALITY 77 sweep (§5) moves to S148, plus the round-28
  lesson that carries the Gate line. `corpus/SOURCES.md` itself is excluded (a row must not cite the registry), and the
  two round-27 lesson files are excluded because they are history, not readers — the counter's `used_by_not_citing`
  check requires every used-by path to contain the new id at the landed rev.

### 4.1 Gate line (step 4)

For the round-28 lesson's `## Gate` section (the counter requires the new id's line to carry a 64-hex sha256 and a
quoted span):

```
| S148 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c (with `include/uapi/linux/oom.h` and `kernel/fork.c` at v7.2) | 2026-10-22T17:58:57Z | `base.c:1147` "if (mm_flags_test(MMF_MULTIPROCESS, p->mm)) {" | admit, A, mined; sha256 cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6 |
```

Quote check: `base.c:1147` is 4 words, verbatim (one `grep -c -F` hit at `:1147`), and it is the anchor the corrected
copy rule rests on. The other two files' hashes are in the row's anchor cell. A second located quote the L1 may prefer
is `mm/oom_kill.c:216-221` "if (adj == OOM_SCORE_ADJ_MIN ||" (5 words, verbatim at `:217`).

### 4.2 Sandbox verification of the row (no lane write)

Applied to a clone at `6ebd518f`, with the reader sweep of §5 and a stub `corpus/lessons/round-28.md`:

- `count-c1.sh` (run against the clone, LANE repointed): `row_identity=rows=145 changed=3 removed=0 bad=0`,
  `superseding=1/8 ids=S127`, and **no `fail S148 …` line** — S148 passes prefix, teaches-changed, status, used-by-citing
  and gate-line checks.
- `scripts/sources-census.sh validate --root <sandbox> mori` → exit 0, `mori ok`. One new W04
  (`S148 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes`) — the expected
  same-URL-different-scope warning, in the same class as the six pre-existing W04s. **It is a warning, not an error**,
  and the census still exits 0.
- Falsification controls (same sandbox, deliberately broken): dropping the sha256 from the Gate line → `fail S148
  gate_line`; adding a used-by path that will not cite S148 → `fail S148 used_by_not_citing=…`. Both confirm the
  row is scored by the real counter, not passing vacuously.
- Row shape: 13 `|`-separated fields, no `|` inside any cell, id `S148`, status `mined`, opened `2026-10-22`,
  recheck `on-release`.

## 5. QUALITY 77 sweep — every place whose prose states the defective wording (step 5)

`corpus/QUALITY.md:349-353` requires that every place stating a corrected fact carries the corrected wording at the
commit that carries the correction, and that the superseded wording is removed, not shadowed.

Live readers (`git grep -w -F 'S127' 6ebd518f -- SKILL.md PROVINCE.md corpus/README.md corpus/knowledge`), all at
`6ebd518f`:

| # | Path:line | What it states | Action |
|---|---|---|---|
| 1 | `corpus/knowledge/oom-victim-selection-r27.md:1` | the entry's `source:` line names S127 for "how /proc/<pid>/oom_score is derived, the oom_score_adj write rules and fork inheritance" | move the id to S148 (the description stays true) |
| 2 | `corpus/knowledge/oom-victim-selection-r27.md:37` | "+300 … weighs like an `oom_score_adj` of about +450 [INFERENCE: arithmetic over S127 `base.c:597` …]" | move the id to S148 |
| 3 | `corpus/knowledge/oom-victim-selection-r27.md:55` | heading "### 2. How the kernel scores a process (S003, S127, S092)" | move the id to S148 |
| 4 | `corpus/knowledge/oom-victim-selection-r27.md:63` | "`0 for an excluded task (S127 `fs/proc/base.c:583-599`)`" and "`the code does not clamp it (S127 `base.c:596-599`)`" | move the ids to S148; the anchor text stays true (`:583-599` and `:596-599` are inside the corrected span) |
| 5 | `corpus/knowledge/oom-victim-selection-r27.md:72` | heading "### 3. Where the fleet's adjustment comes from (S129, S130, S127)" | move the id to S148 |
| 6 | `corpus/knowledge/oom-victim-selection-r27.md:84` | "`fork` copies both the value and its floor (S127 `kernel/fork.c:1768-1769,1949-1966`)" | move the id to S148 |
| 7 | `corpus/knowledge/oom-victim-selection-r27.md:89` | "only a writer with `CAP_SYS_RESOURCE` may go below that floor or move it (S127 `fs/proc/base.c:1131-1133, 1156-1157`)" | move the id to S148 |
| 8 | `SKILL.md:722` | "Grounding for every row: … (sources S003, S118, **S127**, S129, S130, S132)" | move the id to S148 |
| 9 | `PROVINCE.md:377` | "… `corpus/knowledge/oom-victim-selection-r27.md` (**S127**–S132, S142)" | range form — see §7 |
| 10 | `corpus/README.md:36` | the entry's used-by cell: "**S127**–S132, S142" | range form — see §7 |

**Must NOT move:** `corpus/knowledge/oom-victim-selection-r27.md:203` — "tsukuroi S115, S118, S120 and **S127** are
`psi.rst`, `cgroup-v2.rst`, `oomd.conf.xml` and a row for mori's `system-pressure-r24.md`, not mori's rows of those
numbers." That is the **tsukuroi registry's** S127, a different row in a different lane's `SOURCES.md`. The round-28
counter's `readers_left` grep excludes lines matching `tsukuroi`, so leaving it is correct and moving it would be a
factual error. (Confirmed: `git grep -w -E 'S127' … | grep -v tsukuroi` drops this line; the counter's own filter is
`grep -v -E 'tsukuroi'`.)

Also unchanged by design: `corpus/SOURCES.md:133` (S127's own row) — QUALITY 81 forbids editing it, and the new row
carries the correction instead.

**Prose that states a defective fact but not by id** (found by sweeping the defective wordings themselves, not the
id): `git grep -F 'every non-thread process' | 'unkillable or oom_score_adj' | 'not cgroup memory.oom.group (S002)' |
'why -1000 reads 0'` at `6ebd518f` returns **only** `corpus/SOURCES.md:133`. No live reader repeats the over-broad copy
rule, the two-reason 0-list, the wrong S002 pointer or the misplaced "why -1000 reads 0". The two facts that do appear
in live prose are stated correctly already: the entry's "0 for an excluded task" (`oom-victim-selection-r27.md:63`) and
"init and kernel threads … and any task at exactly -1000" (`:60-61`) — the latter is the *victim-selection* exclusion
list (which is init, kernel threads and -1000) and is correct for that question; the five-case LONG_MIN list concerns
the *exported oom_score* value and is what S127 got wrong.

## 6. Findings and routing

- **F1 (medium, confirmed)** — S127's scope points at S002 for `memory.oom.group`. S002's row (`SOURCES.md:8`) names
  memory events, memory.peak and hierarchy; the text is at `cgroup-v2.rst:1450-1466` in S092's file. Corrected in S148.
- **F2 (medium, confirmed)** — "copied to every non-thread process sharing the mm" is over-broad. Corrected in S148.
- **F3 (low-medium, confirmed)** — two reasons for a 0 reading; there are five. Corrected in S148.
- **F4 (low, confirmed)** — the scope put the "-1000 reads 0" reason in S127 although it is S003's. Corrected in S148.
- **F5 (low-medium, confirmed) — belongs to the S128 seat, not S148.** The mis-pointed `totalpages/1000` clause and the
  "that code is row S127" pointer live in **S128's** row (`corpus/SOURCES.md:134`), whose anchor cell lists twelve S127
  base.c pointers that all hold. `mm/oom_kill.c:233-234` (`adj *= totalpages / 1000; points += adj;`) is inside
  `oom_badness` — S003's file — and v7.2 `oom_badness` has no 3% root term at all (`grep -inE 'root|3 ?%|percent'`
  over the fetched `oom_kill.c` → no match). **S148 states the corrected attribution explicitly** ("scaled by
  totalpages/1000 inside `oom_badness` (S003's mm/oom_kill.c:233-234), not in this row's files"), so the S149 seat can
  point at S148 for the code and at S003 for the scaling. The S149 row itself is not this seat's to draft.
- **F6/F7/F8 (low, from the round-27 report, out of scope here)** — the writer-identity claim in the entry
  (`:98-99`), the unlabelled INFERENCE on the SKILL ceiling row (`:727-728`) and the wave-1 report's unfinished access
  times remain as reported. Not re-verified by this seat; flagged so the L1 does not lose them.
- **F9 (low, observation, now partly answered)** — S127's used-by listed only the knowledge entry although the lesson
  and SKILL also cited it. S148's used-by names all five reader paths that will cite it (§4), which the counter's
  `used_by_not_citing` check enforces.
- **F10 (low, observation, still open)** — `corpus/lessons/round-27.md:37` and `:87` cite "CORPUS.md Rules 2"; no
  `CORPUS.md` exists in the lane tree (`git ls-tree -r` finds none; the fleet-root file is outside the lane). Unchanged
  by this seat; the L1 may want to name the real file.

## 7. Routing hazard for the L1 (read before landing)

`PROVINCE.md:377` and `corpus/README.md:36` write the range `S127–S132`. `git grep -w -E 'S127'` **matches inside an
en-dash range** (verified: a file containing only `(S127–S132, S142)` is matched by `-w -E 'S127'`). The round-28
counter's `readers_left` count therefore drops from **27 lines at `6ebd518f`** to **20** only after the S127 sweep in a
sandbox — and it cannot reach 0 while the range text still names the other owed ids.

Concretely: the S127 sweep must rewrite the range, and the rewrite must simultaneously be consistent with the S149
(S128), S150 (S129) and S151 (S131) seats. In the sandbox I used `(S130, S132, S148–S151,` for `PROVINCE.md` and
`S130, S132, S142, S148–S151` for `corpus/README.md`, i.e. the S130/S132 members of the old range kept their ids and
the four superseded members moved to their new ids. **The L1 owns that reconciliation**; it is a cross-seat edit, not
a per-seat one, and my sandbox numbers are a proposal, not a landing.

## 8. Out of scope for this seat

- S145/S146/S147 (S096, S097, S101 restoration) and S149/S150/S151/S152 (S128, S129, S131, S140) — other seats.
- The round-27 lessons, `LOG.md` and `SCORECARD.md` are history files and keep S127; the counter exempts them
  (`READERS="SKILL.md PROVINCE.md corpus/README.md corpus/knowledge"`).
- `corpus/SOURCES.md:133` (S127) stays byte-identical; the L1 edits it never.
- `tools/mori-oom-killers.py` and the C2 case freeze (r26 D7) — a different claim.
- Retention scan, the five round-26 selftests and the r25 R1/R5 sandboxed fixes — other seats.

## 9. Artifact paths

- Draft row (paste-ready, 1 line): `/fast/scratch/hyaku/mori-r28/SupersedeS127/draft-S148.txt`
- Fetched bytes: `/fast/scratch/hyaku/mori-r28/SupersedeS127/{base.c,oom.h,fork.c,oom_kill.c,cgroup-v2.rst}`
- S127 row at first publication and at the tip: `/fast/scratch/hyaku/mori-r28/SupersedeS127/s127-first.txt`,
  `s127-tip.txt` (byte-identical)
- Sandbox clone used for verification: `/fast/scratch/hyaku/mori-r28/SupersedeS127/clone3` (tip `cd597d4`)
- Counter copies repointed at the sandbox: `/fast/scratch/hyaku/mori-r28/SupersedeS127/count-c1-clone3.sh`,
  `check-row-identity.py`
- Census sandbox tree: `/fast/scratch/hyaku/mori-r28/SupersedeS127/root-final`
- This report: `.ufo/waves/round-28/w1/SupersedeS127.md`
