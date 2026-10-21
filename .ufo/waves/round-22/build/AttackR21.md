# AttackR21 — frozen requirement R21 ("symlink input reject2")

Seat: MoriR22.AttackR21 (critic, static review only). No tests, builds, or fixtures were run. No tools were installed. Every claim below comes from a file or a read-only `git -C` plumbing read; anything not observed is marked [INFERENCE].

## Contract text under attack

- R21: "symlink input reject2".
- The contract body says: "Safe repo-relative paths: no absolute, dotdot, empty, controls; committed symlink input is rejected." It also says "Read receipt/policy/allowlist via Git blobs, not worktree" and "Policy and allowlist bytes at input revision must equal bytes at target revision."
- The three inputs are `--receipt`, `--policy` and `--allowlist`, all repo-relative and read at `--rev`. Policy and allowlist are also read at the receipt's target revision for the byte-equality check.

## State observed

- No candidate implementation, fixture generator or oracle exists yet. `tools/mori-retention-reconcile.py` is absent, `.scratch/round22` is absent, and `build/` contains only `swarm-registry.json`. This review therefore attacks the requirement and the existing gate's semantics, not a candidate.
- At 9fb1f911, e9f340ce and 77a5bbe8, the real inputs are all plain blobs with mode 100644: `.ufo/waves/round-18/frozen/c1-policy.json` (blob 8bf285bd, whose sha256 db06e981… equals the receipt's `policy_sha256`) and `corpus/evidence/retention-allowlist.json` (blob f8be55b1). `.ufo/waves/round-21/evidence/final/retention-floor.json` is a mode-100644 blob at 77a5bbe8 and is absent at 9fb1f911.
- Each of those trees contains 4 committed symlinks (mode 120000), all under `.ufo/waves/round-17/fixtures/seat/{SecurityRootSymlink,SymlinkIgnore}/`. The retained receipt has 0 hits on those paths.
- The existing gate (`tools/mori-retention-gate.py`, lines 199–203) skips only `kind != blob` and mode `160000`. It **scans mode-120000 symlink blobs**, meaning the link-target text, as ordinary content.

## Why R21 can pass superficially

`git cat-file blob <rev>:<path>` (and `git show <rev>:<path>`) does not follow a final-component symlink. It returns the link-target bytes. If the symlink fixture's target is a short string such as `real-policy.json`, the tool exits 2 because of `invalid_json` or a schema failure, not because it detected a symlink. With no mode check at all, the arm still shows exit 2 and `RETENTION_RECONCILIATION_SETUP`. All setup errors share that one finding_id, so the contract's "assertions include exit and finding_id" cannot tell the causes apart.

## Counterexample fixtures (strongest first)

Each fixture is a synthetic Git repo in the executor's own clone. Build it from a valid R01 baseline: the receipt, policy and allowlist that return exit 0 `RETENTION_RECONCILED`. Then change exactly one tree entry.

**F1. Symlink whose blob is a valid input, read at the input revision (decisive).**
- Setup: `B=$(git hash-object -w valid-policy.json)`, then `git update-index --add --cacheinfo 120000,$B,policy.json`, then commit. The tree entry is a symlink whose blob bytes equal the valid policy exactly, so the blob OID is the same as the baseline regular file's.
- Run three variants, one per input: policy, allowlist, receipt.
- Expected: exit 2, finding_id `RETENTION_RECONCILIATION_SETUP`, a symlink-specific sanitized error code (for example `input_symlink`), and no `raw_total` or other metrics emitted.
- A mode-blind tool returns exit 0 `RETENTION_RECONCILED`. Content-equality and digest checks cannot catch this, because the bytes and OID are identical.

**F2. Mode differs only at the target revision.**
- Setup: the target commit T has `policy.json` as a mode-120000 entry with blob B. The input commit I, a descendant of T, has the same path as mode 100644 with the same blob B. Run the mirror case too (regular at T, symlink at I), and both cases for the allowlist.
- Expected: exit 2 with the symlink error code in all 4 variants.
- A tool that checks mode only at `--rev`, or compares only bytes or OIDs across revisions, accepts this. Byte equality holds, so the "changed policy bytes" check (R15/R16) does not fire.

**F3. Worktree and index disagree with the committed mode.**
- Setup: commit F1's symlink entry, then put a regular file with valid content at that worktree path without staging it. Separately, commit a regular file and replace the worktree path with a symlink.
- Expected: the committed symlink gives exit 2 with the symlink code. The committed regular file gives exit 0, the same as R01.
- This catches `os.path.islink(repo/path)`, `Path.resolve()` and other worktree checks in both directions. It also catches any worktree open, which the contract forbids.

**F4. Symlinked parent directory.**
- Setup: `cfg` is committed as mode 120000 with target `real`, `real/policy.json` is a regular file, and `--policy cfg/policy.json` is passed.
- Expected: exit 2 with no data emitted. A specific error code is preferred; at minimum the input must be unresolved, never a successful read.
- This catches `git cat-file --batch --follow-symlinks`, which would resolve the path and return exit 0.

**F5. Over-application guard. This fixture must not be rejected.**
- Setup: in the R01 baseline, add one non-input committed symlink (mode 120000) whose target text matches one class. Reuse the R4-matching fixture bytes from the gate selftest, `second_text` at `tools/mori-retention-gate.py:566`; do not decode it into the report. Produce the receipt with the existing gate at that commit.
- Expected: exit 0 `RETENTION_RECONCILED`, and `raw_total` is one higher than the baseline because the symlink hit is counted. The hit identity is (link path, line 1, class, sha256 of the target text).
- A tool that applies R21 by skipping every symlink blob in the scan gets a dropped hit and returns exit 1 `MISMATCH` on a valid receipt. A tool that rejects any tree containing symlinks returns exit 2.
- The real tree has 4 symlinks but 0 hits on them, so only this synthetic fixture can catch the divergence.

**F6. Mode acceptance boundary.**
- Mode 100755 inputs must be accepted (exit 0).
- Mode 160000 (gitlink) and 040000 (tree) inputs must give exit 2. These cases fall under R20/R13-style setup handling rather than R21, but the same mode gate decides them.

## Exact actionable criterion for R21

For each input path, at every revision where that input is read, the tool should run:

`git -C REPO --literal-pathspecs ls-tree -z --full-tree <resolved-commit> -- <path>`

That revision set is the receipt at `--rev`, and the policy and allowlist at both `--rev` and the target `measured_revision`. Accept only if:

- the output has exactly one record,
- its path bytes equal the requested path byte-for-byte,
- its type is `blob`,
- its mode is `100644` or `100755`.

Then read the blob by the OID taken from that record, not by `rev:path`, and never with `--follow-symlinks`.

- A mode of `120000` gives exit 2 `RETENTION_RECONCILIATION_SETUP` with a dedicated sanitized code, checked before any parsing.
- An empty result, which is how a symlinked parent shows up, gives exit 2 with a missing or unresolved code.
- There must be no worktree `stat`, `islink`, `open` or `readlink`.
- Scan population semantics are unchanged: mode-120000 blobs anywhere else are scanned exactly as the existing gate scans them.

The `--selftest` R21 arms should be F1 (policy, allowlist and receipt), F2 (both directions), F3 and F4. Each must assert exit == 2, finding_id == `RETENTION_RECONCILIATION_SETUP`, the symlink-specific error code, the absence of all metric keys, and that stdout/stderr contain no input-blob bytes. The F5 arm must assert exit == 0, `receipt_match` true, and the +1 raw count. An R21 arm that asserts only exit and finding_id is a superficial pass.

## Semantic ambiguities L1 must pin

- **A1: which revision is the "target revision".** In the round-21 entering receipt (`retention-floor-entering.json`), the wrapper `measured_revision` is 9fb1f911, but `argv --rev` and stdout `commit` are e9f340ce. The tool must pick one authority for the target revision and check that the others agree; the agreement check is R13/R24. Whichever revision is chosen is also where the F2 mode check runs. A tool that checks mode at the wrong one of the two commits passes F2 only by accident.
- **A2: the mode check applies to all three inputs.** The contract groups "committed symlink input" with the path rules for all inputs. The receipt is read only at `--rev`; it is absent at the real target 9fb1f911, so it must not be required there.
- **A3: R21 covers committed tree entries only.** Rejecting a symlinked `--repo` directory or `.git` would be extra scope that no frozen requirement asks for.
- **A4: error-code granularity.** The contract requires "sanitized error code only" but freezes no name. The selftest and oracle should freeze one exact string for the symlink case so that F1 through F4 cannot be satisfied by `invalid_json`.

## Cross-requirement observation (outside R21; for L1)

In the retained receipt (`retention-floor.json` stdout), exactly 4 hits sit on the supplied policy path `.ufo/waves/round-18/frozen/c1-policy.json`. Another 4 sit on its copy `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json`. The open-debt statement says "raw95 includes5policy source hits" and "scanner90". Excluding exactly the one supplied path, as the contract mandates, gives `policy_excluded=4` and `scanner_total=91`, not 5 and 90. This is a count from the retained receipt, not a recomputation.

There is a risk that an implementer widens the exclusion until it reaches 90. The contract forbids exactly that ("never broad regex/path exclusions"). The R02/R03/R04 seats should reconcile which population the "5" and "90" figures came from.

## Impacted axes

Calibration (C1): a superficial R21 pass would inflate a requirement's status. Correctness of the denominator: F5 guards against undercounting symlink hits in `raw_total`. Provenance: F2 guards the target/input byte-equality binding.

## Smallest safe correction

Add the single per-input `ls-tree` mode gate described above (one function, called for each input and revision before any blob is parsed). Add the symlink-specific error code to the R21 selftest assertions. Add F5 as a no-regression arm. Make no change to the scan loop, the existing gate, the policy, the allowlist or history.
