# CodeSafePath: round-22 falsification of `safe_path` and its direct call contracts

Seat: MoriR22.CodeSafePath (leaf, read-only, static). No subagents, no production edits, no test, build, lint or fixture execution, no background jobs, no peer messages, no session or private-config reads.

## Audited object (pinned)

- `tools/mori-retention-reconcile.py`: 18,226 bytes, sha256 `0795bac9367c33e534b79599114c1635d83c4b0e4a57fbbe235644858a59de32`, mtime 2026-10-21 12:27:36 -0300. Digest re-checked at the start of the final pass and again just before this report was written; stable.
- The file changed during this audit. My first pass saw sha256 `08dc3c5104ff891c1a2edbaa21aea84bd71acdadbd5f30d45c93558068126987` (17,354 bytes). That version is superseded. Its findings were re-derived against `0795…`. Two no longer reproduce (R1, R2), one shifted, and one is new (F5).
- `tools/mori-retention-gate.py`: sha256 `cf0896a2ea36f169c9e900c58eefe7e2a900a4c9d67f849f753f4631d8ab829e`, unchanged.
- In scope: `safe_path` (51–53); its direct caller `committed` (86–91), which calls `safe_path` at 87 and `tree` (73–84); `check` (159–241), path handling at 160–166 and 183–194; the process boundary `git` (55–62); and the exit mapping at `Parser.error` (243–244) and `main` (276–296).
- Callers: a search of `tools/`, `round-22/frozen/`, `measure-round22.py`, `refinement-reconcile.py` and `oracle-reconcile-v2.py` finds no caller of this file's `safe_path` other than `committed` (87) and `check` (166, 194). `measure-round22.py` runs the tool only as a subprocess, and reads it via `git show` (58–59).
- Correction applied: `denominator-correction.md`. Policy-excluded means non-author-glob identities. That is not part of `safe_path`; the partition (`excluded` 216, `scanner` 217) was read only as a neighbour.
- Read-only references: `git.1` (300, 1616–1625), `git-fsck.1` (289–292, 707–711), `git-rev-parse.1` (374: `--show-toplevel` "If there is no working tree, report an error"), `git-ls-tree.1` header (Git 2.56.0), Python 3.14 `argparse.py` (1272, 1956), `pathlib/__init__.py` (283–284, 563), and `mori-retention-gate.py` (147, 164, 189–203, 241, 715–719).
- Installs or updates: none. Tools used: `read`, `grep`, `glob`, and `bash` for `sha256sum` and `stat` only.

## Verdict

- The `safe_path` predicate (line 52) enforces every path rule in contract line 15 except that it does not reject U+0080–U+009F (F3).
- Four findings change accept or reject behaviour relative to the contract or the gate: F1 (recorded relative `--repo` refused, 188), F2 (mode 100664 refused, 90), F3 (C1 accepted, 52), F4 (strict decoding of every tree row, 81–82).
- F5 is new in `0795…`: the CLI now requires an absolute `--repo` (160), which refuses the command shape documented in `ConnectKagi.md:63`.
- Two earlier findings are resolved in `0795…`: empty, relative or nested `--repo` aliasing (R1, lines 160–164), and `MemoryError` escaping as exit 1 (R2, lines 288–289).
- No line in this chain converts a mismatch into `RECONCILED`. Every check is a `require` (reject) or an equality. `privacy_clearance` is hard-coded false (238).
- Every input read is a Git object read. The only filesystem read in `check` is the tool's own bytes for `tool_sha256` (240).

## `safe_path` predicate (line 52), static trace

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
| `-x`, `:x`, `:(glob)*`, `a\..\b`, leading space, `my receipt (final).json`, `データ.json` | accepted | single literal components. `--` (75) and `GIT_LITERAL_PATHSPECS` (57) keep git from reading them as options or magic |

The predicate cannot raise anything other than `Invalid`, for any input type, because each method call is guarded by `isinstance` or runs on a `str`.

## Findings (current source, `0795…`)

### F1. A relative `--repo` in the receipt argv is refused (line 188). Low to medium, fail-closed

- Source: 187 `recorded_repo=recorded_option('--repo').rstrip('/')`; 188 `require(recorded_repo.startswith('/') and not any(ord(c)<32 for c in recorded_repo),'receipt_repo_binding')`.
- Counterexample (static trace). CLI: `check --repo /x/repo --rev R --receipt r.json --policy policy.json --allowlist allowlist.json`. Receipt `argv`: `["scan","--repo",".","--rev",M,"--policy","policy.json","--allowlist","allowlist.json"]`, with all other bytes valid. Line 188 fails on `'.'`. `main` catches at 286 and returns exit 2 with `error=receipt_repo_binding`, before any hit is compared.
- The producer accepts the same argv. `mori-retention-gate.py:715` declares `--repo` as any string, and `:164` runs `git -C <repo>`, which accepts `.`.
- Not in the contract. Line 11 says argv "appear[s] in receipt"; line 15 fixes REPO_REL inputs. The absolute-repo rule was already flagged as open by AttackR01 item 5 and AttackR02 A-6. It is still present at 188.
- Option: move line 188 inside the branch at 191 (`if recorded.startswith('/')`). Relative recorded values then compare exactly at 194. An absolute recorded path under a relative repo fails at 192, because `'/…'.startswith('./')` is false.
- `GateRegistry.md` item 3 says receipt argv uses absolute lane paths. That was not re-read in this lane.

### F2. Legacy file mode `100664` is refused as "not regular" (line 90). Low, fail-closed, reason code wrong

- Source: 90 `require(mode in (b'100644',b'100755') and kind==b'blob','input_not_regular')`.
- Counterexample (static). An input blob committed as `100664 blob <oid>\treceipt.json`, with all else valid. Line 88 passes (one row, name equal). Line 90 rejects with `input_not_regular`.
- The file-type bits of `100664` are `100` (S_IFREG), so `input_not_regular` is a false reason for it. `git-fsck.1` lines 289–292 classify `badFilemode` as INFO, not as an error. Contract line 15 requires rejecting symlinks, not this mode. [INFERENCE: the entry is a regular blob under Git's file-type test; not executed.]
- Prior notes: none mention 100664.
- Option: accept `100664`, or any S_IFREG mode other than 120000 and 160000. Alternatively give non-canonical modes a distinct reason.

### F3. C1 control characters are accepted in paths (line 52). Low, definitional

- Source: 52 `not any(ord(c)<32 or ord(c)==127 for c in path)`.
- Counterexample (static). A committed input named `policy` + U+0085 + `.json` (bytes `70 6f 6c 69 63 79 C2 85 2e 6a 73 6f 6e`), passed as `--policy`. Line 52 accepts. Line 88 matches the tree name. Line 91 reads the blob.
- Contract line 15 says "controls". If that means Unicode category Cc, U+0080–U+009F are in it and this is a violation. No output channel carries the name unescaped: `print(json.dumps(...))` (291) uses the default `ensure_ascii`.
- Prior notes: AttackR20 F3; FinalR20 (M2 / C1). Re-verified at 52.
- Option: add `or 0x80<=ord(c)<=0x9f` at 52, if Cc is meant.

### F4. Every ls-tree row is decoded strictly, gitlinks included (lines 77–82). Low, fail-closed divergence from the gate

- Source: 77 loops over all rows; 81 `name=name.decode('utf8',errors='strict')`; 82 maps `UnicodeError` to `Invalid('invalid_tree_path')`. `scan` (145) calls `tree(repo,revision)`. Its kind filter (146) runs after decoding.
- Gate: `mori-retention-gate.py:199–200` skips non-blob and gitlink entries before decoding. Line 202 decodes with `errors="replace"`.
- Counterexample (a). A tracked blob named bytes `FF 2E 74 78 74` (`\xff.txt`). The tool exits 2 at 81–82. The gate records a hit under the path `\ufffd.txt`.
- Counterexample (b). A gitlink named `FF 73 75 62` (`\xffsub`, mode 160000). The tool exits 2 at 81–82, although `scan` would skip the entry at 146. The gate skips it at 199 and never decodes it. This is a pure divergence; no hit is affected.
- Prior notes: FinalR04 and FinalR22 T3 cover the blob case (a). Case (b) is new.
- Caveat: `replace` would let distinct names collide. `normalize_hits` (130) would then raise `duplicate_receipt_hit` (156), exit 2. Strict decoding is a defensible fail-closed choice, but it should be an explicit decision.

### F5. An absolute-only `--repo` refuses the documented command shape (line 160). Low, compatibility. New in `0795…`

- Source: 160 `require(isinstance(a.repo,str) and a.repo.startswith('/') and not any(ord(c)<32 for c in a.repo),'repo_not_absolute')`.
- Counterexample (static). `check --repo . --rev <R> --receipt … --policy … --allowlist …`, the form shown in `.ufo/waves/round-22/build/ConnectKagi.md:63` under "Expected result". Exit 2 with `repo_not_absolute`, before any Git read.
- Contract line 11 says `--repo DIR`, not absolute. Lines 163–164 already compare `realpath` of the top-level directory with `realpath(a.repo)`, so a relative path can be normalised without the absolute rule.
- Option: normalise with `os.path.realpath(a.repo)` before line 161 and keep 163–164. Or update `ConnectKagi.md` and `GateRegistry.md` to absolute examples.

## Resolved in `0795…` (findings in `08dc…`)

- R1. `--repo` aliasing. Earlier: `Path('')` is `.` (`pathlib/__init__.py` 283–284, 563), and a directory without `.git` bound to an enclosing repository (`git.1` 1624–1625). Now: line 160 refuses empty and relative paths. Lines 163–164 require `git rev-parse --show-toplevel` to resolve to the same real path as `a.repo`. A non-repository directory fails at 163 (non-zero exit). A nested directory fails at 164. Residual: bare repositories are now refused. `git-rev-parse.1` 374 says that without a working tree the command reports an error, so `git()` raises `git_read_failed` (exit 2). This is not in the contract and is fail-closed. The `--repo ''` counterexample in CodeMain.md no longer reproduces.
- R2. `MemoryError` as exit 1. Now line 288 catches `MemoryError`, and 289 returns exit 2 with `input_unavailable`. Other classes (AttributeError, IndexError, RuntimeError) still escape to exit 1. I found no path from this lane's functions that raises them for inputs that pass the validators (static reading).

## Bounded no-findings (static trace, current source)

- B1 Ordering. `--repo` checks (160–164), then `resolve` (165), then `safe_path` (166), then input reads (167). Receipt-recorded values pass `safe_path` at 194 before exact equality.
- B2 Git argument safety. `--end-of-options` before the revision (69). `--` before the path (75). `GIT_LITERAL_PATHSPECS=1` (57). `--no-replace-objects` (59). Every `GIT_*` variable is removed from the environment (56). `git.1` line 300: `--literal-pathspecs` means "no globbing, no pathspec magic", equal to the environment variable. So `:`-prefixed names are literal.
- B3 Identity. `committed` requires exactly one row whose decoded name equals the requested path (88). A directory, a prefix or a glob cannot satisfy this.
- B4 Symlink and gitlink input. Mode 120000 and kind `commit` both fail at 90. A path with a symlink parent returns no rows, because ls-tree does not descend into a blob, and fails at 88.
- B5 Measured-revision bytes. The policy and allowlist are re-read with the same mode-checked `committed` at the measured revision (176–177).
- B6 Receipt strings never reach Git unvalidated. The only receipt string passed to Git is `measured`. It must pass the OID regex at 171 before its uses at 172, 175, 177 and 207. The recorded `--policy` and `--allowlist` values never reach Git, so a receipt cannot cause `ValueError: embedded null byte` or `UnicodeEncodeError` in a subprocess call.
- B7 Traversal after prefix stripping. `/repo/../x` strips to `../x` (193) and is refused at 194. A stripped path must still equal an already-safe CLI path.
- B8 Argparse errors. Subparsers are instances of the tool's `Parser` (`argparse.py` 1956 `type(self)`, 1272). `Parser.error` (244) raises `Invalid('usage')`. No argparse text reaches stderr for `check`.
- B9 Duplicate names in `scan`. `scan` enumerates rows as the gate does (145–155; gate 189–203). Only byte-identical duplicates diverge: `normalize_hits` (156 → 130) raises `duplicate_receipt_hit`, exit 2. That divergence fails closed.
- B10 Allocation. `safe_path` is linear in path length and runs at most ten times per invocation. `committed` runs five times per invocation, with two Git processes each. Not material. `scan` spawns one `cat-file` per unique blob (149), matching the gate (201). That is outside this lane.
- B11 Allowlist and must-redact strings are data, not REPO_REL inputs. They are compared by equality (212), as the gate does (`gate:241`). The gate checks only non-emptiness (`gate:147`). No divergence.
- B12 Over-rejection guard. Names with spaces, parentheses or non-ASCII (`my receipt (final).json`, `データ.json`) pass line 52 and reach the exact-name match at 88 (static).
- B13 The new `--repo` checks read no input path. They run `rev-parse --show-toplevel` on `a.repo` only, and their failures are fixed tokens.

## Prior-note reconciliation

- AttackR01 item 5 → F1: still present at 188.
- AttackR20 F3; FinalR20 (M2 / C1) → F3: still present at 52.
- FinalR04; FinalR22 T3 → F4: still present at 81–82. Case (b), gitlinks, is new.
- ReviewPath; CodeMain (`--repo ''`) → R1: resolved at 160–164.
- AttackR06 item 1; AttackR17 → R2: resolved at 288–289.
- FixtureSymlink C1 (mode-blind mutant) → the shipping file has the mode gate at 90. The mutant is not shipped.
- Stale: FinalR20's tool hash `d6870fb6…0ce7` and its check and committed line numbers describe an earlier version.

## Outside this lane (not audited further)

- Line 174: the comment says exit 1 is a "distinct finding". Line 175 maps that case to the same SETUP reason, `measured_not_ancestor`, as any other failure.
- Line 240: `tool_sha256` hashes the file when the result is built, not the bytes loaded at startup. A mid-run edit would make the recorded hash disagree with the code that ran.
- Lines 234–235: `raw_unallowlisted` (234) still equals `scanner_unallowlisted` (`len(unallowed)`). The new `raw_not_allowlisted` (235) is the identity-based raw count, so the two are now distinct fields. This addresses the alias note in FixtureForbidden and FinalR04.
- Line 281: `argv` in the output is now the argv actually passed (`argv_seen`).

## Checks for L1 after integration (not run by me)

1. F1: a same-command arm with argv `--repo .`. Expect exit 2 `receipt_repo_binding` on the current source, and exit 0 if relative recorded repos are accepted after the correction.
2. F2: a `100664` input arm, with the chosen behaviour pinned.
3. F4: a non-UTF-8 blob arm and a non-UTF-8 gitlink arm. Expect exit 2 `invalid_tree_path` for both under the strict choice. Expect the gitlink arm to pass if gitlinks are skipped before decoding.
4. F5: a `check --repo .` arm. Expect `repo_not_absolute` now, and exit 0 after normalisation.
5. R2: inject `MemoryError` into `scan`. Expect exit 2 with JSON on stdout.

## Verification gaps

- Static trace only. Every counterexample is derived from the code and the cited documentation, and none was executed. [INFERENCE] marks Git behaviour that was inferred rather than documented.
- The shipping tool changed during the audit (`08dc…` → `0795…`). This report is pinned to `0795…`. If the file changes again, the line numbers above must be re-read.
- The real r21 receipt's argv was not re-read. The producer shape comes from the gate CLI (715–719) and from prior notes.
- Git documentation is the locally installed man pages. The Git binary's behaviour on this host was not probed.
