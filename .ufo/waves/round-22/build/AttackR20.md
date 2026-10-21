# AttackR20 — frozen requirement R20 ("unsafe input path returns2")

Seat: MoriR22.AttackR20 (critic, static review only). No tests, builds, or fixtures were run. No tools were installed. Every claim below comes from a file read or a read-only `git -C` plumbing read; anything not observed is marked [INFERENCE].

## Contract text under attack

- R20: "unsafe input path returns2".
- Body clause: "Safe repo-relative paths: no absolute, dotdot, empty, controls; committed symlink input is rejected." The symlink half is R21's; R20 owns the lexical rule.
- Scope: the three `REPO_REL` arguments `--receipt`, `--policy`, `--allowlist`. `--repo` is `DIR` (absolute permitted, required for `--selftest`); `--rev` is `COMMIT` (R13/R18 territory). `Path`s recorded inside the receipt `argv` are also inputs the tool acts on.

## State observed

- Candidate exists: `tools/mori-retention-reconcile.py` (274 lines). Its lexical gate is `safe_path` at lines 49–51: requires non-empty `str`, rejects a leading `/`, rejects any `/`-split component in `{'', '.', '..'}`, and rejects any char with `ord(c) < 32` or `== 127`. It is applied to all three path args at line 156 before any `ls-tree`, and to the receipt-recorded `--policy`/`--allowlist` values at line 182. Blob reads go through `ls-tree -r -z --full-tree <rev> -- <path>` under `GIT_LITERAL_PATHSPECS=1` (lines 55, 68–86), with an exact one-row name match and mode ∈ {100644, 100755}.
- Oracle arm: `.ufo/waves/round-22/oracle-reconcile.py:57` — `record('R20', receipt_override='../receipt.json', code=2, finding='RETENTION_RECONCILIATION_SETUP')`. One arm, one argument, one unsafe class. `record()` also requires parseable JSON on stdout and `cp.stderr == ''` (line 42). It does not check the `error` string or the absence of metric keys.
- Impl selftest arm: line 252 — `base[:-1]+['../allow.json']`, again only `../` and only one argument.
- Fixture builder (`frozen/fixture-builder.py`) has no unsafe-path variant; `receipt_override` only substitutes the argv string. The repo root for that run is `…-fixtures/valid-unsafe`, so `../receipt.json` names `…-fixtures/receipt.json`, which exists neither in the tree nor in the worktree.

## Why R20 can pass superficially

1. **The frozen arm is satisfied by having no path validator at all.** Git trees can never contain `..` or `.` components, so `ls-tree <rev> -- ../receipt.json` returns zero rows for any correct implementation. A SUT that performs zero lexical checks fails closed as `missing_input_blob` → exit 2, `RETENTION_RECONCILIATION_SETUP`, empty stderr, valid JSON — a full pass with `unsafe_input_path` never implemented. The oracle cannot distinguish "rejected because unsafe" from "rejected because absent". This is the central superficial-pass risk: the only arm cannot detect the absence of the feature under test.
2. **A worktree-opening SUT also passes the arm.** `open(<repo>/../receipt.json)` raises `FileNotFoundError` for this fixture; any SUT that sanitizes `OSError` still exits 2 with SETUP. The contract's "read via Git blobs, not worktree" is unexercised by this arm because the path happens not to exist on disk either.
3. **Only one of three arguments is exercised.** A SUT validating only `--receipt` (or only the first arg parsed) passes while leaving `--policy` and `--allowlist` unchecked — a real hole, because all three reach `ls-tree`/blob reads.
4. **Only one unsafe class is exercised.** Absolute paths, embedded/normalizable `..`, `.` components, empty components (`a//b`, `a/`), empty string, and control bytes are all unarmed. A validator implementing only `path.startswith('..')` or only `'..' in path` passes.
5. **No error-code or payload assertion.** All setup failures share `RETENTION_RECONCILIATION_SETUP`. The oracle does not assert a distinct sanitized code (e.g. `unsafe_input_path` vs `missing_input_blob`), nor that no metric keys (`raw_total`, `raw_hits`, …) were emitted before the rejection.

## Counterexample fixtures (decisive arms)

Each arm is the R01-valid synthetic fixture (exit 0 `RETENTION_RECONCILED`) with exactly one argv element changed, unless stated. Expected for every unsafe arm: exit 2, `finding_id == RETENTION_RECONCILIATION_SETUP`, the frozen unsafe-path error code (see criterion), `privacy_clearance is False`, `receipt_match is False`, **no metric keys** (`raw_total`, `raw_hits`, `scanner_hits`, `policy_excluded`, `inputs_sha256` all absent), stderr empty.

**F1. Dotdot that resolves to a real sibling receipt on the worktree (kills worktree readers).**
- Setup: run the oracle's `valid` fixture first (it already exists under `…-fixtures/valid` with deterministic commit SHAs — the builder pins author/committer/dates, so `valid-unsafe` commits are identical). Invoke with `--repo …-fixtures/valid-unsafe --rev <rev> --receipt ../valid/receipt.json`.
- `…-fixtures/valid/receipt.json` exists on disk and is a byte-valid receipt whose `measured_revision` matches this repo's deterministic SHAs.
- Expected: exit 2, unsafe-path code.
- A blob-only SUT passes trivially (no such tree path). A worktree SUT without `safe_path` opens the sibling receipt and, lacking argv-binding checks, can reach exit 0 — decisive failure mode made observable. A worktree SUT with a `resolve()`-then-containment check also reads it (the path stays inside `…-fixtures`, though outside `--repo`) — see ambiguity A1.

**F2. Absolute path to the committed receipt's worktree copy (kills FS fallback and root-strip).**
- Invoke with `--receipt /absolute/path/to/<repo>/receipt.json` (the real file on disk).
- Expected: exit 2, unsafe-path code, no metrics.
- A SUT that strips a leading `/` and treats the rest as repo-relative reads the real blob and returns 0. A worktree SUT opens the file. Both are caught; the frozen arm catches neither.

**F3. Committed control-character filename (kills missing-control-check).**
- Setup: commit a valid allowlist under the name `a\tb.json` (literal TAB; git permits it), and a variant with `\x7f` and `\x85` (NEL, a Unicode `Cc` control not covered by `ord<32 or ==127`).
- Invoke `--allowlist 'a\tb.json'` (and each variant).
- Expected: exit 2, unsafe-path code — never 0.
- A SUT with no control check resolves the blob and reconciles → exit 0, caught. The `\x85` variant pins what "controls" means (see A2).

**F4. Embedded normalizable dotdot: `sub/../receipt.json`.**
- `sub/` is any committed directory; the requested path contains a `..` component but normalizes to `receipt.json`, a real committed blob.
- Expected: exit 2 under the literal reading of "no dotdot" (see A1 — this arm is decisive only once L1 pins the interpretation).
- A SUT that validates `normpath(path)` containment accepts it and returns 0/1 — caught. A lexical SUT rejects → 2. This is the arm that separates "reject `..` components" from "reject escaping paths".

**F5. Per-argument sweep.** Repeat F4's value class and `../x` independently on `--policy` and `--allowlist`. Expected: 2/SETUP/unsafe code on each. This is the arm that proves the validator covers all three REPO_REL parameters, not just the one the oracle mutates.

**F6. Pathspec-magic and dash-prefixed values.**
- `--receipt ':(icase)RECEIPT.JSON'`, `--receipt ':(glob)*.json'`, `--receipt '-x'`.
- Expected: 2 each (unsafe or missing-input code — pin which; see A5). A SUT that passes the arg without `--` or without `GIT_LITERAL_PATHSPECS` can resolve `:(icase)` to a real blob and return 0/1 — caught. The impl covers this via env + `--` + exact-name match; the contract freezes neither, so the arm must exist to keep it covered.

**F7. Receipt-embedded recorded path (JSON-carried unsafe value).**
- Mutate the committed receipt wrapper so `argv` records `--policy 'bad\tname.json'` or `--policy 'sub/../policy.json'`, while the CLI passes the safe committed `policy.json`. Keep everything else valid.
- Expected: exit 2 (binding or unsafe code — pin). This exercises the *only* channel through which a NUL or control byte can reach a path the tool acts on (argv cannot carry NUL; JSON strings can). Include one recorded `bad\x00name.json` arm: a SUT passing it to subprocess gets `ValueError: embedded null byte` — must still be exit 2 SETUP, never a traceback.

**F8. Over-rejection guard (must NOT exit 2).**
- Commit a valid input under a legal-but-unusual name: `my receipt (final).json` (spaces, parens) and `データ.json` (non-ASCII, NFC). Use it as `--receipt` in an otherwise valid run.
- Expected: the ordinary verdict (0 `RETENTION_RECONCILED` or 1 `MISMATCH`), never a path-rejection 2. Guards against validators that regex `^[A-Za-z0-9_./-]+$` or reject non-ASCII — a real failure class the unsafe-arms-only oracle cannot see.

**F9. Empty and boundary values.** `--policy ''`, `--policy .`, `--policy a/`, `--policy a//b`, `--policy //`, `--policy ' '` (single space). Expected: 2 each. `''` and `a//b`/`a/` carry empty components; `.`/` ` depend on A1/A3 pinning — assert them only after L1 decides, but freeze the decision either way.

## Exact actionable criterion for R20

An implementation satisfies R20 iff all of the following hold:

1. **Lexical validation precedes any use.** Every `REPO_REL` argv value (`--receipt`, `--policy`, `--allowlist`) and every path value acted upon from the receipt `argv` is checked before it reaches `ls-tree`, `cat-file`, `open()`, or `pathlib` operations. Validation order vs. `--rev` resolution may differ, but the unsafe path must never reach a read primitive (see A4).
2. **The lexical rule is frozen as:** reject unless the value is a non-empty `str` with no leading `/`, no component in `{'', '.', '..'}` when split on `/`, and no character in Cc (`ord<32`, `==127`, plus C1 `0x80–0x9f` pending A2). Rejection is independent of whether the name could resolve — it fires on the string, not the tree.
3. **Observable contract per unsafe arm:** exit 2; stdout is a single JSON object containing `finding_id == 'RETENTION_RECONCILIATION_SETUP'`, a dedicated sanitized `error` code frozen by L1 (the impl's `unsafe_input_path` is an acceptable freeze target — distinct from `missing_input_blob` so arms can tell cause), `privacy_clearance: false`, `receipt_match: false`; containing no recomputation fields (`raw_total`, `raw_hits`, `scanner_hits`, `policy_excluded`, `non_author`, `inputs_sha256`, `measured_revision`, `argv`); stderr byte-empty. Requiring the dedicated code is what makes F1–F4 distinguish a real validator from missing-blob fallback.
4. **Arguments are forwarded safely:** literal pathspecs (env or `:(literal)`/`--literal-pathspecs`), `--` separator before the path, no `--follow-symlinks`, exact one-row name equality on the returned record.
5. **Selftest/oracle must add arms F1–F7 and the F8 over-rejection arm.** An R20 selftest asserting only `../x` on one argument is a superficial pass — it is satisfied by a build with no validator at all.

## Semantic ambiguities L1 must pin

- **A1: component-level vs. resolved-path dotdot.** "No dotdot" reads literally (reject any `..` component → `sub/../receipt.json` is 2). A resolve-then-contain validator calls it safe (it lands on `receipt.json` → 0/1). The impl chose literal rejection — recommend freezing that, since git can never store `..` components and the literal rule is the only reading under which F4 is decisive. Same question for `.` components (`./receipt.json`): impl rejects, contract is silent.
- **A2: "controls" definition.** Impl rejects C0 + DEL but accepts C1 (`0x80–0x9f`, e.g. NEL) and `Cf`/`Zl`/`Zp` (BOM, U+2028/29). If the contract means Unicode `Cc`, the impl under-rejects; if it means ASCII control bytes, it conforms. F3's `\x85` arm exists to force the decision into an observable.
- **A3: whitespace-only and backslash.** `' '` passes the impl's lexical gate (then fails as missing blob → still 2, different code). `..\receipt.json` is a legal POSIX filename — impl accepts lexically, misses → 2. Contract is silent on both; freeze whether they are unsafe-path or missing-blob cases so the error code is deterministic.
- **A4: ordering vs. `--rev`.** Impl resolves the revision before `safe_path`, so `bad-rev + unsafe-path` reports `invalid_revision` rather than `unsafe_input_path` — both exit 2, but if arms assert the error code, validation order becomes observable. Freeze an order (paths-first is simpler to reason about) or declare either acceptable.
- **A5: unsafe vs. missing code granularity.** `../receipt.json` is both unsafe and absent. If the contract intends one bucket, the dedicated-code requirement in the criterion is optional and the superficial-pass risk stands. Recommend freezing `unsafe_input_path` for lexical rejections and `missing_input_blob` for safe-but-absent — that single distinction is what makes R20 non-trivially checkable.
- **A6: scope boundary.** `--repo` is a `DIR` argument and must stay outside R20 (absolute/`..`-containing repo paths are legitimate). `--rev` lexical rules belong to R13. Do not let an R20 fix creep into rejecting `--repo` strings.

## Cross-requirement observation (outside R20; for L1)

- Impl decodes tree path bytes with `errors='strict'` (line 76) and raises `invalid_tree_path` for the whole run; the existing gate decodes `errors='replace'` (gate line 202) and counts such hits. A repo containing any non-UTF-8 filename anywhere therefore flips the tool to exit 2 while the gate would still produce a population — a divergence in scan semantics worth a QualityDenom/CriticPopulation look; not an R20 defect.
- The impl's `safe_path` also guards receipt-recorded argv paths (line 182), which is the correct extra — that is the only channel that can smuggle NUL/controls into an acted-upon path. No arm currently exercises it (F7).

## Impacted axes

Calibration (C1): as shipped, the frozen R20 arm passes with zero path validation implemented, so a superficial pass directly inflates the claimed requirement count the wave exists to measure. Correctness: F1/F2 are the only arms that separate blob-only reads from worktree reads — the contract's core input-integrity guarantee. Fail-closed behavior: F6/F7 pin argument separation and JSON-carried hostile paths.

## Smallest safe correction

1. Freeze the lexical rule and one dedicated sanitized code (`unsafe_input_path`) for lexical rejections; keep `missing_input_blob` distinct.
2. In `oracle-reconcile.py`, extend the R20 record into the F1–F7 arm matrix (each asserting exit 2 + SETUP + frozen code + no metric keys + empty stderr) and one F8 must-accept arm.
3. In the impl selftest, replace the single `../allow.json` arm with the same matrix.
4. No change needed to `safe_path` itself unless A2 (C1 controls) or A1 (`.`) is pinned differently; its current literal rule already covers F1–F6 for a blob-only reader.
