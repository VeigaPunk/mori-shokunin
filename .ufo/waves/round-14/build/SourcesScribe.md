# MoriR14.SourcesScribe — source census and mutable-cell recommendations

Seat: MoriR14.SourcesScribe (scribe, leaf). Milestone: restore OOM alarm and structured fleet routing. Axis: coverage.
Scope: read `corpus/SOURCES.md` (36 rows); in-memory parse, not the lane census gate; report only. **No edits to SOURCES, no other files changed.**

Tooling: none installed or updated by this seat. Actions: one in-memory Python parse (eval kernel), read-only greps, one read of the S032 page.

## 1. Census (in-memory parser, `corpus/SOURCES.md` lines 7–42)

Parse method: split table rows on `|`, header `id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by`, skip separator rows, require 11 cells per row.

| Check | Result |
|---|---|
| Data rows | **36** (S001–S036) |
| Malformed rows (cell count ≠ 11) | 0 |
| Duplicate ids / duplicate URLs | 0 / 0 |
| Ids contiguous S001…S036 | yes |
| Tier | A **33**, B **2** (S021, S029), C **1** (S030) |
| Status | mined **15**, queued **20**, rejected **1** (S030) |
| Tier × status | A/mined 15, A/queued 18, B/queued 2, C/rejected 1 |
| Kind | docs 15, code 10, tool 4, spec 3, community 2, book 1, own-work 1 |
| Recheck | on-release 27, 90d 5, 180d 3, 365d 1 |
| Every mined row has a non-empty used-by | yes |
| Every queued/rejected row has used-by `—` | yes |
| Every used-by path exists on disk | yes |

Per-row record (line / tier / status / kind / opened / recheck / used-by):

| id | line | tier | status | kind | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|
| S001 | 7 | A | mined | docs | 2026-10-19 | on-release | lessons/2026-10-15-free-lunch-measurements-counter-baselines.md |
| S002 | 8 | A | mined | docs | 2026-10-19 | on-release | knowledge/oom-kill-counter-kernel-only-r12.md, knowledge/userspace-oom-killers-r12.md |
| S003 | 9 | A | mined | code | 2026-10-19 | on-release | 4 knowledge notes (oom-kill-counter, kill-classes, kernel-oom-line-attribution, userspace-oom-killers) |
| S004 | 10 | A | mined | code | 2026-10-19 | on-release | knowledge/oom-kill-counter-kernel-only-r12.md, knowledge/kernel-oom-line-attribution-r12.md |
| S005 | 11 | A | queued | code | 2026-10-19 | on-release | — |
| S006 | 12 | A | queued | code | 2026-10-19 | on-release | — |
| S007 | 13 | A | mined | docs | 2026-10-19 | on-release | knowledge/oom-kill-counter-kernel-only-r12.md, knowledge/userspace-oom-killers-r12.md |
| S008 | 14 | A | queued | docs | 2026-10-19 | on-release | — |
| S009 | 15 | A | queued | docs | 2026-10-19 | on-release | — |
| S010 | 16 | A | queued | docs | 2026-10-19 | on-release | — |
| S011 | 17 | A | mined | code | 2026-10-19 | on-release | knowledge/oom-kill-counter-kernel-only-r12.md, knowledge/userspace-oom-killers-r12.md |
| S012 | 18 | A | mined | docs | 2026-10-19 | 90d | knowledge/userspace-oom-killers-r12.md |
| S013 | 19 | A | mined | code | 2026-10-19 | on-release | knowledge/kill-classes-by-message-id-r12.md, knowledge/userspace-oom-killers-r12.md, knowledge/structured-journal-scopes-r13.md |
| S014 | 20 | A | mined | docs | 2026-10-19 | on-release | knowledge/kill-classes-by-message-id-r12.md, knowledge/kernel-oom-line-attribution-r12.md, knowledge/structured-journal-scopes-r13.md |
| S015 | 21 | A | mined | docs | 2026-10-19 | on-release | knowledge/kill-classes-by-message-id-r12.md, knowledge/kernel-oom-line-attribution-r12.md, knowledge/structured-journal-scopes-r13.md |
| S016 | 22 | A | mined | tool | 2026-10-19 | on-release | knowledge/oom-kill-counter-kernel-only-r12.md, knowledge/userspace-oom-killers-r12.md |
| S017 | 23 | A | queued | tool | 2026-10-19 | on-release | — |
| S018 | 24 | A | queued | tool | 2026-10-19 | 90d | — |
| S019 | 25 | A | queued | code | 2026-10-19 | on-release | — |
| S020 | 26 | A | queued | code | 2026-10-19 | on-release | — |
| S021 | 27 | B | queued | community | 2026-10-19 | 180d | — |
| S022 | 28 | A | queued | spec | 2026-10-19 | on-release | — |
| S023 | 29 | A | queued | spec | 2026-10-19 | on-release | — |
| S024 | 30 | A | queued | spec | 2026-10-19 | 90d | — |
| S025 | 31 | A | queued | tool | 2026-10-19 | 90d | — |
| S026 | 32 | A | queued | docs | 2026-10-19 | on-release | — |
| S027 | 33 | A | queued | docs | 2026-10-19 | on-release | — |
| S028 | 34 | A | queued | docs | 2026-10-19 | 180d | — |
| S029 | 35 | B | queued | book | 2026-10-19 | 365d | — |
| S030 | 36 | C | rejected | community | 2026-10-19 | 180d | — |
| S031 | 37 | A | mined | docs | 2026-10-19 | on-release | knowledge/verdict-contract-r13.md |
| S032 | 38 | A | queued | docs | 2026-10-19 | on-release | — |
| S033 | 39 | A | queued | docs | 2026-10-19 | on-release | — |
| S034 | 40 | A | mined | own-work | 2026-10-19 | 90d | knowledge/roster-truth-r12.md |
| S035 | 41 | A | mined | code | 2026-10-20 | on-release | knowledge/structured-journal-scopes-r13.md |
| S036 | 42 | A | mined | code | 2026-10-20 | on-release | knowledge/structured-journal-scopes-r13.md |

## 2. Citation cross-check (used-by versus citing text)

Searched `corpus/knowledge/`, `corpus/lessons/`, `corpus/QUALITY.md`, `corpus/README.md`, `SKILL.md`, `PROVINCE.md`, `LOG.md` for `S0nn` ids and compared with each row's used-by.

- Mined rows: used-by is consistent with citing knowledge notes for S002, S003, S004, S007, S011, S012, S013, S014, S015, S016, S031, S034, S035, S036. Lessons-only citations (round-12/13 lessons that enumerate rows) are not use-sites and are not counted.
- **Gap A (milestone-relevant, new row needed, not a mutable edit):** `corpus/knowledge/structured-journal-scopes-r13.md:14` cites `sd-messages.h:178-179,185` and `process-util.c:2306-2309` (`CLD_KILLED` → "killed") at the pinned systemd commit `cf8ebfc6…`. No registry row covers either file. The note's `unit_sigkill_record` filter (`EXIT_CODE=killed EXIT_STATUS=9`, line 46) depends on the "killed" mapping, so that claim has no registered source. `sd-messages.h` path is `src/systemd/sd-messages.h` (per the note's own recheck line 3). The `process-util.c` path is not stated in the note and must be resolved by the opener.
- **Gap B:** `structured-journal-scopes-r13.md:45` (`segfault_signal11`, `COREDUMP_SIGNAL=11`) uses a field that S032 documents, but the note cites no S-id.
- **Gap C:** `corpus/knowledge/surfaces-r7.md:123-128` and `surfaces-r8.md` rely on the `/proc/diskstats` sectors-written field, which S033 documents, with no S-id cited.
- **Gap D:** S020 (queued) is used as evidence in `corpus/lessons/round-12.md:44` (M21) and cited in `corpus/QUALITY.md:34`, with used-by `—`.

## 3. Milestone source support (OOM alarm, structured fleet routing)

Already supported with registered, mined rows; no mutable change is required for these:
- Kernel/unit OOM notice identity (`fe6faa94…`): S013 (`:604-616`), used-by includes `structured-journal-scopes-r13.md`.
- Field scope and no-MESSAGE output (`--output-fields`, `MESSAGE_ID` trust, `_BOOT_ID`): S014, S015, both with the structured note in used-by.
- Unit-failure result and process-exit fields (`UNIT_RESULT`, `EXIT_CODE`, `EXIT_STATUS`): S035 (catalog `:561-575`) and S036 (`src/core/unit.c:6333-6392`), both with the structured note in used-by.
- Fleet membership is lane-defined (roster census). S034 is used-by `roster-truth-r12.md` and explicitly does not establish complete fleet coverage. No registered row supports a "fleet vs non-fleet, owner tsukuroi" split; that split is an adjacency/ownership claim that cannot be cited to a SOURCES row. Recommend no SOURCES change for it.

The only milestone-blocking source gap is Gap A, and its fix is a new immutable row (section 5), not a mutable cell change.

## 4. Recommended mutable old → new changes (report only; not applied)

Milestone-required mutable changes: **none**.

Conditional mutable changes (apply only when the named consumer edit lands in the same round):

| id | cell | old | new | condition |
|---|---|---|---|---|
| S032 | status | `queued` | `mined` | structured note cites S032 at `:45` (COREDUMP_SIGNAL) and an access record with a ≤25-word located quote is appended to the round-14 lesson. Priority: low, not OOM/fleet. |
| S032 | used-by | `—` | `corpus/knowledge/structured-journal-scopes-r13.md` | same condition as above |
| S033 | status | `queued` | `mined` | `surfaces-r7.md` (or a new note) cites S033 for the sectors-written field, stating the mapping between S033 "Field 7" and `/proc/diskstats` column 10. Priority: low. |
| S033 | used-by | `—` | `corpus/knowledge/surfaces-r7.md` | same condition as above |
| S020 | status | `queued` | `mined` | L1 rules that `lessons/round-12.md` M21 is a genuine use (it is currently the only consumer) |
| S020 | used-by | `—` | `corpus/lessons/round-12.md` | same ruling as above |

Also noted, no change proposed: S013, S014, S015, S031, S034, S035, S036 used-by values are complete for their current consumers. S013/S014/S015/S031 were re-opened 2026-10-20 per the round-13 lesson, but the immutable `opened` cells remain 2026-10-19; the re-open record lives in `corpus/lessons/round-13.md`. S013 and S035 share one URL, which the census reports as an informational W04 (already known, not an error).

## 5. Proposed new immutable row (not a mutable change; L1 to file only after opening)

Proposed `S037` (appended; contiguous with S036): kind `code`, tier `A`, status `queued` until opened, recheck `on-release`, used-by `—` until the consuming note cites it. Scope: systemd process-result mapping of `CLD_KILLED` to `killed`, the `EXIT_CODE=killed` value the milestone's SIGKILL filter depends on. Anchor: `process-util.c:2306-2309` (path to confirm at the pinned commit) and `src/systemd/sd-messages.h:178-185`, commit `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af`. Teaches: `CLD_KILLED` maps to the string `killed` in process-exit records; signal-9 sender and cause remain unobserved. Once opened, the structured note's `unit_sigkill_record` row cites `S037` alongside `S035/S036`.

## 6. Evidence limits

- The census is an in-memory parse of the table text; it did not run `scripts/sources-census.sh` or the lane gate, and it did not verify contract-v1 rules beyond observable vocabulary and structure.
- S032 was re-read this turn (`https://www.freedesktop.org/software/systemd/man/latest/systemd-coredump.html`, systemd 262): the page documents the `COREDUMP_SIGNAL` field and its example entry `COREDUMP_SIGNAL=11`. I did not record a numbered located quote, so the conditional S032 change remains conditional.
- Not verified: URL reachability for the other 35 rows; the `process-util.c` path; whether S034's tier A for an own-work receipt is permitted under contract v1 `[INFERENCE: possibly tier-inflation, not checked against contract text]`.
- No commits, no edits to SOURCES, MANIFEST, SHONEN, LOG, or any verifier file.
