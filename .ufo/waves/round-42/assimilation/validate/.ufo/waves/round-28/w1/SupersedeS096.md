# SupersedeS096 — S096 changed in place: cell diff, bytes verdict, paste lines, counter state

seat: MoriR28.SupersedeS096 (leaf; no subagent dispatch; no background job)
lane: /home/vgpnk/Projects/shokunin/mori-shokunin
tip examined: 6ebd518f (round-27 verifier spot-check); lane HEAD at read time 079a47c (round-28 declaration)
scratch: /fast/scratch/hyaku/mori-r28/SupersedeS096/ (no lane writes; one clone under scratch; commits only in that clone)
lane writes by this seat: this report file only

## 0. Summary

- Exactly one cell of S096 differs from its first publication: the `teaches` cell. The in-place edit is commit
  `7c77fba` (round-24 wave-2, "S096 teaches"). All ten other cells are byte-identical.
- The first-published `teaches` cell is **false against the commit's own bytes**: it says an absent irq file "is a
  build-configuration fact", and the commit's `psi_proc_init()` hunk creates `pressure/irq` inside `if (psi_enable)`
  as well as inside `#ifdef CONFIG_IRQ_TIME_ACCOUNTING`. Round 24's own wave-2 seats said so and asked for a
  superseding row; round 24 edited the cell in place instead (CORPUS.md Rules 2 breach).
- Re-opened today (2026-10-22T17:59:57Z): the commit patch, the v6.1 result `kernel/sched/psi.c`, and the v6.0
  `kernel/sched/psi.c`. Every statement S145 makes was checked against those bytes (section 3).
- Ready-to-paste: the restored first-published S096 row (section 5) and one new row **S145** (section 4).
- Scratch-verified: `sources-census.sh validate` exits 0 with only the six pre-existing W04 warnings; the round-27
  QUALITY 81 check drops S096 from its changed list; the round-28 C1 counter's own superseding test accepts S145.
- **Open conflict for the L1 (section 7):** QUALITY 81 (restore the first-published bytes) and QUALITY 77 (the
  superseded wording must be removed, not shadowed) cannot both hold for this row, because the first-published
  wording is the false one. The contract's C1 forces the restore, so the resolution is the L1's to log.

## 1. First-published cells versus the tip

First commit carrying `| S096 |` in `corpus/SOURCES.md`:

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --reverse --format='%H %ad %s' --date=iso -S'| S096 |' -- corpus/SOURCES.md
df4db54a341f396271ea39be9e3db47ac794eb73 2026-10-22 05:45:30 -0300 round-24: sources S090-S097, system pressure knowledge entry, lesson, evidence
```

The row sits at line 102 at `df4db54` and at line 102 at `6ebd518f`. Cell split (11 cells) at both revisions:

| # | cell | df4db54 (first published) | 6ebd518f (tip) | differs |
|---|---|---|---|---|
| 1 | id | S096 | S096 | no |
| 2 | source | Linux sched/psi: Add PSI_IRQ to track IRQ/SOFTIRQ pressure — https://github.com/torvalds/linux/commit/52b1364ba0b105122d6de0e719b36db705011ac1 | same | no |
| 3 | kind | code | code | no |
| 4 | tier | A | A | no |
| 5 | scope | upstream introduction of the IRQ/softirq pressure resource: the /proc/pressure/irq file, the cgroup irq.pressure file, and the full-only reporting rule; the introduction commit only, not later PSI behaviour | same | no |
| 6 | anchor | kernel/sched/psi.c psi_account_irqtime(), psi_irq_proc_ops and psi_show() only_full; include/linux/psi_types.h PSI_IRQ / PSI_IRQ_FULL; kernel/cgroup/cgroup.c irq.pressure; commit 52b1364ba0b105122d6de0e719b36db705011ac1 (authored 2022-08-26, committed 2022-09-09, merged into v6.1-rc1 by bd9a3dba185c on 2022-10-14; absent from the v6.0 psi.c history, first release Linux 6.1); commit pages opened 2026-10-22T08:15:40Z | same | no |
| 7 | **teaches** | …so an absent irq file is a **build-configuration fact** and never a zero reading. | …so an absent irq file is never a zero reading; it is consistent with no IRQ time accounting at build, PSI disabled at boot (the commit gates the file under psi_enable), or a kernel older than 6.1. | **yes** |
| 8 | status | mined | mined | no |
| 9 | opened | 2026-10-22 | 2026-10-22 | no |
| 10 | recheck | on-release | on-release | no |
| 11 | used-by | corpus/knowledge/system-pressure-r24.md, corpus/lessons/round-24.md | same | no |

Only the `teaches` cell changed. The in-place edit is `7c77fba` (2026-10-22 06:11:03 -0300, "round-24: wave-2 source
corrections (S093 anchor, S096 teaches, S097 cells)"); its diff shows one `-| S096 | …` line and one `+| S096 | …`
line. The edit was logged in the round-24 lesson (`corpus/lessons/round-24.md:40-42`) but was made in the row, not
in a new row.

The defect and the fix the lane itself named in round 24, unapplied:

- `.ufo/waves/round-24/w2/ReopenS094S097.md:12` — "Fails on \"absent irq file is a build-configuration fact\" (F1)",
  verdict "Overclaim, Medium (F1)"; `:21` — "an absent irq file has at least three causes: a boot-time disable
  (`psi=0`, or CONFIG_PSI_DEFAULT_DISABLED without `psi=1`), no CONFIG_PROC_FS, or no CONFIG_IRQ_TIME_ACCOUNTING.
  The teaches cell names only the last."; `:25` — the fix text.
- `.ufo/waves/round-24/w2/ReviewSourcesShape.md:87` — "Fix: add a row \"supersedes S096 —\" that keeps the true part
  (the irq file exists only when CONFIG_IRQ_TIME_ACCOUNTING is built) and drops \"a build-configuration fact.\""
- Routed later: `corpus/lessons/round-27.md:35` (M2: "S096 (teaches) … against its first-published text at
  `df4db54`"), `corpus/lessons/round-27.md:128` (carried), `corpus/lessons/round-27-verifier-spotcheck.md:133` and
  `:148` (routed defect 3).

## 2. Sources re-opened today (ordinary curl; no bot challenge)

| URL | accessed (UTC) | HTTP | bytes | sha256 | file |
|---|---|---|---|---|---|
| https://github.com/torvalds/linux/commit/52b1364ba0b105122d6de0e719b36db705011ac1.patch | 2026-10-22T17:59:57Z | 200 | 8899 (282 lines) | a255f4471b9388ba3d5bfdf64a093dec35a66cd8080473fb4bd2d4b49dce7cd6 | scratch `psiirq.patch` |
| https://raw.githubusercontent.com/torvalds/linux/v6.1/kernel/sched/psi.c | 2026-10-22T18:01:19Z | 200 | 43235 (1537 lines) | f3038de87e41da91a1050093d367084c201e68784336de24e1428d3b0db67ab6 | scratch `v6.1-psi.c` |
| https://raw.githubusercontent.com/torvalds/linux/v6.0/kernel/sched/psi.c | 2026-10-22T18:01:36Z | 200 | 39513 (1403 lines) | 126479b39bc86ac4c27cbd5c134266eb03b5d3fa9333df22eda4314a870790aa | scratch `v6.0-psi.c` |

Not fetched: `https://raw.githubusercontent.com/torvalds/linux/v6.1/include/linux/psi_types.h` — HTTP 429 (rate limited)
on two attempts. The `psi_types.h` claims are therefore anchored to the patch hunks (`:58-60`, `:69-71`), not to a
fetched v6.1 header. Gap, stated.

## 3. Claim-by-claim verdicts (against the bytes in section 2)

| # | statement | bytes | verdict |
|---|---|---|---|
| 1 | scope: the commit introduces the /proc/pressure/irq file | patch `:250-262`: `proc_create("pressure/irq", 0666, NULL, &psi_irq_proc_ops);` at `:258` | holds |
| 2 | scope: the commit introduces the cgroup irq.pressure file | patch `:111-120` (cftype `.name = "irq.pressure"` at `:113`), handlers `:87-102` | holds |
| 3 | scope: the commit introduces the full-only reporting rule | patch `:190-194` (`only_full = res == PSI_IRQ;` `:191`, `for (full = 0; full < 2 - only_full; full++)` `:194`), label `:202-203` | holds |
| 4 | scope: the introduction commit only, not later PSI behaviour | the patch touches 6 files (`:24-30` diffstat) and no later behaviour | holds |
| 5 | first-published teaches: "no some line for irq exists and its absence is by design" | commit message `:15-17`; `only_full` `:191-194`, `:202-203` | holds |
| 6 | first-published teaches: "the resource and its file are compiled in only under CONFIG_IRQ_TIME_ACCOUNTING" | patch `:58-60` (PSI_IRQ), `:69-71` (PSI_IRQ_FULL), `:144-145`, `:257-259`, `:87`; v6.1 psi.c `:1529` | holds |
| 7 | **first-published teaches: "an absent irq file is a build-configuration fact"** | patch `:250-252`: `static int __init psi_proc_init(void)` / `{` / `if (psi_enable) {`; v6.1 psi.c `:145-154` (`psi_enable`, `setup_psi`, `__setup("psi=")`), `:202-206` (`psi_init` returns when `psi_enable` is false), `:1524` (`if (psi_enable) {`), `:1529-1530`; v6.1 psi.c `:1353-1537` (the whole block under `#ifdef CONFIG_PROC_FS`) | **fails**: the file is absent for at least three reasons, not one |
| 8 | first-published teaches: "never a zero reading" | no upstream text; it is the lane's own rule (`.ufo/waves/round-24/w2/ReopenS094S097.md:23`) | not upstream text; keep it as a lane rule, marked as such |
| 9 | tip teaches: "consistent with no IRQ time accounting at build, PSI disabled at boot (the commit gates the file under psi_enable), or a kernel older than 6.1" | v6.1 psi.c `:145-149` (CONFIG_PSI_DEFAULT_DISABLED → `static bool psi_enable;` else `= true`), `:150-154` (`psi=1`/`psi=0` via `setup_psi`), `:202-206`; patch `:250-252` | holds |
| 10 | version bound: the resource first ships in Linux 6.1 | v6.0 psi.c has **no** `PSI_IRQ`, no `psi_account_irqtime`, no `pressure/irq` (grep over all 1403 lines: no match); v6.1 psi.c has all three (`:914-915`, `:937`, `:1530`) | holds, verified today |
| 11 | old anchor: "merged into v6.1-rc1 by bd9a3dba185c on 2022-10-14" | not re-opened today (the merge page was not fetched); the file-level bound in row 10 is verified | carried from round 24, not re-verified here |

Located quotes (verbatim, ≤25 words, with line numbers in the fetched bytes):

- patch `:15-17` (commit message ¶4), 25 words: "IRQ/SOFTIRQ always happen in the current task on the CPU, make nothing productive could run even if it were runnable, so we only use PSI_IRQ_FULL."
- patch `:11-13` (commit message ¶3), 25 words: "When CONFIG_IRQ_TIME_ACCOUNTING, we can get IRQ/SOFTIRQ delta time from update_rq_clock_task(), in which we can record that delta to CPU curr task's cgroups as PSI_IRQ_FULL status."
- v6.1 psi.c `:1524` and `:1530`: "if (psi_enable) {" … "proc_create("pressure/irq", 0666, NULL, &psi_irq_proc_ops);"

## 4. Ready-to-paste row S145

Insert after the S144 row (`corpus/SOURCES.md:150` at the tip). Scope is kept **verbatim** from S096: it holds against
the bytes (rows 1-4 above) and keeping the same scope keeps the census E04 exemption in force instead of adding a
W04 "duplicate url across scopes" warning (section 6). The anchor is corrected: the old anchor carried no line
numbers and a stale access time; the new one carries located line numbers, the digests and today's access time.

```
| S145 | Linux sched/psi: Add PSI_IRQ to track IRQ/SOFTIRQ pressure — https://github.com/torvalds/linux/commit/52b1364ba0b105122d6de0e719b36db705011ac1 | code | A | upstream introduction of the IRQ/softirq pressure resource: the /proc/pressure/irq file, the cgroup irq.pressure file, and the full-only reporting rule; the introduction commit only, not later PSI behaviour | commit patch https://github.com/torvalds/linux/commit/52b1364ba0b105122d6de0e719b36db705011ac1.patch (sha256 a255f4471b9388ba, 282 lines, opened 2026-10-22T17:59:57Z): message :11-13 (the CONFIG_IRQ_TIME_ACCOUNTING dependency) and :15-17 (only PSI_IRQ_FULL); include/linux/psi_types.h :58-60 (PSI_IRQ) and :69-71 (PSI_IRQ_FULL), each under #ifdef CONFIG_IRQ_TIME_ACCOUNTING; kernel/sched/psi.c :144-145 (psi_account_irqtime), :190-194 and :202-203 (only_full = res == PSI_IRQ; full or only_full prints "full"), :211-213 (an irq trigger is refused unless PSI_IRQ_FULL), :240 (psi_irq_proc_ops), :250-262 (psi_proc_init: if (psi_enable) :252, #ifdef CONFIG_IRQ_TIME_ACCOUNTING :257, proc_create("pressure/irq", 0666, NULL, and psi_irq_proc_ops) :258); kernel/cgroup/cgroup.c :87-102 (cgroup_irq_pressure_show and _write) and :111-120 (the irq.pressure cftype); kernel/sched/core.c :132 (psi_account_irqtime(rq->curr, irq_delta)); Documentation/admin-guide/cgroup-v2.rst :40-43 (irq.pressure); the v6.1 result kernel/sched/psi.c (sha256 f3038de87e41da9, 1537 lines, opened 2026-10-22T18:01:19Z): :145-154 (psi_enable, setup_psi, __setup("psi=")), :202-206 (psi_init returns when psi_enable is false), :914-915 and :937 (psi_account_irqtime; times[PSI_IRQ_FULL]), :1145 and :1160-1164 and :1178 (only_full), :1206-1209 (the trigger refusal), :1497-1498 and :1512 (psi_irq_show, psi_irq_proc_ops), :1522-1533 (psi_proc_init: if (psi_enable) :1524, #ifdef CONFIG_IRQ_TIME_ACCOUNTING :1529, proc_create("pressure/irq") :1530), :1353-1537 (the CONFIG_PROC_FS block); the v6.0 kernel/sched/psi.c (sha256 126479b39bc86ac4, 1403 lines, opened 2026-10-22T18:01:36Z) carries no PSI_IRQ, no psi_account_irqtime and no pressure/irq, so the resource first ships in Linux 6.1; commit 52b1364ba0b105122d6de0e719b36db705011ac1 authored 2022-08-26, committed 2022-09-09 | supersedes S096 — the old row's last clause called an absent irq file a build-configuration fact, which names one cause and contradicts the commit's own hunk: psi_proc_init() creates pressure/irq only inside if (psi_enable) and only under CONFIG_IRQ_TIME_ACCOUNTING, so the file is absent for at least three reasons — the option not built in, PSI switched off at boot (psi=0, or CONFIG_PSI_DEFAULT_DISABLED without psi=1), and a kernel older than 6.1 — and an absent file is never a zero reading. The full-only shape is upstream text, not a lane inference: psi_show() sets only_full = res == PSI_IRQ, so the irq resource prints the full line and no some line, because IRQ/softirq time is charged to the task running on the CPU. | mined | 2026-10-22 | on-release | corpus/knowledge/system-pressure-r24.md, corpus/lessons/round-24.md, corpus/lessons/round-24-verifier-spotcheck.md, corpus/lessons/round-27.md, corpus/lessons/round-27-verifier-spotcheck.md, PROVINCE.md, SKILL.md |
```

The block above is the complete row: one line, 11 cells, 3213 bytes, byte-identical to the single line of
`/fast/scratch/hyaku/mori-r28/SupersedeS096/row-S145.txt` (the file that was tested in the scratch clone, section 8).
Cell check: `teaches` opens exactly `supersedes S096 — ` (em dash), `status` `mined`, `opened` `2026-10-22`,
`recheck` `on-release` (S096's convention), `used-by` as listed in section 5.

## 5. Restored S096 row (first-published bytes, verbatim)

Replace `corpus/SOURCES.md:102` with these bytes. They are byte-identical to `df4db54:corpus/SOURCES.md:102`
(asserted equal in the scratch clone). S096's `status`, `recheck` and `used-by` at the tip equal the first-published
values, so nothing else in the row moves.

```
| S096 | Linux sched/psi: Add PSI_IRQ to track IRQ/SOFTIRQ pressure — https://github.com/torvalds/linux/commit/52b1364ba0b105122d6de0e719b36db705011ac1 | code | A | upstream introduction of the IRQ/softirq pressure resource: the /proc/pressure/irq file, the cgroup irq.pressure file, and the full-only reporting rule; the introduction commit only, not later PSI behaviour | kernel/sched/psi.c psi_account_irqtime(), psi_irq_proc_ops and psi_show() only_full; include/linux/psi_types.h PSI_IRQ / PSI_IRQ_FULL; kernel/cgroup/cgroup.c irq.pressure; commit 52b1364ba0b105122d6de0e719b36db705011ac1 (authored 2022-08-26, committed 2022-09-09, merged into v6.1-rc1 by bd9a3dba185c on 2022-10-14; absent from the v6.0 psi.c history, first release Linux 6.1); commit pages opened 2026-10-22T08:15:40Z | The irq resource is reported for the full state only, because IRQ/softirq time is charged to the task running on the CPU, so no some line for irq exists and its absence is by design; the resource and its file are compiled in only under CONFIG_IRQ_TIME_ACCOUNTING, so an absent irq file is a build-configuration fact and never a zero reading. | mined | 2026-10-22 | on-release | corpus/knowledge/system-pressure-r24.md, corpus/lessons/round-24.md |
```

`used-by` for S145 (the files that cite S096 at the tip, with the citing line):
`corpus/knowledge/system-pressure-r24.md` (`:1`, `:30`, `:41`, `:61`, `:110`, `:177`),
`corpus/lessons/round-24.md` (`:15`, `:31`, `:36`, `:40`),
`corpus/lessons/round-24-verifier-spotcheck.md` (`:25`, `:131`),
`corpus/lessons/round-27.md` (`:35`, `:128`),
`corpus/lessons/round-27-verifier-spotcheck.md` (`:133`, `:148`),
`PROVINCE.md:257`, `SKILL.md:619`.
(`corpus/SOURCES.md:102`, `:159` and `:195` also carry the id; the registry is not a used-by path.)

## 6. Gate line

| Row | URL | Accessed | Located quote | Decision |
|---|---|---|---|---|
| S145 | https://github.com/torvalds/linux/commit/52b1364ba0b105122d6de0e719b36db705011ac1.patch | 2026-10-22T17:59:57Z | patch `:15-17` (25 words): "IRQ/SOFTIRQ always happen in the current task on the CPU, make nothing productive could run even if it were runnable, so we only use PSI_IRQ_FULL." | admit, A, mined |

## 7. QUALITY 77 sweep — every place whose prose states the defective wording

`corpus/QUALITY.md:349` (criterion 77): a correction sweeps every mention in place; the superseded wording is removed,
not shadowed. The defective wording is "an absent irq file is a build-configuration fact". At `6ebd518f`:

| path:line | what it says | kind |
|---|---|---|
| `corpus/SOURCES.md:102` | the S096 row's own `teaches` cell | the defect; restored by this round, corrected by S145 |
| `.ufo/waves/round-24/w1/SrcPsiIrqCommit.md:112` | "…an absent irq file is a build-configuration" | **live false claim in a seat report** |
| `.ufo/waves/round-24/w1/SrcPsiIrqCommit.md:113` | "fact and must not be reported as a zero reading." | **live false claim in a seat report** |
| `.ufo/waves/round-24/w1/SrcPsiIrqCommit.md:161` | the drafted row `S0xx` carrying the defective `teaches` | **live false claim in a seat report** |
| `.ufo/waves/round-24/w1/CriticC2Semantics.md:169` | "an absent irq file is a permanent build-config state on kernels without `CONFIG_IRQ_TIME_ACCOUNTING`" | **live false claim in a seat report** |
| `.ufo/waves/round-24/w2/ReopenS094S097.md:12`, `:18`, `:21`, `:25` | quotes the claim to name it as F1 and gives the fix | falsification record — keep as it is |
| `.ufo/waves/round-24/w2/ReviewSourcesShape.md:38`, `:84`, `:87` | "overclaims (absent irq file)"; the quoted claim; the fix text | falsification record — keep as it is |
| `corpus/lessons/round-24.md:40` | logs the narrowing old → new | lesson history — keep as it is |

Places that already carry the corrected wording (these must stay, and they are what S145 agrees with):
`corpus/knowledge/system-pressure-r24.md:34-36` (P4), `:112-115` (F6), `:179` (decision table), `SKILL.md:630`,
`corpus/SOURCES.md:97` (S091's teaches: "a PSI switched off at boot leaves them absent rather than unreadable").

**Conflict for the L1 (decide, do not leave implicit).** QUALITY 81 requires the row to go back to its first-published
bytes, which puts the false wording back into `corpus/SOURCES.md:102`; QUALITY 77 requires the superseded wording to
be removed, not shadowed. The C1 counter forces the restore (`changed=0`), so the restore happens; the lane's
precedent for the same shape is the S124→S133, S090→S143 and S093→S144 restores (corrected teaching in the new row,
old → new logged in the lesson, `corpus/lessons/round-27.md:92-100` "Row changes logged old → new", the S124 bullet at
`:97-100`). What this case adds is that the restored text is false, not merely imprecise. Recommended sweep for the L1:
(a) log the old → new cells in the round-28 lesson in the S124 form; (b) add a dated correction block to the two
round-24 seat reports that state the claim as live (`SrcPsiIrqCommit.md`, `CriticC2Semantics.md`) or name them and
their disposition in the round-28 lesson, following the r26 D4 precedent (`corpus/lessons/round-27.md:109`); (c) leave
the two round-24 wave-2 falsification records and the round-24 lesson log untouched, because they quote the claim in
order to refute it. Whether the two live seat reports are rewritten or logged as history is the L1's call; this seat
did not write in the lane.

## 8. Checks run (scratch only; the lane was not modified)

Scratch clone: `/fast/scratch/hyaku/mori-r28/SupersedeS096/census-root/mori-shokunin` (`git clone --no-hardlinks` of
the lane at 079a47c), one commit `d57b2fc` holding the restored S096 row and the new S145 row. A minimal
`shokunin.conf` with the single `mori|mori-shokunin` row sits beside it.

- `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root <scratch-root> mori` → **exit 0**,
  six W04 warnings, all pre-existing (S035, S037, S073, S074, S075, S076); `mori ok …`.
- Control: the same tree with `supersedes S096 — ` removed from the S145 `teaches` → **exit 1**, `mori E04 S145
  duplicate url … within scope …`. The prefix is what keeps the census clean (`scripts/sources-census.sh:646-649`).
- QUALITY 81 check (the lane's `.ufo/waves/round-27/check-row-identity.py`, with its `LANE` constant repointed at the
  scratch clone): before → `changed S096 cells=teaches`, `changed S097 …`, `changed S101 …`, `rows=144 changed=3
  removed=0 bad=0`, exit 1; after → `changed S097 …`, `changed S101 …`, `rows=145 changed=2 removed=0 bad=0`, exit 1.
  S096 is no longer listed. S097 and S101 are other seats' items, outside this one.
- The round-28 C1 counter's own superseding test (the script's python block, run on the scratch `corpus/SOURCES.md`):
  `superseding=1 ids=S096` for this seat's row; the other seven owed ids (S097, S101, S127, S128, S129, S131, S140)
  are other seats' rows.
- Read-only in the lane: `bash .ufo/waves/round-28/count-c1.sh 6ebd518f` → `row_identity=rows=144 changed=3
  removed=0 bad=0`, `superseding=0/8 ids=none`, `C1=unmet`, exit 1 — the before state the contract declares.
- Byte equality asserted in the scratch clone: the restored row equals the first-published bytes (1242 bytes each).
- Observed in the lane working tree at 2026-10-22T18:31Z, **not** written by this seat: `corpus/SOURCES.md` already
  carries an S096 row whose eleven cells are all byte-equal to the first-published bytes (the restore of section 5 is
  already applied there), and the S097 and S101 lines are changed as well; `grep -c S145 corpus/SOURCES.md` = 0, so the
  S145 row of section 4 is still missing. `git diff --stat` in the lane also lists `.ufo/waves/round-27/contract.md`
  as modified. These are concurrent sibling-seat edits in the working tree, not committed bytes; the L1 owns them.

## 9. Out of scope, gaps, limits

- This seat owns S096 only. S097, S101, S127, S128, S129, S131 and S140 are other rows of C1 and are untouched here.
- `https://raw.githubusercontent.com/torvalds/linux/v6.1/include/linux/psi_types.h` returned HTTP 429 on two
  attempts; the `psi_types.h` anchors are the patch hunks, not a fetched v6.1 header.
- The merge commit `bd9a3dba185c` (v6.1-rc1, 2022-10-14) named in the old anchor was not re-opened; the file-level
  version bound (v6.0 has no `PSI_IRQ`, v6.1 has it) is verified today.
- The old anchor's "commit pages opened 2026-10-22T08:15:40Z" refers to the round-24 fetch of the rendered commit
  pages; today's fetch is the raw patch. S145 carries today's digest and access time.
- The full S145 row was not pasted into the report body by hand (section 4 explains why); it is the single line of
  `row-S145.txt`, which is the exact bytes tested in the scratch clone.
- No lane file was written except this report. No git or jj mutation in the lane, no host write, no service or package
  change, no unit started or stopped, no process signalled.

## 10. Tooling and privacy

- No installs and no updates. Versions used: bash 5.3.20, curl 8.23.0, git 2.56.0, Python 3.14.8, sha256sum 0.8.0,
  GNU Awk 5.4.1. The operator's agent rules file (`/home/vgpnk/.omp/agent/RULES.md`) was read; its tooling directive
  was followed (no tool was needed, so nothing was installed; all pacman transactions remain paused host-wide).
- Only read-only git was used in the lane (`show`, `log`, `rev-parse`, `grep`); `git clone --no-hardlinks` wrote only
  into the scratch tree, and the one commit exists only there.
- This report carries commit ids, URLs, digests, line numbers, row cells and counts only. No uid, pid, session id,
  unit name of this host's user session, settings value or command line.
