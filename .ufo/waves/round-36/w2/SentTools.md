# SentTools — safety sweep

**Attack:** `tools/mori-source-drift.py`, `tools/mori-sources-appendonly.py`, and `tools/mori-index-clean.sh`.

## Finding — MEDIUM: fetched response is unbounded

**Exploit path:** An untrusted `corpus/SOURCES.md` row supplies an HTTP(S) URL (drift tool lines 9–12, 44–46, 63–68). `fetch()` issues a `urllib.request.Request` and calls `urlopen(..., timeout=30)` (lines 101–112). The timeout is not an overall response deadline, and `resp.read()` consumes the body to EOF without a byte limit. A server can keep the response open and send data often enough to avoid the socket inactivity timeout; the call then need not return, while the response body is accumulated. The three-attempt loop (lines 50–51, 108) cannot bound this because it only advances after `urlopen`/`read` returns.

**Impact:** Running the drift tool against a registry entry pointing at such a server can hang the invocation and exhaust its memory. This violates the bounded-operation expectation for external fetches. The request is GET by default; the observed request header is only the tool's User-Agent (lines 109–112).

**Smallest remediation:** Stream the response in chunks with both a strict maximum body size and an absolute per-fetch deadline; classify an over-limit/expired response as unavailable.

## Other checks

- **Credential-pattern scan:** `grep` over the three target files with `(?i)(password|passwd|secret|token|api[_-]?key|credential|authorization|bearer|BEGIN (RSA|OPENSSH|EC|PGP) PRIVATE KEY|gh[pousr]_[A-Za-z0-9]{10,}|sk-[A-Za-z0-9]{10,})` → `No matches found.` Static inspection found no credential retrieval or auth header construction; drift's request header is `User-Agent` only.
- **Write boundaries:** Static inspection: drift's normal path opens `corpus/SOURCES.md` and copy files read-only (lines 159–185); its fixture writes under `tempfile.mkdtemp` roots and removes both roots in `finally` (lines 238–350). Append-only's normal subprocess calls are argv-based read-only `rev-parse`, `log`, and `show` with 120-second subprocess timeouts (lines 87–117, 190–216); its fixture repo is under a `mkdtemp` root removed in `finally` (lines 391–461). Index-clean's normal git wrapper uses `--no-optional-locks` and sets `GIT_OPTIONAL_LOCKS=0` (lines 10–11, 26–27, 39–41); its only file redirects and mutating git calls are inside the `mktemp` sandbox repo, cleaned by the RETURN trap (lines 144–160, 171–186). No non-selftest write outside those temporary roots was found.
- **Network/retry bounds:** Static inspection: drift's production fetch uses `urllib.request.urlopen` only (line 111), with `FETCH_TIMEOUT_S = 30`, `FETCH_TRIES = 3` (lines 50–51), and bounded retry waits (lines 119–144). The unbounded body consumption described above means the timeout does not bound completion.

## Executed selftests

- Command: `python3 tools/mori-source-drift.py --selftest`

  Output:
  ```
  selftest exit_code            PASS
  selftest row_states           PASS
  selftest summary              PASS
  selftest missing_sources_exit2 PASS
  MORI_SOURCE_DRIFT_SELFTEST: PASS (4 cases)
  ```

- Command: `python3 tools/mori-sources-appendonly.py --selftest`

  Output: `MORI_SOURCES_APPENDONLY_SELFTEST pass=8 fail=0`

- Command: `bash tools/mori-index-clean.sh --selftest`

  Output: `MORI_INDEX_CLEAN_SELFTEST pass=4 fail=0`

**VERDICT: FAIL — `tools/mori-source-drift.py:111–112`**