# MutC1Walrus2 — walrus-branch mutant re-derivation and kill probe

Role: mutation-tester (leaf, no delegation). Probe only: no contract change, no integration.

## Target / tip

- Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`
- Claimed landed tip: `34b926730c30e0251e1aec531863d8355dc491f1` — **exists as a commit** (`git cat-file -t` = `commit`); lane HEAD is the later `f3ec0977`. Clone was checked out detached at the claimed tip and verified with `git rev-parse HEAD` → `34b926730c30e0251e1aec531863d8355dc491f1`.
- Subject: `.ufo/waves/round-42/conform.py` (v5, 46994 bytes, sha256 `8efa9cfc4d2c36c21bea0cbdcd0a82fa67e15e9bd10c40556710b8f06cf48064`, tip blob `8add90f0c0a34a856890ad9886d19fc2c98c7c50`).
- Frozen transform: `.ufo/waves/round-42/count-c1.py` `TRANSFORMS["walrus-branch"]` (anchor = the 3-line `elif isinstance(sub, ast.NamedExpr):` block in `_assignment_values`, replacement = empty string).

## Mutant construction (independent re-derivation)

Operation: delete exactly the frozen 3-line block (first and only occurrence; `v5.count(anchor) == 1`):

```
        elif isinstance(sub, ast.NamedExpr):
            if isinstance(sub.target, ast.Name) and sub.target.id == name:
                add(sub.target, "value", sub.value)
```

Behavior-bearing point: dropping `NamedExpr` recording means an in-function walrus timeout binding (`(timeout := GIT_TIMEOUT_S)`, fixture `.ufo/waves/round-42/fixtures/counter-walrus-positive.py:110`) is no longer resolved, so `conform.py` must fail closed on the walrus-positive counter.

Byte results (sandbox `/tmp/mut-walrus2`, no lane writes):

| artifact | bytes | sha256 | git blob |
|---|---|---|---|
| pristine v5 (`git show <tip>:...`) | 46994 | `8efa9cfc4d2c36c21bea0cbdcd0a82fa67e15e9bd10c40556710b8f06cf48064` | `8add90f0` |
| derived mutant | 46822 | `1fc61948425c5a64ec6ba259027b845b7cea2715e82dcea6381616c21ff72a8d` | `3d8964002ae0a1203dc237997316a6ec7d82dea7` |
| committed `fixtures/mutants/conform-mut-walrus-branch.py` | 46822 | `1fc61948425c5a64ec6ba259027b845b7cea2715e82dcea6381616c21ff72a8d` | `3d8964002ae0a1203dc237997316a6ec7d82dea7` |

- `derived == committed`: **True** (`cmp` IDENTICAL). The tip's committed blob hash for the fixture is `3d8964002ae0a1203dc237997316a6ec7d82dea7`, i.e. the derived bytes equal the committed fixture at the claimed tip.
- Diff pristine→derived is exactly `-3` lines at 313-318 (NamedExpr branch removed), nothing else.

## Detector (same bounded behavioral detector for all three runs)

```
python3 <clone>/.ufo/waves/round-42/conform.py 34b926730c30e0251e1aec531863d8355dc491f1 \
  --repo <clone> \
  --contract <clone>/.ufo/waves/round-39/contract.md \
  --counter <clone>/.ufo/waves/round-41/fixtures/c1/count-c8.py --selftest
```

Expected on a killed walrus-branch mutant (per count-c1 P-C1 / the v5 arm table): `CONFORM_SELFTEST pass=16 fail=1`, exit 1, the only `FAIL` being exactly `timeout_scope_walrus_positive`.

## Measured outputs

| run | file sha256 in clone | rc | selftest line | FAIL lines |
|---|---|---|---|---|
| pristine (baseline) | `8efa9cfc…cf48064` | 0 | `CONFORM_SELFTEST pass=17 fail=0` | none (17 PASS) |
| derived mutant | `1fc61948…ff72a8d` | 1 | `CONFORM_SELFTEST pass=16 fail=1` | `FAIL timeout_scope_walrus_positive  A walrus binding of a finite-positive timeout must pass -> failing=['timeout_scope']` |
| restored pristine | `8efa9cfc…cf48064` | 0 | `CONFORM_SELFTEST pass=17 fail=0` | none (17 PASS) |

Baseline is green, so the mutant run is conclusive (not a baseline failure). The mutant fails exactly one arm, and that arm is the walrus-positive fixture; `failing=['timeout_scope']` is the checker's inner `timeout_scope` check rejecting the walrus-bound fixture, i.e. the delete branch propagates to precisely the intended observable.

Raw receipts kept in `/tmp/mut-walrus2/{base.out,mut.out,restored.out}` (stderr empty for all three).

## Verdict

**KILLED.** Mutant `conform-mut-walrus-branch.py` (derived or committed — byte-identical) is detected by exactly the expected arm with `pass=16 fail=1`, rc=1, and no collateral arm failure. Expected detector == observed detector.

## Restoration evidence

- Restored bytes were copied from the pristine snapshot (`/tmp/mut-walrus2/pristine.py`, taken from `git show <tip>:.ufo/waves/round-42/conform.py`), verified `cmp` IDENTICAL before restarting the detector.
- Post-restore sha256 in clone: `8efa9cfc4d2c36c21bea0cbdcd0a82fa67e15e9bd10c40556710b8f06cf48064`; unchanged after the restored detector run.
- All writes were confined to `/tmp/mut-walrus2` (one throwaway clone + scratch outputs). Lane `conform.py` and lane `fixtures/mutants/conform-mut-walrus-branch.py` hashes read before/after are unchanged (`8efa9cfc…`, `1fc61948…`). No lane Git index, jj state, `.ufo/state`, `.ufo/watchdog.log`, fleet repo, or sibling repo was written; only this report file was created.

## Tooling

No installs or upgrades were needed: `python3` 3.14.8 and `git` 2.56.0 from the host suffice. Nothing recorded under the install directive.

## Notes (scope-bounded, not a contract judgment)

- The freeze file `.ufo/waves/round-42/evidence/freeze-r42.txt` pins the three **v4** mutants and the three v5 fixture counters but carries no pin for the three **v5** mutant fixtures; count-c1's `v5_mutant_derived_*` check byte-compares against the committed tip blob instead. Recorded as an observation only; the committed fixture matches the frozen transform at this tip.
- Direct deletion of the NamedExpr branch from the v5 bytes reproduces the committed fixture exactly, so the transform is deterministic and anchor-unique at tip `34b9267`.
