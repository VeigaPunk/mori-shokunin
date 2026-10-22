# ReopenRejections — re-screen of SOURCES rows S098–S113 (C2's seven rejections and nine admissions)

Seat `MoriR25.ReopenRejections`, round 25 wave 2, 2026-10-22. Leaf seat: no subagents, no background jobs.
Read-only on the lane: **this file is the only lane write**. Scratch bytes live in `/tmp/r25-reopen`
(one sparse clone of tag `v18.12.6` under `/tmp/r25-reopen/omp-tag`, removed after the check). No `jj`, no
git write, no `omp` execution, no settings edit, no install, no `pacman`. Sources opened by ordinary HTTP
(`curl`, GitHub API, one `git clone --depth 1 --sparse`); no headless browser and no attempt at any access
control. All fetches 2026-10-22 between 11:36Z and 11:38Z unless a row states otherwise.

## Verdict

**All seven rejections hold; no admitted row should have been rejected.** Two reasons as written are not
literally true (S111's "no `Background job` text", S109's frozen error-body digest) and one title is
paraphrased (S110); none of the three changes a verdict. All nine admitted rows (S098–S104, S112–S113)
reproduce their anchors, digests and line numbers exactly. Severity of every defect found: low or info.

| Row | Claim under attack | Re-screened result | Agree? | Severity of any defect |
|---|---|---|---|---|
| S105 | rejected, 0 hits, launcher only | HTTP 200; raw README 5,518 B sha `0846b461…` exact; **all 14 repo blobs** have 0 hits; 0 issues | **agree** | none |
| S106 | rejected, no `async:` block | HTTP 200; raw 6,161 B / 111 lines sha `9ae986fc…` exact; 0 `async`, 0 `maxJobs`; keys match scope | **agree** | none |
| S107 | rejected, 0 `maxJobs` on four pages | HTTP 200 ×4; sha prefixes `0902796c…`, `8e95cbb8…`, `e6c0d205…`, `8af7dc4b…` exact; 0 `maxJobs`/`maxRunningJobs` each | **agree** | none |
| S108 | rejected, search summary not page content | HTTP 200; 42,402 B sha `046818a3…` exact; 0 `async*`, 0 `maxJobs`, 0 "background job" | **agree** | none |
| S109 | rejected, HTTP 521, body never opened | **still HTTP 521**; body is a JS anti-bot challenge, no article text | **agree** | low (digest drift) |
| S110 | rejected, issue prose, flip = maintainer answer | HTTP 200; 0 comments, so flip unmet; quote matches word for word | **agree** | low (title paraphrase) |
| S111 | rejected, 0 `maxJobs` **and** no "Background job" text | 0 `maxJobs`/`maxRunningJobs`/`async.maxJobs`/`Background job limit`, **but 29 lowercase "background job"** | **agree on verdict, disagree on wording** | low |
| S098 | admitted, job-manager cap anchors | all eight anchor ranges verified at the pinned sha | agree (admit) | low (truncated sha) |
| S099 | admitted, sole construction + clamp | clamp at :2284, guard at :2282; **exactly one** `new AsyncJobManager` in `src` at the tag | agree (admit) | none |
| S100 | admitted, setting schema | :941–946 exact, no `ui` block | agree (admit) | none |
| S101 | admitted, docs default/floor, no maximum | :593 and :623 exact; only one `maxJobs` mention in the file | agree (admit) | none |
| S102 | admitted, own-work binary | sha and size exact; both byte offsets and both owner comments exact; 1 clamp match, 1 schema match | agree (admit) | none |
| S103 | admitted, "default and maximum 100" | :258 exact; scope sentence and error name present | agree (admit) | none |
| S104 | admitted, introduction commit + history | patch sha `00f6cbb0…` exact; date, subject, first bullet, twin commit, v12.19.0, and the 4-day raise all verified | agree (admit) | none |
| S112 | admitted, bash cap behaviour | :843, :882, :1188–1192, :1220–1229 all exact; tag bytes = commit bytes | agree (admit) | info (tag URL) |
| S113 | admitted, eval cap behaviour | :533–538 exact | agree (admit) | info (tag URL) |

## What was re-opened, and what it says now

### S105 — `github.com/Daxiongmao87/oh-my-pi-termux` — reject stands

- Page HTTP 200 (290,231 B). Raw `README.md` 5,518 B, sha256
  `0846b461000fa46ca95fbcbc390ed8d870a3fb825fb4fa06b504ee98817fe1cf` — **identical** to the row's pin.
- The row's universal claim ("no `maxJobs`/`Background job` text **in any file**") was wider than wave 1's
  check: `SrcRejections.md` §3/C1 greps five files, while the tree has **14 blobs** (`.gitignore`,
  `CHANGELOG.md`, `LICENSE`, `README.md`, `bin/omp`, `ci/tests.yml`, `docs/troubleshooting.md`,
  `docs/update-design.md`, `docs/verification.md`, `install.sh`, `lib/omp_termux.py`,
  `tests/termux-integration.sh`, `tests/test_update.py`, `uninstall.sh`). I fetched all 14:
  `grep -ril -e maxJobs -e maxRunningJobs -e 'background job' -e background-job s105/` → **no file**.
  The row is correct; wave 1 had under-checked, not over-claimed.
- Issues API `?state=all` → 0 items, so "no issue mentions the cap" holds vacuously. The README quote at
  `README.md:6-7` and the version claim (18.12.0 / 18.11.3, `README.md:91`) both verify.
- Flip condition (repo records an observed `Background job limit reached`) is **not** met.

### S106 — gist `sonsu-lee/4d76307b…` — reject stands

- Raw 6,161 B, 111 lines, sha256 `9ae986fcae301544a8af80032ca7e3b40892503540002259fbc041bfcf9e0f3c`
  — exact. Counts: `async` 0, `maxJobs` 0, `maxRunningJobs` 0, "background job" 0. The gist page
  `<title>` is verbatim `omp (oh-my-pi) settings — Codex main, Claude fallback: config.yml, MCP/LSP · GitHub`.
- The scope cell ("model roles, retry fallbacks, task overrides, worktree") matches the file:
  `modelRoles:4`, `retry:33`, `task.agentModelOverrides:82`, `task.isolation:87`, `worktree:109`.

### S107 — four `omp.sh/docs` pages — reject stands

- All four HTTP 200. Digests reproduce the row's prefixes exactly: subagents `0902796c…`, settings
  `8e95cbb8…` (61,904 B; `async` occurs once, as a nav group label), tools `e6c0d205…`, slash `8af7dc4b…`.
- `maxJobs` and `maxRunningJobs`: **0 on every page**. `task.maxConcurrency` occurs twice on the
  subagents page (defaults table), exactly as the row says. "background job" occurs once each on tools
  (`…follow or cancel background jobs…`) and slash (`Shows running and recently settled background jobs.`)
  as capability prose, not a limit; the row does not claim otherwise.

### S108 — DeepSeek integration page — reject stands

- HTTP 200, 42,402 B, sha256 `046818a304e47d9246dc17e29ab0ebc6300f4f4db96ae38c3689db8e0b2b3e0d`
  — exact. It is the real page (`<title>Using DeepSeek with Oh My Pi | DeepSeek API Docs</title>`,
  `Prerequisites` heading present, `models.yml` 7×).
- Token counts on the served bytes: `maxJobs` 0, `async*` 0, "background job" 0. The search summary that
  credited the page with `async.maxJobs` is indeed not page content; the reject's discernment point holds.

### S109 — CSDN blog — reject stands; the pinned error body no longer reproduces

- **HTTP 521 again** on the article URL (2,195 B), on a query-string variant (2,252 B, 521), and a
  2,198 B repeat. The body is an obfuscated JS challenge (`window.onload=setTimeout("cx(197)",200)` …
  `eval("qo=eval;qo(po);")`) with no article text. Per the bounds I did **not** attempt to pass it; the
  page stays unopened.
- Drift: the row records "error body 2,156 B, sha256 `f2ddd654…`". Today three fetches gave 2,195 / 2,198 /
  2,252 B with three different digests (`00cde418…`, `47e45451…`, `0c926e4f…`). The size/digest pair is a
  per-request challenge page, so the recorded anchor is unreproducible. `m.blog.csdn.net` now answers
  **301** (166 B) rather than 521, though it redirects back to the challenged host.
- The reject reason itself ("unreachable, no body, no quotable sentence") is **true today**. Flip is not met.

### S110 — issue #14636 — reject stands

- Issue still `open`, opened `2026-10-06T20:23:29Z`, **0 comments** — the flip ("a maintainer answer states
  the wiring rationale") is **not** met.
- The body's "Description" paragraph matches the row's 12-word quote exactly:
  `` `AsyncJobManager` counts jobs of any kind (`DEFAULT_MAX_RUNNING_JOBS` 15, `async.maxJobs` up to 100) ``.
- The row's subject reads `…"Limit how many heavy commands run at once across subagents"`; the served title
  is `Limit how many heavy commands (cargo, tsc, test runners) run at once across subagents`. The
  parenthetical is dropped without an ellipsis (F3).
- The rejection's substantive point — that the "15" is the fallback for an undefined option — is confirmed
  independently: at tag `v18.12.6` the sparse checkout of `packages/coding-agent/src` contains **exactly
  one** `new AsyncJobManager` (sdk.ts:2283) and it always passes a function, so `DEFAULT_MAX_RUNNING_JOBS`
  is never reached in a shipped session.

### S111 — gradually.ai changelog — reject stands, one reason clause is wrong

- HTTP 200, 1,186,509 B, sha256 `33834e6c8bfb98ff29b21582322f1f3a1fe4af641a43216a176ec310e87d1c74`
  — exact. Header quote exact: `This view shows 112 of 175 recorded entries. Older entries are not loaded
  here.` The v18.12.6 entry is present, dated `October 21, 2026`.
- Counts on the served bytes: `maxJobs` **0**, `maxRunningJobs` **0**, `async.maxJobs` **0**,
  `Background job limit` **0** — the cap is absent, so the reject stands and the flip is unmet.
- **But** the row's clause `no "Background job" text anywhere on the served page (0 hits)` is misleading:
  `background job` occurs **29** times (31 case-insensitively), including `Running agents and background
  jobs in Tern now share one compact counter` and `/jobs kill <id>|all to cancel a running background job`.
  The exact capitalized string is 0, but the page plainly discusses background jobs. (F1)

## Admitted rows — anchor verification (all reproduce)

| Row | Check | Result |
|---|---|---|
| S098 | raw 49,665 B sha `0f37afaa…`; `DEFAULT_MAX_RUNNING_JOBS:43`; queued doc :118–123; option :170–171; getter :330–335 (:331, floor :334); atCapacity :337–346 (:338); count :363–368; check+throw :369–374 (:372 exact text) | all exact |
| S099 | sha `c0228add…`; import :53; `cfgAsyncMaxJobs` import :326; guard :2282 (`!options.parentTaskPrefix`); clamp :2284 (`Math.min(100, cfgAsyncMaxJobs.get(settings))`) | all exact |
| S100 | sha `51497414…`; `cfgAsyncMaxJobs` :941, id :942, protocolDefault :943, type :944, default :945, close :946; no `ui` block | exact |
| S101 | sha `0b2e1457…`; `### Tools and approvals` :593; `async.maxJobs` row :623 with default `100`, "floored to at least 1", no upper bound; single `maxJobs` mention in the file | exact |
| S102 | binary 256,702,432 B sha `85d9daf3…`; clamp match at 164,406,766 (`maxRunningJobs: () => Math.min(100, XPe.get(R))`), schema match at 155,231,590 (`default: 100`), owner comments 164,380,488 / 155,206,756; `--user-agent=omp/18.12.6` at 256,648,593; manifest `version: "18.12.6"` at 151,991,030; 1 match each | exact |
| S103 | sha `fb2fc4a1…`; :258 carries "default and maximum 100", the session-wide sharing list, and "`agent()` fails with `Background job limit reached`" | exact |
| S104 | patch 76,782 B sha `00f6cbb0…`; `Date: Sun, 22 Feb 2026 12:44:23 +0100` = 2026-02-22T11:44:23Z; subject and first bullet exact; added line `const asyncMaxJobs = Math.min(100, Math.max(1, settings.get("async.maxJobs") ?? 15));`; twin `3ce6a683` exists with an identical patch; tag `v12.19.0` (commit `0dddac8e`, 2026-02-22T14:35:13Z) carries the clamp at sdk.ts:726; the raise is `944d7f8d` (2026-02-26T11:34:29Z, `default: 15 → 100`, `?? 15 → ?? 100`) — four days later, as taught | exact |
| S112 | sha `d985ef25…`; `#startManagedBashJob` :843; `manager.register` :882; explicit branch :1188–1192 (manager-presence check only, no `atCapacity`); auto-background guard :1220–1229 includes `!autoBgManager.atCapacity` | exact |
| S113 | sha `01e9c5c5…`; :533 `autoBgManager`; :534–535 comment; :536–538 `… || autoBgManager.atCapacity) { return await run(...) }` | exact |

Tag cross-check: `git ls-remote https://github.com/can1357/oh-my-pi refs/tags/v18.12.6*` →
`45c35e40c46166dc726ccc52f5d27f40f2449f99`, and the tag-URL bytes equal the commit-pinned bytes
(`bash.ts` `d985ef25…`, `eval.ts` `01e9c5c5…`).

## Findings

**F1 — S111's rejection reason overstates its 0-hit claim. (severity: low; verdict unaffected.)**
`corpus/SOURCES.md` S111 teaches cell says `no "Background job" text anywhere on the served page (0 hits)`.
Measured: `Background job` (capital B) 0, `background job` 29, `job` 136, `/jobs kill` present. Smallest fix:
replace that clause with `0 hits for maxJobs, async.maxJobs and "Background job limit"; the page discusses
background jobs generically but states no cap`.

**F2 — S109's pinned error-body size and digest do not reproduce. (severity: low; verdict unaffected.)**
Row: `error body 2,156 B, sha256 f2ddd654…`. Observed today: 2,195 / 2,198 / 2,252 B with three other
digests; `m.blog.csdn.net` now 301, not 521. The HTTP 521 and the "unopened, JS challenge" reason are true.
Smallest fix: drop the digest and write `HTTP 521, JS anti-bot challenge body ~2.1–2.3 KB (digest varies per
request)`.

**F3 — S110's subject drops part of the real issue title. (severity: low.)**
Row: `"Limit how many heavy commands run at once across subagents"`. Served:
`Limit how many heavy commands (cargo, tsc, test runners) run at once across subagents`. Smallest fix:
restore the parenthetical or mark the elision with `…`.

**F4 — S098 records a 16-hex sha256 prefix where every sibling records 64. (severity: low.)**
The prefix `0f37afaaa822ef1d` is correct; the full digest is
`0f37afaaa822ef1de845b8eb21473a70210176ff61e2dcff5925f85ec0e544e7`. Smallest fix: record the full digest.

**F5 — rendered-HTML digests on rejected rows are not reproducible. (severity: info; rejected rows carry no
claim, so nothing rests on them.)** S105 HTML `a61566e4…`/290,225 B is now `e06ffd0b…`/290,231 B; S106 HTML
183,727 B is now 183,732 B; S110 HTML `2060061d…` is now `e27cfaa6…`. Raw digests reproduce exactly. Smallest
fix: pin raw bytes and titles for such rows, not the served HTML digest.

**F6 — S112/S113 pin the tag URL, not the commit. (severity: info.)** Tags can be moved upstream; the
recorded sha256 still catches a change, and today `v18.12.6` = `45c35e40`. Optional smallest fix: use the
commit URL as S098–S100 do.

**No wrong admissions.** Each admitted row carries the fact it claims, at the line range it claims, with a
digest that reproduces. None belongs at a lower tier or under a rejection: S098–S100, S103, S112, S113 are
upstream code/docs at the exact tag; S101 is the same tag's reference; S102 is an own-work byte read of the
installed binary (the S034 precedent); S104 is the primary introduction commit plus a verified history claim.

## Unrun / unresolved

- `archive.org` availability lookup for S109 returned **HTTP 429** twice; no archived copy was tested. If an
  archived body exists, the reject still stands on the served-URL rule, but the flip could be re-screened
  from the archive at tier C.
- The S104 history check sampled the introduction, the raise, the twin commit and tag `v12.19.0`; it did not
  walk every tag between v12.19.0 and v18.12.6 for a second change to the fallback.
- No tool installs or upgrades were made; no pacman transaction was attempted.
