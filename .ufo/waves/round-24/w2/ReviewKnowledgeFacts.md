# ReviewKnowledgeFacts: round 24, wave 2, facts F1 to F6

Seat: MoriR24.ReviewKnowledgeFacts (leaf reviewer, no subagents, no mutants run).
Target: `corpus/knowledge/system-pressure-r24.md`, facts F1 to F6.
Reference: Linux v7.2 tag files (`Documentation/accounting/psi.rst`, `kernel/sched/psi.c`, `init/Kconfig`,
`include/linux/psi_types.h`), plus the other copies named in section 7. Scratch copies live in
`/fast/scratch/hyaku/mori-r24-a2/w2/ReviewKnowledgeFacts/`.

Conventions: `psi.c` means kernel/sched/psi.c at v7.2 unless a version is named. Entry line numbers refer to
lane HEAD `1046aca` (short hash) at the time of review. The F1 to F6 body text there is identical to the copy I first
audited (section 1).

## 0. Result

- **Quotes: 20 of 20 pass.** Every quoted string and code span in F1 to F6 that carries a line anchor appears
  in the v7.2 text after whitespace normalisation. Differences are line wraps and marked "…" elisions only.
  Identifiers were checked by grep. Three paraphrases were checked by location and are accurate.
- **Anchors: 19 line anchors.** 4 are exact or acceptable, 13 are loose (they contain the target plus unrelated
  lines), and 2 are wrong or incomplete: the F3 reader list and the F5 add anchor. Section 3 gives each correct anchor.
- **Claims: 2 literal errors, both still in the body at HEAD.** F4 "refreshed on each read" is wrong for the averages.
  F5 "adds only to `PSI_IRQ_FULL`" is wrong as literally written. The correction preamble fixes F4 and the F3 reader
  list, but the body still says the old thing. Nothing corrects the F5 sentence.
- **Inferences: 3 unlabeled** in F1 to F6 (lines 66 to 67, line 87, line 104).
- **Version scope: 2 headings need a qualifier.** F3 "the kernel writes zeros there" holds only from v5.19.
  F2 "each documented file holds two lines" holds for cpu only from v5.13.
- **Process: the measured tip is not the lane HEAD.** The tip is a730ecfe. HEAD is now 1046aca. The C2 tool and
  its fixtures changed after the tip (section 5). The C2 numbers declared at the tip do not carry over to HEAD
  without re-measurement.

Severity legend: Medium means a false or misleading claim. Low means a loose or incomplete anchor, a missing
qualifier, or an unlabeled inference. Note means adjacent material outside F1 to F6.

## 1. Versions reviewed

| Label | Commit | Entry sha256 (prefix) | Lines | Relation |
|---|---|---|---|---|
| Measured tip | a730ecfe (committed 05:56:21) | addc4f5f | 196 | F1 to F6 body defects present |
| Audited working copy | a536b18 plus an uncommitted F1 fix | 70731a7b | 227 | F1 to F6 body identical to the tip except the F1 Kconfig anchor |
| Current HEAD, identical to working copy | 1046aca | 4f8a0fd1 | 232 | F1 to F6 body identical to the audited copy; one new provenance bullet at lines 34 to 37 |

Timeline: the tip was committed at 05:56:21. HEAD a536b18 was committed at 06:05:01. The working copy was last
written at 06:05:55 and carries the F1 fix. HEAD then moved to 7c77fba and 1046aca while this review ran.

## 2. Findings by severity

### Medium

**M1. F4, lines 94 to 95: "refreshed on each read" is wrong for the averages.**
- `psi.c:1268` runs `collect_percpu_times`, which folds per-CPU times into the totals on every read.
- `psi.c:1269-1270` recomputes the averages only when `now >= group->avg_next_update`.
- The averages work item (`psi.c:600-602`) recomputes them on its own schedule.
- The preamble (K5, lines 17 to 18) says this correctly, but the body still contradicts it.
- Replacement text: "Each read folds the per-CPU times into the totals (`psi.c:1268`). The averages are recomputed on a
  read only when `now >= group->avg_next_update` (`psi.c:1269-1270`), and otherwise by the averages work item
  (`psi.c:600-602`)."

**M2. F5, line 101: "The IRQ accounting path adds only to `PSI_IRQ_FULL`" is false as written.**
- `psi.c:1039` calls `record_times(groupc, now)` before the IRQ add.
- `record_times` adds elapsed time to every bucket named in `state_mask` (`psi.c:771-790`: IO, MEM and CPU, each
  some and full, and NONIDLE).
- The IRQ delta itself goes only to `PSI_IRQ_FULL` (`psi.c:1040`).
- The cited range `psi.c:1032-1042` is the wrong window. The function spans `psi.c:1005-1047`.
- Replacement text: "The IRQ delta is added only to `PSI_IRQ_FULL` (`psi.c:1039-1040`). The same call first flushes
  elapsed time into the states named in `state_mask` (`psi.c:771-790`)."

**M3. F3, lines 85 to 86: the reader anchor is incomplete.**
- The claim "All four `/proc/pressure/*` readers pass the system group" is true.
- The cited range `psi.c:1538-1550` covers three readers: io at 1540, memory at 1545, cpu at 1550.
- The fourth reader is `psi_irq_show` at `psi.c:1684-1686`, inside the IRQ `#ifdef` opened at 1683.
- The preamble "Citations (minor)" item gives the right list. The body does not.
- Replacement: `psi.c:1540,1545,1550,1686`.

**M4. Body and preamble disagree (F3, F4, and the F9 cross-reference).**
- The preamble says "Where this section and a later line disagree, this section wins."
- That leaves contradictory text in the knowledge base. The body should be fixed in place, and the preamble items
  that duplicate those fixes should then be removed.

### Low

**L1. F3 heading (line 80) and sentence (lines 80 to 81): "the kernel writes zeros there" needs "v5.19 onward".**
- `psi_v5.18.c` has no zeroing guard. Its loop at line 1062 prints computed values.
- `psi_v5.19.c:1067-1068` adds the guard, under the comment "CPU FULL is undefined at the system level".
- Commit `890d550d7dba` has the subject "sched/psi: report zeroes for CPU full at the system level".
- The K3 preamble item (lines 13 to 16) says this, but only for decision-table rules.

**L2. F2, line 69: "Each documented file (cpu, memory, io) holds two lines" needs "cpu from v5.13".**
- `psi_v5.12.c:1021` is `for (full = 0; full < 2 - (res == PSI_CPU); full++)`, so v5.12 prints one CPU line.
- `psi_v5.13.c:1045` is `for (full = 0; full < 2; full++)`, so v5.13 prints both CPU lines.

**L3. Unlabeled inferences in F1 to F6.**
- Lines 66 to 67 (F1): "So on v7.2 the kernel can expose an IRQ file the documentation does not mention; the documentation is
  not an inventory of the file set." This is derived from `psi.rst:37-38` and `psi.c:1718`. Label it.
- Line 87 (F3): "so the system CPU `full` line is always zeros at v7.2." This is derived from the `psi.c:1283` guard. Label it.
- Line 104 (F5): "a missing `some` line for IRQ is the kernel's shape, not a defect." This is a judgement. Label it [INFERENCE].

**L4. Loose anchors.** Thirteen anchors contain the target but also unrelated lines. Section 3 lists exact
replacements. None is a false claim on its own.

**L5. The F1 Kconfig anchor is version-specific.** HEAD now reads `init/Kconfig:730-731`, which is right for v7.2.
In stable v7.2.11 the same help text sits at line 736, because that release inserts a 5-line block before line 176
(`CC_OPT_INLINE_MEMSET`). The help text itself is unchanged.

### Note (adjacent material outside F1 to F6)

**N1. Preamble P2 (lines 22 to 26) conflicts with the new provenance bullet (lines 34 to 37).**
- P2 withdraws the `[INFERENCE]` label in F7 and U4, citing `init/main.c:1011,1047,1445`.
- I fetched `init/main.c` at v7.2. Line 1011 is `after_dashes = parse_args(..., &unknown_bootoption)`, which runs
  the `__setup` handlers. Line 1047 is `sched_init();`. Line 1445 is `do_initcalls();`. All three anchors resolve.
- P2 does not cite the `psi_init()` call site, and I did not locate it.
- The provenance bullet says statements resting on `init/main.c` are "pointers for the next round, not admitted
  facts". P2 therefore relies on something the entry itself does not admit.

**N2. F9 lines 142 to 143 cite `psi.c:1538-1550`** for "the former pass `&psi_system`". It has the same omission as M3.

**N3. Decision table, the CPU-full row (line 173).** It says "a nonzero value means the file is not the kernel's
system CPU pressure file". This is an unlabeled inference from F3 with no v5.19 scope.

**N4. Registry rows agree with my anchors, not with the body.** `corpus/SOURCES.md:96` (S090) says
"documented file set:37-38", which matches my F1 fix. `corpus/SOURCES.md:99` (S093) says
"help-text file list:730-731". F1's body still says 36-38.

## 3. Corrected anchors and wording (every disagreement)

| # | HEAD line | Fact | Written | Verified location | Verdict | Correct anchor or text |
|---|---|---|---|---|---|---|
| 1 | 63 | F1 | psi.rst:36-38 | quote at 37-38, line 36 blank; S090 row says 37-38 | loose | psi.rst:37-38 |
| 2 | 65 | F1 | psi.c:1710-1721 | `#ifdef` 1717, proc_create 1718, `#endif` 1719; 1710 is the function header | loose | psi.c:1717-1719 |
| 3 | 67 | F1 | init/Kconfig:730-733 | names at 731; 732 to 733 unrelated | fixed at HEAD | init/Kconfig:730-731 (v7.2) |
| 4 | 72 | F2 | psi.rst:40-43 | format lines 42-43; line 40 is the lead-in | loose | psi.rst:42-43 |
| 5 | 75 | F2 | psi.c:1290-1296 | seq_printf 1290-1295; 1296 closes the loop | loose | psi.c:1290-1295 |
| 6 | 78 | F2 | psi.rst:45-56 | "some" 45-46; "full" 48-49; 50-56 unquoted | loose | psi.rst:45-46 and 48-49 |
| 7 | 82 | F3 | psi.rst:57-59 | quote 57-58; line 59 blank | loose | psi.rst:57-58 |
| 8 | 84 | F3 | psi.c:1282-1288 | comment 1282, guard 1283, close 1288 | exact | keep |
| 9 | 86 | F3 | psi.c:1538-1550 | readers 1540, 1545, 1550; IRQ reader 1686 | incomplete (M3) | psi.c:1540,1545,1550,1686 |
| 10 | 90 to 91 | F4 | psi.rst:60-65 | quotes at 60-61 and 62-63 | acceptable superset | psi.rst:60-63 |
| 11 | 93 | F4 | psi.c:1284-1288 | total at 1286-1287; 1284 to 1285 is the loop | loose | psi.c:1286-1287 |
| 12 | 95 | F4 | psi.c:160-164 | PSI_FREQ at 161; EXP at 162 to 164 | loose | psi.c:161 |
| 13 | 95 to 96 | F4 | psi.c:1265-1272 | collect 1268; gate 1269-1270 | loose | psi.c:1268-1270 |
| 14 | 94 to 95 | F4 | "refreshed on each read" | see M1 | WRONG (M1) | M1 replacement text |
| 15 | 100 | F5 | psi.c:1273-1296 | only_full 1274; loop 1277; label 1291 | loose | psi.c:1274, 1277, 1291 |
| 16 | 101 | F5 | psi.c:1032-1042 | function 1005-1047; record_times 1039; add 1040 | wrong window | psi.c:1039-1040 |
| 17 | 101 | F5 | "adds only to PSI_IRQ_FULL" | see M2 | WRONG (M2) | M2 replacement text |
| 18 | 103 | F5 | psi.c:1364-1367 | refusal 1365-1366; `#ifdef` 1364, `#endif` 1367 | loose | psi.c:1365-1366; write path psi.c:1603-1605 |
| 19 | 104 | F5 | psi_types.h:41-49,57-70 | PSI_IRQ 45-47; PSI_IRQ_FULL 64-66; no PSI_IRQ_SOME | loose | psi_types.h:45-47, 64-66 (S095 row already says this) |
| 20 | 107 | F6 | psi.c:1717-1719 | `#ifdef` 1717; proc_create 1718; `#endif` 1719 | exact | keep |
| 21 | 110 | F6 | psi.c:1260-1263 | `#ifdef` 1260; if 1261; return 1262; `#endif` 1263 | exact bracket | keep |
| 22 | 104 | F5 | commit 52b1364ba0b1 | message "so we only use PSI_IRQ_FULL."; absent in v6.0, present in v6.1 | correct | keep |

Counts: 4 exact or acceptable (rows 8, 10, 20, 21); 13 loose (rows 1 to 7, 11 to 13, 15, 18, 19); 2 wrong or
incomplete (rows 9, 16). Rows 14 and 17 are claim errors, and row 22 is a commit reference.

Wording notes (not errors): F4 `PSI_FREQ = (2*HZ+1)` paraphrases `#define PSI_FREQ\t(2*HZ+1)`. F5 "refused with
`-EINVAL`" is accurate, because the write path returns `PTR_ERR(new)` at `psi.c:1603-1605`.

## 4. What I confirmed

**Quotes and code spans with anchors (20 checked, all present):**
1. F1 psi.rst:37-38 "Pressure information ... cpu, memory, and io." (wrapped).
2. F1 psi.c:1718 `proc_create("pressure/irq", 0666, NULL, &psi_irq_proc_ops)`.
3. F1 init/Kconfig:731 "pressure statistics files cpu, memory, and io."
4. F2 psi.rst:42 and psi.rst:43, the two format lines (two quotes).
5. F2 psi.c:1290, the seq_printf format string.
6. F2 psi.rst:45-46 "the share of time in which at least some tasks ... on a given resource".
7. F2 psi.rst:48-49 "the share of time in which all non-idle tasks ... simultaneously".
8. F3 psi.rst:57-58 "CPU full is undefined ... backward compatibility." (wrapped).
9. F3 psi.c:1283 `if (!(group == &psi_system && res == PSI_CPU && full))`.
10. F3 psi.c:1540 `psi_show(m, &psi_system, ...)` (elided form).
11. F4 psi.rst:60-61 "ratios (in %) ... tracked as recent trends over ten, sixty, and three hundred second windows" (elided "are").
12. F4 psi.rst:62-63 "The total absolute stall time (in us) is tracked and exported as well."
13. F4 psi.c:1286-1287 `total = div_u64(group->total[PSI_AVGS][...], NSEC_PER_USEC)` (elided).
14. F4 psi.c:161 "2 sec intervals".
15. F5 psi.c:1274 `only_full = res == PSI_IRQ;`
16. F5 psi.c:1277 `for (full = 0; full < 2 - only_full; full++)`
17. F5 psi.c:1291 `full || only_full ? "full" : "some"`
18. F5 commit 52b1364ba0b1 message: "so we only use PSI_IRQ_FULL."
19. F6 psi.c:1261-1262 `if (!irqtime_enabled() && res == PSI_IRQ) return -EOPNOTSUPP;`

Item 4 holds two strings, so the total is 20 strings.

**Claims verified (no error):**
- F1: psi.rst contains no "irq", "IRQ", "interrupt" or "softirq" (case-insensitive search returned nothing). The kernel
  creates a fourth file (psi.c:1718). The live `/proc/pressure` directory lists irq, cpu, io and memory.
- F2: the emitter format matches exactly. Two-digit fractions come from `%02lu` and the total from `%llu`.
- F3: the guard at psi.c:1283 and the zeroed averages and totals for that one line are correct at v7.2. Live
  `/proc/pressure/cpu` shows `full avg10=0.00 avg60=0.00 avg300=0.00 total=0`.
- F4: `EXP_10s`, `EXP_60s` and `EXP_300s` are used in `calc_avgs` (psi.c:342-359). psi.c:401 says "Pressure
  percentages are sampled at PSI_FREQ." The totals are in nanoseconds and divided by `NSEC_PER_USEC` at print time
  (derived from the nanosecond buckets in `record_times`).
- F5: `PSI_IRQ` (psi_types.h:45-47) and `PSI_IRQ_FULL` (psi_types.h:64-66) are under `CONFIG_IRQ_TIME_ACCOUNTING`.
  There is no IRQ `some` state. The write path returns `PTR_ERR(new)` (psi.c:1603-1605), so `-EINVAL` reaches
  userspace. Commit 52b1364ba0b1 is the introduction commit, subject "sched/psi: Add PSI_IRQ to track IRQ/SOFTIRQ
  pressure", and it adds `only_full`. `psi_60.c` (v6.0) contains none of PSI_IRQ, only_full or pressure/irq.
  `psi_61.c` contains `PSI_IRQ_FULL` at line 937 and `only_full` at line 1161. So "first shipped in Linux 6.1" is
  confirmed.
- F6: the `#ifdef` bracket at psi.c:1717-1719 and the EOPNOTSUPP line at psi.c:1261-1262 are correct. The IRQ
  accounting path returns early when `irqtime_enabled()` is false (psi.c:1014-1015).
- K3 (preamble): verified. The zeroing arrived in v5.19 (commit 890d550d7dba). v5.12 printed only "some" for CPU
  (`psi_v5.12.c:1021`), so "before 5.13" holds for v5.12. Older releases were not fetched.
- K5 (preamble): verified. The gate is at psi.c:1269-1270 and the unconditional collect at psi.c:1268.
- Live host, read-only: `uname -r` reports `7.2.11-arch1-1`, which matches the entry header. Memory and io each print
  two lines. irq prints one line, `full avg10=0.01 avg60=0.01 avg300=0.00 total=26155024`. cpu prints
  `some avg10=0.05 avg60=0.04 avg300=0.00 total=12514550` and `full ... total=0`. These match F2, F3 and F5.

**Provenance of the sources:**
- raw.githubusercontent.com returned HTTP 429 on the first attempt. A later re-check and the body-hash run returned
  HTTP 200.
- The v7.2 raw bodies hash to the same sha256 as the local copies and as the git.kernel.org `plain?h=v7.2` copies:
  - psi.rst `11c6b712...`
  - psi.c `452318be...`
  - init/Kconfig `a43f09d8...`
  - psi_types.h `483269b2...`
- Stable v7.2.11 psi.rst, psi.c and psi_types.h are byte-identical to v7.2. Stable init/Kconfig differs only by the
  5-line insertion described in L5.

## 5. Lane state observations (outside F1 to F6)

- `git log a730ecfe..HEAD` lists 7 commits after the measured tip.
- 89849a7 and 6a344d2 change the C2 tool (`tools/mori-pressure.py`, 58 lines changed across the tip-to-HEAD range) and add
  `tools/fixtures/mori-pressure/supplementary-cases.json` (new, 181 lines).
- 1046aca changes the C1 tool (`tools/mori-routed-check.py`, 17 lines changed).
- 7c77fba changes the S093, S096 and S097 rows of `corpus/SOURCES.md`.
- `git diff --name-only a730ecfe HEAD` lists 21 paths, including the ones above and
  `.ufo/waves/round-24/evidence/c2-selftest-after.txt` (new).
- The C2 numbers declared at the tip (selftest PASS 12/12 at f6a29702) do not transfer automatically to HEAD. I did
  not re-run the selftest. The lead should re-measure at HEAD or restate the tip.

## 6. Residual risk and verification gaps

- F7 to F12 and the other preamble items (K6, P2 apart from N1, P4, U7, the F9 and F12 changes) were not checked.
- K3's "before 5.13" was checked for v5.12 only.
- The host kernel is 7.2.11. I checked psi.c, psi.rst and psi_types.h against the stable copy. I did not check Arch
  packaging patches on top of the stable tree.
- The `psi_init()` call site (N1) was not located.
- F6's EOPNOTSUPP branch was not exercised live. There is no safe read-only way to switch IRQ time accounting off.
- Quote checks are whitespace-normalised substring matches. They prove presence, not the surrounding context.
- The live reads are one sample each and show the shape only.

## 7. What I ran

Sources and provenance:
- `curl -fsSL` on the four v7.2 raw URLs, with retries after HTTP 429, and a fallback to
  `git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/<path>?h=v7.2`.
- `curl` for `kernel/sched/psi.c` at `plain?h=v6.0`, `v6.1`, `v5.12`, `v5.13`, `v5.18` and `v5.19`.
- `curl` for `stable/linux.git/plain/...?h=v7.2.11` (psi.rst, psi.c, init/Kconfig, psi_types.h).
- `curl` for the cgit commit pages of 52b1364ba0b105122d6de0e719b36db705011ac1 and 890d550d7dba.
- `curl` for `init/main.c` at v7.2 (N1).
- `sha256sum` on each file and on the raw bodies piped from `curl`.

Anchor and quote checks:
- Search and read tools on the scratch copies, for every anchor in section 3.
- Python in the eval kernel: whitespace-normalised substring search, about 45 checks (quotes, code spans, paraphrase
  keys and version-presence tests), printing the start and end line of each match. Its output is the basis for section 3.
- A few exploratory `grep`, `sed` and `head` calls in bash on scratch copies. They were not used on lane files, and
  every anchor in this report was re-pinned with the search and read tools.

Lane (all read-only):
- `git rev-parse HEAD`, `git log`, `git cat-file -t`, `git show <rev>:<path>`, `git diff --stat`,
  `git diff --name-only`. No index writes and no checkout.
- `sha256sum` and `cp` of the working copy into scratch. The lane itself was not modified.
- Reads of `corpus/knowledge/system-pressure-r24.md`, `corpus/SOURCES.md`, and the directory
  `.ufo/waves/round-24/w2/` (to confirm the report path was free).

Host (detection only, no writes):
- `uname -r`.
- Reads of `/proc/pressure` (directory), `/proc/pressure/cpu`, `/proc/pressure/memory`, `/proc/pressure/io` and
  `/proc/pressure/irq`. No trigger and no write.

Not run: mutants, the C2 selftest, `tools/mori-pressure.py`, and any build.

## 8. Tooling

- No installs or upgrades. I read `/home/vgpnk/.omp/agent/RULES.md` first.
- Tools used, all already present: `curl`, `sha256sum`, `diff`, `cp`, `uname`, `git` (read-only subcommands), and
  Python in the eval kernel (analysis only).

## 9. Suggested order for Main

1. Fix the body in place: F3 heading (line 80) and reader anchor (lines 85 to 86); F2 line 69 (cpu from v5.13);
   F4 lines 94 to 95 (M1); F5 lines 100 to 104 (anchors and M2); F1 anchors (lines 63 and 65).
2. Remove the preamble items that the body fix makes redundant (K5 and the citations item), and resolve N1.
3. Label the three inferences in L3.
4. Re-measure C2 at HEAD, or restate the tip, given section 5.
