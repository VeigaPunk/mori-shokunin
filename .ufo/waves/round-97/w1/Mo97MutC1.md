# Mo97MutC1 — mutation battery on the frozen C1 counter (round 97, wave w1)

Seat: Mo97MutC1 (mutation-tester, mori r97 w1). Scope: challenge the frozen counter
`.ufo/waves/round-97/count-c1.py` (sha256 `78a09016fa8151b72049400600b6b154437c919df6fccb55b8bfa6253b4d2a95`,
matches contract and `controls-r97.txt` line 1) with single-change mutants run on rebuilt control
fixtures. The frozen file was never edited in place; all mutants are copies under scratch
`$HYAKU_SCRATCH/mori-r97/Mo97MutC1` (disposable, removed at end).

Method: fixtures rebuilt exactly per `.ufo/waves/round-97/controls-r97.sh` (git archive of entering
`973b2af11f41bd362163d7e29ac08286832f546b`, verified by `git rev-parse`; same fixture edits, same
candidate input `candidate/skill-append.md`, sha256 `61b89b8b96da7f6460f0f1539ab06c12fe410dc9d15494fd563a09ba7d06beb3`,
matches receipt). Kill rule (as tasked): a mutant is KILLED on a fixture when any verdict line
(`TARGET*` / `C1=*`, `root=` field masked) differs from the pristine counter's on the same fixture;
exit-code-only differences are reported separately and marked. `root=` is masked because scratch
paths differ from the receipt's.

## 1. Pristine reproduction (required first) — all five receipt verdicts reproduced

Driver: scratch `driver1.sh`; comparison parses `evidence/controls-r97.txt` C1 blocks and diffs
(rc, masked TARGET/C1= lines) against fresh runs. `TMPDIR` set to scratch.

```
PRISTINE_REPRO c1-donothing: MATCH (rc got=1 want=1 lines_match=True)
PRISTINE_REPRO c1-junkrows: MATCH (rc got=1 want=1 lines_match=True)
PRISTINE_REPRO c1-staleline: MATCH (rc got=1 want=1 lines_match=True)
PRISTINE_REPRO c1-notoken: MATCH (rc got=1 want=1 lines_match=True)
PRISTINE_REPRO c1-positive: MATCH (rc got=0 want=0 lines_match=True)
PRISTINE_REPRO_FAILS=0
```

Example reproduced verdict (c1-positive; root masked):
`C1=met unregistered=0 registry=met targets_ok=4/4 checks_failed=- root=<MASKED>` rc=0.
Pristine baselines on the constructed killer fixtures were recorded the same way before mutants ran.

## 2. Mutant table — 12 single-change mutants × 11 fixtures

Fixtures: the five receipt controls (`c1-donothing`, `c1-junkrows`, `c1-staleline`, `c1-notoken`,
`c1-positive`) plus six constructed killers K1–K6 (§3). Each mutant ran on all 11 fixtures
(132 mutant runs + 11 pristine baselines + 1 restored-pristine rerun). A mutant may be killed by
several fixtures; the table lists them all. rc-only kill = verdict lines identical, exit code differs.

| mutant | single change (vs pristine line) | killed-by | survivor |
|---|---|---|---|
| m01 | registry conjunct dropped: `failed = [] if registry == "met" else ["registry"]` → `failed = []` | c1-donothing, K2-duprows, K3-sevencells (checks_failed loses leading `registry`) | — |
| m02 | `REGISTRY=met` scan hardcoded: `registry = "met" if "REGISTRY=met" in out else "unmet"` → `registry = "met"` | c1-donothing, K2-duprows, K3-sevencells (`registry=unmet` → `met`) | — |
| m03 | selftest rc ignored: `good = st.returncode == 0 and stated and verdict` → `good = stated and verdict` | K1-selftestrc (unmet 3/4 rc=1 → false `C1=met` rc=0) | 5 receipt controls (all selftests exit 0 there) — killed by constructed K1 |
| m04 | verdict-token check removed: `verdict = token in row[3]` → `verdict = True` | c1-junkrows, c1-notoken, K5-tokenmoved | — |
| m05 | selftest-line containment dropped (`in`→always True for stated line): `stated = bool(last) and last in row[4]` → `stated = bool(last)` | c1-junkrows, c1-staleline (staleline: 0/4 rc=1 → false `C1=met` 4/4 rc=0) | — |
| m06 | rows_found>1 accepted: `len(cand) != 1` → `len(cand) < 1` | K2-duprows (checks_failed `registry,target_×4` → `registry`) | 5 receipt controls — killed by constructed K2 |
| m07 | 7-cell row accepted: `len(cand[0]) != 8` → `len(cand[0]) < 8` | none — SURVIVED all 11 fixtures (coverage finding, §4) | survivor on every fixture |
| m08 | exit codes swapped: `return 0 if met else 1` → `return 1 if met else 0` | 9 fixtures incl. c1-donothing and c1-positive (rc-only kill; verdict line unchanged) | K4-noskill, K6-noauditor (setup aborts before exit path) |
| m09 | summary label swapped: `"met" if met else "unmet"` → `"unmet" if met else "met"` | 9 fixtures (verdict line label flips on every run that prints one) | K4-noskill, K6-noauditor |
| m10 | TARGETS loses `tools/mori-source-digest.py` | 9 fixtures (c1-donothing: checks_failed loses digest target; c1-positive: `targets_ok=3/4` rc=1 vs `4/4` rc=0) | K4-noskill, K6-noauditor |
| m11 | token scan widened to whole row: `verdict = token in row[3]` → `verdict = token in "\|".join(row)` | K5-tokenmoved (unmet 3/4 rc=1 → false `C1=met` rc=0) | 5 receipt controls + K1–K4, K6 — killed by constructed K5 |
| m12 | missing-file setup guard disabled: `if not os.path.isfile(p):` → `if not p:` | none — SURVIVED all 11 fixtures (coverage finding, §4) | survivor on every fixture |

10/12 killed, 2 survivors. Every killed-by claim above is backed by the run files
`runs/m<NN>-<fixture>.{out,rc}` vs `runs/pristine-<fixture>.{out,rc}` in scratch (compared by
`compare3.py`); example kills shown in §5 output.

## 3. Constructed killer fixtures (scratch, entering rev + candidate rows)

- **K1-selftestrc** — c1-positive plus `sed 's/return 0 if failed == 0 else 1/return 1/'` on the
  fixture's `tools/mori-source-digest.py` (digest selftest now prints the same last line but exits 1).
  Pristine: `C1=unmet ... targets_ok=3/4 checks_failed=target_mori-source-digest.py` rc=1.
- **K2-duprows** — `skill-append.md` appended twice (each registry name occurs twice).
  Pristine: every target `rows_found=2`, `C1=unmet ... registry=unmet targets_ok=0/4` rc=1.
- **K3-sevencells** — candidate digest row reduced to 7 cells (`s/ | mori |$/ |/` on the
  `SOURCES digest check` row only). Pristine: digest `unattributed`, `registry=unmet` rc=1.
- **K4-noskill** — c1-positive minus `SKILL.md`. Pristine: `C1_SETUP missing .../SKILL.md` rc=2.
- **K5-tokenmoved** — digest row's `DIGEST_CHECK` moved from the verdict-map cell into the
  self-test cell (token still in row, not in row[3]; `DIGEST_CHECK rows=N` → `ROWS=N`,
  `DIGEST_SELFTEST pass=11 fail=0` → `DIGEST_CHECK DIGEST_SELFTEST pass=11 fail=0`).
  Pristine: `token_in_verdict_map=no`, `targets_ok=3/4` rc=1.
- **K6-noauditor** — c1-positive minus `tools/mori-gate-registry.py`.
  Pristine: `C1_SETUP missing .../mori-gate-registry.py` rc=2.

## 4. Survivors — coverage findings (no contract change proposed)

- **m07 (7-cell row accepted).** No fixture can kill it: the auditor refuses to attribute any row
  whose cell count ≠ 8 before the counter's own cell-count check runs — `tools/mori-gate-registry.py`
  line 412 `if len(cells) != len(FIELDS): fail(target, "wrong_row", ...)`, and the counter only
  accepts rows from `PASS row=` audit lines. Empirical: on K3 the 7-cell digest row is
  `unattributed` with `registry=unmet`, so pristine and m07 print identical verdicts. The auditor's
  own selftest asserts a seven-cell row is rejected (`mori-gate-registry.py:570-572`). Finding: the
  counter's `len(cand[0]) != 8` is defense-in-depth shadowed by the auditor's `wrong_row` rule; it is
  unreachable as an independent kill switch. It cannot produce a false `C1=met` (an unattributed
  target still fails P1(b)).
- **m12 (missing-file setup guard disabled).** Every reachable difference is confined to the
  `C1_SETUP` message text; verdict and exit code are identical. K4 (SKILL.md missing): pristine
  `C1_SETUP missing .../SKILL.md` vs m12 `C1_SETUP auditor rc=2: REGISTRY_SETUP registry absent at
  WORK: SKILL.md` — the auditor aborts rc=2 first, counter returns 2 either way. K6 (auditor
  missing): pristine `C1_SETUP missing .../mori-gate-registry.py` vs m12 `C1_SETUP auditor rc=2:
  /usr/bin/python3: can't open file '...': [Errno 2] No such file or directory` — the interpreter's
  own rc=2 for a missing script lands in the counter's auditor-rc=2 arm. Both rc=2, no verdict line
  in either. Finding: the counter's file-existence guard is message-only redundancy on all reachable
  inputs.

Neither survivor can flip a `C1=met`/`C1=unmet` verdict or the exit code on any input reachable
through the auditor; both are redundancy findings about the instrument, recorded per the mutation-
tester role as coverage findings, not contract defects.

## 5. Evidence excerpts (from the battery)

Pristine vs mutant verdict lines on the killing fixtures (root masked; full lines in scratch runs,
compared programmatically):

```
m03 K1-selftestrc:  pristine rc=1 C1=unmet unregistered=0 registry=met targets_ok=3/4 checks_failed=target_mori-source-digest.py
                    mutant   rc=0 C1=met unregistered=0 registry=met targets_ok=4/4 checks_failed=-
m05 c1-staleline:   pristine rc=1 C1=unmet unregistered=0 registry=met targets_ok=0/4 checks_failed=target_{cgroup-pressure,drift-recheck,scorecard-calibration,source-digest}.py
                    mutant   rc=0 C1=met unregistered=0 registry=met targets_ok=4/4 checks_failed=-
m06 K2-duprows:     pristine rc=1 ... targets_ok=0/4 checks_failed=registry,target_mori-cgroup-pressure.py,target_mori-drift-recheck.py,target_mori-scorecard-calibration.py,target_mori-source-digest.py
                    mutant   rc=1 ... targets_ok=4/4 checks_failed=registry
m08 c1-donothing:   pristine rc=1, mutant rc=0 (verdict lines identical — rc-only kill)
m10 c1-positive:    pristine rc=0 C1=met unregistered=0 registry=met targets_ok=4/4 checks_failed=-
                    mutant   rc=1 C1=unmet unregistered=0 registry=met targets_ok=3/4 checks_failed=target_mori-source-digest.py
m11 K5-tokenmoved:  pristine rc=1 C1=unmet unregistered=0 registry=met targets_ok=3/4 checks_failed=target_mori-source-digest.py
                    mutant   rc=0 C1=met unregistered=0 registry=met targets_ok=4/4 checks_failed=-
m02 c1-donothing:   pristine rc=1 C1=unmet unregistered=4 registry=unmet targets_ok=0/4 checks_failed=registry,target_...
                    mutant   rc=1 C1=unmet unregistered=4 registry=met targets_ok=0/4 checks_failed=target_...
```

Cited receipt lines (from `evidence/controls-r97.txt`, C1 sections; `CONTROLS_DONE unexpected=0`):

```
## C1 do-nothing (entering tree)
EXPECT rc=1 contains='C1=unmet unregistered=4'   ... OBSERVED rc=1 -> AS_EXPECTED
## C1 forgery: eight-cell junk rows (auditor alone goes green)
EXPECT rc=1 contains='C1=unmet unregistered=0 registry=met targets_ok=0/4'   ... OBSERVED rc=1 -> AS_EXPECTED
## C1 forgery: well-formed rows stating a wrong selftest outcome
EXPECT rc=1 contains='C1=unmet unregistered=0 registry=met targets_ok=0/4'   ... OBSERVED rc=1 -> AS_EXPECTED
## C1 forgery: verdict map without the tool's verdict token (digest row)
EXPECT rc=1 contains='targets_ok=3/4'   ... OBSERVED rc=1 -> AS_EXPECTED
## C1 positive control (candidate rows)
EXPECT rc=0 contains='C1=met unregistered=0 registry=met targets_ok=4/4'   ... OBSERVED rc=0 -> AS_EXPECTED
```

## 6. Integrity / restoration evidence

- Frozen counter sha256 before first run and after all 132 mutant runs + restore rerun:
  `78a09016fa8151b72049400600b6b154437c919df6fccb55b8bfa6253b4d2a95` — unchanged; the file at
  `.ufo/waves/round-97/count-c1.py` was never opened for writing.
- Restored pristine copy (`pristine-restore.py`, `cp` of the frozen file): `cmp` →
  `RESTORED_BYTES_IDENTICAL`; rerun on c1-positive rc=0, output identical to pristine baseline
  (`RESTORE c1-positive rc=0 identical_to_pristine=True`).
- Mutant file sha256s (recorded after runs; scratch disposable, removed with the scratch dir):
  m01 `40af181b…`, m02 `68aa04ea…`, m03 `2db4e000…`, m04 `137cb644…`, m05 `37c7660d…`,
  m06 `6d5fbb74…`, m07 `cb2b7798…`, m08 `eea6fc7a…`, m09 `575a6d5b…`, m10 `a50d47d8…`,
  m11 `bd49c8a3…`, m12 `f20e0e7b…` (all 12 differ from pristine; pre-run copies were
  byte-identical to the frozen counter, verified by a single sorted-unique hash before mutation).

## 7. Unrun checks (named, not fabricated)

- `count-c2.py` not mutation-tested (seat scope is C1).
- The landing revision `e85ed912…` was not measured by this seat; the battery tests the instrument,
  not the landing claim's measurement run.
- The auditor `tools/mori-gate-registry.py` itself was not mutated (treated as ground truth per the
  frozen contract; its 8-cell attribution rule was read, not fuzzed).
- No live-network legs were exercised (C1 has none).
- No tool installs were made (stock python3/git/sed/cmp/sha256sum only).

## VERDICT

VERDICT C1 holds: the frozen counter reproduced all five pre-freeze control verdicts byte-for-byte
(root masked), killed 10/12 single-change mutants — including every mutant that could produce a
false `C1=met` (m03, m04, m05, m06, m11) — and its two survivors (m07, m12) are defense-in-depth
shadowed by the auditor's own wrong_row/attribution and rc=2 arms, unable to flip any verdict on
any reachable input.
