# Mo50bScribeWhatChanges — `## What this changes for mori` for `oom-memcg-stat-r50.md`

Seat: scribe, mori round 50 attempt 2, wave a2w1. Skill read: `skill://godspeed` (axes: link
correctness, line-anchor accuracy, contradiction surfacing; iterated by opening all six entries and
the three frozen sources in parallel batches). No tool installs, no pacman. Draft only — I wrote no
lane file except this report.

Read at: lane tip `4548a34dc8b4072abaa4335c1f54a9efcfcc314a` (`git rev-parse HEAD`), data commit
`487941b9395e89678af0053cc443cdb49cdee6e3`, contract `.ufo/waves/round-50/contract.md`.

## Behavior

- Opened the new entry (`corpus/knowledge/oom-memcg-stat-r50.md`, 83 lines) and each of the five
  entries named in the ticket, whole: `kernel-oom-line-attribution-r12.md` (51 lines),
  `oom-tracepoints-r47.md` (80), `oom-victim-context-r41.md` (103),
  `oom-kill-counter-kernel-only-r12.md` (33), `census-cgroup-levels-r45.md` (66). `ls
  corpus/knowledge/ | grep -E 'oom|census-cgroup'` also lists `oom-evidence-loss-r38.md`,
  `oom-victim-selection-r27.md`, `earlyoom-invocation-scope-r30.md`,
  `userspace-oom-killers-r12.md`, `userspace-oom-killers-r26.md`; the ticket names five and I linked
  those five, so the other four are out-of-scope for this section (see Out of scope).
- Checked every claim of the new entry that my section relies on against the committed v7.2 copies
  under `corpus/evidence/sources-r50/` (read-only). All held; three conditioning facts the entry
  does not state are in Findings.
- Drafted the section below (8 lines inside the fence, fenced). Placement recommendation: insert
  between `## Limits` and `## Boundaries` (before line 79), matching `oom-tracepoints-r47.md:53` which puts
  its section before `## Boundaries`.

## Draft — `## What this changes for mori` (fenced, 8 lines)

```markdown
## What this changes for mori

- `kernel-oom-line-attribution-r12.md:6` names the summary fields (task, PID, UID, "when available" `task_memcg`); this entry adds the label before them — `oom_memcg=<path>`, else the literal `global_oom` (`:33`) — so the summary's first token states whether the kill had a charged scope at all.
- `oom-tracepoints-r47.md:56-58` holds that no `oom` trace event carries a cgroup path; the only record here that does is this printk pair (`oom_memcg=` / `task_memcg=`, `:33-34`), so a `mark_victim`-keyed tracer must be joined to the printk on pid and cannot take scope from tracefs. [INFERENCE: no row states the join]
- `oom-victim-context-r41.md:61-64` asks attribution to carry "which cgroup the killed process belonged to"; this entry names that token — `task_memcg`, beside `oom_memcg` — plus the source NOTE that the two differ when hierarchy is enabled (`:58`).
- `oom-victim-context-r41.md:12` frames selection as "cgroup-scoped"; this entry narrows that to a memcg OOM: a global OOM prints `global_oom` (`:33`) and `__show_mem` in place of the block (`:38`), so its burst names no scope.
- `oom-kill-counter-kernel-only-r12.md:12,27` labels the counter kernel-OOM-only because the docs phrase is "broader than the increment site"; this entry gives that same sentence the opposite reading (`:27`, "any kind of OOM killer") — see Findings. The increment at `__oom_kill_process` is unconditional, which is the ground the conclusion needs.
- `census-cgroup-levels-r45.md:48` holds that a line number travels with its copy and digest; this entry honours that (committed v7.2 copies, no live-render line numbers) and touches no census surface — the census reads `memory.events`/`memory.current` only (`tools/mori-census.sh:304-305`), so `oom_kill` stays a process count, never one of these byte amounts.
```

Line anchors used in the draft are the new entry's own line numbers at `487941b9` (`:33` = the
`global_oom` claim row, `:34` = the `task_memcg` row, `:38` = the `__show_mem` row, `:58` = the
hierarchy NOTE bullet, `:27` = the `oom_kill` claim row).

## Per-link evidence (what changed relative to each entry, and the line relied on)

1. **`kernel-oom-line-attribution-r12.md`** — line 6: "the summary includes task, PID, UID and
   (when available) `task_memcg`". It names the fields but not the token that opens them. New
   entry line 33: `When no cgroup is named the OOM context prints global_oom instead of a cgroup
   path`, quote `if (memcg) { pr_cont(",oom_memcg="); pr_cont_cgroup_path(memcg->css.cgroup); }
   else pr_cont(",global_oom");` — verified in `memcontrol.c.v7.2:1774-1778`. **Adds** the
   `oom_memcg=`/`global_oom` label (r12:12 says `memcontrol.c:1820–1826` appends "`oom_memcg=` and
   `task_memcg=`", so the label existed in r12's evidence but not in its claim sentence; the new
   entry states it as a claim and grounds it in S490).
2. **`oom-tracepoints-r47.md`** — lines 56-58: "No event in the set carries a cgroup path, a memcg
   name, or the task that triggered the allocation failure". The new entry's `oom_memcg=`/`task_memcg=`
   printk is the surface that does carry a path (new entry 33-34; `memcontrol.c.v7.2:1774-1781`).
   **Adds** the complementary record, so the tracer/printk division of labour is now sourced on both
   sides. The join sentence is mine → marked `[INFERENCE]` in the draft. Cross-check I did: the
   `mark_victim` field list (r47:39) is pid, comm, total_vm, anon_rss, file_rss, shmem_rss, uid,
   pgtables, oom_score_adj — the same quantities as the new entry's `Killed process` row (new entry
   36), so a pid-keyed join is possible; r47 states no pid join itself.
3. **`oom-victim-context-r41.md` probe shape** — lines 61-64: attribution "must carry … which
   cgroup the killed process belonged to, and which other cgroups were resident on the same kernel
   at that moment". The first half now has a kernel token: `task_memcg=` (new entry 34), and the
   new entry's line 58 records the NOTE at `memcontrol.c.v7.2:1765-1767` ("@memcg and @p's
   mem_cgroup can be different when hierarchy is enabled"). **Adds** the token name plus the
   charged-vs-victim distinction; the co-tenancy half stays r41's and is not supplied by the new
   entry.
4. **`oom-victim-context-r41.md` framing** — line 12: "**The kernel's OOM victim selection is
   cgroup-scoped but not container-scoped**". The new entry documents the non-cgroup case: a global
   OOM prints `global_oom` (new entry 33, `oom_kill.c`/`memcontrol.c.v7.2:1778`) and `__show_mem`
   instead of the block (new entry 38, `oom_kill.c.v7.2:466-468`). **Qualifies** r41's
   generalization → Finding F2.
5. **`oom-kill-counter-kernel-only-r12.md`** — lines 12 and 27. Line 12: "The documentation phrase
   is broader than the increment site: cite the implementation, not the description alone." Line 27:
   "label this counter as kernel-OOM-only". New entry line 27: "A rising oom_kill count does not
   prove a kernel memcg OOM, because the field counts kills by any kind of OOM killer." Same docs
   sentence, opposite reading → Finding F1. The conclusion survives on other ground that I verified
   in the copy: `__oom_kill_process` increments both counters unconditionally
   (`oom_kill.c.v7.2:935-936`), is called from `oom_kill_process` with the message chosen by
   `is_memcg_oom(oc)` at `:1169-1170` via `:1042`, so a *global* kill also raises the victim mm's
   `MEMCG_OOM_KILL`. [INFERENCE from those three call sites: the counter cannot separate global from
   memcg kills.]
6. **`census-cgroup-levels-r45.md`** — line 48: "a line number travels with its copy and digest".
   The new entry makes no line-number claim on the live docs page; every quote is located in the
   three frozen copies (counter `pins=ok`). **Confirms** the rule rather than changing r45's finding.
   I checked the census surface so the draft does not overstate: `grep -n 'memory\.stat' …` over
   `tools/mori-census.sh` → no hit; the census reads `memory.events` (304), `memory.current` (305),
   pressure and max (`:26`). So the new entry's byte/kB/page unit map does not restate or correct
   the `local_oom_kill` provenance defect.

## Gates

| gate | state at my read | evidence |
|---|---|---|
| Contract frozen bytes | both counters and controls are the committed freeze; I changed none | `contract.md` read; no write to `.ufo/waves/round-50/` except this report |
| C2 counter at the data commit | `C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok`, rc 0 | `python3 .ufo/waves/round-50/count-c2.py 487941b9395e89678af0053cc443cdb49cdee6e3` |
| Copy digests match the entry's `recheck:` | all three match | `sha256sum` → `2d716cb7…bf34 cgroup-v2.7.2.html`, `8a28e0bc…fd5e memcontrol.c.v7.2`, `452f1348…6b4e oom_kill.c.v7.2`, rc 0; entry line 8 lists the same three in the same order |
| Disk before run | `/fast/scratch/hyaku` 24 % used, 617.9 G free, rc 0 | `scripts/hyaku/disk-guard.sh status` |
| Fleet repo / jj / index | untouched; only read-only `git log`/`rev-parse` and `awk`/`grep`/`read` | no mutating git or jj command run |
| Host reads | no journal, no cgroup write, no `MESSAGE` grep; one network read of `docs.kernel.org` to compare the live docs sentence (Finding F1) | curl output below |

Live-docs check used in F1 (read-only, no temp file):

```
curl -fsSL --max-time 30 https://docs.kernel.org/admin-guide/cgroup-v2.html | (strip tags)
→ '… oom_killThe number of processes belonging to this cgroup killed by any kind of OOM killer. oom_group_killThe number of times a group OOM has occurred. …'
rc=0
```

The live render and the frozen v7.2 copy carry the identical sentence, so F1 is not version drift.

## Touched surfaces

- Written: `.ufo/waves/round-50/a2w1/Mo50bScribeWhatChanges.md` (this file) only.
- Read: `corpus/knowledge/oom-memcg-stat-r50.md` and the five linked entries;
  `corpus/evidence/sources-r50/{cgroup-v2.7.2.html,memcontrol.c.v7.2,oom_kill.c.v7.2}`;
  `tools/mori-census.sh`; `.ufo/waves/round-50/{contract.md,count-c2.py}`.
- Not edited: `SKILL.md`, `SHONEN.md`, `SCORECARD.md`, `LOG.md`, `corpus/`, `tools/`,
  `considerthese/`, counters, controls, other seats' reports.
- Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bScribeWhatChanges/` (`mkdir -p` + `TMPDIR` exported
  for the one curl); removed at the end (`rm -rf`; `ls` → empty, see Verification).

## Verification

```
$ git rev-parse HEAD                       → 4548a34dc8b4072abaa4335c1f54a9efcfcc314a   rc 0
$ sha256sum corpus/evidence/sources-r50/*  → the three digests above                    rc 0
$ python3 .ufo/waves/round-50/count-c2.py 487941b9…                                   rc 0, C2=met
$ grep -n 'Memory cgroup stats\|memory_stat_format\|mem_cgroup_print_oom' memcontrol.c.v7.2
  1751:memory_stat_format   1762/1770:mem_cgroup_print_oom_context   1787/1791:mem_cgroup_print_oom_meminfo
  1824:pr_info("Memory cgroup stats for ");   1828:memory_stat_format(memcg, &s);   4914:memory_stat_format(memcg, &s)
$ grep -n 'count_vm_event(OOM_KILL)\|memcg_memory_event_mm\|__ratelimit(&oom_rs)\|Killed process' oom_kill.c.v7.2
  935, 936, 1012, 1030, 1032, 945, 1169                                        rc 0
$ grep -n 'sysctl_oom_dump_tasks\|dump_tasks(oc)' oom_kill.c.v7.2   → 58, 473, 474  rc 0
$ grep -n 'memory\.stat' tools/mori-census.sh                       → no hit       rc 0
$ ls /fast/scratch/hyaku/mori-r50/Mo50bScribeWhatChanges  → ls: cannot access …: No such file or directory, rc 2 (after rm -rf)
```

Fence body line count check: `awk '/^```markdown$/{f=1;next} /^```$/{…} f{n++}'` over this report →
`BODY_LINES=8`.

Positive checks that are **not** findings (source says what the entry says): the stats block is
printed only on the memcg branch (`oom_kill.c.v7.2:466-468` + `memcontrol.c.v7.2:1824-1829`), so
"a stats block means the kill was charged to a scope" (entry line 15) is exact; the block uses
`KERN_INFO` and a `SEQ_BUF_SIZE` buffer under `oom_lock` with a warn-only overflow (entry 31, 73-74;
`memcontrol.c.v7.2:1793-1829`, `1751-1762`); `kernel`/`pagetables`/`per-cpu`/`vmalloc`/`slab` key
names exist separately in the docs copy (offsets 54178-56830); the rate-limit asymmetry is exact
(`dump_header`+`dump_oom_victim` inside `if (__ratelimit(&oom_rs))` at `:1030-1033`,
`__oom_kill_process` outside at `:1042`); the `oom.group` message string matches
(`memcontrol.c.v7.2:1996-1998`); `Tasks state (memory values in pages)` is at `oom_kill.c.v7.2:424`.

## Out of scope

- No edit to the entry (L1 integrates), no counter/predicate change, no re-scoring.
- Four further knowledge entries on the same subject were not linked because the ticket names five:
  `oom-victim-selection-r27.md`, `oom-evidence-loss-r38.md`, `userspace-oom-killers-r12.md`,
  `userspace-oom-killers-r26.md`, `earlyoom-invocation-scope-r30.md`. The first two are the likeliest
  additional links (victim choice, and journal loss which would eat the block this entry describes);
  I did not read them and make no claim about them.
- No host verification of any block; the entry's own limit (no `MESSAGE` read) stands.
- I did not judge C1/C2 or the wave; I am a dispatched seat, not an independent judge.

## Findings

**F1 — HIGH — `corpus/knowledge/oom-memcg-stat-r50.md:27` (against
`corpus/knowledge/oom-kill-counter-kernel-only-r12.md:12,27`).** The two held entries read the same
docs sentence in opposite directions.
- New entry line 27: `A rising oom_kill count does not prove a kernel memcg OOM, because the field
  counts kills by any kind of OOM killer.` (quote: `The number of processes belonging to this cgroup
  killed by any kind of OOM killer.`)
- Held entry line 12: `S002, memory.events:1448–1458,1491–1494, defines the field as “The number of
  processes belonging to this cgroup killed by any kind of OOM killer”; … The documentation phrase is
  broader than the increment site: cite the implementation, not the description alone.` Line 27 of
  the same file: `label this counter as kernel-OOM-only`.
- Consequence if both stand: the new entry tells a reader the field counts userspace-killer kills
  too, while the held entry (which governs `SKILL.md:17`/`:28` guidance) tells a reader it does not.
  The live docs render carries the identical sentence (checked 2026-10-26), so this is not version
  drift.
- Correction available to the L1 without touching any counter: keep the conclusion, replace the
  reason with the increment site I verified — `memcg_memory_event_mm(mm, MEMCG_OOM_KILL)` is
  unconditional inside `__oom_kill_process` (`oom_kill.c.v7.2:935-936`), which is called with the
  message already chosen by `is_memcg_oom(oc)` (`:1169-1170`, `:1042`), and the docs sentence is
  about *processes belonging to this cgroup*, not about distinguishing memcg from global kills.

**F2 — LOW — `corpus/knowledge/oom-victim-context-r41.md:12` (against
`corpus/knowledge/oom-memcg-stat-r50.md:33,38`).** r41 opens with "**The kernel's OOM victim
selection is cgroup-scoped but not container-scoped**". The new entry documents a kernel OOM path
with no cgroup scope at all: `else pr_cont(",global_oom")` (`memcontrol.c.v7.2:1778`, new entry 33)
and `__show_mem(...)` in place of the memcg block (`oom_kill.c.v7.2:466-468`, new entry 38). Read as
written, r41's sentence over-generalizes; the label applies to a memcg OOM only. Severity LOW because
r41's operative claim is the container half, which the new entry does not touch.

**F3 — LOW — `corpus/knowledge/oom-memcg-stat-r50.md:21`.** The claim cell reads "Every memory amount
*the block* prints is a byte count", but the same burst's usage and swap lines print kB (the entry's
own rows 28 and 30, and Reading rules 46-47). The docs sentence quoted at row 21 stands under "Memory
Interface Files" and covers the `memory.*` files, not the printk burst; the bridge that makes it true
for the block is row 32 (same `memory_stat_format` formatter). Suggest "the stats block" in row 21 so
the two readings cannot be confused by a parser author.

**F4 — LOW — `corpus/knowledge/oom-memcg-stat-r50.md:42`.** "The Tasks state table prints total_vm
and rss in pages" omits two conditions: the table is printed only under `if (sysctl_oom_dump_tasks)`
(`oom_kill.c.v7.2:473-474`, default 1 at `:58`) and inside the rate-limited `dump_header` guard
(`:1030-1033`). A reader who expects the table whenever a victim line appears will mis-detect a
truncated burst.

**Checked, no contradiction found** (recorded so the L1 need not re-open): r47:56-58 is scoped to the
eight trace events and does not deny that the printk path carries cgroup paths; r45:48's
render-and-digest rule is satisfied by this entry's copy-located quotes; r12 line-attribution's
`task_memcg` "when available" is sharper in the new entry (`if (p)` at `memcontrol.c.v7.2:1779-1781`)
but not in conflict; `census-cgroup-levels-r45.md:11,38`'s `local_oom_kill` provenance defect is
untouched by the new entry, which reads no census file.
