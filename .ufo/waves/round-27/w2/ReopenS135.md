# ReopenS135 — re-open of SOURCES row S135 (oh-my-pi task/workpool.ts at 45c35e40)

Seat: MoriR27.ReopenS135 (leaf; no subagents, no background jobs). Lane: /home/vgpnk/Projects/shokunin/mori-shokunin.
Tip under test: 5f00fd045c137b7e3835506d69946cfd9d010eb5 (master). Access date: 2026-10-22 (UTC).
Scratch (not in the lane): /fast/scratch/hyaku/mori-r27/ReopenS135/.

## 1. Verdict in brief

- Fetch, size, sha256, tag-to-commit, anchors :175 and :363, duplicate check and row identity: **hold**.
- Row `teaches`, second clause ("both draw on the same session-wide cap"): **wrong for the pool job**. The pool job is
  registered with `queued: true` and its body never calls `markRunning()`, so it never counts toward the running cap.
  Only the batch job counts (workpool.ts:204, :367, :424; job-manager.ts:367, :393).
- Lane statements that rely on S135:
  - SKILL.md:659 (row 2) says `workpool()` "do raise the refusal". **High, wrong for batch registrations.** It holds
    for the pool job only.
  - SKILL.md:660 (row 3) says "a batch can partially start" and "refusals and starts coexist in one result" for a
    `workpool()` batch. **Medium, wrong for workpool.**
  - ReviewR7Knowledge.md:64 and :159 cite "S135" for commit 6962d5cd. **Medium, wrong ID collision.** Registry S135 is
    workpool.ts; that commit is S140.
  - The rest hold or have wording gaps (§7).
- New, code-read only and not exercised (§8): a refused registration can strand items in `queued` or `running` state,
  and a refused batch never reaches the `push()` caller. [INFERENCE]

## 2. Fetch and hash record

| item | source | access (UTC) | bytes | HTTP | sha256 | result |
|---|---|---|---|---|---|---|
| S135 URL (the only URL the row names) | https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/task/workpool.ts | 2026-10-22T17:10:40Z | 22,838 | 200 | 8cc4b17def435db43d49294dbc67946585c009832d3faf0b21aebaed59be6dc6 | equals SOURCES.md:141 and ReviewR3SkillRows.md:24 (prefix `8cc4b17d…6dc6`) |
| dependency (same commit) | …/packages/coding-agent/src/async/job-manager.ts | 2026-10-22, after 17:10:40Z | 49,665 | 200 | 0f37afaaa822ef1de845b8eb21473a70210176ff61e2dcff5925f85ec0e544e7 | equals the hash in corpus/knowledge/harness-job-capacity-r25.md line 2 |
| tag check | https://api.github.com/repos/can1357/oh-my-pi/git/refs/tags/v18.12.6 | 2026-10-22 | — | 200 | — | `object.sha` 45c35e40c46166dc726ccc52f5d27f40f2449f99, type commit |
| whole-tree check | https://codeload.github.com/can1357/oh-my-pi/tar.gz/45c35e40c46166dc726ccc52f5d27f40f2449f99 | completed 2026-10-22T17:15:25Z | 76,435,207 | 200 | 645df2d527de1b0ff62514ac14250230622439d5d5e84f781ffa06d38415b8d0 | equals ReviewR3SkillRows.md §1; 1,441 `.ts` files under packages/coding-agent/src |

Tools: curl, tar, sha256sum, wc and date (pre-existing); git read-only (`grep`, `show`, `diff`, `log`, `ls-tree`); the
grep and read tools for line-numbered search on the fetched bytes; eval (Python subprocess) only to write `git show`
copies to scratch. No installs, upgrades or pacman use in this seat.
`lsp` is not available: `xd://lsp` returned "No such tool: xd://lsp. Mounted devices: ast_edit, debug". Caller checks
below are therefore textual line-numbered searches over the extracted tree, not semantic references.

## 3. Row S135 at the tip (corpus/SOURCES.md:141), cell by cell

| cell | row says | evidence | verdict |
|---|---|---|---|
| id | S135 | `git grep -n 'S135' 5f00fd04` gives one registry row (:141) | holds |
| source | oh-my-pi task/workpool.ts at v18.12.6, one URL | URL fetched, HTTP 200, §2 | holds |
| kind / tier | code / A | upstream source file | holds |
| scope | "how workpool() registers its pool job and its batch with the async job manager: both register without a capacity check; v18.12.6 only" | see §4 and §7 C2 | holds, wording gaps (low) |
| anchor | ":175 (pool job registration), :363 (batch registration)" | §4 | holds; omits `queued: true` (:204) |
| teaches | "A pool is one registration and a batch is another; both draw on the same session-wide cap without pre-checking it." | §5 | **wrong clause** (medium) |
| status | mined | lesson line 78 Gate: "admit, A, mined (as S134)" | holds |
| opened | 2026-10-22 | §2 fetch date | holds |
| recheck | on-release | same as the other upstream code rows | holds |
| used-by | SKILL.md | SKILL.md:659 cites `task/workpool.ts:175,363`; `corpus/knowledge/harness-job-capacity-r25.md` has no S135 (grep at tip) | holds |

## 4. Anchors and quotes (line-numbered search on the fetched bytes, 45c35e40)

| anchor | bytes at that line | enclosing code | verdict |
|---|---|---|---|
| :175 | `const id = manager.register(` | `#ensurePoolJob()`, :169–210 | holds (pool job registration). Options at :204: `{ id: this.name, ownerId: this.ownerId, queued: true },` |
| :363 | `const jobId = manager.register(` | `#startTurn()`, :355–429 | holds (batch registration). Options at :424: `{ id: batch.id, agentId: agent.id, ownerId: this.ownerId },` (no `queued`) |
| all `register(` calls in workpool.ts | exactly two hits: :175 and :363 | whole file | holds |
| `markRunning` in workpool.ts | :366 (destructured) and :367 (`markRunning();`), both in the batch body | the pool body (:178–203) takes only `{ signal }` | pool job is never marked running |
| capacity words in workpool.ts | `capacity` and `atCapacity` do not appear; the words used are `limit()` (:147–150, the pool worker ceiling from `task.maxConcurrency`), checked at :264 and :280 | — | no job-manager capacity pre-check (holds); "capacity" also names the pool worker ceiling |

The row has no quotes. The lesson Gate row (line 78) gives line numbers only.

## 5. The teaches clause against the job manager (job-manager.ts, same commit)

- job-manager.ts:118–121 (doc): "Queued jobs do not count toward the running-job limit until the caller invokes
  `markRunning()` from the run context."
- job-manager.ts:367: `if (existing.status === "running" && !existing.queued) activeCount++;` (the count in `register()`);
  :343 is the same rule in `atCapacity` (:338–345).
- job-manager.ts:384 `status: "running",` and :393 `queued: options?.queued === true,`. The pool job's status therefore
  reads "running" while `queued` stays true, so :367 excludes it.
- job-manager.ts:369–374: the refusal throws whenever the count reaches the cap. It does not test the new job's `queued`,
  so the pool job's registration at workpool.ts:175 can be refused, but it never holds a slot.
- Batch job: no `queued` option (workpool.ts:424), so `queued` is false (job-manager.ts:393) and it counts from
  registration.
- Conclusion: both registrations face the same `register()` check, which is what "without pre-checking it" and "same
  cap" can honestly mean. "Both draw on the cap" is wrong for the pool job. The lane's own row 3 (SKILL.md:660) states the
  population as "every **running, non-queued** job", which matches these bytes and contradicts the teaches clause.

**Correction route.** QUALITY criterion 81 (corpus/QUALITY.md:373–374) says a row's `teaches` cannot change in place; the
correction is a new row whose `teaches` opens `supersedes S135 —`, with old → new logged in the round-27 lesson. Proposed
row (the owner confirms the number; S142 is the next free id at the tip, since SOURCES.md:147 is S141):

- `teaches`: "supersedes S135 — A pool is one queued registration: its `queued` flag stays true (workpool.ts:204) and its
  body never calls `markRunning()`, so it is not counted toward the running cap, although its status reads running
  (job-manager.ts:384). A batch is one registration that counts from registration (workpool.ts:363, :424). `register()`
  refuses either when the cap is full (job-manager.ts:369–374, which has no queued exemption). Neither pre-checks the cap."
- `scope`: "how the WorkPool class registers its pool job and its batch jobs with the session's job manager; v18.12.6 only."
- `anchor`: ":175 (pool registration), :204 (`queued: true`), :363 (batch registration), :367 (`markRunning()`, batch body
  only); HTTP 200, 22,838 B, sha256 8cc4b17def435db43d49294dbc67946585c009832d3faf0b21aebaed59be6dc6. The count and
  refusal rules are stated in S098 (corpus/SOURCES.md:104); its anchors were not re-verified here."

## 6. Duplicates and row identity

- Only one registry row cites workpool.ts. At the tip, `grep -n workpool corpus/SOURCES.md` hits :109 (S103 prose,
  "`workpool()` pools") and :141 (S135). The row is not a duplicate of an older row's file.
- History: `git log -S workpool.ts -- corpus/SOURCES.md` lists 79ecf58b only (the row's introduction). The round-26 draft
  proposed the same text as id S119 (.ufo/waves/round-26/w1/DraftHygieneKnowledge.md:222). That id was not admitted;
  registry S119 is earlyoom main.c (SOURCES.md:125).
- In-place edits: `git diff -U0 79ecf58b 5f00fd04 -- corpus/SOURCES.md` adds only S138–S141 (hunk `@@ -143,0 +144,4 @@`).
  Line 141 is unchanged, so S135 keeps its first-published cells (QUALITY 81 identity holds by diff; the lane's
  `check-row-identity.py` was not run).

## 7. Citing statements: verdict per statement

| # | location (tip) | statement | verdict | severity | correction |
|---|---|---|---|---|---|
| C1 | corpus/SOURCES.md:141 `teaches` | "both draw on the same session-wide cap" | wrong for the pool job | medium | new row (§5) |
| C2 | corpus/SOURCES.md:141 `scope` | "both register without a capacity check" | holds; wording | low | say "without a caller-side capacity check" (register() applies it, job-manager.ts:369–374); say the file's `limit()` is the pool worker ceiling (:147–150) |
| C3 | SKILL.md:646 | "rows 2–3 also S134, S135, S136" | holds as a union | low | optional: "row 2 also S134, S135; row 3 also S136" (row 2 cites agent-bridge.ts:210, workpool.ts:175,363; row 3 cites task/index.ts:1191–1219, :1233–1236) |
| C4 | SKILL.md:659 (row 2) | "eval `agent()`, `workpool()` and an explicit `async: true` bash reach `register()` with no `atCapacity` check and do raise the refusal (…`task/workpool.ts:175,363`…)" | **holds for the pool job; wrong for batches** | **high** | see below |
| C5 | SKILL.md:660 (row 3) | "a batch can partially start, so refusals and starts coexist in one result" (trigger names an eval `workpool()` batch) | wrong for workpool | medium | see below |
| C6 | corpus/lessons/round-27.md:78 (Gate) | "`:175,363` … admit, A, mined (as S134)" | holds | low | no located quote (other Gate rows carry one); add `const id = manager.register(` (:175) and `const jobId = manager.register(` (:363) and log the S142 supersession |
| C7 | .ufo/waves/round-27/w1/ReviewR3SkillRows.md:24 | `src/task/workpool.ts | 22,838 | 8cc4b17d…6dc6` | holds | — | none |
| C8 | ReviewR3SkillRows.md:84–86 | "`workpool()` registers twice, no pre-check", anchors :169–175 and :355–363 | holds; incomplete | low | add "(`queued: true`, :204; no `markRunning()` in the pool body)" |
| C9 | ReviewR7Knowledge.md:64, :159 (also :63, :74–75, :157–160) | "(S135, S136)" and "S135 \| oh-my-pi commit 6962d5cd…" | **wrong ID** | medium | S133→S138, S134→S139, S135→S140, S136→S141 (lines 63–64, 74–75, 157–160); line 25 "next free id is S133" → S142 |
| C10 | corpus/knowledge/harness-job-capacity-r25.md:95–96 (does not cite S135; adjacent) | "every background job in the session shares one cap" | overstated for a parked pool job | low | "every running, non-queued background job shares one cap" (workpool.ts:204; job-manager.ts:367) |
| C11 | .ufo/waves/round-25/w2/CriticHarnessOverclaim.md:132–134 (does not cite S135) | `task/workpool.ts:204` is a `queued: true` site; `:363` counts from registration | holds | — | none |
| C12 | .ufo/waves/round-26/w1/DraftHygieneKnowledge.md:222 (draft id S119; not a citation of S135) | the teaches text is the same as S135's | origin of C1 | — | none; the anchors were re-verified in round 27 but the `queued` flag was not |

**C4 detail.** The quoted sentence holds for the pool job. The throw from `register()` (workpool.ts:175) escapes
`#ensurePoolJob()` and `push()` (:164). `push()` is called by `runEvalWorkpool` (eval/workpool-bridge.ts:114), which does
not catch it, and the JS and Python wrappers do not catch either (eval/js/shared/prelude.txt:487–497;
eval/py/prelude.py:1067–1074). The Python `_bridge_call` raises `RuntimeError` when the bridge returns `ok` false
(prelude.py:471–473). So the script caller sees a pool-job refusal.
It does not hold for batches. A batch refusal from `#drain` → `#startTurn` (workpool.ts:344 → :363) escapes
`#dispatch`, and `#queueDispatch` catches it and only logs it (workpool.ts:231–239; `logger.warn` at :233). `push()` has
already returned the item ids (:165–166), so the caller gets no error. A refusal during a follow-up turn is thrown out of
`#finishTurn` (`#drain(agent)` at :499 sits outside the try blocks at :458–488) and fails the finishing batch job
(job-manager.ts:431–439). Neither path reaches the `push()` caller. **Correction (in place; SKILL.md is not a SOURCES
row):** replace "reach `register()` with no `atCapacity` check and do raise the refusal (`docs/tools/eval.md:258`;
`eval/agent-bridge.ts:210`; `task/workpool.ts:175,363`; `tools/bash.ts:1188-1209`)" with "reach `register()` with no
`atCapacity` check and do raise the refusal (`docs/tools/eval.md:258`; `eval/agent-bridge.ts:210`;
`tools/bash.ts:1188-1209`); `workpool()` raises it to its caller only when the pool job registers
(`task/workpool.ts:164,175`), while a batch refusal (`task/workpool.ts:363`) is caught and logged
(`task/workpool.ts:231–239`) or fails the batch that was finishing (`task/workpool.ts:499`; `job-manager.ts:431–439`)".
The `agent()` and bash clauses were not re-verified here (S134 and the bash rows are outside this re-open).

**C5 detail.** For `workpool()`, one batch is one registration: `#drain` splices the agent's whole queue into one batch
(workpool.ts:324) and calls `#startTurn` once (:344), which registers once (:363). So a batch cannot partially start.
The sentence holds for task spawns (S136, `task/index.ts:1191–1219`). **Correction (in place):** after "so refusals and
starts coexist in one result (`task/index.ts:1191-1219`, `:1233-1236`)" add "; a `workpool()` batch is one registration
(`task/workpool.ts:324`, `:363`), so it refuses whole, and its refusal is not returned to the `push()` caller
(`task/workpool.ts:231–239`)". Also change "a batch can partially start" to "a task-spawn batch can partially start".

## 8. Refusal path read from the bytes (not exercised; [INFERENCE] from code)

Omp was not run (bounds), and no sandbox harness was built. These are code-reading findings for the owner to test.

- **O1 — batch refused on first dispatch.** `#drain` sets each item to `running` (workpool.ts:334–338), the agent to
  `running` (:339–340) and records the batch (:341) before `#startTurn` registers (:344 → :363). After a refusal those
  items stay `running`. The catch at :231–239 changes only items still `queued` (:232), so none become `failed`, and
  `#isDrained()` (:219–221) never becomes true. `status()` (:552–570) would keep reporting them as running.
- **O2 — pool job refused.** `#poolJobStarted` is set before the register (:174 → :175). After a refusal it stays true, so
  later `push()` calls skip `#ensurePoolJob()` (:170). Items added in the failing call (:157–163) are never passed to
  `#queueDispatch` (:165 is skipped). The only other callers of `#queueDispatch` are :494 and :508, which take items from
  the fresh queue and the stranded-agent queue, so these items stay `queued` forever.
- **O3 — follow-up batch refused.** `#finishTurn` → `#drain` (:499) → refusal fails the finishing batch job
  (job-manager.ts:431–439). Whether that failure is delivered depends on the watch and delivery rules
  (job-manager.ts:568 `watchJobs`, :581 `unwatchJobs`, doc :578–579). Not traced.

## 9. Residual risk and verification gaps

- No runtime test. O1–O3 rest on reading the bytes at the cited lines.
- The host-side handler that converts a thrown error into `ok: false` for `__workpool__` was not traced.
- Caller checks were textual searches over the extracted tree, not semantic references (no lsp).
- SOURCES rows S098 and S099 and the knowledge entry were read at the cited lines only; their anchors were not re-verified.
- S135's Gate row gives no located quote, and ReviewR3SkillRows §3 quotes tokens only. This is documentation risk, not an
  error in the row.
- `check-row-identity.py` was not run; S135's identity was shown by `git diff` (§6).

## 10. Checks for the main agent after any fix

- `python3 -I -B .ufo/waves/round-27/check-row-identity.py 5f00fd04` must print `changed=0`, exit 0, with S135 unchanged
  and the correction in a new row.
- Re-open the S135 URL and confirm the sha256 if the row's URL changes.
- Lint this report and any edited report for host identifiers before commit (QUALITY 82 pattern), as the lane requires.
- Owner decision needed: whether to add the S142 row, and whether to test O1–O3 in a clone under scratch (not in the lane).
