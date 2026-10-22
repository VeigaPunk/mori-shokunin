# ConnSiblingOverlap — sibling-overlap scan for C1 (mori round 27, wave 1)

Seat: MoriR27.ConnSiblingOverlap (connector, leaf). Read-only. Date 2026-10-22.
Tools installed or updated: none.
Scratch: `/fast/scratch/hyaku/mori-r27/ConnSiblingOverlap/` holds `git show 157ee255:<path>` copies of the
four named tsukuroi entries (sha256: oom-event-plane `30cb31fd…be76`, kill-event-deep-r8 `cd2fe9bb…0861`,
memory-pressure-r25 `ecafdcdd…bdcd25`, systemd-user-plane `85ada775…35465e`). Line numbers below are at
tsukuroi `157ee255`. `git diff --quiet 157ee255 HEAD` on oom-event-plane.md, kill-event-deep-r8.md and
systemd-user-plane.md → `unchanged-at-HEAD` (tsukuroi HEAD `420a1ae1`); only memory-pressure-r25.md moved
(an appended "R26 source-row note", tsukuroi commits `ef72f10`, `75449b1`), so its lines 1-392 are stable.

## Axes

Depth (C1's own axis), adjacency (observed 6), freshness (observed 5). No-harm guards: privacy (counts and
classes only) and the lane retention scan (this report carries no settings path, session id or routing key).

## Sweep

Pattern (case-insensitive) `oom_score|OOMScoreAdjust|earlyoom.{0,40}victim|victim.{0,40}earlyoom|oom_adj|
ManagedOOM|memory\.oom\.group|--prefer|--avoid|sort-by-rss` over every `*-shokunin/corpus/knowledge`
(21 lanes). Hits: tsukuroi 10 files, mori 2 files (`journal-alarm-routing-r14.md:56`,
`userspace-oom-killers-r26.md:1,19,145,193`), every other lane 0. A wider pass for
`earlyoom|oom.?killer|badness` adds kaidoku (2 files), tabi (2 files), and one false hit in kotodama
(`symbolism-synthesis-method.md:28`, unrelated). Kumitate has 0 hits for both patterns; its seat-lifecycle
and kill-sender lines were read directly (rows K1-K3).

## Table — sibling path:line → fact → cite-only or conflict with C1

C1 basis used to judge each row (round cache, primary bytes): Linux v7.2 `mm/oom_kill.c`
(sha256 `452f1348…6b4e`, scout cache `MoriR27.SrcKernelOomBadness/oom_kill.c`): points are
rss + swap + page tables (lines 228-229), then `adj *= totalpages / 1000; points += adj;` (233-234); one pass
over every process keeps the maximum (340, 359-360: "We choose the process with the highest number of
'points'."); global `totalpages = totalram_pages() + total_swap_pages` (263), memcg OOM uses the memcg max
(258) and scans only that memcg (367). systemd v262 `man/systemd-system.conf.xml` (sha256 `16135998…9b0c58`)
lines 305-306. earlyoom v1.9.0 `kill.c` (sha256 `b32e0fad…0bf3`): default picks the largest `oom_score`
(457-458), signals with `kill()` then `process_mrelease` (242, 251).

| # | Sibling path:line | Fact (paraphrase; no pid, uid, command line) | Verdict for C1 |
|---|---|---|---|
| T1 | tsukuroi `oom-event-plane.md:60-69` | Event A (2026-10-13) was a global kernel OOM; the victim, python class, ran at `oom_score_adj` +200 | cite-only: a worked example C1 may cite; kernel victim, predates earlyoom |
| T2 | tsukuroi `oom-event-plane.md:104-119` | Event-A dump: victim held ≈26.6 GiB anon + ≈27.1 GiB swapped; adj histogram of the dump's task table; "[inference] the victim was the dominant anonymous-memory holder" | cite-only: consistent with max-points selection (rss + swap term dominates) |
| T3 | tsukuroi `oom-event-plane.md:116` | the +200 band "is exactly the band the kernel scans first" | **conflict (mechanism)**: no band is scanned first; one pass keeps the max of footprint + adj×totalpages/1000 (`oom_kill.c:233-234,340,362-376`) |
| T4 | tsukuroi `oom-event-plane.md:349` | §7 row 6: "the +200 band is chosen first"; operator lever "`OOMScoreAdjust=` in units (user-scope units are the user's)" | **conflict (mechanism)** on "chosen first", as T3; lever wording conflicts with T9 (see sibling conflicts) |
| T5 | tsukuroi `oom-event-plane.md:51,280,345`; `kill-event-deep-r8.md:256` | earlyoom not installed / absent (measured 2026-10-14) | cite-only, dated: superseded for current use by R18 notices `oom-event-plane.md:442-452`, `kill-event-deep-r8.md:350-354` (earlyoom 1.9.0-1 active since 2026-10-20 09:57:11 -03, `oom-event-plane.md:448`) |
| T6 | tsukuroi `kill-event-deep-r8.md:138-145,323` | Live 2026-10-14 bands: +300 (an `other`-class browser's children), +200 (143 user-session processes), +100 exactly the user manager and its pam helper ("`user@.service` sets `OOMScoreAdjust=100`"), 0, −250/−900/−1000 system defenders | cite-only: same bands C1 should find; host file agrees today (`/usr/lib/systemd/system/user@.service:35` → `OOMScoreAdjust=100`) |
| T7 | tsukuroi `kill-event-deep-r8.md:142` | quotes `man systemd.exec`: default is "the OOM score adjustment level of the service manager itself" | **conflict (incomplete source)**: true for the system manager; for an unprivileged user manager systemd v262 `systemd-system.conf.xml:305-306` makes the default manager + 100 (see source tension below) |
| T8 | tsukuroi `kill-event-deep-r8.md:148-152`, `:260`, `:295` (Q12) | "The origin of the +200 band is [unknown]"; Q12 open: "Origin of the session-wide +200" | **conflict (C1 resolves)**: user manager at +100 (`user@.service`, systemd commit `ce7de0ba8ef3…` "units: run user service managers at OOM score adjustment 100") plus `DefaultOOMScoreAdjust=` default +100 for an unprivileged manager (commit `d4a402e4f693…`, both 2021-09-30; `systemd-system.conf.xml:305-306`) gives +200 to every user service; scopes inherit from their launcher (fork copies it; LabratInherit probe: parent shell 200 → `sh` and `python` children 200, `probe-output.txt:2-4`) |
| T9 | tsukuroi `kill-event-deep-r8.md:260` | "Scope units expose no `OOMScoreAdjust` property, so per-scope steering must come from the launcher" | cite-only: agrees with `systemd.exec.xml:1295-1296` ("for executed processes") [INFERENCE: a scope executes nothing, so the setting has nothing to apply to] |
| T10 | tsukuroi `kill-event-deep-r8.md:148` | "[inference] under a kernel OOM the scan prefers the higher-scored, larger-RSS tasks first"; the +100 manager being the event-B casualty contradicts a kernel pick | cite-only for the conclusion (a +100 manager with small footprint cannot out-score a +200 client of equal size); **wording conflict** on "first", as T3 |
| T11 | tsukuroi `kill-event-deep-r8.md:258` | swap plane 2026-10-14: 30.25 GiB swapfile + 4 GiB zram | **freshness conflict for any totalpages figure**: today `swapon --show --bytes` lists only `/swap/swapfile` 32484225024 B; `/proc/meminfo` MemTotal 31721800 kB, SwapTotal 31722876 kB → totalpages 15,861,169, so +200 is worth 3,172,200 pages ≈ 12.10 GiB of footprint today. C1 must date its totalpages; event-era weight differed |
| T12 | tsukuroi `kill-event-deep-r8.md:266`, `:381` | `ManagedOOMPreference=` named as the oomd steering knob; R25 notice narrows it (only matters for cgroups oomd monitors) | cite-only: systemd-oomd is not a victim chooser on this host (inactive, disabled, mori `userspace-oom-killers-r26.md` F1); C1 should not mix it with `oom_score_adj` |
| T13 | tsukuroi `memory-pressure-r25.md:318-327,364-365` | a userspace killer moves no kernel kill counter; "an earlyoom kill would not move the kernel counters" | cite-only: agrees with earlyoom `kill.c:242,251` (plain `kill()` + `process_mrelease`) vs kernel increment at `oom_kill.c:935-936`. Already mori S125 — an anchor on S125, not a new row |
| T14 | tsukuroi `memory-pressure-r25.md:344-346` | cites "S119, Linux v7.2 `mm/oom_kill.c`", sha256 `452f1348…6b4e` | cite-only, **numbering hazard**: tsukuroi S119 = kernel `oom_kill.c`; mori S119 = earlyoom `main.c`. Same bytes as the round cache (`sha256sum` match). Mori S003 (`corpus/SOURCES.md:9`) records no digest; C1's re-open of `oom_kill.c` is an anchor on mori S003 and may add this digest there |
| T15 | tsukuroi `memory-pressure-r25.md:392` | "S127 supersedes S125 (mori facts …)" — tsukuroi S127 is a row about mori `system-pressure-r24.md` (tsukuroi `corpus/SOURCES.md:133`) | **numbering hazard**: mori S127 will be a new C1 row; never write a bare "S127" in a cross-lane line |
| T16 | tsukuroi `boot-plane.md:247-248` | `user@.service` read: `KillMode=mixed`, `OOMScoreAdjust=100` | cite-only |
| T17 | tsukuroi `degraded-triage-r4.md:211-213`, `driver-firmware-plane.md:166-168`, `journal-boot-plane.md:110-111` | restatements of the event-A kill line with `oom_score_adj` 200 | cite-only (duplicates of T1; cite T1 only) |
| T18 | tsukuroi `systemd-user-plane.md:114,181` | the event-A kill counted among kernel err lines; open question on its relation to coredump storms | cite-only, no selection content |
| M1 | mori `userspace-oom-killers-r26.md:19,193` | r26 refuses to read `--avoid`/`--prefer` values; a send line means "earlyoom signalled a victim it selected" | in-lane predecessor: C1 deepens "selected" into how; must keep the r26 privacy stance (presence only) |
| M2 | mori `journal-alarm-routing-r14.md:56` | `oom_group_kill` when `memory.oom.group=1` | in-lane, cite-only for the `memory.oom.group` row |
| P1 | kaidoku `2026-10-18-arc2-r6-pe-midrung.md:28-32`, `2026-10-18-arc2-r7-pe-wall.md:27-31` | a kaidoku decompile run under a `MemoryMax` cap was kernel-OOM-killed with `constraint=CONSTRAINT_MEMCG`; the tool envelope typed it `cancelled` | cite-only, and a scope rule for C1: in a memcg OOM the adj weight is relative to the memcg max (`oom_kill.c:258`) and only that memcg is scanned (`:367`); a fleet tool's own status label misnames the killer |
| P2 | tabi `webbridge-daemon-disposition.md:271`, `webbridge-revival-assessment.md:62-67` | event B (2026-10-14) called an "OOM-teardown event"; a tabi daemon's death "consistent with" it; per-process victim list unknown | conflicts with tsukuroi (see below); for C1: event B predates earlyoom (T5), so it is outside any earlyoom-send share |
| K1 | kumitate `swarm-wave-lifecycle.md:114-119` | seat status map `cancelled|canceled|aborted→aborted`; failure classes list no OOM or signal class (`process_exit` nearest) | cite-only, attribution boundary: a dead seat's status cannot say which killer acted |
| K2 | kumitate `ops-watchers.md:178-180` | a fleet watchdog SIGKILLs a watch daemon whose state file is stale > 6 min | cite-only: a non-OOM fleet kill sender exists; process deaths are not earlyoom sends |
| K3 | kumitate `omp-task-contract.md:134` | the Hub can abort and kill an agent; a kill is revivable | cite-only, same boundary as K2 |

## Conflicting statements between siblings

1. **Where scope steering can live.** tsukuroi `oom-event-plane.md:349` offers "`OOMScoreAdjust=` in
   units (user-scope units are the user's)" as the lever; tsukuroi `kill-event-deep-r8.md:260` (four days'
   later capture, same lane) says scope units expose no `OOMScoreAdjust` property and steering "must come
   from the launcher". r8 is the later and better-supported reading (`systemd.exec.xml:1295-1296`); r8 does
   not mark itself as superseding line 349, and no R18/R25 notice touches that cell.
2. **Event B's killer.** tabi `webbridge-daemon-disposition.md:271` names event B an "OOM-teardown
   event"; tsukuroi `kill-event-deep-r8.md:277-279` (E6) says the kernel-OOM hypothesis "loses its last
   support" and "the *sender* of the SIGKILL remains unknown". Both agree the victim list is unknown.
3. **One process, two bands (internal to one entry).** tsukuroi `oom-event-plane.md:111` lists the eighth
   top consumer (an `other`-class process) at +200; the same entry's `:349` names that process in a
   "−900/0" group. Both cite §2.3; one is wrong. C1 should not reuse either cell.
4. **Population, not conflict.** `oom-event-plane.md:115` (event-A dump, all uids in the OOM domain,
   2026-10-13) and `kill-event-deep-r8.md:323` (live, one user's processes, 2026-10-14) give different
   histograms of different populations; never add or compare them as one count.

Source tension C1 must state, not smooth: systemd v262 `systemd.exec.xml:1299-1300` says the unset
default is "the OOM score adjustment level of the service manager itself, which is normally at 0", while
`systemd-system.conf.xml:305-306` says the default, "except if the service manager is run for an
unprivileged user, in which case this defaults to the service manager's OOM adjustment value plus 100".
The host's measured +200 under a +100 manager (T6) matches the second; the first describes the system
manager only. Both files are in the round cache (`SrcSystemdExecOomScoreAdjust/`).

## Proposed move (one, bounded)

Carry the sibling overlap as one adjacency line plus a short "Narrows" paragraph that (a) closes tsukuroi
Q12 with the systemd v262 user-manager default (T8), and (b) replaces the shared "band scanned first"
model with the single-pass maximum and a dated weight (T3, T4, T10, T11). It improves depth (an open
sibling question answered from primary bytes C1 already holds) and adjacency (the line names exact sibling
ranges, and tsukuroi's inbound-anchor ledger already tracks mori adjacency lines: tsukuroi
`adjacency-anchors-r19.md:171` row IN-076). No new SOURCES row is needed for sibling files: the
r12 entries' "Adjacent:" lines cite tsukuroi paths without rows (mori
`kernel-oom-line-attribution-r12.md:8`, `kill-classes-by-message-id-r12.md:8`), and memory-pressure-r25
is already mori S125. No harm to freshness, privacy or retention: nothing dated is restated as current,
and only classes, bands and counts appear.

Ready-to-paste adjacency line (line 8 convention of the r12 entries):

```markdown
Adjacent: `tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md:60-69,104-119` (at tsukuroi 157ee255, unchanged at 420a1ae1) holds the only kernel-chosen victim in retention (event A, 2026-10-13, a python-class process at `oom_score_adj` +200) and `kill-event-deep-r8.md:138-152,260,295` the live 2026-10-14 bands with the +200 origin open as Q12; `memory-pressure-r25.md:318-327` (mori S125) shows a userspace kill moves no kernel counter. Both kill planes predate earlyoom on this host (installed 2026-10-20, `oom-event-plane.md:442-452`), so neither victim enters this entry's earlyoom-send share. This entry adds the selection mechanics and does not re-attribute either event. Cross-lane source ids are lane-qualified: tsukuroi S119 is `mm/oom_kill.c` (mori S003, same sha256 `452f1348…6b4e`) and tsukuroi S127 is not mori S127.
```

Ready-to-paste "Narrows" paragraph:

```markdown
**Narrows.** tsukuroi `kill-event-deep-r8.md:149-152,295` (Q12, "origin of the +200 band is [unknown]"): systemd v262 runs the user manager at `OOMScoreAdjust=100` (`user@.service`; systemd commit ce7de0ba) and, for an unprivileged manager, defaults its services to the manager's value plus 100 (`systemd-system.conf.xml:305-306`; commit d4a402e4), giving +200; scopes inherit it from the launching process. `oom-event-plane.md:116,349` and `kill-event-deep-r8.md:148,260` ("the +200 band is scanned first"): the kernel makes one pass and keeps the largest footprint + adj × totalpages/1000 (`mm/oom_kill.c:228-234,340`); on 2026-10-22 +200 equals about 12.1 GiB of footprint (totalpages 15,861,169), so a larger process at 0 can still be chosen over a smaller one at +200. `kill-event-deep-r8.md:142` quotes `systemd.exec` for the default; that text describes the system manager, not a user manager.
```

## Risks

- R1: the +200 explanation is a documented default plus a measured match, not a trace of the session
  launch chain; if the operator sets `DefaultOOMScoreAdjust=` in a user-manager config the mechanism
  changes. C1 should check presence only (never values) of a `DefaultOOMScoreAdjust` line in the
  user-manager config files before stating it as the cause on this host. Not checked by this seat.
- R2: the ≈12.10 GiB figure uses `MemTotal` as `totalram_pages()`; it drifts with any swap change (zram
  already left between 2026-10-14 and today, T11). Date it or state only the formula.
- R3: tsukuroi may later append a notice to lines 116/349; the adjacency line pins 157ee255 so it stays
  valid, but tsukuroi's anchor ledger may re-grade it.
- R4: privacy: the sibling lines carry pids, uids and unit names with a uid; the paste blocks above carry
  none. Keep it that way if editing them.

## Verification (for the L1; not run by this seat)

- `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff --quiet 157ee255 HEAD -- corpus/knowledge/oom-event-plane.md corpus/knowledge/kill-event-deep-r8.md && echo stable` — run here → `unchanged-at-HEAD`.
- `sed -n '303,307p' /fast/scratch/hyaku/mori-r27/SrcSystemdExecOomScoreAdjust/systemd-system.conf.xml` and `sed -n '1295,1300p' …/systemd.exec.xml` — run here; quotes above are verbatim.
- `sed -n '228,234p;340p;358,360p' /fast/scratch/hyaku/mori-r27/MoriR27.SrcKernelOomBadness/oom_kill.c` — run here.
- Unrun: the retention scan on the landed entry (`python3 -I -B tools/mori-retention-gate.py scan …` per contract, must stay ≤ 4); `count-c1.sh` at the landed tip.
