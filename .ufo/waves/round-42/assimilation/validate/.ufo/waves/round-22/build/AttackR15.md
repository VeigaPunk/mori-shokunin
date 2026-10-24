# AttackR15 — R15 "changed policy bytes returns 2" (static review only)

Seat MoriR22.AttackR15. Static review only: no tests, builds, oracle or fixture runs; no installs. Every finding below comes from reading files and from read-only `git -C` plumbing (`ls-tree`, `cat-file`, `show`, `log`, `merge-base`, `status`). No measurement is claimed.

## Inputs read

- Contract `.ufo/waves/round-22/contract.md` (sha256 1658c390…21a1, matches `requirements.json.contract_sha256`).
- Frozen fixture builder `.ufo/waves/round-22/frozen/fixture-builder.py` and oracle `.ufo/waves/round-22/oracle-reconcile.py`, both from commit e825c7f.
- `tools/mori-retention-gate.py`, which defines the receipt `stdout` shape and the allowlist semantics.
- The real r21 receipt `.ufo/waves/round-21/evidence/final/retention-floor.json` (keys and scalars only; no hit text).
- No implementation candidate exists: `.scratch/round22` is absent and no `mori-retention-reconcile*` file was found. Nothing was polled.

## Verdict

R15 as frozen can be passed superficially, and the shipped fixture family has a defect that makes the R15 arm non-discriminating.

The fixture's mutation is strong on one axis. It appends a trailing `\n` to `policy.json` in the input commit, a byte change that does not change the parsed policy. That means it does reject implementations that compare parsed JSON or regex sets instead of bytes. It is weak on every other axis, because the oracle asserts only `exit==2`, `finding_id=="RETENTION_RECONCILIATION_SETUP"` and empty stderr. Every exit-2 path in the tool shares that `finding_id`, so any unrelated setup failure in the same fixture satisfies R15.

## Counterexample 1 (blocking): the fixture's allowlist is invalid under the existing gate, so R15 passes for the wrong reason

Evidence:
- `fixture-builder.py` lines 52–56 build allowlist rows as `{path, class, line_sha256, reason}`. There is no `rule` field.
- `mori-retention-gate.py` `_validate_allowlist` (lines 143–152) requires exactly `{"path","class","line_sha256","reason","rule"}` and `rule ∈ {"a","b","c"}`. Otherwise it raises `invalid_allowlist_row`, which exits 2.
- The contract requires raw partitions to "reproduce existing … allowlist semantics", and requires schema inconsistencies to "fail closed".

Consequence: a faithful reconciler rejects the allowlist in every variant with exit 2.
- R13–R21 (including R15) then pass for the wrong reason.
- R01–R12 and R22–R24 fail.
- The synthetic receipt claims `exit_code: 1`, which the real gate could never have produced on that tree.

A lenient reconciler that skips the `rule` check passes R01 but diverges from the gate semantics the contract mandates. Either way, the R15 pass is not caused by the policy change.

Smallest safe correction: before integration, add `row['rule']='a'` in `fixture-builder.py` (the existing gate selftest uses `"a"` for its allow arm). Then the `valid` control is a real-gate-reproducible receipt. Because the builder is frozen and committed, this needs an L1 decision. The alternative is a frozen ruling that the reconciler does not validate `rule`. That is a contract deviation and should be recorded as such.

## Counterexample 2 (blocking): the oracle cannot tell the R15 cause apart from any other setup failure

Evidence: `oracle-reconcile.py` uses `record('R15','policy-changed',2,'RETENTION_RECONCILIATION_SETUP')` with no predicate. The contract says setup emits a "sanitized error code", but no code value is frozen for R15.

These wrong implementations all pass R15 today:
- (a) A reconciler that always returns setup for any input revision ≠ measured revision. It would also fail R01, but R15 is still scored as passing, so the per-requirement pass count is inflated.
- (b) Counterexample 1.
- (c) A reconciler that runs its allowlist, receipt-schema or ancestor checks first and fails one of them.

Smallest safe correction: freeze an R15-specific error code and assert it.

```python
record('R15','policy-changed',2,'RETENTION_RECONCILIATION_SETUP',
       predicate=lambda v,f: v.get('error')=='policy_bytes_changed'
                             and v.get('receipt_match') is not True
                             and 'R22_SAMPLE' not in json.dumps(v))
```

The R15 run's stdout and stderr must also not contain `R22_SAMPLE`. The policy file is itself a hit source: line `"synthetic": "R22_SAMPLE"`, the exact r21 policy self-hit. An error path that echoes a policy diff or line would leak matched text, and R23 only checks the `valid` variant.

## Counterexample 3: an implementation that checks only the receipt's digest against the input policy passes R15 without reading the measured-revision blob

The receipt's `stdout.policy_sha256` is `sha256(P)`, where `P` is the measured bytes. In the `policy-changed` variant the input bytes are `P+"\n"`. An implementation that compares `receipt.policy_sha256` against `sha256(input blob)` gets a mismatch and returns 2. It passes R15 without ever comparing the input blob to the measured blob, which is the actual requirement.

Discriminating fixture "policy-changed-forged-digest":
- Measured commit has `policy.json = P`.
- The receipt `stdout.policy_sha256 = sha256(P+"\n")`.
- The input commit has `policy.json = P+"\n"`.

Expected: exit 2, `finding_id=RETENTION_RECONCILIATION_SETUP`, `error=policy_bytes_changed`, no counters claiming reconciliation. A receipt-vs-input-only implementation returns 0, because the digests agree and the recomputed hits are semantically identical.

## Counterexample 4: the precedence between setup and mismatch is not exercised

The trailing-newline arm never changes the recomputation, so it cannot catch an implementation that recomputes first and returns 1 on mismatch before running setup checks.

Discriminating fixture "policy-changed-semantic":
- The input commit's `policy.json` changes `non_author_paths_glob` from `["non-author.txt"]` to `[]`, or adds class `{"id":"R23","regex":"[a]llowed"}`.
- The receipt and measured tree are unchanged.

Expected: exit 2 with `error=policy_bytes_changed`, not exit 1 `RETENTION_RECONCILIATION_MISMATCH`. Frozen criterion: setup (2) takes precedence over mismatch (1), and policy/allowlist byte equality is checked before any recomputation or receipt-list comparison.

## Counterexample 5: worktree reads

The contract requires Git blobs, not the worktree. In every fixture variant the worktree equals the input commit, so a worktree reader is indistinguishable from a blob reader.

Discriminating arms:
- "policy-changed-worktree-reverted": the input commit has `P+"\n"`; after committing, write `P` back to the worktree file without staging it. Expected: exit 2, `policy_bytes_changed`. A worktree reader compares `P` to `P`, so it returns 0.
- "policy-dirty-worktree": `P` is committed at both revisions and the worktree holds `P+"\n"`, uncommitted. Expected: exit 0 `RETENTION_RECONCILED`. A worktree reader returns 2.

Byte reads must use `git cat-file blob <oid>` with object IDs from `ls-tree <resolved-commit> -- <path>`, as the existing gate does. Never use `git show <rev>:<path>`, `cat-file --filters` or `--textconv`, because attributes such as eol, smudge or textconv could rewrite the bytes. Both revisions must be read through the once-resolved commit object IDs, never the symbolic `--rev` string.

## Semantic ambiguities L1 must freeze

1. **Which policy path is compared.** The CLI `--policy` is a REPO_REL path, but the receipt `argv` carries an absolute `--policy` under the absolute `--repo`. In the real r21 receipt, `/…/mori-shokunin/.ufo/waves/round-18/frozen/c1-policy.json` relativizes to `.ufo/waves/round-18/frozen/c1-policy.json`.
   - Decoy counterexample: a tracked `policy-copy.json` with bytes `P` at both revisions, passed as `--policy`, while the receipt's argv `policy.json` changed. Byte equality on the supplied path passes, and the receipt digest `sha256(P)` also matches the decoy.
   - Proposed criterion: `relpath(argv[--policy], argv[--repo])` must equal `--policy` exactly; otherwise exit 2 `receipt_policy_path_mismatch`.
2. **Receipt digest vs committed bytes.** The r21 gate read the policy from the worktree (`read_json(args.policy)`), so equal blobs at both revisions do not prove the gate used those bytes. The only receipt-side witness is `stdout.policy_sha256`.
   - Proposed criterion: `stdout.policy_sha256 == sha256(blob at measured) == sha256(blob at input)`; otherwise exit 2 (`receipt_policy_digest_mismatch`), not 1, per the contract's "not silently current policy applied historically".
   - The allowlist has no digest in the receipt `stdout`, so the equivalent binding for R16 is weaker. That belongs to the R16 seat.
3. **Policy missing at one revision** (added after the measured commit, or deleted). Must be exit 2 with a distinct code such as `policy_missing_at_measured` / `policy_missing_at_input`, not a generic `git_read_failed`.
4. **Non-regular entries.** If the policy is a non-blob or mode 120000/160000 at either revision, it must be rejected with exit 2 (overlaps R21).
5. **Mode-only change with identical bytes** (100644→100755): bytes are equal, so evaluation proceeds. **A→B→A history**: equal at both endpoints, so it proceeds. Both are correct under "bytes at input revision must equal bytes at target revision". Freeze them explicitly so that no implementation adds a history-walk rule.
6. **Output shape on setup.** Proposed: exactly one JSON object `{finding_id, error, privacy_clearance:false}`, optionally with `policy_sha256_input` / `policy_sha256_measured`. Digests are not arbitrary bytes. No `raw_total`/`scanner_total`/`receipt_match:true`/`retention_state`, empty stderr, and no blob bytes.

## Real-repository check (not a measurement)

`.ufo/waves/round-18/frozen/c1-policy.json` is blob 8bf285bd… with sha256 db06e981…3128 at the measured commit 9fb1f911, at the entering commit 77a5bbe8 and at HEAD. That equals the receipt `stdout.policy_sha256`, and the worktree has the same digest. `corpus/evidence/retention-allowlist.json` is blob f8be55b1… (sha256 f46c78ec…) at all three revisions. 9fb1f911 is an ancestor of 77a5bbe8, and there are 0 commits touching either path in `9fb1f911..77a5bbe8`. So R15 and the proposed criteria in ambiguities 1–2 should not turn the real R02 run into a setup failure (inferred from the blob identities, not executed). The real receipt itself is tracked (blob 5c81c3f9…).

## Impacted axes

- **calibration**: false R15 passes inflate the per-requirement score.
- **depth**: the precedence and blob-versus-worktree semantics are untested.
- **operability**: an R15 pass is not attributable to the policy check.

## Exact actionable criterion (R15)

R15 passes if and only if all of these hold:

1. **Paired control.** The same fixture family with the policy unchanged returns exit 0 `RETENTION_RECONCILED`. This requires the Counterexample 1 fix: allowlist rows carry `rule`.
2. **Required arms.** Each of these returns exit 2, `finding_id=RETENTION_RECONCILIATION_SETUP`, `error=policy_bytes_changed`, empty stderr, no `R22_SAMPLE` in stdout or stderr, and no reconciliation counters or `receipt_match:true`:
   - `policy-changed` (trailing newline, already frozen);
   - `policy-changed-semantic` (Counterexample 4);
   - `policy-changed-forged-digest` (Counterexample 3);
   - `policy-changed-worktree-reverted` (Counterexample 5).
3. **Dirty worktree.** `policy-dirty-worktree` returns exit 0.
4. **Read discipline.** The policy bytes compared are the raw `cat-file blob` contents at the resolved input and measured commit object IDs, for the path bound to the receipt argv.

No tool installs or updates were performed.
