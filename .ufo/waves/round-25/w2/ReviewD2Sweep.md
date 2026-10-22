# ReviewD2Sweep — D2 correction sweep in `corpus/knowledge/system-pressure-r24.md` (diff `28b79d3d..tip`)

Seat: MoriR25.ReviewD2Sweep (falsify, leaf). Date 2026-10-22. Lane tip read: `90cc042f22ea7a7f492502b7210ccca49b8a8e88`.

## Verdict

**Held** for all five rewrites (K5, K4, P3, K3, P4) and for the routed-phrase sweep of the entry and its
sibling files (`corpus/README.md`, `SKILL.md`, `PROVINCE.md`). Every cited upstream anchor in the five
rewrites was re-checked against v7.2 bytes re-opened by curl, and every anchor is right; no sibling line
restates the superseded wording. **Three residual stale mentions remain in the entry** (S1–S3 below,
severity: minor each) — all are body-vs-corrections lags against the round-24 "Citations (minor)" bullet at
`corpus/knowledge/system-pressure-r24.md:42-44`, none restates the K3/K4/K5/P3/P4 old wording, and none was
introduced by the round-25 diff. One of them (S2) is not disclosed anywhere; the other two are partially
disclosed.

## What was opened and how

- Upstream, re-opened by curl this session into `/tmp/psi-v72/` (outside the lane), all
  `raw.githubusercontent.com/torvalds/linux/<tag>`: v7.2 `kernel/sched/psi.c` (1725 lines),
  `Documentation/accounting/psi.rst` (188), `include/linux/psi_types.h` (216),
  `Documentation/admin-guide/cgroup-v2.rst` (3524); plus `psi.c` at v5.12, v5.13, v5.18, v5.19, v6.0, v6.1;
  plus commits `890d550d7dba`, `e7fcd7622823`, `52b1364ba0b1` via the GitHub commits API.
- Lane diff `28b79d3d..HEAD` for the entry: 3 hunks (preamble `:10-13`, F4 `:97-102`, decision rows
  `:176-183`); 16 insertions, 10 deletions; no other PSI wording in the lane changed.
- Sweep instrument: regex over `corpus/**`, root `*.md` (incl. `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`,
  `LOG.md`), plus a semantic pass over every sibling line matching `(?i)psi|pressure|stall|avg10`. No `lsp`
  device exists in this session and Markdown has no language server, so no server answered the file — text
  grep is the sweep instrument, and no grep output below is offered as semantic proof of code behavior; all
  semantic checks cite the upstream bytes.
- Gate rerun (read-only, git objects only): `python3 -I -B tools/mori-routed-r24.py --repo . --rev HEAD` →
  `{"held":4,"items":4,"mismatches":0,"hygiene":{"held":true,...},"status":"held"}`, exit 0; D2 row held,
  detail `banner_in_whole_entry:false`, `corrections_sections:1`, `decision_table_data_rows:11` (base 11).
  Base check: `git show 28b79d3d:corpus/knowledge/system-pressure-r24.md` matches the four superseded
  phrases 4 times; at HEAD, 0 in the entry.

## Per-rewrite verification (all correct, with evidence)

1. **K5 — averages not refreshed on each read** (entry `:20-21` bullet, `:97-102` F4 body).
   - `psi.c:1268` `collect_percpu_times(group, PSI_AVGS, NULL);` runs inside `psi_show` on **every** read
     (collects the totals) — matches "Each read collects the totals".
   - `psi.c:1269-1270` `if (now >= group->avg_next_update) group->avg_next_update = update_averages(group, now);`
     — the averages are recomputed on a read **only** when the 2-second update is due. Exact.
   - `psi.c:160-164` contains `#define PSI_FREQ (2*HZ+1) /* 2 sec intervals */` (at `:161`) and the EXP_*
     constants. `psi.c:600-602` is the averages work item's own due-time gate
     (`psi_avgs_work` at `:578`, gate at `:600-602`). Both secondary anchors check out.

2. **K4 — a short spike is counted, not invisible** (entry `:19` new corrections bullet, `:176` row 1,
   `:190-193` Limits, already correct at base).
   - `psi.c:409-411` `group->total[aggregator][s] += div_u64(deltas[s], max(nonidle_total, 1UL));` — the
     spike lands in `total`. `psi.c:342-360` is `calc_avgs()` decaying via `calc_load`/`EXP_10s/60s/300s`;
     `psi.c:551` `sample = group->total[PSI_AVGS][s] - group->avg_total[s];` and `psi.c:572`
     `calc_avgs(group->avg[s], missed_periods, sample, period);` — folded into the averages at the next due
     update. `psi.rst:60-65` ends "…to allow detection of latency spikes which wouldn't necessarily make a
     dent in the time averages" — the exact upstream warrant for "may leave `avg10` under the threshold".
     All four cited anchors verified.

3. **P3 — `some: null` for irq means not tracked** (entry `:30-32` bullet, `:177` row 2).
   - `psi_types.h` v7.2 `enum psi_states`: `PSI_IO_SOME … PSI_CPU_FULL`, then `PSI_IRQ_FULL` under
     `CONFIG_IRQ_TIME_ACCOUNTING`; there is **no** IRQ `some` state (S095 ✓).
   - Commit `52b1364ba0b1` ("sched/psi: Add PSI_IRQ to track IRQ/SOFTIRQ pressure"): "Note we don't use
     PSI_IRQ_SOME since IRQ/SOFTIRQ always happen in the current task on the CPU … so we only use
     PSI_IRQ_FULL" (S096 rationale ✓; committer date 2022-09-09 → 6.1 cycle, matching "first shipped in
     Linux 6.1").
   - "undefined" is psi.rst's word for system CPU `full` only: `psi.rst:57` "CPU full is undefined at the
     system level" ✓. The row's new `[UNKNOWN]` anchor `psi.c:1017` is `if (!curr->pid) return;` inside
     `psi_account_irqtime` (charge at `:1040`) — "charges IRQ time only to a non-idle current task" holds.

4. **K3 — version scope for system CPU `full` / `malformed`** (entry `:15-18` bullet; rows `:178`, `:182`).
   - v5.12 `psi_show`: `for (full = 0; full < 2 - (res == PSI_CPU); full++)` — pre-5.13 kernels print **no**
     CPU `full` line at all (a genuine pre-5.13 cpu file reads `malformed` under required-kinds ✓).
   - v5.13: `for (full = 0; full < 2; full++)` — line appears (matches psi.rst:57-58 "reported since 5.13");
     v5.18 has no zeroing guard; v5.19 has it (`psi.c:1067-1068` "/* CPU FULL is undefined at the system
     level */"), as does v7.2 (`psi.c:1282-1288`).
   - Commit `890d550d7dbac7a31ecaa78732aa22be282bb6b8` exists; subject "sched/psi: report zeroes for CPU full
     at the system level"; committer date 2022-04-22 (5.19 cycle) — "zeroing arrived in 5.19" ✓.

5. **P4 — no decrement path; missing-file causes** (entry `:33-36` bullet; rows `:179`, `:183`; F10
   `:153-156` at base already carried `[INFERENCE]`).
   - The only write to `group->total` in v7.2 `psi.c` is the `+=` at `:410-411`; every other `->total[` site
     (467, 551, 619-620, 724, 1286, 1395) is a read. "No decrement path" ✓, and the `[INFERENCE]` label on
     "not comparable" is the honest strength.
   - Causes: `psi_proc_init` (`psi.c:1710-1721`) creates the files only when `psi_enable` → boot-disabled
     removes all files; `pressure/irq` only under `CONFIG_IRQ_TIME_ACCOUNTING` (`:1717-1719`); `pressure/irq`
     is absent from v6.0 `psi.c` and present at v6.1 `:1530` → "a kernel older than 6.1 (irq only)" ✓;
     CONFIG_PSI absence (S093) and `--root` elsewhere are tool/kernel facts.

6. **Banner/preamble** (entry `:10-13`). "Where this section and a later line disagree, this section wins" is
   gone; the replacement sentence ("in round 25 the K3, K4, K5, P3 and P4 body rows were corrected in place")
   is accurate — each of the five carries an in-place marker (K3 `:178`,`:182`; K4 `:176`; K5 `:102`; P3
   `:177`; P4 `:179`,`:183`). Gate detail confirms the phrase is absent from the whole normalized entry.

## Sibling-file sweep (QUALITY #77, `corpus/QUALITY.md:349-354`)

Every sibling line mentioning PSI/pressure was read; **none restates the superseded wording**:

- `corpus/README.md:449` (round-24 coverage row) and `:457-479` (frontier note): "System CPU `full` is
  reported undefined…", "`irq` carries `full` only, so its absent `some` is expected, not malformed",
  "no cause is inferred from it" — all agree with the P3/P4-corrected entry.
- `SKILL.md:611-634`: `:625` cites `psi.rst:57-58` (exact range) for the CPU-`full` zero; `:628` irq
  full-only; `:630` already carries the P2-scoped EOPNOTSUPP reachability; `:634` never infers "pressure
  fell" from a decreasing counter — consistent with P4 without restating its superseded form.
- `PROVINCE.md:55`, `:236-258`, `:282-283`: consistent; the round-25 appended note (`:292+`) is C2-only and
  carries no PSI wording.
- Mentions of the old wording that are historical records, not restatements (allowed): 
  `corpus/lessons/round-24-verifier-spotcheck.md:139-143` (the defect text), `corpus/lessons/round-25.md:82-84`
  (the fix record), `corpus/QUALITY.md:351` (the rule naming the banned banner), `SCORECARD.md:1555`
  (before/after row), `.ufo/waves/round-25/w1/D2KnowledgeFix.md` (wave-1 patch report).

## Remaining stale mentions (path:line, severity, smallest fix)

All three are in the entry, predate round 25, and lag the round-24 "Citations (minor)" bullet at `:42-44`.
None is among the five routed rows; the routed D2 gate cannot see them (its four phrases are absent).

- **S1 (minor).** `corpus/knowledge/system-pressure-r24.md:89` and `:148` cite `psi.c:1538-1550` where the
  corrections bullet (`:42`) gives the readers as `psi.c:1540,1545,1550` plus the irq reader at `psi.c:1686`.
  Verified: the three non-irq readers sit at 1540/1545/1550 (functions 1538-1551); the irq reader is at 1686
  — the cited range omits it. *Disclosed* in `corpus/lessons/round-25.md:83-84` ("Not fixed: two F3 citation
  ranges"). Smallest fix: cite `psi.c:1540,1545,1550` + `1686` (or function ranges `1538-1551` and
  `1684-1687`).
- **S2 (minor).** `corpus/knowledge/system-pressure-r24.md:143` — "The cgroup v2 documentation **lists
  `irq.pressure` beside `cpu`, `io` and `memory.pressure`** … (S092, `cgroup-v2.rst:1066-1087`)" vs the
  corrections bullet (`:43`) "the cgroup files sit in separate sections of cgroup-v2.rst (1083, 1215, 1911,
  2171)". Verified in v7.2 cgroup-v2.rst: `1066-1087` holds `cgroup.pressure` (~1066-1081) and
  `irq.pressure` (~1083-1087); `cpu.pressure` is at ~1215, `memory.pressure` at ~1911, `io.pressure` at
  ~2171 — separate controller sections, not "beside" and not inside the cited range. The superseded
  single-range wording stands uncorrected and is **not disclosed** in the round-25 lesson. Smallest fix:
  reword to "documented in separate sections (irq 1083, cpu 1215, memory 1911, io 2171); `cgroup.pressure`
  at ~1066-1081".
- **S3 (minor).** `corpus/knowledge/system-pressure-r24.md:158` — F11 "The **kernel source** defines no
  'warn at N %' rule" is unscoped, vs the corrections bullet (`:43-44`) scoping the claim to `psi.c` and
  `psi.rst`, the files read. **Not disclosed.** Smallest fix: "no threshold rule in `psi.c` or `psi.rst`, the
  files read".

None of S1–S3 states a false kernel fact at v7.2 except S2's locality implication ("beside"); the defect
class is QUALITY #77's "superseded wording is removed, not shadowed" applied to the Citations bullet.

## Residual risk and verification gaps

- The D2 gate reads only the entry; sibling paraphrases are invisible to it by construction (contract A3
  reports, does not count). This report is that sibling sweep.
- Upstream identity: sources are GitHub-served tag bytes; the cross-tag greps (v5.12/5.13/5.18/5.19/6.0/6.1)
  and three commit lookups corroborate the tag contents, but no second mirror was fetched.
- Wave-1's `D2KnowledgeFix.md` patch text differs from the landed diff (its preamble wording, and it
  deliberately left the K3/P4 rows untouched); the landed diff is the superset and was verified hunk-by-hunk
  against the current bytes.
- Not re-run here: the pressure tool's own selftest (D1's measurement, already exercised by the gate rerun's
  D1 row) — outside this seat's item.

## Tooling record

No tools installed or upgraded (`curl`, `git`, `python3` already present and sufficient). No lane writes
except this report; `/tmp/psi-v72/` scratch copies live outside the lane. No `jj` or git-mutating command was
run; only read-only `git show/rev-parse/merge-base/diff` in the lane.
