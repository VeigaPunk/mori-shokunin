# Mo54CritLedgerDrift — attack on `## Release drift`

Axes: freshness (documentation vs implementation), calibration (behavioral-change attribution), coverage (adjacent release drift).

## Counterexample and evidence

**The `io.stat` field-name/unit change is a documentation correction, not an implementation change.** The ledger and the SOURCES lead say the field changed from `delay`/microseconds at 7.2 to `delay_nsec`/nanoseconds at 7.3, implying observers keyed to the former interface would newly misread it. But in `block/blk-cgroup.c` at both tags, `blkcg_print_stat()` emits `use_delay=%d delay_nsec=%llu`, reading `blkg->delay_nsec` (v7.2 line 1164; v7.3 line 1170). The only matching `seq_printf` in either file is that output. `block/blk-iolatency.c` has no such `io.stat` print and its v7.2→v7.3 diff does not change a field name or unit. The RST diff does show a documentation edit from `delay`/microseconds to `delay_nsec`/nanoseconds. Further qualification: that output is conditional on `blkcg_debug_stats` and nonzero `use_delay`; the flag is initialized false and exported as a module parameter (`block/blk-cgroup.c` v7.2 lines 60, 1163–1167, 2243–2244; v7.3 lines 63, 1169–1173, 2262–2263). Thus the ledger's observer-impact sentence attributes a new runtime drift where the inspected implementation shows none, and omits that the fields are debug-gated.

**The pressure-file documentation did change, but its access-mode change is documentation-only.** The RST states `memory.pressure` and `io.pressure` are read-only at v7.2 and read-write at v7.3 (v7.2 lines 1911–1915, 2171–2175; v7.3 lines 1939–1942, 2203–2206). In `kernel/cgroup/cgroup.c` v7.2, `cgroup_psi_files[]` already attaches `.write = cgroup_io_pressure_write` and `.write = cgroup_memory_pressure_write` (lines 5549–5566); both wrappers call `pressure_write()`, which creates a PSI trigger and returns `nbytes` on success (lines 3992–4052). The table and handlers persist at v7.3. This supports the parenthetical that trigger writes worked at v7.2 when these cgroup PSI files are available; it does not establish the unqualified historical word “always.”

**The CPU-stat note is a real documentation change, but not the whole CPU-related delta.** The v7.3 RST adds that the five CFS bandwidth stats are non-hierarchical and adds `cpu.stat.local`, describing local throttling; the v7.2 RST lacks both additions. `kernel/sched/core.c` already registers `stat.local` at v7.2 (lines 10270–10271) as well as v7.3 (lines 10337–10338). So the documentation clarifies old behavior / surfaces existing in code; the ledger should avoid implying the file itself was introduced in v7.3. The ledger says three changes “sit on mori ground”; it is a selected list, not a complete inventory of adjacent observability changes.

**Another concrete omitted documentation catch-up on mori's event surface:** the v7.2→v7.3 RST changes the `misc.events` key description from `max` to `<res>.max` (v7.2 lines 3013–3017; v7.3 lines 3067–3077), while `kernel/cgroup/misc.c` emits `"%s.max %llu\n"` at both tags (v7.2 line 379; v7.3 line 379). This too is a doc correction rather than a newly changed event key. Since the ledger limits itself to three examples, this does not falsify its listed examples, but makes any implied completeness unsafe.

The “32 places” word-level-diff count is reproducible on the committed rendered HTML after stripping markup: a `git diff --no-index --word-diff=porcelain` consecutive +/- run count produced 32. The statement that none touches the cited memory.stat/OOM quote rows is consistent with the diff inspected; no counterexample found there.

## Smallest safe correction

Replace the `io.stat` release-drift sentence with: “The v7.3 cgroup-v2 documentation corrects its `io.stat` throttle-field description from `delay`/microseconds to `delay_nsec`/nanoseconds; `block/blk-cgroup.c` already emitted `delay_nsec` in nanoseconds at v7.2, conditionally when debug stats are enabled and `use_delay` is nonzero, so this is documentation drift rather than a v7.3 interface change.”

Retain the pressure documentation transition, but state explicitly that `cgroup.c` already wired PSI-trigger write handlers for `memory.pressure` and `io.pressure` at v7.2, when the files are available; avoid “always” as an unbounded historical assertion. Retain the CPU note as documentation drift, and add one compact adjacent example: v7.3 documents `cpu.stat.local`, already registered in v7.2 code. Optionally note the `misc.events` key documentation correction if the section intends to catalogue adjacent observability docs comprehensively.

Replace the SOURCES.md lead's `io.stat throttle field renamed...` clause with: “v7.3 cgroup-v2 documentation corrects the throttle-field spelling/unit (`delay_nsec`, nanoseconds); v7.2 and v7.3 `block/blk-cgroup.c` both emit that field, gated by `blkcg_debug_stats` and nonzero `use_delay`. `memory.pressure`/`io.pressure` are documented read-write at 7.3 (read-only at 7.2), although v7.2 `kernel/cgroup/cgroup.c` already wires trigger-write handlers. The CFS bandwidth note and `cpu.stat.local` are documented at 7.3; the latter is already registered in v7.2 code.” Remove the claim that `block/blk-iolatency.c` is the unexamined source for the `io.stat` field; the output is in `block/blk-cgroup.c`.

## Findings

- **HIGH** — `corpus/knowledge/kernel-v7.3-recheck-r54.md`, “Release drift” `io.stat` sentence: overclaims an implementation rename/unit change; both versions' `block/blk-cgroup.c` emit `delay_nsec` in nanoseconds.
- **MED** — `corpus/SOURCES.md`, `## Leads (unopened)` line 369: repeats the false `io.stat` rename premise and points to `blk-iolatency.c`, not the printing code; amend as above.
- **LOW** — `corpus/knowledge/kernel-v7.3-recheck-r54.md`, “Release drift”: listed examples are accurate as documentation changes, but do not distinguish doc catch-ups from runtime changes and omit the already-present v7.2 `cpu.stat.local` code. Add the distinction; treat adjacent-drift completeness as a limit unless expanded.

## Evidence commands

- `curl -sfL ... cgroup-v2.rst?h=v7.2` and `...?h=v7.3` into `/fast/scratch/hyaku/mori-r54/Mo54CritLedgerDrift/f/`; `diff -u` showed the pressure, `io.stat`, CPU stats and misc.events documentation changes (exit 1, expected differences).
- `curl -sfL ... kernel/cgroup/cgroup.c?h=v7.2|v7.3`; `grep`/`sed` located the pressure handlers and `.write` cftype assignments. Both fetches succeeded; output shows v7.2 `.write` wiring and trigger creation.
- `curl -sfL ... block/blk-cgroup.c?h=v7.2|v7.3` and `... block/blk-iolatency.c?h=v7.2|v7.3`; output shows the same `delay_nsec` print in both blk-cgroup copies; iolatency diff contains no print-field rename.
- `curl -sfL ... kernel/sched/core.c?h=v7.2|v7.3`; `grep` showed `stat.local` registered at both tags.
- `curl -sfL ... kernel/cgroup/misc.c?h=v7.2|v7.3`; `grep` showed `%s.max` emission at both tags.
- `disk-guard.sh status`: `/fast/scratch/hyaku` free 596.5G at check. No tools installed. No host state changed.

## Unverified

No attempt was made to determine when the v7.2 code first acquired these behaviors; the checked tags prove only that they were present by v7.2. `dmem.peak` was not checked. No claim is made that the examples exhaust all differences between releases.