# SentData — round-37 evidence hygiene

Axes: credential exposure; private/cursor data; operator-path hygiene.

**Severity: LOW.** **Attack path:** anyone with access to the committed receipts can read the operator's local account name and checkout layout. This is metadata exposure, not an access credential.

**Scope command:** `git archive e57c58b57c025364e79d130fbdf764d2674d83d6 -- .ufo/waves/round-37/evidence corpus/evidence/sources-r37`. Observed: 7 round evidence files and 4 copied source files (11 total) in the scored snapshot; scans below were read-only against these files.

| Scan / command pattern | Hits / observed output |
|---|---|
| Credential formats: `AKIA[0-9A-Z]{16}`, `ASIA[0-9A-Z]{16}`, GitHub/Slack token formats, private-key block, `Authorization: Bearer <value>`, URL user-info | `grep` output: **No matches found**. |
| Secret assignments: `(?i)(password|passwd|token|secret|api[_-]?key)[[:space:]]*[:=][[:space:]]*["']?[A-Za-z0-9+/=_-]{16,}` | `grep` output: **No matches found**. |
| Auth header: `(?i)(authorization|proxy-authorization):[[:space:]]*(basic|bearer)[[:space:]]+[A-Za-z0-9+/._~=-]+` | One published RFC example: `corpus/evidence/sources-r37/S221.src:4312`, `Proxy-Authorization: basic aGVsbG86d29ybGQ=`. `printf '%s' 'aGVsbG86d29ybGQ=' | base64 --decode` output: `hello:world` (example value, not a live credential). |
| Live cursor/runtime records: cursor assignment/value, journal cursor command, `_BOOT_ID`, `_MACHINE_ID`, `COREDUMP_*` | `grep` output: **No matches found**. |
| Email/private-record marker: `[[:alnum:]._%+-]+@[[:alnum:].-]+\.[[:alpha:]]{2,}` | Six public contact/example addresses in `S221.src:4545,8112,8972,10767,10775,10784` (RFC text); no private user records observed. |
| Operator/external path roots: `(/home/|/root/|/tmp/|/var/tmp/|/fast/|/mnt/|/media/|[A-Za-z]:\\)` | Three lane-root absolute paths: `.ufo/waves/round-37/evidence/c1-before-memo.txt:2`, `c1-before-summary.txt:2`, `census-start.txt:16`. One non-operator documentation example, `C:\\Program Files`, at `corpus/evidence/sources-r37/S223.src:412`. No lane-external operator path found. |

**Impact:** the three receipts expose the operator's absolute home/workspace path. No secret or live cursor/private runtime record was found. The Windows path is a public documentation example and is not an operator path.

**Smallest remediation:** regenerate those three receipts with repository-relative path display. No remediation performed (detection/report scope only).

**VERDICT: FAIL** — absolute operator paths at `.ufo/waves/round-37/evidence/c1-before-memo.txt:2`, `c1-before-summary.txt:2`, and `census-start.txt:16`.