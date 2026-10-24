# ReopenDocsAndCommit: S101, S103, S104 re-opened by ordinary fetch (round 25, wave 2)

Scope: re-open S101 (docs/settings.md), S103 (docs/tools/eval.md) and S104 (commit 476b858) by ordinary fetch; verify quotes, anchors and dates; test the claim that the 100 ceiling dates from the feature's first commit, against the patch text. Agree or disagree per row.

Lane: read-only. Lane HEAD read as `07a31ae8e22514bbc603afa13f2de7c8b2424cca` (not `28b79d3d`). Only this file was written in the lane. Downloads and listings are in `/fast/scratch/hyaku/mori-r25/w2-ReopenDocsAndCommit` (1.6 MB).

## Verdicts

| Row | Verdict | Basis |
|---|---|---|
| S101 docs/settings.md | **Agree, with two amendments** | Quote, anchors (593, 623), sha256 and "default 100, floor 1, no ceiling stated" all match the tag. Disagree with "docs and code disagree": the page is silent on a ceiling, and the eval page at the same tag states one. The row itself was first committed 2026-09-30, not at the feature date. |
| S103 docs/tools/eval.md | **Agree, with one amendment** | Line 258 and every quoted phrase match verbatim; sha256 and size match. The wording was first committed 2026-10-06. |
| S104 commit 476b858 | **Agree, with notes** | Commit, author date, patch sha256, quoted sdk.ts line, subject and first bullet all match. The 100 ceiling is an added line in this patch, so it dates from the feature's first commit. "Raised four days later" is correct by calendar date (2026-02-26). The twin split is exactly at v15.1.9, as stated. "First release tag v12.19.0" holds for the twin lineage only. |
| Knowledge U1, "only the default moved (15 to 100)" (not a row; rests on S104) | **Disagree** | The ceiling (100) and floor (1) values held. But the UI range text "(1-100)" was removed on 2026-05-03, and the clamp was rewritten on 2026-09-24. The fallback moved together with the default in one commit. |

## Findings (severity; smallest fix)

1. **Medium.** Knowledge U1 says "only the default moved (15 to 100)". That is wrong (timeline below). Fix: replace with "The default and the sdk fallback moved 15 to 100 on 2026-02-26 (944d7f8d). The UI range text '(1-100)' was removed on 2026-05-03 (e398f831). The clamp was rewritten on 2026-09-24 (6962d5cd, c4a2441d). The value 100 and the floor 1 held to v18.12.6."
2. **Low.** S101 says "so docs and code disagree for values above 100". That overstates it. Fix: "The settings reference states the default and the floor but no ceiling. The code clamps at 100 (sdk.ts:2284 at v18.12.6). The eval reference at the same tag states the ceiling (S103)."
3. **Low.** S101 has no date for its row. Fix: add "the `async.maxJobs` row was first committed 2026-09-30 (1b3222187919)".
4. **Low.** S103 has no date for its wording. Fix: add "'(default and maximum 100)' and the refusal sentence first committed 2026-10-06 (ee690a93e91a); the 'shared with every other background job' sentence first committed 2026-10-06 (7fe31da5f772)".
5. **Low.** S104 "four days later" is a calendar statement. Elapsed time from the feature's author time is 3 d 23 h 50 m. Fix: "raised 2026-02-26 (944d7f8d8d44)".
6. **Low.** S104 "first release tag carrying the clamp v12.19.0" is true for the twin lineage only. On the main lineage, which v18.12.6 descends from, the first release carrying the feature is v15.1.9 (2026-05-21). Fix: add "(twin lineage; main lineage first ships it in v15.1.9)".
7. **Low.** S104 gives no anchor for the quoted line. Fix: add "sdk.ts new-file line 726 (patch line 1016; hunk `@@ -715,6 +722,55 @@`)".

None of these changes an 18.12.6 fact that C2 uses (clamp 100, default 100, sdk.ts:2284, tools/settings.ts:945) or the C2 after-value.

## Evidence

### S101: docs/settings.md

- Fetched raw at `45c35e40c46166dc726ccc52f5d27f40f2449f99`: 148,359 bytes; sha256 `0b2e1457021fa526f2c35015672f1d7ccbac95e7b9f217528ab8022c55ed5883`. Matches the row.
- Line 593 is `### Tools and approvals` (raw read of lines 591 to 594).
- Line 623, exact text: `| \`async.maxJobs\` | number | \`100\` | Running background-job cap, floored to at least 1; parked/queued jobs do not consume execution slots. |`. Matches the knowledge F1 quote.
- Case-sensitive scan of the whole file for `maxJobs|maximum 100|Background job limit|background-job cap`: only line 623 matches. No ceiling sentence.
- Code at the same tag, for the "code clamps it" half:
  - `packages/coding-agent/src/sdk.ts:2284`: `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)),` (file sha256 `c0228add…`).
  - `packages/coding-agent/src/tools/settings.ts:941-946`: `cfgAsyncMaxJobs` registered with `default: 100` at line 945 and no description (file sha256 `51497414…`).
  - `packages/coding-agent/src/async/job-manager.ts:334`: `return Math.max(1, Math.floor(value ?? DEFAULT_MAX_RUNNING_JOBS));` (file sha256 `0f37afaa…`).
- Date: the first commit containing the row is `1b3222187919` ("chore: updated docs", author 2026-09-30T17:57:16Z, committer 17:58:43Z, 138 files). Linear check over all 226 commits that touch the file: the row is present in 72 of them, first at index 154 (1b322218), absent in every earlier commit, and present in every later one. The previous commit touching the file by author date (`ea0952609fb4`) has no `maxJobs` text at all.

### S103: docs/tools/eval.md

- Fetched raw at the tag: 28,027 bytes; sha256 `fb2fc4a139ba187f1cc062fab53bd72a48dd13b1f81f0c3318ec7a79d41e495c`. Matches.
- Line 258 (the bullet "Eval subagent spawning obeys …") contains, verbatim:
  - "every handle is a running background job counted against the session-wide `async.maxJobs` cap (default and maximum 100)"
  - "which it shares with every other background job in the session, including async `bash`, async `task` spawns, `workpool()` pools and nested subagents' jobs"
  - "`agent()` fails with `Background job limit reached` once that cap is full."
- Only line 258 matches `maxJobs|maximum 100|Background job limit` in the file.
- Dates, from a linear check of all 54 commits that touch the file:
  - "(default and maximum 100)" and the refusal sentence first appear in `ee690a93e91a` (author 2026-10-06T19:57:40Z, "docs(coding-agent): correct agent() and workpool concurrency limits in eval docs").
  - "shares with every other background job" first appears in `7fe31da5f772` (2026-10-06T21:11:21Z, "docs(coding-agent): note that async.maxJobs is shared across background jobs").
  - The feature commit touches no docs/ file.

### S104: commit 476b858b3a4abe6f6c8a06c252c23961be41e912

- Patch (`github.com/can1357/oh-my-pi/commit/476b858….patch`): 76,782 bytes; sha256 `00f6cbb0b786dd8416e3c764d90e51b159bde6873bd1f7e955f5fd847b571257`. Matches.
- API: author 2026-02-22T11:44:23Z, committer 2026-02-22T11:44:57Z, parent `8a49f11110af4d3bc379df2711eb95ed7b550388`.
- Subject matches: "feat(coding-agent): added async background job execution with configurable concurrency limits". First bullet matches: "- Added async background job execution for bash and task tools with configurable concurrency limits and automatic result delivery."
- Quoted line matches exactly: `+	const asyncMaxJobs = Math.min(100, Math.max(1, settings.get("async.maxJobs") ?? 15));`. It is at patch line 1016 and sdk.ts new-file line 726 (hunk `@@ -715,6 +722,55 @@`, patch line 1011).
- Same commit, other lines:
  - `config/settings-schema.ts` adds `"async.maxJobs"` with `default: 15,` and `description: "Maximum concurrent background jobs (1-100)"` (patch lines 464 to 470).
  - `async/job-manager.ts` is a new file, with `const DEFAULT_MAX_RUNNING_JOBS = 15;` (line 113) and the refusal `Background job limit reached (${this.#maxRunningJobs}). …` (line 184).
- Ceiling origin: no commit before this one carries `async.maxJobs`, the clamp, or `job-manager.ts`. The 100 ceiling is an added line here. **Agree** that it dates from the feature's first commit.
- Twin `3ce6a68380f11d6ba3c32133d1660bd58a3bb346`:
  - Identical author and committer times.
  - Patch identical to 476b858 except the `From` header line (a full `diff` of the two patch files shows one changed line).
  - Its parent `818a2d561d1bc744a10929636f3569cc1b8b79b0` and 476b858's parent are also twins: same subject, both authored 2026-02-22T11:01:26Z.
- Lineage, from `compare` calls against all 593 tags dated on or after 2026-02-01:
  - 3ce6a683 is an ancestor of every tag from v12.19.0 through v15.1.8 (all 178 tags in that window). It is an ancestor of none from v15.1.9 on.
  - 476b858 is an ancestor of every tag from v15.1.9 on (fe5b96e8a1ce, 2026-05-21T04:24:41Z). It is an ancestor of none before.
  - The split is exactly at v15.1.9, as the row says.
- Release: v12.19.0 (commit `0dddac8e`, committed 2026-02-22T14:35:13Z; release published 14:49:15Z) carries the clamp at sdk.ts:726. The previous tag v12.18.3 (2026-02-21T22:15:03Z) has neither `asyncMaxJobs` nor `async.maxJobs`.
- Raise: `944d7f8d8d44` ("feat(coding-agent): increased async max jobs limit to 100 for concurrency", author 2026-02-26T11:34:29Z) changes `default: 15` to `default: 100` in settings-schema.ts and `?? 15` to `?? 100` in sdk.ts. Twin lineage: the sdk fallback is still `?? 15` at tag v13.3.4 (committed 2026-02-26T10:54:40Z) and `?? 100` at v13.3.5 (2026-02-26T11:43:21Z). The settings default is 15 at v12.19.0 and 100 at v15.1.8.

### Dates

| When (UTC) | What | Commit or tag |
|---|---|---|
| 2026-02-22 11:44:23 (committed 11:44:57) | Feature: default 15, fallback 15, "(1-100)" description, clamp `Math.min(100, …)` | 476b858b3a4a (twin 3ce6a68380f1) |
| 2026-02-22 14:35:13 (published 14:49:15) | First tag carrying the clamp, on the twin lineage | v12.19.0 (0dddac8e) |
| 2026-02-26 11:34:29 | Default 15 to 100 and fallback 15 to 100 (main lineage) | 944d7f8d8d44 |
| 2026-02-26 10:54:40 to 11:43:21 | Fallback 15 to 100 (twin lineage) | v13.3.4 to v13.3.5 |
| 2026-05-03 05:09:09 | UI block with "(1-100)" description removed; default 100 kept | e398f8316372 |
| 2026-05-21 04:24:41 | First main-lineage tag carrying the feature | v15.1.9 (fe5b96e8) |
| 2026-09-24 18:04:41 | config/settings-schema.ts removed; clamp becomes a function with `?? 100` | 6962d5cd2ef1 |
| 2026-09-24 23:02:43 | `?? 100` dropped from the function | c4a2441d8f91 |
| 2026-09-30 17:57:16 | docs/settings.md gains the `async.maxJobs` row | 1b3222187919 |
| 2026-10-06 19:57:40 and 21:11:21 | eval.md gains "(default and maximum 100)", then the "shared" sentence | ee690a93e91a, 7fe31da5f772 |
| 2026-10-21 20:49:59 | Tag v18.12.6 | 45c35e40c461 |

## Timeline for rewriting knowledge U1 (main lineage)

- 476b858: default 15; fallback 15; description "(1-100)"; clamp `Math.min(100, Math.max(1, … ?? 15))`; manager gets a static number.
- 944d7f8d: default 100; fallback 100. Clamp value unchanged.
- v15.1.9: clamp `Math.min(100, Math.max(1, … ?? 100))`; static `maxRunningJobs: asyncMaxJobs`.
- 6962d5cd: `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings) ?? 100)`. Its parent d9bc4fbd still has the static form.
- c4a2441d: `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings))`. Unchanged at v18.12.6 (sdk.ts:2284).
- Unchanged to v18.12.6: the ceiling 100 in the clamp; default 100 (tools/settings.ts:945); floor 1 enforced by the manager (job-manager.ts:334). The sdk-level `Math.max(1, …)` and the `?? 15` fallback are gone by the tag.

## Limits and residual risk

- The docs histories were scanned linearly, over every commit that touches each file. The settings and sdk transitions come from a binary search over commits ordered by author date. Each "first" commit is sound only if the state is monotone in that order. Committer dates are not in parent-child order (for example, parent d9bc4fbd was committed 2026-09-24T19:09:04Z, while its child 6962d5cd was authored 18:04:41Z). So "first" means first by author date.
- Not checked: every sdk.ts commit between 2026-05-21 and 2026-09-24. The clamp line was verified only at v15.1.9 and at 6962d5cd's parent. Also not checked: the twin lineage's settings default at v13.3.5 (only the sdk fallback), and later docs wording beyond the first-appearance dates.
- The twin-versus-feature patch comparison used `diff`, not a patch application.
- Upstream sources were read, not executed. The omp binary was not read (out of scope for this seat).
- GitHub API quota: 2,404 of 5,000 core requests remained at my last check (reset epoch 1792672603).

## Tooling record

- Installed or updated: nothing.
- Existing tools used: gh 2.102.0 (`~/.local/bin/gh`, authenticated), curl 8.23.0, jq, python3 3.14.8, git 2.56.0 (read-only subcommands only).
- Read `~/.omp/agent/RULES.md` first. Its tooling directive required no install here.
- Fetch methods: raw.githubusercontent.com (tag commit and tag names); github.com `.patch` and `.diff`; api.github.com through `gh api` (GET only); urllib for raw bodies.
- No headless browser. No bot challenge met. No source left unopened.
- No subagents, no background jobs, no jj, no git writes in the lane.
