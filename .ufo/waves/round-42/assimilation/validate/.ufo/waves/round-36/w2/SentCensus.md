# SentCensus — round 36 live-surface safety review

**Item attacked:** whether round 36 adds a live-host write path or changes existing census/oracle/silence/journal behavior or host thresholds. Read-only inspection only; no new tool was run against live URLs or host services. No tools installed.

## Finding — C1 probe can issue requests to host-local services

- **Severity:** Medium, conditional SSRF / side-effectful GET.
- **Exploit path:** A data contributor appends a `corpus/SOURCES.md` row whose source URL targets `127.0.0.1`, a private/link-local address, or a public URL that redirects there, and includes a matching committed copy. An operator runs `python3 tools/mori-source-drift.py --root .`. The parser extracts that URL; because a copy exists, the production path calls `fetch()`, which uses `urllib.request.urlopen()` with its default redirect handling. A reachable local service that mutates state on GET could therefore be triggered by this supposedly read-only probe. No request was made to test or operationalize this scenario.
- **Evidence:** `tools/mori-source-drift.py:57-69` takes the first HTTP(S) URL from the row; `:101-112` constructs a default-method `Request` and calls `urlopen`; `:159-188` reads the registry/copy and fetches each URL-backed copied row. The frozen contract at `.ufo/waves/round-36/contract.md:36-46` confirms row URLs are fetched and redirects followed. The production entry point is distinct from `--selftest` at `:363-372`.
- **Impact:** There are no production filesystem writes in this tool’s run path, but the untrusted URL/redirect is an indirect path from repository data to requests against live local services. Whether it mutates state depends on an accessible endpoint’s behavior; no such endpoint was tested or observed.
- **Smallest remediation:** Restrict fetch destinations to an explicit set of source hosts, or reject non-global addresses and re-check every redirect destination before connecting. Preserve the existing fixture-only writes in `--selftest`.

## Other live-surface checks

- The existing census, silence/oracle, journal, and regression-arm files are byte-unchanged. `mori-index-clean.sh` and `mori-sources-appendonly.py` have read-only production paths; their `--selftest` branches create/clean temporary fixtures. `mori-index-clean.sh` explicitly uses `git --no-optional-locks` (`:10-12,39-41`) and its production `check_repo()` uses `rev-parse`, `diff`, and `status` (`:83-120`). The append-only gate’s production git helper is read-only (`tools/mori-sources-appendonly.py:87-117`); sandbox writes are in its separate self-test (`:291-345,391-463`). The drift probe’s local fixture writes are likewise in `_selftest()` only (`:238-350`).
- No existing census/host threshold or tuning code changed: all pre-existing executable paths in the tools directory are untouched. The new probe has probe-local fetch bounds (`FETCH_TIMEOUT_S=30`, `FETCH_TRIES=3`); the new index gate has a report-list cap (`MAX_PATHS=20`). These are new-tool behavior, not edits to existing host grading thresholds.

## Measurements

1. Command: `git diff --stat 6bd57097..bf0df77fee4b6ef54a90aea09335c7617f125151`
   Observed: `118 files changed, 33850 insertions(+)`.
2. Command: `git diff --name-status 6bd57097..bf0df77fee4b6ef54a90aea09335c7617f125151 -- tools/`
   Observed:
   ```
   A tools/mori-index-clean.sh
   A tools/mori-source-drift.py
   A tools/mori-sources-appendonly.py
   ```
3. Command: `git diff --quiet 6bd57097..bf0df77fee4b6ef54a90aea09335c7617f125151 -- tools/mori-census.sh tools/mori-silence-cases.sh tools/mori-journal-window.py tools/mori-blind-check.sh tools/mori-round13-regressions.py tools/mori-round16-regressions.py; printf 'DIFF_QUIET_EXIT=%s\n' "$?"; git diff --name-status 6bd57097..bf0df77fee4b6ef54a90aea09335c7617f125151 -- tools/mori-census.sh tools/mori-silence-cases.sh tools/mori-journal-window.py tools/mori-blind-check.sh tools/mori-round13-regressions.py tools/mori-round16-regressions.py`
   Observed: `DIFF_QUIET_EXIT=0`; the following name-status command emitted no paths.
4. Command: `git diff --name-status 6bd57097..bf0df77fee4b6ef54a90aea09335c7617f125151 -- tools/mori-census.sh tools/mori-silence-cases.sh tools/mori-journal-window.py tools/mori-blind-check.sh tools/mori-round13-regressions.py tools/mori-round16-regressions.py`
   Observed: no output.
5. Command: `git diff --unified=0 6bd57097..bf0df77fee4b6ef54a90aea09335c7617f125151 -- SKILL.md corpus/QUALITY.md corpus/SOURCES.md`
   Observed summary: `3 files changed, 61 insertions(+), 0 deletions(-)`; the existing policy additions are registry/criteria text, with no existing tool tuning lines replaced.

**VERDICT: FAIL** — the existing live census/oracle/silence/journal arms are unchanged, but the new C1 probe’s unvalidated URL and redirect destinations provide a conditional live-host side-effect path.