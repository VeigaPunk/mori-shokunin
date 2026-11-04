# Mo89E01ArmsC1 — round-88 `count-c1.py` three attributed arms (C2 calibration)

Seat: Mo89E01ArmsC1 (executor, leaf). L1: MoriR89. Scope: implement only the r88 `count-c1.py`
subject in scratch; no production edit; no commit.

## Entering subject (exported, not edited in place)

- Source: `git show 760428abf925d98025b34bf23f2cbf54cbeb3bca:.ufo/waves/round-88/count-c1.py`
- Export: `/fast/scratch/hyaku/mori-r89/Mo89E01ArmsC1-count-c1.py` (removed at seat close)
- sha256 `3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2`
- Entering own selftest: 25 arms (`EXPECTED_ARMS = 25`).

## Candidate (delivered)

- Path: `.ufo/waves/round-89/w1/candidates/r88-count-c1.py`
- sha256 `d5b83c775d199c66ae7c1a1310c054d2d39b5e5a4ba102ccc4b69f0859fd6037`
- Diff vs entering export: `.ufo/waves/round-89/w1/Mo89E01ArmsC1-candidate.diff`
  (sha256 `8f0e6f138aadef18fc22e4da8c5e876575bb982d0d39be634b80a236d236f688`)

Changes, exactly as scoped:

1. `own_ok_of(rc, out)` extracted as a pure module-level helper. It has the same predicate as
   the previous inline `own_ok` in `main`: `rc == 0`, `"C1_COUNTER_SELFTEST"` in output, and
   `pass=EXPECTED_ARMS fail=0` matched. `main` now calls `own_ok = own_ok_of(...)`.
2. `EXPECTED_ARMS` 25 → 28.
3. Three arms added before `own_arms_pinned` (so `len(cases)+1` evaluates to 28 at that arm):
   - `arms_last_tally`: `arms_of` on two tallies returns the last one `(2, 0)`.
   - `green_mixed_fail`: `green(0, "fail=0")` true; `green(0, "fail=0 … fail=2")` refused.
   - `own_ok_red`: `own_ok_of` refuses rc≠0 with a green tally, and refuses a `fail=1` tally.
4. `ARMS_BY_FILE = {"count-c1.py": 24}`, `TARGET_ARMS = 24`, `TARGET = (6, 0, 6)` and
   `SUBJECTS` are unchanged (they refer to the r87 subject).
5. Docstring: one paragraph added describing the three arms; the rest is the original text.
   The `want_met` / `FX … refused` legibility items are in the r88 `count-c2.py` subject, not
   this one, so none apply here.

## Commands and receipts (all run in `/fast/scratch/hyaku/mori-r89/Mo89E01ArmsC1/`)

| step | command | rc | result |
|---|---|---|---|
| export verify | `git show 760428abf…:.ufo/waves/round-88/count-c1.py \| sha256sum` | 0 | `3ba0f97b…` (matches) |
| candidate selftest | `TMPDIR=<seat>/scratch-run python3 -I work.py --selftest --scratch <seat>/scratch-run` | 0 | `C1_COUNTER_SELFTEST pass=28 fail=0` |
| frozen mutants | `python3 -I mutate.py` (loads the three C1 pairs from frozen `round-89/count-c2.py` MUTANTS, sha `40eacccc…`) | 0 | see below |

Frozen mutant pairs, each applied to an isolated copy, each run through its own `--selftest`:

| label | declared arm | anchor occurrences | mutated rc | attributed FAIL line | tally |
|---|---|---|---|---|---|
| C1-arms-first | arms_last_tally | 1 | 1 | `FAIL arms_last_tally last of two tallies` | `pass=27 fail=1` |
| C1-green-drop-fail | green_mixed_fail | 1 | 1 | `FAIL green_mixed_fail mixed tallies refused` | `pass=27 fail=1` |
| C1-own-ok | own_ok_red | 1 | 1 | `FAIL own_ok_red own_ok_of()` | `pass=27 fail=1` |

All three are killed under the frozen kill rule: red run, and a `FAIL <declared arm>` line
present. Transcripts saved at `.ufo/waves/round-89/w1/Mo89E01ArmsC1-selftest-transcript.txt`
and `.ufo/waves/round-89/w1/Mo89E01ArmsC1-mutants-transcript.txt`; digests and
receipts at `.ufo/waves/round-89/w1/Mo89E01ArmsC1-receipts.txt`.

## Not run / limits (named, not papered over)

- The candidate's `main` path (grading the r87 subject at a revision) was **not run**. The
  `own_ok_of` refactor is covered by the `own_ok_red` arm and by the selftest; the main wiring
  itself was not exercised end-to-end.
- The frozen `count-c2.py` (r89) was **not** run against this candidate. The C2 claim is not
  measured by this seat; L1 integrates the nine + three arms and runs the counter.
- The `own_ok_red` arm's `not own_ok_of(0, "... fail=1")` clause is redundant for killing the
  frozen mutant (the mutant is killed by the `rc=1` clause alone). It is kept because it pins
  the predicate against the tally's green form, not because it adds a kill.
- No commit, no push, no production or corpus edit. No tool installed or upgraded.

## Status

Candidate complete, selftest 28/0, all three frozen mutants killed with attribution.
Scratch removed at close (export and work copy deleted after receipts were saved).

Report: .ufo/waves/round-89/w1/Mo89E01ArmsC1.md
