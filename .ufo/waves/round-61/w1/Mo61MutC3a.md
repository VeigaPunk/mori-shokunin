# Mo61MutC3a — frozen C3 mutation probe

## Scope and verdict
Axes: detector discrimination, witness independence, restoration fidelity.
Frozen contract read first; freeze revision `7370a731abcafc4c803111de7c22cd6264d63be1`.
**Required probe: 2 killed; 1 survived (ROUTED DEFECT).** No contract/counter amendment proposed or applied.
Pristine is a reference, not a mutant or routed defect.

## Detector and commands
All Python invocations used `TMPDIR` within `/fast/scratch/hyaku/mori-r61/Mo61MutC3a/`, and passed an absolute `--scratch` directory. Each selftest had fresh scratch: reusing its `st-live` makes its commit fail with nothing to commit, which is not a kill.

Command patterns (M is an absolute scratch counter-copy path; D is a fresh absolute scratch directory; L is `/home/vgpnk/Projects/shokunin/mori-shokunin`):

```sh
TMPDIR="$D" python3 "$M" --selftest --scratch "$D"
TMPDIR="$D" python3 "$M" 7370a731abcafc4c803111de7c22cd6264d63be1 --repo "$L" --scratch "$D"
TMPDIR="$D" python3 "$M" 325f7e639916fcbc77fa2ec7475951a1b86bb1cb --repo "$L" --scratch "$D"
```
The selftest cwd was L because the frozen selftest reads its c1/c2/r60 inputs from cwd. Repository access during those runs was read-only. The entering-revision state reproduces committed `evidence/control-c3-do-nothing.txt`; the battery reproduces `evidence/selftest-c3.txt`.
Expected pristine results: selftest `C3_SELFTEST pass=8 fail=0` rc=0; freeze met/all tokens ok rc=0; entering control unmet/livepins FAIL rc=1.

## Required kill table
| Mutant | Exact change | Selftest | Freeze | Entering control | Verdict |
|---|---|---|---|---|---|
| M1 | Replace `c1_ok = all(b.values()); met = c1_ok` with `met = all(b.values())` | 6 pass/2 fail, rc=1 | unmet, r61repair FAIL, rc=1 | unmet, r61repair/livepins FAIL, rc=1 | KILLED |
| M2 | TOKEN_MAP key `r60hole` → `r60hole_x`, fmt unchanged | 6 pass/2 fail, rc=1 | unmet, r61repair FAIL, rc=1 | unmet, r61repair/livepins FAIL, rc=1 | KILLED |
| M3 | Insert `return True, ""` at start of arm_blobrefusal | 8 pass/0 fail, rc=0 | met/all ok, rc=0 | identical to pristine control, rc=1 | **SURVIVED → ROUTED DEFECT** |

M1 is semantically equivalent to the original conjunction but violates the frozen literal `c1_ok` requirement; its kill is textual, not proof of semantic conjunction enforcement. The behavior-bearing variant `met = b["livepins_ok"]` was also killed by selftest (5 pass/3 fail).
M1/M2 failing selftest cases: `all-arms-good` and `r61repair-real-bytes`.

## Finding: blobrefusal arm lacks a negative witness
`count-c3.py:126-139` measures refusal, but `:259` only checks `arm_blobrefusal()[0] == True`. Constant True passes. The source scan at `:119-122` checks assignment syntax, not whether the called arm measures anything. M3 preserved `:183` and passed every committed witness exercised.

A stronger one-point mutant Q1 inserts a child execution in the unpinned refusal branch (`:77-78`) before returning `(None, "unpinned")`, without appending EXEC_LOG. It survives the entire battery and both committed states. Instrumentation wrapping real subprocess.run counted **one actual child execution** while arm_blobrefusal returned `(True, "")` and EXEC_LOG remained empty. This demonstrates the recorded-execution check at `:131` is not independent child-execution observation. No third-party target or arbitrary payload was involved: the frozen harmless blob was `print('hostile')`.

## Supplementary findings (not changes)
- `EXPECT_PIN` at `:46-48` is derived from EXPECTS, not an independent frozen digest. P1 changes every EXPECTS value from `ok` to `FAIL`; its pin moves from prefix `3a62b4f49066` to `f4783928aa7f`; `arm_expectpin()` still returns True and selftest/freeze/control remain pristine. Constant-True expectpin also survives. These are routed witness gaps; no repair was made. P2 using an unrelated literal pin fails, showing comparison can fail when the pin is independent.
- TOKEN_MAP values are unused: `:113-118` checks keys; `:119-122` checks convention-named assignment strings; `:194` prints via `b[t + '_ok']`, not TOKEN_MAP. Renaming a value, or setting `r60hole`'s value to `livepins_ok`, survives. Treat these as dead-metadata/contract-mechanism findings, not evidence that pristine printed tokens are currently wrong.
- Dropping the token-binding loop survives; no committed negative witness exercises that sub-arm.
- Removing the pinned run branch or the EXEC_LOG check survives. These are coverage observations, not standalone proof of an unpinned execution in pristine. The literal fmt-list mutant is behavior-equivalent and excluded from defect counts.

## Clean hostile-state receipt
One shared clone was created at absolute scratch path `.../scratch/hostile2`; all later fixture git calls named that path. Its top-level was checked before mutations. A comment was appended to c1 only and committed there as `a8b4ffa6429eabb42cd4737aa4bc9e6fc9adff59`. c1 hash `62679bbba9512747e9b2e14a66fdab10c48c691a4efc2a5839df46076ccddce5`; c2 and r60 remained pinned. Pristine, M3, and all surviving supplementary mutants yielded unmet/livepins FAIL with r60hole ok, rc=1. This hostile state is seat-generated; it is not a pre-freeze committed witness.

## Actual required-mutant outputs

### M1_drop_c1_ok_from_met
Mutated SHA256: `4f8c55de374d` (prefix; full hashes below).
```text
case all-arms-good: got=False want=True FAIL
case r60-tamper-detected: got=True want=True pass
case self-mutant-detected: got=True want=True pass
case wrong-pins-detected: got=True want=True pass
case blobrefusal: got=True want=True pass
case expectpin: got=True want=True pass
case r60hole-real-bytes: got=True want=True pass
case r61repair-real-bytes: got=False want=True FAIL
C3_SELFTEST pass=6 fail=2
freeze: C3=unmet r60hole=ok r61repair=FAIL blobrefusal=ok expectpin=ok livepins=ok cases=5 failed=self source lost the c1_ok conjunct or TOKEN_MAP rev=7370a731abcafc4c803111de7c22cd6264d63be1
rc=1
control: C3=unmet r60hole=ok r61repair=FAIL blobrefusal=ok expectpin=ok livepins=FAIL cases=5 failed=self source lost the c1_ok conjunct or TOKEN_MAP;r61 counters absent or sha pin mismatch at rev rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb
rc=1
hostile: C3=unmet r60hole=ok r61repair=FAIL blobrefusal=ok expectpin=ok livepins=FAIL cases=5 failed=self source lost the c1_ok conjunct or TOKEN_MAP;r61 counters absent or sha pin mismatch at rev rev=a8b4ffa6429eabb42cd4737aa4bc9e6fc9adff59
rc=1
```

### M2_tokenmap_keys_renamed
Mutated SHA256: `3e177551a060` (prefix; full hashes below).
```text
case all-arms-good: got=False want=True FAIL
case r60-tamper-detected: got=True want=True pass
case self-mutant-detected: got=True want=True pass
case wrong-pins-detected: got=True want=True pass
case blobrefusal: got=True want=True pass
case expectpin: got=True want=True pass
case r60hole-real-bytes: got=True want=True pass
case r61repair-real-bytes: got=False want=True FAIL
C3_SELFTEST pass=6 fail=2
freeze: C3=unmet r60hole=ok r61repair=FAIL blobrefusal=ok expectpin=ok livepins=ok cases=5 failed=self source lost the c1_ok conjunct or TOKEN_MAP rev=7370a731abcafc4c803111de7c22cd6264d63be1
rc=1
control: C3=unmet r60hole=ok r61repair=FAIL blobrefusal=ok expectpin=ok livepins=FAIL cases=5 failed=self source lost the c1_ok conjunct or TOKEN_MAP;r61 counters absent or sha pin mismatch at rev rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb
rc=1
hostile: C3=unmet r60hole=ok r61repair=FAIL blobrefusal=ok expectpin=ok livepins=FAIL cases=5 failed=self source lost the c1_ok conjunct or TOKEN_MAP;r61 counters absent or sha pin mismatch at rev rev=a8b4ffa6429eabb42cd4737aa4bc9e6fc9adff59
rc=1
```

### M3_blobrefusal_constant_true
Mutated SHA256: `95323479aef3` (prefix; full hashes below).
```text
case all-arms-good: got=True want=True pass
case r60-tamper-detected: got=True want=True pass
case self-mutant-detected: got=True want=True pass
case wrong-pins-detected: got=True want=True pass
case blobrefusal: got=True want=True pass
case expectpin: got=True want=True pass
case r60hole-real-bytes: got=True want=True pass
case r61repair-real-bytes: got=True want=True pass
C3_SELFTEST pass=8 fail=0
freeze: C3=met r60hole=ok r61repair=ok blobrefusal=ok expectpin=ok livepins=ok cases=5 failed=none rev=7370a731abcafc4c803111de7c22cd6264d63be1
rc=0
control: C3=unmet r60hole=ok r61repair=ok blobrefusal=ok expectpin=ok livepins=FAIL cases=5 failed=r61 counters absent or sha pin mismatch at rev rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb
rc=1
hostile: C3=unmet r60hole=ok r61repair=ok blobrefusal=ok expectpin=ok livepins=FAIL cases=5 failed=r61 counters absent or sha pin mismatch at rev rev=a8b4ffa6429eabb42cd4737aa4bc9e6fc9adff59
rc=1
```

## Hashes, restoration, and cleanup
Pristine/source SHA256: `6e1fcd3e29b1496bd41a9adab85ce5a980b8c3c05b033f2fc67b5c664f1e6630`.
Required mutated SHA256s:
- M1 `4f8c55de374d19052850505f0bee900eac9997119b08d5e9700607a1f277df07`
- M2 `3e177551a0605bb8a1c5d5880ace31a043235b2b0d4181e58a111342bb803cd5`
- M3 `95323479aef316bf92f0265a2b393f2abf599d0134a00c537e27d7bd482cd469`

Each required mutant copy was restored to the exact pristine bytes and hash above. The same detector was rerun on every restored copy: 8/8 selftest rc=0, freeze met/all ok rc=0, committed control unmet/livepins FAIL rc=1. Production counter bytes were never edited; its final observed hash equals the original. Only this report is retained; seat scratch is removed after receipt capture. Supplementary scratch copies are disposable and removed rather than restored.

## Caveats and discarded harness results
Initial shared-scratch selftests crashed on an existing fixture commit; all such apparent kills were discarded and rerun with isolated scratch. An initial hostile fixture used a no-op first-byte change and omitted other inputs; it was discarded in favor of the clone above. A printed `rows[0]` label misleadingly called M1 pristine; actual pristine JSON rows were checked and passed. The later met/FAIL consistency helper searched the wrong delimiter (` FAIL` rather than `=FAIL`); its negative results are not evidence. These harness defects do not affect the required kill table, based on explicit outputs above.

Disk guard before work: scratch 55% used, 367.0G free (green). No installs or upgrades. No lane/fleet VCS mutations; scratch fixture git only. No remediation or service/config changes.

Self-evaluation: accuracy 4 (discarded harness mistakes explicitly isolated); completeness 4 (required pristine/mutated/restored probes complete; supplemental equivalents separated); clarity 4 (required table precedes extras); actionability 4 (exact edits/outputs/source lines retained); conciseness 3 (supplementary probes exceeded the assigned three). Overall 3.8/5. Improvement applied: label only M3 as the required routed defect; do not count pristine or equivalent mutants as defects.
