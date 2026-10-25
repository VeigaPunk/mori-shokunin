# ScribeRowS476 — round-47 w1 report (SOURCES row S476 draft + duplicate-URL verdict)

Seat: ScribeRowS476 (leaf scribe, godspeed). Lane: mori-shokunin. Report path (lane-relative): `.ufo/waves/round-47/w1/ScribeRowS476.md`. No production file was edited; only this report (plus scratch under `.scratch/r47-ScribeRowS476/`) was written. No tool installs/upgrades were needed or performed (verified against `/home/vgpnk/.omp/agent/RULES.md`; nothing was installed, so no install record).

## 1. Behavior and evidence (command + output + exit code)

### 1.1 Committed round-47 source copies (anchors for S476)

Committed copies under `corpus/evidence/sources-r47/`, sha256 (local, read-only):

```
$ sha256sum corpus/evidence/sources-r47/mm_oom_kill.c corpus/evidence/sources-r47/mm_page_alloc.c corpus/evidence/sources-r47/fs_proc_base.c corpus/evidence/sources-r47/include_trace_events_oom.h
452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e  .../mm_oom_kill.c
439ae8ec1e47cbf38770865e53e98bf2229e32a20c4b0f8178e6f19f34edbc50  .../mm_page_alloc.c
cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6  .../fs_proc_base.c
82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d  .../include_trace_events_oom.h
```

Cross-checks against already-committed rows: `fs_proc_base.c` digest equals S127/S148's base.c digest (`cef1a2cf…`); `mm_oom_kill.c` digest equals S148's cross-row anchor for oom_kill.c (`452f1348e79c…`); `include_trace_events_oom.h` digest equals S475's copy digest (`82f04ad4108b…`). The four committed copies are byte-consistent with the digests the registry already pins.

### 1.2 The oom trace-event set (committed header copy)

`include_trace_events_oom.h` defines 8 `TRACE_EVENT`s (lines 12, 34, 76, 118, 134, 150, 166, 183): `oom_score_adj_update`, `reclaim_retry_zone`, `mark_victim`, `wake_reaper`, `start_task_reaping`, `finish_task_reaping`, `skip_task_reaping`, `compact_retry` (`compact_retry` under `CONFIG_COMPACTION`). Generated trace call names match `trace_<name>(`.

### 1.3 Emitting calls (grep over committed copies)

`mm_oom_kill.c`:
- `:562 static bool oom_reap_task_mm(struct task_struct *tsk, struct mm_struct *mm)`
- `:567 trace_skip_task_reaping(tsk->pid);`, `:578 trace_skip_task_reaping(tsk->pid);`
- `:582 trace_start_task_reaping(tsk->pid);`
- `:595 trace_finish_task_reaping(tsk->pid);`
- `:656 static void wake_oom_reaper(struct timer_list *timer)`; `:673 trace_wake_reaper(tsk->pid);`
- `:751 static void mark_oom_victim(struct task_struct *tsk)`; `:774 trace_mark_victim(tsk, cred->uid.val);`

`mm_page_alloc.c`:
- `:4201 static inline bool should_compact_retry(...)` (CONFIG_COMPACTION branch); `:4265 trace_compact_retry(order, priority, compact_result, retries, max_retries, ret);` (the `:4278` stub variant has no trace call; the function is `:4580 should_reclaim_retry(...)`; `:4630 trace_reclaim_retry_zone(z, order, reclaimable, available, min_wmark, *no_progress_loops, wmark);`

`fs_proc_base.c`:
- `:1106 static int __set_oom_adj(struct file *file, int oom_adj, bool legacy)`; `:1158 trace_oom_score_adj_update(task);`

All 8 events have exactly one emitting call site in the committed v7.2 copies (skip_task_reaping has two call sites in the same function). Reaper-path order in `oom_reap_task_mm`: skip (567/578) → start (582) → finish (595); `wake_oom_reaper` (673) precedes reaping; `mark_oom_victim` (774) is the victim-marking emitter.

### 1.4 Tag v7.2 verification (read-only remote read)

```
$ git ls-remote https://github.com/torvalds/linux.git 'refs/tags/v7.2' 'refs/tags/v7.2^{}'
237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63	refs/tags/v7.2
8d3ae59288f1e7d58d76558a6ee96d533bc5019f	refs/tags/v7.2^{}
exit=0
```

The tag peels to commit `8d3ae59288f1e7d58d76558a6ee96d533bc5019f`, matching the peel already recorded in S475. UNVERIFIED: the three raw.githubusercontent.com URLs' HTTP bytes were not re-fetched this seat (the anchors are the committed copies, whose digests are verified above).

### 1.5 Live census run (read-only) against the current working tree

```
$ TMPDIR=.../.scratch/r47-ScribeRowS476 /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
mori	W04	S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori	W04	S073 duplicate url docs.python.org/3/library/pathlib.html across scopes
mori	W04	S074 duplicate url kubernetes.io/docs/concepts/architecture/controller across scopes
mori	W04	S075 duplicate url ftp.gnu.org/gnu/bash/bash-5.3.tar.gz across scopes
mori	W04	S076 duplicate url michaelfeathers.silvrback.com/characterization-testing across scopes
mori	W04	S147 duplicate url raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md across scopes
mori	W04	S148 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S149 duplicate url man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html across scopes
mori	W04	S150 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml across scopes
mori	W04	S166 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S168 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
mori	W04	S201 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c across scopes
mori	W04	S218 duplicate url github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch across scopes
mori	W04	S220 duplicate url raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c across scopes
mori	W04	S228 duplicate url docs.python.org/3/library/os.path.html across scopes
mori	W04	S349 duplicate url www.openeuler.org/whitepaper/openEuler%2024.03%20LTS%20%E6%8A%80%E6%9C%AF%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf across scopes
mori	W04	S351 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S470 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S476 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
exit=0
```

The S476 row as it stands in the working tree passes validation (no E01–E12, no E04, exit 0, lane `ok`), adding exactly one new informational W04: `S476 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes` (vs S003). No W04/E04 is emitted for S476's share of the base.c URL (S127/S148/S166 already carry that URL; see 1.6 for why S476 contributes no new line for it).

## 2. Draft SOURCES.md row S476

The working-tree `corpus/SOURCES.md` already contains an S476 row with anchors identical to 1.3; the draft below is this seat's refined proposal (adds the four committed-copy digests, function start lines, and the tag peel; keeps the same scope, gate quote, status/opened/recheck/used-by cells).

```markdown
| S476 | Linux mm/oom_kill.c, mm/page_alloc.c and fs/proc/base.c at tag v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c ; https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/page_alloc.c ; https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c | code | A | which v7.2 function emits each oom trace event and the order the OOM reaper path emits them; not the event field schemas (S475) | oom_kill.c:567,578,582,595 in oom_reap_task_mm (:562), :673 in wake_oom_reaper (:656), :774 in mark_oom_victim (:751); page_alloc.c:4265 in should_compact_retry (:4201, CONFIG_COMPACTION), :4630 in should_reclaim_retry (:4580); base.c:1158 in __set_oom_adj (:1106); copies corpus/evidence/sources-r47/mm_oom_kill.c sha256 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e, mm_page_alloc.c sha256 439ae8ec1e47cbf38770865e53e98bf2229e32a20c4b0f8178e6f19f34edbc50, fs_proc_base.c sha256 cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6; tag v7.2 peels to commit 8d3ae59288f1e7d58d76558a6ee96d533bc5019f (ls-remote 2026-10-25) | mark_victim is emitted in mark_oom_victim and the reaper reports skip, start and finish by pid only | mined | 2026-10-25 | on-release | corpus/knowledge/oom-tracepoints-r47.md |
```

Required cells (per seat assignment): kind `code`, tier `A`, scope = which function emits each oom tracepoint at v7.2, anchor = the `trace_<name>(` line numbers in the committed copies under `corpus/evidence/sources-r47/`, status `mined`, opened `2026-10-25`, recheck `on-release`, used-by the C2 entry (`corpus/knowledge/oom-tracepoints-r47.md`). All satisfied.

Gate quote (teaches column), 16 words, located:

> mark_victim is emitted in mark_oom_victim and the reaper reports skip, start and finish by pid only

Located at `mm_oom_kill.c:774` (mark_oom_victim) and `:567,:578,:582,:595` (oom_reap_task_mm) in the committed copy.

## 3. Comparison with S127/S148 and duplicate-URL verdict

S127 and S148 (opened 2026-10-22, round 27) are the same v7.2 proc-file source row: both carry `https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c` as their first URL, S148 supersedes S127, and the census already flags `S148 duplicate url … fs/proc/base.c across scopes` (and `S166 duplicate url … fs/proc/base.c across scopes`; line 1.5). S476 shares that base.c URL, but as its third URL.

Census mechanism (from `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, read-only): the gawk `row_pass` runs `url_of()` on the **first** URL match only per row (lines 600–605), so only a row's first URL participates in W04/E04. W04 (`:644-645`) fires when the URL was already seen and the `(url, scope)` pair is new; E04 (`:646-649`) fires only when the same `(url, scope)` pair was previously seen by a non-rejected row and the current teaches does not match `/supersedes S[0-9]{3}/`. URL normalization strips scheme, trailing slash and fragment, lowercases the host, keeps path case.

Verdict, observed and explained:
- **W04 — yes, one new line.** S476's first URL `raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c` is already used by S003 → `mori W04 S476 duplicate url … mm/oom_kill.c across scopes`. Warning-only; exit stays 0; lane `ok`.
- **W04 for base.c — no new line.** base.c is S476's third URL (not parsed) and S127/S148/S166 already hold it; no new warning is produced.
- **E04 — no.** E04 requires the exact same (URL, scope) pair. S476's scope text ("which v7.2 function emits each oom trace event and the order the OOM reaper path emits them; not the event field schemas (S475)") differs from S003's scope (kernel OOM counter updates / kernel summary-victim records) and from S127/S148's scope (/proc oom_score/oom_score_adj file semantics). Confirmed empirically: the live validate run prints no E04 for S476.

How to avoid E04 (guidance, grounded in the script):
1. Keep the scope cell distinct from every existing row sharing any of the row's URLs — S476 does (its scope is the emitter/order question; S003 and S127/S148 are different questions). Distinct scope ⇒ W04 at worst.
2. If a same-URL + same-scope row were ever intended, the teaches cell must contain `supersedes S[0-9]{3}` (e.g. open with `supersedes S127 —`), per the round-16 precedent; otherwise E04 fires for non-rejected rows. This seat does not recommend superseding — S003/S127/S148 stay valid neighbours of S476.
3. Keep status non-rejected (mined) — rejected rows are exempt from E04 but would add W02 if the teaches is thin, and are not the intent.
4. Spell the shared URL identically to the existing row (normalization is scheme/fragment/trailing-slash tolerant, path case-sensitive), and remember only the first URL of the cell is censused — putting a shared URL later in the cell is not a duplicate-flag avoidance technique, just an observation about the parser.

## 4. Scope notes

- Lane bounds respected: no subagents; no edits to SKILL.md, SOURCES.md, corpus/, tools/, LOG.md, SCORECARD.md or any other production file; no git/jj mutations (only read-only `git ls-remote`/`sha256sum`/`grep`/`read` and the read-only census script); `/home/vgpnk/Projects/shokuknow` untouched.
- The working-tree S476 row (already present) matches this seat's anchors exactly; the L1 may integrate the 1.2 draft (with digests) or the existing row as-is — the census outcome is identical (W04 S476 oom_kill.c only, exit 0).
