# Round 36 wave 2 — evidence-file safety sweep

**Item attacked:** Evidence-file safety for `.ufo/waves/round-36/evidence/` and `corpus/evidence/sources-r36/` (credential/cursor/private-data leakage).

**Severity:** Low — local-path/username disclosure; no credential or journal-data disclosure found.

## Scope and measurements

- `glob(path="mori-shokunin/.ufo/waves/round-36/evidence/", hidden=true, gitignore=false)` → 12 top-level evidence files and `refs/`; recursive searches below include the refs. `glob(path="mori-shokunin/corpus/evidence/sources-r36/", hidden=true, gitignore=false)` → `S205.src` through `S220.src` (16 files).
- `functions.grep(path="mori-shokunin/.ufo/waves/round-36/evidence/;mori-shokunin/corpus/evidence/sources-r36/", gitignore=false, pattern="(?i)(\\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16})\\b|-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----|\\b(?:Bearer|Basic)[[:space:]]+[A-Za-z0-9._~+/-]{16,}={0,2})")` → **No matches found**.
- `functions.grep` over the same paths with pattern `(?i)(?:^|[[:space:]])(?:cookie|set-cookie|authorization|proxy-authorization):[[:space:]]*\\S|(?:access[_-]?token|refresh[_-]?token|api[_-]?key|client[_-]?secret|password|passwd)[[:space:]]*[:=][[:space:]]*[^[:space:]<>{}'\"]{8,}` → **No matches found**.
- `functions.grep` over the same paths with pattern `(?i)(op://[A-Za-z0-9_-]+/[A-Za-z0-9_-]+|-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----|-----END (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----)` → **No matches found** (no actual vault reference or key block).
- `functions.grep` over the same paths with pattern `(?i)https?://[^/@[:space:]]+:[^/@[:space:]]+@|https?://[^?#[:space:]]+[?&](?:token|access_token|auth|key|password|signature|sig)=[^&#[:space:]]{8,}` → **No matches found** (no credentialed URL or credential-like URL query).
- `functions.grep` over the same paths with pattern `(?i)(__CURSOR=|(?:^|[[:space:]])_CURSOR=|cursor=[A-Za-z0-9+/=:_-]{16,}|s=[0-9a-f]{16,};i=[0-9a-f]{1,};b=[0-9a-f-]{16,};m=|_BOOT_ID=[0-9a-f-]{16,}|MESSAGE=.{80,}|journalctl[[:space:]]+-o[[:space:]]+(?:export|json))` → **No matches found**.
- Broad keyword query `functions.grep` over the same paths for `(?i)(op://|-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----|-----BEGIN OPENSSH PRIVATE KEY-----|\\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16})\\b|\\b(?:authorization|proxy-authorization|cookie|set-cookie|access[_-]?token|refresh[_-]?token|api[_-]?key|client[_-]?secret|password|passwd|secret)\\s*[:=])` → only non-secret lexical hits: `S205.src:49-50,129` uses `op://…` as a placeholder while describing the prohibition; `S215.src:980,990` contains a Linux `cookie` variable / `BLK_QC_T_NONE`, not cookie data. Strict reference/value scans above found no actual secret.

## Finding — absolute local workspace paths in evidence

**Exploit path:** Anyone receiving the committed evidence bundle can read the census/C0 captures and recover the operator account name plus local project/workspace layout. No execution or elevated access is needed.

**Evidence and command output:**

- `read(path="mori-shokunin/.ufo/waves/round-36/evidence/census-start.txt")` → line 14: `mori\tok\t/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`.
- `read(path="mori-shokunin/.ufo/waves/round-36/evidence/census-end.txt")` → line 16: `mori\tok\t/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`.
- `read(path="mori-shokunin/.ufo/waves/round-36/evidence/c0-rescore-v2.txt:1-4")` → line 2 includes `control=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J1.py`; line 4 repeats the absolute control path. The home-path search over both scoped directories likewise returned paths under this same `/home/vgpnk/Projects/shokunin/mori-shokunin/` prefix; no other lane's absolute workspace path was observed.

The census start/end outputs otherwise show duplicate public source URLs and `EXIT=0`; they contain no raw journal cursor or journal entry. Direct reads of `c1-after.txt`, `c1-after-final.txt`, and `c2-after.txt` show only counters, status, IDs, tool path/seed (C1 seeds and C2 `/tmp` path), and no raw cursor/journal text.

**Impact:** The captured evidence reveals a local username and filesystem layout. It does not expose an authentication secret, and this scan found no other lane's private path/data.

**Smallest remediation:** Redact the absolute home/workspace prefix in the census and C0 evidence captures to repo-relative paths (for example, `corpus/SOURCES.md` and `.ufo/waves/round-36/c0/controls/J1.py`); have future evidence capture repo-relative paths.

No files outside this report were changed; no tools were installed.

VERDICT: FAIL — operator workspace path disclosure at `evidence/census-start.txt:14`, `evidence/census-end.txt:16`, and `evidence/c0-rescore-v2.txt:2,4`.