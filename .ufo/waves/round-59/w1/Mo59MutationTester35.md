# Mo59MutationTester35 — settlement scanner silent-pass mutation test (round 59, w1)

Seat: mutation-tester (leaf, no dispatch). Target: `tools/mori-settlement-scan.py`
(frozen C2 scanner, PIN `4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9`).
Claimed invariant under challenge: strict field typing per the tool's own docstring —
`seats` int == len(results); `round` int ≥ 1; `output` str | null; verdict
SETTLEMENT_SCAN_OK only when every file validates. Plausible defect probed: fields that
silently pass (`output` non-str truthy, `seats` bool True, `round` float 59.0).

Read-only on the lane; all probes ran on byte-identical scratch copies under
`/fast/scratch/hyaku/mori-r59/Mo59MutationTester35/` (cleaned before yield; receipts inline).
No VCS mutation: the frozen counter materializes the scanner via `git show <rev>`
(`count-c2.py:196`), so working-tree probes cannot touch scored bytes.

## Method (bounded)

- Pristine check: `sha256sum` of lane tool and scratch copy — both
  `4c04bf21…ac9a9` (byte-identical to the frozen PIN).
- Detector: 7 single-field fixtures (1-member valid base; one field varied each),
  run as `python3 <scanner> <fixture>`; expectations from the tool's docstring contract.
  Fixtures: `valid`; F1 `output=123`; F2 `seats=true` (1 member); F3 `round=59.0`;
  F4 `round=true`; F5 `seats=false, results=[]`; F6 `seats=1.0`.
  Plus `<scanner> --selftest --scratch` under the seat TMPDIR.
- Two mutants, one behavior-bearing point each, on a scratch copy, restored between runs.

## Probe verdicts — pristine pinned bytes

Baseline: selftest `SETSCAN_SELFTEST pass=10 fail=0`; `valid` → rc=0 SETTLEMENT_SCAN_OK.

| probe | field varied | verdict | reason |
|---|---|---|---|
| F1 | `output=123` (non-str truthy) | FAIL rc=1 | `member[0]:output_bad` — **caught, no counterexample** |
| F2 | `seats=true`, 1 member | **OK rc=0** | **SILENT PASS** — `isinstance(True, int)` is True; `True == 1` |
| F3 | `round=59.0` | FAIL rc=1 | `round_bad` — **caught, no counterexample** |
| F4 | `round=true` | **OK rc=0** | **SILENT PASS** — bool passes `isinstance(…, int)` and `True ≥ 1` |
| F5 | `seats=false`, `results=[]` | **OK rc=0** | **SILENT PASS** — `False == 0` |
| F6 | `seats=1.0` | FAIL rc=1 | `seats_mismatch` — float seats rejected (contrast: bool seats pass) |

Raw driver output (pristine):

```
valid                        rc=0 SETTLEMENT_SCAN_OK
F1_output_int                rc=1 SETTLEMENT_SCAN_FAIL member[0]:output_bad
F2_seats_bool_true           rc=0 SETTLEMENT_SCAN_OK
F3_round_float               rc=1 SETTLEMENT_SCAN_FAIL round_bad
F4_round_bool_true           rc=0 SETTLEMENT_SCAN_OK
F5_seats_bool_false_empty    rc=0 SETTLEMENT_SCAN_OK
F6_seats_float               rc=1 SETTLEMENT_SCAN_FAIL seats_mismatch
```

**Counterexample (no mutation needed): bool-typed `seats` and `round` silently pass at the
pinned sha.** The docstring contract says `seats`/`round` are ints; JSON `true`/`false`
round-trip to Python `bool`, a subclass of `int` (evidence: `python3 -c` →
`1==True: True; 0==False: True; json true -> bool`). The three named axes resolve as:
`output` non-str truthy — rejected; `round` float 59.0 — rejected; `seats` bool True —
**silently passes** (plus same-family `round` bool and `seats` bool/empty).

## Mutation probes (scratch copies; lane untouched)

**M1 — seats axis.** Smallest point: `scan_file` seats check,
`isinstance(seats, int)` → `isinstance(seats, (int, float))` (copy line 62).
Mutant sha256 `7d9a1a743570d312a9fd63e32cd7f4acafd8d54aaefd83df2600aebbf95e80c3`.
Expected detector: F6 flips FAIL→OK. Observed: exactly that; F2–F5 unchanged;
selftest **still `pass=10 fail=0`** (its `seats_mismatch` case uses int 5 vs 2 members —
no bool/float cases exist, selftest source lines 164-166).
Counter arms (`count-c2.py`): `tool_sha` (196-203) — mutant bytes ≠ PIN → **killed**;
selftest arm (213-217, `EXPECT_SELFTEST` at 214) — green, not killed; scan arm (242-246) —
real files all int seats, green; drift arm (258-263) — r53 extra-keys still FAIL, green.
**Verdict M1: killed by frozen byte-PIN only; survived every behavioral arm** → coverage
gap: a float-typed-`seats` regression would pass selftest + scan + drift undetected.

**M2 — round axis.** Smallest point: round check type clause dropped,
`not isinstance(d.get("round"), int) or …` → `d.get("round") is None or …` (copy line 67).
Mutant sha256 `3f49dc6b7e86b5586cc8755b6a4553d13a6605777982008e258ffefe89d7c659`.
Expected: F3 flips FAIL→OK. Observed: exactly that; selftest **still `pass=10 fail=0`**
(no round-type case). Same counter-arm analysis.
**Verdict M2: killed by frozen byte-PIN only; survived every behavioral arm.**

## Restoration evidence

- Between mutants: `cp scanner-pristine.py scanner-mutant.py` then `sha256sum` →
  `4c04bf21…ac9a9` before each edit.
- After probes: mutant copies deleted; lane file re-hashed post-run →
  `4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9` (unchanged, matches PIN).
- No other lane writes; scratch removed before yield.

## Findings

1. **Adversarial finding (defect live at pinned bytes):** the scanner silently accepts
   bool-typed `seats` (`true`/`false`) and bool `round`, violating its own strict-int
   contract. Trigger requires `len(results)` to equal 1 for `seats:true` or 0 for
   `seats:false`, so the numeric `seats == members` identity is preserved — but the type
   contract is not enforced. Downstream, even the counter's scan-arm check
   `f.get("members") == f.get("seats")` (`count-c2.py:243`) evaluates `1 == True → True`,
   so a real artifact carrying `"seats": true` would pass C2's scan arm end-to-end.
2. **No counterexample** for the other two named axes: `output` non-str truthy →
   `output_bad`; `round` float 59.0 → `round_bad`. The scanner is strict there.
3. **Coverage finding (mutant survived behavioral arms; killed only by the byte PIN):**
   the scanner selftest (10 cases) has zero bool/float type-confusion cases; the C2
   counter's behavioral arms (selftest string, real-scan OK, drift FAIL) cannot
   distinguish type-validation mutants. The frozen PIN (`count-c2.py:196-203`) is the
   sole kill — it freezes bytes, not behavior. Per role: this is a coverage finding,
   not a contract change; no production edits proposed or made.
