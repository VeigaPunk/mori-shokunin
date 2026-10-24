# SrcPsiC — round-24 C2 sourced frontier step (draft only, no lane file edited)

Seat: `MoriR24.SrcPsiC` (leaf, no subagents). Surface claimed: **one** `SOURCES.md` row for the
Linux v7.2 `kernel/sched/psi.c` file, plus a `## Gate` block for the round-24 lesson.

Lane file status: **not edited.** `corpus/SOURCES.md` is unchanged on disk — `git diff --stat`
in the lane repo is empty after this seat's work, and `git status --porcelain` lists only
pre-existing untracked `.scratch/` material from earlier rounds. This report carries the draft
row and the draft Gate block for the L1 to admit.

---

## 1. Fetch record (provenance)

| Item | Value |
|---|---|
| URL | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c |
| UTC access time (first fetch) | **2026-10-22T08:14:54Z** (request issued; the file was written before the timestamp line was printed — see command transcript) |
| UTC access time (re-fetch) | 2026-10-22T08:17:46Z |
| HTTP status | 200 (`http_code=200`, `url_effective` identical to the request URL) |
| Bytes | 48859 (matches `wc -c`) |
| Lines | 1725 (`wc -l`) |
| SHA-256 (full) | `452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5` |
| **SHA-256 (first 16 hex)** | **`452318beaca3e6d1`** |
| Digest stability | second fetch is byte-identical (`cmp` → identical, same SHA-256) |
| Tool | `curl 8.23.0` (pre-installed system package; **no install performed**) |
| Local copy (outside the lane repo) | `/fast/scratch/hyaku/mori-r24-a2/srcpsic/psi.c` (+ `psi.c.refetch`) |

Commands actually run:

```
$ mkdir -p /fast/scratch/hyaku/mori-r24-a2/srcpsic && cd /fast/scratch/hyaku/mori-r24-a2/srcpsic \
  && date -u +"%Y-%m-%dT%H:%M:%SZ" > access_utc.txt \
  && curl -fsSL -o psi.c https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c \
  && sha256sum psi.c && cat access_utc.txt && wc -l psi.c && wc -c psi.c
452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5  psi.c
2026-10-22T08:14:54Z
1725 psi.c
48859 psi.c

$ date -u +"%Y-%m-%dT%H:%M:%SZ" && curl -sS -f -o psi.c.refetch \
    -w "http_code=%{http_code}\nsize=%{size_download}\nurl_effective=%{url_effective}\n" \
    https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c \
  && sha256sum psi.c psi.c.refetch && cmp psi.c psi.c.refetch && echo IDENTICAL
2026-10-22T08:17:46Z
http_code=200
size=48859
url_effective=https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c
452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5  psi.c
452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5  psi.c.refetch
IDENTICAL
```

The URL is pinned to the upstream tag `v7.2`, so no commit hash is needed for byte identity; the
digest above is the receipt. No `git`/`jj` command was run in the lane repo for this seat, and
no lane, sibling-lane or index mutation was performed.

## 2. Line anchors verified in the fetched bytes

Anchors were read from the fetched copy with line numbers; the numbers below are that file's
own numbering (the file is the upstream v7.2 `kernel/sched/psi.c`).

**`psi_show` — 1251-1301** (entry point 1251):

```
1251|int psi_show(struct seq_file *m, struct psi_group *group, enum psi_res res)
1257|	if (static_branch_likely(&psi_disabled))
1258|		return -EOPNOTSUPP;
1260|#ifdef CONFIG_IRQ_TIME_ACCOUNTING
1261|	if (!irqtime_enabled() && res == PSI_IRQ)
1262|		return -EOPNOTSUPP;
1263|#endif
1273|#ifdef CONFIG_IRQ_TIME_ACCOUNTING
1274|	only_full = res == PSI_IRQ;
1275|#endif
1277|	for (full = 0; full < 2 - only_full; full++) {
1282|		/* CPU FULL is undefined at the system level */
1283|		if (!(group == &psi_system && res == PSI_CPU && full)) {
1286|			total = div_u64(group->total[PSI_AVGS][res * 2 + full],
1287|					NSEC_PER_USEC);
1290|		seq_printf(m, "%s avg10=%lu.%02lu avg60=%lu.%02lu avg300=%lu.%02lu total=%llu\n",
1291|			   full || only_full ? "full" : "some",
```

**PSI disable switch and the proc entries — 145-158, 228-235, 1709-1721:**

```
145|DEFINE_STATIC_KEY_FALSE(psi_disabled);
149|#ifdef CONFIG_PSI_DEFAULT_DISABLED
150|static bool psi_enable;
151|#else
152|static bool psi_enable = true;
153|#endif
154|static int __init setup_psi(char *str)
156|	return kstrtobool(str, &psi_enable) == 0;
158|__setup("psi=", setup_psi);
228|void __init psi_init(void)
230|	if (!psi_enable) {
231|		static_branch_enable(&psi_disabled);
232|		static_branch_disable(&psi_cgroups_enabled);
233|		return;
234|	}
1710|static int __init psi_proc_init(void)
1712|	if (psi_enable) {
1713|		proc_mkdir("pressure", NULL);
1714|		proc_create("pressure/io", 0666, NULL, &psi_io_proc_ops);
1715|		proc_create("pressure/memory", 0666, NULL, &psi_memory_proc_ops);
1716|		proc_create("pressure/cpu", 0666, NULL, &psi_cpu_proc_ops);
1717|#ifdef CONFIG_IRQ_TIME_ACCOUNTING
1718|		proc_create("pressure/irq", 0666, NULL, &psi_irq_proc_ops);
1719|#endif
1720|	}
1721|	return 0;
```

**Per-resource entry points that feed `psi_show` — 1538-1550, 1683-1686:**

```
1538|static int psi_io_show(struct seq_file *m, void *v)
1540|	return psi_show(m, &psi_system, PSI_IO);
1543|static int psi_memory_show(struct seq_file *m, void *v)
1545|	return psi_show(m, &psi_system, PSI_MEM);
1548|static int psi_cpu_show(struct seq_file *m, void *v)
1550|	return psi_show(m, &psi_system, PSI_CPU);
1683|#ifdef CONFIG_IRQ_TIME_ACCOUNTING
1684|static int psi_irq_show(struct seq_file *m, void *v)
1686|	return psi_show(m, &psi_system, PSI_IRQ);
```

**Cross-reference outside this seat's URL (supporting read only, not rowed here):**
`kernel/sched/sched.h:3492-3495` defines `irqtime_enabled()` as
`static_branch_likely(&sched_clock_irqtime)` when `CONFIG_IRQ_TIME_ACCOUNTING` is built, and
`kernel/sched/sched.h:3518-3521` returns `0` when it is not. `kernel/sched/core.c:9101` calls
`psi_init()`. These three reads are recorded as provenance for the IRQ nuance in §7; they are
**not** proposed as a row by this seat (no seat owns `kernel/sched/sched.h`).

**Live-host corroboration (read-only, this host is not claimed to be v7.2):**
`cat /proc/pressure/{cpu,memory,io,irq}` on this machine printed `cpu` with a `some` line and a
`full` line whose values are all zero, `irq` with a single `full` line, and `memory`/`io` with
`some` and `full` lines — exactly the shapes the source predicts. This is one observation of
one host, recorded as corroboration only; it is **not** a claim about the host kernel version.

## 3. Duplicate / supersession check against `corpus/SOURCES.md`

Checked `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` (registry rows
S001-S089 at lines 7-95).

- `grep` over the whole fleet root for `kernel/sched/psi.c` / `sched/psi.c` in `**/SOURCES.md`
  → **no match** in any lane (mori or sibling). No existing row uses this URL or this file.
- `grep -n -i "psi" corpus/SOURCES.md` → the only PSI-specific rows are **S001**
  (`https://docs.kernel.org/accounting/psi.html`, kind `docs`, scope: "Linux PSI counters,
  totals, thresholds and per-cgroup files") and **S002**
  (`https://docs.kernel.org/admin-guide/cgroup-v2.html`, kind `docs`, scope: cgroup-v2 memory
  events and scope). Neither names `kernel/sched/psi.c`.
- Other pressure-adjacent rows — S007 (systemd-oomd.service(8)), S010 (systemd.io/PRESSURE/),
  S021 (LWN BPF OOM proposal), S034 (own-work census) — none names this file.
- Registry validator baseline, read-only, on the lane as it stands:
  `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → **exit 0**,
  six pre-existing `W04` (same-URL-across-scopes) warnings for S035/S037/S073/S074/S075/S076 and
  `ok` for the lane. No `E` codes today.

**Determination: this is a NEW row, not a supersession.** It neither replaces nor edits S001 or
S002. S001 is the *documentation* of the PSI interface; S002 is the *cgroup-v2* interface.
This row is the *v7.2 implementation* of the **system-level** `/proc/pressure/*` files: which
kinds each resource prints, that the system CPU `full` line is a fixed zero, the `EOPNOTSUPP`
read path, and the single place where the `/proc/pressure/*` entries are created. It is
**adjacent** to S001 (same subject, different kind and evidence) and disjoint from S002
(cgroup-scoped pressure files are not in `kernel/sched/psi.c`; they live in the cgroup code).

Coordination: the duplicate-connector peer `MoriR24.ConnectSourceDuplicates` was messaged with
this URL, digest, anchors and the new-row determination before this report was written.

## 4. Draft row for `corpus/SOURCES.md` (id left as `S0xx` for the L1)

Header (line 5), for shape reference — 11 cells:
`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`

Draft row (one line, 11 cells, `SOURCES.md` registry style as in S077-S089):

```
| S0xx | Linux kernel/sched/psi.c at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c | code | A | v7.2 system-level PSI implementation only: the kinds psi_show prints per resource, the undefined system CPU full line, the EOPNOTSUPP read path, and where the /proc/pressure/* entries are created; not cgroup pressure files, not trigger semantics, not this host's kernel | psi_show:1251; psi_disabled EOPNOTSUPP:1257-1258; IRQ EOPNOTSUPP:1260-1263; only_full:1273-1275; kind loop:1277; system CPU full zero line:1282-1288; print format:1290-1291; psi_proc_init:1710-1721 (io/memory/cpu:1714-1716; irq:1717-1719); psi_enable switch:145-158,228-235; tag v7.2; sha256 452318beaca3e6d1 | psi_show prints one some line and one full line for cpu, memory and io but only a full line for IRQ, and the system CPU full line is a fixed zero rather than a measurement; psi_show returns EOPNOTSUPP on the psi_disabled branch and, for IRQ, when IRQ time accounting is off; the /proc/pressure/* entries are created once at init, so a PSI switched off at boot leaves them absent rather than unreadable | queued | 2026-10-22 | on-release | — |
```

Cell-by-cell justification:

| cell | value | why |
|---|---|---|
| id | `S0xx` | id left for the L1 to assign. **The literal placeholder is not registrable**: the validator requires `^S[0-9]{3,}$` and prints `E02 S0xx` for it (measured, §5). The registry's next free number looked like **S090**, but sibling seat `SrcPsiIrqCommit` also proposes `S090` — two rows with the same id in one registry produce `E03 S090 duplicate id` (measured, §5). Keep `S0xx` in the draft and let the L1 assign a free id across all round-24 rows. |
| source | Linux kernel/sched/psi.c at v7.2 — raw URL | matches the S077-S089 naming shape (`Linux <path> at v7.2 — <raw URL>`); the URL is pinned to the upstream tag `v7.2` |
| kind | `code` | `code` is in the registry's existing kind vocabulary (alongside `docs`, `spec`, `tool`, `paper`, `book`, `community`, `own-work`); a kernel source file is `code`, and no new kind is introduced |
| tier | `A` | primary upstream kernel source at a pinned tag, same tier as S003/S077-S089 |
| scope | v7.2 system-level PSI implementation only: printed kinds per resource, the undefined system CPU full line, the EOPNOTSUPP read path, where the `/proc/pressure/*` entries are created; **not** cgroup pressure files, **not** trigger semantics, **not** this host's kernel | deliberately narrow, and it names its own exclusions so a later reader cannot widen it into S001's or S002's territory |
| anchor | the verified line ranges plus `tag v7.2` and `sha256 452318beaca3e6d1` | every line number was printed from the fetched bytes; digest style matches S077-S089 (16 hex chars) |
| teaches | the three claims, each tied to an anchor above | phrased as kernel behaviour, not as host observations |
| status | `queued` | **proposed `queued` with used-by `—`** because `corpus/lessons/round-24.md` and `corpus/knowledge/system-pressure-r24.md` do not exist on disk today, and a `mined` row whose used-by path is missing raises `E11` (measured, §5). The round-23 precedent ("New rows enter mined with used-by this lesson") applies **only if** the lesson is committed in the same or an earlier commit — the `E11` clears only once `corpus/lessons/round-24.md` exists on disk. Then flip to `mined` with used-by `corpus/lessons/round-24.md`, and append `corpus/knowledge/system-pressure-r24.md` after that note exists and cites the row. |
| opened | `2026-10-22` | UTC fetch date (§1) |
| recheck | `on-release` | the URL is pinned to the `v7.2` tag, so recheck happens on a kernel release bump |
| used-by | `—` (queued) / `corpus/lessons/round-24.md` (mined, once it exists) | see the status row above |

## 5. Validator falsifier results (read-only; the lane file was never touched)

`scripts/sources-census.sh validate` was run against **copies of the lane in `/tmp`**
(`/tmp/mori-srcpsic-full/<case>/mori-shokunin/`, each a full copy of `corpus/` plus `SKILL.md`
so used-by paths resolve). The lane repo itself was not modified.

| case | row shape tested | validator result |
|---|---|---|
| baseline (lane as-is) | — | exit 0; six pre-existing `W04` lines + `ok` |
| `queued` | id `S090`, status `queued`, used-by `—` | **exit 0; no new line attributable to the new row** (only the six pre-existing `W04` + `ok`) |
| `placeholder` | id literal `S0xx` | exit 1 with **`E02 S0xx`** → the L1 must assign a numeric id; `S0xx` cannot be landed as-is |
| `mined-noexist` | id `S090`, status `mined`, used-by `corpus/lessons/round-24.md`, lesson file absent | exit 1 with **`E11 S090 missing used-by corpus/lessons/round-24.md`** |
| `mined-withlesson` | id `S090`, status `mined`, lesson file present | **exit 0**, no new line |
| `duplicate-id` | two rows both with id `S090` in one registry (this row plus a stand-in for the sibling `SrcPsiIrqCommit` row) | exit 1 with **`E03 S090 duplicate id`** → ids must be unique across the whole registry |

The new row therefore adds **no** `W04` (its URL is new), no `E01` (11 cells, verified by the
validator's own field count), no `E05`-`E10` (kind `code`, tier `A`, status in the enum,
`opened` a present ISO date, `recheck` symbolic) and no `E11` **provided** the L1 either lands
the lesson in the same commit or keeps the row `queued`.

## 6. Draft `## Gate` block for `corpus/lessons/round-24.md`

Round-23 lesson Gate shape is `| Row | URL | Located quote (≤25 words) | Decision / scope |`.
Draft below, ready to paste into the round-24 lesson.

```markdown
## Gate

One new source row for the C2 pressure step; no supersession. The row is a NEW row, not a
replacement: `corpus/SOURCES.md` has no row for `kernel/sched/psi.c` (a fleet-root grep for
`sched/psi.c` in every `*/corpus/SOURCES.md` returns nothing). S001
(docs.kernel.org/accounting/psi.html) and S002 (docs.kernel.org/admin-guide/cgroup-v2.html)
keep their scopes — the PSI interface documentation and the cgroup-v2 interface — and are
adjacent, not superseded.

URL: https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c
Access date: 2026-10-22 (UTC), request issued 2026-10-22T08:14:54Z; re-fetch 2026-10-22T08:17:46Z;
HTTP 200; 48859 bytes; SHA-256 452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5
(first 16 hex: 452318beaca3e6d1).

| Row | URL | Located quote (≤25 words) | Decision / scope |
|---|---|---|---|
| S0xx | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c | 1282-1283: “/* CPU FULL is undefined at the system level */ if (!(group == &psi_system && res == PSI_CPU && full)) {” | Admit A for the v7.2 system-level PSI implementation: the kinds each resource prints, the fixed-zero system CPU full line, the EOPNOTSUPP read path, and the single creation point of the /proc/pressure/* entries; not for cgroup pressure files, thresholds, verdicts or this host's kernel. |

Line anchors verified in the fetched bytes:
`psi_show` 1251-1301 (psi_disabled EOPNOTSUPP 1257-1258; IRQ EOPNOTSUPP 1260-1263;
`only_full = res == PSI_IRQ` 1273-1275; kind loop 1277; system CPU full zero line 1282-1288;
print format 1290-1291); `psi_enable` switch 145-158 and `psi_init` 228-235; `psi_proc_init`
1709-1721 (`proc_mkdir("pressure")` 1713; `pressure/io` 1714; `pressure/memory` 1715;
`pressure/cpu` 1716; `pressure/irq` 1717-1719); per-resource show entries 1538-1550 and
1683-1686.

Additional located quotes (each ≤25 words, same fetch):
- 1257-1258: “if (static_branch_likely(&psi_disabled)) return -EOPNOTSUPP;”
- 1261-1262: “if (!irqtime_enabled() && res == PSI_IRQ) return -EOPNOTSUPP;”
- 1274: “only_full = res == PSI_IRQ;”
- 1277: “for (full = 0; full < 2 - only_full; full++) {”
- 1290-1291: “seq_printf(m, "%s avg10=%lu.%02lu avg60=%lu.%02lu avg300=%lu.%02lu total=%llu\n", full || only_full ? "full" : "some",”
- 1712: “if (psi_enable) {”
- 1713: “proc_mkdir("pressure", NULL);”
- 1714: “proc_create("pressure/io", 0666, NULL, &psi_io_proc_ops);”
- 1718: “proc_create("pressure/irq", 0666, NULL, &psi_irq_proc_ops);”

Reject: that `EOPNOTSUPP` on a system pressure file means only "PSI disabled" — in this file
the same errno is also returned for the IRQ resource when IRQ time accounting is off; that a
zero-valued system CPU `full` line is evidence of no stall — the kernel prints it as a fixed
zero because the value is undefined at the system level; that a missing `/proc/pressure/*`
entry is a fault — the entries are created only when the `psi=` boot switch is on; that a
threshold, verdict vocabulary, stall ratio or counter-regression rule is kernel-defined — none
of them appear in this file.

No existing immutable registry row is edited. The row enters `queued` with used-by `—` unless
`corpus/lessons/round-24.md` lands in the same commit, in which case it enters `mined` with
used-by this lesson and gains the knowledge note only after
`corpus/knowledge/system-pressure-r24.md` exists and cites it.
```

## 7. The narrow claim this source supports — and what it does NOT support

**Supports (each tied to verified lines):**

1. **Which kinds each resource prints.** `psi_show` (1251) loops over the two kinds with
   `for (full = 0; full < 2 - only_full; full++)` (1277) and labels the line
   `full || only_full ? "full" : "some"` (1291). `only_full` is set to `res == PSI_IRQ`
   (1273-1275), so **cpu, memory and io print a `some` line and a `full` line, while IRQ prints
   only a `full` line**. The per-resource entry points confirm the resource mapping:
   `psi_io_show` → `PSI_IO` (1538-1540), `psi_memory_show` → `PSI_MEM` (1543-1545),
   `psi_cpu_show` → `PSI_CPU` (1548-1550), `psi_irq_show` → `PSI_IRQ` (1684-1686).
2. **System CPU `full` is undefined, not zero-valued evidence.** The kernel still *prints* a
   `full` line for system CPU, but the values are a hard-coded zero: the copy-out is guarded by
   `if (!(group == &psi_system && res == PSI_CPU && full))` under the comment
   "CPU FULL is undefined at the system level" (1282-1283), so `avg` and `total` stay at their
   initialised zero (1286-1288). A reader must therefore label that line undefined and must
   never read it as "no stall".
3. **The disabled-PSI return path.** `psi_show` returns `-EOPNOTSUPP` when the `psi_disabled`
   static branch is on (1257-1258). It returns the same errno for the IRQ resource when
   `irqtime_enabled()` is false (1260-1263) — a **second, distinct cause** of the same errno.
   The write path has the same guard (1578-1579) and the trigger path returns
   `ERR_PTR(-EOPNOTSUPP)` (1348-1349).
4. **Where the `/proc/pressure/*` entries are created.** `psi_proc_init` (1710-1721) creates
   the directory once (`proc_mkdir("pressure", NULL)`, 1713) and the entries
   `pressure/io` (1714), `pressure/memory` (1715), `pressure/cpu` (1716), and — only under
   `CONFIG_IRQ_TIME_ACCOUNTING` — `pressure/irq` (1717-1719). The whole block is guarded by
   `if (psi_enable)` (1712), and `psi_enable` is the `psi=` boot switch (149-158) that also
   drives `psi_init` (228-235).
5. **The printed line grammar.** The kernel's format is
   `"%s avg10=%lu.%02lu avg60=%lu.%02lu avg300=%lu.%02lu total=%llu\n"` (1290) — one kind
   token, three averages with exactly two fractional digits, and `total` converted from
   nanoseconds to **microseconds** by `div_u64(..., NSEC_PER_USEC)` (1286-1288).

**Does NOT support (explicit limits for the L1 and for the C2 knowledge note):**

- **Not a threshold, verdict or calibration source.** The file contains no `avg10` threshold, no
  `--warn-avg10` value, no `PRESSURE_OK|HIGH|PARTIAL|UNAVAILABLE` vocabulary, no exit codes and
  no selftest. The contract's default threshold of 10.0 is the lane's own local, uncalibrated
  choice and is **not** taught here.
- **Not a source for the delta/interval rule.** `total_delta_us`, `stall_ratio` and the
  `counter_regressed` state are tool-side derivations over two reads; the kernel file states
  only that `total` is a cumulative microsecond counter (1286-1288). A decreasing total is not
  described by the kernel at all.
- **Not a source for the malformed-detection rule.** The kernel emits a fixed grammar; the
  "duplicate kinds / missing required kinds → malformed" rule is the tool's own parsing policy,
  not kernel behaviour.
- **Not cgroup scope.** `kernel/sched/psi.c` implements the **system** `/proc/pressure/*`
  files; per-cgroup `cpu.pressure` / `memory.pressure` / `io.pressure` / `irq.pressure` files
  live in the cgroup code and are not in this file. S002 (and the round-24 cgroup-v2 seat) own
  that territory.
- **Not a statement about this host.** The file is v7.2 source; the live host's kernel version
  and configuration are separate facts (`ScoutHostKernelConfig` owns that). The live
  `/proc/pressure/*` read in §2 is one observation, not a version claim.
- **Not the IRQ-disabled trigger semantics.** `psi_trigger_create` rejects a non-`PSI_IRQ_FULL`
  state for the IRQ resource with `-EINVAL` (1364-1367) and the trigger/poll plumbing is
  separate from the read path; nothing here is a trigger-lifetime authority (S001 keeps that).
- **Not version-general.** Anchors and digest are v7.2-only.

## 8. Findings reported to the canonical Rust judge (verbatim, no interpretation added)

1. `psi_show` prints `some` and `full` for cpu/memory/io and **only `full`** for IRQ:
   `only_full = res == PSI_IRQ;` (1274) with `for (full = 0; full < 2 - only_full; full++) {`
   (1277) and the label `full || only_full ? "full" : "some"` (1291).
2. The system CPU `full` line is printed but its values are a fixed zero:
   `/* CPU FULL is undefined at the system level */` (1282) with
   `if (!(group == &psi_system && res == PSI_CPU && full)) {` (1283).
3. `psi_show` has **two** `EOPNOTSUPP` return paths: the global `psi_disabled` branch
   (1257-1258) and the IRQ-specific `!irqtime_enabled()` branch (1260-1263).
4. `/proc/pressure/*` entries are created in exactly one place, `psi_proc_init` (1710-1721),
   under `if (psi_enable)` (1712); `pressure/irq` exists only under
   `CONFIG_IRQ_TIME_ACCOUNTING` (1717-1719). `psi_enable` is the `psi=` boot switch
   (`__setup("psi=", setup_psi);`, 158) and the same value makes `psi_init` enable the
   `psi_disabled` branch (228-235).
5. Consequence for the C2 contract's error mapping: with PSI switched off by the boot
   parameter, the *entries are never created*, so the observable state is **absent (ENOENT)**,
   not an `EOPNOTSUPP` read. `EOPNOTSUPP` from these files is the defensive read-time guard and,
   for IRQ, the "IRQ time accounting off" case. A tool that labels every `EOPNOTSUPP` as
   "PSI disabled" over-claims for the `irq` resource; the mapping should be stated as
   "unsupported/unavailable", with the cause left open in `notes`.
6. `irqtime_enabled()` is a runtime static branch `sched_clock_irqtime` when
   `CONFIG_IRQ_TIME_ACCOUNTING` is built and a constant `0` otherwise
   (`kernel/sched/sched.h:3492-3495`, `3518-3521`). This seat did **not** locate the site that
   enables that branch at runtime, so no claim is made about when the IRQ `EOPNOTSUPP` is
   reachable — an open limit, not a conclusion.
7. The kernel's `total` is a cumulative **microsecond** stall counter
   (`div_u64(..., NSEC_PER_USEC)`, 1286-1288) and the averages are printed with exactly two
   fractional digits (`%lu.%02lu`, 1290) — consistent with the contract's line grammar, which
   the tool may accept more loosely than the kernel emits.

## 9. Out of scope for this seat (not done, deliberately)

- No edit to `corpus/SOURCES.md`, `corpus/lessons/round-24.md`, `corpus/knowledge/`, `SKILL.md`
  or any other lane file. **Draft only.**
- No `git`/`jj` mutation in the lane repo; no `git add/commit/stash/checkout/reset/pull/push`;
  no mutating `jj` command. Read-only `git status --porcelain` and `git diff --stat` were used
  to show the lane is unmodified (both clean for tracked files).
- The validator falsifier runs used **copies of the lane under `/tmp`**; the lane repository was
  never the target of a write.
- No host writes to `/proc`, `/sys` or cgroup files; no PSI trigger registration; no service or
  package change; no restart of anything. The only host interaction was reading
  `/proc/pressure/*`.
- No fetch of `Documentation/accounting/psi.rst`, `cgroup-v2.rst`, `init/Kconfig`,
  `kernel-parameters.txt`, `proc_pressure(5)` or `psi_types.h` as *sources* — those are other
  seats' surfaces. (`init/Kconfig` was not fetched by this seat either; the SOURCES.md rows
  read for context were read, not opened.)
- No tool installs or upgrades were needed; **nothing was installed** (no pacman transaction,
  no `uv tool install`, no release binary). Tools used, all pre-installed: `curl 8.23.0`,
  `sha256sum`, `cmp`, `grep`, `awk`/`sed` for numbered reads, `python3` 3.14.8 (stdlib only,
  for assembling the `/tmp` validator fixtures), and the repo's own
  `scripts/sources-census.sh` (bash + gawk, read-only in `validate` mode).

## 10. Artifact paths

- Fetched bytes (outside the lane repo):
  `/fast/scratch/hyaku/mori-r24-a2/srcpsic/psi.c` and `psi.c.refetch`
  (both sha256 `452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5`).
  Supporting cross-reference reads kept beside them: `ksched.h` (kernel/sched/sched.h),
  `core.c` (kernel/sched/core.c) — supporting reads only, no row proposed from them.
- Validator fixtures (throwaway, outside the lane repo): `/tmp/mori-srcpsic-full/` (the four
  id/status/used-by cases), `/tmp/mori-srcpsic-test/` (the first partial-copy pass),
  `/tmp/mori-srcpsic-dup/` (the duplicate-id case) and `/tmp/mori-srcpsic-final/` (the final row
  text as it now stands in this report, re-validated: exit 0, no new finding attributable to
  the new row).
- This report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-24/w1/SrcPsiC.md`
  (the only file created inside the lane repo by this seat).
- Files read but not modified: `corpus/SOURCES.md`, `corpus/lessons/round-23.md` (Gate shape),
  `.ufo/waves/round-24/contract.md`, `.ufo/waves/round-24/wave1-spec.json`,
  `.ufo/waves/round-24/wave1-assignments.json`, `.ufo/waves/round-24/w1/SrcKconfig.md`
  (house style of a sibling scribe report).
