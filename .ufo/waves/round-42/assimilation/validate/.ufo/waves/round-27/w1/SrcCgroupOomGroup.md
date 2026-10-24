# Seat MoriR27.SrcCgroupOomGroup — C1 source scout (memory.oom.group)

Question: for the C1 frontier item "fleet attribution of an OOM victim", open the pinned Linux v7.2
`Documentation/admin-guide/cgroup-v2.rst`, locate `memory.oom.group` and the `memory.events`
`oom_group_kill` entry, and say whether that file is a new SOURCES row or an anchor on an existing row.

**Answer in one line: neither a new row nor an S002 anchor — the exact fetched artifact is already row
S092 (same URL, same tag, same sha256), so the anchors belong on S092; S002 is a different artifact
(the unpinned docs.kernel.org HTML render) and receives nothing.** This item therefore contributes zero
S127+ rows to C1.

## Gate block

- URL: https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst
- Access: 2026-10-22T15:46:30Z, `curl -sS`, HTTP 200, 133,236 bytes, 3524 lines (command output:
  `200 133236`, `sha256sum` below).
- sha256 of fetched bytes: `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad`
- Local copy for these line numbers: `/fast/scratch/hyaku/mori-r27/MoriR27.SrcCgroupOomGroup/cgroup-v2.rst`

Verbatim quotes (all line numbers are in the fetched file; each <=25 words):

1. `:1454-1455` — "Determines whether the cgroup should be treated as an indivisible workload by the OOM
   killer." (15 words)
2. `:1457-1458` — "(if the memory cgroup is not a leaf cgroup) are killed together or not at all." (16 words)
3. `:1461-1462` — "Tasks with the OOM protection (oom_score_adj set to -1000) are treated as an exception and
   are never killed." (18 words)
4. `:1464-1465` — "If the OOM killer is invoked in a cgroup, it's not going to kill any tasks outside of this
   cgroup" (20 words)
5. `:1510-1511` — "oom_group_kill" / "The number of times a group OOM has occurred." (9 words in the
   description line; the field name is on `:1510`, the sentence on `:1511`)

## What the pinned file grounds (located, not inferred)

- `memory.oom.group` is a read-write single-value file on non-root cgroups, default `"0"`
  (`:1450-1452`; the default sentence is `:1452`, no quote slot used above).
- Set, it makes the cgroup an indivisible OOM-killer workload (quote 1), and every task of the cgroup and
  of its descendants — explicitly including a non-leaf memory cgroup — dies together or not at all
  (quote 2, `:1456-1458`); the stated purpose is to avoid partial kills for workload integrity (`:1458-1459`).
- `oom_score_adj` `-1000` tasks are an exception inside that group kill and "are never killed" (quote 3).
  This is the only mention of `oom_score_adj` or `oom_score` in the whole file (counts: `oom_score` 1,
  `oom_score_adj` 1, both `:1461`).
- An OOM kill invoked in a cgroup never kills tasks outside it, "regardless memory.oom.group values of
  ancestor cgroups" (quote 4 + `:1466`).
- `memory.events` gains `oom_group_kill`, counting group OOM occurrences (quote 5), sitting next to
  `oom_kill`, "The number of processes belonging to this cgroup killed by any kind of OOM killer."
  (`:1506-1508`).
- Hierarchical scope: "all fields in this file are hierarchical" (`:1474`) and `memory.events.local` is
  "Similar to memory.events but the fields in the file are local to the cgroup" (`:1517-1519`). That the
  `oom_group_kill` field also appears in `memory.events.local` follows from the "similar" sentence, not
  from a field list — [INFERENCE], and it agrees with the existing claim at
  `corpus/knowledge/journal-alarm-routing-r14.md:55-57` (systemd reads `memory.events.local`
  `oom_group_kill` when `memory.oom.group=1`).

Not in this file (0 hits each): `earlyoom` (0), `--prefer`/`--avoid`/`--ignore` (0). The doc never defines
how `oom_score` is computed, and gives no host values, no victim-selection ordering, no `--sort-by-rss`
equivalent. Those belong to `mm/oom_kill.c` (S003) and the earlyoom rows (S114-S120).

## Row verdict

Fetched artifact identity:

- S092 (`corpus/SOURCES.md:98`) is `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst`,
  `docs`, tier A, status `mined`, anchor cell records `tag v7.2; sha256 a9433bb0e16a67f0` — the same 64-bit
  prefix as my full `a9433bb0e16a67f0…b7ad`, i.e. the same bytes.
- Cross-check on line numbering: every one of S092's five anchored lines reproduces exactly in my fetch —
  `cgroup.pressure` `:1066`, `irq.pressure` `:1083`, `cpu.pressure` `:1215`, `memory.pressure` `:1911`,
  `io.pressure` `:2171` (grep -n output). So S092 and my file are one artifact, and my new line numbers are
  directly comparable with S092's cell.
- S092's used-by already carries `corpus/knowledge/system-pressure-r24.md, corpus/lessons/round-24.md`, so a
  new entry citing it is an append to that cell, matching the round-15 used-by append precedent
  (`corpus/SOURCES.md:159`).

Why not S002: S002 (`corpus/SOURCES.md:8`) is the docs.kernel.org HTML rendering of the same document,
unpinned ("current page opened 2026-10-19"), and its anchors (`memory.events:1448-1509`,
`memory.peak:1418-1426`) are *display* line numbers of that HTML. Mixing raw-ReST line numbers into S002
would put two numbering systems in one cell; the registry already records that rendered-page numbers do not
reproduce (`corpus/SOURCES.md:159`: "Re-deriving the S014/S015 numeric anchors from the rendered systemd 262
pages did not reproduce the pinned line numbers"). S002 also declares a narrower scope (events/peak,
hierarchical vs local) and its anchor does not mention `memory.oom.group`. So S002 stays untouched.

Consequence for the C1 counter (material): `count-c1.sh` counts only ids numerically `>= 127` whose row is
`mined` and names the entry in used-by. An anchor append on S092 is invisible to it. **This frontier item
can supply at most 0 of C1's three new rows**; the knowledge entry may legitimately cite S092 (anchored,
pinned, mined) and S002, but the three S127+ rows must come from other wave-1 sources. The contract's own
rule ("re-opening a file with an existing row adds an anchor to that row, not a new row") and S092's
byte-identical sha256 make any new row for this URL a duplicate artifact.

## Ready-to-paste: S092 replacement line (anchor + scope + used-by extension)

Replace line 98 of `corpus/SOURCES.md` with this single line (cells unchanged except `scope`, `anchor`,
`used-by`; `teaches` kept byte-identical unless the L1 elects the optional sentence below):

```
| S092 | Linux cgroup v2 pressure files and the cgroup.pressure switch v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst | docs | A | the cgroup v2 interface files that expose per-controller pressure (cpu, io, irq, memory) and the cgroup.pressure switch that enables or disables PSI accounting for one cgroup; interface file names, documented access modes and switch semantics only, not PSI counter semantics and not host availability; plus the memory.oom.group switch and the memory.events oom_group_kill entry: a rw single value defaulting to "0", the indivisible-workload rule, the oom_score_adj -1000 exception, no kill outside the invoked cgroup, and a group-OOM count as documented interface only, not the victim-scoring algorithm and not host values | cgroup.pressure:1066-1081; irq.pressure:1083-1087; cpu.pressure:1215-1221; memory.pressure:1911-1915; io.pressure:2171-2175; memory.oom.group:1450-1466 (rw single value, default "0":1452; indivisible workload:1454-1455; descendants killed together incl. non-leaf:1456-1458; oom_score_adj -1000 exception:1461-1462; no kill outside the invoked cgroup:1464-1466); memory.events oom_group_kill:1510-1511 beside oom_kill:1506-1508; hierarchical note:1474; memory.events.local similarity:1517-1519; tag v7.2; HTTP 200, 2026-10-22T15:46:30Z, 133,236 B, sha256 a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad | Each controller carries its own pressure file, and the cgroup.pressure switch is a per-cgroup 0/1 switch, not a hierarchical one, so disabling PSI accounting in a cgroup leaves its descendants unaffected. | mined | 2026-10-22 | on-release | corpus/knowledge/system-pressure-r24.md, corpus/lessons/round-24.md, corpus/knowledge/oom-victim-selection-r27.md |
```

Optional `teaches` addition (only if the L1 wants the row to state the OOM fact it now anchors): append
"`memory.oom.group` makes a cgroup an indivisible OOM unit whose tasks die together except those with
`oom_score_adj` -1000, and `memory.events.oom_group_kill` counts group OOMs."

## Alternative, only if the L1 rules that a NEW row is required

Mechanically this would satisfy `count-c1.sh` (id >= 127, `mined`, entry in used-by) while pointing at the
same bytes as S092. I do not recommend it: it duplicates an existing artifact (same URL, same tag, same
sha256, same line numbers) and contradicts the contract's re-open rule, so the L1 would have to record the
duplicate-artifact decision explicitly in `corpus/lessons/round-27.md`. Shape is exact if chosen:

```
| S??? | Linux cgroup v2 memory.oom.group and the oom_group_kill event entry at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst | docs | A | the memory.oom.group switch and the memory.events oom_group_kill entry as the kernel documents them: rw single value default "0", the indivisible-workload group-kill rule over a cgroup and its descendants, the oom_score_adj -1000 exception, no kill outside the invoked cgroup regardless of ancestor values, and a group-OOM counter; documented interface only, not the victim-scoring algorithm, not earlyoom policy, not host values — the same bytes as S092 | memory.oom.group:1450-1466 (default "0":1452; indivisible workload:1454-1455; descendants killed together incl. non-leaf:1456-1458; oom_score_adj -1000 exception:1461-1462; no kill outside the invoked cgroup:1464-1466); memory.events oom_group_kill:1510-1511 beside oom_kill:1506-1508; tag v7.2; HTTP 200, 2026-10-22T15:46:30Z, 133,236 B, sha256 a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad | The memory.oom.group switch makes a cgroup an indivisible OOM unit whose tasks die together except those with oom_score_adj -1000, and memory.events.oom_group_kill counts group OOMs separately from the per-process oom_kill count. | mined | 2026-10-22 | on-release | corpus/knowledge/oom-victim-selection-r27.md |
```

## Facts the entry may take from this source (with the limits)

Open, safe to cite: default `"0"` and read-write on non-root cgroups; group-kill semantics and the non-leaf
descendant clause; the `-1000` exception wording; the no-kill-outside rule; the `oom_group_kill` meaning and
its separation from `oom_kill`; the hierarchical/local relationship.

Do not take: any statement that `-1000` protects a task from the *global* (non-group) kernel OOM killer — the
sentence sits inside the `memory.oom.group` paragraph and the doc does not restate it elsewhere (0 other
hits for `oom_score_adj`); any claim that `memory.oom.group` gates earlyoom (0 hits for `earlyoom`,
`--prefer`, `--avoid`, `--ignore`); any host value of `memory.oom.group` — that is a host capture, not this
doc.

## Unresolved / handoff

- Whether the fleet's units run with `memory.oom.group=1` is a host fact; not this seat's question and not
  answerable from this file.
- Whether `oom_group_kill` is present in `memory.events.local` on this kernel is [INFERENCE] from `:1517-1519`;
  a `/sys/fs/cgroup/.../memory.events.local` read in the C1 executor seat would settle it.
- The victim-scoring side (`oom_score`, badness, `oom_score_adj` arithmetic) and earlyoom's
  `--prefer`/`--avoid`/`--ignore`/`--sort-by-rss` are outside this artifact; other wave-1 seats own them.

## Tooling

No installs or upgrades: `curl`, `sha256sum`, `grep`, `python3` (word counts) were already present. No
pacman transaction attempted. No subagents, no background jobs. Read-only commands only; no signals, no
writes outside this report and my scratch dir.

Report: .ufo/waves/round-27/w1/SrcCgroupOomGroup.md
