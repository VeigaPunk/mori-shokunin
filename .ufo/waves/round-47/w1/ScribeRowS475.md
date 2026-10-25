# ScribeRowS475 — round-47 wave w1 report (SOURCES row S475 + S005 status recommendation)

Seat: `ScribeRowS475` (scribe, leaf — no subagents). Lane: mori-shokunin.
Scope assigned: draft SOURCES.md row S475 for Linux include/trace/events/oom.h at tag v7.2
(11-column schema), draft its Gate line (URL, access date, ≤25-word located quote), and
recommend whether the existing row S005 changes status (rule 2: only
status/recheck/used-by may change, logged old→new).

No production file was edited; drafts are fenced blocks below. Only this report was
written (plus scratch dir `~/.scratch/r47-ScribeRowS475/`).

## 1. Observed evidence (command + output + exit)

Freeze commit `63eecf2738db96f46b0bd02b1b2dfd66787493d0` (2026-10-25 16:32:10 -0300,
"round-47: freeze — contract P-C1/P-C2, … v7.2 OOM source copies, …") commits the four
v7.2 source copies under `corpus/evidence/sources-r47/`.

### 1.1 Committed copy hash (bash `sha256sum`, exit 0)
```
82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d  .../sources-r47/include_trace_events_oom.h
452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e  .../sources-r47/mm_oom_kill.c
439ae8ec1e47cbf38770865e53e98bf2229e32a20c4b0f8178e6f19f34edbc50  .../sources-r47/mm_page_alloc.c
cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6  .../sources-r47/fs_proc_base.c
```

### 1.2 Live URL fetch (read tool, 2026-10-25)
`https://raw.githubusercontent.com/torvalds/linux/v7.2/include/trace/events/oom.h`
fetched; text identical to the committed copy. Live sha256 via `curl -fsSL … | sha256sum`
(exit 0): `82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d` — byte-equal
to the committed copy.

### 1.3 TRACE_EVENT count and line numbers (committed copy)
`grep -c '^TRACE_EVENT(' …/include_trace_events_oom.h` → `8`. The eight events and the
header line of each `TRACE_EVENT(`:
| tracepoint | header line |
|---|---|
| `oom_score_adj_update` | 12 |
| `reclaim_retry_zone` | 34 |
| `mark_victim` | 76 |
| `wake_reaper` | 118 |
| `start_task_reaping` | 134 |
| `finish_task_reaping` | 150 |
| `skip_task_reaping` | 166 |
| `compact_retry` | 183 (inside `#ifdef CONFIG_COMPACTION`) |

### 1.4 TP_STRUCT__entry field schemas (committed copy)
- `oom_score_adj_update` (12): `pid`, `comm`, `oom_score_adj` (lines 18–22).
- `reclaim_retry_zone` (34): `node`, `zone_idx`, `order`, `reclaimable`, `available`,
  `min_wmark`, `no_progress_loops`, `wmark_check` (lines 46–55).
- `mark_victim` (76): `pid`, `comm`, `total_vm`, `anon_rss`, `file_rss`, `shmem_rss`,
  `uid`, `pgtables`, `oom_score_adj` (field list lines 82–90; `TP_STRUCT__entry` block
  82–91).
- `wake_reaper` (118): `pid` (lines 123–125).
- `start_task_reaping` (134): `pid`.
- `finish_task_reaping` (150): `pid`.
- `skip_task_reaping` (166): `pid`.
- `compact_retry` (183): `order`, `priority`, `result`, `retries`, `max_retries`, `ret`
  (lines 194–201).

### 1.5 Tag peel (GitHub API, 2026-10-25)
`refs/tags/v7.2` is an annotated tag object `237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63`
(tagger Linus Torvalds, 2026-08-16) whose object is the commit
`8d3ae59288f1e7d58d76558a6ee96d533bc5019f`. The peel claim in the draft anchor is verified.

### 1.6 Registry state at freeze vs now
`git show 63eecf2:corpus/SOURCES.md` line 11 (S005): `status = queued`, `used-by = —`.
Current working-tree `corpus/SOURCES.md` line 11 (S005): `status = mined`, `used-by =
corpus/knowledge/oom-tracepoints-r47.md`. `git diff --stat 63eecf2 -- corpus/SOURCES.md`
→ `4 insertions(+), 1 deletion(-)` — consistent with the S005 status/used-by cell change
plus three new rows (S475, S476, S477). No other S005 cell changed (id, source, kind,
tier, scope, anchor, teaches, opened, recheck identical at freeze and now).

The knowledge entry `corpus/knowledge/oom-tracepoints-r47.md` exists in the working tree
(untracked, post-freeze), opens with `source:` / `verified-at:` / `recheck:`, cites
S475/S476/S477, and carries a table whose header first cell is `tracepoint` with one row
per event; its Boundaries section references S005: "S005 holds the `mark_victim` schema at
an earlier master commit."

## 2. Draft SOURCES.md row S475 (11-column, no `|` in cells)

```markdown
| S475 | Linux include/trace/events/oom.h at tag v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/trace/events/oom.h | code | A | the OOM tracepoint set and TP_STRUCT__entry field schemas at tag v7.2; not the running kernel and not any other tag | TRACE_EVENT at lines 12, 34, 76, 118, 134, 150, 166, 183; mark_victim TP_STRUCT__entry lines 82-91; tag v7.2 peels to commit 8d3ae59288f1e7d58d76558a6ee96d533bc5019f; copy corpus/evidence/sources-r47/include_trace_events_oom.h sha256 82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d | The oom system defines eight trace events and only mark_victim carries the victim's comm, uid and memory fields | mined | 2026-10-25 | on-release | corpus/knowledge/oom-tracepoints-r47.md |
```

Note: the working tree already carries an integrated S475 row whose cells are equivalent to
this draft (same source URL, kind code, tier A, scope with the same negative bounds, same
line anchors, same peel commit, same sha256, same teaches, status mined, opened
2026-10-25, recheck on-release, same used-by). The only micro-difference: the integrated
row writes `mark_victim entry lines 82-92`; the precise field-list block is 82–91 (fields
82–90, closing paren at 91, blank at 92). Immaterial for the counter; no correction to the
immutable anchor is requested.

## 3. Draft Gate line (round lesson `## Gate`, per CORPUS.md rule 1)

- URL: `https://raw.githubusercontent.com/torvalds/linux/v7.2/include/trace/events/oom.h`
- Access date: 2026-10-25
- Located quote (9 words ≤ 25), from the committed copy, `mark_victim` `TP_printk`
  format string, lines 105–114:
  > `pid=%d comm=%s total-vm=%lukB anon-rss=%lukB file-rss:%lukB shmem-rss:%lukB uid=%u pgtables=%lukB oom_score_adj=%hd`
  (word count verified with `wc -w` → 9.)

## 4. S005 recommendation (rule 2: status/recheck/used-by only, logged old→new)

Recommendation: **yes — S005 status should change `queued` → `mined`**, and its `used-by`
should gain `corpus/knowledge/oom-tracepoints-r47.md`, because the new entry cites S005
(the earlier-master `mark_victim` schema). This change is already present in the working
tree; only the allowed cells changed (verified by freeze-vs-now diff), so it conforms to
rule 2. The round lesson must log it old→new: `status queued → mined; used-by — →
corpus/knowledge/oom-tracepoints-r47.md` (the L1 integration should record this if the
lesson does not already carry it).

One observation for the L1's judgment: S005's citation lives in the entry's Boundaries
prose ("S005 holds the `mark_victim` schema at an earlier master commit"), not in the
entry's `source:` frontmatter trio (which names only S475/S476/S477). If the lane reads
"mined = cited by a used-by path" strictly as frontmatter `source:` citation, the status
could stay `queued`; the entry plainly relies on S005's content, so I recommend `mined`.

## 5. Out-of-scope (left to other seats / L1)

- C1 `mori-pin-check.py` and C2 `count-c2.py` runs and their controls: other seats / L1
  (not run here; this seat is source-row drafting only).
- Host tracefs reading: S477 seat (receipt `.ufo/waves/round-47/evidence/host-tracefs.txt`).
- Emitting-call-site verification (S476) and integration of the entry: L1.
