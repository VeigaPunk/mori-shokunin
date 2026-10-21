# CodeSafePath: round-22 falsification of `safe_path` and its direct call contracts

Seat: MoriR22.CodeSafePath (leaf, read-only, static). No subagents, no production edits, no test, build, lint, or fixture execution, no background jobs, no peer messages.

## Scope and audited object

- Object: `tools/mori-retention-reconcile.py`, 17,354 bytes, sha256 `08dc3c5104ff891c1a2edbaa21aea84bd71acdadbd5f30d45c93558068126987`. Hash taken before and after the audit; unchanged. It equals `committed_sha256` for this path in `.ufo/waves/round-22/evidence/measure2/executing-input-bindings.json`.
- Older notes cite tool hash `d6870fb6…0ce7` and different line numbers (for example check at 155, committed at 81–86). Those describe an earlier version. Everything below was re-read against `08dc…`.
- Functions in scope: `safe_path` (49–51); its direct callers `committed` (84–89, calls `safe_path` at 85) and `check` (157–233, calls `safe_path` at 159 and 187); the helpers they pass the path into, `tree` (71–82) and `git` (53–60); and the exit mapping that turns path failures into codes, `Parser.error` (235–236) and `main` (268–282).
- Callers: a search of `tools/`, `round-22/frozen/`, `measure-round22.py`, `refinement-reconcile.py` and `oracle-reconcile-v2.py` shows no other caller of this file's `safe_path`. `measure-round22.py` runs the tool only as a subprocess, and reads it via `git show` (58–59).
- Correction applied: `denominator-correction.md`. Policy-excluded means non-author-glob identities. Not part of `safe_path`; the exclusion code (208–212) was read only as a neighbour of the path chain.
- Read-only references: `git.1` (lines 300, 1616–1625), `git-fsck.1` (289–292, 707–711), `git-ls-tree.1` (header: Git 2.56.0), Python 3.14 `argparse.py` (1272, 1956), `pathlib/__init__.py` (283–284, 563), and `tools/mori-retention-gate.py` (147, 164, 189–203, 241, 715–719).
- Installs or updates: none. Only `read`, `grep`, `glob` and one `sha256sum` checksum were used.

## Verdict

- `safe_path`'s predicate (line 50) enforces every rule in contract line 15 except that it does not reject U+0080–U+009F (F3).
- Four findings change accept or reject behaviour relative to the contract or the gate (F1–F4). Two are provenance or exit-code issues (F5, F6).
- No line in this chain converts a mismatch into `RECONCILED`. Every check is a `require` (reject) or an equality. The only way a verdict can name the wrong commit is F5 with a symbolic `--rev`, and `privacy_clearance` stays hard-coded false (230).
- Every input read is a Git object read. The only filesystem read in `check` is the tool's own bytes for `tool_sha256` (232).

## `safe_path` predicate (line 50), static trace

| Input | Result | Reason |
|---|---|---|
| non-`str` | rejected | `isinstance` is evaluated first and short-circuits |
| `''` | rejected | falsy |
| `/x`, `/` | rejected | `startswith('/')` |
| `.`, `./a`, `a/.`, `a/./b` | rejected | component `.` |
| `..`, `../x`, `a/../b` | rejected | component `..` |
| `a//b`, `a/`, `//` | rejected | empty component |
| NUL, LF, CR, TAB, other C0, DEL | rejected | `ord(c)<32 or ord(c)==127` |
| U+0080–U+009F | accepted (F3) | not in the predicate |
| `..x`, `.x`, `a..b`, `...` | accepted | not a reserved component |
| `-x`, `:x`, `:(glob)*`, `a\..\b`, leading space, `my receipt (final).json`, `データ.json` | accepted | single literal components. `--` (73) and `GIT_LITERAL_PATHSPECS` (55) keep git from reading them as options or magic |

The predicate cannot raise anything except `Invalid`, for any input type, because every method call is guarded by `isinstance` or runs on a `str`.

## Findings

### F1. A relative `--repo` in the receipt argv is refused (lines 180–181). Low–Medium, fail-closed

- Source: 180 `recorded_repo=recorded_option('--repo').rstrip('/')`; 181 `require(recorded_repo.startswith('/') and not any(ord(c)<32 for c in recorded_repo),'receipt_repo_binding')`.
- Counterexample (static trace). CLI: `check --repo /x/repo --rev R --receipt r.json --policy policy.json --allowlist allowlist.json`. Receipt `argv`: `["scan","--repo",".","--rev",M,"--policy","policy.json","--allowlist","allowlist.json"]`, all other bytes valid. Line 181 fails on `'.'`. `main` catches at 277 and returns exit 2 with `error=receipt_repo_binding`, before any hit is compared.
- The producer accepts the same argv. `mori-retention-gate.py:715` declares `--repo` as any string, and `:164` runs `git -C <repo>`, which accepts `.`.
- Not in the contract. Contract line 15 requires REPO_REL CLI inputs; line 11 says argv appears in the receipt. The absolute-repo rule is an implementation choice that was flagged as open by AttackR01 item 5 and AttackR02 A-6. It is still present at 181.
- Minimal option, if relative producers should be accepted: move the 181 requirement inside the `if recorded.startswith('/')` branch at 184. Relative recorded values already compare exactly at 187. An absolute recorded path under a relative repo then fails at 185, because `'/…'.startswith('./')` is false.
- Note: `GateRegistry.md` item 3 states that real r21 receipts use absolute `--repo`. That was not re-read in this lane.

### F2. Legacy file mode `100664` is refused as "not regular" (line 88). Low, fail-closed, reason code wrong

- Source: 88 `require(mode in (b'100644',b'100755') and kind==b'blob','input_not_regular')`.
- Counterexample (static). An input blob committed as `100664 blob <oid>\treceipt.json`, all else valid. Line 86 passes (one row, name equal). Line 88 rejects with `input_not_regular`.
- The file-type bits of `100664` are `100` (S_IFREG), so `input_not_regular` is a false reason for it. `git-fsck.1` lines 289–292 classify such an entry as `badFilemode` at INFO, not as an error. Contract line 15 requires rejecting symlinks, not this mode. [INFERENCE: the entry is a regular blob to Git's file-type test; not executed.]
- Prior notes: none. A search of `round-22/` finds no mention of `100664` or `badFilemode`.
- Option: accept `100664`, or accept any mode with S_IFREG and not 120000 or 160000. Or give non-canonical modes their own reason.

### F3. C1 control characters are accepted in paths (line 50). Low, definitional

- Source: 50 `not any(ord(c)<32 or ord(c)==127 for c in path)`.
- Counterexample (static). A committed input named `policy` + U+0085 + `.json` (bytes `70 6f 6c 69 63 79 C2 85 2e 6a 73 6f 6e`), passed as `--policy`. Line 50 accepts. Line 86 matches the tree name. Line 89 reads the blob.
- Contract line 15 says "controls". If that means Unicode category Cc, U+0080–U+009F are in it, and this is a violation. No output channel carries the name unescaped: `print(json.dumps(...))` at 281 uses the default `ensure_ascii`.
- Prior notes: AttackR20 F3 and FinalR20 (M2 / C1). Re-verified at 50 against `08dc…`.
- Option: add `or 0x80<=ord(c)<=0x9f` to line 50, if Cc is meant.

### F4. Every ls-tree row is decoded strictly, including gitlinks (lines 75–80). Low, fail-closed divergence from the gate

- Source: 75 `for row in git_out(repo,*args).split(b'\0')` runs over all rows. 79 `name=name.decode('utf8',errors='strict')`. 80 maps `UnicodeError` to `Invalid('invalid_tree_path')`. `scan` (143) calls `tree(repo,revision)`, and the kind filter (144) runs only after decoding.
- Gate: `mori-retention-gate.py:199–200` skips non-blob and gitlink entries before decoding. Line 202 decodes with `errors="replace"`.
- Counterexample (a). A tracked blob named `FF 2E 74 78 74` (`\xff.txt`). Tool exits 2 at 79–80 (`invalid_tree_path`). The gate records a hit under the path `\ufffd.txt`.
- Counterexample (b). A gitlink named `FF 73 75 62` (`\xffsub`, mode 160000). The tool exits 2 at 79–80, although `scan` would skip the entry at 144. The gate skips it at 199 and never decodes it. No hit is affected, so this is a pure divergence.
- Prior notes: FinalR04 and FinalR22 T3 cover (a) only. (b) is new.
- Caveat: `replace` would let distinct names collide. `normalize_hits` (128) would then raise `duplicate_receipt_hit` (154), exit 2. The strict choice is a defensible fail-closed design, but it should be an explicit decision.

### F5. `--repo` identity is not pinned: empty or nested paths bind to another repository (lines 158, 57). Low, provenance

- Source: 158 `repo=Path(a.repo); revision=resolve(repo,a.rev)`. `git()` (57) runs `git --no-replace-objects -C <repo>`. Nothing checks that `repo` is a repository top, and nothing rejects an empty `--repo`. Contract line 11 says `--rev` is "the exact committed input revision, resolved once". Lines 66–67 accept any selector that peels to a commit.
- Counterexample (a), static. `--repo ''`. `Path('')` is `.`: `pathlib/__init__.py` 283–284 returns no parts for an empty path, and 563 documents the empty path's string form as `'.'`. The repository containing the working directory is then evaluated.
- Counterexample (b), static. `--repo D`, where D is a directory without `.git`, lies inside repository R, and is on the same filesystem. `git -C D` discovers R (`git.1` 1624–1625).
- With a symbolic `--rev` such as `HEAD`, the input commit becomes R's HEAD, not D's.
- Impact. The receipt binds object IDs, so the verdict is a function of R's objects. The output records `input_revision` and `argv`, but not the repository used. A `RECONCILED` for R's HEAD can therefore be read as one for D's HEAD. This is attribution, not clearance (230).
- Prior notes: ReviewPath recommends rejecting an empty `--repo` and resolving it. Not implemented at 158.
- Option: reject an empty `--repo`. Require `git -C DIR rev-parse --show-toplevel` (or `--is-bare-repository`) to match the resolved DIR. Emit the resolved git directory in the output.

### F6. An uncaught exception in the check path exits 1, the MISMATCH code (lines 277–281, 233). Low, bounded

- Source: 277 `except Invalid`; 279 `except (OSError,UnicodeError,ValueError,TypeError,KeyError,RecursionError)`. Nothing else is caught.
- Reachable example (static). `scan` (147) reads a blob too large for memory. `MemoryError` is not caught. Python exits 1 with a traceback. Line 281 is not reached, so no JSON is printed. Exit 1 is the MISMATCH code (`int(bool(differences))` at 233), so a consumer keyed on exit status records a disagreement that did not happen.
- Within `safe_path`, `committed`, `tree` and the argv-binding code, I found no other uncaught exception class reachable for inputs that pass the validators (static reading).
- Prior notes: AttackR06 item 1 and AttackR17 (narrow `except` yields exit 1) describe the general case. This is the concrete catch list.
- Option: map any residual `Exception` to exit 2 with a fixed token.

## Bounded no-findings (static trace)

- B1 Ordering. `resolve` (158), then `safe_path` for all three inputs (159), then any Git read of an input (160). Receipt-recorded values pass `safe_path` at 187 before exact equality.
- B2 Git argument safety. `--` precedes the path (73). `--end-of-options` precedes the revision (67). `GIT_LITERAL_PATHSPECS=1` (55). `--no-replace-objects` (57). Every `GIT_*` variable is removed from the environment (54). `git.1` line 300: `--literal-pathspecs` means "no globbing, no pathspec magic", equivalent to `GIT_LITERAL_PATHSPECS=1`. So `:`-prefixed names are literal.
- B3 Identity. `committed` requires exactly one row whose decoded name equals the requested path (86). A directory, a prefix, a glob, or a magic-looking string cannot satisfy this unless it is the literal name. A duplicated name yields two rows and fails at 86.
- B4 Symlink and gitlink input. Mode 120000 fails at 88. A gitlink (kind `commit`) fails at 88. A path with a symlink parent returns no rows, because ls-tree does not descend into a blob, and fails at 86.
- B5 Revision pinning. The policy and allowlist bytes at the measured revision are read with the same mode-checked `committed` (169–170).
- B6 Receipt strings never reach Git unvalidated. The only receipt string passed to Git is `measured`, which must pass the OID regex at 164 before its uses at 165, 168, 170 and 200. The recorded `--policy` and `--allowlist` values never reach Git. A receipt therefore cannot cause `ValueError: embedded null byte` or `UnicodeEncodeError` in a subprocess call.
- B7 Traversal after prefix stripping. `/repo/../x` strips to `../x` (186) and is refused at 187. A stripped absolute path must equal an already-safe CLI path, so no new path is created.
- B8 Argparse errors. Subparsers are created with the tool's `Parser` class (`argparse.py` 1956 `type(self)`, 1272). `Parser.error` (236) raises `Invalid('usage')`. No argparse text reaches stderr for `check`.
- B9 Duplicate names in `scan`. `scan` enumerates rows as the gate does (143–153; gate 189–203). Duplicates behave identically except byte-identical duplicates, where `normalize_hits` (154) raises `duplicate_receipt_hit`, exit 2. That divergence fails closed.
- B10 Allocation. `safe_path` is linear in path length and is called ten times per invocation at most. `committed` runs two Git processes and is called five times per invocation. Not material. `scan` spawns one `cat-file` per unique blob (147), which matches the gate (201). That is outside this lane.
- B11 Allowlist and must-redact strings are data, not REPO_REL inputs. They are compared by equality (205), as the gate does (`gate:241`). The gate checks only non-emptiness (`gate:147`). No divergence.
- B12 Over-rejection guard. Names with spaces, parentheses or non-ASCII (`my receipt (final).json`, `データ.json`) pass line 50 and reach the exact-name match at 86 (static).

## Prior-note reconciliation

- AttackR01 item 5 → F1: confirmed at 181 against `08dc…`.
- AttackR20 F3 and FinalR20 (M2 / C1) → F3: confirmed at 50. FinalR20's check and committed line numbers and its tool hash are stale.
- FinalR04 and FinalR22 T3 → F4: confirmed for blob names. The gitlink case (b) is new.
- ReviewPath (reject empty `--repo`; resolve it) → F5: confirmed absent at 158.
- AttackR06 item 1 and AttackR17 → F6: confirmed; the catch list is 279–280.
- FixtureSymlink C1 (mode-blind mutant) → the mode gate exists at 88 in the shipping file. The mutant is not in the shipping file.

## Outside this lane (not audited further)

- Line 167 comment says exit 1 is a "distinct finding". Line 168 maps that case to the same SETUP reason, `measured_not_ancestor`, as any other failure.
- Line 232 hashes the tool file when the result is built, not the bytes that were loaded at startup. A mid-run edit would make `tool_sha256` disagree with the code that ran.

## Checks for L1 after integration (not run by me)

1. Same-command arm for F1 with argv `--repo .`. Expect exit 2 `receipt_repo_binding` on the current tool, and exit 0 if relative producers are accepted after the correction.
2. F2: a `100664` input arm. Expect the chosen behaviour, with a distinct reason if still rejected.
3. F4: a non-UTF-8 blob arm and a non-UTF-8 gitlink arm. Expect exit 2 `invalid_tree_path` for both under the strict choice; expect the gitlink arm to pass if gitlinks are skipped before decoding.
4. F5: `--repo ''`, and a non-repository directory inside a repository. Expect exit 2 after the correction.
5. F6: a mutant that raises `MemoryError` inside `scan`. Expect exit 2 with JSON on stdout after the correction.

## Verification gaps

- Static trace only. Each counterexample is derived from the code and the cited documentation. None was executed. Labelled [INFERENCE] where Git's behaviour is inferred rather than documented.
- The real r21 receipt's argv was not re-read. The producer shape was taken from the gate's CLI (715–719) and from prior notes.
- Git documentation is the locally shipped man pages (ls-tree page header: Git 2.56.0). The behaviour of the Git binary on this host was not probed.
