# SrcClampSite — upstream clamp-site row for C2 (omp 18.12.6)

Seat `MoriR25.SrcClampSite`, round 25 wave 1, 2026-10-22. Read-only scout/scribe seat.
Nothing in the lane was edited: no `corpus/SOURCES.md` change, no lesson edit, no tool install, no
omp run, no git/jj write, no `~/.omp` read of settings content. Scratch bytes live in `/tmp`; this
report file is the only lane write.

## 1. What this seat was asked for, and what it delivers

Assignment: draft one `corpus/SOURCES.md` row plus a `## Gate` block for the upstream oh-my-pi file
that constructs `AsyncJobManager` with `maxRunningJobs: () => Math.min(100, ...)`, and check
whether the clamp was introduced recently (git history / blame via GitHub), quoting the commit
message if found.

Delivered below:

1. The upstream file is **`packages/coding-agent/src/sdk.ts`** (not a `session/sdk*` file), at tag
   `v18.12.6` = commit `45c35e40c46166dc726ccc52f5d27f40f2449f99`. Draft row + `## Gate` block in §5.
2. The clamp is **not recent**. It dates to **2026-02-22** (the feature commit that created async
   background jobs), and the *live* form used by the shipped binary dates to **2026-09-24**. Full
   commit-by-commit history with quotes in §4.
3. The `parentTaskPrefix` guard is a **separate, later** change: the guard first appears
   **2026-05-12**, and its current one-clause shape dates to **2026-10-10**. §4.3.

Everything below is a fact observed by a command in this session; inference is marked `[INFERENCE]`.

## 2. Upstream file identification (facts)

| Fact | Evidence (command → observed) |
|---|---|
| `v18.12.6` = commit `45c35e40c46166dc726ccc52f5d27f40f2449f99` | `git ls-remote --tags https://github.com/can1357/oh-my-pi` → `45c35e40c46166dc726ccc52f5d27f40f2449f99 refs/tags/v18.12.6`; `git log -1 --format='%H %ad %s' --date=iso v18.12.6` → `45c35e40c46166dc726ccc52f5d27f40f2449f99 2026-10-21 22:49:59 +0200 chore: bump version to 18.12.6` |
| The clamp site is `packages/coding-agent/src/sdk.ts` | `grep -rn 'maxRunningJobs' --include='*.ts'` in the cloned tree at `v18.12.6` → the only non-test, non-declaration hit is `packages/coding-agent/src/sdk.ts:2284` |
| It is the **only** `AsyncJobManager` construction in the shipped source | `git grep -n 'new AsyncJobManager(' v18.12.6 -- packages/coding-agent/src` → exactly one hit: `v18.12.6:packages/coding-agent/src/sdk.ts:2283` |
| The clamp appears exactly once in the source tree | `git grep -n 'Math\.min(100' v18.12.6 -- packages/coding-agent/src` → 9 hits, of which exactly one is a job cap (`sdk.ts:2284`); the other 8 are unrelated (usage reserve pct, slow-mode percentage, downloader percent, browser timeouts) |
| Raw bytes at the tag and at the commit are identical | `curl -o sdk_pinned.ts https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40…/packages/coding-agent/src/sdk.ts` → HTTP 200, 255,525 bytes, sha256 `c0228addd4cfe93cfd370c7248e9db29743f0fa802aea0e1d1adf4994dbe6957`; `curl -o sdk_v18126.ts …/v18.12.6/packages/coding-agent/src/sdk.ts` → HTTP 200, same size, same sha256; `diff -q` → identical |

### 2.1 The construction site, verbatim (lines 2279–2286 at `v18.12.6`)

```
2279		// Every root owns its jobs and delivery sinks, even when another root is live.
2280		// Children use the exact manager passed by their parent; the singleton remains
2281		// only a legacy pointer to whichever root first installed it, never a routing fallback.
2282		const asyncJobManager = !options.parentTaskPrefix
2283			? new AsyncJobManager({
2284					maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)),
2285				})
2286			: undefined;
```

Supporting anchors: `sdk.ts:53` `import { AsyncJobManager } from "./async";`; `sdk.ts:326`
`cfgAsyncMaxJobs,` inside the `./tools/settings` import block; `sdk.ts:2284` is the clamp line.

## 3. The ≤25-word quote for the Gate block

Both the 100 clamp and the `parentTaskPrefix` guard, in one located quote, line-folded to single
spaces (12 words):

> `const asyncJobManager = !options.parentTaskPrefix ? new AsyncJobManager({ maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)),`

Located: `packages/coding-agent/src/sdk.ts:2282-2284` at tag `v18.12.6` =
`45c35e40c46166dc726ccc52f5d27f40f2449f99`.

The clamp expression alone (5 words), for a narrower quote if the L1 prefers one:

> `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)),`

Word count check: `awk 'NR>=2282 && NR<=2284' sdk_v18126.ts | tr -d '\n' | wc -w` → `12`.

## 4. Was the clamp introduced recently? (git history / blame via GitHub)

**Answer: no for the clamp itself, yes for the live-re-read form.** The 100 ceiling is old; the
*shipped* expression `() => Math.min(100, cfgAsyncMaxJobs.get(settings))` and the current
`parentTaskPrefix` guard are both recent. `git blame -w -L 2282,2284 v18.12.6` attributes the
three lines to three different commits, which is the reason a naive blame of the current line
misleads: the **number 100** is inherited, the **closure shape** and the **guard** are new.

### 4.1 The clamp's origin — 2026-02-22, the async-background-jobs feature commit

`git log --oneline -S 'Math.min(100, Math.max(1, settings.get("async.maxJobs")' --reverse` over
the whole `sdk.ts` history returns exactly two commits, one per upstream lineage (see §4.4):

- `476b858b3a4abe6f6c8a06c252c23961be41e912` — *ancestor of `v18.12.6`: YES*
- `3ce6a68380f11d6ba3c32133d1660bd58a3bb346` — *ancestor of `v18.12.6`: NO*

Commit message (identical for both; GitHub API `…/commits/476b858b3a4abe6f6c8a06c252c23961be41e912`
→ HTTP 200, author date `2026-02-22T11:44:23Z`):

> `feat(coding-agent): added async background job execution with configurable concurrency limits`

Body bullet (first line of the body):

> `- Added async.enabled and async.maxJobs settings to control background job execution behavior.`

The clamp arrived in that commit's diff as (`feat.patch` hunk, `packages/coding-agent/src/sdk.ts`):

> `+	const asyncMaxJobs = Math.min(100, Math.max(1, settings.get("async.maxJobs") ?? 15));`

So the **ceiling of 100 was present at the very first release of the feature**; only the *fallback
default* was 15 at that moment. First release tags carrying the clamp: `v12.19.0` (2026-02-22,
lineage A) and `v15.1.9` (2026-05-21, lineage B) — `git tag --contains … | sort -V | head -2`.
`v12.18.3`'s `sdk.ts` has **0** occurrences of `async.maxJobs`
(`curl …/v12.18.3/packages/coding-agent/src/sdk.ts | grep -c 'async.maxJobs'` → `0`).

### 4.2 Default raised 15 → 100 — 2026-02-26 (four days after the feature)

Same pickaxe on the fallback literal returns the paired commit:

- `944d7f8d8d44d889b77f1865f394afd1dfb48c86` — *ancestor of `v18.12.6`: YES*
- `d38e1d55e1b205b5bd76a9174b0ba85b31c1668c` — *ancestor of `v18.12.6`: NO*

Commit message (GitHub API HTTP 200, author date `2026-02-26T11:34:29Z`):

> `feat(coding-agent): increased async max jobs limit to 100 for concurrency`

Body bullet:

> `- Increased default async max jobs limit from 15 to 100 for improved concurrent task handling.`

Diff hunk (`git show d38e1d55e1 … -- packages/coding-agent/src/sdk.ts`):

```
-	const asyncMaxJobs = Math.min(100, Math.max(1, settings.get("async.maxJobs") ?? 15));
+	const asyncMaxJobs = Math.min(100, Math.max(1, settings.get("async.maxJobs") ?? 100));
```

### 4.3 The shipped closure shape and the `parentTaskPrefix` guard — 2026-09-24 and 2026-10-10

`git blame -w -L 2282,2284 v18.12.6 -- packages/coding-agent/src/sdk.ts` (verbatim):

```
9ce580c11e (roboomp 2026-10-10 16:16:27 +0000 2282) 	const asyncJobManager = !options.parentTaskPrefix
6962d5cd2e (can1357 2026-09-24 20:04:41 +0200 2283) 		? new AsyncJobManager({
c4a2441d8f (can1357 2026-09-25 01:02:43 +0200 2284) 				maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)),
```

Three upstream commits, each with its message (GitHub API HTTP 200 for each):

| Commit | Date | Message (quoted subject line) | What it changed at this site |
|---|---|---|---|
| `6962d5cd2ef157ebf9f415acd58b8744f66400d8` | 2026-09-24 | `feat: implemented centralized settings registry and internal URL routing` | Replaced the eager constant with the live closure `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings) ?? 100)` and added the comment `// Re-read per capacity check so \`async.maxJobs\` resizes the cap live.` |
| `c4a2441d8f9195de810b3492be5bf5673cecf9c9` | 2026-09-25 | `feat: centralized configuration registry and internal URL routing` | Dropped the now-redundant `?? 100` fallback, giving today's `Math.min(100, cfgAsyncMaxJobs.get(settings))` |
| `9ce580c11eb330b1c41939acf9e4c6aee160a1a8` | 2026-10-10 | `fix(sdk): isolated async jobs for concurrent roots` | Simplified the guard from `!options.parentTaskPrefix && !AsyncJobManager.instance()` to the current one-clause `!options.parentTaskPrefix` |

Neither `6962d5cd`'s nor `9ce580c11e`'s message mentions the number 100 or the cap; both messages
are about other concerns (settings registry; concurrent-root isolation). The number 100 is
therefore **not** attributable to either of them by message — only by the diff and by §4.1.

Guard history (same method): the `parentTaskPrefix` clause on the construction first appears in
`ec649278bd2105b872e7866f188d75cbfc7dce3c` (2026-05-12, message
`fix(coding-agent): resolved async job owner filters for scoped cancelAll`, body line
`- Updated session handoff and disposal so subagents inherit the parent manager, top-level sessions own it, and teardown cancels own jobs only.`),
whose diff adds `backgroundJobsEnabled && !options.parentTaskPrefix` before the constructor. The
`&& !AsyncJobManager.instance()` clause was added by
`36db2530a98fa2b78b5c85fde49671bccea067b5` (2026-06-05, message
`fix(sdk): keep primary AsyncJobManager when secondary top-level session disposes`) and removed
again by `9ce580c11e` (2026-10-10). All three are ancestors of `v18.12.6`.

### 4.4 Upstream history has two lineages (why two commit SHAs for one change)

`git merge-base --is-ancestor` results:

| Tag | ancestor of `HEAD` | contains `476b858b3a4a` (feature) | contains `3ce6a68380` (feature twin) |
|---|---|---|---|
| `v12.19.0` | NO | NO | YES |
| `v13.0.0` | NO | NO | YES |
| `v14.0.0` | NO | NO | YES |
| `v15.0.0` | NO | NO | YES |
| `v15.1.8` | NO | NO | YES |
| `v15.1.9` | YES | YES | NO |
| `v18.12.6` | YES | YES | NO |

`git merge-base --is-ancestor v15.1.8 v15.1.9` → NO: the tag series splits at `v15.1.8`/`v15.1.9`.
The two feature commits carry the same message, the same author timestamp (`2026-02-22T11:44:23Z`
/ `12:44:23 +0100`) and byte-identical patches: `diff` of the two `.patch` downloads differs only
in the `From <sha>` header line (patch sha256 `00f6cbb0…` vs `1c2f996e…`; bodies identical).
`[INFERENCE]` the upstream project rewrote/rebased its history and re-published the release tags,
so a commit hash alone does not identify "the" introduction; both SHAs are the same logical change.
Practical consequence for this round: quote the **message and date**, not a bare hash, when
attributing the clamp's origin.

### 4.5 Upstream prose agrees, and states a maximum

`docs/tools/eval.md:258` at `v18.12.6` (found via `git grep -n -i 'maxJobs' v18.12.6 -- docs/`),
one sentence, quoted in part:

> `every handle is a running background job counted against the session-wide \`async.maxJobs\` cap (default and maximum 100)`

and `docs/settings.md:623`:

> `| \`async.maxJobs\` | number | \`100\` | Running background-job cap, floored to at least 1; parked/queued jobs do not consume execution slots. |`

(The `docs/settings.md` row is a **sibling seat's** row — `MoriR25.UpstreamTagLocate` S101 and
`MoriR25.SrcRejections` S106 — not mine; recorded here only because the upstream docs are the
corroborating surface for the same fact.)

## 5. Draft SOURCES.md row + `## Gate` block (proposal only — SOURCES.md NOT edited)

### 5.1 Id space note (conflict to be resolved by the L1)

Measured current maximum in `corpus/SOURCES.md`: `S097` (97 rows). Sibling seats have claimed ids
in this wave: `MoriR25.UpstreamTagLocate` proposed **S098–S102**; `MoriR25.SrcJobManager` took
**S098** for `async/job-manager.ts` and recorded the agreement that **S099 = sdk.ts**,
**S100 = tools/settings.ts**, **S101 = docs/settings.md**, **S102 = the installed binary**;
`MoriR25.SrcRejections` proposed **S103–S117** (rejections). `MoriR25.UpstreamTagLocate`'s S099
covers the *same file* as this seat's assignment.

**Overlap, stated plainly:** the sibling's S099 already drafts a row for
`packages/coding-agent/src/sdk.ts` at v18.12.6 with the clamp quote. This seat's assignment is
the same file. Two rows for one file would violate the contract's append-only/no-duplicate
intent (`CORPUS.md` "SOURCES.md — where a shokunin learns", shape + rule 1), so the L1 has two
coherent options and I recommend the first:

- **Option A (recommended):** fold this seat's evidence into the existing **S099** row — the row
  stays one row per file; add the `parentTaskPrefix` clause to the quote and the two anchors
  (`:2282` guard, `:2284` clamp) plus the 2026-09-24 / 2026-10-10 provenance in the `anchor` cell.
  Nothing new needs a row id.
- **Option B:** keep this seat's row separate as a **provenance/history** row for the *upstream
  commit* rather than the file — the shape precedent exists in this registry (`S096` is a commit
  URL row: `https://github.com/torvalds/linux/commit/52b1364b…`). Under Option B the next free id
  after the wave's `S117` is **S118**.

I do **not** propose a third id: `S099` (file row) already exists as a proposal, and inventing a
second file row for `sdk.ts` would be the duplicate the contract warns about.

### 5.2 Draft row (Option A — the amendment text for S099)

Column order is the frozen contract's: id | source | kind | tier | scope | anchor | teaches |
status | opened | recheck | used-by.

```
| S099 | oh-my-pi sdk.ts at v18.12.6 — https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/sdk.ts | code | A | the single shipped construction of AsyncJobManager at v18.12.6: the 100 clamp on async.maxJobs and the parentTaskPrefix guard that keeps the manager to root sessions only; upstream source at the tag matching omp 18.12.6 only; not the job manager's own default, not the setting schema, not the running-job count | sdk.ts:2282-2284 (guard :2282, clamp :2284); import of AsyncJobManager :53; cfgAsyncMaxJobs import :326; tag v18.12.6 = commit 45c35e40c46166dc726ccc52f5d27f40f2449f99; raw sha256 c0228addd4cfe93cfd370c7248e9db29743f0fa802aea0e1d1adf4994dbe6957; clamp lineage: introduced 2026-02-22 by 476b858b3a4a (twinned upstream as 3ce6a68380), default 15 to 100 on 2026-02-26 by 944d7f8d8d (twinned as d38e1d55e1), live closure 2026-09-24 by 6962d5cd2ef, fallback removed 2026-09-25 by c4a2441d8f, guard simplified 2026-10-10 by 9ce580c11e | The 100 ceiling is a construction-site clamp on async.maxJobs, so no shipped root session exceeds 100 running async jobs whatever the config says; the clamp is not new (it ships with the 2026-02-22 async-background-jobs feature) and only its live re-read and the parentTaskPrefix guard are recent. | mined | 2026-10-22 | on-release | corpus/knowledge/harness-job-capacity-r25.md |
```

### 5.3 Draft row (Option B — a separate provenance row, id to be assigned by the L1)

```
| S118 | oh-my-pi async background job execution feature commit — https://github.com/can1357/oh-my-pi/commit/476b858b3a4abe6f6c8a06c252c23961be41e912 | code | A | the upstream introduction of async background job execution and of the 100 ceiling on async.maxJobs, dated 2026-02-22, with the fallback default 15; the introduction commit only, not later behaviour | sdk.ts added line "const asyncMaxJobs = Math.min(100, Math.max(1, settings.get(\"async.maxJobs\") ?? 15));"; commit message subject and first body bullet; commit 476b858b3a4abe6f6c8a06c252c23961be41e912 (authored 2026-02-22T11:44:23Z); twinned upstream commit 3ce6a68380f11d6ba3c32133d1660bd58a3bb346 on the pre-v15.1.9 tag lineage; patch sha256 00f6cbb0b786dd8416e3c764d90e51b159bde6873bd1f7e955f5fd847b571257; first release tag carrying the clamp v12.19.0 (2026-02-22) | The 100-job ceiling is original to the feature that introduced async background jobs on 2026-02-22, with a fallback default of 15 that was raised to 100 four days later; upstream history carries the same change under two commit SHAs across a tag-lineage split, so attribution must cite message and date. | queued | 2026-10-22 | on-release | — |
```

### 5.4 Draft `## Gate` block for the round-25 lesson

Shape follows `corpus/lessons/round-24.md:18-32` (id | URL | accessed | anchors verified | located
quote), with the HTTP status and sha256 spelled out because the assignment asks for both.

```markdown
## Gate — C2 upstream clamp site (wave-1 scribe seat MoriR25.SrcClampSite)

Opened 2026-10-22. Tag `v18.12.6` = commit `45c35e40c46166dc726ccc52f5d27f40f2449f99`
(`git ls-remote --tags https://github.com/can1357/oh-my-pi`). All raw fetches HTTP 200; digests are
SHA-256 of the fetched bytes.

| id | URL | accessed (UTC) | HTTP / sha256 | anchors verified | located quote (≤25 words) |
|---|---|---|---|---|---|
| S099 | https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/sdk.ts | 2026-10-22 | 200 / c0228addd4cfe93cfd370c7248e9db29743f0fa802aea0e1d1adf4994dbe6957 (255,525 B) | 2282-2284 (guard :2282, clamp :2284); import :53; cfgAsyncMaxJobs :326 | 2282-2284 (line-folded, 12 words): "const asyncJobManager = !options.parentTaskPrefix ? new AsyncJobManager({ maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings))," |
| S118 | https://github.com/can1357/oh-my-pi/commit/476b858b3a4abe6f6c8a06c252c23961be41e912 | 2026-10-22 | 200 / patch sha256 00f6cbb0b786dd8416e3c764d90e51b159bde6873bd1f7e955f5fd847b571257 (76,782 B) | sdk.ts added line 726; commit message subject + first body bullet | "feat(coding-agent): added async background job execution with configurable concurrency limits" — body: "Added async.enabled and async.maxJobs settings to control background job execution behavior." |

Provenance (not separate rows): the clamp line descends from `476b858b3a4abe6f6c8a06c252c23961be41e912`
(2026-02-22, "feat(coding-agent): added async background job execution with configurable
concurrency limits"), its fallback default was raised 15 to 100 on 2026-02-26 by
`944d7f8d8d44d889b77f1865f394afd1dfb48c86` ("feat(coding-agent): increased async max jobs limit to
100 for concurrency"), the live closure arrived 2026-09-24 in `6962d5cd2ef157ebf9f415acd58b8744f66400d8`
("feat: implemented centralized settings registry and internal URL routing"), its `?? 100` fallback
was dropped 2026-09-25 in `c4a2441d8f9195de810b3492be5bf5673cecf9c9` ("feat: centralized
configuration registry and internal URL routing"), and the guard was simplified to
`!options.parentTaskPrefix` on 2026-10-10 by `9ce580c11eb330b1c41939acf9e4c6aee160a1a8` ("fix(sdk):
isolated async jobs for concurrent roots"). Upstream carries the 2026-02-22 feature under two SHAs
(`476b858b3a4a` on the v15.1.9+ lineage that reaches v18.12.6, `3ce6a68380` on the v12.19.0-v15.1.8
lineage); their patches are byte-identical apart from the `From` header. The 100 ceiling therefore
predates the recent commits by eight months, and the current blame of :2282-2284 reflects only the
recent edits.
```

Registry change proposed by this seat: **none in place.** The `sdk.ts` fact is already proposed as
**S099** by `MoriR25.UpstreamTagLocate`; this seat supplies the guard-inclusive quote, the extra
anchors, the provenance and the HTTP/sha256 evidence for that row, and offers the optional
separate provenance row (**S118**, id provisional) if the L1 prefers a commit-shaped row.

## 6. Cross-check against the installed binary (read-only, bytes only)

The clamp row must describe the shipped binary, so the source claim was checked against the bytes
of `~/.local/bin/omp` (256,702,432 B, sha256
`85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4`; the binary contains the
literal `18.12.6`, 9 occurrences). Read as bytes only; the binary was never executed.

- Contract rule 2 clamp regex over the binary bytes: **1 match, value 100**
  (`maxRunningJobs:\s*\(\)\s*=>\s*Math\.min\(\s*(\d+)\s*,\s*[\w$]+\.get\([\w$]+\)\s*\)`).
- Contract rule 3 setting regex: **1 match, value 100**
  (`id:\s*"async\.maxJobs",[^}]{0,300}?default:\s*(\d+)`).
- Raw binary text of the construction site: `maxRunningJobs: () => Math.min(100, XPe.get(R)` —
  the same expression as `sdk.ts:2284`, minified identifiers only.

[INFERENCE] The shipped binary is the v18.12.6 build of this source: the clamp, the setting default
and the version string all match the tag's bytes. The sibling seat `MoriR25.UpstreamTagLocate`
independently established byte identity with the GitHub release asset `omp-linux-x64`.

## 7. Facts vs inference vs gaps

**Facts** (each with a command in this report): the file and line of the clamp; the single
construction site; tag→commit resolution; raw byte identity of tag vs commit fetch and its sha256;
the 12-word guard+clamp quote; the full blame of lines 2282-2284 at the tag; the introduction,
default-change, closure, fallback-removal and guard-simplification commits with their messages,
dates and ancestry; the two-lineage split; the upstream docs sentences; the binary regex match
counts.

**[INFERENCE]** (marked, not asserted): that the two-lineage split is a history rewrite rather
than two independent implementations (evidence: identical message, identical author timestamp,
byte-identical patch bodies); that the shipped binary is the build of this tag (evidence: matching
clamp text, setting default and embedded version string).

**Gaps / limits:**
- Upstream history was **rewritten** across the `v15.1.8`/`v15.1.9` split, so "the commit that
  introduced the clamp" is two SHAs; message+date is the stable identifier, not the hash.
- No upstream issue or PR discussing the number 100 was opened; the 2026-09-24 and 2026-10-10
  commit messages do not mention the cap, so intent for the value itself is **not** evidenced by
  upstream prose — only the diffs and the docs sentences are.
- The `docs/tools/eval.md:258` and `docs/settings.md:623` sentences corroborate the cap but belong
  to sibling rows (S103/S106/S101); they are cited here as corroboration only.
- Nothing was verified about behaviour at runtime: no omp execution, no session, no observed job
  rejection. The cap claim is a source-and-bytes claim only.

## 8. Commands run, and tooling

Read-only upstream access: `git ls-remote`, `git clone --filter=blob:none --no-checkout` of
`https://github.com/can1357/oh-my-pi` into `/tmp/ohmypi-src` (scratch, outside the lane),
`git log`/`git show`/`git blame`/`git grep`/`git merge-base --is-ancestor`/`git tag --contains`
against that clone, `git checkout v18.12.6`; `curl` to `raw.githubusercontent.com`,
`github.com` (commit pages and `.patch`) and `api.github.com`; Python 3.14.8 stdlib for byte
regexes over `~/.local/bin/omp`.

Tools: git 2.56.0, curl 8.23.0, Python 3.14.8 — all already present on the host. **No tool was
installed, upgraded or removed this seat**, so nothing to record under the tooling directive; no
pacman transaction was attempted (host-wide pacman transactions are paused).

Lane discipline: no git/jj write, no `jj` command at the fleet root, no `~/.omp` file read or
write, no omp run, no edit to `corpus/SOURCES.md`, `corpus/lessons/round-25.md` or any other lane
file. The only file written in the lane is this report.
