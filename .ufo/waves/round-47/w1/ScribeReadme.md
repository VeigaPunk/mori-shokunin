# ScribeReadme — round-47 w1 report

Seat: ScribeReadme (leaf; no subagents dispatched). Lane: mori-shokunin.
Date: 2026-10-25. Lane HEAD: `63eecf2738db96f46b0bd02b1b2dfd66787493d0` (freeze commit).

Scope: draft the `## Round-47 coverage additions` block for `corpus/README.md`
(Round-44 block style, README.md:628-642) and rule on whether the FR13 Frontier-table
row needs an append-only note. No production file was edited; this report is the only
write (plus read-only scratch fetches under `.scratch/r47-ScribeReadme/`).

## Evidence observed (read-only)

| # | Command / read | Result | Exit |
|---|---|---|---|
| 1 | `read` contract `.ufo/waves/round-47/contract.md` | C2 surface: entry `corpus/knowledge/oom-tracepoints-r47.md`, row S475; P-C2 requirements. | — |
| 2 | `read` `corpus/README.md:560-680` | Round-44 block at lines 628-642 (prose style, bold leads, entry + row range, closing frontier sentence). An uncommitted `## Round-47 coverage additions` block already sits at lines 644-655. | — |
| 3 | `git status --porcelain corpus/README.md`; `git log --oneline -5 -- corpus/README.md`; `git rev-parse HEAD` | ` M corpus/README.md`; newest README commit is round-45 (`18fd68b0`); HEAD = freeze commit. | 0 |
| 4 | `git diff --stat -- corpus/README.md`; `git diff -- corpus/README.md \| grep -c '^+## Round-47'` | diff = exactly +13 lines; exactly one new `## Round-47` heading. The Round-47 block is the entire uncommitted README delta. | 0 |
| 5 | `git status --porcelain` (whole repo) | Also modified: `SKILL.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`; untracked: `corpus/knowledge/oom-tracepoints-r47.md`, `.ufo/waves/round-47/evidence/*`, `w1/`. | 0 |
| 6 | `git diff 63eecf2 -- corpus/SOURCES.md` | SOURCES uncommitted delta = in-place flip of S005 (queued → mined; used-by now names the entry) + appended S475, S476, S477. | 0 |
| 7 | `read` `corpus/knowledge/oom-tracepoints-r47.md` | Entry opens with `source:` (S475, S476, S477), `verified-at: 2026-10-25`, `recheck:`; table first cell `tracepoint`, 8 rows, each with backticked event and field names and `emitted in` path; lifecycle section; boundaries section (knowledge only, no tracer). | — |
| 8 | `grep` S475/S476/S477 in `corpus/SOURCES.md`; `read` full rows 254-256 | S475 mined 2026-10-25 on-release, used-by = entry, anchor cites TRACE_EVENT lines 12/34/76/118/134/150/166/183 and sha256 `82f04ad4108b…`; S476 mined, used-by = entry; S477 mined, used-by = entry. | 0 |
| 9 | `grep -c '^TRACE_EVENT(' corpus/evidence/sources-r47/include_trace_events_oom.h` | **8**. S475's copy `sha256sum` = `82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d`. | 0 |
| 10 | `read` `.ufo/waves/round-47/evidence/host-tracefs.txt` (S477 receipt) | `sudo -n ls /sys/kernel/tracing/events/oom` lists 8 events (compact_retry, finish_task_reaping, mark_victim, oom_score_adj_update, reclaim_retry_zone, skip_task_reaping, start_task_reaping, wake_reaper); `events/oom/enable` cat → `0`; unprivileged ls → Permission denied (rc=2); mark_victim format fields = pid comm total_vm anon_rss file_rss shmem_rss uid pgtables oom_score_adj. | 0 |
| 11 | curl (read-only) of S005's pinned master header `c03c1a14507dfaf8b856c2608f9ac216021fc222` vs v7.2 header into `.scratch/r47-ScribeReadme/` | `cmp` → BYTE_IDENTICAL; both sha256 `82f04ad4108b…`; v7.2 copy greps 8 TRACE_EVENTs. → "S005 re-opened, byte-identical to v7.2" verified. | 0 |
| 12 | `grep` S262 in SOURCES; `ls` knowledge dir | S262 exists (ROMA paper, tier A, mined); `knowledge/oom-victim-context-r41.md` exists. | 0 |

## Draft block (for L1 integration)

Verified against evidence #2/#7-#11. Style follows Round-44 (README.md:628-642): prose,
bold lead, entry path + row range, closing frontier sentence.

```markdown
## Round-47 coverage additions

FR13 ground the map held only as a peer-reviewed abstract (`knowledge/oom-victim-context-r41.md`,
S262) and one queued field-schema row (S005): the **full v7.2 `oom` trace-event set** — eight
events, each with its `TP_STRUCT__entry` field set and the function that emits it — and the
reaper lifecycle (`mark_victim` → `wake_reaper` → `skip`/`start`/`finish_task_reaping`, all
pid-only after the mark). Entry: `corpus/knowledge/oom-tracepoints-r47.md` (S475 header, S476
call sites, S477 this host's tracefs listing; S005 re-opened, byte-identical to v7.2). Count:
8 — `grep -c '^TRACE_EVENT(' corpus/evidence/sources-r47/include_trace_events_oom.h` 2026-10-25.
FR13 stays frontier: no tracer is enabled, installed or proposed (the host's `events/oom/enable`
reads `0` and stays untouched); the entry names what the kernel's own event says (victim pid,
comm, uid, memory) and what it never says (cgroup path, culprit).
```

Claim map:
- "peer-reviewed abstract (…r41.md, S262)" — #12.
- "one queued field-schema row (S005)" — #6 (S005 was queued at freeze; flipped to mined this round).
- "eight events … field set … emitting function" — #7, #9, #10 (8/8 events; row-level fields; `emitted in` paths).
- "reaper lifecycle … all pid-only after the mark" — #7 (lifecycle section; wake/start/finish/skip carry only `pid`).
- "S475 header, S476 call sites, S477 this host's tracefs listing; S005 re-opened, byte-identical to v7.2" — #8, #11.
- "Count: 8 — grep -c … 2026-10-25" — #9 (I ran the identical command today: output `8`, exit 0).
- "no tracer is enabled … events/oom/enable reads 0 … stays untouched" — #10 (receipt cat → `0`); "installed or proposed" is carried from the entry's boundaries section and this lane's no-mutation rule [INFERENCE beyond the record: no install/change was performed by this seat].
- "what it never says (cgroup path, culprit)" — #7 (entry: no event carries cgroup path/memcg name/triggering task; the host receipt's formats confirm no such fields).

Note: the same block already exists uncommitted in `corpus/README.md` (lines 644-655,
evidence #3/#4) and matches this draft word-for-word; L1 may keep it as-is or replace with
this verified copy. It is not in HEAD (freeze commit), so it must be included in the landing
commit.

## FR13 Frontier-row append-only question

**Ruling: no in-place edit and no appended note inside the FR13 row is needed.** Evidence:

1. The row (README.md:353) cites `SOURCES.md:11-12,23-26` — those lines are still S005/S006
   and S017-S020 (evidence #8; S475-S477 were appended at lines 254-256, which do not shift
   earlier lines). The reference stays correct; append-only appends do not invalidate it.
2. The row's statement — "Privilege and version matter; a resident tracer is outside the
   census, so retain this as knowledge/frontier only" — remains true after this round:
   the entry is version-pinned (v7.2), tracefs is root-only (receipt `Permission denied` as
   user), no resident tracer is enabled or proposed (`enable` → `0`), and FR13 stays
   frontier/knowledge-only. No correction is forced by accuracy.
3. Precedent: rounds 34, 42, 43, 44 all left Frontier-table rows untouched when FR6/FR13
   ground moved, recording the movement in per-round coverage sections instead (Round-42
   explicitly: "Frontier rows stay frontier"). The per-round section is the permanent,
   append-only record; the row is historical.

If the L1 ever wants the row's sourcing picture refreshed or FR13 closed/retired, the
append-safe mechanism is a new section / supersede-style note — not an in-place row edit —
matching how SOURCES.md handles in-place changes. That need does not arise this round.

Supplementary observation (SOURCES hygiene, not the README row): this round's uncommitted
SOURCES delta includes an in-place flip of S005 (queued → mined, used-by added; evidence #6).
The append-only gate reports in-place edits, and I could not score the gate against the
uncommitted working tree (it reads a committed revision, and committing is forbidden here),
so the L1 should confirm S005's flip has an acceptable disposition (or a supersede-row
disposition) when it integrates.

## Artifacts

- Report: `.ufo/waves/round-47/w1/ScribeReadme.md` (this file).
- Scratch (read-only fetches): `.scratch/r47-ScribeReadme/s005-master-oom.h`,
  `.scratch/r47-ScribeReadme/v72-oom.h` (byte-identical; sha256 `82f04ad4108b…`).
- No production files touched.
