measured 2026-10-23T09:17:09Z

# JudgeRowsR25 — register rows rounds[455].capabilities_added[0] and [1] (wave 2, falsify)

Seat: MoriR35.JudgeRowsR25. Target: the two round-25 rows in the final `## Capabilities`
section of SCORECARD.md at cedb0ec4f3a4f672804deac388b7191258f01fcd, judged under the
frozen decision rule (c1-controls.txt): cells (a) non-empty and closure-faithful — every
fact stated by the record and bounded as the record bounds it — and (b) evidence cell
holding only backticked paths; then separately (c) pointer relevance of the cited artifact
at the closure commit 829d8c9072d5907b9050d06c16cc34b0bb73d0f8.

## Method and sources (all read-only; no writes in the lane; no counter run, none needed)

- SCORECARD.md at cedb0ec4 via `git -C mori-shokunin show cedb0ec4…:SCORECARD.md` (extracted to scratch; rows at :1972-1973, register header at :1959, register preamble :1943-1949).
- MANIFEST.json rounds[455] at fleet 37b51a24 via `git -C /home/vgpnk/Projects/shokunin show 37b51a24:MANIFEST.json`; capabilities_added at JSON path rounds[455].capabilities_added (scratch lines 13431-13432). round: 25, admitted: true, verdict: admitted, commit mori-shokunin@829d8c9….
- Closure record: corpus/lessons/round-25-verifier-spotcheck.md@248408f5b661 (210 lines) and .ufo/reports/round-25/mori.md@37b51a24 (255 lines).
- Closure commit confirmed a lane commit: `git show --stat 829d8c9…` in the lane adds .ufo/waves/round-25/w2/MutRoutedD1.md (the fleet repo has no such object; MANIFEST binds it as mori-shokunin@829d8c9…).
- Both evidence tools extracted at the closure commit: tools/mori-job-runway.py (690 lines), tools/mori-routed-r24.py (951 lines).
- LSP: no server was consulted; this is a frozen-revision blob review of markdown and Python extracted by `git show`, so text reads of extracted blobs are the primary evidence, not a grep substitute for a live workspace.
- Tooling directive record: no tool installed or updated; everything needed was present (git, python3, coreutils).

## Row 1 — `rounds[455].capabilities_added[0]` (SCORECARD.md@cedb0ec4:1972)

Cells: capability `harness background-job runway read`; what `Reads the configured
async.maxJobs from one settings file plus the binary clamp and default, and reports the
effective cap and a verdict (not a live job count); frozen selftest PASS 21/21; bounded to
block-style configs.`; evidence `` `tools/mori-job-runway.py` ``; round 25.

(a) Fact-by-fact against the record (MANIFEST JSON path rounds[455].capabilities_added[0], scratch MANIFEST line 13431):

1. Reads configured async.maxJobs from one settings file — record: `configured async.maxJobs from one settings file`. Match. Bound held: the tool itself scopes to one settings file, with project-level and environment overrides named out of scope (mori-job-runway.py@829d8c9:16-17, DEFAULT_CONFIG :110).
2. Plus the binary clamp and default — record: `binary clamp and setting default`. Match (Rule 2 clamp :30-36 with CLAMP_RE :113-115; Rule 3 setting default :37-39 with DEFAULT_RE :117).
3. Reports the effective cap and a verdict — record: `effective cap and verdict`. Match (Rule 4 effective = max(1, min(clamp, base)) :40-43, code :455; Rule 5 verdicts RUNWAY_* :44-47).
4. Parenthetical (not a live job count) — record bounds it: fleet report .ufo/reports/round-25/mori.md@37b51a24:50 names the live job count as still frontier; tool docstring :77 says the live count of running background jobs is not readable from outside. The row states the record's own bound, adds nothing.
5. Frozen selftest PASS 21/21 — record: `frozen selftest PASS 21/21 over cases 48df844a … evidence-verified at d3b7af2a, tool blob equal at head`. Match; spotcheck@248408f5b661:16 records it as evidence-verified, not re-run; the row makes no stronger claim.
6. Bounded to block-style configs — record: `bounded to block-style configs (72 of 307 probe configs read a false 100, routed R1)`. The row carries exactly the record's bound phrase; it omits the count detail and the R1 marker but states the same bound. The same scoped form is restated in the lane's own round-25 section (SCORECARD.md@cedb0ec4:1650-1651).

Non-empty; no fact in the cell is absent from or wider than the record.

(b) Evidence cell holds exactly one backticked path, `tools/mori-job-runway.py`; no prose. Holds.

VERDICT: rounds[455].capabilities_added[0] supported

(c) Pointer relevance: tools/mori-job-runway.py@829d8c9 implements this capability end to end — configured-state line grammar for one `async:` block (Rule 1 :18-28, code :299-346), binary clamp regex over installed-binary bytes (:30-36, :113-115), setting-default regex (:37-39, :117), effective-cap and verdict rules (:40-47, :437-470), and `--selftest` over the frozen cases printing MORI_JOB_RUNWAY_SELFTEST PASS n/N (:52-58, :561-604). This is the runway read itself, not another round-25 capability.

VERDICT: rounds[455].capabilities_added[0] pointer-relevance holds

## Row 2 — `rounds[455].capabilities_added[1]` (SCORECARD.md@cedb0ec4:1973)

Cells: capability `round-24 routed-defect and Axes-table check`; what `Checks round-24
defects D1-D3 and D5 from git objects plus D4 hygiene; 4 to 0, re-measured by the closure
with plain git reads; no registry row or selftest.`; evidence `` `tools/mori-routed-r24.py`
``; round 25.

(a) Fact-by-fact against the record (MANIFEST rounds[455].capabilities_added[1], scratch line 13432):

1. Checks round-24 defects D1-D3 and D5 from git objects plus D4 hygiene — record: `D1-D3 and D5 from git objects plus D4 hygiene`. Match, same shape and scope. The tool docstring states a read-only check of items D1..D5 against committed bytes (mori-routed-r24.py@829d8c9:2) and that every predicate reads git objects only (cat-file, ls-tree, archive, merge-base) (:8-9).
2. 4 to 0, re-measured by the closure with plain git reads — record: `4 -> 0 re-measured by plain git reads`; the closure identity and method are in the spotcheck, authored by the non-author closure: `C1 was re-measured with plain git reads (4 → 0)` (spotcheck@248408f5b661:15). Match; the row does not claim the tool re-measured it, only that the closure did.
3. No registry row or selftest — record: `no registry row or selftest yet (routed R5)`; spotcheck@248408f5b661:34-36 states both tools have no registry row in SKILL.md and mori-routed-r24.py has no self-test. The fact is stated by the record and restated in the row as a conservative disclosure. The row drops the `yet (routed R5)` bookkeeping — see finding N1; no capability is widened by the omission.

Non-empty; no fact is wider than the record.

(b) Evidence cell holds exactly one backticked path, `tools/mori-routed-r24.py`; no prose. Holds.

VERDICT: rounds[455].capabilities_added[1] supported

(c) Pointer relevance: tools/mori-routed-r24.py@829d8c9 implements this check — D1 stale gate evidence (:16-24, _check_d1 :436), D2 knowledge-entry correction sweep (:25-35, _check_d2 :528), D3 lesson count drift (:36-40, _check_d3 :758), D5 Axes table against pinned observed scores with the round-1 Last-change rule (:44-51, _check_d5 :691, constants :140-165), and D4 hygiene (:55-59, _check_d4 :825); exit 0 only when mismatches 0 and hygiene holds (:62-65, :946-947). It also confirms the row's own debt disclosure: its argparse offers only --repo and --rerun (:896-901), no selftest. This is the round-24 routed-defect and Axes-table check itself.

VERDICT: rounds[455].capabilities_added[1] pointer-relevance holds

## Findings by severity

- N1 (minor, row 2): the what cell drops the record's `yet (routed R5)` marker on the missing registry row and selftest. The fact and its conservative direction are preserved; only the round-26 routing pointer is lost from the row. The routing survives in the closure record (MANIFEST capabilities_added[1]) and spotcheck:34-36. Not a bound violation under the frozen rule; recorded as a fidelity nit.
- N2 (minor, row 1): the what cell omits the `(72 of 307 probe configs read a false 100, routed R1)` detail and the live-run RUNWAY_CLAMPED fact. The rule requires record-stated facts in cells, not record-exhaustive cells; the operative bound (block-style configs) is carried verbatim. No action implied by the rule.

No defect-class finding: no cell fact lacks a record statement, no bound is widened, both evidence cells are bare backticked paths, and both pointers resolve at the closure commit to the artifact that implements the named capability.

## Residual risk and verification gaps

- Pointer relevance was judged by reading the two tool sources extracted at 829d8c9, not by executing them; the frozen PASS 21/21 remains evidence-verified per the closure record (spotcheck:16), not re-run here. Mechanism-level code reading, cited above, is the basis.
- The 72-of-307 probe count is evidence-cited in the closure record itself (probe script not committed; spotcheck:80-81); the row does not repeat the count, so this gap does not touch the row.
- MANIFEST was read at the fleet commit 37b51a24 as assigned; the fleet working tree was not consulted and nothing in the fleet or lane repos was mutated (read-only git only; scratch under /fast/scratch/hyaku/mori-r35/JudgeRowsR25/).
- Counter count-c1.py was not run: the frozen decision rule for this seat is the per-row (a)/(b) judgment applied above, and no row-level question remained that the counter would answer.
