# Round 24 wave 2 — ReviewKnowledgeTable

Seat: MoriR24.ReviewKnowledgeTable (reviewer, leaf). No subagents, no mutants in the lane, no writes outside scratch and this report.
Target: `corpus/knowledge/system-pressure-r24.md` (C2 knowledge entry), scope F7–F12, the decision table, and the Limits section.
Checked against: Linux v7.2 raw sources, `tools/mori-pressure.py`, a scratch harness that drives the tool over every decision-table row, and read-only host reads.

## Revisions examined

- Pinned review revision: `a536b1844c99895d1b96a520d9a4cdd7fd3c85ea`. Entry blob `2d084411`; tool blob `a300244b`. Line numbers below are at this revision unless marked otherwise.
- Measured tip named in the assignment: `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc` (entry blob `50b2e601`, tool blob `4e08739a`). I ran the same tests there; differences are stated.
- The lane HEAD moved while I worked: `6a344d2` (first query), then `a536b18`, then `1046aca3ba6ef7d2646ad3a45addcfdebbf039bd` (commits `7c77fba`, `1046aca`). The tool did not change after `a536b18` (blob `a300244b`). The entry gained one provenance bullet at corrections lines 34–38 (so body line numbers after line 33 move by +5 at `1046aca`) and an S093 anchor fix (`init/Kconfig:730-733` became `730-731`). Every finding below still applies at `1046aca`.

Severity: High = an operator would read a wrong cause, a wrong "healthy" signal, or a wrong exit code from the entry. Medium = a wrong or overbroad statement, a tool-versus-table mismatch, or a stale unknown. Low = wording, citation, provenance, or coverage gap.

## Verdict (recommendation)

The decision table's mapping from file states to tool states is accurate for 37 of the 38 harness scenarios that carry a table-derived expectation at the pinned tool. The one miss is a verdict-precedence gap (F-4). The defects are in the prose: several statements about F7, F9, decision-table row 170, row 166, U1, U3 and U7 are contradicted by the v7.2 sources, by the host, or by the entry's own correction block. The body still carries those statements, and the correction block says it "wins", so a reader who quotes the body gets the wrong answer. I recommend editing those lines in place (F-6) before the C2 knowledge part is treated as sourced. Nothing here touches tool code or the frozen after-value (`MORI_PRESSURE_SELFTEST: PASS 12/12`).

## Findings

### High

**F-1 — Row 170 (EOPNOTSUPP) names a cause that the v7.2 files cannot reach.**
- Entry: row 170 (line 170) says "v7.2 returns it on the `psi_disabled` branch". F7 (lines 107–108) says the key "makes every read fail". U3 (lines 209–211) says a real host "may show `absent` rather than `EOPNOTSUPP`".
- Source (v7.2 `kernel/sched/psi.c`): `psi_enable` is written only by its definition and the `psi=` setter (`:150`, `:152`, `:156`), and read at `:230` and `:1712`. `psi_init()` enables `psi_disabled` only under `if (!psi_enable)` (`:230-231`). `psi_proc_init()` creates `/proc/pressure/*` only under `if (psi_enable)` (`:1712-1720`). The key is enabled at no other place in psi.c. So a `/proc/pressure/{cpu,memory,io}` read cannot reach `psi.c:1257-1258` while the file exists. The only reachable `/proc` EOPNOTSUPP at v7.2 is the IRQ branch `psi.c:1260-1263` (IRQ time accounting off at run time).
- Ordering is sourced, so the F7 `[INFERENCE]` label (lines 116–118) and U4 (lines 212–213) are stale: `parse_args("Booting kernel")` at `init/main.c:1011` handles `psi=`; `sched_init()` (`init/main.c:1047`) calls `psi_init()` at `kernel/sched/core.c:9101`; `do_initcalls()` (`init/main.c:1445`) runs `module_init(psi_proc_init)`. The lane's P2 correction (lines 22–26) says the same.
- Host: `/proc/cmdline` has no `psi=` and CONFIG_PSI=y. A boot-disabled host was not observed (rebooting is out of bounds).
- Smallest fix: row 170 becomes "On v7.2 reachable for `/proc` only on `irq`, when IRQ time accounting is off at run time (`tsc=noirqtime` on x86, or the sched clock marked unstable: `kernel/sched/clock.c:176,243`). A boot-disabled PSI removes all four files and gives `absent`, never `EOPNOTSUPP`." Rewrite U3; drop the `[INFERENCE]` labels in F7 and U4 and cite `init/main.c:1011,1047,1445` and `core.c:9101`.

**F-2 — The root cgroup's pressure files are the system group. F9 and Limits say the populations differ.**
- Entry: F9 lines 137–139 say "The system readers and the cgroup readers are different groups". Limits lines 184–185 say per-cgroup files "are a different population (F9)". The correction at line 140 fixes only F9's last sentence.
- Source: `include/linux/psi.h:39` returns `&psi_system` from `cgroup_psi()` when `cgroup_ino(cgrp) == 1`. The root's psi files are created by `css_populate_dir(&root_cgrp->self)` (`kernel/cgroup/cgroup.c:2195`) through `cgroup_psi_files` (`cgroup.c:1799-1801`, no root exclusion). The readers `cgroup_io/memory/cpu/irq_pressure_show` pass `cgroup_psi(cgrp)` (`cgroup.c:3970-3989`, `:4077-4082`).
- Live (read-only): `/sys/fs/cgroup/cpu.pressure` and `/proc/pressure/cpu` gave the same `total=12792488` in 5 of 5 back-to-back pairs. `/sys/fs/cgroup/irq.pressure` and `/proc/pressure/irq` gave `total=27063406` in 3 of 3 pairs. Sequential commands run seconds apart differed by 1 µs (cpu) and 8 µs (irq), which fits one counter that keeps advancing. The lane's "byte-identical in one read pass" (line 140) holds for back-to-back reads only.
- Smallest fix: line 137–139: "The system and cgroup readers are different groups for every non-root cgroup; for the root cgroup they are the same group (`psi.h:39`)." Limits 184–185: "non-root cgroups' … are a different population."

**F-3 — Row 166 (PRESSURE_OK) omits the frozen-counter case. U7 is still labeled unknown although its mechanism is sourced.**
- Row 166 "does NOT prove" lists stall, health, per-cgroup coverage, and threshold. It does not say the counters advanced. U7 (line 217) says writing 0 to the root `cgroup.pressure` stops `psi_system` accounting, so a one-shot read can report `PRESSURE_OK` under pressure.
- Source for the mechanism: `kernel/cgroup/cgroup.c:4123-4131` (`psi = cgroup_psi(cgrp); … psi->enabled = enable`); `psi.h:39` (root maps to `psi_system`); `psi.c:845-859` (in `psi_group_change`, `if (!group->enabled) { … return; }` skips the state sampling); `psi.c:1034-1035` (IRQ accounting skips a disabled group); `psi.c:551` and `:1269-1270` (averages decay toward zero on zero samples).
- Flag readable live: `/sys/fs/cgroup/cgroup.pressure` reads `1` on this host. The tool never reads it: `RESOURCE_NAMES` are `cpu, memory, io, irq` under `--root` only.
- Not exercised: writing the flag is out of bounds. The freeze is a code reading. Only the live flag value is observed.
- Smallest fix: add to row 166: "That the counters advanced: writing 0 to the root `cgroup.pressure` freezes them (U7)." Move U7's mechanism out of `[UNKNOWN]` and say "not exercised" in its text. Recommendation for a later round (not implemented here): have the tool report the root flag as a field.

### Medium

**F-4 — Precedence gap: a HIGH finding outranks PARTIAL, but rows 169 and 175 say PARTIAL exit 0.**
- Harness scenario `R4-irq-absent-plus-memory-high` (irq file absent; memory full avg10 25.00). Tool: `PRESSURE_HIGH`, exit 1, finding `memory/full`. Table rows 169 and 175: `PRESSURE_PARTIAL`, exit 0 "(if others are `ok`)". The code is `evaluate()`: `elif findings:` (HEAD line 343) before `elif any(s != STATE_OK …)` (line 345). The contract says "Exit 1 on PRESSURE_HIGH".
- Smallest fix: rows 169 and 175 state the precedence: "any finding gives `PRESSURE_HIGH`, exit 1; `PRESSURE_PARTIAL` needs no finding."

**F-5 — Limits line 180 says the tool "reads a file and stops". That is wrong for `--interval`.**
- Tool: `--interval S` reads every resource, sleeps S seconds, and reads again (`evaluate()` HEAD lines 315–326; `_sleep(interval_s)` at `:325`). Live run: `python3 -I tools/mori-pressure.py --interval 1` returned `PRESSURE_OK`, exit 0, `elapsed_us: 1000290`, and per-kind `total_delta_us`.
- Scope line 45 ("It describes one-shot, system-scope reads") has the same problem.
- Smallest fix: "By default one read per file. With `--interval S` (0 < S ≤ 10), two reads S seconds apart. Still no trigger and no poll."

**F-6 — The body contradicts the correction block in at least 16 places.** The block says "where this section and a later line disagree, this section wins". The body is what a reader quotes, so the contradictions should be removed in place. Pairs (body line → correction):
1. Line 89–91 "refreshed on each read" → K5 (lines 17–18): averages refresh only when the next 2-second update is due (`psi.c:1269-1270`).
2. Lines 116–118 `[INFERENCE]` on the boot ordering → P2 (lines 22–26).
3. Line 123 "the kernel accepts windows ranging from 500ms to 10s" → K6 (lines 19–21); see F-9.
4. Line 137 "different groups" → F-2 (line 140 is the partial fix).
5. Lines 145–146 "not a stall event and not a kernel fault" → P4 (lines 30–33); see F-10.
6. Line 148 "The kernel source defines no 'warn at N %' rule" → citation note (lines 34–36): scope is `psi.c` and `psi.rst` only.
7. Row 167 "`null` means *undefined*, not *zero*" → P3 (lines 27–29): "undefined" is psi.rst's word for system CPU `full`.
8. Row 169 "a missing file is consistent with either" (two causes) → P4 (lines 30–33) adds CONFIG_PSI off, kernel older than 6.1, and a wrong `--root`.
9. Row 170 → F-1.
10. Row 173 "so a decrease means the two samples are not comparable readings" (no `[INFERENCE]` label) → P4 (line 31).
11. Line 207 U1 "where the branch is switched on … was not located" → F-7.
12. Lines 209–211 U3 → F-1.
13. Lines 212–213 U4 → F-1.
14. Lines 214–215 U5 "was not checked" → F-17.
15. Lines 184–185 "a different population" → F-2.
16. Line 153 F12 header → F-8.
- Smallest fix: edit each place. Keep the correction block only as a changelog, not as an override.

**F-7 — U1 says the run-time switch was "not located". It is located, and the file that holds it is not cited anywhere.**
- Source: `kernel/sched/cputime.c:16` (`DEFINE_STATIC_KEY_FALSE(sched_clock_irqtime)`), `:31-34` (`enable_sched_clock_irqtime()` calls `static_branch_enable`), `:36-40` (`disable_sched_clock_irqtime()` calls `static_branch_disable`). `irqtime_enabled()` reads that key (`kernel/sched/sched.h:3492-3495`).
- Enable callers: `kernel/time/sched_clock.c:242-243` (generic sched clock only), and `arch/x86/kernel/tsc.c:1544-1545` (x86, suppressed by `tsc=noirqtime` at `tsc.c:327-328`).
- Disable callers: `kernel/sched/clock.c:176` (runtime, in `__sched_clock_work`) and `:243` (inside `sched_clock_init_late`, which is a `late_initcall` at `:247`).
- The lane's K2 kill (peer report) reaches the same conclusion for the clock callers; this finding adds `cputime.c`, which is the switch itself.
- Smallest fix: U1 rewritten with these lines; add `kernel/sched/cputime.c` to the provenance list.

**F-8 — The F12 header overgeneralizes: "the IRQ clock itself is a boot parameter" (line 153).**
- `irqtime=` exists only where `sched_clock.o` is built, which is `kernel/time/Makefile:23` (`CONFIG_GENERIC_SCHED_CLOCK`). `arch/x86/Kconfig` does not select that symbol: a grep of the file for `GENERIC_SCHED_CLOCK` and `HAVE_UNSTABLE_SCHED_CLOCK` finds only the second, at `:302`. On the x86 path the enable is the TSC init call (`tsc.c:1544-1545`), and its opt-out is `tsc=noirqtime`, documented at `Documentation/admin-guide/kernel-parameters.txt:7930-7933`.
- The body (line 156) now says this; the header does not. The `tsc=` text is in the S094 source file but outside S094's stated row scope ("the `psi=` kernel boot parameter").
- Smallest fix: header: "On generic-sched-clock architectures the `irqtime=` boot parameter decides; on x86 the TSC init enables IRQ time accounting unless `tsc=noirqtime` is given."

**F-9 — F8 states a kernel window range the code does not enforce (line 123).**
- "The kernel accepts windows ranging from 500ms to 10s" is the sentence of `psi.rst:102-104`. The v7.2 code rejects only `window_us == 0 || window_us > WINDOW_MAX_US` (`psi.c:1372-1373`), requires a multiple of 2 s for unprivileged writers (`psi.c:1379-1380`), and requires `0 < threshold ≤ window` (`psi.c:1383-1384`). A grep of psi.c finds no minimum-window constant at v7.2.
- The peer report found `WINDOW_MIN_US 500000` at v6.1. So "stale at v7.2" is fair, but the entry should say "not enforced at v7.2" and cite the documentation for the 500 ms figure.
- Smallest fix: "The documentation states 500 ms to 10 s (psi.rst:102-104). The v7.2 code enforces 0 < window ≤ 10 s (psi.c:1372-1373) and, for unprivileged writers, a multiple of 2 s (psi.c:1379-1380)."

**F-10 — F10 (lines 145–146) and row 173 draw a conclusion the source does not give.**
- The total is accumulated with `+=` (`psi.c:410-411`), so within one boot it cannot decrease. The source has no path that lowers it. A decrease is therefore unexplained by the source. It could be a reboot between reads, a different file, or a defect. "Not a stall event and not a kernel fault" is not sourced.
- Smallest fix: "The v7.2 code has no decrement path (`psi.c:410-411`). A decrease is unexplained by the source [INFERENCE: reboot, different file, or defect]." Apply the same change to row 173.

### Low

**F-11 — Limits lines 197–199 omit that `stall_ratio` is nominal.** The code divides by the requested S (`round(delta / (interval_s * 1e6), 6)`, HEAD line 277), and the tool reports the measured `elapsed_us` beside it. Live: `interval_s: 1.0`, `elapsed_us: 1000290`. Add one sentence.

**F-12 — Coverage gaps between the decision table and the tool's real mapping.**
- (a) Row 172 (malformed) does not name non-UTF-8 content. At the pinned tool it is `malformed` (`_read_resource`, `except UnicodeDecodeError`, HEAD line 162). At the measured tip it was `unreadable` (harness `R7-memory-non-utf8`, run-a730). The table is silent at both revisions.
- (b) Row 171 names EACCES and EPERM only. The tool maps every other errno to `unreadable` and names the errno (`_state_for_oserror`, lines 135–148). Harness `R7-directory-named-cpu` (cpu is a directory) gives `unreadable`.
- (c) Row 169 (ENOENT) omits CONFIG_PSI=n: `kernel/sched/build_utility.c:92-93` includes psi.c only under `#ifdef CONFIG_PSI`, so no `/proc/pressure` exists. It also omits a wrong `--root`. The lane's P4 correction lists both; the row does not.
- (d) Row 172's "the kernel's own emitter produces exactly the documented shape" lacks the v7.2 qualifier that K3 (lines 13–16) adds. My own fetches confirm K3's dates: `kernel/sched/psi.c` at v5.18 (git.kernel.org plain, 39384 bytes) has neither "CPU FULL is undefined" nor "PSI_CPU && full"; at v5.19 (raw GitHub, 39560 bytes) both are present at lines 1067–1068.

**F-13 — Limits lines 184–185: "Only `/proc/pressure` is read" holds by default only.** `--root` accepts any directory that holds files named `cpu`, `memory`, `io` or `irq`. Live check: `--root /sys/fs/cgroup` gave `PRESSURE_UNAVAILABLE`, exit 2, with all four `absent`. That confirms the tool cannot read cgroup files as written. Say "by default".

**F-14 — Limits lines 194–196: "the tool's grammar accepts any decimal" is wider than the regex.** `.5`, `1e2` and `-1` are `malformed` (harness `R7-io-avg10-*`). `4.731` is accepted. Replace with "any unsigned decimal with at least one leading digit and at most one fraction part".

**F-15 — Provenance is incomplete.** Header line 1 lists two supporting reads without registry rows (`kernel/cgroup/cgroup.c`, `kernel/time/sched_clock.c`). The body also rests on `sched.h`, `include/linux/sched/clock.h`, `include/linux/psi.h`, `init/main.c`, `arch/x86/kernel/tsc.c`, `kernel/sched/clock.c`, `kernel/time/Makefile:23` (F12), `kernel/sched/core.c:9101` (P2 cites `init/main.c:1047`, which is only the `sched_init()` call), `kernel/sched/build_utility.c:92-93` (CONFIG_PSI include, not cited), `kernel/sched/cputime.c` (not cited), and `arch/x86/Kconfig:302` (not cited). The 1046aca bullet names eight files and omits `time/Makefile`, `core.c`, `build_utility.c`, `cputime.c` and `x86/Kconfig`. List every file in the header and in the bullet.

**F-16 — Citation drift (checked against the v7.2 text).** F7 `psi.c:1711-1719`: the `if (psi_enable)` is `:1712`, the block is `:1712-1720`. F10 `psi.c:408-410`: the statement is `:410-411`. P2's `init/main.c:1047` should also cite `kernel/sched/core.c:9101` (`psi_init()` is called inside `sched_init()`).

**F-17 — U5 is partly answered and still says "not checked".** Raw `kernel/sched/psi.c` at v6.0 has 0 `PSI_IRQ` lines (39513 bytes); at v6.1 it has 6 (43235 bytes). That fits S096's "first released in Linux 6.1". The cgroup doc at v6.0 and v6.1 was not fetched (HTTP 429 on retries). Update U5 to say psi.c was checked at v6.0 and v6.1, and the cgroup doc was not.

**F-18 — `kernel/sched/clock.c:243` is boot time, not after boot.** Line 243 is inside `sched_clock_init_late`, a `late_initcall` (`:228`, `:247`). Line 176 is the runtime path. Line 156 should say "at boot (`:243`) or after boot (`:176`)".

**F-19 — Tool-side observations (no entry claim depends on them).**
- Usage errors print `"root": "/proc/pressure"` (`_emit_error`) even when `--root` was given.
- `--warn-avg10 0` flags every `ok` resource that has a `some` or `full` line: harness `USAGE-warn-zero-all-high` gave four findings. Limits say "threshold local" but not zero.

## Row-by-row check (decision table, pinned tool `a300244b`, harness on `a536b18`)

| Row (line) | Table says (tool state, verdict, exit) | Harness evidence | Result |
|---|---|---|---|
| 166 all four present, low | `ok` ×4, PRESSURE_OK 0 | R1 OK 0, irq `some` null; live OK 0 | agrees |
| 167 irq full only | irq `ok`, `some: null` | R1 `irq_some` None | agrees (wording "undefined" wrong: F-6 item 7) |
| 168 cpu full present | cpu `ok`, `full_system_undefined`, never thresholded | R3 cpu full 99.99 → OK 0 | agrees |
| 169 ENOENT | `absent`; PARTIAL 0; UNAVAILABLE 2 if all absent | R4 irq absent → PARTIAL 0; all absent → UNAVAILABLE 2; missing dir → UNAVAILABLE 2 | agrees except precedence: irq absent + memory HIGH → HIGH 1 (F-4) |
| 170 EOPNOTSUPP | `unsupported`; PARTIAL 0 / UNAVAILABLE 2 | R5 (hook) irq unsupported → PARTIAL 0; R5b all → UNAVAILABLE 2 | tool agrees; the cause text is wrong (F-1) |
| 171 EACCES/EPERM | `unreadable` | R6 real file mode 000 → unreadable; R6b EPERM hook → unreadable | agrees; other errnos (EISDIR) not listed (F-12b) |
| 172 malformed | `malformed`; PARTIAL 0 | missing full, duplicate some, exponent, leading dot, negative, empty, cpu without full, irq some-only → malformed PARTIAL 0; all four malformed → PARTIAL 0 | agrees; non-UTF-8: HEAD malformed, measured tip unreadable (F-12a) |
| 173 counter_regressed | `counter_regressed`; PARTIAL 0 | R8 memory some delta −243 → counter_regressed PARTIAL 0 | agrees (wording: F-10) |
| 174 over threshold | finding `PRESSURE_HIGH`, exit 1 | cpu some 10.00; memory full 25.00; irq full 15.00 → HIGH 1 with the right findings | agrees (equality `≥` confirmed) |
| 175 any other resource unavailable/malformed | PARTIAL 0 "if others are ok" | irq absent + memory HIGH → HIGH 1 | DISAGREES when another resource is HIGH (F-4) |
| 176 all unavailable | UNAVAILABLE 2 | R4b, R5b, missing root → UNAVAILABLE 2 | agrees |

## Limits check

| Limit (line) | Tool behaviour observed | Result |
|---|---|---|
| 180 "One-shot only. The tool reads a file and stops." | `--interval` reads twice (live `--interval 1`) | DISAGREES (F-5) |
| 184–187 "No cgroup scope. Only `/proc/pressure` is read" | default root only; `--root` accepts any directory; `/sys/fs/cgroup` → UNAVAILABLE 2 | true by default only (F-2, F-13) |
| 188–191 threshold local, default 10.0 | default 10.0; `--warn-avg10 0` flags every ok resource | agrees; zero case not stated (F-19) |
| 192–193 CPU full excluded from threshold | cpu threshold uses `some` only; `full_system_undefined: true` | agrees |
| 194–196 grammar looser than the kernel | `4.731` accepted; `.5`, `1e2`, `-1` malformed | direction agrees; "any decimal" overstated (F-14) |
| 197–199 interval is a two-point slope | `stall_ratio` divides by requested S; `elapsed_us` reported | incomplete (F-11) |
| 200–201 detection and report only | tool opens files with mode `"r"` only; no trigger code | agrees |
| 202–203 vocabulary is the tool's own | kernel strings used as sources only | agrees |

## F7–F12 facts check

| Fact | Entry cites | Source check (v7.2 unless marked) | Result |
|---|---|---|---|
| F7 | `psi.c:1257-1258`, `:228-240`, `:149-158`, `:1553-1566`, `:1711-1719` | `:1257-1258` yes; `:230-231` (the `psi_init` enable) yes; `:150-158` yes; `:1553-1566` single_open yes; the `if` is `:1712` | code cites right (F-16); reachability claim wrong (F-1) |
| F8 | `psi.rst:67-88`, `:102-104`, `WINDOW_MAX_US psi.c:167`, EBUSY `psi.c:1596-1598` | `psi.rst` text matches; `:167` yes; `:1597-1598` return `-EBUSY` yes | the 500 ms lower bound is not in code (F-9) |
| F9 | `psi.rst:178-187`, `cgroup-v2.rst:1066-1087`, `cgroup.c:4077-4091`, `:4127`, `:3970-4091` | all quotes and lines match; `cgroup-v2.rst` irq 1083, cpu 1215, memory 1911, io 2171 | "different groups" wrong for root (F-2) |
| F10 | `psi.c:408-410` | accumulate is `psi.c:410-411`; monotonic within a boot | cite drift (F-16); "not a kernel fault" unsourced (F-10) |
| F11 | psi.rst examples `:70-88` | examples at `psi.rst:73-75`, `:85-88` match; no threshold rule in psi.c or psi.rst | scope wording (F-6 item 6); tree-wide negative not run |
| F12 | `sched_clock.c:48-50, 242-243`; `clock.h:112-116` | `sched_clock.c:48`, `:50`, `:242-243` yes; `clock.h:112-116` yes | the switch is `cputime.c:31-34`, not cited (F-7); x86 scope (F-8) |

## Survivors (checked and confirmed)

- `psi_types.h:41-49, 57-70` enums; PSI_IRQ and PSI_IRQ_FULL under `CONFIG_IRQ_TIME_ACCOUNTING`; no IRQ-some state.
- `psi.c:1364-1366`: a trigger naming `some` for IRQ decrements to 5, which is not `PSI_IRQ_FULL` (6), so it returns `-EINVAL`.
- `psi.c:1283-1288`: system CPU `full` is zeroed. Confirmed at v5.19 and not at v5.18 (F-12d).
- U2 host facts (live read-only): CONFIG_PSI=y, `# CONFIG_PSI_DEFAULT_DISABLED is not set`, CONFIG_IRQ_TIME_ACCOUNTING=y, CONFIG_CGROUPS=y, CONFIG_X86_TSC=y; `/proc/cmdline` has no `psi=`, `irqtime=` or `tsc=noirqtime`; kernel `7.2.11-arch1-1`.
- U7 mechanism (code, F-3) and the live flag value `1`.
- S096: commit `52b1364ba0b1` (patch date 26 Aug 2022, subject "sched/psi: Add PSI_IRQ to track IRQ/SOFTIRQ pressure"); v6.0 psi.c has no PSI_IRQ and v6.1 psi.c has 6 matches.
- Tool row mapping for rows 166–176 (except F-4 and F-12).
- The tool never writes: it opens files with mode `"r"` only.

## Commands run (read-only except scratch; outputs summarized)

1. Lane reads: `git rev-parse HEAD` (moved `6a344d2` → `a536b18` → `1046aca`); `git cat-file -t`, `merge-base --is-ancestor` (a730 is an ancestor of HEAD); `git show <rev>:<path>` into scratch; `git diff` between two commits (never against the index); `git log --oneline` between revisions. No index writes. Lane files read: entry, tool, `.ufo/waves/round-24/contract.md`, `corpus/SOURCES.md` (rows S090–S097), `.ufo/waves/round-24/w2/CriticKnowledgeOverclaim.md`.
2. Clones (scratch only): `git clone --no-hardlinks <lane> clone-a730` (checkout `a730ecfe`) and `clone-head` (checkout `a536b18`).
3. Frozen selftest: a730 → `MORI_PRESSURE_SELFTEST: PASS 12/12`, exit 0. a536b18 → `PASS 12/12`, `MATCHER: rejected 48/48 corrupted expectations`, exit 0. Supplementary cases at a536b18 (`--selftest --cases …supplementary-cases.json`) → `PASS 6/6`, `rejected 24/24`, exit 0.
4. Harness `harness.py` (scratch), 40 scenarios per revision. a536b18: MATCH 37, DIFF 1 (F-4), info 2. a730: MATCH 36, DIFF 2 (F-4 and the non-UTF-8 row), info 2. Outputs: `run-head.txt`, `run-a730.txt`, `results-head.json`, `results-a730.json`.
5. Live read-only: `/proc/cmdline`; `zcat /proc/config.gz | grep` for PSI, IRQ_TIME_ACCOUNTING, CGROUPS, X86_TSC; `cat /proc/pressure/*`; `cat /sys/fs/cgroup/{cgroup,cpu,irq}.pressure`; back-to-back pair loops (cpu ×5, irq ×3); `python3 -I clone-head/tools/mori-pressure.py` → PRESSURE_OK exit 0; `--interval 1` → PRESSURE_OK exit 0, `elapsed_us 1000290`; `--root /sys/fs/cgroup` → PRESSURE_UNAVAILABLE exit 2.
6. Kernel raw text (v7.2 via raw.githubusercontent.com, tag `v7.2`): `kernel/sched/psi.c`, `include/linux/psi.h`, `include/linux/psi_types.h`, `kernel/cgroup/cgroup.c`, `include/linux/cgroup.h`, `Documentation/accounting/psi.rst`, `Documentation/admin-guide/cgroup-v2.rst`, `init/Kconfig`, `Documentation/admin-guide/kernel-parameters.txt`, `kernel/time/sched_clock.c`, `include/linux/sched/clock.h`, `kernel/sched/sched.h`, `kernel/sched/cputime.c`, `kernel/sched/clock.c`, `kernel/sched/core.c`, `kernel/sched/build_utility.c`, `kernel/sched/Makefile`, `kernel/time/Makefile`, `init/main.c`, `arch/x86/kernel/tsc.c`, `arch/x86/Kconfig`. Other tags: `kernel/sched/psi.c` at v5.18 (git.kernel.org plain), v5.19, v6.0, v6.1 (raw). Commit patches `52b1364ba0b1` and `890d550d7dba` (github.com `.patch`).
7. The GitHub API returned 403 (rate limit) and raw.githubusercontent.com returned 429 on some retries. Each retry was spaced; the gaps are listed under residual risk.

No write went to `/proc`, `/sys` or any cgroup file. No PSI trigger was registered. No host service, package or lane file changed except this report.

## Tooling record

No installs and no updates. Existing tools used: curl, git 2.56.0 (read-only subcommands, clones into scratch), python3 3.14.8, jq at `~/.local/bin/jq`, zcat, grep, awk, sed. `pacman` was not run. The operator directive in `~/.omp/agent/RULES.md` was read first.

## Overlap with the peer critic report

I read `CriticKnowledgeOverclaim.md` after my own checks. Its K1, K2, K3, K5, K6 and P1–P4 agree with my independent results. My additions are F-4 (precedence), F-5 (one-shot limit), F-7 (`cputime.c` is the switch), F-11 (nominal ratio), F-12 (coverage gaps), F-13, F-14 and F-19, and the rule in F-6 that the body must be edited in place.

## Residual risk and verification gaps

- Boot-disabled (`psi=0`) behaviour was not exercised. It is a code reading (`psi.c:230-231`, `:1712`; `init/main.c:1011,1047,1445`).
- U7 freeze was not exercised; writing the flag is out of bounds. The mechanism is a code reading plus the live flag value.
- EOPNOTSUPP on `irq` was not reproduced live: this host has IRQ time accounting on. The harness exercises that row through the tool's own in-process hook, which tests the mapping, not the kernel.
- Tree-wide negatives were not run: no grep over the whole v7.2 tree for other `static_branch_enable(&psi_disabled)` sites or other `enable_sched_clock_irqtime()` callers. The "no threshold" claim (F11) is checked for psi.c, psi.rst and the cgroup docs only.
- `cgroup_ino(root) == 1` is sourced only from the comparison in `psi.h:39`. The kernfs root inode value was not read. The live match in F-2 supports it.
- v5.12 and v5.13 CPU-full claims were not re-fetched by me; the peer report did. v5.18 and v5.19 were checked by me (F-12d).
- The cgroup-v2 doc at v6.0 and v6.1 was not fetched (429). The S096 check used psi.c only.
- One host only (x86_64, kernel 7.2.11-arch1-1). Nothing here is a fleet fact.
- The lane HEAD moved three times while I worked. I reviewed the entry at `a536b18` in full and checked the one later change (`1046aca`: provenance bullet and S093 anchor). A later commit after `1046aca` would need the same diff check.
- The harness is in scratch: `/fast/scratch/hyaku/mori-r24-a2/w2/ReviewKnowledgeTable/harness.py`, with the clones `clone-a730` and `clone-head` beside it and the run outputs `run-head.txt` and `run-a730.txt`.
