# ReviewPath — Git argument safety, repo-relative inputs, special pathnames, symlink input semantics

Seat: MoriR22.ReviewPath (reviewer, read-only). Scope: `contract.md`, `frozen/fixture-builder{,-v2}.py`, `frozen/requirements{,-v2}.json`, `oracle-reconcile{,-v2}.py`, `denominator-correction.md`, `tools/mori-retention-gate.py` (git plumbing only), sibling reports `GateGit.md`, `ReceiptBinding.md`, `RequirementTrace.md`, `expected-real.json`. Verification: read-only `git` plumbing against the lane repo (git 2.56.0, sha1 repo, not shallow, no replace refs — per GateGit). No SUT candidate exists yet (`build/ImplReconcile/` and `.scratch/round22/` are absent), so every control below is spec-level for the pending implementation; no measurements claimed. No tools installed. No matched text emitted.

## Findings by severity

### F1 HIGH — R21 fixture makes the symlink-mode check unobservable

`frozen/fixture-builder-v2.py:94` creates `--receipt` as `symlink_to('allowed.txt')`. The committed 120000 blob's content is the link text `allowed.txt`, which is not JSON. A SUT that skips `ls-tree` mode inspection entirely — reads `cat-file blob <rev>:receipt.json`, gets the link text, fails JSON parsing — still exits 2 and passes R21 **for the wrong reason** (malformed input, not symlink rejection). The mode check the contract actually requires is exercised only if the link text parses as a valid receipt.

Control: re-arm the fixture with a symlink whose target text is valid receipt JSON (dangling link; link text need not name a real file), and/or add oracle assertions that distinguish `unsafe_input_symlink` from `malformed_json`. Also add symlink arms for `--policy` and `--allowlist` (currently untested). Reviewer: recommend only; fixture/oracle edits belong to L1.

### F2 HIGH — Oracle path-safety coverage: one unsafe arm on one argument

`oracle-reconcile-v2.py:57` tests R20 only via `receipt_override='../receipt.json'` on `--receipt`. Untested: `--policy`/`--allowlist` with `..`; absolute paths (`/…`), empty strings, control characters on all three REPO_REL args; interior `a/../b`; `.` components; and hostile `--rev`/`measured_revision` strings (leading `-`, embedded NUL). A validator covering only `..` on `--receipt` passes the oracle (RequirementTrace gap 7 agrees). Control: per-argument × per-bad-class arms; a single shared lexical validator (grammar in §Controls) is the boring design that makes the untested matrix safe by construction.

### F3 HIGH — `rev:path` dot-component resolution is filesystem-normalized and `-C`-dependent — never delegate normalization to git

Observed on git 2.56.0 against this repo (read-only):

- `cat-file -t HEAD:./tools/mori-retention-gate.py` → `blob` (`.` resolves)
- `cat-file -t HEAD:./` → `tree`; `HEAD:.` → error (inconsistent)
- `git -C tools cat-file -t HEAD:../contract.md` → resolves relative to **repo root**, not the `-C` dir
- `cat-file -t HEAD:../x` from repo root → `fatal: '../x' is outside repository`
- `HEAD:.ufo/../contract.md` → `fatal: does not exist` (interior `..` not normalized at root)

Meaning: `.`/`..` handling is inconsistent, position-dependent, and can alias paths inside the tree. Control: reject any `/`-split component equal to `.` or `..` lexically, on all REPO_REL args, **before** any git spawn — interior and leading alike. Contract ("no dotdot") plus this observed inconsistency make full rejection the only honest rule; do not normalize-and-continue.

### F4 HIGH — `git -C <repo>` does not protect against `GIT_*` environment retargeting (observed)

- `GIT_DIR=/nonexistent git -C <repo> rev-parse HEAD` → `fatal: not a git repository` (overrides `-C`)
- `GIT_OBJECT_DIRECTORY=<empty dir>` → `fatal: Not a valid object name` (object lookups silently redirected)

Same class: `GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_NAMESPACE`, `GIT_REPLACE_REF_BASE`, `GIT_CEILING_DIRECTORIES`, `GIT_INDEX_FILE`, `GIT_WORK_TREE`, `GIT_CONFIG_COUNT`+`GIT_CONFIG_KEY_n`/`GIT_CONFIG_VALUE_n` (arbitrary config injection), `GIT_TRACE*` (diagnostic writes). The SUT inherits the caller env by default. Control: pass an explicit env to every `subprocess.run`: drop every inherited `GIT_*`; set `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_NO_REPLACE_OBJECTS=1` (cat-file/ls-tree honor `refs/replace`; GateGit §3.1), `GIT_NO_LAZY_FETCH=1` (missing-blob promisor fetch = network, not read-only), `GIT_TERMINAL_PROMPT=0`, `LC_ALL=C`, `GIT_LITERAL_PATHSPECS=1` if any pathspec is ever used. `frozen/fixture-builder.py:22-30` is the in-repo precedent for this scrub. `merge-base` ignores replace refs (reachability exemption), so that call is unaffected — scrub for the read path regardless.

### F5 MED — `git -C ''` silently falls back to the CWD repository (observed)

`git -C '' rev-parse --show-toplevel` printed the lane toplevel. An empty `--repo` therefore silently retargets reconciliation onto whatever repo contains the SUT's cwd — a fail-open exactly where provenance matters. Control: reject empty `--repo` lexically; then `git rev-parse --git-dir` must succeed. `--repo` is a host path: do NOT apply the REPO_REL grammar to it (a host path legitimately contains `..`); normalize with `os.path.realpath` once and use the resolved dir for `git -C`. Subdirectory `--repo` is safe **only if** both `--full-tree` (gate line 189 precedent; without it `ls-tree` under `-C subdir` silently lists the subtree) and lexical `.`/`..` rejection (F3's subdir-relative resolution) hold.

### F6 MED — Option-injection surface on revision arguments

If the SUT ever passes a rev expression positionally (`rev-parse`, `merge-base`, `ls-tree <rev>`), a value like `--all`, `-C`, or `^{}`-decorated input parses as options. Controls:

- `--rev` must lexically match `[0-9a-f]{40}` (contract: "exact committed input revision"); then `cat-file -t <arg>` must be `commit`. Verify the object itself is a commit *before* peeling — `cat-file -t <oid>` returns `tag` for an annotated tag OID, which `^{commit}` would silently peel to a commit. Reject tag OIDs.
- `measured_revision` (receipt field): required string, exact `[0-9a-f]{40}`, `cat-file -t` == `commit`, then `merge-base --is-ancestor <measured> <resolved-input>`; any nonzero exit → 2 (covers unknown object, not-ancestor, shallow boundary).
- If name resolution is ever needed (short rev, ref): feed via `cat-file --batch-check` stdin like `_scan_git_revision` (`tools/mori-retention-gate.py:180-185`) — never argv.

### F7 MED — Crash paths that violate "sanitized error code only, never exception text"

- `subprocess.run` raises `ValueError: embedded null byte` if **any** argv element contains `\x00` — before exec, traceback on stderr, exit ≠ 2. NUL reaches argv not only via CLI args but via receipt JSON strings (`measured_revision` flows to `merge-base`/`cat-file` argv). Validate every git-bound string (`\0` absent; OID regex for revs) *before* spawn — schema validation (hex40 for measured_revision) incidentally covers this, but a generic `except` safety net is still required.
- `arg.encode('utf-8')` on a surrogateescape argv (non-UTF8 CLI bytes) raises `UnicodeEncodeError`. Use `os.fsencode`.
- Oracle asserts `cp.stderr == ''` on **every** arm including exit-2 (`oracle-reconcile-v2.py:42`): argparse's default error path writes usage to stderr — the SUT needs a structured-error emitter (JSON on stdout, sanitized code, exit 2) and a top-level catch mapping residual exceptions to exit 2 without exception text.

### F8 MED — Input-object type checks: `cat-file -t` cannot see symlinks

Observed: `cat-file -t` on a committed 120000 entry returns `blob`; `cat-file blob` emits the raw link text (observed bytes `target`). Gitlinks (`160000`) return `commit`, directory paths return `tree`. Control: for each REPO_REL input, obtain the tree entry and require mode ∈ {`100644`,`100755`} with kind `blob` before reading — via `ls-tree -z --full-tree <rev> -- <dirname>` + byte-exact basename match, or `GIT_LITERAL_PATHSPECS=1` + exact-match path (GateGit §2.B). Never match input paths through pathspec glob semantics. A path under a committed-symlink parent yields no entry → missing-input exit 2 (correct). After mode/type check, `cat-file blob <oid>` on the ls-tree-returned OID (hex-regex-validated) is injection-free — prefer OID reads over `rev:path` reads once the mode is known, since OID argv can never be option- or path-interpreted.

### F9 LOW — Non-UTF8 committed filenames

Tree paths are bytes; gate decodes `errors='replace'` for scan parity (line 202). Two distinct byte-paths can decode to the same hit `path` string (multiset ambiguity — inherited gate limitation, keep parity, note residual). For input-path matching compare **bytes** (`os.fsencode(arg)` vs raw ls-tree path bytes), never the replaced-decode.

### F10 INFO — Oracle subprocess hygiene is adequate

`oracle-reconcile-v2.py:35`: argv-form `subprocess.run`, `sys.executable`, `capture_output`, `timeout=60`, no shell — sound. Its `receipt_override='../receipt.json'` confirms R20 is lexical-path rejection, not filesystem traversal (blobs, not worktree, are read).

## Precise payload controls (implementation grammar)

**REPO_REL (`--receipt`, `--policy`, `--allowlist`)** — reject iff: empty; starts with `/`; any `/`-split component ∈ {``, `.`, `..`}; contains byte `< 0x20`, `0x7f`, or `\0`; (recommended also: `.git` component — uncommittable anyway). Compare against tree paths as raw bytes via `os.fsencode`. Optional sanity cap ~4 KiB.

**`--repo`** — nonempty; realpath once; `rev-parse --git-dir` succeeds. No component grammar (host path).

**`--rev`** — `[0-9a-f]{40}` then `cat-file -t` == `commit`; resolve once to itself. **Git argv discipline**: `git -C <repo>` argv-list only; permitted verbs `rev-parse`, `cat-file`, `ls-tree -r -z --full-tree`, `merge-base --is-ancestor`; scrubbed env per F4; `check=False`, captured stdio, timeout; every git-bound string NUL-free and (for OIDs) hex-validated pre-spawn. **Scan**: `ls-tree` filter kind==`blob` && mode!=`160000` — **include `120000` blobs** (symlink target text is in the hit population per GateGit §2.A; R21 rejects symlink *inputs* only). **Input reads**: mode/type check first (F8), then `cat-file blob <oid>`.

## Residual risk and verification gaps

- No SUT exists to review; findings F1–F8 are contract/fixture/oracle-level and must be re-verified against the landed candidate's diff plus an oracle run (L1's integration measurement).
- F1/F2 mean R20/R21 can currently pass with materially weaker validation than the contract intends — highest-value oracle hardening in scope.
- Gate-parity residual: `errors='replace'` path decoding ambiguity (F9) is inherited, not introduced.
- Out of scope (peers own): denominator/non-author semantics (v2 correction), receipt schema fields beyond revision binding, `--selftest` arm coverage.
