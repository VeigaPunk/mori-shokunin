# ReceiptBinding — r21 retention-floor receipt: missing bindings and committed-byte checks

Seat: MoriR22.ReceiptBinding (scout, read-only). Scope: `.ufo/waves/round-21/evidence/final/retention-floor.json` plus the evidence its argv names directly (`tools/mori-retention-gate.py`, `.ufo/waves/round-18/frozen/c1-policy.json`, `corpus/evidence/retention-allowlist.json`). No tests, builds, gate runs, or full-tree rescan were run. The only checks were read-only `git -C` plumbing (`rev-parse`, `cat-file`, `ls-tree`, `log`, `merge-base`, `diff`, a `git grep -l` limited to `tools/` and `.ufo/waves/round-21`) and partition arithmetic over committed blob bytes and the receipt's own hit lists. Nothing was installed. No matched text appears below.

## Verdict

- The wrapper does not bind its inputs. It names the policy, allowlist, and tool only by absolute worktree path. Apart from the policy digest that the gate reports about itself inside `stdout`, it carries no digest, blob ID, or tree binding for any of them. Its `cwd`, `started_utc`, and `elapsed_seconds` are unauthenticated self-reports.
- The independent committed-byte checks I ran are all consistent with the receipt. They were run after the fact against git objects, so they rule out a mismatch at the committed level. They cannot prove which bytes the worktree held at run time.
- **Denominator finding (affects the contract's open-debt wording):** the receipt contains **4** hits at the exact policy path, not 5. Removing the exact policy path by identity gives **91**, not 90. The only partition in this receipt that has exactly 5 members is `non_author` (the `corpus/lessons/*-verifier-spotcheck.md` hits), and 95 − 5 = 90 is the gate's own `metric_before` formula (`_population_summary`). [INFERENCE] The "95 including 5 policy-source hits, scanner 90" figure most likely conflates the non-author exclusion with the policy-source exclusion. That is the count-subtraction failure the contract's root lesson warns about.

## Observed facts

### Wrapper shape (`mori-r21-command-receipt-v1`)

- Wrapper keys: `schema, measured_revision, argv, cwd, started_utc, elapsed_seconds, exit_code, stdout, stderr`.
- Inner `stdout` keys: `allowlisted_hits, commit, finding_id, forbidden_allowlist, hits, metric, non_author, policy_sha256, routed, unallowlisted_hits, warnings`.
- `measured_revision` = `argv --rev` = inner `commit` = `9fb1f911cfdd6061005c300795f44b1b45523897` (a full commit ID that resolves to a commit object).
- `cwd` equals `argv --repo`. `exit_code` is an int (1) and `elapsed_seconds` is a float. `stdout` is the gate's canonical `json.dumps(sort_keys, compact)+"\n"` byte-for-byte. `stderr` is empty.
- Producer: `git grep -l mori-r21-command-receipt-v1 HEAD -- tools .ufo/waves/round-21` matches only evidence files. No committed tool under `tools/` writes or validates this wrapper schema.
- `tools/mori-retention-reconcile.py` is absent at HEAD, so the baseline is `capability_absent`.

### How the gate reads its inputs (`tools/mori-retention-gate.py`)

- The tree scan uses committed objects: `_scan_git_revision` does `cat-file --batch-check <rev>^{commit}`, then `ls-tree -r -z --full-tree`, then `cat-file blob` for each entry. It skips gitlinks and non-blobs. `_blob_hits` skips blobs containing NUL, decodes with `errors="replace"`, and splits on `"\n"`.
- `--policy` and `--allowlist` are **worktree reads**: `read_json`, which calls `Path(path).read_bytes()` (`scan()`, lines 310–320). The reported `policy_sha256` is the SHA-256 of whatever worktree bytes were read. No allowlist digest is computed or emitted.
- The allowlist key is `(path, class, line_sha256)` with no line number, and a dict-form allowlist's `schema` is not checked. Non-author matching uses `fnmatch.fnmatch`, where `*` can match across `/`.

### Independent committed-byte checks (run)

| Input | Blob at measured revision | SHA-256 of committed bytes | Same at HEAD and in worktree now |
|---|---|---|---|
| gate `tools/mori-retention-gate.py` (100755) | `988c5484…` | `cf0896a2…829e` | yes |
| policy `.ufo/waves/round-18/frozen/c1-policy.json` | `8bf285bd…` | `db06e981…3128`, which equals inner `policy_sha256` | yes |
| allowlist `corpus/evidence/retention-allowlist.json` | `f8be55b1…` | `f46c78ec…c63b`, which is not bound anywhere in the receipt | yes |

- None of the three inputs changed between the measured revision and HEAD (`git diff --quiet`). Their last touching commits (`29b0dc7`, `3127c3a`, `9db5168`) all predate the measured revision.
- The measured revision is an ancestor of the receipt's landing commit `77a5bbe` (1 commit apart) and of HEAD `306e06ec`. The receipt itself is not in the measured tree, which is expected because it was landed afterwards.

### Partitions recomputed from committed allowlist and policy bytes against the receipt's `hits`

- `hits` = 95, all distinct, sorted by path and then line. `allowlisted_hits` = 86, `unallowlisted_hits` = 4, `non_author` = 5. 86 + 4 + 5 = 95 with no residual and no overlap between the allowlisted and non-author sets.
- The allowlist has 86 rows: 0 forbidden (no row is on a must-redact path), 0 stale, and no line-free key matching more than one hit.
- The recomputed allowlisted and unallowlisted lists equal the receipt's lists exactly, by ordered identity `(path, line, class, line_sha256)`. `metric` = 4, `routed` = 0, `finding_id` = `RETENTION_FINDINGS`, and `exit_code` = 1 are all consistent with this.
- Policy-source hits:
  - The exact policy path has 4 hits (classes R2, R5, R6, R8), and all 4 are allowlisted.
  - `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json` is the **same blob** (`8bf285bd…`, last touched `71abd41`). It has 4 hits, and **all 4 unallowlisted hits are this copy**.
  - So an exact-path policy exclusion gives scanner_total = 91 with scanner_unallowlisted = 4 unchanged. Excluding both paths gives 87. Neither result is 90.
- Not run: an independent regex rescan of every tracked blob. That recomputation is R01's job and is L1's measurement after integration, so the raw 95 itself has not been re-derived here.

## Bindings missing from the wrapper (each should be required, checked against committed bytes)

1. **Policy binding.** Record the input revision, repo-relative path, blob ID, and byte SHA-256 of the policy. Do not use an absolute worktree path. Check the SHA-256 of `cat-file blob <measured>:<path>` against the inner `policy_sha256`. The inner value alone is the verified tool attesting to its own input and does not count.
2. **Allowlist binding.** The receipt has nothing for the allowlist today. Record its repo-relative path, blob ID, and SHA-256 at the measured revision, and require identical bytes at the input revision (R16).
3. **Tool binding.** Record the gate's repo-relative path, blob ID, mode, and SHA-256 at the measured revision. `argv[0]` is an unresolved `python3`; record the interpreter and git versions as unauthenticated metadata only.
4. **Tree binding.** Record the resolved commit and tree ID, plus whether any tracked file was dirty at run time. Today only the gate's tree scan is pinned by `--rev`, while policy and allowlist come from the worktree. The fact that the committed bytes match now is an after-the-fact consistency check, not proof of what the run read.
5. **Argument form.** Replace absolute `--repo` and worktree paths in argv with repo-relative selectors read through `git cat-file`. Reject `..`, absolute paths, control characters, and committed symlinks (R20, R21).
6. **Do not trust `cwd`, `started_utc`, or `elapsed_seconds`.** None of them proves anything. The timeline (measured commit 13:29:35Z, run 13:31:10Z, landed 13:36:27Z) only shows ordering consistency.
7. **Producer.** No committed writer or validator exists for `mori-r21-command-receipt-v1`. The reconciler has to fail closed on wrong required-field types or schema itself, for example bool versus int for `exit_code` and `line` (R18), and duplicate hits (R19). The receipt passes these shape checks today: it has 0 duplicates and integer types.
8. **Denominator labels.** Report `raw_total` (95), `policy_excluded` (exact path only: 4), `scanner_total` (91), and `non_author` (5) as separate identity lists or digests. Never derive 90 by subtraction. Keep the identical-blob copy outside the policy exclusion, which keeps `scanner_unallowlisted` = 4 and `privacy_clearance` = false.

## Confidence and remaining unknowns

- High confidence: wrapper shape, the gate's worktree reads, the committed-blob digests, input stability from the measured revision to HEAD, and the partition identities. All come from the reads and plumbing above.
- Medium confidence [INFERENCE]: that "5 policy / 90 scanner" comes from the non-author exclusion. The origin of the scanner-90 figure is outside this seat's allowed sources and was not opened.
- Unknown: the worktree bytes and dirty state at 13:31:10Z, which nothing recorded and which cannot be recovered; the raw 95 recomputed independently, which L1 measures under R01; and the dispositions of the historical waves, which remain unknown.
