# SrcCgroupV2 — round-24 C2 sourced frontier step (cgroup-v2 pressure files + cgroup.pressure switch)

Seat: `MoriR24.SrcCgroupV2` (scribe, read-only on the lane repo; draft only, no lane file edited).
Claim served: **C2 (coverage, frontier FR12)** — the C2 tool `tools/mori-pressure.py` reads system
`/proc/pressure/{cpu,memory,io,irq}`; the contract's "Sourced" clause requires this round's
`SOURCES.md` rows to include "cgroup-v2 pressure files". This seat owns exactly that source.
Status of this deliverable: **draft row + draft `## Gate` block only.** `corpus/SOURCES.md` was
not modified.

---

## 1. Provenance of the fetched bytes

| item | value |
|---|---|
| Primary URL opened | `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst` |
| Fetch method | `curl -sS -L --fail` into scratch (no clone, no mirror, no local git checkout) |
| HTTP result | `http_code=200`, `size_download=133236`, `time_total=0.567783` |
| UTC access time (fetch start) | **2026-10-22T08:15:00Z** |
| UTC access time (independent re-fetch, byte-identity check) | **2026-10-22T08:17:37Z** |
| SHA-256 of fetched bytes (full) | `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad` |
| SHA-256, first 16 hex (as required) | **`a9433bb0e16a67f0`** |
| Re-fetch SHA-256 | identical — `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad` (byte-identical across two fetches) |
| File length | 3524 lines (reStructuredText source of the `v7.2` tag) |
| Scratch location (outside the lane repo) | `/fast/scratch/hyaku/mori-r24-a2/src-cgroupv2/cgroup-v2.rst` (and `cgroup-v2.refetch.rst`, `psi.rst`) |
| Companion fetch (overlap check only, not this row's source) | `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst` — 2026-10-22T08:16Z, SHA-256 `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692`, 188 lines |
| installs | **none** — no pacman, uv, npx, cargo or `~/.local/bin` install was needed or performed; `curl` and `sha256sum` were already present |

Nothing was written inside the lane repo except this report. The lane's Git index, `jj` state and
working tree were not touched (read-only `git log` only).

---

## 2. Line anchors I actually verified (numbered dump of the fetched bytes)

Enclosing sections: `Core Interface Files` (heading line 855) holds `cgroup.pressure` and
`irq.pressure`; `CPU` (1094) holds `cpu.pressure`; `Memory` (1267) holds `memory.pressure`;
`IO` (1982) holds `io.pressure`.

Verified anchors (exact line numbers in the fetched file):

- **1066–1081 — `cgroup.pressure`** (Core Interface Files)
  - 1066 `  cgroup.pressure`
  - 1067 `	A read-write single value file that allowed values are "0" and "1".`
  - 1068 `	The default is "1".`
  - 1070 `	Writing "0" to the file will disable the cgroup PSI accounting.`
  - 1071 `	Writing "1" to the file will re-enable the cgroup PSI accounting.`
  - 1073–1075 `	This control attribute is not hierarchical, so disable or enable PSI` /
    `	accounting in a cgroup does not affect PSI accounting in descendants` /
    `	and doesn't need pass enablement via ancestors from root.`
  - 1077–1081 the stated reason for the switch: PSI accounts stalls per cgroup and aggregates at
    each hierarchy level, which may cost overhead in deep hierarchies, so the attribute can
    disable PSI accounting in non-leaf cgroups.
- **1083–1087 — `irq.pressure`** (Core Interface Files)
  - 1083 `  irq.pressure`
  - 1084 `	A read-write nested-keyed file.`
  - 1086–1087 `	Shows pressure stall information for IRQ/SOFTIRQ. See` /
    `	:ref:`Documentation/accounting/psi.rst <psi>` for details.`
- **1215–1221 — `cpu.pressure`** (CPU controller)
  - 1215 `  cpu.pressure`; 1216 `	A read-write nested-keyed file.`; 1218–1219 `Shows pressure stall
    information for CPU.` + psi.rst cross-reference; 1221 `	This file accounts for all the
    processes in the cgroup.`
- **1911–1915 — `memory.pressure`** (Memory controller)
  - 1911 `  memory.pressure`; 1912 `	A read-only nested-keyed file.`; 1914–1915 `Shows pressure
    stall information for memory.` + psi.rst cross-reference.
- **2171–2175 — `io.pressure`** (IO controller)
  - 2171 `  io.pressure`; 2172 `	A read-only nested-keyed file.`; 2174–2175 `Shows pressure stall
    information for IO.` + psi.rst cross-reference.

Note the documented asymmetry, which the row must carry and not smooth over: the v7.2 document
calls `cpu.pressure` and `irq.pressure` **read-write** nested-keyed files, and `memory.pressure`
and `io.pressure` **read-only** nested-keyed files. I report the document's wording; I do not
assert the kernel's runtime mode.

---

## 3. Draft `SOURCES.md` row (11 cells, exact registry shape)

Registry column order (read from `corpus/SOURCES.md:6`):
`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`

**This is a draft for the L1. It was NOT written to `corpus/SOURCES.md`.**

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0xx | Linux cgroup v2 pressure files and the cgroup.pressure switch v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst | docs | A | the cgroup v2 interface files that expose per-controller pressure (cpu, io, irq, memory) and the cgroup.pressure switch that enables or disables PSI accounting for one cgroup; interface file names, documented access modes and switch semantics only, not PSI counter semantics and not host availability | cgroup.pressure:1066-1081; irq.pressure:1083-1087; cpu.pressure:1215-1221; memory.pressure:1911-1915; io.pressure:2171-2175; tag v7.2; sha256 a9433bb0e16a67f0 | Each controller carries its own pressure file, and the cgroup.pressure switch is a per-cgroup 0/1 switch, not a hierarchical one, so disabling PSI accounting in a cgroup leaves its descendants unaffected. | mined | 2026-10-22 | on-release | corpus/knowledge/system-pressure-r24.md |

Notes for the L1 on this draft:

- **id**: left `S0xx` as instructed. Two sibling seats (`SrcKconfig.md:143`,
  `SrcPsiIrqCommit.md:159`) both provisionally claimed `S090`, so the L1 must resolve that
  collision and give this row the next free id (likely `S091`).
- **status `mined` / used-by**: the C2 contract says the knowledge entry
  `corpus/knowledge/system-pressure-r24.md` will cite this round's rows. **That note does not
  exist yet** (checked: `corpus/knowledge/` has no `system-pressure-r24.md`, and
  `corpus/lessons/` has no `round-24.md`). Following the round-23 rule ("they gain the final
  knowledge note only after that note exists and cites them"), `status: mined` and the named
  `used-by` are proposals; if the note is not landed, `used-by` should be `—` and `status`
  `queued`. This mirrors the sibling `SrcPsiIrqCommit` draft's caveat.
- **kind `docs`**: the registry uses `docs` for kernel documentation (S001, S002, S082, S083,
  S084, S077) and `code` for kernel source files (S003, S004, S085–S089). This URL is
  documentation source at the `v7.2` tag, so `docs` matches the existing convention.
- **scope cell** deliberately excludes PSI counter semantics (avg10/avg60/avg300/total,
  `some`/`full`), threshold semantics and any host-availability claim; see §5.

---

## 4. Draft `## Gate` block for the round-24 lesson

```markdown
## Gate

| Row | URL | Access date (UTC) | Verified line anchors | Located quote (≤25 words) | Decision / scope |
|---|---|---|---|---|---|
| S0xx | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst | 2026-10-22T08:15:00Z (re-fetch 2026-10-22T08:17:37Z, byte-identical; sha256 a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad, first16 a9433bb0e16a67f0) | cgroup.pressure:1066-1081; irq.pressure:1083-1087; cpu.pressure:1215-1221; memory.pressure:1911-1915; io.pressure:2171-2175 | 1073-1074: "This control attribute is not hierarchical, so disable or enable PSI accounting in a cgroup does not affect PSI accounting in descendants" (22 words) | Admit A for the cgroup pressure file set and the per-cgroup cgroup.pressure switch. Not a counter-semantics source, not a host-availability attestation, not a threshold source. |
```

Supporting quotes verified in the same file (each ≤25 words, exact):

- 1070–1071: `Writing "0" to the file will disable the cgroup PSI accounting.` / `Writing "1" to
  the file will re-enable the cgroup PSI accounting.`
- 1086–1087: `Shows pressure stall information for IRQ/SOFTIRQ. See`
- 1218–1219: `Shows pressure stall information for CPU. See`
- 1914–1915: `Shows pressure stall information for memory. See`
- 2174–2175: `Shows pressure stall information for IO. See`
- 1221: `This file accounts for all the processes in the cgroup.`

---

## 5. New row or supersession?

**New row. Not a supersession of S001 or S002, and not a duplicate of the sibling `S090` draft.**

Checked every row of `corpus/SOURCES.md` for the same URL or the same scope:

| existing row | URL | scope | relation to this draft |
|---|---|---|---|
| S001 | `https://docs.kernel.org/accounting/psi.html` | "Linux PSI counters, totals, thresholds and per-cgroup files"; anchor includes `Cgroup2 interface` | **Overlap, not supersession.** I opened the same document's `v7.2` source (`Documentation/accounting/psi.rst`, sha256 `11c6b7129103b4547`). Its Cgroup2 interface section (lines 181-185) names only `cpu.pressure, memory.pressure, and io.pressure` per cgroupfs subdirectory, states that the format is the same as `/proc/pressure/`, and says nothing about `irq.pressure` and nothing about the `cgroup.pressure` switch. This draft therefore adds content S001 does not carry; it does not contradict S001. |
| S002 | `https://docs.kernel.org/admin-guide/cgroup-v2.html` | "cgroup-v2 memory events, memory.peak and local versus hierarchical scope"; anchors `memory.events:1448-1509`, `memory.peak:1418-1426` | **Same document, different scope and different edition.** S002 is the *rendered, current* docs.kernel.org page scoped to memory events; this draft is the *`v7.2`-pinned .rst source* scoped to the pressure files and the accounting switch. Different URL, disjoint scope. S002's cells are not rewritten by this row. |
| sibling draft `S090` (`SrcPsiIrqCommit`) | `https://github.com/torvalds/linux/commit/52b1364ba0b1...` | upstream introduction of the IRQ resource: `/proc/pressure/irq`, cgroup `irq.pressure`, the full-only rule; `kind: code` | **Complementary.** That row is code-level origin evidence for the IRQ resource; this row is documentation evidence for which pressure files the cgroup v2 interface defines and how `cgroup.pressure` works. The only shared token is the file name `irq.pressure`. Flagged for `MoriR24.ConnectSourceDuplicates`; I see no duplicate anchor. |
| S010 | `https://systemd.io/PRESSURE/` | systemd pressure-watch protocol | unrelated scope |
| S033 | `https://docs.kernel.org/admin-guide/iostats.html` | `/proc/diskstats` sector counters | unrelated scope (I/O counters, not I/O pressure) |

No existing row uses the `v7.2` `Documentation/admin-guide/cgroup-v2.rst` URL. The registry ends at
`S089`, and the `v7.2` `.rst` documentation rows already present (S077, S082, S083, S084) use the
same `raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/...` shape and record
`sha256 <first16>` in the anchor cell — the draft above follows that pattern.

---

## 6. What the source supports, and what it does not

**Narrow claim the source supports.** In Linux `v7.2`, the cgroup v2 interface defines one
pressure file per controller — `cpu.pressure`, `io.pressure`, `irq.pressure`, `memory.pressure` —
each described as a nested-keyed file carrying that resource's stall information, with the
document calling `cpu.pressure` and `irq.pressure` read-write and `memory.pressure` and
`io.pressure` read-only. A separate core interface file, `cgroup.pressure`, is a single-value
read-write file whose only allowed values are `0` and `1`, default `1`; writing `0` disables PSI
accounting for that cgroup and writing `1` re-enables it, and the attribute is **not
hierarchical** — disabling or enabling it in one cgroup does not affect descendants and does not
need to be passed down from the root. The document gives the reason: PSI accounts stalls per
cgroup and aggregates them at each hierarchy level, which may be non-negligible overhead in deep
hierarchies, so the switch exists to disable accounting in non-leaf cgroups.

**What this source does NOT support (explicit non-claims).**

1. **No counter semantics.** The document defines no `avg10`/`avg60`/`avg300`/`total` semantics
   and no `some`/`full` meaning; it defers to `Documentation/accounting/psi.rst` for "details".
   The contract's `full_system_undefined` rule for system `cpu` and the "irq needs `full` only"
   rule are **not** in this file — they come from `psi.rst` (S001's source) and, for IRQ, from
   the sibling `S090` code row. This row must not be cited for either.
2. **No system-level `/proc/pressure` claim.** `cgroup-v2.rst` never mentions `/proc/pressure/`
   or the system-wide files at all. It is a cgroup-interface document only.
3. **No host-availability attestation.** The document says nothing about whether a given host
   exposes these files (it depends on `CONFIG_CGROUPS`, cgroup2 being mounted, PSI being
   enabled in the build). A documented interface is not proof that a host has it.
4. **No file paths.** The document names the interface files but not their on-disk locations
   (`/sys/fs/cgroup/<path>/…`), and it does not name the `cgroup.pressure` path either.
5. **No thresholds, no verdict names, no arithmetic.** Nothing here supports `--warn-avg10`,
   `PRESSURE_HIGH`/`PRESSURE_OK`/`PRESSURE_PARTIAL`/`PRESSURE_UNAVAILABLE`, `total_delta_us`,
   `stall_ratio` or `counter_regressed`; those are the lane's own tool contract.
6. **No write authority.** The document describes `cgroup.pressure` as writable, but this round's
   bounds are detection-and-report only: no `/proc`, `/sys` or cgroup file may be written, and no
   PSI trigger may be registered. The row records the documented semantics; it authorises no
   write.
7. **No IRQ "some" rule.** `cgroup-v2.rst` does not say whether `irq.pressure` carries a `some`
   line; only the sibling code row and the live host observation below do.
8. **Version bound.** Everything above is bound to the `v7.2` tag. It is not a statement about
   the running kernel of this host.

---

## 7. Live host corroboration (read-only, this seat — NOT a claim of the tool)

Observed on this workstation at 2026-10-22T08:18Z, read-only, no writes to `/proc` or `/sys`:

```
$ ls /proc/pressure
cpu  io  irq  memory
$ head -3 /proc/pressure/irq
full avg10=0.00 avg60=0.00 avg300=0.00 total=6147168
```

`/proc/pressure/{cpu,memory,io,irq}` all exist here; `irq` exposes **only** a `full` line and no
`some` line, while `cpu`, `memory` and `io` each expose `some` and `full`. This corroborates the
contract's P03 expectation and the sibling `S090` code row's full-only IRQ rule, and it is the
reason the tool's `irq.some = null` is an expected shape rather than a malformed read. It is a
host observation only: it is not sourced from `cgroup-v2.rst`, and it attests nothing about other
hosts.

---

## 8. Coordination notes for the L1

- `S090` is provisionally claimed twice (by `SrcKconfig` and `SrcPsiIrqCommit`). This seat left
  its own id as `S0xx` per the dispatch; assign it after the collision is resolved.
- `used-by` naming `corpus/knowledge/system-pressure-r24.md` presumes that note lands and cites
  the row. Until then, `used-by: —` and `status: queued` are the honest cells.
- Overlap check against the sibling IRQ-code row: none found (see §5). `MoriR24.ConnectSourceDuplicates`
  should confirm.

## 9. Limits — what this seat did not do

- Did not edit `corpus/SOURCES.md`, `corpus/lessons/`, `corpus/knowledge/`, `SKILL.md` or any lane
  file; the only file written is this report.
- Did not touch the lane's Git index or `jj` state; no `git add`/`commit`/`checkout`/`reset`/
  `stash`/`push`, no mutating `jj` command; no clone was made and no sandbox git check was run.
- Did not open `docs.kernel.org/admin-guide/cgroup-v2.html` (S002's rendered page) or
  `docs.kernel.org/accounting/psi.html` (S001's rendered page); the overlap analysis in §5 rests on
  the `v7.2` `.rst` sources of the same two documents plus the existing registry rows' own scope
  cells. The rendered pages may differ in line numbers from the pinned sources.
- Did not open `kernel/sched/psi.c`, `include/linux/psi_types.h` or the PSI Kconfig/boot-parameter
  pages; those are other seats' rows.
- Did not write any `/proc`, `/sys` or cgroup file, did not register a PSI trigger, did not restart
  a service, and did not run, build or test `tools/mori-pressure.py` (not present in the lane at
  report time).
- No tool was installed or upgraded for this seat.
