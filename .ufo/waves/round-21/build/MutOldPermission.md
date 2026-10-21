# MutOldPermission — proposed bounded C2 mutation/control

## Status and axes

**Proposal only; target and probe have NOT been executed. No killed/survived verdict has been measured.** This follows the assignment's explicit no-target-execution boundary. No production or frozen input was mutated, so runtime restoration evidence is not yet applicable.

- **Calibration (C2):** challenge whether the evaluator actually reads `evidence_loss_blocks` and detects exactly two wrongly permitted lost-evidence cases.
- **Freshness (C1 boundary):** preserve the distinction between an unknown disposition and independent disposition. This probe neither settles historical losses nor authorizes a pin.
- **Control fidelity:** same evaluator bytes, same rule pathname, same cases, and same bounded detector before mutation, after mutation, and after exact restoration.

## Candidate artifact and exact mutation

Standalone stdlib Python proposal:

`.ufo/waves/round-21/build/MutOldPermission/probe_old_permission.py`

Artifact SHA-256 observed with `sha256sum`:

`38be675d536f43f14145524e16e434b78cf6ce926b0517fa46153c70d757a1f1`

The future run copies the supplied evaluator into a fresh `probe-*` directory under this seat. It constructs isolated rule/case files and changes **only one boolean token in isolated `rule.json`**:

```diff
-  "evidence_loss_blocks": true,
+  "evidence_loss_blocks": false,
```

The rule schema and `source` metadata remain unchanged. The script checks that removing this field makes the pristine and mutant rule objects equal. It does **not** replace the whole object with `frozen/before-rule.json`, which would also change provenance metadata.

Basis: `.ufo/waves/round-21/contract.md:15,20-25`; `frozen/after-rule.json:2-4`. `frozen/before-rule.json:3-5` explicitly models QUALITY67's historical cause-only permission; it is not evidence that historical QUALITY67 had executable code.

## Frozen expectation and exact expected mismatch2

The expectation table is embedded independently from the target implementation, using `contract.md:20-25` and `frozen/cases.json:4-51`.

| Frozen case | Pristine/restored observed pair expected | Mutant observed pair expected | Mutant mismatch? |
|---|---|---|---|
| `loss-unknown` | `census-regression`, `false` | `live-state`, `true` | Yes |
| `loss-cleanup-only` | `census-regression`, `false` | `live-state`, `true` | Yes |
| `loss-independent-cleanup` | `live-state`, `true` | unchanged | No |
| `loss-independent-settlement` | `live-state`, `true` | unchanged | No |
| `ordinary-aging` | `live-state`, `true` | unchanged | No |
| `ordinary-state` | `live-state`, `true` | unchanged | No |

Thus the primary frozen detector must observe **`mismatched: 0 → 2 → 0`, rc `0 → 1 → 0`**. The mutant has two mismatched **cases**, not four mismatched fields. The first two differ in `ordinary_state_change`, so neither its true nor its false value can excuse missing required evidence without independent disposition. The final four cases are negative controls.

These are expected outputs, not actual execution results.

## Same bounded detector and diagnostic control

For each phase, the proposal runs the same copied classifier twice, using identical pathnames and arguments in every phase:

```text
<same Python> -I -B <seat-run>/evaluator.py classify --rule <seat-run>/rule.json --cases <seat-run>/frozen-cases.json
<same Python> -I -B <seat-run>/evaluator.py classify --rule <seat-run>/rule.json --cases <seat-run>/permission-witness.json
```

The second file is a **diagnostic witness, not a replacement policy expectation table**. It preserves all six input flag triples and changes only the first two expected pairs to `live-state,true`. This makes all six witness expectations permissive. Matching the entire witness after mutation confirms the precise mutant decision vector, rather than accepting any arbitrary two mismatches. It also avoids guessing undocumented per-case output field names; the script consumes the documented integer `mismatched` and return code, and retains the complete output.

| Phase | Frozen detector `(rc, mismatched)` | Witness detector `(rc, mismatched)` |
|---|---|---|
| Pristine flag `true` | `(0, 0)` | `(1, 2)` |
| Mutant flag `false` | `(1, 2)` | `(0, 0)` |
| Restored flag `true` | `(0, 0)` | `(1, 2)` |

This is at most **six classifier launches**, each with six cases and a fixed 10-second timeout. No `audit`, `--selftest`, census, pin, build, lint, formatter, network action, Git write, or other runtime is invoked by the proposal. No phase flag is passed to the target; only the isolated rule bytes change between phases.

Verdict handling in the proposal:

- `killed` / probe rc0 only when both pristine/restored controls match, inputs remain intact, exact restoration succeeds, and the mutant has the exact two-case-flip signature above.
- `survived` / probe rc1 when pristine/restored controls pass but mutation leaves the decision vector unchanged. This is a coverage finding, not a contract change.
- `inconclusive` / probe rc2 on setup failure, timeout, malformed output, inconsistent rc/count, failed baseline/restored control, failed restoration, or an unexpected mutant response that does not establish the specified flip. A failed baseline is never called a kill.

## Proposed later L1 invocation — not run here

```sh
TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch python3 \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-21/build/MutOldPermission/probe_old_permission.py \
  --evaluator /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-evidence-loss.py
```

L1 may supply a different completed evaluator source via `--evaluator`; it is read and copied, never edited. During this seat's inspection, `glob` reported the default `tools/mori-evidence-loss.py` path missing. That observation does not establish its later state. No execution was attempted.

The script generates only seat-local `probe-*` files. Each phase preserves verbatim `.stdout` and `.stderr`, actual return codes, parsed JSON, and before/after SHA-256s for evaluator, rule, frozen cases, and witness. `result.json` records the verdict, expected versus observed signatures, copied evaluator identity, and restoration evidence. Generated embedded fixture bytes must match the recorded frozen rule/case SHA-256s before execution; that guard has not been exercised here.

## Observed evidence and restoration boundary

The only executed binary command was `sha256sum`, first for source fingerprints and then for the candidate script. Actual source fingerprint output:

```text
c49e66c2db9572225a0355ac8ab73f3feacd1f78b5fc157210d5d516c9b3ec6f  .ufo/waves/round-21/contract.md
8bf6cd9f20fb1fefc25e7b3381deda0220dbe8fd5012b4a6baa9b37f0646bc95  .ufo/waves/round-21/frozen/after-rule.json
e616b229d97cd2e7068aadeb053f622d2af6e72bd31b1eb1e86c98d78f0fa39a  .ufo/waves/round-21/frozen/before-rule.json
10603c9e2a506f0aab9e03036e76b9149621a875e762616acbbbfa9a52e66878  .ufo/waves/round-21/frozen/cases.json
```

Paths above are shortened relative to the lane root; the hashing command used their absolute lane paths and `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch`.

**Actual detector output: none. Actual mutated/restored hashes: not measured, because no mutation was applied.** The future probe uses nested `finally` blocks to restore the original rule bytes before the restored detector and again afterward, even on detector failure. Its final record requires exact byte equality and the pristine SHA-256; mutated phase hashes are also retained. These are proposed safeguards, not claimed successful restoration observations.

Writes for this assignment are limited to this report and the named candidate script. No tools were installed or updated. No broad tests, syntax checks, smoke runs, target execution, census, or pin were run.
