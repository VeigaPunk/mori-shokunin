# Mo52CritC2Coverage — attack on the C2 expansion claim (overcommit accounting as new ground for mori)

Seat: critic (leaf). Assignment: attack the expansion claim behind C2 — is overcommit
accounting really new ground for mori? Verdict with pointers.
Scratch: `/fast/scratch/hyaku/mori-r52/Mo52CritC2Coverage/` (created, removed on exit).
No tool installs (nothing was installed; no RULES.md action needed).

## Verdict

The C2 predicate and its sweep are correctly scoped as designed, but the claim's
narrative wording "are undefined in the lane" (contract line 55-56) overstates what
was measured. At the freeze commit `4f266ef2`, the lane already carried the defining
v7.2 bytes of both lines — the `CommitLimit` paragraph with its formula and the
mode-2 enforcement statement, plus the `Committed_AS` paragraph — inside
`corpus/evidence/sources-r51/proc.rst.v7.2:1220-1248`, and the printer lines in
`corpus/evidence/sources-r51/meminfo.c.v7.2:125-126`. Those copies are registered
sources S492/S494 of the round-51 MemAvailable entry. What was absent at freeze was
any `corpus/knowledge` entry that mines those bytes; the sweep (per
`evidence/sweep-overcommit.txt`) covered only `corpus/SOURCES.md`, `corpus/knowledge`,
`SKILL.md` and `merge/mori/` — not `corpus/evidence/`.

So C2 as a depth claim (new knowledge entry on an unwritten-up runway line) is
defensible, but the expansion text "undefined in the lane" is wrong in the literal
sense and should be corrected to the sweep scope, with a pointer to the round-51
copies. Province: yes — the two meminfo lines are resource-runway read probes, which
is mori's Core (`PROVINCE.md:10`); no sibling defines them; tsukuroi records only the
host's *value* (`overcommit_memory=0`) and a different btrfs-overcommit meaning.

## Evidence

### 1. Commit identity (exit 0)

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse --short 8524904adb25e44f24d9f25aac7eae909625c18c
# 8524904a
git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse --short 4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d
# 4f266ef2
```

### 2. The sweep receipt (read; file `evidence/sweep-overcommit.txt`)

Header line: `# sweep at 4f266ef2 over corpus/SOURCES.md corpus/knowledge SKILL.md (git grep -l -F, files per term)`.
All fourteen terms (CommitLimit, Committed_AS, overcommit_memory, overcommit_ratio,
overcommit_kbytes, vm_commit_limit, __vm_enough_memory, vm_committed_as,
user_reserve_kbytes, admin_reserve_kbytes, MAP_NORESERVE, OVERCOMMIT_NEVER,
overcommit-accounting) count 0 files over those paths; `merge/mori/` 0.

### 3. Whole-lane grep at the data commit

Command:
```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n -i -E 'overcommit|commitlimit|committed_as|enomem' 8524904adb25e44f24d9f25aac7eae909625c18c -- ':!*.png' ':!*.jpg' ':!*.gif' ':!*.pdf'
```
Exit 0. Semantic (theme-defining) hits, not generic `-ENOMEM` kernel error codes
(which occur only inside raw kernel source copies, e.g. round-23 `evidence/sources/S078…`):

| file at data commit | lines | content |
|---|---|---|
| `corpus/evidence/sources-r51/proc.rst.v7.2` | 1092-1093, 1220-1237, 1238-1248 | sample output; `CommitLimit` definition incl. formula `(total RAM pages - huge TLB pages) * overcommit_ratio / 100 + total swap pages`; "if strict overcommit accounting is enabled (mode 2 in 'vm.overcommit_memory')"; `Committed_AS` definition: "allocations which would exceed the CommitLimit (detailed above) will not be permitted" |
| `corpus/evidence/sources-r51/meminfo.c.v7.2` | 125-126 | `show_val_kb(m, "CommitLimit:    ", vm_commit_limit());` / `show_val_kb(m, "Committed_AS:   ", committed);` |
| `corpus/evidence/recheck-r32/S001.src`, `S002.src` | 205, 305, 1246, 1265, 3247, 3281 | "excessive overcommit", cgroup `memory.min`/`memory.low` overcommitment, userspace overcommit discussion (cgroup protection domain) |
| `corpus/evidence/sources-r50/cgroup-v2.7.2.html` | 297, 1215, 1234, 3190, 3224 | same cgroup overcommitment text |
| `.ufo/waves/round-23/evidence/sources/S082-Documentation_filesystems_proc.rst` | 1092-1093, 1220-1248 | older copy of the same proc.rst definition block (round-23 evidence) |
| `.ufo/waves/round-27/w1/HostUnitOomAdjust.md` | 108, 114 | read `/proc/sys/vm/overcommit_memory`, reported value `0` (heuristic overcommit) |
| `.ufo/waves/round-27/falsify/QHostLike.md`, `scan.json` | 182, 933 | probe list includes `/proc/sys/vm/overcommit_memory` |
| `.ufo/waves/round-24/w1/SrcKconfig.md` | 71 | quoted Kconfig description "Collect metrics that indicate how overcommitted the CPU, memory, …" |
| `.ufo/waves/round-34/wa/CritResidualA.md` | 53 | `/proc/sys/vm/overcommit_memory` read noted as emitted by a trace |
| `corpus/knowledge/overcommit-commit-limit-r52.md` | all | the new C2 entry itself (present only at data commit, not at freeze) |

### 4. Freeze-commit state (the swept "before" world)

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n -i -E 'commitlimit|committed_as|overcommit' 4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d -- corpus/ SKILL.md
```
Exit 0. Hits (all under `corpus/evidence/`, none under `corpus/knowledge/` or
`SKILL.md`):
- `corpus/evidence/sources-r51/proc.rst.v7.2:1092-1093,1220-1248`
- `corpus/evidence/sources-r51/meminfo.c.v7.2:125-126`
- `corpus/evidence/recheck-r32/S001.src:205`, `S002.src:305,1246,1265,3247,3281`
- `corpus/evidence/sources-r50/cgroup-v2.7.2.html:297,1215,1234,3190,3224`

This confirms the defining bytes existed at freeze, before the C2 data landed.

### 5. Registry context (SOURCES.md at data commit)

- S492 (round-51): proc.rst at v7.2, scope = meminfo field definitions
  (MemFree, MemAvailable, Cached, Shmem, KReclaimable, SReclaimable), anchors
  1124-1135, 1138-1141, 1192-1201 — the `CommitLimit`/`Committed_AS` paragraphs at
  1220-1248 were explicitly out of that row's scope.
- S494 (round-51): fs/proc/meminfo.c at v7.2, anchors include 105; the new entry
  itself cites `meminfo.c.v7.2:125-126` for the two printed lines.
- S497-S501 (new, C2): overcommit-accounting.rst, vm.rst, mm/util.c, mman.h,
  mm/mmap.c, all v7.2, opened 2026-10-26.

The entry is honest about the printer (`meminfo.c` S494) but does not note that the
S492 copy of the same `proc.rst` already contained the `CommitLimit`/`Committed_AS`
definition paragraphs (1220-1248) that this entry restates.

### 6. Sibling lanes sweep (read-only, corpus/ + SKILL.md, .scratch/.ufo excluded)

Command:
```
cd /home/vgpnk/Projects/shokunin; for l in *-shokunin; do [ -d "$l" ] || continue; hit=$(grep -rilE 'overcommit|commitlimit|committed_as' "$l/corpus" "$l/SKILL.md" 2>/dev/null | grep -vE '/(\.scratch|\.ufo)/' | wc -l); echo "== $l files_with_hits=$hit"; …; done
```
Exit 0. Results: 17 lanes 0 hits. Two lanes with hits:

- `kaidoku-shokunin/corpus/evidence/round-34/elf/e12.bin` (1) — an ELF fixture
  (`file`: ELF 64-bit LSB pie, static-pie, stripped) whose embedded string includes
  `/proc/sys/vm/overcommit_memory` (`grep -aoiE '.{0,24}overcommit.{0,24}'` →
  `eap->size)/proc/sys/vm/overcommit_memorydouble free or`). Probe-list string in a
  binary fixture; not knowledge, not a definition.
- `tsukuroi-shokunin` (4):
  - `corpus/knowledge/kill-event-deep-r8.md:262` — diagnostic row: `overcommit_memory`=0 (value only)
  - `corpus/knowledge/oom-event-plane.md:351` — same value row
  - `corpus/knowledge/btrfs-space-r30.md:18` — btrfs metadata reservations "may overcommit" vs `ENOSPC` (different meaning)
  - `corpus/SOURCES.md:165` (S159) — btrfs space-info.c overcommit/reservation scope

No sibling defines `CommitLimit`/`Committed_AS` or the mode-2 enforcement semantics.

### 7. Province check

- mori `PROVINCE.md:10` (Core): "resource runway (disk on the fleet root and
  `/tmp`, memory pressure)" — the two meminfo lines are memory-resource runway read
  probes; detection and report only (`PROVINCE.md:16`).
- tsukuroi `PROVINCE.md:30-33`: "Host memory and kill-event measurements support OS
  triage; … fleet correlation belongs to mori" — explicit hand-off of memory-signal
  correlation to mori. tsukuroi owns OS/package/systemd/boot/driver diagnosis and
  config, not meminfo semantics read.
- The entry's own boundary (overcommit-commit-limit-r52.md, "Reading rules"): mori
  reads `/proc/sys/vm/overcommit_memory` + meminfo lines and never writes a `vm.*`
  sysctl; choosing/changing the mode is operator-owned; OS-state triage is
  tsukuroi's — consistent with the province split above.

## Findings

- **MED — claim wording overstates the measured scope.** Contract line 55-56 says
  `CommitLimit`/`Committed_AS` "are undefined in the lane"; the sweep only covered
  `corpus/SOURCES.md`, `corpus/knowledge`, `SKILL.md`, `merge/mori/`. At freeze the
  lane already contained the defining v7.2 bytes at
  `corpus/evidence/sources-r51/proc.rst.v7.2:1220-1248` and
  `corpus/evidence/sources-r51/meminfo.c.v7.2:125-126` (registered S492/S494),
  un-mined. The true gap is "no corpus/knowledge entry defines them", not "undefined
  in the lane". Correct the wording (data is correctable by the L1); the frozen
  counter, predicate and sweep scope stay untouched. Also record this as a named
  limit / round-53 routed item: the sweep does not assert absence of the bytes in
  `corpus/evidence/`.
- **LOW — entry coverage-map label "new ground" has the same nuance.** The entry's
  `coverage-map:` line (overcommit-commit-limit-r52.md, header) rests on the sweep;
  recommend qualifying as "new knowledge entry; defining bytes present since round 51
  in the S492/S494 copies".
- **LOW — no sibling overlap; province confirmed.** tsukuroi holds only the host's
  sysctl *value* (kill-event-deep-r8.md:262, oom-event-plane.md:351) and a btrfs
  reservation meaning (btrfs-space-r30.md:18); kaidoku's hit is a probe-list string
  inside an ELF fixture. Resource-runway read probes are mori's Core
  (`PROVINCE.md:10`); sysctl change/OS triage remain operator/tsukuroi.
- **LOW — prior host reads of the sysctl existed in wave artifacts** (round-27
  `HostUnitOomAdjust.md:114`, `QHostLike.md:182`; round-34 `wa/CritResidualA.md:53`;
  round-24 `SrcKconfig.md:71`) — value reads, no semantics; supports the conclusion
  that the gap was distillation, not byte-absence.

## UNVERIFIED

None material: every path cited above was read at the named commit or in the working
tree. The frozen counters were not re-run (not this seat's action); sweep and
reports stand as read.
