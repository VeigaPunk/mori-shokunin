# GateGit — Git tree modes, symlink blobs, object-id handling in `tools/mori-retention-gate.py`

Seat: MoriR22.GateGit (read-only scout). Scope: the named file plus direct, read-only git plumbing and the installed git man pages. No tests, builds, fixtures or probes were run. No matched text appears here. No tools installed or updated.

Observed environment facts (read-only commands): git 2.56.0. The entering revision `77a5bbe8a0b41dfbfd2546d024d36e294b814bd0` is a commit in a sha1 repo. It is not shallow, has no partial-clone extension, and has 0 `refs/replace/*` refs. Its full-tree mode census is 7368 `100644 blob`, 378 `100755 blob`, 4 `120000 blob`, 0 gitlinks. All four symlinks live under `.ufo/waves/round-17/fixtures/seat/` (`SecurityRootSymlink/root-link`, `SymlinkIgnore/Dangling.jsonl`, `SymlinkIgnore/Link.jsonl`, `SymlinkIgnore/linked-dir`). I did not check whether their target strings produce hits under the c1 policy, so the r21 population's dependence on them is **unmeasured**.

## 1. How the gate scans a tree (observed, lines 177–204)

- **Revision resolution:** `git -C <repo> cat-file --batch-check=%(objectname) %(objecttype)` receives `<rev>^{commit}\n` on stdin. Because the revision travels on stdin, there is no argv/option injection. NUL and LF are rejected up front. Missing or ambiguous names print `<name> missing|ambiguous`. A name containing spaces yields more than 2 tokens. In all these cases `len != 2`, `type != commit`, or `OBJECT_ID_RE` fails, and the gate raises `revision_not_commit` (exit 2).
  - `^{commit}` peels annotated tags. Any rev-expression is accepted: `HEAD`, abbreviations, `@{-1}`, `branch~3`. The full resolved id is emitted as `commit`.
  - The gate does **not** require that `--rev` already be a full id. The reconciler contract does require it ("receipt measured_revision must be full commit"), so the reconciler needs its own full-id-equality check. The gate gives it nothing to inherit here.
- **`OBJECT_ID_RE`** is `[0-9a-f]{40}|[0-9a-f]{64}`, lowercase only. It accepts both sha1 and sha256 lengths, without checking that the length matches the repo's object format. It is applied to the resolved commit and to population `commit`. It is **not** applied to the tree-entry object ids.
- **Tree listing:** `ls-tree -r -z --full-tree <commit>`.
  - `-r` without `-t` means tree entries never appear. Only leaf entries do: blobs of any mode, plus gitlinks.
  - `--full-tree` makes the listing independent of `--repo` pointing at a subdirectory.
  - `-z` means paths are unquoted. The split on the first `\t` is safe because the metadata never contains a tab, and paths containing tab or LF are kept intact.
- **Entry filter:** `if kind != b"blob" or mode == b"160000": continue`.
  - Gitlinks (`160000`) always have kind `commit`, so the mode clause is redundant (harmless). Submodule contents are skipped silently: no hit, no count, no diagnostic.
  - `100644`, `100755` and **`120000`** entries all have kind `blob` and are **all scanned identically**. The executable bit has no effect.
- **Blob read:** one `git cat-file blob <oid>` subprocess per entry, with the oid passed as argv (hex from git's own output, so no injection). `cat-file blob` returns raw object bytes. No textconv, smudge, eol or `.gitattributes` filters run (those require `--filters`/`--textconv`). The worktree is never consulted for scanned content.
- **Errors:** any non-zero git exit maps to `git_read_failed` (exit 2). A non-ASCII oid would raise `UnicodeDecodeError`, which falls through to `internal_error` (exit 2). That is unreachable with honest git output.

## 2. Symlink content scan vs. symlink input rejection (the key distinction)

**A. Scanning symlink blobs (gate behavior; the reconciler must reproduce it).**
- A `120000` blob's bytes are the link target string. Git never follows it.
- The gate scans this string like any text file:
  - The NUL check almost never fires.
  - There is usually no trailing LF, so the target is line 1 and no empty line 2 is added.
  - It is decoded with `errors="replace"`, and every class regex is applied to it.
- A committed symlink whose target text matches a policy class therefore yields a hit `(path, 1, class, sha256(target))`. Dangling links are scanned the same way, and so are links pointing outside the repo or at directories (`linked-dir`). The target is never resolved or opened.
- For exact multiset agreement, the reconciler's independent scan **MUST include `120000` blobs as content**. It must not skip them, follow them, or reject them. Skipping them would make the reconciler disagree with any receipt whose population includes a symlink-target hit. That would be a false `RETENTION_RECONCILIATION_MISMATCH` (exit 1) or a hidden undercount.
- The reconciler must still skip `160000` entries (and not recurse into submodules), and it must ignore tree entries.

**B. Rejecting symlink input files (reconciler contract R21; the gate has no equivalent).**
- The gate reads `--policy`, `--allowlist` and `--expect-population` from the **filesystem** via `Path.read_bytes()` (lines 49–55, 311, 317, 323). Symlinks there are **followed**, and nothing checks the git tree.
- Consequence: the `policy_sha256` recorded in a historical receipt is the sha256 of the worktree/filesystem bytes the gate saw at run time, not necessarily the committed blob. When the reconciler compares committed blob bytes to the receipt digest, a mismatch may mean the run used dirty or uncommitted bytes. Per contract, that is unevaluable (exit 2), not proof of a defect.
- R21 concerns the *input* paths `--receipt`, `--policy` and `--allowlist`, resolved inside `--rev` (and the measured revision for byte-equality). If an input entry has mode `120000`, it must be rejected with exit 2 before any bytes are interpreted.
  - Do not use `git cat-file blob <rev>:<path>` or `git show <rev>:<path>` alone. On a symlink they return the target string without error. The JSON parse would then usually fail, giving exit 2 with the wrong reason (malformed JSON instead of symlink), and a crafted target could even parse.
  - Recommended lookup:
    1. Run `git ls-tree -z --full-tree <commit> -- <path>` with `GIT_LITERAL_PATHSPECS=1`. The ls-tree man page says paths are "a list of patterns to match", so literal mode prevents glob or magic interpretation.
    2. Require exactly one entry whose decoded path equals the input byte-for-byte.
    3. Require mode `100644` or `100755` and kind `blob`. Reject `120000`, `160000` and `tree`.
    4. Only then run `cat-file blob <oid>`, validating the oid with the object-id regex first.
  - A path whose *parent directory* is a committed symlink cannot be reached through the tree: ls-tree descends only real trees. So it yields no entry, which is the "unresolvable input" case (exit 2). Report that case as missing input, not as a symlink.

Summary: symlinks as **scanned content** are in-population and must be counted. Symlinks as **reconciler inputs** must be rejected. Neither behavior may borrow the other's rule.

## 3. Object-id and git-environment risks the gate does not guard (reconciler should not inherit them)

1. **Replace refs** (high relevance to "measured tree" authenticity). From `git-replace(1)` (installed): "Replacement references will be used by default by all Git commands except those doing reachability traversal". `cat-file`, `ls-tree` and blob reads therefore honor `refs/replace/*`. The gate reports the original commit id, but the content it reads could be substituted. The current repo has 0 replace refs, so this is not observed in the retained receipt; it is a latent risk.
   - Reconciler: run `git --no-replace-objects` or set `GIT_NO_REPLACE_OBJECTS=1` (documented in `git(1)`).
   - [INFERENCE] `%(objectname)` from batch-check reports the requested, unreplaced id.
2. **Inherited `GIT_*` environment.** `_git` passes the caller's environment unchanged. `GIT_DIR`, `GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_NAMESPACE`, `GIT_REPLACE_REF_BASE`, `GIT_CONFIG_*` and `GIT_CEILING_DIRECTORIES` can redirect which repo or objects are read, despite `-C`. Only the selftest sets `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1`, and only for its fixtures. Reconciler: build a scrubbed env with those set, and drop every inherited `GIT_*` variable.
3. **Lazy fetch.** In a partial clone, a missing blob would trigger a promisor fetch (network, not read-only). `git(1)` documents `GIT_NO_LAZY_FETCH` set to `1`. The current repo has no partial-clone extension, so this is not observed. Reconciler: set `GIT_NO_LAZY_FETCH=1` so a missing blob fails closed as exit 2.
4. **Ancestry (R14).** Grafts and shallow boundaries affect `merge-base --is-ancestor`. The repo is not shallow (observed). [INFERENCE] With `--no-replace-objects` and no grafts, ancestry is the plain commit graph. On a shallow clone, a false "not ancestor" result maps to exit 2 per contract, which is acceptable.
5. **Object-format consistency.** `OBJECT_ID_RE` accepts 64-hex in a sha1 repo. Batch-check would then report `missing`, so the outcome is still fail-closed exit 2. No defect; noted for the reconciler's full-id check.

## 4. Text-identity semantics the reconciler must replicate exactly (observed, lines 89–103, 186–203)

- Skip the blob if it contains `b"\0"` anywhere (R22). Otherwise decode with `utf-8, errors="replace"` and split on `"\n"` only:
  - CR is kept in a CRLF line, so the digest includes it.
  - A trailing LF produces a final empty line N+1.
  - The line number starts at 1.
- `line_sha256 = sha256(decoded_line.encode("utf-8"))`. This is the digest of the **replacement-decoded** text, not the original bytes. Two different invalid byte sequences in a line can collide.
- The path is `path_bytes.decode("utf-8", errors="replace")`. Two distinct non-UTF-8 paths can decode to the same string. That is the only way the gate can emit two identical `(path, line, class, line_sha256)` hits. Within one file, each line gets at most one hit per class.
  - Interaction with the contract ("preserve duplicates as multiset but reject duplicate receipt hits"): a legitimate gate run on such a tree would produce a receipt the reconciler rejects (exit 2). The current tree's path encoding was not inspected, so it is unmeasured whether any non-UTF-8 paths exist.
  - Recommend recording this as a known boundary, not silently de-duplicating.
- Hits are ordered by `ls-tree` order (git's byte-sorted path order within each tree, recursive), then line, then policy class order. Multiset comparison must not depend on that order. If list order is compared, it must be reproduced with the same traversal.

## 5. Findings summary

| Item | Status |
|---|---|
| `120000` symlink blobs scanned as target text | Observed in gate; reconciler MUST match |
| `160000` gitlinks / submodules skipped silently | Observed; reconciler MUST match |
| Exec bit has no effect; no filters/textconv | Observed |
| Revision via stdin, `^{commit}` peel, non-full ids accepted | Observed; reconciler adds full-id check |
| Policy/allowlist read from filesystem, symlinks followed | Observed; reconciler reads blobs, rejects `120000` inputs (R21) |
| Replace refs honored by default | Documented by git; not present in repo (0 refs) |
| Inherited `GIT_*` env, lazy fetch | Unguarded in gate; not observed active |
| Non-UTF-8 path/line replacement collisions | Code-path fact; prevalence unmeasured |

Remaining unknowns: whether any of the 4 committed symlink targets contribute to the r21 raw-95 population. Whether any tracked path is non-UTF-8. Whether the r21 receipt's `policy_sha256` equals the committed policy blob at its measured revision. All three need L1 measurement after integration.
