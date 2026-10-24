# CriticTrust — round-22 C1 retention reconciler (forged wrapper / revision / argv / mutable inputs)

Seat: MoriR22.CriticTrust (critic, leaf). Scope: contract.md design for `tools/mori-retention-reconcile.py` against the real r21 receipts. No implementation exists yet in the lane (`tools/mori-retention-reconcile*` absent), so this attacks the contract and the receipts it must consume.
Evidence was gathered with read-only `git -C` plumbing (`ls-tree`, `cat-file`, `log`, `merge-base`, `rev-parse`, `hash-object`), reads of committed JSON field names, counts, and paths, and Python `-c` checks of language semantics only. I ran no project tests, builds, linters, or gates. No matched text, regex bodies, or line contents were emitted. No tools were installed.

## Axes

The trust axes are: provenance, meaning which fields are bound to which actor or bytes; identity, meaning which commit, path, and blob; the denominator, meaning raw versus policy-excluded versus scanner; and fail-closed parsing. These map to the held scores as follows: calibration (5) for whether claims match evidence; depth (5); freshness (5), since revision semantics (S064) were reopened; and operability (7), for how exit codes are consumed downstream.

## Findings (severity order)

### T1 — The caller-chosen `--policy` path can relabel the 4 real unallowlisted hits as "policy source" (fixable defect, HIGH)
**Counterexample.** The tree contains a byte-identical copy of the policy:
- `.ufo/waves/round-18/frozen/c1-policy.json`
- `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json`

Both paths resolve to blob `8bf285bd…` at e9f340ce, 9fb1f911 and 77a5bbe8, and both have sha256 `db06e981…`, which equals the receipt's `policy_sha256`. All 4 r21 unallowlisted hits are in the copy, classes R2, R5, R6, and R8. The 4 hits at the real policy path are all allowlisted.

Now run `check --policy <copy path>`. Every contract check passes: the bytes are equal at input and target, the receipt's `policy_sha256` matches, the path is safe, and it is not a symlink. The only consequence is that the copy becomes the "policy-excluded" population. That gives policy_excluded=4, scanner_total=91, and **scanner_unallowlisted=0**. Requirement R04 still holds, because scanner equals raw minus policy-path hits. So the frozen requirements do not catch this.

**Impacted axes:** calibration and depth. The secondary denominator reads clean while the real retained result has 4 hits. That is the exact r21 failure mode of count subtraction posing as population equality.

**Smallest correction:**
1. Pin the policy-exclusion path as a constant in the committed expected-values file, created before integration, rather than trusting the caller.
2. Require `--policy` to equal the receipt argv's `--policy`, mapped to a repo-relative path (see T3).
3. Report `policy_blob_oid` and `policy_blob_alias_paths`, the other tracked paths with the same blob (1 here), so that identical copies are visibly kept in the scanner population.
4. Add one frozen requirement: "same-blob copy passed as `--policy` returns 2."

### T2 — The contract's "raw95 includes 5 policy source hits; scanner 90" does not match the receipt (calibration defect, HIGH)
**Evidence.** These counts come from `retention-floor.json` stdout. The receipt has 95 hits:
- 4 at the policy path, all allowlisted.
- 5 non-author hits: 3 in `corpus/lessons/round-17-verifier-spotcheck.md` and 2 in `corpus/lessons/round-18-verifier-spotcheck.md`.
- 86 allowlisted and 4 unallowlisted.

So 95 − 5 = 90 = 86 + 4. The 90 matches **non-author exclusion**, not policy-source exclusion. Under the contract's own definition (exactly the supplied policy path), the tool must report policy_excluded=4 and scanner_total=91.

No committed source for "90" or for "5 policy source hits" exists anywhere in the mori-shokunin tree outside contract.md. I searched with session dirs and wave JSON excluded. That 90 came from a non-author-excluding scanner is my inference.

**Risk.** If L1 expects 90, a correct tool "mismatches". The pressure is then to widen exclusion, which the contract forbids, or to declare the receipt wrong.

**Smallest correction.** L1 restates the r21 debt with identities rather than counts:
- policy-path hits = 4, all allowlisted.
- non-author = 5.
- raw_unallowlisted = 4, all in the NoHarmRun policy copy.
- The 90 figure is unexplained, or non-author-derived. It is not policy-source.

The R03 synthetic fixture (5/1/4) is unaffected.

### T3 — Wrapper revision fields are not the scanned commit (fixable defect, HIGH; freshness, S064)
**Evidence.**
- In `retention-floor-entering.json`, wrapper `measured_revision` = **9fb1f911**, while argv `--rev` = **e9f340ce** and stdout `commit` = e9f340ce.
- In `retention-floor.json`, all three fields = 9fb1f911.
- The hit lists of the two receipts are identical: the same 95 tuples in the same order.

No committed tool writes `mori-r21-command-receipt-v1`; the wrapper came from the L1 harness, so its field semantics are undocumented. Empirically, `measured_revision` is the capture-time worktree revision, where the tool, policy, and allowlist were read. It is not the scan target.

**Counterexample.** A reconciler that does what the contract literally says scans the wrapper's `measured_revision` as the "receipt target". For the entering receipt it scans 9fb1f911 and compares against the e9f340ce stdout. Every hit, partition, and count matches, because the hit lists are identical. It returns **RETENTION_RECONCILED** while binding the wrong commit, which is false provenance. Only a stdout `commit` comparison catches it, and the contract never names that field.

**Smallest correction.** Name three distinct fields and fail with exit 2 on any inconsistency:
- `scan_commit` = stdout `commit`. It must equal argv `--rev` literally: a full lowercase OID, not a symbolic ref, because `HEAD` or a branch cannot be re-resolved historically.
- `capture_revision` = wrapper `measured_revision`. Policy, allowlist, and claimed tool blobs are read here.
- `input_revision`.

Require that `scan_commit` is an ancestor of or equal to `capture_revision`, which is in turn an ancestor of or equal to `input_revision`. Also require `resolve(X^{commit}) == X` literally, so an annotated-tag OID cannot be peeled into a different identity. Add a frozen arm: the entering receipt with `commit` swapped returns 2.

### T4 — argv is attacker-shaped, and argparse semantics make naive parsing wrong (fixable defect, MEDIUM-HIGH)
**Evidence.** The gate's `build_parser()` uses argparse defaults. I checked argparse semantics locally:
- `--allow A` is accepted as an abbreviation of `--allowlist`.
- `--policy X --policy=Y` parses as policy=Y, because the last occurrence wins and the `=` form is accepted.
- `--allowlist` is optional, and `--expect-population` changes stdout fields and the finding.
- The r21 argv uses absolute worktree paths under the argv's own `--repo`.

**Counterexample.** A forged argv `[..., '--policy', <copy>, '--policy=<real>']` makes a first-match reader bind the copy, while the actual gate used the real policy. The gate also accepts `--allow` and `--expect-population`, so a literal `--allowlist` lookup misses an abbreviated flag and the reconciler misjudges whether an allowlist was applied.

**Smallest correction.** Accept only this exact form:

`argv == ['python3', <abs>/tools/mori-retention-gate.py, 'scan', '--repo', R, '--rev', OID, '--policy', R + '/' + policy_rel, ('--allowlist', R + '/' + allow_rel)?]`

Apply these rules:
- Use exact full option spellings, with no `=` forms, no repeats, and no `--expect-population`.
- Require absolute paths.
- Map paths through the argv's own `R`, not the current `--repo`, since clones differ.
- Do no path normalization: reject `//`, `/./`, and trailing `/`.

Anything else returns exit 2 `receipt_argv_unsupported`.

### T5 — Type forgery passes multiset equality in Python (fixable defect, MEDIUM-HIGH)
**Evidence.** I checked these Python language facts locally:
- `Counter([('p',1,'R2','x')]) == Counter([('p',1.0,…)])` is True, and the same holds with `True` in place of `1`.
- `json.loads` keeps the **last** duplicate key.
- `json.loads` accepts `NaN`.

**Counterexample.** A receipt with `"line": 1.0` or `true`, `"exit_code": true`, `"metric": 4.0`, or a duplicate `"hits"` key reconciles as exit 0. Contract R18 names only bool line and metric values. Float values and `exit_code`, `non_author`, and `routed` are uncovered. Duplicate keys let a forged first `hits` list be shown to humans or other parsers while Python checks the last one.

**Smallest correction:**
- Parse both the wrapper and stdout with an `object_pairs_hook` that rejects duplicate keys, and with `parse_constant` rejecting NaN and Infinity.
- Check every integer field with `type(v) is int`.
- Strongest and cheapest: also report `stdout_canonical_match`, meaning receipt stdout equals `json.dumps(recomputed, sort_keys=True, separators=(",",":")) + "\n"`. That is the gate's exact `emit` format. Diff only known fields for the exit-1 decision, so unknown fields stay permitted.

### T6 — Git object substitution and inherited environment are common-mode for both the gate and the reconciler (fixable defect, MEDIUM)
**Evidence.** The gate's `_git` is `["git","-C",repo,*args]`, run with the inherited environment and repo config and without `--no-replace-objects`. In the live repo today: 0 `refs/replace/*`, no `objects/info/alternates`, no `info/grafts`, and not shallow. This was observed with read-only `rev-parse` and a directory listing; git version is 2.56.0.

**Counterexample.** A fixture or any `--repo` with `refs/replace/<blob>` (or `GIT_DIR`, `GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_REPLACE_REF_BASE`, `GIT_GRAFT_FILE`, or `GIT_CONFIG_*` in the environment) substitutes the bytes of the receipt, policy, or any tree blob. It can also change commit parents, which forges ancestry, while every OID string still looks right. "Independent recomputation" then agrees with a forged receipt because both read the same substituted store.

Pathspec magic is a second issue: `ls-tree REV -- ':(glob)**/c1-policy.json'` or a path containing `*` passes the contract's safe-path rules, which exclude only absolute, dotdot, empty, and control characters, and can match a different file.

**Smallest correction:**
- Run git with a scratch environment: `PATH`, `LC_ALL=C`, `GIT_NO_REPLACE_OBJECTS=1`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, and no other `GIT_*` variables.
- Add the global flags `--no-replace-objects --literal-pathspecs`.
- Require exactly one `ls-tree` record whose path bytes equal the input path, with mode `100644` or `100755`. This rejects `120000` and `160000` at the input, capture, and scan revisions.
- Reject `.` segments, `//`, and leading `:`.
- Record `git rev-parse --absolute-git-dir` and the object format in the output receipt.

### T7 — Hashes bind bytes, not actors or runs (tradeoff; wording and label fix, MEDIUM)
**Evidence.** The wrapper's `schema`, `cwd`, `started_utc`, `elapsed_seconds`, `exit_code`, `stderr`, and argv[0] (`python3`, resolved through PATH) are all unauthenticated. No tool or interpreter digest is in the r21 receipt. The gate tool blob is `988c5484…` at both e9f340ce and 9fb1f911, but the capture read worktree files whose cleanliness is unprovable.

`policy_sha256` is self-reported. Allowlist bytes have no digest. Their effects are fully observable through `allowlisted_hits`, `warnings`, and `forbidden_allowlist`; the only invisible part is `reason` and `rule` text.

**Counterexample.** Anyone can author a wrapper whose stdout is regenerated from the committed tree, and it reconciles as exit 0. RECONCILED proves only that the receipt content is consistent with recomputation. It does not prove that the gate ran, when it ran, or with what code.

**Smallest correction:**
- Emit `receipt_authenticity: "unattested"` and `claimed_tool_blob` labeled as unattested.
- Have the reconciler's own receipt record both the on-disk `__file__` sha256 and the tool blob OID at `input_revision`, plus a `tool_matches_input_rev` boolean.
- The lesson and knowledge drafts must not cite exit 0 as evidence that the r21 measurement occurred.

This is not something the canonical Rust judge should reject. It is a scope label.

### T8 — The receipt file at the input revision is a mutable carrier (low; fixable)
**Evidence.** Both receipts were first added at 77a5bbe8. Their committed blobs (`5c81c3f9…` and `df160d7c…`) equal the current worktree `hash-object`. Byte-unchanged holds today.

**Counterexample.** The receipt is read at `--rev`. A later commit could amend the receipt bytes, and reconciliation would then validate the amended version.

**Smallest correction.** Report the receipt's blob OID and its first-add commit. Mark `receipt_amended_since_first_add` true if the blob differs from the first-add blob. That does not need to be exit 2; it is a provenance field.

### T9 — Exit 0 on a red retention state (accepted tradeoff, LOW; operability)
Under the contract, exit 0 means RETENTION_RECONCILED even when `retention_state=red`. Any consumer that gates on the exit code reads "pass". `privacy_clearance` must be the literal JSON `false` constant, never derived. `retention_state` must be required in the output. This is consistent with the contract; flag it in documentation only.

## Not defects (checked)
- Duplicate hits: neither r21 receipt has any (0 duplicates), and all `line` values are `int`.
- The policy and allowlist blobs (`8bf285bd`, `f8be55b1`) are unchanged across e9f340ce, 9fb1f911, and 77a5bbe8. So R15 and R16 do not trip on the real receipts, and the comparison remains meaningful only together with T1 and T3.
- The allowlist at 9fb1f911 is a dict with a `rows` key (86 rows). The reconciler must reproduce the gate's dict-to-`rows` unwrap.
- Adjacent, outside this lane: `fnmatch` `*` crosses `/`. So `corpus/lessons/round-*-verifier-spotcheck.md` silently treats any nested `round-…/…-verifier-spotcheck.md` as non-author. The reconciler must reproduce this, and should report the matched glob per non-author hit. Population critics own this.

## Proposed added frozen arms
These must be committed before integration, and are not claimed run:
1. Same-blob policy copy passed as `--policy` returns 2 (T1).
2. Wrapper `measured_revision` differing from stdout `commit` or argv `--rev` returns 2 unless the ancestry chain holds and fields are distinct, with the entering receipt as the real case (T3).
3. Repeated, abbreviated, or `=` argv options, or `--expect-population`, return 2 (T4).
4. Float or boolean values for `line`, `exit_code`, or `metric`, a duplicate JSON key, or NaN return 2 (T5).
5. A `refs/replace` blob substitution, a `GIT_DIR` environment override, or a pathspec-magic path returns 2 or is neutralized (T6).
6. Output contains `receipt_authenticity="unattested"` and `privacy_clearance=false` (T7 and T9).

## Tool installs
None.
