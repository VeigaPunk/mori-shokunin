# MutC8NoneVal — bypass-none vs r39 `timeout_value` (P-C8)

Seat: mutation-tester | Wave: round-39 / w1 | Scored rev: `13bfba23b7ca063c76d3504a2ff6eb7b6a294932`
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only for this seat; no lane bytes edited)
Scratch: `.ufo/waves/round-39/scratch/MutC8NoneVal/` (all artifacts below are there)
Tools installed: none. Interpreter: `/usr/bin/python3` = Python 3.14.8.

## Mutant

r38-M19 bypass A re-derived from the entering tip, never hand-written:

```
python3 .ufo/waves/round-39/fixtures/make-m19-bypass.py \
  13f3db7e5c7163e7ef300259ff597a42a79f81f1 /home/vgpnk/Projects/shokunin/mori-shokunin \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/scratch/MutC8NoneVal
-> derived 2 drain(s) into bypass-none.py; bypass-wait.py from the primary communicate drain   (exit 0)
```

Source bytes `git show 13f3db7e:.ufo/waves/round-38/count-c1.py` → `count-c1-r38.py`
sha256 `5aa51556946a3e5293ba069a12b9e816694ea406bd11f5cb22da5e5ba7c22ea3`.
Mutant `bypass-none.py` sha256 `ae70b4ca74a0d566506cf797a79759cfba4ffa5f947c26f2e0cc0730d627a2b2`.
The only delta is the defect under test (`diff -u count-c1-r38.py bypass-none.py`):

```
+UNBOUNDED_DRAIN_S = None                                  # line 81
-            out, err = proc.communicate(timeout=TOOL_GRACE_S)     # line 124
+            out, err = proc.communicate(timeout=UNBOUNDED_DRAIN_S)
-            out, err = proc.communicate(timeout=TOOL_GRACE_S)     # line 131
+            out, err = proc.communicate(timeout=UNBOUNDED_DRAIN_S)
```

`nl -ba bypass-none.py` confirms lines 81, 124, 131 are exactly the `UNBOUNDED_DRAIN_S` lines.
The defect: both post-SIGTERM drain attempts pass `timeout=None`, so a setsid descendant holding
the pipe can block the counter forever — the keyword name is present, the bound is not.

## Detector (r39 checker, exactly the evidence invocation shape)

```
python3 .ufo/waves/round-39/conform.py 13bfba23b7ca063c76d3504a2ff6eb7b6a294932 \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
  --counter .../scratch/MutC8NoneVal/bypass-none.py
```

Checker under test: `.ufo/waves/round-39/conform.py` sha256
`fe0be179aba9df7150f0b6cdb50a5f9bbdb411efb1263b46ffa6b21d46ef7987` (git blob
`99ab4feffdd14ddde74d2f704fd5445e3f4418be` = `13bfba23:.../conform.py`; verified equal).
Exact transcript: `scratch/MutC8NoneVal/logs/mutant-none.txt` / `.json` (exit=1, 0.3 s):

```
check predicate          FAIL (exit=0 equal=False)
check head_pin           PASS (pin=20260b0c804fa2882d0ed3b916a11d2ab6cc1406 tip=20260b0c804fa2882d0ed3b916a11d2ab6cc1406)
check tool_resolve       PASS (exit=0 resolved=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/fixtures/witness-summary-only-live.txt)
check bounded_reads      PASS (bypass-none.py: bounded=[] value=['line 124 (communicate): non-numeric constant', 'line 131 (communicate): non-numeric constant'])
check timeout_value      FAIL (bypass-none.py: bounded=[] value=['line 124 (communicate): non-numeric constant', 'line 131 (communicate): non-numeric constant'])
check drain_shape        PASS (violations=[])
check timeout_state      FAIL (exit=2 timeout_reason=False pass=False)
check scratch            FAIL (bypass-none.py: mkdtemp_dir=True root=False)
check selftest_conjunct  PASS (honest_comm=[] mutant_comm=['communicate without timeout at line 117'])
CONFORM=unmet
```

**Failing check lines: `predicate`, `timeout_value`, `timeout_state`, `scratch`; exit 1.**
`timeout_value` is the mutation-attributable failure and fails exactly on the two drains that
name `UNBOUNDED_DRAIN_S` (cited lines 124 and 131). The other three failures belong to the
fixture's r38 ancestry and its use as *first* counter (r38 predicate text, r38 CLI lacking
`--arms` → exit 2, r38 `SCRATCH_ROOT`): the same set is reproduced by the r38 source itself in
the ancestry control below, and matches `evidence/c8-after-none.txt` check-for-check.

Note on the acceptance phrase "lines naming UNBOUNDED_DRAIN_S": the checker's message cites
*line numbers* 124/131, whose source text is `proc.communicate(timeout=UNBOUNDED_DRAIN_S)`;
the message *text* says `non-numeric constant`, not the symbol. The literal symbol appears in
the message only in the unbound-name control (`name 'UNBOUNDED_DRAIN_S' has no binding`).
If the acceptance demands the symbol in the message string, that specific wording is unmet;
the check itself is red either way.

## Three-arm run (pristine / mutated / restored) — same detector

| Arm | Bytes | sha256 | `timeout_value` | Full result |
|---|---|---|---|---|
| pristine | `pristine/count-c7.py` (`git show 13bfba23:.../count-c7.py`) | `b92c65f2…ef0520` | **PASS** | `CONFORM=met`, exit 0 (`logs/baseline-c7.txt`) |
| mutated | `bypass-none.py` | `ae70b4ca…27a2b2` | **FAIL** (lines 124, 131) | `CONFORM=unmet`, exit 1 (`logs/mutant-none.txt`) |
| restored | `restored.py` | `5aa51556…c22ea3` | **PASS** | predicates/timeout_state/scratch as r38, exit 1 (`logs/restored.txt`) |

Baseline excerpt (`logs/baseline-c7.txt`, 3.24 s, exit 0): all nine `PASS`, `CONFORM=met`.
Restoration is exact: reversing the two replacements and deleting the inserted line reproduces
the r38 source byte-for-byte (`restored == count-c1-r38.py`, sha256
`5aa51556…c22ea3`); `timeout_value` flips back to PASS.

## Controls (causality and ancestry, all in scratch)

- **Name vs value** — `bypass-none-value5.py` (`UNBOUNDED_DRAIN_S = 5`, same name at both drains, sha256 `690e02d5…`): `timeout_value PASS`. So the FAIL is the `None` value, not the new identifier. `logs/value5.txt`.
- **Unbound name** — `bypass-none-unbound.py` (assignment line removed, sha256 `fa01260f…`): `timeout_value FAIL (line 123/130: "name 'UNBOUNDED_DRAIN_S' has no binding")`. Confirms the resolver path and shows the only message form that spells the symbol. `logs/unbound.txt`.
- **Ancestry** — `count-c7.py` + `count-c1-r38.py` under one checker: `timeout_value PASS`; `scratch FAIL (count-c1-r38.py root=False)`; all other first-counter checks PASS. The `scratch` failure is the r38 scratch-root path, independent of this mutation. `logs/audit-ancestry.txt`.
- **Isolated audit** — `count-c7.py` + `bypass-none.py`: only `timeout_value` and the ancestry `scratch` fail; `bounded_reads` stays PASS because the keyword is present (as designed: presence-only vs value are separate checks). `logs/audit-both.txt`.

## Verdict

**KILLED — PASS against acceptance.** Expected `timeout_value` FAIL on bypass-none; observed
`timeout_value FAIL` citing the two `UNBOUNDED_DRAIN_S` drain lines (124, 131), exit 1; the
pristine arm is green (`CONFORM=met`) under the identical invocation, so the red is attributable
to the mutant. The r39 checker rejects the r38-M19 bypass A fixture, matching
`evidence/c8-after-none.txt` (that receipt was measured at `f920eaf7`; this re-derivation at
`13bfba23` reproduces the same failing set and the same cited line numbers).

## Restoration / write-scope evidence

- No lane file was mutated at any point. Before and after this seat's runs:
  `conform.py` sha256 `fe0be179…ef7987`, `count-c7.py` `b92c65f2…ef0520`, `contract.md`
  `fc36841b…8ebcd3` — unchanged; `git status --porcelain` shows only untracked wave scratch
  (and a sibling's `w1/MutC9IndexOrder.md`), no modified tracked files.
- Mutant/restored/control bytes exist only under `scratch/MutC8NoneVal/`; logs under its `logs/`.
- Environment observation: lane HEAD advanced under me during the window
  (`5561819` → `20260b0c` → `296b2c56`, sibling wave commits). `head_pin` passed in every run
  because counter `--pin-only` and the checker's `git rev-parse HEAD` both read live HEAD; the
  pin is time-sensitive by construction, not pinned to a fixed rev.

## Files cited

- `.ufo/waves/round-39/scratch/MutC8NoneVal/{bypass-none.py,restored.py,count-c1-r38.py,bypass-none-value5.py,bypass-none-unbound.py,pristine/count-c7.py,drive.py}`
- `.ufo/waves/round-39/scratch/MutC8NoneVal/logs/{mutant-none,baseline-c7,restored,value5,unbound,audit-both,audit-ancestry}.{txt,json}`
- `.ufo/waves/round-39/conform.py:150-160` (`_timeout_value`), `:191-221` (value audit), `:355-361` (`timeout_value` result)
- `.ufo/waves/round-39/evidence/c8-after-none.txt` (prior receipt, same failing set)
