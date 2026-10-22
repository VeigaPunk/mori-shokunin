# SrcRejections — rejected-candidate rows for C2 (claim: `omp` caps background jobs at `min(100, async.maxJobs)`)

Seat `MoriR25.SrcRejections`, round 25 wave 1, 2026-10-22. Read-only seat (leaf: no subagents
dispatched, no background jobs). Lane writes: **this file only**. Scratch bytes live in `/tmp`
(`/tmp/manifest/`, `/tmp/omp-src/`). No `jj`/`git` write in the lane, no `omp` execution, no
settings edits, no `pacman`/install. Contract read first:
`.ufo/waves/round-25/contract.md` (landed `7634be75c74891b5cd2815d0bd5374f89abd7087`), C2 section.

`corpus/SOURCES.md` was **not** edited. Row shapes below follow the rejected-row shape already in
that file (see `S030`, `S055`, `S057`, `S059`, `S061`, `S063`, `S065`, `S072`, `S097`): the `teaches`
cell carries `REJECTED: <reason>; flip: <condition>` and `status` is `rejected`.

---

## 1. What the claim needs from a source

The C2 claim decomposes into four separable facts, so a candidate can support one and fail another:

| Part | Fact a source must carry |
|---|---|
| A | the **configured** value comes from `async.maxJobs` in `~/.omp/agent/config.yml` |
| B | a **ceiling of 100** is applied to whatever is configured (`Math.min(100, …)`) |
| C | the value is **floored at 1** and **queued/parked jobs hold no slot** |
| D | the observable error text when the cap is hit (`Background job limit reached (N). …`) — **scoped**: the throw comes from `AsyncJobManager.register()`; two production consumers pre-check `atCapacity` and fall back to foreground execution instead of throwing (see §5.6) |

A candidate that names a job *limit* but not its *ceiling* supports neither B nor A; a candidate
that states a *default* of 100 supports only the default, which is not the same fact as a ceiling.

---

## 2. Verdict summary (18 candidates opened)

| # | URL | HTTP | Access (UTC) | Verdict | One-line reason |
|---|---|---|---|---|---|
| C1 | `https://github.com/Daxiongmao87/oh-my-pi-termux` | 200 | 2026-10-22T10:06:29Z | **reject** | Termux launcher/updater for upstream omp; no job-limit text anywhere in the repo |
| C2 | `https://gist.github.com/sonsu-lee/4d76307bc70d6696c8336855ac292d3e` | 200 | 2026-10-22T10:06:30Z | **reject** | a user's `config.yml` with no `async:` block and no limit statement |
| C3 | `https://raw.githubusercontent.com/can1357/oh-my-pi/v18.12.6/docs/tools/eval.md` | 200 | 2026-10-22T10:06:30Z | **ADMIT** (tier A docs) | official doc at the tag states the cap's **default and maximum 100** |
| C4 | `https://raw.githubusercontent.com/can1357/oh-my-pi/v18.12.6/docs/settings.md` | 200 | 2026-10-22T10:06:30Z | reject *as evidence of B* (row itself already proposed as S101 by `MoriR25.UpstreamTagLocate`) | documents default 100 + floor 1, states **no maximum** |
| C5 | `https://omp.sh/docs/subagents` | 200 | 2026-10-22T10:06:31Z | reject | official docs site page; no `async.maxJobs` entry, only `task.maxConcurrency` 32 |
| C6 | `https://omp.sh/docs/tools` | 200 | 2026-10-22T10:06:31Z | reject | tool index; "background jobs" appears as a tool capability, not a limit |
| C7 | `https://omp.sh/docs/settings` | 200 | 2026-10-22T10:08:22Z | reject | settings index lists `async` as a group label only; no value, no `maxJobs` |
| C8 | `https://omp.sh/docs/slash` | 200 | 2026-10-22T10:06:31Z | reject | slash-command reference; no job-limit statement |
| C9 | `https://api-docs.deepseek.com/quick_start/agent_integrations/oh_my_pi/` | 200 | 2026-10-22T10:06:31Z | reject | search summary claimed it states `async.maxJobs`; the served page contains **no** such text |
| C10 | `https://inferri.com/en/projects/cmm7hxszc00eds4x78kzz5fi6` | 200 | 2026-10-22T10:06:31Z | reject | third-party project page, no version pin, no citation |
| C11 | `https://blog.csdn.net/gitblog_01054/article/details/164872117` | **521** | 2026-10-22T10:06:33Z | reject | unreachable on three URL variants; article body never opened |
| C12 | `https://github.com/can1357/oh-my-pi/issues/14636` | 200 | 2026-10-22T10:06:34Z | reject | user issue prose; corroborates, adds no fact over the code rows |
| C13 | `https://github.com/can1357/oh-my-pi/pull/14634` | 200 | 2026-10-22T10:06:35Z | reject | PR description; the same sentence is **merged upstream prose** (→ C3) |
| C14 | `https://github.com/can1357/oh-my-pi/issues/14967` | 200 | 2026-10-22T10:06:36Z | reject | different bug (per-session manager ownership); no limit statement |
| C15 | `https://www.gradually.ai/en/changelogs/omp/` | 200 | 2026-10-22T10:06:36Z | reject | release list; zero occurrences of `maxJobs` even for the v18.12.6 entry |
| C16 | `https://vietbui.mintlify.app/entities/omp` | 200 | 2026-10-22T10:06:37Z | reject | third-party "LLM Wiki" entity page mirroring the tool list |
| C17 | `https://deepakness.com/blog/omp-setup/` | 200 | 2026-10-22T10:06:37Z | reject | personal setup blog; no job-limit statement |
| C18 | `https://pi.dev/packages/omp-oracle` | 200 | 2026-10-22T10:06:37Z | reject | third-party plugin page; the served HTML contains **zero** occurrences of `100` |

(C1 and C2 are the two candidates named in my assignment; C3–C18 are the "blog/doc page that
states an omp job limit" population that the search surfaced and that I screened.)

---

## 3. Per-candidate detail

### C1 — `https://github.com/Daxiongmao87/oh-my-pi-termux` — REJECT

- **Access date:** 2026-10-22 (page 10:06:29Z; raw README 10:06:30Z). **HTTP status:** 200
  (HTML 290,225 B, sha256 `a61566e45a1a344daac12ba0aa2c2cef1c871ae5aebc6a686f70b9646c571767`;
  raw README 5,518 B, sha256 `0846b461000fa46ca95fbcbc390ed8d870a3fb825fb4fa06b504ee98817fe1cf`).
- **What it does support:** that upstream `omp` can be launched unmodified on ARM64/Termux via
  `glibc-runner`; it pins upstream releases **18.12.0 and 18.11.3**, not 18.12.6.
- **What it does not support:** parts A–D of the claim. `grep -i -E "maxJobs|maxRunningJobs|Background
  job limit|background job"` over `README.md`, `docs/verification.md`, `docs/troubleshooting.md`,
  `docs/update-design.md` and `install.sh` returns **0 hits**; the repository's issue list is empty
  (GitHub API `issues?state=all` → 0 items).
- **Quote (16 words, README.md:6-7):** `This is a community launcher and updater, not an upstream fork or a native Android rebuild.`
- **Verdict: reject.** A launcher wrapper for the upstream binary carries no statement of the
  background-job cap; the binary it installs is the same upstream artifact the own-work row already
  covers.
- **Flip:** the repo documents the observed failure text `Background job limit reached (N)` under
  `glibc-runner` on ARM64 (the explicit-async registration path; the auto-background path falls back
  to foreground instead — §5.6), or prints its effective `async.maxJobs` in `/settings` — then admit
  as an own-work cross-architecture observation row (tier C), not as a source for the ceiling.

### C2 — `https://gist.github.com/sonsu-lee/4d76307bc70d6696c8336855ac292d3e` — REJECT

- **Access date:** 2026-10-22 (page 10:06:30Z; raw 10:06:30Z). **HTTP status:** 200
  (HTML 183,727 B; raw 6,161 B, sha256 `9ae986fcae301544a8af80032ca7e3b40892503540002259fbc041bfcf9e0f3c`).
- **What it does support:** a real-world `config.yml` for `omp` (Codex-main/Claude-fallback model
  roles, `retry.fallbackChains`, `task.agentModelOverrides`, `task.isolation`, `worktree`, `lsp`).
- **What it does not support:** parts A–D. The file contains **no `async:` block at all**
  (`grep -c -E "maxJobs|maxRunningJobs|async"` → 0), so it neither states a configured cap nor a
  ceiling; its silence is evidence about *that user's* config only.
- **Quote (13 words, gist page `<title>` element, verbatim including the trailing `· GitHub`):** `omp (oh-my-pi) settings — Codex main, Claude fallback: config.yml, MCP/LSP · GitHub`
- **Verdict: reject.** A third-party user's configuration file is not a source for a product limit;
  admitting it would turn one person's settings into a claimed default.
- **Flip:** the author adds an `async:` block with `maxJobs:` and reports the resulting
  `Background job limit reached (N)` — then admit as a tier-C "real-world configured ≠ effective"
  note, still not as the source of the ceiling.

### C3 — `https://raw.githubusercontent.com/can1357/oh-my-pi/v18.12.6/docs/tools/eval.md` — **ADMIT** (candidate)

- **Access date:** 2026-10-22T10:06:30Z. **HTTP status:** 200 (28,027 B,
  sha256 `fb2fc4a139ba187f1cc062fab53bd72a48dd13b1f81f0c3318ec7a79d41e495c`; tag URL and `main`
  URL bytes identical — `main` fetched separately, same digest).
- **What it supports:** **part B (the ceiling)** in official upstream prose at the *exact* tag that
  the installed binary was built from, plus part C's scope ("session-wide", shared with async
  `bash`, async `task` spawns, `workpool()` pools and nested subagents) and part D (the error text).
  This is the only prose I found that states a **maximum**, not merely a default.
- **Quote (17 words, `docs/tools/eval.md:258`):** `every handle is a running background job counted against the session-wide \`async.maxJobs\` cap (default and maximum 100)`
- **Second quote (12 words, same line):** `` `agent()` fails with `Background job limit reached` once that cap is full. ``
- **Verdict: admit** — tier A docs, pinned to tag `v18.12.6`, scope limited to *what upstream
  documents about the cap* (it does not state the `Math.min` expression; the code row does).
- **Flip (for a future re-screen):** upstream deletes or rewrites that sentence — then the ceiling
  rests on the code rows only and this row must be re-scoped to the *scope* sentence ("session-wide,
  shared with every other background job in the session").

### C4 — `https://raw.githubusercontent.com/can1357/oh-my-pi/v18.12.6/docs/settings.md` — REJECT *as evidence of the ceiling*

- **Access date:** 2026-10-22T10:06:30Z. **HTTP status:** 200 (148,359 B, sha256
  `0b2e1457021fa526f2c35015672f1d7ccbac95e7b9f217528ab8022c55ed5883`; `main` bytes identical —
  same digest from a separate fetch).
- **What it supports:** part A (the setting name and its place in the settings tree), the default
  **100**, and part C ("floored to at least 1; parked/queued jobs do not consume execution slots").
- **What it does not support:** part B. The row says "floored to at least 1" and says nothing about
  an upper bound, so a reader of this page alone would predict a configured `async.maxJobs: 200`
  gives 200 running jobs — which is false at this tag (the source clamps at 100).
- **Quote (18 words, `docs/settings.md:623`):** `` | `async.maxJobs` | number | `100` | Running background-job cap, floored to at least 1; parked/queued jobs do not consume execution slots. | ``
- **Verdict: reject** for the clamp claim (it supports the default and the floor, not the ceiling).
  **Overlap note:** `MoriR25.UpstreamTagLocate` already proposes this exact file as **S101** with
  `status = mined`; that proposal is about the *documented default and floor*, which this row
  confirms — the rejection here is only about using it as evidence for the 100 ceiling.
- **Flip:** upstream documents the ceiling in this table (e.g. "capped at 100") — then this page
  becomes the documentation-side evidence for part B and the eval.md row becomes redundant.

### C5 — `https://omp.sh/docs/subagents` — REJECT

- **Access date:** 2026-10-22T10:06:31Z. **HTTP status:** 200 (54,929 B, sha256
  `0902796c581b2b0fc2e7fcf071162778f21d84ebeae66f580e27356b9b63c880`).
- **What it supports:** the *task*-concurrency defaults (`task.maxConcurrency` 32, `async.enabled`
  true) and the `/jobs` / Agent-Hub surface.
- **What it does not support:** parts A–D — the page has **0** occurrences of `maxJobs` or
  `maxRunningJobs`; it never mentions the session-wide background-job cap and conflates the
  per-call task concurrency with it.
- **Quote (11 words, "important defaults" table):** `task.maxConcurrency 32 Bound concurrently running workers; additional work queues. 0 is unlimited.`
- **Verdict: reject.** Different knob; citing it for the background-job ceiling would substitute an
  easier, familiar fact for the asked one.
- **Flip:** the page gains an `async.maxJobs` row in that defaults table — then admit at tier A
  scope "documented session-wide cap default".

### C6 — `https://omp.sh/docs/tools` — REJECT

- **Access date:** 2026-10-22T10:06:31Z. **HTTP status:** 200 (59,950 B, sha256
  `e6c0d205d0a6631cbbc124e18d2a3a216b51a8ea368b8b39d78baa28051fa3e0`).
- **What it supports:** the tool inventory (`bash` with backgrounding, `hub`, `wait`).
- **What it does not support:** any limit — 0 occurrences of `maxJobs`/`maxRunningJobs`.
- **Quote (7 words, `bash` tool entry):** `Long commands can move to the background automatically.`
- **Verdict: reject.** Capability prose, not a limit statement.
- **Flip:** a tool entry gains a numeric concurrency cap — then admit narrowly for that tool.

### C7 — `https://omp.sh/docs/settings` — REJECT

- **Access date:** 2026-10-22T10:08:22Z. **HTTP status:** 200 (61,904 B, sha256
  `8e95cbb8753dc25b6318651c61a53f256d2618a585a97d1eb8f87dfbed91f30a`).
- **What it supports:** the settings-group inventory of the docs site.
- **What it does not support:** parts A–D. `async` appears exactly **once**, as a group label in a
  navigation list; there is no `maxJobs` anywhere on the page (0 occurrences).
- **Quote (12 words, settings-group list):** `browser , async , irc , mcp , tasks , extensionHandlers , and developer options under dev .`
- **Verdict: reject.** The official docs site's settings page carries no value; it cannot support
  the claim's default or ceiling.
- **Flip:** the page inlines the `async.maxJobs` row from `docs/settings.md` — then admit at tier A
  scope "documented default and floor", not the ceiling.

### C8 — `https://omp.sh/docs/slash` — REJECT

- **Access date:** 2026-10-22T10:06:31Z. **HTTP status:** 200 (74,038 B, sha256
  `8af7dc4b15c0bd9761e3a31240afe29af5e817506729b8d1ced7a50629ae719b`).
- **What it supports:** the slash-command reference.
- **What it does not support:** parts A–D (0 occurrences of `maxJobs`/`maxRunningJobs`).
- **Verdict: reject.** Out of scope for a job cap; no quote worth pinning.
- **Flip:** a `/jobs` or `/settings` entry documents the effective cap — then admit narrowly.

### C9 — `https://api-docs.deepseek.com/quick_start/agent_integrations/oh_my_pi/` — REJECT

- **Access date:** 2026-10-22T10:06:31Z. **HTTP status:** 200 (42,402 B, sha256
  `046818a304e47d9246dc17e29ab0ebc6300f4f4db96ae38c3689db8e0b2b3e0d`).
- **What it supports:** how to configure `~/.omp/agent/models.yml` for DeepSeek models.
- **What it does not support:** parts A–D. **Discernment point:** the web-search summary for this
  page asserted that it "states `async.maxJobs` … defaults to `100` and caps running background
  jobs"; the page as served contains **0** occurrences of `maxJobs`, `async` or "background job".
  The summary is not page content and cannot be quoted.
- **Quote (7 words, "Prerequisites" section):** `Install Oh My Pi: https://github.com/can1357/oh-my-pi#installation`
- **Verdict: reject.** A model-provider integration page; the claim it was credited with is not on
  the page.
- **Flip:** the served page gains an `async.maxJobs` paragraph — then admit at tier-B scope
  "third-party documentation of the default".

### C10 — `https://inferri.com/en/projects/cmm7hxszc00eds4x78kzz5fi6` — REJECT

- **Access date:** 2026-10-22T10:06:31Z. **HTTP status:** 200 (320,692 B, sha256
  `374567b980c8062d184857c0da048726e71beae471a1b953fcfb0621e7435eb8`).
- **What it supports:** a third-party overview sentence that a 100-job ceiling exists for
  asynchronous work.
- **What it does not support:** the *shape* of the claim. "up to 100 concurrent jobs" conflates the
  **default** with a **ceiling**; it never mentions `async.maxJobs`, `Math.min`, the floor at 1, or
  the config file. No version pin, no citation to upstream.
- **Quote (20 words, "Underlying Architecture" paragraph):** `Asynchronous background tasks can be configured for up to 100 concurrent jobs, with the await tool to wait for results.`
- **Verdict: reject.** A portfolio/project page describing another product; it cannot be the source
  for a value, and its wording would mis-state the claim if used.
- **Flip:** the page cites the upstream file/line that produces the 100 — then admit as a tier-C
  cross-reference note, not as the value's source.

### C11 — `https://blog.csdn.net/gitblog_01054/article/details/164872117` — REJECT

- **Access date:** 2026-10-22 (10:06:33Z and four earlier attempts 09:58Z–10:0xZ, including
  `m.blog.csdn.net` and a query-string variant). **HTTP status: 521** on every attempt
  (2,156 B error page, sha256 `f2ddd654b7dfd225340aa4ab8e1ed951bc549f556613d9f87f35b90d5533865b`).
- **What it does support:** nothing observed — the body was never retrieved.
- **What it does not support:** parts A–D, unverifiably. The search index summary claimed the
  article "explicitly mentions `async.maxJobs`, `100`, and clamping to `1..100`"; that is a search
  engine's characterisation of an unopened page and is recorded here as **[INFERENCE], unverified**.
- **Quote:** none available (error page only).
- **Verdict: reject.** Unopened source; the same rule that produced `S097` (HTTP 404 candidate
  manual page) applies — an unreachable page cannot support a claim.
- **Flip:** the URL returns 200 and the body states the clamp with a code excerpt — then re-screen;
  even then it is a Chinese blog restating upstream, tier C at best.

### C12 — `https://github.com/can1357/oh-my-pi/issues/14636` — REJECT

- **Access date:** 2026-10-22T10:06:34Z. **HTTP status:** 200 (272,910 B, sha256
  `2060061d6c0b882dbfa44088f147f6e9e5fc9227893477f3a064e5610f8e6f16`; opened 2026-10-06T20:23:29Z).
- **What it supports:** that a user *observed* both numbers in the source: the module fallback
  default 15 and a max of 100 for `async.maxJobs`.
- **What it does not support:** the wiring. It states them as siblings, which invites the wrong
  reading that the shipped cap is 15.
- **Quote (12 words, "Description" paragraph):** `` `AsyncJobManager` counts jobs of any kind (`DEFAULT_MAX_RUNNING_JOBS` 15, `async.maxJobs` up to 100) ``
- **Verdict: reject.** Community-issue prose; it corroborates numbers that the code rows already
  establish with anchors, and its "15" is the *fallback* for an undefined option, unreachable in a
  shipped session (`sdk.ts` always passes the function form).
- **Flip:** the maintainer answers in-thread with the wiring rationale — then the answer text
  becomes quotable upstream prose, and the issue would be re-screened at tier C.

### C13 — `https://github.com/can1357/oh-my-pi/pull/14634` — REJECT

- **Access date:** 2026-10-22T10:06:35Z. **HTTP status:** 200 (344,501 B, sha256
  `4c6fe571e05b31c5ed1080be6d15ce48242944f11f84a2dbc5f33fe21428c008`; PR created
  2026-10-06T20:19:48Z, **merged** 2026-10-08T10:23:51Z, merge commit `afa3e750aa1083c8f5ca44bd082f7c94db52c04b`).
- **What it supports:** that upstream authors state the ceiling in prose ("at most 100") and that
  the limit throws instead of queueing.
- **What it does not support:** nothing new — the sentence was **merged into `docs/tools/eval.md`**,
  which is candidate C3 and is the citable form.
- **Quote (16 words, PR body):** `the real limit is \`async.maxJobs\` (at most 100), and it throws instead of queueing`
- **Verdict: reject** (superseded by C3, which carries the merged text at the tag).
- **Flip:** the merged doc text is removed from `docs/tools/eval.md` while the PR body stays — then
  the PR becomes the only prose source and would be re-screened at tier C.

### C14 — `https://github.com/can1357/oh-my-pi/issues/14967` — REJECT

- **Access date:** 2026-10-22T10:06:36Z. **HTTP status:** 200 (313,718 B, sha256
  `fe6e38bdcbc7b8f30b2bd0f5ea4fd9faa91caec7b4a4f306d2c44565388d129d`; opened 2026-10-08T15:42:26Z).
- **What it supports:** a repro for a *different* defect (an SDK embedder wanting a per-session
  `AsyncJobManager`); it confirms background jobs exist per session.
- **What it does not support:** parts A–D — no cap, no setting name, no error text about a limit.
- **Quote (13 words, "Repro" paragraph):** `Session A runs \`bash {command: "sleep 100000", async: true, timeout: 0}\`, then \`wait\`.`
- **Verdict: reject.** Off-claim subject matter.
- **Flip:** an upstream maintainer states the shipped cap in the thread — then re-screen the
  maintainer comment as tier C.

### C15 — `https://www.gradually.ai/en/changelogs/omp/` — REJECT

- **Access date:** 2026-10-22T10:06:36Z. **HTTP status:** 200 (1,186,509 B, sha256
  `33834e6c8bfb98ff29b21582322f1f3a1fe4af641a43216a176ec310e87d1c74`).
- **What it supports:** an aggregated release list (latest shown v18.12.6, 2026-10-21).
- **What it does not support:** parts A–D. The served page contains **0** occurrences of `maxJobs`
  or "Background job" — including in the v18.12.6 entry it reproduces.
- **Quote (15 words, page header):** `This view shows 112 of 175 recorded entries. Older entries are not loaded here.`
- **Verdict: reject.** A secondary mirror of upstream release notes; it reproduces no job-limit text
  and truncates history, so it cannot stand in for the upstream repo.
- **Flip:** the aggregator adds the `async.maxJobs` line from upstream release notes with a date —
  then it is a usable mirror, but the upstream note stays the better source.

### C16 — `https://vietbui.mintlify.app/entities/omp` — REJECT

- **Access date:** 2026-10-22T10:06:37Z. **HTTP status:** 200 (530,318 B, sha256
  `17accaf9dc5a4c8e3e5ed6cbaa00f4ee4ddb1f4d04eefc63943c9fe6888b3597`).
- **What it supports:** a machine-generated "LLM Wiki" entity page listing the tool inventory.
- **What it does not support:** parts A–D (0 occurrences of `maxJobs`/`maxRunningJobs`).
- **Quote (7 words, Runtime tool table):** `bash Workspace shell; optional PTY or background jobs`
- **Verdict: reject.** Tertiary, unsourced, and about tools rather than limits.
- **Flip:** the page cites the upstream `async.maxJobs` definition — then admit as tier C.

### C17 — `https://deepakness.com/blog/omp-setup/` — REJECT

- **Access date:** 2026-10-22T10:06:37Z. **HTTP status:** 200 (51,835 B, sha256
  `58031cb2f41831b0e302a49eff94a071335153811f3f7a8fd788d444498daa14`).
- **What it supports:** a personal multi-provider setup walkthrough.
- **What it does not support:** parts A–D (0 occurrences of `maxJobs`).
- **Quote (20 words, "Here's how it works" section):** `DeepSeek v4 Flash – my default driver. Fast, cheap, and it handles most of what I do day to day.`
- **Verdict: reject.** Setup prose with no limit statement.
- **Flip:** the post reports an observed `Background job limit reached (N)` while tuning the
  harness (registration path only — the auto-background path degrades to foreground, §5.6) — then
  admit as a tier-C observation of the *observable* error, still not of the ceiling.

### C18 — `https://pi.dev/packages/omp-oracle` — REJECT

- **Access date:** 2026-10-22T10:06:37Z. **HTTP status:** 200 (74,093 B, sha256
  `62331369d9347be56d1eb266b6ed3ed6bb13a8b3abb4863339fe634ef4111be9`).
- **What it supports:** that a third-party plugin advertises "durable background jobs" for `omp`.
- **What it does not support:** parts A–D. The served page contains **zero** occurrences of `100`
  (and none of `maxJobs`), despite the search summary crediting it with the default-100 statement.
- **Quote (22 words, package description):** `Asynchronous ChatGPT and Grok web-oracle jobs for Oh My Pi and pi: isolated browser auth, durable background jobs, and project-context archives.`
- **Verdict: reject.** Plugin marketing page; the claim credited to it is not present in the served
  bytes.
- **Flip:** the package README documents the `async.maxJobs` default it relies on — then admit at
  tier C.

---

## 4. Proposed SOURCES.md rows

Next free id after `S097` is `S098`, but `MoriR25.UpstreamTagLocate` has already proposed
`S098`–`S102` (upstream code + docs + binary). **The L1 must reconcile the id space**; the ids below
are proposals only, and `S103` may need renumbering.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S103 | oh-my-pi docs/tools/eval.md at v18.12.6 — https://raw.githubusercontent.com/can1357/oh-my-pi/v18.12.6/docs/tools/eval.md | docs | A | upstream's prose statement of the session-wide background-job cap: its **default and maximum 100**, its scope (shared with async `bash`, async `task` spawns, `workpool()` pools, nested subagents) and the failure text; v18.12.6 only; documents the cap, not the `Math.min` expression | docs/tools/eval.md:258; tag v18.12.6; sha256 fb2fc4a139ba187f1cc062fab53bd72a48dd13b1f81f0c3318ec7a79d41e495c | The cap is session-wide and shared by every kind of background job; upstream states 100 as both default and maximum, so a configured value above 100 cannot raise it. | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md |
| S104 | oh-my-pi-termux ARM64 launcher — https://github.com/Daxiongmao87/oh-my-pi-termux | tool | C | Termux packaging of the *unmodified* upstream `omp` binary (versions 18.12.0 / 18.11.3 verified); no statement of the background-job cap | README.md:6-7; raw README sha256 0846b461000fa46ca95fbcbc390ed8d870a3fb825fb4fa06b504ee98817fe1cf; HTTP 200, 2026-10-22T10:06:29Z | REJECTED: a community launcher/updater that installs the upstream binary; it contains no `maxJobs`/`Background job` text in any file (0 hits) and no issue mentions the cap, so it supports nothing about the ceiling. Flip: the repo records an observed `Background job limit reached (N)` under glibc-runner, then admit as an own-work ARM64 observation row. | rejected | 2026-10-22 | 90d | — |
| S105 | omp settings gist by sonsu-lee — https://gist.github.com/sonsu-lee/4d76307bc70d6696c8336855ac292d3e | community | C | one user's `omp` `config.yml` (model roles, retry fallbacks, task overrides, worktree); contains no `async:` block | gist page `<title>`; raw 6,161 B, 111 lines, sha256 9ae986fcae301544a8af80032ca7e3b40892503540002259fbc041bfcf9e0f3c; HTTP 200, 2026-10-22T10:06:30Z | REJECTED: a personal configuration file with no `async:` block (0 hits for `async`/`maxJobs`); its silence describes that user's config, not the product's cap. Flip: the author publishes an `async.maxJobs` block together with the observed limit error, then admit as a tier-C configured-versus-effective note. | rejected | 2026-10-22 | 90d | — |
| S106 | oh-my-pi docs/settings.md at v18.12.6 (rejected as evidence of the 100 ceiling) — https://raw.githubusercontent.com/can1357/oh-my-pi/v18.12.6/docs/settings.md | docs | A | the settings reference row for `async.maxJobs`: type number, default 100, floored to at least 1, queued/parked jobs excluded; **no upper bound is stated** | docs/settings.md:623; sha256 0b2e1457021fa526f2c35015672f1d7ccbac95e7b9f217528ab8022c55ed5883; HTTP 200, 2026-10-22T10:06:30Z | REJECTED *for the clamp claim*: it documents the default and the floor but never a maximum, so read alone it predicts that a configured 200 yields 200 running jobs, which is false at v18.12.6 (the ceiling is documented in docs/tools/eval.md, S103, and implemented in sdk.ts). Overlaps the row `MoriR25.UpstreamTagLocate` proposes as S101; that proposal is sound for the default and floor only. Flip: upstream adds the ceiling to this table, then the row is admitted at the same scope and S103 becomes redundant. | rejected | 2026-10-22 | on-release | — |
| S107 | omp docs site, subagents and settings pages — https://omp.sh/docs/subagents , https://omp.sh/docs/settings , https://omp.sh/docs/tools , https://omp.sh/docs/slash | docs | C | the official documentation site: task-concurrency defaults and the tool/slash-command inventories; no background-job cap | subagents "important defaults" table; settings group list; tools `bash` entry; all HTTP 200 on 2026-10-22T10:06:31Z–10:08:22Z (sha256 0902796c…, 8e95cbb8…, e6c0d205…, 8af7dc4b…) | REJECTED: none of the four pages contains `maxJobs` or `maxRunningJobs` (0 hits each); `task.maxConcurrency` 32 is a different knob, so citing it for the background-job ceiling would substitute an easier fact. Flip: the docs site inlines the `async.maxJobs` row from docs/settings.md, then admit at tier A scope "documented default and floor". | rejected | 2026-10-22 | 90d | — |
| S108 | Using DeepSeek with Oh My Pi — https://api-docs.deepseek.com/quick_start/agent_integrations/oh_my_pi/ | docs | C | provider integration page: `~/.omp/agent/models.yml` for DeepSeek models; no harness setting text | "Prerequisites" section; 42,402 B, sha256 046818a304e47d9246dc17e29ab0ebc6300f4f4db96ae38c3689db8e0b2b3e0d; HTTP 200, 2026-10-22T10:06:31Z | REJECTED: a search summary credited this page with stating `async.maxJobs` and its 100 default, but the served page has 0 occurrences of `maxJobs`, `async` or "background job"; the summary is not page content and cannot be quoted. Flip: the page gains an `async.maxJobs` paragraph, then admit at tier B scope "third-party statement of the default". | rejected | 2026-10-22 | 90d | — |
| S109 | Inferri project page "can1357/oh-my-pi" — https://inferri.com/en/projects/cmm7hxszc00eds4x78kzz5fi6 | community | C | third-party overview of `oh-my-pi`; describes asynchronous background tasks in one sentence | "Underlying Architecture" paragraph; 320,692 B, sha256 374567b980c8062d184857c0da048726e71beae471a1b953fcfb0621e7435eb8; HTTP 200, 2026-10-22T10:06:31Z | REJECTED: "up to 100 concurrent jobs" conflates the default with a ceiling and never names `async.maxJobs`, the clamp, the floor, or the config file; no version pin and no citation. Flip: the page links the upstream line that produces the 100, then admit as a tier-C cross-reference, never as the value's source. | rejected | 2026-10-22 | 90d | — |
| S110 | oh-my-pi 子代理后台任务挂起通知解析 (CSDN blog) — https://blog.csdn.net/gitblog_01054/article/details/164872117 | community | C | candidate Chinese-language blog said by a search summary to mention `async.maxJobs`, 100 and a 1..100 clamp; body never retrieved | HTTP 521 on four attempts 2026-10-22 (09:58Z–10:06:33Z), error body 2,156 B, sha256 f2ddd654b7dfd225340aa4ab8e1ed951bc549f556613d9f87f35b90d5533865b; `m.blog.csdn.net` and a query-string variant also 521 | REJECTED: unreachable page, no body, no quotable sentence; the search summary's characterisation of the clamp is [INFERENCE], unverified. Flip: the URL returns 200 and the body quotes the clamp from upstream, then re-screen at tier C at best. | rejected | 2026-10-22 | 90d | — |
| S111 | oh-my-pi issue #14636 "Limit how many heavy commands run at once across subagents" — https://github.com/can1357/oh-my-pi/issues/14636 | community | C | a user issue citing the two numbers found in the source: the module fallback default 15 and `async.maxJobs` up to 100 | "Description" paragraph; opened 2026-10-06T20:23:29Z; HTTP 200, 2026-10-22T10:06:34Z, sha256 2060061d6c0b882dbfa44088f147f6e9e5fc9227893477f3a064e5610f8e6f16 | REJECTED: issue prose that corroborates numbers the code rows already anchor, and its "15" is the fallback for an *undefined* option, unreachable in a shipped session, so the row risks teaching the wrong default. Flip: a maintainer answer states the wiring rationale, then that comment is re-screened at tier C. | rejected | 2026-10-22 | 90d | — |
| S112 | oh-my-pi PR #14634 "docs(coding-agent): correct agent() and workpool concurrency limits in eval docs" — https://github.com/can1357/oh-my-pi/pull/14634 | community | C | a merged docs PR whose body states the session-wide limit as `async.maxJobs` (at most 100) and that it throws instead of queueing | PR body; created 2026-10-06T20:19:48Z, merged 2026-10-08T10:23:51Z (merge commit afa3e750aa1083c8f5ca44bd082f7c94db52c04b); HTTP 200, 2026-10-22T10:06:35Z, sha256 4c6fe571e05b31c5ed1080be6d15ce48242944f11f84a2dbc5f33fe21428c008 | REJECTED: superseded — the same sentence is merged upstream prose in docs/tools/eval.md at v18.12.6 (S103), which is the citable form; a PR description is not a version-pinned source. Flip: the merged text is later removed from docs/tools/eval.md while the PR body stands, then re-screen at tier C. | rejected | 2026-10-22 | 90d | — |
| S113 | oh-my-pi issue #14967 "Let an SDK embedder give each top-level session its own AsyncJobManager" — https://github.com/can1357/oh-my-pi/issues/14967 | community | C | a bug report about per-session job-manager ownership; no statement of the cap | "Repro" paragraph; opened 2026-10-08T15:42:26Z; HTTP 200, 2026-10-22T10:06:36Z, sha256 fe6e38bdcbc7b8f30b2bd0f5ea4fd9faa91caec7b4a4f306d2c44565388d129d | REJECTED: off-claim subject matter — it shows background jobs exist per session but names no limit, no setting and no limit error. Flip: a maintainer states the shipped cap in the thread, then re-screen that comment at tier C. | rejected | 2026-10-22 | 90d | — |
| S114 | OMP Changelog (October 2026), gradually.ai — https://www.gradually.ai/en/changelogs/omp/ | community | C | an aggregated mirror of upstream OMP release notes (latest v18.12.6, 2026-10-21); partial history | page header; HTTP 200, 2026-10-22T10:06:36Z, 1,186,509 B, sha256 33834e6c8bfb98ff29b21582322f1f3a1fe4af641a43216a176ec310e87d1c74 | REJECTED: no `maxJobs` and no "Background job" text anywhere on the served page (0 hits), including in the v18.12.6 entry it reproduces, and it truncates history; a mirror cannot stand in for the upstream repository. Flip: the aggregator inlines the upstream `async.maxJobs` release note with its date, then it becomes a usable mirror. | rejected | 2026-10-22 | 90d | — |
| S115 | "omp (oh-my-pi)" entity page, vietbui LLM Wiki — https://vietbui.mintlify.app/entities/omp | community | C | a machine-generated third-party summary listing the tool inventory | Runtime tool table; HTTP 200, 2026-10-22T10:06:37Z, 530,318 B, sha256 17accaf9dc5a4c8e3e5ed6cbaa00f4ee4ddb1f4d04eefc63943c9fe6888b3597 | REJECTED: tertiary, unsourced, and about tools rather than limits (0 hits for `maxJobs`/`maxRunningJobs`). Flip: the page cites the upstream `async.maxJobs` definition, then admit at tier C. | rejected | 2026-10-22 | 90d | — |
| S116 | Setting Up and Testing OMP (Oh My Pi) Agent — https://deepakness.com/blog/omp-setup/ | community | C | a personal multi-provider setup walkthrough | "Here's how it works" section; HTTP 200, 2026-10-22T10:06:37Z, 51,835 B, sha256 58031cb2f41831b0e302a49eff94a071335153811f3f7a8fd788d444498daa14 | REJECTED: setup prose with no job-limit statement (0 hits for `maxJobs`). Flip: the post reports an observed `Background job limit reached (N)` while tuning, then admit as a tier-C observation of the error text only. | rejected | 2026-10-22 | 90d | — |
| S117 | omp-oracle package page, pi.dev — https://pi.dev/packages/omp-oracle | community | C | a third-party plugin advertising durable background jobs for `omp` | package description; HTTP 200, 2026-10-22T10:06:37Z, 74,093 B, sha256 62331369d9347be56d1eb266b6ed3ed6bb13a8b3abb4863339fe634ef4111be9 | REJECTED: plugin marketing page; the search summary credited it with the default-100 statement, but the served HTML contains zero occurrences of `100` and none of `maxJobs`. Flip: the package README documents the `async.maxJobs` default it relies on, then admit at tier C. | rejected | 2026-10-22 | 90d | — |

**Coverage of the 18 screened candidates (check completeness):** C3→S103 (admitted);
C1→S104; C2→S105; C4→S106; C5+C6+C7+C8→S107 (the four `omp.sh` pages folded into one family row);
C9→S108; C10→S109; C11→S110; C12→S111; C13→S112; C14→S113; C15→S114; C16→S115; C17→S116;
C18→S117. 18 candidates → 15 proposed rows (1 admitted, 14 rejected); plus 2 further admitted
upstream-code rows proposed outside the rejected-candidate remit = **17 proposed rows in total**.
**Id note (reconciled against the landed registry at `cb51e84`):** the L1 placed the two upstream
code rows as **S112** (bash.ts) and **S113** (eval.ts) — my proposal ids S118/S119 were not used.
My proposed ids and the landed ids: S103→S103; S104 (termux)→**S105**; S105 (gist)→**S106**;
S106 (docs/settings.md)→**admitted as S101**; S107→S107; S108→S108; S109 (inferri)→**not placed**;
S110 (CSDN)→**S109**; S111 (issue #14636)→**S110**; S112 (PR #14634)→**not placed**; S113 (issue
#14967)→**not placed**; S114 (vietbui)→**not placed**; S115 (deepakness)→**not placed**; S116
(pi.dev)→**not placed**; S117 (gradually)→**S111**; S118 (bash.ts)→**S112**; S119 (eval.ts)→**S113**.

**Two additional admitted rows, outside my rejected-candidate remit** (proposed because they bound
part D of the claim and no seat claimed those files; see §5.6 for the verification) — landed by the
L1 as **S112** and **S113**:

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S112 *(my proposal S118)* | oh-my-pi tools/bash.ts at v18.12.6 — https://raw.githubusercontent.com/can1357/oh-my-pi/v18.12.6/packages/coding-agent/src/tools/bash.ts | code | A | how the bash tool behaves at the running-job cap: the auto-background branch pre-checks `atCapacity` and falls back to foreground execution, while an explicit `async: true` call registers without a pre-check; the single register site `:882` is reached from **both** callers, so the guard status belongs to the caller path; v18.12.6 only | bash.ts:1188-1192 (explicit async branch) → :843 `#startManagedBashJob` → :882 `manager.register`; auto-background caller :1235 with guard :1220-1229 (`!autoBgManager.atCapacity`); `grep -n startManagedBashJob` → 3 hits (:843 definition, :1192, :1235); HTTP 200, 67,415 B, sha256 d985ef25639993e05fb4de8c8b6dc75dde76422f63d1a295b95eb575e8cc3ea2 | Reaching the cap does not always surface an error: the auto-background path degrades to a foreground run, and the limit error belongs to the explicit-async registration path. | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md |
| S113 *(my proposal S119)* | oh-my-pi tools/eval.ts at v18.12.6 — https://raw.githubusercontent.com/can1357/oh-my-pi/v18.12.6/packages/coding-agent/src/tools/eval.ts | code | A | how the eval tool behaves at the running-job cap: the auto-background branch pre-checks `atCapacity` and runs in the foreground instead; its register site `:563` is reached only from that guarded branch; v18.12.6 only | eval.ts:533-538 (`autoBgManager.atCapacity` → `return await run(...)`); register at :563 on the guarded auto-background branch; HTTP 200, 41,679 B, sha256 01e9c5c56af15d3e04cdeaf99d959afa90129f8cbb015d6908e02795351920e3 | The same cap has two observable behaviours by consumer: a pre-check falls back to foreground execution, while an unguarded registration throws the limit error. | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md |

---

## 5. Findings for the canonical judge

1. **One candidate is admitted, and it closes a documentation gap the other seat left open.**
   `docs/tools/eval.md:258` at tag `v18.12.6` states the cap's "**default and maximum 100**".
   `MoriR25.UpstreamTagLocate` §3/R7 reports that `docs/settings.md:623` is "the only `maxJobs`
   mention in the fetched docs" — true for that seat's sampled file list, but the tag tree carries a
   second official mention in `docs/tools/eval.md`. Verified: `grep -rl -i maxJobs` over the tag's
   `docs/` returns exactly `docs/settings.md` and `docs/tools/eval.md` (2 hits total, one each);
   `README.md` → 0.
   **Recommended wording for the L1:** the settings
   reference documents the *default* and the *floor*; the eval guide documents the *maximum*.
   Neither states the `Math.min` expression; the code rows do.
2. **Two official doc pages disagree in coverage, not in value.** `docs/settings.md:623` — "floored to
   at least 1", no upper bound; `docs/tools/eval.md:258` — "default and maximum 100". Both are in the
   same tag and are byte-stable (`main` and `v18.12.6` fetches are identical for both files,
   sha256 `0b2e1457…` and `fb2fc4a1…`). A reader of the settings page alone would predict that
   `async.maxJobs: 200` yields 200 running jobs; the shipped code clamps at 100.
3. **The upstream "15" is a fallback, not a shipped default — keep the two apart.** `sdk.ts:2284`
   always passes `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings))`, so the
   `DEFAULT_MAX_RUNNING_JOBS = 15` in `job-manager.ts:43` is unreachable in a shipped session.
   Issue #14636's phrasing ("`DEFAULT_MAX_RUNNING_JOBS` 15, `async.maxJobs` up to 100") invites the
   opposite reading; that is why S111 is rejected rather than admitted.
4. **Search-engine summaries are not sources.** Three candidates (C9 DeepSeek, C18 pi.dev, C11 CSDN)
   were credited by the search tool with a statement that the served bytes do not contain
   (`maxJobs`/`async`/`100` counts are 0 on C9 and C18; C11 is HTTP 521 with no body). Every verdict
   above is based on bytes fetched directly, with status, size and sha256 recorded.
5. **Corroboration observed while screening (not part of any row).** The installed
   `~/.local/bin/omp` (256,702,432 B) matches the contract's own byte search exactly: one match for
   `maxRunningJobs:\s*\(\)\s*=>\s*Math\.min\(\s*(\d+)\s*,\s*[\w$]+\.get\([\w$]+\)\s*\)` with value
   `100`, and one match for `id:\s*"async\.maxJobs",[^}]{0,300}?default:\s*(\d+)` with value `100`.
   The upstream source at tag `v18.12.6` reproduces both expressions verbatim, so the tag is the right
   pin for the upstream rows.
6. **The limit error is not the universal symptom of hitting the cap — scope limit on any
   "the harness refuses at the cap" statement.** Verified at tag `v18.12.6` (raw fetch HTTP 200;
   tarball copy and raw fetch digests identical):
   - `packages/coding-agent/src/async/job-manager.ts:369-373` — `register()` **throws**
     `` `Background job limit reached (${maxRunningJobs}). Wait for running jobs to finish or cancel one.` ``
     when the running count reaches the cap (sha256
     `0f37afaaa822ef1de845b8eb21473a70210176ff61e2dcff5925f85ec0e544e7` — the same digest
     `MoriR25.UpstreamTagLocate` records for S098, an independent cross-check).
   - `packages/coding-agent/src/tools/bash.ts:1220-1229` — the **auto-background** branch guards on
     `!autoBgManager.atCapacity` and, at the cap, "fall[s] through to direct foreground execution
     instead of failing every bash call until a slot frees up" (sha256
     `d985ef25639993e05fb4de8c8b6dc75dde76422f63d1a295b95eb575e8cc3ea2`).
   - `packages/coding-agent/src/tools/eval.ts:533-538` — the **eval auto-background** branch does the
     same (sha256 `01e9c5c56af15d3e04cdeaf99d959afa90129f8cbb015d6908e02795351920e3`); its
     `autoBgManager.register(` at `:563` is reached only on the auto-background branch the `:536`
     guard diverts when `atCapacity` is true.
   - An **explicit** `async: true` bash call does not pre-check: `bash.ts:1188` (`if (asyncRequested)`)
     → `:1192` `#startManagedBashJob` (`:843`), which calls `manager.register` (`:882`) — so that path
     throws the limit error at the cap. (The auto-background branch is the second
     `#startManagedBashJob` call, at `:1235`, guarded by the `:1228` `atCapacity` check.)
   - `grep -rn "atCapacity" packages/coding-agent/src` at the tag returns exactly **three**
     consumers: the getter definition (`job-manager.ts:338`) and the two pre-checks above.
   - **Which paths throw, measured statically (my own enumeration, two independent methods).**
     (a) `grep -rnE "[A-Za-z0-9_$.]*[Mm]anager\.register\(" --include=*.ts .` over the tag's
     `src` (excluding tests: 0 hits in test files) returns **12** production call sites in 11 files:
     `eval/agent-bridge.ts:210`, `eval/judgment-batch-bridge.ts:223`,
     `modes/controllers/tan-command-controller.ts:144`, `security/coordinator.ts:499`,
     `task/executor.ts:3272`, `task/index.ts:1407`, `task/restore.ts:85`, `task/workpool.ts:175`,
     `task/workpool.ts:363`, `tools/bash.ts:882`, `tools/eval.ts:563`, `vibe/runtime.ts:1370`.
     (b) Cross-check by the `register()` kind argument (`grep -rn -A1 -E "\.register\($"` filtered on
     `"bash"|"task"|"eval"|"agent"|"judgment"`) returns the **same 12** sites and no others.
     `grep -rn "Background job limit reached" --include=*.ts .` in `src` returns exactly **one** hit
     (`job-manager.ts:372`), so there is a single throw source.
     Net: **two** guarded escape hatches (`tools/bash.ts:1220-1229` auto-background,
     `tools/eval.ts:533-538` auto-background) against **ten** unguarded registration sites, of which
     `task/index.ts:1407` is the task/agent spawn path that matches the observed symptom of `task`
     calls being refused while the cap is full.
   - **Guard status attaches to the caller path, not to the register call site** (correction after
     `MoriR25.SrcJobManager`'s second pass; verified by me): per-file `atCapacity` counts at the tag
     are 1 for `tools/bash.ts`, 1 for `tools/eval.ts` and **0** for each of the other nine files that
     contain a register site (`eval/agent-bridge.ts`, `eval/judgment-batch-bridge.ts`,
     `modes/controllers/tan-command-controller.ts`, `security/coordinator.ts`, `task/executor.ts`,
     `task/index.ts`, `task/restore.ts`, `task/workpool.ts` ×2, `vibe/runtime.ts`). But
     `tools/bash.ts:882` is reached from **both** `#startManagedBashJob` call sites — `:1192`
     (explicit async, unguarded) and `:1235` (auto-background, guarded at `:1228`) — so that site
     must **not** be counted as simply guarded; and `tools/eval.ts:563` is the one site reached only
     from a guarded branch. The honest classification of the 12 sites is therefore: **ten** sites in
     files that never consult `atCapacity` (always throw at the cap), **one** mixed site
     (`bash.ts:882`, throws when reached via `:1192`), **one** guarded-only site (`eval.ts:563`).
     `grep -n startManagedBashJob tools/bash.ts` → exactly three hits: the `:843` definition plus
     `:1192` and `:1235`.
   **Consequence for the round:** a refusal record quoting `Background job limit reached (100)`
   comes from a *registration* path (explicit async bash, task/agent spawns), not from every cap
   encounter; the auto-background paths degrade to foreground execution instead. Any statement of the
   form "the harness refuses at the cap" must be scoped to registration paths. Verified by me after
   `MoriR25.SrcJobManager` raised it; I did not take that seat's anchors on trust (its quoted
   `job-manager.ts` body sha256 `e86a701b…` is the *issue* body, not this file).
   **Count discrepancy, reported verbatim for the judge:** `MoriR25.SrcJobManager` states "14
   production register call sites" and then enumerates **12** — the enumerated list is the one I
   reproduced twice; the number 14 is not reproduced by either of my greps.
   **Routing:** `tools/bash.ts` and `tools/eval.ts` were outside every seat's claimed surface, so I
   proposed them as admitted code rows; the L1 landed them as **S112** and **S113** (§4).
   **Independent re-check by a second seat:** `MoriR25.KnowledgeDraftC2` re-ran the `atCapacity`
   grep at the tag and reports the same three hits with the same two file digests, and cites the
   explicit-async branch as `tools/bash.ts:1187-1208` (the block range; my narrower anchors are
   `:1188` `if (asyncRequested)`, `:1192` `#startManagedBashJob`, `:843`, `:882`). Three seats
   (`SrcJobManager`, `KnowledgeDraftC2`, this seat) have now read the same tag bytes for this
   finding; the only disagreement found between them is the 14-vs-12 call-site count, reported above.
7. **The L1's landed S104 row (upstream feature commit `476b858`) re-verified by me — it also
   answers the "why 100" question the knowledge draft had marked untraced.** Patch fetched
   (HTTP 200, 76,782 B, sha256 `00f6cbb0b786dd8416e3c764d90e51b159bde6873bd1f7e955f5fd847b571257`):
   commit `476b858b3a4abe6f6c8a06c252c23961be41e912`, authored 2026-02-22 by can1357, subject
   "feat(coding-agent): added async background job execution with configurable concurrency limits",
   "Fixes #56". The patch introduces, at once:
   - the clamp `const asyncMaxJobs = Math.min(100, Math.max(1, settings.get("async.maxJobs") ?? 15));`
     (patch line 1016) — the *same shape* as v18.12.6's `Math.min(100, cfg)` plus the manager's
     `Math.max(1, …)` floor, with the fallback `?? 15` inline;
   - the setting itself, `"async.maxJobs": { type: "number", default: 15, … "Maximum concurrent
     background jobs (1-100)" }` (patch line 464) — the **UI description states the range 1-100**,
     so the ceiling was documented from the feature's introduction;
   - `DEFAULT_MAX_RUNNING_JOBS = 15` and the `Background job limit reached (${this.#maxRunningJobs})`
     throw.
   **Historical reading, worth carrying:** the *default* was 15 at introduction and is 100 at
   v18.12.6 (the setting moved into `tools/settings.ts` with `default: 100`); the *ceiling* of 100
   and the *floor* of 1 never changed. That is why `docs/settings.md` documents the default and the
   floor but not a maximum, while `docs/tools/eval.md` states "default and maximum 100".
8. **Reconciliation of my proposals with the landed registry (read-only check of `corpus/SOURCES.md`
   at `cb51e84`; I did not edit it).** Landed rows from this screening: **S103** (my eval.md doc
   row, id unchanged), **S105** (termux — my S104), **S106** (gist — my S105), **S107** (omp.sh
   family — unchanged), **S108** (DeepSeek — unchanged), **S109** (CSDN — my S110), **S110**
   (issue #14636 — my S111), **S111** (gradually — my S113), **S112** (tools/bash.ts — my S118),
   **S113** (tools/eval.ts — my S119). My proposal for `docs/settings.md` (my S106) was **admitted**
   by the L1 as **S101**, scoped to the documented default and floor — that is the admission my row's
   flip condition named, and it is consistent with my rejection (which was scoped to the ceiling,
   not to the default). **Six of my rejected candidates were not placed in the registry:** inferri
   (my S109), upstream PR #14634 (my S112), upstream issue #14967 (my S113), vietbui (my S114),
   deepakness (my S115), pi.dev omp-oracle (my S116). Their URLs, statuses, quotes, reasons and
   flip conditions survive only in this report — the registry holds seven of my rejected rows.
   The L1 also added **S104** (the upstream feature commit), which I had not screened; §5.7 is my
   verification of it.
9. **Version history of the cap, measured by me (independent of §5.7, and it fixes the "why 100"
   and "why 15" questions).** `grep -c "Math.min(100"` over `packages/coding-agent/src/sdk.ts` at
   successive tags (each raw fetch HTTP 200): **v12.17.2 → 0**, **v12.18.3 → 0**, **v12.19.0 → 1**
   (at `sdk.ts:726`, `const asyncMaxJobs = Math.min(100, Math.max(1, settings.get("async.maxJobs") ?? 15));`),
   v13.3.4 → 1 (same expression, fallback still `?? 15`), **v13.3.5 → 1 with the fallback changed to
   `?? 100`** (`sdk.ts:732`), v18.12.6 → 1. The upstream changelog at `v12.19.0`
   (`packages/coding-agent/CHANGELOG.md:11,15`) reads "Added async background job execution for bash
   commands and tasks with `async: true` parameter" and "Added `async.enabled` and `async.maxJobs`
   settings to control background job execution"; at `v13.3.5` the same file, line 12, reads
   "Increased default async max jobs limit from 15 to 100 for improved concurrent task handling".
   **Reading:** the ceiling of 100 and the floor of 1 are original to the feature (2026-02-22) and were
   documented as the range 1-100 from the start; the *default* moved 15 → 100 on 2026-02-26. For the
   first four days the effective cap when `async.maxJobs` was absent was therefore **15**, not 100 —
   the shipped 18.12.6 behaviour (default 100) is a later change, and the module fallback constant
   15 in `job-manager.ts:43` is the fossil of that first four days. This corroborates the narrowing
   in S098's scope cell ("module fallback constant 15, used only when the option is undefined, not
   the effective cap"). The *reason* the number 100 was chosen is still not stated by any source I
   found — the UI range text "Maximum concurrent background jobs (1-100)" says what, not why.
10. **The upstream feature patch exists under two SHAs with byte-identical content.** Fetching
   `…/commit/3ce6a68380f11d6ba3c32133d1660bd58a3bb346.patch` gives HTTP 200, 76,782 B, sha256
   `1c2f996e37f3d8c235df4d8589b1347a088d38d5182c14008b832a37f86b50cc`; `diff` against the `476b858`
   patch (sha256 `00f6cbb0…b571257`) differs on exactly **one** line — the `From <sha>` header
   (2 diff lines counting `<`/`>`). Same author date, same message, same body. **Audit note:** a
   source row anchored to one SHA must not be read as a second independent source, and "the commit
   that introduced the cap" is not unique by SHA; it is unique by content. [INFERENCE] The pair is
   consistent with a rebase or amend pair; I did not inspect either commit's parents (the GitHub
   commits API returned `API rate limit exceeded` for this host), so the relationship between the two
   SHAs is untraced.
   **Digest receipt, corrected (2026-10-22, after `MoriR25.SrcJobManager` flagged it):** an earlier
   draft of this report cited the twin patch's digest as the 62-character string
   `2f996e37f3d8c235df4d8589b1347a088d38d5182c14008b832a37f86b50cc` — the leading `1c` was dropped
   in transcription from the terminal output. The receipt is the 64-character
   `1c2f996e37f3d8c235df4d8589b1347a088d38d5182c14008b832a37f86b50cc`, recomputed from the file still
   on disk (`sha256sum twin_3ce6a683.patch`, length check 64). The finding itself was never affected;
   only the receipt string was unusable. Recorded here rather than silently fixed, so the judge can
   see the correction.
11. **Corroboration of the v18.4.0 rewiring (my own measurements; the fact was traced by
   `MoriR25.SrcJobManager`, and I re-verified it independently rather than repeating it).**
   - The module constant was never raised: `const DEFAULT_MAX_RUNNING_JOBS = 15` at `v12.19.0`,
     `v13.3.5`, `v18.4.0` and `v18.12.6` (`job-manager.ts:43`) — each raw fetch HTTP 200.
   - The *function-shaped* option is a v18.4.0-era design: the option type
     `maxRunningJobs?: number | (() => number)` and the getter branch `typeof option === "function"`
     are **absent** at `v12.19.0` and `v13.3.5` (0 hits each) and present at `v18.4.0` and
     `v18.12.6` (1 hit each).
   - `sdk.ts` rewiring: the session-lifetime form `const asyncMaxJobs = Math.min(100, …)` is present
     at `v14.0.0` and `v18.3.0` (1 hit each, 0 of the function form), and at `v18.4.0` it is
     **replaced** by `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings))` (1 hit,
     const form now 0), which holds through `v18.12.6`.
   **Consequence:** the "re-read on every capacity check" comment in the v18.12.6 manager describes
   the v18.4.0 design, not the feature's original wiring — which is why the getter branches on the
   option's type, and why the 15 constant survived unchanged for the whole life of the feature. It
   moves none of the v18.12.6 anchors; it explains why 15 and 100 coexist in the shipped source.

---

## 6. Out of scope / not done

- `corpus/SOURCES.md` was **not** edited (assignment says so); the rows above are proposals for the
  L1 to place, and the id space must be reconciled with `MoriR25.UpstreamTagLocate`'s `S098`–`S102`.
- The C2 tool `tools/mori-job-runway.py` and its frozen cases were not built, run or reviewed by this
  seat; `tools/fixtures/mori-job-runway/cases.json` was not inspected.
- The knowledge entry `corpus/knowledge/harness-job-capacity-r25.md` was not drafted or edited.
- `~/.omp/agent/config.yml` was **not** read or written by this seat (the job-limit claim does not
  need it; the config side belongs to the tool rows). No OMP setting, MCP file or fleet script was
  touched.
- No `omp` process was run; the binary was only read as bytes (one regex probe, reported in §5.5).
- No session transcript under `~/.omp` was opened; no message content was read.
- Upstream `docs/` was not exhaustively enumerated: I read the tag's `docs/settings.md`,
  `docs/tools/eval.md`, `docs/tools/task.md` and grepped the whole `docs/` tree for `maxJobs`
  (1 hit in `settings.md`, 1 in `tools/eval.md`, none elsewhere). **[INFERENCE]** The docs tree's
  `maxJobs` coverage is therefore bounded by those two files, not proven exhaustive.
- Other seats' territory left untouched: upstream code rows (`MoriR25.SrcJobManager`,
  `MoriR25.SrcClampSite`), the tag/commit resolution (`MoriR25.UpstreamTagLocate`), the binary
  own-work row (`MoriR25.SrcBinaryOwnWork`), the C2 tool and its fixtures
  (`MoriR25.BuildJobRunwayTool`), and the knowledge draft (`MoriR25.KnowledgeDraftC2`).
- Exception, stated for the record: `packages/coding-agent/src/tools/bash.ts` and
  `packages/coding-agent/src/tools/eval.ts` at tag `v18.12.6` were **not** claimed by any seat
  (`MoriR25.SrcJobManager` flagged them as outside its surface), and they bound part D of the claim
  (§5.6). I therefore read them, verified them independently, and proposed them as code rows — the
  L1 landed them as **S112** (bash.ts) and **S113** (eval.ts). I did not touch any file another seat
  owns, and I did not create those rows in `SOURCES.md`.

## 7. Commands, tools, installs

- `curl -sS -L -w "%{http_code}"` against 21 URLs (GitHub HTML/API, raw.githubusercontent.com,
  gist, omp.sh, third-party pages); one bulk manifest pass wrote status + UTC timestamp + size +
  sha256 + `maxJobs` hit count per URL to `/tmp/manifest/manifest.tsv`; body sha256 values quoted
  above are from that manifest. A second pass fetched three upstream files by raw tag URL for the
  §5.6 rows: `tools/bash.ts` (67,415 B), `tools/eval.ts` (41,679 B), `async/job-manager.ts`
  (49,665 B), each HTTP 200 with digests equal to the tarball copies.
- One extra upstream fetch for §5.7: `https://github.com/can1357/oh-my-pi/commit/476b858b3a4abe6f6c8a06c252c23961be41e912.patch`
  with `Accept: application/vnd.github.patch` → HTTP 200, 76,782 B, sha256 `00f6cbb0…b571257`
  (the GitHub commits API returned `API rate limit exceeded` for this host, so commit metadata was
  read from the patch header: `Date: Sun, 22 Feb 2026 12:44:23 +0100`).
- §5.9: six raw tag fetches of `packages/coding-agent/src/sdk.ts` (v12.17.2, v12.18.3, v12.19.0,
  v13.3.4, v13.3.5, v18.12.6 — each HTTP 200) plus two raw tag fetches of
  `packages/coding-agent/CHANGELOG.md` (v12.19.0, v13.3.5 — each HTTP 200), all grepped for
  `Math.min(100` and the async-job lines.
- §5.10: one more patch fetch, `…/commit/3ce6a68380f11d6ba3c32133d1660bd58a3bb346.patch` →
  HTTP 200, 76,782 B, sha256 `1c2f996e37f3d8c235df4d8589b1347a088d38d5182c14008b832a37f86b50cc`
  (corrected receipt: an earlier draft of this report dropped the leading `1c`; see §5.10),
  `diff`ed against the `476b858` patch (1 changed line).
- §5.11: four raw tag fetches of `packages/coding-agent/src/async/job-manager.ts` (v12.19.0, v13.3.5,
  v18.4.0, v18.12.6 — each HTTP 200) and four of `packages/coding-agent/src/sdk.ts` (v14.0.0, v18.3.0,
  v18.4.0, v18.12.6 — each HTTP 200), grepped for `DEFAULT_MAX_RUNNING_JOBS`, the function-shaped
  option type, the `typeof option === "function"` branch, and both sdk.ts forms.
- `python3` (stdlib only) for HTML→text extraction, regex hit counts and byte probes;
  `grep`/`sed` over fetched files and over the unpacked tag tree; `tar -xzf` of the upstream tag
  tarball (76,414,434 B, sha256 `d5c557d2150ac7181d983d6300cfa4f02eab117667a4a5d8b0d4a268059c377e`)
  into `/tmp/omp-src/` for the line-anchored reading of `sdk.ts`, `tools/settings.ts`,
  `async/job-manager.ts`, `docs/settings.md`, `docs/tools/eval.md`.
- GitHub REST read-only: `repos/can1357/oh-my-pi/issues/{14636,14967}`,
  `repos/can1357/oh-my-pi/pulls/14634`, `search/issues?q=repo:can1357/oh-my-pi+…`,
  `repos/Daxiongmao87/oh-my-pi-termux/issues?state=all`.
- **Tool installs this seat: none** (no `pacman`, no `uv tool install`, no `npm -g`). Nothing was
  upgraded. The `curl`/`python3`/`git`/`tar` used were already present on the host.
- **No lane commits, no `jj`/`git` writes, no `omp` run, no settings edit.** The only write inside
  the lane repository is this report file.
