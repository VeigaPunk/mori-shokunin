# R48MutC1Counter — mutation test of the frozen C1 counter, round 48 wave w2

Seat: `R48MutC1Counter` (leaf; no subagents dispatched). Lane: `mori-shokunin`. Date: 2026-10-25.

**Attacked:** the frozen calibration counter `.ufo/waves/round-48/count-c1.py` (bytes
`7a2a6aa09b923ef8521a1182fb1bc11f4f92ed7450e9eba86882e454284e4b97`) — 8 single-point mutants over
`verdict()`, `run_tool()` status consistency, `MIN_TALLY`, the real arm, and `--selftest`/setup
error handling — with one bounded 4-probe behavioral detector run on pristine, each mutant, and
restored bytes, in scratch only.

**Verdict: HOLDS (instrument), 4/8 killed; 3 survivors + 1 redundancy finding recorded as limits.**
The pristine counter reproduces P-C1 at the landed tip: `C1=met junk_met=0 honest_unmet=0
real=met errors=0 variants=12 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492`, exit 0, and
`--selftest` prints `C1_SELFTEST pass=34 fail=0` exit 0. Killed: M1, M6, M7, M8. Survived: M2
(`honest_unmet` clause), M3 (`errors` clause — logically redundant), M4 (`run_tool` met↔rc
consistency — zero selftest coverage, unobservable at R), M5 (`MIN_TALLY` 26→1 — every run at R
invariant between floors 1 and 26). Survivors are coverage findings about the counter, not
permission to change the contract; the C1 claim itself is untouched by this seat.

## 1. Setup

- Frozen counter never modified; all work on byte-identical scratch copies under
  `.scratch/r48w2-R48MutC1Counter/` (`count-pristine.py`, `mutants/M1..M8.py`, all sha256
  `7a2a6aa0…` before mutation). Every run used `TMPDIR` under the same scratch; every probe A/D
  passed `--scratch` explicitly so the counter's workspace stayed inside my scratch.
- Flag deltas vs the verbatim claim command, and why the detector is equivalent:
  `--repo /home/vgpnk/Projects/shokunin/mori-shokunin` is provably the frozen-path default
  (`dirname⁴` of `.ufo/waves/round-48/count-c1.py` = the lane repo — verified by execution);
  `--scratch` only relocates the counter's `mkdtemp` workspace (same code path); `--jobs 8`
  instead of the default 4 (w1 `ExecC1Replay` §7 observed jobs 4→8 produce identical output; it
  is thread count over the same 13 runs).
- Probe A wall cost: ~3–4 min/arm (13 tool runs each); full 10-arm sweep 2286 s.

## 2. Detector (bounded, identical bytes per arm)

| Probe | Command | Pristine expectation |
|---|---|---|
| A claim | `python3 <counter> --tool tools/mori-pin-check.py --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 --repo <lane> --scratch <scratch>/wt-<arm> --jobs 8` | 12 variant lines + `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=e4dfff3…`, rc 0 |
| B selftest | `python3 <counter> --selftest` | 34×`PASS`, `C1_SELFTEST pass=34 fail=0`, rc 0 |
| C argv | `python3 <counter> --selftest extra` | `C1_SETUP usage: …`, rc 2 |
| D badrev | `python3 <counter> --tool tools/mori-pin-check.py --rev 000…0 --repo <lane> --scratch <scratch>/wt2-<arm>` | `C1_SETUP unresolvable revision 000…0`, rc 2 |

Kill rule: a mutant is KILLED iff any probe's (rc, stdout) differs from the pristine vector;
otherwise SURVIVED. stderr merged into stdout for capture. Full vectors:
`.scratch/r48w2-R48MutC1Counter/detector-results.json` (driver: `run_detector.py`).

## 3. Pristine baseline (observed)

Probe A (rc 0), all 13 lines:

```
variant name=J1 expect=unmet got=unmet rc=1
… J2–J8 identical: expect=unmet got=unmet rc=1
variant name=H1 expect=met got=met rc=0
variant name=H2 expect=met got=met rc=0
variant name=H3 expect=met got=met rc=0
variant name=H4 expect=met got=met rc=0
variant name=real expect=met got=met rc=0
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492
```

Probe B (rc 0): 34 `PASS` lines, `C1_SELFTEST pass=34 fail=0`. Probe C (rc 2): `C1_SETUP usage: …`.
Probe D (rc 2): `C1_SETUP unresolvable revision 0000000000000000000000000000000000000000`.
This also reproduces the C1 claim at the landed tip exactly as P-C1 specifies.

## 4. Mutations and verdicts

| # | Site | Mutation (single point) | Expected detector | Observed | Verdict |
|---|---|---|---|---|---|
| M1 | `verdict()` | `met = junk_met == 0 and …` → `junk_met <= 1 and …` (tolerates one junk green) | B `verdict_one_junk_green` flips | B rc 1: `FAIL verdict_one_junk_green`, `C1_SELFTEST pass=33 fail=1`; A/C/D identical | **KILLED** (B) |
| M2 | `verdict()` | drop `honest_unmet == 0` from `met` | B honest-red arm — none exists | all 4 probes byte-identical to pristine | **SURVIVED** (finding §5.1) |
| M3 | `verdict()` | drop `errors == 0` from `met` | B `verdict_error_not_unmet` | all 4 probes byte-identical | **SURVIVED** (redundant, §5.2) |
| M4 | `run_tool()` | delete `elif (got == "met") != (rc == 0): got = "error"` (status↔exit consistency reclassification) | A: some variant/real inconsistent at R; B: impossible (selftest injects `run=`) | all 4 probes byte-identical; A variant lines all consistent (`unmet`↔rc 1, `met`↔rc 0) | **SURVIVED** (finding §5.3) |
| M5 | constant | `MIN_TALLY = 26` → `MIN_TALLY = 1` | A: any of the 13 runs flips between floors 1 and 26 | A byte-identical: same 13 variant lines and same `C1=met …` line with floor 1; B/C/D identical | **SURVIVED** (finding §5.4) |
| M6 | `verdict()` real arm | drop `real == "met"` from `met` (real still looked up and printed) | B `verdict_real_red` flips | B rc 1: `FAIL verdict_real_red`, `C1_SELFTEST pass=33 fail=1`; A/C/D identical | **KILLED** (B) |
| M7 | `main()` argv | `if argv == ["--selftest"]:` → `if argv[:1] == ["--selftest"]:` | C | C rc 0: mutant runs the full selftest on `--selftest extra` (`C1_SELFTEST pass=34 fail=0`) where pristine prints usage rc 2; A/B/D identical | **KILLED** (C) |
| M8 | `main()` setup error | unresolvable-revision `return 2` → `return 1` (same `C1_SETUP` message) | D | D rc 1 vs pristine rc 2, identical message text; A/B/C identical | **KILLED** (D) |

Mutant bytes (post-mutation sha256, each differing from pristine in exactly the one hunk shown by
`diff -u`): M1 `ec94eef2…`, M2 `bf45a33f…`, M3 `667c8486…`, M4 `e05d5332…`, M5 `62364e1a…`,
M6 `c40ca37b…`, M7 `8a802ece…`, M8 `9800794e…`.

## 5. Survivors — coverage findings, not contract changes

1. **M2 (honest clause unexercised).** No selftest arm constructs "an honest variant red while the
   real registry is green" (`always_unmet_unmet` confounds it with a red real arm; `error_not_unmet`
   with a junk error). At R all four honest variants are met, so the claim arm cannot distinguish
   either. A counter missing `honest_unmet == 0` would print `C1=met` on a tool that fools H1–H4
   while staying green on the real registry — exactly the narrowness the contract warns about —
   and the current arms would not notice. Suggested future arm: fake returning `unmet` for one `H*`
   only (one-line addition to the selftest's control list).
2. **M3 (`errors == 0` is logically redundant).** `error`/`timeout` outcomes are already counted by
   `junk_met` (`g != "unmet"`), `honest_unmet` (`g != "met"`) or the real clause, so the clause
   changes no verdict on any input; `errors=N` in the output line is display-only. Dropping it is
   safe but the clause is dead weight as a guard — fine to keep for readability; it is not an
   independent defense.
3. **M4 (`run_tool` consistency guard has zero test coverage).** `selftest()` injects `run=`, so
   `run_tool` is never executed by `--selftest`; and at R the instrument is status-consistent on
   all 13 runs, so probe A cannot see the guard either. Under M4 a spoofing tool printing
   `PIN_CHECK=met` while exiting 1 would be scored `met` (then flipped by nothing). The guard is
   correct and needed; it is simply untested by every arm this counter runs on itself.
4. **M5 (`--min-tally-pins 26` is behaviorally unpinned at R).** With the floor weakened to 1, all
   13 runs produce byte-identical verdicts: the 26 floor is not what makes any junk variant red at
   this rev (J4's `pass=12` row is rejected for its rebound, not its tally). The P-C1 sentence
   names `--min-tally-pins 26` as part of the predicate, but no variant at R distinguishes floor 26
   from floor 1; a counter (or receipt) asserting the floor is asserted, not demonstrated, at this
   rev. If a future registry row legitimately pins a tally between 1 and 26, this limit closes.

## 6. Restoration evidence

- Frozen counter sha256 before the session and after the sweep, unchanged:
  `7a2a6aa09b923ef8521a1182fb1bc11f4f92ed7450e9eba86882e454284e4b97`
  (`git status --porcelain` on it: clean).
- Mutants and the pristine copy exist only under `.scratch/r48w2-R48MutC1Counter/`; no tracked
  path was edited.
- Restored arm = pristine bytes re-run after all mutants: sha256 `7a2a6aa0…` and all four probes
  byte-identical to the pristine vector (A rc 0 `C1=met …`, B rc 0 `pass=34 fail=0`, C rc 2, D rc 2).

## 7. Tooling

No tools installed or upgraded (none needed); no pacman/uv/npx/cargo actions.

## 8. Notes for the main agent

- The C1 claim at the landed tip reproduced under this seat's pristine run (probe A above, exit 0) —
  consistent with the w1 acceptance direction; the predicate's acceptance run remains the main
  agent's call.
- Cheapest hardening if wanted (counter change ⇒ unfreeze/re-freeze, so record only): add an
  `honest_red` selftest arm (kills M2-class), an error-only arm or a `run=`-level run_tool test
  (kills M4-class), and a `MIN_TALLY` echo or a variant whose verdict depends on the floor (closes
  M5). M3 needs nothing (redundant by construction).
- The survivor analyses rely on the pristine probe A outputs at `e4dfff3…` (13/13 runs status-
  consistent, all verdicts floor-invariant). If the landed tool or registry changes, M4/M5 survivors
  should be re-probed.
