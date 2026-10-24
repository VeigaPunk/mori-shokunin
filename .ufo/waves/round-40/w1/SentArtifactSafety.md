# SentArtifactSafety — round 40

Scope: static review of `.ufo/waves/round-40/` and `corpus/`, including command construction, path handling, embedded credential-like material, and child cleanup. **No builder, counter, conformance check, gate, fixture, or test was executed.** No files other than this seat report were written; no Git/JJ commands were run.

## Findings

### High (when the candidate repository/revision is untrusted): C7 executes code read from the selected revision

**Exploit path:** invoke `count-c8.py` against a repo/revision containing a malicious `tools/mori-source-drift.py`. The counter reads that revision's blob (`count-c8.py:455-479`), writes it into its scratch directory, then runs it with the current Python interpreter via `selftest_arms()` (`count-c8.py:371-382`). The subprocess inherits the caller environment except for a few Git variables (`count-c8.py:178-182`).

**Impact:** arbitrary Python code executes with the caller's filesystem/network permissions and access to inherited environment secrets. Timeouts and process-group termination (`count-c8.py:109-135,139-169`) bound ordinary hangs but are not a sandbox and do not restrict those capabilities.

**Smallest remediation:** treat this counter as trusted-revision-only; if untrusted revisions must be evaluated, run the extracted tool in an isolated sandbox with no secrets, restricted filesystem, and network disabled (or redesign the selftest so candidate code is not run).

### Low: fixture CLI output paths are not confined to lane scratch/evidence

**Exploit path:** `make-survivor-fixtures.py` accepts `outdir` from `argv[2]`, creates it, and writes fixed `survivor-*.py` names there without validating the resolved path (`fixtures/make-survivor-fixtures.py:117-125`). `run-c11-dags.py` accepts `lane` and `out_path` from argv, uses `<lane>/.scratch` for temporary repositories, and opens `out_path` for writing without a root or symlink check (`fixtures/run-c11-dags.py:32-42,64-65`). Passing a path outside the lane can write there; its `gate_script` argument is also directly executed as Python (`:33,51-54`). This is not shell injection: subprocess arguments are passed as a list, without a shell.

**Impact:** a mistaken or hostile invocation can overwrite a target outside the allowed artifact roots (including a fleet/sibling file); a hostile `gate_script` runs as the caller. The recorded invocations use lane evidence/scratch paths; this audit did not invoke either builder. Current `.scratch`, round-40 scratch, and `fixtures/generated` are directories (not symlinks), each mode `755`.

**Smallest remediation:** canonicalize and enforce the expected lane root and allowlisted output subdirectories before writing; reject symlinked destinations. Restrict the runner's gate script to the expected checked-in gate paths.

### Low / unverified: a third-party API-key field is copied into corpus evidence

**Evidence:** `corpus/evidence/recheck-r32/S041.src:698`, `S062.src:1696`, `corpus/evidence/sources-r36/S206.src:698`, and `S209.src:1696` contain the same `typesenseApiKey` field in captured RFC Editor page JavaScript. The value is intentionally not reproduced here. The captures show a browser-side field, but local evidence does not establish whether the value is active or its permission scope; it may be a public, restricted search key rather than a secret.

**Impact:** if the copied value is an active credential with more than public read/search scope, publishing the corpus can enable unauthorized use or access. The credential-material absence claim is not established by this corpus.

**Smallest remediation:** establish the key's owner, validity, and scope; redact it from these captures, and revoke/rotate it only if it is sensitive or overprivileged. Do not treat an `oidcClientId` as a secret without evidence.

### Informational: absolute paths outside the lane/fleet roots remain in the scanned artifacts

**Evidence:** the round-40 `/tmp/` search found the test-mutation literal `/tmp/mori-r39-scratch` at `conform.py:733`, extracted/generated copies at `fixtures/extracted/conform-v2-r39.py:450`, `fixtures/generated/conform-r39-conjunct-gutted.py:450`, and `fixtures/generated/conform-v3-conjunct-gutted.py:733`, plus two round-40 scratch copies at `scratch/mutconform-arms2/conform-mut-cond-unconditional.py:733` and `conform-pristine.py:733`. These are mutation-test strings, not active output destinations. The full corpus `/tmp/` scan returned 601 matches; examples include `corpus/evidence/README.md:27,308,430,542` and historical receipts such as `corpus/evidence/backchannel-r6-20261015T191216Z-attack-r1.log:5,11,143`. These are archived test paths, not round-40 runtime writes. The targeted scan of the newly admitted S229 source, round-40 lesson, and round-40 knowledge entry found no external absolute paths.

**Impact:** this fails a strict literal “no absolute paths outside lane/fleet roots” criterion, though the round-40 `/tmp` literals are test data and the corpus examples are historical scratch paths. They disclose old temporary naming, not a current fleet path or secret.

**Smallest remediation:** if the criterion applies literally to all corpus text, replace archived temp-path literals with placeholders; otherwise explicitly scope the rule to active paths/new artifacts and document archived receipts as exceptions. No edit was authorized here.

## Checks and observed outputs

The following are the exact static-search parameters used with `functions.grep` (not shell commands; shell `grep` was not run):

- Credential-pattern search over `.ufo/waves/round-40/` and `corpus/`: `(?i)(op://|(?:api[_-]?key|access[_-]?token|auth[_-]?token|password|passwd|secret|credential)\s*[:=]\s*['\"]?[A-Za-z0-9_./:+-]{8,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)`. Output included the four `typesenseApiKey` captures listed above and policy/prompt text mentioning `op://`; no matching vault reference, private-key header, or common GitHub/AWS token form was identified. The matching key value is redacted from this report.
- `pattern="typesenseApiKey"`, `path="/home/vgpnk/Projects/shokunin/mori-shokunin/corpus"` → exactly the four file:line hits listed above.
- `pattern="op://"`, path `.ufo/waves/round-40;/home/vgpnk/Projects/shokunin/mori-shokunin/corpus` → matches were assignment/policy prose (`gen-wave-spec.py:147`, `w1-spec.json:320`, `corpus/evidence/sources-r36/S205.src:50,129`, and `corpus/lessons/round-25-verifier-spotcheck.md:115`); no actual vault reference was found.
- `pattern="/tmp/"`, path `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40` → the six test-literal hits listed in the path finding.
- `pattern="/tmp/"`, path `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus` → 601 matches; representative lines listed in the path finding.
- External-path pattern `(/(?:tmp|var|etc|root|opt|mnt|media|srv|run|dev|proc|sys|usr|workspace|workspaces)/[^\s`'\"<>)]*|/home/[^\s`'\"<>)]*)`, path `corpus/evidence/sources-r40/S229.src;corpus/knowledge/conform-scope-r40.md;corpus/lessons/round-40.md` → no matches.
- Command-construction search on fixture builders for `(shell\s*=\s*True|os\.system\(|subprocess\.(?:run|Popen|call|check_call|check_output)\(|\beval\(|\bexec\()` → subprocess calls only; no `shell=True`, `os.system`, `eval`, or `exec` in the builders. `run-c11-dags.py:51-54` uses an argv list and timeout; `:62-65` removes the temporary DAG root in `finally` and then writes the requested receipt.
- `stat -c '%F %a %N' <lane>/.scratch <lane>/.ufo/waves/round-40/scratch <lane>/.ufo/waves/round-40/fixtures/generated` → all three reported `directory 755`, not symlinks.
- `stat -c '%A %a %n' <lane>/.ufo/waves/round-40/fixtures/make-survivor-fixtures.py <lane>/.ufo/waves/round-40/fixtures/run-c11-dags.py <lane>/tools/mori-sources-appendonly.py` → each reported `-rwxr-xr-x 755`.

Static source reads covered `make-survivor-fixtures.py:17-25,34-129`, `run-c11-dags.py:24-70`, `conform.py:127-135,738-767`, `count-c8.py:109-205,371-382,455-529`, `mori-sources-appendonly.py:99-163,424-511,776-875`, and `gen-wave-spec.py:16-18,41-47,147-163`. No shell command, fixture builder, credential, or cleanup check was run dynamically.
