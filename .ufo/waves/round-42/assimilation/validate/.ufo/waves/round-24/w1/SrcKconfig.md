# SrcKconfig — round-24 C2 sourced frontier step (draft only, no lane file edited)

Seat: `MoriR24.SrcKconfig` (leaf, no subagents). Surface claimed: **one** `SOURCES.md` row
for the Linux v7.2 `init/Kconfig` file, plus a `## Gate` block for the round-24 lesson.

Lane file status: **not edited.** `corpus/SOURCES.md` is unchanged on disk; this report
carries the draft row and the draft Gate block for the L1 to admit.

---

## 1. Fetch record (provenance)

| Item | Value |
|---|---|
| URL | https://raw.githubusercontent.com/torvalds/linux/v7.2/init/Kconfig |
| UTC access time | **2026-10-22T08:14:40Z** (request issued; post-fetch check 2026-10-22T08:15:47Z) |
| HTTP status | 200 (`http_code=200`, `url_effective` identical to the request URL) |
| Bytes | 74156 (matches `wc -c`) |
| Lines | 2321 |
| SHA-256 (full) | `a43f09d89309a6bd7036c96e0836c30c021f2d56b042be288a15533dd9e944bd` |
| **SHA-256 (first 16 hex)** | **`a43f09d89309a6bd`** |
| Tool | `curl 8.23.0` (system package, no install performed) |
| Local copy (outside the lane repo) | `/tmp/mori-src-kconfig/Kconfig.v72` |

Command actually run:

```
$ mkdir -p /tmp/mori-src-kconfig && cd /tmp/mori-src-kconfig \
  && date -u +"%Y-%m-%dT%H:%M:%SZ" \
  && curl -sS -f -o Kconfig.v72 \
       -w "http_code=%{http_code}\nsize=%{size_download}\nurl_effective=%{url_effective}\n" \
       https://raw.githubusercontent.com/torvalds/linux/v7.2/init/Kconfig
2026-10-22T08:14:40Z
http_code=200
size=74156
url_effective=https://raw.githubusercontent.com/torvalds/linux/v7.2/init/Kconfig
$ sha256sum Kconfig.v72
a43f09d89309a6bd7036c96e0836c30c021f2d56b042be288a15533dd9e944bd  Kconfig.v72
```

No `git`/`jj` command was run in the lane repo for this seat; no lane, sibling-lane or
index mutation was performed. Only `curl`, `sha256sum`, `grep`, `awk`, `sed`-free
numbered reads were used.

## 2. Line anchors verified in the fetched bytes

Anchors were verified by printing the fetched file with line numbers (`awk 'NR>=a && NR<=b
{printf "%d|%s\n", NR, $0}'`), so the numbers below are the fetched file's own numbering.

**`CONFIG_IRQ_TIME_ACCOUNTING` — 615–624** (config 615, `bool` 616,
`depends on HAVE_IRQ_TIME_ACCOUNTING && !VIRT_CPU_ACCOUNTING_NATIVE` 617, `help` 618):

```
615|config IRQ_TIME_ACCOUNTING
616|	bool "Fine granularity task level IRQ time accounting"
617|	depends on HAVE_IRQ_TIME_ACCOUNTING && !VIRT_CPU_ACCOUNTING_NATIVE
618|	help
619|	  Select this option to enable fine granularity task irq time
620|	  accounting. This is done by reading a timestamp on each
621|	  transitions between softirq and hardirq state, so there can be a
622|	  small performance impact.
```

**`CONFIG_PSI` — 723–741** (config 723, `bool` 724, `select KERNFS` 725, `help` 726):

```
723|config PSI
724|	bool "Pressure stall information tracking"
725|	select KERNFS
726|	help
727|	  Collect metrics that indicate how overcommitted the CPU, memory,
728|	  and IO capacity are in the system.
...
730|	  If you say Y here, the kernel will create /proc/pressure/ with the
731|	  pressure statistics files cpu, memory, and io. These will indicate
732|	  the share of walltime in which some or all tasks in the system are
733|	  delayed due to contention of the respective resource.
...
735|	  In kernels with cgroup support, cgroups (cgroup2 only) will
736|	  have cpu.pressure, memory.pressure, and io.pressure files,
737|	  which aggregate pressure stalls for the grouped tasks only.
739|	  For more details see Documentation/accounting/psi.rst.
```

**`CONFIG_PSI_DEFAULT_DISABLED` — 743–760** (config 743, `bool` 744, `default n` 745,
`depends on PSI` 746, `help` 747):

```
743|config PSI_DEFAULT_DISABLED
744|	bool "Require boot parameter to enable pressure stall information tracking"
745|	default n
746|	depends on PSI
747|	help
748|	  If set, pressure stall information tracking will be disabled
749|	  per default but can be enabled through passing psi=1 on the
750|	  kernel commandline during boot.
```

**Negative check performed:** `grep -n -i irq` over lines 723–760 of the fetched file
returns **nothing** — the v7.2 PSI option block names only `cpu`, `memory` and `io`
pressure files; `irq` appears in this file only in unrelated options
(`IRQ_TIME_ACCOUNTING` 615, `HAVE_SCHED_AVG_IRQ` 626).

**Important limit on that negative check (added after peer coordination, 2026-10-22):**
the Kconfig help text's enumeration is *not* the kernel's complete `/proc/pressure/` file
set. The duplicate-connector peer `MoriR24.ConnectSourceDuplicates` flagged that
`kernel/sched/psi.c` v7.2 also creates `pressure/irq` under `CONFIG_IRQ_TIME_ACCOUNTING`.
I verified that claim myself before re-wording the row (cross-check only — **no row is
proposed for `kernel/sched/psi.c` here; that URL belongs to seat `SrcPsiC`**):

| Item | Value |
|---|---|
| URL | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c |
| UTC access time | 2026-10-22T08:20:41Z |
| HTTP status / size | 200 / 48859 bytes |
| SHA-256 | `452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5` |
| Local copy (outside the lane repo) | `/tmp/mori-src-kconfig/psi.c.v72` |

```
1710|static int __init psi_proc_init(void)
1711|{
1712|	if (psi_enable) {
1713|		proc_mkdir("pressure", NULL);
1714|		proc_create("pressure/io", 0666, NULL, &psi_io_proc_ops);
1715|		proc_create("pressure/memory", 0666, NULL, &psi_memory_proc_ops);
1716|		proc_create("pressure/cpu", 0666, NULL, &psi_cpu_proc_ops);
1717|#ifdef CONFIG_IRQ_TIME_ACCOUNTING
1718|		proc_create("pressure/irq", 0666, NULL, &psi_irq_proc_ops);
1719|#endif
1720|	}
```

So the correct reading is: the **Kconfig help text names only** `cpu`, `memory` and `io`;
the **kernel** additionally creates `pressure/irq` when `CONFIG_IRQ_TIME_ACCOUNTING` is
built in. The Kconfig row is therefore worded as what the *option text* says, never as the
kernel's complete file list.

## 3. Duplicate / supersession check against `corpus/SOURCES.md`

Checked `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` (141 lines, registry
rows S001–S089 at lines 7–95).

- `grep -rn "init/Kconfig" corpus/` → **no match**. No existing row uses this URL or this file.
- `grep -n -i "Kconfig" corpus/SOURCES.md` → **no match**; the registry has no Kconfig row at all.
- S001 = https://docs.kernel.org/accounting/psi.html — different URL, different kind
  (`docs`), different scope (runtime counters, totals, thresholds, per-cgroup files;
  page dated 2018-04, opened 2026-10-19).
- S002 = https://docs.kernel.org/admin-guide/cgroup-v2.html — different URL, different scope
  (cgroup-v2 memory events, `memory.peak`, local vs hierarchical scope).
- Other pressure-adjacent rows: S007 (systemd-oomd.service(8)), S010 (systemd.io/PRESSURE/),
  S021 (LWN BPF OOM proposal) — none names `init/Kconfig` or the build-time PSI options.

**Determination: this is a NEW row, not a supersession.** It neither replaces S001 nor S002
and edits neither. Its scope (build-time kernel options: the `/proc/pressure/` files the
`CONFIG_PSI` help text names, the `psi=1` opt-in that overrides
`CONFIG_PSI_DEFAULT_DISABLED`, and the separate IRQ-time-accounting option) is disjoint from
S001's runtime-counter scope and S002's cgroup-interface scope. It is **adjacent** to
S001/S002/S010, not a correction of them.

Coordination: the duplicate-connector peer `MoriR24.ConnectSourceDuplicates` was messaged
with this URL, digest, anchors and the irq-negative finding before this report was written,
and confirmed the NEW-row determination (its probe over all 8 planned round-24 URLs found
no row for this URL, so no W04/E04). It also flagged that `kernel/sched/psi.c` v7.2 creates
`pressure/irq` under `CONFIG_IRQ_TIME_ACCOUNTING`; that claim was verified here (§2b) and
the row was re-worded so it no longer presents the Kconfig help text as the kernel's
complete file list. The connector's scope split is adopted: this row keeps `psi=1` as the
build-default override only, and boot-parameter semantics stay with `SrcKernelParams`.

## 4. Draft row for `corpus/SOURCES.md` (id left for the L1; `S0xx`)

Header (line 5), for shape reference — 11 cells:
`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`

Draft row (one line, 11 cells, `SOURCES.md` registry style as in S077–S089):

```
| S0xx | Linux PSI and IRQ time accounting Kconfig at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/init/Kconfig | code | A | the CONFIG_PSI, CONFIG_PSI_DEFAULT_DISABLED and CONFIG_IRQ_TIME_ACCOUNTING build options and their help text: the /proc/pressure/ files the CONFIG_PSI help text names, and the psi=1 opt-in that overrides CONFIG_PSI_DEFAULT_DISABLED; v7.2 only | CONFIG_PSI:723-741 (help-text file list:730-733, cgroup2 text:735-737); CONFIG_PSI_DEFAULT_DISABLED:743-760 (psi=1 text:748-750); CONFIG_IRQ_TIME_ACCOUNTING:615-624; tag v7.2; sha256 a43f09d89309a6bd | The CONFIG_PSI help text names only the pressure statistics files cpu, memory, and io under /proc/pressure/ plus the cgroup2 per-cgroup files; CONFIG_PSI_DEFAULT_DISABLED leaves tracking disabled unless psi=1 is passed on the kernel commandline; CONFIG_IRQ_TIME_ACCOUNTING is a separate fine-granularity task irq time option. | mined | 2026-10-22 | on-release | corpus/lessons/round-24.md |
```

Cell-by-cell justification:

| cell | value | why |
|---|---|---|
| id | `S0xx` | id left for the L1 to assign; the registry's next free number is S090 |
| source | Linux PSI and IRQ time accounting Kconfig at v7.2 — URL | matches the S077–S089 naming shape (`Linux <path> at v7.2 — <raw URL>`); the URL itself is pinned to tag `v7.2` |
| kind | `code` | the registry's existing kind vocabulary is `docs`(48), `code`(20), `spec`(9), `tool`(4), `community`(3), `paper`(2), `book`(2), `own-work`(1); `init/Kconfig` is a kernel-tree source file, so `code` is the closest existing value and introduces no new kind |
| tier | `A` | primary upstream kernel source, same tier as S003/S077–S089 |
| scope | CONFIG_PSI / CONFIG_PSI_DEFAULT_DISABLED / CONFIG_IRQ_TIME_ACCOUNTING options and help text only; v7.2 only | deliberately narrow: build-time option semantics, not runtime counter semantics (S001), not cgroup scope (S002), not thresholds or triggers; the file list is stated as what the *help text names*, not as the kernel's complete file set (§2b) |
| anchor | the four verified line ranges + `tag v7.2` + `sha256 a43f09d89309a6bd` | every line number was printed from the fetched bytes; digest style matches S077–S089 (16 hex chars) |
| teaches | the three claims each tied to a verified anchor, with the file list attributed to the help text | stated as build-time facts, not as host observations; "names only" keeps the row from over-claiming completeness against `kernel/sched/psi.c` 1717–1719 |
| status | `mined` | the row is used by the round-24 lesson Gate (per the round-23 precedent: "New rows enter mined with used-by this lesson"), and gains the knowledge note once `corpus/knowledge/system-pressure-r24.md` exists and cites it |
| opened | `2026-10-22` | UTC fetch date recorded in §1 |
| recheck | `on-release` | the URL is pinned to the `v7.2` tag, so recheck happens on a kernel release bump |
| used-by | `corpus/lessons/round-24.md` | the artifact that will cite it; append `corpus/knowledge/system-pressure-r24.md` after that note exists and cites the row (that file does not exist yet — `corpus/knowledge/` has no `system-pressure-r24.md` today) |

## 5. Draft `## Gate` block for `corpus/lessons/round-24.md`

Round-23 lesson Gate shape is `| Row | URL | Located quote (≤25 words) | Decision / scope |`.
Draft below, ready to paste into the round-24 lesson:

```markdown
## Gate

One new source row for the C2 pressure step; no supersession. The row is a NEW row, not a
replacement: `corpus/SOURCES.md` has no row for `init/Kconfig` (`grep -rn "init/Kconfig"
corpus/` returns nothing). S001 (docs.kernel.org/accounting/psi.html) and S002
(docs.kernel.org/admin-guide/cgroup-v2.html) keep their scopes — runtime PSI counters and
thresholds, and the cgroup-v2 interface respectively — and are adjacent, not superseded.

URL: https://raw.githubusercontent.com/torvalds/linux/v7.2/init/Kconfig
Access date: 2026-10-22 (UTC), request issued 2026-10-22T08:14:40Z; HTTP 200; 74156 bytes.
SHA-256 of the fetched bytes: a43f09d89309a6bd7036c96e0836c30c021f2d56b042be288a15533dd9e944bd
(first 16 hex: a43f09d89309a6bd).

| Row | URL | Located quote (≤25 words) | Decision / scope |
|---|---|---|---|
| S0xx | https://raw.githubusercontent.com/torvalds/linux/v7.2/init/Kconfig | 730–733: “If you say Y here, the kernel will create /proc/pressure/ with the pressure statistics files cpu, memory, and io.” | Admit A for the v7.2 build-time PSI options and the file list the option help text names; not for the kernel's complete file set, host PSI state, thresholds or trigger behaviour. |

Line anchors verified in the fetched bytes:
`CONFIG_IRQ_TIME_ACCOUNTING` 615–624 (help text 619–622); `CONFIG_PSI` 723–741
(`bool` 724, `select KERNFS` 725, pressure-file text 730–733, cgroup2 text 735–737,
cross-reference `Documentation/accounting/psi.rst` 739); `CONFIG_PSI_DEFAULT_DISABLED` 743–760
(`default n` 745, `depends on PSI` 746, help text 748–750).

Additional located quotes (≤25 words each, same fetch):
- 748–750 (`CONFIG_PSI_DEFAULT_DISABLED`): “If set, pressure stall information tracking will
  be disabled per default but can be enabled through passing psi=1 on the kernel commandline
  during boot.”
- 619–620 (`CONFIG_IRQ_TIME_ACCOUNTING`, wraps across two lines):
  “Select this option to enable fine granularity task irq time accounting.”

Reject: that the Kconfig help text enumerates the kernel's complete `/proc/pressure/` file
set — it names only `cpu`, `memory` and `io`, while `kernel/sched/psi.c` v7.2 1717–1719
creates `pressure/irq` under `CONFIG_IRQ_TIME_ACCOUNTING` (cross-checked here; that URL
belongs to the `kernel/sched/psi.c` row, not to this one); that `CONFIG_IRQ_TIME_ACCOUNTING`
is itself pressure accounting — its help text describes IRQ *time* accounting; that a host
has PSI enabled — this file is build-time configuration, not runtime state; that any
threshold or `avg10` value is calibrated here — the option text states no numbers.

No existing immutable registry row is edited. The row enters `mined` with used-by this
lesson and gains the knowledge note only after `corpus/knowledge/system-pressure-r24.md`
exists and cites it.
```

## 6. The narrow claim this source supports — and what it does NOT support

**Supports (all three tied to verified lines):**

1. The `CONFIG_PSI` help text (723–741) states that with the option enabled the kernel
   creates `/proc/pressure/` with the pressure statistics files `cpu`, `memory` and `io`
   (730–733), and — where cgroup2 support exists — per-cgroup `cpu.pressure`,
   `memory.pressure`, `io.pressure` aggregating for the grouped tasks only (735–737). It
   points at `Documentation/accounting/psi.rst` for detail (739). **This is what the option
   text names, not the kernel's complete file set** (§2b).
2. `CONFIG_PSI_DEFAULT_DISABLED` (743–760) defaults to `n` (745) and depends on `PSI` (746);
   when set, tracking is disabled by default and is enabled by passing `psi=1` on the kernel
   commandline at boot (748–750). So "PSI absent/disabled" is a *build-and-boot* state, and a
   missing `/proc/pressure/` file is not by itself evidence of a fault. (Boot-parameter
   *semantics* belong to the `SrcKernelParams` kernel-parameters row; this row owns only the
   build-option override as stated in this option's help text.)
3. `CONFIG_IRQ_TIME_ACCOUNTING` (615–624) is a separate option, depending on
   `HAVE_IRQ_TIME_ACCOUNTING && !VIRT_CPU_ACCOUNTING_NATIVE` (617), that enables fine
   granularity task irq time accounting by timestamping softirq/hardirq transitions, with a
   stated small performance impact (619–622). Its help text names no pressure file.

**Does NOT support (explicit limits for the L1 and for the C2 knowledge note):**

- **Not the kernel's complete `/proc/pressure/` file list.** The Kconfig option text names
  only `cpu`, `memory` and `io`; `grep -i irq` over lines 723–760 returns nothing. The
  kernel additionally creates `pressure/irq` under `CONFIG_IRQ_TIME_ACCOUNTING`
  (`kernel/sched/psi.c` v7.2 1717–1719, cross-checked in §2b). So a C2 sentence such as
  "the kernel creates cpu, memory, io and irq pressure files" is **not** supported by this
  row; the `irq` resource in `tools/mori-pressure.py` must be sourced from the
  `kernel/sched/psi.c` (or `Documentation/accounting/psi.rst`) row, or from the tool's own
  "absent is a legitimate state" rule.
- **Not runtime state.** This is build-time configuration. It says nothing about whether any
  particular host has PSI enabled, has `psi=1` on its commandline, or exposes
  `/proc/pressure/` at all.
- **Not counters, totals, thresholds or triggers.** No `avg10`/`avg60`/`avg300`/`total`
  semantics, no `avg10` threshold value, no cgroup trigger lifetime — those are S001's scope
  (`docs.kernel.org/accounting/psi.html`) and remain so.
- **Not a calibration source.** The only numeric-ish statement is the option's qualitative
  overhead note (752–756: overhead "too low to affect common scheduling-intense workloads
  in practice"); it justifies no threshold value and no verdict calibration.
- **Not a version-general statement.** Anchors and digest are v7.2-only; other releases may
  differ.

## 7. Findings reported to the canonical Rust judge (verbatim, no interpretation added)

- `grep -n -i "irq" Kconfig.v72` restricted to lines 723–760 → empty. The v7.2 PSI Kconfig
  block names only `cpu`, `memory` and `io` pressure files.
- Cross-check (raised by `MoriR24.ConnectSourceDuplicates`, verified here):
  `kernel/sched/psi.c` v7.2 1717–1719 — `#ifdef CONFIG_IRQ_TIME_ACCOUNTING` /
  `proc_create("pressure/irq", 0666, NULL, &psi_irq_proc_ops);` / `#endif`. So the Kconfig
  help text's list is **not** the kernel's complete `/proc/pressure/` file set, and the
  Kconfig row must not be worded as if it were. This URL is not claimed by this seat.
- `CONFIG_IRQ_TIME_ACCOUNTING` help text (619–622) describes IRQ **time** accounting
  (timestamping softirq/hardirq transitions), not pressure stalls and not a pressure file.
- `CONFIG_PSI_DEFAULT_DISABLED` (743–760) is the only place in this file where a `psi=`
  boot parameter appears: "passing psi=1 on the kernel commandline during boot" (749).
- The C2 contract sentence "Sourced: … cite `SOURCES.md` rows opened this round (… PSI
  Kconfig and boot parameter …)" is satisfied for the *Kconfig and boot parameter* part by
  this row: the `psi=1` boot parameter is documented inside
  `CONFIG_PSI_DEFAULT_DISABLED` in the same file. Per the duplicate connector's split, this
  row owns only the build-default override as stated in the option help text; the
  boot-parameter *semantics* belong to the `SrcKernelParams` kernel-parameters row, so the
  L1 keeps exactly one row owning each fact and the two rows do not duplicate.

## 8. Out of scope for this seat (not done, deliberately)

- No edit to `corpus/SOURCES.md`, `corpus/lessons/round-24.md`, `corpus/knowledge/`, `SKILL.md`
  or any other lane file. Draft only.
- No `git`/`jj` mutation in the lane repo; no `git add/commit/stash/checkout/reset/pull/push`;
  no sandbox clone was needed (no git-writing check was run by this seat).
- No host writes to `/proc`, `/sys` or cgroup files; no PSI trigger registration; no service
  or package change; no restart of anything.
- No row is proposed for `kernel/sched/psi.c`: it was fetched **only** as a cross-check of a
  claim raised by the duplicate-connector peer, so that this row would not over-claim the
  complete `/proc/pressure/` file set (§2b). That URL belongs to seat `SrcPsiC`.
  `Documentation/accounting/psi.rst` and `proc_pressure(5)` were not fetched — they are other
  seats' surfaces.
- No tool installs or upgrades were needed; nothing was installed (no pacman transaction, no
  `uv tool install`, no release binary). The only tools used were pre-installed `curl 8.23.0`,
  `sha256sum`, `grep`, `awk`, `date`.

## 9. Artifact paths

- Fetched bytes (outside the lane repo): `/tmp/mori-src-kconfig/Kconfig.v72`
  (sha256 `a43f09d89309a6bd7036c96e0836c30c021f2d56b042be288a15533dd9e944bd`) — the row's source.
- Cross-check bytes (outside the lane repo, not claimed as a row):
  `/tmp/mori-src-kconfig/psi.c.v72`
  (sha256 `452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5`).
- This report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-24/w1/SrcKconfig.md`
  (the only file created inside the lane repo by this seat).
- Files read but not modified: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`,
  `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-23.md` (Gate shape),
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-24/contract.md`,
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-24/wave1-assignments.json`.
