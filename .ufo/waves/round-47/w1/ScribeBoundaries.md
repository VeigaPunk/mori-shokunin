# ScribeBoundaries — round-47 wave w1 (build) report

Seat: `ScribeBoundaries` (scribe, leaf — no subagents). Wave: `mori-r47-w1-build`.
Date: 2026-10-25. Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`.

Scope: draft the `## Boundaries` and `## What it changes for mori` sections for the C2
entry `corpus/knowledge/oom-tracepoints-r47.md`, grounded in the FR13 row read first and in
the committed kernel header copy. Drafts are fenced blocks below; nothing production was
edited.

## Evidence read (all absolute paths, read-only)

- Frozen contract: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-47/contract.md`
  (lines 48-78: C2 surface, sources, named limits; lines 80-84 separability).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/PROVINCE.md`:
  - line 16 — "Detection and report only — never remediation."
  - line 56 — FR13 row boundary: "Privilege and version matter; a resident tracer is outside
    the census, so retain this as knowledge/frontier only."
  - line 44 — FR1 (no raw MESSAGE; a host record alone does not prove a fleet-caused kill).
  - line 53 — FR10 (never enable or tune a killer; fleet attribution of a victim stays frontier).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/README.md`:
  - line 353 — FR13 row (same boundary sentence).
  - lines 616-619 — round-42 note: victim-context abstract anchor
    (`knowledge/oom-victim-context-r41.md`, S262): "the kernel's victim selection has no
    container context, so a host observer cannot attribute an OOM to a container from the
    kernel record alone".
  - lines 644-655 — Round-47 coverage additions: FR13 ground held only as abstract (S262)
    and one queued field-schema row (S005); full v7.2 `oom` trace-event set = eight events;
    "FR13 stays frontier: no tracer is enabled, installed or proposed (the host's
    `events/oom/enable` reads `0` and stays untouched); the entry names what the kernel's own
    event says (victim pid, comm, uid, memory) and what it never says (cgroup path, culprit)."
- Committed source copy: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r47/include_trace_events_oom.h`.
- Staged assimilation entry (read-only, `/home/vgpnk/Projects/shokuknow`):
  `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/oom-tracing-tracepoints-r42.md`.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` — S475 row at line 254,
  S476 at line 255, S477 at line 256.

## Commands run (observed evidence)

1. `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-ScribeBoundaries grep -n '^TRACE_EVENT(' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r47/include_trace_events_oom.h`
   → output: `12:TRACE_EVENT(oom_score_adj_update,` `34:TRACE_EVENT(reclaim_retry_zone,`
   `76:TRACE_EVENT(mark_victim,` `118:TRACE_EVENT(wake_reaper,`
   `134:TRACE_EVENT(start_task_reaping,` `150:TRACE_EVENT(finish_task_reaping,`
   `166:TRACE_EVENT(skip_task_reaping,` `183:TRACE_EVENT(compact_retry,`; exit code 0.
   → eight TRACE_EVENT declarations at header lines 12, 34, 76, 118, 134, 150, 166, 183.
2. `sha256sum corpus/evidence/sources-r47/include_trace_events_oom.h` (cwd = lane repo, TMPDIR as above)
   → `82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d` — matches the
   sha256 pinned in the S475 row (SOURCES.md line 254) and cited by the entry.
3. `git rev-parse HEAD` → `63eecf2738db96f46b0bd02b1b2dfd66787493d0` (the freeze commit,
   per contract).
4. `git ls-files corpus/knowledge/oom-tracepoints-r47.md corpus/evidence/sources-r47/`
   → lists only the four `sources-r47/` copies; `corpus/knowledge/oom-tracepoints-r47.md`
   is **not tracked at the freeze tip**, i.e. it exists in the working tree untracked at my
   reading time. It was not modified or created by this seat.
## Findings

F1. **Eight TRACE_EVENTs, not three.** Confirmed by grep on the committed v7.2 copy
(header lines 12, 34, 76, 118, 134, 150, 166, 183): `oom_score_adj_update`,
`reclaim_retry_zone`, `mark_victim`, `wake_reaper`, `start_task_reaping`,
`finish_task_reaping`, `skip_task_reaping`, `compact_retry` (the last inside
`#ifdef CONFIG_COMPACTION`, header line 182-219).

F2. **mark_victim's field set** (header lines 81-91, `TP_STRUCT__entry`): `pid` (int),
`comm` (string), `total_vm` (ulong), `anon_rss` (ulong), `file_rss` (ulong),
`shmem_rss` (ulong), `uid` (uid_t), `pgtables` (ulong), `oom_score_adj` (short).
What it lets an observer attribute: the victim's pid, comm, uid and its memory at mark
time. What it does not carry: no cgroup path, no memcg name, and no field naming the task
that triggered the allocation failure (no culprit). Only `mark_victim` in the set carries
comm/uid; the four reaper events (`wake_reaper`, `start_task_reaping`,
`finish_task_reaping`, `skip_task_reaping`) are pid-only.

F3. **Staged headline correction.** Staged entry
`oom-tracing-tracepoints-r42.md`: line 2 headline "The OOM lifecycle an observer can hook
is three named tracepoints"; lines 12-13 claim "has exactly three named tracepoints". The
same staged entry quotes the paper (S507) as "OOM-related kernel tracepoints such as
`mark_victim`, `start_task_reaping`, and `finish_task_reaping`" (lines 15-16) — i.e. the
paper's own wording is the **"such as"** list of examples, not an exhaustive enumeration. The
The committed header defines eight events. The "exactly three" headline is therefore
refused; the C2 entry catalogues all eight events (one row per TRACE_EVENT, per P-C2).

F4. **FR13 boundary is already fixed in the province/corpus row and carries over verbatim:**
PROVINCE.md:56 and corpus/README.md:353 — resident tracer outside the census, knowledge/
frontier only; corpus/README.md:653-655 — no tracer enabled/installed/proposed, host
`events/oom/enable` reads 0 and stays untouched, mori reads and never enables tracing.

F5. Working-tree observation: `corpus/knowledge/oom-tracepoints-r47.md` already exists
untracked at the freeze tip (not in `git ls-files`) with content covering the same two
sections. Per lane rules this seat did not touch it; the L1 integrates.

## Draft: `## Boundaries` (for the C2 entry; fenced)

```markdown
## Boundaries

- **Knowledge only — outside the one-shot census.** FR13's boundary row is unchanged:
  "Privilege and version matter; a resident tracer is outside the census, so retain this as
  knowledge/frontier only" (`PROVINCE.md:56`; `corpus/README.md:353`). The entry catalogues
  what the kernel's own header defines; it enables, installs or proposes no tracer. Mori
  reads; it never enables tracing — the host's `events/oom/enable` reads `0` and stays
  untouched (`corpus/README.md:653-654`). No census surface, probe or finding id is added.
- **What `mark_victim`'s fields let an observer attribute:** the victim's pid, comm, uid
  and its memory at mark time (`total_vm`, `anon_rss`, `file_rss`, `shmem_rss`,
  `pgtables`, `oom_score_adj`) — the `TP_STRUCT__entry` set of the v7.2 copy
  (`include_trace_events_oom.h` lines 81-91, S475). The four reaper events carry only a pid.
- **What it does not carry:** no cgroup path, no memcg name, and no culprit field — no
  event names the task whose allocation failed. This matches the victim-context anchor: the
  kernel's victim selection has no container context, so a host observer cannot attribute an
  OOM to a container from the kernel record alone (`corpus/README.md:616-619`). Kill
  attribution to a fleet seat still has to come from the journal/cgroup evidence the lane
  already holds (FR1, FR10; `PROVINCE.md:44,53`).
- **Version-specific:** event set and field layouts hold for the v7.2 tag copies pinned by
  sha256 in `.ufo/waves/round-47/count-c2.py`; re-derive from a new tag before relying on
  them. The counter checks names, field sets and one emitting call per event in the
  committed copies — it does not check prose, lifecycle ordering claims, or the host's
  running kernel (contract lines 76-78; a host tracefs reading is separate own-work evidence,
  S477).
```

## Draft: `## What it changes for mori` (for the C2 entry; fenced)

```markdown
## What it changes for mori

- **The headline correction lands here.** The staged assimilation entry
  `oom-tracing-tracepoints-r42.md` headlined "exactly three named tracepoints" (line 2;
  claim lines 12-13). The paper it cites lists tracepoints "such as" `mark_victim`,
  `start_task_reaping`, and `finish_task_reaping` (staged lines 15-16, source S507) — three
  named examples, not an exhaustive count. The committed Linux v7.2 `include/trace/events/
  oom.h` defines **eight** `TRACE_EVENT`s (lines 12, 34, 76, 118, 134, 150, 166, 183), so
  the C2 entry catalogues eight rows, one per event, and refuses the "exactly three" claim.
- **FR13 stops being a bare abstract anchor.** It was grounded only as a peer-reviewed
  abstract (`knowledge/oom-victim-context-r41.md`, S262) and one queued field-schema row
  (S005) (`corpus/README.md:646`). It is now a concrete, version-pinned event set: which
  events exist in the `oom` system at v7.2, each event's `TP_STRUCT__entry` field schema,
  and which committed v7.2 function emits each event (S475, S476).
- **The attribution vocabulary gains a precise ceiling.** The only identity-bearing event is
  `mark_victim`: pid, comm and uid of the victim, plus its memory at mark time. No event in
  the set carries a cgroup path or a culprit. A future attribution claiming "this seat
  caused that OOM" would be claiming something the kernel's own record does not support;
  kill attribution to a fleet seat still routes through the journal/cgroup evidence the lane
  already holds (FR1, FR10).
```

## Out of scope / not run

- No tool installs or upgrades were needed (nothing installed; pacman untouched; no
  `~/.local/bin` changes). Tooling-authorization rule read as satisfied by "no tool".
- Not run by this seat (other w1 seats' lanes): `count-c2.py`, `mori-pin-check.py`, the
  four C2 controls, mutation tests, host tracefs reads (`sudo -n …` under
  `/sys/kernel/tracing/events/oom/` was not repeated here; S477 owns that receipt).
- Host state: no tracing enabled, nothing written to tracefs; no git/jj mutation.

## Artifacts

- This report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-47/w1/ScribeBoundaries.md`
- Scratch: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-ScribeBoundaries/`
  (created; empty of working files).

Report: .ufo/waves/round-47/w1/ScribeBoundaries.md
