# SrcPsiTypes — round-24 source seat: `include/linux/psi_types.h` at Linux v7.2

Scope of this seat: open the kernel header that defines the PSI resource enum and the
pressure-state set, verify the anchors, and draft **one** SOURCES.md row plus a `## Gate`
block for the round-24 lesson. Draft only — the lane file was not edited.

- Claim served: **C2 (coverage, frontier FR12)** — system `/proc/pressure/{cpu,memory,io,irq}`
  is unobserved; C2 moves a one-shot system PSI read into Core.
- Sibling rows: `MoriR24.SrcPsiRst` (Documentation/accounting/psi.rst), `MoriR24.SrcPsiC`
  (kernel/sched/psi.c), `MoriR24.SrcCgroupV2`, `MoriR24.SrcKconfig`,
  `MoriR24.SrcKernelParams`, `MoriR24.SrcProcPressureMan`,
  `MoriR24.SrcPsiIrqCommit` (introduction commit `52b1364ba0b1`).

## 1. What was done (executed, in order)

1. Fetched the URL cold, no cache, no local checkout involved:
   ```
   curl -sS -o /fast/scratch/hyaku/psi_types.h \
     -w 'http=%{http_code} size=%{size_download} url=%{url_effective}\n' \
     https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/psi_types.h
   ```
   Output: `http=200 size=5061 url=https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/psi_types.h`
2. Access timestamps (UTC, host clock): **2026-10-22T08:14:51Z** before the fetch and
   **2026-10-22T08:14:51Z** after it (same second).
3. Digest of the fetched bytes:
   ```
   sha256sum /fast/scratch/hyaku/psi_types.h
   483269b27c82b438450632555aba2ba8a9c47b608243f78a029c4300b3618ccc  psi_types.h
   ```
   **SHA-256 first 16 hex: `483269b27c82b438`** (full: `483269b27c82b438450632555aba2ba8a9c47b608243f78a029c4300b3618ccc`),
   5061 bytes. First bytes are `/* SPDX-License-Identifier: GPL-2.0 */` — the expected file head, so the
   fetch was a real body, not an error page.
4. Anchors located and read in the fetched bytes (line numbers are of the fetched file):
   - `enum psi_res` — lines **41–49**: `PSI_IO` (42), `PSI_MEM` (43), `PSI_CPU` (44),
     `#ifdef CONFIG_IRQ_TIME_ACCOUNTING` (45), `PSI_IRQ` (46), `#endif` (47), `NR_PSI_RESOURCES` (48).
   - `enum psi_states` — lines **57–70**: `PSI_IO_SOME` (58), `PSI_IO_FULL` (59), `PSI_MEM_SOME` (60),
     `PSI_MEM_FULL` (61), `PSI_CPU_SOME` (62), `PSI_CPU_FULL` (63),
     `#ifdef CONFIG_IRQ_TIME_ACCOUNTING` (64), `PSI_IRQ_FULL` (65), `#endif` (66),
     `/* Only per-CPU, to weigh the CPU in the global average: */` (67), `PSI_NONIDLE` (68),
     `NR_PSI_STATES` (69).
   - State-semantics comment — lines **51–56** (`SOME`/`FULL` definitions).
   - `PSI_IRQ_SOME` — **absent** (`grep -c PSI_IRQ_SOME` → `0`); the IRQ resource has a `FULL`
     state only.
   - `CONFIG_PSI` off branch — line **208** `#else /* CONFIG_PSI */`, line **210**
     `#define NR_PSI_RESOURCES 0`, line 214 `#endif /* CONFIG_PSI */`.
5. Overlap check inside `corpus/SOURCES.md` (read-only; the file was not modified):
   `grep -n "psi_types\|psi\.rst\|sched/psi\.c\|proc_pressure"` → **no hits**; the only PSI
   rows in the registry are **S001** (`https://docs.kernel.org/accounting/psi.html`) and **S002**
   (`https://docs.kernel.org/admin-guide/cgroup-v2.html`). No row already covers this URL or this
   scope.
6. Cross-check fetch of `https://docs.kernel.org/accounting/psi.html` (S001's URL, `http=200`,
   19726 bytes) was made **only** to test whether S001 already teaches what the header teaches.
   It does not: the page is user-facing (file format, ratios, thresholds) and contains no
   `psi_res`/`psi_states` enum. The page does contain the sentence "CPU full is undefined at the
   system level, but has been reported since 5.13, so it is set to zero for backward
   compatibility." — that is the **documentation's** claim and is *not* supported by the header
   row drafted here. S001 was not re-opened for a new claim and its original 2026-10-19 bytes
   were not re-verified.

## 2. Drafted SOURCES.md row (exact 11-cell shape; id left for the L1)

Header shape verified against `corpus/SOURCES.md:5-6`
(`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`)
and against the style of rows S085–S089 at `corpus/SOURCES.md:89-93`.

Draft row — **new row, id left as `S0xx` for the L1 to assign**:

```markdown
| S0xx | Linux include/linux/psi_types.h at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/psi_types.h | code | A | kernel-internal PSI enums: the stallable-resource set and the per-resource pressure-state set; the IRQ resource and PSI_IRQ_FULL are compile-time conditional on CONFIG_IRQ_TIME_ACCOUNTING; v7.2 only | enum psi_res:41-49; enum psi_states:57-70; state-semantics comment:51-56; PSI_IRQ conditional:45-47,64-66; PSI_NONIDLE:67-68; CONFIG_PSI off branch:208-214; tag v7.2; sha256 483269b27c82b438 | The stallable resources are IO, MEM and CPU, plus IRQ only when CONFIG_IRQ_TIME_ACCOUNTING is built in; IO, MEM and CPU each carry a SOME and a FULL state while IRQ carries a FULL state only, so an irq reading without a some line is expected rather than malformed. | queued | 2026-10-22 | on-release | — |
```

Notes for the L1 on the mutable cells:

- `status` is drafted **queued** and `used-by` **—** because the file that will cite this row,
  `corpus/knowledge/system-pressure-r24.md`, does not exist in the lane yet (it is being drafted
  by the knowledge-entry seat). Promote to `mined` with
  `used-by = corpus/knowledge/system-pressure-r24.md` only after that file lands; the SKILL.md
  decision table may be added to `used-by` at the same time, per the C2 "Sourced" clause.
- `id`: the sibling IRQ-commit seat has taken **S090**; this row should take the next free id.
- `kind` = `code` (a C header, matching S003–S006 and S077–S089 style), `tier` = `A`
  (primary upstream source, same tier as every other Linux v7.2 code row).

## 3. Draft `## Gate` block for the round-24 lesson

Modelled on the round-23 Gate tables (`corpus/lessons/round-23.md:34-48` and `:213-224`),
one row per decision, ≤25-word located quote, and the row's own scope statement.

```markdown
## Gate

Source rows opened this round for C2 (system pressure capability, frontier FR12) — all URLs
fetched cold on 2026-10-22; raw bytes retained under `.ufo/waves/round-24/evidence/sources/`.
A-tier primary sources are documentary authority for the stated scope only; they are not proof
of a running kernel's configuration or of tool health.

| Row | Opened URL / access date | Located literal quote (≤25 words) | Gate |
|---|---|---|---|
| S0xx | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/psi_types.h ; 2026-10-22T08:14:51Z | lines 54-55: "SOME: Stalled tasks & working tasks" / "FULL: Stalled tasks & no working tasks" (13) | A/mined for the kernel resource enum (IO, MEM, CPU, IRQ under CONFIG_IRQ_TIME_ACCOUNTING) and the state set, including that IRQ has a FULL state and no SOME state. Not evidence of which resources a live host exposes, nor of the /proc/pressure line grammar or the system-level CPU-full rule. |
```

Verbatim quote block for the same anchors, copied exactly from the fetched bytes
(`include/linux/psi_types.h`, lines 51–56):

```
/*
 * Pressure states for each resource:
 *
 * SOME: Stalled tasks & working tasks
 * FULL: Stalled tasks & no working tasks
 */
```

and the resource enum, lines 40–49, verbatim:

```
/* Resources that workloads could be stalled on */
enum psi_res {
	PSI_IO,
	PSI_MEM,
	PSI_CPU,
#ifdef CONFIG_IRQ_TIME_ACCOUNTING
	PSI_IRQ,
#endif
	NR_PSI_RESOURCES,
};
```

### Narrow claim this source supports

1. The kernel's stallable PSI resources are `PSI_IO`, `PSI_MEM` and `PSI_CPU`, plus `PSI_IRQ`
   **only when `CONFIG_IRQ_TIME_ACCOUNTING` is built in** (`enum psi_res`, lines 41–49). A host
   built without IRQ time accounting has no IRQ resource at all — so an `irq` reading that is
   absent or unavailable is a legitimate configuration state, not a zero and not an error to
   be retried forever.
2. The pressure-state set is per-resource `SOME`/`FULL` pairs for IO, MEM and CPU, and a
   `FULL`-only state for IRQ (`enum psi_states`, lines 57–70); `PSI_IRQ_SOME` does not exist in
   the header. Therefore an IRQ pressure file that carries no `some` line is the **expected**
   shape and must not be reported as malformed.
3. `SOME` and `FULL` are distinct stall states with the stated meanings (lines 51–56): `some`
   is "Stalled tasks & working tasks", `full` is "Stalled tasks & no working tasks".
4. `PSI_NONIDLE` is per-CPU only and exists to weigh the CPU in the global average (line 67–68)
   — it is not a user-visible per-resource state.
5. With `CONFIG_PSI` off, `NR_PSI_RESOURCES` is 0 (lines 208–214): PSI is a compile-time
   feature of the kernel build, independent of any runtime setting.

### What this source does NOT support

- **It does not define the `/proc/pressure/{cpu,memory,io,irq}` file names or the
  `avg10= avg60= avg300= total=` line grammar.** Those live in `kernel/sched/psi.c`
  (`psi_show()`) and `Documentation/accounting/psi.rst` — other rows in this round. This row
  must not be cited for the line grammar or for the file names.
- **It does not support the C2 label `full_system_undefined: true`.** The header defines
  `PSI_CPU_FULL` as an ordinary state and says nothing about the system level. The
  "CPU full is undefined at the system level" rule is the **documentation's** statement
  (docs.kernel.org/accounting/psi.html, and psi.rst) — cite S001 or the psi.rst row for it,
  not this header.
- **It does not support any threshold semantics** (`--warn-avg10` default 10.0, `PRESSURE_HIGH`
  cut-off), any verdict/exit-code rule, or the claim that any particular threshold is
  calibrated. Those are mori's own local, labelled thresholds.
- **It does not support the runtime error mapping** `ENOENT → absent`, `EOPNOTSUPP →
  unsupported`, `EACCES/EPERM → unreadable`. No errno handling exists in this header; that
  mapping is the tool's own rule.
- **It does not establish what any live host exposes.** `CONFIG_PSI` and
  `CONFIG_IRQ_TIME_ACCOUNTING` are build-time choices; this header says nothing about the
  running kernel's configuration, and no host-state claim may be derived from it.
- **It does not support any per-resource reading of live values**, `total_delta_us`,
  `stall_ratio`, or counter-regression detection. Those are `/proc/pressure` file semantics.
- **It does not establish introduction history.** `PSI_IRQ` appears here as v7.2 tree state;
  the commit that introduced IRQ/softirq pressure (`52b1364ba0b105122d6de0e719b36db705011ac1`,
  first released in Linux 6.1) belongs to the sibling row `MoriR24.SrcPsiIrqCommit`, which
  deliberately does not claim v7.2 bytes. No supersession in either direction.
- **It does not cover cgroup-scoped pressure files** (cgroup-v2 `memory.pressure` etc.) — that
  is S002 / the cgroup-v2 seat.

## 4. New row or supersession?

**New row.** No existing SOURCES.md row has this URL or this scope.

- **S001** (`https://docs.kernel.org/accounting/psi.html`, kind `docs`) — user-facing PSI
  documentation: counter semantics, ratios, thresholds, per-cgroup files. Different URL,
  different kind, different scope; it does not teach the kernel enums. **Not superseded.**
- **S002** (`https://docs.kernel.org/admin-guide/cgroup-v2.html`) — cgroup-v2 memory events and
  scope. **Not superseded.**
- **S090 (sibling, `MoriR24.SrcPsiIrqCommit`)** — the upstream commit that introduced
  `PSI_IRQ`/`PSI_IRQ_FULL`. Same enum identifiers, different URL (the commit page), different
  anchors (commit diff vs v7.2 header lines), different claim (introduction history vs current
  tree state). The two seats exchanged this agreement in-channel
  (`agent://MoriR24.SrcPsiIrqCommit`); the overlap is flagged here for the L1 and for
  `MoriR24.ConnectSourceDuplicates`.

## 5. Gates, touched surfaces, out of scope

- **Gates observed:** lane file `corpus/SOURCES.md` read-only — not edited, not staged, not
  committed; no `git add`/`commit`/`stash`/`checkout`/`reset`/`pull`/`push` and no mutating `jj`
  command was run in the lane. All writes of this seat are confined to
  `/fast/scratch/hyaku/psi_types.h` (a scratch copy outside the repo) and to this report file.
- **Touched surfaces:** `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-24/w1/SrcPsiTypes.md`
  (this report — the only file created inside the lane repo, as permitted);
  `/fast/scratch/hyaku/psi_types.h` and `/fast/scratch/hyaku/psi.html` (scratch fetch copies).
- **Out of scope / not done:** no lane-file edit (draft only, per the assignment); no
  product-code edit; no commit/push/publish/deploy; no second runtime invocation beyond the
  read-only `curl`/`sha256sum`/`grep`/`sed` commands shown; no `/proc`, `/sys` or cgroup write;
  no PSI trigger registration; no service or package change.
- **Tooling:** no install or upgrade was needed. `curl 8.23.0 (x86_64-pc-linux-gnu)
  libcurl/8.23.0 OpenSSL/3.6.5 zlib/1.3.2` was already present on the host and was used for the
  fetch; `sha256sum`, `grep`, `awk`, `sed` are coreutils. The pacman guard (all pacman
  transactions paused host-wide) was therefore never engaged.

## 6. Findings for the canonical judge

1. **Falsifier-relevant:** the C2 contract requires `irq` to need `full` only and its missing
   `some` to be expected (`some: null`, never malformed). This header is the primary-source
   basis for that rule — `enum psi_states` contains `PSI_IRQ_FULL` and **no** `PSI_IRQ_SOME`.
   The tool's rule and the kernel's enum agree; a tool that marks an irq-only file malformed
   would contradict the kernel's own state set.
2. **Boundary that must not be blurred:** the header defines `PSI_CPU_FULL` as a normal state
   and is **silent** on the system level. The C2 `full_system_undefined: true` label is
   therefore *not* supported by this row; it must be cited to the documentation row (S001 /
   psi.rst). If a knowledge entry cites this header for `full_system_undefined`, that citation
   is wrong.
3. **Same reasoning for the line grammar:** `^(some|full) avg10=… total=N$` is a `psi.c` /
   psi.rst fact, not a `psi_types.h` fact. A C2 row citing this header for the grammar is
   misattributed.
4. **Conditional-resource consequence:** `PSI_IRQ` is behind `CONFIG_IRQ_TIME_ACCOUNTING` and
   the whole subsystem behind `CONFIG_PSI` (`NR_PSI_RESOURCES 0` when off). An `irq` resource
   that is unavailable must be reported as unavailable, never as zero pressure — the header
   supports that a kernel may legitimately have no IRQ pressure at all.
5. **Duplicate-surface note:** two round-24 rows (this one and S090) touch the same enum
   identifiers from two different directions (v7.2 tree bytes vs introduction commit). Not a
   supersession; flag retained for `ConnectSourceDuplicates`.

## 7. Artifact paths

- Draft row (for `corpus/SOURCES.md`): inside this report, §2.
- Draft `## Gate` block (for `corpus/lessons/round-24.md`): inside this report, §3.
- Fetched bytes (scratch, outside the lane): `/fast/scratch/hyaku/psi_types.h` —
  sha256 `483269b27c82b438450632555aba2ba8a9c47b608243f78a029c4300b3618ccc`, 5061 bytes,
  fetched 2026-10-22T08:14:51Z.
- Cross-check fetch of S001's page (overlap test only, not a source for this row):
  `/fast/scratch/hyaku/psi.html`, 19726 bytes, `http=200`.
- This report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-24/w1/SrcPsiTypes.md`.

**Report: `.ufo/waves/round-24/w1/SrcPsiTypes.md`**
