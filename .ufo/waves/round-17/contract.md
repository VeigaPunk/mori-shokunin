# mori round 17 — shared seat contract (L1-authored, 2026-10-20)

Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin` (branch `master`, entering tip
`24526ea9617cd020fee16c28fe4d4a2789dc28cb`, jj-colocated). L1 `MoriR17` is the only
integration owner and holds the canonical planner seat.

## Declared claims

- **C1 coverage (capability acquisition, lowest owned axis 6):** a read-only, field-limited
  *seat terminal-status* observation of OMP subagent transcripts. For a sessions directory it
  classifies each seat transcript's terminal record (completed / dead by rate limit / dead by
  quota / dead other error / aborted / incomplete / unavailable) and tallies per seat-name
  prefix and per provider/model. Detection and report only; it never edits, resumes or
  re-routes anything. Motivation: zai `429 ... (type=1302)` seat deaths today ("Retry budget
  exhausted after 10 retries").
- **C2 operability (7):** jj-colocation correctness of the census git probes: grade lane
  progress and report closure from `refs/heads/<branch>` instead of bare `HEAD`, and emit two
  new findings `HEAD_BRANCH_MISMATCH` and `LANE_AUTHOR_MISMATCH`. Routed evidence:
  `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditMori.md` (F3, F4, rows
  1/2/5/6) and `JjTrialMori.md`.
- **C3 calibration (5, added after wave-1 reconnaissance, before L1 measurement):** close the
  routed r16 blind-sweep mistake with a falsifiable misroot detector. On a sandbox retaining
  byte-exact `MoriR16.Lesson` content, a legacy `.ufo/waves .ufo/reports` pathspec misses the
  root file while the no-pathspec, filename-or-content detector finds it. Count missed
  known-misroot artifacts **1→0**; sibling and tracked controls stay unclaimed. This selects a
  lowest-scoring axis even under the literal all-six reading of AXES.md (ScorecardAxisCheck).
  Existing MisrootSweep work serves C3; it is no longer merely unclaimed conformance work.

The three claims are causally separable: C1 is a new standalone transcript tool; C2 edits the
census; C3 is a standalone misroot detector and a sandbox witness of the prior blind spot.

## C1 tool contract — `tools/mori-seat-terminal.py` (python3 stdlib only)

```
mori-seat-terminal.py --sessions-dir DIR [--prefix P ...] [--max-tail-bytes N] [--max-files N]
mori-seat-terminal.py --selftest
```

- Walk `DIR` recursively for regular files named `*.jsonl`; never follow symlinks; stop with
  rc2 `MORI_SEAT_TERMINAL_SETUP reason=too-many-files` above `--max-files` (default 20000).
  Seat id = file name without `.jsonl` (e.g. `TameshiR17.RR7-2`); prefix = text before the
  first `.` (e.g. `TameshiR17`); `--prefix` keeps only seats whose prefix equals one given.
- Read at most the last `--max-tail-bytes` (default 262144) of each file; if the read did not
  start at byte 0, drop the first (possibly partial) line. Parse each line as JSON; skip lines
  that fail. Consider ONLY records with `type == "message"` and a dict `message`. Every other
  record type (including `credential_pin`, `session_init`, `custom`) is skipped unread.
- Terminal record = the LAST such message record in the tail. Classes:
  - `completed`: role `assistant`, `stopReason == "stop"`.
  - `aborted`: role `assistant`, `stopReason == "aborted"`.
  - `dead_rate_limit`: role `assistant`, `stopReason == "error"` and (`errorStatus == 429` or
    errorMessage contains one of `429`, `rate_limit`, `Rate limit`, `RATE_LIMITED`,
    `resource_exhausted`).
  - `dead_quota`: `stopReason == "error"`, not rate-limit, errorMessage contains one of
    `quota`, `usage limit`, `402`, `credits`.
  - `dead_error_other`: any other `stopReason == "error"`.
  - `incomplete`: terminal role is `toolResult` or `user`, or assistant with any other
    stopReason (e.g. `toolUse`).
  - `unavailable`: no parseable message record in the tail, unreadable file.
  Order of tests: rate-limit before quota (a 429 that mentions quota is rate-limit).
- Per seat emit: `seat`, `prefix`, `class`, `provider`, `model`, `error_status` (int or null),
  `retry_exhausted` (bool: errorMessage starts with `Retry budget exhausted`),
  `retries` (int parsed from `after N retries`, else null), `error_code` (the digits of a
  `(type=NNNN)` token, else null). **Never emit errorMessage text, content, usage or any
  other field.**
- Output: one JSON document on stdout, schema `mori-seat-terminal-v1`, keys `schema`,
  `sessions_dir`, `files_scanned`, `totals` (every class, zeros included), `retry_exhausted`,
  `by_prefix` {prefix: totals}, `by_provider_model` {"provider/model": totals}, `seats`
  (sorted by seat id). Then exactly one stderr-free summary line on stdout is NOT allowed —
  the JSON is the only stdout. Exit 0 = scan complete and zero `dead_*`; exit 1 = scan
  complete and ≥1 `dead_*` (finding `MORI_SEAT_TERMINAL_DEAD` in key `finding`); exit 2 =
  setup/unavailable directory (finding `MORI_SEAT_TERMINAL_SETUP`). Finding key values:
  `MORI_SEAT_TERMINAL_OK` / `_DEAD` / `_SETUP`.
- Limits it must state in `--help`: a terminal error is the *last observed* state, not proof
  the session will never resume; dead counts are seats, not distinct incidents; prefixes are
  naming conventions, not authenticated lane membership.

## C1 fixtures and gate

- Fixture packs: `.ufo/waves/round-17/fixtures/seat/<pack>/` (synthetic transcripts built
  only from the record shapes above; never copied from real sessions) plus
  `.ufo/waves/round-17/fixtures/seat/expected.json` = `{"cases":[{"id","pack","args":[...],
  "want":{"rc":int,"finding":str,"totals":{...},"seats":{seat:class}}}]}`.
- Gate: `tools/mori-round17-seat-regressions.py --tool PATH --fixtures DIR --output DIR`
  runs the tool once per case as a real subprocess, writes `run-manifest.json` with per-case
  `match|mismatch|capability_absent`, input SHA-256 before/after, and exits 0 only when every
  case matches; a missing tool path gives `capability_absent` for every case and rc1.

## C2 census contract — `tools/mori-census.sh`

- Resolve the lane branch like `scripts/hyaku/jj-lane.sh detect_branch`: `symbolic-ref -q
  HEAD` → `refs/remotes/origin/HEAD` → unique of `refs/heads/master`/`refs/heads/main`.
- Use `refs/heads/<branch>` instead of `HEAD` for: the report-closure `cat-file -e` and
  `log -1` (row 6), the authorship `rev-parse --verify` and the `log --since` scan (row 9).
- `HEAD_BRANCH_MISMATCH` (severity drift): HEAD resolves and `merge-base --is-ancestor HEAD
  refs/heads/<branch>` fails; detail names lane, short head, short branch tip.
- `LANE_AUTHOR_MISMATCH` (severity drift): a post-launch commit on the branch whose committer
  is `<lane>-shokunin <lane>@shokunin.local` while its author differs. Grading semantics of
  rows A/B/C are otherwise unchanged.
- Gate: `tools/mori-round17-jj-regressions.py --census PATH --output DIR` builds real
  colocated jj sandboxes in its own temp tree (never in the lane or fleet), runs the census
  against them, and counts failed case assertions; run against the entering census
  (`git show 24526ea:tools/mori-census.sh`) and the delivered census.

## Seat discipline (binding)

Read `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/wave1-context.txt`
(the wave context) — it is the binding rule set; this file only carries interfaces.

## Amendment A1 (L1, 2026-10-20 ~16:10, after wave-1 reviews; supersedes the C1/C2 text above where they differ)

C1 tool/fixtures/gate:
1. Error classification order: quota tokens (`quota`, `usage limit`, `402`, `credits`) are tested FIRST, then rate-limit (`errorStatus == 429` or `429`, `rate_limit`, `Rate limit`, `rate limit`, `RATE_LIMITED`, `resource_exhausted`), then other. (Z.AI also returns 429 for quota errors — CriticFrontier/S043.)
2. Settle window: `--settle-seconds N` (default 900). A terminal `stopReason == "error"` record whose `completedAt`/`timestamp` (ms epoch) is newer than scan time minus N is class `error_unsettled` (not dead). `--now-ms MS` overrides scan time (fixtures use it). Dead classes therefore mean "last observed record is an error older than the settle window", never "will not resume".
3. Seat key = path relative to `--sessions-dir` without `.jsonl`; `seat` = file stem; duplicates of a stem across directories are separate entries and counted in `duplicate_stems`. Files directly in `--sessions-dir` whose stem matches `^\d{4}-\d\d-\d\dT[\d-]+Z_[0-9a-f-]+$` are main sessions: `kind: "main"`, excluded from totals (counted in `main_sessions`).
4. `--prefix P` matching zero seats => rc2 `MORI_SEAT_TERMINAL_SETUP reason=prefix-matched-none` (never a false clean). Prefix = text before the first `.` of the stem.
5. Robustness: only regular files via lstat (no symlinks, FIFOs, devices); a malformed/undecodable line is skipped, never a crash; any uncaught error => rc2, never rc1. Default `--max-tail-bytes` 524288.
6. Schema: read at most the first 4096 bytes for the header record `{"type":"session","version":N}`; version not in {3} or absent => that seat is `unavailable` with `reason: "schema"`.
7. `retries` regex `after (\d+) retr(?:y|ies)`; terminal roles other than assistant (toolResult, user, developer, bashExecution, …) => `incomplete`.
8. Output key `finding_id` (not `finding`), values `MORI_SEAT_TERMINAL_OK` / `_DEAD` / `_SETUP`; JSON adds `now_ms`, `settle_seconds`, `main_sessions`, `duplicate_stems`. Per-seat adds `key`, `kind`, `terminal_ms`, `reason` (null or `schema`/`no-message`/`unreadable`).
9. expected.json `want` uses `finding_id`; every case pins `--now-ms`.

C2 census (see message to CensusJj): severity `warn`; LANE_AUTHOR_MISMATCH only when the author email does not end in `@shokunin.local`; unresolved branch => exact old HEAD behavior; SURFACE/GL_EXTRA text unchanged.
10. (S043, Z.AI error-code table) a `(type=1113)` or `(type=1308)` error code means usage/balance => `dead_quota` even under HTTP 429; `(type=1302)` => rate limit. The code test runs before the token tests.
