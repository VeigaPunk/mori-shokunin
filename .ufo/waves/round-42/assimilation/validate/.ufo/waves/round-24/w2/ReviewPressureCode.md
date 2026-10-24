# ReviewPressureCode: falsification review of `tools/mori-pressure.py` (C2, round 24, wave 2)

Seat: `MoriR24.ReviewPressureCode` (leaf; no subagents, no peer messages, no installs).
Pinned target: commit `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc`, file sha256
`852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5`, 569 lines.
The lane moved while I worked. I also tested the newer tip `a536b18` (`clone-a536` in the scratch tree).
The tool blob is unchanged from `a536b18` through the fleet HEAD `1046aca`, which I checked last.
Each finding below shows its status at the pin (P) and at `a536b18` (H).

Contract references are to `.ufo/waves/round-24/contract.md`. Tool line numbers are at the pin unless marked `a536b18`.
Scratch root: `/fast/scratch/hyaku/mori-r24-a2/w2/ReviewPressureCode/`.

## 1. Verdict

- The declared after-value `MORI_PRESSURE_SELFTEST: PASS 12/12`, exit 0, reproduces at the pin (repro block R0) and at `a536b18`.
- That result alone does not establish the behaviour the contract states:
  - F1 is the most material defect: it turns a high reading into exit 0. A counter that moves backwards hides a PRESSURE_HIGH reading, where the contract's A3 text gives exit 1.
  - F2 to F6 are strictness, classification and reporting gaps.
  - F7 and F9 are oracle gaps. A changed case file, and four tool or matcher mutants, pass the selftest.
- Fixed since the pin:
  - Non-UTF-8 content now reads as `malformed` (commit `6a344d2`; probe G20 changed from DEV to PASS).
  - The verdict-less matcher is now killed by new negative controls (commit `89849a7`; mutant M02 gives FAIL 12/12 at `a536b18`).

## 2. Findings by severity
Each finding names the `repro.sh` block (R0 to R13) that shows it in its Observed line. Running `bash $S/repro.sh` reproduces all of them in about 13 s, where `S=/fast/scratch/hyaku/mori-r24-a2/w2/ReviewPressureCode`.

### MEDIUM

**F1. A counter regression hides a threshold breach (exit 0 instead of exit 1). P, H.**
- Code: `tools/mori-pressure.py:287-288` `_findings` skips every resource whose state is not `ok`. The state becomes `counter_regressed` at `:275-279`, after both reads parsed `ok`. At `a536b18` the skip is at line 290.
- Contract: `contract.md:131-132` (A3): "thresholds use the second read when both reads are ok". `contract.md:133` says `counter_regressed` counts toward PARTIAL. The tool's own docstring (`:32-34`) repeats the A3 rule.
  - The literal reading: a regressed resource whose reads both parsed gets its threshold evaluated.
  - If the lane intends "no threshold for a regressed counter", A3 must say so. As written, the code contradicts its docstring.
- Observed (R1): `{"verdict":"PRESSURE_PARTIAL","memory":"counter_regressed","memory_some_avg10":50.0,"findings":0}`, exit 0.
  - Same payload relabelled `ok`: `_findings` returns `PRESSURE_HIGH` (pure-function check, `_eval` in the scratch session).
- Reproduce: `bash /fast/scratch/hyaku/mori-r24-a2/w2/ReviewPressureCode/repro.sh`, block R1. Probe check I04 gives the same DEV at both tips.
- Fix direction (not applied, as the lane owns the edit): evaluate thresholds on the second read whenever both reads parse, or amend A3 and state the suppression.

### LOW

**F2. A 4301-digit `total=` aborts the whole run as a usage error. P, H.**
- Code: `:184` `int(match.group(5))` raises `ValueError` past CPython 3.14's default limit of 4300 digits (`sys.get_int_max_str_digits()` returned 4300).
  - `:165` runs the parse outside the `try` at `:153-164`.
  - `:559-563` `main` catches the `ValueError` and calls `_emit_error` (`:394`), exit 2.
- Contract: `contract.md:62-63` (other shape → resource state `malformed`); `contract.md:77-79` (exit 2 only when every resource is unavailable or on usage error).
- Observed (R3): exit 2, `{"error":"Exceeds the limit (4300 digits) for integer string conversion…","root":"/proc/pressure"}`. No resource is reported.
- Reach: [INFERENCE] kernel PSI totals are 64-bit counters, so the kernel should not print such numbers. This is a classification defect, not a kernel-reachable failure. I did not check the kernel source here.

**F3. Output is not standard JSON for huge decimals or tiny intervals. P, H.**
- Code:
  - `:181-183` `float()` returns inf for a decimal too large for a double.
  - `:274` `round(delta / (interval_s * 1e6), 6)` returns inf for a subnormal interval.
  - `:390` `json.dumps` with the default `allow_nan=True` writes `Infinity`.
- Contract: `contract.md:75-76` "Output: one JSON object".
- Observed:
  - R4 (400-digit avg10): exit 1 (HIGH), and `strict JSON: invalid (non-standard constant Infinity)`.
  - `_combine_interval` with `interval_s=1e-320` and a delta of 1 returns `stall_ratio` inf, which serialises as `Infinity`.

**F4. The grammar accepts CRLF and non-LF line separators. P, H.**
- Code: `:170-171` `text.splitlines()` and `rstrip("\r")`. `:157` text-mode `open` maps CRLF to LF.
- Contract: `contract.md:61-62` (the regex ends at `$`); `contract.md:62-63` (other shape → malformed).
- Observed (R2): a U+2028 separator between the two lines gives `memory ok` and `PRESSURE_OK`, exit 0. A CRLF file also gives `memory ok`. Probe G15 (U+000C) is accepted too.
- Impact: live kernel files use LF (see §6). The strictness claim is still not met literally.

**F5. `stall_ratio` is rounded to six places, so a non-zero movement reads 0.0. P, H.**
- Code: `:274` (`a536b18` `:277`).
- Contract: `contract.md:72-73` gives `stall_ratio = total_delta_us / (S * 1e6)` and says nothing about rounding.
- Observed (R5): delta 1 µs over S=3 gives `memory_stall_ratio: 0.0` (unrounded value 3.33e-07).

**F6. Error JSON always reports `/proc/pressure` as the root. P, H.**
- Code: `:394` `_emit_error` hard-codes `DEFAULT_ROOT` (`a536b18` `:398-399`). The `--cases`-without-`--selftest` error at `a536b18` `:596-597` inherits it.
- Observed (R10): `--root /nonexistent-psi-root --interval 0` gives `{"error":"--interval must satisfy 0 < S <= 10","root":"/proc/pressure"}`, exit 2.

**F7. The selftest does not pin the frozen case set, so a changed file prints the same line. P, H.**
- Code: `:514-515` takes the case count from whatever the file holds. At `a536b18`, `--cases` (`:389`, `:599-600`) runs any file and prints no file identity. The only new output line is the MATCHER line at `a536b18` `:585`.
- Contract: `contract.md:80-82` (12 frozen cases P01–P12; after-value `PASS 12/12`).
- Observed:
  - R8 (P12 replaced by a copy of P01 in `cases.json`): `MORI_PRESSURE_SELFTEST: PASS 12/12`, exit 0, at both tips.
  - S04 (P12 dropped): `PASS 11/11`, exit 0, at both tips.
  - At `a536b18`, `--selftest --cases supplementary-cases.json`: `PASS 6/6`, exit 0.
- What does hold: the default fixture is unchanged since `f6a2970`: git blob `39cc96ab…` at `f6a2970`, `a730ecf` and HEAD, file sha256 `aeb80ea0…`. `f6a2970` is an ancestor of the tool's landing commit `6ee6248` (checked with `git merge-base --is-ancestor`). The freeze lives in git history, not in the tool.
- Fix direction: print the case file path and sha256 in the selftest output, and pin the id list and count (or the blob hash).

**F8. A non-object `cases.json` gives a traceback and exit 1. P, H.**
- Code: `:503-506` catches only `OSError` and `ValueError`. `:510` calls `document.get` on whatever was decoded.
- Observed (R9): `AttributeError: 'list' object has no attribute 'get'`, exit 1. Exit 1 also means PRESSURE_HIGH and selftest FAIL (see O2).

**F9. Oracle survivors: mutants the frozen selftest does not kill. P (a, b, c); H (a, b, c, d).**
Mutants are scratch copies. With `S=/fast/scratch/hyaku/mori-r24-a2/w2/ReviewPressureCode`, each command below prints the selftest result:
- Command for mutant (a): `python3 -I $S/probe/mut3-a730ecf-bound/tools/mori-pressure.py --selftest` (also in R13).
- Command for mutant (b): `python3 -I $S/probe/mut4-eperm/tools/mori-pressure.py --selftest`.
- Command for mutant (c): `python3 -I $S/probe/mut-Mx2-some-full-numbers-unchecked/tools/mori-pressure.py --selftest` (copy built from a536b18).
- Command for mutant (d): `python3 -I $S/probe/mut-Mx3-irq-resource-unchecked/tools/mori-pressure.py --selftest` (copy built from a536b18).
- Composite of mutant (c) with the delta off-by-one: `$S/probe/mut3-a730ecf-delta-mx2/` and `$S/probe/mut3-a536b18-delta-mx2/` (both in R13).
- (a) Boundary. `:297` `avg10 >= warn_avg10` changed to `>`. Selftest: `PASS 12/12` at both tips.
  - Behaviour check (run): `--warn-avg10 10` with a reading of exactly 10.00 gives pinned `PRESSURE_HIGH` exit 1, and the mutant gives `PRESSURE_OK` exit 0.
  - Contract `contract.md:71` says ≥. The same equality case, run by hand on both trees, shows the difference (pinned exit 1, mutant exit 0). Probe check V02 tests exactly this case, but the frozen set does not.
- (b) EPERM mapping. `:145-146` changed to return `STATE_ABSENT`. Selftest: `PASS 12/12` at the pin.
  - No frozen case uses EPERM. The only error tokens in `cases.json` are EACCES and EOPNOTSUPP (checked with `jq`).
  - `contract.md:68-69` names EPERM.
- (c) Numeric matcher blind spot. The matcher's numeric comparison (`:479` at the pin, `elif actual_value[k2] != v2`) disabled.
  - At `a536b18`, the new controls still reject 48 of 48, so numeric fields have no negative control. That mutant alone passes `12/12`.
  - At the pin, a tool delta off-by-one (`:272`) combined with this matcher mutant also passes `PASS 12/12`. At `a536b18` the same combination passes too, with 48 of 48 controls rejected (R13).
  - The delta off-by-one alone is killed by P11 (`FAIL 11/12` at both tips).
- (d) State-control scope. At `a536b18` the state control mutates only the first resource that has a state (`:517-522`, then `break`). A matcher that stops checking irq's state passes `12/12`.
- Single point at the pin: the verdict comparison (`:459-460`) is the only thing that kills PARTIAL→OK. M01 gives `FAIL 7/12` with it; M02 (verdict check removed) gives `PASS 12/12` without it. At `a536b18`, M02 gives `FAIL 12/12`, so this part is fixed.

### LOW: question

**F10. A decreasing system cpu `full` total is never flagged. P, H (decision needed).**
- Code: `:267-271` set the delta to null and `continue` before the regression test at `:275-276`.
- Contract: `contract.md:130` (cpu `full` deltas are null) and `contract.md:133` (`counter_regressed` on any decreasing total). The two readings disagree, and the tool takes the first.
- Observed (R6, total 100→50): `cpu.state ok`, `total_delta_us null`.
- Decision for the lane: either flag it, or say in A3 that system cpu `full` has no monotonicity check.

### LOW: robustness

**F11. `open()` on a FIFO at a PSI name blocks with no bound. P, H.**
- Code: `:157` (no timeout, no non-blocking open). `a536b18` `:157` is the same open.
- Observed (R7): `timeout 5` returns 124, so the open was still blocked. Same at `a536b18`.
- Exposure: custom `--root` trees only. The default files are regular procfs files (see §6).

### Nits (no action needed for the verdict)
- `:425` an unknown error token silently maps to `EIO` (a case-authoring hazard).
- `:264-266` an irq `some` present only in the second read gives a `some` object with no `total_delta_us` or `stall_ratio` keys (unit check: keys `avg10, avg300, avg60, total`).
- `:65` `import math` sits after the `typing` import. `:319-325` `start` is bound in one branch only. `:401` duplicates a candidate path.

## 3. Observations (not defects) and residual risk

- O1 (`:342-343`): four malformed resources give `PRESSURE_PARTIAL` with exit 0 (probe V14). The contract's literal rule gives this. A consumer that treats exit 0 as healthy would miss an all-malformed host.
- O2: exit 1 is shared by PRESSURE_HIGH, selftest FAIL, and any uncaught exception (F8). Exit code alone cannot tell a crash from HIGH.
- O3 (`a536b18` `:585`): `--selftest` prints a second line, `MATCHER: rejected 48/48 corrupted expectations`. The after-value line is still line 1. A consumer that compares the whole stdout would see a difference. Probe checks S01, S02 and H02 flag this for the same reason. They are probe artifacts, not tool defects.
- O4 (`:147-148`): ENOTDIR (the root is a regular file) maps to unreadable. The contract names three errnos only. The docstring documents this extension. Observed as all unavailable, exit 2 (E04).
- O5 (`:140-142`): EOPNOTSUPP maps to `unsupported` with no cause, per A2. There is no PSI-disabled host here, so this is exercised only through the hook.

## 4. Held: checked, no defect at the pin

- Grammar (probe G01–G33): the strict regex rejects an exponent, negative and fractional totals, a trailing space, an uppercase kind, duplicate and unknown kinds, a missing `avg300`, an empty file, a blank tail, NBSP, BOM, an Arabic-Indic digit and NUL.
  - irq full-only gives `ok` with `some: null`. irq some-only gives `malformed`. cpu missing `full` gives `malformed`.
  - A 4300-digit total is accepted (boundary).
- Errno mapping:
  - ENOENT → absent (E01); EISDIR → unreadable (E02); EACCES → unreadable as uid 1000 (E03); ENOTDIR → unreadable (E04).
  - Missing root → exit 2 (E05); all EACCES → exit 2 (E06); mixed → PARTIAL exit 0 (E07).
  - The selftest kills EOPNOTSUPP→absent and EACCES→absent (M03, M04: `FAIL 11/12` each).
- Interval:
  - Identical snapshots give zero deltas, null cpu `full` deltas, and an integer `elapsed_us` (I01).
  - A 1e7 µs move over S=2 gives a ratio of 5.0 (I02).
  - Second read absent gives absent with no delta (I06). First read malformed gives malformed with no delta (I07). Both absent gives absent (I08).
  - S outside (0, 10] gives exit 2 (I09).
- Verdict and exit:
  - HIGH beats PARTIAL (V13). Equality is HIGH (V02).
  - cpu `full` and irq `some` are never thresholded (V04, V05). io `full`, cpu `some` and irq `full` are thresholded (V06–V08).
  - All absent gives UNAVAILABLE, exit 2 (V15, E05, E06).
  - Usage errors give exit 2 (U01–U07, V10–V12, I09). `--help` gives exit 0 (U08).
- Hook isolation:
  - `_OPEN_HOOK` and `_SLEEP_HOOK` are assigned only at `:450-451`, inside `_case_failures`. Only `_selftest` calls that (`:527`).
  - `_selftest` restores them in its `finally` (`:532-534`). `_SELFTEST_RUNNING` is set at `:523` and cleared at `:534`.
  - Other reads of the hooks are at `:154-155`, `:228-229`, `:319` and `:324`.
  - Runtime: normal runs open the real paths. strace shows `openat(…/U00-base/cpu, O_RDONLY)` and the same for memory, io and irq.
- No writes: strace (`-e trace=%file`, strace 7.2) over one-shot, interval, selftest and usage runs. Zero write-mode opens in all four traces (R11). Two hits from my own regex for "mutating" calls were `readlink(` matches, not writes.
- `python3 -I`:
  - Without `-I`, a shadowing `json.py` in the script directory wins (exit 99, R12 control).
  - With `-I` and `PYTHONPATH` pointing at the shadow, the selftest passes 12/12 (R12; probe H02).
- Selftest: `PASS 12/12` with `-I` from the clone (S01), and without `-I` from `/` (S02). An altered expectation gives `FAIL 11/12`, exit 1 (S05).
- Frozen case topics P01–P12 match `contract.md:85-91` for verdict and exit (all 12 cases). State expectations were checked for P02–P05, P08, P10–P12. The selftest compares the P11 delta expectations, and they pass at the pin (S01).

## 5. Fixed or changed since the pin

- `6a344d2` (commit time 06:03:35 -03:00): non-UTF-8 content now gives `malformed`. The new clause is at `a536b18` `:162-164`, ahead of the generic `except Exception`. Probe G20 changed from DEV (unreadable) to PASS (malformed).
- `89849a7` (commit time 05:59:07 -03:00): adds negative controls (`_corrupted_expectations`, `a536b18` `:501`), the `--cases` option, and `supplementary-cases.json` (6 cases).
  - Closes the verdict-less matcher (M02).
  - Adds the F7 surface and does not close F9 (a) to (d).
- The uncommitted working-tree edit I first saw (614 lines, sha256 `f2e39df3…`) is byte-identical to the `89849a7` blob (`git show 89849a7:tools/mori-pressure.py | sha256sum`). I used only committed bytes.

## 6. Live host (read-only)

- `cat /proc/pressure/{cpu,memory,io,irq}`: the grammar matches. irq has only a `full` line. cpu `full` total is 0. All four files are ASCII with LF line ends and zero CR bytes (checked with `od` and a byte count).
- `python3 -I tools/mori-pressure.py` (default root): `"verdict": "PRESSURE_OK"`, all four `ok`, irq `some: null`, exit 0.
- This is not the A2 bracket check (committed at `6a344d2`, outside this seat's list).

## 7. Verification gaps

- Read-time errno mapping cannot be exercised on its own. `:153-158` uses one `try` for open and read, and the hook covers the pair. The mapping is checked by reading only.
- EPERM mapping is untested by the frozen cases (F9 b).
- Interval tests use a real race: write at 1.0 s, interval 2 or 3 s. Each run's observed deltas confirmed the order. A loaded host could in principle reorder. I did not repeat runs to test flakiness.
- `supplementary-cases.json` was run (PASS 6/6) but not reviewed as a co-evolved fixture.
- The reach statements in F2 and F3 depend on kernel numeric formats, which I inferred and did not check against kernel source.
- ruff output (158 findings, mostly style) was not used as evidence. pyflakes was clean at the pin.

## 8. Reproduction index

- Pinned clone (checked out `a730ecf`): `/fast/scratch/hyaku/mori-r24-a2/w2/ReviewPressureCode/clone`.
- Newest-tip clone (checked out `a536b18`): `…/ReviewPressureCode/clone-a536`.
- Reproducers: `…/ReviewPressureCode/repro.sh`, blocks R0 to R13, about 13 s. Output: `…/ReviewPressureCode/repro-output.txt`.
- Probe: `…/ReviewPressureCode/probe/probe.py all`, 86 checks.
  - `probe/results-a730ecf.json`: 73 pass, 13 deviate.
  - `probe/results-a536b18.json`: 72 pass, 14 deviate.
  - Logs: `probe/run-a730ecf.log`, `probe/run-a536b18.log`.
- Mutants: `probe/mut3-*`, `probe/mut4-eperm`, `probe/variant-*`, `probe/mut-*`, `probe/mut2-*`.
- Traces: `probe/trace-{oneshot,interval,selftest,usage}.txt`.
- Diffs: `diff-89849a7-to-a536b18.patch`, `diff-fixtures-a730-89849a7.patch`, `worktree-at-review-start.py`.

## 9. Tooling record

- No installs or updates by this seat. Tools used: strace 7.2, pyflakes, ruff 0.17.1, jq, Python 3.14.8 (system), and uv 0.13.0 (present, not invoked).
- No pacman, no `/proc` or `/sys` writes, no PSI trigger registration, no cgroup writes, no service changes.
- Fleet repo: read-only git only (`show`, `log`, `diff`, `branch --contains`, `merge-base`, `cat-file`, `rev-parse`, and `clone --no-hardlinks` into scratch). No commit, stash, checkout, reset or index write in the lane.

## 10. Status summary

| ID | Severity | Pin `a730ecf` | Tip `a536b18` | Note |
|---|---|---|---|---|
| F1 | MEDIUM | present | present | threshold hidden by `counter_regressed` |
| F2 | LOW | present | present | 4301-digit total gives exit 2 |
| F3 | LOW | present | present | `Infinity` in output |
| F4 | LOW | present | present | CRLF and U+2028 accepted |
| F5 | LOW | present | present | `stall_ratio` rounded |
| F6 | LOW | present | present | error JSON root hard-coded to `/proc/pressure` |
| F7 | LOW | present | present | frozen set not pinned by the tool |
| F8 | LOW | present | present | list `cases.json` gives traceback |
| F9 | LOW | present (a, b, c) | present (a, b, c, d) | oracle survivors; verdict single point fixed at `a536b18` |
| F10 | LOW (question) | present | present | cpu `full` decrease unflagged |
| F11 | LOW | present | present | FIFO open blocks |
| UTF-8 classification | n/a | DEV (probe G20) | fixed (`6a344d2`) | now `malformed` |
