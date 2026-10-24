# RevC7Kill — `drift_kill_v2` re-derived end-to-end: four drawn-state mutants

Seat: `mori-r39.RevC7Kill` (reviewer, wave 1). Lane read-only; every build/run under
`.ufo/waves/round-39/scratch/RevC7Kill/`. No installs, no lane mutations.

**Verdict: PASS on the assigned acceptance.** From the pinned bytes at
`13bfba23b7ca063c76d3504a2ff6eb7b6a294932`, the honest probe selftest is 6/6 PASS, and each of the four
drawn states (`fresh`, `excerpt`, `unavailable`, `no-copy`) substituted for `return "drifted"` produces a
`row_states` FAIL whose `got` table differs from `want` in **exactly one row — S103, `drifted` → drawn** —
with the other nine rows byte-for-byte unchanged and the same ten ids. No state flips a non-drifted row and
no state leaves S103 unflipped. The counter's own `drift_kill_v2` condition is true for all four, and the
counter at the scored rev prints `C7=met` exit 0 for a seed drawing each state (seeds 0/1/2/5), including the
claimed `--seed 20261024` (draws `fresh`).

## 0. Bytes and environment

| item | value | source |
|---|---|---|
| revision | `13bfba23b7ca063c76d3504a2ff6eb7b6a294932`, `git cat-file -t` → `commit` | `git cat-file -t`/`git rev-parse` |
| probe blob at R | `tools/mori-source-drift.py`, type `blob`, 466 lines | `git cat-file -t <rev>:tools/mori-source-drift.py` |
| extracted probe sha256 | `453c5d8e260301df7a99daf62b4c16ea08e4a0b4f9e4f53821cdbce447011552` | scratch `mori-source-drift.py` |
| extracted vs worktree | byte-identical (`diff -q` silent, same sha256) | — |
| mutation anchor occurrences | exactly 1 (`grep -c 'return "drifted"'` → `1`), at line 208 | scratch probe `:208` |
| counter bytes | `count-c7.py` sha256 `b92c65f224a6268a901aa6bc5ad66b499048eaca82b493356eb8e1f324ef0520`; `DRAWN_STATES` at `:65` | — |
| python | 3.14.8 | `sys.version` |

## 1. Honest selftest from the pinned bytes (`python3 mori-source-drift.py --selftest`)

Exit **0**; output `out-mori-source-drift.txt:2`:

```
selftest row_states           PASS
```

All six arms PASS: `exit_code`, `row_states`, `summary`, `huge_cap`, `redirect_private_refused`,
`missing_sources_exit2` (parsed from `out-mori-source-drift.txt`). The honest `want` table (embedded in the
probe, scratch probe `:368-374`) is `S101 fresh, S102 excerpt, S103 drifted, S104 unavailable,
S105 unavailable, S106 no-copy, S107 no-copy, S108 fresh, S109 unavailable, S110 unavailable`. The honest
verdict is deterministic: an identical rerun is byte-identical (`out-honest-rerun.txt`, `diff` silent).

## 2. The four mutants

Construction: the single anchor `return "drifted"` (probe `:208`) replaced by `return "<state>"` for each
`state ∈ {no-copy, fresh, excerpt, unavailable}` — the four values of `DRAWN_STATES` (counter `:65`).
Mutant sha256: `no-copy 188fd340…b1e83d`, `fresh e56e2f32…ec5605b5`, `excerpt c25ee332…0468caf0`,
`unavailable 5217f771…01cb0627`. Each selftest exited **1** (the mutant's own arm fails), and the
`row_states` arm read **FAIL** with a structurally parsed table (counter's `parse_got_want`, cross-checked
against an independent `ast.literal_eval` of the same line — identical tables in all four).

| drawn | exit | row_states | rows got/want | ids equal | changed rows (`want`→`got`) | counter `drift_kill_v2` condition |
|---|---|---|---|---|---|---|
| `no-copy` | 1 | FAIL | 10 / 10 | yes | `S103: drifted → no-copy` | **True** |
| `fresh` | 1 | FAIL | 10 / 10 | yes | `S103: drifted → fresh` | **True** |
| `excerpt` | 1 | FAIL | 10 / 10 | yes | `S103: drifted → excerpt` | **True** |
| `unavailable` | 1 | FAIL | 10 / 10 | yes | `S103: drifted → unavailable` | **True** |

Full `got` for `drawn=no-copy` (`out-mutant-no-copy.txt:2`; the other three differ only in the S103 cell):

```
got=[('S101', 'fresh'), ('S102', 'excerpt'), ('S103', 'no-copy'), ('S104', 'unavailable'),
     ('S105', 'unavailable'), ('S106', 'no-copy'), ('S107', 'no-copy'), ('S108', 'fresh'),
     ('S109', 'unavailable'), ('S110', 'unavailable')]
want=[('S101', 'fresh'), ('S102', 'excerpt'), ('S103', 'drifted'), ('S104', 'unavailable'),
      ('S105', 'unavailable'), ('S106', 'no-copy'), ('S107', 'no-copy'), ('S108', 'fresh'),
      ('S109', 'unavailable'), ('S110', 'unavailable')]
```

The other three `got` tables (raw receipts `out-mutant-fresh.txt`, `out-mutant-excerpt.txt`,
`out-mutant-unavailable.txt`) each carry `('S103', '<drawn>')` in that position and are otherwise identical
to the above; the per-state changed-row map is exactly `{'S103': ('drifted', drawn)}` in all four
(`evidence-analysis.txt`). The mutation is deterministic: rerunning `mutant-unavailable.py` produced a
byte-identical FAIL line (`out-mutant-unavailable-rerun.txt`, `diff` silent).

Value collisions do not weaken the check: `no-copy` is also S106/S107's state and `unavailable` is also
S104/S105/S109/S110's, but comparison is per-id on dicts built from the tables, so a flipped S103 is still
isolated.

## 3. Vacuity controls (the acceptance test is not trivially true)

- **Non-drifted flip is rejected.** A control that also swaps the excerpt branch (`S102: excerpt → drifted`,
  everything else honest) fails the counter's condition: `changes={'S102': ('excerpt', 'drifted')}`,
  `counter_ok=False` (`mutant-control-nondrift.py`, `out-mutant-control-nondrift.txt`).
- **An unflipped drifted row is rejected.** A control where classify returns a module constant on the live
  path and leaves `return "drifted"` only as dead code: after the counter's own anchor replacement the run
  still prints `row_states PASS` (exit 0), so `parse_got_want` is never reached and the arm is False
  (`mutant-control-unflipped*.py`, transcript in `evidence-analysis.txt`). The arm requires
  `row_states == FAIL` (`count-c7.py:493-511`).

## 4. End-to-end through the counter at the scored rev

Seed → drawn-state mapping is `random.Random(seed).choice(("excerpt","fresh","unavailable","no-copy"))`
(counter `:65`, `:486-487`): seed 0 → `no-copy`, 1 → `fresh`, 2 → `excerpt`, 5 → `unavailable`, 20261024 →
`fresh`. All executions of
`python3 .ufo/waves/round-39/count-c7.py 13bfba23b7ca063c76d3504a2ff6eb7b6a294932 --seed <S>`:

| seed | drawn | `check drift_kill_v2` | `C7=` | exit | receipt |
|---|---|---|---|---|---|
| 0 | no-copy | PASS | met | 0 | `scratch/RevC7Kill/receipt-seed0.txt` |
| 1 | fresh | PASS | met | 0 | `receipt-seed1.txt` |
| 2 | excerpt | PASS | met | 0 | `receipt-seed2.txt` |
| 5 | unavailable | PASS | met | 0 | `receipt-seed5.txt` |
| 20261024 | fresh | PASS | met | 0 | `receipt-20261024.txt` |

Each run also printed all four negative witnesses `rejected` and `named_row_drift PASS`. The claimed command
in the assignment (`--seed 20261024`) therefore reproduces `C7=met` exit 0 at R, and the drawn-state arm is
exercised against every one of the four drawn values, not just the receipt's one.

## 5. Findings

**F1 — LOW — `--arms selftest` mode can never report pass on an honest probe.**
`count-c7.py:333-341` (`parse_rowstates`) anchors on `^selftest row_states (PASS|FAIL)`, i.e. exactly one
space, but the probe prints the arm name through `"selftest %-20s %s"` (`tools/mori-source-drift.py:441`),
so the line is `selftest row_states           PASS` (10 pad spaces). Observed on the honest extracted bytes:

```
$ python3 .ufo/waves/round-39/count-c7.py 13bfba23… --tool scratch/RevC7Kill/mori-source-drift.py --arms selftest
tool selftest: fail exit=0 row_states=None
C7=unmet
exit=1
```

Also `ROWSTATES_RE` (`count-c7.py:98`) is defined and never referenced — dead code that encodes the same
over-strict spacing. Impact is diagnostics-only: the scored five-check path uses `selftest_arms`
(`count-c7.py:372-383`), whose `^selftest (\S+)\s+(PASS|FAIL)` tolerates the padding, and `drift_kill_v2`
consumes that dict (`:494-496`); no round-39 evidence or claim depends on `--arms selftest` (grep of
round-39 sources/evidence: no invocation). Still, a documented subcommand that misreports a good probe is a
false-negative instrument.

**F2 — LOW (provenance) — the cited C7 receipt names a different revision than the claim.**
`evidence/c7-after.txt:1` is `command: python3 .ufo/waves/round-39/count-c7.py f920eaf7 --seed 20261024`,
while C1 pins `13bfba23`. Not a fabrication: all five counter inputs are the *same blobs* at both revs
(`tools/mori-source-drift.py` `162ee87b5b07`, `corpus/knowledge/source-drift-content-anchor-r38.md`
`06e7ea067f53`, `SCORECARD.md` `f9f34f98729b`, `.ufo/waves/round-37/evidence/drift-live-r37.txt`
`66c17a2fe47e`, `corpus/SOURCES.md` `cd87a9c375ff`; `git diff --stat f920eaf7 13bfba23` touches only
`evidence/` files), and re-running at `13bfba23` reproduces the receipt body exactly — `diff
evidence/c7-after.txt scratch/RevC7Kill/receipt-20261024.txt` shows only the absent `command:` line and the
absent `EXIT=0` line as differences. The stale header is a citation defect, not a result defect.

## 6. Residual risk

- **Probe-authored `want` table.** `drift_kill_v2` takes the reference table from the *mutated* run's own
  printed detail (`count-c7.py:499-510`) and never compares it to the honest run's expected table (the
  honest PASS line carries no table). A probe that derives the printed S103 cell from its own source text
  (e.g. `inspect.getsource(classify)` echoing the return literal) rather than from `classify(body, copy)`
  would satisfy the drawn-state arm without the row state depending on body/copy. I did not build this
  forgery; it is contrived and sits next to the contract's disclosed static-indistinguishability bound, but
  it is the natural next rung (r40) for the r38-M18 descent.
- `kill_rc == 1` is required but not tied to the arm failure: a probe exiting 1 for an unrelated reason while
  printing the required table satisfies that leg. The table condition remains the binding.
- `DRAWN_STATES` excludes `drifted` by construction (correct: the honest literal is the mutated one), so the
  draw space is exactly the four tested values.

## 7. Verification gaps

- **No `lsp` device in this session's tool inventory**, so references/definition/diagnostics could not be run
  server-backed; semantic checks were done by executing the pinned bytes and by importing the counter's own
  parsers (`importlib` on `count-c7.py`) rather than by grep inference.
- The self-source-introspection forgery in §6 is analytic, not run.
- Egress was not blocked during selftest runs; the probe binds loopback only, and no external fetch is used
  by the arm.
- Tool installs/upgrades: none.
