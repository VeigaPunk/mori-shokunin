# Mo52ConnSiblings — sibling-overlap scan for C2 (overcommit / CommitLimit / Committed_AS)

Seat: Mo52ConnSiblings. Scan run 2026-10-26 from the fleet root, read-only.

## Scan command (verbatim)

```
grep -rliE 'overcommit|CommitLimit|Committed_AS|overcommit_memory|user_reserve_kbytes' /home/vgpnk/Projects/shokunin/*-shokunin/corpus /home/vgpnk/Projects/shokunin/*-shokunin/SKILL.md /home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md
```

Exit 2: `audio-shokunin/SKILL.md` and `game-dev-2d-shokunin/SKILL.md` do not exist (path errors only); every `corpus` tree, the remaining `SKILL.md`s and all `PROVINCE.md`s were scanned. `.scratch` and `.ufo/waves` were not in scope (no such subtree sits inside a `corpus` path).

Term counts per hit are from `grep -oE … | sort | uniq -c` on the same file set.

## Hits

| # | owning lane | file:line | matched term (count) | nature |
|---|---|---|---|---|
| 1 | kaidoku | corpus/evidence/round-34/elf/e12.bin | `overcommit_memory` (1, as the literal string `/proc/sys/vm/overcommit_memory`) | ELF fixture: `file` → ELF 64-bit LSB PIE, static-pie linked, stripped, BuildID[sha1]=6b23bbd795db03c2c6a634c54a2bb89663e4ce68, for GNU/Linux 4.4.0. Round-34 lesson (`corpus/lessons/round-34.md:80`) identifies e12 as a static carrier test fixture (`/usr/bin/sln`) selected with no requirement/string table. Evidence byte stream, not a claim. |
| 2 | mori (own) | corpus/knowledge/overcommit-commit-limit-r52.md | the new C2 entry itself | claim data |
| 3 | mori (own) | corpus/SOURCES.md (rows S497–S501, lines 276–280) | overcommit terms in the five new rows | claim data |
| 4 | mori (own) | corpus/evidence/sources-r52/overcommit-accounting.rst.v7.2, vm.rst.v7.2, util.c.v7.2, mman.h.v7.2, mmap.c.v7.2 | the five new v7.2 source copies | claim data |
| 5 | mori (own, pre-existing) | corpus/evidence/recheck-r32/S001.src (1× overcommit), S002.src (5× overcommit) | kernel source copies from round-32 recheck | evidence copy under corpus/evidence/ — outside the round-52 sweep path (sweep = `corpus/SOURCES.md corpus/knowledge SKILL.md`), receipt `evidence/sweep-overcommit.txt` confirms 0 files there at 4f266ef2 |
| 6 | mori (own, pre-existing) | corpus/evidence/sources-r50/cgroup-v2.7.2.html (5× overcommit) | round-50 source copy (S489 cgroup-v2 doc) | evidence copy, outside sweep path |
| 7 | mori (own, pre-existing) | corpus/evidence/sources-r51/proc.rst.v7.2 (10× overcommit, 6× CommitLimit, 2× Committed_AS); meminfo.c.v7.2 (1× CommitLimit, 1× Committed_AS) | round-51 source copies (S492, S494) | evidence copies, outside sweep path; the new entry's `fs/proc/meminfo.c:125-126` citation points into meminfo.c.v7.2 (verified exact: line 125 `show_val_kb(m, "CommitLimit:    ", vm_commit_limit());`, line 126 `show_val_kb(m, "Committed_AS:   ", committed);` with `committed = vm_memory_committed();` at line 46) |
| 8 | tsukuroi | corpus/knowledge/oom-event-plane.md:351 (row 8 of the diagnostics table) | `overcommit_memory` (1) | host sysctl value read: `oom_dump_tasks=1`, `panic_on_oom=0`, `overcommit_memory=0`, `swappiness=60` — used to argue dumps are enabled and `panic_on_oom=1` would be catastrophic for a global OOM. No CommitLimit/Committed_AS anywhere in the file. |
| 9 | tsukuroi | corpus/knowledge/kill-event-deep-r8.md:262 (row 8) | `overcommit_memory` (1) | same pattern: observed `overcommit_memory=0`, `dmesg_restrict=1`; no CommitLimit/Committed_AS. |
| 10 | tsukuroi | corpus/knowledge/btrfs-space-r30.md:18 | `overcommit` (1) | btrfs space-allocation homonym: "The kernel's metadata reservations may overcommit only against unallocated space; 'If there is no unallocated space to be had, all reservations are kept within the free space in the allocated metadata chunks' (S159 lines 176-178)." Filesystem reservation accounting, not the VM commit ledger. |
| 11 | tsukuroi | corpus/SOURCES.md:165 (row S159) | `overcommit` (2) | line-range description of the btrfs space-info C source: "unallocated-space overcommit limit and reclaim buffer … overcommit is allowed only against unallocated device space" — same btrfs homonym. |

## Duplicate / contradict / contested scope

- **No duplication.** tsukuroi's OOM/kill entries carry the host's observed `vm.overcommit_memory` *value* (mode 0) as one diagnostic row; they assert no semantics of `CommitLimit`/`Committed_AS` and never use those terms (term counts above). Their use — mode 0 is the observed default and dumps are enabled — is consistent with the new entry's S497/S498 claims ("Mode 0 is the default and refuses only allocations that are plainly too large"). No contradiction found.
- **No contradiction in substance.** The only shared word with tsukuroi's btrfs entry is the homonym "overcommit" in the btrfs space-reservation sense; it is unrelated to the v7.2 VM commit ledger and to `/proc/meminfo`.
- **Contested scope: none, and the partition is explicit.** tsukuroi's PROVINCE.md:28 = "never restarts services. Detection and report; the operator remediates." PROVINCE.md:30-33 = "Host memory and kill-event measurements support OS triage; they do not establish which fleet wave caused pressure or whether an endpoint works. The existing census reports those signals; fleet correlation belongs to mori (../mori-shokunin/PROVINCE.md:6-16)." The new entry (lines 63-66) fences exactly this: mori reads `/proc/sys/vm/overcommit_memory` plus the two meminfo lines and never writes a `vm.*` sysctl; choosing/changing the mode is operator-owned; "this entry claims no sysctl ownership for either lane." That matches mori's own PROVINCE.md:12-15 (refuses OS state → tsukuroi; owns resource runway read-only, including memory pressure). Neither province grants either lane sysctl-write ownership.
- **kaidoku e12.bin** is a fixture; no knowledge claim in kaidoku touches overcommit (no other kaidoku hit). No contested scope.

## PROVINCE boundary-wording check (mori entry lines 63-66 vs tsukuroi PROVINCE.md)

- Entry: "Host OS-state triage is tsukuroi's ground (`../tsukuroi-shokunin/PROVINCE.md:8-14,28`: detection and report, the operator remediates)".
- `:28` supports "detection and report; the operator remediates" verbatim. ✓
- `:8-14` lists tsukuroi's owned surfaces (pacman state, systemd user units/timers, journal/boot triage, driver/firmware plane) — none of them memory. The memory-relevant tsukuroi clause is at `:30-33` ("Host memory and kill-event measurements support OS triage … fleet correlation belongs to mori"), which the entry does not cite but which agrees with what the entry says. So the citation range is loose, not wrong: `:28` alone already carries the "detection and report; operator remediates" wording, and the memory handoff lives at `:30-33`.

## Findings

- **LOW** — mori `corpus/knowledge/overcommit-commit-limit-r52.md` lines 63-66: parenthetical citation `../tsukuroi-shokunin/PROVINCE.md:8-14,28` — `:8-14` does not mention memory (surfaces list only); the memory-relevant handoff is `:30-33`. Substance is correct; the L1 may add `:30-33` to the citation if the entry is corrected. Not a C1/C2 counter issue (the locator arm reads Axes rows and SHONEN boxes, not this entry).
- **LOW** — tsukuroi `corpus/knowledge/oom-event-plane.md:351` and `corpus/knowledge/kill-event-deep-r8.md:262` record `overcommit_memory=0` as an observed value; if the host mode changed, those rows would stale. No contradiction; optional future cross-reference to mori's new entry for the semantics (routing suggestion only, no action this round).
- **INFO** — kaidoku `corpus/evidence/round-34/elf/e12.bin` contains the literal string `/proc/sys/vm/overcommit_memory`; fixture byte stream, no claim, no action.
- **INFO** — no sibling claim contradicts or duplicates the v7.2 overcommit ledger claims; the only terminological neighbor (tsukuroi btrfs-space-r30) uses the homonym in a different subsystem.
- **INFO** — the round-52 sweep receipt `evidence/sweep-overcommit.txt` is consistent with the working tree: the sweep path (`corpus/SOURCES.md corpus/knowledge SKILL.md` at 4f266ef2) was clean; all pre-existing occurrences in the mori lane live under `corpus/evidence/` (prior-round source copies), outside the sweep path.
