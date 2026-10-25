# SentPinExec — security review of `tools/mori-pin-check.py` (round 47 w1)

Seat: SentPinExec (leaf; security review of the tool that executes commands parsed from committed SKILL.md text).
Reviewed bytes: working tree `tools/mori-pin-check.py` sha256 `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1` — equals the frozen contract bytes (contract.md:14), so line numbers below refer to the measured instrument. Runtime: Python 3.14.8, git 2.56.0, `tarfile.data_filter` available. No tools installed (none needed).

Scope: interpreter allowlist, argument injection via backticked spans, path traversal in digest-file lookup, tar extraction filter, TMPDIR containment, and whether a malicious SKILL.md row can execute outside the export tree.

## Evidence (observed)

- `python3 -V` → `Python 3.14.8`; `git --version` → `git version 2.56.0`; `python3 -c 'import tarfile; print(hasattr(tarfile,"data_filter"))'` → `True`.
- In-memory probe of the frozen module (import + calls only; nothing executed):
  - `command_from_span("bash -c 'cat /etc/passwd' --selftest", …)` → `['bash', '-c', 'cat /etc/passwd', '--selftest']` (accepted).
  - `command_from_span("python3 -c 'import os; os.system(\"id\")' --selftest", …)` → `['python3', '-c', 'import os; os.system("id")', '--selftest']` (accepted).
  - `command_from_span("sh -c 'ls /' --selftest", …)` → `['sh', '-c', 'ls /', '--selftest']` (accepted).
  - `command_from_span("sudo bash -c 'x' --selftest", …)` → `None` (allowlist works only at position 0).
  - `command_from_span("tools/foo.py", …)` → `['python3', 'tools/foo.py', '--selftest']`; `command_from_span("../..//../esc.py", …)` → `['python3', 'tools/../esc.py', '--selftest']`; `command_from_span("../esc.sh", …)` → `['bash', '../esc.sh', '--selftest']` (bare-path spans execute, traversal allowed).
  - `PATH_RE.findall` on a row containing `` `../../../etc/passwd.txt` `` → matches; `os.path.normpath(os.path.join("/a/tree", "../../../etc/passwd.txt"))` → `/etc/passwd.txt` (digest lookup escapes the tree).

## Findings

### F1 — HIGH: interpreter "allowlist" is not enforced; arbitrary code execution from any backticked span (lines 147–156, 191)
`derive_command` (147–172) accepts any span whose first word, after `strip_env`, is in `INTERPRETERS` (`python3`, `python`, `bash`, `sh`; line 70) and returns the entire `shlex.split` argv verbatim (153–154); `run_cmd` execs it with `subprocess.run` (191). A span `` `bash -c '<anything>' --selftest` `` or `` `python3 -c '<anything>' --selftest` `` is therefore executed, with no restriction to the intended `<interp> <tool-path> --selftest` shape.
Exploit path: a malicious or compromised SKILL.md row self-test cell (the gate registry is the exact surface C1 measures) yields host RCE at the checker's privilege on any run of `python3 tools/mori-pin-check.py --rev …`. Verified by probe above.
Impact: arbitrary code execution with the operator's credentials; the tool is meant to run on the landed tip and in CI/verifier contexts. Consequence: an untrusted row is complete host compromise, not just a false green.

### F2 — HIGH: a malicious row executes entirely outside the export tree (lines 183–199, 189–192)
`run_cmd` runs children with `cwd=root` (191) but `env` = full `os.environ` + TMPDIR (189) and no sandbox (no namespace/chroot/restricted PATH/HOME). `cwd` only affects relative-path resolution; the process has the host filesystem, network, and environment. `bash -c 'curl … | bash' --selftest` is fully outside-scope. Additionally, bare-path spans (114–117) auto-execute any backticked `.py`/`.sh` span in the cell, including `..`-containing paths (probe: `tools/../esc.py`, `../esc.sh` accepted), so even the "no `-c`" shape can launch an executable resolved outside the measured tree (`--root` mode: sibling dirs; `--rev` mode: up from `<repo>/.scratch/…/tree` into the lane repo and beyond).
Impact: a malicious row can read/modify/delete anything the checker user can — including the repo being verified and the host — regardless of the export-tree containment the docstring claims ("Read-only over committed bytes", 50–52).

### F3 — MEDIUM: path traversal in digest-file lookup (lines 67, 273–277)
`PATH_RE` (67) permits `.` and `/` inside path components and thus `..`; candidates are collected from the **whole raw row** (273), joined with `os.path.join(root, p)` (276), and opened via `isfile` + `sha256_file` (277) with no normalization or containment check. Probe: `../../../etc/passwd.txt` normalizes to `/etc/passwd.txt`.

- Integrity bypass: a digest pin can be matched against a file **outside the measured revision** — e.g. under `--rev`, `../../../SKILL.md` resolves to the live worktree SKILL.md (tree → `..` = scratch dir → `../..` = `repo/.scratch` → `../../..` = lane repo root), so a stale digest can be made to "match" a file the revision does not contain, silently passing the `mismatches=0` gate and defeating the calibration claim. Sibling-lane files are reachable one level further (fleet root).
- Filesystem read oracle: opens arbitrary readable files (any of the six extensions, anywhere reachable via `..`), and the hash computation is inline in the parent with no timeout/size cap — a large `.txt`/`.md` file (or a slow read) hangs the checker indefinitely (DoS).
- Symlink following: `git archive` preserves committed symlinks; `sha256_file` follows them, so a symlink inside the tree pointing outside also makes an out-of-tree match possible without `..`.

### F4 — LOW (informational): tar extraction filter is sound (line 312)
`t.extractall(tree, filter="data")` uses the Python `data` filter (present on host 3.14.8), which blocks absolute paths, `..` members, devices, and out-of-tree links — appropriate for an archive of `git archive` output, which cannot emit such members anyway. Residual: a hostile tar member raises `ValueError` and aborts the whole check (availability, not compromise). No change needed.

### F5 — LOW (advisory): TMPDIR containment is informative, not enforced (lines 186–189)
TMPDIR is set to a fresh dir under `<root>/.scratch` and `PYTHONDONTWRITEBYTECODE=1` is set (189), but nothing prevents a spawned command from ignoring TMPDIR and writing anywhere (including the repo itself). This satisfies the "lane tools refuse a TMPDIR outside their lane root" convention but is not a security boundary. Note: leading `VAR=value` words in spans are silently dropped by `strip_env` (141–144), not honored — benign but surprising.

## Smallest remediation (for the integrator; not applied here — review seat)
1. F1/F2: in `derive_command` (147–172) and `command_from_span` (111–119), accept only the exact shape `[<allowed-interp>, <path>, "--selftest"]` with `<path>` resolved (normpath) and required to remain inside the measured tree; drop `-c` and any extra argv. Optionally run children with a sanitized env (PATH/HOME only) and `cwd=root`.
2. F3: at 273–277, reject candidates whose `os.path.normpath(os.path.join(root, p))` does not start with `root`; use `os.path.realpath` and skip non-regular files (avoid symlink escape); cap read size.
3. F4/F5: no code change required; document that TMPDIR is advisory.

## Verification status
Everything above is verified by reading the frozen bytes (sha256 matches contract) and by an in-memory module probe; no malicious command was executed, and no host state was touched. UNVERIFIED: none (no claims outside what was observed).
