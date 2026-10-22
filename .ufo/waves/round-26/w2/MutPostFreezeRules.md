# MutPostFreezeRules — mutation test of the A2 post-freeze rules (round 26, wave 2)

Seat: `MoriR26.MutPostFreezeRules` (mutation tester, leaf).
Lane: `mori-shokunin`; lane tip under attack `16935e24c93fa7e7567413d7ec091339a5df1474`.
Sandbox clone: `/fast/scratch/hyaku/mori-r26/wt-w2mutRules` (branch `r26-wt-w2mutRules`, base
`16935e24`, clean before and after).
Tool under test: `tools/mori-oom-killers.py` (sandbox blob `44dac3fd6cb1320752a226a360f29d1805ce93f3`,
byte-identical to `git rev-parse 16935e24:tools/mori-oom-killers.py` in the lane).
Attack target: amendment A2 (`.ufo/waves/round-26/contract.md`, "Amendment A2 (2026-10-22, after the
tool landed; tool rules only, counted value unchanged)"), i.e. the eight post-freeze rules the frozen
case file predates.

## Method

1. Baseline: `python3 -I -B tools/mori-oom-killers.py --selftest` → `MORI_OOM_KILLERS_SELFTEST: PASS
   32/32`, exit 0; the same with `--cases .../cases-supplementary.json` → `PASS 32/32`, exit 0.
2. For each rule: one exact-string revert applied to the sandbox copy of the tool (one behaviour-bearing
   point, no other change), then the two case files plus one invented-input detector are run on the
   mutated bytes; the file is then restored byte-for-byte and the same detectors are re-run.
3. Harness: `/fast/scratch/hyaku/mori-r26/MutPostFreezeRules/run_mutants.py`; raw results
   `results/summary.json`; invented inputs `inputs/*.json`; live-probe stubs `stub/`.
4. Baseline sha256 of the tool: `1a71b2dfa45ef547b1a5042cc71a28ae63f54af35d0c4973f6056bf439b2f8e4`.
   Every mutant below restored to exactly that hash (`restoration_ok: true` for all eight).

## Verdict table

| Mutant | Rule (A2 clause) | Tool line | Frozen file | Supplementary file | Invented-input detector | Verdict |
|---|---|---|---|---|---|---|
| M1 | A1b suppressed line → scope incomplete | `tools/mori-oom-killers.py:378` | survives | survives | **kills** (`inputs/m1-suppressed.json`) | killed |
| M2 | A2b non-steady `ActiveState` → unavailable | `tools/mori-oom-killers.py:212` | survives | survives | **kills** (`inputs/m2-nonsteady.json`) | killed |
| M3 | A6 dry-run send lines | `tools/mori-oom-killers.py:372` | survives | survives | **kills** (`inputs/m3-dryrun-send.json`) | killed |
| M4 | A5 process-group lines | `tools/mori-oom-killers.py:362` | survives | survives | **kills** (`inputs/m4-process-group.json`, field only) | killed (weak) |
| M5 | earlier-invocation send lines are positive evidence when not active | `tools/mori-oom-killers.py:422` | survives | survives | **kills** (`inputs/m5-earlier-invocation.json`) | killed |
| M6 | malformed timestamp → setup error | `tools/mori-oom-killers.py:296` | survives | **kills** (`FAIL 31/32`, case `c35`) | kills as well | killed |
| M7 | AETM 0 / missing → unbounded invocation, scope incomplete | `tools/mori-oom-killers.py:279` | survives | survives | **kills** (`inputs/m7-aetm-zero.json`) | killed |
| M8 | A1c live journal readability probe | `tools/mori-oom-killers.py:545`, `:558-559` | survives | survives | **kills** (live mode, stub PATH) | killed |

No mutant was inconclusive (every baseline detector passed on pristine bytes before mutation).

## Per-mutant detail

**M1 — A1b, suppressed journald notice.** Revert: `scope_complete = scope_known and version is not None
and not suppressed` → `scope_complete = scope_known and version is not None` (line 378).
Expected detector: a journal line `Suppressed 12 messages from earlyoom.service` inside the scope must
force `scope_complete: false` → `KILLERS_UNKNOWN`, exit 2.
Output — pristine: `"earlyoom.scope_complete": false`, `"verdict": "KILLERS_UNKNOWN"`, exit 2.
Mutant: `"earlyoom.scope_complete": true`, `"verdict": "KILLERS_QUIET"`, exit 0.
Killed by `inputs/m1-suppressed.json` (invented thresholds 10.00/10.00/5.00/5.00, no process names).
Both case files pass on the mutant (`PASS 32/32` each) → the frozen file does not cover A1b.

**M2 — A2b, non-steady `ActiveState`.** Revert: the final `return "unavailable"` of `unit_state`
(line 212) → `return "inactive"`, i.e. a failed/activating/deactivating/reloading/maintenance unit is
read as a stopped killer again.
Expected detector: `ActiveState=failed` → state `unavailable` → `KILLERS_UNKNOWN`, exit 2.
Output — pristine: `"earlyoom.state": "unavailable"`, `"verdict": "KILLERS_UNKNOWN"`, exit 2.
Mutant: `"earlyoom.state": "inactive"`, `"verdict": "KILLERS_QUIET"`, exit 0.
Killed by `inputs/m2-nonsteady.json`. Both case files pass on the mutant.

**M3 — A6, dry-run send lines.** Revert: drop the block that moves `counts["sigterm"]`/`["sigkill"]`
into `dryrun_send_lines` and zeroes them (lines 370-374).
Expected detector: a journal with `dryrun mode enabled` plus a send line → `dryrun: true`,
`actions.sigterm: 0`, `dryrun_send_lines: 1`, `KILLERS_QUIET`, exit 0.
Output — pristine: `"dryrun_send_lines": 1`, `"actions": {…"sigterm": 0…}`, `"verdict": "KILLERS_QUIET"`,
exit 0. Mutant: `"dryrun_send_lines": 0`, `"actions": {…"sigterm": 1…}`, `"verdict": "KILLER_ACTED"`,
exit 1.
Killed by `inputs/m3-dryrun-send.json`. Both case files pass on the mutant (frozen `c18` has the dry-run
flag but no send line, so it cannot see the revert).

**M4 — A5, process-group lines.** Revert: `process_group_lines += 1` → `pass` (lines 362-363).
Expected detector: a `killing whole process group …` line → `process_group_lines: 1`.
Output — pristine: `"process_group_lines": 1`, verdict `KILLERS_QUIET`, exit 0.
Mutant: `"process_group_lines": 0`, verdict `KILLERS_QUIET`, exit 0.
Killed by `inputs/m4-process-group.json`, but **only on the field**: verdict and exit are identical, so a
verdict-only detector cannot see this revert. The supplementary file *does* contain a process-group line
(case `c21-nearmiss-midline-sigkill`) but asserts no `process_group_lines` field, so it also passes on
the mutant (`PASS 32/32`).

**M5 — earlier invocations are positive evidence when earlyoom is not active.** Revert: drop the term
`or (earlyoom_state != "active" and earlier_send_lines)` from the `acted` expression (line 422). The
reported field `earlyoom.earlier_invocation_send_lines` is left in place (it is the reporting half of
the same adopted clause).
Expected detector: an inactive earlyoom whose boot journal holds a send line → `KILLER_ACTED`, exit 1
(a stop without restart must not read quiet).
Output — pristine: `"earlier_invocation_send_lines": 1`, `"verdict": "KILLER_ACTED"`, exit 1.
Mutant: `"earlier_invocation_send_lines": 1`, `"verdict": "KILLERS_QUIET"`, exit 0.
Killed by `inputs/m5-earlier-invocation.json`. Both case files pass on the mutant (frozen `c02` pins
`KILLERS_QUIET` for the *active* shape, which this rule deliberately does not change).

**M6 — malformed timestamp is a setup error.** Revert: `raise SetupError("journal record without a
numeric __MONOTONIC_TIMESTAMP")` → `continue` (line 296).
Expected detector: a record whose `__MONOTONIC_TIMESTAMP` is not numeric → `KILLERS_UNKNOWN`, exit 2,
`error` field present.
Output — pristine: `{"earlyoom": null, "error": "journal record without a numeric __MONOTONIC_TIMESTAMP",
"verdict": "KILLERS_UNKNOWN"}`, exit 2. Mutant: `"verdict": "KILLERS_QUIET"`, exit 0.
**Killed by the supplementary file**: `--selftest --cases cases-supplementary.json` prints
`MORI_OOM_KILLERS_SELFTEST: FAIL 31/32` with `FAIL c35-malformed-monotonic-timestamp: verdict: got
'KILLERS_QUIET' expected 'KILLERS_UNKNOWN'` and `exit: got 0 expected 2`. The frozen file passes on the
mutant (`PASS 32/32`), so this is the only rule of the eight that the supplementary file covers.

**M7 — unbounded invocation when AETM is missing or 0.** Revert: `if aetm is None or aetm == 0:` →
`if aetm is None:` (line 279), so `ActiveEnterTimestampMonotonic=0` bounds the invocation again.
Expected detector: an active earlyoom with `ActiveEnterTimestampMonotonic=0` → `scope_complete: false`
→ `KILLERS_UNKNOWN`, exit 2.
Output — pristine: `"scope_complete": false`, `"verdict": "KILLERS_UNKNOWN"`, exit 2.
Mutant: `"scope_complete": true`, `"verdict": "KILLERS_QUIET"`, exit 0.
Killed by `inputs/m7-aetm-zero.json`. Both case files pass on the mutant (their `AETM=0` cases
`c06`/`c07`/`c29` have an inactive/absent earlyoom, so the rule never applies).

**M8 — A1c live journal readability probe.** Revert: `"earlyoom_journal": _collect_journal() if readable
else None` / `"oomd_notices": _collect_oomd_notices() if readable else None` (lines 558-559) → both
reads unconditional; `_system_journal_readable()` (line 545) is then unused.
Expected detector: live mode with an unreadable journal (the PID-1 probe answers nothing) → the reads
count as `null`, not as an empty journal.
Detector used: live mode with `stub/journalctl` (answers nothing, exit 0 — what `journalctl -q` does on
an inaccessible system journal) and `stub/systemctl` (fixed invented properties) first on `PATH`.
Output — pristine: `"actions": null`, `"oomd": {"notices_this_boot": null}`, verdict `KILLERS_UNKNOWN`,
exit 2. Mutant: `"actions": {…"sigterm": 0…}`, `"oomd": {"notices_this_boot": 0}`, verdict
`KILLERS_UNKNOWN`, exit 2. The mutant reports *counts of an unreadable journal* instead of "unreadable",
which the tool itself forbids (contract C2 verdict 2: a needed read that is `null` means the counts are
unavailable, not zero — the pristine branch `elif journal is None:` sets `actions = None`).
**This rule cannot be exercised through `--inputs`**: the `--inputs` branch
(`tools/mori-oom-killers.py:789-790`) loads the JSON file and never calls `collect_live()`
(`tools/mori-oom-killers.py:792`), so no JSON inputs object can kill M8. It is the one rule of the
eight with no `--inputs` detector, and it is also the one no case file can reach.

## Findings (coverage, not contract changes)

1. **The frozen case file kills none of the eight post-freeze rules.** All eight mutants pass
   `PASS 32/32` on `tools/fixtures/mori-oom-killers/cases.json`. The counted value `PASS 32/32` therefore
   certifies only the pre-freeze behaviour; the A2 rules are untested by it.
2. **The supplementary file kills exactly one of the eight** (M6, malformed timestamp, via `c35`). The
   other seven survive it, so `PASS 32/32` on the supplementary file is also no evidence for A1b, A2b,
   A5, A6, the earlier-invocation clause, the AETM-0 clause or A1c.
3. **A5 (process-group lines) is invisible to any verdict-based detector**: the rule changes only the
   `earlyoom.process_group_lines` count; verdict and exit stay the same (M4 output above). The
   supplementary file already carries a process-group line in `c21` but asserts no field for it.
4. **A1c is unreachable from the JSON inputs interface** (M8): it is live-mode-only, so it needs the
   stub-PATH live probe above. The amended contract states this ("live mode only").
5. Side observation, not a mutation result: `cases-supplementary.json` is not a superset of
   `cases.json` — it drops frozen `c19-version-line-only`, `c24-nearmiss-kill-failed-without-colon` and
   `c28-oomd-active-quiet` and adds `c33`/`c34`/`c35`, so it is 32 cases but not the frozen set plus
   extras. Running it alone loses three frozen checks.

## Restoration evidence

Every mutant was reverted by rewriting the exact baseline bytes; the file was then re-hashed and the
detectors re-run.

| Mutant | mutated sha256 | restored sha256 | restored == baseline |
|---|---|---|---|
| M1 | `a2023b69c2199efcdc767313c1c3e5072354a72742270155ebb52f5b1b7a1f80` | `1a71b2df…2f8e4` | yes |
| M2 | `97f76424ab898886c42218c7a56a76106d6efee5168b966e508df10f13739ec9` | `1a71b2df…2f8e4` | yes |
| M3 | `d4c956eaebf2cc35b5b31f06c3bcaad7d5dff3917bef87337893e7dde7d1be9a` | `1a71b2df…2f8e4` | yes |
| M4 | `f49e853589c4c92c91df9463260cb2dd2864317e47f7842539bcf352510eb75a` | `1a71b2df…2f8e4` | yes |
| M5 | `64967c9a95cd0cb98addb272537d710a70acc56c6c764e593af7e9b597f08d38` | `1a71b2df…2f8e4` | yes |
| M6 | `788effbd8ba689e641f41b8357086d1b0b9fcb09aebe14e6c90078f5ddf613a8` | `1a71b2df…2f8e4` | yes |
| M7 | `beea9bcdfb15ca727076225152b5dcf07f42bb9e0eaf90ebd13e02112c1aba91` | `1a71b2df…2f8e4` | yes |
| M8 | `b42b34c423b903820413f4db5cf9b52ec8f8b0a547a92abadaf90132f1dfeb1c` | `1a71b2df…2f8e4` | yes |

`git status --porcelain` in the sandbox clone is empty after the run; the lane repo was never written
to (no `git add/commit/checkout` in the lane; the only lane write is this report file).
Re-running the detectors on the restored bytes reproduces the baseline: frozen `PASS 32/32`,
supplementary `PASS 32/32`, and the live probe reproduces the pristine JSON.

## Tooling record

No package was installed or upgraded: the harness needs only Python 3 standard library.
Python 3.14.8 (`python3 -VV`), git 2.56.0. No pacman transaction, no `uv tool install`, no service
restart, no network access, no change to operator settings or MCP files.

## Files written

- This report: `.ufo/waves/round-26/w2/MutPostFreezeRules.md` (lane).
- Sandbox clone: `/fast/scratch/hyaku/mori-r26/wt-w2mutRules` (branch `r26-wt-w2mutRules`, unmodified
  in the end; only the working-tree copy of `tools/mori-oom-killers.py` was mutated and restored).
- Harness and evidence: `/fast/scratch/hyaku/mori-r26/MutPostFreezeRules/{run_mutants.py, inputs/,
  stub/, results/summary.json}`.
