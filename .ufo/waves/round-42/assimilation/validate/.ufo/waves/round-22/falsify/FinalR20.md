# FinalR20 — static falsification of R20 ("unsafe input path returns2")

Seat MoriR22.FinalR20, critic, static analysis only. I did not execute the shipping tool, the oracle, the fixture builder, the refinement runner, the selftest, or any test, build, or mutant. I read source files, ran `sha256sum`, used read-only `git -C <lane> log/status/show --stat/rev-parse`, and parsed already-recorded `evidence/measure1/*.json` with a read-only JSON reader. No tools were installed. Claims I did not observe are marked [INFERENCE]. Prior build notes (`build/AttackR20.md`) were re-verified against current shipping source, not trusted.

## Verdict

- **Behavioral R20 holds for the delivered tool.** Recorded evidence bound to tool SHA256 `d6870fb6…0ce7` shows exit 2, `RETENTION_RECONCILIATION_SETUP`, `error=unsafe_input_path`, and the five-key setup shape.
- **The frozen R20 arm does not check the branch-level reason.** `oracle-reconcile-v2.py:57` asserts only the exit code, `finding_id`, parseable JSON, and empty stderr. Any setup failure satisfies it, so the frozen R20 pass is not evidence that the path guard exists.
- **The reason is asserted only in the non-frozen refinement runner.** It is not part of the 24 frozen requirements. It covers the dotdot class only.
- **The same-command red control is missing.** No path-guard mutant was ever run against the R20 command, or against the refinement `unsafe-*` commands. So the discriminating arm has never been observed going red.

## Inputs and bindings verified

| Artifact | SHA256 (observed) | Bound by |
|---|---|---|
| `contract.md` | `1658c390…21a1` | requirements-v2 `contract_sha256` ✓ |
| `denominator-correction.md` | `968945b2…24f9` | `correction_sha256` ✓ |
| `frozen/fixture-builder-v2.py` | `1b3e16f7…15d1` | `fixture_builder_sha256` ✓ |
| `oracle-reconcile-v2.py` | `dcd1c7c6…8adb` | `oracle_sha256` ✓ |
| `tools/mori-retention-reconcile.py` | `d6870fb6…0ce7` | after/restored/refinement observations ✓ |
| `refinement-reconcile.py` | `06e104a3…0d97` | refinement-observed `runner_sha256` ✓ |

The shipping tool is committed and clean. Its last change is commit 3985b3d. The denominator correction concerns the meaning of "policy-excluded"; it does not change R20.

## Branch trace in the shipping source

In `check()`, the order is: line 155 `resolve(repo,a.rev)`, then line 156 `safe_path` on `--receipt`, `--policy`, and `--allowlist`, then line 157 `committed()`. An unsafe path therefore never reaches `ls-tree` or `cat-file`.

`safe_path` (lines 49–51) is one combined `require(...,'unsafe_input_path')`. It requires a non-empty string, rejects a leading `/`, rejects any component in `{'', '.', '..'}`, and rejects characters with `ord<32` or `==127`.

`committed()` (lines 81–86) separately requires that `ls-tree` returns exactly one row whose name equals the requested path byte-for-byte, under `GIT_LITERAL_PATHSPECS=1` and after `--`.

Frozen arm trace: the `valid-unsafe` fixture with a valid `--rev` resolves. Then `safe_path('../receipt.json')` hits the `..` component and raises `unsafe_input_path`, giving exit 2, SETUP, empty stderr, and keys `{schema,finding_id,error,privacy_clearance,receipt_match}`. The recorded `after-observed.json` and `restored-observed.json` show exactly this.

## Smallest counterexample: the frozen R20 arm cannot kill the guard

**Mutant M1** deletes the single token `'..',` from the component tuple in `safe_path`.

- **Frozen R20 under M1.** `'../receipt.json'` now passes `safe_path`. Then `ls-tree … -- ../receipt.json` either fails because the path is outside the repository (`git_read_failed`) or returns zero rows (`missing_input_blob`) [INFERENCE: git pathspec handling]. Both outcomes give exit 2, SETUP, and empty stderr, so **R20 stays green.**
- **The other 23 frozen arms under M1** pass only the literal safe names `receipt.json`, `policy.json`, and `allowlist.json`. The receipt-recorded absolute paths are stripped to the same safe names. So M1 is predicted to pass **24/24** frozen requirements [INFERENCE: static; not executed].
- **Same result for M0** (`safe_path` returns `path` unchanged).
- **Same result for a worktree reader.** `../receipt.json` resolves to `<oracle-out>-fixtures/receipt.json`, which does not exist, so an `OSError` maps to `input_unavailable`, which is still exit 2.
- **The selftest has the same blind spot.** Its arm 3 (`../allow.json`) also checks only exit and `finding_id`.

Recorded corroboration: all four executed mutants (count-only, false-clearance, wrong-population, setup-leak) pass frozen R20. The setup-leak mutant adds a `detail` key to the setup payload, and frozen R20 still passed it, because the arm does not check the key set.

**What would kill M1:** the refinement arms `unsafe-receipt`, `unsafe-policy`, and `unsafe-allowlist` (path prefixed with `sub/../`) assert `error=='unsafe_input_path'` and the exact five-key set. Under M1, `sub/../receipt.json` passes `safe_path`. `ls-tree` then either normalizes it to `receipt.json`, which fails the exact-name check (`missing_input_blob`), or finds no rows. Either way the arm goes **red** [INFERENCE: static]. These arms are the only reason-level evidence for R20. They are bound to the current tool and observed green 27/27, but they sit outside the frozen 24-requirement denominator.

## Missing same-command red control

`measure-round22.py:77-82` defines four mutants and none touches `safe_path`. The refinement runner runs only against the delivered tool (`measure-round22.py:74`), never against mutants. So:

- **Required red control:** run the same `unsafe-*` refinement commands, and the frozen R20 command, against M1. The `unsafe-*` arms must fail. The frozen R20 arm is predicted to *pass* under M1; that is the non-discrimination this report claims, and executing it would confirm it.
- **Missing paired green control for the frozen arm:** the frozen oracle never runs the `valid-unsafe` fixture with the safe token `receipt.json`. R01 uses a different fixture directory, and the receipt argv binds a different repo path, so the commits differ. A broken `valid-unsafe` fixture would still turn R20 green. Only the selftest pairs `base` (exit 0) with `base[:-1]+['../allow.json']` (exit 2) on the same repo, and that pair is not reason-checked and not run against mutants.

## Class coverage versus the contract

The contract lists four unsafe classes: absolute, dotdot, empty, and control characters.

| Class | Frozen arm | Refinement arm | Selftest | Consequence of dropping the clause |
|---|---|---|---|---|
| dotdot | `../` receipt, reason not checked | `sub/../` ×3, reason checked | `../` allowlist, reason not checked | Reason only (the exact-name check still fails closed) |
| absolute | none | none | none | Reason only [INFERENCE] |
| empty / empty component | none | none | none | Reason only [INFERENCE] |
| controls (C0, DEL) | none | none | none | **Behavioral**: git tree names can contain C0 controls, so a committed `a<TAB>b.json` would be read and reconciled (exit 0/1 instead of 2) |

Second counterexample (behavioral, no arm anywhere): **M2** drops `ord(c)<32 or ord(c)==127`. Commit a valid allowlist named with an embedded TAB and pass `--allowlist` with that name. Shipping tool: exit 2, `unsafe_input_path`. M2: reconciles normally [INFERENCE]. No frozen, refinement, or selftest arm would catch it. C1 controls (0x80–0x9f) are accepted by both the shipping tool and M2. The contract does not say whether C1 counts as "controls"; that is a definitional tradeoff, not a defect.

Minor points:

- The `safe_path(recorded)` call at line 182, which checks paths recorded in the receipt argv, only affects the reason code. The equality with an already-safe `paths[key]` already rejects any unsafe recorded value, so no arm is needed for safety.
- `unsafe_input_path` is emitted by both line 156 and line 182, so the code alone does not identify the branch. In the refinement arms, line 156 fires first by ordering, so the attribution there is unambiguous.

## Impacted axes

- **Calibration (C1):** the frozen count of 24/24 includes an R20 pass that a guard-less tool would also earn, which is scalar agreement standing in for branch evidence (the same pattern as lesson M1).
- **Correctness:** the control-character class has no observable coverage.
- **Provenance:** the reason-level evidence lives outside the frozen denominator and has no red control.

The delivered tool itself shows no R20 defect. This is a gap in the measurement, not in production code.

## Smallest safe correction (measurement only; no production edit)

1. Add one mutant to `measure-round22.py`: replace `('','..','.')` with `('','.')`, and run **both** the frozen oracle and `refinement-reconcile.py` against it. The kill basis must be the refinement `unsafe-*` arms going red. Record that frozen R20 stays green under M1 as an explicit non-discrimination finding, rather than counting R20 as a discriminating requirement.
2. In the refinement runner, add a same-fixture paired green control for each `unsafe-*` case: the same argv with the original safe token, expecting exit 0. Add one committed TAB-named input arm expecting `unsafe_input_path`.
3. Do not rewrite the frozen oracle; record the R20 reason gap against it as debt. No change to `safe_path` is required for the dotdot or C0 classes.
