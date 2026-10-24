# AttackR24 — R24 "full provenance bindings retained": the frozen arm checks echoes, not bindings

Seat: MoriR22.AttackR24 (critic, read-only, static). Scope is R24 only. Sources read: `contract.md`, `denominator-correction.md`, `frozen/requirements-v2.json`, `frozen/expected-real.json`, `frozen/fixture-builder-v2.py` (sha256 `1b3e16f7…`), `oracle-reconcile-v2.py` (`dcd1c7c6…`), `refinement-reconcile.py` (HEAD 3985b3d), `measure-round22.py`, the candidate `tools/mori-retention-reconcile.py` at 3985b3d (sha256 `d6870fb6…`, which equals the worktree), `tools/mori-retention-gate.py`, and the two r21 receipts (shape and revision fields only). No tests, builds, oracle runs, or mutants were executed. Every "survives" or "kills" below is a static trace marked [INFERENCE]. Nothing was installed, and no matched text appears here.

## Verdict

The candidate implements most of the R24 bindings, at `check()` lines 155–228. However, the frozen R24 predicate (`oracle-reconcile-v2.py:61`), the refinement controls, and the real-run check (`measure-round22.py:81`) leave six of them unverified. A SUT that echoes its inputs instead of binding them still scores 24/24, refinements 19/19, and `real_matches_frozen_expected=true`. The R24 pass is therefore superficial until the arms in §4 exist.

## 1. Axes

- **Provenance:** every emitted identity is derived from the bytes or objects actually read, never copied from an argument or the receipt.
- **Identity:** a revision means a full commit OID, not a tag OID, abbreviation, or symbolic name.
- **Fail-closed:** a binding conflict returns exit 2 with a sanitized code.
- **No leakage:** exit 2 never echoes argv bytes.
- **Discrimination:** every binding line is killed by at least one retained arm.

## 2. What the R24 predicate actually checks (`oracle-reconcile-v2.py:61`, valid arm only)

| Field | Oracle expectation | Why it does not prove a binding |
|---|---|---|
| `input_revision` | `== f['rev']` | `f['rev']` is already a full OID from `rev-parse HEAD`. Echoing `a.rev` passes, so "resolved once" is never exercised. |
| `measured_revision` | `== f['measured_revision']` | Copied from the wrapper. The valid fixture has wrapper revision = argv `--rev` = stdout `commit`, so ignoring the latter two passes. |
| `tool_sha256` | equals the tool's bytes | This does discriminate. |
| `inputs_sha256` | equals fixture digests | `expected_*_sha256` is computed from worktree bytes that equal the committed blobs, so a worktree reader passes. The contract's "via Git blobs, not worktree" is untested. |
| `argv` | `isinstance(list)` | `[]` passes. |
| (exit 1 outputs) | not checked | A mismatch output with no provenance passes R05–R10. |

## 3. Binding lines in the candidate, and whether anything kills their removal [INFERENCE, static]

Each anchor string occurs exactly once in the 3985b3d bytes (verified with `str.count`).

| # | Mutant (replace anchor) | v2 oracle | refinements | measure real/entering | Survives? |
|---|---|---|---|---|---|
| M1 | `'input_revision':revision` → `'input_revision':a.rev` | pass (full-OID `--rev`) | not checked | `realmatch` does not compare `input_revision` | **yes** |
| M2 | `raw={k:committed(repo,revision,p) for k,p in paths.items()}` → `raw={k:(repo/p).read_bytes() for k,p in paths.items()}` | pass: worktree = committed. R21 still exits 2 via `invalid_json` because the oracle does not check `error`, and R20 is caught earlier by `safe_path`. | pass | pass (real worktree blobs unchanged) | **yes** |
| M3 | `'argv':sys.argv[1:]` → `'argv':[]` | pass | n/a | not compared | **yes** |
| M4 | `require(receipt.get('policy_sha256')==digest(raw['policy']),'receipt_policy_digest')` → `require(True,'receipt_policy_digest')` | no arm mutates `policy_sha256` | none | pass | **yes** |
| M5 | `require(receipt.get('commit')==measured,'receipt_revision_conflict')` → `require(True,'receipt_revision_conflict')` | R13 changes both fields together, and the argv check or the git read still fails | `wrong-command-revision` is caught by the argv line | the entering receipt is caught by the argv line | **yes** |
| M6 | `resolve(repo,measured)==measured` → `True` (regex only) | R13 `'0'*40` still exits 2 via `git_read_failed`, because the oracle does not check `error` | none | pass | **yes** |
| M7 | `for key in ('policy','allowlist'):` (argv path loop) → `for key in ('allowlist',):` | none | only `allowlist-path-substitution` | pass | **yes** (policy path unbound) |

`measure-round22.py:54-58` mutates only count-only, false-clearance, and wrong-population, and it judges mutants by the v2 oracle alone (`killed=rc==1 and unmet>0`). Refinements are never run against mutants.

## 4. Concrete counterexample fixtures

Each fixture starts from `FIX.make(root,'valid')`, then is post-edited the way `refinement-reconcile.py` does it. The base invocation is `check --repo R --rev REV --receipt receipt.json --policy policy.json --allowlist allowlist.json`. Unless stated, the expected counters are the valid ones: `raw_total=5, policy_excluded=1, scanner_total=4, raw_unallowlisted=1, retention_state=red, privacy_clearance=false`.

**F24-A, symbolic input revision (kills M1).** Use the valid fixture unchanged and invoke with `--rev HEAD`, then again with `--rev <first 12 hex of REV>`. Expect exit 0, `RETENTION_RECONCILED`, `receipt_match=true`, `input_revision == REV` (the full 40-hex OID, which differs from the literal argument), and `argv[argv.index('--rev')+1]` equal to the literal argument. This freezes reading (i): `--rev` may be any selector, and the output records its single resolution. If L1 prefers reading (ii), full-OID-only, the expectation becomes exit 2 `invalid_revision`. Either way the arm must exist.

**F24-B, worktree divergence (kills M2).** After the fixture's final commit, and without committing anything further, overwrite three worktree files:
- `receipt.json`: a valid wrapper whose stdout drops the `unallowed.txt` hit (the refinement `forged-clean` edit).
- `policy.json`: the committed bytes plus `b' '`.
- `allowlist.json`: `{"rows":[]}`.

Expect exit 0 `RETENTION_RECONCILED` with the valid counters, and `inputs_sha256 == {k: sha256(git cat-file blob REV:<path>)}`. Those are the fixture's pre-divergence `expected_*_sha256` values. A worktree reader returns exit 2 `policy_changed`, or exit 1, or wrong digests.

**F24-C, inner commit split (kills M5).** Add `clean.txt` with content `b"clean\n"` in a commit `C2` on top of REV. `C2` has the same hit multiset as the measured `C1`, because `receipt.json` and `clean.txt` contain no hits. Set wrapper `measured_revision=C2` and argv `--rev=C2`, but leave stdout `commit=C1`. Commit the receipt as REV2 and invoke with `--rev REV2`. Expect exit 2 `RETENTION_RECONCILIATION_SETUP`, `error=receipt_revision_conflict`. A SUT that ignores stdout `commit` returns exit 0 with 5/1/4, which is false provenance hit agreement cannot reveal. Also change refinement `wrong-command-revision` to set argv `--rev` to the real ancestor `C1` instead of `'0'*40`, so the equality check, not resolvability, is what is tested.

**F24-D, annotated-tag OID (kills M6).** Run `git tag -a -m t t1 C1` and take `tag_oid` from `rev-parse t1`, a 40-hex tag object. Set wrapper `measured_revision`, argv `--rev`, and stdout `commit` all to `tag_oid`, then commit. Expect exit 2 `error=receipt_revision`. With a regex-only check, the tag peels through `merge-base`, `ls-tree`, and the scan, giving exit 0 with `measured_revision` naming a non-commit object. Also add the 40-hex uppercase form of `C1`, which needs the same exit 2.

**F24-E, policy digest lie (kills M4).** Use the valid fixture with stdout `policy_sha256 = sha256(policy_bytes + b"\n")`. Expect exit 2 `error=receipt_policy_digest`. The receipt then attests a different policy than the bytes reconciled against. This is an input binding, so freeze it as exit 2 and not exit 1.

**F24-F, policy path substitution (kills M7).** Commit `copy-policy.json` byte-identical to `policy.json` and invoke with `--policy copy-policy.json`. Expect exit 2 `error=receipt_path_binding`. This mirrors the existing `allowlist-path-substitution` control.

**F24-G, provenance on exit 1.** On the R05 `drop` arm, require the full R24 predicate below plus `receipt_match is False` and `'hits' in differences`. Exit-1 evidence is the claim most likely to be cited, and today nothing checks that it carries provenance.

**F24-H, exit 2 minimality (protects R20 and R23 from an R24 "fix").** On every exit-2 arm (R13–R21 and F24-C/D/E/F), require that the stdout key set is a subset of `{schema, finding_id, error, privacy_clearance, receipt_match}`. On R20, also require that the literal `../receipt.json` does not appear in stdout. Adding `argv` to setup errors would emit attacker-chosen path bytes.

## 5. Exact actionable R24 criterion

The R24 predicate on the valid arm (applied the same way to F24-A and F24-G) must be:

```text
v['input_revision'] == git rev-parse --verify REV^{commit}
  and the value is a full lowercase OID; for F24-A the argument differs from the value
v['measured_revision'] == wrapper.measured_revision == stdout.commit == argv[--rev],
  each one equal to its own ^{commit} resolution
v['tool_sha256'] == sha256(tool bytes); at measurement, == sha256(git show <measure-rev>:tools/mori-retention-reconcile.py)
v['inputs_sha256'] == {k: sha256(git cat-file blob REV:path_k)}   (blob bytes, proven by F24-B)
v['argv'] == cmd[2:]   (exact: 'check' and everything after it)
```

Every exit-2 binding conflict asserts both `finding_id` and the exact `error` code: `receipt_revision_conflict`, `receipt_revision`, `receipt_policy_digest`, or `receipt_path_binding`.

Retained controls must kill M1–M7. The smallest change that does not touch the pinned v2 oracle:
1. Add F24-A through F24-H to `refinement-reconcile.py`, which is already labeled co-evolved and is not pinned.
2. In `measure-round22.py`, run the refinements against every mutant, append M1–M7 to `mutations`, and set `killed = oracle_unmet>0 or refinements_failed>0`, recording which suite killed each mutant.
3. Extend `realmatch` at line 81 with:
   - `real['input_revision']==expected['input_revision']`
   - `real['measured_revision']==expected['measured_revision']`
   - `real['tool_sha256']==sha(code_cp.stdout)`
   - `real['argv']==realcmd[2:]`

The alternative is a co-evolved v3 oracle with no new IDs, using the R18 conjunctive precedent at `oracle-reconcile-v2.py:56`. That is L1's choice.

## 6. Semantic ambiguities L1 must freeze, with the reading recommended for each

1. **"appear in receipt" (`contract.md:10`) refers to the reconciler's output, not the r21 wrapper.** The wrapper carries no tool or allowlist digest and no separate resolved input revision (also noted in EnteringPartition and ReceiptBinding). Requiring them there would make every real r21 receipt exit 2, and R02 and the real run would be unsatisfiable.
2. **"executing tool SHA256" is the reconciler's own bytes.** The gate path in receipt `argv[1]` is not digested by the receipt, so any gate-blob digest the tool reports is unattested metadata, never "executed". The candidate's `receipt_authenticity:'unattested'` is the right shape.
3. **"Loaded input SHA256" means the Git blob bytes at the resolved input revision.** For policy and allowlist these are proven equal at the measured revision by R15/R16. The receipt blob exists only at the input revision.
4. **"resolved input … commits".** The input revision is the single `^{commit}` peel of `--rev`. The measured revision must be a literal full lowercase OID equal to its own peel (rejecting tags, abbreviations, and uppercase).
5. **Target revision.** The target is wrapper `measured_revision`, which must equal stdout `commit` and argv `--rev`. The real `retention-floor-entering.json` has 9fb1f91 against e9f340c, so its exit 2 `receipt_revision_conflict` is expected. `measure-round22.py:83-84` already asserts this. That outcome is correct, not a defect.
6. **Which outcomes carry `argv` and provenance.** They appear on exit 0 and exit 1 only. Exit 2 carries only the sanitized code, which F24-H enforces.
7. **Policy digest lie exits 2, not 1** (F24-E).

## 7. Minor defects (fixable, non-blocking)

- `'argv':sys.argv[1:]` ignores `main(argv)` when the tool is called in-process. Use `argv if argv is not None else sys.argv[1:]`. The CLI arms are unaffected.
- `tool_sha256` is read after the scan, so a file replaced mid-run is digested as the new bytes. Digest at start. The measurement's `code_cp.stdout==tool.read_bytes()` check bounds this for admission.
- `--repo` is echoed in `argv` without any control-character check. For the real argv, a count-only check of the 9 frozen c1 policy classes across all 11 argv strings found 0 matches. Synthetic fixture paths under `.scratch/round22/…` cannot match `[R]22_SAMPLE`. Applying the same control-character rule as `safe_path` to `--repo` before echoing it closes the residual.
- Repo-local `info/grafts` still affects `merge-base --is-ancestor`, because `--no-replace-objects` does not disable grafts. A local graft could forge R14 ancestry. Setting `GIT_GRAFT_FILE` to a nonexistent path inside `git()` closes it. This is adjacent to R24 provenance and outside R24's exit contract.

## 8. Impacted axes and scores

- **Calibration (5):** an R24 pass is currently uninformative, because the M1–M7 survivors mean the claim "full provenance bindings retained" is not evidenced by any retained arm.
- **Depth (5):** binding lines exist in code but are undiscriminated.
- **Operability (7):** the exit-2 key contract is unfrozen (F24-H).

None of this argues for raising a score. R24 should not count toward the 24/24 until M1–M7 are killed by retained controls.

## Tooling

No installs or updates.
