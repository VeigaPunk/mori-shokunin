measured 2026-10-23T12:06:12Z

# Round 36 safety and containment review

VERDICT: defect

## Findings

### HIGH — counter executes the candidate with host-user filesystem authority

- Exploit path: a candidate supplied through `--tool` or loaded from the revision is executed as Python by the counter; C1 runs it with the lane as cwd/root, and C2 runs it with the repository passed as `--repo`. The counters do not isolate candidate filesystem access. [C1 `count-c1.py:273-284,679-710`; C2 `count-c2.py:493-495,624-631,670-687`]
- C1 checks that `corpus/` matches the revision before candidate execution, then runs the candidate and reads the corpus afterward without repeating that check. [C1 `count-c1.py:573-593`]
- Impact: candidate code can alter lane files or the Git index, read accessible credentials/settings, or write outside the fixture roots; C1 can then evaluate a corpus the candidate itself changed. [INFERENCE from execution context and missing isolation/checks: C1 `count-c1.py:280-281,573-593`; C2 `count-c2.py:72-83,624-631`]
- Smallest remediation: run candidates in a restricted child sandbox with the lane/repository mounted read-only, a minimal environment, and explicit network policy; verify worktree and index invariance after execution.

### MEDIUM — C1 inherits Git-routing environment into its git and candidate processes

- C1's `git()` calls and candidate `subprocess.run()` omit `env=`, so they inherit the parent environment. [C1 `count-c1.py:92-104,277-284,575-578`]
- C2 explicitly removes `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, object-directory, alternate-object-directory, and common-dir variables before child processes. [C2 `count-c2.py:62-67,86-91,493-495`]
- Exploit path: if the runner has Git routing variables set, C1's `git -C` calls and candidate can be directed to a different repository/index; C1 also passes unrelated environment values to candidate code. [INFERENCE; C1 `count-c1.py:92-104,280-281`]
- Impact: false revision/worktree evidence and exposure of environment secrets/settings to the candidate. Smallest remediation: use a controlled environment for every C1 child process, including the C2 Git-variable removals and a non-secret allowlist.

### MEDIUM — C1 oracle permits redirect-based SSRF and unbounded response bodies

- The live oracle fetches URLs parsed from registry rows that have copies. It uses `urlopen()` (which follows redirects) and reads the entire response into memory with no byte limit. [C1 `count-c1.py:129-144,177-198,235-253`]
- Exploit path: a registry URL, or its redirect response, can target loopback/private services; a large or slowly delivered response can consume memory or hold up the run. [INFERENCE from URL handling and `resp.read()`: C1 `count-c1.py:194-198,245-253`]
- Impact: requests escape the intended public-source set and can probe/internal-GET reachable services; oversized responses can exhaust resources. Smallest remediation: validate every resolved address and redirect hop against an explicit public-host policy, and cap body bytes and total fetch duration.

### MEDIUM — candidate diagnostics can echo secrets into counter output

- C1 appends up to 200 characters of candidate stderr on unexpected exit; C2 prints the final line of captured stdout/stderr when no summary is parsed. [C1 `count-c1.py:560-561,638-639`; C2 `count-c2.py:601-607,700-702`]
- Since candidate processes receive the host environment (C1 fully; C2 except its listed Git variables), a candidate can print a secret or setting into that diagnostic path. [INFERENCE; C1 `count-c1.py:280-281`; C2 `count-c2.py:62-67,72-83,493-495`]
- Impact: secret/settings values can enter saved counter logs. Smallest remediation: never include raw candidate output in reports; emit fixed error categories and exit status only.

### LOW — exceptional setup failures can leave temporary directories

- C1 creates the extracted-tool directory before entering the `try/finally` that removes it; a failure writing the extracted blob can leave it behind. [C1 `count-c1.py:685-690,698-719`]
- C2 creates the scratch path before entering its cleanup `try`; a failure during `os.makedirs()` can leave a partially created path. [C2 `count-c2.py:689-691,717-720`]
- Smallest remediation: put each creation step inside the corresponding cleanup `try/finally`.

## Checks that passed by inspection

- C1 binds the fixture server specifically to `127.0.0.1`; normal blind-arm cleanup calls server shutdown/close and removes the fixture root. [C1 `count-c1.py:351-359,543-550,563-564`]
- C2 normal-path cleanup removes its sandbox root and extracted-tool directory. [C2 `count-c2.py:689-720`]
- Inspected subprocess calls use argument lists; no `shell=True` occurrence was found in either counter. [C1 `count-c1.py:92-104,273-284,575-578`; C2 `count-c2.py:70-90,493-495`; searches for `shell=True` returned no matches]

## Planned tool drafts

- Not reviewable at this inspection: both lane tool paths were absent (`read` returned “Path not found” for `tools/mori-source-drift.py` and `tools/mori-sources-appendonly.py`), and the requested `/fast/scratch/hyaku/mori-r36/Build*/tools/` glob returned no files. No claim is made about those tools' URL allowlists, path handling, output, size limits, or Git behavior.
- No index-check draft was present in the inspected build scratch paths. [Glob of `/fast/scratch/hyaku/mori-r36/BuildIndexCheck/` returned “Path not found”.]

No tools were installed or updated for this review.
