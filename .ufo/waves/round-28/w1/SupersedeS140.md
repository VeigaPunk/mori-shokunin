# Round 28, wave 1 — SupersedeS140 (seat MoriR28.SupersedeS140)

Claim: C1 (freshness). Row S152 supersedes S140 (routed defect 4: "the low finding in ReopenS140", `corpus/lessons/round-27.md:128`, `corpus/lessons/round-27-verifier-spotcheck.md:151`). This report gives the L1 the ready-to-paste S152 row, the Gate line, the fetch ledger, the QUALITY 77 sweep list, and the falsifications run on sandbox clones. The lane was not written except this report file.

## 1. First-published cells vs the row at 6ebd518f

Oldest lane commit carrying `| S140 |`: `5f00fd045c137b7e3835506d69946cfd9d010eb5` (`git log --reverse --format=%H -S'| S140 |' -- corpus/SOURCES.md | head -1`). The S140 row at `5f00fd0` and at `6ebd518f` is byte-identical:

```
| S140 | oh-my-pi commit 6962d5cd2ef157ebf9f415acd58b8744f66400d8 — https://github.com/can1357/oh-my-pi/commit/6962d5cd2ef157ebf9f415acd58b8744f66400d8 | code | A | the 2026-09-24 rewrite of the clamp from a static value to a per-check function; that rewrite only | sdk.ts:1949 `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings) ?? 100),`; parent d9bc4fbd still static (`:1797`, `:1811`) (authored 2026-09-24T18:04:41Z) | The clamp site is not immutable: the same ceiling can be re-expressed as a per-check function, and the explicit floor can vanish in the rewrite. | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md |
```

Row line sha256 at both revs: `6103520e0c3a59a512338f98ec9c48befb14f5e506bab2662c4d94b37f61bd62` (identical). **No cell differs.** S140 was never edited in place (`check-row-identity.py` at `6ebd518f` prints `changed=3` for S096/S097/S101 only). The S140 defect is a published-content defect, not a drift.

## 2. Fetch ledger (curl, `-f`; all HTTP 200)

| URL (fetched) | access (UTC) | sha256 |
|---|---|---|
| https://raw.githubusercontent.com/can1357/oh-my-pi/6962d5cd2ef157ebf9f415acd58b8744f66400d8/packages/coding-agent/src/sdk.ts | 2026-10-22T17:59:24Z | 84f3a112a670f36de9c030756f4babc0ad83e37efeca99154ea4d4263423e633 |
| https://raw.githubusercontent.com/can1357/oh-my-pi/6962d5cd2ef157ebf9f415acd58b8744f66400d8/packages/coding-agent/src/async/job-manager.ts | 2026-10-22T17:59:30Z | f8851470a8bd953f25ab659c0d0aac2ea8c34df9a433e154ec4127c7683b70bd |
| https://raw.githubusercontent.com/can1357/oh-my-pi/d9bc4fbdc06a967c5cb1f41a53d67a4dda8dfd1f/packages/coding-agent/src/sdk.ts | 2026-10-22T17:59:24Z | fde5a959e3a310be1d9fd291163dd817d2328d2b5a2012697b75b3205d592104 |
| https://raw.githubusercontent.com/can1357/oh-my-pi/d9bc4fbdc06a967c5cb1f41a53d67a4dda8dfd1f/packages/coding-agent/src/async/job-manager.ts | 2026-10-22T17:59:30Z | c417f63c7686e19ef9a0a658519de843e87dede6e23f73ee3ef1583f95e61aaf |
| https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/sdk.ts | 2026-10-22T17:59:30Z | c0228addd4cfe93cfd370c7248e9db29743f0fa802aea0e1d1adf4994dbe6957 |
| https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/async/job-manager.ts | 2026-10-22T17:59:30Z | 0f37afaaa822ef1de845b8eb21473a70210176ff61e2dcff5925f85ec0e544e7 |
| https://api.github.com/repos/can1357/oh-my-pi/commits/6962d5cd2ef157ebf9f415acd58b8744f66400d8 | 2026-10-22T17:59:24Z | ff56022fce1f209b25030b9292649185cdaf890fc863a91d2437dd176067c03f |
| https://github.com/can1357/oh-my-pi/commit/6962d5cd2ef157ebf9f415acd58b8744f66400d8.patch | 2026-10-22T18:03:46Z | 0c8fa1ee3d1a241b6eb740eb117e56dcfd7ca7fa5e4dcd947fd1eb98a5a8d2e7 |

Digests 1, 3, 5, 6, 7, 8 match the r27 ReopenS140 report (`/fast/scratch/hyaku/mori-r27/ReopenS140/`) byte-for-byte; 2 and 4 are job-manager.ts at 6962d5cd and its parent (not previously recorded). Verified bytes:

- sdk.ts@6962d5cd:1949 (five-tab indent): `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings) ?? 100),` (sole `maxRunningJobs` hit).
- sdk.ts@parent d9bc4fbd:1797 `const asyncMaxJobs = Math.min(100, Math.max(1, settings.get("async.maxJobs") ?? 100));`; :1811 `? new AsyncJobManager({ maxRunningJobs: asyncMaxJobs })` — static, computed once.
- job-manager.ts@6962d5cd:148 `maxRunningJobs?: number | (() => number);`; :285 `this.#maxRunningJobsOption = options.maxRunningJobs;`; :302-306 getter, floor at :305 `return Math.max(1, Math.floor(value ?? DEFAULT_MAX_RUNNING_JOBS));`.
- job-manager.ts@parent:284 `this.#maxRunningJobs = Math.max(1, Math.floor(options.maxRunningJobs ?? DEFAULT_MAX_RUNNING_JOBS));` — the manager already floored the cap at 1 at construction before this commit.
- API: parent `d9bc4fbd` sole; author date 2026-09-24T18:04:41Z, committer 2026-09-24T19:09:05Z; subject "feat: implemented centralized settings registry and internal URL routing"; 300 files, +21217/−15807.

## 3. Ready-to-paste row S152 (insert after the S144 row at `corpus/SOURCES.md:150`)

```
| S152 | oh-my-pi sdk.ts and async/job-manager.ts at commit 6962d5cd2ef157ebf9f415acd58b8744f66400d8 and at its parent d9bc4fbdc06a967c5cb1f41a53d67a4dda8dfd1f — https://raw.githubusercontent.com/can1357/oh-my-pi/6962d5cd2ef157ebf9f415acd58b8744f66400d8/packages/coding-agent/src/sdk.ts ; https://raw.githubusercontent.com/can1357/oh-my-pi/6962d5cd2ef157ebf9f415acd58b8744f66400d8/packages/coding-agent/src/async/job-manager.ts ; https://raw.githubusercontent.com/can1357/oh-my-pi/d9bc4fbdc06a967c5cb1f41a53d67a4dda8dfd1f/packages/coding-agent/src/sdk.ts ; https://raw.githubusercontent.com/can1357/oh-my-pi/d9bc4fbdc06a967c5cb1f41a53d67a4dda8dfd1f/packages/coding-agent/src/async/job-manager.ts ; commit page https://github.com/can1357/oh-my-pi/commit/6962d5cd2ef157ebf9f415acd58b8744f66400d8 | code | A | the 2026-09-24 rewrite of the running-job cap: the sdk clamp site moves from a static value to a per-check function, the manager option widens from a number to a function, and the cap's floor of 1 moves from session construction to a per-check getter; that commit's clamp and floor only, not the settings registry and internal URL routing the same commit also carried (300 files changed; subject "feat: implemented centralized settings registry and internal URL routing") | sdk.ts at 6962d5cd:1949 (five-tab indent) `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings) ?? 100),`; sdk.ts at parent d9bc4fbd:1797 `const asyncMaxJobs = Math.min(100, Math.max(1, settings.get("async.maxJobs") ?? 100));` and :1811 `? new AsyncJobManager({ maxRunningJobs: asyncMaxJobs })` (static, computed once); async/job-manager.ts at 6962d5cd:148 (option type widens from a number to a number or a function), :285 (the constructor stores the option), :302-306 (getter; floor at :305 `return Math.max(1, Math.floor(value ?? DEFAULT_MAX_RUNNING_JOBS));`); async/job-manager.ts at parent d9bc4fbd:284 (the constructor already floored the cap at 1: `this.#maxRunningJobs = Math.max(1, Math.floor(options.maxRunningJobs ?? DEFAULT_MAX_RUNNING_JOBS));`); commit authored 2026-09-24T18:04:41Z, committed 2026-09-24T19:09:05Z; sha256 sdk.ts@6962d5cd 84f3a112a670f36de9c030756f4babc0ad83e37efeca99154ea4d4263423e633, sdk.ts@parent fde5a959e3a310be1d9fd291163dd817d2328d2b5a2012697b75b3205d592104, job-manager.ts@6962d5cd f8851470a8bd953f25ab659c0d0aac2ea8c34df9a433e154ec4127c7683b70bd, job-manager.ts@parent c417f63c7686e19ef9a0a658519de843e87dede6e23f73ee3ef1583f95e61aaf | supersedes S140 — the old row taught that the explicit floor can vanish in the rewrite and cited only the sdk clamp site, so read alone it says the cap lost its floor of 1; the bytes say the opposite: the sdk site's own Math.max(1, …) vanished (parent sdk.ts:1797 — sdk.ts:1949) while the cap's floor of 1 stayed, because the manager already floored it at construction (parent job-manager.ts:284) and this commit moved that floor into a per-check getter (job-manager.ts:302-306). The clamp site is not immutable; the floor can move from the call site to the consumer without the cap ever losing it | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md, corpus/lessons/round-28.md |
```

Cells: 13 fields, no `|` inside cells, `teaches` opens `supersedes S140 — ` (em dash U+2014), status `mined`, `recheck on-release`, `opened 2026-10-22`. Scope/anchor/teaches corrected per the Low-1 finding and the byte check. The `teaches` differs from S140's (counter `teaches_unchanged` check passes).

## 4. Gate line (round-28 lesson `## Gate`)

| Row | URL | Accessed | Located quote (verbatim, ≤25 words) | Decision |
|---|---|---|---|---|
| S152 | https://raw.githubusercontent.com/can1357/oh-my-pi/6962d5cd2ef157ebf9f415acd58b8744f66400d8/packages/coding-agent/src/async/job-manager.ts | 2026-10-22T17:59:30Z | `job-manager.ts:305` "return Math.max(1, Math.floor(value ?? DEFAULT_MAX_RUNNING_JOBS));" (5 words) | admit, A, mined (sha256 `f8851470a8bd953f25ab659c0d0aac2ea8c34df9a433e154ec4127c7683b70bd`) |

The counter requires the line to carry an https URL, a 64-hex sha256 and a quoted span; the sha256 is in the Decision cell.

## 5. Used-by conflict (assignment vs counter)

The assignment says used-by = "the files that cite S140 today" (`git grep -n 'S140' 6ebd518f -- corpus SKILL.md PROVINCE.md`): `corpus/SOURCES.md:146`, `corpus/knowledge/harness-job-capacity-r25.md:1,277,330`, `corpus/lessons/round-27.md:80,128`, `corpus/lessons/round-27-verifier-spotcheck.md:151`. The amended counter (`count-c1.sh`) requires each used-by path to contain the **new** id `S152` as a word at `<rev>` (`git grep -q -w -F S152`), and the census E11 requires the paths to exist. The history lessons (`round-27.md`, `round-27-verifier-spotcheck.md`) cite S140 as history and cannot be repointed, so listing them fails: measured `fail S152 used_by_not_citing=corpus/lessons/round-27.md,corpus/lessons/round-27-verifier-spotcheck.md`. The counter-clean used-by is `corpus/knowledge/harness-job-capacity-r25.md, corpus/lessons/round-28.md` — the two files that will cite S152 after the sweep (knowledge entry repointed; round-28.md Gate). **Requires the L1 to create `corpus/lessons/round-28.md` in the same batch** (E11 fails otherwise). Also move S140's own `used-by` (mutable cell) to `corpus/lessons/round-27.md` and log old→new in the round-28 lesson.

## 6. QUALITY 77 sweep — places stating the defective wording

Live surfaces (must carry the corrected wording at the correction commit):
1. `corpus/knowledge/harness-job-capacity-r25.md:281-283` — U1 head clause "the explicit floor `Math.max(1, …)` did not survive that rewrite — neither the clamp expression nor the accessor (`tools/settings.ts:941-946`) carries a floor at v18.12.6." → apply ReopenS140 Low-1 old→new (add "clamp site's … the manager getter's own floor stayed; F3").
2. `corpus/knowledge/harness-job-capacity-r25.md:330` — same wording in the round-27 corrections log; answer with a dated correction block in the round-28 lesson (not a rewrite of the closed log).
3. `corpus/SOURCES.md:146` — S140 row's `teaches` ("the explicit floor can vanish in the rewrite"): frozen by QUALITY 81; corrected by the superseding row S152 (not edited in place).
4. `corpus/knowledge/harness-job-capacity-r25.md:1,277,330` — must be repointed S140 → S152 (readers_left check), the S140 row's own used-by moved to the history lesson.

Records (keep as history; log the correction in the round-28 lesson): `corpus/lessons/round-27.md:80,116,128`; `corpus/lessons/round-27-verifier-spotcheck.md:151`; `.ufo/waves/round-27/w1/ReviewR7Knowledge.md:15-20,60-71`; `.ufo/waves/round-27/w2/ReopenS140.md:110-111,121,138-143`; `.ufo/waves/round-27/w2/ReviewHygieneR7.md:96,110-114,120-127`.

## 7. Falsifications (sandbox clones in `/fast/scratch/hyaku/mori-r28/MoriR28.SupersedeS140/`; lane untouched)

- Census `sources-census.sh validate --today 2026-10-22 <scratch>/<lane>` on the row: exit 0, same six pre-existing W04 lines, no new finding (checked on `sandbox`, `sim3`, `final`, `final2`, `final3`).
- Row-identity (`LANE` repointed, single-commit insert): `rows=145 changed=3 removed=0 bad=0` — S152 is a new id (no diff), S140 not flagged (its used-by moved only in the mutable cell).
- Amended counter (`LANE` repointed to the sim with row + sweep + lesson): `superseding=1/8 ids=S140`, no `fail S152` line; the other seven ids report `row_absent` (other seats), `readers_left=25` (other ids' readers; S140-specific readers = 0 after the sweep).
- Counter with the assignment-literal used-by: `fail S152 used_by_not_citing=corpus/lessons/round-27.md,corpus/lessons/round-27-verifier-spotcheck.md`.

## 8. Bounds, tools, installs

Lane writes: this report file only. No `git add/commit/stash/checkout/switch/reset/pull/push` in the lane; only read-only `git log/show/grep/rev-parse/cat-file` and `git clone --no-hardlinks` into scratch. No jj command ran. Fetches: plain `curl -f` only, no bot challenge. Tools: `curl`, `sha256sum`, `python3 -I -B`, `gawk` (via the census script), read-only `git`. **No installs or upgrades** (nothing needed; pacman transactions paused host-wide). Privacy: no OMP settings values, session ids, pids, uids, unit names or journal text; upstream code quotes, digests, line numbers and counts only.

## 9. Findings

- The S140 row is byte-identical to its first publication; the routed defect (ReopenS140 Low-1) is a wording/prose defect that QUALITY 81 requires to be corrected by a superseding row (done by S152).
- Byte-verified correction: the cap's floor of 1 never vanished — the manager already floored it at construction before this commit (parent `job-manager.ts:284`) and the commit moved that floor into a per-check getter (`job-manager.ts:302-306`); only the sdk clamp site's own `Math.max(1, …)` vanished.
- The r27 ReopenS140 report's Low-1 rationale says the commit "added an explicit Math.max(1, …) floor to the job-manager getter" — imprecise: the manager's floor pre-existed at the parent (constructor); the commit relocated it. The L1 should use the corrected phrasing (S152 carries it).
- Used-by conflict reported in §5: the assignment-literal list fails the amended counter; the counter-clean list requires `corpus/lessons/round-28.md` to exist when the row lands.
- Out of scope: S145–S151 (other seats), the three restores (S096/S097/S101), the counter script and the round-28 lesson content (L1's editing).
