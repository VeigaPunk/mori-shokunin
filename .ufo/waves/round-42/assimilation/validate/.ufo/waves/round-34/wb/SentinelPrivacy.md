measured 2026-10-23T07:45:18Z

# Privacy scan — round 34 wave B

Scope: every file listed under `wa/`, `evidence/` (including `ctl-postdata-shortcut/`), and the six files in the L1 `drafts/` snapshot. The scans included nested evidence and both `.pyc` files under the untracked fleet `__pycache__` entry.

VERDICT: findings 5

Two finding lines contain five sensitive-value occurrences:

1. **Severity: Low — four real PIDs.** `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/wa/ExecRerunLane.md:184` records four concrete process IDs for a sibling's live process tree; context at `:181-187` identifies the concurrent counter run. **Exploit path:** a reader of the candidate report can correlate these identifiers with host process/audit records if they have access to those records. **Impact:** unnecessary disclosure of transient process identifiers; no process-control access is demonstrated. **Smallest remediation:** redact the four numbers in any committed copy and retain only that a sibling process tree was visible.

2. **Severity: Low — one actual OMP setting value.** `/fast/scratch/hyaku/mori-r34/a3-L1/drafts/LOG.md:1801` exposes the operator's configured `async.maxJobs` value (value omitted here). `:1802` describes the installed binary's clamp/default, not the operator's configured value. **Exploit path:** if the L1 copies the draft line into a committed log, a reader learns the local concurrency configuration. **Impact:** operational configuration disclosure; no credential or token is exposed. **Smallest remediation:** omit the literal configured value in any landing; retain only the configured-versus-effective conclusion if needed.

**Other requested classes:** no UID, `user-<digits>.slice`, session ID, journal `MESSAGE` payload, home-directory secret/token, or block-device serial/WWN/UUID was found. `functions.grep` scans over the full scope for UID/slice and session-ID/UUID forms, exact `MESSAGE` fields, credential/private-key/token patterns and credential-bearing home paths, and block identifiers (`ID_SERIAL`, `ID_WWN`, UUID/PARTUUID and by-id/by-uuid paths) returned “No matches found.”

**Fleet-root check:** `timeout 10s git -C /home/vgpnk/Projects/shokunin status --porcelain` returned a non-clean worktree: 11 modified entries (10 `.ufo/state/*report-baseline` files, including `.ufo/state/mori.report-baseline`, plus `.ufo/watchdog.log`) and 15 untracked entries. Each untracked entry was scanned individually for case-insensitive whole-word `mori` or `round 34`; the `scripts/hyaku/__pycache__/` directory contained two files and was included. Every scan returned “No matches found,” so **there are no untracked fleet-root files whose content names `mori` or `round 34`**. The status output does not identify who made the existing changes or when; attribution to an earlier seat, or proof that none wrote elsewhere, is [INFERENCE] and not established by this check.

Tooling: no tools installed or updated. Operator rules read at `/home/vgpnk/.omp/agent/RULES.md:1-14`.