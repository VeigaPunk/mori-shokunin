# MutCounters — round-45 counter mutation testing (wave 1, mori)

Mutation-tester seat. Probed the three round-45 counters (`count-c1.py`,
`count-c2.py`, `count-c3.py`) for single-check granularity: each mutant
disables exactly one check; the detector is the mutant's own `--selftest`
(exit 0 = green, exit 1 = killed, exit 2 = setup). All work was done in
`$TMPDIR` = `.ufo/waves/round-45/tmp/MutCounters` under the lane wave dir;
the lane counters were never edited. Baseline: every counter's own
`--selftest` is green on the measured bytes (C1 16/16, C2 14/14, C3 19/19).

## Measured bytes (snapshot, sha256)

All results below are against these exact lane bytes (quiet ≥180 s before
measurement; verified identical at report time):

| file | sha256 |
|---|---|
| `count-c1.py` | `5f2deea0b35c5e1346229d265aa0c07bf7f365bf6c5acda87648045bce658d23` |
| `count-c2.py` | `153423c48ca90466e85b02707828f5c6b2cf39c87c68ee67e3f9abee956baf93` |
| `count-c3.py` | `37fd7c24ff52d6aa27f718ef0b0a2f2e4affa7a1cd0ab67c1fa05f028854a98e` |
| `tools/mori-gate-registry.py` (v2 auditor) | `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832` |

During the wave the counters were still being edited by their executors
(dozens of byte changes as the fleet landed); every result below was re-run
against the final quiet bytes (snapshot 4).

## Mutation matrix (mine — produced in TMPDIR, one check disabled each)

### C1 (count-c1.py, selftest 16 arms)

| mutant | disabled check | caught by arm | rc |
|---|---|---|---|
| M1-dupid (`if fid in ids:` → `if False:`) | duplicate-id rejection | `duplicate_id_rejected` | 1 |
| M1-witness (`ok = rejected == total` → `ok = True`) | witness rejection | `witness_dir_one_passing_witness` | 1 |
| M1-absent (remove `fails.append("ledger_present")`) | absent-path FAIL | `absent_ledger_unmet` | 1 |
| M1-rowfloor (`record("row_floor", …)` → `True`) | row floor | `below_floor_rejected` | 1 |
| M1-reconcile (`record("commands_reconcile", …)` → `True`) | recompute-exact | `offbyone_row_mismatch` | 1 |
| M1-revsens (`ok = not problems and not constant and not unreadable` → `ok = True`) | revision-constant rows rejected | `revision_constant_row_rejected` (+ `honest_ledger_met`, `witness_dir_one_passing_witness`, `all_const_ledger_unmet`) | 1 |
| M1-revmoves (`record("revision_moves", …)` → `True`) | at least one row must move | `all_const_ledger_unmet` | 1 |
| M1-constcap (`record("const_cap", …)` → `True`) | CONST= cap | `const_heavy_ledger_unmet` (+ `all_const_ledger_unmet`) | 1 |
| M1-classfloor (`record("class_floor", …)` → `True`) | class floor | **SURVIVED** (no arm) | 0 |

### C2 (count-c2.py, selftest 14 arms)

| mutant | disabled check | caught by arm | rc |
|---|---|---|---|
| M2-duplicate (`record("duplicate", …)` → `True`) | duplicate rows finding | `duplicate_row_unmet` | 1 |
| M2-noselftest (`record("no_selftest", …)` → `True`) | comment-only selftest row | `comment_only_selftest_unmet` | 1 |
| M2-mutantkill (`record("mutant_kill", killed, …)` → `True`) | surviving mutant | `surviving_mutant_unmet` | 1 |
| M2-tables (`record("tables", …)` → `True`) | tables floor (TABLE_FLOOR=7) | `tables_floor_unmet` | 1 |
| M2-popmembers (`record("population_members", …)` → `True`) | population partition | `registered_mismatch_unmet` | 1 |
| M2-registered (`record("registered", …)` → `True`) | registered ≥ 1 | **SURVIVED** | 0 |
| M2-wrongrow (`record("wrong_row", …)` → `True`) | wrong-row attribution | **SURVIVED** | 0 |
| M2-auditorselftest (`record("auditor_selftest", …)` → `True`) | auditor selftest green tally | **SURVIVED** | 0 |
| M2-writescopeentries (`record("writescope_entries", …)` → `True`) | ≥1 checkable write-scope entry | **SURVIVED** | 0 |

### C3 (count-c3.py, selftest 19 arms)

| mutant | disabled check | caught by arm | rc |
|---|---|---|---|
| M3-census (`record("census_ok", "census", proc.returncode == 0, …)` → `True`) | red census is unmet | `red_census_unmet`, `red_census_ignores_tmpdir` | 1 |
| M3-token (`if cell in forms:` → `if any(f in cell for f in forms):`) | used-by token-exact match | `usedby_suffix_collision_unmet` | 1 |
| M3-root (`info = {"census_argv": ["bash", census, "validate", "--root", root, LANE]…}` → dropped `--root`) | census `--root` arm | `registered_entry_met` (argv receipt) | 1 |
| M3-absent (`record("entry_present", entry, body is not None, …)` → `True`) | absent entry FAIL | `absent_entry_unmet` | 1 |
| M3-entering (`record("entering_absent", entry, not was_there, …)` → `True`) | entry must be absent at `--entering-rev` | `entering_present_unmet` | 1 |
| M3-entries (`record("entries_declared", … bool(entries), …)` → `True`) | ≥1 `--entry` declared | `empty_entries_unmet` | 1 |
| M3-rows (`record("rows_declared", … bool(rows), …)` → `True`) | ≥1 `--row` declared | `empty_rows_unmet` | 1 |
| M3-readme (`record("readme_row", entry, found, …)` → `True`) | README coverage-map row names entry | **SURVIVED** | 0 |

Notes on multi-arm catches: a disabled check is caught by every arm that
asserts it. Some arms assert indirectly (e.g. M1-revsens breaks
`honest_ledger_met` because the witness set then includes a passing witness).
M3-census is caught twice because two arms exercise a red census.

## Committed mutants (`fixtures/mutants/`) — byte-diff verification

Each committed mutant is a byte-diff of the committed counter disabling exactly
one check, and each is killed by its own selftest with the arm naming the
disabled check:

| committed mutant | diff vs counter | single disabled check | its own `--selftest` | rc |
|---|---|---|---|---|
| `fixtures/mutants/count-c1.py` | 1 hunk / 2 changed lines `if fid in ids:` → `if False:  # MUTANT: duplicate-id check disabled` | duplicate-id rejection | `C1_SELFTEST pass=15 fail=1` fail `duplicate_id_rejected` | 1 |
| `fixtures/mutants/count-c2.py` | 1 hunk / 4 changed lines `record("writescope_mismatch", ws["mismatch"] == 0, …)` → `record("writescope_mismatch", True, …)` | write-scope mismatch check | `C2_SELFTEST pass=13 fail=1` fail `writescope_mismatch_unmet` | 1 |
| `fixtures/mutants/count-c3.py` | 1 hunk / 2 changed lines `record("census_ok", "census", proc.returncode == 0, …)` → `record("census_ok", "census", True, …)` | census-red check | `C3_SELFTEST pass=17 fail=2` fail `red_census_unmet`, `red_census_ignores_tmpdir` | 1 |

During the build wave the committed c1 mutant was transiently stale (a diff
against an earlier counter generation; 239 changed lines — an entire rewrite
reverted); by the quiet final bytes the c1 mutant had been refreshed and is the
single-duplicate-id-check diff above. Only the final state is reported.

## STUB hazard

A tool whose `--selftest` prints a pass line without asserting anything is
not detected by the auditor, and C2's `--audit-all`/mutant arm does not detect
it either — C2 prints `met` with rc 0 while the mutant is a script that merely
claims a failure.

Evidence (all under `$TMPDIR`):

1. **Auditor v2** (`tools/mori-gate-registry.py`, sha256 above) on fixture repo
   `stub/repo` whose `tools/stub-gate.sh` has a real `--selftest` argv branch
   printing `STUB_SELFTEST pass=1 fail=0` (asserts nothing) and an 8-cell row:
   - `--audit-all` → `audit tools/stub-gate.sh PASS row='stub gate' (8 cells, entry resolves, --selftest argv branch)`; `REGISTRY=met`; rc 0.
   - Auditor selftest is green: `GATE_REGISTRY_SELFTEST pass=15 fail=0`, rc 0.
   - Control: comment-only `--selftest` is now caught (v1 false positive closed): `no_selftest=1`, `REGISTRY=unmet`, rc 1.
2. **C2 counter** on fixture repo `stub-c2/repo` with a stub auditor that
   prints conformant v2 counters (`tables=7 registered=1 unregistered=0
   no_selftest=0 duplicate=0 wrong_row=0`, `mode=population`, digest,
   `members=1`) and a "mutant" `fixtures/mutants/count-c2.py` that is a 6-line
   script printing `X_SELFTEST pass=1 fail=1` and exiting 1 — no counter, no
   byte-diff, no assertion:
   - `check mutant_kill PASS (count-c2.py pass=1 fail=1)`; `C2=met`; rc 0.
   - Complementary control: same repo with the "mutant" replaced by a stub that
     prints `pass=2 fail=0` → `check mutant_kill FAIL`, `C2=unmet`, rc 1 (so
     the arm only checks the *mutant's own* claim of failure).

**Finding**: the mutant arm trusts the mutant's output. It never verifies that
the mutant is a byte-diff of the counter, and the auditor never runs the
instrument's selftest to see whether it can detect anything. A registered tool
(or a registered counter's mutant) that prints a green tally without asserting
is therefore indistinguishable from a real one. Kill-rule strength for the
stub/do-nothing class rests on the mutant *failing honestly*, which the current
byte checks cannot force.

## Survivors — coverage findings (not permission to change the contract)

Disabled-check probes whose selftest stayed green (rc 0, pass=N fail=0):

- C1 `class_floor` — no selftest arm exercises the class floor (the below-floor
  arm builds 5 rows but they still span 4+ classes).
- C2 `registered >= 1`, `wrong_row`, `auditor_selftest`, `writescope_entries`
  — no selftest arm perturbs the corresponding stub-auditor counter or the
  write-scope fixture (the `registered_mismatch` arm covers the population
  partition, not `registered>=1`).
- C3 `readme_row` `found` (token-exact map-row match) — both readme arms hit
  the "no map section" branch (`readme_section is None`), so the third branch
  where a section exists but no row names the entry is never exercised
  negatively.

## Method / tooling

Harness `harness.py` in `$TMPDIR`: copies the pristine counter per mutant,
asserts the `old` string occurs exactly once, applies the substitution, records
before/after sha256, runs `python3 <mutant> --selftest` with
`TMPDIR=<per-mutant scratch>`, then restores exact pristine bytes and verifies
the digest (`restored: … equal=True` for every mutant). No tools were installed
or updated; no lane file was edited. Lane VCS was read-only.

Arms and rc are the actual command outputs pasted above; every rc is the
subprocess exit code of the mutant's own `--selftest`.
