# FinalR02 — static falsification of R02 (retained red reconciles at exit 0, no clearance)

Seat: MoriR22.FinalR02 (critic, leaf). Static analysis only. No tests, builds, oracle, selftest or tool runs were executed by this seat. Retained measurement evidence was read as observation. No tool installed or updated.

## Inputs (current shipping source, verified by digest)

| File | SHA-256 |
|---|---|
| `tools/mori-retention-reconcile.py` | `d6870fb6db7c7d0886f1823b42399821f4f54a4ff0290ee1b43adf9400ac0ce7` (equals `measure1/summary.json` `tool_sha256`; git blob `f163c87b…` equals HEAD) |
| `.ufo/waves/round-22/oracle-reconcile-v2.py` | `dcd1c7c656ea8b2e266f88762bf5540e42e41c78078a4b8b11f41e23670d8adb` (equals `requirements-v2.json` pin) |
| `.ufo/waves/round-22/frozen/fixture-builder-v2.py` | `1b3e16f74a032e066dd881c15affbc4401f2f44447d78efc650ee98a6d2d15d1` (equals pin) |

I read `denominator-correction.md` first. Under it, policy-excluded means the identities matched by `non_author_paths_glob`. I cross-checked the semantics against `tools/mori-retention-gate.py` lines 88-307 (`_blob_hits` and `_scan_result`).

## Verdict

R02 **HOLDS** at branch level for the current shipping source, on the frozen `valid` fixture and on the real input. However, the frozen R02 arm **does not discriminate** two of its sub-claims: that the red state is derived, and that the receipt's verdict fields are reconciled. The same-command red control is missing. This means R02 is admitted evidence for the counts and `privacy_clearance=false`, but not for verdict-field reconciliation.

## Branch-level reason R02 holds (valid fixture)

The fixture has 5 raw hits: `policy.json`×1, `allowed.txt`×2, `unallowed.txt`×1, `non-author.txt`×1. The `binary.bin` file is skipped because it contains a NUL byte. The allowlist has 2 rows (`policy.json` and `allowed.txt`); the two identical `allowed.txt` lines deduplicate to one row.

1. Setup (lines 155-194) passes:
   - `measured` is a full OID, and `--is-ancestor` succeeds.
   - The policy and allowlist bytes are equal at both revisions.
   - `exit_code=1` is in (0,1), and `stderr` is empty.
   - The `--repo` value is absolute. The `--policy` and `--allowlist` values are absolute under the repo and strip to the same relative paths.
   - The `--rev` value equals `measured`, `commit` equals `measured`, and `policy_sha256` matches.
   - No population keys are present.
2. `scan` (lines 138-152) reproduces the gate's `split('\n')`, `errors=replace` and `sha256(line.encode())`. The result is 5 hits.
3. The allowlist loop (lines 198-202) puts both rows in `allowed_keys`. `forbidden` and `stale` are both empty.
4. The partition (lines 203-208) gives:
   - `excluded`: 1 hit (by glob)
   - `scanner`: 4 hits
   - `allowed`: 3 hits (the policy hit and both `allowed.txt` hits)
   - `unallowed`: 1 hit (`scanner` minus `allowed`)
   - `routed`: 0
5. Line 209 gives `retention_code=1`, which yields `retention_state='red'` at line 224. Line 210 gives `RETENTION_FINDINGS`.
6. Lines 211-218 leave `differences` empty. Every comparison agrees:
   - hit counts 5/3/1, metric 1, routed 0, non_author 1
   - `finding_id` agrees
   - forbidden and warnings are both `Counter()`
   - exit code 1 == 1
7. Line 219 returns exit 0 with `RETENTION_RECONCILED`. Line 225 sets the literal `privacy_clearance: False`, which is also present on every JSON path (lines 225, 261, 273, 275).

The retained observations agree:
- `measure1/after-observed.json` R02 `pass: true`, with run `valid`: exit 0, `differences: []`, `raw_unallowlisted=1`, `scanner_unallowlisted=1`, `red`, and `privacy_clearance=false`.
- `measure1/real-reconciliation.json`: exit 0, 95/5/90, unallowlisted 4/4, non_author 5, allowlisted 86, `red`, `privacy_clearance=false`.

## Counterexamples and gaps

### C1. Missing same-command red control: a verdict-only lie is unexercised

- **Smallest counterexample:** take the frozen `valid` fixture and the identical R02 argv. Change only the wrapper `exit_code` from 1 to 0, so the receipt claims the gate exited green on a red tree.
  - Shipping source correctly flags this: line 218 appends `exit_code`, so the result is exit 1 with `RETENTION_RECONCILIATION_MISMATCH`.
- **The gap:** I enumerated every arm statically. None changes `exit_code` alone, or `finding_id` alone, while leaving the hit lists and metric intact.
  - **Frozen 24:** the fixture wrapper's `exit_code` is always 1. Every expected-1 variant also changes `hits` or `metric`. The `bool-*` variants fail type checks at line 168 or 187.
  - **`--selftest` (4 arms):** `wrong.json` changes `hits` only.
  - **Refinements (25 arms):**
    - `forged-clean` changes 5 fields: `differences=[hits, unallowlisted_hits, metric, finding_id, exit_code]`.
    - `clean-control` is self-consistent.
    - `boolean-exit` is a type setup (line 168), not the line 218 comparison.
- **Surviving mutants** (this is an inference from static enumeration; I did not execute them):

| Mutant | Frozen 24 | Selftest | Refinements |
|---|---|---|---|
| Ignore exit: delete line 218 | survives | survives | survives |
| Ignore finding: drop `('finding_id', retention_finding)` from line 215 | survives | survives | survives |
| Constant red: hard-code `retention_code=1`, or `retention_state='red'` | survives (R02 and R11 both expect red; no frozen arm expects clean) | — | killed only by the co-evolved `clean-control` |

  Under the ignore-exit mutant, the one-field lie above reconciles at exit 0. That is a false "receipt matches" on a red tree.
- **Missing control:** R02's own arm is positive-only. It shares the cached `valid` invocation with R01, R03, R04, R12, R22, R23 and R24, and has no paired arm with identical argv where only the verdict fields lie and exit 1 is expected.
- **Smallest safe correction:** keep the frozen artifacts byte-unchanged. Append a co-evolved control set, labelled post-implementation and not frozen-requirement evidence. On the `valid` fixture with identical argv:
  1. Wrapper `exit_code` 0 only: expect exit 1, `MISMATCH`, `differences == ['exit_code']`.
  2. Inner `finding_id` `RETENTION_CLEAN` only: expect `differences == ['finding_id']`.
  3. Both changes: expect `differences == ['finding_id', 'exit_code']`.

  Each arm must also assert `retention_state == 'red'`, `raw_unallowlisted == scanner_unallowlisted == 1`, and `privacy_clearance is False`. Add the ignore-exit, ignore-finding and constant-red mutants to `measure-round22.py`. They must be killed by this set, not only by `clean-control`.

### C2. `raw_unallowlisted` duplicates `scanner_unallowlisted` (tradeoff, not a frozen-expectation failure)

- **Evidence:** line 222 sets both `raw_unallowlisted` and `scanner_unallowlisted` to `len(unallowed)`. Line 207 computes `unallowed` from `scanner`.
- **Counterexample by name:** in the R02 fixture, the `non-author.txt` raw hit is unallowlisted. The raw-population unallowlisted count would therefore be 2, but the tool reports `raw_unallowlisted=1`.
- **Why this is not a failure:** the frozen expectations pin 1/1 (fixture) and 4/4 (`expected-real.json`). The value is correct under v2, which partitions raw as allowlisted + unallowlisted + non-author.
- **Consequence:** R02's "raw/scanner_unallowlisted > 0" conjunct is one observation reported twice. No input can make the two fields diverge, so their agreement is not two-population evidence. This is the same mistake as lesson M1, where scalar agreement was taken to establish population agreement.
- **The judge's call:** reject any claim that R02 independently confirms the raw and scanner unallowlisted denominators.
- **Smallest safe correction:** keep the values. State in the lesson or report that `raw_unallowlisted` is defined as author-scope unallowlisted, which is identical by construction to `scanner_unallowlisted`. Alternatively, emit a single field. Do not redefine the value against the frozen expectations.

### C3. Exit 0 is not unique to reconciliation (fixable defect next to R02)

- **Counterexample:** append `-h` to the R02 command. `Parser` overrides only `error()`, and argparse's `add_help` is True by default; the subparser inherits `parser_class=Parser` (argparse.py:1956). The help action raises `SystemExit(0)`, which `main` does not catch (it catches `Invalid` plus six exception types).
- **Result:** exit 0, which is `RETENTION_RECONCILED`'s code. stdout is help text, with no JSON, no `privacy_clearance` field and no reconciliation. A consumer that checks only the exit code reads this as "reconciled".
- **Smallest fix:** pass `add_help=False` to both `Parser(...)` and `sub.add_parser('check', ...)`.

### C4. A regex with a huge repeat count crashes with exit 1 (fixable defect next to R02)

- **Counterexample:** a policy class regex `a{4294967295}`. In Python 3.14 (`re/_parser.py:670-675`), `re.compile` raises `OverflowError` when the repeat count is ≥ MAXREPEAT.
  - `policy_rules` catches only `re.error` (line 97), and `main` does not catch `OverflowError`.
  - The result is a traceback on stderr and exit 1, which collides with the `MISMATCH` code. It should be exit 2 `SETUP`. This violates the contract's "invalid regex cannot crash".
- **Smallest fix:** change line 97 to `except (re.error, OverflowError)`.

### C5. Oracle result depends on an absolute `--output` (false red, not false green)

- `oracle-reconcile-v2.py` derives the fixture root from `--output`. A relative `--output` puts a relative `--repo` into the receipt `argv`. Line 176 then fails with `receipt_repo_binding` (exit 2), which turns R01, R02 and the other `valid` arms red.
- `measure-round22.py` passes absolute paths, so the retained results are unaffected. Record the absolute-path precondition with the oracle evidence.

## Impacted axes

- **Calibration:** R02's admitted evidence overstates what it discriminates (C1, C2).
- **Depth:** the verdict-field reconciliation has no control (C1).
- **Operability:** exit codes collide (C3, C4).
- **Unaffected:** coverage, freshness and adjacency.

None of these findings grants privacy clearance, settles historical dispositions or clears the RED11/12 original permission control.
