# Mo56MutDriver1 — mutation probes: tools/mori-driver-liveness.py (round 56, wave w1)

Date: 2026-10-27. Role: mutation tester (C1 coverage instrument). Leaf seat: no subagents.
Target: `tools/mori-driver-liveness.py`, pristine sha256
`6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997`. Provenance: the working-tree
file equals the freeze-tip blob — `git cat-file -p 8be2717b0809281d07dffe83dad424a4859e0747:tools/mori-driver-liveness.py`
hashes to the same value (git blob `be8dd1ed0dfc7857e556535cbc9684b3b4c0786c`, mode 100755),
and `git status --porcelain tools/mori-driver-liveness.py` is empty. All mutation work ran on
scratch copies under `/fast/scratch/hyaku/mori-r56/Mo56MutDriver1/`; the fleet repo file was
never opened for writing (re-hashed after the run: unchanged; `git status --porcelain` for the
file: empty, rc 0).

## Method (bounded detector)

1. Baseline on pristine bytes, run twice, asserted identical and equal to the frozen expectation:
   `python3 <tool> --selftest` -> stdout `DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0`, rc 0.
   A baseline failure would have made every verdict inconclusive; it did not occur.
2. Eleven mutants, one smallest behavior-bearing point each, applied as exact one-occurrence
   string replacements (each replacement asserted `count==1` in the pristine text before use).
3. Detector per mutant, run with the mutant placed at `<scratch>/work/repo/tools/mori-driver-liveness.py`
   so the selftest's repo-relative fixture root resolves:
   a. `--selftest` — KILLED iff rc != 0 (the frozen selftest is C1's pinned instrument, so this
      rc rule is the verdict of record).
   b. Coverage probe: `--fixture <dir> --now 1800000000` over each of the 9 frozen fixtures,
      JSON+rc diffed against the pristine tool's output for the same invocation; a fixture
      "catches" the mutant iff output or rc differs. Pristine fixture outputs were recorded twice
      and asserted identical (determinism check); all 9 pristine fixture runs exit rc 0.
4. Restoration: pristine bytes written back into the run tree, sha256 re-compared, selftest re-run.

Detector-validity note (disclosed for calibration): a first harness draft ran the mutants from a
`mutants/` directory outside the run tree; the selftest's `_fixture_dir()` resolved against the
script location, found no fixture tree, and 11 fixture-dependent cases reported as *skipped*
(observed line: `DRIVER_LIVENESS_SELFTEST pass=2 fail=0 skipped=11`), which would have produced
false SURVIVED verdicts. The harness was corrected to place every probe in-tree and to hard-fail
(INCONCLUSIVE, exit 3) unless the pristine baseline prints exactly `pass=13 fail=0 skipped=0`.
All verdicts below come from the corrected run only. No tool was installed or upgraded for this
seat (tooling authorization: nothing used; pacman untouched per the 2026-10-20 pause).
Disk guard checked before the run: `/fast/scratch/hyaku` 28% used, 583.2G free (rc 0).

## Verdicts (KILLED iff selftest rc != 0)

| id | mutated point | selftest | verdict | killing case(s) | fixtures NOT catching it |
|----|---------------|----------|---------|-----------------|--------------------------|
| M01 | `LAUNCH_REST_RE` opened to `r".*"` (accept any launch rest) | rc 1, pass=3 fail=10 | KILLED | `t_hyaku_pairing` (first failure; all 10 fixture cases die on `EXC: no such group`) | fails-and-dead |
| M02 | `in_flight` = `launches > completes` instead of last-event | rc 1, pass=11 fail=2 | KILLED | `t_attempt_rollover`, `t_variants` | fails-and-dead, hyaku-pairing, in-flight, legacy-grammar, malformed, state-shapes, two-lanes |
| M03 | `_bad` body deleted (malformed never counted) | rc 1, pass=11 fail=2 | KILLED | `t_malformed_refusal`, `t_other_lines_not_malformed` | attempt-rollover, fails-and-dead, hyaku-pairing, in-flight, legacy-grammar, state-shapes, two-lanes, variants |
| M04 | ts-first non-event lines classified malformed (counters merged) | rc 1, pass=11 fail=2 | KILLED | `t_variants`, `t_other_lines_not_malformed` | attempt-rollover, fails-and-dead, hyaku-pairing, in-flight, legacy-grammar, state-shapes, two-lanes |
| M05 | `MAX_MALFORMED_EXAMPLES` 3 -> 0 | rc 0, pass=13 | SURVIVED | — (none) | attempt-rollover, fails-and-dead, hyaku-pairing, in-flight, legacy-grammar, state-shapes, two-lanes, variants |
| M06 | `close_round` no-op (unclosed pairing never clears) | rc 1, pass=11 fail=2 | KILLED | `t_hyaku_pairing`, `t_attempt_rollover` | fails-and-dead, in-flight, malformed, state-shapes |
| M07 | empty-log UNAVAILABLE branch disabled | rc 1, pass=12 fail=1 | KILLED | `t_empty_log` | all 9 |
| M08 | absent-log rc coerced 2 -> 0 | rc 1, pass=12 fail=1 | KILLED | `t_missing_log` | all 9 |
| M09 | `DEAD_REST_RE` opened to `r".*"` (accept any dead rest) | rc 0, pass=13 | SURVIVED | — (none) | all 9 |
| M10 | `lane-dead-no-report` forgets to clear open launches | rc 1, pass=12 fail=1 | KILLED | `t_attempt_rollover` | fails-and-dead, hyaku-pairing, in-flight, legacy-grammar, malformed, state-shapes, two-lanes, variants |
| M11 | `nlines` never incremented (`lines` always 0) | rc 0, pass=13 | SURVIVED | — (none) | none (all 9 catch it via output diff) |

8 KILLED / 3 SURVIVED. Per the frozen kill rule (`--selftest` rc) the three survivors are
coverage findings on the C1 instrument; none of them is a reason to touch the frozen counter.

## Per-mutant evidence (exact diffs; before-hash = pristine `6b3dba74…` in all cases)

M01 — `LAUNCH_REST_RE = re.compile(\n r"^(?: pgid=…mission=(\S+))?"\n r"| pid=(\d+)| mission=(\S+)| runId=(\S+))?$")` → `LAUNCH_REST_RE = re.compile(r".*")`.
sha256 `0a0b0ca64ab628c14d536ec01ec138a1dd0b0276c05320f62d0770676291316d`.
Selftest stdout (truncated to first failures): `failed=t_hyaku_pairing:EXC:no such group,t_hyaku_pairing,t_attempt_rollover:EXC:no such group,…`.
Kill mode caveat: every launch line now trips `m2.group(4)` on a 1-group pattern (re error
"no such group"), so the kill is an unhandled exception, not an assertion mismatch; 8 of 9
fixture invocations also crash (rc 1, no JSON). Only `fails-and-dead` (no launch lines) is
output-identical. A semantically gentler loosening would NOT be killed by assertion: no frozen
fixture carries a launch line with an unrecognized rest, so `t_malformed_refusal`'s
`malformed >= 3` guard never sees a bad launch rest (the malformed fixture's bad lines are a
non-ts line, a bad-ts complete, a broken complete rest, and two non-ts prose lines).

M02 — `"in_flight": row["last_event"] == "launch",` → `"in_flight": row["launches"] > row["completes"],`.
sha256 `f8d37e8b435f388a156616ee099859ea3348781d49a093143f01da28910a319e`.
Killing cases `t_attempt_rollover` (2 launches, 1 complete, expected `in_flight is False`) and
`t_variants` (kama 1/1 after a post-dead relaunch, expected True). Only 2 of 9 fixtures
(`attempt-rollover`, `variants`) produce differing output.

M03 — `_bad` body (`nonlocal malformed; malformed += 1; if len(examples) < …: examples.append(raw[:120])`) → `pass`.
sha256 `4a303a6d78f992daca8a13dbac0409f9d64cc5258232a4b6e336fa6f00ba5760`.
Killing cases `t_malformed_refusal` (`malformed >= 3` fails: 0), `t_other_lines_not_malformed`
(`malformed == 5` fails: 0). Only the `malformed` fixture output differs; the other 8 fixtures
contain no malformed line, so each alone would let this mutant through.

M04 — `other_lines += 1  # ts-first driver prose (steer, watchdog tick, ...)` → `_bad(raw)`.
sha256 `b22942c3979e9f3157fad44a7f175e28b168dd548b896914b618cc2f4081cf3e`.
Killing cases `t_variants` (`other_lines == 2` fails: 0), `t_other_lines_not_malformed`
(`other_lines == 1` fails: 0; `malformed == 5` fails: 6). Fixtures catching: `malformed`, `variants`.

M05 — `MAX_MALFORMED_EXAMPLES = 3` → `0`.
sha256 `f6e10480cbf317e652a2ae7538e08339bfe81b5ceefa97e8c769109d299564a2`.
Selftest: `DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0`, rc 0 → SURVIVED. The only
examples assertions are `len(...) <= 3`, which an empty list satisfies; no case requires
evidence to be present. The JSON diff does catch it on the `malformed` fixture:
observed output of the mutant over `fixtures/driver/malformed`:
`{"malformed": 5, "examples": []}` (pristine: 3 capped examples). The probe can go silent on
its evidence field while claiming malformed=5.

M06 — `close_round` body (exact-key removal + `(round, None)` fallback) → `pass`.
sha256 `975b94133cf4a942884e72f6f0c733b80b67515d4cd51adc6121431598bdcead`.
Killing cases `t_hyaku_pairing`, `t_attempt_rollover` (`unclosed == 0` fails: 1). Fixtures
catching: attempt-rollover, hyaku-pairing, legacy-grammar, two-lanes, variants; not caught by
fails-and-dead, in-flight, malformed, state-shapes outputs.

M07 — `if text.strip() == "":` → `if False and text.strip() == "":`.
sha256 `4175ecb2b197ff91ffef9024029b7bfe35101c5f5ddd2b83dad49b52b288df99`.
Killing case `t_empty_log` (rc 2 expected, 0 observed). No frozen fixture is an empty log, so
all 9 fixture outputs are identical to pristine — the "unavailable is never zero" guard for the
empty state is held by a synthetic case only.

M08 — absent-log branch `return report, 2` → `return report, 0`.
sha256 `0dbe029435f1d4931c0b78b4ce907b10f60f9aabc1be34aaa6424d4e4e656eed`.
Killing case `t_missing_log` (rc==2 expected). No fixture exercises the absent path (all 9
identical) — synthetic-case-only coverage, as M07.

M09 — `DEAD_REST_RE = re.compile(r"^; retry same round(?: \((.*)\))?$")` → `re.compile(r".*")`.
sha256 `f28915c19858b7e383fee3ffccbfd9cbb0b958b9f9d9f4df63c63dcd2c33686f`.
Selftest `pass=13 fail=0`, rc 0 → SURVIVED, and all 9 fixture outputs identical: every dead
line in the frozen fixtures has a well-formed rest. Demonstration on a synthetic line
(`2026-10-27T10:00:00-03:00 lane-dead-no-report mori round=56; retry later`, run via `--log`):
pristine `{"malformed": 1, "examples_n": 1, "mori_deads": 0}` vs mutant
`{"malformed": 0, "examples_n": 0, "mori_deads": 1}` — the mutant converts a malformed line
into a counted dead event and nothing in the frozen instrument objects.

M10 — `row["open_launches"] = [k for k in row["open_launches"] if k[0] != int(round_s)]` → `pass`.
sha256 `65263a7becb9d5f3a75a94ac2b015c76ecf4ad43b229f53cc1ab73add5c4ed8a`.
Killing case `t_attempt_rollover` (`unclosed == 0` fails: 1 — the dead launch stays open).
Only the `attempt-rollover` fixture output differs; it is the single frozen witness for
dead-clears-open-launches semantics (variants' kama dead has no open launch that round, so it
does not catch it).

M11 — `nlines += 1` → `pass`.
sha256 `313d93f376081a63d5edd6b276f25b33daec9c00d4ead8bc021fa2f3af993805`.
Selftest `pass=13 fail=0`, rc 0 → SURVIVED: no selftest case asserts `log.lines`. All 9 fixture
outputs catch it via the JSON diff; observed over `variants`: `{"lines": 0, "other_lines": 2,
"malformed": 0}` (pristine: lines 12). The headline line-count fact can be wrong by any amount
with the frozen selftest still green.

## Restoration evidence

- Pristine bytes copied to `mutants/pristine_mori-driver-liveness.py` (sha `6b3dba74…`), used as
  the restoration source; run-tree file after the final mutant:
  sha256 `6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997` (matches pristine).
- Post-restoration selftest: `DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0`, rc 0.
- Fleet repo file re-hash after all probes: `6b3dba74…` (unchanged); `git status --porcelain
  tools/mori-driver-liveness.py` empty (rc 0). No git/jj mutating command was run in the fleet
  repo; the only repo write this seat made is this report file.

## Bounds

- Scratch: everything (run tree, 11 mutant copies, results.json `results.json` with full
  selftest outputs, harness `mutate.py`, temp logs) lived under
  `/fast/scratch/hyaku/mori-r56/Mo56MutDriver1/`; `TMPDIR` pointed at its `tmp/`; the directory
  is removed after this report is written (cited outputs are quoted above verbatim).
- No pacman transaction, no tool install, no network fetch, no host writes, no process
  steering; host access was read-only (disk-guard status only).
- No vote items in this wave; this report contains no vote-shaped lines.

## Findings

1. HIGH — `tools/mori-driver-liveness.py` M09 (survivor): opening `DEAD_REST_RE` (line ~59,
   `DEAD_REST_RE = re.compile(r"^; retry same round(?: \((.*)\))?$")`) to accept any rest leaves
   the 13-case selftest green (rc 0) and all 9 frozen fixtures byte-identical; a malformed dead
   rest is silently counted as a dead event (`malformed 1→0, deads 0→1` in the synthetic
   demonstration). No frozen instrument tests the dead-rest grammar's rejection path. Named
   limit of the C1 instrument; candidate routed item for round 57 (a fixture carrying a
   malformed dead rest would close it — data-side, no counter change proposed).
2. HIGH — `tools/mori-driver-liveness.py` M05 (survivor): `MAX_MALFORMED_EXAMPLES = 3` (line ~60)
   can drop to 0 — the evidence `examples` list silently empties — with the selftest still
   `pass=13 fail=0`: every examples assertion is an upper bound (`<= 3`), none requires the
   evidence to exist. The probe's "never silent" property for malformed input is untested on the
   evidence field. Candidate routed item: a selftest assertion `malformed >= 3 →
   len(examples) >= 1` on the malformed fixture (instrument-data, frozen-counter untouched).
3. HIGH — `tools/mori-driver-liveness.py` M11 (survivor): `log.lines` (the `nlines` counter,
   parse_log) is asserted by no selftest case; the total-line-count fact can be stuck at 0 (or
   any wrong value) with the frozen selftest green. All 9 fixtures expose it only via raw output
   diff, which the pinned counter does not perform. Candidate routed item: assert `lines` on one
   fixture (e.g. variants → 12) in the selftest.
4. MED — single-fixture dependence for two killed semantics: the malformed counter (M03) is
   caught only by `fixtures/driver/malformed`, and dead-clears-open-launches (M10) only by
   `fixtures/driver/attempt-rollover`; deletion of either fixture (or a writer-side change those
   two logs don't model) removes the only witness for those behaviors.
5. MED — `in_flight` semantics are witnessed by only 2 of 9 fixtures (M02 was caught by
   `attempt-rollover` and `variants` alone); 7 fixtures' outputs are invariant under swapping
   `in_flight` to a launches-vs-completes arithmetic.
6. LOW — the absent-log and empty-log "unavailable is never zero" guards (M07/M08) are killed,
   but only by synthetic selftest cases; no frozen fixture exercises either path, so the guard
   has no fixture-level witness.
7. LOW — M01's kill is an unhandled `re.error: no such group` (pattern collapsed to 1 group,
   code still calls `m2.group(4)`), i.e. a crash-kill rather than an assertion kill; the
   launch-rest grammar's *rejection* path (`launch <lane> round=<n> <unrecognized rest>` →
   malformed) has no fixture witness, so a well-typed loosening of `LAUNCH_REST_RE` would
   survive. Overlaps finding 1's shape on the launch side.
8. INFO — detector-procedure observation, not a tool defect: the selftest skips fixture cases
   silently when run from outside a repo-like tree (observed `pass=2 fail=0 skipped=11`), which
   would flatter any mutation result; an operator running the tool standalone should place it
   under a tree containing `.ufo/waves/round-56/fixtures/driver/` or treat `skipped>0` as
   inconclusive. Candidate routed item: print skipped fixtures by name (selftest-side notice).
